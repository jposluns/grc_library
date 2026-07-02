# Minimum Viable Governance Structure Guideline

**Document Title:** Minimum Viable Governance Structure Guideline\
**Document Type:** Guideline\
**Version:** 1.0.4\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/register-role-authority.md`](register-role-authority.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the library's role or forum vocabulary\
**Repository Path:** [`governance/guideline-minimum-viable-governance-structure.md`](guideline-minimum-viable-governance-structure.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

The library references multiple governance forums (AI Governance Council, Enterprise Risk Committee, Board Risk Committee, Architecture Review Board, Change Advisory Board, Data Council, Reliability Council, Capacity Council, and others). A small or mid-sized organization cannot staff all of these as discrete bodies. This guideline shows how an adopting organization can implement the library's governance content at three maturity tiers, consolidating forums where appropriate and naming clear seats for the responsibilities the library assigns.

This guideline is non-binding; it is adopter guidance. The library's individual documents continue to reference the formal forum names (which a large organization may have as discrete bodies). This document describes how a smaller organization maps those formal names to a leaner structure without losing the underlying accountability.

---

## Scope

This guideline applies to:

1. Organizations adopting the library who need to decide which formal forums to instantiate as discrete bodies and which to combine.
2. Smaller organizations (no dedicated risk function, no separate AI governance body) seeking a minimum-viable starting point.
3. Maturing organizations that have outgrown a leaner structure and need a target-state design.

It does not redefine the formal forum names used elsewhere in the library; it shows the consolidation patterns that preserve the responsibilities.

---

## Three tiers of governance structure

The guideline describes three reference structures. Adopting organizations choose the tier that matches their size, complexity, and regulatory profile.

| Tier | Profile | Number of discrete forums |
| --- | --- | --- |
| Tier 1: Minimum viable | Small organization (under approximately 200 staff, low regulatory exposure, no high-risk AI in production) | 2-3 |
| Tier 2: Mid-market | Mid-sized organization (200-2,000 staff, sector-regulated, some production AI) | 4-6 |
| Tier 3: Enterprise / regulated | Large organization, multiple jurisdictions, financial-services or healthcare-grade regulation, material AI portfolio | 8-12 (close to the library's full forum vocabulary) |

---

## Tier 1: Minimum viable

A small organization can implement the library's governance content with two named bodies plus the founder / CEO / equivalent for board-level decisions.

| Library forum | Tier-1 home |
| --- | --- |
| Governing Body / Board | Founder, CEO, or equivalent decision-maker |
| Enterprise Risk Committee | Combined executive forum (whatever cross-functional senior meeting already runs weekly or fortnightly) |
| AI Governance Council | Same as above (with AI-specific items as standing agenda when an AI item exists) |
| Architecture Review Board | Same as above (as standing agenda) |
| Change Advisory Board | Same as above (as standing agenda) or delegated to the IT Operations Lead |
| Data Council | Same as above (as standing agenda) |
| Audit and Risk Committee | Where no formal audit committee exists, the founder/CEO with an external advisor reviewing periodically |
| Reliability Council, Capacity Council, Technology Council | Standing agenda items in the executive forum |

Named seats: the executive forum should still record decisions against the formal roles the library uses (CISO, CIO, CRO, CCO, DPO, etc.). One person may wear multiple role hats; in that case, record which role's authority a given decision invokes.

Key practice: the *responsibilities* the library assigns to each forum remain accountable; the discrete *forum* is consolidated.

---

## Tier 2: Mid-market

A mid-sized organization typically instantiates four to six discrete bodies.

| Body | Library forums combined |
| --- | --- |
| Board (or equivalent) | Governing Body |
| Executive Committee | Executive Management, Audit Committee (where the board does not have a separate audit committee) |
| Enterprise Risk Committee | Enterprise Risk Committee, Risk Committee, Insider Risk Steering Committee |
| Technology / Architecture Council | Architecture Review Board, Technology Council, Data Council, AI Governance Council (with AI-specific working groups as needed), Reliability Council, Capacity Council |
| Change Advisory Board | Change Advisory Board (often the only purely operational body separate from technology council) |
| Ethics and Compliance Committee | Ethics Committee, Ethics and Compliance Committee, Whistleblower oversight |

A mid-market organization might add an AI Governance Council as a separate body when the AI portfolio reaches a complexity that warrants dedicated cadence; otherwise the technology council carries AI items.

---

## Tier 3: Enterprise / regulated

A large or regulated organization typically instantiates most of the library's named forums as discrete bodies. The library's individual document references then map one-to-one onto the organization's actual forums.

At this tier:

- The Board has separate Risk and Audit Committees (or equivalent), each with documented terms of reference.
- The AI Governance Council is a discrete body with the composition documented in [`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md).
- The Architecture Review Board, Technology Council, Data Council are discrete with documented decision rights.
- The Insider Risk Steering Committee exists as a discrete cross-functional body.
- The Change Advisory Board is a discrete operational body.

Even at this tier, the library's forum vocabulary is the maximum; an organization may still consolidate forums that don't justify discrete cadence in its context.

---

## Seat names

Across all tiers, the library's role vocabulary remains the same. The roles are defined in [`governance/register-role-authority.md`](register-role-authority.md). At Tier 1 one person may hold multiple roles; at Tier 3 each role has a dedicated incumbent.

The roles fall into four groups:

| Group | Roles | Tier 1 typical incumbents |
| --- | --- | --- |
| Senior executive | CEO/equivalent, CIO, CISO, CRO, CCO, DPO, CTO, CFO, CHRO, General Counsel, Chief Audit Executive | One or two people wearing several hats |
| AI sub-roles (when AI is in scope) | AI Governance Lead, AI Governance Approver, AI Data Steward, AI System Inventory Keeper, AI Risk Maintainer, AI Security Maintainer | One role-holder covers all four AI roles; the CISO or CIO is often the AI Governance Lead |
| Ownership roles | System Owner, Data Owner, Control Owner, Process Owner, Supplier Owner, Resilience Owner, Security Owner, Communications Owner | Per-system / per-process; can be the operator who runs the thing |
| Maintainer roles | Document Owner, Supplier Risk Maintainer, Compliance Maintainer, Privacy Maintainer, Risk Maintainer, Information Security Maintainer, Control Framework Maintainer, Assurance Metrics Maintainer | One role-holder covers several maintainer functions |

---

## Mapping the library to your structure

When adopting the library, document the mapping between the library's formal forum names and your actual structure. The mapping document does not need to be lengthy; a short table suffices.

Example (Tier 1):

| Library forum | Our equivalent | Cadence |
| --- | --- | --- |
| AI Governance Council | Executive forum (AI items on agenda) | Weekly |
| Architecture Review Board | Executive forum (architecture items on agenda) | Weekly |
| Enterprise Risk Committee | Executive forum (risk items on agenda) | Weekly |
| Change Advisory Board | IT Operations Lead approval list | Continuous |

This mapping makes the library's documents auditable in your context: a reader of, say, the AI governance framework can determine which body in your organization actually exercises the council's authority.

---

## Quality expectations

The mapping has succeeded when:

| Element | Indicator |
| --- | --- |
| Every responsibility the library names has a named owner in your structure | All library role names map to at least one named individual |
| Every approval the library requires has a decision-maker | No library `shall` operates without a corresponding accountable role |
| Every cadence the library expects has a forum | Quarterly reviews actually happen quarterly; the forum is identified |
| The mapping survives personnel change | Roles, not people, are the authoritative bindings |
| The mapping is reviewed at least annually | The annual library health report (per the library quality and review cadence procedure) verifies the mapping remains current |

---

## Operating expectations

1. Choose a tier deliberately; do not aspire to Tier 3 if your operating context is Tier 1.
2. Document your mapping in a short internal artefact; do not rely on tacit knowledge.
3. Revisit the mapping as your organization grows. Tier transitions are deliberate decisions, recorded against the appropriate body.
4. Where consolidation is chosen, agenda items still record which library responsibility is being exercised, so audit and review remain possible.
5. Where you cannot map a library responsibility to any body, treat that as a finding and either accept the responsibility gap deliberately (with a documented rationale) or stand up the corresponding forum.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 37000:2021 | Governance of organizations | Governance maturity guidance |
| ISO/IEC 27001:2022 | A.5.2 Information security roles and responsibilities | Role and forum design |
| ISO/IEC 42001:2023 | §5 Leadership | AI governance leadership |
| COBIT 2019 | EDM (Evaluate, Direct, Monitor) processes | Governance forum design |
| OECD G20 Principles of Corporate Governance | Board structure | Governance structure |
| IIA Three Lines Model 2020 | Lines of defence | Forum role separation |

---

## Limitations

This guideline is a CC BY-SA 4.0 baseline. The mapping an organization produces is organization-specific. The guideline does not prescribe which forums must exist for a specific regulatory regime; sector regulators (financial-services, healthcare, critical infrastructure) may require specific bodies with specific compositions. Adopting organizations confirm sector-specific requirements with subject-matter experts.

---

**End of Document**
