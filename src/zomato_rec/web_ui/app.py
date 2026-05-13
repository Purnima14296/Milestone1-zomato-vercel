from __future__ import annotations

import html
import os
import sys
from pathlib import Path

# Repo root: src/zomato_rec/web_ui/app.py → parents[3] == repository root (for `backend` imports on Streamlit Cloud).
_REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (_REPO_ROOT / "src", _REPO_ROOT):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from dotenv import load_dotenv

load_dotenv(_REPO_ROOT / ".env", override=False)

import streamlit as st

from backend.app.pipeline import default_dataset_path, list_dataset_cities, run_recommendations
from backend.app.schemas import BudgetRangeIn, PreferencesIn, RecommendationRequest

# Fixed pipeline defaults (no advanced UI)
_DEFAULT_TOP_K = 5
_DEFAULT_SHORTLIST_N = 30


def _inject_streamlit_secrets() -> None:
    """Map Streamlit Cloud / local `.streamlit/secrets.toml` into os.environ for Settings + pipeline."""
    try:
        sec = st.secrets
    except FileNotFoundError:
        return
    for key in ("GROQ_API_KEY", "GROQ_MODEL", "ZOMATO_PROCESSED_DATASET", "HF_DATASET_ID", "HF_DATASET_SPLIT"):
        if key in sec and str(sec[key]).strip():
            os.environ[key] = str(sec[key]).strip()
    if "HF_TOKEN" in sec and str(sec["HF_TOKEN"]).strip():
        t = str(sec["HF_TOKEN"]).strip()
        os.environ["HF_TOKEN"] = t
        os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", t)


def _inject_ui_styles() -> None:
    """Typography + polish on top of `.streamlit/config.toml` dark theme."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Outfit:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet" />
        <style>
            :root {
                --olive: #8b9a6e;
                --olive-dark: #6f7d56;
                --olive-muted: #a8b596;
                --surface-form: #14141c;
                --surface-field: #0a0a10;
            }
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                font-family: "Source Sans 3", "Segoe UI", system-ui, sans-serif !important;
                font-size: 16px;
            }
            [data-testid="stAppViewContainer"] .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 900px;
            }
            /* Main title — distinct serif */
            h1 {
                font-family: "Fraunces", Georgia, "Times New Roman", serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
                font-size: 2.15rem !important;
                color: #f7f5f2 !important;
                line-height: 1.2 !important;
            }
            /* Section subtitles — dark olive on dark UI */
            h2, h3 {
                font-family: "Outfit", "Source Sans 3", sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                text-transform: none !important;
                color: var(--olive) !important;
                margin-top: 0.35rem !important;
            }
            /* Widget labels — lighter olive, different weight from body */
            [data-testid="stWidgetLabel"] p,
            label[data-testid="stWidgetLabel"] span {
                font-family: "Outfit", sans-serif !important;
                font-weight: 500 !important;
                font-size: 0.8125rem !important;
                letter-spacing: 0.06em !important;
                text-transform: uppercase !important;
                color: var(--olive-muted) !important;
            }
            /* Captions / helper copy */
            [data-testid="stCaption"] {
                font-family: "Source Sans 3", sans-serif !important;
                color: #9aa08c !important;
                font-size: 0.875rem !important;
                line-height: 1.5 !important;
            }
            [data-testid="stMarkdownContainer"] p {
                line-height: 1.55 !important;
                color: #d6d8d0 !important;
            }
            [data-testid="stForm"] {
                border: 1px solid rgba(139, 154, 110, 0.22);
                border-radius: 16px;
                padding: 1.25rem 1.35rem 1.5rem;
                background: var(--surface-form);
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 8px 28px rgba(0, 0, 0, 0.35);
            }
            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {
                color: rgba(160, 168, 150, 0.5) !important;
                opacity: 1 !important;
            }
            div[data-testid="stTextInput"] input::-webkit-input-placeholder,
            div[data-testid="stTextArea"] textarea::-webkit-input-placeholder {
                color: rgba(160, 168, 150, 0.5) !important;
            }
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {
                font-family: "Source Sans 3", sans-serif !important;
                background-color: var(--surface-field) !important;
                color: #eef0ea !important;
                border-color: rgba(255, 255, 255, 0.09) !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            }
            div[data-testid="stTextInput"]:hover input,
            div[data-testid="stTextArea"]:hover textarea {
                border-color: rgba(139, 154, 110, 0.35) !important;
                box-shadow: 0 0 0 1px rgba(139, 154, 110, 0.12) !important;
            }
            div[data-testid="stTextInput"]:focus-within input,
            div[data-testid="stTextArea"]:focus-within textarea {
                border-color: rgba(226, 55, 68, 0.55) !important;
                box-shadow: 0 0 0 2px rgba(226, 55, 68, 0.12) !important;
            }
            div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
                background-color: var(--surface-field) !important;
                border-color: rgba(255, 255, 255, 0.09) !important;
            }
            div[data-testid="stSelectbox"]:hover [data-baseweb="select"] > div {
                border-color: rgba(139, 154, 110, 0.35) !important;
                box-shadow: 0 0 0 1px rgba(139, 154, 110, 0.1) !important;
            }
            div[data-testid="stSelectbox"]:focus-within [data-baseweb="select"] > div {
                border-color: rgba(226, 55, 68, 0.5) !important;
                box-shadow: 0 0 0 2px rgba(226, 55, 68, 0.1) !important;
            }
            div[data-testid="stSelectbox"] [role="combobox"] {
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
                background-color: var(--surface-field) !important;
            }
            div[data-testid="stSelectbox"]:hover [role="combobox"] {
                border-color: rgba(139, 154, 110, 0.32) !important;
                box-shadow: 0 0 0 1px rgba(139, 154, 110, 0.1) !important;
            }
            div[data-testid="stFormSubmitButton"] button,
            section[data-testid="stSidebar"] button,
            .stButton > button {
                font-family: "Outfit", sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: 0.03em !important;
                transition: filter 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease !important;
            }
            div[data-testid="stFormSubmitButton"]:hover button {
                filter: brightness(1.04);
                box-shadow: 0 4px 14px rgba(226, 55, 68, 0.22) !important;
            }
            div[data-testid="stFormSubmitButton"]:active button {
                filter: brightness(0.98);
            }
            .stButton > button:hover,
            section[data-testid="stSidebar"] button:hover {
                filter: brightness(1.05);
                box-shadow: 0 3px 12px rgba(0, 0, 0, 0.28) !important;
            }
            .reco-card {
                border: 1px solid rgba(139, 154, 110, 0.18);
                border-radius: 14px;
                padding: 1rem 1.15rem;
                margin-bottom: 0.75rem;
                background: rgba(20, 22, 26, 0.85);
                transition: border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease !important;
            }
            .reco-card:hover {
                border-color: rgba(139, 154, 110, 0.35);
                background: rgba(26, 28, 32, 0.95);
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            }
            .reco-title {
                font-family: "Fraunces", Georgia, serif !important;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0 0 0.35rem 0;
                color: #f2f0ec !important;
            }
            .reco-meta { font-family: "Source Sans 3", sans-serif !important; font-size: 0.88rem; color: #a8b596 !important; margin-bottom: 0.5rem; }
            .reco-reason { font-family: "Source Sans 3", sans-serif !important; font-size: 0.95rem; line-height: 1.55; color: #c8ccc0 !important; margin: 0; }
            .reco-rank {
                font-family: "Outfit", sans-serif !important;
                color: var(--olive-muted) !important;
                font-weight: 600 !important;
                font-size: 0.72rem !important;
                text-transform: uppercase !important;
                letter-spacing: 0.08em !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _dataset_ok() -> bool:
    return default_dataset_path().is_file()


def _parse_cuisines(raw: str) -> list[str]:
    parts = [p.strip() for p in raw.replace("\n", ",").split(",")]
    return [p for p in parts if p]


def _default_parquet_paths() -> tuple[Path, Path]:
    out = _REPO_ROOT / "data" / "processed" / "restaurants.parquet"
    rep = _REPO_ROOT / "data" / "processed" / "ingest_report.json"
    return out, rep


def _run_phase1_bootstrap() -> None:
    """Build `data/processed/restaurants.parquet` from Hugging Face (same as `python -m zomato_rec.phase1.ingest`)."""
    from zomato_rec.config import Settings
    from zomato_rec.logging_config import configure_logging
    from zomato_rec.phase1.ingest import run as phase1_run

    s = Settings()
    configure_logging("WARNING")
    out, rep = _default_parquet_paths()
    phase1_run(
        dataset_id=s.hf_dataset_id,
        split=s.hf_dataset_split,
        out_path=str(out),
        out_format="parquet",
        report_path=str(rep),
    )


def _budget_range_in_from_text(raw: str) -> BudgetRangeIn | None:
    from zomato_rec.phase2.normalize import parse_budget

    br = parse_budget(raw)
    if br is None:
        return None
    return BudgetRangeIn(min=br.min, max=br.max)


def main() -> None:
    _inject_streamlit_secrets()

    st.set_page_config(
        page_title="Zomato AI Recommender",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    _inject_ui_styles()

    st.title("Find your next meal")
    st.caption(
        "Preferences → shortlist → Groq — same engine as the **FastAPI** backend. "
        "Use the **Next.js** app only when you run `frontend` + `backend` separately."
    )

    from zomato_rec.config import Settings

    settings = Settings()

    with st.sidebar:
        st.subheader("Status")
        if _dataset_ok():
            st.success("Dataset ready")
            st.caption(str(default_dataset_path()))
        else:
            st.warning("Dataset not built yet — use the button in the main area.")

        if settings.groq_api_key:
            st.success("Groq API key configured")
        else:
            st.error("Set `GROQ_API_KEY` in secrets or `.env`.")

        st.divider()
        st.caption("Streamlit Cloud: main file `streamlit_app.py`, `requirements.txt` at repo root.")

    if not _dataset_ok():
        st.error(
            "**No processed restaurant file yet.** This host has no `data/processed/restaurants.parquet` "
            "(that folder is not in git)."
        )
        st.markdown(
            "Run **Phase 1** once here: downloads the Hugging Face dataset and builds the Parquet. "
            "Typical time **1–4 minutes**."
        )
        if st.button("Prepare dataset from Hugging Face", type="primary"):
            try:
                with st.spinner("Downloading and preprocessing…"):
                    _run_phase1_bootstrap()
                st.success("Dataset ready. Reloading…")
                st.rerun()
            except Exception as e:
                st.error("Ingest failed. For private HF data, add **HF_TOKEN** to secrets.")
                st.exception(e)
        st.divider()

    cities: list[str] = []
    if _dataset_ok():
        try:
            cities = list_dataset_cities(limit=500)
        except Exception:
            cities = []

    with st.form("preferences"):
        st.markdown("### Your preferences")

        loc_col, budget_col = st.columns(2)
        with loc_col:
            if cities:
                loc_options = [""] + cities

                def _loc_label(v: str) -> str:
                    return "Select location" if v == "" else v

                location = st.selectbox("Location", options=loc_options, format_func=_loc_label)
            else:
                location = st.text_input("Location", placeholder="City or locality, e.g. Koramangala")

        with budget_col:
            budget_raw = st.text_input(
                "Budget (for two)",
                placeholder="Examples: 1500 · 500-2000 · under 800 · medium · high · leave empty for any",
                help="Numbers in ₹, ranges, “under/over”, or low / medium / high.",
                autocomplete="off",
            )

        r1, r2 = st.columns(2)
        with r1:
            rating_choice = st.selectbox(
                "Minimum rating",
                options=["Any", "3.0+", "3.5+", "4.0+", "4.5+"],
                index=0,
            )
        with r2:
            cuisines_raw = st.text_input(
                "Cuisines (optional)",
                placeholder="Comma-separated, e.g. North Indian, Thai",
                autocomplete="off",
            )

        extra = st.text_area(
            "Additional preferences (optional)",
            placeholder="Date night, outdoor seating, kid-friendly…",
            height=100,
        )

        submitted = st.form_submit_button("Get recommendations", type="primary", use_container_width=True)

    if not submitted:
        return

    if not (location or "").strip():
        st.error("Please choose or enter a location.")
        return

    if not settings.groq_api_key:
        st.error("Configure `GROQ_API_KEY` before running recommendations.")
        return

    if not _dataset_ok():
        st.error("Dataset still missing. Use **Prepare dataset from Hugging Face** above.")
        return

    budget_in = _budget_range_in_from_text(budget_raw)
    if budget_raw.strip() and budget_in is None:
        st.warning("Budget text was not recognized; continuing **without** a budget cap. Try a number, range (500-2000), or low / medium / high.")
    rating_map = {"Any": None, "3.0+": 3.0, "3.5+": 3.5, "4.0+": 4.0, "4.5+": 4.5}
    min_rating = rating_map[rating_choice]
    cuisines = _parse_cuisines(cuisines_raw)

    prefs = PreferencesIn(
        location=location.strip(),
        budget=budget_in,
        cuisines=cuisines,
        minimum_rating=min_rating,
        additional_preferences=extra.strip() if extra.strip() else None,
    )
    req = RecommendationRequest(
        preferences=prefs,
        top_k=_DEFAULT_TOP_K,
        shortlist_top_n=_DEFAULT_SHORTLIST_N,
    )

    with st.spinner("Finding restaurants…"):
        try:
            result = run_recommendations(req)
        except FileNotFoundError as e:
            st.error(str(e))
            return
        except ValueError as e:
            st.warning(str(e))
            return
        except RuntimeError as e:
            st.error(str(e))
            return
        except Exception as e:
            st.exception(e)
            return

    meta = result.metadata
    st.markdown("### Your picks")
    st.caption(
        f"{meta.model} · {meta.processing_time_ms:.0f} ms · {meta.shortlist_size} shortlisted "
        f"({meta.candidates_after_filtering} after filters)"
    )

    for row in result.recommendations:
        name = html.escape(str(row.get("restaurant_name", "Restaurant")))
        rank = html.escape(str(row.get("rank", "")))
        bits = [
            row.get("city"),
            f"★ {row['rating']}" if row.get("rating") is not None else None,
            f"~₹{row['cost_estimate']}" if row.get("cost_estimate") is not None else None,
        ]
        meta_line = html.escape(" · ".join(str(b) for b in bits if b))
        cu_html = ""
        if row.get("cuisines"):
            cu = row["cuisines"]
            cu_text = ", ".join(map(str, cu)) if isinstance(cu, list) else str(cu)
            cu_html = f'<p class="reco-meta" style="margin-top:0.25rem">{html.escape(cu_text)}</p>'
        reason_raw = str(row.get("reason", ""))
        reason = html.escape(reason_raw).replace("\n", "<br/>")
        st.markdown(
            f"""
            <div class="reco-card">
                <div class="reco-rank">Rank #{rank}</div>
                <p class="reco-title">{name}</p>
                <p class="reco-meta">{meta_line}</p>
                {cu_html}
                <p class="reco-reason">{reason}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
