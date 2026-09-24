#!/usr/bin/env python3
"""Section-placement audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_section_placement.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-section-placement``, enforcing the pack's
``section-placement`` clause); this thin wrapper keeps the house
``python3 tools/lint-section-placement.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the AIQT bootstrap,
the repo root, the grc PLACEMENT RULES (the pack profile defaults/grc/placement.toml, loaded via
profile_loader.load('placement') and composed to the engine's rule tuples in _placement_config(),
Phase-4 PR-D), the
target selection (the exempt dirs, the ``Status: Superseded`` skip, the narrative / default-exempt
scope predicates via ``is_target`` + ``iter_targets``), and the default scan root. These wrapper
bytes are HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them. _placement_config,
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
from lint_common import guard_explicit_paths_cwd, is_default_exempt_root, DEFAULT_EXEMPT_DIRS, is_narrative_root, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]


EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS  # narrative-root exclusion is root-anchored via is_narrative_root (P-1.25 scan-root split)

def _placement_config() -> list[tuple[str, str, frozenset[str], tuple[str, int], tuple[str, ...] | None]]:
    """Load the gate-38 placement rules from the pack profile, composed to the
    engine's exact rule shape (Phase-4 PR-D).

    The model is the pack reference-vocabulary profile
    ``.corpus-management/defaults/grc/placement.toml``, loaded via
    ``profile_loader.load('placement')`` (fail-closed: the loader raises
    ProfileError on an envelope defect; a missing field surfaces as a KeyError
    below, never a silent pass). Each ``[[placement.rules]]`` table is rebuilt
    into the engine's ``(rule_id, description, frozenset(aliases),
    (position, count), doctypes_tuple_or_None)`` tuple; a rule with no
    ``doctypes`` key applies to all in-scope files (the None convention), and
    an explicit empty list is a deliberate applies-to-none disable.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader (PR-A)

    prof = profile_loader.load("placement")
    return [
        (
            str(r["id"]),
            str(r["description"]),
            frozenset(str(a) for a in r["section_aliases"]),
            (str(r["position"]), int(r["count"])),
            tuple(str(d) for d in r["doctypes"]) if "doctypes" in r else None,
        )
        for r in prof["rules"]
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
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    return _engine().run(iter_targets(args.paths), _placement_config(), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
