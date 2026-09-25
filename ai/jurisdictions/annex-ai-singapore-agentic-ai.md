# Singapore IMDA Model AI Governance Framework for Agentic AI

**Document Title:** Singapore IMDA Model AI Governance Framework for Agentic AI\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-09-25\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md), [`ai/procedure-ai-system-impact-assessment.md`](../procedure-ai-system-impact-assessment.md), [`ai/standard-ai-human-oversight.md`](../standard-ai-human-oversight.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon a new edition of the Framework\
**Repository Path:** [`ai/jurisdictions/annex-ai-singapore-agentic-ai.md`](annex-ai-singapore-agentic-ai.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-framework view of Singapore's Model AI Governance Framework for Agentic AI (the MGF for Agentic AI). It presents the Framework as guidance and best practice that an organization may take up voluntarily to demonstrate trustworthy governance of agentic AI systems. It is deliberately NOT a binding-obligation annex: unlike the EU AI Act annex ([`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md)) or the Colorado annex ([`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md)), the Framework is a voluntary model framework, not legislation, so this annex frames its four dimensions as recommended practices an adopter may map to its own AI-governance controls, never as legal obligations. It is the agentic-AI companion to the generative-AI annex ([`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md)); the two are separate frameworks, each with its own per-framework annex.

## Framework and issuing body

The Model AI Governance Framework for Agentic AI is issued by Singapore's Infocomm Media Development Authority (IMDA), Version 1.5, published 20 May 2026. Unlike the generative-AI Framework, whose held edition is co-issued by IMDA together with the AI Verify Foundation, the held edition of the agentic-AI Framework is attributed to IMDA. It is voluntary: it highlights emerging best practices for a trusted agentic-AI ecosystem, and it carries no legal force, no enforcement mechanism, and no penalties. It is a living document that builds on the responsible-AI practices for organizations set out in the earlier Model AI Governance Framework, extending them to address the new concerns that arise when AI agents act with autonomy. The Framework proposes four dimensions to be viewed as an iterative process rather than a one-time checklist: an anomaly surfaced during implementation or monitoring prompts an organization to re-evaluate the earlier dimensions and bound the risks further.

## The four dimensions

Each dimension below summarizes the recommended practice an adopter may take up voluntarily; the wording paraphrases the held Framework text.

1. **Assess and bound the risks upfront.** The Framework begins by helping organizations assess and bound the risks before deployment. It highlights the risks that should be considered during risk assessment and the design considerations at the planning stage that limit the potential scope of impact of the agents, and that keep agents traceable and controllable. The aim is to right-size an agent's autonomy and reach to the task and its risk before it is given the go-ahead to operate.
2. **Make humans meaningfully accountable.** While agents may act autonomously, human responsibility continues to apply. Once the decision is given to deploy agentic AI, an organization should take immediate steps to make humans meaningfully accountable: clearly defining responsibility across the multiple actors, inside and outside the organization, involved in the agent lifecycle, and taking measures to ensure that human-in-the-loop oversight stays effective over time notwithstanding automation bias.
3. **Implement technical controls and processes.** To operationalize agents safely and reliably, an organization should implement technical controls and processes across the AI lifecycle. During development, guardrails for new components such as planning and tools should be implemented. Before deployment, agents should be tested for baseline safety and reliability. After deployment, agents should be continuously monitored as they interact dynamically with their environment.
4. **Enable end-user responsibility.** Trustworthy deployment of agents does not rest solely on developers; it also depends on end-users. Under the Framework, organizations are responsible for enabling end-user responsibility by equipping end-users with the essential information to use agents appropriately and to exercise effective oversight, while helping them maintain the underlying skills and judgment that oversight requires.

## Adopter-role framing

Because the Framework is voluntary, an adopter treats the four dimensions as best practices it MAY take up to demonstrate trustworthy agentic-AI governance, mapping each dimension to its existing AI-governance controls rather than to a legal duty. This annex deliberately contrasts with the binding annexes in this corpus (the EU AI Act annex and the Colorado annex): those carry enforceable obligations, effective dates, and enforcement regimes, whereas this Framework recommends and does not compel. A reader should not mistake any dimension here for a statutory requirement. The iterative framing matters for adoption: an adopter revisits the assessment dimension whenever monitoring surfaces new agent behaviour, rather than treating the four dimensions as a sequential one-pass exercise.

## Relationship to corpus AI-governance content

This annex is the per-framework view; it cross-references the operational substance in the corpus rather than duplicating it. The four dimensions map onto the risk-assessment, human-oversight, lifecycle, and responsible-use practices already in the corpus: the AI system impact and risk assessment ([`ai/procedure-ai-system-impact-assessment.md`](../procedure-ai-system-impact-assessment.md)), human oversight ([`ai/standard-ai-human-oversight.md`](../standard-ai-human-oversight.md)), the AI development lifecycle and agentic development security, and responsible-use guidance ([`ai/guideline-ethical-ai-use.md`](../guideline-ethical-ai-use.md)). An adopter aligning to the Framework applies those existing corpus controls and records the mapping; this annex supplies the Singapore-specific framing and the dimension-to-control crosswalk below, not new operational requirements.

## Limitations

This annex is voluntary guidance, not legal advice and not a binding obligation; the controlling text is the Framework itself. The held edition is Version 1.5, published 20 May 2026, and the Framework is described as a living document; a voluntary framework is less date-sensitive than legislation, but the current edition is to be confirmed against IMDA before reliance, because IMDA updates the Framework and its companion tools over time, and the specific recommended practices under each dimension evolve with those updates. The dimension descriptions paraphrase the held source; where an adopter needs the exact recommended practice, the held Framework text governs.

## Framework alignment

The Singapore-dimension column is the load-bearing, held-source-grounded content. The NIST AI RMF function tags and the ISO/IEC 42001:2023 clause and Annex A anchors are a crosswalk to help an adopter reuse its existing management-system controls; they are a mapping aid, not an assertion that the voluntary Framework and those standards impose the same obligations.

| Singapore agentic-AI dimension | Corpus AI-governance touchpoint | NIST AI RMF | ISO/IEC 42001:2023 |
| --- | --- | --- | --- |
| Assess and bound the risks upfront | AI system impact and risk assessment; scope and autonomy bounding | Map | Clause 6, Annex A.5 |
| Make humans meaningfully accountable | AI human oversight; roles and responsibility across the agent lifecycle | Govern | Clause 5.3, Annex A.3 |
| Implement technical controls and processes | AI development lifecycle; agentic development security; continuous monitoring | Manage, Measure | Clause 8, Annex A.6 |
| Enable end-user responsibility | Responsible AI use guidance; end-user enablement and skills | Manage | Annex A.8 |
