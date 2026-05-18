from __future__ import annotations

import logging
import threading

import pandas as pd

from backend.app.dataset import resolve_dataset_path

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_cached_df: pd.DataFrame | None = None
_cached_path: str | None = None
_warm_in_progress = False


def get_processed_dataframe() -> pd.DataFrame:
    """Load processed restaurants once per process (slim columns, no `raw`)."""
    global _cached_df, _cached_path

    path = str(resolve_dataset_path())
    with _lock:
        if _cached_df is not None and _cached_path == path:
            return _cached_df

    from zomato_rec.phase3.retrieve import API_DATASET_COLUMNS, load_processed_dataset

    logger.info("Loading dataset cache from %s (slim columns)", path)
    df = load_processed_dataset(path, columns=list(API_DATASET_COLUMNS))
    with _lock:
        _cached_df = df
        _cached_path = path
    logger.info("Dataset cache ready (%d rows)", len(df))
    return df


def warm_dataset_cache_async() -> None:
    """Background warm after startup — must not run in lifespan (OOM restart loop on small RAM)."""
    global _warm_in_progress

    path = resolve_dataset_path()
    if not path.is_file():
        return

    with _lock:
        if _cached_df is not None or _warm_in_progress:
            return
        _warm_in_progress = True

    def worker() -> None:
        global _warm_in_progress
        try:
            get_processed_dataframe()
        except Exception:
            logger.exception("Background dataset cache warm failed")
        finally:
            with _lock:
                _warm_in_progress = False

    threading.Thread(target=worker, name="dataset-warm", daemon=True).start()


def warm_dataset_cache() -> bool:
    """Synchronous warm (local/dev only). On Railway prefer lazy load or async warm."""
    path = resolve_dataset_path()
    if not path.is_file():
        return False
    try:
        get_processed_dataframe()
        return True
    except Exception:
        logger.exception("Failed to warm dataset cache")
        return False


def clear_dataset_cache() -> None:
    global _cached_df, _cached_path
    with _lock:
        _cached_df = None
        _cached_path = None
