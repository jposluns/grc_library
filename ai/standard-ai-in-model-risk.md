# Standard: In Model Risk

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | In Model Risk Standard |
| **Document Type** | Standard |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Chief Compliance Officer (CCO) |
| **Approving Authority** | Chief Legal Officer and General Counsel (CLO/GC) |
| **Related Documents** | Framework: In Model Risk; Framework: AI Governance; Framework: AI System Audit and Certification; Standard: AI Lifecycle Governance |
| **Classification** | Internal |
| **Category** | Artificial Intelligence |
| **Review Frequency** | Annual |
| **Repository Path** | /ai/standard-ai-in-model-risk.md |
| **Confidentiality** | Internal Use Only |

---

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

---

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Risk Officer (CRO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Compliance Officer (CCO) |  |  |
| Chief Legal Officer / General Counsel (CLO/GC) |  |  |
| Chief Technology Officer (CTO) |  |  |
| Chair, AI Governance Council |  |  |

---

# Purpose

This standard defines mandatory requirements, controls, activities, and evidence obligations for the assessment and management of in model risk across artificial intelligence, machine learning, and large language model systems.

It operationalizes the In Model Risk Framework by establishing enforceable expectations for interpretability, robustness, alignment, lifecycle governance, and documentation.

This standard supports compliance with ISO 42001, ISO 23894, ISO 24028, NIST AI RMF, COBIT 2025, and CSA CCM v5.

---

# Scope

- Applies to all AI and ML models that impact business decisions, automated processes, workflows, or external outputs.  
- Applies to internally developed models, vendor supplied models, open source models, and fine tuned models.  
- Applies across the entire AI lifecycle, from problem definition through archival and decommissioning.  
- Applies to production systems, pilots, experimental systems used for business insight, and embedded AI functionalities in enterprise platforms.

---

# Mandatory Controls

The following controls are mandatory and must be implemented for every AI and ML system governed by this standard.

---

# 1 Interpretability Controls

## 1.1 Interpretability Baseline Requirement
All models must maintain a documented interpretability profile appropriate to their risk category.

## 1.2 Feature Attribution Evidence
All models must generate feature attribution evidence using at least one approved method:  
- SHAP  
- Integrated Gradients  
- LIME  

Evidence must be preserved as part of the model card and updated during each retraining cycle.

## 1.3 Representation and Embedding Analysis
Models using embeddings or latent variables must undergo representation analysis to detect bias, clustering anomalies, or harmful internal associations.

Reports must include:  
- visualization of embedding clusters  
- identification of sensitive attribute correlations  
- summary of potential semantic risks

## 1.4 Mechanistic Interpretability for High Risk Models
High risk models must include deeper interpretability analysis, such as neuron activation review or causal tracing, consistent with available tooling and platform capabilities.

---

# 2 Adversarial Evaluation Controls

## 2.1 Adversarial Test Suite Requirement
Each model must undergo adversarial testing using a formally documented evaluation suite appropriate to its architecture.

## 2.2 Gradient and Perturbation Testing
Models must be tested using minimal perturbation adversarial methods to measure sensitivity and brittleness.

## 2.3 Red Team Evaluation
High risk and general enterprise systems must undergo structured red team testing that includes:  
- prompt conflict tests  
- chain of thought disruption tests  
- misdirection attempts  
- counterfactual reversals  
- malicious input exposure  

All findings must be documented and remediated or formally risk accepted.

## 2.4 Out of Distribution Evaluation
Models must be evaluated against out of distribution inputs to ensure stable behavior and detect unsafe generalization patterns.

---

# 3 Goal Alignment and Behavioral Controls

## 3.1 Alignment Validation Requirement
All models must be evaluated for alignment with intended functional purpose, ethical constraints, and documented enterprise guidelines.

## 3.2 Behavioral Drift Monitoring
Deployed models must include drift detection mechanisms that monitor:  
- model outputs  
- internal distribution shifts  
- anomaly indicators  
- alignment deviations  

Alerts must be logged and escalated.

---

# 4 Data and Training Controls

## 4.1 Training Data Documentation
Training data, data sources, and data transformations must be fully documented.

## 4.2 Sensitive Attribute Review
Datasets must be evaluated for the presence of sensitive attributes and potential correlation risks.

## 4.3 Provenance and Lineage Requirement
All data used in model training must include provenance documentation and lineage tracking through the lifecycle.

---

# 5 Lifecycle Governance Controls

## 5.1 Model Card Requirement
Every model must have a complete model card prior to deployment, including:  
- purpose  
- architecture  
- training sources  
- evaluation results  
- interpretability findings  
- adversarial evaluation summaries  
- limitations  
- risk statements

## 5.2 System Card Requirement
Models embedded in broader systems must include a system card that summarizes system wide risks and interactions.

## 5.3 Deployment Approval Requirement
Models cannot be deployed until approved by:  
- Model Owner  
- AI Governance Council  
- Compliance and Legal  
- Security (for adversarial review)

## 5.4 Documentation Integrity
All lifecycle documentation must be stored in an immutable repository with version control.

---

# 6 Monitoring and Re Evaluation Controls

## 6.1 Continuous Monitoring
Models must be continuously monitored for:  
- drift  
- degradation  
- anomalous behaviour  
- adversarial indicators

## 6.2 Periodic Re Evaluation
All models must undergo full re evaluation at least annually or following:  
- a significant architecture change  
- retraining  
- data pipeline modifications  
- material incident

## 6.3 Incident Response Integration
Model failures, anomalous events, or adversarial findings must trigger incident response procedures and be logged in the enterprise risk system.

---

# 7 Documentation and Evidence Requirements

The following artefacts must be created and maintained:

- model card  
- system card  
- interpretability report  
- adversarial testing report  
- representation and embedding analysis  
- drift monitoring logs  
- approval and change logs  
- retraining and evaluation summaries  
- residual risk acceptance statements  

All evidence must be retained for the full lifecycle of the model and archived according to the AI Lifecycle Governance Standard.

---

# Roles and Responsibilities

## Model Owner
Ensures compliance with all controls, completes documentation, and manages ongoing risk.

## AI Governance Council
Provides oversight, evaluates risk acceptance, and ensures adherence to enterprise principles.

## Compliance and Legal
Validates compliance with applicable legislation and regulatory requirements.

## Security and Risk Management
Conducts adversarial testing and manages related security and safety risks.

## Internal Audit
Verifies that mandatory controls and documentation have been implemented and maintained.

---

## Definitions

Key terms and acronyms used in this document are defined in the **Key Terms and Definitions Register**.

Definitions of organizational roles and authorities are provided in the **Role Authority Register**.

---

**End of Document**
