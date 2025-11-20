"""
Keywords package initializer.

This module ensures the project root is on `sys.path` when Robot Framework
imports keywords from this package. Robot adds the directory containing the
calling `.robot` file to `sys.path`, which is `Resource/Keywords` — not the
project root. That means `from Libraries import ...` will fail unless the
project root is added to `sys.path` or Robot is invoked with `--pythonpath`.

We add a safe, idempotent insertion of the project root to `sys.path` so
keyword modules can import the `Libraries` package reliably.
"""
import sys
from pathlib import Path

# Determine project root (two levels up from this file: Resource/Keywords -> Resource -> project root)
_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent.parent

_PROJECT_ROOT_STR = str(_PROJECT_ROOT)

if _PROJECT_ROOT_STR not in sys.path:
	# Insert at position 0 so it takes precedence over installed packages
	sys.path.insert(0, _PROJECT_ROOT_STR)

__all__ = []

