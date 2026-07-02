# Risk Acceptance Procedure

**Document Title:** Risk Acceptance Procedure\
**Document Type:** Procedure\
**Version:** 1.1.1\
**Date:** 2026-07-02\
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

The High and critical acceptance authorities below align with the canonical approval-authority chain in [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) §2.2 (High or critical: Executive Committee or Board Risk Committee); adopters tune the named bodies to local governance structure there, and this table follows.

| Residual Risk Level | Typical Approval Authority |
| --- | --- |
| Low | Process Owner or Control Owner. |
| Medium | Domain Executive or delegated risk owner. |
| High | Executive Committee or Board Risk Committee, with risk, security, privacy, compliance, or legal consultation where applicable. |
| Critical | Executive Committee or Board Risk Committee (the governing body), or its formally delegated executive risk authority. |

---

## Duration and renewal limits

A risk acceptance is time-bound (the Expiry or review date field below). Renewal requires updated justification and reassessment (step 9). The cumulative lifetime of an acceptance, summed across the initial term and all renewals, must not exceed 540 days unless the Board Risk Committee (or, where the organisation has no Board Risk Committee, the highest governance body to which the Enterprise Risk Committee (ERC) reports) explicitly approves a longer horizon when the acceptance is first recorded, mirroring the exception-register ceiling in [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) Section 3.4. An acceptance created by converting an exception at its renewal ceiling (that policy's Section 3.4 conversion path) counts the exception's elapsed lifetime toward this ceiling, so conversion cannot be used to restart the clock.

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
