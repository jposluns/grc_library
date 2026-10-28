#!/usr/bin/env bash
# quick-guard.sh - a FAST local ITERATION aid, NOT the push gate (3.137a (closing PR #1245)).
#
# Runs the "fast-ready" gates while iterating, in two groups: per-file-sound
# gates on ONLY the changed .md files, plus a few FIXED-TARGET gates (matrix /
# CHANGELOG) in default mode (they validate one specific file, so feeding them
# an arbitrary changed doc would spuriously FAIL, Sweep-133), so a developer
# gets a quick sound subset-check. It NEVER prints "safe to push" and MUST NOT be the left side of
# `&& git push`. The full 109-gate tools/pre-push-guard.sh remains the AUTHORITY
# and still runs once before every push; it catches everything this omits.
#
# Residual NOT covered here (run the full guard to catch these): the
# register/edge-guarded gates (a change to a central register can false-clean a
# changed-only scan), and the ~29 corpus-wide gates (counts, parity, generator
# sync, history-aware, cross-file consistency) that cannot be soundly scoped to
# changed files at all.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

# --- changed-.md detection: union of (committed since merge-base with
# origin/main) + (working tree vs HEAD) + (untracked), minus deletions. ---
# NOTE: if origin/main is absent, MB falls back to HEAD, so this reduces to a
# working-tree-vs-HEAD diff and misses .md already COMMITTED on the branch. That is
# a graceful degradation for an iteration aid, and it is announced; the full
# pre-push-guard.sh (which runs the history-aware gates against the real merge
# base) is unaffected. Any OTHER git failure exits 2 rather than reading as "no
# changed files" (3b551). A repository with no commits (an unborn HEAD) refuses
# too, before origin/main is read: every listing diffs against HEAD or a merge
# base with it, and rev-parse cannot tell an unborn HEAD from one git cannot read,
# so it is not treated as having no prior state (3b647). --quiet hides git's own report
# for some of these failures (for example an unborn HEAD, a garbage or unreadable ref, or
# a tag naming a missing commit) and not for others (for example dubious ownership, a bad
# config or a corrupt object), whose report appears above the refusal; either way the
# guard refuses with exit 2.
git_failed() {
  echo "quick-guard: ERROR: $1 failed; the changed .md files cannot be listed, so nothing was checked." >&2
  echo "(This is an iteration aid; tools/pre-push-guard.sh is still required before push.)" >&2
  exit 2
}
# origin/main is read by its full name with show-ref --verify, which reads that one
# name: rev-parse's short-name lookup also tries refs/heads/<name> and the other DWIM
# names, so a local branch origin/main stood in for it; given the full name, rev-parse
# still tries refs/heads/refs/remotes/origin/main, so only show-ref's exact read counts.
# show-ref fails on a ref that does not exist, and also on one git skips: with an error
# (a ref naming a missing object) or silently (a malformed loose ref, a dangling loose
# symlink or symbolic ref, a malformed or unsorted packed-refs line, a loose file
# shadowing a packed ref, a ref directory git cannot read). So origin/main is absent
# only when symbolic-ref -q exits 1 (128 is a ref git cannot read or parse, such as one
# under a mode-000 directory; 0 is a symbolic ref show-ref could not follow), show-ref
# --verify --quiet exits 1 and prints nothing, for-each-ref (which reads every record)
# exits 0, prints nothing to stderr and does not list it, and its loose path holds
# nothing or a plain directory (a remote branch main/x keeps refs/remotes/origin/main/),
# as lint-library-version-monotonicity.py reads it, except that it follows a symbolic ref.
ORIGIN_MAIN=refs/remotes/origin/main
origin_main_absent() {
  local said listed loose
  git symbolic-ref -q "$ORIGIN_MAIN" >/dev/null 2>&1
  [ $? -eq 1 ] || return 1
  said="$(git show-ref --verify --quiet "$ORIGIN_MAIN" 2>&1)"
  [ $? -eq 1 ] && [ -z "$said" ] || return 1
  said="$(git for-each-ref --format='%(refname)' 2>&1 >/dev/null)" && [ -z "$said" ] || return 1
  listed="$(git for-each-ref --format='%(refname)')" || return 1
  case $'\n'"$listed"$'\n' in *$'\n'"$ORIGIN_MAIN"$'\n'*) return 1 ;; esac
  loose="$(git rev-parse --git-path "$ORIGIN_MAIN")" || return 1
  if [ -e "$loose" ] || [ -L "$loose" ]; then
    [ -d "$loose" ] && [ ! -L "$loose" ] || return 1
  fi
}
git rev-parse --verify --quiet 'HEAD^{commit}' >/dev/null ||
  git_failed "git rev-parse --verify --quiet HEAD^{commit} (HEAD names no commit: a repository with no commits yet, or a HEAD git cannot read)"
if base="$(git show-ref --verify --hash "$ORIGIN_MAIN" 2>/dev/null)"; then
  MB="$(git merge-base HEAD "$base")" || git_failed "git merge-base HEAD $ORIGIN_MAIN"
elif ! origin_main_absent; then
  git_failed "git show-ref --verify $ORIGIN_MAIN (git cannot read it, or holds a record of it that it skips)"
else
  echo "quick-guard: NOTE: origin/main is absent; checking only uncommitted and untracked .md changes."
  MB=HEAD
fi
since_mb="$(git diff --name-only --diff-filter=d "$MB" -- '*.md')" || git_failed "git diff $MB"
since_head="$(git diff --name-only --diff-filter=d HEAD -- '*.md')" || git_failed "git diff HEAD"
untracked="$(git ls-files --others --exclude-standard -- '*.md')" || git_failed "git ls-files --others"
# Restrict to CORPUS-CONTENT .md: files under an audited domain directory, minus
# the guardrails/ pack subtree and README.md files. The fast-ready
# gates scope to exactly this set in their default (no-argument) run, so passing
# a non-corpus .md (a root file like TODO.md/CHANGELOG.md, a .claude/ file, docs/,
# tools/, tests/, .github/, .web/, or a pack file) that the gate would EXEMPT in
# default mode would make the gate process it explicitly and spuriously FAIL. Such
# files are checked only by the full tools/pre-push-guard.sh, never by this aid.
mapfile -t CHANGED < <(
  printf '%s\n' "$since_mb" "$since_head" "$untracked" | sort -u | grep -E '^(ai|architecture|compliance|crypto|dev-security|governance|\.project-governance|operations|privacy|resilience|risk|security|supply-chain)/' | grep -vE '(^|/)README\.md$'
)

if [ "${#CHANGED[@]}" -eq 0 ]; then
  echo "quick-guard: no changed corpus-content .md files to fast-check."
  echo "(This is an iteration aid; tools/pre-push-guard.sh is still required before push.)"
  exit 0
fi

echo "quick-guard: fast-checking ${#CHANGED[@]} changed .md file(s) against the fast-ready gates."
echo "NOTE: ITERATION AID ONLY, not the push gate. Run tools/pre-push-guard.sh before pushing;"
echo "it runs all 109 gates incl. the register-guarded and corpus-wide ones this omits."
echo "------------------------------------------------------------"

# The fast-ready gates, in two groups:
#  - CHANGED-FILE gates (FAST_TOOLS): per-file-sound, so they run on ONLY the
#    changed .md files. Includes the two refactored gates (check-review-cadence
#    = gate 10, lint-skill-internal-refs = gate 76). All accept a uniform
#    positional list of .md paths (3.137a (closing PR #1245)).
#  - FIXED-TARGET gates (FAST_FIXED_TARGET): each validates ONE specific file
#    (the compliance matrix / CHANGELOG.md). Feeding them an arbitrary changed
#    doc makes them mis-validate it AS that file and spuriously FAIL (Sweep-133
#    finding), so they run in DEFAULT (no-arg) mode and always check their own
#    correct target.
FAST_TOOLS=(
  lint-metadata.py lint-language.py lint-citations.py lint-filename-title-alignment.py
  lint-shall-near-uncertainty.py lint-placeholder-leakage.py
  lint-date-format.py lint-license-consistency.py lint-stub-documents.py lint-intra-doc-refs.py
  lint-required-sections.py lint-secrets-in-content.py lint-pii-in-content.py
  lint-internal-references.py lint-external-link-domains.py lint-metadata-line-breaks.py
  lint-document-date-staleness.py lint-section-placement.py lint-version-bump-recency.py
  lint-followup-ageing.py lint-ccm-aicm-citations.py
  lint-working-prose-hygiene.py lint-directional-dependency.py lint-document-control-codes.py
  lint-bare-normative-shall.py lint-todo-marked-done.py lint-document-iso-annex-a.py
  lint-cobit-iso31000-citations.py lint-unbalanced-fences.py lint-nested-markdown-links.py
  lint-positional-backlog-tokens.py lint-cobit-title-text.py
  check-review-cadence.py lint-skill-internal-refs.py
)
FAST_FIXED_TARGET=(
  lint-changelog-link-coverage.py lint-matrix-control-codes.py
)

FAILED=()
for tool in "${FAST_TOOLS[@]}"; do
  # 3b50b2c: "--" ends option parsing, so a changed file whose name begins with "-" is read as
  # a path; every FAST_TOOL accepts it (QuickGuardSeparatorTests keeps that true).
  out="$(python3 "tools/$tool" -- "${CHANGED[@]}" 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    FAILED+=("$tool")
    echo "[FAIL rc=$rc] $tool"
    echo "$out"
  fi
done
# Fixed-target gates run WITHOUT the changed-file args (default single target).
for tool in "${FAST_FIXED_TARGET[@]}"; do
  out="$(python3 "tools/$tool" 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    FAILED+=("$tool")
    echo "[FAIL rc=$rc] $tool (fixed-target, default-mode run)"
    echo "$out"
  fi
done

echo "------------------------------------------------------------"
if [ "${#FAILED[@]}" -gt 0 ]; then
  echo "quick-guard: ${#FAILED[@]} fast-ready gate(s) FAILED: ${FAILED[*]}"
  echo "Fix them, then run the FULL tools/pre-push-guard.sh before pushing."
  exit 1
fi
echo "quick-guard: all $(( ${#FAST_TOOLS[@]} + ${#FAST_FIXED_TARGET[@]} )) fast-ready gates passed (${#FAST_TOOLS[@]} on changed files, ${#FAST_FIXED_TARGET[@]} fixed-target in default mode)."
echo "This is NOT a green light to push. Run tools/pre-push-guard.sh (the authority) first."
exit 0
