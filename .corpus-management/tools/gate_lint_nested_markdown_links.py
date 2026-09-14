#!/usr/bin/env python3
"""Nested-markdown-link malformation audit (grc gate 68): pack-owned engine (source of record).

No scanned markdown file may contain a nested markdown link of the form
``[[text](url)](url)`` (a link whose visible text is itself a link), which renders in
GitHub-flavoured Markdown as a broken literal ``[`` followed by a dangling ``](url)``.
The class is GATE-BLIND to the link-coverage gate (a nested link still contains a
well-formed inner link) and to the broken-link gate (the inner link resolves), so this
gate closes that blind spot; it is preventive (the corpus census found zero after the
originating cleanup).

Detection (the load-bearing constraint): for each non-fenced line (via the shared
fence-aware ``aiqt_corpus.iter_non_code_lines`` iterator) inline code spans are first
neutralized to a single placeholder character, so a code-span DESCRIPTION of the pattern
inside backticks is NOT flagged while a REAL malformation, whose live ``[[``, ``](`` and
``)](`` brackets survive masking, still exposes its ``[[X](url)](url)`` structure. The
nested-link regex is then applied to the masked line.

Engine/wrapper split (compile PR-7): this engine carries the pure check (the regexes,
``find_nested_links`` + ``run``); the project wrapper (``tools/lint-nested-markdown-links.py``)
supplies the grc scan configuration (the default ``*.md`` walk minus ``DEFAULT_EXEMPT_DIRS``
/ ``is_default_exempt_root``, and the explicit-path iterator) and the AIQT bootstrap.
``run`` takes the target list and the repo root from the wrapper; it holds no scan-scope
policy.

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
        "(python3 tools/lint-nested-markdown-links.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# An inline code span (backtick-delimited run). Neutralized to a single placeholder so a
# description of the pattern inside backticks is not flagged, while a real malformation's
# live brackets survive.
CODE_SPAN_RE = SIMPLE_CODE_SPAN_RE

# A markdown link whose visible text is itself a markdown link:
#   [ [text](url) ] (url)
# After code-span masking the inner text is at least the placeholder "X".
NESTED_LINK_RE = re.compile(r"\[\[[^\]]+\]\([^)]+\)\]\([^)]+\)")


def find_nested_links(text: str) -> list[int]:
    """Return the 1-indexed line numbers carrying a nested-link malformation."""
    hits: list[int] = []
    for lineno, line in iter_non_code_lines(text):
        masked = CODE_SPAN_RE.sub("X", line)
        if NESTED_LINK_RE.search(masked):
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
        for lineno in find_nested_links(text):
            try:
                rel = path.relative_to(repo_root).as_posix()
            except ValueError:  # explicit path outside repo_root
                rel = path.as_posix()
            findings.append(
                f"{rel}:{lineno}: nested markdown link "
                "([[text](url)](url), a link whose text is itself a link); "
                "renders as a broken literal '[' plus a dangling '](url)'. "
                "Collapse to the single well-formed link."
            )

    if findings:
        print(f"FAIL: {len(findings)} nested-markdown-link finding(s):")
        for f in findings:
            print(f"  - {f}")
        print(
            "A nested markdown link is gate-blind to the link-coverage and "
            "broken-link gates (the inner link is well-formed and resolves); "
            "collapse [[text](url)](url) to [text](url). To DESCRIBE the "
            "pattern in prose, wrap the whole token in a backtick code span."
        )
        return 1

    print(
        f"OK: {checked} markdown file(s) checked; no nested-markdown-link "
        "malformation found."
    )
    return 0
