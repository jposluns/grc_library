#!/usr/bin/env python3
"""Cross-file section-NAME reference audit (gate 65, the names phase).

Gate 62 (``lint-cross-file-section-refs.py``) validates that a
cross-file ``Section N`` / ``§N`` reference resolves to a real numbered
heading or inline clause in the linked target document. This gate adds
the TITLE dimension for the subset of references that pair the number
with a heading title, e.g. ``[target](target.md) §4 (Encryption
standards)`` or ``Section 5.4, "Key rotation", in [target](...)``: the
cited title must belong to the cited number in the target.

The core design is the TITLE-ANCHORING rule (from the 2026-07-04
corpus survey): a parenthetical or quoted candidate after a reference
is treated as a title claim ONLY when its normalized form exactly
equals SOME numbered-heading title in the resolved target. Then:

- candidate equals the cited number's own title: PASS;
- candidate equals a DIFFERENT number's title only: FAIL (the
  stale-renumber shape, the #548 / FR-48-lockstep escape class);
- candidate matches no heading title in the target: SKIP (it is an
  explanatory paraphrase, a deliberate shorthand, or a reference to
  the citing document's own sections, none of which is a title claim).

Anchoring is what keeps the gate quiet on the corpus's dominant
non-title parenthetical population (explanations such as ``§3 (sixth
accountability action ...)`` and shorthands such as ``Section 7
(network)``) without excluding the genuine title citations.

Deliberate deltas from gate 62, each evidence-backed by the survey:

- TABLE ROWS ARE SCANNED. Gate 62 excludes table lines because bare
  external clause NUMBERS sit in cells next to corpus links (a large
  false-positive surface). The names phase's trigger is far narrower
  (number plus an anchoring title), and the canonical renumber-drift
  carriers (the ``§4 (Encryption standards)`` TLS rows) live in
  tables; scanning them found zero false positives corpus-wide.
  ``adjacent_link``'s pipe-breaks-adjacency defence still prevents a
  cell's reference binding to a neighbouring cell's link.
- ``dev-security/claude-rules/README.md`` is exempt BY RELATIVE PATH
  (its version-history table narrates past reference shapes frozen
  as-of-write, the same rationale as the CHANGELOG exemption; the
  root README.md stays scanned).
- References whose cited number carries no heading title in the
  target are skipped on NON-TABLE lines (gate 62 owns existence
  there, and an inline clause has no title to verify). On TABLE rows,
  which gate 62 excludes wholesale, an anchored title claim whose
  cited number is absent from the target FAILS here instead: without
  this, the vanished-number renumber shape on the framework-table
  carriers (this gate's canonical class) would be claimed by gate 62
  on paper and covered by neither gate in fact (the r4 O-1 seam).

Comparison rule: case-insensitive, whitespace collapsed, trailing
``.`` / ``:`` stripped, otherwise exact. Containment or prefix
matching is deliberately NOT applied (it would drag the deliberate
shorthands into checked scope and create cross-anchor collisions on
short generic titles); widening is a documented option, not the
default.

The shared ``ADJACENCY_WINDOW = 40`` also means a titled reference
whose link sits 41-60 characters away is unclaimed here exactly as it
is unclaimed by gate 62 (the accepted heuristic band documented in
``lint-intra-doc-refs.py``'s docstring).

The five shared reference-extraction constants (REF_PATTERNS,
MD_LINK_RE, BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, ADJACENCY_WINDOW)
are imported from ``lint_common``'s CROSS_* block, the single source
of truth for both cross-file gates since the 2026-07-04
guardrail-review G-4 hoist (they were copy-with-comment duplicates
before it). The helper functions (resolve_target, binding_target,
adjacent_link) and HEADING_RE remain copied from
``lint-cross-file-section-refs.py`` with the in-code provenance note
(hyphenated module names cannot be imported; the copy-with-comment
pattern follows gate 62's own reuse of ``lint-intra-doc-refs.py``'s
heading model).

Usage:
    python3 tools/lint-cross-file-section-names.py
    python3 tools/lint-cross-file-section-names.py path1 path2 ...

Exit codes:
    0   every anchored cross-file number+title reference matches
    1   one or more title claims anchor to a different number
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import (
    CROSS_ADJACENCY_WINDOW as ADJACENCY_WINDOW,
    CROSS_BINDING_SENTINEL as BINDING_SENTINEL,
    CROSS_EXTERNAL_CONTEXT_RE as EXTERNAL_CONTEXT_RE,
    CROSS_MD_LINK_RE as MD_LINK_RE,
    CROSS_REF_PATTERNS as REF_PATTERNS,
    REPO_ROOT,
    iter_markdown_targets,
    iter_non_code_lines,
    read_text_safe,
)

DEFAULT_PATHS = [str(REPO_ROOT)]

# Basename exemptions (historical/meta narration of reference shapes),
# matching gate 62's set.
EXEMPT_FILES = frozenset(
    {
        "CHANGELOG.md",
        "TODO.md",
    }
)

# Relative-path exemptions: the pack README's version-history table
# narrates past pack-rule reference shapes frozen as-of-write (rows
# citing a rule's sections by number and title as they were when the
# row was written). Exempting by relpath keeps the root README scanned.
EXEMPT_RELPATHS = frozenset(
    {
        "dev-security/claude-rules/README.md",
    }
)

# --- Copied from lint-cross-file-section-refs.py (gate 62); see the
# --- docstring provenance note. Keep in sync with that gate. The five
# --- shared extraction constants (REF_PATTERNS, MD_LINK_RE,
# --- BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, ADJACENCY_WINDOW) are no
# --- longer copied: they are imported from lint_common's CROSS_* block
# --- (the 2026-07-04 guardrail-review G-4 hoist), so only HEADING_RE
# --- and the helper functions below remain copy-with-comment.
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")
# --- End of the gate-62 copied block.

# Gate 62's HEADING_RE with a title capture group: markdown headings
# only (inline clauses carry no title, so the names phase skips them).
TITLE_HEADING_RE = re.compile(
    r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]\s*(.*)$"
)

# Title-candidate shapes immediately after a reference: a parenthetical
# or a (optionally comma-led) double-quoted run.
PAREN_TITLE_RE = re.compile(r"^\s*\(([^)]{2,120})\)")
QUOTE_TITLE_RE = re.compile(r'^\s*,?\s*["“]([^"”]{2,120})["”]')


def normalize_title(raw: str) -> str:
    collapsed = " ".join(raw.split())
    return collapsed.rstrip(".:").strip().lower()


def extract_titles(text: str) -> dict[str, str]:
    """Map heading number to normalized title (markdown headings only)."""
    titles: dict[str, str] = {}
    for _lineno, line in iter_non_code_lines(text):
        match = TITLE_HEADING_RE.match(line)
        if match:
            number = match.group(2).rstrip(".")
            title = normalize_title(match.group(3))
            if title:
                titles.setdefault(number, title)
    return titles


def resolve_target(source: Path, target_rel: str) -> Path | None:
    """Resolve a markdown link target relative to the citing file."""
    try:
        candidate = (source.parent / target_rel).resolve()
    except (OSError, ValueError):
        return None
    if not candidate.is_file():
        return None
    try:
        candidate.relative_to(REPO_ROOT)
    except ValueError:
        return None
    return candidate


def binding_target(line: str, source: Path) -> Path | None:
    """Return the binding target for a sentinel line (last link before it)."""
    sentinel_at = line.find(BINDING_SENTINEL)
    if sentinel_at < 0:
        return None
    best: str | None = None
    for match in MD_LINK_RE.finditer(line):
        if match.end() <= sentinel_at:
            best = match.group(1)
    if best is None:
        return None
    return resolve_target(source, best)


def adjacent_link(line: str, ref_start: int, ref_end: int) -> str | None:
    """Return the .md link within the adjacency window of a reference."""
    best: tuple[int, str] | None = None
    for match in MD_LINK_RE.finditer(line):
        if match.end() <= ref_start:
            gap = ref_start - match.end()
            between = line[match.end() : ref_start]
        elif match.start() >= ref_end:
            gap = match.start() - ref_end
            between = line[ref_end : match.start()]
        else:
            continue
        if gap > ADJACENCY_WINDOW or "|" in between:
            continue
        if best is None or gap < best[0]:
            best = (gap, match.group(1))
    return best[1] if best else None


def title_candidate(line: str, ref_end: int) -> str | None:
    """Return the raw title candidate immediately after a reference."""
    tail = line[ref_end:]
    for pattern in (PAREN_TITLE_RE, QUOTE_TITLE_RE):
        match = pattern.match(tail)
        if match:
            return match.group(1)
    return None


def check_file(path: Path) -> list[str]:
    """Return finding strings for one markdown file."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    title_cache: dict[Path, dict[str, str]] = {}
    bound_target: Path | None = None

    def target_titles(target: Path) -> dict[str, str]:
        if target not in title_cache:
            target_text = read_text_safe(target)
            title_cache[target] = (
                extract_titles(target_text) if target_text is not None else {}
            )
        return title_cache[target]

    for lineno, line in iter_non_code_lines(text):
        candidate_binding = binding_target(line, path)
        if candidate_binding is not None:
            bound_target = candidate_binding
            continue
        if EXTERNAL_CONTEXT_RE.search(line):
            continue
        for pattern in REF_PATTERNS:
            for match in pattern.finditer(line):
                number = match.group(1).rstrip(".")
                raw_title = title_candidate(line, match.end())
                if raw_title is None:
                    continue
                link = adjacent_link(line, match.start(), match.end())
                if link is not None:
                    target = resolve_target(path, link)
                elif bound_target is not None:
                    target = bound_target
                else:
                    continue
                if target is None or target == path:
                    continue
                titles = target_titles(target)
                if not titles:
                    continue
                claimed = normalize_title(raw_title)
                if not claimed:
                    continue
                # The anchoring rule: only a candidate that IS some
                # heading title in the target is a title claim.
                anchor_numbers = [n for n, t in titles.items() if t == claimed]
                if not anchor_numbers:
                    continue
                own_title = titles.get(number)
                if own_title is None:
                    if "|" in line:
                        # Table row: gate 62 excludes it, so the
                        # anchored-title + absent-number shape is
                        # this gate's to fail (the r4 O-1 seam).
                        anchors = ", ".join(sorted(anchor_numbers))
                        findings.append(
                            f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                            f"cross-file reference §{number} ({raw_title}) "
                            f"names the title of heading §{anchors} of "
                            f"{target.relative_to(REPO_ROOT)}, but §{number} "
                            f"is not a numbered heading there"
                        )
                    # Non-table: gate 62 owns existence; an inline
                    # clause has no title to verify.
                    continue
                if own_title != claimed:
                    anchors = ", ".join(sorted(anchor_numbers))
                    findings.append(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: cross-file "
                        f"reference §{number} ({raw_title}) names a title "
                        f"that is heading §{anchors}, not §{number}, of "
                        f"{target.relative_to(REPO_ROOT)}"
                    )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv)

    findings: list[str] = []
    scanned = 0
    for path in iter_markdown_targets([Path(p) for p in args.paths]):
        if path.name in EXEMPT_FILES:
            continue
        try:
            rel = str(path.relative_to(REPO_ROOT))
        except ValueError:
            rel = ""
        if rel in EXEMPT_RELPATHS:
            continue
        scanned += 1
        findings.extend(check_file(path))

    if findings:
        for finding in findings:
            print(finding)
        print(
            f"\nFAIL: {len(findings)} cross-file section-name mismatch(es). "
            "A reference pairing a number with a heading title must cite the "
            "title's actual number in the target; fix the citer (or the "
            "target's numbering), do not weaken this check."
        )
        return 1

    print(
        f"OK: all anchored cross-file number+title references match their "
        f"targets (scanned {scanned} files)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
