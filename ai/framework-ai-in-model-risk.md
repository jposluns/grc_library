# Framework: In Model Risk

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | In Model Risk Framework |
| **Document Type** | Framework |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Chief Compliance Officer (CCO) |
| **Approving Authority** | Chief Legal Officer and General Counsel (CLO/GC) |
| **Related Documents** | Framework: AI Governance; Framework: AI System Audit and Certification; Standard: AI Lifecycle Governance; Standard: In Model Risk (forthcoming); Policy: Responsible AI |
| **Classification** | Internal |
| **Category** | Artificial Intelligence |
| **Review Frequency** | Annual |
| **Repository Path** | /ai/framework-ai-in-model-risk.md |
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

This framework establishes the enterprise model for assessing in model risk across artificial intelligence, machine learning, and large language model systems.

It defines risk domains, interpretability methods, adversarial evaluation requirements, lifecycle expectations, documentation patterns, and oversight structures required to ensure that internal model behaviours remain transparent, reliable, fair, and aligned to enterprise governance obligations.

This framework provides conceptual structure only. Mandatory requirements are defined in the In Model Risk Standard.

Aligned with ISO 42001, ISO 23894, ISO 24028, NIST AI RMF, COBIT 2025, and CSA CCM v5.

---

# Scope

- Applies to all AI and ML systems created, acquired, or deployed within the organization, regardless of model type, hosting environment, or development source.  
- Covers predictive, generative, classification, regression, reinforcement learning, embedding based, and hybrid model architectures.  
- Applies across the entire AI lifecycle including design, data preparation, development, training, validation, deployment, monitoring, and retirement.  
- Applies to production systems, internal tooling, pilot deployments, and external vendor supplied models that affect business decisions or automated actions.

---

# Objectives

1. Define enterprise wide domains of in model risk.  
2. Establish consistent interpretability and representation analysis expectations.  
3. Provide a uniform adversarial evaluation structure for robustness and safety.  
4. Strengthen lifecycle governance and documentation requirements.  
5. Support responsible, fair, and traceable internal model behaviour.  
6. Enable consistent oversight by the AI Governance Council and related risk committees.

---

# In Model Risk Domains

## 1 Interpretability and Explainability Risk
Risk arising when internal reasoning, decision pathways, or influencing inputs cannot be clearly understood, examined, or validated.  
This includes both local and global interpretability concerns.

## 2 Representation Risk
Risk that internal embeddings, latent variables, or hidden states encode biased, harmful, or unstable relationships that propagate discriminatory or unreliable outcomes.

## 3 Adversarial Robustness Risk
Risk that adversarial prompts, malicious inputs, or subtle perturbations cause unintended, unsafe, or contradictory behaviour.

## 4 Generalization and Out of Distribution Risk
Risk that the model behaves unpredictably when encountering data or contexts not represented in its training distribution.

## 5 Goal Alignment and Behavioral Drift Risk
Risk that internal model behaviours or priorities shift over time, deviating from intended objectives, policy expectations, or ethical constraints.

## 6 Dependence and Fragility Risk
Risk associated with reliance on unstable, spurious, or non causal features or patterns that compromise resilience or fairness.

## 7 Lifecycle Governance Risk
Risk arising from incomplete documentation, missing version control, insufficient evaluation evidence, or inadequate monitoring of live model performance.

---

# Interpretability Framework

## 1 Feature Attribution Methods
Methods that identify how inputs contribute to predictions.  
Examples include:  
- SHAP  
- Integrated Gradients  
- LIME  

Used to detect bias, fragile dependencies, and non causal logic.

## 2 Representation and Embedding Analysis
Analysis of internal vectors, latent spaces, and clustering patterns.  
Methods include:  
- activation clustering  
- layer wise relevance propagation  
- concept activation vectors  

Used to assess semantic integrity, fairness, and harmful internal associations.

## 3 Mechanistic Interpretability
Deep inspection of internal computational pathways.  
Methods include:  
- neuron activation analysis  
- causal tracing  
- internal circuit mapping  

Used to detect deceptive patterns, unsafe reasoning, or emergent misalignment.

---

# Adversarial Evaluation Framework

## 1 Gradient and Perturbation Tests
Tests applying minimal changes to inputs to identify sensitivity and brittleness.

## 2 Structured Red Teaming
Targeted stress evaluations that attempt to exploit internal weaknesses.  
Common categories include:  
- prompt conflict  
- chain of thought derailment  
- goal hijacking  
- counterfactual stress  
- misdirection attempts  

## 3 Out of Distribution Testing
Evaluation against data or contexts outside the training environment to measure safe generalization.

## 4 Long Horizon Reasoning Stress Tests
For LLMs, tests evaluating consistency, safety, and alignment over extended multi step reasoning sequences.

---

# Lifecycle Integration

In model risk assessment must be embedded at each lifecycle phase:

## 1 Design
- define risk expectations  
- set interpretability requirements  
- confirm ethical and regulatory alignment  

## 2 Development
- perform embedding checks  
- conduct initial adversarial evaluations  
- document internal design choices  

## 3 Pre Deployment
- complete red team evaluations  
- validate robustness and fairness  
- generate model cards and system cards  

## 4 Deployment
- establish performance thresholds  
- implement drift detection  
- configure logging and monitoring  

## 5 Post Deployment
- periodic re evaluation  
- incident review  
- evidence refresh  
- retirement and archival checks

---

# Evidence and Documentation Requirements

The following artefacts support in model risk assurance:

- model cards  
- system cards  
- interpretability reports  
- adversarial test summaries  
- representation audits  
- training data documentation  
- evaluation datasets and scripts  
- lifecycle decision logs  
- approval records  
- residual risk statements  

---

# Governance and Roles

## Model Owner
Responsible for model development, documentation, testing, and ongoing risk management.

## AI Governance Council
Ensures alignment with enterprise policy, regulatory frameworks, and ethical expectations.

## Compliance and Legal
Validates compliance with AI related legislation and applicable standards including ISO and NIST.

## Security and Risk Management
Evaluates adversarial and safety risks and manages related incidents.

## Internal Audit
Verifies adherence to standards, evidence completeness, and lifecycle integrity.

---

# Definitions

Key terms and acronyms used in this document are defined in the **register key terms and definitions md**, located at the top level of the GRC library.

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.

---

**End of Document**
