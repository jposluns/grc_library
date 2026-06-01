#!/usr/bin/env bash
#
# run_all_audits.sh
#
# Single-command audit runner. Executes every linter and generator-check
# that is also wired into .github/workflows/quality.yml, in the same order
# the CI workflow runs them. Exits non-zero on the first failure (FAIL_FAST
# mode) or aggregates all failures (default).
#
# Usage:
#   tools/run_all_audits.sh            # run all gates, aggregate failures
#   FAIL_FAST=1 tools/run_all_audits.sh  # stop on first failure
#
# Rationale (see TODO.md Decisions log, Phase 23.30): phase-completion
# gating requires the full audit sweep to pass locally before any push.
# This script provides a single deterministic invocation for that sweep.
# The current sweep is 33 gates; see governance/specification-audit-programme.md
# section 6 for the canonical inventory.
#
# Keep this list in lock-step with .github/workflows/quality.yml. If a new
# audit is added to the CI workflow, add the same step here. The
# specification-audit-programme.md document defines the authoritative
# audit-programme architecture.

set -u

# Resolve repository root from the script's own location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

FAIL_FAST="${FAIL_FAST:-0}"
TOTAL=0
FAILED=0
FAILED_LIST=()

# A single audit step. Args: <human-name> <command...>
run_gate() {
    local name="$1"
    shift
    TOTAL=$((TOTAL + 1))
    printf '[%2d] %-58s ... ' "${TOTAL}" "${name}"
    local output
    output="$("$@" 2>&1)"
    local rc=$?
    if [ ${rc} -eq 0 ]; then
        echo "OK"
    else
        echo "FAIL (rc=${rc})"
        echo "${output}" | sed 's/^/      /'
        FAILED=$((FAILED + 1))
        FAILED_LIST+=("${name}")
        if [ "${FAIL_FAST}" = "1" ]; then
            echo ""
            echo "FAIL_FAST=1: stopping on first failure."
            exit ${rc}
        fi
    fi
}

echo "Running full audit programme (${REPO_ROOT})"
echo ""

# ----------------------------------------------------------------------
# Markdown linters (29 gates). Order mirrors quality.yml.
# ----------------------------------------------------------------------
run_gate "Metadata audit"                                python3 tools/lint-metadata.py
run_gate "Language and style audit"                      python3 tools/lint-language.py
run_gate "Repository-internal link audit"                python3 tools/lint-links.py
run_gate "Structural index integrity audit"              python3 tools/lint-structure.py
run_gate "Framework citation hallucination audit"        python3 tools/lint-citations.py
run_gate "Standards-currency audit"                      python3 tools/lint-standards-currency.py
run_gate "Filename and Document Title alignment audit"   python3 tools/lint-filename-title-alignment.py
run_gate "Owner and Approving Authority role audit"      python3 tools/lint-roles.py
run_gate "Mandatory requirement near uncertainty marker audit" python3 tools/lint-shall-near-uncertainty.py
run_gate "Per-document review cadence audit"             python3 tools/check-review-cadence.py
run_gate "CHANGELOG file-reference link coverage"        python3 tools/lint-changelog-link-coverage.py
run_gate "Placeholder leakage audit"                     python3 tools/lint-placeholder-leakage.py
run_gate "Library and document version monotonicity audit" python3 tools/lint-library-version-monotonicity.py
run_gate "Metadata date format audit"                    python3 tools/lint-date-format.py
run_gate "License consistency audit"                     python3 tools/lint-license-consistency.py
run_gate "Stub document audit"                           python3 tools/lint-stub-documents.py
run_gate "Section anchor reference audit"                python3 tools/lint-section-anchors.py
run_gate "Intra-document section reference audit"        python3 tools/lint-intra-doc-refs.py
run_gate "Required sections audit"                       python3 tools/lint-required-sections.py
run_gate "Acronym expansion consistency audit"           python3 tools/lint-acronym-consistency.py
run_gate "Secret pattern audit"                          python3 tools/lint-secrets-in-content.py
run_gate "PII pattern audit"                             python3 tools/lint-pii-in-content.py
run_gate "Internal references audit"                     python3 tools/lint-internal-references.py
run_gate "External link domain audit"                    python3 tools/lint-external-link-domains.py
run_gate "Cross-document numerical coherence audit"      python3 tools/lint-cross-doc-numbers.py
run_gate "Orphan document audit"                         python3 tools/lint-orphan-documents.py
run_gate "Citation verification freshness audit"         python3 tools/lint-citation-verification-freshness.py
run_gate "Tooling provenance freshness audit"            python3 tools/lint-tooling-provenance-freshness.py
run_gate "Version-date consistency audit"                python3 tools/lint-version-date-consistency.py

# ----------------------------------------------------------------------
# Generator-output drift gates (2 gates). These ensure that the auto-
# generated taxonomy.yml / portal.md / maturity-scorecard.md are in sync
# with the canonical metadata blocks they derive from.
# ----------------------------------------------------------------------
run_gate "Machine-readable taxonomy in sync"             python3 tools/build-taxonomy.py --check
run_gate "Adopter portal and maturity scorecard in sync" python3 tools/build-portal.py --check

# ----------------------------------------------------------------------
# Self-parity gate (1 gate). Validates that the audit programme's four
# surfaces (spec inventory, workflow, this runner, pre-commit hook) all
# declare the same gates with the same names and scripts in the same
# order. See governance/specification-audit-programme.md section 3
# principle 5 for the CI-parity rule this gate enforces.
# ----------------------------------------------------------------------
run_gate "Gate-name parity audit"                        python3 tools/lint-audit-gate-parity.py

# ----------------------------------------------------------------------
# Linter regression test suite (1 gate). Positive tests for each
# in-scope linter: each test constructs a synthetic markdown fixture
# that should trigger exactly one rule, invokes the linter, and asserts
# non-zero exit. See tests/README.md for scope and limits.
# ----------------------------------------------------------------------
run_gate "Linter regression test suite"                  python3 tools/run-linter-regression.py

# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------
echo ""
echo "------------------------------------------------------------"
if [ ${FAILED} -eq 0 ]; then
    echo "All ${TOTAL} audit gates passed."
    exit 0
else
    echo "${FAILED} of ${TOTAL} audit gate(s) failed:"
    for n in "${FAILED_LIST[@]}"; do
        echo "  - ${n}"
    done
    exit 1
fi
