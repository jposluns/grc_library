# Architecture Review Procedure

**Document Title:** Architecture Review Procedure\
**Document Type:** Procedure\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-reference-architecture.md`](standard-reference-architecture.md), [`architecture/standard-technology-radar.md`](standard-technology-radar.md), [`dev-security/procedure-secure-code-review.md`](../dev-security/procedure-secure-code-review.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to architecture review forum or practice\
**Repository Path:** [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how proposed architectures are reviewed before commitment. It expresses outcomes and operating expectations for the architecture review board (ARB) and for ad-hoc review.

The objective is informed challenge: the proposer leaves the review with a stronger architecture, and the organisation with a recorded decision.

---

## Scope

This procedure applies to:

1. New product or service architectures.
2. Material changes to existing architecture (technology change, integration change, scaling-mode change, security-architecture change).
3. Cross-team architecture proposals.
4. Architecture decisions invoking exception against a reference architecture or the technology radar.
5. AI-bearing architecture choices.
6. Architecture choices with material risk, regulatory, supplier, or cost implications.

It does not apply to routine implementation within an existing reference architecture.

---

## Procedure

### Step 1: Identify a review-worthy change

A change is review-worthy when any of the following apply:

| Trigger | Examples |
| --- | --- |
| Cross-team scope | The change affects more than one product or team |
| Material risk | Security, privacy, AI, supplier-concentration, regulatory implications |
| Material cost | Material capital or operating cost implications |
| Reversibility | The change is hard or expensive to reverse |
| Deviation | The change deviates from a reference architecture or from the technology radar |
| New capability | A new architectural capability is introduced |
| Replacement | A material existing component is replaced |
| AI-bearing | The change introduces, removes, or materially alters an AI element |
| External-facing change | The change affects customers, suppliers, or regulators directly |

If a proposer is uncertain, they contact the architecture function early; an early five-minute conversation often avoids a late surprise.

### Step 2: Pre-review preparation

| Activity | Required output |
| --- | --- |
| Problem statement | The problem being solved, the users affected, and the success criteria |
| Context | Current state; constraints; assumptions; out-of-scope |
| Options | At least two options considered; the trade-offs of each |
| Recommendation | The proposed option with rationale |
| Architecture views | Component view; sequence views as appropriate; data view; security view |
| Quality attributes | Reliability, performance, security, privacy, cost, sustainability targets |
| Risks and dependencies | Identified risks; dependencies on other teams or initiatives |
| Compliance considerations | Regulatory, security, privacy, AI, supplier implications |
| Linked artefacts | Reference architectures, ADRs, radar placements, risk register entries |
| Reviewer list | Suggested reviewers; the architecture function may adjust |

Preparation is proportionate to the change; lightweight proposals are reviewed lightly.

### Step 3: Reviewer assignment

| Change class | Reviewer assignment |
| --- | --- |
| Routine cross-team change | Lead solution architect plus one peer reviewer |
| Significant architecture change | Architecture review board |
| Security-architecture change | Security architecture forum participates |
| Data-architecture change | Data council participates |
| AI-architecture change | AI architecture council participates; AI governance reviewer where the change crosses an AI risk threshold |
| Supplier choice | Supplier risk function participates |
| Regulated capability | Compliance function participates |
| Customer-facing material change | Product leadership participates |

The Chief Architect (or equivalent) designates reviewers on time-bound review windows.

### Step 4: Review forum

| Forum option | Use |
| --- | --- |
| Architecture review board (scheduled) | Standard cadence; major proposals |
| Ad-hoc review | Time-sensitive proposals; the Chief Architect approves the path |
| Asynchronous review | Lightweight proposals; documented in the architecture repository |
| Joint review | Proposals where multiple councils share interest |

Reviews use a consistent agenda: proposer presents, reviewers ask, reviewers caucus, decision is rendered, decision is recorded.

### Step 5: Reviewer dispositions

Reviewers select one of:

| Disposition | Meaning |
| --- | --- |
| Endorse | The proposal is acceptable as presented |
| Endorse with comments | Acceptable; comments are recommendations |
| Request revision | Acceptable in principle; specific items to address before approval |
| Conditional endorsement | Acceptable with documented conditions to be met before, during, or after implementation |
| Block | Not acceptable; specific reasons recorded; path to revision documented |
| Refer | Outside this forum's competence; routed elsewhere |

A block can only be issued for substantive reasons recorded in writing; the proposer has a right to appeal.

### Step 6: Recording the decision

| Element | Required output |
| --- | --- |
| Decision | Recorded as an architecture decision record per the ADR standard |
| Conditions | Conditions are recorded with owner and due date |
| Risks accepted | Material risks accepted are recorded on the relevant risk register |
| Linked artefacts | The decision is linked from the proposal, the reference architectures it affects, and the technology radar entries it touches |
| Communication | Material decisions are communicated to affected teams |
| Follow-up | Follow-up items are tracked and revisited at a defined cadence |

### Step 7: Implementation oversight

| Activity | Description |
| --- | --- |
| Conditions tracking | Conditions are tracked to closure |
| Mid-implementation review | For long-running implementations, mid-implementation reviews verify the architecture is being built as decided |
| Drift detection | Where implementation drifts from the architecture, the change is reviewed back through this procedure |
| Post-implementation review | Outcomes are compared to the success criteria; lessons feed back into reference architectures and the radar |

### Step 8: Closure and learning

| Activity | Description |
| --- | --- |
| Closure record | The architecture is committed; the decision record is finalized |
| Lessons | Lessons feed the architecture practice |
| Pattern extraction | Recurring patterns become candidates for new or updated reference architectures |
| Antipattern recording | Anti-patterns identified are added to the anti-pattern catalogue |
| Metrics update | Architecture-practice metrics update based on outcomes |

---

## Roles

| Role | Responsibility |
| --- | --- |
| Proposer | Brings the proposal; remains accountable for the outcome |
| Chief Architect | Owns the architecture review function |
| ARB members | Provide informed challenge; render dispositions |
| Domain reviewers | Bring domain expertise (security, data, AI, integration) |
| Functional reviewers | Bring functional expertise (privacy, compliance, supplier risk) |
| Architecture community | Source of broader sense-check before forum review |
| Architect-on-call | Triages incoming proposals and assigns reviewer paths |

---

## Section: review quality expectations

| Expectation | Description |
| --- | --- |
| Informed challenge | Reviewers prepare; they do not arrive cold |
| Constructive | The objective is a stronger architecture, not points scored |
| Decisive | Reviews end with a decision; indefinitely-deferred decisions are themselves a decision and are recorded as such |
| Recorded | Outcomes are recorded; verbal-only outcomes do not survive |
| Time-respectful | Review time is treated as scarce; proposers prepare in advance |
| Transparent | Conflicts of interest are declared; reviewer assignment is transparent |
| Accountable | Reviewers accept accountability for the dispositions they render |

---

## Section: appeal

| Step | Description |
| --- | --- |
| Right to appeal | The proposer may appeal a block or a contested condition |
| Appeal forum | The architecture review board chair or the Chief Architect |
| Escalation | The Chief Technology Officer or equivalent for material disagreements |
| Time-bound | Appeals are time-bound; protracted appeals trigger executive escalation |
| Recorded | Appeals and their outcomes are recorded |

---

## Operating expectations

1. The architecture review forum has documented decision rights, cadence, and escalation paths.
2. Proposals carry standard preparation per Step 2; preparation depth scales with change significance.
3. Material decisions are recorded as ADRs; verbal-only decisions are an anti-pattern.
4. Reviewer assignments reflect the substance of the proposal, not seniority alone.
5. Architecture review is a learning function as well as a control function; outcomes feed back into the practice.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| The Open Group TOGAF Standard | Architecture Compliance; Architecture Governance | Enterprise architecture |
| ISO/IEC/IEEE 42010:2022 | Architecture description and review | Architecture practice |
| OWASP SAMM | Design; Architecture Assessment | Software assurance maturity |
| ISO/IEC 27001:2022 | A.5.8 Information security in project management | Information security cross-walk |
| NIST CSF 2.0 | Govern function | Risk integration |
| COBIT 2019 | APO03 Manage enterprise architecture | Governance of enterprise IT |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. The specific forum cadence, reviewer pool, and recording tooling are organisation-specific. The procedure expresses outcomes, not a vendor-specific implementation.

---

**End of Document**
