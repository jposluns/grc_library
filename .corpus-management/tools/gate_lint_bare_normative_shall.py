#!/usr/bin/env python3
"""Bare normative-wording audit (grc gate 56): pack-owned engine (source of record).

Detect a bare normative ``shall`` in authored prose: the house style harmonizes normative
requirement verbs on ``must``, so a free-standing ``shall`` is a regression of that convention.
Three classes are deliberately preserved (NOT flagged): a hyphenated identifier embedding
``shall`` (the boundary requires non-word, non-hyphen edges); a backticked ``shall``
word-reference (inline code spans are stripped before matching); a verbatim quote carried as
a Markdown blockquote (``>`` lines) or a fenced code block (skipped via ``iter_non_code_lines``);
and a verbatim quote carried as a whole Markdown table cell, i.e. a cell whose entire trimmed
content is one straight-double-quoted span (a quoted statute or policy provision). A cell that
mixes unquoted text with a quote is still checked, as is every non-table line.

Engine/wrapper split (compile PR-9): this engine carries the PURE check (``BARE_SHALL``,
``INLINE_CODE_SPAN``, ``check_file``) and a ``run`` that groups + reports; the project wrapper
(``tools/lint-bare-normative-shall.py``) supplies the grc scan scope (the default roots, the
markdown selector) and the grc-specific exempt-file set, and filters those files out before
delegating, so this engine holds no scan-scope or project-file policy.

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
        "(python3 tools/lint-bare-normative-shall.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# A bare normative ``shall``: the word standing free, not part of a hyphenated identifier
# (e.g. ``lint-shall-near-uncertainty``) and not a substring of another word (e.g. ``Marshall``).
# Case-insensitive so a sentence-initial ``Shall`` is also caught.
BARE_SHALL = re.compile(r"(?<![A-Za-z0-9_-])shall(?![A-Za-z0-9_-])", re.IGNORECASE)

# Inline backtick code spans: stripped before matching so a backticked ``shall`` word-reference
# does not register.
INLINE_CODE_SPAN = SIMPLE_CODE_SPAN_RE

# Preserved class 4: a table cell that is wholly one double-quoted verbatim quotation.
_UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")
_WHOLE_QUOTE_CELL = re.compile(r'^"[^"]*"$')


def _strip_for_check(line: str) -> str:
    """The text the check reads: for a table row, each cell separately (a wholly quoted cell
    blanked, inline code stripped within the cell only, so a span can never pair backticks across
    cells); for any other line, the line with inline code stripped."""
    if not line.lstrip().startswith("|"):
        return INLINE_CODE_SPAN.sub("", line)
    cells = _UNESCAPED_PIPE.split(line)
    return "|".join("" if _WHOLE_QUOTE_CELL.match(c.strip()) else INLINE_CODE_SPAN.sub("", c)
                    for c in cells)


def check_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (lineno, line_snippet) findings. PURE (the wrapper filters exempt files)."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, str]] = []
    for lineno, line in iter_non_code_lines(text):
        # Preserved class 3: verbatim quotes carried as Markdown blockquotes.
        if line.lstrip().startswith(">"):
            continue
        # Preserved class 2: strip inline backtick spans so a backticked word-reference does not register.
        stripped = _strip_for_check(line)
        if BARE_SHALL.search(stripped):
            findings.append((lineno, line.strip()[:150]))
    return findings


def run(files: list[Path], *, repo_root: Path) -> int:
    grouped: dict[str, list[tuple[int, str]]] = {}
    total = 0
    for f in files:
        try:
            rel = f.relative_to(repo_root).as_posix()
        except ValueError:  # explicit path outside repo_root
            rel = f.as_posix()
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
