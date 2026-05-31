#!/usr/bin/env python3
"""Enforce ISO 8601 (YYYY-MM-DD) date format in document metadata.

Every artefact document records its `**Date:**` field in the canonical
metadata block. This linter verifies that the field's value matches
the YYYY-MM-DD pattern and represents a real calendar date.

Scope:
- Metadata `**Date:** ...` line in every markdown file with a metadata block.
- Does not enforce ISO format for inline dates in prose (would produce
  false positives on legitimate phrasings like "the EU AI Act 2024").
- **Fenced code blocks are skipped.** A `**Date:**` line inside a
  ``` ``` ``` block is documentation showing the metadata-block
  format (e.g., as in README, CONTRIBUTING, the ingestion spec), not
  the file's own metadata. Skipping code blocks via the shared
  `iter_non_code_lines` helper is the structurally-correct way to
  distinguish "real metadata" from "documentation example", instead
  of maintaining an inline allowlist of files known to contain
  examples.

Catches:
- Non-ISO date formats: "April 30, 2026", "4/30/2026", "30/04/2026", "2026/5/30".
- Two-digit years: "26-05-30".
- Implausible values: "2026-13-45".
- Missing zero-padding: "2026-5-30".
- Years outside the plausible 1900-2100 range.

Placeholder permissions:
- ``YYYY-MM-DD`` and ``<YYYY-MM-DD>`` are permitted ONLY in files whose
  name starts with ``template-`` or ``worklist-``. Those files carry
  fill-in markers by design.
- Placeholder Date values in production artefacts are flagged as
  findings. The previous file-identity allowlist
  (``PLACEHOLDER_EXEMPT_FILES``) was retired in Phase 23.57 in favour
  of the code-block-skipping rule above.

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

from lint_common import REPO_ROOT, iter_markdown_targets, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

DATE_FIELD_RE = re.compile(r"^\*\*Date:\*\*\s+(.+?)(?:\\)?$", re.MULTILINE)
ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


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


# Literal placeholder values that appear in template/worklist metadata
# blocks (which carry fill-in markers by design). Production artefacts
# (anything not prefixed `template-` or `worklist-`) may not use these.
PLACEHOLDER_VALUES = {"YYYY-MM-DD", "<YYYY-MM-DD>"}


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    # Placeholder Date values are only legitimate in templates and
    # worklists (which carry fill-in markers as their own metadata).
    is_placeholder_eligible = (
        path.name.startswith("template-")
        or path.name.startswith("worklist-")
    )
    # Iterate only outside fenced code blocks. A `**Date:**` line
    # inside a code block is documentation showing the metadata-block
    # format, not the file's own metadata, and is not validated.
    for lineno, line in iter_non_code_lines(text):
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
                if is_placeholder_eligible:
                    # Template/worklist's own metadata is a fill-in marker.
                    continue
                findings.append((lineno, f"placeholder Date {value!r} in non-template file"))
                continue
            err = validate_date(value)
            if err:
                findings.append((lineno, err))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce ISO 8601 date format in document metadata."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_markdown_targets(args.paths)
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
