#!/usr/bin/env python3
"""Required-sections-by-doctype audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_required_sections.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-required-sections``, enforcing the pack's
``required-sections`` clause); this thin wrapper keeps the house
``python3 tools/lint-required-sections.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the AIQT bootstrap,
the repo root, the grc SECTION MODEL (the pack profile defaults/grc/sections.toml, loaded via
profile_loader.load('sections') and composed to the engine's required_map in _sections_config(),
Phase-4 PR-C), the
target selection (the exempt-file set, the ``Status: Superseded`` lifecycle skip, the
narrative / default-exempt scope predicates via ``is_target`` + ``iter_targets``), and the
default scan root. These wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99
does NOT own them. ``_sections_config``, ``is_target``, ``iter_targets``, and ``main`` stay
HERE (grc config) so the scan-scope regression's WALKER map and the CLI/``main`` regression
tests observe them unmoved.

Usage:
    python3 tools/lint-required-sections.py
    python3 tools/lint-required-sections.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 finding(s).
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

# Directory-walk exemption: shared default set from lint_common (plus the
# root-anchored executive/ narrative-tree exclusion via is_narrative_root,
# P-1.25 scan-root split). The
# is_target function reads each file's metadata to check for the
# Status: Superseded lifecycle exemption (re-keyed from the former
# Classification: Deprecated overload, the L-j migration), so this linter
# cannot use the shared iter_markdown_targets helper as-is.
EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS  # narrative-root exclusion is root-anchored via is_narrative_root (P-1.25 scan-root split)

def _sections_config() -> dict[str, list[list[str]]]:
    """Load the gate-19 section model from the pack profile, composed to the
    engine's required_map shape (Phase-4 PR-C).

    The model is the pack reference-vocabulary profile
    ``.corpus-management/defaults/grc/sections.toml``, loaded via
    ``profile_loader.load('sections')`` (fail-closed: the loader raises
    ProfileError on an envelope/regex defect; a missing key surfaces as a
    KeyError below, never a silent pass). The profile mirrors the former
    wrapper constants 1:1 (one orientation-alias list plus the doctypes that
    reference it); this boundary performs the same composition the deleted
    dict literal performed: each enforced doctype maps to
    ``[orientation_options]``. Per-doctype lists are independent copies so a
    consumer mutating one cannot alias the others. Gate 67 (lint-doctype-parity)
    Check 2 reads this function, not a module constant, so removing the literal
    cannot leave that check vacuous.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader (PR-A)

    prof = profile_loader.load("sections")
    options = [str(o) for o in prof["orientation_options"]]
    return {str(dt): [list(options)] for dt in prof["orientation_doctypes"]}


EXEMPT_FILES: set[str] = {
    # README files use a simpler shape than canonical artefacts.
    # Phase 23.73b removed `CITATION.cff` and `LICENSE`: this linter scans
    # `.md` files only (see `is_target`), so non-`.md` entries were
    # unreachable defensive listings.
    "README.md",
    "NOTICE.md",
    "AUTHORS.md",
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    # Worklists and templates use their own shapes.
}


def is_target(path: Path) -> bool:
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return False
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts) or is_narrative_root(path):
        return False
    if path.name in EXEMPT_FILES:
        return False
    if path.name.startswith("template-"):
        return False
    if path.name.startswith("worklist-"):
        return False
    # Documents marked Status: Superseded (the lifecycle marker) are short
    # redirect notices.
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Status:\*\*\s+Superseded", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        pass
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
    return targets


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_required_sections  # the pack-owned engine (source of record)
    return gate_lint_required_sections


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce required section presence by document type."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    return _engine().run(iter_targets(args.paths), _sections_config(), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
