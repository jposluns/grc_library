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

The DELTA-CHECK half (the r4 G-3 extension, decided 2026-07-04): the
section-6.1 PR-only delta gates were the same seam one layer down
(numeric-gate-only coverage), so when the spec carries a ``| Dn |``
delta-gate table the linter additionally verifies:

- every table row ``Dn`` has a ``Delta gate Dn `` narrative opener in
  the spec prose (the per-check description every D check carries);
- the table's Gate-name cells and the parity linter's
  ``WORKFLOW_DELTA_GATE_STEPS`` registry (loaded from
  ``tools/lint-audit-gate-parity.py``; entries marked
  ``(informational)`` exempt) match EXACTLY in both directions, so a
  registry entry for a removed delta check, or a new table row never
  registered, fails loud instead of dying silently (the registry is
  exclusion-only for gate 35, which is why gate 35 cannot catch it).

A spec with no delta-gate table skips the delta half (the fixture
case); a spec whose section-6.1 heading is present but whose table
parses to zero rows is a parse failure (exit 2). Deleting section 6.1
outright from the real spec is outside this gate's reach and stays
review territory.

Usage:
    python3 tools/lint-audit-spec-detailed-prose.py
    python3 tools/lint-audit-spec-detailed-prose.py --spec path/to/spec.md
    python3 tools/lint-audit-spec-detailed-prose.py \
        --spec path/to/spec.md --parity-script path/to/parity.py

Exit codes:
    0   every in-scope gate carries its required prose
    1   one or more gates are missing prose, or the delta registry and
        table disagree
    2   the spec file is missing, carries no parseable inventory rows,
        has a delta-gate heading with no parseable rows, or the parity
        script / registry cannot be loaded when the delta half runs
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = "governance/specification-audit-programme.md"
PARITY_SCRIPT_PATH = "tools/lint-audit-gate-parity.py"

DESCRIPTION_FLOOR = 35
APPENDED_FLOOR = 47

# Section-6 inventory rows: | N | Gate name | script link |
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")

# Section-6.1 delta-gate rows: | Dn | Gate name | script link | surface |
DELTA_ROW_RE = re.compile(r"^\|\s*D(\d+)\s*\|\s*([^|]+?)\s*\|")

# The section-6.1 heading (presence with zero parseable rows is a
# parse failure, not a skip).
DELTA_HEADING_RE = re.compile(r"^###\s+6\.1\b")

# Registry entries carrying this marker are workflow steps excluded
# from gate 35's parity for reasons other than being a delta gate;
# they have no table row by design.
INFORMATIONAL_MARKER = "(informational)"

# Scope the row scan to the section-6 region so a numeric-first-cell
# table elsewhere in the spec cannot inflate the gate set (gate 60's
# #577-motivated scoping, mirrored). The ### 6.1 subsection stays
# inside this region (its heading matches neither boundary regex).
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


def parse_delta_rows(text: str) -> tuple[dict[int, str], bool]:
    """Return ``({Dn number: gate-name cell}, heading_present)`` for the
    section-6 region's delta-gate table."""
    rows: dict[int, str] = {}
    heading = False
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
        if DELTA_HEADING_RE.match(line):
            heading = True
            continue
        m = DELTA_ROW_RE.match(line)
        if m:
            rows[int(m.group(1))] = m.group(2)
    return rows, heading


def load_delta_registry(parity_script: Path) -> set[str] | None:
    """Load ``WORKFLOW_DELTA_GATE_STEPS`` from the parity linter;
    ``None`` on any load failure (the caller fails loud)."""
    try:
        spec = importlib.util.spec_from_file_location(
            "lint_audit_gate_parity", parity_script
        )
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        registry = getattr(module, "WORKFLOW_DELTA_GATE_STEPS", None)
        if not isinstance(registry, (set, frozenset)):
            return None
        return set(registry)
    except Exception:
        return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Presence check for the audit spec's per-gate detailed prose."
    )
    parser.add_argument("--spec", default=str(REPO_ROOT / SPEC_PATH))
    parser.add_argument(
        "--parity-script", default=str(REPO_ROOT / PARITY_SCRIPT_PATH)
    )
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

    delta_rows, delta_heading = parse_delta_rows(text)
    if delta_heading and not delta_rows:
        print(
            f"ERROR: the spec's section-6.1 delta-gate heading is present "
            f"but no '| Dn |' rows parsed from {spec}"
        )
        return 2
    if delta_rows:
        for n in sorted(delta_rows):
            if f"Delta gate D{n} " not in text:
                missing.append(
                    f"delta check D{n}: no 'Delta gate D{n} ...' narrative "
                    "sentence in the spec prose"
                )
        registry = load_delta_registry(Path(args.parity_script))
        if registry is None:
            print(
                f"ERROR: could not load WORKFLOW_DELTA_GATE_STEPS from "
                f"{args.parity_script}"
            )
            return 2
        expected = {e for e in registry if INFORMATIONAL_MARKER not in e}
        table_names = set(delta_rows.values())
        for name in sorted(expected - table_names):
            missing.append(
                f"delta registry: WORKFLOW_DELTA_GATE_STEPS entry '{name}' "
                "has no matching section-6.1 table row (stale entry for a "
                "removed check, or an unrecorded rename)"
            )
        for name in sorted(table_names - expected):
            missing.append(
                f"delta table: section-6.1 row '{name}' is not in "
                "WORKFLOW_DELTA_GATE_STEPS (register the workflow step "
                "name, or reconcile the rename)"
            )

    if missing:
        print(f"=== {spec} ===")
        for item in missing:
            print(f"  [detailed-prose] {item}")
        print(
            f"\nFAIL: {len(missing)} missing detailed-prose or delta-parity element(s). "
            f"Each gate at or above {DESCRIPTION_FLOOR} carries a 'Gate N is ...' "
            f"description and each at or above {APPENDED_FLOOR} a 'Gate N is appended "
            "...' sentence; each section-6.1 delta check carries a 'Delta gate Dn ...' "
            "narrative and matches the parity registry exactly; write the missing "
            "prose or reconcile the registry, do not weaken this check."
        )
        return 1

    print(
        f"OK: all in-scope gates carry their detailed prose "
        f"({checked_desc} description(s) from gate {DESCRIPTION_FLOOR}, "
        f"{checked_app} appended-order sentence(s) from gate {APPENDED_FLOOR}; "
        f"{len(set(gates))} inventory rows parsed; "
        f"{len(delta_rows)} delta check(s) narrated and registry-matched)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
