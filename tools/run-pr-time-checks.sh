#!/usr/bin/env bash
#
# run-pr-time-checks.sh
#
# Wrapper that runs every PR-only delta gate locally against the current
# branch. The corpus-wide audit programme (tools/run_all_audits.sh)
# covers the 45 corpus gates that operate from HEAD; this wrapper
# covers the two PR-only delta gates plus gate 45 (TODO staleness),
# which behave like delta gates because their inputs include git
# history relative to the merge base.
#
# Usage:
#   tools/run-pr-time-checks.sh            # run against origin/main..HEAD
#   BASE_REF=origin/develop tools/run-pr-time-checks.sh
#
# Intended use: run BEFORE `git push -u origin <branch>` opens a PR, so
# the PR-time delta gates' diagnoses appear locally instead of after
# CI has flipped the check red. Pairs with `tools/run_all_audits.sh`:
# the corpus runner covers the 45 corpus gates; this wrapper covers
# the delta surface.
#
# Exit codes: 0 on all pass; first non-zero rc from any gate on
# failure (aggregation is not the goal here — these checks are fast and
# the maintainer wants to address them before push).

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

BASE_REF="${BASE_REF:-origin/main}"
HEAD_REF="${HEAD_REF:-HEAD}"

# Make sure the base ref exists locally. If origin/main has not been
# fetched yet this turn, fetch it once so the diff has something to
# compare against.
if ! git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
    echo "Base ref ${BASE_REF} not found locally; fetching..."
    git fetch origin --quiet
fi

BASE_SHA="$(git rev-parse "${BASE_REF}" 2>/dev/null || echo "${BASE_REF}")"
HEAD_SHA="$(git rev-parse "${HEAD_REF}" 2>/dev/null || echo "${HEAD_REF}")"

echo "PR-time checks: ${BASE_REF} (${BASE_SHA:0:8}) .. ${HEAD_REF} (${HEAD_SHA:0:8})"
echo ""

FAILED=0

run_check() {
    local name="$1"
    shift
    printf '%-58s ... ' "${name}"
    if "$@"; then
        echo "OK"
    else
        local rc=$?
        echo "FAIL (rc=${rc})"
        FAILED=$((FAILED + 1))
    fi
}

# Delta gate D1: CHANGELOG-on-PR check (dual-entry as of PR #125).
# The check scripts accept `base` and `head` as positional arguments.
run_check "D1 CHANGELOG-on-PR check" \
    python3 tools/check-changelog-on-pr.py "${BASE_REF}" "${HEAD_REF}"

# Delta gate D2: per-PR version-bump check.
run_check "D2 Per-PR version-bump check" \
    python3 tools/check-version-bump-on-pr.py "${BASE_REF}" "${HEAD_REF}"

# Gate 45: TODO staleness audit. Behaves like a delta gate because its
# inputs (git log of merged-PR commit subjects, .working/validate-sweeps/
# history.md) include history relative to the working state of TODO.md.
run_check "Gate 45 TODO staleness audit" \
    python3 tools/lint-todo-staleness.py

echo ""
if [ "${FAILED}" -eq 0 ]; then
    echo "All PR-time checks passed."
    exit 0
else
    echo "${FAILED} PR-time check(s) failed."
    exit 1
fi
