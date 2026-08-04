# European Union AI Regulatory Requirements

**Document Title:** European Union AI Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.8\
**Date:** 2026-08-04\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/procedure-ai-system-impact-assessment.md`](../procedure-ai-system-impact-assessment.md), [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../procedure-integrated-ai-and-privacy-assessment.md), [`privacy/jurisdictions/annex-privacy-european-union.md`](../../privacy/jurisdictions/annex-privacy-european-union.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI regulatory change\
**Repository Path:** [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of the European Union artificial-intelligence framework, Regulation (EU) 2024/1689 (the "AI Act"). The corpus already carries the operational substance of the AI Act scattered across the AI-governance documents: the risk-tier classification model, the deployer obligation chain, and the general-purpose AI (GPAI) obligations all live in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), and the fundamental-rights impact assessment sits in the unified router [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../procedure-integrated-ai-and-privacy-assessment.md). This annex consolidates that content by cross-reference rather than restating it, and adds the per-regime framing an adopter needs to see the whole jurisdiction at once: the operator roles, the applicability timeline, the penalty structure, and which obligations land on the adopter as provider, deployer, importer, or distributor.

It is the founding document of the `ai/jurisdictions/` subdirectory, mirroring the `privacy/jurisdictions/` model.

## Applicable law and regulatory authorities

- **Regulation (EU) 2024/1689** of the European Parliament and of the Council laying down harmonized rules on artificial intelligence (the AI Act), in force since the twentieth day following its publication in the Official Journal (OJ L, 12 July 2024), as amended by Regulation (EU) 2026/1744 (the Digital Omnibus on AI), published on 24 July 2026 and in force since 27 July 2026. This annex cites the in-force consolidated text; the Digital Omnibus amendments material to this annex (including the Article 4 AI-literacy duty, the new Article 5(1) points (ba) and (bb), Articles 4a and 60a, the Article 6(1a) to (1c) boundary, the restaged Article 113 timeline, and the Article 27, 75, 99, and 111 and Annex I machinery changes detailed below) are reflected here; this list is illustrative rather than exhaustive, and the Limitations section carries the fuller summary.
- **The AI Office** (within the European Commission) supervises general-purpose AI models and coordinates enforcement across Member States. Since Regulation (EU) 2026/1744 replaced Article 75(1), the AI Office is also exclusively competent to supervise and enforce this Regulation for certain AI systems: those based on a general-purpose AI model developed by the same provider as the system, or by providers forming part of the same undertaking (subject to the Article 75(1) exceptions), and those that constitute, or are integrated into, a very large online platform or search engine designated under Regulation (EU) 2022/2065; the new Articles 75a to 75d give the Office investigation, inspection, and fining powers over those systems. This exclusive competence binds the providers of those systems, and their deployers only where the deployer is also the provider or forms part of the same undertaking; other deployers remain under national supervision.
- **National market-surveillance authorities** designated by each Member State supervise the AI systems outside that exclusive competence placed on or used in their market.
- **Notified bodies** perform third-party conformity assessment for the high-risk AI systems that require it.
- **The European Artificial Intelligence Board** coordinates consistent application across Member States.

The controlling text is the Regulation itself; where this annex states an obligation, the article reference points to the enacted text, and time-varying detail (implementing-act deadlines, delegated-act thresholds) is handled per the timeline and limitations sections below rather than pinned to a fixed value the Regulation does not settle.

## Scope and extraterritorial reach

The AI Act applies, under Article 2, to providers placing AI systems or general-purpose AI models on the Union market or putting them into service in the Union regardless of where the provider is established, to deployers of AI systems established or located in the Union, and, materially for a non-EU adopter, to providers and deployers established outside the Union where the output produced by the AI system is used in the Union. An adopter without an EU establishment is therefore in scope whenever the output of its AI system is used in the Union; the corpus states this extraterritorial reach at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 7.

The AI Act's obligations attach only to systems that meet the Article 3(1) definition of an *AI system*, so that definition is the first scope gate an adopter applies. Article 3(1) turns on seven elements: a machine-based system; designed to operate with varying levels of autonomy; that may exhibit adaptiveness after deployment; that, for explicit or implicit objectives, infers from the input it receives how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments. The Commission's interpretive guidance on applying that test is the *Commission Guidelines on the definition of an artificial intelligence system*, C(2025) 5053 final (29 July 2025), non-binding soft law that assists the reading of Article 3(1); the binding provision remains the AI Act itself, and an authoritative interpretation can come only from the Court of Justice of the European Union.

## Operator roles

The AI Act assigns obligations by operator role (Article 3 definitions). An adopter first determines which role or roles it holds for a given AI system, because the obligation set follows the role:

- **Provider** (Article 3(3)): develops an AI system or a general-purpose AI model, or has one developed, and places it on the market or puts the AI system into service under its own name or trademark. An adopter that builds or fine-tunes a model and offers it under its own brand is a provider.
- **Deployer** (Article 3(4)): uses an AI system under its own authority, except in a personal non-professional activity. Most adopters using a procured AI system are deployers.
- **Authorized representative** (Article 3(5)): established in the Union under written mandate from a non-EU provider to carry out the provider's obligations.
- **Importer** (Article 3(6)): established in the Union, places on the market an AI system bearing the name or trademark of a third-country entity.
- **Distributor** (Article 3(7)): makes an AI system available on the Union market other than as provider or importer.

Article 3(8) collects these as "operator". A single adopter can hold more than one role across its AI estate, and the same modification (for example, substantially modifying a high-risk system, or putting a general-purpose model to a high-risk use under its own name) can move an adopter from deployer to provider.

## Risk-tier structure

The AI Act classifies AI systems into risk tiers, and the obligation set follows the tier. The corpus carries the classification table (prohibited, high-risk, general-purpose AI with systemic risk, general-purpose AI standard, and the residual limited-risk and minimal-risk cases) at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 4.1; this annex references it rather than restating it. The tier structure in the enacted text:

- **Prohibited practices** (Article 5): the unacceptable-risk set. Article 5(1) prohibits ten practices (as amended by Regulation (EU) 2026/1744, which inserted points (ba) and (bb)): (a) harmful subliminal, manipulative, or deceptive techniques; (b) exploitation of vulnerabilities due to age, disability, or a specific social or economic situation; (ba) an AI system that generates or manipulates realistic images, videos, audio, or similar material of an identifiable natural person's intimate parts, or of an identifiable natural person engaged in sexually explicit activities, without that person's freely-given, specific, informed, unambiguous, and explicit consent, subject to the Article 5(1a) intent-and-reasonable-foreseeability conditions and the Article 5(1b) limit on what counts as manipulation; (bb) the equivalent generation or manipulation of material or performance within the meaning of Article 2, points (c) and (e), of Directive 2011/93/EU (child sexual abuse material), subject to the same Article 5(1a) intent-and-reasonable-foreseeability conditions and except where a 'without right' defence applies under national law; (c) social scoring leading to unjustified or disproportionate detrimental treatment; (d) individual criminal-offence risk assessment based solely on profiling or personality traits; (e) untargeted scraping of facial images from the internet or CCTV footage to build facial-recognition databases; (f) emotion inference in the workplace or education institutions, except for medical or safety reasons; (g) biometric categorization to infer sensitive characteristics; and (h) real-time remote biometric identification in publicly accessible spaces for law enforcement, subject to the narrow Article 5(1)(h)(i) to (iii) exceptions and the Article 5(2) to (7) authorization conditions. The Commission's interpretive guidance is the *Commission Guidelines on prohibited artificial intelligence practices*, C(2025) 5052 final (29 July 2025), non-binding soft law that reads Article 5 rather than creating new binding law.
- **High-risk** (Article 6 and Annex III): under Article 6(1) an AI system is high-risk where both conditions are met: (a) it is intended to be used as a safety component of, or is itself, a product covered by the Union harmonization legislation listed in Annex I; and (b) that product is required to undergo third-party conformity assessment under that legislation. The Digital Omnibus added Article 6(1a) to (1c), which bounds this (an AI system used solely for a non-safety-related function is not a safety component; a system whose failure would endanger health or safety remains one; and a product assessed solely for risks other than to health and safety does not meet the Article 6(1)(b) condition). Separately, AI systems in the eight Annex III areas are high-risk: biometrics, critical infrastructure, education and vocational training, employment and workers' management, access to essential private and public services, law enforcement, migration/asylum/border control, and administration of justice and democratic processes.
- **General-purpose AI models** (Article 51): a GPAI model is classified as carrying systemic risk when it has high-impact capabilities; Article 51(2) sets a presumption of high-impact capability when the cumulative training compute exceeds 10^25 floating-point operations.
- **Limited-risk and minimal-risk**: the residual tiers, subject to the Article 50 transparency obligations (for example, disclosure of AI interaction, and marking of AI-generated or manipulated content) where applicable.

## High-risk obligation chain

For a high-risk AI system the obligations split between provider and deployer, and the corpus carries the deployer chain in operational form at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 5. The enacted references:

- **Provider obligations** (Article 16): the conformity-assessment, technical-documentation, quality-management, logging, and post-market-monitoring obligations; registration of the high-risk system in the EU database under Article 49; and the transparency obligations under Article 50.
- **Deployer obligations** (Article 26): use in accordance with the instructions, human oversight, input-data relevance, monitoring and logging, and, where the deployer is a public body or a private provider of public services, registration and the fundamental-rights impact assessment.
- **Fundamental-rights impact assessment (FRIA)** (Article 27): required, prior to deploying a high-risk AI system referred to in Article 6(2), of deployers that are bodies governed by public law or private entities providing public services, and of deployers of the high-risk systems in Annex III points 5(b) and (c); the Regulation excepts high-risk systems used in the area listed in Annex III point 2 (critical infrastructure). Where an obligation under Article 27 is already met through the data-protection impact assessment conducted under Article 35 GDPR or Article 27 of the Law Enforcement Directive (Directive (EU) 2016/680), Article 27(4) (as replaced by Regulation (EU) 2026/1744) allows the deployer to include, in the FRIA, cross-references to the relevant sections of, or relevant parts of, that assessment; and Article 27(5) tasks the AI Office with developing a questionnaire template, including an automated tool, to facilitate compliance. The corpus routes the two assessments together in [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../procedure-integrated-ai-and-privacy-assessment.md).

## General-purpose AI model obligations

Where the adopter provides, or builds substantially upon, a general-purpose AI model, the GPAI obligation set applies (the corpus carries the operational detail at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 6):

- **All GPAI providers** (Article 53): technical documentation for the model, information and documentation for downstream providers who integrate the model, a policy to comply with Union copyright law, and a sufficiently detailed summary of the training content.
- **GPAI models with systemic risk** (Article 55): in addition, model evaluation including adversarial testing, systemic-risk assessment and mitigation, serious-incident tracking and reporting to the AI Office, and an adequate level of cybersecurity.

A deployer that integrates a GPAI model into its own high-risk system remains subject to the deployer obligations above for that system; the GPAI provider obligations attach to whoever places the model on the market.

## Applicability timeline

Article 113 sets a phased application. The Regulation applies in general from 2 August 2026, with these staged exceptions:

- **Chapters I and II** (the general provisions and the prohibited-practices set of Article 5) apply from 2 February 2025, except that the prohibitions inserted by Regulation (EU) 2026/1744 at Article 5(1) points (ba) and (bb), together with Article 5(1a) and (1b), apply from 2 December 2026 (amended Article 113, third paragraph, point (a)).
- **Chapter V** (general-purpose AI models), together with Chapter III Section 4, Chapter VII, Chapter XII, and Article 78, applies from 2 August 2025, with the exception of Article 101 (fines for GPAI-model providers).
- **High-risk systems** (Chapter III, Sections 1 to 3, except Article 6(5)) apply on the timeline restaged by Regulation (EU) 2026/1744 (amended Article 113, third paragraph, point (c)): from **2 December 2027** for systems classified as high-risk under Article 6(2) and Annex III, and from **2 August 2028** for systems classified as high-risk under Article 6(1) and Annex I. Before that amendment, the Article 6(1) obligations applied from 2 August 2027. Articles 102 to 110 apply from 27 July 2026 (point (d)). For AI systems in machinery (Regulation (EU) 2023/1230, which the Digital Omnibus moved from Annex I Section A to Section B), the regime is narrower: under the amended Article 2(2), only Article 6(1), Article 60a, and Articles 102 to 112 apply (Articles 57, 58, and 59 apply only in so far as the high-risk requirements have been integrated into that harmonization legislation).

Some obligations the Regulation ties to delegated or implementing acts, or to Commission guidance, carry enacted dates (for example, the Article 2(13) delegated acts by 2 August 2027); the detail of harmonized standards and other time-varying instruments is tracked against those instruments as adopted. An adopter confirms each deadline against the current act, standard, or guidance rather than a date asserted here. Two dated legacy duties also apply under Article 111 (as amended): providers and deployers of high-risk AI systems intended to be used by public authorities take the steps to comply by **2 August 2030** (Article 111(2)); and providers of AI systems generating synthetic audio, image, video, or text content that were placed on the market before 2 August 2026 comply with the Article 50(2) marking obligation by **2 December 2026** (Article 111(4)).

## Penalties

Article 99 sets the administrative-fine ceilings as a maximum; Member States set the enforceable amounts within that framework for the AI systems under national supervision, while the AI Office imposes the fines for the systems within its exclusive competence (Articles 75a to 75d). The enacted maxima are:

- **Prohibited practices** (Article 99(3)): up to EUR 35 000 000, or, for an undertaking, up to 7% of total worldwide annual turnover for the preceding financial year, whichever is higher.
- **Other operator or notified-body obligations** (Article 99(4), covering provider obligations under Article 16, deployer obligations under Article 26, and the transparency obligations under Article 50, among others): up to EUR 15 000 000, or up to 3% of total worldwide annual turnover, whichever is higher.
- **Supply of incorrect, incomplete, or misleading information** to notified bodies or national competent authorities (Article 99(5)): up to EUR 7 500 000, or up to 1% of total worldwide annual turnover, whichever is higher.
- **GPAI-model providers** (Article 101): the Commission may impose fines of up to 3% of worldwide annual turnover or EUR 15 000 000, whichever is higher.
- **AI Office fines** (Articles 75a to 75d, inserted by Regulation (EU) 2026/1744): for the AI systems within its exclusive competence under Article 75(1), the AI Office may impose fines and periodic penalty payments, with Article 99(3) to (7) applying to the Office mutatis mutandis.
- **SME and start-up cap** (Article 99(6)): for small and medium-sized enterprises, including start-ups, each fine is capped at the lower of the percentage or the fixed amount, rather than the higher.
- **Small mid-cap (SMC) cap** (Article 99(6a), inserted by Regulation (EU) 2026/1744): for small mid-cap enterprises (defined at Article 3, point (14b)), each Article 99(4) or (5) fine is likewise capped at the lower of the percentage or the fixed amount. The same amendment added, at Article 99(4) point (da), the Article 25(2) and (4) obligations as a fineable category.

## Adopter-role framing

Which obligations land on the adopter depends on the role it holds for each system:

- **As deployer** (the most common adopter posture): classify each system before deployment, ensure that human oversight and logging are in place for high-risk systems, complete the FRIA where the adopter is a public body or public-service provider, register high-risk systems where required, and meet the Article 50 transparency obligations for limited-risk uses.
- **As provider** (an adopter that builds, brands, or substantially modifies a system): the full Article 16 provider chain, including conformity assessment, technical documentation, and EU-database registration for high-risk systems, plus the GPAI provider obligations where a general-purpose model is placed on the market.
- **As importer or distributor**: verify that the provider has met its obligations (conformity marking, documentation, registration) before making the system available, and cooperate with market-surveillance authorities.

An adopter maps its AI estate to these roles as the first step; the AI System Impact Assessment ([`ai/procedure-ai-system-impact-assessment.md`](../procedure-ai-system-impact-assessment.md)) and the classification process in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 4.2 carry the operational workflow.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the enacted Regulation or for legal advice; the controlling text is Regulation (EU) 2024/1689 and its implementing and delegated acts.
- **Digital Omnibus on AI (enacted).** Regulation (EU) 2026/1744 (the Digital Omnibus on AI) of 8 July 2026, published in the Official Journal on 24 July 2026 and in force since 27 July 2026, amended Regulation (EU) 2024/1689 (and Regulations (EU) 2018/1139 and (EU) 2023/1230) to simplify implementation. Its changes reflected in this annex: the Article 4 AI-literacy duty was softened to a take-measures-to-support obligation; two prohibitions were inserted at Article 5(1) points (ba) and (bb) (non-consensual intimate imagery and child sexual abuse material), with the Article 5(1a) and (1b) conditions and a 2 December 2026 application date; Articles 4a (processing special categories of personal data for bias detection and correction) and 60a (real-world testing of certain Annex I Section B high-risk systems) were inserted; Article 6 gained paragraphs 1a to 1c (AI used solely for non-safety-related aspects is not a safety component; systems whose failure would endanger health or safety remain safety components; and a product assessed solely for non-health-and-safety risks does not meet the Article 6(1)(b) third-party-conformity-assessment condition); and the Article 113 application timeline was restaged (high-risk obligations delayed to 2 December 2027 for Article 6(2) and Annex III systems, and 2 August 2028 for Article 6(1) and Annex I systems); Article 27(4) and (5) were replaced (the deployer may cross-reference the DPIA in the FRIA; the AI Office develops a questionnaire template); Article 75(1) was replaced to give the AI Office exclusive competence over certain AI systems, with new Articles 75a to 75d enforcement powers; Article 99 gained a small-mid-cap fine cap (Article 99(6a)) and a new fineable category (Article 99(4), point (da)); Article 111 added two dated legacy duties (public-authority high-risk systems by 2 August 2030; legacy synthetic-content Article 50(2) marking by 2 December 2026); and Regulation (EU) 2023/1230 (machinery) was moved from Annex I Section A to Section B, narrowing its regime to the amended Article 2(2); and Article 50(7) was replaced so that the Commission (not the AI Office) encourages and facilitates codes of practice on detecting, marking, and labelling synthetic content and assesses their adequacy under the amended Article 56(6) procedure (Article 56(6) was replaced accordingly). The enacted amending Regulation is held in the reference base (EUR-Lex CELEX:32026R1744); the superseded proposal COM(2025) 836 is legislative history only. As always, confirm the current consolidated text at EUR-Lex.
- Values that the Regulation delegates to implementing acts, delegated acts, or harmonized standards (the detail of technical-documentation templates and any amendment to the Article 51 compute threshold under Article 51(3)) are time-varying and are not pinned to a fixed value here; the adopter confirms the current position against the acts as adopted.
- The corpus operational detail this annex references (the classification table, the deployer obligation chain, the GPAI obligations) is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md); on any divergence, that document governs the operational procedure and this annex governs the per-regime framing.
- Member-State-specific transpositions and national market-surveillance designations are not enumerated here; the adopter confirms the competent authority for each Member State in which it operates.

## Framework alignment

| Requirement | EU AI Act | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Risk-based classification before deployment | Article 6, Annex III | Map | Clause 6.1 |
| Provider conformity and documentation | Article 16, Article 49 | Govern, Measure | Clause 8 |
| Deployer oversight and impact assessment | Article 26, Article 27 | Manage | Clause 8.3 |
| General-purpose model transparency | Article 53, Article 55 | Measure | Clause 8 |
| Transparency to affected persons | Article 50 | Govern | Annex A.8 |
