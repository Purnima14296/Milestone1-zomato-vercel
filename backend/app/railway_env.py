from __future__ import annotations

import os

# Production + preview Vercel URLs (e.g. https://my-app.vercel.app).
VERCEL_ORIGIN_REGEX = r"https://([a-z0-9-]+\.)*vercel\.app"


def is_railway() -> bool:
    """True when running on Railway (any environment)."""
    return bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"))


def is_railway_production() -> bool:
    env = os.getenv("RAILWAY_ENVIRONMENT", "").strip().lower()
    return env in {"production", "staging", "preview"}


def railway_public_url() -> str | None:
    """Public HTTPS URL for this Railway service, if assigned."""
    for key in ("RAILWAY_PUBLIC_DOMAIN", "RAILWAY_STATIC_URL"):
        domain = os.getenv(key, "").strip()
        if not domain:
            continue
        if domain.startswith("http://") or domain.startswith("https://"):
            return domain.rstrip("/")
        return f"https://{domain}"
    return None


def apply_railway_defaults() -> None:
    """Production-safe defaults on Railway when variables are unset."""
    if not is_railway():
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
            "Set API_CORS_ORIGINS to your Vercel URL on Railway, or keep API_CORS_ALLOW_VERCEL=1 (default)."
        )


def auto_ingest_if_missing() -> bool:
    return os.getenv("ZOMATO_AUTO_INGEST_IF_MISSING", "").strip().lower() in {"1", "true", "yes"}


def cors_localhost_disabled() -> bool:
    return os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip().lower() in {"1", "true", "yes"}


def cors_allow_vercel() -> bool:
    return os.getenv("API_CORS_ALLOW_VERCEL", "1").strip().lower() not in {"0", "false", "no"}


def cors_origin_regex() -> str | None:
    """Combined origin regex (localhost dev + Vercel on Railway)."""
    parts: list[str] = []
    if not cors_localhost_disabled():
        parts.append(r"https?://(localhost|127\.0\.0\.1)(:\d+)?")
    if is_railway() and cors_allow_vercel():
        custom = os.getenv("API_CORS_ORIGIN_REGEX", "").strip()
        parts.append(custom if custom else VERCEL_ORIGIN_REGEX)
    if not parts:
        return None
    return "|".join(f"({p})" for p in parts)


def cors_has_production_access(origins: list[str]) -> bool:
    for o in origins:
        if o.startswith("https://") and "localhost" not in o and "127.0.0.1" not in o:
            return True
    return is_railway() and cors_allow_vercel() and bool(cors_origin_regex())
