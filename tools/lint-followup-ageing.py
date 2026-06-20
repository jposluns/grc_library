#!/usr/bin/env python3
"""Follow-up ageing audit.

Implements Rule 3 of the maintenance-tag dating discipline added to
``governance/register-sweep-history.md`` in PR #90 ("Dating discipline
for deferred findings"). The discipline:

- Each deferred finding carries ``surfaced: YYYY-MM-DD``.
- Optional ``re-triage-by: YYYY-MM-DD`` (default ``surfaced + 30 days``).
- Optional ``re-triaged: YYYY-MM-DD`` trailer recording maintainer review.

The audit fails when ``today() > re-triage-by`` and no
``re-triaged: YYYY-MM-DD`` line with a date at or after ``re-triage-by``
is found in the same block. Resolution: re-triage (add the trailer),
close the follow-up (remove the block), or extend ``re-triage-by``
with a one-line rationale.

Scope: scans ``governance/register-sweep-history.md`` by default.
Other registers adopting the convention should be added to
``TARGET_FILES`` or supplied via ``--target``.

Exit codes:
    0 - All deferred-finding blocks are within their re-triage-by
        deadline or have a fresh re-triaged trailer.
    1 - At least one block is past its deadline with no fresh trailer.
    2 - Invalid date format in a tracked field.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe


TARGET_FILES: list[str] = [
    "governance/register-sweep-history.md",
]

DEFAULT_GRACE_DAYS = 30

SURFACED_RE = re.compile(r"\bsurfaced:\s*(\d{4}-\d{2}-\d{2})\b", re.IGNORECASE)
RETRIAGE_BY_RE = re.compile(
    r"\bre-triage-by:\s*(\d{4}-\d{2}-\d{2})\b", re.IGNORECASE
)
RETRIAGED_RE = re.compile(r"\bre-triaged:\s*(\d{4}-\d{2}-\d{2})\b", re.IGNORECASE)


def parse_iso_date(s: str) -> datetime.date | None:
    """Parse ISO 8601 YYYY-MM-DD; return None on invalid format."""
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def find_blocks(text: str) -> list[tuple[int, str]]:
    """Find blocks containing a ``surfaced:`` field.

    A block is heuristically defined as the surrounding lines from
    the preceding blank line (or start of file) to the next blank
    line (or end of file). This captures a single bullet-block,
    paragraph, or list-item that holds a deferred-finding entry.

    Returns a list of ``(start_line_1_indexed, block_text)`` tuples.
    Each block contains exactly one ``surfaced:`` field; blocks
    overlap only if pathological input has multiple ``surfaced:``
    fields with no blank-line separator (then both are included in
    each block, and the caller checks each independently).
    """
    lines = text.splitlines()
    blocks: list[tuple[int, str]] = []
    i = 0
    n = len(lines)
    while i < n:
        if SURFACED_RE.search(lines[i]):
            # Walk backwards to the previous blank line (or start of file).
            start = i
            while start > 0 and lines[start - 1].strip() != "":
                start -= 1
            # Walk forwards to the next blank line (or end of file).
            end = i
            while end < n - 1 and lines[end + 1].strip() != "":
                end += 1
            block_text = "\n".join(lines[start:end + 1])
            blocks.append((start + 1, block_text))
            i = end + 1
        else:
            i += 1
    return blocks


def check_block(
    block_text: str, today: datetime.date
) -> tuple[bool, str | None]:
    """Check a single block for an expired re-triage-by deadline.

    Returns ``(invalid_date_format, error_message_or_none)``. When
    ``invalid_date_format`` is True, the caller should exit with
    code 2 rather than 1. When the message is None, the block is OK.
    """
    m_surfaced = SURFACED_RE.search(block_text)
    if not m_surfaced:
        return False, None
    surfaced = parse_iso_date(m_surfaced.group(1))
    if surfaced is None:
        return True, (
            f"invalid surfaced date: {m_surfaced.group(1)!r} "
            "(expected YYYY-MM-DD)"
        )

    m_retriage = RETRIAGE_BY_RE.search(block_text)
    if m_retriage:
        retriage_by = parse_iso_date(m_retriage.group(1))
        if retriage_by is None:
            return True, (
                f"invalid re-triage-by date: {m_retriage.group(1)!r} "
                "(expected YYYY-MM-DD)"
            )
    else:
        retriage_by = surfaced + datetime.timedelta(days=DEFAULT_GRACE_DAYS)

    if today <= retriage_by:
        return False, None

    # Past deadline; look for a fresh re-triaged trailer.
    fresh: datetime.date | None = None
    for m in RETRIAGED_RE.finditer(block_text):
        d = parse_iso_date(m.group(1))
        if d is None:
            return True, (
                f"invalid re-triaged date: {m.group(1)!r} "
                "(expected YYYY-MM-DD)"
            )
        if fresh is None or d > fresh:
            fresh = d
    if fresh is not None and fresh >= retriage_by:
        return False, None

    days_overdue = (today - retriage_by).days
    return False, (
        f"deferred finding (surfaced {surfaced.isoformat()}) is "
        f"{days_overdue} day(s) past its re-triage-by deadline "
        f"({retriage_by.isoformat()}) with no fresh `re-triaged:` "
        "trailer. Re-triage the finding (add a line "
        "`re-triaged: YYYY-MM-DD`), close it (remove the entry), or "
        "extend `re-triage-by` with a one-line rationale."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit deferred-finding entries for expired re-triage-by deadlines."
    )
    parser.add_argument(
        "--target",
        action="append",
        default=None,
        help=(
            "File path (relative to repo root) to scan; may be passed "
            "multiple times. Defaults to TARGET_FILES."
        ),
    )
    parser.add_argument(
        "--today",
        default=None,
        help=(
            "ISO 8601 date to treat as 'today' (for testing). "
            "Defaults to the actual current date."
        ),
    )
    parser.add_argument(
        "--root",
        default=None,
        help=(
            "Repository root override (for testing). Defaults to the "
            "lint_common REPO_ROOT."
        ),
    )
    args = parser.parse_args()

    if args.today is not None:
        today = parse_iso_date(args.today)
        if today is None:
            print(
                f"ERROR: --today value {args.today!r} is not a valid "
                "YYYY-MM-DD date.",
                file=sys.stderr,
            )
            return 2
    else:
        today = datetime.date.today()

    root = Path(args.root).resolve() if args.root else REPO_ROOT
    targets = args.target if args.target else TARGET_FILES

    expired: list[str] = []
    invalid: list[str] = []
    for rel in targets:
        path = root / rel
        if not path.is_file():
            continue
        text = read_text_safe(path)
        if text is None:
            continue
        for start_line, block in find_blocks(text):
            bad_format, msg = check_block(block, today)
            if bad_format:
                invalid.append(f"{rel}:L{start_line}: {msg}")
            elif msg is not None:
                expired.append(f"{rel}:L{start_line}: {msg}")

    if invalid:
        for line in invalid:
            print(f"INVALID: {line}", file=sys.stderr)
        return 2
    if expired:
        for line in expired:
            print(f"FAIL: {line}", file=sys.stderr)
        return 1
    print(
        f"OK: no expired follow-up findings "
        f"(today {today.isoformat()}, {len(targets)} target(s) scanned)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
