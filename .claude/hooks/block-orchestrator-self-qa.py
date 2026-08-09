#!/usr/bin/env python3
"""PreToolUse hook (Task / Agent): block every in-session reasoning dispatch.

ACTIVE guardrail, wired on the Task|Agent PreToolUse matcher in
`.claude/settings.json` by PR #1470.

WHY THIS EXISTS. The orchestrator's own account is the scarce, slow-to-renew
resource. A subagent dispatched with the Task / Agent tool bills that account:
an in-session subagent is not an offload, it is the orchestrator spending itself
twice. Running the QA cadence that way cost a full week of orchestrator usage,
which is the specific failure this hook is built to prevent.

WHY IT DOES NOT LOOK AT THE WORKER REGISTRY, unlike its predecessor. The
retired `block-mandatory-offload.py` gated its block on
`count_live_workers() > 0`. That was a hole rather than a nuance: list-workers
read ZERO because the deprecated file-drop fleet registers none, so the guard
fell through to ALLOW in exactly the situation it was written for. Under the
exec'd-worker model, a worker is spawned on demand with
`tools/exec-dispatch.py --dispatch`. Therefore, no live worker is never a fact
about capability and never a licence to self-run. There is no `list-workers`
call, no freshness window, and nothing that can read zero and open the gate.

WHY UNCONDITIONAL. A marker scan is inherently leaky. Paraphrased QA evades it,
as do real examples such as `/fitness`, `verify`, `validation sweep`, `screen
publications`, and `poke holes in this diff`. The robust guard blocks the tool
class instead of trying to classify the prompt. Every Task or Agent dispatch is
blocked, whether it asks for QA, research, drafting, or exploration. The only
inputs to the decision are the tool name and the sentinel. Deterministic Bash
and Read calls remain allowed because they are not Task or Agent calls.

WHAT IT DOES.
  * A tool other than Task or Agent                 -> ALLOW silently (exit 0).
  * Task or Agent, no consumable sentinel           -> BLOCK (exit 2).
  * Task or Agent, sentinel consumed successfully   -> ALLOW once, report the
                                                       authorized bypass.

AUTHORIZATION. The sentinel is a deliberate speed bump plus an audit record,
not a maintainer-only capability. The actor can create it with one shell call:

    touch /home/grc/grc_working/.allow-orchestrator-qa

The hook honours only a regular-file sentinel that it successfully removes. A
directory, symlink, missing path, or removal failure does not authorize the
dispatch. A successful bypass leaves a filesystem trace through consumption of
the sentinel and appends a BYPASS-AUTHORIZED row to the register when possible.
The actor can create the sentinel, so this is a guardrail, not a security
boundary.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it
and feeds stderr back to the model as the reason. Malformed stdin and unexpected
hook errors fail open so a broken hook does not trap the actor. Sentinel
validation and consumption failures are expected authorization failures and
therefore leave the block standing.

Severity: `BLOCK_SEVERITY = True` (exit 2). Flip to False for WARN-only. BLOCK
is the right default here and the argument is empirical, not stylistic: the WARN
arm of the predecessor is precisely the arm that fired during the week that was
lost, and it changed nothing.

REGISTER. Each BLOCK and each authorized BYPASS appends a row to
`/home/grc/grc_working/guard-fires.tsv` when that file's directory is writable.
Best-effort by order, `log_fire()` returns False rather than raising so a
logging failure can never cost a block. The register currently has no reader,
and rotation is not implemented, so it is an append-only trace for human
calibration and nothing gates on it.

DOCUMENTATION RESOLUTION RECORD. In the same PR, the dual-family standard in
`.claude/CLAUDE.md` and the pre-push-verifier exception in
`references/worker-offload.md` were amended to use exec-dispatch workers. This
resolved the earlier conflict between those documents and the guard.

Self-test: `python3 block-orchestrator-self-qa.py --self-test`.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

# BLOCK (exit 2) on an unauthorized in-session dispatch. False downgrades to
# WARN-only (exit 0 plus stderr). See the severity paragraph before changing it.
BLOCK_SEVERITY = True

# The settings matcher scopes the hook, and this set is the internal re-check.
DISPATCH_TOOLS = {"Task", "Agent"}

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))

# Actor-created and once-only. Reachable from any shell with `touch <path>`.
SENTINEL = WORKING_ROOT / ".allow-orchestrator-qa"

# Append-only fire register. See the REGISTER note in the docstring.
FIRE_LOG = WORKING_ROOT / "guard-fires.tsv"


def _dispatch_text(payload: dict) -> str:
    """Return lower(prompt + description + subagent_type), or '' on an error."""
    try:
        ti = payload.get("tool_input") or payload.get("toolInput") or {}
        parts = [
            str(ti.get("prompt", "")),
            str(ti.get("description", "")),
            str(ti.get("subagent_type", "")),
        ]
        return "\n".join(part for part in parts if part).lower()
    except Exception:
        return ""


def _is_dispatch(payload: dict) -> bool:
    name = payload.get("tool_name") or payload.get("toolName") or ""
    return name in DISPATCH_TOOLS


def _consume_sentinel() -> bool:
    """Remove a regular-file sentinel once, returning True only on success.

    `lstat()` rejects symlinks as well as non-regular paths. `unlink()` is the
    atomic consumption step. Absence, inspection failure, or removal failure is
    failed authorization and returns False.
    """
    try:
        sentinel_stat = SENTINEL.lstat()
    except OSError:
        return False
    if not stat.S_ISREG(sentinel_stat.st_mode):
        return False
    try:
        SENTINEL.unlink()
    except OSError:
        return False
    return True


def log_fire(event: str, detail: str) -> bool:
    """Append one register row, returning True if written and False on failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>. The four-column shape
    matches existing rows. Column 2 carries the event class, BLOCK or
    BYPASS-AUTHORIZED. The caller ignores a False result on the block path, but
    the self-test can assert that the writer works.
    """
    try:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row = "\t".join(
            [
                stamp,
                event,
                "block-orchestrator-self-qa",
                " ".join(str(detail).split()),
            ]
        ) + "\n"
        with FIRE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(row)
        return True
    except Exception:
        return False


def _dispatch_summary(text: str) -> str:
    """Return a bounded one-line rendering of dispatch fields for the register."""
    compact = " ".join(text.split())
    return compact[:500] if compact else "<empty dispatch fields>"


def _block_message(dispatch_text: str) -> str:
    return (
        "BLOCKED (orchestrator dispatch guardrail): every in-session Task/Agent "
        "dispatch is prohibited. Dispatch fields: "
        + repr(_dispatch_summary(dispatch_text))
        + ".\n"
        "\n"
        "An in-session subagent is not an offload. It bills the orchestrator's "
        "account, which is the scarce resource. The guard blocks the entire "
        "Task/Agent tool class because prompt classification is inherently leaky.\n"
        "\n"
        "  Exec-dispatch a worker instead:\n"
        "    python3 /home/grc/grc_library/tools/exec-dispatch.py --dispatch \\\n"
        "        --family {claude|codex} --model <model> "
        "--effort <low|medium|high|xhigh> \\\n"
        "        --account <account> --order-id <id> --prompt-file <path>\n"
        "  (the prompt file must live under the job directory named in the "
        "_private worker-accounts config `wrapper.job_dir`; use --dry-run first "
        "to see eligible accounts and the pick).\n"
        "\n"
        "  If this dispatch genuinely must run in-session, that is a deliberate "
        "authorization. The actor can create the once-only sentinel from a shell:\n"
        "    touch "
        + str(SENTINEL)
        + "     # honoured once, then deleted\n"
        "\n"
        "  The sentinel is a speed bump and audit record. It is not a security "
        "boundary. A failed deletion does not authorize the dispatch."
    )


def decide(payload: dict):
    """Return (action, message), where action is allow, block, or bypass.

    The dispatch text is collected only for logging. It does not affect the
    decision. The decision uses only the tool name and successful sentinel
    consumption.
    """
    if not _is_dispatch(payload):
        return "allow", ""
    dispatch_text = _dispatch_text(payload)
    if _consume_sentinel():
        return "bypass", (
            "AUTHORIZED IN-SESSION DISPATCH BYPASS CONSUMED: the regular-file "
            "sentinel "
            + str(SENTINEL)
            + " was removed successfully. The next Task/Agent dispatch blocks "
            "again. Dispatch fields: "
            + repr(_dispatch_summary(dispatch_text))
            + ". Record why this pass ran in-session."
        )
    return "block", _block_message(dispatch_text)


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        action, message = decide(payload)
    except Exception:
        return 0
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
    import io
    import tempfile
    import unittest
    from unittest import mock

    def dispatch(tool="Task", prompt="", desc="", subagent=""):
        return {
            "tool_name": tool,
            "tool_input": {
                "prompt": prompt,
                "description": desc,
                "subagent_type": subagent,
            },
        }

    class T(unittest.TestCase):
        def setUp(self):
            global SENTINEL, FIRE_LOG
            self._temporary_root = tempfile.TemporaryDirectory()
            self._root = Path(self._temporary_root.name)
            self._sentinel, self._fire_log = SENTINEL, FIRE_LOG
            SENTINEL = self._root / ".allow-orchestrator-qa"
            FIRE_LOG = self._root / "guard-fires.tsv"

        def tearDown(self):
            global SENTINEL, FIRE_LOG
            SENTINEL, FIRE_LOG = self._sentinel, self._fire_log
            self._temporary_root.cleanup()

        def test_bash_allowed(self):
            self.assertEqual(decide(dispatch(tool="Bash"))[0], "allow")

        def test_read_allowed(self):
            self.assertEqual(decide(dispatch(tool="Read"))[0], "allow")

        def test_non_dispatch_allowed(self):
            self.assertEqual(decide(dispatch(tool="Edit"))[0], "allow")

        def test_task_blocks(self):
            self.assertEqual(decide(dispatch(prompt="do anything"))[0], "block")

        def test_agent_blocks(self):
            self.assertEqual(
                decide(dispatch(tool="Agent", prompt="do anything"))[0], "block"
            )

        def test_research_and_drafting_dispatches_block(self):
            prompts = (
                "research incident response standards",
                "draft the release note",
                "explore the repository structure",
                "summarize the current control taxonomy",
            )
            for prompt in prompts:
                with self.subTest(prompt=prompt):
                    self.assertEqual(decide(dispatch(prompt=prompt))[0], "block")

        def test_empty_task_dispatch_blocks(self):
            self.assertEqual(decide(dispatch())[0], "block")
            self.assertEqual(decide({"tool_name": "Task"})[0], "block")

        def test_dispatch_fields_are_read_for_logging(self):
            action, message = decide(
                dispatch(prompt="PROMPT", desc="DESCRIPTION", subagent="SPECIALIST")
            )
            self.assertEqual(action, "block")
            self.assertIn("prompt description specialist", message)

        def test_regular_file_sentinel_bypasses_and_is_consumed(self):
            SENTINEL.write_text("", encoding="utf-8")
            action, message = decide(dispatch(prompt="research"))
            self.assertEqual(action, "bypass")
            self.assertIn("BYPASS CONSUMED", message)
            self.assertFalse(SENTINEL.exists())

        def test_second_dispatch_after_consumption_blocks(self):
            SENTINEL.write_text("", encoding="utf-8")
            self.assertEqual(decide(dispatch(prompt="first"))[0], "bypass")
            self.assertEqual(decide(dispatch(prompt="second"))[0], "block")

        def test_directory_at_sentinel_path_blocks(self):
            SENTINEL.mkdir()
            self.assertEqual(decide(dispatch(prompt="research"))[0], "block")
            self.assertTrue(SENTINEL.is_dir())

        def test_symlink_at_sentinel_path_blocks(self):
            target = self._root / "regular-target"
            target.write_text("", encoding="utf-8")
            SENTINEL.symlink_to(target)
            self.assertEqual(decide(dispatch(prompt="research"))[0], "block")
            self.assertTrue(SENTINEL.is_symlink())

        def test_unlink_failure_blocks(self):
            SENTINEL.write_text("", encoding="utf-8")
            with mock.patch.object(
                Path, "unlink", side_effect=PermissionError("simulated failure")
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")
            self.assertTrue(SENTINEL.exists())

        def test_malformed_payload_fails_open(self):
            with mock.patch.object(sys, "stdin", io.StringIO("{")):
                self.assertEqual(main(["block-orchestrator-self-qa.py"]), 0)

        def test_log_fire_writes_four_columns(self):
            self.assertTrue(log_fire("BLOCK", "reason  with spaces\nand newline"))
            row = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n")
            self.assertEqual(len(row.split("\t")), 4)
            self.assertNotIn("\n", row)
            self.assertIn("block-orchestrator-self-qa", row)

        def test_log_failure_never_costs_block(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "missing" / "guard-fires.tsv"
            self.assertFalse(log_fire("BLOCK", "x"))
            self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_documented_block_all_contract(self):
            examples = (
                "/fitness",
                "verify",
                "validation sweep",
                "screen publications",
                "poke holes in this diff",
                "write a friendly greeting",
            )
            for prompt in examples:
                with self.subTest(prompt=prompt):
                    self.assertEqual(decide(dispatch(prompt=prompt))[0], "block")
            self.assertEqual(decide(dispatch(tool="Bash", prompt="verify"))[0], "allow")

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
