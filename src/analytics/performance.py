"""
Performance Analysis: persists Practice Mode session results locally as
JSON and aggregates them into topic-level statistics and charts.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

from src.utils.chart_utils import new_figure
from src.utils.helpers import load_json, save_json


def load_sessions(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = load_json(path)
    except ValueError:
        return []
    return data if isinstance(data, list) else []


def save_session(path: Path, session_summary: dict) -> None:
    sessions = load_sessions(path)
    sessions.append({
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        **session_summary,
    })
    save_json(path, sessions)


def aggregate_topic_stats(sessions: list[dict]) -> dict[str, dict]:
    """Merge topic_breakdown across every stored session into one totals dict."""
    totals: dict[str, dict] = {}
    for session in sessions:
        for topic, stats in session.get("topic_breakdown", {}).items():
            entry = totals.setdefault(topic, {"attempted": 0, "correct": 0})
            entry["attempted"] += stats.get("attempted", 0)
            entry["correct"] += stats.get("correct", 0)
    for entry in totals.values():
        entry["accuracy"] = round(entry["correct"] / entry["attempted"] * 100, 2) if entry["attempted"] else 0.0
    return totals


def overall_stats(sessions: list[dict]) -> dict:
    if not sessions:
        return {"total_questions": 0, "correct": 0, "accuracy_percent": 0.0,
                "average_time": 0.0, "sessions_completed": 0}
    total_q = sum(s.get("total_questions", 0) for s in sessions)
    total_correct = sum(s.get("correct", 0) for s in sessions)
    total_time = sum(s.get("total_time", 0.0) for s in sessions)
    return {
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy_percent": round(total_correct / total_q * 100, 2) if total_q else 0.0,
        "average_time": round(total_time / total_q, 2) if total_q else 0.0,
        "sessions_completed": len(sessions),
    }


def build_accuracy_by_topic_chart(topic_stats: dict[str, dict]):
    fig, ax = new_figure((6.4, 3.8))
    topics = list(topic_stats.keys())
    accuracy = [topic_stats[t]["accuracy"] for t in topics]
    ax.bar(topics, accuracy, color="#34D399")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Accuracy by Topic")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig


def build_attempted_by_topic_chart(topic_stats: dict[str, dict]):
    fig, ax = new_figure((6.4, 3.8))
    topics = list(topic_stats.keys())
    attempted = [topic_stats[t]["attempted"] for t in topics]
    ax.bar(topics, attempted, color="#4F7DF3")
    ax.set_ylabel("Questions Attempted")
    ax.set_title("Questions Attempted by Topic")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig
