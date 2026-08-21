#!/usr/bin/env python3
"""PreToolUse hook: block a tool call when the assistant's CURRENT message carries PROSE that lacks
the required leading UTC timestamp / trailing session duration (maintainer standing rule 2026-08-21).

WHY PreToolUse (the gap this closes): the Stop hook `block-unstamped-turn-end.py` gates only the
FINAL message of a turn. INTERMEDIATE narration (prose written before a tool call, mid-turn) escaped
it. Such prose ALWAYS precedes a tool call, so a PreToolUse gate on the current message's text
catches it. Together the two hooks cover every authored PROSE message: PreToolUse the intermediate
ones, Stop the turn-final one.

RACE-FREE CORRELATION via tool_use_id (the load-bearing detail). Claude Code writes ONE transcript
entry per content BLOCK: a message's thinking / text / tool_use become SEPARATE `type:"assistant"`
entries that SHARE one `message.id`, one block each (verified against a real session JSONL). The
transcript LAGS: when a PreToolUse fires for message N's tool call, N's own entries may not be
flushed yet, so the last transcript entry can still be message N-1. Reading "the last message"
therefore mis-reads N-1 (and, since N is often the CORRECTION of N-1's omission, spuriously blocks
the fix). The fix: the PreToolUse payload carries `tool_use_id`; find the transcript tool_use entry
with that id, and assess ITS message. If that entry is present, the same message's text block (written
BEFORE the tool_use) is present too, so the read is race-free. If it is ABSENT (the call has not been
flushed yet), ALLOW (fail-open) - the message is assessed on a later call, or by the Stop hook.

PRESENCE, NOT CURRENCY (deliberate): checks FORMAT/PRESENCE (`conforms`) only, NOT `values_current`.
Intermediate prose is stamped once when authored; a long turn's later tool calls would otherwise
false-block correctly-stamped-but-now-older prose. Stamp CURRENCY stays the Stop hook's job.

EMPTY PROSE = ALLOW: a message with no text block (a pure tool-use message, e.g. thinking + tool_use)
is not a prose message, so it never blocks.

FAIL-OPEN (the contract): the whole body runs under a broad guard; ANY error, a non-dict payload, a
missing/unreadable transcript, an ABSENT tool_use_id or an unmatched one (lag), OR an uncomputable
duration returns 0 (allow). The hook never wedges the session and never demands a value it cannot
supply. MAINTAINER-SCOPED: no-op for adopters (the grc_library_private sibling is absent).

RESIDUE (stated, not hidden):
  * A PreToolUse fires AFTER the assistant message is rendered to the maintainer, so this FORCES a
    stamped re-emit rather than PREVENTING the unstamped render (corrective, like the Stop hook).
  * It cannot see a turn that is pure prose with NO following tool call; that is the Stop hook's
    domain, so the pair is complementary with no gap.
  * Presence-only means a stamped-but-stale intermediate stamp passes; the Stop hook's currency
    check catches a stale FINAL stamp, which is the one the maintainer relies on for "how long".
  * Bounded 64KB TAIL read: the matched tool_use and its message's text are always at the file end,
    so a tail suffices and avoids slurping a transcript that grows unbounded across a long session.

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


def _owning_message_text(tp, tool_use_id):
    """PROSE of the message that OWNS `tool_use_id`, or None to signal ALLOW. None means: no id, an
    unreadable transcript, or the tool_use entry is not yet in the transcript (lag) -> cannot assess
    -> fail open. Race-free: a present tool_use entry implies its same-message text block is present.
    Reads a bounded 64KB tail (the current call and its text are at the file end)."""
    if not tool_use_id:
        return None
    try:
        with open(tp, "rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            fh.seek(max(0, size - 65536))
            data = fh.read().decode("utf-8", "ignore")
    except Exception:
        return None
    text_by_mid = {}   # message_id -> [text blocks]
    owner_mid = None   # message_id that carries tool_use_id
    for ln in data.splitlines():
        s = ln.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except Exception:
            continue
        if not isinstance(obj, dict) or obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            continue
        mid = msg.get("id")
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text":
                text_by_mid.setdefault(mid, []).append(b.get("text", ""))
            elif bt == "tool_use" and b.get("id") == tool_use_id:
                owner_mid = mid
    if owner_mid is None:
        return None  # current tool call not in transcript yet -> allow (fail open on lag)
    return " ".join(text_by_mid.get(owner_mid, [])).strip()


def _decide(payload) -> int:
    """Pure decision: 0 allow, 2 block."""
    if not isinstance(payload, dict):
        return 0
    if not maintainer_env():
        return 0
    tp = payload.get("transcript_path")
    if not tp:
        return 0
    text = _owning_message_text(tp, payload.get("tool_use_id"))
    if text is None:          # lag / no id -> cannot assess -> allow
        return 0
    if conforms(text):        # empty prose -> True (allow); well-formed stamp -> allow
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


def _self_test() -> int:
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


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    try:
        return _decide(json.load(sys.stdin))
    except Exception:
        return 0  # FAIL-OPEN: any error whatsoever -> allow


if __name__ == "__main__":
    sys.exit(main())
