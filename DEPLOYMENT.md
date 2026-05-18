# Deployment plan — Render (backend) + Vercel (frontend)

This project ships as two services:

| Service | Platform | Code | Public URL (example) |
|---------|----------|------|----------------------|
| **API** (FastAPI / Phase 7) | [Render](https://render.com) | Repo root → `backend/` | `https://zomato-api.onrender.com` |
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
Render Web Service (uvicorn → FastAPI)
    │
    ├── restaurants.parquet  (Phase 1 dataset on disk or env path)
    └── Groq API             (GROQ_API_KEY, server-side only)
```

**Secrets rule:** `GROQ_API_KEY` lives only on Render. Vercel exposes no LLM keys—only `NEXT_PUBLIC_API_URL`.

---

## Prerequisites

1. **GitHub** — code on `master` (or your deploy branch).
2. **Groq** — API key from [console.groq.com](https://console.groq.com).
3. **Processed dataset** — `data/processed/restaurants.parquet` from Phase 1:
   ```bash
   python -m zomato_rec.phase1.ingest
   ```
   `data/` is gitignored, so production must **build, mount, or download** this file (see below).

---

## Part 1 — Backend on Render

### 1.1 Create the Web Service

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Web Service**.
2. Connect **Milestone1-zomato-vercel** (GitHub).
3. Suggested settings:

| Setting | Value |
|---------|--------|
| **Name** | `zomato-api` (your choice) |
| **Region** | Closest to users |
| **Branch** | `master` |
| **Root directory** | *(leave empty — repo root)* |
| **Runtime** | Python 3 |
| **Build command** | `bash scripts/render_build.sh` (or see [Dataset strategies](#13-dataset-on-render-required)) |
| **Start command** | `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` |

Alternatively, import **`render.yaml`** (Option A) or **`render.disk.yaml`** (Option B disk) from the repo root (Blueprint).

### 1.2 Environment variables (Render)

Set in **Environment** (never commit real values):

| Key | Required | Example / notes |
|-----|----------|-----------------|
| `GROQ_API_KEY` | Yes | Groq secret |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` (default in Settings) |
| `API_CORS_ORIGINS` | Yes | `https://your-app.vercel.app` (exact origin, no trailing slash) |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Yes (prod) | `1` |
| `HF_DATASET_ID` | No | Default in config if you ingest on build |
| `HF_DATASET_SPLIT` | No | `train` |
| `ZOMATO_PROCESSED_DATASET` | If using disk | e.g. `/var/data/restaurants.parquet` |
| `LOG_LEVEL` | No | `INFO` |

After the Vercel app exists, add its **production URL** to `API_CORS_ORIGINS`. For preview deploys, add each preview origin or use a single production URL first.

### 1.3 Dataset on Render (required)

The API returns **503** if `restaurants.parquet` is missing. Pick one approach:

**Option A — Build-time ingest (simplest for demos)**

Build command (repo includes `scripts/render_build.sh`):

```bash
bash scripts/render_build.sh
```

- Pros: no extra Render products.
- Cons: **re-downloads on every deploy** (~1–4 min build); ephemeral disk—file is lost if the instance is replaced unless you re-run build.

**Option B — Persistent disk (recommended for production)**

1. Add a **Disk** (e.g. 1 GB) mounted at `/var/data`.
2. One-time: open Render **Shell** or a one-off job and run:
   ```bash
   pip install -r requirements.txt
   python -m zomato_rec.phase1.ingest
   mv data/processed/restaurants.parquet /var/data/restaurants.parquet
   ```
3. Set `ZOMATO_PROCESSED_DATASET=/var/data/restaurants.parquet`.
4. Build command: `pip install -r requirements.txt` only.

**Option C — Hosted Parquet**

Upload `restaurants.parquet` to object storage, download in build/startup, set `ZOMATO_PROCESSED_DATASET` to the local path after download.

### 1.4 Verify the API

- Health: `GET https://<your-service>.onrender.com/api/health`
  - Expect `"dataset_ok": true`, `"groq_configured": true`.
- Docs: `https://<your-service>.onrender.com/docs`

Render free tier **spins down** after idle; first request may take 30–60s (cold start).

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
| **Output** | Next.js default |

### 2.2 Environment variables (Vercel)

| Key | Environments | Value |
|-----|----------------|-------|
| `NEXT_PUBLIC_API_URL` | Production (and Preview if needed) | `https://<your-render-service>.onrender.com` |

No trailing slash. Redeploy after changing this variable.

### 2.3 Verify the UI

1. Open the Vercel URL.
2. Confirm location dropdown loads (`GET /api/locations`).
3. Submit preferences and confirm recommendations (`POST /api/recommendations`).

If the browser shows CORS errors, fix `API_CORS_ORIGINS` on Render to match the **exact** Vercel origin (scheme + host, no path).

---

## Part 3 — Deploy order checklist

Use this order on first setup:

- [ ] Push repo to GitHub (includes removal of Streamlit-only paths).
- [ ] Create **Render** Web Service; set `GROQ_API_KEY` and dataset strategy.
- [ ] Deploy API; confirm `/api/health` → `dataset_ok: true`.
- [ ] Create **Vercel** project with root `frontend/`.
- [ ] Set `NEXT_PUBLIC_API_URL` to the Render URL; deploy.
- [ ] Set Render `API_CORS_ORIGINS` to the Vercel production URL (+ preview URLs if needed).
- [ ] Set `API_CORS_DISABLE_LOCALHOST_REGEX=1` on Render.
- [ ] Redeploy Render if you changed CORS after Vercel existed.
- [ ] End-to-end test: preferences → recommendations on production.

---

## Part 4 — Local parity

| Local | Production |
|-------|------------|
| `uvicorn backend.app.main:app --reload --port 8000` | Render start command with `$PORT` |
| `frontend/.env.local` → `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` | Vercel env → Render HTTPS URL |
| `.env` at repo root with `GROQ_API_KEY` | Render environment variables |

---

## Part 5 — Optional hardening

- **Custom domains** — Render + Vercel each support custom domains; update `API_CORS_ORIGINS` and `NEXT_PUBLIC_API_URL` accordingly.
- **Health checks** — Render health check path: `/api/health`.
- **Rate limits** — In-process limiter in `backend/app/main.py` (per instance); upgrade plan or add edge proxy if you need global limits.
- **Monitoring** — Use Render logs + Vercel Analytics; Groq usage in Groq dashboard.

---

## Files reference

| File | Purpose |
|------|---------|
| `requirements.txt` | Render `pip install -r requirements.txt` |
| `scripts/render_build.sh` | Install deps + conditional Phase 1 ingest |
| `runtime.txt` | Python 3.12.7 for Render |
| `render.yaml` | Blueprint Option A (build-time ingest) |
| `render.disk.yaml` | Blueprint Option B (persistent disk) |
| `backend/app/env.py` | Render detection + production CORS defaults |
| `backend/app/main.py` | FastAPI app + CORS + `/api/health` |
| `frontend/src/lib/api.ts` | Uses `NEXT_PUBLIC_API_URL` |
| `.env.example` | Local / documented env keys |
