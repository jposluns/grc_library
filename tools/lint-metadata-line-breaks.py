#!/usr/bin/env python3
"""Metadata-block line-break audit (grc wrapper over the pack-owned engine).

Detect runs of consecutive ``**Field:**`` lines that lack a Markdown hard-break
marker on the non-last lines of the run. Without a hard-break, GitHub renders the
metadata block as a single soft-wrapped paragraph rather than as a vertical list
of labelled facts. Two hard-break markers are accepted: a trailing backslash or
two-or-more trailing spaces. Fenced code blocks are skipped, so a metadata-format
example inside a fence is not a false positive; the last line of a run is exempt.

Engine/wrapper split (SHARED/SAFETY lane, Pattern A): the PURE check (``META_LINE``,
``has_hard_break``, ``scan_file``) lives in the pack-owned engine
(``.corpus-management/tools/gate_lint_metadata_line_breaks.py``, source of record).
This wrapper supplies the grc scan scope (``DEFAULT_TARGETS`` / ``iter_target_files``)
and the grouped reporting, and keeps a thin module-global ``scan_file`` shim
delegating to the engine so the scan-scope regression test (which patches
``mod.scan_file`` and runs ``main``) observes the original signature and behaviour.

Usage:

    python3 tools/lint-metadata-line-breaks.py
    python3 tools/lint-metadata-line-breaks.py path/to/specific/file.md

The optional positional path argument restricts the scan to one file, used by the
gate-36 regression test suite for synthetic-fixture isolation.

Exit codes:
    0   no findings.
    1   one or more files have at least one metadata block with a non-last line
        missing the hard-break marker.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, AUDITED_DOMAIN_DIRS, DEFAULT_EXEMPT_DIRS, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_TARGETS = [
    "README.md",
    "CONTRIBUTING.md",
    "NOTICE.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    "docs",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run); ``docs`` above is a per-linter extra.
    *AUDITED_DOMAIN_DIRS,
]


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_metadata_line_breaks  # the pack-owned engine (source of record)
    return gate_lint_metadata_line_breaks


def scan_file(path: Path) -> list[tuple[int, int]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression test
    patches ``mod.scan_file`` and runs ``main``; the check logic (META_LINE,
    has_hard_break, scan_file) lives in the pack engine (source of record).
    """
    return _engine().scan_file(path)


def iter_target_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for t in targets:
        p = REPO_ROOT / t
        if p.is_file() and p.suffix == ".md":
            files.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if any(part in DEFAULT_EXEMPT_DIRS for part in f.relative_to(REPO_ROOT).parts):
                    continue
                files.append(f)
    return sorted(f for f in set(files) if not is_default_exempt_root(f, repo_root=REPO_ROOT))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit metadata-block line breaks across the markdown corpus."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=None,
        help="Optional .md files or directories to scan (default: all corpus directories).",
    )
    args = parser.parse_args(argv)

    if args.paths:
        files = []
        for raw in args.paths:
            target = Path(raw)
            if not target.is_absolute():
                target = REPO_ROOT / target
            if target.is_file():
                files.append(target)
            elif target.is_dir():
                files.extend(sorted(target.rglob("*.md")))
    else:
        files = iter_target_files(DEFAULT_TARGETS)

    files = [f for f in files if not is_default_exempt_root(f, repo_root=REPO_ROOT)]
    total_findings = 0
    files_flagged = 0
    for f in files:
        findings = scan_file(f)
        if not findings:
            continue
        files_flagged += 1
        rel = f.relative_to(REPO_ROOT).as_posix()
        print(f"=== {rel} ===")
        for block_start, missing in findings:
            print(
                f"  L{block_start} [missing-hard-break] metadata block "
                f"has {missing} non-last line(s) without a trailing `\\` or "
                f"two-trailing-spaces marker"
            )
            total_findings += missing

    if total_findings == 0:
        print("OK: no metadata-block line-break findings.")
        return 0

    print(
        f"\nFAIL: {total_findings} non-last metadata line(s) across "
        f"{files_flagged} file(s) lack a Markdown hard-break marker. "
        f"Each metadata-block line except the last must end with a "
        f"trailing `\\` (the library convention) or two-or-more trailing "
        f"spaces; otherwise GitHub soft-wraps the block into a paragraph."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
