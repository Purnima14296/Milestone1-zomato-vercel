from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import asdict, dataclass

from datasets import load_dataset

from zomato_rec.config import Settings
from zomato_rec.logging_config import configure_logging
from zomato_rec.phase1.preprocess import build_processed_df


logger = logging.getLogger("zomato_rec.phase1")


@dataclass(frozen=True)
class IngestReport:
    dataset_id: str
    split: str
    raw_rows: int
    processed_rows: int
    inferred_mapping: dict[str, str | None]
    output_path: str
    output_format: str


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Phase 1: ingest + preprocess Zomato dataset")
    p.add_argument("--dataset-id", default=None, help="Hugging Face dataset id (overrides HF_DATASET_ID).")
    p.add_argument("--split", default=None, help="Dataset split (overrides HF_DATASET_SPLIT).")
    p.add_argument(
        "--out",
        default=os.path.join("data", "processed", "restaurants.parquet"),
        help="Output path for processed dataset.",
    )
    p.add_argument(
        "--format",
        choices=["parquet", "csv"],
        default="parquet",
        help="Output format.",
    )
    p.add_argument(
        "--report",
        default=os.path.join("data", "processed", "ingest_report.json"),
        help="Write a JSON report with schema mapping + counts.",
    )
    return p


def run(dataset_id: str, split: str, out_path: str, out_format: str, report_path: str) -> IngestReport:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    logger.info("Loading dataset from Hugging Face: %s (split=%s)", dataset_id, split)
    ds = load_dataset(dataset_id, split=split)
    raw_df = ds.to_pandas()
    logger.info("Loaded raw rows=%d cols=%d", len(raw_df), len(raw_df.columns))

    processed_df, mapping = build_processed_df(raw_df)
    logger.info("Processed rows=%d (dropped=%d)", len(processed_df), len(raw_df) - len(processed_df))
    logger.info("Inferred column mapping: %s", mapping)

    if out_format == "parquet":
        processed_df.to_parquet(out_path, index=False)
    else:
        processed_df.to_csv(out_path, index=False, encoding="utf-8")

    rep = IngestReport(
        dataset_id=dataset_id,
        split=split,
        raw_rows=len(raw_df),
        processed_rows=len(processed_df),
        inferred_mapping=mapping,
        output_path=out_path,
        output_format=out_format,
    )

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(asdict(rep), f, indent=2, ensure_ascii=False)
    logger.info("Wrote report to %s", report_path)

    logger.info("Wrote processed dataset to %s", out_path)
    return rep


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings()
    configure_logging(settings.log_level)

    dataset_id = args.dataset_id or settings.hf_dataset_id
    split = args.split or settings.hf_dataset_split

    run(
        dataset_id=dataset_id,
        split=split,
        out_path=args.out,
        out_format=args.format,
        report_path=args.report,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

