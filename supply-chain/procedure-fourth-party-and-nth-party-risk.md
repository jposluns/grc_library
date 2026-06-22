# Fourth-Party and Nth-Party Risk Procedure

**Document Title:** Fourth-Party and Nth-Party Risk Procedure\
**Document Type:** Procedure\
**Version:** 1.0.2\
**Date:** 2026-06-22\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md), [`supply-chain/register-concentration-risk.md`](register-concentration-risk.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md)\
**Classification:** Public\
**Category:** Supply Chain Governance\
**Review Frequency:** Annual and upon material change to the supplier ecosystem, regulatory expectation, or concentration risk posture\
**Repository Path:** [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](procedure-fourth-party-and-nth-party-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how the organisation identifies, monitors, and escalates risk arising from suppliers beyond the direct third-party relationship: fourth-party (the supplier's supplier) and nth-party (any subsequent tier). It supports DORA's critical-ICT-third-party regime, GDPR Article 28 sub-processor obligations, NIS 2 supply-chain security obligations, and the organisation's broader supplier governance.

---

## Scope

This procedure applies to all third-party relationships within scope of the supplier security and privacy assurance standard where the third party itself depends on further suppliers to deliver the service to the organisation. It applies regardless of contract type (SaaS, managed service, professional services, hardware, logistics).

It does not duplicate per-supplier due diligence; it overlays the existing supplier lifecycle with the multi-tier visibility actions the organisation can take.

---

## Definitions

| Term | Definition |
| --- | --- |
| Third party | A supplier with a direct contractual relationship with the organisation |
| Fourth party | A supplier whose service is consumed by a third party in delivering services to the organisation |
| Nth party | Any subsequent tier in the supply chain (fifth, sixth, etc.) |
| Sub-processor | Under GDPR / UK GDPR, a third party engaged by the controller's processor to process personal data on the controller's behalf |
| Critical sub-tier supplier | A fourth-party or nth-party supplier whose failure would materially affect the third party's ability to deliver service to the organisation |
| Concentration risk | The risk that multiple third parties share a common sub-tier dependency such that a single sub-tier failure has cross-portfolio impact |

---

## Visibility tiers

Visibility into the supply chain decreases with each tier. The procedure applies a tiered visibility expectation aligned to supplier criticality.

| Supplier criticality tier | Tier visibility expectation |
| --- | --- |
| Tier 1: Critical | Disclosed list of all fourth parties supporting the service; contractual right to be notified of fourth-party changes; concentration analysis at the fourth-party layer; selected nth-party visibility for known systemic dependencies |
| Tier 2: High | Disclosed list of material fourth parties (those with access to organisational data or that operate the critical infrastructure of the service); notification of material fourth-party changes |
| Tier 3: Moderate | Disclosed sub-processor list where personal data is processed; notification of sub-processor changes |
| Tier 4: Low | No tier-visibility requirement beyond contractual baseline |

---

## Identification

The Supplier Relationship Owner (SRO) identifies sub-tier suppliers through the following inputs:

1. **Contractual disclosure.** The contract with the third party requires disclosure of fourth parties at the criticality-driven granularity. Disclosure includes name, country, service provided, and a categorisation flag (cloud platform, identity provider, payment processor, data processor, communications, etc.).
2. **Sub-processor list.** Where the third party processes personal data on the organisation's behalf, the sub-processor register is the authoritative source.
3. **Service architecture diagram.** The third party provides a high-level architecture that names the categories of sub-tier dependencies.
4. **Service organisation control reports.** SOC 2, ISAE 3402, and equivalent reports name the third party's material sub-service providers and the controls relied upon.
5. **Public attestations and registries.** Where the third party publishes a sub-processor or partner list, the SRO references the public source.
6. **Targeted intelligence.** For Tier 1 critical suppliers, threat intelligence and open-source reporting on the third party's known dependencies.

---

## Procedure steps

### Step 1: Identify

The SRO maintains a per-third-party record of disclosed sub-tier suppliers. The record includes for each sub-tier supplier:

| Field | Description |
| --- | --- |
| Sub-tier supplier name | As disclosed; private record |
| Tier | Fourth, fifth, etc. |
| Service provided | What the sub-tier supplier does for the third party |
| Country of operation | For data residency and geopolitical risk |
| Critical-sub-tier designation | Yes or no, with rationale |
| Personal data processed | Yes or no |
| Contractual flow-down confirmed | Yes or no |
| Date last updated | |

### Step 2: Assess sub-tier risk

For each disclosed sub-tier supplier identified as critical:

1. Determine whether the failure of the sub-tier supplier would interrupt the service the third party provides to the organisation.
2. Determine whether the third party has documented contingency for the sub-tier supplier's failure (alternate, manual fallback, time-bound continuity plan).
3. Determine whether the sub-tier supplier appears in the concentration risk register (i.e. is shared across multiple third parties).
4. Categorize the residual risk: Negligible, Low, Moderate, High, Unacceptable.

The output is captured in the supplier risk record for the third party and cross-referenced to the concentration risk register.

### Step 3: Monitor

Sub-tier risk is monitored on an ongoing basis. Triggers for review:

| Trigger | Action |
| --- | --- |
| Third party notifies of a sub-tier supplier change | Update record; reassess if the change affects critical sub-tier |
| Sub-tier supplier itself has a publicly disclosed incident | Engage the third party; assess impact; record in the incident timeline |
| Sub-tier supplier classified as a critical ICT third party under DORA (or equivalent) | Update record; flag concentration risk; engage the third party on contractual contingency |
| Sub-tier supplier becomes subject to sanctions, export controls, or geopolitical restriction | Engage the third party urgently; assess substitutability |
| Concentration analysis identifies a new shared dependency | Update concentration risk register; reassess critical sub-tier designation |
| Sub-tier supplier merger or acquisition by a higher-risk entity | Reassess; engage third party |

### Step 4: Escalate

The SRO escalates to the Supplier Risk Maintainer when:

1. A critical sub-tier supplier failure or incident occurs.
2. The residual risk classification moves to High or Unacceptable.
3. The concentration risk crosses the appetite threshold (multiple critical third parties share an undocumented or unsubstitutable sub-tier dependency).
4. The third party refuses or repeatedly fails to disclose sub-tier information that the contract requires.

Escalation to the CISO and CIO follows for any Tier 1 critical-sub-tier event. Where personal data is implicated, the Privacy Officer is engaged.

### Step 5: Treat

Treatment options, in order of preference:

1. **Reduce concentration.** Request the third party adopt alternate sub-tier suppliers; diversify the organisation's own portfolio of third parties so a single sub-tier failure has less impact.
2. **Strengthen contingency.** Require the third party to document and test fallback procedures for the critical sub-tier dependency.
3. **Strengthen contractual rights.** Negotiate stronger sub-tier disclosure, audit, and notification rights at next contract renewal.
4. **Transfer.** Use insurance or contractual indemnity where economically rational.
5. **Avoid.** Exit the third-party relationship if sub-tier risk is unacceptable and unmitigated.
6. **Accept.** Formal acceptance per the exception policy where treatment is not economically rational and residual risk is within appetite.

### Step 6: Record and report

Sub-tier risk findings are reported to the Supplier Risk Maintainer at minimum quarterly. Tier 1 critical sub-tier events are reported immediately on identification. Aggregate sub-tier posture is included in the annual supplier-risk report to the Executive Sponsor.

---

## Coordination with adjacent procedures

| Source | Coordination point |
| --- | --- |
| Supplier due diligence | Pre-engagement sub-tier disclosure as a gating criterion for Tier 1 and Tier 2 |
| Supplier ongoing monitoring | Periodic re-verification of disclosed sub-tier supplier list |
| Subprocessor register | For personal-data-processing scenarios; authoritative source |
| Concentration risk register | Cross-portfolio shared dependency analysis |
| Cross-domain incident coordination | Sub-tier supplier incidents that affect the organisation route through the standard incident procedure |
| Privacy breach response | Sub-tier supplier breaches involving personal data |

---

## Operating expectations

1. Tier 1 critical sub-tier register is reviewed quarterly with the SRO.
2. Tier 2 material sub-tier register is reviewed semi-annually.
3. Concentration analysis is refreshed at minimum semi-annually and after any material change in the supplier portfolio.
4. The procedure recognises that visibility beyond the fourth tier becomes proportionate; nth-party visibility is best-effort intelligence rather than contractual right.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| DORA | Articles 28 to 44 (third-party ICT risk including subcontracting) | EU financial services |
| GDPR / UK GDPR | Article 28 (sub-processor obligations) | Personal data processing |
| NIS 2 | Article 21(2)(d) (supply chain security) | EU essential entities |
| NIST CSF 2.0 | GV.SC subcategories | Supply chain risk management |
| NIST SP 800-161 Rev. 1 | Cybersecurity Supply Chain Risk Management | US baseline |
| ISO 28000 | Security management for supply chains | International |
| ISO/IEC 27036 | Information security for supplier relationships | Supplier security |
| FSB Cyber Lexicon and Third-Party Risk Toolkit | Financial Stability Board | International financial-sector practice |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Effective fourth-party and nth-party risk visibility depends on the contractual rights the organisation has negotiated, the third party's willingness to disclose, the public-record availability of sub-tier information, and the maturity of the organisation's threat intelligence capability. The procedure does not guarantee visibility; it sets expectations and a treatment framework.

---

**End of Document**
