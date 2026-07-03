# GRC Programme Management and Annual Review Procedure

**Document Title:** GRC Programme Management and Annual Review Procedure\
**Document Type:** Procedure\
**Version:** 1.0.6\
**Date:** 2026-07-02\
**Owner:** GRC Programme Manager\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../dev-security/register-compliance-controls-and-gap-register.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change\
**Repository Path:** [`governance/procedure-grc-programme-management-and-annual-review.md`](procedure-grc-programme-management-and-annual-review.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This procedure governs the annual GRC programme management cycle. It defines how the GRC library is reviewed, updated, version-controlled, reported on, and presented to the Enterprise Risk Committee (ERC). It establishes the cadence and accountability framework for annual governance reviews, quarterly reporting, policy owner attestation, control testing scheduling, risk treatment status updates, and ERC reporting.

This procedure aligns to ISO 37301:2021 §9 (Performance evaluation), ISO/IEC 27001:2022 §9.3 (Management review), ISO 31000:2018 §6.6 (Monitoring and review), and COBIT 2019 APO01 (Managed IT Management Framework).

---

## 2. Scope

2.1 This procedure applies to all documents held in the GRC library, spanning the following domains: governance, risk, compliance, information security, privacy, artificial intelligence governance, resilience, supply chain security, IT operations, and development security.

2.2 The GRC Programme Manager is the primary responsible party for coordinating the annual review cycle and for maintaining the quality and currency of the library.

2.3 This procedure applies to all document owners, domain approvers, and governance bodies with authority over GRC library documents.

2.4 This procedure does not govern individual audit engagements (see the Internal Audit Standard) or individual corrective actions (see the CAPA Procedure), although outputs from those processes feed into the annual GRC programme report.

---

## 3. Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| GRC Programme Manager | Coordinates the annual review cycle. Maintains the document index and version register. Collates review attestations. Drafts the annual GRC programme report. Publishes approved changes. Maintains the rolling control testing schedule. Produces quarterly GRC metrics reports. |
| Chief Information Security Officer (CISO) | Approving authority for security and AI governance domain documents. Reviews and approves security and AI-related changes. Receives quarterly GRC metrics reports. |
| Data Protection Officer | Approving authority for privacy domain documents. Reviews privacy-related changes and ensures that alignment with applicable data protection law is maintained. |
| Chief Risk Officer | Approving authority for risk domain documents. Reviews risk treatment status updates. Receives quarterly GRC metrics reports. Co-chairs risk register quarterly reviews. |
| Chief Compliance Officer | Approving authority for compliance domain documents. Monitors regulatory change log. Ensures that compliance domain documents remain current with applicable law and regulation. |
| AI Governance Council | Approving authority for AI governance domain documents. Reviews AI policy, standard, and procedure changes. |
| Document Owners | Complete annual attestation for each document they own. Submit change requests by the deadline. Collaborate with the GRC Programme Manager on draft revisions. |
| Enterprise Risk Committee (ERC) | Annual approval authority for the GRC programme report and material policy or framework changes. Provides strategic direction for the GRC programme. |
| Internal Audit | Independently assesses the effectiveness of the GRC programme management process. Samples attestation records, control testing results, and deprovisioning evidence annually. |

---

## 4. Annual review cycle

### 4.1 Calendar and milestones

The following milestones govern each annual review cycle. All dates refer to calendar year unless otherwise stated.

| Month | Milestone | Responsible Party | Output |
| --- | --- | --- | --- |
| January (1st to 31st) | All document owners complete the annual review attestation form for each document they own | All Document Owners | Completed attestation forms submitted to GRC Programme Manager |
| 31 January | Deadline: all attestation forms and change requests submitted to GRC Programme Manager | Document Owners | Change request log compiled |
| February to March | GRC Programme Manager collates attestation outcomes; drafts revisions for approved change requests; prepares annual GRC programme report | GRC Programme Manager | Draft revisions; draft annual GRC programme report |
| 31 March | Annual GRC programme report submitted to ERC for review | GRC Programme Manager | Annual GRC programme report (draft) |
| April | ERC reviews and approves the annual GRC programme report; approves material policy or framework changes | ERC | Approved annual report; approved change list |
| 30 April | All approved changes incorporated into library documents; version numbers incremented; documents published | GRC Programme Manager | Updated GRC library; version register updated; change log closed |
| May to December | Continuous monitoring; triggered reviews upon material regulatory change or significant event | GRC Programme Manager; Domain Approvers | Triggered review records; updated documents as required |

### 4.2 Attestation form content

Each attestation must address the following:

- Document identifier and current version
- Attestation decision: (a) still current, no changes required; (b) minor update required, description provided; (c) material change required: change request submitted
- Domain approver sign-off
- Date of attestation

---

## 5. Triggered (out-of-cycle) reviews

### 5.1 Trigger events

A triggered review is required outside the annual cycle when any of the following events occurs:

| Trigger | Examples |
| --- | --- |
| Material regulatory change | New legislation, amended regulation, new supervisory guidance that affects one or more GRC library documents |
| Significant security incident | Incident classified at severity 1 or 2 that exposes a gap in existing policy, standard, or procedure |
| Major organizational change | Merger, acquisition, divestiture, significant change in business model or operating geography |
| New framework adoption | Adoption of a new compliance framework, certification standard, or industry code that requires GRC library additions or changes |
| ERC instruction | ERC directs a specific document or domain review outside the annual cycle |

### 5.2 Triggered review timeline

5.2.1 Triggered reviews must be completed within 60 calendar days of the trigger event being identified or notified to the GRC Programme Manager.

5.2.2 The GRC Programme Manager will assign the relevant document owner and domain approver and set a completion date within the 60-day window.

5.2.3 Where a triggered review cannot be completed within 60 days (e.g., due to regulatory complexity or pending external guidance), the GRC Programme Manager must escalate to the CISO or relevant domain approver and document the delay with a revised completion date.

5.2.4 Triggered reviews are recorded in the document index alongside their trigger event and completion date.

---

## 6. Document version control

### 6.1 Version numbering convention

All GRC library documents follow semantic versioning using the format MAJOR.MINOR.PATCH:

| Version Component | When Incremented | Example |
| --- | --- | --- |
| MAJOR (x.0.0) | Material change to scope, obligations, governance structure, or key requirements | 1.0.0 → 2.0.0 |
| MINOR (x.y.0) | Minor addition, clarification, or update that does not alter core requirements | 1.0.0 → 1.1.0 |
| PATCH (x.y.z) | Typographical correction, formatting fix, broken link update, minor reference correction | 1.0.0 → 1.0.1 |

### 6.2 Change approval requirements

6.2.1 All version increments, including patch fixes, require sign-off from the document's approving authority before publication.

6.2.2 MAJOR changes additionally require ERC notification (and ERC approval where they relate to policy-level or framework-level documents).

### 6.3 Version history

6.3.1 A version history section must be maintained within each document, recording the version number, date, nature of change, and approving authority for each revision.

6.3.2 The GRC Programme Manager maintains a central version register in the document index register for cross-document tracking.

### 6.4 Retired documents

6.4.1 When a document is superseded, it is retired. Retired documents must be:

- Marked with the `**Status:** Superseded` lifecycle line in its metadata (Classification stays Public; the 2026-07-02 lifecycle-marker migration), with a cross-reference to the superseding document recorded in the document index register
- Archived in the designated document archive location with read-only access
- Cross-referenced from the superseding document with the retirement date
- Not deleted: archived copies must be retained per the Records Retention and Destruction Standard

---

## 7. Policy owner attestation

### 7.1 Annual attestation requirement

7.1.1 Every document owner must complete an annual attestation for each document they own, confirming either:

- The document remains current and no changes are required; or
- A change request is submitted to the GRC Programme Manager

7.1.2 Attestation is due by 31 January of each year, covering documents as they stand on 1 January.

### 7.2 Missing attestation

7.2.1 Where a document owner fails to submit an attestation by 31 January, the GRC Programme Manager will treat the absence as a change-request trigger and initiate a review of the document.

7.2.2 The GRC Programme Manager will escalate missing attestations to the CISO and relevant domain approver by 7 February.

7.2.3 Persistent non-attestation will be reported to the ERC as a governance gap in the annual GRC programme report.

### 7.3 Records retention

7.3.1 Attestation records must be retained for a minimum of 7 years. They constitute evidence of governance oversight for audit and regulatory purposes.

7.3.2 Records must be stored in the approved records management system with access restricted to the GRC Programme Manager, CISO, and Internal Audit.

---

## 8. Control testing schedule

### 8.1 Schedule maintenance

8.1.1 The GRC Programme Manager maintains a rolling 12-month control testing schedule. The schedule is published in the Compliance Controls and Gap Register at the start of each year (Q1).

8.1.2 The schedule assigns each testable control a test frequency, responsible tester, test method (automated or manual), and target completion date.

### 8.2 Testing frequencies

| Control Domain | Minimum Test Frequency |
| --- | --- |
| CSA CCM v4.1 controls | Quarterly |
| COBIT 2019 processes | Annually |
| ISO/IEC 27001:2022 Annex A controls | Annually (or more frequently for high-risk controls as determined by the CISO) |
| Regulatory compliance controls | Per applicable regulatory cadence |

### 8.3 Results recording

8.3.1 All control test results, pass, fail, or exception, must be recorded in the Compliance Controls and Gap Register.

8.3.2 Failed control tests must generate a CAPA in accordance with the CAPA Procedure within 5 business days of the test result being confirmed.

8.3.3 The GRC Programme Manager will report overdue control tests to the CISO as part of the quarterly metrics report.

---

## 9. Quarterly GRC metrics reporting

### 9.1 Purpose and audience

9.1.1 The GRC Programme Manager produces a quarterly GRC metrics report for the CISO and Chief Risk Officer. The report provides a concise, data-driven view of the health of the GRC programme across all domains.

9.1.2 The quarterly report is used by the CISO and Chief Risk Officer to identify trends, prioritize resources, and escalate material issues to the ERC.

### 9.2 Report contents

Each quarterly report must include the following:

| Section | Content |
| --- | --- |
| Executive summary | 1 to 2 paragraph summary of programme health; material changes since last quarter |
| Domain status table | Per-domain summary (see template in Section 9.3) |
| Open gaps | Count of open control gaps by domain and severity; comparison with prior quarter |
| CAPA status | Open CAPAs, overdue CAPAs, CAPAs closed in the quarter |
| Overdue control tests | List of controls not tested within the required frequency |
| Regulatory change log | New or amended regulations identified in the quarter; affected documents flagged |
| New and updated documents | Documents added or revised in the quarter; version changes noted |

### 9.3 Domain status metrics template

| Domain | Open Gaps | Overdue Tests | CAPA Count | Regulatory Changes | Status |
| --- | --- | --- | --- | --- | --- |
| Governance | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Risk | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Compliance | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Information Security | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Privacy | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| AI Governance | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Resilience | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Supply Chain | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| IT Operations | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |
| Development Security | [n] | [n] | [n] | [n] | Compliant / At Risk / Non-Compliant |

**Status definitions:**
- **Compliant:** No material gaps; all controls tested within cadence; no overdue CAPAs
- **At Risk:** One or more open gaps or overdue tests; CAPAs in progress; no critical non-compliance
- **Non-Compliant:** Critical gap confirmed; regulatory obligation at risk; overdue CAPA unresolved beyond 90 days

---

## 10. Risk treatment status updates

### 10.1 Quarterly risk register review

10.1.1 The risk register is reviewed and updated quarterly by the GRC Programme Manager in conjunction with risk owners across all domains.

10.1.2 Each quarterly review assesses:

- Progress of active risk treatment plans
- Whether the target risk rating has been achieved or the timeline requires adjustment
- Any new or emerging risks identified since the last review
- Risks where the residual risk level has changed materially

### 10.2 Risk owner accountability

10.2.1 Risk owners are responsible for reporting treatment progress to the GRC Programme Manager before each quarterly review.

10.2.2 Where a treatment plan is overdue or the risk owner cannot be identified, the GRC Programme Manager escalates to the Chief Risk Officer.

### 10.3 Residual risk acceptance

10.3.1 Where a risk treatment plan is concluded and a residual risk remains above the organization's risk appetite threshold, the residual risk must be formally accepted in writing by the CIO or above.

10.3.2 Written risk acceptance records are retained as evidence of informed decision-making. They are retained for 7 years and referenced in the risk register.

10.3.3 Residual risks accepted at ERC level are reported in the annual GRC programme report.

---

## 11. ERC governance reporting

### 11.1 Annual GRC programme report

11.1.1 The annual GRC programme report is the primary governance artefact submitted to the ERC. It is submitted by 31 March each year and covers the preceding calendar year.

11.1.2 The report must include the following sections:

| Section | Content |
| --- | --- |
| Executive Summary | Overall programme health assessment; key achievements; material risks or gaps |
| Programme Scorecard | Domain-by-domain status (Compliant / At Risk / Non-Compliant) with trend indicators vs prior year |
| Regulatory Change Log | Regulatory and framework changes in the period; impact on GRC library assessed |
| Open Gaps and CAPA Status | Summary of open control gaps; CAPA progress; overdue items highlighted |
| Material Incidents | Incidents that triggered GRC library reviews or revealed control gaps |
| Upcoming Review Priorities | Documents due for major revision; regulatory changes anticipated; domains requiring resource focus |
| Resource Requirements | Staff, tooling, and budget requirements for the upcoming programme year |

### 11.2 ERC approval

11.2.1 The ERC reviews the annual GRC programme report at its April session and provides one of the following outcomes:

- Approved: report accepted; all proposed changes approved
- Approved with conditions: report accepted subject to specified modifications or additional actions
- Deferred: additional information required; re-submission within 30 days

11.2.2 ERC approval of material policy or framework changes is a prerequisite for publication of those changes in the GRC library.

11.2.3 The GRC Programme Manager records the ERC outcome and publishes approved changes no later than 30 April.

---

## 12. Document retirement and archival

12.1 A document is retired when it is superseded by a new or revised document, when the organizational obligation it addressed no longer exists, or when directed by the ERC.

12.2 Retirement process:

| Step | Action | Responsible Party |
| --- | --- | --- |
| 1 | Mark the document with the `**Status:** Superseded` metadata lifecycle line; record the retirement date and superseding-document reference in the document index register | GRC Programme Manager |
| 2 | Update the superseding document to include a reference to the retired document and retirement date | GRC Programme Manager |
| 3 | Move the retired document to the designated document archive; set access to read-only | GRC Programme Manager |
| 4 | Notify all document owners and domain approvers of the retirement | GRC Programme Manager |
| 5 | Confirm no active compliance obligations reference the retired document; if they do, ensure that the superseding document addresses them | GRC Programme Manager / Domain Approver |

12.3 Physical copies of retired documents, where they exist, must be securely destroyed via cross-cut shredding or equivalent.

12.4 Digital archived records of retired documents must be retained in accordance with the Records Retention and Destruction Standard. Retired documents are not deleted.

12.5 The document index register is the system of record for all active, retired, and archived documents in the GRC library.

---

## 13. Framework alignment

| Framework | Reference | Alignment |
| --- | --- | --- |
| ISO 37301:2021 | §9.1 Monitoring, measurement, analysis, and evaluation | Quarterly metrics reporting, control testing schedule, and attestation requirements |
| ISO 37301:2021 | §9.2 Internal audit | Control testing and gap reporting feeding into programme review |
| ISO 37301:2021 | §9.3 Management review | Annual ERC review and GRC programme report |
| ISO/IEC 27001:2022 | §9.3 Management review | Annual review inputs, outputs, and ERC approval process |
| ISO/IEC 27001:2022 | §10.2 Continual improvement | CAPA process integration; triggered reviews; version control |
| ISO 31000:2018 | §6.6 Monitoring and review | Risk register quarterly review; risk treatment status updates; residual risk acceptance |
| ISO 31000:2018 | §6.5 Risk treatment | Treatment plan tracking and risk owner accountability |
| COBIT 2019 | APO01 Managed IT Management Framework | Programme management governance, roles and responsibilities, document lifecycle |
| COBIT 2019 | APO12 Managed Risk | Risk treatment status updates; ERC reporting; quarterly risk register reviews |
| COBIT 2019 | APO14 Managed Data | Records retention requirements for attestation and deprovisioning evidence |
| NIST CSF 2.0 | GV.OC (Organizational Context) | ERC governance reporting and programme scorecard |
| NIST CSF 2.0 | GV.RM (Risk Management Strategy) | Residual risk acceptance and quarterly risk review |

---

**End of Document**
