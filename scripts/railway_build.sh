#!/usr/bin/env bash
# Railway build — repo root. See DEPLOYMENT.md §1.3 Option C
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Installing Python dependencies"
bash "$(dirname "$0")/railway_install.sh"

OUT="${ZOMATO_PROCESSED_DATASET:-data/processed/restaurants.parquet}"
REPORT_DIR="$(dirname "$OUT")"

if [[ -f "$OUT" ]]; then
  echo "==> Dataset already present at ${OUT} — skipping Phase 1 ingest"
  exit 0
fi

if [[ "${RAILWAY_SKIP_DATASET_INGEST:-}" =~ ^(1|true|yes)$ ]]; then
  echo "==> RAILWAY_SKIP_DATASET_INGEST set and dataset missing at ${OUT}"
  echo "    Use a volume at /data or run: python -m zomato_rec.phase1.ingest --out ${OUT}"
  exit 0
fi

echo "==> Building processed dataset (Phase 1) -> ${OUT}"
mkdir -p "${REPORT_DIR}"
python -m zomato_rec.phase1.ingest --out "${OUT}" --report "${REPORT_DIR}/ingest_report.json"
