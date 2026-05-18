# Deployment — Railway (backend) + Vercel (frontend)

Two separate deployments from this monorepo:

| Component | Platform | Directory | Public URL |
|-----------|----------|-----------|------------|
| FastAPI API | [Railway](https://railway.app) | repo root | `https://<service>.up.railway.app` |
| Next.js UI | [Vercel](https://vercel.com) | `frontend/` | `https://<project>.vercel.app` |

Prerequisites: GitHub repo pushed (e.g. `Milestone1-zomato-vercel`), Groq API key, and a **processed dataset** (`restaurants.parquet` from Phase 1).

---

## Architecture

```text
User browser
    → Vercel (Next.js, NEXT_PUBLIC_API_URL)
        → Railway (FastAPI /api/*)
            → Parquet dataset + Groq LLM
```

Secrets stay on Railway only. Vercel exposes only `NEXT_PUBLIC_API_URL` (no Groq key in the browser).

---

## Part 1 — Backend on Railway

### 1. Create the service

1. [Railway](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
2. Select this repository.
3. **Root directory**: repository root (not `frontend/`).
4. Railway reads `railway.toml` and `requirements.txt` automatically.

### 2. Build & start (already in repo)

- **Install**: `pip install -r requirements.txt` (installs `-e .[api]` from `pyproject.toml`).
- **Start**: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- **Health check**: `GET /api/health`

Override in the Railway dashboard only if you need a custom command.

### 3. Environment variables (Railway → Variables)

| Variable | Required | Example / notes |
|----------|----------|-----------------|
| `GROQ_API_KEY` | Yes | From [Groq console](https://console.groq.com) |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` (default) |
| `API_CORS_ORIGINS` | Yes (prod) | `https://your-app.vercel.app` — add preview URLs if needed |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Recommended prod | `1` — only allow listed origins |
| `ZOMATO_PROCESSED_DATASET` | If not default path | `/data/processed/restaurants.parquet` when using a volume |
| `ZOMATO_AUTO_INGEST_IF_MISSING` | Optional | `1` — run Phase 1 ingest on startup if Parquet is missing (~1–4 min first boot) |
| `HF_DATASET_ID` | No | Only if rebuilding dataset on deploy |
| `LOG_LEVEL` | No | `INFO` |

On Railway **production/staging**, localhost CORS regex is disabled automatically unless you set `API_CORS_DISABLE_LOCALHOST_REGEX=0`.

Do **not** commit `.env` to git.

### 4. Processed dataset (choose one)

`data/` is gitignored, so Railway will not have Parquet unless you provide it.

**Option A — Railway volume (recommended)**

1. Railway → your service → **Volumes** → mount at `/data`.
2. One-time: run Phase 1 locally, upload `restaurants.parquet` to the volume, or run ingest in a one-off shell:
   ```bash
   python -m zomato_rec.phase1.ingest
   ```
   with output under `/data/processed/`.
3. Set `ZOMATO_PROCESSED_DATASET=/data/processed/restaurants.parquet`.

**Option B — Build-time ingest (slower, no volume)**

Add a custom **build** command or deploy hook:

```bash
pip install -r requirements.txt
python -m zomato_rec.phase1.ingest
```

First deploy downloads from Hugging Face (~1–4 min). Ephemeral filesystem may lose data on redeploy unless you use a volume.

**Option C — Object storage**

Upload Parquet to S3/R2, fetch in build or at startup, set `ZOMATO_PROCESSED_DATASET` to the local path after download.

### 5. Verify Railway

1. Generate a public domain: Railway → **Settings** → **Networking** → **Generate domain**.
2. Open `https://<your-service>.up.railway.app/api/health`.
3. Expect `"status": "ok"`, `"dataset_ok": true`, `"groq_configured": true`.
4. Open `/docs` for OpenAPI.

Copy the Railway URL (no trailing slash) for Vercel.

---

## Part 2 — Frontend on Vercel

### 1. Import the project

1. [Vercel](https://vercel.com) → **Add New** → **Project** → import the same GitHub repo.
2. **Root Directory**: `frontend` (important).
3. Framework preset: **Next.js** (auto-detected).
4. `frontend/vercel.json` already sets `buildCommand` and `installCommand`.

### 2. Environment variables (Vercel → Settings → Environment Variables)

| Variable | Environments | Value |
|----------|----------------|-------|
| `NEXT_PUBLIC_API_URL` | Production, Preview | `https://<your-railway-service>.up.railway.app` |

No trailing slash. Redeploy after changing this variable.

### 3. Deploy

1. Deploy the default branch.
2. Open `https://<project>.vercel.app`.
3. Submit a recommendation; confirm network calls go to Railway `/api/recommendations`.

### 4. CORS round-trip

If the browser shows a CORS error:

1. Add the exact Vercel origin to Railway `API_CORS_ORIGINS` (include `https://`).
2. Set `API_CORS_DISABLE_LOCALHOST_REGEX=1` on Railway.
3. Redeploy Railway, then hard-refresh the Vercel site.

---

## Part 3 — Order of operations (checklist)

- [ ] Phase 1 dataset exists on Railway (volume or build ingest).
- [ ] Railway deployed with `GROQ_API_KEY` and public URL.
- [ ] `GET /api/health` shows `dataset_ok: true`.
- [ ] Vercel deployed with `NEXT_PUBLIC_API_URL` = Railway URL.
- [ ] `API_CORS_ORIGINS` on Railway includes Vercel production URL.
- [ ] End-to-end test: preferences form → recommendations on Vercel.

---

## Local development (unchanged)

**Backend** (repo root):

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend**:

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

`frontend/.env.local`: `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|----------------|-----|
| `503` / dataset not found | No Parquet on Railway | Volume + `ZOMATO_PROCESSED_DATASET`, or run Phase 1 ingest |
| CORS error in browser | Vercel origin not allowed | Update `API_CORS_ORIGINS` on Railway |
| Empty recommendations / Groq error | Missing `GROQ_API_KEY` | Set on Railway, redeploy |
| UI calls wrong host | `NEXT_PUBLIC_API_URL` unset on Vercel | Set in Vercel env, redeploy frontend |
| `dataset_ok: false` on health | Wrong path | Check `ZOMATO_PROCESSED_DATASET` and volume mount |

---

## Files reference

| File | Purpose |
|------|---------|
| `railway.toml` | Railway build/deploy defaults |
| `Procfile` | Alternative process definition |
| `requirements.txt` | `pip install -e .[api]` for Railway |
| `frontend/vercel.json` | Vercel build settings |
| `backend/app/main.py` | CORS + API routes + startup dataset check |
| `backend/app/dataset.py` | Railway `/data` path resolution + optional ingest |
| `backend/app/railway_env.py` | Railway / production CORS helpers |
| `nixpacks.toml` / `runtime.txt` | Python 3.12 build for Railway |
| `.env.example` | Local and production variable template |
