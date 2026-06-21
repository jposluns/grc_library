# Risk Acceptance Procedure

**Document Title:** Risk Acceptance Procedure\
**Document Type:** Procedure\
**Version:** 1.0.1\
**Date:** 2026-06-21\
**Owner:** Chief Risk Officer\
**Approving Authority:** Executive Management\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md), [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material risk governance change\
**Repository Path:** [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how residual risk is formally accepted, reviewed, monitored, renewed, or closed. It prevents undocumented risk ownership from being quietly converted into institutional folklore.

---

## Procedure

1. **Identify Residual Risk:** Confirm the risk remaining after current controls and planned treatments.
2. **Validate Ownership:** Assign an accountable owner with authority over the affected process, data, system, supplier, AI system, or service.
3. **Document Context:** Record affected objectives, business justification, alternatives considered, and reason treatment is not immediately completed.
4. **Assess Severity:** Evaluate residual likelihood, impact, control limitations, affected parties, regulatory implications, supplier exposure, data sensitivity, and resilience impact.
5. **Define Compensating Controls:** Identify temporary or alternate controls reducing exposure during the acceptance period.
6. **Set Expiry:** Define an expiry date or event-based review trigger.
7. **Approve:** Obtain approval from the authority required by severity and domain.
8. **Monitor:** Track accepted risks against expiry, control condition, incidents, and material change.
9. **Renew or Close:** Renew only with updated justification and reassessment. Close only when risk is mitigated, transferred, avoided, no longer applicable, or superseded by a new decision.

---

## Approval guidance

| Residual Risk Level | Typical Approval Authority |
| --- | --- |
| Low | Process Owner or Control Owner. |
| Moderate | Domain Executive or delegated risk owner. |
| High | Executive Management with risk, security, privacy, compliance, or legal consultation where applicable. |
| Critical | Governing Body or formally delegated executive risk authority. |

---

## Required record fields

- Risk acceptance ID.
- Risk statement.
- Affected requirement or control.
- Owner role.
- Residual risk rating.
- Business rationale.
- Compensating controls.
- Evidence of review.
- Approval authority.
- Approval date.
- Expiry or review date.
- Monitoring requirement.
- Closure condition.
- Related exception register entry: ID of the corresponding entry in the exception register if this acceptance derives from or relates to a documented policy / control exception (see [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md)); record `None` if the acceptance is a pure risk acceptance unrelated to a policy exception. This linkage makes the two registers cross-traversable: an auditor reviewing an exception can find the corresponding risk acceptance and vice versa.

---

**End of Document**
