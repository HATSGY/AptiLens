"""Tests for the Concepts Library: content integrity + numeric verification
of the worked examples against the verified logic layer."""

import datetime

import pytest

from src.modules.calendar.calendar_logic import (
    calculate_day_of_week, century_odd_days, count_leap_years, days_between_dates,
    doomsday_weekday, leap_years_up_to, month_start_groups, next_repeating_year,
    odd_days_weekday, shift_day,
)
from src.modules.clock.clock_logic import (
    calculate_clock_angle, clock_gain_loss_in_24h, find_times_for_angle,
    hands_opposite_time, hands_overlap_time, mirror_image_time, water_image_time,
)
from src.modules.concepts.concepts_data import (
    CALENDAR_TOPICS, CATEGORIES, CLOCK_TOPICS, all_topics, search_topics,
)

VALID_SOLVERS = {None, "clock", "calendar", "tabular", "graphs", "caselet", "missing_data"}


# --------------------------------------------------------------- content integrity
def test_both_categories_have_topics():
    assert len(CLOCK_TOPICS) >= 10 and len(CALENDAR_TOPICS) >= 10
    assert set(CATEGORIES) == {"Clock", "Calendar", "Data Interpretation"}


def test_topic_keys_are_unique():
    keys = [t.key for _, t in all_topics()]
    assert len(keys) == len(set(keys))


@pytest.mark.parametrize("category,topic", all_topics(), ids=lambda v: getattr(v, "key", v))
def test_every_topic_is_complete(category, topic):
    assert topic.title and topic.summary
    assert topic.points, "needs key ideas"
    assert topic.formulas, "needs at least one formula"
    assert topic.examples, "needs at least one worked example"
    assert topic.solver in VALID_SOLVERS
    for ex in topic.examples:
        assert ex.problem and ex.steps and ex.answer
    if topic.table:
        width = len(topic.table[0])
        assert all(len(row) == width for row in topic.table)


def test_search_finds_by_title_and_keyword():
    assert any(t.key == "cal_zeller" for _, t in search_topics("zeller"))
    assert any(t.key == "clock_mirror_water" for _, t in search_topics("upside down"))
    assert search_topics("zzzz-no-match") == []
    assert len(search_topics("")) == len(all_topics())


# --------------------------------------------------------------- clock examples
def test_clock_angle_examples():
    assert calculate_clock_angle(3, 20).angle == 20
    assert calculate_clock_angle(4, 40).angle == 100
    nine_fifteen = calculate_clock_angle(9, 15)
    assert nine_fifteen.angle == 172.5 and nine_fifteen.reflex_angle == 187.5


def test_hand_positions_at_7_30():
    h, m = 7, 30
    assert 30 * h + 0.5 * m == 225 and 6 * m == 180


def test_time_for_angle_examples():
    five = find_times_for_angle(5, 60)
    assert five == pytest.approx([180 / 11, 420 / 11], abs=0.01)
    two = find_times_for_angle(2, 30)
    assert two == pytest.approx([60 / 11, 180 / 11], abs=0.01)


def test_overlap_formula_zero_angle_for_every_hour():
    for h in range(1, 11):
        m = hands_overlap_time(h)
        assert abs(30 * h - 5.5 * m) < 1e-9
    assert hands_overlap_time(4) == pytest.approx(240 / 11)       # 4:21 9/11
    assert 720 / 11 == pytest.approx(65 + 5 / 11)                  # gap between overlaps


def test_opposite_formula_gives_180_degrees():
    for h in range(0, 12):
        m = hands_opposite_time(h)
        if 0 <= m < 60:
            raw = abs(30 * h - 5.5 * m)
            assert min(raw, 360 - raw) == pytest.approx(180)
    assert hands_opposite_time(4) == pytest.approx(600 / 11)       # 4:54 6/11
    assert hands_opposite_time(8) == pytest.approx(120 / 11)       # 8:10 10/11


def test_right_angle_examples_between_3_and_4():
    assert find_times_for_angle(3, 90) == pytest.approx([0.0, 360 / 11], abs=0.01)


def test_minute_space_shortcut_matches_formula():
    assert 40 * 12 / 11 == pytest.approx(hands_overlap_time(8))    # 8:43 7/11
    assert 30 * 12 / 11 == pytest.approx(360 / 11)                 # 3:32 8/11


def test_overlap_count_is_eleven_in_twelve_hours():
    # H = 11 gives 11:60 == 12:00, the same instant as H = 0, so 12 hours -> 11 distinct overlaps.
    instants = {round(h * 60 + hands_overlap_time(h)) % 720 for h in range(12)}
    assert len(instants) == 11


def test_mirror_and_water_examples():
    assert mirror_image_time(4, 25) == (7, 35)
    assert mirror_image_time(10, 10) == (1, 50)
    assert water_image_time(4, 25) == (1, 35)
    assert water_image_time(8, 0) == (10, 0)


def test_mirror_matches_true_reflection_of_both_hands():
    """A plane mirror maps every hand angle to 360 - angle; the result is a valid time."""
    for h in range(1, 13):
        for m in range(0, 60, 5):
            hour_angle = (30 * (h % 12) + 0.5 * m) % 360
            minute_angle = (6 * m) % 360
            mh, mm = mirror_image_time(h, m)
            assert (30 * (mh % 12) + 0.5 * mm) % 360 == pytest.approx((360 - hour_angle) % 360)
            assert (6 * mm) % 360 == pytest.approx((360 - minute_angle) % 360)


def test_water_image_is_mirror_image_turned_upside_down():
    """Exam convention: water image = mirror image rotated 180 degrees (6 hours)."""
    for h in range(1, 13):
        for m in range(0, 60, 5):
            mh, mm = mirror_image_time(h, m)
            expected = ((mh % 12) * 60 + mm - 360) % 720
            wh, wm = water_image_time(h, m)
            assert ((wh % 12) * 60 + wm) % 720 == expected


def test_mirror_plus_time_is_twelve():
    h, m = mirror_image_time(4, 25)
    assert (h * 60 + m) + (4 * 60 + 25) == 12 * 60


def test_fast_slow_clock_examples():
    assert 6 * 5 == 30                                   # gains 30 min in 6 h
    assert 420 * 60 / 56 == 450                          # loses 4 min/h: 7 h shown = 7.5 h true
    assert clock_gain_loss_in_24h(66) == pytest.approx(-11 - 109 / 121, abs=1e-6)
    assert clock_gain_loss_in_24h(720 / 11) == pytest.approx(0, abs=1e-9)
    assert clock_gain_loss_in_24h(60) > 0                # hands meet sooner -> clock runs fast


def test_clock_strikes_and_time_arithmetic():
    assert 5 / (6 - 1) * (11 - 1) == 10
    assert 6 / (4 - 1) * (10 - 1) == 18
    assert 2 * sum(range(1, 13)) + 24 == 180
    assert ((6 * 60 + 20) - (21 * 60 + 45)) % 1440 == 515


# --------------------------------------------------------------- calendar examples
def test_leap_year_counts():
    assert count_leap_years(1901, 2000) == 25
    assert count_leap_years(2001, 2100) == 24
    assert leap_years_up_to(2000) == 485 and leap_years_up_to(1900) == 460
    assert leap_years_up_to(2100) == 509


def test_odd_days_in_years_and_centuries():
    assert (30 + count_leap_years(1991, 2020)) % 7 == 3
    assert [century_odd_days(c) for c in (100, 200, 300, 400)] == [5, 3, 1, 0]
    assert century_odd_days(1600) == 0 and century_odd_days(1900) == 1 and century_odd_days(2000) == 0
    with pytest.raises(ValueError):
        century_odd_days(150)


def test_odd_days_method_examples():
    r = odd_days_weekday(15, 8, 1947)
    assert (r["centuries_odd"], r["years_odd"], r["days_odd"], r["weekday"]) == (1, 1, 3, "Friday")
    assert odd_days_weekday(26, 1, 1950)["weekday"] == "Thursday"


def test_zeller_examples():
    assert calculate_day_of_week(7, 10, 2026)["weekday"] == "Wednesday"
    assert calculate_day_of_week(7, 10, 2026)["h_value"] == 4
    assert calculate_day_of_week(1, 1, 2000)["weekday"] == "Saturday"
    assert calculate_day_of_week(1, 1, 2000)["h_value"] == 0


def test_doomsday_examples():
    r = doomsday_weekday(7, 10, 2026)
    assert r["doomsday_name"] == "Saturday" and r["weekday"] == "Wednesday"
    r = doomsday_weekday(4, 7, 1976)
    assert r["doomsday_name"] == "Sunday" and r["weekday"] == "Sunday"


def test_methods_agree_with_datetime_on_a_wide_sweep():
    for year in range(1583, 2600, 11):
        for month in range(1, 13):
            for day in (1, 14, 28):
                expected = datetime.date(year, month, day).strftime("%A")
                assert odd_days_weekday(day, month, year)["weekday"] == expected
                assert doomsday_weekday(day, month, year)["weekday"] == expected
                assert calculate_day_of_week(day, month, year)["weekday"] == expected


def test_century_end_days():
    assert datetime.date(1700, 12, 31).strftime("%A") == "Friday"
    assert datetime.date(1800, 12, 31).strftime("%A") == "Wednesday"
    assert datetime.date(1900, 12, 31).strftime("%A") == "Monday"
    assert datetime.date(2000, 12, 31).strftime("%A") == "Sunday"
    assert datetime.date(1901, 1, 1).strftime("%A") == "Tuesday"
    assert datetime.date(2001, 1, 1).strftime("%A") == "Monday"


def test_days_between_examples():
    assert days_between_dates(10, 1, 2024, 15, 3, 2024)["days_between"] == 65
    assert days_between_dates(26, 1, 2026, 15, 8, 2026)["days_between"] == 201


def test_weekday_after_n_days_examples():
    # 7 Oct 2026 is Wednesday; +100 days -> Friday
    result = shift_day(7, 10, 2026, 100)["result_date"]
    d, m, y = map(int, result.split("-"))
    assert datetime.date(y, m, d).strftime("%A") == "Friday"
    assert datetime.date(2027, 10, 7).strftime("%A") == "Thursday"
    assert datetime.date(2028, 10, 7).strftime("%A") == "Saturday"
    assert datetime.date(2026, 1, 1).strftime("%A") == "Thursday"
    assert datetime.date(2025, 1, 1).strftime("%A") == "Wednesday"


def test_counting_weekdays_examples():
    def count(year, weekday_name):
        d, n = datetime.date(year, 1, 1), 0
        while d.year == year:
            n += d.strftime("%A") == weekday_name
            d += datetime.timedelta(days=1)
        return n

    assert datetime.date(2024, 1, 1).strftime("%A") == "Monday"
    assert count(2024, "Monday") == 53 and count(2024, "Tuesday") == 53 and count(2024, "Wednesday") == 52
    assert datetime.date(2026, 3, 1).strftime("%A") == "Sunday"
    sundays = [d for d in range(1, 32) if datetime.date(2026, 3, d).strftime("%A") == "Sunday"]
    assert sundays == [1, 8, 15, 22, 29]


def test_repeating_calendar_examples():
    assert next_repeating_year(2017) == 2023
    assert next_repeating_year(2023) == 2034
    assert next_repeating_year(2000) == 2028
    assert next_repeating_year(2024) == 2052
    # claimed gap sets
    ordinary = {next_repeating_year(y) - y for y in range(1901, 2100) if y % 4 != 0}
    assert ordinary <= {6, 11, 12}


def test_repeated_year_really_has_identical_calendar():
    for y in (2017, 2023, 2000):
        z = next_repeating_year(y)
        a, b = datetime.date(y, 1, 1), datetime.date(z, 1, 1)
        assert a.strftime("%A") == b.strftime("%A")
        assert (datetime.date(y + 1, 1, 1) - a).days == (datetime.date(z + 1, 1, 1) - b).days


def test_month_start_groups_match_the_published_table():
    ordinary = {frozenset(g) for g in month_start_groups(False)}
    leap = {frozenset(g) for g in month_start_groups(True)}
    assert {frozenset(s) for s in (["Jan", "Oct"], ["Feb", "Mar", "Nov"], ["Apr", "Jul"], ["Sep", "Dec"],
                                    ["May"], ["Jun"], ["Aug"])} == ordinary
    assert {frozenset(s) for s in (["Jan", "Apr", "Jul"], ["Feb", "Aug"], ["Mar", "Nov"], ["Sep", "Dec"],
                                    ["May"], ["Jun"], ["Oct"])} == leap
    # Real-world check: Jan 1 and Oct 1 2026 (ordinary) share a weekday.
    assert datetime.date(2026, 1, 1).weekday() == datetime.date(2026, 10, 1).weekday()


def test_gregorian_cycle_constants():
    assert 400 * 365 + 97 == 146097 == 7 * 20871
    assert 146097 / 400 == 365.2425
    assert (datetime.date(2400, 1, 1) - datetime.date(2000, 1, 1)).days == 146097
