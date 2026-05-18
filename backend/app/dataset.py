from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Literal

from backend.app.paths import repo_root
from backend.app.railway_env import auto_ingest_if_missing, is_railway

logger = logging.getLogger(__name__)

RAILWAY_VOLUME_DATASET = Path("/data/processed/restaurants.parquet")
BUILD_DEFAULT_DATASET = repo_root() / "data" / "processed" / "restaurants.parquet"

IngestState = Literal["idle", "running", "ready", "failed"]

_ingest_lock = threading.Lock()
_ingest_state: IngestState = "idle"
_ingest_error: str | None = None


def ingest_state() -> IngestState:
    with _ingest_lock:
        return _ingest_state


def ingest_error() -> str | None:
    with _ingest_lock:
        return _ingest_error


def is_ingest_running() -> bool:
    return ingest_state() == "running"


def resolve_dataset_path() -> Path:
    """
    Resolved Parquet path for the API.

    Priority:
    1. `ZOMATO_PROCESSED_DATASET` env (Railway volume, custom mount)
    2. `/data/processed/restaurants.parquet` on Railway if the file exists
    3. `data/processed/restaurants.parquet` under repo root if it exists
    """
    override = os.environ.get("ZOMATO_PROCESSED_DATASET", "").strip()
    if not override:
        try:
            from zomato_rec.config import Settings

            override = (Settings().zomato_processed_dataset or "").strip()
        except Exception:
            override = ""
    if override:
        return Path(override)

    candidates: list[Path] = []
    if is_railway():
        candidates.extend([RAILWAY_VOLUME_DATASET, BUILD_DEFAULT_DATASET])
    else:
        candidates.append(BUILD_DEFAULT_DATASET)

    for path in candidates:
        if path.is_file():
            return path

    return BUILD_DEFAULT_DATASET


def _set_ingest_state(state: IngestState, *, error: str | None = None) -> None:
    global _ingest_state, _ingest_error
    with _ingest_lock:
        _ingest_state = state
        _ingest_error = error


def _try_start_ingest() -> bool:
    """Mark ingest as running if not already. Returns False if already running."""
    global _ingest_state, _ingest_error
    with _ingest_lock:
        if _ingest_state == "running":
            return False
        _ingest_state = "running"
        _ingest_error = None
        return True


def _run_ingest(*, settings: object | None = None) -> Path:
    """Blocking ingest (Phase 1). Used from background thread or sync callers."""
    from zomato_rec.config import Settings
    from zomato_rec.logging_config import configure_logging
    from zomato_rec.phase1.ingest import run as run_ingest

    cfg = settings if isinstance(settings, Settings) else Settings()
    configure_logging(cfg.log_level)

    path = resolve_dataset_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    report_path = path.parent / "ingest_report.json"
    logger.info("Running Phase 1 ingest → %s", path)
    run_ingest(
        dataset_id=cfg.hf_dataset_id,
        split=cfg.hf_dataset_split,
        out_path=str(path),
        out_format="parquet",
        report_path=str(report_path),
    )
    logger.info("Ingest complete (%s)", path)
    from backend.app.dataset_cache import clear_dataset_cache, warm_dataset_cache

    clear_dataset_cache()
    warm_dataset_cache()
    return path


def ensure_dataset(*, settings: object | None = None) -> Path:
    """Ensure processed Parquet exists. Optional startup ingest via `ZOMATO_AUTO_INGEST_IF_MISSING=1`."""
    path = resolve_dataset_path()
    if path.is_file():
        _set_ingest_state("ready")
        logger.info("Dataset ready at %s", path)
        return path

    if not auto_ingest_if_missing():
        logger.warning("Dataset missing at %s (set ZOMATO_AUTO_INGEST_IF_MISSING=1 to ingest on startup)", path)
        return path

    _set_ingest_state("running")
    try:
        path = _run_ingest(settings=settings)
        _set_ingest_state("ready" if path.is_file() else "failed")
        return path
    except Exception as exc:
        _set_ingest_state("failed", error=str(exc))
        logger.exception("Dataset ingest failed")
        raise


def start_background_ingest(*, settings: object | None = None) -> bool:
    """
    Start Hugging Face ingest in a daemon thread so uvicorn can serve /api/health immediately.
    Returns True if a new ingest thread was started.
    """
    path = resolve_dataset_path()
    if path.is_file():
        _set_ingest_state("ready")
        return False

    if not auto_ingest_if_missing():
        return False

    if not _try_start_ingest():
        return False

    def worker() -> None:
        try:
            result = _run_ingest(settings=settings)
            _set_ingest_state("ready" if result.is_file() else "failed")
        except Exception as exc:
            _set_ingest_state("failed", error=str(exc))
            logger.exception("Background dataset ingest failed")

    thread = threading.Thread(target=worker, name="dataset-ingest", daemon=True)
    thread.start()
    logger.info("Background dataset ingest started → %s", path)
    return True


def prepare_dataset_at_startup(*, settings: object | None = None) -> Path:
    """
    Called from FastAPI lifespan: use existing file, or kick off background ingest.
    Never blocks on Hugging Face download when auto-ingest is enabled.
    """
    path = resolve_dataset_path()
    if path.is_file():
        _set_ingest_state("ready")
        logger.info("Dataset ready at %s", path)
        return path

    if auto_ingest_if_missing():
        start_background_ingest(settings=settings)
        return path

    logger.warning(
        "Dataset missing at %s — recommendations will return 503 until "
        "ZOMATO_PROCESSED_DATASET is set, a Railway volume is mounted at /data, or "
        "ZOMATO_AUTO_INGEST_IF_MISSING=1 is enabled.",
        path,
    )
    return path
