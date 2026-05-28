# AI Risk Register

**Document Title:** AI Risk Register 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** GRC Programme Manager 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Quarterly and upon material AI system change or incident 
**Repository Path:** [`ai/register-ai-risk.md`](register-ai-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register defines the schema, governance, and representative risk entries for the AI Risk Register. The AI Risk Register is the central record of identified risks associated with AI systems deployed or under development by the organisation. It supports the AI Governance Council's risk oversight function and feeds into the enterprise risk management process.

---

## Register schema

Each AI risk entry must contain the following fields:

| Field | Description |
| --- | --- |
| **Risk ID** | Unique identifier (format: AIR-YYYY-NNN) |
| **AI System** | Name and version of the affected AI system |
| **Risk Category** | Bias / Explainability / Security / Privacy / Performance / Compliance / Governance |
| **Risk Description** | Clear statement of the risk event and its potential consequences |
| **Threat Source** | Technical failure / Human error / External threat / Regulatory change |
| **Affected Stakeholders** | Internal users / Customers / Regulators / Third parties |
| **Inherent Likelihood** | 1 (Very Low) to 5 (Very High) |
| **Inherent Impact** | 1 (Negligible) to 5 (Critical) |
| **Inherent Risk Score** | Likelihood × Impact |
| **Current Controls** | Description of controls currently in place |
| **Control Effectiveness** | Weak / Partial / Effective |
| **Residual Risk Score** | Calculated residual score after controls |
| **Risk Rating** | Low / Medium / High / Critical |
| **Treatment Option** | Mitigate / Transfer / Avoid / Accept |
| **Treatment Plan** | Actions to be taken, owner, and due date |
| **Risk Owner** | Role title of responsible party |
| **Status** | Open / In Treatment / Accepted / Closed |
| **Review Date** | Date of next scheduled review |

---

## Risk categories

| Category | Description |
| --- | --- |
| **Bias** | AI model outputs are unfairly influenced by protected characteristics or unrepresentative training data |
| **Explainability** | AI decision-making cannot be sufficiently explained to affected individuals or regulators |
| **Security** | AI system is vulnerable to adversarial attacks, model extraction, prompt injection, or data poisoning |
| **Privacy** | AI system processes or exposes personal data beyond declared purpose or in violation of privacy laws |
| **Performance** | AI model accuracy degrades to the point of causing operational or compliance failures |
| **Compliance** | AI system fails to meet applicable regulatory requirements (EU AI Act, GDPR, AIDA, etc.) |
| **Governance** | AI system lacks adequate documentation, oversight, or lifecycle controls |

---

## Representative risk entries

The following entries represent the baseline risk register template. Actual operational entries are maintained in the GRC platform and are updated quarterly by the GRC Programme Manager.

| Risk ID | AI System | Category | Risk Description | Inherent Score | Residual Score | Rating | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AIR-2026-001 | All deployed AI systems | Governance | AI systems lack complete model documentation, preventing regulatory audit | 4×3=12 | 4×2=8 | Medium | In Treatment |
| AIR-2026-002 | Decision-support AI | Bias | Automated recommendations exhibit demographic disparity due to unrepresentative training data | 3×4=12 | 3×2=6 | Medium | In Treatment |
| AIR-2026-003 | Generative AI tools | Security | Prompt injection attacks manipulate AI outputs or extract confidential training data | 4×4=16 | 4×2=8 | Medium | In Treatment |
| AIR-2026-004 | Decision-support AI | Explainability | AI decisions affecting customers cannot be explained in plain language as required under GDPR Article 22 | 3×3=9 | 3×2=6 | Medium | In Treatment |
| AIR-2026-005 | All AI systems | Compliance | AI systems classified as High-risk under EU AI Act are not fully compliant with Annex IV documentation requirements | 3×4=12 | 3×3=9 | Medium | Open |
| AIR-2026-006 | ML/prediction models | Performance | Model performance drift causes incorrect outputs over time without detection | 3×3=9 | 3×1=3 | Low | In Treatment |
| AIR-2026-007 | Third-party AI | Governance | Third-party AI embedded in procured software lacks transparency on training data or decision logic | 4×3=12 | 4×2=8 | Medium | Open |

---

## Governance

The AI Risk Register is reviewed quarterly by the GRC Programme Manager and presented to the AI Governance Council at its quarterly meeting.

High and Critical risks are reviewed monthly and escalated to the ERC immediately upon identification.

Risk treatment actions are tracked in the CAPA Register with defined owners and due dates.

The register is updated within 5 business days of any:
- New AI system deployment.
- Material change to an existing AI system.
- AI-related security or compliance incident.
- Material regulatory development affecting AI governance.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §6.1: Actions to Address Risks | AI risk identification and treatment |
| ISO/IEC 42001:2023 | §9: Performance Evaluation | AI risk monitoring |
| EU AI Act (2024) | Article 9: Risk Management System | High-risk AI risk register obligations |
| NIST AI RMF (2023) | MAP and MEASURE functions | AI risk mapping and measurement |
| ISO 31000:2018 | Risk Management Guidelines | Enterprise risk register methodology |

---

**End of Document**
