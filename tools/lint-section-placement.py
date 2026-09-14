#!/usr/bin/env python3
"""Section-placement audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_section_placement.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-section-placement``, enforcing the pack's
``section-placement`` clause); this thin wrapper keeps the house
``python3 tools/lint-section-placement.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the AIQT bootstrap,
the repo root, the grc PLACEMENT_RULES (the per-position, per-doctype section-order rules), the
target selection (the exempt dirs, the ``Status: Superseded`` skip, the narrative / default-exempt
scope predicates via ``is_target`` + ``iter_targets``), and the default scan root. These wrapper
bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them. PLACEMENT_RULES,
is_target, iter_targets, and main stay HERE (grc config) so the scan-scope regression's WALKER map
and the CLI regression tests observe them unmoved.

Usage:
    python3 tools/lint-section-placement.py
    python3 tools/lint-section-placement.py path1 path2 ...

Exit codes: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, DEFAULT_EXEMPT_DIRS, is_narrative_root, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]


EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS  # narrative-root exclusion is root-anchored via is_narrative_root (P-1.25 scan-root split)

# Each rule: (rule_id, description, canonical_heading_names, position, applicable_doctypes_or_none)
# - canonical_heading_names: case-insensitive exact-match set; a section heading
#   matches the rule if (after normalization) it equals any of these names.
# - position: ("top", N) means the matched section must be in the first N
#   ``##`` sections; ("bottom", N) means in the last N ``##`` sections.
# - applicable_doctypes_or_none: None means apply to all in-scope files
#   (regardless of doctype, including README and meta files); a tuple of
#   doctype names means apply only when the file's Document Type matches one
#   of those names.
PLACEMENT_RULES: list[tuple[str, str, frozenset[str], tuple[str, int], tuple[str, ...] | None]] = [
    (
        "SP-01",
        "orientation sections (Purpose, Scope, Purpose and Scope, Overview, "
        "Applicability, Introduction, Executive Summary) must be in the top "
        "three sections",
        frozenset({
            "purpose",
            "scope",
            "purpose and scope",
            "overview",
            "applicability",
            "introduction",
            "executive summary",
        }),
        ("top", 3),
        None,
    ),
    (
        "SP-03",
        "version history sections (Version history, Release history, Changelog) "
        "must be in the bottom three sections",
        frozenset({
            "version history",
            "release history",
            "changelog",
        }),
        ("bottom", 3),
        None,
    ),
    (
        "SP-04",
        "licence sections (Licence, License, Licence boundary, License boundary, "
        "Licence and third-party reference boundary, License and third-party "
        "reference boundary) must be in the bottom three sections",
        frozenset({
            "licence",
            "license",
            "licence boundary",
            "license boundary",
            "licence and third-party reference boundary",
            "license and third-party reference boundary",
        }),
        ("bottom", 3),
        None,
    ),
]


def is_target(path: Path) -> bool:
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return False
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts) or is_narrative_root(path):
        return False
    # Skip documents marked Status: Superseded (the lifecycle marker).
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Status:\*\*\s+Superseded", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        return False
    return True


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return sorted(targets)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_section_placement  # the pack-owned engine (source of record)
    return gate_lint_section_placement


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce section-placement conventions across the markdown corpus."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    return _engine().run(iter_targets(args.paths), PLACEMENT_RULES, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
