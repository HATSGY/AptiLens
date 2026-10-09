"""
Standalone "AI Study Assistant" page.

Lets the student interact with the AI layer directly (independent of any
particular module's solved result) for: explaining a solution, getting a
hint, explaining a formula, generating a similar practice question,
simplifying a difficult explanation, and explaining why an answer is
correct. Graph-insight explanations are handled inline on the Graph
Analysis page itself, since they require the page's already-computed stats.
"""

from __future__ import annotations

import threading
from typing import Callable

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.config.settings import get_ai_settings
from src.ui.styles import COLORS, font
from src.ui.widgets import PageHeader, SectionLabel

MODULES = ["Clock", "Calendar", "Patterns", "Tabular DI", "Graph Analysis",
           "Caselet DI", "Missing Data", "General Aptitude"]


def _run_async(button: ctk.CTkButton, output: ctk.CTkTextbox, task: Callable[[], dict]) -> None:
    button.configure(state="disabled")
    output.configure(state="normal")
    output.delete("1.0", "end")
    output.insert("1.0", "🤖 Thinking...")
    output.configure(state="disabled")

    def worker() -> None:
        try:
            result = task()
        except Exception as exc:  # noqa: BLE001
            result = {"available": False, "text": f"AI explanation is currently unavailable ({exc})."}

        def finish() -> None:
            button.configure(state="normal")
            output.configure(state="normal")
            output.delete("1.0", "end")
            prefix = "🤖 " if result.get("available") else "ℹ️  "
            output.insert("1.0", prefix + result.get("text", ""))
            output.configure(state="disabled")

        button.after(0, finish)

    threading.Thread(target=worker, daemon=True).start()


class AIAssistantPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "🤖 AI Study Assistant", on_back=lambda: controller_show("dashboard")
                   ).pack(fill="x", pady=(0, 10))

        self.status_label = ctk.CTkLabel(outer, text="", font=font(12, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 14))

        self.tabs = ctk.CTkTabview(outer, corner_radius=12, fg_color=COLORS["card"])
        self.tabs.pack(fill="both", expand=True)
        for name in ("Explain a Solution", "Give a Hint", "Explain a Formula",
                     "Similar Question", "Simplify", "Why Correct"):
            self.tabs.add(name)

        self._build_explain_tab(self.tabs.tab("Explain a Solution"))
        self._build_hint_tab(self.tabs.tab("Give a Hint"))
        self._build_formula_tab(self.tabs.tab("Explain a Formula"))
        self._build_similar_tab(self.tabs.tab("Similar Question"))
        self._build_simplify_tab(self.tabs.tab("Simplify"))
        self._build_why_tab(self.tabs.tab("Why Correct"))

    def on_show(self, **_kwargs) -> None:
        settings = get_ai_settings()
        if settings.is_configured:
            self.status_label.configure(
                text=f"✅ AI Assistant is configured (model: {settings.model}).",
                text_color=COLORS["success"])
        else:
            self.status_label.configure(
                text="ℹ️  AI Assistant is currently unavailable — please configure your API key "
                     "in .env. Core solving features are still fully functional.",
                text_color=COLORS["warning"])

    # ---- Shared helpers -------------------------------------------------
    @staticmethod
    def _labeled_entry(parent, row: int, label: str, width: int = 500, placeholder: str = "") -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, font=font(13)).grid(row=row, column=0, padx=(16, 8), pady=8, sticky="ne")
        entry = ctk.CTkEntry(parent, width=width, placeholder_text=placeholder)
        entry.grid(row=row, column=1, pady=8, sticky="w")
        return entry

    @staticmethod
    def _output_box(parent) -> ctk.CTkTextbox:
        box = ctk.CTkTextbox(parent, height=180, corner_radius=10, fg_color=COLORS["input_bg"], wrap="word", font=font(13))
        box.configure(state="disabled")
        return box

    # ---- Tabs -------------------------------------------------------------
    def _build_explain_tab(self, tab) -> None:
        module = ctk.CTkOptionMenu(tab, values=MODULES, width=220)
        ctk.CTkLabel(tab, text="Module:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        module.grid(row=0, column=1, pady=(16, 8), sticky="w")
        problem = self._labeled_entry(tab, 1, "Problem:", placeholder="e.g. Find the angle at 3:20")
        formula = self._labeled_entry(tab, 2, "Formula:", placeholder="e.g. |30H - 5.5M|")
        result = self._labeled_entry(tab, 3, "Verified result:", placeholder="e.g. 20 degrees")
        output = self._output_box(tab)
        output.grid(row=5, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Get Explanation", fg_color=COLORS["surface_alt"])
        btn.grid(row=4, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(btn, output, lambda: default_ai_service.explain_solution(
            module=module.get(), problem=problem.get() or "N/A", inputs={},
            formula=formula.get() or "N/A", verified_result=result.get() or "N/A")))

    def _build_hint_tab(self, tab) -> None:
        module = ctk.CTkOptionMenu(tab, values=MODULES, width=220)
        ctk.CTkLabel(tab, text="Module:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        module.grid(row=0, column=1, pady=(16, 8), sticky="w")
        problem = self._labeled_entry(tab, 1, "Problem:", placeholder="Describe the question you're stuck on")
        difficulty = ctk.CTkOptionMenu(tab, values=["Easy", "Medium", "Hard"], width=140)
        ctk.CTkLabel(tab, text="Difficulty:", font=font(13)).grid(row=2, column=0, padx=(16, 8), pady=8, sticky="e")
        difficulty.grid(row=2, column=1, pady=8, sticky="w")
        output = self._output_box(tab)
        output.grid(row=4, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Get Hint", fg_color=COLORS["surface_alt"])
        btn.grid(row=3, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(btn, output, lambda: default_ai_service.generate_hint(
            module=module.get(), problem=problem.get() or "N/A", difficulty=difficulty.get())))

    def _build_formula_tab(self, tab) -> None:
        module = ctk.CTkOptionMenu(tab, values=MODULES, width=220)
        ctk.CTkLabel(tab, text="Module:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        module.grid(row=0, column=1, pady=(16, 8), sticky="w")
        formula_name = self._labeled_entry(tab, 1, "Formula name:", placeholder="e.g. Zeller's Congruence")
        output = self._output_box(tab)
        output.grid(row=3, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Explain Formula", fg_color=COLORS["surface_alt"])
        btn.grid(row=2, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(btn, output, lambda: default_ai_service.explain_formula(
            module=module.get(), formula_name=formula_name.get() or "N/A")))

    def _build_similar_tab(self, tab) -> None:
        module = ctk.CTkOptionMenu(tab, values=MODULES, width=220)
        ctk.CTkLabel(tab, text="Module:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        module.grid(row=0, column=1, pady=(16, 8), sticky="w")
        original = self._labeled_entry(tab, 1, "Original problem:", placeholder="e.g. 2, 4, 8, 16, ?")
        difficulty = ctk.CTkOptionMenu(tab, values=["Easy", "Medium", "Hard"], width=140)
        ctk.CTkLabel(tab, text="Difficulty:", font=font(13)).grid(row=2, column=0, padx=(16, 8), pady=8, sticky="e")
        difficulty.grid(row=2, column=1, pady=8, sticky="w")
        output = self._output_box(tab)
        output.grid(row=4, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Generate Similar Question", fg_color=COLORS["surface_alt"])
        btn.grid(row=3, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(btn, output, lambda: default_ai_service.generate_similar_question(
            module=module.get(), original_problem=original.get() or "N/A", difficulty=difficulty.get())))

    def _build_simplify_tab(self, tab) -> None:
        SectionLabel(tab, "Paste an explanation that was too difficult to follow:").grid(
            row=0, column=0, columnspan=2, padx=16, pady=(16, 6), sticky="w")
        text_box = ctk.CTkTextbox(tab, height=100, corner_radius=8)
        text_box.grid(row=1, column=0, columnspan=2, padx=16, pady=(0, 8), sticky="nsew")
        output = self._output_box(tab)
        output.grid(row=3, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Simplify", fg_color=COLORS["surface_alt"])
        btn.grid(row=2, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(
            btn, output, lambda: default_ai_service.simplify_explanation(text_box.get("1.0", "end").strip() or "N/A")))

    def _build_why_tab(self, tab) -> None:
        module = ctk.CTkOptionMenu(tab, values=MODULES, width=220)
        ctk.CTkLabel(tab, text="Module:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        module.grid(row=0, column=1, pady=(16, 8), sticky="w")
        problem = self._labeled_entry(tab, 1, "Problem:")
        answer = self._labeled_entry(tab, 2, "Verified answer:")
        output = self._output_box(tab)
        output.grid(row=4, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="nsew")
        btn = ctk.CTkButton(tab, text="Explain Why Correct", fg_color=COLORS["surface_alt"])
        btn.grid(row=3, column=0, columnspan=2, padx=16, pady=(6, 10), sticky="w")
        btn.configure(command=lambda: _run_async(btn, output, lambda: default_ai_service.explain_why_correct(
            module=module.get(), problem=problem.get() or "N/A", answer=answer.get() or "N/A")))
