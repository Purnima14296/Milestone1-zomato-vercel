from __future__ import annotations

import re
from typing import Any

from zomato_rec.phase2.models import BudgetRange


_WS_RE = re.compile(r"\s+")
_NUM_RE = re.compile(r"(\d+(?:\.\d+)?)")


def _norm_key(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return _WS_RE.sub(" ", s).strip()


def normalize_location(value: str) -> str:
    s = _WS_RE.sub(" ", value.strip())
    aliases = {
        "bengaluru": "Bangalore",
        "bangalore": "Bangalore",
        "new delhi": "Delhi",
        "delhi ncr": "Delhi",
    }
    return aliases.get(_norm_key(s), s)


def parse_cuisines(value: str | None) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,\|/&]+", value)
    out: list[str] = []
    seen: set[str] = set()
    for p in parts:
        p = p.strip()
        if not p:
            continue
        k = _norm_key(p)
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(p)
    return out


def parse_min_rating(value: str | float | int | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        r = float(value)
        return r if 0 <= r <= 5 else None
    s = value.strip()
    if not s:
        return None
    s = s.replace("+", "").strip()
    m = _NUM_RE.search(s)
    if not m:
        return None
    r = float(m.group(1))
    return r if 0 <= r <= 5 else None


def parse_budget(value: Any) -> BudgetRange | None:
    """
    Supported examples:
    - low / medium / high
    - 500
    - 500-800
    - under 400 / below 400
    - above 1000 / over 1000
    - no budget / any
    """

    if value is None:
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        return BudgetRange(min=0, max=v) if v > 0 else None

    s = str(value).strip().lower()
    if not s:
        return None
    if s in {"any", "no budget", "none", "na", "n/a"}:
        return None

    # bucket mapping (can be tuned later)
    bucket = {
        "low": BudgetRange(min=0, max=400),
        "budget": BudgetRange(min=0, max=400),
        "medium": BudgetRange(min=400, max=800),
        "mid": BudgetRange(min=400, max=800),
        "high": BudgetRange(min=800, max=None),
        "premium": BudgetRange(min=800, max=None),
    }
    if s in bucket:
        return bucket[s]

    # ranges like 500-800
    if "-" in s:
        a, b = [p.strip() for p in s.split("-", 1)]
        ma = _NUM_RE.search(a)
        mb = _NUM_RE.search(b)
        if ma and mb:
            lo = float(ma.group(1))
            hi = float(mb.group(1))
            if lo > hi:
                lo, hi = hi, lo
            return BudgetRange(min=lo, max=hi)

    # under/below
    if "under" in s or "below" in s:
        m = _NUM_RE.search(s)
        if not m:
            return None
        hi = float(m.group(1))
        return BudgetRange(min=0, max=hi)

    # above/over
    if "above" in s or "over" in s:
        m = _NUM_RE.search(s)
        if not m:
            return None
        lo = float(m.group(1))
        return BudgetRange(min=lo, max=None)

    # single number
    m = _NUM_RE.search(s)
    if m:
        hi = float(m.group(1))
        return BudgetRange(min=0, max=hi) if hi > 0 else None

    return None

