"""
Reusable input-validation helpers.

Every function here either returns a cleanly-typed value or raises a
ValueError with a human-readable message that is safe to show directly
in the GUI.
"""

from __future__ import annotations

import datetime as _dt


def validate_int_in_range(value: str, low: int, high: int, field_name: str = "Value") -> int:
    """Parse `value` as an int and ensure low <= value <= high."""
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name} cannot be empty.")
    try:
        parsed = int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a whole number.") from exc
    if not (low <= parsed <= high):
        raise ValueError(f"{field_name} must be between {low} and {high}.")
    return parsed


def validate_float(value: str, field_name: str = "Value", allow_negative: bool = True) -> float:
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name} cannot be empty.")
    try:
        parsed = float(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a number.") from exc
    if not allow_negative and parsed < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return parsed


def validate_hour_minute(hour: str, minute: str) -> tuple[int, int]:
    h = validate_int_in_range(hour, 0, 12, "Hour")
    m = validate_int_in_range(minute, 0, 59, "Minute")
    if h == 0:
        h = 12
    return h, m


def validate_date(day: str, month: str, year: str) -> _dt.date:
    """Validate a calendar date given as separate day/month/year strings.

    Uses datetime.date only to confirm the date actually exists (e.g. reject
    31 February); the algorithmic day-of-week / difference logic lives in
    calendar_logic.py and does not depend on this check.
    """
    d = validate_int_in_range(day, 1, 31, "Day")
    mo = validate_int_in_range(month, 1, 12, "Month")
    y = validate_int_in_range(year, 1, 9999, "Year")
    try:
        return _dt.date(y, mo, d)
    except ValueError as exc:
        raise ValueError("That date does not exist on the calendar.") from exc


def validate_non_empty_sequence(text: str, field_name: str = "Sequence") -> list[float]:
    """Parse a comma/space separated sequence of numbers."""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    raw_parts = [p for p in text.replace(",", " ").split(" ") if p.strip() != ""]
    if len(raw_parts) < 3:
        raise ValueError(f"{field_name} needs at least 3 numbers to detect a pattern.")
    numbers: list[float] = []
    for part in raw_parts:
        try:
            numbers.append(float(part))
        except ValueError as exc:
            raise ValueError(f"'{part}' is not a valid number.") from exc
    return numbers


def safe_divide(numerator: float, denominator: float, field_name: str = "value") -> float:
    if denominator == 0:
        raise ValueError(f"Cannot compute {field_name}: division by zero.")
    return numerator / denominator
