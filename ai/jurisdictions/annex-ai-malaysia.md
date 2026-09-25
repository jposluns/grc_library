# Malaysia National Guidelines on AI Governance and Ethics (AIGE)

**Document Title:** Malaysia National Guidelines on AI Governance and Ethics (AIGE)\
**Document Type:** Annex\
**Version:** 0.0.7\
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

The Guidelines adopt seven principles, stated to be in alignment with principles established by UNESCO, the OECD, and the European Commission, among others. They describe the principles in several places (for example, a cascade explained for end users in Part A); the summaries below follow the section that sets out the principles for AI development (Section 2.7.3, "Seven (7) AI Principles"), which itself notes that the descriptions vary between sections and proposes a single consolidated description in a future revision. The Guidelines word several of these points as "must" or "should"; within a voluntary framework they are the Guidelines' recommended practices, not legal duties.

1. **Fairness.** AI development must be designed to avoid bias or discrimination against its target users; AI systems should not take one-size-fits-all approaches and should address the widest possible range of factors (for example age, gender, religion, and ethnicity), enabling equitable access and active participation of all stakeholders.
2. **Privacy and Security.** AI systems should be safe and secure, perform as intended, and resist being compromised by unauthorized parties. Developers should, where necessary, obtain consent from individuals before using or disclosing personal data for AI development and deployment; the systems must guarantee privacy and data protection throughout the AI system's life cycle; information and data collected from users must not be used in an unlawful or discriminatory way against them; and developers should incorporate security-by-design and privacy-by-design principles and refer to international information-security and privacy standards when implementing an AI system.
3. **Reliability, Safety and Control.** AI systems or solutions must be robustly tested to be reliable, safe, and fail-safe by default, so that users can trust and depend on them; for proper access, control and protection in critical situations, they should work reliably and consistently and operate in the real world under normal circumstances and unexpected conditions; and, to prevent or mitigate negative outcomes, they should be able to respond quickly according to their intended purposes. Developers and end users are encouraged to carry out relevant testing and certification and risk and impact assessments, to prevent any potential harm and mitigate risks. Autonomous systems must have safeguards that secure ultimate controllability by humans, particularly for high-risk applications such as autonomous vehicles, military applications, and where human life is at stake.
4. **Inclusiveness.** AI must be inclusive for all stakeholders, to avoid unequal access to AI (the Guidelines give "social clefts" as the case); AI systems should benefit everyone and address national needs and experiences inclusively, in compliance with the Federal Constitution and the National Principles, in three ways: using inclusive development techniques, strategically developing tools sensitive to the specific needs of vulnerable groups, and proactively ensuring diversity among AI developers and decision-makers.
5. **Transparency.** AI algorithms should be transparent so that capabilities can be explained, covering both the technical processes of AI systems and the related human decisions, which allows stakeholders to evaluate AI risks and address issues that arise. The principle applies mainly where AI is used as part of a decision-making process, and the Guidelines name five elements to be adhered to: full disclosure that an AI system is being used in decision-making; the system's intended purpose; the training data (a description of the data used in training, the historical and social biases in it, and the procedures used to verify data quality); maintenance and assessment of the system; and the ability to challenge the system's decisions.
6. **Accountability.** Developers, owners of AI models, and AI actors should be accountable for the success or failure of AI solutions and should take responsibility for ensuring the proper functioning of AI systems in compliance with "AI Acts, governances, and ethical principles" (source wording); in designing AI systems, four elements (system purpose, technology capability, quality and reliability, and sensitive users) need to be considered to avoid consequential harm.
7. **Pursuit of Human Benefit and Happiness.** AI systems should respect human-centred values, pursue human benefit for society, enhance the quality of life, and increase human happiness, and should not be used for malicious purposes in making decisions. Understanding how users interact with AI systems, and how any negative outcomes of AI adoption are perceived, can improve happiness and human well-being. Human oversight helps to ensure that AI systems do not undermine human autonomy, through governance mechanisms such as human-in-the-loop (the capability for human intervention in every decision cycle), human-on-the-loop (the capability for human intervention during the design cycle and in monitoring the system's operation), and human-in-command (the capability to oversee the system's overall activity and to decide when and how to use it).

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
