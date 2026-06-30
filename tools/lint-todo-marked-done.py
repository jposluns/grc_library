#!/usr/bin/env python3
"""Detect a TODO item that marks ITSELF done in place (gate 57).

The TODO/DONE rotation discipline (the change-tracking rule's
PR-finalization protocol) requires that when a PR closes a backlog item,
the item is DELETED from ``TODO.md`` and an entry is added to
``.working/DONE.md`` in the same diff, not annotated done-in-place.
``TODO.md`` is forward-looking; a self-marked-done item is rotation
debris that the rule explicitly forbids ("Removal means deletion of the
line ... not a strikethrough, not a '[done]' suffix, not a
'Status: completed' annotation").

This is the marked-done detector half of the TODO/DONE-rotation
bookkeeping-parity gate family (maintainer-decided "Option B", the
project's §4.10). It is the static, content-side check: it flags a TODO
item that self-marks done. Its companion, the CHANGELOG-asserts-closure
PR-time check, catches the *wholesale-forgotten* rotation (where TODO is
never edited at all, so there is nothing self-marked to detect here).

Detected self-done markers (each a STRUCTURAL marker that never appears
in legitimate open-item prose, so the gate is false-positive-free):

  1. A Markdown strikethrough span ``~~...~~`` (an item struck through
     instead of deleted).
  2. A done tag ``[done]`` / ``[completed]`` (case-insensitive), the
     ``[done]`` suffix the rule names.
  3. A ``Status: completed`` / ``Status: done`` field on an item.

Deliberately NOT detected: a bare ``SHIPPED`` word. ``SHIPPED`` appears
legitimately in open-item prose describing shipped SUB-parts of a
still-open multi-part item (e.g. FR-167's "the ... column SHIPPED in
PR-B" while FR-167 itself was still open), which is exactly the multi-part
false-positive class that rejected the id-cross-check design. The
shipped-but-unrotated case is covered instead by the companion
CHANGELOG-asserts-closure PR-time check, which keys on the closure
assertion and the diff, not on a word in prose.

Inline backtick spans are stripped and fenced code blocks are skipped
before matching, so a backticked mention of these markers (as in this
file's own design note in ``TODO.md``) does not register.

Scope: ``TODO.md`` only. ``.working/DONE.md`` is the done ledger and
legitimately carries done items, so it is never scanned.

Usage:
    python3 tools/lint-todo-marked-done.py
    python3 tools/lint-todo-marked-done.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, iter_non_code_lines, read_text_safe

# Markdown strikethrough span: an item struck through in place.
STRIKETHROUGH = re.compile(r"~~[^~]+~~")

# A bracketed done tag used as a status suffix.
DONE_TAG = re.compile(r"\[(?:done|completed)\]", re.IGNORECASE)

# A Status: completed / Status: done field on an item.
STATUS_DONE = re.compile(r"\bStatus:\s*(?:completed|done)\b", re.IGNORECASE)

# Inline backtick code spans: stripped before matching so a backticked
# mention of a marker (e.g. this gate's own design note that names
# ``~~`` and ``[done]``) does not register.
INLINE_CODE_SPAN = re.compile(r"`[^`]*`")

DEFAULT_PATHS = ["TODO.md"]


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
    """Return list of (lineno, marker, line_snippet) findings."""
    text = read_text_safe(path)
    if text is None:
        return []

    findings: list[tuple[int, str, str]] = []
    for lineno, line in iter_non_code_lines(text):
        stripped = INLINE_CODE_SPAN.sub("", line)
        if STRIKETHROUGH.search(stripped):
            findings.append((lineno, "strikethrough ~~...~~", line.strip()[:150]))
        elif DONE_TAG.search(stripped):
            findings.append((lineno, "[done]/[completed] tag", line.strip()[:150]))
        elif STATUS_DONE.search(stripped):
            findings.append((lineno, "Status: completed/done", line.strip()[:150]))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect a TODO item that marks itself done in place."
    )
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
        print("OK: no self-marked-done items in TODO.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, marker, snippet in findings:
            print(f"  L{lineno} [{marker}] {snippet}")

    print(f"\nFAIL: {total} self-marked-done item(s) across {len(grouped)} file(s).")
    print("TODO is forward-looking: a closed item is DELETED from TODO and added to")
    print(".working/DONE.md in the same PR, not annotated done-in-place. Rotate the item.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
