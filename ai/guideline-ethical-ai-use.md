# Ethical AI Use Guideline

**Document Title:** Ethical AI Use Guideline 
**Document Type:** Guideline 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md), [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Annual and upon material AI framework or regulatory change 
**Repository Path:** [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## Purpose

This guideline provides practical direction for all staff, developers, and managers on the ethical use of AI tools and systems within the organization. It translates the organization's AI governance principles into concrete day-to-day expectations, helping employees understand their responsibilities when using, developing, or relying on AI.

---

## Scope

Applies to all employees, contractors, and third parties who use, develop, procure, or are affected by AI systems operated by the organization. Includes all AI tools: productivity AI, generative AI, decision-support AI, and internally developed models.

---

## Foundational Ethical Principles

The organization's approach to AI is grounded in the following principles, aligned with the OECD AI Principles and ISO/PAS 8800:

| Principle | What it means in practice |
| --- | --- |
| **Human-centred** | AI supports human decision-making; it does not replace human judgement on matters that materially affect individuals |
| **Transparent** | AI use is disclosed to those affected; explanations are available for AI-influenced decisions |
| **Fair** | AI systems are tested for bias; outcomes are equitable across groups |
| **Accountable** | Every AI system has a named owner who is responsible for its behaviour and outputs |
| **Safe** | AI systems are tested before deployment; risks are identified and managed |
| **Privacy-preserving** | AI systems process personal data only as necessary and within declared purposes |

---

## Guidance for All Staff Using AI Tools

### 1. Using Approved AI Tools Only

Use only AI tools that have been approved through the Acceptance Into Service process. Unapproved AI tools may introduce security, privacy, or compliance risks.

If you discover a useful AI tool that is not yet approved, raise it with your manager or the IT team for evaluation.

### 2. Do Not Input Sensitive Data Into Consumer AI Tools

Do not input the following into non-approved or consumer AI services (e.g., publicly available generative AI chatbots):
- Personal data of customers, employees, or any individual.
- Confidential business information.
- Financial data.
- Legal or regulatory correspondence.
- Trade secrets or proprietary processes.

Approved enterprise AI tools have been configured with appropriate data governance controls. Consumer tools have not.

### 3. Verify AI Outputs

AI outputs are not always accurate. Before acting on AI-generated content:
- Check factual claims against authoritative sources.
- Do not assume AI-generated legal, financial, or regulatory guidance is correct.
- Apply professional judgement to AI recommendations.

This is especially important in customer-facing communications and decision-making that affects individuals.

### 4. Report AI Concerns

If you observe AI behaviour that appears biased, inaccurate, harmful, or ethically questionable, report it through the incident reporting channel or directly to your manager. AI ethics concerns are treated seriously and investigated.

---

## Guidance for Developers and Data Scientists

### 1. Build for Fairness

During model development, actively test for demographic disparities in model outputs. Use established fairness metrics (demographic parity, equalized odds) and document results. Do not deploy models with residual bias above defined acceptable thresholds without AIGC review and explicit risk acceptance.

### 2. Build for Explainability

Design AI systems so that their outputs can be explained in plain language to affected individuals. Implement an appropriate explainability technique (SHAP, LIME, or equivalent) for all production models. Test whether explanations are meaningful to non-technical stakeholders.

### 3. Protect Privacy by Design

Apply data minimization: use only the personal data necessary for the model's purpose. Anonymize or pseudonymize training data where possible. Confirm legal basis before using personal data for model training.

### 4. Document Everything

Maintain a current Model Card, AI Impact Assessment, and Training Data Record for every AI system you own. Documentation is not optional: it is a governance requirement and a professional responsibility.

### 5. Human in the Loop for High-Stakes Decisions

For decisions that materially affect individuals (credit, employment, benefits, safety), ensure that there is a human review step. AI must support, not replace, human accountability for consequential decisions.

---

## Guidance for Managers

### 1. Know What AI Your Team Uses

Maintain awareness of the AI tools your team uses. Ensure that all tools are approved. Raise unapproved usage with IT for assessment.

### 2. Create Space for Concerns

Ensure that team members feel safe raising concerns about AI behaviour, bias, or ethics. Discourage pressure to deploy AI systems faster than proper evaluation allows.

### 3. Support Documentation Obligations

Ensure that AI system owners in your team have time to maintain required documentation. Model Cards and AI Impact Assessments are governance obligations, not optional extras.

---

## Red Lines: AI Uses That Are Not Permitted

The following uses of AI are prohibited regardless of the tool or context:

1. **Autonomous consequential decisions about individuals** without any human review (credit refusal, employment termination, benefit denial).
2. **Biometric surveillance** of individuals in public spaces.
3. **Social scoring** of individuals based on personal characteristics.
4. **Manipulation of individuals** through subliminal or deceptive techniques.
5. **AI for disinformation** or the production of misleading content intended to deceive.
6. **AI systems classified as Unacceptable risk** under the EU AI Act.

These are absolute prohibitions. Requests to deploy AI for these purposes are escalated to the AIGC and Legal Counsel.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OECD AI Principles (2023) | Human-centric, fair, transparent, accountable AI | Core ethical principles |
| ISO/PAS 8800:2023 | Responsible Innovation Management | Responsible AI use |
| EU AI Act (2024) | Articles 5, 9: Prohibited practices and risk management | AI red lines and high-risk governance |
| ISO/IEC 42001:2023 | §6, Planning; §8, Operation | AI ethics integration |
| NIST AI RMF (2023) | GOVERN and MAP functions | AI risk governance and ethics |

---

**End of Document**
