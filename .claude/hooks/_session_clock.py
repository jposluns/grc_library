"""Shared helper for the timestamp/duration console-rule hooks. NOT a hook itself.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current UTC
timestamp `[YYYY-MM-DD HH:MMZ]` and end with the session duration `(session: Xh Ym)`. This helper
computes those values from the transcript (session start = earliest message timestamp) and validates
a message against the format. Self-contained (no _private / no network); every function fails soft.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

LEAD_RE = re.compile(r"^\s*\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?Z\]")
TAIL_RE = re.compile(r"\(session:[^)]*\)\s*$")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(ts: str):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def session_start(transcript_path) -> "str | None":
    """The earliest message `timestamp` in the transcript (session start), or None on any failure."""
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
                if ts and (earliest is None or ts < earliest):
                    earliest = ts
    except Exception:
        return None
    return earliest


def stamp_and_duration(transcript_path, now: "datetime | None" = None):
    """Return (stamp, duration) strings. duration is None if the session start cannot be determined."""
    now = now or _now()
    stamp = f"[{now.strftime('%Y-%m-%d %H:%M')}Z]"
    start = session_start(transcript_path)
    if start:
        sd = _parse_iso(start)
        if sd is not None:
            m = int((now - sd).total_seconds() // 60)
            if m < 0:
                m = 0
            return stamp, f"(session: {m // 60}h {m % 60}m)"
    return stamp, None


def conforms(text: str) -> bool:
    """True if `text` begins with the required stamp AND ends with a `(session: ...)` duration."""
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
    ("tail not at end", conforms("[2026-08-21 02:31Z] (session: 2h 21m) trailing words") is False),
    ("lead not at start", conforms("prefix [2026-08-21 02:31Z] x (session: 1h 0m)") is False),
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
