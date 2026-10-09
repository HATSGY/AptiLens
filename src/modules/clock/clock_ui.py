"""GUI page for the Clock Problems module."""

from __future__ import annotations

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.modules.clock.clock_logic import calculate_clock_angle, sample_clock_questions
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel
from src.utils.validators import validate_hour_minute


class ClockPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._last_result = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "🕐 Clock Problems", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset,
                   extra=("📘 Concepts", lambda: controller_show("concepts", category="Clock"))).pack(fill="x", pady=(0, 16))

        form = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        form.pack(fill="x", pady=(0, 16))

        SectionLabel(form, "Find the angle between the hour and minute hands").grid(
            row=0, column=0, columnspan=4, padx=16, pady=(16, 8), sticky="w")

        ctk.CTkLabel(form, text="Hour (1-12):", font=font(13)).grid(row=1, column=0, padx=(16, 8), pady=10, sticky="e")
        self.hour_entry = ctk.CTkEntry(form, width=90, placeholder_text="e.g. 3")
        self.hour_entry.grid(row=1, column=1, pady=10, sticky="w")

        ctk.CTkLabel(form, text="Minute (0-59):", font=font(13)).grid(row=1, column=2, padx=(16, 8), pady=10, sticky="e")
        self.minute_entry = ctk.CTkEntry(form, width=90, placeholder_text="e.g. 20")
        self.minute_entry.grid(row=1, column=3, pady=10, sticky="w")

        calc_btn = ctk.CTkButton(form, text="Calculate", command=self._on_calculate,
                                  fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                  corner_radius=8)
        calc_btn.grid(row=2, column=0, columnspan=4, padx=16, pady=(4, 16), sticky="w")

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))

        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))

        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        samples_box = ctk.CTkFrame(outer, fg_color="transparent")
        samples_box.pack(fill="x", pady=(18, 0))
        SectionLabel(samples_box, "Sample competitive-exam questions:").pack(anchor="w")
        for q in sample_clock_questions():
            ctk.CTkLabel(samples_box, text=f"• {q['question']}", font=font(12),
                         text_color=COLORS["text_muted"]).pack(anchor="w", padx=8)

    def _on_calculate(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        try:
            hour, minute = validate_hour_minute(self.hour_entry.get(), self.minute_entry.get())
            result = calculate_clock_angle(hour, minute)
        except ValueError as exc:
            self.result_card.clear()
            self.error_banner.show(str(exc))
            self._last_result = None
            return

        self._last_result = result
        lines = [
            f"Input: Hour = {result.hour}, Minute = {result.minute}",
            f"Formula: {result.formula}",
            f"Substitution: {result.substitution}",
        ] + result.steps
        self.result_card.render(lines, f"{result.angle}° (smaller angle)")

    def _ai_explain(self) -> dict:
        r = self._last_result
        if r is None:
            return {"available": False, "text": "Calculate a result first."}
        return default_ai_service.explain_solution(
            module="Clock Problems",
            problem=f"Find the angle between the hands of a clock at {r.hour}:{r.minute:02d}.",
            inputs={"Hour": r.hour, "Minute": r.minute},
            formula=r.formula,
            verified_result=f"{r.angle}° (smaller angle), {r.reflex_angle}° (reflex angle)",
        )

    def reset(self) -> None:
        self.hour_entry.delete(0, "end")
        self.minute_entry.delete(0, "end")
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None
