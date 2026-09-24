#!/usr/bin/env python3
"""Bare normative-wording audit (grc gate 56): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_bare_normative_shall.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-bare-normative-shall``, enforcing the pack's
``normative-wording`` clause); this thin wrapper keeps the house
``python3 tools/lint-bare-normative-shall.py`` shape (gate 35 parses exactly that) and supplies
the grc-local scan configuration the pack engine deliberately does not carry: the AIQT bootstrap,
the markdown scope selector (``iter_markdown_files``, kept here so the scan-scope regression's
ALLOW map observes it unmoved), the default scan roots, and the grc-specific EXEMPT_FILES set
(the CHANGELOG and the master / ingestion specifications and the ingestion instruction, which
legitimately discuss the convention and its target word). The wrapper filters the exempt files
out before delegating, so the engine holds no project-file policy. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them.

Scope: ``README.md``, ``NOTICE.md``, the audited domain directories (splatted from ``lint_common``
so the scan-scope-parity gate is satisfied), and ``guardrails``.

Usage:
    python3 tools/lint-bare-normative-shall.py
    python3 tools/lint-bare-normative-shall.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 findings.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, guard_explicit_paths, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

# Derive the pack tools/ from this file's location, independent of the (test-rebound) REPO_ROOT.
PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Files that legitimately discuss the convention and its target word. Mirrors gate 9's EXEMPT_FILES.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    # Domain run splatted from lint_common (scan-scope parity gate forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]


def iter_markdown_files(paths: list[str]) -> list[Path]:
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_bare_normative_shall  # the pack-owned engine (source of record)
    return gate_lint_bare_normative_shall


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect bare normative 'shall' in authored corpus prose."
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
    raise SystemExit(main(sys.argv))
