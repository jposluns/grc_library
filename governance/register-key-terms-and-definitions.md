# Key Terms and Definitions Register

**Document Title:** Key Terms and Definitions Register\
**Document Type:** Register\
**Version:** 1.1.1\
**Date:** 2026-05-28\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`governance/register-glossary.md`](register-glossary.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material terminology change\
**Repository Path:** [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register defines **library-internal GRC concepts** used across the GRC Documentation Library: terms whose specific meaning within the library's governance vocabulary differs from generic usage and that anchor how the library writes about governance, risk, and compliance. Definitions are written for organisation-neutral reuse and do not incorporate restricted wording from external standards or framework materials.

### Scope distinction

- This register (**Key Terms and Definitions**) defines **internal** GRC concepts (Audit, Authorize, Control, Owner roles, Exception, etc.) as the library uses them.
- The companion [`register-glossary.md`](register-glossary.md) (**Glossary and Acronym Index**) resolves **acronyms and external-domain terms** (regulations, standards, frameworks, regulators, sector programmes, technical concepts).

When in doubt: external term or acronym → the glossary. Internal governance concept → this register.

---

## Terms

| Term | Definition |
| --- | --- |
| Accountability | The assigned obligation to own, decide, maintain, evidence, or accept risk for a governance outcome. |
| AI Agent | An autonomous actor implemented on top of one or more AI models that invokes tools, makes decisions, and carries out multi-step tasks on behalf of a user or service. An agent has its own identity, an explicit capability scope, and a defined human-in-the-loop posture. |
| AI Capability | The specific task or function an AI system or AI service performs (for example, summarisation, classification, retrieval-augmented generation, tool invocation). Several capabilities may be combined inside one AI system. |
| AI Service | An externally-provided AI capability consumed by the organisation (typically a provider-hosted API or managed service). The contractual relationship and supplier governance apply at the service level. |
| AI System | An organisational system that incorporates AI models, AI services, or inference capabilities. An AI system has an owner, a lifecycle, a risk classification, and a governance record. The AI System Register is the inventory of AI systems. |
| AI System Owner | The role accountable for the lifecycle, risk posture, documentation, use conditions, and control compliance of an AI system. |
| Approve | A binding governance decision recorded against an artefact, change, deployment, or exception. The Approving Authority is named in the artefact's metadata; the act of approval is dated and traceable. |
| Audit | A formal, evidence-based, time-bounded assessment of whether controls, processes, or commitments are operating as documented, conducted by an independent or designated function. |
| Authorize | A delegated grant of permission to a specific subject (person, role, system, agent) to perform a specific action; narrower in scope than approval and typically session- or task-bounded. |
| Assurance | Evidence-based confidence that controls, processes, or governance commitments are operating as expected. |
| Control | A requirement, safeguard, process, configuration, review, or activity that modifies risk or provides assurance. |
| Control Owner | The role accountable for maintaining and evidencing a control. |
| Data Lineage | A record of data origin, movement, transformation, use, retention, and deletion across lifecycle stages. |
| Data Owner | The role accountable for business use, classification, quality, retention, and authorized disclosure of a data set. |
| Data Provenance | Evidence describing the origin, rights, collection basis, quality, and permitted use of data. |
| Event | An observation of a security-, operational-, or business-relevant occurrence. Many events are routine and do not require response. |
| Exception | An approved deviation from a requirement, with defined risk, owner, compensating control, expiry, and review condition. |
| Foundation Model | A large, broadly-trained model intended to be adapted to many downstream uses (for example, large language, vision-language, or multimodal models). The organisation typically consumes foundation models from external providers. |
| Framework | A structured governance model defining scope, principles, roles, lifecycle, and integration points for a domain. |
| Impact Assessment | A structured evaluation of risks, obligations, controls, affected parties, and residual exposure before or during use of a system, process, or data activity. |
| Incident | A confirmed or triaged event that meets the documented incident criteria. Incidents are recorded, responded to, and reviewed; events are observed and may or may not become incidents. |
| Log | A recording of a discrete event or transaction. Distinct from monitoring (continuous measurement) and review (qualitative assessment). |
| Model | The trained or fine-tuned weights and architecture that produce predictions or outputs in response to inputs. A model is the inner artefact within an AI system or AI service. |
| Monitor | Continuous measurement of an indicator against a baseline or threshold. Distinct from logging (recording events) and auditing (periodic formal assessment). |
| Legal Obligation | A requirement directly arising from applicable law, regulation, order, contract, or binding authority. |
| Matrix | A structured mapping among risks, controls, obligations, frameworks, evidence, lifecycle stages, or artefacts. |
| Membership Inference | A model attack attempting to determine whether a specific record or individual was present in training or reference data. |
| Model Inversion | A model attack attempting to reconstruct sensitive training or input data from model outputs or access patterns. |
| Policy | A binding statement of governance intent and mandatory principles. |
| Procedure | A repeatable operational method for executing a policy, standard, plan, or control. |
| Prompt Injection | An attack in which instructions embedded in user input, documents, retrieved content, or tool outputs alter system behaviour or cause unauthorized action or disclosure. |
| Register | An authoritative structured record of assets, roles, risks, obligations, controls, systems, exceptions, metrics, or evidence. |
| Regulatory Interpretation | A reasoned position on how a requirement may apply, subject to jurisdiction, sector, role, facts, and legal review. |
| Residual Risk | Risk remaining after controls, mitigations, transfer, avoidance, or acceptance have been applied. |
| Review | A qualitative assessment of logs, monitoring results, audit findings, or other evidence by an accountable role. Distinct from auditing (formal, evidence-based) and monitoring (continuous measurement). |
| Risk Appetite | The amount and type of risk an organisation, at the board or executive level, is willing to take in pursuit of its objectives. Stated in directional, strategic terms. |
| Risk Tolerance | The operational threshold against which a specific risk is assessed (likelihood-impact rating, breach criteria, exception triggers). More granular and quantitative than risk appetite. |
| Shadow AI | Use of AI systems, model services, agents, plugins, datasets, or automation outside approved governance, security, procurement, or data protection processes. |
| Standard | A measurable and enforceable requirement implementing policy intent. |
| Supplier | An external organisation that provides goods, services, or capabilities under a documented commercial relationship. Includes the categories the third-party risk standard enumerates (technology, cloud, logistics, AI, data, professional services, etc.). Synonyms commonly used in the library: third party (legal/contractual emphasis), vendor (technology emphasis). The library's canonical preferred term is "supplier". |
| Third Party | An external provider, contractor, supplier, processor, platform, data provider, model provider, integrator, or service operator. Used in legal and contractual contexts. The library's canonical preferred term for the general case is "supplier". |
| Training Data Leakage | Unauthorized disclosure or recoverability of sensitive training, fine-tuning, prompt, retrieval, or reference data through system outputs or access paths. |
| Vendor | A technology supplier (software, infrastructure, platform, AI provider). The library's canonical preferred term for the general case is "supplier"; "vendor" is reserved for technology-supplier contexts. |

---

## Maintenance rules

1. Definitions must be original and library-canonical.
2. Definitions must not copy external standards text unless republication is explicitly compatible with the library's CC BY-SA 4.0.
3. Definitions must remain organisation-neutral.
4. Terms specific to one domain should be added only when they materially improve consistency across documents.

---

**End of Document**
