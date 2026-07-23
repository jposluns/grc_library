# AI Model Lifecycle Management Procedure

**Document Title:** AI Model Lifecycle Management Procedure\
**Document Type:** Procedure\
**Version:** 1.0.5\
**Date:** 2026-07-23\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI framework or regulatory change\
**Repository Path:** [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the end-to-end lifecycle management process for AI models, from initial development or procurement through deployment, monitoring, retraining, and decommissioning. It ensures that every AI model in the organization's inventory is governed, documented, and reviewed throughout its operational life.

---

## Scope

Applies to all AI models and machine learning systems developed internally, procured from third parties, or operated as embedded components within business applications. Includes generative AI models, predictive models, classification systems, and automated decision engines.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Approves production deployment and decommissioning of AI models; reviews lifecycle governance. |
| **AI System Owner** | Accountable for model currency, performance, and compliance throughout lifecycle. |
| **AI Development / Data Science Teams** | Execute development, testing, training, and retraining activities. |
| **CISO** | Reviews security requirements at deployment and retraining gates. |
| **GRC Programme Manager** | Maintains the AI System Inventory and tracks lifecycle status. |

---

## 1. AI system inventory

1.1 The GRC Programme Manager maintains an AI System Inventory covering all AI models in use or under development.

1.2 Inventory records include: model name, version, owner, risk tier, deployment date, last review date, monitoring status, lifecycle stage, and the recorded performance thresholds (metric, floor value, and accountable owner) required at deployment by 4.5.

1.3 The inventory is reviewed and updated at minimum quarterly by the GRC Programme Manager.

---

## 2. Development and pre-deployment

2.1 New AI model development must be registered in the AI System Inventory at inception.

2.2 Development follows the AI Testing, Validation and Documentation Standard.

2.3 Mandatory pre-deployment gates:

| Gate | Requirement |
| --- | --- |
| Risk Classification | AI risk tier assigned by AIGC or delegated owner |
| AI Impact Assessment | Completed and reviewed for High-risk systems |
| Technical Validation | All testing requirements from the AI Standard passed |
| Security Review | CISO sign-off on security test results |
| Documentation | Model Card, Validation Report, Deployment Record complete |
| AIGC Approval | Required for High-risk systems; delegated for Minimal/Limited |

2.4 Deployment to production must follow the Acceptance Into Service Policy.

---

## 3. Production deployment

3.1 Approved AI models are deployed via the change management process.

3.2 The Deployment Record is updated to include: deployment date, environment details, integration configuration, and monitoring configuration.

3.3 Monitoring alerts are configured per the AI Testing, Validation and Documentation Standard before go-live.

---

## 4. Ongoing monitoring

4.1 AI System Owners review model performance monitoring outputs at minimum monthly.

4.2 Monitoring covers: accuracy/performance metrics, bias drift, input distribution shift, and output anomalies.

4.3 Performance below defined thresholds triggers a model review. Outcomes are: continue (document rationale), retrain, restrict scope, or decommission.

4.4 Material monitoring findings are reported to the AIGC at the next quarterly meeting.

4.5 The performance thresholds referenced in 4.3 (and the retraining threshold in 5.1) are defined per model, the metric, the floor value, and the accountable owner, and are recorded in the model's entry in the AI System Inventory at deployment; a model with no recorded threshold does not enter production. This turns "defined thresholds" from an assumption into a deployment obligation, aligned with ISO/IEC 42001 Section 9 (performance evaluation).

4.6 For deployments that apply automated continuous learning without human interaction, an automated rollback process is enabled at defined performance thresholds, defaulting to a safe alternative model on a threshold breach (ISO/IEC 5338:2023 Section 6.4.14, continuous validation).

4.7 Contingency plans for model unavailability, performance deterioration, or outright failure, with the associated escalation procedures, are defined and recorded.

---

## 5. Retraining and model updates

5.1 Retraining is triggered by: scheduled retraining cycle, performance drift below threshold, significant change in input data distribution, or post-incident review recommendation.

5.2 Retraining follows the same testing and validation requirements as pre-deployment.

5.3 Retrained models are versioned, documented, and subject to AIGC review where the model is High-risk.

5.4 The AI System Inventory is updated to reflect the new version and retraining date.

---

## 6. Annual review

6.1 All AI models in production undergo an annual review.

6.2 Review assesses: continued business need, performance against current benchmarks, regulatory compliance status, and security posture.

6.3 Review outcomes (continue, retrain, decommission) are documented and reported to the AIGC.

---

## 7. Decommissioning

7.1 Decommissioning is initiated when an AI model is: no longer required, replaced by a new model, or declared non-compliant and not remediable.

7.2 Decommissioning checklist:

- [ ] AI System Owner and AIGC confirm decommission decision.
- [ ] All dependent systems and integrations identified and updated or removed.
- [ ] Training data and model artefacts disposed of per the Data Retention Schedule.
- [ ] Model monitoring disabled and alerts removed.
- [ ] AI System Inventory status updated to Decommissioned.
- [ ] Decommission record retained for audit purposes.
- [ ] Where the retired model may serve as a benchmark or fallback, the model and its documentation are retained for a defined period before disposal.

7.3 Training data and model artefacts containing personal data are disposed of per privacy obligations and the Records Retention and Destruction Standard.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8: Operation | AI model lifecycle governance |
| ISO/IEC 42001:2023 | §10: Improvement | Model performance monitoring and improvement |
| ISO/IEC 5338:2023 | AI system life cycle processes; §6.4.14 continuous validation | AI system lifecycle process model and automated rollback |
| OSFI Guideline E-23 (2025, effective 2027) | Model risk management: inventory, review triggers, decommission retention, unavailability contingency | Model-risk lifecycle governance, adopted sector-neutrally |
| EU AI Act (2024) | Article 9: Risk Management System | Ongoing AI risk management |
| NIST AI RMF (2023) | GOVERN, MAP, MEASURE, MANAGE functions | End-to-end AI lifecycle |
| COBIT 2019 | BAI09: Managed Assets | AI asset lifecycle management |

---

**End of Document**
