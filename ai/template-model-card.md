Document Title: Model Card Template
Document Type: Template
Version: 0.0.1
Date: 2025 11 18
Owner: Compliance Officer
Approving Authority: Chief Compliance Officer
Related Documents: in-model-risk-framework (framework-in-model-risk.md); in-model-risk-standard (standard-in-model-risk.md); ai-lifecycle-governance-standard (standard-ai-lifecycle-governance.md); procedure-in-model-risk-assessment (procedure-in-model-risk-assessment.md)
Classification: Public
Category: Artificial Intelligence
Review Frequency: Annual
Repository Path: /ai/template-model-card.md
Confidentiality: Public

# Purpose

This template provides the standardized structure for documenting model attributes, evaluation evidence, interpretability results, adversarial testing outcomes, lifecycle metadata, and residual risk information. It ensures consistent documentation across all artificial intelligence and machine learning systems, supports assurance activities, and aligns with the enterprise in model risk governance framework.

# Scope

This template applies to all AI and ML models developed, acquired, integrated, or deployed by the organization. It must be completed prior to deployment, updated at each retraining event, and maintained for the full model lifecycle.

# Model Card Template

## 1 Model Overview

**Model Name:**  
**Model Identifier:**  
**Version:**  
**Model Owner:**  
**Business Unit:**  
**Primary Use Case:**  
**Intended Purpose:**  
**Model Type:** (classification, regression, NLP, LLM, embedding model, reinforcement learning, etc.)  
**Deployment Environment:** (cloud, on premise, edge, vendor hosted)

## 2 Functional Description

**High Level Description:**  
**Inputs:**  
**Outputs:**  
**Decision Impact:**  
**Supported Workflows or Systems:**  
**Dependencies and External Services:**  

## 3 Architecture Summary

**Model Architecture:** (algorithm, architecture family, neural network type, transformer model, etc.)  
**Training Data Overview:**  
**Feature Summary:**  
**Embedding Details (if applicable):**  

## 4 Training and Evaluation

**Training Process Summary:**  
**Data Sources:**  
**Data Transformations:**  
**Evaluation Datasets:**  
**Performance Metrics:** (accuracy, F1, recall, etc.)  
**Validation Approach:** (cross validation, holdout, etc.)  
**Fairness Metrics:**  
**Stress and Scenario Tests:**  

## 5 Interpretability Findings

**Interpretability Method(s) Used:** (SHAP, LIME, Integrated Gradients, etc.)  
**Key Insights:**  
**Highlighted Features:**  
**Bias or Disparity Indicators:**  
**Representation Analysis Summary:**  
**Known Model Limitations:**  

## 6 Adversarial and Robustness Testing

**Adversarial Test Suite Used:**  
**Gradient and Perturbation Results:**  
**Red Team Evaluation Summary:**  
**Out of Distribution Test Results:**  
**Robustness Observations:**  
**Identified Vulnerabilities:**  

## 7 Alignment and Behavioural Analysis

**Intended Purpose Alignment:**  
**Ethical and Policy Alignment Review:**  
**Behavioural Drift Risk:**  
**Long Horizon Reasoning Observations (if applicable):**  

## 8 Model Risk Rating

**Risk Category:** (low, medium, high)  
**Rationale:**  

## 9 Monitoring and Controls

**Drift Detection Mechanisms:**  
**Alert Thresholds:**  
**Logging Configuration:**  
**Continuous Monitoring Requirements:**  
**Human in the Loop Requirements:**  

## 10 Residual Risk Statements

**Identified Residual Risks:**  
**Mitigation Actions:**  
**Accepted Risks:**  
**Approval References:**  

## 11 Governance and Approvals

**Model Owner Approval:**  
**Compliance Review:**  
**Legal Review:**  
**Security Review:**  
**AI Governance Review:**  
**Final Approval Authority:**  

## 12 Evidence Repository Index

**Location of Evidence:**  
- interpretability report  
- adversarial testing report  
- representation analysis  
- evaluation datasets  
- training documentation  
- monitoring configuration  
- version history  
- lifecycle decision logs  

# Monitoring, Metrics, and Reporting

1. Model cards must be reviewed during periodic re evaluation.  
2. Updates must be tracked in the repository with version control.  
3. Annual reporting must summarize changes, findings, and maturity indicators.

# Continuous Improvement

1. Improvements to this template may be proposed when new standards, methods, or evaluation approaches emerge.  
2. Non substantive revisions may be made without reapproval but must be recorded in the continuous improvement register.

# References and Framework Alignment

- In Model Risk Framework  
- In Model Risk Standard  
- AI Lifecycle Governance Standard  
- ISO 42001  
- ISO 23894  
- ISO 24028  
- NIST AI RMF  
- CSA CCM v5  
- COBIT 2025
