"""
Central navigation controller.

Implements the single-window, multi-frame navigation pattern required by
the project spec: ONE root Tk/CTk window, with every "page" being a Frame
stacked in the same container and raised to the front on demand. This
avoids ever creating multiple root Tk() windows.
"""

from __future__ import annotations

import customtkinter as ctk


class NavigationController:
    def __init__(self, container: ctk.CTkFrame) -> None:
        self.container = container
        self.frames: dict[str, ctk.CTkFrame] = {}
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def register(self, name: str, frame: ctk.CTkFrame) -> None:
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show(self, name: str, **kwargs) -> None:
        if name not in self.frames:
            raise KeyError(f"No page registered with name '{name}'")
        frame = self.frames[name]
        on_show = getattr(frame, "on_show", None)
        if callable(on_show):
            on_show(**kwargs)
        frame.tkraise()
