# Foundation Model Lifecycle Procedure

**Document Title:** Foundation Model Lifecycle Procedure 
**Document Type:** Procedure 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** AI Governance Approver 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md), [`ai/register-model-registry.md`](register-model-registry.md), [`ai/template-ai-vendor-security-questionnaire.md`](template-ai-vendor-security-questionnaire.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Annual and upon material change to foundation-model providers, regulatory expectation, or risk posture 
**Repository Path:** [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure governs the lifecycle of foundation and frontier models consumed by the organisation: evaluation, supplier selection, contractual integration, deployment, ongoing monitoring, version-transition management, and exit. It complements the AI model lifecycle management procedure (which is generic) with the specific obligations and risk vectors of foundation-model consumption.

---

## Scope

This procedure applies to:

1. Large language models, vision-language models, audio models, image and video generation models, multimodal models, and other general-purpose AI systems consumed from an external provider.
2. Open-source foundation models adopted at scale, where the organisation depends on the model's continued availability and integrity.
3. Significant fine-tunes of foundation models where the underlying foundation continues to drive the system behaviour.

It does not cover narrow, organisation-trained, task-specific models; those follow the AI model lifecycle management procedure.

---

## Procedure

### Step 1: Identify the candidate foundation model

The AI System Inventory Keeper maintains a candidate list with the following per-candidate fields:

| Field | Description |
| --- | --- |
| Candidate name and provider | Specific version, modality, intended use |
| Provider type | Proprietary cloud-hosted, proprietary self-hosted, open-source self-hosted, open-source cloud-hosted |
| Use case | The organisational use this candidate supports |
| Risk classification | Per the AI governance framework |
| Decision-due date | When the candidate must be selected or rejected |

### Step 2: Pre-engagement evaluation

| Evaluation dimension | Required output |
| --- | --- |
| Capability evaluation | Pass against the candidate's intended use cases on the organisation's eval suite |
| Safety evaluation | Pass against the safety, refusal, and harmful-output evaluations including OWASP LLM Top 10 and MITRE ATLAS-aligned tests |
| Adversarial evaluation | Pass against the adversarial test reference suite |
| Fairness evaluation | Subgroup performance analysis appropriate to the use case |
| Data-handling assessment | Provider's data-handling commitments per the AI vendor security questionnaire |
| Training-data provenance | Provider's documented training data sources and any litigation or regulatory exposure |
| Privacy assessment | Personal-data exposure profile; cross-reference to a DPIA if required |
| Security assessment | Provider security questionnaire, supplier assurance evidence, threat model |
| Cost and rate-limit assessment | Inference and training cost, latency, capacity guarantees |
| Substitutability | Practical effort to migrate to an alternative provider or model |
| Exit plan feasibility | Documented exit strategy; cross-reference to the cloud exit standard |

The output is a recommendation memo to the AI Governance Council with a Go, Go-with-conditions, or No-go decision.

### Step 3: Contractual integration

For proprietary cloud-hosted providers, the contract includes the following beyond the standard supplier security and privacy assurance terms:

| Clause | Required content |
| --- | --- |
| Data handling | No training on the organisation's prompts, completions, fine-tuning data, or any derived content unless explicit opt-in is documented |
| Data retention | Specific retention windows for prompts, completions, and telemetry; right to request deletion |
| Logging and observability | Provider commitments on log retention, access, and integrity |
| Service-level commitment | Latency, availability, and capacity targets; service credits |
| Model version stability | Notice period for material model behaviour changes; the provider's deprecation policy |
| Safety classifier coverage | The safety, content, or moderation classifiers running on the provider side |
| Subprocessor list and notification | As required under GDPR Article 28 where applicable |
| Cross-border transfer | Mechanism per Chapter V GDPR; data residency commitments |
| Indemnity for IP claims | Coverage for copyright claims arising from model outputs where the contract allows |
| Indemnity for personal data claims | Coverage where personal data is involved in training-data disputes |
| Audit and assurance | SOC 2 Type II, ISO 27001, ISO 42001 (when available) evidence cadence; right to audit or right to an independent attestation |
| Incident notification | Notification window matching the organisation's regulatory obligations |
| Right to exit | Documented exit assistance; data return and destruction obligations |
| Co-operation on regulatory enquiries | Provider's commitments where the organisation faces a regulator under EU AI Act, NIS 2, sector regulator |

For open-source self-hosted models, the contractual layer is replaced by an internal acceptance memo that records: the licence, the weights provenance, the integrity verification (hash on download), and the secure-hosting plan.

### Step 4: Deployment

| Action | Required output |
| --- | --- |
| Register in the model registry | Production-state row with full metadata |
| Document in the AI System Register | One or more system rows pointing to this model |
| Produce model card and system card | Published per the documentation framework |
| Configure observability | Prompt logs, response logs, safety classifier outputs, tool invocation logs (where agentic), cost metrics |
| Configure safety guardrails | Input filters, output filters, retrieval guardrails (where applicable), agent permission enforcement |
| Acceptance into service | Per the acceptance policy |
| Customer-facing transparency | Privacy notice updates; algorithm transparency register entry if applicable |
| Rollback plan | Documented; tested in staging |

### Step 5: Ongoing monitoring

| Monitoring activity | Cadence |
| --- | --- |
| Eval suite regression run | At least monthly for production foundation models; on every provider version notification |
| Safety classifier review | Quarterly |
| Cost and capacity review | Monthly |
| Supplier incident monitoring | Continuous; subscribe to the provider's security advisory channel |
| Provider model-card or system-card update review | Per provider release |
| Regulatory or litigation environment review | Quarterly; legal counsel feeds material developments |
| Drift detection | Continuous where automatable |
| Customer-impact review | After each material customer feedback signal |

### Step 6: Version transition

Provider model version changes are managed through a defined transition window.

| Step | Action |
| --- | --- |
| Notification | Receive provider notice; record in the model registry on the existing version |
| Impact analysis | Run the eval suite on the new version; compare to the current version |
| Risk assessment | Document material behaviour changes; reassess risk classification |
| Stakeholder communication | Internal teams whose systems depend on the model; customers if material |
| Staged rollout | Canary; ramp; full |
| Old version archive | Where the provider permits pinning, the prior version remains available for rollback for a defined window |
| Update model registry | New version row; supersedes the prior row; lineage updated |

If the version transition is involuntary (provider deprecates the prior version without offering continuity), the procedure escalates the supplier and concentration risk for the AI Governance Council.

### Step 7: Exit

| Step | Action |
| --- | --- |
| Trigger | Provider failure, contractual breach, change in provider ownership creating restricted-list exposure, material behavioural change rendering the model unsuitable, organisational decision to consolidate providers |
| Successor selection | Per Step 1 and Step 2 |
| Migration | Per the cloud exit and data portability standard for cloud-hosted; per the open-source migration plan for self-hosted |
| Data return and destruction | Per the supplier offboarding evidence template; specific to AI artefacts include prompt logs, completions, fine-tuning data, derived embeddings, evaluation data |
| Customer communication | If the change is customer-facing |
| Closure record | Per the supplier offboarding evidence template |

---

## Specific risk vectors and mitigations

| Risk | Mitigation |
| --- | --- |
| Provider trains on the organisation's data | Contractual no-train clause; technical controls (zero-data-retention deployment options); periodic audit |
| Provider deprecates without notice | Contractual notice period; concentration analysis; pin where supported |
| Provider model behaviour changes silently | Eval-suite regression detection; provider release-note monitoring |
| Provider faces regulatory action affecting service | Geopolitical and regulatory environment review; pre-identified alternates |
| Provider faces IP litigation that disrupts service | Indemnity coverage; alternates |
| Provider security incident exposes the organisation's prompts or completions | Incident response coordination; data-residency and tenant-isolation commitments |
| Provider concentration becomes a critical-ICT-third-party concern | Concentration register; DORA Oversight Framework where applicable |

---

## Operating expectations

1. Foundation-model selection is approved by the AI Governance Council with a documented Go decision.
2. Quarterly status reviews aggregate evaluation, monitoring, cost, and supplier-risk signals per provider.
3. Annual deep review revisits substitutability and exit-plan feasibility.
4. Every foundation-model provider has an identified alternate at one tier of substitution effort or better.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8 operation; §8.4 documentation; §9 performance evaluation | AI management system |
| EU AI Act | Articles 26 (deployer obligations), 50 (transparency), 53 (general-purpose AI obligations) | Foundation-model regulation |
| NIST AI RMF | All four functions | AI risk management |
| ISO/IEC 23894:2023 | AI risk management | Risk integration |
| OECD AI Principles | All five values | Foundational principles |
| Hiroshima Process on Generative AI | Voluntary code of conduct for advanced AI | Provider expectations |
| DORA | Articles 28 to 44 (third-party ICT risk including critical providers) | EU financial services |

---

## Limitations

This procedure is a public-domain baseline. Foundation-model lifecycle is rapidly evolving; specific provider terms, technical mitigations, and regulatory expectations change frequently. Adopting organisations confirm current provider terms, current regulatory positions, and current evaluation practice with subject-matter experts at every cycle.

---

**End of Document**
