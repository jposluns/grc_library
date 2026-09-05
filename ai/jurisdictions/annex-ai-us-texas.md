# Texas Responsible Artificial Intelligence Governance Act (TRAIGA) Regulatory Requirements

**Document Title:** Texas Responsible Artificial Intelligence Governance Act (TRAIGA) Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-09-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`ai/jurisdictions/annex-ai-us-california.md`](annex-ai-us-california.md), [`ai/jurisdictions/annex-ai-us-new-york-city.md`](annex-ai-us-new-york-city.md), [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to TRAIGA, Attorney-General enforcement activity, or the Chapter 553 sandbox and Chapter 554 council implementation\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-texas.md`](annex-ai-us-texas.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of Texas's comprehensive state AI statute, the Texas Responsible Artificial Intelligence Governance Act (TRAIGA), HB 149 of the 89th Legislature (2025), effective 1 January 2026. It sits alongside the other `ai/jurisdictions/` US-state annexes (Colorado, California, New York City). TRAIGA takes a different shape from Colorado's duty-of-care and risk-programme model: it is organized around a set of intent-based prohibited uses that bind any covered person, a narrower set of prohibitions and a disclosure duty specific to governmental entities, a regulatory sandbox, and an advisory council, and it preempts local AI regulation. This annex frames those provisions and cross-references the operational substance rather than restating it; the controlling text is HB 149 as codified.

## Applicable law and regulatory authority

- **The Texas Responsible Artificial Intelligence Governance Act (TRAIGA)**, HB 149, 89th Legislature (2025), which adds Subtitle D, "Artificial Intelligence Protection", to Title 11 of the Business and Commerce Code, comprising Chapter 551 (general provisions), Chapter 552 (artificial intelligence protection), Chapter 553 (the regulatory sandbox program), and Chapter 554 (the Texas Artificial Intelligence Council).
- **The Texas Attorney General** is the exclusive enforcer: the Attorney General has exclusive authority to enforce Chapter 552, except to the extent Section 552.106 provides for licensing-agency sanctions, and the chapter provides no private right of action (Sec. 552.101). The Texas Department of Information Resources (DIR) administers the Chapter 553 sandbox.
- **Local preemption (Sec. 552.003):** the chapter supersedes and preempts any ordinance, rule, or other regulation adopted by a political subdivision regarding the use of artificial intelligence systems.
- **Construction limits (Sec. 552.002):** the chapter is not to be construed to impose a requirement that adversely affects rights or freedoms including free speech, nor to authorize any body other than the Department of Insurance to regulate the business of insurance.

The controlling text is the enrolled bill as codified. Version-sensitive facts (the citation form, effective date, and any signing date) are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (the Texas TRAIGA row); this annex cross-references them rather than re-deriving them.

## Transition timeline

- **Effective date:** the Act takes effect 1 January 2026 (SECTION 10).
- **Attorney-General complaint mechanism:** not later than 1 September 2026, the Attorney General is to post the online complaint mechanism required by Section 552.102 (SECTION 8).
- **State-agency funding contingency (SECTION 9):** a state agency is not required to implement a mandatory duty the Act imposes on it unless money is specifically appropriated for that purpose, subject to a certification and cost-estimate duty to the Legislative Budget Board.
- The held enrolled text records House passage (23 April 2025), Senate passage with amendments (23 May 2025), and House concurrence (30 May 2025); a signing date is not present in the held text and is not asserted here.

## Scope: covered actors and covered systems

- **Artificial intelligence system (Sec. 551.001):** a machine-based system that, for any explicit or implicit objective, infers from the inputs it receives how to generate outputs (content, decisions, predictions, or recommendations) that can influence physical or virtual environments.
- **Consumer (Sec. 551.001):** an individual who is a Texas resident acting only in an individual or household context; the term excludes an individual acting in a commercial or employment context. TRAIGA's consumer-facing provisions therefore do not reach the employment or commercial context, a material contrast with Colorado; the prohibited-use provisions, however, bind a "person" or a "governmental entity" generally rather than only vis-a-vis consumers.
- **Applicability (Sec. 551.002):** the subtitle applies only to a person who promotes, advertises, or conducts business in Texas; produces a product or service used by Texas residents; or develops or deploys an artificial intelligence system in Texas.
- **Actor definitions (Sec. 552.001):** a "deployer" is a person who deploys an AI system for use in Texas; a "developer" is a person who develops an AI system offered, sold, leased, given, or otherwise provided in Texas; a "governmental entity" is an administrative unit of the state or a political subdivision, excluding hospital districts and institutions of higher education.

## Core obligations

**Disclosure to consumers (Sec. 552.051).** A governmental agency that makes available an AI system intended to interact with consumers is required to disclose to each consumer, before or at the time of interaction, that the consumer is interacting with an AI system; the duty applies regardless of whether the interaction would be obvious to a reasonable consumer. The disclosure must be clear and conspicuous, in plain language, and must not use a dark pattern (as defined by Section 541.001); a hyperlink to a separate page is permitted. For an AI system used in relation to a health care service or treatment, the provider is required to make the disclosure to the recipient (or the recipient's representative) no later than the date the service is first provided, or, in an emergency, as soon as reasonably possible. (The subsection (b) duty is drafted as a governmental-agency duty while subsection (c) refers to "a person"; the annex states the enacted scope precisely rather than generalizing the duty to all private deployers.)

**Prohibited uses that bind any person:**
- **Behavioural manipulation (Sec. 552.052):** a person may not develop or deploy an AI system in a manner that intentionally aims to incite or encourage a person to commit physical self-harm (including suicide), to harm another person, or to engage in criminal activity.
- **Constitutional infringement (Sec. 552.055):** a person may not develop or deploy an AI system with the sole intent that it infringe, restrict, or otherwise impair an individual's rights guaranteed under the United States Constitution; the section is remedial and is not to be construed to create or expand any right.
- **Unlawful discrimination (Sec. 552.056):** a person may not develop or deploy an AI system with the intent to unlawfully discriminate against a protected class in violation of state or federal law; a disparate impact is not by itself sufficient to demonstrate an intent to discriminate. Insurance entities subject to the applicable unfair-discrimination statutes, and federally insured financial institutions that comply with applicable banking law, are carved out.
- **Prohibited sexual-content uses (Sec. 552.057):** a person may not develop or distribute an AI system with the sole intent of producing or distributing unlawful visual material under the referenced Penal Code provisions, or one that engages in text-based conversations simulating sexual conduct while impersonating a child younger than 18.

**Prohibited uses that bind governmental entities only:**
- **Social scoring (Sec. 552.053):** a governmental entity may not use or deploy an AI system that evaluates or classifies natural persons based on social behaviour or personal characteristics with the intent to assign a social score, where the score results or may result in detrimental or disproportionate treatment in an unrelated context or the infringement of a constitutional or legal right.
- **Biometric identification (Sec. 552.054):** a governmental entity may not develop or deploy an AI system to uniquely identify a specific individual using biometric data, or the targeted or untargeted gathering of images or media from the internet or other publicly available sources, without consent, where doing so would infringe a right of the individual. The biometric-data definition excludes photographs and recordings and data derived from them, and HIPAA treatment, payment, and operations data.

**What TRAIGA does not impose.** Subtitle D contains no deployer risk-management-programme, impact-assessment, or algorithmic-discrimination duty-of-care of the Colorado type; the operative private-sector provisions are the intent-based prohibitions above. The nearest analogue to a documentation duty is the Attorney General's investigative-demand list (Sec. 552.103), which is responsive rather than standing.

## Consumer rights

- **Complaint mechanism (Sec. 552.102):** the Attorney General is to create and maintain an online mechanism through which a consumer may submit a complaint under the chapter.
- **Disclosure** of AI interaction per Section 552.051, above.
- **No private right of action (Sec. 552.101(b)).** Because enforcement is exclusively the Attorney General's and no private action lies, the consumer-rights surface is narrower than Colorado's or California's; this annex states that plainly rather than implying broader individual remedies.

## Enforcement

- **Exclusive Attorney-General enforcement; no private action (Sec. 552.101).**
- **Investigative authority (Sec. 552.103):** on a complaint, the Attorney General may issue a civil investigative demand and may request an enumerated set of materials, including a high-level description of the system's purpose, intended use, and deployment context; a description of the types of data used to train it; the categories of input data and the outputs produced; performance-evaluation metrics; known limitations; and post-deployment monitoring and user safeguards.
- **Notice and 60-day cure (Sec. 552.104):** the Attorney General must give written notice identifying the provisions alleged to be violated and may not bring an action before the 60th day after notice; no action lies if, within that period, the person cures and provides a written statement of the cure, supporting documentation, and the internal-policy changes needed to reasonably prevent further violation.
- **Civil penalties (Sec. 552.105):** curable violations or breach of a cure statement carry a penalty of not less than $10,000 and not more than $12,000 per violation; uncurable violations carry not less than $80,000 and not more than $200,000 per violation; continued violations carry not less than $2,000 and not more than $40,000 for each day the violation continues, alongside injunctive relief, attorney's fees, court costs, and investigative expenses. A rebuttable presumption of reasonable care applies, and a defendant is not liable where another person misuses the system or where the defendant discovers a violation through feedback or adversarial or red-team testing following applicable guidelines. A defendant that substantially complies with the most recent NIST "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile", or another nationally or internationally recognized AI risk-management framework, together with an internal review process, is afforded the statute's protection; the Attorney General may not collect a civil penalty for a system that has not been deployed.
- **State-agency sanctions (Sec. 552.106):** a licensing agency may sanction a licensee for a Subchapter B violation only after a Section 552.105 finding and an Attorney-General recommendation; sanctions include license suspension, probation, or revocation and a monetary penalty not to exceed $100,000.

## Regulatory sandbox and the Texas Artificial Intelligence Council

- **Regulatory sandbox (Chapter 553):** DIR, in consultation with the council, is to create a regulatory sandbox program that lets a participant test an innovative AI system with legal protection and limited market access without obtaining a license or other regulatory authorization (Sec. 553.051). During testing the Attorney General and state agencies may not pursue action for waived laws, but the requirements of Subchapter B of Chapter 552 (the prohibitions and the disclosure duty) may not be waived. An application requires a detailed system description, a benefit assessment addressing impacts on consumers, privacy, and public safety, a mitigation plan, and proof of compliance with applicable federal AI law (Sec. 553.052); participation runs for not more than 36 months, extendable for good cause (Sec. 553.053). Participants file quarterly reports, and DIR reports annually to the legislature.
- **Texas Artificial Intelligence Council (Chapter 554):** a seven-member advisory council, administratively attached to DIR, whose purposes include ethics and public-safety recommendations, identifying laws that impede AI innovation, evaluating regulatory capture, and sandbox oversight, and which provides training for state agencies and local governments. The council is advisory only: it may not adopt binding rules or guidance, interfere with or override a state agency, or exercise a power not granted by the chapter (Sec. 554.103). This is a material contrast with Colorado, where the Attorney General holds rulemaking authority.

## Relationship to the Texas privacy layer

TRAIGA also amends adjacent Texas privacy statutes; this annex cross-references the privacy layer rather than duplicating it, per the other US-state annexes:
- **SECTION 2** amends the Texas biometric-identifier statute (Business and Commerce Code Section 503.001): an individual has not consented to biometric capture based solely on the presence of media containing the individual's biometric identifiers on the internet or a publicly available source unless the individual made the media public; a new exemption covers biometrics used in developing, training, evaluating, or offering AI models or systems, unless a system is used to uniquely identify a specific individual; and a biometric identifier captured for AI training and then used for a non-exempt commercial purpose re-enters the statute's possession, destruction, and penalty provisions.
- **SECTION 3** amends the processor-duty provision of the Texas Data Privacy and Security Act (Business and Commerce Code Section 541.104): the processor assists the controller with the security of personal data processed by an AI system (as defined by Section 551.001) and with breach notification.
- A government-operations tail (SECTIONS 5 to 7) adds AI-use assessment to agency sunset review and to DIR's agency information-resources reviews and inventories.

The broader US privacy posture and these statutes' privacy mechanics are maintained in [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), which this annex cross-references rather than duplicates.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the enrolled bill or for legal advice; the controlling text is HB 149 as codified.
- **Version-sensitivity.** Implementing activity (the Attorney-General complaint mechanism, DIR sandbox rules, and council formation) post-dates the held enrolled text; an adopter reconfirms the current position upstream before committing to a compliance milestone. A signing date is not in the held text.
- **Intent-based prohibitions.** Several private-sector prohibitions turn on intent, and Section 552.056 expressly excludes disparate impact alone; the annex does not present TRAIGA as an algorithmic-discrimination-outcome statute.
- The corpus operational substance this annex references is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | Texas TRAIGA | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Consumer disclosure of AI interaction (government; health care) | Sec. 552.051 | Govern | Annex A.8 |
| Prohibited manipulation, intent-based discrimination, unlawful sexual-content uses | Secs. 552.052, 552.055, 552.056, 552.057 | Govern, Manage | Annex A.5 |
| Government social-scoring and biometric-identification prohibitions | Secs. 552.053, 552.054 | Govern, Map | Annex A.5 |
| Recognized-framework compliance as an enforcement protection (statutorily named NIST GenAI Profile) | Sec. 552.105 | Govern, Map, Measure, Manage | Clause 8 |
| Investigative documentation categories (purpose, training data, limitations, monitoring) | Sec. 552.103 | Map, Measure | Clause 7.5 |
| Sandbox pre-deployment testing with benefit assessment and mitigation plan | Chapter 553 | Measure, Manage | Annex A.6 |
