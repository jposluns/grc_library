# Risk Register Procedure

**Document Title:** Risk Register Procedure\
**Document Type:** Procedure\
**Version:** 1.2.0\
**Date:** 2026-06-22\
**Owner:** Chief Risk Officer\
**Approving Authority:** Executive Management\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md), [`risk/annex-ai-risk-methodology.md`](annex-ai-risk-methodology.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material risk process change\
**Repository Path:** [`risk/procedure-risk-register.md`](procedure-risk-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how risks are recorded, maintained, reviewed, escalated, and closed in a risk register.

---

## Procedure

1. **Identify Risk:** Record the risk source, event, consequence, affected process, data, asset, supplier, AI system, service, or obligation.
2. **Assign Owner:** Assign a role accountable for risk treatment and review.
3. **Classify Risk:** Assign domain, category, affected objectives, data sensitivity, regulatory relevance, supplier dependency, and resilience impact.
4. **Assess Inherent Risk:** Evaluate likelihood and impact before additional treatment.
5. **Record Existing Controls:** Identify controls already operating and their evidence.
6. **Assess Control Effectiveness:** Determine whether controls are designed and operating adequately.
7. **Assess Residual Risk:** Evaluate remaining likelihood and impact.
8. **Select Treatment Option:** one of the six canonical options defined in [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md) Section 6: Avoid, Mitigate, Transfer, Accept, Exploit (positive-risk: act to make the upside more likely or larger), or Enhance (positive-risk: increase the likelihood or impact of an existing positive-risk scenario). "Monitor" and "Further Analysis" are NOT treatment options under the canonical set; they are workflow states tracked separately via the standard's **Treatment Status** field (Pending / In Progress / Complete). A risk being monitored is one whose Treatment Option has been selected and whose Treatment Status is Pending or In Progress.
9. **Define Action Plan:** Record actions, owner, due date, dependency, target residual risk, and evidence required.
10. **Review and Escalate:** Escalate overdue, high, critical, or worsening risks according to governance thresholds.
11. **Close Risk:** Close only when treatment is complete, evidence exists, or accountable approval accepts the residual risk.

---

## Minimum register fields

| Field | Description |
| --- | --- |
| Risk ID | Unique identifier. |
| Risk Statement | Clear cause-event-impact statement. |
| Domain | Security, privacy, AI, supplier, resilience, compliance, operational, financial, or other. |
| Owner Role | Accountable role. |
| Affected Asset or Process | Generic service, process, data class, supplier class, or system class. |
| Inherent Likelihood | Pre-treatment likelihood. |
| Inherent Impact | Pre-treatment impact. |
| Existing Controls | Control summary and evidence. |
| Residual Likelihood | Post-control likelihood. |
| Residual Impact | Post-control impact. |
| Treatment Option | One of the six canonical options per [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md) Section 6: Avoid / Mitigate / Transfer / Accept / Exploit / Enhance. |
| Treatment Status | Workflow state of the chosen Treatment Option: Pending / In Progress / Complete. "Monitor" and "Further Analysis" correspond to Pending or In Progress on the canonical six-option set, not to separate treatment options. |
| Action Plan | Required treatment steps. |
| Due Date | Target date. |
| Status | Open / Closed (risk-record lifecycle, per `risk/standard-enterprise-risk-management.md` Section 7.1). The Status field does NOT name the treatment outcome (captured by Treatment Option) or the treatment workflow state (captured by Treatment Status). Prior values "in treatment" / "accepted" / "retired" are retired by this version in favour of the cleaner three-field decomposition. |
| Review Date | Next required review. |
| Evidence Reference | Link to internal evidence in adopting organisation. |

---

## Quality rules

Risk statements must be specific enough to support decision-making. "Cyber risk exists" is not a risk statement; it is the sort of fog bank that turns governance into theatre. A usable risk statement identifies cause, event, impact, and affected objective.

---

**End of Document**
