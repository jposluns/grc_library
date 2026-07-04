#!/usr/bin/env bash
#
# pre-push-guard.sh
#
# The single pre-push QA gate. Run it (it must exit 0) immediately before
# a push, as one command:
#
#   tools/pre-push-guard.sh && git push -u origin <branch>
#
# It chains the two runners that PR-workflow step 1 mandates before any
# push, stopping on the first failure:
#
#   1. tools/run_all_audits.sh      — all corpus gates, from HEAD.
#   2. tools/run-pr-time-checks.sh  — the PR-only delta gates (D1-D7) plus
#                                     the history-aware trio (gates 45/40/31)
#                                     against the merge base.
#
# Together those two runners cover every gate the CI workflow runs, so a
# green guard means the push will not flip CI red on a gate failure.
#
# Why a standalone &&-gated guard rather than a git pre-push hook: git
# hooks do not fire in this execution environment (the same reason
# `preflight-changelog.py` is run as `python3 ... && git commit` rather
# than from a pre-commit hook). An &&-chained helper is therefore what
# actually enforces the discipline here. The guard closes the
# momentum-bypass gap where an "intermediate" push skipped the runner and
# a delta gate flipped CI red after the fact (improvement-log #438).
#
# Scope boundary: this guard gates PUSHES (the two post-commit / pre-push
# runners). The commit-time hygiene gate, `preflight-changelog.py`, stays
# the `&&`-gate on COMMITS (`python3 tools/preflight-changelog.py && git
# commit ...`), because it inspects newly-added working-tree lines that
# are already committed by push time. The two helpers are complementary,
# not redundant.
#
# Usage:
#   tools/pre-push-guard.sh && git push -u origin <branch>
#   BASE_REF=origin/develop tools/pre-push-guard.sh   # non-default base
#
# Exit codes: 0 only if BOTH runners pass; 3 if the guard REFUSES to run
# because stdout is piped (the RM-10 self-defence below, before any runner
# starts); otherwise the first failing runner's non-zero rc (that runner's
# own diagnostics are printed above).

set -u

# RM-10 pipe self-defence (TODO section 1.9(b), maintainer-approved
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

# Best-effort refresh of the merge base so the delta gates in
# run-pr-time-checks.sh compare against the true base ref (origin/main by
# default; whatever BASE_REF names otherwise). Fetching all of origin keeps
# the refresh correct under a BASE_REF override. Offline is tolerated:
# run-pr-time-checks.sh falls back to whatever base ref exists locally, and a
# stale base only risks a false PASS on the delta gates, which CI then catches.
git fetch origin --quiet 2>/dev/null || true

# Capture each runner's exit code from the BARE command, not from inside an
# `if ! cmd` test: `rc=$?` after `if ! cmd; then` would capture the negated
# status (0), making the guard exit 0 on failure. (improvement-log #439 HIGH:
# the original `if ! cmd; then rc=$?` form exited 0 on a failing runner and
# let `&& git push` proceed. set -u is on, set -e is NOT, so a non-zero rc
# does not abort the script before we handle it.)
echo "=== pre-push guard 1/2: run_all_audits.sh (corpus gates, from HEAD) ==="
tools/run_all_audits.sh
rc=$?
if [ "${rc}" -ne 0 ]; then
    echo ""
    echo "pre-push guard FAILED at run_all_audits.sh (rc=${rc}). Fix the artefact; do not push."
    exit "${rc}"
fi

echo ""
echo "=== pre-push guard 2/2: run-pr-time-checks.sh (delta + history-aware gates) ==="
tools/run-pr-time-checks.sh
rc=$?
if [ "${rc}" -ne 0 ]; then
    echo ""
    echo "pre-push guard FAILED at run-pr-time-checks.sh (rc=${rc}). Fix the artefact; do not push."
    exit "${rc}"
fi

echo ""
echo "=== pre-push guard PASS: both runners green. Safe to push. ==="
exit 0
