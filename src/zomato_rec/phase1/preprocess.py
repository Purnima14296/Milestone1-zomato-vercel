from __future__ import annotations

import re
from typing import Any

import pandas as pd


_WS_RE = re.compile(r"\s+")
_NUM_RE = re.compile(r"(\d+(?:\.\d+)?)")


def _norm_key(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return _WS_RE.sub(" ", s).strip()


def guess_column(columns: list[str], candidates: list[str]) -> str | None:
    """
    Try to find a column in `columns` that matches any of `candidates`
    using normalized (lowercased, punctuation-stripped) comparison.
    """

    norm_to_original: dict[str, str] = {_norm_key(c): c for c in columns}

    # Respect candidate priority order.
    for cand_raw in candidates:
        cand = _norm_key(cand_raw)
        if not cand:
            continue
        if cand in norm_to_original:
            return norm_to_original[cand]

    # fallback: partial match (still respects candidate order)
    for cand_raw in candidates:
        cand = _norm_key(cand_raw)
        if not cand:
            continue
        for n, original in norm_to_original.items():
            if cand in n or n in cand:
                return original
    return None


def parse_rating(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        r = float(value)
        return r if 0 <= r <= 5 else None
    s = str(value).strip()
    if not s or s.lower() in {"-", "na", "n/a", "new", "not rated", "not_rated"}:
        return None
    m = _NUM_RE.search(s)
    if not m:
        return None
    r = float(m.group(1))
    return r if 0 <= r <= 5 else None


def parse_cost(value: Any) -> float | None:
    """
    Normalize cost into a single numeric value (best-effort).
    Expected to represent a comparable estimate like "cost for two".
    """

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        c = float(value)
        return c if c > 0 else None
    s = str(value).strip()
    if not s or s.lower() in {"-", "na", "n/a", "unknown"}:
        return None
    s = s.replace(",", "")
    m = _NUM_RE.search(s)
    if not m:
        return None
    c = float(m.group(1))
    return c if c > 0 else None


def parse_cuisines(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        raw = [str(x) for x in value]
    else:
        raw = [str(value)]

    parts: list[str] = []
    for item in raw:
        item = item.strip()
        if not item:
            continue
        # common separators: comma, |, /, &
        for p in re.split(r"[,\|/&]+", item):
            p = p.strip()
            if p:
                parts.append(p)

    seen: set[str] = set()
    out: list[str] = []
    for p in parts:
        key = _norm_key(p)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def normalize_city(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    s = str(value).strip()
    if not s:
        return None
    # very light normalization; aliases can be extended later
    aliases = {
        "bengaluru": "Bangalore",
        "bangalore": "Bangalore",
        "delhi ncr": "Delhi",
        "new delhi": "Delhi",
    }
    k = _norm_key(s)
    return aliases.get(k, s)


def build_processed_df(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str | None]]:
    """
    Map arbitrary dataset schema into a stable processed schema.

    Output columns:
    - restaurant_name
    - city
    - cuisines (list[str])
    - cost_estimate
    - rating
    - raw (dict-like JSON-serializable)
    """

    cols = list(raw_df.columns)
    mapping = {
        "name": guess_column(cols, ["restaurant name", "name", "restaurant"]),
        # Prefer explicit city fields before falling back to general location/address.
        "city": guess_column(
            cols,
            [
                "listed_in(city)",
                "listed in city",
                "city",
                "location",
                "locality",
                "address",
            ],
        ),
        "cuisines": guess_column(cols, ["cuisines", "cuisine", "cuisine type"]),
        "cost": guess_column(cols, ["average cost", "avg cost", "cost", "price", "cost for two", "approx cost for two"]),
        "rating": guess_column(cols, ["rate", "rating", "aggregate rating", "user rating"]),
    }

    def _raw_row(row: pd.Series) -> dict[str, Any]:
        # keep a compact raw payload for traceability
        out: dict[str, Any] = {}
        for c in cols:
            v = row.get(c)
            if isinstance(v, float) and pd.isna(v):
                continue
            out[c] = v
        return out

    name_col = mapping["name"]
    city_col = mapping["city"]
    cuisine_col = mapping["cuisines"]
    cost_col = mapping["cost"]
    rating_col = mapping["rating"]

    processed = pd.DataFrame()
    processed["restaurant_name"] = raw_df[name_col].astype(str).str.strip() if name_col else None

    if city_col:
        processed["city"] = raw_df[city_col].apply(normalize_city)
    else:
        processed["city"] = None

    if cuisine_col:
        processed["cuisines"] = raw_df[cuisine_col].apply(parse_cuisines)
    else:
        processed["cuisines"] = [[] for _ in range(len(raw_df))]

    processed["cost_estimate"] = raw_df[cost_col].apply(parse_cost) if cost_col else None
    processed["rating"] = raw_df[rating_col].apply(parse_rating) if rating_col else None
    processed["raw"] = raw_df.apply(_raw_row, axis=1)

    # Clean up critical fields
    if name_col:
        processed["restaurant_name"] = processed["restaurant_name"].replace({"None": None, "nan": None, "": None})
    processed["city"] = processed["city"].replace({"None": None, "nan": None, "": None})

    processed = processed.dropna(subset=["restaurant_name", "city"], how="any").reset_index(drop=True)
    return processed, mapping

