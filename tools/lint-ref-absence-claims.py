#!/usr/bin/env python3
"""Reference-absence claim audit, using the tracked acquisition manifest.

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
or books. Staleness is observable only once the manifest is regenerated;
the gate reads the working-tree file (under a `git commit` pre-commit run,
the staged content of tracked files),
and the sibling reference repository is never read. The advisory
heuristics cannot reliably infer semantics; missing-content wordings are
distinguished from missing-source wordings only by the documented token
windows. The audit specification records those residues.

A blocking obfuscation screen (3b144, rounds 14 to 16) backs the
readings: the canonical claim's words found in token order where no
reading detects a claim. The screen's readable subset is small:
letters grouped into words, whitespace, plain sentence punctuation
(commas, periods, semicolons, colons, question and exclamation
marks, apostrophes, quotation marks, parentheses, hyphens, dashes
and ellipses), tags and entities matched by the screen's loose
patterns, backslash escapes and ref-absence markers (each blanked
before tokenizing), and
closed link tails (blanked up to their first whitespace; a
destination does not render). An unclosed link tail keeps its text,
which renders as prose, and only its "](" or "][" is blanked, and
closed link tails are never masked across whitespace, so neither
broken nor prose-swallowing link syntax can erase the words the
screen checks. Tokens are the letter runs of that reading. A word
may be read from up to four consecutive tokens, skipping letters
only across a gap the screen cannot read; up to three junk tokens
may sit before each later word; and the matcher backtracks over
junk counts and over taking or skipping the optional words. Each
of the following constructs, in or between the matched words, is
itself a finding ("unreadable markup around a possible
reference-absence claim; write the sentence plainly"), never a
silent pass and never an advisory downgrade: a claim word split or
partly erased across unreadable gaps; keyword letters a closed link
tail would swallow; an unclosed link tail between claim words;
markup debris ("<", ">", "&", a backslash or a caret), a footnote
or superscript digit mark, an invisible or format character, or a
blank-rendering filler character between claim words (a plain ASCII
digit alone is readable prose); or a bracket beside junk tokens or
a numeric mark between claim words. A plain-prose paraphrase
such as "not yet held in the reference base" carries none of these
and stays advisory; a markup-laced paraphrase, or a positive
holding statement laced with markup, can be falsely blocked, the
fail-closed direction this gate prefers, and is resolved on review
by rewriting the sentence plainly. Other visible characters
between claim words (a slash, a pipe, a symbol, an emoji) are
readable prose to the screen; the permissive reader below refuses
them when they hide the claim phrase. A bidirectional override or
isolate control (U+202A-U+202E, U+2066-U+2069, literal or as an
entity) or a <bdo> element anywhere in a scanned line is a blocking
finding naming its line: it can display letters in an order other
than the logical order every reading scans.

A permissive hidden-claim reader (3b144 round 16) is the second
half of a two-reader design, in which the readings and the screen
are the strict reader. Each paragraph is also normalized
permissively: closed comments, images, closing link tails that
CommonMark closes while a link opener is open (an angle-bracket or
whitespace-free destination with an optional quoted title, or a
reference label) and inline tags well-formed under the CommonMark
attribute grammar are blanked; entities that decode are decoded;
ASCII letters and digits are kept and case-folded; combining,
format and control characters (Unicode categories Mn, Cf and Cc,
except whitespace) and default-ignorable code points (including
unassigned ones and the Hangul fillers) are deleted and join their
neighbours, so a split word rejoins; and every other character
(whitespace, delimiters, visible punctuation, symbols, emoji,
non-ASCII letters and digits) reads as a word separator, collapsed
to one space. Each paragraph is read twice, once with images
blanked and once with each image read as its alt text (a Markdown
image's alt text or an <img> tag's alt value, with unescaped
emphasis, strong and strikethrough delimiters and code-span
backticks deleted from a Markdown alt text, as the strict readings
delete them elsewhere). Where the body has a non-rendering element
(<rp>, <template>, <script>, <style>, <noscript>, or any element
with the hidden attribute or an inline display:none), each of those
readings is also made with the element deleted, content included,
to its closing tag or the paragraph's end, so its neighbours join.
Each reading's paragraphs are joined with a separator for every
paragraph break, so a claim split across a paragraph break is read
too. Where that
normalization spells the canonical claim and no detected claim's
span and no screen finding covers the spelled claim's start, the
text is refused ("possible hidden claim"), never read silently.
Ordinary prose with emoji, curly quotes or accents is therefore
never flagged unless it spells the claim phrase the strict reader
misses.

Residue, shipped under the maintainer rulings of 2026-09-30 22:49Z
and 23:04Z and narrowed by the 3b144 obfuscation screen and its
round-16 permissive reader: detection
does not fail closed in general. The first paragraph's "fails
closed" and the second paragraph's "cannot hide one" and "keeps the
claim text visible" state the design intent, not a guarantee. The
screen catches the round-14 escapes (a quoted attribute holding ">"
or "<", a tag outside INLINE_JOIN_TAGS or a well-formed marker
splitting a claim word; an entity-encoded or literal soft hyphen,
zero-width character, word joiner U+2060, combining grapheme joiner
U+034F or variation selector inside a word; an unmatched backtick
making a code-span link opener swallow a later linked claim; and an
unclosed link title or tag attribute leaving its text between the
words) and the round-15 escapes (a link tail swallowing prose
through an angle destination or a quoted title with no unpaired
backtick nearby; punctuation-only attribute debris between claim
words; an unclosed link tail erasing a claim word; an invisible,
format or blank-rendering filler character beside a claim word,
including the braille blank U+2800 and the fillers U+3164, U+115F
and U+1160; a numeric footnote or superscript digit beside a claim
word; letters erased inside a claim word by entity blanking; and
the greedy misreads of the optional words). The round-16
permissive reader catches the screen's second review round: an
image rendering no text between claim words; an invisible Mn
character (a variation selector outside U+FE00-U+FE0F, a Mongolian
free variation selector, a Khmer inherent vowel) beside a claim
word; a malformed tag or an undecodable entity, which renders as
text, erased by the screen's looser blanking; an invalid link
tail's rendered prose erased by tail masking; a claim word's
leading or trailing letters erased by entity blanking; a detected
claim inside an attribute suppressing the refusal on the claim
around it; and visible separators (a slash, a hyphen, a comma)
spelling the claim that no reading matches. After the screen's
third review round it also catches a claim word in an image's alt
text (inline, reference-style or an <img> tag's alt value); a word
split into five or more parts by default-ignorable code points,
including unassigned ones (U+2065, U+FFF0-U+FFF8, U+E0000-U+E0FFF)
and the Hangul fillers U+115F, U+1160, U+3164 and U+FFA0; and a
claim split across a paragraph break with an image, a selector, a
visible separator or a thematic break beside the break. After the
fourth round it also catches letters inside a non-rendering element
splitting a claim word and emphasis inside an image's alt text, and
the screen refuses bidirectional overrides and isolates. Still open:
a claim word split by well-formed tags into more pieces than the
four-part and three-junk budgets together can reach, because the
permissive reading reads a blanked tag as a word separator and
does not rejoin the word. Letters reversed by inline CSS
(unicode-bidi: bidi-override) rather than a control character or
<bdo>, and an element hidden by a class or stylesheet rule rather
than by its name, the hidden attribute or an inline display:none,
are not recognized. A letter homoglyph, such as a Cyrillic
letter shaped like a Latin one or a fullwidth or mathematical
letter, or a blank-rendering character of letter category outside
the default-ignorable set, reads as a different word in every
reading, in the screen and in the permissive reading, which reads
a non-ASCII letter as a separator. The strict reader still reads
link titles, image alt text, comments and tag attribute values, so
a claim spelled there in plain words is detected; the permissive
reader blanks inline link and image titles, comments and tag
attribute values, reads a reference definition line, destination
and title included, as text, and, in its alt-text reading, also
reads alt text. Plain words in an angle-bracket inline destination
are read by the strict reader, which keeps destination text in
some readings, so a claim spelled there is detected. A claim
spelled only in a whitespace-free inline link or image destination,
its words joined by hyphens, slashes or similar, is not read and
carries no finding, and neither is one spelled with visible
separators, such as hyphens, only in a comment or a tag attribute
value. A permissive claim whose
spelled start lies inside a detected claim's span or a screen
finding's span is attributed to that claim or finding; and
a plain sentence whose words spell the canonical claim across
sentence punctuation ("not. Held in the reference base") is
refused, the fail-closed direction this gate prefers, resolved by
rewriting the sentence plainly. Escaped backticks, or backticks
paired across list items, headings, table cells, link destinations
or attribute values, form a false code span that can keep an
in-word comment literal; the in-word link and tag variants split
the word and are blocked. A "<!--" in a code span or fenced block
can pair with a later "-->", so a real fence line counts as
comment-covered and fences pair wrongly. A fence line inside a raw
HTML block pairs with a later fence. The remaining shapes stay
tracked on the backlog under item 3b144's follow-up; the audit
specification states the same narrowed residue.

Usage: python3 tools/lint-ref-absence-claims.py [path ...]
Exit: 0 no blocking findings; 1 blocking findings; 2 invalid inputs.
"""

from __future__ import annotations

import argparse
import bisect
import html
import re
import sys
import unicodedata
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


# ---- Obfuscation screen (3b144) -------------------------------------
# A blocking keyword rule behind the readings: the canonical claim's
# words found in token order where no reading detects a claim. The
# screen fails closed on markup it cannot read exactly: any such
# construct in or between the matched words is a finding, never a
# silent pass and never an advisory downgrade. A plain-prose paraphrase
# such as "not yet held in the reference base" stays advisory under the
# 2026-09-30 00:57Z/14:05Z ruling.

SCREEN_FILLER_CHARS = frozenset("\u2800\u3164\u115f\u1160")
SCREEN_LETTER_FILLER_RE = re.compile("[\u3164\u115f\u1160]")
SCREEN_TAG_OPENER_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*>?")
SCREEN_TOKEN_RE = re.compile(r"[^\W\d_]+")
SCREEN_SEQUENCE = (("not",), ("currently",), ("held",), ("in",),
                   ("the", "our"), ("reference",), ("base", "library"))
SCREEN_OPTIONAL = frozenset((1, 4))  # currently; the|our
SCREEN_MAX_JUNK = 3
SCREEN_MAX_PARTS = 4

# The punctuation the screen reads as plain prose around claim words.
SCREEN_PLAIN_PUNCT = frozenset(
    ",.;:!?'\"()\u2018\u2019\u201c\u201d-\u2010\u2011\u2013\u2014\u2026")


def _screen_unreadable_char(c: str) -> bool:
    """A character the screen refuses between claim words: markup debris
    ("<", ">", "&", a backslash or a caret), a non-ASCII numeric
    character (a superscript digit beside a claim word), an invisible
    or format character, a variation selector or combining grapheme
    joiner, or a blank-rendering filler (the braille blank or a Hangul
    filler). A plain ASCII digit alone is readable prose; one beside a
    bracket is a footnote or reference mark and is refused in
    _screen_evidence."""
    return (c in "<>&\\^" or (c.isnumeric() and not c.isascii())
            or c in SCREEN_FILLER_CHARS
            or "\ufe00" <= c <= "\ufe0f" or c == "\u034f"
            or unicodedata.category(c) == "Cf")


def _screen_gap_unreadable(body, marker_spans, a, b) -> bool:
    """True when body[a:b], the source gap between two token parts,
    holds anything beyond whitespace and plain sentence punctuation, or
    overlaps a blanked ref-absence marker (a well-formed marker
    splitting a claim word hides it from every reading)."""
    if any(not c.isspace() and c not in SCREEN_PLAIN_PUNCT for c in body[a:b]):
        return True
    return any(ms < b and me > a for ms, me in marker_spans)


def _screen_view(prefixed: str) -> str:
    """The screen's reading: well-formed inline tags, entities and
    escapes blanked, blank-rendering filler letters and non-ASCII
    numeric characters (a superscript digit reads as a word letter)
    blanked, tag openers blanked, and closed link tails blanked up to
    their first whitespace (a destination does not render). An
    unclosed link tail keeps its text, which renders as prose, and
    only its "](" or "][" is blanked; closed link tails are never
    masked across whitespace.
    So neither broken nor prose-swallowing link syntax can erase the
    words the screen checks."""
    view = prefixed
    for markup_re in INLINE_MARKUP_RES:
        view = _blank_matches(markup_re, view)
    view = _blank_matches(SCREEN_LETTER_FILLER_RE, view)
    if any(c.isnumeric() and not c.isascii() for c in view):
        view = "".join(" " if c.isnumeric() and not c.isascii() else c
                       for c in view)
    view = _blank_matches(SCREEN_TAG_OPENER_RE, view)
    chars = list(view)
    i = 0
    while i < len(view) - 1:
        if view[i] != "]" or view[i + 1] not in "([":
            i += 1
            continue
        if _tail_end(prefixed, i) is None:
            chars[i] = chars[i + 1] = " "
            i += 2
        else:
            end = LOOSE_TAIL_RE.match(view, i).end()
            chars[i:end] = " " * (end - i)
            i = end
    return "".join(chars)


def _screen_keyword(body, marker_spans, tokens, i, words):
    """(index past the last token used, split evidence) for the tokens
    reading as one of words from token i, or None. A word may be read
    from up to SCREEN_MAX_PARTS consecutive tokens (he + ld reads
    "held", the way rendering joins a split word). Letters erased from
    the screen's reading (a blanked entity or marker) may be skipped
    after the first part, but only across a gap the screen cannot
    read. A multi-part word is evidence only when an unreadable gap
    joins it, so plain prose such as "no T held" carries no evidence."""
    for word in words:
        pos, split = 0, False
        for j in range(i, min(i + SCREEN_MAX_PARTS, len(tokens))):
            part = tokens[j][0]
            if j == i:
                k = 0 if word.startswith(part) else -1
            else:
                k = word.find(part, pos)
            if k < 0:
                break
            if j > i:
                unreadable = _screen_gap_unreadable(
                    body, marker_spans, tokens[j - 1][2], tokens[j][1])
                if k > pos and not unreadable:
                    break
                split = split or unreadable or k > pos
            pos = k + len(part)
            if pos == len(word):
                return j + 1, split
    return None


def _screen_sequence(body, marker_spans, tokens, start):
    """(first, past-last, split) token ranges per matched keyword for
    the canonical word sequence anchored at tokens[start], or None. Up
    to SCREEN_MAX_JUNK junk tokens may sit before each later keyword.
    The search backtracks over junk counts and over taking or skipping
    the optional words, so one greedy choice cannot hide a match."""

    def solve(k, idx):
        if k == len(SCREEN_SEQUENCE):
            return []
        for junk in range((SCREEN_MAX_JUNK if idx > start else 0) + 1):
            if idx + junk >= len(tokens):
                break
            found = _screen_keyword(body, marker_spans, tokens, idx + junk,
                                    SCREEN_SEQUENCE[k])
            if found is not None:
                rest = solve(k + 1, found[0])
                if rest is not None:
                    return [(idx + junk, found[0], found[1])] + rest
        return solve(k + 1, idx) if k in SCREEN_OPTIONAL else None

    return solve(0, start)


def _gap_unclosed_tail(body, a, b) -> bool:
    """An unclosed inline link tail or reference label opening inside
    body[a:b]: its text renders as prose between the claim words."""
    for g in range(a, b - 1):
        if body[g] == "]" and body[g + 1] in "([" and _tail_end(body, g) is None:
            return True
    return False


def _screen_evidence(body, screen, linked, tokens, ranges) -> bool:
    """Unreadable markup for a matched sequence: a claim word split or
    partly erased across unreadable gaps; keyword letters erased by
    link-tail masking (a closed tail swallowing prose); or, in a gap
    between claim words, an unclosed link tail, an unreadable character
    (markup debris, a superscript digit, an invisible or format
    character, a blank-rendering filler) or a bracket beside junk
    tokens or a numeric footnote or reference mark. Any of these is a
    finding, never a silent pass."""
    if any(split for _, _, split in ranges):
        return True
    offsets = [o for a, b, _ in ranges
               for o in range(tokens[a][1], tokens[b - 1][2])]
    if any(screen[o].isalpha() and linked[o] != screen[o] for o in offsets):
        return True
    for (_, pb, _), (na, _, _) in zip(ranges, ranges[1:]):
        a, b = tokens[pb - 1][2], tokens[na][1]
        gap = body[a:b]
        if any(_screen_unreadable_char(c) for c in gap):
            return True
        if (("[" in gap or "]" in gap)
                and (na > pb or any(c.isnumeric() for c in gap))):
            return True
        if _gap_unclosed_tail(body, a, b):
            return True
    return False


# Bidirectional override and isolate controls (U+202A-U+202E,
# U+2066-U+2069), literal or entity-encoded, and the <bdo> element:
# each can display a line's letters in an order other than the logical
# order every reading scans ("ton dleh" displayed as "held not").
SCREEN_BIDI_RE = re.compile("[\u202a-\u202e\u2066-\u2069]")
SCREEN_BDO_RE = re.compile(r"<bdo(?![A-Za-z0-9-])", re.IGNORECASE)


def bidi_control_offsets(body: str) -> "list[int]":
    """Source offsets of bidirectional override or isolate controls
    (literal or as a decoding entity) and <bdo> tags in the body."""
    offsets = [m.start() for m in SCREEN_BIDI_RE.finditer(body)]
    offsets += [m.start() for m in SCREEN_BDO_RE.finditer(body)]
    offsets += [m.start() for m in ENTITY_RE.finditer(body)
                if SCREEN_BIDI_RE.search(html.unescape(m.group()))]
    return sorted(offsets)


def obfuscated_claim_hits(body, screen, linked, claim_spans,
                          marker_spans) -> "list[tuple[int, int]]":
    """Source (start, end) spans where the canonical claim's words appear
    in order with unreadable markup and no reading detects a claim."""
    tokens = [(m.group().casefold(), m.start(), m.end())
              for m in SCREEN_TOKEN_RE.finditer(screen)]
    hits: "list[tuple[int, int]]" = []
    i = 0
    while i < len(tokens):
        ranges = _screen_sequence(body, marker_spans, tokens, i)
        if ranges is None:
            i += 1
            continue
        start = tokens[ranges[0][0]][1]
        end = tokens[ranges[-1][1] - 1][2]
        if any(start < ce and end > cs for cs, ce in claim_spans):
            i = ranges[-1][1]
            continue
        if _screen_evidence(body, screen, linked, tokens, ranges):
            hits.append((start, end))
            i = ranges[-1][1]
        else:
            i += 1
    return hits


# ---- Permissive hidden-claim reader (3b144 round 16) -----------------
# The second reader of the two-reader design: the readings and the
# screen above are the strict reader (what the gate already treats as
# readable text). This reader normalizes each paragraph permissively,
# joins the paragraphs with a separator for each paragraph break, and
# refuses wherever the normalization spells the canonical claim at
# a place where no reading detects a claim and the screen raises
# nothing. Ordinary prose with emoji, curly quotes or accents is never
# flagged unless it actually spells the claim phrase the strict reader
# misses.

# A well-formed inline tag under the CommonMark attribute grammar.
# TAG_RE above is looser on purpose for the blanked readings; here a
# malformed tag must stay text, because CommonMark renders it as text.
_PERMISSIVE_ATTR = (r"[A-Za-z_:][A-Za-z0-9_.:-]*"
                    r"(?:\s*=\s*(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?")
PERMISSIVE_TAG_RE = re.compile(
    r"<[A-Za-z][A-Za-z0-9-]*(?:\s+" + _PERMISSIVE_ATTR + r")*\s*/?>"
    r"|</[A-Za-z][A-Za-z0-9-]*\s*>")

# A link tail that CommonMark actually closes: an angle-bracket or
# whitespace-free destination (one parenthesis nesting level) with an
# optional quoted title, or a reference label. LOOSE_TAIL_RE above
# blanks up to the first whitespace; here a tail that does not parse
# stays text, because its prose renders.
_PERMISSIVE_DEST = (r"(?:<[^<>\n]*>"
                    r"|[^\s()]*(?:\([^\s()]*\)[^\s()]*)*)")
_PERMISSIVE_TITLE = r"(?:\"[^\"]*\"|'[^']*'|\([^()]*\))"
_PERMISSIVE_TAIL = (r"(?:\(\s*" + _PERMISSIVE_DEST
                    + r"(?:\s+" + _PERMISSIVE_TITLE + r")?\s*\)"
                    + r"|\[[^\[\]]*\])")
PERMISSIVE_TAIL_RE = re.compile(r"\]" + _PERMISSIVE_TAIL)
PERMISSIVE_IMAGE_RE = re.compile(r"!\[[^\[\]]*\]" + _PERMISSIVE_TAIL)

# One attribute of a PERMISSIVE_TAG_RE tag, and the tag's name, so the
# alt-text reading can keep an <img> tag's alt value.
_PERMISSIVE_ATTR_RE = re.compile(
    r"\s+([A-Za-z_:][A-Za-z0-9_.:-]*)"
    r"(?:\s*=\s*([^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?")
_PERMISSIVE_TAG_NAME_RE = re.compile(r"<([A-Za-z][A-Za-z0-9-]*)")

# Unicode Default_Ignorable_Code_Point (DerivedCoreProperties.txt),
# including its unassigned ranges and the Hangul fillers U+115F, U+1160,
# U+3164 and U+FFA0: renderers draw these invisibly, so the permissive
# reading deletes them and their neighbours join.
PERMISSIVE_IGNORABLE_RE = re.compile(
    "[\u00ad\u034f\u061c\u115f\u1160\u17b4\u17b5\u180b-\u180f"
    "\u200b-\u200f\u202a-\u202e\u2060-\u206f\u3164\ufe00-\ufe0f"
    "\ufeff\uffa0\ufff0-\ufff8\U0001bca0-\U0001bca3"
    "\U0001d173-\U0001d17a\U000e0000-\U000e0fff]")

# Elements whose content does not render: <rp> (hidden by the HTML
# default style), <template>, <script>, <style> and <noscript>, and any
# element with the hidden attribute or an inline display:none. The
# hidden-content reading deletes each such element, content included,
# so its neighbours join (he<rp>x</rp>ld renders "held"). Void elements
# have no content; script and style content is raw text, so nested
# tags of the same name do not nest there.
PERMISSIVE_NONRENDER_TAGS = frozenset((
    "noscript", "rp", "script", "style", "template"))
PERMISSIVE_RAWTEXT_TAGS = frozenset(("script", "style"))
PERMISSIVE_VOID_TAGS = frozenset((
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "source", "track", "wbr"))
_PERMISSIVE_DISPLAY_NONE_RE = re.compile(r"display\s*:\s*none", re.IGNORECASE)

# Deleted by the permissive reading (a default-ignorable code point), so
# text replaced by it joins its neighbours while keeping offsets.
_PERMISSIVE_DELETED = "\u200b"


def _permissive_nonrendering(tag: str) -> bool:
    """True for an opening PERMISSIVE_TAG_RE tag whose element content
    does not render."""
    name = _PERMISSIVE_TAG_NAME_RE.match(tag)
    if not name:
        return False
    lname = name.group(1).lower()
    if lname in PERMISSIVE_VOID_TAGS:
        return False
    if lname in PERMISSIVE_NONRENDER_TAGS:
        return True
    pos = name.end()
    while (attr := _PERMISSIVE_ATTR_RE.match(tag, pos)):
        attr_name = attr.group(1).lower()
        if attr_name == "hidden":
            return True
        if (attr_name == "style" and attr.group(2)
                and _PERMISSIVE_DISPLAY_NONE_RE.search(attr.group(2))):
            return True
        pos = attr.end()
    return False


def _permissive_delete_hidden(text: str) -> str:
    """Replace each non-rendering element, from its opening tag to its
    matching closing tag (or the paragraph's end when unclosed), with
    characters the permissive reading deletes, keeping offsets."""
    tags = list(PERMISSIVE_TAG_RE.finditer(text))
    chars = list(text)
    k = 0
    while k < len(tags):
        opener = tags[k]
        if opener.group().startswith("</") or not _permissive_nonrendering(
                opener.group()):
            k += 1
            continue
        name = _PERMISSIVE_TAG_NAME_RE.match(opener.group()).group(1).lower()
        depth, end, j = 1, len(text), k + 1
        while j < len(tags):
            tag = tags[j].group()
            tag_name = re.match(r"</?([A-Za-z][A-Za-z0-9-]*)", tag).group(1).lower()
            if tag_name == name:
                if tag.startswith("</"):
                    depth -= 1
                    if depth == 0:
                        end = tags[j].end()
                        break
                elif name not in PERMISSIVE_RAWTEXT_TAGS:
                    depth += 1
            j += 1
        start = opener.start()
        chars[start:end] = _PERMISSIVE_DELETED * (end - start)
        while k < len(tags) and tags[k].start() < end:
            k += 1
    return "".join(chars)


def _permissive_mask_tails(text: str, alt: bool = False) -> str:
    """Blank image syntax (keeping the alt text when alt is set), and
    closing link tails only while an unmatched "[" is open before the
    "]": a bare "](...)" with no link opener renders literally, so its
    text is kept. In kept alt text, unescaped emphasis, strong and
    strikethrough delimiters and code-span backticks are deleted, joining
    their neighbours as the strict readings delete them elsewhere
    (![r*e*f*e*rence](x.png) has the alt text "reference")."""
    chars = list(text)
    depth, i, n = 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == "\\" and ESCAPE_RE.match(text, i):
            i += 2
            continue
        if c == "!" and (m := PERMISSIVE_IMAGE_RE.match(text, i)):
            keep = text.index("]", i + 2) if alt else i
            chars[i:i + 2] = "  "
            chars[keep:m.end()] = " " * (m.end() - keep)
            j = i + 2
            while j < keep:
                if text[j] == "\\" and ESCAPE_RE.match(text, j):
                    j += 2
                    continue
                if text[j] in "*_~`":
                    chars[j] = _PERMISSIVE_DELETED
                j += 1
            i = m.end()
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            if depth and (m := PERMISSIVE_TAIL_RE.match(text, i)):
                depth -= 1
                chars[i:m.end()] = " " * (m.end() - i)
                i = m.end()
                continue
            depth = max(0, depth - 1)
        i += 1
    return "".join(chars)


def _permissive_blank_tag(tag: str, alt: bool) -> str:
    """Spaces for a well-formed tag, keeping offsets; with alt set, an
    <img> tag's alt value is kept, because it renders as text."""
    blanked = _blank(tag)
    name = _PERMISSIVE_TAG_NAME_RE.match(tag)
    if not alt or not name or name.group(1).lower() != "img":
        return blanked
    chars = list(blanked)
    pos = name.end()
    while (attr := _PERMISSIVE_ATTR_RE.match(tag, pos)):
        a, b = attr.span(2)
        if attr.group(1).lower() == "alt" and a < b:
            if tag[a] in "\"'":
                a, b = a + 1, b - 1
            chars[a:b] = tag[a:b]
        pos = attr.end()
    return "".join(chars)


def _permissive_reading(para: str, base: int, alt: bool = False,
                        hide: bool = False):
    """(text, source-offset map) of the paragraph's permissive
    normalization: closed comments, images, closing link tails and
    well-formed inline tags blanked, except that with alt set an
    image's alt text (Markdown or an <img> tag's alt value) is kept,
    with emphasis delimiters in a Markdown alt text deleted; with hide
    set, non-rendering elements deleted with their content, joining
    their neighbours; entities that decode decoded; ASCII letters and
    digits kept case-folded; combining, format and control characters
    (Unicode categories Mn, Cf and Cc, except whitespace) and
    default-ignorable code points deleted, joining their neighbours;
    every other character read as a word separator; and separators
    collapsed to one space."""
    masked = _blank_matches(COMMENT_RE, para)
    if hide:
        masked = _permissive_delete_hidden(masked)
    masked = _permissive_mask_tails(masked, alt)
    masked = PERMISSIVE_TAG_RE.sub(
        lambda m: _permissive_blank_tag(m.group(), alt), masked)
    out: list[str] = []
    cmap: list[int] = []

    def emit(piece: str, src: int) -> None:
        for c in piece:
            if c.isascii() and c.isalnum():
                out.append(c.lower())
                cmap.append(src)
            elif PERMISSIVE_IGNORABLE_RE.match(c) or (
                    not c.isspace()
                    and unicodedata.category(c) in ("Mn", "Cf", "Cc")):
                continue
            elif out and out[-1] != " ":
                out.append(" ")
                cmap.append(src)

    i, n = 0, len(masked)
    while i < n:
        if masked[i] == "&" and (em := ENTITY_RE.match(masked, i)):
            decoded = html.unescape(em.group())
            if decoded != em.group():
                emit(decoded, base + i)
                i = em.end()
                continue
        emit(masked[i], base + i)
        i += 1
    return "".join(out), cmap


def permissive_hidden_claims(body: str) -> "list[tuple[int, int]]":
    """Source (start, end) spans where the body's permissive reading
    spells the canonical claim. Each paragraph is read twice, with
    images blanked and with images read as their alt text, and each
    of those twice more where the body has a non-rendering element,
    with its content kept and with it deleted. Each reading's
    paragraphs are joined with a separator for every paragraph break,
    so a claim split across a paragraph break is spelled as well as
    one inside a paragraph. Overlapping spans are reported once. The
    caller drops spans whose start a detected claim or a screen
    finding already covers; each remaining span is a refusal finding
    (a possible hidden claim)."""
    found: "set[tuple[int, int]]" = set()
    nonrendering = any(
        not m.group().startswith("</") and _permissive_nonrendering(m.group())
        for m in PERMISSIVE_TAG_RE.finditer(body))
    for alt, hide in ((False, False), (True, False), (False, True),
                      (True, True)):
        if hide and not nonrendering:
            continue
        texts: list[str] = []
        cmap: list[int] = []
        pos = 0
        for blank in [*BLANK_LINE_RE.finditer(body), None]:
            end = blank.start() if blank else len(body)
            text, para_map = _permissive_reading(body[pos:end], pos, alt, hide)
            texts.append(text + " ")
            cmap.extend(para_map)
            cmap.append(end)
            if blank is None:
                break
            pos = blank.end()
        for m in CANONICAL_STRIPPED_RE.finditer("".join(texts)):
            found.add((cmap[m.start()], cmap[m.end() - 1] + 1))
    hits: "list[tuple[int, int]]" = []
    for start, end in sorted(found):
        if hits and start < hits[-1][1]:
            continue
        hits.append((start, end))
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
    marker_spans: list[tuple[int, int]] = []
    for start, end, queries, problem in find_markers(body):
        if problem:
            findings.append(
                f"{rel}:{line_at(start)}: malformed ref-absence marker: "
                f"{problem}, so it satisfies no claim"
            )
            continue
        markers.append((line_at(start), queries))
        marker_spans.append((start, end))
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
    screen = _screen_view(views[0])
    screen_hits = obfuscated_claim_hits(
        body, screen, views[1], [(s, e) for _, _, s, e in claims],
        marker_spans)
    for start, end in screen_hits:
        first, last = line_at(start), line_at(end - 1)
        span = f"line {first}" if first == last else f"lines {first}-{last}"
        findings.append(
            f"{rel}:{first}: unreadable markup around a possible "
            f"reference-absence claim; write the sentence plainly "
            f"({span}): the claim's words appear in order through markup "
            f"the screen cannot read exactly; if the sentence claims a "
            f"source is absent, write the canonical 'not held in the "
            f"reference base' sentence in plain Markdown with its "
            f"<!-- ref-absence: query1 | query2 --> marker on its lines"
        )
    for lineno in sorted({line_at(o) for o in bidi_control_offsets(body)}):
        findings.append(
            f"{rel}:{lineno}: bidirectional override or isolate control "
            f"(U+202A-U+202E, U+2066-U+2069 or a <bdo> element) on line "
            f"{lineno}: it can display the line's text in an order other "
            f"than the order every reading scans, so a reference-absence "
            f"claim can hide in it; remove it and write the sentence plainly"
        )
    covered = [(s, e) for _, _, s, e in claims] + screen_hits
    for start, end in permissive_hidden_claims(body):
        if any(cs <= start < ce for cs, ce in covered):
            continue
        first, last = line_at(start), line_at(end - 1)
        span = f"line {first}" if first == last else f"lines {first}-{last}"
        findings.append(
            f"{rel}:{first}: possible hidden claim ({span}): a permissive "
            f"reading of the text spells the canonical reference-"
            f"absence sentence where no reading detects a claim; write "
            f"the claim in plain Markdown with its "
            f"<!-- ref-absence: query1 | query2 --> marker on its lines"
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
            "stay absent from the tracked reference-acquisition manifest."
        ),
    )
    parser.add_argument("paths", nargs="*", default=None, help="Paths to scan.")
    args = parser.parse_args(argv[1:])
    manifest_rows = load_manifest_rows(REPO_ROOT)
    if manifest_rows is None or not manifest_rows:
        print(
            f"ERROR: cannot read any data rows from {MANIFEST_PATH}; the "
            f"tracked manifest is this gate's staleness source "
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
