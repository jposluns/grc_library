#!/usr/bin/env python3
"""Metadata-block line-break audit (grc gate): pack-owned engine (source of record).

Detect runs of ``**Field:**`` metadata lines that lack a Markdown hard-break marker
on the non-last lines of the run. A run is the rendered paragraph (3b146): the lines
that render into one paragraph form one run, whatever their indentation, read without
their block quote and list item markers, so an indented or lazy continuation line
between metadata lines does not split it. ``scan_file`` follows the GFM specification's
block structure (version 0.29-gfm, which GitHub's renderer follows), with its tables,
whitespace characters and blank lines: block quotes, list items (a sibling item ends the
paragraph whatever its number; an item that interrupts a paragraph needs content and,
if ordered, the number 1, as ``1.`` or ``01.``), fenced code (closed only by a fence
of the opening character at least as long, so a mixed backtick and tilde pair is not
a pair and a backtick line whose info string holds a backtick is text), indented code,
HTML blocks to their end condition (their content is never a run), setext headings and
GFM tables (a table's header row and body rows are never part of a run). A setext
heading's lines stay a run, because the heading shows them joined. Without a
hard-break, GitHub renders the metadata block as a single soft-wrapped paragraph rather
than as a vertical list of labelled facts. Two hard-break markers are accepted: a
trailing backslash (``\\``) or two-or-more trailing spaces (a trailing tab is not one).
The last line of a run is exempt (the following blank line or ``---`` separator
already breaks the paragraph). A metadata-format example inside a fence is not a
false positive.

Residual: when a lazy continuation line that omits the markers of two or more nested
block quotes is indented four or more columns and would start a block once unindented,
the gate checks only the lines of its paragraph before that line, and no line from that
line to the next blank line outside every container. Tabs are expanded to four-column
stops before the structure is read, and lines are split at newlines only.

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
    from aiqt_corpus import read_text_safe
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


# 3b146: a run is the rendered paragraph, not a stretch of consecutive metadata lines. The
# scan follows the GFM 0.29-gfm block structure: block quote and list item containers (so a
# quoted or list-item paragraph is a run, read without its markers), lazy continuation lines,
# fenced code (a closing fence uses the opening character, at least as many times), indented
# code, HTML blocks to their end condition, and tables.
# GFM 0.29 section 2.1: a whitespace character is a space, tab, newline, line tabulation
# (U+000B), form feed (U+000C) or carriage return; a blank line holds no characters, or only
# spaces and tabs, so a line holding a form feed or line tabulation is not blank.
_WS = r"[ \t\n\x0b\x0c\r]"
_BLANK_LINE = re.compile(r"[ \t]*")


def _is_blank(rest: str) -> bool:
    return bool(_BLANK_LINE.fullmatch(rest))


_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|"
    "details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|"
    "h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|"
    "optgroup|option|p|param|section|source|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    "track|ul"
)
# The kind 6 tag list above is the GFM specification's (version 0.29-gfm, 2019-04-06), which
# GitHub's renderer follows. Kinds 1, 4 and 7 are also GFM 0.29's. CommonMark 0.31.2 differs on
# four points: its kind 6 list drops source and adds search, its kind 1 adds textarea, its kind 4
# accepts any ASCII letter after <! where GFM 0.29 needs an uppercase one, and its kind 7
# exclusion list (script, style, pre, for open tags) adds textarea.
# Tag names are ASCII only (GFM 0.29 section 6.10), so every pattern that folds case is also
# re.ASCII: without it, IGNORECASE matches the Kelvin sign U+212A against [A-Za-z] or k.
# HTML block kinds 1 to 6: (start, end). Kinds 1 to 5 end on the line holding the end marker,
# the start line included; kind 6 (end None) ends before a blank line. All six can interrupt
# a paragraph.
HTML_BLOCK_STARTS = (
    (re.compile(r" {0,3}<(?:script|pre|style)(?:" + _WS + r"|>|$)", re.IGNORECASE | re.ASCII),
     re.compile(r"</(?:script|pre|style)>", re.IGNORECASE | re.ASCII)),
    (re.compile(r" {0,3}<!--"), re.compile(r"-->")),
    (re.compile(r" {0,3}<\?"), re.compile(r"\?>")),
    (re.compile(r" {0,3}<![A-Z]"), re.compile(r">")),
    (re.compile(r" {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    (re.compile(r" {0,3}</?(?:" + _HTML_BLOCK_TAGS + r")(?:" + _WS + r"|>|/>|$)",
                re.IGNORECASE | re.ASCII), None),
)
# HTML block kind 7: a whole open or closing tag alone on its line. It cannot interrupt a
# paragraph, so it only starts a block where no paragraph is open.
HTML_BLOCK_7 = re.compile(
    r" {0,3}(?:<(?!(?:script|style|pre)(?![A-Za-z0-9-]))[A-Za-z][A-Za-z0-9-]*"
    r"(?:" + _WS + r"+[A-Za-z_:][A-Za-z0-9_.:-]*"
    r"(?:" + _WS + r"*=" + _WS + r"*(?:[^ \t\n\x0b\x0c\r\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)*"
    + _WS + r"*/?>|</[A-Za-z][A-Za-z0-9-]*" + _WS + r"*>)" + _WS + r"*$",
    re.IGNORECASE | re.ASCII,
)
ATX_HEADING = re.compile(r" {0,3}#{1,6}(?:[ \t]|$)")
THEMATIC_BREAK = re.compile(r" {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
# After paragraph text, a line of only ``=`` or ``-`` is a setext underline: it ends the paragraph.
SETEXT_UNDERLINE = re.compile(r" {0,3}(?:=+|-+)[ \t]*$")
FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})(.*)$")
BLOCK_QUOTE = re.compile(r" {0,3}> ?")
LIST_MARKER = re.compile(r"( {0,3})([-+*]|([0-9]{1,9})[.)])(?= |$)")
TABLE_DELIMITER = re.compile(r" {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$")


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _table_cells(row: str) -> int:
    """Count a GFM table row's cells: split on unescaped pipes, less one outer pipe a side."""
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return len(re.split(r"(?<!\\)\|", row))


def _is_table_delimiter(row: str, header: str) -> bool:
    """A GFM delimiter row under ``header`` whose cell count matches, with a pipe in either."""
    return (
        bool(TABLE_DELIMITER.match(row))
        and ("|" in row or "|" in header)
        and _table_cells(row) == _table_cells(header)
    )


def _leaf_interrupts(rest: str) -> bool:
    """Whether ``rest`` opens a leaf block that ends a paragraph (lists and quotes aside)."""
    return bool(
        ATX_HEADING.match(rest)
        or THEMATIC_BREAK.match(rest)
        or _fence_open(rest)
        or any(start.match(rest) for start, _ in HTML_BLOCK_STARTS)
    )


def _fence_open(rest: str) -> tuple[str, int] | None:
    m = FENCE_OPEN.match(rest)
    if not m or (m.group(1)[0] == "`" and "`" in m.group(2)):
        return None
    return m.group(1)[0], len(m.group(1))


def scan_file(path: Path) -> list[tuple[int, int]]:
    """Return ``[(block_start_line, missing_count), ...]`` for every offending block."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[tuple[int, int]] = []
    # A paragraph line is (lineno, text without container markers, original line); the
    # hard-break test reads the original line's end, so a trailing tab is not two spaces.
    para: list[tuple[int, str, str]] = []
    # Open containers, outermost first: ["quote"] or ["item", content indent, has content].
    containers: list[list] = []
    # The open non-paragraph leaf: None, ("fence", char, length), ("html", end), ("code",)
    # or ("table",).
    leaf: tuple | None = None
    # Where renderers part on whether the paragraph continues, the index of the first line in
    # doubt: only the lines before it are checked, as every reading renders them alike.
    unsure: int | None = None
    # After such a line the renderers' block structures differ, so no later paragraph is
    # checked until a blank line outside every container.
    doubt = False

    def flush() -> None:
        nonlocal para, unsure
        checked = para if unsure is None else para[:unsure]
        if doubt and unsure is None:
            checked = []
        meta = [i for i, (_, ln, _) in enumerate(checked) if META_LINE.match(ln.lstrip(" \t"))]
        if len(meta) >= 2:
            # Every metadata line that another line of its paragraph follows needs a hard break.
            missing = sum(
                1 for i in meta if i < len(checked) - 1 and not has_hard_break(checked[i][2])
            )
            if missing:
                findings.append((checked[meta[0]][0], missing))
        para, unsure = [], None

    # Markdown ends a line only at a newline (the read already folds CR and CRLF into one), so
    # a form feed or U+2028 in a line does not shift the reported line numbers.
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.expandtabs(4)
        # Match the open containers: a quote needs its marker, an item its content indent (or
        # a blank line once it has content).
        pos, matched = 0, 0
        for c in containers:
            if c[0] == "quote":
                m = BLOCK_QUOTE.match(line, pos)
                if not m:
                    break
                pos = m.end()
            elif _is_blank(line[pos:]) and c[2]:
                pos = len(line)
            elif _indent(line[pos:]) >= c[1]:
                pos += c[1]
            else:
                break
            matched += 1
        all_matched = matched == len(containers)
        rest = line[pos:]

        # Inside a fence, an HTML block or indented code, a fully matched line is block content.
        if all_matched and leaf is not None and leaf[0] == "fence":
            m = re.match(r" {0,3}(%s{%d,})[ \t]*$" % (re.escape(leaf[1]), leaf[2]), rest)
            if m:
                leaf = None
            continue
        if all_matched and leaf is not None and leaf[0] == "html":
            if leaf[1] is None and _is_blank(rest):
                leaf = None
            elif leaf[1] is not None and leaf[1].search(rest):
                leaf = None
            continue
        if all_matched and leaf == ("code",) and (_is_blank(rest) or _indent(rest) >= 4):
            continue

        # Open new containers. A list item interrupts a paragraph of its own container only
        # when it has content and, if ordered, starts at 1 (``1.``, ``01.``); in an enclosing
        # list it starts a sibling item whatever its number.
        para_tip = bool(para) and all_matched
        opened = False
        while _indent(rest) < 4:
            m = BLOCK_QUOTE.match(rest)
            if m:
                if not opened:
                    del containers[matched:]
                    flush()
                    leaf, opened = None, True
                containers.append(["quote"])
                matched += 1
                pos += m.end()
                rest = line[pos:]
                continue
            m = LIST_MARKER.match(rest)
            if not m or THEMATIC_BREAK.match(rest):
                break
            after = rest[m.end():]
            if para_tip and not opened and (
                _is_blank(after) or (m.group(3) is not None and int(m.group(3)) != 1)
            ):
                break
            gap = _indent(after)
            width = m.end() + (gap if 1 <= gap <= 4 and not _is_blank(after) else 1)
            if not opened:
                del containers[matched:]
                flush()
                leaf, opened = None, True
            for c in containers:
                if c[0] == "item":
                    c[2] = True
            containers.append(["item", width, False])
            matched += 1
            pos += min(width, len(rest))
            rest = line[pos:]
        all_matched = matched == len(containers)

        # A lazy continuation line: an unmatched container's paragraph continues through text
        # that opens no block of its own.
        if (
            not all_matched and not opened and para and not _is_blank(rest)
            and not _leaf_interrupts(rest)
        ):
            if (
                _indent(rest) >= 4
                and sum(c[0] == "quote" for c in containers[matched:]) >= 2
                and (_leaf_interrupts(rest.lstrip(" ")) or BLOCK_QUOTE.match(rest.lstrip(" "))
                     or LIST_MARKER.match(rest.lstrip(" ")))
                and unsure is None
            ):
                # The disclosed residual: an indented block start after nested quotes. The
                # line and those after it are not checked, so it can miss, never over-report.
                unsure, doubt = len(para), True
            para.append((lineno, rest, raw))
            continue
        if not all_matched:
            del containers[matched:]
            flush()
            leaf = None

        if _is_blank(rest):
            flush()
            if leaf is not None and leaf[0] == "table":
                leaf = None
            if not containers:
                doubt = False
            continue
        for c in containers:
            if c[0] == "item":
                c[2] = True
        if leaf is not None and leaf[0] == "table":
            if _indent(rest) < 4 and not _leaf_interrupts(rest):
                continue  # a table row, whatever it holds
            leaf = None
        if leaf == ("code",):
            leaf = None
        if para:
            if SETEXT_UNDERLINE.match(rest):
                flush()  # a setext heading still shows its lines joined, so it stays a run
                continue
            if _is_table_delimiter(rest, para[-1][1]):
                # The paragraph's last line is the table's header row, not paragraph text.
                para.pop()
                flush()
                leaf = ("table",)
                continue
            if not _leaf_interrupts(rest):
                # A paragraph continuation line, at any indentation (3b146).
                para.append((lineno, rest, raw))
                continue
            flush()
        if _indent(rest) >= 4:
            leaf = ("code",)
        elif _fence_open(rest):
            leaf = ("fence",) + _fence_open(rest)
        elif ATX_HEADING.match(rest) or THEMATIC_BREAK.match(rest):
            pass
        elif any(start.match(rest) for start, _ in HTML_BLOCK_STARTS) or HTML_BLOCK_7.match(rest):
            end = next((e for s, e in HTML_BLOCK_STARTS if s.match(rest)), None)
            if end is None or not end.search(rest):
                leaf = ("html", end)
        else:
            para.append((lineno, rest, raw))
    flush()
    return findings
