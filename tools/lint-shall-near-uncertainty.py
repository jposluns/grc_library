#!/usr/bin/env python3
"""Detect mandatory requirements near uncertainty markers.

A mandatory requirement adjacent to an uncertainty marker signals an
unfinished requirement that should not yet be presented as mandatory.
This linter catches such patterns.

Mandatory markers detected: ``shall``, ``must``, ``is required``,
``are required``, ``will be required``. (Bare ``will`` is NOT a
mandatory marker in this linter — too many false positives in
descriptive/future-tense prose such as "the user will see ...".
Only the multi-word ``will be required`` form is detected.)

Uncertainty markers detected: ``[Unverified]``, ``Draft``, ``TBD``,
``FIXME``, ``XXX``, ``placeholder``, ``TODO``, and ``[Draft N Reference]``.

Boundary with the placeholder-leakage audit (``lint-placeholder-leakage.py``):
the two linters share five identical marker tokens (TODO, TBD, FIXME, XXX,
[Unverified]) plus a sixth in differing forms (that linter matches only the
parenthesized ``(placeholder)``; this one matches bare ``placeholder``), and
split by PRESENCE vs CONJUNCTION: that linter flags a marker's mere presence
in a scanned document, while this one flags only a MANDATORY marker within
the window of an uncertainty marker. Each maintains its own token list and
exempt set, so a token added to one is not automatically checked by the
other; extend both deliberately.

The linter detects a finding when a mandatory marker appears within
WINDOW_LINES (=2) lines above or below an uncertainty marker (a 5-line
window centred on the uncertainty marker line). Fenced code blocks are
skipped.

Examples this catches:

  - "[Unverified] The organization shall implement ..."
  - "Draft 2026 X Revision ... shall be ..."
  - "TODO: define the threshold; the organization must ..."

Files in EXEMPT_FILES (the CHANGELOG, the project and ingestion
master specifications, and the document-ingestion instruction, all
of which legitimately discuss this rule and inevitably contain its
target patterns) are skipped.

Usage:
    python3 tools/lint-shall-near-uncertainty.py
    python3 tools/lint-shall-near-uncertainty.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, read_text_safe

# Uncertainty markers that should not appear in mandatory text.
UNCERTAINTY_PATTERNS = [
    re.compile(r"\[Unverified\]"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bTODO\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"\bXXX\b"),
    # "Draft" followed by a year or generic noun suggesting an unpublished doc.
    re.compile(r"\bDraft\s+(20\d{2}|[A-Z][a-z]+)"),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
    re.compile(r"\[Draft\s*\d*\s*Reference\]"),
]

# Mandatory-requirement words; matched in the same line OR within a small window.
MANDATORY_PATTERN = re.compile(r"\b(shall|must|will be required|is required|are required)\b", re.IGNORECASE)

# Files exempt from this check:
# - CHANGELOG records historical defects using these markers.
# - The project and ingestion master specifications discuss the markers
#   as rule patterns.
# - The document-ingestion instruction references the markers.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
}
# Note: tools/*.py entries were previously listed here but are
# unreachable — the linter only scans .md targets via
# iter_markdown_targets, so Python sources are never seen.
# Removed in Phase 23.59.

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
]

# Window: report uncertainty + mandatory if they appear within N lines of each other.
WINDOW_LINES = 2


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = REPO_ROOT / p
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    return sorted(set(files))


def check_file(path: Path) -> list[tuple[int, str, str]]:
    """Return list of (lineno, uncertainty_match, line_snippet) findings."""
    relative = path.relative_to(REPO_ROOT).as_posix()
    if relative in EXEMPT_FILES:
        return []

    text = read_text_safe(path)
    if text is None:
        return []
    lines = text.splitlines()
    findings: list[tuple[int, str, str]] = []

    # Pre-compute the set of line indices that fall inside a fenced
    # code block. Both passes consult this set so a mandatory marker
    # inside a code block within window range of an uncertainty marker
    # outside the code block is correctly skipped (and vice versa).
    in_code_lines: set[int] = set()
    in_code_block = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            in_code_lines.add(i)  # the fence line itself is also non-content
            continue
        if in_code_block:
            in_code_lines.add(i)

    # First pass: locate uncertainty markers outside code blocks.
    uncertainty_lines: dict[int, str] = {}
    for i, line in enumerate(lines):
        if i in in_code_lines:
            continue
        for pat in UNCERTAINTY_PATTERNS:
            m = pat.search(line)
            if m:
                uncertainty_lines[i] = m.group(0)
                break

    # Second pass: scan a window around each uncertainty marker for
    # mandatory words. Skip mandatory-marker lines that sit inside a
    # code block — they are example syntax, not prescriptive prose.
    for u_line, u_marker in uncertainty_lines.items():
        lo = max(0, u_line - WINDOW_LINES)
        hi = min(len(lines), u_line + WINDOW_LINES + 1)
        for i in range(lo, hi):
            if i in in_code_lines:
                continue
            if MANDATORY_PATTERN.search(lines[i]):
                findings.append((u_line + 1, u_marker, lines[u_line].strip()[:150]))
                break

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Detect mandatory requirements near uncertainty markers.")
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])

    paths = args.paths or DEFAULT_PATHS
    files = iter_markdown_files(paths)

    grouped: dict[str, list[tuple[int, str, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        findings = check_file(f)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no mandatory-near-uncertainty findings.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, marker, snippet in findings:
            print(f"  L{lineno} [near {marker}] {snippet}")

    print(f"\nFAIL: {total} finding(s) across {len(grouped)} file(s).")
    print("Mandatory shall/must/will requirements should not appear next to uncertainty markers.")
    print("Either complete the requirement (remove the marker) or soften the language (may, recommended).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
