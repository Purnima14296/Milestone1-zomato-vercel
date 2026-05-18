from __future__ import annotations

import os


def is_railway() -> bool:
    """True when running on Railway (any environment)."""
    return bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"))


def is_railway_production() -> bool:
    env = os.getenv("RAILWAY_ENVIRONMENT", "").strip().lower()
    return env in {"production", "staging", "preview"}


def cors_disable_localhost_regex() -> bool:
    flag = os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip().lower()
    if flag in {"1", "true", "yes"}:
        return True
    if flag in {"0", "false", "no"}:
        return False
    # Railway deploys should not rely on localhost regex unless explicitly opted in.
    return is_railway_production()


def auto_ingest_if_missing() -> bool:
    return os.getenv("ZOMATO_AUTO_INGEST_IF_MISSING", "").strip().lower() in {"1", "true", "yes"}
