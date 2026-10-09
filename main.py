#!/usr/bin/env python3
"""
AptiLens — Aptitude & Data Interpretation Studio
Entry point.

Run with:
    python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so `import src...` works no matter
# which directory this script is launched from.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app import main  # noqa: E402

if __name__ == "__main__":
    main()
