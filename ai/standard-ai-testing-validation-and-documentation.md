# AI Testing, Validation and Documentation Standard

**Document Title:** AI Testing, Validation and Documentation Standard\
**Document Type:** Standard\
**Version:** 1.0.15\
**Date:** 2026-10-27\
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

The standard aligns with ISO/IEC 42001:2023 §8, ISO/IEC 42005:2025 (AI system impact assessment), ISO/IEC TS 25058:2024 and ISO/IEC 25059:2023 (AI quality evaluation and the Systems and software Quality Requirements and Evaluation (SQuaRE) AI quality model), NIST AI RMF 1.0, NIST AI 600-1 (Generative AI Profile measurement actions), NIST IR 8312 (explainability principles), ISO/IEC TR 24027:2021 (bias in AI systems), ISO/IEC TR 24029-1:2021 (statistical robustness assessment), EU AI Act Annex IV, OWASP LLM Top 10, and the NIST AI 100-2e2025 adversarial machine-learning taxonomy.

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
| **AI Impact Assessment** | Impact level, bias analysis, fairness evaluation, privacy impact, affected stakeholders |
| **Training Data Record** | Data sources, preprocessing steps, known limitations, consent and provenance |
| **Validation Report** | Test methodology, performance benchmarks, bias test results, robustness evaluation, uncertainty statements and sample sizes (Section 5.6), run counts for non-deterministic systems, contamination record, evaluator agreement |
| **Deployment Record** | Target environment, integration points, monitoring configuration, rollback plan |
| **Change Log** | Version history, retraining events, performance drift events, incident history |

High-risk AI systems (EU AI Act Annex III) maintain technical documentation per EU AI Act Annex IV. As a statutory Chapter III, Sections 1 to 3 obligation, this applies from 2 December 2027 for Article 6(2)/Annex III systems and from 2 August 2028 for Article 6(1)/Annex I systems (Article 113, third paragraph, point (c), as replaced by Regulation (EU) 2026/1744); earlier documentation is an internal control.

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

### 5.6 Evaluation uncertainty and result reporting

These requirements apply to every quantitative evaluation result relied on for a testing gate under Sections 5.1 to 5.5 and Section 7. They govern the statistical precision of evaluation results; they are distinct from the per-output confidence thresholds of the knowledge-limits declaration in Section 5.3, which is unchanged.

- **Uncertainty statement.** Each quantitative evaluation result relied on for a gate must report the number of evaluated items, a measure of the result's statistical uncertainty (such as a confidence interval), and the method used to derive that measure. The confidence level is set by the organization and recorded before the evaluation runs. A point estimate reported without an uncertainty statement must not be used to pass a gate. This implements the NIST AI RMF 1.0 §5.3 MEASURE expectation of performance assessment methodologies with associated measures of uncertainty and formalized reporting of results.
- **Subgroup sample size.** Where results are disaggregated across subgroups (Section 5.2), the number of evaluated items must be reported per subgroup. A subgroup whose sample is too small to support the organization-set precision must be recorded as not measured, not as passed (NIST AI RMF 1.0 MEASURE 1.1: characteristics that will not or cannot be measured are documented; ISO/IEC 42001:2023 Annex B.6.2.6: evaluation criteria inform the amount of data used in assessment).
- **Run variance.** Where outputs are non-deterministic (sampled decoding, agentic workflows, or non-deterministic inference), the evaluation must be repeated across multiple runs, and the report must state the number of runs, the sampling or seed configuration, and the spread of results across runs (NIST AI 600-1 MS-2.13-001: statistical variance in applied metrics is measured or estimated and documented; Singapore IMDA Agentic AI framework §2.3.2: repeated runs to check stability). Both anchors are scoped (NIST AI 600-1 to generative AI; the IMDA framework to agentic AI); applying this requirement to every non-deterministic system is an organizational extension of those anchors.
- **Comparisons.** A claim that one model or version outperforms another, or has not regressed (Section 7), must rest on a comparison over the same evaluation items that reports the measured difference together with its uncertainty or an appropriate statistical test. Two independently reported point estimates are not a comparison. ISO/IEC TR 24029-1:2021 §5.1 reaches a robustness decision through a statistical test on a selected metric against thresholds; the paired-comparison requirement is the organization's extension of that discipline.
- **Contamination record.** Each benchmark or evaluation dataset must carry a record of the check performed for overlap between evaluation data and training or fine-tuning data. For a third-party model, the provider's contamination disclosure is recorded; the absence of a disclosure is recorded as a documented gap (NIST AI 600-1 MS-2.11-001: benchmark assumptions and limitations documented, including actual or possible training/test data cross contamination; ISO/IEC TS 25058:2024 §6.2: training, validation, and testing datasets built from different data).
- **Evaluator agreement.** Where scores are produced by human raters or by a grading model, the report must state the scoring rubric, the number of raters, and an agreement measure such as inter-annotator agreement (ISO/IEC TR 24029-1:2021 §5.2.4.2: Cohen's kappa as an inter-annotator agreement measure; NIST AI 600-1 MS-2.8-002: instructions given to annotators documented). For a grading model, its agreement with a human-scored sample must be reported; this is an organizational extension without an external anchor.
- **External validity statement.** The evaluation report must state how the evaluation conditions differ from the deployment context (NIST AI RMF 1.0 §3.1: accuracy measurements paired with clearly defined, realistic, representative test sets and test-methodology details). Evidence-sufficiency grading of this statement is owned by [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) (deployment-representative demonstration) and is not restated here.

### 5.7 Treatment of inconclusive results

- A quantitative result passes its threshold only when its whole reported uncertainty range lies on the passing side of the threshold, or when an organization-set decision rule recorded before the evaluation runs provides otherwise (ISO/IEC 42001:2023 Annex B.6.2.4: the AI system is evaluated against documented evaluation criteria, including acceptable error rates).
- A result whose uncertainty range straddles its threshold is **inconclusive**. It must not be reported as a pass. An inconclusive result may proceed to conditional approval by the AIGC with a recorded rationale and recorded conditions, or be returned for further evaluation.
- The safety-margin treatment of measurement uncertainty in the EU GPAI Code of Practice (Safety and Security Chapter) corroborates this rule from the general-purpose AI systemic-risk context; that instrument is voluntary and scoped to GPAI models with systemic risk.

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
| **Minimal** | Functional validation and basic documentation only; from Section 5.6, the evaluation report states the sample size and the test-set contamination status only |
| **Limited** | Functional + bias testing + explainability validation + the full Section 5.6 and Section 5.7 requirements |
| **High** | All of the above + security testing + AI Impact Assessment + AIGC review |
| **Unacceptable** | Deployment prohibited |

---

## 9. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8.1 (Operational planning and control); A.6.2.4 (AI system verification and validation); A.6.2.6 (AI system operation and monitoring) | AI system operation and validation |
| ISO/IEC 42005:2025 | AI system impact assessment | AI risk and bias assessment |
| EU AI Act (2024) | Annex IV: Technical Documentation | High-risk AI documentation |
| NIST AI RMF 1.0 (2023) | MEASURE 1.1 (measurement approaches and metrics), MEASURE 2.1 (test sets, metrics, and tools) | AI testing and measurement |
| NIST AI RMF 1.0 (2023) | §5.3 MEASURE function narrative (performance assessment with associated measures of uncertainty and formalized reporting); §3.1 (accuracy paired with representative test sets; disaggregated results) | Evaluation uncertainty and result reporting (Sections 5.6, 5.7) |
| NIST AI 600-1 (Generative AI Profile) | MS-2.11-001 (benchmark limitations, including training/test data cross contamination), MS-2.13-001 (measurement error and statistical variance), MS-2.8-002 (annotator instructions documented) | Contamination record, run variance, and evaluator agreement (Section 5.6) |
| EU GPAI Code of Practice, Safety and Security Chapter (July 2025) | Glossary definition of internal validity (sample sizes, statistical significance and power, train-test separation, repeated runs, inter-annotator agreement); Appendix 3.1 (rigorous model evaluations); safety margin for measurement uncertainty | Corroborative basis for Sections 5.6 and 5.7; voluntary instrument scoped to GPAI models with systemic risk |
| ISO/IEC TR 24029-1:2021 | §5.1 (statistical test to reach a robustness decision over thresholds); §5.2.4.2 (Cohen's kappa) | Statistical decision and evaluator-agreement basis (Section 5.6) |
| ISO/IEC 42001:2023 | Annex B.6.2.4 (documented evaluation criteria, including acceptable error rates, and evaluation against them); Annex B.6.2.6 (evaluation data and the amount of data used in assessment) | Threshold decision rules and sample sizing (Sections 5.6, 5.7) |
| ISO/IEC 23894:2023 | §6.3.4, Table 4 (understanding uncertainty across the AI system; measurement methods consistently evaluated for effectiveness) | Uncertainty awareness in evaluation (Section 5.6) |
| OWASP LLM Top 10 (2026) | LLM01:2026 to LLM10:2026 (all ten entries) | Generative AI security testing |
| ISO/IEC TS 25058:2024 | §5 evaluation methodology; §6.2 functional test methods | AI quality-evaluation methods (Section 5.1); separate training, validation, and testing data (Section 5.6) |
| ISO/IEC 25059:2023 | §5.5 Robustness (SQuaRE AI quality model) | Robustness and quality characteristics (Section 5.1) |
| NIST IR 8312 | §2.1 to §2.4 four principles of explainable AI | Explanation accuracy and knowledge limits (Section 5.3) |
| ISO/IEC TR 24027:2021 | Clause 7 fairness metrics | Bias and fairness testing (Section 5.2) |
| NIST AI 100-2e2025 | Adversarial machine-learning taxonomy | Adversarial attack taxonomy for security testing (Section 5.4) |
| ISO/IEC 27001:2022 | Annex A | Security controls for AI systems |
| ETSI EN 304 223 V2.1.1 | Provisions 5.2.5-1, 5.2.5-2 (Principle 9) | Security-assessment testing before release, and System Operator testing before deployment |
| Singapore IMDA Model AI Governance Framework for Agentic AI (v1.5, 2026) | §2.3.2 - agentic-system testing: complete workflows, policy compliance, tool-call correctness, agents individually and together, realistic environments, repeated stochastic runs | Voluntary governance alignment for agentic-system test coverage (scoped to agentic AI) and repeated-run variance reporting (Section 5.6) |

---

**End of Document**
