#!/usr/bin/env python3
"""Shared TODO index-row and item-heading grammar, and the index-header gate, for the backlog item readers.

Three tools read backlog items. The decision-log hook
(``.claude/hooks/block-unjustified-decision.py``) compares a submitted
``backlog-audit: <N> items enumerated`` token with its own item count; the
actionability audit (``tools/audit-backlog-actionability.py``) produces that N and
feeds the stop guard through ``.claude/hooks/nmw-actionable``; and gate 78
(``tools/lint-todo-number-permanence.py``) reads the live item ids to catch a
recycled or duplicated number. Before P-TODO 3b121 each kept its own row grammar:
the hook counted any ``| <id> |`` row, and counted public ``TODO.md`` rows
without the index-header gate; the tool read only ``| <id> | <title> | <tags> |``
rows under an index header; and gate 78 read ``lint_common.parse_todo_index``
rows, which drop an unreadable row and ignore the header gate. The hook and gate
78 also kept their own ``### <id>`` heading regexes, and gate 78's ended an id
only at whitespace or a colon, so ``### RB-6. title`` was an item in the tool and
not live in gate 78. All three now read rows through ``index_rows`` and headings
through ``item_headings`` / ``match_heading`` here, so they read the same items
with the same ids. Bold-bullet items are outside this module: gate 78 reads them
with the audit tool's own parser, and the hook keeps a replica that fixtures pin
to it (3b119).

The row grammar:

- The header gate is ``lint_common.has_todo_index_header``. A file with no
  ``| ID | Item | Tags |`` header row has no index rows, public or private.
- A row CANDIDATE is a line that starts ``| <id> |`` after at most three spaces of
  indentation (Markdown renders such a line as a table row; four spaces or a tab
  make it code), where ``<id>`` is a ``lint_common.TODO_ID_RE`` backlog id. Once
  the header is present, candidates are read anywhere in the file, fenced text
  included, as the counters read them before.
- A candidate is READABLE when it also has a title cell and a tags cell,
  ``| <id> | <title> | <tags> |``; later cells are ignored.
- An UNREADABLE candidate (``| 1.2 | title only |``, or a row without its closing
  pipe) fails closed: it is returned with ``readable=False``, so every reader
  keeps it as an open item. The audit tool counts it ACTIONABLE with no
  ``[BLOCKED:]`` grant, since its tags cannot be read, and gate 78 holds its id
  live. Dropping it would hide an open item from the stop guard and a recycled
  number from gate 78; a nonzero tool exit would make the stop guard fail open
  (nmw-actionable reads a tool error as indeterminate).

The heading grammar, ``ITEM_HEADING_RE`` (the audit tool's since 3b119): a line
that starts ``### `` (one space) and then a private ``P-n.m`` id, a section number
of two or three parts with an optional letter, or a coded id (``RB-6``,
``GR-GAP-1``, ``TF-2``). The id ends at a word boundary, so ``### RB-6. title``
reads as ``RB-6`` and ``### 3.92.a child`` as ``3.92``. Every such line is an item
heading, inside a code fence or an HTML comment too (a masked heading is a
one-line item, 3b119 QA r5), and no header gate applies. A heading outside the
grammar (a ``§`` marker, a tab or a second space after ``###``) is not an item in
any reader; the audit tool lists it among its ITEM-LIKE lines when its lead word
looks like an id.

Lines are split with ``str.splitlines`` (CR, form feed and U+2028 end a line too),
as the audit tool splits them. A first cell that is not a backlog id (``| 3b7 |``,
``| RB-6 |``, the header, the separator) is not a candidate.

Stdlib-only Python 3.11.
"""
from __future__ import annotations

import re
from typing import NamedTuple

from lint_common import TODO_ID_RE, has_todo_index_header

# The backlog-id alternation, taken from lint_common.TODO_ID_RE (``^(?:...)$``) so the row grammar and
# the id grammar the other backlog gates read cannot drift apart.
if not (TODO_ID_RE.pattern.startswith("^(?:") and TODO_ID_RE.pattern.endswith(")$")):
    raise ImportError("lint_common.TODO_ID_RE is not an anchored ^(?:...)$ alternation; "
                      "re-derive TODO_ID_ALT in tools/todo_index_rows.py")
TODO_ID_ALT = TODO_ID_RE.pattern[1:-1]

# A row candidate: the line starts ``| <id> |`` after at most three spaces (P-TODO 3b121 QA r1).
ROW_START_RE = re.compile(r"^ {0,3}\|\s*(?P<id>" + TODO_ID_ALT + r")\s*\|")
# A readable row: ``| <id> | <title> | <tags> |``.
ROW_RE = re.compile(r"^ {0,3}\|\s*(?P<id>" + TODO_ID_ALT + r")\s*\|(?P<title>[^|]*)\|(?P<tags>[^|]*)\|")

# An item heading: ``### <id> <title>``, the id ending at a word boundary (see the module docstring).
ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)


class IndexRow(NamedTuple):
    """One row candidate. ``line`` is 1-based over ``text.splitlines()``. ``title`` and ``tags`` are the
    stripped cells of a readable row, and empty for an unreadable one."""

    line: int
    item_id: str
    title: str
    tags: str
    readable: bool


class ItemHeading(NamedTuple):
    """One item heading. ``line`` is 1-based over ``text.splitlines()``; ``title`` is the stripped rest of the
    line after the id."""

    line: int
    item_id: str
    title: str


def match_row(line: str, lineno: int = 0) -> "IndexRow | None":
    """The row candidate on one line, or None when the line does not start ``| <id> |`` after at most three
    spaces."""
    m = ROW_RE.match(line)
    if m:
        return IndexRow(lineno, m.group("id"), m.group("title").strip(), m.group("tags").strip(), True)
    m = ROW_START_RE.match(line)
    if m:
        return IndexRow(lineno, m.group("id"), "", "", False)
    return None


def index_rows(text: str) -> "list[IndexRow]":
    """Every row candidate in a backlog file, in file order, readable or not; none without an index header."""
    if not has_todo_index_header(text):
        return []
    rows: list[IndexRow] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        row = match_row(line, lineno)
        if row is not None:
            rows.append(row)
    return rows


def match_heading(line: str, lineno: int = 0) -> "ItemHeading | None":
    """The item heading on one line, or None when the line is not a ``### <id>`` item heading."""
    m = ITEM_HEADING_RE.match(line)
    if m:
        return ItemHeading(lineno, m.group("id"), m.group("title").strip())
    return None


def item_headings(text: str) -> "list[ItemHeading]":
    """Every item heading in a backlog file, in file order, fenced or commented ones included; no header gate."""
    headings: list[ItemHeading] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        heading = match_heading(line, lineno)
        if heading is not None:
            headings.append(heading)
    return headings
