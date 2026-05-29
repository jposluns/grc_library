# Enterprise Architecture Framework

**Document Title:** Enterprise Architecture Framework\
**Document Type:** Framework\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-reference-architecture.md`](standard-reference-architecture.md), [`architecture/standard-technology-radar.md`](standard-technology-radar.md), [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md), [`architecture/standard-api-design.md`](standard-api-design.md), [`architecture/standard-data-architecture.md`](standard-data-architecture.md), [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md), [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to architecture practice, technology strategy, or organisational structure\
**Repository Path:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This framework defines the enterprise architecture practice: its principles, scope, viewpoints, deliverables, governance forum, and integration with adjacent governance programmes. It expresses outcomes and operating expectations, not a specific toolchain or notation.

The framework supports the organisation in making coherent, consistent, and risk-aware architecture decisions across business, information, application, and technology domains.

---

## Scope

This framework applies to:

1. Strategic architecture decisions affecting more than one product, service, or business unit.
2. Architecture of regulated, customer-facing, safety-relevant, or organisational-critical services.
3. Cross-cutting architecture concerns: identity, integration, data, observability, AI, cloud, and security.
4. New product or service introductions requiring architecture review.
5. Material changes to existing architecture (technology change, vendor change, platform consolidation).

It does not govern routine implementation choices made within an existing reference architecture.

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Outcome-led | Architecture decisions follow from customer and business outcomes, not from technology preference |
| Defensible | Each decision is recorded with rationale and trade-offs |
| Reversible by default | Decisions favour reversibility unless reversibility is impractical |
| Standards-based | Open standards preferred over proprietary lock-in |
| Cloud-aware, not cloud-blind | Cloud is used deliberately; lock-in cost is accounted for |
| Security and privacy by design | Security, privacy, and resilience are inputs to design, not retrofits |
| Sustainable | Operational, financial, and environmental sustainability are inputs to design |
| Composable | Capabilities are composable across products and services |
| Data as a product | Data is treated as a product with ownership, quality, and contract |
| AI-aware | AI is a first-class architectural element with its own governance hooks |
| Bounded innovation | Innovation is encouraged within boundaries that the architecture practice maintains |

---

## Section 2: architecture viewpoints

The framework uses four primary viewpoints, consistent with the spirit of the Open Group TOGAF and ISO/IEC/IEEE 42010 conventions.

| Viewpoint | Scope |
| --- | --- |
| Business architecture | Capabilities, value streams, business processes, organisational roles |
| Information (data) architecture | Data domains, master data, data flow, lifecycle, ownership |
| Application architecture | Applications, services, interfaces, components |
| Technology architecture | Infrastructure, platforms, networks, runtime, security-architecture overlays |

A fifth cross-cutting view, the security and resilience view, overlays all four primary viewpoints. An AI view overlays the four primary viewpoints for AI-bearing architectures.

---

## Section 3: capability model

| Element | Description |
| --- | --- |
| Capability map | A stable description of what the organisation does, decomposed to a working level |
| Capability ownership | Each capability has a named owner |
| Capability maturity | Each capability has a maturity rating |
| Heatmap | Capability map overlaid with investment, risk, technical-debt, or strategic-priority signals |
| Mapping to products and services | Each product or service is mapped to the capabilities it draws on |
| Mapping to systems | Each system is mapped to the capabilities it supports |

The capability map is the spine across business, information, application, and technology architecture.

---

## Section 4: target state and transition

| Element | Description |
| --- | --- |
| Current-state architecture | Documented at a level proportionate to its complexity |
| Target-state architecture | Documented for a defined planning horizon |
| Gap analysis | The gap between current and target is articulated |
| Transition architectures | Intermediate states are documented where the journey is multi-phase |
| Roadmap | Initiatives that progress towards the target state |
| Decision records | Significant decisions are recorded per the ADR standard |
| Reference architectures | Reference architectures express recommended target patterns |

Target-state architecture is updated at least annually and on material strategic change.

---

## Section 5: governance forum

| Forum | Purpose | Cadence |
| --- | --- | --- |
| Architecture review board | Reviews significant architecture decisions and exceptions | Fortnightly or as required |
| Technology council | Owns the technology radar and the technology strategy | Quarterly |
| Data council | Owns data architecture, master data, and data product practice | Quarterly |
| AI architecture council | Owns AI architecture choices and integrates with the AI governance council | Quarterly |
| Security architecture forum | Owns security architecture, integrates with security governance | Monthly |
| Architecture community of practice | Practitioner exchange | Monthly |

Forum membership, decision rights, escalation paths, and recording practice are documented per the role authority register.

---

## Section 6: roles

| Role | Responsibility |
| --- | --- |
| Chief Technology Officer | Accountable for the architecture practice |
| Chief Architect | Owns enterprise architecture and the architecture community |
| Domain architects | Own architecture within a domain (security, data, AI, integration, infrastructure) |
| Solution architects | Lead architecture for products and projects |
| Architecture review board | Reviews significant decisions |
| Architecture community | Practitioner network across the organisation |
| Business architects | Bridge business and technology architecture |

---

## Section 7: deliverables

| Deliverable | Description | Where it lives |
| --- | --- | --- |
| Architecture principles | This framework, Section 1 | This framework |
| Capability map | Capability inventory | Architecture repository |
| Reference architectures | Per the reference architecture standard | Architecture repository |
| Architecture decision records | Per the ADR standard | Per-product repositories or a central ADR store |
| Technology radar | Per the technology radar standard | Architecture repository |
| Architecture review outcomes | Per the architecture review procedure | Architecture review records |
| Solution architecture documents | Per-solution architecture | Per-product repositories |
| Pattern library | Reusable architecture patterns | Architecture repository |
| Anti-pattern catalogue | Known anti-patterns with rationale | Architecture repository |

---

## Section 8: integration with adjacent programmes

| Programme | Integration point |
| --- | --- |
| Enterprise risk | Architecture risk fed into the enterprise risk register |
| Information security | Security architecture overlays; zero trust framework alignment |
| Privacy | Data architecture aligned with privacy-by-design |
| AI governance | AI architecture choices feed the AI governance council |
| Operations and SRE | Operational fitness fed back into architecture |
| Supplier and third-party | Architecture decisions consider supplier concentration |
| Acceptance into service | Architecture review is an input to acceptance |
| Records retention | Data architecture aligned with the retention schedule |
| Sustainability | Carbon and cost implications considered in architecture |

---

## Section 9: fitness functions

Architecture quality is measured continuously through fitness functions and not by point-in-time assessment alone.

| Fitness area | Example function |
| --- | --- |
| Deployment | Deployment frequency, lead time, change failure rate, MTTR |
| Reliability | SLO attainment per service |
| Security | Vulnerability backlog age, control coverage signals |
| Privacy | Data subject request handling time, breach indicators |
| Cost | Cost per customer, cost per transaction, cost-vs-performance |
| Sustainability | Workload efficiency signals |
| Complexity | Service count growth, integration complexity signals |
| Talent | Architecture-coupled skill availability, developer experience signals |

Fitness functions are evolved alongside the architecture; the framework does not freeze a specific measure as the universal truth.

---

## Section 10: operating expectations

1. Significant architecture decisions are recorded as architecture decision records per the ADR standard.
2. Reference architectures are maintained as living artefacts; outdated reference architectures are retired or refreshed.
3. The technology radar is reviewed at least quarterly; assess, trial, adopt, hold states are deliberately managed.
4. The architecture review board has documented decision rights and an escalation path.
5. Architecture practice is itself reviewed annually for fitness, with feedback from product, engineering, security, and operations.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| The Open Group TOGAF Standard | Architecture Development Method, ADM phases | Enterprise architecture |
| ISO/IEC/IEEE 42010:2022 | Architecture description | Architecture viewpoints |
| Open Agile Architecture (O-AA) | Agile enterprise architecture | Modern EA practice |
| IT4IT Reference Architecture | IT value streams | IT operating model |
| C4 model | Architecture documentation notation | Architecture documentation |
| Domain-driven design | Bounded contexts, ubiquitous language | Software architecture practice |
| Team Topologies | Team-system alignment | Socio-technical architecture |
| Wardley mapping | Strategy and evolution | Strategic architecture |
| Accelerate (DORA research) | Capabilities, fitness functions | Engineering performance |
| ISO/IEC 27001:2022 | A.5.1 Policies for information security; A.5.8 Information security in project management | Information security cross-walk |
| NIST CSF 2.0 | Govern function | Risk integration |

---

## Limitations

This framework is a public-domain baseline. The specific notation, tooling, level of formality, and forum cadence are organisation-specific. Adopting organisations select an architecture toolchain, level of formality, and integration depth consistent with their size, regulatory profile, and engineering culture.

---

**End of Document**
