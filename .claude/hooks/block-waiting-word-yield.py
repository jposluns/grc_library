#!/usr/bin/env python3
"""Stop hook: when the turn ends on a WAITING-word, force a productivity revisit.

Maintainer-directed (Architect self-nudge idea, 2026-08-09), after the orchestrator
repeatedly ended a turn saying it would ``wait`` / ``await`` / be ``re-invoke``d by a
monitor and then simply YIELDED, instead of using the wait for productive parallel
work (reviewing or revising the next seed, prepping the next PR read-only, analysing
the next backlog item, drafting the next order).

The failure this closes: a wait on a background worker or CI is not idle time. There
is almost always independent, read-only, or authoring work the orchestrator can do
while the awaited result is in flight. Ending the turn on a waiting-word is the tell
that the orchestrator is about to sit.

WHAT IT DOES. A Stop hook. It reads the LAST assistant message from the transcript.
If that message ends the turn on a confirmed waiting-word AND a continuation is not
already under way, it BLOCKS the turn-end once (exit 2) with a message that forces a
revisit of what productive work is available.

WHY IT IS SAFE TO ADD.
- Loop-safe: it honours ``stop_hook_active`` and never blocks a continuation, so it
  fires AT MOST ONCE per yield. After the nudge the orchestrator either does
  productive work (and the next stop is a fresh decision) or states plainly that
  nothing is available and takes the escape.
- Escapable: ``touch <GRC_DROP_ROOT>/.allow-waiting-yield`` is honoured once and
  deleted, so a genuine no-productive-work yield is one command away. The block
  message prints it. The escape is reachable by the actor (a Bash tool call), which
  is the point: the guard is a speed bump plus a forcing question, not a wall.
- Fails open: any error (no transcript, unreadable, unexpected shape) returns allow.
  A guard that traps the actor on its own malfunction gets removed.

RESIDUE STATED. The trigger is the WORD, not a verified absence of productive work;
the hook cannot know whether productive work exists. That is deliberate: the word is
the reliable, observable signal that the orchestrator is yielding to a wait, and the
forcing question ("what can you do now?") is exactly the revisit that was missing.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))
ESCAPE_FILE = WORKING_ROOT / ".allow-waiting-yield"

# The confirmed waiting-word set (Architect design 2026-08-09, guardrail-inventory).
# A Stop hook fires only at turn-END, so any of these in the final message is a
# yield-to-wait signal, not mid-turn prose. Matched case-insensitively, as whole
# words / phrases so "await" does not fire inside "awaiting a review" twice, etc.
WAITING_PATTERNS = [
    r"re-?invoke",
    r"awaiting",
    r"\bawait\b",
    r"\bwait\b",          # bare "wait" too: "a genuine wait" slipped past \bwaiting\b
    r"\bwaiting\b",
    r"dispatch-and-await",  # the sneaky dressed-up substitutes the actor actually used
    r"offload-and-await",
    r"\bnot idle\b",      # "this is not idle time" is the rationalization, not productivity
    r"not (just )?sitting",
    r"genuine (dispatch|offload|wait)",
    r"i['’]?ll wait\b",
    r"i will wait\b",
    r"the monitor will\b",
    r"will re-?invoke\b",
    r"i['’]?ll report when\b",
    r"\bon delivery\b",
    r"re-invoke me\b",
]
_RX = re.compile("|".join(WAITING_PATTERNS), re.IGNORECASE)


def last_assistant_text(transcript_path: str) -> str:
    """The concatenated text of the LAST assistant message in the transcript.

    Returns "" on any failure (fail-open upstream treats "" as no trigger)."""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        content = msg.get("content")
        parts = []
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def first_trigger(text: str) -> str | None:
    """The first waiting-word/phrase present in the text, else None."""
    m = _RX.search(text or "")
    return m.group(0) if m else None


def decide(stop_hook_active: bool, escape: bool, text: str) -> str | None:
    """Return a block message, or None to allow. Pure: no IO."""
    if stop_hook_active or escape:
        return None
    trigger = first_trigger(text)
    if trigger is None:
        return None
    return (
        "PRODUCTIVITY NUDGE (turn-end guard): your last message ends the turn on a "
        "waiting-word (" + repr(trigger) + "). A wait on a worker, CI, or monitor is "
        "NOT idle time. Before you yield, REVISIT what productive work you can do NOW, "
        "independent of the awaited result:\n"
        "  - review or revise the NEXT seed / hook / candidate (not just the one in flight),\n"
        "  - prep the next PR read-only (verify a draft against main, pre-identify fixes),\n"
        "  - analyse the next backlog item, or draft the next worker order,\n"
        "  - process a delivered result you have not yet consumed.\n"
        "If, after revisiting, there is GENUINELY nothing productive that does not block "
        "on the awaited result, say so in ONE explicit line, then take the escape:\n"
        "    touch " + str(ESCAPE_FILE) + "\n"
        "The escape is honoured once. Do NOT reword the message to dodge the trigger; "
        "the point is the revisit, not the phrasing."
    )


def _consume_escape() -> bool:
    """True iff the escape sentinel was present and successfully removed (once-only)."""
    try:
        if not ESCAPE_FILE.is_file():
            return False
    except OSError:
        return False
    try:
        ESCAPE_FILE.unlink()
    except OSError:
        return False
    return True


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        return 0  # fail-open on a malformed payload
    try:
        if payload.get("stop_hook_active"):
            return 0
        text = last_assistant_text(payload.get("transcript_path", ""))
        escape = _consume_escape()
        message = decide(bool(payload.get("stop_hook_active")), escape, text)
    except Exception:
        return 0  # fail-open on any unexpected error
    if message is None:
        return 0
    print(message, file=sys.stderr)
    return 2


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_reinvoke_blocks(self):
            self.assertIsNotNone(decide(False, False, "the monitor will re-invoke me on delivery"))

        def test_awaiting_blocks(self):
            self.assertIsNotNone(decide(False, False, "Awaiting the r2 dual-family result."))

        def test_ill_wait_blocks(self):
            self.assertIsNotNone(decide(False, False, "I'll wait for the workers to deliver."))
            self.assertIsNotNone(decide(False, False, "I’ll wait for the workers."))

        def test_waiting_blocks(self):
            self.assertIsNotNone(decide(False, False, "Genuine dispatch-and-await; recording the wait. waiting on CI."))

        def test_on_delivery_blocks(self):
            self.assertIsNotNone(decide(False, False, "I'll reconcile on delivery."))

        def test_sneaky_substitutes_block(self):
            # the dressed-up "not really waiting" rationalizations must also fire
            for phrase in (
                "This is a genuine wait, all prep complete.",
                "A legitimate dispatch-and-await, not idle time.",
                "Genuine offload-and-await; the worker is drafting.",
                "I'm not just sitting; the monitor is armed.",
            ):
                self.assertIsNotNone(decide(False, False, phrase), phrase)

        def test_ordinary_message_allows(self):
            self.assertIsNone(decide(False, False, "Fixed the three findings; all 89 gates green; merging."))
            self.assertIsNone(decide(False, False, "Here is the reconciled result: 2 errors fixed."))

        def test_stop_hook_active_allows(self):
            # a continuation is under way: never block again (loop-safety)
            self.assertIsNone(decide(True, False, "re-invoke me later"))

        def test_escape_allows(self):
            self.assertIsNone(decide(False, True, "re-invoke me later"))

        def test_last_assistant_extraction(self):
            import tempfile
            rows = [
                {"type": "user", "message": {"role": "user", "content": "hi"}},
                {"type": "assistant", "message": {"role": "assistant",
                    "content": [{"type": "text", "text": "first"}]}},
                {"type": "assistant", "message": {"role": "assistant",
                    "content": [{"type": "text", "text": "awaiting the result"}]}},
            ]
            with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
                path = f.name
            try:
                self.assertEqual(last_assistant_text(path), "awaiting the result")
                self.assertIsNotNone(decide(False, False, last_assistant_text(path)))
            finally:
                os.unlink(path)

        def test_missing_transcript_is_empty(self):
            self.assertEqual(last_assistant_text("/nonexistent/x.jsonl"), "")
            self.assertIsNone(decide(False, False, last_assistant_text("/nonexistent/x.jsonl")))

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if result.wasSuccessful():
        print("OK", file=sys.stderr)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
