# Architecture Domain

**Document Title:** Architecture Domain README\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-28\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](../README.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to enterprise architecture practice or technology stack\
**Repository Path:** [`architecture/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This directory contains the architecture governance artefacts for the library: the enterprise architecture framework, the architecture decision record standard, reference-architecture practice, technology selection practice, architecture review, API design, data architecture, and integration architecture. All content is released under CC0 1.0 Universal.

The architecture domain complements (and does not duplicate) the security, dev-security, AI, operations, and risk domains. Security-, AI-, and operations-relevant architecture controls live in their primary domain; this domain governs the architecture practice itself.

---

## Active documents

| Type | Title | Path |
| --- | --- | --- |
| Framework | Enterprise Architecture Framework | [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md) |
| Standard | Architecture Decision Records Standard | [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md) |
| Standard | Reference Architecture Standard | [`architecture/standard-reference-architecture.md`](standard-reference-architecture.md) |
| Standard | Technology Radar Standard | [`architecture/standard-technology-radar.md`](standard-technology-radar.md) |
| Procedure | Architecture Review Procedure | [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md) |
| Standard | API Design Standard | [`architecture/standard-api-design.md`](standard-api-design.md) |
| Standard | Data Architecture Standard | [`architecture/standard-data-architecture.md`](standard-data-architecture.md) |
| Standard | Integration Architecture Standard | [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md) |

---

## Domain coverage

The architecture domain covers:

- **Enterprise architecture**: the architecture framework, principles, viewpoints, capability mapping, target-state architecture, transition architectures, and architecture governance forum.
- **Architecture decision records**: the practice of recording significant architecture decisions in immutable, versioned, searchable records.
- **Reference architecture**: how reference architectures are commissioned, authored, kept current, and consumed.
- **Technology selection**: the technology radar practice and the lifecycle states (assess, trial, adopt, hold).
- **Architecture review**: the architecture review board, fitness-for-purpose review, and architecture-as-design-input gating.
- **API design**: design principles, versioning, identifiers, error model, and longevity.
- **Data architecture**: data modelling, data ownership, master data, data integration, and data product practice.
- **Integration architecture**: event-driven, messaging, synchronous, batch, and integration patterns.

---

## Relationship to adjacent domains

| Adjacent domain | Boundary |
| --- | --- |
| Security | Security architecture controls (zero trust, segmentation, IAM patterns) live in security; architecture practice for security-relevant architecture lives here |
| Dev-security | Application security controls live in dev-security; API design as architecture practice lives here, API security as a control standard lives in dev-security |
| AI | AI governance, model risk, and AI security live in AI; AI-aware architecture practice lives here |
| Operations | Infrastructure operating practice lives in operations; reference architectures for operational platforms live here |
| Risk | Enterprise risk methodology lives in risk; architecture risk is fed by architecture review and recorded against the risk registers |
| Data privacy | Privacy controls live in privacy; data architecture's privacy-by-design hooks are referenced from privacy |

---

**End of Document**
