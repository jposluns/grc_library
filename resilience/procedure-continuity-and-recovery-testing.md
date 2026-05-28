# Continuity and Recovery Testing Procedure

**Document Title:** Continuity and Recovery Testing Procedure 
**Document Type:** Procedure 
**Version:** 0.0.1 
**Date:** 2026-05-27 
**Owner:** Resilience Owner 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](policy-business-continuity-and-disaster-recovery.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-business-impact-analysis.md`](procedure-business-impact-analysis.md), [`resilience/business-continuity-and-crisis-management.md`](business-continuity-and-crisis-management.md), [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md), [`resilience/procedure-backup-and-recovery.md`](procedure-backup-and-recovery.md), [`resilience/register-resilience-metrics-and-testing-log.md`](register-resilience-metrics-and-testing-log.md) 
**Classification:** Public 
**Category:** Resilience 
**Review Frequency:** Annual and upon material continuity, recovery, supplier, system, data, or AI change 
**Repository Path:** [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## Purpose

This procedure defines a reusable method for planning, executing, documenting, evaluating, and improving continuity and recovery tests.

---

## Scope

This procedure applies to critical processes, systems, data stores, suppliers, facilities, workforce dependencies, cloud services, AI systems, communication channels, and recovery capabilities identified through business impact analysis or risk assessment.

---

## Test Types

| Type | Purpose |
| --- | --- |
| Tabletop Exercise | Reviews roles, decisions, assumptions, communication, and escalation through scenario discussion. |
| Walkthrough | Reviews plan steps, dependencies, evidence, and readiness without executing recovery. |
| Technical Restoration Test | Restores data, systems, configurations, or services in a controlled environment. |
| Communications Test | Validates contact paths, message approval, escalation, and status reporting. |
| Supplier Escalation Test | Validates supplier notification, response, evidence, and recovery commitments. |
| Failover or Recovery Test | Exercises service recovery, alternate processing, or recovery site capability. |
| AI Resilience Test | Validates AI service fallback, retrieval store recovery, emergency disablement, monitoring, and data restoration. |

---

## Procedure

### Step 1: Define Test Scope

Identify the service, process, supplier, system, data set, AI system, facility, or scenario being tested. Define objectives, assumptions, participants by role, and exclusions.

### Step 2: Define Success Criteria

Define measurable criteria including recovery time, recovery point, minimum service level, data integrity, security control restoration, communication timing, supplier response, and business acceptance.

### Step 3: Prepare Test Plan

Document scenario, schedule, roles, evidence requirements, communication plan, rollback method, safety constraints, privacy considerations, and approval to execute.

### Step 4: Execute Test

Perform the test according to the approved plan. Record actions, timing, decisions, deviations, failures, manual workarounds, supplier responses, and observed control issues.

### Step 5: Validate Results

Validate whether success criteria were met. Confirm recovered data, restored services, access control, logging, monitoring, integrations, AI system behaviour, and business acceptance.

### Step 6: Record Findings

Classify findings by severity, owner, corrective action, target date, dependency, and residual risk.

### Step 7: Report and Approve

Prepare a test report with scope, results, evidence, limitations, failed assumptions, corrective actions, residual risk, and approval or acceptance.

### Step 8: Track Improvement

Track corrective actions to closure. Update continuity plans, recovery plans, supplier records, BIA outputs, risk records, and recovery objectives where required.

---

## Required Test Record

| Field | Description |
| --- | --- |
| Test ID | Unique internal identifier. |
| Test Type | Tabletop, walkthrough, restoration, communications, supplier, failover, AI resilience, or other. |
| Scope | Service, process, data set, supplier, system, or scenario tested. |
| Objectives | Expected outcomes. |
| Success Criteria | Measurable criteria for success. |
| Participants by Role | Roles involved in test execution or observation. |
| Actual Recovery Time | Actual time to restore acceptable operation. |
| Actual Recovery Point | Actual point to which data was restored. |
| Issues Identified | Gaps, failures, or limitations found. |
| Corrective Actions | Required remediation and owner. |
| Approval | Role accepting result or residual risk. |
| Evidence Location | Internal evidence reference for adopting organizations. |

---

## Evidence Requirements

Maintain test plans, execution records, screenshots or logs where appropriate for internal use, validation results, communications records, supplier evidence, corrective action logs, and approval records. Public CC0 templates must not include internal screenshots, system names, supplier names, contact details, or operational evidence.

---

**End of Document**
