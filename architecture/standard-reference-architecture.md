# Reference Architecture Standard

**Document Title:** Reference Architecture Standard\
**Document Type:** Standard\
**Version:** 1.0.2\
**Date:** 2026-07-01\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-technology-radar.md`](standard-technology-radar.md), [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md), [`architecture/standard-api-design.md`](standard-api-design.md), [`architecture/standard-data-architecture.md`](standard-data-architecture.md), [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to reference-architecture practice or platform stack\
**Repository Path:** [`architecture/standard-reference-architecture.md`](standard-reference-architecture.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard governs how reference architectures are commissioned, authored, reviewed, published, consumed, and kept current. A reference architecture is a documented, recommended pattern for solving a recurring class of problem; consuming teams adopt it directly or justify a deviation.

---

## 2. Scope

This standard applies to:

1. Reference architectures intended for use across more than one team or product.
2. Pattern libraries that codify recurring architecture choices.
3. Reusable building blocks (templates, modules, scaffolds) that embody architecture choices.

It does not apply to per-product solution architecture documents (which are governed by team practice and the architecture review procedure).

---

## 3. Principles

| Principle | Description |
| --- | --- |
| Useful | A reference architecture is adopted because it makes work easier, not because it is mandated alone |
| Opinionated | Reference architectures take a position; ambivalent recommendations are not useful |
| Maintained | Outdated reference architectures are refreshed or retired |
| Composable | Reference architectures compose; one does not contradict another |
| Tested | Recommended patterns are exercised in production, not aspirational only |
| Discoverable | A consuming engineer can find the right reference architecture quickly |
| Bounded | A reference architecture states what it does and does not cover |

---

## 4. Classes of reference architecture

| Class | Description |
| --- | --- |
| Platform reference | The recommended way to build on a specific platform (cloud, container, serverless) |
| Capability reference | The recommended way to implement a capability (identity, payments, notification) |
| Integration reference | The recommended pattern for a class of integration (event-driven, batch, synchronous) |
| Domain reference | A pattern recommended within a business domain |
| Cross-cutting reference | A pattern that applies across many systems (observability, telemetry shape, secret handling) |
| AI reference | A recommended pattern for an AI-bearing system (RAG, agent, evaluation harness) |
| Data reference | A recommended pattern for a data system (lakehouse, streaming, master data) |

---

## 5. Structure of a reference architecture

Each reference architecture document contains:

| Section | Description |
| --- | --- |
| Identification | Title, owner, version, date, maturity level |
| Intent | The problem the reference architecture addresses |
| Scope | What the reference architecture covers and does not cover |
| Audience | Who consumes the reference architecture |
| Context | The conditions under which the reference architecture is appropriate |
| Architecture overview | High-level component view; use C4 or equivalent notation |
| Detailed views | Detailed views as required (data, integration, security, operations) |
| Quality attributes | Reliability, performance, security, privacy, cost, sustainability targets |
| Patterns and anti-patterns | The patterns the reference architecture endorses and the anti-patterns it rejects |
| Technology choices | The technologies the reference architecture uses; alignment with the technology radar |
| Reference implementation | Pointer to a reference implementation (scaffold, module, example) where available |
| Customisation guidance | How consumers tailor the reference architecture |
| Compliance considerations | Regulatory, security, privacy, AI implications |
| Deviation handling | When and how to deviate from the reference architecture |
| Linked ADRs | Architecture decision records that motivated the reference architecture |
| Maturity level | Per the maturity scale below |
| Lifecycle status | Per the lifecycle below |
| Maintenance | Owner, review cadence, sunset criteria |

---

## 6. Maturity scale

| Level | Description |
| --- | --- |
| Sketch | Early-stage concept; not yet adopted |
| Pilot | Validated in one or two systems; suitable for early adopters |
| Established | Adopted broadly; supported by tooling and examples |
| Standardized | Required pattern unless a deviation is approved |
| Sunsetting | Being replaced; new systems should not adopt |
| Retired | No longer in use; preserved for historical context |

The maturity level is a deliberate choice; not all reference architectures need to reach Standardized.

---

## 7. Authoring

| Activity | Description |
| --- | --- |
| Commissioning | The architecture council commissions a reference architecture in response to a recurring need |
| Author | An identified architect or working group is named |
| Stakeholders | Affected engineering, security, privacy, AI, operations, and supplier-risk teams are consulted |
| Draft | The first draft proposes patterns and identifies open questions |
| Review | Reviewed by the architecture review board and affected stakeholders |
| Approval | Approved at a maturity level appropriate to the validation done |
| Publication | Published to the architecture repository with the supporting reference implementation where available |

---

## 8. Consumption

| Activity | Description |
| --- | --- |
| Discovery | Engineers can find the right reference architecture through a searchable index, recommendation engine, or guidance |
| Bootstrap | A reference implementation or scaffold allows quick adoption |
| Customisation | Consumers may customize within the boundaries the reference architecture states |
| Deviation | Consumers may deviate with documented rationale (an ADR) |
| Feedback | Consumers feed back issues, gaps, and successes to the reference-architecture owner |
| Telemetry | Where feasible, adoption is measured (number of consuming systems, deviation count) |

---

## 9. Deviation handling

| Step | Action |
| --- | --- |
| Identify deviation | The consuming team identifies the deviation needed |
| Capture rationale | The rationale is recorded as an ADR |
| Review | The deviation is reviewed by the reference-architecture owner |
| Approve, reject, or escalate | The owner approves, rejects, or escalates to the architecture review board |
| Feed back | Repeated deviations of the same type indicate the reference architecture needs to evolve |

Mandatory reference architectures require formal exception handling per the security exceptions process where the reference architecture embodies a control.

---

## 10. Maintenance

| Activity | Description |
| --- | --- |
| Owner | Each reference architecture has a named owner |
| Review cadence | At least annually; more frequently for high-velocity domains |
| Trigger refresh | New technology, new regulation, new threat, observed pattern failure |
| Sunset criteria | Documented; sunsetting is a deliberate decision, not neglect |
| Communication | Material changes are communicated to consuming teams |
| Versioning | Significant changes increment the reference architecture version |
| Retirement | Retired reference architectures are clearly marked |

---

## 11. Governance integration

| Programme | Integration |
| --- | --- |
| Architecture review | Reference architectures are consulted in architecture review |
| Acceptance into service | Acceptance reviews check alignment with reference architectures |
| Security architecture | Security reference architectures are owned jointly with the security function |
| AI governance | AI reference architectures coordinate with the AI governance council |
| Technology radar | Reference architectures reflect technology choices at adopt or trial state |
| ADRs | Significant choices within a reference architecture are themselves ADRs |
| Pattern library | Patterns within reference architectures contribute to the pattern library |

---

## 12. Quality expectations

| Quality | Indicator |
| --- | --- |
| Adoption | Number and proportion of consuming systems |
| Deviation rate | Where deviation is frequent, the reference architecture is incomplete or wrong |
| Currency | Time since last review; outdated reference architectures lose value quickly |
| Reference implementation health | The reference implementation is itself maintained |
| Consumer satisfaction | Periodic feedback from consuming teams |

---

## 13. Operating expectations

1. Each active reference architecture has a named owner, a review cadence, and a current review date.
2. Outdated reference architectures are marked Sunsetting or Retired; they are not silently abandoned.
3. The reference-architecture catalogue is reviewed by the architecture council at least quarterly.
4. Material deviation patterns trigger refresh.
5. Reference architectures and ADRs are kept consistent; an ADR superseding a reference architecture pattern triggers reference architecture review.

---

## 14. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| The Open Group TOGAF Standard | Architecture Building Blocks; Reference Models | Enterprise architecture |
| ISO/IEC/IEEE 42010:2022 | Architecture description | Architecture documentation |
| C4 model | Architecture notation | Documentation notation |
| Open Agile Architecture (O-AA) | Pattern library practice | Modern EA practice |
| OWASP SAMM | Design | Software assurance maturity |
| NIST CSF 2.0 | Govern function | Risk integration |

---

## 15. Limitations

This standard is a CC BY-SA 4.0 baseline. The notation, repository tooling, and indexing approach are organisation-specific. Reference architectures themselves are organisation-specific; this standard governs how they are produced, not their content.

---

**End of Document**
