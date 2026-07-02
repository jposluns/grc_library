# Key Risk Indicator Catalogue

**Document Title:** Key Risk Indicator Catalogue\
**Document Type:** Register\
**Version:** 1.1.1\
**Date:** 2026-07-02\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Risk Management: Monitoring\
**Review Frequency:** Annual and upon material change to risk landscape or strategic objectives\
**Repository Path:** [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This catalogue defines Key Risk Indicators (KRIs) for monitoring enterprise risk across all risk categories. KRIs provide early warning signals that a risk is increasing or that an existing control is degrading. They supplement reactive incident reporting with proactive threshold monitoring.

---

## KRI schema

Each KRI is defined by the following fields.

| Field | Description |
|---|---|
| **KRI ID** | Unique identifier: `KRI-[CATEGORY]-[NNN]` |
| **KRI Name** | Short descriptive name |
| **Risk Category** | Enterprise risk category this KRI monitors |
| **Risk Register Link** | Risk ID(s) in [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md) that this KRI tracks |
| **Indicator Description** | What is being measured |
| **Measurement Unit** | How the metric is expressed (%, count, days, score, etc.) |
| **Data Source** | System or report providing the metric |
| **Collection Frequency** | How often the metric is collected |
| **Green Threshold** | Value range indicating risk is within appetite |
| **Amber Threshold** | Value range indicating elevated risk; increased monitoring required |
| **Red Threshold** | Value indicating risk exceeds tolerance; immediate action required |
| **KRI Owner** | Role responsible for collecting and reporting this KRI |
| **Reporting To** | Risk Committee; CRO; Board |
| **Red-Threshold Escalation Owner** | Role with decision authority when the Red threshold is breached: decides the response (add or update risk register entry; commission an investigation; invoke a control intervention; escalate further). Must be a single named role per KRI. Default for cybersecurity KRIs is the CISO; for compliance KRIs the CCO; for operational KRIs the Risk Committee. Adopters substitute their organization's escalation hierarchy. |
| **Red-Threshold Evidence Class** | The evidence captured when the Red threshold is breached: typically (a) timestamp of breach; (b) value at breach time and value trajectory leading into the breach; (c) the named escalation owner's decision and rationale; (d) link to risk register entry created or updated; (e) link to any incident, exception, or control intervention triggered. Retained per the records-retention schedule. |

---

## Cybersecurity kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-CYB-001 | Unpatched Critical Vulnerabilities | Count of critical-severity vulnerabilities unpatched beyond defined SLA | Count | 0 | 1 to 5 | >5 | CISO | Weekly |
| KRI-CYB-002 | Mean Time to Detect (MTTD) | Average time from incident start to detection | Hours | <4 | 4 to 24 | >24 | CISO | Monthly |
| KRI-CYB-003 | Mean Time to Respond (MTTR) | Average time from detection to containment | Hours | <8 | 8 to 48 | >48 | CISO | Monthly |
| KRI-CYB-004 | Phishing Click Rate | Percentage of staff clicking simulated phishing emails | % | <5% | 5 to 15% | >15% | CISO | Quarterly |
| KRI-CYB-005 | Privileged Account MFA Coverage | Percentage of privileged accounts with MFA enforced | % | 100% | 95 to 99% | <95% | CISO | Monthly |
| KRI-CYB-006 | Security Training Completion | Percentage of staff completing annual security awareness training | % | >95% | 85 to 95% | <85% | CISO / HR | Quarterly |
| KRI-CYB-007 | Endpoint Protection Coverage | Percentage of managed endpoints with active protection | % | >99% | 95 to 99% | <95% | IT Operations | Weekly |
| KRI-CYB-008 | Security Incidents (P1+P2) | Count of P1 and P2 security incidents in the period | Count | 0 | 1 to 2 | >2 | CISO | Monthly |

---

## Privacy kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-PRV-001 | Data Subject Requests Overdue | Count of DSARs not responded to within statutory deadline | Count | 0 | 1 to 2 | >2 | Data Protection Officer | Weekly |
| KRI-PRV-002 | Privacy Impact Assessments Outstanding | Count of processing activities requiring DPIA without completed DPIA | Count | 0 | 1 to 3 | >3 | Data Protection Officer | Monthly |
| KRI-PRV-003 | Personal Data Breach Notifications | Count of breaches requiring regulatory notification in the period | Count | 0 | 1 | >1 | Data Protection Officer | Monthly |
| KRI-PRV-004 | Consent Withdrawal Rate | Percentage of individuals withdrawing consent for marketing or analytics | % | <5% | 5 to 15% | >15% | Data Protection Officer | Quarterly |
| KRI-PRV-005 | Cross-Border Transfer Compliance | Count of cross-border data transfers without valid transfer mechanism | Count | 0 | 1 to 2 | >2 | Data Protection Officer | Quarterly |

---

## Supplier and third-party kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-SUP-001 | Critical Supplier Incidents | Count of P1/P2 incidents involving Tier 1 suppliers | Count | 0 | 1 to 2 | >2 | Chief Risk Officer | Monthly |
| KRI-SUP-002 | Overdue Supplier Risk Reviews | Count of Tier 1 suppliers with overdue risk review | Count | 0 | 1 to 2 | >2 | Supplier Risk Manager | Monthly |
| KRI-SUP-003 | Trade Compliance Programme Status | Count of Tier 1 logistics suppliers whose CTPAT/AEO-S/PIP/BASC certification has lapsed | Count | 0 | 1 | >1 | Trade Compliance Manager | Quarterly |
| KRI-SUP-004 | Supplier Financial Distress Signals | Count of Tier 1 suppliers with credit rating downgrade or financial distress alert | Count | 0 | 1 to 2 | >2 | Chief Risk Officer | Monthly |
| KRI-SUP-005 | Concentration: Top Supplier Revenue | Percentage of freight operations dependent on single largest supplier | % | <25% | 25 to 40% | >40% | Chief Risk Officer | Quarterly |

---

## Resilience kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-RES-001 | Business Continuity Plan Test Results | Pass rate in most recent BCP test | % | >90% | 70 to 90% | <70% | Resilience Manager | Semi-annually |
| KRI-RES-002 | Recovery Time Objective Achievement | Percentage of Tier 1 systems meeting RTO in DR test | % | 100% | 80 to 99% | <80% | IT Operations | Semi-annually |
| KRI-RES-003 | Backup Validation Success Rate | Percentage of backup restorations successfully validated | % | >99% | 95 to 99% | <95% | IT Operations | Monthly |
| KRI-RES-004 | Crisis Response Training Currency | Percentage of crisis team members with training current (within 12 months) | % | 100% | 80 to 99% | <80% | Resilience Manager | Quarterly |

---

## Legal and regulatory kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-REG-001 | Regulatory Compliance Obligations Overdue | Count of compliance obligations with overdue action items | Count | 0 | 1 to 3 | >3 | Chief Compliance Officer | Monthly |
| KRI-REG-002 | Internal Audit Findings Overdue | Count of High-rated audit findings with overdue remediation | Count | 0 | 1 to 2 | >2 | Chief Compliance Officer | Monthly |
| KRI-REG-003 | Trade Compliance Violations | Count of customs or trade compliance violations in the period | Count | 0 | 1 | >1 | Trade Compliance Manager | Quarterly |
| KRI-REG-004 | CAPA Overdue Rate | Percentage of open CAPAs past target completion date | % | <10% | 10 to 25% | >25% | Chief Compliance Officer | Monthly |
| KRI-REG-005 | Regulatory Enquiries | Count of active regulatory investigations or enquiries | Count | 0 | 1 | >1 | General Counsel | Monthly |

---

## AI kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-AI-001 | AI Systems Missing Risk Assessment | Count of deployed AI systems without completed risk assessment | Count | 0 | 1 to 2 | >2 | AI Governance Lead | Quarterly |
| KRI-AI-002 | AI Model Performance Drift | Count of AI systems with performance metrics outside acceptable thresholds | Count | 0 | 1 to 2 | >2 | AI Operations | Monthly |
| KRI-AI-003 | AI Bias Alerts | Count of AI systems with active bias finding from fairness monitoring | Count | 0 | 1 | >1 | AI Governance Lead | Monthly |
| KRI-AI-004 | Unreviewed High-Risk AI Deployments | Count of Tier 2 (high-risk) AI systems not reviewed by AIGC within 12 months | Count | 0 | 1 | >1 | AI Governance Lead | Quarterly |

---

## Operational kris

| KRI ID | KRI Name | Indicator | Unit | Green | Amber | Red | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|
| KRI-OPS-001 | Critical System Availability | Uptime of Tier 1 systems in the period | % | >99.9% | 99 to 99.9% | <99% | IT Operations | Monthly |
| KRI-OPS-002 | Change-Related Incidents | Percentage of changes resulting in unplanned incidents | % | <5% | 5 to 15% | >15% | IT Operations | Monthly |
| KRI-OPS-003 | Open P1/P2 Incidents | Count of P1/P2 incidents unresolved beyond SLA | Count | 0 | 1 to 2 | >2 | IT Operations | Weekly |

---

## KRI reporting and escalation

| Threshold Breached | Required Action | Timeframe |
|---|---|---|
| **Red** | Immediate notification to KRI owner and CRO; initiate investigation; add or update risk register entry | Within 24 hours |
| **Amber** | KRI owner to investigate and report root cause; increase monitoring frequency | Within 5 business days |
| **Green** | No action required; include in standard risk reporting | Per reporting cycle |

### Reporting cadence

| Report | Frequency | Audience |
|---|---|---|
| KRI Dashboard | Monthly | Chief Risk Officer; CISO; DPO |
| KRI Trends Summary | Quarterly | Risk Committee; executive leadership |
| Red KRI Escalation Report | As triggered | Board; relevant executive |
| Annual KRI Review | Annual | Board / Risk Committee |

---

**End of Document**
