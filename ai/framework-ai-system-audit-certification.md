# AI System Audit and Certification Framework

**Document Title:** AI System Audit and Certification Framework\
**Document Type:** Framework\
**Version:** 1.0.26\
**Date:** 2026-10-30\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This framework defines the audit and certification approach for AI systems within the organization. It establishes the audit programme structure, evidence requirements, audit frequency by audit tier, the certification pathway to ISO/IEC 42001:2023, post-market monitoring obligations, conformity assessment requirements for EU AI Act high-risk systems, and the integration of audit findings into the corrective and preventive action (CAPA) process.

The framework draws on ISO/IEC 42001:2023 §9.2 to 9.3 (internal audit and management review), EU AI Act Chapter IX (post-market monitoring and serious incident reporting), NIST AI RMF 1.0 Measure and Manage functions, ISO/IEC 42006:2025 (requirements for bodies providing third-party audit and certification of an AI management system), and the Cloud Security Alliance AI Controls Matrix (CSA AICM v1.1).

### 1.2 Scope

This framework applies to all AI systems in production or entering production. It covers:

- Internally developed AI systems.
- Procured or third-party AI systems that the organization deploys and operates.
- AI systems embedded within third-party services that the organization configures and is responsible for deploying.
- General-purpose AI models integrated into the organization's products, services, or operational processes.

This framework complements the Supplier Third-Party AI Due Diligence Procedure (see [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md)) for external AI services where the organization is not the technical operator. That procedure applies at the point of supplier selection and periodic supplier review; this framework applies to systems once they are in production.

---

## 2. Governance

### 2.1 AIGC: audit programme owner

The AI Governance Council (AIGC) owns the AI audit programme. It approves the annual AI audit plan, reviews audit findings, tracks CAPA completion, and escalates unresolved material findings to the Board or appropriate Board committee.

### 2.2 CISO: technical audit lead

The CISO leads the technical execution of AI audits. The CISO is responsible for:

- Scheduling and resourcing audit activities.
- Maintaining the AI audit evidence repository.
- Engaging independent third-party auditors for high-risk system audits.
- Reporting audit findings to the AIGC.
- Ensuring CAPA records are raised for each finding and tracked to closure.

### 2.3 Independent auditor for high-risk systems

High-risk AI systems (EU AI Act Annex III) require an independent auditor who is not involved in the development or operation of the system under review. For systems requiring EU AI Act conformity assessment by a third-party notified body, the engagement and output of that assessment satisfies the independent audit requirement for that assessment cycle.

---

## 3. AI system audit classification and frequency

All AI systems are assigned an audit tier at the time of classification (see [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) Section 4). Audit tier determines the frequency, audit type, and evidence requirements.

| Audit Tier | System Classification | Audit Frequency | Audit Type | Primary Evidence Required |
|---|---|---|---|---|
| **Audit Tier 1: High-Risk** | systems high-risk under EU AI Act Article 6 (Annex III use cases after the Article 6(3) derogation, or products and safety components covered by Article 6(1) and Annex I); safety-critical AI; AI making or materially influencing decisions with significant impact on individuals | Annual | Full technical audit by independent auditor; includes conformity assessment alignment check | Model card; system card; training data provenance; bias and fairness test results; explainability documentation; human oversight records; incident register entries; post-market monitoring data; FRIA (where the Article 27(1) deployer test is met) |
| **Audit Tier 2: General-Purpose** | GPAI models integrated into products or operations; large language models; foundation models | Every 18 months | Internal audit with CISO lead; supplemented by provider's published transparency documentation | Model card; system card; provider transparency documentation; use case assessment; incident register entries; copyright and licensing records |
| **Audit Tier 3: Standard** | AI systems with limited decision-making impact; AI tools used for operational support without individual impact | Every 24 months (biennial) | Internal audit | AI System Register entry; model card (if applicable); access control review; incident log review |
| **Audit Tier 4: Low-Risk** | Minimal-risk AI tools; AI-assisted productivity tools without personal data processing or individual impact | Every 24 months (biennial); triggered review if risk profile changes | Desk-based review | AI System Register entry; confirmation of current classification; access log review |

---

## 4. Audit evidence catalogue

The following evidence must be available for each audit tier. Evidence gaps identified during the pre-audit documentation review are recorded as preliminary findings and must be remediated before the audit proceeds, unless the auditor determines a compensating assessment is adequate.

### 4.1 Audit tier 1 (high-risk): full evidence requirements

| Evidence Item | Description | Responsible Party |
|---|---|---|
| Model card | Completed model card per [`ai/template-model-card.md`](template-model-card.md); current version reflecting the model in production | AI System Owner |
| System card | Completed system card per [`ai/template-system-card.md`](template-system-card.md); includes deployment context, human oversight design, and limitations | AI System Owner |
| Training data provenance | Documentation of training data sources, data quality measures, data governance agreements, and any data exclusions | AI System Owner / Data Owner |
| Bias and fairness test results | Results of bias testing performed before deployment and at the most recent periodic re-assessment; methodology documented | CISO / AI System Owner |
| Explainability documentation | Description of explainability approach; output of explainability testing; documentation of any inherent explainability limitations | AI System Owner |
| Human oversight records | Evidence that designated human overseers exist; training completion records (anonymized); evidence of override capability testing; evidence that overseers hold the necessary competence and authority and receive the necessary support (Article 26(2)) | AI System Owner / Business Unit Owner |
| Fundamental rights impact assessment (FRIA) | Completed FRIA where required per [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) Section 5.2 (Article 27(1) deployer test); evidence of Data Protection Officer review | Data Protection Officer / AI System Owner |
| Incident register entries | Extract from the AI Incident Register for incidents involving this system in the preceding audit period | CISO |
| Post-market monitoring data | Monitoring plan; performance metrics including accuracy trend, drift metrics, and bias drift; alerts generated and resolved | AI System Owner |
| Conformity assessment records | EU AI Act Annex IV technical documentation; prior conformity assessment report if applicable | CISO / Legal |

### 4.2 Audit tier 2 (general-purpose): evidence requirements

Model card; system card; provider-published transparency and capability documentation; use case scope assessment; copyright and licensing records; incident register entries for the system for the preceding 18 months.

### 4.3 Audit tier 3 (standard) and audit tier 4 (low-risk): evidence requirements

AI System Register entry (current); model card if the system uses a trained model; access control configuration review output; incident log review for the system for the preceding audit period.

---

## 5. Internal audit process

### 5.1 Scoping

At least four weeks before the audit commences, the CISO confirms:

- The AI system(s) to be audited.
- The audit tier and applicable evidence requirements.
- The audit team composition (internal auditors; independent auditor for Audit Tier 1).
- The audit period covered.
- The audit objectives and any specific focus areas identified from the previous audit, incident register, or post-market monitoring signals.

### 5.2 Pre-audit documentation review

The auditor conducts a desk-based review of all evidence items listed in Section 4. Gaps and deficiencies are logged in a pre-audit findings list and communicated to the AI System Owner. The AI System Owner has 10 business days to remediate or provide a written explanation for any gap before the on-site or technical review phase begins.

### 5.3 Technical review checklist

During the technical review phase, the auditor verifies:

- AI system configuration matches the system card description.
- Access controls are consistent with the principle of least privilege; privileged access is logged.
- Human oversight mechanism functions as documented; override capability is testable.
- Monitoring and alerting are active and alert thresholds are documented.
- AI-generated content labelling is implemented where required.
- Output validation controls are in place before downstream use.
- Security controls align with the AI Algorithmic Compliance Checklist ([`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md)).

### 5.4 Human oversight observation

For Audit Tier 1 systems, the auditor conducts a structured observation of the human oversight process, confirming that designated overseers understand the system's limitations, are capable of interpreting outputs, and can exercise the override capability documented in the system card.

### 5.5 Bias re-assessment

At each audit of an Audit Tier 1 system, bias testing is re-run against the current production model. Results are compared with the baseline recorded in the training data provenance and original deployment documentation. Statistically significant increases in bias across protected characteristics are recorded as High findings. The comparison reports its uncertainty at the organization-set confidence level recorded before the evaluation runs ([`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md) Section 5.6), and the threshold decision follows its Section 5.7: the result is decided by where its whole reported uncertainty range lies, or by an organization-set decision rule recorded before the evaluation runs. As this framework's own additional requirement, the statistical test to be applied and the minimum sample size for the comparison are also recorded before the audit run.

### 5.6 Incident log review

The auditor reviews all AI Incident Register entries for the system covering the audit period, assessing whether:

- Incidents were classified correctly.
- Response timelines were met.
- Root cause analysis was completed.
- Corrective actions were implemented and verified.
- External reporting obligations were met where applicable.

---

## 6. ISO/IEC 42001:2023 certification roadmap

| Stage | Activity | Description |
|---|---|---|
| **Stage 1: Gap Assessment** | Gap assessment against ISO/IEC 42001:2023 | Conducted by a qualified assessor; outputs a gap report identifying missing policies, procedures, records, and governance structures |
| **Stage 2: AIMS Design** | AI management system (AIMS) design and documentation | Policies, procedures, registers, roles, and governance structures developed or updated to address gaps |
| **Stage 3: Stage 1 Audit** | Documentation review by certification body | External certification body reviews AIMS documentation for completeness and adequacy; issues a Stage 1 report identifying areas to address before Stage 2 |
| **Stage 4: Stage 2 Audit** | On-site or remote audit by certification body | Certification body verifies that the AIMS is implemented and operating effectively; interviews staff; reviews evidence; assesses conformity with ISO/IEC 42001:2023 |
| **Stage 5: Certification** | ISO/IEC 42001:2023 certificate issued | Issued upon satisfactory completion of Stage 2 audit; typically valid for three years subject to annual surveillance |
| **Stage 6: Annual Surveillance** | Annual surveillance audits | Certification body conducts annual surveillance to confirm ongoing conformity; findings are reported and remediated |
| **Stage 7: Recertification** | Three-year recertification audit | Full recertification audit every three years; scope may be broadened to include new AI systems or capabilities added since initial certification |

### 6.1 Certification body requirements (ISO/IEC 42006:2025)

Stages 3 to 7 are performed by an external certification body, whose competence and conduct are governed by ISO/IEC 42006:2025, which adds requirements to ISO/IEC 17021-1:2015 for bodies auditing and certifying an AI management system against ISO/IEC 42001:2023. When selecting and engaging a certification body, the organization confirms:

- **Impartiality and no consulting (ISO/IEC 42006:2025 §5.2.2).** The body must not have provided the organization consulting on AI, information security, data protection, or risk management, and must not have carried out the organization's internal audits; the internal-audit restriction cannot be circumvented by renaming the activity.
- **Auditor competence and qualification (§7.1.3, §7.2.2).** The audit team collectively must be competent across artificial intelligence, the audited activity, management systems, and auditing principles; individual auditors must meet the standard's education, workplace-experience, training, and prior-audit thresholds.
- **Audit time (Annex A, normative).** The body sets audit duration per the Annex A calculation (scaled by the number of persons in the AI life cycle and the AIMS role, and adjusted for regulatory frameworks, the number and risk of the AI systems, third-party agreements, and the Statement of Applicability control count); the total audit time cannot be reduced by reallocating it within the audit team. Surveillance is approximately one third, and recertification at least two thirds, of the initial audit time.
- **Two-stage initial audit (§9.3.2).** Stage 3 (documentation review) and Stage 4 (implementation audit) above correspond to the standard's stage 1 and stage 2; the body reviews the stage 1 report before proceeding to stage 2, and stage 2 confirms that the AIMS is effectively implemented and that the organization adheres to its own policies, objectives, and procedures.

An ISO/IEC 42001:2023 AIMS certificate issued under ISO/IEC 42006 is a management-system certification. It is distinct from, and does not substitute for, the EU AI Act per-system conformity assessment in Section 7, and the AIMS certificate does not authorize product, process, or service conformity labelling.

---

## 7. High-risk AI act conformity assessment

### 7.1 Self-assessment vs. third-party notified body

Under EU AI Act Art. 43, the conformity-assessment route for Annex III high-risk AI systems depends on the category:

- For AI systems in Annex III point 1 (biometrics), where the provider has applied the relevant harmonized standards or, where applicable, common specifications, the provider must choose either internal control (Annex VI) or an assessment involving a notified body (Annex VII), per Article 43(1). Notified-body assessment (Annex VII) is instead mandatory in any of the four Article 43(1) cases: the harmonized standards do not exist and common specifications are not available; the provider has not applied, or has applied only part of, the harmonized standard; applicable common specifications exist but have not been applied; or a harmonized standard has been published with a restriction, for the restricted part.
- For AI systems in Annex III points 2 to 8, internal control (Annex VI) is the default; the Commission may, by delegated act under Article 43(6), subject those categories to Annex VII assessment or parts of it.

Where the organization acts as a deployer of a high-risk system rather than the provider, it relies on the provider's conformity assessment documentation, supplemented by its own deployer obligations assessment.

### 7.2 Documentation requirements: EU AI act annex IV

For high-risk AI systems where the organization is the provider, Annex IV technical documentation must include:

- A general description of the AI system, its intended purpose, and the version.
- A description of the system's design, including model architecture, training methodology, and key design choices.
- A description of the training, validation, and testing data and procedures.
- A description of the risk management system applied throughout the lifecycle.
- A description of human oversight measures and their implementation.
- Performance metrics and results of validation and testing.
- A declaration of conformity.

The CISO is responsible for ensuring Annex IV documentation is maintained and updated following any substantial modification.

### 7.3 Registration in the EU database

High-risk AI systems within scope of EU AI Act Art. 49 registration obligations must be registered in the EU database for high-risk AI systems (Art. 71) by the provider before the system is placed on the market or put into service. The AI System Owner initiates and maintains the registration, with Legal support.

---

## 8. Post-market monitoring obligations

### 8.1 Monitoring plan

Each high-risk AI system in production must have a documented post-market monitoring plan that specifies:

- Performance metrics to be monitored (accuracy, precision, recall, F1, or task-appropriate equivalents).
- Drift detection thresholds for data drift and concept drift.
- Bias monitoring approach including protected characteristics monitored and alerting thresholds.
- Monitoring frequency and tooling.
- The responsible party for reviewing monitoring outputs.
- Escalation path when thresholds are breached.

### 8.2 Serious incident reporting

Where post-market monitoring or any other signal identifies a serious incident as defined under EU AI Act Art. 3(49), the following reporting timeline applies. Article 73 is in Chapter IX, which follows the general application date of 2 August 2026 (Article 113, second paragraph). The amended Article 113, third paragraph, point (c), defers only Chapter III, Sections 1 to 3 (except Article 6(5)): to 2 December 2027 for Article 6(2)/Annex III systems and to 2 August 2028 for Article 6(1)/Annex I systems. Article 73 binds providers of high-risk AI systems placed on the Union market, and the Article 6 classification rules are in the deferred Section 1. The held texts do not settle whether Article 73 reaches a given system before those dates, so Legal confirms the position, and until then the organization applies this timeline to every serious incident. The deployer's Article 26(5) notification, and its fallback to Article 73 when the provider cannot be reached, are Chapter III, Section 3 duties that apply from those dates; before then, deployer escalation is an organizational control.

Where the organization acts as a deployer of a high-risk AI system and identifies a serious incident, it immediately notifies first the provider, then the importer or distributor and the relevant market surveillance authorities under Article 26(5); the duty does not cover sensitive operational data of deployers that are law enforcement authorities (Article 26(5)); whether this also limits a fallback report made under Article 73 is not settled by the held text, and Legal confirms it. If the organization cannot reach the provider, the Article 73 procedure applies to it mutatis mutandis (Article 26(5)), and, as reasoning rather than express text, applying Article 73(1) mutatis mutandis (Article 26(5)), it reports, subject to the separate-entity case below, to the market surveillance authorities of the Member States where the incident occurred. Article 26(5) applies Article 73 without limiting it to particular paragraphs, so Article 73(10) also applies: where the high-risk AI system is a safety component of a device, or is itself a device, covered by Regulations (EU) 2017/745 and (EU) 2017/746, the organization's fallback notification is limited to the serious incidents referred to in Article 3, point (49)(c), and, subject to the separate-entity case below, is made to the national competent authority chosen for that purpose by the Member States where the incident occurred. For the same reason Article 73(9) also applies, although its condition concerns the provider: where the high-risk AI system is referred to in Annex III and is placed on the market or put into service by a provider subject to Union legislative instruments laying down reporting obligations equivalent to those set out in the EU AI Act, the organization's fallback notification is limited to the serious incidents referred to in Article 3, point (49)(c); Article 73(9) names no recipient, so the fallback report goes to the recipient set out in this paragraph, subject to the separate-entity case below. The Article 75(1a) route set out here names providers; Article 75(1) applies the AI Office's exclusive competence for supervision and enforcement to the deployers of the systems it lists "only when they are also the provider or form part of the same undertaking as the provider"; as reasoning, since Article 75(1a) names only providers, a deployer's fallback report follows Article 73 (Article 26(5)), subject to the separate-entity case below. Where the organization is itself the provider, it reports as provider on whichever provider route applies (for a high-risk AI system placed on the Union market and outside the AI Office's Article 75(1) competence, to the market surveillance authorities of the Member States where the incident occurred, Article 73(1), subject to the Article 73(10) and 73(9) limits below; for a system subject to the AI Office's competence under Article 75(1), to the AI Office by way of derogation from Article 73, with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated, Article 75(1a)); where neither applies, for example a system it only puts into service for its own use outside the AI Office's Article 75(1) competence, Legal confirms the route. For a deployer of a system within the AI Office's Article 75(1) competence that is a separate entity in the provider's undertaking, the held texts do not state the recipient of a fallback report; Legal confirms it. Providers of high-risk AI systems placed on the Union market otherwise report to the market surveillance authorities of the Member States where the incident occurred (Article 73(1)), while, by way of derogation from Article 73, a provider of a high-risk AI system subject to the AI Office's competence under Article 75(1) reports any serious incident to the AI Office, with Article 73(2) to (9) applying mutatis mutandis (Article 75(1a)). The AI Office promptly transmits the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated. For providers of high-risk AI systems placed on the Union market that report under Article 73(1), where the high-risk AI system is a safety component of a device, or is itself a device, covered by Regulations (EU) 2017/745 and (EU) 2017/746, the notification is limited to the serious incidents referred to in Article 3, point (49)(c), and is made to the national competent authority chosen for that purpose by the Member States where the incident occurred (Article 73(10)). For providers of high-risk AI systems placed on the Union market that report under Article 73(1), where the system is referred to in Annex III and the provider placing it on the market or putting it into service is subject to Union legislative instruments laying down reporting obligations equivalent to those set out in the EU AI Act, the notification of serious incidents is limited to those referred to in Article 3, point (49)(c) (Article 73(9)); Article 73(9) names no recipient, so the report goes to the recipient that Article 73(1) or, where it applies, Article 73(10) names. Article 75(1a) applies Article 73(2) to (9) mutatis mutandis, so Article 73(9) also applies on the Article 75(1a) route, where the notification still goes to the AI Office. The recipient column distinguishes the provider and deployer routes:

| Incident Type | Reporting Deadline | Report Recipient (subject to the Article 73(10) and 73(9) limits in the note below the table) |
|---|---|---|
| Serious incident, general case (serious harm to a person's health; infringement of obligations under Union law protecting fundamental rights; serious harm to property or the environment) | Immediately after establishing a causal link, or its reasonable likelihood, and no later than 15 days of becoming aware, the period taking account of the severity of the serious incident (Art. 73(2)) | Provider of a high-risk AI system subject to the AI Office's competence under Article 75(1): AI Office, by way of derogation from Article 73, with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated (Article 75(1a)); any other provider of a high-risk AI system placed on the Union market: market surveillance authorities of the Member States where the incident occurred (Article 73(1)). Deployer fallback, as reasoning (Article 73(1) applied mutatis mutandis by Article 26(5)): those market surveillance authorities (where the deployer is itself the provider, whichever provider route applies, or, where neither applies, the route Legal confirms; for a separate deployer in the provider's undertaking of a system within Article 75(1) competence, Legal confirms the recipient). |
| Widespread infringement, or a serious and irreversible disruption of the management or operation of critical infrastructure (Art. 3(49)(b)) | Immediately, and no later than 2 days of becoming aware (Art. 73(3)) | Provider of a high-risk AI system subject to the AI Office's competence under Article 75(1): AI Office, by way of derogation from Article 73, with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated (Article 75(1a)); any other provider of a high-risk AI system placed on the Union market: market surveillance authorities of the Member States where the incident occurred (Article 73(1)). Deployer fallback, as reasoning (Article 73(1) applied mutatis mutandis by Article 26(5)): those market surveillance authorities (where the deployer is itself the provider, whichever provider route applies, or, where neither applies, the route Legal confirms; for a separate deployer in the provider's undertaking of a system within Article 75(1) competence, Legal confirms the recipient). |
| Death of a person | Immediately after establishing, or as soon as suspecting, a causal relationship, and no later than 10 days of becoming aware (Art. 73(4)) | Provider of a high-risk AI system subject to the AI Office's competence under Article 75(1): AI Office, by way of derogation from Article 73, with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated (Article 75(1a)); any other provider of a high-risk AI system placed on the Union market: market surveillance authorities of the Member States where the incident occurred (Article 73(1)). Deployer fallback, as reasoning (Article 73(1) applied mutatis mutandis by Article 26(5)): those market surveillance authorities (where the deployer is itself the provider, whichever provider route applies, or, where neither applies, the route Legal confirms; for a separate deployer in the provider's undertaking of a system within Article 75(1) competence, Legal confirms the recipient). |
| Near-miss or significant malfunction that could lead to a serious incident if not addressed | Internal escalation without undue delay; reported to the authority if it develops into a serious incident | If escalated to a serious incident: a provider of a high-risk AI system subject to the AI Office's competence under Article 75(1) reports to the AI Office, by way of derogation from Article 73, with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated (Article 75(1a)); any other provider of a high-risk AI system placed on the Union market reports to the market surveillance authorities of the Member States where it occurred (Article 73(1)); deployer fallback, as reasoning (Article 73(1) applied mutatis mutandis by Article 26(5)), reports to those market surveillance authorities (where the deployer is itself the provider, whichever provider route applies, or, where neither applies, the route Legal confirms; for a separate deployer in the provider's undertaking of a system within Article 75(1) competence, Legal confirms the recipient). |

For a high-risk AI system that is a safety component of a device, or is itself a device, covered by Regulations (EU) 2017/745 and (EU) 2017/746, Article 73(10) limits the provider's Article 73(1) route in the table and, as reasoning through Article 26(5) applying Article 73 mutatis mutandis, the deployer's fallback, as stated above: only Article 3, point (49)(c) incidents are notified, to the national competent authority chosen for that purpose by the Member States where the incident occurred (for a separate deployer in the provider's undertaking of a system within Article 75(1) competence, Legal confirms the recipient). For a high-risk AI system referred to in Annex III that is placed on the market or put into service by a provider subject to Union legislative instruments laying down reporting obligations equivalent to those set out in the EU AI Act, Article 73(9) limits the provider's Article 73(1) route and, because Article 75(1a) and Article 26(5) apply Article 73 as stated above, the provider's Article 75(1a) route and the deployer's fallback to Article 3, point (49)(c) incidents; Article 73(9) names no recipient, so the recipient column applies or, where Article 73(10) applies, the national competent authority it names, with the same separate-entity exception.

The CISO is responsible for preparing and submitting reports, in coordination with Legal. Reports are logged in the AI Incident Register.

### 8.3 Substantial modification

Where a substantial modification is made to a high-risk AI system (including changes to the training data, model architecture, or intended purpose that affect the system's conformity with EU AI Act requirements), the conformity assessment process must be re-initiated. The CISO determines whether a full re-assessment or a targeted assessment of the modification is required.

---

## 9. Audit findings and CAPA integration

### 9.1 Findings classification

| Finding Classification | Definition | Required Response |
|---|---|---|
| **Critical** | A finding that indicates a high likelihood of serious harm to individuals, a breach of a mandatory regulatory obligation, or a systemic failure of a key control | Deployment must be suspended or human oversight significantly increased pending remediation; CAPA raised within 2 business days; AIGC notified |
| **High** | A significant control gap or evidence of non-compliance that materially increases risk but does not require immediate suspension | CAPA raised within 5 business days; remediation plan with target date approved by CISO; progress reported to AIGC at next scheduled meeting |
| **Medium** | A control weakness or documentation deficiency that could lead to a higher finding if not addressed | CAPA raised within 10 business days; resolved within agreed timeline not exceeding 90 days |
| **Low** | An observation or improvement opportunity with limited risk impact | Noted in the audit report; assigned to AI System Owner for resolution within the next review cycle |

### 9.2 CAPA process

Each finding classified as Critical, High, or Medium generates a formal CAPA record. The CAPA record documents:

- The finding, including the control or requirement that was not met.
- Root cause analysis.
- Proposed corrective action and target completion date.
- Responsible owner.
- Verification method: how the CISO will confirm the corrective action has been implemented effectively.

CAPAs are tracked in the organization's CAPA management system and reviewed at each AIGC quarterly meeting. Overdue CAPAs are escalated to the CIO.

---

## 10. Framework alignment

| Framework / Standard | Relevant Requirements | Section Addressed |
|---|---|---|
| ISO/IEC 42001:2023 §9.2.1-9.2.2 | Internal audit programme; audit criteria, scope, frequency, and methods | 3, 5 |
| ISO/IEC 42001:2023 §9.3.1-9.3.3 | Management review of the AIMS; inputs including audit results, incidents, performance data | 2.1, 8 |
| ISO/IEC 42006:2025 §5.2, §7.1.2-7.1.3, §9.1.4, §9.3.2 | Requirements for bodies certifying an AIMS: impartiality and no consulting, auditor competence and qualification, audit time, two-stage certification audit | 6.1 |
| EU AI Act Chapter IX | Post-market monitoring; serious incident reporting; market surveillance | 7, 8 |
| NIST AI RMF 1.0: MEASURE 1.1, 2.9, 2.11 | Metrics and methods for assessing AI risk; bias and fairness evaluation; explainability | 4, 5.5 |
| NIST AI RMF 1.0: MANAGE 1.2, 1.4, 4.1, 4.3 | Risk treatment; incident response; CAPA; residual risk documentation | 9 |
| CSA AICM v1.1 A&A-01 through A&A-06 | Audit and assurance controls: independent assessments, risk-based planning, compliance verification | 3, 4, 5 |

---

**End of Document**
