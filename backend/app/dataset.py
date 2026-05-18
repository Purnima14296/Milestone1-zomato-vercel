from __future__ import annotations

import logging
import os
from pathlib import Path

from backend.app.paths import repo_root
from backend.app.railway_env import auto_ingest_if_missing, is_railway

logger = logging.getLogger(__name__)

RAILWAY_VOLUME_DATASET = Path("/data/processed/restaurants.parquet")
LOCAL_DEFAULT_DATASET = repo_root() / "data" / "processed" / "restaurants.parquet"


def resolve_dataset_path() -> Path:
    """
    Resolved Parquet path for the API.

    Priority:
    1. `ZOMATO_PROCESSED_DATASET` env (Railway volume, custom mount)
    2. `/data/processed/restaurants.parquet` on Railway if the file exists
    3. `data/processed/restaurants.parquet` under repo root if it exists
    4. Railway volume path when on Railway, else repo-local default (for clear errors)
    """
    override = os.environ.get("ZOMATO_PROCESSED_DATASET", "").strip()
    if override:
        return Path(override)

    candidates: list[Path] = []
    if is_railway():
        candidates.append(RAILWAY_VOLUME_DATASET)
    candidates.append(LOCAL_DEFAULT_DATASET)

    for path in candidates:
        if path.is_file():
            return path

    return candidates[0] if is_railway() else LOCAL_DEFAULT_DATASET


def ensure_dataset(*, settings: object | None = None) -> Path:
    """
    Ensure processed Parquet exists. When `ZOMATO_AUTO_INGEST_IF_MISSING=1`, run Phase 1 ingest.
    """
    path = resolve_dataset_path()
    if path.is_file():
        logger.info("Dataset ready at %s", path)
        return path

    if not auto_ingest_if_missing():
        logger.warning("Dataset missing at %s (set ZOMATO_AUTO_INGEST_IF_MISSING=1 to ingest on startup)", path)
        return path

    from zomato_rec.config import Settings
    from zomato_rec.logging_config import configure_logging
    from zomato_rec.phase1.ingest import run as run_ingest

    cfg = settings if isinstance(settings, Settings) else Settings()
    configure_logging(cfg.log_level)

    path.parent.mkdir(parents=True, exist_ok=True)
    report_path = path.parent / "ingest_report.json"
    logger.info("Dataset missing; running Phase 1 ingest → %s", path)
    run_ingest(
        dataset_id=cfg.hf_dataset_id,
        split=cfg.hf_dataset_split,
        out_path=str(path),
        out_format="parquet",
        report_path=str(report_path),
    )
    logger.info("Ingest complete (%s)", path)
    return path
