import pytest

from src.modules.missing_data.missing_data_logic import (
    solve_missing_by_average, solve_missing_by_ratio, solve_missing_by_total,
    solve_missing_growth_table,
)


def test_solve_missing_by_total():
    result = solve_missing_by_total({"A": 30, "B": None, "C": 50}, total=100)
    assert result["missing_key"] == "B"
    assert result["answer"] == 20


def test_solve_missing_by_total_requires_exactly_one_missing():
    with pytest.raises(ValueError):
        solve_missing_by_total({"A": None, "B": None}, total=100)


def test_solve_missing_by_average():
    result = solve_missing_by_average([15, None, 25], average=20)
    assert result["answer"] == 20


def test_solve_missing_by_ratio_find_a():
    result = solve_missing_by_ratio(None, 100, ratio_a=3, ratio_b=5)
    assert result["answer"] == pytest.approx(60.0)


def test_solve_missing_by_ratio_find_b():
    result = solve_missing_by_ratio(60, None, ratio_a=3, ratio_b=5)
    assert result["answer"] == pytest.approx(100.0)


def test_solve_missing_by_ratio_requires_one_missing():
    with pytest.raises(ValueError):
        solve_missing_by_ratio(60, 100, ratio_a=3, ratio_b=5)


def test_solve_missing_growth_table_from_spec_example():
    rows = [
        {"year": 2022, "value": 100.0, "growth_pct": None},
        {"year": 2023, "value": None, "growth_pct": 20.0},
        {"year": 2024, "value": 144.0, "growth_pct": None},
    ]
    result = solve_missing_growth_table(rows)
    assert result["fully_solved"] is True
    resolved = {r["year"]: r for r in result["resolved_rows"]}
    assert resolved[2023]["value"] == pytest.approx(120.0)
    assert resolved[2024]["growth_pct"] == pytest.approx(20.0)


def test_solve_missing_growth_table_solves_previous_value():
    # cur_val and growth known, prev_val missing -> must solve backwards.
    rows = [
        {"year": 2022, "value": None, "growth_pct": None},
        {"year": 2023, "value": 120.0, "growth_pct": 20.0},
    ]
    result = solve_missing_growth_table(rows)
    resolved = {r["year"]: r for r in result["resolved_rows"]}
    assert resolved[2022]["value"] == pytest.approx(100.0)


def test_solve_missing_growth_table_multi_step_chain():
    rows = [
        {"year": "Q1", "value": 50.0, "growth_pct": None},
        {"year": "Q2", "value": None, "growth_pct": 10.0},
        {"year": "Q3", "value": None, "growth_pct": 15.0},
        {"year": "Q4", "value": 75.0, "growth_pct": None},
    ]
    result = solve_missing_growth_table(rows)
    assert result["fully_solved"] is True
    resolved = {r["year"]: r for r in result["resolved_rows"]}
    assert resolved["Q2"]["value"] == pytest.approx(55.0)
    assert resolved["Q3"]["value"] == pytest.approx(63.25)
