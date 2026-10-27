#!/usr/bin/env python3
"""Metadata-block line-break audit (grc gate): pack-owned engine (source of record).

Detect runs of ``**Field:**`` metadata lines that lack a Markdown hard-break marker
on the non-last lines of the run. A run is the rendered paragraph (3b146): lines that
render into one paragraph form one run, whatever their indentation, so an indented
continuation line between metadata lines does not split it. Without a hard-break,
GitHub renders the metadata block as a single soft-wrapped paragraph rather than as a
vertical list of labelled facts. Two hard-break markers are accepted: a trailing
backslash (``\\``) or two-or-more trailing spaces. The last line of a run is exempt
(the following blank line or ``---`` separator already breaks the paragraph).
Fenced code blocks are skipped via ``aiqt_corpus.iter_non_code_lines``, so a
metadata-format example inside ``` ``` ``` is not a false positive.

Engine/wrapper split (SHARED/SAFETY lane, Pattern A): this engine carries the PURE
check (``META_LINE``, ``has_hard_break``, ``scan_file``); the project wrapper
(``tools/lint-metadata-line-breaks.py``) supplies the grc scan scope
(``DEFAULT_TARGETS`` / ``iter_target_files``) and the grouped reporting in ``main``,
and keeps a thin module-global ``scan_file`` shim delegating here, so the
scan-scope regression test (which patches ``mod.scan_file`` and runs ``main``)
observes the original signature and behaviour. The engine's check is generic (no
scan-scope or repository-root policy).

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_metadata_line_breaks: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# A field name starts with a letter and runs, without an asterisk, to the closing colon, so a
# hyphen, slash, parenthesis or underscore in it (an SPDX-License-Identifier-style key, an
# "Owner/Approver" key) cannot split a run and hide a missing hard break before it (P-1.89(b)).
META_LINE = re.compile(r"^\*\*[A-Za-z][^*]*?:\*\*")


def has_hard_break(line: str) -> bool:
    """A line has a Markdown hard-break marker if it ends with ``\\`` or two-plus spaces."""
    if line.endswith("\\"):
        return True
    if len(line) >= 2 and line.endswith("  "):
        return True
    return False


# 3b146: a run is the rendered paragraph, not a stretch of consecutive metadata lines. A
# paragraph continues through any non-blank line, whatever its indentation, unless the line
# starts another block (CommonMark 0.31): these leaf blocks end it and are not paragraph text.
_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|"
    "details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|"
    "h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|"
    "optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    "track|ul"
)
LEAF_BLOCK_START = re.compile(
    r" {0,3}(?:"
    r"#{1,6}(?:[ \t]|$)"  # ATX heading
    r"|(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"  # thematic break
    r"|<(?:!--|\?|![A-Za-z]|!\[CDATA\[)"  # HTML blocks 2 to 5
    r"|<(?:script|pre|style|textarea)(?:[ \t>]|$)"  # HTML block 1
    r"|</?(?:" + _HTML_BLOCK_TAGS + r")(?:[ \t>]|/>|$)"  # HTML block 6
    r")",
    re.IGNORECASE,
)
# After paragraph text, a line of only ``=`` or ``-`` is a setext underline: it ends the paragraph.
SETEXT_UNDERLINE = re.compile(r" {0,3}(?:=+|-+)[ \t]*$")
# A block quote or a list item that may interrupt a paragraph (a bullet, or an ordered item
# numbered 1, with content) ends the paragraph and opens a new one with its own text.
CONTAINER_START = re.compile(r" {0,3}(?:>|[-+*][ \t]+\S|1[.)][ \t]+\S)")


def _indent(line: str) -> int:
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip(" "))


def scan_file(path: Path) -> list[tuple[int, int]]:
    """Return ``[(block_start_line, missing_count), ...]`` for every offending block."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, int]] = []
    para: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal para
        meta = [i for i, (_, ln) in enumerate(para) if META_LINE.match(ln.lstrip(" \t"))]
        if len(meta) >= 2:
            # Every metadata line that another line of its paragraph follows needs a hard break.
            missing = sum(
                1 for i in meta if i < len(para) - 1 and not has_hard_break(para[i][1])
            )
            if missing:
                findings.append((para[meta[0]][0], missing))
        para = []

    prev = 0
    for lineno, line in iter_non_code_lines(text):
        # The fence-aware scan omits fenced lines, so a gap in line numbers is a fenced block.
        # A fence between metadata lines ends the run: the lines either side are not one
        # paragraph, so the one before the fence needs no hard break (P-1.89(c)).
        if lineno != prev + 1:
            flush()
        prev = lineno
        if not line.strip():
            flush()
        elif para:
            if LEAF_BLOCK_START.match(line) or SETEXT_UNDERLINE.match(line):
                flush()
            elif CONTAINER_START.match(line):
                flush()
                para.append((lineno, line))
            else:
                # A paragraph continuation line, at any indentation (3b146).
                para.append((lineno, line))
        elif _indent(line) < 4 and not LEAF_BLOCK_START.match(line):
            # Four or more columns outside a paragraph is an indented code block.
            para.append((lineno, line))
    flush()
    return findings
