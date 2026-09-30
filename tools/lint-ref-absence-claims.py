#!/usr/bin/env python3
"""Reference-absence claim audit: absence claims carry a checkable identity.

A corpus sentence saying a source is "not held in the reference base" is a
HOLDINGS claim: it goes stale the moment the named source is ingested into
``grc_library_ref``, and a stale absence caveat propagates (templates and
procedures copy it). Prose-inference of the claim's referent is not
achievable in a stdlib gate without false positives (the referent is
usually anaphoric), so the claim CARRIES its own checkable identity and
the gate checks it against repository state alone (the
marker-plus-committed-manifest design):

1. CANONICAL FORM + MARKER. Every canonical absence sentence
   (``not held in the reference base`` / ``... reference library``, with
   an optional ``currently``) must be immediately followed by a
   machine-readable HTML-comment marker naming the claimed-absent source
   as one or more ``|``-separated index queries::

       ... that guidance is not held in the reference base, so an adopter
       confirms the current PIPC position directly.
       <!-- ref-absence: PIPC automated-decision guidance | PIPC AI -->

   The marker renders invisible. Detection is per prose BLOCK, not per
   physical line: consecutive prose lines are joined (source line numbers
   preserved; blank lines, fences, headings, table rows and list items
   bound a block, and blockquote markers are stripped first: an INCREASE
   of blockquote depth bounds a block, a DECREASE is CommonMark lazy
   continuation and joins, so a quoted wrapped sentence stays in the
   gate's sight even when its continuation line drops the ``>``), so
   ordinary Markdown line wrapping cannot split the canonical sentence
   out of the gate's sight. A claim occupies its whole SENTENCE, not
   just the canonical phrase: a marker is adjacent when it sits after
   the phrase, anywhere up to the end of the line the claim's sentence
   ENDS on (when that line carries exactly ONE canonical claim,
   further sentences may sit between the claim and its marker), or on
   the next line, so the example above (phrase, a
   wrapped continuation, then the marker) is correctly annotated, and
   so is a marker placed right after the phrase with the sentence
   continuing past it. Marker accounting is per CLAIM, not per line:
   each marker binds to at most ONE claim, in document order, so N
   claims whose sentences end on one physical line need N adjacent
   markers, each placed after its own claim and BEFORE the next
   claim's canonical phrase; and a next-line marker binds ONLY when nothing but
   earlier markers precedes it on its line AND that line carries no
   detectable absence claim of its own, canonical or paraphrase (a
   marker after any next-line prose annotates THAT prose, which may
   word a claim the net cannot parse, such as ``nor is the decree
   held``; a marker annotating its own bare ``not held`` line is that
   line's, per rule 2), so one marker can never shield two claims.
   Authoring guidance: use the most stable identifier available (a
   document number such as ``SR 11-7`` beats an agency acronym) and
   keep each query
   jurisdiction-unambiguous (a bare ``AI Ethics Principles`` matches
   Australia's held principles). Stated residue: a query is matched
   inside ONE manifest cell (a row's cells are ``|``-separated and
   ``|`` splits query alternatives), so a query for a source with no
   stable identifier is the maintainer's best forward guess at the
   future title-cell text and may need renaming when the row lands. A
   class-claim with no nameable source
   (instruments outside an annex's scope) still carries a marker naming
   the class; it can never match, which is correct: no specific source,
   no staleness possible.

2. NO ORPHAN MARKERS. A ``ref-absence`` marker must sit on or directly
   under a line carrying a reference-absence claim, so a marker cannot
   detach from its claim and silently stop guarding it. A bare paraphrase
   line (``not held`` / ``does not hold`` with no reference-base
   vocabulary in range, which rule 4 deliberately does not flag) COUNTS
   as a claim line here, so an author can annotate such a claim manually
   and the staleness check (rule 3) then guards it. A marker with no
   query, or with an empty alternative, is malformed and fails.

3. STALENESS. Each marker query is matched (case-insensitive,
   whitespace-normalized substring) against the DATA ROWS of the
   committed public bibliography
   ``docs/reference-acquisition-manifest.md``, which lists the four
   trusted ``grc_library_ref/catalogue.yml`` acquisition buckets only.
   The untrusted publications and books buckets are deliberately not
   published (maintainer ruling 2026-09-29), so a claim that a
   publication or book is not held is NOT staleness-checked (residue). A hit means the reference index says the source IS
   held, so the "not held" sentence is stale: the finding quotes the
   manifest row (the executed-not-narrated rule ``ref-holds.py``
   codifies). Consuming the committed manifest keeps the gate
   deterministic from repository state alone: sibling-free and green on
   adopter clones and in CI, no sibling-degrade path needed. TIMING
   RESIDUE: this gate never observes ``grc_library_ref`` itself; it
   re-checks claims only when it runs, against whatever manifest is
   committed. The manifest is regenerated maintainer-side under the
   resync-``_ref`` discipline (``build-reference-manifest.py --check``
   and the pre-push guard REPORT drift as advisories; neither is a CI
   gate, neither blocks, and nothing in this repository forces the
   regeneration PR to exist), so after an ingestion into
   ``grc_library_ref`` a claim stays stale-but-green until a
   regenerated manifest is committed; the earliest this gate can flip
   the claim red is its first run on that manifest-regeneration PR.

4. ADVISORY NEAR-MISS NET (maintainer ruling 2026-09-30). A paraphrase
   prints an ADVISORY use-the-canonical-phrasing message but NEVER
   affects the exit code. Rules 1-3 remain BLOCKING. The heuristic
   can miss holdings claims and flag content claims; its suggestions
   require human judgement before rewording. The triggers: ``not held`` / ``not
   <adverb>ly held`` / ``not yet held`` / ``does not hold`` / ``do
   not hold`` within
   eight tokens of ``reference base`` / ``reference library`` /
   ``held text`` / ``grc_library_ref``; a rewording (``not included``
   / ``not present`` / ``not available`` / ``not indexed`` / ``not
   stored`` / ``does not include`` / ``does not contain`` / ``does
   not carry`` / ``absent from`` / ``missing from`` / ``excluded
   from`` / ``omitted from``) within eight tokens of ``reference
   base`` / ``reference library`` / ``grc_library_ref``; a NEGATIVE
   SUBJECT with a positive verb (``neither X is held`` / ``none of
   them are held`` / ``no decree is held``, and the same subjects
   with ``included`` / ``present`` / ``available`` / ``indexed`` /
   ``stored``), classified by its verb like the forms above; and the
   collection as an active subject (``the reference base lacks`` /
   ``... omits``). The rewording and non-``held`` negative-subject
   triggers deliberately do NOT count beside ``held text``, and one
   whose OBJECT is the held text ("a signing date is absent from the
   held text") or whose SUBJECT is the held text ("the held text does
   not include a signing date") is skipped even when collection
   vocabulary sits elsewhere in the window: both assert missing
   CONTENT of a held document, a different claim from a missing
   SOURCE, and rephrasing either canonically would change its
   meaning. The held-text subject may carry a possessive ("the held
   text's annex"), set-off punctuation, and a modifier of up to six
   non-collection tokens before its verb ("the held texts of Decree
   13 do not include ..."). A held text POSSESSED by the collection
   ("absent from the reference base's held texts", "the reference
   base's held texts do not include") is the collection itself, so it
   stays IN the net, however long its modifier; typographic
   apostrophes are normalized to ASCII first, so ``the reference
   base’s`` and ``the reference base's`` read the same.
   Stated residue: a
   bare ``not held`` with no reference-base vocabulary in the window is
   not auto-detected (most such lines are content claims); a holdings
   claim worded that way is annotated manually with a marker, which rule
   2 accepts and rule 3 checks. Further stated residue, each annotated
   manually under rule 2 because mechanical detection false-positives
   on content claims: a rewording whose collection reference is
   anaphoric or beyond the eight-token window, a holding verb outside
   the enumerated set ("carries no copy of"), an inverted negative
   subject ("nor is the decree held"), and a held-text subject whose
   modifier runs more than six tokens before its verb. And the
   REVERSE residue: the rewording and negative-subject triggers read
   a world-EXISTENCE claim ("no official English translation is
   available") as a holdings claim when collection vocabulary falls
   inside the eight-token window; the gate cannot tell existence from
   holdings without semantics. These false positives and missed forms
   are advisory limitations, not reasons to rewrite accurate content.

Meta-documents that quote the pattern as a rule (the CHANGELOG and the
audit-programme specification) are exempt by name below, per the
audit-programme section 3 principle-4 meta-document carve-out; the
claim-fit / matrix-fit pack skills, exempted through r3 for their
not-held rubric vocabulary, scan clean under the current net and are no
longer exempt.
Scan scope: ``README.md``, ``NOTICE.md``, the audited domain directories
(splatted from ``lint_common.AUDITED_DOMAIN_DIRS``; the scan-scope
parity gate forbids hardcoding the run), and the ``guardrails/`` pack.
Fenced code is skipped with a width- and character-matching fence parser
(a four-backtick example fence may legitimately enclose three-backtick
lines, which stay code; the shared toggle-only iterator would re-expose
them). The fence parser reads THROUGH blockquote markers (a quoted
fence still toggles, so a quoted absence sentence inside it stays
code), and a fence opened inside a blockquote ends when the quote does
(CommonMark), so quoted code cannot swallow the prose after it; a fence
opened on a LIST-ITEM line or its indented continuation toggles too, so its closing fence cannot
masquerade as an opener and hide the prose after the list, and it ends
when its list item does (CommonMark: a non-blank line left of the
item's content column leaves the list), so an unclosed list fence
cannot swallow the prose after the list either; and a
backtick run whose info string itself contains a backtick is an inline
code span, not an opening fence (CommonMark), so it cannot swallow the
rest of the file.

Usage:
    python3 tools/lint-ref-absence-claims.py
    python3 tools/lint-ref-absence-claims.py path1.md dir2 ...

Exit codes:
    0   no blocking findings (ADVISORY findings may be printed)
    1   one or more blocking marker or staleness findings
    2   the committed manifest is missing or has no data rows, or an
        explicit path argument is refused

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
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

# The committed staleness source (never the sibling): the public
# bibliography of the four trusted catalogue buckets (publications and books
# are deliberately not published; see the docstring residue).
MANIFEST_PATH = "docs/reference-acquisition-manifest.md"

# Meta-documents exempt by name (section 3 principle 4): each quotes the
# canonical sentence or the marker as a RULE PATTERN, not as a claim.
# The claim-fit / matrix-fit pack skills, exempted here through r3 for
# their not-held rubric vocabulary, scan clean under the current net and
# are no longer exempt.
EXEMPT_FILES = set((
    # Historical record; narrates the pattern when describing this gate.
    "CHANGELOG.md",
    # The audit-programme spec's gate-104 prose quotes sentence and marker.
    "governance/specification-audit-programme.md",
))

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    # Domain run splatted from lint_common (scan-scope parity gate forbids
    # hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]

CANONICAL_RE = re.compile(
    r"\bnot\s+(?:currently\s+)?held\s+in\s+(?:the\s+|our\s+)?reference\s+(?:base|library)\b",
    re.IGNORECASE,
)

MARKER_RE = re.compile(r"<!--\s*ref-absence:(.*?)-->", re.DOTALL)

# Paraphrase triggers: plain "not held", one optional adverb (an -ly
# adverb, "not independently held", or bare "yet": "not yet held in the
# reference base" must not slip past the gate as r4 let it),
# the "does/do not hold" verb form, and the
# plausible rewordings (not included / present / available / indexed /
# stored; does not include / contain / carry; absent / missing /
# excluded / omitted from). "not in the held text" (a content-absence
# claim) does NOT match: "in"/"the" are not -ly adverbs.
NEAR_MISS_TRIGGER_RE = re.compile(
    r"\bnot\s+(?:(?:\w+ly|yet)\s+)?(?:held|included|present|available|indexed|stored)\b"
    r"|\b(?:absent|missing|excluded|omitted)\s+from\b"
    r"|\b(?:does|do)\s+not\s+(?:(?:\w+ly|yet)\s+)?(?:hold|include|contain|carry)\b",
    re.IGNORECASE,
)
# A negative subject with a positive verb is the same absence claim
# ("neither instrument is held", "no successor decree is included",
# "none of them are indexed"); without this the net is blind to it.
# Inverted forms ("nor is the decree held") are stated residue.
NEGATIVE_SUBJECT_TRIGGER_RE = re.compile(
    r"\b(?:neither|none|no|nor)\b(?:\s+[\w'-]+){0,6}?\s+(?:is|are|was|were)\s+"
    r"(?:(?:\w+ly|yet)\s+)?(?:held|included|present|available|indexed|stored)\b",
    re.IGNORECASE,
)
# The collection as an active subject rewords the same claim ("the
# reference base lacks the decree"); the trigger itself carries the
# collection vocabulary, so the context check is trivially satisfied.
COLLECTION_SUBJECT_TRIGGER_RE = re.compile(
    r"\b(?:reference\s+(?:base|library)|grc_library_ref)\s+"
    r"(?:[\w'-]+\s+){0,2}?(?:lacks|omits)\b",
    re.IGNORECASE,
)
# Every trigger family the near-miss net and the rule-2 claim-line
# accounting consult, in one place.
TRIGGER_RES = (
    NEAR_MISS_TRIGGER_RE,
    NEGATIVE_SUBJECT_TRIGGER_RE,
    COLLECTION_SUBJECT_TRIGGER_RE,
)
# Distinguishes the "held"/"hold" trigger wordings (which may use the
# held-text context legitimately) from the rewordings, which may not.
HELD_VERB_RE = re.compile(r"\bh[eo]ld\b", re.IGNORECASE)
# A trigger is a finding only near the reference base's own vocabulary.
# Deliberately NOT bare "reference": "absent from library section-20
# references" is a content claim, not a holdings claim.
NEAR_MISS_CONTEXT_RE = re.compile(
    r"reference\s+(?:base|library)|held\s+texts?|grc_library_ref",
    re.IGNORECASE,
)
# Every trigger except the "held"/"hold" wordings uses this NARROWER
# context: beside "held text(s)" a rewording asserts missing CONTENT of
# a held document ("a signing date is absent from the held text"), not a
# missing source, so only the collection vocabulary keeps it in the net
# (rule 4).
NEAR_MISS_COLLECTION_CONTEXT_RE = re.compile(
    r"reference\s+(?:base|library)|grc_library_ref",
    re.IGNORECASE,
)
NEAR_MISS_WINDOW_TOKENS = 8

# A rewording whose OBJECT is the held text is a content claim whatever
# else the window carries: "absent from the held text" and "not included
# in the held text" stay exempt even when "reference base" sits in the
# same sentence. Matched against the text right after the trigger. The
# filler words may NOT be collection vocabulary: "absent from the
# reference base's held texts" names the collection, not a document,
# and stays a holdings claim.
HELD_TEXT_OBJECT_RE = re.compile(
    r"^\s*(?:(?:in|within|from)\s+)?"
    r"(?:(?!(?:reference|base's|library's|grc_library_ref)\b)[\w'-]+\s+){0,3}?"
    r"held\s+texts?\b",
    re.IGNORECASE,
)
# A rewording whose SUBJECT is the held text is the same content claim
# ("the held text does not include a signing date"). Matched against
# the text right before the trigger. The subject may carry a modifier
# of up to six tokens between "held text(s)" and its verb ("the held
# texts of Decree 13 do not include ..."), a possessive ("the held
# text's annex"), and interior punctuation ("the held texts, as
# amended, do not include ..."); the modifier tokens may NOT be
# collection vocabulary, so "the held texts show that the reference
# base does not include X" (whose subject is the collection) stays in
# the net.
HELD_TEXT_SUBJECT_RE = re.compile(
    r"\bheld\s+texts?(?:'s?)?"
    r"(?:[,;:]?\s+(?!(?:reference|grc_library_ref)\b)[\w'()-]+){0,6}"
    r"[,;:]?\s*$",
    re.IGNORECASE,
)
# ... unless the held text is POSSESSED by the collection ("the
# reference base's held texts do not include"): that subject is the
# collection itself, so the claim stays in the net.
# Its tail mirrors HELD_TEXT_SUBJECT_RE's widened modifier, so a
# possessed-collection subject cannot slip out of the net by growing a
# modifier the content-claim exemption tolerates. Typographic
# apostrophes are normalized to ASCII before any of these run.
COLLECTION_POSSESSED_SUBJECT_RE = re.compile(
    r"\b(?:reference\s+(?:base|library)|grc_library_ref)'s\s+"
    r"(?:[\w'-]+\s+){0,2}?held\s+texts?(?:'s?)?"
    r"(?:[,;:]?\s+[\w'()-]+){0,6}[,;:]?\s*$",
    re.IGNORECASE,
)

# The end of the sentence a canonical phrase belongs to: the next
# terminator (closing quotes or brackets tolerated) followed by
# whitespace or the block end. The claim occupies its whole sentence, so
# the marker's adjacency anchor is the line the SENTENCE ends on; anchor
# on the phrase instead and the documented authoring example (phrase, a
# wrapped continuation, then the marker) reads as unmarked plus orphan.
SENTENCE_END_RE = re.compile(r"[.!?][\"')\]]*(?=\s|$)")

# A fence line: a run of three-plus backticks or tildes (leading indent
# tolerated). Unlike lint_common.iter_non_code_lines' toggle, the CLOSE
# must match the OPENING fence's character, be at least as wide, and carry
# no info string (CommonMark), so a four-backtick example fence keeps its
# enclosed three-backtick lines as code instead of re-exposing them.
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

# A list-item prefix: a fence may OPEN on a list-item line (CommonMark),
# and missing that opener would let its closing fence masquerade as an
# opener and swallow the prose after the list.
LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s+")

# A line that STARTS a new Markdown block: heading, table row, or list
# item. A wrapped sentence never continues INTO one of these, so they
# bound the prose blocks the cross-line detection joins. Blockquote
# markers are stripped BEFORE this test (a quoted wrapped sentence joins
# like any other prose); a change of blockquote depth bounds the block
# in iter_prose_blocks instead.
BLOCK_START_RE = re.compile(r"^\s*(?:#{1,6}\s|\||[-*+]\s|\d{1,9}[.)]\s)")

# One or more leading blockquote markers, each with its optional space.
QUOTE_PREFIX_RE = re.compile(r"^ {0,3}((?:> ?)+)")


def _dequote(line: str) -> "tuple[int, str]":
    """(blockquote depth, the line with its blockquote markers stripped)."""
    m = QUOTE_PREFIX_RE.match(line)
    if not m:
        return 0, line
    return m.group(1).count(">"), line[m.end():]


def _comment_open(text: str, opened: bool = False) -> bool:
    """Track HTML comments without interpreting Markdown inside them."""
    for token in re.finditer(r"<!--|-->", text):
        if token.group() == "<!--" and not opened:
            opened = True
        elif token.group() == "-->" and opened:
            opened = False
    return opened


def _normalize(text: str) -> str:
    text = text.translate(str.maketrans("‘’“”‐‑‒–—−", "''\"\"------"))
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
        # Skip the header row and the dash separator; keep data rows only,
        # so a query can never "match" the manifest's overview prose.
        if not first or first == "Title" or set(first) <= set("- :"):
            continue
        rows.append((lineno, _normalize(stripped), stripped))
    return rows


def iter_prose_lines(text: str) -> "list[tuple[int, int, str]]":
    """(lineno, blockquote depth, dequoted line) for each line outside
    fenced code, fence-width-aware. Fences are matched on the DEQUOTED
    text, so a fence inside a blockquote still toggles; a fence opened
    inside a blockquote ends when the quote does (CommonMark), so quoted
    code cannot swallow the prose after the quote. A fence may OPEN on a
    list-item line or its indented continuation; a backtick opener whose info string contains a
    backtick is an inline code span, not a fence (CommonMark)."""
    out: list[tuple[int, int, str]] = []
    fence_char, fence_len, fence_depth, fence_item_indent = "", 0, 0, 0
    list_items: list[tuple[int, int]] = []  # (quote depth, content column)
    comment_open = paragraph = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        depth, content = _dequote(line.expandtabs(4))
        if comment_open:
            out.append((lineno, depth, content))
            comment_open = _comment_open(content, True)
            continue
        if fence_char and depth < fence_depth:
            # Leaving the blockquote closes the fence it opened.
            fence_char, fence_len, fence_item_indent = "", 0, 0
        if (fence_char and fence_item_indent and content.strip()
                and len(content) - len(content.lstrip()) < fence_item_indent):
            # A fence opened on a list-item line ends when the item does
            # (CommonMark): a non-blank line indented left of the item's
            # content column leaves the list, so it is prose (or a fresh
            # fence), not swallowed code.
            fence_char, fence_len, fence_item_indent = "", 0, 0
        lm = None
        if not fence_char and content.strip():
            indent = len(content) - len(content.lstrip())
            while list_items and (depth != list_items[-1][0]
                                  or indent < list_items[-1][1]):
                list_items.pop()
            base = list_items[-1][1] if list_items else 0
            if indent - base <= 3:
                lm = LIST_PREFIX_RE.match(content)
            if lm:
                list_items.append((depth, lm.end()))
        base = fence_item_indent if fence_char else (
            list_items[-1][1] if list_items else 0)
        relative = content[base:]
        # Four spaces relative to the container are code only when no
        # paragraph is being continued; they can never open a fence.
        if (not fence_char and not lm and relative.startswith("    ")
                and not paragraph):
            continue
        m = FENCE_RE.match(relative)
        if not m and not fence_char:
            if lm:
                m = FENCE_RE.match(content[lm.end():])
        if m:
            run = m.group(1)
            if not fence_char:
                if run[0] == "~" or "`" not in m.group(2):
                    paragraph = False
                    fence_char, fence_len, fence_depth = run[0], len(run), depth
                    fence_item_indent = list_items[-1][1] if list_items else 0
                    continue
                # A backtick run with a backtick in its info string is an
                # inline code span, not an opening fence: fall through.
            elif run[0] == fence_char and len(run) >= fence_len and not m.group(2).strip():
                fence_char, fence_len, fence_item_indent = "", 0, 0
                continue
            # A narrower or different-character fence inside an open fence
            # is literal code content, not a toggle.
        if fence_char:
            continue
        out.append((lineno, depth, content))
        comment_open = _comment_open(content)
        paragraph = bool(content.strip()) and not re.match(r"^ {0,3}(?:#|\|)", content)
    return out


def iter_prose_blocks(text: str) -> "list[list[tuple[int, str]]]":
    """Prose blocks as [(lineno, dequoted line), ...] runs: blank lines
    and fences end a block; a heading, table-row or list-item line starts
    a fresh one (a wrapped sentence never continues into those). An
    INCREASE of blockquote depth starts a fresh block (a quote interrupts
    a paragraph); a DECREASE on a consecutive prose line is CommonMark
    lazy continuation and JOINS, so a quoted wrapped sentence stays in
    the gate's sight even when its continuation line drops the ">"."""
    blocks: list[list[tuple[int, str]]] = []
    block: list[tuple[int, str]] = []
    prev_line, prev_depth = None, 0
    comment_open = False
    for lineno, depth, line in iter_prose_lines(text):
        inside_comment = comment_open
        comment_open = _comment_open(line, comment_open)
        if inside_comment:
            block.append((lineno, line))
            prev_line = lineno
            continue
        if not line.strip():
            if block:
                blocks.append(block)
            block = []
            prev_line = None
            continue
        lazy = (bool(block) and lineno == prev_line + 1 and depth < prev_depth
                and not BLOCK_START_RE.match(line))
        if block and not lazy and (lineno != prev_line + 1 or depth != prev_depth
                                   or BLOCK_START_RE.match(line)):
            blocks.append(block)
            block = []
        block.append((lineno, line))
        prev_line = lineno
        prev_depth = prev_depth if lazy else depth
    if block:
        blocks.append(block)
    return blocks


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
                # A rewording whose OBJECT or SUBJECT is the held text
                # asserts missing CONTENT, not a missing source: skip it
                # however much collection vocabulary the rest of the
                # window carries. A held text POSSESSED by the collection
                # is the collection, so it stays in the net.
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
    findings: list[str] = []
    # How many claims end on each line: the sentence-end line anchors the
    # marker adjacency, and the binding below is per claim, so one marker
    # can never shield two claims that end on the same line.
    canonical_counts: dict[int, int] = dict()
    claim_lines: set[int] = set()      # every line any claim touches (orphan adjacency)
    trigger_lines: set[int] = set()    # lines carrying an absence wording of their own
    markers: dict[int, list[list[str]]] = dict()
    # Marker instances with their block-local offsets, for per-claim binding.
    slots: "list[dict]" = []
    # Canonical claims: phrase-end offset (block-local), sentence-end line.
    claims: "list[dict]" = []

    for block_id, block in enumerate(iter_prose_blocks(text)):
        starts: list[tuple[int, int]] = []
        pos = 0
        for lineno, line in block:
            starts.append((pos, lineno))
            pos += len(line) + 1  # the joining space
        # Typographic apostrophes are the same claim (and the same
        # length, so the offset math is untouched): normalize them so
        # "the reference base\u2019s held texts" cannot buy an exemption
        # its ASCII twin is denied.
        joined = " ".join(line for _, line in block)
        marker_matches = list(MARKER_RE.finditer(joined))
        # Comments are metadata, not claims or sentence terminators. Keep
        # their offsets and physical line mapping intact for binding.
        joined = MARKER_RE.sub(lambda m: " " * len(m.group()), joined)
        joined = joined.replace("\u2019", "'").replace("\u2018", "'")

        def line_at(offset: int) -> int:
            lineno = block[0][0]
            for start, candidate in starts:
                if offset < start:
                    break
                lineno = candidate
            return lineno

        spans = [(m.start(), m.end()) for m in CANONICAL_RE.finditer(joined)]
        for span_idx, (start, end) in enumerate(spans):
            # The claim runs to the end of its SENTENCE, not its phrase,
            # so a marker after a wrapped continuation stays adjacent.
            sentence = SENTENCE_END_RE.search(joined, end)
            sent_end = sentence.end() if sentence else len(joined)
            end_line = line_at(sent_end - 1)
            canonical_counts[end_line] = canonical_counts.get(end_line, 0) + 1
            claim_lines.update(range(line_at(start), end_line + 1))
            next_start = (spans[span_idx + 1][0] if span_idx + 1 < len(spans)
                          else len(joined) + 1)
            claims.append(dict(phrase_end=end, next_start=next_start,
                               end_line=end_line,
                               block=block_id, covered=False))
        for trigger_re in TRIGGER_RES:
            for m in trigger_re.finditer(joined):
                # Any trigger line is annotatable (rule 2): a marker beside
                # a bare paraphrase the net does not flag is still no
                # orphan; and a trigger line has a claim of ITS OWN, so a
                # marker there never binds to the claim above (rule 1).
                for edge in (m.start(), m.end() - 1):
                    claim_lines.add(line_at(edge))
                    trigger_lines.add(line_at(edge))
        for offset, snippet in near_miss_hits(joined, spans):
            findings.append(
                f"ADVISORY: {rel}:{line_at(offset)}: non-canonical reference-absence phrasing "
                f"({snippet!r}): use the canonical 'not held in the reference "
                f"base' sentence with an adjacent <!-- ref-absence: ... --> "
                f"marker so the claim is machine-checkable"
            )
        for m in marker_matches:
            lineno = line_at(m.start())
            line_start = next(start for start, number in starts if number == lineno)
            queries = [q.strip() for q in m.group(1).split("|")]
            markers.setdefault(lineno, []).append(queries)
            # Earlier markers are already masked; only prose before the
            # opener disqualifies next-line binding.
            lead = bool(joined[line_start:m.start()].strip())
            slots.append(dict(off=m.start(), lineno=lineno,
                              block=block_id, used=False, lead=lead))

    own_claim_lines = trigger_lines | set(canonical_counts)

    # Per-claim marker binding, in document order: each claim binds the
    # first unused marker that sits after its phrase, up to the end of
    # its sentence-end line (a marker may sit mid-sentence, right after
    # the phrase), or on the next line when that line carries no absence
    # claim of its own (a marker annotating its own bare "not held" line
    # never shields the canonical claim above).
    slots_by_block: dict[int, "list[dict]"] = dict()
    for slot in slots:
        slots_by_block.setdefault(slot["block"], []).append(slot)
    for claim in claims:
        for slot in slots_by_block.get(claim["block"], []):
            if slot["used"] or slot["off"] < claim["phrase_end"]:
                continue
            # Same-line binding: a line carrying exactly ONE canonical
            # claim binds a marker anywhere later on it (further
            # sentences may intervene); a line carrying several binds
            # each claim's marker only BEFORE the next claim's phrase,
            # so one marker can never shield two.
            if (slot["lineno"] <= claim["end_line"]
                    and (canonical_counts[claim["end_line"]] == 1
                         or slot["off"] < claim["next_start"])) or (
                slot["lineno"] == claim["end_line"] + 1
                and not slot["lead"]
                and slot["lineno"] not in own_claim_lines
            ):
                slot["used"] = True
                claim["covered"] = True
                break
    # A next-line marker may open a DIFFERENT block (a claim closing a
    # list item, the marker on the following plain line): same rule, the
    # next line must carry no absence claim of its own.
    for claim in claims:
        if claim["covered"]:
            continue
        next_line = claim["end_line"] + 1
        if next_line in own_claim_lines:
            continue
        for slot in slots:
            if (not slot["used"] and not slot["lead"]
                    and slot["lineno"] == next_line
                    and slot["block"] != claim["block"]):
                slot["used"] = True
                claim["covered"] = True
                break

    uncovered: dict[int, int] = dict()
    for claim in claims:
        if not claim["covered"]:
            uncovered[claim["end_line"]] = uncovered.get(claim["end_line"], 0) + 1
    for lineno in sorted(uncovered):
        total = canonical_counts[lineno]
        covered = total - uncovered[lineno]
        shortfall = (
            f" ({total} claims end on this line and only {covered} adjacent"
            f" marker(s) cover them; each claim carries its own marker)"
            if total > 1 else ""
        )
        findings.append(
            f"{rel}:{lineno}: canonical reference-absence claim carries no "
            f"adjacent <!-- ref-absence: query1 | query2 --> marker (same "
            f"line or the next line) naming the claimed-absent source"
            + shortfall
        )

    for lineno in sorted(markers):
        # A marker beside a NEAR-MISS line is not additionally an orphan:
        # the canonical-phrasing finding already tells that story.
        if not (set((lineno, lineno - 1)) & claim_lines):
            findings.append(
                f"{rel}:{lineno}: orphan ref-absence marker: no reference-"
                f"absence claim on this line or the line above"
            )
        for queries in markers[lineno]:
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

    # Explicit paths are refused when unsound and normalized otherwise (3b21).
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
