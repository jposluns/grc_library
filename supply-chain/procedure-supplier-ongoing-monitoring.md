# Supplier Ongoing Monitoring Procedure

**Document Title:** Supplier Ongoing Monitoring Procedure\
**Document Type:** Procedure\
**Version:** 1.0.3\
**Date:** 2026-07-04\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`risk/register-key-risk-indicators.md`](../risk/register-key-risk-indicators.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md)\
**Classification:** Public\
**Category:** Supply Chain Governance: Ongoing Monitoring\
**Review Frequency:** Annual and upon significant monitoring finding or regulatory update\
**Repository Path:** [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the activities, frequencies, and escalation steps for ongoing monitoring of active supplier relationships. Monitoring ensures that supplier risk ratings remain current, contractual obligations are being met, and emerging risks are identified before they cause harm to the organization's operations, data, or compliance posture.

---

## Monitoring principles

- Risk-proportionate: Tier 1 suppliers receive more intensive monitoring than Tier 3 and Tier 4 suppliers
- Evidence-based: monitoring activities produce documented evidence that is retained in the supplier risk register
- Continuous where cost-effective: automated signals (security ratings, financial alerts) supplement periodic reviews
- Trigger-aware: events outside scheduled cycles must initiate unscheduled reviews

---

## Scheduled monitoring activities

### Tier 1: critical suppliers

| Activity | Frequency | Method | Responsible |
|---|---|---|---|
| Security posture update: refresh questionnaire or obtain updated certification/audit report | Quarterly | Questionnaire; request for updated evidence | Supplier Risk Manager |
| Financial health check | Quarterly | Credit rating service; review of public financial indicators | Supplier Risk Manager / Finance |
| SLA and performance review | Monthly | Review SLA reports submitted by supplier; compare against contractual thresholds | Contract Owner |
| Trade compliance programme status verification (CTPAT / AEO-S / PIP / BASC where applicable) | Quarterly | Verify via CBP CTPAT portal; HMRC AEO portal; CBSA PIP directory; BASC registry | Trade Compliance Manager |
| Sub-contractor disclosure review | Semi-annually | Request updated list of material sub-contractors; compare against last-known list | Supplier Risk Manager |
| Incident and vulnerability intelligence review | Monthly | Review public breach disclosures; threat intelligence feeds; security ratings service | Information Security |
| Access review: verify access grants remain appropriate | Quarterly | Review access logs and account inventory | IT Operations |
| Contract compliance review | Quarterly | Verify key contractual obligations are being met; review invoices and reports | Contract Owner |
| Fourth-party risk review | Semi-annually | Review sub-contractor security posture; identify new concentration risks | Supplier Risk Manager |
| Business continuity test invitation | Annually | Invite Tier 1 suppliers to participate in or demonstrate continuity testing | Resilience Manager |
| Full periodic reassessment | Annually | Comprehensive reassessment covering all risk domains (security, privacy, financial, operational, trade compliance) | Supplier Risk Manager |

### Tier 2: high suppliers

| Activity | Frequency | Method | Responsible |
|---|---|---|---|
| Security posture update | Semi-annually | Questionnaire refresh; request updated audit report or certification | Supplier Risk Manager |
| Financial health check | Semi-annually | Credit indicator review | Supplier Risk Manager / Finance |
| SLA and performance review | Quarterly | SLA report review | Contract Owner |
| Trade compliance status | Semi-annually (where applicable) | Portal verification | Trade Compliance Manager |
| Incident intelligence review | Quarterly | Security ratings; breach disclosure monitoring | Information Security |
| Access review | Semi-annually | Access log and account review | IT Operations |
| Contract compliance review | Semi-annually | Key clause verification | Contract Owner |
| Full periodic reassessment | Annually | All domains | Supplier Risk Manager |

### Tier 3: moderate suppliers (where data access exists)

| Activity | Frequency | Method | Responsible |
|---|---|---|---|
| Security questionnaire refresh | Annually | Updated questionnaire | Supplier Risk Manager |
| SLA review | Semi-annually | Performance report | Contract Owner |
| Access review | Annually | Account inventory | IT Operations |
| Full periodic reassessment | Every 2 years (or at contract renewal) | Scoped reassessment | Supplier Risk Manager |

### Tier 4: low suppliers

| Activity | Frequency | Method | Responsible |
|---|---|---|---|
| Contract renewal check | At renewal | Standard procurement review | Procurement |
| No formal security monitoring required | N/A | N/A | N/A |

---

## Continuous monitoring signals

In addition to scheduled activities, the following continuous signals should be monitored where tooling supports it:

| Signal Type | What to Monitor | Action on Alert |
|---|---|---|
| **Security ratings** | External security rating drops materially (e.g., by one grade or 10+ points) | Initiate unscheduled security posture review |
| **Dark web / threat intelligence** | Supplier's credentials or data appear in threat intelligence or breach notifications | Initiate immediate review; assess impact; notify DPO if personal data involved |
| **Financial distress signals** | Credit rating downgrade; county court judgements; news of financial difficulty | Initiate contingency planning review; escalate to CRO |
| **Regulatory sanctions** | Supplier named in regulatory enforcement action | Assess impact on organization; escalate to CCO and CRO |
| **Adverse media** | Significant negative news coverage involving security, privacy, or ethical conduct | Review and assess relevance; escalate if material |
| **Trade compliance alerts** | Supplier loses CTPAT / AEO-S / PIP / BASC certification; enters customs sanctions list | Immediate escalation to Trade Compliance Manager and CRO; assess operational impact |

---

## Trigger-based (unscheduled) reviews

The following events must trigger an immediate unscheduled review regardless of scheduled monitoring cycle:

| Trigger | Required Action | Timeframe |
|---|---|---|
| Supplier discloses a security or data breach | Assess impact; notify DPO; escalate per [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md); update risk register | Within 4 hours of notification |
| Supplier loses trade compliance programme certification | Assess operational and regulatory impact; engage alternatives if Tier 1 logistics supplier | Within 24 hours |
| Supplier is acquired, merged, or changes ownership | Re-initiate onboarding security review for affected scope | Within 30 days of announcement |
| Key security contact or DPO change at supplier | Obtain updated contact details; re-confirm compliance commitments | Within 10 business days |
| Supplier announces material technology change affecting service delivery | Re-assess security and continuity implications | Within 30 days of announcement |
| Contracted security obligation is not met (e.g., late incident notification) | Raise corrective action; document in risk register; escalate if repeated | Within 5 business days |

---

## Reassessment process

When a full periodic reassessment or trigger-based reassessment is required:

1. Re-issue the supplier security questionnaire ([`supply-chain/template-supplier-security-questionnaire.md`](template-supplier-security-questionnaire.md))
2. Request updated assurance evidence (certificates, audit reports, pen test)
3. Conduct a gap analysis against [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md)
4. Update residual risk score in [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md)
5. Re-confirm tier classification: escalate if tier has changed
6. Where personal data processing is in scope, re-confirm DPA adequacy and check for new sub-processors
7. Where trade compliance is relevant, re-confirm programme membership and certification status

---

## Findings and corrective action

| Finding Severity | Definition | Required Action |
|---|---|---|
| **Critical** | Supplier breach, data loss, or loss of trade compliance certification with material operational impact | Immediate escalation to CRO, CISO, CCO; activate contingency plan; consider exit ([`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md)) |
| **High** | Significant control gap or compliance failure; unresolved within contractual deadline | Raise CAPA ([`compliance/procedure-capa.md`](../compliance/procedure-capa.md)); escalate to CRO if not remediated within 30 days |
| **Medium** | Partial gap or performance shortfall; corrective action plan agreed | Issue formal corrective action notice; track in risk register; follow up at next monitoring cycle |
| **Low** | Administrative or documentation gap | Note in risk register; request update at next scheduled review |

---

## Monitoring records

All monitoring activities must be documented in [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md):
- Date of activity
- Type of activity
- Findings summary
- Risk score update (if changed)
- Action items and target dates
- Sign-off by Supplier Risk Manager

---

**End of Document**
