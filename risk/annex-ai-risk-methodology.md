# AI-Specific Risk Methodology Annex

**Document Title:** AI-Specific Risk Methodology Annex\
**Document Type:** Annex\
**Version:** 1.0.17\
**Date:** 2026-10-26\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md), [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Risk Management: AI\
**Review Frequency:** Annual and upon material AI regulatory change or significant AI incident\
**Repository Path:** [`risk/annex-ai-risk-methodology.md`](annex-ai-risk-methodology.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex extends the enterprise risk assessment methodology in [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md) with AI-specific risk dimensions, assessment criteria, and treatment guidance. It supports consistent identification, scoring, and management of risks arising from the development, deployment, and use of AI systems across the organization.

---

## AI risk taxonomy

AI risks span multiple enterprise risk categories. This annex organizes them into seven AI-specific risk clusters that map to the broader enterprise risk register categories.

| AI Risk Cluster | Maps to ERM Category | Description |
|---|---|---|
| **Technical Failure** | Technology; Operational | Model degradation, performance drift, adversarial inputs, hallucination, data poisoning, system unavailability |
| **Bias and Fairness** | Legal and Regulatory; Human Capital | Discriminatory outputs; proxy discrimination; disparate impact on protected groups; reputational harm |
| **Transparency and Explainability** | Legal and Regulatory; Strategic | Inability to explain AI decisions to affected parties, regulators, or courts; opacity in high-stakes decisions |
| **Security and Adversarial** | Cybersecurity | Prompt injection; model extraction; training data poisoning; API abuse; output manipulation |
| **Privacy** | Privacy | Training data privacy violations; inference attacks; re-identification; unlawful data use in training |
| **Regulatory and Legal** | Legal and Regulatory | EU AI Act classification obligations; Canadian AI-governance obligations (Treasury Board Directive on Automated Decision-Making; AIDA lapsed); sector-specific AI regulation; liability for automated decisions |
| **Dependency and Concentration** | Supplier; Resilience | Over-reliance on single AI provider; model API unavailability; third-party AI supply chain risks |

---

## AI system risk classification

Before applying the risk assessment methodology, each AI system must be assigned a risk tier based on its use case, decision impact, and applicable regulatory classification.

| Risk Tier | EU AI Act Classification | Criteria | Required Controls |
|---|---|---|---|
| **Tier 1, Unacceptable** | Prohibited | The ten Article 5(1) practices, as amended by Regulation (EU) 2026/1744: law-enforcement real-time remote biometric identification in publicly accessible spaces (Article 5(1)(h), narrow exceptions apply); social scoring leading to unrelated-context or unjustified or disproportionate detrimental treatment (Article 5(1)(c)); subliminal, purposefully manipulative, or deceptive techniques whose objective or effect is to materially distort behaviour by appreciably impairing informed decision-making, thereby causing a decision that would not otherwise have been taken in a manner that causes or is reasonably likely to cause significant harm (Article 5(1)(a)); exploitation of age, disability, or social or economic vulnerability whose objective or effect is to materially distort behaviour so as to cause or be reasonably likely to cause significant harm (Article 5(1)(b)); emotion inference in the workplace or education institutions, except for medical or safety reasons (Article 5(1)(f)); biometric categorization of individual natural persons based on their biometric data to deduce or infer their race, political opinions, trade-union membership, religious or philosophical beliefs, sex life, or sexual orientation, other than the labelling or filtering of lawfully acquired biometric datasets or the categorization of biometric data in the area of law enforcement (Article 5(1)(g)); risk assessment of a natural person to assess or predict the risk of committing a criminal offence, based solely on profiling or on assessing personality traits and characteristics, other than support for a human assessment of involvement in a criminal activity that is already based on objective and verifiable facts directly linked to that activity (Article 5(1)(d)); creation or expansion of facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage (Article 5(1)(e)); and, from 2 December 2026, AI that generates or manipulates realistic images, videos, audio, or similar material of an identifiable natural person's intimate parts, or of an identifiable natural person engaged in sexually explicit activities, without that person's freely-given, specific, informed, unambiguous, and explicit consent (Article 5(1)(ba)), or that generates or manipulates material or performance within the meaning of Article 2, points (c) and (e), of Directive 2011/93/EU, except where a "without right" defence applies under national law (Article 5(1)(bb)), both subject to the Article 5(1a) conditions and, for point (ba), the Article 5(1b) limit on what counts as manipulation | Not permitted for deployment, must be blocked at governance gate |
| **Tier 2: High Risk** | High-risk (Article 6(1) and Annex I; Annex III, subject to the Article 6(3) derogation) | Systems in biometrics where the use is permitted under Union or national law and not prohibited (Annex III point 1, including emotion recognition and biometric categorization according to sensitive or protected attributes or characteristics), critical infrastructure, employment, education, credit, insurance, law enforcement, border management, AI in legal proceedings; AI that is, or is a safety component of, an Annex I regulated product subject to third-party conformity assessment (Article 6(1), as bounded by Article 6(1a) to (1c), inserted by Regulation (EU) 2026/1744: an AI system solely used for non-safety-related aspects of user assistance, performance optimization, service efficiency, automation, convenience or quality control is not a safety component unless its failure or malfunctioning would endanger health and safety, and a product that requires third-party conformity assessment solely for risks other than to health and safety does not meet the Article 6(1)(b) condition) | Full pre-deployment assessment; human oversight mandatory; AIGC approval required; ongoing monitoring |
| **Tier 3, Limited Risk** | Transparency obligation | Chatbots; deepfakes; other systems outside Tiers 1 and 2 that carry an Article 50 transparency obligation (for example, biometric categorization not according to sensitive or protected attributes or characteristics, unless the Article 50(3) exception covers it), transparency disclosure required | User disclosure; documentation; quarterly review |
| **Tier 4: Minimal Risk** | Minimal or no obligation | All other AI systems: outside Tiers 1 to 3 and carrying no Article 50 transparency obligation, typically with low impact on safety or fundamental rights (for example, internal automation tools); a system outside Tiers 1 and 2 that carries an Article 50 obligation, such as a low-impact chatbot, is Tier 3 | Standard testing; annual review |

Article 50(3) requires the deployer of an emotion recognition or biometric categorization system to inform the natural persons exposed to it of the operation of the system, and to process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. The obligation does not apply to AI systems used for biometric categorization and emotion recognition that are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties and in accordance with Union law. That disclosure is an additional duty and does not set the tier. A system the exception covers carries no Article 50(3) duty, so that duty does not place it in Tier 3: it is Tier 1 or Tier 2 where those criteria are met, Tier 3 where another Article 50 obligation applies to it, and otherwise Tier 4.

The assigned tier, which is the system's organizational AI risk classification, must be documented in the AI system's model card ([`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md)) and in the AI System Risk Classification field of the AI Risk Register ([`ai/register-ai-risk.md`](../ai/register-ai-risk.md)).

---

## AI risk assessment dimensions

In addition to the standard 5×5 likelihood × impact matrix, AI system risk assessments must evaluate the following AI-specific dimensions.

### Dimension 1: decision autonomy and human oversight

| Level | Description | Risk Modifier |
|---|---|---|
| **Full human decision** | AI provides information only; human makes all decisions | No modifier |
| **Human-in-the-loop** | AI recommends; human approves before action | +1 to likelihood if oversight quality is low |
| **Human-on-the-loop** | AI acts autonomously; human can intervene after action | +2 to impact for high-stakes decisions |
| **Fully autonomous** | AI acts without human oversight | +3 to both; requires Tier 2 minimum classification |

### Dimension 2: affected population scale

| Scale | Criterion | Risk Modifier |
|---|---|---|
| **Internal only** | AI decisions affect only internal staff | No modifier |
| **Limited external** | AI decisions affect fewer than 1,000 individuals annually | No modifier |
| **Moderate external** | AI decisions affect 1,000 to 100,000 individuals annually | +1 to impact |
| **Large-scale external** | AI decisions affect more than 100,000 individuals | +2 to impact |

### Dimension 3: decision reversibility

| Reversibility | Description | Risk Modifier |
|---|---|---|
| **Fully reversible** | Any AI decision can be corrected quickly at low cost | No modifier |
| **Partially reversible** | Corrections possible but costly or time-consuming | +1 to impact |
| **Difficult to reverse** | AI decisions have lasting consequences (e.g., credit denial, employment action, fraud flag) | +2 to impact |
| **Irreversible** | AI decisions cannot be undone (e.g., physical actions, data deletion) | +3 to impact |

### Dimension 4: data sensitivity

| Sensitivity | Description | Risk Modifier |
|---|---|---|
| **Non-personal** | Training and inference data contains no personal data | No modifier |
| **Personal: general** | Training or inference uses general personal data | +1 to likelihood of privacy risk |
| **Personal: special category** | Training or inference uses health, biometric, or other special category data | +2 to likelihood and impact |
| **Confidential business** | Training uses confidential commercial data | +1 to likelihood of leakage risk |

---

## Composite AI risk score

The composite AI risk score is derived by:

1. Applying the standard 5×5 likelihood × impact matrix from [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md)
2. Adding applicable risk modifiers from the four dimensions above
3. Capping the composite score at 25 (Critical)
4. Documenting each modifier applied and its rationale

**Formula:** Composite Score = min(25, (Likelihood + L-modifiers) × (Impact + I-modifiers))

---

## AI-specific risk treatment options

In addition to the standard Avoid / Mitigate / Transfer / Accept / Exploit / Enhance treatment options, AI risks may be treated through:

| AI Treatment | Description |
|---|---|
| **Model redesign** | Modify model architecture, training data, or objective function to reduce risk |
| **Constrained deployment** | Deploy in limited context (subset of use cases, users, or jurisdictions) pending full risk reduction |
| **Human oversight injection** | Introduce mandatory human review step before high-stakes AI decisions are executed |
| **Transparency measures** | Implement explainability outputs, disclosure notices, or decision review mechanisms |
| **Bias mitigation** | Apply fairness-aware retraining, re-sampling, or post-processing calibration |
| **Monitoring and circuit breakers** | Deploy automated monitoring with automatic halt conditions if performance thresholds are breached |
| **Regulatory pre-notification** | For Tier 2 AI systems, engage regulatory authority before deployment to confirm compliance approach |

---

## AI risk review triggers

The following events must trigger an unscheduled AI risk review:

- Model or system update that changes training data, architecture, or output scope
- Change in deployment context (new user group, new jurisdiction, new use case)
- Material performance degradation or fairness metric deviation
- Security incident involving the AI system
- New regulatory guidance that affects the system's classification
- Adverse outcome, complaint, or legal challenge related to the AI system's outputs
- Third-party AI provider notifying of material changes to the underlying model

---

## Regulatory context

| Regulation | Key AI Risk Obligations | Applicability |
|---|---|---|
| **EU AI Act** | Risk-tiered obligations; prohibited systems list; high-risk system requirements; conformity assessment | EU market; global operators with EU users |
| **Canada (Treasury Board Directive on Automated Decision-Making in force; AIDA lapsed)** | Algorithmic impact assessment and transparency for federal automated decision systems; AIDA's proposed high-impact AI regime lapsed at the 2025-01-06 prorogation and is not in force | Government of Canada institutions subject to the Policy on Service and Digital; production automated decision systems used for administrative decisions or related assessments about a client |
| **UK AI approach** | Principles-based; sector regulator-led; a government central function for cross-sector risk assessment and monitoring; AI Security Institute evaluation of frontier models (see [`ai/jurisdictions/annex-ai-united-kingdom.md`](../ai/jurisdictions/annex-ai-united-kingdom.md)) | UK operations and markets |
| **GDPR (EU) / UK GDPR** | Automated decision-making rights (EU Art 22; UK Arts 22A-22D); purpose limitation in training data; Data Protection Impact Assessments for AI | Processing EU/UK personal data |
| **CPPA (Canada, lapsed with Bill C-27)** | Algorithmic transparency obligations; automated decision explanation rights (from the lapsed Bill C-27, not in force) | Canadian personal data processing |
| **PIPL (China)** | Automated decision-making transparency; user right to refuse profiling | Processing data of individuals in China |

---

## Integration with AI governance

| Governance Process | Integration Point |
|---|---|
| Pre-deployment gate | AI risk assessment must be completed and approved before deployment ([`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md)) |
| AI Risk Register | All Tier 2 and Tier 3 AI systems must have entries in [`ai/register-ai-risk.md`](../ai/register-ai-risk.md) |
| AI Audit | AI risk register feeds into periodic AI audit scope ([`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md)) |
| Enterprise Risk Register | AI risks rated High or Critical must be in the enterprise risk register, entered under the AI category or the cluster-mapped category per the taxonomy table above, with the AI Flag set either way ([`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md) Section 7) |
| AIGC | Tier 2 AI system risk assessments require AIGC review and approval ([`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md)) |

---

**End of Document**
