"""
Core algorithmic logic for Clock Angle problems.

This is the CORE LOGIC LAYER: every function here returns a verified
numerical answer with zero dependency on the AI layer. The AI layer only
ever receives the dictionaries produced here -- it never recomputes them.

Formula:
    Angle between the hour hand and minute hand at H hours, M minutes:
        raw_angle = |30*H - 5.5*M|
    The reported "angle" is normalised to the smaller of raw_angle and
    (360 - raw_angle), since a clock angle is conventionally reported as
    the value <= 180 degrees.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ClockResult:
    hour: int
    minute: int
    formula: str
    substitution: str
    raw_angle: float
    angle: float
    reflex_angle: float
    steps: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "hour": self.hour,
            "minute": self.minute,
            "formula": self.formula,
            "substitution": self.substitution,
            "raw_angle": self.raw_angle,
            "angle": self.angle,
            "reflex_angle": self.reflex_angle,
            "steps": self.steps,
        }


def calculate_clock_angle(hour: int, minute: int) -> ClockResult:
    """Calculate the angle between the hour and minute hands.

    Args:
        hour: 1-12 (12-hour format; 0 is treated as 12).
        minute: 0-59.

    Returns:
        ClockResult with the full worked solution.

    Raises:
        ValueError: if hour/minute are outside valid ranges.
    """
    if not (0 <= hour <= 12):
        raise ValueError("Hour must be between 0 and 12.")
    if not (0 <= minute <= 59):
        raise ValueError("Minute must be between 0 and 59.")

    h = 0 if hour == 12 else hour  # 12 behaves like 0 in the formula
    raw_angle = abs(30 * h - 5.5 * minute)
    smaller = min(raw_angle, 360 - raw_angle)
    reflex = 360 - smaller

    steps = [
        f"Step 1: Hour hand moves 30° per hour, minute hand moves 5.5° per minute.",
        f"Step 2: Apply formula  Angle = |30H - 5.5M|",
        f"Step 3: Substitute H = {h}, M = {minute}  ->  |30×{h} - 5.5×{minute}| "
        f"= |{30*h:.1f} - {5.5*minute:.1f}| = {raw_angle:.1f}°",
        f"Step 4: If the result is greater than 180°, subtract it from 360° "
        f"to get the smaller angle.",
        f"Step 5: Final smaller angle = {smaller:.1f}°  "
        f"(reflex angle = {reflex:.1f}°)",
    ]

    return ClockResult(
        hour=hour,
        minute=minute,
        formula="Angle = |30H - 5.5M|",
        substitution=f"|30×{h} - 5.5×{minute}|",
        raw_angle=round(raw_angle, 2),
        angle=round(smaller, 2),
        reflex_angle=round(reflex, 2),
        steps=steps,
    )


def find_times_for_angle(hour: int, angle: float) -> list[float]:
    """Find the minute value(s) within the given hour where the hands form
    the requested angle (0-180 degrees).

    Solves  |30H - 5.5M| (mod 360, folded to <=180) = angle  for M in [0, 60).

    Returns a sorted list of valid minute values (may contain 0, 1 or 2
    solutions within a single hour).
    """
    if not (0 <= hour <= 12):
        raise ValueError("Hour must be between 0 and 12.")
    if not (0 <= angle <= 180):
        raise ValueError("Angle must be between 0 and 180 degrees.")

    h = 0 if hour == 12 else hour
    base = 30 * h
    solutions: list[float] = []

    # 30H - 5.5M = angle + 360k   OR   30H - 5.5M = -angle + 360k
    for target in (angle, -angle):
        for k in (-1, 0, 1):
            m = (base - target - 360 * k) / 5.5
            if -1e-9 <= m < 60:
                m = max(0.0, round(m, 2))
                if not any(abs(m - existing) < 1e-6 for existing in solutions):
                    solutions.append(m)

    return sorted(solutions)


def sample_clock_questions() -> list[dict]:
    """A handful of representative competitive-exam style questions."""
    return [
        {"question": "Find the angle between the hands of a clock at 3:20.", "hour": 3, "minute": 20},
        {"question": "Find the angle between the hands of a clock at 6:00.", "hour": 6, "minute": 0},
        {"question": "Find the angle between the hands of a clock at 4:40.", "hour": 4, "minute": 40},
        {"question": "Find the angle between the hands of a clock at 9:15.", "hour": 9, "minute": 15},
        {"question": "Find the angle between the hands of a clock at 12:45.", "hour": 12, "minute": 45},
    ]


# ---------------------------------------------------------------------------
# Concept helpers (used by the Concepts Library and its self-tests)
# ---------------------------------------------------------------------------
def hands_overlap_time(hour: int) -> float:
    """Minutes past `hour` at which the two hands coincide: M = 60H / 11."""
    if not (0 <= hour <= 12):
        raise ValueError("Hour must be between 0 and 12.")
    return 60 * (0 if hour == 12 else hour) / 11


def hands_opposite_time(hour: int) -> float:
    """Minutes past `hour` at which the hands are 180 degrees apart.

    M = (60H + 360) / 11 when H < 6, and (60H - 360) / 11 when H >= 6.
    """
    if not (0 <= hour <= 12):
        raise ValueError("Hour must be between 0 and 12.")
    h = 0 if hour == 12 else hour
    return (60 * h + 360) / 11 if h < 6 else (60 * h - 360) / 11


def mirror_image_time(hour: int, minute: int) -> tuple[int, int]:
    """Time seen in a plane mirror held to the clock: 11:60 - T (12-hour clock)."""
    total = (11 * 60 + 60) - ((hour % 12) * 60 + minute)  # minutes, 0..720
    total %= 720
    h, m = divmod(total, 60)
    return (12 if h == 0 else h), m


def water_image_time(hour: int, minute: int) -> tuple[int, int]:
    """Time seen when the clock is reflected top-to-bottom: 5:60 - T (mod 12 h)."""
    total = (5 * 60 + 60) - ((hour % 12) * 60 + minute)
    total %= 720
    h, m = divmod(total, 60)
    return (12 if h == 0 else h), m


def clock_gain_loss_in_24h(coincidence_interval_min: float) -> float:
    """Gain (+) / loss (-) in minutes over 24 h of true time when the hands of
    a faulty clock coincide every `coincidence_interval_min` true minutes.

    gain = 1440 * (720/11 - m) / m
    """
    m = coincidence_interval_min
    if m <= 0:
        raise ValueError("Interval must be positive.")
    return 1440 * (720 / 11 - m) / m
