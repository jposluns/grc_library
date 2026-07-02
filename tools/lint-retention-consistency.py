#!/usr/bin/env python3
"""Verify cross-document retention-period consistency.

Several procedures cite an evidence-retention period that must agree with the
canonical value recorded in the Data Retention Schedule register
(`governance/register-data-retention-schedule.md`). When a procedure's stated
retention drifts from the register row it implements (or vice versa), adopters
get contradictory guidance on how long to keep the same records, and the
register's role as the single source of truth is silently broken.

This linter is deliberately narrow and explicit: it checks a curated set of
(register category, procedure) pairs rather than attempting to parse every
retention mention in the corpus. Each pair names a register row (matched by its
first table cell) and a procedure document; the linter extracts the register
row's canonical period and the procedure's "retained for a minimum of ..."
statement, normalizes both to days, and fails if they disagree or if either
citation cannot be found (a missing citation means a document was restructured
in a way that broke the link the register's cross-reference notes rely on).

Tracked pairs (see RETENTION_CHECKS for the live set):

  - CAPA records  <->  compliance/procedure-capa.md
  - Internal audit reports  <->  compliance/standard-internal-audit.md
  - Control testing evidence  <->  compliance/procedure-control-testing.md

All three currently agree at a 7-year floor; the register rows carry explicit
"matches ..." cross-reference notes naming the procedure, and this gate is the
mechanical enforcement of those notes.

Usage:
    python3 tools/lint-retention-consistency.py

Exit codes:
    0   every tracked pair agrees (register canonical == procedure statement)
    1   a mismatch or a missing citation was detected
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

REGISTER = "governance/register-data-retention-schedule.md"

# Each check names a register row (matched on its first table cell, case-
# insensitive, exact after trimming) and the procedure document that must cite
# the same retention period. The procedure value is the period stated after the
# "retained for a minimum of" anchor phrase.
RETENTION_CHECKS: list[dict[str, str]] = [
    {
        "label": "CAPA records evidence-retention",
        "register_category": "CAPA records",
        "procedure": "compliance/procedure-capa.md",
    },
    {
        "label": "Internal-audit evidence-retention",
        "register_category": "Internal audit reports",
        "procedure": "compliance/standard-internal-audit.md",
    },
    {
        "label": "Control-testing evidence-retention",
        "register_category": "Control testing evidence",
        "procedure": "compliance/procedure-control-testing.md",
    },
]

UNIT_TO_DAYS = {"year": 365, "month": 30, "day": 1}

# Captures a "<number> <unit>" period; tolerates a hyphen ("7-year") and the
# markdown bold markers around the value ("**7 years**").
PERIOD_RE = re.compile(r"(\d+)[\s-]*(year|month|day)s?", re.IGNORECASE)

# The procedure's retention statement is anchored on this phrase so the linter
# pins the evidence-retention figure and not an unrelated period (a 12-month
# recurrence window, a 30-day remediation target) elsewhere in the document.
PROCEDURE_ANCHOR_RE = re.compile(
    r"retained for a minimum of[^.\n]*?(\d+)[\s-]*(year|month|day)s?",
    re.IGNORECASE,
)


def normalise(value: int, unit: str) -> int:
    """Return the period in days."""
    return value * UNIT_TO_DAYS.get(unit.lower().rstrip("s"), 0)


def register_value(text: str, category: str) -> tuple[int, str] | None:
    """Return (days, raw) for the register row whose first cell is `category`."""
    cat_lower = category.lower()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if cells[0].lower() == cat_lower:
            # Search the period cell (and the rest of the row) for the first
            # period figure; the canonical value is the first one stated.
            row_rest = " | ".join(cells[1:])
            m = PERIOD_RE.search(row_rest)
            if m:
                return normalise(int(m.group(1)), m.group(2)), f"{m.group(1)} {m.group(2)}"
    return None


def procedure_value(text: str) -> tuple[int, str] | None:
    """Return (days, raw) for the procedure's retained-for-a-minimum-of figure."""
    m = PROCEDURE_ANCHOR_RE.search(text)
    if m:
        return normalise(int(m.group(1)), m.group(2)), f"{m.group(1)} {m.group(2)}"
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify cross-document retention-period consistency."
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to resolve the register and procedures against "
        "(defaults to the live repo; overridden in regression tests).",
    )
    args = parser.parse_args(argv[1:])
    root = Path(args.root)

    register_path = root / REGISTER
    # read_text_safe catches only UnicodeDecodeError; guard the missing-file case
    # explicitly so a renamed / moved register yields the intended finding rather
    # than an uncaught FileNotFoundError (the linter's whole point is catching a
    # broken cross-reference link).
    register_text = read_text_safe(register_path) if register_path.is_file() else None
    findings: list[str] = []
    if register_text is None:
        print(f"FAIL: cannot read the retention register at {REGISTER}.")
        return 1

    for check in RETENTION_CHECKS:
        label = check["label"]
        category = check["register_category"]
        proc_rel = check["procedure"]
        reg = register_value(register_text, category)
        if reg is None:
            findings.append(
                f"{label}: register row '{category}' not found in {REGISTER} "
                f"(or its period could not be parsed)."
            )
            continue
        proc_path = root / proc_rel
        proc_text = read_text_safe(proc_path) if proc_path.is_file() else None
        if proc_text is None:
            findings.append(f"{label}: cannot read procedure {proc_rel}.")
            continue
        proc = procedure_value(proc_text)
        if proc is None:
            findings.append(
                f"{label}: no 'retained for a minimum of ...' statement found in "
                f"{proc_rel} (the retention citation may have been removed or reworded)."
            )
            continue
        reg_days, reg_raw = reg
        proc_days, proc_raw = proc
        if reg_days != proc_days:
            findings.append(
                f"{label}: MISMATCH. Register '{category}' says {reg_raw}; "
                f"{proc_rel} says {proc_raw}. Reconcile to a single canonical period."
            )

    if findings:
        for f in findings:
            print(f"  - {f}")
        print(
            f"\nFAIL: {len(findings)} retention-consistency issue(s). A procedure's "
            f"evidence-retention period must match the canonical row in {REGISTER}."
        )
        return 1

    print(
        f"OK: {len(RETENTION_CHECKS)} retention pair(s) consistent; each procedure's "
        f"evidence-retention period matches its canonical row in {REGISTER}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
