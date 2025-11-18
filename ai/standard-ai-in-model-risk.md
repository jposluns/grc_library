Document Title
In Model Risk Standard

Document Type
Standard

Version
0.0.1

Date
2025 November 18

Owner
Chief Compliance Officer

Approving Authority
Chief Legal Officer

Related Documents
In Model Risk Framework (framework-in-model-risk.md)
AI Governance Framework (framework-ai-governance.md)
AI System Audit and Certification Framework (framework-ai-system-audit-and-certification.md)
AI Lifecycle Governance Standard (standard-ai-lifecycle-governance.md)

Classification
Internal

Category
Artificial Intelligence

Review Frequency
Annual

Repository Path
/ai/standard-in-model-risk.md

Confidentiality
Public

---

## Purpose

This standard defines mandatory requirements, controls, and evidence obligations for assessing and managing in model risk across artificial intelligence, machine learning, and large language model systems. It operationalizes the In Model Risk Framework through enforceable expectations for interpretability, robustness, alignment, lifecycle governance, and documentation.

This standard supports alignment with ISO 42001, ISO 23894, ISO 24028, NIST AI RMF, COBIT 2025, and CSA CCM v5.

## Scope

This standard applies to all AI and machine learning models that affect business decisions, automated workflows, or external outputs. It applies to internally developed models, vendor-supplied models, open-source models, and fine-tuned models. Requirements apply across all lifecycle phases, from problem definition through archival and decommissioning, and to production systems, pilots, and embedded AI functionalities.

## Objectives

1. Establish enforceable controls for interpretability, robustness, alignment, and lifecycle governance.  
2. Ensure consistent and reliable internal model behaviour across AI systems.  
3. Define evidence and documentation required to maintain auditability.  
4. Support safe, ethical, and transparent deployment of AI capabilities.

## Mandatory Controls

### 1 Interpretability Controls

#### 1.1 Interpretability Baseline
All AI models must maintain a documented interpretability profile proportional to risk category.

#### 1.2 Feature Attribution Evidence
Models must generate attribution evidence using at least one approved technique such as SHAP, Integrated Gradients, or LIME. Evidence must be attached to the model card and refreshed during retraining.

#### 1.3 Representation and Embedding Analysis
Models using embeddings or latent variables must undergo structured representation analysis including:

- embedding cluster visualization  
- sensitive attribute correlation review  
- summary of semantic or fairness-related risks

#### 1.4 Mechanistic Interpretability for High-Risk Models
High-risk models must include advanced interpretability analysis such as neuron activation review or causal tracing.

### 2 Adversarial Evaluation Controls

#### 2.1 Adversarial Test Suite
All models must undergo adversarial testing using a documented evaluation suite appropriate to architecture and risk level.

#### 2.2 Gradient and Perturbation Testing
Models must be evaluated using minimal perturbation techniques to detect brittleness and sensitivity.

#### 2.3 Red Team Evaluation
High-risk and enterprise-impact models must undergo structured red team evaluations including:

- prompt conflict  
- chain-of-thought disruption  
- misdirection attempts  
- counterfactual reversal tests  
- malicious input exposure  

Findings must be documented, remediated, or formally risk accepted.

#### 2.4 Out-of-Distribution Evaluation
Models must be tested against out-of-distribution inputs to verify stable and safe generalization.

### 3 Goal Alignment and Behavioral Controls

#### 3.1 Alignment Validation
All models must be evaluated to ensure alignment with intended purpose, ethical guidelines, and enterprise governance principles.

#### 3.2 Behavioral Drift Monitoring
Deployed models must include drift monitoring mechanisms assessing:

- output anomalies  
- internal distribution shifts  
- alignment deviations  
- unusual behaviour indicators  

Alerts must be logged and escalated.

### 4 Data and Training Controls

#### 4.1 Training Data Documentation
All training data, sources, and transformations must be fully documented.

#### 4.2 Sensitive Attribute Review
Datasets must be reviewed for sensitive attributes and associated correlation risks.

#### 4.3 Provenance and Lineage
All training data must include provenance and lineage documentation and be traceable throughout the lifecycle.

### 5 Lifecycle Governance Controls

#### 5.1 Model Card Requirement
Each model must include a complete model card before deployment summarizing:

- purpose  
- architecture  
- training sources  
- evaluation results  
- interpretability findings  
- adversarial evaluation summaries  
- limitations  
- risk statements  

#### 5.2 System Card Requirement
Models embedded within broader systems must include a system card that describes system-level risks, dependencies, and interactions.

#### 5.3 Deployment Approval
Models may only be deployed following approval from:

- Model Owner  
- AI Governance Council  
- Compliance and Legal  
- Security (adversarial review)

#### 5.4 Documentation Integrity
All lifecycle documentation must be maintained in an immutable repository with version control.

### 6 Monitoring and Re-Evaluation Controls

#### 6.1 Continuous Monitoring
Models must be continuously monitored for drift, degradation, anomalous behaviour, and adversarial indicators.

#### 6.2 Periodic Re-Evaluation
All models must undergo full re-evaluation at least annually or when triggered by:

- major architectural changes  
- retraining events  
- data pipeline modifications  
- material incidents  

#### 6.3 Incident Response Integration
Model anomalies or adversarial events must trigger established incident response processes and be logged in the enterprise risk system.

### 7 Documentation and Evidence Requirements

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

Evidence must be retained for the full lifecycle and archived according to the AI Lifecycle Governance Standard.

## Roles and Responsibilities

### Model Owner
Ensures control compliance and maintains complete documentation.

### AI Governance Council
Provides oversight, evaluates exceptions, and assures alignment with enterprise AI governance expectations.

### Compliance and Legal
Validates adherence to applicable laws, regulations, and standards.

### Security and Risk Management
Conducts adversarial testing and manages safety-related risks.

### Internal Audit
Verifies control enforcement and completeness of documentation and evidence.

## References and Framework Alignment

- In Model Risk Framework  
- AI Governance Framework  
- AI System Audit and Certification Framework  
- AI Lifecycle Governance Standard  
- ISO 42001  
- ISO 23894  
- ISO 24028  
- NIST AI RMF  
- COBIT 2025  
- CSA CCM v5
