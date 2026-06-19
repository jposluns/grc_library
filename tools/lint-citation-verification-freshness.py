#!/usr/bin/env python3
"""Flag citation-register entries whose latest verification is past the cadence.

Per the Citation Verification Specification §12.1, entries in the
Canonical Citations Register are re-verified every 12 months. This
linter parses the Citation Verifications Register, computes per-entry
due dates using calendar-month arithmetic (matching the helper in
``tools/lint-tooling-provenance-freshness.py``), and flags any entry
whose latest verification log row is past the 12-month cadence.

Currently the verifications register is empty (verification batches are
pending per Phase Q track). The linter ships as a scaffold and passes
vacuously while the register is empty. When Q-batches begin populating
verifications, the linter will start enforcing the cadence.

Usage:
    python3 tools/lint-citation-verification-freshness.py
    python3 tools/lint-citation-verification-freshness.py --today YYYY-MM-DD

The ``--today`` flag overrides the current date for deterministic
testing (parsed as ISO 8601).

Exit codes:
    0   no entries past the cadence (or the register is empty)
    1   one or more entries past the 12-month cadence
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFICATIONS = REPO_ROOT / "governance" / "register-citation-verifications.md"
CADENCE_MONTHS = 12  # per Citation Verification Specification §12.1


def _add_months(d: date, months: int) -> date:
    """Return ``d`` advanced by ``months`` calendar months.

    Handles month-end roll-forward: 31 January + 1 month → 28/29 February.
    Stdlib-only; avoids dateutil dependency. Mirrors the helper in
    ``tools/lint-tooling-provenance-freshness.py`` so the two freshness
    linters use identical calendar-aware arithmetic (Phase 23.65 parity).
    """
    total_month_index = d.month - 1 + months
    new_year = d.year + total_month_index // 12
    new_month = total_month_index % 12 + 1
    if new_month == 12:
        next_month_first = date(new_year + 1, 1, 1)
    else:
        next_month_first = date(new_year, new_month + 1, 1)
    last_day_of_new_month = (next_month_first.toordinal() - 1)
    last_day_of_new_month_date = date.fromordinal(last_day_of_new_month)
    new_day = min(d.day, last_day_of_new_month_date.day)
    return date(new_year, new_month, new_day)


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
    global VERIFICATIONS
    parser = argparse.ArgumentParser(
        description="Flag canonical citations past the 12-month verification cadence."
    )
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Override today's date (for testing). Default: current date.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the verifications register is "
             "read from (used by the gate-36 regression test suite for "
             "synthetic-fixture isolation testing). Default: the actual "
             "repository root derived from this file's location.",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        VERIFICATIONS = args.root.resolve() / "governance" / "register-citation-verifications.md"
    today = args.today
    # Distinguish "register file missing" (environmental failure;
    # exit 2) from "register present but parses zero rows" (the
    # current documented state — Q-track verifications pending;
    # exit 0 with note). The two cases are not equivalent: a missing
    # file indicates a broken repository, whereas an empty register
    # is the expected starting state.
    if not VERIFICATIONS.exists():
        print(
            f"ERROR: Citation Verifications Register not found at {VERIFICATIONS}",
            file=sys.stderr,
        )
        return 2
    entries = parse_register()
    if not entries:
        print("OK: Citation Verifications Register has no entries yet (Phase Q-track pending). Cadence will engage when verifications begin.")
        return 0
    stale: list[tuple[str, date, int]] = []
    for sid, d in entries.items():
        # Calendar-aware cadence: due date is d + CADENCE_MONTHS months,
        # not d + 365 days. Matches lint-tooling-provenance-freshness.py
        # so the two freshness linters apply consistent semantics.
        due = _add_months(d, CADENCE_MONTHS)
        if today > due:
            age = (today - d).days
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
