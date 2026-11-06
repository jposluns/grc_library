#!/usr/bin/env bash
#
# pre-push-guard.sh
#
# The single pre-push QA gate, run by the installed git pre-push hook:
#
#   tools/install-git-hooks.sh       # once per clone, shared by worktrees
#   tools/install-git-hooks.sh --check
#   git push -u origin <branch>
#
# A direct run remains available; every guarded push runs the guard again.
# Hook output streams through a regular file; direct pipes retain RM-10 refusal.
# Git --no-verify and core.hooksPath can bypass hooks; see tools/README.md.
#
# A push whose every changed path is site-only, and that clears every check
# below that would send it to the full guard, takes the FAST PATH described
# below; any other push runs the full guard. Both paths run every runner gate
# except the linter regression test suite (gate 36) gate by gate. The FULL
# guard then runs gate 36 WHOLE, with the private store present, as six
# parallel local shards (maintainer decision 2026-11-05 09:08 EST, replacing
# the reviewed store-dependent list); the fast path leaves gate 36 to CI. The
# quality workflow still runs the whole suite on every pull request, split
# across parallel shard jobs that together run exactly the serial run's tests
# plus a partition-verifying step, and tools/merge-when-green.py merges only
# when its required check (the summary job "Lint markdown corpus", which needs
# every shard) succeeded. The full guard runs, stopping on the first failure:
#
#   1. Every tools/run_all_audits.sh gate except gate 36, in runner order, by
#      the runner's own name and command, read from its run_gate lines at run
#      time (the same reading the fast path uses; see its grammar below).
#      On this full path each gate runs with the runner's advisory echo, as
#      run_gate does: a per-gate GRC_RUNNER_ECHO_TOKEN, a passing gate's
#      DUE-SOON lines always shown, and its WARN and NOTE lines shown when
#      the gate opted in by printing the runner-echo marker with that token
#      (gates 6, 72 and 106). When the gate-list reading fails, the guard
#      FAILS CLOSED to running tools/run_all_audits.sh whole, gate 36
#      included, so doubt never drops a check.
#   1b. Gate 36 whole, as REGRESSION_SHARD_COUNT (6, the quality workflow's
#      shard count) parallel local shards: tools/run-linter-regression.py
#      --shard i/6, each in its OWN temporary detached checkout of the exact
#      commit being pushed (git worktree add --detach into a mktemp
#      directory), so no shard's fixtures under tests/tmp are seen by
#      another shard's whole-repository scan (round-4 finding: one shared
#      working tree failed VanishingScratchTests). Beside each checkout sit
#      symbolic links to whichever of this clone's own siblings exist (the
#      private store <repo-parent>/private, grc_library_private,
#      grc_library_ref and grc_library_scratch), and a relative GRC_STORE is
#      made absolute, so the store is reachable as it is for the serial run.
#      Each shard runs in its own process group with stdin from /dev/null;
#      its output goes to its own log file, its step outputs to its own
#      GITHUB_OUTPUT file, and its exit status is read directly from wait.
#      When every shard exits 0, each shard's GITHUB_OUTPUT file must be
#      present and non-empty, or the step fails (exit 2) without running
#      the reconcile. tools/reconcile-regression-shards.py --shard-outputs
#      then reconciles the six (every shard succeeded, all six discovered
#      one unit set, every module earned a credited start); after a shard
#      failure it still runs, for its report only. A shard failure, a
#      shard without step outputs, or a reconcile failure fails the push,
#      keeping every checkout and log and printing their paths. INT, TERM
#      or HUP during this step stops every shard's process group (TERM,
#      then KILL after 10 seconds), waits for the shards, keeps and names
#      every checkout and log, and exits 130, 143 or 129. A kept shard
#      directory (a failure or an interrupt) is reported as left behind,
#      with what it holds and any process still using it, and no removal
#      command, since this run has not ended yet; the next push's leftover
#      report (below) checks it again. The shard directory holds a
#      guard-owner record (this guard's pid, clone, start time, pid
#      namespace, boot id and machine id), and the same run record sits
#      beside the git record of each checkout, so a later push can tell a
#      live run's checkouts from leftovers. A passing run
#      removes each checkout with git worktree remove --force, then the
#      shard directory (only a real directory named grc-gate36-shards.*;
#      the sibling links are removed as links, never followed). A failed
#      removal is reported with its path, git worktree prune then runs
#      after the directory is gone, and the guard says whether that
#      checkout's registration remains; it never claims a removal that
#      failed. On the fail-closed whole-runner fallback below gate 36 has
#      just run serially, so this step does not run again.
#   2. tools/run-pr-time-checks.sh  - the per-PR D-numbered delta gates (D6 retired) plus
#                                     the history-aware trio (gates 45/40/31) against
#                                     the merge base.
#   3. .web/build.py --check         - web-generator health (parse + render, no write).
#
# It then prints one ADVISORY that never blocks: build-reference-manifest.py --check
# (reference-manifest drift against the grc_library_ref sibling; P-TODO 3b62).
#
# Leftover report (strictly read-only; on both paths, before the gates): an
# interrupt, a KILL or a crash can leave shard checkouts, their shard
# directory and a process behind. Each push first reports what earlier runs
# of this guard in this clone left: the git worktrees registered with this
# clone whose path is <dir>/grc-gate36-shards.*/shard-<n>/<clone name>, and
# the directories named grc-gate36-shards.* under ${TMPDIR:-/tmp} that are
# owned by this user and are, or may be, this clone's (their guard-owner
# record names this clone, a checkout in them points into this clone's git
# directory, or something in them cannot be read), with every process whose
# working directory, root directory, open files or mapped files are inside
# one (read from /proc: every thread of a process is read for its own
# working directory, root directory and open files, since a thread can have
# its own, and a process whose thread-group leader has exited while other
# threads run is read thread by thread; the mappings of every thread are
# read when the leader is exiting or shows no mapping while other threads
# run). The report runs no git and starts
# and signals no process: it reads this clone's worktree registrations
# directly from <git common dir>/worktrees/*/ (gitdir, locked, HEAD and
# the run record), the common directory passed by the shell (git
# rev-parse --git-common-dir, which runs before the report and outside its
# bound). The final component of each path it reads in a leftover or a
# git record is never followed, and its type is read before it is opened,
# so a FIFO or other entry that is not a regular file is not opened unless
# it is swapped in (by one who can write its directory) between that check
# and the open, which are two lookups by name; the type of the open
# descriptor is then checked again, so it is closed unread; directories
# above it are resolved as usual. A git record that is a
# symbolic link is reported as unreadable. It stops, signals and deletes
# nothing of a leftover and
# changes no git state. A clean start prints nothing. Otherwise one block
# on stderr names each leftover by its path (a path holding anything but
# A-Z, a-z, 0-9 and _ . / + @ % = : , - is printed as a bash $'...' string
# whose every other byte, ! included, is escaped, so it is ASCII and safe
# to paste) and
# marks it REMOVABLE or INSPECT. Its advice is never stronger than what it
# proved. A leftover whose directory exists is REMOVABLE, with the commands
# that remove it (git worktree remove --force -- <checkout> for each
# registered checkout, whose HEAD is shown with the warning that --force
# discards its uncommitted changes and untracked files and that a commit
# no branch or tag holds is lost, then rm -rf -- <directory>), only when the scan
# finished and proved all of this: the directory is a real directory owned
# by this user; its guard-owner record is readable and names this clone;
# the run it names has ended (below); every checkout in it is registered
# with this clone, unlocked, and its .git points into this clone's git
# directory (a relative gitdir is read against the checkout); it holds
# nothing else but the guard's own logs, records and sibling links; this
# push does not run inside it; and every process /proc shows (kernel
# threads aside) was read (the working directory, root directory and open
# files of each of its threads, and its mapped files), with none using it.
# A thread still running that cannot be read makes its process
# unreadable; one that has exited, or whose entries are gone while the
# kernel marks it exiting (PF_EXITING), holds nothing. A process
# that cannot be read, whoever owns it and whatever the directory's mode,
# leaves use
# unknown, so for a non-root user on almost any host (any running a root
# daemon) an existing leftover is INSPECT. A registered checkout whose
# shard directory is gone leaves only its git record: it is REMOVABLE,
# with its HEAD shown and then git worktree remove -- <checkout>, which
# removes only that record, when the run record beside that git record
# names this clone and a run that has ended, the scan finished, the
# checkout is unlocked and no process is seen using the old path. A run
# has ended when, under the boot id it recorded, no process has its pid in
# its pid namespace or that pid started at another time; or when its boot
# id differs while its machine id (/etc/machine-id) is this machine's (an
# earlier boot). A differing boot id with another or unknown machine id,
# or an unknown boot id, proves nothing (another kernel may still run it).
# A copied machine id, or a VM restored from a memory snapshot (which
# keeps both the boot id and the machine id), defeats this check.
# Anything else is INSPECT, with the facts that are known, why it is not
# proven, and no removal command: unreadable or malformed metadata, git
# records included (reported as UNREADABLE, never dropped), an incomplete
# scan, mixed ownership, a live run or one whose state is unknown (another
# pid namespace or kernel, no /proc, no start time recorded), a process
# using it (this guard, the processes that started this push, a pre-push
# guard the report identified and a process with one among its parents are
# labelled), a
# registered checkout git would list as prunable while its directory
# exists, or a HEAD it cannot read (in a clone that keeps its refs in
# reftable, every git record holds the placeholder HEAD refs/heads/.invalid,
# reported as "reftable HEAD not read", so every leftover of such a clone
# stays INSPECT). A pre-push guard is known by identity, never by its
# command line: a process is one when its pid and start time are those of
# this guard or of a live run (a run record the scan read, of any clone,
# whose run is running: same boot id and pid namespace, matching start
# time), and was started by one when a parent is, the start time of each
# parent read, in a walk kept consistent (the process read again with
# another start time, a parent that started later than its child, or a
# child whose parent pid or start time changed once its parent was read,
# ends it as uncertain); a process whose start time or parents cannot be
# read consistently is said to be uncertain, not labelled. A run writes a
# run record only from its gate 36 step on (step 1b, once its shard
# directory exists), and a passing run removes it with that directory
# before steps 2 and 3; a fast-path run, a whole-runner fallback and a full
# run before step 1b write none, so only the guards the report identified
# are labelled. A git record an older guard left with no run record also gets a
# manual inspection procedure, marked as not proved. A leftover a process
# uses also gets a manual stop procedure, marked as not proved and never a
# stop command: recheck the pid's start time and command line just before
# any signal, never for this guard, the processes that started this push,
# a pre-push guard, a process one started or a live guard run, then push
# again and remove the leftover only if that report marks it REMOVABLE.
# The scan has 4 seconds. An alarm ends the whole report at 5 seconds
# (counted from when its code starts). When the scan bound is reached it
# says the report is INCOMPLETE, and nothing it lists has a removal
# command. A failed report is reported, and the push continues either
# way. tools/README.md gives the rules in full.
#
# Coverage: a green full guard has run every runner gate, gate 36 included
# (whole, sharded, with the private store present), so its tests that skip
# or degrade in CI for want of the store have run here. A green fast path
# covers less (see its residual below).
#
# Site-only fast path (maintainer directive 2026-11-04: accelerated pushes when
# the change is web site content, not corpus or tooling).
#
#   Changed set: every record of the committed diff from the merge base of
#   BASE_REF (origin/main by default, the base tools/run-pr-time-checks.sh uses)
#   to HEAD, read after the fetch below as
#     git --no-replace-objects diff --raw -z --no-abbrev --no-renames
#         --no-relative --ignore-submodules=none <merge base> HEAD --
#   Records and paths are NUL-delimited and every path is matched literally.
#   The fast path needs every record to be an added or modified regular file:
#   status A from mode 000000 to 100644 or 100755, or status M with both modes
#   100644 or both 100755. A deletion, a rename (a deletion plus an addition
#   under --no-renames), a type change, a mode change, a gitlink (160000) or a
#   symlink (120000) means the full guard, and so does a path holding a
#   character other than A-Z, a-z, 0-9 and . _ / + @ - (every path git would
#   quote is among them) or an empty, . or .. component.
#
#   The guard FAILS CLOSED to the full guard when HEAD_REF names anything other
#   than HEAD; when PRE_PUSH_GUARD_ALLOW_DIRTY is set (the working tree the
#   gates read may then hold changes the diff does not show); when git config
#   sets diff.ignoreSubmodules, diff.relative or any submodule.<name>.ignore
#   (each could hide a change from a diff; the diff options above override them
#   as well) or cannot be read; when git cannot read the merge base or finds
#   more than one; when the diff fails, is empty, or holds a record it cannot
#   parse; and when tools/run_all_audits.sh cannot be read, a line in it that
#   names run_gate anywhere cannot be parsed, or its linter regression suite
#   gate is not there exactly once by name and command. Every line naming
#   run_gate must parse as a gate line, except the definition line
#   run_gate() { itself. A gate line parses only as
#   run_gate "<name>" python3 <command>, starting the line, where the name
#   holds no ", $, `, \ or | and the command is plain tokens of A-Z, a-z, 0-9
#   and _ . / = -, each separated by one space; the words are separated by
#   spaces and tabs only, the two blanks the shell splits on, so the shell gives
#   the runner the same words the guard reads: a quoted argument, an expansion,
#   a comment, a line continuation, a carriage return, a vertical tab or form
#   feed, or a run_gate call that does not start the line (behind a test, for
#   example) makes the line unparseable.
#
#   Site-only paths: anything under .web/ (the templates and the vendored
#   .web/baseline/ files) except a .py file, anything under .baseline/ except
#   a .py file, tests/test_web_draft.py, and the per-PR close-out surfaces
#   CHANGELOG.md, README.md and NOTICE.md at the repository root. README.md and
#   NOTICE.md belong: a site PR bumps the README library version (60d550d58),
#   and a baseline or licence change updates NOTICE.md; 65669d0c6 and
#   8fee33861 each change only .web/, .baseline/, tests/test_web_draft.py,
#   CHANGELOG.md, README.md and NOTICE.md. Both files are corpus-adjacent, so
#   every gate that scans them still runs. A .py file under .web/ (the
#   generator .web/build.py among them) or .baseline/ is tooling; the linter
#   regression suite tests .web/build.py and the .baseline/ scripts, and the
#   fast path does not run that suite, so a change to any such file takes the
#   full guard (maintainer decision 2026-11-04 13:02Z, scope B, read strictly:
#   Python tooling takes the full guard). Any other
#   path (a corpus document, tools/, any other test, .claude/,
#   .corpus-management/, .github/, a generated registry) means the full guard.
#
#   The fast path runs, stopping on the first failure:
#     1. tools/run-pr-time-checks.sh (unchanged; every delta gate, D3 included).
#     2. Every tools/run_all_audits.sh gate except the linter regression suite
#        (gate 36), in runner order, by the runner's own name and command, read
#        from its run_gate lines at run time, so a gate added to the runner runs
#        here by existing. As in the runner, a passing gate prints only OK and
#        a failing gate's output is printed in full; unlike the runner (and
#        unlike this guard's own FULL path, which echoes them), no advisory
#        line is echoed from a passing gate (neither the DUE-SOON lines the
#        runner shows for every gate nor the WARN and NOTE lines it shows for
#        the gates that opt in), and the step stops at the first failing
#        gate. The step ends with its elapsed time.
#     3. The palette gate .baseline/check_palette.py, with the arguments
#        .web/build.py passes it but without .web/build.py's pin check (step 4
#        runs .web/build.py, which makes that check).
#     4. .web/build.py --check and python3 -B tests/test_web_draft.py.
#   It prints one FAST PATH line naming the changed paths, then the reference
#   manifest advisory, then a PASS line with the elapsed time.
#
#   The skip lives here alone (maintainer decisions 2026-11-04 13:02Z and
#   17:36 EST, and 2026-11-05 09:08 EST): the guard lists the runner's gates
#   itself and runs each gate except 36, one at a time, on BOTH paths, then, on the
#   full path only, gate 36 as local shards, so tools/run_all_audits.sh takes
#   no skip option or variable and still runs gate 36 whole when invoked
#   directly (as the nightly sweep does), and .github/workflows/quality.yml
#   is never told to skip a gate: it runs every gate on every pull request,
#   gate 36 as six parallel shard jobs that together run exactly the serial
#   run's tests plus the lint job's partition-verifying --verify-shards step
#   (kept in lock-step with run_all_audits.sh by the gate-parity gate).
#
#   Skipped locally on the FAST PATH only, disclosed as left to CI: gate 36
#   (every tests/test_*.py module and the completeness checks
#   tools/run-linter-regression.py makes; the fast path still runs
#   tests/test_web_draft.py directly as its own step). On both paths, when
#   the gate list is read from the runner, the full guard's former
#   run_all_audits.sh summary line is not printed.
#   .github/workflows/quality.yml runs gate 36 whole, sharded, on every pull
#   request (each shard publishing its per-module credited-start counts and
#   unit-set digests), and tools/merge-when-green.py merges only when its
#   required check, the summary job that needs every shard and reconciles
#   those outputs, succeeded.
#
#   Residual (what is lost on the fast path): local detection, before the
#   push, of a gate 36 failure a site-only change causes; that failure first
#   shows in CI, on the shard running the failing test, and the merge guard
#   still blocks the merge. CI has no private store, so a gate 36 test that
#   needs the store and skips or degrades there runs before merge only on a
#   full-path push from a clone that has the store. On the fast path a
#   passing gate's DUE-SOON, WARN and NOTE lines are not shown before the
#   push (the full path shows them, as the runner does).
#
# Scope boundary: this guard gates PUSHES (the full guard's two post-commit /
# pre-push runners plus `.web/build.py --check` when .web/build.py is present,
# or the fast path's steps, where the build check always runs). The commit-time
# hygiene gate, `preflight-changelog.py`, gates COMMITS, because it judges
# newly-added lines that are already committed by push time. In a clone
# where tools/install-git-hooks.sh has installed the pre-commit hook,
# tools/check-changelog-preflight-commit.py runs it with --staged, judging
# the staged (index) lines, on each `git commit` that stages CHANGELOG.md;
# in a clone without the installer, the `&&` chain
# (`python3 tools/preflight-changelog.py && git commit`) remains the
# commit-time gate. The two helpers are complementary, not redundant.
#
# Usage:
#   git push -u origin <branch>
#   BASE_REF=origin/develop tools/pre-push-guard.sh   # non-default base
#
# Exit codes: 1 for an installed-hook check failure; 0 only if the gate steps, the local gate 36 shards and their reconcile, run-pr-time-checks.sh and the web check (when .web/build.py is present) pass, or on the fast path only if every fast-path check passes; 3 if the guard REFUSES to run
# because stdout is piped (the RM-10 self-defence below, before any runner
# starts); 4 if grc_library_private is required but absent (the _private check
# below); 5 if the tracked working tree is dirty or its state cannot be read
# (the attestation-soundness check below). At the local gate 36 shards (step
# 1b): the first failing shard's own exit status, in shard order, when any
# shard fails; otherwise 2 when the shard run cannot be set up or a shard
# exited 0 without writing its step outputs; otherwise the reconcile's own
# status when it fails (1 for a failure, 2 for a refusal); 130, 143 or 129
# when SIGINT, SIGTERM or SIGHUP interrupts the step. Otherwise the first
# failing blocking check's non-zero rc (that check's own diagnostics are
# printed above).

set -u

# RM-10 pipe self-defence (shipped PR #620, maintainer-approved
# 2026-07-03): refuse to run with stdout PIPED into another command, the
# shape that masks this guard's exit code (`guard | tail && push` pushes
# past a failing guard). Detection is `[ -p /dev/stdout ]`, not the
# spec's literal `[ -t 1 ]`: in this execution environment a plain
# invocation's stdout is a regular FILE (the harness capture), so a
# tty-check would fail every sanctioned run, while a pipe-check fails
# exactly the masking shape and passes both sanctioned patterns (plain
# run, and file-redirect capture `guard > log; CODE=$?`). CI is
# unaffected (it invokes the runners directly, and its stdout is not this
# guard's concern). Documented override for a deliberate, judged pipe:
#   PRE_PUSH_GUARD_ALLOW_PIPE=1 tools/pre-push-guard.sh | ...
# The sanctioned display-truncation path is tools/tail-safe.sh, which
# captures to a regular file (so it passes this check) and preserves the
# real exit code. Note: command substitution (out=$(guard)) is also
# refused (its stdout is a pipe) even though it preserves the exit code;
# use a file-redirect capture instead, or the override deliberately.
if [ -p /dev/stdout ] && [ -z "${PRE_PUSH_GUARD_ALLOW_PIPE:-}" ]; then
  echo "pre-push-guard: REFUSING to run with stdout piped (RM-10: a pipe masks this guard's exit code). Run it standalone, use a file-redirect capture, or use tools/tail-safe.sh -- tools/pre-push-guard.sh. Deliberate override: PRE_PUSH_GUARD_ALLOW_PIPE=1." >&2
  exit 3
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_NAME="$(basename "${REPO_ROOT}")"
cd "${REPO_ROOT}"

# _private defence-in-depth (1.19.8 (closing PR #1030) layered assurance): on the maintainer's
# OWN clone (origin is jposluns/grc_library), grc_library_private is a REQUIRED operational
# dependency. Fail LOUD at push time if it is absent, so a push authored without it (the
# Bash-write path the PreToolUse Edit/Write hook does not gate) is caught here too. This is
# identity-conditional: an adopter clone (any other origin) and CI are exempt (they legitimately
# have no _private). Exit 4 is the _private-refuse code (3 the pipe-refuse above, 5 the dirty-tree refuse below).
_origin="$(git remote get-url origin 2>/dev/null || true)"
# Boundary-anchored (a "/" or ":" before the owner) so a fork owner ending in "jposluns"
# is not misread as the maintainer.
case "${_origin}" in
  */jposluns/grc_library|*:jposluns/grc_library|*/jposluns/grc_library.git|*:jposluns/grc_library.git)
    if [ ! -d "${REPO_ROOT}/../grc_library_private" ] || [ -z "$(ls -A "${REPO_ROOT}/../grc_library_private" 2>/dev/null)" ]; then
      echo "pre-push-guard: REFUSING to push (1.19.8 (closing PR #1030) _private-required): origin is the maintainer repo but grc_library_private is absent or empty. It holds the operational state the CLAUDE.md delegation directive points to; clone it (git clone <the private sibling's remote URL> ../grc_library_private) or grant access (--add-dir ../grc_library_private), then retry. An adopter clone is exempt." >&2
      exit 4
    fi
    ;;
esac

# Working-tree-vs-committed-tree attestation soundness (git-add-drop backstop,
# 2026-09-19). The runners below read the WORKING TREE, but `git push` ships the
# COMMITTED tree (HEAD). When a tracked file is modified or staged the two differ,
# so a green run here can still flip CI red: the #2378 signature (a
# regenerated-but-unstaged generated artefact, an unstaged stale-count fix, any
# unstaged edit to a gate-read file all present local-green / CI-red). Refuse on a
# dirty tracked tree so the working-tree attestation equals HEAD for tracked
# content and the "from HEAD" runs below are sound. Untracked new files (??) are
# out of scope here (a first-generation output never `git add`ed); a queued
# commit-time hook (2a) will backstop that case. FAIL CLOSED: if `git status`
# itself errors, the tree state cannot be attested, so refuse rather than treat an
# empty result as clean (ignorance must refuse, not permit; the guard-input
# soundness discipline). Exit 5 is the dirty-tree / unattestable-tree refuse code.
# Deliberate override, rare and announced on the console like the pipe override:
# PRE_PUSH_GUARD_ALLOW_DIRTY=1.
if [ -z "${PRE_PUSH_GUARD_ALLOW_DIRTY:-}" ]; then
  if ! _dirty="$(git status --porcelain --untracked-files=no)"; then
    echo "pre-push-guard: REFUSING to run: 'git status' failed, so the working-tree state cannot be attested against HEAD (the committed tree that ships). Fix the repository state, then retry. Deliberate override: PRE_PUSH_GUARD_ALLOW_DIRTY=1." >&2
    exit 5
  fi
  if [ -n "${_dirty}" ]; then
    echo "pre-push-guard: REFUSING to run: tracked files are modified or staged, so the working-tree gate run would not attest what HEAD (the committed tree that ships) contains. Commit or stash the changes, then retry. Deliberate override: PRE_PUSH_GUARD_ALLOW_DIRTY=1." >&2
    exit 5
  fi
else
  echo "pre-push-guard: NOTE: PRE_PUSH_GUARD_ALLOW_DIRTY is set; skipping the dirty-tracked-tree attestation check (deliberate override)." >&2
fi

# Validate the shared dispatcher even for a direct run. CI has no private store.
sh tools/install-git-hooks.sh --check || exit $?

# The leftover report (header, "Leftover report"), in Python for its escaping,
# /proc reading and time bound. Mode "scan" reports what earlier runs left,
# on stderr; mode "left" reports one shard directory this run is keeping, on
# stdout; mode "identity" prints this guard's start time, pid namespace,
# boot id and machine id for its run records. The arguments are the mode,
# this clone's directory name, this guard's pid, this clone's git common
# directory as git rev-parse --git-common-dir names it to the shell (empty
# when that failed), and for "left" the shard directory. The report runs no
# git and starts and signals no process: it reads this clone's worktree
# registrations directly from <git common dir>/worktrees/*/ (gitdir,
# locked, HEAD and the run record), never following the final component of
# a path it reads and reading its type before opening it, and anything
# unreadable or malformed there is reported, never taken as clean. The scan
# runs in a worker thread with SCAN_BOUND seconds; the main thread then
# prints what the worker found so far, and an alarm ends the whole report
# at BOUND seconds, so a blocked call cannot hold the push. It stops,
# signals or removes nothing of a leftover, and it changes no git state.
LEFTOVER_PY='
import copy, errno, os, re, signal, stat, sys, threading, time
STARTED = time.monotonic()
BOUND = 5
SCAN_BOUND = 4
PREFIX = "grc-gate36-shards."
OWNER = "guard-owner"
RUN_RECORD = "grc-guard-owner"
PF_KTHREAD = 0x00200000
PF_EXITING = 0x00000004
SHARD = re.compile("shard-[1-9][0-9]*")
OBJECT_ID = re.compile(b"[0-9a-f]{40}|[0-9a-f]{64}")
REF_NAME = re.compile(b"refs/[A-Za-z0-9_./+@-]+")
# The branch a clone that keeps its refs in reftable names in HEAD of each
# git record, in place of its real HEAD (which only its reftable holds).
REFTABLE_STUB = b"refs/heads/.invalid"
# The labels of a process that uses a leftover whose guard identity the
# report could not establish: it stays one that gets the stop procedure.
# UNSURE_PARENTS covers every way its ancestry is not established: its own
# start time or a parent cannot be read, or the walk is not consistent.
UNSURE_SELF = "whether it is a pre-push guard is unknown: its start time cannot be read"
UNSURE_PARENTS = "whether a pre-push guard started it is unknown: its ancestry could not be established consistently"
ROOT_FILES = ("guard-owner", "reconcile.log")
SHARD_FILES = ("github-output", "shard.log", "worktree.log")
MAX_ITEMS = 64
MAX_RECORDS = 1024
MAX_LISTED = 50
MAX_MAPS = 8 << 20
SAFE = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./+@%=:,-")
DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
FILE_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
mode, repo_name, guard_pid = sys.argv[1], sys.argv[2], sys.argv[3]
common_arg = sys.argv[4] if len(sys.argv) > 4 else ""
only = os.path.realpath(sys.argv[5]) if mode == "left" else None
lock = threading.Lock()
shared = {"snap": None, "stage": "starting", "done": False, "stop": False}
QUOTE = chr(39)
BACKSLASH = chr(92)

class Bounded(Exception):
    pass

def q(text):
    raw = os.fsencode(text)
    if raw and raw[:1] != b"-" and all(b in SAFE for b in raw):
        return text
    out = []
    for b in raw:
        if b in (39, 92):
            out.append(BACKSLASH + chr(b))
        elif 32 <= b < 127 and b != 33:
            out.append(chr(b))
        else:
            out.append(BACKSLASH + "x%02x" % b)
    return "$" + QUOTE + "".join(out) + QUOTE

def shown(raw, limit=100):
    text = "".join(chr(b) if 32 <= b < 127 else BACKSLASH + "x%02x" % b for b in raw)
    return text if len(text) <= limit else text[:limit] + "..."

def remaining():
    return STARTED + SCAN_BOUND - time.monotonic()

def root_of(path):
    shard_dir, name = os.path.split(path)
    root, shard = os.path.split(shard_dir)
    base = os.path.basename(root)
    if name == repo_name and SHARD.fullmatch(shard) and base.startswith(PREFIX) and len(base) > len(PREFIX):
        return root
    return None

def read_small(path, dir_fd=None):
    fd = os.open(path, FILE_FLAGS, dir_fd=dir_fd)
    try:
        return os.read(fd, 4096)
    finally:
        os.close(fd)

def read_all(path, regular=False):
    # Whole, to MAX_MAPS bytes; with regular, NotRegular unless the open
    # descriptor is a regular file (checked before anything is read).
    fd = os.open(path, FILE_FLAGS)
    try:
        if regular and not stat.S_ISREG(os.fstat(fd).st_mode):
            raise NotRegular(22, "it is not a regular file")
        chunks, size = [], 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                return b"".join(chunks)
            size += len(chunk)
            if size > MAX_MAPS:
                raise OSError(27, "too large to read")
            chunks.append(chunk)
    finally:
        os.close(fd)

def proc_stat(pid):
    try:
        data = read_small("/proc/%s/stat" % pid)
    except (FileNotFoundError, ProcessLookupError):
        return None
    rest = data[data.rindex(b")") + 2:].split()
    return rest[19].decode("ascii"), rest[1].decode("ascii")

def identity(pid):
    try:
        found = proc_stat(pid)
        start = found[0] if found and found[0].isdigit() else "-"
    except (OSError, ValueError, IndexError):
        start = "-"
    try:
        ns = os.readlink("/proc/%s/ns/pid" % pid)
    except OSError:
        ns = "-"
    if not ns or any(c.isspace() for c in ns):
        ns = "-"
    return start, ns

def boot_id():
    try:
        boot = read_small("/proc/sys/kernel/random/boot_id").strip().decode("ascii")
    except (OSError, UnicodeDecodeError):
        return "-"
    return boot if boot and not any(c.isspace() for c in boot) else "-"

def machine_id():
    # This machine id (/etc/machine-id, a symbolic link followed, as the
    # system may make it one), or - when it cannot be read or is not the 32
    # lower-case hexadecimal digits systemd writes ("uninitialized" among
    # them): fail closed.
    try:
        fd = os.open("/etc/machine-id", os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        try:
            value = os.read(fd, 4096).strip().decode("ascii")
        finally:
            os.close(fd)
    except (OSError, UnicodeDecodeError):
        return "-"
    return value if re.fullmatch("[0-9a-f]{32}", value) else "-"

def parse_owner(data):
    # A run record (the guard-owner record of a shard directory, or the run
    # record beside the git record of a checkout), NUL-separated: pid,
    # clone, start time, pid namespace, boot id and machine id (- for one
    # that could not be read).
    parts = data.split(b"\0")
    if (len(parts) == 7 and parts[-1] == b"" and parts[0].isdigit()
            and parts[1][:1] == b"/" and (parts[2].isdigit() or parts[2] == b"-")
            and all(parts[3:6])):
        return {"pid": parts[0].decode("ascii"), "clone": os.fsdecode(parts[1]),
                "start": parts[2].decode("ascii"), "ns": os.fsdecode(parts[3]),
                "boot": os.fsdecode(parts[4]), "machine": os.fsdecode(parts[5])}
    return None

def record_state(owner):
    # Whether the run a record names has ended. Its pid, start time and pid
    # namespace mean something only under the kernel that ran it (its boot
    # id; the first pid namespace has the same name under every kernel), so
    # they are read only under the same boot id. Another boot id is another
    # kernel: an earlier boot of this machine only when the machine id is
    # this machine id too; otherwise another machine, VM or container that
    # shares this clone may still run it.
    pid, boot = owner["pid"], owner["boot"]
    if mode == "left" and pid == guard_pid:
        return "this", "this run made it and has not ended yet: the next push checks it again and prints the commands that remove it only once this run has ended and nothing uses it"
    now = boot_id()
    if boot == "-" or now == "-":
        return "unknown", "whether guard run pid %s ran under this kernel is unknown (%s), so whether it has ended is not proved" % (pid, "its boot id was not recorded" if boot == "-" else "the boot id of this kernel cannot be read")
    if boot == now:
        return run_state(owner)
    machine, here = owner["machine"], machine_id()
    if machine != "-" and machine == here:
        return "ended", "guard run pid %s ran during an earlier boot of this machine (its boot id differs, its machine id is this one)" % pid
    if machine == "-":
        why = "its machine id was not recorded"
    elif here == "-":
        why = "the machine id of this machine cannot be read"
    else:
        why = "its machine id %s is not this one" % shown(os.fsencode(machine))
    return "unknown", "guard run pid %s ran under another kernel (boot id %s), and %s, so it may still be running on another machine that shares this clone" % (pid, shown(os.fsencode(boot)), why)

def run_state(owner):
    pid, start, ns = owner["pid"], owner["start"], owner["ns"]
    if not os.path.isdir("/proc/self"):
        return "unknown", "whether guard run pid %s has ended is unknown (no /proc here)" % pid
    mine = identity("self")[1]
    if ns == "-" or mine == "-":
        return "unknown", "whether guard run pid %s has ended is unknown (its pid namespace %s)" % (pid, "was not recorded" if ns == "-" else "cannot be compared with this one, which cannot be read")
    if ns != mine:
        return "unknown", "guard run pid %s ran in another pid namespace (%s), so whether it has ended cannot be read from here" % (pid, shown(os.fsencode(ns)))
    try:
        found = proc_stat(pid)
    except (OSError, ValueError, IndexError):
        return "unknown", "whether guard run pid %s has ended is unknown (its /proc entry cannot be read)" % pid
    if found is None:
        return "ended", "no process %s exists" % pid
    if start == "-":
        return "unknown", "a process %s exists, and the record holds no start time to tell it from the run that made it" % pid
    if found[0] == start:
        return "running", "guard run pid %s is still running" % pid
    return "ended", "pid %s is now another process (its start time differs from the record)" % pid

def ancestors(pid):
    chain = []
    while pid and pid not in ("0", "1") and len(chain) < 64:
        chain.append(pid)
        try:
            found = proc_stat(pid)
        except (OSError, ValueError, IndexError):
            break
        if found is None:
            break
        pid = found[1]
    return chain

def unread_kind(pid):
    # What is known of a process whose working directory, root, descriptors
    # or mappings cannot be read, from its world-readable stat and status:
    # None for a kernel thread (PF_KTHREAD: it runs no user code, has no
    # memory map, shares the empty descriptor table and the working
    # directory of the kernel, so it cannot be using a leftover in any way
    # the scan reads); otherwise (own, privileged), where own is True when
    # its real or effective uid is yours and privileged is True when it may
    # be privileged (a uid of 0, any effective capability, or a status that
    # cannot be read). Every such process leaves use unknown.
    try:
        data = read_small("/proc/%s/stat" % pid)
        flags = int(data[data.rindex(b")") + 2:].split()[6])
        if flags & PF_KTHREAD:
            return None
    except (OSError, ValueError, IndexError):
        pass
    me = str(os.geteuid())
    own, uid_root, caps = True, None, None
    try:
        for line in read_all("/proc/%s/status" % pid).split(b"\n"):
            fields = line.decode("ascii", "replace").split()
            if line.startswith(b"Uid:") and len(fields) == 5:
                own = me in fields[1:3]
                uid_root = "0" in fields[1:]
            elif line.startswith(b"CapEff:") and len(fields) == 2:
                caps = int(fields[1], 16) != 0
    except (OSError, ValueError):
        pass
    return own, not (uid_root is False and caps is False)

def read_uses(base, roots, hits, maps=True):
    # The working directory, root, descriptors and (with maps) mappings of
    # the process or thread whose /proc directory is base, noted in hits.
    # True when its mappings were read and showed at least one mapping.
    def note(path, how):
        for root in roots:
            if path == root or path.startswith(root + os.sep):
                hits.setdefault(root, set()).add(how)
    note(os.readlink(base + "cwd"), "working directory")
    note(os.readlink(base + "root"), "root directory")
    for fd in os.listdir(base + "fd"):
        try:
            note(os.readlink(base + "fd/" + fd), "open file")
        except FileNotFoundError:
            pass
    if not maps:
        return False
    data = read_all(base + "maps")
    for line in data.split(b"\n"):
        parts = line.split(None, 5)
        if len(parts) == 6:
            path = os.fsdecode(parts[5])
            note(path, "mapped file")
            note(path.replace(BACKSLASH + "012", "\n"), "mapped file")
    return bool(data.strip())

def leader_exiting(base):
    # True when the thread-group leader whose /proc directory is base is
    # exiting (PF_EXITING in the flags of its stat) or has exited, and also
    # when its stat cannot be read or parsed, so that the caller then reads
    # the mappings of every thread (the more it reads, the more it finds).
    try:
        data = read_small(base + "stat")
        rest = data[data.rindex(b")") + 2:].split()
        return rest[0] in (b"Z", b"X", b"x") or bool(int(rest[6]) & PF_EXITING)
    except (OSError, ValueError, IndexError):
        return True

def thread_ended(base, exiting=False):
    # True when the thread whose /proc directory is base has exited (it is
    # gone, a zombie or dead): the kernel has then let go of its memory map,
    # descriptor table and working directory, so it holds nothing. With
    # exiting, asked only once an entry of the thread was found missing,
    # also when the kernel marks it exiting (PF_EXITING in the flags of its
    # stat) though it is not yet a zombie: an exiting thread lets go of its
    # memory map, then its descriptor table, then its working directory and
    # root, and an entry goes missing only once what it shows has been let
    # go, so by then it holds none of them. A thread whose entries are all
    # present is read, exiting or not.
    try:
        data = read_small(base + "stat")
    except (FileNotFoundError, ProcessLookupError):
        return True
    try:
        rest = data[data.rindex(b")") + 2:].split()
        if rest[0] in (b"Z", b"X", b"x"):
            return True
        return exiting and bool(int(rest[6]) & PF_EXITING)
    except (ValueError, IndexError):
        return False

def uses(pid, roots):
    # What of roots process pid uses. FileNotFoundError or ProcessLookupError
    # means it has gone; any other OSError, that it cannot be read. The
    # leader is read whole (working directory, root, descriptors and
    # mappings); then every other thread is read for its own working
    # directory, root and descriptors, since a thread can have its own
    # (unshare with CLONE_FS or CLONE_FILES). Mappings are not read per
    # thread while those of the leader stand for them: every thread of a
    # process shares one memory map. When the leader has exited while other
    # threads run, its entries are gone, so each thread is read whole. So
    # is each other thread when the leader, read whole, showed no mapping
    # or is exiting (leader_exiting) while other threads run (round 9,
    # claude NOTE 2): an exiting leader lets go of the shared memory map for
    # itself before its working directory and root (as a probe in that
    # review saw; not reproduced here), so it can be read whole with no
    # mapping while the other threads still map files. A thread whose
    # entries are missing counts as read only when it is then seen to have
    # exited or to be exiting (thread_ended with exiting); a thread that
    # cannot be read otherwise makes the process one that cannot be read.
    hits = {}
    base = "/proc/%s/" % pid
    leader = True
    try:
        mapped = read_uses(base, roots, hits)
    except (FileNotFoundError, ProcessLookupError):
        if not os.path.lexists(base + "stat"):
            raise
        leader = False
    try:
        tids = sorted(os.listdir(base + "task"))
    except (FileNotFoundError, ProcessLookupError):
        if not os.path.lexists(base + "stat"):
            raise
        raise OSError("the threads of process %s cannot be listed" % pid)
    maps = not leader
    if leader and len(tids) > 1 and (not mapped or leader_exiting(base)):
        maps = True
    for tid in tids:
        if leader and tid == pid:
            continue
        thread = "%stask/%s/" % (base, tid)
        if thread_ended(thread):
            continue
        try:
            read_uses(thread, roots, hits, maps=maps)
        except (FileNotFoundError, ProcessLookupError):
            if not thread_ended(thread, exiting=True):
                raise OSError("thread %s of process %s cannot be read" % (tid, pid))
    return hits

def command_line(pid):
    # Its command line, from a thread still running when the thread-group
    # leader has exited (an exited leader has none).
    base = "/proc/%s/" % pid
    try:
        cmd = read_small(base + "cmdline")
        if not cmd:
            for tid in sorted(os.listdir(base + "task")):
                cmd = read_small("%stask/%s/cmdline" % (base, tid))
                if cmd:
                    break
    except OSError:
        return "(command line unreadable)"
    cmd = cmd.rstrip(b"\0").replace(b"\0", b" ")
    return shown(cmd) if cmd else "(no command line)"

def live_runs(scan):
    # The live guard runs, by identity, never by command line: this guard
    # (its pid and start time), and every run record the scan read (the
    # guard-owner record of each shard directory under TMPDIR, of another
    # clone too, read before such a directory is set aside, and the run
    # record beside each git record of this clone) whose run is running:
    # the same boot id and pid namespace, and a process with its pid and
    # its start time. A set of (pid, start time).
    runs = set()
    start = identity(guard_pid)[0]
    if start != "-":
        runs.add((guard_pid, start))
    for owner in scan.run_records:
        if remaining() <= 0:
            raise Bounded()
        if owner["start"] != "-" and record_state(owner)[0] in ("running", "this"):
            runs.add((owner["pid"], owner["start"]))
    return runs

def guard_label(pid, start, live):
    # "a pre-push guard" when (pid, start) is a live run; "started by a
    # pre-push guard" when the (pid, start time) of one of its parents is,
    # the start time of each parent read as it is reached; UNSURE_SELF or
    # UNSURE_PARENTS when what decides it cannot be read or is not
    # consistent (it is then not labelled as either); None otherwise. The
    # walk is kept consistent, so a pid reused while it runs cannot join
    # an unrelated chain: the
    # process reread must still have the start time given; a parent must
    # not have started later than its child; and once a parent is read,
    # its child is read again and must still have the same parent pid and
    # start time (when a parent exits, its children get another parent
    # before its pid can be reused, so a reused pid shows here). Any
    # inconsistency is UNSURE_PARENTS.
    if (pid, start) in live:
        return "a pre-push guard"
    if start == "-" and pid in {p for p, _s in live}:
        return UNSURE_SELF
    try:
        found = proc_stat(pid)
    except (OSError, ValueError, IndexError):
        return UNSURE_PARENTS
    if found is None or not found[0].isdigit() or found[0] != start:
        return UNSURE_PARENTS
    child, seen = (pid,) + found, 0
    parent = found[1]
    while parent not in ("0", "1"):
        seen += 1
        if seen > 64:
            return UNSURE_PARENTS
        try:
            found = proc_stat(parent)
            again = proc_stat(child[0])
        except (OSError, ValueError, IndexError):
            return UNSURE_PARENTS
        if found is None or not found[0].isdigit():
            return UNSURE_PARENTS
        if int(found[0]) > int(child[1]):
            return UNSURE_PARENTS
        if again != child[1:]:
            return UNSURE_PARENTS
        if (parent, found[0]) in live:
            return "started by a pre-push guard"
        child = (parent,) + found
        parent = found[1]
    return None

def new_checkout():
    return {"exists": None, "registered": False, "locked": None, "prunable": None,
            "gitdir": None, "detail": None, "head": None, "branch": None, "head_problem": None,
            "record": None, "record_state": None, "admin": None}

class Scan:
    def __init__(self):
        self.groups = {}
        self.notes = []
        self.here = None
        self.common = None
        self.reg_problem = None
        self.reg_unread = []
        self.run_records = []
        self.procs_read = False
        self.proc_note = None
        self.unread_own = 0
        self.unread_other = 0
        self.unread_privileged = 0

    def group(self, root):
        if root not in self.groups:
            self.groups[root] = {"exists": True, "read": False, "dir": False, "uid": None,
                                 "mode": None, "owner": None, "owner_ours": False,
                                 "run": None, "checkouts": {}, "unexpected": [],
                                 "unreadable": [], "problems": [], "truncated": False,
                                 "users": [], "inside": False}
        return self.groups[root]

def publish(scan, stage):
    with lock:
        if shared["stop"]:
            raise SystemExit
        shared["snap"] = copy.deepcopy(scan)
        shared["stage"] = stage

def read_owner(scan, root, g, rfd):
    try:
        data = read_file(OWNER, rfd)
    except FileNotFoundError:
        return
    except NotRegular:
        g["owner"] = "malformed"
        return
    except OSError as exc:
        g["owner"] = "unreadable"
        g["unreadable"].append((os.path.join(root, OWNER), exc.strerror))
        return
    owner = parse_owner(data)
    if owner is None:
        g["owner"] = "malformed"
    else:
        g["owner"] = owner
        g["owner_ours"] = os.path.realpath(owner["clone"]) == scan.here
        scan.run_records.append(owner)

class NotRegular(OSError):
    pass

def check_regular(name, dir_fd=None):
    # Its type, read without following its final component, before it is
    # ever opened, so a FIFO or other entry that is not a regular file is
    # not opened (opening a FIFO would complete the open of a writer
    # blocked on it): ELOOP for a symbolic link, NotRegular for anything
    # else that is not a regular file. This check and the open that follows
    # are two lookups by name, so an entry swapped in between them (by one
    # who can write its directory) is opened; each caller then checks the
    # type of the open descriptor and closes it unread when it is not a
    # regular file. (An O_PATH descriptor reopened through /proc/self/fd
    # would close the window, at the cost of a second open of each file
    # through /proc; it is not used, since a swap needs write access to
    # that directory and the descriptor check already keeps the report
    # from reading what was swapped in.)
    st = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    if stat.S_ISLNK(st.st_mode):
        raise OSError(errno.ELOOP, os.strerror(errno.ELOOP))
    if not stat.S_ISREG(st.st_mode):
        raise NotRegular(22, "it is not a regular file")

def read_file(name, dir_fd=None):
    # A regular file, read no-follow (its first 4096 bytes), its type
    # checked before it is opened and again once it is open; NotRegular
    # when it is something else.
    check_regular(name, dir_fd)
    fd = os.open(name, FILE_FLAGS, dir_fd=dir_fd)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise NotRegular(22, "it is not a regular file")
        return os.read(fd, 4096)
    finally:
        os.close(fd)

def resolve_ref(scan, ref):
    # The commit the branch ref names, from its loose ref file in the git
    # common directory or else its packed-refs line, as (commit, None); or
    # (None, why) when neither can be read or it names no commit.
    if not REF_NAME.fullmatch(ref) or any(p in (b"", b".", b"..") for p in ref.split(b"/")):
        return None, "it is not a ref name this report reads"
    try:
        data = read_file(os.path.join(scan.common, os.fsdecode(ref)))
    except (FileNotFoundError, NotADirectoryError):
        data = None
    except OSError as exc:
        return None, "its ref file cannot be read (%s)" % exc.strerror
    if data is not None:
        if OBJECT_ID.fullmatch(data.strip()):
            return data.strip().decode("ascii"), None
        return None, "its ref file is not in a form this report reads"
    try:
        check_regular(os.path.join(scan.common, "packed-refs"))
        packed = read_all(os.path.join(scan.common, "packed-refs"), regular=True)
    except FileNotFoundError:
        return None, "no ref file or packed ref names it"
    except OSError as exc:
        return None, "packed-refs cannot be read (%s)" % exc.strerror
    for line in packed.split(b"\n"):
        parts = line.rstrip(b"\r").split(b" ")
        if len(parts) == 2 and parts[1] == ref and OBJECT_ID.fullmatch(parts[0]):
            return parts[0].decode("ascii"), None
    return None, "no ref file or packed ref names it"

def read_registrations(scan):
    # The checkouts registered with this clone, read directly from their
    # git records, <git common dir>/worktrees/<id>/, as git worktree list
    # reads them (the report runs no git): the checkout path is the gitdir
    # file without its trailing blanks and /.git (a relative one read
    # against the git record, as git reads it), locked is the reason in the
    # locked file ("" when it gives none), the commit is read from HEAD (a
    # branch through its ref), and an unlocked checkout whose .git the
    # gitdir names does not exist is prunable, with the reason git gives. Every
    # read is no-follow, its type read before it is opened. A git record
    # that git would skip (an entry that is not a directory or a symbolic
    # link, or has no gitdir file) is skipped; one that cannot be read or
    # is malformed (a symbolic link, as the record itself or as its gitdir
    # file, or an unreadable or empty gitdir) is kept in scan.reg_unread,
    # never dropped; HEAD that cannot be read (the placeholder HEAD of a
    # reftable clone among them) is kept as the head_problem of that
    # checkout. The run record beside each git record is read too. Returns
    # None, with the reason in scan.reg_problem, when the records cannot be
    # listed.
    base = os.path.join(scan.common, "worktrees")
    try:
        bfd = os.open(base, DIR_FLAGS)
    except FileNotFoundError:
        return []
    except OSError as exc:
        scan.reg_problem = "%s cannot be read (%s)" % (q(base), exc.strerror)
        return None
    records = []
    try:
        try:
            names = sorted(os.listdir(bfd))
        except OSError as exc:
            scan.reg_problem = "%s cannot be listed (%s)" % (q(base), exc.strerror)
            return None
        if len(names) > MAX_RECORDS:
            scan.reg_problem = "%s holds more than %d git records, more than the report reads" % (q(base), MAX_RECORDS)
            return None
        for name in names:
            if remaining() <= 0:
                raise Bounded()
            admin = os.path.join(base, name)
            # Its type first, without following it: git follows a symbolic
            # link here and reads the record it names, which the report
            # does not, so a link is kept as unreadable; git skips any
            # other entry that is not a directory, and so does the report.
            # (Opening a link with O_DIRECTORY and O_NOFOLLOW fails with
            # ENOTDIR, the error of an entry git skips, so the type is
            # read before, never inferred from that error.)
            try:
                st = os.stat(name, dir_fd=bfd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            except OSError as exc:
                scan.reg_unread.append((admin, exc.strerror))
                continue
            if stat.S_ISLNK(st.st_mode):
                scan.reg_unread.append((admin, "it is a symbolic link, which the report does not follow"))
                continue
            if not stat.S_ISDIR(st.st_mode):
                continue
            try:
                afd = os.open(name, DIR_FLAGS, dir_fd=bfd)
            except FileNotFoundError:
                continue
            except OSError as exc:
                scan.reg_unread.append((admin, exc.strerror))
                continue
            try:
                record = read_registration(scan, admin, afd)
            finally:
                os.close(afd)
            if record is not None:
                records.append(record)
    finally:
        os.close(bfd)
    return records

def read_registration(scan, admin, afd):
    try:
        raw = read_file("gitdir", afd).rstrip()
    except FileNotFoundError:
        return None
    except OSError as exc:
        scan.reg_unread.append((os.path.join(admin, "gitdir"), exc.strerror))
        return None
    if not raw:
        scan.reg_unread.append((os.path.join(admin, "gitdir"), "it is empty"))
        return None
    dotgit = os.fsdecode(raw)
    path = os.fsdecode(raw[:-5] if raw.endswith(b"/.git") else raw)
    if not os.path.isabs(path):
        path = os.path.realpath(os.path.join(admin, path))
    r = {"worktree": path, "admin": admin, "locked": None, "prunable": None, "HEAD": None,
         "branch": None, "head_problem": None, "record": read_run_record(afd)}
    if isinstance(r["record"], dict):
        scan.run_records.append(r["record"])
    try:
        r["locked"] = os.fsdecode(read_file("locked", afd).strip())
    except FileNotFoundError:
        pass
    except OSError as exc:
        r["locked"] = "its lock file cannot be read (%s)" % exc.strerror
    if r["locked"] is None and not os.path.lexists(os.path.join(admin, dotgit)):
        r["prunable"] = "gitdir file points to non-existent location"
    try:
        head = read_file("HEAD", afd).strip()
    except OSError as exc:
        r["head_problem"] = "its HEAD cannot be read (%s)" % exc.strerror
        return r
    if head.startswith(b"ref: ") and head[5:].strip() == REFTABLE_STUB:
        r["head_problem"] = "reftable HEAD not read: its HEAD names %s, the placeholder a clone that keeps its refs in reftable writes there, and the report reads no reftable" % shown(REFTABLE_STUB)
    elif head.startswith(b"ref: "):
        ref = head[5:].strip()
        r["branch"] = os.fsdecode(ref)
        r["HEAD"], why = resolve_ref(scan, ref)
        if why:
            r["head_problem"] = "its HEAD names %s, whose commit cannot be read: %s" % (shown(ref), why)
    elif OBJECT_ID.fullmatch(head):
        r["HEAD"] = head.decode("ascii")
    else:
        r["head_problem"] = "its HEAD is not in a form this report reads"
    return r

def read_run_record(afd):
    # The run record a guard writes beside the git record of each checkout
    # it registers (RUN_RECORD in <git common dir>/worktrees/<id>/, open as
    # afd): a parsed record, or "missing", "unreadable" or "malformed".
    try:
        data = read_file(RUN_RECORD, afd)
    except FileNotFoundError:
        return "missing"
    except NotRegular:
        return "malformed"
    except OSError:
        return "unreadable"
    return parse_owner(data) or "malformed"

def read_checkout(scan, g, path, sfd, name):
    c = g["checkouts"].setdefault(path, new_checkout())
    c["exists"] = True
    try:
        cfd = os.open(name, DIR_FLAGS, dir_fd=sfd)
    except OSError as exc:
        c["gitdir"], c["detail"] = "unreadable", exc.strerror
        return
    try:
        try:
            check_regular(".git", cfd)
            fd = os.open(".git", FILE_FLAGS, dir_fd=cfd)
        except FileNotFoundError:
            c["gitdir"] = "missing"
            return
        except NotRegular:
            c["gitdir"], c["detail"] = "foreign", "its .git is not a file"
            return
        except OSError as exc:
            c["gitdir"], c["detail"] = "unreadable", exc.strerror
            return
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                c["gitdir"], c["detail"] = "foreign", "its .git is not a file"
                return
            line = os.read(fd, 4096)
        except OSError as exc:
            c["gitdir"], c["detail"] = "unreadable", exc.strerror
            return
        finally:
            os.close(fd)
    finally:
        os.close(cfd)
    if scan.common is None:
        c["gitdir"], c["detail"] = "unknown", "this clone repository directory is unknown"
        return
    if not line.startswith(b"gitdir: "):
        c["gitdir"], c["detail"] = "foreign", "its .git is not a gitdir: line"
        return
    target = os.fsdecode(line[len(b"gitdir: "):].rstrip(b"\r\n"))
    target = os.path.realpath(os.path.join(path, target))
    if os.path.dirname(target) == os.path.join(scan.common, "worktrees"):
        c["gitdir"] = "ours"
    else:
        c["gitdir"], c["detail"] = "foreign", "its .git names %s" % q(target)

def read_shard(scan, g, root, rfd, name):
    path = os.path.join(root, name)
    try:
        sfd = os.open(name, DIR_FLAGS, dir_fd=rfd)
    except OSError as exc:
        g["unreadable"].append((path, exc.strerror))
        return
    try:
        try:
            names = sorted(os.listdir(sfd))
        except OSError as exc:
            g["unreadable"].append((path, exc.strerror))
            return
        if len(names) > MAX_ITEMS:
            g["truncated"] = True
            names = names[:MAX_ITEMS]
        for entry in names:
            try:
                st = os.stat(entry, dir_fd=sfd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            except OSError as exc:
                g["unreadable"].append((os.path.join(path, entry), exc.strerror))
                continue
            if entry == repo_name and stat.S_ISDIR(st.st_mode):
                read_checkout(scan, g, os.path.join(path, entry), sfd, entry)
            elif entry in SHARD_FILES and stat.S_ISREG(st.st_mode):
                continue
            elif stat.S_ISLNK(st.st_mode) and entry != repo_name:
                continue
            else:
                g["unexpected"].append(os.path.join(path, entry))
        for cpath, c in g["checkouts"].items():
            if os.path.dirname(cpath) == path and c["exists"] is None:
                c["exists"] = False
    finally:
        os.close(sfd)

def read_root(scan, root):
    g = scan.group(root)
    if g["read"]:
        return
    g["read"] = True
    if scan.here == root or scan.here.startswith(root + os.sep):
        g["inside"] = True
    try:
        st = os.lstat(root)
    except FileNotFoundError:
        g["exists"] = False
        return
    except OSError as exc:
        g["unreadable"].append((root, exc.strerror))
        return
    if not stat.S_ISDIR(st.st_mode):
        g["problems"].append("it is not a directory (it is a %s)" % ("symbolic link" if stat.S_ISLNK(st.st_mode) else "file or other entry"))
        return
    g["dir"], g["uid"], g["mode"] = True, st.st_uid, stat.S_IMODE(st.st_mode)
    try:
        rfd = os.open(root, DIR_FLAGS)
    except OSError as exc:
        g["unreadable"].append((root, exc.strerror))
        return
    try:
        read_owner(scan, root, g, rfd)
        try:
            names = sorted(os.listdir(rfd))
        except OSError as exc:
            g["unreadable"].append((root, exc.strerror))
            return
        if len(names) > MAX_ITEMS:
            g["truncated"] = True
            names = names[:MAX_ITEMS]
        for name in names:
            try:
                st = os.stat(name, dir_fd=rfd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            except OSError as exc:
                g["unreadable"].append((os.path.join(root, name), exc.strerror))
                continue
            if SHARD.fullmatch(name) and stat.S_ISDIR(st.st_mode):
                read_shard(scan, g, root, rfd, name)
            elif not (name in ROOT_FILES and stat.S_ISREG(st.st_mode)):
                g["unexpected"].append(os.path.join(root, name))
    finally:
        os.close(rfd)

def relevant(g):
    if g["unreadable"] or g["inside"] or g["owner"] in ("unreadable", "malformed"):
        return True
    if isinstance(g["owner"], dict) and g["owner_ours"]:
        return True
    return any(c["registered"] or c["gitdir"] in ("ours", "unreadable", "unknown")
               for c in g["checkouts"].values())

def run():
    scan = Scan()
    publish(scan, "reading this clone repository directory")
    scan.here = os.path.realpath(".")
    if common_arg and os.path.isdir(common_arg):
        scan.common = os.path.realpath(common_arg)
    else:
        scan.reg_problem = "this clone repository directory is unknown"
        scan.notes.append("UNREADABLE: this clone repository directory is unknown (%s), so which checkouts are its own is unknown" % ("git rev-parse --git-common-dir failed in the guard" if not common_arg else "%s is not a directory" % q(common_arg)))
    publish(scan, "listing the temporary directory")
    if only is None:
        tmp = os.path.realpath(os.environ.get("TMPDIR") or "/tmp")
        try:
            entries = sorted(os.scandir(tmp), key=lambda e: e.name)
        except FileNotFoundError:
            entries = []
        except OSError as exc:
            entries = []
            scan.notes.append("UNREADABLE: the temporary directory %s cannot be listed (%s), so shard directories left there are unknown" % (q(tmp), exc.strerror))
        for entry in entries:
            if not (entry.name.startswith(PREFIX) and len(entry.name) > len(PREFIX)):
                continue
            try:
                st = entry.stat(follow_symlinks=False)
            except FileNotFoundError:
                continue
            except OSError as exc:
                scan.group(entry.path)["unreadable"].append((entry.path, exc.strerror))
                continue
            if st.st_uid != os.geteuid() or not stat.S_ISDIR(st.st_mode):
                continue
            scan.group(entry.path)
    else:
        scan.group(only)
    publish(scan, "reading the shard directories")
    for root in sorted(scan.groups):
        read_root(scan, root)
        publish(scan, "reading the shard directories")
    publish(scan, "reading the git worktree records")
    records = read_registrations(scan) if scan.common is not None else None
    if records is None:
        if scan.common is not None:
            scan.notes.append("UNREADABLE: %s, so the checkouts registered with this clone are unknown" % scan.reg_problem)
        records = []
    for path, err in scan.reg_unread:
        scan.notes.append("UNREADABLE: %s (%s), so whether that git record registers a checkout of a leftover is unknown; no leftover has a removal command while it cannot be read" % (q(path), err))
    for r in records:
        root = root_of(r["worktree"])
        if root is None or (only is not None and root != only):
            continue
        c = scan.group(root)["checkouts"].setdefault(r["worktree"], new_checkout())
        c["registered"], c["locked"], c["prunable"] = True, r["locked"], r["prunable"]
        c["head"], c["branch"], c["head_problem"] = r["HEAD"], r["branch"], r["head_problem"]
        c["admin"], c["record"] = r["admin"], r["record"]
    for root in sorted(scan.groups):
        read_root(scan, root)
        for path, c in scan.groups[root]["checkouts"].items():
            if c["exists"] is None and not scan.groups[root]["unreadable"]:
                c["exists"] = os.path.lexists(path)
        publish(scan, "reading the git worktree records")
    for root in [r for r, g in scan.groups.items() if not relevant(g)]:
        del scan.groups[root]
    gone = {path: c for g in scan.groups.values() if not g["exists"]
            for path, c in g["checkouts"].items() if c["registered"] and c["exists"] is False}
    if gone:
        publish(scan, "reading the run records of checkouts whose directory is gone")
        for path in sorted(gone):
            record = gone[path]["record"]
            if isinstance(record, dict):
                gone[path]["record_state"] = record_state(record)
        publish(scan, "reading the run records of checkouts whose directory is gone")
    publish(scan, "reading which processes use the leftovers")
    if scan.groups:
        for g in scan.groups.values():
            if isinstance(g["owner"], dict):
                g["run"] = record_state(g["owner"])
        roots = [r for r, g in scan.groups.items() if g["dir"] or not g["exists"]]
        if not os.path.isdir("/proc/self"):
            scan.proc_note = "processes cannot be read here (no /proc)"
        else:
            try:
                pids = sorted((n for n in os.listdir("/proc") if n.isdigit()), key=int)
            except OSError as exc:
                pids = []
                scan.proc_note = "processes cannot be listed (%s)" % exc.strerror
            me = str(os.getpid())
            family = ancestors(guard_pid)
            live = live_runs(scan)
            for pid in pids:
                if pid == me:
                    continue
                if remaining() <= 0:
                    raise Bounded()
                try:
                    hits = uses(pid, roots)
                except (FileNotFoundError, ProcessLookupError):
                    continue
                except OSError:
                    kind = unread_kind(pid)
                    if kind is not None:
                        if kind[0]:
                            scan.unread_own += 1
                        else:
                            scan.unread_other += 1
                        if kind[1]:
                            scan.unread_privileged += 1
                    continue
                for root, how in hits.items():
                    cmd = command_line(pid)
                    start = identity(pid)[0]
                    if pid == guard_pid:
                        label = "this guard"
                    elif pid in family:
                        label = "started this push"
                    else:
                        label = guard_label(pid, start, live)
                    scan.groups[root]["users"].append((pid, cmd, sorted(how), label, start))
            scan.procs_read = scan.proc_note is None
    publish(scan, "finishing")
    with lock:
        shared["done"] = True

def worker():
    try:
        run()
    except (SystemExit, Bounded):
        pass
    except BaseException as exc:
        with lock:
            shared["error"] = "%s: %s" % (type(exc).__name__, shown(str(exc).encode("utf-8", "replace")))

def checkout_line(path, c):
    if c["registered"]:
        what = "registered with this clone"
        if c["locked"] is not None:
            what += ", locked" + (": " + shown(os.fsencode(c["locked"])) if c["locked"] else "")
        if c["prunable"] is not None:
            what += "; git would list it as prunable" + (" (" + shown(os.fsencode(c["prunable"])) + ")" if c["prunable"] else "")
    else:
        what = "not registered with this clone"
    what += {True: "; its directory exists", False: "; its directory does not exist",
             None: "; whether its directory exists is unknown"}[c["exists"]]
    what += {"ours": "; its .git points into this clone", "missing": "; it has no .git file",
             "unreadable": "; its .git cannot be read (%s)" % c["detail"],
             "foreign": "; it is not a checkout of this clone (%s)" % c["detail"],
             "unknown": "; whose checkout it is is unknown (%s)" % c["detail"], None: ""}[c["gitdir"]]
    return "    checkout %s: %s" % (q(path), what)

def assess(root, g, complete, scan):
    reasons = []
    if not complete:
        reasons.append("the scan did not finish, so what it holds and whether a process uses it are not fully known")
    for path, err in g["unreadable"]:
        reasons.append("UNREADABLE: %s (%s); it is not reported as clean" % (q(path), err))
    reasons.extend(g["problems"])
    if scan.reg_problem:
        reasons.append("the checkouts registered with this clone are unknown (%s)" % scan.reg_problem)
    if scan.reg_unread:
        reasons.append("%d git record(s) of this clone cannot be read (listed below), so the checkouts registered with this clone are not fully known" % len(scan.reg_unread))
    if not g["exists"]:
        reasons.extend(gone_reasons(g, scan))
    elif g["dir"]:
        if g["uid"] != os.geteuid():
            reasons.append("it is owned by uid %d, not by you" % g["uid"])
        owner = g["owner"]
        if owner is None and g["read"] and not g["unreadable"]:
            reasons.append("it has no guard-owner record (an older guard made it, or its run stopped before writing one), so which run made it and whether that run has ended are unknown")
        elif owner == "malformed":
            reasons.append("its guard-owner record is not in the form this guard writes")
        elif isinstance(owner, dict):
            if not g["owner_ours"]:
                reasons.append("its guard-owner record names another clone, %s" % q(owner["clone"]))
            if g["run"] is None:
                reasons.append("whether guard run pid %s has ended was not read" % owner["pid"])
            elif g["run"][0] != "ended":
                reasons.append(g["run"][1])
    if g["inside"]:
        reasons.append("this push runs inside it (this clone, %s, is in it)" % q(scan.here))
    for path, c in sorted(g["checkouts"].items()):
        if c["locked"] is not None:
            reasons.append("checkout %s is locked" % q(path))
        if c["registered"] and c["head_problem"]:
            reasons.append("the git record of checkout %s: %s" % (q(path), c["head_problem"]))
        if c["exists"] is None:
            reasons.append("whether checkout %s exists is unknown" % q(path))
        elif c["exists"] and c["gitdir"] != "ours":
            reasons.append("checkout %s is not proven to be a checkout of this clone (see below)" % q(path))
        elif c["exists"] and not c["registered"]:
            reasons.append("checkout %s points into this clone, but no git record of this clone registers it" % q(path))
        if c["exists"] and c["prunable"] is not None:
            reasons.append("git would list checkout %s as prunable although its directory exists" % q(path))
    for path in g["unexpected"]:
        reasons.append("it holds %s, which this guard does not make" % q(path))
    if g["truncated"]:
        reasons.append("it holds more than %d entries in one directory, more than the report reads" % MAX_ITEMS)
    if g["users"]:
        reasons.append("%d process(es) use it, listed below" % len(g["users"]))
    elif complete:
        unread = scan.unread_own + scan.unread_other
        if not scan.procs_read:
            reasons.append("whether a process uses it is unknown (%s)" % (scan.proc_note or "the scan did not reach the processes"))
        elif unread and g["exists"]:
            reasons.append("%d process(es) could not be read (%d of yours, %d of other users; %d of them may be privileged), so whether one uses it is unknown: its mode does not exclude one, since a privileged or setuid process, or one handed a descriptor, can use it anyway" % (unread, scan.unread_own, scan.unread_other, scan.unread_privileged))
    if g["exists"]:
        removable = not reasons and isinstance(g["owner"], dict) and g["run"] is not None and g["run"][0] == "ended"
    else:
        removable = not reasons
    if not reasons and not removable:
        reasons.append("it is not proven to be a finished run of this guard in this clone")
    return removable, reasons

def gone_reasons(g, scan):
    # A shard directory that is gone leaves only git records of its
    # checkouts. git worktree remove -- <checkout> then removes only that
    # record (it cannot touch a directory that does not exist), so the one
    # thing to prove is that the run that registered the checkout, the only
    # run that could own it, has ended: the run record beside its git
    # record must name this clone and a run that has ended. The checks of
    # assess (scan complete, git records read, checkout unlocked and absent,
    # no process seen using the old path) apply too.
    reasons = []
    if not g["checkouts"]:
        reasons.append("its directory does not exist and no checkout of this clone is registered in it")
    for path, c in sorted(g["checkouts"].items()):
        record = c["record"]
        if not c["registered"] or c["exists"] is not False:
            continue
        if record is None:
            reasons.append("its directory does not exist, and the run record beside the git record of checkout %s was not read, so whether the run that registered it has ended is not proved" % q(path))
        elif record == "missing":
            reasons.append("its directory does not exist, and no run record beside the git record of checkout %s shows which run registered it (an older guard writes none, or its run stopped before writing it), so whether that run has ended is not proved" % q(path))
        elif record in ("unreadable", "malformed"):
            reasons.append("its directory does not exist, and the run record beside the git record of checkout %s is %s, so whether the run that registered it has ended is not proved" % (q(path), "unreadable" if record == "unreadable" else "not in the form this guard writes"))
        elif os.path.realpath(record["clone"]) != scan.here:
            reasons.append("the run record of checkout %s names another clone, %s" % (q(path), q(record["clone"])))
        elif c["record_state"] is None:
            reasons.append("whether guard run pid %s, which registered checkout %s, has ended was not read" % (record["pid"], q(path)))
        elif c["record_state"][0] != "ended":
            reasons.append("checkout %s: %s" % (q(path), c["record_state"][1]))
    return reasons

def manual_check(path, c):
    # For a git record an older guard left with no run record: the facts
    # known are printed above it; this is what a person checks by hand
    # before the narrow command, which the report does not prove and so
    # does not give as a removal command.
    head = shown(os.fsencode(c["head"])) if c["head"] else None
    lines = ["      NOT PROVED, so no removal command: no run record shows which run registered it. To check it by hand (its git record is %s):" % q(c["admin"]),
             "        1. that no run of this guard that could have registered it is still running, on this host or on another host, VM or container that shares this clone;"]
    if head:
        lines.append("        2. that HEAD %s is held by a branch or tag, or is not needed (git branch --all --contains %s; git tag --contains %s);" % (head, head, head))
    else:
        lines.append("        2. which commit its git record holds (the report could not read its HEAD), and that it is held by a branch or tag, or is not needed;")
    lines.append("        3. that the checkout directory still does not exist (ls -ld -- %s)." % q(path))
    lines.append("        Only then, by your own judgement: git worktree remove -- %s removes that git record alone." % q(path))
    return lines

def stop_check(g):
    # For a leftover a process uses: what a person checks by hand before
    # stopping one, marked NOT PROVED and never given as a command. There
    # is none while the run that made it is live (its processes belong to
    # that push), and none for this guard, the processes that started this
    # push, a pre-push guard or a process with a pre-push guard among its
    # parents (a live run of this guard, on this host). The leftover stays
    # INSPECT: the report of the next push decides whether it is REMOVABLE.
    # A guard is known by its identity (live_runs), never by its command
    # line; a process whose guard identity could not be read in full is not
    # labelled a guard and gets the procedure, whose step 2 checks it. Only
    # a run whose run record the scan read is known (a run writes one from
    # its gate 36 step on, and a fast-path run never does), so the
    # procedure says that only the guards the report identified are
    # labelled.
    run = g["run"]
    if run is not None and run[0] in ("running", "this"):
        return ["    no stop procedure: the guard run that made it has not ended, and the processes using it belong to that run; let that run end"]
    eligible = sorted((u for u in g["users"] if u[3] in (None, UNSURE_SELF, UNSURE_PARENTS)),
                      key=lambda u: int(u[0]))
    if not eligible:
        return ["    no stop procedure: each process using it is this guard, started this push, is a pre-push guard or was started by one"]
    lines = ["    NOT PROVED, so no stop command: the report does not prove that a process using it is abandoned. To stop one by hand (never this guard, a process that started this push, a pre-push guard or a process one started; only the guards the report identified are labelled above, and a guard run whose run record it did not read, such as a fast-path run, which writes none, is not), check:",
             "      1. that no run of this guard that could have made it is still running, on this host or on another host, VM or container that shares this clone (a live run uses its own shard directory: let it end);",
             "      2. that the process is not part of another push (no pre-push guard among its parents) and that stopping it loses nothing you need;",
             "      3. just before any signal, that the pid is still the process listed here, since a pid can be reused: its start time (field 22 of /proc/<pid>/stat) and its command line (/proc/<pid>/cmdline) must still be:"]
    for pid, cmd, _how, _label, start in eligible:
        if start == "-":
            lines.append("           pid %s: its start time could not be read, so it cannot be rechecked: do not signal it" % pid)
        else:
            lines.append("           pid %s: start time %s, command line %s" % (pid, start, cmd))
    lines.append("      Only then, by your own judgement, stop it (TERM before anything stronger); then push again, and remove the leftover only if the report of that push marks it REMOVABLE.")
    return lines

def render(root, g, complete, scan):
    removable, reasons = assess(root, g, complete, scan)
    lines = []
    if removable and not g["exists"]:
        lines.append("  %s: REMOVABLE: its directory does not exist, and the guard run that registered each checkout in it has ended (see below), so only the git record of each checkout is left" % q(root))
    elif removable:
        lines.append("  %s: REMOVABLE: guard run pid %s of this clone made it and has ended (%s); every process this /proc shows was read (kernel threads aside: the working directory, root directory and open files of each of its threads, and its mapped files), and none uses it there" % (q(root), g["owner"]["pid"], g["run"][1]))
    else:
        lines.append("  %s: INSPECT (no removal command), because:" % q(root))
        for reason in reasons:
            lines.append("    - " + reason)
    owner = g["owner"]
    if isinstance(owner, dict):
        lines.append("    guard-owner record: guard run pid %s, clone %s" % (owner["pid"], q(owner["clone"])))
    for path, c in sorted(g["checkouts"].items()):
        lines.append(checkout_line(path, c))
        gone = c["exists"] is False and c["registered"]
        if gone and isinstance(c["record"], dict):
            state = c["record_state"][1] if c["record_state"] else "whether it has ended was not read"
            lines.append("      its run record: guard run pid %s, clone %s (%s)" % (c["record"]["pid"], q(c["record"]["clone"]), state))
        # The HEAD of a checkout whose git record alone is left, and of one
        # that exists and is given git worktree remove --force (which also
        # discards its uncommitted changes and untracked files).
        if c["registered"] and c["head"] and (gone or (removable and c["exists"])):
            lines.append("      its git record holds HEAD %s%s; a commit made there that no branch or tag holds is lost with the record" % (shown(os.fsencode(c["head"])), " on " + shown(os.fsencode(c["branch"])) if c["branch"] else " (detached)"))
        if gone and c["record"] == "missing" and c["admin"] and c["locked"] is None and not removable:
            lines.extend(manual_check(path, c))
    for pid, cmd, how, label, _start in sorted(g["users"], key=lambda u: int(u[0])):
        lines.append("    used by pid %s%s: %s (%s)" % (pid, " (" + label + ")" if label else "", cmd, ", ".join(how)))
    if g["users"]:
        lines.extend(stop_check(g))
    if removable and not g["exists"]:
        lines.append("    to remove only the git record of each checkout (its HEAD is shown above):")
        for path, c in sorted(g["checkouts"].items()):
            lines.append("      git worktree remove -- %s" % q(path))
    elif removable:
        if g["checkouts"]:
            lines.append("    to remove it (git worktree remove --force discards the uncommitted changes and untracked files of each checkout, and a commit made there that no branch or tag holds is lost; the HEAD of each checkout is shown above):")
        else:
            lines.append("    to remove it:")
        for path, c in sorted(g["checkouts"].items()):
            lines.append("      git worktree remove --force -- %s" % q(path))
        lines.append("      rm -rf -- %s" % q(root))
    return lines

def main():
    signal.signal(signal.SIGALRM, signal.SIG_DFL)
    signal.alarm(BOUND)
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    thread.join(max(0.0, remaining() + 0.3))
    scan, complete, stage, error, held = Scan(), False, None, None, True
    # The exit path: with lock, stop the worker and take what it found.
    if lock.acquire(timeout=max(0.05, STARTED + BOUND - 0.5 - time.monotonic())):
        try:
            shared["stop"] = True
            scan = shared["snap"] or Scan()
            complete = shared["done"]
            stage = shared["stage"]
            error = shared.get("error")
            held = False
        finally:
            lock.release()
    body = []
    groups = sorted(scan.groups.items())
    for root, g in [(r, g) for r, g in groups if relevant(g)][:MAX_LISTED]:
        body.extend(render(root, g, complete, scan))
    hidden = len([g for _r, g in groups if relevant(g)]) - MAX_LISTED
    if hidden > 0:
        body.append("  %d more leftover(s) are not listed here" % hidden)
    for note in scan.notes:
        body.append("  " + note)
    out = []
    if mode == "left":
        if body:
            out.append("Left behind by this run (nothing was removed; the next push reports it until it is removed):")
            out.extend(body)
    elif body:
        out.append("pre-push guard: LEFTOVERS of earlier runs of this guard in this clone (report only: the report ran no git and started and signalled no process; no process of a leftover was stopped or signalled, nothing was removed and no git state was changed; the push continues):")
        out.extend(body)
    if error:
        out.append("pre-push guard: the leftover scan failed (%s), so the report is INCOMPLETE; leftovers it had not reached are not listed, and none listed has a removal command." % error)
    elif not complete:
        if held:
            out.append("pre-push guard: the leftover scan is INCOMPLETE: its state could not be read within the %ds bound; leftovers are not listed." % BOUND)
        else:
            out.append("pre-push guard: the leftover scan is INCOMPLETE: its %ds scan bound (the whole report is bounded to %ds) was reached while %s; leftovers it had not reached are not listed, and none listed has a removal command." % (SCAN_BOUND, BOUND, stage))
    if out:
        sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()
    os._exit(0)

if mode == "identity":
    sys.stdout.write("%s %s %s %s\n" % (identity(guard_pid) + (boot_id(), machine_id())))
else:
    main()
'

# This clone's git common directory, which the leftover report reads the
# worktree registrations from (the report itself runs no git); empty when
# git cannot name it, which the report reports. git names it relative to
# the current directory, the repository root here, so a relative one is
# made absolute against that root. This git command runs before the
# report starts and is not under its 5-second bound (no bounded form is
# used: the guard does not rely on timeout(1)); a git that stalls here
# delays the push as any other git command of the guard would.
if ! GUARD_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"; then
    GUARD_COMMON_DIR=""
fi
case "${GUARD_COMMON_DIR}" in
    "" | /*) ;;
    *) GUARD_COMMON_DIR="${REPO_ROOT}/${GUARD_COMMON_DIR}" ;;
esac

# Runs the leftover report in mode $1 (see LEFTOVER_PY), with this clone's
# name, this guard's pid and this clone's git common directory, and any
# further arguments. Its status is captured inside an `if`, so an inherited
# errexit cannot end the guard; a failure is reported, never taken as a
# clean scan.
leftover_report() {
    local mode="$1" rc unknown how
    shift
    if python3 -I -c "${LEFTOVER_PY}" "${mode}" "${REPO_NAME}" "$$" "${GUARD_COMMON_DIR}" "$@"; then
        return 0
    else
        rc=$?
    fi
    if [ "${mode}" = left ]; then
        unknown="what this run left in ${1:-its shard directory} (named above) and whether a process uses it are unknown"
    else
        unknown="what earlier runs of this guard left is unknown"
    fi
    if [ "${rc}" -eq 142 ]; then
        how="was ended at its 5-second bound before it printed"
    else
        how="failed (rc=${rc})"
    fi
    echo "pre-push guard: WARNING: the leftover report (${mode}) ${how}, so ${unknown}; it stopped and removed nothing of a leftover." >&2
    return 0
}

leftover_report scan >&2

# Best-effort refresh of the merge base so the delta gates in
# run-pr-time-checks.sh compare against the true base ref (origin/main by
# default; whatever BASE_REF names otherwise). Fetching all of origin keeps
# the refresh correct under a BASE_REF override. Offline is tolerated:
# run-pr-time-checks.sh falls back to whatever base ref exists locally, and a
# stale base only risks a false PASS on the delta gates, which CI then catches.
if ! git fetch origin --quiet 2>/dev/null; then
  echo "pre-push-guard: WARNING: fetch of origin failed; delta gates use the locally available base, which may be stale." >&2
fi

# Site-only fast path selection (see the header). Any doubt leaves fast_path at
# 0 with the reason in full_reason, so the full guard runs.
BASE_REF="${BASE_REF:-origin/main}"
# The runner's linter regression suite gate (gate 36), as "runner name|command":
# the one runner gate the fast path does not run whole.
REGRESSION_GATE="Linter regression test suite|tools/run-linter-regression.py"
# The full guard's local gate 36 shard count: the quality workflow's six
# regression-shard jobs (a regression test keeps the two equal).
REGRESSION_SHARD_COUNT=6
# The siblings each shard checkout's parent links back to this clone's own,
# so a shard reaches the private store and siblings as the serial run does.
REGRESSION_SHARD_SIBLINGS=(private grc_library_private grc_library_ref grc_library_scratch)
# Seconds a stopped shard's process group has after TERM before KILL.
REGRESSION_SHARD_STOP_GRACE=10
fast_path=0
full_reason=""
changed_paths=()
fast_gates=()

# True when a changed path is site-only (see the header), matched literally.
# The allowed characters are listed one by one, not as ranges, so the match
# does not depend on the locale.
site_only_path() {
    local path="$1"
    case "${path}" in
        "" | *[!ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._/+@-]*) return 1 ;;
    esac
    case "/${path}/" in
        *//* | */./* | */../*) return 1 ;;
    esac
    # Python tooling, .web/build.py among it; * here also matches "/".
    case "${path}" in
        .web/*.py | .baseline/*.py) return 1 ;;
    esac
    case "${path}" in
        .web/?* | .baseline/?* | tests/test_web_draft.py | CHANGELOG.md | README.md | NOTICE.md) return 0 ;;
    esac
    return 1
}

# The runner's gates, as "runner name|command" in runner order, read from its
# run_gate lines into runner_gates (shared by the fast path and the full
# guard, which both run every gate but gate 36). A line that names run_gate
# anywhere, other than the function's definition line, but does not match the
# one shape the runner uses, an unreadable runner, or a gate 36 line missing
# or repeated leaves the reason in runner_gates_reason and returns 1. The
# name holds nothing the shell expands inside double quotes, and the command
# is plain tokens separated by single spaces (see the header), so the shell
# splits it exactly as the guard does. The blanks are space and tab alone,
# the two the shell splits words on, not [[:space:]], which also admits a
# carriage return, vertical tab and form feed. The characters are listed one
# by one, not as ranges, so the match does not depend on the locale.
runner_gates=()
runner_gates_reason=""
read_runner_gates() {
    local line name key found=0 blank gate_re token
    local -a gates=()
    blank='[ '$'\t'']'
    token='[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./=-]+'
    gate_re='^run_gate'"${blank}"'+"([^"$`\|]+)"'"${blank}"'+python3'"${blank}"'+('"${token}"'( '"${token}"')*)'"${blank}"'*$'
    if [ ! -f tools/run_all_audits.sh ] || [ ! -r tools/run_all_audits.sh ]; then
        runner_gates_reason="tools/run_all_audits.sh cannot be read, so the gates to run cannot be listed"
        return 1
    fi
    while IFS= read -r line || [ -n "${line}" ]; do
        [[ "${line}" == *run_gate* ]] || continue
        [ "${line}" = "run_gate() {" ] && continue
        if ! [[ "${line}" =~ ${gate_re} ]]; then
            runner_gates_reason="the tools/run_all_audits.sh line '${line}' cannot be parsed, so the gates to run cannot be listed"
            return 1
        fi
        name="${BASH_REMATCH[1]}"
        key="${name}|${BASH_REMATCH[2]}"
        if [ "${key}" = "${REGRESSION_GATE}" ]; then
            found=$((found + 1))
        else
            gates+=("${key}")
        fi
    done < tools/run_all_audits.sh
    if [ "${found}" -ne 1 ]; then
        runner_gates_reason="tools/run_all_audits.sh has ${found} linter regression suite gate lines ('${REGRESSION_GATE%%|*}' running ${REGRESSION_GATE#*|}), not one, so the gate the guard narrows cannot be named"
        return 1
    fi
    if [ "${#gates[@]}" -eq 0 ]; then
        runner_gates_reason="tools/run_all_audits.sh has no gate besides the linter regression suite"
        return 1
    fi
    runner_gates=("${gates[@]}")
    return 0
}
# The status is captured inside an `if`, so an inherited errexit (SHELLOPTS)
# cannot end the guard on a reading failure; the full guard then fails closed
# to the whole runner, gate 36 included.
if read_runner_gates; then
    runner_gates_ok=1
else
    runner_gates_ok=0
fi

# Sets fast_path to 1 when the push qualifies, filling changed_paths and
# fast_gates; otherwise returns with the reason in full_reason.
select_fast_path() {
    local hiding rc merge_base record_re header path shown ended=0
    if [ -n "${HEAD_REF:-}" ] && [ "${HEAD_REF}" != "HEAD" ]; then
        full_reason="HEAD_REF is ${HEAD_REF}, not HEAD, so the changed set would not describe the tree the gates read"
        return
    fi
    if [ -n "${PRE_PUSH_GUARD_ALLOW_DIRTY:-}" ]; then
        full_reason="PRE_PUSH_GUARD_ALLOW_DIRTY is set, so the working tree may hold changes outside the committed diff"
        return
    fi
    # git config exits 1 when no key matches. The status is captured inside an
    # `if`, so an inherited errexit (SHELLOPTS) cannot end the guard here.
    if hiding="$(git config --name-only --get-regexp '^(diff\.ignoresubmodules|diff\.relative|submodule\..+\.ignore)$')"; then
        rc=0
    else
        rc=$?
    fi
    if [ "${rc}" -eq 0 ]; then
        full_reason="git config sets ${hiding//$'\n'/, }, which could hide a change from the changed set"
        return
    elif [ "${rc}" -ne 1 ]; then
        full_reason="git config cannot be read (rc=${rc}), so a setting that hides changes cannot be ruled out"
        return
    fi
    if ! merge_base="$(git --no-replace-objects merge-base --all "${BASE_REF}" HEAD 2>/dev/null)" \
            || [ -z "${merge_base}" ]; then
        full_reason="the merge base of ${BASE_REF} and HEAD cannot be read"
        return
    fi
    if [[ "${merge_base}" == *$'\n'* ]]; then
        full_reason="${BASE_REF} and HEAD have more than one merge base"
        return
    fi
    # Each record is a header field and a path field, each NUL-terminated. The
    # diff's own exit status follows as one more field, "END <rc>", so a failed
    # or cut-short diff cannot pass for a complete one. The status is captured
    # inside an `if`, so an inherited errexit cannot drop that field.
    record_re='^:([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}|[0-9a-f]{64}) ([0-9a-f]{40}|[0-9a-f]{64}) ([A-Z])$'
    while IFS= read -r -d '' header; do
        if [ "${ended}" -eq 1 ]; then
            full_reason="the changed set has data after the end of git diff's output"
            return
        fi
        case "${header}" in
            "END 0") ended=1; continue ;;
            "END "*)
                full_reason="git diff ${merge_base} HEAD failed (rc=${header#END }), so the changed set cannot be read"
                return
                ;;
        esac
        if ! [[ "${header}" =~ ${record_re} ]]; then
            printf -v shown '%q' "${header}"
            full_reason="the changed-set record ${shown} cannot be read"
            return
        fi
        if ! IFS= read -r -d '' path; then
            full_reason="a changed-set record has no path"
            return
        fi
        printf -v shown '%q' "${path}"
        case "${BASH_REMATCH[5]}:${BASH_REMATCH[1]}:${BASH_REMATCH[2]}" in
            A:000000:100644 | A:000000:100755 | M:100644:100644 | M:100755:100755) ;;
            *)
                full_reason="${shown} is not an added or modified regular file with its mode unchanged (status ${BASH_REMATCH[5]}, mode ${BASH_REMATCH[1]} to ${BASH_REMATCH[2]})"
                return
                ;;
        esac
        if ! site_only_path "${path}"; then
            full_reason="${shown} is not a site-only path"
            return
        fi
        changed_paths+=("${path}")
    done < <(if git --no-replace-objects diff --raw -z --no-abbrev --no-renames --no-relative \
                    --ignore-submodules=none "${merge_base}" HEAD --; then
                 printf 'END 0\0'
             else
                 printf 'END %s\0' "$?"
             fi)
    if [ "${ended}" -ne 1 ] || [ -n "${header}" ]; then
        full_reason="the changed set ends before git diff's exit status, so it cannot be read"
        return
    fi
    if [ "${#changed_paths[@]}" -eq 0 ]; then
        full_reason="the changed set against ${BASE_REF} is empty"
        return
    fi

    # The runner's gates, read once above by read_runner_gates (shared with
    # the full guard). A reading failure means the full guard, which then
    # fails closed to the whole runner.
    if [ "${runner_gates_ok}" -ne 1 ]; then
        full_reason="${runner_gates_reason}"
        return
    fi
    fast_gates=("${runner_gates[@]}")
    fast_path=1
}
select_fast_path

# One fast-path step: run it and, on a non-zero status, report it and exit with
# that status. The status is captured inside an `if` that keeps it (not the
# negated `if !` form the capture note below warns of), so an inherited errexit
# cannot end the guard before the report.
fast_step() {
    local label="$1"
    shift
    local rc
    echo ""
    echo "=== pre-push guard fast path: ${label} ==="
    if "$@"; then rc=0; else rc=$?; fi
    if [ "${rc}" -ne 0 ]; then
        echo ""
        echo "pre-push guard FAILED at ${label} (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi
}

# One FULL-path audit gate, with the runner's advisory echo: as in
# tools/run_all_audits.sh run_gate, the gate runs with a fresh per-gate
# GRC_RUNNER_ECHO_TOKEN (CSPRNG, /dev/urandom fallback, else empty and said
# so); on a pass its DUE-SOON lines are always shown, and its WARN and NOTE
# lines too when the gate opted in by printing the runner-echo marker line
# with this run's token (gates 6, 72 and 106; the token is the part data
# cannot forge). A failing gate's output is printed in full before the guard
# exits with the gate's status. The status is captured inside an `if`, as in
# fast_step.
audit_gate_echo() {
    local prefix="$1"
    local label="$2"
    shift 2
    local out rc token marker advisory
    token="$(python3 -c 'import secrets; print(secrets.token_hex(16))' 2>/dev/null)"
    [[ "${token}" =~ ^[0-9a-f]{32}$ ]] || token="$(od -An -N16 -tx1 /dev/urandom 2>/dev/null | tr -d ' \n')"
    [[ "${token}" =~ ^[0-9a-f]{32}$ ]] || token=""
    printf '%-66s ... ' "${prefix}: ${label}"
    if out="$(GRC_RUNNER_ECHO_TOKEN="${token}" "$@" 2>&1)"; then rc=0; else rc=$?; fi
    if [ "${rc}" -ne 0 ]; then
        echo "FAIL (rc=${rc})"
        printf '%s\n' "${out}"
        echo ""
        echo "pre-push guard FAILED at ${label} (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi
    echo "OK"
    [ -n "${token}" ] || echo "      NOTE: no random source for the advisory-echo token; this gate's advisory WARN/NOTE lines are not shown"
    marker="runner-echo: tools/run_all_audits.sh shows this gate's advisory lines on a pass"
    advisory='^DUE-SOON'
    if [ -n "${token}" ] \
        && printf '%s\n' "${out}" | grep -xF -- "${marker} ${token}" >/dev/null; then
        advisory='^(DUE-SOON|WARN|NOTE)'
    fi
    printf '%s\n' "${out}" | grep -E "${advisory}" | sed 's/^/      /' || true
}

# One FAST-path audit gate: like tools/run_all_audits.sh, a passing
# gate's output stays hidden (its advisory lines are not echoed here; the
# header discloses that) and a
# failing gate's output is printed in full before the guard exits with the
# gate's status. The status is captured inside an `if`, as in fast_step.
audit_gate() {
    local prefix="$1"
    local label="$2"
    shift 2
    local out rc
    printf '%-66s ... ' "${prefix}: ${label}"
    if out="$("$@" 2>&1)"; then rc=0; else rc=$?; fi
    if [ "${rc}" -ne 0 ]; then
        echo "FAIL (rc=${rc})"
        printf '%s\n' "${out}"
        echo ""
        echo "pre-push guard FAILED at ${label} (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi
    echo "OK"
}

# Gate 36 whole, as REGRESSION_SHARD_COUNT parallel local shards (header,
# step 1b). shard_root and shard_dirs (indexed from 1) name the temporary
# directories, so a failure can keep and print them; shard_pids (indexed
# from 1) holds each running shard's pid, which is also its process group.
shard_root=""
shard_dirs=()
shard_pids=()

# A failed local shard run: keep every checkout and log, print where they
# are, and exit with rc.
shard_fail() {
    local rc="$1" message="$2" i
    trap - INT TERM HUP
    echo ""
    echo "pre-push guard FAILED at gate 36 local shards (rc=${rc}): ${message}."
    if [ -n "${shard_root}" ]; then
        echo "The shard checkouts and logs are kept for inspection under ${shard_root}:"
        for i in "${!shard_dirs[@]}"; do
            echo "  shard ${i}: ${shard_dirs[i]} (checkout ${shard_dirs[i]}/${REPO_NAME}, log ${shard_dirs[i]}/shard.log)"
        done
        # What is left (the directory, its checkouts and any process still
        # using it), with no removal command while this run lasts; the next
        # push reports it again until it is removed.
        leftover_report left "${shard_root}"
    fi
    echo "Fix the artefact; do not push."
    exit "${rc}"
}

# INT, TERM or HUP during the shard step (the trap run_gate36_shards sets):
# TERM every shard's process group, KILL any group still alive after
# REGRESSION_SHARD_STOP_GRACE seconds, wait for every shard, then keep and
# name every checkout and log and exit 128 + the signal number. Further
# signals are ignored while the shards are stopped.
shard_interrupted() {
    local name="$1" rc="$2" i alive deadline
    trap '' INT TERM HUP
    echo ""
    echo "pre-push guard: SIG${name} received during the gate 36 local shards; stopping every shard's process group."
    for i in "${!shard_pids[@]}"; do
        kill -TERM -- "-${shard_pids[i]}" 2>/dev/null || kill -TERM "${shard_pids[i]}" 2>/dev/null || true
    done
    deadline=$((SECONDS + REGRESSION_SHARD_STOP_GRACE))
    while :; do
        alive=""
        for i in "${!shard_pids[@]}"; do
            if kill -0 -- "-${shard_pids[i]}" 2>/dev/null; then
                alive="${alive:+${alive} }${i}"
            fi
        done
        [ -n "${alive}" ] || break
        if [ "${SECONDS}" -ge "${deadline}" ]; then
            echo "pre-push guard: shard(s) ${alive} still running ${REGRESSION_SHARD_STOP_GRACE}s after TERM; sending KILL."
            for i in ${alive}; do
                kill -KILL -- "-${shard_pids[i]}" 2>/dev/null || true
            done
            break
        fi
        sleep 0.2
    done
    for i in "${!shard_pids[@]}"; do
        wait "${shard_pids[i]}" 2>/dev/null || true
    done
    shard_fail "${rc}" "interrupted by SIG${name}; every shard's process group was stopped and waited for"
}

run_gate36_shards() {
    local count="${REGRESSION_SHARD_COUNT}" commit parent store i dir tree rc started
    local sibling ran verdict first_rc=0 failed="" reconcile_rc no_output="" out
    local identity owner_start owner_ns owner_boot owner_machine admin
    local -a statuses=() pairs=() unremoved=()
    trap 'shard_interrupted INT 130' INT
    trap 'shard_interrupted TERM 143' TERM
    trap 'shard_interrupted HUP 129' HUP
    echo ""
    echo "=== pre-push guard 1b/3: linter regression suite (gate 36) whole, as ${count} parallel local shards, each in its own checkout of the commit being pushed ==="
    started=${SECONDS}
    if ! commit="$(git rev-parse --verify --quiet 'HEAD^{commit}')" || [ -z "${commit}" ]; then
        shard_fail 2 "HEAD cannot be read, so the commit being pushed cannot be checked out"
    fi
    if ! parent="$(cd "${REPO_ROOT}/.." && pwd -P)"; then
        shard_fail 2 "the directory holding this clone cannot be read, so its siblings cannot be linked"
    fi
    if ! shard_root="$(mktemp -d "${TMPDIR:-/tmp}/grc-gate36-shards.XXXXXX")" || [ -z "${shard_root}" ]; then
        shard_root=""
        shard_fail 2 "cannot create the temporary shard directory"
    fi
    # Its physical path, so each checkout's path is the one git registers.
    if ! dir="$(cd "${shard_root}" && pwd -P)" || [ -z "${dir}" ]; then
        shard_fail 2 "the temporary shard directory ${shard_root} cannot be resolved"
    fi
    shard_root="${dir}"
    # The guard-owner record: this guard's pid, this clone, and this guard's
    # start time, pid namespace, boot id and machine id (read from /proc and
    # /etc/machine-id, - when they cannot be read), NUL-separated, so a
    # later push's leftover report knows the directory is this clone's and
    # tells this run, while it lasts, from a finished one even after its pid
    # is reused or under another kernel.
    if ! identity="$(python3 -I -c "${LEFTOVER_PY}" identity "${REPO_NAME}" "$$")"; then
        identity="- - - -"
    fi
    read -r owner_start owner_ns owner_boot owner_machine <<< "${identity}"
    if ! printf '%s\0%s\0%s\0%s\0%s\0%s\0' "$$" "${REPO_ROOT}" "${owner_start:--}" "${owner_ns:--}" \
            "${owner_boot:--}" "${owner_machine:--}" > "${shard_root}/guard-owner"; then
        shard_fail 2 "cannot write ${shard_root}/guard-owner"
    fi
    # A relative GRC_STORE is read against the repository root, so it is made
    # absolute here to keep naming this clone's store from a shard checkout.
    store="${GRC_STORE:-}"
    if [ -n "${store}" ] && [ "${store#/}" = "${store}" ]; then
        store="${REPO_ROOT}/${store}"
    fi
    for ((i = 1; i <= count; i++)); do
        dir="${shard_root}/shard-${i}"
        tree="${dir}/${REPO_NAME}"
        shard_dirs[i]="${dir}"
        if ! mkdir "${dir}" || ! : > "${dir}/github-output"; then
            shard_fail 2 "cannot create ${dir}"
        fi
        if ! git worktree add --detach "${tree}" "${commit}" > "${dir}/worktree.log" 2>&1; then
            cat "${dir}/worktree.log"
            shard_fail 2 "git worktree add --detach of ${commit} into ${tree} failed"
        fi
        # The run record beside the checkout's git record
        # (<git common dir>/worktrees/<id>/grc-guard-owner): the guard-owner
        # fields, boot id and machine id among them, so that once the shard
        # directory is gone (a reboot, or a temporary-directory cleaner) a
        # later leftover report can prove that the run which registered the
        # checkout has ended. git worktree remove and prune delete it with
        # the record. Without it that report keeps the record INSPECT, so a
        # failure to write it is noted and the run goes on.
        if admin="$(unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_PREFIX
                    git -C "${tree}" rev-parse --absolute-git-dir 2>/dev/null)" \
                && [ -n "${admin}" ] && [ -d "${admin}" ] \
                && printf '%s\0%s\0%s\0%s\0%s\0%s\0' "$$" "${REPO_ROOT}" "${owner_start:--}" \
                    "${owner_ns:--}" "${owner_boot:--}" "${owner_machine:--}" \
                    > "${admin}/grc-guard-owner"; then
            :
        else
            echo "pre-push guard: NOTE: could not write the run record beside the git record of ${tree}; if this run's shard directory is removed before the checkout is, a later push cannot prove this run has ended, and reports that record as INSPECT." >&2
        fi
        for sibling in "${REGRESSION_SHARD_SIBLINGS[@]}"; do
            if [ -e "${parent}/${sibling}" ] || [ -L "${parent}/${sibling}" ]; then
                if ! ln -s "${parent}/${sibling}" "${dir}/${sibling}"; then
                    shard_fail 2 "cannot link ${dir}/${sibling} to ${parent}/${sibling}"
                fi
            fi
        done
    done
    # Each shard runs its own checkout's runner, from that checkout, with its
    # own GITHUB_OUTPUT file and log and stdin from /dev/null; Git's
    # repository variables are cleared so a git command in a test reads the
    # shard's checkout. Job control is on only while the shards start, so
    # each shard (a subshell that execs the runner) leads its own process
    # group, which the signal trap stops whole.
    set -m
    for ((i = 1; i <= count; i++)); do
        (
            cd "${shard_dirs[i]}/${REPO_NAME}" || exit 2
            unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_PREFIX
            if [ -n "${store}" ]; then
                export GRC_STORE="${store}"
            fi
            export GITHUB_OUTPUT="${shard_dirs[i]}/github-output"
            exec python3 tools/run-linter-regression.py --shard "${i}/${count}"
        ) < /dev/null > "${shard_dirs[i]}/shard.log" 2>&1 &
        shard_pids[i]=$!
    done
    set +m
    # Each exit status is read directly from wait, inside an `if` that keeps
    # it, so an inherited errexit cannot end the guard before the report.
    for ((i = 1; i <= count; i++)); do
        if wait "${shard_pids[i]}"; then rc=0; else rc=$?; fi
        statuses[i]="${rc}"
        ran="$(grep -E '^Ran [0-9]+ tests? in ' "${shard_dirs[i]}/shard.log" | tail -n 1 || true)"
        verdict="$(grep -E '^(OK|FAILED)( \(.*\))?$' "${shard_dirs[i]}/shard.log" | tail -n 1 || true)"
        echo "gate 36 local shard ${i}/${count}: rc=${rc}; ${ran:-no Ran line}; ${verdict:-no result line} (log ${shard_dirs[i]}/shard.log)"
        if [ "${rc}" -ne 0 ]; then
            failed="${failed:+${failed}, }${i}"
            [ "${first_rc}" -ne 0 ] || first_rc="${rc}"
        elif [ ! -s "${shard_dirs[i]}/github-output" ]; then
            no_output="${no_output:+${no_output}, }${i}"
        fi
    done
    shard_pids=()
    for ((i = 1; i <= count; i++)); do
        if [ "${statuses[i]}" -ne 0 ]; then
            echo ""
            echo "--- gate 36 local shard ${i}/${count} failed (rc=${statuses[i]}); the last 60 lines of ${shard_dirs[i]}/shard.log:"
            tail -n 60 "${shard_dirs[i]}/shard.log"
        fi
        pairs+=("${statuses[i]}" "${shard_dirs[i]}/github-output")
    done
    # A shard that exited 0 must have written its step outputs; without them
    # the reconcile has nothing of that shard to check, so it is not run.
    if [ -z "${failed}" ] && [ -n "${no_output}" ]; then
        shard_fail 2 "shard(s) ${no_output} of ${count} exited 0 but wrote no step outputs (GITHUB_OUTPUT file missing or empty), so the reconcile was not run"
    fi
    # The reconcile reads tests/ from the first shard's checkout (the commit
    # being pushed), with that checkout's own tool.
    echo ""
    echo "gate 36 local shard reconcile (tools/reconcile-regression-shards.py --shard-outputs ${count}):"
    if (cd "${shard_dirs[1]}/${REPO_NAME}" \
            && exec python3 tools/reconcile-regression-shards.py --shard-outputs "${count}" "${pairs[@]}") \
            > "${shard_root}/reconcile.log" 2>&1; then
        reconcile_rc=0
    else
        reconcile_rc=$?
    fi
    sed 's/^/      /' "${shard_root}/reconcile.log"
    if [ -n "${failed}" ]; then
        shard_fail "${first_rc}" "shard(s) ${failed} of ${count} failed (reconcile rc=${reconcile_rc})"
    fi
    if [ "${reconcile_rc}" -ne 0 ]; then
        shard_fail "${reconcile_rc}" "the shard reconcile failed (rc=${reconcile_rc})"
    fi
    trap - INT TERM HUP
    # A passing run removes every temporary checkout, then the shard
    # directory. rmtree removes the sibling links as links and never follows
    # them, and it runs only on a real directory named grc-gate36-shards.*.
    for ((i = 1; i <= count; i++)); do
        tree="${shard_dirs[i]}/${REPO_NAME}"
        if out="$(git worktree remove --force "${tree}" 2>&1)"; then
            :
        else
            rc=$?
            unremoved+=("${tree}")
            echo "pre-push guard: WARNING: git worktree remove --force failed (rc=${rc}) for the shard checkout ${tree}: ${out//$'\n'/ }" >&2
        fi
    done
    case "${shard_root##*/}" in
        grc-gate36-shards.?*)
            if [ -d "${shard_root}" ] && [ ! -L "${shard_root}" ] \
                    && python3 -I -c 'import shutil, sys; shutil.rmtree(sys.argv[1])' "${shard_root}"; then
                rc=0
            else
                rc=1
            fi
            ;;
        *) rc=1 ;;
    esac
    if [ "${rc}" -ne 0 ]; then
        echo "pre-push guard: WARNING: could not remove the shard directory ${shard_root}." >&2
    fi
    if [ "${#unremoved[@]}" -gt 0 ]; then
        # The registration of a checkout git could not remove is stale once
        # its directory is gone; prune clears it then, and only then.
        if out="$(git worktree prune 2>&1)"; then rc=0; else rc=$?; fi
        echo "pre-push guard: WARNING: ran git worktree prune (rc=${rc})${out:+: ${out//$'\n'/ }}." >&2
        out="$(git worktree list --porcelain 2>/dev/null || true)"
        for tree in "${unremoved[@]}"; do
            if [[ $'\n'"${out}"$'\n' == *$'\n'"worktree ${tree}"$'\n'* ]]; then
                echo "pre-push guard: WARNING: the shard checkout ${tree} is still registered; once its directory is gone, run git worktree prune." >&2
            else
                echo "pre-push guard: WARNING: the shard checkout ${tree} was not removed by git worktree remove; its registration is no longer listed after git worktree prune." >&2
            fi
        done
        echo "pre-push guard: gate 36 passed as ${count} local shards in $((SECONDS - started))s; ${#unremoved[@]} of ${count} shard checkouts could not be removed by git worktree remove (named above)."
        return 0
    fi
    echo "pre-push guard: gate 36 passed as ${count} local shards in $((SECONDS - started))s; the shard checkouts were removed."
}

if [ "${fast_path}" -eq 1 ]; then
    echo "=== pre-push guard FAST PATH: every changed path is site-only, so tools/run_all_audits.sh runs here without the linter regression suite (gate 36), which is left to CI; the full suite still runs in CI before merge. Changed paths (${#changed_paths[@]}): ${changed_paths[*]} ==="
    fast_step "run-pr-time-checks.sh (delta + history-aware gates)" tools/run-pr-time-checks.sh
    echo ""
    echo "=== pre-push guard fast path: ${#fast_gates[@]} tools/run_all_audits.sh gates (all but gate 36) ==="
    gates_started=${SECONDS}
    for key in "${fast_gates[@]}"; do
        # The command's plain tokens split into an array at single spaces, with
        # no pathname expansion, and run as that array.
        read -r -a gate_words <<< "${key#*|}"
        audit_gate "pre-push guard fast path gate" "${key%%|*}" python3 "${gate_words[@]}"
    done
    echo "pre-push guard fast path: ${#fast_gates[@]} runner gates passed in $((SECONDS - gates_started))s."
    fast_step "palette gate (.baseline/check_palette.py, with .web/build.py's arguments)" \
        python3 -I .baseline/check_palette.py --site grclibrary --palettes .web/baseline/palettes.css
    fast_step ".web/build.py --check (web-generator health, from HEAD)" python3 .web/build.py --check
    fast_step "tests/test_web_draft.py (web draft tests)" python3 -B tests/test_web_draft.py
else
    echo "pre-push-guard: running the full guard (${full_reason})."

    if [ "${runner_gates_ok}" -eq 1 ]; then
        # Every runner gate but gate 36, in runner order, by the runner's own
        # name and command (the same reading the fast path uses), each with
        # the runner's advisory echo (audit_gate_echo, as run_gate echoes);
        # then gate 36 whole, as local shards (step 1b).
        echo "=== pre-push guard 1/3: tools/run_all_audits.sh gates (all but the linter regression suite, gate 36, which runs next as local shards) ==="
        gates_started=${SECONDS}
        for key in "${runner_gates[@]}"; do
            read -r -a gate_words <<< "${key#*|}"
            audit_gate_echo "pre-push guard gate" "${key%%|*}" python3 "${gate_words[@]}"
        done
        echo "pre-push guard: ${#runner_gates[@]} runner gates passed in $((SECONDS - gates_started))s."
        run_gate36_shards
    else
        # Fail closed: the gate list cannot be read, so run the whole runner,
        # gate 36 included; doubt never drops a check.
        echo "pre-push-guard: NOTE: the runner's gate list cannot be read (${runner_gates_reason}); failing closed to the whole runner, gate 36 included." >&2
        # Capture the runner's exit code from the BARE command, not from inside an
        # `if ! cmd` test: `rc=$?` after `if ! cmd; then` would capture the negated
        # status (0), making the guard exit 0 on failure. (improvement-log #439 HIGH:
        # the original `if ! cmd; then rc=$?` form exited 0 on a failing runner and
        # let `&& git push` proceed. set -u is on and the guard does not set -e, but
        # an inherited errexit (SHELLOPTS) is possible: it ends the guard at the
        # failing runner, before the report below, with that runner's rc, so the
        # exit code still reaches the caller.)
        echo "=== pre-push guard 1/3: run_all_audits.sh (corpus gates, from HEAD) ==="
        tools/run_all_audits.sh
        rc=$?
        if [ "${rc}" -ne 0 ]; then
            echo ""
            echo "pre-push guard FAILED at run_all_audits.sh (rc=${rc}). Fix the artefact; do not push."
            exit "${rc}"
        fi
    fi

    echo ""
    echo "=== pre-push guard 2/3: run-pr-time-checks.sh (delta + history-aware gates) ==="
    tools/run-pr-time-checks.sh
    rc=$?
    if [ "${rc}" -ne 0 ]; then
        echo ""
        echo "pre-push guard FAILED at run-pr-time-checks.sh (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi

    if [ -f .web/build.py ]; then
        echo ""
        echo "=== pre-push guard 3/3: .web/build.py --check (web-generator health, from HEAD) ==="
        python3 .web/build.py --check
        rc=$?
        if [ "${rc}" -ne 0 ]; then
            echo ""
            echo "pre-push guard FAILED at .web/build.py --check (rc=${rc}). Fix the generator or templates; do not push."
            exit "${rc}"
        fi
    else
        echo ""
        echo "=== pre-push guard 3/3: .web/build.py --check SKIPPED (.web/build.py absent; not applicable here) ==="
    fi
fi

# Advisory, never blocking: reference-acquisition manifest drift (P-TODO 3b62). The manifest
# lists every trusted-bucket entry in the grc_library_ref sibling, and its --check is not a CI
# gate (CI has no grc_library_ref), so a reference ingest leaves it stale until someone
# regenerates it. Failing here would force an unrelated PR to carry the regeneration, so the
# drift is reported, not blocked. The check no-ops (exit 0) when the sibling is absent.
echo ""
echo "=== pre-push guard advisory: build-reference-manifest.py --check (reference manifest vs grc_library_ref; does not block) ==="
# The status is captured inside an `if`, so an inherited errexit (SHELLOPTS) cannot end the guard
# here; drift is reported only for exit 1 together with the generator's DRIFT line (exit 1 alone
# could also be an interpreter-level failure).
if manifest_out=$(python3 tools/build-reference-manifest.py --check 2>&1); then rc=0; else rc=$?; fi
printf '%s\n' "${manifest_out}"
if [ "${rc}" -eq 1 ] && [[ "${manifest_out}" == *"--check: DRIFT"* ]]; then
    echo "pre-push guard ADVISORY: docs/reference-acquisition-manifest.md has drifted from grc_library_ref. Not blocking this push; regenerate it (python3 tools/build-reference-manifest.py) in its own PR next."
elif [ "${rc}" -ne 0 ]; then
    echo "pre-push guard ADVISORY: the reference-manifest check could not run (rc=${rc}; see its message above). Not blocking this push."
fi

echo ""
if [ "${fast_path}" -eq 1 ]; then
    echo "=== pre-push guard PASS (FAST PATH, site-only change, ${SECONDS}s): the site checks are green. Safe to push; the full suite runs in CI before merge. ==="
else
    echo "=== pre-push guard PASS: all applicable checks green. Safe to push. ==="
fi
exit 0
