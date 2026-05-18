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


def render_service_url() -> str | None:
    """Public HTTPS URL assigned by Render (if available)."""
    url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    return url or None
