# Concentration Risk Register

**Document Title:** Concentration Risk Register\
**Document Type:** Register\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md), [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](procedure-fourth-party-and-nth-party-risk.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md), [`compliance/annex-nis-2-implementation.md`](../compliance/annex-nis-2-implementation.md)\
**Classification:** Public\
**Category:** Supply Chain Governance\
**Review Frequency:** Quarterly and upon material supplier portfolio, geopolitical, or regulatory change\
**Repository Path:** [`supply-chain/register-concentration-risk.md`](register-concentration-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register records the concentration of supplier dependencies across the supplier portfolio. It identifies single points of failure, shared dependencies, geographical clusters, and regulatory or geopolitical concentrations that would cause cross-portfolio impact if a concentrated dependency fails. It supports DORA's critical-ICT-third-party designation and the broader supplier risk programme.

A populated concentration register identifies specific suppliers and is sensitive operational data. This CC BY-SA 4.0 template contains no example values.

---

## Scope

The register applies to all third-party relationships in scope of the supplier security and privacy assurance standard. It includes intra-group dependencies (between legal entities of the same group) where they create concentration in the operational sense.

---

## Concentration dimensions

A concentration exists when multiple critical or material dependencies share a common attribute. The register tracks the following dimensions.

### Dimension 1: service-class concentration

Multiple suppliers in the same service category. Concentration here is normally desirable (substitutability) up to a point; the register flags where the organisation relies on a single supplier in a critical service class.

| Service class | Indicative concentration concern |
| --- | --- |
| Cloud infrastructure (IaaS) | Single-cloud reliance for production workloads |
| Identity provider | Single IdP for all human and machine identity |
| Payment processor | Single processor for all card-based revenue |
| Email and collaboration | Single platform for all communications |
| Endpoint management | Single EDR/MDM vendor for the entire estate |
| Code repository and CI/CD | Single hosted platform for all source and builds |
| Observability and logging | Single platform for all telemetry |
| Certificate authority | Single CA family for TLS termination |
| Telecoms / connectivity | Single carrier for primary connectivity |
| AI model provider | Single model provider for all AI features |

### Dimension 2: shared sub-tier dependency

Multiple third parties whose service to the organisation depends on the same fourth-party or nth-party supplier. A failure of that shared sub-tier dependency cascades through the portfolio.

| Shared sub-tier type | Common examples |
| --- | --- |
| Cloud platform | Multiple SaaS suppliers running on the same hyperscale cloud |
| Identity / authentication | Multiple SaaS suppliers federating with the same identity broker |
| Payment / financial rails | Multiple suppliers settling through the same payment scheme |
| DNS / CDN | Multiple customer-facing services depending on the same DNS or CDN provider |
| Communications | Multiple services depending on the same SMS or email gateway |

### Dimension 3: geographical concentration

Multiple suppliers operating from the same country, region, or facility. Concentration here exposes the portfolio to regional events (extreme weather, infrastructure failure, civil disturbance) and to regional regulatory action.

### Dimension 4: jurisdiction and regulatory concentration

Multiple suppliers subject to the same jurisdictional regime such that a regulatory event (data localisation order, sanctions, export controls) cascades through the portfolio.

### Dimension 5: vendor-family concentration

Multiple suppliers owned by the same parent or under a common controlling shareholder. Mergers and acquisitions can convert previously diversified suppliers into a concentration over time.

### Dimension 6: intra-group concentration

Multiple critical services delivered by legal entities of the same group, where group-level events (insolvency, sanction, restructure) cascade.

---

## Register schema

Each row records one concentration finding.

| Field | Description |
| --- | --- |
| Concentration ID | Unique identifier |
| Dimension | Service-class, shared sub-tier, geographical, jurisdiction, vendor-family, intra-group |
| Concentration subject | The shared attribute (e.g. cloud platform name, country, parent company) |
| Affected third parties | List of in-scope third parties exhibiting this concentration |
| Critical service impact | What organisational service is at risk if the concentration crystallises |
| Likelihood (descriptive) | Rare, Unlikely, Possible, Likely, Almost Certain |
| Impact (descriptive) | Negligible, Minor, Moderate, Major, Severe |
| Overall residual risk | Negligible, Low, Moderate, High, Unacceptable |
| Detection mechanism | How the concentration was identified (intelligence, contract disclosure, SOC 2 review, public registry, audit) |
| Treatment status | Open, Treating, Accepted (with reference to the exception register), Closed |
| Treatment owner | Role accountable for closure |
| Treatment plan | Specific actions (diversify, contingency strengthen, contract renegotiate, exit) |
| Target review date | When the concentration is next reviewed |
| Last reviewed | Date |
| Linked regulatory designation | If the concentration subject is a designated critical ICT third party or equivalent |

---

## Operating expectations

1. The register is reviewed quarterly by the Supplier Risk Maintainer with input from the CISO, CIO, and Privacy Officer.
2. Each Tier 1 critical third party's record cross-references the relevant concentration entries.
3. Concentration findings rated High or Unacceptable are escalated to the Executive Sponsor within the same review cycle they are identified.
4. The register feeds the annual supplier risk report to the board or board-equivalent.
5. New third parties undergo a concentration check as part of due diligence; any new concentration finding is opened immediately on onboarding.
6. The register is integrated with the geopolitical-risk briefing where the organisation operates one; events that materially change risk in a jurisdiction trigger an ad-hoc review.

---

## Treatment options

| Option | Description | Typical use |
| --- | --- | --- |
| Diversify | Add an alternate supplier; split workload across providers | Service-class concentration with available alternates |
| Decouple shared sub-tier | Choose third parties that do not share the at-risk sub-tier | Shared sub-tier concentration |
| Strengthen contingency | Require third party to demonstrate workable fallback | Where diversification is not economically rational |
| Geographic redistribution | Spread reliance across regions | Geographical concentration |
| Contractual protections | SLAs, exit assistance, audit rights, escrow | Where vendor-family or intra-group concentration cannot be eliminated |
| Insurance and indemnity | Risk transfer | Residual financial exposure |
| Exit | End the relationship | Concentration unacceptable and untreatable |
| Accept | Formal acceptance per exception policy | Within appetite and untreatable economically |

---

## Coordination with the critical ICT third-party regime

Under DORA, designated critical ICT third-party providers (CTPPs) are supervised by a Lead Overseer. Where one of the affected third parties is a CTPP, the concentration register cross-references the regulatory designation and the organisation's reliance becomes subject to additional contractual and reporting requirements.

Adopting financial entities populate per-CTPP fields including the designation date, the Lead Overseer, and the entity's contractual position with the CTPP.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Concentration coverage | Percentage of Tier 1 and Tier 2 suppliers with at least one dimension assessed | 100% |
| Concentration treatment closure rate | Percentage of identified High or Unacceptable concentrations with treatment plans within 30 days | At least 90% |
| Cross-portfolio cloud concentration | Percentage of Tier 1 suppliers running on the most-relied-upon cloud platform | Trend-monitored; tolerance per appetite |
| Single-IdP exposure | Percentage of critical authentication flows depending on a single IdP | Trend-monitored |
| Geopolitical concentration in restricted-list countries | Percentage of Tier 1 supplier operations in countries on the organisation's restricted list | Per policy |
| Designated CTPP reliance | Count of relied-upon DORA-designated critical ICT third-party providers | Trend-monitored |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| DORA | Article 29 (concentration risk assessment); Article 31 (CTPP designation criteria); Articles 35 to 40 (Oversight Framework) | EU financial services |
| EBA Guidelines on outsourcing arrangements | EBA/GL/2019/02 §76 to 80 | Banking concentration |
| FSB Cyber Lexicon and Third-Party Risk Toolkit | FSB | International financial-sector practice |
| NIS 2 | Article 21(2)(d); Article 22 (coordinated risk assessments at Union level) | EU essential entities |
| NIST SP 800-161 Rev 1 | Cybersecurity Supply Chain Risk Management | US baseline |
| ISO 28000 | Security management for supply chains | International |
| OECD Recommendation on Critical Information Infrastructure Protection | OECD | National-security framing |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. Concentration identification depends on the quality of fourth-party and nth-party disclosure obtained from third parties, on public-record availability of vendor ownership data, and on the maturity of the organisation's threat intelligence. The register is not a regulatory designation tool; CTPP designation is determined by competent authorities under the applicable regime.

---

**End of Document**
