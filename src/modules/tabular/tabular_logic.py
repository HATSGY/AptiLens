"""
Core algorithmic logic for Tabular Data Interpretation.

Loads a CSV with pandas and performs verified arithmetic operations on it.
All numeric work is done with pandas/numpy -- nothing here is hardcoded.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.validators import safe_divide

OPERATIONS = [
    "Sum", "Average", "Maximum", "Minimum", "Percentage of Total",
    "Ratio (Row A : Row B)", "Difference (Row A - Row B)",
    "Percentage Increase/Decrease (Row A -> Row B)",
]


def load_tabular_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path.name}")
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001 - surfaced to the GUI as a friendly message
        raise ValueError(f"Could not read '{path.name}' as a CSV file: {exc}") from exc
    if df.empty:
        raise ValueError(f"'{path.name}' contains no data.")
    return df


def numeric_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def label_column(df: pd.DataFrame) -> str | None:
    non_numeric = [c for c in df.columns if c not in numeric_columns(df)]
    return non_numeric[0] if non_numeric else None


def apply_operation(df: pd.DataFrame, operation: str, column: str,
                     row_a: int | None = None, row_b: int | None = None) -> dict:
    """Apply one of OPERATIONS to `column` of `df` and return a full worked answer."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")
    series = df[column]
    if not pd.api.types.is_numeric_dtype(series):
        raise ValueError(f"Column '{column}' is not numeric.")

    label_col = label_column(df)

    def row_label(idx: int) -> str:
        if label_col is not None:
            return str(df.iloc[idx][label_col])
        return f"Row {idx + 1}"

    if operation == "Sum":
        total = float(series.sum())
        return {"operation": operation, "column": column,
                "formula": "Sum = Σ(values)",
                "calculation": " + ".join(f"{v:g}" for v in series),
                "answer": round(total, 4)}

    if operation == "Average":
        total = float(series.sum())
        n = len(series)
        avg = total / n
        return {"operation": operation, "column": column,
                "formula": "Average = Sum / Count",
                "calculation": f"{total:g} / {n}",
                "answer": round(avg, 4)}

    if operation == "Maximum":
        idx = int(series.idxmax())
        return {"operation": operation, "column": column,
                "formula": "Maximum = max(values)",
                "calculation": f"max({[round(v,2) for v in series]}) at {row_label(idx)}",
                "answer": float(series.max()), "row": row_label(idx)}

    if operation == "Minimum":
        idx = int(series.idxmin())
        return {"operation": operation, "column": column,
                "formula": "Minimum = min(values)",
                "calculation": f"min({[round(v,2) for v in series]}) at {row_label(idx)}",
                "answer": float(series.min()), "row": row_label(idx)}

    if operation == "Percentage of Total":
        if row_a is None:
            raise ValueError("Select a row to compute its percentage of the total.")
        total = float(series.sum())
        value = float(series.iloc[row_a])
        pct = safe_divide(value, total, "percentage") * 100
        return {"operation": operation, "column": column,
                "formula": "Percentage = (Row Value / Total) × 100",
                "calculation": f"({value:g} / {total:g}) × 100",
                "answer": round(pct, 2), "row": row_label(row_a)}

    if operation in ("Ratio (Row A : Row B)", "Difference (Row A - Row B)",
                     "Percentage Increase/Decrease (Row A -> Row B)"):
        if row_a is None or row_b is None:
            raise ValueError("Select both Row A and Row B for this operation.")
        a = float(series.iloc[row_a])
        b = float(series.iloc[row_b])

        if operation == "Ratio (Row A : Row B)":
            import math
            g = math.gcd(int(round(a * 100)), int(round(b * 100))) or 1
            ra, rb = round(a * 100 / g), round(b * 100 / g)
            return {"operation": operation, "column": column,
                    "formula": "Ratio = Row A : Row B",
                    "calculation": f"{a:g} : {b:g}",
                    "answer": f"{ra} : {rb}",
                    "row_a": row_label(row_a), "row_b": row_label(row_b)}

        if operation == "Difference (Row A - Row B)":
            diff = a - b
            return {"operation": operation, "column": column,
                    "formula": "Difference = Row A - Row B",
                    "calculation": f"{a:g} - {b:g}",
                    "answer": round(diff, 4),
                    "row_a": row_label(row_a), "row_b": row_label(row_b)}

        # Percentage Increase/Decrease
        pct_change = safe_divide(b - a, a, "percentage change") * 100
        direction = "increase" if pct_change >= 0 else "decrease"
        return {"operation": operation, "column": column,
                "formula": "% Change = ((B - A) / A) × 100",
                "calculation": f"(({b:g} - {a:g}) / {a:g}) × 100",
                "answer": f"{abs(round(pct_change, 2))}% {direction}",
                "row_a": row_label(row_a), "row_b": row_label(row_b)}

    raise ValueError(f"Unknown operation: {operation}")
