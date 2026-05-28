# Supplier Risk Register Template

**Document Title:** Supplier Risk Register Template 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-onboarding-security-review.md`](procedure-supplier-onboarding-security-review.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`risk/template-enterprise-risk-register.md`](../risk/template-enterprise-risk-register.md) 
**Classification:** Public 
**Category:** Supply Chain Governance: Risk Register 
**Review Frequency:** Quarterly review of active entries; annual template review 
**Repository Path:** [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This template defines the schema for the organisation's Supplier Risk Register: the operational record of all active supplier relationships, their risk classifications, assurance status, monitoring history, and contract details. It serves as the single source of truth for supplier governance and feeds into the enterprise risk register for Tier 1 and High-rated Tier 2 risks.

---

## Supplier record schema

### Part a: supplier identification

| Field | Description | Example |
|---|---|---|
| **Supplier ID** | Unique identifier: `SUP-[YYYY]-[NNN]` | `SUP-2026-001` |
| **Supplier Name** | Legal name of the supplier entity | [Supplier Legal Name] |
| **Supplier Type** | Logistics / Technology / Cloud / Managed Service / Professional Services / Data Processor / Trade Compliance / Other | Logistics |
| **Primary Contact** | Supplier-side primary contact (role title, not name) | Account Manager |
| **Organisation Contact** | Internal contract owner (role title) | Head of Procurement |
| **Onboarding Date** | Date relationship was approved and onboarded | |
| **Last Review Date** | Date of most recent risk review | |
| **Status** | Active / Under Review / Exiting / Exited | Active |

### Part b: services and scope

| Field | Description |
|---|---|
| **Services Provided** | Description of services delivered |
| **Geographic Scope** | Countries and regions where services are delivered |
| **Data Access Scope** | Categories of organisation data the supplier can access (if any) |
| **System Integration** | Specific systems or platforms to which the supplier has access |
| **Personal Data Processing** | Yes / No: if Yes, link to DPA and subprocessor register entry |
| **Trade Compliance Relevance** | Yes / No: if Yes, specify programme(s): CTPAT / AEO-S / PIP / BASC / Other |

### Part c: risk classification

| Field | Scale / Options | Value |
|---|---|---|
| **Tier Classification** | Tier 1, Critical / Tier 2, High / Tier 3: Moderate / Tier 4: Low | |
| **Classification Rationale** | Why this tier was assigned | |
| **Last Tier Review Date** | Date tier was last confirmed or revised | |
| **Inherent Risk Score** | 1 to 25 (Likelihood × Impact from [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md)) | |
| **Residual Risk Score** | 1 to 25 after controls | |
| **Residual Risk Rating** | Low / Medium / High / Critical | |
| **Within Risk Appetite?** | Yes / No / Borderline | |

### Part d: assurance and compliance

| Field | Description | Current Status |
|---|---|---|
| **Security Questionnaire** | Last completed questionnaire and date | |
| **Certification / Audit** | ISO 27001 certificate; SOC 2 report; other (type and expiry) | |
| **Penetration Test** | Date of most recent penetration test; finding summary | |
| **Trade Programme Membership** | CTPAT: Active/Expired | |
| | AEO-S: Active/Expired | |
| | PIP: Active/Expired | |
| | BASC: Active/Expired | |
| | NEEC: Active/Expired | |
| | OEA: Active/Expired | |
| **Financial Health** | Last financial health check; rating | |
| **Data Processing Agreement** | Executed / Not Required; date executed | |
| **Sub-Contractor Disclosure** | Date of last sub-contractor list; number of material sub-contractors | |

### Part e: contract details

| Field | Description |
|---|---|
| **Contract Reference** | Contract ID or file reference |
| **Contract Start Date** | Effective date |
| **Contract End / Renewal Date** | Expiry or next renewal date |
| **Termination Notice Period** | Days notice required |
| **Auto-Renewal** | Yes / No |
| **Key SLAs** | Summary of material service level commitments |
| **Incident Notification Obligation** | Timeline stated in contract (hours) |
| **Audit Rights** | Direct / Report-only / None |
| **Data Return Obligation** | Format and timeline for data return on exit |
| **Deletion Obligation** | Format and timeline for secure deletion on exit |

### Part f: monitoring log

Each monitoring activity must be recorded as a log entry:

| Date | Activity Type | Findings Summary | Risk Score Change | Actions Required | Action Owner | Target Date | Status |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Activity types:** Questionnaire review; Certification review; Financial check; Trade compliance verification; SLA review; Access review; Incident review; Unscheduled triggered review; Full reassessment

### Part g: issues and corrective actions

| Issue ID | Date Identified | Issue Description | Severity | CAPA Reference | Status | Resolved Date |
|---|---|---|---|---|---|---|
| | | | | | | |

### Part h: relationship history

| Event | Date | Description |
|---|---|---|
| Onboarding approved | | |
| Tier escalation / de-escalation | | |
| Contract renewal | | |
| Incident or breach | | |
| Trade compliance status change | | |
| Exit initiated | | |
| Exit completed | | |

---

## Risk score reference

| Score | Rating | Monitoring Frequency (Tier 1) |
|---|---|---|
| 1 to 4 | Low | Annual |
| 5 to 9 | Medium | Semi-annual |
| 10 to 16 | High | Quarterly |
| 17 to 25 | Critical | Monthly + immediate escalation |

For detailed scoring criteria see [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md).

---

## Register governance

| Obligation | Frequency | Responsible |
|---|---|---|
| New supplier entry following onboarding | Within 2 business days of approval | Supplier Risk Manager |
| Quarterly status update for all Tier 1 and Tier 2 suppliers | Quarterly | Supplier Risk Manager |
| Annual full register review | Annual | Supplier Risk Manager / CRO |
| Update following monitoring activity | Within 5 business days of activity | Supplier Risk Manager |
| Update following supplier incident | Within 24 hours | Supplier Risk Manager |
| Escalation of Critical-rated suppliers to enterprise risk register | At identification | Supplier Risk Manager → CRO |

---

## Sample entries

| Supplier ID | Type | Tier | Residual Risk | Trade Compliance | Status |
|---|---|---|---|---|---|
| SUP-2026-001 | Logistics: primary freight forwarder | Tier 1 | High (12) | CTPAT Active; AEO-S Active; PIP Active | Active |
| SUP-2026-002 | Cloud infrastructure provider | Tier 1 | Medium (8) | Not applicable | Active |
| SUP-2026-003 | Customs broker | Tier 2 | Medium (6) | AEO-S Active | Active |
| SUP-2026-004 | HR management system | Tier 1 | Medium (9) | Not applicable | Active |
| SUP-2026-005 | Office supplies | Tier 4 | Low (2) | Not applicable | Active |

---

**End of Document**
