#!/usr/bin/env python3
"""TODO-marked-done audit (grc gate): pack-owned engine (source of record).

Flag a backlog item that marks itself done IN PLACE rather than being removed: a
strikethrough span (``~~...~~``), a bracketed ``[done]`` / ``[completed]`` status tag, or
a ``Status: completed`` / ``Status: done`` field. A forward-looking backlog holds only
open work; a closed item is deleted (its completion recorded elsewhere), not annotated
done in place. A line is read outside fenced code blocks, and inline backtick code spans
are stripped first, so a backticked mention of a marker (naming ``~~`` or ``[done]`` in
prose) does not register.

Engine/wrapper split (compile PR-15): this engine carries the PURE check (the three
done-marker patterns, the code-span strip, ``check_file``) and a ``run`` that groups +
reports; the project wrapper (``tools/lint-todo-marked-done.py``) supplies the scan scope
(which backlog file) and the repository root. This engine holds no scan-scope policy and
is repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import SIMPLE_CODE_SPAN_RE, iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-todo-marked-done.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# Markdown strikethrough span: an item struck through in place.
STRIKETHROUGH = re.compile(r"~~[^~]+~~")

# A bracketed done tag used as a status suffix.
DONE_TAG = re.compile(r"\[(?:done|completed)\]", re.IGNORECASE)

# A Status: completed / Status: done field on an item.
STATUS_DONE = re.compile(r"\bStatus:\s*(?:completed|done)\b", re.IGNORECASE)

# Inline backtick code spans: stripped before matching so a backticked mention of a
# marker does not register.
INLINE_CODE_SPAN = SIMPLE_CODE_SPAN_RE


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


def run(files: list[Path], *, repo_root: Path) -> int:
    grouped: dict[str, list[tuple[int, str, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
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
    print("TODO is forward-looking: a closed item is DELETED from TODO in this PR;")
    print("its DONE entry rotates cross-repo to the private sibling, not annotated")
    print("done-in-place. Rotate the item.")
    return 1
