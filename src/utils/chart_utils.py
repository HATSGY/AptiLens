"""
Helpers for embedding Matplotlib figures inside CustomTkinter frames.

Keeping this logic in one place means every module (Graph Analysis,
Performance Analysis, ...) embeds charts the exact same way.
"""

from __future__ import annotations

from typing import Any

import matplotlib

matplotlib.use("Agg")  # safe default; main_window switches to TkAgg once Tk exists
import matplotlib.pyplot as plt  # noqa: E402


# Dark-theme chart palette (kept in sync with src.config.settings).
CHART_BG = "#161B22"
CHART_TEXT = "#E6EAF2"
CHART_MUTED = "#8B97AB"
CHART_GRID = "#2A3342"
CHART_SERIES = ["#4F7DF3", "#2DD4BF", "#FBBF24", "#F472B6", "#A78BFA", "#34D399", "#F87171"]

plt.rcParams.update({
    "figure.facecolor": CHART_BG,
    "axes.facecolor": CHART_BG,
    "axes.edgecolor": CHART_GRID,
    "axes.labelcolor": CHART_MUTED,
    "axes.titlecolor": CHART_TEXT,
    "axes.prop_cycle": matplotlib.cycler(color=CHART_SERIES),
    "text.color": CHART_TEXT,
    "xtick.color": CHART_MUTED,
    "ytick.color": CHART_MUTED,
    "grid.color": CHART_GRID,
    "legend.facecolor": CHART_BG,
    "legend.edgecolor": CHART_GRID,
    "savefig.facecolor": CHART_BG,
})


def new_figure(figsize: tuple[float, float] = (6.4, 4.2)) -> tuple[plt.Figure, plt.Axes]:
    """Create a Matplotlib figure/axes pair styled to match the dark app theme."""
    fig, ax = plt.subplots(figsize=figsize, dpi=100)
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    return fig, ax


def embed_figure(parent: Any, fig: plt.Figure):
    """Embed a Matplotlib figure inside a CustomTkinter/Tkinter parent widget.

    Returns the FigureCanvasTkAgg instance so the caller can keep a reference
    (Tkinter will not render the canvas if it gets garbage collected).
    """
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
    return canvas


def close_figure(fig: plt.Figure) -> None:
    plt.close(fig)
