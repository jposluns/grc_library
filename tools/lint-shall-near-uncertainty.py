#!/usr/bin/env python3
"""Mandatory-near-uncertainty audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_shall_near_uncertainty.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-shall-near-uncertainty``, enforcing the pack's
``shall-near-uncertainty`` clause); this thin wrapper keeps the house
``python3 tools/lint-shall-near-uncertainty.py`` shape (gate 35 parses exactly that) and supplies
the grc-local scan configuration the pack engine deliberately does not carry: the AIQT bootstrap,
the repo root, the markdown scope selector, the default scan roots, and the grc-specific
EXEMPT_FILES set (the CHANGELOG and the master / ingestion specifications and the ingestion
instruction, which legitimately discuss the markers). The wrapper filters the exempt files out
before delegating, so the engine holds no project-file policy. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them; ``iter_markdown_files``
stays here so the scan-scope regression's ALLOW map observes it unmoved.

Usage:
    python3 tools/lint-shall-near-uncertainty.py
    python3 tools/lint-shall-near-uncertainty.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Files exempt from this check:
# - CHANGELOG records historical defects using these markers.
# - The project and ingestion master specifications discuss the markers as rule patterns.
# - The document-ingestion instruction references the markers.
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
    import gate_lint_shall_near_uncertainty  # the pack-owned engine (source of record)
    return gate_lint_shall_near_uncertainty


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Detect mandatory requirements near uncertainty markers.")
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])

    paths = args.paths or DEFAULT_PATHS
    files = [
        f for f in iter_markdown_files(paths)
        if f.relative_to(REPO_ROOT).as_posix() not in EXEMPT_FILES
    ]
    return _engine().run(files, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
