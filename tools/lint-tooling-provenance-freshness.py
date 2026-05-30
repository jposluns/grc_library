#!/usr/bin/env python3
"""Flag tooling-register entries whose latest provenance is past the cadence.

Per Citation Verification Specification §12.2, entries in the AI Security
Tooling Landscape Register are re-verified at 6-month cadence for active
open-source projects and commercial vendors, 12-month cadence for archived
or unmaintained projects.

This linter parses each entry's Provenance block, extracts the Date assessed
field, and flags entries past the cadence.

Currently all entries are AI-captured-pending-human-verification with
Date assessed 2026-05-30; the linter passes while entries are within
the cadence window.

Usage:
    python3 tools/lint-tooling-provenance-freshness.py

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

ACTIVE_CADENCE_DAYS = 6 * 30  # 6 months
ARCHIVED_CADENCE_DAYS = 12 * 30  # 12 months

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
    parser = argparse.ArgumentParser(
        description="Flag tooling-register entries past the provenance cadence."
    )
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Override today's date for testing.",
    )
    args = parser.parse_args(argv[1:])
    today = args.today
    entries = parse_register()
    if not entries:
        print("OK: AI Security Tooling Landscape Register has no entries with Date assessed; cadence not applicable.")
        return 0
    stale: list[tuple[str, str, date, int, int]] = []
    for sid, name, d, archived in entries:
        cadence = ARCHIVED_CADENCE_DAYS if archived else ACTIVE_CADENCE_DAYS
        age = (today - d).days
        if age > cadence:
            stale.append((sid, name, d, age, cadence))
    if not stale:
        print(f"OK: all {len(entries)} tooling-register entries are within the provenance cadence (active 6 months, archived 12 months).")
        return 0
    print("=== tooling entries past provenance cadence ===")
    for sid, name, d, age, cadence in sorted(stale, key=lambda x: -x[3]):
        print(f"  {sid} {name}: assessed {d.isoformat()} ({age} days ago; cadence {cadence}d)")
    print(f"\nFAIL: {len(stale)} entry(ies) past the provenance cadence.")
    print(
        "Tooling entries past their cadence must be re-verified per Citation "
        "Verification Specification §12.2. Update the entry's Provenance block "
        "with a fresh Date assessed and refreshed integrity anchors."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
