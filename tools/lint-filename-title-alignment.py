#!/usr/bin/env python3
"""Filename / Document-Title alignment audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_filename_title_alignment.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-filename-title-alignment``, enforcing the pack's
``filename-title-alignment`` clause); this thin wrapper keeps the house
``python3 tools/lint-filename-title-alignment.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the repo root, the markdown
scope selector, the default scan roots, the grc document-type prefix set (``DOCTYPES``), the grc
synonym map (``SYNONYMS``), and the target-selection exemptions. ``DOCTYPES`` MUST stay a module
attribute here: the doctype-parity gate (gate 67) loads this module and reads ``DOCTYPES`` to
cross-check it against the canonical type set. These wrapper bytes are HAND-MAINTAINED, not
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

DOCTYPES = {
    "annex", "charter", "checklist", "framework", "guide", "guideline",
    "matrix", "plan", "policy", "principle", "procedure", "register", "roadmap",
    "sop", "specification", "standard", "template", "worklist",
}


# Tokens that mean the same thing across filename and title variations.
# Lowercase only. The right-hand side is the canonical expansion; the linter
# treats either side of the synonym as matching if either appears in the
# opposing token set. Add new entries when the linter false-positives on a
# legitimate acronym-in-filename / expansion-in-title pattern.
SYNONYMS: dict[str, str] = {
    "kpis": "kpi",
    "kpi": "kpi",
    "uk": "united kingdom",
    "us": "united states",
    "eu": "european union",
    "sbom": "software bill of materials",
    "capa": "corrective and preventive action",
    "sox": "sarbanes oxley",
    "fedramp": "federal risk and authorization management program",
    "itgc": "it general controls",
    "aeo": "authorized economic operator",
    "ctpat": "customs trade partnership against terrorism",
    "pip": "partners in protection",
    "basc": "business alliance for secure commerce",
    "dora": "digital operational resilience act",
    "nis": "network and information systems",
    "dsar": "data subject access request",
    "ai": "artificial intelligence",
}



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
    return _engine().run(
        iter_active_files(paths),
        synonyms=SYNONYMS,
        doctypes=DOCTYPES,
        min_overlap=args.min_overlap,
        repo_root=REPO_ROOT,
    )


if __name__ == "__main__":
    sys.exit(main())
