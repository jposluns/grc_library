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
# A push whose every changed path is site-only takes the FAST PATH described
# below; any other push runs the full guard. The full guard chains the two
# runners that PR-workflow step 4 mandates, plus a web-generator health check,
# before any push, stopping on the first failure:
#
#   1. tools/run_all_audits.sh      - all corpus gates, from HEAD.
#   2. tools/run-pr-time-checks.sh  - the per-PR D-numbered delta gates (D6 retired) plus
#                                     the history-aware trio (gates 45/40/31) against
#                                     the merge base.
#   3. .web/build.py --check         - web-generator health (parse + render, no write).
#
# It then prints one ADVISORY that never blocks: build-reference-manifest.py --check
# (reference-manifest drift against the grc_library_ref sibling; P-TODO 3b62).
#
# Together those two runners cover every gate the CI workflow runs, so a
# green full guard means the push will not flip CI red on a gate failure. A
# green fast path does not carry that promise (see its residual below).
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
#   parse; and when tools/run_all_audits.sh cannot be read, a run_gate line in
#   it cannot be parsed, or its linter regression suite gate is not there
#   exactly once by name and command. A run_gate line parses only as
#   run_gate "<name>" python3 <command>, where the name holds no ", $, `, \ or
#   | and the command is plain tokens of A-Z, a-z, 0-9 and _ . / = -, each
#   separated by one space, so the shell gives the runner the same words the
#   guard reads: a quoted argument, an expansion, a comment or a line
#   continuation makes the line unparseable.
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
#        a failing gate's output is printed in full; unlike the runner, no
#        advisory line is echoed from a passing gate (neither the DUE-SOON
#        lines the runner shows for every gate nor the WARN and NOTE lines it
#        shows for the gates that opt in), and the step stops at the first
#        failing gate. The step ends with its elapsed time.
#     3. The palette gate .baseline/check_palette.py, with the arguments
#        .web/build.py passes it but without .web/build.py's pin check (step 4
#        runs .web/build.py, which makes that check).
#     4. .web/build.py --check and python3 -B tests/test_web_draft.py.
#   It prints one FAST PATH line naming the changed paths, then the reference
#   manifest advisory, then a PASS line with the elapsed time.
#
#   The skip lives here alone (maintainer decision 2026-11-04 13:02Z, design
#   B): the guard lists the runner's gates itself and runs each but gate 36, so
#   tools/run_all_audits.sh takes no skip option or variable, and neither it
#   nor .github/workflows/quality.yml, which runs each gate, gate 36 included,
#   as its own step, is changed or can be told to skip a gate.
#
#   Skipped locally, disclosed as left to CI: gate 36 apart from
#   tests/test_web_draft.py (the rest of tests/test_linters.py and of the other
#   tests/test_*.py modules, and the completeness checks
#   tools/run-linter-regression.py makes), and the full guard's own
#   run_all_audits.sh summary. .github/workflows/quality.yml runs the full gate
#   set, gate 36 whole included, on every pull request (kept in lock-step with
#   run_all_audits.sh by the gate-parity gate), and tools/merge-when-green.py
#   merges only on green CI. This change alters neither.
#
#   Residual (what is lost): local detection, before the push, of a failure in
#   a gate 36 test that a site-only change causes (a test that reads a template,
#   a vendored .web/baseline/ file, .baseline/pin.toml or a root close-out
#   file); that failure now first shows in CI. A passing gate's DUE-SOON, WARN
#   and NOTE lines are not shown before the push either.
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
# Exit codes: 1 for an installed-hook check failure; 0 only if both runners and the web check (when .web/build.py is present) pass, or on the fast path only if every fast-path check passes; 3 if the guard REFUSES to run
# because stdout is piped (the RM-10 self-defence below, before any runner
# starts); 4 if grc_library_private is required but absent (the _private check
# below); 5 if the tracked working tree is dirty or its state cannot be read
# (the attestation-soundness check below); otherwise the first failing blocking check's
# non-zero rc (that check's own diagnostics are printed above).

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

# Sets fast_path to 1 when the push qualifies, filling changed_paths and
# fast_gates; otherwise returns with the reason in full_reason.
select_fast_path() {
    local hiding rc merge_base record_re header path shown ended=0 line name
    local call_re gate_re token key found=0
    local -a gates=()
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

    # The runner's gates, as "runner name|command" in runner order, read from its
    # run_gate lines. A line that starts with run_gate but does not match the one
    # shape the runner uses, an unreadable runner, or a gate 36 line missing or
    # repeated means the full guard. The name holds nothing the shell expands
    # inside double quotes, and the command is plain tokens separated by single
    # spaces (see the header), so the shell splits it exactly as the guard does.
    # The characters are listed one by one, not as ranges, so the match does
    # not depend on the locale.
    call_re='^[[:space:]]*run_gate([[:space:]]|$)'
    token='[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./=-]+'
    gate_re='^run_gate[[:space:]]+"([^"$`\|]+)"[[:space:]]+python3[[:space:]]+('"${token}"'( '"${token}"')*)[[:space:]]*$'
    if [ ! -f tools/run_all_audits.sh ] || [ ! -r tools/run_all_audits.sh ]; then
        full_reason="tools/run_all_audits.sh cannot be read, so the gates to run cannot be listed"
        return
    fi
    while IFS= read -r line || [ -n "${line}" ]; do
        [[ "${line}" =~ ${call_re} ]] || continue
        if ! [[ "${line}" =~ ${gate_re} ]]; then
            full_reason="the tools/run_all_audits.sh line '${line}' cannot be parsed, so the gates to run cannot be listed"
            return
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
        full_reason="tools/run_all_audits.sh has ${found} linter regression suite gate lines ('${REGRESSION_GATE%%|*}' running ${REGRESSION_GATE#*|}), not one, so the gate the fast path narrows cannot be named"
        return
    fi
    if [ "${#gates[@]}" -eq 0 ]; then
        full_reason="tools/run_all_audits.sh has no gate besides the linter regression suite"
        return
    fi
    fast_gates=("${gates[@]}")
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

# One fast-path audit gate: like tools/run_all_audits.sh, a passing gate's output
# stays hidden (its advisory lines are not echoed here) and a failing gate's
# output is printed in full before the guard exits with the gate's status. The
# status is captured inside an `if`, as in fast_step.
fast_gate() {
    local label="$1"
    shift
    local out rc
    printf '%-66s ... ' "pre-push guard fast path gate: ${label}"
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
        fast_gate "${key%%|*}" python3 "${gate_words[@]}"
    done
    echo "pre-push guard fast path: ${#fast_gates[@]} runner gates passed in $((SECONDS - gates_started))s."
    fast_step "palette gate (.baseline/check_palette.py, with .web/build.py's arguments)" \
        python3 -I .baseline/check_palette.py --site grclibrary --palettes .web/baseline/palettes.css
    fast_step ".web/build.py --check (web-generator health, from HEAD)" python3 .web/build.py --check
    fast_step "tests/test_web_draft.py (web draft tests)" python3 -B tests/test_web_draft.py
else
    echo "pre-push-guard: running the full guard (${full_reason})."

    # Capture each runner's exit code from the BARE command, not from inside an
    # `if ! cmd` test: `rc=$?` after `if ! cmd; then` would capture the negated
    # status (0), making the guard exit 0 on failure. (improvement-log #439 HIGH:
    # the original `if ! cmd; then rc=$?` form exited 0 on a failing runner and
    # let `&& git push` proceed. set -u is on, set -e is NOT, so a non-zero rc
    # does not abort the script before we handle it.)
    echo "=== pre-push guard 1/3: run_all_audits.sh (corpus gates, from HEAD) ==="
    tools/run_all_audits.sh
    rc=$?
    if [ "${rc}" -ne 0 ]; then
        echo ""
        echo "pre-push guard FAILED at run_all_audits.sh (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
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
