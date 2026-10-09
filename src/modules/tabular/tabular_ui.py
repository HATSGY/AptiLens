"""GUI page for the Tabular Data Interpretation module."""

from __future__ import annotations

import tkinter.ttk as ttk

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.config.settings import TABULAR_DATA_FILE
from src.modules.tabular.tabular_logic import (
    OPERATIONS, apply_operation, label_column, load_tabular_dataset, numeric_columns,
)
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel

_ROW_OPS = {"Percentage of Total", "Ratio (Row A : Row B)",
            "Difference (Row A - Row B)", "Percentage Increase/Decrease (Row A -> Row B)"}
_TWO_ROW_OPS = {"Ratio (Row A : Row B)", "Difference (Row A - Row B)",
                "Percentage Increase/Decrease (Row A -> Row B)"}


class TabularPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._last_result: dict | None = None
        self.df = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "📊 Tabular Data Interpretation", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset).pack(fill="x", pady=(0, 16))

        self.load_error = ErrorBanner(outer)
        self.load_error.pack(fill="x")

        table_frame = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                    border_width=1, border_color=COLORS["border"])
        table_frame.pack(fill="x", pady=(0, 16))
        SectionLabel(table_frame, "Dataset: Quarterly Regional Sales (₹ Lakhs)").pack(
            anchor="w", padx=16, pady=(14, 8))
        self.tree = ttk.Treeview(table_frame, show="headings", height=8)
        self.tree.pack(fill="x", padx=16, pady=(0, 16))

        form = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        form.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(form, text="Operation:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="e")
        self.op_menu = ctk.CTkOptionMenu(form, values=OPERATIONS, command=self._on_operation_change, width=280)
        self.op_menu.grid(row=0, column=1, columnspan=3, pady=(16, 8), sticky="w")

        ctk.CTkLabel(form, text="Column:", font=font(13)).grid(row=1, column=0, padx=(16, 8), pady=8, sticky="e")
        self.col_menu = ctk.CTkOptionMenu(form, values=["-"], width=280)
        self.col_menu.grid(row=1, column=1, columnspan=3, pady=8, sticky="w")

        ctk.CTkLabel(form, text="Row A:", font=font(13)).grid(row=2, column=0, padx=(16, 8), pady=8, sticky="e")
        self.row_a_menu = ctk.CTkOptionMenu(form, values=["-"], width=200)
        self.row_a_menu.grid(row=2, column=1, pady=8, sticky="w")

        self.row_b_label = ctk.CTkLabel(form, text="Row B:", font=font(13))
        self.row_b_label.grid(row=2, column=2, padx=(16, 8), pady=8, sticky="e")
        self.row_b_menu = ctk.CTkOptionMenu(form, values=["-"], width=200)
        self.row_b_menu.grid(row=2, column=3, pady=8, sticky="w")

        ctk.CTkButton(form, text="Calculate", command=self._on_calculate,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=3, column=0, columnspan=4, padx=16, pady=(6, 16), sticky="w")

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        self._load_dataset()

    def _load_dataset(self) -> None:
        try:
            self.df = load_tabular_dataset(TABULAR_DATA_FILE)
        except (FileNotFoundError, ValueError) as exc:
            self.load_error.show(str(exc))
            return

        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        num_cols = numeric_columns(self.df)
        self.col_menu.configure(values=num_cols)
        if num_cols:
            self.col_menu.set(num_cols[0])

        lab_col = label_column(self.df)
        row_labels = [str(v) for v in self.df[lab_col]] if lab_col else [f"Row {i+1}" for i in range(len(self.df))]
        self.row_a_menu.configure(values=row_labels)
        self.row_b_menu.configure(values=row_labels)
        if row_labels:
            self.row_a_menu.set(row_labels[0])
            self.row_b_menu.set(row_labels[-1])

        self.op_menu.set(OPERATIONS[0])
        self._on_operation_change(OPERATIONS[0])

    def _on_operation_change(self, operation: str) -> None:
        show_row_a = operation in _ROW_OPS
        show_row_b = operation in _TWO_ROW_OPS
        state_a = "normal" if show_row_a else "disabled"
        self.row_a_menu.configure(state=state_a)
        if show_row_b:
            self.row_b_menu.grid()
            self.row_b_label.grid()
            self.row_b_menu.configure(state="normal")
        else:
            self.row_b_menu.configure(state="disabled")

    def _on_calculate(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        if self.df is None:
            self.error_banner.show("Dataset failed to load.")
            return
        try:
            operation = self.op_menu.get()
            column = self.col_menu.get()
            lab_col = label_column(self.df)
            row_labels = list(self.df[lab_col]) if lab_col else list(range(len(self.df)))

            row_a_idx = row_labels.index(self._coerce(self.row_a_menu.get(), row_labels)) \
                if operation in _ROW_OPS else None
            row_b_idx = row_labels.index(self._coerce(self.row_b_menu.get(), row_labels)) \
                if operation in _TWO_ROW_OPS else None

            result = apply_operation(self.df, operation, column, row_a_idx, row_b_idx)
        except ValueError as exc:
            self.result_card.clear()
            self.error_banner.show(str(exc))
            self._last_result = None
            return

        self._last_result = result
        lines = [f"Operation: {result['operation']}", f"Column: {result['column']}",
                 f"Formula: {result['formula']}", f"Calculation: {result['calculation']}"]
        self.result_card.render(lines, str(result["answer"]))

    @staticmethod
    def _coerce(value: str, row_labels: list) -> object:
        # row_labels may be strings or ints depending on the dataset's label column
        for candidate in row_labels:
            if str(candidate) == value:
                return candidate
        return value

    def _ai_explain(self) -> dict:
        r = self._last_result
        if r is None:
            return {"available": False, "text": "Run a calculation first."}
        return default_ai_service.explain_solution(
            module="Tabular Data Interpretation",
            problem=f"{r['operation']} of column '{r['column']}'",
            inputs={"Column": r["column"]},
            formula=r["formula"],
            verified_result=str(r["answer"]),
        )

    def reset(self) -> None:
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._last_result = None
