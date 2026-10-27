#!/usr/bin/env python3
"""Table cell-count audit (gate 108, backlog 3b570).

Every GitHub-flavoured Markdown table body row in a tracked ``.md`` file must
split into as many cells as its header row. A renderer pads a short row with
empty cells and drops the cells of a long row past the header's count, so a
mismatch silently loses or shifts content. The recurring cause was a
ref-absence marker written with its bare-pipe query separator inside a table
row: the marker's pipe split the cell.

Scope: the files ``git ls-files -z`` lists whose names, lowercased, end in
``.md`` (so a name ending in ``.MD`` is scanned too), read from the working
tree. No directory is exempt.

Decision rule:

- Files are split into lines at LF, CRLF and a lone CR, as markdown-it-py
  normalizes line ends, and tabs expand to four-column stops. Only spaces
  and tabs make a line blank or may follow a closing fence, as CommonMark
  and markdown-it-py read them: a line holding any other whitespace, such
  as a no-break space, is not blank. Each line is read through its open
  containers as CommonMark reads it: a block quote opens on a ``>``
  indented at most three columns and continues on a line starting with
  ``>`` (at any indentation, as markdown-it-py reads it), and a list item
  opens on ``-``, ``+``, ``*`` or one to nine ASCII digits (0 to 9, as
  CommonMark and markdown-it-py read them, so another script's digit is
  text) followed by ``.`` or ``)``, and continues on a blank line or on a
  line indented at least to the item's content column (an item whose first
  line is empty ends at a blank line).
  Indentation is measured from the enclosing container's content column. A
  line that does not continue a container ends it, unless the line is a
  paragraph's lazy continuation.
- Fenced code, indented code and HTML blocks hold no table. A fence line is
  three or more backticks or tildes indented at most three columns in its
  container; the fence closes on a line of the same character, at least as
  long, with nothing else on it, or when its container ends. A line indented
  four or more columns in its container is indented code (or paragraph
  text), never a fence or HTML block start. HTML blocks start and end as
  CommonMark types 1 to 7 do (a comment, ``<!--``, is type 2), so a comment
  opener that holds ``-->``, such as ``<!-->``, closes on its own line. A
  U+0000 is read as U+FFFD, as CommonMark and markdown-it-py replace it.
  A fence, or an HTML block of type 1 to 5, that never closes is code or
  raw HTML through the end of the file, as the renderer reads it, so no
  table is found after its opening line, and the block is itself a finding
  (below).
  This fence model deliberately differs from the shared toggle predicate,
  ``aiqt_corpus.is_fence_line``, that gates 66 and 107 use, which toggles
  on any fence line, pairing fences by neither character nor width and
  modelling no container: gate 66 keeps a corpus scan's fence state
  consistent and gate 107 follows the same toggle model, while this gate
  must find the tables a renderer shows, so cases such as a four-backtick
  fence holding a three-backtick line, a backtick fence closed by tildes, a
  closing line with text after it, or a fence ended by its list item can get
  opposite verdicts from this gate and from gates 66 and 107.
  A block also ends with its container. Text after a file's last line end
  that holds only spaces and tabs is not a line, as markdown-it-py reads
  it, so it ends no container.
- HTML blocks are read two ways. The CommonMark reading matches a tag name,
  in a block start or in a type-1 closer such as ``</script>``, ignoring
  ASCII case only; ends an unquoted attribute value at a space, a quote,
  ``=``, ``<``, ``>`` or a backtick; and holds an HTML block of type 1 to 5
  in a list item to its end condition across blank lines. markdown-it-py
  3.0.0's reading matches a tag name under Unicode case folding (so
  ``<script>`` spelled with a long s, U+017F, starts a type-1 block); also
  ends an unquoted attribute value at U+0000 to U+0020; and also ends an
  HTML block of type 1 to 5 in a list item at a blank line indented less
  than the content columns of the list items it is in (counted inside the
  innermost block quote). Both readings take only a space (or a tab) as
  the separator after a tag name, around an attribute and its ``=``,
  before ``>`` and to the end of the line; a third reading, markdown-it-py
  3.0.0's with Python's ``\\s`` there as its HTML block starts take it
  (also U+000B, U+000C, U+001C to U+001F and Unicode spaces such as
  U+00A0), is otherwise markdown-it-py's reading. No reading alone checks
  more lines: a line that one reading starts an HTML block on hides the
  table after it, which another reading renders after the line as text,
  and a line one reading reads as text in a block quote or list item makes
  the table after it lazy text, which another renders after the HTML block
  ends the container. The file is scanned under each reading, and the row
  findings of all three are reported; the unclosed-block findings and the
  table and row counts are those of the CommonMark reading.
- A row's cells come from splitting on every ``|`` that is not directly
  preceded by a backslash, then dropping one empty leading cell and one
  empty trailing cell, so a row that is only a pipe has no cells. The row
  is first trimmed with ``str.strip()``, as markdown-it-py trims it. A pipe
  after a backslash is escaped even when that backslash itself follows a
  backslash, as markdown-it-py 3.0.0 reads it. A pipe inside a backtick
  code span splits the cell too: GFM table parsing splits a row into cells
  before inline code is parsed, so a literal pipe in a table code span is
  written ``\\|``.
- A table starts at a line of Markdown text holding a pipe, escaped or
  not, as markdown-it-py reads it, that is directly followed, inside the
  same containers, by a delimiter row: every cell, trimmed of spaces and
  tabs only, matches ``:?-+:?`` and the cell count equals the header's
  (markdown-it-py admits no other character to a delimiter row, so a
  no-break space in it makes the line text). A header with no cells, or a
  header and delimiter of different counts, do not form a table and are
  not checked.
- Body rows are the lines after the delimiter row until the table ends. A
  blank line ends it, and so does a line that does not continue the table's
  containers or that starts another block, as GFM table parsing ends it: a
  block quote, a list item, an ATX heading, a thematic break, a fence, an
  HTML block start of CommonMark types 1 to 6, or a line indented four or
  more columns in the table's container. None of these is a finding.
- Findings, each printed as ``path:line header=N row=M``: a body row whose
  cell count M differs from the header's N; and, by house rule, a body row
  that does not start with ``|`` after its indentation of spaces and tabs
  (so a row starting with a no-break space is one). GFM accepts such a row
  (a renderer shows a line without a pipe as a one-cell row), but this
  repository writes every body row with a leading pipe, so the row is a
  finding even when its count matches: suffix ``no-leading-pipe`` when it
  holds an unescaped pipe, else
  ``lazy-row`` (M=1 for a line of text). Scanning continues after such a
  row, so the rows after it are checked too. An unclosed block is a finding
  at its opening line, printed with the closer to add, and "unclosed" means
  two things. ``path:line unclosed-fence`` is the Markdown block: a fence
  still open at the end of the file (a fence that ends with its container
  is closed there, as renderers close it, and renders as code). A renderer
  that ends it sooner would show tables after it that this gate did not
  check. ``path:line unclosed-html-block`` is the HTML syntax: an HTML
  block of type 1 to 5 whose end condition never appears in the block, as
  the CommonMark reading holds it; only that reading reports it. It is
  reported when the block runs to the end of the file, and also when its
  block quote or list item ends it first, because the block's raw opener,
  such as ``<!--``, then reaches the page unterminated and a browser can
  read what follows as inside it. A block that markdown-it-py ends at a
  blank line in a list item is reported only when the CommonMark reading
  finds no closer either.

Exit codes:

  0   clean.
  1   one or more findings.
  2   any input could not be read or was refused: a refused ``--root``
      (an empty value, or a path that is not a directory as given or
      cannot be resolved), the tracked-file listing failed or listed no
      ``.md`` file, or a listed ``.md`` file is missing, unreadable or not
      UTF-8. A refusal never reports a clean verdict.

Residue: a row with the right count but content in the wrong column; a wrong
header (every body row is then flagged instead); non-Markdown surfaces; a
table inside an HTML block, which CommonMark shows as raw HTML (not
checked); a fence or HTML block that this model reads as never closed
while a renderer closes it, reported as unclosed (a possible false
positive, such as a ``<script>`` block closed only by ``</script>``
spelled with a long s, which markdown-it-py ends; the tables after it are
checked once it is closed, in that case under markdown-it-py's reading);
in an HTML block of type 1 to 5 in a list item, table-shaped lines after
a blank line indented less than the item's content column, checked under
markdown-it-py's reading although CommonMark shows them as raw HTML (a
possible false positive: indent that blank line to the content column);
under that reading, the block's opener left unterminated when its closer
comes only after such a blank line, and a block opened after the blank
line that stays open, neither reported as unclosed (the unclosed findings
are the CommonMark reading's; the rows after the blank line are checked);
whitespace other than spaces and tabs where markdown-it-py reads it as
space: a line holding only such whitespace directly after a table row,
which markdown-it-py's table rule (trimming with ``str.strip()``) takes as
the table's end, read as a body row and flagged ``lazy-row`` (a possible
false positive; GFM's blank-line definition also makes it a row), and
such whitespace wherever markdown-it-py's HTML block starts take Python's
``\\s``: after a type-1 or type-6 tag name, and in a type-7 tag before an
attribute, around its ``=``, before the closing ``>`` or ``/>`` and after
the tag to the end of the line, open or closing tag alike (such as a
no-break space after ``<span>``, or in place of the space in ``<span >``
or ``</span >``). markdown-it-py accepts such a line as the start of an
HTML block; only the third reading reads it so (the CommonMark reading
also does when it takes the whitespace into an unquoted attribute value,
as in ``<a href=x``, U+001F, ``>``), and its row findings are reported,
so a table that markdown-it-py renders after the line once its block
quote or list item ends the block is checked (for ``> <span>`` and a
no-break space, then a table; for ``1. <a href=x``, U+000B, ``>``, then
``<b x=``, U+0001, `` y=z>`` and a table; and, after a tag name that
matches only under Unicode case folding, for ``> - <ſcript>`` or
``> - <dıv>``, then ``> <a href=x``, U+001F, ``>`` and a table after the
quote). Where markdown-it-py's block instead holds the table-shaped lines
after such a line (at the top level, or inside the same block quote, as
for ``<span``, U+00A0, ``>`` and a table, or for ``> - <ſcript>``,
``> <a href=x``, U+001F, ``>`` and a quoted table), the other two
readings check them (a possible false positive). The subtests of
``test_html_block_starts_read_with_python_whitespace`` in
``tests/test_linters.py`` show that the starts named there are caught:
a tag name that matches only under Unicode case folding (``<ſcript>``,
``<dıv>`` and ``<ſtyle>``), and U+000B, U+000C, U+001C, U+001E, U+001F,
U+00A0 or U+2003 where markdown-it-py's HTML block starts take ``\\s``.
A residual not fixed in this change, and not characterized exactly: a
table after a paragraph inside a block quote (or inside a list item or
further quote within one) that a following line indented four or more
columns ends can have a short row this gate passes, in more than one
arrangement of those containers (for ``> > text``, ``    <!--`` and a
quoted table with a short row, markdown-it-py 3.0.0 renders the indented
line as indented code and then the table; the gate before backlog 3b617
misses it too, and backlog 3b640 tracks the fix); table-shaped lines that one reading holds in an HTML
block, or reads as lazy text, while another renders them as a
table, checked (a possible false positive for the renderer of the first
reading: after ``<script>`` spelled with a long s, U+017F, markdown-it-py
shows a table as raw HTML while this gate checks it); a line in a list item's
paragraph that is indented four or more columns but less than the item's
content column and starts a block, such as ``>``, which CommonMark reads
as lazy paragraph text, while markdown-it-py measures its indent from the
content column, so it ends the paragraph and the item there and the line
and the indented lines after it render as indented code, read as
CommonMark reads it (for ``1.   x``, ``    >``, ``     <!--`` and
``Text``, the comment is reported as unclosed while markdown-it-py shows
it as code: a possible false positive); a lazy continuation line followed
by a delimiter row, read as markdown-it-py reads it outside a list item
the line does not continue, and inside a block quote, where markdown-it-py
forms no table, read so under markdown-it-py's reading but checked as a
table under the CommonMark reading (a possible false positive); the next
line that leaves the quote ends that table, and when it starts an HTML
block there, which markdown-it-py reads as lazy text, the block hides a
later table from the CommonMark reading, so that table is checked under
markdown-it-py's reading only (for ``> | x |``, ``| y |``, ``> |---|``,
``<a href=xx>`` and a quoted table with a short row); a list item line
that, with the next line, could also head a table, which is
checked as a table (a possible false positive); and any
other difference between this block model and a renderer: it was compared
with markdown-it-py 3.0.0 only, not with GitHub's renderer or the site
generator.

``--root`` points the audit at another git work tree (the regression tests'
fixture repositories). Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# A line ends at LF, CRLF or a lone CR, as markdown-it-py normalizes it.
LINE_END_RE = re.compile(r"\r\n?|\n")
# Lines are matched after tab expansion, so a space pattern covers tabs too. A
# block quote opens on a ">" indented at most three columns; markdown-it-py
# continues one on a ">" at any indentation, and so does this gate.
QUOTE_RE = re.compile(r" {0,3}> ?")
QUOTE_CONTINUED_RE = re.compile(r" *> ?")
# A list marker's digits are ASCII, as CommonMark and markdown-it-py read them
# (Python's \d would also take other scripts' digits, such as U+0661).
LIST_RE = re.compile(r"( {0,3})([-+*]|[0-9]{1,9}[.)])(?= |$)( *)")
FENCE_RE = re.compile(r" {0,3}(`{3,}|~{3,})(.*)$")
ATX_RE = re.compile(r" {0,3}#{1,6}(?: |$)")
THEMATIC_RE = re.compile(r" {0,3}(?:(?:\* *){3,}|(?:- *){3,}|(?:_ *){3,})$")
SETEXT_RE = re.compile(r" {0,3}(?:=+|-+) *$")
DELIMITER_CELL_RE = re.compile(r":?-+:?")
UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")

# HTML block starts with their end conditions (None: a blank line), CommonMark
# types 1 to 7 in order. Type 4 needs an uppercase letter, as in markdown-it-py
# 3.0.0 and CommonMark before 0.31. The type-6 names equal markdown-it-py
# 3.0.0's block_names list (62 names). HTML_BLOCKS holds them under each
# reading, keyed by scan_lines's quirk: CommonMark's ignores ASCII case only in
# a tag name (re.A: markdown-it-py's Unicode re.I also takes U+017F for "s") and
# ends an unquoted attribute value at a space, a quote, "=", "<", ">" or a
# backtick; markdown-it-py's also ends the value at U+0000 to U+0020. No
# reading alone checks more lines: a start one reads as text, in a block quote
# or list item, makes the lines after it lazy text, so all are scanned.
HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|"
    "details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|"
    "h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|"
    "noframes|ol|optgroup|option|p|param|section|source|summary|table|tbody|td|tfoot|th|"
    "thead|title|tr|track|ul"
)


def html_blocks(flags: re.RegexFlag, unquoted: str, space: str = " "
                ) -> tuple[tuple[re.Pattern[str], re.Pattern[str] | None], ...]:
    """HTML block starts and end conditions whose tag names match under
    ``flags``, whose unquoted attribute values are runs of ``unquoted`` and
    whose separators after a tag name, between attributes, around ``=`` and
    before the end of the line are runs of ``space``."""
    attribute = (rf"""(?:{space}+[A-Za-z_:][A-Za-z0-9_.:-]*"""
                 rf"""(?:{space}*={space}*(?:{unquoted}+|'[^']*'|"[^"]*"))?)""")
    return (
        (re.compile(rf" {{0,3}}<(?:script|pre|style|textarea)(?:[{space}>]|$)", flags),
         re.compile(r"</(?:script|pre|style|textarea)>", flags)),
        (re.compile(r" {0,3}<!--"), re.compile(r"-->")),
        (re.compile(r" {0,3}<\?"), re.compile(r"\?>")),
        (re.compile(r" {0,3}<![A-Z]"), re.compile(r">")),
        (re.compile(r" {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
        (re.compile(rf" {{0,3}}</?(?:{HTML_BLOCK_TAGS})(?:[{space}>]|/>|$)", flags), None),
        (re.compile(rf" {{0,3}}(?:<[A-Za-z][A-Za-z0-9-]*{attribute}*{space}*/?>"
                    rf"|</[A-Za-z][A-Za-z0-9-]*{space}*>){space}*$"), None),
    )


# The third reading, markdown-it-py's with Python's \s wherever its HTML block
# starts take it (also U+000B, U+000C, U+001C to U+001F and Unicode spaces such
# as U+00A0); scan_lines reads it as markdown-it-py's (a true quirk).
WHITESPACE = 2
HTML_BLOCKS = {False: html_blocks(re.I | re.A, r"""[^ "'=<>`]"""),
               True: html_blocks(re.I, r"""[^"'=<>`\x00-\x20]"""),
               WHITESPACE: html_blocks(re.I, r"""[^"'=<>`\x00-\x20]""", r"\s")}
# What ends an HTML block of types 1 to 5, for the unclosed-block hint.
HTML_CLOSERS = ("</script>, </pre>, </style> or </textarea>", "-->", "?>", ">", "]]>")

# A container on the stack: a block quote, or a list item held as its content
# column (2 or more) relative to the enclosing container.
QUOTE = 0


class InputError(Exception):
    """An input the audit cannot read; the run exits 2."""


def split_cells(content: str, trim: str | None = None) -> list[str]:
    """Cells of one row: split on unescaped pipes, then drop one empty
    leading and one empty trailing cell, so a row that is only a pipe has
    none. The row is trimmed with ``str.strip()``, as markdown-it-py trims it
    (``trim``: the characters to trim instead)."""
    cells = UNESCAPED_PIPE_RE.split(content.strip(trim))
    if cells and not cells[0]:
        cells = cells[1:]
    if cells and not cells[-1]:
        cells = cells[:-1]
    return cells


def is_delimiter(content: str) -> bool:
    """True when every cell of ``content``, trimmed of spaces and tabs only,
    matches ``:?-+:?``: markdown-it-py admits no other character to a
    delimiter row, so a no-break space makes the line text."""
    cells = split_cells(content, " \t")
    return "-" in content and all(DELIMITER_CELL_RE.fullmatch(c.strip(" \t")) for c in cells)


def indent_of(content: str) -> int:
    return len(content) - len(content.lstrip(" "))


def continued(container: int, rest: str) -> str | None:
    """``rest`` after ``container``'s continuation, or None when the line
    does not continue it."""
    if container == QUOTE:
        quote = QUOTE_CONTINUED_RE.match(rest)
        return rest[quote.end():] if quote else None
    if not rest.strip(" \t"):
        return ""
    return rest[container:] if indent_of(rest) >= container else None


def opened(rest: str, interrupts: bool) -> tuple[int, str] | None:
    """(container, rest after its marker) when ``rest`` starts a block quote
    or list item. ``interrupts``: the line would otherwise continue a
    paragraph, which an empty item or an ordered item not numbered 1 cannot
    interrupt."""
    quote = QUOTE_RE.match(rest)
    if quote:
        return QUOTE, rest[quote.end():]
    item = LIST_RE.match(rest)
    if not item or THEMATIC_RE.match(rest):
        return None
    marker, spaces, after = item.group(2), len(item.group(3)), rest[item.end():]
    if interrupts and (not after or (marker[0] in "0123456789" and int(marker[:-1]) != 1)):
        return None
    width = len(item.group(1)) + len(marker) + (1 if not after or spaces > 4 else spaces)
    return width, rest[width:]


def fence_opener(rest: str) -> re.Match[str] | None:
    fence = FENCE_RE.match(rest)
    if fence and not (fence.group(1)[0] == "`" and "`" in fence.group(2)):
        return fence
    return None


def html_block(rest: str, interrupts: bool, quirk: int) -> int | None:
    """Index into HTML_BLOCKS[quirk] of the HTML block ``rest`` starts; type 7
    cannot interrupt a paragraph."""
    for kind, (start, _end) in enumerate(HTML_BLOCKS[quirk]):
        if start.match(rest) and not (interrupts and kind == 6):
            return kind
    return None


def starts_leaf(rest: str, quirk: int) -> bool:
    """True when ``rest`` starts a block that ends a table body or
    interrupts a paragraph (containers and indented code apart)."""
    return bool(fence_opener(rest) or ATX_RE.match(rest) or THEMATIC_RE.match(rest)
                or html_block(rest, True, quirk) is not None)


def header_width(rest: str, following: str | None, stack: list[int]) -> int:
    """The header's cell count when ``rest`` and the ``following`` line,
    read through every container on ``stack``, open a table; else 0."""
    if following is None or "|" not in rest:
        return 0
    delimiter: str | None = following.expandtabs(4)
    for container in stack:
        delimiter = continued(container, delimiter)
        if delimiter is None:
            return 0
    if indent_of(delimiter) >= 4 or opened(delimiter, False) or not is_delimiter(delimiter):
        return 0
    width = len(split_cells(rest))
    return width if len(split_cells(delimiter)) == width else 0


def scan_lines(lines: list[str], quirk: int) -> tuple[list[tuple[int, str]], int, int]:
    """(findings as (line, text) pairs, tables, body rows) for one file's
    lines. ``quirk`` (True or WHITESPACE): markdown-it-py 3.0.0's reading, in
    which an HTML block of type 1 to 5 in a list item also ends at a blank
    line indented less than the content columns of the list items inside the
    innermost block quote, and HTML blocks start and end as
    HTML_BLOCKS[quirk] reads them."""
    findings: list[tuple[int, str]] = []
    tables = rows = width = 0
    stack: list[int] = []
    leaf: str | None = None
    fence = ("", 0)
    html_end: re.Pattern[str] | None = None
    opener, close_with = 0, ""
    empty_item = -1
    i = 0
    while i < len(lines):
        following = lines[i + 1] if i + 1 < len(lines) else None
        rest = lines[i].expandtabs(4)
        matched = 0
        quoted, item_columns = rest, 0
        for container in stack:
            nxt = continued(container, rest)
            if nxt is None:
                break
            rest, matched = nxt, matched + 1
            if container == QUOTE:
                quoted, item_columns = rest, 0
            else:
                item_columns += container
        # Only spaces and tabs are blank, as CommonMark and markdown-it-py read it.
        blank = not rest.strip(" \t")
        if blank and 0 <= empty_item < matched:
            matched = empty_item
        empty_item = -1
        whole = matched == len(stack)
        i += 1
        if leaf in ("fence", "html", "code"):
            if whole:
                if leaf == "fence":
                    closer = FENCE_RE.match(rest)
                    if (closer and closer.group(1)[0] == fence[0]
                            and len(closer.group(1)) >= fence[1]
                            and not closer.group(2).strip(" \t")):
                        leaf = None
                    continue
                if leaf == "html":
                    if html_end.search(rest) if html_end else blank:
                        leaf = None
                    elif quirk and html_end and blank and indent_of(quoted) < item_columns:
                        leaf = None
                    continue
                if blank or indent_of(rest) >= 4:
                    continue
            elif leaf == "html" and html_end is not None:
                # The block ends with its container before its end condition, so
                # its raw opener still reaches the page unterminated.
                findings.append((opener, f"unclosed-html-block: close it with a line holding "
                                         f"{close_with}, indented as its opening line"))
            leaf = None
        if leaf == "para" and not whole and not blank:
            # A line that would head a table with the next line is not lazy
            # text: markdown-it-py ends the list items it does not continue and
            # reads it again outside them. Under a block quote it does not
            # continue, markdown-it-py forms no table, so its reading keeps the
            # line as lazy text and a line after the quote can be lazy text too;
            # the CommonMark reading checks a table there, inside the quote.
            width = header_width(rest, following, stack)
            quoted_header = width and QUOTE in stack[matched:]
            if quoted_header and not quirk:
                tables, leaf = tables + 1, "table"
                i += 1
                continue
            if (not width or quoted_header) and not opened(rest, False) and (
                    indent_of(rest) >= 4 or not starts_leaf(rest, quirk)):
                continue
        if not whole:
            stack, leaf = stack[:matched], None
        if leaf == "table":
            if not (blank or indent_of(rest) >= 4 or opened(rest, False)
                    or starts_leaf(rest, quirk)):
                # Only spaces indent a row (tabs are expanded), so a row starting
                # with a no-break space does not start with "|".
                body = rest.lstrip(" ")
                rows += 1
                count = len(split_cells(body))
                if not body.startswith("|"):
                    suffix = "no-leading-pipe" if UNESCAPED_PIPE_RE.search(body) else "lazy-row"
                    findings.append((i, f"header={width} row={count} {suffix}"))
                elif count != width:
                    findings.append((i, f"header={width} row={count}"))
                continue
            leaf = None
        while True:
            if not rest.strip(" \t"):
                leaf = None
                break
            if indent_of(rest) >= 4:
                leaf = "para" if leaf == "para" else "code"
                break
            width = header_width(rest, following, stack)
            if width:
                tables, leaf = tables + 1, "table"
                i += 1
                break
            fenced = fence_opener(rest)
            if fenced:
                leaf, opener, close_with = "fence", i, fenced.group(1)
                fence = (fenced.group(1)[0], len(fenced.group(1)))
                break
            got = opened(rest, leaf == "para")
            if got:
                stack.append(got[0])
                rest, leaf = got[1], None
                if got[0] != QUOTE and not rest.strip(" \t"):
                    empty_item = len(stack) - 1
                continue
            kind = html_block(rest, leaf == "para", quirk)
            if kind is not None:
                html_end = HTML_BLOCKS[quirk][kind][1]
                leaf = None if html_end is not None and html_end.search(rest) else "html"
                if html_end is not None:
                    opener, close_with = i, HTML_CLOSERS[kind]
                break
            if ATX_RE.match(rest) or THEMATIC_RE.match(rest) or (
                    leaf == "para" and SETEXT_RE.match(rest)):
                leaf = None
                break
            leaf = "para"
            break
    # A block still open here holds the rest of the file. A renderer that
    # ends it sooner would show tables after it that were not checked.
    if leaf == "fence":
        findings.append((opener, f"unclosed-fence: close it with a line of {close_with}, "
                                 f"indented as its opening line"))
    elif leaf == "html" and html_end is not None:
        findings.append((opener, f"unclosed-html-block: close it with a line holding "
                                 f"{close_with}, indented as its opening line"))
    return findings, tables, rows


def scan_text(rel: str, text: str) -> tuple[list[str], int, int]:
    """(findings, tables, body rows) for one file's text: the row findings of
    the three readings, CommonMark's, markdown-it-py's and markdown-it-py's
    with \\s separators, and the unclosed-block findings and counts of the
    CommonMark reading."""
    # U+0000 is read as U+FFFD, as CommonMark and markdown-it-py replace it.
    lines = LINE_END_RE.split(text.replace("\0", "\ufffd"))
    if not lines[-1].strip(" \t"):
        # Not a line, as markdown-it-py reads it: a block quote running to the
        # end of the file holds its fence to the end, with or without a final LF.
        lines.pop()
    found, tables, rows = scan_lines(lines, False)
    quirk_rows = [f for quirk in (True, WHITESPACE) for f in scan_lines(lines, quirk)[0]
                  if f[1].startswith("header=")]
    return [f"{rel}:{line} {what}" for line, what in sorted(set(found + quirk_rows))], tables, rows


def tracked_markdown(root: Path) -> list[Path]:
    """Tracked ``.md`` files; a failed listing is an InputError."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise InputError(f"cannot run git ls-files: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise InputError(f"git ls-files failed (exit {result.returncode}): {detail}")
    names = [os.fsdecode(n) for n in result.stdout.split(b"\0") if n]
    return sorted(root / n for n in names if n.lower().endswith(".md"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Every tracked Markdown table body row has its header's cell count.")
    parser.add_argument("--root", default=None,
                        help="git work tree to audit (default: this repository)")
    args = parser.parse_args(argv)
    root = REPO_ROOT
    if args.root is not None:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lint_common import require_dir
        root = require_dir(args.root, "--root")
    try:
        files = tracked_markdown(root)
    except InputError as exc:
        print(f"ERROR: {exc}; nothing was checked.", file=sys.stderr)
        return 2
    if not files:
        print(f"ERROR: git ls-files lists no .md file under {root}; nothing was checked.",
              file=sys.stderr)
        return 2
    findings: list[str] = []
    errors = 0
    tables = rows = 0
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"ERROR: {rel}: unreadable ({exc})", file=sys.stderr)
            errors += 1
            continue
        found, t, r = scan_text(rel, text)
        findings += found
        tables += t
        rows += r
    for finding in findings:
        print(finding)
    if errors:
        print(f"ERROR: {errors} tracked .md file(s) could not be read; no clean verdict "
              f"is given.", file=sys.stderr)
        return 2
    if findings:
        print(f"FAIL: {len(findings)} table cell-count finding(s). header=N is the header "
              f"row's cell count and row=M the flagged line's. A ref-absence marker inside "
              f"a table row takes a single query, <!-- ref-absence: query -->: gate 104 "
              f"splits marker queries on a bare pipe and keeps a backslash, so escaping a "
              f"marker's pipe would stop gate 104 detecting the query as stale. Escape any "
              f"other literal pipe as \\| (also inside backticks); no-leading-pipe: start "
              f"the row with '|'; lazy-row: add a blank line after the table; "
              f"unclosed-fence: the fence opened on that line never closes, so the rest of "
              f"the file renders as code and no table there is checked; unclosed-html-block: "
              f"the HTML block opened on that line ends, with the file or with its list item "
              f"or block quote, before its closer appears, so a browser can read what "
              f"follows as inside it (a line meant to close a block in a list item or block "
              f"quote must continue that container).")
        return 1
    print(f"OK: table cell counts match their headers across {len(files)} tracked .md "
          f"files ({tables} tables, {rows} body rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
