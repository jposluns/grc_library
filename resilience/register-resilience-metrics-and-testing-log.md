# Resilience Metrics and Testing Log Template

**Document Title:** Resilience Metrics and Testing Log Template  
**Document Type:** Template  
**Version:** 0.0.1  
**Date:** 2026-05-27  
**Owner:** Resilience Owner  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](policy-business-continuity-and-disaster-recovery.md), [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md)  
**Classification:** Public  
**Category:** Resilience  
**Review Frequency:** Annual and upon material resilience, testing, metric, service, supplier, or regulatory change  
**Repository Path:** [`resilience/register-resilience-metrics-and-testing-log.md`](register-resilience-metrics-and-testing-log.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This template provides a reusable structure for recording resilience metrics, continuity tests, recovery tests, crisis exercises, corrective actions, and residual risk decisions.

Completed versions must not be published under CC0 unless sanitized. Real test results, service names, supplier names, system names, people names, incident details, recovery evidence, and internal metrics can reveal operational weakness and must be handled under an adopting organization's internal classification rules.

---

## Use Requirements

1. Record tests and exercises after completion.
2. Use objective measurements where available.
3. Record assumptions, limitations, failed criteria, and residual risk.
4. Track corrective actions to closure.
5. Link testing evidence to business impact analysis, recovery objectives, supplier assessments, AI system continuity records, and risk registers.
6. Do not include real operational evidence in the public CC0 repository.

---

## Section 1: Test and Exercise Log

| Test ID | Test Date | Test Type | Scope | Objective | RTO Target | RTO Actual | RPO Target | RPO Actual | Success Criteria Met | Owner Role | Findings Summary | Residual Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Tabletop, walkthrough, restoration, communications, supplier, failover, AI resilience, or other. |  |  |  |  |  |  |  |  |  |  |

---

## Section 2: Resilience Metrics

| Metric Category | Metric Name | Measurement Rule | Target or Threshold | Current Value | Status | Evidence Class | Owner Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Continuity Coverage | Critical services with current continuity plans | Count or percentage of critical services with approved plans. |  |  |  | Plan register, review record. | Resilience Owner |
| Recovery Objectives | Critical services with approved RTO and RPO | Count or percentage of critical services with approved recovery objectives. |  |  |  | BIA, recovery objective register. | Resilience Owner |
| Recovery Testing | Tests meeting recovery objectives | Count or percentage of recovery tests meeting approved RTO and RPO. |  |  |  | Test report, restoration log. | Resilience Owner |
| Supplier Resilience | Critical suppliers with current resilience assessment | Count or percentage of critical suppliers assessed within required cadence. |  |  |  | Supplier assessment, contract control schedule. | Supplier Owner |
| Corrective Action | Corrective actions closed within target | Count or percentage of corrective actions closed within approved target. |  |  |  | Corrective action log. | Process Owner |
| AI Resilience | AI systems with fallback or disablement method | Count or percentage of AI systems with documented fallback, emergency disablement, or recovery plan. |  |  |  | AI system register, system card, resilience test. | AI Governance Maintainer |
| Data Recovery | Critical data stores with tested restoration | Count or percentage of critical data stores with recent restoration validation. |  |  |  | Backup record, restoration test. | Data Owner |

---

## Section 3: Corrective Action Log

| Action ID | Source | Issue Summary | Corrective Action | Owner Role | Target Date | Completion Date | Status | Verification Method | Residual Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Test, incident, audit, supplier review, BIA, or risk assessment. |  |  |  |  |  | Open, in progress, complete, accepted, deferred. |  |  |

---

## Section 4: Review Summary

| Review Period | Scope | Key Findings | Risk Trend | Improvement Priorities | Approval Role | Review Date |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | Improving, stable, worsening, unknown. |  |  |  |

---

## Evidence Requirements

Adopting organizations should retain test plans, execution records, restoration logs, communication logs, supplier evidence, screenshots or technical records where internally appropriate, corrective actions, risk decisions, and approval records.

---

## Limitations

This template is a public-domain baseline. It does not define an adopting organization's actual resilience thresholds, recovery objectives, supplier obligations, legal obligations, or testing cadence.

---

**End of Document**
