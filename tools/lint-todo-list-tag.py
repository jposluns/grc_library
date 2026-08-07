#!/usr/bin/env python3
"""Detect an open backlog item heading with zero or 2+ [public]/[private]
list tags (gate 81).

Every open ``### `` item heading in ``TODO.md`` (and, when present, the
private ``grc_library_private/P-TODO.md``) must carry EXACTLY ONE
``[public]`` or ``[private]`` tag, the list-membership axis PR #1293
applied to all then-open items (design of record:
``grc_library_private/.working/todo-split-blocked-guardrail-design.md``). Nothing
mechanical enforced that going forward, so a new item could ship untagged,
or a copy-edit could accidentally leave both tags on a line. This gate is
the mechanical backstop.

Detection reuses audit-backlog-actionability.py's ITEM_HEADING_RE grammar
(the two tools must never disagree on what counts as an item). Findings are
keyed by the PHYSICAL LINE, not the captured id: ITEM_HEADING_RE's id group
captures only a shared prefix for a lettered sub-heading (``### 3.92.a ...``,
``### 3.92.b ...``, ``### 3.92.c ...`` all capture id ``"3.92"``), so keying
off the captured id could hide two untagged siblings behind one tagged one.

Adopter-graceful: when the private sibling is absent (public-only clone /
adopter checkout) the private list is simply not scanned; that is a no-op,
not an error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import resolve_sibling

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

TODO_REL = "TODO.md"
PTODO_REL = "P-TODO.md"

ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)

LIST_TAG_RE = re.compile(r"\[(public|private)\]")


def find_untagged_or_ambiguous(text: str) -> list[tuple[int, str, int]]:
    """Return (lineno, heading_line, tag_count) for every heading whose tag
    count is not exactly 1. Keyed by LINE, not captured id."""
    findings: list[tuple[int, str, int]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if ITEM_HEADING_RE.match(line):
            count = len(LIST_TAG_RE.findall(line))
            if count != 1:
                findings.append((lineno, line, count))
    return findings


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Detect an open TODO/P-TODO item heading lacking "
        "exactly one [public]/[private] list tag."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override the repository root TODO.md (and, if present, "
             "P-TODO.md) are read from (used by the regression fixtures for "
             "synthetic isolation).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    todo_path = REPO_ROOT / TODO_REL
    if not todo_path.is_file():
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2

    ptodo_path: Path | None
    if args.root is not None:
        cand = REPO_ROOT / PTODO_REL
        ptodo_path = cand if cand.is_file() else None
    else:
        private = resolve_sibling("private")
        cand = (private / PTODO_REL) if private is not None else None
        ptodo_path = cand if (cand is not None and cand.is_file()) else None

    try:
        todo_text = todo_path.read_text(encoding="utf-8")
        ptodo_text = ptodo_path.read_text(encoding="utf-8") if ptodo_path is not None else None
    except OSError as exc:
        print(f"ERROR: cannot read a required file: {exc}", file=sys.stderr)
        return 2

    sources: list[tuple[str, str]] = [(TODO_REL, todo_text)]
    if ptodo_text is not None:
        sources.append((PTODO_REL, ptodo_text))
    else:
        print(
            f"OK: {PTODO_REL} not present (no private sibling; public-only "
            f"clone / adopter checkout). Scanning {TODO_REL} only."
        )

    total_items = 0
    all_findings: list[tuple[str, int, str, int]] = []
    for rel, text in sources:
        total_items += sum(1 for line in text.splitlines() if ITEM_HEADING_RE.match(line))
        for lineno, line, count in find_untagged_or_ambiguous(text):
            all_findings.append((rel, lineno, line, count))

    if not all_findings:
        print(
            f"OK: {total_items} open item heading(s) across {len(sources)} "
            f"file(s); every heading carries exactly one [public]/[private] "
            f"list tag."
        )
        return 0

    print("=== item headings with zero or 2+ [public]/[private] tags ===")
    for rel, lineno, line, count in all_findings:
        reason = "no list tag" if count == 0 else f"{count} list tags (ambiguous)"
        print(f"  {rel}:{lineno}: {reason}: {line.strip()}")

    print(f"\nFAIL: {len(all_findings)} list-tag finding(s).")
    print("Every open TODO.md / P-TODO.md item heading must carry EXACTLY ONE")
    print("[public] or [private] tag (PR #1293). Add the missing tag, or remove")
    print("the extra one, on the heading line itself.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
