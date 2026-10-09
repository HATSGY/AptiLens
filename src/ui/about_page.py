"""About / User Guide page."""

from __future__ import annotations

import customtkinter as ctk

from src.config import settings
from src.ui.styles import COLORS, font, heading_font
from src.ui.widgets import PageHeader, SectionLabel

GUIDE_TEXT = """\
1. Concepts Library — Learn every Clock and Calendar concept with formulas, worked \
examples and exam tips. Choose Clock or Calendar, pick a topic (or search), then jump \
straight to the matching solver.

2. Clock Problems — Enter an hour and minute to see the formula, step-by-step \
substitution and the verified angle between the hands.

3. Calendar Problems — Use the tabs to find a day of the week, check a leap \
year, compute the days between two dates, or shift a date by N days.

4. Pattern Recognition — Type a number sequence to detect its underlying \
rule (arithmetic, geometric, Fibonacci-like, quadratic, alternating, ...).

5. Tabular Data Interpretation — Explore the sample dataset and compute \
sums, averages, ratios, differences and percentage changes.

6. Graph Analysis — Generate a Bar / Pie / Line / Scatter / Histogram chart, \
then click Analyze Graph for verified statistics.

7. Caselet Data Interpretation — Read a short business scenario and solve \
its data-driven questions.

8. Missing Data Interpretation — Recover missing table values from growth, \
average, ratio or total relationships.

9. AI Study Assistant — Ask for a step-by-step explanation, a hint, a \
formula explanation, a similar practice question, or a simplified version \
of a difficult explanation.

10. Practice Mode — Choose topics/difficulty, answer timed MCQ/numerical \
questions, and get instant scoring with an AI hint option.

11. Performance Analysis — Review your accuracy and speed across topics, \
aggregated across every Practice Mode session you have completed.

AI Configuration — Copy .env.example to .env and set OPENAI_API_KEY (and \
optionally OPENAI_MODEL / OPENAI_BASE_URL). Without a key, every "Explain \
with AI" feature shows a friendly unavailable message, but ALL core solving \
features keep working normally.
"""


class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "ℹ️ User Guide / About", on_back=lambda: controller_show("dashboard")
                   ).pack(fill="x", pady=(0, 16))

        card = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(card, text=settings.APP_NAME, font=heading_font(26),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=(20, 0))
        ctk.CTkLabel(card, text=settings.APP_FULL_NAME, font=font(14),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(0, 12))
        ctk.CTkLabel(card, text="Purpose: To provide an interactive environment for learning and "
                                 "practicing aptitude and data interpretation concepts.",
                     font=font(13), wraplength=860, justify="left").pack(anchor="w", padx=20, pady=(0, 6))
        ctk.CTkLabel(card, text="Technology: Python, CustomTkinter, Pandas, NumPy, Matplotlib, "
                                 "python-dotenv, and an OpenAI-compatible AI API.",
                     font=font(13), wraplength=860, justify="left").pack(anchor="w", padx=20, pady=(0, 6))
        ctk.CTkLabel(card, text=f"Version: {settings.APP_VERSION}", font=font(12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=20, pady=(0, 4))
        ctk.CTkLabel(card, text="Team Members: [Add your name(s) here]\nCollege: [Add your college]\n"
                                 "Department: [Add your department]\nAcademic Year: [Add academic year]",
                     font=font(12), text_color=COLORS["text_muted"], justify="left"
                     ).pack(anchor="w", padx=20, pady=(0, 20))

        guide_card = ctk.CTkFrame(outer, corner_radius=12, fg_color=COLORS["card"],
                                   border_width=1, border_color=COLORS["border"])
        guide_card.pack(fill="x")
        SectionLabel(guide_card, "How to use each module").pack(anchor="w", padx=20, pady=(16, 6))
        ctk.CTkLabel(guide_card, text=GUIDE_TEXT, font=font(12), justify="left",
                     wraplength=860, text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(0, 20))
