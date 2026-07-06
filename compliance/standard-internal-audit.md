# Internal Audit Standard

**Document Title:** Internal Audit Standard\
**Document Type:** Standard\
**Version:** 1.1.0\
**Date:** 2026-07-06\
**Owner:** Chief Audit Executive\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md), [`compliance/procedure-capa.md`](procedure-capa.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/template-audit-evidence-package.md`](template-audit-evidence-package.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material audit methodology or regulatory change\
**Repository Path:** [`compliance/standard-internal-audit.md`](standard-internal-audit.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Table of contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Governance](#2-governance)
3. [Audit Principles](#3-audit-principles)
4. [Audit Programme Management](#4-audit-programme-management)
5. [Audit Types](#5-audit-types)
6. [Audit Lifecycle](#6-audit-lifecycle)
7. [Finding Classification](#7-finding-classification)
8. [Audit Evidence Requirements](#8-audit-evidence-requirements)
9. [Auditor Competency Requirements](#9-auditor-competency-requirements)
10. [Relationship to CAPA Procedure](#10-relationship-to-capa-procedure)
11. [Framework Alignment](#11-framework-alignment)

---

## 1. Purpose and scope

### 1.1 Purpose

This standard establishes the requirements, principles, and operational framework governing the internal audit function within the GRC programme. It defines how internal audits are planned, conducted, reported, and followed up to provide objective assurance that controls are designed appropriately and are operating effectively.

Internal audits serve as a primary mechanism for:

- Providing independent assurance to senior leadership and the Enterprise Risk Committee (ERC) that material risks are being managed within tolerance;
- Identifying control gaps and nonconformities before they result in incidents, regulatory findings, or certification failures;
- Driving continuous improvement across the GRC programme;
- Supporting readiness for external audits, regulatory inspections, and certification surveillance assessments.

### 1.2 Scope

This standard applies to all internal audit activity conducted across the following GRC domains:

| Domain | Description |
|--------|-------------|
| Information Security | Controls protecting the confidentiality, integrity, and availability of information assets |
| Privacy | Data protection obligations, privacy-by-design, and data subject rights management |
| Risk Management | Enterprise risk identification, assessment, treatment, and monitoring processes |
| Operations | Operational controls, business process integrity, and continuity arrangements |
| Artificial Intelligence | Governance, transparency, accountability, and bias controls for AI/ML systems |
| Supply Chain Security | Third-party risk management, supplier controls, and vendor assurance |
| Regulatory Compliance | Adherence to applicable legal, regulatory, and contractual requirements |
| Organizational Resilience | Business continuity, disaster recovery, and crisis management capabilities |
| Development Security | Secure development lifecycle, code quality, and DevSecOps control effectiveness |

This standard applies to all personnel who plan, conduct, manage, or are subject to internal audits.

---

## 2. Governance

### 2.1 Audit function ownership

The **Chief Audit Executive (CAE)**, or where a dedicated CAE role does not exist, the **GRC Manager**, holds primary accountability for the internal audit function. Responsibilities include:

- Maintaining and updating this standard;
- Developing and obtaining approval for the Annual Audit Plan;
- Ensuring adequate audit resources, competency, and independence;
- Reporting audit programme status, key findings, and trend analysis to the ERC on at least a quarterly basis;
- Coordinating with the CISO on security and privacy audit activity.

### 2.2 CISO responsibilities

The **Chief Information Security Officer (CISO)** is responsible for:

- Ensuring that security and privacy audit findings are treated as priorities and resourced appropriately;
- Receiving immediate notification of Critical findings;
- Reviewing and accepting or challenging audit findings that fall within the information security and privacy domains;
- Sponsoring remediation plans for Critical and High findings within those domains.

### 2.3 Independence requirements

The internal audit function must operate with sufficient independence to provide objective assurance. The following requirements apply:

a. **Auditor independence:** An auditor must not conduct an audit of any area, process, or control for which they hold direct operational responsibility. This applies regardless of seniority or role title.

b. **Structural independence:** The CAE/GRC Manager must have a reporting line that permits direct escalation to the ERC without obstruction by the areas being audited.

c. **Conflict disclosure:** Any auditor who identifies a potential conflict of interest must disclose it to the CAE/GRC Manager before fieldwork commences. The CAE/GRC Manager will reassign the engagement if a material conflict exists.

d. **External support:** Where internal independence cannot be achieved for a particular domain (e.g., where the audit team is small), the organization may supplement the internal audit function with qualified external auditors or peer reviewers to maintain objectivity.

---

## 3. Audit principles

The internal audit function operates in accordance with the following principles, derived from ISO 19011:2018 §4:

| Principle | Description |
|-----------|-------------|
| **Integrity** | Auditors conduct their work honestly, diligently, and responsibly. Audit conclusions are not influenced by personal relationships, organizational pressures, or anticipated outcomes. |
| **Fair Presentation** | Audit findings, conclusions, and reports accurately and truthfully reflect the evidence gathered. Significant obstacles encountered during the audit and unresolved divergences of opinion between auditors and auditees are reported. |
| **Due Professional Care** | Auditors exercise the level of care, judgement, and skill expected of a competent audit professional, commensurate with the complexity and risk of the audit. |
| **Confidentiality** | Audit evidence, working papers, and findings are handled with discretion and are not disclosed to parties outside the defined distribution list without authorization. |
| **Independence** | Auditors are free from bias and conflicts of interest to the greatest extent practicable. Independence underpins the objectivity and credibility of audit conclusions. |
| **Evidence-Based Approach** | Audit conclusions are grounded in verifiable, reproducible evidence. Findings are not made on the basis of assumption or hearsay. |
| **Risk-Based Approach** | Audit resources are directed towards the highest-risk domains, processes, and controls. The audit programme is adapted dynamically as the risk profile of the organization changes. |
| **Continual Improvement** | The audit programme itself is subject to periodic evaluation and improvement. Lessons learned from completed audits are applied to future audit cycles. |

---

## 4. Audit programme management

### 4.1 Annual audit plan

The CAE/GRC Manager develops an **Annual Audit Plan** each year. The plan must:

- Be risk-prioritized, drawing on the Enterprise Risk Register and control assessment data;
- Provide coverage across all in-scope GRC domains, with higher-risk domains scheduled for more frequent review;
- Be reviewed and approved by the **ERC no later than 31 January** of the year to which it applies;
- Be made available to the CISO, domain owners, and relevant senior leadership;
- Be reviewed at mid-year and updated to reflect changes in organizational risk, incidents, or regulatory changes.

### 4.2 Three-year rolling coverage

The audit programme must achieve complete coverage of all in-scope GRC domains across a rolling three-year cycle. No domain may remain unaudited for more than three consecutive years. Higher-risk domains should be audited annually or more frequently as risk dictates.

### 4.3 Risk-based scheduling

Scheduling priority is determined by:

1. Inherent and residual risk levels from the Enterprise Risk Register;
2. History of prior findings (domains with Critical or High findings are re-audited within 12 months);
3. Regulatory, certification, and contractual requirements that mandate audit frequency;
4. Time elapsed since the last audit of the domain;
5. Significant changes to the domain, systems, or operating environment since the last audit.

### 4.4 Triggers for unplanned audits

The following events may trigger an unplanned audit outside the Annual Audit Plan schedule:

| Trigger | Response |
|---------|----------|
| Material security incident or data breach | Targeted audit of affected controls and processes within 30 days of incident closure |
| Significant control failure identified through monitoring | Immediate focused audit of the control and related compensating controls |
| Material regulatory change or new certification requirement | Audit of impacted controls and processes before the effective date of the change |
| ERC or CISO direction | Audit initiated within the timeframe specified by the directing body |
| Significant organizational change (e.g., merger, acquisition, outsourcing) | Audit of affected domains within 60 days |

Unplanned audits are incorporated into the audit register and reported to the ERC at the next scheduled reporting cycle.

---

## 5. Audit types

The internal audit function recognizes the following audit types:

### 5.1 Compliance audit

Assesses whether organizational practices conform to applicable policies, standards, procedures, legal requirements, and contractual obligations. Compliance audits are typically used to verify adherence to certification requirements (e.g., supply chain security standards, information security management systems) and regulatory mandates.

### 5.2 Control effectiveness audit

Evaluates whether controls are not only designed appropriately to address the risks they are intended to mitigate, but are also operating effectively in practice. This type of audit goes beyond confirming the existence of a control to assessing whether it achieves its intended outcome.

### 5.3 Technical security audit

Examines the technical implementation of security controls across infrastructure, applications, networks, and platforms. May include configuration review, vulnerability assessment review, access control testing, logging and monitoring validation, and secure configuration benchmarking. Technical security audits are typically conducted by auditors with specialist technical competency or with the assistance of technical subject matter experts.

### 5.4 Third-party / supplier audit

Assesses the security, privacy, and compliance posture of suppliers or third parties that process, store, or transmit organizational data, or that provide services material to the organization's operations or certification requirements. May be conducted as a document review, questionnaire-based assessment, or on-site audit depending on risk classification and contractual rights.

### 5.5 AI system audit

Examines the governance, transparency, accountability, and risk management controls applied to artificial intelligence and machine learning systems in use across the organization. Specific areas of focus include: data quality and provenance, model bias and fairness assessment, explainability and output review mechanisms, human oversight controls, change management for model updates, and alignment with applicable AI governance frameworks and regulations.

---

## 6. Audit lifecycle

All internal audits follow the lifecycle defined in this section. Deviations from this lifecycle must be documented and approved by the CAE/GRC Manager.

### 6.1 Planning

The CAE/GRC Manager, in consultation with relevant domain owners, defines:

- Audit objectives and scope;
- Audit type and applicable criteria (policies, standards, regulatory requirements);
- Audit team composition and independence verification;
- Planned dates and resource allocation;
- High-level risks or areas of focus to inform the audit approach.

Refer to the Audit Planning Procedure (compliance/procedure-audit-planning.md) for detailed planning requirements.

### 6.2 Preparation

The lead auditor:

- Develops the detailed audit programme, including sampling methodology, evidence checklist, and interview schedule;
- Requests and reviews pre-audit documentation from the auditee;
- Notifies the auditee of the audit at least **10 business days** before the commencement of fieldwork;
- Identifies and documents any preliminary findings or areas of concern from document review.

### 6.3 Opening meeting

An opening meeting is held between the audit team and relevant auditees before fieldwork begins. The opening meeting:

- Confirms the audit scope, objectives, and timetable;
- Introduces the audit team and confirms the auditee contacts;
- Explains the evidence collection methods to be used;
- Clarifies expectations for availability and cooperation;
- Addresses any questions from the auditee.

### 6.4 Evidence collection

The audit team collects evidence in accordance with the audit programme. Evidence collection methods include:

- **Interviews:** Structured discussions with process owners, system administrators, and subject matter experts;
- **Document Review:** Examination of policies, procedures, records, logs, reports, and other documentation;
- **Observation:** Direct observation of processes, practices, and controls in operation;
- **Technical Testing:** Inspection of system configurations, access control lists, audit logs, security baselines, and similar technical artefacts.

All evidence is documented in audit working papers, cross-referenced to the relevant audit criterion, and retained in accordance with §8.

### 6.5 Analysis

The audit team analyzes collected evidence against the audit criteria to:

- Identify conformities and nonconformities;
- Assess the design adequacy and operational effectiveness of controls;
- Evaluate the materiality and risk implications of identified gaps;
- Identify patterns or systemic issues across multiple control areas.

### 6.6 Draft findings

The lead auditor prepares draft audit findings. Each finding includes:

- A unique finding reference;
- Domain and control area;
- Finding title and description;
- Classification (Critical / High / Moderate / Low / Observation);
- Supporting evidence references;
- Risk and potential impact statement;
- Recommended corrective action.

Draft findings are reviewed by the audit team for consistency and accuracy before sharing with the auditee.

### 6.7 Management response

Draft findings are shared with the auditee for factual accuracy review and management response. Auditees have **5 business days** to:

- Accept the finding and provide a proposed remediation plan with target date; or
- Dispute factual inaccuracies (substantiated by evidence) for consideration by the lead auditor.

Where a dispute cannot be resolved, the finding is reported in the final report with both the auditor's position and the auditee's response documented.

### 6.8 Final report

The lead auditor issues the final audit report within **10 business days** of fieldwork completion. Where the management-response window makes the 10-business-day target infeasible, the CAE/GRC Manager may extend it to **15 business days** with documented rationale (see [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md) §8.3). The final report includes:

- Audit identification details (scope, dates, audit team, auditee);
- Executive summary;
- Audit approach and methodology;
- Summary of findings by classification;
- Full finding details with management responses;
- Overall audit opinion;
- Distribution list.

The final report is distributed to the auditee, the CAE/GRC Manager, the CISO (for security and privacy audits), and the ERC.

### 6.9 Closure tracking

All findings are entered into the audit register and, where required, into the CAPA register (see §10). The CAE/GRC Manager tracks remediation progress against agreed target dates and reports overdue items to the ERC.

Findings are marked as closed only when the CAE/GRC Manager has verified that the corrective action has been implemented and is effective.

---

## 7. Finding classification

Audit findings are classified using the following scheme, aligned to the CAPA Procedure (compliance/procedure-capa.md):

### 7.1 Critical

**Definition:** A material control failure that exposes the organization to significant risk of harm, regulatory sanction, certification failure, or operational disruption. The control is absent, has failed completely, or is being actively circumvented.

**Response requirements:**
- Immediate verbal or written notification to the CISO and CIO on the day of identification;
- Escalation to the ERC within **2 business days**;
- Documented remediation plan within **5 business days**;
- Remediation or interim compensating control implemented within **30 days**;
- Mandatory CAPA record (see §10);
- Follow-up audit of the affected control area within **12 months** of closure.

### 7.2 High

**Definition:** A significant control gap or deficiency that, if not remediated, is likely to increase risk exposure materially or result in a nonconformity at an external audit or regulatory inspection.

**Response requirements:**
- Notification to the CISO (for security/privacy domains) within **1 business day**;
- Documented remediation plan within **10 business days**;
- Remediation completed within **60 days**;
- Mandatory CAPA record (see §10).

### 7.3 Moderate

**Definition:** A control weakness where the control exists and provides some mitigation but does not fully meet the applicable requirement or operates with less-than-required effectiveness.

**Response requirements:**
- Documented remediation plan within the management response window;
- Remediation completed within **90 days**;
- CAPA record recommended but not mandatory unless the control area has recurring findings.

### 7.4 Low / observation

**Definition:** A minor improvement opportunity or best-practice observation that does not constitute a nonconformity against a defined requirement. The control is broadly effective but could be enhanced.

**Response requirements:**
- Acknowledged by the auditee in the management response;
- Addressed within **180 days** at the discretion of the domain owner;
- Tracked in the audit register.

---

## 8. Audit evidence requirements

### 8.1 Types of acceptable evidence

Audit evidence must be sufficient, appropriate, and relevant to support audit conclusions. Acceptable evidence types include:

| Evidence Type | Examples |
|---------------|----------|
| **Interviews** | Notes or recordings from structured discussions with process owners and subject matter experts |
| **Document Review** | Policies, procedures, records, training completion logs, change management logs, risk registers, contracts |
| **Observation** | Documented observations of processes in operation, physical controls, workspace practices |
| **Technical Testing** | Configuration screenshots, access control reports, vulnerability scan summaries, log extracts, tool output |

Where a finding is solely based on interview evidence, the auditor must attempt to corroborate through at least one additional evidence type before classifying the finding as Critical or High.

### 8.2 Evidence documentation

All evidence must be:

- Documented in audit working papers at the time of collection;
- Clearly cross-referenced to the relevant audit criterion and finding reference;
- Labelled with the collection date, collection method, and the auditor responsible;
- Stored securely in the designated audit evidence repository.

### 8.3 Evidence retention

All audit working papers, evidence artefacts, draft findings, management responses, and final reports must be retained for a minimum of **7 years** from the date of the final report, in accordance with the organization's data retention policy.

### 8.4 Verification basis in assembled evidence packages

Where control evidence is assembled into a package for an audit, internal or external (per [`compliance/template-audit-evidence-package.md`](template-audit-evidence-package.md)), each control's implementation status and operating effectiveness carries its verification basis: whether the status is independently verified (supported by an independent test per [`compliance/procedure-control-testing.md`](procedure-control-testing.md), where the tester is not the control owner), owner-asserted (asserted by the control owner and not independently tested for the period), or presented for the external auditor to verify. An owner-asserted status must not be presented as independently verified without a supporting test. This extends the Evidence-Based Approach principle and the interview-corroboration rule in section 8.1 to the assembly of evidence packages, so that a reader can distinguish verified status from a management assertion awaiting test.

---

## 9. Auditor competency requirements

### 9.1 Competency framework

Auditors must demonstrate competency aligned to the ISO 19011:2018 competency framework, covering:

- **Generic audit knowledge and skills:** Audit principles, evidence collection, interviewing, report writing, and audit programme management;
- **Management system knowledge:** Understanding of the management systems being audited (e.g., ISMS, PIMS, QMS);
- **Domain-specific knowledge:** Technical and process knowledge relevant to the domain being audited (e.g., information security, supply chain, AI governance);
- **Professional behaviour:** Integrity, objectivity, discretion, and professional scepticism.

### 9.2 Credential requirements

Lead auditors must hold at least one of the following, or must be operating under a structured supervised qualification programme:

- Relevant professional certification in auditing, information security, risk management, or a cognate discipline (e.g., certified internal auditor, certified information systems auditor, or equivalent);
- Documented completion of formal audit training that covers the ISO 19011 competency framework, with a minimum of three completed supervised audits as supporting lead auditor;
- For technical security audits: specialist technical certification or documented equivalent experience, reviewed and approved by the CAE/GRC Manager.

### 9.3 Supervised qualification programme

Where an auditor does not yet hold the required credentials, they may conduct audits under the direct supervision of a qualified lead auditor. The supervisory arrangement must be:

- Documented before commencement of the supervised audit;
- Reviewed by the CAE/GRC Manager;
- Limited to no more than three consecutive supervised engagements before formal qualification is required.

### 9.4 Continuing professional development

All auditors are expected to maintain current knowledge of evolving threats, control frameworks, and regulatory requirements relevant to the domains they audit. Evidence of continuing professional development is recorded as part of the annual competency review.

---

## 10. Relationship to CAPA procedure

### 10.1 Mandatory CAPA generation

All findings classified as **Critical** or **High** must result in a Corrective and Preventive Action (CAPA) record in accordance with the CAPA Procedure (compliance/procedure-capa.md).

The CAPA record must be opened within **2 business days** of the final report being issued, or immediately upon identification for Critical findings discovered during fieldwork.

### 10.2 Linkage between audit and CAPA records

Each CAPA record generated from an audit finding must reference:

- The audit identifier;
- The finding reference number;
- The finding classification.

Conversely, each audit finding record in the audit register must reference the corresponding CAPA ID once raised.

### 10.3 Moderate and low findings

Moderate findings may be elevated to a CAPA record at the discretion of the CAE/GRC Manager, particularly where:

- The finding represents a recurring issue across multiple audit cycles;
- The control area is material to a certification or regulatory requirement;
- The domain owner requests formalized tracking.

Low / Observation findings are tracked in the audit register and do not routinely generate CAPA records unless a pattern of recurrence is identified.

### 10.4 CAPA closure verification

Audit findings are not closed in the audit register until the corresponding CAPA record (where one exists) has been verified as closed by the GRC Manager. The CAE/GRC Manager may request evidence of closure and, for Critical and High findings, may require a follow-up audit to confirm sustained effectiveness.

---

## 11. Framework alignment

| Framework / Standard | Relevant Clause or Control | Mapping |
|----------------------|---------------------------|---------|
| ISO/IEC 27001:2022 | §9.2 Internal Audit | This standard operationalizes the internal audit requirements of the ISMS |
| ISO 19011:2018 | All clauses | Primary methodological reference for audit principles, programme management, and auditor competency |
| COBIT 2019 | MEA04 (Managed Assurance) | Audit programme management and assurance reporting align to MEA04 objectives |
| CSA Cloud Controls Matrix | A&A-01 through A&A-06 (Audit and Assurance) | Audit planning, scope, independence, results, metrics, and remediation |
| NIST Cybersecurity Framework 2.0 | DE.AE (Adverse Event Analysis) | Audit of detection and analysis controls |
| BASC Standard | §9.2 Internal Audit | Internal audit requirements for BASC certification scope |

---

**End of Document**
