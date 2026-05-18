# Railway backend — Python 3.12 with pip preinstalled (avoids Nix ensurepip issues).
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
COPY backend ./backend
COPY scripts/railway_start.sh ./scripts/railway_start.sh

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir ".[api]" \
    && chmod +x ./scripts/railway_start.sh

# Bake dataset at image build so Railway runtime does not HF-download (OOM / restart loop).
# Set SKIP_DATASET_BUILD=1 to skip (e.g. use a Railway volume at /data instead).
ARG SKIP_DATASET_BUILD=0
RUN if [ "$SKIP_DATASET_BUILD" = "0" ]; then \
      mkdir -p /app/data/processed \
      && python -m zomato_rec.phase1.ingest \
        --out /app/data/processed/restaurants.parquet \
        --report /app/data/processed/ingest_report.json; \
    fi

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
# Runtime ingest is optional; image already includes data/processed/restaurants.parquet
ENV ZOMATO_AUTO_INGEST_IF_MISSING=0

# Railway routes public traffic to $PORT (dynamic). EXPOSE is documentation only.
EXPOSE 8080

CMD ["/app/scripts/railway_start.sh"]

