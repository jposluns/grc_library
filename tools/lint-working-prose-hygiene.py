#!/usr/bin/env python3
"""Prose-hygiene audit for the `.working/` maintainer working tree (gate 51).

The corpus-wide language gate (`lint-language.py`, gate 19) forbids em-dashes
(`—`) and en-dashes (`–`) in prose, but it exempts the `.working/` tree (the
maintainer working space is in `DEFAULT_EXEMPT_DIRS`). The 2026-06-26 em-dash
conformance pass (#353) brought `.working/` prose into line with the house
style, leaving a small set of *intentional* em/en-dash literals inside inline
code spans (regex character classes such as ``[–—]``, frozen historical
quotes, the house-style rule's own glyph examples). This gate ratchets that
conformance: it forbids em/en-dashes in `.working/` PROSE while ALLOWING them
inside inline code spans, so the conformance cannot silently regress.

The principled boundary (established by the #353 bulk apply): a dash is a
prose violation only if it appears outside an inline code span and outside a
fenced code block. Dashes inside code spans are content (a regex literal, a
quoted format string), not prose, and are left untouched.

Scope is the `.working/` tree ONLY. The corpus proper is covered by
`lint-language.py`; the root `CHANGELOG.md`'s historical entries carry
legitimate en-dashes and are covered at PR time by the D3 dash gate
(`check-changelog-dash.py`), so this gate does NOT full-scan `CHANGELOG.md`.

Detection logic, per line outside a fenced block (`iter_non_code_lines`):

  1. Strip inline code spans with the standard CommonMark code-span regex
     ``(`+)(.+?)\\1`` (a run of N backticks, content, a closing run of N
     backticks). This correctly handles single- and multi-backtick spans and
     spans whose content contains backticks (e.g. the self-referential line in
     `session-handoff.md` that quotes this very regex), which a naive
     ``` `[^`]*` ``` strip would mis-pair.
  2. Flag any em-dash or en-dash remaining in the residue.

Usage:
    python3 tools/lint-working-prose-hygiene.py [paths...]

With no arguments, scans the `.working/` tree. A path argument (file or
directory) overrides the default, which the regression fixtures rely on to
point the gate at a single test file. Exits non-zero if any finding is
reported.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import iter_markdown_targets, iter_non_code_lines, read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCAN_PATHS = [str(REPO_ROOT / ".working")]

# The `.working` tree is in DEFAULT_EXEMPT_DIRS for every other linter; this
# gate deliberately overrides that exemption to scan inside it. The remaining
# exemptions are the universal non-content dirs.
EXEMPT_DIRS = frozenset({".git", "node_modules", "__pycache__"})

# Standard CommonMark inline code span: an opening run of N backticks, the
# shortest content, then a closing run of exactly N backticks. Stripping these
# leaves only prose (and any unmatched backtick, which carries no dash).
CODE_SPAN_PATTERN = re.compile(r"(`+)(.+?)\1")
EM_DASH_PATTERN = re.compile(r"[—–]")  # em dash or en dash


def strip_inline_code(line: str) -> str:
    """Return ``line`` with inline code spans removed."""
    return CODE_SPAN_PATTERN.sub("", line)


def check_file(path: Path) -> list[tuple[int, str]]:
    """Return ``(lineno, snippet)`` for each prose em/en-dash in ``path``."""
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        residue = strip_inline_code(line)
        if EM_DASH_PATTERN.search(residue):
            findings.append((lineno, line.strip()))
    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or DEFAULT_SCAN_PATHS
    files = iter_markdown_targets(paths, exempt_dirs=EXEMPT_DIRS)

    grouped: dict[str, list[tuple[int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for lineno, snippet in check_file(f):
            grouped[f.relative_to(REPO_ROOT).as_posix()].append((lineno, snippet))
            total += 1

    if not grouped:
        print(f"OK: no prose em/en-dashes in {len(files)} .working/ file(s).")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, snippet in grouped[relpath]:
            print(f"  L{lineno} [prose-dash] {snippet[:160]}")

    print(f"\nFAIL: {total} prose em/en-dash finding(s) across {len(grouped)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
