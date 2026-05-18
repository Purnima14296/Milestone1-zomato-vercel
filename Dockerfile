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

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0

# Railway routes public traffic to $PORT (dynamic). EXPOSE is documentation only.
EXPOSE 8080

CMD ["/app/scripts/railway_start.sh"]

