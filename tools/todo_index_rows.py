#!/usr/bin/env python3
"""Shared TODO index-row grammar and index-header gate for the backlog item counters.

Two counters read backlog index rows. The decision-log hook
(``.claude/hooks/block-unjustified-decision.py``) compares a submitted
``backlog-audit: <N> items enumerated`` token with its own item count, and the
actionability audit (``tools/audit-backlog-actionability.py``) produces that N and
feeds the stop guard through ``.claude/hooks/nmw-actionable``. Before P-TODO 3b121
each kept its own row regex: the hook counted any ``| <id> |`` row, and counted
public ``TODO.md`` rows without the index-header gate, while the tool read only
``| <id> | <title> | <tags> |`` rows under an index header. Both now read rows
through ``index_rows`` here, so they count the same rows.

The grammar:

- The header gate is ``lint_common.has_todo_index_header``. A file with no
  ``| ID | Item | Tags |`` header row has no index rows, public or private.
- A row CANDIDATE is a line that starts ``| <id> |``, where ``<id>`` is a
  ``lint_common.TODO_ID_RE`` backlog id. Once the header is present, candidates are
  read anywhere in the file, fenced text included, as both counters read them before.
- A candidate is READABLE when it also has a title cell and a tags cell,
  ``| <id> | <title> | <tags> |``; later cells are ignored.
- An UNREADABLE candidate (``| 1.2 | title only |``, or a row without its closing
  pipe) fails closed: it is returned with ``readable=False``, so both counters count
  it as an open item, and the audit tool counts it ACTIONABLE with no
  ``[BLOCKED:]`` grant, since its tags cannot be read. Dropping it would hide an
  open item from the stop guard; a nonzero tool exit would make the stop guard fail
  open (nmw-actionable reads a tool error as indeterminate).

Lines are split with ``str.splitlines`` (CR, form feed and U+2028 end a line too),
as the audit tool splits them. A first cell that is not a backlog id (``| 3b7 |``,
``| RB-6 |``, the header, the separator) is not a candidate; heading and bullet
items are counted by each consumer's own grammar.

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

# A row candidate: the line starts ``| <id> |``.
ROW_START_RE = re.compile(r"^\|\s*(?P<id>" + TODO_ID_ALT + r")\s*\|")
# A readable row: ``| <id> | <title> | <tags> |``.
ROW_RE = re.compile(r"^\|\s*(?P<id>" + TODO_ID_ALT + r")\s*\|(?P<title>[^|]*)\|(?P<tags>[^|]*)\|")


class IndexRow(NamedTuple):
    """One row candidate. ``line`` is 1-based over ``text.splitlines()``. ``title`` and ``tags`` are the
    stripped cells of a readable row, and empty for an unreadable one."""

    line: int
    item_id: str
    title: str
    tags: str
    readable: bool


def match_row(line: str, lineno: int = 0) -> "IndexRow | None":
    """The row candidate on one line, or None when the line does not start ``| <id> |``."""
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
