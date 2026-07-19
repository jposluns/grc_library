#!/usr/bin/env python3
"""PreToolUse hook (Bash AND AskUserQuestion): break the resubmit-the-blocked-command loop.

Shipped 2026-07-19 after the orchestrator re-submitted a `python3
tools/credit-offload-queue.py ...` command SEVEN times, each blocked by
`block-wrong-repo-tool.py`, without ever adding the `cd` the block asked for: it kept editing
the command DESCRIPTION, not the command STRING. The sibling guards each block one mistake
shape but cannot see that the SAME command is being resubmitted unchanged, nor that the
session is stuck in a retry loop. This hook adds the two cross-cutting guards:

  GUARD 1 (repeat-block loop-breaker): if the current command byte-matches (trailing
    whitespace aside) one a sibling guard BLOCKED within the last few minutes, block again
    with a message that says, in effect: your literal command string did not change, so it
    still fails the same way; change its STRUCTURE, do not resubmit the same shape.

  GUARD 2 (diagnosis circuit-breaker): if there is a run of >= 2 consecutive same-class
    blocks in the recent window, add a hard-stop requirement to WRITE a concrete mechanism
    diagnosis before any further retry, and explicitly forbid attributing the loop to session
    length / degradation before a logged, assessed degradation-watch entry.

State is shared through `_hook_state.py` (a small gitignored JSONL log the sibling guards
append to at block time; see the patch spec). This hook reads that log; it also records its
OWN block when it fires, so the circuit-breaker accumulates even if the harness short-circuits
the remaining matcher hooks once one blocks (which would otherwise stop the siblings from
recording after this hook, placed FIRST, starts blocking). GUARD 1 does not depend on that
ordering: on the FIRST submission this hook runs, finds nothing, and allows, so the sibling
then blocks and records; the match is seen on the resubmission.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. Fail-OPEN on any parse/state error: this is a
guardrail against a retry-loop shape, not a security boundary, and a hook that blocked on a
malformed payload would be worse than the loop it prevents. Like the sibling guards, it does
not fire in a child session whose `CLAUDE_PROJECT_DIR` is unset (documented harness
limitation); the disciplines it enforces are the primary control either way.

Self-test: `python3 .claude/hooks/block-repeated-tool-failure.py --self-test`.
"""

import json
import os
import sys

# `_hook_state` is colocated in .claude/hooks/, which is sys.path[0] when this script is run
# directly (as a hook or via `--self-test`), so a plain import resolves it. Fail-open if it
# is somehow unavailable: without shared state this hook simply allows.
try:
    import _hook_state
except Exception:  # pragma: no cover - defensive
    _hook_state = None

HOOK_NAME = "repeated-tool-failure"


def decide(subject: str):
    """Return (block, reason). Pure w.r.t. side effects: it READS the shared block state but
    does not write it (the caller records). `subject` is the canonical block subject from
    `_hook_state.subject_from_payload`."""
    if _hook_state is None or not isinstance(subject, str) or not subject.strip():
        return False, ""
    prior = _hook_state.find_recent_block(subject)
    if not prior:
        return False, ""  # GUARD 1 gate: only engage on a genuine repeat of a blocked subject

    blocking_hook = prior.get("hook", "a prior guard")
    # The concrete remediation depends on WHICH sibling guard blocked: a class-mismatched
    # example (advising a `cd` after a pipe-guard block) would misdirect the fix, so branch
    # the steer on the recorded hook name and fall back to a class-agnostic clause for any
    # other recorder (and for this hook's own re-fires).
    steer = {
        "wrong-repo": "add an explicit `cd <repo-root> &&` prefix, use `git -C <path>`, or use "
                      "an absolute path so the command targets the intended repo",
        "verification-pipes": "drop the truncating pipe (`| tail`, `| head`, `| grep`); run the "
                              "verification unpiped, or via `tools/tail-safe.sh`, which "
                              "preserves the exit code",
        "answered-question": "the question is already decided; run `python3 "
                             "tools/decisions-search.py <key>`, read the recorded answer, and "
                             "act on it instead of re-asking",
    }.get(blocking_hook, "change its STRUCTURE (not just its wording or description) so it no "
                         "longer trips the same block")
    lines = [
        f"REPEAT-BLOCK (self-guard loop-breaker): you resubmitted a command that "
        f"`{blocking_hook}` just blocked, UNCHANGED. READ your literal command string: it "
        f"does not reflect the fix the block asked for (a common cause is editing the command "
        f"DESCRIPTION, not the command STRING). To fix it: {steer}. Do not "
        f"resubmit the same shape; that is the intent-vs-artefact loop this guard breaks."
    ]

    # GUARD 2: diagnosis circuit-breaker on a run of consecutive same-class blocks.
    run = _hook_state.consecutive_block_count()
    if run >= 2:
        lines.append(
            "CIRCUIT-BREAKER: >= 2 consecutive same-class blocks. Before ANY retry, WRITE a "
            "concrete diagnosis: what literally failed, the exact fix, and how THIS attempt "
            "differs byte-for-byte from the blocked one. Do NOT attribute this to session "
            "length or degradation as a first move; DIAGNOSE THE MECHANISM. If you are about "
            "to cite session length or heaviness, first append a `considered` row to "
            "`grc_library_private/degradation-watch-log.md` and read plus assess it (session "
            "duration, whether a compaction happened, prior real indicators) before asserting "
            "degradation."
        )

    return True, "\n".join(lines)


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    if _hook_state is None:
        return 0  # fail-open: no shared state available
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    try:
        subject = _hook_state.subject_from_payload(payload)
        block, reason = decide(subject)
    except Exception:
        return 0  # fail-open on any unexpected error
    if block:
        # Record this hook's own block so the circuit-breaker run accumulates even under a
        # short-circuiting matcher (see the module docstring). Fail-tolerant inside record_block.
        try:
            _hook_state.record_block(subject, HOOK_NAME)
        except Exception:
            pass
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import tempfile
    import time
    import unittest

    if _hook_state is None:
        print("self-test FAILED: _hook_state not importable")
        return 1

    def _payload_bash(cmd):
        return {"tool_input": {"command": cmd}}

    def _payload_ask(question, header="h"):
        return {"tool_input": {"questions": [{"question": question, "header": header}]}}

    class T(unittest.TestCase):
        def setUp(self):
            # Redirect the shared state file to an isolated temp path for each test.
            self.tmp = tempfile.mkdtemp()
            os.environ["HOOK_STATE_FILE"] = os.path.join(self.tmp, "recent-blocks.jsonl")

        def tearDown(self):
            os.environ.pop("HOOK_STATE_FILE", None)

        def test_fresh_command_allows(self):
            block, _ = decide("python3 tools/credit-offload-queue.py list-workers")
            self.assertFalse(block)

        def test_resubmitted_blocked_command_blocks(self):
            cmd = "python3 tools/credit-offload-queue.py list-workers"
            _hook_state.record_block(cmd, "wrong-repo")  # a sibling blocked it last turn
            block, reason = decide(cmd)
            self.assertTrue(block)
            self.assertIn("REPEAT-BLOCK", reason)
            self.assertIn("wrong-repo", reason)

        def test_structural_change_allows(self):
            blocked = "python3 tools/credit-offload-queue.py list-workers"
            _hook_state.record_block(blocked, "wrong-repo")
            fixed = "cd ../grc_library_scratch && python3 tools/credit-offload-queue.py list-workers"
            block, _ = decide(fixed)
            self.assertFalse(block)  # the command STRING changed, so it is not a repeat

        def test_trailing_whitespace_still_matches(self):
            cmd = "python3 tools/credit-offload-queue.py list-workers"
            _hook_state.record_block(cmd, "wrong-repo")
            block, _ = decide(cmd + "   ")  # only trailing whitespace differs
            self.assertTrue(block)

        def test_non_matching_command_allows(self):
            _hook_state.record_block("python3 tools/a.py", "wrong-repo")
            block, _ = decide("python3 tools/b.py")
            self.assertFalse(block)

        def test_circuit_breaker_escalates_at_two(self):
            cmd = "python3 tools/credit-offload-queue.py list-workers"
            # two consecutive same-class blocks already on record
            _hook_state.record_block(cmd, "repeated-tool-failure")
            _hook_state.record_block(cmd, "repeated-tool-failure")
            block, reason = decide(cmd)
            self.assertTrue(block)
            self.assertIn("CIRCUIT-BREAKER", reason)

        def test_single_prior_block_no_circuit_breaker(self):
            cmd = "python3 tools/credit-offload-queue.py list-workers"
            _hook_state.record_block(cmd, "wrong-repo")  # only one prior block
            block, reason = decide(cmd)
            self.assertTrue(block)
            self.assertNotIn("CIRCUIT-BREAKER", reason)

        def test_stale_block_outside_window_allows(self):
            cmd = "python3 tools/credit-offload-queue.py list-workers"
            # write a record with an old timestamp directly (outside the 180s GUARD-1 window)
            state = os.environ["HOOK_STATE_FILE"]
            old = {"cmd": cmd, "hook": "wrong-repo", "ts": int(time.time()) - 10000}
            with open(state, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(old) + "\n")
            block, _ = decide(cmd)
            self.assertFalse(block)

        def test_askuserquestion_subject_matches(self):
            payload = _payload_ask("Decide the section 3.69 MFA scope")
            subject = _hook_state.subject_from_payload(payload)
            _hook_state.record_block(subject, "answered-question")
            block, reason = decide(subject)
            self.assertTrue(block)
            self.assertIn("answered-question", reason)

        def test_steer_is_class_specific(self):
            # A pipe-guard block must advise dropping the pipe, NOT adding a `cd`
            # (the wrong-repo-specific steer would misdirect the fix).
            cmd = "python3 tools/run_all_audits.sh | tail"
            _hook_state.record_block(cmd, "verification-pipes")
            _, reason = decide(cmd)
            self.assertIn("pipe", reason)
            self.assertNotIn("cd <repo-root>", reason)
            # A wrong-repo block still gets the cd/-C steer.
            cmd2 = "python3 tools/credit-offload-queue.py list-workers"
            _hook_state.record_block(cmd2, "wrong-repo")
            _, reason2 = decide(cmd2)
            self.assertIn("cd <repo-root>", reason2)

        def test_malformed_state_fails_open(self):
            state = os.environ["HOOK_STATE_FILE"]
            with open(state, "w", encoding="utf-8") as fh:
                fh.write("this is not json\n{also not\n")
            block, _ = decide("python3 tools/credit-offload-queue.py list-workers")
            self.assertFalse(block)  # unreadable records -> no match -> allow

        def test_empty_subject_allows(self):
            self.assertFalse(decide("")[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
