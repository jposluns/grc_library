# Enterprise Risk Register Template

**Document Title:** Enterprise Risk Register Template\
**Document Type:** Template\
**Version:** 1.1.4\
**Date:** 2026-06-24\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md), [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Quarterly review of register entries; annual template review\
**Repository Path:** [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines the schema, field definitions, population guidance, and governance requirements for the organisation's enterprise risk register. The register is the primary instrument for tracking identified risks, their assessment scores, treatment plans, residual risk, and monitoring obligations across all risk categories.

---

## Risk record schema

Each risk entry in the register captures the following fields.

### Identification

| Field | Description | Example |
|---|---|---|
| **Risk ID** | Unique identifier: `RSK-[YYYY]-[NNN]` | `RSK-2026-001` |
| **Risk Title** | Short descriptive name | Ransomware disruption to logistics operations |
| **Risk Category** | Strategic / Operational / Cybersecurity / Privacy / AI / Supplier / Resilience / Financial / Legal and Regulatory / Technology / Human Capital / Physical | Cybersecurity |
| **Risk Owner** | Role accountable for risk management | Chief Information Security Officer |
| **Date Identified** | Date risk was first entered | 2026-01-15 |
| **Date Last Reviewed** | Date of most recent review | 2026-04-01 |
| **Next Review Date** | Scheduled next review | 2026-07-01 |

### Risk description

| Field | Description | Example |
|---|---|---|
| **Risk Statement** | "There is a risk that [threat/event] causes [impact] due to [root cause/vulnerability]" | There is a risk that a ransomware attack encrypts logistics and customs data, causing operational disruption and revenue loss, due to gaps in endpoint detection and backup isolation |
| **Threat / Event** | The event or scenario that could cause harm | Ransomware encryption of critical systems |
| **Root Cause / Vulnerability** | Underlying condition enabling the risk | Insufficient network segmentation; delayed patching cycle |
| **Affected Assets / Processes** | Systems, processes, or data at risk | Logistics management system; customs declarations platform |
| **Triggering Conditions** | Circumstances under which risk may materialize | Successful phishing leading to credential theft; unpatched vulnerability exploited |

### Inherent risk assessment

Assessed before any controls are applied, based on the likelihood × impact matrix in [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md).

| Field | Scale | Value |
|---|---|---|
| **Inherent Likelihood** | 1 (Very Low) to 5 (Very High) | |
| **Inherent Impact** | 1 (Negligible) to 5 (Catastrophic) | |
| **Inherent Risk Score** | Likelihood × Impact (1 to 25) | |
| **Inherent Risk Rating** | Low (1 to 4) / Medium (5 to 9) / High (10 to 16) / Critical (17 to 25) | |

### Current controls

| Field | Description |
|---|---|
| **Existing Controls** | List of controls currently in place, with policy/procedure references |
| **Control Effectiveness** | Strong / Adequate / Weak / Not Tested |
| **Control References** | Links to relevant policy, standard, or procedure documents |

### Residual risk assessment

Assessed after existing controls are applied.

| Field | Scale | Value |
|---|---|---|
| **Residual Likelihood** | 1 (Very Low) to 5 (Very High) | |
| **Residual Impact** | 1 (Negligible) to 5 (Catastrophic) | |
| **Residual Risk Score** | Likelihood × Impact (1 to 25) | |
| **Residual Risk Rating** | Low / Medium / High / Critical | |
| **Within Risk Appetite?** | Yes / No / Borderline: compare against [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md) | |

### Treatment

| Field | Description | Example |
|---|---|---|
| **Treatment Option** | Avoid / Mitigate / Transfer / Accept / Exploit / Enhance (canonical 6 per `risk/standard-enterprise-risk-management.md` Section 6) | Mitigate |
| **Treatment Actions** | Specific steps to reduce likelihood or impact | Deploy EDR on all endpoints; implement immutable backup; enhance network segmentation |
| **Treatment Owner** | Role responsible for implementing treatment | CISO / IT Operations Manager |
| **Target Residual Risk Score** | Score expected after treatment completion | 6 (Medium) |
| **Target Completion Date** | When treatment actions should be complete | 2026-09-30 |
| **Treatment Status** | Pending / In Progress / Complete (canonical 3 per `risk/standard-enterprise-risk-management.md` Section 6 + 7.1) | In Progress |
| **CAPA Reference** | Link to CAPA record if treatment is tracked as a corrective action | CAPA-2026-007 |

### Acceptance (if applicable)

If residual risk is not within appetite and is being formally accepted, complete:

| Field | Description |
|---|---|
| **Acceptance Rationale** | Reason treatment to appetite level is not practicable |
| **Acceptance Conditions** | Conditions under which acceptance remains valid |
| **Compensating Controls** | Controls in place that reduce residual risk to the level being accepted; list each by control ID with a brief note on how it offsets the un-treated risk. Required by [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md) §5; recorded here so the acceptance record is self-contained and auditable. |
| **Accepted By** | Role with authority to accept (per [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md)) |
| **Acceptance Date** | Date of formal acceptance |
| **Acceptance Expiry** | Date by which acceptance must be reviewed |
| **Acceptance Reference** | Risk Acceptance Record ID from [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md) |

### Monitoring

| Field | Description |
|---|---|
| **Key Risk Indicators** | KRI IDs from [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md) monitoring this risk |
| **Review Trigger Events** | Events that should prompt unscheduled review (e.g., related incident, regulatory change) |
| **Linked Incidents** | Any past incidents linked to this risk |
| **Linked Audit Findings** | Audit finding IDs related to this risk |

---

## Risk categories and definitions

| Category | Description |
|---|---|
| **Strategic** | Risks to strategic objectives, market position, or stakeholder confidence |
| **Operational** | Risks to day-to-day operational processes, service delivery, or productivity |
| **Cybersecurity** | Threats to information assets, systems, and data from malicious actors or technical failure |
| **Privacy** | Risks arising from processing personal data: regulatory non-compliance, data breach, misuse |
| **AI** | Risks from development, deployment, or use of AI systems: bias, transparency, security, regulatory |
| **Supplier** | Risks from third-party and supply chain dependencies: failure, security breach, non-compliance |
| **Resilience** | Risks to business continuity, disaster recovery, and crisis management capability |
| **Financial** | Risks to financial performance, liquidity, or financial reporting integrity |
| **Legal and Regulatory** | Risks from non-compliance with applicable laws, regulations, and standards |
| **Technology** | Risks from IT infrastructure failure, obsolescence, or capacity constraints |
| **Human Capital** | Risks from workforce shortfalls, skills gaps, succession, or misconduct |
| **Physical** | Risks to physical assets, facilities, and supply chain from environmental or security events |

---

## Risk rating matrix

The full 5×5 matrix is defined in [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md). Summary:

| | **1 Negligible** | **2 Minor** | **3 Moderate** | **4 Major** | **5 Catastrophic** |
|---|---|---|---|---|---|
| **5 Very High** | Medium (5) | High (10) | High (15) | Critical (20) | Critical (25) |
| **4 High** | Low (4) | Medium (8) | High (12) | High (16) | Critical (20) |
| **3 Medium** | Low (3) | Medium (6) | Medium (9) | High (12) | High (15) |
| **2 Low** | Low (2) | Low (4) | Medium (6) | Medium (8) | High (10) |
| **1 Very Low** | Low (1) | Low (2) | Low (3) | Low (4) | Medium (5) |

---

## Register governance

| Obligation | Frequency | Responsibility |
|---|---|---|
| New risk identification and entry | Ongoing: trigger-based | Risk owners; Risk Manager |
| Quarterly status update for all open risks | Quarterly | Risk owners |
| Full register review for treatment progress | Quarterly | Chief Risk Officer |
| Board / Risk Committee reporting pack | Quarterly | Chief Risk Officer |
| Annual comprehensive register review | Annual | Chief Risk Officer |
| Escalation of Critical risks to Board | Within 5 business days of identification | Chief Risk Officer |

---

## Sample risk entries

The following examples illustrate correctly populated risk records.

| Risk ID | Title | Category | Inherent Score | Residual Score | Treatment | Status |
|---|---|---|---|---|---|---|
| RSK-2026-001 | Ransomware disruption to logistics operations | Cybersecurity | 20 (Critical) | 9 (Medium) | EDR deployment; immutable backup; segmentation | Open |
| RSK-2026-002 | Key supplier insolvency disrupting freight operations | Supplier | 12 (High) | 6 (Medium) | Dual-sourcing; contractual SLAs; financial monitoring | Open |
| RSK-2026-003 | GDPR enforcement action for cross-border data transfer gaps | Legal and Regulatory | 16 (High) | 6 (Medium) | SCCs signed; transfer impact assessments completed | Open |
| RSK-2026-004 | AI bias in automated cargo routing causing discrimination claims | AI | 9 (Medium) | 4 (Low) | Bias testing pre-deployment; quarterly fairness review | Open |
| RSK-2026-005 | Loss of AEO-S certification due to security compliance gap | Legal and Regulatory | 12 (High) | 4 (Low) | AEO-S self-assessment procedure; controls maintained | Open |

---

**End of Document**
