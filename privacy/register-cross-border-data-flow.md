# Cross-Border Data Flow Register

**Document Title:** Cross-Border Data Flow Register 
**Document Type:** Register 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Privacy Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/README.md`](README.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md), [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../compliance/policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md) 
**Classification:** Public 
**Category:** Privacy: Cross-Border Transfer 
**Review Frequency:** Updated upon each new or changed transfer; full register review annually and upon material regulatory change 
**Repository Path:** [`privacy/register-cross-border-data-flow.md`](register-cross-border-data-flow.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register documents all cross-border transfers of personal data from the organisation's operating jurisdictions to third countries. It provides the basis for demonstrating compliance with Chapter V of the GDPR, Schedule 21 of the UK GDPR, and equivalent requirements under applicable privacy laws in Canada (PIPEDA/CPPA), Quebec (Law 25), Brazil (LGPD), China (PIPL), and other applicable regimes.

---

## Legal context

Cross-border data transfer restrictions apply when personal data is transmitted, accessed, or stored in a country outside the originating jurisdiction's regulatory protection area. The following regimes require documented transfer mechanisms:

| Regime | Trigger | Transfer Mechanism Options |
|---|---|---|
| **GDPR (EU)** | Transfer outside EEA | Adequacy decision; Standard Contractual Clauses (SCCs 2021); Binding Corporate Rules (BCRs); Derogations (Article 49) |
| **UK GDPR** | Transfer outside UK | UK adequacy regulations; International Data Transfer Agreement (IDTA); UK Addendum to EU SCCs; BCRs; Derogations |
| **PIPEDA / CPPA (Canada)** | Transfer outside Canada | Contractual protection; consent where appropriate |
| **Quebec Law 25** | Transfer outside Quebec | Privacy Impact Assessment (PIA); contractual protection |
| **LGPD (Brazil)** | Transfer outside Brazil | Adequacy decision by ANPD; contractual clauses; BCRs; specific consent; international convention |
| **PIPL (China)** | Transfer outside China | Cyberspace Administration of China (CAC) security assessment; standard contract filed with CAC; personal information protection certification; applicable treaty |

---

## Transfer record schema

### Identification

| Field | Description | Example |
|---|---|---|
| **Transfer ID** | Unique identifier: `TRF-[YYYY]-[NNN]` | `TRF-2026-001` |
| **Transfer Name** | Short descriptive name | HR payroll data to Canadian payroll processor |
| **Status** | Active / Suspended / Terminated | Active |
| **Date Added** | Date transfer was first recorded | |
| **Last Reviewed** | Date of most recent review | |
| **Next Review Date** | Date of next scheduled review | |

### Data details

| Field | Description | Example |
|---|---|---|
| **Data Controller** | Legal entity acting as controller | [Organisation legal entity] |
| **Data Processor / Recipient** | Legal entity receiving the data | [Recipient entity name and jurisdiction] |
| **Relationship Type** | Controller → Processor; Controller → Controller; Processor → Sub-processor | Controller → Processor |
| **Data Categories** | Categories of personal data being transferred | Employee names, salary details, bank account numbers |
| **Special Category Data?** | Yes / No: if Yes, specify | No |
| **Data Subject Categories** | Who the data relates to | Employees; contractors |
| **Approximate Volume** | Estimated number of records transferred | Approx. [X] records per payroll cycle |
| **Transfer Frequency** | How often the transfer occurs | Bi-weekly (payroll processing) |
| **Processing Purpose** | Why the data is being transferred | Payroll processing and remittance |

### Geography

| Field | Description | Example |
|---|---|---|
| **Originating Jurisdiction(s)** | Country/countries from which data originates | Canada (Quebec); United States |
| **Destination Country** | Country receiving the data | United States |
| **Data Residency** | Where data is ultimately stored | Cloud region in destination country (specify provider and region) |
| **Onward Transfer?** | Does the recipient further transfer to other countries? | No |
| **Onward Transfer Countries** | If yes, destination countries | N/A |

### Transfer mechanism

| Field | Description |
|---|---|
| **Primary Transfer Mechanism** | Legal basis for transfer (per table below) |
| **Mechanism Reference** | Document reference for the specific instrument (e.g., SCC execution date; IDTA reference) |
| **Adequacy Status** | If relying on adequacy: confirm adequacy decision remains in force |
| **SCCs / IDTA Version** | If using SCCs or IDTA: version / module used |
| **Transfer Impact Assessment (TIA)** | Completed / Not Required: and date |
| **TIA Reference** | File reference for TIA documentation |
| **UK Assessment** | For UK GDPR: Transfer Risk Assessment (TRA) completed? |
| **PIPL Assessment** | For China PIPL transfers: CAC assessment / standard contract filed? |

### Transfer mechanisms by regime

| Regime | Mechanism | Instrument |
|---|---|---|
| EU GDPR | SCCs | EU Commission Implementing Decision (EU) 2021/914: Module 2 (C→P) or Module 1 (C→C) |
| EU GDPR | BCRs | ICO/DPA-approved BCR document |
| EU GDPR | Adequacy | Current list of adequate countries: verify annually |
| UK GDPR | IDTA | ICO-published International Data Transfer Agreement (version 1.0) |
| UK GDPR | UK Addendum | Addendum to EU SCCs published by ICO (version B1.0) |
| UK GDPR | Adequacy | UK Government adequacy regulations: verify annually |
| Canada PIPEDA | Contractual protection | DPA with contractual privacy obligations |
| Quebec Law 25 | PIA + contract | Completed AFIPD (Privacy Impact Assessment for Cross-Border Transfer) |
| LGPD (Brazil) | SCCs or contractual clauses | ANPD-recognized clauses or ANPD adequacy decision |
| PIPL (China) | Standard Contract | CAC Standard Contract for Cross-Border Transfer of Personal Information (filed) |

### Risk assessment

| Field | Description |
|---|---|
| **Risk Rating** | Low / Medium / High: considering destination country legal framework, recipient type, data sensitivity |
| **Key Risks Identified** | Brief description of main risks (government access risk; recipient jurisdiction assessment) |
| **Mitigating Measures** | Supplementary measures applied (encryption; pseudonymization; access controls; contractual restrictions on government disclosure) |
| **Residual Risk Assessment** | Overall residual risk after mitigating measures |

### Contractual

| Field | Description |
|---|---|
| **DPA / Contract Reference** | Reference to executed Data Processing Agreement |
| **DPA Execution Date** | Date DPA containing transfer clauses was executed |
| **Transfer Clauses Included** | Yes / No |
| **Deletion on Transfer End** | Confirmed in DPA? What obligation? |
| **Breach Notification** | Notification timeline for breach affecting transferred data |

### Regulatory notifications

| Field | Description |
|---|---|
| **Regulatory Registration Required?** | Whether the transfer requires registration with a supervisory authority | 
| **Authority Notified** | Which authority was notified (if required) |
| **Notification Date** | Date of notification |
| **Registration Reference** | Reference number from authority |

---

## Active transfers summary table

*Populate with all active cross-border transfers. Remove sample entries when implementing.*

| TRF ID | Transfer Name | Data Categories | Origin → Destination | Mechanism | Status | Next Review |
|---|---|---|---|---|---|---|
| TRF-2026-001 | Payroll processing | Employee personal and financial data | CA → US | Contractual (PIPEDA); Quebec Law 25 PIA | Active | |
| TRF-2026-002 | HR management system | Employee records | CA, US → Data centre location | Contractual protection; SCCs (EU employees) | Active | |
| TRF-2026-003 | Cloud productivity platform (email, collaboration) | Internal communications; employee contact data | CA, US, EU, UK → Cloud provider regions | EU SCCs; UK IDTA; US adequacy (EU-US DPF) | Active | |
| TRF-2026-004 | Customer data analytics | Shipping and logistics data; business contact data | EU → US | EU SCCs Module 2 | Active | |
| TRF-2026-005 | Security monitoring (SIEM) | Security logs; user activity data | All regions → SIEM hosting location | SCCs; IDTA; contractual protection | Active | |

---

## Register governance

| Obligation | Frequency | Responsible |
|---|---|---|
| Add new transfer upon DPA execution or new processing activity | Within 10 business days | DPO |
| Review all entries for adequacy status currency | Annually | DPO |
| Review all entries following material regulatory change | On change | DPO |
| Update on change in processing scope or recipient | Within 10 business days of change | DPO |
| Verify TIA / TRA currency | Annually for High-risk transfers | DPO |
| Annual full register review | Annual | DPO / Chief Privacy Officer |
| Share with supervisory authority on request | On demand | DPO / Legal |

---

## Connection to related registers

| Related Register | Connection |
|---|---|
| [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md) | Each subprocessor involving cross-border transfer must have an entry in both registers |
| Article 30 Records of Processing Activities | Each transfer must be reflected in the controller's Article 30 record |
| [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) | Applicable transfer regimes flow from the global regulatory applicability analysis |

---

**End of Document**
