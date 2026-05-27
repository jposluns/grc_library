# Digital Trust and Assurance Metrics Register

**Document Title:** Digital Trust and Assurance Metrics Register
**Document Type:** Register
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Assurance Metrics Maintainer
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `governance/charter-governance-library.md`, `governance/matrix-cross-framework-alignment.md`, `resilience/framework-business-continuity-and-resilience.md`, `ai/framework-ai-governance-and-risk.md`
**Classification:** Public
**Category:** Core Governance
**Review Frequency:** 6 to 12 months and upon material assurance model change
**Repository Path:** `governance/register-digital-trust-and-assurance-metrics.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This register defines reusable metric categories for evaluating governance maturity, control coverage, resilience, data protection, supplier assurance, and artificial intelligence governance. Metrics are original, organization-neutral, and do not reproduce restricted third-party metrics catalogues.

---

## Metric Design Principles

1. Metrics must have a defined owner, data source, frequency, and interpretation rule.
2. Metrics must distinguish activity from effectiveness.
3. Metrics must not create perverse incentives that reward superficial compliance over risk reduction.
4. Metrics should connect to evidence classes, not unsupported assertions.
5. Metrics should identify known limitations and data-quality issues.
6. Metrics should be reviewed on a 6 to 12 month cadence where risk patterns change.

---

## Core Metric Categories

| Category | Example Metric | Measurement Intent | Evidence Class | Frequency |
| --- | --- | --- | --- | --- |
| Governance Coverage | Percentage of active documents with owner, approver, review date, and repository path. | Tests policy corpus maintainability. | Document index, metadata scan. | Quarterly. |
| Review Timeliness | Percentage of documents reviewed within required cadence. | Tests governance hygiene. | Review log, pull request history. | Quarterly. |
| Exception Discipline | Percentage of active exceptions with owner, expiry, compensating control, and residual risk. | Tests risk acceptance control. | Exception register. | Monthly or quarterly. |
| Control Evidence Coverage | Percentage of mapped controls with current evidence. | Tests assurance completeness. | Evidence register, control matrix. | Quarterly. |
| Control Test Effectiveness | Percentage of tested controls meeting acceptance criteria. | Tests operating effectiveness. | Test records, audit results. | Quarterly. |
| Remediation Timeliness | Percentage of remediation actions closed within target. | Tests corrective action execution. | Issue tracker, audit log. | Monthly. |
| Supplier Assurance Coverage | Percentage of critical suppliers with current assessment and contractual control review. | Tests external dependency governance. | Supplier register, assessment record. | Quarterly. |
| Resilience Test Completion | Percentage of critical services tested against recovery objectives. | Tests recoverability. | BIA, test report, corrective action log. | Semi-annual or annual. |
| Privacy Assessment Coverage | Percentage of high-risk processing activities with current impact assessment. | Tests privacy governance. | Data inventory, impact assessment. | Quarterly. |
| AI System Inventory Coverage | Percentage of AI systems with assigned owner, risk tier, data classification, lifecycle status, and approval state. | Tests AI governance control boundary. | AI system register. | Monthly or quarterly. |
| AI Data Lineage Coverage | Percentage of AI systems with documented data provenance, lineage, retention, and deletion method. | Tests data-risk control. | Data lineage record, model documentation. | Quarterly. |
| AI Security Testing Coverage | Percentage of AI systems tested for prompt injection, data leakage, unsafe tool use, and access-control failure. | Tests AI-specific control effectiveness. | Security test record, red-team record. | Release and periodic. |

---

## Metric Quality Fields

Each metric should define:

- Metric name.
- Objective.
- Calculation rule.
- Numerator.
- Denominator.
- Data source.
- Data owner.
- Control owner.
- Frequency.
- Target or threshold.
- Reporting audience.
- Known limitations.
- Escalation trigger.
- Related document.

---

## Reporting Pattern

| Report | Audience | Content |
| --- | --- | --- |
| Governance Status Report | Governance stakeholders | Review status, approval gaps, exceptions, overdue remediation, document changes. |
| Assurance Report | Risk, compliance, security, privacy, audit | Control evidence coverage, test results, findings, residual risk. |
| AI Governance Report | AI governance stakeholders | AI inventory, risk tiers, impact assessments, data lineage, security test status, exceptions. |
| Resilience Report | Operations, security, risk, executive stakeholders | Recovery testing, critical supplier resilience, BIA coverage, corrective actions. |
| Supplier Assurance Report | Procurement, legal, security, privacy, risk | Due diligence status, contract controls, assurance evidence, concentration risk, exit readiness. |

---

## Limitations

Metrics are not proof of compliance by themselves. They require reliable source data, defined ownership, review, supporting evidence, and meaningful thresholds. Poorly designed metrics can industrialize self-deception with charts, which is still self-deception.

---

**End of Document**
