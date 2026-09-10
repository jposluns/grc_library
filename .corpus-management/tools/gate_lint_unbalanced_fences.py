#!/usr/bin/env python3
"""Unbalanced-fence audit (grc gate 66): pack-owned engine (source of record).

No scanned markdown file may end inside an open fenced code block. The shared
fence-aware iterator (``aiqt_corpus.iter_non_code_lines``) treats every line
whose stripped form starts with three backticks or three tildes as a state
TOGGLE, so an UNBALANCED fence (an odd number of fence lines) leaves the
iterator "inside a code block" for the remainder of the file, silently
suppressing every downstream fence-aware check's scanning of everything after
it. Detection here mirrors the iterator's semantics EXACTLY (one shared toggle
for both fence characters, ``line.strip()`` prefix match), so "this gate passes"
and "the iterator scans the whole file" are the same statement; the fence syntax
is therefore deliberately NOT configurable.

Engine/wrapper split (compile PR-6): this engine carries the pure check
(``fence_lines`` + ``run``); the project wrapper
(``tools/lint-unbalanced-fences.py``) supplies the grc scan configuration
(the default ``*.md`` walk minus ``DEFAULT_EXEMPT_DIRS`` / ``is_default_exempt_root``,
and the explicit-path iterator) and the AIQT bootstrap. ``run`` takes the target
list and the repo root from the wrapper; it holds no scan-scope policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

from pathlib import Path

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-unbalanced-fences.py), which bootstraps the vendored copy, or put "
        "the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc


def fence_lines(text: str) -> list[int]:
    """Return the 1-indexed line numbers of every fence-toggle line,
    using the same test as ``aiqt_corpus.iter_non_code_lines``."""
    hits: list[int] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            hits.append(lineno)
    return hits


def run(files: list[Path], *, repo_root: Path) -> int:
    findings: list[str] = []
    checked = 0
    for path in files:
        text = read_text_safe(path)
        if text is None:
            continue
        checked += 1
        fences = fence_lines(text)
        if len(fences) % 2 == 1:
            try:
                rel = path.relative_to(repo_root).as_posix()
            except ValueError:  # explicit path outside repo_root
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
