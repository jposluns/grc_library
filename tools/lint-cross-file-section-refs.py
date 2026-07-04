#!/usr/bin/env python3
"""Validate cross-file section references (numbers phase).

The names phase (gate 65, ``lint-cross-file-section-names.py``) layers
title-fit checking on top of this gate's number-existence checking; its
docstring documents the deliberate scope deltas (table rows scanned
there, the pack-README relpath exemption, the table-row absent-number
ownership).

Library documents cite sections of OTHER corpus documents by number,
e.g. "see [the mobile standard](standard-mobile-application-security.md)
§5.4" or, via a binding declaration, a file-wide "Section numbers below
refer to that standard." sentinel after which bare §N references bind to
the declared target. When the target document is renumbered, such
references silently go stale: the intra-document gate
(``lint-intra-doc-refs.py``) deliberately filters cross-document context
out, so this class was gate-blind (the #548 and #545 escaped-miss
clusters that motivated this gate; design record in
``.working/cross-file-section-ref-gate-design.md``).

This linter fires ONLY on the two high-confidence resolvable-target
classes the 2026-07-02 corpus survey identified:

1. **Adjacent-link class** (non-table lines only): a ``§N`` /
   ``Section N`` reference with a markdown ``.md`` link within
   ``ADJACENCY_WINDOW`` characters on the same line and no intervening
   table pipe. The link names the target; the cited number must be a
   numbered heading or a line-initial inline clause in that target.
2. **Binding-declaration class**: a line carrying the sentinel
   ``Section numbers below refer to that standard.`` together with a
   ``.md`` link binds every SUBSEQUENT bare ``§N`` / ``Section N`` in
   the file to that target. The binding target is the last link ending
   BEFORE the sentinel (the language rule files list sibling documents
   earlier on the line; taking the first link mis-bound 63 references
   in the first cut).

Documented exclusions (recall costs, not gaps; each was a measured
false-positive source in the survey):

- Table rows (any line containing a pipe): the compliance-matrix and
  per-document framework tables place external-framework clause numbers
  in cells adjacent to corpus-document links.
- External-standard context lines (ISO / IEC / NIST / OWASP / GDPR /
  BASC / CSA / COBIT / ``Clause`` / ``Article`` / ``SP 800`` and
  similar): the section number cites the external standard.
- Targets with zero numbered headings and zero inline clauses: a
  numbered reference to an unnumbered document is not a stale-heading
  case (mirrors ``lint-intra-doc-refs.py``'s early return).
- Bare references with no adjacent link and no active binding: the
  intra-document gate owns those, except for the accepted heuristic
  band a link 41-60 chars from the reference occupies (outside this
  gate's 40-char adjacency window, inside gate 18's 60-char cross-doc
  disclaim window; documented in ``lint-intra-doc-refs.py``'s
  docstring, symmetric on both sides of the reference).
- Name-based references and range second endpoints: no (second) number
  to resolve.

Usage:
    python3 tools/lint-cross-file-section-refs.py
    python3 tools/lint-cross-file-section-refs.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more cross-file section references that do not resolve
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

# Files whose cross-file section references are by convention historical
# or meta (they quote reference shapes rather than cite live sections).
EXEMPT_FILES = frozenset(
    {
        "CHANGELOG.md",
        "TODO.md",
    }
)

# Same heading model as lint-intra-doc-refs.py.
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")

# The FR-48 canonical section model also numbers line-initial inline
# prose clauses ("4.7.1 All audit reports ...") that are NOT markdown
# headings; corpus citers reference them (`§4.7.1`), so target
# extraction includes them. At least two levels required, which keeps
# single-level markdown ordered-list items ("1. ...") out of the set.
CLAUSE_RE = re.compile(r"^(\d+(?:\.\d+){1,3})\s")

# REF_PATTERNS, MD_LINK_RE, BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, and
# ADJACENCY_WINDOW are the shared cross-file reference-extraction
# constants, hoisted into lint_common (the CROSS_* block) by the
# 2026-07-04 guardrail-review G-4 so this gate and the names-phase
# sibling (gate 65) cannot drift; imported above under the local names
# this module has always used.


def extract_sections(text: str) -> set[str]:
    """Return the numeric heading and inline-clause identifiers of a document."""
    sections: set[str] = set()
    for _lineno, line in iter_non_code_lines(text):
        match = HEADING_RE.match(line)
        if match:
            sections.add(match.group(2).rstrip("."))
            continue
        clause = CLAUSE_RE.match(line)
        if clause:
            sections.add(clause.group(1))
    return sections


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
    """Return the .md link within the adjacency window of a reference.

    The nearest link (either side) within ``ADJACENCY_WINDOW`` characters
    wins; a table pipe between the reference and the link breaks
    adjacency (defence in depth; table lines are skipped wholesale).
    """
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


def check_file(path: Path) -> list[str]:
    """Return finding strings for one markdown file."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    section_cache: dict[Path, set[str]] = {}
    bound_target: Path | None = None

    def target_sections(target: Path) -> set[str]:
        if target not in section_cache:
            target_text = read_text_safe(target)
            section_cache[target] = (
                extract_sections(target_text) if target_text is not None else set()
            )
        return section_cache[target]

    for lineno, line in iter_non_code_lines(text):
        candidate_binding = binding_target(line, path)
        if candidate_binding is not None:
            bound_target = candidate_binding
            continue
        if "|" in line:
            continue
        if EXTERNAL_CONTEXT_RE.search(line):
            continue
        for pattern in REF_PATTERNS:
            for match in pattern.finditer(line):
                number = match.group(1).rstrip(".")
                link = adjacent_link(line, match.start(), match.end())
                if link is not None:
                    target = resolve_target(path, link)
                elif bound_target is not None:
                    target = bound_target
                else:
                    continue
                if target is None or target == path:
                    continue
                sections = target_sections(target)
                if not sections:
                    continue
                if number not in sections:
                    findings.append(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: cross-file reference "
                        f"§{number} does not resolve to a numbered heading or "
                        f"inline clause in {target.relative_to(REPO_ROOT)}"
                    )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv)

    findings: list[str] = []
    for path in iter_markdown_targets([Path(p) for p in args.paths]):
        if path.name in EXEMPT_FILES:
            continue
        findings.extend(check_file(path))

    if findings:
        for finding in findings:
            print(f"FAIL {finding}")
        print(f"FAIL: {len(findings)} unresolved cross-file section reference(s).")
        return 1
    print("OK: all cross-file section references resolve against their targets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
