# AI Vendor Security Questionnaire Template

**Document Title:** AI Vendor Security Questionnaire Template\
**Document Type:** Template\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/template-supplier-security-questionnaire.md`](../supply-chain/template-supplier-security-questionnaire.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/register-model-registry.md`](register-model-registry.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI provider, threat-pattern, or regulatory change\
**Repository Path:** [`ai/template-ai-vendor-security-questionnaire.md`](template-ai-vendor-security-questionnaire.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This questionnaire extends the general supplier security questionnaire with AI-specific items. Use this template for any supplier providing a foundation model, AI platform, AI service, or AI-enabled product that materially shapes the organisation's AI behaviour or processes the organisation's data through AI.

The general supplier security questionnaire is the baseline; this template adds the AI-specific sections. Provide both to AI suppliers.

---

## Scope

This template covers:

1. Foundation-model providers (LLM, vision, audio, multimodal).
2. AI platform providers offering hosted training, fine-tuning, or serving infrastructure.
3. AI-enabled SaaS where AI materially shapes the customer-facing function.
4. AI safety and evaluation tooling providers whose outputs are relied upon for the organisation's AI assurance.
5. Vector store, embedding pipeline, retrieval, or AI orchestration providers.
6. AI agent or assistant providers.

It is not a substitute for the general supplier security questionnaire. Submit both.

---

## Section 1: AI provider profile

| Question | Expected response |
| --- | --- |
| What AI category is the offering | Foundation model, fine-tuning platform, serving platform, agent platform, safety tooling, evaluation tooling, embedding or retrieval, AI-enabled SaaS |
| What modalities are supported | Text, image, audio, video, multimodal, embeddings |
| What is the deployment model | Public cloud (multi-tenant), public cloud (single-tenant), customer cloud (vendor-managed), on-premises, edge |
| What is the geographical footprint of training, serving, and support | Country list with operational role |
| Is the offering ISO/IEC 42001 certified or under audit | State and timeline |
| Does the offering hold sector-specific accreditations relevant to AI (e.g. healthcare AI, financial-services AI) | List |
| What is the provider's published responsible-AI policy or framework | URL or document reference |

---

## Section 2: training-data provenance and governance

| Question | Expected response |
| --- | --- |
| What sources comprise the training data | Categorical description of sources |
| Is training data licensed or obtained under documented permission | Categorical breakdown |
| Has the training data been audited for personal data presence | Method and outcome |
| Does the training data include data subject to copyright disputes or active litigation | Disclosure |
| Has the training data been audited for CSAM, hate, or other prohibited categories | Method and outcome |
| What filtering, cleaning, and labelling pipeline produced the training data | Summary or reference |
| What rights mechanism is available for individuals whose data may be in the training corpus | Mechanism description |
| Has the provider committed publicly to specific training data ethics or standards | URL or document reference |
| How does the provider trace lineage from training data to model | Method |

---

## Section 3: customer data handling

| Question | Expected response |
| --- | --- |
| Does the provider train on customer prompts, completions, fine-tuning data, or any derived content by default | Yes / No / Configurable |
| If configurable, is the opt-out the default in the contractual offering for the organisation | Yes / No |
| What is the provider's retention period for prompts, completions, telemetry, and other customer-generated content | Per category |
| Are customer prompts and completions used to produce evaluation datasets shared with other customers | Yes / No |
| Does the provider use customer data for safety classifier development | Yes / No / Configurable |
| Are administrators of the provider able to access customer prompts and completions | Operational model description |
| Is customer data segregated by tenant | Tenancy model |
| What is the provider's response to a customer right to deletion under GDPR, CCPA, or other regimes | Process and timing |
| Is data-residency commitment available | Available residency options |

---

## Section 4: model security

| Question | Expected response |
| --- | --- |
| Has the provider conducted adversarial-evaluation (red team) against the offering | Frequency; methodology |
| Does the provider publish a system card or model card | URL or document reference |
| What safety classifiers run on the provider side | Categories; sensitivity adjustability |
| How does the provider handle prompt injection (direct and indirect) | Mitigations description |
| How does the provider handle jailbreak attempts | Mitigations description |
| How does the provider handle PII leakage in outputs | Mitigations description |
| Does the provider offer customer-configurable safety controls | Available controls |
| Does the provider offer customer-configurable refusal-rate controls | Available controls |
| How does the provider detect and respond to anomalous use of the API or platform | Capability description |
| What logging is available to the customer for security investigation | Log categories and retention |
| Are model weights protected against extraction | Mitigations description |
| How does the provider notify customers of model behaviour changes | Mechanism |

---

## Section 5: tool and agent capabilities

This section applies where the provider offers agentic or tool-using capabilities.

| Question | Expected response |
| --- | --- |
| Does the provider's offering invoke external tools on behalf of users | Yes / No |
| What is the tool authorisation model | Per-tool, per-session, per-agent |
| Can customers restrict the tool list per deployment | Yes / No |
| Are dangerous actions (e.g. payments, deletions, cross-tenant access) protected by human-in-the-loop confirmation | Yes / No / Configurable |
| How does the provider prevent prompt injection from causing unauthorised tool invocation | Mitigations description |
| What rate and chain-length limits apply to agent operations | Limits |
| What audit log is produced per tool invocation | Log content |
| Can customers integrate the provider's agents with the customer's own tools via Model Context Protocol or equivalent | Integration model |
| Does the provider's agent framework support sandboxed code execution | Yes / No / Configurable |

---

## Section 6: evaluation and assurance

| Question | Expected response |
| --- | --- |
| Does the provider publish evaluation benchmarks for the offering | URL or document reference |
| Does the provider publish safety evaluation results | URL or document reference |
| Does the provider publish fairness evaluation results | URL or document reference |
| Does the provider engage independent third-party evaluation | Frequency; reports available |
| Does the provider participate in voluntary AI safety frameworks | List (e.g. UK AISI, US AISI evaluations, GPAI codes of practice) |
| How does the provider validate model behaviour on a new version before release | Process description |
| What is the provider's process for vulnerability disclosure | Process and SLA |

---

## Section 7: compliance and transparency

| Question | Expected response |
| --- | --- |
| Has the provider classified the offering under the EU AI Act risk categories | Classification and rationale |
| Does the offering qualify as a general-purpose AI system or general-purpose AI model with systemic risk | Classification and rationale |
| Does the provider publish or commit to the EU GPAI code of practice | Yes / No |
| What regulatory regimes does the provider operate under | List |
| Has the provider received regulatory enforcement actions in the past 24 months | Disclosure |
| Has the provider received takedown or court orders affecting model behaviour | Disclosure |
| What is the provider's approach to copyright disputes arising from outputs | Disclosure |
| What is the provider's approach to indemnifying customers against copyright or IP claims for outputs | Coverage description |

---

## Section 8: incident response

| Question | Expected response |
| --- | --- |
| What is the provider's AI-incident notification commitment | Notification window |
| What is the provider's commitment to support customer regulatory notifications | Process and timing |
| Does the provider have a documented AI-specific incident response procedure | Yes / No |
| Does the provider conduct annual exercises against AI-specific incident scenarios | Yes / No |
| What is the provider's customer support model during AI-specific incidents | Description |
| Has the provider experienced AI-specific incidents in the past 24 months that affected customers | Disclosure |

---

## Section 9: continuity and exit

| Question | Expected response |
| --- | --- |
| What is the provider's deprecation policy for model versions | Description |
| What notice period applies to material model behaviour changes | Window |
| Can customers pin a specific model version | Yes / No; window |
| What is the provider's exit assistance | Available services |
| What is returned or deleted at contract end (prompts, completions, fine-tuning data, embeddings) | Per category |
| How does the provider handle continuity in the event of provider insolvency | Description |
| Is there a successor-product migration path within the provider's portfolio | Description |

---

## Operating expectations

1. Submit this questionnaire alongside the general supplier security questionnaire before contract signature.
2. Responses are reviewed by the AI Security Maintainer and the Supplier Risk Maintainer; material deficiencies require remediation or formal risk acceptance before procurement.
3. Responses are refreshed annually for Tier 1 critical AI suppliers and at major release events.
4. Material discrepancies between questionnaire responses and observed operating behaviour are treated as a supplier risk event.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | All clauses | AI management system |
| EU AI Act | Articles 26 (deployer), 53 (GPAI), 55 (GPAI systemic risk) | Provider regulation |
| NIST AI RMF | MAP, MEASURE, MANAGE | Risk management functions |
| OWASP LLM Top 10 | LLM03 supply chain | AI supply-chain risk |
| ISO/IEC 27036 | Information security for supplier relationships | Supplier security baseline |
| GDPR / UK GDPR | Article 28 | Processor obligations where personal data is involved |
| DORA | Articles 28 to 44 | Where the provider is a critical ICT third party |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. AI provider questionnaires evolve quickly; new threat vectors and regulatory expectations may require additional sections. Adopting organisations adapt the template to their procurement workflow and the specific provider category.

---

**End of Document**
