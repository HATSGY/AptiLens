import pytest

from src.modules.patterns.pattern_logic import analyze_pattern


def test_arithmetic_progression():
    result = analyze_pattern([3, 6, 9, 12])
    assert result["detected"] is True
    assert result["next_value"] == 15
    assert "Arithmetic" in result["pattern_name"]


def test_geometric_progression():
    result = analyze_pattern([2, 4, 8, 16])
    assert result["detected"] is True
    assert result["next_value"] == 32
    assert "Geometric" in result["pattern_name"]


def test_fibonacci_like():
    result = analyze_pattern([1, 1, 2, 3, 5, 8])
    assert result["detected"] is True
    assert result["next_value"] == 13
    assert "Fibonacci" in result["pattern_name"]


def test_perfect_square_pattern():
    result = analyze_pattern([1, 4, 9, 16])
    assert result["detected"] is True
    assert result["next_value"] == 25
    assert "Square" in result["pattern_name"]


def test_perfect_cube_pattern():
    result = analyze_pattern([1, 8, 27, 64])
    assert result["detected"] is True
    assert result["next_value"] == 125
    assert "Cube" in result["pattern_name"]


def test_quadratic_second_difference_pattern():
    result = analyze_pattern([2, 6, 12, 20])
    assert result["detected"] is True
    assert result["next_value"] == 30


def test_alternating_pattern():
    result = analyze_pattern([1, 3, 2, 6, 3, 9])
    assert result["detected"] is True
    assert result["next_value"] is not None


def test_unrecognized_pattern_reports_not_detected():
    result = analyze_pattern([1, 7, 2, 19, 100])
    assert result["detected"] is False
    assert result["next_value"] is None


def test_too_short_sequence_raises():
    with pytest.raises(ValueError):
        analyze_pattern([1, 2])
