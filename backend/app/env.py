from __future__ import annotations

import os


def is_render() -> bool:
    """True when the process runs on Render (Web Service or Shell)."""
    if os.getenv("RENDER", "").strip().lower() in {"true", "1", "yes"}:
        return True
    return bool(os.getenv("RENDER_SERVICE_ID") or os.getenv("RENDER_EXTERNAL_URL"))


def apply_render_defaults() -> None:
    """
    Production-safe defaults on Render (only when the variable is unset).

    Matches DEPLOYMENT.md: lock CORS to API_CORS_ORIGINS in production.
    """
    if not is_render():
        return
    if not os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip():
        os.environ["API_CORS_DISABLE_LOCALHOST_REGEX"] = "1"

    cors = os.getenv("API_CORS_ORIGINS", "").strip()
    if not cors or "localhost" in cors or "127.0.0.1" in cors:
        import logging

        logging.getLogger(__name__).warning(
            "API_CORS_ORIGINS is missing or still points at localhost — set your Vercel URL on Render "
            "(see DEPLOYMENT.md §1.2)."
        )


def render_service_url() -> str | None:
    """Public HTTPS URL assigned by Render (if available)."""
    url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    return url or None


def auto_ingest_if_missing() -> bool:
    return os.getenv("ZOMATO_AUTO_INGEST_IF_MISSING", "").strip().lower() in {"1", "true", "yes"}
