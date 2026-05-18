## Milestone 1 — Zomato Restaurant Recommendation (Phase 0)

This repo contains the foundation for an AI-powered restaurant recommendation system inspired by Zomato.

### Folder structure

- `Docs/`: project documentation
- `src/`: application source code
- `data/`: local datasets (ignored by git)
- `storage/`: local DB files (ignored by git)
- `backend/`: Phase 7 FastAPI service (repo root)
- `frontend/`: Phase 8 Next.js app (repo root)

### Setup (Windows PowerShell)

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -e ".[api]"
```

Create your env file:

```bash
copy .env.example .env
```

Run the phase-0 sanity check:

```bash
python -m zomato_rec.main --check
```

### Phase 1 (data ingestion)

Ingest + preprocess the dataset into `data/processed/`:

```bash
python -m zomato_rec.phase1.ingest
```

### Phase 2 (user preferences)

Collect validated user preferences and save them to `storage/preferences.json`:

#### Web UI (Phase 8)

Use the Next.js app (see [Phase 7–8](#phase-78-api--nextjs-web-ui) below) or the CLI.

#### CLI

```bash
python -m zomato_rec.phase2.collect --interactive
```

Or non-interactive:

```bash
python -m zomato_rec.phase2.collect --location Bellandur --budget "500-800" --cuisines "Italian, Chinese" --min-rating 4
```

### Phase 3 (candidate retrieval + shortlist)

Build a deterministic shortlist (JSON) from the processed dataset + saved preferences:

```bash
python -m zomato_rec.phase3.shortlist --top-n 30
```

### Phase 4 (LLM ranking + explanations with Groq)

1) Set your Groq key in `.env`:

- `GROQ_API_KEY=...`
- `GROQ_MODEL=llama-3.3-70b-versatile` (or any Groq-supported model)

2) Run:

```bash
python -m zomato_rec.phase4.run --top-k 5
```

### Phase 7–8 (API + Next.js web UI)

Requires Phase 1 completed (`data/processed/restaurants.parquet`) and `GROQ_API_KEY` in `.env`.

**Terminal 1 — backend (from repo root, venv active)**

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Optional: `API_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000` in `.env` if you use another origin.

**Terminal 2 — frontend**

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 . Set `NEXT_PUBLIC_API_URL` in `frontend/.env.local` if the API is not on `http://127.0.0.1:8000`.

See `backend/README.md` and `frontend/README.md` for details.

### Production deployment (Render + Vercel)

- **Backend (FastAPI)** → [Render](https://render.com)
- **Frontend (Next.js)** → [Vercel](https://vercel.com)

Step-by-step instructions: **[DEPLOYMENT.md](DEPLOYMENT.md)**.
