# AI Compliance Policy

**Document Title:** AI Compliance Policy\
**Document Type:** Policy\
**Version:** 1.0.9\
**Date:** 2026-07-11\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This policy establishes the organization's obligations and commitments for AI regulatory compliance. It defines the classification of AI systems, the governance structures accountable for compliance, the obligations that apply to the organization as an AI deployer and, where relevant, as a provider, and the obligations that arise under applicable national and international AI governance frameworks.

The policy is grounded in the EU AI Act 2024, ISO/IEC 42001:2023, NIST AI Risk Management Framework 1.0 (with the AI 600-1 Generative AI Profile), the OECD AI Principles (2019 Recommendation as updated 2024), and UK AI Safety Institute guidance. Canada's proposed Artificial Intelligence and Data Act (AIDA) is retained only as a lapsed planning indicator: AIDA lapsed with Bill C-27 at the January 2025 prorogation and would require reintroduction, so adopting entities treat it as a planning indicator rather than a binding instrument until reintroduced and align in the meantime to the in-force Canadian instruments set out in Section 7.2.

### 1.2 Scope

This policy applies to:

- All AI systems deployed, operated, procured, or materially configured by the organization.
- All employees, contractors, and third parties who develop, deploy, manage, or use AI systems on behalf of the organization.
- All AI system lifecycle phases: design, development, acquisition, deployment, monitoring, and retirement.
- All geographies in which the organization operates or where AI outputs are used, with specific obligations triggered by EU, UK, and Canadian jurisdictional presence.

This policy does not replace privacy, information security, or supplier governance policies. Those policies apply concurrently and their requirements must be met alongside the obligations set out here.

---

## 2. Policy statement

Senior leadership recognizes that AI systems present opportunities to improve operational efficiency, decision quality, and service delivery, and also introduce risks to individuals, society, and the organization if deployed without adequate governance.

The organization commits to:

- Deploying AI systems in a manner that is lawful, transparent, accountable, and respectful of fundamental rights.
- Classifying AI systems according to applicable regulatory risk tiers before deployment.
- Meeting all obligations applicable to the organization as a deployer of AI systems, and where applicable as a provider.
- Maintaining governance structures that can demonstrate compliance to regulators, customers, and other stakeholders.
- Embedding human oversight into high-risk AI deployments and ensuring that individuals affected by AI-assisted decisions have meaningful recourse.
- Reporting serious AI incidents to competent authorities within the timeframes prescribed by applicable law.
- Pursuing ISO/IEC 42001:2023 certification as the organization's AI management system standard.

---

## 3. Governance

### 3.1 AI governance council (AIGC)

The AI Governance Council is the organization's primary body for AI compliance oversight. It is chaired by the CISO and includes representation from the Data Protection Officer, CIO, Legal, and representatives from business functions that deploy or use AI systems. The AIGC meets at least quarterly.

### 3.2 Accountability table

| Role | AI Compliance Responsibilities |
|---|---|
| AI Governance Council (AIGC) | Owns the AI compliance programme; approves AI system classifications; reviews annual AI compliance audit findings; escalates material non-compliance to the Board |
| Chief Information Security Officer (CISO) | Leads technical AI compliance; chairs the AIGC; ensures that AI security controls align with regulatory obligations; co-ordinates AI incident response |
| Data Protection Officer | Ensures that fundamental rights impact assessments and privacy impact assessments are completed for high-risk AI systems; advises on GDPR Art. 22 (automated decision-making) and Art. 33 (personal data breach) interactions with AI incidents |
| Chief Information Officer (CIO) | Accountable for AI system infrastructure compliance; ensures that AI systems are registered and lifecycle-managed; approves significant AI system changes |
| Legal | Interprets regulatory obligations; advises on jurisdiction-specific compliance; reviews AI-generated content labelling and transparency disclosures |
| Business Unit Owners | Designate an AI system owner for each AI system under their control; ensure that staff complete required AI training; escalate AI compliance concerns to the AIGC |
| AI System Owner | Maintains the AI System Register entry; ensures that the model card and system card are current; coordinates with CISO and Data Protection Officer on impact assessments; monitors for post-market issues |

---

## 4. AI system classification

All AI systems must be classified before deployment. Classification determines the regulatory obligations and internal controls that apply. The organization uses the EU AI Act risk tier framework as the primary classification model, supplemented by NIST AI RMF risk categorization for systems not subject to EU AI Act jurisdiction.

### 4.1 Classification table

| EU AI Act Risk Tier | EU AI Act Scope | Regulatory Obligations | Organization Approach |
|---|---|---|---|
| **Prohibited** | AI systems that pose unacceptable risk: social scoring by public authorities; real-time remote biometric identification in public spaces (subject to narrow exceptions); AI exploiting vulnerabilities of specific groups; subliminal manipulation that causes harm (EU AI Act Chapter II, Article 5) | Deployment prohibited | The organization does not deploy prohibited AI systems. Any proposed use case that may fall within this tier must be referred to the AIGC and Legal before any procurement or development activity |
| **High-risk** | AI systems listed in EU AI Act Annex III: AI in critical infrastructure; educational or vocational training decisions; employment and workforce management; access to essential services; law enforcement; migration and border control; administration of justice; AI used as safety components in regulated products (Annex I) | Conformity assessment; registration in the EU database; fundamental rights impact assessment; human oversight; technical documentation (Annex IV); logging; post-market monitoring; serious incident reporting | Full compliance programme applies; AI System Impact Assessment required before deployment; annual audit; human oversight mandatory; incident reporting pathway established |
| **General-purpose AI (GPAI) model with systemic risk** | GPAI models with training compute above 10^25 FLOPs or designated by the European Commission (EU AI Act Chapter V) | Adversarial testing; incident reporting to the AI Office; cybersecurity measures; energy efficiency transparency | Where the organization deploys or integrates GPAI models meeting this threshold, it ensures that the provider's obligations are met and documents its own deployer obligations |
| **General-purpose AI (GPAI) model: standard** | GPAI models that do not meet the systemic risk threshold | Technical and copyright compliance documentation; transparency obligations | Transparency and documentation obligations met; AI System Register entry required |
| **Limited-risk** | AI systems with specific transparency obligations: chatbots; AI-generated content; emotion recognition and biometric categorization systems (EU AI Act Art. 50) | Disclose AI interaction to users; label AI-generated content | User notification implemented; AI-generated content labelling policy applied |
| **Minimal-risk** | All other AI systems | No mandatory obligations under EU AI Act | Best-practice governance applied; AI System Register entry still required; periodic review conducted |

### 4.2 Classification process

1. The AI System Owner completes an initial classification using the classification table above and the NIST AI RMF risk categorization criteria.
2. The AIGC reviews and approves the classification before deployment.
3. Classification is re-assessed when the system undergoes a substantial modification, is deployed in a new context, or when applicable regulations are updated.

---

## 5. Deployer obligations for high-risk AI systems

Where the organization deploys a high-risk AI system (as classified under Section 4), the following obligations apply.

### 5.1 Registration

High-risk AI systems used in contexts covered by EU AI Act Annex III must be registered in the EU database of high-risk AI systems by the deployer, where required by the applicable provision. The AI System Owner is responsible for initiating and maintaining this registration, with Legal support.

### 5.2 Fundamental rights impact assessment (FRIA)

A Fundamental Rights Impact Assessment must be completed before deploying any high-risk AI system. The FRIA must:

- Identify the fundamental rights that may be affected by the AI system.
- Assess the likelihood and severity of adverse impacts on those rights.
- Document the groups likely to be affected, including vulnerable groups.
- Identify the specific risks arising from the intended use context.
- Set out the human oversight and safeguard measures that will mitigate identified risks.
- Be completed in consultation with the Data Protection Officer and, where required, affected stakeholders.

The FRIA is documented as part of the AI System Impact Assessment (see [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md)) and retained as part of the system's compliance documentation.

### 5.3 Human oversight

High-risk AI systems must be deployed with appropriate human oversight mechanisms that:

- Allow designated individuals to understand the system's capabilities and limitations.
- Allow designated individuals to correctly interpret outputs before relying on them for decisions.
- Allow designated individuals to disregard, override, or interrupt the system.
- Prevent automation bias by ensuring human reviewers are equipped and empowered to challenge AI outputs.

Human oversight assignments must be documented in the AI System Register and reviewed annually.

### 5.4 Incident reporting

AI-related incidents involving high-risk AI systems must be reported in accordance with Section 10 of this policy.

---

## 6. General-purpose AI model obligations

Where the organization deploys, integrates, fine-tunes, or builds upon a general-purpose AI (GPAI) model, the following obligations apply.

### 6.1 Transparency documentation

The organization must maintain or obtain from the model provider documentation covering:

- The model's intended use and known limitations.
- Training data sources and, where available, data governance measures applied by the provider.
- The model's performance characteristics across relevant tasks.
- Technical safeguards against misuse.

This documentation is recorded in the model card ([`ai/template-model-card.md`](template-model-card.md)) associated with the relevant AI System Register entry.

### 6.2 Copyright compliance

Where the organization fine-tunes a GPAI model using proprietary, licensed, or third-party data, the Legal team must confirm that the use of that data for training is lawful and that any applicable text and data mining exemptions or licenses are documented.

### 6.3 Systemic risk assessment

Where a GPAI model is identified as presenting systemic risk under EU AI Act Chapter V (Articles 51 to 56, general-purpose AI models) (whether because the model provider has designated it as such or because the European Commission has so determined), the organization must assess and document:

- The nature of the systemic risks introduced by the model in its deployment context.
- Adversarial testing results or, where the organization is relying on the provider's testing, the provider's testing summary.
- Cybersecurity measures applied to protect the model from adversarial manipulation.
- Incident reporting arrangements to the AI Office.

---

## 7. National and regional compliance

### 7.1 EU AI act

The EU AI Act applies to AI systems placed on the market or put into service in the EU, and to outputs of AI systems used in the EU, regardless of where the deployer or provider is established. Where any AI system operated by the organization generates outputs used in, or affects individuals in, the EU, the obligations of the EU AI Act apply.

Key compliance obligations:

- AI system classification per Section 4 of this policy.
- Deployer obligations for high-risk systems per Section 5.
- Transparency and labelling obligations per Section 9.
- Serious incident reporting per Section 10.
- Post-market monitoring for high-risk systems per [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md).

### 7.2 Canada: automated decision-making governance

Canada has no in-force federal AI statute. The Artificial Intelligence and Data Act (AIDA), introduced as Part 3 of Bill C-27, lapsed when that bill died at the January 2025 prorogation and would require reintroduction to take effect (Section 1.1). Pending a successor, where the organization operates in Canada or processes data in connection with Canadian operations it aligns to the in-force Canadian instruments:

- **Treasury Board Directive on Automated Decision-Making**, the mandatory federal instrument governing automated decision systems. It binds federal government institutions directly; other organizations use it as a leading-practice benchmark. Where the organization is a federal institution or delivers automated decisions on behalf of one, it complies with the Directive's requirements, using the **Algorithmic Impact Assessment (AIA)** tool to classify and document each automated decision system by impact level.
- **ISED Voluntary Code of Conduct on the Responsible Development and Management of Advanced Generative AI Systems (2023)**, the voluntary code for advanced generative-AI systems. The organization adopts its commitments (accountability; safety; fairness and equity; transparency; human oversight and monitoring; and validity and robustness) for generative-AI systems it develops or manages, pending binding legislation.
- The federal Personal Information Protection and Electronic Documents Act (PIPEDA) remains the private-sector privacy law governing personal data used in AI systems.

The AIGC is responsible for monitoring AIDA-successor legislation and updating this policy and associated procedures when a binding federal AI statute is enacted.

### 7.3 UK AI safety priorities

The UK does not currently have a single AI Act equivalent. The organization follows the UK AI Safety Institute's guidance on frontier AI safety and the Information Commissioner's Office guidance on AI and data protection. Specific commitments:

- AI systems that process personal data comply with the UK GDPR and Data Protection Act 2018.
- The organization monitors UK AI regulatory developments and participates in relevant consultation processes where material to operations.
- High-risk AI systems that may affect UK individuals are assessed against the AI Safety Institute's evaluation criteria for frontier models.

### 7.4 ISO/IEC 42001:2023 certification roadmap

ISO/IEC 42001:2023 specifies requirements for an AI management system (AIMS). The organization's certification roadmap is:

| Stage | Activity | Target |
|---|---|---|
| 1 | Gap assessment against ISO/IEC 42001:2023 requirements | Completed prior to first annual AIGC review |
| 2 | AIMS design and documentation (policies, procedures, registers, governance structures) | Within 6 months of gap assessment |
| 3 | Stage 1 documentation review by certification body | Within 12 months of gap assessment |
| 4 | Stage 2 on-site audit by certification body | Within 18 months of gap assessment |
| 5 | Certification to ISO/IEC 42001:2023 | Upon successful Stage 2 audit |
| 6 | Annual surveillance audits | Annually post-certification |
| 7 | Three-year recertification audit | Every 3 years post-certification |

### 7.5 United States: state and municipal AI laws

The United States has no comprehensive federal AI statute; specific AI uses are governed by state and municipal laws that apply where the organization operates in, or makes covered decisions affecting individuals in, the relevant jurisdiction:

- **Colorado Artificial Intelligence Act** (Senate Bill 24-205, C.R.S. 6-1-1701 et seq.), the first US-state AI law of its kind, imposing a duty of reasonable care on developers and deployers of high-risk AI systems to protect consumers from algorithmic discrimination in consequential decisions. Colorado has repealed and re-enacted this part, with substantial amendments, as the Automated Decision-Making Technology in Consequential Decisions act (Senate Bill 26-189). The effective-date sequence and litigation status are version-sensitive; the organization tracks them via [`ai/jurisdictions/annex-ai-us-colorado.md`](jurisdictions/annex-ai-us-colorado.md) and applies the requirements in force for each covered decision.
- **New York City Local Law 144 (2021)** on automated employment decision tools requires that an automated employment decision tool (AEDT) used to screen candidates or employees for a role in New York City undergo an independent bias audit within one year of use, that a summary of the audit results be published, and that affected candidates receive notice; an AEDT may not be used if its most recent bias audit is more than one year old (New York City Department of Consumer and Worker Protection rule, 6 RCNY 5-300 to 5-304). The effective and enforcement dates are version-sensitive; the organization tracks them via [`ai/jurisdictions/annex-ai-us-new-york-city.md`](jurisdictions/annex-ai-us-new-york-city.md).

Where the organization deploys AI in hiring, lending, housing, insurance, or other consequential decisions affecting United States residents, it assesses applicability against these and successor state laws and applies the classification and oversight controls in Sections 4 and 5.

---

## 8. AI compliance audit and review

### 8.1 Annual AIGC review

The AIGC conducts an annual AI compliance review that covers:

- The current state of the AI System Register, including all systems in production.
- Compliance status for each AI system against applicable regulatory obligations.
- AI incident register summary for the preceding 12 months.
- Post-market monitoring findings for high-risk systems.
- Status of open corrective and preventive actions (CAPAs) arising from prior audits or incidents.
- Changes in applicable regulations or guidance that require policy or procedure updates.

The AIGC produces a written annual review report. The CISO presents a summary to the Board or appropriate Board committee.

### 8.2 Third-party audit for high-risk deployments

High-risk AI systems must be subject to an independent third-party audit at least annually. The audit scope, evidence requirements, and findings management process are defined in [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md).

### 8.3 Continuous monitoring

AI System Owners maintain continuous monitoring of AI system performance, including accuracy, drift, bias drift, and incident signals, as defined in the post-market monitoring plan for each high-risk system.

---

## 9. AI transparency and disclosure

### 9.1 User notification

Where individuals interact with an AI system, including chatbots, automated response systems, or AI-assisted advisory tools, the system must clearly disclose that they are interacting with an AI system and not a human. This disclosure must be made at the point of first interaction or before the individual provides information to the system.

### 9.2 AI-generated content labelling

AI-generated content, including text, images, audio, and video produced or substantially modified by an AI system, must be labelled as AI-generated where:

- The content is published externally or shared with third parties.
- The content could reasonably be mistaken for human-created content.
- The EU AI Act Art. 50 obligation applies, including for deep fakes and AI-generated media.

The labelling mechanism must be technically implemented and documented in the relevant system card.

### 9.3 Explainability for individuals

Where an AI system makes or materially contributes to a decision that significantly affects an individual, including employment, financial, or service access decisions, the individual has the right to:

- Be informed that an AI system was involved in the decision.
- Receive a meaningful explanation of the factors that influenced the decision.
- Request human review of the decision.

Business unit owners are responsible for implementing and communicating these rights in their AI-assisted processes.

---

## 10. AI incident reporting

### 10.1 Incident classification

An AI incident is any unintended behaviour of an AI system, or an event resulting from AI system operation, that:

- Causes or risks causing serious harm to individuals.
- Results in a significant deviation from the AI system's intended purpose.
- Involves a security compromise of an AI system (including adversarial attacks, data poisoning, or model extraction).
- Generates discriminatory, unlawful, or harmful outputs at scale.
- Constitutes a "serious incident" under EU AI Act Art. 3(49): an incident or malfunctioning that directly or indirectly leads to any of (a) the death of a person or serious harm to a person's health; (b) a serious and irreversible disruption of the management or operation of critical infrastructure; (c) the infringement of obligations under Union law intended to protect fundamental rights; or (d) serious harm to property or the environment.

### 10.2 Internal reporting

All AI incidents must be reported internally within 24 hours of detection to the CISO and the relevant AI System Owner. The CISO assesses the incident and determines whether external reporting obligations are triggered.

### 10.3 External reporting: EU AI act

For serious incidents involving high-risk AI systems deployed in the EU, the organization must report to the relevant national competent authority:

- **Within 15 days** of becoming aware of a serious incident involving a high-risk AI system, the general deadline (EU AI Act Art. 73).
- **Immediately, and no later than 2 days**, where the serious incident is a widespread infringement or a serious and irreversible disruption of the management or operation of critical infrastructure (Art. 73(3), referencing Art. 3(49)(b)).
- **Immediately, and no later than 10 days**, in the event of the death of a person (Art. 73).

The CISO is responsible for preparing and submitting the report, in coordination with Legal.

### 10.4 Co-ordination with privacy officer: GDPR art. 33

Where an AI incident involves a personal data breach (as defined under GDPR Art. 4(12)), the Data Protection Officer must be notified immediately. The Data Protection Officer determines whether:

- A GDPR Art. 33 notification to the supervisory authority within 72 hours is required.
- A GDPR Art. 34 notification to affected individuals is required.

The AI incident report and the GDPR personal data breach report are managed as parallel but co-ordinated obligations. The CISO and Data Protection Officer jointly own the co-ordination process.

### 10.5 Incident register

All AI incidents, whether or not they meet the threshold for external reporting, must be recorded in the AI Incident Register maintained by the CISO. The register records incident description, affected systems, timeline, response actions, root cause, and outcome.

---

## 11. Non-compliance consequences

Failure to comply with this policy may result in:

- Regulatory investigation, enforcement action, and financial penalties under applicable AI legislation (EU AI Act penalties of up to EUR 35 million or 7% of annual global turnover for the most serious violations).
- Reputational damage and loss of customer and partner trust.
- Suspension of AI system deployment pending remediation.
- Internal disciplinary action, up to and including termination of employment or contract.
- Requirement to complete mandatory AI governance training.

Material non-compliance must be reported to the AIGC by the relevant business unit owner or the CISO. The AIGC determines appropriate remediation and escalation.

---

## 12. Related documents and framework alignment

| Framework / Regulation | Relevance | Primary Policy Section |
|---|---|---|
| EU AI Act 2024 | AI system classification; deployer obligations; GPAI obligations; transparency; incident reporting; post-market monitoring | 4, 5, 6, 7.1, 9, 10 |
| ISO/IEC 42001:2023 | AI management system requirements; governance; risk management; audit | 3, 7.4, 8 |
| NIST AI RMF 1.0: Govern function | AI governance structure; accountability; policy | 3 |
| NIST AI RMF 1.0: Map/Measure/Manage | AI risk classification; control effectiveness; incident response | 4, 5, 10 |
| OECD AI Principles (2019 Recommendation as updated 2024) | Responsible AI development; human oversight; transparency; accountability | 2, 5.3, 9 |
| UK AI Safety Institute guidance 2024 | Frontier model safety; evaluation criteria | 7.3 |
| Canada: TBS Directive on Automated Decision-Making; ISED Voluntary Code (2023) | Federal automated-decision governance; algorithmic impact assessment; voluntary generative-AI commitments | 7.2 |
| Colorado AI Act (SB24-205, re-enacted SB26-189) | High-risk AI developer and deployer duties; algorithmic-discrimination protection in consequential decisions | 7.5 |
| NYC Local Law 144 (2021) | Automated employment decision tools; bias audit; candidate notice | 7.5 |
| GDPR (UK and EU) | Personal data processing; automated decision-making; breach reporting | 5.2, 9.3, 10.4 |

### Related GRC library documents

- [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md)
- [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md)
- [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md)
- [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md)
- [`ai/template-ai-system-register.md`](template-ai-system-register.md)
- [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md)
- [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md)
- [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md)
- [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md)

---

**End of Document**
