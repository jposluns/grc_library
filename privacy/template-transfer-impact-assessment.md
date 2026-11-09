# Transfer Impact Assessment (TIA) Template

**Document Title:** Transfer Impact Assessment (TIA) Template\
**Document Type:** Template\
**Version:** 1.0.3\
**Date:** 2026-07-13\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/register-cross-border-data-flow.md`](register-cross-border-data-flow.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/standard-pseudonymization-and-anonymization.md`](standard-pseudonymization-and-anonymization.md), [`privacy/jurisdictions/annex-privacy-european-union.md`](jurisdictions/annex-privacy-european-union.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material processing, jurisdiction, or regulatory change\
**Repository Path:** [`privacy/template-transfer-impact-assessment.md`](template-transfer-impact-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template is the instrument that records and evidences a **Transfer Impact Assessment (TIA)**: the documented assessment an organization completes before transferring personal data to a third country in reliance on an Article 46 transfer tool, to confirm that the tool secures, in the destination country, a level of protection essentially equivalent to that guaranteed within the EEA. It operationalizes the **six-step methodology in the EDPB Recommendations 01/2020 on measures that supplement transfer tools** (attributed; the methodology is articulated by the European Data Protection Board, not reproduced verbatim here) and evidences compliance with **GDPR Chapter V** (Regulation (EU) 2016/679, Articles 44 to 49).

The assessment exists because **GDPR Article 46(1)** permits a transfer on the basis of appropriate safeguards only where "enforceable data subject rights and effective legal remedies for data subjects are available", and the effectiveness of those safeguards depends on the law and practice of the destination country. Where the destination country's law (for example its government-access and surveillance regime) would undermine the Article 46 tool, the transfer may proceed only if supplementary measures bring the protection back up to the required standard, or it must be suspended.

A populated TIA is operationally sensitive: complete it as a working document, not as published content.

## Scope

This template applies wherever the organization transfers, or proposes to transfer, personal data to a third country or international organization in reliance on an **Article 46** appropriate-safeguards tool (Commission Standard Contractual Clauses, binding corporate rules, or another Article 46 mechanism).

It does **not** apply where:

- the transfer is covered by a European Commission **adequacy decision under Article 45** (no TIA is required, though the adequacy decision's continued validity should be monitored); or
- the transfer relies on an **Article 49 derogation** (explicit consent, contract necessity, important reasons of public interest, legal claims, vital interests, or the compelling-legitimate-interests last resort), which has its own conditions and is not a substitute for a general transfer mechanism.

The controlling process is the [cross-border transfer procedure](procedure-privacy-impact-and-cross-border-transfer.md); this template is the instrument that procedure invokes for EEA-origin transfers, and the completed TIA is referenced from the [cross-border data flow register](register-cross-border-data-flow.md). Where a transfer is also governed by another regime (for example China PIPL), the strictest applicable requirement governs, per that procedure.

## How to use this template

1. Complete **Section 1** to map the transfer precisely.
2. Work **Sections 2 to 6** in order; they follow the EDPB six-step methodology. Each step must be completed before the next is meaningful.
3. Record the overall outcome and the committed supplementary measures in **Section 7**, with sign-off.
4. Record the TIA reference in the corresponding [cross-border data flow register](register-cross-border-data-flow.md) entry and in the Record of Processing Activities.
5. Re-run the assessment on the triggers in Section 6.

Fill the right-hand cells of each table. A field left blank is an incomplete assessment, not a passed one.

## Section 1. Know the transfer (Step 1: mapping)

| Field | Required content |
| --- | --- |
| Transfer name and identifier | Stable identifier, cross-referenced from the cross-border data flow register and the Record of Processing Activities. |
| Exporter | The EEA controller or processor exporting the data. |
| Importer | The third-country recipient (controller, processor, or sub-processor) and its role. |
| Destination country or countries | The third country or international organization receiving the data, including onward-transfer destinations. |
| Categories of personal data | The data fields transferred. Flag special-category data (Article 9) and data of children or other vulnerable individuals. |
| Categories of data subjects | Whose data is transferred. |
| Purpose and processing in the destination | What the importer does with the data, and the systems involved. |
| Transfer mechanics | The technical path (direct, via sub-processor, remote access, cloud storage location), including whether the data is in the clear at any point. |

## Section 2. Identify the transfer tool (Step 2)

| Field | Required content |
| --- | --- |
| Is the destination covered by an Article 45 adequacy decision? | Yes / No. If yes, no TIA is required; record the decision and monitor its validity, and stop here. |
| The Article 46 tool relied on | The specific appropriate-safeguards tool: Commission Standard Contractual Clauses (Article 46(2)(c)), binding corporate rules (Articles 46(2)(b) and 47), an approved code of conduct with binding and enforceable commitments (Article 46(2)(e)), an approved certification mechanism with binding and enforceable commitments (Article 46(2)(f)), or an authorization-required mechanism (ad hoc contractual clauses or administrative arrangements between public authorities, Article 46(3)). Name the specific instrument and module or set of clauses; note that a code of conduct or certification carries a different effectiveness analysis in Section 3 than Standard Contractual Clauses or binding corporate rules; for the certification mechanism, the EDPB's **Guidelines 07/2022 on certification as a tool for transfers** (Version 2.0, adopted 14 February 2023) are the authoritative guidance on that analysis. |
| Is an Article 49 derogation being relied on instead? | If so, this template does not apply; the derogation's own conditions govern, and a derogation is not a repeatable general transfer mechanism. |
| Status of the tool | Executed / in negotiation; the date and the parties bound. |

## Section 3. Assess the effectiveness of the tool in the destination (Step 3)

This is the Schrems II assessment: whether anything in the destination country's law or practice would prevent the Article 46 tool from securing essentially equivalent protection, with particular attention to public-authority and government access to the transferred data.

| Factor | Assessment | Rationale and evidence |
| --- | --- | --- |
| The destination country's laws relevant to the transfer (data protection, government access, surveillance, retention). | | |
| Whether public authorities in the destination can access the data, on what legal basis, and with what limits. | | |
| Whether a third-country authority's demand to transfer or disclose the data would have a basis in an international agreement (GDPR Article 48); a court judgment or administrative order not founded on such an agreement (for example a mutual legal assistance treaty) is not, by itself, a lawful ground for the importer to disclose. | | |
| Whether data subjects have enforceable rights and effective legal remedies in the destination (Article 46(1)). | | |
| Whether independent oversight of public-authority access exists. | | |
| Relevant sources consulted (legislation, supervisory-authority guidance, case law, government-access transparency, the importer's documented experience of access requests). | | |
| **Conclusion**: does the Article 46 tool, on its own, secure essentially equivalent protection? | | |

## Section 4. Identify and adopt supplementary measures (Step 4)

Complete this section only where Section 3 concludes the tool alone is not effective. Supplementary measures must address the specific deficiency identified, and a measure that does not address the identified risk does not make the transfer lawful.

| Measure type | Measure adopted | How it addresses the Section 3 deficiency |
| --- | --- | --- |
| Technical (for example strong encryption with keys held only in the EEA, pseudonymization per [`privacy/standard-pseudonymization-and-anonymization.md`](standard-pseudonymization-and-anonymization.md), split or multi-party processing). | | |
| Contractual (for example transparency on access requests, warranties, audit rights, commitments to challenge unlawful requests). | | |
| Organizational (for example access-request logging and notification, internal policy, data-minimization before transfer, governance of onward transfers). | | |
| **Conclusion**: with the supplementary measures applied, is essentially equivalent protection achieved? | | |

## Section 5. Procedural steps (Step 5)

| Field | Required content |
| --- | --- |
| Formal adoption of supplementary measures | Where supplementary measures are relied on, how they are bound (amended clauses, technical configuration, documented procedure). |
| Re-execution or amendment of the Article 46 tool, if required | Whether the measures require a change to the clauses or arrangement. |
| Supervisory-authority consultation, where required | Whether the chosen path requires authorization or consultation, and its status. |
| Decision to proceed, pause, or suspend | The transfer proceeds only where essentially equivalent protection is established; otherwise it is paused or suspended. |

## Section 6. Re-evaluation (Step 6)

Re-run this assessment:

- At appropriate intervals defined by the risk of the transfer (at minimum, on the cadence in the cross-border data flow register).
- On any material change to the destination country's law or practice (for example a new surveillance law or a relevant court judgment).
- On any material change to the transfer (new data categories, new importer or sub-processor, new onward transfer, changed purpose).
- On any change to the validity of the Article 46 tool relied on.

## Section 7. Outcome, decision, and sign-off

| Field | Required content |
| --- | --- |
| Overall verdict | The transfer may proceed under the Article 46 tool (with the committed supplementary measures) / may not proceed and is paused or suspended. |
| Committed supplementary measures | The measures relied on in Section 4 that must be implemented and maintained. |
| Residual risk and its acceptance | Any residual risk after the measures, and the role that accepts it where acceptance is within authority. |
| Record of Processing Activities reference | The activity identifier this TIA is linked from. |
| Cross-border data flow register reference | The register entry whose TIA-reference field points to this assessment. |
| Assessor | Role that completed the TIA. |
| Date completed | |
| DPO review | Date of DPO review and the DPO's opinion on whether the transfer may proceed. |
| Approver | Role with authority to approve the transfer on the basis of this TIA. |
| Date approved | |
| Date of next scheduled review | Per Section 6. |

## Framework alignment

| Reference | Provision | Relevance to this template |
| --- | --- | --- |
| GDPR (Regulation (EU) 2016/679) | Article 44 | General principle that all Chapter V conditions must be met so the level of protection is not undermined. |
| GDPR | Article 45 | Adequacy decisions; where one applies, a TIA is not required (Section 2). |
| GDPR | Article 46 | Appropriate-safeguards transfer tools (Standard Contractual Clauses, binding corporate rules); Article 46(1) requires enforceable rights and effective remedies, the basis this TIA assesses. |
| GDPR | Article 47 | Binding corporate rules as an Article 46 tool. |
| GDPR | Article 48 | A third-country authority's order to transfer or disclose is recognizable or enforceable only on the basis of an international agreement; central to the Section 3 government-access assessment. |
| GDPR | Article 49 | Derogations; outside this template's scope (Section 2). |
| EDPB Recommendations 01/2020 | Measures that supplement transfer tools | The six-step methodology this template operationalizes (attributed; framed in this library's own operational prose, not reproduced verbatim). |
| EDPB Guidelines 07/2022 | Certification as a tool for transfers | The authoritative guidance on the Article 46(2)(f) certification-mechanism transfer tool and its effectiveness analysis, distinct from the Standard-Contractual-Clauses and binding-corporate-rules analysis. |
| UK GDPR | Articles 44 to 49 | The equivalent restricted-transfer regime for UK-scoped transfers (the UK uses its own transfer-risk-assessment approach; adapt the destination-law analysis accordingly). |
| ISO/IEC 27701:2025 | Privacy information management | The PIMS control environment within which the transfer determination is recorded and reviewed. |

## Limitations

This template is a CC BY-SA 4.0 structural baseline. Adopting organizations must validate the template against the specific obligations of their applicable jurisdictions, the published guidance of their supervisory authority, the current text of the transfer tool they rely on, and any change to adequacy decisions or to the destination country's law. The six-step methodology is attributed to the EDPB Recommendations 01/2020; an organization relying on it should consult the current text of that Recommendation and confirm the current version of any Standard Contractual Clauses decision it cites. The template is not a substitute for legal advice, and a TIA does not by itself make an unlawful transfer lawful: where essentially equivalent protection cannot be established, the transfer must be paused or suspended.

A populated TIA contains operationally sensitive information (the destination-law analysis, the access-risk assessment, the residual-risk decision). This template provides no example values for any field, and adopting organizations must store populated TIAs under an appropriate confidentiality classification.

---

**End of Document**
