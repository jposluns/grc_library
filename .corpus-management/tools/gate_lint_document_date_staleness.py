#!/usr/bin/env python3
"""Document Date-staleness check (grc gate): pack-owned engine (source of record).

The pure, environment-free half of the document-date-staleness audit: parse a
file's metadata ``Date`` field, and compute the two day-count comparisons the
audit thresholds against. The audit compares a document's ``Date`` to the file's
most-recent git commit date (it must not lag by more than a tolerated number of
whole days) and to the current UTC date (a "last updated" Date cannot be in the
future).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine
carries the PURE check (``get_metadata_date``, ``future_lead_days``,
``commit_lag_days``); the project wrapper
(``tools/lint-document-date-staleness.py``) supplies the OBSERVER and policy that
are inherently project- and environment-specific: the git commit-date lookup
(``git log --follow``), the concurrency pool, the "today (UTC)" clock, the scan
scope, the baseline/lag/future thresholds, and the reporting. The wrapper keeps
the module-global ``read_text_safe`` its scan-scope regression test patches, reads
each file, and passes the TEXT to ``get_metadata_date`` here, so the engine never
touches the filesystem, git, or the clock.

Note the deliberate ordering the wrapper preserves: the future-date comparison is
applied to every dated file BEFORE the git lookup, so a future-dated file with no
commit history is still flagged; the lag comparison is applied only after the git
commit date is known. The engine exposes the two comparisons as separate pure
functions precisely so the wrapper can keep that split.
"""

from __future__ import annotations

import datetime

try:
    from aiqt_corpus import parse_iso_date, parse_metadata_block
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_document_date_staleness: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


def get_metadata_date(text: str) -> tuple[datetime.date | None, str | None]:
    """Return ``(date, malformed_value)`` for a file's metadata Date field.

    Three outcomes:

      - ``(date, None)``: a well-formed ``**Date:** YYYY-MM-DD`` field.
      - ``(None, None)``: no Date field in the metadata head window;
        the caller skips the file (legitimately date-free).
      - ``(None, raw_value)``: a Date field is PRESENT but its value is
        not exactly an ISO date (trailing annotation, malformed value).
        The caller reports a finding; silently skipping here was the
        fail-open the GR-3 migration closed.
    """
    block = parse_metadata_block(text)
    if "Date" not in block.fields:
        return None, None
    value = block.fields["Date"]
    parsed = parse_iso_date(value)
    if parsed is None:
        return None, value
    return parsed, None


def future_lead_days(metadata_date: datetime.date, today: datetime.date) -> int:
    """Whole days the metadata Date LEADS today (positive = in the future)."""
    return (metadata_date - today).days


def commit_lag_days(commit_date: datetime.date, metadata_date: datetime.date) -> int:
    """Whole days the metadata Date LAGS the file's most-recent commit date."""
    return (commit_date - metadata_date).days
