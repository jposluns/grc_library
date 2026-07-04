#!/usr/bin/env python3
"""Unbalanced-fence audit: no scanned markdown file may end inside an
open fenced code block (the guardrail review's GR-4 residual).

Why this gate exists: the shared fence-aware iterator
(``lint_common.iter_non_code_lines``) treats every line whose stripped
form starts with three backticks or three tildes as a state TOGGLE. An
UNBALANCED fence (an odd number of fence lines) therefore leaves the
iterator "inside a code block" for the remainder of the file, silently
suppressing every downstream linter's scanning of everything after it:
the defect is invisible precisely because the linters that would report
it stop looking. The 2026-07-02 guardrail review's GR-4 shipped the
tilde-toggle half into the iterator; this gate is the maintainer-chosen
standalone-check half (decided at the 2026-07-04 morning round). The
corpus census at build time found ZERO unbalanced fences, so the gate is
preventive, not remedial.

Detection mirrors the iterator's semantics EXACTLY (one shared toggle
for both fence characters, ``line.strip()`` prefix match), so "this gate
passes" and "the iterator scans the whole file" are the same statement.
A file whose fence-line count is odd fails, reporting the line number of
the last (unclosed) fence opener.

Scope: every ``*.md`` under the repository root except
``DEFAULT_EXEMPT_DIRS`` (the population the fence-aware linters scan in
their DEFAULT walks). Honest residual (the r5 gap lens): some linters
also accept EXPLICIT path arguments with no exempt-dir filter (the
mandated new-pack-prose ``lint-language.py`` run on ``.claude/`` files
is the recurring case), and an unbalanced fence there would suppress
that invocation's tail while this gate's default walk never sees the
file; this gate accepts explicit paths too, so scan the same paths when
it matters. The default-population widening is a routed maintainer
shape call (TODO section 3.15).

Usage:
    python3 tools/lint-unbalanced-fences.py
    python3 tools/lint-unbalanced-fences.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more unbalanced-fence findings
"""

from __future__ import annotations

import sys
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    read_text_safe,
)


def fence_lines(text: str) -> list[int]:
    """Return the 1-indexed line numbers of every fence-toggle line,
    using the same test as ``lint_common.iter_non_code_lines``."""
    hits: list[int] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            hits.append(lineno)
    return hits


def iter_targets(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    if paths:
        for p in paths:
            path = REPO_ROOT / p
            if path.is_file() and path.suffix == ".md":
                files.append(path)
            elif path.is_dir():
                files.extend(path.rglob("*.md"))
    else:
        for f in REPO_ROOT.rglob("*.md"):
            rel_parts = f.relative_to(REPO_ROOT).parts
            if any(part in DEFAULT_EXEMPT_DIRS for part in rel_parts):
                continue
            files.append(f)
    return sorted(set(files))


def main(argv: list[str]) -> int:
    findings: list[str] = []
    checked = 0
    for path in iter_targets(argv):
        text = read_text_safe(path)
        if text is None:
            continue
        checked += 1
        fences = fence_lines(text)
        if len(fences) % 2 == 1:
            try:
                rel = path.relative_to(REPO_ROOT).as_posix()
            except ValueError:  # explicit path outside REPO_ROOT
                rel = path.as_posix()
            findings.append(
                f"{rel}:{fences[-1]}: unbalanced fence (odd fence-line "
                f"count {len(fences)}; the file ends inside an open code "
                "block, silently suppressing every fence-aware linter's "
                "scan of the remainder)"
            )

    if findings:
        print(f"FAIL: {len(findings)} unbalanced-fence finding(s):")
        for f in findings:
            print(f"  - {f}")
        print(
            "Close the open fence (or remove the stray fence line); an "
            "odd fence count silences downstream scanning."
        )
        return 1

    print(
        f"OK: {checked} markdown file(s) checked; every fenced code "
        "block is balanced."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
