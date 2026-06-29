#!/usr/bin/env python3
"""Detect bare normative ``shall`` in authored corpus prose (gate 56).

The library's house style harmonizes normative requirement verbs on
``must`` (the FR-44 convention; see ``specification-master-project.md``).
A bare normative ``shall`` in authored prose is a regression of that
convention. Gate 9 (``lint-shall-near-uncertainty.py``) only fires when
``shall`` sits adjacent to an uncertainty marker, so the plain normative
form is gate-9-blind; this gate closes that gap mechanically (it would
have caught the #455 miss in ``dev-security/policy-secure-development-and-engineering.md``
that the next session's corpus-wide ``/validate`` had to find by hand).

Three classes are deliberately preserved (NOT flagged), matching the
FR-44 sweep's preserved set:

  1. The gate-9 linter filename token ``lint-shall-near-uncertainty.py``
     (and any other hyphenated identifier embedding ``shall``). The
     detection requires non-word, non-hyphen boundaries around ``shall``,
     so a hyphenated identifier never matches.
  2. Backticked ``shall`` word-references (the word discussed as a token,
     e.g. ``No library `shall` operates ...``). Inline backtick spans are
     stripped before matching.
  3. Verbatim source extracts / quotes. Fenced code blocks are skipped
     (via ``iter_non_code_lines``) and blockquote lines (Markdown ``>``)
     are skipped, since the house style exempts verbatim quotes.

Files in EXEMPT_FILES (the CHANGELOG and the master / ingestion
specifications and the ingestion instruction, which legitimately discuss
the convention and its target word) are skipped, mirroring gate 9.

Scope: ``README.md``, ``NOTICE.md``, and the audited domain directories
(splatted from ``lint_common`` so the scan-scope-parity gate is satisfied).

Usage:
    python3 tools/lint-bare-normative-shall.py
    python3 tools/lint-bare-normative-shall.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

# A bare normative ``shall``: the word standing free, not part of a
# hyphenated identifier (e.g. ``lint-shall-near-uncertainty``) and not a
# substring of another word (e.g. ``Marshall``). Case-insensitive so a
# sentence-initial ``Shall`` is also caught.
BARE_SHALL = re.compile(r"(?<![A-Za-z0-9_-])shall(?![A-Za-z0-9_-])", re.IGNORECASE)

# Inline backtick code spans: stripped before matching so a backticked
# ``shall`` word-reference (preserved class 2) does not register.
INLINE_CODE_SPAN = re.compile(r"`[^`]*`")

# Files that legitimately discuss the convention and its target word.
# Mirrors gate 9's EXEMPT_FILES.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
]


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


def check_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (lineno, line_snippet) findings."""
    relative = path.relative_to(REPO_ROOT).as_posix()
    if relative in EXEMPT_FILES:
        return []

    text = read_text_safe(path)
    if text is None:
        return []

    findings: list[tuple[int, str]] = []
    for lineno, line in iter_non_code_lines(text):
        # Preserved class 3: verbatim quotes carried as Markdown blockquotes.
        if line.lstrip().startswith(">"):
            continue
        # Preserved class 2: strip inline backtick spans so a backticked
        # ``shall`` word-reference does not register.
        stripped = INLINE_CODE_SPAN.sub("", line)
        if BARE_SHALL.search(stripped):
            findings.append((lineno, line.strip()[:150]))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect bare normative 'shall' in authored corpus prose."
    )
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])

    paths = args.paths or DEFAULT_PATHS
    files = iter_markdown_files(paths)

    grouped: dict[str, list[tuple[int, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        findings = check_file(f)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no bare normative 'shall' in authored corpus prose.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, snippet in findings:
            print(f"  L{lineno} {snippet}")

    print(f"\nFAIL: {total} bare normative 'shall' finding(s) across {len(grouped)} file(s).")
    print("The house style harmonizes normative verbs on 'must' (FR-44). Convert 'shall' to 'must',")
    print("or, for a preserved case, backtick a word-reference / use a blockquote for a verbatim quote.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
