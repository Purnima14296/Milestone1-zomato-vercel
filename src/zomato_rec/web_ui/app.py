from __future__ import annotations

import os

import streamlit as st

from zomato_rec.phase2.io import save_preferences
from zomato_rec.phase2.models import UserPreferences
from zomato_rec.phase2.normalize import normalize_location, parse_budget, parse_cuisines, parse_min_rating


DEFAULT_OUT = os.path.join("storage", "preferences.json")


def main() -> None:
    st.set_page_config(page_title="Zomato Recommender (Milestone 1)", layout="centered")
    st.title("Restaurant Preferences")
    st.caption("Phase 2 input UI — saves validated preferences for later phases.")

    with st.form("prefs"):
        location = st.text_input("Location (city/locality)", placeholder="e.g., Bangalore", value="")
        budget = st.text_input("Budget (optional)", placeholder="e.g., low / medium / high / 500 / 500-800 / under 400")
        cuisines = st.text_input("Cuisine(s) (optional)", placeholder="e.g., Italian, Chinese")
        min_rating = st.text_input("Minimum rating (optional)", placeholder="e.g., 4 or 4+")
        extra = st.text_area("Additional preferences (optional)", placeholder="e.g., family-friendly, quick service")
        out_path = st.text_input("Save to", value=DEFAULT_OUT)
        submitted = st.form_submit_button("Save preferences")

    if not submitted:
        return

    if not location.strip():
        st.error("Location is required.")
        return

    prefs = UserPreferences(
        location=normalize_location(location),
        budget=parse_budget(budget),
        cuisines=parse_cuisines(cuisines),
        minimum_rating=parse_min_rating(min_rating),
        additional_preferences=(extra.strip() if extra and extra.strip() else None),
    )

    save_preferences(prefs, out_path)
    st.success(f"Saved preferences to `{out_path}`")
    st.subheader("Saved JSON preview")
    st.json(prefs.model_dump())


if __name__ == "__main__":
    main()

