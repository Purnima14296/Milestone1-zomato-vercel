from __future__ import annotations

import os


def is_railway() -> bool:
    """True when the process runs on Railway."""
    return bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"))


def apply_production_defaults() -> None:
    """
    Production-safe defaults on Railway (only when the variable is unset).

    Matches DEPLOYMENT.md: lock CORS to API_CORS_ORIGINS in production.
    """
    if not is_railway():
        return
    if not os.getenv("API_CORS_DISABLE_LOCALHOST_REGEX", "").strip():
        os.environ["API_CORS_DISABLE_LOCALHOST_REGEX"] = "1"
    if not os.getenv("API_CORS_ALLOW_VERCEL_REGEX", "").strip():
        os.environ["API_CORS_ALLOW_VERCEL_REGEX"] = "1"


def public_service_url() -> str | None:
    """Public HTTPS URL for this Railway service (if configured)."""
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
    if domain:
        return f"https://{domain}"
    return None
