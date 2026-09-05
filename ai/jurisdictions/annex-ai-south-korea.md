# South Korea AI Regulatory Requirements

**Document Title:** South Korea AI Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-09-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`ai/jurisdictions/annex-ai-singapore.md`](annex-ai-singapore.md), [`privacy/jurisdictions/annex-privacy-south-korea.md`](../../privacy/jurisdictions/annex-privacy-south-korea.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to the AI Basic Act, its Enforcement Decree, or Ministry of Science and ICT implementing guidelines\
**Repository Path:** [`ai/jurisdictions/annex-ai-south-korea.md`](annex-ai-south-korea.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of South Korea's comprehensive national AI statute, the Framework Act on the Development of Artificial Intelligence and Establishment of Trust (widely cited as the "AI Basic Act"), Law No. 20676, enacted 21 January 2025 and in force since 22 January 2026. It sits alongside the other `ai/jurisdictions/` annexes and is the corpus's first binding-statute annex for the Asia-Pacific region (Singapore's is a voluntary framework). In shape the Act resembles the EU AI Act more than the US state laws, a risk-tiered ("high-impact AI"), economy-wide, extraterritorial statute carrying transparency, safety, and human-oversight duties, but it is materially lighter: a promotion-first framework law whose binding duties are few, whose operative thresholds are largely delegated to Presidential Decree, and whose maximum administrative fine is 30 million won. This annex frames the Act's provisions and cross-references the operational substance rather than restating it.

**Translation provenance (governs every quotation below).** The reference base holds an unofficial English translation of the Act (the CSET Georgetown University translation, dated 9 July 2025, of the Korean text published by the Korean Law Information Center under the Ministry of Government Legislation). The official text is Korean and controls; every quotation in this annex is from that held English translation and is identified as such, and any binding use requires verification against the official Korean text. The Act's statutory purpose, as the held translation renders Article 1, is "to protect human rights and dignity, and to contribute to enhance the quality of life, while strengthening national competitiveness by establishing essential regulations for the sound development of artificial intelligence (AI) and the establishment of trust."

## Applicable law and regulatory authority

- **The statute** is the Framework Act on the Development of Artificial Intelligence and Establishment of Trust, Law No. 20676, marked in the held translation "[Enforced January 22, 2026] [Law No. 20676, Enacted January 21, 2025]". The translator notes that a more literal rendering of the title begins "Basic Act on the Development of Artificial Intelligence...", which is the source of the common short name "AI Basic Act".
- **The enforcing authority is the Minister of Science and ICT (MSIT).** Under the held translation the Minister establishes the triennial AI Basic Plan (Article 6), confirms high-impact status on request and may issue related guidelines (Article 33), receives the Article 32 safety-measure results, receives domestic-representative reports (Article 36), conducts investigations and issues corrective orders (Article 40), and imposes and collects the administrative fines (Article 43).
- **Framework-act character (Article 5).** The held translation provides that, unless other laws contain special provisions on AI, this Act applies, and that later AI-related laws are to be aligned with its purposes.
- The controlling text is the Korean statute. Version-sensitive facts (the citation form and the enactment and enforcement dates) are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (the South Korea AI Basic Act row); this annex cross-references them rather than re-deriving them.

## Transition timeline

- **Already in force.** The Act took effect 22 January 2026, one year after promulgation; under the held translation's Addenda Article 1 the Act enters into force one year after the date of its promulgation, with the digital-medical-devices slice of the high-impact definition entering into force 24 January 2026. Both dates have passed, so the regime is live at the time of writing.
- **The operative detail still awaited is decree- and guideline-level.** Nearly every threshold and much of the operative detail is delegated to the Presidential Decree (the Enforcement Decree) and to MSIT guidelines; the reference base does not hold the Enforcement Decree, and this annex asserts no decree-level value (see Limitations).
- **Institutional sunset.** The held translation provides that the National AI Committee subsists for five years from the date the Act takes effect (Article 7).

## Scope: covered actors and covered systems

Definitions are from Article 2 of the held translation:

- **Artificial intelligence** is defined as "the electronic implementation of human intellectual abilities, such as learning, reasoning, perception, judgment, and understanding of language."
- **AI system** is defined as "an AI-based system that infers results such as predictions, recommendations, and decisions that affect the real and virtual environment for a given objective with various levels of autonomy and adaptability." (This is recognizably OECD-derived, like the EU AI Act's system definition; a side-by-side comparison is commentary, not statute.)
- **Generative AI** is defined as "an AI system that generates text, sound, images, video, and various other outputs by imitating the structure and characteristics of input data" (the held translation's definition then cross-references the data statute for the meaning of "data").
- **High-impact AI** is defined as AI systems "that have the potential to significantly impact human life, safety, or fundamental rights", used in an enumerated set of areas: energy supply, drinking-water production, health-care service systems, medical and digital medical devices, nuclear materials and facilities, biometric analysis for criminal investigation or arrest, "Judgments or evaluations that have a significant impact on the rights and obligations of an individual, such as employment and loan assessments", transportation, national-institution decision-making affecting the public, and student assessment from early-childhood through secondary education. The list closes with a residual: "Other areas that have a significant impact on the protection of human life, physical safety, and basic human rights, as prescribed by Presidential Decree", so the high-impact set is open-ended and decree-extensible, a contrast with the EU AI Act's closed Annex III.
- **AI business operator** is defined as "any corporation, organization, individual, or government agency engaged in business related to the AI industry", split into an "AI Developer" ("An individual or entity that develops and provides AI") and an "AI-using Business Operator" ("An individual or entity that provides AI products or services using AI provided by" a developer). Most operative duties attach to "AI business operators" generally rather than to one role, a contrast with the EU AI Act's role-differentiated obligation chains.
- **Extraterritorial reach (Article 4(1)).** The held translation provides that the Act applies to "acts conducted abroad that affect the domestic market or users in the Republic of Korea", the scope gate for a non-Korean adopter. Article 4(2) excludes AI developed and used solely for national defense or national security purposes, as prescribed by Presidential Decree.
- **Affected-person explanation principle (Article 3(2)).** Among the Act's basic principles, affected persons are to be "provided with a clear and meaningful explanation of the key criteria and principles, used to derive the final AI outcomes, to the extent technically and reasonably possible." This is stated as a basic principle; the operator-level explanation duty is in Article 34.

## Governance architecture

The Act builds a substantial institutional layer (Chapter 2) that is neither enforcing authority nor adopter obligation:

- **National AI Committee (Article 7):** established under the President, who serves as its chairperson, with up to 45 members; its functions, enumerated in Article 8, include the regulation of high-impact AI. The held translation provides that the Committee subsists for five years from the date the Act takes effect.
- **AI Policy Center (Article 11):** MSIT-designated, for AI policy development and the establishment and dissemination of international norms.
- **AI Safety Research Institute (Article 12):** MSIT may operate it to secure AI safety, with tasks including risk definition and analysis, safety-evaluation-criteria research, and support for the Article 32 safety measures.
- **AI Basic Plan (Article 6):** a triennial plan established by MSIT and deliberated by the Committee.

## Core obligations

The Act mixes binding duties with effort-based ("strive to" / "make efforts") duties; a compliance reader must not over-read the soft ones, so the two are separated here.

**Binding duties (paraphrased from the held translation, with distinctive phrases quoted):**

1. **Advance notice that a product or service is AI-based (Article 31(1)).** AI business operators providing products or services using high-impact AI or generative AI are required to notify users in advance that the product or service is AI-based.
2. **Generative-output notice (Article 31(2)).** When providing generative-AI products or services, operators are required to notify users in advance that the products or services are generative-AI-generated.
3. **Synthetic-content labelling (Article 31(3)).** Operators are required to notify or indicate to users when virtual sounds, images, or videos are AI-generated and may be difficult to distinguish from authentic ones; where the output is part of an artistic or creative work, the indication may be made in a manner that does not hinder its exhibition or enjoyment. The methods of notification are delegated to Presidential Decree (Article 31(4)).
4. **Safety measures above a training-compute threshold (Article 32).** For AI systems in which "the cumulative computing amount used for learning meets or exceeds the standards prescribed by Presidential Decree", operators are required to implement "Identification, assessment, and mitigation of risks throughout the entire AI lifecycle" and the "Building of a risk management system to monitor and respond to AI-related safety incidents", and to submit the results to the Minister of Science and ICT. The compute threshold itself is not stated in the Act; it is decree-delegated, so no figure is asserted here (a structural contrast with the EU AI Act, which carries its systemic-risk compute presumption in the statutory text).
5. **Advance high-impact review (Article 33(1)).** Operators providing AI-based products or services are required to review in advance whether an AI system qualifies as high-impact AI, and may request confirmation from the Minister of Science and ICT; the Minister may issue criteria guidelines.
6. **High-impact operator measures (Article 34(1)).** Operators providing high-impact AI, or products and services based on it, are required to implement measures, "as prescribed by presidential decree", for the safety and reliability of the high-impact AI: a risk-management plan; a plan, to the extent technically feasible, to explain AI-generated outputs including the key criteria used and an overview of the training data; user-protection measures; "Human management and supervision of high-impact AI" (the human-oversight duty); the preparation and storage of documents demonstrating the safety-and-reliability measures taken; and other matters the Committee resolves for the safety and reliability of high-impact AI (so the statutory measure list is open, not closed). Measures implemented under other decree-prescribed laws are deemed equivalent (Article 34(3)).
7. **Domestic representative for foreign operators (Article 36).** Operators without an address or place of business in the Republic of Korea that meet user and revenue thresholds defined by Presidential Decree are required to appoint a domestic representative in writing and report it to the Minister of Science and ICT; the representative must have an address or place of business in Korea, and, where the representative violates the Act as to the matters in Article 36(1), the appointing operator is held responsible.

**Effort-based duties (stated as such):**

- **Verification and certification (Article 30(3)).** Operators are to "strive to obtain verification and certification prior to providing high-impact AI"; national institutions should prioritize verified or certified products when using high-impact AI (Article 30(4)).
- **Human-rights impact assessment (Article 35).** Operators providing products or services using high-impact AI are to "make efforts to assess in advance the impact on basic human rights"; national institutions must prioritize products or services that have undergone such an assessment. The public-procurement preferences in Articles 30(4) and 35(2) are the Act's lever for making these effort-based duties commercially real for public-sector suppliers.

## Promotion and support measures

By volume the Act is chiefly a promotion statute (Chapter 3): government support for AI research and safe-use technologies (including emergency-shutdown research), standardization, learning-data policies and an integrated data-provision system, priority consideration for small and medium enterprises (including support for their implementation of the Article 34 and Article 35 measures), startups, AI convergence with temporary permits and regulatory sandboxes under the ICT Convergence Special Act, overseas-talent recruitment, international cooperation, AI clusters, demonstration infrastructure, AI data centres, and the Korea AI Promotion Association. None of this binds an adopter, so it is noted here rather than detailed.

## AI ethics and voluntary governance

- **AI ethics principles (Article 27).** The government may establish and announce AI ethics principles, with MSIT gathering opinions and publicizing practical measures.
- **Private autonomous AI ethics committees (Article 28).** Educational and research institutions and AI business operators may establish a private autonomous AI ethics committee; the held translation constrains its composition, providing that the committee may not be "composed exclusively of one gender" and must include external members.
- **Trust-foundation and verification/certification support (Articles 29 to 30).** The Act authorizes government support for trust-building and for verification and certification of AI.

## Enforcement

The enforcement chain is asymmetric, and stating the asymmetry precisely is this annex's highest-value point:

- **Investigations and corrective orders (Article 40).** MSIT may require data submission or investigate where violations of Article 31(2) or (3), Article 32(1) or (2), or Article 34(1) are discovered or suspected, or on a report or complaint; it may exercise entry and inspection powers under the Framework Act on Administrative Investigation, and may order an operator to cease or rectify a violation.
- **Administrative fines (Article 43).** An administrative fine "not exceeding 30 million won" is imposed, and collected by MSIT, on a person who fails to give the Article 31(1) notice, fails to designate the Article 36(1) domestic representative, or fails to comply with a cease or corrective order under Article 40. (The held translation annotates the amount with a translator's US-dollar equivalent, which is not statutory text.)
- **The asymmetry.** Only three failures are directly finable: the Article 31(1) AI-based notice, the Article 36(1) domestic-representative appointment, and non-compliance with a corrective order. Violations of the generative and synthetic-content labelling (Article 31(2) to (3)), the compute-threshold safety duties (Article 32), and the high-impact measures (Article 34(1)) are enforced indirectly, through investigation and a corrective order, with a fine arising only for defying the order. Conversely, the directly finable Article 31(1) notice is not itself in the Article 40 investigation-trigger list.
- **Criminal penalty (Article 42).** A confidentiality breach by Committee members carries "imprisonment for not more than three years or by a fine not exceeding 30 million won"; this is a Committee-integrity provision, not an operator-facing one.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the statute or for legal advice; the controlling text is the Korean statute, and this annex works from the held CSET English translation, so any binding use requires verification against the official Korean text.
- **Decree-delegation.** Nearly every operative threshold lives in the Presidential Decree (the residual high-impact areas; the national-security exclusion scope; the Article 32 compute threshold; the Article 36 user and revenue thresholds; the Article 31 notification methods; the Article 34 measure details and equivalence-law list; and the fine procedure) or in MSIT guidelines. The Enforcement Decree is not held in the reference base; the adopter confirms current decree values upstream before committing to a compliance milestone, and no decree-level value (including any reported compute-threshold figure) is asserted here.
- **Translation sensitivity.** Several provisions (notably the Article 31(3) synthetic-content duty and the Article 36(1) domestic-representative provision) have elliptical renderings in the held translation; their precise scope turns on the Korean text.
- **Effort-based duties are stated as such;** this annex does not present the Article 35 impact assessment or the Article 30 verification and certification as mandatory.
- The corpus operational substance this annex references is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

The table is a mapping aid, not an assertion that the regimes impose the same obligations; every cell, including the statute anchors (which are translation-derived), is a mapping judgement.

| Requirement | South Korea AI Basic Act | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Advance notice that a product or service is AI-based (high-impact or generative AI) | Article 31(1) | Govern | Annex A.8 |
| Generative-output notice and synthetic-content labelling | Article 31(2), 31(3) | Govern, Map | Annex A.8 |
| Lifecycle risk identification, assessment, and mitigation, and an incident-monitoring risk-management system, above the decree-set training-compute threshold, with results submitted to MSIT | Article 32 | Map, Measure, Manage | Clause 6.1, Clause 8 |
| Advance review (and optional ministerial confirmation) of high-impact status | Article 33 | Map | Clause 6.1 |
| High-impact measures: risk-management plan, output explanation, user protection, human oversight, and demonstration documentation | Article 34(1) | Govern, Manage | Clause 8, Annex A.5, Annex A.8 |
| Human-rights impact assessment (effort-based; public-procurement preference) | Article 35 | Map, Measure | Annex A.5 |
| Domestic representative for extraterritorial operators above decree thresholds | Article 36 | Govern | Clause 5.3 |
| Verification and certification prior to providing high-impact AI (effort-based; public-procurement preference) | Article 30(3), 30(4) | Measure | Clause 9, Annex A.6 |
