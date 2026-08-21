#!/usr/bin/env python3
"""Stop hook: block turn-end if the assistant's FINAL authored message lacks the required leading
UTC timestamp or trailing session duration (maintainer standing rule 2026-08-21). Supplies the
correct current values in the block reason so the re-emit is trivially correct.

LOOP-SAFE: on `stop_hook_active` it returns 0, so it blocks AT MOST ONCE per turn-end sequence (one
forced correction with the values supplied), never an infinite wedge.
FAIL-OPEN: any error, missing transcript, or empty prose (a pure tool-use turn) returns 0 (allow).
MAINTAINER-SCOPED: no-op for adopters (no grc_library_private), so an adopter is never blocked by the
maintainer's console-format preference.

RESIDUE (stated): this gates only the FINAL message of a turn, not intermediate narration before
tool calls; and because it blocks at most once, a second non-conforming re-emit would pass. The
UserPromptSubmit re-prime + the discipline cover the rest. Hooks cannot rewrite assistant text, so
this forces a correction rather than performing one.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _session_clock import stamp_and_duration, conforms, maintainer_env
except Exception:
    def stamp_and_duration(tp, now=None):
        return None, None

    def conforms(t):
        return True  # fail-open

    def maintainer_env():
        return False


def _last_assistant_text(tp) -> "str | None":
    try:
        lines = open(tp, encoding="utf-8").readlines()
    except Exception:
        return None
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            return None
        parts = msg.get("content", [])
        if not isinstance(parts, list):
            return None
        return " ".join(
            p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"
        ).strip()
    return None


def main() -> int:
    if "--self-test" in sys.argv:
        from _session_clock import conforms, _self_test as clock_test
        ok = conforms("[2026-08-21 02:31Z] x (session: 1h 0m)") and not conforms("no stamp")
        rc = clock_test()
        print(f"{'block-unstamped-turn-end'} self-test: {'OK' if ok and rc==0 else 'FAIL'}")
        return 0 if (ok and rc == 0) else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("stop_hook_active"):
        return 0  # continuation under way: block at most once (loop-safe)
    try:
        if not maintainer_env():
            return 0
        tp = payload.get("transcript_path")
        if not tp:
            return 0
        text = _last_assistant_text(tp)
        if not text:
            return 0  # no prose to stamp (pure tool-use turn)
        if conforms(text):
            return 0
        stamp, dur = stamp_and_duration(tp)
    except Exception:
        return 0
    stamp = stamp or "[<now>Z]"
    dur = dur or "(session: <duration>)"
    print(
        "TURN-END BLOCKED (maintainer standing rule 2026-08-21): your final message must BEGIN with "
        f"the current UTC timestamp and END with the session duration. Re-send it starting with "
        f"`{stamp}` and ending with `{dur}`.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
