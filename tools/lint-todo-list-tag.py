#!/usr/bin/env python3
"""Detect an open backlog item heading with zero or 2+ [public]/[private]

list tags (gate 81).

Every open item (a ``| id | ... |`` index row in ``TODO.md``, and a ``### `` heading in the private
``grc_library_private/P-TODO.md``) must carry EXACTLY ONE
``[public]`` or ``[private]`` tag, the list-membership axis PR #1293
applied to all then-open items (design of record:
``todo-split-blocked-guardrail-design.md`` in the operational store). Nothing
mechanical enforced that going forward, so a new item could ship untagged,
or a copy-edit could accidentally leave both tags on a line. This gate is
the mechanical backstop.

Detection reads PUBLIC ``TODO.md`` items as index rows (``lint_common.parse_todo_index``);
private ``P-TODO.md`` items reuse audit-backlog-actionability.py's ITEM_HEADING_RE grammar
(the two tools must never disagree on what counts as an item). Findings are
keyed by the PHYSICAL LINE, not the captured id: ITEM_HEADING_RE's id group
captures only a shared prefix for a lettered sub-heading (``### 3.92.a ...``,
``### 3.92.b ...``, ``### 3.92.c ...`` all capture id ``"3.92"``), so keying
off the captured id could hide two untagged siblings behind one tagged one.

Adopter-graceful: when the private sibling is absent (public-only clone /
adopter checkout) the private list is simply not scanned; that is a no-op,
not an error. A default-lookup sibling that is present but unusable (not a
directory, a dangling link, or one that cannot be examined) is not absent: it
fails with exit 2 naming it. So does a sibling whose contents cannot be listed,
or whose ``P-TODO.md`` cannot be examined or is not a regular file, and so does
a ``P-TODO.md`` or ``TODO.md`` that is not valid UTF-8 (3b677). Only a sibling,
or a ``P-TODO.md`` in a readable sibling, that is genuinely absent (no entry at
the path) is skipped. The lookups probe with ``os.lstat``/``os.stat``, so the
verdict is the same on Python 3.11 and 3.12+.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from lint_common import InaccessiblePath, resolve_sibling, parse_todo_index, has_todo_index_header, print_degraded, require_dir, strict_kind

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


def find_untagged_index(text: str) -> list[tuple[int, str, int]]:
    """New-format TODO.md: every index row ``| id | title | tags |`` must carry
    exactly one [public]/[private] tag in its Tags cell. Returns (lineno, row,
    tag_count) for rows whose count != 1."""
    findings: list[tuple[int, str, int]] = []
    for it in parse_todo_index(text):
        count = sum(1 for t in it["tags"] if LIST_TAG_RE.search(t))
        if count != 1:
            findings.append((it["line"], f"{it['id']} {it['title']}", count))
    return findings


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Detect an open TODO/P-TODO item heading lacking "
        "exactly one [public]/[private] list tag."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Override the repository root TODO.md (and, if present, "
             "P-TODO.md) are read from (used by the regression fixtures for "
             "synthetic isolation).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    todo_path = REPO_ROOT / TODO_REL
    if not todo_path.is_file():
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2

    ptodo_path: Path | None
    private: Path | None = None
    if args.root is not None:
        cand = REPO_ROOT / PTODO_REL
        ptodo_path = cand if cand.is_file() else None
    else:
        # Strict (3b74): an ABSENT sibling still takes the degraded path below, but one that is
        # present and unusable (a file, a FIFO, a dangling link, an unsearchable parent) refuses.
        try:
            private = resolve_sibling("private", strict=True)
        except InaccessiblePath as exc:
            print(f"ERROR: the private sibling is present but unusable ({exc}); refusing "
                  f"the degraded path it would silently select.", file=sys.stderr)
            return 2
        cand = (private / PTODO_REL) if private is not None else None
        ptodo_path = None
        if cand is not None:
            # 3b677: probe as gate 90 does (list the sibling, then strict_kind), not with
            # Path.is_file, which reads a file in an unsearchable sibling as absent (3.12+) or
            # raises PermissionError (3.11). Only ENOENT in a readable sibling is absent.
            try:
                os.listdir(private)
                kind = strict_kind(cand)
            except OSError as exc:
                print(f"ERROR: the private sibling is present but unusable: cannot examine "
                      f"{exc.filename or cand} ({exc.strerror}).", file=sys.stderr)
                return 2
            if kind not in (None, "file"):
                print(f"ERROR: the private sibling is present but unusable: {cand} is present "
                      f"but is not a regular file.", file=sys.stderr)
                return 2
            ptodo_path = cand if kind == "file" else None

    # 3b677: a file that is not valid UTF-8 exits 2 naming it, as gate 90 does, not a traceback.
    reading = todo_path
    try:
        todo_text = todo_path.read_text(encoding="utf-8")
        reading = ptodo_path
        ptodo_text = ptodo_path.read_text(encoding="utf-8") if ptodo_path is not None else None
    except OSError as exc:
        print(f"ERROR: cannot read a required file: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: cannot decode {reading} as UTF-8 ({exc.reason} at byte {exc.start}).",
              file=sys.stderr)
        return 2

    sources: list[tuple[str, str]] = [(TODO_REL, todo_text)]
    if ptodo_text is not None:
        sources.append((PTODO_REL, ptodo_text))
    else:
        # 3b677: the default lookup skips for an absent sibling AND for a usable sibling with no
        # P-TODO.md in it; name the one that applies (a --root run keeps the first wording).
        if private is None:
            where = "no private sibling; public-only clone / adopter checkout"
            why = "no private sibling supplies it"
        else:
            where = f"the private sibling {private} has no {PTODO_REL}"
            why = f"the private sibling has no {PTODO_REL}"
        print(f"OK: {PTODO_REL} not present ({where}). Scanning {TODO_REL} only.")
        if args.root is None:
            # 3b635: the DEFAULT lookup's skip exits 0, so a green CI run must not read as a pass.
            print_degraded(
                "gate 81",
                f"gate 81 skipped the {PTODO_REL} list-tag check ({why}); "
                f"this pass attests nothing about it."
            )

    total_items = 0
    all_findings: list[tuple[str, int, str, int]] = []
    for rel, text in sources:
        # Both backlogs move to index form (2026-08); P-TODO.md is ### -block
        # pre-migration. UNION both parsers (F1793-4): check index rows AND any
        # leftover ### headings (deduped by captured id), so a mixed / half-
        # converted file cannot let an untagged legacy item pass. A pure file has
        # exactly one shape, so the other parser contributes nothing.
        # F1793-7: classify index form by the header, not any parseable row, so a
        # legacy item body table does not flip this to the index path.
        if has_todo_index_header(text):
            idx_items = parse_todo_index(text)
            total_items += len(idx_items)
            for lineno, line, count in find_untagged_index(text):
                all_findings.append((rel, lineno, line, count))
        # legacy ### headings (pure-index files carry none; their detail is in the
        # reference file). F1793-9: count every ### heading by PHYSICAL LINE, no
        # dedup by captured id (that key is only the numeric prefix for lettered
        # subheadings, which would drop ### 3.92.a/.b against an index row 3.92).
        for line in text.splitlines():
            if ITEM_HEADING_RE.match(line):
                total_items += 1
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
    print("Every open item (a TODO.md index row / a P-TODO.md ### heading) must carry EXACTLY ONE")
    print("[public] or [private] tag (PR #1293). Add the missing tag, or remove")
    print("the extra one (a TODO.md index-row Tags cell, or a P-TODO.md ### heading).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
