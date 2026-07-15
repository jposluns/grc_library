#!/usr/bin/env python3
"""Flag renumber-fragile positional backlog-token references in corpus prose.

A reference like ``TODO §4.10``, ``TODO item 3.4``, or ``backlog item P4.17``
points at a backlog item by its POSITION in `TODO.md`. A backlog item's number retires when the item
closes (so such a reference dangles), and items numbered before the permanent-
numbering rule were historically renumbered; either way a positional reference in
a durable corpus document can dangle or point at a different item. The stable
form is the item's coded id (`FR-N`, `GR-N`, `SR-N`) or its topic name. This gate
flags the fragile form so authors reword toward the stable one, the same class as
the CLAUDE.md section-close cross-file cleanup guard, made mechanical for the corpus.

Scope: authored corpus prose only. The pack subtree
``dev-security/claude-rules/`` is EXEMPT (its README version-history legitimately
narrates past PRs by their then-current backlog position), as are ``CHANGELOG.md``
and ``TODO.md`` itself (the backlog is the source of the numbering, not a fragile
external reference to it), and the ``.working`` / ``.claude`` trees (already outside
the corpus scan set). Only references QUALIFIED by ``TODO`` (optionally
``TODO item(s)``) or ``backlog item(s)`` are flagged; a document's own internal
``§N`` section cross-reference is not.

Usage:
    python3 tools/lint-positional-backlog-tokens.py
    python3 tools/lint-positional-backlog-tokens.py path1 path2 ...

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

# A positional backlog reference: TODO / TODO item(s) / backlog item(s), then a
# section-shaped token (a `§`- or `P`-prefixed number, or a dotted N.M). A bare
# single digit with no prefix and no dot is deliberately NOT matched (too
# ambiguous to be false-positive-free), so an optional `item(s)` qualifier
# between `TODO` and the token only ever matches when a section token follows
# (ordinary prose like "the financial-services TODO item covers ..." has no
# token and is not flagged). Case-sensitive TODO; "item(s)" / "backlog item(s)"
# either case.
POSITIONAL_REF = re.compile(
    r"(?<![\w-])(?:TODO(?:\s+[Ii]tems?)?|[Bb]acklog items?)\s+(?:(?:§|P)\d+(?:\.\d+)*|\d+\.\d+)\b"
)

INLINE_CODE_SPAN = re.compile(r"`[^`]*`")

# Files exempt from this gate (the backlog source, the append-only history).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
}

# Path prefixes exempt from this gate. The pack subtree carries AI-assistant
# guidance whose README version-history narrates past PRs positionally.
EXEMPT_PREFIXES = (
    "dev-security/claude-rules/",
)

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
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
    relative = path.relative_to(REPO_ROOT).as_posix()
    if relative in EXEMPT_FILES:
        return []
    if any(relative.startswith(p) for p in EXEMPT_PREFIXES):
        return []
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, str]] = []
    for lineno, line in iter_non_code_lines(text):
        if line.lstrip().startswith(">"):
            continue
        stripped = INLINE_CODE_SPAN.sub("", line)
        m = POSITIONAL_REF.search(stripped)
        if m:
            findings.append((lineno, m.group(0)))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Flag renumber-fragile positional backlog-token references.")
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
        print("OK: no renumber-fragile positional backlog-token references in "
              "corpus prose.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, token in findings:
            print(f"  line {lineno}: {token!r} (reword to the stable coded id "
                  f"FR-N / GR-N / SR-N or the topic name)")
    print(f"\nFAIL: {total} positional backlog reference(s) in corpus prose.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
