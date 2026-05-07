from __future__ import annotations

import argparse
import logging
import os

from zomato_rec.config import Settings
from zomato_rec.logging_config import configure_logging
from zomato_rec.phase3.retrieve import run_phase3, save_report


logger = logging.getLogger("zomato_rec.phase3")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 3: deterministic candidate retrieval + shortlist")
    p.add_argument(
        "--dataset",
        default=os.path.join("data", "processed", "restaurants.parquet"),
        help="Path to processed dataset (parquet/csv).",
    )
    p.add_argument(
        "--prefs",
        default=os.path.join("storage", "preferences.json"),
        help="Path to saved user preferences JSON.",
    )
    p.add_argument(
        "--out",
        default=os.path.join("storage", "shortlist.json"),
        help="Output shortlist JSON path.",
    )
    p.add_argument(
        "--top-n",
        type=int,
        default=30,
        help="Number of shortlisted restaurants to output.",
    )
    p.add_argument(
        "--report",
        default=os.path.join("storage", "shortlist_report.json"),
        help="Write a JSON report for Phase 3 run.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings()
    configure_logging(settings.log_level)

    report = run_phase3(
        processed_dataset_path=args.dataset,
        preferences_path=args.prefs,
        out_path=args.out,
        top_n=args.top_n,
    )
    save_report(report, args.report)
    logger.info(
        "Phase 3 complete: candidates_after_filtering=%d shortlist=%d out=%s",
        report.candidates_after_filtering,
        report.shortlist_size,
        report.output_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

