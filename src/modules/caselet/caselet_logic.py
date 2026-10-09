"""
Core algorithmic logic for Caselet Data Interpretation.

Caselets are loaded from data/caselet_data.json. Every question inside a
caselet declares a generic `operation` + `params`; `solve_caselet_question`
interprets that declaration against the caselet's table with pandas and
returns a fully worked, verified answer. Nothing is hardcoded per-question:
if you edit the JSON dataset, the same solver still produces correct maths.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.helpers import load_json
from src.utils.validators import safe_divide


def load_caselets(path: Path) -> list[dict[str, Any]]:
    raw = load_json(path)
    if not isinstance(raw, list) or not raw:
        raise ValueError("caselet_data.json must contain a non-empty list of caselets.")
    return raw


def caselet_dataframe(caselet: dict[str, Any]) -> pd.DataFrame:
    table = caselet["table"]
    df = pd.DataFrame(table["rows"], columns=table["columns"])
    index_col = table.get("index_col")
    if index_col and index_col in df.columns:
        df = df.set_index(index_col)
    return df


def _row_value(df: pd.DataFrame, column: str, row_label: str) -> float:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not present in this caselet's table.")
    if row_label not in df.index:
        raise ValueError(f"Row '{row_label}' not present in this caselet's table.")
    return float(df.loc[row_label, column])


def solve_caselet_question(caselet: dict[str, Any], question: dict[str, Any]) -> dict:
    """Generic solver driven entirely by `question['operation']` + `params`."""
    df = caselet_dataframe(caselet)
    op = question["operation"]
    params = question.get("params", {})

    if op == "sum":
        col = params["column"]
        total = float(df[col].sum())
        return {"formula": f"Sum({col}) = Σ values in '{col}'",
                "calculation": " + ".join(f"{v:g}" for v in df[col]),
                "answer": round(total, 2)}

    if op == "average":
        col = params["column"]
        total = float(df[col].sum())
        n = len(df[col])
        return {"formula": f"Average({col}) = Sum / Count",
                "calculation": f"{total:g} / {n}",
                "answer": round(total / n, 2)}

    if op == "percentage_of_total":
        col, row_label = params["column"], params["row_label"]
        total = float(df[col].sum())
        value = _row_value(df, col, row_label)
        pct = safe_divide(value, total, "percentage") * 100
        return {"formula": "Percentage = (Row Value / Column Total) × 100",
                "calculation": f"({value:g} / {total:g}) × 100",
                "answer": round(pct, 2)}

    if op == "ratio":
        col = params["column"]
        a = _row_value(df, col, params["row_label_a"])
        b = _row_value(df, col, params["row_label_b"])
        import math
        g = math.gcd(int(round(a * 100)), int(round(b * 100))) or 1
        return {"formula": f"Ratio = {params['row_label_a']} : {params['row_label_b']} (column '{col}')",
                "calculation": f"{a:g} : {b:g}",
                "answer": f"{round(a*100/g)} : {round(b*100/g)}"}

    if op == "difference":
        row_label = params["row_label"]
        col_a, col_b = params["column_a"], params["column_b"]
        a = _row_value(df, col_a, row_label)
        b = _row_value(df, col_b, row_label)
        return {"formula": f"Difference = {col_a} - {col_b} (row '{row_label}')",
                "calculation": f"{a:g} - {b:g}",
                "answer": round(a - b, 2)}

    if op == "comparison_max":
        col = params["column"]
        idx = df[col].idxmax()
        return {"formula": f"Comparison = max({col}) across all rows",
                "calculation": f"max({[round(v,2) for v in df[col]]})",
                "answer": f"{idx} with {df[col].max():g}"}

    if op == "total":
        cols = params.get("columns") or list(df.select_dtypes("number").columns)
        total = float(df[cols].to_numpy().sum())
        return {"formula": f"Grand Total = Σ over columns {cols}",
                "calculation": f"sum of all values in {cols}",
                "answer": round(total, 2)}

    raise ValueError(f"Unsupported caselet operation: {op}")
