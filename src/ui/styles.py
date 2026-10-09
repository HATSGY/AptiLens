"""Central dark theme definition so every page looks consistent."""

from __future__ import annotations

import customtkinter as ctk

from src.config import settings

FONT_FAMILY = "Segoe UI"
MONO_FAMILY = "Consolas"


def apply_theme() -> None:
    """Force dark appearance and load the AptiLens colour theme."""
    ctk.set_appearance_mode("dark")
    if settings.THEME_FILE.exists():
        ctk.set_default_color_theme(str(settings.THEME_FILE))
    else:  # graceful fallback if the theme file is missing
        ctk.set_default_color_theme("blue")


def font(size: int = 14, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


def heading_font(size: int = 24) -> ctk.CTkFont:
    return font(size=size, weight="bold")


def mono_font(size: int = 13, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=MONO_FAMILY, size=size, weight=weight)


COLORS = {
    "primary": settings.COLOR_PRIMARY,
    "primary_hover": settings.COLOR_PRIMARY_HOVER,
    "primary_soft": settings.COLOR_PRIMARY_SOFT,
    "accent": settings.COLOR_ACCENT,
    "secondary": settings.COLOR_SECONDARY,
    "success": settings.COLOR_SUCCESS,
    "success_hover": settings.COLOR_SUCCESS_HOVER,
    "warning": settings.COLOR_WARNING,
    "warning_hover": settings.COLOR_WARNING_HOVER,
    "danger": settings.COLOR_DANGER,
    "background": settings.COLOR_BACKGROUND,
    "card": settings.COLOR_CARD,
    "surface_alt": settings.COLOR_SURFACE_ALT,
    "surface_hover": settings.COLOR_SURFACE_HOVER,
    "input_bg": settings.COLOR_INPUT_BG,
    "border": settings.COLOR_BORDER,
    "text": settings.COLOR_TEXT,
    "text_muted": settings.COLOR_TEXT_MUTED,
    "info_bg": settings.COLOR_INFO_BG,
    "info_border": settings.COLOR_INFO_BORDER,
    "formula": settings.COLOR_FORMULA,
    "success_bg": settings.COLOR_SUCCESS_BG,
    "success_border": settings.COLOR_SUCCESS_BORDER,
    "warning_bg": settings.COLOR_WARNING_BG,
    "warning_border": settings.COLOR_WARNING_BORDER,
}
