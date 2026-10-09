"""GUI page for the Pattern Recognition module."""

from __future__ import annotations

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.modules.patterns.pattern_logic import analyze_pattern, sample_pattern_questions
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel
from src.utils.validators import validate_non_empty_sequence


class PatternPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._last_result = None
        self._last_sequence: list[float] | None = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "🔢 Pattern Recognition", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset).pack(fill="x", pady=(0, 16))

        form = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        form.pack(fill="x", pady=(0, 16))

        SectionLabel(form, "Enter a number sequence (comma or space separated)").pack(
            anchor="w", padx=16, pady=(16, 6))
        self.seq_entry = ctk.CTkEntry(form, placeholder_text="e.g. 2, 4, 8, 16")
        self.seq_entry.pack(fill="x", padx=16)

        ctk.CTkButton(form, text="Analyze Pattern", command=self._on_analyze,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).pack(anchor="w", padx=16, pady=16)

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        samples_box = ctk.CTkFrame(outer, fg_color="transparent")
        samples_box.pack(fill="x", pady=(18, 0))
        SectionLabel(samples_box, "Sample questions:").pack(anchor="w")
        for q in sample_pattern_questions():
            ctk.CTkLabel(samples_box, text=f"• {q['question']}", font=font(12),
                         text_color=COLORS["text_muted"]).pack(anchor="w", padx=8)

    def _on_analyze(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        try:
            sequence = validate_non_empty_sequence(self.seq_entry.get(), "Sequence")
            result = analyze_pattern(sequence)
        except ValueError as exc:
            self.result_card.clear()
            self.error_banner.show(str(exc))
            self._last_result = None
            return

        self._last_result = result
        self._last_sequence = sequence
        lines = [f"Sequence: {', '.join(str(v) for v in sequence)}",
                 f"Detected pattern: {result['pattern_name']}"] + result["reasoning"]
        answer = str(result["next_value"]) if result["detected"] else "Not determined"
        self.result_card.render(lines, answer)

    def _ai_explain(self) -> dict:
        r, seq = self._last_result, self._last_sequence
        if r is None:
            return {"available": False, "text": "Analyze a sequence first."}
        return default_ai_service.explain_solution(
            module="Pattern Recognition",
            problem=f"Find the next term of the sequence: {', '.join(str(v) for v in seq)}, ?",
            inputs={"Sequence": seq},
            formula=r["pattern_name"],
            verified_result=str(r["next_value"]),
        )

    def reset(self) -> None:
        self.seq_entry.delete(0, "end")
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None
        self._last_sequence = None
