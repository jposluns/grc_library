#!/usr/bin/env python3
"""Broken-internal-link audit (grc gate 3): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_links.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-links``, enforcing the pack's ``markdown-link-resolution``
clause); this thin wrapper keeps the house ``python3 tools/lint-links.py`` shape (gate 35
parses exactly that) and supplies the grc-local scan configuration the pack engine
deliberately does not carry: the AIQT bootstrap, the repo root, the markdown scope selector
(``iter_markdown_files``), and the default scan roots (``DEFAULT_SCAN_ROOTS``). These wrapper
bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them. Both
``iter_markdown_files`` and ``DEFAULT_SCAN_ROOTS`` stay HERE (grc scan config) so the scan-scope
regression's ALLOW map and the resolved-scan-root behavioural tests observe them unmoved.

Usage:
    python3 tools/lint-links.py
    python3 tools/lint-links.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 broken link(s).
"""

from __future__ import annotations

import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, guard_explicit_paths, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


def iter_markdown_files(paths: list[str]) -> list[Path]:
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


# Default scan roots when no paths are given. Exposed as a module-level constant so a
# regression test can assert membership BEHAVIOURALLY (against the list the code actually
# scans), not by grepping source text. ``tools`` and ``docs`` are per-linter extras beyond
# the audited domains; the domain run is splatted from lint_common (the scan-scope parity
# gate forbids hardcoding it). ``.claude/rules`` (3.182 (closing PR #1347)) is a shipped rule
# surface, the pack mirror plus third-party overlays, whose relative Markdown targets must
# resolve; it is in DEFAULT_EXEMPT_DIRS so no other gate link-checks it, and scanning it here
# catches dead links (never-vendored companions, mirror path rot) before they ship in the
# guardrails pack.
DEFAULT_SCAN_ROOTS: list[str] = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    *AUDITED_DOMAIN_DIRS,
    "tools",
    "docs",
    ".claude/rules",
    "guardrails",
    "executive",  # narrative layer: IN link-integrity scope (P-1.25 scan-root split)
]


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_links  # the pack-owned engine (source of record)
    return gate_lint_links


def main(argv: list[str]) -> int:
    # Explicit paths are refused when unsound and normalized otherwise (3b21).
    paths = guard_explicit_paths(argv[1:], repo_root=REPO_ROOT) if argv[1:] else DEFAULT_SCAN_ROOTS
    return _engine().run(iter_markdown_files(paths), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
