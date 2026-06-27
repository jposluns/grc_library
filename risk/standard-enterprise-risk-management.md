# Enterprise Risk Management Standard

**Document Title:** Enterprise Risk Management Standard\
**Document Type:** Standard\
**Version:** 1.7.2\
**Date:** 2026-06-27\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](policy-enterprise-governance-and-risk-management.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual or as required by regulatory or framework changes\
**Repository Path:** [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the enterprise-wide risk management framework, taxonomy, and scoring methodology that guide the identification, evaluation, treatment, and monitoring of risks across all business units and functions. It ensures that risk management practices are consistent, measurable, and traceable, aligned with ISO 31000, COBIT 2019 APO12, and CSA CCM v4.1 GRC-01.

---

## 2. Scope

1. This standard applies to all business, operational, financial, security, privacy, AI, and technology risks managed within the organisation and its subsidiaries. Sector-specific risk overlays (for example, BASC for trade and logistics operations) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).
2. It covers both strategic and operational risk management activities across enterprise, project, and system levels.
3. It applies to all employees, contractors, and third parties responsible for risk identification, analysis, reporting, or control execution.

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Risk Officer | Accountable for the overall enterprise risk management framework and its alignment with strategic objectives; owns risk strategy, risk appetite stewardship, and ERM-programme outcomes; reports to the Board or Risk Committee. |
| Chief Information Officer | Provides executive support to the ERM programme on technology-risk integration; ensures that IT-strategy risk is reflected in the enterprise risk register. |
| Chief Information Security Officer | Responsible for managing information security, privacy, and AI-related risks; ensures that integration into the risk register. |
| Enterprise Risk Committee (ERC) | Oversees risk appetite, tolerance, and periodic risk reporting; meets quarterly. |
| Risk Manager / Compliance Officer | Administers risk registers and scoring models; facilitates risk assessments across the organisation. |
| Risk Owner | Accountable for a specific named risk entered in the enterprise risk register: confirms the risk statement, selects the treatment option, owns the treatment plan and target dates, monitors residual exposure, reports status per the cadence in §8, and validates risk assessments supporting exception requests (per [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) §2: confirms residual exposure stays within the enterprise risk appetite when an exception is requested). Distinct from the Chief Risk Officer (who owns the ERM framework and methodology) and from Process and System Owners (who identify risks within their operational domains but do not necessarily own each named risk in the register). Canonical role definition in [`governance/register-role-authority.md`](../governance/register-role-authority.md) §Authority register. |
| Process and System Owners | Identify risks within their domains, implement controls, and report residual exposures. |
| Internal Audit | Provides independent assurance on risk governance and control effectiveness. |

---

## 4. Risk taxonomy

The organisation maintains the following risk taxonomy. Each category contains subcategories used to classify risks consistently in the risk register.

| Category | Example Subcategories |
|---|---|
| Strategic | Market disruption, regulatory change, AI governance deficiencies, ESG non-compliance |
| Operational | Process failure, supply chain disruption, human error, system outages |
| Information Security | Cyberattack, data breach, privilege misuse, cryptographic failure |
| Compliance and Legal | Regulatory penalties, contract non-compliance, privacy law violations |
| Financial | Budget variance, fraud, liquidity shortfall |
| AI and Data | Algorithmic bias, model drift, explainability gaps, dataset integrity failure, misuse of personal data |
| Environmental and Sustainability | Energy inefficiency, environmental damage, technology lifecycle waste |
| Third-Party and Supply Chain | Supplier insolvency, concentration risk, vendor security failure |
| Business Continuity and Resilience | Single point of failure, disaster recovery gap, critical service unavailability |
| Human Capital | Insider threat, key-person dependency, skills gap |

---

## 5. Risk assessment and scoring

### 5.1 Assessment process

Each material risk assessment must record:

- Risk statement (cause → event → impact format recommended).
- Affected assets, services, data, suppliers, or AI systems.
- Inherent likelihood and impact scores (before controls).
- Existing controls and assessed control effectiveness.
- Residual likelihood and impact scores (after controls).
- Treatment decision and owner.
- Review date and evidence references.

### 5.2 Scoring matrix

Risk scores are calculated as **Likelihood (1 to 5) × Impact (1 to 5) = Risk Score (1 to 25)**. The likelihood labels and descriptions and the score-to-rating thresholds below match the canonical scale defined in the risk-assessment methodology [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md) Section 4 to Section 5; the [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md) scoring fields reference this scale rather than defining their own, so a given score yields the same Low / Medium / High / Critical rating in this standard and the methodology.

#### Likelihood scale

| Score | Label | Description |
|---|---|---|
| 1 | Very Low | Unlikely; no known precedent in the industry |
| 2 | Low | Possible; known to occur occasionally |
| 3 | Medium | Likely; occurs periodically across the industry |
| 4 | High | Expected; known active threat, frequently observed |
| 5 | Very High | Near-certain; active exploitation confirmed |

#### Impact scale

| Score | Label | Description |
|---|---|---|
| 1 | Negligible | Minimal effect; no regulatory exposure; fully absorbed operationally |
| 2 | Minor | Limited disruption; minor financial loss; no regulatory action |
| 3 | Moderate | Significant operational disruption; measurable financial loss; possible regulatory inquiry |
| 4 | Major | Serious harm to operations, customers, or data subjects; regulatory investigation likely |
| 5 | Catastrophic | Existential financial or reputational impact; regulatory sanctions; loss of operating licence |

#### 5×5 risk scoring matrix

| | **Impact 1** | **Impact 2** | **Impact 3** | **Impact 4** | **Impact 5** |
|---|---|---|---|---|---|
| **Likelihood 5** | 5 | 10 | 15 | 20 | 25 |
| **Likelihood 4** | 4 | 8 | 12 | 16 | 20 |
| **Likelihood 3** | 3 | 6 | 9 | 12 | 15 |
| **Likelihood 2** | 2 | 4 | 6 | 8 | 10 |
| **Likelihood 1** | 1 | 2 | 3 | 4 | 5 |

#### Score thresholds and required response

| Score Range | Rating | Required Response |
|---|---|---|
| 1 to 4 | Low | Accept; monitor annually |
| 5 to 9 | Medium | Mitigate and monitor; review quarterly |
| 10 to 16 | High | Mitigate or transfer; assign owner; review monthly |
| 17 to 25 | Critical | Immediate action required; ERC oversight; escalate to executive leadership |

---

## 6. Risk treatment

Treatment decisions must be documented with one of the following options:

| Option | Description |
|---|---|
| Avoid | Eliminate the activity or condition that gives rise to the risk |
| Mitigate | Implement controls to reduce likelihood or impact to an acceptable level |
| Transfer | Shift financial consequence to a third party (e.g., insurance, contractual liability) |
| Accept | Formally accept residual risk per the Risk Acceptance Procedure |
| Exploit | Pursue a positive-risk (opportunity) scenario by acting to make it more likely to occur or to amplify its upside |
| Enhance | Increase the likelihood or impact of an existing positive-risk scenario without creating a new one |

Each treatment plan must include: accountable owner, target completion date, required actions, dependencies, expected residual risk score, and current status.

**Terminology**: this Section 6 "Treatment Option" names the choice the risk owner makes about how to address the risk; Section 7.1's "Treatment Status" (added in this Standard's version 1.6.0 to remove the prior ambiguity) names the workflow state of that choice's execution. The two fields are independent: a risk with Treatment Option = Mitigate may have Treatment Status = Pending (plan documented, controls not yet implemented), In Progress, or Complete. Section 7.1's "Status" field is the risk-record lifecycle state (Open / Closed) and does NOT duplicate Treatment Status.

---

## 7. Risk register entry fields

Each risk register entry must include the following fields.

### 7.1 Standard fields

| Field | Description |
|---|---|
| Risk ID | Unique identifier (e.g., RISK-2025-001) |
| Category | Taxonomy category (see Section 4) |
| Subcategory | Taxonomy subcategory |
| Risk Statement | Cause → event → impact description |
| Likelihood (Inherent) | Score 1 to 5 |
| Impact (Inherent) | Score 1 to 5 |
| Inherent Risk Score | Likelihood × Impact |
| Existing Controls | Description of current controls |
| Control Effectiveness | Assessed as Strong / Adequate / Weak / Untested |
| Likelihood (Residual) | Score 1 to 5 |
| Impact (Residual) | Score 1 to 5 |
| Residual Risk Score | Likelihood × Impact |
| Treatment Option | Avoid / Mitigate / Transfer / Accept / Exploit / Enhance (per Section 6) |
| Treatment Actions | Specific steps with owner and target date |
| Treatment Status | Pending / In Progress / Complete. Workflow state of the Treatment Option's execution; independent of the Status field below |
| Risk Owner | Accountable individual (role title) |
| Status | Open / Closed. Risk-record lifecycle state. A risk is Open while it remains within the organisation's risk appetite considerations; a risk is Closed when no further treatment or monitoring action remains (e.g., the underlying activity has ceased, or the residual risk is accepted indefinitely under a documented acceptance). The Status field does NOT name the treatment outcome (which is captured by Treatment Option) or the treatment workflow state (Treatment Status above). |
| Review Frequency | Monthly / Quarterly / Annually |
| Last Reviewed | Date |
| Next Review | Date |
| AI Flag | Yes / No |

### 7.2 Additional fields for AI-specific risks

When the AI Flag is set to Yes, the following additional fields are required:

| Field | Description |
|---|---|
| Model or Dataset Reference ID | Identifier linking to the AI system or dataset inventory |
| Bias Detection Outcome | Result of most recent bias assessment (Pass / Fail / In Progress) |
| Explainability Confidence Score | Assessed confidence that model outputs can be explained (High / Medium / Low) |
| AI System Classification | Minimal / Limited / High / Unacceptable per applicable AI regulatory classification |
| Human-in-the-Loop Requirement | Required / Recommended / Not Required |

---

## 8. Risk monitoring and reporting

### 8.1 Monitoring cadence

- Departmental risk reviews are conducted quarterly by process and system owners.
- AI risk trends (bias recurrence, model drift, ethical deviations) are monitored on an ongoing basis and summarized quarterly.
- Risk Owner review cadences by score band (Low / Medium / High cadences taken verbatim from the §5.2 "Score thresholds and required response" table; Critical's cadence is the existing monthly position from this section):
  - Critical risks (score 17 to 25) are reviewed monthly by the Risk Owner and reported to the ERC.
  - High risks (score 10 to 16) are reviewed monthly by the Risk Owner.
  - Medium risks (score 5 to 9) are reviewed quarterly by the Risk Owner.
  - Low risks (score 1 to 4) are reviewed annually by the Risk Owner.

### 8.2 Reporting

- Aggregated departmental risk reports are escalated to the ERC quarterly.
- The CIO and CISO present a consolidated Enterprise Risk Dashboard to executive leadership quarterly and annually.
- The Enterprise Risk Dashboard includes: open risk counts by category and score band, KRI trends, overdue treatment actions, AI risk summary, and third-party risk exposure.
- Material changes in risk posture or new critical risks are escalated outside the regular cycle within five business days of identification.

---

## 9. Evidence requirements

### 9.1 General evidence catalogue

Required evidence for audit and assurance purposes includes, but is not limited to:

- Completed risk register entries with scoring rationale.
- Risk assessment records and workshop outputs.
- Treatment plans with status and owner confirmation.
- Control test results and exception records.
- Risk acceptance approvals (per Risk Acceptance Procedure).
- ERC and AIGC meeting records referencing risk items.
- Supplier risk assessments and due diligence outputs.
- AI impact assessments and bias test reports.
- Business impact analyses and continuity test records.
- Internal audit findings and management responses.

### 9.2 Risk Owner evidence by accountability action

The Risk Owner role's six accountability actions (defined in §3) map to specific evidence types from §9.1:

| Risk Owner accountability action (per §3) | Evidence that proves execution |
|---|---|
| Confirms the risk statement | Risk register entry with Risk Owner attribution and scoring rationale (from §9.1 "Completed risk register entries with scoring rationale"). |
| Selects the treatment option | Treatment plan record showing the selected option from the §6 set (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance) with Risk Owner sign-off (from §9.1 "Treatment plans with status and owner confirmation"). |
| Owns the treatment plan and target dates | Treatment plan record with target dates, Risk Owner identified as plan owner, and dated progress entries (from §9.1 "Treatment plans with status and owner confirmation"). |
| Monitors residual exposure | Periodic risk register update entries dated per the §8.1 cadence band (annually for Low, quarterly for Medium, monthly for High and Critical), each recording the current residual exposure and any changes from the previous review. |
| Reports status per the §8.1 cadence | Risk Owner status reports (per the §8.1 cadence band) recorded in the risk register or in the ERC meeting record (from §9.1 "ERC and AIGC meeting records referencing risk items"). |
| Validates risk assessments for exception requests | Exception register entries with Risk Owner sign-off confirming the residual exposure stays within enterprise risk appetite (from §9.1 "Risk acceptance approvals (per Risk Acceptance Procedure)"; cross-references [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) §2). |

---

## 10. Framework alignment

| Framework | Relevant Reference |
|---|---|
| ISO 31000:2018 | Risk Management: Guidelines (full framework) |
| ISO/IEC 23894:2023 | AI Risk Management |
| ISO/IEC 42001:2023 | AI Management System |
| COBIT 2019 | APO12 Manage Risk; APO10 Manage Suppliers; MEA01 |
| CSA CCM v4.1 | GRC-01 Risk Management Framework |
| NIST SP 800-39 | Managing Information Security Risk |
| NIST AI RMF | Govern, Map, Measure, Manage functions |
| OECD AI Principles | Transparency, robustness, accountability |
| GDPR | As applicable to EU personal data |
| PIPEDA (Canada Personal Information Protection and Electronic Documents Act) | As applicable to Canadian personal information |
| PIPL | As applicable to personal information in China |
| LGPD | As applicable to Brazilian personal data |
| CBPR 2.0 | Cross-Border Privacy Rules as applicable |

---

## 11. Licence

This document is released under the **CC BY-SA 4.0** CC BY-SA 4.0 licence. To the extent possible under law, the organisation waives all copyright and related rights to this document.

---

**End of Document**
