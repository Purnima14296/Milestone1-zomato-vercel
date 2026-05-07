from __future__ import annotations

import json
from typing import Any

from zomato_rec.phase2.models import UserPreferences


def build_system_prompt() -> str:
    return (
        "You are a restaurant recommendation engine.\n"
        "You MUST recommend ONLY from the provided candidate list.\n"
        "Return STRICT JSON only. No markdown. No extra text.\n"
    )


def build_user_prompt(prefs: UserPreferences, candidates: list[dict[str, Any]], top_k: int) -> str:
    """
    Candidates is a list of dicts (from shortlist.json) containing:
    restaurant_name, city, cuisines, cost_estimate, rating
    """

    pref_payload = {
        "location": prefs.location,
        "budget": prefs.budget.model_dump() if prefs.budget else None,
        "cuisines": prefs.cuisines,
        "minimum_rating": prefs.minimum_rating,
        "additional_preferences": prefs.additional_preferences,
    }

    schema = {
        "recommendations": [
            {
                "rank": 1,
                "restaurant_name": "string (must match exactly one candidate restaurant_name)",
                "reason": "string (1-2 sentences, specific to user preferences)",
            }
        ]
    }

    return (
        "User preferences (JSON):\n"
        f"{json.dumps(pref_payload, ensure_ascii=False)}\n\n"
        "Candidate restaurants (JSON array). You may ONLY choose from these:\n"
        f"{json.dumps(candidates, ensure_ascii=False)}\n\n"
        f"Task:\n- Select and rank the best {top_k} restaurants.\n"
        "- Provide a short reason for each.\n\n"
        "Output JSON schema (example types):\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n"
    )

