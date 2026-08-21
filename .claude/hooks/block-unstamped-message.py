#!/usr/bin/env python3
"""PreToolUse hook: block a tool call when the assistant's CURRENT message carries PROSE that lacks
the required leading UTC timestamp / trailing session duration (maintainer standing rule 2026-08-21).

WHY PreToolUse (the gap this closes): the Stop hook `block-unstamped-turn-end.py` gates only the
FINAL message of a turn. INTERMEDIATE narration (prose written before a tool call, mid-turn) escaped
it entirely, and did so repeatedly. Such prose ALWAYS precedes a tool call, so a PreToolUse gate on
the current message's text catches it. Together the two hooks cover every authored PROSE message:
PreToolUse the intermediate ones, Stop the turn-final one.

CURRENT MESSAGE SOURCE: the transcript's last assistant entry. When a PreToolUse fires, that entry is
the in-flight message carrying THIS tool_use; its `text` blocks are the prose, its `tool_use` blocks
are not (only text is checked).

PRESENCE, NOT CURRENCY (deliberate): this hook checks FORMAT/PRESENCE (`conforms`) only, NOT
`values_current`. Intermediate prose is stamped once when authored; a long turn's later tool calls
would otherwise false-block correctly-stamped-but-now-older prose. Stamp CURRENCY stays the Stop
hook's job, on the turn-final stamp.

EMPTY PROSE = ALLOW: a pure tool-use message (no text block) is not a prose message, so it never
blocks. This is also the intended boundary: the rule governs PROSE the maintainer reads, not bare
tool calls.

FAIL-OPEN (the contract): any error, a non-dict payload, a missing/unreadable transcript, OR an
uncomputable duration (no parseable session start, so the correct value cannot be supplied) returns 0
(allow). The hook never wedges the session and never demands a value it cannot itself provide.
MAINTAINER-SCOPED: no-op for adopters (the grc_library_private sibling is absent).

RESIDUE (stated, not hidden):
  * A PreToolUse fires AFTER the assistant message is already rendered to the maintainer, so this
    FORCES a stamped re-emit rather than PREVENTING the unstamped render. It is corrective, like the
    Stop hook, because a hook cannot rewrite assistant text.
  * It cannot see a turn that is pure prose with NO following tool call; that is exactly the Stop
    hook's domain, so the pair is complementary with no overlap gap.
  * Presence-only means a stamped-but-stale intermediate stamp passes here; the Stop hook's currency
    check catches a stale FINAL stamp, which is the one the maintainer relies on for "how long".

Self-test: python3 .claude/hooks/block-unstamped-message.py --self-test
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _session_clock import stamp_and_duration, conforms, maintainer_env
except Exception:  # fail-open shims if the shared helper is unavailable
    def stamp_and_duration(tp, now=None):
        return None, None

    def conforms(t):
        return True

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


def _current_assistant_text(tp) -> str:
    """Text of the transcript's last assistant entry (the in-flight message carrying this tool_use)."""
    try:
        lines = open(tp, encoding="utf-8").readlines()
    except Exception:
        return ""
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if not isinstance(obj, dict) or obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            return ""
        return _text_from_content(msg.get("content", []))
    return ""


def main() -> int:
    if "--self-test" in sys.argv:
        checks = [
            ("stamped allows", conforms("[2026-08-21 02:31Z] x (session: 1h 0m)") is True),
            ("unstamped blocks", conforms("no stamp") is False),
            ("empty prose allows", conforms("   ") is True),
            ("no-tail blocks", conforms("[2026-08-21 02:31Z] x") is False),
            ("no-lead blocks", conforms("x (session: 1h 0m)") is False),
        ]
        bad = [n for n, ok in checks if not ok]
        print("block-unstamped-message self-test: " + ("OK" if not bad else f"FAIL {bad}"))
        return 0 if not bad else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0
    if not maintainer_env():
        return 0
    tp = payload.get("transcript_path")
    if not tp:
        return 0
    text = _current_assistant_text(tp)
    if conforms(text):  # empty prose -> True (allow); well-formed stamp -> allow
        return 0
    stamp, dur = stamp_and_duration(tp)
    if dur is None:
        return 0  # cannot compute the correct value -> fail open, never block demanding the unknowable
    print(
        "MESSAGE UNSTAMPED (maintainer standing rule 2026-08-21): the prose in your current message "
        f"must BEGIN with `{stamp}` and END with `{dur}`. Re-send the message with both, then retry "
        "this tool call. (This gates INTERMEDIATE narration; the Stop hook gates the final message.)",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
