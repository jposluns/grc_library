#!/usr/bin/env python3
"""Flag citation-register entries whose latest verification is past the cadence.

Per the Citation Verification Specification §12.1, entries in the
Canonical Citations Register are re-verified every 12 months. This
linter parses the Citation Verifications Register, computes per-entry
age, and flags any entry whose latest verification log row is older
than 365 days.

Currently the verifications register is empty (verification batches are
pending per Phase Q track). The linter ships as a scaffold and passes
vacuously while the register is empty. When Q-batches begin populating
verifications, the linter will start enforcing the cadence.

Usage:
    python3 tools/lint-citation-verification-freshness.py

Exit codes:
    0   no entries past the cadence
    1   one or more entries past the 12-month cadence
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFICATIONS = REPO_ROOT / "governance" / "register-citation-verifications.md"
CADENCE_DAYS = 365  # 12 months per Citation Verification Specification §12.1

# Each row begins with `| <Standard ID> | <Verified Field> | ... | <Date checked> | ...`
ROW_RE = re.compile(
    r"^\|\s*(?P<sid>[^|]+?)\s*\|.*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|",
    re.MULTILINE,
)


def parse_register() -> dict[str, date]:
    """Return {standard_id -> latest_verification_date} from the register."""
    if not VERIFICATIONS.exists():
        return {}
    try:
        text = VERIFICATIONS.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {}
    latest: dict[str, date] = {}
    for m in ROW_RE.finditer(text):
        sid = m.group("sid").strip()
        # Skip header / separator rows
        if sid in ("Standard ID", "---", "**Standard ID**"):
            continue
        try:
            d = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
        except ValueError:
            continue
        if sid in latest:
            if d > latest[sid]:
                latest[sid] = d
        else:
            latest[sid] = d
    return latest


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Flag canonical citations past the 12-month verification cadence."
    )
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Override today's date (for testing). Default: current date.",
    )
    args = parser.parse_args(argv[1:])
    today = args.today
    entries = parse_register()
    if not entries:
        print("OK: Citation Verifications Register has no entries yet (Phase Q-track pending). Cadence will engage when verifications begin.")
        return 0
    stale: list[tuple[str, date, int]] = []
    for sid, d in entries.items():
        age = (today - d).days
        if age > CADENCE_DAYS:
            stale.append((sid, d, age))
    if not stale:
        print(f"OK: all {len(entries)} verified citations are within 12 months of latest verification.")
        return 0
    print("=== citations past 12-month cadence ===")
    for sid, d, age in sorted(stale, key=lambda x: -x[2]):
        print(f"  {sid}: last verified {d.isoformat()} ({age} days ago)")
    print(f"\nFAIL: {len(stale)} citation(s) past the 12-month verification cadence.")
    print(
        "Citations past the cadence must be re-verified per Citation "
        "Verification Specification §12.1. Open a new Q-batch worklist "
        "covering the stale entries and route through the standard "
        "human-verifier workflow."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
