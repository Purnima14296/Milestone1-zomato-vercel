# Deployment plan — Railway (backend) + Vercel (frontend)

This project ships as two services:

| Service | Platform | Code | Public URL (example) |
|---------|----------|------|----------------------|
| **API** (FastAPI / Phase 7) | [Railway](https://railway.com) | Repo root → `backend/` | `https://zomato-api-production.up.railway.app` |
| **Web** (Next.js / Phase 8) | [Vercel](https://vercel.com) | `frontend/` | `https://your-app.vercel.app` |

GitHub repo: [Milestone1-zomato-vercel](https://github.com/Purnima14296/Milestone1-zomato-vercel).

---

## Architecture

```text
User browser
    │
    ▼ HTTPS
Vercel (Next.js, NEXT_PUBLIC_API_URL)
    │
    ▼ HTTPS  /api/*
Railway Service (uvicorn → FastAPI)
    │
    ├── restaurants.parquet  (Phase 1 dataset on disk or volume)
    └── Groq API             (GROQ_API_KEY, server-side only)
```

**Secrets rule:** `GROQ_API_KEY` lives only on Railway. Vercel exposes no LLM keys—only `NEXT_PUBLIC_API_URL`.

---

## Prerequisites

1. **GitHub** — code on `master` (or your deploy branch).
2. **Groq** — API key from [console.groq.com](https://console.groq.com).
3. **Railway account** — [railway.com](https://railway.com).
4. **Processed dataset** — `data/processed/restaurants.parquet` from Phase 1:
   ```bash
   python -m zomato_rec.phase1.ingest
   ```
   `data/` is gitignored, so production must **build, mount a volume, or download** this file (see below).

---

## Part 1 — Backend on Railway

### 1.1 Create the service

1. [Railway Dashboard](https://railway.com/dashboard) → **New Project** → **Deploy from GitHub repo**.
2. Select **Milestone1-zomato-vercel**.
3. Railway reads **`railway.toml`** at the repo root (build + start commands).

| Setting | Value |
|---------|--------|
| **Root directory** | Repository root (default) |
| **Builder** | Nixpacks (auto from `runtime.txt` + `requirements.txt`) |
| **Build command** | `bash scripts/railway_build.sh` (from `railway.toml`) |
| **Start command** | `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` |

4. **Settings** → **Networking** → **Generate domain** to get a public HTTPS URL.

### 1.2 Environment variables (Railway)

In the service → **Variables** (never commit real values):

| Key | Required | Example / notes |
|-----|----------|-----------------|
| `GROQ_API_KEY` | Yes | Groq secret |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` |
| `API_CORS_ORIGINS` | Recommended | `https://your-app.vercel.app` (exact origin, no trailing slash) |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Auto on Railway | Set `1` if not using defaults |
| `API_CORS_ALLOW_VERCEL_REGEX` | Auto on Railway | `1` allows `*.vercel.app` previews |
| `HF_DATASET_ID` | No | Default in config |
| `HF_DATASET_SPLIT` | No | `train` |
| `ZOMATO_PROCESSED_DATASET` | If using volume | e.g. `/data/restaurants.parquet` |
| `RAILWAY_SKIP_DATASET_INGEST` | Volume-only builds | `1` to skip ingest when Parquet is on a volume |
| `LOG_LEVEL` | No | `INFO` |

Railway sets `PORT`, `RAILWAY_ENVIRONMENT`, and `RAILWAY_PUBLIC_DOMAIN` automatically.

### 1.3 Dataset on Railway (required)

The API returns **503** if `restaurants.parquet` is missing.

**Option A — Build-time ingest (simplest for demos)**

Default `railway.toml` runs `scripts/railway_build.sh`, which installs deps and runs Phase 1 ingest if the file is absent.

- Pros: no extra setup.
- Cons: re-downloads from Hugging Face on each deploy (~1–4 min); ephemeral filesystem unless you use a volume.

**Option B — Railway volume (recommended for production)**

1. In the service → **Volumes** → **Add volume** (e.g. mount at `/data`).
2. One-time via **Railway shell** (`railway shell` CLI or dashboard):
   ```bash
   pip install -r requirements.txt
   python -m zomato_rec.phase1.ingest --out /data/restaurants.parquet
   ```
3. Set variables:
   - `ZOMATO_PROCESSED_DATASET=/data/restaurants.parquet`
   - `RAILWAY_SKIP_DATASET_INGEST=1`
4. Redeploy (build only runs `pip install` if you adjust the build script, or keep ingest skip logic).

**Option C — Hosted Parquet**

Upload to object storage, download in build/startup, set `ZOMATO_PROCESSED_DATASET` to the local path.

### 1.4 Verify the API

- Health: `GET https://<your-domain>.up.railway.app/api/health`
  - Expect `"dataset_ok": true`, `"groq_configured": true`, `"railway": true`.
- Docs: `https://<your-domain>.up.railway.app/docs`

---

## Part 2 — Frontend on Vercel

### 2.1 Import the project

1. [Vercel Dashboard](https://vercel.com/dashboard) → **Add New** → **Project**.
2. Import the same GitHub repo.
3. Configure:

| Setting | Value |
|---------|--------|
| **Framework preset** | Next.js |
| **Root directory** | `frontend` |
| **Build command** | `npm run build` (default) |

### 2.2 Environment variables (Vercel)

| Key | Environments | Value |
|-----|----------------|-------|
| `NEXT_PUBLIC_API_URL` | Production (+ Preview) | `https://<your-railway-domain>.up.railway.app` |

No trailing slash. Redeploy after changing.

### 2.3 Verify the UI

1. Open the Vercel URL.
2. Location dropdown loads (`GET /api/locations`).
3. Submit preferences → recommendations (`POST /api/recommendations`).

If CORS errors appear, set `API_CORS_ORIGINS` on Railway to your exact Vercel origin, or rely on `API_CORS_ALLOW_VERCEL_REGEX=1` (default on Railway).

---

## Part 3 — Deploy order checklist

- [ ] Push repo to GitHub.
- [ ] Create **Railway** project from repo; set `GROQ_API_KEY`.
- [ ] Generate Railway **public domain**; confirm `/api/health`.
- [ ] Create **Vercel** project (`frontend/` root).
- [ ] Set `NEXT_PUBLIC_API_URL` to Railway HTTPS URL; deploy.
- [ ] Set Railway `API_CORS_ORIGINS` to Vercel URL (optional if Vercel regex is enough).
- [ ] End-to-end test on production.

---

## Part 4 — Local parity

| Local | Production |
|-------|------------|
| `uvicorn backend.app.main:app --reload --port 8000` | Railway start command with `$PORT` |
| `frontend/.env.local` → `http://127.0.0.1:8000` | Vercel → Railway HTTPS URL |
| `.env` at repo root | Railway service variables |

---

## Part 5 — Optional hardening

- **Custom domains** — Railway and Vercel both support custom domains; update `API_CORS_ORIGINS` and `NEXT_PUBLIC_API_URL`.
- **Health checks** — `/api/health` (configured in `railway.toml`).
- **CLI** — [Railway CLI](https://docs.railway.com/develop/cli) for logs: `railway logs`.
- **Monitoring** — Railway metrics + Vercel Analytics; Groq usage in Groq dashboard.

---

## Files reference

| File | Purpose |
|------|---------|
| `railway.toml` | Railway build/start + health check |
| `requirements.txt` | `pip install -e ".[api]"` |
| `scripts/railway_build.sh` | Install deps + conditional Phase 1 ingest |
| `runtime.txt` | Python 3.12.7 for Nixpacks |
| `backend/app/env.py` | Railway detection + production CORS defaults |
| `backend/app/main.py` | FastAPI + CORS + `/api/health` |
| `frontend/vercel.json` | Vercel Next.js build |
| `frontend/.env.example` | `NEXT_PUBLIC_API_URL` for Vercel |
