"""
Reusable prompt templates for the AI Study Assistant.

IMPORTANT DESIGN RULE: every prompt built here embeds a verified, already-
calculated result from the Core Logic Layer. The AI is asked to EXPLAIN
that result, never to derive it independently. If the AI's own reasoning
ever disagrees with the supplied numbers, the system prompt instructs it
to flag the inconsistency rather than silently override the answer.
"""

from __future__ import annotations

SYSTEM_PROMPT = """You are a competitive-exam aptitude tutor helping a student \
preparing for exams such as CAT, GATE, banking, GRE/GMAT and UPSC/MPSC-style \
aptitude sections.

Explain concepts in simple, student-friendly language. Do not unnecessarily \
complicate the mathematics.

When you are given a problem together with a verified, already-calculated \
solution, explain the reasoning step by step (state the formula, substitute \
the values, show the calculation, interpret the result). Do NOT override or \
silently change the application's verified numerical result.

If the supplied calculation appears inconsistent or you notice a possible \
error in it, explicitly point out the inconsistency rather than silently \
producing a different final answer.

Keep explanations concise: prefer short paragraphs and, where useful, a \
numbered list of steps."""


def build_explain_solution_prompt(module: str, problem: str, inputs: dict,
                                   formula: str, verified_result: str) -> str:
    inputs_str = "\n".join(f"  - {k}: {v}" for k, v in inputs.items())
    return (
        f"Module: {module}\n"
        f"Problem: {problem}\n"
        f"Inputs:\n{inputs_str}\n"
        f"Formula: {formula}\n"
        f"Verified calculated result: {verified_result}\n\n"
        f"Task: Explain this solution simply and step by step for a student. "
        f"Do not change the verified result."
    )


def build_hint_prompt(module: str, problem: str, difficulty: str) -> str:
    return (
        f"Module: {module}\n"
        f"Problem: {problem}\n"
        f"Difficulty: {difficulty}\n\n"
        f"Task: Give the student ONE short hint that nudges them toward the "
        f"right method, WITHOUT revealing the final numerical answer."
    )


def build_formula_prompt(module: str, formula_name: str) -> str:
    return (
        f"Module: {module}\n"
        f"Task: Explain the formula '{formula_name}' in simple terms: what it "
        f"means, when it is used in competitive exams, and a short generic "
        f"example of applying it (use made-up sample numbers, not the "
        f"student's current problem)."
    )


def build_graph_analysis_prompt(graph_type: str, verified_stats: dict) -> str:
    stats_str = "\n".join(f"  - {k}: {v}" for k, v in verified_stats.items())
    return (
        f"Graph type: {graph_type}\n"
        f"Verified statistics computed locally from the data:\n{stats_str}\n\n"
        f"Task: Turn these verified statistics into a short, student-friendly "
        f"interpretation of what the graph shows. Do not invent numbers that "
        f"are not listed above."
    )


def build_similar_question_prompt(module: str, original_problem: str, difficulty: str) -> str:
    return (
        f"Module: {module}\n"
        f"Original problem (for style/topic reference only): {original_problem}\n"
        f"Difficulty: {difficulty}\n\n"
        f"Task: Generate ONE new, similar practice question on the same topic "
        f"and difficulty, with different numbers. Provide the question, then "
        f"on a new line starting with 'Answer:' give the final answer, and "
        f"then a short worked explanation."
    )


def build_simplify_prompt(text_to_simplify: str) -> str:
    return (
        f"The following explanation was too difficult for a student to follow:\n"
        f"\"{text_to_simplify}\"\n\n"
        f"Task: Rewrite it in much simpler language, using a short everyday "
        f"analogy if it helps, while keeping the same final result."
    )


def build_why_correct_prompt(module: str, problem: str, answer: str) -> str:
    return (
        f"Module: {module}\n"
        f"Problem: {problem}\n"
        f"Verified correct answer: {answer}\n\n"
        f"Task: Explain WHY this answer is correct, addressing the most "
        f"common mistake students make on this type of question."
    )
