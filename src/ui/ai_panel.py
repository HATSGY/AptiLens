"""
Reusable "Explain with AI" panel.

Used by every module page after a result has been calculated. The AI call
runs on a background thread so the network request never freezes the GUI;
the result is then marshalled back onto the Tkinter main thread with
`.after(...)`, which is the officially supported way to update widgets from
a non-GUI thread in Tkinter.
"""

from __future__ import annotations

import threading
from typing import Callable

import customtkinter as ctk

from src.ui.styles import COLORS, font


class AIPanel(ctk.CTkFrame):
    def __init__(self, parent, fetch_callback: Callable[[], dict],
                 button_text: str = "🤖  Explain with AI", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.fetch_callback = fetch_callback

        self.button = ctk.CTkButton(
            self, text=button_text, command=self._on_click,
            fg_color=COLORS["surface_alt"], hover_color=COLORS["surface_hover"],
            corner_radius=8, height=36,
        )
        self.button.pack(anchor="w", pady=(10, 6))

        self.output = ctk.CTkTextbox(self, height=140, corner_radius=10,
                                      fg_color=COLORS["input_bg"], wrap="word",
                                      font=font(13))
        self.output.configure(state="disabled")
        # Hidden until first use to keep the page compact.

    def _set_output(self, text: str, available: bool) -> None:
        self.output.pack(fill="x", pady=(0, 10))
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        prefix = "🤖 AI Explanation:\n\n" if available else "ℹ️  "
        self.output.insert("1.0", prefix + text)
        self.output.configure(state="disabled")

    def _on_click(self) -> None:
        self.button.configure(state="disabled", text="Thinking...")
        self._set_output("Contacting AI Study Assistant...", available=True)

        def worker() -> None:
            try:
                result = self.fetch_callback()
            except Exception as exc:  # noqa: BLE001 - never let a stray error crash the GUI
                result = {"available": False,
                          "text": f"AI explanation is currently unavailable ({exc})."}
            self.after(0, lambda: self._finish(result))

        threading.Thread(target=worker, daemon=True).start()

    def _finish(self, result: dict) -> None:
        self.button.configure(state="normal", text="🤖  Explain with AI")
        self._set_output(result.get("text", ""), result.get("available", False))

    def reset(self) -> None:
        self.output.pack_forget()
        self.button.configure(state="normal", text="🤖  Explain with AI")
