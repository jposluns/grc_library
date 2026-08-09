#!/usr/bin/env python3
"""PreToolUse hook (Task / Agent): refuse an IN-SESSION subagent that would run offloadable QA.

CANDIDATE DRAFT for guardrail PR1. Not yet wired into `.claude/settings.json`; the orchestrator
verifies and re-authors before it ships.

WHY THIS EXISTS. The orchestrator's own account is the scarce, slow-to-renew resource. A subagent
dispatched with the Task / Agent tool bills THAT account: an in-session subagent is not an offload,
it is the orchestrator spending itself twice. Running the QA cadence that way cost a full week of
orchestrator usage, which is the specific failure this hook is built to make impossible.

WHY IT DOES NOT LOOK AT THE WORKER REGISTRY, unlike its predecessor. The retired
`block-mandatory-offload.py` (removed in the same PR that added this hook) gated its block on
`count_live_workers() > 0`, and that was a hole rather than a nuance: the deprecated file-drop fleet reads ZERO workers, so the guard fell through
to ALLOW in exactly the situation it was written for. Under the exec'd-worker model a worker is
SPAWNED ON DEMAND (`tools/exec-dispatch.py --dispatch ...`), so "no worker is live" is never a fact
about capability and never a licence to self-run. This hook is therefore UNCONDITIONAL: the only
input to the decision is the dispatch text plus the maintainer's sentinel. There is no
`list-workers` call, no freshness window, and nothing that can read zero and open the gate.

WHY THERE IS NO OVERRIDE ALLOWLIST. The predecessor checked an ALLOW-OVERRIDE marker set FIRST
(pre-push / skeptical / high-assurance / adversarial), biasing the residual error toward a false
ALLOW. Those markers are BLOCK TRIGGERS here, per the PR1 order. That is a POLICY REVERSAL and it
collides with prose still live at this SHA -- see the DOC COLLISION note at the bottom of this
docstring, which the orchestrator must resolve in the same PR.

WHAT IT DOES.
  * Builds a haystack from lower(prompt + description + subagent_type).
  * No QA marker present                       -> ALLOW silently (exit 0).
  * QA marker present, no sentinel             -> BLOCK (exit 2), naming the marker that fired and
                                                  the exec-dispatch invocation to use instead.
  * QA marker present, sentinel present        -> CONSUME the sentinel (delete it), ALLOW, and say
                                                  on stderr that an authorized bypass was spent.

AUTHORIZATION, and it is reachable from a shell. The maintainer creates the sentinel:

    touch /home/grc/grc_working/.allow-orchestrator-qa

It is honoured ONCE and deleted, so an authorization cannot silently become the standing state.
This is the `.allow-stop` pattern from `block-turn-end-with-outstanding-work.py`, chosen for the
same reason recorded there: an environment variable is NOT a reachable escape for the actor,
because a hook inherits the harness environment and never the environment of a Bash tool call.

CONSUME ORDER, deliberate. The sentinel is only tested AFTER the dispatch text has already matched
a QA marker, so an unrelated Task call cannot burn an authorization the maintainer created for a
specific pass.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds stderr
back to the model as the reason. FAIL-OPEN on every parse or IO error: this is a guardrail, not a
security boundary, and a guard that traps the actor on its own malfunction gets switched off.

Severity: `BLOCK_SEVERITY = True` (exit 2). Flip to False for WARN-only. BLOCK is the right default
here and the argument is empirical, not stylistic: the WARN arm of the predecessor is precisely the
arm that fired during the week that was lost, and it changed nothing.

REGISTER. Each BLOCK and each authorized BYPASS appends a row to
`/home/grc/grc_working/guard-fires.tsv` when that file's directory is writable. Best-effort by
order; `log_fire()` returns False rather than raising so the block itself can never be lost to a
logging failure. Residue, stated because a dual-family review raised it against the earlier
register (finding E-7): the register currently has NO READER, and rotation is not implemented, so
it is an append-only trace for human calibration and nothing gates on it.

DOC COLLISION -- ORCHESTRATOR MUST RESOLVE IN THIS PR. Two live passages contradict this hook:
  1. `.claude/CLAUDE.md` "dual-family QA standard": "the Claude half as an in-session subagent".
     This hook blocks exactly that shape.
  2. `references/worker-offload.md`: the pre-push skeptical verifier and the high-assurance
     adversarial verifiers "stay orchestrator-side" and the offload guard's "override allowlist
     treats [them] as always-allowed".
Shipping this hook without amending both leaves the guard and the written rule disagreeing, which
is the condition under which a guard gets called broken and removed.

Self-test: `python3 block-orchestrator-self-qa.py --self-test`.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# BLOCK (exit 2) on an unauthorized offloadable dispatch. False downgrades to WARN-only (exit 0 +
# stderr). See the severity paragraph above before flipping this.
BLOCK_SEVERITY = True

# The subagent-dispatch tool names this hook targets. The settings.json matcher "Task|Agent" scopes
# it; this set is the belt-and-braces re-check inside the hook.
DISPATCH_TOOLS = {"Task", "Agent"}

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))

# Maintainer-created, once-only. Reachable from any shell: `touch <this path>`.
SENTINEL = WORKING_ROOT / ".allow-orchestrator-qa"

# Append-only fire register (no reader today; see the REGISTER note in the docstring).
FIRE_LOG = WORKING_ROOT / "guard-fires.tsv"

# QA-BLOCK TRIGGERS, verbatim from the PR1 order. Substring match against the lowered haystack,
# matching the sibling guards' convention. Ordered longest-context-first only for readability; the
# match is a plain scan and the FIRST hit is what the block message names.
QA_MARKERS = (
    "validate-pr",
    "/validate",
    "skeptical verif",          # covers verifier / verification / verify-pass phrasings
    "refute",
    "adversarial verif",
    "matrix-fit",
    "claim-fit",
    "reference-audit",
    "screen-publications",
    "full-qa",
    "deep-assessment",
    "fitness review",
    "hunt what the author missed",
    "verifier",
    "re-verify",
    "cross-family",
    "qa pass",
)


def _dispatch_text(payload: dict) -> str:
    """lower(prompt + description + subagent_type) of a Task / Agent dispatch. '' on any error."""
    try:
        ti = payload.get("tool_input") or payload.get("toolInput") or {}
        parts = [
            str(ti.get("prompt", "")),
            str(ti.get("description", "")),
            str(ti.get("subagent_type", "")),
        ]
        return "\n".join(p for p in parts if p).lower()
    except Exception:
        return ""


def _is_dispatch(payload: dict) -> bool:
    name = payload.get("tool_name") or payload.get("toolName") or ""
    return name in DISPATCH_TOOLS


def matched_marker(text: str):
    """The first QA marker present in the haystack, else None. Pure, so the self-test needs no IO."""
    if not isinstance(text, str) or not text.strip():
        return None
    low = text.lower()
    for m in QA_MARKERS:
        if m in low:
            return m
    return None


def log_fire(event: str, detail: str) -> bool:
    """Append one row to the fire register. Returns True on a written row, False on any failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>. Four columns, matching the rows already in
    the file. Column 2 carries the EVENT class (BLOCK / BYPASS-AUTHORIZED) rather than the `GR-4`
    tag those rows used: a dual-family review established that GR-4 already names an unrelated
    2026-07-02 guardrail item, so reusing it collides two record streams in one file.

    Returns a bool instead of swallowing, because the same review found a register whose write
    failures were invisible. The CALLER still ignores the result on the block path -- a logging
    failure must never cost a block -- but the self-test can assert the writer works.
    """
    try:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row = "\t".join([stamp, event, "block-orchestrator-self-qa",
                         " ".join(str(detail).split())]) + "\n"
        with FIRE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(row)
        return True
    except Exception:
        return False


def _block_message(marker: str) -> str:
    return (
        "BLOCKED (orchestrator self-QA guardrail): this Task/Agent dispatch matched the "
        "offloadable-QA marker " + repr(marker) + ".\n"
        "\n"
        "An in-session subagent is NOT an offload. It bills the ORCHESTRATOR's account, which is "
        "the scarce resource; self-running the QA cadence this way cost a full week of usage. "
        "There is no such thing as 'no worker available': a worker is SPAWNED ON DEMAND.\n"
        "\n"
        "  Exec-dispatch a worker instead:\n"
        "    python3 /home/grc/grc_library/tools/exec-dispatch.py --dispatch \\\n"
        "        --family {claude|codex} --model <model> --effort <low|medium|high|xhigh> \\\n"
        "        --account <account> --order-id <id> --prompt-file <path>\n"
        "  (the prompt file MUST live under the job directory named in the _private "
        "worker-accounts config `wrapper.job_dir`; --dry-run first to see the eligible accounts "
        "and the pick).\n"
        "\n"
        "  If this pass genuinely must run in-session, that is a MAINTAINER decision. Ask for it, "
        "and the maintainer authorizes it from a shell:\n"
        "    touch " + str(SENTINEL) + "     # honoured once, then deleted\n"
        "\n"
        "  Do NOT reword the prompt to dodge the marker. Rewording to evade a guard is the "
        "intent-vs-artefact failure this guard family exists to stop."
    )


def decide(payload: dict):
    """Pure-ish decision. Returns (action, message) with action in {'allow', 'block', 'bypass'}.

    Touches the filesystem only to test and consume the sentinel, and only after a marker matched.
    """
    if not _is_dispatch(payload):
        return "allow", ""
    marker = matched_marker(_dispatch_text(payload))
    if marker is None:
        return "allow", ""
    if SENTINEL.exists():
        try:
            SENTINEL.unlink()               # once-only: an authorization must not become standing
        except OSError:
            pass                            # already gone / unwritable: still honour it, once
        return "bypass", (
            "AUTHORIZED SELF-QA BYPASS CONSUMED: the dispatch matched " + repr(marker) + " and "
            "would normally be blocked, but the maintainer sentinel " + str(SENTINEL) + " was "
            "present. It has been DELETED, so the next such dispatch blocks again. Record why this "
            "pass ran in-session."
        )
    return "block", _block_message(marker)


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0                                    # fail-open on a malformed payload
    try:
        action, message = decide(payload)
    except Exception:
        return 0                                    # fail-open on any unexpected error
    if action == "bypass":
        log_fire("BYPASS-AUTHORIZED", message.splitlines()[0])
        print(message, file=sys.stderr)
        return 0
    if action == "block":
        log_fire("BLOCK", message.splitlines()[0])
        print(message, file=sys.stderr)
        return 2 if BLOCK_SEVERITY else 0
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    def dispatch(tool="Task", prompt="", desc="", subagent=""):
        return {"tool_name": tool,
                "tool_input": {"prompt": prompt, "description": desc,
                               "subagent_type": subagent}}

    class T(unittest.TestCase):
        def setUp(self):
            # Redirect the sentinel and the register into a throwaway root so the test never
            # touches the real working directory.
            global SENTINEL, FIRE_LOG
            self._root = Path(tempfile.mkdtemp())
            self._sent, self._log = SENTINEL, FIRE_LOG
            SENTINEL = self._root / ".allow-orchestrator-qa"
            FIRE_LOG = self._root / "guard-fires.tsv"

        def tearDown(self):
            global SENTINEL, FIRE_LOG
            SENTINEL, FIRE_LOG = self._sent, self._log

        # --- scope -------------------------------------------------------------------------
        def test_non_dispatch_tool_allowed(self):
            self.assertEqual(decide(dispatch(tool="Bash", prompt="/validate-pr"))[0], "allow")

        def test_unknown_tool_name_allowed(self):
            self.assertEqual(decide(dispatch(tool="Edit", prompt="refute this"))[0], "allow")

        def test_agent_tool_name_also_covered(self):
            self.assertEqual(decide(dispatch(tool="Agent", prompt="run /validate-pr"))[0], "block")

        # --- every marker in the order must actually fire -------------------------------------
        def test_every_marker_blocks(self):
            for m in QA_MARKERS:
                self.assertEqual(decide(dispatch(prompt="please " + m + " now"))[0], "block",
                                 "marker did not fire: " + m)

        def test_marker_reported_in_message(self):
            action, msg = decide(dispatch(prompt="do a full-qa sweep"))
            self.assertEqual(action, "block")
            self.assertIn("full-qa", msg)
            self.assertIn("exec-dispatch.py", msg)
            self.assertIn(str(SENTINEL), msg)

        # --- the registry hole the predecessor had must NOT exist here ------------------------
        def test_blocks_with_no_worker_registry_anywhere(self):
            # No scratch dir, no workers/, no list-workers: the predecessor allowed here.
            self.assertEqual(decide(dispatch(prompt="run the /validate-pr subagent"))[0], "block")

        # --- the predecessor's override markers are now TRIGGERS ------------------------------
        def test_pre_push_skeptical_verifier_now_blocks(self):
            self.assertEqual(
                decide(dispatch(prompt="pre-push skeptical verifier on this diff"))[0], "block")

        def test_high_assurance_adversarial_verification_now_blocks(self):
            self.assertEqual(
                decide(dispatch(prompt="high-assurance adversarial verification"))[0], "block")

        # --- fields other than prompt are read ------------------------------------------------
        def test_description_field_triggers(self):
            self.assertEqual(decide(dispatch(desc="QA pass on PR 1467"))[0], "block")

        def test_subagent_type_field_triggers(self):
            self.assertEqual(decide(dispatch(subagent="reference-audit"))[0], "block")

        def test_case_insensitive(self):
            self.assertEqual(decide(dispatch(prompt="Run /Validate-PR NOW"))[0], "block")

        # --- ordinary work is untouched --------------------------------------------------------
        def test_ordinary_dispatch_allowed(self):
            for p in ("author the CHANGELOG entry for this PR",
                      "draft a taxonomy section on incident response",
                      "summarise the open TODO items",
                      "search the corpus for control-family gaps"):
                self.assertEqual(decide(dispatch(prompt=p))[0], "allow", p)

        def test_empty_and_missing_input_allowed(self):
            self.assertEqual(decide(dispatch())[0], "allow")
            self.assertEqual(decide({"tool_name": "Task"})[0], "allow")
            self.assertEqual(decide({})[0], "allow")

        # --- sentinel semantics -----------------------------------------------------------------
        def test_sentinel_allows_and_is_consumed(self):
            SENTINEL.write_text("", encoding="utf-8")
            action, msg = decide(dispatch(prompt="run /validate-pr"))
            self.assertEqual(action, "bypass")
            self.assertIn("BYPASS CONSUMED", msg)
            self.assertFalse(SENTINEL.exists(), "sentinel must be deleted (once-only)")
            # and the very next identical dispatch blocks again
            self.assertEqual(decide(dispatch(prompt="run /validate-pr"))[0], "block")

        def test_sentinel_not_burned_by_unrelated_dispatch(self):
            SENTINEL.write_text("", encoding="utf-8")
            self.assertEqual(decide(dispatch(prompt="write the release notes"))[0], "allow")
            self.assertTrue(SENTINEL.exists(),
                            "an unrelated dispatch must not consume an authorization")

        def test_sentinel_unlink_failure_still_allows_once(self):
            SENTINEL.mkdir()               # a directory: unlink() raises, the hook must still allow
            self.assertEqual(decide(dispatch(prompt="refute this claim"))[0], "bypass")

        # --- register ----------------------------------------------------------------------------
        def test_log_fire_writes_a_four_column_row(self):
            self.assertTrue(log_fire("BLOCK", "reason  with   spaces\nand a newline"))
            row = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n")
            self.assertEqual(len(row.split("\t")), 4)
            self.assertNotIn("\n", row)
            self.assertIn("block-orchestrator-self-qa", row)

        def test_log_fire_returns_false_when_unwritable(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "no-such-dir" / "guard-fires.tsv"
            self.assertFalse(log_fire("BLOCK", "x"))

        def test_log_failure_never_costs_a_block(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "no-such-dir" / "guard-fires.tsv"
            self.assertEqual(decide(dispatch(prompt="/validate-pr"))[0], "block")

        # --- purity of the matcher ----------------------------------------------------------------
        def test_matched_marker_pure(self):
            self.assertEqual(matched_marker("run /validate-pr"), "validate-pr")
            self.assertIsNone(matched_marker("write the docs"))
            self.assertIsNone(matched_marker(""))
            self.assertIsNone(matched_marker(None))

        # --- known false-positive shapes, asserted so the residue is VISIBLE, not claimed away ----
        def test_known_false_positives_are_documented_behaviour(self):
            # Both of these BLOCK today. They are recorded here as the guard's accepted cost, and
            # a change in either direction should break this test and force a decision.
            self.assertEqual(decide(dispatch(prompt="quote: the guard said do not refute"))[0],
                             "block", "quote-blindness: the guard cannot tell mention from intent")
            self.assertEqual(decide(dispatch(prompt="check cross-family naming in the taxonomy"))[0],
                             "block", "'cross-family' is a broad substring")

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
