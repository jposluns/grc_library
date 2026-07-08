# Governance Library Charter

**Document Title:** Governance Library Charter\
**Document Type:** Charter\
**Version:** 1.2.5\
**Date:** 2026-07-08\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`NOTICE.md`](../NOTICE.md), [`governance/framework-human-capital-and-ethical-conduct.md`](framework-human-capital-and-ethical-conduct.md), [`governance/policy-digital-twin-and-simulation-governance.md`](policy-digital-twin-and-simulation-governance.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material framework, regulatory, or licence change\
**Repository Path:** [`governance/charter-governance-library.md`](charter-governance-library.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This charter establishes the authority model, document hierarchy, lifecycle, quality expectations, and licence boundary for the Governance, Risk, and Compliance Documentation Library.

The library provides organization-neutral governance artefacts that can be adopted or adapted by any organization. It is not a record of one organization's internal governance programme and must not contain organization-specific names, evidence, systems, incidents, vendors, customers, or personal identifiers.

The library also serves as a reference implementation for AI-assisted maintenance of a governed corpus. The audit toolchain under [`tools/`](../tools/) and the operational pack under [`dev-security/claude-rules/`](../dev-security/claude-rules/) show how a CC BY-SA 4.0 GRC corpus can be maintained with Claude Code participating in PRs without losing internal consistency, metadata integrity, or audit-trail discipline. The pack is also documented as a standalone Claude Code baseline usable on any project, with or without a GRC corpus, distilled from the disciplines this library required to maintain itself. This charter governs the corpus; the operational layer is an artefact of the corpus's own maintenance, not an additional authority claim.

---

## Scope

This charter applies to all repository content, including charters, frameworks, policies, standards, procedures, plans, guidelines, registers, matrices, specifications, templates, examples, metadata, and supporting documentation.

It governs:

- Document creation, review, approval, versioning, maintenance, and retirement.
- Domain placement and canonical naming.
- Role-based ownership and approval.
- Use of third-party standards and framework references.
- Exclusion of personal, proprietary, and organization-specific information.
- Cross-framework and regulatory mapping conventions.
- Review cadence and quality control.

---

## Governance principles

1. **Organization neutrality:** Documents must be reusable without editing out company-specific or person-specific content.
2. **Role-based accountability:** Owners and approving authorities must be generic roles, not named individuals.
3. **Licence compatibility:** Original repository content is CC BY-SA 4.0. Restricted third-party material must not be copied into the repository.
4. **Traceability:** Documents should identify parent artefacts, related artefacts, applicable domains, and evidence classes.
5. **Applicability discipline:** Documents must distinguish legal obligation, regulatory interpretation, industry practice, architectural recommendation, and optional assurance evidence.
6. **Data lifecycle focus:** AI, privacy, supplier, and resilience artefacts must address data collection, storage, processing, use, retention, deletion, and evidence handling.
7. **Reviewability:** Each document must carry metadata sufficient for version control, review, and maintenance.

---

## Document hierarchy

| Level | Artefact Type | Purpose |
| --- | --- | --- |
| 1 | Charter | Defines repository authority, scope, principles, and governance lifecycle. |
| 2 | Principle | States the foundational, cross-cutting production principles (such as integrity and trustworthiness) that the frameworks, policies, and standards operationalize. |
| 3 | Framework | Defines domain structure, scope, lifecycle, and integration points. |
| 4 | Policy | States mandatory governance intent and principles. |
| 5 | Standard | Defines measurable control requirements and baselines. |
| 6 | Procedure | Defines repeatable multi-actor or cross-functional operational steps. |
| 7 | SOP | Defines a single-actor or narrow team sequence with explicit step ownership for one repeatable task. |
| 8 | Plan | Defines coordinated incident, continuity, recovery, migration, or response actions. |
| 9 | Roadmap | Defines a multi-phase forward strategy tied to a strategic outcome with phased milestones and dependencies. |
| 10 | Guideline | Provides advisory implementation interpretation of a policy or standard requirement. |
| 11 | Guide | Provides technical reference material organized for adoption such as patterns, examples, configuration models, or implementation walkthroughs. |
| 12 | Register | Records authoritative metadata, obligations, risks, assets, systems, exceptions, or evidence. |
| 13 | Matrix | Maps relationships among controls, risks, obligations, frameworks, lifecycle stages, and evidence. |
| 14 | Specification | Defines technical or structural requirements for artefact creation, data fields, interfaces, or evidence. |
| 15 | Template | Provides reusable forms, logs, assessments, or evidence structures. |
| 16 | Annex | Provides supplementary domain-specific guidance that remains subordinate to the parent framework, policy, or standard. |
| 17 | Checklist | Provides a structured verification list for a specific process or gate. |
| 18 | Worklist | Captures a per-instance working artefact derived from a Template, scoped to one batch or task, and typically retired when the work closes (the authoritative record migrates to a register or log). |

---

## Document lifecycle

Each document follows this lifecycle:

1. **Draft:** Initial content creation, metadata assignment, and domain placement.
2. **Review:** Validation for structure, originality, licence compatibility, organization neutrality, and framework accuracy.
3. **Approved:** Maintainer acceptance for publication under CC BY-SA 4.0.
4. **Maintained:** Periodic review, correction, and version updates.
5. **Superseded:** Retained for history but no longer recommended; marked with the dedicated `Status: Superseded` metadata marker.
6. **Retired:** Removed from the active document index while preserved in repository history.

---

## Change management

Material changes require version increment and document-control update. Material changes include:

- New or altered control requirements.
- New legal, regulatory, framework, or assurance alignment.
- New document dependencies.
- Substantive changes to scope, applicability, authority, or evidence requirements.
- Changes to licence, confidentiality, or permitted use.

Non-substantive changes may be made without a version increment where they are limited to formatting, spelling, broken links, metadata correction, or non-material wording improvement.

---

## Approval model

Repository content is approved by role, not by named person. Suitable approving authorities include:

- Governance Library Maintainer.
- Domain Maintainer.
- Control Framework Maintainer.
- Licence Reviewer.
- Technical Reviewer.

No document may require approval by a real individual name in the public CC BY-SA 4.0 repository.

---

## Exclusion requirements

Repository content must not include:

- Real company names.
- Real personal names.
- Email addresses.
- Phone numbers.
- Physical addresses.
- Tenant IDs or customer IDs.
- Domain names or IP addresses.
- Internal system names.
- Customer, supplier, or contract names.
- Internal audit evidence.
- Incident-specific details.
- Proprietary implementation details.

---

## Framework and regulatory mapping

Mappings may identify external frameworks, standards, or laws at a high level. They must not reproduce restricted source text and must not imply certification, conformity, audit conclusion, or regulatory approval.

Mappings must state whether they represent:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Evidence category.

---

## Review cycle

Core governance documents should be reviewed annually. AI, privacy, cloud assurance, supplier risk, and resilience artefacts should be reviewed on a 6 to 12 month cadence where external expectations, threat patterns, or source framework versions change materially.

---

**End of Document**
