"""
Application-wide configuration and settings.

This module is responsible ONLY for:
    * Locating project paths
    * Loading environment variables (.env) via python-dotenv
    * Exposing typed, safe accessors for configuration values
    * Defining UI theme constants used across the application

It never prints or logs secret values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = PROJECT_ROOT / "data"
ASSETS_DIR: Path = PROJECT_ROOT / "assets"
ENV_PATH: Path = PROJECT_ROOT / ".env"

# Load environment variables from .env if it exists. This never raises if the
# file is missing -- the application must keep working without it.
load_dotenv(dotenv_path=ENV_PATH, override=False)


@dataclass(frozen=True)
class AISettings:
    """Typed, read-only view of the AI-related configuration."""

    api_key: str | None
    model: str
    base_url: str

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())


def get_ai_settings() -> AISettings:
    """Read AI configuration from environment variables.

    Returns a fresh AISettings snapshot every call so that a user who edits
    their .env file and restarts the app always gets up-to-date values.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip() or None
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    return AISettings(api_key=api_key, model=model, base_url=base_url)


# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "AptiLens"
APP_FULL_NAME = "Aptitude & Data Interpretation Studio"
APP_TAGLINE = "Learn  •  Practice  •  Analyze  •  Improve"
APP_VERSION = "2.0.0"
WINDOW_MIN_WIDTH = 1180
WINDOW_MIN_HEIGHT = 720

# ---------------------------------------------------------------------------
# Theme / color palette (used by src.ui.styles)
# ---------------------------------------------------------------------------
COLOR_PRIMARY = "#4F7DF3"
COLOR_PRIMARY_HOVER = "#3E6AE0"
COLOR_PRIMARY_SOFT = "#1B2A4D"      # subtle accent-tinted surface
COLOR_ACCENT = "#2DD4BF"            # teal highlight
COLOR_SECONDARY = "#0B0F17"         # deepest surface (headers)
COLOR_SUCCESS = "#34D399"
COLOR_SUCCESS_HOVER = "#10B981"
COLOR_WARNING = "#FBBF24"
COLOR_WARNING_HOVER = "#D99A06"
COLOR_DANGER = "#F87171"
COLOR_BACKGROUND = "#0D1117"
COLOR_CARD = "#161B22"
COLOR_SURFACE_ALT = "#1E2633"       # raised surface / secondary buttons
COLOR_SURFACE_HOVER = "#273246"
COLOR_INPUT_BG = "#0F141C"
COLOR_BORDER = "#2A3342"
COLOR_TEXT = "#E6EAF2"
COLOR_TEXT_MUTED = "#8B97AB"
COLOR_INFO_BG = "#12203A"
COLOR_INFO_BORDER = "#25416F"
COLOR_FORMULA = "#9DB7FF"           # formula text
COLOR_SUCCESS_BG = "#0F2A22"
COLOR_SUCCESS_BORDER = "#1D5C45"
COLOR_WARNING_BG = "#2A2310"
COLOR_WARNING_BORDER = "#5C4A12"

THEME_FILE = ASSETS_DIR / "theme" / "aptilens_dark.json"

# Data file locations
SAMPLE_QUESTIONS_FILE = DATA_DIR / "sample_questions.json"
TABULAR_DATA_FILE = DATA_DIR / "tabular_data.csv"
GRAPH_DATA_FILE = DATA_DIR / "graph_data.csv"
CASELET_DATA_FILE = DATA_DIR / "caselet_data.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
