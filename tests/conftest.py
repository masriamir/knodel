"""Pytest configuration helpers."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the ``src`` directory is importable when running tests without installation.
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
