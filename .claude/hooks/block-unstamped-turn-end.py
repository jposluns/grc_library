#!/usr/bin/env python3
"""Stop hook: block turn-end if the assistant's FINAL authored message lacks the required leading
UTC timestamp or trailing session duration (maintainer standing rule 2026-08-21). Supplies the
correct current values in the block reason so the re-emit is trivially correct.

FINAL MESSAGE SOURCE: the Stop payload's `last_assistant_message` (a string, or an object with
`content`) is preferred over the transcript, because the transcript can lag; the transcript's last
assistant entry (content as a list of blocks OR a plain string) is the fallback.

LOOP-SAFE: on `stop_hook_active` returns 0, so it blocks AT MOST ONCE per turn-end sequence.
FAIL-OPEN: any error, a non-dict payload, a missing/unreadable transcript, empty prose, OR an
UNCOMPUTABLE duration (no parseable session start) returns 0 (allow) - it never blocks demanding a
value it cannot supply, and never wedges the session.
MAINTAINER-SCOPED: no-op for adopters (no grc_library_private).

RESIDUE: hooks cannot rewrite assistant text, so this FORCES a correction rather than performing it,
and gates only the FINAL message of a turn (intermediate narration relies on the re-prime +
discipline).
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


def _text_from_content(parts) -> str:
    if isinstance(parts, str):
        return parts.strip()
    if isinstance(parts, list):
        return " ".join(
            p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"
        ).strip()
    return ""


def _last_assistant_text(tp) -> str:
    try:
        lines = open(tp, encoding="utf-8").readlines()
    except Exception:
        return ""
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            return ""
        return _text_from_content(msg.get("content", []))
    return ""


def final_message(payload) -> str:
    """The final assistant message text. If the payload PROVIDES `last_assistant_message`, use it
    AUTHORITATIVELY (even when empty -> ""), never falling through to the lagging transcript; only
    when the key is ABSENT do we read the transcript (codex ERR1 + gemini WARN)."""
    if "last_assistant_message" in payload:
        lam = payload.get("last_assistant_message")
        if isinstance(lam, str):
            return lam.strip()
        if isinstance(lam, dict):
            return _text_from_content(lam.get("content", []))
        return ""  # present but null/other -> treat as empty, do NOT fall back
    return _last_assistant_text(payload.get("transcript_path"))


def main() -> int:
    if "--self-test" in sys.argv:
        from _session_clock import _self_test as clock_test
        ok = conforms("[2026-08-21 02:31Z] x (session: 1h 0m)") and not conforms("no stamp")
        rc = clock_test()
        print(f"block-unstamped-turn-end self-test: {'OK' if ok and rc == 0 else 'FAIL'}")
        return 0 if (ok and rc == 0) else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0  # a non-dict JSON root (null / list): fail OPEN, do not crash
    if payload.get("stop_hook_active"):
        return 0  # continuation under way: block at most once (loop-safe)
    try:
        if not maintainer_env():
            return 0
        text = final_message(payload)
        if not text:
            return 0  # no prose to stamp (pure tool-use turn)
        if conforms(text):
            return 0
        stamp, dur = stamp_and_duration(payload.get("transcript_path"))
        if dur is None:
            return 0  # cannot compute the duration -> cannot enforce it -> fail OPEN
    except Exception:
        return 0
    print(
        "TURN-END BLOCKED (maintainer standing rule 2026-08-21): your final message must BEGIN with "
        f"the current UTC timestamp and END with the session duration. Re-send it starting with "
        f"`{stamp}` and ending with `{dur}`.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
