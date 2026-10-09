"""
Core algorithmic logic for Calendar problems: leap years, day-of-week
(Zeller's Congruence), and date differences (Julian Day Number method).

`datetime` is used ONLY to validate that a date actually exists on the
calendar (see validators.validate_date). The actual day-of-week and
date-difference calculations are implemented algorithmically here so the
underlying mathematics is visible and demonstrable, exactly as required.
"""

from __future__ import annotations

from dataclasses import dataclass

_WEEKDAY_NAMES = [
    "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
]  # index matches Zeller's raw output (0 = Saturday)


def is_leap_year(year: int) -> dict:
    """Determine whether `year` is a leap year using the standard rule."""
    if year % 400 == 0:
        result, reason = True, f"{year} is divisible by 400 -> leap year."
    elif year % 100 == 0:
        result, reason = False, f"{year} is divisible by 100 but not 400 -> not a leap year."
    elif year % 4 == 0:
        result, reason = True, f"{year} is divisible by 4 (not by 100) -> leap year."
    else:
        result, reason = False, f"{year} is not divisible by 4 -> not a leap year."
    return {"year": year, "is_leap": result, "reason": reason}


def calculate_day_of_week(day: int, month: int, year: int) -> dict:
    """Calculate the day of the week using Zeller's Congruence.

    Formula (Gregorian calendar):
        h = (q + floor(13(m+1)/5) + K + floor(K/4) + floor(J/4) - 2J) mod 7
    where:
        q = day of month
        m = month (3 = March, 4 = April, ..., 14 = February)
          (January and February are counted as months 13 and 14 of the
           PREVIOUS year)
        K = year of the century (year mod 100)
        J = zero-based century (year // 100)
        h : 0 = Saturday, 1 = Sunday, 2 = Monday, ... 6 = Friday
    """
    q = day
    m = month
    y = year
    if month < 3:
        m = month + 12
        y = year - 1

    K = y % 100
    J = y // 100

    h = (q + (13 * (m + 1)) // 5 + K + K // 4 + J // 4 - 2 * J) % 7
    weekday_name = _WEEKDAY_NAMES[h]

    steps = [
        "Step 1: Apply Zeller's Congruence:",
        "        h = (q + floor(13(m+1)/5) + K + floor(K/4) + floor(J/4) - 2J) mod 7",
        f"Step 2: January/February are treated as months 13/14 of the previous year."
        f" Adjusted month m = {m}, adjusted year y = {y}.",
        f"Step 3: q (day) = {q}, K (year of century) = {K}, J (century) = {J}",
        f"Step 4: h = ({q} + {(13*(m+1))//5} + {K} + {K//4} + {J//4} - {2*J}) mod 7 = {h}",
        f"Step 5: h = {h}  ->  {weekday_name}  (0=Saturday, 1=Sunday, ... 6=Friday)",
    ]

    return {
        "day": day, "month": month, "year": year,
        "formula": "h = (q + floor(13(m+1)/5) + K + floor(K/4) + floor(J/4) - 2J) mod 7",
        "weekday": weekday_name,
        "h_value": h,
        "steps": steps,
    }


def to_julian_day_number(day: int, month: int, year: int) -> int:
    """Convert a Gregorian calendar date to a Julian Day Number (JDN).

    Standard algorithmic conversion (Fliegel & Van Flandern formula), used
    here so date differences can be computed by pure integer arithmetic
    rather than by delegating everything to a library.
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn


def days_between_dates(day1: int, month1: int, year1: int,
                        day2: int, month2: int, year2: int) -> dict:
    """Calculate the number of days between two dates using JDN subtraction."""
    jdn1 = to_julian_day_number(day1, month1, year1)
    jdn2 = to_julian_day_number(day2, month2, year2)
    difference = abs(jdn2 - jdn1)

    steps = [
        "Step 1: Convert both dates to a Julian Day Number (JDN), a continuous "
        "day count that lets us subtract dates directly.",
        f"Step 2: JDN({day1:02d}-{month1:02d}-{year1}) = {jdn1}",
        f"Step 3: JDN({day2:02d}-{month2:02d}-{year2}) = {jdn2}",
        f"Step 4: Difference = |{jdn2} - {jdn1}| = {difference} days",
    ]

    return {
        "date1": f"{day1:02d}-{month1:02d}-{year1}",
        "date2": f"{day2:02d}-{month2:02d}-{year2}",
        "jdn1": jdn1, "jdn2": jdn2,
        "days_between": difference,
        "steps": steps,
    }


def shift_day(day: int, month: int, year: int, offset: int) -> dict:
    """Find the date `offset` days before/after the given date (offset can be
    negative). Implemented via JDN arithmetic + conversion back to a
    calendar date so the algorithm stays fully self-contained.
    """
    jdn = to_julian_day_number(day, month, year) + offset
    # Convert JDN back to Gregorian date (standard inverse algorithm).
    j = jdn + 32044
    g = j // 146097
    dg = j % 146097
    c = (dg // 36524 + 1) * 3 // 4
    dc = dg - c * 36524
    b = dc // 1461
    db = dc % 1461
    a = (db // 365 + 1) * 3 // 4
    da = db - a * 365
    y = g * 400 + c * 100 + b * 4 + a
    m = (da * 5 + 308) // 153 - 2
    d = da - (m + 4) * 153 // 5 + 122
    year_out = y - 4800 + (m + 2) // 12
    month_out = (m + 2) % 12 + 1
    day_out = d + 1

    direction = "after" if offset >= 0 else "before"
    return {
        "original_date": f"{day:02d}-{month:02d}-{year}",
        "offset": offset,
        "result_date": f"{day_out:02d}-{month_out:02d}-{year_out}",
        "explanation": f"{abs(offset)} day(s) {direction} {day:02d}-{month:02d}-{year} "
                        f"is {day_out:02d}-{month_out:02d}-{year_out}.",
    }


# ---------------------------------------------------------------------------
# Concept helpers (used by the Concepts Library and its self-tests)
# ---------------------------------------------------------------------------
_SUN_FIRST = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def leap_years_up_to(year: int) -> int:
    """Number of leap years in 1..year (Gregorian): y//4 - y//100 + y//400."""
    return year // 4 - year // 100 + year // 400


def count_leap_years(start_year: int, end_year: int) -> int:
    """Leap years in the inclusive range [start_year, end_year]."""
    return leap_years_up_to(end_year) - leap_years_up_to(start_year - 1)


def century_odd_days(completed_years: int) -> int:
    """Odd days contributed by `completed_years` (a multiple of 100).

    100 yrs -> 5, 200 -> 3, 300 -> 1, 400 -> 0, then the cycle repeats.
    """
    if completed_years % 100 != 0:
        raise ValueError("completed_years must be a multiple of 100.")
    return {1: 5, 2: 3, 3: 1, 0: 0}[(completed_years // 100) % 4]


def odd_days_weekday(day: int, month: int, year: int) -> dict:
    """Day of week via the classical 'odd days' method (0 = Sunday ... 6 = Saturday)."""
    prior = year - 1                      # complete years before this one
    centuries = (prior // 100) * 100
    rest = prior - centuries              # leftover complete years
    c_odd = century_odd_days(centuries)
    leaps = count_leap_years(centuries + 1, prior)
    y_odd = (rest + leaps) % 7
    feb = 29 if is_leap_year(year)["is_leap"] else 28
    days = sum(_MONTH_DAYS[:month - 1]) + (1 if month > 2 and feb == 29 else 0) + day
    d_odd = days % 7
    total = (c_odd + y_odd + d_odd) % 7
    return {"centuries_odd": c_odd, "years_odd": y_odd, "days_odd": d_odd,
            "total": total, "weekday": _SUN_FIRST[total]}


_DOOMSDAY_ANCHOR = {0: 2, 1: 0, 2: 5, 3: 3}  # century % 4 -> anchor (Sun=0): 1600=Tue, 1700=Sun, 1800=Fri, 1900=Wed


def doomsday_weekday(day: int, month: int, year: int) -> dict:
    """Conway's Doomsday rule. Returns the year's doomsday and the weekday of the date."""
    c, yy = divmod(year, 100)
    anchor = _DOOMSDAY_ANCHOR[c % 4]
    doomsday = (yy // 12 + yy % 12 + (yy % 12) // 4 + anchor) % 7
    leap = is_leap_year(year)["is_leap"]
    ref = {1: 4 if leap else 3, 2: 29 if leap else 28, 3: 14, 4: 4, 5: 9, 6: 6,
           7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12}[month]
    weekday = (doomsday + day - ref) % 7
    return {"anchor": anchor, "doomsday": doomsday, "doomsday_name": _SUN_FIRST[doomsday],
            "reference_date": ref, "weekday": _SUN_FIRST[weekday]}


def next_repeating_year(year: int) -> int:
    """Next year whose calendar is identical to `year`'s (same leap status and start day)."""
    leap = is_leap_year(year)["is_leap"]
    odd = 0
    y = year
    while True:
        odd = (odd + (2 if is_leap_year(y)["is_leap"] else 1)) % 7
        y += 1
        if odd == 0 and is_leap_year(y)["is_leap"] == leap:
            return y


def month_start_groups(leap: bool) -> list[list[str]]:
    """Groups of months that begin on the same weekday in a given kind of year."""
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days = list(_MONTH_DAYS)
    if leap:
        days[1] = 29
    offsets: dict[int, list[str]] = {}
    total = 0
    for n, d in zip(names, days):
        offsets.setdefault(total % 7, []).append(n)
        total += d
    return list(offsets.values())
