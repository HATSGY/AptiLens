import pytest

from src.modules.clock.clock_logic import calculate_clock_angle, find_times_for_angle


def test_angle_3_20():
    result = calculate_clock_angle(3, 20)
    assert result.angle == 20.0


def test_angle_6_00_is_180():
    result = calculate_clock_angle(6, 0)
    assert result.angle == 180.0
    assert result.reflex_angle == 180.0


def test_angle_12_00_is_zero():
    result = calculate_clock_angle(12, 0)
    assert result.angle == 0.0


def test_angle_4_40():
    result = calculate_clock_angle(4, 40)
    assert result.angle == 100.0


def test_angle_always_between_0_and_180():
    for h in range(0, 13):
        for m in range(0, 60, 7):
            result = calculate_clock_angle(h, m)
            assert 0.0 <= result.angle <= 180.0
            assert result.angle + result.reflex_angle == pytest.approx(360.0)


def test_invalid_hour_raises():
    with pytest.raises(ValueError):
        calculate_clock_angle(13, 0)


def test_invalid_minute_raises():
    with pytest.raises(ValueError):
        calculate_clock_angle(5, 60)


def test_find_times_for_angle_180_between_6_and_7():
    # Classic result: hands are opposite at 6:00 exactly.
    solutions = find_times_for_angle(6, 180)
    assert 0.0 in solutions


def test_find_times_for_angle_roundtrip():
    # Whatever minute find_times_for_angle returns for a target angle at
    # a given hour must, when fed back into calculate_clock_angle, actually
    # reproduce that angle.
    hour, target_angle = 7, 180
    solutions = find_times_for_angle(hour, target_angle)
    assert solutions, "expected at least one solution"
    for m in solutions:
        result = calculate_clock_angle(hour, round(m))
        assert abs(result.angle - target_angle) <= 3  # rounding tolerance
