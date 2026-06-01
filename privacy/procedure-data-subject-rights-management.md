# Data Subject Rights Management Procedure

**Document Title:** Data Subject Rights Management Procedure\
**Document Type:** Procedure\
**Version:** 1.3.0\
**Date:** 2026-05-27\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the end-to-end process for receiving, validating, fulfilling, and documenting requests from individuals exercising their rights over personal data held by the organisation. It ensures that compliance with applicable data subject rights obligations under GDPR, UK GDPR, CPPA, PIPL, and related laws, and establishes consistent standards for identity verification, response timelines, denial justification, and record keeping.

The procedure is aligned to ISO/IEC 27701:2025 (PII principals' rights; section numbering changed in 2025 standalone revision), GDPR Articles 15 to 22, CPPA Part 2 Division 5, PIPL Articles 44 to 47, and CSA CCM v4.1 PRI-04.

### 1.2 Scope

1. Applies to all personal data held by the organisation in any format, structured, unstructured, digital, or physical, across all systems, applications, and third-party processors.
2. Covers requests submitted by individuals including employees, customers, suppliers, and other data subjects regardless of jurisdiction, subject to applicable legal rights.
3. Covers all rights categories: access (Subject Access Request / SAR), correction, deletion, data portability, restriction of processing, objection to processing, and review of automated decisions.
4. Includes AI-derived or AI-processed personal data where the individual is the subject of that data.
5. Does not apply to data that is fully anonymized and no longer capable of identifying an individual.

---

## 2. Governance

### 2.1 Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **Chief Information Officer (CIO, acting DPO)** | Accountable executive for the data subject rights programme. Signs off on all denials. Assumes DPO responsibilities until a formal DPO is appointed. Represents the organisation in regulatory matters relating to data subject rights. |
| **Privacy Officer** | Operational ownership of the DSR process. Manages the DSR register, coordinates fulfilment, reviews responses for accuracy and completeness, and escalates complex or contentious requests to the CIO. |
| **Legal Counsel** | Advises on exemptions, applicable law, and denial justifications. Reviews and approves responses involving potentially litigation-sensitive information or novel legal questions. |
| **CISO** | Ensures that technical measures are available to locate, extract, restrict, and delete personal data across systems. Provides guidance on AI system data retrieval and AI-derived data scope. |
| **IT Operations / System Owners** | Execute data location, extraction, restriction, and deletion actions as directed by the Privacy Officer within defined timeframes. |
| **All Employees** | Forward any received data subject request to the Privacy Officer immediately upon receipt. No employee may respond to, dismiss, or take action on a DSR without Privacy Officer involvement. |

### 2.2 Acting DPO status

The CIO currently assumes all responsibilities normally assigned to a Data Protection Officer (DPO) as documented in [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md) §Governance and [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md). All references to DPO in this procedure refer to the CIO in that acting capacity until a formal appointment is made.

---

## 3. Rights catalogue

The following table defines the rights managed under this procedure, the applicable legal instruments, standard response timeframes, and key exemptions.

| Right | Applicable Laws | Scope | Response Timeframe | Key Exemptions |
| --- | --- | --- | --- | --- |
| **Access (Subject Access Request / SAR)** | GDPR Art. 15; UK GDPR Art. 15; CPPA s.63; PIPL Art. 45 | Confirmation that data is held; categories of data; purposes; recipients; retention periods; source; automated decision logic where applicable | 30 days (extendable to 90 days for complexity or volume with notification at day 30) | Data subject rights of third parties; legal professional privilege; ongoing law enforcement cooperation; disproportionate effort for purely archival data |
| **Correction / Rectification** | GDPR Art. 16; UK GDPR Art. 16; CPPA s.66; PIPL Art. 46 | Correction of inaccurate personal data; completion of incomplete data | 30 days | Data that is required for legal or regulatory compliance in its current form; disputes over factual accuracy subject to legal assessment |
| **Deletion / Erasure (Right to be Forgotten)** | GDPR Art. 17; UK GDPR Art. 17; CPPA s.69 | Erasure of personal data where no longer necessary; consent withdrawn; unlawful processing; legal obligation to erase | 30 days (subject to retention obligations) | Legal obligation to retain; defence of legal claims; public interest; legitimate interests overriding erasure; statutory or regulatory retention requirements |
| **Data Portability** | GDPR Art. 20; UK GDPR Art. 20 | Provision of data in a structured, commonly used, machine-readable format; direct transmission to another controller where technically feasible | 30 days | Applies only to data provided by the individual and processed by consent or contract; does not apply to data processed under other legal bases |
| **Restriction of Processing** | GDPR Art. 18; UK GDPR Art. 18 | Marking data to restrict active processing while accuracy, lawfulness, or competing interests are assessed | Acknowledgement within 72 hours; restriction applied within 30 days | Restriction lifted only on data subject consent, legal claims, overriding public interest, or resolution of the disputed grounds |
| **Objection to Processing** | GDPR Art. 21; UK GDPR Art. 21; CPPA s.67 | Right to object to processing based on legitimate interests or for direct marketing | Halt direct marketing processing immediately; assess other objections and respond within 30 days | Compelling legitimate grounds overriding the individual's interests; legal claims |
| **Automated Decision Review (including profiling)** | GDPR Art. 22; UK GDPR Art. 22; CPPA s.63(3) | Right to not be subject to solely automated decisions with significant legal or similarly significant effect; request human review | Acknowledgement within 5 business days; human review completed within 30 days | Decisions necessary for contract performance; authorized by law; explicit consent with appropriate safeguards |

---

## 4. Request intake

### 4.1 Submission channels

Data subjects may submit requests through:

- The designated privacy request contact (email address or web portal maintained by the Privacy Officer).
- Written correspondence to the organisation's registered address, directed to the Privacy Officer.
- Any other channel where a request is received by an employee; employees must forward to the Privacy Officer on the same business day.

The Privacy Officer maintains the official DSR submission channel and ensures that it is published in the organisation's privacy notice.

### 4.2 Identity verification

Identity verification is required before any personal data is disclosed or action taken. The verification standard must be proportionate to the sensitivity of the data involved.

| Verification Level | When Applied | Acceptable Methods |
| --- | --- | --- |
| **Standard** | General access, correction, or deletion requests for low-sensitivity data categories | Government-issued photo ID; confirmation of account details or employment record; two independently verifiable data points matching held records |
| **Enhanced** | Requests involving health, financial, or biometric data; requests with indications of identity fraud; requests from authorized third parties acting on behalf of the data subject | Government-issued photo ID plus secondary verification; notarized authorization for third-party requestors |
| **Re-verification** | Requests for the same data type made within 12 months of a prior request | Standard verification unless circumstances indicate heightened risk |

Requests where identity cannot be verified within 10 business days are suspended. The data subject is notified of the verification requirement and given a reasonable further period to provide acceptable evidence.

### 4.3 DSR register logging

Upon receipt, every request is assigned a unique DSR identifier and logged in the DSR register with:

- DSR ID
- Date received (and time where received electronically)
- Right(s) requested
- Data subject identity (verified / pending verification)
- Applicable jurisdiction(s) and governing law
- Assigned Privacy Officer
- Response deadline (calculated from date received)
- Current status
- Outcome

---

## 5. Triage and assessment

Following intake and initial logging, the Privacy Officer completes a triage assessment within 3 business days:

1. **Confirm identity:** Verify that identity verification has been completed or is in progress. If not in progress, initiate verification.
2. **Determine applicable law:** Identify the jurisdiction(s) governing the request based on the data subject's location, the applicable privacy law, and the data categories involved.
3. **Determine the right(s) invoked:** Confirm which rights under §3 apply and whether all conditions for the right are prima facie met.
4. **Check exemptions:** Review whether any exemptions in §3 apply and document the assessment.
5. **Scope the request:** For access requests, identify all systems, data stores, third-party processors, and AI systems that may hold relevant personal data.
6. **Assign to Privacy Officer:** Assign formal ownership and confirm the response deadline in the DSR register.
7. **Notify the data subject:** Send an acknowledgement confirming receipt, the estimated response timeframe, and any verification requirements still outstanding.

---

## 6. Fulfilment workflow

### 6.1 Data location

The Privacy Officer coordinates with IT Operations and relevant System Owners to locate all personal data within scope of the request. Data location covers:

- Primary operational systems and databases.
- Archival and backup systems (where technically accessible without disproportionate effort).
- Cloud platform storage and SaaS applications.
- Third-party processors and sub-processors subject to data processing agreements.
- AI systems that process, store, or generate outputs from the data subject's personal data, including AI-derived data and profiling outputs.

### 6.2 Scoping the response

The Privacy Officer determines:

- Which data falls within the scope of the specific right invoked.
- Whether any exemptions apply to specific data elements.
- Whether any third-party personal data is intermingled with the requestor's data and must be redacted before disclosure.

### 6.3 Redaction of third-party data

Responses must not disclose the personal data of third parties without their consent or legal basis. Redaction must be applied to:

- Names, contact details, or identifying information of other individuals appearing in documents or records.
- Data that, in combination with the disclosed data, would allow identification of another individual.

Redaction must be documented in the fulfilment record. The Privacy Officer retains the unredacted version in the case file.

### 6.4 Preparation and delivery of response

Responses are prepared in clear, plain language. The response format depends on the right invoked:

| Right | Response Format |
| --- | --- |
| Access (SAR) | Summary of data held; attachment of data copies in PDF or other accessible format; explanation of processing purposes, retention, and recipients |
| Correction | Confirmation of correction made; or explanation of why correction was not made with legal basis |
| Deletion | Confirmation of deletion and scope; or explanation of retention obligation with legal basis |
| Portability | Machine-readable export (CSV, JSON, or equivalent) of requested data |
| Restriction | Confirmation that restriction has been applied and description of its scope; notification when restriction is lifted |
| Objection | Confirmation that processing has ceased (for direct marketing) or assessment outcome with legal basis |
| Automated Decision Review | Explanation of the logic applied; outcome of human review; any changes resulting from the review |

Responses are delivered via a secure channel. Transmission of personal data by unencrypted email is prohibited.

---

## 7. Denial and exemptions

### 7.1 Grounds for denial

A request may be denied wholly or in part on the following grounds (non-exhaustive; determined by applicable law):

- Exercising or defending legal claims.
- Legal professional privilege.
- Prevention, detection, or prosecution of criminal offences.
- Protection of the rights of third parties.
- Statutory or regulatory retention obligation preventing deletion.
- The right invoked does not apply under the relevant law (e.g., portability not available for data processed under legitimate interests).
- The request is manifestly unfounded or excessive (repeat or abusive requests); this must be assessed individually and objectively.

### 7.2 Denial process

1. The Privacy Officer documents the proposed grounds for denial with reference to the specific legal provision.
2. Legal Counsel reviews the denial rationale and confirms the legal basis.
3. The CIO (acting DPO) signs off on the denial in writing before notification is sent to the data subject.
4. The data subject is notified in writing of the denial, the specific grounds, and their right to lodge a complaint with the relevant supervisory authority (ICO, OPC, CAI, or other applicable authority).
5. The denial, its grounds, and the CIO sign-off are recorded in the DSR register.

All denials must be justified in writing and reviewed by the CIO (acting DPO) before being communicated to the data subject, consistent with [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md) §8.

---

## 8. Cross-border and AI considerations

### 8.1 Cross-border requests

Where a request involves personal data transferred across jurisdictions, the Privacy Officer:

- Determines the applicable legal rights in each relevant jurisdiction.
- Identifies any legal mechanism constraints (e.g., PIPL restrictions on disclosing China-held data in response to foreign legal requests).
- Consults Legal Counsel before fulfilling or denying the cross-border element of the request.

### 8.2 AI-derived data

Data subjects have the right to access data held about them regardless of whether it was directly provided or derived through automated processing, including AI systems. When fulfilling access requests:

- The scope of the response includes AI-inferred or AI-derived personal data attributes (e.g., risk scores, profiling outputs, predicted categories) where those attributes are held and associated with the data subject.
- The Privacy Officer coordinates with the CISO and AI system owners to retrieve AI-derived data within the access scope.
- The system card or model card for relevant AI systems is consulted to confirm what data is generated and retained.

### 8.3 Automated decision review (GDPR art. 22 / CPPA)

Where a data subject exercises their right to human review of an automated decision:

1. The Privacy Officer identifies the AI system and decision record involved.
2. A qualified human reviewer (not the same system that generated the original decision) conducts an independent review within 30 days.
3. The reviewer documents the logic reviewed, the evidence assessed, the outcome, and any changes to the original decision.
4. The data subject is notified of the review outcome in writing.
5. If the original decision is maintained, the reasons must be clearly explained.

---

## 9. Record keeping

### 9.1 DSR register

The Privacy Officer maintains the DSR register as a living record of all requests received. The register must be accessible to the CIO and available for production to supervisory authorities on request. The DSR register contains, for each request, all fields defined in §4.3 plus fulfilment notes, denial grounds where applicable, and closure date.

### 9.2 Retention

DSR records, including intake records, identity verification evidence, internal assessments, response copies, denial documentation, and CIO sign-off records, are retained for 2 years following the closure date of each request, consistent with the retention schedule in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) (Privacy / Data Subject Requests: 2 years post-closure).

Records subject to regulatory investigation, litigation hold, or supervisory authority inquiry are retained until the hold is formally lifted by Legal Counsel, regardless of the standard retention period.

### 9.3 Evidence of fulfilment

For each completed request, the case file must include:

- Confirmation of identity verification method and outcome.
- Data location and scope documentation.
- Redaction log (where applicable).
- Copy of the response delivered to the data subject.
- Secure delivery confirmation.
- Closure approval by the Privacy Officer.

---

## 10. Metrics

The following metrics are tracked and reported to the CIO at the quarterly Privacy Governance Review:

| Metric | Definition | Target |
| --- | --- | --- |
| **Requests Received** | Total DSRs received in the reporting period, by right type | Tracked; volume trend monitored |
| **On-Time Fulfilment Rate (%)** | Percentage of requests fulfilled within the applicable legal timeframe | ≥ 95% |
| **Denial Rate (%)** | Percentage of requests denied wholly or in part | Tracked; material increase triggers process review |
| **Average Response Time (days)** | Mean number of calendar days from request receipt to response delivery | Target: ≤ 25 days (ahead of the 30-day deadline) |
| **Identity Verification Failure Rate (%)** | Percentage of requests suspended or closed due to failure to verify identity | Tracked; used to assess intake process usability |
| **AI-Related DSR Rate (%)** | Percentage of SARs that included AI-derived data elements in scope | Tracked; informs AI data governance programme |
| **Escalations to CIO** | Number of requests escalated to CIO for denial sign-off or complex legal determination | Tracked |

---

## 11. Framework alignment

| Control Area | Framework Reference |
| --- | --- |
| Data subject rights management | ISO/IEC 27701:2025 (PII principals' rights); CSA CCM v4.1 PRI-04 |
| Access and transparency | GDPR Art. 15; UK GDPR Art. 15; CPPA s.63; PIPL Art. 45 |
| Correction and rectification | GDPR Art. 16; UK GDPR Art. 16; CPPA s.66; PIPL Art. 46 |
| Deletion and erasure | GDPR Art. 17; UK GDPR Art. 17; CPPA s.69 |
| Data portability | GDPR Art. 20; UK GDPR Art. 20 |
| Restriction of processing | GDPR Art. 18; UK GDPR Art. 18 |
| Objection to processing | GDPR Art. 21; UK GDPR Art. 21; CPPA s.67 |
| Automated decision review | GDPR Art. 22; UK GDPR Art. 22; CPPA s.63(3) |
| DPO accountability and record keeping | GDPR Art. 37 to 39; ISO/IEC 27701 §6.2.3 |
| Retention of DSR records | [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) |

---

*This document is released under the CC BY-SA 4.0 licence. To the extent possible under law, all copyright and related rights are waived. See [`LICENSE`](../LICENSE) in the repository root.*

---

**End of Document**
