"""
Main application window.

Creates exactly ONE CTk root window and a single container Frame in which
every "page" is stacked (see NavigationController). No module ever creates
its own Tk()/CTk() root -- this is what keeps navigation centralized and
consistent across the whole application.
"""

from __future__ import annotations

import customtkinter as ctk

from src.analytics.performance_ui import PerformancePage
from src.config import settings
from src.modules.calendar.calendar_ui import CalendarPage
from src.modules.caselet.caselet_ui import CaseletPage
from src.modules.clock.clock_ui import ClockPage
from src.modules.concepts.concepts_ui import ConceptsPage
from src.modules.graphs.graph_ui import GraphPage
from src.modules.missing_data.missing_data_ui import MissingDataPage
from src.modules.patterns.pattern_ui import PatternPage
from src.modules.tabular.tabular_ui import TabularPage
from src.practice.practice_ui import PracticePage
from src.ui.about_page import AboutPage
from src.ui.ai_assistant_page import AIAssistantPage
from src.ui.dashboard import Dashboard
from src.ui.navigation import NavigationController
from src.ui.styles import apply_theme


class AptiLensApp(ctk.CTk):
    def report_callback_exception(self, exc, val, tb) -> None:  # noqa: D401
        """Ignore CustomTkinter's harmless 'widget already destroyed' redraw race.

        When a page rebuilds its content (destroying frames), a queued <Configure>
        event can still reach a frame whose canvas is gone. That is a known
        CustomTkinter quirk and has no effect on the user, so we skip printing it.
        Every other exception is reported normally.
        """
        if isinstance(val, AttributeError) and "winfo_exists" in str(val):
            return
        super().report_callback_exception(exc, val, tb)

    def __init__(self) -> None:
        super().__init__()
        apply_theme()

        self.title(f"{settings.APP_NAME} — {settings.APP_FULL_NAME}")
        self.minsize(settings.WINDOW_MIN_WIDTH, settings.WINDOW_MIN_HEIGHT)
        self.geometry(f"{settings.WINDOW_MIN_WIDTH}x{settings.WINDOW_MIN_HEIGHT}")

        container = ctk.CTkFrame(self, fg_color=settings.COLOR_BACKGROUND)
        container.pack(fill="both", expand=True)

        self.nav = NavigationController(container)

        def show(name: str, **kwargs) -> None:
            self.nav.show(name, **kwargs)

        pages = {
            "dashboard": Dashboard(container, show),
            "concepts": ConceptsPage(container, show),
            "clock": ClockPage(container, show),
            "calendar": CalendarPage(container, show),
            "patterns": PatternPage(container, show),
            "tabular": TabularPage(container, show),
            "graphs": GraphPage(container, show),
            "caselet": CaseletPage(container, show),
            "missing_data": MissingDataPage(container, show),
            "ai_assistant": AIAssistantPage(container, show),
            "practice": PracticePage(container, show),
            "performance": PerformancePage(container, show),
            "about": AboutPage(container, show),
        }
        for name, frame in pages.items():
            self.nav.register(name, frame)

        self.nav.show("dashboard")


def run() -> None:
    app = AptiLensApp()
    app.mainloop()
