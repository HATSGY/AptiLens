import datetime as dt

import pytest

from src.modules.calendar.calendar_logic import (
    calculate_day_of_week, days_between_dates, is_leap_year, shift_day, to_julian_day_number,
)

_PY_WEEKDAY_TO_NAME = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
    4: "Friday", 5: "Saturday", 6: "Sunday",
}


@pytest.mark.parametrize("year,expected", [
    (2000, True), (1900, False), (2100, False), (2024, True), (2023, False), (2400, True),
])
def test_is_leap_year(year, expected):
    assert is_leap_year(year)["is_leap"] is expected


@pytest.mark.parametrize("day,month,year", [
    (1, 1, 2024), (15, 6, 2000), (29, 2, 2024), (25, 12, 1999), (4, 7, 1776), (1, 1, 2100),
])
def test_day_of_week_matches_python_datetime(day, month, year):
    result = calculate_day_of_week(day, month, year)
    expected = _PY_WEEKDAY_TO_NAME[dt.date(year, month, day).weekday()]
    assert result["weekday"] == expected


def test_days_between_dates_matches_python_datetime():
    d1, d2 = (15, 1, 2024), (10, 3, 2024)
    result = days_between_dates(*d1, *d2)
    expected = (dt.date(d2[2], d2[1], d2[0]) - dt.date(d1[2], d1[1], d1[0])).days
    assert result["days_between"] == expected


def test_days_between_dates_is_symmetric():
    r1 = days_between_dates(1, 1, 2024, 1, 1, 2025)
    r2 = days_between_dates(1, 1, 2025, 1, 1, 2024)
    assert r1["days_between"] == r2["days_between"]


def test_julian_day_number_is_monotonic():
    jdn1 = to_julian_day_number(1, 1, 2024)
    jdn2 = to_julian_day_number(2, 1, 2024)
    assert jdn2 == jdn1 + 1


def test_shift_day_forward_and_back():
    forward = shift_day(1, 1, 2024, 45)
    assert forward["result_date"] == "15-02-2024"
    back = shift_day(15, 2, 2024, -45)
    assert back["result_date"] == "01-01-2024"


def test_shift_day_matches_python_datetime():
    base = dt.date(2024, 1, 1)
    expected = base + dt.timedelta(days=100)
    result = shift_day(1, 1, 2024, 100)
    assert result["result_date"] == expected.strftime("%d-%m-%Y")
