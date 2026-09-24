# United States Federal AI Policy (OMB M-25-21, M-25-22, and M-26-04) Regulatory Requirements

**Document Title:** United States Federal AI Policy (OMB M-25-21, M-25-22, and M-26-04) Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-09-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-texas.md`](annex-ai-us-texas.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`ai/jurisdictions/annex-ai-us-california.md`](annex-ai-us-california.md), [`ai/jurisdictions/annex-ai-us-illinois.md`](annex-ai-us-illinois.md), [`ai/jurisdictions/annex-ai-us-new-york-city.md`](annex-ai-us-new-york-city.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to, rescission of, or replacement of OMB M-25-21, M-25-22, or M-26-04, or the executive orders they implement\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-federal.md`](annex-ai-us-federal.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of United States federal executive-branch AI policy: three Office of Management and Budget (OMB) memoranda, M-25-21 on federal agency use of AI, M-25-22 on federal acquisition of AI, and M-26-04 on the Unbiased AI Principles for agency-procured large language models (LLMs), set against the national strategy in America's AI Action Plan (July 2025). It sits alongside the `ai/jurisdictions/` US-state annexes (California, Colorado, Illinois, New York City, and Texas).

The instruments differ in kind from those state statutes. They are executive-branch policy directed to federal agencies, not legislation that binds the public: M-25-21 states that it "governs only agencies' own use of AI and does not create rights or obligations for the public". They reach a private organization in two ways: an organization that is itself a covered federal agency applies them directly, and an organization that sells AI systems or services to a federal agency meets them as contract terms, because M-25-22 and M-26-04 direct agencies to write their requirements into solicitations and contracts. This annex frames the instruments for both readers and cross-references the operational substance rather than restating it; the controlling texts are the memoranda themselves.

## Applicable instruments and issuing authority

- **OMB Memorandum M-25-21**, "Accelerating Federal Use of AI through Innovation, Governance, and Public Trust" (3 April 2025). It is issued under Executive Order 14179, "Removing Barriers to American Leadership in Artificial Intelligence" (23 January 2025), and consistent with the AI in Government Act of 2020, which required its issuance. It rescinds and replaces OMB M-24-10.
- **OMB Memorandum M-25-22**, "Driving Efficient Acquisition of Artificial Intelligence in Government" (3 April 2025). It rescinds and replaces OMB M-24-18.
- **OMB Memorandum M-26-04**, "Increasing Public Trust in Artificial Intelligence Through Unbiased AI Principles" (11 December 2025), issued to implement Executive Order 14319, "Preventing Woke AI in the Federal Government" (23 July 2025), which directed OMB to issue guidance applying the order's two Unbiased AI Principles.
- **America's AI Action Plan** (the White House, July 2025), organized around three pillars: innovation, infrastructure, and international diplomacy and security. Its operative content is framed as recommended policy actions; this annex treats it as strategy context, not as a source of obligations.
- **OMB** issues the memoranda and receives the agency reporting they require; each agency's Chief AI Officer (CAIO) carries the agency-level responsibilities M-25-21 assigns.

Version-sensitive facts (issuance dates, the M-26-04 sunset, and the last upstream verification) are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (the US OMB rows); this annex cross-references them rather than re-deriving them. Two defects in the published source documents affect citation. M-26-04's first footnote names the implemented order as "Executive Order 14139" while its body and the order's own title and date identify Executive Order 14319; this annex cites 14319. M-25-22's Section 3 items are printed with the letters b through h while the memorandum's own cross-references use a sequence shifted back by one letter (for example, "Section 3(c)" for privacy, which is printed as item d); this annex therefore cites M-25-22's Section 3 items by heading, not by letter.

## Transition timeline

Deadlines run from each memorandum's issuance date; the dates below are computed from the stated day counts.

- **M-25-21 (issued 3 April 2025):** each agency retains or designates a Chief AI Officer within 60 days; each Chief Financial Officers Act (CFO Act) agency convenes an AI governance board within 90 days and develops an AI Strategy within 180 days; each agency submits to OMB and posts publicly a compliance plan within 180 days and every two years thereafter until 2036; agencies update internal AI policies, and should develop a generative-AI acceptable-use policy, within 270 days; and agencies document implementation of the minimum risk management practices for high-impact AI within 365 days (3 April 2026).
- **M-25-22 (issued 3 April 2025):** applies to any contract awarded under a solicitation issued on or after the date 180 days after issuance, and to any option to renew or extend an existing contract exercised after that date; agencies update their internal acquisition procedures within 270 days.
- **M-26-04 (issued 11 December 2025):** agencies update procurement policies and procedures no later than 11 March 2026; the memorandum ceases to have force or effect two years after issuance (11 December 2027) unless the Director of OMB provides otherwise.

## Scope: covered actors and covered systems

- **M-25-21, covered agencies:** except as specifically noted, all agencies defined in 44 U.S.C. 3502(1), including independent regulatory agencies. Some requirements apply only to CFO Act agencies, and some do not apply to elements of the Intelligence Community.
- **M-25-21, covered AI:** new and existing AI that is developed, used, or acquired by or on behalf of covered agencies, subject to the memorandum's stated exclusions.
- **M-25-22:** AI systems or services acquired by or on behalf of covered agencies. It does not apply to AI acquired for use as a component of a National Security System, nor to AI used incidentally by a contractor during performance (AI the contractor uses at its option when not directed or required to fulfill contract requirements).
- **M-26-04:** any LLM procured by an agency (an executive department, military department, independent establishment, or wholly owned government corporation, as defined in the memorandum), regardless of how the LLM will be deployed, modified, or used. It does not apply to national security systems, though application to them is encouraged where practicable, and agencies consider whether to apply it to agency-developed LLMs and to AI models other than LLMs.

## Core obligations: agencies using high-impact AI (M-25-21)

**High-impact AI.** AI is high-impact when its output serves as a principal basis for decisions or actions that have a legal, material, binding, or significant effect on rights or safety, whether or not a human oversees the decision or action. M-25-21 lists categories of use presumed to be high-impact; an agency official who determines that a use in a presumed category is not high-impact documents that determination in writing to the CAIO.

**Minimum risk management practices.** For each high-impact use, the agency must:
1. **Conduct pre-deployment testing** and prepare risk mitigation plans reflecting expected real-world outcomes. Where the agency lacks access to the underlying source code, models, or data, it uses alternative methods, such as querying the AI service and observing the outputs, or providing evaluation data to the vendor and obtaining the results.
2. **Complete an AI impact assessment** before deployment, updated through the lifecycle, covering at minimum: intended purpose and expected benefit; the quality and appropriateness of the data and model capability; potential impacts on privacy, civil rights, and civil liberties, with planned mitigations; reassessment scheduling and procedures; related costs; the results of an independent review by an agency reviewer not involved in development; and risk acceptance, supported by the signature of the individual accepting the risk.
3. **Conduct ongoing monitoring** for performance and adverse impacts, designed to detect unforeseen circumstances, post-deployment changes to the system, and changes to the context of use or its data.
4. **Train and assess operators** sufficiently and periodically, so that those who interpret and act on the AI's output can manage its risks.
5. **Provide human oversight, intervention, and accountability** suitable for high-impact use, including an appropriate fail-safe where practicable.
6. **Offer consistent remedies or appeals:** individuals affected by AI-enabled decisions have access to timely human review and a chance to appeal negative impacts, where appropriate.
7. **Consult and incorporate feedback** from end users and the public on the use case, where appropriate.

**Non-compliance, pilots, and waivers.** A high-impact use that does not meet the minimum practices must be safely discontinued. A pilot is exempt from the minimum practices if it is of limited scale and duration, the CAIO has certified it (with the certification tracked centrally), individuals can opt in and out where possible, and the practices are applied where practicable. The CAIO may waive a practice for a specific application on a written, system-specific, and context-specific risk determination; this responsibility may not be delegated, each waiver is recertified annually, a waiver grant or revocation is reported to OMB within 30 days, and a summary of each determination and waiver is released publicly to the extent consistent with law.

**Agency governance.** Beyond high-impact AI, M-25-21 requires the Chief AI Officer, the CFO Act agency AI governance board and AI Strategy, the published compliance plans, and an AI use-case inventory submitted to OMB and posted publicly at least annually (the Department of Defense and the Intelligence Community excepted).

## Core obligations reaching AI vendors through contracts

**M-25-22 (acquisition).** For contracts within its scope, M-25-22 directs agencies to write the following into solicitations and contracts, making them contractual obligations on the vendor:
- **Government data:** contracts permanently prohibit the use of non-public inputted agency data and outputted results to further train publicly or commercially available AI algorithms, consistent with applicable law, absent explicit agency consent (under the Section 3 item headed "Protect IP Rights and Use of Government Data").
- **High-impact compliance:** contracts must require compliance with the M-25-21 minimum risk management practices for high-impact use cases, and for systems with potential or expected high-impact uses the agency informs vendors of the transparency and documentation it will require, such as the descriptive information needed to complete the AI impact assessment.
- **Testing and monitoring:** contractual terms give the agency the ability to monitor and evaluate the system's performance, risks, and effectiveness regularly; vendors must provide the access and time agencies need to complete independent evaluation (or, where the agency allows vendor-run testing, produce results detailed enough to be independently verified or reproduced if practicable); and contracts must detail the vendor's examination, testing, and validation procedures and must not prohibit the agency from internally disclosing how the vendor conducts testing or its results.
- **Vendor lock-in protections:** terms such as knowledge transfer, data and model portability, agency rights to code and models produced in performance of the contract, and transparency in licensing and pricing.
- **Recommended, not required:** agencies are encouraged to require vendor performance monitoring, performance standards before a new version is deployed, and roll-back when a new version fails them; and should consider requiring notice before new AI features are integrated into a delivered system. Agencies also determine whether a solicitation should require the vendor to disclose its own use of AI in performing the contract (under the Section 3 item headed "Determine Necessary Disclosures of AI Use in the Fulfillment of a Government Contract").

**M-26-04 (Unbiased AI Principles).** The two principles are truth-seeking (LLMs are truthful in responding to requests for factual information or analysis, prioritize historical accuracy, scientific inquiry, and objectivity, and acknowledge uncertainty where reliable information is incomplete or contradictory) and ideological neutrality (LLMs are neutral, nonpartisan tools that do not manipulate responses in favour of ideological dogmas, and developers do not intentionally encode partisan or ideological judgments into outputs unless those judgments are prompted by or readily accessible to the end user). Agencies must:
- include contractual requirements addressing compliance with the principles in any LLM solicitation or order issued after the memorandum's date;
- modify existing LLM contracts to include those requirements to the extent practicable, at the latest before exercising any option that extends performance;
- request, at minimum, the vendor's acceptable use policy, model, system, or data cards, end-user resources, and a mechanism for end-user feedback on outputs that violate the principles; and may request enhanced transparency (for example, pre-training and post-training activities affecting factuality, and system-level prompts) where the planned use warrants it; and
- maintain a process through which agency users report outputs that violate the principles.

## Public rights

M-25-21 creates no rights enforceable by the public. The remedies-and-appeals and public-feedback practices are agency duties owed within the agency's own processes, and the public's visibility comes through the published compliance plans, use-case inventories, and waiver summaries. This annex states that plainly rather than implying individual remedies of the kind the state statutes provide.

## Oversight and enforcement

- **OMB oversight through reporting:** compliance plans submitted to OMB and posted publicly, the annual use-case inventory, waiver reporting within 30 days, and documentation of the minimum practices on OMB's request or in its periodic accountability reviews.
- **Termination:** a high-impact use that cannot meet the minimum practices is discontinued, not retained under a documented exception (the pilot and waiver routes above are the only sanctioned alternatives).
- **No civil penalties.** The memoranda carry no statutory penalty regime. For a vendor, the consequence of non-compliance runs through the contract, under the terms the agency has written into it.

## National strategy context

America's AI Action Plan sets the national direction the memoranda operate within. Among its recommended policy actions are that OMB work with agencies that have AI-related discretionary funding to consider a state's AI regulatory climate when making funding decisions, relevant to how an adopter reads the state annexes; that NIST revise the AI Risk Management Framework; and that federal procurement guidelines be updated so that the government contracts only with frontier LLM developers whose systems are objective and free from top-down ideological bias, the direction M-26-04 implements for agency LLM procurement. These are recommendations, not obligations.

## Relationship to the state annexes

The federal instruments do not preempt the state AI statutes covered in the other `ai/jurisdictions/` US annexes: an organization that is both a federal vendor and subject to a state statute meets both. The Texas annex records that TRAIGA's internal-review no-liability route is conditioned on substantial compliance with the NIST AI RMF Generative AI Profile or another recognized framework (see [`ai/jurisdictions/annex-ai-us-texas.md`](annex-ai-us-texas.md)); an adopter using the NIST AI RMF for both purposes records how the federal minimum practices map onto it.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the memoranda or for legal advice; the controlling texts are the memoranda as issued.
- **Version sensitivity.** Executive-branch memoranda can be rescinded or replaced without legislation, as M-25-21 and M-25-22 themselves rescinded M-24-10 and M-24-18. M-26-04 sunsets on 11 December 2027 unless extended. An adopter reconfirms the current position upstream before committing to a compliance milestone.
- **Source-document defects.** The M-26-04 footnote and M-25-22 Section 3 lettering defects described above are in the published documents; this annex cites around them rather than reproducing them.
- The corpus operational substance this annex references is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | US federal instrument | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Chief AI Officer, governance board, strategy, and compliance plans | M-25-21 | Govern | Clause 5 |
| High-impact determination and AI impact assessment with independent review and signed risk acceptance | M-25-21 | Map, Measure | Annex A.5 |
| Pre-deployment testing and ongoing monitoring | M-25-21 | Measure, Manage | Annex A.6 |
| Human oversight, operator training, remedies, and public feedback | M-25-21 | Govern, Manage | Annex A.9 |
| Contractual data-use, testing-access, lock-in, and high-impact compliance terms for AI vendors | M-25-22 | Govern, Manage | Annex A.10 |
| LLM transparency artefacts (acceptable use policy, model, system, or data cards) and feedback mechanism | M-26-04 | Map, Govern | Annex A.8 |
