"""Shared helper for the timestamp/duration console-rule hooks. NOT a hook itself.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current UTC
timestamp `[YYYY-MM-DD HH:MMZ]` and end with the session duration `(session: Xh Ym)`. This helper
computes those from the transcript (session start = earliest PARSED message timestamp), validates a
message's FORMAT (real date, minutes 0-59), and checks the values are CURRENT (within a generous
tolerance of now / the computed duration, to catch reused-stale or drifted values without spurious
blocks). Self-contained (no _private / no network); every function fails soft.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Anchored SHAPE, with capture groups; semantic validity (real date, minutes 0-59) is checked below.
LEAD_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?::\d{2})?)Z\]")
TAIL_RE = re.compile(r"\(session: (\d{1,5})h ([0-5]?\d)m\)\s*$")

# Staleness tolerance: the message's stamp must be within this of `now`, and its duration within
# this of the computed duration. Generous enough that normal compose-to-Stop lag never false-blocks,
# tight enough to catch reused-stale values and gross drift.
TOLERANCE_MIN = 10


def _now() -> datetime:
    return datetime.now(timezone.utc)


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


def _parse_stamp(stamp_body: str):
    """Parse the `YYYY-MM-DD HH:MM(:SS)` body of a message stamp to an aware UTC datetime, or None.
    A structurally-shaped but impossible date (2026-02-31, 25:00) fails to parse -> None."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(stamp_body, fmt).replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


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
    """Return (stamp, duration). duration is None when the session start cannot be determined."""
    now = now or _now()
    stamp = f"[{now.strftime('%Y-%m-%d %H:%M')}Z]"
    sd = session_start_dt(transcript_path)
    if sd is not None:
        m = max(int((now - sd).total_seconds() // 60), 0)
        return stamp, f"(session: {m // 60}h {m % 60}m)"
    return stamp, None


def _msg_stamp_dt(text: str):
    m = LEAD_RE.match(text.strip()) if isinstance(text, str) else None
    return _parse_stamp(m.group(1)) if m else None


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
    from datetime import timedelta
    now = datetime(2026, 8, 21, 3, 0, 0, tzinfo=timezone.utc)
    checks = [
        ("conforms full", conforms("[2026-08-21 03:00Z] hi (session: 2h 21m)") is True),
        ("conforms seconds", conforms("[2026-08-21 03:00:05Z] hi (session: 0h 3m)") is True),
        ("no lead", conforms("hi (session: 2h 21m)") is False),
        ("no tail", conforms("[2026-08-21 03:00Z] hi") is False),
        ("empty ok", conforms("   ") is True),
        ("bad duration text", conforms("[2026-08-21 03:00Z] x (session: bananas)") is False),
        ("minutes 99 rejected", conforms("[2026-08-21 03:00Z] x (session: 3h 99m)") is False),
        ("impossible date rejected", conforms("[2026-02-31 03:00Z] x (session: 1h 0m)") is False),
        ("hour 25 rejected", conforms("[2026-08-21 25:00Z] x (session: 1h 0m)") is False),
        ("tail not at end", conforms("[2026-08-21 03:00Z] (session: 1h 0m) x") is False),
        # values_current: fresh stamp ok, stale stamp not
        ("fresh stamp current", values_current("[2026-08-21 03:00Z] x (session: 0h 0m)", None, now) is True),
        ("stale stamp not current", values_current("[2026-08-21 02:30Z] x (session: 0h 0m)", None, now) is False),
        ("unparseable value fails soft", values_current("no stamp", None, now) is True),
        ("huge-hours duration rejected by grammar", conforms("[2026-08-21 03:00Z] x (session: 999999h 0m)") is False),
        ("5-digit hours ok", conforms("[2026-08-21 03:00Z] x (session: 99999h 0m)") is True),
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
