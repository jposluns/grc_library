#!/usr/bin/env python3
"""Check per-document review cadence against current date.

Parses each active document's metadata block, computes the next-review-due
date from the Date and Review Frequency fields, and reports any document
that is overdue or past the action threshold.

Usage:
    python3 tools/check-review-cadence.py
    python3 tools/check-review-cadence.py --as-of YYYY-MM-DD
    python3 tools/check-review-cadence.py --action-threshold 90
    python3 tools/check-review-cadence.py --warn-window 30

Exit codes:
    0   no overdue documents beyond the action threshold
    1   one or more documents past the action threshold (CI failure)

The cadence is derived from the document's Review Frequency field. Frequencies
that include phrases such as "and upon material change to X" are treated as
periodic for the schedule; the event trigger is informational.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOMAINS = [
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "sectors",
    "security",
    "supply-chain",
]

EXEMPT_FROM_INDEX = {
    "privacy/annex-regional-privacy-requirements.md",
}

EXEMPT_DIRECTORY_PREFIXES = (
    "dev-security/claude-rules/",
    "tools/",
    "docs/",
)

ROOT_DOCS = (
    "specification-master-project.md",
    "specification-ingestion.md",
)

FIELD_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")

# Frequency phrase -> months. Order matters; longer phrases first.
FREQUENCY_MAP = [
    ("continuous / monthly", 1),
    ("continuous / quarterly", 3),
    ("monthly", 1),
    ("quarterly", 3),
    ("6 to 12 months", 12),
    ("semi-annual", 6),
    ("semi annual", 6),
    ("biennial", 24),
    ("biannual", 24),
    ("annual", 12),
    ("yearly", 12),
    ("12 months", 12),
    ("24 months", 24),
    ("6 months", 6),
    ("3 months", 3),
]


def iter_active_docs() -> list[Path]:
    files: list[Path] = []
    for domain in DOMAINS:
        base = REPO_ROOT / domain
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            rel = f.relative_to(REPO_ROOT).as_posix()
            if f.name == "README.md":
                continue
            if rel in EXEMPT_FROM_INDEX:
                continue
            if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
                continue
            files.append(f)
    for name in ROOT_DOCS:
        p = REPO_ROOT / name
        if p.exists():
            files.append(p)
    return sorted(set(files))


def extract_metadata(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    seen = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("---") and seen:
            break
        if not s and seen:
            break
        m = FIELD_PATTERN.match(line)
        if m:
            name, value = m.groups()
            value = value.strip()
            # Strip CommonMark hard-line-break backslash if present.
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            fields[name.strip()] = value
            seen = True
    return fields


def parse_date(value: str) -> dt.date | None:
    s = value.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_frequency_months(value: str) -> int | None:
    """Return periodic-cadence months, or None for event-driven only."""
    low = value.lower()
    for phrase, months in FREQUENCY_MAP:
        if phrase in low:
            return months
    return None


def add_months(d: dt.date, months: int) -> dt.date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(d.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return dt.date(year, month, day)


def status_for(lag_days: int, warn_window: int, action_threshold: int) -> str:
    if lag_days > action_threshold:
        return "action-threshold"
    if lag_days > 0:
        return "overdue"
    if -lag_days <= warn_window:
        return "due-soon"
    return "current"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check document review cadence.")
    parser.add_argument("--as-of", default=None,
                        help="Override the reference date (YYYY-MM-DD); default is today.")
    parser.add_argument("--action-threshold", type=int, default=90,
                        help="Days past due to escalate (default 90).")
    parser.add_argument("--warn-window", type=int, default=30,
                        help="Days before due to warn (default 30).")
    parser.add_argument("--all", action="store_true",
                        help="Show all documents, not only overdue and due-soon.")
    args = parser.parse_args(argv[1:])

    today = dt.date.today() if not args.as_of else parse_date(args.as_of)
    if today is None:
        print(f"Invalid --as-of value: {args.as_of}", file=sys.stderr)
        return 2

    rows: list[tuple[str, str, dt.date, int | None, dt.date | None, str, int, str]] = []
    skipped: list[tuple[str, str]] = []

    for path in iter_active_docs():
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        meta = extract_metadata(text)
        date_value = meta.get("Date", "")
        freq_value = meta.get("Review Frequency", "")
        owner = meta.get("Owner", "(no owner)")
        last = parse_date(date_value)
        if last is None:
            skipped.append((rel, f"unparseable Date: {date_value!r}"))
            continue
        months = parse_frequency_months(freq_value)
        if months is None:
            # Event-driven only; not date-tracked.
            rows.append((rel, owner, last, None, None, "event-driven", 0, freq_value))
            continue
        due = add_months(last, months)
        lag = (today - due).days
        status = status_for(lag, args.warn_window, args.action_threshold)
        rows.append((rel, owner, last, months, due, status, lag, freq_value))

    overdue = [r for r in rows if r[5] in ("overdue", "action-threshold")]
    due_soon = [r for r in rows if r[5] == "due-soon"]
    action = [r for r in rows if r[5] == "action-threshold"]

    print(f"Reference date: {today.isoformat()}")
    print(f"Total active documents scanned: {len(rows)}")
    print(f"  Current: {sum(1 for r in rows if r[5] == 'current')}")
    print(f"  Due-soon (within {args.warn_window} days): {len(due_soon)}")
    print(f"  Overdue: {len(overdue)}")
    print(f"  Past action threshold ({args.action_threshold} days): {len(action)}")
    print(f"  Event-driven (no periodic cadence): {sum(1 for r in rows if r[5] == 'event-driven')}")
    if skipped:
        print(f"  Skipped (unparseable metadata): {len(skipped)}")

    def fmt_row(r):
        rel, owner, last, months, due, status, lag, freq = r
        due_s = due.isoformat() if due else "n/a"
        months_s = f"{months}m" if months else "event"
        lag_s = f"{lag:+d}d" if due else "n/a"
        return f"  [{status:18}] {rel}  (owner: {owner}; last: {last.isoformat()}; freq: {months_s}; due: {due_s}; lag: {lag_s})"

    if action:
        print("\nPast action threshold:")
        for r in sorted(action, key=lambda x: -x[6]):
            print(fmt_row(r))

    if overdue and not action:
        print("\nOverdue (under action threshold):")
        for r in sorted(overdue, key=lambda x: -x[6]):
            print(fmt_row(r))

    if due_soon and (args.all or not action):
        print("\nDue soon:")
        for r in sorted(due_soon, key=lambda x: x[6]):
            print(fmt_row(r))

    if args.all:
        print("\nAll documents:")
        for r in sorted(rows, key=lambda x: x[0]):
            print(fmt_row(r))

    if skipped:
        print("\nSkipped:")
        for rel, reason in skipped:
            print(f"  {rel}: {reason}")

    if action:
        print(f"\nFAIL: {len(action)} document(s) past the action threshold ({args.action_threshold} days).")
        return 1

    print("\nOK: no documents past the action threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
