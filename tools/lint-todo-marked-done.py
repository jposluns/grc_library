#!/usr/bin/env python3
"""TODO-marked-done audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_todo_marked_done.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-todo-marked-done``, enforcing the pack's ``todo-forward-only``
clause); this thin wrapper keeps the house ``python3 tools/lint-todo-marked-done.py`` shape (gate 35
parses exactly that) and supplies the grc-local scan configuration the pack engine deliberately does
not carry: the AIQT bootstrap, the repo root, the markdown scope selector, and the default scan
target (``TODO.md``: the public index; the per-item detail moved to the private sibling in the
2026-08 migration and is governed there). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; ``iter_markdown_files`` stays here so the
scan-scope regression's ALLOW map observes it unmoved.

Usage:
    python3 tools/lint-todo-marked-done.py
    python3 tools/lint-todo-marked-done.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = ["TODO.md"]  # the public index; the per-item DETAIL moved to the private sibling (2026-08 migration), governed there


def iter_markdown_files(paths: list[str]) -> list[Path]:
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_todo_marked_done  # the pack-owned engine (source of record)
    return gate_lint_todo_marked_done


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect a TODO item that marks itself done in place."
    )
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])
    paths = args.paths or DEFAULT_PATHS
    return _engine().run(iter_markdown_files(paths), repo_root=REPO_ROOT)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
