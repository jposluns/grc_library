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
  1. The resolved operating mode is not `unattended` -> allow; only a resolved `unattended` arms the guard.
     Via the grc adapter (`_grc_map_mode`), the WHOLE leading mode token decides (3b101): `unattended`,
     `overnight-unattended`, `daytime-unattended` or `attended-autonomous` resolves to `unattended` and ARMS; commentary after it
     is ignored, and EVERY other value (plain `attended`, `fully-attended`,
     `attended-manual`, an unknown string, an absent or unreadable mode) resolves to non-`unattended` and
     allows. The portable MODE_FILE branch returns its text unmapped, so there only a literal `unattended`
     arms (even `attended-autonomous` from that source allows).
  2. `stop_hook_active` true -> allow (already nudged this chain; the documented loop-guard).
  3. The backlog tool's actionable set (open items whose block is NOT a granted block) is empty, or
     indeterminate -> allow (tool-verified exhaustion, or a read failure -> fail open).
  4. otherwise -> BLOCK (exit 2), enumerating the actionable items and pointing at the rule.

Fail-OPEN. On ANY failure to determine the mode or the actionable set, the hook ALLOWS the stop. A
guard that traps the actor on its own malfunction protects nothing; a convenience guardrail that
wrongly blocks a legitimate stop is worse than the mistake it prevents.

PORTABILITY. Three adapter functions couple this hook to a project's tooling (fenced below as the
ADAPTER SEAM). GRC NOTE: this project ALSO customized main() (a one-shot-escape pre-step) and
MODE_SET_HINT (which names the escape file's path) below the
seam; see the GRC ADAPTATION note. The default implementations are a MINIMAL, dependency-free, file-based adapter. A project
with real backlog/mode tooling REPLACES the two adapter bodies with calls into its own tools (lab_infra's
`tools/flow.py` read_mode and `tools/pipeline.py` load_config+derive are the reference implementation,
deliberately NOT bundled). Everything below the seam is portable as-is; do not edit the pure `decide()`.
Exceptions (emitted message text only; predicates/decisions/exit unchanged): P-1.36, #2291, #2496.

Self-test: `python3 stop-guard-unattended.py --self-test` (self-contained; no project tooling required).

GRC ADAPTATION (2026-09-03). Adopted from the lab_infra "No Manufactured Wind-Down" delivery
(inbox msg 20260903T002018Z.from-lab_infra), Architect-directed cross-project adoption. The delivered
decide()/run()/actionable_items/is_orchestrator_session/_parse_payload/self-test keep the vendored
LOGIC unchanged (predicates, decisions, exit codes), but the file is NOT byte-identical to the vendored
source: emitted message text carries grc adaptations (P-1.36; the #2291 terse backlog count; the
#2496 escape-path hint).
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
# grc adaptation (2026-09-24, mistakes report item B): the hint also NAMES the declared-wait escape
# path (resolved like _grc_escape_file, honouring GRC_DROP_ROOT), because the sentinel was once created
# at the WRONG path for a whole session when the message did not say where it is read from. Carried in
# the single refusal message (the blocking-hook message contract allows no trailing extra line).
# Same fully resolved path as repo_root(), so a symlinked hook file cannot split the two (3b101 QA r1).
_GRC_REPO_ROOT = str(Path(__file__).resolve().parents[2])
_GRC_PARENT = os.path.dirname(_GRC_REPO_ROOT)


def _grc_under_root(value, default):
    """An override path, resolved against the repo root when relative so the working directory cannot
    change its meaning; the default when unset or empty (3b101 QA r1)."""
    if not value:
        return default
    return value if os.path.isabs(value) else os.path.normpath(os.path.join(_GRC_REPO_ROOT, value))


_GRC_STATE_FILE = os.path.join(_grc_under_root(os.environ.get("GRC_STORE"), os.path.join(_GRC_PARENT, "private")),
                               "session-state.md")


def _grc_escape_file():
    """Path of the grc one-shot declared-wait sentinel, resolved at call time (honours GRC_DROP_ROOT)."""
    return os.path.join(_grc_under_root(os.environ.get("GRC_DROP_ROOT"), os.path.join(_GRC_PARENT, "grc_working")),
                        ".allow-idle-stop")


def _is_grc_main_checkout(root):
    """The grc adapter applies only in the MAIN checkout: <root>/.git is a directory there and a file in
    every linked worktree, so a worker's Stop in a sibling worktree can neither consume the orchestrator's
    declared-wait sentinel nor be armed by its lease. The old hard-coded root path gave this scoping;
    deriving the root from __file__ alone made the check always true (3b101 QA r1, claude F1)."""
    return os.path.realpath(root) == _GRC_REPO_ROOT and _is_primary_checkout(root)


def _is_primary_checkout(root):
    """True for a main checkout (.git is a directory) or a submodule (.git is a file naming an admin
    directory), False for a linked worktree or anything unreadable. The test is structural, as git's own:
    a linked worktree's admin directory holds a `commondir` file, a submodule's does not. The gitdir is
    resolved against the checkout with every symlink followed, so neither the spelling of the path nor an
    ancestor directory named `worktrees` changes the answer (3b101 QA r3). A gitdir that is missing or not
    a directory returns False: the adapter then stays off, which allows the stop and consumes nothing."""
    dotgit = os.path.join(root, ".git")
    if os.path.isdir(dotgit):
        return True
    try:
        with open(dotgit, encoding="utf-8") as fh:
            first = fh.readline(4096).strip()
    except (OSError, UnicodeDecodeError):
        return False
    if not first.startswith("gitdir:"):
        return False
    target = first[len("gitdir:"):].strip()
    if not target:
        return False
    admin = os.path.realpath(os.path.join(root, target))
    return os.path.isdir(admin) and not os.path.exists(os.path.join(admin, "commondir"))


def _grc_is_worker():
    """A dispatched worker, by either signal the fleet provides: the ORCH_VERIFY_OWNER marker that
    orch-verify exports (presence, even empty), or a CLAUDE_CONFIG_DIR whose basename carries the broker's
    reserved `orch-worker.` prefix (the signal _hookutil.is_worker_session reads). A worker is never armed
    by the orchestrator's lease and never consumes its declared wait (3b101 QA r2, r3). Both signals are
    environment values the same uid can set, so this separates honest sessions, it is not a boundary."""
    if "ORCH_VERIFY_OWNER" in os.environ:
        return True
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or ""
    return os.path.basename(cfg.rstrip("/\\")).startswith("orch-worker.")


MODE_SET_HINT = (
    "set the operating mode to attended in your project's mode record (the operator-set escape hatch); "
    "for a genuine external wait (a running QA leg or CI check), record the blocker, then touch "
    + _grc_escape_file()  # the same resolution the reader uses (3b101 QA r2)
    + " (the grc one-shot declared-wait escape, honoured once)"
)


def repo_root():
    """The repository this hook belongs to, from __file__ (not the payload): the hook lives at
    <root>/.claude/hooks/<name>, so parents[2] is the guarded project's root. The payload is NOT trusted
    to name the root, so it cannot redirect which project's mode/backlog is consulted."""
    return str(Path(__file__).resolve().parents[2])


# ---------------------------------------------------------------------------
# GRC ADAPTATION (project wiring; see the module docstring's GRC note). Only the
# read_operating_mode() adapter body and main() (a grc one-shot-escape pre-step) are customized;
# decide()/run() and the other two adapters are the delivered portable core, unedited. The grc code is
# Exceptions (emitted message text only; predicates/decisions/exit unchanged): P-1.36, #2291, #2496.
# gated on the grc repo root so the bundled --self-test stays hermetic on this host.
# ---------------------------------------------------------------------------
# Paths follow the checkout (3b101): the repo root is this file's grandparent's parent, the lease lives
# in the operational store (GRC_STORE, else <repo-parent>/private), and the declared-wait sentinel in
# GRC_DROP_ROOT, else <repo-parent>/grc_working. No host path is hard-coded.
def _grc_consume_escape(root):
    """grc one-shot operator escape. If this is the grc repo AND the declared-wait sentinel exists,
    CONSUME it (unlink) and return True (allow this stop). A failed unlink returns False (REFUSE the
    escape, mirroring the retired hook). Non-grc-root, a worker session, or an absent sentinel returns
    False. Called at the TOP of main() so the sentinel is consumed one-shot on every ORCHESTRATOR Stop
    invocation -- including the malformed-payload and unconfirmable-owner fail-open paths that return
    before run() -- so a declared wait cannot survive to authorize a later, unintended stop (codex
    validate-pr #1945 f1). A worker never consumes it (3b101 QA r2, r3), so a worker's stop cannot spend
    the orchestrator's one-shot wait."""
    if _grc_is_worker():
        return False
    if not _is_grc_main_checkout(root):
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
    """Map a grc Operating-mode word to the portable arm-state by its WHOLE leading token (3b101): the
    no-idle-stop modes (unattended, overnight-unattended, daytime-unattended, attended-autonomous) map to
    'unattended' (arm the guard); attended and fully-attended map to 'attended' (allow); anything else
    passes through unchanged and allows. This preserves the mode coverage of the retired
    block-idle-stop-with-actionable-backlog.py, which armed on attended-autonomous + the unattended
    modes and exempted fully-attended."""
    if raw is None:
        return None
    # Map the LEADING mode token only: commentary such as "attended; was overnight-unattended" must not
    # arm the guard, and fully-attended is attended (3b101, from the NMW-map-bug finding).
    m = re.match(r"\s*([a-z][a-z-]*)(?![a-z0-9_-])", raw.lower())  # a whole token: no -autonomous_v2 prefix
    word = m.group(1) if m else ""
    if word in ("unattended", "overnight-unattended", "daytime-unattended", "attended-autonomous"):
        return "unattended"
    if word in ("attended", "fully-attended"):
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
         read '**Operating-mode:**' from the store lease (GRC_STORE, else <repo-parent>/private, then
         session-state.md) and map it via _grc_map_mode.
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
    if not _is_grc_main_checkout(root) or _grc_is_worker():
        return None  # a worker is never armed by the orchestrator's lease (3b101 QA r3)
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
# Exceptions (emitted message text only; predicates/decisions/exit unchanged): P-1.36, #2291, #2496.
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
    # Terse block message: emit the COUNT only, never the item enumeration. The full
    # actionable list floods the operator's console and scrolls real content off-screen
    # (maintainer-directed 2026-09-16: keep the detail off-screen). The list is available
    # on demand by running ACTIONABLE_PRODUCER directly.
    reason = (
        "BLOCKED (stop-guard-unattended): a turn-end yield in unattended mode while the backlog "
        "tool reports %d actionable open backlog item(s).\n"
        "WHY: actionable work remaining is not whole-set exhaustion; per "
        "10-TRUST-no-manufactured-winddown, session depth, run length, and work shape are NOT stop "
        "reasons, and a self-reported \"high-priority exhausted\" is not exhaustion.\n"
        "CONSIDER INSTEAD: continue on the highest-priority actionable item (full list on demand: "
        "run %s). If EVERY remaining item is genuinely granted-blocked or deferred to a RECORDED "
        "maintainer decision, record that first (which removes it from the actionable set) and a "
        "stop is then permitted; for a genuine operator stop, %s."
        % (len(actionable), ACTIONABLE_PRODUCER, MODE_SET_HINT)
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

    # Deterministic: the tests control both worker signals (3b101 QA r3: a worker running this self-test
    # has CLAUDE_CONFIG_DIR set to a worker directory).
    _saved_env = {k: os.environ.pop(k, None) for k in ("ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}

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
            self.assertIn("2", reason)          # the COUNT (2 items), not the enumeration
            self.assertNotIn("1: a", reason)    # items are no longer enumerated (terse-console change)

        def test_decide_allow_stop_hook_active(self):
            self.assertFalse(decide("unattended", True, [("1", "a")])[0])

        def test_decide_allow_exhausted(self):
            self.assertFalse(decide("unattended", False, [])[0])

        def test_decide_allow_indeterminate(self):
            self.assertFalse(decide("unattended", False, None)[0])

        def test_decide_allow_attended(self):
            self.assertFalse(decide("attended", False, [("1", "a")])[0])

        def test_decide_message_bounded(self):
            # Terse-console change (maintainer-directed 2026-09-16): the block message
            # emits the COUNT only, never the item enumeration, so its length does not
            # grow with the backlog size and item titles never reach the console.
            many = [("%d" % i, "title%d" % i) for i in range(500)]
            _b, reason = decide("unattended", False, many)
            self.assertNotIn("title", reason)
            self.assertIn("500", reason)
            self.assertLess(len(reason), 1200)

        # ---- default file-based mode adapter ----
        def test_grc_mode_map_reads_the_leading_token(self):
            # 3b101: commentary mentioning "unattended" must not arm the guard; fully-attended is attended.
            for raw, want in (("overnight-unattended", "unattended"), ("daytime-unattended", "unattended"),
                              ("attended-autonomous", "unattended"), ("  Attended-Autonomous ", "unattended"),
                              ("attended; was overnight-unattended", "attended"),
                              ("attended (previously unattended)", "attended"), ("fully-attended", "attended"),
                              (None, None)):
                self.assertEqual(_grc_map_mode(raw), want, raw)

        def test_grc_paths_follow_the_checkout(self):
            # 3b101: no hard-coded host path; the lease and sentinel sit beside the checkout unless overridden.
            # (3b101 QA r3, claude O6: each assertion now pins a value rather than holding trivially.)
            self.assertEqual(_GRC_REPO_ROOT, repo_root())
            self.assertEqual(_GRC_PARENT, os.path.dirname(_GRC_REPO_ROOT))
            saved = os.environ.pop("GRC_DROP_ROOT", None)
            try:
                self.assertEqual(_grc_escape_file(), os.path.join(_GRC_PARENT, "grc_working", ".allow-idle-stop"))
            finally:
                if saved is not None:
                    os.environ["GRC_DROP_ROOT"] = saved
            env = {k: v for k, v in os.environ.items() if k != "GRC_STORE"}
            code = "import runpy,sys; print(runpy.run_path(sys.argv[1])['_GRC_STATE_FILE'])"
            out = subprocess.run([sys.executable, "-B", "-c", code, __file__], capture_output=True, text=True,
                                 env=env, timeout=60)
            self.assertEqual(out.stdout.strip(), os.path.join(_GRC_PARENT, "private", "session-state.md"), out.stderr)
            with open(__file__, encoding="utf-8") as fh:
                self.assertNotIn("/opt/" + "grc", fh.read())

        def test_grc_mode_map_needs_a_whole_token(self):
            # 3b101 QA r1: a malformed suffix is not a known mode, so it passes through (and allows).
            for raw in ("attended-autonomous_v2", "attended-autonomous2", "overnight-unattended9"):
                self.assertEqual(_grc_map_mode(raw), raw.strip(), raw)

        def test_grc_relative_override_resolves_against_the_repo_root(self):
            # 3b101 QA r1: a relative GRC_STORE must not change meaning with the working directory.
            self.assertEqual(_grc_under_root("../private", "x"),
                             os.path.normpath(os.path.join(_GRC_REPO_ROOT, "../private")))
            self.assertEqual(_grc_under_root("", "dflt"), "dflt")
            self.assertEqual(_grc_under_root("/abs/store", "x"), "/abs/store")

        def test_grc_sentinel_is_the_main_checkouts_alone(self):
            # 3b101 QA r1 (claude F1): a worker's Stop in a sibling worktree must not consume the
            # orchestrator's declared-wait sentinel; the main checkout's Stop consumes it.
            import shutil, subprocess, tempfile
            with tempfile.TemporaryDirectory() as parent:
                main_root = os.path.join(parent, "grc_library")
                wt_root = os.path.join(parent, "wt-x")
                for r in (main_root, wt_root):
                    os.makedirs(os.path.join(r, ".claude", "hooks"))
                    shutil.copy(__file__, os.path.join(r, ".claude", "hooks", os.path.basename(__file__)))
                os.makedirs(os.path.join(main_root, ".git"))
                with open(os.path.join(wt_root, ".git"), "w", encoding="utf-8") as fh:
                    fh.write("gitdir: " + os.path.join(main_root, ".git", "worktrees", "wt-x") + "\n")
                drop = os.path.join(parent, "grc_working")
                os.makedirs(drop)
                sentinel = os.path.join(drop, ".allow-idle-stop")
                env = {k: v for k, v in os.environ.items() if k not in ("GRC_DROP_ROOT", "GRC_STORE")}
                for r, want_present in ((wt_root, True), (main_root, False)):
                    open(sentinel, "w").close()
                    subprocess.run([sys.executable, "-B", os.path.join(r, ".claude", "hooks", os.path.basename(__file__))],
                                   input="{}", text=True, capture_output=True, env=env, cwd=r, timeout=60)
                    self.assertEqual(os.path.exists(sentinel), want_present, r)

        def test_grc_worker_in_main_checkout_leaves_the_sentinel(self):
            # 3b101 QA r2: a dispatched worker running in the MAIN checkout must not consume the wait.
            import tempfile
            with tempfile.TemporaryDirectory() as d:
                old = {k: os.environ.get(k) for k in ("GRC_DROP_ROOT", "ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}
                real_gate = globals()["_is_grc_main_checkout"]
                try:
                    # Stand in the main-checkout gate so the worker rule is what is tested, not the layout.
                    globals()["_is_grc_main_checkout"] = lambda root: True
                    os.environ["GRC_DROP_ROOT"], os.environ["ORCH_VERIFY_OWNER"] = d, "worker"
                    sentinel = os.path.join(d, ".allow-idle-stop")
                    open(sentinel, "w").close()
                    self.assertFalse(_grc_consume_escape(_GRC_REPO_ROOT))
                    self.assertTrue(os.path.exists(sentinel))
                    del os.environ["ORCH_VERIFY_OWNER"]  # the config-dir signal alone marks a worker too
                    os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(d, "orch-worker.example") + "/"
                    self.assertFalse(_grc_consume_escape(_GRC_REPO_ROOT))
                    self.assertTrue(os.path.exists(sentinel))
                    os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(d, "orchestrator")  # control: consumes
                    self.assertTrue(_grc_consume_escape(_GRC_REPO_ROOT))
                    self.assertFalse(os.path.exists(sentinel))
                finally:
                    globals()["_is_grc_main_checkout"] = real_gate
                    for k, v in old.items():
                        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

        def test_grc_hint_names_the_file_the_reader_uses(self):
            # 3b101 QA r2 (codex): the refusal's touch path is the path the escape reader consumes.
            self.assertIn(_grc_escape_file(), MODE_SET_HINT)

        def test_grc_lease_arms_only_the_main_checkout_and_submodules(self):
            # 3b101 QA r2: the lease half of the scoping, on real hook copies: the main checkout and a
            # submodule read the lease; a linked worktree does not.
            import shutil, subprocess, tempfile
            with tempfile.TemporaryDirectory() as parent:
                os.makedirs(os.path.join(parent, "private"))
                with open(os.path.join(parent, "private", "session-state.md"), "w", encoding="utf-8") as fh:
                    fh.write("# Session state: grc\n\n**Operating-mode:** overnight-unattended\n")
                # Real admin directories (3b101 QA r3): a linked worktree's holds `commondir`, a submodule's
                # does not. wt-alias reaches the worktree admin through a relative symlinked path; sub-deep
                # is a submodule whose admin path has an ancestor named worktrees.
                wt_admin = os.path.join(parent, "grc_library", ".git", "worktrees", "wt-x")
                os.makedirs(wt_admin)
                open(os.path.join(wt_admin, "commondir"), "w").close()
                os.makedirs(os.path.join(parent, ".git", "modules", "sub"))
                os.makedirs(os.path.join(parent, "worktrees", "modules", "sub-deep"))
                os.makedirs(os.path.join(parent, "wt-alias"))
                os.symlink(os.path.join(parent, "grc_library", ".git", "worktrees"),
                           os.path.join(parent, "wt-alias", "worktrees"))
                layouts = {"grc_library": None, "wt-x": f"gitdir: {wt_admin}\n",
                           "wt-alias": "gitdir: worktrees/wt-x\n", "sub": "gitdir: ../.git/modules/sub\n",
                           "sub-deep": f"gitdir: {os.path.join(parent, 'worktrees', 'modules', 'sub-deep')}\n",
                           "missing": "gitdir: ../nowhere\n"}
                got = {}
                for name, gitfile in layouts.items():
                    r = os.path.join(parent, name)
                    os.makedirs(os.path.join(r, ".claude", "hooks"))
                    hook = os.path.join(r, ".claude", "hooks", os.path.basename(__file__))
                    shutil.copy(__file__, hook)
                    if gitfile is None:
                        os.makedirs(os.path.join(r, ".git"), exist_ok=True)
                    else:
                        with open(os.path.join(r, ".git"), "w", encoding="utf-8") as fh:
                            fh.write(gitfile)
                    env = {k: v for k, v in os.environ.items()
                           if k not in ("GRC_STORE", "ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}
                    code = ("import runpy,sys; m=runpy.run_path(sys.argv[1]); "
                            "print(m['read_operating_mode'](m['repo_root']()))")
                    out = subprocess.run([sys.executable, "-B", "-c", code, hook], capture_output=True, text=True,
                                         env=env, timeout=60)
                    got[name] = out.stdout.strip()
                self.assertEqual(got, {"grc_library": "unattended", "wt-x": "None", "wt-alias": "None",
                                       "sub": "unattended", "sub-deep": "unattended", "missing": "None"}, got)
                # A worker in the main checkout is never armed by the lease (3b101 QA r3).
                hook = os.path.join(parent, "grc_library", ".claude", "hooks", os.path.basename(__file__))
                env["CLAUDE_CONFIG_DIR"] = os.path.join(parent, "orch-worker.example")
                out = subprocess.run([sys.executable, "-B", "-c", code, hook], capture_output=True, text=True,
                                     env=env, timeout=60)
                self.assertEqual(out.stdout.strip(), "None", out.stderr)

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
    for k, v in _saved_env.items():
        if v is not None:
            os.environ[k] = v
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

