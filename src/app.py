"""Application bootstrap module, imported by the top-level main.py."""

from __future__ import annotations

from src.ui.main_window import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
