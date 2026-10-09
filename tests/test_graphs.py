import pytest

from src.modules.graphs.graph_logic import (
    analyze_bar, analyze_histogram, analyze_line, analyze_pie, analyze_scatter,
)


def test_analyze_bar_highest_lowest():
    categories = ["Jan", "Feb", "Mar"]
    values = [45, 60, 30]
    result = analyze_bar(categories, values)
    assert result["highest"] == {"category": "Feb", "value": 60.0}
    assert result["lowest"] == {"category": "Mar", "value": 30.0}
    assert result["difference_highest_lowest"] == 30.0


def test_analyze_pie_percentages_sum_to_100():
    categories = ["A", "B", "C"]
    values = [50, 30, 20]
    result = analyze_pie(categories, values)
    assert result["total"] == 100
    total_pct = sum(s["percentage"] for s in result["sector_breakdown"])
    assert total_pct == pytest.approx(100.0, abs=0.1)
    assert result["largest_sector"]["category"] == "A"


def test_analyze_line_consistently_increasing():
    result = analyze_line(["Q1", "Q2", "Q3", "Q4"], [10, 20, 30, 40])
    assert result["trend"] == "Consistently increasing"
    assert result["overall_change"] == 30
    assert result["maximum"]["point"] == "Q4"
    assert result["minimum"]["point"] == "Q1"


def test_analyze_line_consistently_decreasing():
    result = analyze_line(["Q1", "Q2", "Q3"], [40, 30, 20])
    assert result["trend"] == "Consistently decreasing"


def test_analyze_scatter_perfect_positive_correlation():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    result = analyze_scatter(x, y)
    assert result["correlation_coefficient"] == pytest.approx(1.0, abs=1e-6)
    assert "positive" in result["relationship"].lower()


def test_analyze_scatter_perfect_negative_correlation():
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]
    result = analyze_scatter(x, y)
    assert result["correlation_coefficient"] == pytest.approx(-1.0, abs=1e-6)
    assert "negative" in result["relationship"].lower()


def test_analyze_scatter_mismatched_lengths_raises():
    with pytest.raises(ValueError):
        analyze_scatter([1, 2, 3], [1, 2])


def test_analyze_histogram_basic():
    values = [10, 12, 15, 20, 22, 25, 30, 33, 35, 40]
    result = analyze_histogram(values, num_bins=3)
    assert result["total_observations"] == 10
    assert sum(result["frequencies"]) == 10
    assert result["highest_frequency"] >= 1
