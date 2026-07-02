#!/usr/bin/env python3
"""Section-placement audit for the GRC Documentation Library.

The library's documents follow strong placement conventions for a small
set of recognizable section types. This linter codifies those
conventions so future drift is caught mechanically rather than relying
on review to catch it. The conventions were surfaced by a corpus-wide
section-ordering survey (recorded in the CHANGELOG entry for the PR
that introduces this audit) which found that the placement rules below
are universally observed across the existing corpus.

Placement rules enforced:

  SP-01  Orientation sections (Purpose, Scope, Purpose and Scope,
         Overview, Applicability, Introduction, Executive Summary)
         must appear in the top three ``##`` sections. Applies to
         all in-scope documents.

  SP-03  Version-history sections (Version history, Release history,
         Changelog) must appear in the bottom three ``##`` sections.
         Applies to all in-scope documents.

  SP-04  Licence sections (Licence, License, Licence boundary,
         License boundary, Licence and third-party reference boundary,
         License and third-party reference boundary) must appear in
         the bottom three ``##`` sections. Applies to all in-scope
         documents.

"Bottom three" and "top three" are based on the count of ``##``
sections in the file; for files with three or fewer ``##`` sections,
the constraints are trivially satisfied.

Matching is case-insensitive and uses exact match against the
normalized section heading (with leading numbering, "Section N", and
common punctuation stripped first). Exact matching is used rather than
prefix or substring matching to avoid false positives on sections that
legitimately reuse a canonical orientation or closing word in a
different sense (for example, "Applicability decision tree" is not an
orientation section even though its heading begins with
"Applicability"; "Licence compatibility rules" is not the document's
own licence section even though it begins with "Licence"; a closing
"Summary" at the end of a guide is a recap, not an orientation
introduction).

Notable rule the corpus-wide section-ordering survey identified but
this audit does not enforce:

- A "Framework alignment placement" rule (SP-02 in the survey draft)
  is not enforced. The survey found that Policy/Standard/Framework/
  Procedure documents universally place Framework alignment near the
  bottom, but two of the project's policies legitimately follow
  Framework alignment with administrative tail sections (Exceptions,
  Enforcement, Compliance mapping table, Definitions). A reliable rule
  would have to express "Framework alignment must be after the
  substantive body sections" rather than a simple bottom-N position
  constraint, which is more complex than the prefix/exact patterns
  this audit uses. Deferred until the project decides whether to enforce
  relative-order rules in addition to absolute-position rules.

Scope:

  Markdown files reachable from the default repository scan paths,
  excluding the DEFAULT_EXEMPT_DIRS set from ``lint_common`` (which
  covers ``.git``, ``node_modules``, ``__pycache__``, ``.claude``).
  Files marked ``Classification: Deprecated`` are skipped. No per-tool
  exempt path prefixes are applied: the placement rules use exact-match
  section-name lookups so they do not produce false positives on
  documents in other directories, and explicit fixture paths (used by
  the gate-36 regression test suite) are scanned the same as any other
  passed-in argument.

Usage:
    python3 tools/lint-section-placement.py
    python3 tools/lint-section-placement.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more placement findings
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

DOCTYPE_RE = re.compile(r"^\*\*Document Type:\*\*\s+(.+?)(?:\\)?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")

EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS

# Each rule: (rule_id, description, canonical_heading_names, position, applicable_doctypes_or_none)
# - canonical_heading_names: case-insensitive exact-match set; a section heading
#   matches the rule if (after normalization) it equals any of these names.
# - position: ("top", N) means the matched section must be in the first N
#   ``##`` sections; ("bottom", N) means in the last N ``##`` sections.
# - applicable_doctypes_or_none: None means apply to all in-scope files
#   (regardless of doctype, including README and meta files); a tuple of
#   doctype names means apply only when the file's Document Type matches one
#   of those names.
PLACEMENT_RULES: list[tuple[str, str, frozenset[str], tuple[str, int], tuple[str, ...] | None]] = [
    (
        "SP-01",
        "orientation sections (Purpose, Scope, Purpose and Scope, Overview, "
        "Applicability, Introduction, Executive Summary) must be in the top "
        "three sections",
        frozenset({
            "purpose",
            "scope",
            "purpose and scope",
            "overview",
            "applicability",
            "introduction",
            "executive summary",
        }),
        ("top", 3),
        None,
    ),
    (
        "SP-03",
        "version history sections (Version history, Release history, Changelog) "
        "must be in the bottom three sections",
        frozenset({
            "version history",
            "release history",
            "changelog",
        }),
        ("bottom", 3),
        None,
    ),
    (
        "SP-04",
        "licence sections (Licence, License, Licence boundary, License boundary, "
        "Licence and third-party reference boundary, License and third-party "
        "reference boundary) must be in the bottom three sections",
        frozenset({
            "licence",
            "license",
            "licence boundary",
            "license boundary",
            "licence and third-party reference boundary",
            "license and third-party reference boundary",
        }),
        ("bottom", 3),
        None,
    ),
]


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    # Skip documents marked Classification: Deprecated.
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Classification:\*\*\s+Deprecated", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        return False
    return True


def extract_doctype(text: str) -> str | None:
    m = DOCTYPE_RE.search(text)
    if not m:
        return None
    return m.group(1).strip().rstrip("\\").strip()


def normalise_heading(heading: str) -> str:
    """Return the heading lower-cased with leading numbering stripped.

    Strips patterns like ``1. ``, ``1.2 ``, ``Section 4: ``, and common
    trailing whitespace so exact matching works against the human-facing
    section name, not the formatting markers.
    """
    cleaned = re.sub(r"^\d+(\.\d+)*[.\s:]*", "", heading)
    cleaned = re.sub(r"^Section\s+\d+(\.\d+)*[.\s:]*", "", cleaned)
    return cleaned.strip().lower()


def extract_headings(text: str) -> list[tuple[int, str]]:
    """Return the ``##`` section headings as (sequence_index, normalised_heading).

    Code-fenced lines are skipped via ``iter_non_code_lines``. The
    sequence_index starts at 0 for the first ``##`` heading.
    """
    headings: list[tuple[int, str]] = []
    idx = 0
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            headings.append((idx, normalise_heading(m.group(1))))
            idx += 1
    return headings


def check_placement(
    headings: list[tuple[int, str]],
    rule: tuple[str, str, frozenset[str], tuple[str, int], tuple[str, ...] | None],
) -> list[str]:
    """Apply one placement rule against a file's section list.

    Returns a list of finding messages (empty if the rule is satisfied or
    no matching section is present).
    """
    rule_id, description, names, position, _doctypes = rule
    total = len(headings)
    if total == 0:
        return []
    findings: list[str] = []
    for seq, heading in headings:
        if heading not in names:
            continue
        constraint_kind, n = position
        if constraint_kind == "top":
            # Allowed positions: 0..n-1 (zero-indexed).
            allowed = seq < n
            if not allowed:
                findings.append(
                    f"[{rule_id}] section #{seq + 1} of {total} "
                    f"({heading!r}) should appear in the top {n} sections; "
                    f"{description}"
                )
        elif constraint_kind == "bottom":
            # Allowed positions: total-n..total-1 (zero-indexed).
            allowed = seq >= max(0, total - n)
            if not allowed:
                findings.append(
                    f"[{rule_id}] section #{seq + 1} of {total} "
                    f"({heading!r}) should appear in the bottom {n} sections; "
                    f"{description}"
                )
    return findings


def scan(path: Path) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    doctype = extract_doctype(text)
    headings = extract_headings(text)
    if not headings:
        return findings
    for rule in PLACEMENT_RULES:
        _rid, _desc, _pre, _pos, doctypes = rule
        if doctypes is not None:
            if doctype is None or doctype not in doctypes:
                continue
        findings.extend(check_placement(headings, rule))
    return findings


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return sorted(targets)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce section-placement conventions across the markdown corpus."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[str]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(
            f"OK: all documents satisfy section-placement conventions "
            f"(scanned {len(targets)} files)."
        )
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for msg in findings:
            print(f"  {msg}")
        total += len(findings)
    print(
        f"\nFAIL: {total} section-placement finding(s) across "
        f"{len(grouped)} file(s)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
