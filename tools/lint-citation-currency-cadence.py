#!/usr/bin/env python3
"""Citation-currency-cadence audit (gate 72) -- TODO section 1.14 Layer A.

The canonical-citations register (``governance/register-canonical-citations.md``)
records, per externally-cited source, a ``Last verified (UTC)`` date (the SR-1
field: present but, until this gate, inert). This gate is the EGRESS-FREE Layer A
of the source-currency mechanism: it reads that recorded date and warns when a
source has drifted past its per-trust-tier re-check window. It performs pure
date arithmetic on the recorded field; it makes NO network request (that is the
deferred, egress-required Layer B, a separate scheduled sweep, never this
read-only lint CI).

It is the TIME axis of citation currency, complementing the two existing gates:
``lint-standards-currency.py`` fires on a cited SUPERSEDED version (the version
axis) and ``lint-citations.py`` on a hand-curated known-bad string (the
enumeration axis). A source that is correctly registered and correctly current
but whose last verification has gone stale is invisible to both; this gate adds
that dimension. It does NOT close the require-registration gap (a source absent
from the register entirely; TODO section 3.9 / GR-GAP-1); it assumes a source IS
registered and checks its freshness.

ADVISORY (WARN) MODE, deliberately (not merely a soft rollout). The register's
own "Version-currency cadence (advisory, not a gate)" note explains that a HARD
gate would fail whenever egress is blocked, an environment condition rather than
a defect. That reasoning still binds here: a row goes stale precisely because the
maintainer could not re-check it upstream (often because egress was unavailable),
so failing CI on staleness would penalize an environment condition. This gate
therefore prints its findings and ALWAYS exits 0; it surfaces drift in the CI log
without blocking a merge. Flipping any tier (or the whole gate) to FAIL is a
one-line change once the maintainer confirms the policy and an egress-aware
exemption path.

The per-tier re-check windows below are conservative stricter-safe DEFAULTS
pending maintainer confirmation (recorded in .working/pending-decisions.md). They
are dormant today: every register row was verified within ~18 days of this gate's
addition, so no row is near any window >= 90 days; the windows only begin to
matter as rows age, by which point the maintainer will have confirmed or adjusted
them. Adjusting a window is editing one integer here.

Exit codes: always 0 (advisory). Findings are printed to stdout.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Per-trust-tier re-check windows, in days. CONSERVATIVE STRICTER-SAFE DEFAULTS
# pending maintainer confirmation (see .working/pending-decisions.md). To change a
# policy window, edit the integer here.
TIER_WINDOW_DAYS = {
    "legislation": 180,   # statutes / regulations amend on shorter, less predictable cycles
    "standards": 365,     # ISO / NIST / IEEE: multi-year revision cycles; annual re-check
    "framework": 365,     # frameworks / assurance criteria: annual re-check
    "dataset": 90,        # datasets / tooling / "continuous"-versioned: quarterly
}
# Default window for a register sub-table not explicitly mapped below (a future
# table addition). 365 keeps an unmapped row in scope and passing under any recent
# last_checked, so a new table is covered conservatively rather than silently
# dropped.
DEFAULT_WINDOW_DAYS = 365

# Register sub-table heading (the "## <heading>" line) -> trust tier. Matched by
# exact normalized heading text. An unmapped heading uses DEFAULT_WINDOW_DAYS and
# is reported once so a new table is noticed.
HEADING_TIER = {
    "ISO / IEC standards": "standards",
    "NIST publications": "standards",
    "IEEE standards": "standards",
    "ETSI standards": "standards",
    "EU regulations and directives": "legislation",
    "North-American regulations and frameworks": "legislation",
    "Asia-Pacific regulations and frameworks": "legislation",
    "Other privacy regulations": "legislation",
    "Soft-law supervisory guidance": "legislation",
    "CSA frameworks": "framework",
    "ISACA frameworks": "framework",
    "AICPA assurance criteria": "framework",
    "Cybersecurity adversary frameworks": "framework",
    "OWASP": "framework",
    "Customs and trade": "framework",
    "Sector-specific (energy, telecom, finance)": "framework",
    "OECD and global": "framework",
    "ICAO and IMO": "framework",
    "AI safety evaluation programmes": "dataset",
    "AI security tooling references": "dataset",
}

# A last_checked cell that is not a real date: skipped (not stale, not checkable).
_NON_DATE_TOKENS = {"", "-", "—", "needs-reconfirm", "n/a", "na"}
_DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _parse_last_checked(cell: str):
    """Return a date from a 'Last verified (UTC)' cell, or None if not a date.

    Handles both live forms: 'verified YYYY-MM-DD' and a bare 'YYYY-MM-DD'.
    """
    token = cell.strip()
    low = token.lower()
    if low in _NON_DATE_TOKENS:
        return None
    # 'verified 2026-07-09' -> take the embedded date; bare '2026-06-30' -> same.
    m = _DATE_RE.search(token)
    if not m:
        return None
    try:
        return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _iter_rows(text: str):
    """Yield (heading, source_id, last_checked_cell) for each register data row.

    Table-aware: tracks the current '## <heading>' so each row carries its tier.
    Works for both the 7-column standard schema and the 8-column AI-tooling schema,
    because 'Last verified (UTC)' is the LAST cell in both.
    """
    heading = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            heading = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        # Split the markdown row into trimmed cells (drop the empty edges).
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        first = cells[0].lower()
        # Skip header and separator rows.
        if first in {"standard id", "project"} or set(cells[0]) <= {"-", " ", ":"}:
            continue
        if cells[0].startswith("---"):
            continue
        yield heading, cells[0], cells[-1]


def _window_for(heading):
    tier = HEADING_TIER.get(heading or "")
    if tier is None:
        return DEFAULT_WINDOW_DAYS, None
    return TIER_WINDOW_DAYS[tier], tier


def main() -> int:
    if not CANONICAL_REGISTER.exists():
        # No register: nothing to check. Adopter-portable no-op (the register is
        # an in-repo file, so this is only reached in a malformed checkout).
        print(
            f"citation-currency-cadence: register not found at {CANONICAL_REGISTER}; "
            "nothing to check.",
        )
        return 0

    text = CANONICAL_REGISTER.read_text(encoding="utf-8")
    today = _today_utc()

    checked = 0
    skipped = 0
    stale: list[str] = []
    unmapped_headings: set[str] = set()

    for heading, source_id, last_cell in _iter_rows(text):
        window, tier = _window_for(heading)
        if tier is None and heading:
            unmapped_headings.add(heading)
        last = _parse_last_checked(last_cell)
        if last is None:
            skipped += 1
            continue
        checked += 1
        age = (today - last).days
        if age > window:
            stale.append(
                f"  [{heading}] {source_id}: last verified {last.isoformat()} "
                f"({age} days ago) exceeds the {window}-day "
                f"{tier or 'default'} window."
            )

    print(
        f"citation-currency-cadence (gate 72, advisory): checked {checked} row(s), "
        f"skipped {skipped} without a parseable date, as of {today.isoformat()} UTC."
    )
    if unmapped_headings:
        print(
            "  note: sub-table(s) with no explicit tier, using the "
            f"{DEFAULT_WINDOW_DAYS}-day default: "
            + ", ".join(sorted(unmapped_headings))
        )
    if stale:
        print(f"WARN: {len(stale)} source(s) past their re-check window (advisory):")
        for line in stale:
            print(line)
        print(
            "  Re-check each source's Upstream check location, update its "
            "'Last verified (UTC)' (and version columns if upstream moved) under QA. "
            "This gate is advisory (exit 0); it never blocks a merge."
        )
    else:
        print("  all dated sources are within their re-check windows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
