# Audit Programme Specification

**Document Title:** Audit Programme Specification\
**Document Type:** Specification\
**Version:** 1.16.2\
**Date:** 2026-06-24\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/charter-governance-library.md`](charter-governance-library.md), [`CHANGELOG.md`](../CHANGELOG.md), [`TODO.md`](../TODO.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual, and upon addition or removal of any audit gate\
**Repository Path:** [`governance/specification-audit-programme.md`](specification-audit-programme.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This specification defines the GRC Documentation Library's automated audit programme: the set of machine-checked rules that gate every change to the library, the mechanisms by which the rules are enforced, the surfaces on which they run, and the conditions under which gates are added, modified, or retired.

The audit programme is the library's primary defence against the failure modes catalogued in [`governance/specification-citation-verification.md`](specification-citation-verification.md) §5: drift, contradiction, mis-attribution, stale references, and silent regressions in document structure, naming, and cross-linkage. Where the Citation Verification Specification governs *what is true about the world* (publisher metadata about external standards), this specification governs *what is internally consistent about the library itself*.

## 2. Scope

### 2.1 In scope

- The audit gates currently wired into the audit-programme (see §6 for the canonical inventory and current count).
- The three enforcement surfaces (CI workflow, local audit runner, pre-commit hook).
- The doctrinal rules for adding, modifying, scoping, and retiring gates (see §9, §10).
- The relationship between the audit programme and the Citation Verification Specification (see §11).

### 2.2 Out of scope

- The substantive content of any one gate (each linter script in [`tools/`](../tools/) is self-documenting via its module docstring; this specification governs the programme, not the rules).
- External standards content (governed by the Citation Verification Specification).
- Manual quality reviews (governed by [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md)).

## 3. Design principles

The audit programme rests on five principles:

1. **Determinism over heuristic**. Every gate produces a deterministic pass/fail outcome from the repository state alone. No gate depends on network access, third-party services, or wall-clock state outside the repository.
2. **Stdlib-only Python**. Every linter is implemented in Python 3.11 standard-library code with no third-party dependencies. This keeps the audit programme reproducible across local, CI, and pre-commit surfaces with zero environment setup beyond a Python interpreter.
3. **One gate, one concern**. Each gate enforces a single, narrowly defined rule. Failure messages name the rule, the file, the line, and the offending content. When a rule's domain grows beyond one file, the gate is split rather than overloaded.
4. **Conservative scope over false positives**. A gate that would produce legitimate false positives at scale is either scoped narrowly enough to track zero items (the [`tools/lint-cross-doc-numbers.py`](../tools/lint-cross-doc-numbers.py) scaffold pattern from Phase 23.26) or not shipped at all. Honest scope management is preferred over either silent false positives or blanket exemption lists. A permitted exception is *meta-documents* whose purpose is to describe a linter's rule set (the linter script itself, the CHANGELOG, this specification, and the Citation Verification Specification): these documents inevitably contain the patterns the linter searches for and are exempted by name in the linter's exemption list, with an inline comment naming the reason.
5. **CI parity**. The local audit runner and the pre-commit hook always run the same set of gates as the CI workflow. Drift between the three surfaces is itself a recoverable defect rather than a feature.

## 4. Enforcement surfaces

The same audit-gate set runs on three surfaces:

| Surface | File | Invocation | Blocking? |
| --- | --- | --- | --- |
| GitHub Actions | [`.github/workflows/quality.yml`](../.github/workflows/quality.yml) | Automatic on push and pull-request events | Yes; required check for merge |
| Local audit runner | [`tools/run_all_audits.sh`](../tools/run_all_audits.sh) | `tools/run_all_audits.sh` (or `FAIL_FAST=1 ...`) | Yes by convention; the maintainer does not push without all gates green |
| Pre-commit hook | [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) | `pre-commit install` (one-time setup); automatic on `git commit` | Yes; commit blocked on failure |

Of the three surfaces, only the GitHub Actions workflow is authoritative: a green CI run is the only signal a reviewer can rely on. The local runner and pre-commit hook exist to catch failures earlier in the loop so they never reach CI. When the three surfaces diverge, the workflow is the source of truth and the others are synchronised to it.

## 5. Gate categories

The gates fall into the following functional categories:

1. **Metadata integrity** (gates 1, 7, 8, 13, 14, 15, 16, 19, 38, 40, 42): canonical metadata block presence and field validity; doctype-to-filename alignment; Owner and Approving Authority field validity against the role register; date format; license value; document-stub detection; required sections per doctype; section placement conventions (orientation sections in the top three `##` sections, Licence and Version-history sections in the bottom three); version monotonicity; per-document version-bump recency, verifying that each document's `Version` field has been bumped at or after the file's most-recent body change (gate 40, the corpus-side counterpart of delta gate D2); and external-overlay licence consistency, verifying that each `.claude/rules/external/<source>/` subdirectory carries the source project's declared LICENSE and that no external markdown file claims the project's own licence (gate 42, the external-overlay counterpart of gate 15).
2. **Reference integrity** (gates 3, 11, 17, 18, 24, 26): intra-repo links resolve; CHANGELOG file-reference link coverage; section anchors resolve; intra-document section references resolve; external-link domains on allow-list; orphan documents have at least one inbound reference.
3. **Content drift defence** (gates 5, 6, 25, 48): external framework hallucinations; standards currency; cross-document numerical coherence; CSA CCM/AICM citation accuracy, verifying that every cited CCM v4.1 / AICM v1.1 control names a real domain and an in-range control number and that control-listing rows title the control correctly against the authoritative catalogue (gate 48).
4. **Language and style** (gates 2, 9, 20): em-dashes, "ize/ization" Americanisms, "ensure that", sanitisation neologisms; mandatory requirements near uncertainty markers; acronym expansion consistency against the glossary.
5. **Programme and index integrity** (gates 4, 32, 35, 36, 37, 39, 41, 44, 47): repository-wide index integrity (gate 4); skill `derives_from` reference integrity, confirming each pack skill's frontmatter points to a real governance rule (gate 32); audit-programme self-consistency across all four name-parity surfaces, which are the §6 inventory table plus the three runtime surfaces enumerated in §4 (gate 35); linter regression tests that confirm each in-scope linter still detects its target rule class (gate 36); sync between the project-local `.claude/rules/` rule copies and their `dev-security/claude-rules/` pack sources (gate 37); cross-file consistency between prose references to the gate count and the actual §6 inventory row count (gate 39); consistency between canonical collection-source directories and the enumerations of those collections elsewhere in the corpus (pack governance rules, pack skills, and similar; gate 41); and step-identifier parity across paired SKILL.md and slash-command surfaces, verifying that when a skill ships both a `SKILL.md` workflow and a `.claude/commands/<name>.md` summary, the two files use the same identifiers for the same logical steps (gate 44, motivated by the Sweep 3 finding where PR #78 introduced the pre-flight scanner as `### 3.5.` in the SKILL and `3a.` in the slash-command); and listing-surface completeness, verifying that each MECHANICAL listing surface (the document-index register and each domain README) enumerates every active document in its scope, where the relevance-based SEMANTIC surfaces (the framework matrices and crosswalks, the glossary and key-terms registers, per-document `Related Documents` fields) are deliberately left to the [`tools/suggest-listing-surfaces.py`](../tools/suggest-listing-surfaces.py) authoring helper rather than a hard gate, because a completeness gate over a relevance-based surface would be noisy and erode gate-discipline (gate 47).
6. **Security and privacy** (gates 12, 21, 22, 23): placeholder leakage, secret patterns, PII patterns, internal-environment leakage (cloud regions, hostnames, deployment identifiers).
7. **Freshness and lifecycle** (gates 10, 27, 28, 29, 30, 31, 33, 34, 43, 45, 46): document review cadence, citation-verification freshness, tooling-provenance freshness, auto-generated taxonomy in sync (gate 33), auto-generated adopter portal and maturity scorecard in sync (gate 34), metadata Date staleness against the file's most-recent git commit date, follow-up ageing in the validation-sweep history register, verifying that each deferred-finding entry's re-triage-by deadline has not lapsed without a fresh re-triaged trailer (gate 43, mechanises Rule 3 of the maintenance-tag dating discipline introduced in PR #90), TODO staleness, verifying that [`TODO.md`](../TODO.md) does not still reference a queued PR that has merged or a sweep cursor behind the most-recent [`.working/validate-sweeps/history.md`](../.working/validate-sweeps/history.md) row (gate 45, added after four consecutive validation sweeps surfaced the same TODO-drift pattern), and overnight-work-file enforcement, verifying that [`.working/overnight-pr.md`](../.working/overnight-pr.md) carries a `Status:` value of `stub` (no overnight in flight) or `in-flight` (overnight session active), failing on `done` (overnight session ended but morning processing PR has not yet routed the file's content into the appropriate working-state ledgers; gate 46, codifies the overnight-work protocol).

Categorisation is descriptive, not prescriptive: a gate may bear on multiple categories. Categories exist to help reviewers reason about coverage.

## 6. Gate inventory (current)

The numbering matches the order in [`tools/run_all_audits.sh`](../tools/run_all_audits.sh) and [`.github/workflows/quality.yml`](../.github/workflows/quality.yml).

| # | Gate | Script |
| --- | --- | --- |
| 1 | Metadata audit | [`tools/lint-metadata.py`](../tools/lint-metadata.py) |
| 2 | Language and style audit | [`tools/lint-language.py`](../tools/lint-language.py) |
| 3 | Repository-internal link audit | [`tools/lint-links.py`](../tools/lint-links.py) |
| 4 | Structural index integrity audit | [`tools/lint-structure.py`](../tools/lint-structure.py) |
| 5 | Framework citation hallucination audit | [`tools/lint-citations.py`](../tools/lint-citations.py) |
| 6 | Standards-currency audit | [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py) |
| 7 | Filename and Document Title alignment audit | [`tools/lint-filename-title-alignment.py`](../tools/lint-filename-title-alignment.py) |
| 8 | Owner and Approving Authority role audit | [`tools/lint-roles.py`](../tools/lint-roles.py) |
| 9 | Mandatory requirement near uncertainty marker audit | [`tools/lint-shall-near-uncertainty.py`](../tools/lint-shall-near-uncertainty.py) |
| 10 | Per-document review cadence audit | [`tools/check-review-cadence.py`](../tools/check-review-cadence.py) |
| 11 | CHANGELOG file-reference link coverage | [`tools/lint-changelog-link-coverage.py`](../tools/lint-changelog-link-coverage.py) |
| 12 | Placeholder leakage audit | [`tools/lint-placeholder-leakage.py`](../tools/lint-placeholder-leakage.py) |
| 13 | Library and document version monotonicity audit | [`tools/lint-library-version-monotonicity.py`](../tools/lint-library-version-monotonicity.py) |
| 14 | Metadata date format audit | [`tools/lint-date-format.py`](../tools/lint-date-format.py) |
| 15 | License consistency audit | [`tools/lint-license-consistency.py`](../tools/lint-license-consistency.py) |
| 16 | Stub document audit | [`tools/lint-stub-documents.py`](../tools/lint-stub-documents.py) |
| 17 | Section anchor reference audit | [`tools/lint-section-anchors.py`](../tools/lint-section-anchors.py) |
| 18 | Intra-document section reference audit | [`tools/lint-intra-doc-refs.py`](../tools/lint-intra-doc-refs.py) |
| 19 | Required sections audit | [`tools/lint-required-sections.py`](../tools/lint-required-sections.py) |
| 20 | Acronym expansion consistency audit | [`tools/lint-acronym-consistency.py`](../tools/lint-acronym-consistency.py) |
| 21 | Secret pattern audit | [`tools/lint-secrets-in-content.py`](../tools/lint-secrets-in-content.py) |
| 22 | PII pattern audit | [`tools/lint-pii-in-content.py`](../tools/lint-pii-in-content.py) |
| 23 | Internal references audit | [`tools/lint-internal-references.py`](../tools/lint-internal-references.py) |
| 24 | External link domain audit | [`tools/lint-external-link-domains.py`](../tools/lint-external-link-domains.py) |
| 25 | Cross-document numerical coherence audit | [`tools/lint-cross-doc-numbers.py`](../tools/lint-cross-doc-numbers.py) |
| 26 | Orphan document audit | [`tools/lint-orphan-documents.py`](../tools/lint-orphan-documents.py) |
| 27 | Citation verification freshness audit | [`tools/lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py) |
| 28 | Tooling provenance freshness audit | [`tools/lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py) |
| 29 | Version-date consistency audit | [`tools/lint-version-date-consistency.py`](../tools/lint-version-date-consistency.py) |
| 30 | Metadata-block line-break audit | [`tools/lint-metadata-line-breaks.py`](../tools/lint-metadata-line-breaks.py) |
| 31 | Document Date staleness audit | [`tools/lint-document-date-staleness.py`](../tools/lint-document-date-staleness.py) |
| 32 | Skill derives-from reference audit | [`tools/lint-skill-derives-from.py`](../tools/lint-skill-derives-from.py) |
| 33 | Machine-readable taxonomy in sync | [`tools/build-taxonomy.py`](../tools/build-taxonomy.py) |
| 34 | Adopter portal and maturity scorecard in sync | [`tools/build-portal.py`](../tools/build-portal.py) |
| 35 | Gate-name parity audit | [`tools/lint-audit-gate-parity.py`](../tools/lint-audit-gate-parity.py) |
| 36 | Linter regression test suite | [`tools/run-linter-regression.py`](../tools/run-linter-regression.py) |
| 37 | Claude-rules local-copy sync audit | [`tools/lint-claude-rules-sync.py`](../tools/lint-claude-rules-sync.py) |
| 38 | Section placement audit | [`tools/lint-section-placement.py`](../tools/lint-section-placement.py) |
| 39 | Cross-file gate-count consistency audit | [`tools/lint-gate-count-consistency.py`](../tools/lint-gate-count-consistency.py) |
| 40 | Corpus version-bump-recency audit | [`tools/lint-version-bump-recency.py`](../tools/lint-version-bump-recency.py) |
| 41 | Collection-enumeration consistency audit | [`tools/lint-collection-enumeration-consistency.py`](../tools/lint-collection-enumeration-consistency.py) |
| 42 | External-overlay license consistency audit | [`tools/lint-external-overlay-license.py`](../tools/lint-external-overlay-license.py) |
| 43 | Follow-up ageing audit | [`tools/lint-followup-ageing.py`](../tools/lint-followup-ageing.py) |
| 44 | Paired-skill step-parity audit | [`tools/lint-paired-skill-step-parity.py`](../tools/lint-paired-skill-step-parity.py) |
| 45 | TODO staleness audit | [`tools/lint-todo-staleness.py`](../tools/lint-todo-staleness.py) |
| 46 | Overnight-work file audit | [`tools/lint-overnight-file.py`](../tools/lint-overnight-file.py) |
| 47 | Listing-surface completeness audit | [`tools/lint-listing-surface-completeness.py`](../tools/lint-listing-surface-completeness.py) |
| 48 | CSA CCM/AICM citation-accuracy audit | [`tools/lint-ccm-aicm-citations.py`](../tools/lint-ccm-aicm-citations.py) |

Most gates are pure read-only linters that exit non-zero on the first violation; the exceptions are gates 33 and 34 (generator-output drift checks), gate 35 (audit-programme self-check), gate 36 (linter regression test suite), gate 37 (Claude-rules local-copy sync drift check), and gate 40 (corpus version-bump-recency audit, which uses `git log` heuristics to compare per-file body-commit and Version-line-commit timestamps), described below. Gates 33 and 34 re-run the generator in `--check` mode and exit non-zero if the regenerated output differs from the committed artefact. Gate 35 is the audit programme's self-check: it parses this §6 inventory and confirms that the workflow, the local audit runner, and the pre-commit config declare the same gates with the same names and scripts in the same order. Gate 36 is the linter regression test suite: for each in-scope linter it constructs a synthetic markdown fixture that should trigger exactly one rule, invokes the linter against the fixture, and asserts the linter exits non-zero. The test suite catches a defect class no other gate can catch (a regression in a linter's own detection logic). Gate 37 is a drift check between the project-local `.claude/rules/` rule copies and their `dev-security/claude-rules/` pack sources: both trees are exempt from the corpus linters, so this is the only gate that catches a local copy (the file a Claude Code session loads as context) drifting from its source. It is logically akin to the generator-output drift checks (gates 33 and 34) but is placed last (paired with gates 38 and 39 below) so that adding it did not renumber the meta-gates above; it also verifies that every local rule file is covered by its source mapping, so a new un-mapped mirror fails rather than going silently unchecked. Gate 38 is a section-placement audit: it codifies the convention (surfaced by the corpus-wide section-ordering survey) that orientation sections appear in the top three `##` sections and that Licence and Version-history sections appear in the bottom three; the audit catches future drift mechanically without requiring per-doctype canonical-order codification. Gate 39 is a cross-file gate-count consistency audit: it parses the row count of this §6 inventory as the canonical gate count, then scans corpus markdown, Python, and shell sources for prose references to gate counts ("N-gate audit programme", "N audit gates", "gates 1-N", "all N gates", and similar idioms) and flags any whose captured N does not match the canonical. The audit catches the failure mode that surfaced when gate 38 was added: the §6 inventory was bumped but downstream prose in registers, procedures, and tooling continued to cite the prior gate count through multiple cleanup PRs. Gates 38, 39, and 40 are all appended at the tail (after gate 37) for the same reason gate 37 was: appending avoids renumbering the meta-gates above. Gate 47 is a listing-surface completeness audit: it reads the canonical active-document set from [`taxonomy.yml`](../taxonomy.yml) (itself kept in sync by gate 33) and verifies that the MECHANICAL listing surfaces enumerate every active document in their scope -- the document-index register ([`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md)) must list every domain-prefixed active document, and each domain README must reference every active document in its own domain. Root-level meta-specifications (`specification-*.md` at the repository root) are exempt from the register rule, which is documented in the linter: the register is organized by domain and has never indexed root-level meta-specs, which describe the library's own infrastructure rather than its GRC content. SEMANTIC listing surfaces (the framework matrices and crosswalks, the glossary and key-terms registers, per-document `Related Documents` fields) are intentionally not gated, because their inclusion rule is relevance-based and a hard gate would be noisy; the [`tools/suggest-listing-surfaces.py`](../tools/suggest-listing-surfaces.py) authoring helper emits high-recall candidates for those surfaces for a human to ratify. Gate 47 is appended at the tail for the same reason gates 38-40 were. Gate 48 is a CSA CCM/AICM citation-accuracy audit: it loads the authoritative control reference in [`tools/ccm_aicm_reference.py`](../tools/ccm_aicm_reference.py) (a fair-use citation index of domain codes, control-ID ranges, and canonical control titles derived from the CSA-published CCM v4.1.0 and AICM v1.1.0 catalogues, carrying none of those catalogues' normative content, so it is an index rather than a redistribution of the matrices) and checks two things across the corpus: that every `<DOMAIN>-<NN>` token whose domain is in the CCM/AICM family names a real domain and an in-range control number (catching superseded or fabricated domains such as `IVS` (renamed to `I&S` in v4.1.0), `GRM` (the v3.0.1 governance code), `GOV` and `NET` (which do not exist), and out-of-range control numbers, such as an `IPY` control above the domain's fourth), and that a control-listing table row (`| <CODE> | <title> |`) whose cited title shares no content word with the catalogue title is flagged as mis-attributed (a deliberately conservative check that tolerates the corpus's localized and abbreviated titles while catching fabricated ones). Corpus-internal control identifiers (`MODEL-GOV-NN`, `AI-GOV-NN`) and other frameworks' codes are not policed. Gate 48 is appended at the tail for the same reason gates 38-40 and 47 were.

Gate 40 is a corpus version-bump-recency audit: for each versioned document, it compares the SHA of the most-recent commit that touched the file at all against the SHA of the most-recent commit that modified a Version metadata line in the file, using `git log -G` pickaxe matching. If they differ, the file's body has changed since the last Version bump, and the gate fails. This is the corpus-side counterpart of delta gate D2 (per-PR version-bump check) in §6.1: D2 catches the failure mode at PR time using `git diff` between PR base and head; gate 40 catches it from HEAD using `git log` heuristics, covering the case where a body change reached `main` through any path (squash merge, direct push, batch commit) without an accompanying Version bump.

Gate 41 is a collection-enumeration consistency audit: for each declared "collection" of items (pack governance rules, pack skills, and similar groupings that appear in multiple places in the corpus), the gate compares the canonical source-of-truth (a directory listing) against the enumerations of that collection elsewhere in the corpus. If an item exists in the canonical source but is missing from an enumeration (or vice versa), the gate fails. The initial configuration ships with two hard-coded collections; a companion detector tool (`tools/detect-collection-candidates.py`, separate deliverable) surfaces additional candidate collections by heuristic scan for the maintainer to triage one-by-one.

Gate 42 is an external-overlay licence consistency audit: it walks each subdirectory of `.claude/rules/external/`, reads each subdirectory's LICENSE file, and verifies the licence identifier matches a hard-coded `EXPECTED_LICENSE` mapping (currently TikiTribe → MIT, Kariedo → MIT, addyosmani → MIT). It additionally walks the markdown files in each external subdirectory and fails if any contains the literal `**License:** CC BY-SA 4.0` claim, since external files retain their source project's licence rather than the project's own. The gate is the external-overlay counterpart of gate 15 (which enforces the project's own licence discipline on the corpus): together, the two gates close the licence-consistency loop across every file in the repository (project content or external overlay).

Gate 45 is a TODO staleness audit: it scans [`TODO.md`](../TODO.md) for two recurring drift patterns that surfaced across four consecutive validation sweeps (Sweep 10 iter 2, iter 3 close-out, iter 3 catch-back, Sweep 11 iter 1). First, the *queued-PR-already-merged* pattern: a line referencing `Next, PR #N` or `queued PR #N` for a PR whose merge commit appears in the current branch's git log. Second, the *sweep-cursor-behind-history* pattern: a `Last validation sweep: Sweep N iter M` line whose `(N, M)` tuple is older than the most-recent row in [`.working/validate-sweeps/history.md`](../.working/validate-sweeps/history.md). The gate deliberately does not enforce the version-snapshot field's currency: per the PR #127 convention amendment, that field is intentionally allowed to drift between session-pause and resume as PRs land. The gate complements the convention amendment by catching the two drift shapes that remained harder to tolerate after the convention reframe.

Gate 46 is an overnight-work file audit: it scans [`.working/overnight-pr.md`](../.working/overnight-pr.md) and verifies that the file's `**Status:**` field carries a value of `stub` (no overnight session is in flight) or `in-flight` (overnight session is active). Both states pass the gate. `done` causes a gate failure, signalling that an overnight session has ended but the next-morning processing PR has not yet routed the file's content into the appropriate working-state ledgers (design decisions to [`.working/design-decisions.md`](../.working/design-decisions.md), closed work to [`.working/DONE.md`](../.working/DONE.md), queued follow-ups to [`TODO.md`](../TODO.md)) and reset the file to the stub form. Other Status values or a missing Status field also fail. The gate codifies the overnight-work protocol defined in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md). The three-value Status field (rather than a binary "stub vs non-stub") preserves the overnight workflow: overnight PRs ship with `Status: in-flight` and pass CI; only after the session ends and Status flips to `done` does the gate flag the missing morning processing.

### 6.1 PR-only delta gates

A delta gate inspects the change set of a pull request, not the repository state at HEAD. Delta gates are not part of the corpus inventory above, because their inputs (git history range, PR base ref) are not available in [`tools/run_all_audits.sh`](../tools/run_all_audits.sh) or [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) and they are therefore exempt from gate 35's parity audit. Delta gates run only in [`.github/workflows/quality.yml`](../.github/workflows/quality.yml) on `pull_request` events.

| # | Gate | Script | Surface |
| --- | --- | --- | --- |
| D1 | CHANGELOG-on-PR check | [`tools/check-changelog-on-pr.py`](../tools/check-changelog-on-pr.py) | GitHub Actions (PR only) |
| D2 | Per-PR version-bump check | [`tools/check-version-bump-on-pr.py`](../tools/check-version-bump-on-pr.py) | GitHub Actions (PR only) |
| D3 | CHANGELOG dash-on-PR check | [`tools/check-changelog-dash-on-pr.py`](../tools/check-changelog-dash-on-pr.py) | GitHub Actions (PR only) |

Delta gate D1 mechanically enforces §7 step 4 below ("the CHANGELOG entry for the phase is written"): it compares the PR head to its merge-base with the target branch and fails when [`CHANGELOG.md`](../CHANGELOG.md) is not in the diff. As of PR #125 (2026-06-21), the gate enforces the project's two-file split convention: BOTH the root [`CHANGELOG.md`](../CHANGELOG.md) AND the detailed mirror at [`.working/changelog-details/CHANGELOG-detailed.md`](../.working/changelog-details/CHANGELOG-detailed.md) must be in the diff (lock-step); modifying one without the other fails the gate. An opt-out trailer `Changelog: <one-line-reason>` in any commit message body in the PR range satisfies the gate regardless of split, for cases where the convention legitimately does not apply (trivial typo corrections, branch-mechanics fixes, content already covered by a CHANGELOG entry from an earlier commit in the same PR).

Delta gate D2 enforces that every versioned document modified in a PR carries a bumped `**Version:**` field. For each markdown file in the diff, the gate reads the file's Version field at the merge-base and at the PR head and fails if the file's body changed but Version did not. Exempt files: [`CHANGELOG.md`](../CHANGELOG.md), generated artefacts, and files without a Version field. The gate catches the per-document-version-bump-omission class of defect that the §6 monotonicity audit (gate 13) cannot detect; gate 13 confirms versions strictly increase, but cannot detect a file whose body changed without an accompanying bump.

Delta gate D3 enforces the prose dash convention (no em dashes, no en dashes; see [`tools/lint-language.py`](../tools/lint-language.py)) on the root [`CHANGELOG.md`](../CHANGELOG.md), but only on lines a PR adds. The root CHANGELOG is deliberately outside `lint-language.py`'s whole-file scan set, because its long append-only entry history accumulated many em dashes before the convention was enforced and rewriting historical entries risks altering their meaning. D3 closes that gap forward-only: it compares the PR head to its merge-base, inspects the added CHANGELOG lines, and fails when any added line contains an em dash or en dash, so new entries follow the convention while history stays untouched. This is the new-entries-only resolution of deferred decision DD-1 (2026-06-23); the detailed mirror under `.working/` is maintainer working state and is not checked.

## 7. Phase-completion gating

A phase is complete when:

1. All file edits intended for the phase are written.
2. Auto-generated artefacts ([`taxonomy.yml`](../taxonomy.yml), [`docs/portal.md`](../docs/portal.md), [`docs/maturity-scorecard.md`](../docs/maturity-scorecard.md)) have been regenerated.
3. The full audit programme passes locally via [`tools/run_all_audits.sh`](../tools/run_all_audits.sh).
4. The CHANGELOG entry for the phase is written.
5. The library calendar version is bumped (and the README version where appropriate).
6. The change is committed and pushed; the pull request is opened.
7. CI's quality.yml workflow confirms green.
8. The pull request is merged and the local branch is fast-forwarded to the merged main.

Selective subset runs are not a substitute for the full sweep. Phase 23.30's lessons-learned decision in [`TODO.md`](../TODO.md) established this rule after the Phase Q-bundle merge introduced five gate violations that would have been caught by a full local sweep.

## 8. Audit programme failure handling

When an audit gate fails, the maintainer (or AI verifier) must:

1. **Read the failure message in full.** Each gate prints the offending file, line, and content.
2. **Locate the underlying cause.** Do not edit the linter to suppress the finding without first investigating whether the linter is correct.
3. **Choose between three responses:**
    1. **Fix the content.** This is the default response. The content is in violation of a documented rule; the content is corrected.
    2. **Extend the linter's exemption list.** Only when the content is correct and the rule does not apply (e.g., the [`tools/lint-citations.py`](../tools/lint-citations.py) `COBIT 2025` exemption granted to documents that *deliberately* discuss the hallucinated framework version as a warning). The exemption must name the file by relative posix path and is recorded inline next to the existing exemption set.
    3. **Modify the rule.** Only when the rule itself is wrong (e.g., the Phase 23.20 loosening of [`lint-required-sections.py`](../tools/lint-required-sections.py) to accept Purpose OR Scope OR Applicability OR Introduction OR Overview). Rule modifications require an entry in the CHANGELOG and a corresponding update to the linter's module docstring.

Bypassing a hook (`--no-verify`, `--no-gpg-sign`, etc.) is not a permitted response. If a hook fails, the underlying defect is fixed before commit, not bypassed.

## 9. Adding a new gate

A new gate is added when:

1. A class of defect is identified that current gates do not catch.
2. The defect is deterministically detectable from repository state without network access or third-party dependencies.
3. The signal-to-noise ratio of the proposed rule is acceptable (false-positive rate is empirically zero or near-zero on the current corpus, or the rule is scoped narrowly enough to track zero items in scaffold form).

The procedure for adding a gate:

1. Write the linter as `tools/lint-<feature>.py` (Python 3.11, stdlib only).
2. Confirm the linter exits 0 on the current corpus (zero false positives) or that its rule set is conservatively scaffolded.
3. Add the gate to [`.github/workflows/quality.yml`](../.github/workflows/quality.yml), [`tools/run_all_audits.sh`](../tools/run_all_audits.sh), [`.pre-commit-config.yaml`](../.pre-commit-config.yaml), and the §6 inventory table above.
4. Add the new gate's row to the §6 inventory; §5 places the gate in its functional category. The §6 inventory table is the canonical source of truth for the gate count.
5. Record the addition in the CHANGELOG under a new phase entry.

## 10. Modifying or retiring a gate

A gate is modified when its rule is found to be incorrect (Phase 23.20 pattern). The modification must include:

1. The corrected linter code.
2. A re-run of the full audit sweep to confirm no new violations surface.
3. A CHANGELOG entry naming the gate, the rule that changed, and the rationale.
4. An update to the linter's module docstring if the rule's substance changed.

A gate is retired when its rule is found to be unhelpful, dominated by another gate, or producing structural false positives that cannot be narrowed. Retirement requires an entry in [`TODO.md`](../TODO.md) Decisions log documenting the rationale, mirroring the Phase 21.4 Strict-Related-Documents-Reciprocity precedent.

## 11. Relationship to the Citation Verification Specification

The Audit Programme Specification and [`governance/specification-citation-verification.md`](specification-citation-verification.md) form a complementary pair:

| Concern | Governed by |
| --- | --- |
| Are the library's internal references, structure, naming, metadata, and language internally consistent? | Audit Programme Specification (this document) |
| Are the library's claims about external standards accurate against publisher canonical sources? | Citation Verification Specification |

Three of the gates sit at the boundary between the two programmes:

- [`tools/lint-citations.py`](../tools/lint-citations.py) (gate 5) detects literal-string drift on external framework versions (for example, the canonical "COBIT 2025" hallucination warning). Its substance is a claim about the world (what version of COBIT is current), which derives from the Citation Verification Specification; its mechanism is deterministic repository-state pattern matching, which is the audit programme.
- [`tools/lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py) (gate 27) and [`tools/lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py) (gate 28) enforce the freshness cadences (12-month for canonical citations, 6-month for active tooling, 12-month for archived tooling) defined in Citation Verification Specification §12.

These three gates are determined automatically from repository state (so they belong to this programme) but enforce semantics defined in the Citation Verification Specification (so their substance derives from there).

When the two specifications conflict, the Citation Verification Specification governs the *substance* of what counts as "verified" and "fresh"; this specification governs the *enforcement mechanism* by which that substance is checked at every change.

## 12. Out-of-scope acknowledgements

The audit programme does not, and cannot, detect:

- **Substantive correctness of content.** A linter cannot detect that a paragraph asserts something untrue about the world; that is the domain of human review and (for external claims) the Citation Verification Specification.
- **Architectural coherence.** Whether a new document is well-placed in the library's information architecture is a human judgement, not a machine-detectable property.
- **Semantic duplication.** Two documents that say the same thing in different words pass every gate; identifying such duplication is part of the manual review cadence.
- **Adopter usefulness.** Whether a document is actually useful to a downstream adopter is not testable from repository state alone.

These limitations are not defects in the audit programme; they are the natural boundary at which automated quality gates stop and human judgement begins. The audit programme is a necessary but not sufficient condition for library quality.

## 13. Framework alignment

The audit programme contributes to control objectives in the following frameworks (cross-referenced for adopter convenience, not authoritative attribution):

- **ISO/IEC 27001 Annex A.5.1 (policies for information security)**: documented quality controls over governance artefacts.
- **NIST CSF 2.0 GV.OC (organisational context)**: documented internal consistency mechanisms.
- **COBIT 2019 BAI06 (managed changes)**: pre-commit and pre-merge gating preventing unreviewed changes.
- **SSDF PO.3.2 (deploy required tools for the secure development environment)**: pre-commit hooks and CI enforcement of repository quality.

These mappings illustrate where automated audit-programme work touches recognized frameworks; they do not claim equivalence.

---

**End of Document**
