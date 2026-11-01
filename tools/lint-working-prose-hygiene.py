#!/usr/bin/env python3
"""Prose-hygiene audit for the `.working/` maintainer working tree (gate 51).

The corpus-wide language gate (`lint-language.py`, gate 2) forbids em-dashes
and en-dashes in prose, but it exempts the `.working/` tree (the
maintainer working space is in `DEFAULT_EXEMPT_DIRS`). The 2026-06-26 em-dash
conformance pass (#353) brought `.working/` prose into line with the house
style, leaving a small set of *intentional* em/en-dash literals inside inline
code spans (regex character classes such as ``[\u2013\u2014]``, frozen historical
quotes, the house-style rule's own glyph examples). This gate ratchets that
conformance: it forbids em/en-dashes in `.working/` PROSE while ALLOWING them
inside inline code spans, so the conformance cannot silently regress.

The principled boundary (established by the #353 bulk apply): a dash is a
prose violation only if it appears outside an inline code span and outside a
fenced code block. Dashes inside code spans are content (a regex literal, a
quoted format string), not prose, and are left untouched.

Scope is the `.working/` tree ONLY, minus any `guardrail-seeds` directory
(see EXEMPT_DIRS: a directory-NAME-component match, so the guardrail-seed pipeline
inbox and everything under it is skipped; it holds verbatim foreign seed prose,
exempt from the store house-style). Keep maintainer control docs and records OUT
of a `guardrail-seeds` directory so they stay scanned. The corpus proper is covered by
`lint-language.py`, whose default whole-file scan also covers the root
`CHANGELOG.md`. The D3 dash gate (`check-changelog-dash-on-pr.py`) additionally
checks every added CHANGELOG line, including code. This working-tree gate
does not scan the root `CHANGELOG.md` by default.

Detection logic (3b696): the gate carries its own fence and code-span model,
following CommonMark 0.31 where it names a rule. Until 3b696 it toggled on any
line starting with three fence characters and stripped spans per line with
``(`+)(.+?)\\1``; that regex is not CommonMark's rule (it backtracks to a
shorter opener and accepts a closer that is part of a longer run), and the
toggle hid prose or refused code for the shapes the 3b609 reviews listed.
Lines are CommonMark lines (``commonmark_lines``), numbered from 1: CommonMark
0.31.2 section 2.1 ends a line only at "a line feed (`U+000A`), a carriage
return (`U+000D`) not followed by a line feed, or a carriage return and a
following line feed", so VT, FF, FS to RS, U+0085, U+2028 and U+2029, which
``str.splitlines()`` also breaks at, stay inside their line (3b696 round 19;
until then the gate used ``str.splitlines()``, and a link destination or
autolink holding one of them failed to form, so its backtick paired as a span
and hid a dash). One leading U+FEFF (a
byte-order mark) is dropped first, and each NUL (U+0000) is read as U+FFFD
before parsing, as CommonMark 0.31.2 section 2.3 requires. The replacement is
in place and NUL breaks no line, so line numbers (and the preflight's mapping
of each line back to its LF line) are unchanged; a snippet shows U+FFFD where
the file holds NUL. Indent is counted in columns, with leading tabs expanded
to tab stops of 4.

Fences:

  F1. A line outside a fence opens one at an indent of 0 to 3 columns (past
      the content column of the list item it is inside, L1) with a run of 3
      or more backticks or 3 or more tildes; the rest is the info string,
      which for a backtick fence must not hold a backtick (such a line is a
      paragraph, scanned as prose).
  F2. A container opener. A list-marker line (0 to 3 columns past the
      enclosing item's content column, ``-``, ``+``, ``*`` or 1 to 9 digits
      and ``.`` or ``)``, then 1 to 4 spaces; one marker may follow another
      on the line, a nested item) whose content is an F1 run opens a fence
      inside the item at content column W (the marker plus the gap). An
      ordered marker other than 1 on a line inside the open paragraph's
      container (I1) opens no item, because CommonMark keeps that line
      paragraph text, so its run opens no fence. A line inside an open list
      item whose content past W is an F1 run opens a fence inside that item.
      A line of one or more block-quote markers (each 0 to 3 spaces, ``>``
      and one optional space, read as Q1 reads them) whose content is an F1
      run opens a fence inside a quote of that depth, inside the list item
      Q1 reads it in, if any.
  F3. Inside a fence of character c and run length n, a line closes it when
      its content (inside the container, if any) is 0 to 3 columns of indent,
      a run of c of length n or more, and only spaces or tabs. Any other line
      is fence content: a shorter run, a run of the other character, or a run
      followed by an info string.
  F4. A container ends its fence. In a list item, a non-blank line indented
      less than W ends the item and the fence; in a quote, a line without
      that many quote markers does (a blank line included), and so, for a
      quote inside a list item, does a line indented less than the item's W,
      whose quote markers (a ``>`` at column 0, say) start another quote.
      That line is then read as a line outside any fence. Fenced code has no
      lazy continuation.
  U1. A fence still open at the end of the file is a finding,
      ``L<n> [unclosed-fence]`` on its opener, and exits 1. CommonMark lets
      such a fence run to the end of the document; the gate refuses it by
      rule, because a stray opener would otherwise hide every later line.
      Fence lines and fence content are not scanned for dashes.
  L1. A list item opened outside any quote stays open while the non-blank
      lines below it are indented W or more; a lazy paragraph continuation
      line (I1) leaves it open, and any other line ends it, as does a quote
      line whose first marker is indented less than W. Blank lines leave it
      open, except that an item whose marker line holds nothing else can
      begin with at most one blank line: that blank line ends it, as in
      CommonMark, so an indented line after it is not the item's content.
  Q1. Quote markers are read at the content column of the innermost open
      list item the line is indented into (column 0 outside any item), and
      on a list-marker line after the markers (``- > text``), where the quote
      opens inside the new item. A quote line belongs to the quote inside
      that item; a quote line outside the item (fewer columns of indent)
      starts another quote, a new unit (I1), since a quote opener is not a
      lazy continuation.

Inline units (a code span may cross a line ending, as in CommonMark):

  I1. Outside fences, consecutive non-blank lines form one unit, standing in
      for a paragraph; a blank line (a quote line with nothing after its
      markers included) or a fence ends it. A line continues the open
      paragraph unless it starts one of the blocks below, either inside the
      paragraph's container (the same number of quote markers, read in the
      same list item (Q1), and, without quote markers, indented at least the
      paragraph's item column) or lazily (fewer quote markers, or less
      indented than that column; a lazy line joins, as in CommonMark). These
      lines start a new unit:
        - a line with more quote markers than the unit's first line (a
          quote interrupts a paragraph), or with quote markers read in
          another list item (Q1), a list-marker line that opens a quote
          included;
        - a list-marker line 0 to 3 columns past the enclosing item's
          content column (L1), except that an ordered marker other than 1
          or an empty item, inside the paragraph's container, is paragraph
          text (CommonMark does not let it interrupt a paragraph); a marker
          indented 4 or more past that column is paragraph text too;
        - after a unit whose first line is indented 4 or more past its
          container (indented code in CommonMark), the first line indented
          less. A line indented 4 or more below a paragraph line joins it.
      These are each a unit alone: an ATX heading or a thematic break,
      including one that is the content of a list-marker line (markers are
      read before headings); a setext underline (a run of ``=`` or ``-``)
      inside the paragraph's container, while a lazy one is paragraph text,
      and so is one below a unit of link reference definitions alone (I6),
      which leaves no text to underline, so the underline and the lines
      after it are paragraph text and no later definition is read (a
      definition cannot interrupt a paragraph). A ``---`` there is paragraph
      text too, though it is also thematic-break-shaped: cmark-gfm's
      src/blocks.c tries the setext branch first, in an else-if chain, so
      its thematic-break branch never reads that line (``- - -`` and ``***``
      are no setext underline, so they stay thematic breaks). Such an
      underline, then the paragraph's only text, can head a table as any
      paragraph line does. Also a unit alone: an empty list item; and each
      line of a GFM table, which starts at a header line whose next line is
      a delimiter row with as many cells (a line with no pipe is one cell,
      so ``a`` over ``:-:`` heads a table, as cmark-gfm's row grammar reads
      it) inside the container of the header line's paragraph (the open
      paragraph's when the header line continues it, lazily or not, else
      the line's own): at the same quote
      depth, its markers read where Q1 reads them, and 0 to 3 columns past
      the content column of the list item the table is in. A delimiter row
      holds cells of an optional ``:``, one or more ``-`` and an optional
      ``:``, split by pipes, a leading and a trailing pipe optional, so
      ``:---:`` under ``| a |`` is one (cmark-gfm's delimiter grammar); a run
      of ``-`` alone there is a setext underline, which cmark-gfm
      0.29.0.gfm.13 reads before a table (its src/blocks.c setext branch,
      line 1198, comes before the block-extension loop, line 1308; the
      CommonMark spec has no tables), and a thematic break of ``-`` with
      spaces between is outside that grammar. Table whitespace is
      cmark-gfm's spacechar, space, tab, VT and FF (extensions/ext_scanners.re
      line 30), in the two places its table scanner reads spacechar: around
      each marker of a delimiter row and before its line end, so a pipe, a
      VT, ``---`` and a pipe make a delimiter row; and after each pipe of any row,
      which takes the run after it, so text after a row's last pipe that is
      only spacechar is no cell (3b696 round 20; until then the gate read
      only spaces and tabs there, so a VT or FF in a delimiter row opened no
      table and its backtick runs paired across the rows). Nowhere else: a
      cell's text (``table_cell``) takes VT and FF as characters; a line's
      leading spaces and tabs are its indent, as before, and a VT or FF
      there is no indent, so it starts a cell in a header or body row and
      a marker's spacechar in a delimiter row; and the rest of the model
      (blank lines, setext underlines, thematic breaks, list markers and
      fence closers) reads only spaces and tabs, as before. A delimiter
      row outside that container is a lazy line and joins the paragraph,
      and so does one indented 4 or more columns past it. A line is a
      header or row only if cmark-gfm's
      extensions/table.c row_from_string parses it whole into 1 to 65535
      cells (``delim? table_cell (delim table_cell)* delim? newline``): a
      leading pipe is a border and an empty cell counts only before a pipe,
      so a lone pipe has no cell and is no row, while ``||`` is one empty
      cell and ``|  |  |`` two; a row of more than 65535 cells overflows
      and is none. A header line that is no row counts as another number of
      cells (row_from_string returns NULL and the paragraph is marked as
      below); a delimiter row that is no row opens no table and marks
      nothing. try_opening_table_header hands row_from_string the whole
      paragraph, not only the header line: the row walk restarts at each
      line ending and keeps the last line's cells, but a line above the
      header line with more than 65535 cells aborts the walk
      (append_row_cell's overflow ends the whole call), so the header is
      NULL there too, no table opens, and the paragraph is marked as below.
      Definitions a setext underline resolved (I6) have left the paragraph
      and are not read. No other line above the header can make it NULL:
      a cell takes every character but a pipe, CR and LF, so each such line
      reaches its line ending, except one that ends in a bare CR (the
      bare-CR residual). Once a delimiter row in a paragraph's container
      follows a line with another number of cells, no table opens in that
      paragraph: cmark-gfm's extensions/table.c then sets
      CMARK_NODE__TABLE_VISITED on the paragraph and opens no table in a
      paragraph that carries it, so a later header line and delimiter row
      there are paragraph text and the unit runs on. A line indented 4 or
      more columns past its own container that starts a unit is indented
      code and heads no table; one
      that continues a paragraph heads a table as any continuation line
      does, since cmark-gfm stores a continuation line in its paragraph's
      container without its indent and checks only the delimiter row's.
      A lazy continuation line is the exception: cmark-gfm's src/blocks.c
      adds it at the offset after the container prefixes it matched
      (lines 1375 to 1378, where the other branches advance to the first
      non-space character, 1434 and 1441), so it keeps the whitespace
      left there, and row_from_string reads that whitespace as a cell
      when a pipe follows it (only a pipe at the line's start is a
      border). The gate counts a lazy line's cells, as a header line and
      as a line above one (the 65535-cell bound), on its text after those
      prefixes with that whitespace kept: ``  | b |`` read lazily below
      ``> a`` is two cells, so it heads no table over ``> |---|`` and
      marks the paragraph as below, and it heads one over ``> |-|-|``.
      The table runs to a blank line,
      another block (indented code included: a
      line indented 4 or more columns past the table's container, where
      cmark-gfm opens no row), a line outside its quote or list item, or a
      line that is no row: a line that is no row ends the table (matches()
      continues a table only on a row with columns), and the line starts a
      new block. A row also ends the table once the table has autocompleted
      more than 524288 (0x80000) cells: extensions/table.c counts each
      row's columns less the cells parsed from it, up to the table's
      columns (get_n_autocompleted_cells), and try_opening_table_row then
      refuses the row, so the line starts a paragraph. The gate counts the
      same way; a table whose columns times rows passes 2**31 overflows
      cmark-gfm's C ``int`` there, which the gate does not model (a named
      residual, below). The
      content of a list-marker line outside any quote can head a table
      inside its new item, over a delimiter row at the item's content
      column. A row shaped as a list item (``- | -``) is that item, not a
      delimiter row, so it heads no table. A pipe-led line outside a table is
      paragraph text. Neither
      splitting nor joining is safe on its own: a split where CommonMark
      joins can leave a closing run to pair with a later one around a prose
      dash, and a join where it splits can pair runs across blocks, so the
      rules follow CommonMark's paragraph continuation where they can.
  I2. Outside a code span, a backslash before ASCII punctuation makes that
      character literal, so an escaped backtick opens nothing.
  I3. An autolink (``<scheme:...>`` or ``<user@host>``) is opaque: its
      backticks neither open nor close a span.
  I4. Raw HTML (an open or closing tag, comment, processing instruction,
      declaration or CDATA section, across the unit's line endings) is
      opaque. <!-- todo-ref-ok: CommonMark 0.31.2 Raw HTML section (6.6), not a backlog item -->
      An open or closing tag follows CommonMark 0.31.2 section 6.6:
      the whitespace in it is spaces, tabs and up to one line ending, and an
      unquoted attribute value holds any character but a space, tab, line
      ending, ``"``, ``'``, ``=``, ``<``, ``>`` or a backtick, so an ASCII
      control character is part of the value (3b696 round 18). A comment,
      processing instruction, CDATA section or
      declaration ends at the first terminator after its opener, and an
      opener with none after it in the unit fails without a rescan, so the
      scan is linear in the unit's length. Each line's leading whitespace and
      quote markers are set aside before I2 to I7 read the unit, as
      CommonMark strips container markers, so a marker does not break a
      construct that crosses a line ending.
  I5. An inline link destination and title, ``](...)`` after an unmatched
      unescaped active ``[`` (or ``![``, an image) in the unit, are opaque
      when they parse; so is a full reference label, ``][label]``, when a
      definition in the file (I6) defines that label. A span opened before
      the ``]`` still wins, because the scan runs left to right. A link holds
      no link, at any level of nesting: once one forms (an inline link, or a
      full, collapsed or shortcut reference to a defined label), each ``[``
      still unmatched before it is inactive, so the ``]`` that matches it is
      text and no destination follows; an image makes no opener inactive.
      A bare destination nests balanced parentheses up to 32 levels
      (markdown-it's limit; deeper, it does not parse) and holds no space
      and no ASCII control character (DEL included), and an autolink's URI
      no ASCII control character, space, ``<`` or ``>``; a backslash
      escapes only ASCII punctuation, so a backslash before a space or a line
      ending is a literal backslash and the space or line ending still ends
      the destination. A label holds 1 to 999 characters inside its brackets,
      counted as written (a backslash pair is two), at least one of them not
      a space, tab or line ending; labels match after case folding, with
      their spaces, tabs and line endings stripped at the ends and collapsed
      inside (NBSP and other Unicode whitespace are kept as they are).
  I6. Link reference definitions leading a unit are opaque: ``[label]:``
      (a label as I5 bounds it), a destination (on that line or the next, as
      I5 bounds a bare or ``<...>`` destination), and an optional title (on
      the destination's line or the next; it may run over several lines),
      with nothing else to the end of the last line. A setext underline in
      the paragraph's container (I1) ends the unit, and with it any title
      still open above it, as cmark-gfm 0.29.0.gfm.13 reads it (its
      src/blocks.c setext branch, lines 1198 to 1217, resolves the
      definitions in the lines above the underline through
      resolve_reference_link_definitions, lines 266 to 280; no CommonMark
      0.31.2 example covers a title cut this way, and markdown-it
      runs the title on over a ``===`` line): a definition whose destination
      ends its line then holds no title, and one with text after its destination is
      heading text. A first line that does
      not complete a definition (trailing words after the destination, for
      example) is paragraph text. Only a paragraph unit defines a label: an
      indented code unit (I1) is not a paragraph, and neither is a line that
      is a unit alone (I1), a table header or row included, so a
      definition-shaped table row defines none. A table header or row is
      inline text (a GFM table cell holds inlines, no block),
      so definition-shaped text in it is not opaque, and a code span there
      masks its dash as in any text. A pipe-less header line is
      no exception: ``[b]: /u`` over ``:-:`` heads a table, so it defines no
      label, as in cmark-gfm 0.29.0.gfm.13: its src/blocks.c resolves a
      paragraph's definitions only when the paragraph is finalized or a
      setext underline is found, after the block-extension loop has let
      extensions/table.c try_opening_table_header read the raw paragraph.
      Nor does a line above the header line in its paragraph: ``[b]: /u``
      over ``| h |`` over ``|---|``, or ``[b]: /u`` and ``[c]: /v`` over
      ``:-:``, defines no label, because try_opening_table_header hands those
      lines to try_inserting_table_header_paragraph, which builds them a new
      paragraph with cmark_node_new and inserts it before the table; that
      paragraph never enters the parser's chain of open blocks, which is all
      finalize_document finalizes, so its definitions are never resolved
      and stay text. The gate reads them as text too: that paragraph's unit
      has no opaque definitions, so a backtick run in a title there opens a
      span as in any text (I7). A definition already resolved by a setext
      underline below it (definitions alone, then ``===`` or ``---``, I1)
      keeps its label and stays opaque, so the paragraph's unit keeps kind
      "para" when a later line of it heads a table, and so does a
      definition in its own paragraph above the table.
  I7. At an unescaped, non-opaque backtick run of length n, the next maximal
      run of exactly n in the rest of the unit closes a code span, which
      masks everything from the opener to the closer. With no closer the run
      is literal. The closer search ignores escapes and opaque constructs.
  I8. A line whose unmasked characters hold U+2014 or U+2013 is reported as
      ``L<n> [prose-dash]``. Opaque constructs stay in the residue: a dash is
      prose unless it is in a code span or a fenced block.

Residuals, named. Where the model and CommonMark disagree on a block boundary
or a span, a dash can be reported that is code (fails safe) or, in the shapes
marked "can hide", missed:

  - Tabs in the marker gap or after a quote marker, and a list inside a
    quote (a list item inside a quote inside a list item included), are not
    recognised as fence containers or as unit boundaries; their lines are
    scanned as prose, so the fence content over-reports, but the opener's
    backtick run can pair as a span with a later run, and the closer can
    open a fence that ends with its container (can hide). A unit line whose
    first ``>`` is indented 4 or more columns past its container (paragraph
    text or indented code in CommonMark) has that ``>`` set aside as a
    quote marker before the inline read (I4), where CommonMark keeps it as
    text, and a quote opened on a list-marker line keeps its markers in the
    inline read; either changes only where a raw HTML tag or an autolink
    across the line ending can end (can hide, either way).
  - Block boundaries the units do not model (can hide): GFM table cells (a
    span can pair backticks across the cells of one table line, as before
    3b696); HTML blocks (read as inline units). One HTML-block shape hides
    since 3b696 round 11: a line above a table header line in its
    paragraph that starts an HTML block able to interrupt a paragraph
    (``<div>``, say) ends that paragraph in CommonMark, so cmark-gfm
    resolves the definitions above it, which are then opaque, while the
    gate reads every line above the header as the inserted paragraph's
    text (I6), so a backtick run in a definition's title there can pair as
    a span with one below it, around a dash on the HTML block's line
    (``[b]: /u '`'`` over ``<div>`` and a dash, then a line ending in a
    backtick, then ``| h |`` and ``|---|``). Indented code blocks are
    scanned as prose (fails safe), and a blank line inside one ends its
    unit.
  - A renderer that nests a destination's parentheses deeper than 32
    levels reads a destination where the gate reads text (can hide, either
    way); a link reference definition inside a list item is read as
    paragraph text, so a backtick run in its destination or title can pair as
    a span around a dash that is no code (can hide). Raw HTML comments follow
    CommonMark 0.31 (any text without ``-->``); a renderer on the older rule
    (no ``--`` inside a comment) reads some comments as text, and a backtick
    run inside one then pairs differently (can hide, either way).
  - The bare-CR residual: the gate splits at LF, CR and CRLF as CommonMark
    does (``commonmark_lines``), but it drops each line's ending, so it
    cannot see a bare CR: cmark-gfm's table scanners end a row only at LF
    or CRLF, so a header, delimiter or body row (or a paragraph line above
    a header) that ends in a bare CR leaves row_from_string short of the
    line end (``offset != len``): no table opens, a NULL header marks the
    paragraph, and a body row ends its table, while the gate, reading the
    same lines, opens or continues the table (can hide, either way).
  - cmark-gfm's extensions/table.c computes a table's autocompleted cells
    in C ``int`` (get_n_autocompleted_cells, 109 to 116: columns times
    rows, less the cells parsed), and that product overflows once it
    passes 2**31; the gate counts with Python's unbounded integers. Where
    the arithmetic wraps (two's complement), the wrapped difference equals
    the true count, which stays under 524288 plus 65535 at every check,
    so the two agree; but signed overflow is undefined in C, so a build
    that optimizes on it can refuse a row the gate continues, or keep one
    the gate refuses, and a backtick run then pairs differently around a
    dash (can hide, either way). It needs about 2**31 parsed cells, a
    file of about 2 GB or more.

``scan_lines`` applies the whole model to one file's lines and ``scan_text``
splits a file with ``commonmark_lines`` for it. ``tools/preflight-changelog.py``
loads this file and runs ``scan_lines`` over the whole new text of each changed
CHANGELOG file, splitting each of git's LF lines again with ``commonmark_lines``
(so at a bare CR) and mapping each piece back to its LF line (3b696 rounds 3
and 19), and keeps
the findings on added lines, so on an added line the two agree, except that
gate 51 skips a whole file that is not valid UTF-8 while the preflight decodes
it with ``surrogateescape`` and still scans its added lines.

Usage:
    python3 tools/lint-working-prose-hygiene.py [paths...]

With no arguments, scans the `.working/` tree, located via
``lint_common.resolve_working``: the operational store (``$GRC_STORE`` or
``<repo-parent>/private``) first, then the private sibling's ``.working/``
tree, then the in-repo ``.working/``. When none is
present (public CI / adopter clone) the gate no-ops with an OK line rather than
reporting a clean scan of zero files. A path argument (file or directory)
overrides the default, which the regression fixtures rely on to point the gate
at a single test file. Exits non-zero if any finding is reported.
"""

from __future__ import annotations

import bisect
import re
import string
import sys
from collections import defaultdict
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, guard_explicit_paths_cwd, iter_markdown_targets, positional_args, print_degraded, resolve_working  # noqa: E402  # grc-config/store, stays local


def default_scan_root() -> Path | None:
    """The `.working/` tree to scan, or None when it is not present.

    Routes the DEFAULT scan root through ``lint_common.resolve_working`` so the
    gate scans the operational store first, then the private sibling's
    ``.working/`` tree when the store is absent --
    without this the gate would silently scan nothing and the private prose's
    em/en-dashes would go undetected, un-ratcheting the #353 conformance. Falls
    back to the in-repo ``.working/``; returns None when none is present. An
    EXPLICIT path argument (the regression fixtures) overrides this entirely.

    ``"."`` denotes the `.working/` ROOT itself rather than a file inside it:
    pathlib drops a "." component, so the candidate is ``<store>`` first,
    then ``<private>/.working`` or ``<repo>/.working``; ``Path.exists()``
    is true for a directory.
    """
    return resolve_working(".")


def display_path(path: Path) -> str:
    """Repo-relative display path, absolute when the file is outside the repo.

    Post-migration the scanned files live in the operational store, so
    a bare ``relative_to(REPO_ROOT)`` raises ValueError on every finding -- the
    same robust-display pattern the other rewired `.working/` readers use.
    """
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()

# The `.working` tree is in DEFAULT_EXEMPT_DIRS for every other linter; this
# gate deliberately overrides that exemption to scan inside it. The remaining
# exemptions are the universal non-content dirs, plus `guardrail-seeds`: the
# operational store's guardrail-seed pipeline inbox holds VERBATIM foreign seed
# prose (worker/external theorycraft outputs, migrated seed archives). Those are
# not the maintainer's own working prose, so the store house-style (which targets
# ORCHESTRATOR store-writes) does not apply to them; forcing it would corrupt a
# migrated artefact. The seed inbox moved here when grc_library_scratch was
# retired (2026-08-29). This is a directory-NAME-component match (any
# `guardrail-seeds` dir under the store is skipped), so keep maintainer control
# docs and migration records OUTSIDE such a directory to keep them scanned.
EXEMPT_DIRS = frozenset({".git", "node_modules", "__pycache__", "guardrail-seeds"})

EM_DASH_PATTERN = re.compile(r"[\u2014\u2013]")  # em dash or en dash

# --- Fence model (F1 to F4, U1; see the module docstring) ---
TAB_STOP = 4
FENCE_RUN = re.compile(r" {0,3}(`{3,}|~{3,})(.*)\Z", re.S)
FENCE_CLOSER = re.compile(r" {0,3}(`+|~+)[ \t]*\Z")
QUOTE_MARKER = re.compile(r" {0,3}> ?")

# --- List items, inline units and spans (L1, I1 to I8) ---
LIST_MARKER = re.compile(r" {0,3}(?:[-+*]|([0-9]{1,9})[.)])(?=[ \t]|\Z)")
ATX_HEADING = re.compile(r" {0,3}#{1,6}(?:[ \t]|\Z)")
THEMATIC_BREAK = re.compile(r" {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})\Z")
SETEXT_UNDERLINE = re.compile(r" {0,3}(?:=+|-+)[ \t]*\Z")
# The table scanner's whitespace, cmark-gfm's spacechar (extensions/ext_scanners.re line 30): VT
# and FF too, around a delimiter row's markers and after a pipe (I1, 3b696 round 20).
SPACECHAR = " \t\v\f"
TABLE_DELIMITER = re.compile(
    r" {0,3}(?:[|\v\f][ \t\v\f]*)?:?-+:?[ \t\v\f]*(?:\|[ \t\v\f]*:?-+:?[ \t\v\f]*)*\|?[ \t\v\f]*\Z")
TABLE_PIPE = re.compile(r"(?<!\\)\|")
MAX_TABLE_CELLS = 65535  # UINT16_MAX: extensions/table.c append_row_cell refuses a cell past it
MAX_AUTOCOMPLETED_CELLS = 0x80000  # extensions/table.c line 15: a table's empty filler-cell cap
# A backslash escapes ASCII punctuation; before any other character it is a literal backslash, so
# it escapes no space, control character or line ending (I5, I6).
_PUNCT = "[" + re.escape(string.punctuation) + "]"
_ESC = rf"\\{_PUNCT}|\\(?!{_PUNCT})"
LABEL_MAX = 999  # characters inside a link label's brackets, counted as written (I5)
_LABEL = rf"\[((?:[^\[\]\\]|{_ESC}){{1,{LABEL_MAX}}})\]"
_BARE = rf"(?:[^\x00-\x20\x7f()\\]|{_ESC})"   # a bare destination: no space or ASCII control
_DESTINATION_ANGLE = rf"<(?:[^<>\n\\]|{_ESC})*>"
PAREN_DEPTH = 32  # balanced parentheses a bare destination nests, markdown-it's limit (I5)
_DESTINATION_BARE = _BARE
for _ in range(PAREN_DEPTH):
    _DESTINATION_BARE = rf"(?:{_BARE}|\({_DESTINATION_BARE}*\))"
_DESTINATION = rf"(?:{_DESTINATION_ANGLE}|(?!<){_DESTINATION_BARE}+)"
_TITLE = rf"(?:\"(?:[^\"\\]|{_ESC})*\"|'(?:[^'\\]|{_ESC})*'|\((?:[^()\\]|{_ESC})*\))"
DEFINITION = re.compile(
    rf" {{0,3}}{_LABEL}:[ \t]*\n?[ \t]*{_DESTINATION}"   # label, colon, destination
    rf"(?:(?:[ \t]+|[ \t]*\n[ \t]*){_TITLE})?"           # optional title
    r"[ \t]*(?=\n|\Z)"                                     # then nothing to the line end
)
REFERENCE = re.compile(_LABEL)
ESCAPABLE = frozenset(string.punctuation)  # CommonMark's ASCII punctuation
BACKTICKS = re.compile(r"`+")
AUTOLINK = re.compile(
    r"<[A-Za-z][A-Za-z0-9+.\-]{1,31}:[^\x00-\x20\x7f<>]*>"
    r"|<[A-Za-z0-9.!#$%&'*+/=?^_`{|}~\-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*>"
)
_WS = r"[ \t\n]"
# <!-- todo-ref-ok: CommonMark 0.31.2 Raw HTML section (6.6), not a backlog item -->
# Raw HTML (I4), as CommonMark 0.31.2 section 6.6 defines it. Its whitespace is spaces, tabs and up
# to one line ending, so a run holding two line endings ends the tag; an attribute needs some.
_TAG_WS = r"[ \t]*(?:\n[ \t]*)?"
# An unquoted attribute value excludes only spaces, tabs, line endings and "'=<>`; any other
# character, an ASCII control included, is part of it. NUL is read as U+FFFD before parsing, so
# none reaches the pattern.
_UNQUOTED = r"[^ \t\n\r\"'=<>`]+"
_ATTRIBUTE = (
    rf"(?=[ \t\n]){_TAG_WS}[A-Za-z_:][A-Za-z0-9_.:-]*"
    rf"(?:{_TAG_WS}={_TAG_WS}(?:{_UNQUOTED}|'[^']*'|\"[^\"]*\"))?"
)
RAW_TAG = re.compile(
    rf"<[A-Za-z][A-Za-z0-9-]*(?:{_ATTRIBUTE})*{_TAG_WS}/?>"   # open tag
    rf"|</[A-Za-z][A-Za-z0-9-]*{_TAG_WS}>"                    # closing tag
)
# The other raw HTML (I4) runs from its opener to the first terminator after it: a comment
# (CommonMark 0.31, after the two short forms), a processing instruction and a CDATA section, then
# a declaration (``<!`` and an ASCII letter, to the first ``>``).
RAW_HTML_SHORT = ("<!-->", "<!--->")
RAW_HTML_SPANS = (("<!--", "-->"), ("<?", "?>"), ("<![CDATA[", "]]>"))
LINK_TAIL = re.compile(
    rf"\({_WS}*(?:{_DESTINATION_ANGLE}|(?!<){_DESTINATION_BARE}*)"
    rf"(?:{_WS}+{_TITLE})?{_WS}*\)",
    re.S,
)


def expand_indent(line: str) -> str:
    """``line`` with the tabs in its leading whitespace expanded to tab stops of 4."""
    col = 0
    for i, ch in enumerate(line):
        if ch == " ":
            col += 1
        elif ch == "\t":
            col += TAB_STOP - col % TAB_STOP
        else:
            return " " * col + line[i:]
    return " " * col


def is_blank(line: str) -> bool:
    """A CommonMark blank line: nothing but spaces and tabs."""
    return not line.strip(" \t")


def quote_strip(line: str, depth: int | None = None) -> tuple[int, str]:
    """``(markers, rest)``: the block-quote markers leading ``line`` (at most ``depth``)."""
    found, pos = 0, 0
    while depth is None or found < depth:
        m = QUOTE_MARKER.match(line, pos)
        if m is None:
            break
        found, pos = found + 1, m.end()
    return found, line[pos:]


def fence_run(text: str) -> tuple[str, int] | None:
    """``(char, length)`` when ``text`` is an F1 fence opener, else None."""
    m = FENCE_RUN.match(expand_indent(text))
    if m is None:
        return None
    run, info = m.group(1), m.group(2)
    if run[0] == "`" and "`" in info:
        return None
    return run[0], len(run)


def container_content(container: tuple[str, int, int], line: str) -> str | None:
    """``line``'s content inside ``container``, or None when the line ends it (F4).

    A container is ``("list", W, 0)``, an item with content column W, or ``("quote", depth,
    base)``, a quote of that depth whose first marker is read at column ``base``: 0 at the top
    level, else the content column of the list item the quote is inside, which the line must
    stay inside (indented at least ``base``) before its markers are read.
    """
    kind, size, base = container
    text = expand_indent(line)
    indent = len(text) - len(text.lstrip(" "))
    if kind == "quote":
        if indent < base:
            return None
        depth, rest = quote_strip(text[base:], size)
        return rest if depth == size else None
    if is_blank(text):
        return ""
    if indent < size:
        return None
    return text[size:]


def list_item(body: str, col: int) -> tuple[int, bool] | None:
    """``(W, interrupts)`` when ``body`` holds a list marker 0 to 3 columns past ``col``.

    W is the item's content column: the marker plus a gap of 1 to 4 spaces, or plus one
    column when the item is empty or its gap is wider (CommonMark: the content then opens
    with indented code). ``interrupts`` is whether the marker may interrupt a paragraph: a
    bullet or the number 1, with content after it.
    """
    m = LIST_MARKER.match(body, col)
    if m is None:
        return None
    after = body[m.end():]
    if is_blank(after):
        return m.end() + 1, False
    gap = len(after) - len(after.lstrip(" "))
    width = gap if 1 <= gap <= 4 else 1
    return m.end() + width, m.group(1) is None or int(m.group(1)) == 1


def open_items(body: str, col: int, inside: bool) -> list[int] | None:
    """The content columns of the list items whose markers start ``body`` at ``col`` (L1), or None.

    A marker that may not interrupt the paragraph the line is ``inside`` (an ordered marker
    other than 1, or an empty item) opens nothing: CommonMark keeps that line paragraph
    text (I1, F2). An item's first line may open a nested item.
    """
    first = list_item(body, col)
    if first is None or (inside and not first[1]):
        return None
    columns = [first[0]]
    while not THEMATIC_BREAK.match(body, columns[-1]):
        nested = list_item(body, columns[-1])
        if nested is None:
            break
        columns.append(nested[0])
    return columns


def table_cells(text: str, lazy: bool = False) -> int:
    """The number of cells in a GFM table line as cmark-gfm's row_from_string counts them, or 0
    when the line is no row (I1).

    The grammar is ``delim? table_cell (delim table_cell)* delim? newline``: a leading pipe is
    an optional border, a cell with text counts, and an empty cell counts only before a pipe, so
    whatever follows the last pipe is a cell only when it holds more than spacechar (``SPACECHAR``,
    ``row_cells``). A lone pipe (only spacechar after it) is the border and nothing else: no
    cell, so row_from_string returns NULL (``n_columns == 0``) and this returns 0. ``||`` is the
    border, then an empty cell before the second pipe: one cell. A row of more than
    MAX_TABLE_CELLS cells is NULL too (append_row_cell's overflow abort), so it is 0. A line from
    ``commonmark_lines`` holds no CR or LF, so the scan always reaches the line end and
    ``offset != len`` cannot arise here (the bare-CR residual).
    ``lazy`` keeps the line's leading whitespace (``row_cells``).
    """
    cells = row_cells(text, lazy)
    return cells if cells <= MAX_TABLE_CELLS else 0


def row_cells(text: str, lazy: bool = False) -> int:
    """The number of cells row_from_string's grammar finds in a line, uncapped (``table_cells``).

    cmark-gfm stores a paragraph line from its first non-space character, except a lazy
    continuation line, which keeps the whitespace left after the container prefixes it matched
    (src/blocks.c 1375 to 1378 against 1429 to 1443, I1). ``lazy`` is that case: the leading
    whitespace is then a cell (extensions/ext_scanners.re 35, ``table_cell``) when a pipe follows
    it, since only a pipe at the line's start is a border (69, ``[|] spacechar*``).

    A pipe takes the SPACECHAR run after it (69 again; spacechar is space, tab, VT and FF, line
    30), so text after the last pipe that holds only spacechar is no cell: ``| a |`` then a VT is
    one cell, and ``|`` then an FF none. A cell (``table_cell``) takes every character but a pipe,
    CR and LF, so a VT or FF elsewhere is a cell character, and a line that is not lazy is stored
    from its first character that is not a space or tab, so a VT or FF at its start is a cell's
    text (3b696 round 20).
    """
    text = text.rstrip(" \t") if lazy else text.strip(" \t")
    cells = TABLE_PIPE.split(text)
    piped = len(cells) > 1
    if text.startswith("|"):
        cells = cells[1:]  # the optional leading border
    if cells and not (cells[-1].strip(SPACECHAR) if piped else cells[-1]):
        cells = cells[:-1]  # only spacechar after the last pipe (or an empty line): no cell
    return len(cells)


def row_overflows(text: str, lazy: bool = False) -> bool:
    """Whether a paragraph line holds more than MAX_TABLE_CELLS cells, so that row_from_string,
    which walks every line of the paragraph above a delimiter row, aborts on it (I1). ``lazy``
    keeps the line's leading whitespace (``row_cells``)."""
    # Each cell past the first needs a pipe, so a line with fewer pipes cannot overflow.
    return text.count("|") >= MAX_TABLE_CELLS and row_cells(text, lazy) > MAX_TABLE_CELLS


def delimiter_cells(lines: list[str], i: int, depth: int, col: int = 0,
                    base: int = 0) -> int | None:
    """The number of cells in the delimiter row below line ``i`` in a container of quote depth
    ``depth``, or None when there is none: the next line, in that container (indented at least
    ``base``, where the quote markers are read (Q1), with ``depth`` markers there, then indented
    at least ``col``, the content column of the list item the table is in), is a delimiter row 0
    to 3 columns past ``col``. A row shaped as a list item (``- | -``) is that item, not a
    delimiter row, and a run of ``-`` alone is a setext underline."""
    if i + 1 >= len(lines):
        return None
    text = expand_indent(lines[i + 1])
    if text[:base].strip(" "):
        return None
    row_depth, row = quote_strip(text[base:])
    row = expand_indent(row)
    if (row_depth == depth and not row[:col].strip(" ")
            and TABLE_DELIMITER.match(row, col) is not None and LIST_MARKER.match(row, col) is None
            and SETEXT_UNDERLINE.match(row, col) is None):
        # A delimiter row row_from_string rejects (more than MAX_TABLE_CELLS cells) is none:
        # try_opening_table_header returns before it marks the paragraph visited.
        return table_cells(row) or None
    return None


def table_header(lines: list[str], i: int, depth: int, body: str, col: int = 0,
                 base: int = 0) -> bool:
    """Whether line ``i`` (content ``body``) heads a GFM table in a container of quote depth
    ``depth``: the next line is a delimiter row there (``delimiter_cells``) with as many cells.
    Neither line needs a pipe, so ``a`` over ``:---:`` is one cell over one (cmark-gfm's row
    grammar)."""
    return delimiter_cells(lines, i, depth, col, base) == table_cells(body)


def block_scan(lines: list[str]) -> tuple[list[bool], list[int], list[list[int]], list[str]]:
    """``(code, unclosed, units, kinds)`` for one file's ``lines`` (F1 to F4, U1, L1, I1).

    ``code[i]`` is True for a fence line or fenced content; ``unclosed`` holds the index of a
    fence opener still open at the end (U1); ``units`` groups the indices of the other
    non-blank lines into inline units, and ``kinds`` names each unit's kind: "para", "inserted"
    (the lines of a paragraph above its table header line, I6), "code" (indented code, I6) or
    "block" (a line that is a unit alone).
    """
    code = [False] * len(lines)
    units: list[list[int]] = []
    kinds: list[str] = []
    unit: list[int] = []
    # The open unit: "para" or "code", its quote depth, the column its quote markers are read at
    # (the content column of the list item a quote is inside, else 0), its own column, and
    # whether a setext underline below its definitions has joined it as text (I1, I6), after
    # which it is never definitions alone.
    kind, unit_depth, unit_base, unit_col, underline_text = "para", 0, 0, 0, False
    # Whether a delimiter row in the open paragraph's container has followed a line of another
    # number of cells, after which no table opens in that paragraph (I1, the table-visited flag).
    visited = False
    # Whether a line of the open paragraph holds more than MAX_TABLE_CELLS cells: cmark-gfm's
    # row_from_string reads the whole paragraph, so that line rejects any header below it (I1).
    overflow = False
    items: list[int] = []  # content columns of the open list items (L1, outside any quote)
    empty_item = False  # the last line opened an item with nothing after its marker (L1)
    table = None  # (quote depth, item column) of the open GFM table: a row must be in its container
    # The open table's columns, rows and parsed cells, as extensions/table.c's node_table counts
    # them (n_columns, n_rows, n_nonempty_cells): columns times rows less the parsed cells is
    # get_n_autocompleted_cells, and past MAX_AUTOCOMPLETED_CELLS no further row opens (I1).
    fill = [0, 0, 0]
    fence = None  # (char, length, container, opener index)

    def close() -> None:
        nonlocal unit
        if unit:
            units.append(unit)
            kinds.append(kind)
        unit = []

    def alone(i: int) -> None:
        close()
        units.append([i])
        kinds.append("block")

    def defined_only() -> bool:
        """Whether the open unit is link reference definitions alone (I1, I6)."""
        text = unit_text([lines[j] for j in unit])[1]
        return definitions(text)[0] == len(text)

    for i, line in enumerate(lines):
        text = expand_indent(line)
        if fence is not None:
            char, length, container, _ = fence
            content = line if container is None else container_content(container, line)
            if content is not None:
                code[i] = True
                m = FENCE_CLOSER.match(expand_indent(content))
                if m and m.group(1)[0] == char and len(m.group(1)) >= length:
                    fence = None
                continue
            fence = None  # F4: the line ends the container and its fence; read it afresh
        margin = len(text) - len(text.lstrip(" "))
        kept = [w for w in items if w <= margin]  # L1: the items this line is inside
        # Q1: quote markers are read at the content column of the innermost item the line is in.
        base = kept[-1] if kept else 0
        depth, body = quote_strip(text[base:])
        stay, fresh = kept, False  # the items open after the line; whether it must start a unit
        if depth:
            body, col = expand_indent(body), 0
        else:
            body, col = text, base
            if not is_blank(body):
                para = bool(unit) and kind == "para"
                lead = open_items(body, col, para and unit_depth == 0 and margin >= unit_col)
                quoted = quote_strip(body[lead[-1]:]) if lead else (0, "")
                if quoted[0]:  # Q1: a quote opened on a list-marker line, inside the new item
                    depth, base, body, col = quoted[0], lead[-1], expand_indent(quoted[1]), 0
                    stay, fresh = kept + lead, True
        if is_blank(body):
            close()
            table = None
            if depth:
                items = stay
            elif empty_item:
                items = items[:-1]  # L1: an item can begin with at most one blank line
            empty_item = False
            continue
        empty_item = False
        indent = len(body) - len(body.lstrip(" "))
        para = bool(unit) and kind == "para" and not fresh
        # I1: the line is in the open paragraph's own container (not a lazy continuation).
        inside = para and depth == unit_depth and (base == unit_base if depth else indent >= unit_col)
        if inside and not underline_text and SETEXT_UNDERLINE.match(body, col) and defined_only():
            # I1, I6: definitions alone leave no paragraph text to underline, so the underline is
            # paragraph text (CommonMark 0.31.2 examples 213 and 216), and so is every later line.
            # A "---" that is also a thematic break is no exception: cmark-gfm's src/blocks.c
            # tries the setext branch first, so the thematic-break branch never sees the line.
            # The underline is then the paragraph's only text, so it can head a table.
            cells = delimiter_cells(lines, i, unit_depth, 0 if unit_depth else unit_col,
                                    unit_base if unit_depth else 0)
            if not visited and cells == table_cells(body):
                alone(i)  # the definitions above keep kind "para": the setext branch resolved them
                items = stay
                table = (unit_depth, unit_base) if unit_depth else (0, unit_col)
                fill = [cells, 1, cells]
                continue
            unit.append(i)
            underline_text, visited = True, visited or cells is not None
            # The setext branch dropped the definitions from the paragraph's content
            # (resolve_reference_link_definitions), so no line above the underline is read.
            overflow = False
            continue
        if THEMATIC_BREAK.match(body, col) or (inside and SETEXT_UNDERLINE.match(body, col)):
            alone(i)
            items, table = stay, None
            continue
        opened = open_items(body, col, inside)
        head = opened[-1] if opened else col
        run = fence_run(body[head:]) if depth == 0 else fence_run(body)
        if run is not None:  # F1, F2
            close()
            code[i] = True
            if depth:
                container = ("quote", depth, base)
            else:
                container = ("list", head, 0) if head else None
            fence = (*run, container, i)
            items, table = stay + (opened or []) if depth == 0 else stay, None
            continue
        if opened is not None or ATX_HEADING.match(body, head):
            close()
            items, table = stay + (opened or []) if depth == 0 else stay, None
            rest = body[head:]
            if ATX_HEADING.match(body, head) or THEMATIC_BREAK.match(body, head) or is_blank(rest):
                alone(i)
                empty_item = depth == 0 and is_blank(rest)
                continue
            kind = "code" if len(rest) - len(rest.lstrip(" ")) >= 4 else "para"
            cells = (delimiter_cells(lines, i, 0, head) if opened and depth == 0 and kind == "para"
                     else None)
            if cells is not None and cells == table_cells(rest):
                alone(i)  # I1: the marker line heads a table inside its new item
                table = (0, head)
                fill = [cells, 1, cells]
                continue
            unit_depth, unit_base, unit_col, unit, underline_text = depth, base, head, [i], False
            visited, overflow = cells is not None, row_overflows(rest)
            continue
        if table is not None and table != (depth, base):
            table = None  # the line is outside the table's quote or list item
        if table is not None and indent - col >= 4:
            table = None  # indented code, another block, ends the table (cmark-gfm opens no row)
        if table is not None and not table_cells(body):
            # I1: extensions/table.c matches() continues a table only on a line row_from_string
            # parses to a row with columns, so a line that is no row (a lone pipe) ends the table
            # and starts a new block.
            table = None
        if table is not None and fill[0] * fill[1] - fill[2] > MAX_AUTOCOMPLETED_CELLS:
            # I1: extensions/table.c try_opening_table_row refuses a row once the table has
            # autocompleted more than MAX_AUTOCOMPLETED_CELLS cells (lines 438 to 440), so the line
            # is no row: src/blocks.c creates a paragraph for it (1437 to 1443), and add_child
            # finalizes the table, which cannot hold one (394 to 402).
            table = None
        joins = para and depth <= unit_depth and (depth == 0 or base == unit_base)
        # I1: a lazy continuation line keeps the whitespace left after the container prefixes it
        # matched (src/blocks.c 1375 to 1378 call add_line at parser->offset), where any other
        # paragraph line is stored from its first non-space character (1434 to 1436, 1441 to
        # 1443), so row_from_string counts that whitespace as a cell before a pipe (row_cells).
        lazy = joins and not inside
        row = body[col:]
        # I1: a line that continues the open paragraph, lazily or not, heads a table in that
        # paragraph's container, so only over a delimiter row there; a delimiter row outside it
        # is a lazy line and joins the paragraph. Its own indent does not matter (cmark-gfm stores
        # a continuation line without it and checks only the delimiter row's), except that a lazy
        # line keeps the whitespace after its matched container prefixes (``lazy``, above).
        held_depth, held_base, held_col = ((unit_depth, unit_base, unit_col) if joins
                                           else (depth, base, col))
        # I1: cmark-gfm's extensions/table.c marks a paragraph visited when a delimiter row in its
        # container follows a line of another number of cells, and opens no table in it after.
        cells = (delimiter_cells(lines, i, held_depth, 0 if held_depth else held_col,
                                 held_base if held_depth else 0)
                 if table is None and (joins or indent - col <= 3) and not (joins and visited)
                 else None)
        # I1: a header line that continues the paragraph is read with every line above it, so a
        # line there with more than MAX_TABLE_CELLS cells makes the header NULL (and the
        # paragraph visited, below), as one of another number of cells does.
        if table is not None or (cells is not None and cells == table_cells(row, lazy)
                                 and not (joins and overflow)):
            if table is not None:
                # A body row: try_opening_table_row counts its parsed cells, up to the table's
                # columns, and the rest are autocompleted (extensions/table.c 459 to 472).
                fill[1] += 1
                fill[2] += min(table_cells(body), fill[0])
            else:
                fill = [cells, 1, cells]  # the header row (376, 405 to 417)
            if joins and not underline_text:
                kind = "inserted"  # I6: the lines above the header, a paragraph never finalized
            alone(i)
            items = items if lazy else stay  # a lazy header leaves the items open
            table = table or ((held_depth, held_base) if held_depth else (0, held_col))
            continue
        if joins:
            unit.append(i)  # paragraph continuation, lazy or not; the open items stay open
            visited = visited or cells is not None
            overflow = overflow or row_overflows(row, lazy)
            continue
        if (unit and not fresh and kind == "code" and depth == unit_depth
                and (depth == 0 or base == unit_base) and indent - unit_col >= 4):
            unit.append(i)
            continue
        close()
        items = stay
        kind = "code" if indent - col >= 4 else "para"
        unit_depth, unit_base, unit_col, unit, underline_text = depth, base, col, [i], False
        visited, overflow = cells is not None, row_overflows(body)
    close()
    return code, [] if fence is None else [fence[3]], units, kinds


LABEL_SPACE = " \t\r\n"  # the whitespace a link label is normalised on (I5): not NBSP or the like
_LABEL_SPACE_RUN = re.compile(r"[ \t\r\n]+")


def label_valid(label: str) -> bool:
    """Whether ``label`` (the text inside a link label's brackets) is a CommonMark link label:
    at most 999 characters as written, at least one of them not a space, tab or line ending."""
    return len(label) <= LABEL_MAX and bool(label.strip(LABEL_SPACE))


def normalize_label(label: str) -> str:
    """A link label as CommonMark matches it: its spaces, tabs and line endings stripped at the
    ends and collapsed to one space inside (no other whitespace), then case-folded."""
    return _LABEL_SPACE_RUN.sub(" ", label.strip(LABEL_SPACE)).casefold()


def unit_text(lines: list[str]) -> tuple[list[str], str]:
    """``(prefixes, text)`` for one inline unit: each line's leading whitespace and block-quote
    markers, and the lines without them joined by LF (CommonMark strips container markers, and a
    paragraph line's leading whitespace, before inline parsing). The markers of a quote inside a
    list item follow the item's indent."""
    prefixes, contents = [], []
    for line in lines:
        rest = quote_strip(line.lstrip(" \t"))[1]
        prefixes.append(line[:len(line) - len(rest)])
        contents.append(rest)
    return prefixes, "\n".join(contents)


def definitions(text: str) -> tuple[int, list[str]]:
    """``(end, labels)``: where the link reference definitions leading one unit's text end, and
    their normalised labels (I6)."""
    pos, labels = 0, []
    while True:
        m = DEFINITION.match(text, pos)
        if m is None or not label_valid(m.group(1)):
            return pos, labels
        labels.append(normalize_label(m.group(1)))
        pos = min(m.end() + 1, len(text))


def raw_html_end(text: str, i: int, last: dict[str, int]) -> int | None:
    """Where the raw HTML (I4) opened at ``text[i]`` (a ``<``) ends, or None when there is none.

    ``last`` maps each terminator in RAW_HTML_SPANS, and ``>``, to its last position in ``text``,
    so an opener with no terminator after it fails at once instead of rescanning the rest of the
    unit, and a scan of repeated unclosed openers stays linear (claude N2).
    """
    if text.startswith(RAW_HTML_SHORT, i):
        return i + len(next(s for s in RAW_HTML_SHORT if text.startswith(s, i)))
    for opener, closer in RAW_HTML_SPANS:
        if text.startswith(opener, i):
            start = i + len(opener)
            return text.find(closer, start) + len(closer) if last[closer] >= start else None
    if text.startswith("<!", i) and text[i + 2:i + 3].isascii() and text[i + 2:i + 3].isalpha():
        return text.find(">", i + 3) + 1 if last[">"] >= i + 3 else None  # a declaration
    m = RAW_TAG.match(text, i)
    return m.end() if m else None


def link_end(text: str, start: int, i: int, labels: frozenset[str]) -> int | None:
    """Where the link or image whose text runs from the ``[`` at ``start`` to the ``]`` at ``i``
    ends, or None when none forms there (I5): an inline destination and title, or a full,
    collapsed or shortcut reference to a label the file defines. A full reference's own label
    decides; only without one does the text in the brackets name the label."""
    m = LINK_TAIL.match(text, i + 1)
    if m:
        return m.end()
    m = REFERENCE.match(text, i + 1)
    if m and label_valid(m.group(1)):
        end = m.end()  # a full reference
    else:  # a collapsed reference ("[]" follows) or a shortcut one
        m = REFERENCE.fullmatch(text, start, i + 1)
        end = i + 3 if text.startswith("[]", i + 1) else i + 1
    return end if m and label_valid(m.group(1)) and normalize_label(m.group(1)) in labels else None


def code_spans(text: str, labels: frozenset[str] = frozenset()) -> list[tuple[int, int]]:
    """``(start, end)`` of each code span in one unit's text (I2 to I5, I7)."""
    spans: list[tuple[int, int]] = []
    runs: dict[int, list[int]] = defaultdict(list)  # run length -> start of each maximal run
    for m in BACKTICKS.finditer(text):
        runs[m.end() - m.start()].append(m.start())
    last = {t: text.rfind(t) for t in (*(closer for _, closer in RAW_HTML_SPANS), ">")}
    openers: list[tuple[int, bool]] = []  # each unmatched "[" or "![": its "[", whether an image
    inactive = 0  # the "[" openers below this depth are inactive: a link formed after them (I5)
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n and text[i + 1] in ESCAPABLE:
            i += 2
            continue
        if ch == "<":
            m = AUTOLINK.match(text, i)
            end = m.end() if m else raw_html_end(text, i, last)
            if end is not None:
                i = end
                continue
        elif ch == "!" and text.startswith("[", i + 1):
            openers.append((i + 1, True))
            i += 2
            continue
        elif ch == "[":
            openers.append((i, False))
        elif ch == "]" and openers:
            start, image = openers.pop()
            depth = len(openers)
            live, inactive = image or depth >= inactive, min(inactive, depth)
            end = link_end(text, start, i, labels) if live else None
            if end is not None:
                if not image:
                    inactive = depth  # a link holds no link, at any level of nesting
                i = end
                continue
        elif ch == "`":
            run = BACKTICKS.match(text, i).end() - i
            starts = runs.get(run, [])
            k = bisect.bisect_left(starts, i + run)  # the next maximal run of exactly this length
            if k < len(starts):
                spans.append((i, starts[k] + run))
                i = starts[k] + run
            else:
                i += run
            continue
        i += 1
    return spans


def inline_residues(lines: list[str], labels: frozenset[str] = frozenset(),
                    kind: str = "para") -> list[str]:
    """Each line of one inline unit with its code-span characters removed (I2 to I8).

    Each line's block-quote markers are set aside before the unit is read and kept in its
    residue. Leading link reference definitions are opaque and returned whole (I6) in a unit of
    ``kind`` "para" or "code"; in an "inserted" or "block" unit (a table header or row
    included) they are text; ``labels`` are the normalised labels the file defines, for full
    references (I5).
    """
    prefixes, text = unit_text(lines)
    start = definitions(text)[0] if kind in ("para", "code") else 0
    masked = bytearray(len(text))
    for a, b in code_spans(text[start:], labels):
        masked[start + a:start + b] = b"\x01" * (b - a)
    residues: list[str] = []
    pos = 0
    for prefix, line in zip(prefixes, lines):
        content = line[len(prefix):]
        kept = masked[pos:pos + len(content)]
        residues.append(prefix + "".join(ch for ch, m in zip(content, kept) if not m))
        pos += len(content) + 1
    return residues


def scan_lines(lines: list[str]) -> list[tuple[int, str, str]]:
    """``(lineno, tag, snippet)`` for each unclosed fence and prose em/en-dash line in one file's
    ``lines``; one leading U+FEFF on the first line is dropped, and each NUL is read as U+FFFD."""
    lines = [line.replace("\x00", "�") for line in lines]  # CommonMark 0.31.2 section 2.3
    if lines and lines[0].startswith("﻿"):
        lines[0] = lines[0][1:]
    _, unclosed, units, kinds = block_scan(lines)
    unit_lines = [[lines[i] for i in unit] for unit in units]
    # I6: only a paragraph defines a label: not indented code (CommonMark 0.31.2 example 211), and
    # not a line alone, a table header or row included (3b696 round 9), and not the lines above a
    # table header in its paragraph (round 10).
    labels = frozenset(label for group, kind in zip(unit_lines, kinds) if kind == "para"
                       for label in definitions(unit_text(group)[1])[1])
    findings = [(i + 1, "unclosed-fence", lines[i].strip()) for i in unclosed]
    for unit, group, kind in zip(units, unit_lines, kinds):
        for i, residue in zip(unit, inline_residues(group, labels, kind)):
            if EM_DASH_PATTERN.search(residue):
                findings.append((i + 1, "prose-dash", lines[i].strip()))
    return sorted(findings)


LINE_ENDING = re.compile(r"\r\n|\r|\n")


def commonmark_lines(text: str) -> list[str]:
    """``text`` split into CommonMark lines (0.31.2 section 2.1): a line ending is LF, a CR not
    followed by LF, or CRLF, and nothing else, so VT, FF, FS to RS, U+0085, U+2028 and U+2029
    stay inside their line (3b696 round 19). As with ``str.splitlines()``, a final line ending
    adds no empty line and an empty text has no lines."""
    lines = LINE_ENDING.split(text)
    if lines[-1] == "":
        lines.pop()
    return lines


def scan_text(text: str) -> list[tuple[int, str, str]]:
    """``(lineno, tag, snippet)`` for each unclosed fence and prose em/en-dash line in ``text``."""
    return scan_lines(commonmark_lines(text))


def check_file(path: Path) -> list[tuple[int, str, str]]:
    """Return ``(lineno, tag, snippet)`` for each finding in ``path`` (see ``scan_text``)."""
    text = read_text_safe(path)
    if text is None:
        return []
    return scan_text(text)


def main(argv: list[str]) -> int:
    paths = positional_args(argv[1:], known_flags=())  # 3b50b2c: '--' separates paths (quick-guard passes one)
    if paths:
        # 3b48: explicit paths are refused when missing, else normalized; the default
        # target is the operational store OUTSIDE this tree by design, so outside paths
        # stay allowed.
        paths = guard_explicit_paths_cwd(paths, repo_root=REPO_ROOT, allow_outside=True)
    if not paths:
        scan_root = default_scan_root()
        if scan_root is None:
            # The `.working/` tree is maintainer-only working state. Once it
            # moves to the operational store it is absent in public CI and adopter
            # clones, so this gate no-ops there; on the maintainer's machine the
            # operational store (or the private-sibling fallback) supplies it and the #353 em-dash conformance stays
            # ratcheted. Said explicitly rather than left to iter_markdown_targets,
            # which returns [] for a nonexistent path and would print a clean
            # result for a scan that never happened.
            print(
                "OK: the .working/ tree is not present (maintainer-only working "
                "state; skipping the prose-hygiene audit in public CI / adopter "
                "clone)."
            )
            print_degraded(
                "gate 51",
                "gate 51 skipped the .working/ prose em/en-dash scan (no private "
                "store supplies the tree); this pass attests nothing about it."
            )
            return 0
        paths = [str(scan_root)]

    files = iter_markdown_targets(
        paths, exempt_dirs=EXEMPT_DIRS, exclude_default_roots=False,
    )

    grouped: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    total = unclosed = 0
    for f in files:
        for lineno, tag, snippet in check_file(f):
            grouped[display_path(f)].append((lineno, tag, snippet))
            if tag == "unclosed-fence":
                unclosed += 1
            else:
                total += 1

    if not grouped:
        print(f"OK: no prose em/en-dashes in {len(files)} .working/ file(s).")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, tag, snippet in grouped[relpath]:
            print(f"  L{lineno} [{tag}] {snippet[:160]}")

    fences = f", {unclosed} unclosed fence(s)" if unclosed else ""
    print(f"\nFAIL: {total} prose em/en-dash finding(s) across {len(grouped)} file(s){fences}.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
