# Supplier Resilience Monitoring Standard

**Document Title:** Supplier Resilience Monitoring Standard\
**Document Type:** Standard\
**Version:** 1.0.5\
**Date:** 2026-07-05\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/register-concentration-risk.md`](register-concentration-risk.md), [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](procedure-fourth-party-and-nth-party-risk.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md)\
**Classification:** Public\
**Category:** Supply Chain Governance\
**Review Frequency:** Annual and upon material change to the supplier portfolio, signals catalogue, or regulator-expected monitoring posture\
**Repository Path:** [`supply-chain/standard-supplier-resilience-monitoring.md`](standard-supplier-resilience-monitoring.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the resilience signals monitored for critical suppliers, the thresholds that trigger action, the cadence of monitoring, and the escalation path. It complements ongoing supplier monitoring (which focuses on contractual and security compliance) with a specific lens on whether the supplier remains capable of delivering its service.

---

## 2. Scope

This standard applies to all Tier 1 critical suppliers and to Tier 2 high suppliers whose service supports an organization-essential function. Tier 3 and Tier 4 suppliers may be monitored against a subset of signals at the Supplier Risk Maintainer's discretion.

It applies regardless of supplier type: cloud, SaaS, managed services, logistics, hardware, professional services.

---

## 3. Resilience signal taxonomy

Five categories of signal are monitored. Each category contains specific signals; for each signal the standard specifies a source, a cadence, a threshold, and the action triggered.

### 3.1 Continuity testing signals

| Signal | Source | Cadence | Acceptance threshold | Action on breach |
| --- | --- | --- | --- | --- |
| BCP test results disclosed by supplier | Supplier assurance report or attestation | Annual | Test executed within the past 12 months with no material gaps unremediated | Request remediation evidence; escalate to Procurement |
| DR test results disclosed by supplier | Supplier assurance report or attestation | Annual | DR test within the past 12 months with RTO and RPO met | Reassess service criticality; engage with supplier on remediation |
| Tabletop or industry exercise participation | Supplier disclosure | Annual or per regulator | Documented participation in at least one industry-sector exercise where applicable | Note for next contract review |
| Time-since-last-test trend | Supplier disclosure | Quarterly | No degradation in cadence | Engage |

### 3.2 Incident signals

| Signal | Source | Cadence | Acceptance threshold | Action on breach |
| --- | --- | --- | --- | --- |
| Disclosed material incidents in the past 12 months | Supplier; regulator filings; public disclosures | Continuous | Threshold per tier and per criticality | Re-rate supplier risk; reassess continuity |
| Incidents affecting the organization directly | Internal incident register | Per incident | Zero unrecovered impact | Per incident response procedure |
| Sector-peer incident pattern | Threat intelligence | Continuous | No pattern indicating systemic weakness | Engage; consider contractual changes |
| Repeated SLA breaches | Service-level reporting | Monthly | Within contractual tolerance | Service credit; remediation plan |

### 3.3 Financial-health signals

| Signal | Source | Cadence | Acceptance threshold | Action on breach |
| --- | --- | --- | --- | --- |
| Credit rating | Credit reference agency | Quarterly | Above the organization's defined threshold for tier | Engage; activate concentration analysis |
| Going-concern statement | Audited accounts | Annual | Clean opinion | Treat as elevated risk; legal review of exit options |
| Material adverse change notices | Public filings; news | Continuous | None | Investigate; potential exit-strategy activation |
| Days payable outstanding to sub-suppliers (signal of cash strain) | Public data; intelligence | Quarterly | No material increase | Engage |
| Auditor change with qualified opinion | Public filings | Per event | None | Escalate to Finance and Legal |

### 3.4 Control and assurance signals

| Signal | Source | Cadence | Acceptance threshold | Action on breach |
| --- | --- | --- | --- | --- |
| SOC 2 / SOC 1 / ISAE 3402 report currency | Direct from supplier | Annual | Within 12 months | Request updated report |
| Qualified opinions or material exceptions in assurance reports | Direct from supplier | Per report | None unaddressed | Request remediation plan |
| ISO/IEC 27001 certification currency | Public certification register | Annual | Current | Engage; revalidate evidence |
| Penetration test attestation (Tier 1, Tier 2) | Direct from supplier | Annual | Independent test within 12 months | Request updated attestation |
| Independent assessment of the supplier's own supplier programme | Direct or public | Triennial | Available for Tier 1 critical suppliers | Investigate |

### 3.5 External-environment signals

| Signal | Source | Cadence | Acceptance threshold | Action on breach |
| --- | --- | --- | --- | --- |
| Geopolitical risk in supplier operating countries | Threat intelligence; government advisories | Continuous | Stable per the appetite | Activate concentration register update |
| Sanctions or export-control changes affecting supplier | Public registries; legal counsel | Continuous | No sanction on supplier or its ownership chain | Immediate legal review; possible exit |
| Regulatory enforcement against the supplier | Public filings; sector regulator | Continuous | None material | Investigate; reassess supplier |
| Material litigation against the supplier | Public filings | Quarterly | None likely to affect service delivery | Investigate |
| Change of ownership or control | Public filings; supplier notification | Per event | Continuity ensured; no concentration created | Update concentration register; reassess contracts |
| Workforce-action risk (strike, layoff) | Public reporting | Per event | No material impact projected | Engage on contingency |
| Climate or physical risk to supplier sites | Internal mapping | Annual | Within tolerance | Engage on resilience planning |

---

## 4. Monitoring posture by supplier tier

| Tier | Monitoring posture |
| --- | --- |
| Tier 1: Critical | All five signal categories; continuous external-environment monitoring; quarterly review meeting with the supplier; designated SRO with direct supplier relationship |
| Tier 2: High | All five categories on a reduced cadence; semi-annual review meeting; SRO with supplier relationship |
| Tier 3: Moderate | §3.2 and §3.4 at minimum; annual review |
| Tier 4: Low | §3.2 only; ad hoc review |

---

## 5. Operating expectations

1. The Supplier Risk Maintainer publishes a quarterly resilience-signal summary for Tier 1 and Tier 2 suppliers. The summary identifies signals at or above threshold, actions taken, and residual risk.
2. Signal sources are documented per supplier; over-reliance on a single source for a critical signal is itself a finding.
3. Where automation is available (security ratings services, financial-health platforms, threat intelligence feeds), the standard prefers automated monitoring with human review of action triggers.
4. Aggregate monitoring posture is reviewed annually by the Executive Sponsor as part of the supplier risk programme report.
5. The standard is integrated with the supplier exit procedure; signals that breach materially and durably are an input to the exit decision.

---

## 6. Coordination with adjacent standards

| Source | Coordination point |
| --- | --- |
| Supplier security and privacy assurance standard | Defines the contractual requirements that monitoring verifies |
| Supplier ongoing monitoring procedure | Operational workflow for evidence collection |
| Concentration risk register | Resilience signals feed concentration analysis |
| Fourth-party and nth-party risk procedure | Sub-tier signals feed third-party resilience signals |
| Cross-domain incident coordination procedure | Confirmed supplier resilience events route to incident coordination |
| Critical ICT third-party regime (DORA) | Designated CTPP monitoring informed by Oversight Framework outputs |

---

## 7. Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Tier 1 signal coverage | Percentage of Tier 1 suppliers with all five signal categories actively monitored | 100% |
| Signal-source diversity for Tier 1 | Average number of independent sources per Tier 1 signal | At least two |
| Action SLA on threshold breach | Percentage of threshold breaches with documented action initiated within 10 business days | At least 95% |
| Resilience-driven exits | Count of supplier exits initiated wholly or partly by resilience-signal degradation | Trend-monitored |
| Forecasting accuracy | Percentage of supplier resilience events foreshadowed by at least one prior threshold breach | At least 70%; lower indicates poor signal selection |

---

## 8. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| DORA | Articles 28, 30, 33 to 34 (monitoring, contractual provisions, risk assessments) | EU financial services |
| EBA Guidelines on outsourcing arrangements | EBA/GL/2019/02 §82 to 95 | Banking monitoring |
| NIST SP 800-161 Rev. 1 | Cybersecurity Supply Chain Risk Management | US baseline |
| ISO 28000 | Security management for supply chains | International |
| ISO/IEC 27036 | Information security for supplier relationships | Supplier monitoring |
| FSB Cyber Lexicon and Third-Party Risk Toolkit | FSB | Financial-sector practice |
| NIST CSF 2.0 | GV.SC | Cross-walk |
| CSA STAR | Continuous monitoring | Cloud supplier monitoring |

---

## 9. Limitations

This standard is a CC BY-SA 4.0 baseline. Effective supplier resilience monitoring depends on signal quality, source independence, and the organization's analytic capacity to interpret signals. The standard does not predict failures; it identifies leading indicators and structures the organizational response. Adopting organizations tune thresholds to their appetite and supplier portfolio.

---

**End of Document**
