# Subprocessor Register Template

**Document Title:** Subprocessor Register Template\
**Document Type:** Register\
**Version:** 1.0.2\
**Date:** 2026-07-02\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/register-cross-border-data-flow.md`](../privacy/register-cross-border-data-flow.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../compliance/policy-legal-and-regulatory-compliance.md)\
**Classification:** Public\
**Category:** Supply Chain Governance: Data Processing\
**Review Frequency:** Updated upon each new subprocessor engagement or change; full register review annually\
**Repository Path:** [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template defines the schema for the organization's Subprocessor Register. The register records all third-party organizations that process personal data on behalf of the organization as data processors or subprocessors. It supports GDPR Article 28 compliance, enables transparency with data subjects and supervisory authorities, and provides the basis for subprocessor notifications to customers where contractually required.

---

## Legal context

Under GDPR and UK GDPR Article 28, a controller must engage processors only where the processor can provide sufficient guarantees about technical and organizational measures. Where a processor engages a subprocessor, the controller retains responsibility for the subprocessor's compliance. This register enables the organization to:

- Meet its Article 30 Record of Processing Activities obligations with respect to processors
- Discharge notification obligations to customers who have subprocessor notification clauses in their contracts
- Monitor subprocessor changes and assess impact on data protection obligations
- Demonstrate accountability to supervisory authorities on request

---

## Subprocessor record schema

### Identification

| Field | Description | Example |
|---|---|---|
| **Subprocessor ID** | Unique identifier: `SP-[YYYY]-[NNN]` | `SP-2026-001` |
| **Entity Name** | Legal name of the processing entity | [Entity Legal Name] |
| **Parent Organization** | Parent company if entity is a subsidiary | [Parent Legal Name] |
| **Supplier Risk Register ID** | Cross-reference to [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md) | `SUP-2026-004` |
| **Status** | Active / Pending Approval / Terminated | Active |
| **Date Added** | Date subprocessor was approved | |
| **Date Terminated** | Date of termination (if applicable) | |

### Processing details

| Field | Description | Example |
|---|---|---|
| **Processing Purpose** | Specific purpose(s) for which personal data is processed | HR system: employee payroll; time and attendance |
| **Processing Activities** | Specific operations (storage, retrieval, analysis, transmission, deletion) | Storage; retrieval; reporting |
| **Data Categories Processed** | Categories of personal data in scope | Employee names; salaries; national identification numbers; bank account details |
| **Special Category Data?** | Yes / No: if Yes, specify categories | No |
| **Data Subjects** | Who the personal data belongs to | Employees; contractors |
| **Approximate Record Count** | Estimated volume of data subject records | Approx. [X] records |

### Geography

| Field | Description | Example |
|---|---|---|
| **Processing Location(s)** | Country/countries where data is processed and stored | Canada; United States |
| **Data Residency Commitment** | Contractual commitment on data location | Data stored in Canada; US access for support only |
| **Cross-Border Transfer?** | Yes / No | Yes: transfers to US |
| **Transfer Mechanism** | Adequacy / SCCs / IDTA / BCRs / Other | Standard Contractual Clauses (EU SCC 2021) |
| **Transfer Register Reference** | Link to cross-border data flow register entry | [`privacy/register-cross-border-data-flow.md`](../privacy/register-cross-border-data-flow.md) entry TRF-2026-001 |
| **Transfer Impact Assessment** | Completed / Not Required / In Progress | Completed: see TIA-2026-001 |

### Contractual

| Field | Description |
|---|---|
| **Data Processing Agreement** | Reference to executed DPA; date executed |
| **DPA Review Date** | Date DPA was last reviewed; next review date |
| **Sub-Subprocessor Clause** | Does the DPA permit further subprocessing? Under what conditions? |
| **Deletion Obligation** | Data deletion / return requirements at contract end |
| **Notification Obligation** | Supplier notification timeline for breaches affecting this data |
| **Audit Rights** | Direct audit / report sharing / questionnaire |

### Assurance

| Field | Description |
|---|---|
| **Security Certification** | ISO 27001; SOC 2 Type II; other (with expiry date) |
| **Privacy Certification** | ISO 27701; privacy seal or equivalent |
| **Last Security Assessment** | Date and outcome |
| **Known Incidents** | Any prior data incidents involving this subprocessor |

### Customer notification obligations

For subprocessors where customer contracts include subprocessor notification clauses:

| Field | Description |
|---|---|
| **Customer Notification Required?** | Yes / No |
| **Customers to Be Notified** | List customer contract references requiring notification |
| **Notification Lead Time** | Days notice contractually required before engaging new subprocessor |
| **Objection Right** | Can customers object to this subprocessor? |
| **Notification Date** | Date customers were notified (when applicable) |
| **Objections Received** | Any customer objections; resolution |

---

## Sub-subprocessor section

Where a subprocessor engages its own sub-subprocessors that will process the organization's personal data, these must be documented:

| Sub-Subprocessor Name | Relationship | Processing Purpose | Location | Approved? | Date |
|---|---|---|---|---|---|
| | | | | | |

---

## Register governance

| Obligation | Frequency | Responsible |
|---|---|---|
| Add new subprocessor upon approval | Within 5 business days of DPA execution | DPO / Supplier Risk Manager |
| Update on change in processing scope or transfer mechanism | Triggered by change | DPO |
| Customer notification for new subprocessors | Per contract notification lead time | DPO / Legal |
| Annual full register review | Annual | DPO / Supplier Risk Manager |
| Remove terminated subprocessors | Within 10 business days of termination | DPO / Supplier Risk Manager |
| Verify active certifications | Annually | Supplier Risk Manager |

---

## Connection to records of processing activities (article 30)

This register forms the processor annex to the organization's Article 30 Records of Processing Activities. The DPO must ensure that:
- Each subprocessor entry is reflected in the relevant processing activity record in the Article 30 register
- Changes to subprocessors are updated in both registers concurrently

---

## Notification template

Where customer contracts require subprocessor notification, the following minimum information should be communicated:

> **Subject: Notice of New Subprocessor Engagement**
>
> In accordance with our Data Processing Agreement, we are providing [X] days advance notice of our intent to engage the following new subprocessor:
>
> **Entity name:** [Legal name] 
> **Processing purpose:** [Purpose] 
> **Data categories:** [Categories] 
> **Processing location:** [Country/countries] 
> **Transfer mechanism:** [Mechanism, if cross-border] 
> **Effective date:** [Date]
>
> You have the right to object to this engagement within [X] days of this notice. If no objection is received, we will proceed with the engagement as of the stated effective date.

---

**End of Document**
