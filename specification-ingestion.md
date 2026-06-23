# GRC Library Ingestion and Transformation Specification

**Document Title:** GRC Library Ingestion and Transformation Specification\
**Document Type:** Specification\
**Version:** 1.7.3\
**Date:** 2026-06-23\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`governance/charter-governance-library.md`](governance/charter-governance-library.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material repository, licence, or source-framework change\
**Repository Path:** [`specification-ingestion.md`](specification-ingestion.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This specification defines how source material is converted into organisation-neutral, library-canonical governance documents for the public GRC Documentation Library. The library is released under CC BY-SA 4.0; ingestion enforces original-authorship and library-canonical structure.

It establishes rules for:

- Assessing source material for licence compatibility.
- Removing identifying and organisation-specific information.
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

## Licence compatibility rules

All original repository content is released under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

The library's principle is that it does not copy externally licensed verbatim content. Source material is used for non-verbatim reference (framework identifiers, control families, domain-level alignment, applicability structure, original commentary in the library's own words). This principle applies regardless of the source material's licence terms: even when source material is permissively licensed (CC0, MIT, CC BY 4.0, etc.) the library prefers original synthesis to direct incorporation.

Where a contributor proposes to incorporate any verbatim or near-verbatim third-party content, the contributor must confirm that the source licence is compatible with CC BY-SA 4.0 and that the contribution preserves the source's attribution and licence notices. Inbound licences known to be compatible with CC BY-SA 4.0 include: CC0 1.0 Universal (most permissive), CC BY 4.0 (with attribution), public-domain works (e.g., US government works such as NIST publications), and MIT or Apache 2.0 source code commentary used as cited examples. Inbound licences known to be incompatible (and not permitted as verbatim content): CC BY-NC, CC BY-ND, CC BY-NC-ND, GPL family (one-way the other direction), and proprietary or all-rights-reserved content.

Do not copy into this repository:

- Third-party control statements.
- Questionnaire text or answer options.
- Implementation guidance.
- Audit guidance.
- Metrics catalogue text.
- Tables reconstructed from restrictively licensed sources.
- Proprietary examples.
- Organisation-specific evidence.

Permitted use includes independent synthesis, framework name references, high-level domain alignment, original commentary, evidence category mapping, and non-verbatim applicability analysis.

---

## Identification and sanitization rules

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

Replace organisation-specific details with generic roles, generic system categories, generic data classes, generic supplier classes, and generic evidence classes. Apply the substitution table in Appendix A to all source content before producing output.

---

## Repository domains

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

The following directories and files exist in the repository but are not used for governance artefacts and are not in scope of this ingestion specification:

```text
CONTRIBUTING.md       Contribution workflow and rules.
CHANGELOG.md          Phase-level history.
SECURITY.md           Defect reporting path.
.pre-commit-config.yaml  Local pre-commit hooks.
.github/              GitHub Actions workflow.
tools/                Audit scripts and taxonomy / portal generators.
docs/                 Adopter documentation (not subject to canonical metadata).
taxonomy.yml          Auto-generated machine-readable registry of artefact metadata.
```

The structural auditor exempts these paths from the requirement that every markdown file appear in a domain README and in the document index register.

---

## Filename rules

Filenames must:

1. Use lowercase letters.
2. Use single hyphens between words.
3. Remove punctuation.
4. Replace ampersands with `and`.
5. Start with the document type prefix.
6. Avoid duplicate, trailing, or leading hyphens.
7. Avoid organisation-specific product, vendor, system, or service names.

Examples:

- [`policy-information-security.md`](security/policy-information-security.md)
- [`standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md)
- [`procedure-risk-register.md`](risk/procedure-risk-register.md)
- [`framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md)
- [`template-ai-system-register.md`](ai/template-ai-system-register.md)
- [`matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)

---

## Document types

Allowed document types are:

- Charter
- Framework
- Policy
- Standard
- Procedure
- SOP
- Plan
- Roadmap
- Guideline
- Guide
- Register
- Matrix
- Specification
- Template
- Annex
- Checklist
- Worklist

### Type selection guidance

- Procedure versus SOP: a Procedure is a multi-actor or cross-functional workflow that coordinates several roles. An SOP is a single-actor or narrow team sequence with explicit step ownership for one repeatable task.
- Plan versus Roadmap: a Plan is event-triggered or schedule-bound coordination such as incident, recovery, migration, or communication. A Roadmap is a multi-phase forward strategy tied to a strategic outcome with phased milestones and dependencies.
- Guideline versus Guide: a Guideline is advisory interpretation of a policy or standard requirement and reads as governance commentary. A Guide is technical reference material organized for adoption such as patterns, examples, configuration models, or implementation walkthroughs.
- Template versus Worklist: a Template is a reusable blank skeleton meant to be copied into instances. A Worklist is a per-instance working artefact derived from a template, scoped to one batch or task, and typically retired or archived when the work is closed (the authoritative record migrates to a register or log).

The canonical filename prefix must match the Document Type field. Filenames use lowercase: `sop-`, `roadmap-`, and `guide-` are valid prefixes for the corresponding types.

---

## Canonical metadata

Every document must start with this metadata pattern. Every line of the metadata block except the last ends with a backslash character (`\`), which is CommonMark §6.7 syntax for a hard line break. This ensures GitHub and other CommonMark renderers display each metadata field on its own line:

```markdown
# Document Title

**Document Title:** Document Title\
**Document Type:** Policy\
**Version:** 1.0.0\
**Date:** YYYY-MM-DD\
**Owner:** Role Name\
**Approving Authority:** Role Name\
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`domain/other.md`](../other-domain/other.md)\
**Classification:** Public\
**Category:** Domain Name\
**Review Frequency:** Annual and upon material change\
**Repository Path:** [`domain/file-name.md`](file-name.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0
```

Notes on the backslash-newline convention:

- Every metadata line except the last must end with `\` immediately before the line terminator.
- The last line (typically `License`) does not require the marker because the following blank line and `---` separator already create a paragraph break.
- Do not use two trailing spaces; that variant is also valid CommonMark but is invisible in source and is fragile against editor whitespace-stripping. The backslash is visible and editor-safe.
- The [`lint-metadata.py`](tools/lint-metadata.py) audit enforces this convention.

Related Documents and Repository Path use markdown links. The display text is the root-relative path. The link target is relative to the current file's directory: same-directory files use the bare filename; cross-directory files use `../` traversal.

Metadata must use role names only and must not use named individuals.

Dates must use ISO 8601 format: `YYYY-MM-DD`.

---

## Version numbering

- All new documents begin at version `0.0.1`.
- Increment the patch segment (`0.0.x`) for minor corrections to content within an existing version.
- Increment the minor segment (`0.x.0`) for substantive content additions or structural changes.
- Advance to `1.0.0` upon first formal approval and publication as a stable active document.
- Increment the major segment (`x.0.0`) for breaking structural changes or significant policy revision.

---

## Required structural pattern

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

## Language requirements

Documents must use precise, organisation-neutral language. They must avoid vendor-marketing language, unsupported maturity claims, and statements implying compliance, certification, regulatory approval, or operating effectiveness without implementation evidence.

Use Oxford English with `-ize` forms where applicable. Do not use em dashes or en dashes. Pair `ensure` with `that`; do not use bare `ensure` or `ensures`.

Use sentence case for all section headings (H2 through H6). The first word of the heading text is capitalised and subsequent words are lowercase except proper nouns and acronyms. Section identifiers such as `A1.`, `Step 1:`, and `Category 1:` count as numbering rather than as the first word, so the word that follows must be capitalised. H1 document titles may use Title Case where they name a controlled artefact such as a policy, standard, or charter title.

Do not state that a document ensures that compliance. State that it provides a baseline, structure, evidence class, or control model that adopting organisations must validate.

---

## Regulatory and framework mapping rules

Mappings must classify each statement as one of:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Evidence category.

Mappings must include applicability conditions where jurisdiction, sector, processing role, deployment model, data residency, data category, or contractual obligation materially affects interpretation.

---

## AI content rules

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

## Quality gate

Before committing a document, validate that:

1. Metadata is complete and follows the canonical pattern including the `License` field.
2. Repository path matches actual file path.
3. License is CC BY-SA 4.0.
4. No prohibited identifiers are present; Appendix A substitutions have been applied.
5. No restrictively licensed third-party text is copied.
6. Roles are generic and role-based.
7. Classification is Public.
8. Framework and regulatory statements are scoped and not overstated.
9. Related Documents field references existing files using canonical paths.
10. The domain-level [`README.md`](README.md) Active Documents table is updated for all new documents.
11. The document index register ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) is updated for all new active documents.
12. The listing surfaces for each new document have been reviewed via [`tools/suggest-listing-surfaces.py`](tools/suggest-listing-surfaces.py) `<doc-path>`, which enumerates the MECHANICAL surfaces (items 10 and 11 above, plus the auto-generated taxonomy and portal, hard-gated by the listing-surface-completeness, taxonomy-sync, and portal-sync audits) and the SEMANTIC surfaces (the framework matrices and crosswalks, the glossary, and the document's own Related Documents field, which a human ratifies because their inclusion is relevance-based).

---

## Appendix a: sanitization substitution table

Apply all substitutions below before producing any output. Substitution is case-insensitive. Apply the longer or more specific form first where multiple entries could match.

### Organisation-specific terms

| Source Term | Replacement |
|---|---|
| Traffic Tech | the organisation |
| Mississauga data centre | primary data centre |
| MissDC | primary data centre |
| Greenfield | infrastructure programme |

### Microsoft product and service names

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

### Third-party product and vendor names

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

### Incident and case references

| Source Term | Replacement |
|---|---|
| Any named specific security incident | a prior security incident |
| CS109236765 or any case reference number | omit |
| TT-REG-001 | omit: highly confidential; do not publish |
| TT-REG-002 | omit: highly confidential; do not publish |

### Personal names

| Source Term | Replacement |
|---|---|
| Any real person's name | omit or replace with role title |

### Terms to preserve without substitution

The following are public standards, frameworks, regulatory citations, and programme names that must not be substituted: ISO, NIST, COBIT, CSA CCM, BASC, WCO, ISO 28000, GDPR, PIPEDA, AIDA, CPPA, PIPL, LGPD, Quebec Law 25, UK GDPR, EU AI Act, FIDO2, MITRE ATT&CK, OWASP, PTES, OSCP, CREST, CVSS, CTPAT, PIP, AEO, AEO-S, HMRC, NEEC, OEA, DORA, NIS 2, PCI DSS, HIPAA, HITECH, SOX, FedRAMP, SLSA, FAIR, VEX, SBOM, HL7, FHIR, IEC 62443, IMO, ICAO, TSA, and all other recognized public regulatory, standards, or programme acronyms.

### Named open-source projects

Open-source projects whose canonical name includes a vendor parent (for example PyRIT, originating from a vendor) may be referenced by the project name alone, without the vendor parent, qualified by an explanatory phrase such as "open-source AI red team automation framework". Do not retain the vendor name in body text. Vendor-only proprietary products remain subject to the sanitization substitution table above.

---

**End of Document**
