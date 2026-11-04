"""Shared helper for the timestamp/duration console-rule hooks. NOT a hook itself.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current
timestamp and end with the session duration `(session: Xh Ym)`. Since 2026-11-04 (maintainer and
Architect) the stamp is Toronto local time with the zone abbreviation, `[YYYY-MM-DD HH:MM EST]` (EDT
in summer), taken from the system zone database (zoneinfo America/Toronto), never a fixed offset.
The earlier UTC form `[YYYY-MM-DD HH:MMZ]` no longer conforms (maintainer decision 2026-11-04).
This helper computes the values from the transcript (session start = earliest PARSED message
timestamp), validates a message's FORMAT (real date, minutes 0-59, the abbreviation the zone gives for
that wall time), and checks the values are CURRENT (within a generous tolerance of now / the computed
duration, to catch reused-stale or drifted values without spurious blocks). Self-contained (no
_private / no network); every function fails soft.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# Anchored SHAPE, with capture groups: the stamp body, then the zone abbreviation.
# Semantic validity (real date, minutes 0-59, abbreviation matching the zone) is checked below.
LEAD_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?::\d{2})?) ([A-Z]{3,4})\]")
TAIL_RE = re.compile(r"\(session: (\d{1,5})h ([0-5]?\d)m\)\s*$")

# The stamp zone, resolved through the system zone database at every use (never a fixed offset).
STAMP_ZONE = "America/Toronto"

# Staleness tolerance: the message's stamp must be within this of `now`, and its duration within
# this of the computed duration. Generous enough that normal compose-to-Stop lag never false-blocks,
# tight enough to catch reused-stale values and gross drift.
TOLERANCE_MIN = 10


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _zone():
    """The STAMP_ZONE tzinfo from the system zone database, or None when it is unavailable."""
    try:
        return ZoneInfo(STAMP_ZONE)
    except Exception:
        return None


def _parse_iso(ts):
    """Parse an ISO-8601 timestamp to an AWARE UTC datetime (naive is assumed UTC), or None."""
    if not isinstance(ts, str):
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_stamp(stamp_body: str, abbr: str):
    """Parse the `YYYY-MM-DD HH:MM(:SS)` body of a message stamp to an aware UTC datetime, or None.
    The body is Toronto wall time and parses only when `abbr` is the abbreviation the zone database
    gives for it (either fold of the repeated autumn hour). A structurally-shaped but impossible date
    (2026-02-31, 25:00) or a wall time the spring change skips fails to parse -> None."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            naive = datetime.strptime(stamp_body, fmt)
        except Exception:
            continue
        zone = _zone()
        if zone is None:
            return None
        for fold in (0, 1):
            local = naive.replace(tzinfo=zone, fold=fold)
            utc = local.astimezone(timezone.utc)
            if local.tzname() == abbr and utc.astimezone(zone).replace(tzinfo=None) == naive:
                return utc
        return None
    return None


def format_stamp(now: datetime):
    """`[YYYY-MM-DD HH:MM ABBR]` for the aware instant `now` in STAMP_ZONE, or None without the zone."""
    zone = _zone()
    if zone is None:
        return None
    local = now.astimezone(zone)
    return f"[{local.strftime('%Y-%m-%d %H:%M')} {local.tzname()}]"


def session_start_dt(transcript_path):
    """Earliest PARSED message timestamp as an aware UTC datetime, or None (parse before comparing)."""
    if not transcript_path:
        return None
    earliest = None
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for ln in f:
                try:
                    ts = json.loads(ln).get("timestamp")
                except Exception:
                    continue
                dt = _parse_iso(ts)
                if dt is not None and (earliest is None or dt < earliest):
                    earliest = dt
    except Exception:
        return None
    return earliest


def stamp_and_duration(transcript_path, now: "datetime | None" = None):
    """Return (stamp, duration). duration is None when the session start cannot be determined, and
    both are None when the zone database lacks STAMP_ZONE (no stamp to require, so callers fail open)."""
    now = now or _now()
    stamp = format_stamp(now)
    if stamp is None:
        return None, None
    sd = session_start_dt(transcript_path)
    if sd is not None:
        m = max(int((now - sd).total_seconds() // 60), 0)
        return stamp, f"(session: {m // 60}h {m % 60}m)"
    return stamp, None


def _msg_stamp_dt(text: str):
    m = LEAD_RE.match(text.strip()) if isinstance(text, str) else None
    return _parse_stamp(m.group(1), m.group(2)) if m else None


def _msg_duration_min(text: str):
    m = TAIL_RE.search(text.strip()) if isinstance(text, str) else None
    if not m:
        return None
    try:
        return int(m.group(1)) * 60 + int(m.group(2))
    except Exception:
        return None


def conforms(text) -> bool:
    """True if `text` BEGINS with a valid current-format stamp (a REAL date) AND ENDS with an
    `Xh Ym` duration (minutes 0-59). Presence + format only; currency is checked separately."""
    if not isinstance(text, str):
        return False
    t = text.strip()
    if not t:
        return True  # empty prose (pure tool-use turn) is not a violation
    return _msg_stamp_dt(t) is not None and TAIL_RE.search(t) is not None


def values_current(text, transcript_path, now: "datetime | None" = None):
    """True if the message's stamp is within TOLERANCE of `now` AND its duration is within TOLERANCE
    of the computed session duration. Fails soft to True (does not block) when a value cannot be
    parsed or the computed duration is unavailable, so this only ever catches a CONFIDENTLY stale
    value, never a message it cannot assess."""
    now = now or _now()
    sd = _msg_stamp_dt(text)
    if sd is not None and abs((now - sd).total_seconds()) > TOLERANCE_MIN * 60:
        return False
    mdur = _msg_duration_min(text)
    start = session_start_dt(transcript_path)
    if mdur is not None and start is not None:
        computed = max(int((now - start).total_seconds() // 60), 0)
        if abs(mdur - computed) > TOLERANCE_MIN:
            return False
    return True


def maintainer_env() -> bool:
    """True only in the maintainer's environment (the grc_library_private sibling is present)."""
    try:
        return (Path(__file__).resolve().parents[2].parent / "grc_library_private").is_dir()
    except Exception:
        return False


def _self_test() -> int:
    now = datetime(2026, 8, 21, 3, 0, 0, tzinfo=timezone.utc)
    winter = datetime(2026, 1, 15, 17, 0, 0, tzinfo=timezone.utc)
    checks = [
        ("conforms full", conforms("[2026-08-20 23:00 EDT] hi (session: 2h 21m)") is True),
        ("conforms seconds", conforms("[2026-08-20 23:00:05 EDT] hi (session: 0h 3m)") is True),
        ("conforms winter", conforms("[2026-01-15 12:00 EST] hi (session: 0h 3m)") is True),
        ("summer EST rejected", conforms("[2026-08-20 23:00 EST] x (session: 1h 0m)") is False),
        ("winter EDT rejected", conforms("[2026-01-15 12:00 EDT] x (session: 1h 0m)") is False),
        ("skipped spring hour rejected", conforms("[2026-03-08 02:30 EST] x (session: 1h 0m)") is False),
        ("legacy UTC rejected", conforms("[2026-08-21 03:00Z] hi (session: 2h 21m)") is False),
        ("no lead", conforms("hi (session: 2h 21m)") is False),
        ("no tail", conforms("[2026-08-20 23:00 EDT] hi") is False),
        ("empty ok", conforms("   ") is True),
        ("bad duration text", conforms("[2026-08-20 23:00 EDT] x (session: bananas)") is False),
        ("minutes 99 rejected", conforms("[2026-08-20 23:00 EDT] x (session: 3h 99m)") is False),
        ("impossible date rejected", conforms("[2026-02-31 03:00 EST] x (session: 1h 0m)") is False),
        ("hour 25 rejected", conforms("[2026-08-20 25:00 EDT] x (session: 1h 0m)") is False),
        ("tail not at end", conforms("[2026-08-20 23:00 EDT] (session: 1h 0m) x") is False),
        # format_stamp: abbreviation and wall time from the zone database
        ("stamp summer", format_stamp(now) == "[2026-08-20 23:00 EDT]"),
        ("stamp winter", format_stamp(winter) == "[2026-01-15 12:00 EST]"),
        # values_current: fresh stamp ok, stale stamp not
        ("fresh stamp current", values_current("[2026-08-20 23:00 EDT] x (session: 0h 0m)", None, now) is True),
        ("stale stamp not current", values_current("[2026-08-20 22:30 EDT] x (session: 0h 0m)", None, now) is False),
        ("unparseable value fails soft", values_current("no stamp", None, now) is True),
        ("huge-hours duration rejected by grammar", conforms("[2026-08-20 23:00 EDT] x (session: 999999h 0m)") is False),
        ("5-digit hours ok", conforms("[2026-08-20 23:00 EDT] x (session: 99999h 0m)") is True),
    ]
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"_session_clock self-test: FAIL {bad}")
        return 1
    print(f"_session_clock self-test: OK ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
