"""GUI page for the Calendar Problems module."""

from __future__ import annotations

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.modules.calendar.calendar_logic import (
    calculate_day_of_week, days_between_dates, is_leap_year, shift_day,
)
from src.ui.ai_panel import AIPanel
from src.ui.styles import COLORS, font
from src.ui.widgets import ErrorBanner, PageHeader, ResultCard, SectionLabel
from src.utils.validators import validate_date, validate_int_in_range


def _date_row(parent, row: int, label_prefix: str = "Date") -> tuple[ctk.CTkEntry, ctk.CTkEntry, ctk.CTkEntry]:
    ctk.CTkLabel(parent, text=f"{label_prefix} (DD / MM / YYYY):", font=font(13)).grid(
        row=row, column=0, padx=(16, 8), pady=10, sticky="e")
    d = ctk.CTkEntry(parent, width=60, placeholder_text="DD")
    d.grid(row=row, column=1, sticky="w")
    m = ctk.CTkEntry(parent, width=60, placeholder_text="MM")
    m.grid(row=row, column=2, padx=6, sticky="w")
    y = ctk.CTkEntry(parent, width=80, placeholder_text="YYYY")
    y.grid(row=row, column=3, sticky="w")
    return d, m, y


class CalendarPage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self._last_context: dict | None = None

        outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(outer, "📅 Calendar Problems", on_back=lambda: controller_show("dashboard"),
                   on_reset=self.reset,
                   extra=("📘 Concepts", lambda: controller_show("concepts", category="Calendar"))).pack(fill="x", pady=(0, 16))

        self.tabs = ctk.CTkTabview(outer, corner_radius=12, fg_color=COLORS["card"])
        self.tabs.pack(fill="x", pady=(0, 16))
        for name in ("Day of Week", "Leap Year", "Date Difference", "Add / Subtract Days"):
            self.tabs.add(name)

        self._build_day_of_week_tab(self.tabs.tab("Day of Week"))
        self._build_leap_year_tab(self.tabs.tab("Leap Year"))
        self._build_difference_tab(self.tabs.tab("Date Difference"))
        self._build_shift_tab(self.tabs.tab("Add / Subtract Days"))

        self.error_banner = ErrorBanner(outer)
        self.error_banner.pack(fill="x", pady=(0, 6))
        self.result_card = ResultCard(outer)
        self.result_card.pack(fill="x", pady=(0, 6))
        self.ai_panel = AIPanel(outer, fetch_callback=self._ai_explain)
        self.ai_panel.pack(fill="x")

    # ---- Tab builders -------------------------------------------------
    def _build_day_of_week_tab(self, tab) -> None:
        SectionLabel(tab, "Find the day of the week for a date").grid(
            row=0, column=0, columnspan=4, padx=16, pady=(12, 4), sticky="w")
        self.dow_d, self.dow_m, self.dow_y = _date_row(tab, 1)
        ctk.CTkButton(tab, text="Calculate", command=self._on_day_of_week,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=2, column=0, columnspan=4, padx=16, pady=(6, 16), sticky="w")

    def _build_leap_year_tab(self, tab) -> None:
        SectionLabel(tab, "Check whether a year is a leap year").grid(
            row=0, column=0, columnspan=2, padx=16, pady=(12, 4), sticky="w")
        ctk.CTkLabel(tab, text="Year:", font=font(13)).grid(row=1, column=0, padx=(16, 8), pady=10, sticky="e")
        self.leap_year_entry = ctk.CTkEntry(tab, width=100, placeholder_text="e.g. 2024")
        self.leap_year_entry.grid(row=1, column=1, sticky="w")
        ctk.CTkButton(tab, text="Check", command=self._on_leap_year,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=2, column=0, columnspan=2, padx=16, pady=(6, 16), sticky="w")

    def _build_difference_tab(self, tab) -> None:
        SectionLabel(tab, "Days between two dates").grid(
            row=0, column=0, columnspan=4, padx=16, pady=(12, 4), sticky="w")
        self.diff_d1, self.diff_m1, self.diff_y1 = _date_row(tab, 1, "Date A")
        self.diff_d2, self.diff_m2, self.diff_y2 = _date_row(tab, 2, "Date B")
        ctk.CTkButton(tab, text="Calculate", command=self._on_days_between,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=3, column=0, columnspan=4, padx=16, pady=(6, 16), sticky="w")

    def _build_shift_tab(self, tab) -> None:
        SectionLabel(tab, "Find the date N days before/after a given date").grid(
            row=0, column=0, columnspan=4, padx=16, pady=(12, 4), sticky="w")
        self.shift_d, self.shift_m, self.shift_y = _date_row(tab, 1)
        ctk.CTkLabel(tab, text="Offset (+/- days):", font=font(13)).grid(
            row=2, column=0, padx=(16, 8), pady=10, sticky="e")
        self.shift_offset = ctk.CTkEntry(tab, width=100, placeholder_text="e.g. 45 or -10")
        self.shift_offset.grid(row=2, column=1, sticky="w")
        ctk.CTkButton(tab, text="Calculate", command=self._on_shift,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
                      ).grid(row=3, column=0, columnspan=4, padx=16, pady=(6, 16), sticky="w")

    # ---- Handlers -------------------------------------------------------
    def _reset_result(self) -> None:
        self.error_banner.clear()
        self.result_card.clear()
        self.ai_panel.reset()
        self._last_context = None

    def _on_day_of_week(self) -> None:
        self._reset_result()
        try:
            date = validate_date(self.dow_d.get(), self.dow_m.get(), self.dow_y.get())
            result = calculate_day_of_week(date.day, date.month, date.year)
        except ValueError as exc:
            self.error_banner.show(str(exc))
            return
        self.result_card.render(
            [f"Input: {result['day']:02d}-{result['month']:02d}-{result['year']}",
             f"Formula: {result['formula']}"] + result["steps"],
            result["weekday"],
        )
        self._last_context = {
            "module": "Calendar - Day of Week",
            "problem": f"What day of the week was {result['day']:02d}-{result['month']:02d}-{result['year']}?",
            "inputs": {"Day": result["day"], "Month": result["month"], "Year": result["year"]},
            "formula": result["formula"],
            "verified_result": result["weekday"],
        }

    def _on_leap_year(self) -> None:
        self._reset_result()
        try:
            year = validate_int_in_range(self.leap_year_entry.get(), 1, 9999, "Year")
            result = is_leap_year(year)
        except ValueError as exc:
            self.error_banner.show(str(exc))
            return
        self.result_card.render(
            [f"Input: Year = {result['year']}", f"Rule: {result['reason']}"],
            "Leap Year" if result["is_leap"] else "Not a Leap Year",
        )
        self._last_context = {
            "module": "Calendar - Leap Year",
            "problem": f"Is {year} a leap year?",
            "inputs": {"Year": year},
            "formula": "Divisible by 4 (and not by 100 unless also by 400)",
            "verified_result": "Leap Year" if result["is_leap"] else "Not a Leap Year",
        }

    def _on_days_between(self) -> None:
        self._reset_result()
        try:
            d1 = validate_date(self.diff_d1.get(), self.diff_m1.get(), self.diff_y1.get())
            d2 = validate_date(self.diff_d2.get(), self.diff_m2.get(), self.diff_y2.get())
            result = days_between_dates(d1.day, d1.month, d1.year, d2.day, d2.month, d2.year)
        except ValueError as exc:
            self.error_banner.show(str(exc))
            return
        self.result_card.render(
            [f"Date A: {result['date1']}", f"Date B: {result['date2']}"] + result["steps"],
            f"{result['days_between']} days",
        )
        self._last_context = {
            "module": "Calendar - Date Difference",
            "problem": f"How many days between {result['date1']} and {result['date2']}?",
            "inputs": {"Date A": result["date1"], "Date B": result["date2"]},
            "formula": "Difference = |JDN(Date B) - JDN(Date A)|",
            "verified_result": f"{result['days_between']} days",
        }

    def _on_shift(self) -> None:
        self._reset_result()
        try:
            date = validate_date(self.shift_d.get(), self.shift_m.get(), self.shift_y.get())
            offset = validate_int_in_range(self.shift_offset.get(), -3650, 3650, "Offset")
            result = shift_day(date.day, date.month, date.year, offset)
        except ValueError as exc:
            self.error_banner.show(str(exc))
            return
        self.result_card.render(
            [f"Original date: {result['original_date']}", f"Offset: {result['offset']} day(s)",
             result["explanation"]],
            result["result_date"],
        )
        self._last_context = {
            "module": "Calendar - Add/Subtract Days",
            "problem": result["explanation"],
            "inputs": {"Date": result["original_date"], "Offset": result["offset"]},
            "formula": "Result JDN = Original JDN + Offset, converted back to a calendar date",
            "verified_result": result["result_date"],
        }

    def _ai_explain(self) -> dict:
        ctx = self._last_context
        if ctx is None:
            return {"available": False, "text": "Calculate a result first."}
        return default_ai_service.explain_solution(**ctx)

    def reset(self) -> None:
        for entry in (self.dow_d, self.dow_m, self.dow_y, self.leap_year_entry,
                      self.diff_d1, self.diff_m1, self.diff_y1,
                      self.diff_d2, self.diff_m2, self.diff_y2,
                      self.shift_d, self.shift_m, self.shift_y, self.shift_offset):
            entry.delete(0, "end")
        self._reset_result()
