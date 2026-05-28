# Control Testing Procedure

**Document Title:** Control Testing Procedure 
**Document Type:** Procedure 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md), [`compliance/procedure-capa.md`](procedure-capa.md), [`governance/framework-continuous-assurance-and-improvement.md`](../governance/framework-continuous-assurance-and-improvement.md), [`governance/framework-governance-performance-and-improvement.md`](../governance/framework-governance-performance-and-improvement.md) 
**Classification:** Public 
**Category:** Compliance Management 
**Review Frequency:** Annual and upon material control framework change 
**Repository Path:** [`compliance/procedure-control-testing.md`](procedure-control-testing.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the processes for testing the design and operating effectiveness of internal controls across the organisation's governance, risk, compliance, security, and operational domains. Control testing provides objective evidence that controls are functioning as intended and supports certification, audit readiness, and continuous assurance activities.

---

## Scope

Applies to all controls defined in the organisation's control frameworks including ISO 27001 Annex A, COBIT 2019, CSA CCM v4.1, NIST SP 800-53, and any applicable regulatory control requirements. Encompasses preventive, detective, and corrective controls across all domains.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Chief Compliance Officer** | Owns the control testing programme; approves the annual testing calendar. |
| **GRC Programme Manager** | Schedules and coordinates control testing activities. |
| **Internal Audit** | Executes independent control testing; issues findings. |
| **Control Owners** | Provide evidence; remediate deficiencies. |
| **CISO** | Reviews security control testing results and approves remediation plans. |

---

## 1. Control testing planning

1.1 The annual Control Testing Calendar is prepared by the GRC Programme Manager in alignment with the Audit Planning Procedure.

1.2 Controls are prioritized for testing based on:
- Risk rating (high-risk controls tested at minimum annually).
- Certification scope (ISO 27001, SOC 2, BASC, etc.).
- Prior year findings and remediation outcomes.
- Material changes to control environment.

1.3 The testing calendar distinguishes between: design effectiveness testing (is the control properly designed?) and operating effectiveness testing (is the control working as designed?).

---

## 2. Control testing methodology

### 2.1 Design effectiveness testing

Design testing verifies that a control, if operating as designed, would prevent or detect the associated risk.

Design testing methods:
- Policy and procedure review.
- Control design interview with control owner.
- Control flowchart and process mapping review.
- Comparison against control framework requirement.

Outcome: Design adequate / Design gap identified.

### 2.2 Operating effectiveness testing

Operating testing verifies that a control has operated consistently during the test period.

Operating testing methods:

| Testing Method | Applicability |
| --- | --- |
| **Inquiry** | Interviews with control operators; supports but does not stand alone |
| **Observation** | Direct observation of control execution |
| **Inspection** | Review of documents, logs, and evidence samples |
| **Re-performance** | Independent re-execution of the control to verify outcome |
| **Automated testing** | Continuous monitoring outputs; automated evidence collection |

Sample sizes for inspection-based tests follow a risk-based sampling methodology:
- High-risk controls: 25 to 40 samples or 100% population if feasible.
- Medium-risk controls: 15 to 25 samples.
- Low-risk controls: 5 to 15 samples.

---

## 3. Evidence collection

3.1 All testing is supported by documented evidence retained in the compliance repository.

3.2 Evidence must be: relevant, sufficient, reliable, and traceable to the control period tested.

3.3 Evidence is retained for a minimum of 5 years or longer where regulatory requirements specify.

---

## 4. Testing results and findings

4.1 Control testing results are classified as:

| Result | Definition |
| --- | --- |
| **Effective** | Control designed and operating effectively; no exceptions noted |
| **Observation** | Minor weakness; no material risk; improvement recommended |
| **Deficiency** | Control gap that, individually or in combination, could lead to failure to prevent or detect a material misstatement or breach |
| **Material Weakness** | Significant deficiency with high likelihood of material impact if not remediated |

4.2 Deficiencies and material weaknesses are logged in the CAPA Register.

4.3 Control owners receive testing results within 5 business days of testing completion.

---

## 5. Reporting

5.1 Control testing summary reports are issued quarterly to the Chief Compliance Officer and CISO.

5.2 Annual control testing outcomes are included in the Governance Status Report to the ERC.

5.3 Certification-scope control testing results are provided to external auditors as required.

---

## 6. Remediation and re-testing

6.1 Control owners must submit remediation plans for all deficiencies within 10 business days.

6.2 Material weaknesses require executive review and remediation within 30 days.

6.3 Remediated controls are re-tested by Internal Audit before the deficiency is closed in the CAPA Register.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | §9.1: Monitoring, Measurement, Analysis and Evaluation | Control effectiveness measurement |
| ISO 19011:2018 | Guidelines for Auditing Management Systems | Control testing methodology |
| NIST SP 800-53A | Assessing Security and Privacy Controls | Control testing guidance |
| COBIT 2019 | MEA01: Monitor, Evaluate, and Assess Performance | Control monitoring and assurance |
| CSA CCM v4.1 | GOV-09: Governance and Continuous Improvement | Continuous control assurance |

---

**End of Document**
