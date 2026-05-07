from __future__ import annotations

import argparse
import logging
import os

from zomato_rec.config import Settings
from zomato_rec.logging_config import configure_logging
from zomato_rec.phase2.io import save_preferences
from zomato_rec.phase2.models import UserPreferences
from zomato_rec.phase2.normalize import (
    normalize_location,
    parse_budget,
    parse_cuisines,
    parse_min_rating,
)


logger = logging.getLogger("zomato_rec.phase2")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 2: collect + validate user preferences")
    p.add_argument("--location", default=None, help="City/locality (e.g., Bangalore).")
    p.add_argument("--budget", default=None, help="Budget: low/medium/high or numeric/range (e.g., 500-800).")
    p.add_argument("--cuisines", default=None, help="Comma-separated cuisines (e.g., Italian, Chinese).")
    p.add_argument("--min-rating", default=None, help="Minimum rating (0-5), e.g., 4.0 or 4+.")
    p.add_argument("--extra", default=None, help="Additional preferences (free text).")
    p.add_argument(
        "--out",
        default=os.path.join("storage", "preferences.json"),
        help="Output path for validated preferences JSON.",
    )
    p.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for missing fields interactively.",
    )
    return p


def _prompt(label: str) -> str:
    return input(label).strip()


def run(
    *,
    location: str,
    budget: str | None,
    cuisines: str | None,
    min_rating: str | None,
    extra: str | None,
    out_path: str,
) -> UserPreferences:
    prefs = UserPreferences(
        location=normalize_location(location),
        budget=parse_budget(budget),
        cuisines=parse_cuisines(cuisines),
        minimum_rating=parse_min_rating(min_rating),
        additional_preferences=(extra.strip() if extra and extra.strip() else None),
    )

    save_preferences(prefs, out_path)
    logger.info("Saved preferences to %s", out_path)
    return prefs


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings()
    configure_logging(settings.log_level)

    location = args.location
    budget = args.budget
    cuisines = args.cuisines
    min_rating = args.min_rating
    extra = args.extra

    if args.interactive:
        if not location:
            location = _prompt("Location (e.g., Bangalore): ")
        if budget is None:
            budget = _prompt("Budget (low/medium/high or 500-800, leave blank for any): ")
        if cuisines is None:
            cuisines = _prompt("Cuisine(s) (comma-separated, leave blank for any): ")
        if min_rating is None:
            min_rating = _prompt("Minimum rating (0-5, leave blank for any): ")
        if extra is None:
            extra = _prompt("Additional preferences (optional): ")

    if not location or not location.strip():
        raise SystemExit("Error: --location is required (or use --interactive).")

    run(
        location=location,
        budget=budget,
        cuisines=cuisines,
        min_rating=min_rating,
        extra=extra,
        out_path=args.out,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

