#!/usr/bin/env python3
"""Metadata-block line-break audit.

Detect runs of consecutive ``**Field:**`` lines that lack a Markdown
hard-break marker on the non-last lines of the run. Without a hard-break,
GitHub renders the metadata block as a single soft-wrapped paragraph
rather than as a vertical list of labelled facts.

Markdown supports two hard-break markers, both of which this linter
treats as valid:

  1. A trailing backslash at end of line (``\\``).
  2. Two or more trailing spaces.

The library convention is the backslash form (see [`README.md`](README.md)
metadata block and every governed document); both are accepted to avoid
flagging documents authored in environments that strip trailing
backslashes or insert hard breaks via trailing whitespace.

Fenced code blocks are skipped via [`tools/lint_common.py`](lint_common.py)
``iter_non_code_lines``, so templates that demonstrate metadata format
inside ``` ``` ``` regions (e.g. [`CONTRIBUTING.md`](../CONTRIBUTING.md),
[`docs/worked-example.md`](../docs/worked-example.md)) are not
false-positives. The last line in a run is exempt from the requirement
because the convention is that the next line is a blank line or a
``---`` separator, which already creates a paragraph break.

Usage:

    python3 tools/lint-metadata-line-breaks.py
    python3 tools/lint-metadata-line-breaks.py path/to/specific/file.md

The optional positional path argument restricts the scan to one file,
used by the gate-34 regression test suite for synthetic-fixture
isolation.

Exit codes:
    0   no findings.
    1   one or more files have at least one metadata block with a
        non-last line missing the hard-break marker.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, iter_non_code_lines, read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent

META_LINE = re.compile(r"^\*\*[A-Za-z][A-Za-z0-9 ]*:\*\*")

DEFAULT_TARGETS = [
    "README.md",
    "CONTRIBUTING.md",
    "NOTICE.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "TODO.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "docs",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
]


def has_hard_break(line: str) -> bool:
    """A line has a Markdown hard-break marker if it ends with ``\\`` or two-plus spaces."""
    if line.endswith("\\"):
        return True
    if len(line) >= 2 and line.endswith("  "):
        return True
    return False


def scan_file(path: Path) -> list[tuple[int, int]]:
    """Return ``[(block_start_line, missing_count), ...]`` for every offending block."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, int]] = []
    block: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal block
        if len(block) >= 2:
            non_last = block[:-1]
            missing = sum(1 for _, ln in non_last if not has_hard_break(ln))
            if missing:
                findings.append((block[0][0], missing))
        block = []

    for lineno, line in iter_non_code_lines(text):
        if META_LINE.match(line):
            block.append((lineno, line))
        else:
            flush()
    flush()
    return findings


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
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit metadata-block line breaks across the markdown corpus."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Optional specific .md file to scan (default: all corpus directories).",
    )
    args = parser.parse_args(argv)

    if args.path is not None:
        target = Path(args.path)
        if not target.is_absolute():
            target = REPO_ROOT / target
        files = [target] if target.is_file() else []
    else:
        files = iter_target_files(DEFAULT_TARGETS)

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
