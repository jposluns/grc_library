#!/usr/bin/env python3
"""UserPromptSubmit hook: every turn, inject the current UTC timestamp + session duration + a
reminder of the maintainer standing rule into context, so the assistant always has FRESH values and
is re-primed against convention-erosion.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current UTC
timestamp and end with the session duration. This hook is the anti-forgetting half (supplies the
exact values so the assistant need not guess); block-unstamped-turn-end.py is the enforcing half.

MAINTAINER-SCOPED (no-op for adopters, who lack grc_library_private): the console-format rule is the
maintainer's preference, not portable. FAIL-OPEN on any error: a prompt is never blocked or delayed.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _session_clock import stamp_and_duration, maintainer_env
except Exception:
    def stamp_and_duration(tp, now=None):
        return None, None

    def maintainer_env():
        return False


def main() -> int:
    if "--self-test" in sys.argv:
        from _session_clock import conforms, _self_test as clock_test
        ok = conforms("[2026-08-21 02:31Z] x (session: 1h 0m)") and not conforms("no stamp")
        rc = clock_test()
        print(f"{'inject-session-timestamp'} self-test: {'OK' if ok and rc==0 else 'FAIL'}")
        return 0 if (ok and rc == 0) else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        if not maintainer_env():
            return 0
        stamp, dur = stamp_and_duration(payload.get("transcript_path"))
    except Exception:
        return 0
    if not stamp:
        return 0
    dur_txt = dur if dur else "(session: unavailable)"
    msg = (
        "STANDING RULE (maintainer-directed 2026-08-21): BEGIN every message you author with the "
        "current UTC timestamp and END it with the session duration. Use these values now: "
        f"start with `{stamp}` , end with `{dur_txt}` . Format: `[YYYY-MM-DD HH:MMZ]` ... "
        "`(session: Xh Ym)`. This applies to every message, including short ones."
    )
    try:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
