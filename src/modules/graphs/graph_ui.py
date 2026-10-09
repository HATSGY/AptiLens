"""GUI page for the Graph Analysis module (Bar / Pie / Line / Scatter / Histogram)."""

from __future__ import annotations

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.config.settings import GRAPH_DATA_FILE
from src.modules.graphs.graph_logic import (
    SAMPLE_HISTOGRAM_SCORES, analyze_bar, analyze_histogram, analyze_line,
    analyze_pie, analyze_scatter, load_graph_dataset,
)
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel
from src.utils.chart_utils import close_figure, embed_figure, new_figure

GRAPH_TYPES = ["Bar Graph", "Pie Chart", "Line Graph", "Scatter Diagram", "Histogram"]


class GraphPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._canvas = None
        self._current_fig = None
        self._analysis: dict | None = None
        self._graph_type: str | None = None
        self.df = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "📈 Graph Analysis", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset).pack(fill="x", pady=(0, 16))

        self.load_error = ErrorBanner(outer)
        self.load_error.pack(fill="x")

        controls = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                 border_width=1, border_color=COLORS["border"])
        controls.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(controls, text="Graph Type:", font=font(13)).grid(row=0, column=0, padx=(16, 8), pady=16, sticky="e")
        self.type_menu = ctk.CTkOptionMenu(controls, values=GRAPH_TYPES, width=220)
        self.type_menu.grid(row=0, column=1, pady=16, sticky="w")
        ctk.CTkButton(controls, text="Generate Graph", command=self._on_generate,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=0, column=2, padx=12, pady=16)
        ctk.CTkButton(controls, text="Analyze Graph", command=self._on_analyze,
                      fg_color=COLORS["success"], hover_color=COLORS["success_hover"]
                      ).grid(row=0, column=3, padx=(0, 16), pady=16)

        self.chart_frame = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                         border_width=1, border_color=COLORS["border"], height=440)
        self.chart_frame.pack_propagate(False)
        self.chart_frame.pack(fill="x", pady=(0, 16))
        self.chart_placeholder = ctk.CTkLabel(
            self.chart_frame, text="Select a graph type and click 'Generate Graph'.",
            font=font(13), text_color=COLORS["text_muted"])
        self.chart_placeholder.pack(pady=60)

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

        self._load_dataset()

    def _load_dataset(self) -> None:
        try:
            self.df = load_graph_dataset(GRAPH_DATA_FILE)
        except (FileNotFoundError, ValueError) as exc:
            self.load_error.show(str(exc))

    def _clear_chart(self) -> None:
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None
        if self._current_fig is not None:
            close_figure(self._current_fig)
            self._current_fig = None
        self.chart_placeholder.pack_forget()

    def _on_generate(self) -> None:
        self.error_banner.clear()
        self.result_card.clear()
        self.ai_panel.reset()
        self._analysis = None
        if self.df is None:
            self.error_banner.show("Dataset failed to load.")
            return

        graph_type = self.type_menu.get()
        self._graph_type = graph_type
        self._clear_chart()
        fig, ax = new_figure()

        months = self.df["Month"].tolist()
        revenue = self.df["Revenue"].tolist()

        if graph_type == "Bar Graph":
            ax.bar(months, revenue, color=COLORS["primary"])
            ax.set_title("Monthly Revenue (₹ Lakhs)")
            ax.set_ylabel("Revenue")
        elif graph_type == "Pie Chart":
            ax.pie(revenue, labels=months, autopct="%1.1f%%", startangle=90)
            ax.set_title("Revenue Share by Month")
        elif graph_type == "Line Graph":
            ax.plot(months, revenue, marker="o", color=COLORS["primary"])
            ax.set_title("Revenue Trend Over Time")
            ax.set_ylabel("Revenue")
        elif graph_type == "Scatter Diagram":
            spend = self.df["Marketing_Spend"].tolist()
            ax.scatter(spend, revenue, color=COLORS["primary"])
            ax.set_title("Marketing Spend vs Revenue")
            ax.set_xlabel("Marketing Spend (₹ Lakhs)")
            ax.set_ylabel("Revenue (₹ Lakhs)")
        elif graph_type == "Histogram":
            ax.hist(SAMPLE_HISTOGRAM_SCORES, bins=6, color=COLORS["primary"], edgecolor=COLORS["card"])
            ax.set_title("Distribution of Aptitude Test Scores (40 students)")
            ax.set_xlabel("Score")
            ax.set_ylabel("Number of Students")

        fig.tight_layout()
        self._current_fig = fig
        self._canvas = embed_figure(self.chart_frame, fig)

    def _on_analyze(self) -> None:
        self.error_banner.clear()
        self.ai_panel.reset()
        if self._graph_type is None or self.df is None:
            self.error_banner.show("Generate a graph first.")
            return

        months = self.df["Month"].tolist()
        revenue = self.df["Revenue"].tolist()

        if self._graph_type == "Bar Graph":
            result = analyze_bar(months, revenue)
            lines = [f"Highest: {result['highest']['category']} ({result['highest']['value']})",
                     f"Lowest: {result['lowest']['category']} ({result['lowest']['value']})",
                     f"Difference (highest - lowest): {result['difference_highest_lowest']}",
                     f"% change ({months[0]} -> {months[-1]}): {result['percentage_change_first_to_last']}%",
                     f"Average: {result['average']}"]
            answer = f"Highest = {result['highest']['category']}, Lowest = {result['lowest']['category']}"

        elif self._graph_type == "Pie Chart":
            result = analyze_pie(months, revenue)
            lines = [f"Total: {result['total']}"] + [
                f"{b['category']}: {b['percentage']}% (value {b['value']})" for b in result["sector_breakdown"]
            ]
            answer = f"Largest sector = {result['largest_sector']['category']} " \
                     f"({result['largest_sector']['percentage']}%)"

        elif self._graph_type == "Line Graph":
            result = analyze_line(months, revenue)
            lines = [f"Maximum: {result['maximum']['point']} ({result['maximum']['value']})",
                     f"Minimum: {result['minimum']['point']} ({result['minimum']['value']})",
                     f"Overall change: {result['overall_change']} ({result['overall_percentage_change']}%)",
                     f"Trend: {result['trend']}"]
            answer = result["trend"]

        elif self._graph_type == "Scatter Diagram":
            spend = self.df["Marketing_Spend"].tolist()
            result = analyze_scatter(spend, revenue)
            lines = [f"Correlation coefficient (r): {result['correlation_coefficient']}",
                     f"Relationship: {result['relationship']}",
                     f"Regression line: {result['regression_line']}"]
            answer = f"r = {result['correlation_coefficient']} ({result['relationship']})"

        else:  # Histogram
            result = analyze_histogram(SAMPLE_HISTOGRAM_SCORES, num_bins=6)
            lines = [f"Intervals: {result['intervals']}",
                     f"Frequencies: {result['frequencies']}",
                     f"Highest-frequency interval: {result['highest_frequency_interval']} "
                     f"({result['highest_frequency']} students)",
                     f"Mean: {result['mean']}, Median: {result['median']}, Std Dev: {result['std_dev']}"]
            answer = f"Most common interval = {result['highest_frequency_interval']}"

        self._analysis = result
        self.result_card.render(lines, answer)

    def _ai_explain(self) -> dict:
        if self._analysis is None:
            return {"available": False, "text": "Analyze the graph first."}
        return default_ai_service.analyze_graph(self._graph_type, self._analysis)

    def reset(self) -> None:
        self._clear_chart()
        self.chart_placeholder.pack(pady=60)
        self.result_card.clear()
        self.error_banner.clear()
        self.ai_panel.reset()
        self._analysis = None
        self._graph_type = None
