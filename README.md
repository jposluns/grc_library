# Governance, Risk, and Compliance Documentation Library

**Version:** 1.2.0
**Date:** 2026-05-27
**Classification:** Public
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Document Control

| Version | Date | Change History |
| --- | --- | --- |
| 1.0.0 | 2025 11 14 | Initial public GRC Library README. |
| 1.0.1 | 2025 11 16 | Updated structure and governance language. |
| 1.0.2 | 2025 11 18 | Introduced domain directories, canonical metadata, contribution rules, and role-based governance. |
| 1.1.0 | 2026 05 26 | Removed organization and person identifiers, clarified CC0 compatibility, added third-party reference boundaries, and aligned the library to a generic authoritative documentation model. |
| 1.1.1 | 2026 05 26 | Added information security as a primary repository domain and clarified the live corpus expansion model. |
| 1.1.2 | 2026-05-26 | Updated canonical AI model risk and backup recovery path references after repository-wide normalization. |
| 1.2.0 | 2026-05-27 | Restructured repository: dissolved /core/ into /governance/, /risk/, /compliance/; dissolved /policy/ into /governance/ and /compliance/ with richer canonical documents; renamed /supplier/ to /supply-chain/ with broader scope including trade continuity; added /operations/ for production and infrastructure security; added /dev-security/ for developer security standards and draggable Claude Code rule files; moved trade and supply-chain continuity annex from /resilience/ to /supply-chain/. |

---

## Purpose

The Governance, Risk, and Compliance Documentation Library is a CC0-licensed public-domain reference set for building an organization-neutral governance, risk, compliance, security, privacy, resilience, supplier, and artificial intelligence governance programme.

The library is designed to be adopted, adapted, or extended by any organization without retaining references to a specific company, individual, internal system, customer, vendor, geography, or operating environment.

The repository provides reusable artefacts across the following domains:

- Enterprise governance, risk, compliance, audit, and assurance.
- Information security, identity, access, logging, data classification, incident response, and secure engineering.
- Privacy, data protection, retention, breach response, and data subject rights.
- Artificial intelligence governance, data security, model risk, lifecycle control, and assurance.
- Business continuity, crisis management, disaster recovery, and operational resilience.
- Supplier, third-party, cloud, and supply-chain governance.
- Cross-framework mapping, regulatory applicability analysis, and metrics.

---

## Operating Position

This repository is intended to become an authoritative public-domain GRC library. Authoritative means that the repository maintains a coherent hierarchy, controlled document model, versioned artefacts, role-based accountability, traceable mappings, and clear boundaries between original CC0 content and external reference materials.

This repository is not legal advice, audit certification, regulatory approval, or a substitute for organization-specific risk acceptance. Adopting organizations must validate applicability, control implementation, and evidence against their own jurisdiction, sector, contractual obligations, processing role, threat model, and risk appetite.

---

## Licence and Third-Party Reference Boundary

All original content committed to this repository is dedicated to the public domain under CC0 1.0 Universal.

External standards, regulatory texts, control frameworks, questionnaires, implementation guides, audit guides, metrics catalogues, and similar materials remain subject to their own licence terms. This repository may use such materials only as reference inputs for independent synthesis, high-level alignment, terminology normalization, and non-verbatim mapping structures.

Do not copy, redistribute, modify, or embed third-party copyrighted control text, questionnaire text, guidance text, tables, metrics catalogues, or implementation notes into this repository unless the material is confirmed to be compatible with CC0 release. Where compatibility is uncertain or restrictive, include only framework identifiers, domain names, high-level alignment notes, and original commentary.

See `NOTICE.md` for repository rules governing external reference materials.

---

## Repository Structure

Documents are organized by primary governance domain.

```text
/governance     Enterprise authority: library charter, document architecture, cross-framework alignment,
                role authority, terminology, metrics, and governance and risk management policies.

/risk           Enterprise risk management: standard, risk register procedure, and risk acceptance procedure.

/compliance     Compliance management, audit governance, CAPA, regulatory applicability register,
                and trade compliance programme references (CTPAT, BASC, PIP, AEO, AEO-S, WCO SAFE, ISO 28000).

/security       Information security governance: policies, identity, access, logging, data classification,
                cryptography, personnel security, and secure operations.

/ai             Artificial intelligence governance: frameworks, risk standards, model risk, lifecycle
                controls, impact assessment, and AI-specific assurance artefacts.

/operations     Production and infrastructure security: network and cloud configuration standards,
                physical security, change management, SIEM operations, patch management, and endpoint controls.

/resilience     Business continuity, disaster recovery, crisis management, resilience testing,
                and recovery governance.

/privacy        Privacy governance, data protection, transfer assessment, breach response, and
                data subject rights.

/supply-chain   Supplier governance, third-party risk, cloud assurance, supply-chain security,
                and trade continuity programme controls.

/dev-security   Developer and DevOps security: standards, quick reference, compliance gap register,
                and claude-rules/ subdirectory of draggable CLAUDE.md rule files for AI coding sessions.
```

Documents use lowercase filenames, single hyphen separators, and a document type prefix.

Examples:

- `governance/charter-governance-library.md`
- `governance/register-document-index-and-classification.md`
- `governance/framework-document-architecture-and-interrelationship.md`
- `governance/policy-governance-and-risk-management.md`
- `risk/standard-enterprise-risk-management.md`
- `compliance/policy-compliance-and-audit-management.md`
- `security/policy-information-security.md`
- `security/standard-logging-and-monitoring.md`
- `ai/framework-ai-governance-and-risk.md`
- `ai/standard-ai-security-and-risk.md`
- `ai/framework-ai-model-risk.md`
- `operations/standard-production-security-requirements.md`
- `resilience/framework-business-continuity-and-resilience.md`
- `resilience/procedure-backup-and-recovery.md`
- `privacy/policy-privacy-and-data-governance.md`
- `supply-chain/framework-supplier-and-cloud-governance.md`
- `dev-security/standard-developer-security-requirements.md`
- `dev-security/claude-rules/CLAUDE.md`

---

## Document Types

The library uses the following artefact types:

| Type | Purpose |
| --- | --- |
| Charter | Establishes authority, mandate, accountability, and decision rights. |
| Framework | Defines domain scope, governance model, lifecycle, and integration points. |
| Policy | States binding governance intent and mandatory principles. |
| Standard | Defines measurable control requirements and baselines. |
| Procedure | Defines repeatable operational steps for implementing a standard or policy. |
| Plan | Defines coordinated actions for continuity, crisis, incident, recovery, or migration events. |
| Guideline | Provides advisory interpretation or implementation options. |
| Register | Records authoritative metadata, ownership, risks, obligations, assets, systems, exceptions, metrics, or evidence. |
| Matrix | Maps relationships among controls, risks, obligations, frameworks, lifecycle stages, and evidence. |
| Specification | Defines technical or structural requirements for artefact creation, data fields, interfaces, or evidence. |
| Template | Provides reusable forms, logs, assessments, or evidence structures. |
| Annex | Provides supplementary domain-specific guidance that remains subordinate to the parent framework, policy, or standard. |

---

## Canonical Metadata

Every document should begin with a metadata block containing:

- Document Title
- Document Type
- Version
- Date
- Owner
- Approving Authority
- Related Documents
- Classification
- Category
- Review Frequency
- Repository Path
- Confidentiality
- Licence

Owners and approving authorities must be role-based, not person-specific. Documents must not include real company names, personal names, internal system names, customer names, vendor names, proprietary service names, IP addresses, domains, tenant identifiers, phone numbers, physical addresses, contract details, incident details, or other identifying information.

---

## Core Reference Set

The current authoritative starter set is organized around these foundational artefacts:

| Domain | Artefact |
| --- | --- |
| Governance | Governance Library Charter |
| Governance | Document Architecture and Interrelationship Framework |
| Governance | Governance and Risk Management Policy |
| Governance | Exception and Risk Acceptance Management Policy |
| Governance | Cross-Framework Alignment Matrix |
| Governance | Document Index and Classification Register |
| Governance | Key Terms and Definitions Register |
| Governance | Role Authority Register |
| Governance | Digital Trust and Assurance Metrics Register |
| Risk | Enterprise Risk Management Standard |
| Risk | Risk Register Procedure |
| Risk | Risk Acceptance Procedure |
| Compliance | Compliance, Audit, and CAPA Management Policy |
| Compliance | Global Regulatory Applicability Register |
| Security | Information Security Policy |
| Security | Identity and Access Management Policy |
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
| Supply Chain | Supplier and Cloud Governance Framework |
| Supply Chain | Trade and Supply-Chain Continuity Controls Annex |

---

## Framework Alignment Model

The library aligns to recognized framework families including ISO management system standards, NIST cybersecurity and artificial intelligence guidance, COBIT governance concepts, CCM, AICM, STAR-style assurance models, OWASP projects (Top 10, LLM Top 10, ASVS, SAMM, Cheat Sheet Series), MITRE ATLAS, MITRE ATT&CK, and jurisdiction-specific laws or regulations.

Mappings must distinguish between:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Optional assurance evidence.

Mappings must not imply certification, compliance, conformity, regulatory approval, or operating effectiveness unless the adopting organization has implemented controls, retained evidence, assigned accountable owners, completed review, and accepted residual risk.

---

## Artificial Intelligence and Data Security Position

AI governance documents in this repository treat data as the primary risk surface. The lifecycle must address collection, annotation, storage, processing, training, retrieval, inference, monitoring, retention, deletion, and decommissioning.

The AI domain explicitly considers prompt injection, data poisoning, model inversion, membership inference, training data leakage, retrieval leakage, insecure tool use, shadow AI, provenance failure, lineage gaps, retention failure, and unenforceable deletion.

The developer security domain (`/dev-security/`) addresses AI coding assistant security through draggable rule files that enforce security requirements directly in AI-assisted development sessions.

---

## Contribution Rules

Contributions must satisfy the following conditions:

1. Content must be original, CC0-compatible, and organization-neutral.
2. Content must not include real company names, personal names, internal identifiers, customer details, vendor-specific implementation data, or proprietary evidence.
3. Third-party materials may be used only for non-verbatim reference, unless their licence terms explicitly permit CC0 republication.
4. Framework references must be accurate, version-aware, and scoped to the stated purpose.
5. Regulatory content must separate obligation from interpretation and must identify where applicability depends on jurisdiction, sector, role, residency, or data category.
6. Documents must maintain role-based ownership and approving authority.
7. New documents must be added to the document index and mapped to parent artefacts where applicable.

---

## Review Cadence

The library should be reviewed at least annually and upon material change to major standards, regulatory expectations, assurance models, AI threat patterns, cloud control frameworks, privacy obligations, or operational resilience requirements.

AI, data security, privacy, and cloud assurance content should be reviewed on a 6 to 12 month cadence because control expectations and attack patterns change faster than conventional policy review cycles.

---

## Licence

This repository is dedicated to the public domain under Creative Commons CC0 1.0 Universal.

The CC0 dedication applies only to original repository content. It does not waive, transfer, or alter rights in external standards, laws, frameworks, questionnaires, guides, catalogues, or other third-party materials used as reference inputs.

---

**End of Document**
