#!/usr/bin/env bash
#
# Adopter-clone portability check (TODO section 1.19.1).
#
# Guarantees the sibling-independence invariant: an adopter who clones ONLY the
# public grc_library repo (reaching no grc_library_ref / grc_library_scratch /
# grc_library_private sibling) can still run every audit gate green. The corpus'
# QA toolchain is PRODUCT (adopters clone and run it), so it must not depend on the
# maintainer's private sibling repos.
#
# How it works: git-clones this repo's current HEAD into a fresh temp directory that
# has NO sibling repos beside it, then runs tools/run_all_audits.sh inside that clone
# and asserts it passes. If any gate reaches a sibling repo at runtime, the sibling is
# absent in the temp clone and the gate fails, so this check fails LOUD.
#
# This is the LOCAL reproduction of what CI already does implicitly (a GitHub Actions
# runner checks out grc_library alone, with no siblings), surfaced as an explicit,
# maintainer-runnable test. The maintainer's own working copy HAS the siblings, so a
# plain local `run_all_audits.sh` would NOT catch a newly-introduced sibling reach;
# this check does.
#
# It is deliberately NOT part of run_all_audits.sh (it would run the whole suite
# inside the suite) and NOT a per-PR gate (CI's sibling-free run already enforces the
# invariant on every PR). Run it on demand, or before a change that touches how a gate
# resolves paths.
#
# Exit codes: 0 = portable (all gates green with no siblings); 1 = a gate failed
# without siblings (likely a sibling reach); 2 = the check could not run (clone failed,
# or the temp dir was not sibling-free).

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HEAD_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null)" || { echo "PORTABILITY: cannot read HEAD of $REPO_ROOT"; exit 2; }

TMP="$(mktemp -d "${TMPDIR:-/tmp}/grc-portability.XXXXXX")" || { echo "PORTABILITY: cannot create temp dir"; exit 2; }
CLONE="$TMP/grc_library"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

echo "== Adopter-clone portability check (TODO 1.19.1) =="
echo "Cloning $REPO_ROOT @ ${HEAD_SHA:0:12} into a sibling-free temp dir ($TMP) ..."
git clone --quiet "$REPO_ROOT" "$CLONE" || { echo "PORTABILITY: git clone failed"; exit 2; }
git -C "$CLONE" checkout --quiet "$HEAD_SHA" || { echo "PORTABILITY: could not check out $HEAD_SHA in the clone"; exit 2; }

# Validate the test setup: the clone's parent must contain NO sibling repos, or the
# check is not actually testing sibling-independence (it would be vacuous).
for sib in grc_library_ref grc_library_scratch grc_library_private; do
  if [ -e "$TMP/$sib" ]; then
    echo "PORTABILITY: temp dir is not sibling-free ($TMP/$sib exists); check is invalid."
    exit 2
  fi
done

echo "Running tools/run_all_audits.sh in the sibling-free clone ..."
( cd "$CLONE" && tools/run_all_audits.sh )
rc=$?

echo
if [ "$rc" -eq 0 ]; then
  echo "PORTABILITY: PASS -- all audit gates green in a sibling-free clone; the corpus is adopter-portable."
  exit 0
else
  echo "PORTABILITY: FAIL (run_all_audits rc=$rc) -- a gate did not pass without the sibling repos."
  echo "A gate likely reaches grc_library_ref / grc_library_scratch / grc_library_private at runtime; fix it to use in-repo data (e.g. the in-repo reference modules), so an adopter clone stays green."
  exit 1
fi
