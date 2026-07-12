# New York City Automated Employment Decision Tool Regulatory Requirements

**Document Title:** New York City Automated Employment Decision Tool Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-07-12\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to Local Law 144 or the DCWP rule\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-new-york-city.md`](annex-ai-us-new-york-city.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex gives the adopter a single per-regime view of New York City Local Law 144 of 2021, a narrow, in-force, municipal law governing the use of an automated employment decision tool (AEDT) in hiring and promotion within New York City. It is distinct from a broad AI-risk or consequential-decision statute: it regulates one class of tool (an AEDT) used for one class of decision (an employment decision) and turns on two obligations, an annual independent bias audit and a candidate notice. This annex presents those obligations, cites the enacted rule, and cross-references the version-sensitive in-force date rather than restating it.

Alongside [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md) and [`ai/jurisdictions/annex-ai-european-union.md`](annex-ai-european-union.md), this annex is a member of the `ai/jurisdictions/` subdirectory. It is kept separate from the Colorado annex because the two regimes are structurally different: Local Law 144 is a municipal, employment-only, bias-audit-and-notice regime enforced by a city agency, whereas Colorado's is a state, cross-domain consequential-decision regime enforced by the Attorney General.

## Applicable law and regulatory authority

- **Local Law 144 of 2021**, the operative statutory mandate, codified in the New York City Administrative Code (the prohibition on using an AEDT without a bias audit, the published-results requirement, and the candidate-notice requirement, at Administrative Code sections 20-870 to 20-872).
- **The Department of Consumer and Worker Protection (DCWP) final rule**, 6 RCNY 5-300 to 5-304 (Subchapter T of Chapter 5, Title 6 of the Rules of the City of New York), which implements the law: it defines the AEDT and the independent auditor, specifies the bias-audit calculations, and sets the data, published-results, and notice requirements.
- **The DCWP is the enforcing agency.** Local Law 144 provides for civil penalties (Administrative Code section 20-872); this annex cites the penalty provision by section and does not state a penalty amount, because the Administrative Code penalty text is not held in the library's reference base (see Limitations).

The controlling texts are the Administrative Code sections and the DCWP rule. The in-force date and enforcement-commencement facts are version-sensitive and are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md); this annex cross-references them rather than re-deriving them.

## Scope: covered actors and covered tools

Local Law 144 applies to an **employer or employment agency** that uses an **automated employment decision tool** to screen a candidate or employee for an **employment decision** (hiring or promotion) for a position in New York City.

An **AEDT** is defined (6 RCNY 5-300, by reference to Administrative Code section 20-870) as a computational process derived from machine learning, statistical modelling, data analytics, or artificial intelligence that issues a simplified output (a score, classification, or recommendation) and that is used to substantially assist or replace discretionary decision-making. The rule fixes "substantially assist or replace discretionary decision making" to three cases: relying solely on a simplified output; using a simplified output as one of a set of criteria where it is weighted more than any other criterion; or using a simplified output to overrule conclusions derived from other factors, including human decision-making.

## Core obligations

- **Annual independent bias audit (6 RCNY 5-301).** An employer or employment agency may not use an AEDT if more than one year has passed since the tool's most recent bias audit. The audit is conducted by an **independent auditor** (a person or group capable of exercising objective and impartial judgment, not involved in using, developing, or distributing the AEDT, not in an employment relationship with the employer or the vendor, and without a financial interest in them). For a selection tool, the audit calculates the selection rate and the impact ratio for each sex category, each race/ethnicity category, and their intersectional categories, using the categories required by the U.S. Equal Employment Opportunity Commission EEO Component 1 report; for a scoring tool, it calculates the median score, the scoring rate, and the impact ratio for the same categories. An independent auditor may exclude a category representing less than 2 percent of the data.
- **Data requirements (6 RCNY 5-302).** The bias audit must use the AEDT's historical data; test data may be used only where insufficient historical data is available to conduct a statistically significant audit, with an explanation in the published summary.
- **Published summary of results (6 RCNY 5-303).** Before using an AEDT, the employer or employment agency must make publicly available, on the employment section of its website in a clear and conspicuous manner, the date of the most recent bias audit and a summary of its results (including the data source and explanation, the number of individuals in an unknown category, and the selection or scoring rates and impact ratios for all categories) and the AEDT's distribution date, and must keep the summary posted for at least six months after the tool's latest use.
- **Candidate and employee notice (Administrative Code section 20-871(b), implemented by 6 RCNY 5-304).** The employer or employment agency must notify each candidate or employee who resides in New York City that an AEDT will be used in their assessment; the content of that notice is set by Administrative Code section 20-871(b) (which the DCWP rule implements and which the library does not hold). The DCWP rule (5-304) sets the mechanics: notice at least ten business days before the AEDT is used, the permitted delivery methods, and a requirement that the notice include instructions for requesting an alternative selection process or a reasonable accommodation, though the law does not require that an alternative be provided. On written request, the employer must within thirty days disclose information about the data the AEDT collects, its source, and the employer's data-retention policy.

## Relationship to federal anti-discrimination law

The bias audit is built on the U.S. Equal Employment Opportunity Commission's EEO-1 Component 1 race/ethnicity and sex categories and is consistent with the Uniform Guidelines on Employee Selection Procedures (29 C.F.R. section 1607.4). Local Law 144 overlays, and does not displace, the employer's obligations under Title VII and the EEOC guidelines; a bias audit satisfying Local Law 144 is not a determination of compliance with federal anti-discrimination law.

## Enforcement

The DCWP enforces Local Law 144. A violation of the bias-audit, published-results, or notice requirements is subject to civil penalties under Administrative Code section 20-872. The penalty structure and amounts are set in the Administrative Code, which the library does not hold (see Limitations); this annex cites the penalty provision by section only and states no figure. An adopter consults Administrative Code section 20-872 directly for the penalty schedule.

## Limitations

- This annex is a consolidating per-regime view, not a substitute for the enacted law or for legal advice; the controlling texts are Administrative Code sections 20-870 to 20-872 and the DCWP rule (6 RCNY 5-300 to 5-304).
- **Statutory text not held.** The library holds the DCWP final rule but not the Administrative Code sections (20-870 to 20-872) that carry the core statutory mandate and the penalty schedule. This annex attributes the audit, published-results, and notice mechanics to the DCWP rule and the statutory mandate and penalty to the Administrative Code sections by number; it does not state a penalty amount or reproduce the statutory text. An adopter needing the penalty amounts or the verbatim statutory mandate consults the Administrative Code directly.
- **Version-sensitive status.** Local Law 144 has been enforced since its enforcement-commencement date; that date and any subsequent amendment are maintained in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), and the adopter confirms the current position upstream before committing to a compliance milestone.
- Detail that the rule leaves to practice (the form of the published summary, the statistical-significance judgment for using test data) is not fixed in the enacted text; the adopter confirms the current position against the rule as adopted.
- The corpus operational substance this annex references (the AI classification and impact-assessment workflow, the bias-testing controls) is maintained in [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md) and the AI assessment procedures; on any divergence, those documents govern the operational procedure and this annex governs the per-regime framing.

## Framework alignment

| Requirement | NYC Local Law 144 / DCWP rule | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Independent bias audit within one year | 6 RCNY 5-301 | Measure, Manage | Clause 8.3 |
| Bias-audit data requirements | 6 RCNY 5-302 | Measure | Clause 8.3 |
| Published summary of audit results | 6 RCNY 5-303 | Govern | Annex A.8 |
| Candidate and employee notice | 6 RCNY 5-304 | Govern | Annex A.8 |
| Enforcement and penalties | Administrative Code section 20-872 | Govern | Clause 9 |

---

**End of Document**
