# United States Privacy Regulatory Requirements

**Document Title:** United States Privacy Regulatory Requirements 
**Document Type:** Annex 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Privacy Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md) 
**Classification:** Public 
**Category:** Privacy 
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change 
**Repository Path:** [`privacy/jurisdictions/annex-privacy-united-states.md`](annex-privacy-united-states.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to processing of personal data in the United States under the FTC Act, federal sector-specific laws, and state comprehensive privacy laws. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

The United States does not have a single comprehensive federal privacy law. Obligations arise from a patchwork of federal sector-specific laws, FTC Act enforcement, and state-level comprehensive privacy laws.

### Federal laws

- **FTC Act (15 U.S.C. § 45):** The FTC prohibits unfair or deceptive acts or practices in commerce. The FTC treats material misrepresentations about privacy practices, inadequate data security, and harmful AI practices as unfair or deceptive.
- **HIPAA:** Governs protected health information held by covered entities and their business associates.
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
- **Illinois BIPA:** Requires informed written consent before collecting biometric identifiers. Private right of action: USD 1,000 to 5,000 per violation.
- **Colorado AI Act (SB 205, effective February 2026):** Requires developers and deployers of high-risk AI to use reasonable care to avoid algorithmic discrimination; requires DPIAs, transparency notices, and right to appeal automated decisions.

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
- **EU-US Data Privacy Framework (DPF):** Organizations certified under the DPF can receive personal data from the EU, UK (via UK Extension), and Switzerland without additional transfer mechanisms. Administered by the International Trade Administration (ITA).
- **CCPA:** Does not restrict cross-border transfers but requires contractual data protection obligations on service providers and contractors.
- **State health data laws:** Washington My Health My Data Act and similar laws restrict sharing of consumer health data across borders.

---

## Enforcement and fines

### FTC

- No specific fine structure for first violations; injunctive relief and consent orders are typical. Subsequent consent order violations: civil penalties up to USD 51,744 per violation per day.

### CCPA/CPRA

- CPPA: Up to USD 2,500 per unintentional violation; USD 7,500 per intentional violation. Violations involving minors treated as intentional.
- Private right of action: USD 100 to 750 per consumer per incident for data breaches from inadequate security (or actual damages if greater).

### BIPA (illinois)

- Private right of action: USD 1,000 per negligent violation; USD 5,000 per intentional or reckless violation. Class action settlements have exceeded USD 600 million.

### State attorneys general

- Enforcement authority under all state comprehensive privacy laws; fines range USD 2,500 to 50,000 per violation depending on state.

### HIPAA

- Civil monetary penalties: USD 137 to 2,067,813 per violation category per year depending on culpability tier. Enforced by HHS Office for Civil Rights (OCR).

---

## Limitations

This document is a public-domain reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
