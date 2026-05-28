# Global Regulatory Applicability Register

**Document Title:** Global Regulatory Applicability Register  
**Document Type:** Register  
**Version:** 0.0.1  
**Date:** 2026-05-27  
**Owner:** Compliance Maintainer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`governance/charter-governance-library.md`](../governance/charter-governance-library.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`compliance/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md), [`compliance/annex-healthcare-sector-requirements.md`](annex-healthcare-sector-requirements.md), [`compliance/annex-transportation-and-logistics-sector-requirements.md`](annex-transportation-and-logistics-sector-requirements.md)  
**Classification:** Public  
**Category:** Core Governance  
**Review Frequency:** 6 to 12 months and upon material regulatory change  
**Repository Path:** [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This register provides an organization-neutral structure for identifying regulatory applicability. It does not state that any specific law applies to an adopting organization. Applicability depends on facts including jurisdiction, establishment, data residency, processing role, sector, customer commitments, regulated activity, data category, and service model.

---

## Applicability Assessment Fields

| Field | Description |
| --- | --- |
| Regulatory Family | Privacy, cybersecurity, AI, resilience, financial, trade, consumer protection, labour, sector, or contractual regime. |
| Jurisdiction | Country, region, state, province, or supranational area. |
| Trigger | Condition that may make the regime relevant. |
| Role | Controller, processor, service provider, supplier, operator, deployer, importer, exporter, employer, or regulated entity. |
| Data Category | Personal data, sensitive data, customer data, employee data, financial data, regulated data, operational data, AI training data, or model output. |
| System Category | Business system, security system, AI system, cloud service, supplier service, critical process, or data platform. |
| Obligation Type | Legal obligation, regulatory interpretation, contractual requirement, industry practice, or architectural recommendation. |
| Control Linkage | Policy, standard, procedure, register, matrix, or template in this repository. |
| Evidence Class | Assessment, approval, record, report, register entry, contract clause, audit result, or test result. |
| Limitation | Facts requiring legal, compliance, privacy, or sector-specific review. |

---

## High-Level Regulatory Families

| Family | Typical Trigger | Relevant Repository Domains | Evidence Classes |
| --- | --- | --- | --- |
| Privacy and data protection | Processing personal data, sensitive data, employee data, or cross-border transfers. | Privacy, AI, Supplier, Core | Data inventory, privacy impact assessment, transfer assessment, retention record, breach response record. |
| Cybersecurity and information security | Operating networked systems, cloud services, regulated infrastructure, or customer-facing services. | Core, Supplier, Resilience, AI | Security policy, risk assessment, control test, incident record, supplier assurance evidence. |
| Artificial intelligence governance | Developing, deploying, procuring, operating, or materially using AI systems. | AI, Privacy, Supplier, Core | AI system register, impact assessment, model documentation, human oversight record, monitoring record. |
| Operational resilience | Operating critical services, material business processes, regulated services, or high-availability systems. | Resilience, Supplier, Core | Business impact analysis, recovery plan, test report, corrective action log, supplier continuity evidence. |
| Cloud and third-party risk | Using external providers for hosting, data processing, AI capabilities, managed services, or critical operations. | Supplier, AI, Privacy, Resilience | Due diligence, contract controls, subprocessor register, assurance report, exit plan. |
| Trade and supply chain security | Participating in controlled logistics, customs, trade security, or international movement of goods. | Supplier, Resilience, Core | Supplier assessment, chain-of-custody control, trade compliance review, incident record. |
| Records and retention | Maintaining business, personal, financial, security, or operational records. | Core, Privacy, AI, Supplier | Retention schedule, deletion record, litigation hold, audit record. |

---

## Legal Obligation Versus Practice

This register separates requirements as follows:

| Type | Meaning |
| --- | --- |
| Legal Obligation | Direct requirement under applicable law, regulation, order, or binding legal authority. Requires legal or compliance validation. |
| Regulatory Interpretation | Reasoned interpretation of how a requirement may apply to a fact pattern. Requires review against current authority. |
| Contractual Requirement | Commitment arising from customer, supplier, employment, insurance, or partner agreements. |
| Industry Practice | Common assurance or governance expectation not necessarily legally binding. |
| Architectural Recommendation | Technical or governance design recommendation based on risk, resilience, security, or assurance rationale. |

---

## Maintenance Rules

1. Do not state that a law applies without a documented applicability basis.
2. Do not state that the repository proves compliance.
3. Do not include legal advice.
4. Do not include organization-specific facts.
5. Do not copy statutory text unless the source is public-domain or otherwise compatible with CC0 publication.
6. Record uncertainty explicitly where deployment model, data residency, processing role, sector, or jurisdiction is unknown.

---

**End of Document**
