#!/usr/bin/env python3
"""Detect mandatory requirements near uncertainty markers.

A `shall`, `must`, or `will` requirement adjacent to an `[Unverified]`, `Draft`,
`TBD`, `FIXME`, `XXX`, or `placeholder` marker signals an unfinished requirement
that should not yet be presented as mandatory. This linter catches such patterns.

Examples this catches:
- "[Unverified] The organisation shall implement ..."
- "Draft 2026 X Revision ... shall be ..."
- "TODO: define the threshold; the organisation must ..."

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

REPO_ROOT = Path(__file__).resolve().parent.parent

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
# - The specifications which legitimately discuss these markers as patterns.
# - CHANGELOG which records historical defects.
# - This linter itself.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    "tools/lint-shall-near-uncertainty.py",
    "tools/lint-citations.py",
    "tools/lint-language.py",
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "sectors",
    "security",
    "supply-chain",
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

    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[tuple[int, str, str]] = []
    in_code_block = False

    # First pass: locate uncertainty markers.
    uncertainty_lines: dict[int, str] = {}
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for pat in UNCERTAINTY_PATTERNS:
            m = pat.search(line)
            if m:
                uncertainty_lines[i] = m.group(0)
                break

    # Second pass: scan a window around each uncertainty marker for mandatory words.
    for u_line, u_marker in uncertainty_lines.items():
        lo = max(0, u_line - WINDOW_LINES)
        hi = min(len(lines), u_line + WINDOW_LINES + 1)
        for i in range(lo, hi):
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
