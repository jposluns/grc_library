#!/usr/bin/env python3
"""Stdlib-only import audit (gate 71).

The corpus' audit / build toolchain is PRODUCT: an adopter clones the public repo and
runs it with a bare Python interpreter and NO third-party packages installed (the same
environment CI provides). So every module the toolchain imports must be either the Python
standard library or a first-party in-repo module. A third-party import (``import yaml``,
``import requests``, ...) breaks a fresh adopter clone and CI, even though it runs fine on
a maintainer machine that happens to have the package installed.

This gate closes exactly that blind spot. It statically AST-parses every toolchain Python
file (``tools/``, ``tests/``, ``.web/``) and flags any imported ROOT module that is not:

  - in ``sys.stdlib_module_names`` (the running interpreter's standard library), OR
  - a first-party in-repo module (the stem of a ``.py`` file in the scanned set, e.g.
    ``lint_common`` or the reference modules), OR
  - an explicitly-allow-listed sanctioned dependency (``ALLOWED_THIRD_PARTY`` below,
    currently empty; the corpus is pure stdlib).

Why static AST, not grep: a grep over import lines throws false positives on prose
("from NIST ...") and misses nothing only by luck. ``ast`` sees the real import graph,
including lazy imports inside functions (a lazy third-party import still breaks the
adopter when the code path runs, so it is flagged too).

Why this and not ``check-portability.sh``: that script clones the repo sibling-free and
runs the suite, but under the MAINTAINER's Python (which may have the package installed),
so it tests sibling-ABSENCE, not the stdlib-only environment. This gate runs inside
``run_all_audits.sh`` and catches a third-party import at every commit, earlier than CI.

Exit codes: 0 = clean (every toolchain import is stdlib or first-party); 1 = one or more
third-party imports.

Sanctioned-exception pattern: if a tool genuinely needs a third-party dependency, add its
root name to ``ALLOWED_THIRD_PARTY`` with a same-line rationale (the gate-discipline
exception pattern) AND ensure the project documents the dependency; do not silence the
gate by any other means.
"""
import argparse
import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories whose *.py ship as the runnable toolchain (adopters execute these).
SCAN_DIRS = ("tools", "tests", ".web")

# Sanctioned third-party dependencies (root module name -> rationale). EMPTY: the
# toolchain is pure standard library. A future entry needs a rationale here and a
# documented project dependency (the gate-discipline exception pattern).
ALLOWED_THIRD_PARTY: dict[str, str] = {}


def _scan_files() -> list[Path]:
    files: list[Path] = []
    for d in SCAN_DIRS:
        base = REPO_ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            files.append(p)
    return files


def _first_party_names(files: list[Path]) -> set[str]:
    # Any scanned .py is importable by its stem as a sibling module (the toolchain adds
    # its own dir to sys.path); those names are first-party, never third-party.
    return {p.stem for p in files}


def _import_roots(tree: ast.AST) -> list[tuple[int, str]]:
    """Return [(lineno, root_module), ...] for every import in the tree. Relative
    imports (from . import x) are first-party by construction and skipped."""
    roots: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.append((node.lineno, alias.name.split(".")[0]))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # relative import: in-package, first-party
            if node.module:
                roots.append((node.lineno, node.module.split(".")[0]))
    return roots


def scan() -> list[tuple[str, int, str]]:
    files = _scan_files()
    allowed = set(sys.stdlib_module_names) | _first_party_names(files) | set(ALLOWED_THIRD_PARTY)
    findings: list[tuple[str, int, str]] = []
    for path in files:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:  # a broken file is its own gate's problem
            findings.append((str(path.relative_to(REPO_ROOT)), 0, f"unparseable: {exc}"))
            continue
        for lineno, root in _import_roots(tree):
            if root not in allowed:
                rel = path.relative_to(REPO_ROOT).as_posix()
                findings.append((rel, lineno, root))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stdlib-only import audit (gate 71): flag "
                                             "third-party imports in the runnable toolchain.")
    ap.parse_args(argv)
    findings = scan()
    if not findings:
        nfiles = len(_scan_files())
        print(f"OK: stdlib-only import audit clean ({nfiles} toolchain file(s) scanned; "
              f"every import is stdlib or first-party).")
        return 0
    print("FAIL: third-party import(s) in the runnable toolchain (breaks a bare adopter "
          "clone and CI):")
    for rel, lineno, root in findings:
        print(f"  {rel}:{lineno} imports non-stdlib, non-first-party module `{root}`")
    print("\nThe toolchain must run on a bare Python (stdlib only). Replace the "
          "third-party import with a stdlib equivalent, or, if the dependency is genuinely "
          "required, add its root name to ALLOWED_THIRD_PARTY with a rationale and document "
          "the project dependency (the gate-discipline exception pattern).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
