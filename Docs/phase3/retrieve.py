from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from zomato_rec.phase2.models import BudgetRange, UserPreferences


_WS_RE = re.compile(r"\s+")


def _norm_key(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return _WS_RE.sub(" ", s).strip()


def load_processed_dataset(path: str) -> pd.DataFrame:
    if path.lower().endswith(".parquet"):
        df = pd.read_parquet(path)
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    elif not path.lower().endswith((".parquet", ".csv")):
        raise ValueError(f"Unsupported dataset format: {path}")

    df = ensure_processed_schema(df)
    return df


def ensure_processed_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure the dataframe matches the Phase 1 processed schema expected by Phase 3.

    Expected columns:
    - restaurant_name (str)
    - city (str)
    - cuisines (list[str])
    - cost_estimate (float | None)
    - rating (float | None)
    - raw (object)

    This also supports a few common alternative column names and will rename them.
    """

    out = df.copy()

    rename_map: dict[str, str] = {}
    if "name" in out.columns and "restaurant_name" not in out.columns:
        rename_map["name"] = "restaurant_name"
    if "listed_in(city)" in out.columns and "city" not in out.columns:
        rename_map["listed_in(city)"] = "city"
    if "approx_cost(for two people)" in out.columns and "cost_estimate" not in out.columns:
        rename_map["approx_cost(for two people)"] = "cost_estimate"
    if "rate" in out.columns and "rating" not in out.columns:
        rename_map["rate"] = "rating"

    if rename_map:
        out = out.rename(columns=rename_map)

    required = {"restaurant_name", "city", "cuisines", "cost_estimate", "rating"}
    missing = sorted(required.difference(set(out.columns)))
    if missing:
        raise ValueError(
            "Dataset does not match expected processed schema. "
            f"Missing columns: {missing}. "
            "Tip: run Phase 1 ingestion first: `python -m zomato_rec.phase1.ingest` "
            "and pass the generated parquet via `--dataset`."
        )

    # Normalize cuisines: if it comes in as a string, convert to a list best-effort.
    def _to_list(v: Any) -> list[str]:
        if isinstance(v, list):
            return [str(x) for x in v if str(x).strip()]
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return []
        s = str(v).strip()
        if not s:
            return []
        return [p.strip() for p in re.split(r"[,\|/&]+", s) if p.strip()]

    out["cuisines"] = out["cuisines"].apply(_to_list)
    return out


def load_preferences(path: str) -> UserPreferences:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return UserPreferences.model_validate(data)


def _cuisine_match_score(row_cuisines: Any, wanted: list[str]) -> float:
    if not wanted:
        return 0.0
    if not isinstance(row_cuisines, list):
        return 0.0
    row_set = {_norm_key(x) for x in row_cuisines if isinstance(x, str)}
    wanted_set = {_norm_key(x) for x in wanted}
    if not wanted_set:
        return 0.0
    inter = row_set.intersection(wanted_set)
    return len(inter) / len(wanted_set)


def _budget_penalty(cost_estimate: float | None, budget: BudgetRange | None) -> float:
    """
    Returns a small penalty in [0, 1] for being far from budget range.
    If cost is missing or budget not provided, no penalty.
    """

    if budget is None or cost_estimate is None:
        return 0.0

    bmin = budget.min
    bmax = budget.max

    if bmin is not None and cost_estimate < bmin:
        # below min: mild penalty
        return min(1.0, (bmin - cost_estimate) / max(bmin, 1.0))
    if bmax is not None and cost_estimate > bmax:
        # above max: stronger penalty
        return min(1.0, (cost_estimate - bmax) / max(bmax, 1.0))
    return 0.0


def filter_candidates(df: pd.DataFrame, prefs: UserPreferences) -> pd.DataFrame:
    out = df.copy()

    # Location: dataset "city" is typically a locality label (e.g., BTM).
    # We match case-insensitively by substring, so "BTM" matches "BTM" and "BTM Layout".
    loc = _norm_key(prefs.location)
    if loc:
        mask = out["city"].astype(str).apply(lambda x: loc in _norm_key(x))
        out = out.loc[mask]

    # Min rating
    if prefs.minimum_rating is not None:
        out = out.loc[out["rating"].fillna(-1) >= prefs.minimum_rating]

    # Budget constraints (hard filter if both min/max present; otherwise one-sided)
    if prefs.budget is not None:
        bmin = prefs.budget.min
        bmax = prefs.budget.max
        if bmin is not None:
            out = out.loc[(out["cost_estimate"].isna()) | (out["cost_estimate"] >= bmin)]
        if bmax is not None:
            out = out.loc[(out["cost_estimate"].isna()) | (out["cost_estimate"] <= bmax)]

    # Cuisine: require at least one match if cuisines provided
    if prefs.cuisines:
        wanted_set = {_norm_key(x) for x in prefs.cuisines}

        def _has_any_match(v: Any) -> bool:
            if not isinstance(v, list):
                return False
            return bool({_norm_key(x) for x in v if isinstance(x, str)}.intersection(wanted_set))

        out = out.loc[out["cuisines"].apply(_has_any_match)]

    return out.reset_index(drop=True)


def score_candidates(df: pd.DataFrame, prefs: UserPreferences) -> pd.DataFrame:
    """
    Deterministic scoring for shortlist selection.
    Higher is better.
    """

    scored = df.copy()
    scored["__rating"] = scored["rating"].fillna(0.0).astype(float)
    scored["__cuisine_score"] = scored["cuisines"].apply(lambda v: _cuisine_match_score(v, prefs.cuisines))
    scored["__budget_penalty"] = scored["cost_estimate"].apply(lambda c: _budget_penalty(c, prefs.budget))

    # Weighted score: rating dominates; cuisine match helps; budget penalty reduces.
    scored["__score"] = (
        (scored["__rating"] / 5.0) * 0.70
        + scored["__cuisine_score"] * 0.25
        - scored["__budget_penalty"] * 0.15
    )

    # Stable tie-breakers
    scored = scored.sort_values(
        by=["__score", "__rating", "restaurant_name"],
        ascending=[False, False, True],
        kind="mergesort",
    )
    return scored.reset_index(drop=True)


def build_shortlist(
    df: pd.DataFrame,
    prefs: UserPreferences,
    *,
    top_n: int = 30,
    max_same_name: int = 3,
) -> pd.DataFrame:
    filtered = filter_candidates(df, prefs)
    scored = score_candidates(filtered, prefs)

    if len(scored) == 0:
        return scored

    # Simple diversification: limit repeated restaurant names.
    kept_rows: list[int] = []
    name_counts: dict[str, int] = {}

    for i, row in scored.iterrows():
        name = str(row.get("restaurant_name") or "").strip()
        key = _norm_key(name)
        if not key:
            continue
        cnt = name_counts.get(key, 0)
        if cnt >= max_same_name:
            continue
        name_counts[key] = cnt + 1
        kept_rows.append(i)
        if len(kept_rows) >= top_n:
            break

    return scored.loc[kept_rows].reset_index(drop=True)


@dataclass(frozen=True)
class ShortlistReport:
    processed_dataset_path: str
    preferences_path: str
    candidates_after_filtering: int
    shortlist_size: int
    output_path: str


def save_shortlist(shortlist_df: pd.DataFrame, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    records = shortlist_df.drop(columns=[c for c in shortlist_df.columns if c.startswith("__")], errors="ignore").to_dict(
        orient="records"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def run_phase3(
    *,
    processed_dataset_path: str = os.path.join("data", "processed", "restaurants.parquet"),
    preferences_path: str = os.path.join("storage", "preferences.json"),
    out_path: str = os.path.join("storage", "shortlist.json"),
    top_n: int = 30,
) -> ShortlistReport:
    df = load_processed_dataset(processed_dataset_path)
    prefs = load_preferences(preferences_path)

    filtered = filter_candidates(df, prefs)
    shortlist = build_shortlist(df, prefs, top_n=top_n)

    save_shortlist(shortlist, out_path)

    return ShortlistReport(
        processed_dataset_path=processed_dataset_path,
        preferences_path=preferences_path,
        candidates_after_filtering=len(filtered),
        shortlist_size=len(shortlist),
        output_path=out_path,
    )


def save_report(report: ShortlistReport, report_path: str) -> None:
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)

