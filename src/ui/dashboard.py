"""The main dashboard: the first screen the user sees."""

from __future__ import annotations

import customtkinter as ctk

from src.config import settings
from src.modules.concepts.concepts_data import CATEGORIES
from src.ui.styles import COLORS, font, heading_font
from src.ui.widgets import FeatureCard

# (section title, section subtitle, [(icon, title, description, page, page kwargs, badge)])
SECTIONS = [
    ("Learn", "Build the theory first — formulas, derivations and worked examples.", [
        ("🕐", "Clock Concepts",
         f"{len(CATEGORIES['Clock'])} topics: hand angles, overlaps, mirror images, fast & slow clocks and more.",
         "concepts", {"category": "Clock"}, "NEW"),
        ("📅", "Calendar Concepts",
         f"{len(CATEGORIES['Calendar'])} topics: odd days, leap years, Zeller, Doomsday, repeating calendars and more.",
         "concepts", {"category": "Calendar"}, "NEW"),
    ]),
    ("Aptitude Solvers", "Step-by-step solvers backed by verified algorithms.", [
        ("🕐", "Clock Problems", "Angle between hands, reflex angle, time-for-angle.", "clock", {}, None),
        ("📅", "Calendar Problems", "Day of week, leap years, date differences.", "calendar", {}, None),
        ("🔢", "Pattern Recognition", "Detect number series and predict the next term.", "patterns", {}, None),
    ]),
    ("Data Interpretation", "Read tables, charts and caselets like an exam topper.", [
        ("📊", "Tabular Data", "Sum, average, ratio, percentage change and more.", "tabular", {}, None),
        ("📈", "Graph Analysis", "Bar, pie, line, scatter & histogram interpretation.", "graphs", {}, None),
        ("📚", "Caselet DI", "Read a caselet, then answer DI questions.", "caselet", {}, None),
        ("❓", "Missing Data", "Recover missing table values algorithmically.", "missing_data", {}, None),
    ]),
    ("Practice & Insights", "Test yourself, get help, and track your progress.", [
        ("📝", "Practice Mode", "Timed MCQ & numerical practice with instant scoring.", "practice", {}, None),
        ("📉", "Performance", "Accuracy and speed analytics across topics.", "performance", {}, None),
        ("🤖", "AI Study Assistant", "Explanations, hints and practice questions.", "ai_assistant", {}, None),
        ("ℹ️", "User Guide / About", "About this project and how to use it.", "about", {}, None),
    ]),
]

COLS = 4


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show

        header = ctk.CTkFrame(self, fg_color=COLORS["secondary"], corner_radius=0,
                               border_width=0)
        header.pack(fill="x")
        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(fill="x", padx=36, pady=(26, 22))

        logo = ctk.CTkFrame(inner, width=58, height=58, corner_radius=16, fg_color=COLORS["primary"])
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="A", font=heading_font(30), text_color="#FFFFFF").pack(expand=True)

        titles = ctk.CTkFrame(inner, fg_color="transparent")
        titles.pack(side="left", padx=16)
        ctk.CTkLabel(titles, text=settings.APP_NAME, font=heading_font(30),
                     text_color=COLORS["text"], anchor="w").pack(anchor="w")
        ctk.CTkLabel(titles, text=settings.APP_FULL_NAME, font=font(13),
                     text_color=COLORS["text_muted"], anchor="w").pack(anchor="w")

        ctk.CTkLabel(inner, text=settings.APP_TAGLINE, font=font(12, "bold"),
                     text_color=COLORS["accent"]).pack(side="right")
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"], corner_radius=0).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        scroll.pack(fill="both", expand=True, padx=24, pady=(8, 16))

        for title, subtitle, items in SECTIONS:
            head = ctk.CTkFrame(scroll, fg_color="transparent")
            head.pack(fill="x", padx=10, pady=(18, 2))
            ctk.CTkLabel(head, text=title, font=heading_font(17), text_color=COLORS["text"]).pack(side="left")
            ctk.CTkLabel(head, text=f"   {subtitle}", font=font(12),
                         text_color=COLORS["text_muted"]).pack(side="left", pady=(3, 0))

            grid = ctk.CTkFrame(scroll, fg_color="transparent")
            grid.pack(fill="x")
            for col in range(COLS):
                grid.grid_columnconfigure(col, weight=1, uniform="card")
            for i, (icon, name, desc, page, kwargs, badge) in enumerate(items):
                row, col = divmod(i, COLS)
                card = FeatureCard(grid, icon, name, desc, badge=badge,
                                   command=lambda p=page, k=kwargs: self.controller_show(p, **k))
                card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
