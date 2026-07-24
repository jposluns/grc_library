# Singapore Model AI Governance Framework for Generative AI

**Document Title:** Singapore Model AI Governance Framework for Generative AI\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-07-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon a new edition of the Framework\
**Repository Path:** [`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-framework view of Singapore's Model AI Governance Framework for Generative AI. It presents the Framework as guidance and best practice that an organization may take up voluntarily to demonstrate trustworthy generative-AI governance. It is deliberately NOT a binding-obligation annex: unlike the EU AI Act annex ([`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md)) or the Colorado annex ([`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md)), the Framework is a voluntary model framework, not legislation, so this annex frames its nine dimensions as recommended practices an adopter may map to its own AI-governance controls, never as legal obligations.

## Framework and issuing body

The Model AI Governance Framework for Generative AI is issued by Singapore's Infocomm Media Development Authority (IMDA) together with the AI Verify Foundation, published 30 May 2024. It is voluntary: it recommends practices for a trusted generative-AI ecosystem, and it carries no legal force, no enforcement mechanism, and no penalties. It builds on the earlier Model AI Governance Framework for traditional AI (first released in 2019 and updated in 2020), whose concerns are carried forward chiefly under the Trusted Development and Deployment dimension below. The Framework proposes nine dimensions to be looked at in totality, so that they foster a trusted ecosystem rather than being applied in isolation.

## The nine dimensions

Each dimension below summarizes the recommended practice an adopter may take up voluntarily; the wording paraphrases the held Framework text.

1. **Accountability.** Put the right incentive structures in place so that the players along the AI development chain are responsible to end-users. Because generative AI, like most software, spans multiple layers of the technology stack, the allocation of responsibility may not be immediately clear; useful parallels with today's cloud and software-development stacks let an adopter take practical first steps in assigning it.
2. **Data.** Data is a core element of model development and significantly affects output quality, so the data fed to a model matters and its quality needs attention, for example through the use of trusted data sources. Where the use of training data is potentially contentious, such as personal data or copyright material, the aim is to give business clarity, treat affected parties fairly, and handle the data pragmatically.
3. **Trusted Development and Deployment.** Model development, and the application deployment built on top of it, are at the core of AI-driven innovation. Despite the limited visibility end-users may have into how a model is built, meaningful transparency about the baseline safety and hygiene measures undertaken is key, achieved through best practices in development and evaluation and through "food label"-style transparency and disclosure.
4. **Incident Reporting.** No software in use today is completely foolproof, and the same applies to AI. Incident reporting is an established practice that enables timely notification and remediation, so structures and processes for incident monitoring and reporting are key, and they also support the continuous improvement of AI systems.
5. **Testing and Assurance.** Third-party testing and assurance plays a complementary role, as it does in domains such as finance and healthcare, by enabling independent verification. Adopting third-party testing and assurance helps an organization demonstrate trust to its end-users, and common standards for AI testing support quality and consistency.
6. **Security.** Generative AI introduces the potential for new threat vectors against the models themselves, beyond the security risks inherent in any software stack. Existing information-security frameworks need to be adapted, and new testing tools developed, to address these risks.
7. **Content Provenance.** AI-generated content, because of the ease with which it can be created, can worsen misinformation. Transparency about where and how content is generated helps end-users consume online content in an informed way; technical solutions such as digital watermarking and cryptographic provenance are relevant, applied in the right context.
8. **Safety and Alignment Research and Development (R&D).** The current state of the science for model safety does not fully cover all risks, so accelerated investment in R&D is required to improve the alignment of models with human intention and values, and global cooperation among AI safety R&D institutes is critical to using limited resources for maximum impact.
9. **AI for Public Good.** Responsible AI goes beyond risk mitigation to uplifting and empowering people and businesses, through democratizing access to AI, improving public-sector AI adoption, upskilling workers, and developing AI systems sustainably.

## Adopter-role framing

Because the Framework is voluntary, an adopter treats the nine dimensions as best practices it MAY take up to demonstrate trustworthy generative-AI governance, mapping each dimension to its existing AI-governance controls rather than to a legal duty. This annex deliberately contrasts with the binding annexes in this corpus (the EU AI Act annex and the Colorado annex): those carry enforceable obligations, effective dates, and enforcement regimes, whereas this Framework recommends and does not compel. A reader should not mistake any dimension here for a statutory requirement.

## Relationship to corpus AI-governance content

This annex is the per-framework view; it cross-references the operational substance in the corpus rather than duplicating it. The nine dimensions map onto the roles, assessment, and model-documentation practices in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the corpus AI assessment and lifecycle procedures. An adopter aligning to the Framework applies those existing corpus controls and records the mapping; this annex supplies the Singapore-specific framing and the dimension-to-control crosswalk below, not new operational requirements.

## Limitations

This annex is voluntary guidance, not legal advice and not a binding obligation; the controlling text is the Framework itself. The held edition is dated 30 May 2024; a voluntary framework is less date-sensitive than legislation, but the current edition is to be confirmed against the issuing bodies before reliance, because the AI Verify Foundation and IMDA update the Framework and its companion tools over time, and the specific recommended practices under each dimension evolve with those updates.

## Framework alignment

The Singapore-dimension column is the load-bearing, held-source-grounded content. The NIST AI RMF function tags and the ISO/IEC 42001:2023 clause and Annex A anchors are a crosswalk to help an adopter reuse its existing management-system controls; they are a mapping aid, not an assertion that the voluntary Framework and those standards impose the same obligations.

| Singapore dimension | Corpus AI-governance touchpoint | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Accountability | AI compliance roles and responsibility | Govern | Clause 5.3, Annex A.3 |
| Data | AI data governance and dataset documentation | Map, Measure | Annex A.7 |
| Trusted Development and Deployment | AI development lifecycle and model documentation and transparency | Map, Manage | Clause 8, Annex A.6 |
| Incident Reporting | AI incident management | Manage | Clause 10, Annex A.8 |
| Testing and Assurance | AI evaluation and third-party assurance | Measure | Clause 9, Annex A.6 |
| Security | AI and agentic development security | Manage | Annex A.6 |
| Content Provenance | AI content provenance and watermarking | Map, Manage | Annex A.8 |
| Safety and Alignment R&D | AI safety and alignment posture | Measure, Manage | Clause 10 |
| AI for Public Good | AI strategy and responsible-adoption framing | Govern | Clause 4 |
