import pytest

from src.config.settings import CASELET_DATA_FILE
from src.modules.caselet.caselet_logic import load_caselets, solve_caselet_question


@pytest.fixture(scope="module")
def caselets():
    return load_caselets(CASELET_DATA_FILE)


def test_load_caselets_returns_five(caselets):
    assert len(caselets) == 5


def test_sales_caselet_sum(caselets):
    caselet = caselets[0]
    question = caselet["questions"][0]  # sum of Sales_2023
    result = solve_caselet_question(caselet, question)
    assert result["answer"] == 150 + 110 + 160 + 125


def test_sales_caselet_percentage_of_total(caselets):
    caselet = caselets[0]
    question = next(q for q in caselet["questions"] if q["operation"] == "percentage_of_total")
    result = solve_caselet_question(caselet, question)
    total = 150 + 110 + 160 + 125
    expected = round(150 / total * 100, 2)
    assert result["answer"] == expected


def test_sales_caselet_ratio(caselets):
    caselet = caselets[0]
    question = next(q for q in caselet["questions"] if q["operation"] == "ratio")
    result = solve_caselet_question(caselet, question)
    assert result["answer"] == "24 : 19"  # North:South 2022 = 120:95 -> 24:19


def test_sales_caselet_difference(caselets):
    caselet = caselets[0]
    question = next(q for q in caselet["questions"] if q["operation"] == "difference")
    result = solve_caselet_question(caselet, question)
    assert result["answer"] == 160 - 140  # East 2023 - East 2022


def test_all_caselets_all_questions_solve_without_error(caselets):
    for caselet in caselets:
        for question in caselet["questions"]:
            result = solve_caselet_question(caselet, question)
            assert "answer" in result
            assert "formula" in result


def test_bank_caselet_grand_total(caselets):
    bank_caselet = next(c for c in caselets if c["id"] == "caselet_bank")
    question = next(q for q in bank_caselet["questions"] if q["operation"] == "total")
    result = solve_caselet_question(bank_caselet, question)
    expected = (50 + 30 + 20) + (60 + 25 + 15) + (45 + 35 + 25) + (70 + 20 + 10)
    assert result["answer"] == expected


def test_invalid_operation_raises(caselets):
    bad_question = {"operation": "not_a_real_operation", "params": {}}
    with pytest.raises(ValueError):
        solve_caselet_question(caselets[0], bad_question)
