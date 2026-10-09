"""GUI page for the Caselet Data Interpretation module."""

from __future__ import annotations

import tkinter.ttk as ttk

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.config.settings import CASELET_DATA_FILE
from src.modules.caselet.caselet_logic import (
    caselet_dataframe, load_caselets, solve_caselet_question,
)
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel


class CaseletPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self.caselets: list[dict] = []
        self._current_caselet: dict | None = None
        self._last_result: dict | None = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "📚 Caselet Data Interpretation", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset).pack(fill="x", pady=(0, 16))

        self.load_error = ErrorBanner(outer)
        self.load_error.pack(fill="x")

        selector = ctk.CTkFrame(outer, fg_color="transparent")
        selector.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(selector, text="Caselet:", font=font(13)).pack(side="left", padx=(0, 8))
        self.caselet_menu = ctk.CTkOptionMenu(selector, values=["-"], command=self._on_caselet_change, width=380)
        self.caselet_menu.pack(side="left")

        self.paragraph_card = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                            border_width=1, border_color=COLORS["border"])
        self.paragraph_card.pack(fill="x", pady=(0, 16))
        self.title_label = ctk.CTkLabel(self.paragraph_card, text="", font=font(16, "bold"),
                                         text_color=COLORS["text"])
        self.title_label.pack(anchor="w", padx=16, pady=(14, 4))
        self.paragraph_label = ctk.CTkLabel(self.paragraph_card, text="", font=font(13),
                                             wraplength=880, justify="left")
        self.paragraph_label.pack(anchor="w", padx=16, pady=(0, 10))
        self.tree = ttk.Treeview(self.paragraph_card, show="headings", height=6)
        self.tree.pack(fill="x", padx=16, pady=(0, 16))

        q_frame = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                border_width=1, border_color=COLORS["border"])
        q_frame.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(q_frame, text="Question:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=16, sticky="e")
        self.question_menu = ctk.CTkOptionMenu(q_frame, values=["-"], width=520)
        self.question_menu.grid(row=0, column=1, pady=16, sticky="w")
        ctk.CTkButton(q_frame, text="Solve", command=self._on_solve,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=0, column=2, padx=16, pady=16)

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        self._load_caselets()

    def _load_caselets(self) -> None:
        try:
            self.caselets = load_caselets(CASELET_DATA_FILE)
        except (FileNotFoundError, ValueError) as exc:
            self.load_error.show(str(exc))
            return
        titles = [c["title"] for c in self.caselets]
        self.caselet_menu.configure(values=titles)
        self.caselet_menu.set(titles[0])
        self._on_caselet_change(titles[0])

    def _on_caselet_change(self, title: str) -> None:
        self._current_caselet = next(c for c in self.caselets if c["title"] == title)
        self.title_label.configure(text=self._current_caselet["title"])
        self.paragraph_label.configure(text=self._current_caselet["paragraph"])

        df = caselet_dataframe(self._current_caselet).reset_index()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        questions = [q["text"] for q in self._current_caselet["questions"]]
        self.question_menu.configure(values=questions)
        self.question_menu.set(questions[0])
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None

    def _on_solve(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        if self._current_caselet is None:
            return
        q_text = self.question_menu.get()
        question = next(q for q in self._current_caselet["questions"] if q["text"] == q_text)
        try:
            result = solve_caselet_question(self._current_caselet, question)
        except ValueError as exc:
            self.result_card.clear()
            self.error_banner.show(str(exc))
            self._last_result = None
            return
        self._last_result = {**result, "question_text": q_text}
        lines = [f"Question: {q_text}", f"Formula: {result['formula']}",
                 f"Calculation: {result['calculation']}"]
        self.result_card.render(lines, str(result["answer"]))

    def _ai_explain(self) -> dict:
        r = self._last_result
        if r is None:
            return {"available": False, "text": "Solve a question first."}
        return default_ai_service.explain_solution(
            module="Caselet Data Interpretation",
            problem=r["question_text"],
            inputs={"Caselet": self._current_caselet["title"]},
            formula=r["formula"],
            verified_result=str(r["answer"]),
        )

    def reset(self) -> None:
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None
