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
   an optional ``currently``) must be immediately followed, on the same
   line or the next, by a machine-readable HTML-comment marker naming the
   claimed-absent source as one or more ``|``-separated index queries::

       ... that guidance is not held in the reference base, so an adopter
       confirms the current PIPC position directly.
       <!-- ref-absence: PIPC automated-decision guidance | PIPC AI -->

   The marker renders invisible. Detection is per prose BLOCK, not per
   physical line: consecutive prose lines are joined (source line numbers
   preserved; blank lines, fences, headings, table rows, list items and a
   change of blockquote depth bound a block, and blockquote markers are
   stripped first, so a quoted wrapped sentence joins like any other
   prose), so ordinary Markdown line wrapping cannot split the canonical
   sentence out of the gate's sight. A claim occupies its whole SENTENCE,
   not just the canonical phrase: the marker is adjacent when it sits on
   the line the claim's sentence ENDS on, or on the next line, so the
   example above (phrase, a wrapped continuation, then the marker) is
   correctly annotated. Marker accounting is per CLAIM, not per line: N
   claims whose sentences end on one physical line need N adjacent
   markers, and a next-line marker counts ONLY when that line ends no
   canonical claim of its own: one marker can never shield two claims.
   Authoring guidance: use the most stable identifier available (a
   document number such as ``SR 11-7`` beats an agency acronym) and
   keep each query
   jurisdiction-unambiguous (a bare ``AI Ethics Principles`` matches
   Australia's held principles). A class-claim with no nameable source
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
   RESIDUE: the manifest is regenerated maintainer-side under the
   resync-``_ref`` discipline (``build-reference-manifest.py --check``
   and the pre-push guard REPORT drift; neither is a CI gate, and the
   pre-push guard does not block on it), so after an ingestion into
   ``grc_library_ref`` a claim stays stale-but-green until the
   manifest-regeneration PR lands; THAT PR is where this gate flips the
   claim red.

4. NEAR-MISS NET. A paraphrase (``not held`` / ``not <adverb>ly held`` /
   ``does not hold`` / ``do not hold`` within eight tokens of
   ``reference base`` / ``reference library`` / ``held text`` /
   ``grc_library_ref``; or a rewording, ``not included`` / ``not
   present`` / ``not available`` / ``not indexed`` / ``not stored`` /
   ``does not include`` / ``does not contain`` / ``does not carry`` /
   ``absent from`` / ``missing from`` / ``excluded from`` / ``omitted
   from``, within eight tokens of ``reference base`` / ``reference
   library`` / ``grc_library_ref``) fails with a
   use-the-canonical-phrasing message, converting a reworded claim into
   a style finding instead of a silent blind spot. The rewording
   triggers deliberately do NOT count beside ``held text``, and a
   rewording whose OBJECT is the held text ("a signing date is absent
   from the held text", "the duty is not included in the held text") is
   skipped even when collection vocabulary sits elsewhere in the
   window: both assert missing CONTENT of a held document, a different
   claim from a missing SOURCE, and rephrasing either canonically would
   change its meaning. Stated residue: a
   bare ``not held`` with no reference-base vocabulary in the window is
   not auto-detected (most such lines are content claims); a holdings
   claim worded that way is annotated manually with a marker, which rule
   2 accepts and rule 3 checks.

Meta-documents that quote the pattern as a rule (the CHANGELOG, the
audit-programme specification, and the claim-fit / matrix-fit pack
skills whose vocabulary is literally not-held) are exempt by name below,
per the audit-programme section 3 principle-4 meta-document carve-out.
Scan scope: ``README.md``, ``NOTICE.md``, the audited domain directories
(splatted from ``lint_common.AUDITED_DOMAIN_DIRS``; the scan-scope
parity gate forbids hardcoding the run), and the ``guardrails/`` pack.
Fenced code is skipped with a width- and character-matching fence parser
(a four-backtick example fence may legitimately enclose three-backtick
lines, which stay code; the shared toggle-only iterator would re-expose
them). The fence parser reads THROUGH blockquote markers (a quoted
fence still toggles, so a quoted absence sentence inside it stays
code), and a fence opened inside a blockquote ends when the quote does
(CommonMark), so quoted code cannot swallow the prose after it.

Usage:
    python3 tools/lint-ref-absence-claims.py
    python3 tools/lint-ref-absence-claims.py path1.md dir2 ...

Exit codes:
    0   no findings
    1   one or more findings
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
EXEMPT_FILES = {
    # Historical record; narrates the pattern when describing this gate.
    "CHANGELOG.md",
    # The audit-programme spec's gate-104 prose quotes sentence and marker.
    "governance/specification-audit-programme.md",
    # The claim-fit / matrix-fit skills' rubric vocabulary is literally
    # not-held ("The source is not held, but I am confident ...").
    "guardrails/skills/claim-fit/SKILL.md",
    "guardrails/skills/matrix-fit/SKILL.md",
}

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

# Paraphrase triggers: plain "not held", one optional -ly adverb ("not
# independently held"), the "does/do not hold" verb form, and the
# plausible rewordings (not included / present / available / indexed /
# stored; does not include / contain / carry; absent / missing /
# excluded / omitted from). "not in the held text" (a content-absence
# claim) does NOT match: "in"/"the" are not -ly adverbs.
NEAR_MISS_TRIGGER_RE = re.compile(
    r"\bnot\s+(?:\w+ly\s+)?(?:held|included|present|available|indexed|stored)\b"
    r"|\b(?:absent|missing|excluded|omitted)\s+from\b"
    r"|\b(?:does|do)\s+not\s+(?:\w+ly\s+)?(?:hold|include|contain|carry)\b",
    re.IGNORECASE,
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
# same sentence. Matched against the text right after the trigger.
HELD_TEXT_OBJECT_RE = re.compile(
    r"^\s*(?:(?:in|within|from)\s+)?(?:[\w'-]+\s+){0,3}?held\s+texts?\b",
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
FENCE_RE = re.compile(r"^(`{3,}|~{3,})(.*)$")

# A line that STARTS a new Markdown block: heading, table row, or list
# item. A wrapped sentence never continues INTO one of these, so they
# bound the prose blocks the cross-line detection joins. Blockquote
# markers are stripped BEFORE this test (a quoted wrapped sentence joins
# like any other prose); a change of blockquote depth bounds the block
# in iter_prose_blocks instead.
BLOCK_START_RE = re.compile(r"^\s*(?:#{1,6}\s|\||[-*+]\s|\d{1,3}[.)]\s)")

# One or more leading blockquote markers, each with its optional space.
QUOTE_PREFIX_RE = re.compile(r"^\s*((?:>\s?)+)")


def _dequote(line: str) -> "tuple[int, str]":
    """(blockquote depth, the line with its blockquote markers stripped)."""
    m = QUOTE_PREFIX_RE.match(line)
    if not m:
        return 0, line
    return m.group(1).count(">"), line[m.end():]


def _normalize(text: str) -> str:
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
    code cannot swallow the prose after the quote."""
    out: list[tuple[int, int, str]] = []
    fence_char, fence_len, fence_depth = "", 0, 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        depth, content = _dequote(line)
        if fence_char and depth < fence_depth:
            # Leaving the blockquote closes the fence it opened.
            fence_char, fence_len = "", 0
        m = FENCE_RE.match(content.lstrip())
        if m:
            run = m.group(1)
            if not fence_char:
                fence_char, fence_len, fence_depth = run[0], len(run), depth
                continue
            if run[0] == fence_char and len(run) >= fence_len and not m.group(2).strip():
                fence_char, fence_len = "", 0
                continue
            # A narrower or different-character fence inside an open fence
            # is literal code content, not a toggle.
        if fence_char:
            continue
        out.append((lineno, depth, content))
    return out


def iter_prose_blocks(text: str) -> "list[list[tuple[int, str]]]":
    """Prose blocks as [(lineno, dequoted line), ...] runs: blank lines
    and fences end a block; a heading, table-row or list-item line starts
    a fresh one (a wrapped sentence never continues into those), and so
    does a change of blockquote depth (consecutive lines of ONE quote
    join, so a quoted wrapped sentence stays in the gate's sight)."""
    blocks: list[list[tuple[int, str]]] = []
    block: list[tuple[int, str]] = []
    prev_line, prev_depth = None, 0
    for lineno, depth, line in iter_prose_lines(text):
        if not line.strip():
            if block:
                blocks.append(block)
            block = []
            prev_line = None
            continue
        if block and (lineno != prev_line + 1 or depth != prev_depth
                      or BLOCK_START_RE.match(line)):
            blocks.append(block)
            block = []
        block.append((lineno, line))
        prev_line, prev_depth = lineno, depth
    if block:
        blocks.append(block)
    return blocks


def parse_markers(line: str) -> "list[list[str]]":
    """Each marker's query alternatives, split on ``|`` and stripped."""
    out = []
    for m in MARKER_RE.finditer(line):
        out.append([q.strip() for q in m.group(1).split("|")])
    return out


def near_miss_hits(text: str, canonical_spans) -> "list[tuple[int, str]]":
    """(offset, snippet) for near-miss triggers, canonical matches excluded."""
    hits = []
    for m in NEAR_MISS_TRIGGER_RE.finditer(text):
        if any(m.start() < end and m.end() > start for start, end in canonical_spans):
            continue
        if HELD_VERB_RE.search(m.group(0)):
            context = NEAR_MISS_CONTEXT_RE
        else:
            # A rewording whose OBJECT is the held text asserts missing
            # CONTENT, not a missing source: skip it however much
            # collection vocabulary the rest of the window carries.
            if HELD_TEXT_OBJECT_RE.match(text[m.end():]):
                continue
            context = NEAR_MISS_COLLECTION_CONTEXT_RE
        before = " ".join(text[: m.start()].split()[-NEAR_MISS_WINDOW_TOKENS:])
        after = " ".join(text[m.end():].split()[:NEAR_MISS_WINDOW_TOKENS])
        window = " ".join(part for part in (before, m.group(0), after) if part)
        if context.search(window):
            hits.append((m.start(), m.group(0)))
    return hits


def scan_text(rel: str, text: str, manifest_rows) -> "list[str]":
    findings: list[str] = []
    # How many claims end on each line: the sentence-end line anchors the
    # marker adjacency, and the COUNT keeps the accounting per claim (a
    # set of line numbers would let one marker shield two claims that end
    # on the same physical line).
    canonical_counts: dict[int, int] = {}
    claim_lines: set[int] = set()      # every line any claim touches (orphan adjacency)
    markers: dict[int, list[list[str]]] = {}

    for block in iter_prose_blocks(text):
        starts: list[tuple[int, int]] = []
        pos = 0
        for lineno, line in block:
            starts.append((pos, lineno))
            pos += len(line) + 1  # the joining space
        joined = " ".join(line for _, line in block)

        def line_at(offset: int) -> int:
            lineno = block[0][0]
            for start, candidate in starts:
                if offset < start:
                    break
                lineno = candidate
            return lineno

        spans = [(m.start(), m.end()) for m in CANONICAL_RE.finditer(joined)]
        for start, end in spans:
            # The claim runs to the end of its SENTENCE, not its phrase,
            # so a marker after a wrapped continuation stays adjacent.
            sentence = SENTENCE_END_RE.search(joined, end)
            sent_end = sentence.end() if sentence else len(joined)
            end_line = line_at(sent_end - 1)
            canonical_counts[end_line] = canonical_counts.get(end_line, 0) + 1
            claim_lines.update(range(line_at(start), end_line + 1))
        for m in NEAR_MISS_TRIGGER_RE.finditer(joined):
            # Any trigger line is annotatable (rule 2): a marker beside a
            # bare paraphrase the net does not flag is still no orphan.
            claim_lines.update({line_at(m.start()), line_at(m.end() - 1)})
        for offset, snippet in near_miss_hits(joined, spans):
            findings.append(
                f"{rel}:{line_at(offset)}: non-canonical reference-absence phrasing "
                f"({snippet!r}): use the canonical 'not held in the reference "
                f"base' sentence with an adjacent <!-- ref-absence: ... --> "
                f"marker so the claim is machine-checkable"
            )
        for lineno, line in block:
            found = parse_markers(line)
            if found:
                markers[lineno] = found

    for lineno in sorted(canonical_counts):
        claims = canonical_counts[lineno]
        covered = len(markers.get(lineno, []))
        # Next-line markers count only when that line ends no canonical
        # claim of its own, and the accounting is per CLAIM: N claims
        # ending on one line need N adjacent markers, so one marker can
        # never shield two claims.
        if canonical_counts.get(lineno + 1, 0) == 0:
            covered += len(markers.get(lineno + 1, []))
        if covered >= claims:
            continue
        shortfall = (
            f" ({claims} claims end on this line and only {covered} adjacent"
            f" marker(s) cover them; each claim carries its own marker)"
            if claims > 1 else ""
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
        if not ({lineno, lineno - 1} & claim_lines):
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
    if findings:
        print(f"\n{len(findings)} reference-absence finding(s).")
        return 1
    print(f"OK: reference-absence claims consistent across {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
