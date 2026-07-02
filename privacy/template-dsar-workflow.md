# Data Subject Access Request Workflow Template

**Document Title:** Data Subject Access Request Workflow Template\
**Document Type:** Template\
**Version:** 1.1.3\
**Date:** 2026-07-02\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, jurisdictional, or system-of-record change\
**Repository Path:** [`privacy/template-dsar-workflow.md`](template-dsar-workflow.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template defines an operational workflow for handling Data Subject Access Requests (DSARs) and equivalent rights requests under GDPR, UK GDPR, LGPD, PIPEDA, PIPL, CCPA, and similar regimes. It complements the Data Subject Rights Management Procedure by providing the request-record structure, the stage gates, an operational rendering of the identity verification ladder the procedure's Section 4.2 defines and governs, and the response artefact format that the procedure relies on. Adopting organizations populate the placeholders, configure their own systems of record, and integrate the workflow with their case-management tooling.

---

## Scope

This template covers all data subject rights requests, including but not limited to: access, rectification, erasure, restriction, portability, objection, withdrawal of consent, automated-decision-making review, complaint, and access to safeguards. It applies whether the request arrives via web form, email, postal mail, social channel, regulator, legal representative, or in-product channel.

---

## Request lifecycle

The workflow has seven stages. Each stage has defined inputs, outputs, owners, and SLAs.

### Stage 1: Intake

| Item | Value |
| --- | --- |
| Trigger | Any inbound communication that purports to exercise a data subject right |
| Owner | Privacy team intake desk |
| Inputs | Request body, sender contact, evidence attached, channel |
| Outputs | Request record created with a unique identifier; receipt acknowledgement sent within one business day |
| SLA | Acknowledge within 1 business day. Restriction-of-processing requests additionally carry the governing procedure's 72-hour calendar ceiling on the receipt acknowledgement, which binds over weekends and holidays |
| Quality gates | Channel logged; locale set; jurisdiction inferred; right-category classified |

### Stage 2: Identity verification

| Item | Value |
| --- | --- |
| Owner | Privacy team |
| Inputs | Submitter contact, claim of identity, available authentication signals |
| Outputs | Verification record at one of the three verification levels (Standard, Enhanced, Re-verification) defined by [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md) Section 4.2, which governs; the table below operationalizes that ladder |
| SLA | Initial verification attempt within 3 business days of intake; a request whose identity cannot be verified within 10 business days is suspended per the governing procedure |
| Quality gates | Verification record stored with the request; collection of any additional identifier limited to the minimum required to confirm identity |

| Verification level | When applied | Verification method |
| --- | --- | --- |
| Standard | General access, correction, or deletion requests for low-sensitivity data categories | Government-issued photo ID; confirmation of account details or employment record; or two independently verifiable data points matching held records. An authenticated session on the system of record, or a verification token confirmed via a registered channel the controller controls, may serve as ONE of the two data points, paired with a second independently verifiable data point |
| Enhanced | Requests involving health, financial, or biometric data; requests with indications of identity fraud; requests from authorized third parties acting on behalf of the data subject; high-impact actions asserted through an unauthenticated channel (erasure, portability of a comprehensive data set, ADM review) | Government-issued photo ID plus secondary verification; notarized authorization for third-party requestors acting on behalf of the data subject. For the unauthenticated high-impact cases, the evidence is additionally reviewed by a second Privacy team member |
| Re-verification | Requests for the same data type made within 12 months of a prior request | Standard verification unless circumstances indicate heightened risk |

If identity cannot be verified within 10 business days, the request is suspended (not closed): the data subject is notified of the outstanding verification requirement and given a reasonable further period to provide acceptable evidence, per the governing procedure.

### Stage 3: Scope definition

| Item | Value |
| --- | --- |
| Owner | Privacy team with the requestor |
| Inputs | Subject's stated scope; defaults from the right category |
| Outputs | A scoped request: time range, data categories, systems involved, recipients of interest |
| SLA | Scope confirmed within 3 business days of identity verification |
| Quality gates | Scope is no broader than the subject's request; clarifying questions are limited to the minimum required |

### Stage 4: Search and assembly

| Item | Value |
| --- | --- |
| Owner | Each system-of-record steward; Privacy team coordinates |
| Inputs | Scoped request; mapping of personal data to systems from the ROPA |
| Outputs | Per-system extracts; aggregated assembly record; provenance per item |
| SLA | Per the right's regulatory window: one month from intake under the GDPR (Art. 12(3)), extendable by two further months for complex or numerous requests with documented reason and subject notification within the first month; 45 days under the CCPA / CPRA, extendable once by an additional 45 days with notice within the first 45-day period; 30 days under PIPEDA |
| Quality gates | Each system queried with the subject identifier; null returns recorded explicitly; backups and cold storage included if reasonable; embeddings, vector stores, AI training data, and derived datasets considered |

### Stage 5: Redaction and exception handling

| Item | Value |
| --- | --- |
| Owner | Privacy team with Legal Counsel |
| Inputs | Assembled data set, exception rules per jurisdiction |
| Outputs | Redacted output set with rationale for each redaction; exemption decisions logged |
| SLA | Within stage 4 SLA |
| Quality gates | Personal data of third parties is redacted unless disclosure is lawful; legally privileged or trade-secret content is excepted with rationale; exception rationale is reviewable on request by the supervisory authority |

### Stage 6: Response delivery

| Item | Value |
| --- | --- |
| Owner | Privacy team |
| Inputs | Redacted output set, response template per right and per jurisdiction |
| Outputs | Response delivered through a secure channel; subject confirmation requested |
| SLA | Within the regulatory window |
| Quality gates | Channel security appropriate to the data classification; delivery evidence retained; subject confirmation logged when received |

### Stage 7: Closure and audit trail

| Item | Value |
| --- | --- |
| Owner | Privacy team |
| Inputs | Delivered response, any follow-up correspondence |
| Outputs | Closure record; metrics updated |
| SLA | Within 5 business days of last subject contact, or at the regulatory deadline if no further contact occurs |
| Quality gates | Audit trail is complete: intake, verification, scope, search, redactions, delivery, closure |

---

## Request record minimum fields

| Field | Description |
| --- | --- |
| Request ID | Unique identifier |
| Right category | Access, rectification, erasure, restriction, portability, objection, consent withdrawal, ADM review, complaint, safeguards access, other |
| Jurisdiction | Applicable regime per the subject's residency and processing context |
| Channel | Web form, email, postal, social, regulator, legal representative, in-product |
| Intake timestamp (UTC) | |
| Acknowledgement timestamp (UTC) | |
| Identity verification level | Standard, Enhanced, Re-verification (per the governing procedure Section 4.2) |
| Identity verification mechanism | Photo ID; account or employment confirmation; paired data points (an auth session or registered-channel token counts as one of the two); photo ID plus secondary verification; notarized third-party authorization |
| Scope | Time range, data categories, systems, recipients of interest |
| Systems searched | List of systems queried; per-system result (data found, null, refused with rationale) |
| Redactions applied | Count and rationale categories |
| Exception decisions | Right-specific exceptions invoked, with rationale |
| Delivery channel | Secure download, secure email, postal, in-product, regulator |
| Delivery timestamp (UTC) | |
| Confirmation of receipt | Where requested or required |
| Closure timestamp (UTC) | |
| Time to acknowledgement | Hours |
| Time to delivery | Calendar days |
| Extension invoked | Yes or no; rationale; subject notification date |
| Appeal initiated | Yes or no; outcome reference |
| Supervisory authority complaint reference | If a complaint follows |

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Acknowledgement adherence | Percentage of requests acknowledged within 1 business day | At least 99% |
| Delivery within regulatory window | Percentage of requests with response delivered before the applicable deadline | 100% |
| Extension rate | Percentage of requests requiring extension | Trend-monitored |
| Appeals filed | Count of appeals initiated by subjects | Trend-monitored |
| Supervisory authority complaints | Count of complaints lodged with regulators that reference the organization | Trend-monitored |
| First-pass identity verification rate | Percentage of requests where identity is verified at the appropriate verification level on the first attempt | At least 90% |

---

## Operating expectations

1. The DSAR record is the single authoritative trail for each request. No off-record handling.
2. Privacy team rotates the on-call intake role to maintain a 1-business-day acknowledgement SLA across timezones.
3. Each system of record listed in the ROPA has a designated steward with a documented response time commitment for DSAR queries.
4. Backups, cold storage, embeddings, vector stores, and AI training data are within scope of search unless excluded by a documented technical impossibility analysis.
5. Volume spikes that threaten the SLA are escalated to the Data Protection Officer with a documented mitigation plan.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Articles 12 to 23 | Data subject rights |
| UK GDPR | Articles 12 to 23 | Equivalent rights |
| LGPD | Articles 17 to 22 | Subject rights |
| CPPA | Sections 12 to 19 (proposed) | Access and other rights |
| PIPL | Articles 44 to 50 | Personal information subject rights |
| CCPA / CPRA | Sections 1798.100 to 1798.135 | Consumer rights |
| ISO/IEC 27701 | §7.3 | Data subject rights |
| NIST Privacy Framework | CT.PO-P3 | Individual rights and choices |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. Adopting organizations must integrate the workflow with their own case-management system, populate per-system search procedures, document jurisdictional exceptions, and validate response windows against the specific regimes applicable to each request. The template is not legal advice.

---

**End of Document**
