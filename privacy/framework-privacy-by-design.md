# Privacy by Design Framework

**Document Title:** Privacy by Design Framework\
**Document Type:** Framework\
**Version:** 1.0.0\
**Date:** 2026-06-30\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/template-legitimate-interest-assessment.md`](template-legitimate-interest-assessment.md), [`privacy/standard-pseudonymisation-and-anonymisation.md`](standard-pseudonymisation-and-anonymisation.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`architecture/procedure-architecture-review.md`](../architecture/procedure-architecture-review.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material regulatory, jurisdictional, or product change\
**Repository Path:** [`privacy/framework-privacy-by-design.md`](framework-privacy-by-design.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This framework operationalizes the **data protection by design and by default** obligation in **GDPR Article 25** (Regulation (EU) 2016/679). It does so by mapping the seven foundational principles of privacy by design to the organisation's architecture and development-security workflows, so that data-protection measures are built into systems at the design stage rather than retrofitted.

The framework distinguishes two things that are often conflated. **GDPR Article 25 is the legal obligation**: a binding, risk-calibrated duty on the controller to implement appropriate technical and organisational measures both when the means of processing are determined and during the processing itself. **The seven foundational principles are a conceptual model** (articulated by Ann Cavoukian as "Privacy by Design") that predates the Regulation and informs how the Article 25 obligation is met in practice. The principles are not GDPR text and carry no independent legal force; they are the design philosophy this framework uses to make the Article 25 duty actionable for architects and engineers.

---

## Scope

This framework applies to the design, build, procurement, material change, and decommissioning of any system, product, service, or process that processes personal data, across all channels and jurisdictions in which the organisation operates. It applies to internally developed systems, externally hosted services, embedded or third-party components, and AI systems that process personal data.

The legal duty in Article 25 falls on the **controller**. Where the organisation acts as a processor, or procures a product or service, it applies this framework to its own design decisions and uses contractual and supplier-assessment controls to obtain equivalent assurance from producers and processors, which Recital 78 encourages but does not directly bind. This framework does not displace the lawful-basis analysis (consent, legitimate interests, contract, and the rest); it governs how, once a basis is established, the processing is designed to protect data subjects.

---

## Legal basis: GDPR Article 25

Article 25 has three operative parts, each of which this framework operationalizes.

- **Article 25(1), data protection by design.** The controller must, "both at the time of the determination of the means for processing and at the time of the processing itself, implement appropriate technical and organisational measures, such as pseudonymisation, which are designed to implement data-protection principles, such as data minimisation, in an effective manner and to integrate the necessary safeguards into the processing". The obligation is **risk-calibrated**: it is weighed against the state of the art, the cost of implementation, and the nature, scope, context, and purposes of the processing, against the risks to the rights and freedoms of natural persons.
- **Article 25(2), data protection by default.** The controller must ensure that "by default, only personal data which are necessary for each specific purpose of the processing are processed". This covers the **amount** of data collected, the **extent** of processing, the **storage period**, and **accessibility**; in particular, personal data must not, by default, be made accessible to an indefinite number of persons without the individual's intervention.
- **Article 25(3), certification.** An approved certification mechanism under Article 42 may be used as **an element** to demonstrate compliance with Article 25(1) and (2). It is evidence, not conclusive proof.

Recital 78 adds that controllers should adopt internal policies and measures that meet the by-design and by-default principles (for example minimizing processing, pseudonymizing as soon as possible, transparency, and enabling the data subject to monitor the processing), and **encourages** producers of products, services, and applications to take the right to data protection into account when developing and designing them.

---

## The seven foundational principles

The following are the seven foundational principles of privacy by design, attributed to Ann Cavoukian's framework. They are paraphrased here as the design philosophy that informs the Article 25 obligation; they are not a quotation of GDPR or of any standard, and an adopter citing them formally should reference Cavoukian's published work.

1. **Proactive, not reactive; preventative, not remedial.** Anticipate and prevent privacy-invasive events before they occur, rather than remediating after the fact.
2. **Privacy as the default setting.** No action should be required of the individual to protect their privacy; the most protective settings apply automatically. This is the principle Article 25(2) makes a legal duty.
3. **Privacy embedded into design.** Privacy is a core component of the system's design and architecture, not a bolt-on.
4. **Full functionality (positive-sum, not zero-sum).** Accommodate legitimate objectives without unnecessary trade-offs; reject the false choice between privacy and functionality.
5. **End-to-end security (full lifecycle protection).** Protect personal data across its full lifecycle, from collection through secure destruction.
6. **Visibility and transparency.** Ensure that the processing operates according to its stated purposes and is open to verification by data subjects and other stakeholders.
7. **Respect for user privacy (keep it user-centric).** Keep the interests of the individual central, with strong defaults, appropriate notice, and user-friendly controls.

---

## Mapping the principles to architecture workflows

The principles are embedded into the architecture lifecycle at defined control points, so that "privacy embedded into design" (principle 3) is a gate, not an aspiration.

| Principle | Architecture control point |
| --- | --- |
| Proactive, not reactive | A privacy-risk screen is part of solution intake; a [DPIA](template-dpia.md) is triggered before design where the processing is likely high-risk. |
| Privacy as the default | Default configurations are reviewed against Article 25(2) (amount, extent, storage, accessibility) at the architecture-review gate; the most protective configuration is the default. |
| Privacy embedded into design | The [architecture review](../architecture/procedure-architecture-review.md) includes a privacy-by-design checkpoint; a design that processes personal data does not pass review without it. |
| Full functionality | Data-minimizing and privacy-preserving design patterns (pseudonymization, aggregation, on-device processing, tokenization) are evaluated as first-class options, not as functionality trade-offs. |
| End-to-end security | The data architecture defines classification-driven controls across the lifecycle, cross-referenced to [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md) and [`architecture/standard-data-architecture.md`](../architecture/standard-data-architecture.md). |
| Visibility and transparency | The design records the data flows, purposes, and retention so the processing can be verified against its stated purpose and surfaced in the privacy notice. |
| Respect for user privacy | Data-subject-rights handling (access, objection, erasure, portability) is a design requirement, not a later addition. |

---

## Mapping the principles to development-security workflows

The principles are embedded into the secure-development lifecycle so that by-design and by-default survive implementation, not just design.

| Principle | Development-security control point |
| --- | --- |
| Proactive, not reactive | Privacy requirements are captured as acceptance criteria at the start of the build, per [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md). |
| Privacy as the default | Default-deny accessibility, minimal-scope data collection, and conservative retention defaults are implemented and tested, not left to configuration. |
| Privacy embedded into design | Privacy and security requirements are part of the developer security requirements ([`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md)), reviewed in code review. |
| Full functionality | Privacy-preserving techniques (pseudonymization per [`privacy/standard-pseudonymisation-and-anonymisation.md`](standard-pseudonymisation-and-anonymisation.md), field-level encryption, data masking in non-production) are available as reusable components. |
| End-to-end security | Secure handling spans build, test, deployment, and decommissioning; test and non-production environments must not expose production personal data. |
| Visibility and transparency | Processing and access are logged so the system's behaviour can be audited against its declared purpose. |
| Respect for user privacy | Data-subject-rights endpoints and consent or objection signals are implemented and tested against the validity standard. |

---

## Data protection by default (Article 25(2))

Independently of the design principles, every system processing personal data must satisfy the by-default obligation on four dimensions. These are the concrete, testable defaults a design must demonstrate.

| Dimension | Default requirement |
| --- | --- |
| Amount of data collected | Only the personal data necessary for each specific purpose is collected by default; optional fields are off by default. |
| Extent of processing | Processing is limited to what each purpose requires; secondary uses require a separate basis and are not enabled by default. |
| Storage period | Retention defaults to the minimum required for the purpose, per the data-retention schedule; indefinite retention is not a default. |
| Accessibility | Personal data is not, by default, made accessible to an indefinite number of persons without the individual's intervention; access defaults to least privilege. |

---

## Supporting instruments

This framework is operationalized through existing instruments rather than duplicating them.

- The **[DPIA template](template-dpia.md)** is the instrument for the Article 25(1) risk assessment where processing is likely to be high-risk.
- The **[Legitimate Interest Assessment template](template-legitimate-interest-assessment.md)** is the design-stage lawful-basis assessment where Article 6(1)(f) is relied on; data minimization tested there feeds the by-default analysis.
- The **[pseudonymisation and anonymisation standard](standard-pseudonymisation-and-anonymisation.md)** specifies the named Article 25(1) example measure.
- The **[data classification and handling standard](../security/standard-data-classification-and-handling.md)** drives the lifecycle controls behind end-to-end security.
- The **[privacy and data governance policy](policy-privacy-and-data-governance.md)** is the parent policy whose privacy-by-design-and-default commitment this framework operationalizes, and the **[privacy management programme charter](charter-privacy-management-programme.md)** is the accountability anchor.

---

## Operating expectations

1. A design that processes personal data does not pass architecture review without a completed privacy-by-design checkpoint; the reviewing role records the outcome.
2. Where the processing is likely high-risk, a DPIA is completed before the design is approved, not after launch.
3. Default configurations are evidenced against the four Article 25(2) dimensions before release, and the evidence is retained.
4. Material changes to an existing system re-trigger the privacy-by-design checkpoint scoped to the change.
5. The DPO reviews privacy-by-design outcomes for high-risk systems and is consulted on the design where the residual risk is material.
6. Certification under Article 42, where the organisation holds it, is recorded as supporting (not conclusive) evidence of Article 25 compliance.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Design-stage privacy coverage | Percentage of in-scope designs with a completed privacy-by-design checkpoint before approval | 100% |
| DPIA timeliness | Percentage of high-risk processing with a DPIA completed before design approval | 100% |
| By-default evidence | Percentage of releases with retained evidence against the four Article 25(2) dimensions | At least 95% |
| Retrofit rate | Count of privacy controls added after launch that should have been designed in | Trending to zero |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 25(1), (2), (3); Recital 78 | Data protection by design and by default; the legal obligation this framework operationalizes |
| GDPR | Article 42 | Certification as an element of demonstrating Article 25 compliance |
| UK GDPR | Article 25 | Equivalent data-protection-by-design-and-default obligation for UK-scoped processing |
| Privacy by Design (Cavoukian) | The seven foundational principles | The conceptual model mapped to architecture and development-security workflows; informs, but is distinct from, the Article 25 legal duty |
| ISO/IEC 27701:2025 | Privacy information management | The PIMS control environment within which by-design measures are implemented and reviewed |
| ISO/IEC 29134:2017 | Privacy impact assessment guidance | Methodology supporting the Article 25(1) risk assessment carried out through the DPIA |

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. Adopting organisations must integrate the architecture-review and secure-development control points with their own lifecycle tooling, calibrate the risk thresholds that trigger a DPIA, and validate the requirements against the obligations of their applicable jurisdictions and sectoral regulators. The seven foundational principles are attributed to Ann Cavoukian's published framework and are paraphrased here; an organisation quoting them should cite that work directly. This framework is not a substitute for legal advice, and the certification mechanism in Article 25(3) is available only where an approved Article 42 scheme exists for the processing in question.

---

**End of Document**
