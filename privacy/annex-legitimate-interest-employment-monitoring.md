# Legitimate Interest Assessment for Employment Monitoring Annex

**Document Title:** Legitimate Interest Assessment for Employment Monitoring Annex\
**Document Type:** Annex\
**Version:** 0.1.0\
**Date:** 2026-09-04\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/template-legitimate-interest-assessment.md`](template-legitimate-interest-assessment.md), [`security/policy-workforce-network-monitoring.md`](../security/policy-workforce-network-monitoring.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/framework-consent-management.md`](framework-consent-management.md), [`privacy/standard-presence-inference-limitations.md`](standard-presence-inference-limitations.md), [`privacy/standard-network-telemetry-and-dpi-controls.md`](standard-network-telemetry-and-dpi-controls.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/standard-pseudonymization-and-anonymization.md`](standard-pseudonymization-and-anonymization.md), [`security/framework-insider-risk-programme.md`](../security/framework-insider-risk-programme.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, employment-law, framework, or monitoring-technology change\
**Repository Path:** [`privacy/annex-legitimate-interest-employment-monitoring.md`](annex-legitimate-interest-employment-monitoring.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This annex specializes the general Legitimate Interest Assessment (LIA) method for one context: the monitoring of personnel and their devices on organization systems and networks. It operationalizes, for that context, the three-part test defined in the [Legitimate Interest Assessment (LIA) Template](template-legitimate-interest-assessment.md), and it is the privacy-analysis companion to the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md).

Employment monitoring sits on a difficult lawful-basis footing. The employer-employee relationship carries an imbalance of power that makes consent an unreliable basis, so monitoring generally relies on the legitimate-interests basis (GDPR Article 6(1)(f)) or another basis, and reliance on that basis is available only through a documented balancing analysis. This annex sets out how each part of the LIA test is applied when the interest pursued is a security, integrity, availability, or compliance aim and the individuals whose data is processed are the organization's own workforce.

This annex supports the LIA template; it does not restate the template's generic method. Where a step is fully covered by the template, this annex points to it and adds only what the monitoring context changes.

---

## 2. Scope

### 2.1 In scope

1. The legitimate-interests balancing analysis for monitoring capabilities that process the personal data of employees, contractors, consultants, and any other personnel authorized to access organization systems, networks, or data.
2. The reasons consent is presumptively not a valid lawful basis for employment monitoring, and the consequences for basis selection (Section 5).
3. The application of the three-part legitimate-interests test to monitoring (Section 6), the balancing factors that turn on workforce reasonable expectations (Section 6.3), and the right to object (Section 7).
4. The EU and United Kingdom regime distinctions that bear on basis selection for monitoring (Section 8).

### 2.2 Out of scope

1. **What monitoring is permitted, and whether a capability may collect at all.** The [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) is the authority for the permitted monitoring, the necessity and proportionality determination, transparency, and the prohibited uses. This annex informs the lawful-basis determination that policy (Section 4) requires; it does not authorize any monitoring.
2. **Routine HR and performance management.** Consistent with the parent policy (Section 2.2), routine HR and performance management is governed by the organization's HR management processes and is expressly not a purpose of the monitoring analyzed here. This annex does not supply, and must not be read as supplying, a performance-management model.
3. **The technical configuration of monitoring telemetry**, which the [Network Telemetry and DPI Controls Standard](standard-network-telemetry-and-dpi-controls.md) governs, and **the interpretation of presence signals as a measure of work**, which the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md) governs.
4. **Bases other than legitimate interests.** Where a monitoring capability relies on a legal-obligation basis, or another Article 6 basis, this annex's balancing analysis does not apply to that basis; the applicable basis and its own conditions govern.

---

## 3. Definitions

| Term | Definition |
| --- | --- |
| Legitimate Interest Assessment (LIA) | The documented three-part test (purpose, necessity, balancing) an organization completes before relying on the legitimate-interests lawful basis under GDPR Article 6(1)(f), as defined in the [Legitimate Interest Assessment (LIA) Template](template-legitimate-interest-assessment.md). |
| Legitimate interests (Article 6(1)(f)) | The lawful basis permitting processing "necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject". |
| Reasonable expectations | What an employee could reasonably expect regarding monitoring, given the workplace context, what was disclosed in advance, the nature and intrusiveness of the monitoring, and whether personal use of the resource is permitted; a central factor in the balancing test. |
| Special-category data | Personal data that, under the applicable regime, concerns categories protected at a heightened level (for example health, racial or ethnic origin, religious or philosophical beliefs, political opinions, trade-union membership, genetic data, biometric data processed for the purpose of uniquely identifying a natural person, or data concerning sex life or sexual orientation). |

---

## 4. Relationship to the parent policy and to the LIA template

1. **This annex implements, and does not supersede, its parent.** The [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) is the authority for the monitoring programme, its lawful-basis posture (Section 4 of that policy), and its prohibited uses. This annex adds the specialized balancing analysis under that authority. Where this annex and the parent policy (or another authoritative document, including a specific legal obligation) appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.
2. **This annex specializes the LIA template; it does not duplicate it.** The [Legitimate Interest Assessment (LIA) Template](template-legitimate-interest-assessment.md) is the instrument that records and evidences an assessment. A monitoring LIA is completed on that template; this annex tells the assessor how each part of the template's Section 2 test is worked for the monitoring context. The completed LIA is a working document, and populated assessments are stored under an appropriate confidentiality classification, per the template.
3. **A stated aim is not a lawful basis, and this annex does not establish one.** Consistent with the parent policy (Section 3), a legitimate security aim is necessary but not sufficient: a separate lawful basis under the applicable privacy and employment law is required for each capability that processes personal data, and the purpose pursued and the Article 6 basis relied on are stated separately in the LIA.

---

## 5. Consent is presumptively not a valid lawful basis in employment

1. **The imbalance of power makes employment consent presumptively invalid.** Consent is a valid lawful basis only where it is freely given, and in the employment relationship it is unlikely to be. The European Data Protection Board's Guidelines 05/2020 on consent under Regulation 2016/679 (Version 1.0, adopted 4 May 2020) explain that an imbalance of power arises in the employment context: given the dependency that results from the employer-employee relationship, it is unlikely that an employee can refuse an employer's request for consent to data processing (for example the activation of monitoring systems) without fear or real risk of detrimental effects from a refusal. The EDPB accordingly deems it problematic for employers to process employee personal data on the basis of consent, and states that for the majority of such data processing at work the lawful basis cannot and should not be the consent of the employees (Article 6(1)(a)). This tracks the freely-given and conditionality requirements the [Consent Management Framework](framework-consent-management.md) enforces.
2. **The supervisory position on data processing at work is long-standing.** The held EDPB Guidelines 05/2020 draw on and carry forward the earlier Article 29 Working Party analysis of data processing at work; this annex relies on the held Guidelines 05/2020, which is the source cited for the imbalance-of-power analysis in item 1.
3. **Monitoring therefore relies on legitimate interests or another basis, not consent.** Because employee consent is presumptively not freely given, workforce monitoring generally relies on the legitimate-interests basis (Article 6(1)(f)) or another basis (for example a legal obligation), and the lawful basis for each capability is documented by the Data Protection Officer per the parent policy (Section 4). Consent is not the default basis for monitoring, and the presumption against it is not overcome by presenting a monitoring notice for signature, by an acceptable-use acknowledgement, or by continued employment.
4. **Defective consent cannot be repurposed.** Where a monitoring capability would process special-category data, the Article 9 prohibition applies (Section 8), and consent that is invalid because it is not freely given cannot be relied on as the Article 9(2) explicit-consent condition either. A basis that fails at Article 6 is not rehabilitated by re-labelling it at Article 9.
5. **Reliance on legitimate interests does not license covert monitoring.** Transparency is both a parent-policy requirement (Section 5) and a balancing safeguard here (Section 6.3). Covert monitoring is prohibited by the parent policy (Section 7) and by the [Insider Risk Programme Framework](../security/framework-insider-risk-programme.md); a legitimate-interests basis does not reintroduce covert monitoring as a standing capability.

---

## 6. The three-part legitimate-interests test applied to monitoring

The three parts are cumulative: the basis is available for a monitoring capability only where all three pass. This section specializes the template's Section 2 test; the assessor records the analysis on the template.

### 6.1 Purpose test (is there a legitimate interest?)

1. **State the specific interest, and who pursues it.** The interest is articulated precisely, not as "monitoring in general". For workforce monitoring the interest is typically the security, integrity, availability, or legal-and-regulatory-compliance aim the parent policy (Section 3) requires the capability to serve, or the protection of the organization and its personnel from harm; the interest is stated as that specific aim, and the controller (or a named third party) pursuing it is identified.
2. **The interest is lawful, clearly articulated, and real and present.** A speculative or open-ended interest ("it may be useful later") does not pass; the parent policy forbids collection on that footing (Section 3, item 5).
3. **The purpose is not the basis.** The purpose test identifies a legitimate interest; it does not by itself satisfy Article 6. Passing the purpose test is a precondition for the necessity and balancing tests, not a substitute for them.

### 6.2 Necessity test (is the monitoring necessary?)

1. **The monitoring must actually serve the interest, and there must be no less intrusive means.** Consistent with the parent policy (Section 3, items 2 and 3), the assessor confirms that the capability advances the stated aim and that the aim cannot reasonably be achieved by a less intrusive option: metadata rather than content, aggregate rather than individual signals, targeted rather than blanket collection. Where a less intrusive means would achieve the aim, the monitoring is not necessary within the meaning of Article 6(1)(f).
2. **Data minimization bounds the collection.** The capability collects the minimum data necessary for its stated aim (GDPR Article 5(1)(c)); this is the same minimization the parent policy (Section 3, item 5) requires, assessed here as part of necessity.
3. **Content inspection is the exceptional case.** Continuous or blanket inspection of communication content is not a baseline necessity; it is the exceptional measure the parent policy (Section 4, item 6) subjects to specific, documented approval, and it is never applied to legally privileged or protected communications.

### 6.3 Balancing test (do the workforce's interests, rights, and freedoms override?)

The balancing test weighs the identified interest against the interests, fundamental rights, freedoms, and reasonable expectations of the affected personnel. The interest prevails only where it is not overridden after the committed safeguards are applied.

**Reasonable-expectation factors.** In the employment context, the balance turns substantially on what personnel could reasonably expect. The assessor weighs at least the following:

| Factor | What it weighs |
| --- | --- |
| Advance disclosure | Whether the monitoring was disclosed to personnel in advance and on an ongoing basis (through the parent policy, the acceptable-use policy, and the applicable privacy notice). Undisclosed monitoring defeats reasonable expectations and weighs heavily against the interest. |
| Nature, scope, and intrusiveness | Whether the monitoring operates on connection metadata and security signals or on communication content; whether it is targeted or blanket; and how continuous and granular it is. Greater intrusiveness weighs against the interest. |
| Personal use of the resource | Whether personal use of the monitored resource is permitted or tolerated. Where personal use is permitted, personnel have a stronger expectation of privacy in that use, which weighs against intrusive monitoring of it. |
| Workplace context | The nature of the role, the sensitivity of the systems accessed, the location of the activity (office, home, or travel), and the applicable workplace norms and any collective agreements. |
| Category and sensitivity of the data | Whether the monitoring may capture or reveal special-category data (Section 8) or data about identifiable individuals in sensitive circumstances. Sensitive data weighs against the interest and may require exclusion by design. |
| Impact and potential for harm | The consequences to personnel of the monitoring and of any action taken on its signals, including the risk of the signals being repurposed. The parent policy's prohibitions (Section 7) bound this: monitoring signals must not drive automated discipline or serve as a productivity metric. |

**Balancing safeguards, and the baseline they build on.** A distinction matters here. Measures the organization is legally required to adopt regardless (transparency and advance notice, the right to object under Section 7, purpose limitation and the prohibition on secondary-purpose creep, role-restricted, logged, and reviewed access under the parent policy Section 9, and minimized retention under the parent policy Section 8) are obligations that must be met, but, being required by law in any event, they do not by themselves tip an otherwise failing balance in the interest's favour (EDPB Opinion 28/2024: mitigating measures are not to be confused with the measures a controller is legally required to adopt anyway). The balance instead turns on safeguards that reduce the impact on personnel beyond that legal baseline: serving the aim in pseudonymized or aggregate form where it can be, excluding special-category-revealing data by design, collecting less or less granularly than the law would strictly permit, and offering and acting on the right to object more readily than the minimum requires. Pseudonymization and aggregation reduce, but do not eliminate, re-identification risk (residual linkage, inference, and singling-out risk remains), and the residual risk is assessed under the [Pseudonymization and Anonymization Standard](standard-pseudonymization-and-anonymization.md) (Section 5.3, re-identification risk assessment), not assumed away.

**Vulnerable individuals.** Where the affected personnel include individuals in a position of particular vulnerability, that weighs against the interest and is recorded in the balancing.

---

## 7. The right to object (GDPR Article 21)

1. **The right attaches to the basis.** Where a monitoring capability relies on Article 6(1)(f), the affected individual has the right under GDPR Article 21(1) to object, on grounds relating to their particular situation, to the processing. On an objection, the organization stops the processing of that individual's data unless it demonstrates compelling legitimate grounds that override the individual's interests, rights, and freedoms, or the processing is for the establishment, exercise, or defence of legal claims.
2. **The right is surfaced prominently.** Consistent with GDPR Article 21(4), the right to object is brought explicitly to the individual's attention and presented clearly and separately from other information, at the latest at the first communication with the individual. The privacy notice and the monitoring notice surface it; a right buried in a general acknowledgement is not surfaced.
3. **Objections are handled, not deferred.** An objection to a monitoring capability is assessed on its particular grounds, and the outcome (cessation, or a recorded demonstration of overriding compelling grounds) is documented and fed back into the balancing for that capability. Handling follows the organization's data-subject-rights process.

---

## 8. Regime specifics: the EU and United Kingdom, and special-category data

The lawful-basis analysis is worked separately for the EU and United Kingdom regimes; the two are not conflated.

1. **EU: Article 6 basis, and Article 9 where special-category data is involved.** Under the GDPR, monitoring that processes personal data requires an Article 6 basis (typically Article 6(1)(f), assessed as above). Processing of special-category data is prohibited by Article 9(1) unless an Article 9(2) condition applies in addition to the Article 6 basis. Explicit consent is one of the Article 9(2) conditions, not the only one, and in employment it is subject to the same freely-given problem as Article 6 consent (Section 5); the applicable Article 9(2) condition is identified explicitly and is not presumed to be consent. Biometric data is special-category data only when it is processed for the purpose of uniquely identifying a natural person (the Article 9(1) qualifier). Employment-context processing may additionally be subject to more specific national rules that Member States are permitted to introduce under GDPR Article 88.
2. **United Kingdom: an Article 6 basis, a UK GDPR Article 9 condition, and, for several, a DPA 2018 Schedule 1 condition.** Under UK GDPR, monitoring that processes personal data requires an Article 6 basis; processing of special-category data requires a UK GDPR Article 9 condition in addition, and for several of those conditions an associated Data Protection Act 2018 Schedule 1 condition (often including an Appropriate Policy Document). The UK conditions are set under the UK regime and are not identical to the EU conditions. Under UK GDPR, Article 88 is not adopted, so there is no UK employment-specific Article 88 regime; UK employment monitoring relies on the general lawful-basis analysis above rather than on Article 88 national rules (see the United Kingdom privacy annex).
3. **Automated decisions are a separate right, worked separately per regime.** Where a monitoring signal could feed a solely automated decision with legal or similarly significant effect, the automated-decision-making rules apply in addition to the lawful-basis analysis, and the parent policy prohibits monitoring signals from triggering employment action automatically (Section 7). Under the GDPR this is Article 22; under UK GDPR, following the Data (Use and Access) Act 2025 (in force 5 February 2026), Article 22 is replaced by Articles 22A to 22D (see the United Kingdom privacy annex). The EU and UK automated-decision regimes are not cited under a single combined shorthand.

---

## 9. Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Data Protection Officer (DPO)** | Independently advises on, reviews, and monitors the legitimate-interests analysis, the balancing test, and the impact assessment for each monitoring capability, and advises on basis selection (including that consent is presumptively not a valid basis for employment monitoring). Acting as an independent adviser and monitor, the DPO does not determine or approve monitoring measures and is not a joint approver of them. |
| **Chief Information Security Officer (CISO)** | Owns the parent monitoring policy; approves monitoring capabilities and their aims; provides the security-aim and necessity input that the purpose and necessity tests rely on. |
| **Legal Counsel** | Advises on the applicable employment, privacy, and consultation law across the organization's footprint, including the EU and United Kingdom regime distinctions and any works-council or codetermination requirements. |
| **HR / People Operations** | Confirms that monitoring signals are not used for automated discipline or as a productivity metric, and coordinates workforce notice and consultation that the balancing relies on. |
| **Capability owner** | Provides the specific aim, data categories, necessity rationale, retention, and access controls for the capability being assessed. |

---

## 10. Framework alignment

The table maps only the controls this annex substantively implements or constrains.

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR (EU) | Article 6(1)(f) legitimate interests; Article 5(2) accountability; Article 21 right to object; Article 9 special-category prohibition (absent an Article 9(2) condition); Article 88 employment-context processing | The legitimate-interests basis this annex's balancing analysis evidences, the accountability the documented assessment provides, the right to object that attaches to the basis, and the special-category and employment-context constraints on basis selection. These provisions inform the annex; the annex does not assert that any single article prescribes the specific balancing factors. |
| UK GDPR | Article 6(1)(f) legitimate interests; Article 9 condition plus, for several, a Data Protection Act 2018 Schedule 1 condition; Article 88 not adopted; Article 22 replaced by Articles 22A to 22D (DUAA 2025, in force 2026-02-05); see the United Kingdom privacy annex | The UK basis, special-category, and automated-decision positions differ from the EU regime and are worked separately; do not conflate the two regimes. |
| EDPB Guidelines 05/2020 (Version 1.1) | Guidelines 05/2020 on consent under Regulation 2016/679 | The supervisory basis for the presumption that employment consent is not freely given, given the imbalance of power (Section 5). |
| EDPB Opinion 28/2024 | Legitimate-interest analysis (three cumulative conditions) | Articulates the three cumulative conditions (purpose, necessity, balancing) that this annex specializes for monitoring. |
| ISO/IEC 27001:2022 | A.5.34 Privacy and protection of personal identifiable information (PII) | Bounds the handling of personal data processed under a monitoring legitimate-interests basis. |
| NIST CSF 2.0 | GV.OC Organizational Context; GV.PO Policy | Governs the legal-and-regulatory-context understanding and the policy constraints within which the lawful-basis determination is made. |
| CSA CCM v4.1 | DSP-12 Limitation of Purpose in Personal Data Processing; DSP-08 Data Privacy by Design and Default | Purpose limitation on monitoring data and privacy-by-default in the balancing safeguards. |

---

## 11. Limitations

This annex is a CC BY-SA 4.0 baseline. It specializes the legitimate-interests balancing analysis for employment monitoring; it does not authorize any monitoring, does not itself establish a lawful basis, and does not define the productivity or performance measures an organization uses (which belong to legitimate, human-led performance management outside this annex's scope). The authority for what monitoring is permitted is the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); the instrument that records an assessment is the [Legitimate Interest Assessment (LIA) Template](template-legitimate-interest-assessment.md). Adopting organizations must validate the framework mappings and the applicable employment, privacy, and consultation law for their jurisdictions, including the EU and United Kingdom distinctions in Section 8 and any works-council, trade-union, or codetermination requirements, and must obtain their own legal advice; this annex is not a substitute for legal advice, and where a supervisory authority publishes its own guidance the supervisory authority's instrument prevails to the extent of any inconsistency. This annex implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); where this annex and the parent policy or another authoritative document appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.

---

**End of Document**
