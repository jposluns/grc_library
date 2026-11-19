#!/usr/bin/env bash
#
# run_all_audits.sh
#
# Single-command audit runner. Executes every section 6 linter and
# generator-check in section 6 order; .github/workflows/quality.yml runs
# only the section 4 CI subset of them. Exits non-zero on the first failure (FAIL_FAST
# mode) or aggregates all failures (default).
#
# Usage:
#   .claude/skills/corpus-management/tools/run_all_audits.sh            # run all gates, aggregate failures
#   FAIL_FAST=1 .claude/skills/corpus-management/tools/run_all_audits.sh  # stop on first failure
#
# Rationale: this script is the single deterministic invocation of the FULL
# sweep, every gate included. Since the gate 36 fast track (maintainer
# directives 2026-11-04 and 2026-11-05), a push no longer runs this script
# itself: the pre-push guard runs every gate here except the linter
# regression test suite (gate 36) one by one, then, on its full path, gate 36
# whole as six parallel local shards with the private store present (its
# site-only fast path leaves gate 36 to the local server run behind the
# local-quality commit status that merge requires), and it falls back to
# this whole script only when it cannot read the gate list. The nightly
# sweep and manual full runs still invoke this script whole, gate 36
# included.
# The current sweep covers the full corpus inventory; see
# .claude/skills/corpus-management/specs/specification-audit-programme.md section 6 for the
# canonical inventory and current gate count.
#
# This list must hold every section 6 gate, as .pre-commit-config.yaml
# does; .github/workflows/quality.yml holds only the CI subset. The
# specification-audit-programme.md document defines the authoritative
# audit-programme architecture.

set -u

# Resolve repository root from the script's own location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
cd "${REPO_ROOT}"

FAIL_FAST="${FAIL_FAST:-0}"
TOTAL=0
FAILED=0
FAILED_LIST=()

# GATE_INDEX maps each gate script to its canonical gate number, as
# " script=number " entries. The gate-name parity tool's own reader
# (parse_spec_inventory) builds it from the gate inventory in
# specification-audit-programme.md section 6. Retired numbers stay in that
# inventory as tombstone rows and are never reused, so a gate's position in
# this file is not its number. A script named by more than one live row is
# left out, and its gate shows [  ?], as every gate does when the inventory
# cannot be read. The numbers are for display: no exit status depends on them.
GATE_INDEX="$(python3 -I -c 'import collections, importlib.util, sys
spec = importlib.util.spec_from_file_location("gate_parity", sys.argv[1])
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)
rows = parity.parse_spec_inventory(parity.REPO_ROOT / parity.SPEC_PATH)
uses = collections.Counter(script for _, _, _, script in rows)
print("", *(f"{script}={number}" for _, number, _, script in rows if uses[script] == 1), "")' "${SCRIPT_DIR}/lint-audit-gate-parity.py")"

# A single audit step. Args: <human-name> <command...>
run_gate() {
    local name="$1"
    shift
    TOTAL=$((TOTAL + 1))
    # Show the canonical number of the gate script this step runs (see GATE_INDEX).
    local script="${2:-}" number="?"
    [ "${script}" = "-I" ] && script="${3:-}"
    case "${GATE_INDEX:-}" in
        *" ${script}="*)
            number="${GATE_INDEX#* "${script}"=}"
            number="${number%% *}"
            ;;
    esac
    printf '[%3s] %-58s ... ' "${number}" "${name}"
    local output
    # A new random token for this gate run, passed to the gate alone in
    # GRC_RUNNER_ECHO_TOKEN; see the marker below. Drawn from a CSPRNG (Python's
    # secrets module, which every gate already needs, else /dev/urandom). If both
    # fail the token stays empty, no gate opts in, and the run says so rather than
    # hiding advisory lines silently.
    local token
    token="$(python3 -c 'import secrets; print(secrets.token_hex(16))' 2>/dev/null)"
    [[ "${token}" =~ ^[0-9a-f]{32}$ ]] || token="$(od -An -N16 -tx1 /dev/urandom 2>/dev/null | tr -d ' \n')"
    [[ "${token}" =~ ^[0-9a-f]{32}$ ]] || token=""
    output="$(GRC_RUNNER_ECHO_TOKEN="${token}" "$@" 2>&1)"
    local rc=$?
    if [ ${rc} -eq 0 ]; then
        echo "OK"
        [ -n "${token}" ] || echo "      NOTE: no random source for the advisory-echo token; this gate's advisory WARN/NOTE lines are not shown"
        # A passing gate's output stays hidden, except advisory lines. Every gate
        # shows lines that start with DUE-SOON (gate 72's due-soon band), so a
        # lapse shows at resume. A gate whose output has the exact marker line
        # below, followed by a space and this run's token, also shows lines that
        # start with WARN or NOTE; only gates 6, 72 and 106 print it (RUNNER_ECHO_MARKER
        # in their scripts, printed only when GRC_RUNNER_ECHO_TOKEN is set), gate 6
        # for its UNPINNED and UNREGISTERED count line, gate 72 for its stale,
        # future-dated and untiered lines and gate 106 for its
        # low-headroom line. The key is a line the gate
        # declares in its own output, not its script path, so a rename, move or
        # other invocation path of the script cannot switch the echo off. The
        # token is the part data cannot forge: the marker text is public, and gate
        # 93 puts record IDs into its WARN lines unescaped, so a record ID holding
        # the marker alone would switch the echo on. With no token, no gate opts
        # in. It is opt-in per gate, not a generic WARN echo: gate 93 (relationship
        # model) passes while it prints hundreds of advisory WARN lines (382 on
        # 2026-09-30), which would bury gate 72's.
        local marker="runner-echo: .claude/skills/corpus-management/tools/run_all_audits.sh shows this gate's advisory lines on a pass"
        local advisory='^DUE-SOON'
        if [ -n "${token}" ] \
            && printf '%s\n' "${output}" | grep -xF -- "${marker} ${token}" >/dev/null; then
            advisory='^(DUE-SOON|WARN|NOTE)'
        fi
        printf '%s\n' "${output}" | grep -E "${advisory}" | sed 's/^/      /' || true
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
[ -n "${GATE_INDEX}" ] || echo "NOTE: the gate inventory could not be read, so no canonical gate number is shown"
echo ""

# ----------------------------------------------------------------------
# Markdown linters (sub-group of the corpus gates). Order follows section 6;
# quality.yml runs its CI subset in the same order.
# ----------------------------------------------------------------------
run_gate "Metadata audit"                                python3 .claude/skills/corpus-management/tools/lint-metadata.py
# Gate 2 checks the whole root .working/CHANGELOG.md through its default scope.
run_gate "Language and style audit"                      python3 .claude/skills/corpus-management/tools/lint-language.py
run_gate "Repository-internal link audit"                python3 .claude/skills/corpus-management/tools/lint-links.py
run_gate "Structural index integrity audit"              python3 .claude/skills/corpus-management/tools/lint-structure.py
run_gate "Framework citation hallucination audit"        python3 .claude/skills/corpus-management/tools/lint-citations.py
run_gate "Standards-currency audit"                      python3 .claude/skills/corpus-management/tools/lint-standards-currency.py
run_gate "Filename and Document Title alignment audit"   python3 .claude/skills/corpus-management/tools/lint-filename-title-alignment.py
run_gate "Owner and Approving Authority role audit"      python3 .claude/skills/corpus-management/tools/lint-roles.py
run_gate "Mandatory requirement near uncertainty marker audit" python3 .claude/skills/corpus-management/tools/lint-shall-near-uncertainty.py
run_gate "Per-document review cadence audit"             python3 .claude/skills/corpus-management/tools/check-review-cadence.py
run_gate "CHANGELOG file-reference link coverage"        python3 .claude/skills/corpus-management/tools/lint-changelog-link-coverage.py
run_gate "Placeholder leakage audit"                     python3 .claude/skills/corpus-management/tools/lint-placeholder-leakage.py
run_gate "Library and document version monotonicity audit" python3 .claude/skills/corpus-management/tools/lint-library-version-monotonicity.py
run_gate "Metadata date format audit"                    python3 .claude/skills/corpus-management/tools/lint-date-format.py
run_gate "License consistency audit"                     python3 .claude/skills/corpus-management/tools/lint-license-consistency.py
run_gate "Stub document audit"                           python3 .claude/skills/corpus-management/tools/lint-stub-documents.py
run_gate "Section anchor reference audit"                python3 .claude/skills/corpus-management/tools/lint-section-anchors.py
run_gate "Intra-document section reference audit"        python3 .claude/skills/corpus-management/tools/lint-intra-doc-refs.py
run_gate "Required sections audit"                       python3 .claude/skills/corpus-management/tools/lint-required-sections.py
run_gate "Acronym expansion consistency audit"           python3 .claude/skills/corpus-management/tools/lint-acronym-consistency.py
run_gate "Secret pattern audit"                          python3 .claude/skills/corpus-management/tools/lint-secrets-in-content.py
run_gate "PII pattern audit"                             python3 .claude/skills/corpus-management/tools/lint-pii-in-content.py
run_gate "Internal references audit"                     python3 .claude/skills/corpus-management/tools/lint-internal-references.py
run_gate "External link domain audit"                    python3 .claude/skills/corpus-management/tools/lint-external-link-domains.py
run_gate "Cross-document numerical coherence audit"      python3 .claude/skills/corpus-management/tools/lint-cross-doc-numbers.py
run_gate "Orphan document audit"                         python3 .claude/skills/corpus-management/tools/lint-orphan-documents.py
run_gate "Citation verification freshness audit"         python3 .claude/skills/corpus-management/tools/lint-citation-verification-freshness.py
run_gate "Tooling provenance freshness audit"            python3 .claude/skills/corpus-management/tools/lint-tooling-provenance-freshness.py
run_gate "Version-date consistency audit"                python3 .claude/skills/corpus-management/tools/lint-version-date-consistency.py
run_gate "Metadata-block line-break audit"               python3 .claude/skills/corpus-management/tools/lint-metadata-line-breaks.py
run_gate "Document Date staleness audit"                 python3 .claude/skills/corpus-management/tools/lint-document-date-staleness.py

# ----------------------------------------------------------------------
# Generator-output drift gates (the first 2 of 7 generator --check gates).
# These ensure the auto-generated .claude/skills/corpus-management/data/taxonomy.yml (from document metadata and
# document structure) and portal.md / maturity-scorecard.md (from the
# taxonomy) are in sync with their sources. The other 5 generator --check
# gates (narrative registry, TODO number-allocation, relationship model,
# corpus-management outputs, citation publishers) run in later sections.
# ----------------------------------------------------------------------
run_gate "Machine-readable taxonomy in sync"             python3 .claude/skills/corpus-management/tools/build-taxonomy.py --check
run_gate "Adopter portal and maturity scorecard in sync" python3 .claude/skills/corpus-management/tools/build-portal.py --check

# ----------------------------------------------------------------------
# Self-parity gate (1 gate). Validates that the spec inventory, this runner
# and the pre-commit hook declare the same gates with the same names and
# scripts in the same order, and that the workflow declares exactly the
# section 4 CI subset, in the same order. See
# .claude/skills/corpus-management/specs/specification-audit-programme.md section 3
# principle 5 for the surface-parity rule this gate enforces.
# ----------------------------------------------------------------------
run_gate "Gate-name parity audit"                        python3 .claude/skills/corpus-management/tools/lint-audit-gate-parity.py

# ----------------------------------------------------------------------
# Linter regression test suite (1 gate). Positive tests for each
# in-scope linter: each test constructs a synthetic fixture appropriate to the linter's target surface (Markdown for corpus linters, Python source for the gate-94/95 code linters)
# that should trigger exactly one rule, invokes the linter, and asserts
# its findings exit code (1 unless the test names another code). See .claude/skills/corpus-management/tests/README.md for scope and limits.
# ----------------------------------------------------------------------
run_gate "Linter regression test suite"                  python3 .claude/skills/corpus-management/tools/run-linter-regression.py

# ----------------------------------------------------------------------
# Claude-rules local-copy sync (1 gate). Verifies that the project-local
# .claude/rules/ copies still match their vendored .claude/aiqt/
# pack sources. Both trees are exempt from the corpus linters, so this
# is the only gate that catches drift between a rule's source and the
# copy a session actually loads. Placed last to avoid renumbering the
# meta-gates above; logically a drift check akin to the generator-output
# in-sync gates.
# ----------------------------------------------------------------------
# Gate 37 also verifies pinned AIQT ownership, scopes, and retained procedures.
run_gate "Claude-rules local-copy sync audit"            python3 .claude/skills/corpus-management/tools/lint-claude-rules-sync.py
run_gate "Section placement audit"                       python3 .claude/skills/corpus-management/tools/lint-section-placement.py
run_gate "Cross-file gate-count consistency audit"       python3 .claude/skills/corpus-management/tools/lint-gate-count-consistency.py
run_gate "Corpus version-bump-recency audit"             python3 .claude/skills/corpus-management/tools/lint-version-bump-recency.py
run_gate "Collection-enumeration consistency audit"      python3 .claude/skills/corpus-management/tools/lint-collection-enumeration-consistency.py
run_gate "TODO staleness audit"                          python3 .claude/skills/corpus-management/tools/lint-todo-staleness.py
run_gate "Listing-surface completeness audit"            python3 .claude/skills/corpus-management/tools/lint-listing-surface-completeness.py
run_gate "CSA CCM/AICM citation-accuracy audit"          python3 .claude/skills/corpus-management/tools/lint-ccm-aicm-citations.py
run_gate "Matrix control-code validity audit"            python3 .claude/skills/corpus-management/tools/lint-matrix-control-codes.py
run_gate "CCM provider-member range-direction audit"     python3 .claude/skills/corpus-management/tools/lint-ccm-provider-member-in-range.py
run_gate "Directory-scan-scope parity audit"             python3 .claude/skills/corpus-management/tools/lint-scan-scope-parity.py
run_gate "Corpus-to-project directional-dependency audit" python3 .claude/skills/corpus-management/tools/lint-directional-dependency.py
run_gate "Per-document NIST CSF 2.0 control-code validity audit" python3 .claude/skills/corpus-management/tools/lint-document-control-codes.py
run_gate "Cross-document retention-consistency audit"    python3 .claude/skills/corpus-management/tools/lint-retention-consistency.py
run_gate "Bare-normative-shall audit"                    python3 .claude/skills/corpus-management/tools/lint-bare-normative-shall.py
run_gate "Backlog marked-done audit"                        python3 .claude/skills/corpus-management/tools/lint-todo-marked-done.py
run_gate "Per-document ISO Annex A validity audit"       python3 .claude/skills/corpus-management/tools/lint-document-iso-annex-a.py
run_gate "CHANGELOG mirror header-parity audit"          python3 .claude/skills/corpus-management/tools/lint-changelog-mirror-header-parity.py
run_gate "COBIT/ISO 31000 citation-existence audit"      python3 .claude/skills/corpus-management/tools/lint-cobit-iso31000-citations.py
run_gate "Cross-file section-reference audit"            python3 .claude/skills/corpus-management/tools/lint-cross-file-section-refs.py
run_gate "Audit-spec detailed-prose presence audit"       python3 .claude/skills/corpus-management/tools/lint-audit-spec-detailed-prose.py
run_gate "Cross-file section-name audit"                   python3 .claude/skills/corpus-management/tools/lint-cross-file-section-names.py
run_gate "Unbalanced-fence audit"                         python3 .claude/skills/corpus-management/tools/lint-unbalanced-fences.py
run_gate "Document-Type enumeration parity audit"         python3 .claude/skills/corpus-management/tools/lint-doctype-parity.py
run_gate "Nested-markdown-link audit"                     python3 .claude/skills/corpus-management/tools/lint-nested-markdown-links.py
run_gate "Positional backlog-token audit"                 python3 .claude/skills/corpus-management/tools/lint-positional-backlog-tokens.py
run_gate "Sibling-repo stub-guard audit"                  python3 .claude/skills/corpus-management/tools/lint-sibling-placeholders.py
run_gate "Stdlib-only import audit"                       python3 .claude/skills/corpus-management/tools/lint-stdlib-only-imports.py
run_gate "Citation-currency-cadence audit"                python3 .claude/skills/corpus-management/tools/lint-citation-currency-cadence.py
run_gate "COBIT objective title-text audit"               python3 .claude/skills/corpus-management/tools/lint-cobit-title-text.py
run_gate "Web-to-corpus link-target integrity audit"      python3 .claude/skills/corpus-management/tools/lint-web-corpus-links.py
run_gate "Gate-name-citation inventory audit"             python3 .claude/skills/corpus-management/tools/lint-gate-citation-inventory.py
run_gate "Backlog item-number permanence audit"                 python3 .claude/skills/corpus-management/tools/lint-todo-number-permanence.py
run_gate "NIST SSDF control-id validity audit"                python3 .claude/skills/corpus-management/tools/lint-ssdf-control-ids.py
run_gate "Backlog list-tag audit"                          python3 .claude/skills/corpus-management/tools/lint-todo-list-tag.py
run_gate "Ungated-surface dash audit"                       python3 .claude/skills/corpus-management/tools/lint-ungated-dashes.py
run_gate "Narrative metadata audit"                      python3 .claude/skills/corpus-management/tools/lint-narrative-metadata.py
run_gate "Narrative registry sync"                       python3 .claude/skills/corpus-management/tools/build-narrative-registry.py --check
run_gate "Narrative boundary audit"                      python3 .claude/skills/corpus-management/tools/lint-narrative-boundary.py
run_gate "Narrative authority-boundary audit"            python3 .claude/skills/corpus-management/tools/lint-narrative-authority-boundary.py
run_gate "Narrative vocabulary audit"                    python3 .claude/skills/corpus-management/tools/lint-narrative-vocabulary.py
run_gate "Narrative disclaimer-presence audit"            python3 .claude/skills/corpus-management/tools/lint-narrative-disclaimer.py
run_gate "Backlog index-reference parity audit"                    python3 .claude/skills/corpus-management/tools/lint-todo-index-reference-parity.py
run_gate ".working/TODO.md number-allocation block sync"                    python3 .claude/skills/corpus-management/tools/build-todo-number-allocation.py --check
run_gate "Index-header parity audit"                              python3 .claude/skills/corpus-management/tools/lint-index-header-parity.py --strict-owner
run_gate "Relationship model in sync"                            python3 .claude/skills/corpus-management/tools/build-relationship-model.py --check
run_gate "Static unused-import audit"                            python3 .claude/skills/corpus-management/tools/lint-unused-imports.py --enforce
run_gate "Alignment-citation existence audit"                     python3 .claude/skills/corpus-management/tools/lint-alignment-citation-existence.py --strict
run_gate "Skill verdict carrier-completeness audit"            python3 .claude/skills/corpus-management/tools/lint-skill-verdict-carrier-completeness.py
run_gate "AIQT vendor digest audit"                              python3 .claude/skills/corpus-management/tools/lint-aiqt-vendor-digest.py
run_gate "Corpus-management generated outputs in sync"           python3 .claude/skills/corpus-management/tools/build-corpus-management.py --check --release-delta
run_gate "Allow-list and publisher-table parity audit"            python3 .claude/skills/corpus-management/tools/lint-allowlist-spec-parity.py
run_gate "Citation-publisher table in sync with its source of record"  python3 .claude/skills/corpus-management/tools/build-citation-publishers.py --check
run_gate "Reference-absence claim audit"                         python3 .claude/skills/corpus-management/tools/lint-ref-absence-claims.py
# Gate 106 runs both halves of delta gate D10 here (the startup character and the
# core-line ceilings), so the ceilings the pre-push guard enforces are visible to a
# corpus-gate run.
run_gate "Startup character and core-line ceiling audit"        python3 .claude/skills/corpus-management/tools/lint-startup-character-ceiling.py
run_gate "Tooling backlog-reference audit"                       python3 .claude/skills/corpus-management/tools/lint-tooling-backlog-refs.py
run_gate "Table cell-count audit"                                python3 .claude/skills/corpus-management/tools/lint-table-cell-count.py
run_gate "Isolated-launch import audit"                          python3 .claude/skills/corpus-management/tools/lint-isolated-launch.py
run_gate "Baseline-pin integrity audit"                          python3 .claude/skills/corpus-management/tools/lint-baseline-pin.py
run_gate "Public hooks syntax and registration-parity audit"     python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py

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
