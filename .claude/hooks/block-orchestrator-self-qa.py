#!/usr/bin/env python3
"""PreToolUse hook: block in-session agent-spawning dispatch in ORCHESTRATOR sessions.

SCOPE. In a DISPATCHED WORKER session this hook is a no-op (see `_is_worker_session`): the
worker is already the offload and its fan-out bills the pooled worker account, so blocking it
only degrades a fan-out skill into a sequential one. In an ORCHESTRATOR session,
DISPATCH_TOOLS (and the settings.json matcher) cover every in-session tool that
spawns or resumes a reasoning agent billing the orchestrator account: Task, Agent,
Workflow (which fans out many subagents, up to the harness cap), and SendMessage (which
resumes one). The set below is the authoritative list; if the harness later adds another
agent-spawning tool, add it here and to the matcher.

ACTIVE guardrail, wired on the `Task|Agent|Workflow|SendMessage` PreToolUse matcher in
`.claude/settings.json` by PR #1470.

WHY THIS EXISTS. The orchestrator's own account is the scarce, slow-to-renew
resource. A subagent dispatched with any tool in the in-session agent-spawning
class (Task, Agent, Workflow, SendMessage) bills that account: an in-session
subagent is not an offload, it is the orchestrator spending itself twice.
Running the QA cadence that way cost a full week of orchestrator usage, which is
the specific failure this hook is built to prevent.

WHY IT DOES NOT LOOK AT THE WORKER REGISTRY, unlike its predecessor. The
retired `block-mandatory-offload.py` gated its block on
`count_live_workers() > 0`. That was a hole rather than a nuance: list-workers
read ZERO because the deprecated file-drop fleet registers none, so the guard
fell through to ALLOW in exactly the situation it was written for. Under the
orch-verify worker model, a worker is spawned on demand with
`orch-verify <family> <prompt-file>`. Therefore, no live worker is never a fact
about capability and never a licence to self-run. There is no `list-workers`
call, no freshness window, and nothing that can read zero and open the gate.

WHY UNCONDITIONAL. A marker scan is inherently leaky. Paraphrased QA evades it,
as do real examples such as `/fitness`, `verify`, `validation sweep`, `screen
publications`, and `poke holes in this diff`. The robust guard blocks the tool
class instead of trying to classify the prompt. Every Task, Agent, Workflow, or
SendMessage dispatch is blocked, whether it asks for QA, research, drafting, or
exploration. The inputs to the decision are the tool name, the SESSION IDENTITY (a dispatched
worker is exempt: it IS the offload, and its fan-out bills the pooled worker account, not the
orchestrator's), and the sentinel.
Deterministic Bash and Read calls remain allowed because they are not members of
the in-session agent-spawning tool class.

WHAT IT DOES.
  * A tool outside DISPATCH_TOOLS                     -> ALLOW silently (exit 0).
  * Task/Agent/Workflow/SendMessage, no consumable
    sentinel                                          -> BLOCK (exit 2).
  * Task/Agent/Workflow/SendMessage, sentinel
    consumed successfully                             -> ALLOW once, report the
                                                         authorized bypass.

AUTHORIZATION. The sentinel is a deliberate speed bump plus an audit record,
not a maintainer-only capability. The actor can create it with one shell call:

    touch /opt/grc/grc_working/.allow-orchestrator-qa

The hook honours only a regular-file sentinel that it successfully removes. A
directory, symlink, missing path, or removal failure does not authorize the
dispatch. A successful bypass leaves a filesystem trace through consumption of
the sentinel and appends a BYPASS-AUTHORIZED row to the register when possible.
The actor can create the sentinel, so this is a guardrail, not a security
boundary.

REJECTION IS NON-DESTRUCTIVE. When the guard refuses a claimed object it tries to
put it back, and that restore is a rename and nothing else. If the rename back
fails, the object is LEFT at its private claim path; the guard never unlinks and
never rmdirs it. A stranded claim file is cosmetic, not a bypass, because
authorization requires a successful claim of the sentinel path followed by a
successful consume. See `_restore()`.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it
and feeds stderr back to the model as the reason. Malformed stdin and unexpected
hook errors fail open so a broken hook does not trap the actor. Sentinel
validation and consumption failures are expected authorization failures and
therefore leave the block standing.

Severity: `BLOCK_SEVERITY = True` (exit 2). Flip to False for WARN-only. BLOCK
is the right default here and the argument is empirical, not stylistic: the WARN
arm of the predecessor is precisely the arm that fired during the week that was
lost, and it changed nothing.

REGISTER. Each BLOCK, each authorized BYPASS, and each FAIL-OPEN appends a row to
`/opt/grc/grc_working/guard-fires.tsv` when that file's directory is writable.
Best-effort by order, `log_fire()` returns False rather than raising so a
logging failure can never cost a block. The register currently has no reader,
and rotation is not implemented, so it is an append-only trace for human
calibration and nothing gates on it.

DOCUMENTATION RESOLUTION RECORD. In the same PR, the dual-family standard in
`.claude/CLAUDE.md` and the pre-push-verifier exception in
`references/worker-offload.md` were amended to use orch-verify workers. This
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

# The shared `orch` worker broker launches each dispatched Claude worker with
# CLAUDE_CONFIG_DIR pointed at an EPHEMERAL credential copy it creates as
# `mktemp -d "<tmpbase>/orch-worker.XXXXXX"`. The orchestrator's own value is a
# stable pooled-account path (`/opt/orch-accounts/<project>/<account>`), so the
# `orch-worker.` basename prefix is a positive marker set by the broker itself.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _hookutil import is_worker_session as _is_worker_session
except Exception:                                  # pragma: no cover
    # FAIL CLOSED: if the shared detector cannot be imported we cannot prove this is a
    # worker, so every dispatch keeps the orchestrator contract and blocks. Ignorance refuses.
    def _is_worker_session() -> bool:              # noqa: D103
        return False

# BLOCK (exit 2) on an unauthorized in-session dispatch. False downgrades to
# WARN-only (exit 0 plus stderr). See the severity paragraph before changing it.
BLOCK_SEVERITY = True

# The settings matcher scopes the hook, and this set is the internal re-check.
DISPATCH_TOOLS = {"Task", "Agent", "Workflow", "SendMessage"}

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/opt/grc/grc_working"))

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


def _restore(claim) -> None:
    """Move a claimed object back to the sentinel path: best-effort and NEVER destructive.

    Called when the claimed object is not a regular file, when its type could not be
    read, or when a regular file could not be consumed. The guard blocks and tries to
    leave the path as it found it, so a directory or symlink someone placed there is not
    destroyed by a probe.

    The ONLY action is `claim.rename(SENTINEL)`. If that raises OSError (a race
    recreated the sentinel at the path, or the directory is not writable), this function
    does NOTHING further. It never unlinks and it never rmdirs. Deleting the claimed
    object was the earlier behaviour and it could destroy the very directory or symlink
    the guard had just refused to honour, which is a worse outcome than any failure it
    was cleaning up after.

    The cost of the safe choice is a possible stranded `..allow-orchestrator-qa.claim-*`
    object in the working root. That is COSMETIC, not a bypass: authorization requires a
    successful claim of the SENTINEL path followed by a successful consume, and a
    stranded claim satisfies neither. Sweep such objects by hand if they accumulate.
    """
    try:
        claim.rename(SENTINEL)
    except OSError:
        pass


def _consume_sentinel() -> bool:
    """Atomically CLAIM the sentinel, then validate and consume the claimed object.

    The claim is a ``rename`` of the sentinel path to a private name in the same
    directory. Rename is atomic and moves the EXACT object that was at the path, so
    nothing can swap a symlink in between the type check and the removal (the TOCTOU a
    separate lstat-then-unlink would allow). Bypass is granted ONLY when the claimed
    object is a regular file and its removal succeeds.

    Every other outcome is a failed authorization and returns False: an absent sentinel
    or any other claim (rename) failure; a failure to read the claimed object's type
    (lstat); a claimed object that is not a regular file; and a removal failure on a
    regular file. In the last three cases the claim already happened, so `_restore()` is
    called to put the object back at the sentinel path. That restore is best-effort and
    NEVER destructive: if it fails the object stays at the private claim path rather
    than being deleted.

    Concurrent dispatches rename to distinct private names and only one rename of the
    single sentinel can succeed, so a race grants exactly one bypass.
    """
    claim = SENTINEL.with_name("." + SENTINEL.name + ".claim-" + str(os.getpid()))
    try:
        SENTINEL.rename(claim)              # atomic claim; fails if the sentinel is absent
    except OSError:
        return False
    try:
        regular = stat.S_ISREG(claim.lstat().st_mode)
    except OSError:
        _restore(claim)                     # type unreadable: restore + block (never orphan)
        return False
    if regular:
        try:
            claim.unlink()                  # consume the exact claimed regular file
            return True
        except OSError:
            _restore(claim)                 # could not consume: restore + block (no bypass)
            return False
    _restore(claim)                         # non-regular: restore intact + block
    return False


def log_fire(event: str, detail: str) -> bool:
    """Append one register row, returning True if written and False on failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>. The four-column shape
    matches existing rows. Column 2 carries the event class, one of BLOCK,
    BYPASS-AUTHORIZED, FAIL-OPEN, WORKER-ALLOWED, or WARN-ALLOWED (the last is what a
    `BLOCK_SEVERITY = False` flip records, because the register logs the OUTCOME
    rather than the intent). The caller ignores a False result on the block path,
    but the self-test can assert that the writer works.
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
        "BLOCKED (orchestrator dispatch guardrail): in an orchestrator session every in-session "
        "Task/Agent/Workflow/SendMessage dispatch is prohibited. Dispatch fields: "
        + repr(_dispatch_summary(dispatch_text))
        + ".\n"
        "\n"
        "An in-session subagent is not an offload. It bills the orchestrator's "
        "account, which is the scarce resource. The guard blocks the entire "
        "in-session agent-spawning tool class (Task, Agent, Workflow, SendMessage) because prompt "
        "classification is inherently leaky.\n"
        "\n"
        "  Dispatch a worker with orch-verify instead:\n"
        "    orch-verify {claude|codex|gemini} <prompt-file> [<workdir>] "
        "[--expensive] [--model <model>] [--effort <low|medium|high|xhigh|max>]\n"
        "  (for a skeptical verifier, add --skip <account-label> so the verifier "
        "never lands on the account that authored the work; orch-verify picks the "
        "account from the shared pool by orch-rank).\n"
        "  (use orch-verify --pick <family> to dry-run the account choice; the "
        "prompt file is any readable path, no job-directory requirement).\n"
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
    """Return (action, message), where action is allow, worker-allow, block, or bypass.

    The dispatch text is collected only for logging. It does not affect the
    decision. The decision uses the tool name, the session identity (a
    dispatched worker session is allowed unconditionally, without consuming
    the sentinel, per #1695), and successful sentinel consumption.
    """
    if not _is_dispatch(payload):
        return "allow", ""
    if _is_worker_session():
        # A dispatched worker IS the offload; its fan-out spends the elastic pooled
        # account, not the orchestrator's scarce one. Allowed without consuming the
        # sentinel, which is the orchestrator's one-shot authorization and must not be
        # burned by a worker. Logged so the register still shows the guard deciding.
        return "worker-allow", (
            "WORKER SESSION: dispatch allowed. CLAUDE_CONFIG_DIR names a broker "
            "ephemeral worker dir, so this process is a dispatched worker rather than "
            "the orchestrator; its subagent fan-out bills the pooled worker account."
        )
    dispatch_text = _dispatch_text(payload)
    if _consume_sentinel():
        return "bypass", (
            "AUTHORIZED IN-SESSION DISPATCH BYPASS CONSUMED: the regular-file "
            "sentinel "
            + str(SENTINEL)
            + " was removed successfully. The next Task/Agent/Workflow/SendMessage "
            "dispatch blocks again. Dispatch fields: "
            + repr(_dispatch_summary(dispatch_text))
            + ". Record why this pass ran in-session."
        )
    return "block", _block_message(dispatch_text)


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        # No dispatch payload arrived at all (a tty, or an empty pipe from a manual
        # invocation). Nothing was decided, so this is not a fail-open: writing a
        # FAIL-OPEN row here would pollute the human calibration record with noise.
        return 0
    try:
        payload = json.loads(raw)
    except Exception:
        # Fail open, but NOT silently: a payload-shape change must not degrade the
        # guard to allow-all with no trace (the register is the human calibration record).
        log_fire("FAIL-OPEN", "unparseable payload: " + raw[:200])
        return 0
    try:
        action, message = decide(payload)
    except Exception as exc:
        log_fire("FAIL-OPEN", type(exc).__name__ + ": " + raw[:200])
        return 0
    if action == "worker-allow":
        log_fire("WORKER-ALLOWED", message.splitlines()[0])
        return 0
    if action == "bypass":
        log_fire("BYPASS-AUTHORIZED", message.splitlines()[0])
        print(message, file=sys.stderr)
        return 0
    if action == "block":
        # The register must record the OUTCOME, not the intent: under a WARN-mode flip
        # (BLOCK_SEVERITY False) the dispatch is ALLOWED, so the row says so.
        log_fire("BLOCK" if BLOCK_SEVERITY else "WARN-ALLOWED", message.splitlines()[0])
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
            # HERMETIC ENVIRONMENT. Existing legacy cases assert the ORCHESTRATOR
            # contract, and `_is_worker_session()` reads ambient CLAUDE_CONFIG_DIR.
            # Pin a non-worker value so each case states its own precondition instead
            # of inheriting the session that happens to run the self-test.
            self._config_dir_patch = mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/test/orchestrator"}
            )
            self._config_dir_patch.start()

        def tearDown(self):
            global SENTINEL, FIRE_LOG
            self._config_dir_patch.stop()
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

        def test_workflow_blocks(self):
            self.assertEqual(
                decide(dispatch(tool="Workflow", prompt="fan out a review"))[0], "block"
            )

        def test_sendmessage_blocks(self):
            self.assertEqual(
                decide(dispatch(tool="SendMessage", prompt="resume the agent"))[0], "block"
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

        def test_block_message_names_the_whole_dispatch_tool_class(self):
            message = decide(dispatch(prompt="research"))[1]
            self.assertIn("Task/Agent/Workflow/SendMessage", message)
            for tool in sorted(DISPATCH_TOOLS):
                with self.subTest(tool=tool):
                    self.assertIn(tool, message)

        def test_block_message_gives_the_skip_operand(self):
            # orch-verify excludes an account with --skip <label>
            self.assertIn("--skip <account-label>", decide(dispatch(prompt="x"))[1])

        def test_bypass_message_names_the_whole_dispatch_tool_class(self):
            SENTINEL.write_text("", encoding="utf-8")
            action, message = decide(dispatch(prompt="research"))
            self.assertEqual(action, "bypass")
            self.assertIn("Task/Agent/Workflow/SendMessage", message)
            for tool in sorted(DISPATCH_TOOLS):
                with self.subTest(tool=tool):
                    self.assertIn(tool, message)

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

        def test_claim_is_a_rename_of_the_sentinel_to_a_private_path(self):
            # Discriminating: the retired lstat-then-unlink-the-SENTINEL design performed
            # NO rename at all, so it would fail on the first assertion below.
            SENTINEL.write_text("", encoding="utf-8")
            renames = []
            original_rename = Path.rename

            def recording_rename(source, target):
                renames.append((Path(source), Path(target)))
                return original_rename(source, target)

            with mock.patch.object(Path, "rename", recording_rename):
                self.assertTrue(_consume_sentinel())
            self.assertTrue(renames, "the sentinel must be claimed by rename")
            source, target = renames[0]
            self.assertEqual(source, SENTINEL)
            self.assertNotEqual(target, SENTINEL)
            self.assertEqual(target.parent, SENTINEL.parent)
            self.assertFalse(SENTINEL.exists())
            self.assertFalse(target.exists())

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

        def test_restore_failure_never_destroys_the_claimed_directory(self):
            # An EMPTY directory is the discriminating case: the retired destructive
            # `_restore` fell back to unlink and then rmdir, which would remove it.
            SENTINEL.mkdir()
            original_rename = Path.rename

            def rename_but_never_back(source, target):
                if Path(target) == SENTINEL:
                    raise PermissionError("simulated restore failure")
                return original_rename(source, target)

            with mock.patch.object(Path, "rename", rename_but_never_back):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")
            survivors = [
                path.name
                for path in self._root.iterdir()
                if path.is_dir() and not path.is_symlink()
            ]
            self.assertEqual(len(survivors), 1, "the claimed directory was destroyed")
            self.assertIn("allow-orchestrator-qa", survivors[0])

        def test_claim_lstat_failure_restores_and_blocks(self):
            SENTINEL.write_text("payload", encoding="utf-8")
            with mock.patch.object(
                Path, "lstat", side_effect=PermissionError("simulated failure")
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")
            self.assertTrue(SENTINEL.is_file())
            self.assertEqual(SENTINEL.read_text(encoding="utf-8"), "payload")

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
            self.assertIn("FAIL-OPEN", FIRE_LOG.read_text(encoding="utf-8"))

        def test_empty_stdin_writes_no_register_row(self):
            for raw in ("", "\n", "   \n\t "):
                with self.subTest(raw=repr(raw)):
                    with mock.patch.object(sys, "stdin", io.StringIO(raw)):
                        self.assertEqual(main(["block-orchestrator-self-qa.py"]), 0)
                    self.assertFalse(FIRE_LOG.exists())

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

        # --- worker-session scoping (GS-1, 2026-08-20) ---------------------------
        # The guard protects the ORCHESTRATOR's scarce account. A dispatched worker is
        # already the offload, so its fan-out must not be blocked. Detection is a
        # POSITIVE match on the broker's ephemeral config dir; every other state must
        # keep blocking, so most of these tests are the fail-closed negatives.

        def test_worker_session_dispatch_is_allowed(self):
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "worker-allow")

        def test_worker_allow_does_not_consume_the_sentinel(self):
            # The sentinel is the ORCHESTRATOR's one-shot authorization. A worker must
            # never burn it, or an unrelated orchestrator dispatch later loses its bypass.
            SENTINEL.write_text("", encoding="utf-8")
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "worker-allow")
            self.assertTrue(SENTINEL.is_file(), "worker-allow consumed the sentinel")

        def test_orchestrator_pooled_account_dir_still_blocks(self):
            with mock.patch.dict(
                os.environ,
                {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/grc/claude-team-pro-jposluns-work"},
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_unset_config_dir_blocks(self):
            env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
            with mock.patch.dict(os.environ, env, clear=True):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_empty_config_dir_blocks(self):
            with mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": ""}):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_marker_must_be_the_basename_not_a_parent(self):
            # A PARENT directory named orch-worker.* must not qualify the session: the
            # broker sets the ephemeral dir itself, so only the basename is authoritative.
            with mock.patch.dict(
                os.environ,
                {"CLAUDE_CONFIG_DIR": "/run/orch-worker.Ab3xZ9/orch-accounts/grc/acct"},
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_lookalike_prefix_blocks(self):
            # "orch-workers-cache" shares a prefix up to the dot; the dot is load-bearing.
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-workers-cache"}
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_non_dispatch_early_return_precedes_the_worker_check(self):
            # NOT a test of the worker detector: `decide()` returns "allow" for a non-dispatch
            # tool BEFORE it consults `_is_worker_session()`, so this case would pass against a
            # broken detector. What it DOES pin is the ORDERING, that the worker branch did not
            # displace the early return and a non-dispatch tool is never reported "worker-allow".
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ):
                self.assertEqual(decide(dispatch(tool="Bash", prompt="verify"))[0], "allow")

        def test_worker_allow_never_calls_consume_sentinel(self):
            # Stronger than checking the sentinel still exists afterwards: this proves the
            # consume was never ATTEMPTED, so no transient claim/restore race can occur.
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ), mock.patch(
                "__main__._consume_sentinel", side_effect=AssertionError("must not be called")
            ) as consume:
                self.assertEqual(decide(dispatch(prompt="research"))[0], "worker-allow")
            consume.assert_not_called()

        def test_main_worker_allow_exits_zero_and_logs_the_event(self):
            payload = json.dumps(dispatch(prompt="research"))
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ), mock.patch.object(sys, "stdin", io.StringIO(payload)):
                self.assertEqual(main(["block-orchestrator-self-qa.py"]), 0)
            self.assertIn("WORKER-ALLOWED", FIRE_LOG.read_text(encoding="utf-8"))

        def test_marker_is_lexical_and_does_not_stat_the_path(self):
            # PINS THE DOCUMENTED WEAKNESS rather than a wish. The check never stats, so a
            # nonexistent or unreadable path bearing the prefix IS accepted. If a future
            # change makes the check filesystem-aware, this test should fail deliberately.
            for path in (
                "/definitely/missing/orch-worker.fake",
                "/root/orch-worker.fake",
                "/run/orch/orch-worker.",          # no mktemp suffix
            ):
                with self.subTest(path=path), mock.patch.dict(
                    os.environ, {"CLAUDE_CONFIG_DIR": path}
                ):
                    self.assertEqual(decide(dispatch(prompt="research"))[0], "worker-allow")

        def test_environment_read_failure_falls_closed(self):
            with mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3"}):
                with mock.patch("os.environ.get", side_effect=RuntimeError("simulated")):
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
