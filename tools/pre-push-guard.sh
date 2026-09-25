#!/usr/bin/env bash
#
# pre-push-guard.sh
#
# The single pre-push QA gate. Run it (it must exit 0) immediately before
# a push, as one command:
#
#   tools/pre-push-guard.sh && git push -u origin <branch>
#
# It chains the two runners that PR-workflow step 2 mandates, plus a web-generator
# health check, before any push, stopping on the first failure:
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
# runners plus the conditional `.web/build.py --check`). The commit-time hygiene gate, `preflight-changelog.py`, stays
# the `&&`-gate on COMMITS (`python3 tools/preflight-changelog.py && git
# commit ...`), because it inspects newly-added working-tree lines that
# are already committed by push time. The two helpers are complementary,
# not redundant.
#
# Usage:
#   tools/pre-push-guard.sh && git push -u origin <branch>
#   BASE_REF=origin/develop tools/pre-push-guard.sh   # non-default base
#
# Exit codes: 0 only if both runners and the web check (when .web/build.py is present) pass; 3 if the guard REFUSES to run
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
      echo "pre-push-guard: REFUSING to push (1.19.8 (closing PR #1030) _private-required): origin is the maintainer repo but grc_library_private is absent or empty. It holds the operational state the CLAUDE.md delegation directive points to; clone it (git clone https://github.com/jposluns/grc_library_private.git ../grc_library_private) or grant access (--add-dir ../grc_library_private), then retry. An adopter clone is exempt." >&2
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
echo "=== pre-push guard PASS: all applicable checks green. Safe to push. ==="
exit 0
