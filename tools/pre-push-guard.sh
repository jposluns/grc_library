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
#   2. tools/run-pr-time-checks.sh  — the PR-only delta gates (D1-D5) plus
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
# Exit codes: 0 only if BOTH runners pass; the first non-zero rc on
# failure (the failing runner's own diagnostics are printed above).

set -u

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
