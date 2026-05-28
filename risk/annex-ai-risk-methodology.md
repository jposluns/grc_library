# AI-Specific Risk Methodology Annex

**Document Title:** AI-Specific Risk Methodology Annex 
**Document Type:** Annex 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Risk Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md), [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Risk Management: AI 
**Review Frequency:** Annual and upon material AI regulatory change or significant AI incident 
**Repository Path:** [`risk/annex-ai-risk-methodology.md`](annex-ai-risk-methodology.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This annex extends the enterprise risk assessment methodology in [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md) with AI-specific risk dimensions, assessment criteria, and treatment guidance. It supports consistent identification, scoring, and management of risks arising from the development, deployment, and use of AI systems across the organisation.

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
| **Regulatory and Legal** | Legal and Regulatory | EU AI Act classification obligations; AIDA compliance; sector-specific AI regulation; liability for automated decisions |
| **Dependency and Concentration** | Supplier; Resilience | Over-reliance on single AI provider; model API unavailability; third-party AI supply chain risks |

---

## AI system risk classification

Before applying the risk assessment methodology, each AI system must be assigned a risk tier based on its use case, decision impact, and applicable regulatory classification.

| Risk Tier | EU AI Act Classification | Criteria | Required Controls |
|---|---|---|---|
| **Tier 1, Unacceptable** | Prohibited | Biometric mass surveillance; social scoring; subliminal manipulation; exploitation of vulnerability | Not permitted for deployment, must be blocked at governance gate |
| **Tier 2: High Risk** | High-risk (Annex III) | Systems in critical infrastructure, employment, education, credit, insurance, law enforcement, border management, AI in legal proceedings | Full pre-deployment assessment; human oversight mandatory; AIGC approval required; ongoing monitoring |
| **Tier 3, Limited Risk** | Transparency obligation | Chatbots; deepfakes; emotion recognition; biometric categorization, transparency disclosure required | User disclosure; documentation; quarterly review |
| **Tier 4: Minimal Risk** | Minimal or no obligation | AI with low impact on safety or fundamental rights; internal automation tools | Standard testing; annual review |

Tier classification must be documented in the AI system's model card ([`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md)) and in the AI Risk Register ([`ai/register-ai-risk.md`](../ai/register-ai-risk.md)).

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

In addition to standard Avoid / Reduce / Transfer / Accept treatment options, AI risks may be treated through:

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
| **AIDA (Canada)** | Risk mitigation for high-impact AI systems; transparency; algorithmic impact assessments | Canadian operations; Canadian personal data |
| **UK AI approach** | Principles-based; sector regulator-led; cross-sector AI Safety Institute oversight | UK operations and markets |
| **GDPR / UK GDPR** | Automated decision-making rights (Article 22); purpose limitation in training data; Data Protection Impact Assessments for AI | Processing EU/UK personal data |
| **CPPA (Canada)** | Algorithmic transparency obligations; automated decision explanation rights | Canadian personal data processing |
| **PIPL (China)** | Automated decision-making transparency; user right to refuse profiling | Processing data of individuals in China |

---

## Integration with AI governance

| Governance Process | Integration Point |
|---|---|
| Pre-deployment gate | AI risk assessment must be completed and approved before deployment ([`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md)) |
| AI Risk Register | All Tier 2 and Tier 3 AI systems must have entries in [`ai/register-ai-risk.md`](../ai/register-ai-risk.md) |
| AI Audit | AI risk register feeds into periodic AI audit scope ([`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md)) |
| Enterprise Risk Register | AI risks rated High or Critical must be in the enterprise risk register (Supplier category) |
| AIGC | Tier 2 AI system risk assessments require AIGC review and approval ([`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md)) |

---

**End of Document**
