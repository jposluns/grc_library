# Australia AI Regulatory Requirements

**Document Title:** Australia AI Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-07-12\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-canada.md`](annex-ai-canada.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`privacy/jurisdictions/annex-privacy-australia.md`](../../privacy/jurisdictions/annex-privacy-australia.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to the Australian AI regulatory landscape\
**Repository Path:** [`ai/jurisdictions/annex-ai-australia.md`](annex-ai-australia.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of Australia's approach to artificial-intelligence governance. Like Canada and unlike the European Union, Australia has **no comprehensive AI statute**: its approach is a voluntary-and-principles-based regime built on largely technology-neutral existing law, with one binding AI-adjacent amendment (a Privacy Act automated-decision transparency obligation). This annex presents the national strategy, the voluntary principles, standard, and current adoption guidance, and the binding privacy amendment, stating each instrument's status (voluntary, strategy, or binding) accurately. It cites the instruments by reference and cross-references the privacy layer rather than restating it.

Alongside [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), and [`ai/jurisdictions/annex-ai-canada.md`](annex-ai-canada.md), this annex is a member of the `ai/jurisdictions/` subdirectory.

## Regulatory posture: voluntary and principles-based

Australia has no omnibus AI law. The government's stated approach is to build on Australia's existing, largely technology-neutral legal and regulatory frameworks, so that established law remains the foundation for addressing AI-related risks, supplemented by voluntary soft-law (the AI Ethics Principles, the Voluntary AI Safety Standard, and the current Guidance for AI Adoption) and targeted or sectoral law. Mandatory guardrails for high-risk AI are under consideration but are **a proposal, not law**. The corpus's operational AI substance is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md); this annex consolidates the Australian regulatory framing.

The lead department is the Department of Industry, Science and Resources (DISR); the National AI Centre (NAIC) publishes the Voluntary AI Safety Standard; the Office of the Australian Information Commissioner (OAIC) regulates the Privacy Act limb.

## National AI Plan 2025

The **National AI Plan 2025** (DISR) sets the government's strategic direction across three goals: capturing the opportunity (investment, capability, and partnerships); spreading the benefits (ensuring all Australians share the advantages of AI); and keeping Australians safe (robust legal, regulatory, and ethical frameworks, ongoing review and adaptation of laws, and the establishment of an AI Safety Institute (AISI)). The Plan states that the government's regulatory approach will continue to build on Australia's existing legal and regulatory frameworks. It is a strategy and policy direction, not a binding obligation on an adopter; the AISI is being established as a body to monitor, test, and share information on AI risks in support of existing regulators, not itself a regulator.

## AI Ethics Principles (voluntary)

Australia's **AI Ethics Principles** (DISR; published 7 November 2019, updated 2 December 2025) are eight **voluntary** principles: human, societal and environmental wellbeing; human-centred values; fairness; privacy protection and security; reliability and safety; transparency and explainability; contestability; and accountability. They are voluntary guidance, not law.

## Voluntary AI Safety Standard (voluntary)

The **Voluntary AI Safety Standard** (National AI Centre, August 2024) sets ten **voluntary** guardrails that apply across the AI supply chain: (1) an accountability process including governance, internal capability, and a regulatory-compliance strategy; (2) a risk-management process; (3) data governance and protection of AI systems; (4) testing and monitoring of AI models and systems; (5) human control and intervention for meaningful human oversight; (6) informing end-users of AI-enabled decisions, AI interactions, and AI-generated content; (7) processes for people impacted by AI to challenge use or outcomes; (8) transparency across the AI supply chain; (9) records to allow third-party assessment of compliance; and (10) stakeholder engagement with a focus on safety, diversity, inclusion, and fairness. The Standard is voluntary; the government has stated that the first nine guardrails align closely with proposed mandatory guardrails, but those mandatory guardrails are a proposal and not law.

## Guidance for AI Adoption (voluntary; the current simplified guidance)

The **Guidance for AI Adoption** (National AI Centre, published 21 October 2025) is the current voluntary guidance for industry, which **condenses the ten guardrails into six essential practices** for safe and responsible AI governance and evolves both the Voluntary AI Safety Standard and the AI Ethics Principles: (1) decide who is accountable; (2) understand impacts and plan accordingly; (3) measure and manage risks; (4) share essential information; (5) test and monitor; and (6) maintain human control. It is voluntary guidance, not a binding instrument; an adopter treats it as the current, simplified expression of the voluntary regime, with the ten guardrails and eight principles as its antecedents.

## Binding AI-adjacent law: Privacy Act automated-decision transparency

The one binding AI-specific obligation is the **automated-decision transparency requirement** added to the Privacy Act 1988 by the Privacy and Other Legislation Amendment Act 2024 (Cth) (No. 128, 2024), which inserts new Australian Privacy Principles (APP) 1.7, 1.8, and 1.9. Where an APP entity has arranged for a computer program to make, or to do a thing substantially and directly related to making, a decision that could reasonably be expected to significantly affect an individual's rights or interests, using the individual's personal information, the entity's **APP privacy policy** must state the kinds of personal information used, the kinds of decisions made solely by such programs, and the kinds of decisions for which a thing substantially and directly related to making the decision is done by such programs. This is a **privacy-policy-content** obligation (the privacy policy must describe the automated decision-making), not an on-request or per-decision individual disclosure.

The obligation is **enacted but not yet in force**: it commences on **10 December 2026** (24 months after the Act's Royal Assent on 10 December 2024), and it applies to decisions made after commencement. (This is a version-sensitive commencement; the adopter confirms the in-force position upstream.)

## Relationship to the Australian privacy regime

Australia's broader Privacy Act reform (the statutory tort for serious invasions of privacy, the children's online privacy code, and the other Privacy and Other Legislation Amendment Act 2024 changes) is carried in [`privacy/jurisdictions/annex-privacy-australia.md`](../../privacy/jurisdictions/annex-privacy-australia.md), which this annex cross-references rather than duplicates; this annex carries only the automated-decision transparency limb precisely, as the AI-specific binding obligation.

## Adopter-role framing

- An organization operating AI in Australia builds on **technology-neutral existing law** (privacy, consumer, anti-discrimination, and sectoral regulation) as the baseline.
- An **APP entity** whose AI makes or substantially assists decisions significantly affecting individuals prepares its APP privacy policy for the automated-decision transparency obligation (in force 10 December 2026).
- Any organization may adopt the **AI Ethics Principles**, the **Voluntary AI Safety Standard**, and the current **Guidance for AI Adoption** (all voluntary) as good practice, noting that the first nine guardrails anticipate the proposed mandatory guardrails and that the Guidance for AI Adoption is the current simplified expression of the voluntary regime.
- No adopter is bound by the National AI Plan (strategy) or by the proposed mandatory guardrails (not law).

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the instruments themselves or for legal advice; the controlling texts are the Privacy Act (as amended), the AI Ethics Principles, the Voluntary AI Safety Standard, the Guidance for AI Adoption, and the National AI Plan.
- **Voluntary versus binding:** the AI Ethics Principles, the Voluntary AI Safety Standard, and the National AI Plan are voluntary or strategic, not binding; the only binding AI-specific obligation is the Privacy Act automated-decision transparency amendment.
- **Not yet in force:** the Privacy Act automated-decision transparency obligation (APP 1.7 to 1.9) commences 10 December 2026; the proposed mandatory guardrails and the AI Safety Institute's statutory footing are prospective. These statuses are version-sensitive; the adopter confirms them upstream before committing to a compliance milestone.
- The corpus operational substance this annex references (the AI classification, impact-assessment, and transparency workflow) is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | Australia instrument | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| National AI strategy and safety institution | National AI Plan 2025 | Govern | Clause 4 |
| Voluntary ethical principles | AI Ethics Principles (8, voluntary) | Govern, Map | Clause 5 |
| Voluntary AI safety guardrails | Voluntary AI Safety Standard (10 guardrails) | Govern, Map, Measure, Manage | Clause 8 |
| Current simplified adoption guidance | Guidance for AI Adoption (6 essential practices) | Govern, Map, Measure, Manage | Clause 8 |
| Automated-decision transparency (binding) | Privacy Act 1988 APP 1.7 to 1.9 (in force 10 December 2026) | Govern | Annex A.8 |

---

**End of Document**
