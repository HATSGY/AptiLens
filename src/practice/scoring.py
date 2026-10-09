"""Scoring and session tracking for Practice Mode."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Attempt:
    question_id: str
    topic: str
    difficulty: str
    correct: bool
    time_taken: float
    user_answer: str
    correct_answer: str


@dataclass
class PracticeSession:
    attempts: list[Attempt] = field(default_factory=list)

    def record(self, attempt: Attempt) -> None:
        self.attempts.append(attempt)

    @property
    def total_questions(self) -> int:
        return len(self.attempts)

    @property
    def total_correct(self) -> int:
        return sum(1 for a in self.attempts if a.correct)

    @property
    def total_incorrect(self) -> int:
        return self.total_questions - self.total_correct

    @property
    def accuracy_percent(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round(self.total_correct / self.total_questions * 100, 2)

    @property
    def total_time(self) -> float:
        return round(sum(a.time_taken for a in self.attempts), 2)

    @property
    def average_time(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round(self.total_time / self.total_questions, 2)

    def topic_breakdown(self) -> dict[str, dict]:
        """Per-topic {attempted, correct, accuracy}."""
        breakdown: dict[str, dict] = {}
        for a in self.attempts:
            entry = breakdown.setdefault(a.topic, {"attempted": 0, "correct": 0})
            entry["attempted"] += 1
            entry["correct"] += int(a.correct)
        for entry in breakdown.values():
            entry["accuracy"] = round(entry["correct"] / entry["attempted"] * 100, 2) if entry["attempted"] else 0.0
        return breakdown

    def summary(self) -> dict:
        return {
            "total_questions": self.total_questions,
            "correct": self.total_correct,
            "incorrect": self.total_incorrect,
            "accuracy_percent": self.accuracy_percent,
            "total_time": self.total_time,
            "average_time": self.average_time,
            "topic_breakdown": self.topic_breakdown(),
        }

    def to_dict(self) -> dict:
        return {
            "attempts": [a.__dict__ for a in self.attempts],
            "summary": self.summary(),
        }
