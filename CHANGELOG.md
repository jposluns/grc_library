# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The changelog records phase-level changes, not per-document version bumps.

## Phase 9.4 (2026-05-28): supply chain (5 new documents)

Closes five supply-chain content gaps identified in the advisory review.

- `supply-chain/procedure-fourth-party-and-nth-party-risk.md`: tiered visibility expectations (T1 fourth-party plus selected nth-party; T2 material fourth-party; T3 sub-processor only); six-step procedure (identify, assess, monitor, escalate, treat, record).
- `supply-chain/register-concentration-risk.md`: six concentration dimensions (service-class, shared sub-tier, geographical, jurisdiction, vendor-family, intra-group); register schema with treatment options; coordination with the critical-ICT-third-party regime.
- `supply-chain/register-sbom.md`: three SBOM acquisition paths (build-time, supplier-provided, post-deployment); register schema with CycloneDX / SPDX / VEX support; linkage to vulnerability management and acceptance gates; customer transparency under EU CRA and EO 14028.
- `supply-chain/template-supplier-offboarding-evidence.md`: eight-section offboarding record covering relationship identification, access revocation (ten access types), data return and destruction (eight categories), service-continuity handover, residual obligations (ten obligation types), contract closure, post-exit review, approval set.
- `supply-chain/standard-supplier-resilience-monitoring.md`: five signal categories (continuity testing, incident, financial-health, control and assurance, external-environment); tier-based monitoring posture; signal source diversity; coordination with the concentration register and the critical-ICT-third-party regime.

Document index `governance/register-document-index-and-classification.md` bumped 1.12.0 to 1.13.0 (minor: five substantive new rows). Supply-chain README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion).

## Phase 9.3 (2026-05-28): resilience templates and plans

Closes five resilience content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- `resilience/template-tabletop-exercise.md`: scenario design, scenario library (eight classes from ransomware to crisis convergence), objectives, participants, format options, inject schedule template, six-criterion evaluation rubric, after-action report structure.
- `resilience/template-recovery-runbook.md`: per-system runbook with ten sections (system identification, dependencies, detection and declaration, pre-recovery checks, recovery steps, validation, communications, rollback, closure and learning, test history).
- `resilience/template-lessons-learned.md`: cross-stream lessons-learned report with eleven sections (event identification, executive summary, timeline reconstruction, root cause and contributing factors, what worked, gaps identified across twelve categories, corrective actions, procedure and control changes, communication of lessons, metric impact, approval).
- `resilience/plan-pandemic-continuity.md`: five-stage activation model (Monitor, Prepare, Activate, Sustained operations, Recovery), workforce health, remote-work scaling, essential-service prioritisation, supplier and supply-chain impact, facility and operational adjustments, communications, deactivation and recovery.
- `resilience/plan-physical-site-continuity.md`: four-posture model (Protective actions, Partial operations on site, Site closed, Restoration), activation criteria, protective actions (deferring to the emergency response guideline), alternate-site activation (ten-step procedure), restoration and return, workforce well-being.

Document index `governance/register-document-index-and-classification.md` bumped 1.11.0 to 1.12.0 (minor: five substantive new rows). Resilience README bumped 1.1.1 to 1.2.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.2 (2026-05-28): compliance sector and regime expansion

Closes seven sector and regime content gaps identified in the advisory review. Each new annex starts at version 0.0.1 per the ingestion specification.

- `compliance/annex-fedramp-requirements.md`: applicability triggers, authorisation route selection (JAB, Agency, FedRAMP Tailored, FedRAMP Ready), baseline selection mapped to FIPS 199, library coverage per NIST SP 800-53 Rev 5 control family, eight named library gaps requiring additional documentation (SSP, ConMon, POA&M, SAR/SAP, OMB M-22-09 reporting, FIPS-validated cryptography, federal personnel investigations, CUI handling).
- `compliance/annex-dora-implementation.md`: per-pillar mapping for ICT risk management (Articles 5 to 16), ICT-related incident reporting (Articles 17 to 23 with 4-hour, 72-hour, one-month windows), digital operational resilience testing including TLPT under TIBER-EU, ICT third-party risk including Article 30 minimum clauses and the critical-ICT-third-party Oversight Framework, information and intelligence sharing.
- `compliance/annex-nis-2-implementation.md`: entity classification (Essential and Important under Annexes I and II), per-sub-measure mapping of Article 21 risk-management measures, Article 20 management body responsibilities and training, the four-stage incident reporting regime under Articles 23 to 25 (early warning, incident notification, intermediate, final), six library gaps requiring additional documentation.
- `compliance/annex-public-sector-requirements.md`: eight overlay areas (freedom of information, accessibility under WCAG 2.2 AA and EN 301 549, public procurement, records management, audit and external scrutiny, ethics and lobbying, AI in the public sector, official languages), library coverage per overlay, seven library gaps.
- `compliance/annex-telecommunications-sector-requirements.md`: seven overlay areas (sector cybersecurity, lawful interception, data retention, sector customer privacy, emergency calling and resilience, vendor and supply-chain restrictions, numbering and addressing resources), regime references for EU EECC, EU NIS 2, UK Telecommunications (Security) Act 2021, US CALEA, FCC, and equivalents.
- `compliance/annex-energy-and-utilities-sector-requirements.md`: six overlay areas (critical-infrastructure cybersecurity baselines, OT and ICS cybersecurity, physical-cyber convergence, sector incident reporting, supplier and component security, resilience and continuity), per-control area mapping for OT including network segmentation, OT vulnerability management, vendor remote access to OT, OT incident response.
- `compliance/annex-sox-itgc.md`: ICFR scope determination, four ITGC domains (access to programs and data, program changes, program development, computer operations) with library coverage per control objective, auditor-expected artefacts beyond the library, coordination with adjacent regimes (SOC 1, PCI DSS, GDPR, NIST CSF, ISO 27001).

Document index `governance/register-document-index-and-classification.md` bumped 1.10.0 to 1.11.0 (minor: seven substantive new rows). Compliance README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Drift fixes (2026-05-28): repository structure documentation and AI ingestion instruction refresh

A post-Phase-9.1 drift audit identified six stale items in the meta files that had fallen out of sync with the repository state during Phases 1, 6, 7, and 9.1. Fixed in this commit:

- `README.md`: Repository structure block now lists the infrastructure directories (`tools/`, `docs/`, `.github/`, `taxonomy.yml`, hygiene files). Document count claim refreshed from approximately 200 to approximately 215. Core reference set table expanded with three privacy templates (ROPA, privacy notice, DSAR workflow) added in Phase 9.1. Version 1.4.2 to 1.5.0 (minor).
- `specification-master-project.md`: Section 4 expanded to distinguish governance-artefact directories from repository infrastructure directories. Version 1.2.2 to 1.2.3 (patch).
- `specification-ingestion.md`: Repository domains section gained a note enumerating the infrastructure paths that are out of scope for ingestion and exempt from the structural audit. Version 1.4.1 to 1.4.2 (patch).
- `instruction-ai-document-ingestion.md`: refreshed end to end. Now references the current 16-type vocabulary, the type-selection guidance, the audit scripts, the taxonomy and portal generators, the CHANGELOG update obligation, and the rules for retiring or superseding documents.
- `tools/lint-language.py`: added the AI ingestion instruction file to the exempt list for the self-referential `ensure` rule, consistent with the existing exemptions for both specifications.

The convention going forward is to update CHANGELOG.md in the same commit as the substantive phase change.

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
