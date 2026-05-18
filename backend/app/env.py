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
    has_https_origin = any(
        o.startswith("https://") and "localhost" not in o and "127.0.0.1" not in o
        for o in cors.split(",")
        if o.strip()
    )
    if not has_https_origin and not cors_allow_vercel():
        import logging

        logging.getLogger(__name__).warning(
            "Set API_CORS_ORIGINS to your Vercel URL on Render, or keep API_CORS_ALLOW_VERCEL=1 (default)."
        )


def render_service_url() -> str | None:
    """Public HTTPS URL assigned by Render (if available)."""
    url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    return url or None


def auto_ingest_if_missing() -> bool:
    return os.getenv("ZOMATO_AUTO_INGEST_IF_MISSING", "").strip().lower() in {"1", "true", "yes"}


# Matches production + preview Vercel URLs (e.g. https://my-app.vercel.app).
VERCEL_ORIGIN_REGEX = r"https://([a-z0-9-]+\.)*vercel\.app"


def cors_localhost_disabled() -> bool:
    return os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip().lower() in {"1", "true", "yes"}


def cors_allow_vercel() -> bool:
    return os.getenv("API_CORS_ALLOW_VERCEL", "1").strip().lower() not in {"0", "false", "no"}


def cors_origin_regex() -> str | None:
    """Combined origin regex for CORSMiddleware (localhost dev + Vercel on Render)."""
    parts: list[str] = []
    if not cors_localhost_disabled():
        parts.append(r"https?://(localhost|127\.0\.0\.1)(:\d+)?")
    if is_render() and cors_allow_vercel():
        custom = os.getenv("API_CORS_ORIGIN_REGEX", "").strip()
        parts.append(custom if custom else VERCEL_ORIGIN_REGEX)
    if not parts:
        return None
    return "|".join(f"({p})" for p in parts)


def cors_has_production_access(origins: list[str]) -> bool:
    """True if explicit https origins or Vercel regex covers production traffic."""
    for o in origins:
        if o.startswith("https://") and "localhost" not in o and "127.0.0.1" not in o:
            return True
    return is_render() and cors_allow_vercel() and bool(cors_origin_regex())
