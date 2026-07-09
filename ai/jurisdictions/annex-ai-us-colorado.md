# Colorado AI and Automated Decision-Making Technology Regulatory Requirements

**Document Title:** Colorado AI and Automated Decision-Making Technology Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to the Colorado ADMT statute, its effective date, or the pending litigation\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of Colorado's artificial-intelligence statute, the first US-state AI law of its kind. Colorado is a two-regime jurisdiction: the original Colorado Artificial Intelligence Act (Senate Bill 24-205, C.R.S. 6-1-1701 et seq.) was repealed and re-enacted with substantial amendments by Senate Bill 26-189 (Automated Decision-Making Technology), so an adopter must track both the outgoing SB24-205 framework and the incoming SB26-189 framework that governs consequential decisions made on or after 1 January 2027. This annex presents both regimes, flags the material differences between them, and frames which obligations land on the adopter as developer or deployer. It cites the enacted texts and cross-references the litigation status rather than restating it.

Alongside [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), this annex is a founding document of the `ai/jurisdictions/` subdirectory, mirroring the `privacy/jurisdictions/` model.

## Applicable law and regulatory authority

- **Senate Bill 24-205**, "Consumer Protections for Artificial Intelligence" (Colorado Artificial Intelligence Act), C.R.S. 6-1-1701 et seq., signed 17 May 2024. The outgoing regime, organized around the "high-risk artificial intelligence system" and "algorithmic discrimination".
- **Senate Bill 26-189**, "Automated Decision-Making Technology", which repeals and re-enacts part 17 with amendments and applies to consequential decisions made on or after 1 January 2027. The incoming regime, organized around "automated decision-making technology" (ADMT) used in a "consequential decision".
- **The Colorado Attorney General** is the exclusive enforcer under both regimes; there is no private right of action. The Attorney General enforces through the Colorado Consumer Protection Act, and a violation is a deceptive trade practice (SB26-189 6-1-1706). The Attorney General may promulgate implementing rules (SB24-205 6-1-1707; SB26-189 directs rules on or before 1 January 2027).

The controlling texts are the statutes themselves. The litigation history and effective-date sequence are version-sensitive and are maintained, with dates, in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (the "Colorado AI Act" row) and [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md); this annex cross-references them rather than re-deriving the dates.

## Transition timeline

- **SB24-205** duties applied "on and after February 1, 2026" (6-1-1702, 6-1-1703). Senate Bill 25B-004 (signed 28 August 2025) postponed implementation to 30 June 2026.
- **Enforcement is currently frozen.** On 27 April 2026 the US District Court for the District of Colorado effectively froze enforcement pending litigation (xAI v. Colorado); the Colorado Attorney General has stated the office will not enforce the statute until rulemaking concludes. The litigation status and its dates are cross-referenced from [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) and [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), not asserted independently here.
- **SB26-189** was signed in May 2026 and applies to consequential decisions made on or after 1 January 2027 (developer responsibilities apply "on and after January 1, 2027", 6-1-1702(1)); the Attorney General is directed to adopt implementing rules on or before 1 January 2027.

An adopter therefore treats SB24-205 as the framework of record until the re-enactment takes effect and SB26-189 as operative for consequential decisions on or after 1 January 2027, while monitoring the pending litigation, which may further change the statute's status.

## Scope: covered actors and covered systems or decisions

Both regimes assign obligations to a **developer** (a person doing business in Colorado that develops or intentionally and substantially modifies the regulated system) and a **deployer** (a person doing business in Colorado that uses the regulated system), with a **consumer** being a Colorado resident. The organizing concept changes between the two regimes:

- **SB24-205** organizes around the **high-risk artificial intelligence system**, one that makes, or is a substantial factor in making, a **consequential decision**, and around **algorithmic discrimination** (an unlawful differential treatment or impact disfavouring an individual or group on a protected basis).
- **SB26-189** organizes around **automated decision-making technology (ADMT)** that materially influences a **consequential decision**, defined (6-1-1701(3), as re-enacted) as a decision, determination, or action about a consumer relating to the provision of, access to, eligibility for, selection for, or compensation for a **covered domain** (or one affecting a differentiated price or other material terms in a manner reasonably likely to materially limit, delay, deny, or fundamentally alter the consumer's access to a covered domain), with an enumerated set of carve-outs (low-stakes or routine business processes, advertising and content moderation, spreadsheets requiring manual human analysis, systems that only summarize or organize information for human review without producing an outcome-influencing inference, and narrow procedural or data-processing tasks). The regulated object is the **covered ADMT**; an **adverse outcome** triggers the post-decision consumer disclosures and rights.

The central change is a shift in the organizing concept from an AI-system-risk-tier model ("high-risk AI system") to a decision-consequence model ("consequential decision" reached via a "covered ADMT").

## Core obligations

- **SB24-205 developer duty** (6-1-1702): use reasonable care to protect consumers from known or reasonably foreseeable risks of algorithmic discrimination, with a rebuttable presumption of reasonable care where the developer complies with the section and the Attorney General's rules, plus documentation to be made available to deployers (intended uses, known limitations, training-data summaries, evaluation and mitigation of algorithmic discrimination). **SB24-205 deployer duty** (6-1-1703): the parallel reasonable-care duty, a risk-management policy and program, an impact assessment for high-risk systems, a consumer correction opportunity, and notice to the Attorney General on discovery of algorithmic discrimination, with a corresponding rebuttable presumption.
- **SB26-189 developer responsibilities** (6-1-1702): make available to each deployer, in an understandable form and protecting trade secrets, a general statement of intended and harmful uses, the categories of training data, known limitations and risks, instructions for appropriate use and meaningful human review, and the information the deployer needs to comply with its own disclosure duty; provide notice of material updates; and retain the compliance records for not less than three years. **SB26-189 deployer duties**: record-keeping for not less than three years (6-1-1703); a clear and conspicuous point-of-interaction notice that a covered ADMT is used in a consequential decision, satisfiable by a prominent public posting (6-1-1704(1)-(2)); and, where a covered ADMT materially influences a consequential decision that results in an adverse outcome, a post-adverse-outcome disclosure within thirty days describing the decision and the role of the ADMT and giving a process to request further information (6-1-1704(3)).

The material reframe: SB24-205 casts the core duty as avoiding algorithmic discrimination (reasonable care, backed by a rebuttable presumption); SB26-189 recasts the core duty as documentation, transparency, and point-of-interaction and post-adverse-outcome disclosure for a covered ADMT, and reorganizes the deployer obligations from a single algorithmic-discrimination risk-management duty into separate record-keeping and disclosure duties.

## Consumer rights

- **SB24-205** requires a deployer, before a high-risk AI system makes or is a substantial factor in a consequential decision, to notify the consumer and disclose the decision's purpose (6-1-1703(4)), with an opportunity to correct the data and to appeal an adverse decision; a separate provision requires a generic disclosure that a consumer is interacting with an AI system (6-1-1704), unless that is obvious to a reasonable person.
- **SB26-189** elevates consumer rights into a dedicated section (6-1-1705): when a consumer experiences an adverse outcome from a consequential decision materially influenced by a covered ADMT, the consumer may request, and the deployer must provide, instructions for requesting and correcting factually incorrect personal data (consistent with C.R.S. 6-1-1306) and an opportunity for **meaningful human review and reconsideration** of the decision, to the extent commercially reasonable. Meaningful human review is defined (6-1-1701, as re-enacted) as review by a designated individual with authority to approve, modify, or override the decision, who considers relevant primary evidence, is trained to conduct the review, does not default to the system output, and has access to the output's intended use, limitations, input categories, and principal factors. The right to correct does not extend to opinions, predictions, scores, or protected evaluations.

## Enforcement

Under both regimes the Colorado Attorney General is the exclusive enforcer and there is no private right of action. Under SB26-189 (6-1-1706), a violation of the disclosure and consumer-rights duties (6-1-1702 through 6-1-1705) is enforceable exclusively by the Attorney General as a deceptive trade practice under the Colorado Consumer Protection Act. Before an enforcement action, the Attorney General issues a notice of violation where a cure is deemed possible; if the developer or deployer fails to cure within **sixty days** of the notice, the Attorney General may bring an action. No cure period is required where the Attorney General demonstrates a knowing or repeated violation. The Attorney General reports annually on enforcement actions and cure periods beginning in January 2028. SB24-205 provided for Attorney-General enforcement under 6-1-1706 and rulemaking under 6-1-1707.

## Relationship to the Colorado Privacy Act

Colorado's automated-decision-making obligations intersect with the profiling and opt-out provisions of the Colorado Privacy Act (CPA, SB21-190, C.R.S. 6-1-1301 et seq.), under which a consumer may opt out of profiling in furtherance of decisions that produce legal or similarly significant effects. This annex governs the AI-statute per-regime framing; the privacy-law profiling intersection and the broader US privacy posture are carried in [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), which this annex cross-references rather than duplicates.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the enacted statutes or for legal advice; the controlling texts are SB24-205 and SB26-189 and the Attorney General's implementing rules.
- **Pending litigation and rulemaking.** Enforcement is frozen pending xAI v. Colorado, and the Attorney General has stated the office will not enforce until rulemaking concludes; the statute's status may change. An adopter tracks the Colorado General Assembly, the Attorney General's rulemaking, and the US District Court for the District of Colorado, and confirms the current status before committing to a compliance milestone. The litigation and effective-date facts are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) and [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md).
- Detail that the statute delegates to Attorney-General rules (the scope of covered domains, the mechanics of meaningful human review, and the disclosure templates) is not fixed in the enacted text; the adopter confirms the current position against the rules as adopted.
- The corpus operational substance this annex references (the AI classification and impact-assessment workflow, the algorithmic-discrimination and adverse-outcome controls) is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | Colorado AI statute | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Developer documentation and disclosure to deployers | SB24-205 6-1-1702; SB26-189 6-1-1702 | Govern, Map | Clause 8 |
| Deployer risk management and record-keeping | SB24-205 6-1-1703; SB26-189 6-1-1703 | Manage | Clause 8.3 |
| Consumer notice and point-of-interaction transparency | SB24-205 6-1-1703(4), 6-1-1704; SB26-189 6-1-1704 | Govern | Clause 8.4 |
| Consumer correction and meaningful human review | SB26-189 6-1-1705 | Manage | Clause 8.3 |
| Adverse-outcome and algorithmic-discrimination controls | SB24-205 6-1-1702, 6-1-1703; SB26-189 6-1-1704 | Measure, Manage | Clause 8.3 |
