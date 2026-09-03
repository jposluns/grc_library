#!/usr/bin/env python3
"""Stop hook: in unattended mode, block a stop while the backlog tool shows actionable open work.

Rationale. This is the mechanical backstop for `10-TRUST-no-manufactured-winddown.md`: an unattended
orchestrator must not manufacture a stop while authorized work remains. It binds the stop decision to a
TOOL-VERIFIED enumeration (the backlog tool's actionable-item set) rather than to the orchestrator's own
narration ("high-priority is exhausted", "a long session"), which the rule forbids as a stop trigger.
It is DEFENCE IN DEPTH with the rule, NOT a security boundary.

Contract (Claude Code Stop hook). A Stop hook exits 0 to ALLOW the stop and exits 2 (with a stderr
message) to BLOCK it and feed the message back to the model. The stdin payload carries
`stop_hook_active` (bool): true when this stop is already the continuation of a prior Stop-hook block.
That field is the DOCUMENTED loop-guard, and this hook honours it: when it is true the hook ALLOWS the
stop, so it cannot loop indefinitely. Multiple Stop hooks run in parallel and any one blocking blocks
the stop, so this coexists with any other Stop hook a project registers.

What it does, in order (all other paths fail OPEN -> allow):
  0. Not the ORCHESTRATOR session (a dispatched worker, or an unconfirmable owner) -> allow. The guard
     binds the singleton orchestrator's wind-down; a bounded worker legitimately finishing its one task
     must not be told to work the orchestrator's backlog (and cannot switch the mode or mark the backlog).
  1. Not unattended (per the operating-mode record) -> allow.
  2. `stop_hook_active` true -> allow (already nudged this chain; the documented loop-guard).
  3. The backlog tool's actionable set (open items whose block is NOT a granted block) is empty, or
     indeterminate -> allow (tool-verified exhaustion, or a read failure -> fail open).
  4. otherwise -> BLOCK (exit 2), enumerating the actionable items and pointing at the rule.

Fail-OPEN. On ANY failure to determine the mode or the actionable set, the hook ALLOWS the stop. A
guard that traps the actor on its own malfunction protects nothing; a convenience guardrail that
wrongly blocks a legitimate stop is worse than the mistake it prevents.

PORTABILITY. Three adapter functions couple this hook to a project's tooling (fenced below as the
ADAPTER SEAM). GRC NOTE: this project ALSO customized main() (a one-shot-escape pre-step) below the
seam; see the GRC ADAPTATION note. The default implementations are a MINIMAL, dependency-free, file-based adapter. A project
with real backlog/mode tooling REPLACES the two adapter bodies with calls into its own tools (lab_infra's
`tools/flow.py` read_mode and `tools/pipeline.py` load_config+derive are the reference implementation,
deliberately NOT bundled). Everything below the seam is portable as-is; do not edit the pure `decide()`.

Self-test: `python3 stop-guard-unattended.py --self-test` (self-contained; no project tooling required).

GRC ADAPTATION (2026-09-03). Adopted from the lab_infra "No Manufactured Wind-Down" delivery
(inbox msg 20260903T002018Z.from-lab_infra), Architect-directed cross-project adoption. The delivered
decide()/run()/actionable_items/is_orchestrator_session/_parse_payload/self-test are byte-UNEDITED;
read_operating_mode carries a grc branch (session-state.md mode), main() carries a grc one-shot
declared-wait escape pre-step (.allow-idle-stop, via _grc_consume_escape), and the _grc_* helpers are
added; all gated on the grc repo root so --self-test (which never calls main()) stays hermetic. Actionable items come from the grc producer
.claude/hooks/nmw-actionable (-> tools/audit-backlog-actionability.py). Workers are detected by the
delivered ORCH_VERIFY_OWNER marker, which grc's orch-verify dispatcher exports. This hook REPLACES the
registration of the bespoke block-idle-stop-with-actionable-backlog.py (retained, de-registered).
Reconciles to the fleet-canonical form when the guardrails/AIQT pack ships it.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ============================================================================
# CONFIG (project-tunable constants; safe defaults)
# ============================================================================

# Cap the enumerated items in the block message (the rest are summarized as a count). Preserve this cap;
# an unbounded enumeration can flood the model's context.
_MAX_LISTED = 20

# The minimal file-based adapter reads the operating mode from a single-line file at this repo-relative
# path (one word: `unattended` or `attended`). A project wiring its own mode tool ignores this.
MODE_FILE = os.path.join(".working", "operating-mode")

# The minimal file-based adapter runs this OPTIONAL repo-relative executable to enumerate actionable
# items (stdout = one `id<TAB>title` per line). A project wiring its own backlog tool ignores this.
ACTIONABLE_PRODUCER = os.path.join(".claude", "hooks", "nmw-actionable")

# Seconds to allow the actionable producer to run before treating it as indeterminate (-> fail open).
# Keep below the Stop-hook timeout configured in settings.json (default 10s there).
PRODUCER_TIMEOUT_S = 8

# The block message's operator-stop hint. Generalize this to your project's mode-set command, e.g.
#   "run `python3 tools/flow.py mode set attended --by \"...\"`"
# so a genuine operator stop has a named, correct escape hatch.
MODE_SET_HINT = "set the operating mode to attended in your project's mode record (the operator-set escape hatch)"


def repo_root():
    """The repository this hook belongs to, from __file__ (not the payload): the hook lives at
    <root>/.claude/hooks/<name>, so parents[2] is the guarded project's root. The payload is NOT trusted
    to name the root, so it cannot redirect which project's mode/backlog is consulted."""
    return str(Path(__file__).resolve().parents[2])


# ---------------------------------------------------------------------------
# GRC ADAPTATION (project wiring; see the module docstring's GRC note). Only the
# read_operating_mode() adapter body and main() (a grc one-shot-escape pre-step) are customized;
# decide()/run() and the other two adapters are the delivered portable core, unedited. The grc code is
# gated on the grc repo root so the bundled --self-test stays hermetic on this host.
# ---------------------------------------------------------------------------
_GRC_REPO_ROOT = "/opt/grc/grc_library"
_GRC_STATE_FILE = "/opt/grc/private/session-state.md"
def _grc_escape_file():
    """Path of the grc one-shot declared-wait sentinel, resolved at call time (honours GRC_DROP_ROOT)."""
    return os.path.join(os.environ.get("GRC_DROP_ROOT") or "/opt/grc/grc_working", ".allow-idle-stop")


def _grc_consume_escape(root):
    """grc one-shot operator escape. If this is the grc repo AND the declared-wait sentinel exists,
    CONSUME it (unlink) and return True (allow this stop). A failed unlink returns False (REFUSE the
    escape, mirroring the retired hook). Non-grc-root, or absent sentinel, returns False. Called at the
    TOP of main() so the sentinel is consumed one-shot on EVERY orchestrator Stop invocation -- including
    the malformed-payload and worker/unconfirmable-owner fail-open paths that return before run() -- so a
    declared wait cannot survive to authorize a later, unintended stop (codex validate-pr #1945 f1;
    parity with the retired hook's test_block_idle_stop_fail_open_consumes_escape invariant)."""
    if os.path.realpath(root) != _GRC_REPO_ROOT:
        return False
    ef = _grc_escape_file()
    try:
        if os.path.isfile(ef):
            os.unlink(ef)
            return True
    except OSError:
        return False
    return False


def _grc_map_mode(raw):
    """Map a grc Operating-mode word to the portable arm-state. grc's no-idle-stop modes
    (attended-autonomous, and any mode containing 'unattended') map to 'unattended' (arm the guard);
    fully 'attended' maps to 'attended' (allow). This preserves the mode coverage of the retired
    block-idle-stop-with-actionable-backlog.py, which armed on attended-autonomous + the unattended
    modes and exempted fully-attended."""
    if raw is None:
        return None
    low = raw.strip().lower()
    if "unattended" in low:
        return "unattended"
    if low == "attended-autonomous":
        return "unattended"
    if low.startswith("attended"):
        return "attended"
    return raw.strip() or None


# ============================================================================
# ADAPTER SEAM -- ADAPT THIS PER PROJECT
# ----------------------------------------------------------------------------
# These THREE functions are the ONLY coupling between the portable decision core
# and a project's tooling. Each has a fixed contract; honour the contract and the
# core is unchanged. The defaults are a minimal, dependency-free, file-based adapter.
#
#   read_operating_mode(root) -> "unattended" | "attended" | <other-str> | None
#       The operating mode. None means INDETERMINATE (a read failure) -> fail open (allow the stop).
#       Any string other than "unattended" allows the stop. Only "unattended" arms the guard.
#
#   actionable_items(root)    -> list[(id, title)] | None
#       The tool-verified set of open backlog items that are NOT granted-blocked. None means
#       INDETERMINATE (a read failure) -> fail open (allow). An EMPTY list means genuine whole-set
#       exhaustion -> allow the stop. A non-empty list -> the guard blocks the stop.
#       The adapter MUST exclude items with a GRANTED (closed-set) blocker; a merely PROPOSED hold is
#       NOT granted and stays actionable (PROPOSED != GRANTED).
#
#   is_orchestrator_session(root) -> bool
#       True iff this is the singleton ORCHESTRATOR session; False for a dispatched worker or an
#       unconfirmable owner (-> allow). The default is generic (euid == repo-owner uid, and no worker
#       marker) and usually needs no change; adapt only the worker-marker env var if yours differs.
# ============================================================================

def read_operating_mode(root):
    """Return the operating mode: "unattended" arms the guard; any other string, or None
    (indeterminate), fails open (allows the stop).

    Two sources, in order:
      1. Portable default (UNCHANGED, serves the bundled --self-test and any file-based adopter):
         the repo-relative single-word file MODE_FILE. Present -> its trimmed word (or None).
      2. grc PRODUCTION adapter (only when root is the grc repo; hermetic for temp-root self-tests):
         read '**Operating-mode:**' from /opt/grc/private/session-state.md and map it via _grc_map_mode.
         (The one-shot declared-wait escape is consumed at the top of main() by _grc_consume_escape.)

    GRC WIRING NOTE: grc keeps the mode in session-state.md (not MODE_FILE) and declares a genuine wait
    with the .allow-idle-stop sentinel (the retired block-idle-stop hook's documented escape), both
    preserved here. A read failure at either source returns None (fail open)."""
    # 1. portable default branch (behaviour unchanged from the delivered core)
    path = os.path.join(root, MODE_FILE)
    try:
        with open(path, encoding="utf-8") as fh:
            val = fh.read().strip()
        return val or None
    except FileNotFoundError:
        pass  # no file-based mode record -> try the grc production source below
    except OSError:
        return None
    # 2. grc production adapter -- gated on the grc repo root so temp-root self-tests never reach it
    if os.path.realpath(root) != _GRC_REPO_ROOT:
        return None
    # grc mode source: session-state.md 'Operating-mode:' -> mapped arm-state. (The one-shot declared-wait
    # escape is handled at the top of main() via _grc_consume_escape, not here, so it is consumed on the
    # malformed/worker fail-open paths too.)
    try:
        with open(_GRC_STATE_FILE, encoding="utf-8") as fh:
            txt = fh.read()
    except OSError:
        return None
    m = re.search(r"(?im)^\*\*Operating-mode:\*\*\s*(.+?)\s*$", txt)
    if not m:
        return None
    return _grc_map_mode(m.group(1))

def actionable_items(root):
    """DEFAULT (minimal file-based) adapter. Run the OPTIONAL executable at ACTIONABLE_PRODUCER and parse
    its stdout as one `id<TAB>title` per line (blank lines and lines whose first non-space char is `#`
    are ignored). Returns [(id, title), ...], or None on absence, non-executable, timeout, or nonzero
    exit (all indeterminate -> fail open).

    Contract: an empty list is genuine exhaustion (allow the stop); a non-empty list blocks; None fails
    open. The producer is responsible for EXCLUDING granted-blocked items.

    REPLACE THIS BODY to read your project's backlog tool. lab_infra's reference implementation loads
    `tools/pipeline.py`, calls `load_config(root)` then `derive(cfg, root)`, and keeps every record whose
    `blocked` is not a dict with `kind == "granted"`, returning `[(rec["id"], rec["title"]), ...]`; it
    returns None on any load error or a tool `SystemExit`."""
    exe = os.path.join(root, ACTIONABLE_PRODUCER)
    if not (os.path.isfile(exe) and os.access(exe, os.X_OK)):
        return None  # no producer wired -> indeterminate -> fail open
    try:
        proc = subprocess.run(
            [exe], cwd=root, input="", capture_output=True, text=True, timeout=PRODUCER_TIMEOUT_S
        )
    except Exception:
        return None  # timeout / spawn failure -> indeterminate -> fail open
    if proc.returncode != 0:
        return None  # producer error -> indeterminate -> fail open
    out = []
    for line in proc.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = line.split("\t", 1)
        iid = parts[0].strip()
        title = parts[1].strip() if len(parts) > 1 else ""
        if iid:
            out.append((iid, title))
    return out


def _is_orchestrator(euid, owner_uid, has_verify_env):
    """Pure: True iff this is the ORCHESTRATOR session (fire the guard), False for a dispatched worker or
    an unconfirmable owner (allow). The orchestrator runs AS the repo-owning user; a dispatched worker
    runs as a different pooled-account uid even with repo read access, and the worker launcher exports a
    worker marker (ORCH_VERIFY_OWNER) into the worker shell. Fire ONLY on a positively-confirmed owner
    match with no worker marker; any uncertainty (unknown euid/owner) or worker signal -> allow."""
    if has_verify_env:
        return False
    if euid is None or owner_uid is None:
        return False
    return euid == owner_uid


def is_orchestrator_session(root):
    """DEFAULT (generic) adapter. Read the real euid, the repo-owner uid, and the worker-marker env var,
    and decide via _is_orchestrator. Any read failure leaves that input None -> fail open (allow).

    WORKER-MARKER ASSUMPTION: a dispatched worker's shell exports `ORCH_VERIFY_OWNER` (presence, not
    truthiness: even an empty string signals a worker). The orchestrator never sets it. If your fleet
    marks workers differently (a different env var, a marker file, a distinct uid range), adapt the
    marker check below to your worker launcher's convention."""
    try:
        euid = os.geteuid()
    except Exception:
        euid = None
    try:
        owner_uid = os.stat(root).st_uid
    except Exception:
        owner_uid = None
    return _is_orchestrator(euid, owner_uid, "ORCH_VERIFY_OWNER" in os.environ)

# ============================================================================
# END ADAPTER SEAM -- decide()/run() below are portable and unedited; do not edit decide(). (GRC:
# main() below carries a one-shot-escape pre-step; see the GRC ADAPTATION note.)
# ============================================================================


def decide(mode, stop_hook_active, actionable):
    """Pure decision. Returns (block: bool, reason: str). Block iff: unattended mode AND not already in a
    stop-hook continuation AND the actionable set is a non-empty list. `actionable` is a list (possibly
    empty) or None (indeterminate -> fail open)."""
    if mode != "unattended":
        return False, ""
    if stop_hook_active:
        return False, ""  # documented loop-guard: already blocked this chain -> allow (no infinite loop)
    if not isinstance(actionable, list) or not actionable:
        return False, ""  # None (indeterminate) or empty (exhausted) -> allow
    listed = actionable[:_MAX_LISTED]
    body = "\n".join("  - %s: %s" % (iid, title) for iid, title in listed)
    more = "" if len(actionable) <= _MAX_LISTED else "\n  ... and %d more" % (len(actionable) - _MAX_LISTED)
    reason = (
        "STOP BLOCKED (unattended): the backlog tool reports %d actionable open backlog item(s), so this "
        "is not whole-set exhaustion:\n%s%s\n\n"
        "Per 10-TRUST-no-manufactured-winddown, continue on the highest-priority actionable item. Session "
        "depth, run length, and work shape are NOT stop reasons, and a self-reported \"high-priority is "
        "exhausted\" is not exhaustion. If EVERY remaining item is genuinely granted-blocked or deferred to "
        "a RECORDED maintainer decision, record that first (a granted-blocked marker on the item, or a "
        "decision-register entry), which removes it from the actionable set, and then a stop is permitted. "
        "For a genuine operator stop, %s." % (len(actionable), body, more, MODE_SET_HINT)
    )
    return True, reason


def run(root, payload):
    """Core: exit 2 (block) iff this is the ORCHESTRATOR session, unattended, not a stop-hook
    continuation, and the backlog tool shows actionable work; else 0 (allow). All failure paths fail open."""
    if not is_orchestrator_session(root):
        return 0  # a dispatched worker (or an unconfirmable owner) -> allow; this guard binds the orchestrator only
    mode = read_operating_mode(root)
    stop_hook_active = bool(payload.get("stop_hook_active")) if isinstance(payload, dict) else False
    actionable = None
    if mode == "unattended" and not stop_hook_active:
        actionable = actionable_items(root)  # only compute when it can change the outcome
    block, reason = decide(mode, stop_hook_active, actionable)
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _parse_payload(raw):
    """Return a dict payload, or None if the stdin is absent / malformed / a JSON non-object (uncertain).
    None -> the caller fails OPEN, so an unreadable `stop_hook_active` never forces a block (a block on an
    unreadable payload would lean on the harness' consecutive-block cap instead of our own loop-guard)."""
    if not raw or not raw.strip():
        return None
    try:
        p = json.loads(raw)
    except Exception:
        return None
    return p if isinstance(p, dict) else None


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    if _grc_consume_escape(repo_root()):
        return 0  # grc one-shot declared-wait sentinel consumed -> allow this stop (before any parse)
    try:
        raw = sys.stdin.read()
    except Exception:
        raw = ""
    payload = _parse_payload(raw)
    if payload is None:
        return 0  # uncertain payload -> fail open (preserve the stop_hook_active loop-guard's reliability)
    return run(repo_root(), payload)


def _self_test():
    """Self-contained: exercises the pure decide() truth table plus the default file-based adapters
    against a temp project. Requires no project tooling."""
    import stat
    import tempfile
    import unittest

    _saved_vo = os.environ.pop("ORCH_VERIFY_OWNER", None)  # deterministic: tests control the worker marker

    def _write(path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def build(d, mode=None, producer_lines=None, producer_exit=0):
        """Create a temp project. mode -> MODE_FILE content; producer_lines (a str) -> a producer script
        that prints it and exits producer_exit; producer_lines None -> no producer wired."""
        if mode is not None:
            _write(os.path.join(d, MODE_FILE), mode + "\n")
        if producer_lines is not None:
            p = os.path.join(d, ACTIONABLE_PRODUCER)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            script = "#!/bin/sh\ncat <<'EOF'\n%s\nEOF\nexit %d\n" % (producer_lines, producer_exit)
            _write(p, script)
            os.chmod(p, os.stat(p).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    class T(unittest.TestCase):
        # ---- pure decision ----
        def test_decide_block_when_actionable(self):
            block, reason = decide("unattended", False, [("1", "a"), ("3", "c")])
            self.assertTrue(block)
            self.assertIn("actionable", reason)
            self.assertIn("1: a", reason)

        def test_decide_allow_stop_hook_active(self):
            self.assertFalse(decide("unattended", True, [("1", "a")])[0])

        def test_decide_allow_exhausted(self):
            self.assertFalse(decide("unattended", False, [])[0])

        def test_decide_allow_indeterminate(self):
            self.assertFalse(decide("unattended", False, None)[0])

        def test_decide_allow_attended(self):
            self.assertFalse(decide("attended", False, [("1", "a")])[0])

        def test_decide_cap(self):
            many = [("%d" % i, "t%d" % i) for i in range(_MAX_LISTED + 5)]
            _b, reason = decide("unattended", False, many)
            self.assertIn("... and 5 more", reason)

        # ---- default file-based mode adapter ----
        def test_mode_missing_is_none(self):
            with tempfile.TemporaryDirectory() as d:
                self.assertIsNone(read_operating_mode(d))

        def test_mode_unattended(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended")
                self.assertEqual(read_operating_mode(d), "unattended")

        def test_mode_attended(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="attended")
                self.assertEqual(read_operating_mode(d), "attended")

        # ---- default file-based actionable producer adapter ----
        def test_actionable_absent_producer_is_none(self):
            with tempfile.TemporaryDirectory() as d:
                self.assertIsNone(actionable_items(d))

        def test_actionable_parses_lines_ignoring_comments_and_blanks(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, producer_lines="# header\n\n1\tFirst item\n3\tThird item")
                self.assertEqual(actionable_items(d), [("1", "First item"), ("3", "Third item")])

        def test_actionable_empty_is_exhaustion(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, producer_lines="# nothing actionable")
                self.assertEqual(actionable_items(d), [])

        def test_actionable_nonzero_exit_is_none(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, producer_lines="1\tx", producer_exit=2)
                self.assertIsNone(actionable_items(d))

        # ---- run() end-to-end (owner session: temp dir owned by the test euid) ----
        def test_run_unattended_actionable_blocks(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended", producer_lines="1\tFirst\n2\tSecond")
                self.assertTrue(is_orchestrator_session(d))
                self.assertEqual(run(d, {"stop_hook_active": False}), 2)

        def test_run_unattended_exhausted_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended", producer_lines="# none")
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_run_unattended_no_producer_fails_open(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended")  # no producer -> None -> allow
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_run_stop_hook_active_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended", producer_lines="1\tFirst")
                self.assertEqual(run(d, {"stop_hook_active": True}), 0)

        def test_run_attended_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="attended", producer_lines="1\tFirst")
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_run_no_mode_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, producer_lines="1\tFirst")  # no mode file -> None -> allow
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        # ---- orchestrator-vs-worker scoping ----
        def test_is_orchestrator_truth_table(self):
            self.assertTrue(_is_orchestrator(1011, 1011, False))    # owner session, no marker -> fire
            self.assertFalse(_is_orchestrator(1011, 1011, True))    # worker marker set -> allow
            self.assertFalse(_is_orchestrator(2020, 1011, False))   # euid != owner -> allow
            self.assertFalse(_is_orchestrator(None, 1011, False))   # unknown euid -> fail open
            self.assertFalse(_is_orchestrator(1011, None, False))   # unknown owner -> fail open

        def test_worker_marker_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended", producer_lines="1\tFirst")
                try:
                    os.environ["ORCH_VERIFY_OWNER"] = "proj.1234"
                    self.assertFalse(is_orchestrator_session(d))
                    self.assertEqual(run(d, {"stop_hook_active": False}), 0)
                    os.environ["ORCH_VERIFY_OWNER"] = ""  # even empty means a worker exported it
                    self.assertFalse(is_orchestrator_session(d))
                    self.assertEqual(run(d, {"stop_hook_active": False}), 0)
                finally:
                    os.environ.pop("ORCH_VERIFY_OWNER", None)

        # ---- payload robustness ----
        def test_parse_payload(self):
            self.assertIsNone(_parse_payload(""))
            self.assertIsNone(_parse_payload("   "))
            self.assertIsNone(_parse_payload("{ not json"))
            self.assertIsNone(_parse_payload("[1, 2, 3]"))
            self.assertIsNone(_parse_payload('"a string"'))
            self.assertEqual(_parse_payload('{"stop_hook_active": true}'), {"stop_hook_active": True})

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    if _saved_vo is not None:
        os.environ["ORCH_VERIFY_OWNER"] = _saved_vo
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

