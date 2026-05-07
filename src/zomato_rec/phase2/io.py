from __future__ import annotations

import json
import os

from zomato_rec.phase2.models import UserPreferences


def save_preferences(prefs: UserPreferences, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(prefs.model_dump(), f, indent=2, ensure_ascii=False)


def load_preferences(path: str) -> UserPreferences:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return UserPreferences.model_validate(data)

