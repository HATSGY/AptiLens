"""
Question engine for Practice Mode.

Loads the question bank from data/sample_questions.json and builds a
practice set filtered by topic(s) and difficulty. This is pure data
selection logic with no GUI or AI dependency, which keeps it easily
testable.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Optional

from src.utils.helpers import load_json


def load_question_bank(path: Path) -> list[dict]:
    questions = load_json(path)
    if not isinstance(questions, list) or not questions:
        raise ValueError("sample_questions.json must contain a non-empty list of questions.")
    return questions


def available_topics(bank: list[dict]) -> list[str]:
    return sorted({q["topic"] for q in bank})


def build_practice_set(bank: list[dict], topics: Optional[list[str]], difficulty: str,
                        count: int, seed: int | None = None) -> list[dict]:
    """Select `count` questions matching the given topics/difficulty.

    Args:
        topics: list of topic names to include, or None/empty for "all topics".
        difficulty: "Easy" | "Medium" | "Hard" | "Any".
        count: desired number of questions.
        seed: optional RNG seed, primarily used by tests for determinism.

    Returns:
        A shuffled list of up to `count` question dicts (fewer if the bank
        does not contain enough matching questions).
    """
    if count <= 0:
        raise ValueError("Number of questions must be at least 1.")

    pool = bank
    if topics:
        pool = [q for q in pool if q["topic"] in topics]
    if difficulty and difficulty != "Any":
        pool = [q for q in pool if q["difficulty"] == difficulty]

    if not pool:
        raise ValueError("No questions match the selected topics/difficulty.")

    rng = random.Random(seed)
    pool = pool.copy()
    rng.shuffle(pool)
    return pool[:count]


def check_answer(question: dict, user_answer: str) -> bool:
    """Compare a user's answer against the question's stored answer.

    Numerical answers are compared with light tolerance for formatting
    (e.g. '20' vs '20.0' vs '20%'); MCQ / text answers are compared
    case-insensitively after stripping whitespace and a trailing '%'.
    """
    correct = str(question["answer"]).strip()
    given = str(user_answer).strip()

    def _normalize(s: str) -> str:
        return s.rstrip("%").strip().lower()

    if question.get("type") == "Numerical":
        try:
            return abs(float(_normalize(correct)) - float(_normalize(given))) < 1e-6
        except ValueError:
            pass  # fall through to text comparison for non-numeric "answers"

    return _normalize(correct) == _normalize(given)
