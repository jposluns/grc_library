# AI Evaluation Procedure

**Document Title:** AI Evaluation Procedure\
**Document Type:** Procedure\
**Version:** 1.0.7\
**Date:** 2026-07-11\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI framework or regulatory change\
**Repository Path:** [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This procedure defines the process for evaluating AI systems before initial deployment, after significant changes, and at scheduled review intervals. AI evaluation provides the evidence base for deployment approval, ongoing governance, and risk management decisions made by the AI Governance Council.

---

## Scope

Applies to all AI systems under consideration for deployment, as well as deployed AI systems undergoing major retraining or scope changes. Includes both internally developed models and third-party AI solutions.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Reviews evaluation outcomes; approves or rejects High-risk AI deployments. |
| **AI System Owner** | Commissions evaluation; provides system access and documentation. |
| **AI Development / Data Science Teams** | Execute technical evaluation activities. |
| **CISO** | Reviews security evaluation outcomes. |
| **Data Protection Officer (DPO)** | Reviews privacy evaluation outcomes. |

---

## 1. Evaluation triggers

An AI evaluation is required when:

| Trigger | Evaluation Scope |
| --- | --- |
| New AI system proposed for deployment | Full evaluation |
| Major model retraining (>20% of training data changed) | Full evaluation |
| Deployment scope expansion (new use case or affected population) | Full evaluation |
| AI incident with material impact | Targeted evaluation of affected capability |
| Scheduled annual review | Abbreviated evaluation (performance and bias checks) |
| Regulatory or framework change affecting the system | Targeted compliance evaluation |

---

## 2. Evaluation dimensions

### 2.1 Technical performance

- Evaluate accuracy, precision, recall, F1, or relevant task-specific metrics against defined thresholds.
- Test on a held-out evaluation dataset representative of the deployment population.
- Evaluate performance consistency across input subgroups.
- Document performance degradation conditions and edge cases.
- Apply the AI quality-evaluation methods of ISO/IEC TS 25058:2024 §6.2 (metamorphic testing, benchmarking, scenario and simulated-environment testing, field trials, and a back-testing phase on a held-out dataset); a residual error rate is expected and may trade off against robustness and performance efficiency (ISO/IEC 25059:2023 §5.4).

### 2.2 Fairness and bias

- Evaluate fairness with one or more ISO/IEC TR 24027:2021 Clause 7 metrics selected for the context: demographic parity (§7.5), equalized odds (§7.3), equality of opportunity (§7.4), or predictive equality (§7.6), across relevant protected groups.
- Quantify bias magnitude; compare against acceptable threshold.
- Validate effectiveness of bias mitigation techniques applied during training.
- Document residual bias with risk acceptance rationale.

### 2.3 Explainability

- Validate that explanations are generated for a representative sample of outputs.
- Assess explanation quality: are explanations meaningful to the intended audience (NIST IR 8312 §2.2)?
- Assess explanation accuracy (the explanation reflects the actual reason for the output, distinct from decision accuracy) and declare the model's knowledge limits (its operating conditions and the confidence threshold below which it should abstain or defer), per NIST IR 8312 §2.3 and §2.4.
- For High-risk systems: confirm explanation methodology meets ISO/IEC 42001 and EU AI Act requirements.

### 2.4 Security

- Adversarial robustness: test resistance to the NIST AI 100-2e2025 attack classes (for predictive AI, evasion, poisoning, and privacy attacks including model extraction; for generative AI, supply-chain poisoning, direct prompting, and indirect prompt injection), evaluating the model's ability to maintain functional correctness under adversarial and invalid inputs (ISO/IEC 25059:2023 §5.5).
- For generative AI: test for prompt injection, data leakage, and hallucination risks.
- Validate output filtering and guardrails where applicable.
- Confirm integration security: authentication, authorization, and API security controls.

### 2.5 Privacy

- Confirm personal data processing scope matches declared purpose.
- Validate data minimization and anonymization techniques.
- Assess re-identification risk for model outputs involving personal data.
- Confirm consent or legal basis for personal data used in training and inference.

### 2.6 Compliance

- Verify alignment with applicable regulations: GDPR, AIDA (Canadian AI and Data Act), EU AI Act.
- Confirm risk tier classification is current and accurate.
- Validate that required documentation (Model Card, AI-IA) is complete.

---

## 3. Evaluation process

### Step 1: Evaluation planning (5 business days before evaluation)

- Define evaluation scope, timeline, and responsible parties.
- Confirm test data, evaluation tooling, and access requirements.
- Notify AIGC of upcoming evaluation.

### Step 2: Technical evaluation (per agreed timeline)

- Execute all evaluation dimensions defined in Section 2.
- Document results with supporting evidence (test outputs, logs, screenshots).

### Step 3: Draft evaluation report (within 5 business days of evaluation completion)

Report includes:
- Executive summary.
- Scores for each evaluation dimension.
- Pass/fail status against defined thresholds.
- Identified risks and recommended mitigations.
- Overall recommendation: Deploy / Deploy with conditions / Do not deploy.

### Step 4: AI governance council review

- Evaluation report submitted to AIGC for review.
- AIGC reviews within 10 business days for High-risk systems.
- AIGC issues approval, conditional approval, or rejection.

### Step 5: Deployment or remediation

- Approved systems proceed through the Acceptance Into Service Policy.
- Conditionally approved systems address specified conditions before deployment.
- Rejected systems require material changes and full re-evaluation. "Material" is defined by the Material change thresholds table in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).

---

## 4. Evaluation report retention

Evaluation reports are retained in the compliance repository for the lifecycle of the AI system plus 5 years.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8: Operation | AI system evaluation and deployment |
| ISO/IEC 42005:2025 | AI system impact assessment | Risk and bias evaluation |
| ISO/IEC TS 25058:2024 | §5 evaluation methodology; §6.2 functional test methods | AI quality-evaluation methods (Section 2.1) |
| ISO/IEC 25059:2023 | §5.4 functional correctness; §5.5 robustness | AI system quality model (Sections 2.1, 2.4) |
| NIST IR 8312 | §2.2 to §2.4 explainability principles | Explanation accuracy and knowledge limits (Section 2.3) |
| ISO/IEC TR 24027:2021 | Clause 7 fairness metrics | Fairness and bias evaluation (Section 2.2) |
| EU AI Act (2024) | Article 9: Risk Management System | Evaluation obligations for high-risk AI |
| NIST AI RMF (2023) | MAP and MEASURE functions | AI evaluation methodology |
| OWASP LLM Top 10 | LLM-specific vulnerabilities | Generative AI security evaluation |

---

**End of Document**
