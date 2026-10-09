"""GUI page for the Concepts Library (Clock + Calendar theory)."""

from __future__ import annotations

import customtkinter as ctk

from src.modules.concepts.concepts_data import CATEGORIES, Topic, search_topics
from src.ui.styles import COLORS, font, heading_font, mono_font
from src.ui.widgets import PageHeader

SIDEBAR_WIDTH = 310
WRAP = 700

SOLVER_LABELS = {"clock": "Clock", "calendar": "Calendar", "tabular": "Tabular Data",
                 "graphs": "Graph Analysis", "caselet": "Caselet", "missing_data": "Missing Data"}


class ConceptsPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self.category = "Clock"
        self.query = ""
        self.current: Topic = CATEGORIES[self.category][0]

        PageHeader(self, "📘 Concepts Library", on_back=lambda: controller_show("dashboard")
                   ).pack(fill="x", padx=24, pady=(20, 12))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_sidebar(body)

        self.content = ctk.CTkScrollableFrame(body, fg_color=COLORS["background"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=(16, 0))

        # Labels that should re-wrap when the window is resized: (label, horizontal offset)
        self._width = 780
        self._wrapped: list[tuple[ctk.CTkLabel, int]] = []
        self.content._parent_canvas.bind("<Configure>", self._on_resize, add="+")

        self._refresh_list()
        self._render_topic()

    # ------------------------------------------------------------------ sidebar
    def _build_sidebar(self, body) -> None:
        side = ctk.CTkFrame(body, width=SIDEBAR_WIDTH, corner_radius=14, fg_color=COLORS["card"],
                            border_width=1, border_color=COLORS["border"])
        side.grid(row=0, column=0, sticky="ns")
        side.grid_propagate(False)
        side.pack_propagate(False)

        self.segment = ctk.CTkSegmentedButton(side, values=list(CATEGORIES.keys()),
                                              command=self._on_category, height=34)
        self.segment.set(self.category)
        self.segment.pack(fill="x", padx=14, pady=(14, 8))

        self.search = ctk.CTkEntry(side, placeholder_text="Search concepts...", height=34)
        self.search.pack(fill="x", padx=14, pady=(0, 8))
        self.search.bind("<KeyRelease>", self._on_search)

        self.counter = ctk.CTkLabel(side, text="", font=font(11), text_color=COLORS["text_muted"], anchor="w")
        self.counter.pack(fill="x", padx=18, pady=(0, 2))

        self.list_frame = ctk.CTkScrollableFrame(side, fg_color="transparent", corner_radius=0)
        self.list_frame.pack(fill="both", expand=True, padx=6, pady=(0, 8))

    def _visible_topics(self) -> list[tuple[str, Topic]]:
        if self.query:
            return search_topics(self.query)
        return [(self.category, t) for t in CATEGORIES[self.category]]

    def _refresh_list(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()
        items = self._visible_topics()
        label = "results" if self.query else f"{self.category} topics"
        self.counter.configure(text=f"{len(items)} {label}")
        if not items:
            ctk.CTkLabel(self.list_frame, text="No concept matches your search.", font=font(12),
                         text_color=COLORS["text_muted"]).pack(padx=10, pady=20)
            return
        for cat, topic in items:
            selected = topic.key == self.current.key
            prefix = f"{cat[:3].upper()} · " if self.query else ""
            btn = ctk.CTkButton(
                self.list_frame, text=f"{prefix}{topic.title}", anchor="w", height=42,
                font=font(12, "bold" if selected else "normal"), corner_radius=8,
                fg_color=COLORS["primary_soft"] if selected else "transparent",
                text_color=COLORS["formula"] if selected else COLORS["text"],
                hover_color=COLORS["surface_alt"],
                command=lambda c=cat, t=topic: self._select(c, t),
            )
            try:  # let long titles wrap onto a second line
                btn._text_label.configure(wraplength=SIDEBAR_WIDTH - 70, justify="left")
            except Exception:  # noqa: BLE001 - purely cosmetic
                pass
            btn.pack(fill="x", padx=4, pady=1)

    # ------------------------------------------------------------------ events
    def _on_category(self, value: str) -> None:
        self.category = value
        self.query = ""
        self._clear_search()
        self.current = CATEGORIES[value][0]
        self._refresh_list()
        self._render_topic()

    def _clear_search(self) -> None:
        if self.search.get():
            self.search.delete(0, "end")

    def _on_search(self, _event=None) -> None:
        self.query = self.search.get().strip()
        self._refresh_list()

    def _select(self, category: str, topic: Topic) -> None:
        self.category = category
        self.segment.set(category)
        self.current = topic
        self._refresh_list()
        self._render_topic()

    def on_show(self, category: str | None = None, topic_key: str | None = None, **_kwargs) -> None:
        """Called by the NavigationController each time the page is raised."""
        if category in CATEGORIES:
            self.category = category
            self.segment.set(category)
            self.query = ""
            self._clear_search()
            known = {t.key for t in CATEGORIES[category]}
            if self.current.key not in known or topic_key:
                self.current = CATEGORIES[category][0]
        if topic_key:
            for t in CATEGORIES[self.category]:
                if t.key == topic_key:
                    self.current = t
        self._refresh_list()
        self._render_topic()

    # ------------------------------------------------------------------ responsive text
    def _on_resize(self, event) -> None:
        if abs(event.width - self._width) < 12:
            return
        self._width = event.width
        self._apply_wrap()

    def _apply_wrap(self) -> None:
        alive = []
        for label, offset in self._wrapped:
            try:
                if label.winfo_exists():
                    label.configure(wraplength=max(320, self._width - offset))
                    alive.append((label, offset))
            except Exception:  # noqa: BLE001 - widget destroyed mid-update
                pass
        self._wrapped = alive

    def _lbl(self, parent, text: str, offset: int, **kwargs) -> ctk.CTkLabel:
        """Create a label whose wraplength follows the page width (minus `offset`)."""
        label = ctk.CTkLabel(parent, text=text, wraplength=max(320, self._width - offset), **kwargs)
        self._wrapped.append((label, offset))
        return label

    # ------------------------------------------------------------------ content
    def _card(self, parent, fg=None, border=None, **kw) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent, corner_radius=12, fg_color=fg or COLORS["card"],
                            border_width=1, border_color=border or COLORS["border"], **kw)

    def _section(self, text: str) -> None:
        row = ctk.CTkFrame(self.content, fg_color="transparent")
        row.pack(fill="x", pady=(20, 8))
        ctk.CTkFrame(row, width=4, height=18, corner_radius=2, fg_color=COLORS["primary"]).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(row, text=text.upper(), font=font(12, "bold"), text_color=COLORS["text_muted"]).pack(side="left")

    def _render_topic(self) -> None:
        t = self.current
        for child in self.content.winfo_children():
            child.destroy()
        self._wrapped = []
        try:
            self.content._parent_canvas.yview_moveto(0)
        except Exception:  # noqa: BLE001
            pass

        topics = CATEGORIES[self.category]
        pos = next((i for i, x in enumerate(topics) if x.key == t.key), 0)

        # ---- title block
        ctk.CTkLabel(self.content, text=f"{self.category.upper()}   ›   TOPIC {pos + 1} OF {len(topics)}",
                     font=font(11, "bold"), text_color=COLORS["accent"], anchor="w").pack(fill="x", pady=(4, 2))
        self._lbl(self.content, t.title, 24, font=heading_font(26), text_color=COLORS["text"],
                  anchor="w", justify="left").pack(fill="x")
        self._lbl(self.content, t.summary, 24, font=font(13), text_color=COLORS["text_muted"],
                  anchor="w", justify="left").pack(fill="x", pady=(6, 0))

        # ---- key ideas
        self._section("Key ideas")
        card = self._card(self.content)
        card.pack(fill="x")
        for i, line in enumerate(t.points):
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=(14 if i == 0 else 4, 14 if i == len(t.points) - 1 else 0))
            ctk.CTkLabel(row, text="•", font=font(14, "bold"), text_color=COLORS["primary"],
                         width=14).pack(side="left", anchor="n")
            self._lbl(row, line, 90, font=font(13), text_color=COLORS["text"], anchor="w",
                      justify="left").pack(side="left", fill="x", expand=True)

        # ---- optional table
        if t.table:
            self._render_table(t)

        # ---- formulas
        self._section("Formulas")
        for label, expr in t.formulas:
            box = self._card(self.content, fg=COLORS["info_bg"], border=COLORS["info_border"])
            box.pack(fill="x", pady=(0, 8))
            ctk.CTkFrame(box, width=4, height=1, corner_radius=0, fg_color=COLORS["primary"]).pack(side="left", fill="y")
            inner = ctk.CTkFrame(box, fg_color="transparent")
            inner.pack(side="left", fill="x", expand=True, padx=16, pady=12)
            ctk.CTkLabel(inner, text=label.upper(), font=font(10, "bold"), text_color=COLORS["text_muted"],
                         anchor="w").pack(fill="x")
            self._lbl(inner, expr, 90, font=mono_font(14, "bold"), text_color=COLORS["formula"],
                      anchor="w", justify="left").pack(fill="x", pady=(3, 0))

        # ---- worked examples
        self._section("Worked examples")
        for n, ex in enumerate(t.examples, start=1):
            self._render_example(n, ex)

        # ---- tip
        if t.tip:
            tip = self._card(self.content, fg=COLORS["warning_bg"], border=COLORS["warning_border"])
            tip.pack(fill="x", pady=(14, 0))
            ctk.CTkLabel(tip, text="💡  EXAM TIP", font=font(11, "bold"), text_color=COLORS["warning"],
                         anchor="w").pack(fill="x", padx=18, pady=(12, 2))
            self._lbl(tip, t.tip, 70, font=font(13), text_color=COLORS["text"], anchor="w",
                      justify="left").pack(fill="x", padx=18, pady=(0, 14))

        # ---- footer navigation
        nav = ctk.CTkFrame(self.content, fg_color="transparent")
        nav.pack(fill="x", pady=(22, 10))
        prev_t = topics[pos - 1] if pos > 0 else None
        next_t = topics[pos + 1] if pos < len(topics) - 1 else None
        ghost = dict(fg_color="transparent", border_width=1, border_color=COLORS["border"],
                     text_color=COLORS["text"], hover_color=COLORS["surface_alt"], height=36)
        if prev_t:
            ctk.CTkButton(nav, text="←  Previous", width=120, command=lambda: self._select(self.category, prev_t),
                          **ghost).pack(side="left")
        if next_t:
            ctk.CTkButton(nav, text="Next  →", width=120, command=lambda: self._select(self.category, next_t),
                          **ghost).pack(side="right")
        if t.solver:
            ctk.CTkButton(nav, text=f"Try it in the {SOLVER_LABELS.get(t.solver, t.solver)} solver  →", height=36,
                          command=lambda: self.controller_show(t.solver)).pack(side="right", padx=10)

    def _render_table(self, t: Topic) -> None:
        self._section(t.table_title or "Reference table")
        card = ctk.CTkFrame(self.content, corner_radius=12, fg_color=COLORS["border"],
                            border_width=1, border_color=COLORS["border"])
        card.pack(fill="x")
        header, *rows = t.table
        ncols = len(header)
        for c in range(ncols):  # wider columns for longer text
            longest = max(len(r[c]) for r in t.table)
            card.grid_columnconfigure(c, weight=max(1, min(5, longest // 8)), uniform="")

        def cell(r: int, c: int, text: str, bg: str, fg: str, bold: bool) -> None:
            box = ctk.CTkFrame(card, corner_radius=0, fg_color=bg, height=1)
            box.grid(row=r, column=c, sticky="nsew", padx=(0 if c == 0 else 1, 0), pady=(0 if r == 0 else 1, 0))
            ctk.CTkLabel(box, text=text, font=font(12, "bold" if bold else "normal"), text_color=fg,
                         anchor="w", justify="left", wraplength=(WRAP // ncols) + 120 if c else (WRAP // ncols) - 24
                         ).pack(fill="x", padx=14, pady=8)

        for c, text in enumerate(header):
            cell(0, c, text, COLORS["info_bg"], COLORS["formula"], True)
        for r, row in enumerate(rows, start=1):
            bg = COLORS["card"] if r % 2 else COLORS["surface_alt"]
            for c, text in enumerate(row):
                cell(r, c, text, bg, COLORS["text"], False)

    def _render_example(self, n: int, ex) -> None:
        card = self._card(self.content)
        card.pack(fill="x", pady=(0, 10))
        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(14, 0))
        ctk.CTkLabel(head, text=f"EXAMPLE {n}", font=font(10, "bold"), text_color="#06201C",
                     fg_color=COLORS["accent"], corner_radius=6, width=78, height=20).pack(side="left")
        self._lbl(card, ex.problem, 70, font=font(14, "bold"), text_color=COLORS["text"],
                  anchor="w", justify="left").pack(fill="x", padx=18, pady=(8, 6))
        for step in ex.steps:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=1)
            ctk.CTkLabel(row, text="›", font=font(13, "bold"), text_color=COLORS["text_muted"],
                         width=14).pack(side="left", anchor="n")
            self._lbl(row, step, 90, font=font(13), text_color=COLORS["text_muted"], anchor="w",
                      justify="left").pack(side="left", fill="x", expand=True)
        ans = ctk.CTkFrame(card, corner_radius=8, fg_color=COLORS["success_bg"],
                           border_width=1, border_color=COLORS["success_border"])
        ans.pack(fill="x", padx=18, pady=(10, 16))
        self._lbl(ans, f"✓  Answer:  {ex.answer}", 100, font=font(13, "bold"), text_color=COLORS["success"],
                  anchor="w", justify="left").pack(fill="x", padx=14, pady=8)
