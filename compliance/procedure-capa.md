# Corrective and Preventive Action (CAPA) Procedure

**Document Title:** Corrective and Preventive Action (CAPA) Procedure 
**Document Type:** Procedure 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** compliance/standard-internal-audit.md, compliance/procedure-audit-planning.md, compliance/policy-compliance-and-audit-management.md 
**Classification:** Public 
**Category:** Compliance Management 
**Review Frequency:** Annual and upon material audit methodology or regulatory change 
**Repository Path:** compliance/procedure-capa.md 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Governance](#2-governance)
3. [Nonconformity Identification and Recording](#3-nonconformity-identification-and-recording)
4. [Root Cause Analysis Requirements](#4-root-cause-analysis-requirements)
5. [CAPA Classification](#5-capa-classification)
6. [Corrective Action Planning](#6-corrective-action-planning)
7. [Implementation and Verification](#7-implementation-and-verification)
8. [CAPA Register](#8-capa-register)
9. [CAPA Escalation](#9-capa-escalation)
10. [Preventive Action](#10-preventive-action)
11. [Relationship to Continual Improvement](#11-relationship-to-continual-improvement)
12. [Evidence Retention](#12-evidence-retention)
13. [Framework Alignment](#13-framework-alignment)

---

## 1. Purpose and Scope

### 1.1 Purpose

This procedure governs the identification, recording, assessment, treatment, verification, and closure of nonconformities and opportunities for improvement across all GRC domains. It defines the Corrective and Preventive Action (CAPA) process that the organization uses to:

- Systematically address control failures, compliance gaps, and identified weaknesses before they recur or escalate;
- Require root cause analysis for material findings so that actions address underlying causes rather than symptoms;
- Ensure that accountability, target dates, and verification requirements are clearly assigned for every nonconformity;
- Provide senior leadership with a consolidated, reliable view of the organization's nonconformity landscape and remediation status;
- Drive measurable, sustained improvement in the GRC programme over time.

### 1.2 Scope

This procedure applies to nonconformities and improvement opportunities identified through any of the following sources:

| Source | Description |
|--------|-------------|
| Internal audits | Findings from audits conducted under the Internal Audit Standard |
| Supplier / third-party audits | Findings from audits of suppliers, sub-processors, or third-party service providers |
| Security incidents | Control failures or gaps identified during security incident investigation and post-incident review |
| Risk register reviews | Control gaps identified during periodic risk assessment or residual risk reviews |
| Regulatory notifications | Nonconformities identified by regulators, certification bodies, or competent authorities |
| Management reviews | Issues identified during periodic management reviews of the GRC programme |
| Self-assessments | Control gaps identified by domain owners through self-assessment activities |
| Control monitoring failures | Automated or manual monitoring that identifies a control as failed or ineffective |

This procedure applies to all personnel who identify, own, or are involved in resolving nonconformities, and to the GRC Manager and CISO who oversee the CAPA programme.

---

## 2. Governance

### 2.1 CAPA Programme Owner

The **CISO** is the owner of the CAPA programme. The CISO is accountable for:

- Ensuring the CAPA process is applied consistently and completely across all GRC domains;
- Providing programme-level oversight and escalation authority for Critical and High CAPAs;
- Reporting CAPA programme status to the ERC on a quarterly basis;
- Approving decisions to extend target dates for Critical findings.

### 2.2 Domain Owner Responsibilities

Each **domain owner** (e.g., the head of operations, IT manager, privacy officer, or equivalent role responsible for a defined GRC domain) is responsible for:

- Accepting or contesting the classification of findings within their domain;
- Assigning a corrective action owner for each CAPA within their domain;
- Ensuring corrective actions are resourced, planned, and implemented within the agreed target dates;
- Providing evidence of corrective action completion to the GRC Manager for verification;
- Escalating resource constraints or implementation obstacles to the CISO promptly.

### 2.3 GRC Manager Responsibilities

The **GRC Manager** is responsible for:

- Maintaining the CAPA register and ensuring it is accurate and current;
- Assigning CAPA IDs and recording new entries within 2 business days of receiving a finding or nonconformity report;
- Monitoring CAPA status and proactively identifying items at risk of becoming overdue;
- Verifying closure of each CAPA through evidence review before marking it as closed;
- Preparing the quarterly CAPA status report for the ERC;
- Conducting annual pattern analysis of recurring nonconformities.

### 2.4 ERC Reporting

The **Executive Risk Committee (ERC)** receives a quarterly CAPA status report that includes:

- Total number of open CAPAs by classification and domain;
- CAPAs opened and closed in the reporting period;
- Overdue items and escalation status;
- Summary of patterns or systemic issues identified;
- Critical CAPAs: individual status update for each open item.

---

## 3. Nonconformity Identification and Recording

### 3.1 Raising a Nonconformity

Any individual across the organization may raise a nonconformity or improvement opportunity. Nonconformities are raised through the designated CAPA submission mechanism (e.g., a GRC platform, shared register, or submission form). Identifying and raising a potential nonconformity is a positive act and must not carry negative consequences for the person raising it.

### 3.2 Minimum Required Fields

Every nonconformity record must include the following minimum information at the time of submission. The GRC Manager will work with the submitter to complete any missing fields within 2 business days:

| Field | Description |
|-------|-------------|
| Date Identified | The date the nonconformity was first observed or identified |
| Domain | The GRC domain to which the nonconformity relates (see Internal Audit Standard §1.2) |
| Source | The mechanism through which the nonconformity was identified (see Section 1.2 table) |
| Description | A clear, factual statement of what the nonconformity is, including the applicable requirement or criterion it fails to meet |
| Root Cause Category | Preliminary categorization of the likely root cause (e.g., process gap, people/training, technology failure, third-party failure, governance gap): to be refined through root cause analysis |
| Risk Level | Preliminary classification per Section 5; to be confirmed by the GRC Manager and domain owner |
| Owner | The individual responsible for implementing the corrective action |
| Target Date | The date by which corrective action is to be completed, aligned to the classification timelines in Section 5 |

### 3.3 CAPA ID Assignment

The GRC Manager assigns a unique CAPA ID to each record upon entry into the CAPA register. The CAPA ID format is: **CAPA-[YYYY]-[NNN]** (e.g., CAPA-2026-001). The CAPA ID is communicated to the submitter and the domain owner within 2 business days.

---

## 4. Root Cause Analysis Requirements

Effective corrective action requires that the underlying cause of the nonconformity is understood and addressed, not merely the observable symptom. Root cause analysis requirements vary by finding classification.

### 4.1 Critical and High Findings

A **formal root cause analysis** is required for all Critical and High classified nonconformities. The responsible owner, in consultation with relevant subject matter experts, conducts root cause analysis using one of the following methodologies (analyst's choice):

| Methodology | Description |
|-------------|-------------|
| **5-Whys** | Iteratively asks "why" five or more times to trace from the observable symptom back to the root cause. Suited to simpler, linear causal chains. |
| **Ishikawa / Fishbone Diagram** | A structured cause-and-effect diagram that organizes potential causes into categories (e.g., people, process, technology, environment). Suited to multifactorial nonconformities. |
| **Fault Tree Analysis (FTA)** | A top-down, deductive logical model that maps combinations of events or conditions that could produce the failure. Suited to complex technical nonconformities or those with multiple contributing causes. |

The chosen methodology and its outputs must be documented in the CAPA record. The root cause statement must be specific and actionable: it must identify what failed, why it failed, and what condition or absence allowed the failure to go undetected or unresolved.

The root cause analysis for Critical findings must be completed and submitted to the GRC Manager within **5 business days** of CAPA opening. For High findings, within **10 business days**.

### 4.2 Moderate and Low Findings

For Moderate and Low classified nonconformities, a **concise root cause statement** (1 to 3 sentences) is sufficient. The statement must still identify the primary cause and the condition that allowed it to persist. A formal methodology is not required, though teams may use one if it aids analysis.

### 4.3 Root Cause Categories

Root causes are categorized using the following taxonomy to enable pattern analysis:

| Category | Examples |
|----------|---------|
| **Process gap** | No documented procedure; procedure exists but is not followed; process design inadequacy |
| **People / Training** | Lack of awareness; insufficient training; role responsibility ambiguity |
| **Technology** | System misconfiguration; missing technical control; tool limitation or failure |
| **Third-party failure** | Supplier non-performance; vendor control gap; outsourced process failure |
| **Governance gap** | Missing policy; unclear accountability; inadequate oversight or monitoring |
| **Resource constraint** | Insufficient budget, staffing, or time to implement or maintain the control |
| **Change management** | Control degraded by an unmanaged change; change introduced risk not captured in risk assessment |

---

## 5. CAPA Classification

CAPA classification aligns to the finding classification scheme defined in the Internal Audit Standard (compliance/standard-internal-audit.md §7). The classification determines the urgency of response, the notification obligations, and the target closure date.

### 5.1 Critical

**Definition:** A material control failure or nonconformity that exposes the organization to significant risk of harm, regulatory sanction, certification failure, or operational disruption. The control is absent, has failed completely, or is being actively circumvented.

**Response requirements:**

| Requirement | Timeframe |
|-------------|-----------|
| Notification to CISO and CIO | Within **24 hours** of identification |
| Documented remediation plan submitted to GRC Manager | Within **5 business days** of CAPA opening |
| Interim compensating control (if full remediation cannot be achieved within 30 days) | Implemented within **10 business days** |
| Full remediation / closure target | **30 days** |
| Formal root cause analysis completed | Within **5 business days** of CAPA opening |
| Follow-up audit of affected control area | Within **12 months** of CAPA closure |

### 5.2 High

**Definition:** A significant control gap or deficiency that, if not remediated, is likely to increase risk exposure materially or result in a nonconformity at an external audit, regulatory inspection, or certification surveillance assessment.

**Response requirements:**

| Requirement | Timeframe |
|-------------|-----------|
| Notification to CISO (for security/privacy domains) | Within **1 business day** |
| Documented remediation plan submitted to GRC Manager | Within **10 business days** of CAPA opening |
| Full remediation / closure target | **60 days** |
| Formal root cause analysis completed | Within **10 business days** of CAPA opening |

### 5.3 Moderate

**Definition:** A control weakness where the control exists and provides some mitigation but does not fully meet the applicable requirement or operates with less-than-required effectiveness. Remediation reduces residual risk but the gap does not immediately threaten compliance or certification status.

**Response requirements:**

| Requirement | Timeframe |
|-------------|-----------|
| Concise root cause statement | Within **15 business days** of CAPA opening |
| Documented remediation plan | Within **15 business days** of CAPA opening |
| Full remediation / closure target | **90 days** |

### 5.4 Low / Observation

**Definition:** A minor improvement opportunity or observation. The control is broadly effective but could be enhanced. Does not constitute a nonconformity against a defined requirement.

**Response requirements:**

| Requirement | Timeframe |
|-------------|-----------|
| Acknowledgement and proposed action | Within **30 days** of CAPA opening |
| Full remediation / closure target | **180 days** |

---

## 6. Corrective Action Planning

### 6.1 Action Plan Requirements

For each CAPA, the owner develops a documented corrective action plan. The plan must contain:

a. **Specific actions:** A list of discrete, concrete tasks that will address the root cause. Actions must be specific enough that their completion can be objectively verified (i.e., not "improve the process" but "update Procedure X to include step Y, train all relevant staff, and implement automated monitoring control Z").

b. **Owner for each action:** Each individual action within the plan is assigned to a named individual or role. If the overall CAPA owner is not the action implementer, the relationship is documented clearly.

c. **Target date for each action:** Intermediate target dates for each action step, consistent with the overall CAPA closure target date.

d. **Verification method:** A statement of how completion will be verified (e.g., document evidence, test result, training completion report, observation, re-test of the control).

### 6.2 Interim Controls

Where full corrective action cannot be completed within the classification target date (e.g., due to technology procurement lead times or complex process redesign), the owner must:

- Identify and implement interim compensating controls that reduce the risk in the interim period;
- Document the interim controls in the CAPA record;
- Obtain approval from the CISO for any Critical finding where full remediation will extend beyond the 30-day target.

Reliance on interim controls does not close the CAPA. The CAPA remains open until the substantive corrective action is implemented and verified.

### 6.3 Target Date Changes

Target date changes must be approved by:

- **Critical:** CISO approval; notification to ERC;
- **High:** GRC Manager approval; noted in quarterly ERC report;
- **Moderate / Low:** GRC Manager approval; recorded in register.

Target date changes must be accompanied by a documented justification and a new realistic completion date. Repeated extensions are flagged in the pattern analysis (see Section 9.2).

---

## 7. Implementation and Verification

### 7.1 Owner Implementation Responsibilities

The corrective action owner is responsible for:

- Implementing all actions in the corrective action plan by the agreed target dates;
- Collecting and preserving evidence of implementation as actions are completed;
- Proactively communicating progress to the GRC Manager at agreed intervals (at minimum, monthly for Critical and High CAPAs);
- Notifying the GRC Manager promptly if any obstacle is encountered that may cause a target date to be missed.

### 7.2 GRC Manager Verification

The GRC Manager verifies that corrective actions have been implemented and are effective before marking a CAPA as closed. Verification must include:

- Review of evidence provided by the owner (e.g., updated procedure versions, training completion records, configuration change evidence, testing results);
- Comparison against the corrective action plan to confirm all actions have been completed;
- For Critical and High CAPAs: confirmation that the control now operates as intended, not merely that an action was taken.

The GRC Manager documents the verification findings in the CAPA record, including the date of verification and the evidence reviewed.

### 7.3 Re-Audit Trigger

For **Critical and High CAPAs** where the verification review raises doubt about the effectiveness of the corrective action, the GRC Manager may request a targeted re-audit of the affected control. The re-audit is conducted in accordance with the Audit Planning Procedure (compliance/procedure-audit-planning.md) and is scoped specifically to the control or controls addressed by the CAPA.

Re-audit findings are recorded as a new audit engagement in the audit register and any resulting findings generate new CAPA records.

### 7.4 Closure

A CAPA is marked as **Closed** in the register when:

- All corrective actions in the plan have been implemented;
- The GRC Manager has verified implementation and effectiveness;
- Closure evidence is documented and retained in the CAPA record;
- For CAPAs linked to an internal audit finding: the corresponding finding in the audit register is also marked as closed.

CAPAs are not closed until verification is complete. The domain owner's assertion that actions are complete is not sufficient: objective evidence is required.

---

## 8. CAPA Register

### 8.1 Register Structure

The GRC Manager maintains a centralized CAPA register. Each record contains the following fields:

| Field | Description |
|-------|-------------|
| **CAPA ID** | Unique identifier (format: CAPA-[YYYY]-[NNN]) |
| **Date Opened** | Date the nonconformity was entered into the register |
| **Source** | Mechanism of identification (audit, incident, regulatory notification, etc.) |
| **Domain** | GRC domain |
| **Finding Summary** | Concise description of the nonconformity |
| **Root Cause** | Root cause statement or reference to root cause analysis document |
| **Risk Level** | Classification: Critical / High / Moderate / Low |
| **Corrective Action** | Summary of planned corrective actions; reference to full action plan if separate |
| **Owner** | Individual or role responsible for implementation |
| **Target Date** | Agreed closure target date |
| **Status** | Open / In Progress / Pending Verification / Closed |
| **Closure Date** | Date verified as closed; blank if not yet closed |
| **Closure Evidence** | Reference to evidence artefacts reviewed during verification |
| **Verified By** | Name or role of the GRC Manager or reviewer who performed closure verification |

### 8.2 Register Maintenance

The CAPA register is:

- Updated by the GRC Manager within 2 business days of any status change;
- Reviewed in full by the GRC Manager at least monthly to identify items approaching or exceeding target dates;
- Shared with the CISO for review at least monthly;
- Included (in summary form) in the quarterly ERC report.

---

## 9. CAPA Escalation

### 9.1 Overdue Critical and High CAPAs

An item is considered **overdue** when its target date has passed and closure has not been verified. Overdue Critical and High CAPAs are subject to the following escalation chain:

| Threshold | Action |
|-----------|--------|
| Target date reached with no closure | GRC Manager notifies the domain owner and requests updated status and revised target date within 2 business days |
| 5 business days past target date | GRC Manager escalates to the CISO (for security/privacy domains) or relevant domain executive |
| 10 business days past target date | CISO/domain executive escalates to the ERC; item reported as overdue in the next ERC cycle (or immediately for Critical) |
| Repeated extensions or sustained non-closure | Considered a governance risk; ERC determines appropriate response |

Overdue Moderate and Low CAPAs are reported in the quarterly ERC status report but do not follow the above escalation chain unless they have been extended more than twice.

### 9.2 Pattern Analysis

The GRC Manager conducts an **annual pattern analysis** of CAPA data to identify:

- Domains or control areas with recurring nonconformities across multiple audit cycles or sources;
- Root cause categories that appear repeatedly, suggesting systemic programme weaknesses;
- CAPAs that were closed but for which the same or related nonconformity recurred within 12 months of closure ("recurrence");
- Domains with consistently high average closure times.

The pattern analysis is documented as a component of the annual GRC management review input and is used to inform the following year's Annual Audit Plan priorities and GRC programme improvement plan.

---

## 10. Preventive Action

### 10.1 Purpose of Preventive Action

Preventive action addresses potential nonconformities: issues that have not yet occurred but that analysis or intelligence suggests may occur if no action is taken. Effective preventive action reduces the frequency and severity of future nonconformities and supports the organization's shift from reactive to proactive risk management.

### 10.2 Triggers for Preventive Action

Preventive action may be initiated from:

- Threat intelligence that indicates emerging risks to current control designs;
- Near-miss events (an event that had the potential to be a security incident but did not result in harm);
- External audit or regulatory findings at peer organizations in the same sector;
- Significant changes to the organizational environment that may affect control effectiveness before those effects are detected;
- Lessons learned from CAPA pattern analysis showing precursor conditions.

### 10.3 Preventive Action Process

Preventive action items are recorded in the same CAPA register as corrective actions, with the Source field designated as "Preventive Action" and the Description field explaining the potential nonconformity being prevented. The same classification, action planning, ownership, and verification process applies.

Preventive action items are classified based on the potential severity of the nonconformity they are intended to prevent, using the same Critical / High / Moderate / Low scheme. Target dates reflect the urgency of implementing the preventive control before the potential nonconformity materializes.

---

## 11. Relationship to Continual Improvement

### 11.1 CAPA as an Improvement Driver

The CAPA programme is a primary mechanism for continual improvement of the GRC programme. Individual CAPAs address specific nonconformities; the aggregate of CAPA activity provides evidence of the programme's improvement trajectory over time.

### 11.2 Annual Management Review Input

CAPA programme data forms a mandatory input to the annual GRC management review. The input package includes:

- Total CAPA volume by classification, domain, and source for the year;
- Average time to closure by classification;
- Recurrence rate (CAPAs where the same or closely related nonconformity recurred within 12 months);
- Overdue CAPA analysis;
- Key themes from root cause analysis, with recommendations for structural programme improvements;
- Preventive actions initiated and their outcomes.

### 11.3 GRC Programme Improvement Plan

Systemic or structural issues identified through CAPA pattern analysis are incorporated into the GRC programme improvement plan. The improvement plan is owned by the CISO and reviewed by the ERC annually. Improvements driven by CAPA outcomes are tracked as a specific category within the improvement plan to demonstrate the value of the CAPA process.

---

## 12. Evidence Retention

All CAPA records, including root cause analysis documentation, corrective action plans, implementation evidence, and closure verification records, must be retained for a minimum of **7 years** from the CAPA closure date.

For CAPAs that remain open at the time of any regulatory inspection, certification audit, or legal proceeding, records must be preserved until the relevant matter is fully resolved, regardless of the standard 7-year retention period.

Records are stored in the designated secure GRC document repository. Access is restricted to the GRC team, CISO, domain owners with records in scope, and authorized senior leadership. Disposal after the retention period is conducted in accordance with the organization's data retention and disposal policy.

---

## 13. Framework Alignment

| Framework / Standard | Relevant Clause or Section | Mapping |
|----------------------|---------------------------|---------|
| ISO 9001:2015 | §10.2 Nonconformity and corrective action; §10.3 Continual improvement | Primary source for corrective and preventive action requirements; this procedure operationalizes these clauses |
| ISO/IEC 27001:2022 | §10.1 Continual improvement; §10.2 Nonconformity and corrective action | ISMS-specific requirements for nonconformity treatment and improvement |
| COBIT 2025 | MEA02 (Managed Assurance) | Assurance-linked corrective action and monitoring requirements |
| CSA Cloud Controls Matrix | A&A-06 (Audit and Assurance: Remediation) | Requirements for tracking and remediating audit findings |
| BASC Standard | §10 Improvement | Corrective action and improvement requirements within the BASC management system |
| NIST Cybersecurity Framework 2.0 | RC.IM (Recovery: Improvements) | Incorporating lessons learned into recovery strategy and GRC programme improvement |

---

**End of Document**
