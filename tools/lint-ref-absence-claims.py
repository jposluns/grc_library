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

   The marker renders invisible. Authoring guidance: use the most stable
   identifier available (a document number such as ``SR 11-7`` beats an
   agency acronym) and keep each query jurisdiction-unambiguous (a bare
   ``AI Ethics Principles`` matches Australia's held principles). A
   class-claim with no nameable source (instruments outside an annex's
   scope) still carries a marker naming the class; it can never match,
   which is correct: no specific source, no staleness possible.

2. NO ORPHAN MARKERS. A ``ref-absence`` marker must sit on or directly
   under a line carrying a reference-absence claim, so a marker cannot
   detach from its claim and silently stop guarding it. A marker with no
   query, or with an empty alternative, is malformed and fails.

3. STALENESS. Each marker query is matched (case-insensitive,
   whitespace-normalized substring) against the DATA ROWS of the
   committed public bibliography
   ``docs/reference-acquisition-manifest.md`` (generated from
   ``grc_library_ref/catalogue.yml``; the
   ``build-reference-manifest.py --check`` sync obligation under the
   resync-``_ref`` discipline keeps it fresh). A hit means the reference
   index says the source IS held, so the "not held" sentence is stale:
   the finding quotes the manifest row (the executed-not-narrated rule
   ``ref-holds.py`` codifies). Consuming the committed manifest keeps
   the gate deterministic from repository state alone: sibling-free and
   green on adopter clones and in CI, no sibling-degrade path needed.

4. NEAR-MISS NET. A paraphrase (``not held`` / ``not <adverb>ly held`` /
   ``does not hold`` / ``do not hold`` / ``absent from`` / ``missing
   from`` within eight tokens of ``reference base`` / ``reference
   library`` / ``held text`` / ``grc_library_ref``) fails with a
   use-the-canonical-phrasing message, converting a reworded claim into
   a style finding instead of a silent blind spot. A content-absence
   claim ABOUT held texts ("searches of both held texts return no such
   duty", "a signing date is not in the held text") does not trigger.

Meta-documents that quote the pattern as a rule (the CHANGELOG, the
audit-programme specification, and the claim-fit / matrix-fit pack
skills whose vocabulary is literally not-held) are exempt by name below,
per the audit-programme section 3 principle-4 meta-document carve-out.
Scan scope: ``README.md``, ``NOTICE.md``, the audited domain directories
(splatted from ``lint_common.AUDITED_DOMAIN_DIRS``; the scan-scope
parity gate forbids hardcoding the run), and the ``guardrails/`` pack,
fence-aware via the shared iterator.

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
    iter_non_code_lines,
    iter_scan_roots_markdown,
    read_text_safe,
)

# The committed staleness source (never the sibling): the public
# bibliography of every trusted-bucket catalogue entry.
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
# independently held"), and the "does/do not hold" verb form. "not in the
# held text" (a content-absence claim) does NOT match: "in"/"the" are not
# -ly adverbs.
NEAR_MISS_TRIGGER_RE = re.compile(
    r"\bnot\s+(?:\w+ly\s+)?held\b"
    r"|\b(?:absent|missing)\s+from\b"
    r"|\b(?:does|do)\s+not\s+(?:\w+ly\s+)?hold\b",
    re.IGNORECASE,
)
# A trigger is a finding only near the reference base's own vocabulary.
# Deliberately NOT bare "reference": "absent from library section-20
# references" is a content claim, not a holdings claim.
NEAR_MISS_CONTEXT_RE = re.compile(
    r"reference\s+(?:base|library)|held\s+texts?|grc_library_ref",
    re.IGNORECASE,
)
NEAR_MISS_WINDOW_TOKENS = 8


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


def parse_markers(line: str) -> "list[list[str]]":
    """Each marker's query alternatives, split on ``|`` and stripped."""
    out = []
    for m in MARKER_RE.finditer(line):
        out.append([q.strip() for q in m.group(1).split("|")])
    return out


def near_miss_snippets(line: str, canonical_spans) -> "list[str]":
    """Trigger snippets on this line that are near-misses, canonical excluded."""
    hits = []
    for m in NEAR_MISS_TRIGGER_RE.finditer(line):
        if any(m.start() < end and m.end() > start for start, end in canonical_spans):
            continue
        before = " ".join(line[: m.start()].split()[-NEAR_MISS_WINDOW_TOKENS:])
        after = " ".join(line[m.end():].split()[:NEAR_MISS_WINDOW_TOKENS])
        window = " ".join(part for part in (before, m.group(0), after) if part)
        if NEAR_MISS_CONTEXT_RE.search(window):
            hits.append(m.group(0))
    return hits


def scan_text(rel: str, text: str, manifest_rows) -> "list[str]":
    findings: list[str] = []
    canonical_lines: set[int] = set()
    near_lines: set[int] = set()
    markers: dict[int, list[list[str]]] = {}

    for lineno, line in iter_non_code_lines(text):
        spans = [(m.start(), m.end()) for m in CANONICAL_RE.finditer(line)]
        if spans:
            canonical_lines.add(lineno)
        for snippet in near_miss_snippets(line, spans):
            near_lines.add(lineno)
            findings.append(
                f"{rel}:{lineno}: non-canonical reference-absence phrasing "
                f"({snippet!r}): use the canonical 'not held in the reference "
                f"base' sentence with an adjacent <!-- ref-absence: ... --> "
                f"marker so the claim is machine-checkable"
            )
        found = parse_markers(line)
        if found:
            markers[lineno] = found

    for lineno in sorted(canonical_lines):
        if lineno not in markers and (lineno + 1) not in markers:
            findings.append(
                f"{rel}:{lineno}: canonical reference-absence claim carries no "
                f"adjacent <!-- ref-absence: query1 | query2 --> marker (same "
                f"line or the next line) naming the claimed-absent source"
            )

    for lineno in sorted(markers):
        # A marker beside a NEAR-MISS line is not additionally an orphan:
        # the canonical-phrasing finding already tells that story.
        claim_adjacent = {lineno, lineno - 1}
        if not (claim_adjacent & canonical_lines or claim_adjacent & near_lines):
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
        f for f in iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)
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
