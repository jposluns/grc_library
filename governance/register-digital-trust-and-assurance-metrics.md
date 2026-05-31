# Digital Trust and Assurance Metrics Register

**Document Title:** Digital Trust and Assurance Metrics Register\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-27\
**Owner:** Assurance Metrics Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md), [`governance/procedure-grc-programme-management-and-annual-review.md`](procedure-grc-programme-management-and-annual-review.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** 6 to 12 months and upon material assurance model change\
**Repository Path:** [`governance/register-digital-trust-and-assurance-metrics.md`](register-digital-trust-and-assurance-metrics.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register defines reusable metric categories for evaluating governance maturity, control coverage, resilience, data protection, supplier assurance, and artificial intelligence governance. Metrics are original, organisation-neutral, and do not reproduce restricted third-party metrics catalogues.

---

## Metric design principles

1. Metrics must have a defined owner, data source, frequency, and interpretation rule.
2. Metrics must distinguish activity from effectiveness.
3. Metrics must not create perverse incentives that reward superficial compliance over risk reduction.
4. Metrics should connect to evidence classes, not unsupported assertions.
5. Metrics should identify known limitations and data-quality issues.
6. Metrics should be reviewed on a 6 to 12 month cadence where risk patterns change.

---

## GRC programme KPI framework

The following KPI categories define the primary measurement dimensions for the GRC programme. Each category maps to one or more governance domains and feeds into the annual programme report to the Executive Review Committee.

| Category | Primary Metric Examples | Frequency |
| --- | --- | --- |
| Governance and Risk | Risk reduction percentage, timely risk closure rate, overdue actions count | Quarterly |
| Information Security and IAM | MFA adoption rate, endpoint compliance percentage, unpatched vulnerability count, incident response time | Monthly |
| Privacy and Data Protection | PIAs completed, cross-border transfer audits, breach containment time | Quarterly |
| AI Governance and Accountability | Percentage of AI systems with model cards and bias assessments, AI incident response completion rate | Quarterly |
| Compliance and Legal | Compliance findings resolved within SLA, percentage of policies reviewed on schedule | Quarterly |
| Supplier Governance | Percentage of critical suppliers with valid certifications, percentage of reassessments completed | Semi-annual |
| Resilience | Recovery testing completion rate, mean time to recover, critical service BIA coverage | Semi-annual |
| Sustainability and ESG | Carbon intensity per compute-hour, percentage of sustainable procurement contracts | Annual |

---

## Digital trust index (DTI)

The DTI is calculated annually as the weighted average of five dimensions, each scored 0 to 5 by the GRC Programme Manager and reviewed by the ERC.

| Dimension | Description |
| --- | --- |
| Integrity | Accuracy and completeness of controls, evidence, and reporting |
| Transparency | Visibility of governance outcomes to stakeholders |
| Accountability | Ownership, escalation, and corrective action timeliness |
| Resilience | Recoverability, continuity testing, and supplier dependency management |
| Ethical Responsibility | AI ethics, privacy compliance, and third-party accountability |

**DTI Thresholds:** 0.0 to 2.4 = Developing; 2.5 to 3.4 = Managed; 3.5 to 4.4 = Integrated; 4.5 to 5.0 = Optimized.

---

## Core metric categories

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

## Metric quality fields

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

## Reporting pattern

| Report | Audience | Content |
| --- | --- | --- |
| Governance Status Report | Governance stakeholders | Review status, approval gaps, exceptions, overdue remediation, document changes. |
| Assurance Report | Risk, compliance, security, privacy, audit | Control evidence coverage, test results, findings, residual risk. |
| AI Governance Report | AI governance stakeholders | AI inventory, risk tiers, impact assessments, data lineage, security test status, exceptions. |
| Resilience Report | Operations, security, risk, executive stakeholders | Recovery testing, critical supplier resilience, BIA coverage, corrective actions. |
| Supplier Assurance Report | Procurement, legal, security, privacy, risk | Due diligence status, contract controls, assurance evidence, concentration risk, exit readiness. |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| COBIT 2019 | MEA01, MEA02: Performance, compliance, and assurance management | KPI governance, digital trust indicators |
| ISO 9001:2015 | §9 to 10: Measurement, analysis, and improvement | Continual improvement metrics |
| ISO/IEC 42001:2023 | §10: AI performance and continual improvement | AI governance KPIs |
| ISO/IEC 27014 | Governance of information security | Security governance performance measurement |
| CSA CCM v4.1 | GOV-09, GOV-10: Governance and digital trust | Control coverage and assurance metrics |

---

## Limitations

Metrics are not proof of compliance by themselves. They require reliable source data, defined ownership, review, supporting evidence, and meaningful thresholds. Poorly designed metrics can industrialize self-deception with charts, which is still self-deception.

---

**End of Document**
