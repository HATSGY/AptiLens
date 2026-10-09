"""
Core algorithmic logic for Graph Analysis: Bar, Pie, Line, Scatter and
Histogram interpretation.

Every "analyze_*" function computes real statistics with numpy/pandas
first. The AI layer (see src/ai) is only ever handed these already-verified
numbers -- it is never asked to eyeball a picture and guess.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# A realistic exam-score style dataset used only for the Histogram view,
# since a histogram needs many raw observations rather than one row per
# category (unlike the bar/line/pie/scatter views, which read graph_data.csv).
SAMPLE_HISTOGRAM_SCORES = [
    41, 52, 58, 63, 47, 71, 66, 74, 39, 82,
    55, 61, 69, 73, 48, 77, 84, 59, 65, 91,
    44, 56, 62, 70, 68, 53, 79, 87, 60, 45,
    72, 64, 57, 88, 50, 67, 75, 42, 81, 63,
]


def load_graph_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path.name}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"'{path.name}' contains no data.")
    return df


# --------------------------------------------------------------------------
# Bar graph
# --------------------------------------------------------------------------
def analyze_bar(categories: list[str], values: list[float]) -> dict:
    arr = np.array(values, dtype=float)
    max_idx, min_idx = int(arr.argmax()), int(arr.argmin())
    difference = float(arr.max() - arr.min())
    pct_change_first_last = ((arr[-1] - arr[0]) / arr[0]) * 100 if arr[0] != 0 else float("nan")

    return {
        "categories": categories,
        "values": values,
        "highest": {"category": categories[max_idx], "value": float(arr.max())},
        "lowest": {"category": categories[min_idx], "value": float(arr.min())},
        "difference_highest_lowest": round(difference, 2),
        "percentage_change_first_to_last": round(pct_change_first_last, 2),
        "average": round(float(arr.mean()), 2),
    }


# --------------------------------------------------------------------------
# Pie chart
# --------------------------------------------------------------------------
def analyze_pie(categories: list[str], values: list[float]) -> dict:
    arr = np.array(values, dtype=float)
    total = float(arr.sum())
    percentages = (arr / total * 100) if total else np.zeros_like(arr)
    max_idx = int(arr.argmax())

    sector_breakdown = [
        {"category": c, "value": float(v), "percentage": round(float(p), 2)}
        for c, v, p in zip(categories, values, percentages)
    ]

    return {
        "categories": categories,
        "values": values,
        "total": round(total, 2),
        "largest_sector": {"category": categories[max_idx], "percentage": round(float(percentages[max_idx]), 2)},
        "sector_breakdown": sector_breakdown,
    }


# --------------------------------------------------------------------------
# Line graph
# --------------------------------------------------------------------------
def analyze_line(x_labels: list[str], values: list[float]) -> dict:
    arr = np.array(values, dtype=float)
    max_idx, min_idx = int(arr.argmax()), int(arr.argmin())
    diffs = np.diff(arr)
    overall_change = float(arr[-1] - arr[0])
    overall_pct = (overall_change / arr[0] * 100) if arr[0] != 0 else float("nan")

    if np.all(diffs > 0):
        trend = "Consistently increasing"
    elif np.all(diffs < 0):
        trend = "Consistently decreasing"
    elif overall_change > 0:
        trend = "Fluctuating, with an overall upward trend"
    elif overall_change < 0:
        trend = "Fluctuating, with an overall downward trend"
    else:
        trend = "Fluctuating, roughly flat overall"

    biggest_jump_idx = int(np.argmax(diffs)) if len(diffs) else None
    biggest_drop_idx = int(np.argmin(diffs)) if len(diffs) else None

    return {
        "x_labels": x_labels,
        "values": values,
        "maximum": {"point": x_labels[max_idx], "value": float(arr.max())},
        "minimum": {"point": x_labels[min_idx], "value": float(arr.min())},
        "overall_change": round(overall_change, 2),
        "overall_percentage_change": round(overall_pct, 2),
        "trend": trend,
        "biggest_increase": (
            {"from": x_labels[biggest_jump_idx], "to": x_labels[biggest_jump_idx + 1],
             "amount": round(float(diffs[biggest_jump_idx]), 2)}
            if biggest_jump_idx is not None else None
        ),
        "biggest_decrease": (
            {"from": x_labels[biggest_drop_idx], "to": x_labels[biggest_drop_idx + 1],
             "amount": round(float(diffs[biggest_drop_idx]), 2)}
            if biggest_drop_idx is not None else None
        ),
    }


# --------------------------------------------------------------------------
# Scatter diagram
# --------------------------------------------------------------------------
def analyze_scatter(x: list[float], y: list[float]) -> dict:
    if len(x) != len(y):
        raise ValueError("X and Y series must be the same length.")
    x_arr, y_arr = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x_arr) < 2 or np.std(x_arr) == 0 or np.std(y_arr) == 0:
        correlation = 0.0
    else:
        correlation = float(np.corrcoef(x_arr, y_arr)[0, 1])

    abs_corr = abs(correlation)
    if abs_corr >= 0.8:
        strength = "Very strong"
    elif abs_corr >= 0.6:
        strength = "Strong"
    elif abs_corr >= 0.3:
        strength = "Moderate"
    elif abs_corr >= 0.1:
        strength = "Weak"
    else:
        strength = "Little to no"

    direction = "positive" if correlation > 0 else ("negative" if correlation < 0 else "no")

    # Simple least-squares regression line: y = m*x + c
    if np.std(x_arr) != 0:
        m, c = np.polyfit(x_arr, y_arr, 1)
    else:
        m, c = 0.0, float(np.mean(y_arr))

    return {
        "x": x, "y": y,
        "correlation_coefficient": round(correlation, 4),
        "relationship": f"{strength} {direction} relationship" if direction != "no" else "No linear relationship",
        "regression_line": f"y = {m:.3f}x + {c:.3f}",
        "slope": round(float(m), 4),
        "intercept": round(float(c), 4),
    }


# --------------------------------------------------------------------------
# Histogram
# --------------------------------------------------------------------------
def analyze_histogram(values: list[float], num_bins: int = 6) -> dict:
    arr = np.array(values, dtype=float)
    counts, bin_edges = np.histogram(arr, bins=num_bins)
    intervals = [f"{bin_edges[i]:.0f}-{bin_edges[i + 1]:.0f}" for i in range(len(bin_edges) - 1)]
    max_freq_idx = int(np.argmax(counts))

    return {
        "values": values,
        "intervals": intervals,
        "frequencies": counts.tolist(),
        "highest_frequency_interval": intervals[max_freq_idx],
        "highest_frequency": int(counts[max_freq_idx]),
        "mean": round(float(arr.mean()), 2),
        "median": round(float(np.median(arr)), 2),
        "std_dev": round(float(arr.std()), 2),
        "total_observations": int(arr.size),
    }
