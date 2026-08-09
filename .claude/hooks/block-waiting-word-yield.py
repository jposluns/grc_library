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

WHAT IT DOES. A Stop hook. It reads the LAST MAIN-THREAD assistant message from the
transcript (subagent / sidechain rows are skipped: a worker's "Awaiting" is not the
orchestrator yielding). If that message ends the turn on a waiting-word AND a
continuation is not already under way, it BLOCKS the turn-end once (exit 2) with a
message that forces a revisit of what productive work is available.

WHY IT IS SAFE TO ADD.
- Loop-safe: it honours ``stop_hook_active`` and never blocks a continuation, so it
  fires AT MOST ONCE per yield. After the nudge the orchestrator either does
  productive work (and the next stop is a fresh decision) or states plainly that
  nothing is available and takes the escape.
- Escapable: ``touch <GRC_DROP_ROOT>/.allow-waiting-yield`` is honoured and deleted,
  so a genuine no-productive-work yield is one command away. The block message prints
  it. The escape is reachable by the actor (a Bash tool call), which is the point: the
  guard is a speed bump plus a forcing question, not a wall.
- The escape is consumed ONLY on a turn the hook was about to block. An ordinary
  turn-end while the sentinel happens to exist leaves it untouched, so the actor
  cannot lose the escape it just armed.
- Fails open: any error (no transcript, unreadable, unexpected shape) returns allow.
  A guard that traps the actor on its own malfunction gets removed. That extends to
  the sentinel: if the sentinel exists but cannot be unlinked, the turn is ALLOWED
  anyway (the actor's intent was recorded; a filesystem fault must not become a wall).

TRIGGER SET PROVENANCE. The pattern list is authored here, seeded from the phrasings
the orchestrator actually used on 2026-08-09 and broadened with the common yield
dialects (stand by, pending, resume when, check back, over to you, and friends). It
is not a citation of any external inventory; there is no such document.

NEGATIVE GUARDS. Before matching, the text is sanitised to drop the most common
LEGITIMATE uses of the vocabulary: fenced code blocks, inline code spans, double- or
curly-quoted spans, path tokens such as ``foo.py``, ``await`` used as a language
keyword, hyphen / underscore compounds (``wait-free``, ``busy-wait``, ``wait_for``),
negated uses (``do not wait``, ``instead of waiting``), historical narration (``caused
the agent to wait``), and the non-yield ``re-invoke`` forms (``pre-invoke``,
``reinvoked``, ``re-invoker``). A turn that is DESCRIBING this hook itself is exempt
outright.

RESIDUE STATED. The trigger is the WORD, not a verified absence of productive work;
the hook cannot know whether productive work exists. That is deliberate: the word is
the observable signal that the orchestrator is yielding to a wait, and the forcing
question ("what can you do now?") is exactly the revisit that was missing. The
negative guards are lexical, not semantic, so a residual FALSE-POSITIVE rate remains.
Measured examples that still fire: "Payment is due on delivery" (the commercial sense
of ``on delivery``), "the monitor will show the queue depth" (``the monitor will``),
and an unquoted prose mention of standing by or handing off inside a report. That is
accepted and NOT worth more lexical machinery: this is a once-only, fail-open, escapable
nudge, so a cheap false positive costs one turn and one ``touch``. A residual
FALSE-NEGATIVE rate remains too: any phrasing outside the set passes through, and the
guard makes no claim to catch every dialect of yielding.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))
ESCAPE_FILE = WORKING_ROOT / ".allow-waiting-yield"

# A Stop hook fires only at turn-END, so any of these in the final main-thread message
# is a yield-to-wait signal, not mid-turn prose. Matched case-insensitively. Entries
# are word-anchored where a boundary is meaningful; "re-?invoke" carries a LEADING
# boundary only, so "reinvokes" still matches while "pre-invoke" no longer does.
WAITING_PATTERNS = [
    r"\bre-?invoke",
    r"\bawaiting\b",
    r"\bawaits\b",              # the plain third-person form: "the result awaits"
    r"\bawait\b",
    r"\bwait\b",                # bare "wait" too: "a genuine wait" slips past \bwaiting\b
    r"\bwaiting\b",
    r"dispatch-and-await",      # the dressed-up substitutes the actor actually used
    r"offload-and-await",
    r"\bnot idle\b",            # "this is not idle time" is the rationalization
    r"not (just )?sitting",
    r"genuine (dispatch|offload|wait)",
    r"i['’]?ll wait\b",
    r"i will wait\b",
    r"the monitor will\b",
    r"will re-?invoke\b",
    r"i['’]?ll report when\b",
    r"\bon delivery\b",
    # Broadened yield dialects (claude-F3 / codex-F2): common ways of saying the same
    # thing that the 2026-08-09 set missed entirely.
    r"\bstand(ing)? by\b",
    r"\bsitting tight\b",
    r"\bhold(ing)? (here|off|tight)\b",
    r"\bpaus(e|ed|ing)\b",
    r"\bresum(e|ing) (when|once|after)\b",
    r"\bcheck(ing)? back\b",
    r"\bping me when\b",
    r"\blet me know when\b",
    r"\bover to you\b",
    r"\bnothing (further|more|else) until\b",
    r"\bnothing to do (meanwhile|in the meantime)\b",
    r"\bblocked on\b",
    r"\bidle until\b",
    r"\byield(ing)? the turn\b",
    r"\bhand(ing)? off\b",
    r"\bpending the\b",
    r"\buntil (it|the \w+) (returns|lands|delivers|finishes|completes|goes green)\b",
]
_RX = re.compile("|".join(WAITING_PATTERNS), re.IGNORECASE)

# Spans removed before matching: legitimate uses of the vocabulary that are not a
# yield. Replaced with a space so surrounding words keep their boundaries.
_STRIP_PATTERNS = [
    r"```.*?```",                                  # fenced code blocks
    r"`[^`]*`",                                    # inline code spans
    r'"[^"]*"',                                    # double-quoted spans
    r"“[^”]*”",                     # curly double quotes
    r"‘[^’]*’",                     # curly single quotes (not apostrophes)
    r"[\w./-]+\.(?:py|js|jsx|ts|tsx|md|sh|json|ya?ml|toml|txt|cfg|ini)\b",  # path tokens
    r"\basync[ /-]?await\b",                       # the language construct
    r"\bawait\b(?=\s*\()",                         # await( ... ) call syntax
    r"\bawait\s+(?:keyword|expression|syntax|point|statement)\b",
    r"\b(?:the|an?)\s+await\b(?=\s+(?:in|of|on)\b)",
    r"\b\w+[-_](?:a?wait(?:ing|s)?)\b",            # busy-wait, spin_wait, no-wait
    r"\ba?wait[-_]\w+\b",                          # wait-free, wait_for, await-free
    r"\b(?:do not|does not|did not|don['’]t|doesn['’]t|didn['’]t|"
    r"no need to|never|instead of|rather than|without|stop|avoid)\s+"
    r"(?:a?wait(?:ing|s)?)\b",                     # negated uses
    r"\bno longer\s+(?:\w+\s+){0,3}?a?wait(?:ing|s)?\b",   # "no longer needs to wait"
    r"\b(?:caused|forced|made|led|used)\b[^.;]{0,40}?\bto\s+a?wait\b",  # historical narration
    r"\b(?:backoff|timeout|retry|polling|poll|sleep|blocking)\s+a?wait\b",
    r"\ba?wait\s+(?:state|time|times|queue|loop|condition|group|handle)\b",
    r"\bre-?invoked\b",                            # past tense: already happened
    r"\bre-?invokers?\b",                          # the noun (a tool), not the act
    r"\bpre-?invoke\w*\b",
]
_STRIP_RXS = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in _STRIP_PATTERNS]

# A turn that is DESCRIBING this hook is exempt: shipping, reviewing, or documenting
# the guard would otherwise trip it every time (claude-F2).
_SELF_REF_RX = re.compile(
    r"block-waiting-word-yield"
    r"|waiting-word (?:hook|guard|yield|set|pattern)"
    r"|allow-waiting-yield"
    r"|guardrail 1\.26\.48",
    re.IGNORECASE,
)


def last_assistant_text(transcript_path: str) -> str:
    """The concatenated text of the LAST MAIN-THREAD assistant message.

    Sidechain (subagent) rows are skipped. Returns "" on ANY failure or unexpected
    shape: unreadable path, undecodable line, non-object row, non-string text."""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError):
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue          # a bare list / string / number row is not a message
        if obj.get("isSidechain"):
            continue          # a subagent's turn is not the orchestrator yielding
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
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue
                value = block.get("text")
                if isinstance(value, str):
                    parts.append(value)      # text: null / 7 / {} is dropped, not raised
        return "\n".join(parts)
    return ""


def _sanitize(text: str) -> str:
    """Drop the legitimate-use spans so they cannot trigger the nudge."""
    for rx in _STRIP_RXS:
        text = rx.sub(" ", text)
    return text


def first_trigger(text: str) -> str | None:
    """The first waiting-word/phrase present in the text, else None."""
    if not text:
        return None
    if _SELF_REF_RX.search(text):
        return None           # the turn is about this hook, not a yield
    m = _RX.search(_sanitize(text))
    return m.group(0) if m else None


def decide(stop_hook_active: bool, text: str) -> str | None:
    """Return a block message, or None to allow. Pure: no IO, no escape handling.

    The escape is deliberately NOT an input here: main() consumes it only after this
    function has already decided to block."""
    if stop_hook_active:
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
    """True iff the escape sentinel was present (and so the turn must be ALLOWED).

    Called ONLY when the hook is about to block, so an ordinary turn never burns it.
    A present sentinel allows the turn even if it cannot be removed: the actor's
    stated intent is honoured and a filesystem fault never becomes a spurious block
    (codex-F4). The cost of that fail-open is that an unremovable sentinel keeps
    allowing, which is the safe direction for a nudge."""
    try:
        if not ESCAPE_FILE.is_file():
            return False
    except OSError:
        return False
    try:
        ESCAPE_FILE.unlink()
    except OSError:
        pass
    return True


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        return 0  # fail-open on a malformed payload
    try:
        if not isinstance(payload, dict):
            return 0
        if payload.get("stop_hook_active"):
            return 0  # a continuation is under way: never block again
        text = last_assistant_text(payload.get("transcript_path", ""))
        message = decide(False, text)
        if message is None:
            return 0  # no trigger: the sentinel, if any, is left untouched
        if _consume_escape():
            return 0  # escape taken (consumed here, and only here)
        print(message, file=sys.stderr)
        return 2
    except Exception:
        return 0  # fail-open on any unexpected error


def _self_test() -> int:
    import contextlib
    import io
    import tempfile
    import unittest

    def run_main(payload):
        """Drive main() end-to-end with a JSON payload on stdin; return exit code."""
        stdin = sys.stdin
        sys.stdin = io.StringIO(json.dumps(payload))
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                return main(["hook"])
        finally:
            sys.stdin = stdin

    @contextlib.contextmanager
    def escape_at(path):
        """Point the module-level ESCAPE_FILE at a test double / temp path."""
        global ESCAPE_FILE
        original = ESCAPE_FILE
        ESCAPE_FILE = path
        try:
            yield
        finally:
            ESCAPE_FILE = original

    def transcript(rows):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
            return f.name

    def assistant_row(text, sidechain=False):
        row = {"type": "assistant", "message": {"role": "assistant",
               "content": [{"type": "text", "text": text}]}}
        if sidechain:
            row["isSidechain"] = True
        return row

    class Unremovable:
        """A sentinel that exists but whose unlink always fails."""
        def is_file(self):
            return True

        def unlink(self):
            raise OSError("read-only file system")

        def __str__(self):
            return "/unwritable/.allow-waiting-yield"

    class T(unittest.TestCase):
        # ---- positive triggers (original set) ----
        def test_reinvoke_blocks(self):
            self.assertIsNotNone(decide(False, "the monitor will re-invoke me on delivery"))

        def test_awaiting_blocks(self):
            self.assertIsNotNone(decide(False, "Awaiting the r2 dual-family result."))

        def test_ill_wait_blocks(self):
            self.assertIsNotNone(decide(False, "I'll wait for the workers to deliver."))
            self.assertIsNotNone(decide(False, "I’ll wait for the workers."))

        def test_waiting_blocks(self):
            self.assertIsNotNone(decide(False, "Genuine dispatch-and-await; recording the wait. waiting on CI."))

        def test_on_delivery_blocks(self):
            self.assertIsNotNone(decide(False, "I'll reconcile on delivery."))

        def test_sneaky_substitutes_block(self):
            for phrase in (
                "This is a genuine wait, all prep complete.",
                "A legitimate dispatch-and-await, not idle time.",
                "Genuine offload-and-await; the worker is drafting.",
                "I'm not just sitting; the monitor is armed.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        # ---- broadened coverage (claude-F3 / codex-F2) ----
        def test_broadened_yield_phrasings_block(self):
            for phrase in (
                "The result awaits; I'll pick it up then.",
                "Standing by for the worker result.",
                "I will stand by until CI finishes.",
                "Pausing until the worker returns.",
                "I will resume when the worker delivers.",
                "I will check back once CI completes.",
                "Sitting tight for the moment.",
                "Holding here for the reviewer.",
                "Over to you.",
                "Let me know when the workers deliver.",
                "Ping me when the sweep finishes.",
                "Nothing further until the worker returns.",
                "Pending the r2 result.",
                "Blocked on CI; will pick this up once it goes green.",
                "Idle until delivery lands.",
                "Yielding the turn now.",
                "Handing off to the reviewer.",
                "In flight: 2 workers. Nothing to do meanwhile.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_reinvoke_leading_anchor(self):
            # anchored, so unrelated compounds no longer over-match (claude-F4)
            self.assertIsNone(decide(False, "Added a pre-invoke sanity check to exec dispatch."))
            self.assertIsNone(decide(False, "The reinvoked worker finished; 3 findings closed."))
            self.assertIsNone(decide(False, "Renamed re-invoker to dispatcher."))
            self.assertIsNotNone(decide(False, "The monitor reinvokes me when the sweep ends."))

        # ---- negative guards (claude-F5 / codex-F1) ----
        def test_code_keyword_uses_allow(self):
            for phrase in (
                "The Python await keyword is only valid inside async functions; done.",
                "Refactored the async/await path; all tests pass.",
                "Documented the await-free fast path.",
                "Documented the wait-free queue algorithm in references/concurrency.md.",
                "Removed a busy-wait loop from tools/exec-dispatch.py.",
                "The retry uses an exponential backoff wait of 200ms; merged.",
                "Renamed wait_for_completion to wait_until_ready; 12 call sites updated.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_quoted_and_code_span_uses_allow(self):
            for phrase in (
                "Fixed the missing `await` keyword in the async helper; tests pass.",
                'The old message read "I will wait for CI" and is now replaced.',
                "Shipped the change to hooks/block-turn-end.py; 89 gates green.",
                "```\nawait worker.result()\n```\nMerged.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_negated_uses_allow(self):
            for phrase in (
                "Do not wait for CI; proceed with the next task now.",
                "Instead of waiting, I prepped the next two seeds; both are ready.",
                "The fix means the agent no longer needs to wait; merged.",
                "The previous bug caused the agent to wait, and this fix is now complete.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_self_reference_allows(self):
            for phrase in (
                "Guardrail 1.26.48: activate block-waiting-word-yield Stop hook.",
                "Added the block-waiting-word-yield Stop hook per PR #1471.",
                "Broadened the waiting-word set; the escape is .allow-waiting-yield.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_ordinary_message_allows(self):
            self.assertIsNone(decide(False, "Fixed the three findings; all 89 gates green; merging."))
            self.assertIsNone(decide(False, "Here is the reconciled result: 2 errors fixed."))

        # ---- loop safety ----
        def test_stop_hook_active_allows(self):
            self.assertIsNone(decide(True, "re-invoke me later"))

        # ---- transcript parsing ----
        def test_last_assistant_extraction(self):
            path = transcript([
                {"type": "user", "message": {"role": "user", "content": "hi"}},
                assistant_row("first"),
                assistant_row("awaiting the result"),
            ])
            try:
                self.assertEqual(last_assistant_text(path), "awaiting the result")
                self.assertIsNotNone(decide(False, last_assistant_text(path)))
            finally:
                os.unlink(path)

        def test_sidechain_message_is_skipped(self):
            # a subagent's "Awaiting" must not trigger the orchestrator's nudge (claude-F6)
            path = transcript([
                assistant_row("Fixed the three findings; all gates green."),
                assistant_row("Awaiting the sweep result.", sidechain=True),
            ])
            try:
                self.assertEqual(last_assistant_text(path),
                                 "Fixed the three findings; all gates green.")
                self.assertIsNone(decide(False, last_assistant_text(path)))
            finally:
                os.unlink(path)

        def test_bad_shapes_return_empty(self):
            # every malformed row shape must yield "", never raise (codex-F5)
            for rows in (
                [[]],                                                   # bare list row
                ["not-an-object"],                                      # bare string row
                [{"type": "assistant", "message": {"role": "assistant",
                  "content": [{"type": "text", "text": None}]}}],       # text: null
                [{"type": "assistant", "message": {"role": "assistant",
                  "content": [{"type": "text"}]}}],                     # text missing
                [{"type": "assistant", "message": {"role": "assistant",
                  "content": [None, 7]}}],                              # non-dict blocks
                [{"type": "assistant", "message": {"role": "assistant",
                  "content": 42}}],                                     # non-list content
                [{"type": "assistant", "message": "not-a-dict"}],       # message not a dict
            ):
                path = transcript(rows)
                try:
                    self.assertEqual(last_assistant_text(path), "", repr(rows))
                finally:
                    os.unlink(path)

        def test_garbage_and_missing_transcript_are_empty(self):
            self.assertEqual(last_assistant_text("/nonexistent/x.jsonl"), "")
            self.assertIsNone(decide(False, last_assistant_text("/nonexistent/x.jsonl")))
            with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
                f.write("{not json\n\n")
                path = f.name
            try:
                self.assertEqual(last_assistant_text(path), "")
            finally:
                os.unlink(path)

        # ---- escape lifecycle ----
        def test_escape_not_burned_on_ordinary_stop(self):
            # codex-F3 / claude-F1: an ordinary turn must leave the sentinel alone
            path = transcript([assistant_row("All 89 gates green; merged.")])
            with tempfile.TemporaryDirectory() as d:
                sentinel = Path(d) / ".allow-waiting-yield"
                sentinel.write_text("")
                try:
                    with escape_at(sentinel):
                        self.assertEqual(run_main({"transcript_path": path}), 0)
                        self.assertTrue(sentinel.is_file())
                        # the sentinel survives and still works on the NEXT real yield
                        yielded = transcript([assistant_row("Awaiting the worker.")])
                        try:
                            self.assertEqual(run_main({"transcript_path": yielded}), 0)
                            self.assertFalse(sentinel.is_file())
                        finally:
                            os.unlink(yielded)
                finally:
                    os.unlink(path)

        def test_escape_consumed_only_on_a_blocking_turn(self):
            path = transcript([assistant_row("Awaiting the r2 result.")])
            with tempfile.TemporaryDirectory() as d:
                sentinel = Path(d) / ".allow-waiting-yield"
                sentinel.write_text("")
                try:
                    with escape_at(sentinel):
                        self.assertEqual(run_main({"transcript_path": path}), 0)
                        self.assertFalse(sentinel.is_file())
                        # once-only: the next yield blocks again
                        self.assertEqual(run_main({"transcript_path": path}), 2)
                finally:
                    os.unlink(path)

        def test_unlink_failure_allows(self):
            # codex-F4: a present-but-unremovable sentinel must ALLOW, not block
            path = transcript([assistant_row("Awaiting the worker result.")])
            try:
                with escape_at(Unremovable()):
                    self.assertTrue(_consume_escape())
                    self.assertEqual(run_main({"transcript_path": path}), 0)
            finally:
                os.unlink(path)

        def test_absent_sentinel_blocks_a_real_yield(self):
            path = transcript([assistant_row("Awaiting the worker result.")])
            with tempfile.TemporaryDirectory() as d:
                try:
                    with escape_at(Path(d) / ".allow-waiting-yield"):
                        self.assertEqual(run_main({"transcript_path": path}), 2)
                finally:
                    os.unlink(path)

        # ---- main() fail-open ----
        def test_main_fails_open(self):
            with tempfile.TemporaryDirectory() as d:
                with escape_at(Path(d) / ".allow-waiting-yield"):
                    self.assertEqual(run_main({}), 0)                      # no transcript key
                    self.assertEqual(run_main([1, 2, 3]), 0)               # non-dict payload
                    self.assertEqual(run_main({"transcript_path": "/nope/x.jsonl"}), 0)

        def test_main_honours_stop_hook_active(self):
            path = transcript([assistant_row("Awaiting the worker result.")])
            with tempfile.TemporaryDirectory() as d:
                sentinel = Path(d) / ".allow-waiting-yield"
                sentinel.write_text("")
                try:
                    with escape_at(sentinel):
                        self.assertEqual(
                            run_main({"transcript_path": path, "stop_hook_active": True}), 0)
                        self.assertTrue(sentinel.is_file())  # and it does not burn the escape
                finally:
                    os.unlink(path)

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if result.wasSuccessful():
        print("OK", file=sys.stderr)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
