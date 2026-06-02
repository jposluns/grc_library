#!/usr/bin/env python3
"""Thin wrapper that runs the linter regression test suite.

The audit programme's gate 34 invokes this script. It exists so that
all four audit-programme surfaces (spec inventory, workflow, runner,
pre-commit hook) can reference the same ``tools/X.py`` shape that the
gate-name parity linter expects.

Equivalent to ``python3 -m unittest tests.test_linters``. Exit code is
forwarded from unittest: 0 if all tests pass, non-zero on failure.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_linters"],
        cwd=str(REPO_ROOT),
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
