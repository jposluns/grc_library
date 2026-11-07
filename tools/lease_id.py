"""Shared lease-id grammar for the Active-session value (3b793).

Decision D-0502-LEASE-ID-GRAMMAR (one shared grammar). Standard library only,
pure functions: no I/O, no repository imports, and parse() never raises,
including for a str subclass whose methods raise (it calls none of them).
tools/session_facts.py loads this file from its reviewed source bytes and
tools/lint-session-state.py (gate 63) imports ID_RE as its Active-session rule.

Two layers, each matched in full with ASCII-only classes:

- ID: 1 to 128 printable ASCII characters (0x21 to 0x7E), gate 63's rule.
  ``none`` in any letter case is NONE: the lease is inactive, with no start.
- STAMPED, a subset of ID: LABEL "-" STAMP, where LABEL is one or more runs
  of [A-Za-z0-9] joined by single hyphens, at most 32 characters including
  the hyphens, and STAMP is one of
    YYYYMMDDTHHMMSSZ      compact, seconds (precision 1 s)
    YYYYMMDDTHHMMZ        compact, minutes (seconds read as 0, precision 60 s)
    YYYY-MM-DDTHH:MM:SSZ  extended, seconds (precision 1 s)
  The three stamp forms differ in length (16, 14 and 20), so a value splits
  only one way, and the stamp must be a real calendar time in UTC.

parse() returns a LeaseId whose kind is one of:
  NONE     the value is ``none`` in any case; no start.
  STAMPED  a valid ID in the STAMPED form; start and precision are set.
  ID       a valid ID with no usable stamp; the start is UNKNOWN.
  INVALID  not a string, or not 1 to 128 printable ASCII characters.

Not stamped (kind ID, start UNKNOWN): extended minutes
(``orch-2026-10-04T13:36Z``), impossible dates or times, a label longer than
32 characters, an empty label or label segment, any other label character
(such as ``_``), trailing text, a missing ``Z`` and a lowercase ``z``.
A reader never takes a start from another field, the transcript or log rows.
"""
import re
from datetime import datetime, timezone
from typing import NamedTuple

ID_RE = re.compile(r"[!-~]{1,128}", re.ASCII)
LABEL_MAX = 32
STAMPED_RE = re.compile(
    r"([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)-"
    r"(\d{8}T\d{6}Z|\d{8}T\d{4}Z|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)",
    re.ASCII,
)
# Stamp length -> (form name, strptime format, precision in seconds).
FORMS = {
    16: ("compact-seconds", "%Y%m%dT%H%M%SZ", 1),
    14: ("compact-minutes", "%Y%m%dT%H%MZ", 60),
    20: ("extended-seconds", "%Y-%m-%dT%H:%M:%SZ", 1),
}
NONE, STAMPED, ID, INVALID = "NONE", "STAMPED", "ID", "INVALID"


class LeaseId(NamedTuple):
    """kind is NONE, STAMPED, ID or INVALID; start, precision and form are set
    only for STAMPED (start is an aware UTC datetime, precision 1 or 60)."""

    kind: str
    start: datetime | None = None
    precision: int | None = None
    form: str | None = None


def parse(value) -> LeaseId:
    """Classify an Active-session value; never raises.

    No method of value is called, so a str subclass that overrides lower() or
    an object whose __class__ raises cannot make parse() raise: type(value)
    replaces isinstance(), and str.lower() replaces value.lower().
    """
    if not issubclass(type(value), str) or not ID_RE.fullmatch(value):
        return LeaseId(INVALID)
    if str.lower(value) == "none":
        return LeaseId(NONE)
    match = STAMPED_RE.fullmatch(value)
    if match is None or len(match[1]) > LABEL_MAX:
        return LeaseId(ID)
    form, fmt, precision = FORMS[len(match[2])]
    try:
        start = datetime.strptime(match[2], fmt).replace(tzinfo=timezone.utc)
    except ValueError:
        return LeaseId(ID)
    return LeaseId(STAMPED, start, precision, form)
