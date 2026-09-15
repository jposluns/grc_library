#!/usr/bin/env python3
"""Framework-citation denylist audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_citations.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-citations``, enforcing the pack's ``citation-denylist``
clause); this thin wrapper keeps the house ``python3 tools/lint-citations.py`` shape (gate 35
parses exactly that) and supplies the grc-local configuration the pack engine deliberately
does not carry: the AIQT bootstrap, the repo root, the framework-citation denylist config
(the pack reference-vocabulary profile .corpus-management/defaults/grc/citations.toml, loaded
via profile_loader.load('citations') and converted to the engine shapes in _citation_config(),
Phase-4 PR-B), the markdown scope selector, and the default scan roots. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them. _citation_config /
iter_markdown_files / main stay HERE (grc config) so the scan-scope regression's ALLOW map and
the CitationsLinterTests CLI observe them unmoved.

Usage:
    python3 tools/lint-citations.py
    python3 tools/lint-citations.py --paths governance ai

Exit codes:
    0   no findings
    1   one or more findings present

Maintenance:
    Add new denylist patterns and per-term exemption paths in the pack profile
    .corpus-management/defaults/grc/citations.toml ([[citations.denylist]] entries;
    [citations.path_exemptions] for paths where the literal string must legitimately
    appear, e.g. CHANGELOG entries documenting the historical defect).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


def _citation_config():
    """Load the gate-5 denylist config from the pack profile, adapted to the
    engine's parameter shapes (Phase-4 PR-B).

    The framework-citation denylist is the pack reference-vocabulary profile
    ``.corpus-management/defaults/grc/citations.toml``, loaded via
    ``profile_loader.load('citations')`` (fail-closed: the loader raises
    ``ProfileError`` on an envelope or regex defect; a malformed denylist entry
    would surface as a KeyError in the conversion below rather than pass
    silently. gate 99 validates the shipped profile's envelope and the wiring
    test locks its shape). The loader returns dicts/lists
    (TOML has no tuples/sets); this wrapper converts them to the engine's
    documented shapes, ``list[tuple[str, str, str]]`` and
    ``dict[str, set[str]]``, at this boundary. The engine is unchanged.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader (PR-A)

    prof = profile_loader.load("citations")
    denylist = [
        (e["term"], e["reason"], e["replacement"]) for e in prof["denylist"]
    ]
    path_exemptions = {
        term: set(paths) for term, paths in prof["path_exemptions"].items()
    }
    return denylist, path_exemptions


DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    # Domain run splatted from the single source of truth in
    # ``lint_common``; the scan-scope parity gate forbids hardcoding it.
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
    import gate_lint_citations  # the pack-owned engine (source of record)
    return gate_lint_citations


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint framework citations against a denylist.")
    parser.add_argument(
        "paths", nargs="*", default=None,
        help="Paths to scan (files or directories).",
    )
    parser.add_argument(
        "--paths", dest="legacy_paths", nargs="*", default=None,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv[1:])
    if args.paths and args.legacy_paths is not None:
        parser.error("use positional paths or --paths, not both")
    paths = (
        args.paths if args.paths
        else args.legacy_paths if args.legacy_paths is not None
        else DEFAULT_PATHS
    )
    denylist, path_exemptions = _citation_config()
    return _engine().run(
        iter_markdown_files(paths), denylist, path_exemptions, repo_root=REPO_ROOT
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
