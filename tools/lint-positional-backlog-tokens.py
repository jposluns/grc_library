#!/usr/bin/env python3
"""Positional backlog-token audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_positional_backlog_tokens.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-positional-backlog-tokens``, enforcing the pack's
``positional-backlog-token`` clause); this thin wrapper keeps the house
``python3 tools/lint-positional-backlog-tokens.py`` shape (gate 35 parses exactly that) and supplies
the grc-local scan configuration the pack engine deliberately does not carry: the AIQT bootstrap, the
repo root, the markdown scope selector, the default scan roots, and the grc-specific EXEMPT_FILES set
(the backlog source and its append-only history, which legitimately carry positional tokens). These
wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them.
``iter_markdown_files`` stays here so the scan-scope regression's ALLOW map observes it unmoved, and
``check_file`` is kept as a thin shim (the exempt-file check plus the engine's generic check) so the
direct-call regression test observes the original signature and behaviour.

Usage:
    python3 tools/lint-positional-backlog-tokens.py
    python3 tools/lint-positional-backlog-tokens.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, guard_explicit_paths, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Files exempt from this gate (the backlog source, the append-only history).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    "guardrails",
    *AUDITED_DOMAIN_DIRS,
]


def iter_markdown_files(paths: list[str]) -> list[Path]:
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_positional_backlog_tokens  # the pack-owned engine (source of record)
    return gate_lint_positional_backlog_tokens


def check_file(path: Path) -> list[tuple[int, str]]:
    """Thin shim preserving the original signature+behaviour (exempt-check + engine check).

    Kept in the wrapper because a direct-call regression test invokes ``mod.check_file(path)`` on
    this module; the pattern logic itself lives in the pack engine.
    """
    if path.relative_to(REPO_ROOT).as_posix() in EXEMPT_FILES:
        return []
    return _engine().check_file(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Flag renumber-fragile positional backlog-token references."
    )
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])
    # Explicit paths are refused when unsound and normalized otherwise (3b21).
    paths = guard_explicit_paths(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    files = [
        f for f in iter_markdown_files(paths)
        if f.relative_to(REPO_ROOT).as_posix() not in EXEMPT_FILES
    ]
    return _engine().run(files, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
