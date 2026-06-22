# DPIA (Data Protection Impact Assessment) Template

**Document Title:** DPIA (Data Protection Impact Assessment) Template\
**Document Type:** Template\
**Version:** 1.0.2\
**Date:** 2026-06-22\
**Owner:** Chief Privacy Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/register-automated-decision-making.md`](register-automated-decision-making.md), [`privacy/framework-childrens-data.md`](framework-childrens-data.md), [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material processing, jurisdiction, or regulatory change\
**Repository Path:** [`privacy/template-dpia.md`](template-dpia.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines the structure of a Data Protection Impact Assessment (DPIA) sufficient to evidence the controller's obligations under GDPR Article 35 and the equivalent obligations under UK GDPR, LGPD Article 38, PIPL Article 55, the EU AI Act (where the processing is part of a high-risk AI system), and AIDA section 29 (Canada). The template provides three working checklists that operationalize the Article 35 framework:

1. The Article 35(1) trigger checklist (when a DPIA is required).
2. The EDPB WP248 nine-criteria framework (the indicators that, when two or more apply, signal high risk requiring a DPIA).
3. The Article 35(7) content checklist (what a complete DPIA must contain).

A populated DPIA is operationally sensitive material and must not be published in this public CC BY-SA 4.0 repository. Adopting organisations populate the template internally, classify it under the organisation's information classification scheme, and retain it per the retention requirements of the operative procedure.

This template addresses Data Protection Impact Assessments only. Assessments of cross-border data transfers (Transfer Impact Assessments, TIAs) are out of scope and are addressed by a separate template; see [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md) Step 4 for the controlling procedure.

---

## Scope

This template applies wherever the organisation, acting as a controller (or as a joint controller jointly with another party), proposes to carry out, or has carried out, processing that is likely to result in a high risk to the rights and freedoms of natural persons. It applies before processing begins (the prior-assessment rule of Article 35(1)) and on each material change to the processing operation.

Where the processing involves an AI system, this template is used together with the AI System Impact Assessment Procedure (see [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md)); the DPIA addresses the data protection limb and the AI System Impact Assessment addresses the AI-specific limb. The two assessments share evidence and reference each other.

---

## How to use this template

1. Begin with the Article 35(1) trigger checklist (Section 1). If any explicit trigger applies, a DPIA is required.
2. If no explicit trigger applies, work through the EDPB WP248 nine-criteria framework (Section 2). When two or more criteria apply, a DPIA is required. When one criterion applies, a DPIA may still be appropriate; document the rationale for the decision either way.
3. If a DPIA is required, complete the Article 35(7) content checklist (Section 3) for the processing operation.
4. Submit the completed DPIA to the Chief Privacy Officer (or the role acting in that capacity) for review per the operative procedure.
5. Where the residual risk after mitigation remains high, consult the supervisory authority under Article 36 prior to commencing the processing.
6. Record the DPIA reference identifier in the Record of Processing Activities entry for the processing operation (see [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), controller-view field "DPIA reference").

---

## Section 1. Article 35(1) trigger checklist

A DPIA must be carried out where a type of processing, in particular using new technologies, taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons. The following three trigger statements are explicit in Article 35(3); each, on its own, requires a DPIA.

| # | Article 35(3) trigger | Applies? (Yes / No) | Evidence or rationale |
| --- | --- | --- | --- |
| T1 | Systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person. (Article 35(3)(a)) | | |
| T2 | Processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10. (Article 35(3)(b)) | | |
| T3 | A systematic monitoring of a publicly accessible area on a large scale. (Article 35(3)(c)) | | |

In addition to the three explicit triggers, the supervisory authority of each Member State publishes a list of the kinds of processing operations which are subject to the requirement for a DPIA (Article 35(4)) and may publish a list of those for which no DPIA is required (Article 35(5)). The controller must consult the applicable supervisory authority's list before concluding that no DPIA is required.

| Supervisory authority list consulted | Date consulted | Outcome (DPIA required / Not required / Inconclusive) |
| --- | --- | --- |
| | | |

---

## Section 2. EDPB WP248 nine-criteria framework

Where no Article 35(3) trigger applies on its own, the controller assesses the processing against the nine criteria set out by the (then) Article 29 Working Party in WP248 rev.01 (4 October 2017), endorsed by the European Data Protection Board (EDPB) at its first plenary meeting (25 May 2018). The criteria are indicators of high-risk processing.

The EDPB position is that, as a rule of thumb, where two or more criteria are met the processing is likely to result in high risk and a DPIA is required. Where only one criterion is met, the controller may still need to conduct a DPIA; the rationale must be recorded either way.

| # | EDPB WP248 criterion | Applies? (Yes / No) | Evidence or rationale |
| --- | --- | --- | --- |
| C1 | Evaluation or scoring, including profiling and predicting, especially from aspects concerning the data subject's performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements. | | |
| C2 | Automated decision-making with legal or similar significant effect: processing that aims at taking decisions on data subjects producing legal effects concerning the natural person or which similarly significantly affects the natural person. | | |
| C3 | Systematic monitoring: processing used to observe, monitor or control data subjects, including data collected through networks or a systematic monitoring of a publicly accessible area. | | |
| C4 | Sensitive data or data of a highly personal nature: includes special categories of personal data as defined in Article 9 (e.g., information about individuals' political opinions), personal data relating to criminal convictions or offences under Article 10, and personal data linked to household and private activities (such as electronic communications whose confidentiality must be protected), or data affecting the exercise of a fundamental right, or data whose disclosure clearly impacts the data subject's day-to-day life. | | |
| C5 | Data processed on a large scale: the EDPB recommends that the following factors be considered in particular when determining whether processing is carried out on a large scale: the number of data subjects concerned (either as a specific number or as a proportion of the relevant population); the volume of data and the range of different data items being processed; the duration, or permanence, of the data processing activity; the geographical extent of the processing activity. | | |
| C6 | Matching or combining datasets: for example originating from two or more data processing operations performed for different purposes and/or by different data controllers in a way that would exceed the reasonable expectations of the data subject. | | |
| C7 | Data concerning vulnerable data subjects: the processing of this type of data is a criterion because of the increased power imbalance between the data subjects and the data controller. Vulnerable data subjects include children, employees, more vulnerable segments of the population requiring special protection (mentally ill persons, asylum seekers, the elderly, patients), and any case where an imbalance in the relationship between the position of the data subject and the controller can be identified. | | |
| C8 | Innovative use or applying new technological or organisational solutions: like combining use of fingerprints and face recognition for improved physical access control. The EDPB notes that the use of such technology can involve novel forms of data collection and usage, possibly with a high risk to individuals' rights and freedoms. | | |
| C9 | When the processing in itself prevents data subjects from exercising a right or using a service or a contract: this includes processing performed in a public area that people passing by cannot avoid, or processing that aims at allowing, modifying or refusing data subjects' access to a service or entry into a contract. | | |

**Decision rule:**

- Two or more criteria met: DPIA required.
- One criterion met: DPIA may be required; record the rationale and the assessor's conclusion.
- No criterion met and no Article 35(3) trigger applies and no supervisory-authority list entry applies: DPIA not required; record the assessment and the date.

| Criteria met (count) | DPIA required (Yes / No) | Rationale | Assessor | Date |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Section 3. Article 35(7) DPIA content checklist

Where a DPIA is required, the assessment must contain at least the four content blocks set out in Article 35(7). The controller may add further blocks (for example, a specific AI-system limb, a cross-border-transfer limb, or a children's-data limb) but must not omit any of the four mandatory blocks.

### 3.1. Systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller (Article 35(7)(a))

| Field | Required content |
| --- | --- |
| Processing operation name and identifier | Stable identifier, cross-referenced from the Record of Processing Activities |
| Nature of the processing | What is being done with the personal data (collection, storage, analysis, disclosure, deletion) |
| Scope of the processing | The categories and volumes of data subjects, the categories and volumes of personal data, the geographical and temporal extent |
| Context of the processing | The relationship to the data subject, the data subject's reasonable expectations, the source of the data, the technologies used |
| Purposes of the processing | Each purpose stated separately; the lawful basis under Article 6 (and Article 9 where special-category data is processed) for each purpose |
| Legitimate interest (where applicable) | Where the lawful basis is Article 6(1)(f), the legitimate interest pursued and the balancing analysis |
| Joint controllers (where applicable) | Identity of any joint controller and the essence of the Article 26 arrangement |
| Processors (where applicable) | Categories of processors and the essence of the Article 28 contract |
| Data flows | Diagram or description of the flow of personal data through the processing operation, including cross-border transfers (cross-reference the cross-border data flow register) |

### 3.2. Assessment of the necessity and proportionality of the processing operations in relation to the purposes (Article 35(7)(b))

| Field | Required content |
| --- | --- |
| Necessity | Why the processing is necessary for the stated purpose; whether the purpose could be achieved with less personal data or by less intrusive means |
| Proportionality | Whether the processing is proportionate to the purpose; whether the volume, retention, and access scope are limited to what is necessary |
| Data minimisation | The data minimisation measures applied (Article 5(1)(c)) |
| Purpose limitation | How the controller prevents use of the data for incompatible purposes (Article 5(1)(b)) |
| Storage limitation | The retention period and the deletion mechanism (Article 5(1)(e)); cross-reference to the data retention schedule |
| Accuracy | Measures to ensure that the data is accurate and kept up to date (Article 5(1)(d)) |
| Lawfulness, fairness, transparency | The Article 13 or 14 information provided to data subjects; the cross-reference to the privacy notice |
| Data subject rights | How the controller will give effect to the rights of access, rectification, erasure, restriction, portability, and objection (Articles 15 to 22); cross-reference to the data subject rights procedure |
| Consent (where applicable) | Where the lawful basis is consent (Article 6(1)(a) or Article 9(2)(a)), the consent mechanism and the means of withdrawal; cross-reference to the consent management framework |

### 3.3. Assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1 (Article 35(7)(c))

For each identified risk:

| Field | Required content |
| --- | --- |
| Risk identifier | Stable identifier within the DPIA |
| Risk description | The specific risk to the rights and freedoms of data subjects (e.g., risk of unauthorised disclosure of health data leading to discrimination in employment) |
| Sources of risk | The threats and vulnerabilities giving rise to the risk |
| Affected rights and freedoms | The Charter of Fundamental Rights articles and the GDPR rights potentially affected (e.g., Article 8 of the Charter, GDPR Article 17 right to erasure) |
| Affected data subjects | The categories and approximate numbers of data subjects who could be affected; identify vulnerable data subjects separately |
| Likelihood | Assessed likelihood (low / medium / high), with rationale; assessed on the ISO 31000 likelihood scale or equivalent |
| Severity | Assessed severity (low / medium / high), with rationale; the severity reflects the impact on the data subject, not on the controller |
| Inherent risk level | Combined likelihood and severity, before mitigation |

Risks must include, at minimum: unauthorised access, unauthorised modification, unauthorised loss or destruction, unauthorised disclosure, unlawful processing, processing inconsistent with the data subject's reasonable expectations, and any AI-specific risk (bias, model opacity, automated decision error) where the processing involves an AI system.

### 3.4. The measures envisaged to address the risks (Article 35(7)(d))

Per Article 35(7)(d), the controller must record the safeguards, security measures and mechanisms that protect personal data and demonstrate compliance with the Regulation, taking into account the rights and legitimate interests of data subjects and other persons concerned.

For each identified risk, the corresponding treatment:

| Field | Required content |
| --- | --- |
| Risk identifier | Cross-reference to Section 3.3 |
| Mitigation measure | The technical or organisational measure that addresses the risk |
| Owner role | The role accountable for implementing the measure (role-based; not a named individual) |
| Implementation date | The date by which the measure must be in place |
| Residual likelihood | The likelihood remaining after the measure is implemented |
| Residual severity | The severity remaining after the measure is implemented |
| Residual risk level | Combined residual likelihood and severity |
| Acceptance authority | Where the residual risk is accepted, the role that has the authority to accept it (cross-reference to the exception and risk acceptance policy) |
| Article 36 consultation | Where the residual risk remains high, the date and outcome of the prior consultation with the supervisory authority |

Measures must include, at minimum: technical measures (encryption at rest and in transit, access control, logging, pseudonymisation where appropriate, secure disposal), organisational measures (role-based access, training, contractual obligations on processors, audit), and procedural measures (incident response, data subject rights handling, breach notification).

---

## Section 4. Sign-off and review

| Field | Required content |
| --- | --- |
| Assessor | Role that completed the DPIA |
| Date completed | |
| Chief Privacy Officer review | Date of Chief Privacy Officer (or acting Chief Privacy Officer) review and the reviewer's opinion |
| Approver | Role with authority to approve the processing on the basis of the DPIA |
| Date approved | |
| Date of next scheduled review | At minimum annual; sooner upon material change |
| Cross-reference to ROPA entry | Activity identifier from the Record of Processing Activities |
| Cross-reference to data subject information | Privacy notice identifier or other Article 13 / 14 evidence |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 35 | Data Protection Impact Assessment obligation, triggers, and required content |
| GDPR | Article 36 | Prior consultation with the supervisory authority where residual risk is high |
| UK GDPR | Article 35 | Equivalent obligation under UK law |
| EDPB | WP248 rev.01 (endorsed 25 May 2018) | Nine-criteria framework for identifying high-risk processing |
| LGPD | Article 38 | Data Protection Impact Report (Relatório de Impacto à Proteção de Dados Pessoais) |
| PIPL | Article 55 | Personal Information Protection Impact Assessment |
| EU AI Act | Article 27 | Fundamental rights impact assessment (where the DPIA is integrated with the AI-system limb) |
| ISO/IEC 29134:2017 | Privacy impact assessment methodology | Methodology guidance for PIA / DPIA |
| ISO/IEC 27701:2025 | Privacy information management | DPIA as a privacy control |
| NIST Privacy Framework | CT.PO-P5, CM.AW-P5 | Risk assessment and awareness |
| AIDA (Canada, Bill C-27 Part 3) | AIDA section 29 | AI Impact Assessment (where applicable to the same processing operation) |

---

## Limitations

This template is a CC BY-SA 4.0 structural baseline. Adopting organisations must validate the template against the specific obligations of their applicable jurisdictions, the published guidance of their supervisory authority, and the requirements of any sectoral regulator. The template is not a substitute for legal advice. Where the supervisory authority publishes its own DPIA template or methodology, the supervisory authority's instrument prevails to the extent of any inconsistency.

A populated DPIA contains operationally sensitive information (system architecture detail, identified risks, residual risk acceptances). This template provides no example values for any field and adopting organisations must store populated DPIAs under an appropriate confidentiality classification.

---

**End of Document**
