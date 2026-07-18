#!/usr/bin/env bash
#
# Adopter-clone portability check (TODO sections 1.19.1 and 1.19.2).
#
# Guarantees the sibling-independence invariant: an adopter who clones ONLY the
# public grc_library repo (reaching no grc_library_ref / grc_library_scratch /
# grc_library_private sibling) can still run every audit gate green AND run the
# three §1.19.2-scoped advisory tools (ref-holds, audit-brief-freshness,
# audit-delivery-status) without a spurious error. The corpus' QA toolchain is
# PRODUCT (adopters clone and run it), so it must not depend on the maintainer's
# private sibling repos. All six maintainer-cadence tools that also reach
# grc_library_ref are now in the advisory-tool loop below (TODO section 3.91):
# audit-reference-breadth, audit-reference-acquisition-gaps, and
# scan-publication-instruction-content each raised on an absent reference base and were
# fixed to a graceful no-op exit 0, while audit-claim-precision, verify-reference-modules,
# and audit-register-currency already degraded (SKIP / advisory exit 0). SCOPE NOTE
# (TODO section 3.90): this check exercises
# the DEFAULT (relative) sibling-reach a bare adopter clone hits (a sibling absent
# beside the clone); a tool reaching an ABSOLUTE sibling path (e.g. a worker's
# /tmp/grc_library_ref) is out of this relative-clone model's scope and is covered by
# the tool's own explicit-path handling, not by this loop.
#
# How it works: git-clones this repo's current HEAD into a fresh temp directory that
# has NO sibling repos beside it, then (1) runs tools/run_all_audits.sh inside that
# clone and asserts it passes, and (2) runs each sibling-reaching advisory tool and
# asserts it degrades to a graceful exit 0 (TODO 1.19.2), not an error. If any gate or
# advisory tool reaches a sibling repo at runtime, the sibling is absent in the temp
# clone and the tool fails, so this check fails LOUD.
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

# Advisory-tool graceful-degradation (TODO section 1.19.2): the sibling-reaching
# advisory tools must no-op and exit 0 (not error) when their sibling repo is
# absent, so an adopter running them on a sibling-free clone gets a clean advisory
# rather than a spurious failure. ref-holds needs a query argument to reach the
# lookup path; the other two take none.
adv_rc=0
echo
echo "Checking the sibling-reaching advisory/generator tools degrade gracefully (TODO 1.19.2, 1.19.7) ..."
for tool in ref-holds.py audit-brief-freshness.py audit-delivery-status.py build-reference-manifest.py \
            audit-reference-breadth.py audit-claim-precision.py verify-reference-modules.py \
            audit-register-currency.py audit-reference-acquisition-gaps.py \
            scan-publication-instruction-content.py; do
  if [ "$tool" = "ref-holds.py" ]; then
    ( cd "$CLONE" && python3 "tools/$tool" probe-query >/dev/null 2>&1 )
  else
    ( cd "$CLONE" && python3 "tools/$tool" >/dev/null 2>&1 )
  fi
  trc=$?
  if [ "$trc" -eq 0 ]; then
    echo "  OK   tools/$tool exited 0 (graceful no-op)"
  else
    echo "  FAIL tools/$tool exited $trc without its sibling (should degrade to exit 0)"
    adv_rc=1
  fi
done

echo
if [ "$rc" -eq 0 ] && [ "$adv_rc" -eq 0 ]; then
  echo "PORTABILITY: PASS -- all audit gates green AND advisory tools degrade gracefully in a sibling-free clone; the corpus is adopter-portable."
  exit 0
else
  if [ "$rc" -ne 0 ]; then
    echo "PORTABILITY: FAIL (run_all_audits rc=$rc) -- a gate did not pass without the sibling repos."
    echo "A gate likely reaches grc_library_ref / grc_library_scratch / grc_library_private at runtime; fix it to use in-repo data (e.g. the in-repo reference modules), so an adopter clone stays green."
  fi
  if [ "$adv_rc" -ne 0 ]; then
    echo "PORTABILITY: FAIL -- a sibling-reaching advisory tool errored without its sibling; it should no-op and exit 0 per TODO section 1.19.2 (route its default sibling lookup through lint_common.resolve_sibling)."
  fi
  exit 1
fi
