from __future__ import annotations

import logging
import threading

import pandas as pd

from backend.app.dataset import resolve_dataset_path

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_cached_df: pd.DataFrame | None = None
_cached_path: str | None = None


def get_processed_dataframe() -> pd.DataFrame:
    """Load processed restaurants once per process (reduces RAM spikes on each POST)."""
    global _cached_df, _cached_path

    path = str(resolve_dataset_path())
    with _lock:
        if _cached_df is not None and _cached_path == path:
            return _cached_df

    from zomato_rec.phase3.retrieve import load_processed_dataset

    logger.info("Loading processed dataset into memory from %s", path)
    df = load_processed_dataset(path)
    with _lock:
        _cached_df = df
        _cached_path = path
    logger.info("Dataset cache ready (%d rows)", len(df))
    return df


def warm_dataset_cache() -> bool:
    """Preload parquet at startup when the file exists. Returns True if cached."""
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
