Document Title: In Model Risk Assessment Procedure
Document Type: Procedure
Version: 0.0.1
Date: 2025 11 18
Owner: Compliance Officer
Approving Authority: Chief Compliance Officer
Related Documents: in-model-risk-framework (framework-in-model-risk.md); in-model-risk-standard (standard-in-model-risk.md); ai-governance-framework (framework-ai-governance.md); ai-system-audit-and-certification-framework (framework-ai-system-audit-and-certification.md); ai-lifecycle-governance-standard (standard-ai-lifecycle-governance.md)
Classification: Public
Category: Artificial Intelligence
Review Frequency: Annual
Repository Path: /ai/procedure-in-model-risk-assessment.md
Confidentiality: Public

# Purpose

This procedure defines the mandatory steps, sequencing, documentation requirements, and approval checkpoints for conducting an in model risk assessment. It operationalizes the In Model Risk Framework and the In Model Risk Standard by providing consistent, repeatable activities for evaluating interpretability, representation behaviour, adversarial robustness, alignment, lifecycle governance, and evidence sufficiency.

# Scope

This procedure applies to all artificial intelligence and machine learning models developed, acquired, fine tuned, integrated, or deployed by the organization. It covers all lifecycle stages including design, development, training, validation, deployment, monitoring, retraining, and decommissioning. It applies to production, pilot, experimental, embedded, and vendor supplied models.

# Objectives

1. Ensure assessments are executed consistently across all AI and ML systems.  
2. Provide a structured sequence for interpretability, representation, adversarial, and lifecycle evaluations.  
3. Define documentation and evidence requirements.  
4. Clarify approval requirements prior to deployment.  
5. Support auditability and traceable model governance.

# Procedure

## 1 Assessment Preparation

1.1 Identify model type, purpose, business owner, risk level, and lifecycle stage.  
1.2 Confirm whether the assessment is initial, periodic, or triggered by change.  
1.3 Retrieve the latest versions of required templates including the model card, system card, interpretability report, adversarial test plan, and evaluation summary.  
1.4 Confirm availability of training data documentation, provenance records, and data lineage evidence.  
1.5 Establish storage locations for assessment evidence in the approved repository.

## 2 Interpretability Assessment

2.1 Determine interpretability expectations based on model risk category.  
2.2 Generate feature attribution evidence using at least one approved method.  
2.3 Conduct representation and embedding analysis for models using latent variables.  
2.4 For high risk systems, conduct mechanistic interpretability analysis when practicable.  
2.5 Document findings in the interpretability report and summarize in the model card.

## 3 Adversarial Evaluation

3.1 Select the appropriate adversarial test suite based on model architecture.  
3.2 Perform gradient and perturbation tests to evaluate brittleness.  
3.3 Execute structured red team evaluations.  
3.4 Conduct out of distribution testing to assess generalization.  
3.5 Document all findings and identify remediation or residual risk acceptance needs.

## 4 Alignment and Behavioural Evaluation

4.1 Evaluate alignment with intended purpose and enterprise ethical guidelines.  
4.2 Review outputs for contradictory, harmful, or policy-noncompliant behaviour.  
4.3 Assess susceptibility to behavioural drift based on historical performance or expected conditions.  
4.4 Identify required constraints, guardrails, or monitoring thresholds.

## 5 Data and Training Evaluation

5.1 Verify completeness of training data documentation including source descriptions and transformations.  
5.2 Review sensitive attribute presence and correlation risks.  
5.3 Validate data provenance and lineage records.  
5.4 Confirm compliance with internal data management requirements.

## 6 Lifecycle Governance Assessment

6.1 Confirm that a complete model card and, where applicable, system card are prepared.  
6.2 Validate that all interpretability, representation, and adversarial evaluation reports are complete.  
6.3 Verify version control, audit trail, and documentation integrity.  
6.4 Confirm alignment with the AI Lifecycle Governance Standard.  
6.5 Verify that monitoring and drift detection mechanisms are configured.

## 7 Risk Rating and Residual Risk Assessment

7.1 Assign a model risk rating consistent with the enterprise taxonomy.  
7.2 Identify residual risks that cannot be remediated prior to deployment.  
7.3 Document residual risks and obtain necessary approvals for acceptance.

## 8 Deployment Approval

8.1 Submit evidence package for review by:  
- Model Owner  
- Compliance Officer  
- Legal Counsel  
- Security Reviewer  
- AI Governance Representative

8.2 Resolve required changes or recommendations.  
8.3 Obtain final approval from the designated approving authority.  
8.4 Record approval in the repository.

## 9 Post Deployment Monitoring Requirements

9.1 Establish performance and drift monitoring thresholds.  
9.2 Configure alerting and logging requirements.  
9.3 Ensure monitoring dashboards or reports are accessible to stakeholders.  
9.4 Document monitoring expectations in the system card.

## 10 Evidence Storage and Archival

10.1 Store all evidence in the approved repository using the correct naming and indexing conventions.  
10.2 Archive superseded evidence upon model decommissioning.  
10.3 Ensure retention requirements align with the AI Lifecycle Governance Standard.

# Roles and Responsibilities

## Compliance Officer
Oversees execution of the procedure, verifies completeness of evidence, and ensures compliance with applicable frameworks.

## Model Owner
Provides documentation, conducts or coordinates required testing, and ensures model compliance with all procedural steps.

## Security Reviewer
Performs adversarial evaluations, identifies robustness risks, and validates mitigation actions.

## Legal Counsel
Assesses legal and regulatory risks.

## AI Governance Representative
Ensures alignment with enterprise AI governance principles and lifecycle expectations.

## Internal Audit
Reviews compliance with this procedure as part of periodic assurance activities.

# Monitoring, Metrics, and Reporting

1. Quarterly reporting on assessment completion rates, common findings, and maturity trends.  
2. Tracking of remediation timelines and residual risk acceptance patterns.  
3. Annual review of procedure effectiveness.

# Continuous Improvement

1. The procedure will be updated based on lessons learned, incident findings, and emerging standards.  
2. Proposed improvements should be recorded in the continuous improvement register.  
3. Non-substantive clarifications may be updated without reapproval but must be logged.

# References and Framework Alignment

- In Model Risk Framework  
- In Model Risk Standard  
- AI Governance Framework  
- AI System Audit and Certification Framework  
- AI Lifecycle Governance Standard  
- ISO 42001  
- ISO 23894  
- ISO 24028  
- NIST AI RMF  
- CSA CCM v5  
- COBIT 2025
