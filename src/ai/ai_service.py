"""
High-level AI operations used by the GUI.

This is the ONLY module the UI layer should import from `src.ai`. Every
public function here returns a plain dict:

    {"available": bool, "text": str}

`available` is False whenever the AI could not be reached for any reason
(no API key, no internet, timeout, API error, empty response, ...); `text`
then holds a friendly fallback message instead of a traceback. The GUI can
therefore always safely display `result["text"]` without extra error
handling of its own.

The AI is never used to compute a numeric result: every function here takes
an already-verified result from a core logic module and asks the AI only to
explain/hint/simplify/generate practice content around it.
"""

from __future__ import annotations

from src.ai import ai_prompts
from src.ai.ai_client import AIClient, AIUnavailableError

_FALLBACK_UNAVAILABLE = (
    "AI Assistant is currently unavailable. "
    "Core solving features are still fully functional."
)


class AIService:
    """High-level AI operations, backed by an injectable AIClient.

    Accepting a client in the constructor (instead of importing/creating
    one deep inside each function) is what makes this class trivially
    mockable in tests -- no real API key or network access is required to
    unit test the fallback behaviour.
    """

    def __init__(self, client: AIClient | None = None) -> None:
        self.client = client or AIClient()

    @property
    def is_available(self) -> bool:
        return self.client.is_available

    def _run(self, user_prompt: str, max_tokens: int = 500) -> dict:
        try:
            text = self.client.chat(ai_prompts.SYSTEM_PROMPT, user_prompt, max_tokens=max_tokens)
            return {"available": True, "text": text}
        except AIUnavailableError as exc:
            return {"available": False, "text": str(exc) or _FALLBACK_UNAVAILABLE}

    # ---- Public operations -------------------------------------------------
    def explain_solution(self, module: str, problem: str, inputs: dict,
                          formula: str, verified_result: str) -> dict:
        prompt = ai_prompts.build_explain_solution_prompt(
            module, problem, inputs, formula, verified_result
        )
        return self._run(prompt, max_tokens=550)

    def generate_hint(self, module: str, problem: str, difficulty: str = "Medium") -> dict:
        prompt = ai_prompts.build_hint_prompt(module, problem, difficulty)
        return self._run(prompt, max_tokens=180)

    def explain_formula(self, module: str, formula_name: str) -> dict:
        prompt = ai_prompts.build_formula_prompt(module, formula_name)
        return self._run(prompt, max_tokens=400)

    def analyze_graph(self, graph_type: str, verified_stats: dict) -> dict:
        prompt = ai_prompts.build_graph_analysis_prompt(graph_type, verified_stats)
        return self._run(prompt, max_tokens=400)

    def generate_similar_question(self, module: str, original_problem: str,
                                   difficulty: str = "Medium") -> dict:
        prompt = ai_prompts.build_similar_question_prompt(module, original_problem, difficulty)
        return self._run(prompt, max_tokens=350)

    def simplify_explanation(self, text_to_simplify: str) -> dict:
        prompt = ai_prompts.build_simplify_prompt(text_to_simplify)
        return self._run(prompt, max_tokens=350)

    def explain_why_correct(self, module: str, problem: str, answer: str) -> dict:
        prompt = ai_prompts.build_why_correct_prompt(module, problem, answer)
        return self._run(prompt, max_tokens=350)


# A module-level singleton for convenient use from simple UI callbacks.
# UI code may also construct its own AIService() if it needs a fresh client
# (e.g. after the user edits their .env and restarts a settings dialog).
default_ai_service = AIService()
