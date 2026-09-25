# United States Federal AI Policy (OMB M-25-21, M-25-22, and M-26-04) Regulatory Requirements

**Document Title:** United States Federal AI Policy (OMB M-25-21, M-25-22, and M-26-04) Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-09-25\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-texas.md`](annex-ai-us-texas.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`ai/jurisdictions/annex-ai-us-california.md`](annex-ai-us-california.md), [`ai/jurisdictions/annex-ai-us-illinois.md`](annex-ai-us-illinois.md), [`ai/jurisdictions/annex-ai-us-new-york-city.md`](annex-ai-us-new-york-city.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to, rescission of, or replacement of OMB M-25-21, M-25-22, or M-26-04, the executive orders they implement, or Executive Order 14365 and the federal actions it directs\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-federal.md`](annex-ai-us-federal.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of United States federal executive-branch AI policy: three Office of Management and Budget (OMB) memoranda, M-25-21 on federal agency use of AI, M-25-22 on federal acquisition of AI, and M-26-04 on the Unbiased AI Principles for agency-procured large language models (LLMs), set against America's AI Action Plan (July 2025) and Executive Order 14365 on state AI laws. It sits alongside the `ai/jurisdictions/` US-state annexes (California, Colorado, Illinois, New York City, and Texas).

The memoranda differ in kind from those state statutes. They are executive-branch policy directed to federal agencies, not legislation that binds the public: M-25-21 states that it "governs only agencies' own use of AI and does not create rights or obligations for the public". They have two readerships. A covered federal agency applies them directly. A private organization that sells AI systems or services to a covered agency meets them indirectly, as contract terms, because M-25-22 and M-26-04 direct agencies to write requirements into solicitations and contracts. This annex frames the memoranda for both readers and cross-references the operational substance rather than restating it; the controlling texts are the memoranda themselves.

## Applicable instruments and issuing authority

- **OMB Memorandum M-25-21**, "Accelerating Federal Use of AI through Innovation, Governance, and Public Trust" (3 April 2025). It is issued under Executive Order 14179, "Removing Barriers to American Leadership in Artificial Intelligence" (23 January 2025), and consistent with the AI in Government Act of 2020, which required its issuance. It rescinds and replaces OMB M-24-10.
- **OMB Memorandum M-25-22**, "Driving Efficient Acquisition of Artificial Intelligence in Government" (3 April 2025). It rescinds and replaces OMB M-24-18.
- **OMB Memorandum M-26-04**, "Increasing Public Trust in Artificial Intelligence Through Unbiased AI Principles" (11 December 2025), issued to implement Executive Order 14319, "Preventing Woke AI in the Federal Government" (23 July 2025), which directed OMB to issue guidance applying the order's two Unbiased AI Principles.
- **America's AI Action Plan** (the White House, July 2025), organized around three pillars: innovation, infrastructure, and international diplomacy and security. Its operative content is framed as recommended policy actions; this annex treats it as strategy context, not as a source of obligations.
- **Executive Order 14365**, "Ensuring a National Policy Framework for Artificial Intelligence" (11 December 2025), which sets a policy of a minimally burdensome national framework for AI and directs federal action on state AI laws (see the section on the state annexes below).
- **OMB** issues the memoranda and receives the agency reporting they require; each agency's Chief AI Officer (CAIO) carries the agency-level responsibilities M-25-21 assigns.

Version-sensitive facts (issuance dates, the M-26-04 sunset, and the last upstream verification) are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (the US OMB rows); this annex cross-references them rather than re-deriving them. Two defects in the published source documents affect citation. M-26-04's first footnote names the implemented order as "Executive Order 14139" while its body and the order's own title and date identify Executive Order 14319; this annex cites 14319. M-25-22's Section 3 items are printed with the letters b through h while the memorandum's own cross-references use a sequence shifted back by one letter (for example, "Section 3(c)" for privacy, which is printed as item d); this annex therefore cites M-25-22's Section 3 items by heading, not by letter.

## Transition timeline

The principal deadlines run from each memorandum's issuance date; the calendar dates in parentheses are computed from the stated day counts.

- **M-25-21 (issued 3 April 2025):** each agency retains or designates a Chief AI Officer within 60 days; each Chief Financial Officers Act (CFO Act) agency convenes an AI governance board within 90 days and develops an AI Strategy within 180 days; within 180 days (30 September 2025), and again after any update to the memorandum and every two years thereafter until 2036, each agency submits to OMB and posts publicly either a compliance plan or a written determination that it does not use and does not anticipate using covered AI; within 270 days (29 December 2025) agencies revisit, and update where necessary, their internal policies on IT infrastructure, data, cybersecurity, and privacy, and should develop a generative-AI acceptable-use policy; and within 365 days (3 April 2026) agencies document implementation of the minimum risk management practices for high-impact AI.
- **M-25-22 (issued 3 April 2025):** applies to any contract awarded under a solicitation issued on or after the date 180 days after issuance (30 September 2025), and to any option to renew or extend an existing contract exercised after that date; within 270 days agencies revisit, and update where necessary, their internal acquisition procedures.
- **M-26-04 (issued 11 December 2025):** agencies update procurement policies and procedures no later than 11 March 2026; the memorandum ceases to have force or effect two years after issuance (11 December 2027) unless the Director of OMB provides otherwise.

## Scope: covered actors and covered systems

- **M-25-21, covered agencies:** except as specifically noted, all agencies defined in 44 U.S.C. 3502(1), including independent regulatory agencies. Some requirements apply only to CFO Act agencies, and some do not apply to elements of the Intelligence Community.
- **M-25-21, covered AI:** new and existing AI that is developed, used, or acquired by or on behalf of covered agencies, subject to the memorandum's stated exclusions.
- **M-25-22, covered agencies and AI:** AI systems or services acquired by or on behalf of covered agencies (the 44 U.S.C. 3502(1) agencies, with some requirements limited to CFO Act agencies). Its requirements do not apply to elements of the Intelligence Community. The term excludes any common commercial product within which AI is embedded, such as a word processor or map navigation system; in deciding whether a product falls in that exception, agencies assess whether it is widely available to the public for commercial use and whether the AI is embedded in a product with substantial non-AI purposes. The memorandum also does not govern: regulatory actions prescribing policy for non-agency AI use; assessments of an AI application because its provider is the target of an enforcement, law-enforcement, or national-security action; development of general-use AI metrics, methods, and standards; acquisition of AI for basic, applied, or experimental research (unless to develop a particular agency AI application); AI used incidentally by a contractor during performance (at the contractor's option, when not directed or required to fulfill the contract); and AI acquired as a component of a National Security System.
- **M-26-04:** any LLM procured by an agency (an executive department, military department, independent establishment, or wholly owned government corporation, as defined in the memorandum), regardless of how the LLM will be deployed, modified, or used. It does not apply to national security systems, though application to them is encouraged where practicable. Agencies are not required to apply it to LLMs acquired under a free, open-source license, but should perform due diligence on their alignment with the principles and with M-25-21 before use; and agencies consider whether to apply it to agency-developed LLMs and to AI models other than LLMs.

## Core obligations: agencies using high-impact AI (M-25-21)

**High-impact AI.** AI is high-impact when its output serves as a principal basis for decisions or actions that have a legal, material, binding, or significant effect on rights or safety, whether or not a human oversees the decision or action. M-25-21 lists categories of use presumed to be high-impact; an agency official who determines that a use in a presumed category is not high-impact documents that determination in writing to the CAIO.

**Minimum risk management practices.** For each high-impact use, the agency must:
1. **Conduct pre-deployment testing** and prepare risk mitigation plans reflecting expected real-world outcomes. Where the agency lacks access to the underlying source code, models, or data, it must use alternative test methods, such as querying the AI service and observing the outputs, or providing evaluation data to the vendor and obtaining the results.
2. **Complete an AI impact assessment** before deployment, updated periodically and through the lifecycle as appropriate, documenting at minimum: intended purpose and expected benefit; the quality and appropriateness of the data and model capability; potential impacts on privacy, civil rights, and civil liberties (the assessment should also describe planned mitigation measures for anticipated negative impacts); reassessment scheduling and procedures; related costs; the results of an independent review by an agency reviewer not involved in development; and risk acceptance, supported by the signature of the individual accepting the risk.
3. **Conduct ongoing monitoring** for performance and adverse impacts, designed to detect unforeseen circumstances, post-deployment changes to the system, and changes to the context of use or its data.
4. **Train and assess operators** sufficiently and periodically, so that those who interpret and act on the AI's output can manage its risks.
5. **Provide human oversight, intervention, and accountability** suitable for high-impact use, including, when practicable and consistent with existing agency practices, an appropriate fail-safe that minimizes the risk of significant harm.
6. **Offer consistent remedies or appeals:** individuals affected by AI-enabled decisions have access to timely human review and a chance to appeal negative impacts, where appropriate.
7. **Consult and incorporate feedback** from end users and the public on the use case, where appropriate.

**Non-compliance, pilots, and waivers.** A high-impact use that does not meet the minimum practices must be safely discontinued. A pilot is exempt from the minimum practices if it is of limited scale and duration, the CAIO has certified it (with the certification tracked centrally), individuals who may interact with it can opt in and out where possible with sufficient notice to make an informed decision, and the practices are applied where practicable. The CAIO, in coordination with other relevant officials, may waive a practice for a specific application only on a written determination, based on a system-specific and context-specific risk assessment, that fulfilling it would increase risks to safety or rights overall or would create an unacceptable impediment to critical agency operations. The responsibility may not be delegated; each waiver is recertified annually and reassessed after significant changes to its conditions or context; a waiver grant or revocation is reported to OMB within 30 days; and, to the extent consistent with law and governmentwide policy, a summary of each determination and waiver is released publicly.

**Agency governance.** Beyond high-impact AI, M-25-21 requires the Chief AI Officer, the CFO Act agency AI governance board and AI Strategy, the published compliance plans or no-use determinations, and an AI use-case inventory submitted to OMB and posted publicly at least annually (the Department of Defense and the Intelligence Community excepted).

## Obligations reaching AI vendors through contracts

**M-25-22 (acquisition).** For contracts within its scope, M-25-22 directs agencies, "where applicable", to include terms addressing the following in contracts for AI systems and services, which makes them contractual obligations on the vendor:
- **IP rights and lawful use of government data:** agencies must include appropriate terms, consistent with the processes each agency adopts under the Section 3 item headed "Protect IP Rights and Use of Government Data". Those processes should address, among other matters, contracts that permanently prohibit the use of non-public inputted agency data and outputted results to further train publicly or commercially available AI algorithms, consistent with applicable law, absent explicit agency consent.
- **Privacy:** agencies establish policies and processes, including contractual terms and conditions, that secure compliance with privacy requirements whenever an agency acquires an AI system or service, or an agency contractor uses one, that will handle federal information containing personally identifiable information (under the Section 3 item headed "Protect Privacy"). This reaches a contractor's use of AI with such information even where the AI is not itself the acquired product.
- **High-impact compliance:** contracts must require compliance with the M-25-21 minimum risk management practices for high-impact use cases, and for systems with potential or expected high-impact uses the agency informs vendors of the transparency and documentation it will require, such as the descriptive information needed to complete the AI impact assessment.
- **Testing and monitoring:** contractual terms give the agency the ability to monitor and evaluate the system's performance, risks, and effectiveness regularly; vendors must provide the access and time agencies need to complete independent evaluation (or, where the agency allows vendor-run testing, produce results detailed enough to be independently verified or reproduced if practicable); and contracts must detail the vendor's examination, testing, and validation procedures and must not prohibit the agency from internally disclosing how the vendor conducts testing or its results.
- **Vendor lock-in protections:** terms such as knowledge transfer, data and model portability, agency rights to code and models produced in performance of the contract, and transparency in licensing and pricing.
- **Authorization to operate:** any AI system or service operated as an information system by or on behalf of an agency must receive an authorization to operate before deployment.
- **Recommended, not required:** agencies are encouraged to require vendor performance monitoring, performance standards before a new version is deployed, and roll-back when a new version fails them; and should consider requiring notice before new AI features are integrated into a delivered system.
- **Disclosure of a vendor's own AI use:** agencies must determine whether circumstances merit including a solicitation provision requiring the vendor to disclose its use of AI in performing the contract (under the Section 3 item headed "Determine Necessary Disclosures of AI Use in the Fulfillment of a Government Contract"); the determination is required, the resulting provision is not.

**M-26-04 (Unbiased AI Principles).** The two principles are truth-seeking (LLMs are truthful in responding to requests for factual information or analysis, prioritize historical accuracy, scientific inquiry, and objectivity, and acknowledge uncertainty where reliable information is incomplete or contradictory) and ideological neutrality (LLMs are neutral, nonpartisan tools that do not manipulate responses in favour of ideological dogmas, and developers do not intentionally encode partisan or ideological judgments into outputs unless those judgments are prompted by or readily accessible to the end user). For the vendor:
- agencies must include contractual requirements addressing compliance with the principles in any LLM solicitation or order issued after the memorandum's date;
- agencies should, to the extent practicable, modify existing LLM contracts to include those requirements, at the latest before exercising any option that extends performance;
- in LLM solicitations, agencies must request, at minimum, the vendor's acceptable use policy, model, system, or data cards, end-user resources, and a mechanism for end-user feedback on outputs that violate the principles; must also request information on LLM development and operation where an LLM is integrated into another product or service being procured; and may request enhanced transparency (for example, pre-training and post-training activities affecting factuality, and system-level prompts) where the planned use warrants it; and
- agencies should identify the requirements as material to eligibility and payment under the contract, to support termination of the contract for default where a vendor refuses to take corrective action on identified noncompliance.

Separately, and as an agency duty rather than a vendor one, each agency's updated procurement policies must include a process through which agency users of LLMs report outputs that violate the principles.

## Public rights

M-25-21 creates no rights enforceable by the public. The remedies-and-appeals and public-feedback practices are agency duties owed within the agency's own processes, and the public's visibility comes through the published compliance plans, use-case inventories, and waiver summaries. This annex states that plainly rather than implying individual remedies of the kind the state statutes provide.

## Oversight and enforcement

- **OMB oversight through reporting:** compliance plans or no-use determinations submitted to OMB and posted publicly, the annual use-case inventory, waiver reporting within 30 days, and documentation of the minimum practices on OMB's request or in its periodic accountability reviews.
- **Termination:** a high-impact use that cannot meet the minimum practices is discontinued; the pilot exemption and the waiver are the only sanctioned alternatives.
- **Vendor consequences:** the memoranda contain no statutory penalty schedule of their own. For a vendor, the consequence of non-compliance runs through the contract under the terms the agency has written into it, including, where an agency has identified the M-26-04 requirements as material, termination for default.

## National strategy context

America's AI Action Plan sets the national direction the memoranda operate within. Among its recommended policy actions are that OMB work with agencies that have AI-related discretionary funding to consider a state's AI regulatory climate when making funding decisions and to limit funding where a state's AI regulatory regime may hinder the effectiveness of that funding; that NIST revise the AI Risk Management Framework; and that federal procurement guidelines be updated so that the government contracts only with frontier LLM developers whose systems are objective and free from top-down ideological bias, the direction M-26-04 implements for agency LLM procurement. These are recommendations, not obligations.

## Relationship to the state annexes

The three memoranda govern agencies' own use and acquisition of AI; none of them purports to displace a state AI statute, so an organization that is both a federal vendor and subject to a state statute covered in the other `ai/jurisdictions/` US annexes plans to meet both. Executive Order 14365 is the federal instrument aimed at state AI laws. It directs the Attorney General to establish an AI Litigation Task Force whose sole responsibility is to challenge state AI laws inconsistent with the order's policy, including on the grounds that they unconstitutionally regulate interstate commerce or are preempted by existing federal regulations; directs the Secretary of Commerce to publish an evaluation of existing state AI laws and to set conditions on remaining Broadband Equity Access and Deployment (BEAD) funding for states with such laws; directs the Federal Communications Commission to consider a federal AI reporting and disclosure standard that preempts conflicting state laws, and the Federal Trade Commission to issue a policy statement on state laws that require deceptive conduct in AI models; and calls for a legislative recommendation for a uniform federal framework that preempts conflicting state AI laws. The order names Colorado's algorithmic-discrimination law as an example. Whether any particular state law is displaced is a matter for litigation, rulemaking, or legislation, not for this annex; an adopter tracks the outcome before relying on a state annex's obligations falling away.

The Texas annex records that TRAIGA's internal-review no-liability route is conditioned on substantial compliance with the NIST AI RMF Generative AI Profile or another recognized framework (see [`ai/jurisdictions/annex-ai-us-texas.md`](annex-ai-us-texas.md)); an adopter using the NIST AI RMF for both purposes records how the federal minimum practices map onto it.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the memoranda or for legal advice; the controlling texts are the memoranda as issued.
- **Version sensitivity.** Executive-branch memoranda and orders can be rescinded or replaced without legislation, as M-25-21 and M-25-22 themselves rescinded M-24-10 and M-24-18. M-26-04 sunsets on 11 December 2027 unless extended, and the actions Executive Order 14365 directs may change the state-law landscape. An adopter reconfirms the current position upstream before committing to a compliance milestone.
- **Source-document defects.** The M-26-04 footnote and M-25-22 Section 3 lettering defects described above are in the published documents; this annex cites around them rather than reproducing them.
- **Selective coverage.** The annex states the principal obligations and deadlines; it does not restate every appendix item of the memoranda.
- The corpus operational substance this annex references is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

The federal-instrument column is the load-bearing, held-source-grounded content. The NIST AI RMF function tags and the ISO/IEC 42001:2023 clause and Annex A anchors are a crosswalk to help an adopter reuse its existing management-system controls; they are a mapping aid, partial for bundled rows, not an assertion that the memoranda and those standards impose the same obligations.

| Requirement | US federal instrument | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Chief AI Officer, governance board, strategy, and compliance plans | M-25-21 | Govern | Clause 5 |
| High-impact determination and AI impact assessment with independent review | M-25-21 | Map, Measure | Annex A.5 |
| Signed risk acceptance for a high-impact use | M-25-21 | Manage | Clause 6.1.3 |
| Pre-deployment testing and ongoing monitoring | M-25-21 | Measure, Manage | Annex A.6 |
| Operator training and assessment | M-25-21 | Govern | Clause 7.2 |
| Human oversight, fail-safe, and remedies or appeals | M-25-21 | Govern, Manage | Annex A.9 |
| Public and end-user feedback | M-25-21 | Measure | Annex A.8 |
| Contractual IP and data-use, privacy, testing-access, lock-in, and high-impact compliance terms for AI vendors | M-25-22 | Govern, Manage | Annex A.10 |
| LLM transparency artefacts (acceptable use policy, model, system, or data cards) and feedback mechanism | M-26-04 | Map, Govern | Annex A.8, Annex A.10 |
