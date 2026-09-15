#!/usr/bin/env python3
"""Filename / Document-Title alignment audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_filename_title_alignment.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-filename-title-alignment``, enforcing the pack's
``filename-title-alignment`` clause); this thin wrapper keeps the house
``python3 tools/lint-filename-title-alignment.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the repo root, the markdown
scope selector, the default scan roots, the grc document-type prefix set + synonym map (the pack profile
defaults/grc/alignment.toml, loaded via profile_loader.load('alignment') and composed to the
engine's synonyms/doctypes in _alignment_config(), Phase-4 PR-E), and the target-selection
exemptions. gate 67 (lint-doctype-parity) Check 1 reads the composed doctypes via
_alignment_config(). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; ``iter_active_files`` stays here so the scan-scope
regression's ALLOW map observes it unmoved.

Usage:
    python3 tools/lint-filename-title-alignment.py
    python3 tools/lint-filename-title-alignment.py path1 path2 ...
    python3 tools/lint-filename-title-alignment.py --min-overlap 2

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_scan_roots_markdown

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


EXEMPT_DIRECTORY_PREFIXES: tuple[str, ...] = (
    "guardrails/",
    "tools/",
    "docs/",
)

# Files exempt from the filename-title alignment rule. Intentionally
# empty: the current corpus has zero false positives, and the linter's
# permissive overlap check (any one significant content word shared
# between filename and title satisfies the rule) makes per-file
# exemptions rarely needed. Kept as a maintenance hook for future
# legitimate exceptions; add with a brief inline reason.
EXEMPT_FILES: set[str] = set()

# README files and the repository root meta-files are exempt.
EXEMPT_FILENAMES: set[str] = {
    "README.md",
}

# The audited domain directories, sourced from the single
# ``AUDITED_DOMAIN_DIRS`` declaration in ``lint_common`` (the scan-scope
# parity gate forbids hardcoding the run here).
DEFAULT_PATHS = list(AUDITED_DOMAIN_DIRS)

def _alignment_config() -> tuple[dict[str, str], set[str]]:
    """Load the gate-7 alignment vocabulary from the pack profile (Phase-4 PR-E).

    Returns ``(synonyms, doctypes)`` composed from the pack reference-vocabulary
    profile ``.corpus-management/defaults/grc/alignment.toml``, loaded via
    ``profile_loader.load('alignment')`` (fail-closed: ProfileError on an
    envelope defect; a missing key surfaces as a KeyError, never a silent pass).
    ``synonyms`` is a ``dict[str, str]`` (acronym -> expansion), ``doctypes`` a
    ``set[str]`` of lowercase document-type prefixes. Both are order-insensitive
    (the engine uses ``synonyms.get`` + ``prefix in doctypes``), so the profile
    mirrors the former DOCTYPES/SYNONYMS literals 1:1. gate 67 (lint-doctype-
    parity) Check 1 reads the composed ``doctypes`` via THIS function, so no
    module constant needs to stay for the cross-gate check.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader (PR-A)

    prof = profile_loader.load("alignment")
    synonyms = {str(k): str(v) for k, v in prof["synonyms"].items()}
    doctypes = {str(d) for d in prof["doctypes"]}
    return synonyms, doctypes



def iter_active_files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for f in iter_scan_roots_markdown(paths, repo_root=REPO_ROOT):
        rel = f.relative_to(REPO_ROOT).as_posix()
        if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
            continue
        if rel in EXEMPT_FILES:
            continue
        if f.name in EXEMPT_FILENAMES:
            continue
        out.append(f)
    return out
def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_filename_title_alignment  # the pack-owned engine (source of record)
    return gate_lint_filename_title_alignment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="*", default=None,
        help="Paths to scan (default: all active library directories)",
    )
    parser.add_argument(
        "--paths", dest="legacy_paths", nargs="+", default=None, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--min-overlap", type=int, default=1,
        help=(
            "Minimum number of shared significant tokens required. "
            "Default 1: flag only files with zero shared tokens."
        ),
    )
    args = parser.parse_args()
    if args.paths and args.legacy_paths is not None:
        parser.error("use positional paths or --paths, not both")
    paths = (
        args.paths if args.paths
        else args.legacy_paths if args.legacy_paths is not None
        else DEFAULT_PATHS
    )
    synonyms, doctypes = _alignment_config()
    return _engine().run(
        iter_active_files(paths),
        synonyms=synonyms,
        doctypes=doctypes,
        min_overlap=args.min_overlap,
        repo_root=REPO_ROOT,
    )


if __name__ == "__main__":
    sys.exit(main())
