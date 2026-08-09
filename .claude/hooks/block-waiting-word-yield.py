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
  fires AT MOST ONCE per yield.
- Escapable: ``touch <GRC_DROP_ROOT>/.allow-waiting-yield`` is honoured and deleted,
  so a genuine no-productive-work yield is one command away. The block message prints
  it. The escape is reachable by the actor (a Bash tool call), which is the point: the
  guard is a speed bump plus a forcing question, not a wall.
- The escape is consumed ONLY on a turn the hook was about to block. An ordinary
  turn-end while the sentinel happens to exist leaves it untouched.
- Fails open: any error (no transcript, unreadable, unexpected shape, RecursionError
  from the JSON decoder) returns allow. That extends to the sentinel in BOTH
  directions: if it cannot be STATTED, or exists but cannot be UNLINKED, the turn is
  ALLOWED anyway (a filesystem fault must never become a wall).

ITER-4: ROOT-CAUSE SIMPLIFICATION OF THE CONTEXT GUARDS.
Three verify rounds each found NEW false-negatives in the elaborate context-guard
machinery, always in a DIFFERENT edge of the same four constructs:
  r1 -> whole-message self-reference exemption swallowed a real yield;
  r2 -> the compound strip ate ``-and-await``, silently allowing the two explicit
        yield targets, and blanket quote-stripping swallowed a quoted status;
  r3 -> the SENTENCE-scoped self-reference exemption still swallowed any yield joined
        with a comma or "and" (both families, blocking); plus ``wait-and-see`` and
        ``dispatch-and-await-results`` eaten by the wait-leading compound rule;
        ``I am being forced to wait`` eaten by the retrospective-narration strip;
        ``My status is "waiting"`` eaten by the quoted-vocabulary exemption; and
        ``I am entering a wait state`` eaten by the wait-noun strip.
The edge-case set of that machinery is UNBOUNDED, and each guard fights the hook's own
purpose. This is a fail-open, once-only, ESCAPABLE NUDGE: a false POSITIVE costs the
actor ONE ``touch`` and is cheap; a false NEGATIVE on a real yield DEFEATS the hook.
So the correct design ERRS TOWARD FIRING, and iter-4 DELETES the fragile guards rather
than adding another lookahead:

  REMOVED  self-reference exemption (all of it: _SELF_REF_RX, _SENTENCE_SPLIT_RX,
           _drop_self_ref_sentences). Naming this hook now FIRES; that costs one touch.
  REMOVED  retrospective-narration strip (``caused|forced|made ... to wait``).
  REMOVED  the wait-leading / compound-await protection lookaheads. The identifier
           exemption below is an explicit ALLOWLIST of single identifiers instead, so
           there is nothing for a phrase join to escape from.
  REMOVED  quoted-status vocabulary exemption (_VOCAB_QUOTE_RX and friends). Quotes are
           now ordinary text: ``My status is "waiting".`` fires.
  REMOVED  ``await state / queue / loop / condition / group / handle`` noun strips.
  REMOVED  technical wait-noun strips (``backoff|retry|polling|sleep wait``), negated-use
           strips (``do not wait``, ``instead of waiting``), and the ``reinvoked`` /
           ``re-invoker`` past-tense strips. All now fire. Accepted, see RESIDUE.

WHAT REMAINS (the whole exemption set, and nothing else). Each of these is
UNAMBIGUOUS: it never coincides with a real yield.
  (a) CODE: fenced blocks and inline `code spans`, plus bare path tokens (``foo.py``).
      A filename is a code identifier, not a yield.
  (b) CODE CONSTRUCTS: ``async/await``; ``await(``; ``await <expr>(`` with NO space
      before the paren (``await worker.result()``). The no-space requirement is what
      keeps ``I await results (from CI)`` firing.
  (c) IDENTIFIER COMPOUNDS, as an explicit allowlist of SINGLE identifiers, never a
      generic ``\\w+-wait`` rule: ``wait_for*``, ``busy-wait``, ``spin_wait``,
      ``wait-free``, ``await-free`` (either joiner). Phrase joins such as
      ``dispatch-and-await`` are NOT in the list and therefore FIRE.
  Note that UNDERSCORE-joined identifiers (``wait_for_completion``, ``spin_wait``,
  ``dispatch_and_await``) never match the patterns anyway, because ``_`` is a word
  character and kills the word boundary. The allowlist spells both joiners regardless,
  so the exemption does not silently depend on that.

TRIGGER SET PROVENANCE. The pattern list is UNCHANGED by iter-4. It is authored here,
seeded from the phrasings the orchestrator actually used on 2026-08-09 and broadened
with the common yield dialects (stand by, pending, resume when, check back, over to
you, and friends). It is not a citation of any external inventory.

RESIDUE STATED (all accepted, all in the ERR-TOWARD-FIRING direction).
These FIRE and are meant to; each costs one ``touch``:
  - naming this hook or its escape file without a ``.py`` extension
    ("Added the block-waiting-word-yield Stop hook") ;
  - negated uses ("Do not wait for CI", "Instead of waiting, I prepped the seeds") ;
  - retrospective narration ("The bug caused the agent to wait") ;
  - technical wait-nouns in prose ("a backoff wait of 200ms", "a wait state") ;
  - discussing the vocabulary in quotes rather than backticks (the "await" keyword) ;
  - past-tense re-invocation ("the reinvoked worker finished", "renamed re-invoker") ;
  - the commercial "on delivery", "the monitor will show the queue depth", and a
    quoted historical yield.
The fix for every one of them is backticks or one ``touch``. That is the intended
trade. FALSE NEGATIVES that remain, on the record: any phrasing outside the pattern
list passes (the guard claims no dialect completeness), and underscore spellings of the
compound targets (``dispatch_and_await``) do not match, because the pattern list is
unchanged by design. The trigger is the WORD, not a verified absence of productive
work; the forcing question ("what can you do now?") is the point.
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
# is a yield-to-wait signal, not mid-turn prose. Matched case-insensitively. UNCHANGED
# by iter-4: the simplification is entirely on the exemption side. "re-?invoke" carries
# a LEADING boundary only, so "reinvokes" matches while "pre-invoke" does not.
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
    # Broadened yield dialects: common ways of saying the same thing that the
    # 2026-08-09 set missed entirely.
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

# (a) CODE. A fenced block or an inline span is never the orchestrator yielding.
_CODE_PATTERNS = [
    r"```.*?```",                                  # fenced code blocks
    r"`[^`]*`",                                    # inline code spans
]
_CODE_RXS = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in _CODE_PATTERNS]

# The COMPLETE exemption set. Nothing is added here without the test that a real yield
# cannot hide inside it. Replaced with a space so surrounding words keep their
# boundaries. If in doubt whether an exemption is safe: DROP it, and let it fire.
_EXEMPT_PATTERNS = [
    # (a) bare path tokens: a filename is a code identifier, not a yield.
    r"[\w.-]+\.(?:py|js|jsx|ts|tsx|md|sh|json|ya?ml|toml|txt|cfg|ini)\b",
    # (b) language constructs.
    r"\basync[ /-]?await\b",
    r"\bawait\b(?=\s*\()",                         # await( ... )
    r"\bawait\s+[A-Za-z_][\w.]*\(",                # await worker.result()  (no space)
    # (c) identifier compounds, an explicit allowlist of SINGLE identifiers. There is
    # deliberately NO generic \w+[-_]wait rule here: that rule is what ate
    # "dispatch-and-await" in r2 and "wait-and-see" in r3, and it needed a lookahead
    # to survive at all. Phrase joins are not identifiers and are not exempt.
    r"\b(?:busy|spin)[-_]a?wait(?:ing|s|ed|er)?\b",
    r"\bwait[-_]for\w*\b",                         # wait_for, wait_for_completion
    r"\ba?wait[-_]free\b",                         # wait-free, await-free
]
_EXEMPT_RXS = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in _EXEMPT_PATTERNS]


def last_assistant_text(transcript_path: str) -> str:
    """The concatenated text of the LAST MAIN-THREAD assistant message.

    Sidechain (subagent) rows are skipped. Returns "" on ANY failure or unexpected
    shape: unreadable path, non-string path, undecodable line, over-nested JSON,
    non-object row, non-string text."""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError, TypeError):
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue      # a deeply nested array overflows the decoder
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
    """Drop code and the three unambiguous exemption classes. Nothing else."""
    for rx in _CODE_RXS:
        text = rx.sub(" ", text)
    for rx in _EXEMPT_RXS:
        text = rx.sub(" ", text)
    return text


def all_triggers(text: str) -> list:
    """Every non-overlapping waiting-word match, in order. Used to PIN sole triggers."""
    if not text:
        return []
    return [m.group(0) for m in _RX.finditer(_sanitize(text))]


def first_trigger(text: str) -> str | None:
    """The first waiting-word/phrase present in the text, else None."""
    if not text:
        return None
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
    """True iff the turn must be ALLOWED on account of the escape sentinel.

    Called ONLY when the hook is about to block, so an ordinary turn never burns it.
    Every filesystem fault resolves to ALLOW, in both directions:
    - the stat itself failing means the hook cannot determine the escape state, and a
      guard that cannot read its own escape hatch must not become a wall;
    - a present sentinel that cannot be unlinked still honours the actor's intent.
    The cost of that fail-open is that an unremovable sentinel keeps allowing, which is
    the safe direction for a nudge."""
    try:
        present = ESCAPE_FILE.is_file()
    except OSError:
        return True           # cannot stat: fail OPEN, never block on a filesystem fault
    if not present:
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


# The mandated isolated-target set. Each phrase carries the target as its SOLE trigger:
# the tests assert both that it blocks AND that exactly one pattern matched, so a
# broken target cannot be propped up by a neighbouring co-trigger.
MUST_BLOCK = [
    ("Dispatch-and-await.", "dispatch-and-await"),
    ("Offload-and-await.", "offload-and-await"),
    ("I will dispatch-and-await from the worker.", "dispatch-and-await"),
    ("blocking wait on the worker.", "wait"),
    ('Status: "waiting on CI".', "waiting"),
    ('My status is "waiting".', "waiting"),
    ("I am being made to wait for CI.", "wait"),
    ("I used the monitor to wait.", "wait"),
    ("I reviewed block-waiting-word-yield.py and I'll wait for CI.", "i'll wait"),
    ("I reviewed the hook, waiting on CI.", "waiting"),
    ("I'll wait.", "i'll wait"),
]

MUST_ALLOW = [
    "The function uses async/await.",
    "Removed a busy-wait loop.",
    "Renamed wait_for_completion.",
    "Fixed all findings; merging.",
]


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

    def transcript(rows, raw=None):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            if raw is not None:
                f.write(raw)
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

    class Unstattable:
        """A sentinel path whose stat itself fails."""
        def is_file(self):
            raise OSError("stat denied")

        def unlink(self):
            raise AssertionError("unlink must not be reached")

        def __str__(self):
            return "/unstattable/.allow-waiting-yield"

    class T(unittest.TestCase):
        # ---- MANDATED must-block set, each target pinned as the SOLE trigger ----
        def test_must_block_set_blocks(self):
            for phrase, _ in MUST_BLOCK:
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_must_block_set_is_sole_trigger(self):
            # the whole point of the isolation requirement: exactly ONE match, and it
            # is the intended token, so no co-trigger can mask a regressed target.
            for phrase, expected in MUST_BLOCK:
                found = all_triggers(phrase)
                self.assertEqual(len(found), 1, (phrase, found))
                self.assertEqual(found[0].lower(), expected, (phrase, found))

        def test_must_block_set_blocks_end_to_end(self):
            for phrase, _ in MUST_BLOCK:
                path = transcript([assistant_row(phrase)])
                with tempfile.TemporaryDirectory() as d:
                    try:
                        with escape_at(Path(d) / ".allow-waiting-yield"):
                            self.assertEqual(run_main({"transcript_path": path}), 2, phrase)
                    finally:
                        os.unlink(path)

        # ---- MANDATED must-allow set ----
        def test_must_allow_set_allows(self):
            for phrase in MUST_ALLOW:
                self.assertIsNone(decide(False, phrase), phrase)
                self.assertEqual(all_triggers(phrase), [], phrase)

        def test_must_allow_set_allows_end_to_end(self):
            for phrase in MUST_ALLOW:
                path = transcript([assistant_row(phrase)])
                with tempfile.TemporaryDirectory() as d:
                    try:
                        with escape_at(Path(d) / ".allow-waiting-yield"):
                            self.assertEqual(run_main({"transcript_path": path}), 0, phrase)
                    finally:
                        os.unlink(path)

        # ---- the surviving exemptions: (a) code, (b) constructs, (c) identifiers ----
        def test_identifier_compounds_allow(self):
            for phrase in (
                "Removed a busy-wait loop.",
                "Removed a busy_wait loop.",
                "Renamed spin_wait to park.",
                "Renamed spin-wait to park.",
                "Renamed wait_for_completion.",
                "Renamed wait_for to wait_until_ready.",
                "Documented the wait-free queue algorithm.",
                "Documented the await-free fast path.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_code_constructs_allow(self):
            for phrase in (
                "The function uses async/await.",
                "The function uses async await syntax.",
                "The helper calls await worker.result() before returning.",
                "The helper calls await(fut) before returning.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        def test_code_spans_and_fences_allow(self):
            for phrase in (
                "Fixed the missing `await` keyword in the async helper; tests pass.",
                "Renamed `waiting` to `pending` in the status line; merged.",
                "```\nawait worker.result()\n```\nMerged.",
                "Shipped the change to hooks/block-turn-end.py; 89 gates green.",
            ):
                self.assertIsNone(decide(False, phrase), phrase)

        # ---- the exemptions must NOT swallow phrase joins (the r2/r3 defect class) ----
        def test_phrase_joins_are_not_exempt(self):
            # no generic \w+[-_]wait rule exists any more, so these need no lookahead
            for phrase in (
                "Dispatch-and-await.",
                "Offload-and-await.",
                "This is a dispatch-then-await on the reviewers.",
                "This is a dispatch-or-await on the reviewers.",
                "I will dispatch-and-await-results from the worker.",
                "I'll wait-and-see on the CI result.",
                "This is a blocking-wait on the worker.",
                "This is a dispatch-await on the reviewers.",
                "Set up an offload-await for the sweep.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        # ---- the four removed guards: every r3 failing case now FIRES ----
        def test_removed_self_reference_exemption(self):
            for phrase in (
                "I reviewed block-waiting-word-yield.py and I'll wait for CI.",
                "Dispatched two reviewers on block-waiting-word-yield.py, "
                "awaiting their deliveries.",
                "I shipped the waiting-word hook and am awaiting the r3 deliveries.",
                "Guardrail 1.26.48 is merged, so I'll wait for the reviewers.",
                "The waiting-word guard is live and I am standing by for the sweep.",
                "Take the escape with touch /home/grc/grc_working/.allow-waiting-yield "
                "and await the worker.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_removed_retrospective_narration_strip(self):
            for phrase in (
                "I am being made to wait for CI.",
                "I am being forced to wait for CI.",
                "The dependency forced me to wait for the r3 reviewer.",
                "That caused me to wait for CI.",
                "The lock made me wait on the worker.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_removed_quoted_vocabulary_exemption(self):
            for phrase in (
                'Status: "waiting on CI".',
                'Status: "waiting".',
                'Status: “waiting”.',
                'My status is "waiting".',
                'My status is "awaiting".',
                'My status is "await".',
                "The ‘wait’ token is the trigger.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_removed_wait_noun_strips(self):
            for phrase in (
                "I am entering a wait state.",
                "I am in a wait loop on the worker.",
                "I am joining the await group for the two workers.",
                "The retry uses a backoff wait of 200ms.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_removed_machinery_is_gone(self):
            # structural pin: the deleted guards must not creep back in
            for name in ("_SELF_REF_RX", "_SENTENCE_SPLIT_RX", "_drop_self_ref_sentences",
                         "_VOCAB_QUOTE_RX", "_QUOTE_SPAN_RXS", "_strip_vocabulary_quotes",
                         "_STRIP_PATTERNS", "_STRIP_RXS"):
                self.assertNotIn(name, globals(), name)

        # ---- accepted false positives: firing is the DESIGN, not a defect ----
        def test_accepted_false_positives_fire(self):
            # each costs the actor one `touch`; that is the stated trade
            for phrase in (
                "The retry uses a backoff wait of 200ms.",
                "Do not wait for CI; proceed with the next task now.",
                "Instead of waiting, I prepped the next two seeds; both are ready.",
                "The previous bug caused the agent to wait, and this fix is complete.",
                "Added the block-waiting-word-yield Stop hook per PR #1471.",
                'Documented the "await" keyword.',
                "The reinvoked worker finished; 3 findings closed.",
                "Renamed re-invoker to dispatcher.",
                'The old message read "I will wait for CI" and is now replaced.',
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        # ---- positive triggers ----
        def test_reinvoke_blocks(self):
            self.assertIsNotNone(decide(False, "The monitor will re-invoke me."))
            self.assertIsNotNone(decide(False, "It reinvokes me later."))
            self.assertIsNotNone(decide(False, "the monitor will re-invoke me on delivery"))

        def test_pre_invoke_allows(self):
            # leading anchor, so unrelated compounds do not over-match
            self.assertIsNone(decide(False, "Added a pre-invoke sanity check to dispatch."))

        def test_sneaky_substitutes_block(self):
            for phrase in (
                "This is a genuine wait, all prep complete.",
                "A legitimate dispatch-and-await, not idle time.",
                "Genuine offload-and-await; the worker is drafting.",
                "I'm not just sitting; the monitor is armed.",
                "Awaiting the r2 dual-family result.",
                "I'll reconcile on delivery.",
                "The result awaits; I'll pick it up then.",
            ):
                self.assertIsNotNone(decide(False, phrase), phrase)

        def test_broadened_yield_phrasings_block(self):
            for phrase in (
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

        def test_ordinary_message_allows(self):
            self.assertIsNone(decide(False, "Fixed all findings; merging."))
            self.assertIsNone(decide(False, "Fixed the three findings; all 89 gates green."))
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
            # a subagent's "Awaiting" must not trigger the orchestrator's nudge
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
            # every malformed row shape must yield "", never raise
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

        def test_deeply_nested_json_row_returns_empty(self):
            # RecursionError from the decoder honours the "" contract
            raw = "[" * 100000 + "0" + "]" * 100000 + "\n"
            path = transcript([], raw=raw)
            try:
                self.assertEqual(last_assistant_text(path), "")
            finally:
                os.unlink(path)

        def test_non_string_transcript_path_returns_empty(self):
            self.assertEqual(last_assistant_text(None), "")

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
            # a present-but-unremovable sentinel must ALLOW, not block
            path = transcript([assistant_row("Awaiting the worker result.")])
            try:
                with escape_at(Unremovable()):
                    self.assertTrue(_consume_escape())
                    self.assertEqual(run_main({"transcript_path": path}), 0)
            finally:
                os.unlink(path)

        def test_stat_failure_allows(self):
            # an OSError from is_file() must fail OPEN, not block
            path = transcript([assistant_row("Waiting on CI.")])
            try:
                with escape_at(Unstattable()):
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
                    self.assertEqual(run_main({"transcript_path": None}), 0)
                    self.assertEqual(run_main(7), 0)                       # scalar payload

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
