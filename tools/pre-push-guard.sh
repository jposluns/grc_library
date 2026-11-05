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
#      links to this clone's own siblings (the private store
#      <repo-parent>/private, grc_library_private, grc_library_ref), and a
#      relative GRC_STORE is made absolute, so the store is reachable as it
#      is for the serial run. Each shard's output goes to its own log file,
#      its step outputs to its own GITHUB_OUTPUT file, and its exit status
#      is read directly from wait. tools/reconcile-regression-shards.py
#      --shard-outputs then reconciles the six (every shard succeeded, all
#      six discovered one unit set, every module earned a credited start).
#      Any shard failure, a missing shard, or a reconcile failure fails the
#      push, keeping the checkouts and printing their paths; a passing run
#      removes every temporary checkout and shard directory. On the
#      fail-closed whole-runner fallback below gate 36 has just run
#      serially, so this step does not run again.
#   2. tools/run-pr-time-checks.sh  - the per-PR D-numbered delta gates (D6 retired) plus
#                                     the history-aware trio (gates 45/40/31) against
#                                     the merge base.
#   3. .web/build.py --check         - web-generator health (parse + render, no write).
#
# It then prints one ADVISORY that never blocks: build-reference-manifest.py --check
# (reference-manifest drift against the grc_library_ref sibling; P-TODO 3b62).
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
#   itself and runs each but gate 36 gate by gate on BOTH paths, then, on the
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
# (the attestation-soundness check below); 1 when a local gate 36 shard fails or
# the shard reconcile fails, 2 when the shard run cannot be set up or a shard is
# missing; otherwise the first failing blocking check's non-zero rc (that check's
# own diagnostics are printed above).

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
# directories, so a failure can keep and print them.
shard_root=""
shard_dirs=()

# A failed local shard run: keep every checkout and log, print where they
# are, and exit with rc.
shard_fail() {
    local rc="$1" message="$2" i
    echo ""
    echo "pre-push guard FAILED at gate 36 local shards (rc=${rc}): ${message}."
    if [ -n "${shard_root}" ]; then
        echo "The shard checkouts and logs are kept for inspection under ${shard_root}:"
        for i in "${!shard_dirs[@]}"; do
            echo "  shard ${i}: ${shard_dirs[i]} (checkout ${shard_dirs[i]}/${REPO_NAME}, log ${shard_dirs[i]}/shard.log)"
        done
        echo "Once inspected, remove each checkout with git worktree remove --force <checkout>, then the directory."
    fi
    echo "Fix the artefact; do not push."
    exit "${rc}"
}

run_gate36_shards() {
    local count="${REGRESSION_SHARD_COUNT}" commit parent store i dir tree rc started
    local sibling ran verdict first_rc=0 failed="" reconcile_rc
    local -a pids=() statuses=() pairs=()
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
        for sibling in "${REGRESSION_SHARD_SIBLINGS[@]}"; do
            if [ -e "${parent}/${sibling}" ] || [ -L "${parent}/${sibling}" ]; then
                if ! ln -s "${parent}/${sibling}" "${dir}/${sibling}"; then
                    shard_fail 2 "cannot link ${dir}/${sibling} to ${parent}/${sibling}"
                fi
            fi
        done
    done
    # Each shard runs its own checkout's runner, from that checkout, with its
    # own GITHUB_OUTPUT file and log; Git's repository variables are cleared
    # so a git command in a test reads the shard's checkout.
    for ((i = 1; i <= count; i++)); do
        (
            cd "${shard_dirs[i]}/${REPO_NAME}" || exit 2
            unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_PREFIX
            if [ -n "${store}" ]; then
                export GRC_STORE="${store}"
            fi
            export GITHUB_OUTPUT="${shard_dirs[i]}/github-output"
            exec python3 tools/run-linter-regression.py --shard "${i}/${count}"
        ) > "${shard_dirs[i]}/shard.log" 2>&1 &
        pids[i]=$!
    done
    # Each exit status is read directly from wait, inside an `if` that keeps
    # it, so an inherited errexit cannot end the guard before the report.
    for ((i = 1; i <= count; i++)); do
        if wait "${pids[i]}"; then rc=0; else rc=$?; fi
        statuses[i]="${rc}"
        ran="$(grep -E '^Ran [0-9]+ tests? in ' "${shard_dirs[i]}/shard.log" | tail -n 1 || true)"
        verdict="$(grep -E '^(OK|FAILED)( \(.*\))?$' "${shard_dirs[i]}/shard.log" | tail -n 1 || true)"
        echo "gate 36 local shard ${i}/${count}: rc=${rc}; ${ran:-no Ran line}; ${verdict:-no result line} (log ${shard_dirs[i]}/shard.log)"
        if [ "${rc}" -ne 0 ]; then
            failed="${failed:+${failed}, }${i}"
            [ "${first_rc}" -ne 0 ] || first_rc="${rc}"
        fi
    done
    if [ "${#statuses[@]}" -ne "${count}" ]; then
        shard_fail 2 "${#statuses[@]} of ${count} shards reported a status, so a shard is missing"
    fi
    for ((i = 1; i <= count; i++)); do
        if [ "${statuses[i]}" -ne 0 ]; then
            echo ""
            echo "--- gate 36 local shard ${i}/${count} failed (rc=${statuses[i]}); the last 60 lines of ${shard_dirs[i]}/shard.log:"
            tail -n 60 "${shard_dirs[i]}/shard.log"
        fi
        pairs+=("${statuses[i]}" "${shard_dirs[i]}/github-output")
    done
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
    # A passing run removes every temporary checkout, then the shard directory.
    for ((i = 1; i <= count; i++)); do
        if ! git worktree remove --force "${shard_dirs[i]}/${REPO_NAME}" > /dev/null 2>&1; then
            echo "pre-push guard: WARNING: could not remove the shard checkout ${shard_dirs[i]}/${REPO_NAME}; remove it with git worktree remove --force." >&2
        fi
    done
    if ! python3 -I -c 'import shutil, sys; shutil.rmtree(sys.argv[1])' "${shard_root}"; then
        echo "pre-push guard: WARNING: could not remove the shard directory ${shard_root}." >&2
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
