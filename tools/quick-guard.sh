#!/usr/bin/env bash
# quick-guard.sh - a FAST local ITERATION aid, NOT the push gate (TODO 3.137a).
#
# Runs the "fast-ready" gates (path-arg-aware AND per-file-sound) on ONLY the
# changed .md files, so a developer gets a quick sound subset-check while
# iterating. It NEVER prints "safe to push" and MUST NOT be the left side of
# `&& git push`. The full 78-gate tools/pre-push-guard.sh remains the AUTHORITY
# and still runs once before every push; it catches everything this omits.
#
# Residual NOT covered here (run the full guard to catch these): the
# register/edge-guarded gates (a change to a central register can false-clean a
# changed-only scan), and the ~28 corpus-wide gates (counts, parity, generator
# sync, history-aware, cross-file consistency) that cannot be soundly scoped to
# changed files at all.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

# --- changed-.md detection: union of (committed since merge-base with
# origin/main) + (working tree vs HEAD) + (untracked), minus deletions. ---
# NOTE: if origin/main is absent, MB falls back to HEAD, so this reduces to a
# working-tree-vs-HEAD diff and misses .md already COMMITTED on the branch. That is
# a graceful degradation for an iteration aid; the full pre-push-guard.sh (which
# runs the history-aware gates against the real merge base) is unaffected.
MB="$(git merge-base HEAD origin/main 2>/dev/null || echo HEAD)"
# Restrict to CORPUS-CONTENT .md: files under an audited domain directory, minus
# the dev-security/claude-rules/ pack subtree and README.md files. The fast-ready
# gates scope to exactly this set in their default (no-argument) run, so passing
# a non-corpus .md (a root file like TODO.md/CHANGELOG.md, a .claude/ file, docs/,
# tools/, tests/, .github/, .web/, or a pack file) that the gate would EXEMPT in
# default mode would make the gate process it explicitly and spuriously FAIL. Such
# files are checked only by the full tools/pre-push-guard.sh, never by this aid.
mapfile -t CHANGED < <(
  {
    git diff --name-only --diff-filter=d "$MB" -- '*.md' 2>/dev/null
    git diff --name-only --diff-filter=d HEAD -- '*.md' 2>/dev/null
    git ls-files --others --exclude-standard -- '*.md' 2>/dev/null
  } | sort -u | grep -E '^(ai|architecture|compliance|dev-security|governance|\.project-governance|operations|privacy|resilience|risk|security|supply-chain)/' | grep -vE '^dev-security/claude-rules/' | grep -vE '(^|/)README\.md$'
)

if [ "${#CHANGED[@]}" -eq 0 ]; then
  echo "quick-guard: no changed corpus-content .md files to fast-check."
  echo "(This is an iteration aid; tools/pre-push-guard.sh is still required before push.)"
  exit 0
fi

echo "quick-guard: fast-checking ${#CHANGED[@]} changed .md file(s) against the fast-ready gates."
echo "NOTE: ITERATION AID ONLY, not the push gate. Run tools/pre-push-guard.sh before pushing;"
echo "it runs all 78 gates incl. the register-guarded and corpus-wide ones this omits."
echo "------------------------------------------------------------"

# The 34 fast-ready gates + the two refactored ones (check-review-cadence = gate
# 10, lint-skill-internal-refs = gate 76), all normalized to accept a uniform
# positional list of .md paths (TODO 3.137a).
FAST_TOOLS=(
  lint-metadata.py lint-language.py lint-citations.py lint-filename-title-alignment.py
  lint-shall-near-uncertainty.py lint-changelog-link-coverage.py lint-placeholder-leakage.py
  lint-date-format.py lint-license-consistency.py lint-stub-documents.py lint-intra-doc-refs.py
  lint-required-sections.py lint-secrets-in-content.py lint-pii-in-content.py
  lint-internal-references.py lint-external-link-domains.py lint-metadata-line-breaks.py
  lint-document-date-staleness.py lint-section-placement.py lint-version-bump-recency.py
  lint-followup-ageing.py lint-ccm-aicm-citations.py lint-matrix-control-codes.py
  lint-working-prose-hygiene.py lint-directional-dependency.py lint-document-control-codes.py
  lint-bare-normative-shall.py lint-todo-marked-done.py lint-document-iso-annex-a.py
  lint-cobit-iso31000-citations.py lint-unbalanced-fences.py lint-nested-markdown-links.py
  lint-positional-backlog-tokens.py lint-cobit-title-text.py
  check-review-cadence.py lint-skill-internal-refs.py
)

FAILED=()
for tool in "${FAST_TOOLS[@]}"; do
  out="$(python3 "tools/$tool" "${CHANGED[@]}" 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    FAILED+=("$tool")
    echo "[FAIL rc=$rc] $tool"
    echo "$out"
  fi
done

echo "------------------------------------------------------------"
if [ "${#FAILED[@]}" -gt 0 ]; then
  echo "quick-guard: ${#FAILED[@]} fast-ready gate(s) FAILED on the changed files: ${FAILED[*]}"
  echo "Fix them, then run the FULL tools/pre-push-guard.sh before pushing."
  exit 1
fi
echo "quick-guard: all ${#FAST_TOOLS[@]} fast-ready gates passed on the changed files."
echo "This is NOT a green light to push. Run tools/pre-push-guard.sh (the authority) first."
exit 0
