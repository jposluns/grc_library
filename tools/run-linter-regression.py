#!/usr/bin/env python3
"""Thin wrapper that runs the full tests/ regression suite.

The audit programme's linter regression test suite gate invokes this
script (a gate in the inventory; its number is maintained in
``governance/specification-audit-programme.md`` §6 and is not repeated
here, because gate numbers shift when a gate is inserted). It exists so
that all four audit-programme surfaces (spec inventory, workflow,
runner, pre-commit hook) can reference the same ``tools/X.py`` shape
that the gate-name parity linter expects.

Discovers every top-level ``tests/test_*.py`` file itself (sorted by
module name), prints the module list it runs, and runs all of the
modules in ONE ``unittest`` invocation, so a new test file is in the
gate by existing rather than by a hand-maintained module list or a
per-class re-export in ``tests/test_linters.py`` (the 3b525 finding:
the hand-maintained list ran two modules and covered the other test
files only through such re-exports, which a new file or class silently
misses). Only top-level ``tests/test_*.py`` files are in scope: a
``test_*.py`` file inside a ``tests/`` SUBDIRECTORY is a refusal (exit
2, naming the nested file), never a silent omission.

Refusals never soften to green (the 3b525 round-1 findings):

* Before running anything, ``main`` re-enumerates ``tests/`` with
  ``os.walk`` (not the discovery glob) and refuses (exit 2) when the
  run list does not exactly match the on-disk top-level test files.
  This completeness self-check lives HERE, not in a test module, so a
  run-list regression that drops a test module (including
  ``tests/test_linters.py`` itself) cannot also remove the check.
* A discovered file whose import raises ANYTHING, ``BaseException``
  included (an import-time ``SystemExit(0)`` must not become a green
  run), is a refusal: exit 2, naming the file.
* A green child exit is believed only when unittest's own output
  carries a ``Ran N tests`` line with N at least 1; otherwise the run
  is refused with exit 2. The child's stderr is captured for that
  check and replayed to this process's stderr.

Exit code is otherwise forwarded from unittest: 0 if all tests pass,
non-zero on failure.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Child driver: import every discovered module first, refusing loud (exit 2,
# naming the file) when one cannot be imported, then hand the whole module
# list to a single unittest invocation. The import check catches
# BaseException, not Exception: a module raising SystemExit(0) at import
# time would otherwise end the child with exit 0 before any test runs.
_DRIVER = """\
import importlib
import sys
import unittest

modules = sys.argv[1:]
failed = False
for name in modules:
    try:
        importlib.import_module(name)
    except BaseException as exc:
        print("REFUSED: cannot import tests/%s.py: %r"
              % (name.partition(".")[2], exc), file=sys.stderr)
        failed = True
if failed:
    sys.exit(2)
unittest.main(module=None, argv=["unittest"] + modules)
"""

# unittest's summary: "Ran 1 test in 0.001s", "Ran 3302 tests in 651.6s".
_SUMMARY_LINE = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)


def discover_test_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    """Every top-level tests/test_*.py as a dotted module name, sorted."""
    return sorted(
        "tests." + path.stem
        for path in (repo_root / "tests").glob("test_*.py")
    )


def completeness_refusal(modules: list[str],
                         repo_root: Path = REPO_ROOT) -> str | None:
    """Refusal message when ``modules`` is not the complete on-disk set.

    Re-enumerates tests/ with os.walk, independently of the discovery
    glob, so a narrowed glob or a filter applied to the run list no
    longer matches the walk. A test_*.py file in a tests/ subdirectory
    is a refusal: only top-level tests/test_*.py files are in scope.
    Returns None when the run list is complete.
    """
    tests_dir = repo_root / "tests"
    on_disk = []
    for dirpath, _dirnames, filenames in os.walk(tests_dir):
        for filename in filenames:
            if filename.startswith("test_") and filename.endswith(".py"):
                if Path(dirpath) != tests_dir:
                    return ("nested test file %s: only top-level "
                            "tests/test_*.py files are in scope"
                            % (Path(dirpath) / filename))
                on_disk.append("tests." + filename[:-3])
    if not on_disk:
        return "no tests/test_*.py files found under %s" % tests_dir
    if sorted(modules) != sorted(on_disk):
        return ("run list %s does not match on-disk tests/test_*.py "
                "files %s" % (sorted(modules), sorted(on_disk)))
    return None


def main(repo_root: Path = REPO_ROOT, run=subprocess.run) -> int:
    modules = discover_test_modules(repo_root)
    refusal = completeness_refusal(modules, repo_root)
    if refusal is not None:
        print("REFUSED: " + refusal, file=sys.stderr)
        return 2
    print("Running test modules:")
    for name in modules:
        print("  " + name)
    result = run(
        [sys.executable, "-c", _DRIVER, *modules],
        cwd=str(repo_root),
        stderr=subprocess.PIPE,
    )
    stderr = (result.stderr or b"").decode("utf-8", "replace")
    sys.stderr.write(stderr)
    sys.stderr.flush()
    counts = _SUMMARY_LINE.findall(stderr)
    if result.returncode == 0 and (not counts or int(counts[-1]) < 1):
        print("REFUSED: unittest exited 0 without a 'Ran N tests' line "
              "with N at least 1; not a believable green run",
              file=sys.stderr)
        return 2
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
