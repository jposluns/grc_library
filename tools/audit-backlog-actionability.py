#!/usr/bin/env python3
"""Backlog actionability enumeration across BOTH backlog lists, so a "queue
exhausted / all blocked / hold" claim cannot be made without confronting every
open item on either list (anti-false-completeness layer 1).

WHY THIS EXISTS. A completeness claim ("everything left is blocked, so I am
stopping") was made from a PARTIAL review and was wrong: actionable items
remained. Nothing mechanical forced the claimant to confront EVERY backlog item
first. This tool does: it enumerates every open item in the PUBLIC ``TODO.md``
AND the PRIVATE ``grc_library_private/P-TODO.md`` and, per item, reports whether
it is BLOCKED.

THE AUTHORITATIVE BLOCKER SIGNAL IS THE TAG, NOT PROSE. An item is counted
BLOCKED only if it carries a ``[BLOCKED:<reason>]`` tag AND the operational
store's approvals register (``blocked-approvals.md``) holds a granted row for it,
citing the maintainer's ruling (P-1.36 S36), in every mode including --pipeline. On a
clone with no operational store at all (an adopter), tags count as written; a store
without a readable register counts no tag. The tag is a maintainer-GRANTED
status: the assistant proposes a block in ``pending-decisions.md`` and only an
approved block becomes a tag and a register row; a tag with no row is reported as
UNAPPROVED and counted ACTIONABLE (a hook that rejects writing such a tag is still
a queued backstop). So "all blocked" is assertable only when EVERY
open item on BOTH lists literally carries an approved ``[BLOCKED:...]`` tag,
which is essentially never. Until the maintainer approves blocks, every item
reads ACTIONABLE, which is the honest state.

PROSE SIGNAL IS ADVISORY ONLY. The closed keyword set below (``egress-gated``,
``DEFERRED``, ``maintainer-decision`` ...) no longer decides blocked-vs-actionable;
it is surfaced as an ADVISORY "this item's prose mentions a blocker; propose a
``[BLOCKED]`` tag for it?" hint. An item with a prose signal but no approved tag
is still ACTIONABLE (the safe direction: it forces a disposition, it does not
hide a blocker behind an unapproved self-assessment).

It is ADVISORY, NOT a gate: it always exits 0, is not wired into
``quality.yml`` / ``run_all_audits.sh`` / ``.pre-commit-config.yaml``, and is
portable-clone-tolerant (a missing list is a no-op for that list; an adopter with
no private sibling simply audits the public list). Regression coverage:
``BacklogActionabilityTests`` in ``tests/test_linters.py``.

USAGE
  python3 tools/audit-backlog-actionability.py
      Enumerate every open item on both lists; print the full table, the summary
      counts, and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --actionable-only
      Print only the summary and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --todo PATH --ptodo PATH
      Override either list path (testing / non-default layout).
  python3 tools/audit-backlog-actionability.py --pipeline
      Render the pipeline view: recent completions (read from DONE.md, a third
      data source alongside the two backlog lists) next to the open queue.
      Add --umbrella to group the queue by umbrella.
  python3 tools/audit-backlog-actionability.py --self-test
      Run the built-in self-test.

Stdlib-only (gate 71). Python 3.11.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import unicodedata
import sys
from pathlib import Path

# Ensure the tools dir is importable whether run standalone or loaded via importlib
# (the regression suite loads this module with spec_from_file_location).
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from lint_common import resolve_working, has_todo_index_header, _store_dir, InaccessiblePath

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_PATH = REPO_ROOT / "TODO.md"
# The private backlog lives in the maintainer's private sibling; adopters have no
# such sibling and simply audit the public list (resolve_sibling no-op).
PTODO_PATH = REPO_ROOT.parent / "grc_library_private" / "P-TODO.md"
# DONE.md moved to the operational store; resolve it via lint_common.resolve_working
# (store-preferred, private-sibling fallback), matching gate 78 (lint-todo-number-permanence).

# An open backlog item heading: ``### <id> <title>`` where <id> is a section
# number (``N.M`` / ``N.M.K``, optional trailing letter), a private ``P-n.m`` id,
# or a coded id (``SR-1`` / ``RB-R6`` / ``GR-GAP-1``). ``## `` section headers are
# NOT items.
ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)

# The AUTHORITATIVE blocker signal: a ``[BLOCKED:<reason>]`` tag (maintainer-granted).
BLOCKED_TAG_RE = re.compile(r"\[BLOCKED:[^\]]*\]")

# A [BLOCKED:] tag is maintainer-GRANTED, never assistant-asserted (P-1.36 S36). The grant is recorded as a
# row of the approvals register in the operational store: ``| <item id> | <reason> | <date> | <evidence> |``,
# where the evidence cell cites the ruling (a pending-decisions entry, a commit or a PR). A tag counts as
# BLOCKED only when its item has a row. None = no store on a git clone whose origin is another repository: tags count
# as written. When a store exists but the register does not, NO tag counts: a missing register must not
# widen what is blocked, since BLOCKED licenses less work (the asymmetric-skepticism rule).
APPROVALS_FILE = "blocked-approvals.md"
_APPROVALS: "set[str] | None" = None


_APPROVAL_HEADER = "| Item | Reason | Granted | Evidence |"
_APPROVAL_SEPARATOR_RE = re.compile(r"\|(?:[ \t]*:?-+:?[ \t]*\|){4}")
_APPROVAL_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_APPROVAL_ITEM_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9.\-]*[A-Za-z0-9])?")
# Characters Python's splitlines treats as line breaks but Markdown does not (QA r5).
_NON_MARKDOWN_BREAKS = "\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029"
_FENCE_LINE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
# A line allowed before the header: a heading, or a prose line that cannot open a list, blockquote, code
# block, setext underline, thematic break or table (QA r6: lazy continuation and pipe-less tables).
_PRE_HEADER_HEADING_RE = re.compile(r"#{1,6}(?:[ \t][^|]*)?")
_PRE_HEADER_PROSE_RE = re.compile(r"(?![-+>=_#~\s])(?![*](?:[ \t]|$))(?!\d{1,9}[.)](?:[ \t]|$))[^|]*")


_CELL_FORBIDDEN = set("`&[]<>\\~")
_SHORTCODE_RE = re.compile(r":[A-Za-z0-9_+\-]+:")


def _cell_problem(cell: str, needs_text: bool) -> "str | None":
    """Why a cell cannot grant, or None (QA r7-r8). A cell is a whitelist: printable ASCII and tab only, without
    a backtick (a code span can swallow pipes), ``&`` (an entity such as ``&nbsp;`` renders as blank),
    brackets (an empty link or image renders as blank), angle brackets, a backslash, ``~`` (strikethrough
    reads as withdrawn) or an emoji shortcode such as ``:x:``. A reason or evidence
    cell must also contain a letter or digit, so it cannot look blank to a reader."""
    bad = sorted({c for c in cell if c in _CELL_FORBIDDEN or not (c == "\t" or " " <= c <= "~")})
    if bad:
        return "a character outside the cell whitelist: " + ", ".join(repr(c) for c in bad)
    if _SHORTCODE_RE.search(cell):
        return "an emoji shortcode, which renders as a symbol"
    if needs_text and not any(c.isalnum() for c in cell):
        return "no letter or digit"
    return None


def _register_lines(text: str) -> "tuple[list[str], str | None]":
    """The register's lines and why it is refused, or None (QA r5-r6). The grammar is CLOSED: rather than track
    every Markdown construct that can hide or reveal a table, a register that contains any of them grants
    nothing, and the tool says why. One leading BOM is dropped and CRLF becomes LF; the same line list serves
    the refusal and the parse. Refused: another BOM, a lone CR, a non-Markdown line-break character, any ``<``
    (HTML, comments, autolinks), an escaped pipe, a code-fence line, and before the exact header line anything
    but blank lines (spaces and tabs only), headings and plain prose lines without a ``|`` (so no table, list, blockquote, indented or
    lazy-continuation context can contain the header); the header must follow a blank line or open the file."""
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    if "\ufeff" in text:
        return lines, "it contains a byte-order mark after the start"
    if "\r" in text:
        return lines, "it contains a carriage return that is not part of CRLF"
    if any(c in text for c in _NON_MARKDOWN_BREAKS):
        return lines, "it contains a line-break character Markdown does not treat as one"
    if "<" in text:
        return lines, "it contains '<' (HTML or a comment could hide or reveal a table)"
    controls = sorted({c for c in text if unicodedata.category(c) == "Cc" and c not in "\t\n"})
    if controls:
        return lines, "it contains a control character: " + ", ".join(repr(c) for c in controls)
    if "\\|" in text:
        return lines, "it contains an escaped pipe, which shifts the cells a reader sees"
    if any(_FENCE_LINE_RE.match(line) for line in lines):
        return lines, "it contains a code fence"
    for n, line in enumerate(lines):
        if line.rstrip(" \t") == _APPROVAL_HEADER:
            if n and lines[n - 1].strip(" \t"):
                return lines, "the header line does not follow a blank line"
            return lines, None
        if line.strip(" \t") and not (_PRE_HEADER_HEADING_RE.fullmatch(line) or _PRE_HEADER_PROSE_RE.fullmatch(line)):
            return lines, f"line {n + 1}, before the header, is not a heading or plain prose"
    return lines, None


def register_refusal(text: str) -> "str | None":
    """Why the register text is refused as a whole, or None (see _register_lines)."""
    return _register_lines(text)[1]


def load_approvals(text: str, today: "datetime.date | None" = None) -> "set[str]":
    """The item ids granted by the register (see parse_approvals)."""
    return parse_approvals(text, today)[0]


def parse_approvals(text: str, today: "datetime.date | None" = None) -> "tuple[set[str], list[str]]":
    """(granted item ids, one note per table row that grants nothing) for the register (QA r1-r8). A refused
    register grants nothing. Otherwise the table is opened by the first line that is exactly ``| Item | Reason |
    Granted | Evidence |`` (trailing spaces ignored) and must be followed at once by a four-cell separator row;
    it ends at the first line not starting with ``|``. A row starts at column 0, ends with ``|`` (trailing
    spaces ignored) and has exactly five ``|`` characters; it grants only with an item id (optionally
    backtick-wrapped, not ending in a dot), whitelisted cells, a reason and evidence containing a letter or
    digit, and a ``YYYY-MM-DD`` calendar date not after today. A row that grants nothing is reported, never
    silently dropped; an indented row ends the table (it grants less, never more)."""
    lines, refusal = _register_lines(text)
    if refusal is not None:
        return set(), []
    today = today or datetime.date.today()
    ids: set = set()
    skipped: list = []
    state = "before"  # before -> separator -> rows
    for n, raw in enumerate(lines, 1):
        if state == "before":
            if raw.rstrip(" \t") == _APPROVAL_HEADER:
                state = "separator"
            continue
        if state == "separator":
            if not _APPROVAL_SEPARATOR_RE.fullmatch(raw.rstrip(" \t")):
                skipped.append(f"line {n}: the header is not followed by its separator row, so no row grants")
                break
            state = "rows"
            continue
        if not raw.startswith("|"):
            # GFM continues a table through indented and pipe-less lines; they and any rows after them grant
            # nothing here, so name each one that still looks like a row (QA r9).
            skipped.extend(f"line {k}: after the table ends at line {n}, not read"
                           for k, rest in enumerate(lines[n - 1:], n) if "|" in rest)
            break
        row = raw.rstrip(" \t")
        if row.count("|") != 5 or not row.endswith("|"):
            skipped.append(f"line {n}: not exactly four cells between pipes")
            continue
        item, reason, granted, evidence = (c.strip(" \t") for c in row[1:-1].split("|"))
        if item.startswith("`") and item.endswith("`") and len(item) > 2:
            item = item[1:-1]
        problem = next((f"{name}: {why}" for name, cell, needs in (("item", item, False), ("reason", reason, True),
                                                                   ("granted", granted, False), ("evidence", evidence, True))
                        for why in [_cell_problem(cell, needs)] if why), None)
        if problem is None and not _APPROVAL_ITEM_RE.fullmatch(item):
            problem = "item: not an item id"
        if problem is None:
            try:
                when = datetime.date.fromisoformat(granted) if _APPROVAL_DATE_RE.fullmatch(granted) else None
            except ValueError:
                when = None
            if when is None:
                problem = "granted: not a YYYY-MM-DD calendar date"
            elif when > today:
                problem = "granted: after today"
        if problem is None:
            ids.add(item)
        else:
            skipped.append(f"line {n}: {problem}")
    return ids, skipped


def set_approvals(approvals: "set[str] | None") -> None:
    global _APPROVALS
    _APPROVALS = approvals


def _approved(item_id: "str | None") -> bool:
    return _APPROVALS is None or (item_id is not None and item_id in _APPROVALS)

# ADVISORY prose-signal set (closed). Detected only to SUGGEST proposing a block;
# it never counts an item blocked. Kept deliberately narrow to avoid false hints.
PROSE_SIGNAL_TOKENS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"egress[- ]gated|egress[- ]blocked", re.I), "egress"),
    (re.compile(r"source[- ]gated|source[- ]not[- ]held|pending held source"
                r"|pending maintainer source|blocked on .{0,30}ingest", re.I),
     "source"),
    (re.compile(r"maintainer[- ](decision|decided|gated|collaborative|"
                r"sign[- ]off|owned)", re.I), "maintainer-decision"),
    (re.compile(r"\bNOT automated\b|explicitly NOT automated"), "maintainer-decision"),
    (re.compile(r"\bDEFERRED\b|\bdeferred\b"), "deferred"),
    (re.compile(r"\bIN PROGRESS\b"), "in-progress"),
    (re.compile(r"fresh[- ]session|fresh[- ]context|attended[- ]preferred"
                r"|attended/fresh|fresh session", re.I), "fresh-session"),
    (re.compile(r"\(standing\)|,\s*standing\)|standing (?:tracker|watch)"
                r"|stays open by design", re.I), "standing"),
]


_REF_ID_RE = re.compile(r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)\s")
_ROW_RE = re.compile(r"^\|\s*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)\s*\|(?P<title>[^|]*)\|(?P<tags>[^|]*)\|")


_PRIVATE_DIR = REPO_ROOT.parent / "grc_library_private"


def _first_existing(*cands: Path | None) -> Path | None:
    for c in cands:
        if c is not None and c.is_file():
            return c
    return None


def _ref_file(which: str, private_dir: "Path | None" = None) -> Path | None:
    """Resolve the detail (reference) file for a backlog.

    Transitional (2026-08 migration): the public detail file (TODO-REFERENCE.md)
    is moving into the private sibling, and the private backlog gains its own
    detail file (P-TODO-REFERENCE.md). ``which='public'`` resolves private-first
    (post-move) then the legacy public location (pre-move); ``which='private'``
    resolves the private P-TODO-REFERENCE.md. Absent -> None (no-op).

    ``private_dir`` (F1793-5 / P-1.53) overrides the import-fixed ``_PRIVATE_DIR`` so a
    ``--private-root`` CLI (or fixture) run loads reference bodies from a fixture, at
    parity with the index-reference-parity gate's own ``--private-root``."""
    base = private_dir if private_dir is not None else _PRIVATE_DIR
    if which == "public":
        return _first_existing(
            base / "TODO-REFERENCE.md",
            REPO_ROOT / "TODO-REFERENCE.md",
        )
    return _first_existing(base / "P-TODO-REFERENCE.md")


def _load_ref_bodies(which: str = "public", private_dir: "Path | None" = None) -> dict[str, str]:
    """Map item id -> its reference ``### <id> <title>`` block body.

    The per-item detail lives in the reference file (TODO-REFERENCE.md for the
    public backlog, P-TODO-REFERENCE.md for the private one). This reads those
    blocks so the actionability scan can still see each item's body prose when
    the backlog is in index-row form."""
    ref = _ref_file(which, private_dir)
    if ref is None:
        return {}
    bodies: dict[str, str] = {}
    cur = None
    buf: list[str] = []
    for line in ref.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _REF_ID_RE.match(line)
        if m:
            if cur is not None:
                bodies[cur] = "\n".join(buf)
            cur = m.group("id")
            buf = [line]
        elif cur is not None:
            if line.startswith("## "):
                bodies[cur] = "\n".join(buf)
                cur = None
                buf = []
            else:
                buf.append(line)
    if cur is not None:
        bodies[cur] = "\n".join(buf)
    return bodies


def parse_items(text: str, source: str,
                ref_bodies: dict[str, str] | None = None,
                private_dir: "Path | None" = None) -> list[tuple[str, str, str, str, str]]:
    """Return ``(id, title, block_text, source, umbrella)`` for every open item. PUBLIC
    ``TODO.md`` items are parsed as INDEX ROWS (the local ``_ROW_RE``), their bodies joined
    from ``TODO-REFERENCE.md``; only private / legacy items use the ``### `` heading-block
    grammar below.

    A block runs from its item heading to the next item heading, the next ``## ``
    section header, or end of file, so a signal is detected only within the item's
    own text. ``source`` labels which list the item came from (``public`` /
    ``private``)."""
    lines = text.splitlines()
    # Both backlogs move to index form: | id | title | tags | rows under ## bands,
    # detail in the reference file. A pre-migration P-TODO.md is still ### -block.
    # UNION both parsers (F1793-3): a pure file yields exactly one shape (the other
    # parser finds nothing), while a mixed / half-converted file keeps BOTH rather
    # than silently dropping the leftover legacy items (which would disagree with
    # the gate-78 / hook union counts). gate 90's index-detail-leak check fails
    # loud on such a mixed state; this keeps the enumeration honest meanwhile.
    idx_items: list[tuple[str, str, str, str, str]] = []
    if has_todo_index_header(text):   # F1793-7: the header, not any parseable row,
        # is the reliable index-form signal (a legacy item body table must not
        # flip this branch and inject false items).
        if ref_bodies is None:
            ref_bodies = _load_ref_bodies(source, private_dir)
        band = ""
        for ln in lines:
            if ln.startswith("## "):
                band = ln[3:].strip()
                continue
            m = _ROW_RE.match(ln)
            if m:
                iid = m.group("id")
                title = m.group("title").strip()
                tags = m.group("tags").strip()
                body = ref_bodies.get(iid, "")
                block = f"{iid} {title} {tags}\n{body}"
                idx_items.append((iid, title, block, source, band))

    legacy_items: list[tuple[str, str, str, str, str]] = []
    cur: tuple[str, str] | None = None
    body_lines: list[str] = []
    umbrella = ""  # the most-recent ``## `` section header (the item's umbrella)

    def flush() -> None:
        if cur is not None:
            legacy_items.append((cur[0], cur[1].strip(), "\n".join(body_lines), source, umbrella))

    for line in lines:
        m = ITEM_HEADING_RE.match(line)
        if m:
            flush()
            cur = (m.group("id"), m.group("title"))
            body_lines = [line]
        elif line.startswith("## "):
            flush()
            cur = None
            body_lines = []
            umbrella = line[3:].strip()
        elif cur is not None:
            body_lines.append(line)
    flush()

    # F1793-9: no dedup by captured id (that key is only the numeric prefix for
    # lettered subheadings, so ### 3.92.a/.b would collide with an index row 3.92
    # and be dropped). With the header classifier, a CLEAN file is one shape (the
    # other list is empty, no overlap); a mixed/botched file is gate-90 fail-loud,
    # where listing both forms is more honest than silently dropping siblings.
    return idx_items + legacy_items


# The heading id; _heading_id checks what follows it (a heading such as ``### 1.1\u0662`` is not item 1.1
# and must not inherit its grant, QA r9 and its fix-checks).
_HEADING_ID_RE = re.compile(r"^(?:#{2,6}\s+|\|\s*)`?(?P<id>[A-Za-z0-9][A-Za-z0-9.\-]*)")
# Returned when a heading's id does not end cleanly (``### 1.1\u0662``, ``### 3.92.<ZWSP>a``): the heading
# is not the ASCII item, and it must not fall back to a shorter parsed id either (fix-check after QA r9),
# so it gets an id that no approvals row can match.
_UNREADABLE_HEADING_ID = "<unreadable heading id>"


def _heading_id(block_text: str) -> "str | None":
    """The item id exactly as the heading writes it (a ``### 3.92.a`` heading or an index row's first cell);
    parse_items may shorten a lettered child's id, and approval must bind to the full one (QA r2)."""
    line = block_text.splitlines()[0].strip() if block_text else ""
    m = _HEADING_ID_RE.match(line)
    if not m:
        return None
    nxt = line[m.end():m.end() + 1]
    # The id must end at the end of the line, a space or tab, or printable ASCII punctuation. Anything else
    # (a letter, digit or underscore; an invisible, combining, control or other non-ASCII character that
    # would hide a longer id such as 3.92.<ZWSP>a) makes the id unreadable, never a shorter grantable one.
    if nxt and not (nxt in " \t" or (nxt.isascii() and nxt.isprintable() and not (nxt.isalnum() or nxt == "_"))):
        return _UNREADABLE_HEADING_ID
    return m.group("id").rstrip(".")


def is_blocked(block_text: str, item_id: "str | None" = None) -> bool:
    """True iff the item's HEADING carries an (approved) ``[BLOCKED:...]`` tag.

    Scans ONLY the heading (first line of the block): per the design the tag lives
    on the item heading, so a ``[BLOCKED:...]`` appearing in an item's BODY prose
    (e.g. an item describing the blocked-tag feature) must NOT false-match as
    blocked, which is the unsafe direction (it would hide an actionable item)."""
    heading = block_text.splitlines()[0] if block_text else ""
    return bool(BLOCKED_TAG_RE.search(heading)) and _approved(_heading_id(block_text) or item_id)


def has_blocked_tag(block_text: str) -> bool:
    """The heading carries a [BLOCKED:] tag, approved or not."""
    heading = block_text.splitlines()[0] if block_text else ""
    return bool(BLOCKED_TAG_RE.search(heading))


def prose_signals(block_text: str) -> list[str]:
    """Sorted distinct ADVISORY prose blocker-signals (never authoritative)."""
    return sorted({cls for pat, cls in PROSE_SIGNAL_TOKENS if pat.search(block_text)})


def build_report(public_text: str,
                 private_text: str | None = None,
                 private_dir: "Path | None" = None) -> tuple[list, int, int]:
    """Return (rows, blocked_count, actionable_count). Each row is
    ``(id, title, source, blocked_bool, prose_list)``."""
    items = parse_items(public_text, "public", private_dir=private_dir)
    if private_text is not None:
        items += parse_items(private_text, "private", private_dir=private_dir)
    rows = []
    blocked = 0
    for item_id, title, block, source, _umbrella in items:
        b = is_blocked(block, item_id)
        rows.append((item_id, title, source, b, prose_signals(block)))
        if b:
            blocked += 1
    return rows, blocked, len(rows) - blocked



# ---- --pipeline mode (maintainer-directed 2026-08-06): the scannable roadmap view ----

# A bulleted SUB-ITEM under an umbrella heading: ``- **<id>** <desc>``.
BULLET_ITEM_RE = re.compile(r"^\s*[-*] \*\*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
                            r"|\d+(?:\.\d+){1,2}[a-z]?"
                            r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\*\*[ \t]*(?P<title>.*)$")

# An INLINE formal-id mention in umbrella wave-prose (NOT a ``- **id**`` bullet):
# e.g. ``_Wave 2_: **P-1.25.12** 4 more briefs; **P-1.25.13** 3 scenarios``. The description
# runs to the next ``;`` or ``**`` (P-1.30 bug b: inline wave items were omitted from the view).
INLINE_ID_RE = re.compile(
    r"\*\*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\*\*[ \t]*(?P<title>(?:[^;*]|\*(?!\*))*)")


def _is_descendant(child_id: str, parent_id: str) -> bool:
    """True if ``child_id`` is a proper dotted descendant of ``parent_id`` (e.g.
    ``P-1.25.12`` under ``P-1.25``). Umbrella children share the umbrella id prefix per
    the multi-phase-series numbering convention."""
    return child_id.startswith(parent_id + ".")

# A DONE.md entry heading. Accepts a SINGLE PR (``### PR #1425: ... (2026-08-06)``) or a
# COMPOUND heading (``### PR #1425 + #1426: ... (date)``); the ``extra`` group captures the
# ``+ #NNNN`` repeats so a compound entry is not silently skipped (P-1.30 bug a).
DONE_ENTRY_RE = re.compile(
    r"^### PR #(?P<pr>\d+)(?P<extra>(?:\s*\+\s*#\d+)*):\s*(?P<title>.*?)\s*\((?P<date>\d{4}-\d\d-\d\d)\)\s*$")

# Priority-ordered (first match wins) TYPE heuristic. Rough by design: the /pipeline
# command refines a wrong guess. Keyword -> one-word type.
_TYPE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("website", (".web", "site route", "site render", "homepage", "re-hero",
                 "role page", "role (", "maturity", "local search", "adjacency",
                 "guided discovery", "portal", "relationship view")),
    ("rule", ("pack rule", "change-tracking extension", "trust-recovery extension",
              "conformance contract", "oversight and autonomy", "discipline (")),
    ("validation", ("validat", "/fitness", "fitness", "reference-increment")),
    ("ops", ("runbook", "changelog", "roll-up", "rollup", "scale wave", "ops ")),
    ("content", ("brief", "scenario", "journey", "exemplar", "story",
                 "narrative page", "outcome map", "control journey")),
    ("gate", ("new gate", "staleness gate", "audit gate", "freshness gate")),  # specific gate phrases
    ("tool", ("lint", "scanner", "guard", ".py", "hook", "tool", "generator")),
    ("gate", ("gate ",)),   # P-1.30 bug d + QA finding 6: generic "gate N" fallback AFTER the tool
                            # rule, so a tool item that also mentions "gate" (e.g. "add gate-count
                            # consistency linter", "... evidence gates ...") stays tool; a pure
                            # "gate 87" item (no tool indicator) still types gate.
    ("rule", (" rule", "extension")),  # last-resort rule catch (after specifics)
]


def infer_type(text: str) -> str:
    low = text.lower()
    for typ, kws in _TYPE_RULES:
        if any(k in low for k in kws):
            return typ
    return "item"


def trunc_words(title: str, n: int = 10) -> str:
    """First ``n`` words of the title, stripped of a leading bold/label run."""
    title = re.sub(r"\*\*[^*]*\*\*", lambda m: m.group(0).strip("*"), title).strip()
    words = title.split()
    return " ".join(words[:n]) + (" ..." if len(words) > n else "")


def parse_done(done_text: str, limit: int = 5) -> list[tuple[int, str]]:
    """The ``limit`` most-recent completed items from DONE.md, most-recent first.
    Ordered by completion DATE (the ledger date), tie-broken by highest PR number, NOT by
    PR number alone (P-1.30 bug a: merge order and completion-ledger order can diverge). A
    compound ``### PR #A + #B`` heading counts as ONE entry, represented by its highest PR.
    Returns ``(pr_number, title)``."""
    entries: list[tuple[str, int, str]] = []   # (date, representative_pr, title)
    for line in done_text.splitlines():
        m = DONE_ENTRY_RE.match(line)
        if m:
            prs = [int(m.group("pr"))]
            if m.group("extra"):
                prs += [int(x) for x in re.findall(r"#(\d+)", m.group("extra"))]
            entries.append((m.group("date"), max(prs), m.group("title").strip()))
    # ISO dates sort lexically == chronologically; reverse => most-recent first,
    # tie-broken by PR number descending.
    entries.sort(key=lambda e: (e[0], e[1]), reverse=True)
    return [(pr, title) for _date, pr, title in entries[:limit]]


def _short_id(title: str) -> str:
    """Leading backlog-id-like token in a title, else empty."""
    m = re.match(r"(P-\d+(?:\.\d+){0,2}[a-z]?|\d+(?:\.\d+){1,2}[a-z]?"
                 r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b", title.strip())
    return m.group(1) if m else ""


def render_pipeline(public_text: str, private_text: str | None,
                    done_text: str | None, umbrella_filter: str | None,
                    limit: int = 20, private_dir: "Path | None" = None) -> str:
    """Render the pipeline view: the 5 most-recent done at top (``[x]`` + PR####),
    then the current umbrella's open items up to ``limit``, filling from subsequent
    umbrellas (file/priority order) when the current one has fewer than ``limit``."""
    items = parse_items(public_text, "public", private_dir=private_dir)
    if private_text is not None:
        items += parse_items(private_text, "private", private_dir=private_dir)

    # Build LEAF items. A ``### `` block that contains ``- **<id>**`` bullets is an
    # umbrella whose bullets are the leaves (umbrella = the ### heading id + title);
    # a ``### `` block with no bullets is itself a leaf (umbrella = its ## parent).
    open_items: list[tuple[str, str, str, str, str]] = []
    for item_id, title, block, source, umb in items:
        if is_blocked(block, item_id):
            continue  # a [BLOCKED:] parent heading excludes itself AND its bullet leaves
        head_umb = f"{item_id} {title}".strip()
        # An umbrella's CHILDREN are the formal ids in its block that are dotted DESCENDANTS
        # of the umbrella id, written either as ``- **id**`` bullets OR inline in wave prose
        # (``**id** ...``); the inline form was previously dropped (P-1.30 bug b). A bullet in
        # the block whose id is NOT a descendant (a sibling item authored inside the block) is
        # promoted to its OWN leaf item rather than mis-attributed as this umbrella's child.
        # Collect every formal-id occurrence in the block and keep the BEST per id: a
        # non-blocked occurrence beats a blocked one, and a bullet beats an inline mention
        # (bullets are authoritative). This one structure unifies bullet-over-inline
        # precedence (r1 finding 1), foreign dedup (r1 finding 5), blocked-then-open recovery
        # (r2 finding 3), the inline-blocked segment (r2 finding 2), and the parent-resurrection
        # guard for all-blocked children whether bullet or inline (r1 finding 4 + r2 finding 1).
        occ: dict[str, dict] = {}
        lines = block.splitlines()

        def _consider(oid: str, otitle: str, oline: str, is_bullet: bool, blocked: bool) -> None:
            # A bullet is the AUTHORITATIVE statement of an item, so source ranks BEFORE
            # blocked status: a blocked bullet is NOT overridden by a non-blocked inline mention
            # (QA r3); a later non-blocked bullet still beats a blocked bullet of the same id.
            rank = (1 if is_bullet else 0, 0 if blocked else 1)
            cur = occ.get(oid)
            if cur is None or rank > cur["rank"]:
                occ[oid] = {"title": otitle, "line": oline, "blocked": blocked,
                            "descendant": _is_descendant(oid, item_id), "rank": rank}

        for line in lines:                 # pass 1: bullets (authoritative)
            bm = BULLET_ITEM_RE.match(line)
            if bm:
                _consider(bm.group("id"), bm.group("title"), line, True,
                          bool(BLOCKED_TAG_RE.search(line)) and _approved(bm.group("id")))
        for line in lines:                 # pass 2: inline wave-prose ids (non-bullet lines)
            if BULLET_ITEM_RE.match(line):
                continue
            ms = list(INLINE_ID_RE.finditer(line))
            for k, im in enumerate(ms):
                iid = im.group("id")
                # ONLY a dotted DESCENDANT inline id is a real child (an umbrella's wave item).
                # A non-descendant bold token in prose (a status word like **NOT-READY**, a
                # track header) matches the coded-id regex but is emphasis, NOT a backlog item,
                # so it is ignored: never promoted to a leaf and never counted toward `occ`
                # (which would suppress the heading's own leaf). Foreign items are BULLETS.
                if not _is_descendant(iid, item_id):
                    continue
                seg_end = ms[k + 1].start() if k + 1 < len(ms) else len(line)
                segment = line[im.start():seg_end]      # id .. next inline id / line end
                idesc = im.group("title").strip()
                # context = the child's OWN desc (the shared wave line mixes sibling items and
                # track keywords, which would mis-type an inline child).
                _consider(iid, idesc, idesc, False, bool(BLOCKED_TAG_RE.search(segment)) and _approved(iid))

        children = [(oid, o["title"], o["line"]) for oid, o in occ.items()
                    if not o["blocked"] and o["descendant"]]
        foreign = [(oid, o["title"], o["line"]) for oid, o in occ.items()
                   if not o["blocked"] and not o["descendant"]]
        if children or foreign:
            for oid, otitle, oline in children:
                open_items.append((oid, otitle, oline, source, head_umb))
            for oid, otitle, oline in foreign:
                open_items.append((oid, otitle, oline, source, umb or ""))
        elif not occ:
            # a genuine leaf with NO formal-id items is the item itself; a heading whose only
            # items are ALL blocked emits nothing (do not resurrect the parent as open).
            open_items.append((item_id, title, block, source, umb or title))

    out: list[str] = []
    # R20-GAP-1: degradation must be LOUD, not silent -- a maintainer view missing the
    # private backlog or the DONE ledger is INCOMPLETE and must say so at the top.
    missing = []
    if private_text is None:
        missing.append("private backlog (P-TODO.md)")
    if not done_text:
        missing.append("DONE ledger (recent-done section)")
    if missing:
        out.append("!!! INCOMPLETE PIPELINE VIEW: missing " + " + ".join(missing)
                   + " -- upcoming private items and/or done-marking are NOT shown !!!")
        out.append("")
    # 1. recent-done header
    if done_text:
        for pr, title in parse_done(done_text, 5):
            sid = _short_id(title) or f"#{pr}"
            out.append(f"{sid} [x] PR{pr} {infer_type(title)} - {trunc_words(title)}")
        out.append("")

    # 2. current umbrella up to limit, then fill from subsequent umbrellas
    umbrellas: list[str] = []
    for _i, _t, _b, _s, umb in open_items:
        if umb not in umbrellas:
            umbrellas.append(umb)
    if umbrella_filter:
        start = next((u for u in umbrellas if umbrella_filter.lower() in u.lower()), None)
        if start is None:
            # a non-matching filter must SIGNAL, not silently render the default view
            out.append(f"(no umbrella matched {umbrella_filter!r}; showing default order)")
            out.append("")
        order = umbrellas[umbrellas.index(start):] if start else umbrellas
    else:
        order = umbrellas  # first umbrella (highest-priority open item) leads

    shown = 0
    for ui, umb in enumerate(order):
        if shown >= limit:
            break
        grp = [it for it in open_items if it[4] == umb]
        if ui > 0:
            out.append("")  # blank line between umbrellas
        for item_id, title, _b, _s, _u in grp:
            if shown >= limit:
                break
            out.append(f"{item_id} [ ] {infer_type(title + ' ' + _b)} - {trunc_words(title)}")
            shown += 1
    return "\n".join(out)


def _self_test() -> int:
    failures: list[str] = []

    def check(name: str, cond: bool) -> None:
        if not cond:
            failures.append(name)

    # infer_type
    check("type-website", infer_type("first live /executive/ site render") == "website")
    check("type-rule", infer_type("new ai-supply-chain-provenance pack rule") == "rule")
    check("type-content", infer_type("author three scenario pages") == "content")
    check("type-validation", infer_type("full validation pass") == "validation")
    check("type-tool", infer_type("shared multi-line link scanner (lint_common)") == "tool")
    check("type-gate", infer_type("wire the new authority-boundary gate 87") == "gate")  # P-1.30 bug d
    check("type-gate-plural-stays-tool", infer_type("lint-executive-metadata.py + section/evidence gates") == "tool")
    check("type-gate-num-on-tool-stays-tool", infer_type("lint-x.py wiring for gate 87") == "tool")  # QA r3 NOTE-1

    # trunc_words: <=10 words, ellipsis when longer
    tw = trunc_words("one two three four five six seven eight nine ten eleven twelve")
    check("trunc-10-plus-ellipsis", tw.split(" ...")[0].split() == ["one","two","three","four","five","six","seven","eight","nine","ten"] and tw.endswith("..."))
    check("trunc-short-no-ellipsis", trunc_words("short title here") == "short title here")

    # parse_done: highest PR first, limit honoured
    done = "### PR #1420: item A (2026-08-05)\n\n### PR #1429: item B (2026-08-06)\n\n### PR #1425: item C (2026-08-05)\n"
    d = parse_done(done, 2)
    check("done-order-and-limit", d == [(1429, "item B"), (1425, "item C")])

    # render_pipeline: 5 done at top, then umbrella-grouped open items, blank between umbrellas
    pub = ("## Umbrella One\n\n### 1.1 First website render task here\n\n### 1.2 Second content brief task here\n\n"
           "## Umbrella Two\n\n### 2.1 A blocked one [BLOCKED:x] should not show\n\n### 2.2 A tool lint task here\n")
    r = render_pipeline(pub, None, "### PR #1429: recent done thing (2026-08-06)\n", None, limit=20)
    lines = r.splitlines()
    check("render-done-header", any(l.startswith("#1429 [x] PR1429 ") for l in lines))
    check("render-has-1.1", any(l.startswith("1.1 [ ] ") for l in lines))
    check("render-1.2-content", any(l.startswith("1.2 [ ] ") for l in lines))
    check("render-excludes-blocked", not any("2.1 [ ]" in l for l in lines))
    check("render-includes-2.2", any(l.startswith("2.2 [ ] ") for l in lines))
    # blank line between the two umbrellas (a "" line exists between 1.x and 2.x groups)
    check("render-blank-between-umbrellas", "" in lines[lines.index(next(l for l in lines if l.startswith("1.1"))):])

    # umbrella filter scopes to the matching umbrella first
    r2 = render_pipeline(pub, None, None, "Two", limit=20)
    r2_lines = [l for l in r2.splitlines() if l and not l.startswith("!!!")]
    check("filter-starts-at-two", r2_lines[0].startswith("2.2 [ ] "))

    # R20 fixes: blocked-parent leaf exclusion + loud banner on missing state
    rb = render_pipeline("## U\n\n### 9.9 Parent [BLOCKED:granted]\n- **9.9.1** child\n\n### 8.8 Open one\n", None, None, None)
    check("blocked-parent-leaf-excluded", "9.9.1" not in rb and any("8.8 [ ]" in l for l in rb.splitlines()))
    check("loud-banner-on-missing-state", any(l.startswith("!!! INCOMPLETE PIPELINE VIEW") for l in rb.splitlines()))

    # P-1.30 bug a: compound DONE headings counted (not skipped) and ordered by DATE, not PR.
    done2 = ("### PR #1500: newer low-pr (2026-08-07)\n\n"
             "### PR #1600: older high-pr (2026-08-01)\n\n"
             "### PR #1425 + #1426: compound entry (2026-08-06)\n")
    d2 = parse_done(done2, 3)
    check("done-date-order-not-pr",
          d2 == [(1500, "newer low-pr"), (1426, "compound entry"), (1600, "older high-pr")])
    check("done-compound-counted", any(pr == 1426 for pr, _ in d2))

    # P-1.30 bug b: inline wave-prose child ids are enumerated, and a non-descendant bullet
    # authored inside an umbrella block is PROMOTED to its own item, not mis-attributed.
    pub2 = ("## U3\n\n### P-9.1 Umbrella heading here\n"
            "- **P-9.9** sibling item authored inside the block\n"
            "- **P-9.1.1** real bullet child here\n"
            "_Wave X:_ **P-9.1.2** inline child two; **P-9.1.3** inline child three\n")
    r3l = render_pipeline(pub2, None, None, None, limit=20).splitlines()
    check("inline-child-enumerated",
          any(l.startswith("P-9.1.2 [ ] ") for l in r3l) and any(l.startswith("P-9.1.3 [ ] ") for l in r3l))
    check("bullet-child-enumerated", any(l.startswith("P-9.1.1 [ ] ") for l in r3l))
    check("foreign-bullet-promoted", any(l.startswith("P-9.9 [ ] ") for l in r3l))
    _ic = next(i for i, l in enumerate(r3l) if l.startswith("P-9.1.1"))
    _if = next(i for i, l in enumerate(r3l) if l.startswith("P-9.9"))
    check("foreign-bullet-separate-group", "" in r3l[min(_ic, _if):max(_ic, _if)])
    # an inline content child must type from its own desc, not the shared wave line
    pub3 = ("## U4\n\n### P-8.1 Umbrella here\n"
            "Track A (content): **P-8.1.1** author four briefs; Track B (website): **P-8.1.2** homepage re-hero\n")
    r4l = render_pipeline(pub3, None, None, None, limit=20).splitlines()
    check("inline-child-typed-from-own-desc",
          any(l.startswith("P-8.1.1 [ ] content ") for l in r4l)
          and any(l.startswith("P-8.1.2 [ ] website ") for l in r4l))

    # P-1.30 QA finding 1: a bullet is authoritative; an inline mention of the same id
    # (even earlier in the text) never shadows it -- the bullet's desc wins, one row only.
    pub5 = ("## U5\n\n### P-5.1 Umbrella\n"
            "_Wave:_ **P-5.1.1** inline shadow desc\n"
            "- **P-5.1.1** authoritative bullet desc here\n")
    r5l = [l for l in render_pipeline(pub5, None, None, None, limit=20).splitlines() if l.startswith("P-5.1.1")]
    check("bullet-wins-over-inline", len(r5l) == 1 and "authoritative bullet desc" in r5l[0])

    # finding 2: an inline desc with markdown emphasis is not truncated at the lone '*'.
    pub6 = ("## U6\n\n### P-6.1 Umbrella\nTrack: **P-6.1.1** author *four* briefs here\n")
    r6l = render_pipeline(pub6, None, None, None, limit=20).splitlines()
    check("inline-emphasis-not-truncated", any("briefs here" in l for l in r6l if l.startswith("P-6.1.1")))

    # finding 3: an inline child carrying a granted [BLOCKED] tag is excluded, like a bullet.
    pub7 = ("## U7\n\n### P-7.1 Umbrella\nWave: **P-7.1.1** ok child; **P-7.1.2** blocked [BLOCKED:granted] one\n")
    r7l = render_pipeline(pub7, None, None, None, limit=20).splitlines()
    check("inline-blocked-excluded",
          any(l.startswith("P-7.1.1 [ ] ") for l in r7l) and not any(l.startswith("P-7.1.2 ") for l in r7l))

    # finding 4: when every child bullet is blocked, neither the children NOR the parent emit.
    pub8 = ("## U8\n\n### P-8.9 Umbrella parent\n- **P-8.9.1** child [BLOCKED:granted]\n- **P-8.9.2** child2 [BLOCKED:granted]\n")
    r8l = render_pipeline(pub8, None, None, None, limit=20).splitlines()
    check("all-blocked-children-no-parent-resurrect",
          not any(l.startswith("P-8.9 ") for l in r8l) and not any(l.startswith("P-8.9.1") for l in r8l))

    # finding 5: a repeated foreign (non-descendant) bullet is deduplicated to one row.
    pub9 = ("## U9\n\n### P-9.5 Umbrella\n- **P-4.1** foreign sibling\n- **P-4.1** foreign sibling dup\n- **P-9.5.1** real child\n")
    r9l = [l for l in render_pipeline(pub9, None, None, None, limit=20).splitlines() if l.startswith("P-4.1 ")]
    check("foreign-bullet-deduped", len(r9l) == 1)

    # P-1.30 QA round 2 finding 1: a block whose ONLY descendants are blocked INLINE ids must
    # not resurrect the umbrella parent as an open leaf (the had_bullets guard missed inline).
    pubA = ("## UA\n\n### P-11.1 Umbrella parent\nWave: **P-11.1.1** one [BLOCKED:granted]; **P-11.1.2** two [BLOCKED:granted]\n")
    rAl = render_pipeline(pubA, None, None, None, limit=20).splitlines()
    check("all-blocked-inline-no-parent-resurrect",
          not any(l.startswith("P-11.1 ") for l in rAl) and not any(l.startswith("P-11.1.1") for l in rAl))

    # finding 2: a blocked tag OUTSIDE the desc span (e.g. bold **[BLOCKED]**) still excludes
    # the inline item, without one sibling's tag blocking the next.
    pubB = ("## UB\n\n### P-12.1 Umbrella\nWave: **P-12.1.1** open child; **P-12.1.2** child **[BLOCKED:granted]**\n")
    rBl = render_pipeline(pubB, None, None, None, limit=20).splitlines()
    check("inline-blocked-bold-span-excluded",
          any(l.startswith("P-12.1.1 [ ] ") for l in rBl) and not any(l.startswith("P-12.1.2 ") for l in rBl))

    # finding 3: a blocked bullet followed by a NON-blocked bullet of the same id emits the
    # authoritative open one (blocked-first must not permanently claim the id).
    pubC = ("## UC\n\n### P-13.1 Umbrella\n- **P-13.1.1** blocked copy [BLOCKED:granted]\n- **P-13.1.1** the real open work here\n")
    rCl = [l for l in render_pipeline(pubC, None, None, None, limit=20).splitlines() if l.startswith("P-13.1.1")]
    check("blocked-then-open-recovers", len(rCl) == 1 and "real open work" in rCl[0])

    # P-1.30 QA round 3: a granted-blocked BULLET is authoritative and is NOT overridden by a
    # non-blocked inline mention of the same id (source ranks before blocked status).
    pubD = ("## UD\n\n### P-14.1 Umbrella\n"
            "Wave: **P-14.1.1** inline open mention\n- **P-14.1.1** the blocked bullet [BLOCKED:granted]\n")
    rDl = render_pipeline(pubD, None, None, None, limit=20).splitlines()
    check("blocked-bullet-not-overridden-by-inline", not any(l.startswith("P-14.1.1") for l in rDl))

    # P-1.30 QA round 5: a bold NON-id-descendant coded/dotted token in a heading's prose (a
    # status word like **NOT-READY** that matches the coded-id regex) must NOT become a phantom
    # leaf and must NOT suppress the heading's own leaf emission (round-3 regression on item 3.119).
    pubE = ("## UE\n\n### 3.500 A real leaf item whose prose bolds a status word\n"
            "The worker returned **NOT-READY** because nothing was probed.\n")
    rEl = render_pipeline(pubE, None, None, None, limit=20).splitlines()
    check("non-descendant-inline-token-ignored",
          any(l.startswith("3.500 ") for l in rEl) and not any("NOT-READY" in l for l in rEl))

    # P-1.36 S36: a [BLOCKED:] tag counts only with a granted row in the approvals register.
    reg = ("| Item | Reason | Granted | Evidence |\n| --- | --- | --- | --- |\n"
           "| 2.1 | source | 2026-09-18 | #2364 |\n| `P-1.77` | ext | 2026-09-18 | 8168ee2 |\n"
           "| 2.2 | no date | soon | x |\n| 2.3 | no evidence | 2026-09-18 |  |\n| 2.4 | too | 2026-09-18 | x | y |\n"
           "| 2.6 |  | 2026-09-18 | #1 |\n")
    check("approvals-parse", load_approvals(reg) == {"2.1", "P-1.77"})
    reg2 = ("| Item | Reason | Granted | Evidence |\n| --- | --- | --- | --- |\n| 2.1 | ok | 2026-09-18 | #1 |\n"
            "| 6.6 | bad date | 2026-13-45 | #5 |\n| 7.7 | future | 2999-01-01 | #6 |\n\nLifted:\n\n"
            "| Item | Reason | Granted | Evidence |\n| --- | --- | --- | --- |\n| 3.3 | lifted | 2026-09-01 | #2 |\n")
    check("approvals-canonical-table-only", load_approvals(reg2) == {"2.1"})
    H = "| Item | Reason | Granted | Evidence |\n| --- | --- | --- | --- |\n"
    R = lambda i: f"| {i} | r | 2026-09-18 | #1 |\n"
    check("approvals-nested-fence", load_approvals("````markdown\n```\n" + H + R("1.1") + "```\n````\n") == set())
    check("approvals-mixed-fence", load_approvals("```\n~~~\n" + H + R("1.1") + "~~~\n```\n") == set())
    check("approvals-fence-refused", load_approvals("```\nexample\n```\n" + H + R("1.1")) == set()
          and load_approvals(H + R("1.1") + "```\nexample\n```\n") == set())
    check("approvals-header-exact", load_approvals(H.lower() + R("1.1")) == set()
          and load_approvals(H.replace("Item", "`Item`") + R("1.1")) == set())
    check("approvals-empty-fifth-cell", load_approvals(H + R("1.1").rstrip("\n") + "|\n") == set())
    # QA r4: the grammar is literal from column 0; commented, indented and malformed tables grant nothing.
    check("approvals-header-spacing", load_approvals(H.replace("| Item", "|  Item") + R("1.1")) == set()
          and load_approvals(H.replace("| Item", "|\tItem") + R("1.1")) == set())
    check("approvals-indented-table", load_approvals("para\n\n" + "".join("    " + l + "\n" for l in (H + R("1.1")).splitlines())) == set())
    check("approvals-commented-table", load_approvals("<!-- revoked\n" + H + R("1.1") + "-->\n") == set()
          and load_approvals("<!-- a --> <!-- revoked\n" + H + R("1.1") + "-->\n") == set()
          and load_approvals("<pre>\n" + H + R("1.1") + "</pre>\n") == set()
          and load_approvals(H + R("1.1").replace("#1", "e <!-- c -->")) == set())
    check("approvals-list-nested-fence", load_approvals("- example:\n\n    ```markdown\n    " + H.replace("\n", "\n    ")
                                                         + R("1.1") + "    ```\n") == set())
    check("approvals-table-before-header", load_approvals("|  Item | Reason | Granted | Evidence |\n\n" + H + R("2.2")) == set()
          and load_approvals("| A | B | C | D |\n|---|---|---|---|\n" + H + R("1.1")) == set()
          and load_approvals("  " + H + R("1.1")) == set())
    # QA r5: only LF, CRLF and CR break lines; other splitlines characters refuse the register.
    check("approvals-line-breaks", all(load_approvals("note:" + c + H.replace("\n", c) + R("1.1")) == set()
                                       for c in "\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029")
          and load_approvals(H.replace("\n", "\r\n") + R("1.1").replace("\n", "\r\n")) == {"1.1"})
    check("approvals-row-tail", load_approvals(H + "| 1.1 | r | 2026-09-18 | #1 | tail\n" + R("1.2")) == {"1.2"})
    check("approvals-row-trailing-space", load_approvals(H + R("1.1").replace("|\n", "|  \n")) == {"1.1"})
    check("approvals-mid-table-text-ends", load_approvals(H + R("1.1") + "note\n" + R("1.2")) == {"1.1"})
    # QA r6: one line model for refusal and parse; nothing before the header can contain it.
    check("approvals-cr-only", load_approvals("note\r```\r" + H.replace("\n", "\r") + R("1.1").replace("\n", "\r") + "```\r") == set()
          and register_refusal(H.replace("\n", "\r") + R("1.1")) is not None)
    check("approvals-pipeless-table-before", load_approvals("Revoked | Reason | Granted | Evidence\n--- | --- | --- | ---\n\n" + H + R("1.1")) == set())
    check("approvals-lazy-continuation", all(load_approvals(f"{m} revoked:\n" + H + R("1.1")) == set() for m in (">", "-", "*", "+", "1."))
          and load_approvals("revoked:\n" + H + R("1.1")) == set()
          and load_approvals("> quote\n\n" + H + R("1.1")) == set())
    check("approvals-escaped-pipe", load_approvals(H + "| 1.1 | r \\| 2026-09-18 | #1 |\n") == set())
    check("approvals-double-bom", load_approvals("\ufeff\ufeff" + H + R("1.1")) == set())
    # QA r7: blank means spaces and tabs only; cells a reader would read differently do not grant.
    check("approvals-unicode-blank", all(load_approvals("revoked:\n" + c + "\n" + H + R("1.1")) == set()
                                         for c in ("\xa0", "\u3000", "\u202f", "\x1f")))
    check("approvals-cell-code-span", load_approvals(H + "| 1.1 | r ` | 2026-09-18 | ` #1 |\n") == set()
          and load_approvals(H + "| `1.1` | r | 2026-09-18 | #1 |\n") == {"1.1"})
    check("approvals-cell-entity-invisible", load_approvals(H + "| 1.1 | r | 2026-09-18 | &nbsp; |\n") == set()
          and load_approvals(H + "| 1.1 | \u200b | 2026-09-18 | #1 |\n") == set())
    check("approvals-header-trailing-space", load_approvals(H.replace("Evidence |\n", "Evidence |  \n") + R("1.1")) == {"1.1"})
    check("approvals-front-matter", load_approvals("---\nx: y\n\n" + H + R("1.1") + "---\n") == set())
    check("approvals-harmless-prose", load_approvals("`blocked-approvals.md` lists grants.\n*Maintainer-granted.*\n"
                                                     "1.26.44 has no recorded grant.\n\n" + H + R("1.1")) == {"1.1"}
          and load_approvals("* item\n\n" + H + R("1.1")) == set() and load_approvals("1. item\n\n" + H + R("1.1")) == set())
    # QA r7: the file is read without newline translation, so a lone-CR register is refused from disk too.
    import tempfile as _tf2
    with _tf2.TemporaryDirectory(prefix="approvals-file-") as ad:
        reg_path = Path(ad) / "reg.md"
        reg_path.write_bytes((H + R("1.1")).replace("\n", "\r").encode("utf-8"))
        saved = _APPROVALS
        try:
            note = _load_default_approvals(str(reg_path))
            check("approvals-file-lone-cr", "refused" in note and _APPROVALS == set())
        finally:
            set_approvals(saved)
    # QA r8: cells are a whitelist; controls anywhere refuse; skipped rows are reported.
    check("approvals-cell-whitelist", all(load_approvals(H + f"| 1.1 | {r} | 2026-09-18 | {e} |\n") == set() for r, e in (
        ("[]()", "#1"), ("r", "[](x)"), ("r", "![]()"), ("r", "\u3164"), ("\u2800", "#1"), ("r\u034f", "#1"),
        ("r", "\ue000"), ("\xa0r", "#1"), ("\x1fr", "#1"), ("r\x1f", "#1"), ("r", "a\\b"), ("r", "--"))))
    check("approvals-cell-tab", load_approvals(H + "| 1.1 | source\tgated | 2026-09-18 | #1 |\n") == {"1.1"})
    check("approvals-file-controls", register_refusal("Register\x1b[8m\n\n" + H + R("1.1")) is not None
          and register_refusal("note\x00\n\n" + H + R("1.1")) is not None)
    check("approvals-toml-and-lists", all(load_approvals(pre + "\n\n" + H + R("1.1")) == set()
                                          for pre in ("+++\ntitle = 'x'", "+ item", "1) item")))
    ids, skipped = parse_approvals(H + R("1.1") + "| 1.2 | r | soon | #1 |\n| 1.3 | r | 2026-09-18 |\n")
    check("approvals-skips-reported", ids == {"1.1"} and len(skipped) == 2 and "line 4" in skipped[0])
    # QA r9
    ids, skipped = parse_approvals(H + R("1.1") + "   " + R("1.2") + R("1.3"))
    check("approvals-after-table-named", ids == {"1.1"} and len(skipped) == 2 and "line 4" in skipped[0] and "line 5" in skipped[1])
    check("approvals-strike-shortcode", load_approvals(H + "| 1.1 | ~~r~~ | 2026-09-18 | #1 |\n") == set()
          and load_approvals(H + "| 1.1 | r | 2026-09-18 | :x: |\n") == set()
          and load_approvals(H + "| 1.1 | r | 2026-09-18 | see https://github.com/x |\n") == {"1.1"})
    ids, skipped = parse_approvals("| Item | Reason | Granted | Evidence |\n" + R("1.1"))
    check("approvals-separator-note", ids == set() and "separator" in skipped[0])
    saved_h = _APPROVALS
    try:
        set_approvals({"1.1", "3.92"})
        rep_h = build_report("", "## 1. Band\n### 1.1 a [BLOCKED:x]\n### 1.1\u0662 b [BLOCKED:y]\n### 1.1.\u0663 c [BLOCKED:z]\n"
                             "### 3.92.a: child [BLOCKED:x]\n### 3.92.a, child [BLOCKED:x]\n### 1.1-x: t [BLOCKED:x]\n"
                             "### 1.1.a\u0662 c [BLOCKED:x]\n")
        # a child never inherits its parent's grant, however its id ends (fix-check after QA r9)
        check("approvals-non-ascii-heading", _heading_id("### 1.1\u0662 b") == _UNREADABLE_HEADING_ID
              and _heading_id("### 1.1 a") == "1.1" and _heading_id("### 3.92.a: child") == "3.92.a"
              and all(_heading_id("### 3.92." + c + "a: child") == _UNREADABLE_HEADING_ID
                      for c in ("\u200b", "\u00ad", "\u2060", "\u0301", "\x9b", "\x7f", "\u200e"))
              and _heading_id("### 3.92.a_b x") == _UNREADABLE_HEADING_ID
              and rep_h[1] == 1)
    finally:
        set_approvals(saved_h)
    check("approvals-refusal-layers", "carriage return" in (register_refusal("note\rmore") or "")
          and "byte-order" in (register_refusal("\ufeff\ufeffnote") or ""))
    check("approvals-prose-and-heading-before", load_approvals("# Title\n\nSome prose (with parens).\n\n" + H + R("1.1")) == {"1.1"})
    check("approvals-separator-padding", load_approvals(H.replace("| --- | --- | --- | --- |", "|  ---  | :--- | ---: |  ---  |  ") + R("1.1")) == {"1.1"})
    check("approvals-refusal-reason", register_refusal("<!--\n" + H) is not None and register_refusal(H + R("1.1")) is None
          and register_refusal(H + R("1.1") + "\x85") is not None)
    check("approvals-needs-separator", load_approvals("| Item | Reason | Granted | Evidence |\n" + R("1.1") + R("1.2")) == set())
    check("approvals-indented-row", load_approvals(H + "    " + R("1.1") + R("1.2")) == set())
    check("approvals-date-form", load_approvals(H + "| 1.1 | r | 20260918 | #1 |\n| 1.2 | r | 2026-W38-5 | #1 |\n") == set())
    check("approvals-trailing-dot-id", load_approvals(H + R("1.1.")) == set())
    check("approvals-bom", load_approvals("\ufeff" + H + R("1.1")) == {"1.1"})
    # QA r4: the origin lookup against real (local, offline) repositories.
    import tempfile as _tf
    with _tf.TemporaryDirectory(prefix="origin-probe-") as od:
        od = Path(od)
        plain = od / "plain"; plain.mkdir()
        repo = od / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True, env=_git_env())
        def with_origin(url):
            subprocess.run(["git", "-C", str(repo), "config", "remote.origin.url", url], check=True, capture_output=True,
                           env=_git_env())
            return _origin_is_maintainer(repo)
        results = {"not-a-repo": _origin_is_maintainer(plain), "no-origin": _origin_is_maintainer(repo),
                   "other": with_origin("https://github.com/someone/repo.git"),
                   "canonical": with_origin("https://github.com/jposluns/grc_library.git"),
                   "trailing-slash": with_origin("https://github.com/jposluns/grc_library/"),
                   "case": with_origin("git@github.com:JPosluns/grc_library.git"),
                   "owner-suffix": with_origin("https://github.com/evil-jposluns/grc_library")}
        with_origin("https://github.com/jposluns/grc_library.git")
        injected = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "remote.origin.url",
                    "GIT_CONFIG_VALUE_0": "https://example.org/x/y.git", "GIT_DIR": str(plain)}
        saved_env = {k: os.environ.get(k) for k in injected}
        os.environ.update(injected)
        try:
            results["inherited-git-env"] = _origin_is_maintainer(repo)  # QA r5: inherited variables are dropped
        finally:
            for k, v in saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        with open(repo / ".git" / "config", "ab") as fh:
            fh.write(b'\n[remote "origin"]\n\turl = https://example.org/\xff/repo.git\n')
        results["undecodable"] = _origin_is_maintainer(repo)
        check("origin-lookup", results == {"not-a-repo": None, "no-origin": False, "other": False,
                                           "canonical": True, "trailing-slash": True, "case": True,
                                           "owner-suffix": False, "inherited-git-env": True, "undecodable": None})
    tagged = "| 2.1 | t | `[BLOCKED:x]` |"
    saved_approvals = _APPROVALS
    try:
        set_approvals(None)
        check("approvals-none-counts-tag", is_blocked(tagged, "2.1"))
        set_approvals(set())
        check("approvals-empty-counts-nothing", not is_blocked(tagged, "2.1"))
        set_approvals({"2.1"})
        check("approvals-row-counts", is_blocked(tagged, "2.1"))
        check("approvals-other-id-does-not", not is_blocked(tagged.replace("2.1", "2.5"), "2.5"))
        check("approvals-no-id-does-not", not is_blocked("`[BLOCKED:x]` a heading with no item id"))
        check("approvals-heading-id-read", is_blocked(tagged))
        check("approvals-tag-still-seen", has_blocked_tag(tagged.replace("2.1", "2.5")))
        set_approvals({"3.92"})
        check("approvals-bind-full-heading-id", not is_blocked("### 3.92.a Child A [BLOCKED:x]", "3.92"))
        set_approvals({"3.92.a"})
        check("approvals-full-heading-id-granted", is_blocked("### 3.92.a Child A [BLOCKED:x]", "3.92"))
        umb = ("## 9. U\n### 9.1 Umbrella\n- **9.1.1** leaf a `[BLOCKED:x]`\n- **9.1.2** leaf b\n")
        set_approvals(set())
        out_none = render_pipeline(umb, None, None, None)
        check("approvals-unapproved-bullet-stays-open", "9.1.1" in out_none)
        set_approvals({"9.1.1"})
        out_ok = render_pipeline(umb, None, None, None)
        check("approvals-approved-bullet-excluded", "9.1.1" not in out_ok and "9.1.2" in out_ok)
        wave = "## 9. U\n### 9.2 Waves\n_Wave 1_: **9.2.1** inline a `[BLOCKED:x]`; **9.2.2** inline b\n"
        set_approvals(set())
        check("approvals-unapproved-inline-stays-open", "9.2.1" in render_pipeline(wave, None, None, None))
        set_approvals({"9.2.1"})
        check("approvals-approved-inline-excluded", "9.2.1" not in render_pipeline(wave, None, None, None))
        # The default register lookup (QA r1, r2): only the authoritative store is read; a store that cannot be
        # examined, a maintainer checkout without a store, a missing register and a non-regular register count
        # no tag; only a non-maintainer checkout with no store keeps tags as written.
        g = globals()
        real_sd, real_om = g["_store_dir"], g["_origin_is_maintainer"]
        import tempfile as _tf
        try:
            with _tf.TemporaryDirectory() as _d:
                store = Path(_d) / "private"
                store.mkdir()
                g["_store_dir"], g["_origin_is_maintainer"] = (lambda *a, **k: None), (lambda *a, **k: False)
                _load_default_approvals(None)
                check("approvals-adopter-no-store-tags-count", _APPROVALS is None)
                g["_origin_is_maintainer"] = lambda *a, **k: True
                _load_default_approvals(None)
                check("approvals-maintainer-without-store-counts-nothing", _APPROVALS == set())
                g["_origin_is_maintainer"] = lambda *a, **k: None
                _load_default_approvals(None)
                check("approvals-unknown-origin-counts-nothing", _APPROVALS == set())
                def _inaccessible(*a, **k):
                    raise InaccessiblePath(13, "Permission denied", str(store))
                g["_store_dir"] = _inaccessible
                _load_default_approvals(None)
                check("approvals-inaccessible-store-counts-nothing", _APPROVALS == set())
                g["_store_dir"] = lambda *a, **k: store
                _load_default_approvals(None)
                check("approvals-store-without-register-counts-nothing", _APPROVALS == set())
                reg = store / APPROVALS_FILE
                reg.write_bytes(b"| Item | Reason | Granted | Evidence |\n| --- | --- | --- | --- |\n"
                                b"| 1.1 | x | 2026-09-18 | \xff\xfe |\n")
                _load_default_approvals(None)
                check("approvals-undecodable-counts-nothing", _APPROVALS == set())
                reg.unlink()
                reg.mkdir()
                _load_default_approvals(None)
                check("approvals-directory-register-counts-nothing", _APPROVALS == set())
                real_exists = Path.exists
                def _raising_exists(self, *a, **k):
                    if self.name == APPROVALS_FILE:
                        raise PermissionError(13, "Permission denied")
                    return real_exists(self, *a, **k)
                Path.exists = _raising_exists
                try:
                    _load_default_approvals(None)
                    check("approvals-stat-error-counts-nothing", _APPROVALS == set())
                finally:
                    Path.exists = real_exists
                reg.rmdir()
                os.mkfifo(reg)
                _load_default_approvals(None)  # must not block on the FIFO
                check("approvals-fifo-register-counts-nothing", _APPROVALS == set())
        finally:
            g["_store_dir"], g["_origin_is_maintainer"] = real_sd, real_om
    finally:
        set_approvals(saved_approvals)

    if failures:
        for f in failures:
            print(f"  SELF-TEST FAIL: {f}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all pipeline cases passed (type inference incl. gate, 10-word truncation, "
          "recent-done date-ordering + compound headings, umbrella grouping, inline-wave children, "
          "foreign-bullet promotion, blocked exclusion, umbrella filter).")
    return 0


_MAINTAINER_ORIGIN = "jposluns/grc_library"


def _git_env() -> "dict[str, str]":
    """The environment without inherited git variables (GIT_DIR, GIT_CONFIG_COUNT/KEY/VALUE and the rest), which
    could point git at another repository or inject an origin; global and system config are not read (QA r5)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return env


def _git_out(root: Path, *args: str) -> "tuple[int, str] | None":
    """(returncode, stripped stdout) of a git command, or None if git cannot run or its output is not UTF-8."""
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=3, env=_git_env())
        return proc.returncode, proc.stdout.decode("utf-8").strip()
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError):
        return None


def _origin_is_maintainer(root: Path = REPO_ROOT) -> "bool | None":
    """True when the checkout's origin is the maintainer repository, False when git reports another origin or
    none, and None when the origin cannot be established: ignorance is not evidence of an adopter (QA r3).
    The match is block-operational-without-private's boundary test (trailing ``.git`` stripped; equal to, or
    containing after ``/`` or ``:``, ``jposluns/grc_library``), made case-insensitive, so a trailing slash or
    a suffixed sibling name also reads as the maintainer; that errs toward counting fewer tags (QA r4). A
    directory git does not recognize as a repository (not one, or refused as dubious ownership) is None, since
    ``config --get`` would report such a failure the same way as an unset key (QA r4). The two 3 s git timeouts
    keeps the lookup inside the unattended stop guard's budget."""
    probe = _git_out(root, "rev-parse", "--git-dir")
    if probe is None or probe[0] != 0:
        return None
    got = _git_out(root, "config", "--get", "remote.origin.url")
    if got is None:
        return None
    rc, out = got
    if rc == 1 and not out:
        return False  # a repository with no origin configured
    if rc != 0:
        return None
    url = out[:-4] if out.endswith(".git") else out
    url, target = url.lower(), _MAINTAINER_ORIGIN
    return url == target or f"/{target}" in url or f":{target}" in url


def _load_default_approvals(explicit: "str | None") -> str:
    """Set the approvals for this run and return a one-line note saying which rule applied. Only the
    authoritative store is read (no fallback location can grant); a store that cannot be examined, a
    maintainer checkout without a store, a missing register and a register that is not a regular file all
    count no tag; only a non-maintainer checkout with no store at all keeps tags as written (QA r2)."""
    if explicit:
        path = Path(explicit)
    else:
        try:
            store = _store_dir(REPO_ROOT, strict=True)
        except (InaccessiblePath, OSError) as exc:
            set_approvals(set())
            return f"[BLOCKED] approvals: the operational store cannot be examined ({exc}); NO tag counts as blocked."
        if store is None:
            origin = _origin_is_maintainer()
            if origin is not False:
                set_approvals(set())
                why = "maintainer checkout" if origin else "checkout whose origin cannot be established"
                return f"[BLOCKED] approvals: {why} without the operational store; NO tag counts as blocked."
            set_approvals(None)
            return "[BLOCKED] approvals: no operational store (adopter clone); tags count as written."
        path = store / APPROVALS_FILE
    try:  # every probe inside the handler: a metadata error must not cost the actionable count (QA r3)
        if not path.exists():
            set_approvals(set())
            return (f"[BLOCKED] approvals: no register at {path}; NO tag counts as blocked "
                    f"(a missing register never widens what is blocked).")
        if not path.is_file():
            set_approvals(set())
            return f"[BLOCKED] approvals: {path} is not a regular file; NO tag counts as blocked."
        text = path.read_bytes().decode("utf-8")  # keep lone CRs for the refusal check (QA r7)
    except (OSError, UnicodeDecodeError) as exc:
        set_approvals(set())
        return f"[BLOCKED] approvals: {path} unreadable ({exc}); NO tag counts as blocked."
    refusal = register_refusal(text)
    if refusal is not None:
        set_approvals(set())
        return f"[BLOCKED] approvals: {path} refused ({refusal}); NO tag counts as blocked."
    ids, skipped = parse_approvals(text)
    set_approvals(ids)
    note = f"[BLOCKED] approvals: {len(ids)} granted row(s) in {path}."
    if skipped:
        note += f" {len(skipped)} row(s) grant nothing: " + "; ".join(skipped)
    return note


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--actionable-only", action="store_true",
                    help="print only the summary and the ACTIONABLE list")
    ap.add_argument("--pipeline", action="store_true",
                    help="render the scannable roadmap pipeline view")
    ap.add_argument("--umbrella", default=None,
                    help="--pipeline: scope to the umbrella whose header matches this substring")
    ap.add_argument("--self-test", action="store_true", help="run internal self-test")
    ap.add_argument("--todo", default=None, help="public TODO.md path")
    ap.add_argument("--ptodo", default=None,
                    help="private P-TODO.md path (no-op if absent)")
    ap.add_argument("--approvals", default=None,
                    help="the [BLOCKED] approvals register (default: blocked-approvals.md in the operational store)")
    ap.add_argument("--private-root", default=None,
                    help="override the private-sibling dir the reference (detail) bodies "
                         "load from (F1793-5 / P-1.53), at parity with the index-reference "
                         "parity gate's --private-root; a fixture run scopes it hermetically")
    args = ap.parse_args(argv)
    # 3b50b2e2: an EXPLICIT --todo, --ptodo or --private-root that does not exist is refused; it
    # used to become a portable-clone no-op, a silent public-only run, or be ignored. The defaults
    # keep their documented portable-clone behaviour.
    for flag, value, want in (("--todo", args.todo, "file"), ("--ptodo", args.ptodo, "file"),
                              ("--private-root", args.private_root, "dir"), ("--approvals", args.approvals, "file")):
        if value is None:
            continue
        ok = value.strip() and (Path(value).is_file() if want == "file" else Path(value).is_dir())
        if not ok:
            print(f"ERROR: {flag} {value!r}: not an existing {'file' if want == 'file' else 'directory'}.",
                  file=sys.stderr)
            return 2
    if args.todo is None:
        args.todo = str(TODO_PATH)
    if args.ptodo is None:
        args.ptodo = str(PTODO_PATH)
    private_dir = Path(args.private_root).resolve() if args.private_root else None

    if args.self_test:
        return _self_test()

    todo = Path(args.todo)
    if not todo.is_file():
        print(f"advisory: TODO.md not found at {todo} (portable clone); no-op.")
        return 0
    public_text = todo.read_text(encoding="utf-8", errors="replace")

    ptodo = Path(args.ptodo)
    private_text = ptodo.read_text(encoding="utf-8", errors="replace") \
        if ptodo.is_file() else None
    private_note = "" if private_text is not None \
        else f" (private list {ptodo} absent; public-only)"

    approvals_note = _load_default_approvals(args.approvals)  # every mode, including --pipeline (QA r1)
    if args.pipeline:
        print(approvals_note, file=sys.stderr)  # the refusal reason stays visible in --pipeline mode (QA r7)
        done = resolve_working("DONE.md")
        done_text = done.read_text(encoding="utf-8", errors="replace") if done and done.is_file() else None
        print(render_pipeline(public_text, private_text, done_text, args.umbrella,
                              private_dir=private_dir))
        return 0

    rows, blocked, actionable = build_report(public_text, private_text, private_dir=private_dir)

    def trunc(t: str, w: int = 52) -> str:
        t = t.strip()
        return t if len(t) <= w else t[: w - 3] + "..."

    if not args.actionable_only:
        print(f"Backlog actionability enumeration (both lists){private_note}:")
        print(f"{'id':<10} {'list':<8} {'BLOCKED?':<9} {'prose-signal':<20} title")
        print("-" * 100)
        for item_id, title, source, b, sig in rows:
            bl = "BLOCKED" if b else "-"
            ps = ",".join(sig) if sig else ""
            print(f"{item_id:<10} {source:<8} {bl:<9} {ps:<20} {trunc(title)}")

    print(f"\n{len(rows)} open item(s) across both lists; {blocked} BLOCKED "
          f"(approved [BLOCKED:] tag); {actionable} ACTIONABLE.")
    print("An item is BLOCKED only via a maintainer-approved [BLOCKED:<reason>] "
          "tag. 'all blocked' is assertable only when EVERY item carries one.")

    print(approvals_note)
    items_all = parse_items(public_text, "public", private_dir=private_dir) + (
        parse_items(private_text, "private", private_dir=private_dir) if private_text is not None else [])
    unapproved = [(i, t) for i, t, blk, _s, _u in items_all
                  if has_blocked_tag(blk) and not _approved(_heading_id(blk) or i)]
    if unapproved:
        print(f"\nUNAPPROVED [BLOCKED] TAG ({len(unapproved)}) -- no row in the approvals register, so "
              f"counted ACTIONABLE; record the maintainer's grant or remove the tag:")
        for item_id, title in unapproved:
            print(f"  - {item_id}  {trunc(title)}")

    # Advisory: items whose PROSE mentions a blocker but that carry no approved tag
    # are ACTIONABLE and are candidates to PROPOSE for a [BLOCKED] tag (never self-tag).
    propose = [(i, t, sig) for i, t, s, b, sig in rows if sig and not b]
    if propose:
        print(f"\nPROSE-SIGNAL, NO APPROVED TAG ({len(propose)}) "
              f"-- ACTIONABLE now; propose a [BLOCKED] tag via pending-decisions.md:")
        for item_id, title, sig in propose:
            print(f"  - {item_id}  [{','.join(sig)}]  {trunc(title)}")

    actionable_rows = [(i, t, s) for i, t, s, b, sig in rows if not b]
    if actionable_rows:
        print(f"\nACTIONABLE ({len(actionable_rows)}):")
        for item_id, title, source in actionable_rows:
            print(f"  - {item_id}  ({source})  {trunc(title)}")
    else:
        print("\n(no actionable items: every open item on both lists carries an "
              "approved [BLOCKED:] tag. Verify each before any all-blocked claim.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
