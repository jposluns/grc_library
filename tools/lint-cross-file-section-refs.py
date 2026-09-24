#!/usr/bin/env python3
"""Validate cross-file section references (numbers phase) - grc wrapper over the pack-owned engine.

Library documents cite sections of OTHER corpus documents by number, e.g.
"see [the mobile standard](standard-mobile-application-security.md) §5.4" or,
via a binding declaration, a file-wide "Section numbers below refer to that
standard." sentinel after which bare §N references bind to the declared target.
When the target is renumbered, such references silently go stale; the
intra-document gate deliberately filters cross-document context out, so this
class was gate-blind (the #548 / #545 escaped-miss clusters that motivated this
gate). The names phase (gate 65, lint-cross-file-section-names.py) layers
title-fit checking on top of this gate's number-existence checking.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(extract_sections, resolve_target, binding_target, adjacent_link, check_file,
with the tool-specific HEADING_RE / CLAUSE_RE) lives in the pack-owned engine
(.corpus-management/tools/gate_lint_cross_file_section_refs.py, source of
record), parameterized by repo_root and the shared cross-file reference-
extraction config (the CROSS_* block in lint_common, shared with the names-phase
sibling so the two cannot drift). This wrapper supplies REPO_ROOT, that CROSS_*
config, the grc scan scope (iter_markdown_targets / EXEMPT_FILES) and the
reporting in main, and keeps a module-global check_file shim delegating to the
engine so the scan-scope regression test (which patches mod.check_file and runs
main) observes the original signature and behaviour.

Usage:
    python3 tools/lint-cross-file-section-refs.py
    python3 tools/lint-cross-file-section-refs.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more cross-file section references that do not resolve
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import guard_explicit_paths_cwd, CROSS_ADJACENCY_WINDOW as ADJACENCY_WINDOW, CROSS_BINDING_SENTINEL as BINDING_SENTINEL, CROSS_EXTERNAL_CONTEXT_RE as EXTERNAL_CONTEXT_RE, CROSS_MD_LINK_RE as MD_LINK_RE, CROSS_REF_PATTERNS as REF_PATTERNS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Files whose cross-file section references are by convention historical
# or meta (they quote reference shapes rather than cite live sections).
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
    import gate_lint_cross_file_section_refs  # the pack-owned engine (source of record)
    return gate_lint_cross_file_section_refs


def check_file(path: Path) -> list[str]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression test
    patches ``mod.check_file`` and runs ``main``; the check logic (extract_sections,
    resolve_target, binding_target, adjacent_link, check_file) lives in the pack
    engine (source of record), parameterized by REPO_ROOT + the shared CROSS_* config.
    """
    return _engine().check_file(
        path, REPO_ROOT, REF_PATTERNS, MD_LINK_RE, BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, ADJACENCY_WINDOW
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv)
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS

    findings: list[str] = []
    for path in iter_markdown_targets([Path(p) for p in args.paths]):
        if path.name in EXEMPT_FILES:
            continue
        findings.extend(check_file(path))

    if findings:
        for finding in findings:
            print(f"FAIL {finding}")
        print(f"FAIL: {len(findings)} unresolved cross-file section reference(s).")
        return 1
    print("OK: all cross-file section references resolve against their targets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
