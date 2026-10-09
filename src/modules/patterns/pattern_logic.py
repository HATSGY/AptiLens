"""
Core algorithmic logic for Number Pattern Recognition problems.

Detection strategy (checked in this order, first match wins):
    1. Arithmetic progression       (constant difference)
    2. Geometric progression        (constant ratio)
    3. Fibonacci-like               (term = sum of previous two)
    4. Perfect square sequence      (n^2, (n+1)^2, ...)
    5. Perfect cube sequence        (n^3, (n+1)^3, ...)
    6. Second-difference pattern    (differences of differences constant)
    7. Alternating pattern          (two interleaved simple sequences)

Every check returns a fully worked explanation; nothing here calls the AI.
"""

from __future__ import annotations

import math
from typing import Optional

_EPS = 1e-6


def _is_close(a: float, b: float, eps: float = _EPS) -> bool:
    return abs(a - b) < eps


def _differences(seq: list[float]) -> list[float]:
    return [round(seq[i + 1] - seq[i], 6) for i in range(len(seq) - 1)]


def _check_arithmetic(seq: list[float]) -> Optional[dict]:
    diffs = _differences(seq)
    if all(_is_close(d, diffs[0]) for d in diffs):
        d = diffs[0]
        next_value = seq[-1] + d
        return {
            "pattern_name": "Arithmetic Progression (constant difference)",
            "reasoning": [
                f"Consecutive differences: {diffs}",
                f"All differences equal {d:g} -> arithmetic progression.",
                f"Next value = last term + common difference = {seq[-1]:g} + {d:g} = {next_value:g}",
            ],
            "next_value": round(next_value, 6),
        }
    return None


def _check_geometric(seq: list[float]) -> Optional[dict]:
    if any(_is_close(v, 0.0) for v in seq[:-1]):
        return None
    ratios = [round(seq[i + 1] / seq[i], 6) for i in range(len(seq) - 1)]
    if all(_is_close(r, ratios[0]) for r in ratios):
        r = ratios[0]
        next_value = seq[-1] * r
        return {
            "pattern_name": "Geometric Progression (constant ratio)",
            "reasoning": [
                f"Consecutive ratios: {ratios}",
                f"All ratios equal {r:g} -> geometric progression.",
                f"Next value = last term × common ratio = {seq[-1]:g} × {r:g} = {next_value:g}",
            ],
            "next_value": round(next_value, 6),
        }
    return None


def _check_fibonacci_like(seq: list[float]) -> Optional[dict]:
    if len(seq) < 3:
        return None
    if all(_is_close(seq[i], seq[i - 1] + seq[i - 2]) for i in range(2, len(seq))):
        next_value = seq[-1] + seq[-2]
        return {
            "pattern_name": "Fibonacci-like (each term = sum of previous two)",
            "reasoning": [
                "Checked whether term[i] = term[i-1] + term[i-2] for every i >= 2: true for all terms.",
                f"Next value = {seq[-1]:g} + {seq[-2]:g} = {next_value:g}",
            ],
            "next_value": round(next_value, 6),
        }
    return None


def _check_power_sequence(seq: list[float], power: int, name: str) -> Optional[dict]:
    """Detect seq[i] == (n0 + i) ** power for some integer starting base n0."""
    roots = []
    for v in seq:
        if v < 0 and power % 2 == 0:
            return None
        root = (abs(v) ** (1.0 / power)) * (1 if v >= 0 else -1)
        rounded = round(root)
        if not _is_close(rounded ** power, v, eps=1e-4):
            return None
        roots.append(rounded)
    # roots must themselves be consecutive integers
    if all(roots[i + 1] - roots[i] == 1 for i in range(len(roots) - 1)):
        next_root = roots[-1] + 1
        next_value = next_root ** power
        return {
            "pattern_name": name,
            "reasoning": [
                f"Each term is a perfect {'square' if power == 2 else 'cube'}: "
                f"{[f'{r}^{power}={r**power}' for r in roots]}",
                f"The bases {roots} increase by 1 each time.",
                f"Next base = {next_root} -> next value = {next_root}^{power} = {next_value}",
            ],
            "next_value": float(next_value),
        }
    return None


def _check_second_difference(seq: list[float]) -> Optional[dict]:
    if len(seq) < 4:
        return None
    diffs = _differences(seq)
    second_diffs = _differences(diffs)
    if all(_is_close(d, second_diffs[0]) for d in second_diffs):
        d2 = second_diffs[0]
        next_diff = diffs[-1] + d2
        next_value = seq[-1] + next_diff
        return {
            "pattern_name": "Quadratic pattern (constant second difference)",
            "reasoning": [
                f"First differences: {diffs}",
                f"Second differences: {second_diffs}",
                f"Second differences are constant ({d2:g}) -> the sequence follows a quadratic rule.",
                f"Next first-difference = {diffs[-1]:g} + {d2:g} = {next_diff:g}",
                f"Next value = {seq[-1]:g} + {next_diff:g} = {next_value:g}",
            ],
            "next_value": round(next_value, 6),
        }
    return None


def _check_alternating(seq: list[float]) -> Optional[dict]:
    if len(seq) < 4:
        return None
    evens = seq[0::2]
    odds = seq[1::2]

    def _simple_rule(sub: list[float]) -> Optional[tuple[str, float]]:
        if len(sub) < 2:
            return None
        diffs = _differences(sub)
        if diffs and all(_is_close(d, diffs[0]) for d in diffs):
            return ("add", diffs[0])
        if all(not _is_close(v, 0) for v in sub[:-1]):
            ratios = [sub[i + 1] / sub[i] for i in range(len(sub) - 1)]
            if ratios and all(_is_close(r, ratios[0]) for r in ratios):
                return ("multiply", ratios[0])
        return None

    even_rule = _simple_rule(evens)
    odd_rule = _simple_rule(odds)
    if even_rule and odd_rule:
        # predict next term (continues whichever sub-sequence is due next)
        next_is_even_slot = len(seq) % 2 == 0
        if next_is_even_slot:
            op, val = even_rule
            next_value = evens[-1] + val if op == "add" else evens[-1] * val
        else:
            op, val = odd_rule
            next_value = odds[-1] + val if op == "add" else odds[-1] * val
        return {
            "pattern_name": "Alternating pattern (two interleaved sequences)",
            "reasoning": [
                f"Odd positions (1st, 3rd, 5th, ...): {evens} -> rule: {even_rule[0]} {even_rule[1]:g}",
                f"Even positions (2nd, 4th, 6th, ...): {odds} -> rule: {odd_rule[0]} {odd_rule[1]:g}",
                f"Next value continues the "
                f"{'odd-position' if next_is_even_slot else 'even-position'} sub-sequence: {next_value:g}",
            ],
            "next_value": round(next_value, 6),
        }
    return None


def analyze_pattern(sequence: list[float]) -> dict:
    """Detect the pattern governing `sequence` and predict the next term.

    Returns a dict with: sequence, detected (bool), pattern_name, reasoning
    (list[str]), next_value (float | None).
    """
    if len(sequence) < 3:
        raise ValueError("Provide at least 3 numbers to detect a pattern.")

    checks = [
        _check_arithmetic,
        _check_geometric,
        _check_fibonacci_like,
        lambda s: _check_power_sequence(s, 2, "Perfect Square pattern"),
        lambda s: _check_power_sequence(s, 3, "Perfect Cube pattern"),
        _check_second_difference,
        _check_alternating,
    ]

    for check in checks:
        result = check(sequence)
        if result is not None:
            return {
                "sequence": sequence,
                "detected": True,
                "pattern_name": result["pattern_name"],
                "reasoning": result["reasoning"],
                "next_value": result["next_value"],
            }

    return {
        "sequence": sequence,
        "detected": False,
        "pattern_name": "No standard pattern recognized",
        "reasoning": [
            "The differences, ratios, Fibonacci rule, power sequences, second "
            "differences and alternating sub-sequences were all checked but "
            "none matched consistently.",
            "Try re-checking the sequence, or this may require a custom rule "
            "not covered by the standard aptitude-exam pattern types.",
        ],
        "next_value": None,
    }


def sample_pattern_questions() -> list[dict]:
    return [
        {"question": "2, 4, 8, 16, ?", "sequence": [2, 4, 8, 16]},
        {"question": "3, 6, 9, 12, ?", "sequence": [3, 6, 9, 12]},
        {"question": "1, 1, 2, 3, 5, ?", "sequence": [1, 1, 2, 3, 5]},
        {"question": "1, 4, 9, 16, ?", "sequence": [1, 4, 9, 16]},
        {"question": "2, 6, 12, 20, ?", "sequence": [2, 6, 12, 20]},
        {"question": "1, 3, 2, 6, 3, 9, ?", "sequence": [1, 3, 2, 6, 3, 9]},
    ]
