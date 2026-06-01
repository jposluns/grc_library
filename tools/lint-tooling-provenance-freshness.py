#!/usr/bin/env python3
"""Flag tooling-register entries whose latest provenance is past the cadence.

Per Citation Verification Specification §12.2, entries in the AI Security
Tooling Landscape Register are re-verified at 6-month cadence for active
open-source projects and commercial vendors, 12-month cadence for archived
or unmaintained projects.

This linter parses each entry's Provenance block, extracts the Date
assessed field, and flags entries past the cadence.

The active-vs-archived classification is derived from each entry's
``**Status notes**`` field: presence of any of ``archived``,
``unmaintained``, or ``deprecated`` (case-insensitive) routes the entry
to the 12-month cadence; otherwise the 6-month cadence applies.

Currently all entries are AI-captured-pending-human-verification with
Date assessed 2026-05-30; the linter passes while entries are within
the cadence window.

Usage:
    python3 tools/lint-tooling-provenance-freshness.py
    python3 tools/lint-tooling-provenance-freshness.py --today YYYY-MM-DD

The ``--today`` flag overrides the current date for deterministic
testing (parsed as ISO 8601).

Exit codes:
    0   no entries past the cadence
    1   one or more entries past the cadence
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTER = REPO_ROOT / "governance" / "register-ai-security-tooling-landscape.md"

ACTIVE_CADENCE_MONTHS = 6   # active OSS / commercial: re-verify every 6 months
ARCHIVED_CADENCE_MONTHS = 12  # archived / unmaintained: re-verify every 12 months


def _add_months(d: date, months: int) -> date:
    """Return ``d`` advanced by ``months`` calendar months.

    Handles month-end roll-forward: 31 January + 1 month → 28/29 February.
    Stdlib-only; avoids dateutil dependency.
    """
    total_month_index = d.month - 1 + months
    new_year = d.year + total_month_index // 12
    new_month = total_month_index % 12 + 1
    # Clamp day to last day of the new month.
    if new_month == 12:
        next_month_first = date(new_year + 1, 1, 1)
    else:
        next_month_first = date(new_year, new_month + 1, 1)
    last_day_of_new_month = (next_month_first.toordinal() - 1)
    last_day_of_new_month_date = date.fromordinal(last_day_of_new_month)
    new_day = min(d.day, last_day_of_new_month_date.day)
    return date(new_year, new_month, new_day)

# Match: #### N.N.N <Project Name>
ENTRY_HEADER_RE = re.compile(r"^####\s+(\d+\.\d+\.\d+)\s+(.+?)\s*$")
DATE_ASSESSED_RE = re.compile(r"^\s*-\s*Date assessed:\s*(\d{4}-\d{2}-\d{2})")
STATUS_NOTES_RE = re.compile(r"^\s*-\s*\*\*Status notes\*\*:\s*(.+)$", re.IGNORECASE)


def parse_register() -> list[tuple[str, str, date, bool]]:
    """Return list of (section_id, name, date_assessed, is_archived)."""
    if not REGISTER.exists():
        return []
    text = REGISTER.read_text(encoding="utf-8")
    entries: list[tuple[str, str, date, bool]] = []
    current_id: str | None = None
    current_name: str | None = None
    current_date: date | None = None
    current_archived = False
    for line in text.splitlines():
        m_header = ENTRY_HEADER_RE.match(line)
        if m_header:
            # Commit previous entry
            if current_id and current_date:
                entries.append((current_id, current_name or "", current_date, current_archived))
            current_id = m_header.group(1)
            current_name = m_header.group(2)
            current_date = None
            current_archived = False
            continue
        m_date = DATE_ASSESSED_RE.match(line)
        if m_date and current_id:
            try:
                current_date = datetime.strptime(m_date.group(1), "%Y-%m-%d").date()
            except ValueError:
                pass
            continue
        # Detect archive markers
        m_status = STATUS_NOTES_RE.match(line)
        if m_status and current_id:
            note = m_status.group(1).lower()
            if "archived" in note or "unmaintained" in note or "deprecated" in note:
                current_archived = True
    # Commit last
    if current_id and current_date:
        entries.append((current_id, current_name or "", current_date, current_archived))
    return entries


def main(argv: list[str]) -> int:
    global REGISTER
    parser = argparse.ArgumentParser(
        description="Flag tooling-register entries past the provenance cadence."
    )
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Override today's date for testing.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the tooling-landscape register "
             "is read from (used by the gate-33 regression test suite "
             "for synthetic-fixture isolation testing). Default: the "
             "actual repository root derived from this file's location.",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REGISTER = args.root.resolve() / "governance" / "register-ai-security-tooling-landscape.md"
    today = args.today
    # Distinguish "register file missing" (environmental failure;
    # exit 2) from "register present but parses zero rows" (parsing
    # bug or accidental wipe; exit 1). The AI Security Tooling
    # Landscape Register has 55+ entries by design; an empty parse
    # would indicate broken parsing or a wipe, not an expected state.
    if not REGISTER.exists():
        print(
            f"ERROR: AI Security Tooling Landscape Register not found at {REGISTER}",
            file=sys.stderr,
        )
        return 2
    entries = parse_register()
    if not entries:
        print(
            "ERROR: AI Security Tooling Landscape Register parsed no entries. "
            "The register exists but no Date-assessed rows were extracted — "
            "likely a parsing bug or an accidental wipe. Linter cannot verify "
            "provenance freshness in this state.",
            file=sys.stderr,
        )
        return 1
    stale: list[tuple[str, str, date, int, int]] = []
    for sid, name, d, archived in entries:
        cadence_months = ARCHIVED_CADENCE_MONTHS if archived else ACTIVE_CADENCE_MONTHS
        # Calendar-aware cadence: due date is d + cadence_months months,
        # not d + cadence_months * 30 days. Avoids the ~3-day early
        # cliff at the 6-month mark on a 30-day-month approximation.
        due = _add_months(d, cadence_months)
        if today > due:
            age = (today - d).days
            stale.append((sid, name, d, age, cadence_months))
    if not stale:
        print(f"OK: all {len(entries)} tooling-register entries are within the provenance cadence (active 6 months, archived 12 months).")
        return 0
    print("=== tooling entries past provenance cadence ===")
    for sid, name, d, age, cadence_months in sorted(stale, key=lambda x: -x[3]):
        print(f"  {sid} {name}: assessed {d.isoformat()} ({age} days ago; cadence {cadence_months} months)")
    print(f"\nFAIL: {len(stale)} entry(ies) past the provenance cadence.")
    print(
        "Tooling entries past their cadence must be re-verified per Citation "
        "Verification Specification §12.2. Update the entry's Provenance block "
        "with a fresh Date assessed and refreshed integrity anchors."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
