# European Union AI Regulatory Requirements

**Document Title:** European Union AI Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.3\
**Date:** 2026-07-12\
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

- **Regulation (EU) 2024/1689** of the European Parliament and of the Council laying down harmonized rules on artificial intelligence (the AI Act), in force since the twentieth day following its publication in the Official Journal (OJ L, 12 July 2024). This annex cites the in-force text; a pending amendment (the Digital Omnibus on AI) is flagged in the Limitations section and is not yet law.
- **The AI Office** (within the European Commission) supervises general-purpose AI models and coordinates enforcement across Member States.
- **National market-surveillance authorities** designated by each Member State supervise AI systems placed on or used in their market.
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

- **Prohibited practices** (Article 5): the unacceptable-risk set. Article 5(1) prohibits eight practices: (a) harmful subliminal, manipulative, or deceptive techniques; (b) exploitation of vulnerabilities due to age, disability, or a specific social or economic situation; (c) social scoring leading to unjustified or disproportionate detrimental treatment; (d) individual criminal-offence risk assessment based solely on profiling or personality traits; (e) untargeted scraping of facial images from the internet or CCTV footage to build facial-recognition databases; (f) emotion inference in the workplace or education institutions, except for medical or safety reasons; (g) biometric categorization to infer sensitive characteristics; and (h) real-time remote biometric identification in publicly accessible spaces for law enforcement, subject to the narrow Article 5(1)(h)(i) to (iii) exceptions and the Article 5(2) to (7) authorization conditions. The Commission's interpretive guidance is the *Commission Guidelines on prohibited artificial intelligence practices*, C(2025) 5052 final (29 July 2025), non-binding soft law that reads Article 5 rather than creating new binding law.
- **High-risk** (Article 6 and Annex III): AI systems used as safety components of regulated products (Article 6(1)), and AI systems in the eight Annex III areas: biometrics, critical infrastructure, education and vocational training, employment and workers' management, access to essential private and public services, law enforcement, migration/asylum/border control, and administration of justice and democratic processes.
- **General-purpose AI models** (Article 51): a GPAI model is classified as carrying systemic risk when it has high-impact capabilities; Article 51(2) sets a presumption of high-impact capability when the cumulative training compute exceeds 10^25 floating-point operations.
- **Limited-risk and minimal-risk**: the residual tiers, subject to the Article 50 transparency obligations (for example, disclosure of AI interaction, and marking of AI-generated or manipulated content) where applicable.

## High-risk obligation chain

For a high-risk AI system the obligations split between provider and deployer, and the corpus carries the deployer chain in operational form at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 5. The enacted references:

- **Provider obligations** (Article 16): the conformity-assessment, technical-documentation, quality-management, logging, and post-market-monitoring obligations; registration of the high-risk system in the EU database under Article 49; and the transparency obligations under Article 50.
- **Deployer obligations** (Article 26): use in accordance with the instructions, human oversight, input-data relevance, monitoring and logging, and, where the deployer is a public body or a private provider of public services, registration and the fundamental-rights impact assessment.
- **Fundamental-rights impact assessment (FRIA)** (Article 27): required, prior to deploying a high-risk AI system referred to in Article 6(2), of deployers that are bodies governed by public law or private entities providing public services, and of deployers of the high-risk systems in Annex III points 5(b) and (c); the Regulation excepts high-risk systems used in the area listed in Annex III point 2 (critical infrastructure). The FRIA complements, and does not replace, the Article 35 GDPR data-protection impact assessment; the corpus routes the two together in [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../procedure-integrated-ai-and-privacy-assessment.md).

## General-purpose AI model obligations

Where the adopter provides, or builds substantially upon, a general-purpose AI model, the GPAI obligation set applies (the corpus carries the operational detail at [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 6):

- **All GPAI providers** (Article 53): technical documentation for the model, information and documentation for downstream providers who integrate the model, a policy to comply with Union copyright law, and a sufficiently detailed summary of the training content.
- **GPAI models with systemic risk** (Article 55): in addition, model evaluation including adversarial testing, systemic-risk assessment and mitigation, serious-incident tracking and reporting to the AI Office, and an adequate level of cybersecurity.

A deployer that integrates a GPAI model into its own high-risk system remains subject to the deployer obligations above for that system; the GPAI provider obligations attach to whoever places the model on the market.

## Applicability timeline

Article 113 sets a phased application. The Regulation applies in general from 2 August 2026, with these staged exceptions:

- **Chapters I and II** (the general provisions and the prohibited-practices set of Article 5) apply from 2 February 2025.
- **Chapter V** (general-purpose AI models), together with Chapter III Section 4, Chapter VII, Chapter XII, and Article 78, applies from 2 August 2025, with the exception of Article 101 (fines for GPAI-model providers).
- **Article 6(1)** (the safety-component high-risk classification) and its corresponding obligations apply from 2 August 2027.

Deadlines that the Regulation delegates to implementing or delegated acts (for example, harmonized standards and the codes of practice) are not fixed calendar dates in the enacted text; an adopter tracks them against the acts as adopted rather than against a date asserted here.

## Penalties

Article 99 sets the administrative-fine ceilings as a maximum, with Member States setting the enforceable amounts within the framework; the enacted maxima are:

- **Prohibited practices** (Article 99(3)): up to EUR 35 000 000, or, for an undertaking, up to 7% of total worldwide annual turnover for the preceding financial year, whichever is higher.
- **Other operator or notified-body obligations** (Article 99(4), covering provider obligations under Article 16, deployer obligations under Article 26, and the transparency obligations under Article 50, among others): up to EUR 15 000 000, or up to 3% of total worldwide annual turnover, whichever is higher.
- **Supply of incorrect, incomplete, or misleading information** to notified bodies or national competent authorities (Article 99(5)): up to EUR 7 500 000, or up to 1% of total worldwide annual turnover, whichever is higher.
- **GPAI-model providers** (Article 101): the Commission may impose fines of up to 3% of worldwide annual turnover or EUR 15 000 000, whichever is higher.
- **SME and start-up cap** (Article 99(6)): for small and medium-sized enterprises, including start-ups, each fine is capped at the lower of the percentage or the fixed amount, rather than the higher.

## Adopter-role framing

Which obligations land on the adopter depends on the role it holds for each system:

- **As deployer** (the most common adopter posture): classify each system before deployment, ensure that human oversight and logging are in place for high-risk systems, complete the FRIA where the adopter is a public body or public-service provider, register high-risk systems where required, and meet the Article 50 transparency obligations for limited-risk uses.
- **As provider** (an adopter that builds, brands, or substantially modifies a system): the full Article 16 provider chain, including conformity assessment, technical documentation, and EU-database registration for high-risk systems, plus the GPAI provider obligations where a general-purpose model is placed on the market.
- **As importer or distributor**: verify that the provider has met its obligations (conformity marking, documentation, registration) before making the system available, and cooperate with market-surveillance authorities.

An adopter maps its AI estate to these roles as the first step; the AI System Impact Assessment ([`ai/procedure-ai-system-impact-assessment.md`](../procedure-ai-system-impact-assessment.md)) and the classification process in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) section 4.2 carry the operational workflow.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the enacted Regulation or for legal advice; the controlling text is Regulation (EU) 2024/1689 and its implementing and delegated acts.
- **Pending amendment (the Digital Omnibus on AI).** A proposal to amend the AI Act, the Digital Omnibus on AI (Commission proposal COM(2025) 836 final, 2025/0359 (COD), 19 November 2025; provisionally agreed at Council on 13 May 2026 per Council document 9247/26), is in the legislative pipeline but is NOT yet adopted and is NOT in force. Once adopted it would amend Regulation (EU) 2024/1689 (and Regulation (EU) 2018/1139) to simplify implementation, inserting Articles 4a, 60a, and 75a to 75e and a new Annex XIV. This annex deliberately cites only the in-force text; an adopter tracks the Omnibus and re-assesses the affected obligations when it is adopted and published, rather than relying on the proposal.
- Values that the Regulation delegates to implementing acts, delegated acts, or harmonized standards (deadlines for codes of practice, the detail of technical-documentation templates, and any amendment to the Article 51 compute threshold under Article 51(3)) are time-varying and are not pinned to a fixed value here; the adopter confirms the current position against the acts as adopted.
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
