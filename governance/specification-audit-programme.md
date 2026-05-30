# Audit Programme Specification

**Document Title:** Audit Programme Specification\
**Document Type:** Specification\
**Version:** 1.0.1\
**Date:** 2026-05-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/charter-governance-library.md`](charter-governance-library.md), [`CHANGELOG.md`](../CHANGELOG.md), [`TODO.md`](../TODO.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual, and upon addition or removal of any audit gate\
**Repository Path:** [`governance/specification-audit-programme.md`](specification-audit-programme.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## 1. Purpose

This specification defines the GRC Documentation Library's automated audit programme: the set of machine-checked rules that gate every change to the library, the mechanisms by which the rules are enforced, the surfaces on which they run, and the conditions under which gates are added, modified, or retired.

The audit programme is the library's primary defence against the failure modes catalogued in [`governance/specification-citation-verification.md`](specification-citation-verification.md) §5: drift, contradiction, mis-attribution, stale references, and silent regressions in document structure, naming, and cross-linkage. Where the Citation Verification Specification governs *what is true about the world* (publisher metadata about external standards), this specification governs *what is internally consistent about the library itself*.

## 2. Scope

### 2.1 In scope

- The 30 audit gates currently wired into the audit-programme (see §6).
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

The gates fall into seven functional categories:

1. **Metadata integrity** (gates 1, 7, 8, 13, 14, 15, 16, 19): canonical metadata block presence and field validity; doctype-to-filename alignment; Owner and Approving Authority field validity against the role register; date format; license value; document-stub detection; required sections per doctype; version monotonicity.
2. **Reference integrity** (gates 3, 11, 17, 18, 24, 26): intra-repo links resolve; CHANGELOG file-reference link coverage; section anchors resolve; intra-document section references resolve; external-link domains on allow-list; orphan documents have at least one inbound reference.
3. **Content drift defence** (gates 5, 6, 25): external framework hallucinations; standards currency; cross-document numerical coherence.
4. **Language and style** (gates 2, 9, 20): em-dashes, "ize/ization" Americanisms, "ensure that", sanitisation neologisms; mandatory requirements near uncertainty markers; acronym expansion consistency against the glossary.
5. **Structural index** (gate 4): repository-wide index integrity.
6. **Security and privacy** (gates 12, 21, 22, 23): placeholder leakage, secret patterns, PII patterns, internal-environment leakage (cloud regions, hostnames, deployment identifiers).
7. **Freshness and lifecycle** (gates 10, 27, 28, 29, 30): document review cadence, citation-verification freshness, tooling-provenance freshness, auto-generated taxonomy and portal/scorecard sync.

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
| 29 | Machine-readable taxonomy in sync | [`tools/build-taxonomy.py`](../tools/build-taxonomy.py) |
| 30 | Adopter portal and maturity scorecard in sync | [`tools/build-portal.py`](../tools/build-portal.py) |

Gates 1 through 28 are pure read-only linters that exit non-zero on the first violation. Gates 29 and 30 are generator-output drift checks: they re-run the generator in `--check` mode and exit non-zero if the regenerated output differs from the committed artefact.

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
    3. **Modify the rule.** Only when the rule itself is wrong (e.g., the Phase 23.20 loosening of `lint-required-sections.py` to accept Purpose OR Scope OR Applicability OR Introduction OR Overview). Rule modifications require an entry in the CHANGELOG and a corresponding update to the linter's module docstring.

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
4. Add the new gate's row to the §6 inventory and update the gate count in §2.1; §5 places the gate in its functional category. The §6 inventory table is the canonical source of truth for the gate count.
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

- **ISO/IEC 27001 A.5.1 (policies for information security)**: documented quality controls over governance artefacts.
- **NIST CSF 2.0 GV.OC (organisational context)**: documented internal consistency mechanisms.
- **COBIT 2019 BAI06 (managed changes)**: pre-commit and pre-merge gating preventing unreviewed changes.
- **SSDF PO.3.2 (deploy required tools for the secure development environment)**: pre-commit hooks and CI enforcement of repository quality.

These mappings illustrate where automated audit-programme work touches recognized frameworks; they do not claim equivalence.

---

**End of Document**
