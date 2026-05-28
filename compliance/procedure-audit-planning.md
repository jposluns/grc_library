# Audit Planning Procedure

**Document Title:** Audit Planning Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Audit Executive 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`compliance/procedure-capa.md`](procedure-capa.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md) 
**Classification:** Public 
**Category:** Compliance Management 
**Review Frequency:** Annual and upon material audit methodology or regulatory change 
**Repository Path:** [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Table of contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Governance](#2-governance)
3. [Annual Audit Plan Development](#3-annual-audit-plan-development)
4. [Individual Audit Planning Steps](#4-individual-audit-planning-steps)
5. [Audit Programme Template](#5-audit-programme-template)
6. [Audit Evidence Collection and Documentation](#6-audit-evidence-collection-and-documentation)
7. [Communication During the Audit](#7-communication-during-the-audit)
8. [Post-Fieldwork Reporting](#8-post-fieldwork-reporting)
9. [Escalation](#9-escalation)
10. [Audit Register and Evidence Retention](#10-audit-register-and-evidence-retention)
11. [Framework Alignment](#11-framework-alignment)

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure operationalizes the Internal Audit Standard (compliance/standard-internal-audit.md) by defining the specific steps, responsibilities, templates, and timelines required to plan, prepare, execute, and report on individual internal audits and the overall annual audit programme.

It provides practical guidance to the GRC Manager, audit team members, and auditees on what to do at each stage of the audit lifecycle, ensuring consistency, completeness, and alignment with ISO 19011:2018 §6.2 to 6.4.

### 1.2 Scope

This procedure applies to all internal audits conducted under the GRC programme, across all domains defined in the Internal Audit Standard. It applies to:

- GRC Managers and Chief Audit Executives responsible for audit programme management;
- Lead auditors and audit team members responsible for individual audit engagements;
- Domain owners and process owners acting as auditees;
- Any external auditors or peer reviewers engaged to supplement the internal audit function.

This procedure does not govern external certification audits or regulatory inspections, though its principles and templates may be adapted for readiness reviews conducted in preparation for such events.

---

## 2. Governance

### 2.1 Audit programme responsibility

The **GRC Manager / Chief Audit Executive (CAE)** is accountable for:

- Developing, maintaining, and executing the Annual Audit Plan;
- Assigning audit team members to individual engagements;
- Verifying auditor independence before each engagement;
- Reviewing and approving final audit reports before distribution;
- Maintaining the audit register and reporting programme status to the ERC.

### 2.2 Audit team composition

For each individual audit, the CAE/GRC Manager appoints:

| Role | Responsibilities |
|------|-----------------|
| **Lead Auditor** | Responsible for planning, managing, and reporting the audit; the primary point of contact with the auditee |
| **Audit Team Member(s)** | Conduct evidence collection, technical testing, and document review under the direction of the lead auditor |
| **Technical Specialist (if required)** | Provides domain-specific expertise for technical security audits or AI system audits; may be an internal subject matter expert or an engaged external specialist |
| **Observer (if applicable)** | May accompany the audit team for training or quality assurance purposes; does not participate in evidence collection or finding determination |

Minimum team size: one lead auditor. For Critical-scope or cross-domain audits, a minimum of two team members is recommended to support evidence corroboration.

### 2.3 Auditor independence verification

Before commencing each audit engagement, the CAE/GRC Manager must confirm that each assigned auditor:

- Does not hold direct operational responsibility for any area, process, or control within the audit scope;
- Has disclosed any personal relationships with auditee staff that could reasonably affect objectivity;
- Has no financial or other interest in the outcome of the audit.

Independence verification is documented in the audit planning record for each engagement. Where a conflict is identified, the auditor is reassigned or the audit is supplemented with an independent reviewer.

---

## 3. Annual audit plan development

### 3.1 Risk-based prioritization

The Annual Audit Plan is developed using a risk-based approach. The CAE/GRC Manager, in collaboration with the CISO and domain owners, assesses:

a. **Enterprise Risk Register linkage:** Domains and processes associated with high-rated or critical risks in the Enterprise Risk Register are prioritized for more frequent audit coverage. The risk rating used is the current residual risk score, not the inherent risk.

b. **Historical finding severity:** Domains that produced Critical or High findings in the preceding audit cycle are scheduled for re-audit in the following year, regardless of their current risk rating.

c. **Control maturity:** Domains where control maturity assessments indicate a lower maturity level receive higher audit priority.

d. **Significant changes:** Domains that have undergone material changes (new systems, process redesign, personnel changes in key control roles, outsourcing) since the last audit are prioritized.

e. **Time since last audit:** No domain may remain unaudited for more than three consecutive years. As domains approach this threshold, they are elevated in scheduling priority.

### 3.2 Regulatory and certification triggers

The following certification and regulatory requirements mandate minimum audit frequencies that must be reflected in the Annual Audit Plan regardless of risk-based prioritization:

| Certification / Requirement | Minimum Internal Audit Frequency | Domains / Scope Items |
|-----------------------------|-----------------------------------|-----------------------|
| BASC Certification | Annual | BASC programme scope |
| AEO-S (Authorized Economic Operator to Security) | Annual | AEO-S IT control scope |
| ISO/IEC 27001 ISMS | Annual | ISMS scope |
| SOC 2 Type II | Annual | SOC 2 Trust Services Criteria scope |

Additional regulatory requirements applicable to the organisation's jurisdictions of operation are identified in the Regulatory Applicability Register and must be reviewed during Annual Audit Plan development.

### 3.3 ERC approval

The draft Annual Audit Plan is submitted to the **Executive Risk Committee (ERC) for approval no later than 31 January** of the year to which it applies.

The submission package includes:

- Draft Annual Audit Plan table (see Section 3.4 for required contents);
- Summary of the risk-based prioritization methodology applied;
- Proposed audit resource allocation and estimated effort;
- Identification of any domains that will not receive full audit coverage in the current year with documented rationale;
- Any proposed use of external auditors or technical specialists.

The ERC may approve, modify, or direct additional coverage. Approved modifications are incorporated into the final Annual Audit Plan, which is distributed to the CISO, domain owners, and relevant senior leadership.

### 3.4 Annual audit plan contents

The Annual Audit Plan is maintained as a structured document or register containing, for each planned audit engagement:

| Field | Description |
|-------|-------------|
| Audit ID | Unique identifier for the engagement |
| Domain | GRC domain(s) in scope |
| Audit Type | Compliance / Control Effectiveness / Technical Security / Third-Party / AI System |
| Scope Summary | Brief description of the processes, controls, or systems to be audited |
| Planned Start Date | Target date for fieldwork commencement |
| Planned Completion Date | Target date for final report issuance |
| Lead Auditor | Name or role of assigned lead auditor |
| Trigger / Rationale | Reason for scheduling (e.g., risk rating, certification requirement, prior finding, three-year coverage) |
| Status | Planned / In Progress / Completed / Deferred |

### 3.5 Mid-year review

The CAE/GRC Manager reviews and updates the Annual Audit Plan at mid-year (no later than 31 July). The mid-year review considers:

- Changes in organisational risk profile;
- Material incidents or control failures that may trigger unplanned audits;
- Significant regulatory or framework changes;
- Resource constraints that may affect delivery.

Material changes to the plan resulting from the mid-year review are reported to the ERC at the next scheduled reporting cycle.

---

## 4. Individual audit planning steps

### 4.1 Define audit scope and objectives

The lead auditor, in consultation with the CAE/GRC Manager and the auditee, formally defines:

- **Audit objectives:** What the audit is intended to determine (e.g., "Determine whether access control procedures for privileged accounts conform to the Access Control Standard and are operating effectively");
- **Audit scope:** The specific processes, systems, organisational units, locations, and time period to be covered;
- **Audit criteria:** The policies, standards, procedures, legal requirements, and contractual obligations against which the audit will be assessed;
- **Audit boundaries:** Explicit statement of what is out of scope, to avoid scope creep and auditee confusion.

The scope and objectives are documented in the audit planning record and shared with the auditee at the time of formal notification.

### 4.2 Identify audit criteria

The lead auditor compiles a comprehensive list of audit criteria applicable to the scope. Criteria sources include:

- Internal policies, standards, and procedures relevant to the domain;
- Applicable legislation and regulation (identified via the Regulatory Applicability Register);
- Certification requirements (e.g., BASC standard clauses, ISO/IEC 27001 controls, SOC 2 criteria);
- Contractual obligations with customers or suppliers, where the audit scope includes supplier management or customer commitment verification;
- Prior audit findings and accepted management responses, to verify that agreed actions have been implemented.

Audit criteria are documented in the audit programme (see Section 5) with a reference to the source document.

### 4.3 Resource and assign audit team

The CAE/GRC Manager:

a. Reviews the scope and estimates the effort required for planning, fieldwork, and reporting;

b. Assigns a lead auditor and, where scope or complexity warrants, one or more audit team members;

c. Verifies auditor independence as described in Section 2.3;

d. Where specialist technical knowledge is required (e.g., for a technical security audit or AI system audit), identifies and engages a technical specialist. The specialist's role and any limitations on their access to audit conclusions are documented in the planning record;

e. Confirms team member availability and books required time in advance of the planned audit dates.

### 4.4 Notify auditees

The lead auditor issues formal written notification to the auditee(s) **at least 10 business days before the planned start of fieldwork**. The notification includes:

- Audit scope and objectives;
- Audit criteria (or reference to where they can be accessed);
- Proposed fieldwork dates and expected duration;
- Identification of the lead auditor and audit team members;
- List of documentation requested in advance (pre-audit documentation package);
- Proposed date and format for the opening meeting;
- Contact details for questions or scheduling coordination.

For unplanned audits triggered by a material incident or control failure, the 10-business-day notification period may be reduced with the approval of the CAE/GRC Manager and notification to the ERC.

### 4.5 Request and review pre-audit documentation package

The lead auditor requests a pre-audit documentation package from the auditee. This package typically includes:

- Current versions of relevant policies, procedures, and standards;
- Evidence of the most recent management review or risk assessment for the domain;
- Previous audit reports and open finding trackers for the domain;
- Relevant records demonstrating control operation (e.g., access review logs, training completion records, change management records);
- Organisational charts and role descriptions for key personnel in scope.

The lead auditor reviews the pre-audit documentation package to:

- Identify gaps or inconsistencies that warrant focused attention during fieldwork;
- Update the audit programme to reflect findings from document review;
- Confirm the accuracy of scope boundaries.

Pre-audit review findings are documented in the audit working papers.

### 4.6 Develop audit programme

The lead auditor develops the detailed **audit programme** before fieldwork commences. The audit programme:

- Lists each control or requirement to be tested, cross-referenced to the audit criterion;
- Defines the evidence types and collection methods to be used for each control;
- Specifies the sampling methodology (see Section 6.2);
- Identifies the auditee staff to be interviewed and the topics to be covered;
- Includes an evidence checklist to track collection status during fieldwork;
- Assigns audit team members to specific programme items.

The audit programme is reviewed and approved by the CAE/GRC Manager before fieldwork commences. Refer to Section 5 for the standard audit programme template.

---

## 5. Audit programme template

The following table structure is used as the standard audit programme for each individual audit engagement. It is maintained as a working document updated throughout fieldwork.

| # | Control / Requirement | Audit Criterion | Evidence Type | Sampling Method | Evidence Ref | Status | Notes |
|---|-----------------------|-----------------|---------------|-----------------|--------------|--------|-------|
| 1 | [Description of control or requirement under review] | [Policy/standard clause, regulatory article, or certification criterion] | [Interview / Document Review / Observation / Technical Testing] | [Full population / Random sample (n=X) / Risk-based selection / Haphazard] | [Reference to working paper or evidence artefact] | [Not Started / In Progress / Complete / Finding Raised] | [Observations, anomalies, or context] |
| 2 | | | | | | | |
| ... | | | | | | | |

**Status key:**
- **Not Started:** Programme item has not yet been addressed
- **In Progress:** Evidence collection commenced but not complete
- **Complete:** Sufficient evidence collected; no finding
- **Finding Raised:** Evidence indicates a nonconformity or gap; finding documented

---

## 6. Audit evidence collection and documentation

### 6.1 Evidence collection principles

All evidence collection must adhere to the requirements defined in the Internal Audit Standard §8. During fieldwork, the lead auditor ensures that:

- Evidence is collected systematically against the audit programme;
- Each piece of evidence is recorded promptly in the audit working papers;
- The collection method, date, and responsible auditor are noted for each item;
- Evidence is stored securely and access is restricted to the audit team and authorized reviewers.

### 6.2 Sampling methodology

Where it is not practicable to test the full population of transactions, records, or events, the auditor applies a defined sampling methodology. The methodology used must be documented in the audit programme. Acceptable methods include:

| Method | When to Use |
|--------|-------------|
| **Full population** | When the population is small (typically fewer than 25 items) or where risk warrants 100% coverage |
| **Random sample** | When the population is large and homogeneous; sample size is documented with rationale |
| **Risk-based selection** | When specific items within the population carry higher risk (e.g., privileged accounts, high-value transactions) |
| **Haphazard selection** | Supplementary method only; not to be used as the primary sampling method for Critical or High risk areas |

The lead auditor documents the sample size, selection rationale, and any limitations on the conclusions that can be drawn from the sample.

### 6.3 Working paper standards

Audit working papers must:

- Be titled and cross-referenced to the relevant audit programme item;
- Record the evidence reference, collection date, and collector;
- Include a brief narrative describing what was reviewed and what it demonstrated;
- Be completed contemporaneously: not reconstructed after fieldwork;
- Be stored in the designated audit evidence repository before the draft findings are issued.

---

## 7. Communication during the audit

### 7.1 Opening meeting

An opening meeting is held at the commencement of fieldwork. Agenda items include:

1. Introduction of the audit team and auditee representatives;
2. Confirmation of audit scope, objectives, and criteria;
3. Review of the proposed fieldwork schedule and access requirements;
4. Explanation of evidence collection methods;
5. Explanation of the finding classification scheme;
6. Logistics (workspace, system access, point of contact for day-to-day queries);
7. Questions from the auditee.

The lead auditor records attendance and key decisions from the opening meeting in the audit working papers.

### 7.2 Fieldwork communications

During fieldwork, the lead auditor:

- Maintains regular communication with the auditee contact to coordinate access and resolve queries promptly;
- Notifies the auditee immediately if fieldwork uncovers a potential Critical finding, so that the auditee is not blindsided at the closing meeting;
- Escalates to the CAE/GRC Manager if access is obstructed or cooperation is insufficient;
- Documents all material communications in the working papers.

### 7.3 Closing meeting

A closing meeting is held at the conclusion of fieldwork, before draft findings are issued. The closing meeting:

- Presents a verbal summary of preliminary findings to the auditee;
- Allows the auditee to raise factual corrections at the earliest opportunity;
- Confirms the timeline for draft findings, management response, and final report;
- Does not constitute a formal presentation of final conclusions: findings remain draft until management responses are received.

---

## 8. Post-fieldwork reporting

### 8.1 Draft report timeline

The lead auditor issues draft audit findings to the auditee within **10 business days** of the completion of fieldwork. The draft includes:

- All findings identified during the audit, classified per the Internal Audit Standard §7;
- Supporting evidence references for each finding;
- Recommended corrective actions;
- A clear statement that findings are in draft pending management response.

### 8.2 Management response window

The auditee has **5 business days** from receipt of draft findings to provide:

- Acknowledgement of each finding;
- A proposed corrective action with an assigned owner and target completion date; or
- A factual dispute (supported by evidence) for the lead auditor's consideration.

If the auditee requires additional time, an extension of up to 3 business days may be granted by the lead auditor with documented justification. Extensions beyond 8 total business days require CAE/GRC Manager approval.

Where a management response is not received within the response window, the lead auditor proceeds to final report with a notation that no management response was provided.

### 8.3 Final report issuance

The lead auditor prepares and the CAE/GRC Manager reviews and approves the final audit report. The report is issued within **10 business days of fieldwork completion** (this target is inclusive of the management response window, meaning the lead auditor must issue the draft promptly to allow time for responses).

Where the management response window causes the 10-business-day target to be infeasible, the CAE/GRC Manager may extend the target to 15 business days, documented with rationale.

**Final report distribution:**

| Recipient | Reason |
|-----------|--------|
| Auditee and domain owner | Primary stakeholders with remediation responsibility |
| CAE / GRC Manager | Programme oversight and register update |
| CISO | For audits covering security or privacy domains |
| ERC | Summary included in next quarterly reporting cycle; full report for Critical findings immediately |

### 8.4 Audit register update

Upon final report issuance, the CAE/GRC Manager updates the audit register with:

- Final finding count by classification;
- Management response summary;
- CAPA IDs for Critical and High findings;
- Agreed remediation target dates;
- Status set to "Report Issued / Tracking Remediation".

---

## 9. Escalation

### 9.1 Critical finding escalation

When a Critical finding is identified during fieldwork:

1. The lead auditor notifies the CAE/GRC Manager immediately, on the same business day;
2. The CAE/GRC Manager notifies the **CISO and CIO verbally or in writing on the same day**;
3. A written summary (may be brief and preliminary) is provided to the CISO and CIO within **1 business day**;
4. A formal escalation report is submitted to the **ERC within 2 business days**, whether or not the annual ERC reporting cycle is due.

The escalation report includes: finding description, domain, risk assessment, immediate actions taken or recommended, and proposed remediation approach.

### 9.2 Obstructed access

If the audit team encounters material obstruction to access (e.g., refusal to provide documentation, unavailability of key personnel beyond reasonable rescheduling), the lead auditor:

1. Documents the obstruction in writing;
2. Escalates to the CAE/GRC Manager within 1 business day;
3. The CAE/GRC Manager escalates to the CISO or relevant domain executive if access is not restored within 2 business days;
4. If access remains obstructed, the audit report notes the limitation and the CAE/GRC Manager reports the situation to the ERC.

### 9.3 Overdue remediation

Overdue remediation tracking is maintained in the audit register. Items that are overdue against their agreed target date are:

- Reported to the domain owner and their direct supervisor;
- Escalated to the CISO (for security/privacy domains) or equivalent senior role for other domains if not resolved within 10 business days of the target date;
- Reported to the ERC as overdue items in the quarterly audit status report.

---

## 10. Audit register and evidence retention

### 10.1 Audit register

The CAE/GRC Manager maintains a centralized audit register covering all planned and completed audit engagements. The register includes, for each engagement:

| Field | Description |
|-------|-------------|
| Audit ID | Unique identifier |
| Audit Type | Compliance / Control Effectiveness / Technical Security / Third-Party / AI System |
| Domain | GRC domain(s) covered |
| Scope Summary | Brief description |
| Lead Auditor | Name or role |
| Fieldwork Dates | Actual start and end dates |
| Report Date | Date of final report issuance |
| Finding Count | Number by classification (Critical / High / Moderate / Low) |
| CAPA IDs | References to generated CAPA records |
| Remediation Status | Summary status of open findings |
| Closure Date | Date all findings marked as closed |

The audit register is reviewed at each ERC reporting cycle.

### 10.2 Evidence retention

All audit working papers, evidence artefacts, draft findings, management responses, and final reports must be retained for a minimum of **7 years** from the date of the final report.

Retention applies regardless of whether the audit produced findings. Working papers for audits with no findings are retained for the same period.

Evidence is stored in the designated secure audit evidence repository. Access is restricted to the audit team, CAE/GRC Manager, and authorized senior leadership. Access by external parties (e.g., regulatory inspectors, certification body auditors) requires approval from the CAE/GRC Manager and, where sensitive, the CISO.

After the 7-year retention period, records are disposed of in accordance with the organisation's data retention and disposal policy.

---

## 11. Framework alignment

| Framework / Standard | Relevant Clause or Section | Mapping |
|----------------------|---------------------------|---------|
| ISO 19011:2018 | §6.2 Establishing the audit programme; §6.3 Managing the audit programme; §6.4 Maintaining and improving the audit programme | Primary procedural reference; this procedure operationalizes these clauses |
| ISO 19011:2018 | §6.5.2 Initiating the audit; §6.5.3 Preparing audit activities | Individual audit planning steps (Sections 4 and 5) |
| ISO/IEC 27001:2022 | §9.2 Internal Audit | Annual programme and individual audit requirements |
| COBIT 2019 | MEA02 (Managed Assurance) | Audit programme planning, resource allocation, and assurance reporting |
| BASC Standard | §9.2 Internal Audit | Annual audit of BASC programme scope; evidence collection and reporting requirements |
| AEO-S IT Control Requirements | IT control testing and documentation | Third-party and technical security audit procedures applicable to AEO-S scope |

---

**End of Document**
