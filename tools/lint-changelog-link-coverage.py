#!/usr/bin/env python3
"""Enforce that file references in CHANGELOG.md are markdown links.

Earlier-phase CHANGELOG entries recorded file references as code-formatted
text only (`path/to/file.md`). Phase 23.11 converted all such references to
markdown links so a reader can navigate from a CHANGELOG entry to the
referenced file in one click. This linter enforces that convention going
forward: every backtick-wrapped file-path-shaped string in CHANGELOG.md
must be wrapped in a markdown link.

A reference qualifies as a file path if it:
- is enclosed in backticks: `...`
- contains at least one of: a directory separator (/), or matches a known
  top-level filename pattern (README.md, CHANGELOG.md, NOTICE.md, etc.)
- ends with a recognized file extension (.md, .py, .yaml, .yml, .json,
  .txt, .cff, .toml)

A reference is correctly linked if it appears as: [`path`](path) or
[`path`](resolved-path) with the bracketed code-formatted path matching
the link target's file basename or relative path.

Usage:
    python3 tools/lint-changelog-link-coverage.py
    python3 tools/lint-changelog-link-coverage.py path/to/CHANGELOG.md

Exit codes:
    0   no findings; every backtick file reference is linked
    1   one or more unlinked backtick file references present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = REPO_ROOT / "CHANGELOG.md"

FILE_EXTENSIONS = (
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".cff",
    ".toml",
)

# Top-level filenames or dotfiles that may appear without directory prefix
# and should still be linked.
TOP_LEVEL_FILES = {
    "README.md",
    "CHANGELOG.md",
    "NOTICE.md",
    "LICENSE",
    "CITATION.cff",
    "AUTHORS.md",
    "TODO.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "taxonomy.yml",
    ".pre-commit-config.yaml",
    "specification-ingestion.md",
    "specification-master-project.md",
}


def looks_like_file_reference(text: str) -> bool:
    """Return True if a backtick-wrapped string looks like a file path.

    A reference looks like a file if it has a directory separator and a known
    extension, or matches a known top-level filename.
    """
    if "/" in text and text.endswith(FILE_EXTENSIONS):
        return True
    if text in TOP_LEVEL_FILES:
        return True
    # bare filenames with recognized extensions
    if "/" not in text and text.endswith(FILE_EXTENSIONS) and re.match(r"^[A-Za-z0-9_\-.]+$", text):
        return True
    return False


def scan(path: Path) -> list[tuple[int, str]]:
    """Return list of (line number, backtick reference) findings.

    Each finding is a backtick-wrapped file reference that is NOT wrapped in
    a markdown link.
    """
    if not path.exists():
        return []
    findings: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8")
    # Strip code blocks (```...```) so backticks inside code blocks are ignored.
    # CHANGELOG.md may contain code blocks for examples; references inside them
    # are not navigation targets.
    in_code_block = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Walk the line looking for backtick-wrapped strings.
        i = 0
        while i < len(line):
            # Skip already-linked references: [`...`](...)
            if line[i] == "[" and i + 1 < len(line) and line[i + 1] == "`":
                # Find the matching `](
                close = line.find("](", i + 2)
                if close != -1:
                    paren_close = line.find(")", close + 2)
                    if paren_close != -1:
                        # entire [`...`](...) is one consumed unit
                        i = paren_close + 1
                        continue
            # Find a backtick
            if line[i] != "`":
                i += 1
                continue
            # Single backtick start
            end = line.find("`", i + 1)
            if end == -1:
                # unterminated
                break
            inner = line[i + 1 : end]
            if looks_like_file_reference(inner):
                findings.append((lineno, inner))
            i = end + 1
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce markdown-link wrapping for file references in CHANGELOG.md."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[str(DEFAULT_TARGET)],
        help="Path(s) to check (default: CHANGELOG.md at repo root).",
    )
    args = parser.parse_args(argv[1:])
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for p in args.paths:
        path = Path(p)
        findings = scan(path)
        if findings:
            grouped[path] = findings
    if not grouped:
        print("OK: every backtick file reference in CHANGELOG is linked.")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"=== {rel} ===")
        for lineno, ref in findings:
            print(f"  L{lineno} [unlinked-file-ref] `{ref}`")
        total += len(findings)
    print(
        f"\nFAIL: {total} unlinked file reference(s) across {len(grouped)} file(s)."
    )
    print(
        "File references in CHANGELOG must be wrapped in markdown links so "
        "readers can navigate to the referenced file. Convert `path/to/file.md` "
        "to [`path/to/file.md`](path/to/file.md)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
