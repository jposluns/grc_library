# GRC Library CC0 Ingestion and Transformation Specification

**Document Title:** GRC Library CC0 Ingestion and Transformation Specification  
**Document Type:** Specification  
**Version:** 1.3.0  
**Date:** 2026-05-27  
**Owner:** Governance Library Maintainer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`governance/charter-governance-library.md`](governance/charter-governance-library.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md)  
**Classification:** Public  
**Category:** Core Governance  
**Review Frequency:** Annual and upon material repository, licence, or source-framework change  
**Repository Path:** [`specification-ingestion.md`](specification-ingestion.md)  
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
- Updating indexes, registers, domain READMEs, and related artefacts.

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

Replace organization-specific details with generic roles, generic system categories, generic data classes, generic supplier classes, and generic evidence classes. Apply the substitution table in Appendix A to all source content before producing output.

---

## Repository Domains

Documents must be placed in the domain that best reflects their primary governance purpose.

```text
governance/    Core governance, charter, frameworks, policies, registers, matrices, role authority,
               document architecture, cross-framework alignment, and assurance metrics.

security/      Information security policies, standards, procedures, access control, identity,
               cryptography, logging, data classification, and secure operations.

ai/            AI governance, AI security, model risk, AI lifecycle, AI documentation, AI assurance,
               AI testing, and AI data security.

privacy/       Privacy governance, data protection, cross-border transfer, breach response,
               records retention, and data subject rights.

resilience/    Business continuity, disaster recovery, crisis management, incident response,
               resilience testing, emergency response, and recovery governance.

supply-chain/  Supplier governance, third-party risk, cloud governance, supply-chain security,
               trade compliance programmes, and service-provider assurance.

compliance/    Compliance management, legal and regulatory obligations, audit governance,
               sector-specific requirements, and trade compliance controls registers.

risk/          Enterprise risk management, risk registers, key risk indicators, risk appetite,
               quantitative analysis, AI risk methodology, and third-party risk standards.

dev-security/  Secure development standards, DevOps security, software composition analysis,
               developer quick references, and AI coding agent rule files.

operations/    IT operations, asset management, change management, configuration management,
               and security operations registers.
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
- Checklist

Do not use `SOP` as the document type. Convert it to Procedure, Standard, or Plan based on content.

---

## Canonical Metadata

Every document must start with this metadata pattern:

```markdown
# Document Title

**Document Title:** Document Title
**Document Type:** Policy
**Version:** 0.0.1
**Date:** YYYY-MM-DD
**Owner:** Role Name
**Approving Authority:** Role Name
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`domain/other.md`](../other-domain/other.md)
**Classification:** Public
**Category:** Domain Name
**Review Frequency:** Annual and upon material change
**Repository Path:** [`domain/file-name.md`](file-name.md)
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal
```

Related Documents and Repository Path use markdown links. The display text is the root-relative path. The link target is relative to the current file's directory: same-directory files use the bare filename; cross-directory files use `../` traversal.

Metadata must use role names only and must not use named individuals.

Dates must use ISO 8601 format: `YYYY-MM-DD`.

---

## Version Numbering

- All new documents begin at version `0.0.1`.
- Increment the patch segment (`0.0.x`) for minor corrections to content within an existing version.
- Increment the minor segment (`0.x.0`) for substantive content additions or structural changes.
- Advance to `1.0.0` upon first formal approval and publication as a stable active document.
- Increment the major segment (`x.0.0`) for breaking structural changes or significant policy revision.

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

1. Metadata is complete and follows the canonical pattern including the `Licence` field.
2. Repository path matches actual file path.
3. Licence is CC0 1.0 Universal.
4. No prohibited identifiers are present; Appendix A substitutions have been applied.
5. No restrictively licensed third-party text is copied.
6. Roles are generic and role-based.
7. Classification is Public.
8. Framework and regulatory statements are scoped and not overstated.
9. Related Documents field references existing files using canonical paths.
10. The domain-level [`README.md`](README.md) Active Documents table is updated for all new documents.
11. The document index register ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) is updated for all new active documents.

---

## Appendix A — Sanitization Substitution Table

Apply all substitutions below before producing any output. Substitution is case-insensitive. Apply the longer or more specific form first where multiple entries could match.

### Organization-Specific Terms

| Source Term | Replacement |
|---|---|
| Traffic Tech | the organisation |
| Mississauga data centre | primary data centre |
| MissDC | primary data centre |
| Greenfield | infrastructure programme |

### Microsoft Product and Service Names

| Source Term | Replacement |
|---|---|
| Microsoft Entra ID | enterprise identity provider |
| Entra ID | enterprise identity provider |
| Entra PIM | Privileged Identity Management (PIM) |
| Microsoft Entra Password Protection | enterprise password protection service |
| Azure Key Vault | secrets management service |
| Microsoft Sentinel | SIEM |
| Azure Monitor | cloud monitoring service |
| Azure Site Recovery | cloud-based site recovery service |
| Azure Logic Apps | integration platform |
| Azure (used as cloud platform name) | cloud platform |
| Microsoft Intune | endpoint management platform |
| Intune | endpoint management platform |
| Microsoft 365 | cloud productivity platform |
| M365 | cloud productivity platform |
| Microsoft Purview DLP | enterprise DLP platform |
| Purview DLP | enterprise DLP platform |
| Defender for Cloud Apps | cloud access security broker (CASB) |
| Microsoft Defender for Cloud | cloud security posture management (CSPM) |
| Microsoft Defender for Endpoint | endpoint detection and response (EDR) platform |
| Microsoft Secure Score | cloud security posture score |
| Microsoft Teams | collaboration platform |
| SharePoint | collaboration and file storage platform |
| OneDrive | collaboration and file storage platform |
| Exchange Online | email platform |
| Microsoft Cloud PKI | cloud-based PKI service |
| BitLocker | full-disk encryption |

### Third-Party Product and Vendor Names

| Source Term | Replacement |
|---|---|
| Workday | HR management system |
| OneTrust | supplier evaluation platform |
| FlexEra | IT asset management system |
| Halo (ITSM) | ITSM portal |
| Binary Defense | external IR partner |
| BizTalk | integration middleware platform |
| ESXi | hypervisor infrastructure |
| metacompliance.com | security awareness training platform |

### Incident and Case References

| Source Term | Replacement |
|---|---|
| Any named specific security incident | a prior security incident |
| CS109236765 or any case reference number | omit |
| TT-REG-001 | omit — highly confidential; do not publish |
| TT-REG-002 | omit — highly confidential; do not publish |

### Personal Names

| Source Term | Replacement |
|---|---|
| Any real person's name | omit or replace with role title |

### Terms to Preserve Without Substitution

The following are public standards, frameworks, regulatory citations, and programme names that must not be substituted: ISO, NIST, COBIT, CSA CCM, BASC, WCO, ISO 28000, GDPR, PIPEDA, AIDA, CPPA, PIPL, LGPD, Quebec Law 25, UK GDPR, EU AI Act, FIDO2, MITRE ATT&CK, OWASP, PTES, OSCP, CREST, CVSS, CTPAT, PIP, AEO, AEO-S, HMRC, NEEC, OEA, DORA, NIS 2, PCI DSS, HIPAA, HITECH, SOX, FedRAMP, SLSA, FAIR, VEX, SBOM, HL7, FHIR, IEC 62443, IMO, ICAO, TSA, and all other recognized public regulatory, standards, or programme acronyms.

---

**End of Document**
