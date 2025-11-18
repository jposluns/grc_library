# Procedure: Continuity & Recovery Testing and Exercising

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | Continuity & Recovery Testing and Exercising Procedure |
| **Document Type** | Procedure |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Business Continuity Manager (BCM) |
| **Approving Authority** | Chief Information Officer (CIO) |
| **Related Documents** | Framework: Business Continuity & Resilience; Policy: Business Continuity and Disaster Recovery; Standard: Business Continuity & Disaster Recovery; Plan: Business Continuity & Crisis Management; Plan: Crisis Communication; Procedure: Business Impact Analysis; Procedure: Crisis Management & EOC Activation |
| **Classification** | Public – Open Access |
| **Category** | Business Continuity / Testing and Assurance |
| **Review Frequency** | Annual or following a major change or incident |
| **Repository Path** | /resilience/procedure-continuity-and-recovery-testing.md |
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

This procedure defines the methodology for planning, executing, and documenting continuity and recovery testing and exercises.  
It ensures that all Business Continuity and Disaster Recovery capabilities are validated, measurable, and continually improved to support enterprise resilience.



## Scope

- Applies to all business units, IT systems, and critical processes identified through the Business Impact Analysis.  
- Covers the scheduling, execution, evaluation, and reporting of all continuity and disaster-recovery exercises.  
- Includes technology failovers, crisis simulations, tabletop exercises, and integrated organizational tests.  
- Applies to internal teams, third-party service providers, and partners who participate in continuity testing activities.



## Objectives

1. Validate that continuity and recovery plans perform as designed and meet defined RTO/RPO targets.  
2. Confirm staff readiness, communication efficiency, and procedural accuracy.  
3. Identify weaknesses and improvement opportunities.  
4. Maintain audit-ready records demonstrating ISO 22301 and COBIT DSS04 compliance.



## Test Types

| Type | Description | Frequency | Owner |
|------|--------------|------------|-------|
| **Tabletop Exercise** | Discussion-based scenario review of roles, procedures, and communication. | Quarterly | BCM / Department Heads |
| **Simulation Test** | Partial functional test of components (e.g., backup restoration, system failover). | Semi-annual | IT Operations / CISO |
| **Full Recovery Test** | End-to-end execution of recovery processes for critical systems or sites. | Annual | CIO / BCM |
| **Crisis Communication Drill** | Messaging and approval workflow validation. | Annual | Communications Director |
| **Integrated Enterprise Exercise** | Multi-department test combining BC, DR, and crisis management. | Every 2 years | CIO / CRO / ERC |



## Test Planning

1. **Annual Test Schedule**  
   - The BCM develops the schedule each Q4 for the following calendar year.  
   - Schedule must cover all Tier-1 and Tier-2 processes at least once per year.

2. **Test Design**  
   - Define objectives, scope, roles, and success criteria.  
   - Prepare scripts or scenarios simulating realistic events (cyber incident, facility outage, data loss, etc.).  
   - Include communication and escalation workflows as applicable.

3. **Approval**  
   - Each exercise plan is reviewed and approved by the CIO and CRO prior to execution.  
   - Tests that may affect production systems require written change-control authorization.



## Execution

1. Conduct exercise according to approved plan and timeline.  
2. Maintain control logs including:  
   - Start/end times  
   - Participants and observers  
   - Steps executed  
   - Anomalies or deviations  
3. Capture quantitative metrics (e.g., recovery times, data-integrity validation, communication latency).  
4. Ensure that testing activities do not compromise operational systems or data integrity.



## Evaluation and Reporting

| Activity | Deliverable | Owner |
|-----------|-------------|-------|
| Immediate debrief | Verbal summary of performance and key findings. | Test Facilitator |
| Written Test Report | Detailed record of results, metrics, and issues. | BCM |
| Review Meeting | Validation of corrective actions and lessons learned. | CIO / CRO / ERC |
| Final Approval | Endorsement of test closure and improvement plan. | CIO |

**Each Test Report must include:**
- Objectives and success criteria.  
- Participants and roles.  
- Observed performance vs. targets.  
- Identified issues, root causes, and corrective actions.  
- Recommendations for improvement.  

All records are stored in the governance repository and retained for a minimum of seven years.



## Performance Metrics

| Metric | Description | Target |
|---------|--------------|--------|
| **RTO Achievement Rate** | % of systems recovered within RTO. | ≥ 95% |
| **RPO Compliance Rate** | % of systems meeting RPO thresholds. | ≥ 95% |
| **Exercise Completion Rate** | % of scheduled exercises completed on time. | 100% |
| **Improvement Closure Rate** | % of corrective actions closed within 90 days. | ≥ 90% |
| **Testing Coverage** | % of Tier-1/Tier-2 functions tested annually. | 100% |



## Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Business Continuity Manager (BCM)** | Develops test plan, coordinates exercises, records outcomes, and reports to leadership. |
| **CIO / CRO** | Approve annual testing program and ensure resource allocation. |
| **CISO** | Oversees cybersecurity and data-protection aspects of testing. |
| **IT Operations** | Executes recovery tests and validates infrastructure readiness. |
| **Communications Director** | Tests internal/external messaging workflows. |
| **Department Heads** | Ensure staff participation and local plan validation. |
| **Enterprise Risk Committee (ERC)** | Reviews results, tracks trends, and ensures continual improvement. |



## Continuous Improvement

Findings, gaps, and lessons learned from each exercise must be documented and tracked through:
- The Corrective and Preventive Action Procedure  
- The Continuous Improvement Register Procedure  
- The Digital Trust Performance Framework  

Improvements remain open until retested and confirmed effective.



## References and Framework Alignment

| Framework | Reference | Objective |
|------------|------------|-----------|
| **ISO 22301:2019** | Clauses 8–10 | Establish, implement, and evaluate BCMS performance. |
| **ISO 22398:2013** | Clauses 5–9 | Provide guidance for developing and conducting exercises. |
| **COBIT 2025** | DSS04, DSS05 | Ensure continuity and security services are tested and improved. |
| **NIST SP 800-34r1** | Chapters 4–5 | Define contingency testing and validation best practices. |
| **CSA CCM v5** | BCR-03, BCR-04 | Establish business-continuity testing and operational-resilience assurance. |



## Definitions

Key terms and acronyms used in this document are defined in the **Resilience Terms and Definitions Register**, which provides standardized terminology for all Business Continuity, Disaster Recovery, and Crisis Management artefacts.

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.



**End of Document**
