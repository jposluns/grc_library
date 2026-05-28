# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The changelog records phase-level changes, not per-document version bumps.

## Phase 9.1 (2026-05-28): privacy templates, registers, framework, and standard

Closes eight long-standing privacy content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- `privacy/template-record-of-processing-activities.md`: GDPR Article 30 ROPA template with controller and processor views.
- `privacy/template-privacy-notice.md`: twelve required content blocks satisfying GDPR Articles 13 and 14, UK GDPR, LGPD, CPPA, PIPL, CCPA, and equivalents; just-in-time variant included.
- `privacy/template-dsar-workflow.md`: seven-stage DSAR lifecycle with identity verification trust levels, twenty-one-field request record schema, and six operational metrics.
- `privacy/framework-consent-management.md`: consent capture, validity standard, granularity rules, withdrawal, refresh and expiry conditions, ePrivacy and cookie consent alignment.
- `privacy/register-automated-decision-making.md`: ADM and profiling register schema, registration triggers, coordination with the AI System Register.
- `privacy/register-cookie-and-tracker.md`: seven-category tracker taxonomy, eighteen-field schema, quarterly-scan operating expectation, dark-pattern prohibitions.
- `privacy/standard-pseudonymisation-and-anonymisation.md`: permitted techniques including k-anonymity (k at minimum 5), l-diversity, t-closeness, differential privacy, synthetic data; five-tier residual-risk classification.
- `privacy/framework-childrens-data.md`: per-jurisdiction age thresholds, age-assurance approaches, parental consent verification, ten design defaults, profiling and ADM restrictions.

Document index `governance/register-document-index-and-classification.md` bumped 1.9.0 to 1.10.0 (minor: eight substantive new rows). Privacy README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 8 (2026-05-28): operational usefulness uplift

- `resilience/procedure-cross-domain-incident-coordination.md` expanded from 92 to 264 lines: domain ownership decision rule, joint command structure, coordination lifecycle, five hand-off checklists, severity rules across streams, joint decision log, cross-stream evidence handling, communication boundaries, joint post-incident review, joint exercises, metrics. Version 1.0.1 to 1.1.0 (minor).
- Tool acceptance criteria sections added with six-column purpose/output/integration/success/escalation tables:
  - `dev-security/standard-software-composition-analysis.md` §8 (ten criteria). Version 1.0.0 to 1.1.0 (minor).
  - `ai/guide-ai-adversarial-test-reference.md` Red team methodology subsection (PyRIT, Garak, promptfoo, manual practitioner). Version 1.2.2 to 1.3.0 (minor).
  - `ai/guide-ai-security-technical-implementation.md` §A7 (SAST, prompt regression, LLM scanner, AI red team automation, cloud guardrails, AI-aware monitoring). Version 1.2.1 to 1.3.0 (minor).
- Targeted measurable-verb pass on three Standards in `operations/`, `security/`, `dev-security/`. Defensible conditional usage left intact.
- `tools/build-portal.py`: generates `docs/portal.md` (audience-keyed navigation) and `docs/maturity-scorecard.md` (per-document maturity classification) from `taxonomy.yml`. Wired into CI and pre-commit.
- Phase 8.5 (per-document adoption notes) deliberately deferred; `docs/worked-example.md` already covers end-to-end adaptation.

## Phase 7 (2026-05-28): machine-readable taxonomy and reverse framework crosswalk

- `tools/build-taxonomy.py`: generates `taxonomy.yml` from canonical metadata of every active artefact (3,690+ lines). `--check` mode wired into CI and pre-commit.
- `governance/matrix-reverse-framework-control-crosswalk.md` (v0.0.1): inverts the forward matrix to answer "given an external control identifier, which library documents address it". Coverage: ISO 27001:2022 Annex A, ISO 42001:2023, NIST CSF 2.0, NIST SP 800-53 Rev 5, NIST AI RMF, CSA CCM v5, EU AI Act, GDPR / UK GDPR, DORA, NIS 2, OWASP LLM Top 10, MITRE ATLAS, CTPAT MSC, BASC v6, WCO SAFE.
- `governance/matrix-cross-framework-alignment.md` updated to cross-reference the reverse matrix; pair-consistent.
- Document index `governance/register-document-index-and-classification.md` bumped 1.8.6 to 1.9.0 (minor: substantive new index row for the reverse crosswalk).

## Phase 6 (2026-05-28): automation, validation, repository hygiene

- Three new audit scripts added: `tools/lint-metadata.py` (13-field canonical metadata block, allowed types, semver, ISO 8601 dates, role-based ownership, License field, repository-path consistency, filename prefix), `tools/lint-links.py` (every relative markdown link resolves), `tools/lint-structure.py` (every active file appears in its domain README and in the document index, and every reference resolves). These complement `tools/lint-language.py` from Phase 5.
- `.github/workflows/quality.yml`: GitHub Actions workflow running all four audits on push to `main` and on every pull request.
- `.pre-commit-config.yaml`: local hooks wiring the same audits.
- Repository hygiene files: `CONTRIBUTING.md` (contribution workflow, metadata rules, style rules, filename rules), `SECURITY.md` (how to report content accuracy defects, CC0 licence concerns, organisation or personal data leakage, broken external links, and tooling defects), `CHANGELOG.md` (this file), `docs/adopter-guide.md` (fork and adapt walkthrough), `docs/worked-example.md` (end-to-end draft-to-CC0-artefact walkthrough).
- Conformance bugs surfaced by the new auditors fixed: three compliance files with plain-text Repository Path links converted to canonical markdown links, one risk template misclassified as Register corrected to Template, master specification gained the four missing canonical metadata fields, twenty-five privacy jurisdiction annexes had a broken self-folder reference repaired, two domain READMEs and one index row reconciled. All version increments patch.

## Phase 5 (2026-05-28): heading style normalisation, language audit, lint tooling

Normalises section heading case across the corpus (24 lettered subsections in `ai/guide-ai-security-technical-implementation.md`, 5 in `ai/guide-ai-adversarial-test-reference.md`, and the `Step N:` and `Category N:` patterns in 17 procedure / guideline / plan / register files). Codifies the sentence-case rule and other language conventions in both specifications. Introduces `tools/lint-language.py`.

## Phase 4 (2026-05-28): near-duplicate reconciliation

Retires the older, weaker governance-domain policy in favour of the newer risk-domain policy as the canonical enterprise governance and risk management policy. Migrates the control-area mapping table into `governance/matrix-cross-framework-alignment.md`. Retires the governance-domain supplier security and privacy assurance procedure; migrates its metrics block into the supply-chain Standard. 37 inbound references redirected; 2 files deleted; 40+ files modified.

## Phase 3 (2026-05-28): duplicate filename resolution

Three duplicate-filename pairs resolved. Renames preserve git history.

- `security/procedure-incident-response.md` and `resilience/procedure-incident-response.md` renamed to `security/procedure-security-incident-response.md` and `resilience/procedure-cross-domain-incident-coordination.md`. The resilience procedure refocused as the cross-domain coordination layer that delegates technical IR to the security procedure.
- `privacy/procedure-data-protection-and-privacy-breach-response.md` and `resilience/procedure-data-protection-and-privacy-breach-response.md` consolidated: AI-specific assessment block migrated into a new section 4.3 of the privacy procedure; resilience-domain duplicate deleted.
- `compliance/register-ctpat-compliance-controls.md` and `supply-chain/register-ctpat-compliance-controls.md` renamed to `compliance/register-ctpat-it-controls.md` and `supply-chain/register-ctpat-full-msc-controls.md` to make their distinct scopes explicit.

## Phase 2 (2026-05-28): filename, type, and cross-reference reconciliation

Brings every file into compliance with the now-expanded specification. Two files renamed via `git mv` to add correct type prefixes (`plan-` and `template-`). Seven files reclassified to their canonical Document Type. Three references to the superseded `privacy/annex-regional-privacy-requirements.md` redirected to `privacy/annex-privacy-jurisdiction-index.md`. Microsoft PyRIT references rewritten under open-source framing. 12 inbound references updated.

## Phase 1 (2026-05-28): document-type expansion

Adds Standard Operating Procedure (SOP), Roadmap, and Guide to the controlled vocabulary of allowed document types. Removes the prior prohibition on SOP. Adds type-selection guidance distinguishing Procedure from SOP, Plan from Roadmap, and Guideline from Guide. Repairs the document hierarchy tables in the governance charter and the document architecture framework which were previously missing Specification, Annex, and Checklist.

## Earlier history (before 2026-05-28)

Repository established as a public-domain CC0 GRC documentation library. Initial corpus included approximately 200 documents across ten domains: AI governance, compliance, developer security, governance, operations, privacy (with a 26-jurisdiction subfolder), resilience, risk, security, and supply chain. The earlier history is preserved in the git log; this changelog adopts phase-level granularity starting from 2026-05-28.
