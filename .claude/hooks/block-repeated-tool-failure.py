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

# `_hook_state` is colocated in .claude/hooks/. The settings.json launcher runs `python3 -I`
# (SECI-config-is-executable-trust-gate): no directory ever enters sys.path, the helper
# executes ONLY from its reviewed source bytes via _load_sibling below, and no import
# statement names it, so nothing planted beside this hook (a decoy module, a
# __pycache__/*.pyc, a seeded sys.modules entry) can run. MISSING-HELPER BEHAVIOUR
# (fail-open): _hook_state stays None and this hook simply allows.
def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


try:
    _hook_state = _load_sibling("_hook_state")
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
        "answered-question": "run `python3 "
                             "tools/decisions-search.py <key>`, read the recorded answer, and "
                             "act on it instead of re-asking",
    }.get(blocking_hook, "change its STRUCTURE (not just its wording or description) so it no "
                         "longer trips the same block")
    lines = [
        f"BLOCKED (repeated-tool-failure): REPEAT-BLOCK: an UNCHANGED resubmission of a command that "
        f"`{blocking_hook}` just blocked.\n"
        f"WHY: the literal command string does not reflect the fix the block asked for (a common "
        f"cause is editing the command DESCRIPTION, not the command STRING); resubmitting the "
        f"same shape is the intent-vs-artefact loop this guard breaks.\n"
        f"CONSIDER INSTEAD: {steer}."
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
            "the operational store's `degradation-watch-log.md` (resolved via lint_common.resolve_working) and read plus assess it (session "
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
    # Every scratch path the self-test makes (including a child git's) lands under one root that is
    # removed on exit, so a run leaves nothing behind in the temp directory (3b103).
    import atexit as _atx, os as _os, shutil as _shu, tempfile as _tpf
    _tpf.tempdir = _tpf.mkdtemp(prefix="grc-selftest-"); _os.environ["TMPDIR"] = _tpf.tempdir
    _atx.register(_shu.rmtree, _tpf.tempdir, True)
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
            self.assertIn("repeated-tool-failure", reason)
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
