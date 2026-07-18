# Governance, Risk, and Compliance Documentation Library

**Date:** 2026-07-18\
**Classification:** Public\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Library Version:** 2026.07.494 (CalVer, library-wide; see [`specification-master-project.md`](specification-master-project.md) §4.5)\
**README Version:** 1.9.855 (semantic per-document version for this file)

---

## New to GRC? Start here

**GRC** stands for **Governance, Risk, and Compliance**: three interlocking disciplines an organization uses to align its activities with strategy, manage uncertainty, and meet legal, regulatory, and contractual obligations.

- **Governance** establishes who decides, who is accountable, and how decisions are made. Charters, policies, role registers, and approval-authority models are governance artefacts.
- **Risk management** identifies, evaluates, and treats threats to the organization's objectives. Risk registers, treatment plans, and acceptance records are risk artefacts.
- **Compliance** ensures that the organization meets external obligations (laws, regulations, standards, contracts) and internal policy. Obligation registers, control mappings, and audit-evidence packages are compliance artefacts.

In modern programmes the boundaries between the three overlap with **security** (protecting information and systems), **privacy** (handling personal data lawfully), **resilience** (continuing operations under disruption), **supplier/third-party governance** (managing risk that originates outside the organization), and **AI governance** (managing the risk introduced by AI systems). This library treats all of those as sibling domains under the GRC umbrella because organizations operate them together.

**This README orients first-time readers and contributors to the library as a whole.** Most adopters do not need to read it end-to-end. If you already know what you are here for, the canonical adopter entry is [`docs/portal.md`](docs/portal.md), which routes by role and intent:

| If you are ... | Start at |
| --- | --- |
| New to GRC, or evaluating the library | Continue reading §Purpose below, then [`docs/portal.md`](docs/portal.md). |
| Unsure which documents apply to your situation | [`docs/decision-tree.md`](docs/decision-tree.md) (the guided reading-order decision tree), then [`docs/portal.md`](docs/portal.md). |
| An adopter setting up a programme | [`docs/portal.md`](docs/portal.md) (canonical front door), then [`docs/adopter-guide.md`](docs/adopter-guide.md) and [`docs/template-quickstart.md`](docs/template-quickstart.md). |
| An auditor or reviewer assessing scope | [`docs/portal.md`](docs/portal.md) and [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md). |
| A maintainer or contributor | [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`specification-master-project.md`](specification-master-project.md). |
| Looking up an unfamiliar acronym or regulator | [`governance/register-glossary.md`](governance/register-glossary.md) and [`governance/register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md). |

---

## Purpose

The Governance, Risk, and Compliance Documentation Library is a Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) reference set for building an organization-neutral governance, risk, compliance, security, privacy, resilience, supplier, and artificial intelligence governance programme.

The library is designed to be adopted, adapted, or extended by any organization without retaining references to a specific company, individual, internal system, customer, vendor, geography, or operating environment.

The repository provides reusable artefacts across the following thematic areas:

- Enterprise governance, risk, compliance, audit, and assurance.
- Information security, identity, access, logging, data classification, incident response, and secure engineering.
- Privacy, data protection, retention, breach response, and data subject rights.
- Artificial intelligence governance, data security, model risk, lifecycle control, and assurance.
- Business continuity, crisis management, disaster recovery, and operational resilience.
- Supplier, third-party, cloud, and supply-chain governance.
- Cross-framework mapping, regulatory applicability analysis, and metrics.

The seven thematic areas above span 11 governance domain directories, and the library grows by routine PR cadence; the current document inventory is machine-generated on every change and lives in [`taxonomy.yml`](taxonomy.yml) (one row per active artefact with canonical metadata). For an audience-keyed view of the same inventory, see [`docs/portal.md`](docs/portal.md). The `compliance/` domain hosts sector-conditional sub-directories ([`compliance/logistics/`](compliance/logistics/), [`compliance/financial-services/`](compliance/financial-services/), [`compliance/healthcare/`](compliance/healthcare/), and others) for organizations operating in those sectors or participating in covered programmes.

---

## What this repository is

This repository is, primarily, a **GRC documentation corpus**: organization-neutral, CC BY-SA 4.0 governance artefacts (charters, frameworks, policies, standards, procedures, registers, matrices, plans, guidelines, templates) across the eleven domains listed above. The corpus is the product an adopter takes away.

The corpus is maintained by a small team using Claude Code as an AI coding assistant, under documented governance and discipline. To keep the corpus internally consistent under that maintenance model, the project carries an audit toolchain ([`tools/`](tools/), the multi-gate audit programme under [`tools/run_all_audits.sh`](tools/run_all_audits.sh)) and a Claude Code rules-and-skills pack at [`dev-security/claude-rules/`](dev-security/claude-rules/). The audit toolchain is the maintainer's quality-assurance machinery, not an adopter dependency: adopters who only consume the corpus do not need it. Adopters who want the same maintenance discipline for their own fork can adopt the toolchain (it is permissively licensed and copy-paste portable), but doing so is optional. The pack distils the maintenance disciplines into reusable rules that ship under CC BY-SA 4.0 alongside the corpus: an adopter who is not building a GRC library can still take the pack for use on any project. The pack is a by-product of the corpus's maintenance, not a parallel deliverable.

The audit gates and the pack rules grew out of the corpus, not the other way around. Audit gates were added in response to specific drift modes observed in the corpus. Pack rules were extracted from real failure modes the maintainer encountered while keeping the corpus consistent (evidence-grounded completion came from a stale-claim incident; clarify-before-acting from "always confirm" feedback; action-before-explanation-of-inaction from a merge-blocked incident). The corpus is the headline; the maintenance discipline is the methodology that keeps the headline honest.

### Three adoption modes

An adopter can engage with this repository at any of three levels:

- **Fork the whole repo.** You want both the GRC corpus and the maintenance toolkit. Your organization forks, substitutes organization-specific values across the artefacts, and inherits the audit programme and the pack as the operational layer your AI coding assistant uses to keep the corpus consistent. See [`docs/adopter-guide.md`](docs/adopter-guide.md) for the full path.

- **Adopt the corpus only.** You want the Markdown artefacts as a starting point and have your own maintenance workflow (or no AI assistance in the loop). Take the domain directories you need; ignore [`tools/`](tools/) and [`dev-security/claude-rules/`](dev-security/claude-rules/). The CC BY-SA 4.0 share-alike clause applies to derivatives you redistribute.

- **Adopt the pack only.** You are not building a GRC library, but you want a Claude Code baseline pack, usable on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. Take [`dev-security/claude-rules/`](dev-security/claude-rules/) (the pack's own [`README.md`](dev-security/claude-rules/README.md) is its front door) and drop it into your project's Claude Code context. For an automated, AI-assisted installation that tailors the pack to your specific project, see the setup generator prompt at [`dev-security/claude-rules/setup-generator-prompt.md`](dev-security/claude-rules/setup-generator-prompt.md). The pack ships with its own version sequence and is documented to operate standalone.

The third mode is an emergent use that has been adopted by developers in practice; it is supported alongside the primary fork-the-whole-repo path.

---

## How to use

1. **Start at the audience-keyed portal.** [`docs/portal.md`](docs/portal.md) is the primary navigation point: it groups the corpus by reader role (CIO, Board / CEO, CISO, GRC, Security Architecture, Privacy, Compliance, Audit, Resilience, Engineering) and lists the documents most likely to be useful to each audience. If you already know what you are looking for, the full machine-auditable document index is at [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), which lists every document with its type, domain, status, and related artefacts.

2. **Identify the documents relevant to your programme.** Begin with the Day-1 floor and the Tier 1 starter set (see [`docs/template-quickstart.md`](docs/template-quickstart.md) and [`docs/adopter-guide.md`](docs/adopter-guide.md)), then grow toward the Core reference set below and into domain-specific standards and procedures as the programme matures.

3. **Copy and adapt.** All content is CC BY-SA 4.0. Copy documents into your own repository (attributing the library per CC BY-SA 4.0) and substitute organization-specific values: role names, jurisdiction, sector, system names, risk appetite, and contact details. If you redistribute the resulting derivative, the CC BY-SA 4.0 "ShareAlike" condition requires you to release that derivative under CC BY-SA 4.0 as well.

4. **Validate applicability.** Not every document applies to every organization. Validate that each document's scope, jurisdictional references, and control requirements match your operating environment, sector, and regulatory obligations before adoption.

5. **Review the contribution and authoring specifications.** If extending or maintaining the library, see the root-level specification files described in the section below.

---

## Operating position

This repository is intended to become an authoritative CC BY-SA 4.0 GRC library. Authoritative means that the repository maintains a coherent hierarchy, controlled document model, versioned artefacts, role-based accountability, traceable mappings, and clear boundaries between original library content and external reference materials.

This repository is not legal advice, audit certification, regulatory approval, or a substitute for organization-specific risk acceptance. Adopting organizations must validate applicability, control implementation, and evidence against their own jurisdiction, sector, contractual obligations, processing role, threat model, and risk appetite.

---

## Repository structure

Documents are organized by primary governance domain.

```text
/governance     Enterprise authority: library charter, document architecture, cross-framework alignment,
                role authority, terminology, metrics, and governance and risk management policies.

/risk           Enterprise risk management: standard, risk register procedure, and risk acceptance procedure.

/compliance     Compliance management, audit governance, CAPA (Corrective and Preventive Action), regulatory applicability register,
                and trade compliance programme references (logistics-specific; skip if not applicable):
                CTPAT (US Customs-Trade Partnership Against Terrorism), BASC (Business Alliance
                for Secure Commerce), PIP (Canada Partners in Protection), AEO (EU Authorised Economic Operator), AEO-S (AEO Security variant), WCO SAFE (World Customs
                Organization SAFE Framework of Standards), and ISO 28000 (supply-chain
                security management).

/security       Information security governance: policies, identity, access, logging, data classification,
                cryptography, personnel security, and secure operations.

/ai             Artificial intelligence governance: frameworks, risk standards, model risk, lifecycle
                controls, impact assessment, and AI-specific assurance artefacts.

/operations     Production and infrastructure security: network and cloud configuration standards,
                physical security, change management, SIEM (Security Information and Event Management) operations, patch management, and endpoint controls.

/resilience     Business continuity, disaster recovery, crisis management, resilience testing,
                and recovery governance.

/privacy        Privacy governance, data protection, transfer assessment, breach response, and
                data subject rights.

/supply-chain   Supplier governance, third-party risk, cloud assurance, supply-chain security,
                and trade continuity programme controls.

/dev-security   Developer and DevOps security: standards, quick reference, compliance gap register,
                and claude-rules/ subdirectory of draggable CLAUDE.md rule files for AI coding sessions.

/architecture   Enterprise architecture practice: framework, decision records, reference architectures,
                technology radar, architecture review, API design, data architecture, and integration architecture.

```

Sector-specific content (financial-services, healthcare, energy-and-utilities, telecommunications, public-sector, logistics) lives under the `compliance/` domain as subdirectories rather than under a separate `/sectors` top-level directory. Sector content is conditional and can be omitted by organizations outside the relevant programme.


Repository infrastructure directories (not used for governance artefacts):

```text
/tools          Stdlib-only Python audit scripts: metadata, language, links, structural index,
                taxonomy generator, adopter portal generator.
/docs           Adopter-facing documentation that is not a governance artefact: adopter guide,
                worked example, auto-generated portal, auto-generated maturity scorecard.
/.github        GitHub Actions workflow that runs the full audit programme (see
                `governance/specification-audit-programme.md` §6 for the canonical gate
                inventory; `tools/run_all_audits.sh` is the local equivalent) on push to
                main and on every pull request.
/taxonomy.yml   Auto-generated machine-readable registry of every active artefact's canonical
                metadata. Regenerated from document metadata by tools/build-taxonomy.py.
/tests          Linter-regression fixtures for the audit toolchain, exercised by the
                regression gate (see tools/run-linter-regression.py).
/.project-governance  The project's OWN governance artefacts (the citation-verification
                cluster), separated from the reusable corpus so an adopter does not consume
                them as their own governance (see .project-governance/README.md).
/.working       Maintainer working state (session handoff, QA-history registers, detailed
                CHANGELOG mirror, improvement log): audit-trail and process records, exempt
                from the corpus audit gates. Adopters may delete it (see .working/README.md).
/TODO.md        Forward-looking maintainer backlog. Not a governance artefact; adopters may delete.
/RESUME.md      Maintainer session-resume pointer. Internal; adopters may delete.
```

Documents use lowercase filenames, single hyphen separators, and a document type prefix.

Examples:

- [`governance/charter-governance-library.md`](governance/charter-governance-library.md)
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)
- [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md)
- [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md)
- [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md)
- [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md)
- [`security/policy-information-security.md`](security/policy-information-security.md)
- [`security/standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md)
- [`ai/framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md)
- [`ai/standard-ai-security-and-risk.md`](ai/standard-ai-security-and-risk.md)
- [`ai/framework-ai-model-risk.md`](ai/framework-ai-model-risk.md)
- [`operations/standard-production-security-requirements.md`](operations/standard-production-security-requirements.md)
- [`resilience/framework-business-continuity-and-resilience.md`](resilience/framework-business-continuity-and-resilience.md)
- [`resilience/procedure-backup-and-recovery.md`](resilience/procedure-backup-and-recovery.md)
- [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md)
- [`supply-chain/framework-supplier-and-cloud-governance.md`](supply-chain/framework-supplier-and-cloud-governance.md)
- [`dev-security/standard-developer-security-requirements.md`](dev-security/standard-developer-security-requirements.md)
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md)

---

## Specification and authoring files

Three root-level files govern how the library is maintained and extended:

| File | Purpose |
| --- | --- |
| [`specification-master-project.md`](specification-master-project.md) | Master project specification: document model, metadata rules, domain structure, quality gates, organization-neutrality requirements, and the library-wide CalVer plus per-document semantic-versioning policy (§4.5). |
| [`specification-ingestion.md`](specification-ingestion.md) | Document ingestion specification: canonical metadata format, allowed types, version numbering, and quality checklist. |
| [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md) | AI-assisted ingestion instructions: step-by-step rules for ingesting documents using an AI coding assistant. |

Contributors and maintainers must read these files before adding or modifying library content.

Additional repository hygiene files:

| File | Purpose |
| --- | --- |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow, metadata block requirements, style rules, filename rules, and review path. |
| [`CHANGELOG.md`](CHANGELOG.md) | Phase-level history of repository changes. |
| [`SECURITY.md`](SECURITY.md) | How to report content accuracy defects, licence concerns, organization or personal data leakage, and tooling defects. |
| [`docs/adopter-guide.md`](docs/adopter-guide.md) | How to fork, adapt, and operate the library inside an adopting organization. |
| [`docs/worked-example.md`](docs/worked-example.md) | End-to-end walkthrough of converting a draft into a library-compliant artefact (ingestion). |
| [`docs/worked-example-adoption.md`](docs/worked-example-adoption.md) | End-to-end walkthrough of one adopter forking the library and running a staged first-year programme (adoption). |
| [`docs/portal.md`](docs/portal.md) | Auto-generated audience-keyed navigation page (CIO, Board / CEO, CISO, GRC, Security Architecture, Privacy, Compliance, Audit, Resilience, Engineering). |
| [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) | Auto-generated per-document maturity classification (Mature, Baseline, Draft). |
| [`tools/README.md`](tools/README.md) | Repository quality tooling: metadata, language, link, structural, taxonomy, and portal generators. |

---

## Document types

The library uses the following artefact types:

| Type | Purpose |
| --- | --- |
| Charter | Establishes authority, mandate, accountability, and decision rights. |
| Principle | States the foundational, cross-cutting production principles (such as integrity and trustworthiness) that frameworks, policies, and standards operationalize. |
| Framework | Defines domain scope, governance model, lifecycle, and integration points. |
| Policy | States binding governance intent and mandatory principles. |
| Standard | Defines measurable control requirements and baselines. |
| Procedure | Defines repeatable multi-actor or cross-functional operational steps for implementing a standard or policy. |
| SOP | Defines a single-actor or narrow team sequence with explicit step ownership for one repeatable task. |
| Plan | Defines coordinated actions for continuity, crisis, incident, recovery, or migration events. |
| Roadmap | Defines a multi-phase forward strategy tied to a strategic outcome with phased milestones and dependencies. |
| Guideline | Provides advisory interpretation of a policy or standard requirement. |
| Guide | Provides technical reference material organized for adoption such as patterns, examples, configuration models, or implementation walkthroughs. |
| Checklist | Provides a structured verification list for a specific process or gate. |
| Register | Records authoritative metadata, ownership, risks, obligations, assets, systems, exceptions, metrics, or evidence. |
| Matrix | Maps relationships among controls, risks, obligations, frameworks, lifecycle stages, and evidence. |
| Specification | Defines technical or structural requirements for artefact creation, data fields, interfaces, or evidence. |
| Template | Provides reusable forms, logs, assessments, or evidence structures. |
| Annex | Provides supplementary domain-specific guidance that remains subordinate to the parent framework, policy, or standard. |
| Worklist | Captures a per-instance working artefact derived from a Template, scoped to one batch or task, and retired when the work closes (the authoritative record migrates to a register or log). |

Type selection notes:

- Procedure versus SOP: a Procedure coordinates several roles. An SOP is a single-actor or narrow team sequence for one repeatable task.
- Plan versus Roadmap: a Plan is event-triggered or schedule-bound coordination. A Roadmap is a multi-phase forward strategy tied to a strategic outcome.
- Guideline versus Guide: a Guideline is advisory interpretation. A Guide is technical reference material organized for adoption.

---

## Canonical metadata

Every document begins with a metadata block in the following format and field order:

```
**Document Title:** <title matching the H1 heading>
**Document Type:** <type from the table above>
**Version:** <x.y.z: three-part semantic versioning; new documents start at 0.0.1>
**Date:** <YYYY-MM-DD>
**Owner:** <role title>
**Approving Authority:** <role title>
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`domain/other.md`](../other-domain/other.md)
**Classification:** Public
**Category:** <domain category>
**Review Frequency:** <cadence statement>
**Repository Path:** [`domain/filename.md`](filename.md)
**Confidentiality:** Public
**License:** CC BY-SA 4.0
```

Related Documents and Repository Path use markdown links. The display text is always the root-relative path (e.g., [`security/policy-information-security.md`](security/policy-information-security.md)). The link target is the path relative to the current file's directory: same-directory files use the bare filename; cross-directory files use `../other-domain/file.md` traversal.

Owners and approving authorities must be role-based, not person-specific. Documents must not include real company names, personal names, internal system names, customer names, vendor names, proprietary service names, IP addresses, domains, tenant identifiers, phone numbers, physical addresses, contract details, incident details, or other identifying information.

---

## Core reference set

This core reference set is the curated catalogue of the library's foundational artefacts across domains; it is the fuller set an adopter grows toward, not the day-one starting point. An adopter begins with the much smaller Day-1 floor and Tier 1 starter set (see [`docs/template-quickstart.md`](docs/template-quickstart.md) and [`docs/adopter-guide.md`](docs/adopter-guide.md)) and adds toward this catalogue as the programme matures. Each artefact below is discoverable by title in the document index ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) and the audience-keyed portal ([`docs/portal.md`](docs/portal.md)); the catalogue here is the grow-toward overview rather than a per-file navigation surface. The foundational artefacts are:

| Domain | Artefact |
| --- | --- |
| Governance | Governance Library Charter |
| Governance | Document Architecture and Interrelationship Framework |
| Governance | Exception and Risk Acceptance Management Policy |
| Governance | Cross-Framework Alignment Matrix |
| Governance | Document Index and Classification Register |
| Governance | Key Terms and Definitions Register |
| Governance | Role Authority Register |
| Governance | Metrics, Monitoring and Performance Reporting Framework |
| Risk | Enterprise Governance and Risk Management Policy |
| Risk | Enterprise Risk Management Standard |
| Risk | Risk Register Procedure |
| Risk | Risk Acceptance Procedure |
| Compliance | Compliance, Audit, and CAPA Management Policy |
| Compliance | Global Regulatory Applicability Register |
| Security | Information Security Policy |
| Security | Acceptable Use Policy |
| Security | Identity and Access Management Policy |
| Security | Security Incident Response Procedure |
| Security | Logging and Monitoring Standard |
| Security | Data Classification and Handling Standard |
| AI | AI Governance and Risk Framework |
| AI | AI Security and Risk Standard |
| AI | AI Model Risk Framework |
| AI | AI Model Risk Standard |
| AI | AI System Impact Assessment Procedure |
| AI | AI Model Risk Assessment Procedure |
| AI | AI System Register Template |
| AI | Model Card Template |
| AI | System Card Template |
| AI | AI Model Risk Control to Lifecycle Mapping Matrix |
| Resilience | Business Continuity and Resilience Framework |
| Resilience | Business Continuity and Disaster Recovery Policy |
| Resilience | Backup and Recovery Procedure |
| Privacy | Privacy and Data Governance Policy |
| Privacy | Record of Processing Activities Template |
| Privacy | Privacy Notice Template |
| Privacy | Data Subject Access Request Workflow Template |
| Supply Chain | Supplier and Cloud Governance Framework |
| Supply Chain | Trade and Supply-Chain Continuity Controls Annex |

---

## Framework alignment model

The library aligns to recognized framework families, including:

- **ISO** (International Organization for Standardization) management system standards.
- **NIST** (United States National Institute of Standards and Technology) cybersecurity and artificial intelligence guidance.
- **COBIT** (Control Objectives for Information and Related Technologies) governance concepts.
- **CSA CCM** (Cloud Security Alliance Cloud Controls Matrix) and **STAR** (Security, Trust, Assurance, and Risk) assurance models.
- **OWASP** (Open Worldwide Application Security Project) work, including Top 10, LLM Top 10, **ASVS** (Application Security Verification Standard), **SAMM** (Software Assurance Maturity Model), and the Cheat Sheet Series.
- **MITRE ATLAS** (Adversarial Threat Landscape for Artificial-Intelligence Systems) and **MITRE ATT&CK** (Adversarial Tactics, Techniques, and Common Knowledge).
- Jurisdiction-specific laws or regulations.

For a fuller glossary of external standards, regulators, and sector programmes, see [`governance/register-glossary.md`](governance/register-glossary.md).

Mappings must distinguish between:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Optional assurance evidence.

Mappings must not imply certification, compliance, conformity, regulatory approval, or operating effectiveness unless the adopting organization has implemented controls, retained evidence, assigned accountable owners, completed review, and accepted residual risk.

---

## Artificial intelligence and data security position

AI governance documents in this repository treat data as the primary risk surface. The lifecycle must address collection, annotation, storage, processing, training, retrieval, inference, monitoring, retention, deletion, and decommissioning.

The AI domain explicitly considers prompt injection, data poisoning, model inversion, membership inference, training data leakage, retrieval leakage, insecure tool use, shadow AI, provenance failure, lineage gaps, retention failure, and unenforceable deletion.

The developer security domain (`/dev-security/`) addresses AI coding assistant security through draggable rule files that enforce security requirements directly in AI-assisted development sessions.

---

## Contribution rules

Contributions must satisfy the following conditions:

1. Content must be original, CC BY-SA 4.0-licensable, and organization-neutral.
2. Content must not include real company names, personal names, internal identifiers, customer details, vendor-specific implementation data, or proprietary evidence.
3. Third-party materials may be used only for non-verbatim reference. The library does not copy external third-party content; it references and synthesizes.
4. Framework references must be accurate, version-aware, and scoped to the stated purpose.
5. Regulatory content must separate obligation from interpretation and must identify where applicability depends on jurisdiction, sector, role, residency, or data category.
6. Documents must maintain role-based ownership and approving authority.
7. New documents must be added to the document index and mapped to parent artefacts where applicable.

---

## Review cadence

The library should be reviewed at least annually and upon material change to major standards, regulatory expectations, assurance models, AI threat patterns, cloud control frameworks, privacy obligations, or operational resilience requirements.

AI, data security, privacy, and cloud assurance content should be reviewed on a 6 to 12 month cadence because control expectations and attack patterns change faster than conventional policy review cycles.

---

## Licence and third-party reference boundary

All original content committed to this repository is released under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Adopters who redistribute the content (in original or modified form) must attribute the library and must release their derivative under CC BY-SA 4.0 as well.

External standards, regulatory texts, control frameworks, questionnaires, implementation guides, audit guides, metrics catalogues, and similar materials remain subject to their own licence terms. This repository may use such materials only as reference inputs for independent synthesis, high-level alignment, terminology normalization, and non-verbatim mapping structures.

Do not copy, redistribute, modify, or embed third-party copyrighted control text, questionnaire text, guidance text, tables, metrics catalogues, or implementation notes into this repository. The library's principle is that it does not copy external third-party content; it references external work by name and synthesizes original commentary. Where a contributor is uncertain whether material is original, the contributor must include only framework identifiers, domain names, high-level alignment notes, and original commentary, not the source text itself.

See [`NOTICE.md`](NOTICE.md) for repository rules governing external reference materials.

---

## Maintained by

Originally created and maintained by **Jeffrey Posluns** ([@jposluns](https://github.com/jposluns), <jeff@posluns.ca>, [LinkedIn](https://linkedin.com/in/jposluns), [ORCID](https://orcid.org/0009-0000-7775-2233)).

The library is released under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). The licence requires attribution of the library when content is redistributed, and requires that derivatives be released under CC BY-SA 4.0 as well (the "ShareAlike" condition). For machine-readable citation metadata see [`CITATION.cff`](CITATION.cff); for full attribution context and acknowledgement of contributors see [`AUTHORS.md`](AUTHORS.md).

---

**End of Document**
