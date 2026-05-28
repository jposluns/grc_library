# AI Audit Procedure

**Document Title:** AI Audit Procedure  
**Document Type:** Procedure  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Officer  
**Approving Authority:** Chief Information Officer  
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)  
**Classification:** Public  
**Category:** AI Governance  
**Review Frequency:** Annual and upon material AI framework or regulatory change  
**Repository Path:** [`ai/procedure-ai-audit.md`](procedure-ai-audit.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This procedure defines the process for planning, executing, reporting, and following up on AI audits across the organisation's AI system inventory. AI audits verify that deployed AI systems operate within defined ethical, technical, and compliance boundaries, and that the AI Management System (AIMS) remains effective and improving.

---

## Scope

Applies to all AI systems in the AI System Inventory, including production AI models, automated decision-making systems, and generative AI tools. AI audits may be conducted internally by Internal Audit or the AIGC, or externally by approved third-party auditors.

---

## Roles and Responsibilities

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Approves the annual AI audit plan; reviews findings and remediation plans. |
| **Internal Audit** | Leads internal AI audit execution; issues findings and tracks closures. |
| **CISO** | Participates in security-focused AI audit activities. |
| **AI System Owner** | Provides evidence; supports audit access; owns remediation actions. |
| **GRC Programme Manager** | Tracks audit findings in the CAPA Register. |

---

## 1. Audit Planning

1.1 The AI audit plan is prepared annually by Internal Audit in consultation with the AIGC.

1.2 AI systems are prioritised for audit based on:
- Risk tier (High-risk systems audited at minimum annually).
- Prior audit findings.
- Material changes since last audit.
- Regulatory requirements.

1.3 The annual AI audit plan is approved by the AIGC and reported to the ERC.

---

## 2. Audit Scope Definition

2.1 For each AI audit, the scope defines:
- AI system(s) under review.
- Audit objectives (ethics, accuracy, security, compliance, or full-scope).
- Audit criteria: ISO/IEC 42001, EU AI Act, NIST AI RMF, OWASP LLM Top 10, and/or internal standards.
- Evidence required.
- Audit timeline.

2.2 The AI System Owner is notified of the audit scope and timeline at least 10 business days before fieldwork begins.

---

## 3. Evidence Collection

3.1 Auditors collect evidence including:
- Model documentation (Model Card, AI Impact Assessment, Training Data Record).
- Validation reports and test results.
- Bias and fairness testing outputs.
- Explainability evaluation records.
- Security testing records.
- Monitoring logs and drift alerts.
- Access control and change management records.
- Post-incident review outputs (if applicable).

3.2 Evidence is collected through document review, system access, and interviews with AI system owners and developers.

---

## 4. Audit Execution

4.1 Auditors assess evidence against audit criteria and note:
- Conformities: requirements met with evidence.
- Observations: areas for improvement without material risk.
- Minor nonconformities: partial or incomplete compliance.
- Major nonconformities: significant failure to meet requirements.

4.2 Auditors validate that bias mitigation, explainability, and safety controls function as documented.

4.3 For high-risk AI systems, auditors independently verify EU AI Act Annex IV documentation completeness.

---

## 5. Audit Reporting

5.1 A draft AI Audit Report is issued to the AI System Owner within 10 business days of fieldwork completion.

5.2 The AI System Owner has 5 business days to submit factual corrections.

5.3 The final AI Audit Report is issued and submitted to the AIGC.

5.4 Reports are retained in the compliance document repository for a minimum of 5 years.

**Report contents:**
- Executive summary.
- Scope and criteria.
- Findings (conformities, observations, nonconformities).
- Risk ratings for nonconformities.
- Recommended corrective actions.

---

## 6. Corrective Action and Follow-Up

6.1 All nonconformities are logged in the CAPA Register.

6.2 The AI System Owner assigns a responsible party and due date for each corrective action.

6.3 Major nonconformities require corrective action plans within 10 business days.

6.4 Minor nonconformities require remediation within the timeframe agreed with Internal Audit.

6.5 Internal Audit verifies closure with objective evidence before closing each CAPA.

6.6 Persistent or unresolved major nonconformities are escalated to the ERC.

---

## 7. AIGC Reporting

7.1 Internal Audit presents an AI audit summary to the AIGC quarterly.

7.2 The quarterly summary covers: audits completed, open findings, overdue CAPAs, and systemic issues.

7.3 Annual AI audit outcomes are included in the AI Governance Performance Report to the ERC and Board.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §9.2 — Internal Audit | AI management system audit |
| ISO 19011:2018 | Guidelines for Auditing Management Systems | Audit methodology |
| EU AI Act (2024) | Article 43 — Conformity Assessment | High-risk AI audit obligations |
| NIST AI RMF (2023) | MEASURE function | AI audit and measurement |
| COBIT 2025 | MEA02 — Manage System of Internal Controls | Internal control assurance |

---

**End of Document**
