import type { BudgetRangeIn } from "@/lib/types";

/** Parse free-text budget (e.g. `1500`, `500-800`, `₹1200`) for the API. */
export function parseBudgetInput(raw: string): BudgetRangeIn | null {
  let s = raw.trim().toLowerCase();
  if (!s) return null;
  if (["any", "no budget", "none", "na", "n/a"].includes(s)) return null;

  s = s.replace(/[₹,]/g, "").replace(/\s+/g, "");

  const range = s.match(/^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)$/);
  if (range) {
    let lo = Number(range[1]);
    let hi = Number(range[2]);
    if (!Number.isFinite(lo) || !Number.isFinite(hi) || lo < 0 || hi < 0) return null;
    if (lo > hi) [lo, hi] = [hi, lo];
    return { min: lo, max: hi };
  }

  const single = s.match(/^(\d+(?:\.\d+)?)$/);
  if (single) {
    const max = Number(single[1]);
    if (!Number.isFinite(max) || max <= 0) return null;
    return { min: 0, max };
  }

  return null;
}
