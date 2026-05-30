#!/usr/bin/env python3
"""Enforce ISO 8601 (YYYY-MM-DD) date format in document metadata.

Every artefact document records its `**Date:**` field in the canonical
metadata block. This linter verifies that the field's value matches
the YYYY-MM-DD pattern and represents a real calendar date.

Scope:
- Metadata `**Date:** ...` line in every markdown file with a metadata block.
- Does not enforce ISO format for inline dates in prose (would produce
  false positives on legitimate phrasings like "the EU AI Act 2024").

Catches:
- Non-ISO date formats: "April 30, 2026", "4/30/2026", "30/04/2026", "2026/5/30".
- Two-digit years: "26-05-30".
- Implausible values: "2026-13-45".
- Missing zero-padding: "2026-5-30".

Usage:
    python3 tools/lint-date-format.py
    python3 tools/lint-date-format.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

DATE_FIELD_RE = re.compile(r"^\*\*Date:\*\*\s+(.+?)(?:\\)?$", re.MULTILINE)
ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    return True


def validate_date(value: str) -> str | None:
    """Return None if value is valid ISO 8601 date, else an error message."""
    value = value.strip()
    m = ISO_DATE_RE.match(value)
    if not m:
        return f"not ISO 8601 YYYY-MM-DD: {value!r}"
    y, mth, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if y < 1900 or y > 2100:
        return f"year {y} outside plausible range 1900-2100"
    try:
        date(y, mth, d)
    except ValueError as exc:
        return f"invalid calendar date: {exc}"
    # Check zero padding by exact length
    if len(m.group(2)) != 2 or len(m.group(3)) != 2:
        return f"missing zero padding: {value!r}"
    return None


# Literal placeholder values that appear in example/template metadata blocks
# (documents showing "here's what your metadata block should look like").
# These are documentation of the expected format, not actual dates.
PLACEHOLDER_VALUES = {"YYYY-MM-DD", "<YYYY-MM-DD>"}


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith("**Date:**"):
            # Strip trailing backslash (CommonMark hard-break syntax)
            value = line[len("**Date:**"):].rstrip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            value = value.strip()
            if not value:
                findings.append((lineno, "empty Date field"))
                continue
            if value in PLACEHOLDER_VALUES:
                # Template-syntax placeholder in an example block.
                continue
            err = validate_date(value)
            if err:
                findings.append((lineno, err))
    return findings


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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce ISO 8601 date format in document metadata."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all Date metadata fields are ISO 8601 (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"=== {rel} ===")
        for lineno, msg in findings:
            print(f"  L{lineno} [date-format] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} date-format finding(s) across {len(grouped)} file(s).")
    print("Metadata Date fields must be ISO 8601 YYYY-MM-DD with zero padding.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
