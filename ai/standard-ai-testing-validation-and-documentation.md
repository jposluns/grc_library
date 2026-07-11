# AI Testing, Validation and Documentation Standard

**Document Title:** AI Testing, Validation and Documentation Standard\
**Document Type:** Standard\
**Version:** 1.0.4\
**Date:** 2026-07-11\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI framework or regulatory change\
**Repository Path:** [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the mandatory requirements for testing, validating, and documenting artificial intelligence systems throughout their lifecycle. It ensures that AI models deployed by the organization are technically sound, ethically validated, explainable, and compliant with applicable standards and regulations before and after deployment.

The standard aligns with ISO/IEC 42001 §8, ISO/IEC 42005:2025 (AI system impact assessment), ISO/IEC TS 25058:2024 and ISO/IEC 25059:2023 (AI quality evaluation and the Systems and software Quality Requirements and Evaluation (SQuaRE) AI quality model), NIST AI RMF, NIST IR 8312 (explainability principles), ISO/IEC TR 24027:2021 (bias in AI systems), EU AI Act Annex IV, OWASP LLM Top 10, and the NIST AI 100-2e2025 adversarial machine-learning taxonomy.

---

## 2. Scope

Applies to all AI systems, machine learning models, generative AI tools, and automated decision-making systems developed, procured, or deployed by the organization. Includes both internally developed and third-party AI systems integrated into operational workflows.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Approves testing standards; reviews validation outcomes for high-risk systems. |
| **CISO** | Ensures that AI security testing is integrated into validation gates. |
| **AI Development / Data Science Teams** | Execute model testing, validation, and documentation requirements. |
| **QA and Testing Teams** | Validate AI system behaviour against defined acceptance criteria. |
| **Internal Audit** | Audits adherence to this standard annually. |

---

## 4. AI system documentation requirements

All AI systems must maintain current documentation covering:

| Document | Content Required |
| --- | --- |
| **Model Card** | Model purpose, inputs, outputs, intended use, out-of-scope uses, performance metrics |
| **AI Impact Assessment** | Risk tier, bias analysis, fairness evaluation, privacy impact, affected stakeholders |
| **Training Data Record** | Data sources, preprocessing steps, known limitations, consent and provenance |
| **Validation Report** | Test methodology, performance benchmarks, bias test results, robustness evaluation |
| **Deployment Record** | Target environment, integration points, monitoring configuration, rollback plan |
| **Change Log** | Version history, retraining events, performance drift events, incident history |

High-risk AI systems (EU AI Act Annex III) must maintain technical documentation per EU AI Act Annex IV.

---

## 5. Pre-deployment testing requirements

All AI systems must pass the following testing gates before production deployment:

### 5.1 Functional validation

- Accuracy, precision, recall, and F1 score meet defined acceptance thresholds.
- Output consistency verified across representative input distributions.
- Edge case and adversarial input handling documented and tested; robustness is evaluated as the model's ability to maintain functional correctness under unseen, biased, adversarial, or invalid inputs, external interference, and varying environmental conditions (ISO/IEC 25059:2023 §5.5).
- Functional testing applies methods appropriate to the model, drawn from the AI quality-evaluation methods of ISO/IEC TS 25058:2024 §6.2: metamorphic testing, benchmarking, expert panels, scenario and simulated-environment testing, and field trials. A distinct back-testing phase re-tests the selected model on a held-out testing dataset before deployment.

### 5.2 Bias and fairness testing

- Fairness evaluated with one or more metrics selected for the context from ISO/IEC TR 24027:2021 Clause 7: demographic parity (§7.5), equalized odds (§7.3), equality of opportunity (§7.4), and predictive equality (§7.6), each grounded in the confusion-matrix basis (§7.2), evaluated across protected groups.
- Bias mitigation techniques documented and validated.
- Residual bias below defined acceptable thresholds; residual risk documented.

### 5.3 Explainability validation

- Explanations generated for representative model decisions.
- Explainability method appropriate to deployment context (SHAP, LIME, or equivalent).
- Output interpretable by the intended decision-making audience (the meaningful principle, NIST IR 8312 §2.2).
- Explanation accuracy assessed as distinct from decision accuracy: the explanation correctly reflects the reason the system generated its output, not merely whether the output is correct (NIST IR 8312 §2.3).
- The model's knowledge limits declared: the conditions under which it is designed to operate, and the confidence threshold below which it should abstain, defer, or flag that its output is unreliable (NIST IR 8312 §2.4).

### 5.4 Security testing

- Adversarial robustness testing performed against the attack taxonomy of NIST AI 100-2e2025: for predictive AI, evasion, poisoning, and privacy attacks (the last including model extraction); for generative AI, supply-chain poisoning, direct prompting (including information extraction), and indirect prompt injection.
- AI system tested against the OWASP LLM Top 10 where applicable.
- Prompt injection and data leakage risks assessed for generative AI systems.
- Model outputs do not expose training data or confidential system information.

### 5.5 Privacy testing

- Personal data processing confirmed within declared scope.
- Data minimization and purpose limitation validated.
- PII outputs reviewed and masked where required.

---

## 6. Post-deployment monitoring requirements

Deployed AI systems must be monitored continuously for:

| Metric | Monitoring Requirement |
| --- | --- |
| Performance drift | Automated alerts when accuracy drops below defined threshold |
| Bias drift | Monthly demographic parity review for high-risk systems |
| Input distribution shift | Statistical monitoring of input feature distributions |
| Output anomalies | Automated alerts for unusual output patterns or error rates |
| Security events | AI-specific security events logged to SIEM |

Material performance degradation triggers model review and potential retraining per the AI Model Lifecycle Management Procedure.

---

## 7. Retraining and update validation

AI models undergoing retraining or significant update must complete:

- Regression testing against the original validation test suite.
- Bias re-evaluation across all protected groups.
- Security re-testing if attack surface or input domain changed.
- Updated documentation before re-deployment.

---

## 8. Risk tier testing requirements

| Risk Tier | Additional Testing Requirements |
| --- | --- |
| **Minimal** | Functional validation and basic documentation only |
| **Limited** | Functional + bias testing + explainability validation |
| **High** | All of the above + security testing + AI Impact Assessment + AIGC review |
| **Unacceptable** | Deployment prohibited |

---

## 9. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8: Operation | AI system operation and validation |
| ISO/IEC 42005:2025 | AI system impact assessment | AI risk and bias assessment |
| EU AI Act (2024) | Annex IV: Technical Documentation | High-risk AI documentation |
| NIST AI RMF (2023) | MAP, MEASURE functions | AI testing and measurement |
| OWASP LLM Top 10 | LLM-specific vulnerabilities | Generative AI security testing |
| ISO/IEC TS 25058:2024 | §5 evaluation methodology; §6.2 functional test methods | AI quality-evaluation methods (Section 5.1) |
| ISO/IEC 25059:2023 | §5.5 Robustness (SQuaRE AI quality model) | Robustness and quality characteristics (Section 5.1) |
| NIST IR 8312 | §2.1 to §2.4 four principles of explainable AI | Explanation accuracy and knowledge limits (Section 5.3) |
| ISO/IEC TR 24027:2021 | Clause 7 fairness metrics | Bias and fairness testing (Section 5.2) |
| NIST AI 100-2e2025 | Adversarial machine-learning taxonomy | Adversarial attack taxonomy for security testing (Section 5.4) |
| ISO/IEC 27001:2022 | Annex A | Security controls for AI systems |

---

**End of Document**
