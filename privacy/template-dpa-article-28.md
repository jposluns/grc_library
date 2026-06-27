# Data Processing Agreement Template (GDPR Article 28)

**Document Title:** Data Processing Agreement Template (GDPR Article 28)\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-06-27\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/template-joint-controller-arrangement.md`](template-joint-controller-arrangement.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material change to the processing arrangement, the sub-processor chain, or the applicable privacy regime\
**Repository Path:** [`privacy/template-dpa-article-28.md`](template-dpa-article-28.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This template defines the structure of a **data processing agreement (DPA)** sufficient to satisfy the controller-to-processor contract that **GDPR Article 28(3)** requires whenever a controller engages a processor to process personal data on its behalf. It collects, into one populatable instrument, the eight mandatory processor obligations of Article 28(3)(a) to (h) plus the sub-processor conditions of Article 28(2) and (4) and the written-form requirement of Article 28(9). It also accommodates the equivalent processor-contract obligation under UK GDPR Article 28 and the analogous operator or processor obligations under LGPD (Brazil), PIPL (China), and PIPEDA (Canada, accountability for transfers to third parties for processing).

A populated DPA is a binding contractual instrument between a controller and a processor. It must be in writing (including electronic form, per Article 28(9)), signed by authorised representatives of each party, and retained as a legal record per the organisation's retention schedule. The populated agreement is sensitive contractual data and must not be published in this public CC BY-SA 4.0 repository; use this template structurally and store the executed instrument internally.

Before this template existed, the controller-processor obligations were distributed across the privacy policy, the supplier-assurance standard, the sub-processor register, and several procedures (see Related Documents). This template consolidates the Article 28(3) clause set into a single instrument; the related documents remain the home of the surrounding programme controls (supplier due diligence, the sub-processor list, breach-response assistance, retention of the executed DPA).

---

## Scope

This template applies to every processing activity where a **processor processes personal data on behalf of a controller** on the controller's documented instructions (Article 28(1)). It is the controller-processor counterpart of [`privacy/template-joint-controller-arrangement.md`](template-joint-controller-arrangement.md): joint controllership (Article 26) is a different relationship and uses that template, not this one.

Typical scenarios that require a DPA under this template:

- A controller engages a cloud or SaaS provider that stores or processes personal data on the controller's instructions.
- A controller outsources payroll, customer support, analytics, or marketing-fulfilment processing to a service provider.
- A controller engages a managed-service or IT-operations provider with access to systems holding personal data.

Scenarios that are NOT in scope of this template:

- Two or more controllers jointly determining the purposes and means of processing (joint controllership, Article 26); use [`privacy/template-joint-controller-arrangement.md`](template-joint-controller-arrangement.md).
- Two independent controllers exchanging personal data, each determining its own purposes and means (no processor relationship).
- A processor that, contrary to its instructions, determines the purposes and means of processing: under Article 28(10) that party is treated as a controller for that processing and a DPA is not the correct instrument.

When in doubt whether a counterparty is a processor or an independent or joint controller, conduct a controller-or-processor assessment before executing this template; the EDPB Guidelines 07/2020 on the concepts of controller and processor provide the methodology.

---

## Field set

A populated DPA carries the processing particulars (Section 1) and one binding clause for each Article 28 obligation (Sections 2 to 11). Adopters populate the Example or Value column for each field; the Requirement column states the Article 28 obligation the clause satisfies and must not be weakened below the statutory minimum.

### Section 1: Parties and processing particulars (Article 28(3) chapeau)

Article 28(3) requires the contract to set out the subject-matter and duration of the processing, the nature and purpose of the processing, the type of personal data, the categories of data subjects, and the obligations and rights of the controller.

| Field | Description |
| --- | --- |
| Controller | Legal name, registered address, and authorised contact of the controller. |
| Processor | Legal name, registered address, and authorised contact of the processor. |
| Subject-matter of the processing | What the processing is for, in one sentence. |
| Duration of the processing | The term, tied to the underlying service agreement and the retention obligation in Section 8. |
| Nature and purpose of the processing | The operations performed (for example storage, hosting, support, analytics) and the controller's purpose. |
| Type of personal data | The categories of personal data processed; flag any special-category data (Article 9) or criminal-offence data (Article 10). |
| Categories of data subjects | Whose personal data is processed (for example customers, employees, end users). |
| Obligations and rights of the controller | Cross-reference to the controller's instruction-giving right (Section 2) and audit right (Section 9). |

### Section 2: Processing on documented instructions (Article 28(3)(a))

| Field | Requirement |
| --- | --- |
| Documented-instructions clause | The processor processes the personal data only on the controller's documented instructions, including for any transfer to a third country or international organisation, unless required to process by Union or Member State law. |
| Legal-requirement notification | Where law compels processing beyond the instructions, the processor informs the controller of that legal requirement before processing, unless the law prohibits such notification on important grounds of public interest. |
| Record of instructions | Where the controller records its instructions (the engagement contract, the configured service scope, this DPA's annexes). |

### Section 3: Confidentiality (Article 28(3)(b))

| Field | Requirement |
| --- | --- |
| Confidentiality commitment | The processor requires that persons authorised to process the personal data have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality. |

### Section 4: Security of processing (Article 28(3)(c), Article 32)

| Field | Requirement |
| --- | --- |
| Technical and organisational measures | The processor takes all measures required under Article 32 (appropriate technical and organisational measures to provide a level of security appropriate to the risk). |
| Measures reference | Where the agreed measures are specified (a security annex, the processor's certifications, the controller's security requirements). |

### Section 5: Sub-processors (Article 28(2), Article 28(3)(d), Article 28(4))

| Field | Requirement |
| --- | --- |
| Sub-processor authorisation | The processor does not engage another processor without the controller's prior specific or general written authorisation (Article 28(2)). |
| Change notification | Under a general authorisation, the processor informs the controller of intended additions or replacements of sub-processors, giving the controller the opportunity to object. |
| Sub-processor list | A reference to the maintained list of authorised sub-processors; use [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md). |
| Flow-down of obligations | The same data-protection obligations as in this DPA are imposed on each sub-processor by contract (Article 28(4)); the initial processor remains fully liable to the controller for a sub-processor's failure. |

### Section 6: Assistance with data-subject rights (Article 28(3)(e))

| Field | Requirement |
| --- | --- |
| Data-subject-rights assistance | Taking into account the nature of the processing, the processor assists the controller by appropriate technical and organisational measures, insofar as possible, in responding to requests to exercise the data subject's rights under Chapter III. |
| Procedure reference | The controller fulfils requests using [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md); the DPA records how the processor supports each request type. |

### Section 7: Assistance with controller obligations (Article 28(3)(f), Articles 32 to 36)

| Field | Requirement |
| --- | --- |
| Security, breach, and assessment assistance | The processor assists the controller in ensuring compliance with Articles 32 to 36 (security of processing, personal-data-breach notification to the authority and to data subjects, data protection impact assessment, and prior consultation), taking into account the nature of processing and the information available to the processor. |
| Breach-notification timing | The processor notifies the controller without undue delay after becoming aware of a personal-data breach, on a clock tight enough to let the controller meet its own Article 33 deadline; coordinate with [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md). |

### Section 8: Deletion or return at the end of processing (Article 28(3)(g))

| Field | Requirement |
| --- | --- |
| Deletion-or-return clause | At the controller's choice, the processor deletes or returns all the personal data after the end of the provision of the services, and deletes existing copies, unless Union or Member State law requires storage. |
| Controller's choice | Whether the controller has elected deletion or return, and the format and timing of any return. |
| Retention of the executed DPA | The executed agreement itself is retained per [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md) (term plus the scheduled period), distinct from deletion of the processed data. |

### Section 9: Audits and inspections (Article 28(3)(h))

| Field | Requirement |
| --- | --- |
| Information for compliance | The processor makes available to the controller all information necessary to demonstrate compliance with Article 28. |
| Audit and inspection right | The processor allows for and contributes to audits, including inspections, conducted by the controller or another auditor mandated by the controller. |
| Audit mechanism | How the audit right is exercised (third-party audit reports, certifications, on-site inspection rights, notice periods). |

### Section 10: Duty to flag infringing instructions (Article 28(3), second subparagraph)

| Field | Requirement |
| --- | --- |
| Infringing-instruction notice | The processor immediately informs the controller if, in its opinion, an instruction infringes the GDPR or other Union or Member State data-protection provisions. |

### Section 11: Form and signature (Article 28(9))

| Field | Requirement |
| --- | --- |
| Written form | The agreement is in writing, including electronic form. |
| Authorised signatures | Signed by authorised representatives of the controller and the processor; record the signatory, role, and date for each party. |
| Standard contractual clauses | Where the parties rely on Commission or supervisory-authority standard contractual clauses to form the contract in whole or part (Article 28(6) to (8)), record the SCC set and version used. |

---

## Use guidance

Adopters populate this template before the processor begins processing. The completed DPA is signed by authorised representatives of both parties and retained per Section 8.

The sub-processor list referenced in Section 5 is maintained separately in [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md); the processor-view record of processing required by Article 30(2) is maintained using [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md). Supplier-side due diligence on the processor's Article 28(1) sufficient guarantees is performed under [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md).

A populated DPA is sensitive contractual data. Adopters do NOT publish the populated agreement in this repository or any equivalent public repository.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 28 (esp. 28(2), 28(3)(a) to (h), 28(4), 28(9)) | The controller-to-processor contract and its eight mandatory clauses. |
| UK GDPR | Article 28 | Equivalent processor-contract obligation. |
| LGPD (Brazil) | Articles 39, 42 | Operator obligations and joint or several liability for processing on the controller's behalf. |
| PIPL (China) | Article 21 | Entrusted-processing agreement obligations. |
| PIPEDA (Canada) | Principle 4.1.3 | Accountability for personal information transferred to a third party for processing. |
| ISO/IEC 27001:2022 | A.5.20 (information security in supplier agreements), A.5.19 to A.5.22 (supplier relationships), A.5.34 (privacy and protection of PII) | The DPA as a security-bearing supplier agreement. |
| ISO/IEC 27701:2025 | PII-processor controls | Privacy information management for the processor role. |
| CSA CCM v4.1 | DSP-13 (Personal Data Sub-processing), DSP-14 (Disclosure of Data Sub-processors), DSP-02 (Secure Disposal), DSP-01 (Security and Privacy Policy and Procedures) | Sub-processor governance, end-of-processing deletion, and the privacy-procedure basis. |
| NIST CSF 2.0 | GV.SC (Cybersecurity Supply Chain Risk Management), PR.DS (Data Security), GV.OC (Organizational Context) | The processor as a supply-chain dependency and the security of the data it processes. |

---

## Limitations

This template is the controller-to-processor instrument only. It does not cover joint controllership (use [`privacy/template-joint-controller-arrangement.md`](template-joint-controller-arrangement.md)), controller-to-controller transfers, or the cross-border transfer mechanism itself (use [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md) and the standard contractual clauses or other Chapter V mechanism). It states the statutory minimum of Article 28; an adopter's executed DPA may add commercial terms (liability caps, insurance, service levels) that are outside the scope of this template. The cross-regime references in the framework-alignment table are signposts to the equivalent obligation in each regime, not a substitute for a jurisdiction-specific legal review of the executed agreement.

**End of Document**
