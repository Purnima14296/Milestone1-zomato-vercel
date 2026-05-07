## Milestone 1 — Zomato Restaurant Recommendation (Phase 0)

This repo contains the foundation for an AI-powered restaurant recommendation system inspired by Zomato.

### Folder structure

- `Docs/`: project documentation
- `src/`: application source code
- `data/`: local datasets (ignored by git)
- `storage/`: local DB files (ignored by git)
- `logs/`: application logs (ignored by git)

### Setup (Windows PowerShell)

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
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

#### Web UI (recommended)

Run the basic web UI (this is the primary input method):

```bash
streamlit run src/zomato_rec/web_ui/app.py
```

#### CLI (optional)

```bash
python -m zomato_rec.phase2.collect --interactive
```

Or non-interactive:

```bash
python -m zomato_rec.phase2.collect --location Bangalore --budget "500-800" --cuisines "Italian, Chinese" --min-rating 4
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

