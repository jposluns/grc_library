# Canada AI Regulatory Requirements

**Document Title:** Canada AI Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.0.2\
**Date:** 2026-07-15\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to the Canadian AI regulatory landscape\
**Repository Path:** [`ai/jurisdictions/annex-ai-canada.md`](annex-ai-canada.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of Canada's approach to artificial-intelligence governance. Unlike the European Union or Colorado, Canada has **no in-force comprehensive AI statute**: the proposed federal Artificial Intelligence and Data Act (AIDA) lapsed (see below), so Canadian AI governance is a **patchwork** of a binding federal public-sector directive, federal soft-law for industry, a sector-specific financial-services guideline, a provincial public-sector statute, and a voluntary national standard. This annex presents each instrument, states its status accurately (what is in force, what is enacted but not yet in force, and what is voluntary), and frames which obligations land on the adopter. It cites the instruments by reference and cross-references the privacy layer rather than restating it.

Alongside [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md) and [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), this annex is a member of the `ai/jurisdictions/` subdirectory.

## The Canadian AI regulatory landscape: patchwork, not a statute

Canada has no omnibus AI law in force. Federal AI governance rests on a binding directive for the federal public sector, soft-law commitments for industry, and sector regulation; provincial and standards-body instruments add further layers. The corpus's operational AI substance is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md); this annex consolidates the Canadian regulatory framing and cross-references that policy rather than duplicating it.

**The Artificial Intelligence and Data Act (AIDA)**, introduced as Part 3 of Bill C-27, was Canada's proposed comprehensive federal AI statute. It **is not in force and must not be treated as law**: Bill C-27 died on the Order Paper when Parliament was prorogued, and the responsible Minister has since stated it will not return in its original form. An adopter therefore does not rely on AIDA as an obligation; the binding Canadian AI requirements are those below. (AIDA's status is a current-events fact; the adopter confirms it upstream before relying on this framing.)

## Federal public-sector automated decision-making: the Treasury Board Directive

The **Treasury Board of Canada Secretariat (TBS) Directive on Automated Decision-Making** is binding on federal government institutions that use an automated decision system to make an administrative decision about a client. It is **in force**: it took effect on 1 April 2019, with compliance required by 1 April 2020, and applies to automated decision systems developed or procured after 1 April 2020. Following its fourth review, the Directive was amended; existing automated decision systems developed or procured before 24 June 2025 have until 24 June 2026 to meet the new or updated requirements. (The 24 June 2025 date is a compliance-transition date for the updated requirements, not the Directive's in-force date, which is 2019.) The Directive is reviewed on a defined cycle.

The Directive requires the following, some obligations scaled to the impact level and others applied as a baseline: an Algorithmic Impact Assessment; transparency (notice before the decision, a meaningful explanation after it, and access to system components); quality assurance (testing, monitoring, data quality and governance, peer review, Gender-Based Analysis Plus, employee training, security, and legal review); recourse; and reporting. At the two highest impact levels the final decision must be made by a human. The TBS Guide on the Scope of the Directive sets out the five elements that bring a system into scope.

## The Algorithmic Impact Assessment

The **Algorithmic Impact Assessment (AIA)** is the mandatory risk-assessment tool under the Directive. It is a questionnaire of 65 risk questions and 41 mitigation questions (as of the 2026-05-28 version of the tool; TBS revises the question set over time) across risk areas (project, system, algorithm, decision, impact, and data) and mitigation areas (consultations and de-risking). The raw score places the system in one of four impact levels (Level I little-to-no, Level II moderate, Level III high, Level IV very high), assessed on the reversibility and duration of the impact and on impact areas including the rights, the equality, dignity, privacy and autonomy, the health and well-being, and the economic interests of individuals, and the sustainability of an ecosystem; a sufficient mitigation score reduces the level.

## Federal generative-AI guidance: the FASTER principles

The **TBS Guide on the Use of Generative AI** provides advisory guidance for federal institutions using generative AI, organized on the **FASTER** principles (Fair, Accountable, Secure, Transparent, Educated, and Relevant). It is guidance, not a binding instrument, and is updated over time.

## Federal public-service AI adoption: the AI Strategy for the Federal Public Service 2025-2027

The **AI Strategy for the Federal Public Service 2025-2027**, published by the Treasury Board of Canada Secretariat (Office of the Chief Information Officer and Chief Data Officer) on 4 March 2025, is the Government of Canada's first strategy for the responsible, secure adoption of artificial intelligence across the federal public service. It is built on four principles (human-centred, collaborative, ready, and responsible) and sets the government's internal direction for how federal institutions adopt and use AI. It is a strategy and policy direction, not a binding obligation on an external adopter; it applies to organizations subject to the Policy on Service and Digital, with exempt bodies encouraged to comply as good practice. One of its transparency deliverables is the **Government of Canada AI Register**, published as a minimum viable product by the Treasury Board of Canada Secretariat on 28 November 2025, a public inventory of the artificial-intelligence systems in use across federal institutions.

## Federal soft-law for industry: the ISED Voluntary Code

The **Voluntary Code of Conduct on the Responsible Development and Management of Advanced Generative AI Systems**, published by Innovation, Science and Economic Development Canada (ISED) in September 2023, is a **voluntary** soft-law instrument for industry. It sets six committed outcomes: accountability, safety, fairness and equity, transparency, human oversight and monitoring, and validity and robustness, with measures differentiated by role (developers and managers) and by whether a system is available for public use. It binds only its signatories, by their commitment, and it does not change existing legal obligations (for example under federal privacy law).

## National strategy: AI for All

**AI for All: Canada's National Artificial Intelligence Strategy** (ISED, launched 4 June 2026) sets the government's strategic direction across six pillars (protecting Canadians and safeguarding democracy; ensuring AI empowers Canadians; powering AI adoption for shared prosperity; building the Canadian sovereign AI foundation; scaling Canadian champions; and building trusted partnerships and global alliances). It is a strategy and policy direction, not a binding obligation on an adopter.

## Provincial: Ontario (the Enhancing Digital Security and Trust Act)

Ontario's Bill 194, the Strengthening Cyber Security and Building Trust in the Public Sector Act, 2024 (S.O. 2024, c. 24), received Royal Assent in November 2024. Its Schedule enacts the **Enhancing Digital Security and Trust Act (EDSTA), 2024**, which addresses the use of artificial intelligence by Ontario public-sector entities (public information, an accountability framework, risk-management steps, prescribed requirements, and a prohibition on certain uses, with specific disclosure and human-oversight duties). The **EDSTA is enacted but its AI provisions are not yet in force**: it comes into force on a day to be named by proclamation of the Lieutenant Governor, and its operative AI duties depend on regulations to be prescribed. An adopter operating as an Ontario public-sector entity monitors the proclamation and the regulations before treating the EDSTA AI duties as operative.

## Sector-specific: OSFI Guideline E-23 (financial institutions)

The **Office of the Superintendent of Financial Institutions (OSFI) Guideline E-23, Model Risk Management** applies to federally regulated financial institutions and governs model risk management across the model lifecycle, expressly covering artificial-intelligence and machine-learning models. It was published on 11 September 2025 and is **effective on 1 May 2027**; it is therefore a future-effective instrument that a federally regulated financial institution prepares for now. Its requirements (an enterprise model-risk-management framework, a model inventory of non-negligible-risk models, a quantitative-and-qualitative model risk rating, and lifecycle governance) are treated corpus-wide in the model-risk documents ([`ai/framework-ai-model-risk.md`](../framework-ai-model-risk.md) and [`ai/standard-ai-model-risk.md`](../standard-ai-model-risk.md)), sector-neutrally; this annex notes E-23 as the Canadian financial-services source.

## Voluntary standard: CAN/DGSI 101:2025

**CAN/DGSI 101:2025 (2nd edition), Ethical design and use of artificial intelligence by small and medium organizations**, is a voluntary national standard, oriented to small and medium organizations but broadly applicable, intended for conformity assessment. It adopts the OECD AI Principles frame and maps to the NIST AI Risk Management Framework, and it defines the human-in-the-loop, human-on-the-loop, and human-out-of-the-loop models, an ethical impact assessment, and diverse-reviewer inputs.

## Adopter-role framing

- A **federal government institution** using an automated decision system for administrative decisions is bound by the Treasury Board Directive and completes the AIA.
- An organization **developing or managing advanced generative AI** may commit to the ISED Voluntary Code (voluntary).
- A **federal government institution** adopting AI for its own operations follows the AI Strategy for the Federal Public Service 2025-2027 (a strategy and policy direction, not an obligation on an external adopter); its AI systems appear in the Government of Canada AI Register.
- A **federally regulated financial institution** prepares for OSFI Guideline E-23 (effective 1 May 2027).
- An **Ontario public-sector entity** monitors the EDSTA AI provisions (enacted, not yet in force).
- Any organization may adopt **CAN/DGSI 101:2025** for conformity assessment (voluntary).
- No adopter is bound by AIDA (lapsed) or by AI for All (strategy).

## Relationship to Canadian privacy law

Canadian AI governance intersects with federal and provincial privacy law (the Personal Information Protection and Electronic Documents Act, the federal Privacy Act, Quebec's Law 25, and provincial private-sector privacy statutes), including their automated-decision provisions. That layer is carried in [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md), which this annex cross-references rather than duplicates; the Treasury Board Directive and the ISED Voluntary Code both tie into privacy obligations, so an adopter reads the two annexes together.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the instruments themselves or for legal advice; the controlling texts are the Treasury Board Directive, the OSFI Guideline, the Ontario statute, and the standards and guidance cited.
- **Not in force / not law:** the **Artificial Intelligence and Data Act (AIDA)** lapsed and is not law; the **Ontario EDSTA AI provisions** are enacted but not yet in force (proclamation and regulations pending). **OSFI Guideline E-23** is published but not effective until 1 May 2027. These statuses are current-events facts; the adopter confirms them upstream before committing to a compliance milestone.
- The Treasury Board Directive dates are the Directive's own: effective 2019, compliance 2020, and a 24 June 2025 to 24 June 2026 compliance transition for the updated requirements. 24 June 2025 is not the Directive's in-force date.
- Detail that the Directive and the EDSTA delegate to guidance or regulations (the scope elements and the EDSTA prescribed requirements) is not fixed in the primary text; the adopter confirms the current position against the guidance and regulations as issued. (The impact-level requirement scaling itself is fixed in the Directive's Appendix C.)
- The corpus operational substance this annex references (the AI classification, impact-assessment, and model-risk workflow) is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI procedures and model-risk documents; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | Canada instrument | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Public-sector automated-decision governance and impact assessment | Treasury Board Directive on Automated Decision-Making; the Algorithmic Impact Assessment | Govern, Map, Measure | Clause 8 |
| Generative-AI governance (federal institutions) | TBS Guide on the Use of Generative AI (FASTER) | Govern | Annex A.8 |
| Federal public-service AI adoption (strategy and system inventory) | AI Strategy for the Federal Public Service 2025-2027; Government of Canada AI Register | Govern | Clause 5 |
| Responsible generative-AI development (industry) | ISED Voluntary Code of Conduct | Govern, Manage | Clause 8 |
| Financial-services model risk management | OSFI Guideline E-23 | Manage | Clause 8.3 |
| Provincial public-sector AI accountability | Ontario EDSTA, 2024 (not yet in force) | Govern | Annex A.8 |
| Ethical design and use of artificial intelligence | CAN/DGSI 101:2025 | Govern, Map, Measure, Manage | Clause 8 |

---

**End of Document**
