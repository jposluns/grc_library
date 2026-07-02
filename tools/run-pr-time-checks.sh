#!/usr/bin/env bash
#
# run-pr-time-checks.sh
#
# Wrapper that runs the commit-graph-aware checks locally against the
# current branch, so their diagnoses appear before push instead of after
# CI has flipped the check red. Two groups:
#
#   1. The PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR
#      version-bump, D3 CHANGELOG-dash-on-PR, D4 per-PR Version-Date
#      co-bump, D5 backlog-rotation-on-PR). These compare the PR head
#      to its merge base, so their
#      inputs are not available in tools/run_all_audits.sh; they run
#      only here and in quality.yml.
#   2. The history-aware gates that examine each file's commit graph
#      (gate 45 TODO staleness, gate 40 version-bump-recency, gate 31
#      document-date-staleness). These ALSO run in run_all_audits.sh;
#      this wrapper re-invokes them so a single pre-push command is a
#      complete commit-graph-aware guard. That matters most for large
#      multi-commit or file-move changes (e.g. the governance Phase-1
#      migration), where the per-commit version-bump-recency and
#      date-staleness checks are easiest to confirm in one pre-push pass.
#
# Together with run_all_audits.sh (the corpus gates from HEAD), the two
# runners cover every gate the CI workflow runs. Gates 40, 31, and 45
# were folded in here per the design-decisions "Gate-family coherence
# (Option A)" decision.
#
# Usage:
#   tools/run-pr-time-checks.sh            # run against origin/main..HEAD
#   BASE_REF=origin/develop tools/run-pr-time-checks.sh
#
# Intended use: run BEFORE `git push -u origin <branch>` opens a PR, so
# the PR-time delta gates' diagnoses appear locally instead of after
# CI has flipped the check red. Pairs with `tools/run_all_audits.sh`:
# the corpus runner covers the corpus gates; this wrapper covers
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

# Delta gate D3: no em/en dashes in newly-added CHANGELOG.md lines (DD-1,
# new-entries-only; historical entries are exempt).
run_check "D3 CHANGELOG dash-on-PR check" \
    python3 tools/check-changelog-dash-on-pr.py "${BASE_REF}" "${HEAD_REF}"

# Delta gate D4: when a PR bumps a versioned document's Version, require
# the same change to co-bump its Date to the bump commit's date (the
# residue gates 31/40 leave open, scoped to the PR diff so historical
# carriers are never in scope).
run_check "D4 Per-PR Version-Date co-bump check" \
    python3 tools/check-date-cobump-on-pr.py "${BASE_REF}" "${HEAD_REF}"

# Delta gate D5: when a PR's added CHANGELOG lines assert a TODO-item
# closure ("clos... TODO §X"), require the same diff to rotate the item
# (touch TODO.md and .working/DONE.md). PR-time companion of gate 57
# (the static marked-done detector); catches the wholesale-forgotten
# rotation where TODO.md is never edited.
run_check "D5 Backlog-rotation-on-PR check" \
    python3 tools/check-todo-rotation-on-pr.py "${BASE_REF}" "${HEAD_REF}"

# Gate 45: TODO staleness audit. Behaves like a delta gate because its
# inputs (git log of merged-PR commit subjects, .working/validate-sweeps/
# history.md) include history relative to the working state of TODO.md.
run_check "Gate 45 TODO staleness audit" \
    python3 tools/lint-todo-staleness.py

# History-aware corpus gates 40 and 31. These also run in
# run_all_audits.sh; re-invoking them here makes the pre-push runner a
# complete commit-graph-aware guard (see the header comment). Each
# examines per-file commit history, so it operates from HEAD and needs
# no base ref.
run_check "Gate 40 version-bump-recency audit" \
    python3 tools/lint-version-bump-recency.py

run_check "Gate 31 document-date-staleness audit" \
    python3 tools/lint-document-date-staleness.py

echo ""
if [ "${FAILED}" -eq 0 ]; then
    echo "All PR-time checks passed."
    exit 0
else
    echo "${FAILED} PR-time check(s) failed."
    exit 1
fi
