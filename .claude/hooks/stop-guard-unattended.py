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
  4. At least max(operator slot share, _MIN_LIVE_GROUPS=3) live owned dispatch groups -> allow
     dispatch-and-await, with a note naming the share source or fallback cause.
     Registry read failure -> allow, except a boundary-byte failure discards the first row and
     continues counting; missing registry means zero groups.
  5. Otherwise -> BLOCK (exit 2). decide() renders the actionable count, producer command, rule and
     escape under B's five-line/160-character clamps; run() routes that text as described under
     CONSOLE AND DETAIL LOG below, so the console carries the count, the detail log path and the
     declared-wait escape path (#2496), and the producer command and rule reach the console only
     on the fallback path. Item IDs and titles never reach the console (#2291); only the detail
     log holds them.

Fail-OPEN. On failure to determine the mode or the actionable set, the hook ALLOWS the stop. A
guard that traps the actor on its own malfunction protects nothing; a convenience guardrail that
wrongly blocks a legitimate stop is worse than the mistake it prevents. An unusable share file
never blocks a stop that the floor of 3 would allow.

PORTABILITY. The ADAPTER SEAM contains grc's lease-mode, producer and generic owner adapters,
plus grc path, checkout, worker and one-shot helpers. main() also carries the one-shot escape
pre-step. The registry observer, decision predicates, run() and payload parsing are from
lab_infra commit 17b407b9 (PR #952, item 373); decide() and run() additionally carry the
3b286 operator slot-share floor (max(share, 3)). Diagnostic transport carries 3b226's
connected-socket syscall adaptation below. decide()'s block text carries P-1.36 (BLOCKED / WHY /
CONSIDER INSTEAD), #2291 (count only, producer on demand), #2496 (resolved declared-wait path)
and 3b286 (required live count); since 2026-11-04 that text goes to the detail log, and the
console shows it only on the fallback path (CONSOLE AND DETAIL LOG below), except that the
short form still names the resolved declared-wait path (#2496). MODE_SET_HINT retains
the detailed grc guidance; the emitted hint is shortened to fit B's message format. B's
per-line clamp never cuts the declared-wait command: an override path too long for that line
leaves it naming the sentinel and the directory setting the hook used without a command
(_declared_wait_line; hook escaping round 4, codex W1). The detail log carries the whole
command when it is written; when it is not, the fallback's line says so instead of pointing
at the log (_fallback_refusal; round 5, claude W1).

GRC ADAPTATION (2026-09-27; backlog 3b113). Rebased the 2026-09-03 cross-project adoption
(inbox msg 20260903T002018Z.from-lab_infra) onto lab_infra 17b407b9, adding the live-dispatch
allowance and bounded diagnostic transport. read_operating_mode in the grc checkout reads the
fleet mode file FIRST through the shared reader .claude/hooks/_operating_mode.py and then the
lease's dated #5(b) swap (3b781, _grc_effective_mode), mapped via _grc_map_mode; a
reader-load failure or reader exception FAILS CLOSED to the armed 'unattended' (3b781 r2:
the lease never outranks the fleet file, and the AskUserQuestion hook fails closed on the
same condition). main() consumes .allow-idle-stop before parsing the payload. Lease and escape
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
cannot count. max(operator slot share, three) groups is the required proxy (three remains the
D-295 floor), not proof of distinct workstreams or progress. Unrecorded/no-timeout dispatches
and leaderless groups do not count. Like the
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
The earlier allowances for continuation, observation failure, declared wait and mode remain.
A stale but valid share file keeps its recorded threshold with no staleness signal. A share above
achievable concurrency blocks each armed turn-end once; the loop guard releases the second.
Share ownership is checked in this process's uid namespace, not necessarily the host's. The check
does not establish parent-directory control or exclude intermediate symlinks. Regular-file reads
are assumed local; O_NONBLOCK does not guarantee bounded filesystem latency.
Diagnostics are delivered only to regular files, FIFOs and sockets. Terminal stderr,
including PTY masters and slaves, other devices and unknown types receives no diagnostic:
these destinations are silently dropped without writing or reopening them. Unavailable
permitted destinations can also lose diagnostics. The exit status remains the contract.

GRC DIAGNOSTIC ADAPTATION (2026-10-05; backlog 3b226). Connected socket stderr needs no
address discovery: wrap the inherited descriptor with explicit neutral metadata and use sendmsg
with MSG_DONTWAIT. This also delivers under sandboxes that deny socket metadata queries and
sendto while permitting sendmsg on an already-connected descriptor. Fork isolation, shared
fd flags, deadlines, message bounds and fail-open behaviour are unchanged.

CONSOLE AND DETAIL LOG (maintainer-directed 2026-11-04: refusal detail belongs on the backend, not
the operator view). This changes only how a block is worded and routed, never whether the hook
blocks. On a block, run() appends the full detail (decide()'s complete reason plus every
actionable item's ID and title) to a per-session log,
<root>/stop-hook-detail/stop-guard.<first 12 characters of session_id>.log (each entry's header
carries the whole session_id), where <root> is the fixed per-account detail log root
<home>/.local/state/grc (_open_detail_root), the same root
block-turn-end-with-outstanding-work.py uses, through helpers identical in both hooks. <home>
is the password-database home of the effective uid (_detail_home); neither HOME nor
XDG_STATE_HOME is read, so a session's environment cannot move the log (tests replace it
through _DETAIL_HOME). The log is never written into the store (the directory of
_GRC_STATE_FILE: GRC_STORE or <repo-parent>/private, the lease's store), and detail logs already
in <store>/stop-hook-detail are neither moved nor deleted. A root inside this checkout
(_GRC_REPO_ROOT), or inside any git working tree or bare repository (a `.git` entry in the root
or any ancestor up to the filesystem root, lexically or after resolving symlinks, or `git
rev-parse --is-inside-work-tree` exiting 0, as it does in a working tree and inside a bare
repository, run with every inherited GIT_* variable removed in the deepest level of the root's
path that exists), is refused before anything is created. The diagnostic is then three short
lines
(_short_refusal), each at most _MAX_LINE_CHARS: what blocked with the actionable count, WHY
with the live group count and the required count (decide()'s max(operator share, 3), from
_required_groups) on every wording, the shortest being "WHY: live 1/5 required; log: " (hook
escaping round 3, codex W2: the count-free wording it replaced was longer), and the one action
that clears it, which names the declared-wait
escape path (_grc_escape_file, #2496: a sentinel was once written at the wrong path because
the message did not name it) as one shell word (_shell_word) with decide()'s condition "(once, after recording the blocker)",
followed by the log path. When the escape path and the log path do not both fit that line, the
escape path keeps the CONSIDER INSTEAD line, with the condition when it fits and "(condition
in log)" when it does not, and the log path moves to the end of the WHY line; there is never a
fourth line. No item ID or title appears in that form. PATH BUDGET: the log path adds 45
characters to the root path (with a 12-character session prefix), so the short form fits a root
path of at most 84 characters while the required count has at most two digits, as run()'s always
has (_SLOT_SHARE_MAX is 64; hook escaping round 4, claude N3: a longer required count leaves
less), and of 86 while it has one digit (the default floor is 3), that is a home of at most 67
or 69 characters (the root adds 17): the shortest WHY wording,
"WHY: live <live>/<required> required; log: ", leaves 129 to 131 characters for the log path
(82 when no required count is passed, as before round 3, where the shortest wording leaves
127); a longer root path, an escape
path longer than 101 characters (shell-quoted), or a log or escape path with any non-printable
character (a newline, a carriage return, a terminal escape or a Unicode space separator other
than the ASCII space, tested with _printable), takes the fallback below. The full detail (every
item ID and title) is built only after the time budget
and the session_id have been checked, inside the deadline-controlled write thread, so a very
large item list cannot push the refusal past the budget. The root is opened without following a
symlink anywhere on its path ("/" first, then each component relative to the one before, with
O_NOFOLLOW), and each open directory is checked with fstat: every directory above the home owned
by root or this uid with no group or other write bit, unless root-owned and sticky; the home,
.local and .local/state owned by this uid with no group or other write bit; grc owned by this
uid with no group or other access. Missing directories from .local down are created with mode
0700; nothing is created at or above the home, and no existing directory is changed. A `.git`
entry in grc or in the subdirectory is refused, and the git working tree check runs again after
the walk, whether or not a directory was created, immediately before the root is returned for
the write, so a `.git` planted meanwhile at a level that already existed is refused too. The
subdirectory must be owned by this uid with no group or other access; the file must be regular,
mode 0600, owned by this uid and singly linked; and after the write the advertised path must
still name the written file (lstat st_dev and st_ino against the descriptor's fstat). Building
the detail, the resolution, checks, open and write run in a daemon thread. TIME BUDGET: the Stop
hook timeout in .claude/settings.json is 10 seconds and the producer alone may take
PRODUCER_TIMEOUT_S (8), so the whole run is kept within _RUN_BUDGET_S (8.5) seconds of this
module starting to execute (main() sets _RUN_DEADLINE): the thread is joined for at most
min(_DETAIL_TIMEOUT_S, time left in that budget), and with less than _MIN_WRITE_S left, or no
usable session_id, no detail is built and no write is attempted. The remaining 1.5 seconds cover
interpreter startup and compiling this file, _diagnostic's 0.2-second fork wait and exit. If the
log cannot be written (no usable session_id in the Stop payload, no password-database entry or
an unusable home, a root inside this checkout, a git working tree or a bare repository, a
symlink, a wrong owner or mode, a timeout, a spent budget, or any open, check or write failure),
or the log path and the
escape path cannot both be shown within the three lines, the fallback is emitted instead
(_fallback_refusal): decide()'s reason, then one NOTE line naming the failure (_note_line: the
cause's type and reason and, for an OSError naming one path, that path; when the line would
exceed _MAX_LINE_CHARS, only the path is shortened (_shorten_path), to the room the form, the
state, the reason and the quoting around the path (the ": '" before it and the "'" after it)
leave of _MAX_LINE_CHARS, so the entry it names, such as a .git, is shown only when that room
holds its name, and the path can shrink to the elision mark alone; when even the mark does not
fit, and for any other cause whose line is too long, the whole line is cut to _MAX_LINE_CHARS
ending in the mark (_clamp), which drops the end of the line, then the path, then the end of the
reason), then the actionable count only. This fails open to visibility, never to silence, and
keeps #2291: no item ID or title reaches the diagnostic on either path. Every fallback line is
clamped to _MAX_LINE_CHARS and _MAX_LINE_BYTES, so the fallback always fits _diagnostic's
PIPE_BUF cap with the NOTE intact. decide() writes the declared-wait path as one printable shell
word (_shell_word), so a newline or terminal escape in it cannot start a diagnostic line on the
fallback (the detail log carries the same text), and the producer's fail-open NOTICE escapes the
producer's stderr and path the same way. Exit status, the escape and stop_hook_active handling
are unchanged. RESIDUE: a home kept in a git working tree or a bare repository refuses every
log (visibly, through the NOTE), with no second location; a bare repository is not seen when
git's configuration sets safe.bareRepository to explicit; a `.git` planted above grc, or in grc
itself, between the last git working tree
check and the file open is not seen (only this uid or root can plant one there); the log is
appended to without rotation; two sessions whose ids share their first 12 characters share one
log file (each entry names its session); a write that times out may still complete later in the
abandoned thread, and the process exit can still wait on a syscall the kernel does not let a
fatal signal interrupt.

Self-test: python3 .claude/hooks/stop-guard-unattended.py --self-test.
Self-contained: grc file/producer fixtures replace lab_infra tooling fixtures; registry cases remain.
"""

import datetime
import errno
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

# Start of the run's time budget (see TIME BUDGET under CONSOLE AND DETAIL LOG).
_LOADED_AT = time.monotonic()

# Architect-directed 2026-09-24: the block message is at most _MAX_REASON_LINES lines of at most
# _MAX_LINE_CHARS characters, whatever the item count. B computes the first _MAX_IDS item numbers;
# grc message exceptions below use the producer command and emit only the count.
_MAX_REASON_LINES = 5
_MAX_LINE_CHARS = 160
_MAX_IDS = 5
_MIN_LIVE_GROUPS = 3  # D-295: three active workstreams; a lone worker cannot license a yield.
_KILLREG_DIR = "/run/orch-workers"
_SLOT_SHARES_FILE = "/opt/orch-operator/slot-shares.json"
_SLOT_SHARE_PROJECT = "grc"
_SLOT_SHARE_EXPECT_UID = 0
_SLOT_SHARE_MAX = 64
_SLOT_SHARE_MAX_BYTES = 65536
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

# The minimal file-based adapter runs this OPTIONAL repo-relative Python executable to enumerate actionable
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

# The fleet's canonical mode file and its required owner (3b781). Module globals so the
# self-test can point them at fixtures; there is deliberately no environment override,
# so no configuration can switch the fleet file off. Fixtures never touch the live path.
_FLEET_MODE_FILE = "/opt/orch-operator/operating-mode"
_FLEET_OWNER_UID = 0


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


_MAX_GITFILE_BYTES = 1 << 20  # git's read_gitfile refuses a larger gitfile


def _is_primary_checkout(root):
    """True for a main checkout (.git is a directory) or a submodule (.git is a file naming an admin
    directory), False for a linked worktree or anything unreadable. The test is structural, as git's own:
    a linked worktree's admin directory holds a `commondir` file, a submodule's does not. The gitdir is
    resolved against the checkout with every symlink followed, so neither the spelling of the path nor an
    ancestor directory named `worktrees` changes the answer (3b101 QA r3). The admin directory must hold a
    HEAD file, as every git directory does, so a gitdir naming some other directory is not taken for one
    (3b101 QA r5). A gitdir that is missing, malformed or not a git directory returns False: the adapter
    then stays off, which allows the stop and consumes nothing. The gitfile is parsed as git's
    read_gitfile parses it (3b124): a regular file of at most 1 MiB that starts with exactly `gitdir: `,
    whose target is every byte after that prefix except the trailing run of newlines and carriage
    returns. Nothing else is stripped, so a doubled space after the prefix, trailing spaces or a trailing
    extra line leaves a target naming no git directory, and git and this check both refuse the gitfile.
    A target that still holds a newline is refused outright (git accepts one only when a directory's own
    name contains it), so the parse is never more lenient than git's. The HEAD-and-directory test stays
    lighter than git's own, which also requires objects and refs."""
    dotgit = os.path.join(root, ".git")
    if os.path.isdir(dotgit):
        return True
    try:
        # O_NONBLOCK: a FIFO named .git cannot stall the hook; git reads only a regular file (3b124)
        with os.fdopen(os.open(dotgit, os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC), "rb") as fh:
            st = os.fstat(fh.fileno())
            if not stat.S_ISREG(st.st_mode) or st.st_size > _MAX_GITFILE_BYTES:
                return False
            data = fh.read(_MAX_GITFILE_BYTES + 1)
    except OSError:
        return False
    if len(data) > _MAX_GITFILE_BYTES or not data.startswith(b"gitdir: "):  # exact prefix (3b101 QA r6)
        return False
    target = data[len(b"gitdir: "):].rstrip(b"\r\n")  # git drops the trailing CR/LF run, nothing more
    if not target or b"\n" in target:  # no path, or a second line (3b124)
        return False
    try:  # a NUL in the gitdir raises ValueError (3b101 QA r5)
        admin = os.path.realpath(os.path.join(root, os.fsdecode(target)))
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
# main() carries the one-shot escape; the registry remains B's, with the 3b286 share reader beside it.
# Decision/message adaptations: P-1.36, #2291, #2496, 3b286.
# ---------------------------------------------------------------------------
# Paths follow the checkout (3b101): the repo root is this file's grandparent's parent, the lease lives
# in the operational store (GRC_STORE, else <repo-parent>/private), and the declared-wait sentinel in
# GRC_DROP_ROOT, else <repo-parent>/grc_working. The operator share has a fixed fleet path.
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

    One source per checkout (3b113 QA r2; fleet-first since 3b781):
      - the primary grc checkout: the fleet mode file FIRST, then the lease's dated #5(b) swap,
        through the shared reader (_grc_effective_mode -> .claude/hooks/_operating_mode.py), the
        result mapped via _grc_map_mode (the lease: 'Operating-mode:', plain or bold, from
        GRC_STORE, else <repo-parent>/private, then session-state.md); on a reader-load
        failure or reader exception, the armed 'unattended' (fail closed, 3b781 r2); a
        MODE_FILE there is ignored, so a stray file never shadows the lease.
      - any other root (the bundled --self-test, a file-based adopter): the repo-relative single-word
        file MODE_FILE. Present -> its trimmed word (or None); absent -> None.
         (The one-shot declared-wait escape is consumed at the top of main() by _grc_consume_escape.)

    GRC WIRING NOTE: grc keeps the lease mode in session-state.md (not MODE_FILE) and declares a
    genuine wait with the .allow-idle-stop sentinel (the retired block-idle-stop hook's documented
    escape), both preserved here. A read failure at every source returns None (fail open); an
    unusable fleet FILE (present but unreadable, wrong-owner, malformed, or missing set_at)
    resolves to 'unattended' through the shared reader's fail-closed default, and a missing or
    failing shared READER resolves to 'unattended' directly (3b781 r2); both ARM the guard,
    the over-blocking direction (an operator ends it by fixing the file, reader or record)."""
    # GRC (3b113 QA r2, 3b781): the grc main checkout reads the fleet file first, then the lease,
    # so a stray MODE_FILE there never shadows either. Every other root takes the delivered
    # core's portable MODE_FILE branch.
    if _is_grc_main_checkout(root):
        return _grc_effective_mode(root)
    path = os.path.join(root, MODE_FILE)
    try:
        with open(path, encoding="utf-8") as fh:
            val = fh.read().strip()
        return val or None
    except FileNotFoundError:
        pass  # no file-based mode record
    except (OSError, UnicodeDecodeError):  # 3b679 r6: an undecodable MODE_FILE is an unreadable one (fail open)
        return None
    # Not the grc checkout, so _grc_lease_mode returns None here; the call is kept as a defensive default.
    return _grc_lease_mode(root)


def _grc_operating_mode_helper(_cache=[]):
    """Load the shared operating-mode reader (.claude/hooks/_operating_mode.py) with a minimal
    copy of the AskUserQuestion hook's containment discipline, or None on ANY failure (the caller
    then FAILS CLOSED to the armed state, 3b781 r2: a packaging defect must not let a stale
    lease disarm the guard). Containment is decided on the path AS LAUNCHED before symlink resolution:
    this hook must sit at <root>/.claude/hooks, no component from the root down to the helper may
    be a symlink, and the helper's real location must sit at exactly its expected place under the
    real repository root; the reviewed SOURCE BYTES are then executed into a fresh module (no
    import machinery, no sys.path, no bytecode cache). The result is cached per process."""
    if _cache:
        return _cache[0]
    try:
        hook_path = os.path.abspath(__file__)
        hooks_dir = os.path.dirname(hook_path)
        claude_dir = os.path.dirname(hooks_dir)
        root = os.path.dirname(claude_dir)
        if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
            return None
        helper_path = os.path.join(hooks_dir, "_operating_mode.py")
        for p in (root, claude_dir, hooks_dir, hook_path, helper_path):
            if os.path.islink(p):
                return None
        real_root = os.path.realpath(root)
        if os.path.realpath(hook_path) != os.path.join(
                real_root, ".claude", "hooks", os.path.basename(hook_path)):
            return None
        if os.path.realpath(helper_path) != os.path.join(
                real_root, ".claude", "hooks", "_operating_mode.py"):
            return None
        with open(helper_path, "rb") as fh:
            source = fh.read()
        module = type(sys)("_operating_mode")
        module.__file__ = helper_path
        exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    except Exception:  # noqa: BLE001 (any load failure -> the caller fails closed to armed)
        return None
    _cache.append(module)
    return module


def _grc_effective_mode(root):
    """grc mode source (3b781): the fleet mode file first, then the lease's dated #5(b) swap,
    combined by the shared reader's effective_mode and mapped via _grc_map_mode, only in the
    primary grc checkout and never for a worker (3b101 QA r3). The lease is read bounded and
    non-blocking (_grc_read_lease_text, 3b781 r2) and parsed exactly as _grc_lease_mode parses
    it (_grc_mode_value: LF-only split, comment-aware, one trailing CR dropped); a lease
    failure never prevents consulting the fleet file. A reader-load failure or reader
    exception FAILS CLOSED to the armed 'unattended' (3b781 r2): the AskUserQuestion hook
    fails closed on the same condition, and the lease never outranks the fleet file. A fleet
    file that is absent leaves the lease deciding as before: the shared reader hands the
    undated value back RAW and _grc_map_mode applies this guard's own legacy leading-token
    rule (the shared reader's documented grc divergence from lab_infra)."""
    if not _is_grc_main_checkout(root) or _grc_is_worker():
        return None
    helper = _grc_operating_mode_helper()
    if helper is None:
        # 3b781 r2 (codex E1, agy1 E1): a missing or refused shared reader fails
        # closed to the armed state; a stale lease must never disarm the guard
        # against the fleet authority.
        return "unattended"
    txt = _grc_read_lease_text()
    lease_value = _grc_mode_value(txt) if txt is not None else None
    try:
        mode, _source = helper.effective_mode(_FLEET_MODE_FILE, lease_value, _FLEET_OWNER_UID)
    except Exception:  # noqa: BLE001 (a reader defect fails closed to armed, 3b781 r2)
        return "unattended"
    if mode is None:
        return None
    return _grc_map_mode(mode)


_GRC_LEASE_MAX_BYTES = 65536  # orch_store's MAX_FILE; gate 63 refuses a larger lease


def _grc_read_lease_text():
    """The lease's text, or None when it cannot be read SAFELY (3b781 r2, codex W3): the
    lease is opened without blocking, rejected unless a regular file BEFORE any read (a
    FIFO lease used to hang the old open() before the fleet file was consulted), and read
    bounded (over _GRC_LEASE_MAX_BYTES, or undecodable, is None: a prefix is not the
    lease). The bytes are decoded without newline translation, so every CR survives and
    _grc_mode_value splits on LF only (3b679 r4)."""
    try:
        fd = os.open(_GRC_STATE_FILE, os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC)
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        raw = b""
        while len(raw) <= _GRC_LEASE_MAX_BYTES:
            chunk = os.read(fd, _GRC_LEASE_MAX_BYTES + 1 - len(raw))
            if not chunk:
                break
            raw += chunk
    except OSError:
        return None
    finally:
        os.close(fd)
    if len(raw) > _GRC_LEASE_MAX_BYTES:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:  # 3b679 r5: an undecodable lease is an unreadable one
        return None


def _grc_lease_mode(root):
    """grc mode source: session-state.md 'Operating-mode:' -> mapped arm-state, only in the primary grc
    checkout and never for a worker (3b101 QA r3). (The one-shot declared-wait escape is handled at the top
    of main() via _grc_consume_escape, not here, so it is consumed on the malformed/worker fail-open paths
    too.) Split out of read_operating_mode in 3b113 QA r2 so the grc checkout reads the lease alone;
    since 3b781 r2 the grc checkout always decides through _grc_effective_mode (a reader failure
    fails closed THERE, never here), so this remains only as read_operating_mode's non-grc
    defensive default and as the self-test's direct lease probe; it shares the bounded,
    non-blocking _grc_read_lease_text (3b781 r2)."""
    if not _is_grc_main_checkout(root) or _grc_is_worker():
        return None
    txt = _grc_read_lease_text()
    if txt is None:
        return None
    value = _grc_mode_value(txt)
    if value is None:
        return None
    return _grc_map_mode(value)

# 3b679: the lease's plain `Operating-mode: <mode>` line (gate 63's form) or the earlier bold form.
# 3b679 r3: the exact label at column zero, the value separated by spaces or tabs only (never a line
# end), on a line that does not start inside an HTML comment.
_GRC_MODE_RE = re.compile(r"(?:\*\*Operating-mode:\*\*|Operating-mode:)[ \t]+(.+?)[ \t]*")
_GRC_COMMENT_DELIMITER = re.compile(r"<!--|-->")


def _grc_mode_value(txt):
    """The first exact `Operating-mode:` line's value, skipping every line that starts inside an HTML
    comment ("<!--" opens and "-->" closes one wherever either appears, across lines; no nesting; an
    unclosed comment runs to EOF), or None. Lines split on LF only, as block-askuserquestion-unattended.py
    and tools/session_facts.py split them; one trailing CR is dropped (3b679 r4)."""
    comment = False
    for line in txt.split("\n"):
        if not comment:
            m = _GRC_MODE_RE.fullmatch(line[:-1] if line.endswith("\r") else line)
            if m:
                return m.group(1)
        for delimiter in _GRC_COMMENT_DELIMITER.finditer(line):
            comment = delimiter.group() == "<!--"
    return None

def actionable_items(root):
    """DEFAULT (minimal file-based) adapter. Run the OPTIONAL Python executable at ACTIONABLE_PRODUCER and parse
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
            [sys.executable, "-I", exe], cwd=root, input="", capture_output=True, text=True, timeout=PRODUCER_TIMEOUT_S
        )
    except Exception:
        return None  # timeout / spawn failure -> indeterminate -> fail open
    if proc.returncode != 0:
        reason = " ".join(proc.stderr.splitlines()).strip() or (exe + " exited " + str(proc.returncode))
        _diagnostic("NOTICE (stop-guard-unattended; fail open): " + _printable(reason[:1024]) + "\n")
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
# END ADAPTER SEAM -- B core below; registry code is unchanged. (GRC:
# Exceptions: message text (P-1.36, #2291, #2496); socket transport (3b226); slot-share floor (3b286).
# Exit statuses are unchanged; read_slot_share, decide() and run() carry the slot-share floor.
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


# Share causes: absent | notreg | unowned | badmode | toobig | invalid | unread.
# run() uses skipped only on paths that allow before formatting the share.
def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def read_slot_share(path=None, project=None, expect_uid=None):
    """Read the operator's recorded share. A valid project needs no valid default.
    Closing is attempted; close errors are contained."""
    path = _SLOT_SHARES_FILE if path is None else path
    project = _SLOT_SHARE_PROJECT if project is None else project
    expect_uid = _SLOT_SHARE_EXPECT_UID if expect_uid is None else expect_uid
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    except OSError as exc:
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            return None, "absent"
        return None, "notreg" if exc.errno == errno.ELOOP else "unread"
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode):
            return None, "notreg"
        if metadata.st_uid != expect_uid:
            return None, "unowned"
        if metadata.st_mode & 0o022:
            return None, "badmode"
        chunks, total = [], 0
        while True:
            chunk = os.read(fd, _SLOT_SHARE_MAX_BYTES + 1 - total)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > _SLOT_SHARE_MAX_BYTES:
                return None, "toobig"
    except OSError:
        return None, "unread"
    finally:
        try:
            os.close(fd)
        except OSError:
            pass
    try:
        data = json.loads(b"".join(chunks).decode("utf-8-sig"), object_pairs_hook=_no_duplicate_keys)
        if not isinstance(data, dict) or type(data.get("schema")) is not int or data["schema"] != 1:
            return None, "invalid"
        if "shares" in data and not isinstance(data["shares"], dict):
            return None, "invalid"
        shares = data.get("shares", {})
        value, source = (shares[project], project) if project in shares else (data["default"], "default")
        if type(value) is not int or not 1 <= value <= _SLOT_SHARE_MAX:
            return None, "invalid"
        return value, source
    except Exception:
        return None, "invalid"


def _required_groups(share):
    """The required live owned dispatch group count for ``share`` (a (value, source-or-cause)
    tuple), by decide()'s rule (3b286): the larger of the value and _MIN_LIVE_GROUPS, or
    _MIN_LIVE_GROUPS when the value is None. run() passes it to the console short form;
    decide() keeps its own statement of the rule (its mutation self-test targets it), and the
    self-test test_short_form_shows_the_required_count checks that the two agree."""
    value = share[0]
    return _MIN_LIVE_GROUPS if value is None else max(_MIN_LIVE_GROUPS, value)


def decide(mode, stop_hook_active, actionable, live_groups, share):
    """Pure decision. Returns (block: bool, reason: str). Block iff: unattended mode AND not already in a
    stop-hook continuation AND the actionable set is non-empty AND the known live count is below
    the required count (the larger of the operator share and 3). `actionable` is a list (possibly
    empty) or None (indeterminate -> fail open). An indeterminate live count also fails open.
    share is a required (value, source-or-cause) tuple from read_slot_share or run(). The requirement is
    max(share, _MIN_LIVE_GROUPS), falling back to _MIN_LIVE_GROUPS when the value is None."""
    if mode != "unattended":
        return False, ""
    if stop_hook_active:
        return False, ""  # documented loop-guard: already blocked this chain -> allow (no infinite loop)
    if not isinstance(actionable, list) or not actionable:
        return False, ""  # None (indeterminate) or empty (exhausted) -> allow
    if live_groups is None:
        return False, "STOP ALLOWED (unattended): live dispatch observation unavailable; fail open."
    value, token = share
    if value is None:
        required = _MIN_LIVE_GROUPS
        note = "minimum %d, share %s" % (required, token)
    else:
        required = max(value, _MIN_LIVE_GROUPS)
        if value < _MIN_LIVE_GROUPS:
            note = "minimum %d, share %s %d below floor" % (required, token, value)
        else:
            note = "minimum %d, share %s" % (required, token)
    if live_groups >= required:
        return False, "STOP ALLOWED (unattended): %d live owned dispatch groups; yielding to await work (%s)." % (
            live_groups, note)
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
        "(a [BLOCKED:<reason>] tag with a granted approvals row)." % required,
        # One shell word naming the declared-wait path itself (_shell_word): an escaped path in
        # this command would touch a different file (hook escaping round 3, codex W1). The
        # command is shown whole or not at all, never cut by the clamp below (round 4, codex W1).
        _declared_wait_line(_grc_escape_file()),
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
            # This connected fd needs no address/type/protocol discovery. Explicit neutral
            # metadata avoids queries denied by some sandboxes; the kernel retains the
            # actual socket properties. Only descriptor-based sendmsg and close are used.
            peer = socket.socket(family=socket.AF_UNSPEC, type=0, proto=0, fileno=fd)
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
            written = (peer.sendmsg([remaining], [], socket.MSG_DONTWAIT) if peer is not None
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


_DETAIL_SUBDIR = "stop-hook-detail"
_DETAIL_NAME = "stop-guard"
_SESSION_PREFIX_CHARS = 12
_DETAIL_TIMEOUT_S = 2.0
# The detail log root, <home>/.local/state/grc, under the password-database home of the effective
# uid (_detail_home). No environment variable moves it; tests set _DETAIL_HOME (None: the lookup).
_DETAIL_ROOT_PARTS = (".local", "state", "grc")
_DETAIL_HOME = None
# The mark _shorten_path puts where it drops part of a path a NOTE line names, and _clamp
# puts at the end of a line it cuts.
_ELISION = "..."
# Set to 1 to let a self-test real detail log write skip, with the reason, on a host whose
# temporary directory cannot provide a fixture home that meets the root's rule; unset, it fails.
# tests/test_linters.py applies the same rule with the same variable.
_UNSAFE_TMP_SKIP_ENV = "GRC_ALLOW_UNSAFE_TMP_SKIP"
# TIME BUDGET: the whole run stays within _RUN_BUDGET_S of _LOADED_AT, under the 10-second Stop
# hook timeout in .claude/settings.json with margin; _RUN_DEADLINE is set by main() only.
_RUN_BUDGET_S = 8.5
_MIN_WRITE_S = 0.25
_RUN_DEADLINE = None
_SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", re.ASCII)
# Per-line byte bound for the fallback: any valid 160-character UTF-8 line fits; only lines that
# escape to more bytes (surrogate escapes) are cut further. Five reason lines plus the NOTE at
# 641 bytes each, plus the short count line, stay below PIPE_BUF (4096), so _diagnostic never
# truncates the fallback.
_MAX_LINE_BYTES = 640


def _printable(value):
    """``value`` as text with every character that is not printable shown as its ascii()
    escape: a control character, and a Unicode space separator (category Zs) other than the
    ASCII space, among others. Used for console lines and the detail log in both Stop hooks."""
    return "".join(ch if ch.isprintable() else ascii(ch)[1:-1] for ch in str(value))


def _shell_word(text) -> str:
    """``text`` as ONE shell word that names the path ``text`` and prints on one line, for a
    command a refusal tells the reader to run (escaping a shell-quoted word would change the
    path the command names): shlex.quote when every character is printable or a space
    separator, else a bash ANSI-C quoted $'...' word in which a backslash or a single quote is
    backslash-escaped and every other character outside that rule is an escape bash reads
    back in any locale: below 0x80 the ascii() escape _printable shows, such as \\n or
    \\x1b; from 0x80 up, a surrogate-escaped byte included, \\xHH for each byte os.fsencode
    gives: the path's own bytes in this process's filesystem encoding, which bash rebuilds in
    any locale (a \\uHHHH escape stayed literal outside a UTF-8 locale, round 4, claude W1;
    UTF-8 bytes named another path when the hook ran in a non-UTF-8 locale, round 5, claude
    N3). A character that encoding cannot hold keeps its UTF-8 bytes. A relative
    path starting with "-" is written "./" first, so touch, cd, git -C or python3 cannot
    read it as an option (round 4, codex W2)."""
    import shlex
    import unicodedata
    text = str(text)
    if text.startswith("-"):
        text = "./" + text

    def plain(char):
        return char.isprintable() or unicodedata.category(char) == "Zs"

    if all(plain(char) for char in text):
        return shlex.quote(text)
    out = []
    for char in text:
        code = ord(char)
        if char in "\\'":
            out.append("\\" + char)
        elif plain(char):
            out.append(char)
        elif code < 0x80:
            out.append(ascii(char)[1:-1])  # \n, \r, \t or \xHH: the escape _printable shows
        else:
            try:
                data = os.fsencode(char)  # a surrogate-escaped byte gives that byte back
            except UnicodeEncodeError:
                data = char.encode("utf-8", "surrogatepass")
            out.append("".join("\\x%02x" % byte for byte in data))
    return "$'" + "".join(out) + "'"


_WAIT_FORMS = ("Declared wait: touch %s (once, after recording blocker); operator stop: set mode "
               "attended.",
               "Declared wait (once, after recording blocker): touch %s")
_WAIT_TOO_LONG = ("Declared wait (once, after recording blocker): touch .allow-idle-stop in %s; "
                  "its path is too long for this line (%s).")
# The directory _grc_escape_file used: GRC_DROP_ROOT absolute, GRC_DROP_ROOT relative (resolved
# against the repo root by _grc_under_root), or unset or empty (round 5, claude N1).
_WAIT_DIRS = ("GRC_DROP_ROOT", "<repo-root>/GRC_DROP_ROOT", "<repo-parent>/grc_working")
_WAIT_LOGGED = "the detail log has it"
_WAIT_NOT_LOGGED = "no detail log written"
# Each too-long line decide() can write, mapped to its wording for an unwritten detail log.
_WAIT_UNLOGGED = {_WAIT_TOO_LONG % (where, _WAIT_LOGGED): _WAIT_TOO_LONG % (where, _WAIT_NOT_LOGGED)
                  for where in _WAIT_DIRS}


def _grc_escape_dir_label():
    """The directory _grc_escape_file uses, named as the too-long declared-wait line shows it,
    from the same GRC_DROP_ROOT reading: the setting when it is absolute, the setting under the
    repo root when it is relative (_grc_under_root), the default when it is unset or empty."""
    value = os.environ.get("GRC_DROP_ROOT")
    if not value:
        return _WAIT_DIRS[2]
    return _WAIT_DIRS[0] if os.path.isabs(value) else _WAIT_DIRS[1]


def _declared_wait_line(escape_path):
    """decide()'s declared-wait line, at most _MAX_LINE_CHARS characters: the touch command
    with the path as one shell word (_shell_word), shown whole or not at all. A cut word names
    another path, or leaves a $'...' word unterminated (hook escaping round 4, codex W1). The
    operator-stop hint is dropped first; when the command alone does not fit, the line names
    the sentinel and the directory the hook used (_grc_escape_dir_label; round 5, claude N1)
    and says the detail log has the command: _detail_text adds the whole command to the log,
    and _fallback_refusal rewords the line when the log was not written (round 5, claude W1)."""
    word = _shell_word(escape_path)
    for form in _WAIT_FORMS:
        if len(form % word) <= _MAX_LINE_CHARS:
            return form % word
    return _WAIT_TOO_LONG % (_grc_escape_dir_label(), _WAIT_LOGGED)


def _clamp(line, limit=_MAX_LINE_CHARS):
    """``line`` as one console line of at most ``limit`` characters (``limit`` at least
    len(_ELISION)) and _MAX_LINE_BYTES encoded bytes: whole when it fits both, else cut to fit
    them, ending in _ELISION."""
    if len(line) <= limit and len(line.encode("utf-8", "backslashreplace")) <= _MAX_LINE_BYTES:
        return line
    line = line[:limit - len(_ELISION)]
    while len((line + _ELISION).encode("utf-8", "backslashreplace")) > _MAX_LINE_BYTES:
        line = line[:-1]
    return line + _ELISION


def _first_fit(forms, values, what):
    """The first of ``forms`` that, filled with ``values``, fits one console line whole; raises
    ValueError naming ``what`` when none does."""
    for form in forms:
        line = form % values
        if _clamp(line) == line:
            return line
    raise ValueError("%s does not fit one console line" % what)


def _short_refusal(count, live_groups, log_path, escape_path, required=None):
    """The three diagnostic lines, each at most _MAX_LINE_CHARS: what blocked (count only,
    #2291), WHY, and the one action that clears it. The WHY line gives the live owned dispatch
    group count and, when ``required`` (decide()'s required count, _required_groups) is given,
    the required count on every wording (the shortest, "WHY: live 1/5 required; log: ", is
    shorter than the count-free "WHY: below the group floor; log: ", which is used only when
    ``required`` is not given; hook escaping round 3, codex W2). The action line names the declared-wait
    escape path (#2496) as one shell word (_shell_word: a path with a space or a quote is
    shell-quoted, so the copied command touches that path) with decide()'s condition (once, after recording the blocker) and then
    the detail log path when all fit it whole; otherwise the escape path keeps the action line,
    with the condition when it fits and "(condition in log)" when it does not, and the log path
    ends the WHY line. There is never a fourth line. A log or escape path with any non-printable
    character, or one that cannot fit whole, raises before its length is used, and the caller
    then shows the fallback.
    PATH BUDGET: with ``required`` given, as run() does, the shortest WHY wording leaves 129 to
    131 characters for the log path while the required count has at most two digits (as run()'s
    always has), so the root path may be at most 84, or 86 with a one-digit required count;
    without it, 127 and 82 (see CONSOLE AND DETAIL LOG); the escape
    path at most 101 as shell-quoted."""
    if _printable(log_path) != log_path:
        raise ValueError("detail log path has a non-printable character")
    if _printable(escape_path) != escape_path:
        raise ValueError("declared-wait path has a non-printable character")
    escape_word = _shell_word(escape_path)
    blocked = _clamp("BLOCKED (stop-guard-unattended): unattended turn-end yield; the backlog tool "
                     "reports %d actionable open backlog item(s)." % count)
    if required is None:
        why = _clamp("WHY: not whole-set exhaustion, and the live owned dispatch group count (%d) "
                     "is below the required count." % live_groups)
        split_whys = ("WHY: the live owned dispatch group count (%d) is below the required "
                      "count; detail log: " % live_groups + "%s",
                      "WHY: below the group floor; log: %s")
    else:
        why = _clamp("WHY: not whole-set exhaustion, and the live owned dispatch group count (%d) "
                     "is below the required count (%d)." % (live_groups, required))
        split_whys = ("WHY: the live owned dispatch group count (%d) is below the required "
                      "count (%d); detail log: " % (live_groups, required) + "%s",
                      "WHY: %d of %d required groups live; log: " % (live_groups, required) + "%s",
                      "WHY: live %d/%d required; log: " % (live_groups, required) + "%s")
    try:
        action = _first_fit(("CONSIDER INSTEAD: continue; wait (once, after recording the "
                             "blocker): touch %s; log: %s",),
                            (escape_word, log_path), "declared-wait and detail log paths")
    except ValueError:
        # Prefer the escape path on the action line; the log path ends the WHY line. The
        # condition stays on the action line when it fits; otherwise the line says it is in
        # the log (decide()'s reason, which the log carries, states it).
        action = _first_fit(("CONSIDER INSTEAD: continue the top actionable item; declared wait "
                             "(once, after recording the blocker): touch %s",
                             "CONSIDER INSTEAD: continue; wait (once, after recording the "
                             "blocker): touch %s",
                             "CONSIDER INSTEAD: continue; wait (condition in log): touch %s"),
                            (escape_word,), "declared-wait path")
        why = _first_fit(split_whys, (log_path,), "detail log path")
    return "\n".join([blocked, why, action])


def _fallback_refusal(reason, count, state, why):
    """The visible fallback: decide()'s reason, the NOTE right after it, then the actionable
    count only (#2291: no item ID or title reaches the diagnostic). Every line is clamped, and
    the reason keeps at most _MAX_REASON_LINES lines, so the text fits _diagnostic's PIPE_BUF cap.
    When the detail log was not written, a too-long declared-wait line says so instead of
    pointing at the log (round 5, claude W1). ``why`` is the failure, an exception or text
    naming one, which _note_line renders, keeping its reason whole only when the line has room
    for it."""
    lines = reason.split("\n")[:_MAX_REASON_LINES]
    if state == "not written":
        lines = [_WAIT_UNLOGGED.get(line, line) for line in lines]
    lines = [_clamp(line) for line in lines]
    form = "NOTE: detail log %s (%s); reason shown here."
    try:
        lines.append(_note_line(form, state, why))
    except Exception:
        lines.append(_clamp(form % (state, type(why).__name__)))
    lines.append(_clamp("Actionable items: %d (IDs and titles are not shown here, #2291)." % count))
    return "\n".join(lines)


def _append_private(top, directory, name, text):
    """Append ``text`` to ``directory/_DETAIL_SUBDIR/name``, where ``top`` is the descriptor
    _open_detail_root returned for ``directory`` (the caller closes it), without following a
    symlink at the subdirectory or the file. The subdirectory must be owned by this uid with no
    group or other access and hold no `.git` entry; the file must be a singly linked regular
    file owned by this uid, mode 0600; after the write the returned path must still name the
    written file (same st_dev and st_ino). Any failure raises; the caller then fails open."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        os.mkdir(_DETAIL_SUBDIR, 0o700, dir_fd=top)
    except FileExistsError:
        pass
    sub = os.open(_DETAIL_SUBDIR, flags, dir_fd=top)
    try:
        info = os.fstat(sub)
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o077):
            raise PermissionError(errno.EPERM, "detail log directory is not private", _DETAIL_SUBDIR)
        try:
            os.stat(".git", dir_fd=sub, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise PermissionError(errno.EPERM, "detail log directory holds a .git entry",
                                  os.path.join(os.fspath(directory), _DETAIL_SUBDIR, ".git"))
        fd = os.open(name, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW
                     | os.O_NONBLOCK | os.O_CLOEXEC, 0o600, dir_fd=sub)
    finally:
        os.close(sub)
    path = os.path.join(os.fspath(directory), _DETAIL_SUBDIR, name)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_nlink != 1):
            raise PermissionError(errno.EPERM, "detail log is not a private regular file", name)
        os.fchmod(fd, 0o600)
        data = text.encode("utf-8", "backslashreplace")
        while data:
            written = os.write(fd, data)
            if written <= 0:
                raise OSError(errno.EIO, "short write to detail log", name)
            data = data[written:]
        named = os.lstat(path)
        if (named.st_dev, named.st_ino) != (info.st_dev, info.st_ino):
            raise PermissionError(errno.EPERM, "detail log path was replaced during the write", name)
    finally:
        os.close(fd)
    return path


def _git_tree_marker(directory, timeout):
    """What places ``directory`` inside a git working tree or a bare repository, or None: the
    first `.git` entry (of any type) in it or an ancestor up to the filesystem root, on the
    lexical path and on the resolved path, then `git rev-parse --is-inside-work-tree` exiting 0
    with every inherited GIT_* variable removed (so neither GIT_DIR nor a ceiling changes
    discovery), bounded by ``timeout``. git runs in the deepest of ``directory`` and its
    ancestors that exists (lexically), so a directory not yet created is checked where it
    would be created; inside a bare repository git prints "false" and still exits 0, so a bare
    repository is found before anything is created in it, unless git's own configuration sets
    safe.bareRepository to explicit (git then refuses the repository and exits nonzero). A
    missing git binary leaves the `.git` walk as the check; any other failure raises."""
    lexical = Path(os.path.abspath(directory))
    for start in (lexical, lexical.resolve()):
        for candidate in (start, *start.parents):
            try:
                os.lstat(candidate / ".git")
            except (FileNotFoundError, NotADirectoryError):
                continue
            return str(candidate / ".git")
    root = lexical
    while root != root.parent and not os.path.lexists(root):
        root = root.parent
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["LC_ALL"] = "C"
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'],
                                stdin=subprocess.DEVNULL, capture_output=True, env=env,
                                timeout=max(timeout, 0.01), check=False)
    except FileNotFoundError:
        return None
    return "git rev-parse" if result.returncode == 0 else None


def _refuse_git_tree(root, timeout):
    """Raise PermissionError when ``root`` is inside a git working tree or a bare repository
    (_git_tree_marker, within ``timeout`` seconds); the reason says "git working tree" for
    both. The error's path is the `.git` entry found, so a NOTE line that must shorten it still
    ends with that entry; when only git rev-parse placed the root in a repository, as for a
    bare repository, the path is the root and the reason says so."""
    marker = _git_tree_marker(root, timeout)
    if marker is None:
        return
    if marker == "git rev-parse":
        raise PermissionError(errno.EPERM, "detail log root is inside a git working tree "
                              "(git rev-parse)", root)
    raise PermissionError(errno.EPERM, "detail log root is inside a git working tree", marker)


def _shorten_path(path, room):
    """``path`` in at most max(``room``, len(_ELISION)) characters: whole when it fits; else its
    middle components replaced by _ELISION, keeping as many of its last components as fit (the
    last names the offending entry, such as a .git) and its first component when that fits
    too, as in "/var/.../home/.git". Only a last component longer than ``room`` allows is
    itself cut, from the left, behind _ELISION; with ``room`` at most len(_ELISION), only
    _ELISION is left."""
    if len(path) <= room:
        return path
    parts = path.split("/")
    lead = 2 if parts[0] == "" else 1
    head = "/".join(parts[:lead])
    for keep in range(len(parts) - lead, 0, -1):
        tail = "/".join(parts[-keep:])
        for shown in (head + "/" + _ELISION + "/" + tail, _ELISION + "/" + tail):
            if len(shown) <= room:
                return shown
    last = parts[-1]
    return _ELISION + last[len(last) - max(room - len(_ELISION), 0):]


def _note_line(form, state, cause):
    """``form``, a NOTE line with %s for the log state and then the cause, filled with
    ``state`` and ``cause`` (an exception, or text already naming one), at most
    _MAX_LINE_CHARS characters. Only the cause is escaped with _printable; ``form`` and
    ``state`` are fixed internal strings and go in as given. The cause is the text itself, or
    the exception's type and its reason text. For an OSError that names one path (a filename
    and no filename2), the reason is "<type>: [Errno N] <strerror>" and the path follows it in
    single quotes, as "<reason>: '<path>'", the reason and the path each escaped on its own
    before the path is shortened. The path gets the room the form, the state, the reason and
    that quoting (the ": '" before the path and the "'" after it) leave of _MAX_LINE_CHARS:
    _shorten_path cuts the path only when it is longer than that room, so the reason stays
    whole and the path keeps as many of its last components as fit (the last names the
    offending entry, such as a .git, only when the room holds its name). Every line then goes
    through _clamp, which cuts a line longer than _MAX_LINE_CHARS to end in _ELISION: an
    OSError line when that room is shorter than both _ELISION and the path, and any other
    cause's line when its text is too long. The end of the form goes first, then the path, if
    any, then the end of the reason, so the reason is kept whole only when it ends within the
    first _MAX_LINE_CHARS - len(_ELISION) characters of the line."""
    if not isinstance(cause, BaseException):
        return _clamp(form % (state, _printable(str(cause))))
    name = type(cause).__name__
    named = cause.filename if isinstance(cause, OSError) else None
    if named is None or cause.filename2 is not None:
        return _clamp(form % (state, _printable("%s: %s" % (name, cause))))
    try:
        path = os.fsdecode(named)
    except TypeError:
        path = str(named)
    reason = _printable("%s: [Errno %s] %s" % (name, cause.errno, cause.strerror))
    path = _printable(path)
    room = _MAX_LINE_CHARS - len(form % (state, "%s: ''" % reason))
    return _clamp(form % (state, "%s: '%s'" % (reason, _shorten_path(path, room))))


def _detail_home():
    """The home of this process's effective uid in the password database (pwd.getpwuid), or
    _DETAIL_HOME when a test sets it. HOME and XDG_STATE_HOME are never read, so a session's
    environment cannot move the detail log. Raises KeyError when the uid has no entry, and
    PermissionError unless the home is an absolute, normalized path below the filesystem root."""
    home = _DETAIL_HOME
    if home is None:
        home = pwd.getpwuid(os.geteuid()).pw_dir
    home = os.fspath(home)
    if (not os.path.isabs(home) or os.path.normpath(home) != home or home.startswith("//")
            or home == "/"):
        raise PermissionError(errno.EPERM, "home directory is not an absolute normalized path "
                              "below the filesystem root", home)
    return home


def _open_detail_root(checkout, timeout):
    """Open the detail log root, <home>/.local/state/grc (_detail_home, _DETAIL_ROOT_PARTS), and
    return (its directory descriptor, its path); the caller closes the descriptor. A root
    inside ``checkout``, or inside any git working tree or bare repository (_git_tree_marker,
    whose git leg runs in the deepest existing level of the root's path, within ``timeout``
    seconds), is refused before anything is created. "/" is opened and then each component
    relative to the one before with O_NOFOLLOW, so a symlink anywhere on the path is refused,
    and every open directory is checked with fstat, never by path: each directory above the
    home must be owned by root or this uid with no group or other write bit, unless it is
    root-owned and sticky; the home, .local and .local/state must be owned by this uid with no
    group or other write bit; grc must be owned by this uid with no group or other access.
    Missing directories from .local down are created with mode 0700, and one that already
    exists is trusted only through the fstat of the descriptor then opened; nothing is created
    at or above the home, and no existing directory is changed. A `.git` entry in grc is
    refused, and the git working tree check (_refuse_git_tree) runs again after the walk,
    whether or not this call created a directory, immediately before the root is returned for
    the write. A failed open or mkdir names the whole path it reached. Any failure raises; the
    caller then fails open."""
    started = time.monotonic()
    home = _detail_home()
    root = os.path.join(home, *_DETAIL_ROOT_PARTS)
    if Path(root).resolve().is_relative_to(Path(checkout).resolve()):
        raise PermissionError(errno.EPERM, "detail log root resolves inside this checkout", root)
    _refuse_git_tree(root, timeout - (time.monotonic() - started))
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    euid = os.geteuid()
    writable = stat.S_IWGRP | stat.S_IWOTH

    def descend(parent, name, path):
        # On failure the caller still holds ``parent`` and closes it.
        try:
            child = os.open(name, flags, dir_fd=parent)
        except OSError as exc:
            if exc.errno in (errno.ELOOP, errno.ENOTDIR):
                raise PermissionError(errno.EPERM, "symlink or non-directory in detail log root "
                                      "path", path) from exc
            raise OSError(exc.errno, exc.strerror, path) from exc
        os.close(parent)
        return child

    path = "/"
    fd = os.open(path, flags)
    try:
        for name in [part for part in home.split("/") if part]:
            info = os.fstat(fd)
            if not (info.st_uid in (0, euid) and not info.st_mode & writable
                    or info.st_uid == 0 and info.st_mode & stat.S_ISVTX):
                raise PermissionError(errno.EPERM, "directory above the home is not owned by "
                                      "root or this uid, or others can write it", path)
            path = os.path.join(path, name)
            fd = descend(fd, name, path)
        for name in ("",) + _DETAIL_ROOT_PARTS:
            if name:
                path = os.path.join(path, name)
                try:
                    os.mkdir(name, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                except OSError as exc:
                    raise OSError(exc.errno, exc.strerror, path) from exc
                fd = descend(fd, name, path)
            info = os.fstat(fd)
            private = name == _DETAIL_ROOT_PARTS[-1]
            if (not stat.S_ISDIR(info.st_mode) or info.st_uid != euid
                    or info.st_mode & (0o077 if private else writable)):
                raise PermissionError(errno.EPERM, "detail log root path component must be owned "
                                      "by this uid with no group or other %s"
                                      % ("access" if private else "write bit"), path)
        try:
            os.stat(".git", dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise PermissionError(errno.EPERM, "detail log root holds a .git entry",
                                  os.path.join(root, ".git"))
        # Again whether or not a directory was created, immediately before the write, so a
        # .git planted at a level that already existed, after the first check, is refused too.
        _refuse_git_tree(root, timeout - (time.monotonic() - started))
    except BaseException:
        os.close(fd)
        raise
    return fd, root


def _log_session(payload):
    """The Stop payload's session_id when it can name a detail log; raises ValueError otherwise
    (checked before the detail is built, and again by _write_detail_log)."""
    session = payload.get("session_id") if isinstance(payload, dict) else None
    if not isinstance(session, str) or not _SESSION_ID.fullmatch(session):
        raise ValueError("no usable session_id in the Stop payload")
    return session


def _detail_text(reason, actionable):
    """The full detail: decide()'s reason plus every actionable item's ID and title, escaped
    with _printable. The reason alone when the items cannot be rendered. Built only inside
    _bounded_write's deadline-controlled thread, so its unbounded size cannot delay the refusal.
    When the reason's declared-wait line could not carry the whole touch command
    (_declared_wait_line), the command follows the reason on a line of its own, uncut."""
    try:
        if any(line in _WAIT_UNLOGGED for line in reason.split("\n")):
            reason += "\nDeclared wait command: touch " + _shell_word(_grc_escape_file())
        return reason + "\nActionable items (%d):" % len(actionable) + "".join(
            "\n  - %s: %s" % (_printable(iid), _printable(title)) for iid, title in actionable)
    except Exception:
        return reason


def _write_detail_log(detail, payload, timeout=_DETAIL_TIMEOUT_S):
    """Append the full refusal detail to this session's log under the detail log root
    (_open_detail_root) and return its path, or raise. A root inside this checkout or inside any
    git working tree or bare repository is refused before anything is created, as in
    block-turn-end-with-outstanding-work.py; the store (_GRC_STATE_FILE) is never written."""
    started = time.monotonic()
    session = _log_session(payload)
    top, directory = _open_detail_root(Path(_GRC_REPO_ROOT),
                                       timeout - (time.monotonic() - started))
    try:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        name = "%s.%s.log" % (_DETAIL_NAME, session[:_SESSION_PREFIX_CHARS])
        return _append_private(top, directory, name,
                               "=== %s stop-guard-unattended session %s ===\n%s\n\n"
                               % (stamp, session, detail))
    finally:
        os.close(top)


def _write_bound():
    """Seconds the detail log write may take: _DETAIL_TIMEOUT_S, cut to the time left before
    _RUN_DEADLINE when main() has set one (TIME BUDGET)."""
    if _RUN_DEADLINE is None:
        return _DETAIL_TIMEOUT_S
    return min(_DETAIL_TIMEOUT_S, _RUN_DEADLINE - time.monotonic())


def _bounded_write(reason, actionable, payload):
    """Build the full detail (_detail_text) and write it (_write_detail_log) in one daemon thread
    joined for at most _write_bound() seconds, so neither a stalled filesystem, a very large item
    list nor a slow producer earlier in the run can push the refusal past the hook timeout. The
    budget and the session_id are checked first: with less than _MIN_WRITE_S left, or no usable
    session_id, no detail is built and no thread is started. A timeout, a spent budget or an
    unusable session raises and the caller fails open."""
    import threading
    bound = _write_bound()
    if bound < _MIN_WRITE_S:
        raise TimeoutError(errno.ETIMEDOUT, "run time budget spent (%.2fs left)" % max(bound, 0.0))
    _log_session(payload)
    started = time.monotonic()
    box = {}

    def work():
        try:
            detail = _detail_text(reason, actionable)
            box["path"] = _write_detail_log(detail, payload,
                                            bound - (time.monotonic() - started))
        except Exception as exc:
            box["error"] = exc

    worker = threading.Thread(target=work, name="stop-hook-detail-log", daemon=True)
    worker.start()
    worker.join(bound)
    if worker.is_alive():
        raise TimeoutError(errno.ETIMEDOUT, "detail log write exceeded %.2fs" % bound)
    if "error" in box:
        raise box["error"]
    return box["path"]


def _route_refusal(reason, actionable, live_groups, payload, required=None):
    """Short diagnostic after a successful log write; the count-only fallback otherwise. The
    full detail is built inside _bounded_write, never here (a very large item list with the
    budget nearly spent still yields the fallback at once). ``required`` is decide()'s
    required live count, passed on to the short form."""
    state = "not written"
    try:
        path = _bounded_write(reason, actionable, payload)
        state = "written but not summarized"
        return _short_refusal(len(actionable), live_groups, path, _grc_escape_file(),
                              required=required)
    except Exception as exc:
        try:
            return _fallback_refusal(reason, len(actionable), state, exc)
        except Exception:
            return reason


def run(root, payload):
    """Core: exit 2 (block) iff this is the ORCHESTRATOR session, unattended, not a stop-hook continuation,
    and pipeline shows actionable work without enough live dispatches; else 0.
    Registry read failures fail open except boundary-byte failures, which discard the first row
    and continue counting; unobservable groups do not count. Read the slot share only when
    actionable work exists and the live count was observable."""
    if not is_orchestrator_session(root):
        return 0  # a dispatched worker (or an unconfirmable owner) -> allow; this guard binds the orchestrator only
    mode = read_operating_mode(root)
    stop_hook_active = bool(payload.get("stop_hook_active")) if isinstance(payload, dict) else False
    actionable = None
    if mode == "unattended" and not stop_hook_active:
        actionable = actionable_items(root)  # only compute when it can change the outcome
    live_groups = live_dispatch_groups() if actionable else 0
    share = (None, "skipped")
    if actionable and live_groups is not None:
        try:
            share = read_slot_share()
        except Exception:
            share = (None, "unread")
    block, reason = decide(mode, stop_hook_active, actionable, live_groups, share)
    if block:
        # Wording and routing only: the full detail goes to the session log and the diagnostic
        # is three lines, or the reason with the count only when the log cannot be written.
        reason = _route_refusal(reason, actionable, live_groups, payload, _required_groups(share))
    if reason:
        import warnings
        with warnings.catch_warnings():
            # A detail-log thread that is still exiting (or abandoned after its timeout) would
            # make os.fork() in _diagnostic warn on stderr; the diagnostic itself is unchanged.
            warnings.filterwarnings("ignore", r".*is multi-threaded, use of fork\(\)",
                                    DeprecationWarning)
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
    global _RUN_DEADLINE
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    _RUN_DEADLINE = _LOADED_AT + _RUN_BUDGET_S  # TIME BUDGET: the run, not only the write
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


# The check tests/test_linters.py (StopHookDetailRootTests._unsafe_above) applies to TMPDIR before
# a real detail log write, the same source (a test compares them), used by the self-test's own
# real writes, so the self-test fails or skips for exactly the reason the suite gives.
def _unsafe_above(path):
    """Why a directory above `path` ("/" first) is a symlink, cannot be opened for reading by
    this uid, or fails the root's rule for directories above the home (owned by root or this
    uid with no group or other write bit, or root-owned and sticky), or None."""
    import stat
    euid = os.geteuid()
    for directory in reversed(Path(path).parents):
        info = os.lstat(directory)
        if stat.S_ISLNK(info.st_mode):
            return "%s is a symlink" % directory
        if not os.access(directory, os.R_OK | os.X_OK):
            return ("%s cannot be opened for reading by uid %d (the hook opens every "
                    "directory on the path)" % (directory, euid))
        if not (info.st_uid in (0, euid) and not info.st_mode & 0o022
                or info.st_uid == 0 and info.st_mode & stat.S_ISVTX):
            return ("%s has owner uid %d and mode %04o (the rule needs root or uid %d as owner "
                    "with no group or other write bit, or a root-owned sticky directory)"
                    % (directory, info.st_uid, stat.S_IMODE(info.st_mode), euid))
    return None


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

    production_share_path = "/opt/" + "orch-operator/" + "slot-shares.json"
    share_declarations = (_SLOT_SHARES_FILE, _SLOT_SHARE_PROJECT, _SLOT_SHARE_EXPECT_UID,
                          _SLOT_SHARE_MAX, _SLOT_SHARE_MAX_BYTES)
    share_opens = []
    recording = True

    # This lexical recorder does not recognize a leading double slash, relative paths,
    # directory-descriptor opens, symlinked directories, or opens in child processes.
    def record_share_open(event, args):
        if recording and event == "open" and args:
            try:
                matches = os.fsdecode(os.path.normpath(os.fspath(args[0]))) == production_share_path
            except Exception:
                return  # Audit callbacks must tolerate non-path arguments and broken PathLike objects.
            if matches:
                share_opens.append(production_share_path)

    sys.addaudithook(record_share_open)

    def self_test_status(result, share_opens):
        return 0 if result.wasSuccessful() and not share_opens else 1

    def _write_share(path, data):
        Path(path).write_bytes(data if isinstance(data, bytes) else _json.dumps(data).encode())
        os.chmod(path, 0o644)
        return path

    def rewrite_share(test, source, path):
        for anchor, replacement in (
                ('_SLOT_SHARES_FILE = "' + production_share_path + '"',
                 "_SLOT_SHARES_FILE = %r" % str(path)),
                ("_SLOT_SHARE_EXPECT_UID = 0", "_SLOT_SHARE_EXPECT_UID = (%r)" % os.geteuid())):
            test.assertEqual(source.count(anchor + "\n"), 1)
            source = source.replace(anchor + "\n", replacement + "\n")
            test.assertNotIn(anchor + "\n", source)
            test.assertIn(replacement + "\n", source)
        test.assertNotIn(production_share_path, source)
        return source

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
            # Real process boundaries: T.test_diagnostic_fork_delivery and
            # T.test_diagnostic_fork_drops_terminals run hook copies as processes (3b123).
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
            script = "#!/usr/bin/env python3\nimport sys\nprint(%r)\nsys.exit(%d)\n" % (producer_lines, producer_exit)
            _write(p, script)
            os.chmod(p, os.stat(p).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    class T(unittest.TestCase):
        def setUp(self):
            # Never let a host's live fleet affect either in-process or subprocess tests.
            self.registry = tempfile.TemporaryDirectory()
            self.addCleanup(self.registry.cleanup)
            patcher = mock.patch.dict(globals(), _KILLREG_DIR=self.registry.name,
                                      _SLOT_SHARES_FILE=os.path.join(self.registry.name, "slot-shares.absent"),
                                      _SLOT_SHARE_EXPECT_UID=os.geteuid())
            patcher.start()
            self.addCleanup(patcher.stop)
            owner_env = mock.patch.dict(os.environ, {"ORCH_OWNER": "fixture"})
            owner_env.start()
            self.addCleanup(owner_env.stop)
            # No inherited GRC_DROP_ROOT reaches decide()'s declared-wait line, here or in a hook
            # process a test starts from os.environ (owner_env restores it after the test); a
            # test that needs the setting sets its own. The hint test keeps the environment this
            # hook loaded with, since MODE_SET_HINT was resolved from it then.
            if self._testMethodName != "test_grc_hint_names_the_file_the_reader_uses":
                os.environ.pop("GRC_DROP_ROOT", None)
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
                            self.assertTrue(decide("unattended", False, [("1", "sample")], count, (None, "absent"))[0])
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
            block, reason = decide("unattended", False, [("1", "a"), ("3", "c")], 0, (None, "absent"))
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
                block, reason = decide("unattended", False, self._items(n), 0, (None, "absent"))
                self.assertTrue(block)
                lines = reason.split("\n")
                self.assertLessEqual(len(lines), 5, "n=%d gave %d lines" % (n, len(lines)))

        def test_reason_lines_short_even_with_long_titles(self):
            for n in (1, 6, 500):
                block, reason = decide("unattended", False, self._items(n, "a long title " * 40), 0, (None, "absent"))
                self.assertTrue(block)
                for line in reason.split("\n"):
                    self.assertLessEqual(len(line), 160, "n=%d line too long: %r" % (n, line))
                self.assertNotIn("a long title", reason)  # titles stay in the producer output

        def test_reason_carries_count_and_continue_instruction(self):
            with mock.patch.dict(globals(), _grc_escape_file=lambda: "/drop/.allow-idle-stop"):
                block, reason = decide("unattended", False, self._items(37), 0, (None, "absent"))
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
            block, reason = decide("unattended", False, self._items(3), 0, (None, "absent"))
            self.assertTrue(block)
            self.assertNotIn("legitimately", reason)  # not framed as the only legitimate stop
            self.assertIn("at least 3 live owned dispatch groups", reason)
            self.assertIn("[BLOCKED:<reason>] tag with a granted approvals row", reason)  # grc's grammar (3b113 QA r2)
            # The complete await/exhaustion alternatives fit before the line clamp.
            line4 = reason.split("\n")[3]
            self.assertLessEqual(len(line4), 150, "line 4 has no margin under the 160 clamp: %r" % line4)

        def test_decide_allow_stop_hook_active(self):
            self.assertFalse(decide("unattended", True, [("1", "a")], 0, (None, "skipped"))[0])

        def test_decide_allow_exhausted(self):
            self.assertFalse(decide("unattended", False, [], 0, (None, "skipped"))[0])

        def test_decide_allow_indeterminate(self):
            self.assertFalse(decide("unattended", False, None, 0, (None, "skipped"))[0])

        def test_decide_allow_attended(self):
            self.assertFalse(decide("attended", False, [("1", "a")], 0, (None, "skipped"))[0])

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
        def _hook_copy(self, d):
            """Copy this hook to <d>/.claude/hooks/hook.py, reading this test's fixture registry."""
            hooks = os.path.join(d, ".claude", "hooks")
            os.makedirs(hooks)
            source = Path(__file__).read_text()
            seam = '_KILLREG_DIR = "/run/orch-workers"'
            self.assertEqual(source.count(seam + "\n"), 1)
            source = source.replace(seam + "\n", "_KILLREG_DIR = %r\n" % self.registry.name)
            path = _write_share(os.path.join(d, "slot-shares.json"),
                                {"schema": 1, "default": 2, "shares": {"grc": 2}})
            Path(hooks, "hook.py").write_text(rewrite_share(self, source, path))
            return os.path.join(hooks, "hook.py")

        def _subproc(self, mode, producer_lines, payload):
            import subprocess
            with tempfile.TemporaryDirectory() as d:
                hook = self._hook_copy(d)
                build(d, mode=mode, producer_lines=producer_lines)
                with tempfile.TemporaryDirectory() as foreign:
                    r = subprocess.run([sys.executable, "-I", hook],
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

        # ---- diagnostic transport across real process boundaries (3b123) ----
        def _blocking_hook(self, stderr):
            """Run a hook copy that blocks an unattended stop (actionable work, no live groups) with the
            given stderr; return its exit status and any stderr captured through a pipe."""
            with tempfile.TemporaryDirectory() as d:
                hook = self._hook_copy(d)
                build(d, mode=UNATT, producer_lines=ITEMS_MIXED)
                env = {k: v for k, v in os.environ.items() if k not in ("ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}
                proc = subprocess.Popen([sys.executable, "-I", "-B", hook], stdin=subprocess.PIPE,
                                        stdout=subprocess.DEVNULL, stderr=stderr, cwd=d, env=env)
                _out, err = proc.communicate(_json.dumps({"stop_hook_active": False}).encode(), timeout=60)
                return proc.returncode, err

        def _require_diagnostic_calls(self):
            """Report refused diagnostic calls by transport in a real forked child."""
            import select
            import socket
            transports = ("pipe", "socket", "regular file")
            report_r = report_w = sink_r = sink_w = -1
            ours = theirs = None
            try:
                report_r, report_w = os.pipe()
                sink_r, sink_w = os.pipe()
                ours, theirs = socket.socketpair()
                try:
                    child = os.fork()
                except OSError as exc:
                    return {name: "os.fork(): %s" % exc for name in transports}
                if child == 0:
                    refused = {}
                    try:
                        step = "os.listdir('/proc/self/fd')"
                        try:
                            os.listdir("/proc/self/fd")
                            step = "os.setsid()"
                            os.setsid()
                        except (OSError, ValueError) as exc:
                            refused = {name: "%s: %s" % (step, exc) for name in transports}
                        if not refused:
                            step = "os.open('/proc/self/fd/<pipe>')"
                            try:
                                fd = os.open("/proc/self/fd/%d" % sink_w,
                                             os.O_WRONLY | os.O_NONBLOCK | os.O_CLOEXEC)
                                try:
                                    step = "select.select(pipe)"
                                    if not select.select([], [fd], [], 1)[1]:
                                        raise OSError("pipe not writable")
                                    step = "os.write(pipe)"
                                    os.write(fd, b"x")
                                finally:
                                    os.close(fd)
                            except (OSError, ValueError) as exc:
                                refused["pipe"] = "%s: %s" % (step, exc)
                            step = "socket.socket(fileno=os.dup(socket))"
                            try:
                                with socket.socket(family=socket.AF_UNSPEC, type=0, proto=0,
                                                   fileno=os.dup(theirs.fileno())) as peer:
                                    step = "select.select(socket)"
                                    if not select.select([], [peer.fileno()], [], 1)[1]:
                                        raise OSError("socket not writable")
                                    step = "socket.sendmsg()"
                                    peer.sendmsg([b"x"], [], socket.MSG_DONTWAIT)
                            except (OSError, ValueError) as exc:
                                refused["socket"] = "%s: %s" % (step, exc)
                    finally:
                        try:
                            os.write(report_w, _json.dumps(refused).encode()[:select.PIPE_BUF])
                        finally:
                            os._exit(0)
                os.close(report_w)
                report_w = -1
                deadline = time.monotonic() + 3
                while True:
                    waited, status = os.waitpid(child, os.WNOHANG)
                    if waited:
                        break
                    if time.monotonic() >= deadline:
                        os.kill(child, signal.SIGKILL)
                        os.waitpid(child, 0)
                        return {name: "probe child timed out" for name in transports}
                    time.sleep(0.01)
                report = os.read(report_r, select.PIPE_BUF).decode(errors="replace")
            except OSError as exc:
                return {name: "probe setup: %s" % exc for name in transports}
            finally:
                for fd in (report_r, report_w, sink_r, sink_w):
                    if fd >= 0:
                        os.close(fd)
                if ours is not None:
                    ours.close()
                if theirs is not None:
                    theirs.close()
            if not os.WIFEXITED(status) or os.WEXITSTATUS(status):
                return {name: "probe child wait status %d" % status for name in transports}
            try:
                return _json.loads(report)
            except (ValueError, TypeError):
                return {name: "invalid probe report: %r" % report for name in transports}

        def test_diagnostic_fork_delivery(self):
            # 3b123: capture_stderr runs the writer's child branch inline; here the real fork delivers.
            # Only the forked child writes, so the refusal arriving on a pipe, a socket and a regular file
            # shows the child's delivery, and each exit status still carries the block.
            import socket
            unavailable = self._require_diagnostic_calls()
            marker = b"BLOCKED (stop-guard-unattended):"
            rc, err = self._blocking_hook(subprocess.PIPE)
            with self.subTest(transport="pipe"):
                self.assertEqual(rc, 2, err)
                if "pipe" in unavailable:
                    self.skipTest("pipe delivery unavailable: %s" % unavailable["pipe"])
                self.assertIn(marker, err)
            ours, theirs = socket.socketpair()
            with ours:
                with theirs:
                    rc, _err = self._blocking_hook(theirs.fileno())
                with self.subTest(transport="socket"):
                    self.assertEqual(rc, 2)
                    if "socket" in unavailable:
                        self.skipTest("socket delivery unavailable: %s" % unavailable["socket"])
                    ours.settimeout(30)
                    received = chunk = ours.recv(4096)
                    while chunk:  # EOF once the hook and its writer child have both closed the socket
                        chunk = ours.recv(4096)
                        received += chunk
                    self.assertIn(marker, received)
            with tempfile.TemporaryFile() as sink:
                rc, _err = self._blocking_hook(sink.fileno())
                with self.subTest(transport="regular file"):
                    self.assertEqual(rc, 2)
                    if "regular file" in unavailable:
                        self.skipTest("regular file delivery unavailable: %s" % unavailable["regular file"])
                    deadline = time.monotonic() + 10  # the writer child may finish after the hook exits
                    while marker not in os.pread(sink.fileno(), 4096, 0) and time.monotonic() < deadline:
                        time.sleep(0.01)
                    self.assertIn(marker, os.pread(sink.fileno(), 4096, 0))

        def test_diagnostic_fork_drops_terminals(self):
            # 3b123: a terminal stderr receives no diagnostic (it is never written or reopened), and the
            # exit status alone carries the block.
            import select
            try:
                master, slave = os.openpty()
            except OSError as exc:
                self.skipTest("no pseudo-terminal available: %s" % exc)
            try:
                rc, _err = self._blocking_hook(slave)
                self.assertEqual(rc, 2)
                # The slave stays open here, so a late write would wait on the master; the writer's own
                # deadline is 0.2 seconds.
                leaked = os.read(master, 4096) if select.select([master], [], [], 1.0)[0] else b""
                self.assertEqual(leaked, b"")
            finally:
                os.close(master)
                os.close(slave)

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


    def fixture_home(case, parent):
        """A fixture home <parent>/home, mode 0700, for a real detail log write. When a directory
        above it fails the check tests/test_linters.py applies (_unsafe_above: a symlink, a
        directory this uid cannot open for reading, or one outside the detail log root's owner
        and mode rule), TMPDIR on this host cannot hold a safe root: ``case`` fails with the
        reason, or skips with it when _UNSAFE_TMP_SKIP_ENV is set to 1."""
        home = os.path.join(parent, "home")
        os.mkdir(home, 0o700)
        os.chmod(home, 0o700)
        why = _unsafe_above(home)
        if why is not None:
            why = "this host cannot provide a safe temporary home root: " + _printable(why)
            if os.environ.get(_UNSAFE_TMP_SKIP_ENV) == "1":
                case.skipTest("%s (%s=1)" % (why, _UNSAFE_TMP_SKIP_ENV))
            case.fail("%s; set %s=1 to skip instead" % (why, _UNSAFE_TMP_SKIP_ENV))
        return home

    class GRCAdapterTests(unittest.TestCase):
        # A's adapter cases also isolate the new registry from the host.
        setUp = T.setUp

        def test_decide_message_bounded(self):
            # Terse-console change (maintainer-directed 2026-09-16): the block message
            # emits the COUNT only, never the item enumeration, so its length does not
            # grow with the backlog size and item titles never reach the console.
            many = [("%d" % i, "title%d" % i) for i in range(500)]
            _b, reason = decide("unattended", False, many, 0, (None, "absent"))
            self.assertNotIn("title", reason)
            self.assertIn("500", reason)
            self.assertLess(len(reason), 1200)

        def test_route_logs_detail_and_returns_three_lines(self):
            # The real write lands under a fixture home in TMPDIR (_DETAIL_HOME); the console
            # assertion follows the PATH BUDGET, so the result does not depend on how long
            # TMPDIR is.
            # A short declared-wait directory, so the escape path fits the short form whatever
            # the checkout's path (test_route_at_a_long_checkout_path is the long path).
            many = [("%d" % i, "title%d" % i) for i in range(500)]
            with tempfile.TemporaryDirectory() as d, \
                    mock.patch.dict(os.environ, GRC_DROP_ROOT="/w"):
                _b, reason = decide("unattended", False, many, 1, (None, "absent"))
                home = fixture_home(self, d)
                with mock.patch.dict(globals(), _DETAIL_HOME=home):
                    short = _route_refusal(reason, many, 1, {"session_id": "self-test-1"})
                escape = _grc_escape_file()
                log = os.path.join(home, *_DETAIL_ROOT_PARTS, _DETAIL_SUBDIR,
                                   "stop-guard.self-test-1.log")
                self.assertEqual(stat.S_IMODE(os.lstat(log).st_mode), 0o600)
                with open(log, encoding="utf-8") as fh:
                    logged = fh.read()
            if len(log) <= _MAX_LINE_CHARS - len("WHY: below the group floor; log: "):
                self.assertEqual(short, _short_refusal(500, 1, log, escape))
                self.assertEqual(len(short.splitlines()), 3)
            else:
                self.assertIn("NOTE: detail log written but not summarized (ValueError", short)
            self.assertNotIn("title", short)
            self.assertIn(reason, logged)
            self.assertIn("  - 499: title499", logged)
            self.assertIn("session self-test-1 ===", logged)

        def test_route_logs_under_home_when_store_is_git_tree(self):
            # The store sits inside a git working tree; the log still lands under the clean
            # fixture home's detail root, and nothing is written in the store.
            items = [("X-1", "t")]
            _b, reason = decide("unattended", False, items, 1, (None, "absent"))
            with tempfile.TemporaryDirectory() as d:
                home = fixture_home(self, d)
                store = os.path.join(d, "outer", "private")
                os.makedirs(store)
                os.mkdir(os.path.join(d, "outer", ".git"))
                with mock.patch.dict(globals(), _DETAIL_HOME=home,
                                     _GRC_STATE_FILE=os.path.join(store, "session-state.md")):
                    routed = _route_refusal(reason, items, 1, {"session_id": "self-test-2"})
                log = os.path.join(home, *_DETAIL_ROOT_PARTS, _DETAIL_SUBDIR,
                                   "stop-guard.self-test-2.log")
                self.assertEqual(stat.S_IMODE(os.lstat(log).st_mode), 0o600)
                self.assertEqual(os.listdir(store), [])
            self.assertNotIn("NOTE: detail log not written", routed)
            self.assertNotIn("inside a git working tree", routed)

        def test_short_form_on_a_short_fixed_directory(self):
            # A short fixed directory, so this result never depends on TMPDIR.
            log = "/s/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            escape = "/w/.allow-idle-stop"
            short = _short_refusal(500, 1, log, escape)
            self.assertEqual(len(short.splitlines()), 3)
            self.assertEqual(short.splitlines()[2],
                             "CONSIDER INSTEAD: continue; wait (once, after recording the "
                             "blocker): touch %s; log: %s" % (escape, log))
            store = "/" + "s" * 81
            fits = store + "/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            lines = _short_refusal(500, 1, fits, escape).splitlines()
            self.assertEqual(len(lines), 3)
            self.assertEqual(lines[1], "WHY: below the group floor; log: " + fits)
            self.assertTrue(lines[2].endswith("(once, after recording the blocker): touch " + escape))
            with self.assertRaises(ValueError):
                _short_refusal(500, 1, "/s" + fits, escape)
            # Round 5: an escape path too long for the condition keeps the path and says the
            # condition is in the log; 101 characters fit, 102 fall back.
            for wide in ("/" + "w" * 89, "/" + "w" * 100):
                lines = _short_refusal(500, 1, log, wide).splitlines()
                self.assertEqual(lines[2], "CONSIDER INSTEAD: continue; wait (condition in log): "
                                           "touch " + wide)
                self.assertTrue(lines[1].endswith(" " + log))
            with self.assertRaises(ValueError):
                _short_refusal(500, 1, log, "/" + "w" * 101)

        def test_short_form_refuses_a_non_printable_log_path(self):
            for odd in ("\n", "\r", "\x1b[2J"):
                with self.assertRaises(ValueError):
                    _short_refusal(1, 0, "/s" + odd + "/stop-guard.x.log", "/w/.allow-idle-stop")
                with self.assertRaises(ValueError):
                    _short_refusal(1, 0, "/s/stop-guard.x.log", "/w" + odd + "/.allow-idle-stop")

        def test_short_form_shows_the_required_count(self):
            # decide()'s required count reaches the WHY line whenever a wording carrying it fits;
            # the shortest wording still takes the longest log path (the PATH BUDGET holds).
            for share, required in (((None, "absent"), 3), ((2, "default"), 3), ((7, "grc"), 7)):
                self.assertEqual(_required_groups(share), required)
            # Parity with decide()'s own statement of the rule: it blocks exactly below this count.
            for value in (None, 1, 2, 3, 4, 7):
                for live in range(9):
                    block, _reason = decide("unattended", False, [("1", "t")], live, (value, "x"))
                    self.assertEqual(block, live < _required_groups((value, "x")), (value, live))
            log = "/s/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            escape = "/w/.allow-idle-stop"
            lines = _short_refusal(500, 1, log, escape, required=7).splitlines()
            self.assertEqual(lines[1], "WHY: not whole-set exhaustion, and the live owned dispatch "
                                       "group count (1) is below the required count (7).")
            wide = "/w/" + "w" * 30 + "/.allow-idle-stop"
            lines = _short_refusal(500, 1, log, wide, required=7).splitlines()
            self.assertEqual(lines[1], "WHY: the live owned dispatch group count (1) is below the "
                                       "required count (7); detail log: " + log)
            mid = "/" + "s" * 70 + "/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            lines = _short_refusal(500, 1, mid, escape, required=7).splitlines()
            self.assertEqual(lines[1], "WHY: 1 of 7 required groups live; log: " + mid)
            fits = "/" + "s" * 81 + "/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            lines = _short_refusal(500, 1, fits, escape, required=7).splitlines()
            self.assertEqual(lines[1], "WHY: live 1/7 required; log: " + fits)
            # Round 3 (codex W2): the compact wording keeps both counts at every log path the
            # count-free wording took, and at four characters more.
            wider = "/" + "s" * 85 + "/" + _DETAIL_SUBDIR + "/stop-guard.0123456789ab.log"
            lines = _short_refusal(500, 1, wider, escape, required=7).splitlines()
            self.assertEqual(lines[1], "WHY: live 1/7 required; log: " + wider)
            for text in (_short_refusal(500, 1, m, e, required=7) for m, e in
                         ((log, escape), (log, wide), (mid, escape), (fits, escape))):
                self.assertEqual(len(text.splitlines()), 3)
                self.assertLessEqual(max(map(len, text.splitlines())), _MAX_LINE_CHARS)

        def test_spent_run_budget_skips_the_write(self):
            items = [("X-1", "t")]
            _b, reason = decide("unattended", False, items, 0, (None, "absent"))
            writer = mock.Mock(return_value="/s/x.log")
            with mock.patch.dict(globals(), _RUN_DEADLINE=time.monotonic() + 0.1,
                                 _write_detail_log=writer):
                routed = _route_refusal(reason, items, 0, {"session_id": "s-1"})
            writer.assert_not_called()
            self.assertIn("NOTE: detail log not written (TimeoutError", routed)
            self.assertIn("run time budget spent", routed)

        def test_route_without_session_keeps_reason_and_count(self):
            items = [("X-917", "zq-title-probe")]
            # A short declared-wait directory, so decide()'s wait line is the whole command and
            # the fallback shows the reason unchanged, whatever the checkout's path (the long
            # path is test_route_at_a_long_checkout_path).
            with mock.patch.dict(os.environ, GRC_DROP_ROOT="/w"):
                _b, reason = decide("unattended", False, items, 0, (None, "absent"))
                with mock.patch.dict(globals(), _append_private=mock.Mock()) as patched:
                    routed = _route_refusal(reason, items, 0, {})
                    patched["_append_private"].assert_not_called()
            self.assertTrue(routed.startswith(reason + "\nNOTE: detail log not written (ValueError"))
            self.assertIn("\nActionable items: 1 ", routed)
            self.assertNotIn("zq-title-probe", routed)  # #2291: count only on the fallback too
            self.assertNotIn("X-917", routed)

        def test_route_at_a_long_checkout_path(self):
            # The checkout's parent is nested directories in a temporary directory, so the
            # default declared-wait path is longer than one console line. After a written log
            # the escape path does not fit the short form, so the fallback shows decide()'s
            # reason, whose wait line names the sentinel's directory and points at the log, and
            # the log has the whole command; without a log the fallback rewords that line to say
            # no log was written. Neither shows any part of the path.
            items = [("X-1", "t")]
            log = "/s/" + _DETAIL_SUBDIR + "/stop-guard.self-test-3.log"
            with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ):
                os.environ.pop("GRC_DROP_ROOT", None)
                parent = os.path.join(d, *("nested-%02d-%s" % (n, "d" * 30) for n in range(5)))
                os.makedirs(parent)
                escape = os.path.join(parent, "grc_working", ".allow-idle-stop")
                self.assertGreater(len(escape), _MAX_LINE_CHARS)
                with mock.patch.dict(globals(), _GRC_PARENT=parent):
                    self.assertEqual(_grc_escape_file(), escape)
                    _b, reason = decide("unattended", False, items, 0, (None, "absent"))
                    with mock.patch.dict(globals(), _bounded_write=mock.Mock(return_value=log)):
                        written = _route_refusal(reason, items, 0, {"session_id": "self-test-3"})
                    unlogged = _route_refusal(reason, items, 0, {})
                    detail = _detail_text(reason, items)
            wait = _WAIT_TOO_LONG % ("<repo-parent>/grc_working", _WAIT_LOGGED)
            self.assertIn(wait, reason.split("\n"))
            self.assertTrue(written.startswith(reason + "\nNOTE: detail log written but not "
                                               "summarized (ValueError"), written)
            self.assertIn("Declared wait command: touch " + _shell_word(escape), detail)
            self.assertTrue(unlogged.startswith(reason.replace(wait, _WAIT_UNLOGGED[wait])
                                                + "\nNOTE: detail log not written (ValueError"),
                            unlogged)
            for text in (written, unlogged):
                self.assertNotIn(parent, text)
                self.assertNotIn("touch /", text)
                self.assertLessEqual(max(map(len, text.splitlines())), _MAX_LINE_CHARS)

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
            # 3b101: the lease and sentinel sit beside the checkout unless overridden.
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
            out = subprocess.run([sys.executable, "-I", "-B", "-c", code, __file__], capture_output=True, text=True,
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
            import subprocess, tempfile
            with tempfile.TemporaryDirectory() as parent:
                main_root = os.path.join(parent, "grc_library")
                wt_root = os.path.join(parent, "wt-x")
                # 3b781 r4 (claude W): every hook copy carries a fixture fleet path (an
                # absent file under this fixture tree), the same redirection the launcher
                # test applies, so no copy can read the live fleet file even off the
                # passing path; the live literal must be absent from each copy.
                source = Path(__file__).read_text(encoding="utf-8")
                live_line = '_FLEET_MODE_FILE = "/opt/' + 'orch-operator/operating-mode"'
                self.assertEqual(source.count(live_line), 1)
                patched_source = source.replace(
                    live_line, "_FLEET_MODE_FILE = %r" % os.path.join(parent, "no-fleet-file"))
                for r in (main_root, wt_root):
                    os.makedirs(os.path.join(r, ".claude", "hooks"))
                    hook = os.path.join(r, ".claude", "hooks", os.path.basename(__file__))
                    Path(hook).write_text(patched_source, encoding="utf-8")
                    self.assertNotIn(live_line, Path(hook).read_text(encoding="utf-8"), r)
                os.makedirs(os.path.join(main_root, ".git"))
                with open(os.path.join(wt_root, ".git"), "w", encoding="utf-8") as fh:
                    fh.write("gitdir: " + os.path.join(main_root, ".git", "worktrees", "wt-x") + "\n")
                drop = os.path.join(parent, "grc_working")
                os.makedirs(drop)
                sentinel = os.path.join(drop, ".allow-idle-stop")
                env = {k: v for k, v in os.environ.items() if k not in ("GRC_DROP_ROOT", "GRC_STORE")}
                for r, want_present in ((wt_root, True), (main_root, False)):
                    open(sentinel, "w").close()
                    subprocess.run([sys.executable, "-I", "-B", os.path.join(r, ".claude", "hooks", os.path.basename(__file__))],
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

        def test_grc_escape_is_consumed_before_the_payload_parse(self):
            # 3b123: main() spends the declared wait before it reads or parses the payload, so the malformed,
            # empty and non-object fail-open returns consume it too. The hook runs from a temporary main
            # checkout, so this holds in a linked worktree as well. A mutant with the escape moved after the
            # payload's fail-open return must leave the sentinel on exactly those payloads; "{}" alone (the
            # payload of the sentinel test above) cannot tell the two orders apart.
            source = Path(__file__).read_text(encoding="utf-8")
            escape = ("    if _grc_consume_escape(repo_root()):\n        return 0  # grc one-shot declared-wait"
                      " sentinel consumed -> allow this stop (before any parse)\n")
            parsed = "    return run(repo_root(), payload)\n"
            self.assertEqual(source.count(escape), 1)
            self.assertEqual(source.count(parsed), 1)
            mutant = source.replace(escape, "").replace(parsed, escape + parsed)
            env = {k: v for k, v in os.environ.items()
                   if k not in ("GRC_DROP_ROOT", "GRC_STORE", "ORCH_VERIFY_OWNER", "CLAUDE_CONFIG_DIR")}
            payloads = ("not-json", "", "[1, 2, 3]", "{}")
            got = {}
            with tempfile.TemporaryDirectory() as parent:
                os.makedirs(os.path.join(parent, "grc_working"))
                sentinel = os.path.join(parent, "grc_working", ".allow-idle-stop")
                # 3b781 r4 (claude N2): both copies carry a fixture fleet path (an
                # absent file under this fixture tree), the same redirection the
                # launcher test applies; the live literal must be absent from each copy.
                live_line = '_FLEET_MODE_FILE = "/opt/' + 'orch-operator/operating-mode"'
                fixture_line = "_FLEET_MODE_FILE = %r" % os.path.join(parent, "no-fleet-file")
                for name, text in (("grc_library", source), ("mutant", mutant)):
                    self.assertEqual(text.count(live_line), 1, name)
                    text = text.replace(live_line, fixture_line)
                    root = os.path.join(parent, name)
                    os.makedirs(os.path.join(root, ".git"))  # a main checkout, whichever checkout runs this
                    hook = os.path.join(root, ".claude", "hooks", os.path.basename(__file__))
                    os.makedirs(os.path.dirname(hook))
                    Path(hook).write_text(text, encoding="utf-8")
                    self.assertNotIn(live_line, Path(hook).read_text(encoding="utf-8"), name)
                    for payload in payloads:
                        open(sentinel, "w").close()
                        out = subprocess.run([sys.executable, "-I", "-B", hook], input=payload, text=True,
                                             capture_output=True, env=env, cwd=root, timeout=60)
                        got[name, payload] = (out.returncode, os.path.exists(sentinel))
            want = {("grc_library", p): (0, False) for p in payloads}
            want.update({("mutant", p): (0, p != "{}") for p in payloads})
            self.assertEqual(got, want)

        def test_grc_hint_names_the_file_the_reader_uses(self):
            # 3b101 QA r2 (codex): the refusal's touch path is the path the escape reader consumes.
            self.assertIn(_grc_escape_file(), MODE_SET_HINT)

        def test_grc_lease_mode_plain_and_bold(self):
            # 3b679: the lease moves from **Operating-mode:** to the plain line; both read.
            for line in ("Operating-mode: overnight-unattended", "**Operating-mode:** overnight-unattended"):
                value = _grc_mode_value("# Session state: grc\n\n" + line + "\n<!-- note -->\n")
                self.assertEqual(value, "overnight-unattended", line)
            for line in ("**Operating-mode**: overnight-unattended", " Operating-mode: overnight-unattended"):
                self.assertIsNone(_grc_mode_value("# Session state: grc\n\n" + line + "\n"), line)

        def test_grc_commented_mode_lines_are_not_read(self):
            # 3b679 r3: only a column-zero field line outside every HTML comment is read, and the value
            # never crosses a line end (an empty commented label used to read "-->").
            head = "# Session state: grc\n\n"
            for text in ("<!-- Operating-mode: overnight-unattended -->\n",
                         "<!--\nOperating-mode: overnight-unattended\n-->\n",
                         "note <!-- was\nOperating-mode: overnight-unattended\n-->\n",
                         "<!--\n**Operating-mode:** overnight-unattended\n-->\n",
                         "<!--\nOperating-mode:\n-->\n", "Operating-mode:\n-->\n"):
                self.assertIsNone(_grc_mode_value(head + text), text)
            for line in ("Operating-mode: fully-attended", "**Operating-mode:** fully-attended"):
                for above in ("<!--\nOperating-mode: overnight-unattended\n-->\n",
                              "note <!-- x\nOperating-mode: overnight-unattended\n-->\n",
                              "<!-- Operating-mode: overnight-unattended -->\n"):
                    value = _grc_mode_value(head + above + line + "\n<!-- note -->\n")
                    self.assertEqual(value, "fully-attended", (above, line))
            from unittest import mock
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                patches = {"_GRC_STATE_FILE": lease, "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    for text in ("<!--\nOperating-mode:\n-->\n",
                                 "note <!-- was\nOperating-mode: overnight-unattended\n-->\n"):
                        with open(lease, "w", encoding="utf-8") as fh:
                            fh.write(head + text)
                        self.assertIsNone(_grc_lease_mode(store), text)

        def test_grc_lease_mode_end_to_end_plain_and_bold(self):
            # 3b679 r2: both forms through _grc_lease_mode() itself, reading a real lease file.
            from unittest import mock
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                patches = {"_GRC_STATE_FILE": lease, "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    for mode in ("overnight-unattended", "fully-attended"):
                        for line in ("Operating-mode: " + mode, "**Operating-mode:** " + mode):
                            with open(lease, "w", encoding="utf-8") as fh:
                                fh.write("# Session state: grc\n\nStatus: active\n\n" + line
                                         + "\n<!-- note -->\n")
                            self.assertEqual(_grc_lease_mode(store), _grc_map_mode(mode), line)
                    self.assertNotEqual(_grc_map_mode("overnight-unattended"),
                                        _grc_map_mode("fully-attended"))
                    os.unlink(lease)
                    self.assertIsNone(_grc_lease_mode(store))

        def test_grc_lease_lone_cr_is_not_a_line_end(self):
            # 3b679 r4: the lease is split on LF only, so a lone CR never starts a field line (text-mode
            # universal newlines read the note's overnight-unattended); one trailing CR is dropped.
            from unittest import mock
            head = b"# Session state: grc\n\n"
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                patches = {"_GRC_STATE_FILE": lease, "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    for text, want in ((b"note\rOperating-mode: overnight-unattended\n"
                                        b"Operating-mode: fully-attended\n", "attended"),
                                       (b"note\rOperating-mode: overnight-unattended\n", None),
                                       (b"Operating-mode: overnight-unattended\r\n", "unattended"),
                                       (b"Operating-mode: fully-attended\r\n", "attended")):
                        with open(lease, "wb") as fh:
                            fh.write(head + text + b"<!-- note -->\n")
                        self.assertEqual(_grc_lease_mode(store), want, text)
            self.assertEqual(_grc_mode_value("Operating-mode: fully-attended\r\n"), "fully-attended")

        def test_grc_undecodable_lease_is_an_unreadable_lease(self):
            # 3b679 r5: a lease that is not valid UTF-8 fails open exactly as a missing or unreadable one
            # does (mode None, the stop allowed); it used to raise UnicodeDecodeError out of run().
            from unittest import mock
            lease_bytes = b"# Session state: grc\n\nOperating-mode: overnight-unattended\n"
            with tempfile.TemporaryDirectory() as store:
                build(store, producer_lines="1\tFirst")
                lease = os.path.join(store, "session-state.md")
                # 3b781: pin the fleet path to an ABSENT fixture so this test never reads the
                # live fleet file and the lease keeps deciding, as before the shared reader.
                patches = {"_GRC_STATE_FILE": lease, "_is_grc_main_checkout": lambda root: True,
                           "_FLEET_MODE_FILE": os.path.join(store, "no-fleet-file"),
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    def outcome():
                        return (_grc_lease_mode(store), read_operating_mode(store),
                                run(store, {"stop_hook_active": False}))
                    with open(lease, "wb") as fh:
                        fh.write(lease_bytes)
                    self.assertEqual(outcome(), ("unattended", "unattended", 2))
                    os.unlink(lease)
                    missing = outcome()
                    os.mkdir(lease)  # open() raises IsADirectoryError, an OSError: an unreadable lease
                    unreadable = outcome()
                    os.rmdir(lease)
                    with open(lease, "wb") as fh:
                        fh.write(lease_bytes + b"note: \xff\n")
                    self.assertEqual((missing, unreadable, outcome()), ((None, None, 0),) * 3)

        def test_grc_fleet_mode_file_is_read_first(self):
            # 3b781 (fails at 430da42ef): the fleet mode file is the authority in the grc
            # checkout; the lease arms or yields only through the shared reader's dated-swap
            # rules. Fixture paths only; the live fleet file is never read.
            from unittest import mock
            head = "# Session state: grc\n\n"
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                fleet = os.path.join(store, "operating-mode")
                patches = {"_GRC_STATE_FILE": lease, "_FLEET_MODE_FILE": fleet,
                           "_FLEET_OWNER_UID": os.geteuid(),
                           "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}

                def put(path, text):
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(text)

                with mock.patch.dict(globals(), patches):
                    put(lease, head + "Operating-mode: fully-attended\n")
                    put(fleet, '{"mode":"unattended","set_at":"2026-11-01T12:00:00Z"}')
                    # NEW: a fleet unattended reading arms over an attended lease.
                    self.assertEqual(read_operating_mode(store), "unattended")
                    put(fleet, '{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}')
                    put(lease, head + "Operating-mode: daytime-unattended\n")
                    # NEW: an UNDATED #5(b) swap is superseded by a readable fleet file.
                    self.assertEqual(read_operating_mode(store), "attended")
                    put(lease, head + "Operating-mode: "
                               "daytime-unattended@2026-11-01T12:00:01Z\n")
                    self.assertEqual(read_operating_mode(store), "unattended")  # newer swap arms
                    put(lease, head + "Operating-mode: "
                               "daytime-unattended@2026-11-01T11:00:00Z\n")
                    self.assertEqual(read_operating_mode(store), "attended")  # stale swap yields
                    # 3b781 r3 (claude N2): an ATTENDED lease here, so this assertion
                    # holds only through the fail-closed reading (the dated swap above
                    # would outrank a tolerated-missing-set_at epoch default anyway).
                    put(lease, head + "Operating-mode: fully-attended\n")
                    put(fleet, '{"mode":"attended"}')  # missing set_at: unusable, fail closed
                    self.assertEqual(read_operating_mode(store), "unattended")
                    put(lease, head + "Operating-mode: "
                               "daytime-unattended@2026-11-01T11:00:00Z\n")
                    os.unlink(fleet)  # absent fleet file: the lease decides as before
                    self.assertEqual(read_operating_mode(store), "unattended")
                    # 3b781 r2 (agy1 N5): the absent-fleet fallback asserted with an
                    # ATTENDED lease too, so it is distinct from the fail-closed default.
                    put(lease, head + "Operating-mode: fully-attended\n")
                    self.assertEqual(read_operating_mode(store), "attended")
                    # 3b781 r2 (codex E2): with the fleet file absent each consumer keeps
                    # its own pre-3b781 rule; this guard maps the WHOLE leading token
                    # (3b101), so commentary mentioning "unattended" must not arm it.
                    put(lease, head + "Operating-mode: attended; was overnight-unattended\n")
                    self.assertEqual(read_operating_mode(store), "attended")

        def test_grc_fleet_nonjson_constants_fail_closed(self):
            # 3b781 r4 (codex E1): NaN, Infinity and -Infinity are not JSON; each
            # constant alone in an otherwise valid ATTENDED fleet fixture must fail
            # closed to the armed state through the shared reader, never disarm the
            # guard. Fixture paths only; the live fleet file and live lease are
            # never read.
            from unittest import mock
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                with open(lease, "w", encoding="utf-8") as fh:
                    fh.write("# Session state: grc\n\nOperating-mode: fully-attended\n")
                fleet = os.path.join(store, "operating-mode")
                patches = {"_GRC_STATE_FILE": lease, "_FLEET_MODE_FILE": fleet,
                           "_FLEET_OWNER_UID": os.geteuid(),
                           "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    with open(fleet, "w", encoding="utf-8") as fh:
                        fh.write('{"mode":"attended","set_at":"2026-11-01T12:00:00Z"}')
                    # control: the fixture is otherwise valid attended
                    self.assertEqual(read_operating_mode(store), "attended")
                    for constant in ("NaN", "Infinity", "-Infinity"):
                        with open(fleet, "w", encoding="utf-8") as fh:
                            fh.write('{"mode":"attended",'
                                     '"set_at":"2026-11-01T12:00:00Z","phase":%s}' % constant)
                        self.assertEqual(read_operating_mode(store), "unattended", constant)

        def test_grc_reader_failure_fails_closed_to_armed(self):
            # 3b781 r2 (codex E1, agy1 E1, agy1 W3): a missing or refused shared reader,
            # or a reader exception, FAILS CLOSED to the armed state: an ATTENDED lease
            # must not disarm the guard while the (fixture) fleet file reads unattended.
            # Fails at c068eeed0, where the lease-only fallback returned "attended".
            # Fixture paths only; the live fleet file and live lease are never read.
            from unittest import mock
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                with open(lease, "w", encoding="utf-8") as fh:
                    fh.write("# Session state: grc\n\nOperating-mode: fully-attended\n")
                fleet = os.path.join(store, "operating-mode")
                with open(fleet, "w", encoding="utf-8") as fh:
                    fh.write('{"mode":"unattended","set_at":"2026-11-01T12:00:00Z"}')
                patches = {"_GRC_STATE_FILE": lease, "_FLEET_MODE_FILE": fleet,
                           "_FLEET_OWNER_UID": os.geteuid(),
                           "_grc_operating_mode_helper": lambda: None,
                           "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    self.assertEqual(read_operating_mode(store), "unattended")

                class _Raising:
                    @staticmethod
                    def effective_mode(*_args, **_kwargs):
                        raise RuntimeError("reader defect")

                patches["_grc_operating_mode_helper"] = lambda: _Raising
                with mock.patch.dict(globals(), patches):
                    self.assertEqual(read_operating_mode(store), "unattended")

        def test_grc_lease_read_is_bounded_and_rejects_non_regular(self):
            # 3b781 r2 (codex W3): a FIFO or oversized lease can neither hang the guard
            # nor keep it from consulting the fleet file; the bounded reader sees None.
            from unittest import mock
            with tempfile.TemporaryDirectory() as store:
                lease = os.path.join(store, "session-state.md")
                fleet = os.path.join(store, "operating-mode")
                with open(fleet, "w", encoding="utf-8") as fh:
                    fh.write('{"mode":"unattended","set_at":"2026-11-01T12:00:00Z"}')
                patches = {"_GRC_STATE_FILE": lease, "_FLEET_MODE_FILE": fleet,
                           "_FLEET_OWNER_UID": os.geteuid(),
                           "_is_grc_main_checkout": lambda root: True,
                           "_grc_is_worker": lambda: False}
                with mock.patch.dict(globals(), patches):
                    os.mkfifo(lease)  # no writer: the non-blocking open cannot hang, and
                    self.assertIsNone(_grc_read_lease_text())  # S_ISREG rejects it unread
                    self.assertEqual(read_operating_mode(store), "unattended")  # fleet consulted
                    os.unlink(lease)
                    with open(lease, "w", encoding="utf-8") as fh:  # a prefix is not the lease
                        fh.write(("# Session state: grc\n\n"
                                  "Operating-mode: overnight-unattended\n")
                                 .ljust(_GRC_LEASE_MAX_BYTES + 1, "x"))
                    self.assertIsNone(_grc_read_lease_text())
                    os.unlink(fleet)  # absent fleet + unreadable lease: indeterminate
                    self.assertIsNone(read_operating_mode(store))

        def test_grc_lease_arms_only_the_main_checkout_and_submodules(self):
            # 3b101 QA r2: the lease half of the scoping, on real hook copies: the main checkout and a
            # submodule read the lease; a linked worktree does not.
            import shutil, subprocess, tempfile
            with tempfile.TemporaryDirectory() as parent:
                os.makedirs(os.path.join(parent, "private"))
                with open(os.path.join(parent, "private", "session-state.md"), "w", encoding="utf-8") as fh:
                    fh.write("# Session state: grc\n\nOperating-mode: overnight-unattended\n")
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
                           "no-space": f"gitdir:{os.path.join(parent, '.git', 'modules', 'sub')}\n",
                           # 3b124: gitfiles git refuses that the old first-line strip accepted
                           "two-space": f"gitdir:  {os.path.join(parent, '.git', 'modules', 'sub')}\n",
                           "trailing-space": f"gitdir: {os.path.join(parent, '.git', 'modules', 'sub')}  \n",
                           "trailing-line": f"gitdir: {os.path.join(parent, '.git', 'modules', 'sub')}\nextra\n"}
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
                # 3b781 r2 (agy1 W4): the REAL hook copies must never read the live fleet
                # file. Each copy carries a fixture fleet path (an absent file under this
                # fixture tree, so the lease keeps deciding) and the shared reader beside
                # it, so the copies exercise the full fleet-first path hermetically.
                source = Path(__file__).read_text(encoding="utf-8")
                live_line = '_FLEET_MODE_FILE = "/opt/' + 'orch-operator/operating-mode"'
                self.assertEqual(source.count(live_line), 1)
                patched_source = source.replace(
                    live_line, "_FLEET_MODE_FILE = %r" % os.path.join(parent, "no-fleet-file"))
                reader = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "_operating_mode.py")
                # 3b781 r5 (claude W, N): the copied reader's own default must point at the
                # fixture too, as HookRoundEightTests rewrites it, and each copy is asserted
                # free of its live literal like the sibling copy tests above.
                reader_live_line = 'CANONICAL_MODE_FILE = "/opt/' + 'orch-operator/operating-mode"'
                fixture_reader_line = "CANONICAL_MODE_FILE = %r" % os.path.join(parent, "no-fleet-file")
                for name, gitfile in layouts.items():
                    r = os.path.join(parent, name)
                    os.makedirs(os.path.join(r, ".claude", "hooks"))
                    hook = os.path.join(r, ".claude", "hooks", os.path.basename(__file__))
                    Path(hook).write_text(patched_source, encoding="utf-8")
                    self.assertNotIn(live_line, Path(hook).read_text(encoding="utf-8"), name)
                    reader_copy = os.path.join(r, ".claude", "hooks", "_operating_mode.py")
                    shutil.copy(reader, reader_copy)
                    reader_text = Path(reader_copy).read_text(encoding="utf-8")
                    self.assertEqual(reader_text.count(reader_live_line), 1, name)
                    Path(reader_copy).write_text(
                        reader_text.replace(reader_live_line, fixture_reader_line), encoding="utf-8")
                    self.assertNotIn(reader_live_line, Path(reader_copy).read_text(encoding="utf-8"), name)
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
                        out = subprocess.run([sys.executable, "-I", "-B", "-c", code, hook], capture_output=True,
                                             text=True, env=env, timeout=60)
                    finally:
                        os.chmod(locked, 0o755)
                    got[name] = out.stdout.strip()
                want = {"grc_library": "unattended", "wt-x": "None", "wt-alias": "None", "sub": "unattended",
                        "sub-deep": "unattended", "missing": "None", "file-target": "None", "no-git": "None",
                        "not-admin": "None", "empty-target": "None", "no-prefix": "None", "nul-target": "None",
                        "sub-symhead": "unattended", "no-space": "None", "two-space": "None",
                        "trailing-space": "None", "trailing-line": "None"}
                if check_locked:
                    want["wt-locked"] = "None"
                self.assertEqual(got, want, got)
                # A worker in the main checkout is never armed by the lease (3b101 QA r3).
                hook = os.path.join(parent, "grc_library", ".claude", "hooks", os.path.basename(__file__))
                env["CLAUDE_CONFIG_DIR"] = os.path.join(parent, "orch-worker.example")
                out = subprocess.run([sys.executable, "-I", "-B", "-c", code, hook], capture_output=True, text=True,
                                     env=env, timeout=60)
                self.assertEqual(out.stdout.strip(), "None", out.stderr)
                # A stray file-based mode record never shadows the lease in the main checkout (3b113 QA r2).
                env.pop("CLAUDE_CONFIG_DIR")
                main = os.path.join(parent, "grc_library")
                os.makedirs(os.path.join(main, ".working"))
                with open(os.path.join(main, MODE_FILE), "w", encoding="utf-8") as fh:
                    fh.write("attended\n")
                out = subprocess.run([sys.executable, "-I", "-B", "-c", code, hook], capture_output=True, text=True,
                                     env=env, timeout=60)
                self.assertEqual(out.stdout.strip(), "unattended", out.stderr)

        def test_gitfile_parse_agrees_with_git(self):
            # 3b124: _is_primary_checkout reads a gitfile as git's read_gitfile does. Every variant names a
            # real git directory, and git's own verdict (git rev-parse --git-dir exits 128 on a refused
            # gitfile) is pinned beside the hook's, so a fixture that stops reproducing on the installed
            # git fails here as well.
            import shutil
            git = shutil.which("git")
            if git is None:
                self.skipTest("git is not installed")
            with tempfile.TemporaryDirectory() as parent:
                env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
                env.update(HOME=parent, GIT_CONFIG_NOSYSTEM="1", GIT_CEILING_DIRECTORIES=parent)
                subprocess.run([git, "init", "-q", os.path.join(parent, "real")], env=env,
                               capture_output=True, check=True, timeout=60)
                admin = os.path.join(parent, "real", ".git")
                cases = {"exact": (f"gitdir: {admin}\n", True), "relative": ("gitdir: ../real/.git\n", True),
                         "no-newline": (f"gitdir: {admin}", True), "crlf": (f"gitdir: {admin}\r\n", True),
                         "blank-tail": (f"gitdir: {admin}\n\n", True),
                         # the three 3b124 reproductions, then two prefix controls
                         "two-space": (f"gitdir:  {admin}\n", False),
                         "trailing-space": (f"gitdir: {admin}  \n", False),
                         "trailing-line": (f"gitdir: {admin}\nextra\n", False),
                         "no-space": (f"gitdir:{admin}\n", False), "leading-space": (f" gitdir: {admin}\n", False)}
                got = {}
                for name, (gitfile, _want) in cases.items():
                    root = os.path.join(parent, name)
                    os.makedirs(root)
                    with open(os.path.join(root, ".git"), "w", encoding="utf-8", newline="") as fh:
                        fh.write(gitfile)
                    out = subprocess.run([git, "rev-parse", "--git-dir"], cwd=root, env=env,
                                         capture_output=True, text=True, timeout=60)
                    got[name] = (out.returncode == 0, _is_primary_checkout(root))
                self.assertEqual(got, {name: (want, want) for name, (_gitfile, want) in cases.items()}, got)

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

        def test_undecodable_mode_file_is_an_unreadable_mode_file(self):
            # 3b679 r6: a MODE_FILE that is not valid UTF-8 takes the unreadable branch (mode None, the stop
            # allowed) as any OSError but FileNotFoundError does; it used to raise UnicodeDecodeError out of
            # run(). An absent MODE_FILE falls through to _grc_lease_mode, stubbed to arm so the two differ.
            from unittest import mock
            with tempfile.TemporaryDirectory() as d:
                build(d, mode="unattended", producer_lines="1\tFirst")
                mode_file = os.path.join(d, MODE_FILE)
                with mock.patch.dict(globals(), {"_grc_lease_mode": lambda root: "unattended"}):
                    def outcome():
                        return read_operating_mode(d), run(d, {"stop_hook_active": False})
                    self.assertEqual(outcome(), ("unattended", 2))
                    os.unlink(mode_file)
                    self.assertEqual(outcome(), ("unattended", 2))  # absent: the lease fallback
                    os.mkdir(mode_file)  # open() raises IsADirectoryError, an OSError: an unreadable MODE_FILE
                    unreadable = outcome()
                    os.rmdir(mode_file)
                    with open(mode_file, "wb") as fh:
                        fh.write(b"unattended\n\xff\n")
                    self.assertEqual((unreadable, outcome()), ((None, 0),) * 2)

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
        def setUp(self):
            self.slot_share_dir = tempfile.TemporaryDirectory()
            self.addCleanup(self.slot_share_dir.cleanup)
            patcher = mock.patch.dict(
                globals(), _SLOT_SHARES_FILE=os.path.join(self.slot_share_dir.name, "slot-shares.absent"),
                _SLOT_SHARE_EXPECT_UID=os.geteuid())
            patcher.start()
            self.addCleanup(patcher.stop)
            # As in T.setUp: no inherited GRC_DROP_ROOT reaches decide()'s declared-wait line.
            environ = mock.patch.dict(os.environ)
            environ.start()
            self.addCleanup(environ.stop)
            os.environ.pop("GRC_DROP_ROOT", None)

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
            block, _ = decide("unattended", False, [("1", "sample")], count, (None, "absent"))
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
                                    decide("unattended", False, [("1", "sample")], count, (None, "absent"))[0],
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
                        self.assertTrue(decide("unattended", False, [("1", "sample")], count, (None, "absent"))[0])
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
                    self.assertTrue(decide("unattended", False, [("1", "sample")], count, (None, "absent"))[0])

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


    class SlotShareTests(unittest.TestCase):
        setUp = T.setUp
        _hook_copy = T._hook_copy
        record = T.record
        workers = T.workers

        def fixture(self, data=None):
            return _write_share(_SLOT_SHARES_FILE, data if data is not None else
                                {"schema": 1, "default": 2, "shares": {"grc": 4}})

        def evaluate(self, live, items=10):
            diagnostic = mock.Mock()
            with mock.patch.dict(globals(), is_orchestrator_session=lambda root: True,
                                 read_operating_mode=lambda root: UNATT,
                                 actionable_items=lambda root: [("1", "work")] * items,
                                 live_dispatch_groups=lambda: live, _diagnostic=diagnostic):
                rc = run(root_real, {"stop_hook_active": False})
            return rc, "".join(call.args[0] for call in diagnostic.call_args_list)

        def test_slot_share_declarations(self):
            self.assertEqual(share_declarations, (production_share_path, "grc", 0, 64, 65536))
            self.assertEqual(Path(__file__).read_text().count(production_share_path), 1)

        def test_slot_share_json(self):
            cases = [
                ({"schema": 1, "default": 2, "shares": {"grc": 4}}, (4, "grc")),
                ({"schema": 1, "default": 2, "shares": {"other": 4}}, (2, "default")),
                ({"schema": 1, "default": 2}, (2, "default")),
                ({"schema": 1, "shares": {"grc": 4}}, (4, "grc")),
                ({"schema": 1, "default": "bad", "shares": {"grc": 4}}, (4, "grc")),
                ({"schema": 1, "extra": True, "shares": {"grc": 4}}, (4, "grc")),
                ({"schema": 1, "default": 8, "shares": {"grc": {}}}, (None, "invalid")),
                ({"schema": 1}, (None, "invalid")),
                ([], (None, "invalid")),
                (None, (None, "invalid")),
                ("object", (None, "invalid")),
            ]
            for value in (True, 2.0, 4.0, "4", "2", None, 0, -1, 65):
                cases.append(({"schema": 1, "default": 2, "shares": {"grc": value}}, (None, "invalid")))
                cases.append(({"schema": 1, "default": value}, (None, "invalid")))
            for value in (1.0, True, 2, "1", None):
                cases.append(({"schema": value, "default": 4}, (None, "invalid")))
            cases.append(({"default": 4}, (None, "invalid")))
            for value in (None, [], [1], 2, "x"):
                cases.append(({"schema": 1, "default": 4, "shares": value}, (None, "invalid")))
            for data, expected in cases:
                with self.subTest(data=data):
                    self.fixture(_json.dumps(data).encode())
                    self.assertEqual(read_slot_share(), expected)

        def test_slot_share_bounds(self):
            for value in (1, 2, 64):
                with self.subTest(value=value):
                    self.fixture({"schema": 1, "shares": {"grc": value}})
                    self.assertEqual(read_slot_share(), (value, "grc"))

        def test_slot_share_encoding(self):
            raw = b'{"schema":1,"shares":{"grc":4}}'
            for data, expected in ((b"\xef\xbb\xbf" + raw, (4, "grc")),
                                   (b"\xef\xbb\xbf" * 2 + raw, (None, "invalid")),
                                   (b'{"schema":1,"default":4,"x":"\xff"}', (None, "invalid")),
                                   (b"\xff", (None, "invalid")), (b"{", (None, "invalid"))):
                with self.subTest(data=data):
                    self.fixture(data)
                    self.assertEqual(read_slot_share(), expected)

        def test_slot_share_non_utf8_documents(self):
            text = '{"schema":1,"shares":{"grc":4}}'
            # Exercise both endian forms, with and without their byte-order marks.
            for encoding, bom in (("utf-16-le", b"\xff\xfe"),
                                  ("utf-16-be", b"\xfe\xff"),
                                  ("utf-32-le", b"\xff\xfe\x00\x00"),
                                  ("utf-32-be", b"\x00\x00\xfe\xff")):
                for prefix in (b"", bom):
                    with self.subTest(encoding=encoding, bom=bool(prefix)):
                        self.fixture(prefix + text.encode(encoding))
                        self.assertEqual(read_slot_share(), (None, "invalid"),
                                         "share documents must be UTF-8")
            self.fixture(text.encode() + b"\x00")
            self.assertEqual(read_slot_share(), (None, "invalid"),
                             "a trailing NUL must invalidate the share document")

        def test_slot_share_duplicates(self):
            for data in (b'{"schema":1,"schema":1,"default":4}',
                         b'{"schema":1,"default":4,"default":8}',
                         b'{"schema":1,"shares":{"grc":4,"grc":4}}',
                         b'{"schema":1,"default":8,"other":1,"other":2}',
                         b'{"schema":1,"default":8,"shares":{"other":1,"other":2}}'):
                with self.subTest(data=data):
                    self.fixture(data)
                    self.assertEqual(read_slot_share(), (None, "invalid"))

        def test_slot_share_owner(self):
            self.fixture()
            self.assertEqual(read_slot_share(expect_uid=os.geteuid() + 1), (None, "unowned"))
            self.assertEqual(read_slot_share(), (4, "grc"))

        def test_slot_share_modes(self):
            path = self.fixture()
            try:
                for mode in (0o600, 0o640, 0o644, 0o444, 0o000):
                    for writable in (0, 0o020, 0o002, 0o022):
                        with self.subTest(mode=oct(mode | writable)):
                            os.chmod(path, mode | writable)
                            if not os.access(path, os.R_OK):
                                self.skipTest("invoking user cannot read mode %04o" %
                                              (mode | writable))
                            expected = (None, "badmode") if writable else (4, "grc")
                            self.assertEqual(read_slot_share(), expected,
                                             "readable non-writable shares must be accepted")
            finally:
                os.chmod(path, 0o644)

        def test_slot_share_objects(self):
            self.assertEqual(read_slot_share(), (None, "absent"))
            path = self.fixture()
            self.assertEqual(read_slot_share(path=path + "/child"), (None, "absent"))
            self.assertEqual(read_slot_share(path=self.registry.name), (None, "notreg"))
            link = os.path.join(self.registry.name, "link")
            os.symlink(path, link)
            self.assertEqual(read_slot_share(path=link), (None, "notreg"))
            os.unlink(path)
            self.assertEqual(read_slot_share(path=link), (None, "notreg"))

        @unittest.skipIf(os.geteuid() == 0, "root bypasses file read permissions")
        def test_slot_share_permissions(self):
            path = self.fixture()
            os.chmod(path, 0)
            self.assertEqual(read_slot_share(), (None, "unread"))

        def test_slot_share_open_error(self):
            with mock.patch.object(os, "open", side_effect=OSError(errno.EACCES, "denied")):
                self.assertEqual(read_slot_share(), (None, "unread"))

        def test_slot_share_post_open_errors(self):
            self.fixture()
            for operation in ("fstat", "read"):
                with self.subTest(operation=operation), \
                        mock.patch.object(os, operation, side_effect=OSError("unread")), \
                        mock.patch.object(os, "close", wraps=os.close) as close:
                    self.assertEqual(read_slot_share(), (None, "unread"))
                    close.assert_called_once()

        def test_slot_share_partial_read_error(self):
            self.fixture()
            with mock.patch.object(os, "read", side_effect=[
                    b'{"schema":1,"default":8}', OSError("after bytes")]) as read:
                self.assertEqual(read_slot_share(), (None, "unread"))
                self.assertEqual(read.call_count, 2)

        def test_slot_share_parser_errors(self):
            self.fixture()
            for failure in (RecursionError, MemoryError):
                with self.subTest(failure=failure), \
                        mock.patch.object(json, "loads", side_effect=failure("parser")):
                    try:
                        result = read_slot_share()
                    except Exception as exc:
                        self.fail("share parser failure escaped: %s" % type(exc).__name__)
                    self.assertEqual(result, (None, "invalid"))

        def test_slot_share_close_error(self):
            self.fixture()
            real_close = os.close
            def close(fd):
                real_close(fd)
                raise OSError("close")
            with mock.patch.object(os, "close", side_effect=close):
                try:
                    result = read_slot_share()
                except OSError as exc:
                    self.fail("share close failure escaped: %s" % exc)
                self.assertEqual(result, (4, "grc"))

        def test_slot_share_short_reads(self):
            self.fixture()
            real_read = os.read
            with mock.patch.object(os, "read", side_effect=lambda fd, size: real_read(fd, min(size, 7))):
                self.assertEqual(read_slot_share(), (4, "grc"))

        def test_slot_share_size(self):
            raw = b'{"schema":1,"default":4}'
            for size, expected in ((65536, (4, "default")), (65537, (None, "toobig"))):
                with self.subTest(size=size):
                    self.fixture(raw + b" " * (size - len(raw)))
                    self.assertEqual(read_slot_share(), expected)

        def test_slot_share_fifo(self):
            with tempfile.TemporaryDirectory() as d:
                hook = self._hook_copy(d)
                fifo = os.path.join(d, "fifo")
                os.mkfifo(fifo)
                code = ("import runpy,sys; m=runpy.run_path(sys.argv[1]); "
                        "print(m['read_slot_share']()); "
                        "print(m['read_slot_share'](path=sys.argv[2])[1])")
                try:
                    out = subprocess.run([sys.executable, "-I", "-c", code, hook, fifo],
                                         capture_output=True, text=True, timeout=10)
                except subprocess.TimeoutExpired:
                    self.fail("slot-share FIFO read exceeded its deadline")
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertEqual(out.stdout.splitlines(), ["(2, 'grc')", "notreg"])

        def test_slot_share_call_time(self):
            path = os.path.join(self.registry.name, "other")
            _write_share(path, {"schema": 1, "default": 2, "shares": {"grc": 4, "other": 8}})
            with mock.patch.dict(globals(), _SLOT_SHARES_FILE=path, _SLOT_SHARE_PROJECT="other",
                                 _SLOT_SHARE_EXPECT_UID=os.geteuid()):
                self.assertEqual(read_slot_share(), (8, "other"))
                rc, reason = self.evaluate(8)
                self.assertEqual(rc, 0)
                self.assertIn("minimum 8, share other", reason)
            self.assertEqual(read_slot_share(path=path, project="other"), (8, "other"))
            with mock.patch.dict(globals(), _SLOT_SHARES_FILE=path, _SLOT_SHARE_EXPECT_UID=os.geteuid() + 1):
                self.assertEqual(read_slot_share(), (None, "unowned"))

        def test_slot_share_decisions(self):
            cases = [
                ({"schema": 1, "shares": {"grc": 4}}, 3, 10, 2, "at least 4"),
                ({"schema": 1, "shares": {"grc": 4}}, 4, 10, 0, "minimum 4, share grc"),
                ({"schema": 1, "shares": {"grc": 2}}, 3, 10, 0, "minimum 3, share grc 2 below floor"),
                ({"schema": 1, "default": 8}, 7, 10, 2, "at least 8"),
                ({"schema": 1, "default": 8}, 8, 10, 0, "minimum 8, share default"),
                ({"schema": 1, "shares": {"grc": 8}}, 3, 1, 2, "at least 8"),
                ({"schema": 1, "shares": {"grc": 8}}, 64, 10, 0, "minimum 8, share grc"),
                ({"schema": 1, "shares": {"grc": "4"}}, 3, 10, 0, "share invalid"),
                ({"schema": 1, "shares": {"grc": 65}}, 3, 10, 0, "share invalid"),
            ]
            for data, live, count, expected, fragment in cases:
                with self.subTest(data=data, live=live, count=count):
                    self.fixture(data)
                    rc, reason = self.evaluate(live, count)
                    self.assertEqual(rc, expected)
                    self.assertIn(fragment, reason)
            os.unlink(_SLOT_SHARES_FILE)
            for live, expected, fragment in ((2, 2, "at least 3"), (3, 0, "minimum 3, share absent")):
                with self.subTest(live=live):
                    rc, reason = self.evaluate(live)
                    self.assertEqual(rc, expected)
                    self.assertIn(fragment, reason)

        def test_slot_share_exact_floor_note(self):
            self.fixture({"schema": 1, "shares": {"grc": 3}})
            rc, reason = self.evaluate(3)
            self.assertEqual(rc, 0)
            self.assertIn("minimum 3, share grc", reason)
            self.assertNotIn("below floor", reason)

        def test_slot_share_floor(self):
            self.fixture({"schema": 1, "shares": {"grc": 2}})
            rc, reason = self.evaluate(2)
            self.assertEqual(rc, 2, "share 2 at live 2 must retain the floor")
            self.assertIn("at least 3", reason)

        def test_slot_share_floor_decide_boundaries(self):
            for value in (1, 2):
                for live in (0, 1, 2, 3):
                    with self.subTest(share=value, live=live):
                        block, reason = decide(UNATT, False, [("1", "work")],
                                               live, (value, "grc"))
                        self.assertEqual(block, live < 3,
                                         "direct decision must retain the floor of three")
                        if live < 3:
                            self.assertIn("at least 3 live owned dispatch groups", reason)
                        else:
                            self.assertIn("minimum 3, share grc %d below floor" % value, reason)

        def test_slot_share_floor_reader_boundaries(self):
            for value in (1, 2):
                self.fixture({"schema": 1, "shares": {"grc": value}})
                for live in (0, 1, 2, 3):
                    with self.subTest(share=value, live=live):
                        rc, reason = self.evaluate(live)
                        self.assertEqual(rc, 2 if live < 3 else 0,
                                         "reader-to-decision path must retain the floor of three")
                        if live < 3:
                            self.assertIn("at least 3 live owned dispatch groups", reason)
                        else:
                            self.assertIn("minimum 3, share grc %d below floor" % value, reason)

        def test_slot_share_upper_decide_boundaries(self):
            for value in (8, 64):
                for live in (value - 1, value):
                    with self.subTest(share=value, live=live):
                        block, reason = decide(UNATT, False, [("1", "work")],
                                               live, (value, "grc"))
                        self.assertEqual(block, live < value,
                                         "direct decision must reach the entire share")
                        if live < value:
                            self.assertIn("at least %d live owned dispatch groups" % value, reason)
                        else:
                            self.assertIn("minimum %d, share grc" % value, reason)

        def test_slot_share_upper_reader_boundaries(self):
            for value in (8, 64):
                self.fixture({"schema": 1, "shares": {"grc": value}})
                for live in (value - 1, value):
                    with self.subTest(share=value, live=live):
                        rc, reason = self.evaluate(live)
                        self.assertEqual(rc, 2 if live < value else 0,
                                         "reader-to-decision path must reach the entire share")
                        if live < value:
                            self.assertIn("at least %d live owned dispatch groups" % value, reason)
                        else:
                            self.assertIn("minimum %d, share grc" % value, reason)

        def test_slot_share_max_mutation(self):
            source = textwrap.dedent(inspect.getsource(decide))
            seam = "max(value, _MIN_LIVE_GROUPS)"
            self.assertEqual(source.count(seam), 1)
            namespace = dict(globals())
            exec(compile(source.replace(seam, "value"), "<share mutation>", "exec"), namespace)
            with mock.patch.dict(globals(), decide=namespace["decide"]):
                result = unittest.TestResult()
                SlotShareTests("test_slot_share_floor").run(result)
            self.assertFalse(result.errors, result.errors)
            self.assertEqual(len(result.failures), 1, result.failures)
            self.assertIn("share 2 at live 2 must retain the floor", result.failures[0][1])

        def test_slot_share_skip_reads(self):
            for mode, active, owner, items, live in (
                    (ATT, False, True, [("1", "work")], 0),
                    (UNATT, True, True, [("1", "work")], 0),
                    (UNATT, False, False, [("1", "work")], 0),
                    (UNATT, False, True, [], 0),
                    (UNATT, False, True, None, 0),
                    (UNATT, False, True, [("1", "work")], None)):
                reader = mock.Mock(side_effect=AssertionError("unexpected share read"))
                with self.subTest(mode=mode, active=active, owner=owner, items=items, live=live), \
                        mock.patch.dict(globals(), is_orchestrator_session=lambda root: owner,
                                        read_operating_mode=lambda root: mode,
                                        actionable_items=lambda root: items,
                                        live_dispatch_groups=lambda: live,
                                        read_slot_share=reader, _diagnostic=mock.Mock()):
                    self.assertEqual(run(root_real, {"stop_hook_active": active}), 0)
                    reader.assert_not_called()
            self.assertFalse(decide(UNATT, False, [("1", "work")], None, object())[0])
            reader = mock.Mock(return_value=(4, "grc"))
            with mock.patch.dict(globals(), read_slot_share=reader):
                rc, reason = self.evaluate(0)
            self.assertEqual(rc, 2)
            self.assertIn("at least 4", reason)
            reader.assert_called_once_with()

        def test_slot_share_reader_exception(self):
            with mock.patch.dict(globals(), read_slot_share=mock.Mock(side_effect=RuntimeError("reader"))):
                try:
                    blocked = self.evaluate(2)[0]
                    rc, reason = self.evaluate(3)
                except Exception as exc:
                    self.fail("share reader failure escaped: %s" % exc)
                self.assertEqual(blocked, 2)
                self.assertEqual(rc, 0)
                self.assertIn("minimum 3, share unread", reason)

        def test_slot_share_live_file(self):
            path = self.fixture()
            real_open = os.open
            opens = []
            def opened(candidate, *args, **kwargs):
                if candidate == path:
                    opens.append((args, kwargs))
                return real_open(candidate, *args, **kwargs)
            diagnostic = mock.Mock()
            with self.workers(), mock.patch.object(os, "open", side_effect=opened), \
                    mock.patch.dict(globals(), is_orchestrator_session=lambda root: True,
                                    read_operating_mode=lambda root: UNATT,
                                    actionable_items=lambda root: [("1", "work")] * 10,
                                    _diagnostic=diagnostic):
                self.assertEqual(run(root_real, {"stop_hook_active": False}), 2)
                self.assertIn("at least 4", diagnostic.call_args.args[0])
                self.fixture({"schema": 1, "shares": {"grc": 3}})
                self.assertEqual(run(root_real, {"stop_hook_active": False}), 0)
                self.assertIn("share grc", diagnostic.call_args.args[0])
            self.assertEqual(len(opens), 2)
            self.assertTrue(all(args[0] & os.O_CLOEXEC for args, _kwargs in opens))

        def test_slot_share_messages(self):
            with mock.patch.dict(globals(), _grc_escape_file=lambda: "/drop/.allow-idle-stop"):
                for share, required in (((_SLOT_SHARE_MAX, "default"), 64), ((2, "grc"), 3)):
                    block, reason = decide(UNATT, False, [("1", "work")] * 10, 0, share)
                    self.assertTrue(block)
                    lines = reason.splitlines()
                    self.assertEqual(len(lines), 5)
                    self.assertTrue(all(len(line) <= 160 for line in lines))
                    self.assertLessEqual(len(lines[3]), 145)
                    self.assertEqual(lines[3], "Yield allowed with at least %d live owned dispatch groups, "
                                     "or no actionable items (a [BLOCKED:<reason>] tag with a granted approvals row)." % required)
                    self.assertTrue(reason.endswith("set mode attended."))
                    for marker in ("BLOCKED (", "WHY:", "CONSIDER INSTEAD:"):
                        self.assertEqual(reason.count(marker), 1)
                    self.assertNotRegex(reason, "[\u2013\u2014]")
            shares = [(None, cause) for cause in ("absent", "notreg", "unowned", "badmode",
                                                  "toobig", "invalid", "unread")]
            shares += [(value, token) for value in (1, 2, 3, _SLOT_SHARE_MAX)
                       for token in ("default", _SLOT_SHARE_PROJECT, "other")]
            for value, token in shares:
                block, reason = decide(UNATT, False, [("1", "work")], 4096, (value, token))
                self.assertFalse(block)
                self.assertEqual(len(reason.splitlines()), 1)
                self.assertLess(len(reason), 160)
                self.assertIn("share " + token, reason)
                if value == 1:
                    self.assertIn("1 below floor", reason)

        def test_slot_share_audit_verdict(self):
            for successful in (False, True):
                with self.subTest(successful=successful):
                    result = mock.Mock()
                    result.wasSuccessful.return_value = successful
                    self.assertEqual(self_test_status(result, [production_share_path]), 1)
                    self.assertEqual(self_test_status(result, []), 0 if successful else 1)

        def test_slot_share_audit_control(self):
            before = list(share_opens)
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
            alias = os.path.dirname(production_share_path) + "/./" + os.path.basename(production_share_path)
            parent_alias = os.path.dirname(production_share_path) + "/child/../slot-shares.json"
            slash_alias = production_share_path.replace("/slot-shares.json", "//slot-shares.json")
            class BrokenPath:
                def __init__(self, failure):
                    self.failure = failure

                def __fspath__(self):
                    raise self.failure("not a usable path")
            try:
                for path in (production_share_path, alias, parent_alias, slash_alias,
                             os.fsencode(alias), Path(alias)):
                    for mode, event_flags in (("r", os.O_RDONLY), (None, flags), ("anything", object())):
                        with self.subTest(path=path, mode=mode):
                            share_opens[:] = before
                            sys.audit("open", path, mode, event_flags)
                            self.assertEqual(share_opens, before + [production_share_path])
                share_opens[:] = before
                sys.audit("slot-share.non-open", production_share_path, None, flags)
                self.assertEqual(share_opens, before, "non-open events must not be recorded")
                # Native opens resolve PathLike objects first, but explicit sys.audit calls
                # can carry one whose __fspath__ raises any exception.
                for path in (None, 7, object(), BrokenPath(TypeError), BrokenPath(ValueError),
                             production_share_path + ".other"):
                    try:
                        sys.audit("open", path, None, flags)
                    except Exception as exc:
                        self.fail("audit recorder must contain malformed paths: %s" %
                                  type(exc).__name__)
                self.assertEqual(share_opens, before)
            finally:
                share_opens[:] = before

        def test_slot_share_audit_callsite(self):
            # Exercise the actual return and post-suite probe, without recursively running this test.
            suite = ("unittest.TestLoader().loadTestsFromTestCase(case)\n"
                     "            for case in (T, GRCAdapterTests, ObservationTests, SlotShareTests)")
            control = ('SlotShareTests("test_slot_share_audit_control")\n'
                       "            for case in (SlotShareTests,)")
            for optimize in (False, True):
                for scenario, expected in (("control", 0), ("recorded", 1), ("active", 1)):
                    with self.subTest(optimize=optimize, scenario=scenario), tempfile.TemporaryDirectory() as d:
                        hook = self._hook_copy(d)
                        source = Path(hook).read_text()
                        self.assertEqual(source.count(suite), 1)
                        source = source.replace(suite, control)
                        if scenario == "recorded":
                            anchor = "            finally:\n                share_opens[:] = before\n"
                            replacement = anchor + '                sys.audit("open", production_share_path, "r", os.O_RDONLY)\n'
                        elif scenario == "active":
                            anchor = "        recording = False\n"
                            replacement = "        recording = True\n"
                        else:
                            anchor = replacement = None
                        if anchor is not None:
                            self.assertEqual(source.count(anchor), 1)
                            source = source.replace(anchor, replacement)
                        Path(hook).write_text(source)
                        if optimize:
                            out = subprocess.run([sys.executable, "-I", "-O", hook, "--self-test"],
                                                 capture_output=True, text=True, timeout=30)
                        else:
                            out = subprocess.run([sys.executable, "-I", hook, "--self-test"],
                                                 capture_output=True, text=True, timeout=30)
                        self.assertIn("Ran 1 test", out.stderr)
                        self.assertIn("\nOK\n", out.stderr)
                        self.assertEqual(out.returncode, expected, out.stdout + out.stderr)
                        if scenario == "recorded":
                            self.assertIn("self-test opened production slot-share path", out.stderr)
                        elif scenario == "active":
                            self.assertIn("slot-share audit recorder still active after suite", out.stderr)

    try:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(
            unittest.TestLoader().loadTestsFromTestCase(case)
            for case in (T, GRCAdapterTests, ObservationTests, SlotShareTests)))
    finally:
        recording = False
        for k, v in _saved_env.items():
            if v is not None:
                os.environ[k] = v
    before = list(share_opens)
    sys.audit("open", production_share_path, None, os.O_RDONLY)
    if share_opens != before:
        print("slot-share audit recorder still active after suite", file=sys.stderr)
        return 1
    if share_opens:
        print("self-test opened production slot-share path: %r" % share_opens, file=sys.stderr)
    return self_test_status(result, share_opens)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
