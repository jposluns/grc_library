# Business Impact Analysis Procedure

**Document Title:** Business Impact Analysis Procedure
**Document Type:** Procedure
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Resilience Owner
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `resilience/framework-business-continuity-and-resilience.md`, `resilience/policy-business-continuity-and-disaster-recovery.md`, `resilience/standard-business-continuity-and-disaster-recovery.md`, `resilience/business-continuity-and-crisis-management.md`, `resilience/procedure-continuity-and-recovery-testing.md`
**Classification:** Public
**Category:** Resilience
**Review Frequency:** Annual and upon material process, system, supplier, data, AI, facility, or organizational change
**Repository Path:** `resilience/procedure-business-impact-analysis.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This procedure defines a reusable method for conducting business impact analysis. It identifies critical processes, dependencies, impact tolerances, recovery priorities, and evidence required to support continuity and disaster recovery planning.

---

## Scope

The procedure applies to business processes, technology services, data sets, suppliers, facilities, workforce roles, cloud services, AI systems, integrations, and records that support critical operations.

---

## Procedure

### Step 1: Define Scope

Identify the process, service, system, supplier, data set, facility, or AI system being assessed. Record the owner, assessment date, assessment trigger, related services, and known dependencies.

### Step 2: Identify Critical Outputs

Record the business outputs, customers, users, regulated activities, data obligations, contractual commitments, and operational outcomes affected by disruption.

### Step 3: Identify Dependencies

Map dependencies including people, facilities, applications, infrastructure, cloud services, identity services, data stores, suppliers, integrations, communication channels, security controls, monitoring systems, and AI services.

### Step 4: Assess Impact

Assess impact over time across operational, financial, legal, regulatory, customer, safety, privacy, security, supplier, reputational, and resilience dimensions.

### Step 5: Define Recovery Objectives

Define recovery time objective, recovery point objective, maximum tolerable disruption, minimum service level, manual workaround viability, data restoration needs, and business acceptance criteria.

### Step 6: Identify Continuity Requirements

Record required continuity strategies, manual workarounds, recovery sequence, alternate suppliers, emergency access requirements, communication requirements, and required evidence.

### Step 7: Validate and Approve

Review the assessment with accountable roles. Approve recovery objectives and unresolved risks. Record assumptions, limitations, exceptions, and residual risk.

### Step 8: Maintain

Review the assessment at the required cadence and after material changes to services, architecture, suppliers, data, AI systems, facilities, legal obligations, or business process criticality.

---

## Minimum BIA Fields

| Field | Description |
| --- | --- |
| Assessment ID | Unique internal identifier. |
| Process or Service | Process, service, system, supplier, or data set assessed. |
| Owner Role | Accountable owner. |
| Critical Outputs | Outputs or obligations affected by disruption. |
| Dependency Summary | Key people, systems, data, suppliers, facilities, and integrations. |
| Impact Timeline | Impact at defined outage intervals. |
| Recovery Time Objective | Target time to restore acceptable service. |
| Recovery Point Objective | Maximum acceptable data loss. |
| Maximum Tolerable Disruption | Longest tolerable disruption before unacceptable impact. |
| Minimum Service Level | Minimum operating capability during disruption. |
| Manual Workaround | Available workaround and limitations. |
| Residual Risk | Remaining risk after planned continuity strategy. |
| Approval Role | Role approving assessment and recovery objectives. |
| Review Date | Next review date. |

---

## AI and Data Considerations

Where the assessed process depends on AI systems, the BIA must consider model service availability, retrieval store availability, data lineage, prompt and output logs, monitoring records, supplier dependency, emergency disablement, fallback decision process, retention, deletion, and recovery validation.

---

## Evidence Requirements

Maintain the completed assessment, dependency map, recovery objective decision, owner approval, exception record, continuity requirement, and related corrective action records.

---

**End of Document**
