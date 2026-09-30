#!/usr/bin/env python3
"""Citation-currency-cadence audit (gate 72) -- 1.14 Layer A (closing PR #1015).

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
from the register entirely; GR-GAP-1); it assumes a source IS
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

DUE-SOON BAND (advisory, never a WARN). The live-register test asserts no WARN, so
a row that crosses its window turns that test red at the next UTC rollover and
blocks every push until the row is re-checked. To show the lapse first, a dated
row with 0 to DUE_SOON_DAYS days left in its window is printed on a line that
starts with ``DUE-SOON``. Rows are grouped into batches by (last verified, tier,
window) and sorted by the date each batch goes stale. A row is stale or due
soon, never both. ``tools/run_all_audits.sh`` echoes this gate's ``DUE-SOON``,
``WARN`` and ``NOTE`` lines even when it passes, because under the runner the gate
prints ``RUNNER_ECHO_MARKER`` with the runner's token (a per-gate opt-in keyed on
the gate's own output, not on its script path, that data cannot forge), and the
pre-commit hook is verbose, so the band and any stale row are seen at resume and
at commit. The band never changes the exit code.

FUTURE-DATED ROWS (advisory WARN). A ``Last verified (UTC)`` date after today (UTC)
is a data error, such as a typo or a local-time date a day ahead of UTC, not the
freshest possible row: its age is negative, so it would pass every window. Such a
row is listed as a WARN and is never counted as fresh, stale or due soon; the exit
code stays 0. A row verified today is fresh. Like a stale row, a future-dated row
in the live register turns the live-register test red (it asserts no ``WARN:``),
so a local date ahead of UTC blocks a push until UTC reaches that date or the
date is corrected. Every stale, future-dated, untiered-sub-table and
missing-register line starts with ``WARN`` or ``NOTE`` at column 0, so the runner
can echo it.

Exit codes: always 0 (advisory). Findings are printed to stdout.
"""

from __future__ import annotations

import datetime as _dt
import os
import re
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

# Due-soon band, in days: a dated row with 0 to DUE_SOON_DAYS days left in its
# window is listed as DUE-SOON (advisory). 21 is longer than the longest gap
# between commit days on main since 2026-06-01 (16 days, 2026-06-03 to
# 2026-06-19), with slack for a stretch without egress, so at least one session
# sees the band before a row goes stale. To change the band, edit the integer here.
DUE_SOON_DAYS = 21

# tools/run_all_audits.sh hides a passing gate's output, but shows this gate's
# WARN and NOTE lines when the output has this exact line followed by a space and
# the token run_gate passed in RUNNER_ECHO_TOKEN_ENV (run_gate holds the same
# string). The gate declares it in its own output, so a rename, move or other
# invocation path of this script cannot switch the echo off. The token is random
# per gate run, so no data a gate prints can forge the line, as a record ID that
# holds the marker text could in gate 93's WARN lines. With the variable unset or
# empty (a direct run, the pre-commit hook, the quality.yml gate step) the line is
# not printed. The line holds no WARN, NOTE or DUE-SOON, so no count or grep of
# those tags sees it.
RUNNER_ECHO_MARKER = (
    "runner-echo: tools/run_all_audits.sh shows this gate's advisory lines on a pass"
)
RUNNER_ECHO_TOKEN_ENV = "GRC_RUNNER_ECHO_TOKEN"

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
    "Cybersecurity and AI security guidance": "dataset",  # living guidance with frequent editions
    "Cybersecurity adversary frameworks": "framework",
    "OWASP": "framework",
    "Customs and trade": "framework",
    "Software supply-chain frameworks": "framework",
    "Sector-specific (energy, telecom, finance)": "framework",
    "International treaties and conventions": "legislation",
    "OECD and global": "framework",
    "ICAO and IMO": "framework",
    "AI safety evaluation programmes": "dataset",
    "AI security tooling references": "dataset",
}

# A last_checked cell that is not a real date: skipped (not stale, not checkable).
_NON_DATE_TOKENS = {"", "-", "\u2014", "needs-reconfirm", "n/a", "na"}
_DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _print_runner_echo_marker() -> None:
    token = os.environ.get(RUNNER_ECHO_TOKEN_ENV, "")
    if token:
        print(RUNNER_ECHO_MARKER + " " + token)


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
            f"NOTE: citation-currency-cadence: register not found at {CANONICAL_REGISTER}; "
            "nothing to check.",
        )
        _print_runner_echo_marker()
        return 0

    text = CANONICAL_REGISTER.read_text(encoding="utf-8")
    today = _today_utc()

    checked = 0
    skipped = 0
    stale: list[str] = []
    # Rows whose last-verified date is after today: a data error, never fresh.
    future: list[str] = []
    # (stale-from date, tier label, window, last verified) -> source ids.
    due_soon: dict[tuple[_dt.date, str, int, _dt.date], list[str]] = {}
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
        if age < 0:
            future.append(
                f"WARN  [{heading}] {source_id}: last verified {last.isoformat()} "
                f"is {-age} day(s) after today."
            )
        elif age > window:
            stale.append(
                f"WARN  [{heading}] {source_id}: last verified {last.isoformat()} "
                f"({age} days ago) exceeds the {window}-day "
                f"{tier or 'default'} window."
            )
        elif window - age <= DUE_SOON_DAYS:
            stale_from = last + _dt.timedelta(days=window + 1)
            key = (stale_from, tier or "default", window, last)
            due_soon.setdefault(key, []).append(source_id)

    print(
        f"citation-currency-cadence (gate 72, advisory): checked {checked} row(s), "
        f"skipped {skipped} without a parseable date, as of {today.isoformat()} UTC."
    )
    _print_runner_echo_marker()
    if unmapped_headings:
        print(
            "NOTE: sub-table(s) with no explicit tier, using the "
            f"{DEFAULT_WINDOW_DAYS}-day default: "
            + ", ".join(sorted(unmapped_headings))
        )
    if stale:
        print(f"WARN: {len(stale)} source(s) past their re-check window (advisory):")
        for line in stale:
            print(line)
        print(
            "WARN  Re-check each source's Upstream check location, update its "
            "'Last verified (UTC)' (and version columns if upstream moved) under QA. "
            "This gate is advisory (exit 0); it never blocks a merge."
        )
    if future:
        print(
            f"WARN: {len(future)} source(s) dated after today ({today.isoformat()} UTC), "
            "a data error, not a fresh row (advisory):"
        )
        for line in future:
            print(line)
        print(
            "WARN  Correct each 'Last verified (UTC)' to the UTC date of its last "
            "upstream re-check under QA. This gate is advisory (exit 0)."
        )
    if not stale and not future:
        print("  all dated sources are within their re-check windows.")
    if due_soon:
        rows = sum(len(ids) for ids in due_soon.values())
        print(
            f"DUE-SOON: {rows} source(s) in {len(due_soon)} batch(es) have "
            f"{DUE_SOON_DAYS} or fewer days left in their re-check window (advisory):"
        )
        for (stale_from, label, window, last), ids in sorted(due_soon.items()):
            print(
                f"DUE-SOON  verified {last.isoformat()} [{label}, {window}-day]: "
                f"{len(ids)} row(s), stale from {stale_from.isoformat()} "
                f"(in {(stale_from - today).days} day(s)): " + ", ".join(ids)
            )
        print(
            "DUE-SOON  Re-check these batches in one upstream sweep before the first "
            "stale-from date, and update each 'Last verified (UTC)' under QA. "
            "Advisory (exit 0)."
        )
    return 0


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    import sys
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    raise SystemExit(main())
