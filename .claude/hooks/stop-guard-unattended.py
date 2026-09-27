#!/usr/bin/env python3
"""Stop hook: block unattended actionable-work stops unless awaiting enough live dispatches.

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

What it does, in order (main first consumes any grc one-shot declared-wait escape):
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
  4. At least _MIN_LIVE_GROUPS (3) live owned dispatch groups -> allow dispatch-and-await, with a note.
     Registry read failure -> allow, except a boundary-byte failure discards the first row and
     continues counting; missing registry means zero groups.
  5. Otherwise -> BLOCK (exit 2), reporting the actionable count, producer command, rule and escape.
     Item IDs and titles are not emitted (#2291). B's five-line/160-character clamps remain.

Fail-OPEN. On failure to determine the mode or the actionable set, the hook ALLOWS the stop. A
guard that traps the actor on its own malfunction protects nothing; a convenience guardrail that
wrongly blocks a legitimate stop is worse than the mistake it prevents.

PORTABILITY. The ADAPTER SEAM contains grc's lease-mode, producer and generic owner adapters,
plus grc path, checkout, worker and one-shot helpers. main() also carries the one-shot escape
pre-step. The registry observer, decision predicates, run(), payload parsing and diagnostic transport
are lab_infra commit 17b407b9 (PR #952, item 373), unchanged. Emitted block-message text alone
carries P-1.36 (BLOCKED / WHY / CONSIDER INSTEAD), #2291 (count only, producer on demand) and
#2496 (resolved declared-wait path). MODE_SET_HINT retains the detailed grc guidance; the emitted
hint is shortened to fit B's message format. Unusually long override paths can still be truncated
by B's unchanged per-line clamp.

GRC ADAPTATION (2026-09-27; backlog 3b113). Rebased the 2026-09-03 cross-project adoption
(inbox msg 20260903T002018Z.from-lab_infra) onto lab_infra 17b407b9, adding the live-dispatch
allowance and bounded diagnostic transport. read_operating_mode reads session-state.md via
_grc_map_mode; main() consumes .allow-idle-stop before parsing the payload. Lease and escape
helpers are scoped to the primary grc checkout and exclude both fleet worker signals.
Actionable items come from .claude/hooks/nmw-actionable (-> tools/audit-backlog-actionability.py);
grc does not use tools/flow.py or tools/pipeline.py. Orchestrator scoping uses both fleet worker signals
(the ORCH_VERIFY_OWNER marker exported by orch-verify, or an `orch-worker.` CLAUDE_CONFIG_DIR). This hook replaces the registration of
block-idle-stop-with-actionable-backlog.py (retained, de-registered).
Paths follow the checkout: GRC_STORE or <repo-parent>/private holds the lease; GRC_DROP_ROOT or
<repo-parent>/grc_working holds the escape. Relative overrides resolve against the repo root.
Reconciles to the fleet-canonical form when the guardrails/AIQT pack ships it.
GRC NOTE (3b113 QA r1): the live-group count below is scoped by uid and ORCH_OWNER, not by session or
repository. grc's orchestrator and its workers share one uid, so groups recorded by another grc session
(a second orchestrator, or a worker dispatching workers of its own) count toward the floor too.

Dispatch-and-await is separately observed through the broker's per-uid kill registry
(/run/orch-workers/killreg.<euid>; tools/orch-worker-broker:killreg_record, tools/orch-verify:load_registry).
A file or narration alone cannot satisfy the live-group threshold: each distinct group needs a live,
non-zombie, non-stopped timeout leader owned by this uid and recorded for this ORCH_OWNER
(default: id -un), with pgid and start time still matching procfs. Empty or invalid owners
cannot count. Three groups is the D-295 minimum proxy, not proof of three distinct workstreams
or progress. Unrecorded/no-timeout dispatches and leaderless groups do not count. Like the
existing registry consumer, this is a cooperative guardrail, not a security boundary against
an owner manufacturing processes. A file alone cannot establish liveness; there is no
payload/env override for the registry path. Only newline-terminated, six-field recorder rows
with canonical decimal identities, valid session/owner characters and a UTC timestamp count.
The owner must match the full field exactly. Malformed rows are skipped; lock contention is
retried for at most 0.2 seconds before failing open. A registry object owned by another uid
counts as zero groups, including unreadable files, symlinks and FIFOs. Unobservable ownership
still fails open. Unobservable groups do not count. Registry reads scan at most 1 MiB plus 4096 bytes,
including discarded fragments, from the file's tail under the shared lock, retaining the newest
4096 complete rows there. Each retained row is at most 4096 bytes and lies within the scan budget.
A nonzero starting offset reads one additional byte under the same lock to check the preceding
newline. An unreadable boundary byte or an initial row fragment discards the first row.
Oversized and unterminated rows do not count; rows before the tail window remain unobserved.
Observation is a point-in-time snapshot.
Diagnostics are delivered only to regular files, FIFOs and sockets. Terminal stderr,
including PTY masters and slaves, other devices and unknown types receives no diagnostic:
these destinations are silently dropped without writing or reopening them. Unavailable
permitted destinations can also lose diagnostics. The exit status remains the contract.

Self-test: python3 .claude/hooks/stop-guard-unattended.py --self-test.
Self-contained: grc file/producer fixtures replace lab_infra tooling fixtures; registry cases remain.
"""

import datetime
import fcntl
import json
import os
import pwd
import re
import stat
import subprocess
import sys
import time
from pathlib import Path
from collections import deque

# Architect-directed 2026-09-24: the block message is at most _MAX_REASON_LINES lines of at most
# _MAX_LINE_CHARS characters, whatever the item count. B computes the first _MAX_IDS item numbers;
# grc message exceptions below use the producer command and emit only the count.
_MAX_REASON_LINES = 5
_MAX_LINE_CHARS = 160
_MAX_IDS = 5
_MIN_LIVE_GROUPS = 3  # D-295: three active workstreams; a lone worker cannot license a yield.
_KILLREG_DIR = "/run/orch-workers"
_MAX_REGISTRY_ROW_BYTES = 4096
_MAX_REGISTRY_ROWS = 4096
_MAX_REGISTRY_SCAN_BYTES = 1024 * 1024 + _MAX_REGISTRY_ROW_BYTES
_MAX_PID = 4194304  # Linux pid_max ceiling; reject malformed identities before procfs lookup.
_LOCK_WAIT_SECONDS = 0.2


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
    ancestor directory named `worktrees` changes the answer (3b101 QA r3). The admin directory must hold a
    HEAD file, as every git directory does, so a gitdir naming some other directory is not taken for one
    (3b101 QA r5). A gitdir that is missing, malformed or not a git directory returns False: the adapter
    then stays off, which allows the stop and consumes nothing. Known residue (3b101 INFO-1, open as
    P-TODO 3b124): only the first line is read and it is whitespace-stripped, so a gitfile git itself
    rejects (extra spaces around the target, a trailing line) is still accepted here."""
    dotgit = os.path.join(root, ".git")
    if os.path.isdir(dotgit):
        return True
    try:
        with open(dotgit, encoding="utf-8") as fh:
            first = fh.readline(4096).strip()
    except (OSError, UnicodeDecodeError):
        return False
    if not first.startswith("gitdir: "):  # git's read_gitfile requires the space (3b101 QA r6)
        return False
    target = first[len("gitdir: "):].strip()
    if not target:
        return False
    try:  # a NUL in the gitdir raises ValueError (3b101 QA r5)
        admin = os.path.realpath(os.path.join(root, target))
        # lexists: git accepts a symlinked HEAD (core.preferSymlinkRefs), even one that dangles (3b101 QA r6)
        if not (os.path.isdir(admin) and os.path.lexists(os.path.join(admin, "HEAD"))):
            return False
        os.stat(os.path.join(admin, "commondir"))  # only a confirmed absence counts (3b101 QA r4)
    except FileNotFoundError:
        return True
    except (OSError, ValueError):
        return False
    return False


def _grc_is_worker():
    """A dispatched worker, by either signal the fleet provides: the ORCH_VERIFY_OWNER marker that
    orch-verify exports (presence, even empty), or a CLAUDE_CONFIG_DIR whose basename carries the broker's
    reserved `orch-worker.` prefix (the signal _hookutil.is_worker_session reads). A worker is never armed
    by the orchestrator's lease and never consumes its declared wait (3b101 QA r2, r3). Both signals are
    environment values the same uid can set, so this separates honest sessions, it is not a boundary."""
    if "ORCH_VERIFY_OWNER" in os.environ:
        return True
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or ""
    return bool(cfg) and Path(cfg).name.startswith("orch-worker.")  # as _hookutil reads it (3b101 QA r4)


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
# GRC ADAPTATION (project wiring; see the module docstring's GRC note).
# Lease-mode and producer adapters plus the grc helpers are carried from A, with the 3b113 QA r1 worker
# scoping (both fleet signals) and the r2 lease-only mode source in the grc checkout.
# main() carries the one-shot escape; decision predicates and the new registry remain B's.
# Emitted-message exceptions only: P-1.36, #2291, #2496.
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
# These THREE adapters couple the portable decision core
# to project tooling. Each has a fixed contract; honour the contract and the
# core is unchanged. The defaults are a minimal, dependency-free, file-based adapter.
#
#   read_operating_mode(root) -> "unattended" | "attended" | <other-str> | None
#       The operating mode. None means INDETERMINATE (a read failure) -> fail open (allow the stop).
#       Any string other than "unattended" allows the stop. Only "unattended" arms the guard.
#
#   actionable_items(root)    -> list[(id, title)] | None
#       The tool-verified set of open backlog items that are NOT granted-blocked. None means
#       INDETERMINATE (a read failure) -> fail open (allow). An EMPTY list means genuine whole-set
#       exhaustion -> allow the stop. A non-empty list -> consult the live dispatch count.
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

    One source per checkout (3b113 QA r2):
      - the primary grc checkout: the store lease only (_grc_lease_mode: '**Operating-mode:**' from
        GRC_STORE, else <repo-parent>/private, then session-state.md, mapped via _grc_map_mode); a
        MODE_FILE there is ignored, so a stray file never shadows the lease.
      - any other root (the bundled --self-test, a file-based adopter): the repo-relative single-word
        file MODE_FILE. Present -> its trimmed word (or None); absent -> None.
         (The one-shot declared-wait escape is consumed at the top of main() by _grc_consume_escape.)

    GRC WIRING NOTE: grc keeps the mode in session-state.md (not MODE_FILE) and declares a genuine wait
    with the .allow-idle-stop sentinel (the retired block-idle-stop hook's documented escape), both
    preserved here. A read failure at either source returns None (fail open)."""
    # GRC (3b113 QA r2): the grc main checkout keeps its mode ONLY in the lease, so a stray MODE_FILE there
    # never shadows it. Every other root takes the delivered core's portable MODE_FILE branch.
    if _is_grc_main_checkout(root):
        return _grc_lease_mode(root)
    path = os.path.join(root, MODE_FILE)
    try:
        with open(path, encoding="utf-8") as fh:
            val = fh.read().strip()
        return val or None
    except FileNotFoundError:
        pass  # no file-based mode record
    except OSError:
        return None
    # Not the grc checkout, so _grc_lease_mode returns None here; the call is kept as a defensive default.
    return _grc_lease_mode(root)


def _grc_lease_mode(root):
    """grc mode source: session-state.md 'Operating-mode:' -> mapped arm-state, only in the primary grc
    checkout and never for a worker (3b101 QA r3). (The one-shot declared-wait escape is handled at the top
    of main() via _grc_consume_escape, not here, so it is consumed on the malformed/worker fail-open paths
    too.) Split out of read_operating_mode in 3b113 QA r2 so the grc checkout reads the lease alone."""
    if not _is_grc_main_checkout(root) or _grc_is_worker():
        return None
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
    truthiness: even an empty string signals a worker). The orchestrator never sets it. GRC: the marker
    read is _grc_is_worker(), which also takes an `orch-worker.` CLAUDE_CONFIG_DIR (3b113 QA r1); grc's
    orchestrator and workers share one uid, so the uid comparison alone does not separate them. If your fleet
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
    # GRC: both fleet worker signals (3b113 QA r1): a worker marked only by its CLAUDE_CONFIG_DIR must not be
    # armed by a file-based mode record either.
    return _is_orchestrator(euid, owner_uid, _grc_is_worker())

# ============================================================================
# END ADAPTER SEAM -- B core below; decision predicates and registry code are unchanged. (GRC:
# Exceptions (emitted message text only; predicates/decisions/exit unchanged): P-1.36, #2291, #2496.
# main() below carries a one-shot-escape pre-step; see the GRC ADAPTATION note.)
# ============================================================================


def _group_is_live(pgid, start, uid):
    """Corroborate a broker record with kernel identity; vanished/reused/dead/foreign -> False.
    The timeout leader retains the orchestrator uid; its worker children may use another uid.
    Hold the proc directory while reading so PID reuse cannot redirect the stat read."""
    try:
        fd = os.open("/proc/%d" % pgid, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        try:
            if os.fstat(fd).st_uid != uid:
                return False
            stat_fd = os.open("stat", os.O_RDONLY | os.O_CLOEXEC, dir_fd=fd)
            with os.fdopen(stat_fd, "rb") as stream:
                data = stream.read()
        finally:
            os.close(fd)
        # /proc stat: comm may contain spaces/parentheses; rest begins at field 3.
        end = data.rindex(b")")
        comm = data[data.index(b"(") + 1:end]
        rest = data[end + 2:].split()
        return (comm == b"timeout" and rest[0] not in (b"Z", b"X", b"x", b"T", b"t")
                and int(rest[2]) == pgid and int(rest[19]) == start)
    except (OSError, ValueError, IndexError):
        return False  # a failed group observation cannot invalidate the registry


def _lock_registry(fd):
    """Retry the broker's non-blocking flock pattern within a short elapsed-time budget."""
    deadline = time.monotonic() + _LOCK_WAIT_SECONDS
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            time.sleep(min(0.01, remaining))


def _registry_rows(stream, offset=0):
    """Bound reads from offset, discarding its initial fragment and retaining complete rows."""
    remaining = _MAX_REGISTRY_SCAN_BYTES
    rows = deque(maxlen=_MAX_REGISTRY_ROWS)
    stream.seek(offset)
    oversized = False
    if offset:
        # A separate one-byte allowance preserves the entire row window. pread
        # neither advances the stream nor triggers buffered read-ahead.
        try:
            previous = os.pread(stream.fileno(), 1, offset - 1)
        except (OSError, ValueError):
            previous = b""  # an unknown boundary conservatively discards the first row
        oversized = previous != b"\n"
    while remaining:
        line = stream.readline(min(_MAX_REGISTRY_ROW_BYTES + 1, remaining))
        remaining -= len(line)
        if not line:
            break
        if oversized or len(line) > _MAX_REGISTRY_ROW_BYTES:
            oversized = not line.endswith(b"\n")
            continue
        if not line.endswith(b"\n"):
            break  # neither EOF nor budget exhaustion completes a trailing fragment
        rows.append(line)
    yield from rows


def live_dispatch_groups():
    """Count distinct live broker groups for this uid and owner, or None on registry read failure.
    A boundary-byte read failure instead discards the first row and continues counting.
    Mirror the broker/reaper's no-symlink, regular-file, uid, owner and bounded flock checks.
    A missing registry is zero; malformed or foreign rows cannot authorize a yield."""
    uid = os.geteuid()
    # The recorder defaults ORCH_OWNER to id -un only when unset, not when empty.
    owner = os.environ.get("ORCH_OWNER")
    if owner is None:
        try:
            owner = pwd.getpwuid(uid).pw_name
        except (KeyError, OSError):
            return 0  # no rows can be attributed to an unresolved owner
    if not owner or any(c not in
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-" for c in owner):
        return 0  # the recorder would refuse this owner
    owner = owner.encode("ascii")
    path = os.path.join(_KILLREG_DIR, "killreg.%d" % uid)
    try:
        try:
            # Inspect ownership before opening: a peer's symlink, FIFO or unreadable
            # file is a known foreign registry, not an observation failure.
            if os.lstat(path).st_uid != uid:
                return 0
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
        except FileNotFoundError:
            return 0
        with os.fdopen(fd, "rb", buffering=_MAX_REGISTRY_ROW_BYTES) as stream:
            st = os.fstat(stream.fileno())
            if st.st_uid != uid:
                return 0
            if not stat.S_ISREG(st.st_mode):
                return None
            if not _lock_registry(stream.fileno()):
                return None
            # The broker appends under this lock; refresh size after acquiring it.
            offset = max(0, os.fstat(stream.fileno()).st_size - _MAX_REGISTRY_SCAN_BYTES)
            rows = list(_registry_rows(stream, offset))
    except (OSError, ValueError):
        # Registry metadata, open, lock and row-read failures fail open; a boundary-byte
        # read failure is handled above by discarding the first row and continuing the count.
        return None
    live = set()
    for line in rows:
        if not line:
            continue
        fields = line.rstrip(b"\n").split(b"\t")
        # tools/orch-worker-broker:killreg_record writes exactly these six fields.
        # Validate the complete schema before attributing a row to its owner.
        if len(fields) != 6:
            continue
        if any(re.fullmatch(rb"(?:0|[1-9][0-9]*)", field) is None
               for field in fields[:3]):
            continue
        if any(re.fullmatch(rb"[A-Za-z0-9._-]+", field) is None
               for field in fields[3:5]):
            continue
        if re.fullmatch(rb"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",
                        fields[5]) is None:
            continue
        try:
            value = fields[5].decode("ascii")
            parsed = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
                continue
            pgid, leader, start = map(int, fields[:3])
        except ValueError:
            continue
        if fields[4] != owner:
            continue
        if pgid <= 1 or pgid > _MAX_PID or leader != pgid or start < 0:
            continue
        if _group_is_live(pgid, start, uid):
            live.add(pgid)
    return len(live)


def decide(mode, stop_hook_active, actionable, live_groups=0):
    """Pure decision. Returns (block: bool, reason: str). Block iff: unattended mode AND not already in a
    stop-hook continuation AND the actionable set is non-empty AND the known live count is below the floor. `actionable` is a list (possibly
    empty) or None (indeterminate -> fail open). Live groups at the floor permit awaiting;
    an indeterminate live count also fails open."""
    if mode != "unattended":
        return False, ""
    if stop_hook_active:
        return False, ""  # documented loop-guard: already blocked this chain -> allow (no infinite loop)
    if not isinstance(actionable, list) or not actionable:
        return False, ""  # None (indeterminate) or empty (exhausted) -> allow
    if live_groups is None:
        return False, "STOP ALLOWED (unattended): live dispatch observation unavailable; fail open."
    if live_groups >= _MIN_LIVE_GROUPS:
        return False, "STOP ALLOWED (unattended): %d live owned dispatch groups; yielding to await work (minimum %d)." % (
            live_groups, _MIN_LIVE_GROUPS)
    ids = ", ".join(str(iid)[:12] for iid, _title in actionable[:_MAX_IDS])
    if len(actionable) > _MAX_IDS:
        ids += " ..."
    lines = [
        "BLOCKED (stop-guard-unattended): unattended turn-end yield; the backlog tool reports "
        "%d actionable open backlog item(s)." % len(actionable),
        "WHY: not whole-set exhaustion; per 10-TRUST-no-manufactured-winddown, "
        "depth, run length and work shape are not stop reasons.",
        "CONSIDER INSTEAD: continue on the highest-priority actionable item "
        "(full list: %s)." % ACTIONABLE_PRODUCER,
        "Yield allowed with at least %d live owned dispatch groups, or no actionable items "
        "(a [BLOCKED:<reason>] tag with a granted approvals row)." % _MIN_LIVE_GROUPS,
        "Declared wait: touch %s (once, after recording blocker); operator stop: set mode attended."
        % _grc_escape_file(),
    ]
    return True, "\n".join(line[:_MAX_LINE_CHARS] for line in lines[:_MAX_REASON_LINES])


def _diagnostic(message):
    """Emit a capped best-effort diagnostic without changing shared fd 2 flags."""
    import select
    import socket
    import stat
    import time
    if sys.stderr is None:
        return  # fd 2 started closed and may now belong to an unrelated file.
    # Fork before inspecting stderr: even metadata can stall on NFS or FUSE.
    deadline = time.monotonic() + 0.2
    try:
        child = os.fork()
    except OSError:
        return  # No caller-side fallback may touch stderr.
    if child:
        try:
            while time.monotonic() < deadline:
                if os.waitpid(child, os.WNOHANG)[0]:
                    break
                time.sleep(min(0.005, max(0, deadline - time.monotonic())))
        except OSError:
            pass
        return
    fd = 2
    peer = None
    try:
        # Release every inherited lock and pipe before inspecting stderr.
        # Failed enumeration drops the diagnostic.
        for entry in os.listdir("/proc/self/fd"):
            other = int(entry)
            if other != 2:
                try:
                    os.close(other)
                except OSError:
                    pass
        os.setsid()
        remaining = memoryview(message[:select.PIPE_BUF].encode(
            "utf-8", "backslashreplace")[:select.PIPE_BUF])
        mode = os.fstat(2).st_mode
        # A delayed classification may still deliver after the caller exits.
        deadline = time.monotonic() + 0.2
        if stat.S_ISFIFO(mode):
            # Independent flags keep a competing pipe writer from blocking us.
            fd = os.open("/proc/self/fd/2",
                         os.O_WRONLY | os.O_NONBLOCK | os.O_CLOEXEC)
        elif stat.S_ISSOCK(mode):
            # MSG_DONTWAIT is per send; dup() alone shares the original flags.
            fd = os.dup(2)
            peer = socket.socket(fileno=fd)
        elif stat.S_ISREG(mode):
            # Regular-file writes ignore O_NONBLOCK; only this child can stall.
            while remaining and time.monotonic() < deadline:
                written = os.write(2, remaining)
                if written <= 0:
                    break
                remaining = remaining[written:]
            return
        else:
            # Terminals, devices and unknown types receive no diagnostic.
            # Never write or reopen them: job control can stop even non-blocking
            # writes, and reopening a PTY master allocates a different PTY.
            return
        while remaining:
            wait = deadline - time.monotonic()
            if wait <= 0:
                return
            target = 2 if peer is not None else fd
            if not select.select([], [target], [], wait)[1]:
                return
            written = (peer.send(remaining, socket.MSG_DONTWAIT) if peer is not None
                       else os.write(fd, remaining))
            if written <= 0:
                return
            remaining = remaining[written:]
    except (OSError, ValueError):
        pass  # Unavailable targets, stale readiness and timeouts drop the rest.
    finally:
        try:
            if peer is not None:
                peer.close()
            elif fd != 2:
                os.close(fd)
        except OSError:
            pass
        finally:
            # Never flush inherited streams or run caller cleanup handlers.
            os._exit(0)


def run(root, payload):
    """Core: exit 2 (block) iff this is the ORCHESTRATOR session, unattended, not a stop-hook continuation,
    and pipeline shows actionable work without enough live dispatches; else 0.
    Registry read failures fail open except boundary-byte failures, which discard the first row
    and continue counting; unobservable groups do not count."""
    if not is_orchestrator_session(root):
        return 0  # a dispatched worker (or an unconfirmable owner) -> allow; this guard binds the orchestrator only
    mode = read_operating_mode(root)
    stop_hook_active = bool(payload.get("stop_hook_active")) if isinstance(payload, dict) else False
    actionable = None
    if mode == "unattended" and not stop_hook_active:
        actionable = actionable_items(root)  # only compute when it can change the outcome
    live_groups = live_dispatch_groups() if actionable else 0
    block, reason = decide(mode, stop_hook_active, actionable, live_groups)
    if reason:
        _diagnostic(reason + "\n")
    return 2 if block else 0


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
    import contextlib
    import io
    import inspect
    import textwrap
    import types
    import json as _json
    import signal
    import subprocess
    from unittest import mock
    import shutil
    import tempfile
    import unittest

    @contextlib.contextmanager
    def capture_stderr(stream):
        real_write = os.write

        def written(fd, data):
            if fd == 2 or os.path.sameopenfile(fd, 2):
                stream.write(bytes(data).decode("utf-8"))
                return len(data)
            return real_write(fd, data)

        # The production helper deliberately drops terminals and devices.
        # Supply a FIFO independently of the self-test runner's stderr type.
        reader, writer = os.pipe()
        saved = os.dup(2)
        try:
            os.dup2(writer, 2)
            # Execute the child branch inline so capture remains observable.
            # Real process boundaries are exercised by test_killreg_writes.py.
            with mock.patch.object(os, "fork", return_value=0), \
                    mock.patch.object(os, "listdir", return_value=[]), \
                    mock.patch.object(os, "setsid"), \
                    mock.patch.object(os, "_exit"), \
                    mock.patch.object(os, "write", side_effect=written):
                yield stream
        finally:
            os.dup2(saved, 2)
            os.close(saved)
            os.close(writer)
            os.close(reader)

    root_real = repo_root()
    # Deterministic: both grc worker signals belong to the fixtures.
    _saved_env = {k: os.environ.pop(k, None) for k in ("ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}

    UNATT = "unattended"
    ATT = "attended"
    # The producer owns granted-block filtering; these fixtures model its output contract.
    ITEMS_MIXED = "1\tFirst actionable item\n3\tProposed-hold item"
    ITEMS_ALL_BLOCKED = "# all items granted-blocked"
    ITEMS_EMPTY = "# nothing actionable"

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
        def setUp(self):
            # Never let a host's live fleet affect either in-process or subprocess tests.
            self.registry = tempfile.TemporaryDirectory()
            self.addCleanup(self.registry.cleanup)
            patcher = mock.patch.dict(globals(), _KILLREG_DIR=self.registry.name)
            patcher.start()
            self.addCleanup(patcher.stop)
            owner_env = mock.patch.dict(os.environ, {"ORCH_OWNER": "fixture"})
            owner_env.start()
            self.addCleanup(owner_env.stop)
            self.surviving_members = {}

        def assert_mutation_detected(self, case, changes, mismatch, witness, faults=None):
            """Require the intended assertion and an affirmative observation of the mutant.
            Deliberate registry failure mutations must mark their own failure branch;
            an incidental None or a fixture/setup assertion is never detection evidence.
            """
            nested = T(case) if isinstance(case, str) else case
            observed, detected = [], []
            count_groups = changes.get("live_dispatch_groups", live_dispatch_groups)
            faults = [] if faults is None else faults

            def observe():
                before = len(faults)
                count = count_groups()
                observed.append((count, len(faults) > before))
                return count

            equal = nested.assertEqual
            def check_equal(actual, expected, *args, **kwargs):
                if (actual, expected) in mismatch and observed:
                    count, deliberate = observed[-1]
                    if count == witness and (count is not None or deliberate):
                        detected.append((actual, expected))
                return equal(actual, expected, *args, **kwargs)

            nested.assertEqual = check_equal
            with mock.patch.dict(globals(), dict(changes, live_dispatch_groups=observe)):
                result = unittest.TestResult()
                nested.run(result)
            self.assertFalse(result.errors, result.errors)
            self.assertTrue(detected, (case, observed, result.failures))
            self.assertEqual(len(result.failures), len(detected), result.failures)
            self.assertTrue(all(count is not None or deliberate
                                for count, deliberate in observed), observed)
            return result

        @contextlib.contextmanager
        def workers(self, count=3, command=None):
            children = []
            try:
                for _ in range(count):
                    children.append(subprocess.Popen(
                        command if command is not None else ["timeout", "60", "sleep", "60"],
                        start_new_session=True,
                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                self.record(children)
                yield children
            finally:
                for child in children:
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()

        def record(self, children, start_delta=0, copies=1, owner="fixture"):
            rows = []
            for child in children:
                data = Path("/proc/%d/stat" % child.pid).read_bytes()
                start = int(data[data.rindex(b")") + 2:].split()[19])
                rows.append("%d\t%d\t%d\t-\t%s\t2026-09-25T00:00:00Z\n" % (
                    child.pid, child.pid, start + start_delta, owner))
            Path(self.registry.name, "killreg.%d" % os.geteuid()).write_text("".join(rows) * copies)

        def outcome(self):
            with tempfile.TemporaryDirectory() as d, capture_stderr(io.StringIO()) as err:
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED)
                rc = run(d, {"stop_hook_active": False})
                return rc, err.getvalue()

        def test_live_floor_allows(self):
            self.assertEqual(_MIN_LIVE_GROUPS, 3)
            with self.workers():
                self.assertEqual(live_dispatch_groups(), 3)
                rc, note = self.outcome()
                self.assertEqual(rc, 0)
                self.assertEqual(len(note.splitlines()), 1)
                self.assertIn("3 live owned dispatch groups", note)

        def test_below_floor_blocks(self):
            with self.workers(2):
                self.assertEqual(live_dispatch_groups(), 2)
                rc, reason = self.outcome()
                self.assertEqual(rc, 2)
                self.assertIn("at least 3 live owned dispatch groups", reason)

        def test_stale_registry_blocks(self):
            with self.workers():
                pass  # leave rows behind after every group is killed and reaped
            self.assertEqual(live_dispatch_groups(), 0)
            self.assertEqual(self.outcome()[0], 2)

        def test_reused_pid_blocks(self):
            with self.workers() as children:
                self.record(children, start_delta=1)
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_duplicates_do_not_meet_floor(self):
            with self.workers(1) as children:
                self.record(children, copies=3)
                self.assertEqual(live_dispatch_groups(), 1)
                self.assertEqual(self.outcome()[0], 2)

        def test_foreign_uid_groups_block(self):
            real_fstat = os.fstat
            def foreign_proc(fd):
                st = real_fstat(fd)
                if stat.S_ISDIR(st.st_mode):  # real proc directory, not the owned registry
                    fields = list(st)
                    fields[4] = os.geteuid() + 1
                    return os.stat_result(fields)
                return st
            with self.workers(), mock.patch.object(os, "fstat", side_effect=foreign_proc):
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_foreign_registry_blocks(self):
            real_fstat = os.fstat
            def foreign_file(fd):
                st = real_fstat(fd)
                if stat.S_ISREG(st.st_mode):
                    fields = list(st)
                    fields[4] = os.geteuid() + 1
                    return os.stat_result(fields)
                return st
            with self.workers(), mock.patch.object(os, "fstat", side_effect=foreign_file):
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_registry_object_ownership_precedes_open(self):
            path = Path(self.registry.name, "killreg.%d" % os.geteuid())
            for kind in ("symlink", "fifo", "unreadable"):
                if kind == "symlink":
                    path.symlink_to(Path(self.registry.name, "absent"))
                elif kind == "fifo":
                    os.mkfifo(path)
                else:
                    path.touch(mode=0o000)
                try:
                    metadata = list(os.lstat(path))
                    metadata[4] = os.geteuid() + 1
                    with mock.patch.object(os, "lstat", return_value=os.stat_result(metadata)):
                        with mock.patch.object(os, "open", side_effect=PermissionError) as opened:
                            count = live_dispatch_groups()
                            self.assertEqual(count, 0)
                            self.assertTrue(decide("unattended", False, [("1", "sample")], count)[0])
                            opened.assert_not_called()
                    # The same object owned by us retains the observation-failure contract.
                    self.assertIsNone(live_dispatch_groups())
                finally:
                    path.unlink()

        def test_registry_lstat_failure_fails_open(self):
            real_lstat = os.lstat
            path = os.path.join(self.registry.name, "killreg.%d" % os.geteuid())
            for failure in (PermissionError, OSError):
                def denied(candidate, *args, **kwargs):
                    if candidate == path:
                        raise failure("sample registry metadata failure")
                    return real_lstat(candidate, *args, **kwargs)
                with mock.patch.object(os, "lstat", side_effect=denied):
                    self.assertIsNone(live_dispatch_groups())
                    self.assertEqual(self.outcome()[0], 0)

        def test_malformed_rows_do_not_mask_blocks_or_live_rows(self):
            path = Path(self.registry.name, "killreg.%d" % os.geteuid())
            bad_rows = (
                b"2\t2\t1\t-\tfixture\t2026-02-30T00:00:00Z\n",
                b"bad row\n", b"a\t2\t3\t-\tfixture\t2026-09-25T00:00:00Z\n",
                b"2\ta\t3\t-\tfixture\t2026-09-25T00:00:00Z\n", b"2\t2\ta\t-\tfixture\t2026-09-25T00:00:00Z\n",
                b"0\t0\t3\t-\tfixture\t2026-09-25T00:00:00Z\n", b"1\t1\t3\t-\tfixture\t2026-09-25T00:00:00Z\n",
                b"-2\t-2\t3\t-\tfixture\t2026-09-25T00:00:00Z\n", b"2\t3\t3\t-\tfixture\t2026-09-25T00:00:00Z\n",
                b"2\t2\t-1\t-\tfixture\t2026-09-25T00:00:00Z\n", b"\xff\t2\t3\t-\tfixture\t2026-09-25T00:00:00Z\n",
            )
            for sample in (b"4194305", b"9" * 4100, b"9" * 5000):
                bad_rows += (
                    sample + b"\t" + sample + b"\t1\t-\tfixture\t2026-09-25T00:00:00Z\n",
                    sample + b"\t2\t1\t-\tfixture\t2026-09-25T00:00:00Z\n",
                    b"2\t" + sample + b"\t1\t-\tfixture\t2026-09-25T00:00:00Z\n",
                )
            for bad in bad_rows:
                with self.subTest(bad=bad):
                    path.write_bytes(bad)
                    self.assertEqual(live_dispatch_groups(), 0)
                    self.assertEqual(self.outcome()[0], 2)
            with self.workers() as children:
                good = path.read_bytes()
                for count in (2, 3):
                    rows = good.splitlines(keepends=True)[:count]
                    for bad in bad_rows:
                        with self.subTest(count=count, bad=bad):
                            path.write_bytes(bad + bad.join(rows) + bad)
                            self.assertEqual(live_dispatch_groups(), count)
                            self.assertEqual(self.outcome()[0], 2 if count == 2 else 0)

        def test_registry_truncated_rows_block(self):
            path = Path(self.registry.name, "killreg.%d" % os.geteuid())
            with self.workers():
                rows = path.read_bytes().splitlines(keepends=True)
                foreign = rows[2].replace(b"\tfixture\t", b"\tfixture.extra\t")
                path.write_bytes(b"".join(rows[:2]) + foreign)
                self.assertEqual(live_dispatch_groups(), 2)
                self.assertEqual(self.outcome()[0], 2)
                fragment = foreign.split(b".extra", 1)[0]
                for tail in (fragment, fragment + b"\n", rows[2][:-1]):
                    with self.subTest(tail=tail):
                        path.write_bytes(b"".join(rows[:2]) + tail)
                        self.assertEqual(live_dispatch_groups(), 2)
                        self.assertEqual(self.outcome()[0], 2)

        def test_registry_exact_schema(self):
            path = Path(self.registry.name, "killreg.%d" % os.geteuid())
            with self.workers():
                rows = path.read_bytes().splitlines(keepends=True)
                fields = rows[2][:-1].split(b"\t")
                self.assertEqual(live_dispatch_groups(), 3)
                invalid = [fields[:5], fields + [b"extra"]]
                for index, samples in (
                        (0, (b"+" + fields[0], b"0" + fields[0], b" " + fields[0])),
                        (1, (b"+" + fields[1], b"0" + fields[1], fields[1] + b" ")),
                        (2, (b"+" + fields[2], b"0" + fields[2], fields[2] + b" ")),
                        (3, (b"", b"bad session", b"\xff")),
                        (4, (b"", b"fixture.extra", b"fixture\x00")),
                        (5, (b"", b"junk", b"2026-09-25T00:00:00",
                             b"2026-9-25T00:00:00Z", b"2026-02-30T00:00:00Z",
                             b"2026-09-25T24:00:00Z", b"2026-09-25T00:00:00Z\r"))):
                    for sample in samples:
                        changed = fields.copy()
                        changed[index] = sample
                        invalid.append(changed)
                for changed in invalid:
                    with self.subTest(fields=changed):
                        path.write_bytes(b"".join(rows[:2]) + b"\t".join(changed) + b"\n")
                        self.assertEqual(live_dispatch_groups(), 2)
                        self.assertEqual(self.outcome()[0], 2)

        def test_registry_unterminated_tail_preserves_complete_rows(self):
            with mock.patch.dict(globals(), _MAX_REGISTRY_ROWS=3):
                self.assertEqual(list(_registry_rows(io.BytesIO(b"a\nb\nc\nfragment"))),
                                 [b"a\n", b"b\n", b"c\n"])

        def test_process_identity_bounds(self):
            path = Path(self.registry.name, "killreg.%d" % os.geteuid())
            for sample, expected in ((1, 0), (2, 1), (4194304, 1), (4194305, 0)):
                with self.subTest(sample=sample):
                    path.write_text("%d\t%d\t1\t-\tfixture\t2026-09-25T00:00:00Z\n" % (sample, sample))
                    with mock.patch.dict(globals(), _group_is_live=mock.Mock(return_value=True)):
                        self.assertEqual(live_dispatch_groups(), expected)
                        if expected:
                            _group_is_live.assert_called_once_with(sample, 1, os.geteuid())
                        else:
                            _group_is_live.assert_not_called()

        def test_foreign_owner_blocks(self):
            with self.workers() as children:
                for owner in ("peer", "fixture.extra", "Fixture", ""):
                    self.record(children, owner=owner)
                    self.assertEqual(live_dispatch_groups(), 0)
                    self.assertEqual(self.outcome()[0], 2)
                # An unrelated owner's unreadable process must not mask our block.
                with mock.patch.dict(globals(), _group_is_live=mock.Mock(side_effect=PermissionError)):
                    self.assertEqual(live_dispatch_groups(), 0)

        def test_owner_default_and_explicit_values(self):
            with self.workers() as children:
                self.record(children, owner=pwd.getpwuid(os.geteuid()).pw_name)
                with mock.patch.dict(os.environ):
                    os.environ.pop("ORCH_OWNER", None)
                    self.assertEqual(live_dispatch_groups(), 3)
                # An explicit empty owner must not fall back to the recorded account name.
                with mock.patch.dict(os.environ, ORCH_OWNER=""):
                    self.assertEqual(live_dispatch_groups(), 0)
                    self.assertEqual(self.outcome()[0], 2)
                for owner in ("", "bad owner", "bad/owner", "caf\u00e9"):
                    with mock.patch.dict(os.environ, ORCH_OWNER=owner):
                        self.record(children, owner=owner)
                        self.assertEqual(live_dispatch_groups(), 0)
                        self.assertEqual(self.outcome()[0], 2)
                with mock.patch.dict(os.environ, ORCH_OWNER="sample.owner-2_3"):
                    self.record(children, owner="sample.owner-2_3")
                    self.assertEqual(live_dispatch_groups(), 3)

        def test_zombie_leaders_block(self):
            with self.workers() as children:
                for child in children:
                    os.killpg(child.pid, signal.SIGKILL)
                    # WNOWAIT observes exit without reaping the real timeout leader.
                    os.waitid(os.P_PID, child.pid, os.WEXITED | os.WNOWAIT)
                    data = Path("/proc/%d/stat" % child.pid).read_bytes()
                    self.assertEqual(data[data.rindex(b")") + 2:].split()[0], b"Z")
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_stopped_leaders_block(self):
            with self.workers() as children:
                self.assertEqual(live_dispatch_groups(), 3)
                for child in children:
                    os.kill(child.pid, signal.SIGSTOP)
                    deadline = time.monotonic() + 2
                    while True:
                        data = Path("/proc/%d/stat" % child.pid).read_bytes()
                        if data[data.rindex(b")") + 2:].split()[0] == b"T":
                            break
                        self.assertLess(time.monotonic(), deadline, "leader did not stop")
                        time.sleep(0.01)
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_traced_leaders_block(self):
            real_fdopen = os.fdopen
            def traced(fd, *args, **kwargs):
                stream = real_fdopen(fd, *args, **kwargs)
                if os.readlink("/proc/self/fd/%d" % fd).startswith("/proc/"):
                    with stream:
                        data = stream.read()
                    end = data.rindex(b")") + 2
                    fields = data[end:].split()
                    fields[0] = b"t"
                    return io.BytesIO(data[:end] + b" ".join(fields))
                return stream
            with self.workers():
                self.assertEqual(live_dispatch_groups(), 3)
                with mock.patch.object(os, "fdopen", side_effect=traced):
                    self.assertEqual(live_dispatch_groups(), 0)
                    self.assertEqual(self.outcome()[0], 2)

        def test_leaderless_groups_block(self):
            # --foreground keeps timeout in the shell's group instead of creating its own.
            with self.workers(command=["sh", "-c", "timeout --foreground 60 sleep 60 & wait"]) as children:
                rows = []
                for child in children:
                    descendants = Path("/proc/%d/task/%d/children" % (child.pid, child.pid))
                    deadline = time.monotonic() + 2
                    while True:
                        members = descendants.read_text().split()
                        if members:
                            data = Path("/proc/%s/stat" % members[0]).read_bytes()
                            if data[data.index(b"(") + 1:data.rindex(b")")] == b"timeout":
                                break
                        self.assertLess(time.monotonic(), deadline, "shell did not spawn timeout")
                        time.sleep(0.01)
                    child.kill()
                    child.wait()
                    # The surviving member satisfies every predicate except being the leader.
                    data = Path("/proc/%s/stat" % members[0]).read_bytes()
                    self.assertEqual(data[data.index(b"(") + 1:data.rindex(b")")], b"timeout")
                    rest = data[data.rindex(b")") + 2:].split()
                    self.assertNotIn(rest[0], (b"Z", b"X", b"x"))
                    self.assertEqual(int(rest[2]), child.pid)
                    self.assertEqual(Path("/proc/%s" % members[0]).stat().st_uid, os.geteuid())
                    self.surviving_members[child.pid] = int(members[0])
                    # Match the member's start time so that check cannot hide a missing leader check.
                    rows.append("%d\t%d\t%s\t-\tfixture\t2026-09-25T00:00:00Z\n" % (
                        child.pid, child.pid, rest[19].decode("ascii")))
                Path(self.registry.name, "killreg.%d" % os.geteuid()).write_text("".join(rows))
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_leaderless_mutation(self):
            nested = T("test_leaderless_groups_block")
            def member_path(pgid):
                return "/proc/%d" % nested.surviving_members[pgid]

            # Change only which proc directory is opened; retain uid, comm, state, pgid and start.
            source = textwrap.dedent(inspect.getsource(_group_is_live))
            seam = '"/proc/%d" % pgid'
            self.assertEqual(source.count(seam), 1)
            namespace = dict(globals(), _member_path=member_path)
            exec(compile(source.replace(seam, "_member_path(pgid)"),
                         "<leaderless mutation>", "exec"), namespace)
            result = self.assert_mutation_detected(
                nested, {"_group_is_live": namespace["_group_is_live"]}, ((3, 0),), 3)
            self.assertEqual(len(result.failures), 1, result.errors)
            self.assertFalse(result.errors)

        def test_leaderless_mutation_ignores_unrelated_read_errors(self):
            real_glob, real_read = Path.glob, Path.read_bytes
            sample = Path("/proc/0/stat")
            denied = []
            def glob(path, pattern, *args, **kwargs):
                if path == Path("/proc") and pattern == "[0-9]*/stat":
                    yield sample
                yield from real_glob(path, pattern, *args, **kwargs)
            def read(path):
                if path == sample:
                    denied.append(path)
                    raise PermissionError("sample unrelated procfs entry")
                return real_read(path)
            with mock.patch.object(Path, "glob", glob), mock.patch.object(Path, "read_bytes", read):
                self.test_leaderless_mutation()
            self.assertEqual(denied, [])

        def test_mutation_controls_reject_observation_errors(self):
            with self.assertRaises(AssertionError):
                self.assert_mutation_detected(
                    "test_stale_registry_blocks", {"live_dispatch_groups": lambda: None},
                    ((3, 0),), 3)
            # Even the intentional fail-open controls require their injected branch to run.
            with self.assertRaises(AssertionError):
                self.assert_mutation_detected(
                    "test_stale_registry_blocks", {"live_dispatch_groups": lambda: None},
                    ((None, 0),), None)

        def test_mutation_controls_reject_setup_failures(self):
            def broken_setup(nested):
                nested.fail("sample fixture setup failure")
            with mock.patch.object(T, "test_leaderless_groups_block", broken_setup):
                with self.assertRaises(AssertionError):
                    self.test_leaderless_mutation()

        def test_non_timeout_leaders_block(self):
            children = []
            try:
                for _ in range(3):
                    children.append(subprocess.Popen(
                        ["sleep", "60"], start_new_session=True,
                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                self.record(children)
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)
            finally:
                for child in children:
                    child.kill()
                    child.wait()

        def test_pgid_mismatch_blocks(self):
            real_fdopen = os.fdopen
            def regrouped(fd, *args, **kwargs):
                stream = real_fdopen(fd, *args, **kwargs)
                if os.readlink("/proc/self/fd/%d" % fd).startswith("/proc/"):
                    with stream:
                        data = stream.read()
                    end = data.rindex(b")") + 2
                    fields = data[end:].split()
                    fields[2] = str(int(fields[2]) + 1).encode()
                    return io.BytesIO(data[:end] + b" ".join(fields))
                return stream
            with self.workers(), mock.patch.object(os, "fdopen", side_effect=regrouped):
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_unreadable_registry_fails_open(self):
            Path(self.registry.name, "killreg.%d" % os.geteuid()).touch()
            real_open = os.open
            def denied(path, *args, **kwargs):
                if str(path).startswith(self.registry.name + os.sep):
                    raise PermissionError("fixture unreadable registry")
                return real_open(path, *args, **kwargs)
            with mock.patch.object(os, "open", side_effect=denied):
                self.assertIsNone(live_dispatch_groups())
                self.assertEqual(self.outcome()[0], 0)

        def test_unreadable_proc_blocks(self):
            real_open = os.open
            def denied(path, *args, **kwargs):
                if str(path).startswith("/proc/"):
                    raise PermissionError("sample unreadable group")
                return real_open(path, *args, **kwargs)
            with self.workers(), mock.patch.object(os, "open", side_effect=denied):
                self.assertEqual(live_dispatch_groups(), 0)
                self.assertEqual(self.outcome()[0], 2)

        def test_transient_lock_contention_retries(self):
            real_flock = fcntl.flock
            for count in (2, 3):
                with self.workers(count):
                    attempts = []
                    def contended(fd, flags):
                        attempts.append(flags)
                        if len(attempts) == 1:
                            raise BlockingIOError("sample transient writer")
                        return real_flock(fd, flags)
                    with mock.patch.object(fcntl, "flock", side_effect=contended):
                        self.assertEqual(live_dispatch_groups(), count)
                        self.assertEqual(len(attempts), 2)
                        self.assertTrue(all(f & fcntl.LOCK_NB for f in attempts))
                        attempts.clear()
                        self.assertEqual(self.outcome()[0], 2 if count == 2 else 0)

        def test_lock_contention_fails_open(self):
            with self.workers():
                path = Path(self.registry.name, "killreg.%d" % os.geteuid())
                with path.open("rb") as held:
                    fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    before = time.monotonic()
                    self.assertIsNone(live_dispatch_groups())
                    elapsed = time.monotonic() - before
                    self.assertGreaterEqual(elapsed, _LOCK_WAIT_SECONDS)
                    self.assertLess(elapsed, 2)
                    self.assertEqual(self.outcome()[0], 0)

        def test_individual_liveness_mutations(self):
            cases = (
                (_group_is_live, 'comm == b"timeout" and ', "", "test_non_timeout_leaders_block"),
                (_group_is_live, 'rest[0] not in (b"Z", b"X", b"x", b"T", b"t")',
                 "True", "test_zombie_leaders_block"),
                (_group_is_live, ', b"T"', "", "test_stopped_leaders_block"),
                (_group_is_live, ', b"t"', "", "test_traced_leaders_block"),
                (_group_is_live, "int(rest[2]) == pgid", "True", "test_pgid_mismatch_blocks"),
                (_group_is_live, "int(rest[19]) == start", "True", "test_reused_pid_blocks"),
                (_group_is_live, "os.fstat(fd).st_uid != uid", "False", "test_foreign_uid_groups_block"),
                (live_dispatch_groups, "fields[4] != owner", "False", "test_foreign_owner_blocks"),
                (live_dispatch_groups, "if owner is None:", "if not owner:",
                 "test_owner_default_and_explicit_values"),
            )
            for function, old, new, case in cases:
                source = textwrap.dedent(inspect.getsource(function))
                self.assertEqual(source.count(old), 1)
                namespace = dict(globals())
                exec(compile(source.replace(old, new), "<liveness mutation>", "exec"), namespace)
                mutant = types.FunctionType(namespace[function.__name__].__code__, globals())
                result = self.assert_mutation_detected(
                    case, {function.__name__: mutant}, ((3, 0),), 3)
                self.assertEqual(len(result.failures), 1, (case, result.errors))
                self.assertFalse(result.errors)

        def test_registry_mutations(self):
            cases = (
                (live_dispatch_groups, "if len(fields) != 6:\n            continue",
                 "if len(fields) != 6:\n            return _mutation_failure(None)",
                 "test_malformed_rows_do_not_mask_blocks_or_live_rows"),
                (live_dispatch_groups, "except ValueError:\n            continue",
                 "except ValueError:\n            return _mutation_failure(None)",
                 "test_malformed_rows_do_not_mask_blocks_or_live_rows"),
                (live_dispatch_groups, "if pgid <= 1 or pgid > _MAX_PID or leader != pgid or start < 0:\n            continue",
                 "if pgid <= 1 or pgid > _MAX_PID or leader != pgid or start < 0:\n            return _mutation_failure(None)",
                 "test_malformed_rows_do_not_mask_blocks_or_live_rows"),
                (live_dispatch_groups, " or pgid > _MAX_PID", "",
                 "test_process_identity_bounds"),
                (_lock_registry, "time.sleep(min(0.01, remaining))",
                 "return _mutation_failure(False)",
                 "test_transient_lock_contention_retries"),
            )
            for function, old, new, case in cases:
                source = textwrap.dedent(inspect.getsource(function))
                self.assertEqual(source.count(old), 1)
                faults = []
                def injected_failure(value):
                    faults.append(value)
                    return value
                namespace = dict(globals())
                exec(compile(source.replace(old, new), "<registry mutation>", "exec"), namespace)
                mutant = types.FunctionType(namespace[function.__name__].__code__, globals())
                bounded = case == "test_process_identity_bounds"
                result = self.assert_mutation_detected(
                    case, {function.__name__: mutant, "_mutation_failure": injected_failure},
                    ((1, 0),) if bounded else ((None, 0), (None, 2), (None, 3)),
                    1 if bounded else None, faults)
                self.assertTrue(result.failures, case)
                self.assertFalse(result.errors, (case, result.errors))

        def test_mutation_controls(self):
            # Execute the actual negative tests against deliberately broken production seams.
            for changes, case in (({"_MIN_LIVE_GROUPS": 1}, "test_below_floor_blocks"),
                                  ({"_group_is_live": lambda *args: True}, "test_stale_registry_blocks")):
                floor = case == "test_below_floor_blocks"
                result = self.assert_mutation_detected(
                    case, changes, ((0, 2),) if floor else ((3, 0),), 2 if floor else 3)
                self.assertEqual(len(result.failures), 1, (case, result.errors))
                self.assertFalse(result.errors)

        # ---- pure decision ----
        def test_decide_block_when_actionable(self):
            block, reason = decide("unattended", False, [("1", "a"), ("3", "c")])
            self.assertTrue(block)
            self.assertIn("actionable", reason)
            self.assertIn("reports 2 actionable open backlog item(s)", reason)
            self.assertIn(ACTIONABLE_PRODUCER, reason)
            self.assertNotIn("First in backlog order:", reason)
            self.assertNotIn("1: a", reason)

        # ---- message shape (Architect-directed 2026-09-24: at most 5 short lines, any item count) ----
        def _items(self, n, title="t"):
            return [(str(i), title) for i in range(1, n + 1)]

        def test_reason_at_most_five_lines_any_count(self):
            for n in (1, 2, 5, 6, 20, 21, 500):
                block, reason = decide("unattended", False, self._items(n))
                self.assertTrue(block)
                lines = reason.split("\n")
                self.assertLessEqual(len(lines), 5, "n=%d gave %d lines" % (n, len(lines)))

        def test_reason_lines_short_even_with_long_titles(self):
            for n in (1, 6, 500):
                block, reason = decide("unattended", False, self._items(n, "a long title " * 40))
                self.assertTrue(block)
                for line in reason.split("\n"):
                    self.assertLessEqual(len(line), 160, "n=%d line too long: %r" % (n, line))
                self.assertNotIn("a long title", reason)  # titles stay in the producer output

        def test_reason_carries_count_and_continue_instruction(self):
            with mock.patch.dict(globals(), _grc_escape_file=lambda: "/drop/.allow-idle-stop"):
                block, reason = decide("unattended", False, self._items(37))
            self.assertIn("reports 37 actionable open backlog item(s)", reason)
            self.assertNotIn("First in backlog order:", reason)
            self.assertNotIn("1, 2, 3, 4, 5", reason)
            self.assertIn(ACTIONABLE_PRODUCER, reason)
            self.assertIn("BLOCKED (stop-guard-unattended):", reason)
            self.assertIn("WHY:", reason)
            self.assertIn("CONSIDER INSTEAD:", reason)
            self.assertIn("continue on the highest-priority actionable item", reason)
            self.assertIn("10-TRUST-no-manufactured-winddown", reason)
            self.assertIn("[BLOCKED:<reason>]", reason)
            self.assertIn("set mode attended", reason)
            # The normal checkout path fits; very long overrides retain B's line clamp.
            self.assertIn("/drop/.allow-idle-stop", reason)
            self.assertTrue(reason.endswith("set mode attended."))

        def test_reason_does_not_claim_sole_legitimate_stop(self):
            block, reason = decide("unattended", False, self._items(3))
            self.assertTrue(block)
            self.assertNotIn("legitimately", reason)  # not framed as the only legitimate stop
            self.assertIn("at least 3 live owned dispatch groups", reason)
            self.assertIn("[BLOCKED:<reason>] tag with a granted approvals row", reason)  # grc's grammar (3b113 QA r2)
            # The complete await/exhaustion alternatives fit before the line clamp.
            line4 = reason.split("\n")[3]
            self.assertLessEqual(len(line4), 150, "line 4 has no margin under the 160 clamp: %r" % line4)

        def test_decide_allow_stop_hook_active(self):
            self.assertFalse(decide("unattended", True, [("1", "a")])[0])

        def test_decide_allow_exhausted(self):
            self.assertFalse(decide("unattended", False, [])[0])

        def test_decide_allow_indeterminate(self):
            self.assertFalse(decide("unattended", False, None)[0])

        def test_decide_allow_attended(self):
            self.assertFalse(decide("attended", False, [("1", "a")])[0])

        # ---- grc file-mode / executable-producer adapters + core (run) ----
        def test_unattended_actionable_blocks_end_to_end(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED)
                # actionable = items 1 and 3 (2 is granted-blocked)
                ids = [i for i, _ in actionable_items(d)]
                self.assertIn("1", ids)
                self.assertIn("3", ids)
                self.assertNotIn("2", ids)
                self.assertEqual(run(d, {"stop_hook_active": False}), 2)

        def test_unattended_all_blocked_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_ALL_BLOCKED)
                self.assertEqual(actionable_items(d), [])
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_unattended_empty_backlog_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_EMPTY)
                self.assertEqual(actionable_items(d), [])
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_unattended_stop_hook_active_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED)  # actionable present, but continuation -> allow
                self.assertEqual(run(d, {"stop_hook_active": True}), 0)

        def test_attended_allows_even_with_actionable(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=ATT, producer_lines=ITEMS_MIXED)
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_no_mode_file_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, producer_lines=ITEMS_MIXED)  # no mode file -> indeterminate -> allow
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        def test_failed_producer_fails_open(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED, producer_exit=2)
                self.assertIsNone(actionable_items(d))
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)

        # ---- production ENTRY point via subprocess: real exit protocol + __file__-root beats a hostile
        # payload root (a regression restoring payload-trust would otherwise ship green) ----
        def _subproc(self, mode, producer_lines, payload):
            import subprocess
            with tempfile.TemporaryDirectory() as d:
                hooks = os.path.join(d, ".claude", "hooks")
                os.makedirs(hooks)
                source = Path(__file__).read_text()
                seam = '_KILLREG_DIR = "/run/orch-workers"'
                self.assertEqual(source.count(seam + "\n"), 1)
                Path(hooks, "hook.py").write_text(source.replace(
                    seam + "\n", "_KILLREG_DIR = %r\n" % self.registry.name))
                build(d, mode=mode, producer_lines=producer_lines)
                with tempfile.TemporaryDirectory() as foreign:
                    r = subprocess.run([sys.executable, os.path.join(hooks, "hook.py")],
                                       input=payload, capture_output=True, text=True, cwd=foreign)
                    return r.returncode

        def test_subprocess_unattended_actionable_blocks_ignoring_hostile_payload_root(self):
            payload = _json.dumps({"stop_hook_active": False, "workspace": {"project_dir": "/nonexistent-attended"}})
            self.assertEqual(self._subproc(UNATT, ITEMS_MIXED, payload), 2)

        def test_subprocess_stop_hook_active_allows(self):
            payload = _json.dumps({"stop_hook_active": True})
            self.assertEqual(self._subproc(UNATT, ITEMS_MIXED, payload), 0)

        def test_subprocess_empty_stdin_allows(self):
            # empty stdin is an absent/uncertain payload -> fail open (allow), even unattended + actionable.
            self.assertEqual(self._subproc(UNATT, ITEMS_MIXED, ""), 0)

        # ---- orchestrator-vs-worker scoping (the guard binds the orchestrator only) ----
        def test_is_orchestrator_truth_table(self):
            self.assertTrue(_is_orchestrator(1011, 1011, False))    # owner session, no worker marker -> fire
            self.assertFalse(_is_orchestrator(1011, 1011, True))    # ORCH_VERIFY_OWNER set -> worker -> allow
            self.assertFalse(_is_orchestrator(2020, 1011, False))   # euid != owner -> worker -> allow
            self.assertFalse(_is_orchestrator(None, 1011, False))   # unknown euid -> fail open
            self.assertFalse(_is_orchestrator(1011, None, False))   # unknown owner -> fail open

        def test_worker_env_marker_allows_end_to_end(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED)  # unattended + actionable, but a verify-worker env
                try:
                    os.environ["ORCH_VERIFY_OWNER"] = "lab_infra.1234"
                    self.assertFalse(is_orchestrator_session(d))
                    self.assertEqual(run(d, {"stop_hook_active": False}), 0)
                    os.environ["ORCH_VERIFY_OWNER"] = ""  # even an EMPTY marker means a worker exported it
                    self.assertFalse(is_orchestrator_session(d))
                    self.assertEqual(run(d, {"stop_hook_active": False}), 0)
                    os.environ.pop("ORCH_VERIFY_OWNER", None)
                    os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(d, "orch-worker.example")  # 3b113 QA r1
                    self.assertFalse(is_orchestrator_session(d))
                    self.assertEqual(run(d, {"stop_hook_active": False}), 0)
                finally:
                    os.environ.pop("ORCH_VERIFY_OWNER", None)
                    os.environ.pop("CLAUDE_CONFIG_DIR", None)

        # ---- payload robustness (uncertain payload -> fail open) ----
        def test_parse_payload(self):
            self.assertIsNone(_parse_payload(""))
            self.assertIsNone(_parse_payload("   "))
            self.assertIsNone(_parse_payload("{ not json"))
            self.assertIsNone(_parse_payload("[1, 2, 3]"))       # JSON non-object
            self.assertIsNone(_parse_payload('"a string"'))
            self.assertEqual(_parse_payload('{"stop_hook_active": true}'), {"stop_hook_active": True})

        def test_subprocess_non_object_payload_allows(self):
            self.assertEqual(self._subproc(UNATT, ITEMS_MIXED, "[1,2,3]"), 0)

        def test_subprocess_malformed_payload_allows(self):
            self.assertEqual(self._subproc(UNATT, ITEMS_MIXED, "{ not json"), 0)

        def test_unknown_mode_file_allows(self):
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unknown-mode", producer_lines=ITEMS_MIXED)  # unknown mode -> not unattended -> allow
                self.assertEqual(run(d, {"stop_hook_active": False}), 0)


    class GRCAdapterTests(unittest.TestCase):
        # A's adapter cases also isolate the new registry from the host.
        setUp = T.setUp

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
                    for suffix in ("", "/", "/."):  # every spelling Path(...).name reads as the dir (3b101 QA r5)
                        os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(d, "orch-worker.example") + suffix
                        self.assertFalse(_grc_consume_escape(_GRC_REPO_ROOT), suffix)
                        self.assertTrue(os.path.exists(sentinel), suffix)
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
                for a in (wt_admin, os.path.join(parent, ".git", "modules", "sub"),
                          os.path.join(parent, "worktrees", "modules", "sub-deep")):
                    open(os.path.join(a, "HEAD"), "w").close()  # every git directory holds HEAD
                os.makedirs(os.path.join(parent, "wt-alias"))
                os.symlink(os.path.join(parent, "grc_library", ".git", "worktrees"),
                           os.path.join(parent, "wt-alias", "worktrees"))
                layouts = {"grc_library": None, "wt-x": f"gitdir: {wt_admin}\n",
                           "wt-alias": "gitdir: worktrees/wt-x\n", "sub": "gitdir: ../.git/modules/sub\n",
                           "sub-deep": f"gitdir: {os.path.join(parent, 'worktrees', 'modules', 'sub-deep')}\n",
                           "missing": "gitdir: ../nowhere\n",
                           # 3b101 QA r4: a gitdir naming a file, no .git at all, and an unsearchable admin dir
                           "file-target": f"gitdir: {os.path.join(parent, 'admin-file')}\n", "no-git": "",
                           # 3b101 QA r5: a directory that is not a git directory, an empty target, no prefix
                           "not-admin": "gitdir: .\n", "empty-target": "gitdir:   \n", "no-prefix": "hello\n",
                           "nul-target": "gitdir: ../x\x00y\n",
                           # 3b101 QA r6: a dangling symlinked HEAD is still a git directory; no space is not a gitfile
                           "sub-symhead": f"gitdir: {os.path.join(parent, 'symhead')}\n",
                           "no-space": f"gitdir:{os.path.join(parent, '.git', 'modules', 'sub')}\n"}
                os.makedirs(os.path.join(parent, "symhead"))
                os.symlink("refs/heads/main", os.path.join(parent, "symhead", "HEAD"))
                open(os.path.join(parent, "admin-file"), "w").close()
                locked = os.path.join(parent, "locked-admin")
                os.makedirs(locked)
                open(os.path.join(locked, "commondir"), "w").close()
                open(os.path.join(locked, "HEAD"), "w").close()
                check_locked = os.geteuid() != 0  # root traverses a mode-000 directory anyway
                if check_locked:
                    layouts["wt-locked"] = f"gitdir: {locked}\n"
                got = {}
                for name, gitfile in layouts.items():
                    r = os.path.join(parent, name)
                    os.makedirs(os.path.join(r, ".claude", "hooks"))
                    hook = os.path.join(r, ".claude", "hooks", os.path.basename(__file__))
                    shutil.copy(__file__, hook)
                    if gitfile is None:
                        os.makedirs(os.path.join(r, ".git"), exist_ok=True)
                    elif gitfile == "":
                        pass
                    else:
                        with open(os.path.join(r, ".git"), "w", encoding="utf-8") as fh:
                            fh.write(gitfile)
                    env = {k: v for k, v in os.environ.items()
                           if k not in ("GRC_STORE", "ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}
                    code = ("import runpy,sys; m=runpy.run_path(sys.argv[1]); "
                            "print(m['read_operating_mode'](m['repo_root']()))")
                    if name == "wt-locked":
                        os.chmod(locked, 0)
                    try:
                        out = subprocess.run([sys.executable, "-B", "-c", code, hook], capture_output=True,
                                             text=True, env=env, timeout=60)
                    finally:
                        os.chmod(locked, 0o755)
                    got[name] = out.stdout.strip()
                want = {"grc_library": "unattended", "wt-x": "None", "wt-alias": "None", "sub": "unattended",
                        "sub-deep": "unattended", "missing": "None", "file-target": "None", "no-git": "None",
                        "not-admin": "None", "empty-target": "None", "no-prefix": "None", "nul-target": "None",
                        "sub-symhead": "unattended", "no-space": "None"}
                if check_locked:
                    want["wt-locked"] = "None"
                self.assertEqual(got, want, got)
                # A worker in the main checkout is never armed by the lease (3b101 QA r3).
                hook = os.path.join(parent, "grc_library", ".claude", "hooks", os.path.basename(__file__))
                env["CLAUDE_CONFIG_DIR"] = os.path.join(parent, "orch-worker.example")
                out = subprocess.run([sys.executable, "-B", "-c", code, hook], capture_output=True, text=True,
                                     env=env, timeout=60)
                self.assertEqual(out.stdout.strip(), "None", out.stderr)
                # A stray file-based mode record never shadows the lease in the main checkout (3b113 QA r2).
                env.pop("CLAUDE_CONFIG_DIR")
                main = os.path.join(parent, "grc_library")
                os.makedirs(os.path.join(main, ".working"))
                with open(os.path.join(main, MODE_FILE), "w", encoding="utf-8") as fh:
                    fh.write("attended\n")
                out = subprocess.run([sys.executable, "-B", "-c", code, hook], capture_output=True, text=True,
                                     env=env, timeout=60)
                self.assertEqual(out.stdout.strip(), "unattended", out.stderr)

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


    class ObservationTests(unittest.TestCase):
        @contextlib.contextmanager
        def groups(self, count=3):
            children = []
            try:
                for _ in range(count):
                    children.append(subprocess.Popen(
                        ["timeout", "60", "sleep", "60"], start_new_session=True,
                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL))
                rows = []
                for child in children:
                    data = Path("/proc/%d/stat" % child.pid).read_bytes()
                    start = int(data[data.rindex(b")") + 2:].split()[19])
                    rows.append(("%d\t%d\t%d\t-\tfixture\t2026-09-25T00:00:00Z\n" % (
                        child.pid, child.pid, start)).encode())
                yield children, rows
            finally:
                for child in children:
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()

        @contextlib.contextmanager
        def registry(self, data, stream_type=io.BytesIO):
            # Exercise registry opening and parsing without writing a fixture file.
            real_open, real_fdopen, real_fstat = os.open, os.fdopen, os.fstat
            real_pread = os.pread
            path = os.path.join(_KILLREG_DIR, "killreg.%d" % os.geteuid())
            metadata = types.SimpleNamespace(
                st_uid=os.geteuid(), st_mode=stat.S_IFREG, st_size=len(data))
            stream = stream_type(data)
            stream.fileno = lambda: -1
            def opened(candidate, *args, **kwargs):
                return -1 if candidate == path else real_open(candidate, *args, **kwargs)
            def fdopened(fd, *args, **kwargs):
                return stream if fd == -1 else real_fdopen(fd, *args, **kwargs)
            def fstatted(fd):
                return metadata if fd == -1 else real_fstat(fd)
            def pread(fd, size, offset):
                return data[offset:offset + size] if fd == -1 else real_pread(fd, size, offset)
            with mock.patch.dict(os.environ, ORCH_OWNER="fixture"), \
                    mock.patch.object(os, "lstat", return_value=metadata), \
                    mock.patch.object(os, "open", side_effect=opened), \
                    mock.patch.object(os, "fdopen", side_effect=fdopened), \
                    mock.patch.object(os, "fstat", side_effect=fstatted), \
                    mock.patch.object(os, "pread", side_effect=pread), \
                    mock.patch.object(fcntl, "flock"):
                yield stream

        def assert_observation(self, data, expected, stream_type=io.BytesIO):
            with self.registry(data, stream_type):
                count = live_dispatch_groups()
            self.assertEqual(count, expected)
            block, _ = decide("unattended", False, [("1", "sample")], count)
            self.assertEqual(block, expected is not None and expected < 3)

        def test_registry_timestamps_do_not_license_yield(self):
            with self.groups() as (_children, rows):
                for sample, expected in (
                        (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()).encode(), 3),
                        (b"2026-09-26T11:59:59Z", 3),
                        (b"2026-09-26T11:59:60Z", 2),
                        (b"2026-09-26T11:59:61Z", 2),
                        (b"2026-09-26T24:00:00Z", 2),
                        (b"2026-02-30T00:00:00Z", 2),
                        (b"2026-9-26T11:59:59Z", 2)):
                    with self.subTest(sample=sample):
                        changed = rows[2].rsplit(b"\t", 1)[0] + b"\t" + sample + b"\n"
                        data = b"".join(rows[:2]) + changed
                        self.assert_observation(data, expected)
                        with self.registry(data), mock.patch.dict(
                                globals(), is_orchestrator_session=lambda root: True,
                                read_operating_mode=lambda root: "unattended",
                                actionable_items=lambda root: [("1", "sample")],
                                _diagnostic=mock.Mock()):
                            self.assertEqual(run(root_real, {"stop_hook_active": False}),
                                             2 if expected == 2 else 0)

        def test_registry_size_boundaries(self):
            with self.groups() as (_children, rows):
                for size in (1048576, 1048577):
                    for count in (0, 2, 3):
                        good = b"".join(rows[:count])
                        padding = b"x" * (size - len(good) - 1) + b"\n"
                        for data in (good + padding, padding + good):
                            with self.subTest(size=size, count=count, prefix=data == padding + good):
                                self.assertEqual(len(data), size)
                                self.assert_observation(data, count)

        def test_registry_row_length_and_fragment_boundaries(self):
            with self.groups() as (_children, rows):
                for size in (_MAX_REGISTRY_ROW_BYTES, _MAX_REGISTRY_ROW_BYTES + 1):
                    # A valid row at the length limit counts; one byte over does not.
                    fields = rows[0][:-1].split(b"\t")
                    fields[3] = b"x" * (size - len(rows[0]) + 1)
                    padded = b"\t".join(fields) + b"\n"
                    self.assertEqual(len(padded), size)
                    expected = 1 if size == _MAX_REGISTRY_ROW_BYTES else 0
                    self.assert_observation(padded, expected)
                # A valid-looking fragment inside an oversized row is still that row.
                for count in (0, 2, 3):
                    oversized = b"x" * (_MAX_REGISTRY_ROW_BYTES + 1) + rows[0]
                    self.assert_observation(oversized + b"".join(rows[:count]), count)

        def test_registry_row_count_and_bounded_reads(self):
            with self.groups() as (_children, rows):
                for count in (0, 2, 3):
                    data = b"".join(rows[:count]) + b"\n" * (_MAX_REGISTRY_ROWS - count)
                    # Appended live rows remain visible after a full retention window.
                    self.assert_observation(data + b"".join(rows), 3)
                for stale in (b"\n", b"bad\n", b"2\t2\t0\t-\tpeer\n"):
                    self.assert_observation(stale * (_MAX_REGISTRY_ROWS + 1)
                                            + b"".join(rows), 3)
                with mock.patch.dict(globals(), _MAX_REGISTRY_ROWS=2):
                    self.assertEqual(list(_registry_rows(io.BytesIO(b"a\nb\nc\n"))),
                                     [b"b\n", b"c\n"])
                stream = io.BytesIO(b"x" * (_MAX_REGISTRY_ROW_BYTES * 3) + b"\n" + rows[0])
                with mock.patch.object(stream, "readline", wraps=stream.readline) as read:
                    self.assertEqual(list(_registry_rows(stream)), [rows[0]])
                self.assertTrue(read.call_args_list)
                self.assertTrue(all(call.args == (_MAX_REGISTRY_ROW_BYTES + 1,)
                                    for call in read.call_args_list))

        def test_registry_scan_budget_sparse_files(self):
            real_open, real_fdopen, real_lstat = os.open, os.fdopen, os.lstat
            real_pread = os.pread
            path = os.path.join(_KILLREG_DIR, "killreg.%d" % os.geteuid())
            with self.groups() as (_children, rows):
                for expected in (0, 2, 3):
                    with self.subTest(expected=expected):
                        # Anonymous regular files exercise real sparse reads and flock without
                        # allocating a terabyte or depending on the filesystem under TMPDIR.
                        with real_fdopen(os.memfd_create("sample", os.MFD_CLOEXEC),
                                         "w+b", buffering=0) as sample:
                            sample.write(b"".join(rows[:expected]))
                            sample.truncate(1 << 40)
                            good = b"".join(rows[:expected])
                            if good:
                                sample.seek((1 << 40) - len(good) - 1)
                                sample.write(b"\n" + good)
                            sample_path = "/proc/self/fd/%d" % sample.fileno()
                            metadata = os.fstat(sample.fileno())
                            self.assertEqual(metadata.st_uid, os.geteuid())
                            self.assertEqual(metadata.st_size, 1 << 40)
                            registry_fds, consumed = set(), []
                            with real_fdopen(real_open(sample_path, os.O_RDONLY), "rb") as writer:
                                def opened(candidate, flags, *args, **kwargs):
                                    if candidate == path:
                                        fd = real_open(sample_path, os.O_RDONLY | os.O_CLOEXEC)
                                        registry_fds.add(fd)
                                        return fd
                                    return real_open(candidate, flags, *args, **kwargs)

                                test = self
                                class Counted:
                                    def __init__(self, stream):
                                        self.stream = stream

                                    def __enter__(self):
                                        return self

                                    def __exit__(self, *args):
                                        return self.stream.__exit__(*args)

                                    def fileno(self):
                                        return self.stream.fileno()

                                    def seek(self, offset):
                                        self.offset = offset
                                        test.assertEqual(offset,
                                                         (1 << 40) - _MAX_REGISTRY_SCAN_BYTES)
                                        with test.assertRaises(BlockingIOError):
                                            fcntl.flock(writer.fileno(),
                                                        fcntl.LOCK_EX | fcntl.LOCK_NB)
                                        # Simulate growth after the locked size snapshot. The
                                        # budget must still hold if a writer ignores the lock.
                                        sample.seek(0, os.SEEK_END)
                                        sample.write(b"x")
                                        return self.stream.seek(offset)

                                    def readline(self, size):
                                        if not consumed:
                                            with test.assertRaises(BlockingIOError):
                                                fcntl.flock(writer.fileno(),
                                                            fcntl.LOCK_EX | fcntl.LOCK_NB)
                                        line = self.stream.readline(size)
                                        consumed.append(len(line))
                                        test.assertLessEqual(sum(consumed),
                                                             _MAX_REGISTRY_SCAN_BYTES,
                                                             "registry scan byte budget")
                                        # Include buffered read-ahead in the physical I/O bound.
                                        test.assertLessEqual(
                                            os.lseek(self.fileno(), 0, os.SEEK_CUR) - self.offset,
                                            _MAX_REGISTRY_SCAN_BYTES,
                                            "registry scan read-ahead budget")
                                        return line

                                def fdopened(fd, *args, **kwargs):
                                    stream = real_fdopen(fd, *args, **kwargs)
                                    if fd in registry_fds:
                                        registry_fds.remove(fd)
                                        return Counted(stream)
                                    return stream

                                def lstatted(candidate, *args, **kwargs):
                                    if candidate == path:
                                        return metadata
                                    return real_lstat(candidate, *args, **kwargs)

                                boundary_reads = []
                                def pread(fd, size, offset):
                                    test.assertEqual(size, 1)
                                    test.assertEqual(offset,
                                                     (1 << 40) - _MAX_REGISTRY_SCAN_BYTES - 1)
                                    with test.assertRaises(BlockingIOError):
                                        fcntl.flock(writer.fileno(),
                                                    fcntl.LOCK_EX | fcntl.LOCK_NB)
                                    data = real_pread(fd, size, offset)
                                    boundary_reads.append(data)
                                    return data

                                with mock.patch.dict(os.environ, ORCH_OWNER="fixture"), \
                                        mock.patch.object(os, "lstat", side_effect=lstatted), \
                                        mock.patch.object(os, "open", side_effect=opened), \
                                        mock.patch.object(os, "fdopen", side_effect=fdopened), \
                                        mock.patch.object(os, "pread", side_effect=pread):
                                    count = live_dispatch_groups()
                                self.assertEqual(boundary_reads, [b"\0"])
                                self.assertEqual(count, expected)
                                self.assertEqual(sum(consumed), _MAX_REGISTRY_SCAN_BYTES)
                                self.assertEqual(
                                    decide("unattended", False, [("1", "sample")], count)[0],
                                    expected < 3)
                                # The read descriptor, and therefore its shared lock, is gone.
                                fcntl.flock(writer.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

        def test_registry_scan_budget_boundaries(self):
            with self.groups() as (_children, rows):
                good = b"".join(rows)
                for padding in (b"", b"bad\n" * 20,
                                b"x" * (_MAX_REGISTRY_ROW_BYTES + 1) + b"\n"):
                    data = padding + good
                    for cut in (len(data) - 1, len(data), len(data) + 1):
                        with self.subTest(padding=len(padding), cut=cut), \
                                mock.patch.dict(globals(), _MAX_REGISTRY_SCAN_BYTES=cut):
                            # Exercise the forward scanner at a fixed offset independently
                            # of the observer's choice of a tail window.
                            stream = io.BytesIO(data + b"x" * 20)
                            retained = b"".join(_registry_rows(stream))
                            self.assert_observation(retained, 2 if cut < len(data) else 3)
                            self.assertEqual(stream.tell(), cut)
                # Fragments that resemble valid rows cannot become observations.
                data = b"x" * (_MAX_REGISTRY_ROW_BYTES + 1) + rows[0]
                with mock.patch.dict(globals(), _MAX_REGISTRY_SCAN_BYTES=len(data) - 1):
                    retained = b"".join(_registry_rows(io.BytesIO(data + good)))
                    self.assert_observation(retained, 0)

        def test_registry_scan_budget_mutation(self):
            source = textwrap.dedent(inspect.getsource(_registry_rows))
            seam = "remaining -= len(line)"
            self.assertEqual(source.count(seam), 1)
            namespace = dict(globals())
            exec(compile(source.replace(seam, "pass"), "<scan mutation>", "exec"), namespace)
            with mock.patch.dict(globals(), _registry_rows=namespace["_registry_rows"]):
                result = unittest.TestResult()
                ObservationTests("test_registry_scan_budget_sparse_files").run(result)
            self.assertFalse(result.errors, result.errors)
            self.assertEqual(len(result.failures), 3, result.failures)
            self.assertTrue(all("registry scan byte budget" in detail
                                for _case, detail in result.failures), result.failures)

        def test_registry_lock_deadline(self):
            # The existing 0.2-second limit applies even if a writer never releases.
            with mock.patch.object(fcntl, "flock", side_effect=BlockingIOError), \
                    mock.patch.object(time, "monotonic", side_effect=(0, 0, _LOCK_WAIT_SECONDS)), \
                    mock.patch.object(time, "sleep") as sleep:
                self.assertFalse(_lock_registry(-1))
                self.assertEqual(fcntl.flock.call_count, 2)
                self.assertTrue(all(call.args[1] & fcntl.LOCK_NB
                                    for call in fcntl.flock.call_args_list))
                sleep.assert_called_once_with(0.01)

        def test_registry_aligned_tail_stop(self):
            with self.groups() as (_children, rows):
                good = b"".join(rows)
                with mock.patch.dict(globals(), _MAX_REGISTRY_SCAN_BYTES=len(good)), \
                        self.registry(b"xxxx\n" + good), \
                        mock.patch.dict(globals(),
                                        is_orchestrator_session=lambda root: True,
                                        read_operating_mode=lambda root: "unattended",
                                        actionable_items=lambda root: [("1", "sample")]), \
                        capture_stderr(io.StringIO()) as stderr:
                    self.assertEqual(run(root_real, {"stop_hook_active": False}), 0)
                self.assertIn("3 live owned dispatch groups", stderr.getvalue())

        def test_registry_tail_windows(self):
            with self.groups() as (_children, rows):
                for stale in (b"\n", b"bad row\n", b"2\t2\t0\t-\tpeer\n"):
                    padding = stale * (_MAX_REGISTRY_SCAN_BYTES // len(stale) + 1)
                    self.assertGreater(len(padding), _MAX_REGISTRY_SCAN_BYTES)
                    for count in (1, 2, 3):
                        with self.subTest(stale=stale, count=count):
                            self.assert_observation(padding + b"".join(rows[:count]), count)
                good = b"".join(rows)
                # Keep complete rows at a boundary; discard only an initial fragment.
                # The preceding byte has its own allowance outside the row budget.
                for prefix, window, expected in (
                        (b"x", good, 2),
                        (b"xx", good, 2),
                        (b"x", b"\n" + good, 3),
                        (b"xx", b"\n" + good, 3),
                        (b"x\n", good, 3)):
                    with self.subTest(prefix=prefix, expected=expected), \
                            mock.patch.dict(globals(), _MAX_REGISTRY_SCAN_BYTES=len(window)):
                        self.assert_observation(prefix + window, expected)
                        with self.registry(prefix + window) as stream:
                            retained = b"".join(_registry_rows(stream, len(prefix)))
                        self.assert_observation(retained, expected)
                # Unknown boundaries discard just the first row, including after a short read.
                for failure in (OSError, ValueError, None):
                    with self.subTest(boundary_failure=failure), \
                            mock.patch.dict(globals(), _MAX_REGISTRY_SCAN_BYTES=len(good)), \
                            self.registry(b"x\n" + good), \
                            mock.patch.object(os, "pread", side_effect=failure,
                                              return_value=b"") as read:
                        count = live_dispatch_groups()
                        self.assertEqual(count, 2)
                        self.assertTrue(decide("unattended", False, [("1", "sample")], count)[0])
                        read.assert_called_once_with(-1, 1, 1)
                # Size must be sampled again after locking, not from the earlier metadata.
                with self.registry(b"bad\n" * _MAX_REGISTRY_SCAN_BYTES + good):
                    fstatted = os.fstat.side_effect
                    def metadata(fd):
                        value = fstatted(fd)
                        if fd == -1 and not fcntl.flock.called:
                            return types.SimpleNamespace(
                                st_uid=value.st_uid, st_mode=value.st_mode, st_size=0)
                        return value
                    os.fstat.side_effect = metadata
                    self.assertEqual(live_dispatch_groups(), 3)
                for failure in (OSError, ValueError):
                    class FailedSeek(io.BytesIO):
                        def seek(self, *args):
                            raise failure("sample registry seek failure")
                    with self.subTest(failure=failure):
                        self.assert_observation(good, None, FailedSeek)

        def test_proc_observation_failures(self):
            real_fdopen = os.fdopen
            with self.groups(4) as (children, rows):
                target = "/proc/%d/stat" % children[0].pid
                original = Path(target).read_bytes()
                end = original.rindex(b")") + 2
                fields = original[end:].split()
                bad_number = fields.copy()
                bad_number[19] = b"sample"
                samples = (b"", b"sample", b"1 (timeout)", original[:end],
                           original[:end] + b" ".join(fields[:3]),
                           original[:end] + b" ".join(bad_number))
                class FailedRead(io.BytesIO):
                    def read(self, *args):
                        raise failure("sample proc read failure")
                for sample in (*samples, FileNotFoundError, ProcessLookupError,
                               PermissionError, OSError):
                    failure = sample
                    def fdopened(fd, *args, **kwargs):
                        stream = real_fdopen(fd, *args, **kwargs)
                        if os.readlink("/proc/self/fd/%d" % fd) == target:
                            stream.close()
                            return (io.BytesIO(sample) if isinstance(sample, bytes)
                                    else FailedRead())
                        return stream
                    for count in (0, 2, 3):
                        with self.subTest(sample=sample, count=count), \
                                mock.patch.object(os, "fdopen", side_effect=fdopened):
                            self.assert_observation(rows[0] + b"".join(rows[1:count + 1]), count)

        def test_proc_open_failures(self):
            real_open = os.open
            with self.groups() as (children, rows):
                target = "/proc/%d" % children[0].pid
                for failure in (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
                    def opened(path, *args, **kwargs):
                        if path == target or path == "stat":
                            raise failure("sample proc open failure")
                        return real_open(path, *args, **kwargs)
                    with self.subTest(failure=failure), \
                            mock.patch.object(os, "open", side_effect=opened):
                        self.assert_observation(b"".join(rows), 0)

        def test_registry_read_failure_still_allows(self):
            class FailedRead(io.BytesIO):
                def readline(self, *args):
                    if self.tell():
                        raise OSError("sample registry read failure")
                    return super().readline(*args)
            self.assert_observation(b"bad row\nremaining\n", None, FailedRead)

        def test_unresolved_default_owner_blocks(self):
            for failure in (KeyError, OSError):
                with self.registry(b""), mock.patch.dict(os.environ), \
                        mock.patch.object(pwd, "getpwuid", side_effect=failure):
                    os.environ.pop("ORCH_OWNER", None)
                    count = live_dispatch_groups()
                    self.assertEqual(count, 0)
                    self.assertTrue(decide("unattended", False, [("1", "sample")], count)[0])

        def test_observation_mutations(self):
            faults = []
            def fail_open(value):
                faults.append(value)
                return value
            source = textwrap.dedent(inspect.getsource(live_dispatch_groups))
            seam = "rows = list(_registry_rows(stream, offset))"
            self.assertEqual(source.count(seam), 1)
            namespace = dict(globals(), _mutation_failure=fail_open)
            exec(compile(source.replace(seam,
                         "if st.st_size > 1048576: return _mutation_failure(None)\n"
                         "            " + seam), "<size mutation>", "exec"), namespace)
            T.assert_mutation_detected(
                self, ObservationTests("test_registry_size_boundaries"),
                {"live_dispatch_groups": namespace["live_dispatch_groups"]},
                ((None, 0), (None, 2), (None, 3)), None, faults)

            source = textwrap.dedent(inspect.getsource(_group_is_live))
            seam = "return False  # a failed group observation cannot invalidate the registry"
            self.assertEqual(source.count(seam), 1)
            exec(compile(source.replace(seam, "raise"), "<proc mutation>", "exec"), namespace)
            original_count = live_dispatch_groups
            def broad_handler():
                try:
                    return original_count()
                except (OSError, ValueError, IndexError):
                    return fail_open(None)
            faults.clear()
            T.assert_mutation_detected(
                self, ObservationTests("test_proc_observation_failures"),
                {"_group_is_live": namespace["_group_is_live"],
                 "live_dispatch_groups": broad_handler},
                ((None, 0), (None, 2), (None, 3)), None, faults)

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(
        unittest.TestLoader().loadTestsFromTestCase(case) for case in (T, GRCAdapterTests, ObservationTests)))
    for k, v in _saved_env.items():
        if v is not None:
            os.environ[k] = v
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
