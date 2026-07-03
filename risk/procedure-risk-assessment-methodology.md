# Risk Assessment Methodology Procedure

**Document Title:** Risk Assessment Methodology Procedure\
**Document Type:** Procedure\
**Version:** 1.2.4\
**Date:** 2026-07-03\
**Owner:** GRC Programme Manager\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`governance/framework-governance-performance-and-improvement.md`](../governance/framework-governance-performance-and-improvement.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md)\
**Classification:** Public\
**Category:** Risk\
**Review Frequency:** Annual and upon material risk framework or regulatory change\
**Repository Path:** [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the methodology for conducting risk assessments across all organizational domains including information security, privacy, AI, business continuity, supply chain, and operational risk. It establishes a consistent approach for identifying, analyzing, evaluating, and treating risks, aligned with ISO 31000:2018 and ISO/IEC 27005:2022.

---

## Scope

Applies to all risk assessments conducted within the organization including: annual enterprise risk assessments, project and change risk assessments, third-party risk assessments, AI impact and risk assessments, and ad-hoc risk assessments triggered by incidents or material changes.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **GRC Programme Manager** | Maintains risk assessment methodology; coordinates enterprise risk assessments. |
| **Risk Owners** | Conduct risk assessments for their domain; own risk treatment decisions. |
| **CISO** | Approves information security and AI risk assessments. |
| **ERC** | Reviews enterprise risk register and risk acceptance decisions; recommends High and Critical acceptances to the Board Risk Committee. |
| **Internal Audit** | Reviews risk assessment quality and methodology adherence annually. |

---

## 1. Risk assessment process overview

The risk assessment process follows the ISO 31000 framework:

```
Establish Context → Identify Risks → Analyze Risks → Evaluate Risks → Treat Risks → Monitor and Review
```

---

## 2. Establish context

2.1 Define the scope: systems, processes, assets, or domains in scope.

2.2 Define the objectives: what the assessment aims to protect or achieve.

2.3 Identify applicable regulatory and framework requirements (ISO 27001, GDPR, PIPEDA, EU AI Act, etc.).

2.4 Confirm the risk criteria: likelihood scale, impact scale, and risk tolerance thresholds.

---

## 3. Risk identification

3.1 Identify risks using a combination of:
- Asset and process inventory review.
- Threat intelligence and vulnerability data.
- Previous incident and CAPA data.
- Regulatory and framework requirement analysis.
- Stakeholder interviews and workshops.

3.2 Each identified risk is documented with:
- Risk ID.
- Risk description.
- Threat source and threat event.
- Affected asset or process.
- Potential consequence.

---

## 4. Risk analysis

4.1 Likelihood and impact are assessed using the following scales:

**Likelihood Scale:**

| Score | Level | Description |
| --- | --- | --- |
| 1 | Very Low | Unlikely; no known precedent in the industry |
| 2 | Low | Possible; known to occur occasionally |
| 3 | Medium | Likely; occurs periodically across the industry |
| 4 | High | Expected; known active threat, frequently observed |
| 5 | Very High | Near-certain; active exploitation confirmed |

**Impact Scale:**

| Score | Level | Description |
| --- | --- | --- |
| 1 | Negligible | Minimal operational impact; no regulatory consequence |
| 2 | Minor | Limited impact; contained within one system or team |
| 3 | Moderate | Significant operational disruption; potential regulatory notice |
| 4 | Major | Significant breach, regulatory investigation, or material financial loss |
| 5 | Catastrophic | Existential regulatory or reputational damage; loss of operating licence |

4.2 Inherent risk score = Likelihood × Impact.

4.3 Control effectiveness is assessed (Strong / Adequate / Weak / Untested, per the risk-register field model in [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md) Section 7) and residual risk is re-scored with existing controls taken into account:

Residual risk score = Residual likelihood × Residual impact

Residual likelihood and residual impact are re-assessed on the same 1-to-5 scales as the inherent assessment, so inherent and residual scores share the 1-to-25 range and the Section 5 score-to-rating bands apply to both.

---

## 5. Risk evaluation

5.1 Risks are classified against the risk tolerance matrix:

| Residual Risk Score | Rating | Action Required |
| --- | --- | --- |
| 1 to 4 | Low | Accept; monitor annually |
| 5 to 9 | Medium | Treat or formally accept with documented rationale |
| 10 to 16 | High | Treat; corrective action required within 90 days |
| 17 to 25 | Critical | Treat immediately; escalate to ERC within 5 business days |

5.2 Risks above the organization's risk tolerance require a treatment plan or formal risk acceptance.

---

## 6. Risk treatment

6.1 Risk treatment options (canonical six per [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md) Section 6):

| Option | Definition |
| --- | --- |
| **Avoid** | Eliminate the activity or asset creating the risk |
| **Mitigate** | Implement controls to reduce likelihood or impact |
| **Transfer** | Shift financial consequence to a third party (e.g., insurance, contractual liability) |
| **Accept** | Formally accept residual risk with documented rationale |
| **Exploit** | Pursue a positive-risk (opportunity) scenario by acting to make it more likely to occur or to amplify its upside |
| **Enhance** | Increase the likelihood or impact of an existing positive-risk scenario without creating a new one |

6.2 Risk treatment plans include: treatment option, controls to be implemented, owner, due date, and residual risk target.

6.3 Risk acceptance decisions are documented in the Risk Register. High and Critical acceptances require Executive Committee or Board Risk Committee approval, per the acceptance-authority chain in the Approval guidance section of [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md) and Section 4.2.2 of [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md); the ERC reviews and recommends per its authority in [`governance/register-role-authority.md`](../governance/register-role-authority.md).

6.4 Risk treatment actions are tracked in the CAPA Register.

---

## 7. Risk register

7.1 All identified risks are recorded in the organizational Risk Register.

7.2 The Risk Register includes: Risk ID, description, risk owner, inherent risk score, current controls, residual risk score, treatment status, and review date.

7.3 The Risk Register is reviewed quarterly by the GRC Programme Manager and presented to the ERC.

7.4 High and Critical risks are reviewed monthly.

---

## 8. Monitoring and review

8.1 Risk assessments are reviewed:
- Annually as part of the GRC Programme Management Procedure.
- Following any material incident, change, or regulatory development.
- When residual risk changes significantly.

8.2 Risk monitoring indicators (KRIs) are defined for High and Critical risks and tracked monthly.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 31000:2018 | Risk Management: Guidelines | Enterprise risk assessment framework |
| ISO/IEC 27005:2022 | Information Security Risk Management | Information security risk methodology |
| ISO/IEC 42001:2023 | §6: Planning (AI risk) | AI risk assessment integration |
| NIST SP 800-30r1 | Guide for Conducting Risk Assessments | Risk assessment methodology |
| COBIT 2019 | APO12: Managed Risk | Enterprise risk governance |
| CSA CCM v4.1 | GRC-01 through GRC-11 | Cloud risk management |

---

**End of Document**
