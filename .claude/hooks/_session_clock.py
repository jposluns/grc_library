"""Shared helper for the timestamp/duration console-rule hooks. NOT a hook itself.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current UTC
timestamp `[YYYY-MM-DD HH:MMZ]` and end with the session duration `(session: Xh Ym)`. This helper
computes those from the transcript (session start = earliest PARSED message timestamp) and validates
a message against the format. Self-contained (no _private / no network); every function fails soft.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Grammar is enforced, not merely shape-detected (codex/claude #1650): a plausible date-time and an
# `Xh Ym` duration, both anchored (stamp at the very start, duration at the very end).
LEAD_RE = re.compile(
    r"^\[\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]) ([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?Z\]"
)
TAIL_RE = re.compile(r"\(session: \d+h \d+m\)\s*$")


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


def session_start_dt(transcript_path):
    """Earliest PARSED message timestamp as an aware UTC datetime, or None. Parses before comparing
    (a lexically-earlier malformed string can no longer poison the real minimum)."""
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
        m = int((now - sd).total_seconds() // 60)
        if m < 0:
            m = 0
        return stamp, f"(session: {m // 60}h {m % 60}m)"
    return stamp, None


def conforms(text) -> bool:
    """True if `text` begins with the required stamp AND ends with an `Xh Ym` session duration."""
    if not isinstance(text, str):
        return False
    t = text.strip()
    if not t:
        return True  # empty prose (pure tool-use turn) is not a violation
    return bool(LEAD_RE.match(t)) and bool(TAIL_RE.search(t))


def maintainer_env() -> bool:
    """True only in the maintainer's environment (the grc_library_private sibling is present).
    The console-format rule is the maintainer's preference, so the hooks no-op for adopters."""
    try:
        return (Path(__file__).resolve().parents[2].parent / "grc_library_private").is_dir()
    except Exception:
        return False


SELF_TEST = [
    ("conforms full", conforms("[2026-08-21 02:31Z] hello there (session: 2h 21m)") is True),
    ("conforms seconds", conforms("[2026-08-21 02:31:05Z] hi (session: 0h 3m)") is True),
    ("no lead", conforms("hello there (session: 2h 21m)") is False),
    ("no tail", conforms("[2026-08-21 02:31Z] hello there") is False),
    ("neither", conforms("just a message") is False),
    ("empty ok", conforms("   ") is True),
    ("tail not at end", conforms("[2026-08-21 02:31Z] (session: 2h 21m) trailing") is False),
    ("lead not at start", conforms("prefix [2026-08-21 02:31Z] x (session: 1h 0m)") is False),
    ("bad duration rejected", conforms("[2026-08-21 02:31Z] x (session: bananas)") is False),
    ("empty duration rejected", conforms("[2026-08-21 02:31Z] x (session:)") is False),
    ("impossible date rejected", conforms("[9999-99-99 99:99Z] x (session: 1h 0m)") is False),
    ("leading whitespace stripped-ok", conforms("   [2026-08-21 02:31Z] x (session: 1h 0m)") is True),
    ("parse naive utc", _parse_iso("2026-08-21T00:00:00") is not None),
    ("parse Z", _parse_iso("2026-08-21T00:00:00Z") is not None),
    ("parse junk None", _parse_iso("not-a-date") is None),
]


def _self_test() -> int:
    bad = [n for n, ok in SELF_TEST if not ok]
    if bad:
        print(f"_session_clock self-test: FAIL {bad}")
        return 1
    print(f"_session_clock self-test: OK ({len(SELF_TEST)} checks)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
