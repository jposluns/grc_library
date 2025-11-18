Document Title
System Card Template

Document Type
Template

Version
0.0.1

Date
2025 November 18

Owner
Chief Compliance Officer

Approving Authority
Chief Compliance Officer

Related Documents
In Model Risk Framework (framework-in-model-risk.md)
In Model Risk Standard (standard-in-model-risk.md)
AI Lifecycle Governance Standard (standard-ai-lifecycle-governance.md)
In Model Risk Assessment Procedure (procedure-in-model-risk-assessment.md)
Model Card Template (template-model-card.md)

Classification
Public

Category
Artificial Intelligence

Review Frequency
Annual

Repository Path
/ai/template-system-card.md

Confidentiality
Public

# Purpose

This template defines the required structure for documenting risks, interactions, dependencies, and operational controls for AI systems that incorporate one or more machine learning or artificial intelligence models. A system card provides holistic visibility into end-to-end AI system behaviour and supports governance, safety, risk evaluation, and auditability across the full system lifecycle.

# Scope

This template applies to all enterprise systems containing embedded AI or ML components, including vendor-supplied platforms, internally developed systems, hybrid pipelines, multi-model architectures, and systems integrating external APIs. A system card must be completed prior to deployment and updated following significant system, data, or model changes.

# System Card Template

## 1 System Overview

System Name  
System Identifier  
Version  
System Owner  
Business Unit  
Primary System Purpose  
System Boundaries and Scope  
Deployment Environment (cloud, on premise, edge, hybrid, vendor hosted)  

## 2 System Architecture

High Level Architecture Diagram Reference  
System Components  
Integrated Models (list each with model identifiers)  
Data Pipelines and Flows  
External Dependencies and APIs  
Upstream and Downstream System Interactions  
Security Architecture Summary  

## 3 Functional Description

System Functions and Capabilities  
Decision or Automation Points  
End User Interactions  
Operational Use Cases  
Workflow Integration  

## 4 Embedded AI Models

Model Inventory Summary  
Purpose of Each Embedded Model  
Role of Each Model in System Behaviour  
Model Dependency Graph  
Model-Specific Risk Ratings  
Links to Model Cards  

## 5 Data Lifecycle

Data Inputs  
Data Outputs  
Data Transformations  
Data Storage Locations  
Sensitive Attributes Present  
Provenance and Lineage Summary  
Data Retention and Deletion Requirements  

## 6 Evaluation and Testing Summary

Functional Testing  
System-Level Performance Metrics  
Scenario and Stress Testing  
Adversarial System-Level Testing Results  
Human Factors Testing (if applicable)  
Safety and Resilience Evaluations  
Validation of Inter-Model Interactions  

## 7 Alignment and Safety Controls

Intended Purpose Alignment  
Ethical and Policy Alignment Review  
Safeguards and Guardrails  
Content Safety Controls (if applicable)  
User Safety and Abuse Prevention Measures  
Compliance With Enterprise Ethical Guidelines  

## 8 System Risks and Controls

System-Level Risk Identification  
Interdependency Risks  
Data Flow Risks  
Operational Risks  
Security Risks  
Model Interaction Risks  
Mitigation Controls Implemented  
Residual Risks  

## 9 Monitoring and Operational Controls

System Monitoring Requirements  
Model Monitoring Integration  
Drift Detection Coverage  
Alert Thresholds  
Logging Requirements  
Incident Indicators  
Performance Degradation Criteria  
Escalation and Notification Procedures  

## 10 Deployment and Change Management

Deployment Prerequisites  
Change Management Requirements  
Rollback and Contingency Plans  
Documentation Requirements for Changes  
System Approval Workflow  
Dependencies on External Vendors  

## 11 Governance and Approvals

System Owner Approval  
Compliance Review  
Legal Review  
Security Review  
AI Governance Review  
Final Approval Authority  

## 12 Evidence Repository Index

Evidence Location References  
Architecture diagrams  
Model cards  
Evaluation datasets  
Test results  
Adversarial testing reports  
Monitoring configuration  
Version history  
Lifecycle decision logs  
Change records  

# Monitoring, Metrics, and Reporting

System cards must be reviewed during re evaluation cycles and updated as part of model or system retraining events.  
Annual summaries should highlight system behaviour, findings, incidents, and maturity indicators.  
All changes must be recorded in the repository with version control.

# Continuous Improvement

System card improvements should be proposed based on lessons learned, incidents, or updated standards.  
Non substantive edits may be made without reapproval but must be logged in the continuous improvement register.

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
