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
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.env import apply_render_defaults, is_render, render_service_url
from backend.app.paths import repo_root
from backend.app.pipeline import (
    default_dataset_path,
    list_dataset_cities,
    restaurants_browse,
    run_recommendations,
)
from backend.app.schemas import RecommendationRequest
from zomato_rec.config import Settings

logger = logging.getLogger("zomato_rec.api")

_env_path = repo_root() / ".env"
if _env_path.is_file():
    load_dotenv(_env_path)

apply_render_defaults()


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


def _cors_origin_regex() -> str | None:
    """
    Extra allowed origins beyond API_CORS_ORIGINS:
    - localhost (dev) unless disabled
    - *.vercel.app on Render (production + preview deploys) unless disabled
    """
    patterns: list[str] = []
    if os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip() not in {"1", "true", "yes"}:
        patterns.append(r"https?://(localhost|127\.0\.0\.1)(:\d+)?")
    allow_vercel = os.getenv("API_CORS_ALLOW_VERCEL_REGEX", "1" if is_render() else "0").strip()
    if allow_vercel not in {"0", "false", "no"}:
        patterns.append(r"https://[\w.-]+\.vercel\.app")
    if not patterns:
        return None
    return "|".join(f"({p})" for p in patterns)


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
    from zomato_rec.logging_config import configure_logging

    configure_logging(Settings().log_level)
    ds = default_dataset_path()
    if ds.is_file():
        logger.info("Dataset ready: %s", ds)
    else:
        logger.warning(
            "Processed dataset missing at %s — /api/recommendations will return 503 until ingest completes",
            ds,
        )
    if is_render():
        logger.info("Running on Render; service URL=%s", render_service_url() or "(pending)")
    yield


app = FastAPI(
    title="Zomato Recommendation API",
    description="Phase 7 — REST layer over Phases 2–4 (see Docs/phase_wise_architecture.md).",
    version=_package_version(),
    lifespan=_lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_origin_regex=_cors_origin_regex(),
    # No cookies / auth on this API yet; false avoids extra CORS friction in browsers.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "service": "zomato-recommendation-api",
        "health": "/api/health",
        "docs": "/docs",
    }


@app.get("/api/health")
def health() -> dict:
    settings = Settings()
    ds = default_dataset_path()
    cors_origins = _cors_origins()
    payload = {
        "status": "ok",
        "dataset_path": str(ds),
        "dataset_ok": ds.is_file(),
        "groq_configured": bool(settings.groq_api_key),
        "groq_model": settings.groq_model,
        "render": is_render(),
        "cors_origins_count": len(cors_origins),
    }
    if is_render():
        payload["service_url"] = render_service_url()
    if is_render() and not cors_origins:
        payload["status"] = "degraded"
        payload["warning"] = "API_CORS_ORIGINS is empty; set your Vercel URL on Render"
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
def recommendations(body: RecommendationRequest) -> dict:
    try:
        out = run_recommendations(body)
        return out.model_dump()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


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
