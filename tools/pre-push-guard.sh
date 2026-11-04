#!/usr/bin/env bash
#
# pre-push-guard.sh
#
# The single pre-push QA gate, run by the installed git pre-push hook:
#
#   tools/install-git-hooks.sh       # once per clone, shared by worktrees
#   tools/install-git-hooks.sh --check
#   git push -u origin <branch>
#
# A direct run remains available; every guarded push runs the guard again.
# Hook output streams through a regular file; direct pipes retain RM-10 refusal.
# Git --no-verify and core.hooksPath can bypass hooks; see tools/README.md.
#
# A push whose every changed path is site-only takes the FAST PATH described
# below; any other push runs the full guard. The full guard chains the two
# runners that PR-workflow step 4 mandates, plus a web-generator health check,
# before any push, stopping on the first failure:
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
# green full guard means the push will not flip CI red on a gate failure. A
# green fast path does not carry that promise (see its residual below).
#
# Site-only fast path (maintainer directive 2026-11-04: accelerated pushes when
# the change is web site content, not corpus or tooling).
#
#   Changed set: the committed diff (git diff --name-only --no-renames) from the
#   merge base of BASE_REF (origin/main by default, the base
#   tools/run-pr-time-checks.sh uses) to HEAD, read after the fetch below. The
#   guard FAILS CLOSED to the full guard when HEAD_REF names anything other than
#   HEAD, when PRE_PUSH_GUARD_ALLOW_DIRTY is set (the working tree the gates
#   read may then hold changes the diff does not show), when git cannot read the
#   merge base or finds more than one, when the diff cannot be read, and when it
#   is empty. A path git quotes (an unusual character) is never site-only.
#
#   Site-only paths: anything under .web/ (the templates, the generator
#   .web/build.py and the vendored .web/baseline/ files), anything under
#   .baseline/, tests/test_web_draft.py, and the per-PR close-out surfaces
#   CHANGELOG.md, README.md and NOTICE.md at the repository root. README.md and
#   NOTICE.md belong: a site PR bumps the README library version (60d550d58),
#   and a baseline or licence change updates NOTICE.md; 65669d0c6 and 8fee33861
#   each change only .web/, .baseline/, tests/test_web_draft.py, CHANGELOG.md,
#   README.md and NOTICE.md. Both files are corpus-adjacent, so every gate that
#   scans them still runs. Any other path (a corpus document, tools/, any other
#   test, .claude/, .corpus-management/, .github/, a generated registry) means
#   the full guard.
#
#   The fast path runs, stopping on the first failure:
#     1. tools/run-pr-time-checks.sh (unchanged; every delta gate, D3 included).
#     2. Each tools/run_all_audits.sh gate, in runner order, that FAST_GATES
#        below tags for a changed path. The table names, with the runner's name
#        and command, every runner gate whose traced run at 65669d0c6 opened,
#        listed or passed to git a path of that kind (w .web/, b .baseline/,
#        t tests/test_web_draft.py, c CHANGELOG.md, r README.md, n NOTICE.md),
#        plus the CHANGELOG mirror gate (59), which reads CHANGELOG.md only
#        when the operational store supplies its detailed mirror, a code path
#        the trace did not take. For CHANGELOG.md and README.md that includes
#        the language gate (2, which also enforces the no-dash rule there; the
#        ungated-surface dash gate 82 does not scan either file), the link
#        gates (3, 11, 17, 68) and the version gates (13, 29, 40); gate numbers
#        are those of governance/specification-audit-programme.md section 6.
#        As in tools/run_all_audits.sh, a passing gate prints only OK and a
#        failing gate's output is printed in full; unlike the runner, no
#        advisory lines are echoed from a passing gate.
#     3. The baseline-pin gate (gate 110, tools/lint-baseline-pin.py) and the
#        palette gate .baseline/check_palette.py, run as the build runs it.
#     4. .web/build.py --check and python3 -B tests/test_web_draft.py.
#     5. The tests/test_linters.py classes of the linter regression suite
#        (gate 36) that read the real .web/ and .baseline/ trees, selected by
#        the class-name patterns in FAST_TEST_PATTERNS below (so a new class
#        with one of those prefixes is included); output as for step 2.
#   It prints one FAST PATH line naming the changed paths, then the reference
#   manifest advisory, then a PASS line with the elapsed time.
#
#   Site-scope record: every tools/run_all_audits.sh gate is named, by runner
#   name and command, in exactly one of FAST_GATES, FAST_STEP_GATES (gates 36
#   and 110, run by steps 5 and 3) and SITE_UNSCANNED_GATES (the gates whose
#   traced run touched no site-only path); PrePushGuardFastPathTests fails
#   otherwise. tools/gate-scope-manifest.json records only whether a gate scans
#   the executive/ narrative tree, so it cannot answer site scope for any gate,
#   and these tables are the record. At run time the guard reads the runner's
#   gate lines: a gate in none of the tables runs on every fast path (fail
#   closed) with a NOTE naming it, and a gate line the guard cannot parse, or a
#   runner it cannot read, means the full guard.
#
#   Skipped locally: every SITE_UNSCANNED_GATES gate, each FAST_GATES entry
#   whose tags match no changed path, and every gate 36 test outside step 5.
#   Each one is still covered before merge: .github/workflows/quality.yml runs
#   the full gate set on every pull request (kept in lock-step with
#   run_all_audits.sh by the gate-parity gate), and tools/merge-when-green.py
#   merges only on green CI. This change alters neither.
#
#   Residual (what is lost): local detection, before the push, of a failure in a
#   skipped gate; that failure now first shows in CI. A site-only change cannot
#   change what a SITE_UNSCANNED_GATES gate scans, by the trace above.
#   Exceptions, which a site-only change CAN fail:
#     - a gate 36 test outside step 5 that reads CHANGELOG.md, README.md or
#       NOTICE.md over the real tree (directly or through a gate it runs), or
#       reads a site path other than by a REPO_ROOT join;
#     - any gate that reads a site-only path only on a code path neither the
#       traced run nor a later reading found; move such a gate from
#       SITE_UNSCANNED_GATES to FAST_GATES when its scan scope changes.
#
# Scope boundary: this guard gates PUSHES (the two post-commit / pre-push
# runners plus the conditional `.web/build.py --check`). The commit-time
# hygiene gate, `preflight-changelog.py`, gates COMMITS, because it judges
# newly-added lines that are already committed by push time. In a clone
# where tools/install-git-hooks.sh has installed the pre-commit hook,
# tools/check-changelog-preflight-commit.py runs it with --staged, judging
# the staged (index) lines, on each `git commit` that stages CHANGELOG.md;
# in a clone without the installer, the `&&` chain
# (`python3 tools/preflight-changelog.py && git commit`) remains the
# commit-time gate. The two helpers are complementary, not redundant.
#
# Usage:
#   git push -u origin <branch>
#   BASE_REF=origin/develop tools/pre-push-guard.sh   # non-default base
#
# Exit codes: 1 for an installed-hook check failure; 0 only if both runners and the web check (when .web/build.py is present) pass, or on the fast path only if every fast-path check passes; 3 if the guard REFUSES to run
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
      echo "pre-push-guard: REFUSING to push (1.19.8 (closing PR #1030) _private-required): origin is the maintainer repo but grc_library_private is absent or empty. It holds the operational state the CLAUDE.md delegation directive points to; clone it (git clone <the private sibling's remote URL> ../grc_library_private) or grant access (--add-dir ../grc_library_private), then retry. An adopter clone is exempt." >&2
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

# Validate the shared dispatcher even for a direct run. CI has no private store.
sh tools/install-git-hooks.sh --check || exit $?

# Best-effort refresh of the merge base so the delta gates in
# run-pr-time-checks.sh compare against the true base ref (origin/main by
# default; whatever BASE_REF names otherwise). Fetching all of origin keeps
# the refresh correct under a BASE_REF override. Offline is tolerated:
# run-pr-time-checks.sh falls back to whatever base ref exists locally, and a
# stale base only risks a false PASS on the delta gates, which CI then catches.
if ! git fetch origin --quiet 2>/dev/null; then
  echo "pre-push-guard: WARNING: fetch of origin failed; delta gates use the locally available base, which may be stale." >&2
fi

# Site-only fast path selection (see the header). Any doubt leaves fast_path at
# 0 with the reason in full_reason, so the full guard runs.
BASE_REF="${BASE_REF:-origin/main}"
fast_path=0
full_reason=""
changed_paths=()
changed_tags=""
if [ -n "${HEAD_REF:-}" ] && [ "${HEAD_REF}" != "HEAD" ]; then
    full_reason="HEAD_REF is ${HEAD_REF}, not HEAD, so the changed set would not describe the tree the gates read"
elif [ -n "${PRE_PUSH_GUARD_ALLOW_DIRTY:-}" ]; then
    full_reason="PRE_PUSH_GUARD_ALLOW_DIRTY is set, so the working tree may hold changes outside the committed diff"
elif ! merge_base="$(git merge-base --all "${BASE_REF}" HEAD 2>/dev/null)" || [ -z "${merge_base}" ]; then
    full_reason="the merge base of ${BASE_REF} and HEAD cannot be read"
elif [[ "${merge_base}" == *$'\n'* ]]; then
    full_reason="${BASE_REF} and HEAD have more than one merge base"
elif ! changed="$(git -c core.quotePath=true diff --name-only --no-renames "${merge_base}" HEAD --)"; then
    full_reason="git diff ${merge_base} HEAD failed, so the changed set cannot be read"
elif [ -z "${changed}" ]; then
    full_reason="the changed set against ${BASE_REF} is empty"
else
    fast_path=1
    while IFS= read -r path; do
        changed_paths+=("${path}")
        case "${path}" in
            .web/*) changed_tags+="w" ;;
            .baseline/*) changed_tags+="b" ;;
            tests/test_web_draft.py) changed_tags+="t" ;;
            CHANGELOG.md) changed_tags+="c" ;;
            README.md) changed_tags+="r" ;;
            NOTICE.md) changed_tags+="n" ;;
            *)
                if [ "${fast_path}" -eq 1 ]; then
                    full_reason="${path} is not a site-only path"
                fi
                fast_path=0
                ;;
        esac
    done <<< "${changed}"
fi

# The runner's gates, as "runner name|command" in runner order, read from its
# run_gate lines (see the site-scope record in the header). A line that starts
# with run_gate but does not match the one shape the runner uses, an unreadable
# runner, or no gate at all means the full guard.
runner_gates=()
if [ "${fast_path}" -eq 1 ]; then
    call_re='^[[:space:]]*run_gate([[:space:]]|$)'
    gate_re='^run_gate[[:space:]]+"([^"]+)"[[:space:]]+python3[[:space:]]+(.*[^[:space:]])[[:space:]]*$'
    if [ ! -f tools/run_all_audits.sh ] || [ ! -r tools/run_all_audits.sh ]; then
        fast_path=0
        full_reason="tools/run_all_audits.sh cannot be read, so its gates cannot be checked against the site-scope record"
    else
        while IFS= read -r line || [ -n "${line}" ]; do
            [[ "${line}" =~ ${call_re} ]] || continue
            if [[ "${line}" =~ ${gate_re} ]]; then
                name="${BASH_REMATCH[1]}"
                read -r -a words <<< "${BASH_REMATCH[2]}"
                runner_gates+=("${name}|${words[*]}")
            else
                fast_path=0
                full_reason="the tools/run_all_audits.sh line '${line}' cannot be parsed, so its gate cannot be checked against the site-scope record"
                break
            fi
        done < tools/run_all_audits.sh
        if [ "${fast_path}" -eq 1 ] && [ "${#runner_gates[@]}" -eq 0 ]; then
            fast_path=0
            full_reason="no gate was read from tools/run_all_audits.sh"
        fi
    fi
fi

# The run_all_audits.sh gates the fast path runs when one of their tags names a
# kind of changed path: "tags|runner name|command", in runner order, with the
# runner's own name and command (PrePushGuardFastPathTests pins both against
# tools/run_all_audits.sh). Tags: w .web/, b .baseline/, t tests/test_web_draft.py,
# c CHANGELOG.md, r README.md, n NOTICE.md.
FAST_GATES=(
    "n|Metadata audit|tools/lint-metadata.py"
    "crn|Language and style audit|tools/lint-language.py"
    "wcrn|Repository-internal link audit|tools/lint-links.py"
    "rn|Framework citation hallucination audit|tools/lint-citations.py"
    "wrn|Standards-currency audit|tools/lint-standards-currency.py"
    "rn|Owner and Approving Authority role audit|tools/lint-roles.py"
    "rn|Mandatory requirement near uncertainty marker audit|tools/lint-shall-near-uncertainty.py"
    "c|CHANGELOG file-reference link coverage|tools/lint-changelog-link-coverage.py"
    "wbrn|Placeholder leakage audit|tools/lint-placeholder-leakage.py"
    "wbrn|Library and document version monotonicity audit|tools/lint-library-version-monotonicity.py"
    "wbcrn|Metadata date format audit|tools/lint-date-format.py"
    "wbcr|License consistency audit|tools/lint-license-consistency.py"
    "wb|Stub document audit|tools/lint-stub-documents.py"
    "wbcrn|Section anchor reference audit|tools/lint-section-anchors.py"
    "wbrn|Intra-document section reference audit|tools/lint-intra-doc-refs.py"
    "wb|Required sections audit|tools/lint-required-sections.py"
    "wbrn|Acronym expansion consistency audit|tools/lint-acronym-consistency.py"
    "wbtcrn|Secret pattern audit|tools/lint-secrets-in-content.py"
    "wbtrn|PII pattern audit|tools/lint-pii-in-content.py"
    "wbtrn|Internal references audit|tools/lint-internal-references.py"
    "wbtcrn|External link domain audit|tools/lint-external-link-domains.py"
    "wbrn|Cross-document numerical coherence audit|tools/lint-cross-doc-numbers.py"
    "wbcrn|Orphan document audit|tools/lint-orphan-documents.py"
    "cr|Version-date consistency audit|tools/lint-version-date-consistency.py"
    "crn|Metadata-block line-break audit|tools/lint-metadata-line-breaks.py"
    "rn|Document Date staleness audit|tools/lint-document-date-staleness.py"
    "wbcrn|Section placement audit|tools/lint-section-placement.py"
    "wbtrn|Cross-file gate-count consistency audit|tools/lint-gate-count-consistency.py"
    "wbcrn|Corpus version-bump-recency audit|tools/lint-version-bump-recency.py"
    "wbrn|CSA CCM/AICM citation-accuracy audit|tools/lint-ccm-aicm-citations.py"
    "wbrn|CCM provider-member range-direction audit|tools/lint-ccm-provider-member-in-range.py"
    "wbcrn|Bookkeeping-parity audit|tools/lint-bookkeeping-parity.py"
    "rn|Corpus-to-project directional-dependency audit|tools/lint-directional-dependency.py"
    "rn|Bare-normative-shall audit|tools/lint-bare-normative-shall.py"
    "c|CHANGELOG mirror header-parity audit|tools/lint-changelog-mirror-header-parity.py"
    "wbrn|COBIT/ISO 31000 citation-existence audit|tools/lint-cobit-iso31000-citations.py"
    "wbrn|Cross-file section-reference audit|tools/lint-cross-file-section-refs.py"
    "wbrn|Cross-file section-name audit|tools/lint-cross-file-section-names.py"
    "wbcrn|Unbalanced-fence audit|tools/lint-unbalanced-fences.py"
    "r|Document-Type enumeration parity audit|tools/lint-doctype-parity.py"
    "wbcrn|Nested-markdown-link audit|tools/lint-nested-markdown-links.py"
    "rn|Positional backlog-token audit|tools/lint-positional-backlog-tokens.py"
    "wt|Stdlib-only import audit|tools/lint-stdlib-only-imports.py"
    "wbrn|COBIT objective title-text audit|tools/lint-cobit-title-text.py"
    "w|Web-to-corpus link-target integrity audit|tools/lint-web-corpus-links.py"
    "wbrn|NIST SSDF control-id validity audit|tools/lint-ssdf-control-ids.py"
    "wbcrn|Narrative boundary audit|tools/lint-narrative-boundary.py"
    "rn|Narrative authority-boundary audit|tools/lint-narrative-authority-boundary.py"
    "wt|Static unused-import audit|tools/lint-unused-imports.py --enforce"
    "wbrn|Alignment-citation existence audit|tools/lint-alignment-citation-existence.py --strict"
    "wbtcrn|Worker-id anonymity audit|tools/lint-worker-id-anonymity.py"
    "rn|Reference-absence claim audit|tools/lint-ref-absence-claims.py"
    "wcrn|Table cell-count audit|tools/lint-table-cell-count.py"
)

# The run_all_audits.sh gates a fast-path step of its own covers: gate 36 by its
# site-reading classes (FAST_TEST_PATTERNS), gate 110 whole.
FAST_STEP_GATES=(
    "Linter regression test suite|tools/run-linter-regression.py"
    "Baseline-pin integrity audit|tools/lint-baseline-pin.py"
)

# The run_all_audits.sh gates whose traced run at 65669d0c6 touched no site-only
# path, in runner order: the fast path skips them.
SITE_UNSCANNED_GATES=(
    "Structural index integrity audit|tools/lint-structure.py"
    "Filename and Document Title alignment audit|tools/lint-filename-title-alignment.py"
    "Per-document review cadence audit|tools/check-review-cadence.py"
    "Citation verification freshness audit|tools/lint-citation-verification-freshness.py"
    "Tooling provenance freshness audit|tools/lint-tooling-provenance-freshness.py"
    "Skill derives-from reference audit|tools/lint-skill-derives-from.py"
    "Machine-readable taxonomy in sync|tools/build-taxonomy.py --check"
    "Adopter portal and maturity scorecard in sync|tools/build-portal.py --check"
    "Gate-name parity audit|tools/lint-audit-gate-parity.py"
    "Claude-rules local-copy sync audit|tools/lint-claude-rules-sync.py"
    "Collection-enumeration consistency audit|tools/lint-collection-enumeration-consistency.py"
    "External-overlay license consistency audit|tools/lint-external-overlay-license.py"
    "Follow-up ageing audit|tools/lint-followup-ageing.py"
    "Paired-skill step-parity audit|tools/lint-paired-skill-step-parity.py"
    "TODO staleness audit|tools/lint-todo-staleness.py"
    "Overnight-work file audit|tools/lint-overnight-file.py"
    "Listing-surface completeness audit|tools/lint-listing-surface-completeness.py"
    "Matrix control-code validity audit|tools/lint-matrix-control-codes.py"
    "Working-tree prose-hygiene audit|tools/lint-working-prose-hygiene.py"
    "Directory-scan-scope parity audit|tools/lint-scan-scope-parity.py"
    "Per-document NIST CSF 2.0 control-code validity audit|tools/lint-document-control-codes.py"
    "Cross-document retention-consistency audit|tools/lint-retention-consistency.py"
    "Backlog marked-done audit|tools/lint-todo-marked-done.py"
    "Per-document ISO Annex A validity audit|tools/lint-document-iso-annex-a.py"
    "Guardrail-review cadence audit|tools/lint-guardrail-cadence.py"
    "Session-state lease audit|tools/lint-session-state.py"
    "Audit-spec detailed-prose presence audit|tools/lint-audit-spec-detailed-prose.py"
    "Sibling-repo stub-guard audit|tools/lint-sibling-placeholders.py"
    "Citation-currency-cadence audit|tools/lint-citation-currency-cadence.py"
    "Rule-scope-table completeness audit|tools/lint-rule-scope-table.py"
    "Skill-body internal-reference audit|tools/lint-skill-internal-refs.py"
    "Gate-name-citation inventory audit|tools/lint-gate-citation-inventory.py"
    "Backlog item-number permanence audit|tools/lint-todo-number-permanence.py"
    "Playbook-pointer-integrity audit|tools/lint-playbook-pointer-integrity.py"
    "Backlog list-tag audit|tools/lint-todo-list-tag.py"
    "Ungated-surface dash audit|tools/lint-ungated-dashes.py"
    "Publication-manifest sync audit|tools/lint-publication-manifest.py"
    "Narrative metadata audit|tools/lint-narrative-metadata.py"
    "Narrative registry sync|tools/build-narrative-registry.py --check"
    "Narrative vocabulary audit|tools/lint-narrative-vocabulary.py"
    "Narrative disclaimer-presence audit|tools/lint-narrative-disclaimer.py"
    "Backlog index-reference parity audit|tools/lint-todo-index-reference-parity.py"
    "TODO.md number-allocation block sync|tools/build-todo-number-allocation.py --check"
    "Index-header parity audit|tools/lint-index-header-parity.py --strict-owner"
    "Relationship model in sync|tools/build-relationship-model.py --check"
    "Hooks Python-syntax audit|tools/lint-hooks-syntax.py"
    "Skill verdict carrier-completeness audit|tools/lint-skill-verdict-carrier-completeness.py"
    "AIQT vendor digest audit|tools/lint-aiqt-vendor-digest.py"
    "Corpus-management generated outputs in sync|tools/build-corpus-management.py --check --release-delta"
    "Allow-list and publisher-table parity audit|tools/lint-allowlist-spec-parity.py"
    "Citation-publisher table in sync with its source of record|tools/build-citation-publishers.py --check"
    "Hook-launcher isolation audit|tools/lint-hooks-syntax.py --launcher-isolation"
    "Startup character and core-line ceiling audit|tools/lint-startup-character-ceiling.py"
    "Tooling backlog-reference audit|tools/lint-tooling-backlog-refs.py"
    "Isolated-launch import audit|tools/lint-isolated-launch.py"
)

# Step 5: the unittest -k patterns (fnmatch over __main__.<class>.<test>) that
# select the tests/test_linters.py tests over the real .web/ and .baseline/ trees.
# Each prefix pattern also takes in a later class with that prefix;
# PrePushGuardFastPathTests requires each pattern to select a test and every
# class that joins REPO_ROOT with a site path to have a selected test.
FAST_TEST_PATTERNS=(
    "*.WebGenerator*.*"
    "*.WebCorpusLink*.*"
    "*.WebSiteHardening*.*"
    "*.BaselinePinLinter*.*"
    "*.GeneratorSortKeyParity*.*"
    "*.CorpusManagementScanScopeTests.test_closed_wired_inventory"
)

# One fast-path step: run it from the bare command (see the capture note below)
# and, on a non-zero status, report it and exit with that status.
fast_step() {
    local label="$1"
    shift
    echo ""
    echo "=== pre-push guard fast path: ${label} ==="
    "$@"
    local rc=$?
    if [ "${rc}" -ne 0 ]; then
        echo ""
        echo "pre-push guard FAILED at ${label} (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi
}

# One fast-path audit gate: like tools/run_all_audits.sh, a passing gate's output
# stays hidden (its advisory lines are not echoed here) and a failing gate's
# output is printed in full before the guard exits with the gate's status.
fast_gate() {
    local label="$1"
    shift
    local out rc
    printf '%-66s ... ' "pre-push guard fast path gate: ${label}"
    out="$("$@" 2>&1)"
    rc=$?
    if [ "${rc}" -ne 0 ]; then
        echo "FAIL (rc=${rc})"
        printf '%s\n' "${out}"
        echo ""
        echo "pre-push guard FAILED at ${label} (rc=${rc}). Fix the artefact; do not push."
        exit "${rc}"
    fi
    echo "OK"
}

if [ "${fast_path}" -eq 1 ]; then
    echo "=== pre-push guard FAST PATH: every changed path is site-only, so only the site checks run here; the full suite (tools/run_all_audits.sh) still runs in CI before merge. Changed paths (${#changed_paths[@]}): ${changed_paths[*]} ==="
    fast_step "run-pr-time-checks.sh (delta + history-aware gates)" tools/run-pr-time-checks.sh
    skipped=$'\n'
    for key in "${FAST_STEP_GATES[@]}" "${SITE_UNSCANNED_GATES[@]}"; do
        skipped+="${key}"$'\n'
    done
    for key in "${runner_gates[@]}"; do
        name="${key%%|*}"
        cmd="${key#*|}"
        tags=""
        for entry in "${FAST_GATES[@]}"; do
            if [ "${entry#*|}" = "${key}" ]; then
                tags="${entry%%|*}"
                break
            fi
        done
        if [ -z "${tags}" ]; then
            case "${skipped}" in
                *$'\n'"${key}"$'\n'*) continue ;;
            esac
            echo "pre-push guard fast path: NOTE: ${name} (${cmd}) has no site-scope record in tools/pre-push-guard.sh, so it runs here (fail closed); record it in FAST_GATES, FAST_STEP_GATES or SITE_UNSCANNED_GATES."
            tags="wbtcrn"
        fi
        selected=0
        for (( i = 0; i < ${#tags}; i++ )); do
            case "${changed_tags}" in
                *"${tags:i:1}"*) selected=1 ;;
            esac
        done
        if [ "${selected}" -eq 1 ]; then
            # ${cmd} is unquoted on purpose: it splits into the script and its flags.
            fast_gate "${name}" python3 ${cmd}
        fi
    done
    fast_gate "Baseline-pin integrity audit" python3 tools/lint-baseline-pin.py
    fast_step "palette gate (.baseline/check_palette.py, as .web/build.py runs it)" \
        python3 -I .baseline/check_palette.py --site grclibrary --palettes .web/baseline/palettes.css
    fast_step ".web/build.py --check (web-generator health, from HEAD)" python3 .web/build.py --check
    fast_step "tests/test_web_draft.py (web draft tests)" python3 -B tests/test_web_draft.py
    test_args=()
    for pattern in "${FAST_TEST_PATTERNS[@]}"; do
        test_args+=(-k "${pattern}")
    done
    fast_gate "Linter regression suite, site-reading classes (tests/test_linters.py)" \
        python3 -B tests/test_linters.py "${test_args[@]}"
else
    echo "pre-push-guard: running the full guard (${full_reason})."

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
if [ "${fast_path}" -eq 1 ]; then
    echo "=== pre-push guard PASS (FAST PATH, site-only change, ${SECONDS}s): the site checks are green. Safe to push; the full suite runs in CI before merge. ==="
else
    echo "=== pre-push guard PASS: all applicable checks green. Safe to push. ==="
fi
exit 0
