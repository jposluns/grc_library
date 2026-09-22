#!/usr/bin/env python3
"""PreToolUse hook: gate Task, Agent, Workflow, and SendMessage calls.

SCOPE. DISPATCH_TOOLS is the fixed set of tool names this hook checks; it does
not discover all reasoning-offload mechanisms or inspect whether a particular
call spawns or resumes an agent. A matching worker marker exempts these calls:
`_is_worker_session()` checks whether the lexical basename of the
caller-controlled CLAUDE_CONFIG_DIR starts with `orch-worker.`. This does not
establish broker provenance, actual session role, or the account billed.
Exempt calls leave the sentinel untouched and attempt a WORKER-ALLOWED log row.
Without that exemption, listed calls require successful sentinel consumption
to bypass the normal block decision. Keep the set and settings matcher aligned.

ACTIVE guardrail, wired on the `Task|Agent|Workflow|SendMessage` PreToolUse matcher in
`.claude/settings.json` by PR #1470.

WHY THIS EXISTS. The policy aims to conserve the orchestrator's scarce,
slow-to-renew account usage by routing reasoning work through external workers.
It treats Task, Agent, Workflow, and SendMessage as in-session dispatch tools.
Billing is a policy assumption here, not something this hook measures or
verifies. The motivating incident was a QA cadence reported to have consumed
a full week of orchestrator usage.

WHY IT DOES NOT LOOK AT THE WORKER REGISTRY, unlike its predecessor. The
retired `block-mandatory-offload.py` gated its block on
`count_live_workers() > 0`. That was a hole rather than a nuance: list-workers
read ZERO because the deprecated file-drop fleet registers none, so the guard
fell through to ALLOW in exactly the situation it was written for. Under the
orch-verify worker model, a worker is spawned on demand with
`orch-verify <family> <prompt-file>`. Therefore, no live worker is never a fact
about capability and never a licence to self-run. This hook makes no `list-workers` call and uses no worker-count or freshness
condition. A zero live-worker count therefore cannot itself authorize a call.

WHY PROMPT-INDEPENDENT. QA wording is not a reliable classification boundary:
prompts such as `/fitness`, `verify`, `validation sweep`, `screen publications`,
and `poke holes in this diff` need no special recognition here. The same
decision applies to every call whose tool name is in DISPATCH_TOOLS, whether
its fields describe QA, research, drafting, exploration, or nothing at all.
The decision uses the tool name, the lexical worker marker, and successful
sentinel consumption, subject to the error handling described below.
Calls named Bash or Read are outside this hook's set and return allow
regardless of their contents; this hook does not inspect commands inside them.

WHAT IT DOES, on the normal decision path:
  * Tool name outside DISPATCH_TOOLS -> ALLOW silently; no sentinel access.
  * Listed tool with a matching worker marker -> ALLOW without consuming the
    sentinel; attempt a WORKER-ALLOWED register row.
  * Listed tool without that exemption, successful sentinel consumption ->
    ALLOW this call and report the bypass.
  * Listed tool without that exemption or successful consumption -> BLOCK
    with exit 2 when BLOCK_SEVERITY is True; warn and exit 0 when it is False.
  Empty input and caught parse/decision errors also return 0 as described below.

AUTHORIZATION. The sentinel is an actor-creatable speed bump, not a
maintainer-only capability or a security boundary. Where filesystem
permissions permit, the actor can create it with:

    touch "${GRC_DROP_ROOT:-/opt/grc/grc_working}/.allow-orchestrator-qa"

The hook renames the sentinel to a PID-derived claim path, checks that path
with lstat for regular-file status, then unlinks it. It returns successful
consumption only if those operations succeed in that order. An OSError
during claim, lstat, or unlink, or an observed non-regular type, returns failed
consumption. The operations after rename remain subject to claim-path races.
Contents, ownership, actor, session, tool, prompt, and expiry are not checked.
Calls sharing the working root share this sentinel; it does not reserve a
bypass for a particular call. Successful consumption removes a directory
entry but leaves no durable filesystem receipt. A BYPASS-AUTHORIZED register
row is attempted separately and can fail.

REJECTION RESTORATION. After a claimed object fails validation or consumption,
`_restore()` attempts only a rename back to SENTINEL. It suppresses OSError
and performs no unlink or rmdir fallback. A successful rename can replace a
compatible object recreated at SENTINEL. A failed rename may leave residue
at the claim path; concurrent filesystem changes can alter that outcome.
Residue alone does not authorize a call, but can affect later claims that
reuse the same PID-derived name. See `_restore()`.

Exit protocol (Claude Code hooks): exit 0 permits the call to proceed past this
hook; exit 2 blocks it and supplies stderr as the reason. Tty input or
empty/whitespace-only stdin returns 0 without logging. Exceptions from JSON parsing or decide() that main() catches as Exception
return 0 after a best-effort FAIL-OPEN log attempt.
Sentinel OSError paths and an observed non-regular claim return failed
consumption, producing the normal block/warn decision when no worker
exemption applies. Other exceptions escaping sentinel processing are handled by the
decision fail-open handler only if they are instances of Exception. Module initialization, stdin reading, and stderr
printing are outside those handlers; this script does not explicitly convert
their failures into exit 0.

Severity: `BLOCK_SEVERITY = True` (exit 2). Flip to False for WARN-only. BLOCK
is the right default here and the argument is empirical, not stylistic: the WARN
arm of the predecessor is precisely the arm that fired during the week that was
lost, and it changed nothing.

REGISTER. main() attempts a row for BLOCK, BYPASS-AUTHORIZED, FAIL-OPEN,
WORKER-ALLOWED, and, when severity is disabled, WARN-ALLOWED, in
``${GRC_DROP_ROOT:-/opt/grc/grc_working}/guard-fires.tsv``.
Appending is best-effort: a writable directory alone does not guarantee
success. log_fire() returns False on Exception, and main() ignores that
result, so logging failure does not change the decision. This hook neither
creates the directory nor rotates the log, and production decisions do not
read it. Self-tests read it to check recorded events. The log is an attempted
audit trace, not a guaranteed durable receipt.

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

# The shared detector recognizes the lexical `orch-worker.` basename prefix
# in caller-controlled CLAUDE_CONFIG_DIR. This convention is intended to mark
# broker workers, but the check does not establish who set it, whether the
# path exists, which credentials are used, or which account fan-out bills.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _hookutil import is_worker_session as _is_worker_session
except Exception:                                  # pragma: no cover
    # Import failure disables only the worker-marker exemption. Listed tools
    # still take the sentinel path; successful consumption can bypass, and
    # exceptions escaping decide() are handled by main()'s fail-open handler
    # only if they are instances of Exception.
    def _is_worker_session() -> bool:              # noqa: D103
        return False

# BLOCK (exit 2) on an unauthorized in-session dispatch. False downgrades to
# WARN-only (exit 0 plus stderr). See the severity paragraph before changing it.
BLOCK_SEVERITY = True

# The settings matcher scopes the hook, and this set is the internal re-check.
DISPATCH_TOOLS = {"Task", "Agent", "Workflow", "SendMessage"}

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT") or "/opt/grc/grc_working")

# Actor-creatable where permissions permit; shared by calls using this root.
# Successful consumption permits the current call; a same-inode rename can leave SENTINEL present.
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
    """Attempt to rename a claimed object back to SENTINEL.

    Called after an lstat OSError, an observed non-regular type, or an unlink
    OSError. This function attempts only claim.rename(SENTINEL), suppresses
    OSError, and performs no unlink or rmdir fallback.

    Rename can replace a compatible destination recreated at SENTINEL, so
    restoration is not universally non-destructive. If rename fails, this
    function takes no further action; the claim may remain, subject to
    concurrent filesystem changes.

    Residue is named `..allow-orchestrator-qa.claim-<pid>`. Its presence alone
    grants no bypass, but it can affect later claims that reuse that name.
    This function does not clean up stranded claims.
    """
    try:
        claim.rename(SENTINEL)
    except OSError:
        pass


def _consume_sentinel() -> bool:
    """Atomically rename the sentinel, then check and unlink the claim path.

    The claim name is `..allow-orchestrator-qa.claim-<pid>` in SENTINEL's
    directory. Rename is atomic, but this function does not protect that
    predictable name against other writers. A compatible existing claim
    destination can be replaced by rename.

    Return True after rename succeeds, lstat reports a regular file, and
    unlink succeeds. These are separate path operations: no inode identity
    is retained or rechecked, so replacing the claim between lstat and unlink
    can change which object is removed.

    Return False on a claim OSError, an lstat OSError, an observed non-regular
    type, or an unlink OSError. After the latter three outcomes, attempt
    _restore(); it can overwrite a compatible destination or leave residue.
    Other exceptions can propagate to main()'s decision fail-open handler.

    With distinct process claim names, no pre-existing claim destination
    naming the sentinel's inode, no competing claim-path changes, and no
    recreation or restoration of the sentinel, one existing sentinel permits
    at most one successful claim and bypass. If source and destination name
    the same inode, rename can succeed without removing SENTINEL; unlinking
    the claim can then return True while leaving SENTINEL available again.
    A claim or consumption failure can yield no bypass. Recreating the
    sentinel permits further attempts; this is not a permanent one-call
    allowance per session.
    """
    claim = SENTINEL.with_name("." + SENTINEL.name + ".claim-" + str(os.getpid()))
    try:
        SENTINEL.rename(claim)              # atomic claim; fails if the sentinel is absent
    except OSError:
        return False
    try:
        regular = stat.S_ISREG(claim.lstat().st_mode)
    except OSError:
        _restore(claim)                     # lstat OSError: attempt restore, then return False
        return False
    if regular:
        try:
            claim.unlink()                  # unlink the current claim-path entry after the regular-file check
            return True
        except OSError:
            _restore(claim)                 # unlink OSError: attempt restore, then return False
            return False
    _restore(claim)                         # non-regular type observed: attempt restore, then return False
    return False


def log_fire(event: str, detail: str) -> bool:
    """Append one register row, returning True if written and False on failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>. The four-column shape
    matches existing rows. Column 2 carries the event class, one of BLOCK,
    BYPASS-AUTHORIZED, FAIL-OPEN, WORKER-ALLOWED, or WARN-ALLOWED (the last is what a
    `BLOCK_SEVERITY = False` flip records, because the register logs the OUTCOME
    rather than the intent). The caller ignores a False result,
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
        "GUARD DECISION (orchestrator-self-qa): this "
        "Task/Agent/Workflow/SendMessage call has no worker-marker exemption or "
        "successful sentinel consumption. It blocks when BLOCK_SEVERITY is True "
        "and warns while allowing when False. Dispatch fields: "
        + repr(_dispatch_summary(dispatch_text))
        + ".\n"
        "\n"
        "WHY: the policy aims to conserve orchestrator usage by routing reasoning "
        "work through external workers. This hook checks the fixed tool names "
        "Task, Agent, Workflow, and SendMessage without classifying their prompts. "
        "It does not verify billing, actual session role, or other offload mechanisms.\n"
        "\n"
        "CONSIDER-INSTEAD: dispatch a worker with orch-verify:\n"
        "    orch-verify {claude|codex|gemini} <prompt-file> [<workdir>] "
        "[--expensive] [--model <model>] [--effort <low|medium|high|xhigh|max>]\n"
        "  (for a skeptical verifier, pass the authoring account's label with "
        "--skip <account-label> to exclude that label from selection; orch-verify "
        "selects from the shared pool through orch-rank. This hook does not "
        "identify the authoring account or verify the exclusion).\n"
        "  (use orch-verify --pick <family> to preview account selection; this "
        "does not reserve an account. The prompt must be a readable regular file "
        "within orch-verify's size limit; no job-directory placement is required).\n"
        "\n"
        "  If this dispatch must run in-session, the actor can create a sentinel "
        "where filesystem permissions permit:\n"
        "    touch "
        + str(SENTINEL)
        + "     # successful rename/check/unlink permits the current call\n"
        "\n"
        "  Calls using the same working root share this speed bump. It does not "
        "reserve a bypass for this call or establish maintainer approval. The "
        "hook attempts rename, regular-file lstat, and unlink in sequence; an "
        "OSError or observed non-regular type grants no sentinel bypass. Other "
        "exceptions from decide() that main() catches as Exception return 0 "
        "after a best-effort FAIL-OPEN log attempt. The claim path "
        "remains subject to races, and audit logging is best-effort."
    )


def decide(payload: dict):
    """Return (action, message): allow, worker-allow, block, or bypass.

    A tool name outside DISPATCH_TOOLS returns allow before either exemption
    is checked. A listed tool with a matching lexical CLAUDE_CONFIG_DIR worker
    marker returns worker-allow without attempting sentinel consumption.
    The marker does not verify actual session role, provenance, or billing.

    Otherwise collect dispatch fields for messages and logging, then return
    bypass on successful sentinel consumption or block on failed consumption.
    Dispatch-field contents do not determine the action. Exceptions escaping
    this function are handled by main()'s fail-open path only if they are
    instances of Exception.
    """
    if not _is_dispatch(payload):
        return "allow", ""
    if _is_worker_session():
        # The lexical worker marker exempts this listed call without attempting
        # sentinel consumption. Actual worker provenance and billing are not
        # verified. main() attempts to log the worker-allow outcome.
        return "worker-allow", (
            "WORKER MARKER: dispatch allowed without consuming the sentinel. "
            "The lexical basename of caller-controlled CLAUDE_CONFIG_DIR starts "
            "with orch-worker.; broker provenance, path existence, actual session "
            "role, and the account billed are not verified."
        )
    dispatch_text = _dispatch_text(payload)
    if _consume_sentinel():
        return "bypass", (
            "AUTHORIZED IN-SESSION DISPATCH BYPASS CONSUMED: sentinel "
            + str(SENTINEL)
            + " had a successful rename operation to a claim path, lstat reported "
            "a regular file there, and unlink succeeded. A same-inode rename can "
            "leave the sentinel available again. This permits the current call; the claim path "
            "was not protected against concurrent replacement. A later "
            "Task/Agent/Workflow/SendMessage call blocks only if it has no worker "
            "marker or new successful sentinel consumption, reaches the normal "
            "block path, and BLOCK_SEVERITY remains True. Dispatch fields: "
            + repr(_dispatch_summary(dispatch_text))
            + ". Record why this pass ran in-session."
        )
    return "block", _block_message(dispatch_text)


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        # Tty input and empty/whitespace-only stdin return 0 without a decision
        # or register row. This branch does not establish why no payload arrived.
        return 0
    try:
        payload = json.loads(raw)
    except Exception:
        # A JSON parsing exception returns 0 after a best-effort FAIL-OPEN
        # log attempt. Logging failure can leave no trace; valid JSON with an
        # unsuitable shape is handled later if decide() raises.
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

        def test_claim_renames_sentinel_to_a_different_path_in_the_same_directory(self):
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

        def test_log_failure_never_changes_the_decision(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "missing" / "guard-fires.tsv"
            self.assertFalse(log_fire("BLOCK", "x"))
            self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        # --- worker-session scoping (GS-1, 2026-08-20) ---------------------------
        # These cases exercise the lexical worker-marker exemption. A matching
        # basename allows listed calls without verifying provenance or billing.
        # Negative-marker cases below expect block with the fixture's absent
        # sentinel. A detector miss alone does not disable sentinel bypass.

        def test_worker_session_dispatch_is_allowed(self):
            with mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "worker-allow")

        def test_worker_allow_does_not_consume_the_sentinel(self):
            # A marker-exempt call must leave the shared sentinel untouched so
            # another call can still attempt to consume it for a bypass.
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
            # A marker in a parent component alone does not match: the detector
            # checks only Path(config_dir).name, without verifying provenance.
            with mock.patch.dict(
                os.environ,
                {"CLAUDE_CONFIG_DIR": "/run/orch-worker.Ab3xZ9/orch-accounts/grc/acct"},
            ):
                self.assertEqual(decide(dispatch(prompt="research"))[0], "block")

        def test_lookalike_prefix_blocks(self):
            # "orch-workers-cache" has "s" where "orch-worker." requires ".".
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
