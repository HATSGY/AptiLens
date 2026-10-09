"""GUI page for Performance Analysis (aggregated across all Practice sessions)."""

from __future__ import annotations

import customtkinter as ctk

from src.analytics.performance import (
    aggregate_topic_stats, build_accuracy_by_topic_chart,
    build_attempted_by_topic_chart, load_sessions, overall_stats,
)
from src.config.settings import SESSIONS_FILE
from src.ui.styles import COLORS, font, heading_font
from src.ui.widgets import PageHeader, SectionLabel
from src.utils.chart_utils import close_figure, embed_figure


class PerformancePage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._canvases: list = []
        self._figs: list = []

        self.outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        self.outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(self.outer, "📉 Performance Analysis", on_back=lambda: controller_show("dashboard"),
                   on_reset=self._render).pack(fill="x", pady=(0, 16))

        self.stats_grid = ctk.CTkFrame(self.outer, fg_color="transparent")
        self.stats_grid.pack(fill="x", pady=(0, 16))

        self.charts_frame = ctk.CTkFrame(self.outer, fg_color="transparent")
        self.charts_frame.pack(fill="x")

        self.empty_label = ctk.CTkLabel(
            self.outer, text="No practice sessions recorded yet. Complete a Practice Mode "
                             "session to see your performance analytics here.",
            font=font(13), text_color=COLORS["text_muted"])

    def on_show(self, **_kwargs) -> None:
        self._render()

    def _clear(self) -> None:
        for w in self.stats_grid.winfo_children():
            w.destroy()
        for w in self.charts_frame.winfo_children():
            w.destroy()
        for fig in self._figs:
            close_figure(fig)
        self._figs = []
        self._canvases = []
        self.empty_label.pack_forget()

    def _render(self) -> None:
        self._clear()
        sessions = load_sessions(SESSIONS_FILE)
        if not sessions:
            self.empty_label.pack(pady=40)
            return

        stats = overall_stats(sessions)
        cards = [
            ("Sessions Completed", stats["sessions_completed"]),
            ("Total Questions", stats["total_questions"]),
            ("Overall Accuracy", f"{stats['accuracy_percent']}%"),
            ("Average Time / Question", f"{stats['average_time']}s"),
        ]
        for i, (label, value) in enumerate(cards):
            box = ctk.CTkFrame(self.stats_grid, corner_radius=10, fg_color=COLORS["card"],
                                border_width=1, border_color=COLORS["border"])
            box.grid(row=0, column=i, padx=8, sticky="nsew")
            self.stats_grid.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(box, text=str(value), font=font(20, "bold"),
                         text_color=COLORS["primary"]).pack(pady=(14, 0))
            ctk.CTkLabel(box, text=label, font=font(12), text_color=COLORS["text_muted"]).pack(pady=(0, 14))

        topic_stats = aggregate_topic_stats(sessions)
        SectionLabel(self.charts_frame, "Topic-wise Performance").pack(anchor="w", pady=(10, 6))

        chart_row = ctk.CTkFrame(self.charts_frame, fg_color="transparent")
        chart_row.pack(fill="x")
        chart_row.grid_columnconfigure(0, weight=1)
        chart_row.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(chart_row, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        left.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        right = ctk.CTkFrame(chart_row, corner_radius=12, fg_color=COLORS["card"],
                              border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        fig1 = build_accuracy_by_topic_chart(topic_stats)
        fig2 = build_attempted_by_topic_chart(topic_stats)
        self._figs.extend([fig1, fig2])
        self._canvases.append(embed_figure(left, fig1))
        self._canvases.append(embed_figure(right, fig2))
