# Procedure: Business Impact Analysis (BIA)

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | Business Impact Analysis (BIA) Procedure |
| **Document Type** | Procedure |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Business Continuity Manager (BCM) |
| **Approving Authority** | Chief Information Officer (CIO) |
| **Related Documents** | Framework: Business Continuity & Resilience; Policy: Business Continuity and Disaster Recovery; Standard: Business Continuity & Disaster Recovery; Procedure: Continuity & Recovery Testing and Exercising; Plan: Business Continuity & Crisis Management |
| **Classification** | Public – Open Access |
| **Category** | Business Continuity / Risk Assessment |
| **Review Frequency** | Annual or following major organizational or technological change |
| **Repository Path** | /resilience/procedure-business-impact-analysis.md |
| **Confidentiality** | None (Public Domain, CC0 License) |



## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |



## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Risk Officer (CRO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Compliance Officer (CCO) |  |  |
| Chief Legal Officer / General Counsel (CLO/GC) |  |  |



## Purpose

This procedure defines the methodology for performing Business Impact Analyses (BIAs) to identify, evaluate, and prioritize critical business processes and dependencies.  
It ensures that recovery objectives (RTO/RPO) and continuity strategies are based on accurate, repeatable, and data-driven assessments.



## Scope

- Applies to all business units, functions, and supporting technologies that enable critical business processes.  
- Includes dependencies on personnel, facilities, information systems, suppliers, and AI or automation services.  
- Covers both enterprise-level and departmental BIAs that feed into the organization’s Business Continuity and Disaster Recovery planning cycle.



## Objectives

1. Identify critical business processes and dependencies required for sustained operations.  
2. Quantify the financial, operational, reputational, and regulatory impact of downtime.  
3. Determine Recovery Time Objectives (RTOs) and Recovery Point Objectives (RPOs).  
4. Provide data to support continuity planning, risk assessments, and testing priorities.



## Methodology

The BIA process follows six sequential phases:

1. **Planning and Scope Definition**  
   - The BCM establishes assessment scope, criteria, and templates.  
   - Stakeholders and departmental coordinators are identified.

2. **Data Collection**  
   - Information is gathered through questionnaires, interviews, and system-data exports.  
   - Minimum required fields include:  
     - Process name and description  
     - Owner and department  
     - Inputs, outputs, and interdependencies  
     - Supporting systems and applications  
     - Required staff, vendors, and data sources  
     - Current RTO/RPO and manual workarounds  

3. **Process-Criticality Assessment**  
   - Each process is classified by tier based on operational urgency and downtime tolerance:  

| Tier | Description | Target RTO | Example |
|------|--------------|-------------|----------|
| **1 – Mission Critical** | Immediate recovery required to sustain operations. | < 4 h | ERP, logistics, communications. |
| **2 – Essential** | Recovery required within same business day. | 4–24 h | Finance, HR, customer portals. |
| **3 – Important** | Temporary outage tolerable with workarounds. | 24–72 h | Departmental reporting, collaboration tools. |
| **4 – Non-Critical** | Minimal operational impact if unavailable. | > 72 h | Training systems, low-priority tools. |

4. **Impact Analysis and Scoring**  
   - Impacts are rated across categories of financial, operational, reputational, regulatory, and AI/automation risk.  
   - Each category scored 1 (Low) – 5 (Critical); totals determine overall impact priority:  

| Total Score | Impact Level | Response Priority |
|--------------|--------------|------------------|
| 1–5 | Low | Monitor only. |
| 6–10 | Moderate | Develop recovery plan. |
| 11–15 | High | Immediate recovery focus. |
| 16–25 | Critical | Executive oversight and redundancy planning. |

5. **Dependency Mapping**  
   - Dependencies are charted across internal systems, third-party services, facilities, and data flows.  
   - AI-enabled mapping tools may be used to visualize dependency chains and simulate failure impacts.  
   - The resulting dependency model is maintained within the BIA Register.

6. **Recovery Objective Determination and Reporting**  
   - RTO and RPO values are reviewed by the BCM and approved by the CIO and ERC.  
   - Enterprise BIA reports summarize:  
     - Process-tier classification  
     - Dependency maps  
     - Aggregate risk and recovery metrics  
     - Recommendations for continuity improvements.  



## Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Business Continuity Manager (BCM)** | Leads BIA planning, templates, and data consolidation. |
| **Department Heads / Process Owners** | Identify critical processes, validate impacts, and approve recovery priorities. |
| **CIO / CRO** | Approve enterprise BIA results and ensure risk alignment. |
| **CISO** | Review ICT, data, and AI dependencies for continuity relevance. |
| **ERC** | Validate outcomes, approve recovery objectives, and monitor follow-up actions. |
| **Internal Audit** | Verify that BIAs are updated, approved, and integrated into continuity planning. |



## Review and Update

- BIAs must be performed at least annually and after major organizational or system changes.  
- Each update must be documented, version-controlled, and stored in the governance repository.  
- Lessons learned from exercises or incidents feed into corrective-action and improvement processes.



## Continuous Improvement

Insights, gaps, and recommendations identified through BIAs must be tracked and validated through:  
- The Corrective and Preventive Action Procedure  
- The Continuous Improvement Register Procedure  
- The Digital Trust Performance Framework  

Actions remain open until verified as effective through testing or subsequent assessment.



## References and Framework Alignment

| Framework | Reference | Objective |
|------------|------------|-----------|
| **ISO 22317:2015** | Business Impact Analysis Guidelines | Provides BIA methodology and reporting structure. |
| **ISO 22301:2019** | Clauses 8–10 | Integrates BIA within BCMS lifecycle. |
| **COBIT 2025** | DSS04.02 – Conduct Business Impact Analysis | Ensures alignment between risk and continuity management. |
| **NIST SP 800-34 Rev 1** | Chapter 3 | Defines contingency-planning inputs and business process analysis. |
| **CSA CCM v5** | GOV-08 – Business Resilience Governance | Establishes governance controls for continuity and resilience. |



## Definitions

Key terms and acronyms used in this document are defined in the **Resilience Terms and Definitions Register**, which provides standardized terminology for all Business Continuity, Disaster Recovery, and Crisis Management artefacts.

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.



**End of Document**
