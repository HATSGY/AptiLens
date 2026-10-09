import pandas as pd
import pytest

from src.modules.tabular.tabular_logic import apply_operation, label_column, numeric_columns


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Region": ["North", "South", "East"],
        "2022": [120, 95, 140],
        "2023": [150, 110, 160],
    })


def test_numeric_columns(sample_df):
    assert numeric_columns(sample_df) == ["2022", "2023"]


def test_label_column(sample_df):
    assert label_column(sample_df) == "Region"


def test_sum(sample_df):
    result = apply_operation(sample_df, "Sum", "2023")
    assert result["answer"] == 420


def test_average(sample_df):
    result = apply_operation(sample_df, "Average", "2022")
    assert result["answer"] == pytest.approx((120 + 95 + 140) / 3)


def test_maximum(sample_df):
    result = apply_operation(sample_df, "Maximum", "2023")
    assert result["answer"] == 160
    assert result["row"] == "East"


def test_minimum(sample_df):
    result = apply_operation(sample_df, "Minimum", "2022")
    assert result["answer"] == 95
    assert result["row"] == "South"


def test_percentage_of_total(sample_df):
    result = apply_operation(sample_df, "Percentage of Total", "2023", row_a=0)
    expected = 150 / 420 * 100
    assert result["answer"] == pytest.approx(round(expected, 2))


def test_ratio(sample_df):
    result = apply_operation(sample_df, "Ratio (Row A : Row B)", "2022", row_a=0, row_b=1)
    assert result["answer"] == "24 : 19"  # 120:95 simplified


def test_difference(sample_df):
    result = apply_operation(sample_df, "Difference (Row A - Row B)", "2023", row_a=0, row_b=1)
    assert result["answer"] == 40


def test_percentage_increase(sample_df):
    result = apply_operation(
        sample_df, "Percentage Increase/Decrease (Row A -> Row B)", "2022", row_a=1, row_b=0)
    # South (95) -> North (120): increase
    expected = (120 - 95) / 95 * 100
    assert f"{round(expected, 2)}%" in result["answer"]
    assert "increase" in result["answer"]


def test_unknown_column_raises(sample_df):
    with pytest.raises(ValueError):
        apply_operation(sample_df, "Sum", "DoesNotExist")


def test_missing_rows_for_ratio_raises(sample_df):
    with pytest.raises(ValueError):
        apply_operation(sample_df, "Ratio (Row A : Row B)", "2022")
