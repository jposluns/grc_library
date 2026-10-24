#!/usr/bin/env python3
"""Thin wrapper that runs the full tests/ regression suite.

The audit programme's linter regression test suite gate invokes this
script (a gate in the inventory; its number is maintained in
``governance/specification-audit-programme.md`` §6 and is not repeated
here, because gate numbers shift when a gate is inserted). It exists so
that all four audit-programme surfaces (spec inventory, workflow,
runner, pre-commit hook) can reference the same ``tools/X.py`` shape
that the gate-name parity linter expects.

Discovers every ``tests/test_*.py`` file itself (sorted by module
name), prints the module list it runs, and runs all of the modules in
ONE ``unittest`` invocation, so a new test file is in the gate by
existing rather than by a hand-maintained module list or a per-class
re-export in ``tests/test_linters.py`` (the 3b525 finding: the
hand-maintained list ran two modules and covered the other test files
only through such re-exports, which a new file or class silently
misses). A discovered file that cannot be imported is a refusal: the
run exits non-zero naming the file, never silently dropping it. Exit
code is forwarded from unittest: 0 if all tests pass, non-zero on
failure.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Child driver: import every discovered module first, refusing loud (exit 2,
# naming the file) when one cannot be imported, then hand the whole module
# list to a single unittest invocation.
_DRIVER = """\
import importlib
import sys
import unittest

modules = sys.argv[1:]
failed = False
for name in modules:
    try:
        importlib.import_module(name)
    except Exception as exc:
        print("REFUSED: cannot import tests/%s.py: %r"
              % (name.partition(".")[2], exc), file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
unittest.main(module=None, argv=["unittest"] + modules)
"""


def discover_test_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every tests/test_*.py as a dotted module name, sorted by module name."""
    return sorted(
        "tests." + path.stem
        for path in (repo_root / "tests").glob("test_*.py")
    )


def main() -> int:
    modules = discover_test_modules()
    if not modules:
        print("REFUSED: no tests/test_*.py files found under "
              + str(REPO_ROOT / "tests"), file=sys.stderr)
        return 2
    print("Running test modules:")
    for name in modules:
        print("  " + name)
    result = subprocess.run(
        [sys.executable, "-c", _DRIVER, *modules],
        cwd=str(REPO_ROOT),
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
