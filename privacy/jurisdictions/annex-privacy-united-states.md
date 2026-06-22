# United States Privacy Regulatory Requirements

**Document Title:** United States Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.3\
**Date:** 2026-06-22\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-united-states.md`](annex-privacy-united-states.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to processing of personal data in the United States under the FTC Act, federal sector-specific laws, and state comprehensive privacy laws. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

The United States does not have a single comprehensive federal privacy law. Obligations arise from a patchwork of federal sector-specific laws, FTC Act enforcement, and state-level comprehensive privacy laws.

### Federal laws

- **FTC Act (15 U.S.C. § 45):** The FTC prohibits unfair or deceptive acts or practices in commerce. The FTC treats material misrepresentations about privacy practices, inadequate data security, and harmful AI practices as unfair or deceptive.
- **HIPAA:** Governs protected health information held by covered entities and their business associates. HHS OCR issued an NPRM on 27 December 2024 (published in the Federal Register on 6 January 2025; comment period closed 7 March 2025) proposing to overhaul the HIPAA Security Rule. The NPRM would make encryption of ePHI (at rest and in transit) and multi-factor authentication for ePHI-access systems mandatory, require an annually-refreshed technology asset inventory and ePHI network map, eliminate the "required vs addressable" implementation-specification distinction, and add explicit annual risk-analysis and vulnerability-management obligations. The final rule remained pending as of May 2026. Once published, covered entities and business associates would have 60 days to the effective date and 180 days after the effective date to reach compliance (240 days total from publication).
- **COPPA:** Governs collection of personal information from children under 13.
- **Gramm-Leach-Bliley Act (GLBA):** Governs financial institutions' treatment of consumer financial information.
- **Fair Credit Reporting Act (FCRA):** Regulates consumer reporting agencies and use of consumer reports; applicable to AI in credit, employment, and tenant screening.
- **Equal Credit Opportunity Act (ECOA) / Fair Housing Act:** Prohibit discriminatory lending and housing decisions; applicable to AI models in credit and housing contexts.

### Federal AI initiatives

- **NIST AI Risk Management Framework (AI RMF 1.0, January 2023):** A voluntary framework for managing AI risks across four functions: Govern, Map, Measure, Manage. Widely adopted by industry and referenced by regulators.
- **NIST Generative AI Profile (NIST AI 600-1, July 2024):** Addresses risks specific to generative AI including hallucination, harmful content, data privacy, and intellectual property.

### State laws

- **California CCPA/CPRA (effective 2023-01-01):** Rights to know, delete, correct, and opt out of sale or sharing. Sensitive personal information opt-out rights. California Privacy Protection Agency (CPPA) as independent enforcement agency. Automated decision-making technology (ADMT) regulations under development.
- **Other state comprehensive privacy laws:** Virginia (VCDPA), Colorado (CPA), Connecticut (CTDPA), Utah (UCPA), Texas (TDPSA), Oregon, Montana, Iowa, Indiana, Tennessee, Florida, and others. Common elements: access, correction, deletion, opt-out from targeted advertising and profiling; DPIAs for high-risk processing; opt-in consent for sensitive data.
- **Illinois BIPA:** Requires informed written consent before collecting biometric identifiers. Private right of action: USD 1,000 per negligent violation, USD 5,000 per intentional or reckless violation. **Illinois SB 2979 (effective 2 August 2024)** amended BIPA to limit recovery to a "single recovery" for the same biometric identifier collected from or disclosed to the same recipient using the same method, which materially reduces aggregate damages exposure relative to the Illinois Supreme Court's earlier per-scan accrual interpretation in Cothron v. White Castle. The amendment also recognises electronic written release. A 2026 Seventh Circuit decision held that SB 2979 applies retroactively to cases pending at its effective date.
- **Colorado AI Act (SB 24-205):** Signed by Governor Polis on 17 May 2024. The Act requires developers and deployers of high-risk AI to use reasonable care to protect consumers from algorithmic discrimination, and imposes DPIAs, transparency notices, and a right to appeal automated decisions. **Effective date is in flux:** the original effective date was 1 February 2026; Colorado SB 25B-004 (signed 28 August 2025) postponed implementation to **30 June 2026**; on 27 April 2026 the United States District Court for the District of Colorado (Magistrate Judge Cyrus Y. Chung) granted a joint motion from xAI and the Colorado Attorney General that effectively **freezes enforcement** while litigation continues (xAI filed a federal suit on 9 April 2026 on First Amendment, Dormant Commerce Clause, due process, and equal protection grounds; the U.S. Department of Justice intervened shortly after). The Governor's Working Group framework released on 17 March 2026 proposes further amendments including a 90-day cure period and a revised effective date of 1 January 2027. Adopting organisations should treat the Act as **pending in litigation** and monitor the Colorado General Assembly and the U.S. District Court for Colorado for any change of status before committing to a compliance milestone.

---

## AI and privacy obligations

### CCPA/CPRA automated decision-making

- The CPPA is developing regulations on ADMT. Draft regulations would require opt-out rights for ADMT used for significant decisions (employment, credit, health, housing, education) and for certain profiling.
- Cybersecurity audits and risk assessments required before processing presenting significant privacy risks, including ADMT use.

### NIST AI RMF (voluntary; broadly adopted in US enterprise practice as of 2026)

- **Govern:** Establish accountability, policies, and processes for responsible AI.
- **Map:** Identify and categorize AI risks in context.
- **Measure:** Analyze and quantify AI risks using metrics and testing.
- **Manage:** Prioritize, treat, and monitor AI risks on an ongoing basis.

### FTC AI enforcement priorities

- AI systems making false or unsubstantiated capability claims.
- AI used to manipulate consumers or engage in dark patterns.
- Inadequate disclosure of AI-generated content.
- AI systems discriminating on the basis of protected characteristics.
- Inadequate security for AI systems processing sensitive personal data.
- "AI washing": misleading claims about AI capabilities or safety.

### Sectoral AI considerations

- **Financial services:** SR 11-7 model risk management guidance applies to AI in credit, fraud, and compliance decisions. Fair lending laws apply to AI-driven credit decisions.
- **Healthcare:** AI clinical decision support may qualify as a medical device subject to FDA regulation. HIPAA applies to AI processing protected health information.
- **Employment:** EEOC guidance that AI hiring tools may violate Title VII if they produce disparate impact.

---

## Cross-border transfer mechanisms

- The United States does not impose general restrictions on outbound cross-border transfers (with sector-specific exceptions such as HIPAA business associate requirements).
- **EU-US Data Privacy Framework (DPF):** Organisations certified under the DPF can receive personal data from the EU, UK (via UK Extension), and Switzerland without additional transfer mechanisms. Administered by the International Trade Administration (ITA).
- **CCPA:** Does not restrict cross-border transfers but requires contractual data protection obligations on service providers and contractors.
- **State health data laws:** Washington My Health My Data Act and similar laws restrict sharing of consumer health data across borders.

---

## Enforcement and fines

### FTC

- No specific fine structure for first violations; injunctive relief and consent orders are typical. Subsequent consent order violations: civil penalties up to USD 51,744 per violation per day.

### CCPA/CPRA

- CPPA: Up to USD 2,500 per unintentional violation; USD 7,500 per intentional violation. Violations involving minors treated as intentional.
- Private right of action: USD 100 to 750 per consumer per incident for data breaches from inadequate security (or actual damages if greater).

### BIPA (Illinois)

- Private right of action: USD 1,000 per negligent violation; USD 5,000 per intentional or reckless violation.
- Following Illinois SB 2979 (effective 2 August 2024), recovery is limited to a "single recovery" for the same biometric identifier or biometric information collected from the same person and disseminated to the same recipient using the same method of collection (that is, repeated scans of the same individual by the same system no longer compound into separate violations). The amendment substantially reduces aggregate damages exposure relative to the earlier Cothron v. White Castle per-scan accrual standard. Class-action settlements pre-dating the amendment exceeded USD 600 million; post-amendment cases are expected to be materially lower in aggregate exposure.

### State attorneys general

- Enforcement authority under all state comprehensive privacy laws; fines range USD 2,500 to 50,000 per violation depending on state.

### HIPAA

- Civil monetary penalties: USD 137 to 2,067,813 per violation category per year depending on culpability tier. Enforced by HHS Office for Civil Rights (OCR).

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organisations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
