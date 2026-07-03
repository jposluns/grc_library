# Acceptance Into Service Policy

**Document Title:** Acceptance Into Service Policy\
**Document Type:** Policy\
**Version:** 1.0.6\
**Date:** 2026-07-03\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material framework or regulatory change\
**Repository Path:** [`security/policy-acceptance-into-service.md`](policy-acceptance-into-service.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This policy establishes a standardized framework for evaluating, approving, and transitioning new or changed systems, services, and AI solutions into operational production environments. It ensures that all deliverables meet readiness, compliance, security, and risk requirements before formal acceptance.

The policy replaces the AIS Lifecycle Process, Readiness Review Procedure, and Post-Implementation Review Procedure, providing a unified acceptance model for IT, cloud, and AI-enabled services.

It aligns with ISO/IEC 42001 §8 Operation, NIST SP 800-37 Risk Management Framework (RMF) Step 6: Authorize the System, COBIT 2019 BAI07 Manage Change Acceptance and Transitioning, and CSA CCM v4.1 CCC-01, CCC-02, and CCC-05 (change acceptance and transitioning).

Mandatory AI risk classification and impact validation are required as a prerequisite for production deployment.

---

## 2. Scope

1. Applies to all new, modified, or upgraded systems, services, applications, infrastructure components, and AI models transitioning into the production environment.
2. Covers both internal and third-party delivered services, including cloud and SaaS integrations.
3. Applies to all business units, project managers, developers, and service owners responsible for solution deployment and operational handover.
4. Encompasses security, compliance, operational, and AI governance readiness validation.

---

## 3. Governance and accountability

### 3.1 Executive oversight

1. The Chief Information Officer (CIO) is accountable for enforcing the AIS process and ensuring integration with enterprise governance, risk, and compliance frameworks.
2. The Chief Information Security Officer (CISO) validates that security, privacy, and risk management controls are satisfied prior to production approval.
3. The Enterprise Architecture and Service Management Offices jointly verify operational readiness, documentation, and support model adequacy.
4. The AI Governance Council (AIGC) reviews AI-related AIS submissions for ethical, risk, and safety conformance.

### 3.2 Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Project Owner / Sponsor** | Ensures that project objectives, requirements, and acceptance criteria are met prior to AIS submission. |
| **CIO** | Authorizes final AIS approval based on security, compliance, and risk validation. |
| **CISO** | Confirms all applicable controls from the ISMS, Privacy, and AI Risk Standards are satisfied. |
| **IT Service Owner** | Validates operational support model, monitoring, and service-level readiness. |
| **AI Governance Council (AIGC)** | Reviews AI systems for ISO/IEC 42001 alignment, risk classification, and compliance readiness. |
| **Change Advisory Board (CAB)** | Reviews change records, rollback plans, and post-implementation validation evidence. |
| **Internal Audit** | Periodically reviews AIS outcomes and verifies adherence to COBIT BAI07 and CSA CCM CCC-01, CCC-02, and CCC-05 controls. |

---

## 4. Policy statements

### 4.1 Acceptance framework

4.1.1 All systems, services, and AI models must complete the AIS process prior to entering production.

4.1.2 Acceptance reviews must verify compliance with design, security, privacy, and operational standards.

4.1.3 No service must be deployed to production without documented AIS approval by the CIO and CISO.

### 4.2 Readiness review

4.2.1 A Readiness Review must confirm that:

- Functional and non-functional requirements have been met.
- Security testing and vulnerability remediation are complete.
- Backout and recovery procedures have been validated.
- Documentation, monitoring, and service support plans are in place.

4.2.2 AI systems must include risk tier classification and AI Impact Assessment results prior to approval.

### 4.3 Risk and compliance validation

4.3.1 AIS submissions must include risk assessment outcomes aligned with NIST SP 800-37 RMF Steps 4 to 6.

4.3.2 Security and privacy validation must include evidence from penetration testing, code reviews, and compliance checks.

4.3.3 AI solutions must demonstrate conformance to ISO/IEC 42001 §8 and the AI Security and Risk Standard.

### 4.4 AI risk classification and impact validation

4.4.1 All AI systems must be classified according to the organizational AI risk taxonomy: Minimal, Limited, High, or Unacceptable.

4.4.2 High-risk AI systems require additional ethical and safety validation by the AIGC prior to deployment.

4.4.3 AI Impact Assessments must evaluate transparency, fairness, and explainability per ISO/IEC 42005:2025 and EU AI Act Annex IV.

### 4.5 Documentation and evidence

4.5.1 Each AIS submission must include:

- Solution architecture and configuration documentation.
- Security and compliance test results.
- Risk register entries and mitigation evidence.
- Operational support procedures and monitoring dashboards.
- AI validation reports where applicable.

4.5.2 All AIS evidence must be stored in the central compliance repository with version control and audit traceability.

### 4.6 Approval and sign-off

4.6.1 The CIO provides final authorization for service go-live after confirming successful completion of all reviews.

4.6.2 The CISO and AIGC must co-approve any AI-related AIS submission.

4.6.3 The CAB must authorize the final change release prior to deployment.

### 4.7 Post-implementation review

4.7.1 A review must occur within 30 days of deployment to evaluate system stability, incident trends, and user feedback.

4.7.2 Lessons learned must be captured in the Continuous Improvement Register and shared with project teams.

4.7.3 Deficiencies identified post-implementation must trigger corrective action plans and potential rollback where required.

### 4.8 Continual improvement

4.8.1 The AIS process must be reviewed annually to reflect updated frameworks, emerging risks, and AI compliance changes.

4.8.2 Performance metrics (time-to-acceptance, post-implementation incidents, audit findings) must be analyzed quarterly.

4.8.3 Feedback loops must ensure that alignment with COBIT BAI07 and CSA CCM CCC-01, CCC-02, and CCC-05 maturity progression is maintained.

---

## 5. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8: AI Management System Operation | AI acceptance and risk classification |
| ISO/IEC 27001:2022 | Annex A.5.36 to A.5.37 | Change and handover controls |
| NIST SP 800-37 Rev. 2 | RMF Step 6: Authorize the System | Risk-based production authorization |
| COBIT 2019 | BAI07: Manage Change Acceptance and Transitioning | Controlled transition and handover |
| COBIT 2019 | DSS01: Manage Operations | Operational readiness validation |
| CSA CCM v4.1 | CCC-01 Change Management Policy and Procedures; CCC-02 Quality Testing; CCC-05 Change Agreements | Controlled change acceptance, readiness testing, and handover sign-off |
| OECD AI Principles | Safety and Accountability | AI readiness and impact validation |
| EU AI Act | Annex III and Annex IV | High-risk AI system acceptance criteria |

---

**End of Document**
