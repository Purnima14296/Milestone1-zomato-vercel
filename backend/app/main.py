from __future__ import annotations

import logging
import os
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.dataset import (
    ingest_error,
    ingest_state,
    is_ingest_running,
    prepare_dataset_at_startup,
    resolve_dataset_path,
)
from backend.app.dataset_cache import warm_dataset_cache
from backend.app.paths import repo_root
from backend.app.pipeline import (
    default_dataset_path,
    list_dataset_cities,
    restaurants_browse,
    run_recommendations,
)
from backend.app.railway_env import (
    apply_railway_defaults,
    auto_ingest_if_missing,
    cors_allow_vercel,
    cors_has_production_access,
    cors_origin_regex,
    is_railway,
    railway_public_url,
)
from backend.app.schemas import RecommendationRequest
from zomato_rec.config import Settings
from zomato_rec.logging_config import configure_logging

logger = logging.getLogger(__name__)

_env_file = repo_root() / ".env"
if _env_file.is_file():
    load_dotenv(_env_file)

apply_railway_defaults()


def _package_version() -> str:
    try:
        from importlib.metadata import version

        return version("zomato-ai-reco")
    except Exception:
        return "0.1.0"


def _cors_origins() -> list[str]:
    # Default covers common Next.js dev ports; override with API_CORS_ORIGINS if needed.
    raw = os.getenv(
        "API_CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001",
    )
    return [o.strip() for o in raw.split(",") if o.strip()]


class _SlidingWindowLimiter:
    """Very small in-process limiter (per server instance)."""

    def __init__(self, max_events: int, window_seconds: float) -> None:
        self.max_events = max_events
        self.window = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        cutoff = now - self.window
        buf = self._hits[key]
        buf[:] = [t for t in buf if t >= cutoff]
        if len(buf) >= self.max_events:
            return False
        buf.append(now)
        return True


_rate_limiter = _SlidingWindowLimiter(max_events=60, window_seconds=60.0)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        if request.url.path.startswith("/api/") and request.method != "OPTIONS":
            host = request.client.host if request.client else "unknown"
            if not _rate_limiter.allow(host):
                return JSONResponse({"detail": "Too many requests. Try again shortly."}, status_code=429)
        return await call_next(request)


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    settings = Settings()
    configure_logging(settings.log_level)
    prepare_dataset_at_startup(settings=settings)
    if resolve_dataset_path().is_file():
        warm_dataset_cache()
    if is_railway():
        port = os.getenv("PORT", "(unset)")
        logger.info(
            "Running on Railway; bind=%s:%s public_url=%s",
            os.getenv("HOST", "0.0.0.0"),
            port,
            railway_public_url() or "(pending)",
        )
    yield


app = FastAPI(
    title="Zomato Recommendation API",
    description="Phase 7 — REST layer over Phases 2–4 (see Docs/phase_wise_architecture.md).",
    version=_package_version(),
    lifespan=_lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(RateLimitMiddleware)
# CORS outermost — required when the browser calls Railway directly (e.g. local debugging).
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_origin_regex=cors_origin_regex(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/api/health")


def _health_status(*, dataset_ok: bool, groq_configured: bool, dataset_loading: bool) -> str:
    if dataset_loading:
        return "starting"
    if dataset_ok and groq_configured:
        return "ok"
    return "degraded"


@app.get("/api/health")
def health() -> dict:
    settings = Settings()
    ds = resolve_dataset_path()
    cors_origins = _cors_origins()
    dataset_ok = ds.is_file()
    dataset_loading = is_ingest_running()
    groq_configured = bool(settings.groq_api_key)
    origin_regex = cors_origin_regex()
    payload = {
        "status": _health_status(
            dataset_ok=dataset_ok,
            groq_configured=groq_configured,
            dataset_loading=dataset_loading,
        ),
        "dataset_path": str(ds),
        "dataset_ok": dataset_ok,
        "dataset_loading": dataset_loading,
        "dataset_ingest_state": ingest_state(),
        "groq_configured": groq_configured,
        "groq_model": settings.groq_model,
    }
    if ingest_error():
        payload["dataset_ingest_error"] = ingest_error()
    if is_railway():
        payload.update(
            {
                "railway": True,
                "railway_url": railway_public_url(),
                "cors_origins": cors_origins,
                "cors_production_origin_configured": cors_has_production_access(cors_origins),
                "cors_origin_regex": origin_regex,
                "cors_allow_vercel": cors_allow_vercel(),
                "auto_ingest_if_missing": auto_ingest_if_missing(),
            }
        )
    return payload


@app.get("/api/metadata")
def metadata() -> dict:
    settings = Settings()
    ds = default_dataset_path()
    return {
        "pipeline_version": _package_version(),
        "groq_model": settings.groq_model,
        "hf_dataset_id": settings.hf_dataset_id,
        "processed_dataset": str(ds),
        "dataset_ok": ds.is_file(),
    }


@app.get("/api/locations")
def locations(limit: int = Query(default=500, ge=10, le=5000)) -> dict:
    """Distinct `city` values from the processed restaurants dataset."""
    try:
        locs = list_dataset_cities(limit=limit)
        return {"locations": locs, "count": len(locs)}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Could not load locations: {e}") from e


@app.post("/api/recommendations")
async def recommendations(body: RecommendationRequest) -> dict:
    try:
        out = await run_in_threadpool(run_recommendations, body)
        return out.model_dump()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Unhandled error in /api/recommendations")
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {e}") from e


@app.get("/api/restaurants")
def restaurants(
    location: str = Query(..., min_length=1, max_length=200),
    minimum_rating: float | None = Query(default=None, ge=0, le=5),
    budget_min: float | None = Query(default=None, ge=0),
    budget_max: float | None = Query(default=None, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict:
    try:
        rows = restaurants_browse(
            location=location,
            minimum_rating=minimum_rating,
            budget_min=budget_min,
            budget_max=budget_max,
            limit=limit,
        )
        return {"restaurants": rows, "count": len(rows)}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
