# Malaysia National Guidelines on AI Governance and Ethics (AIGE)

**Document Title:** Malaysia National Guidelines on AI Governance and Ethics (AIGE)\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-09-25\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`privacy/jurisdictions/annex-privacy-malaysia.md`](../../privacy/jurisdictions/annex-privacy-malaysia.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon a new edition of the Guidelines or a successor to the National AI Roadmap 2021-2025\
**Repository Path:** [`ai/jurisdictions/annex-ai-malaysia.md`](annex-ai-malaysia.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-framework view of Malaysia's National Guidelines on AI Governance and Ethics (AIGE). It presents the Guidelines as a voluntary framework that an organization may take up to demonstrate responsible AI governance in Malaysia. Like the Singapore annex ([`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md)), and unlike the binding annexes in this corpus (for example the EU AI Act annex, [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md)), it is deliberately NOT a binding-obligation annex: the Guidelines create no legal duty, and an adopter's binding Malaysian obligations for personal data sit in the Personal Data Protection Act, covered in [`privacy/jurisdictions/annex-privacy-malaysia.md`](../../privacy/jurisdictions/annex-privacy-malaysia.md).

## Framework and issuing body

The Guidelines are issued by Malaysia's Ministry of Science, Technology and Innovation (MOSTI). They were launched in September 2024, and the PDF MOSTI served when this annex was written (checked 24 September 2026) is a revised file whose name and document metadata are dated 18 November 2024; it differs from the September launch PDF. They support the implementation of the Malaysia National Artificial Intelligence Roadmap 2021-2025 (AI-RMAP), and they describe themselves as a policy document and a living document, to be reviewed regularly and made available in both Malay and English.

The Guidelines are voluntary: they state that they "are on a voluntary for the stakeholders" (source wording), and their aspiration is "the voluntary adoption of the seven AI Principles by developers and deployers of AI alongside existing laws", operationalized "as part of a self-governance mechanism alongside the use of AI assurance techniques when assessing and auditing AI systems". Being voluntary, they set out no enforcement mechanism or penalties of their own. Their stated objectives are to support the AI-RMAP, to facilitate responsible AI according to the seven principles, to build trustworthiness in AI, to manage the risks of AI development and deployment, and to maximize AI's benefits for national productivity, growth, and competitiveness.

## The seven AI principles

The Guidelines adopt seven principles, stated to be in alignment with principles established by UNESCO, the OECD, and the European Commission, among others. Each summary below paraphrases the held text.

1. **Fairness.** AI systems prevent discrimination and provide equal treatment: they do not discriminate on grounds such as race, gender, or religion, developers guard against unintentional bias in data, and the benefits of AI are distributed equitably so that groups are not left without access to them.
2. **Reliability, Safety and Control.** AI systems are reliable and safe, with particular weight in areas such as autonomous vehicles, healthcare, and financial services, and measures are taken to prevent intentional misuse and to keep control over AI systems.
3. **Privacy and Security.** Personal data such as financial and health information is handled through proper procedures, informed consent, and secure storage, in compliance with data-protection law, and security measures protect against hacking and other malicious attacks.
4. **Inclusiveness.** No group is unfairly excluded from AI or its benefits; diverse stakeholders are considered.
5. **Transparency.** An individual can understand what an organization does with personal data in its AI and can access the relevant information; the organization shows how it operates, especially regarding personal data.
6. **Accountability.** Responsibility for the actions and outcomes of AI is identified and assigned during design and deployment, because after a failure it can be hard to attribute to a single person or entity.
7. **Pursuit of Human Benefit and Happiness.** Given prominence as the central principle to which the others connect: AI serves human well-being, a moral responsibility of organizations beyond shareholder return.

## Structure by stakeholder

The Guidelines address three stakeholder groups in separate parts: Part A for end users of AI; Part B for policy makers in government, agencies, organizations, and institutions; and Part C for developers, designers, technology providers, and suppliers ("sector players"). The Guidelines note that one organization can play more than one role: an organization that develops, designs, or supplies AI reads Part C, and one that uses AI products is also an end user under Part A, which the Guidelines apply to organizations as well as individuals. Points of particular relevance to an adopter:

- **Consumer-protection principles (Part A).** The Guidelines set out consumer rights in relation to AI: to information (including awareness when an algorithm uses personal information to make offers or decisions, or reports data to third parties), to object and to receive an explanation, to have personal data deleted, to interact with a human instead of AI, to redress and compensation for damage (including collective redress), and to complain to a supervisory authority or take legal action; they state that developers and deployers of AI are to establish systems through which these rights are available. In a voluntary framework these are recommended practices, not enforceable rights; where Malaysian law separately confers a right (for example under the Personal Data Protection Act), that law governs.
- **Responsible AI in contracts (Part C).** Where a sector player builds AI to a customer's specification, the Guidelines encourage advocating for responsible-AI clauses in contracts with the paying customer, including adherence to ethical guidelines, transparency requirements, and accountability mechanisms across the project lifecycle.
- **Independent advisory body (Part B).** The Guidelines propose a feasibility study for an independent national AI advisory agency, working with the relevant national councils and ministries. This is a proposal, not an established regulator.

## Adopter-role framing

Because the Guidelines are voluntary, an adopter treats the seven principles and the Part C practices as best practices it MAY take up to demonstrate responsible AI in Malaysia, mapping each principle to its existing AI-governance controls rather than to a legal duty. Its binding Malaysian obligations remain those of existing law, principally the Personal Data Protection Act for personal data, which this annex does not restate.

## Relationship to corpus AI-governance content

This annex is the per-framework view; it cross-references the operational substance in the corpus rather than duplicating it. The seven principles map onto the roles, assessment, and transparency practices in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the corpus AI assessment and lifecycle procedures. An adopter aligning to the Guidelines applies those existing corpus controls and records the alignment, noting any recommendation (for example the consumer-protection items on redress) that its current controls do not yet address.

## Limitations

- This annex is voluntary guidance, not legal advice and not a binding obligation; the controlling text is the Guidelines themselves.
- **Version sensitivity.** The Guidelines call themselves a living document, and MOSTI revised the published PDF after launch: the held edition is the revised PDF dated 18 November 2024, which differs from the September 2024 launch document; the September text is retained in the reference base's superseded store. The AI-RMAP they support ran to 2025. An adopter confirms the current edition with MOSTI before reliance.
- The consumer-protection section uses rights language; this annex presents those items as the Guidelines' recommendations, not as rights an individual can enforce under the Guidelines.

## Framework alignment

The Malaysia-principle column is the load-bearing, held-source-grounded content. The NIST AI RMF function tags and the ISO/IEC 42001:2023 clause and Annex A anchors are a crosswalk to help an adopter reuse its existing management-system controls; they are a mapping aid, not an assertion that the voluntary Guidelines and those standards impose the same obligations.

| Malaysia AIGE principle | Corpus AI-governance touchpoint | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Fairness | AI bias and fairness assessment | Map, Measure | Annex A.5 |
| Reliability, Safety and Control | AI testing, monitoring, and human oversight | Measure, Manage | Annex A.6 |
| Privacy and Security | AI data governance and privacy | Map, Manage | Annex A.7 |
| Inclusiveness | AI impact assessment across affected groups | Map | Annex A.5 |
| Transparency | AI model documentation and transparency | Govern, Map | Annex A.8 |
| Accountability | AI compliance roles and responsibility | Govern | Clause 5.3, Annex A.3 |
| Pursuit of Human Benefit and Happiness | AI strategy and societal-impact assessment | Govern, Map | Annex A.5 |
