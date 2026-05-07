from __future__ import annotations

import json
import re
from typing import Any


class LLMOutputError(ValueError):
    pass


_JSON_BLOCK_RE = re.compile(r"(\{[\s\S]*\})")


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # Best-effort: extract first {...} block
    m = _JSON_BLOCK_RE.search(text)
    if not m:
        raise LLMOutputError("LLM output is not valid JSON and no JSON block was found.")
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise LLMOutputError(f"Failed to parse JSON block: {e}") from e
    if not isinstance(obj, dict):
        raise LLMOutputError("Parsed JSON is not an object.")
    return obj


def validate_and_normalize_recommendations(
    llm_text: str,
    *,
    allowed_names: set[str],
    top_k: int,
) -> list[dict[str, Any]]:
    obj = _extract_json_object(llm_text)
    recs = obj.get("recommendations")
    if not isinstance(recs, list):
        raise LLMOutputError("JSON must contain key 'recommendations' as a list.")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()

    for i, item in enumerate(recs):
        if not isinstance(item, dict):
            continue
        name = item.get("restaurant_name")
        reason = item.get("reason")

        if not isinstance(name, str) or not name.strip():
            continue
        name = name.strip()

        if name not in allowed_names:
            # drop hallucinations
            continue
        if name in seen:
            continue
        seen.add(name)

        if not isinstance(reason, str) or not reason.strip():
            reason = "Recommended based on your preferences."
        reason = reason.strip()

        normalized.append(
            {
                "rank": len(normalized) + 1,
                "restaurant_name": name,
                "reason": reason,
                "source": "groq_llm",
            }
        )
        if len(normalized) >= top_k:
            break

    if not normalized:
        raise LLMOutputError("No valid recommendations after validation (possible hallucinations or empty output).")

    return normalized

