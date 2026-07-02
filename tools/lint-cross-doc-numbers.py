#!/usr/bin/env python3
"""Detect cross-document numerical drift on canonical-term thresholds.

Library documents repeatedly mention certain numeric thresholds. When the
same threshold appears with different values in different documents, the
inconsistency is a real defect that adopters will encounter.

This linter is deliberately conservative: it focuses on a curated set of
canonical terms with well-defined numeric values, extracted via specific
regex. False positives are minimized by requiring the term to appear
close to the number on the same line.

Terms currently tracked (see TERM_PATTERNS for the live set):

  - P1 acknowledgement time + unit
  - P2 acknowledgement time + unit
  - P3 acknowledgement time + unit
  - GDPR breach-notification window (in hours)

The P1/P2/P3 acknowledgement patterns are deliberately narrow per the
Phase 23.26 false-positive analysis. They match 0 documents on the
current corpus and exist as scaffolding for a future expansion. Future
Phase 23.35 explicitly does NOT broaden them to resolution / MTTR /
convene / notification times because the empirical data confirms each
SLA dimension legitimately carries different per-Pn values across the
corpus.

The GDPR-breach-notification pattern was added in Phase 23.35 after
empirical confirmation that 8+ documents reference the statutory
72-hour deadline and all currently agree on the value. The regex
requires GDPR (or UK GDPR) to appear before an N-hours fragment on the
same line, capturing the number. Any divergent value introduced by a
future edit will produce a finding.

RTO, RPO, retention periods, P4 acknowledgement, NIS 2 reporting
windows, and DORA reporting windows are not curated. They are either
context-dependent (RTO/RPO vary by tier and adopter), have multiple
legitimate sub-deadlines that need per-deadline patterns (NIS 2 has
24-hour early-warning, 72-hour report, 1-month final), or appear too
few times in the corpus to justify a curated pattern (DORA 4-hour
appears in one document).

The unit normalizer (UNIT_TO_MINUTES) converts minutes, hours, days, and
business days to minutes for comparison, so a document saying "60
minutes" and another saying "1 hour" do not produce a false positive.

Usage:
    python3 tools/lint-cross-doc-numbers.py

Exit codes:
    0   no divergence detected (each tracked term has at most one
        canonical value across the scanned corpus)
    1   divergence detected: the same term carries different values
        across documents
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import REPO_ROOT, iter_markdown_targets, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_FILES = {
    # The CHANGELOG quotes specific numeric thresholds when describing
    # the linter's term set; treating it as a target would produce
    # spurious "divergent value" findings against its own historical
    # narrative.
    "CHANGELOG.md",
}
# Phase 23.62 removed `lint-cross-doc-numbers.py` from this set: the
# linter scans `.md` only, so the .py entry was unreachable. Phase
# 23.64 added the inline justification above for the remaining
# CHANGELOG entry (previously undocumented).

# Each pattern extracts (term, value_text). The match must be a substring
# of a single line to avoid spurious cross-line matches.
#
# Patterns capture both the time/duration value AND a unit, normalizing
# minute/hour/day equivalences during comparison.
TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    "P1-acknowledgement": re.compile(
        r"\bP1[^.\n]{0,80}?acknowledg(?:e|ement)[^.\n]{0,40}?(\d+)\s*(minute|hour|day|business day)s?",
        re.IGNORECASE,
    ),
    "P2-acknowledgement": re.compile(
        r"\bP2[^.\n]{0,80}?acknowledg(?:e|ement)[^.\n]{0,40}?(\d+)\s*(minute|hour|day|business day)s?",
        re.IGNORECASE,
    ),
    "P3-acknowledgement": re.compile(
        r"\bP3[^.\n]{0,80}?acknowledg(?:e|ement)[^.\n]{0,40}?(\d+)\s*(minute|hour|day|business day)s?",
        re.IGNORECASE,
    ),
    # GDPR (and UK GDPR) breach notification: Article 33 sets a 72-hour
    # deadline. Captures the first N-hour fragment after "GDPR" on the
    # same line, requiring "breach", "notif", "report", or "notify" to
    # appear within the same window to narrow the FP surface. Statutory:
    # any value other than 72 indicates a defect.
    "GDPR-breach-notification-hours": re.compile(
        r"\b(?:UK\s+)?GDPR\b[^.\n]{0,250}?(?:breach|notif|notify|report)[^.\n]{0,150}?(\d+)[\s\-]*(hour)s?\b",
        re.IGNORECASE,
    ),
}

UNIT_TO_MINUTES = {
    "minute": 1,
    "hour": 60,
    "day": 60 * 24,
    "business day": 60 * 8,  # 8-hour business day
}


def normalise(value: int, unit: str) -> int:
    """Return value in minutes."""
    unit_clean = unit.lower().rstrip("s")
    return value * UNIT_TO_MINUTES.get(unit_clean, 0)


def scan(path: Path) -> dict[str, set[tuple[int, str]]]:
    """Return {term: {(normalised_minutes, raw_text), ...}} for the file."""
    out: dict[str, set[tuple[int, str]]] = defaultdict(set)
    text = read_text_safe(path)
    if text is None:
        return out
    for _lineno, line in iter_non_code_lines(text):
        for term, pattern in TERM_PATTERNS.items():
            for m in pattern.finditer(line):
                value = int(m.group(1))
                unit = m.group(2)
                norm = normalise(value, unit)
                raw = f"{value} {unit}"
                out[term].add((norm, raw))
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect cross-document numerical drift on canonical-term thresholds."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_markdown_targets(args.paths, exempt_files=EXEMPT_FILES)
    # term -> {normalised_value -> [(doc, raw_text)]}
    aggregate: dict[str, dict[int, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for t in targets:
        rel = t.relative_to(REPO_ROOT).as_posix() if t.is_relative_to(REPO_ROOT) else str(t)
        per_file = scan(t)
        for term, value_set in per_file.items():
            for norm, raw in value_set:
                aggregate[term][norm].append((rel, raw))
    divergent: list[tuple[str, dict[int, list[tuple[str, str]]]]] = []
    for term, values in aggregate.items():
        if len(values) > 1:
            divergent.append((term, values))
    if not divergent:
        terms_count = len(aggregate)
        print(f"OK: no cross-document numerical drift detected ({terms_count} tracked term(s); scanned {len(targets)} files).")
        return 0
    for term, values in divergent:
        print(f"=== {term} ===")
        for norm, occurrences in sorted(values.items()):
            print(f"  {norm} minutes ({occurrences[0][1]}): {len(occurrences)} occurrence(s)")
            for doc, raw in occurrences[:5]:
                print(f"    - {doc}: {raw}")
            if len(occurrences) > 5:
                print(f"    ...and {len(occurrences) - 5} more")
    print(f"\nFAIL: {len(divergent)} term(s) with divergent values across documents.")
    print(
        "The same canonical term carries different numeric values in different "
        "documents. Reconcile to a single canonical value, or document the "
        "reason for variance per scope."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
