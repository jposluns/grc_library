# Technology Radar Standard

**Document Title:** Technology Radar Standard\
**Document Type:** Standard\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-reference-architecture.md`](standard-reference-architecture.md), [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Quarterly\
**Repository Path:** [`architecture/standard-technology-radar.md`](standard-technology-radar.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard governs how the organisation curates its technology choices over time. The technology radar is a structured way to evaluate, classify, and communicate the organisation's stance on specific technologies, techniques, platforms, languages, and tools.

The radar supports deliberate, accountable technology selection and avoids both unchecked accretion and stagnation.

---

## Scope

This standard applies to:

1. Programming languages used for production systems.
2. Frameworks and libraries with significant footprint.
3. Platforms, runtimes, and cloud services.
4. Development practices, architecture patterns, and engineering techniques.
5. Vendor products and managed services.
6. AI models, providers, and tooling.

It does not govern routine library choice within a programming-language ecosystem (handled by the SCA standard and developer practice).

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Evidence-led | Radar placement is justified by evidence (production use, evaluation, supplier diligence), not opinion alone |
| Curated | A specific function (the technology council) maintains the radar |
| Communicated | The radar is visible to engineering; placement changes are announced |
| Time-bound | Each placement is reviewed at a defined cadence; placements expire if not refreshed |
| Independent | Vendor sales motion does not determine radar placement |
| Honest | Hold-state placements are made when warranted; the radar is not an aspiration list |
| Integrated | The radar feeds into reference architectures, ADRs, supplier assurance, and SCA |

---

## Section 2: rings

The radar uses four rings, consistent with the public ThoughtWorks radar convention used as a vendor-neutral reference.

| Ring | Meaning |
| --- | --- |
| Adopt | Default choice; new systems use this; existing systems migrate to it when natural opportunity arises |
| Trial | Encouraged for selected use; production use is permitted in defined contexts |
| Assess | Worth investigating; not for production use without explicit approval |
| Hold | Not for new use; existing use is expected to wind down |

A placement at Hold does not mean a technology is wrong; it means the organisation is choosing not to invest further.

---

## Section 3: quadrants

The radar organises entries into quadrants:

| Quadrant | Examples |
| --- | --- |
| Languages and frameworks | Programming languages, application frameworks |
| Platforms and tools | Cloud platforms, container platforms, observability platforms, developer tools |
| Techniques | Architecture patterns, engineering practices |
| AI and data | AI models, providers, data platforms, vector stores |

Adopting organisations may add quadrants as warranted.

---

## Section 4: blip structure

Each entry (blip) on the radar has:

| Field | Description |
| --- | --- |
| Title | Specific technology, technique, or platform |
| Quadrant | Per Section 3 |
| Ring | Per Section 2 |
| Direction | Moving toward Adopt, stable, moving toward Hold |
| Owner | Named person or function accountable for the placement |
| Rationale | Why the placement is what it is |
| Conditions of use | Where Trial or Assess, the conditions under which use is permitted |
| Linked ADRs | Architecture decision records justifying the placement |
| Linked supplier assurance | Where the technology is supplier-supplied, linked supplier diligence |
| Linked reference architectures | Where the technology appears in a reference architecture |
| Last reviewed | Date of last review |
| Next review due | Date of next review |
| Sunset path | Where Hold, the path for retiring existing use |

---

## Section 5: lifecycle

| Stage | Trigger | Action |
| --- | --- | --- |
| Proposed | A new candidate is suggested | Recorded in the candidate list; pre-Assess |
| Assess | The technology council accepts the candidate for evaluation | Time-bound evaluation; published with conditions |
| Trial | Evaluation positive; production use in defined contexts | Time-bound; success criteria defined |
| Adopt | Trial successful; broad adoption recommended | Default choice; tooling and reference architectures align |
| Hold | New use discouraged | Existing use wound down per the sunset path |
| Retired | Use is complete | Placement removed from active radar; preserved in history |

Movement between rings is a deliberate decision documented as an ADR.

---

## Section 6: governance

| Element | Description |
| --- | --- |
| Owner | Technology council, chaired by the Chief Architect |
| Cadence | Quarterly review; mid-cycle adjustments where warranted |
| Inputs | Engineering team proposals, supplier-risk signals, security findings, operations signals, customer demands |
| Approval | Council approves placement changes |
| Communication | Each cycle publishes the updated radar with a change-log |
| Escalation | Disputes escalate to the architecture review board |
| Veto | Security, privacy, AI governance, and supplier risk functions may veto placement on serious risk grounds |

---

## Section 7: criteria

The council uses the criteria below when placing a blip. Not every criterion is decisive in every case.

| Criterion | Description |
| --- | --- |
| Maturity | The technology's market and engineering maturity |
| Fit | How well the technology fits the organisation's architecture |
| Engineering experience | Whether the organisation has the skills to operate the technology |
| Operability | The operational characteristics (reliability, observability, scalability) |
| Security and privacy | Security and privacy posture of the technology and its supplier |
| AI considerations | Where AI is involved, the AI risk profile |
| Cost | Acquisition cost, run cost, exit cost |
| Lock-in | The cost of reversal |
| Supplier health | The supplier's continuing viability |
| Community and ecosystem | The strength of the technology's ecosystem |
| Regulatory standing | Any regulatory concerns |
| Sustainability | Environmental and resource implications |

---

## Section 8: relationship to other governance artefacts

| Artefact | Relationship |
| --- | --- |
| Architecture decision records | Movement between rings is documented as an ADR |
| Reference architectures | Reference architectures favour Adopt-ring technologies; Trial-ring technologies appear in reference architectures with conditions |
| Software evaluation, acceptance, and lifecycle standard | The radar feeds the evaluation pipeline; the lifecycle standard handles individual product evaluation |
| Software composition analysis | The radar informs the in-scope inventory the SCA standard analyses |
| Supplier security and privacy assurance | Trial and Adopt placements require supplier assurance evidence where the technology is supplier-supplied |
| Acceptance into service | Acceptance reviews check alignment with the radar |
| Foundation-model lifecycle | AI models are evaluated through the foundation-model lifecycle procedure; placement feeds the AI portion of the radar |

---

## Section 9: AI and the radar

| Concern | Practice |
| --- | --- |
| AI models | Individual model and provider blips placed per the foundation-model lifecycle |
| AI techniques | Patterns (RAG, agentic, fine-tuning) placed as technique blips |
| AI tooling | Vector stores, evaluation frameworks, model-routing tools placed as platform blips |
| Provider concentration | Multiple foundation-model providers held at Adopt or Trial to avoid concentration |
| Velocity | AI quadrant reviewed monthly rather than quarterly due to rate of change |
| Veto | The AI governance council can veto AI placements on risk grounds |

---

## Section 10: handling exceptions

| Situation | Handling |
| --- | --- |
| Production use of an Assess-ring technology | Approved by exception only, recorded as an ADR, time-bound |
| New use of a Hold-ring technology | Exception only, approved by the council, with a sunset plan |
| Trial extension beyond the time-box | Exception with documented rationale |
| Removal of an Adopt-ring technology | Sunset plan; consuming systems given a defined runway |

---

## Operating expectations

1. The radar is reviewed at least quarterly; the AI quadrant more frequently.
2. Each blip has a named owner and a next-review date; expired placements lose visibility.
3. Movement to Adopt is justified by evidence of successful Trial.
4. Movement to Hold has an accompanying sunset path.
5. The radar is published to engineering and is the source of truth for technology stance.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ThoughtWorks Technology Radar | Format and ring conventions | Vendor-neutral reference |
| Open Group TOGAF Standard | Technology Reference Model | Enterprise architecture |
| Open Agile Architecture (O-AA) | Architecture practice | Modern EA practice |
| OWASP SAMM | Operations: Environment Management; Software Composition | Software assurance maturity |
| NIST SSDF SP 800-218 | PW.4 Reuse of existing software | Secure software development |
| ISO/IEC 27001:2022 | A.5.20 Information security in supplier agreements; A.8.30 Outsourced development | Supplier and external software |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. The radar's specific entries and their placements are organisation-specific and time-specific. The radar tooling and publication mechanism are organisation choices. The standard expresses how the radar operates, not the entries themselves.

---

**End of Document**
