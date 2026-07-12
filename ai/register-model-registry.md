# Model Registry

**Document Title:** Model Registry\
**Document Type:** Register\
**Version:** 0.0.7\
**Date:** 2026-07-12\
**Owner:** AI System Inventory Keeper\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/template-dataset-datasheet.md`](template-dataset-datasheet.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/register-ai-risk.md`](register-ai-risk.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Continuous; entries created at registration and updated at every material change\
**Repository Path:** [`ai/register-model-registry.md`](register-model-registry.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the authoritative inventory of every model used in production or pre-production by the organization. A model is any artefact whose outputs are consumed by the organization's products, services, internal operations, or AI systems. The register complements the AI System Register (which lists deployed AI systems and use cases) by capturing per-model technical, ownership, lineage, evaluation, and lifecycle attributes.

A populated model registry identifies real systems and is sensitive operational data; populate, classify, and store internally.

---

## Scope

This register covers:

1. **Internally trained or fine-tuned models** at every stage from research checkpoint through production.
2. **Foundation models** consumed from a provider, recorded at the specific version and configuration the organization depends on.
3. **Open-source models** downloaded and deployed.
4. **Embeddings models** that produce vector representations.
5. **Classifier or scoring models** that support safety, moderation, or routing decisions.
6. **Tool-using or agentic model configurations** where the configuration (system prompt, tool list, guardrails) materially defines the model's effective behaviour.

It does not cover transient or one-off experimentation that is not promoted beyond the experimenter's environment.

---

## Register schema

Each model entry is one row keyed by Model ID. Mandatory fields:

| Field | Description |
| --- | --- |
| Model ID | Unique stable identifier within the registry |
| Model name | Human-readable name |
| Provider | Internal team, or external provider |
| Model family | Architecture family (e.g. transformer, diffusion, gradient-boosting) |
| Base model | If derived, the base model and its version |
| Version | Specific version identifier; semver or vendor-supplied |
| Hash | Cryptographic hash of the model weights or artefact where available |
| Format | Storage format (e.g. safetensors, ONNX, GGUF, vendor-API endpoint) |
| Modality | Input and output modality |
| Parameter count | Where disclosed |
| Training data | Cross-reference to one or more datasheets |
| Fine-tuning data | Cross-reference to fine-tuning datasheets |
| Reinforcement-learning feedback data | Cross-reference where applicable |
| Training compute | Approximate compute used, where disclosed |
| Energy and emissions | Where disclosed; supports the sustainability framework |
| Lineage | Predecessor and successor model identifiers |
| Dependencies | Models, data sources, and operational components the model depends on |
| Owner role | Role accountable for the model |
| Model developer | Team or role that developed the model, or, for an external model, the supplier |
| Model reviewer | Role that independently reviewed the model's conceptual soundness and performance, distinct from the developer |
| Approving authority | Role that approved promotion to production |
| Tier | AI system tier classification per the AI governance and risk framework |
| Use cases | Cross-reference to AI System Register entries that depend on this model |
| Deployment status | Research, evaluation, staging, production, deprecated, retired |
| Deployment environments | Where the model is deployed (cloud, edge, embedded) |
| Inference endpoints | Internal endpoint identifiers in private use |
| Risk classification | EU AI Act risk class where applicable; internal risk classification |
| Model risk rating | Inherent model-risk tier from quantitative and qualitative criteria, recorded as provisional or confirmed |
| Impact assessment reference | Cross-reference to the AI System Impact Assessment |
| Privacy classification | Personal-data exposure profile |
| Security classification | Per the data classification standard |
| Evaluation results | Cross-reference to the most recent evaluation; per-evaluation pass/fail and score |
| Safety evaluation results | Cross-reference to safety, fairness, and adversarial evaluation results |
| Known limitations | Documented limitations from the model card |
| Restricted uses | Uses for which the model must not be used |
| Monitoring posture | Drift monitoring, performance monitoring, safety classifier coverage |
| Last evaluation date | |
| Next evaluation due | |
| Retirement plan | Conditions under which the model is retired |
| Decommissioned-model retention | Where the retired model is kept as a benchmark or fallback, the retention window and its basis |
| Customer-facing transparency | Whether the model is disclosed to end users (per the privacy notice and EU AI Act Article 50) |

---

## Lifecycle states

| State | Definition | Gate to next state |
| --- | --- | --- |
| Research | Model exists in experimentation; not promoted beyond researcher access | Documented model card draft; security review of training data origin |
| Evaluation | Model is being evaluated against the eval suite | Full eval suite pass; fairness and safety eval; risk classification confirmed |
| Staging | Model is deployed to a non-production environment for integration testing | Acceptance-into-service review per the acceptance policy; security review of deployment pipeline; impact assessment confirmed |
| Production | Model serves customer or operational traffic | Monitoring active; rollback procedure tested; customer-facing transparency satisfied |
| Deprecated | Model still serves traffic but no new uses are added; migration path defined | All consuming systems migrated to the successor |
| Retired | Model removed from production; weights archived or deleted per retention | Cascaded deletion of dependent embeddings, caches, derived data as applicable |

---

## Lineage tracking

For each model, the registry records two lineage chains:

1. **Backward lineage.** Base model, fine-tuning data, RL feedback data, training compute. Allows traceability to upstream inputs for incident response, supplier-incident impact, and contractual or legal claims.
2. **Forward lineage.** Successor models, derived embeddings, distilled or quantized variants, fine-tunes by downstream teams. Allows impact analysis when a model is retired or recalled.

---

## Integration with adjacent governance

| Adjacent artefact | Integration point |
| --- | --- |
| AI System Register | Each system entry lists the model identifiers it depends on |
| Dataset datasheet | Each training or fine-tuning dataset row references its datasheet |
| Model card | Each production model has a published model card |
| System card | Each AI system has a system card that summarizes its models |
| AI risk register | High-risk models map to specific risk entries |
| AI impact assessment | Production promotion requires a current impact assessment |
| Third-party AI due diligence | External-provider models reference the supplier assurance evidence |
| Supplier risk register | External-provider models cross-link to the supplier record |
| MCP server register | Where the model is consumed via an MCP server, the server record cross-links |
| AI incident response plan | Each model carries its inferred role in the incident class taxonomy |
| Foundation model lifecycle procedure | External foundation models follow that procedure |

---

## Operating expectations

1. A model is not deployed to a production environment without a corresponding registry row in Production state.
2. Material changes (new base model, new fine-tuning data, new restricted use, new tier) trigger a row update within five business days.
3. The AI System Inventory Keeper reviews the registry at minimum quarterly for completeness and accuracy.
4. The Data Protection Officer reviews entries for personal-data exposure at minimum annually.
5. The AI Security Maintainer reviews entries for adversarial-evaluation currency at minimum semi-annually.
6. Retired model artefacts are handled per the records retention standard with explicit consideration of derived embeddings, caches, and downstream model lineage.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8 operation, §7.5 documented information | AI management system |
| EU AI Act | Articles 9, 11, 12, 26, 50; Annex IV | High-risk AI documentation, deployer obligations, transparency |
| NIST AI RMF | MAP, MEASURE, MANAGE | Risk-management functions |
| ISO/IEC 42006:2025 | Requirements for AIMS audit and certification bodies | Audit baseline |
| ISO/IEC 23894:2023 | AI risk management | Risk integration |
| OSFI Guideline E-23 (2025, effective 2027) | Model risk management: inventory information (Appendix 1), risk rating, independent review | Model-risk governance, adopted sector-neutrally |
| OECD AI Principles | Transparency and accountability | Governance reference |
| Model card pattern | Mitchell et al. 2019 | Model documentation |
| Datasheets for datasets | Gebru et al. 2018 | Dataset documentation |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. The completeness of a populated registry depends on the maturity of MLOps tooling and the discipline of model promotion. The register is not a substitute for the model card or for the impact assessment; it is the inventory and lineage layer that connects them.

---

**End of Document**
