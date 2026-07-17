# AI Governance Council Charter

**Document Title:** AI Governance Council Charter\
**Document Type:** Charter\
**Version:** 1.2.8\
**Date:** 2026-07-17\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`ai/charter-ai-ethics-review-panel.md`](charter-ai-ethics-review-panel.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material organizational or regulatory change\
**Repository Path:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This charter establishes the mandate, composition, authority, responsibilities, and operating procedures of the AI Governance Council (AIGC). The AIGC is the enterprise body responsible for overseeing the risk and compliance governance of all artificial intelligence systems deployed or developed by the organization, working with the independent AI Ethics Review Panel on the ethics dimension (see below).

The AIGC ensures that AI use aligns with the organization's values, applicable law, and international standards including ISO/IEC 42001, the EU AI Act, NIST AI RMF, and OECD AI Principles.

Independent ethical review of AI systems is performed by the [AI Ethics Review Panel](charter-ai-ethics-review-panel.md), a separate body that applies the [Ethical AI Use Guideline](guideline-ethical-ai-use.md) and can challenge a Council decision on ethical grounds through the Panel's independent challenge mechanism. The Council retains AI risk and compliance governance and deployment-approval authority; it considers the Panel's ethical opinions and reconsiders and responds to the Panel's challenges. The separation exists so that ethical review is independent of the body whose decisions it reviews.

---

## Mandate

The AI Governance Council is mandated to:

1. Provide oversight of AI system risk and compliance, and act on the independent ethical review and challenges provided by the AI Ethics Review Panel.
2. Approve high-risk AI system deployments and significant AI lifecycle changes.
3. Review and approve AI governance policies, standards, and frameworks.
4. Monitor AI maturity, bias, explainability, and safety performance indicators.
5. Advise the Enterprise Risk Committee (ERC) and executive leadership on AI governance matters.
6. Maintain alignment with ISO/IEC 42001, EU AI Act, NIST AI RMF, and OECD AI Principles.

---

## Scope of authority

The AIGC has authority to:

- Approve or reject high-risk AI system deployments.
- Require remediation or decommissioning of AI systems that fail governance standards.
- Commission AI audits; refer AI systems to the AI Ethics Review Panel for independent ethical review.
- Reconsider and respond to ethical challenges raised by the AI Ethics Review Panel.
- Escalate critical AI risks to the ERC and Board.
- Issue binding guidance on AI risk and compliance, informed by the AI Ethics Review Panel's ethical opinions.

---

## Composition

| Role | Seat |
| --- | --- |
| **Chair** | Chief Information Security Officer |
| **Deputy Chair** | Chief Information Officer |
| **Member** | Chief Technology Officer |
| **Member** | Chief Financial Officer |
| **Member** | Chief Human Resources Officer |
| **Member** | General Counsel |
| **Member** | Data Protection Officer |
| **Member** | Chief Risk Officer |
| **Secretariat** | AI Governance Lead (per the role authority register) |
| **Member** | Business Domain Representative (rotating; appointed by the Enterprise Risk Committee) |
| **Standing observer** | Independent External Adviser (appointed for a defined term) |

The council is an active body. Where any member seat is unfilled at a given time, the responsibilities of that seat are exercised by the role's direct delegate or by an acting appointee designated by the Chair. The Chair confirms each meeting's roster at the start of the meeting.

Quorum requires attendance of the Chair (or Deputy Chair) plus at least four members. Decisions are recorded with the date, attendees, and the decision rationale.

### Roles outside the council that report into it

The AI governance function has three operational sub-roles defined in the role authority register. They report into the council through the AI Governance Lead (secretariat):

| Role | Reports through | Council interaction |
| --- | --- | --- |
| AI Governance Approver | AI Governance Lead | Brings approval items (deployment gates, policy approvals, exception approvals) to the council; acts under delegated authority between council meetings |
| AI Data Steward | AI Governance Lead | Brings dataset, training-data, and deletion-propagation matters to the council where they cross the council's escalation thresholds |
| AI System Inventory Keeper | AI Governance Lead | Maintains the inventories the council reviews; reports inventory consistency and material additions |

Charter administrative ownership rests with the Chief Information Officer (the charter's metadata Owner); governance decisions rest with the council; per-system or per-decision approvals rest with the AI Governance Approver acting under delegated council authority. The role authority register is the source of truth for the role definitions.

---

## Responsibilities

### 1. AI risk oversight

- Review AI Impact Assessments for all high-risk AI systems.
- Assess AI systems against the organizational AI risk taxonomy: Minimal, Limited, High, Unacceptable.
- Consider the AI Ethics Review Panel's independent ethical opinion (fairness, bias mitigation, transparency, explainability, human oversight, and impact on affected individuals and groups) alongside the risk and compliance review.
- Monitor outcomes of deployed AI systems against defined performance thresholds.

### 2. Policy and standards governance

- Approve AI governance policies, standards, and frameworks before publication.
- Ensure that AI documents remain current with ISO/IEC 42001 and regulatory requirements.
- Review and approve the AI System Inventory annually.

### 3. Audit and assurance

- Oversee the AI audit programme per the AI Audit Procedure.
- Review AI audit findings and approve corrective action plans.
- Report on AI governance maturity to the ERC quarterly.

### 4. Incident and escalation management

- Receive and review escalated AI-related security or ethics incidents.
- Approve responses to AI system failures with significant impact.
- Ensure that AI incidents are documented and lessons learned are incorporated.

### 5. Model lifecycle governance

- Approve the deployment of new AI models into production.
- Review material changes to deployed AI models (retraining, scope expansion). "Material" is defined by the Material change thresholds table in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).
- Confirm decommissioning of AI systems that are end-of-life or non-compliant.

---

## Operating procedures

| Activity | Frequency |
| --- | --- |
| Regular AIGC meeting | Quarterly |
| AI risk review | Quarterly |
| High-risk deployment reviews | As required (within 10 business days of request) |
| Annual AI governance report | Annual: submitted to ERC and Board |
| Policy and standards review | Annual |

Meetings are minuted. Decisions, approvals, and escalations are recorded. Minutes are retained in the governance document repository.

---

## Reporting

The AIGC reports to the Enterprise Risk Committee (ERC). Quarterly AI Governance Reports include:

- AI system inventory status.
- High-risk deployment decisions.
- Audit findings and remediation status.
- AI maturity KPI performance, assessed against the [AI Maturity Model Framework](framework-ai-maturity-model.md) (the overall maturity level with its floor-check exceptions).
- Regulatory compliance status.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §5.1 to §5.3: Leadership and commitment, AI policy, roles and responsibilities | AI management system governance |
| ISO/IEC 42001:2023 | A.3: Internal organization | Accountability structure and reporting of concerns |
| ISO/IEC 42001:2023 | §9: Performance Evaluation | AI maturity monitoring |
| ISO/IEC 38507:2022 | Governance implications of the use of AI by organizations | Governing-body AI oversight responsibilities |
| EU AI Act (2024) | Chapter III: High-Risk AI Systems | High-risk AI oversight |
| NIST AI RMF (2023) | GOVERN 2.3 (executive-leadership responsibility) and GOVERN 1.6 (AI inventory) | AI governance structure |
| OECD AI Principles (2019, updated 2024) | Accountability and oversight | AI ethics oversight |
| COBIT 2019 | EDM01: Ensured Governance Framework Setting and Maintenance | AI governance-framework setting and oversight-body maintenance |

---

**End of Document**
