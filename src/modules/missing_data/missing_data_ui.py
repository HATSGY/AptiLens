"""GUI page for the Missing Data Interpretation module."""

from __future__ import annotations

import tkinter.ttk as ttk

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.modules.missing_data.missing_data_logic import (
    sample_missing_data_problems, solve_missing_growth_table,
)
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel


class MissingDataPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self.problems = sample_missing_data_problems()
        self._current = None
        self._last_result: dict | None = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "❓ Missing Data Interpretation", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset).pack(fill="x", pady=(0, 16))

        selector = ctk.CTkFrame(outer, fg_color="transparent")
        selector.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(selector, text="Problem:", font=font(13)).pack(side="left", padx=(0, 8))
        self.problem_menu = ctk.CTkOptionMenu(
            selector, values=[p["title"] for p in self.problems],
            command=self._on_problem_change, width=300)
        self.problem_menu.pack(side="left")

        info_card = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                  border_width=1, border_color=COLORS["border"])
        info_card.pack(fill="x", pady=(0, 16))
        self.desc_label = ctk.CTkLabel(info_card, text="", font=font(13), wraplength=880, justify="left")
        self.desc_label.pack(anchor="w", padx=16, pady=(14, 8))
        self.tree = ttk.Treeview(info_card, columns=("Year", "Value", "Growth %"), show="headings", height=6)
        for col in ("Year", "Value", "Growth %"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")
        self.tree.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkButton(outer, text="Solve Missing Values", command=self._on_solve,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).pack(anchor="w", pady=(0, 16))

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        self._on_problem_change(self.problems[0]["title"])

    def _fill_tree(self, rows: list[dict]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            val = "?" if r["value"] is None else r["value"]
            growth = "-" if r["growth_pct"] is None else f"{r['growth_pct']}%"
            self.tree.insert("", "end", values=(r["year"], val, growth))

    def _on_problem_change(self, title: str) -> None:
        self._current = next(p for p in self.problems if p["title"] == title)
        self.desc_label.configure(text=self._current["description"])
        self._fill_tree(self._current["rows"])
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None

    def _on_solve(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        if self._current is None:
            return
        try:
            result = solve_missing_growth_table(self._current["rows"])
        except ValueError as exc:
            self.result_card.clear()
            self.error_banner.show(str(exc))
            self._last_result = None
            return

        self._fill_tree(result["resolved_rows"])
        lines = [f"Formula: {result['formula']}"] + result["steps"]
        if result["fully_solved"]:
            answer = "All missing values resolved (see table above)."
        else:
            answer = f"Could not resolve: {result['unresolved_years']}"
        self._last_result = {**result, "title": self._current["title"]}
        self.result_card.render(lines, answer)

    def _ai_explain(self) -> dict:
        r = self._last_result
        if r is None:
            return {"available": False, "text": "Solve the problem first."}
        return default_ai_service.explain_solution(
            module="Missing Data Interpretation",
            problem=f"Fill in the missing values for: {r['title']}",
            inputs={"Known rows": self._current["rows"]},
            formula=r["formula"],
            verified_result=str(r["resolved_rows"]),
        )

    def reset(self) -> None:
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None
