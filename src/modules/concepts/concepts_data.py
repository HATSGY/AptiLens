"""
Content for the Concepts Library: every Clock and Calendar concept, with
formulas, worked examples and exam tips.

This file is pure data (no GUI code) so the content can be unit-tested --
see tests/test_concepts.py, which re-computes the key numbers in the worked
examples using the verified logic layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Example:
    problem: str
    steps: list[str]
    answer: str


@dataclass(frozen=True)
class Topic:
    key: str
    title: str
    summary: str
    points: list[str]
    formulas: list[tuple[str, str]]          # (label, expression)
    examples: list[Example]
    tip: str = ""
    solver: str | None = None                # page name of the matching solver
    table: list[list[str]] | None = None     # optional table: first row = header
    table_title: str = ""
    keywords: str = ""                       # extra search terms


# ===========================================================================
# CLOCK
# ===========================================================================
CLOCK_TOPICS: list[Topic] = [
    Topic(
        key="clock_basics",
        title="Clock Basics & Hand Speeds",
        summary="The dial is a 360° circle split into 12 hour marks and 60 minute spaces. "
                "Everything in clock problems starts from how fast each hand moves.",
        points=[
            "Full dial = 360° = 12 hour marks = 60 minute spaces.",
            "1 hour mark = 360° ÷ 12 = 30°.   1 minute space = 360° ÷ 60 = 6°.   1 hour mark = 5 minute spaces.",
            "Minute hand: one full turn (360°) in 60 min  →  6° per minute.",
            "Hour hand: one full turn in 12 h  →  30° per hour  →  0.5° per minute.",
            "Second hand: 6° per second (360° per minute).",
            "Speed ratio  hour : minute : second  =  1 : 12 : 720.",
            "In 12 h the hour hand turns 1 time, the minute hand 12 times. In 24 h: 2 and 24 turns.",
            "The minute hand gains 5.5° (= 55 minute spaces per hour) on the hour hand.",
        ],
        formulas=[
            ("Minute-hand angle from 12", "6 × M   degrees"),
            ("Hour-hand angle from 12", "30 × H + 0.5 × M   degrees"),
            ("Relative speed of minute hand", "6 − 0.5 = 5.5   degrees per minute"),
        ],
        examples=[
            Example("Where are the hands at 7:30 (measured clockwise from 12)?",
                    ["Hour hand = 30×7 + 0.5×30 = 210 + 15 = 225°",
                     "Minute hand = 6×30 = 180°"],
                    "Hour hand 225°, minute hand 180°"),
            Example("How far does each hand turn in 45 minutes?",
                    ["Minute hand: 6° × 45 = 270°",
                     "Hour hand: 0.5° × 45 = 22.5°"],
                    "Minute hand 270°, hour hand 22.5°"),
        ],
        tip="Memorise 6° (minute hand) and 0.5° (hour hand) per minute — every other clock formula is built from them.",
        solver="clock", keywords="speed degrees revolution second hand",
    ),
    Topic(
        key="clock_angle",
        title="Angle Between the Hands",
        summary="Find the angle between the hour and minute hands at any given time H:M.",
        points=[
            "Derivation: Angle = |hour-hand angle − minute-hand angle| = |(30H + 0.5M) − 6M| = |30H − 5.5M|.",
            "Use H on a 12-hour scale (treat 12 as 0).",
            "If the result is more than 180°, the angle between the hands is 360° − result (the smaller angle).",
            "The larger angle (reflex angle) = 360° − smaller angle.",
            "At an exact hour (M = 0) the angle is simply 30 × H (or 360 − 30H when that exceeds 180°).",
        ],
        formulas=[
            ("Angle between hands", "θ = |30H − 5.5M|"),
            ("Smaller angle", "if θ > 180°  then  θ = 360° − θ"),
            ("Reflex angle", "360° − (smaller angle)"),
        ],
        examples=[
            Example("Find the angle between the hands at 3:20.",
                    ["θ = |30×3 − 5.5×20| = |90 − 110| = 20°"], "20°"),
            Example("Find the angle between the hands at 4:40.",
                    ["θ = |30×4 − 5.5×40| = |120 − 220| = 100°"], "100°"),
            Example("Find the smaller and reflex angles at 9:15.",
                    ["θ = |30×9 − 5.5×15| = |270 − 82.5| = 187.5°",
                     "187.5° > 180°, so smaller angle = 360° − 187.5° = 172.5°",
                     "Reflex angle = 187.5°"],
                    "Smaller 172.5°, reflex 187.5°"),
        ],
        tip="Do the subtraction first, then fold into 0°–180°. Never forget to treat 12 as 0.",
        solver="clock", keywords="angle formula 30H 5.5M reflex",
    ),
    Topic(
        key="clock_time_for_angle",
        title="Time When the Hands Make a Given Angle",
        summary="Reverse problem: at what time between H and H+1 do the hands make an angle θ?",
        points=[
            "Set |30H − 5.5M| = θ. Two cases:  30H − 5.5M = +θ  or  30H − 5.5M = −θ.",
            "Solving for M gives two candidate times in each hour.",
            "Accept only answers with 0 ≤ M < 60 — sometimes only one is valid.",
            "Fractions are normal: divide by 11 and write the answer as a mixed fraction.",
        ],
        formulas=[
            ("Minutes past H", "M = (30H ± θ) / 5.5  =  (60H ± 2θ) / 11"),
            ("Valid range", "0 ≤ M < 60"),
        ],
        examples=[
            Example("At what times between 5 and 6 are the hands 60° apart?",
                    ["M = (60×5 − 2×60)/11 = 180/11 = 16 4/11",
                     "M = (60×5 + 2×60)/11 = 420/11 = 38 2/11",
                     "Both lie between 0 and 60, so both are valid."],
                    "5:16 4/11 and 5:38 2/11"),
            Example("At what times between 2 and 3 are the hands 30° apart?",
                    ["M = (120 − 60)/11 = 60/11 = 5 5/11",
                     "M = (120 + 60)/11 = 180/11 = 16 4/11"],
                    "2:05 5/11 and 2:16 4/11"),
        ],
        tip="If a question says 'exactly 3 minutes apart in time', convert to angle first: 1 minute space = 6°.",
        solver="clock", keywords="reverse find time angle",
    ),
    Topic(
        key="clock_overlap",
        title="Overlapping Hands (0°)",
        summary="When do the hour and minute hands lie exactly on top of each other?",
        points=[
            "The hands coincide 11 times in 12 hours and 22 times in 24 hours.",
            "Between 11 and 1 they coincide only once — at exactly 12:00.",
            "Time between two successive overlaps = 12 h ÷ 11 = 720/11 = 65 5/11 minutes.",
            "Why 60H/11?  At H:00 the hour hand is 5H spaces ahead; the minute hand gains 55 spaces per hour, "
            "so it needs 5H ÷ 55 hours = 5H × 60/55 minutes = 60H/11.",
        ],
        formulas=[
            ("Minutes past H when hands overlap", "M = 60H / 11"),
            ("Gap between overlaps", "720 / 11 = 65 5/11 minutes"),
        ],
        examples=[
            Example("At what time between 4 and 5 do the hands coincide?",
                    ["M = 60×4 / 11 = 240/11 = 21 9/11"], "4:21 9/11"),
            Example("Hands of a correct clock coincide after how many minutes?",
                    ["Interval = 720/11 = 65 5/11 minutes"], "65 5/11 minutes"),
        ],
        tip="Overlap times are exactly H × 5 5/11 minutes past H — add 5 5/11 each hour.",
        table_title="The 11 overlap times in 12 hours",
        table=[["Between", "Time", "Between", "Time"],
               ["12 and 1", "12:00", "6 and 7", "6:32 8/11"],
               ["1 and 2", "1:05 5/11", "7 and 8", "7:38 2/11"],
               ["2 and 3", "2:10 10/11", "8 and 9", "8:43 7/11"],
               ["3 and 4", "3:16 4/11", "9 and 10", "9:49 1/11"],
               ["4 and 5", "4:21 9/11", "10 and 11", "10:54 6/11"],
               ["5 and 6", "5:27 3/11", "11 and 12", "none (next is 12:00)"]],
        solver="clock", keywords="coincide together same position",
    ),
    Topic(
        key="clock_opposite_right",
        title="Opposite Hands (180°) & Right Angles (90°)",
        summary="Special angles that appear in almost every exam: straight line (180°) and perpendicular (90°).",
        points=[
            "Opposite hands: 11 times in 12 hours (22 in a day).",
            "Right angle: 22 times in 12 hours (44 in a day).",
            "Overlapping + opposite together ('hands in a straight line'): 22 times in 12 hours.",
            "Opposite uses θ = 180° in the general formula; right angle uses θ = 90°.",
            "Opposite time formula: for H = 0–5 add 360, for H = 6–11 subtract 360.",
        ],
        formulas=[
            ("Hands opposite", "M = (60H + 360)/11  (H < 6)   or   (60H − 360)/11  (H ≥ 6)"),
            ("Hands at right angle", "M = (60H ± 180) / 11     (keep 0 ≤ M < 60)"),
        ],
        examples=[
            Example("At what time between 4 and 5 are the hands opposite?",
                    ["M = (60×4 + 360)/11 = 600/11 = 54 6/11"], "4:54 6/11"),
            Example("At what time between 8 and 9 are the hands opposite?",
                    ["H = 8 ≥ 6, so M = (60×8 − 360)/11 = 120/11 = 10 10/11"], "8:10 10/11"),
            Example("At what times between 3 and 4 are the hands at right angles?",
                    ["M = (180 − 180)/11 = 0   →  3:00",
                     "M = (180 + 180)/11 = 360/11 = 32 8/11   →  3:32 8/11"],
                    "3:00 and 3:32 8/11"),
        ],
        tip="Right angles come in pairs each hour (once as hour-hand-leads, once as minute-hand-leads), except at the very edges.",
        solver="clock", keywords="straight line perpendicular 90 180 opposite",
    ),
    Topic(
        key="clock_minute_space",
        title="Minute-Space Shortcut",
        summary="Skip algebra: count how many minute spaces the minute hand must gain, then multiply by 12/11.",
        points=[
            "Measure everything in minute spaces (1 space = 6°). The dial has 60 spaces.",
            "At H:00 the hour hand is 5H spaces ahead of the minute hand (which sits at 12).",
            "The minute hand gains 55 spaces in 60 minutes, i.e. 1 space every 12/11 minutes.",
            "Gain needed = 5H  (overlap);   5H + 30 (if H < 6) or 5H − 30 (if H ≥ 6)  (opposite);   5H ± 15  (right angle).",
            "For a general angle θ: gain = 5H ± (θ ÷ 6).",
        ],
        formulas=[
            ("Time taken", "minutes = (spaces to gain) × 12 / 11"),
            ("Spaces gained", "5H  ±  (required gap in spaces)"),
        ],
        examples=[
            Example("When do the hands overlap between 8 and 9?",
                    ["Spaces to gain = 5×8 = 40", "Time = 40 × 12/11 = 480/11 = 43 7/11"], "8:43 7/11"),
            Example("At what time after 3:00 do the hands next form a right angle?",
                    ["At 3:00 the hour hand leads by 15 spaces. Minute hand must lead by 15: gain = 15 + 15 = 30",
                     "Time = 30 × 12/11 = 360/11 = 32 8/11"], "3:32 8/11"),
        ],
        tip="This method is the fastest in the exam hall — no formula to recall, just 'spaces × 12/11'.",
        solver="clock", keywords="minute spaces gain 55 shortcut",
    ),
    Topic(
        key="clock_frequency",
        title="How Often Do the Hands Align?",
        summary="Counting questions: how many times in 12 hours / a day do the hands overlap, oppose or cross at an angle?",
        points=[
            "Why 22?  In 12 hours the minute hand laps the hour hand 11 times; it passes any given angle once "
            "per lap on each side — so 22 times. For 0° and 180° the two sides merge, giving 11.",
            "Counting between two clock times (e.g. 2:00 to 8:00): count the events that fall inside the window, "
            "using the lists of exact times.",
        ],
        formulas=[
            ("Events per 12 h", "11 (for 0° or 180°),   22 (for any other angle)"),
            ("Events per 24 h", "22 (for 0° or 180°),   44 (for any other angle)"),
        ],
        examples=[
            Example("How many times in a day do the hands overlap?", ["11 × 2 = 22"], "22 times"),
            Example("How many times in a day are the hands at right angles?", ["22 × 2 = 44"], "44 times"),
        ],
        tip="Remember: 11 for 0° and 180°, 22 for everything else (per 12 hours).",
        table_title="Frequency of hand positions",
        table=[["Event", "In 12 hours", "In 24 hours"],
               ["Hands overlap (0°)", "11", "22"],
               ["Hands opposite (180°)", "11", "22"],
               ["Right angle (90°)", "22", "44"],
               ["Any other angle θ", "22", "44"]],
        solver="clock", keywords="count times per day frequency",
    ),
    Topic(
        key="clock_mirror_water",
        title="Mirror Image & Water Image",
        summary="What time does a clock appear to show in a mirror, or when turned upside down?",
        points=[
            "Mirror image (reflected left–right, as in a plane mirror): subtract the time from 11:60.",
            "Water image (reflected top–bottom, as in still water below the clock): subtract the time from 5:60.",
            "Work in a 12-hour clock. If the result is zero or negative, add 12 hours; an hour of 0 is shown as 12.",
            "A time and its mirror image always sum to 12:00.",
            "Why the mirror rule works: a plane mirror turns every hand angle θ into 360° − θ, which is again a valid time, namely 11:60 − T.",
            "Why the water rule works: the water image is the mirror image turned upside-down (a 180° turn = 6 hours): (11:60 − T) − 6:00 = 5:60 − T. "
            "This is the standard exam convention.",
        ],
        formulas=[
            ("Mirror image of T", "11:60 − T"),
            ("Water image of T", "5:60 − T      (add 12:00 if negative)"),
        ],
        examples=[
            Example("Mirror image of 4:25?", ["11:60 − 4:25 = 7:35"], "7:35"),
            Example("Mirror image of 10:10?", ["11:60 − 10:10 = 1:50"], "1:50"),
            Example("Water image of 4:25?", ["5:60 − 4:25 = 1:35"], "1:35"),
            Example("Water image of 8:00?", ["5:60 − 8:00 = −2:00",
                                             "Negative, so add 12 h: −2:00 + 12:00 = 10:00"], "10:00"),
        ],
        tip="For a time exactly on 6:00 or 12:00 the image looks identical in a mirror.",
        solver=None, keywords="reflection flip upside down",
    ),
    Topic(
        key="clock_fast_slow",
        title="Fast & Slow Clocks (Gain / Loss)",
        summary="A faulty clock gains or loses a fixed amount per hour. Find the time it shows, or the true time.",
        points=[
            "If a clock gains g minutes per hour, it shows 60 + g minutes for every 60 minutes of true time.",
            "If it loses l minutes per hour, it shows 60 − l minutes for every 60 true minutes.",
            "Set the clock right at a known time, then work with the elapsed time since.",
            "Faulty-clock puzzle: if the hands of a clock coincide every m minutes of true time, then in 24 hours the clock "
            "gains (m < 720/11) or loses (m > 720/11).",
        ],
        formulas=[
            ("Time shown (gaining clock)", "shown elapsed = true elapsed × (60 + g) / 60"),
            ("True time (gaining clock)", "true elapsed = shown elapsed × 60 / (60 + g)"),
            ("Time shown (losing clock)", "shown elapsed = true elapsed × (60 − l) / 60"),
            ("True time (losing clock)", "true elapsed = shown elapsed × 60 / (60 − l)"),
            ("Gain / loss in 24 h from coincidence gap m", "1440 × (720/11 − m) / m   (negative = loss)"),
        ],
        examples=[
            Example("A clock gains 5 min per hour and is set right at 8:00 AM. What does it show at true 2:00 PM?",
                    ["True elapsed = 6 h, so gain = 6 × 5 = 30 min", "Shown = 2:00 PM + 30 min"], "2:30 PM"),
            Example("A watch loses 4 min per hour and was correct at 6:00 AM. It now shows 1:00 PM. What is the true time?",
                    ["Shown elapsed = 7 h = 420 min", "True elapsed = 420 × 60/56 = 450 min = 7 h 30 min",
                     "True time = 6:00 AM + 7 h 30 min"], "1:30 PM"),
            Example("The hands of a clock coincide every 66 minutes of correct time. How much does it gain or lose in 24 h?",
                    ["Correct gap = 720/11 = 65 5/11 min, which is less than 66",
                     "Change = 1440 × (720/11 − 66) / 66 = 1440 × (−6/11) / 66 = −11 109/121 min"],
                    "Loses 11 109/121 min (≈ 11 min 54 s)"),
        ],
        tip="Always convert 'loses l min per hour' to a ratio 60 : (60 − l) between shown and true time.",
        solver=None, keywords="gain loss faulty watch slow fast correct",
    ),
    Topic(
        key="clock_strikes",
        title="Clock Striking & Chimes",
        summary="Strikes take time, but the gaps between them are what matter.",
        points=[
            "n strikes have (n − 1) equal intervals between them (the strike itself is taken as instantaneous).",
            "Interval = total time ÷ (n − 1).   Time for N strikes = (N − 1) × interval.",
            "A clock that strikes the hour number of times plus once every half hour makes 2×(1+2+…+12) + 24 = 180 strikes in 24 hours.",
            "Sum of hour strikes in 12 hours = 12×13/2 = 78.",
        ],
        formulas=[
            ("Interval between strikes", "t / (n − 1)"),
            ("Time to strike N times", "(N − 1) × t / (n − 1)"),
            ("Total hour strikes in 12 h", "N(N + 1)/2 = 78   (N = 12)"),
        ],
        examples=[
            Example("A clock takes 5 seconds to strike 6. How long to strike 11?",
                    ["Interval = 5/(6 − 1) = 1 s", "Time for 11 strikes = (11 − 1) × 1 = 10 s"], "10 seconds"),
            Example("A clock takes 6 seconds to strike 4. How long to strike 10?",
                    ["Interval = 6/3 = 2 s", "Time for 10 strikes = 9 × 2 = 18 s"], "18 seconds"),
        ],
        tip="Fence-post rule: n strikes → n − 1 gaps. This one trap catches most students.",
        solver=None, keywords="chime bell strike interval gap",
    ),
    Topic(
        key="clock_time_arith",
        title="Time Arithmetic & 24-Hour Clock",
        summary="Convert between 12- and 24-hour formats and compute elapsed time reliably.",
        points=[
            "1 day = 24 h = 1440 min = 86 400 s.   1 h = 60 min = 3600 s.",
            "24-hour to 12-hour: 13:00–23:59 → subtract 12 (PM);  00:xx → 12:xx AM;  12:xx → 12:xx PM.",
            "Elapsed time: convert both times to minutes since midnight and subtract. If the result is negative, add 1440.",
            "When adding times, carry 60 minutes into 1 hour and 24 hours into 1 day.",
        ],
        formulas=[
            ("Minutes since midnight", "total = 60 × H(24h) + M"),
            ("Elapsed time", "(end − start) mod 1440 minutes"),
        ],
        examples=[
            Example("How long from 9:45 PM to 6:20 AM the next morning?",
                    ["Start = 21×60 + 45 = 1305 min,  End = 6×60 + 20 = 380 min",
                     "380 − 1305 = −925  →  −925 + 1440 = 515 min"], "8 h 35 min"),
            Example("Convert 17:08 to 12-hour format.", ["17 − 12 = 5, afternoon"], "5:08 PM"),
        ],
        tip="For overnight spans, always add 24 h to the end time before subtracting.",
        solver=None, keywords="24 hour elapsed duration convert am pm",
    ),
    Topic(
        key="clock_cheat",
        title="Clock Cheat Sheet",
        summary="Every clock formula on one screen — revise this before an exam.",
        points=[
            "Dial: 360° = 12 hours = 60 minute spaces.   1 hour = 30°,  1 minute space = 6°.",
            "Minute hand 6°/min,  hour hand 0.5°/min,  relative speed 5.5°/min  (55 spaces/h).",
            "Counts per 12 h: overlap 11, opposite 11, right-angle 22, other angle 22.  Per day: double.",
            "Overlap gap = 65 5/11 min.  Overlap time after H = 60H/11.",
            "Opposite time after H = (60H ± 360)/11.   Right-angle time = (60H ± 180)/11.",
            "Mirror image = 11:60 − T.   Water image = 5:60 − T.",
            "n strikes → (n − 1) intervals.",
            "Gain/loss per hour g: shown = true × (60 + g)/60.",
        ],
        formulas=[
            ("Angle", "θ = |30H − 5.5M|   (take 360 − θ if > 180)"),
            ("Time for angle θ", "M = (60H ± 2θ)/11"),
            ("Minute-space shortcut", "minutes = spaces × 12/11"),
        ],
        examples=[
            Example("Quick check: angle at 6:00?", ["|30×6 − 0| = 180°"], "180° (hands opposite)"),
        ],
        tip="Practise each formula on 3 different times until the arithmetic feels automatic.",
        solver="clock", keywords="summary revision formulas",
    ),
]

# ===========================================================================
# CALENDAR
# ===========================================================================
CALENDAR_TOPICS: list[Topic] = [
    Topic(
        key="cal_basics",
        title="Calendar Basics & Odd Days",
        summary="Years, months, weeks — and the idea of 'odd days' that powers every calendar shortcut.",
        points=[
            "A week has 7 days. Everything repeats modulo 7.",
            "Ordinary year = 365 days = 52 weeks + 1 odd day.   Leap year = 366 days = 52 weeks + 2 odd days.",
            "31-day months: Jan, Mar, May, Jul, Aug, Oct, Dec.   30-day months: Apr, Jun, Sep, Nov.   February: 28 (29 in a leap year).",
            "Knuckle trick: on your fist, knuckles = 31-day months, valleys = 30/28-day months (Jul and Aug are both knuckles).",
            "Odd days = days left after removing complete weeks = (total days) mod 7.",
            "Month odd days:  31 days → 3,   30 days → 2,   February (28) → 0,   February (29) → 1.",
            "Quick conversions: 1 week = 7 d;  1 year = 365 d (366 leap);  1 decade = 3652 or 3653 d.",
        ],
        formulas=[
            ("Odd days", "(total days) mod 7"),
            ("Same date next year", "weekday + 1  (ordinary),   weekday + 2  (if Feb 29 lies in between)"),
        ],
        examples=[
            Example("1 Jan 2025 is a Wednesday. What day is 1 Jan 2026?",
                    ["2025 is an ordinary year = 1 odd day", "Wednesday + 1"], "Thursday"),
            Example("How many odd days are there in January + February + March of a leap year?",
                    ["31 → 3,  29 → 1,  31 → 3", "3 + 1 + 3 = 7  →  7 mod 7 = 0"], "0 odd days"),
        ],
        tip="Always reduce to odd days (mod 7) at every step — keeps numbers tiny.",
        solver="calendar", keywords="week month days odd knuckle",
    ),
    Topic(
        key="cal_leap",
        title="Leap Years",
        summary="Which years have 366 days, and how many leap years lie in a given range?",
        points=[
            "A year is a leap year if it is divisible by 4, except century years (ending in 00).",
            "Century years are leap years only if divisible by 400.",
            "So 1900 and 2100 are NOT leap years; 2000 and 2400 are.",
            "Leap years in 1..N (Gregorian):  floor(N/4) − floor(N/100) + floor(N/400).",
            "Leap years in a range [A, B] = L(B) − L(A − 1).",
            "A person born on 29 Feb has a 'real' birthday only every 4 years.",
        ],
        formulas=[
            ("Leap year test", "(Y mod 4 = 0 and Y mod 100 ≠ 0)  or  (Y mod 400 = 0)"),
            ("Leap years up to N", "L(N) = floor(N/4) − floor(N/100) + floor(N/400)"),
            ("Leap years from A to B", "L(B) − L(A − 1)"),
        ],
        examples=[
            Example("Is 2024 a leap year? 1900? 2000? 2100?",
                    ["2024: divisible by 4, not by 100 → leap",
                     "1900: divisible by 100 but not 400 → not leap",
                     "2000: divisible by 400 → leap", "2100: divisible by 100 but not 400 → not leap"],
                    "2024 yes, 1900 no, 2000 yes, 2100 no"),
            Example("How many leap years are there from 1901 to 2000?",
                    ["L(2000) = 500 − 20 + 5 = 485", "L(1900) = 475 − 19 + 4 = 460", "485 − 460 = 25"], "25"),
            Example("How many leap years are there from 2001 to 2100?",
                    ["L(2100) = 525 − 21 + 5 = 509", "L(2000) = 485", "509 − 485 = 24  (2100 is not a leap year)"], "24"),
        ],
        tip="Every 100-year block has 24 leap years, except one that contains a year divisible by 400 (25).",
        solver="calendar", keywords="leap year 29 february divisible 400",
    ),
    Topic(
        key="cal_odd_days_years",
        title="Odd Days in Years & Centuries",
        summary="How many odd days do N years or complete centuries contribute?",
        points=[
            "N years contribute  (N + number of leap years among them) mod 7  odd days.",
            "100 years (with no leap century year) = 76 ordinary + 24 leap = 76 + 48 = 124 odd-day units → 124 mod 7 = 5 odd days.",
            "200 years → 3 odd days.   300 years → 1 odd day.   400 years → 0 odd days  (then it repeats).",
            "Reason: 400 years have 97 leap years → 400×365 + 97 = 146 097 days = 20 871 weeks exactly.",
            "The 4th century of a 400-year cycle (e.g. 1901–2000) contains the leap year 2000, so it has 6 odd days; 5 + 5 + 5 + 6 = 21 → 0.",
            "Counted from a 400-year boundary, the last day (31 Dec) of the 100th, 200th, 300th, 400th year is Friday, Wednesday, Monday, Sunday.",
        ],
        formulas=[
            ("Odd days in N years", "(N + leap years in N) mod 7"),
            ("Century odd days", "100 → 5,   200 → 3,   300 → 1,   400 → 0"),
        ],
        examples=[
            Example("How many odd days are in the 30 years 1991–2020?",
                    ["Leap years = 1992, 96, 2000, 04, 08, 12, 16, 20 = 8", "30 + 8 = 38  →  38 mod 7 = 3"], "3 odd days"),
            Example("How many odd days are in 1600 years?",
                    ["1600 = 4 × 400  →  4 × 0 = 0"], "0 odd days"),
            Example("How many odd days are in 1900 years?",
                    ["1900 = 1600 + 300  →  0 + 1 = 1"], "1 odd day"),
        ],
        tip="Reduce the century count mod 4: 1900 years → 19 centuries → 19 mod 4 = 3 → the '300 years' row → 1 odd day.",
        table_title="Odd days in complete centuries",
        table=[["Completed years", "Odd days", "31 Dec falls on"],
               ["100", "5", "Friday"],
               ["200", "3", "Wednesday"],
               ["300", "1", "Monday"],
               ["400", "0", "Sunday"]],
        solver="calendar", keywords="century 100 200 300 400",
    ),
    Topic(
        key="cal_day_odd_days",
        title="Day of the Week — Odd Days Method",
        summary="The classical exam method: add odd days from centuries, years and months/dates.",
        points=[
            "Step 1: Count odd days in the COMPLETED centuries before the date.",
            "Step 2: Count odd days in the remaining COMPLETED years (years + leap years among them).",
            "Step 3: Count odd days from January 1 up to the date (add the Feb 29 day when applicable).",
            "Step 4: Add all three and take mod 7.   0 = Sunday, 1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday.",
            "'Completed' means before the year of the date; the year of the date itself is handled in step 3.",
        ],
        formulas=[
            ("Weekday", "(century odd days + year odd days + date odd days) mod 7"),
            ("Mapping", "0 Sun · 1 Mon · 2 Tue · 3 Wed · 4 Thu · 5 Fri · 6 Sat"),
        ],
        examples=[
            Example("What day was 15 August 1947 (India's independence)?",
                    ["Completed centuries: 1900 years → 1 odd day",
                     "Completed years: 46 (1901–1946) with 11 leap years → 46 + 11 = 57 → 1 odd day",
                     "Days in 1947 up to 15 Aug: 31+28+31+30+31+30+31 = 212, +15 = 227 → 227 mod 7 = 3",
                     "Total = 1 + 1 + 3 = 5"], "Friday"),
            Example("What day was 26 January 1950?",
                    ["Completed centuries: 1900 → 1",
                     "Completed years: 49 with 12 leap years → 61 mod 7 = 5",
                     "Days: 26 mod 7 = 5", "Total = 1 + 5 + 5 = 11 → 11 mod 7 = 4"], "Thursday"),
        ],
        tip="Write the 0–6 mapping at the top of your rough sheet before you start.",
        solver="calendar", keywords="weekday day of week method odd days",
    ),
    Topic(
        key="cal_zeller",
        title="Zeller's Congruence",
        summary="A single formula that returns the weekday of any Gregorian date. This is the algorithm used by the Calendar solver.",
        points=[
            "q = day of the month.",
            "m = month number with March = 3, April = 4, … December = 12, and January = 13, February = 14 (of the PREVIOUS year).",
            "K = year of the century (year mod 100), using the adjusted year for Jan/Feb.",
            "J = century (year ÷ 100, rounded down), using the adjusted year for Jan/Feb.",
            "Result h:  0 = Saturday, 1 = Sunday, 2 = Monday, 3 = Tuesday, 4 = Wednesday, 5 = Thursday, 6 = Friday.",
        ],
        formulas=[
            ("Zeller (Gregorian)", "h = (q + floor(13(m+1)/5) + K + floor(K/4) + floor(J/4) − 2J) mod 7"),
        ],
        examples=[
            Example("Find the weekday of 7 October 2026.",
                    ["q = 7, m = 10, year = 2026 → K = 26, J = 20",
                     "floor(13×11/5) = floor(28.6) = 28,  floor(K/4) = 6,  floor(J/4) = 5,  2J = 40",
                     "h = (7 + 28 + 26 + 6 + 5 − 40) mod 7 = 32 mod 7 = 4"], "h = 4  →  Wednesday"),
            Example("Find the weekday of 1 January 2000.",
                    ["January counts as month 13 of 1999 → m = 13, year = 1999 → K = 99, J = 19",
                     "floor(13×14/5) = 36,  floor(K/4) = 24,  floor(J/4) = 4,  2J = 38",
                     "h = (1 + 36 + 99 + 24 + 4 − 38) mod 7 = 126 mod 7 = 0"], "h = 0  →  Saturday"),
        ],
        tip="If h comes out negative in your calculation, add multiples of 7 until it is in 0–6.",
        solver="calendar", keywords="zeller formula congruence algorithm",
    ),
    Topic(
        key="cal_doomsday",
        title="Doomsday Rule (Mental Shortcut)",
        summary="John Conway's trick: every year has a 'doomsday' weekday shared by easy-to-remember dates.",
        points=[
            "Anchor weekday for the century:  1700s Sunday · 1800s Friday · 1900s Wednesday · 2000s Tuesday (2100s Sunday).",
            "Year's doomsday = (floor(yy/12) + yy mod 12 + floor((yy mod 12)/4) + anchor) mod 7, where yy = last two digits.",
            "Dates that always fall on the doomsday:  4/4, 6/6, 8/8, 10/10, 12/12;  5/9, 9/5;  7/11, 11/7;  3/14 (Pi Day).",
            "January: 3rd (ordinary year) or 4th (leap year).   February: 28th (ordinary) or 29th (leap).",
            "From the nearest doomsday date, count forward or back in steps of 7 to reach your target.",
        ],
        formulas=[
            ("Year's doomsday", "(floor(yy/12) + yy mod 12 + floor((yy mod 12)/4) + anchor) mod 7"),
            ("Target weekday", "doomsday + (date − nearest doomsday date)   (mod 7)"),
        ],
        examples=[
            Example("What weekday is 7 October 2026?",
                    ["Anchor for 2000s = Tuesday (2); yy = 26",
                     "floor(26/12) = 2, 26 mod 12 = 2, floor(2/4) = 0 → 2 + 2 + 0 + 2 = 6 → doomsday = Saturday",
                     "10/10 is a doomsday = Saturday, so 7 Oct is 3 days earlier",
                     "Saturday − 3 days"], "Wednesday"),
            Example("What weekday is 4 July 1976?",
                    ["Anchor for 1900s = Wednesday (3); yy = 76",
                     "floor(76/12) = 6, 76 mod 12 = 4, floor(4/4) = 1 → 6 + 4 + 1 + 3 = 14 → 0 = Sunday",
                     "Doomsday = Sunday. 7/11 is a doomsday, so 4 Jul is 7 days earlier → same weekday"], "Sunday"),
        ],
        tip="Sunday = 0 in this rule. Learn the doomsday dates as a rhyme — 4/4, 6/6, 8/8, 10/10, 12/12.",
        solver="calendar", keywords="conway mental shortcut anchor",
    ),
    Topic(
        key="cal_shift_days",
        title="Weekday After N Days",
        summary="Given today's weekday, find the weekday N days later or earlier.",
        points=[
            "Only N mod 7 matters — whole weeks bring you back to the same weekday.",
            "Add N mod 7 for the future, subtract it for the past.",
            "Same date next year moves forward by 1 weekday (2 if a Feb 29 lies in between).",
            "Same date 4 years later moves forward by 5 weekdays (4 + 1 leap day); the usual 28-year cycle returns to the same weekday inside a century.",
        ],
        formulas=[
            ("Weekday after N days", "(today + N) mod 7"),
            ("Weekday before N days", "(today − N) mod 7"),
        ],
        examples=[
            Example("Today (7 Oct 2026) is Wednesday. What day will it be after 100 days?",
                    ["100 mod 7 = 2", "Wednesday + 2"], "Friday"),
            Example("7 Oct 2026 is a Wednesday. What day is 7 Oct 2027? And 7 Oct 2028?",
                    ["2027: no Feb 29 between → +1 → Thursday",
                     "2028: Feb 29, 2028 lies between → +2 more → Saturday"], "Thursday, then Saturday"),
        ],
        tip="'After N days' → reduce N mod 7 immediately.  100 days = 14 weeks + 2 days.",
        solver="calendar", keywords="after days later earlier add subtract",
    ),
    Topic(
        key="cal_between",
        title="Counting Days Between Dates",
        summary="Number of days between two dates by hand and by the Julian Day Number (JDN) method.",
        points=[
            "By hand: (days left in the first month) + (full months in between) + (days elapsed in the last month).",
            "Exclusive counting: do not include both end dates.  Inclusive counting: add 1.",
            "By algorithm: convert both dates to a JDN — a continuous day count — then subtract. This is what the Date-Difference solver does.",
            "JDN steps: a = floor((14 − month)/12);  y = year + 4800 − a;  m = month + 12a − 3.",
        ],
        formulas=[
            ("Julian Day Number", "JDN = day + floor((153m + 2)/5) + 365y + floor(y/4) − floor(y/100) + floor(y/400) − 32045"),
            ("Days between", "|JDN(date 2) − JDN(date 1)|"),
        ],
        examples=[
            Example("How many days from 10 Jan 2024 to 15 Mar 2024?",
                    ["Rest of January: 31 − 10 = 21", "February 2024 (leap year) = 29", "March: 15", "21 + 29 + 15 = 65"], "65 days"),
            Example("How many days from 26 Jan 2026 to 15 Aug 2026?",
                    ["Jan: 31 − 26 = 5", "Feb 28 + Mar 31 + Apr 30 + May 31 + Jun 30 + Jul 31 = 181", "Aug: 15",
                     "5 + 181 + 15 = 201"], "201 days"),
        ],
        tip="Watch February in leap years and decide early whether the question wants inclusive counting.",
        solver="calendar", keywords="difference between dates jdn julian day number duration",
    ),
    Topic(
        key="cal_count_weekdays",
        title="Counting a Particular Weekday",
        summary="How many Sundays / Mondays / … are in a month or year?",
        points=[
            "28 days → each weekday occurs exactly 4 times.",
            "29 days → the weekday of the 1st occurs 5 times.",
            "30 days → the weekdays of the 1st and 2nd occur 5 times.",
            "31 days → the weekdays of the 1st, 2nd and 3rd occur 5 times.",
            "Ordinary year (52 weeks + 1 day): the weekday of 1 Jan (= 31 Dec) occurs 53 times.",
            "Leap year (52 weeks + 2 days): the weekdays of 1 Jan and 2 Jan occur 53 times.",
        ],
        formulas=[
            ("Extra days in a month", "days − 28   (0, 1, 2 or 3)"),
            ("Extra days in a year", "1 (ordinary) or 2 (leap)  → those weekdays occur 53 times"),
        ],
        examples=[
            Example("1 Jan 2024 was a Monday. Which weekdays occur 53 times in 2024?",
                    ["2024 is a leap year → 2 extra days", "The extra weekdays are those of 1 Jan and 2 Jan"], "Monday and Tuesday"),
            Example("How many Sundays are there in March 2026, if 1 March 2026 is a Sunday?",
                    ["March has 31 days → 3 extra days", "Weekdays of the 1st, 2nd, 3rd (Sun, Mon, Tue) occur 5 times"], "5 Sundays (1, 8, 15, 22, 29)"),
        ],
        tip="Only the 'extra' days beyond 28 matter — everything else is just 4 full weeks.",
        solver="calendar", keywords="count sundays mondays number of weekdays 53",
    ),
    Topic(
        key="cal_repeat",
        title="Repeating Calendars",
        summary="When does a year's calendar repeat exactly (same dates on the same weekdays)?",
        points=[
            "Two years have the same calendar when (1) both are ordinary or both are leap, and (2) 1 Jan falls on the same weekday.",
            "Condition (2) holds when the odd days of the years in between add up to a multiple of 7.",
            "Method: from the given year, add 1 odd day for each ordinary year and 2 for each leap year until the total is 0 mod 7 AND the new year has the same leap status.",
            "Ordinary-year calendars repeat after 6, 11 or 12 years depending on where the leap years fall.",
            "Leap-year calendars usually repeat after 28 years (12 or 40 years around a non-leap century such as 2100).",
            "Across all centuries the calendar repeats every 400 years.",
        ],
        formulas=[
            ("Repeat condition", "sum of odd days (1 per ordinary, 2 per leap year) ≡ 0 (mod 7), same leap status"),
            ("Leap-year cycle", "28 years (usually)"),
        ],
        examples=[
            Example("Which year will have the same calendar as 2017?",
                    ["2017–2022: 6 years, one leap year (2020) → 6 + 1 = 7 → 0", "2023 is an ordinary year"], "2023"),
            Example("Which year will have the same calendar as 2023?",
                    ["2023–2033: 11 years with leap years 2024, 2028, 2032 → 11 + 3 = 14 → 0", "2034 is ordinary"], "2034"),
            Example("Which year will have the same calendar as 2000?",
                    ["28 years, 7 leap years → 28 + 7 = 35 → 0", "2028 is a leap year"], "2028"),
        ],
        tip="Check the leap status first, then add odd days; stop only when both conditions are true together.",
        solver="calendar", keywords="same calendar repeat 28 year cycle",
    ),
    Topic(
        key="cal_month_groups",
        title="Months With Identical Calendars",
        summary="Which months of the same year start on the same weekday (and therefore look identical)?",
        points=[
            "Each month's start weekday shifts by the previous month's odd days.",
            "Use these groups to move from a known weekday to any other month instantly.",
        ],
        formulas=[
            ("Start-weekday shift", "start(next month) = start(this month) + (days in this month) mod 7"),
        ],
        examples=[
            Example("1 Jan 2026 is a Thursday. What day is 7 October 2026?",
                    ["2026 is an ordinary year → January and October start on the same weekday", "1 Oct is a Thursday",
                     "7 Oct is 6 days later → Thursday + 6"], "Wednesday"),
        ],
        tip="Memorise the ordinary-year groups: Jan-Oct, Feb-Mar-Nov, Apr-Jul, Sep-Dec.",
        table_title="Months that start on the same weekday",
        table=[["Year type", "Same-start groups", "Stand alone"],
               ["Ordinary", "Jan–Oct · Feb–Mar–Nov · Apr–Jul · Sep–Dec", "May, Jun, Aug"],
               ["Leap", "Jan–Apr–Jul · Feb–Aug · Mar–Nov · Sep–Dec", "May, Jun, Oct"]],
        solver="calendar", keywords="same month same calendar start weekday",
    ),
    Topic(
        key="cal_cycles",
        title="Gregorian Cycle & Century Facts",
        summary="Why calendars behave the way they do over centuries.",
        points=[
            "The Gregorian calendar has 97 leap years in every 400 years → 146 097 days = 20 871 weeks exactly.",
            "So the whole calendar repeats every 400 years. Average year length = 365.2425 days.",
            "100 years without a leap century year = 36 524 days = 5217 weeks + 5 days → 5 odd days; a century containing one (e.g. 1901–2000) has 36 525 days → 6 odd days.",
            "31 December of 1700 was a Friday, of 1800 a Wednesday, of 1900 a Monday and of 2000 a Sunday (Fri – Wed – Mon – Sun).",
            "The Gregorian reform started in October 1582; exam problems use the Gregorian rules for all dates.",
        ],
        formulas=[
            ("Days in 400 years", "400 × 365 + 97 = 146 097 = 7 × 20 871"),
            ("Mean year", "146 097 / 400 = 365.2425 days"),
        ],
        examples=[
            Example("What day was 1 January 1901?",
                    ["1900 years completed → 1 odd day → 31 Dec 1900 is a Monday", "1 Jan 1901 is the next day"], "Tuesday"),
            Example("What day was 1 January 2001?",
                    ["2000 years completed → 0 odd days → 31 Dec 2000 is a Sunday", "1 Jan 2001 is the next day"], "Monday"),
        ],
        tip="Century-end days repeat in the order Fri – Wed – Mon – Sun (1700, 1800, 1900, 2000).",
        solver="calendar", keywords="gregorian 400 year cycle century",
    ),
    Topic(
        key="cal_cheat",
        title="Calendar Cheat Sheet",
        summary="Every calendar formula on one screen — revise this before an exam.",
        points=[
            "Odd days: ordinary year 1, leap year 2.   Months: 31 → 3, 30 → 2, Feb → 0 (1 if leap).",
            "Centuries: 100 → 5, 200 → 3, 300 → 1, 400 → 0 odd days  (century ends: Fri, Wed, Mon, Sun).",
            "Leap year: divisible by 4 and not by 100, or divisible by 400.   L(N) = N/4 − N/100 + N/400 (floors).",
            "Weekday: (century + year + date odd days) mod 7;  0 = Sunday.",
            "Zeller: h = (q + floor(13(m+1)/5) + K + K/4 + J/4 − 2J) mod 7;  0 = Saturday.",
            "Weekday after N days = (today + N mod 7).",
            "Month groups (ordinary): Jan-Oct, Feb-Mar-Nov, Apr-Jul, Sep-Dec.",
            "53 weekdays in a year: 1 (ordinary) or 2 (leap).",
        ],
        formulas=[
            ("Weekday (odd days)", "(C + Y + D) mod 7"),
            ("Days between", "|JDN₂ − JDN₁|"),
        ],
        examples=[
            Example("Quick check: is 2100 a leap year?", ["2100 is divisible by 100 but not by 400"], "No"),
        ],
        tip="Practise one date per method (odd days, Zeller, Doomsday) and compare — all must agree.",
        solver="calendar", keywords="summary revision formulas",
    ),
]

CATEGORIES: dict[str, list[Topic]] = {
    "Clock": CLOCK_TOPICS,
    "Calendar": CALENDAR_TOPICS,
}


def all_topics() -> list[tuple[str, Topic]]:
    """Every topic paired with its category name."""
    return [(cat, t) for cat, topics in CATEGORIES.items() for t in topics]


def search_topics(query: str) -> list[tuple[str, Topic]]:
    """Case-insensitive search over title, summary and keywords."""
    q = query.strip().lower()
    if not q:
        return all_topics()
    return [
        (cat, t) for cat, t in all_topics()
        if q in t.title.lower() or q in t.summary.lower() or q in t.keywords.lower()
    ]
