# Legitimate Interest Assessment (LIA) Template

**Document Title:** Legitimate Interest Assessment (LIA) Template\
**Document Type:** Template\
**Version:** 1.0.2\
**Date:** 2026-07-02\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/framework-consent-management.md`](framework-consent-management.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material processing, jurisdiction, or regulatory change\
**Repository Path:** [`privacy/template-legitimate-interest-assessment.md`](template-legitimate-interest-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template is the instrument that records and evidences a **Legitimate Interest Assessment (LIA)**: the documented three-part test an organization completes before relying on the legitimate-interests lawful basis under **GDPR Article 6(1)(f)** (Regulation (EU) 2016/679). Article 6(1)(f) permits processing that is "necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject". Relying on that basis without a recorded assessment leaves the organization unable to demonstrate the accountability that Article 5(2) requires.

The LIA documents the three cumulative conditions the basis demands: a **purpose test** (is there a legitimate interest?), a **necessity test** (is the processing necessary to pursue it?), and a **balancing test** (do the data subject's interests, rights, and freedoms override the interest?). A completed LIA feeds the lawful-basis field of the Record of Processing Activities, the legitimate-interest disclosure in the privacy notice, and, where the processing is high-risk, the DPIA.

A populated LIA is operationally sensitive: complete it as a working document, not as published content.

## Scope

This template applies wherever the organization relies, or proposes to rely, on Article 6(1)(f) (legitimate interests) as the lawful basis for processing personal data. It does not apply where another lawful basis governs (consent, contract, legal obligation, vital interests, or public task); the boundary with consent is covered in [`privacy/framework-consent-management.md`](framework-consent-management.md), and transfer-specific assessment is covered by the transfer-impact assessment, not this template.

**Threshold exclusion.** Article 6(1)(f) does not apply to processing carried out by public authorities in the performance of their tasks (Article 6(1)(f), second subparagraph). A public-authority adopter must confirm, as a threshold question, that the processing falls outside its public-task functions before using this basis.

The assessment is completed at the outset of the processing, with the DPO involved, and is retained as part of the organization's accountability record under Article 5(2).

## How to use this template

1. Complete **Section 1** to identify the processing precisely.
2. Work the three parts of **Section 2** in order: the purpose test (2.1), the necessity test (2.2), and the balancing test (2.3). Each part must pass; the conditions are cumulative.
3. Record the overall outcome and the committed safeguards in **Section 3**.
4. Record the LIA reference in the corresponding Record of Processing Activities entry, and reflect the legitimate interest pursued in the privacy notice (Articles 13 and 14).
5. Re-run the assessment on the triggers in **Section 4**.

Fill the right-hand cells of each table. A field left blank is an incomplete assessment, not a passed one.

## Section 1. Identification of the processing

| Field | Required content |
| --- | --- |
| Processing operation name and identifier | Stable identifier, cross-referenced from the Record of Processing Activities. |
| Controller (and any joint controller) | The legal entity or entities determining the purposes and means. |
| Third party relying on the interest (if any) | Where the legitimate interest is pursued by a third party rather than the controller, name it. |
| Categories of personal data | The data fields processed. Flag any special-category data (Article 9): Article 6(1)(f) does not by itself legitimize special-category processing, which also requires an Article 9(2) condition. |
| Categories of data subjects | Whose data is processed. State whether children or other vulnerable individuals are among them (this carries extra weight in the balancing test). |
| Source of the data | Collected from the data subject, or obtained indirectly. |
| Processing activities and technologies | What is done with the data, and the systems or techniques involved. |

## Section 2. The three-part test

The three parts are cumulative: the basis is available only where all three pass. The structure follows Article 6(1)(f) and Recital 47, and is articulated as three cumulative conditions in EDPB Opinion 28/2024.

### 2.1 Purpose test (is there a legitimate interest?)

| Criterion | Assessment (Yes / No) | Rationale and evidence |
| --- | --- | --- |
| The interest is **lawful** (consistent with applicable law). | | |
| The interest is **clearly and precisely articulated** (not vague). | | |
| The interest is **real and present** (not speculative or remote). | | |
| State the specific interest and who pursues it (controller or named third party). | | |

Recital 47 recognizes certain interests as capable of being legitimate, including fraud prevention, direct marketing, and (Recital 48) intra-group administrative transfers; naming the interest within a recognized category strengthens the analysis but does not by itself satisfy the necessity and balancing tests.

### 2.2 Necessity test (is the processing necessary?)

| Question | Assessment (Yes / No) | Rationale and evidence |
| --- | --- | --- |
| Does the processing actually allow the legitimate interest to be pursued? | | |
| Is there no less intrusive way to achieve the same purpose? | | |
| Is the processing consistent with data minimization (Article 5(1)(c)): no more data than necessary? | | |

Necessity is assessed against Recital 39 and the data-minimization principle: if the purpose can reasonably be achieved with less data or by a less intrusive means, the processing is not necessary for the purposes of Article 6(1)(f).

### 2.3 Balancing test (do the data subject's interests, rights, and freedoms override?)

| Factor | Assessment | Rationale and evidence |
| --- | --- | --- |
| The data subject's interests, fundamental rights, and freedoms at stake. | | |
| The data subject's **reasonable expectations** given the relationship with the controller (Recital 47). | | |
| The nature of the data and the intrusiveness of the processing. | | |
| The possible impact or harm to the data subject. | | |
| Whether the data subject is a **child** or otherwise vulnerable (Article 6(1)(f) names children explicitly; this weighs against the interest). | | |
| Safeguards and mitigations that reduce the impact (transparency, the Article 21 right to object and how it is offered, pseudonymization, retention limits, access controls). | | |
| **Conclusion**: does the legitimate interest prevail after the safeguards are applied? | | |

## Section 3. Outcome and decision

| Field | Required content |
| --- | --- |
| Overall verdict | Article 6(1)(f) is available / is not available for this processing. |
| Residual concerns | Any concerns that remain after the safeguards. |
| Committed safeguards | The mitigations the organization commits to (those relied on in 2.3 must be implemented). |
| Right to object (Article 21) | How the data subject's right to object is handled and surfaced. Confirm the Article 21(4) prominence requirement: the right is brought explicitly to the data subject's attention, presented clearly and separately from other information, at the latest at the first communication. |
| DPIA required? | Whether the processing is high-risk and a DPIA ([`privacy/template-dpia.md`](template-dpia.md)) is also required. |
| Record of Processing Activities reference | The activity identifier this LIA is linked from. |
| Assessor | Role that completed the LIA. |
| Date completed | |
| DPO review | Date of DPO (or acting DPO) review and the DPO's opinion on whether the basis is available. |
| Approver | Role with authority to approve reliance on the basis. |
| Date approved | |
| Date of next scheduled review | At minimum annual; sooner upon material change (per Section 4). |

## Section 4. Review triggers

Re-run this assessment:

- Annually, as part of the privacy programme review cadence.
- On any material change to the purpose, the categories of data or data subjects, the processing activity, or the relationship with the data subject.
- Whenever the balance struck in Section 2.3 may have shifted (for example, a new data source, a change in data subjects' reasonable expectations, or a new impact).

## Framework alignment

| Reference | Provision | Relevance to this template |
| --- | --- | --- |
| GDPR (Regulation (EU) 2016/679) | Article 6(1)(f) | The legitimate-interests lawful basis and its override clause; the basis this LIA evidences. |
| GDPR | Recital 47 | Reasonable expectations, the controller-or-third-party interest, the careful-assessment requirement, and recognized interests (fraud prevention, direct marketing). |
| GDPR | Recital 39, Article 5(1)(c) | Necessity and data minimization, the no-less-intrusive-means analysis in the necessity test. |
| GDPR | Article 21 | The right to object that attaches to Article 6(1)(f) processing (Article 21(1) also covers Article 6(1)(e), outside this template's scope); recorded in Section 3, including the Article 21(4) prominence requirement. |
| GDPR | Article 5(2) | Accountability: the documented assessment is the evidence of compliance. |
| UK GDPR | Article 6(1)(f) | The equivalent legitimate-interests basis for UK-scoped processing. |
| EDPB Opinion 28/2024 | Legitimate-interest analysis | Articulates the three cumulative conditions (purpose, necessity, balancing) and the assessment factors. |
| ISO/IEC 27701:2025 | Privacy information management | The PIMS control environment within which the lawful-basis determination is recorded and reviewed. |

## Limitations

This template is a CC BY-SA 4.0 structural baseline. Adopting organizations must validate the template against the specific obligations of their applicable jurisdictions, the published guidance of their supervisory authority, and the requirements of any sectoral regulator. The template is not a substitute for legal advice. Where the supervisory authority publishes its own legitimate-interests guidance or methodology, the supervisory authority's instrument prevails to the extent of any inconsistency.

A populated LIA contains operationally sensitive information (the interests pursued, the risks weighed, the residual-risk decision). This template provides no example values for any field, and adopting organizations must store populated LIAs under an appropriate confidentiality classification.

---

**End of Document**
