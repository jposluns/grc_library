# GRC Library CC0 Ingestion and Transformation Specification

**Document Title:** GRC Library CC0 Ingestion and Transformation Specification
**Document Type:** Specification
**Version:** 1.2.0
**Date:** 2026 05 26
**Owner:** Governance Library Maintainer
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `README.md`, `NOTICE.md`, `core/charter-governance-library.md`, `core/register-document-index-and-classification.md`, `core/framework-document-architecture-and-interrelationship.md`
**Classification:** Public
**Category:** Core Governance
**Review Frequency:** Annual and upon material repository, licence, or source-framework change
**Repository Path:** `specification-ingestion.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This specification defines how source material is converted into organization-neutral, CC0-compatible governance documents for the public GRC Documentation Library.

It establishes rules for:

- Assessing source material for licence compatibility.
- Removing identifying and organization-specific information.
- Selecting document type and canonical filename.
- Selecting repository domain.
- Applying metadata and document structure.
- Separating legal obligation, regulatory interpretation, industry practice, contractual requirement, and architectural recommendation.
- Avoiding verbatim reproduction of restrictively licensed source material.
- Updating indexes, registers, matrices, and related artefacts.

---

## Scope

This specification applies to all content added to, modified in, or synthesized for this repository.

It applies to source material from internal documents, public standards, control frameworks, legal or regulatory references, audit guidance, questionnaires, implementation guides, metrics catalogues, and user-provided drafts.

---

## Licence Compatibility Rules

All original repository content is released under CC0 1.0 Universal.

Before source material is used, determine whether it is compatible with CC0 republication. Where licence terms are restrictive, uncertain, proprietary, all-rights-reserved, noncommercial, no-derivatives, no-redistribution, or otherwise incompatible with CC0, the source may be used only for non-verbatim reference.

Do not copy into this repository:

- Third-party control statements.
- Questionnaire text or answer options.
- Implementation guidance.
- Audit guidance.
- Metrics catalogue text.
- Tables reconstructed from restrictively licensed sources.
- Proprietary examples.
- Organization-specific evidence.

Permitted use includes independent synthesis, framework name references, high-level domain alignment, original commentary, evidence category mapping, and non-verbatim applicability analysis.

---

## Identification and Sanitization Rules

Repository content must not include:

- Real company names.
- Real people names.
- Email addresses.
- Phone numbers.
- Physical addresses.
- Tenant IDs.
- Domain names.
- IP addresses.
- Customer names.
- Supplier names.
- Contract references.
- Internal system names.
- Incident-specific details.
- Audit evidence.
- Screenshots or exports from internal systems.

Replace organization-specific details with generic roles, generic system categories, generic data classes, generic supplier classes, and generic evidence classes.

---

## Repository Domains

Documents must be placed in the domain that best reflects their primary governance purpose.

```text
/core        Cross-domain governance, risk, compliance, audit, mappings, registers, role authority, document architecture, and metrics.
/security    Information security, identity, access, logging, incident response, data classification, secure engineering, and secure operations.
/ai          AI governance, AI security, model risk, AI lifecycle, AI documentation, AI assurance, AI testing, and AI data security.
/privacy     Privacy governance, data protection, transfer assessment, breach response, records retention, and data subject rights.
/resilience  Business continuity, disaster recovery, crisis management, resilience testing, emergency response, and recovery governance.
/supplier    Supplier, third-party, cloud, external dependency, supply-chain, and service-provider governance.
```

---

## Filename Rules

Filenames must:

1. Use lowercase letters.
2. Use single hyphens between words.
3. Remove punctuation.
4. Replace ampersands with `and`.
5. Start with the document type prefix.
6. Avoid duplicate, trailing, or leading hyphens.
7. Avoid organization-specific product, vendor, system, or service names.

Examples:

- `policy-information-security.md`
- `standard-logging-and-monitoring.md`
- `procedure-risk-register.md`
- `framework-ai-governance-and-risk.md`
- `template-ai-system-register.md`
- `matrix-cross-framework-alignment.md`

---

## Document Types

Allowed document types are:

- Charter
- Framework
- Policy
- Standard
- Procedure
- Plan
- Guideline
- Register
- Matrix
- Specification
- Template
- Annex

Do not use `SOP` as the document type. Convert it to Procedure, Standard, or Plan based on content.

---

## Canonical Metadata

Every document must start with this metadata pattern:

```markdown
# Document Title

**Document Title:** Document Title
**Document Type:** Policy
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Role Name
**Approving Authority:** Role Name
**Related Documents:** `path/file.md`, `path/file.md`
**Classification:** Public
**Category:** Domain Name
**Review Frequency:** Annual and upon material change
**Repository Path:** `domain/file-name.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal
```

Metadata must use role names only and must not use named individuals.

---

## Required Structural Pattern

After metadata, documents should use this structure unless the document type requires a different structure:

1. Purpose.
2. Scope or Applicability.
3. Requirements, Policy Statements, Procedure, or Framework Components.
4. Evidence Requirements.
5. Limitations.
6. Maintenance or Review Requirements.
7. End of Document marker.

Documents must use `---` to separate major sections and must end with:

```markdown
**End of Document**
```

---

## Language Requirements

Documents must use precise, organization-neutral language. They must avoid vendor-marketing language, unsupported maturity claims, and statements implying compliance, certification, regulatory approval, or operating effectiveness without implementation evidence.

Use Oxford English with `-ize` forms where applicable.

Do not state that a document ensures compliance. State that it provides a baseline, structure, evidence class, or control model that adopting organizations must validate.

---

## Regulatory and Framework Mapping Rules

Mappings must classify each statement as one of:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Evidence category.

Mappings must include applicability conditions where jurisdiction, sector, processing role, deployment model, data residency, data category, or contractual obligation materially affects interpretation.

---

## AI Content Rules

AI documents must treat data as the primary risk surface and must address relevant lifecycle stages:

- Collection.
- Annotation.
- Storage.
- Processing.
- Training.
- Retrieval.
- Inference.
- Monitoring.
- Retention.
- Deletion.
- Decommissioning.

AI documents must explicitly consider prompt injection, indirect prompt injection, data poisoning, model inversion, membership inference, training data leakage, retrieval leakage, unsafe tool use, shadow AI, provenance, lineage, retention, and enforceable deletion where relevant.

---

## Quality Gate

Before committing a document, validate that:

1. Metadata is complete and follows the canonical pattern.
2. Repository path matches actual file path.
3. Licence is CC0 1.0 Universal.
4. No prohibited identifiers are present.
5. No restrictively licensed third-party text is copied.
6. Roles are generic and role-based.
7. Classification is Public.
8. Framework and regulatory statements are scoped and not overstated.
9. Related documents are updated where required.
10. Index register is updated for new active documents.

---

**End of Document**
