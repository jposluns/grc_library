# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see `specification-master-project.md` section 4.5. The changelog records phase-level changes, not per-document version bumps.

## Phase 21.6 (2026-05-28, Library Version 2026.05.1): Filename and Document Title alignment audit

Sixth sub-phase of Phase 21. Closes the final Priority 2 item: an audit that catches typos and copy-paste defects where a file's name and its Document Title diverge.

### New file

- `tools/lint-filename-title-alignment.py`: permissive linter. For each active document, normalises both the filename's stem (after the doctype prefix) and the Document Title into a token set, and flags files where the two sets share **no** significant content words after normalisation. Honours a synonym table for legitimate acronym-in-filename / expansion-in-title patterns (SBOM, CAPA, FedRAMP, SOX, AEO, CTPAT, PIP, BASC, DORA, NIS, AI, and others).

### Result on initial run

- One match initially detected: `supply-chain/register-sbom.md` (filename uses the acronym, title uses the expansion "Software Bill of Materials Register"). Resolved by adding the SBOM → "software bill of materials" mapping to the synonym table. All 269 active documents now pass.
- No content changes to the corpus; the existing filenames and titles were already aligned once acronym synonyms were recognised.

### Tooling integration

- `.github/workflows/quality.yml`: new "Filename and Document Title alignment audit" step added between the standards-currency audit and the role audit. The library now runs **12 audits** per PR.
- `tools/README.md`: scripts table updated.

### Convention captured

The synonym table in the new linter doubles as a quick reference for which acronyms the library accepts in filenames. Adding new acronym-spelled filenames (for example, future country programmes) should update the synonym table at the same time.

### TODO

Priority 2.1 (filename ↔ Document Title alignment audit) removed. Priority 2 tier now complete.

All 12 audits clean. Library Version: 2026.05.1.

## Phase 21.5 (2026-05-28, Library Version 2026.05.0): Library-level CalVer versioning adopted

Fifth sub-phase of Phase 21 (foundations before content expansion). Resolves the absence of a library-level versioning scheme noted during Phase 20 review. Until now, each document carried its own semantic version, but the library as a whole had no declared version, leaving adopters to reference commit SHAs.

### Scheme adopted

Calendar Versioning (CalVer) of the form `YYYY.MM.patch`:

- `YYYY` is the four-digit year of the most recent merge to `main`.
- `MM` is the two-digit month of the most recent merge to `main`.
- `patch` is a sequential counter that increments on every merge to `main` within the same `YYYY.MM` window. It resets to `0` when the month rolls over.

Rationale for CalVer over SemVer:

- The library evolves continuously through small phased PRs rather than discrete versioned releases.
- The most useful question for an adopter is "how recent is this snapshot?", not "is this backwards-compatible?".
- The patch counter records cumulative churn within a month, surfacing the high merge frequency that semantic versioning would obscure.
- No judgment is needed to decide between major/minor/patch bumps; the scheme is mechanical.

### Files updated

- `specification-master-project.md` (1.2.7 → 1.3.0): new section 4.5 "Library versioning" documenting the scheme, rationale, recording location, maintenance procedure, and relationship to per-document semantic versioning.
- `README.md` (1.5.4 → 1.6.0): metadata block restructured. The previous `**Version:**` field is renamed to `**README Version:**` (clarifying it tracks the README content, not the library). A new `**Library Version:**` field is introduced and set to the initial value `2026.05.0`. An explanatory sentence below the metadata block points to the specification.
- `CHANGELOG.md` (this file): preamble updated to reference the new versioning scheme. Phase headings now include the Library Version in effect at the time of the phase's completion.

### Initial value

The library version is initialised at `2026.05.0` by this Phase 21.5. Future PRs merged to `main` will increment the patch counter (2026.05.1, 2026.05.2, etc.) within the same calendar month. When the calendar month changes, the next merge sets the version to `YYYY.MM.0`.

### Maintenance

Each PR that merges to `main` updates `README.md`'s `Library Version` field as part of the PR. The audit suite does not automatically enforce monotonicity, but reviewers verify the bump is present before approving the PR.

### TODO

Priority 2.1 (library-level versioning policy) removed. Remaining P2 items: 2.1 (was 2.2) filename ↔ Document Title alignment audit.

All eleven audits clean.

## Phase 21.4 (2026-05-28): Related-Documents reciprocity rule considered and dropped

Fourth sub-phase of Phase 21 (foundations before content expansion). A draft reciprocity linter was implemented and empirically tested against the library; the test revealed 1,269 non-reciprocal Related-Documents references across 266 of 280 active documents.

### Finding

The library's actual convention is **asymmetric** Related Documents: each document lists "what this document consumes / relates to from its own perspective", not "the complete bidirectional graph". Authors curate Related Documents to be useful to a reader of that document, not to satisfy graph symmetry. This is a reasonable convention.

### Decision

The strict-reciprocity rule was dropped. Three reasons:

1. The convention is established and reasonable; enforcing strict reciprocity would require either rewriting 1,269 cross-references (mostly noise) or adopting an exemption-marker mechanism on every legitimately one-way reference (also extensive).
2. The underlying concern (catching half-updated cross-references during refactors) is already covered by `lint-links.py` (broken-link detection), which would catch the kind of file-rename mishap that drove this proposal.
3. A narrower doctype-pair rule (Framework↔Standard, Policy↔Standard, Charter↔Framework) was considered but rejected: the marginal value over `lint-links.py` does not justify the maintenance cost of a curated rule set with many exemptions.

### Recorded in TODO

The decision is also recorded in a new `## Decisions log` section in `TODO.md` so the rationale is preserved if the question recurs.

### Result

No linter added. No code changes other than the TODO and CHANGELOG entries. Priority 2 list renumbered: former 2.2 (library-level versioning) becomes 2.1; former 2.3 (filename/title alignment) becomes 2.2.

## Phase 21.3 (2026-05-28): Standards-currency checker and canonical citations register

Third sub-phase of Phase 21 (foundations before content expansion). Introduces a positive-list catalogue of canonical standards citations and a new linter that detects stale references against it. Resolves the highest-leverage consistency risk identified during Phase 20 review: standards citations drifting as new versions are published.

### New files

- `governance/register-canonical-citations.md` (v1.0.0, Register doctype): positive list of standards citations across ISO/IEC, NIST, EU regulations and directives, North-American regulations, other privacy regulations, CSA frameworks, ISACA frameworks, MITRE adversary frameworks, OWASP, customs and trade, sector-specific standards, OECD, and ICAO/IMO. ~81 standards entries. For each: current version, publication date, topic, and known superseded versions for the linter to flag.
- `tools/lint-standards-currency.py` (new audit): permissive linter. Parses the canonical citations register and flags references to versions listed as superseded. The register is the source of truth; new standards added to the catalogue extend the linter's coverage automatically. Complementary to `lint-citations.py` (denylist for hallucinations) rather than replacing it.

### Existing-content fixes triggered by the new linter

Initial run of the new linter detected two stale citations:

- `governance/framework-human-capital-and-ethical-conduct.md` (1.0.0 → 1.0.1): "ISO 37001:2016" → "ISO 37001:2025" (ISO 37001 was revised and republished in February 2025).
- `governance/procedure-whistleblower-and-incident-reporting.md` (1.0.0 → 1.0.1): same correction.

### Tooling integration

- `.github/workflows/quality.yml`: new "Standards-currency audit" step added to the CI pipeline. The library now runs 11 audits on every PR and push.
- `tools/README.md`: scripts table expanded to document all linters including the new standards-currency one (previously listed only 4 of the 8 scripts).
- `tools/lint-citations.py`: PATH_EXEMPTIONS extended to include `governance/register-canonical-citations.md` (the canonical register intentionally documents hallucinated/superseded strings as part of its scope).

### Cross-references updated

- `governance/README.md`: canonical citations register entry added to Active Documents.
- `governance/register-document-index-and-classification.md` (1.25.1 → 1.25.2): canonical citations register entry added.
- `TODO.md`: P1.1 (standards-currency checker + canonical citations catalogue) removed; Priority 1 tier now complete.

### Result

Every PR adding new content will now have its standards citations automatically checked against the canonical register. When a new version of a listed standard is published, updating the register's "Superseded versions" column will surface every stale citation in the library on the next CI run.

All eleven audits clean.

## Phase 21.2 (2026-05-28): Glossary and acronym index

Second sub-phase of Phase 21 (foundations before content expansion). Introduces a single canonical resolved reference for the acronyms and external-domain terms used throughout the library.

### New file

- `governance/register-glossary.md` (v1.0.0, Register doctype): alphabetical glossary covering ~150 acronyms and external terms used by the library, including regulatory bodies (HMRC, CBSA, CBP, OCC, PRA, FCA, MAS, FSA, NERC, TSA, etc.), regulations (GDPR, CPPA, CCPA, PIPL, LGPD, AIDA, DORA, HIPAA, HITECH, MDR, IVDR, SOX, etc.), frameworks and standards (WCO SAFE, ISO 27001 family, NIST AI RMF, COBIT, MITRE ATT&CK, MITRE ATLAS), sector programmes (AEO-UK, CTPAT, PIP, BASC, NEEC, ATT, STP, SES), CSA CCM domain codes (AAC, AIS, BCR, CCC, CEK, DCS, DSP, GRC, HRS, IAM, IPY, IVS, LOG, SEF, STA, TVM, UEM), CSA AICM, library role acronyms (AIGC, ERC, BCM, DPO), and common technical/security/governance acronyms (IAM, PAM, ZTNA, SBOM, SCA, SAST, SIEM, MFA, PKI, HSM, RPO, RTO, KRI, KPI, RACI, etc.).

The glossary also includes a doctype reference section explaining the library's doctype vocabulary (Annex, Charter, Framework, Guideline, Matrix, Plan, Policy, Procedure, Register, Roadmap, SOP, Specification, Standard, Template).

### Scope distinction established

Two related registers now serve complementary purposes:

- **[`register-glossary.md`](governance/register-glossary.md)** (new): acronyms and external-domain terms (regulations, standards, frameworks, regulators, sector programmes, technical concepts).
- **[`register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md)** (existing, 1.1.0 → 1.1.1): library-internal GRC concepts (Audit, Authorize, Control, Owner roles, Exception, etc.).

Both registers now cross-reference each other and explain their scope distinction in their Purpose sections.

### Cross-references updated

- `governance/README.md`: glossary entry added to the Active Documents table.
- `governance/register-document-index-and-classification.md` (1.25.0 → 1.25.1): glossary entry added.
- `TODO.md`: P1.1 (glossary) removed; remaining P1 items renumbered.

All ten audits clean.

## Phase 21.1 (2026-05-28): Backlog file established

First sub-phase of Phase 21 (project foundations before content expansion). Introduces `TODO.md` at the repository root as the canonical living backlog. Completed work is recorded here in `CHANGELOG.md`; pending work is recorded in `TODO.md`. The two files together form the project's working history-and-future record.

### New file

- `TODO.md` (root, no metadata block per convention for root meta-files): seeded with the prioritised enhancement list discussed during Phase 20 review. Six priority tiers from foundations (glossary, standards-currency checker) through content expansion (logistics country additions, financial-services regulators, healthcare/energy/telecom/public-sector country overlays, AI jurisdictions, privacy jurisdiction gaps) to domain-level expansion (cloud, OT/ICS, identity, PQC, cross-framework matrix expansion).

### Rationale

The project has been growing in scope across Phases 19 and 20 with a number of deferred items captured only in conversation. Capturing them in a tracked file in the repository ensures:
- Continuity across sessions, contributors, and AI-assisted authorship cycles.
- Honest disclosure of what's queued versus what's done.
- A natural prioritisation framework before scaling country and sector content.

### Convention established

Root-level meta-files (`README.md`, `NOTICE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `TODO.md`) are maintained at a simpler standard than tracked governance artefacts: no full 13-field metadata block, no per-document version tracking, no taxonomy or portal inclusion. They are informational and operate as project meta-infrastructure rather than tracked GRC content.

All ten audits clean.

## Phase 20.2 (2026-05-28): Other industry-sector sub-directories

Second sub-phase of Phase 20. Phase 20.1 established the `compliance/<sector>/` sub-directory pattern for logistics. Phase 20.2 applies the same pattern to the remaining five industry sectors so that all sector-conditional compliance content lives under its respective sector sub-directory.

### Sub-directories created

- `compliance/financial-services/` — banks, investment firms, insurers, payment institutions, financial-market infrastructures.
- `compliance/healthcare/` — healthcare providers, payers, medical-device manufacturers, healthcare technology platforms.
- `compliance/energy-and-utilities/` — electricity, gas, water, district heating, renewable-energy operators.
- `compliance/telecommunications/` — telecom network operators, ISPs, internet exchange points, electronic communications service providers.
- `compliance/public-sector/` — government agencies, public bodies, and cloud-service providers to public sector.

Each sub-directory has a `README.md` (v1.0.0) describing the sector, applicability, the artefacts within, and future-coverage placeholders for country/regulator-specific overlays.

### Files moved

| Origin | Destination | Notes |
| --- | --- | --- |
| `compliance/annex-financial-services-sector-requirements.md` | `compliance/financial-services/annex-financial-services-sector-requirements.md` | Path move; version bump |
| `compliance/annex-dora-implementation.md` | `compliance/financial-services/annex-dora-implementation.md` | EU financial-services regulation; path move |
| `compliance/annex-sox-itgc.md` | `compliance/financial-services/annex-sox-itgc.md` | US financial-services regulation; path move |
| `compliance/annex-healthcare-sector-requirements.md` | `compliance/healthcare/annex-healthcare-sector-requirements.md` | Path move |
| `compliance/annex-energy-and-utilities-sector-requirements.md` | `compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md` | Path move |
| `compliance/annex-telecommunications-sector-requirements.md` | `compliance/telecommunications/annex-telecommunications-sector-requirements.md` | Path move |
| `compliance/annex-public-sector-requirements.md` | `compliance/public-sector/annex-public-sector-requirements.md` | Path move |
| `compliance/annex-fedramp-requirements.md` | `compliance/public-sector/annex-fedramp-requirements.md` | US federal cloud regulation; path move |

### Held at `compliance/` root (horizontal cross-sector regulation)

- `compliance/annex-nis-2-implementation.md` — EU NIS 2 Directive applies to "essential and important entities" across energy, transport, banking, healthcare, digital infrastructure, and other sectors. Not naturally one sector. Stays at root.

### Library-wide cross-reference updates

- All references to the eight moved files (across ~10 documents) updated to new paths.
- Internal sibling references within moved files updated from `../security/` to `../../security/` style (the files are now one level deeper).
- Internal compliance-sibling references in moved files updated from `(filename.md)` to `(../filename.md)`.
- `compliance/README.md` (1.3.0 → 1.4.0): sector sub-directory table expanded to list all six sectors; per-sector artefact tables added.

### Result

The compliance domain now consistently organises sector-specific content under sub-directories: `logistics/`, `financial-services/`, `healthcare/`, `energy-and-utilities/`, `telecommunications/`, `public-sector/`. The pattern scales to new sectors (when added) and to country-specific regulator overlays within each sector (as adopters require).

All ten audits clean. Taxonomy and portal regenerated.

## Phase 20.1 (2026-05-28): Logistics sector consolidation

First sub-phase of Phase 20 (compliance sub-directory restructure). Phase 12.3 had moved BASC into a new `/sectors/` top-level directory, which was inconsistent with the established pattern of sector-specific content living in `/compliance/` (where AEO-UK, CTPAT, PIP, and the sector annexes already lived). Phase 20.1 reverses that misstep and establishes the `compliance/<sector>/` sub-directory pattern, beginning with logistics.

### What changed

The library now hosts all trade-and-logistics sector-conditional content in a single `compliance/logistics/` sub-directory. The `/sectors/` directory has been deleted entirely.

### Files moved into `compliance/logistics/`

| Origin | Destination | Notes |
| --- | --- | --- |
| `sectors/basc/policy-basc-information-security.md` | `compliance/logistics/policy-basc-information-security.md` | Path move; version 1.1.1 |
| `sectors/basc/register-basc-it-responsibilities.md` | `compliance/logistics/register-basc-it-responsibilities.md` | Path move; version 1.1.1 |
| `sectors/basc/register-basc-it-compliance-kpis.md` | `compliance/logistics/register-basc-it-compliance-kpis.md` | Path move; version 1.1.1 |
| `sectors/basc/README.md` | `compliance/logistics/annex-basc-programme-overview.md` | Doctype conversion (Register → Annex); content preserved; version 1.1.0 |
| `compliance/annex-transportation-and-logistics-sector-requirements.md` | `compliance/logistics/annex-logistics-sector-requirements.md` | Renamed; sector overview; title shortened to "Logistics Sector GRC Requirements Annex"; version 1.0.1 |
| `compliance/annex-aeo-s-it-cybersecurity-requirements.md` | `compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md` | Renamed for jurisdiction clarity; title "UK AEO-S IT and Cybersecurity Requirements"; version 1.0.1 |
| `compliance/procedure-aeo-it-self-assessment.md` | `compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md` | Renamed; title "UK AEO IT Self-Assessment Procedure"; version 1.0.1 |
| `compliance/register-ctpat-it-controls.md` | `compliance/logistics/register-ctpat-united-states-it-controls.md` | Renamed; title "US CTPAT IT and Cybersecurity Compliance Controls Register"; version 1.0.2 |
| `compliance/register-pip-compliance-controls.md` | `compliance/logistics/register-pip-canada-controls.md` | Renamed; title "Canada PIP IT and Cybersecurity Compliance Controls Register"; version 1.0.1 |
| `supply-chain/register-ctpat-full-msc-controls.md` | `compliance/logistics/register-ctpat-united-states-msc-controls.md` | Cross-domain move; renamed; title "US CTPAT Full Minimum Security Criteria Controls Register"; version 1.0.2 |
| `compliance/template-trade-compliance-gap-assessment.md` | `compliance/logistics/template-trade-compliance-gap-assessment.md` | Path move; version 1.0.1 |

### New files

- `compliance/logistics/README.md` (new, v1.0.0): sector home, programme index, applicability, future-coverage placeholders.

### Files deleted

- `sectors/README.md` and `sectors/basc/README.md`: content preserved as `annex-basc-programme-overview.md` and consolidated into the new `compliance/logistics/README.md`.
- `sectors/` directory removed entirely.

### Library-wide cross-reference updates

- All `[\`sectors/\`](../sectors/)` pointers (44 across the library, introduced in Phase 19.1/19.4) updated to point to `[\`compliance/\`](../compliance/)`.
- All references to renamed files (CTPAT/AEO/PIP/transport-annex/trade-template) updated to new paths and filenames.
- `supply-chain/README.md` (1.2.0 → 1.3.0): CTPAT MSC register row removed (file moved to compliance/logistics/); trusted-trader programme list replaced with a pointer to `compliance/logistics/`.
- `compliance/README.md` (1.2.0 → 1.3.0): restructured to describe the root-vs-sector layer separation; logistics sub-directory artefacts listed; pending Phase 20.2 sector moves flagged.
- `governance/register-document-index-and-classification.md` (1.24.2 → 1.25.0): all moved/renamed entries updated; category labels normalised from "Sectors" to "Compliance" for the BASC artefacts.
- `README.md` (1.5.3 → 1.5.4): document-count description updated to reference compliance sub-directories rather than `/sectors/`.
- `specification-master-project.md` (1.2.6 → 1.2.7): repository directory listing and domain table updated.
- `docs/adopter-guide.md`: "The sectors directory" section replaced with "Sector-conditional content".

### Tooling update

- `tools/lint-structure.py`: removed `sectors` from the `DOMAINS` list (the directory no longer exists). The structural-membership rule now requires that all `compliance/logistics/*` files are referenced by `compliance/README.md`, which they are.

### Result

The library now has one consistent home for sector-conditional compliance content. The logistics sub-directory pattern is established and ready to scale to the 90+ AEO/equivalent trusted-trader programmes globally. Future country-specific programme additions (Mexico NEEC, Australia ATT, Singapore STP, EU AEO, Japan AEO, etc.) drop into `compliance/logistics/` with no additional structural change.

The Phase 20.2 sub-phase will apply the same sub-directory pattern to the other industry sectors (financial-services, healthcare, energy-and-utilities, telecommunications, public-sector).

All ten audits clean. Taxonomy and portal regenerated.

## Phase 19.6 (2026-05-28): ISO/IEC 42005 and 42006 topic-attribution correction

Phase 19 sub-phase 6, resolving the topic-attribution concern flagged in the Phase 19.4 changelog. ISO/IEC 42006:2025 covers "Requirements for bodies providing audit and certification of artificial intelligence management systems" — that is, requirements for accreditation bodies who audit and certify AIMS implementations against ISO/IEC 42001. It is the AIMS analogue of ISO/IEC 27006 (which provides the equivalent requirements for ISO/IEC 27001 audit bodies). The standard covering AI impact assessment guidance is ISO/IEC 42005:2025, published in May 2025.

Several documents in the library had been authored before ISO/IEC 42005 was published and had assigned the AI Impact Assessment topic to ISO 42006 by mistake. Phase 19.6 corrects the attribution.

### Citations corrected (topic was impact-assessment, attribution moved to ISO/IEC 42005:2025)

- `ai/procedure-ai-evaluation.md` (1.0.1 → 1.0.2): framework alignment row updated to "ISO/IEC 42005:2025 | AI system impact assessment | Risk and bias evaluation".
- `ai/standard-ai-testing-validation-and-documentation.md` (1.0.0 → 1.0.1): Purpose paragraph alignment list and framework alignment row both updated to ISO/IEC 42005:2025.
- `privacy/procedure-privacy-impact-and-cross-border-transfer.md` (1.3.1 → 1.3.2): Step 5 consultation rule ("AIGC conducts additional review per ISO 42006") and the framework-mapping table row ("AI Impact Assessment | ISO 42006") both updated to ISO/IEC 42005:2025.
- `security/policy-acceptance-into-service.md` (1.0.0 → 1.0.1): rule 4.3 ("AI Impact Assessments must evaluate transparency, fairness, and explainability per ISO 42006") updated to ISO/IEC 42005:2025.
- `governance/register-document-index-and-classification.md` (1.24.1 → 1.24.2): three index rows updated where the document's topic is impact assessment — AI System Impact Assessment Procedure, AI Testing/Validation/Documentation Standard, AI Evaluation Procedure.

### Citations clarified (topic was audit/certification, attribution retained as ISO 42006 with status updated)

- `ai/register-model-registry.md` (0.0.1 → 0.0.2): "ISO/IEC 42006 | AI system audit | Audit baseline" updated to "ISO/IEC 42006:2025 | Requirements for AIMS audit and certification bodies | Audit baseline" to make the actual scope of the standard explicit. The model registry's use of ISO 42006 for audit-baseline context is correct.
- `governance/register-document-index-and-classification.md`: two index rows where the topic is audit/certification — AI System Audit and Certification Framework, Model Registry — kept ISO 42006 attribution and updated to "ISO/IEC 42006:2025".

### Standards now correctly cited in the library

| Standard | Scope | Citation context |
|---|---|---|
| ISO/IEC 42001:2023 | AI management system requirements | All AI governance, lifecycle, and assurance documents |
| ISO/IEC 42005:2025 | AI system impact assessment guidance | Impact assessment procedure, evaluation procedure, testing-validation-documentation standard, privacy impact procedure, acceptance-into-service policy |
| ISO/IEC 42006:2025 | Requirements for bodies providing audit and certification of AIMS | AI System Audit and Certification Framework, Model Registry, document index rows for audit-related artefacts |

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.5 (2026-05-28): Document count and BrE licence normalisation

Phase 19 sub-phase 5. Two low-severity findings.

### L-1: README document count

- `README.md` (1.5.2 → 1.5.3, patch-level per the main-README rule): the document count description said "approximately **240 documents**". Actual count: 282 documents in active domain directories (`ai/`, `architecture/`, `compliance/`, `dev-security/`, `governance/`, `operations/`, `privacy/`, `resilience/`, `risk/`, `security/`, `supply-chain/`, `sectors/`), excluding domain READMEs. Updated to "approximately **280 documents**" — still an approximation as the description states, with the actual count expected to fluctuate as Phase 19 sub-phases progress.

### L-2: BrE licence noun normalisation (body content)

The library uses Oxford English (BrE word stems + `-ize` verb endings). The noun `license` in body content was inconsistent with the convention — BrE uses `licence` for the noun and `license` for the verb. The metadata field name `License` and the `LICENSE` repository-root file are GitHub conventions left as-is.

Files updated:

- `NOTICE.md` (1.0.0 → 1.0.1): title and 3 body usages (incl. document title "External Reference Materials and Licence Boundaries").
- `README.md` (1.5.2 → 1.5.3): 2 body usages plus the L-1 count change.
- `CONTRIBUTING.md`: 3 body usages (no metadata block; not version-tracked).
- `specification-master-project.md` (1.2.5 → 1.2.6): Review Frequency field reference and one body usage.
- `specification-ingestion.md` (1.4.2 → 1.4.3): Review Frequency field reference, section heading "Licence compatibility rules", and 2 body usages.
- `instruction-ai-document-ingestion.md`: 2 body usages (no metadata block; not version-tracked).
- `ai/framework-ai-governance-and-risk.md` (1.1.0 → 1.1.1): 1 body usage.
- `ai/README.md`: section heading "Licence boundary".
- `governance/register-document-index-and-classification.md` (1.24.0 → 1.24.1): 1 body usage.
- `governance/README.md`: section heading "Licence boundary" and 1 body usage.
- `governance/charter-governance-library.md` (1.1.0 → 1.1.1): Review Frequency field reference, 3 body usages, and 1 role-name body usage ("Licence Reviewer").
- `governance/matrix-cross-framework-alignment.md` (1.1.1 → 1.1.2): 1 body usage.
- `risk/standard-enterprise-risk-management.md` (1.3.1 → 1.3.2): section heading "Licence" and 1 body usage.
- `risk/policy-enterprise-governance-and-risk-management.md` (1.4.0 → 1.4.1): section heading "Licence".
- `compliance/financial-services/annex-financial-services-sector-requirements.md` (1.0.0 → 1.0.1): 1 body usage.
- `compliance/register-compliance-obligations-template.md` (1.0.1 → 1.0.2): 1 body usage.
- `dev-security/standard-developer-security-requirements.md` (1.0.0 → 1.0.1): 1 body usage.
- `dev-security/standard-security-quick-reference.md` (1.0.0 → 1.0.1): 2 body usages.
- `dev-security/standard-software-composition-analysis.md` (1.1.0 → 1.1.1): section heading and 11 body usages (table column header "Licence Category", row headers, and inventory obligations bullets).
- `dev-security/standard-software-evaluation-acceptance-and-lifecycle.md` (1.0.0 → 1.0.1): 1 body usage.
- `dev-security/standard-devops-security-requirements.md` (1.0.1 → 1.0.2): 1 body usage.
- `dev-security/guideline-ai-coding-assistant-security.md` (1.0.1 → 1.0.1 — already bumped in Phase 19.4): 1 body usage (checklist label).
- `dev-security/claude-rules/README.md`: section heading "Licence".
- `dev-security/claude-rules/CLAUDE.md`: 1 body usage (no metadata block; not version-tracked).
- `dev-security/claude-rules/pipeline/cicd-gates.md`: 1 body usage (no metadata block; not version-tracked).
- `dev-security/claude-rules/ai/ai-security.md`: 2 body usages (no metadata block; not version-tracked).
- `operations/standard-certificate-authority-management.md` (1.3.0 → 1.3.1): 2 body usages.
- `operations/register-asset-inventory.md` (1.0.0 → 1.0.1): 1 body usage (table row label).
- `resilience/README.md`: section heading "Licence boundary".
- `sectors/README.md`: section heading "Licence and neutrality posture".
- `compliance/logistics/annex-basc-programme-overview.md`: section heading "Licence boundary".
- `security/README.md`: section heading "Licence boundary".
- `security/procedure-security-incident-response.md` (1.3.2 → 1.3.3): section heading "Licence".
- `security/procedure-onboarding-and-offboarding.md` (1.0.0 → 1.0.1): 1 body usage.
- `supply-chain/README.md`: section heading "Licence boundary".

Additionally, the `Unlicenced` spelling in `standard-software-composition-analysis.md` was corrected to `Unlicensed` (BrE/AmE shared participle adjective form; `Unlicenced` is non-standard in both).

### Not converted

- `License` as the metadata field name (defined library convention): kept (specification-master-project.md, specification-ingestion.md, instruction-ai-document-ingestion.md, docs/adopter-guide.md, tools/README.md).
- The `LICENSE` repository-root file: GitHub convention; kept.
- `licensed` (past-participle adjective): same spelling in BrE and AmE; kept.

### Result

Body content is now consistent BrE: `licence` (noun) and `license` (verb), parallel to the existing `practice/practise`, `defence/defend`, `analyse/analysis` patterns. The metadata field name `License` and the `LICENSE` file remain as GitHub-convention exceptions, documented above.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.4 (2026-05-28): Standards-currency and BASC-residue cleanup

Phase 19 sub-phase 4. Three findings from the exhaustive re-audit: an obsolete ISO 42006 status reference; a guideline document containing 11 normative `must` statements that belong in a standard, not a guideline; and additional baseline `Regional BASC Compliance Officer` references that Phase 12.3 and Phase 19.1 had not reached.

### M-1: ISO/IEC 42006 status correction

- `ai/framework-ai-system-audit-certification.md` (1.0.0 → 1.0.1): the framework cited "ISO/IEC 42006 (draft 2024)" in its framework alignment table and "the ISO/IEC 42006 draft AI audit requirements" in its Purpose. The standard was published in 2025; references updated to "ISO/IEC 42006:2025".

A separate concern was flagged but not silently corrected: several documents (notably `procedure-ai-evaluation.md`, `standard-ai-testing-validation-and-documentation.md`, multiple register-document-index rows, `procedure-privacy-impact-and-cross-border-transfer.md`, and `policy-acceptance-into-service.md`) cite "ISO 42006" with the topic attribution "AI Impact Assessment". ISO/IEC 42006:2025 is the standard for bodies providing audit and certification of AI management systems; the AI-impact-assessment standard is ISO/IEC 42005:2025. Whether to retain the existing citations or correct them to ISO 42005 is left for the user's review in a subsequent pass — the topic-attribution correction is materially distinct from a status update.

### M-2: AI coding assistant guideline `must` → `should`

- `dev-security/guideline-ai-coding-assistant-security.md` (1.0.0 → 1.0.1): 11 normative `must` statements softened to `should` so the document language matches its Guideline doctype. The substantive content (security rules loaded before generating code; tool access scoped to the minimum necessary; no standing write access to production; no direct push to main without human review; agentic sessions logged; destructive actions require human confirmation) is retained — only the modal verb is changed. Adopters who wish to enforce these requirements upgrade the document to a Standard or Policy in their own copy of the library.

### M-3: BASC baseline residue cleanup

Phase 12.3 moved BASC to a sector overlay, and Phase 19.1 closed four files. The exhaustive re-audit found 13 additional documents that still treated `Regional BASC Compliance Officer` as a baseline role or that retained dedicated BASC sections. Phase 19.4 cleans those:

- `governance/framework-metrics-monitoring-and-performance-reporting.md` (1.0.0 → 1.0.1)
- `governance/framework-continuous-assurance-and-improvement.md` (1.0.0 → 1.0.1)
- `compliance/policy-legal-and-regulatory-compliance.md` (1.0.0 → 1.0.1)
- `supply-chain/procedure-supplier-audit.md` (1.0.1 → 1.0.2)
- `operations/procedure-media-handling-and-transport.md` (1.3.0 → 1.3.1)
- `operations/procedure-security-monitoring-and-alert-management.md` (1.3.0 → 1.3.1)
- `privacy/procedure-data-protection-and-privacy-breach-response.md` (1.4.0 → 1.4.1)
- `security/sop-incident-escalation-matrix.md` (1.2.0 → 1.2.1)
- `security/framework-cryptographic-key-lifecycle.md` (1.0.0 → 1.0.1)
- `security/standard-logging-and-monitoring.md` (1.4.0 → 1.4.1)
- `security/policy-network-communications-security.md` (1.0.0 → 1.1.0): had a dedicated `BASC trade-network security controls` section with multiple programme-specific requirements; replaced with a `Sector-programme network security overlays` section that defers to `sectors/`. Minor version bump because the change replaced a numbered section.
- `security/procedure-security-incident-response.md` (1.3.1 → 1.3.2)
- `security/policy-encryption-and-key-management.md` (1.3.0 → 1.3.1)
- `security/standard-data-classification-and-handling.md` (1.3.0 → 1.3.1): the dedicated `BASC and regional trade data handling` section was generalised to `Sector-programme data handling overlays` with deference to `sectors/`.

### Result

Across the four post-12.3 cleanup phases (12.3 initial, 19.1, 19.4), the BASC overlay is now consistently positioned: BASC appears as a named example of a sector programme in the running text, never as a baseline role, scoping assumption, or unconditional framework requirement. Where the user's organisation participates in BASC, the `compliance/logistics/` annex remains the authoritative source for the additional controls, roles, and timeframes.

Taxonomy and portal regenerated. All ten audits clean.

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
- `compliance/logistics/annex-basc-programme-overview.md` (new, v1.0.0): BASC sub-register describing applicability and listing active BASC documents.

### Files moved (git history preserved via `git mv`)

- `compliance/policy-basc.md` → `compliance/logistics/policy-basc-information-security.md` (v1.0.0 → v1.1.0; renamed to reflect canonical naming; Category updated from "Compliance Management" to "Sector Annex"; cross-references updated)
- `compliance/register-basc-it-responsibilities.md` → `compliance/logistics/register-basc-it-responsibilities.md` (v1.0.0 → v1.1.0; same updates)
- `compliance/register-basc-it-compliance-kpis.md` → `compliance/logistics/register-basc-it-compliance-kpis.md` (v1.0.0 → v1.1.0; same updates)

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

- `compliance/public-sector/annex-fedramp-requirements.md`: applicability triggers, authorisation route selection (JAB, Agency, FedRAMP Tailored, FedRAMP Ready), baseline selection mapped to FIPS 199, library coverage per NIST SP 800-53 Rev 5 control family, eight named library gaps requiring additional documentation (SSP, ConMon, POA&M, SAR/SAP, OMB M-22-09 reporting, FIPS-validated cryptography, federal personnel investigations, CUI handling).
- `compliance/financial-services/annex-dora-implementation.md`: per-pillar mapping for ICT risk management (Articles 5 to 16), ICT-related incident reporting (Articles 17 to 23 with 4-hour, 72-hour, one-month windows), digital operational resilience testing including TLPT under TIBER-EU, ICT third-party risk including Article 30 minimum clauses and the critical-ICT-third-party Oversight Framework, information and intelligence sharing.
- `compliance/annex-nis-2-implementation.md`: entity classification (Essential and Important under Annexes I and II), per-sub-measure mapping of Article 21 risk-management measures, Article 20 management body responsibilities and training, the four-stage incident reporting regime under Articles 23 to 25 (early warning, incident notification, intermediate, final), six library gaps requiring additional documentation.
- `compliance/public-sector/annex-public-sector-requirements.md`: eight overlay areas (freedom of information, accessibility under WCAG 2.2 AA and EN 301 549, public procurement, records management, audit and external scrutiny, ethics and lobbying, AI in the public sector, official languages), library coverage per overlay, seven library gaps.
- `compliance/telecommunications/annex-telecommunications-sector-requirements.md`: seven overlay areas (sector cybersecurity, lawful interception, data retention, sector customer privacy, emergency calling and resilience, vendor and supply-chain restrictions, numbering and addressing resources), regime references for EU EECC, EU NIS 2, UK Telecommunications (Security) Act 2021, US CALEA, FCC, and equivalents.
- `compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`: six overlay areas (critical-infrastructure cybersecurity baselines, OT and ICS cybersecurity, physical-cyber convergence, sector incident reporting, supplier and component security, resilience and continuity), per-control area mapping for OT including network segmentation, OT vulnerability management, vendor remote access to OT, OT incident response.
- `compliance/financial-services/annex-sox-itgc.md`: ICFR scope determination, four ITGC domains (access to programs and data, program changes, program development, computer operations) with library coverage per control objective, auditor-expected artefacts beyond the library, coordination with adjacent regimes (SOC 1, PCI DSS, GDPR, NIST CSF, ISO 27001).

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
