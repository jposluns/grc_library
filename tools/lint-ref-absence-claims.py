#!/usr/bin/env python3
"""Reference-absence claim audit, using the committed acquisition manifest.

Binding is line-bound under the maintainer ruling of 2026-09-30
18:34Z, and detection fails closed under the ruling of 20:47Z. A
canonical claim is satisfied only by its own marker opening on a source
line the claim spans, from the line holding its first word to the line
holding its last. No paragraph, list, table, heading or HTML block is
modelled, so no marker is borrowed from a neighbouring line. Files are
split into lines on newlines only, one model shared by fenced-code
detection and claim scanning, so a Unicode line separator never moves a
marker off its claim's line.

Claims are detected on stripped copies of each file that remove inline
markup at any position, including inside a word, and case-fold:
emphasis, strong and strikethrough delimiters, code-span backticks,
backslash escapes and soft hyphens are dropped, entities are decoded,
HTML tags and closed comments are removed, and link syntax keeps the
visible link text while dropping the destination, title or reference
label. Each copy maps every kept character back to its source offset,
so the line-bound rule is applied to the original lines the claim
spans. Because a reference label may or may not resolve and a
commented-out claim is still a claim, four copies cover both comment
readings and both link readings, and the offset-preserving blanked
readings of earlier rounds are still scanned. A claim found in any
reading is checked, and matches sharing a start keep the shortest
span, so an inline construct the scanner cannot resolve can add a
blocking finding but cannot hide one; an unclosed construct is read in
whichever direction keeps the claim text visible.

A marker opens with "<!-- ref-absence:" and must close before a blank
line. An unclosed marker, or one whose text between blank lines holds an
unpaired backtick run, is malformed and satisfies nothing; one inside a
paired code span is example text, and backtick runs inside closed
comments never pair as code spans. Markers are checked for orphaning,
empty queries and staleness; a marker is orphaned unless a canonical
claim or annotatable paraphrase spans its line. Near misses are advisory
only.

Fenced code is skipped only when its closing fence arrives before a
line leaves the opener's quote or list prefix or indentation. A fence
line inside a closed HTML comment neither opens nor closes a fence, and
an ordered-list fence opener written other than as 1 directly under a
non-blank line is not an opener. An unclosed fence and indented code
are read as prose. Raw HTML blocks are not modelled, so fence lines
inside them still pair as fences.

The manifest covers four trusted acquisition buckets, not publications
or books. Staleness is observable only after a regenerated manifest is
committed; the sibling reference repository is never read. The advisory
heuristics cannot reliably infer semantics; missing-content wordings are
distinguished from missing-source wordings only by the documented token
windows. The audit specification records those residues.

Residue, shipped under the maintainer rulings of 2026-09-30 22:49Z
and 23:04Z: detection does not fail closed in general. The first
paragraph's "fails closed" and the second paragraph's "cannot hide
one" and "keeps the claim text visible" state the design intent, not
a guarantee. Inline HTML (valid or malformed), entity-encoded or
invisible characters, escaped or unbalanced backticks and unclosed
constructs can hide a canonical claim from the detector. So can comment pairing across fence lines and raw
HTML blocks, even in valid Markdown. Known examples: a quoted
attribute holding ">" or "<", a tag outside INLINE_JOIN_TAGS or a
well-formed marker inside a claim word. Entities are decoded after
the _JOINER_CHARS check, so "&shy;" or "&#8203;" splits a word, as do
U+2060, U+034F and variation selectors. Escaped backticks, or
backticks paired across list items, headings, table cells, link
destinations or attribute values, form a false code span that keeps
an in-word link, tag or comment literal. An unmatched backtick can make a code-span
link opener swallow a later linked claim. An unclosed link title or
tag attribute leaves its text between the words. A "<!--" in a code
span or fenced block can pair with a later "-->", so a real fence
line counts as comment-covered and fences pair wrongly. A fence line
inside a raw HTML block pairs with a later fence. These shapes are
tracked as backlog item 3b144; the audit specification states the
same residue.

Usage: python3 tools/lint-ref-absence-claims.py [path ...]
Exit: 0 no blocking findings; 1 blocking findings; 2 invalid inputs.
"""

from __future__ import annotations

import argparse
import bisect
import html
import re
import sys
from pathlib import Path

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    REPO_ROOT,
    guard_explicit_paths,
    iter_scan_roots_markdown,
    read_text_safe,
)


MANIFEST_PATH = "docs/reference-acquisition-manifest.md"


EXEMPT_FILES = set((
    "CHANGELOG.md",  # Historical rule-pattern quotations.
    "governance/specification-audit-programme.md",  # Gate specification.
))

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]


_GAP = r"(?:\s|[*_~`\[\]])+"
CANONICAL_RE = re.compile(
    r"(?<![^\W_])not" + _GAP + r"(?:currently" + _GAP + r")?held" + _GAP + r"in" + _GAP
    + r"(?:(?:the|our)" + _GAP + r")?reference" + _GAP + r"(?:base|library)(?![^\W_])",
    re.IGNORECASE,
)

# The stripped copies already delete emphasis and underscores, so plain
# word boundaries and whitespace gaps are exact there.
CANONICAL_STRIPPED_RE = re.compile(
    r"\bnot\s+(?:currently\s+)?held\s+in\s+(?:(?:the|our)\s+)?reference\s+(?:base|library)\b"
)

MARKER_OPEN_RE = re.compile(r"<!--\s*ref-absence:")
BLANK_LINE_RE = re.compile(r"\n[ \t]*\n")
BACKTICK_RUN_RE = re.compile(r"`+")


# Word edges use (?<![^\W_]) and (?![^\W_]) rather than \b so an emphasis
# underscore touching a trigger word does not defeat the trigger.
NEAR_MISS_TRIGGER_RE = re.compile(
    r"(?<![^\W_])not\s+(?:(?:\w+ly|yet)\s+)?(?:held|included|present|available|indexed|stored)(?![^\W_])"
    r"|(?<![^\W_])(?:absent|missing|excluded|omitted)\s+from(?![^\W_])"
    r"|(?<![^\W_])(?:does|do)\s+not\s+(?:(?:\w+ly|yet)\s+)?(?:hold|include|contain|carry)(?![^\W_])",
    re.IGNORECASE,
)


NEGATIVE_SUBJECT_TRIGGER_RE = re.compile(
    r"(?<![^\W_])(?:neither|none|no|nor)(?![^\W_])(?:\s+[\w'-]+){0,6}?\s+(?:is|are|was|were)\s+"
    r"(?:(?:\w+ly|yet)\s+)?(?:held|included|present|available|indexed|stored)(?![^\W_])",
    re.IGNORECASE,
)


COLLECTION_SUBJECT_TRIGGER_RE = re.compile(
    r"(?<![^\W_])(?:reference\s+(?:base|library)|grc_library_ref)\s+"
    r"(?:[\w'-]+\s+){0,2}?(?:lacks|omits)(?![^\W_])",
    re.IGNORECASE,
)

TRIGGER_RES = (
    NEAR_MISS_TRIGGER_RE,
    NEGATIVE_SUBJECT_TRIGGER_RE,
    COLLECTION_SUBJECT_TRIGGER_RE,
)


MANUAL_ABSENCE_RE = re.compile(
    r"(?<![^\W_])(?:carries|carry)\s+no\s+copy\s+of(?![^\W_])"
    r"|(?<![^\W_])nor\s+(?:is|are|was|were)(?![^\W_])"
    r"(?:(?:\b(?:[A-Za-z]\.){2,}|\b(?:Mr|Mrs|Ms|Dr|Prof|St|No|Sec|Art)\."
    r"|\b\d+(?:\.\d+)+)|[^.!?])*?"
    r"(?<![^\W_])(?:held|included|present|available|indexed|stored)(?![^\W_])",
    re.IGNORECASE,
)
ANNOTATABLE_TRIGGER_RES = (*TRIGGER_RES, MANUAL_ABSENCE_RE)


HELD_VERB_RE = re.compile(r"\bh[eo]ld\b", re.IGNORECASE)


NEAR_MISS_CONTEXT_RE = re.compile(
    r"reference\s+(?:base|library)|held\s+texts?|grc_library_ref",
    re.IGNORECASE,
)


NEAR_MISS_COLLECTION_CONTEXT_RE = re.compile(
    r"reference\s+(?:base|library)|grc_library_ref",
    re.IGNORECASE,
)
NEAR_MISS_WINDOW_TOKENS = 8


HELD_TEXT_OBJECT_RE = re.compile(
    r"^\s*(?:(?:in|within|from)\s+)?"
    r"(?:(?!(?:reference|base's|library's|grc_library_ref)\b)[\w'-]+\s+){0,3}?"
    r"held\s+texts?\b",
    re.IGNORECASE,
)


HELD_TEXT_SUBJECT_RE = re.compile(
    r"\bheld\s+texts?(?:'s?)?"
    r"(?:[,;:]?\s+(?!(?:reference|grc_library_ref)\b)[\w'()-]+){0,6}"
    r"[,;:]?\s*$",
    re.IGNORECASE,
)


COLLECTION_POSSESSED_SUBJECT_RE = re.compile(
    r"\b(?:reference\s+(?:base|library)|grc_library_ref)'s\s+"
    r"(?:[\w'-]+\s+){0,2}?held\s+texts?(?:'s?)?"
    r"(?:[,;:]?\s+[\w'()-]+){0,6}[,;:]?\s*$",
    re.IGNORECASE,
)


FENCE_RE = re.compile(r"( {0,3})(`{3,}|~{3,})(.*)$")
FENCE_QUOTE_RE = re.compile(r" {0,3}> ?")
FENCE_LIST_RE = re.compile(r" {0,3}(?:[-*+]|\d{1,9}[.)]) {1,4}(?! )")
FENCE_ORDERED_RE = re.compile(r" {0,3}(\d{1,9})[.)]")


# Line-start quote, list, heading and pipe syntax. Every reading blanks
# it, so a claim wrapped inside a container is one match.
LINE_PREFIX_RE = re.compile(
    r"^[ \t]*(?:(?:>|\|)[ \t]*|(?:[-*+]|\d{1,9}[.)]|#{1,6})(?:[ \t]+|$))+",
    re.MULTILINE,
)


TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)(?:\s(?:[^<>\n]|\n(?![ \t]*\n))*)?/?>")
ENTITY_RE = re.compile(r"&(?:#[0-9]{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});")
ESCAPE_RE = re.compile(r"\\(?=[\n!-/:-@\[-`{-~])")  # Escapes and hard breaks.
TAG_FRAGMENT_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*")

INLINE_MARKUP_RES = (TAG_RE, ENTITY_RE, ESCAPE_RE)


# Link tails and tag openers, closed or not, blanked in the loose reading.
LOOSE_MARKUP_RE = re.compile(
    r"\](?:\([^\s()]*\)?|\[[^\s\]]*\]?)|</?[A-Za-z][A-Za-z0-9-]*>?"
)

# An unclosed link tail, dropped in the stripped copies the way the
# loose reading blanks it.
LOOSE_TAIL_RE = re.compile(r"\](?:\([^\s()]*\)?|\[[^\s\]]*\]?)")


COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


# Emphasis, strong and strikethrough delimiters, soft hyphens and
# zero-width characters: deleted at any position, joining their
# neighbours the way rendering does (he**ld** renders "held").
_JOINER_CHARS = frozenset("*_~\u00ad\u200b\u200c\u200d\ufeff")

# Tags that render inline with no separation, so deleting them joins
# their neighbours ([he](x)ld and refer<b></b>ence render as one word).
# Every other tag (br, div, td, ...) separates and becomes a space.
INLINE_JOIN_TAGS = frozenset((
    "a", "abbr", "b", "bdi", "bdo", "cite", "code", "del", "dfn", "em",
    "i", "ins", "kbd", "mark", "q", "s", "samp", "small", "span",
    "strong", "sub", "sup", "time", "u", "var", "wbr",
))

# (keep closed-comment interiors as text, read link syntax literally).
_STRIP_READINGS = ((False, False), (False, True), (True, False), (True, True))

_INTERESTING_RE = re.compile(r"[*_~\u00ad\u200b\u200c\u200d\ufeff`\\\[\]&<]|-->")


def _normalize(text: str) -> str:
    text = text.translate(str.maketrans("\u2018\u2019\u201c\u201d\u2010\u2011\u2012\u2013\u2014\u2212", "''\"\"------"))
    return re.sub(r"\s+", " ", text).strip().lower()


def load_manifest_rows(repo_root: Path) -> "list[tuple[int, str, str]] | None":
    """(lineno, normalized, raw) for each manifest DATA row, or None."""
    path = repo_root / MANIFEST_PATH
    text = read_text_safe(path) if path.is_file() else None
    if text is None:
        return None
    rows: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        first = cells[0] if cells else ""
        if not first or first == "Title" or set(first) <= set("- :"):
            continue
        rows.append((lineno, _normalize(stripped), stripped))
    return rows


def _blank(text: str) -> str:
    """Spaces for every character except newlines, keeping offsets."""
    return re.sub(r"[^\n]", " ", text)


def _blank_matches(pattern: "re.Pattern[str]", text: str) -> str:
    return pattern.sub(lambda m: _blank(m.group()), text)


def _fence_opener(line: str):
    """(continuation regex, quoted, indent, run, interrupts) for a fence
    opener, or None.

    Leading quote and list markers become the prefix that every fenced
    line repeats; a list marker's width becomes required indentation.
    ``interrupts`` is False when an ordered marker other than 1 is in
    the prefix: that list cannot interrupt a paragraph, so under a
    non-blank line the opener is read as prose (fail closed).
    """
    parts: list[str] = []
    quoted, pos, interrupts = False, 0, True
    while True:
        m = FENCE_QUOTE_RE.match(line, pos)
        if m:
            parts.append(r" {0,3}> ?")
            quoted = True
        else:
            m = FENCE_LIST_RE.match(line, pos)
            if not m:
                break
            ordered = FENCE_ORDERED_RE.match(line, pos)
            if ordered and ordered.group(1) != "1":
                interrupts = False
            parts.append(" {%d}" % (m.end() - pos))
        pos = m.end()
    m = FENCE_RE.match(line, pos)
    if not m or (m.group(2)[0] == "`" and "`" in m.group(3)):
        return None
    return re.compile("".join(parts)), quoted, len(m.group(1)), m.group(2), interrupts


def _naive_comment_spans(text: str) -> "list[tuple[int, int]]":
    """Sequential closed <!-- ... --> spans, blind to code spans."""
    spans: list[tuple[int, int]] = []
    pos = 0
    while (start := text.find("<!--", pos)) >= 0:
        close = text.find("-->", start + 4)
        if close < 0:
            break
        spans.append((start, close + 3))
        pos = close + 3
    return spans


def _covering(spans, pos: int) -> bool:
    """True when a (start, end) span in the sorted list covers pos."""
    k = bisect.bisect_right(spans, (pos, sys.maxsize)) - 1
    return k >= 0 and spans[k][1] > pos


def _comment_covered_lines(lines: "list[str]") -> "set[int]":
    """Zero-based indices of lines lying wholly inside a closed comment.

    Those lines never open or close a fence: rendering reads them as
    comment text, so skipping code on their say-so could hide a claim.
    """
    text = "\n".join(lines)
    starts = [0] + [m.end() for m in re.finditer("\n", text)]
    covered: set[int] = set()
    for start, end in _naive_comment_spans(text):
        first = bisect.bisect_right(starts, start) - 1
        last = bisect.bisect_right(starts, end - 1) - 1
        for k in range(first, last + 1):
            if start < starts[k] and starts[k] + len(lines[k]) <= end:
                covered.add(k)
    return covered


def fenced_code_lines(lines: "list[str]", comment_lines=frozenset()) -> "set[int]":
    """Zero-based indices of the lines of closed fenced code blocks.

    A fence closes only on a matching fence line that arrives before any
    line leaves the opener's prefix or is indented less than the opener.
    Otherwise the opener is read as prose, so a misread fence can add
    findings but cannot hide a claim. Lines inside closed comments and
    non-interrupting ordered openers under a non-blank line never fence.
    """
    lines = [line.expandtabs(4) for line in lines]
    code: set[int] = set()
    i = 0
    while i < len(lines):
        opened = None if i in comment_lines else _fence_opener(lines[i])
        if opened is None:
            i += 1
            continue
        prefix_re, quoted, indent, run, interrupts = opened
        if not interrupts and i > 0 and lines[i - 1].strip() and (i - 1) not in code:
            i += 1
            continue
        closer = re.compile(r" {0,3}" + re.escape(run[0]) + "{%d,}[ \t]*$" % len(run))
        j, closed = i + 1, False
        while j < len(lines):
            m = prefix_re.match(lines[j])
            if m is None and (quoted or lines[j].strip()):
                break
            rest = lines[j][m.end():] if m else ""
            if closer.match(rest) and j not in comment_lines:
                closed = True
                break
            if rest.strip() and len(rest) - len(rest.lstrip(" ")) < indent:
                break
            j += 1
        if closed:
            code.update(range(i, j + 1))
            i = j + 1
        else:
            i += 1
    return code


def _tail_end(text: str, i: int) -> "int | None":
    """Offset just past the link tail opening at text[i] == "]", or None
    when the tail stays open at a blank line or the end of the text. A
    tail must follow its "]" directly, as CommonMark requires. Balanced
    parentheses, angle destinations, quoted titles and escapes are
    handled.
    """
    opener = text[i + 1]
    closer = ")" if opener == "(" else "]"
    depth, j, quote = 1, i + 2, ""
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "\n" and BLANK_LINE_RE.match(text, j):
            return None
        if quote:
            if c == quote:
                quote = ""
        elif opener == "(" and c == "<":
            quote = ">"
        elif opener == "(" and c in "\"'" and text[j - 1].isspace():
            quote = c
        elif c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if not depth:
                return j + 1
        j += 1
    return None


def _mask_link_tails(text: str) -> str:
    """Blank closed inline link tails and reference labels, keeping
    offsets and newlines; a tail left open stays unchanged."""
    chars = list(text)
    i = 0
    while i < len(text) - 1:
        if text[i] != "]" or text[i + 1] not in "([":
            i += 1
            continue
        end = _tail_end(text, i)
        if end is None:
            i += 1
        else:
            chars[i + 1:end] = _blank(text[i + 1:end])
            i = end
    return "".join(chars)


def readings(text: str) -> "tuple[str, ...]":
    """Offset-preserving readings of the text; each is searched for claims."""
    prefixed = _blank_matches(LINE_PREFIX_RE, text)
    linked = _mask_link_tails(prefixed)
    inline = linked
    for markup_re in INLINE_MARKUP_RES:
        inline = _blank_matches(markup_re, inline)
    loose = _blank_matches(LOOSE_MARKUP_RE, inline)
    return (prefixed, linked, inline, loose, _blank_matches(COMMENT_RE, loose))


def _code_span_intervals(text: str, excluded) -> "list[tuple[int, int]]":
    """(start, end) content intervals of code spans paired between blank
    lines, ignoring backtick runs inside closed comments (excluded)."""
    intervals: list[tuple[int, int]] = []
    bounds = [0]
    for m in BLANK_LINE_RE.finditer(text):
        bounds.extend((m.start(), m.end()))
    bounds.append(len(text))
    for k in range(0, len(bounds), 2):
        opened = None
        for run in BACKTICK_RUN_RE.finditer(text, bounds[k], bounds[k + 1]):
            if _covering(excluded, run.start()):
                continue
            if opened is None:
                opened = run
            elif len(run.group()) == len(opened.group()):
                intervals.append((opened.end(), run.start()))
                opened = None
    return intervals


def _comment_spans(text: str, code_intervals) -> "list[tuple[int, int]]":
    """Comment spans whose opener sits outside a paired code span; an
    unclosed opener is recorded with end -1."""
    spans: list[tuple[int, int]] = []
    pos = 0
    while (start := text.find("<!--", pos)) >= 0:
        if _covering(code_intervals, start):
            pos = start + 4
            continue
        close = text.find("-->", start + 4)
        if close < 0:
            spans.append((start, -1))
            break
        spans.append((start, close + 3))
        pos = close + 3
    return spans


def _strip_copies(text: str) -> "list[tuple[str, list[int]]]":
    """(stripped text, source-offset map) per stripping reading.

    Four readings: closed-comment interiors dropped or kept as text,
    crossed with link syntax resolved (visible text kept; destination,
    title or label dropped, neighbours joined) or read literally (the
    label may not resolve, so bracket characters become separators).
    """
    naive = _naive_comment_spans(text)
    code_intervals = _code_span_intervals(text, naive)
    comments = _comment_spans(text, code_intervals)
    return [_strip(text, code_intervals, comments, keep, literal)
            for keep, literal in _STRIP_READINGS]


def _strip(text, code_intervals, comments, keep_interior, literal_links):
    openers = dict(comments)
    closers = set(end - 3 for _, end in comments if end >= 0)
    out: list[str] = []
    cmap: list[int] = []

    def emit(piece: str, src: int) -> None:
        for ch in piece.casefold():
            out.append(ch)
            cmap.append(src)

    def emit_span(a: int, b: int) -> None:
        piece = text[a:b]
        if piece.isascii():
            out.extend(piece.lower())
            cmap.extend(range(a, b))
        else:
            for k in range(a, b):
                emit(text[k], k)

    i, n = 0, len(text)
    while i < n:
        m = _INTERESTING_RE.search(text, i)
        if m is None:
            emit_span(i, n)
            break
        if m.start() > i:
            emit_span(i, m.start())
            i = m.start()
        c = text[i]
        if c in _JOINER_CHARS:
            i += 1
            continue
        if c == "\\":
            if ESCAPE_RE.match(text, i):
                i += 1
            else:
                emit("\\", i)
                i += 1
            continue
        if c == "`":
            while i < n and text[i] == "`":
                i += 1
            continue
        if c == "&":
            em = ENTITY_RE.match(text, i)
            if em:
                emit(html.unescape(em.group()), i)
                i = em.end()
            else:
                emit("&", i)
                i += 1
            continue
        if _covering(code_intervals, i):
            emit(c, i)
            i += 1
            continue
        if c == "<":
            if i in openers:
                end = openers[i]
                if end >= 0 and not keep_interior:
                    i = end
                else:
                    i += 4
                continue
            tm = TAG_RE.match(text, i)
            if tm:
                if tm.group(1).lower() not in INLINE_JOIN_TAGS:
                    emit(" ", i)
                i = tm.end()
                continue
            tm = TAG_FRAGMENT_RE.match(text, i)
            if tm:
                emit(" ", i)
                i = tm.end()
                continue
            emit("<", i)
            i += 1
            continue
        if c == "-":  # only "-->" reaches here
            if i in closers:
                i += 3
            else:
                emit_span(i, i + 3)
                i += 3
            continue
        if c == "[":
            if literal_links:
                emit(" ", i)
            i += 1
            continue
        # c == "]"
        if literal_links:
            emit(" ", i)
            i += 1
            continue
        if i + 1 < n and text[i + 1] in "([":
            end = _tail_end(text, i)
            if end is None:
                end = LOOSE_TAIL_RE.match(text, i).end()
            i = end
            continue
        i += 1
    return "".join(out), cmap


def canonical_claims(views, copies) -> "list[tuple[int, int]]":
    """Source (start, end) of every canonical claim found in any blanked
    reading or stripped copy. Matches sharing a start keep the earliest
    end (min, not max): a marker satisfies the claim only on a line in
    the shortest reading's span, so no reading is left unsatisfied. The
    min is load-bearing; see the reading-bounds regression test.
    """
    ends: dict[int, int] = {}

    def add(start: int, end: int) -> None:
        ends[start] = min(end, ends.get(start, end))

    for view in views:
        for m in CANONICAL_RE.finditer(view):
            add(m.start(), m.end())
    for stripped, cmap in copies:
        for m in CANONICAL_STRIPPED_RE.finditer(stripped):
            add(cmap[m.start()], cmap[m.end() - 1] + 1)
    return sorted(ends.items())


def _code_span_state(text: str, pos: int) -> str:
    """"unpaired" if a backtick run between the blank lines around pos stays
    open, "code" if pos lies inside a code span paired there, else "".
    Backtick runs inside closed comments never pair as code spans."""
    excluded = _naive_comment_spans(text)
    start = 0
    for blank in BLANK_LINE_RE.finditer(text, 0, pos):
        start = blank.end()
    blank = BLANK_LINE_RE.search(text, pos)
    opened = None
    inside = False
    for run in BACKTICK_RUN_RE.finditer(text, start, blank.start() if blank else len(text)):
        if _covering(excluded, run.start()):
            continue
        if opened is None:
            opened = run
        elif len(run.group()) == len(opened.group()):
            inside = inside or opened.start() < pos < run.start()
            opened = None
    if opened is not None:
        return "unpaired"
    return "code" if inside else ""


def find_markers(text: str) -> "list[tuple[int, int, str, str]]":
    """(start, end, queries, problem) for each marker opening.

    A problem makes the marker malformed. A marker inside a paired code
    span is example text and is not returned.
    """
    markers: list[tuple[int, int, str, str]] = []
    pos = 0
    while (m := MARKER_OPEN_RE.search(text, pos)):
        close = text.find("-->", m.end())
        problem = ""
        if close < 0:
            problem = "the comment is never closed"
        elif BLANK_LINE_RE.search(text, m.start(), close):
            problem = "the comment is not closed before a blank line"
        elif "<!--" in text[m.start() + 4:close]:
            problem = "the comment contains another comment opener"
        else:
            state = _code_span_state(text, m.start())
            if state == "code":
                pos = close + 3
                continue
            if state == "unpaired":
                problem = ("an unpaired backtick run shares its text between "
                           "blank lines, so it may sit inside a code span")
        if problem:
            markers.append((m.start(), m.end(), "", problem))
            pos = m.end()
        else:
            markers.append((m.start(), close + 3, text[m.end():close], ""))
            pos = close + 3
    return markers


def near_miss_hits(text: str, canonical_spans) -> "list[tuple[int, str]]":
    """(offset, snippet) for near-miss triggers, canonical matches excluded."""
    hits = []
    seen: set[tuple[int, int]] = set()
    for trigger_re in TRIGGER_RES:
        for m in trigger_re.finditer(text):
            if (m.start(), m.end()) in seen:
                continue
            if any(m.start() < end and m.end() > start for start, end in canonical_spans):
                continue
            if HELD_VERB_RE.search(m.group(0)):
                context = NEAR_MISS_CONTEXT_RE
            else:
                before_text = text[: m.start()]
                if HELD_TEXT_OBJECT_RE.match(text[m.end():]):
                    continue
                if (HELD_TEXT_SUBJECT_RE.search(before_text)
                        and not COLLECTION_POSSESSED_SUBJECT_RE.search(before_text)):
                    continue
                context = NEAR_MISS_COLLECTION_CONTEXT_RE
            before = " ".join(text[: m.start()].split()[-NEAR_MISS_WINDOW_TOKENS:])
            after = " ".join(text[m.end():].split()[:NEAR_MISS_WINDOW_TOKENS])
            window = " ".join(part for part in (before, m.group(0), after) if part)
            if context.search(window):
                hits.append((m.start(), m.group(0)))
                seen.add((m.start(), m.end()))
    hits.sort()
    return hits


def scan_text(rel: str, text: str, manifest_rows) -> "list[str]":
    """Findings for one file; each claim's marker opens on its own lines."""
    findings: list[str] = []
    lines = text.split("\n")
    code = fenced_code_lines(lines, _comment_covered_lines(lines))
    body = "\n".join("" if i in code else line for i, line in enumerate(lines))
    starts = [0] + [m.end() for m in re.finditer("\n", body)]

    def line_at(offset: int) -> int:
        return bisect.bisect_right(starts, offset)

    markers: list[tuple[int, str]] = []
    for start, end, queries, problem in find_markers(body):
        if problem:
            findings.append(
                f"{rel}:{line_at(start)}: malformed ref-absence marker: "
                f"{problem}, so it satisfies no claim"
            )
            continue
        markers.append((line_at(start), queries))
        body = body[:start] + _blank(body[start:end]) + body[end:]
    body = body.replace("\u2019", "'").replace("\u2018", "'")
    views = readings(body)
    claims = [(line_at(start), line_at(end - 1), start, end)
              for start, end in canonical_claims(views, _strip_copies(views[0]))]
    absence = [(first, last) for first, last, _, _ in claims]
    for trigger_re in ANNOTATABLE_TRIGGER_RES:
        absence.extend((line_at(m.start()), line_at(m.end() - 1))
                       for m in trigger_re.finditer(views[1]))
    for offset, snippet in near_miss_hits(views[1], [(s, e) for _, _, s, e in claims]):
        findings.append(
            f"ADVISORY: {rel}:{line_at(offset)}: non-canonical reference-absence phrasing "
            f"({snippet!r}): use the canonical 'not held in the reference "
            f"base' sentence with a <!-- ref-absence: ... --> marker on "
            f"the claim's own line so the claim is machine-checkable"
        )
    # Taking claims by last line, each with the earliest free marker on its
    # lines, is a maximum matching for these ordered line ranges.
    used: set[int] = set()
    for first, last, _, _ in sorted(claims, key=lambda claim: (claim[1], claim[0])):
        on_lines = [k for k, (line, _) in enumerate(markers) if first <= line <= last]
        free = [k for k in on_lines if k not in used]
        if free:
            used.add(free[0])
            continue
        span = f"line {first}" if first == last else f"lines {first}-{last}"
        shortfall = (
            f" ({len(on_lines)} marker(s) on those lines already cover other "
            f"claims; each claim carries its own marker)"
            if on_lines else ""
        )
        findings.append(
            f"{rel}:{first}: canonical reference-absence claim ({span}) has no "
            f"<!-- ref-absence: query1 | query2 --> marker on its own lines "
            f"naming the claimed-absent source" + shortfall
        )
    for lineno, queries_text in markers:
        if not any(first <= lineno <= last for first, last in absence):
            findings.append(
                f"{rel}:{lineno}: orphan ref-absence marker: no reference-"
                f"absence claim spans this line"
            )
        queries = [q.strip() for q in queries_text.split("|")]
        if not any(queries):
            findings.append(
                f"{rel}:{lineno}: malformed ref-absence marker: no query "
                f"(expected <!-- ref-absence: query1 | query2 -->)"
            )
            continue
        for query in queries:
            if not query:
                findings.append(
                    f"{rel}:{lineno}: malformed ref-absence marker: empty "
                    f"alternative in the query list"
                )
                continue
            needle = _normalize(query)
            for row_lineno, normalized, raw in manifest_rows:
                if needle in normalized:
                    findings.append(
                        f"{rel}:{lineno}: STALE reference-absence claim: "
                        f"marker query {query!r} matches "
                        f"{MANIFEST_PATH}:{row_lineno}, so the reference "
                        f"index says this source IS held: {raw[:200]}"
                    )
                    break
    return findings


def scan_file(path: Path, manifest_rows) -> "list[str]":
    text = read_text_safe(path)
    if text is None:
        return []
    rel = path.relative_to(REPO_ROOT).as_posix() if path.is_absolute() else path.as_posix()
    return scan_text(rel, text, manifest_rows)


def iter_markdown_files(paths: "list[str]") -> "list[Path]":
    """The scan-scope selector, module-level so the scan-scope regression's
    ALLOW map can exercise it (as lint-roles.py keeps its own)."""
    return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)


def main(argv: "list[str]") -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reference-absence claims carry ref-absence markers whose queries "
            "stay absent from the committed reference-acquisition manifest."
        ),
    )
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])
    manifest_rows = load_manifest_rows(REPO_ROOT)
    if manifest_rows is None or not manifest_rows:
        print(
            f"ERROR: cannot read any data rows from {MANIFEST_PATH}; the "
            f"committed manifest is this gate's staleness source "
            f"(regenerate with tools/build-reference-manifest.py).",
            file=sys.stderr,
        )
        return 2
    paths = guard_explicit_paths(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    files = [
        f for f in iter_markdown_files(paths)
        if f.relative_to(REPO_ROOT).as_posix() not in EXEMPT_FILES
    ]
    findings: list[str] = []
    for f in files:
        findings.extend(scan_file(f, manifest_rows))
    for finding in findings:
        print(finding)
    blocking = sum(not finding.startswith("ADVISORY: ") for finding in findings)
    if blocking:
        print(f"\n{blocking} blocking reference-absence finding(s).")
        return 1
    print(f"OK: no blocking reference-absence findings across {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
