"""Reusable CustomTkinter widgets shared across all module pages."""

from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from src.ui.styles import COLORS, font, heading_font


class FeatureCard(ctk.CTkFrame):
    """A clickable dashboard card representing one module (icon chip + hover glow)."""

    def __init__(self, parent, icon: str, title: str, description: str,
                 command: Callable[[], None], badge: str | None = None, wrap: int = 240, **kwargs):
        super().__init__(parent, corner_radius=14, fg_color=COLORS["card"],
                          border_width=1, border_color=COLORS["border"], **kwargs)
        self.command = command

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(18, 0))
        chip = ctk.CTkFrame(top, width=44, height=44, corner_radius=12, fg_color=COLORS["primary_soft"])
        chip.pack(side="left")
        chip.pack_propagate(False)
        icon_label = ctk.CTkLabel(chip, text=icon, font=font(20))
        icon_label.pack(expand=True)
        widgets = [self, top, chip, icon_label]

        if badge:
            badge_label = ctk.CTkLabel(top, text=badge, font=font(10, "bold"), corner_radius=8,
                                        fg_color=COLORS["accent"], text_color="#06201C",
                                        width=44, height=20)
            badge_label.pack(side="right")
            widgets.append(badge_label)

        title_label = ctk.CTkLabel(self, text=title, font=font(15, "bold"),
                                    text_color=COLORS["text"], anchor="w", justify="left", wraplength=wrap)
        title_label.pack(fill="x", padx=18, pady=(12, 0))

        desc_label = ctk.CTkLabel(self, text=description, font=font(12),
                                   text_color=COLORS["text_muted"], anchor="w",
                                   wraplength=wrap, justify="left")
        desc_label.pack(fill="x", padx=18, pady=(4, 8))

        open_label = ctk.CTkLabel(self, text="Open  →", font=font(12, "bold"),
                                   text_color=COLORS["primary"], anchor="w")
        open_label.pack(fill="x", padx=18, pady=(0, 16))
        widgets += [title_label, desc_label, open_label]

        # Clicking anywhere on the card opens it; hovering highlights the border.
        for widget in widgets:
            widget.bind("<Button-1>", lambda _e: command())
            widget.bind("<Enter>", lambda _e: self.configure(border_color=COLORS["primary"]))
            widget.bind("<Leave>", lambda _e: self.configure(border_color=COLORS["border"]))
            try:
                widget.configure(cursor="hand2")
            except Exception:  # noqa: BLE001 - cursor is cosmetic only
                pass


class PageHeader(ctk.CTkFrame):
    """Standard header for every module page: title + Back + Reset."""

    def __init__(self, parent, title: str, on_back: Callable[[], None],
                 on_reset: Callable[[], None] | None = None,
                 extra: tuple[str, Callable[[], None]] | None = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        back_btn = ctk.CTkButton(self, text="←  Dashboard", command=on_back,
                                  fg_color="transparent", text_color=COLORS["text"],
                                  hover_color=COLORS["surface_alt"], corner_radius=8, width=130,
                                  border_width=1, border_color=COLORS["border"])
        back_btn.grid(row=0, column=0, sticky="w")

        title_label = ctk.CTkLabel(self, text=title, font=heading_font(22),
                                    text_color=COLORS["text"])
        title_label.grid(row=0, column=1, padx=20, sticky="w")

        self.grid_columnconfigure(1, weight=1)

        if extra is not None:
            extra_text, extra_cmd = extra
            ctk.CTkButton(self, text=extra_text, command=extra_cmd, corner_radius=8, width=130,
                          fg_color=COLORS["primary_soft"], hover_color=COLORS["info_border"],
                          text_color=COLORS["formula"], border_width=1,
                          border_color=COLORS["info_border"]).grid(row=0, column=2, sticky="e", padx=(0, 8))

        if on_reset is not None:
            reset_btn = ctk.CTkButton(self, text="Reset", command=on_reset,
                                       fg_color=COLORS["surface_alt"], hover_color=COLORS["surface_hover"],
                                       text_color=COLORS["warning"], border_width=1,
                                       border_color=COLORS["border"], corner_radius=8, width=90)
            reset_btn.grid(row=0, column=3, sticky="e")


class ResultCard(ctk.CTkFrame):
    """Displays Input / Formula / Calculation / Answer, and optional steps.

    The card collapses to nothing until there is a result to show, so empty
    pages stay clean.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=12, fg_color="transparent",
                          border_width=0, height=1, **kwargs)
        self._body = ctk.CTkLabel(self, text="", font=font(13), justify="left",
                                   text_color=COLORS["text"], wraplength=760)
        self._answer_label = ctk.CTkLabel(self, text="", font=font(18, "bold"),
                                           text_color=COLORS["success"])
        self._collapse()

    def _collapse(self) -> None:
        self._body.pack_forget()
        self._answer_label.pack_forget()
        self.configure(fg_color="transparent", border_width=0, height=1)
        self.pack_propagate(False)

    def _expand(self) -> None:
        self.pack_propagate(True)
        self.configure(fg_color=COLORS["info_bg"], border_width=1, border_color=COLORS["info_border"])
        self._body.pack(padx=18, pady=16, anchor="w")
        self._answer_label.pack(padx=18, pady=(0, 16), anchor="w")

    def render(self, lines: list[str], answer: str) -> None:
        self._expand()
        self._body.configure(text="\n".join(lines))
        self._answer_label.configure(text=f"✅ Answer: {answer}")

    def clear(self) -> None:
        self._body.configure(text="")
        self._answer_label.configure(text="")
        self._collapse()


class ErrorBanner(ctk.CTkLabel):
    """A small inline error message label, hidden until `.show()` is called."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="", text_color=COLORS["danger"],
                          font=font(12, "bold"), wraplength=760, justify="left", **kwargs)

    def show(self, message: str) -> None:
        self.configure(text=f"⚠ {message}")

    def clear(self) -> None:
        self.configure(text="")


class SectionLabel(ctk.CTkLabel):
    def __init__(self, parent, text: str, **kwargs):
        super().__init__(parent, text=text, font=font(13, "bold"),
                          text_color=COLORS["text"], **kwargs)
