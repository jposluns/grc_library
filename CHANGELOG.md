# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The changelog records phase-level changes, not per-document version bumps.

## Phase 19.3 (2026-05-28): Role authority register completions

Phase 19 sub-phase 3. Two high-severity findings from the exhaustive re-audit: documents named "AI Security Maintainer" as Owner or Approving Authority on 10+ files but the role had no definition in the authoritative register (it was only suppressed via a linter exemption); documents named "Board Risk Committee" and "Enterprise Risk Committee (ERC)" as approval bodies but the register had no entry for either.

### Changes

- `governance/register-role-authority.md` (1.2.0 → 1.3.0): added three new authority-register entries — AI Security Maintainer (with explicit demarcation from CISO and AI Governance Approver), Board Risk Committee (board-level risk-appetite oversight, with consolidation pointer to the minimum-viable governance guideline), and Enterprise Risk Committee / ERC (executive-level forum delegated by the Board Risk Committee).
- `tools/lint-roles.py`: removed the AI Security Maintainer linter exemption because the role is now in the register itself; known-role count rose from 40 to 42.

### Result

The library's authoritative role definitions now match its actual role usage. Linter exemptions no longer mask undefined roles. Adopters reading the role authority register get the complete set of roles the library references, with explicit demarcation where roles could be confused.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.2 (2026-05-28): Sanitisation residue cleanup

Phase 19 sub-phase 2. Three findings from the exhaustive re-audit involved content that revealed the original drafting organisation's specific operating context where a CC0-licensed reusable template should use generic placeholder phrasing.

### Files updated

- `privacy/register-cross-border-data-flow.md` (1.0.0 → 1.0.1): the Data Residency example column referenced "US East data centre", a specific cloud region tied to one organisation's deployment. Replaced with the generic placeholder "Cloud region in destination country (specify provider and region)" so adopters fill in their own residency without first having to overwrite a residual example.
- `supply-chain/template-supplier-security-questionnaire.md` (1.0.0 → 1.0.1): five question rows used "our organisation" / "our data" / "our personal data" — first-person pronouns that read as residue from a specific organisation's internal version of the questionnaire. The document's own Purpose section already uses the formulation "the Organisation"; questions 1.5, 1.6, 7.4, 8.3, 9.1, and 9.5 are now consistent with that convention. Sample notification text in `register-subprocessor-template.md` was deliberately left in first person because the "we/our" appears inside a quoted email body the organisation sends to its customers — first-person pronouns are correct in that quoted speech.

### Result

Adopters cloning the library no longer encounter a specific cloud-region example or first-person "our organisation" phrasing in templates intended to be filled in or issued from the adopter's own organisational context.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.1 (2026-05-28): BASC migration completion

Phase 19 sub-phase 1. The Phase 12.3 sector annex migration (in which BASC was moved from being treated as an organisation-wide baseline standard to being a sector overlay invoked only where the organisation participates in the BASC programme) was incomplete: four active documents retained content that scoped the organisation to BASC, named "Regional Compliance Officers" as a baseline role, or aligned the document's own framework table to BASC/WCO SAFE/ISO 28000 unconditionally. Phase 19.1 cleans that residue.

### Files updated

- `operations/standard-network-security-and-segmentation.md` (1.3.0 → 1.4.0): removed BASC/Latin America scoping, the "BASC / Logistics" network zone row, the dedicated "BASC trade-network security controls" section, and the unconditional BASC/WCO SAFE/ISO 28000 framework rows; sector overlays now invoked via `sectors/` pointers throughout. Also generalised "prior ransomware incident" references to industry-experience phrasing.
- `supply-chain/procedure-supplier-due-diligence.md` (1.0.1 → 1.1.0): removed BASC from baseline framework alignment statement, baseline security-certification list, and References section; removed "Regional Compliance Officers" governance row; converted "BASC Compliance" evidence row, "BASC and regional compliance integration" step, contractual review clauses, and re-audit triggers to sector-conditional formulations.
- `resilience/plan-it-disaster-recovery.md` (1.1.0 → 1.2.0): generalised the Purpose paragraph that referenced "a prior security incident" requiring "approximately a 30-day phased recovery" to industry-experience phrasing about phased recovery from major security incidents, since adopting organisations must calibrate RTO/RPO, tier assignments, and phasing to their own incident history and risk appetite rather than to the original drafting organisation's history.
- `governance/standard-records-retention-and-destruction.md` (1.3.0 → 1.4.0): removed BASC/Latin America scope item content, "Regional Compliance Officers" governance row, the "BASC Trade and Customs" retention row, and the unconditional BASC/WCO SAFE framework alignment rows; sector overlays now invoked via `sectors/` pointers throughout.

### Result

The four documents that still implicitly assumed BASC participation now read consistently with the sector-overlay pattern established in Phase 12.3: BASC appears only as an illustrative example of "a sector programme an organisation may participate in", parallel with CTPAT, AEO, PIP, HIPAA, and financial-services overlays.

Taxonomy regenerated. All ten audits clean.

## Phase 18 (2026-05-28): BrE/AmE spelling normalisation

Resolves the final editorial finding from the next-passes list (item 1.1). The library now uses consistent Oxford English (BrE word stems + -ize verb endings) throughout active content.

### Conversion applied

`organization*` → `organisation*` across active content (713 replacements across 191 files), preserving 18 proper-noun occurrences (World Customs Organization, International Maritime Organization, International Civil Aviation Organization, ISO's full title "International Organization for Standardization", and COBIT 2019 process names containing "Organizational").

### Library posture

The library now consistently uses Oxford English: BrE word stems (organisation, behaviour, centre, labelling, programme, colour, favour, honour) with -ize verb endings (organize, recognize, prioritize, etc.). The language linter continues to enforce the -ize ending convention and now benefits from the consistent BrE word stems.

### Not converted

- `license` (verb and noun) and the LICENSE file: GitHub convention; metadata field name; left as-is.
- `program` (technical contexts): the library already uses `programme` consistently in governance/operational contexts.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 17 (2026-05-28): Adopter-facing content

Adds the adopter-facing content identified by the next-passes list. Closes items 5.2 (decision tree), 5.3 (maturity progression), 5.5 (library health report template), and 5.6 (content feedback channel).

### Adopter guide enhancements

`docs/adopter-guide.md`: two new substantial sections added.

- **Applicability decision tree**: a table of yes/no questions mapping organisational characteristics (handles personal data? operates AI? cloud workloads? customer-facing services? BASC certification? sector regulation?) to the library domains and sector annexes that apply. Enables adopters to quickly determine which subset of the library is relevant to their operating context.
- **Maturity progression**: explicit guidance keyed to the three tiers from the minimum-viable governance structure guideline. Tier 1 starter set lists 15 specific documents to adopt first; Tier 2 growth set adds the next layer; Tier 3 enterprise set adopts the full library. Each tier maps to the corresponding governance forum structure.
- **Sectors directory note**: brief sub-section noting that most organisations will skip `/sectors/` entirely.

### New artefact

- `governance/template-library-health-report.md` (v0.0.1): eleven-section template for the quarterly library health report referenced (but previously not templated) by the Phase 11 library quality and review cadence procedure. Sections cover identification, executive summary, the ten-audit status table, content additions and retirements, review cadence state, drift hot-spots, incidents and lessons, contributor activity, adopter signal, next-period plan, and sign-off. Worked example fragment included.

### Content feedback channel

- `CONTRIBUTING.md`: new "Reporting content issues without contributing a fix" section. Defines six issue categories (factual error, cross-document inconsistency, sanitisation residue, ambiguous responsibility, unsafe guidance, operational unrealism). Provides a non-PR channel for readers to raise concerns. Security-related defects continue to route through `SECURITY.md`.

### Registry updates

- `governance/README.md` (v1.2.0 → v1.3.0): new template added.
- `governance/register-document-index-and-classification.md` (v1.23.0 → v1.24.0): new row.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 16 (2026-05-28): CCM v4.1 domain code corrections

Resolves four CCM domain-code findings surfaced by the Phase 15 citation deep-dive. The Phase 12.1 corrective pass fixed the version string ("CSA CCM v5" → "CSA CCM v4.1") but did not migrate the v3-era domain codes that CSA renamed during the v3 → v4 transition. Three documents also used a domain code (TIM) that has never existed in any CCM version.

### Domain code corrections

Primary CSA sources (Cloud Controls Matrix and CAIQ v4.1 artifact; CCM v4.1 transition blog; CSF Tools CCM v4 reference) confirm the CCM v4.1 has exactly 17 domains: AIS, AAC, BCR, CCC, CEK, DCS, DSP, GRC, HRS, IAM, IPY, IVS, LOG, SEF, STA, TVM, UEM. The library used four codes that do not appear in this list:

| Stale code | Corrected to | Rationale |
| --- | --- | --- |
| GRM (Governance and Risk Management) | GRC (Governance, Risk, Compliance) | Renamed in v3 → v4 transition |
| EKM (Encryption and Key Management) | CEK (Cryptography, Encryption, Key Management) | Renamed and broadened in v3 → v4 transition |
| END (Endpoint Security) | UEM (Universal Endpoint Management) | Renamed and re-scoped in v3 → v4 transition |
| TIM (Threat Intelligence Management) | TVM (Threat and Vulnerability Management) | TIM never existed in any CCM version; threat intelligence is part of TVM |

### Replacements applied

25 replacements across 10 files. Specific numeric controls (GRM-12 → GRC-12, EKM-01 → CEK-01, etc.) substituted where the v3 control numbering plausibly maps to the v4 domain code with the same numeric sequence. TIM references — for which no number mapping is sound because the domain did not exist — rewritten to generic TVM domain references rather than swapping the prefix.

Affected files: `governance/policy-exception-and-risk-acceptance-management.md`, `governance/register-document-index-and-classification.md`, `risk/procedure-risk-assessment-methodology.md`, `security/policy-encryption-and-key-management.md`, `security/procedure-cryptographic-key-operations.md`, `security/procedure-key-escrow-and-recovery.md`, `security/framework-cryptographic-key-lifecycle.md`, `operations/standard-certificate-authority-management.md`, `operations/procedure-threat-intelligence-and-siem-operations.md`, plus the framework alignment annotations on a small number of other files.

### Citation denylist extended

`tools/lint-citations.py` extended with four new denylist entries (`CCM GRM`, `CCM EKM`, `CCM END`, `CCM TIM`) so the v3-era codes cannot be reintroduced silently.

### Not corrected (verified accurate)

- **CSA AICM v1.0.3**: confirmed real by CSA's official AICM artifact page. The Phase 15 audit flagged this as suspect; primary-source verification confirms the patch version is current. No change.
- **SEF-01 to SEF-10**: source evidence is ambiguous (some sources say 8 SEF controls, others say 10). Leaving the library's SEF-01 to SEF-10 reference unchanged pending unambiguous primary-source confirmation.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 15 (2026-05-28): Minimum-viable governance structure guideline

Resolves the forum-proliferation audit finding by adding a new adopter-facing guideline that shows how the library's 13+ named forums can be implemented at three maturity tiers (minimum viable, mid-market, enterprise / regulated). The library's individual documents continue to reference the formal forum names; this guideline shows the consolidation patterns that preserve the responsibilities for smaller adopters.

### New document

- `governance/guideline-minimum-viable-governance-structure.md` (v0.0.1): three-tier structure (Tier 1: 2-3 forums; Tier 2: 4-6 forums; Tier 3: 8-12 forums) mapping the library's formal forum names to consolidated bodies. Per-tier consolidation table, seat-name mapping by role group (senior executive, AI sub-roles, ownership, maintainer), and mapping-document worked example.

### Registry updates

- `governance/README.md` (v1.1.0 → v1.2.0): new guideline added to active documents.
- `governance/register-document-index-and-classification.md` (v1.22.0 → v1.23.0): new row added.

Taxonomy, portal, and maturity scorecard regenerated.

A separate (in-flight) citation verification deep-dive is running for items 7.1-7.4 of the next-passes list; any resulting corrections will be applied in a future phase.

## Phase 14 (2026-05-28): Provisional-draft and ownership cleanup

Resolves three lingering status-uncertainty items and tightens AIGC ownership clarity.

### Provisional-draft banners removed

Three documents previously carried "Document Status: Provisional" banners with "Target formal review: Q3 2026" framing. The banners over-claimed uncertainty against the library's posture (every active document is intended as public-domain reference baseline). Removed; the substantive Limitations sections in each document remain.

- `resilience/plan-it-disaster-recovery.md` (v1.0.0 → v1.1.0): banner removed.
- `supply-chain/standard-cloud-exit-and-data-portability.md` (v1.0.0 → v1.1.0): banner removed.
- `security/sop-incident-escalation-matrix.md` (v1.1.0 → v1.2.0): banner removed.

### AIGC ownership reconciliation

`ai/charter-ai-governance-council.md` (v1.1.0 → v1.2.0): new "Roles outside the council that report into it" sub-section in the Composition section. Documents how the three Phase 12.8 sub-roles (AI Governance Approver, AI Data Steward, AI System Inventory Keeper) report into the council via the AI Governance Lead secretariat. Charter administrative ownership (CIO), governance decisions (Council), and per-system approvals (Approver under delegated council authority) are explicitly disambiguated.

### Material change cross-references

Three operational triggers that say "material change" without specifying thresholds now point at the authoritative thresholds table:

- `ai/charter-ai-governance-council.md` §1: "Review material changes to deployed AI models" → cross-references the Material change thresholds table in the AI governance framework.
- `ai/standard-ai-security-and-risk.md` §6.1: "AI systems must be tested before release and after material change" → same cross-reference.
- `ai/procedure-ai-evaluation.md` Step 5: "Rejected systems require material changes and full re-evaluation" → same cross-reference.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 13 (2026-05-28): Tooling hardening — two new linters and full audit-suite wire-up

Resolves the audit blind-spots that allowed the Phase 12 defect set to accrete: the linter suite now catches the patterns Phase 12 had to fix manually. The audit suite grows from 8 to 10 audits, all wired into pre-commit and CI.

### New linters

- `tools/lint-shall-near-uncertainty.py` (new): detects mandatory `shall`/`must`/`will` requirements within 2 lines of uncertainty markers (`[Unverified]`, `TBD`, `TODO`, `FIXME`, `XXX`, `Draft <year/proper-noun>`, `placeholder`, `[Draft N Reference]`). Would have caught the Phase 12.5 finding before merge. Returns non-zero on findings.

- `tools/lint-roles.py` (new): parses every `**Owner:**` and `**Approving Authority:**` value from document metadata blocks and verifies the value is either defined in `governance/register-role-authority.md` or in the linter's `EXTRA_KNOWN_ROLES` exemption set (for cross-functional bodies, alias roles, and named maintainer functions). Detects undefined-role usage that creates governance ambiguity. Skips obvious template placeholders (`<role title>`, `Role Name`, bracketed text).

### Role authority register expanded

- `governance/register-role-authority.md` (v1.1.0 → v1.2.0): nine additional roles added that were used in document metadata but not previously defined: Board of Directors, Chief Technology Officer, Chief Audit Executive, Security Owner, Communications Owner, IT Operations Lead, AI Risk Maintainer, Assurance Metrics Maintainer, Control Framework Maintainer. Total known roles in scanned files: 40 (was 22).

### Tooling pipeline wire-up

- `.pre-commit-config.yaml`: extended to run all 10 audits locally on commit. Previously ran 6 (missing the four newer linters added in Phases 11, 12.1, 13).
- `.github/workflows/quality.yml`: extended to run all 10 audits in CI on push to main and on every PR.
- `CONTRIBUTING.md`: local-audit instructions extended to list all 10 audits.

### Result

The audit pipeline now catches:
1. Metadata block defects (lint-metadata).
2. Language and style defects including em/en dashes, BrE `-ise` endings, bare `ensure`, sanitisation residue, heading-case violations (lint-language).
3. Broken internal links (lint-links).
4. Structural defects such as documents missing from their domain README (lint-structure).
5. Hallucinated or stale framework version citations (lint-citations).
6. Undefined Owner/Approving Authority roles in metadata (lint-roles).
7. Mandatory requirements next to uncertainty markers (lint-shall-near-uncertainty).
8. Overdue document reviews past the action threshold (check-review-cadence).
9. Taxonomy drift between source documents and the auto-generated registry (build-taxonomy --check).
10. Portal and maturity-scorecard drift (build-portal --check).

Taxonomy regenerated. No content changes beyond the role-register expansion.

## Phase 12.10 (2026-05-28): Editorial and terminology consolidation

Resolves the remaining medium and low-severity findings from the comprehensive audit. Closes the corrective campaign at Phase 12.

### Term definitions added

- `governance/register-key-terms-and-definitions.md` (v1.0.0 → v1.1.0): 18 new term definitions added to close terminology drift:
  - AI lexicon: AI Agent, AI Capability, AI Service, AI System (refined), Foundation Model, Model — each formally distinguished so the reader can determine whether a ChatGPT API integration is an AI system, an AI service, a capability, or an agent.
  - Approval verbs: Approve, Audit, Authorize, Monitor, Review — each formally distinguished against the others.
  - Event vs Incident: Event = observation; Incident = triaged event meeting criteria.
  - Risk Appetite vs Risk Tolerance: Appetite = strategic/board statement; Tolerance = operational threshold.
  - Log: distinguished from Monitor, Audit, Review.
  - Supplier / Third Party / Vendor: defined with explicit canonical-preference note (library prefers "supplier" as the general term; "third party" reserved for legal-contractual contexts; "vendor" reserved for technology-supplier contexts).

### "Ensures compliance" phrasing replaced

`governance/register-data-retention-schedule.md`, `compliance/policy-compliance-and-audit-management.md`, `privacy/policy-privacy-and-data-governance.md` (two instances): "ensures that compliance" replaced with "supports the organization's compliance" / "oversees compliance" so the library does not overclaim a guarantee CC0 baseline content cannot deliver.

### MASVS terminology clarification

`dev-security/standard-mobile-application-security.md`: a note added clarifying that MASVS v2 reorganised operational test groupings into MAS Testing Profiles in MASTG; the L1/L2/R concepts remain as verification-level shorthand used by this standard.

### RFC 7807 ↔ RFC 9457

`architecture/standard-api-design.md`: RFC 7807 reference annotated with the note that RFC 9457 supersedes it; both are listed in the framework alignment table.

### "Widely adopted" claims date-stamped

`privacy/jurisdictions/annex-privacy-united-states.md`: "voluntary, widely adopted" → "voluntary; broadly adopted in US enterprise practice as of 2026".
`privacy/jurisdictions/annex-privacy-singapore.md`: same pattern applied to the PDPC Model Governance Framework reference.

### AI-assistance transparency note

`CONTRIBUTING.md`: new "AI-assisted authorship" section declaring that a substantial portion of the library was authored with AI assistance and then human-reviewed. Contributors are reminded that they remain accountable for content, that framework citations must be verified against primary sources (the citation linter prevents known-hallucination reintroduction but does not substitute for new-citation verification), and that organisation-neutrality must be preserved.

### Supplier Risk Maintainer role formalised

`governance/register-role-authority.md`: "Supplier Risk Maintainer" added as a role distinct from "Supplier Owner" (the latter is per-supplier; the former maintains the cross-supplier governance content). Resolves the audit finding that "Supplier Risk Maintainer" was used as a metadata owner in supply-chain documents without being defined in the role authority register.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.9 (2026-05-28): AI procedure realism

Resolves six AI realism findings from the comprehensive audit. The AI domain now reads as more operationally honest about what is enforceable, what is best-effort, and what the procedure mechanics actually look like.

### Eval cadence realism

- `ai/procedure-foundation-model-lifecycle.md` (v0.0.1 → v0.0.2) Step 5: "Eval suite regression run at least monthly" recalibrated to "at minimum quarterly; monthly where the eval-suite cost and infrastructure permit". Eval scope, sample size, and the metrics evaluated are explicitly required to be documented per model so the cadence is substantive rather than nominal.

### Material change thresholds harmonised

- `ai/framework-ai-governance-and-risk.md` (v1.0.0 → v1.1.0): new "Material change thresholds" sub-section under the lifecycle model. Defaults specified across eight dimensions: capability performance (≥5%), cost (≥20%, consistent with the AI cost governance standard), user population, data category, tool surface, provider version, regulatory environment, supplier change. Two or more dimensions crossing simultaneously is material regardless of individual magnitude.

### Agent self-protection threat model

- `ai/standard-ai-access-and-agent-permissions.md` (v0.0.1 → v0.0.2): new §4.1.1 "Agent self-protection (defence in depth)". Seven controls covering allow-list enforcement point (outside the model, not by it), tool-registration boundary, schema validation, untrusted-content marker, cross-tool data-flow control, privilege-escalation prevention, and high-priority logging. Cross-reference to OWASP MCP Top 10 risk categories added.

### Identity propagation mechanics

- `ai/standard-ai-access-and-agent-permissions.md` §4.3.1: four concrete propagation patterns documented (Token Exchange RFC 8693, OAuth On-Behalf-Of, workload-identity-with-claim-propagation, step-up at the boundary), each with a "when appropriate" guideline. Boundary-validation requirements expanded with signature/issuer, audience, lifetime, subject-vs-agent, tenant scoping, replay protection. Token-format defaults documented (JWT per RFC 7519 with JWT BCP per RFC 8725; alternatives permitted).

### Deletion-propagation honest scope

- `ai/procedure-training-data-governance.md` (v0.0.1 → v0.0.2) Step 6: new "Limits of deletion propagation (honest scope)" table distinguishing guaranteed outcomes (dataset removal, embeddings in active vector stores, backup copies at cycle) from best-effort outcomes (production-served models trained on the data, fine-tunes and adapters) from out-of-scope (external models the organisation does not control). Adopting organisations are explicitly enjoined to distinguish what they can guarantee from what is best-effort when communicating to data subjects and regulators.

### Hard cost ceiling enforcement architecture

- `ai/standard-ai-inference-cost-governance.md` (v0.0.1 → v0.0.2): new §3.1 "Enforcement architecture". Four layers documented in ordering preference: application middleware per-request gating (required and primary), provider rate-limit configuration (secondary safeguard), provider commitment ceiling (backstop), post-billing reconciliation (detective). Hard kill switch implementation explicitly placed in the application middleware layer; documented fallback behaviour (non-AI response, cached value, explicit message) when the switch is toggled. Kill-switch operation tested per the resilience programme.

### Coordination

The five AI documents touched in this phase are now individually operationally executable; an adopting organisation reading any one of them finds explicit mechanism, not just intent.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.8 (2026-05-28): AI Governance Maintainer role split

Resolves the role-bandwidth-overload finding by splitting the overloaded `AI Governance Maintainer` role into three named roles, each with a clearly bounded scope. The umbrella `AI Governance Lead` role retained as the secretariat / chair function on the AI Governance Council.

### New roles defined in `governance/register-role-authority.md` (v1.0.0 → v1.1.0)

- **AI Governance Approver** — approval decisions for AI policies, frameworks, standards, deployment gates, foundation-model selection, risk-classification approvals, and material lifecycle changes.
- **AI Data Steward** — training-data governance, dataset acceptance, deletion-propagation, lineage tracking, sensitive-content controls, and dataset documentation (datasheets).
- **AI System Inventory Keeper** — maintenance of the AI System Register, Model Registry, MCP server register, model cards, system cards, and cross-references between AI inventories and adjacent registers (ADM, resilience, supplier).

The umbrella `AI Governance Lead` role description updated to declare it as the AIGC secretariat role coordinating the three sub-roles.

### Documents reassigned

40 occurrences of `AI Governance Maintainer` across 19 files mapped to the appropriate new role.

Owner-field reassignments by responsibility area:

- **AI Governance Approver** (the policy/framework/decision standards): `ai/README.md`, `ai/framework-ai-governance-and-risk.md`, `ai/framework-ai-model-risk.md`, `ai/standard-ai-model-risk.md`, `ai/standard-ai-inference-cost-governance.md`, `ai/procedure-foundation-model-lifecycle.md`, `ai/procedure-ai-model-risk-assessment.md`, `supply-chain/procedure-third-party-ai-due-diligence.md`. Governance index rows for `ai/policy-ai-compliance.md`, `ai/framework-ai-system-audit-certification.md`, `ai/checklist-ai-algorithmic-compliance.md` also reassigned.
- **AI Data Steward** (training-data, datasheet): `ai/procedure-training-data-governance.md`, `ai/template-dataset-datasheet.md`.
- **AI System Inventory Keeper** (registries, cards, lifecycle mapping): `ai/register-model-registry.md`, `ai/template-ai-system-register.md`, `ai/template-model-card.md`, `ai/template-system-card.md`, `ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`.

Body-content references in seven files retargeted to the appropriate sub-role per responsibility area:

- `ai/procedure-foundation-model-lifecycle.md`: candidate-list maintenance → AI System Inventory Keeper.
- `ai/procedure-training-data-governance.md`: dataset acceptance and recording → AI Data Steward.
- `ai/standard-ai-inference-cost-governance.md`: cost-dashboard ownership and anomaly summary → AI Governance Approver.
- `ai/template-dataset-datasheet.md`: dataset sign-off role → AI Data Steward.
- `ai/register-model-registry.md`: quarterly registry review → AI System Inventory Keeper.
- `privacy/register-automated-decision-making.md`: cross-register consistency owner → AI System Inventory Keeper.
- `resilience/register-resilience-metrics-and-testing-log.md`: AI resilience metric owner → AI System Inventory Keeper.

A reader of any AI document now sees a single, scope-appropriate role; no role is asked to be the owner of approvals, data stewardship, and inventory maintenance simultaneously.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.7 (2026-05-28): Scope matrices for paired standards

Resolves three scope-collision findings from the comprehensive audit by adding explicit scope-boundary clauses to each affected document pair.

### Cloud baselines — operations vs dev-security

- `operations/standard-cloud-security-configuration-baseline.md` (v1.3.0 → v1.4.0): new §2.1 "Scope boundary with dev-security cloud hardening baselines" with a per-subject table mapping enterprise-tenant administration (this standard) to workload-level concerns (dev-security baselines).
- `dev-security/standard-cloud-hardening-baseline-aws.md` (v0.0.1 → v0.0.2): new "Scope boundary with the operations cloud configuration baseline" sub-section.
- `dev-security/standard-cloud-hardening-baseline-azure.md` (v0.0.1 → v0.0.2): same.
- `dev-security/standard-cloud-hardening-baseline-gcp.md` (v0.0.1 → v0.0.2): same.

A workload now reads as conforming to both standards with a clear division of authority.

### Logging vs observability — routing rule

- `security/standard-logging-and-monitoring.md` (v1.3.0 → v1.4.0): new "Scope boundary with the operations observability and telemetry standard" sub-section with an event-class routing table. Security-relevant events route to SIEM; operational signals route to observability; dual-purpose events emitted to both with shared trace identifiers. Also: BASC residue in the Scope section (caught here, missed by Phase 12.3) replaced with a sector-overlay pointer.
- `operations/standard-observability-and-telemetry.md` (v0.0.1 → v0.0.2): reciprocal note pointing back to the security standard's routing table.

### API design vs API security — approval sequence

- `architecture/standard-api-design.md` (v0.0.1 → v0.0.2): new "Relationship to the API security standard and approval sequence" sub-section documenting the design-gate → threat-model-gate → implementation sequence.
- `dev-security/standard-api-security.md` (v0.0.1 → v0.0.2): reciprocal sub-section with the same sequence; conditional-endorsement loop documented for cases where a security finding requires reshaping the contract.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.5 / 12.6 (2026-05-28): [Unverified] tags, phantom dependency, internal hostname

Resolves the `[Unverified]`-tag-in-mandatory-policy finding, the phantom "IT Operations Documentation Framework" dependency, and the internal-looking hostname in an AI code example. Bundled as a single change for compactness.

### `[Unverified]` tags removed from mandatory policy text

- `governance/policy-exception-and-risk-acceptance-management.md` (v1.0.0 → v1.0.1):
  - §7.1: removed `[Unverified]` marker and softened "shall implement" to "may implement"; the machine-readable exception registry is reclassified as a recommended practice rather than a mandatory `shall` obligation.
  - §7 heading updated from "(future readiness)" to "(recommended where automation is practical)".
  - References table: removed `[Unverified]` qualifier on the NIST AI RMF 1.0 entry.
  - Compliance mapping table: replaced `[Draft 2026 Reference]` / `[Unverified]` cells with concrete framework references for the recommended-registry row.
- `compliance/policy-compliance-and-audit-management.md` (v1.0.0 → v1.0.1):
  - §5.3: removed `[Unverified]` marker; reframed as a where-cost-justifies recommendation.
  - References list: removed the "Draft 2026 ISO 37301 Revision" `[Unverified]` entry.

### Phantom "IT Operations Documentation Framework" dependency resolved

- `compliance/policy-compliance-and-audit-management.md` §2.4: replaced the reference with concrete pointers to `governance/standard-records-retention-and-destruction.md` (for retention) and `operations/framework-it-service-management.md` (for ITSM-aligned documentation).
- `resilience/plan-it-disaster-recovery.md`: same reference replaced with a concrete pointer to the recovery runbook template.

### Internal hostname in AI code example replaced with generic placeholders

- `ai/guide-ai-security-technical-implementation.md` (v1.3.0 → v1.3.1) line 493: `Server=db-server.internal;Database=AppDB` replaced with `Server=[DATABASE_HOSTNAME];Database=[DATABASE_NAME]`. The example continues to demonstrate the prohibited pattern but no longer reads as sanitisation residue from an internal codebase.

### Citation denylist extended

`tools/lint-citations.py` denylist now also pins "Draft 2026 ISO 37301" and "IT Operations Documentation Framework" so neither can be reintroduced silently.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.4 (2026-05-28): Third-party risk standard consolidation

Resolves the duplicate-authority finding identified by the comprehensive audit. Per the user's decision to merge, the two parallel third-party risk standards are consolidated into a single document in the risk domain.

### Merged

- `risk/standard-third-party-and-supply-chain-risk.md` (v1.0.0 → v1.1.0): becomes the sole, master third-party-and-supply-chain risk standard for the library. Augmented with the supply-chain document's lifecycle content: an explicit AI service-provider contract-clause sub-section (dataset lineage, model validation per ISO/IEC 42001 §9, ethical sourcing, no-training-on-customer-data, deprecation notice, cross-border mechanism); supporting-tooling references in the monitoring section (TPRAQ, security-rating services, threat intelligence); a dedicated Offboarding and contract termination section; framework alignment expanded with ISO/IEC 27036-3, NIST SP 800-161r2, COBIT 2019 APO10, and CSA CCM v4.1 STA-02. A `supersedes` sentence references the deleted file.

### Deleted

- `supply-chain/standard-third-party-risk.md` (was v1.0.0): consolidated into the risk-domain master per the audit recommendation.

### Cross-references updated

21 files updated to point at the consolidated risk-domain standard. Affected directories: compliance/, dev-security/, governance/, operations/, security/, supply-chain/.

- Governance index `governance/register-document-index-and-classification.md` (v1.21.0 → v1.22.0): the supply-chain duplicate row removed; risk-domain row retained.
- Supply-chain README (v1.1.0 → v1.2.0): supply-chain TPR row removed from active documents.

### Result

A reader looking for the third-party risk standard now finds one canonical document, with consistent tier criteria, lifecycle, and ownership. The CRO is the named owner. The operational procedures in `supply-chain/` continue to implement the lifecycle steps.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.3 (2026-05-28): BASC migration to /sectors/ domain (organisation-neutrality)

Resolves the organisation-neutrality violation identified by the comprehensive audit. The library declared itself "organization-neutral" in `README.md` while three core policy documents explicitly scoped themselves to "BASC-certified logistics operations in Latin America (Colombia, Mexico, Peru, Chile)" and the compliance domain hosted a BASC-specific policy and two BASC registers as if universal content.

### Structural change

New top-level directory `/sectors/` created for optional, programme-conditional governance content. Organisations not participating in a covered sector programme can omit the corresponding annex entirely without affecting the main library.

- `sectors/README.md` (new, v1.0.0): domain register describing the sector-annex pattern, applicability rules, and relationship to the main library.
- `sectors/basc/README.md` (new, v1.0.0): BASC sub-register describing applicability and listing active BASC documents.

### Files moved (git history preserved via `git mv`)

- `compliance/policy-basc.md` → `sectors/basc/policy-basc-information-security.md` (v1.0.0 → v1.1.0; renamed to reflect canonical naming; Category updated from "Compliance Management" to "Sector Annex"; cross-references updated)
- `compliance/register-basc-it-responsibilities.md` → `sectors/basc/register-basc-it-responsibilities.md` (v1.0.0 → v1.1.0; same updates)
- `compliance/register-basc-it-compliance-kpis.md` → `sectors/basc/register-basc-it-compliance-kpis.md` (v1.0.0 → v1.1.0; same updates)

### BASC scoping stripped from main-domain documents

- `security/policy-information-security.md`: scope section, governance section, network section (4.1, 4.3, 4.4), data section (7.1, 7.2, 7.3), incident section (9.1, 9.2), framework alignment (line 145) — generalised; sector overlay pointer added. Inline NIST AI RMF 1.1 reference (missed by Phase 12.1 because of bare "AI RMF" form) corrected to NIST AI RMF 1.0.
- `risk/policy-enterprise-governance-and-risk-management.md`: scope section generalised; sector overlay pointer added.
- `risk/standard-enterprise-risk-management.md`: scope section generalised; sector overlay pointer added.
- `governance/standard-records-retention-and-destruction.md`: BASC-specific Section 6 generalised into "sector-specific retention overlays" with pointer to `/sectors/` and the transportation-and-logistics sector annex in `/compliance/`.

### Cross-references updated

Cross-references to old BASC paths updated in: `compliance/README.md` (v1.1.0 → v1.2.0), `compliance/annex-transportation-and-logistics-sector-requirements.md`, `compliance/matrix-grc-compliance-alignment.md`, `compliance/register-ctpat-it-controls.md`, `compliance/register-pip-compliance-controls.md`, `compliance/template-trade-compliance-gap-assessment.md`, `governance/matrix-reverse-framework-control-crosswalk.md`, `governance/register-document-index-and-classification.md` (v1.20.0 → v1.21.0; three BASC rows reclassified from Compliance to Sectors domain), `supply-chain/README.md`, `supply-chain/matrix-supply-chain-security-programme-alignment.md`, `supply-chain/register-ctpat-full-msc-controls.md`.

### Tooling updates

`sectors` added to the DOMAINS / scan-path lists in `tools/build-taxonomy.py`, `tools/lint-structure.py`, `tools/lint-metadata.py`, `tools/lint-language.py`, `tools/lint-links.py`, `tools/lint-citations.py`, `tools/check-review-cadence.py`. New denylist entry in `tools/lint-citations.py` for bare "AI RMF 1.1" form to complement the existing "NIST AI RMF 1.1" entry.

### Top-level updates

- `README.md` (v1.5.1 → v1.5.2, patch per the standing rule): new `/sectors/` directory entry added to the repository structure; document-count statement updated to mention the optional sector-annex domain.
- `specification-master-project.md` (v1.2.4 → v1.2.5): `/sectors/` added to the directory listing and the domain purpose summary.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.2 (2026-05-28): AI Governance Council operationalisation

Resolves the charter status whereby the AI Governance Council was declared "in formation" with full operationalisation targeted for Q3 2026 while 16+ AI documents referenced its approval as binding. The council is now an active governance body.

- `ai/charter-ai-governance-council.md` (v1.0.0 → v1.1.0): the "in formation" note removed. Composition table restated with eleven active seats: Chair (Chief Information Security Officer), Deputy Chair (Chief Information Officer), and members covering Chief Technology Officer, Chief Financial Officer, Chief Human Resources Officer, General Counsel, Chief Privacy Officer, Chief Risk Officer, AI Governance Lead (secretariat), Business Domain Representative (rotating), and Independent External Adviser (standing observer). The Chair confirms each meeting's roster; where a seat is unfilled the role's delegate or an acting appointee designated by the Chair exercises the responsibility. Quorum is the Chair (or Deputy Chair) plus four members.

The charter now reads as an active body; all downstream AI documents that reference AIGC approval as binding are unblocked. No other document changes were required; the existing dependency chain assumes the council can act, which is now true.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.1 (2026-05-28): Framework citation corrections

Corrects three repository-wide framework citation hallucinations identified by the comprehensive audit (Phase 11 follow-up).

- **COBIT 2025 → COBIT 2019**: 132 replacements across 78 files. ISACA's current published COBIT version is COBIT 2019; "COBIT 2025" does not exist. Process identifiers cited alongside (APO01, APO14, BAI09, MEA01, MEA02, APO06, APO07, etc.) are valid COBIT 2019 process IDs.
- **CSA CCM v5 → CSA CCM v4.1**: 115 replacements across 75 files. CSA's current Cloud Controls Matrix version is v4.1; "CCM v5" does not exist. Domain identifiers cited alongside (AIS, DSP, GOV, GRM, SEF, IVS, IAM, LOG, IPY, TIM, EKM, END, TVM, SR) are valid CCM v4 domain prefixes.
- **NIST AI RMF 1.1 → NIST AI RMF 1.0 (with AI 600-1 GenAI Profile)**: 1 replacement in `governance/policy-exception-and-risk-acceptance-management.md`. NIST AI RMF was published as version 1.0; the Generative AI Profile is published as NIST AI 600-1.

New tool: `tools/lint-citations.py` — stdlib-only Python linter that pins known-hallucinated framework strings on a denylist and reports any reintroduction. Exits non-zero on findings; suitable for CI integration. Denylist currently covers the three patterns above. `CONTRIBUTING.md` updated to list the linter in the local audit suite (now 8 audits).

Historical CHANGELOG entries are preserved verbatim; their descriptions reference the strings as they existed at the time, which the linter exempts.

Source verification: ISACA COBIT page, CSA CCM artifacts page, NIST CSRC.

## Phase 11 (2026-05-28): Continuous quality and review cadence (3 new documents + cadence checker)

Codifies the library maintenance practice with three new governance artefacts and a new audit tool. Closes the continuous-quality phase of the advisory review.

- `governance/procedure-library-quality-and-review-cadence.md`: eight-step procedure covering schedule establishment, overdue detection, per-document review (currency, framework alignment, cross-reference, sanitisation, language, disposition, record), disposition application, derived-artefact maintenance, the standing audit suite (now seven audits), periodic library-level review (quarterly/semi-annual/annual cadences), and drift handling.
- `governance/register-document-review-schedule.md`: schedule schema with eleven fields, review-frequency normalisation table, six status values (Current, Due-soon, Overdue, Action-threshold, Blocked, Retired), maintenance rules, operating cadence, integration with tooling, and reporting outputs.
- `governance/template-document-review-record.md`: six-section per-document review record (identification, assessment of thirteen items, findings, disposition, actions, sign-off), style and length expectations, worked example.

New tool:

- `tools/check-review-cadence.py`: stdlib-only Python script that parses each active document's Date and Review Frequency metadata, computes next-review-due dates, and reports overdue and past-action-threshold entries with configurable warn-window and action-threshold parameters. Returns non-zero when documents are past the action threshold to gate CI.

Supporting changes:

- Governance README bumped 1.0.3 to 1.1.0 (minor: three substantive new rows).
- Document index `governance/register-document-index-and-classification.md` bumped 1.19.0 to 1.20.0 (minor: three substantive new rows).
- Specification master bumped 1.2.3 to 1.2.4 (patch: architecture domain added to the repository structure listing).
- `CONTRIBUTING.md` updated to list the full seven-audit suite local contributors should run.
- Language linter exemption list extended to include the document review record template (which references the "ensure that" rule explicitly).
- Taxonomy, portal, and maturity scorecard regenerated.

Baseline: 266 active documents scanned by the cadence checker; all current except 1 due-soon (a monthly-cadence operations register) and 2 event-driven.

## Phase 10 (2026-05-28): Architecture domain (8 new documents)

Establishes the new `/architecture/` domain. Each new artefact starts at version 0.0.1 per the ingestion specification.

- `architecture/README.md`: domain register with 8 active documents and 6 domain-coverage areas.
- `architecture/framework-enterprise-architecture.md`: ten-section framework (principles, viewpoints, capability model, target-state and transition, governance forum, roles, deliverables, integration with adjacent programmes, fitness functions, operating expectations) aligned to TOGAF, ISO/IEC/IEEE 42010, IT4IT, C4, DDD, Team Topologies, Wardley mapping, and Accelerate research.
- `architecture/standard-architecture-decision-records.md`: ten-section ADR standard (principles, when to write, template, status lifecycle, review and approval, storage, integration with adjacent processes, AI-aware practice, quality expectations, anti-patterns).
- `architecture/standard-reference-architecture.md`: ten-section reference-architecture practice (principles, classes, structure, maturity scale, authoring, consumption, deviation handling, maintenance, governance integration, quality expectations).
- `architecture/standard-technology-radar.md`: ten-section radar standard (principles, four rings, quadrants, blip structure, lifecycle, governance, criteria, relationship to other artefacts, AI radar handling, exceptions).
- `architecture/procedure-architecture-review.md`: eight-step architecture review procedure with reviewer assignment, dispositions, decision recording, implementation oversight, closure and learning, plus appeal process.
- `architecture/standard-api-design.md`: fourteen-section API design standard (principles, style choice, REST conventions, contract and schema, identifiers, errors, versioning, time and units, documentation, pagination, idempotency, AI-callable APIs, customer-facing APIs, governance).
- `architecture/standard-data-architecture.md`: fourteen-section data architecture standard (principles, domains and ownership, classification, schemas and contracts, integration, quality, lineage, lifecycle, analytical and AI platforms, sharing, master and reference data, governance forum, relationship to adjacent artefacts, anti-patterns).
- `architecture/standard-integration-architecture.md`: fourteen-section integration standard (principles, pattern selection, classes, contracts, event-driven, synchronous, batch, webhooks, AI provider integration, observability, reliability patterns, security overlay, governance, anti-patterns).

Document index `governance/register-document-index-and-classification.md` bumped 1.18.0 to 1.19.0 (minor: eight substantive new rows). Top-level README bumped 1.5.0 to 1.5.1 (patch: domain listing and document-count update). Tooling (`tools/build-taxonomy.py`, `tools/lint-structure.py`, `tools/lint-metadata.py`, `tools/lint-language.py`, `tools/lint-links.py`) updated to include the new domain in their scan lists. Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.9 (2026-05-28): Risk and governance (4 new documents)

Closes four risk and governance content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- `risk/template-operational-risk-register.md`: ten-section operational risk register template (identification, scope and assumptions, risk entries, risk taxonomy, assessment scales, control linkage, scenario and emerging-risk linkage, loss events and near-misses, aggregation and reporting, integration), with a Basel-aligned taxonomy of thirteen categories and a worked example.
- `risk/register-scenario-risk-catalogue.md`: scenario catalogue covering eleven classes (cyber attack, AI-specific, technology failure, supplier failure, people and conduct, external event, financial market, regulatory, reputational, climate-related, concurrent) with a reference set of fifty scenarios; severity calibration (moderate, severe-but-plausible, extreme); seven uses of the catalogue.
- `risk/template-board-risk-report.md`: fourteen-section board-facing risk report template (cover, executive summary, risk appetite and tolerance, top enterprise risks, emerging risks, incidents and near-misses, regulatory and external environment, supplier and concentration, AI and emerging-technology risk, resilience and continuity, assurance, risk culture, board decisions requested, appendices) with style guidance, cadence, and preparation process.
- `risk/register-assurance-map.md`: assurance map applying the three-lines model across twelve domains with a six-level assurance rating scale (green, amber-1, amber-2, red, not applicable, out of cycle), fourteen-activity taxonomy, governance forum, integration with the assurance plan, gap-management process, and a worked example.

Document index `governance/register-document-index-and-classification.md` bumped 1.17.0 to 1.18.0 (minor: four substantive new rows). Risk README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.8 (2026-05-28): Operations (5 new documents)

Closes five operations content gaps identified in the advisory review.

- `operations/standard-observability-and-telemetry.md`: fourteen sections covering principles, service-level signals, metrics, logs, distributed tracing, error and exception telemetry, events, synthetic and real-user monitoring, dashboards and alerting, privacy and data classification, cost governance, AI and ML telemetry, tooling and platform, testing.
- `operations/standard-site-reliability-engineering.md`: twelve sections covering principles, SLOs and SLIs, error budget policy, reliability practices, change-related risk, incident management, on-call, toil management, runbooks, AI service reliability, tooling and platform, governance.
- `operations/standard-capacity-and-performance-management.md`: twelve sections covering principles, capacity classes (eight), demand forecasting, capacity planning, performance objectives and measurement, performance testing, scaling, capacity for resilience, third-party and vendor capacity, cost governance, governance forum, AI inference capacity.
- `operations/procedure-release-management.md`: nine-step procedure (planning, build and packaging, pre-production validation, authorisation, deployment, verification, stabilisation, rollback or forward-fix, closure and learning), release classes (routine, expedited, emergency, standard repeatable), seven role definitions, coordination with seven adjacent procedures, six deployment strategies.
- `operations/standard-it-financial-management.md`: twelve sections covering principles, cost taxonomy, attribution, budgeting, monitoring and forecasting, optimisation, vendor commitment management, AI cost governance, sustainability considerations, governance, integration with related programmes, financial reporting and compliance.

Document index `governance/register-document-index-and-classification.md` bumped 1.16.0 to 1.17.0 (minor: five substantive new rows). Operations README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.7 (2026-05-28): DevSecOps (7 new documents)

Closes seven developer-security content gaps identified in the advisory review.

- `dev-security/standard-api-security.md`: twelve sections covering lifecycle gates, authentication, authorisation, input validation, transport, rate limiting and abuse prevention, observability and logging, gateway management, third-party API consumption, AI-exposed APIs, GraphQL-specific controls, event-driven and webhook security.
- `dev-security/standard-container-and-image-security.md`: ten sections covering image build, registry management, runtime security, orchestrator hardening, developer workflow, serverless containers, supply-chain integrity (SBOM, signing, attestation), vulnerability management, data handling, incident readiness.
- `dev-security/standard-mobile-application-security.md`: twelve sections aligned to OWASP MASVS v2 (L1, L2, R) with four-tier sensitivity mapping; covers storage, cryptography, authentication, network, platform interaction, code quality and resilience, third-party SDKs, store and distribution, privacy (including children's data), testing, incident readiness.
- `dev-security/procedure-secure-code-review.md`: seven-step procedure (pre-review preparation, reviewer assignment, reviewer evaluation, reviewer dispositions, author response, merge gate, post-merge actions), ten evaluation categories (secrets, input handling, authentication and authorisation, cryptography, data, errors and logging, dependencies, IaC and platform, AI components, change hygiene), AI-assisted and AI-generated code considerations.
- `dev-security/standard-cloud-hardening-baseline-aws.md`: thirteen sections covering account structure and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, tagging and inventory, provisioning and change, incident readiness; aligned to CIS AWS Foundations Benchmark and AWS Well-Architected Security Pillar.
- `dev-security/standard-cloud-hardening-baseline-azure.md`: thirteen sections covering tenant, subscription, and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, tagging and inventory, provisioning and change, incident readiness; aligned to CIS Microsoft Azure Foundations Benchmark and the Microsoft Cloud Security Benchmark.
- `dev-security/standard-cloud-hardening-baseline-gcp.md`: thirteen sections covering organisation, folder, and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, labelling and inventory, provisioning and change, incident readiness; aligned to CIS Google Cloud Platform Foundations Benchmark and the Google Cloud Architecture Framework security pillar.

Document index `governance/register-document-index-and-classification.md` bumped 1.15.0 to 1.16.0 (minor: seven substantive new rows). Dev-security README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion; removed completed items from the planned expansion list). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.6 (2026-05-28): Security (7 new documents)

Closes seven security content gaps identified in the advisory review.

- `security/framework-zero-trust-architecture.md`: seven principles, seven pillars (identity, devices, networks, applications and workloads, data, visibility and analytics, automation and orchestration), policy-engine input model, four-stage maturity ladder.
- `security/standard-email-security.md`: eight sections covering outbound authentication (SPF/DKIM/DMARC/BIMI/MTA-STS), inbound controls, anti-phishing and BEC, outbound controls, user-facing controls, secure-email-gateway requirements, AI-generated and AI-processed considerations, incident response.
- `security/standard-soc-operating-model.md`: four capability tiers, staffing model (nine roles), tool stack (fourteen tool categories), coverage hours, detection engineering practices, threat hunting, intelligence integration, on-call governance, metrics, supplier-managed-SOC requirements, continuous improvement.
- `security/standard-saas-security-posture-management.md`: ten sections covering inventory, configuration baselines, continuous posture monitoring, SaaS-to-SaaS integration risk, third-party application access, shadow-SaaS detection, SaaS-to-SaaS supplier risk, data protection within SaaS, incident readiness, lifecycle.
- `security/framework-insider-risk-programme.md`: five insider risk categories, governance model with Insider Risk Steering Committee, four pillars (prevention, detection, response, learning), eleven privacy and due-process safeguards, deliberate out-of-scope exclusions, coordination with eight adjacent programmes, metrics.
- `security/standard-endpoint-hardening.md`: twelve sections covering identity and authentication, device integrity, software and configuration, EDR, data protection, network and connectivity, privileged access workstations, developer workstations, BYOD and unmanaged devices, mobile devices, kiosks and shared devices, lifecycle.
- `security/procedure-key-escrow-and-recovery.md`: three key categories (productivity-data, operational service, root and signing), escrow architectures per category, recovery triggers, dual-control matrix, Category 3 ten-step ceremony, authorisation flow, post-recovery actions, lost or compromised key handling, post-quantum considerations.

Document index `governance/register-document-index-and-classification.md` bumped 1.14.0 to 1.15.0 (minor: seven substantive new rows). Security README bumped 1.1.1 to 1.2.0 (minor: substantive section expansion).

## Phase 9.5 (2026-05-28): AI (10 new documents)

Closes ten AI content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- `ai/plan-ai-incident-response.md`: AI-specific incident classes and triggers, P1 to P4 severity criteria, seven-phase lifecycle with AI-specific actions at each phase, coordination with security and privacy streams, evidence requirements.
- `ai/template-dataset-datasheet.md`: ten-section datasheets-for-datasets template covering motivation, composition, collection process, preprocessing and labelling, uses, distribution, maintenance, ethical considerations, provenance and lineage, signatures.
- `ai/register-model-registry.md`: comprehensive model inventory with 30-field schema, six lifecycle states (Research, Evaluation, Staging, Production, Deprecated, Retired), backward and forward lineage tracking, integration with eleven adjacent governance artefacts.
- `ai/procedure-foundation-model-lifecycle.md`: seven-step lifecycle for foundation-model consumption (identify, pre-engagement evaluation, contractual integration, deployment, ongoing monitoring, version transition, exit), seven AI-specific contract clauses, seven risk vectors with mitigations.
- `ai/template-ai-vendor-security-questionnaire.md`: nine-section AI-specific extension to the general supplier questionnaire covering provider profile, training-data provenance, customer data handling, model security, tool and agent capabilities, evaluation and assurance, compliance and transparency, incident response, continuity and exit.
- `ai/standard-ai-access-and-agent-permissions.md`: eight sections covering principles (six), human access to AI capabilities, service-to-AI access, AI-to-tool access for agentic systems (with tool allow-list, capability scopes, identity propagation, three confirmation modes, rate and chain-length limits, logging), AI-to-data access, AI-to-AI access, access review cadence, incident-time controls.
- `ai/register-mcp-server.md`: MCP server inventory with 25-field schema, four-tier approval categories, server-security baseline (eleven control areas), coordination with seven adjacent governance artefacts.
- `ai/procedure-training-data-governance.md`: ten-step procedure covering source identification, sensitive-content removal, consent and subject-rights mechanism, approval to train, lineage tracking, deletion propagation with SLAs, supplier-provided training data, synthetic data, retrieval index content, periodic review.
- `ai/standard-ai-inference-cost-governance.md`: ten sections covering principles, budgeting and allocation, cost ceilings and rate limits, model-choice criteria, monitoring and anomaly response (dual-routed financial and security), feature lifecycle controls, agent and autonomous workflow controls, customer-facing transparency, provider-side cost-management, reporting.
- `ai/template-ai-red-team-report.md`: nine-section red team engagement report covering engagement profile, methodology, structured findings (with twelve-field-per-finding schema), coverage assessment against OWASP LLM Top 10 and MITRE ATLAS, positive observations, recommendations, validation and retest, distribution, signatures.

Document index `governance/register-document-index-and-classification.md` bumped 1.13.0 to 1.14.0 (minor: ten substantive new rows). AI README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion).

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
