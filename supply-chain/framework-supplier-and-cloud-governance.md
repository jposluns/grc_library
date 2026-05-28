# Supplier and Cloud Governance Framework

**Document Title:** Supplier and Cloud Governance Framework 
**Document Type:** Framework 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-onboarding-security-review.md`](procedure-supplier-onboarding-security-review.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md) 
**Classification:** Public 
**Category:** Supplier Governance 
**Review Frequency:** 6 to 12 months and upon material supplier, service, data, contract, or regulatory change 
**Repository Path:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This framework defines an organisation-neutral model for supplier, third-party, cloud, managed service, outsourced processing, AI service, and supply-chain governance.

It establishes lifecycle controls for supplier intake, risk classification, due diligence, contract control alignment, onboarding, monitoring, reassessment, incident management, resilience, exit, and evidence retention.

---

## Scope

This framework applies to external providers that provide, operate, host, process, access, store, transmit, analyze, support, maintain, or materially affect organisational data, systems, services, operations, security, privacy, AI capabilities, or resilience.

Supplier categories may include:

- Cloud infrastructure and platform providers.
- Software as a service providers.
- Managed service providers.
- Security service providers.
- AI model, AI platform, AI agent, data labelling, and AI integration providers.
- Data processors and subprocessors.
- Professional service providers with access to data or systems.
- Critical logistics, facilities, telecommunications, and operational dependency providers.
- Open-source and commercial software dependencies where supplier-like assurance is required.

---

## Supplier lifecycle

| Stage | Required Governance Activity | Evidence Class |
| --- | --- | --- |
| Intake | Record supplier request, business purpose, owner, service type, data categories, and intended use. | Supplier intake record. |
| Classification | Classify supplier by criticality, data sensitivity, system access, regulatory exposure, resilience impact, and AI involvement. | Supplier risk classification. |
| Due Diligence | Assess security, privacy, resilience, compliance, financial, legal, operational, and AI-specific risks. | Supplier assessment, questionnaire, evidence review. |
| Contracting | Define confidentiality, security, privacy, breach notification, audit, subprocessors, data use, deletion, resilience, and exit commitments. | Contract control schedule. |
| Onboarding | Approve access, integrations, data flows, service configuration, logging, monitoring, and support model. | Onboarding checklist. |
| Monitoring | Review performance, assurance evidence, incidents, changes, vulnerabilities, control attestations, and risk changes. | Supplier monitoring record. |
| Reassessment | Reassess based on cadence, material change, incident, contract renewal, regulatory change, or risk trigger. | Reassessment report. |
| Exit | Execute data return, deletion, access removal, service transition, evidence retention, and dependency closure. | Exit checklist, deletion attestation. |

---

## Risk classification criteria

Suppliers should be classified using factors including:

- Access to personal data.
- Access to sensitive data.
- Access to confidential business data.
- Privileged or administrative access.
- Hosting of critical workloads.
- Role in backup, recovery, identity, network, security, monitoring, or logging.
- AI model operation, training, fine-tuning, retrieval, inference, or monitoring.
- Business process criticality.
- Recovery dependency.
- Geographic or cross-border exposure.
- Subprocessor reliance.
- Contractual or regulatory obligations.
- Concentration risk.
- Exit complexity.

---

## Minimum supplier control domains

| Domain | Control Intent |
| --- | --- |
| Governance | Supplier has assigned business owner, risk owner, and control owner. |
| Security | Supplier implements access control, encryption, logging, vulnerability management, incident handling, and secure operations appropriate to risk. |
| Privacy | Supplier processes personal data only under documented authority and contractual control. |
| Data Use | Supplier data use, retention, deletion, training, analytics, and improvement rights are defined and approved. |
| AI Services | Supplier AI systems disclose data handling, retention, model training use, retrieval boundaries, monitoring, and human oversight support. |
| Resilience | Supplier recovery commitments, continuity capabilities, test evidence, and failure scenarios are reviewed. |
| Subprocessors | Supplier discloses relevant subcontractors or subprocessors and provides notification or approval mechanisms where required. |
| Compliance | Supplier provides assurance evidence appropriate to risk and contractual obligations. |
| Incident Management | Supplier notification, cooperation, investigation, containment, and evidence obligations are defined. |
| Exit | Data return, deletion, access removal, transition support, and survivability of obligations are defined. |

---

## AI supplier requirements

AI suppliers require specific assessment where they provide model hosting, inference APIs, embedded AI capabilities, agents, assistants, coding systems, document processing, data labelling, model tuning, retrieval infrastructure, or monitoring.

Assessment should cover:

- Whether submitted data is used for training, fine-tuning, evaluation, or service improvement.
- Prompt, file, output, log, and embedding retention.
- Model provider and subprocessor chain.
- Data residency and access geography.
- Access to customer-controlled retrieval stores or repositories.
- Tool execution boundaries.
- Security testing, abuse monitoring, and incident notification.
- Deletion, export, and decommissioning capability.
- Administrative access and support access controls.
- Contractual restriction on unauthorized secondary use.

---

## Cloud governance requirements

Cloud services should be governed across:

- Identity and access management.
- Logging and monitoring.
- Encryption and key management.
- Network segmentation and exposure management.
- Configuration baseline management.
- Vulnerability and patch responsibilities.
- Backup and recovery.
- Region and data residency selection.
- Shared responsibility allocation.
- Incident response integration.
- Asset and service inventory.
- Cost, capacity, and service lifecycle governance.

---

## Evidence requirements

Adopting organisations should maintain:

- Supplier inventory.
- Supplier risk classification.
- Due diligence record.
- Contract control schedule.
- Data processing terms where applicable.
- AI data-use review where applicable.
- Assurance evidence.
- Access review.
- Incident records.
- Resilience assessment.
- Reassessment record.
- Exit plan.
- Deletion or return attestation.

---

## Limitations

This framework does not replace legal, procurement, privacy, security, or sector-specific supplier review. Supplier obligations depend on service model, data category, contract terms, regulatory context, jurisdiction, and operational dependency.

---

**End of Document**
