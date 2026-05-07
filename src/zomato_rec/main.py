from __future__ import annotations

import argparse
import logging
import os
import sys

from zomato_rec.config import Settings
from zomato_rec.logging_config import configure_logging


logger = logging.getLogger("zomato_rec")


def _ensure_phase0_folders() -> None:
    os.makedirs("Docs", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("storage", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


def run_check() -> int:
    _ensure_phase0_folders()
    settings = Settings()
    configure_logging(settings.log_level)

    logger.info("Phase 0 check: OK")
    logger.info("Dataset configured as id=%s split=%s", settings.hf_dataset_id, settings.hf_dataset_split)

    # LLM settings are optional in Phase 0; warn if partially configured.
    if (settings.llm_provider and not settings.llm_api_key) or (settings.llm_api_key and not settings.llm_provider):
        logger.warning("LLM config is partially set (provider=%s, api_key_set=%s).", settings.llm_provider, bool(settings.llm_api_key))
    else:
        logger.info("LLM config present: %s", "yes" if (settings.llm_provider and settings.llm_api_key) else "no (optional in Phase 0)")

    logger.info("Logs are being written to logs/app.log")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Zomato AI Recommendation System (Phase 0 scaffold)")
    p.add_argument(
        "--check",
        action="store_true",
        help="Run a basic Phase 0 sanity check (config + logging + folders).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.check:
        return run_check()

    print("Nothing to run yet. Try: python -m zomato_rec.main --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

