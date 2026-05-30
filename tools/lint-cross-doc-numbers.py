#!/usr/bin/env python3
"""Detect cross-document numerical drift on canonical-term thresholds.

Library documents repeatedly mention certain numeric thresholds: incident
acknowledgement times (P1/P2/P3/P4), retention periods, RTO/RPO values.
When the same threshold appears with different values in different
documents, the inconsistency is a real defect that adopters will encounter.

This linter is deliberately conservative: it focuses on a curated set
of canonical terms with well-defined numeric values, extracted via
specific regex. False positives are minimised by requiring the term to
appear close to the number.

Terms tracked:
- P1 / P2 / P3 / P4 acknowledgement (or response) time + unit
- RTO / RPO values
- Retention periods in years

Usage:
    python3 tools/lint-cross-doc-numbers.py

Exit codes:
    0   no divergence detected (each term has at most one canonical value)
    1   divergence detected: the same term carries different values across documents
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

EXEMPT_FILES = {
    "lint-cross-doc-numbers.py",
    "CHANGELOG.md",
}

# Each pattern extracts (term, value_text). The match must be a substring
# of a single line to avoid spurious cross-line matches.
#
# Patterns capture both the time/duration value AND a unit, normalising
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


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def scan(path: Path) -> dict[str, set[tuple[int, str]]]:
    """Return {term: {(normalised_minutes, raw_text), ...}} for the file."""
    out: dict[str, set[tuple[int, str]]] = defaultdict(set)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return out
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for term, pattern in TERM_PATTERNS.items():
            for m in pattern.finditer(line):
                value = int(m.group(1))
                unit = m.group(2)
                norm = normalise(value, unit)
                raw = f"{value} {unit}"
                out[term].add((norm, raw))
    return out


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
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect cross-document numerical drift on canonical-term thresholds."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
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
