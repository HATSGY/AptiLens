"""General-purpose helper functions shared across modules."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    """Load a JSON file, raising a friendly error if it is missing/invalid."""
    if not path.exists():
        raise FileNotFoundError(f"Required data file not found: {path.name}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Data file '{path.name}' is not valid JSON.") from exc


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def format_percentage(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 2) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.{decimals}f}"


class Stopwatch:
    """Small helper used by Practice Mode to time each question."""

    def __init__(self) -> None:
        self._start: float | None = None

    def start(self) -> None:
        self._start = time.perf_counter()

    def elapsed(self) -> float:
        if self._start is None:
            return 0.0
        return round(time.perf_counter() - self._start, 2)


def ordinal(n: int) -> str:
    """Return the ordinal string for an integer, e.g. 1 -> '1st'."""
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
