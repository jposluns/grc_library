Document Title
In Model Risk Control-to-Lifecycle Mapping Matrix

Document Type
Matrix

Version
0.0.1

Date
2025 November 18

Owner
Chief Risk Officer

Approving Authority
Chief Information Security Officer

Related Documents
In Model Risk Framework (framework-in-model-risk.md)
In Model Risk Standard (standard-in-model-risk.md)
AI Lifecycle Governance Standard (standard-ai-lifecycle-governance.md)
In Model Risk Assessment Procedure (procedure-in-model-risk-assessment.md)
Model Card Template (template-model-card.md)
System Card Template (template-system-card.md)
Adversarial Evaluation Suite Development Guideline (guideline-adversarial-evaluation-suite-development.md)

Classification
Public

Category
Artificial Intelligence

Review Frequency
Annual

Repository Path
/ai/matrix-in-model-risk-control-to-lifecycle-mapping.md

Confidentiality
Public

# Purpose

This matrix establishes a unified mapping between the controls defined in the In Model Risk Framework and the mandatory requirements outlined in the In Model Risk Standard.  
The matrix aligns each control to applicable lifecycle phases defined in the AI Lifecycle Governance Standard and supports auditability, system assurance, and traceability of risk treatments.

# Scope

This matrix applies to all AI and ML models covered by enterprise AI governance, regardless of platform, architecture, risk category, or deployment environment.  
It is used by model owners, evaluators, auditors, and governance committees to assess coverage, completeness, and lifecycle integration of in model risk controls.

# Matrix: In Model Risk Controls Mapped to Lifecycle Phases

## Lifecycle Phases
Design  
Development  
Pre Deployment  
Deployment  
Monitoring  
Re Evaluation  
Retirement  

## Control Mapping Table

| Control Area | Control Reference | Design | Development | Pre Deployment | Deployment | Monitoring | Re Evaluation | Retirement |
|--------------|------------------|--------|-------------|----------------|------------|------------|---------------|------------|
| Interpretability baseline | Standard 1.1 | ✔ | ✔ | ✔ | – | ✔ | ✔ | – |
| Feature attribution evidence | Standard 1.2 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Representation and embedding analysis | Standard 1.3 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Mechanistic interpretability (high risk) | Standard 1.4 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Adversarial test suite requirement | Standard 2.1 | ✔ | ✔ | ✔ | – | ✔ | ✔ | – |
| Gradient and perturbation tests | Standard 2.2 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Red team evaluation | Standard 2.3 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Out of distribution evaluation | Standard 2.4 | – | ✔ | ✔ | – | ✔ | ✔ | – |
| Alignment validation | Standard 3.1 | ✔ | ✔ | ✔ | – | ✔ | ✔ | – |
| Behavioral drift monitoring | Standard 3.2 | – | – | – | ✔ | ✔ | ✔ | – |
| Training data documentation | Standard 4.1 | ✔ | ✔ | ✔ | – | – | ✔ | – |
| Sensitive attribute review | Standard 4.2 | ✔ | ✔ | ✔ | – | – | ✔ | – |
| Data provenance and lineage | Standard 4.3 | ✔ | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| Model card requirement | Standard 5.1 | – | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| System card requirement | Standard 5.2 | – | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| Deployment approval | Standard 5.3 | – | – | ✔ | ✔ | – | ✔ | – |
| Documentation integrity | Standard 5.4 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Continuous monitoring | Standard 6.1 | – | – | – | ✔ | ✔ | ✔ | – |
| Periodic re evaluation | Standard 6.2 | – | – | – | – | ✔ | ✔ | – |
| Incident response integration | Standard 6.3 | – | – | ✔ | ✔ | ✔ | ✔ | – |
| Interpretability report | Standard 7 | – | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| Adversarial testing report | Standard 7 | – | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| Representation and embedding analysis report | Standard 7 | ✔ | ✔ | ✔ | – | ✔ | ✔ | ✔ |
| Drift monitoring logs | Standard 7 | – | – | – | ✔ | ✔ | ✔ | ✔ |
| Residual risk acceptance statements | Standard 7 | – | – | ✔ | ✔ | ✔ | ✔ | ✔ |

# Interpretation Notes

- A checkmark (✔) indicates the control must be executed or validated during that lifecycle phase.  
- A dash (–) indicates the control does not apply in that lifecycle phase.  
- Controls that appear in multiple phases require updated evidence each time.  
- All evidence must be stored in an immutable repository with version control.  
- Residual risk statements must be reviewed during every re evaluation cycle.

# Monitoring, Metrics, and Reporting

The matrix is used as an audit checkpoint during lifecycle reviews and quality assurance processes.  
Lifecycle coverage metrics must be:  
- monitored continuously,  
- reviewed during re evaluation,  
- and summarized annually for governance committees.

# Continuous Improvement

This matrix must be updated when:  
- new control requirements are introduced,  
- an AI lifecycle phase changes,  
- new adversarial or interpretability techniques emerge,  
- regulatory obligations evolve,  
- significant incidents yield new evaluation criteria.

# References and Framework Alignment

In Model Risk Framework  
In Model Risk Standard  
AI Lifecycle Governance Standard  
ISO 42001  
ISO 23894  
ISO 24028  
NIST AI RMF  
CSA CCM v5  
COBIT 2025
