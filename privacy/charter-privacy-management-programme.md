# Privacy Management Programme Charter

**Document Title:** Privacy Management Programme Charter\
**Document Type:** Charter\
**Version:** 1.5.3\
**Date:** 2026-07-02\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This charter establishes the Privacy Management Programme: the organizational structure, accountabilities, and operating principles governing how personal data is collected, used, stored, disclosed, and disposed of across all jurisdictions. It creates the overarching framework within which the Privacy and Data Governance Policy, the Privacy Impact and Cross-Border Transfer Procedure, and the Data Subject Rights Management Procedure operate. The programme aligns to ISO/IEC 27701:2025, which is now a standalone Privacy Information Management System (PIMS) standard (the 2019 edition was an extension to ISO/IEC 27001; the 2025 revision restructured ISO/IEC 27701 as an independent standard; transition deadline October 2028).

---

## Scope

1. Applies to all personal data processed by the organization, including employee data, customer data, supplier data, and partner data.
2. Applies across all jurisdictions: Canada (PIPEDA and provincial legislation including Quebec Law 25), United States (applicable state breach notification and privacy laws), Latin America (applicable national privacy laws in jurisdictions where the organization operates), and United Kingdom (UK GDPR / Data Protection Act 2018).
3. Applies to all employees, contractors, and third parties who process personal data on behalf of the organization.

---

## Privacy accountability structure

The following roles hold defined accountability within the Privacy Management Programme:

| Role | Accountability |
|---|---|
| **Chief Information Officer (CIO)** | Executive accountability for the privacy programme. Signs off on material privacy risk decisions. |
| **Data Protection Officer (DPO)** | Operational ownership of the privacy programme. Manages regulatory obligations, data subject requests, PIA oversight, and cross-border transfer assessment. |
| **Chief Information Security Officer (CISO)** | Accountable for information security controls that protect personal data. Joint responsibility with the Data Protection Officer for data breach response. |
| **Legal Counsel** | Advises on regulatory notification obligations; manages regulatory relationships; reviews Data Processing Agreement (DPA) documentation. |
| **Human Resources** | Manages employee personal data; ensures that HR data processing complies with applicable employment privacy law. |

> **Interim Accountability:** Where a formal Data Protection Officer (DPO) has not yet been designated, the CIO assumes these responsibilities as interim accountability. See the DPO independence and conflict-of-interest section below for the constraints the interim arrangement creates and the mitigations adopters must apply.

### DPO independence and conflict of interest (GDPR Articles 38(3) and 38(6))

GDPR Article 38 imposes two structural protections on the DPO role that adopters must preserve regardless of the formal-or-interim designation status:

**Article 38(3) independence requirements.** The controller and processor must ensure that the DPO:

| Requirement | Source | What it forbids in practice |
|---|---|---|
| Does not receive any instructions regarding the exercise of DPO tasks | Article 38(3) sentence 1 | Management cannot direct the DPO's privacy assessments, regulator-engagement positions, or breach-notification decisions on a case-by-case basis |
| Cannot be dismissed or penalized for performing DPO tasks | Article 38(3) sentence 2 | Dismissal, demotion, salary reduction, or denial of training cannot be linked to DPO advice the management disliked |
| Reports directly to the highest management level | Article 38(3) sentence 3 | The DPO must have an unfiltered escalation path; intermediary management layers cannot gate DPO communications to the board or executive |

**Article 38(6) conflict-of-interest constraint.** The DPO may fulfil other tasks and duties, but the controller / processor must ensure that any such tasks and duties do not result in a conflict of interests. The Article 29 Working Party Guidelines on DPOs (WP243 rev.01) and the EDPB's subsequent guidance identify the following positions as **typically incompatible** with the DPO role:

- Chief Executive Officer
- Chief Operating Officer
- Chief Financial Officer
- Chief Information Officer
- Chief Information Security Officer (where the CISO determines purposes and means of security processing)
- Head of Marketing
- Head of Human Resources
- Head of IT operations or processing department
- Any role that determines purposes and means of processing personal data
- Any role that audits or sanctions the DPO

This list is not exhaustive; the test is whether the secondary role results in the DPO determining (in whole or part) the purposes and means of the processing the DPO is supposed to oversee.

**Interim CIO-as-DPO arrangement: known conflict.** The interim accountability note above explicitly creates an Article 38(6) conflict: the CIO determines purposes and means of IT processing AND advises on its privacy compliance. The library makes this conflict visible rather than silent. Adopters must either:

1. **Designate a formal DPO** (the preferred path; the formal designation triggers Article 37-39 protections and resolves the Article 38(6) conflict);
2. **Implement mitigation controls** while the interim arrangement persists, naming each control to the supervisory authority in any DPIA, ROPA, or Article 36 prior consultation; OR
3. **Document the formal exemption analysis** if Article 37(1) thresholds are not met (most organizations operating at any non-trivial scale will not qualify for exemption).

**Mitigation controls for the interim arrangement** (operational only, not a substitute for formal designation):

| Control | Purpose |
|---|---|
| Independent privacy-decision escalation path: the acting DPO's privacy advice is reviewed by Legal Counsel and the audit committee before any decision that would be vetoed by IT-operations interests | Mitigates Article 38(3) instruction-on-tasks risk |
| Documented separation of "CIO acting in operations capacity" vs "CIO acting as DPO" in meeting minutes, sign-offs, and supervisory-authority communications | Mitigates Article 38(6) role-blending risk |
| External privacy counsel retained on standing brief for any matter where the CIO's operations interest and DPO advice would diverge | Provides arms-length advice channel |
| Annual independent review of the interim arrangement's effectiveness, with a documented decision to renew or replace the arrangement | Maintains discipline against indefinite reliance on the interim arrangement |
| Public statement in the privacy notice and the Article 30 ROPA that the acting-DPO arrangement is interim | Transparency to data subjects and supervisory authorities |

**Cross-regime independence equivalents.**

| Regime | DPO independence basis | Conflict-of-interest test |
|---|---|---|
| **UK GDPR** (UK) | Article 38(3) (same as EU GDPR) | Article 38(6) (same); ICO guidance mirrors EDPB |
| **LGPD** (Brazil, Article 41) | DPO must have appropriate technical knowledge and act independently; ANPD guidance on conflict |
| **PIPL** (China, Article 52) | Personal information protection officer must have professional knowledge and management experience; CAC Provisions impose function-separation expectations |
| **India DPDP 2023** | Data Protection Officer required for Significant Data Fiduciaries; must be independent; Data Protection Board provides oversight |

For multi-regime non-EU controllers the strictest applicable independence regime governs.

### EU representative (GDPR Article 27)

Where the organization is not established in the European Union but is subject to GDPR by virtue of Article 3(2) (offering goods or services to data subjects in the Union, or monitoring the behaviour of data subjects in the Union), Article 27 requires the designation in writing of an **EU representative**.

**Trigger.** The Article 27 obligation is triggered when **both** of the following are true:

1. The organization is established outside the European Union (and outside the EEA more broadly: Iceland, Liechtenstein, Norway are within the EEA scope of GDPR).
2. The organization processes personal data of subjects in the Union in the context of offering goods or services (irrespective of payment) OR monitoring behaviour that takes place within the Union (Article 3(2)).

**Article 27(2) exemptions.** The obligation does NOT apply where ALL of the following are true:

| Exemption criterion | Description |
|---|---|
| Processing is occasional | Not part of regular activity; ad hoc rather than systematic |
| Excludes Article 9 / Article 10 special categories | No large-scale processing of special-category (Article 9) or criminal-conviction (Article 10) data |
| Unlikely to result in a risk to rights and freedoms | Risk assessment documents this conclusion |
| Public authority or body | Public authorities and bodies are exempt |

The DPO documents the Article 27(2) exemption analysis in the organization's Article 30 ROPA.

**Representative criteria.** The EU representative must:

| Criterion | Source |
|---|---|
| Be established in one of the Member States where the data subjects whose data is processed (in relation to the offering of goods/services or monitoring of behaviour) are located | Article 27(3) |
| Be designated in writing | Article 27(1) |
| Be mandated to be addressed in addition to or instead of the controller/processor by supervisory authorities and data subjects on all issues related to processing | Article 27(4) |
| Have sufficient knowledge of GDPR and the controller's processing activities to act as point of contact | EDPB Guidelines 3/2018 on the territorial scope of GDPR |
| Maintain a copy of the controller's or processor's Article 30 records on Union territory where requested by the supervisory authority | Article 30(4) by extension |

**Designation process.**

1. The DPO assesses Article 3(2) applicability and the Article 27(2) exemption analysis annually and on material change to processing.
2. Where the obligation applies, the DPO identifies a candidate representative in a Member State where the affected data subjects are located.
3. Legal Counsel drafts and executes a written mandate between the organization and the representative covering the Article 27(4) scope (responding to supervisory authorities, responding to data subjects, maintaining the ROPA copy where requested).
4. The CIO signs the designation; the representative countersigns acceptance.
5. The DPO publishes the representative's contact details in the organization's privacy notices (Article 13(1)(a) and Article 14(1)(a)) using [`privacy/template-privacy-notice.md`](template-privacy-notice.md).
6. The representative's contact details are also recorded in the Article 30 ROPA using [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md).
7. The designation is filed with the lead supervisory authority where required by national implementing law (some Member States require notification; some do not).

**Maintenance.** The designation is reviewed:

- **Annually** by the DPO; if the affected data subjects' Member State distribution has changed materially, the representative may need to be re-designated.
- **Upon material change** to the controller's processing activities (new product lines, new monitoring activities, change in EU subject base).
- **Upon the representative's resignation or material change in capacity** (insolvency, loss of registration, change in mandate scope).

**Article 27(5) clarification.** The designation of an EU representative does NOT affect legal actions which could be initiated against the controller or processor themselves. Article 27 creates an additional point of contact, not a liability shield.

**Cross-regime equivalents.**

| Regime | Equivalent | Notable variations |
|---|---|---|
| **UK GDPR** (UK) | UK representative (UK GDPR Article 27) | Required where the controller / processor is outside the UK but subject to UK GDPR; ICO is the supervisory authority |
| **LGPD** (Brazil) | Legal representative (Article 5(VIII)) | Required for non-Brazilian controllers offering services to Brazilian subjects; ANPD is the supervisory authority |
| **PIPL** (China, Article 53) | Designated organization or appointed agent in China | Required for non-Chinese personal-information handlers; must be filed with the Cyberspace Administration of China (CAC) |
| **India DPDP Act 2023** | Local representative where designated as Significant Data Fiduciary | Required at the Significant-Data-Fiduciary designation level; Data Protection Board of India is the supervisory authority |
| **Saudi Arabia PDPL** | Local representative for non-Saudi controllers (subject to executive regulations) | SDAIA is the supervisory authority |

For multi-regime non-EU controllers, the organization may need to designate multiple regional representatives in parallel.

---

## Privacy by design

Privacy considerations must be incorporated into any new system, process, or data collection activity from the design stage. Privacy Impact Assessments (PIAs) are mandatory before any of the following:

- Any new personal data collection activity.
- Any new or changed system processing personal data at scale.
- Any cross-border data transfer.
- Any material change to data retention practices.

---

## Applicable regulatory obligations

| Jurisdiction | Instrument | Key Obligations |
|---|---|---|
| **Canada (Federal)** | PIPEDA: Personal Information Protection and Electronic Documents Act | Consent, purpose limitation, breach notification (material risk of significant harm), accountability. |
| **Quebec (Provincial)** | Law 25: Act Respecting the Protection of Personal Information in the Private Sector (Law Modernizing Privacy) | Designated Data Protection Officer mandatory; privacy impact assessments; 72-hour breach notification to the Commission d'accès à l'information (CAI); data subject rights. |
| **United States** | Applicable state breach notification and sector-specific laws | Breach notification timelines vary by state. Refer to the Global Regulatory Mapping Register for current state-level obligations. |
| **United Kingdom** | UK GDPR / Data Protection Act 2018 | Lawful basis for processing; data subject rights; 72-hour breach notification to the ICO; international transfer mechanisms. |
| **Latin America** | National privacy laws by jurisdiction (including Brazil LGPD and others) | Jurisdiction-specific requirements apply. Refer to the Global Regulatory Mapping Register and Regional Annexes. |

---

## Data breach response

Privacy breaches involving personal data are managed under the Data Protection and Privacy Breach Response Procedure, which includes regulatory notification assessment. The CISO and Data Protection Officer are jointly responsible for initiating breach response. Legal Counsel determines notification obligations by jurisdiction in accordance with the applicable law table above.

---

## Annual review

The Privacy Management Programme is reviewed annually by the Data Protection Officer and CISO. The review assesses:

- Regulatory changes affecting obligations.
- PIA register completeness.
- Data subject request volumes and response times.
- Cross-border transfer mechanism currency.
- Programme gaps identified through audits or incidents.

Results are reported to the CIO and included in the annual GRC programme report to the Enterprise Risk Committee (ERC).

---

## Framework alignment

| Framework | Relevance |
|---|---|
| ISO/IEC 27701:2025 | Privacy Information Management System (PIMS), standalone |
| PIPEDA | Personal Information Protection and Electronic Documents Act (Canada) |
| Quebec Law 25 | Act Respecting the Protection of Personal Information in the Private Sector |
| UK GDPR / Data Protection Act 2018 | United Kingdom data protection law |
| CSA CCM v4.1 Data Security and Privacy Lifecycle Management (DSP) domain | Privacy controls |
| NIST Privacy Framework v1.0 | Privacy risk management |

---

*This document is released under the CC BY-SA 4.0 licence. No rights reserved.*



**End of Document**
