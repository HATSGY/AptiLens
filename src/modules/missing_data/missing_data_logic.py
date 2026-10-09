"""
Core algorithmic logic for Missing Data Interpretation problems.

Covers the standard competitive-exam "fill in the missing cell" style
questions built on: totals, averages, ratios and year-over-year growth
tables. Every solver shows the known values, the formula used, and the
derived missing value.
"""

from __future__ import annotations

from typing import Optional

from src.utils.validators import safe_divide


def solve_missing_by_total(known_values: dict[str, Optional[float]], total: float) -> dict:
    """Exactly one entry in `known_values` should be None; solve for it."""
    missing_keys = [k for k, v in known_values.items() if v is None]
    if len(missing_keys) != 1:
        raise ValueError("Exactly one value must be missing to solve by total.")
    missing_key = missing_keys[0]
    known_sum = sum(v for v in known_values.values() if v is not None)
    missing_value = total - known_sum

    return {
        "formula": f"{missing_key} = Total - (sum of all other known values)",
        "known_values": known_values,
        "total": total,
        "calculation": f"{missing_key} = {total:g} - {known_sum:g}",
        "missing_key": missing_key,
        "answer": round(missing_value, 2),
    }


def solve_missing_by_average(values: list[Optional[float]], average: float) -> dict:
    missing_indices = [i for i, v in enumerate(values) if v is None]
    if len(missing_indices) != 1:
        raise ValueError("Exactly one value must be missing to solve by average.")
    idx = missing_indices[0]
    n = len(values)
    known_sum = sum(v for v in values if v is not None)
    required_total = average * n
    missing_value = required_total - known_sum

    return {
        "formula": "Missing value = (Average × Count) - (sum of known values)",
        "known_values": values,
        "average": average,
        "count": n,
        "calculation": f"({average:g} × {n}) - {known_sum:g}",
        "missing_index": idx,
        "answer": round(missing_value, 2),
    }


def solve_missing_by_ratio(a: Optional[float], b: Optional[float],
                            ratio_a: float, ratio_b: float) -> dict:
    """Given a:b = ratio_a:ratio_b and one of a/b, find the other."""
    if a is None and b is not None:
        answer = safe_divide(b * ratio_a, ratio_b, "ratio value")
        return {
            "formula": f"a = b × (ratio_a / ratio_b)   [a:b = {ratio_a:g}:{ratio_b:g}]",
            "calculation": f"{b:g} × ({ratio_a:g} / {ratio_b:g})",
            "missing": "a", "answer": round(answer, 2),
        }
    if b is None and a is not None:
        answer = safe_divide(a * ratio_b, ratio_a, "ratio value")
        return {
            "formula": f"b = a × (ratio_b / ratio_a)   [a:b = {ratio_a:g}:{ratio_b:g}]",
            "calculation": f"{a:g} × ({ratio_b:g} / {ratio_a:g})",
            "missing": "b", "answer": round(answer, 2),
        }
    raise ValueError("Exactly one of a/b must be missing (set the other to None only).")


def solve_missing_growth_table(rows: list[dict]) -> dict:
    """Fill in the blanks of a Year | Value | Growth% table.

    `rows` is a list of dicts: {"year": int, "value": float|None, "growth_pct": float|None}
    Relationship for i >= 1:  value[i] = value[i-1] * (1 + growth_pct[i] / 100)

    Uses iterative constraint propagation: repeatedly scans every row and
    solves whichever single unknown in that row's relationship can be
    determined from the other two, until no more progress can be made.
    """
    rows = [dict(r) for r in rows]  # shallow copy so we don't mutate caller's data
    steps: list[str] = []
    changed = True
    iterations = 0

    while changed and iterations < 10:
        changed = False
        iterations += 1
        for i in range(1, len(rows)):
            prev_val = rows[i - 1]["value"]
            cur_val = rows[i]["value"]
            growth = rows[i]["growth_pct"]

            if cur_val is None and prev_val is not None and growth is not None:
                new_val = prev_val * (1 + growth / 100)
                rows[i]["value"] = round(new_val, 4)
                steps.append(
                    f"Value({rows[i]['year']}) = Value({rows[i-1]['year']}) × (1 + growth/100) "
                    f"= {prev_val:g} × (1 + {growth:g}/100) = {rows[i]['value']:g}"
                )
                changed = True

            elif growth is None and prev_val is not None and cur_val is not None:
                new_growth = safe_divide(cur_val - prev_val, prev_val, "growth %") * 100
                rows[i]["growth_pct"] = round(new_growth, 4)
                steps.append(
                    f"Growth({rows[i]['year']}) = ((Value({rows[i]['year']}) - Value({rows[i-1]['year']})) "
                    f"/ Value({rows[i-1]['year']})) × 100 = (({cur_val:g} - {prev_val:g}) / {prev_val:g}) × 100 "
                    f"= {rows[i]['growth_pct']:g}%"
                )
                changed = True

            elif prev_val is None and cur_val is not None and growth is not None:
                new_prev = safe_divide(cur_val, (1 + growth / 100), "previous value")
                rows[i - 1]["value"] = round(new_prev, 4)
                steps.append(
                    f"Value({rows[i-1]['year']}) = Value({rows[i]['year']}) / (1 + growth/100) "
                    f"= {cur_val:g} / (1 + {growth:g}/100) = {rows[i-1]['value']:g}"
                )
                changed = True

    unresolved = [
        r["year"] for r in rows
        if r["value"] is None or (rows.index(r) > 0 and r["growth_pct"] is None)
    ]

    return {
        "formula": "Value(year) = Value(previous year) × (1 + Growth% / 100)",
        "resolved_rows": rows,
        "steps": steps,
        "fully_solved": len(unresolved) == 0,
        "unresolved_years": unresolved,
    }


def sample_missing_data_problems() -> list[dict]:
    return [
        {
            "title": "Sales Growth Table",
            "description": "A company's sales grew year over year. Some cells are missing.",
            "rows": [
                {"year": 2022, "value": 100.0, "growth_pct": None},
                {"year": 2023, "value": None, "growth_pct": 20.0},
                {"year": 2024, "value": 144.0, "growth_pct": None},
            ],
        },
        {
            "title": "Quarterly Revenue Table",
            "description": "Quarterly revenue (in lakhs) with one missing quarter.",
            "rows": [
                {"year": "Q1", "value": 50.0, "growth_pct": None},
                {"year": "Q2", "value": None, "growth_pct": 10.0},
                {"year": "Q3", "value": None, "growth_pct": 15.0},
                {"year": "Q4", "value": 75.0, "growth_pct": None},
            ],
        },
    ]
