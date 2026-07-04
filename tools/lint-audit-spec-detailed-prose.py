#!/usr/bin/env python3
"""Audit-spec detailed-prose presence audit.

The audit programme's specification
(``governance/specification-audit-programme.md``) carries, beyond the
mechanically-gated section-6 inventory table, a detailed-prose
enumeration: each gate's ``Gate N is ...`` description paragraph and,
for the tail-appended gates, a ``Gate N is appended ...`` ordering
sentence. Gate 35 checks only the inventory table's parity with the
three runtime surfaces, and gate 39 only counts the table's rows;
neither verifies the per-gate detailed prose's presence, so a shipped
gate whose prose pair was never written recurs silently (gate 57's pair was absent for
several PRs until Sweep 77 found it; gate 55's description initially
landed in section 5 instead; gates 43 and 44 carried no detailed prose
at all until the backfill that shipped with this gate).

This linter closes that seam with a PRESENCE-ONLY check (deliberately
not semantic: whether the prose accurately describes the gate remains
sweep-and-review territory):

- It parses the section-6 inventory table for the gate numbers,
  scoped to the section-6 region (a numeric-first-cell table elsewhere
  in the spec must not inflate the gate set; the same #577-motivated
  scoping gate 60 applies).
- For each gate at or above ``DESCRIPTION_FLOOR`` (35), the spec body
  must contain a ``Gate N is `` sentence opener (the description).
- For each gate at or above ``APPENDED_FLOOR`` (47), the spec body
  must also contain ``Gate N is appended`` (the tail-ordering
  sentence).

The floors reflect the convention's actual adoption history (the
2026-07-03 census, re-run at build time): gates below 35 are described
in section 5's grouped lists and the section-6 preamble using plural
and placement variants, and the appended-order sentence became the
per-gate convention at gate 47. Raising either floor retroactively
would demand prose archaeology with no drift-prevention payoff; new
gates always land above both floors.

Usage:
    python3 tools/lint-audit-spec-detailed-prose.py
    python3 tools/lint-audit-spec-detailed-prose.py --spec path/to/spec.md

Exit codes:
    0   every in-scope gate carries its required prose
    1   one or more gates are missing a description or appended sentence
    2   the spec file is missing or carries no parseable inventory rows
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = "governance/specification-audit-programme.md"

DESCRIPTION_FLOOR = 35
APPENDED_FLOOR = 47

# Section-6 inventory rows: | N | Gate name | script link |
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")

# Scope the row scan to the section-6 region so a numeric-first-cell
# table elsewhere in the spec cannot inflate the gate set (gate 60's
# #577-motivated scoping, mirrored).
SECTION_6_RE = re.compile(r"^##\s+6[.\s]")
SECTION_END_RE = re.compile(r"^##\s+(?!6[.\s])")


def parse_gate_numbers(text: str) -> list[int]:
    numbers: list[int] = []
    in_section_6 = False
    for line in text.splitlines():
        if SECTION_6_RE.match(line):
            in_section_6 = True
            continue
        if in_section_6 and SECTION_END_RE.match(line):
            in_section_6 = False
            continue
        if not in_section_6:
            continue
        m = ROW_RE.match(line)
        if m:
            numbers.append(int(m.group(1)))
    return numbers


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Presence check for the audit spec's per-gate detailed prose."
    )
    parser.add_argument("--spec", default=str(REPO_ROOT / SPEC_PATH))
    args = parser.parse_args(argv[1:])

    spec = Path(args.spec)
    if not spec.is_file():
        print(f"ERROR: spec file not found: {spec}")
        return 2
    text = spec.read_text(encoding="utf-8")

    gates = parse_gate_numbers(text)
    if not gates:
        print(f"ERROR: no §6 gate-inventory rows parsed from {spec}")
        return 2

    missing: list[str] = []
    checked_desc = 0
    checked_app = 0
    for n in sorted(set(gates)):
        if n >= DESCRIPTION_FLOOR:
            checked_desc += 1
            if f"Gate {n} is " not in text:
                missing.append(
                    f"gate {n}: no 'Gate {n} is ...' description sentence in the spec prose"
                )
        if n >= APPENDED_FLOOR:
            checked_app += 1
            if f"Gate {n} is appended" not in text:
                missing.append(
                    f"gate {n}: no 'Gate {n} is appended ...' ordering sentence in the spec prose"
                )

    if missing:
        print(f"=== {spec} ===")
        for item in missing:
            print(f"  [detailed-prose] {item}")
        print(
            f"\nFAIL: {len(missing)} missing detailed-prose element(s). Each gate at or "
            f"above {DESCRIPTION_FLOOR} carries a 'Gate N is ...' description and each at "
            f"or above {APPENDED_FLOOR} a 'Gate N is appended ...' sentence; write the "
            "missing prose in the spec's section 6, do not weaken this check."
        )
        return 1

    print(
        f"OK: all in-scope gates carry their detailed prose "
        f"({checked_desc} description(s) from gate {DESCRIPTION_FLOOR}, "
        f"{checked_app} appended-order sentence(s) from gate {APPENDED_FLOOR}; "
        f"{len(set(gates))} inventory rows parsed)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
