# Data Subject Rights Management Procedure

**Document Title:** Data Subject Rights Management Procedure\
**Document Type:** Procedure\
**Version:** 1.5.2\
**Date:** 2026-07-01\
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

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the end-to-end process for receiving, validating, fulfilling, and documenting requests from individuals exercising their rights over personal data held by the organisation. It ensures that compliance with applicable data subject rights obligations under GDPR, UK GDPR, PIPEDA, PIPL, and related laws, and establishes consistent standards for identity verification, response timelines, denial justification, and record keeping.

The procedure is aligned to ISO/IEC 27701:2025 (PII principals' rights; section numbering changed in 2025 standalone revision), GDPR Articles 15 to 22, PIPEDA Schedule 1 (CSA Model Code fair-information principles), PIPL Articles 44 to 47, and CSA CCM v4.1 DSP-11.

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
| **Data Protection Officer** | Operational ownership of the DSR process. Manages the DSR register, coordinates fulfilment, reviews responses for accuracy and completeness, and escalates complex or contentious requests to the CIO. |
| **Legal Counsel** | Advises on exemptions, applicable law, and denial justifications. Reviews and approves responses involving potentially litigation-sensitive information or novel legal questions. |
| **CISO** | Ensures that technical measures are available to locate, extract, restrict, and delete personal data across systems. Provides guidance on AI system data retrieval and AI-derived data scope. |
| **IT Operations / System Owners** | Execute data location, extraction, restriction, and deletion actions as directed by the Data Protection Officer within defined timeframes. |
| **All Employees** | Forward any received data subject request to the Data Protection Officer immediately upon receipt. No employee may respond to, dismiss, or take action on a DSR without Data Protection Officer involvement. |

### 2.2 Acting DPO status

The CIO currently assumes all responsibilities normally assigned to a Data Protection Officer (DPO) as documented in [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md) §Governance and [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md). All references to DPO in this procedure refer to the CIO in that acting capacity until a formal appointment is made.

---

## 3. Rights catalogue

The following table defines the rights managed under this procedure, the applicable legal instruments, standard response timeframes, and key exemptions.

| Right | Applicable Laws | Scope | Response Timeframe | Key Exemptions |
| --- | --- | --- | --- | --- |
| **Access (Subject Access Request / SAR)** | GDPR Art. 15; UK GDPR Art. 15; PIPEDA Sch 1 Principle 9 (Individual Access); PIPL Art. 45 | Confirmation that data is held; categories of data; purposes; recipients; retention periods; source; automated decision logic where applicable | 30 days (extendable to 90 days for complexity or volume with notification at day 30) | Data subject rights of third parties; legal professional privilege; ongoing law enforcement cooperation; disproportionate effort for purely archival data |
| **Correction / Rectification** | GDPR Art. 16; UK GDPR Art. 16; PIPEDA Sch 1 Principle 9 (amendment of inaccurate data); PIPL Art. 46 | Correction of inaccurate personal data; completion of incomplete data | 30 days | Data that is required for legal or regulatory compliance in its current form; disputes over factual accuracy subject to legal assessment |
| **Deletion / Erasure (Right to be Forgotten)** | GDPR Art. 17; UK GDPR Art. 17 | Erasure of personal data where no longer necessary; consent withdrawn; unlawful processing; legal obligation to erase | 30 days (subject to retention obligations) | Legal obligation to retain; defence of legal claims; public interest; legitimate interests overriding erasure; statutory or regulatory retention requirements |
| **Data Portability** | GDPR Art. 20; UK GDPR Art. 20 | Provision of data in a structured, commonly used, machine-readable format; direct transmission to another controller where technically feasible | 30 days | Applies only to data provided by the individual and processed by consent or contract; does not apply to data processed under other legal bases |
| **Restriction of Processing** | GDPR Art. 18; UK GDPR Art. 18 | Marking data to restrict active processing while accuracy, lawfulness, or competing interests are assessed | Acknowledgement within 72 hours; restriction applied within 30 days | Restriction lifted only on data subject consent, legal claims, overriding public interest, or resolution of the disputed grounds |
| **Objection to Processing** | GDPR Art. 21; UK GDPR Art. 21; PIPEDA Sch 1 Principle 3 (withdrawal of consent) | Right to object to processing based on legitimate interests or for direct marketing | Halt direct marketing processing immediately; assess other objections and respond within 30 days | Compelling legitimate grounds overriding the individual's interests; legal claims |
| **Automated Decision Review (including profiling)** | GDPR Art. 22; UK GDPR Art. 22 | Right to not be subject to solely automated decisions with significant legal or similarly significant effect; request human review | Acknowledgement within 5 business days; human review completed within 30 days | Decisions necessary for contract performance; authorized by law; explicit consent with appropriate safeguards |

**Canadian legal basis.** The in-force Canadian federal basis for these rights is PIPEDA Schedule 1 (the CSA Model Code fair-information principles): access and amendment rest on Principle 9 (Individual Access), and objection rests on Principle 3 (Consent, including withdrawal of consent). PIPEDA does not provide a standalone right to erasure or a right not to be subject to automated decision-making; for those, the basis above is GDPR (and equivalents). The Consumer Privacy Protection Act (CPPA, Part 1 of Bill C-27) would have introduced disposal and automated-decision-explanation rights, but Bill C-27 lapsed at the 2025-01-06 prorogation and is **not in force**; it would require reintroduction in a future Parliament (see [`privacy/jurisdictions/annex-privacy-canada.md`](jurisdictions/annex-privacy-canada.md)). Where the organisation processes the personal information of Quebec residents, Quebec Law 25 provides stronger rights (including portability and de-indexing) and applies in addition to PIPEDA.

---

## 4. Request intake

### 4.1 Submission channels

Data subjects may submit requests through:

- The designated privacy request contact (email address or web portal maintained by the Data Protection Officer).
- Written correspondence to the organisation's registered address, directed to the Data Protection Officer.
- Any other channel where a request is received by an employee; employees must forward to the Data Protection Officer on the same business day.

The Data Protection Officer maintains the official DSR submission channel and ensures that it is published in the organisation's privacy notice.

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
- Assigned Data Protection Officer
- Response deadline (calculated from date received)
- Current status
- Outcome

---

## 5. Triage and assessment

Following intake and initial logging, the Data Protection Officer completes a triage assessment within 3 business days:

1. **Confirm identity:** Verify that identity verification has been completed or is in progress. If not in progress, initiate verification.
2. **Determine applicable law:** Identify the jurisdiction(s) governing the request based on the data subject's location, the applicable privacy law, and the data categories involved.
3. **Determine the right(s) invoked:** Confirm which rights under §3 apply and whether all conditions for the right are prima facie met.
4. **Check exemptions:** Review whether any exemptions in §3 apply and document the assessment.
5. **Scope the request:** For access requests, identify all systems, data stores, third-party processors, and AI systems that may hold relevant personal data.
6. **Assign to Data Protection Officer:** Assign formal ownership and confirm the response deadline in the DSR register.
7. **Notify the data subject:** Send an acknowledgement confirming receipt, the estimated response timeframe, and any verification requirements still outstanding.

---

## 6. Fulfilment workflow

### 6.1 Data location

The Data Protection Officer coordinates with IT Operations and relevant System Owners to locate all personal data within scope of the request. Data location covers:

- Primary operational systems and databases.
- Archival and backup systems (where technically accessible without disproportionate effort).
- Cloud platform storage and SaaS applications.
- Third-party processors and sub-processors subject to data processing agreements.
- AI systems that process, store, or generate outputs from the data subject's personal data, including AI-derived data and profiling outputs.

### 6.2 Scoping the response

The Data Protection Officer determines:

- Which data falls within the scope of the specific right invoked.
- Whether any exemptions apply to specific data elements.
- Whether any third-party personal data is intermingled with the requestor's data and must be redacted before disclosure.

### 6.3 Redaction of third-party data

Responses must not disclose the personal data of third parties without their consent or legal basis. Redaction must be applied to:

- Names, contact details, or identifying information of other individuals appearing in documents or records.
- Data that, in combination with the disclosed data, would allow identification of another individual.

Redaction must be documented in the fulfilment record. The Data Protection Officer retains the unredacted version in the case file.

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
- The request is manifestly unfounded or excessive (repeat or abusive requests); this must be assessed individually and objectively per the Article 12(5) assessment checklist in §7.2.

### 7.2 Article 12(5) assessment checklist (manifestly unfounded or excessive)

GDPR Article 12(5) provides that DSR responses are **free of charge by default**. Two exceptions allow the controller to either charge a reasonable fee OR refuse the request: where the request is **manifestly unfounded** OR **manifestly excessive**. Article 12(5) imposes the **burden of proof on the controller**: the controller must demonstrate the manifestly-unfounded-or-excessive character of the request, not the data subject's good faith.

This section structures that assessment as a checklist. Every invocation of Article 12(5) requires documented evidence against each applicable criterion before fee or refusal is communicated to the subject.

#### 7.2.1 Default: free of charge

| Default | Reference |
|---|---|
| All DSRs handled free of charge | GDPR Article 12(5) sentence 1 |
| Information under Articles 13 and 14 (privacy notices) provided free | Article 12(5) sentence 1 |
| Communications under Articles 15 to 22 (access, rectification, erasure, restriction, portability, objection, automated decision-making) provided free | Article 12(5) sentence 1 |
| Breach notifications to data subjects under Article 34 provided free | Article 12(5) sentence 1 |

A charge or refusal is the **exception**; the assessment below must support either action with documented evidence.

#### 7.2.2 Manifestly unfounded: criteria

A request is "manifestly unfounded" when, on the face of it, the request has no legitimate basis under Articles 15 to 22. Tests applied (assess each individually; document evidence):

| Criterion | Description | Evidence required |
|---|---|---|
| (a) No nexus to actual processing | Subject is not, and has never been, a data subject of the controller (e.g., never customer, employee, applicant, recipient of services) | Identity verification result; absence of records in any system of record |
| (b) Request inconsistent with stated grounds | Subject states a reason that is contradicted by the controller's records or by the subject's prior communications | Quoted statements; record cross-references |
| (c) Abusive purpose evident | Request submitted with declared abusive intent (e.g., to harass staff, to disrupt operations, to bring leverage in an unrelated dispute) | Documented threats, public statements, or correspondence demonstrating intent |
| (d) Request lacks coherent specification | Request is incomprehensible or non-specific after a single reasonable clarification attempt | Clarification request issued; subject's response or non-response within 30 days |

A request is NOT manifestly unfounded merely because the subject is unhappy with the controller, exercises rights frequently in good faith, or seeks a result the controller does not wish to provide.

#### 7.2.3 Manifestly excessive: criteria

A request is "manifestly excessive" when its volume or repetition is disproportionate to legitimate exercise of the right. Tests applied:

| Criterion | Description | Evidence required |
|---|---|---|
| (a) Repetitive in short interval | The same subject made the same or substantially similar request within a defined short interval; the prior request was responded to in full | Prior request log; date-and-content comparison; demonstrated overlap of scope |
| (b) Disproportionate volume | Volume of records requested exceeds what is reasonably needed for the subject to verify or act on their rights | Record-count estimate; effort estimate; subject's stated purpose where available |
| (c) Disproportionate scope sweep | Subject requests "all records" without scope limitation despite previous specific responses | History of prior requests; categorisation of available record types |
| (d) Use of request as discovery vehicle | Pattern of requests calibrated to obtain materials for litigation, journalism, or competitive intelligence rather than for the subject's own data | Pattern documentation; volume trajectory |

The repetitive-in-short-interval test (criterion a) is the most commonly used and the easiest to evidence. Other criteria require closer judgement; consult Legal Counsel before invoking criteria (b), (c), or (d).

#### 7.2.4 Action options under Article 12(5)

Where the assessment supports the manifestly-unfounded-or-excessive determination, the controller may take ONE of two actions:

| Action | Description | Constraints |
|---|---|---|
| **(a) Charge a reasonable fee** | Take into account the administrative costs of providing the information, the communication, or the action requested | Fee MUST be cost-recovery, not punitive; the controller must be able to demonstrate the cost-basis of the fee |
| **(b) Refuse to act on the request** | Decline the request entirely | Subject retains the right to lodge a complaint with the supervisory authority and to seek judicial remedy per Articles 77-79 |

The controller cannot do both (charge a fee AND refuse the substantive action); the language of Article 12(5) is an either/or election.

#### 7.2.5 Burden-of-proof requirements

Per Article 12(5) sentence 3, the controller bears the burden of demonstrating the manifestly-unfounded-or-excessive character. The documentation required:

1. Written assessment against each criterion in §7.2.2 and §7.2.3 with quoted evidence.
2. Legal Counsel sign-off on the assessment before fee or refusal is communicated.
3. DPO sign-off on the fee-or-refusal election.
4. Written communication to the subject naming: the determination, the specific Article 12(5) criterion invoked, the action taken (fee with amount and basis, OR refusal), and the subject's right to lodge a complaint with the supervisory authority and to seek judicial remedy per Articles 77 to 79.
5. Entry in the DSR register linking the assessment, sign-offs, and subject communication.

Records retained per the organisation's privacy retention schedule; minimum **3 years** for fee/refusal evidence (or longer where the supervisory authority has indicated a longer retention requirement).

#### 7.2.6 Reasonable-fee calculation

Where the controller elects to charge a reasonable fee (Article 12(5)(a)):

| Element | Method |
|---|---|
| Cost categories | (a) staff time for retrieval, review, and redaction; (b) storage media if physical copy requested; (c) postage if physical delivery; (d) external Legal Counsel time if involved in redaction review |
| Hourly rate | Internal staff: salary-based cost-recovery rate (NOT a punitive markup). External counsel: actual rate charged to the controller |
| Fee cap | The fee MUST be cost-recovery only; no profit margin |
| Itemisation | Fee communication to the subject MUST itemise the cost categories and time/rate applied |
| Payment method | The controller may NOT require advance payment that effectively denies the right; payment-on-delivery is acceptable; instalment options should be offered for substantial fees |
| Waiver | The controller MAY waive the fee in cases of demonstrated financial hardship without prejudice |

The fee schedule should be documented as an internal cost-recovery policy reviewed annually.

#### 7.2.7 Cross-regime equivalents

| Regime | Equivalent provision | Notable variations |
|---|---|---|
| **UK GDPR** (UK) | Article 12(5) (same as EU GDPR) | ICO Subject Access Code of Practice provides guidance; "reasonable fee" interpreted as administrative cost only |
| **LGPD** (Brazil, Article 18) | Free of charge by default; ANPD may establish exceptions in regulation | No explicit "manifestly unfounded or excessive" exception in primary law |
| **PIPL** (China, Article 50) | Free of charge by default; processor may charge reasonable fee for "repeated handler-of-information information requests" | "Repeated" threshold not statutorily defined; processor must justify |
| **PIPEDA** (Canada) | OPC guidance: free of charge by default; nominal fee permitted for non-routine requests with prior notice to the subject | Subject must have option to abandon request after fee notice |
| **CCPA / CPRA** (California) | Generally free; "manifestly unfounded or excessive, in particular because of their repetitive nature" exception; controller may charge reasonable fee or decline | Mirrors GDPR Article 12(5) language closely |
| **APPI** (Japan, Article 38) | Reasonable fee permitted; must be communicated in advance | No explicit "manifestly unfounded" gate |

When the joint controllers or processors operate across multiple regimes, the strictest applicable regime governs (typically GDPR/UK GDPR where applicable).

### 7.3 Denial process

1. The Data Protection Officer documents the proposed grounds for denial with reference to the specific legal provision.
2. Legal Counsel reviews the denial rationale and confirms the legal basis.
3. The CIO (acting DPO) signs off on the denial in writing before notification is sent to the data subject.
4. The data subject is notified in writing of the denial, the specific grounds, and their right to lodge a complaint with the relevant supervisory authority (ICO, OPC, CAI, or other applicable authority).
5. The denial, its grounds, and the CIO sign-off are recorded in the DSR register.

All denials must be justified in writing and reviewed by the CIO (acting DPO) before being communicated to the data subject, consistent with [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md) §4.8.

---

## 8. Cross-border and AI considerations

### 8.1 Cross-border requests

Where a request involves personal data transferred across jurisdictions, the Data Protection Officer:

- Determines the applicable legal rights in each relevant jurisdiction.
- Identifies any legal mechanism constraints (e.g., PIPL restrictions on disclosing China-held data in response to foreign legal requests).
- Consults Legal Counsel before fulfilling or denying the cross-border element of the request.

### 8.2 AI-derived data

Data subjects have the right to access data held about them regardless of whether it was directly provided or derived through automated processing, including AI systems. When fulfilling access requests:

- The scope of the response includes AI-inferred or AI-derived personal data attributes (e.g., risk scores, profiling outputs, predicted categories) where those attributes are held and associated with the data subject.
- The Data Protection Officer coordinates with the CISO and AI system owners to retrieve AI-derived data within the access scope.
- The system card or model card for relevant AI systems is consulted to confirm what data is generated and retained.

### 8.3 Automated decision review (GDPR art. 22)

Where a data subject exercises their right to human review of an automated decision:

1. The Data Protection Officer identifies the AI system and decision record involved.
2. A qualified human reviewer (not the same system that generated the original decision) conducts an independent review within 30 days.
3. The reviewer documents the logic reviewed, the evidence assessed, the outcome, and any changes to the original decision.
4. The data subject is notified of the review outcome in writing.
5. If the original decision is maintained, the reasons must be clearly explained.

---

## 9. Record keeping

### 9.1 DSR register

The Data Protection Officer maintains the DSR register as a living record of all requests received. The register must be accessible to the CIO and available for production to supervisory authorities on request. The DSR register contains, for each request, all fields defined in §4.3 plus fulfilment notes, denial grounds where applicable, and closure date.

### 9.2 Retention

DSR records, including intake records, identity verification evidence, internal assessments, response copies, denial documentation, and CIO sign-off records, are retained for 3 years following the closure date of each request, consistent with the retention schedule in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) (Privacy / Data Subject Requests: 3 years post-closure).

Records subject to regulatory investigation, litigation hold, or supervisory authority inquiry are retained until the hold is formally lifted by Legal Counsel, regardless of the standard retention period.

### 9.3 Evidence of fulfilment

For each completed request, the case file must include:

- Confirmation of identity verification method and outcome.
- Data location and scope documentation.
- Redaction log (where applicable).
- Copy of the response delivered to the data subject.
- Secure delivery confirmation.
- Closure approval by the Data Protection Officer.

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
| Data subject rights management | ISO/IEC 27701:2025 (PII principals' rights); CSA CCM v4.1 DSP-11 |
| Access and transparency | GDPR Art. 15; UK GDPR Art. 15; PIPEDA Sch 1 Principle 9 (Individual Access); PIPL Art. 45 |
| Correction and rectification | GDPR Art. 16; UK GDPR Art. 16; PIPEDA Sch 1 Principle 9 (amendment); PIPL Art. 46 |
| Deletion and erasure | GDPR Art. 17; UK GDPR Art. 17 |
| Data portability | GDPR Art. 20; UK GDPR Art. 20 |
| Restriction of processing | GDPR Art. 18; UK GDPR Art. 18 |
| Objection to processing | GDPR Art. 21; UK GDPR Art. 21; PIPEDA Sch 1 Principle 3 (withdrawal of consent) |
| Automated decision review | GDPR Art. 22; UK GDPR Art. 22 |
| DPO accountability and record keeping | GDPR Art. 37 to 39; ISO/IEC 27701 §6.2.3 |
| Retention of DSR records | [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) |

---

*This document is released under the CC BY-SA 4.0 licence. To the extent possible under law, all copyright and related rights are waived. See [`LICENSE`](../LICENSE) in the repository root.*

---

**End of Document**
