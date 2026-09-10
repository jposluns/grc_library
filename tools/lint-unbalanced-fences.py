#!/usr/bin/env python3
"""Unbalanced-fence audit (grc gate 66): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_unbalanced_fences.py`` (Corpus-Management pack,
gate register ``core/gates.toml``, id ``lint-unbalanced-fences``, enforcing the pack's
``corpus-scan-integrity`` clause); this thin wrapper keeps the house
``python3 tools/lint-unbalanced-fences.py`` shape (gate 35 parses exactly that) and
supplies the grc-local scan configuration the pack engine deliberately does not carry:
the AIQT bootstrap, the repo root, and lint_common's default markdown walk (the
``DEFAULT_EXEMPT_DIRS`` / ``is_default_exempt_root`` exemption plus the explicit-path
iterator). These wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99
does NOT own them; the linter-regression suite (``UnbalancedFenceTests``) and gate 99's
entry-point existence check are the wrapper's mechanical coverage. ``iter_targets`` stays
here (grc scan config) so the scan-scope regression's WALKERS map observes it unmoved.

Scope (unchanged by the transfer): a default run walks every ``*.md`` under the
repository root, minus both the ``DEFAULT_EXEMPT_DIRS`` path components and the
``is_default_exempt_root`` default-root exemption (``DEFAULT_EXEMPT_ROOTS``, currently
``.corpus-management``); explicit path arguments are scanned as given (the mandated
new-pack-prose run on ``.claude/`` files is the recurring explicit case).

Usage:
    python3 tools/lint-unbalanced-fences.py
    python3 tools/lint-unbalanced-fences.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 findings.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import (  # noqa: E402  # grc-config/store, stays local
    is_default_exempt_root,
    DEFAULT_EXEMPT_DIRS,
    iter_scan_roots_markdown,
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_unbalanced_fences  # the pack-owned engine (source of record)
    return gate_lint_unbalanced_fences


def iter_targets(paths: list[str]) -> list[Path]:
    if paths:
        return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)
    files: list[Path] = []
    for f in REPO_ROOT.rglob("*.md"):
        if is_default_exempt_root(f, repo_root=REPO_ROOT):
            continue
        rel_parts = f.relative_to(REPO_ROOT).parts
        if any(part in DEFAULT_EXEMPT_DIRS for part in rel_parts):
            continue
        files.append(f)
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    engine = _engine()
    return engine.run(iter_targets(argv), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main())
