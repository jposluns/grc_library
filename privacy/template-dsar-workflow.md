# Data Subject Access Request Workflow Template

**Document Title:** Data Subject Access Request Workflow Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Privacy Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, jurisdictional, or system-of-record change\
**Repository Path:** [`privacy/template-dsar-workflow.md`](template-dsar-workflow.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines an operational workflow for handling Data Subject Access Requests (DSARs) and equivalent rights requests under GDPR, UK GDPR, LGPD, CPPA, PIPL, CCPA, and similar regimes. It complements the Data Subject Rights Management Procedure by providing the request-record structure, the stage gates, the identity verification ladder, and the response artefact format that the procedure relies on. Adopting organisations populate the placeholders, configure their own systems of record, and integrate the workflow with their case-management tooling.

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
| SLA | Acknowledge within 1 business day |
| Quality gates | Channel logged; locale set; jurisdiction inferred; right-category classified |

### Stage 2: Identity verification

| Item | Value |
| --- | --- |
| Owner | Privacy team |
| Inputs | Submitter contact, claim of identity, available authentication signals |
| Outputs | Verification record at one of three trust levels (Low, Medium, High) per the table below |
| SLA | Within 3 business days of intake |
| Quality gates | Verification record stored with the request; collection of any additional identifier limited to the minimum required to confirm identity |

| Trust level | Use case | Verification method |
| --- | --- | --- |
| Low | Subject is contacting through an authenticated account channel where the system of record is the same as the channel | Authenticated session is sufficient |
| Medium | Subject is reachable through a registered communication channel that the controller controls | Verification token sent to the registered channel; subject confirms within window |
| High | Subject is asserting identity through an unauthenticated channel and is requesting high-impact action (erasure, portability of comprehensive data set, ADM review) | Government-issued identifier or equivalent strong evidence; review by a second Privacy team member |

If identity verification fails, the request is closed and the submitter is informed.

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
| SLA | Per the right's regulatory window; default 30 calendar days from intake; extendable to 60 or 90 days where permitted with documented reason and subject notification |
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
| Identity trust level | Low, Medium, High |
| Identity verification mechanism | Auth session, registered-channel token, strong identifier |
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
| Supervisory authority complaints | Count of complaints lodged with regulators that reference the organisation | Trend-monitored |
| First-pass identity verification rate | Percentage of requests where identity is verified at the appropriate trust level on the first attempt | At least 90% |

---

## Operating expectations

1. The DSAR record is the single authoritative trail for each request. No off-record handling.
2. Privacy team rotates the on-call intake role to maintain a 1-business-day acknowledgement SLA across timezones.
3. Each system of record listed in the ROPA has a designated steward with a documented response time commitment for DSAR queries.
4. Backups, cold storage, embeddings, vector stores, and AI training data are within scope of search unless excluded by a documented technical impossibility analysis.
5. Volume spikes that threaten the SLA are escalated to the Privacy Officer with a documented mitigation plan.

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

This template is a CC BY-SA 4.0 baseline. Adopting organisations must integrate the workflow with their own case-management system, populate per-system search procedures, document jurisdictional exceptions, and validate response windows against the specific regimes applicable to each request. The template is not legal advice.

---

**End of Document**
