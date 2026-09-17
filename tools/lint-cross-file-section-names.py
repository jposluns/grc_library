#!/usr/bin/env python3
"""Validate cross-file section NAMES (title-fit phase) - grc wrapper over the pack-owned engine.

The names phase layers title-fit checking on top of the numbers phase (gate 62,
lint-cross-file-section-refs): a reference pairing a section NUMBER with a heading
TITLE must cite the title's actual number in the resolved target. It fires on the
same two resolvable-target classes (adjacent-link and binding-declaration), plus
the table-row seam gate 62 excludes (an anchored-title reference to a number that
is not a numbered heading in the target, on a table row).

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(normalize_title, extract_titles, resolve_target, binding_target, adjacent_link,
title_candidate, check_file, with the tool-specific TITLE_HEADING_RE /
PAREN_TITLE_RE / QUOTE_TITLE_RE) lives in the pack-owned engine
(.corpus-management/tools/gate_lint_cross_file_section_names.py, source of
record), parameterized by repo_root + the shared cross-file reference-extraction
config (the CROSS_* block in lint_common, shared with the numbers-phase sibling
gate 62 so the two cannot drift). This wrapper supplies REPO_ROOT, that CROSS_*
config, the grc scan scope (iter_markdown_targets / EXEMPT_FILES) and the
reporting in main, and keeps a module-global check_file shim delegating to the
engine so the scan-scope regression test (which patches mod.check_file and runs
main) observes the original signature and behaviour.

Usage:
    python3 tools/lint-cross-file-section-names.py
    python3 tools/lint-cross-file-section-names.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more cross-file references pair a number with a title that
        belongs to a different (or absent) numbered heading in the target
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import CROSS_ADJACENCY_WINDOW as ADJACENCY_WINDOW, CROSS_BINDING_SENTINEL as BINDING_SENTINEL, CROSS_EXTERNAL_CONTEXT_RE as EXTERNAL_CONTEXT_RE, CROSS_MD_LINK_RE as MD_LINK_RE, CROSS_REF_PATTERNS as REF_PATTERNS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Basename exemptions (historical/meta narration of reference shapes),
# matching gate 62's set.
EXEMPT_FILES = frozenset(
    {
        "CHANGELOG.md",
        "TODO.md",
        "TODO-REFERENCE.md",
    }
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_cross_file_section_names  # the pack-owned engine (source of record)
    return gate_lint_cross_file_section_names


def check_file(path: Path) -> list[str]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression test
    patches ``mod.check_file`` and runs ``main``; the check logic lives in the pack
    engine (source of record), parameterized by REPO_ROOT + the shared CROSS_* config.
    """
    return _engine().check_file(
        path, REPO_ROOT, REF_PATTERNS, MD_LINK_RE, BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, ADJACENCY_WINDOW
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv)

    findings: list[str] = []
    scanned = 0
    for path in iter_markdown_targets([Path(p) for p in args.paths]):
        if path.name in EXEMPT_FILES:
            continue
        scanned += 1
        findings.extend(check_file(path))

    if findings:
        for finding in findings:
            print(finding)
        print(
            f"\nFAIL: {len(findings)} cross-file section-name mismatch(es). "
            "A reference pairing a number with a heading title must cite the "
            "title's actual number in the target; fix the citer (or the "
            "target's numbering), do not weaken this check."
        )
        return 1

    print(
        f"OK: all anchored cross-file number+title references match their "
        f"targets (scanned {scanned} files)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
