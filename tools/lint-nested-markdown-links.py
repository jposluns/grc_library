#!/usr/bin/env python3
"""Nested-markdown-link malformation audit (gate 68): no scanned markdown
file may contain a nested markdown link of the form
``[[text](url)](url)`` (a link whose visible text is itself a link),
which renders in GitHub-flavoured Markdown as a broken literal ``[``
followed by a dangling ``](url)``.

Why this gate exists: the class recurred in PR #802, where a global
bare-code-span replacement (rewriting `` `tool.py` `` to
``[`tool.py`](tool.py)`` to satisfy the CHANGELOG link-coverage gate)
also re-wrapped the same code span WHERE IT ALREADY SAT INSIDE A LINK in
unrelated historical entries, producing ``[[`tool.py`](tool.py)](tool.py)``.
The pre-push skeptical verifier caught the in-scope corruption; two
pre-existing instances in early-PR historical CHANGELOG entries survived
until PR #807's cleanup. This malformation is GATE-BLIND to the existing
link-coverage gate (a nested link still contains a well-formed inner
link, so the path-shape / markdown-link checks pass) and to the
broken-link gate (the inner link resolves). This gate closes that blind
spot. The build-time corpus census found ZERO malformations after the
#807 cleanup, so the gate is preventive.

Detection: for each non-fenced line (via the shared fence-aware
``iter_non_code_lines`` iterator), inline code spans are first neutralized
to a single placeholder character. This is the load-bearing design
constraint (the #807 ``/validate-pr`` Finding-1 lesson): a code-span
DESCRIPTION of the pattern (e.g. a CHANGELOG entry that writes the literal
`` `[[ ... ]( ... )]( ... )` `` inside backticks to document it) must NOT
be flagged, while a REAL malformation, whose inner link TEXT may be a code
span but whose ``[[``, ``](`` and ``)](`` brackets and URLs are live
markdown, still exposes its ``[[X](url)](url)`` structure after the inner
code span becomes the placeholder ``X``. The nested-link regex is then
applied to the masked line.

Scope: every ``*.md`` under the repository root except
``DEFAULT_EXEMPT_DIRS`` (the population the markdown linters scan by
default; this includes the root ``CHANGELOG.md``, the surface where the
class recurred, and excludes ``.working`` and ``.claude``, so the
``[[wikilink]]`` convention of the memory files is out of scope by
construction). Explicit path arguments are accepted too.

Usage:
    python3 tools/lint-nested-markdown-links.py
    python3 tools/lint-nested-markdown-links.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more nested-markdown-link findings
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    iter_non_code_lines,
    read_text_safe,
)

# An inline code span (backtick-delimited run). Neutralized to a single
# placeholder so a description of the pattern inside backticks is not
# flagged, while a real malformation's live brackets survive.
CODE_SPAN_RE = re.compile(r"`[^`]*`")

# A markdown link whose visible text is itself a markdown link:
#   [ [text](url) ] (url)
# After code-span masking the inner text is at least the placeholder "X".
NESTED_LINK_RE = re.compile(r"\[\[[^\]]+\]\([^)]+\)\]\([^)]+\)")


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


def find_nested_links(text: str) -> list[int]:
    """Return the 1-indexed line numbers carrying a nested-link malformation."""
    hits: list[int] = []
    for lineno, line in iter_non_code_lines(text):
        masked = CODE_SPAN_RE.sub("X", line)
        if NESTED_LINK_RE.search(masked):
            hits.append(lineno)
    return hits


def main(argv: list[str]) -> int:
    findings: list[str] = []
    checked = 0
    for path in iter_targets(argv):
        text = read_text_safe(path)
        if text is None:
            continue
        checked += 1
        for lineno in find_nested_links(text):
            try:
                rel = path.relative_to(REPO_ROOT).as_posix()
            except ValueError:  # explicit path outside REPO_ROOT
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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
