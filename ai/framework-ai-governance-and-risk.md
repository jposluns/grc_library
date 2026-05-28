# AI Governance and Risk Framework

**Document Title:** AI Governance and Risk Framework 
**Document Type:** Framework 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** AI Governance Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/register-ai-risk.md`](register-ai-risk.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** 6 to 12 months and upon material AI risk or regulatory change 
**Repository Path:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This framework defines a reusable governance model for artificial intelligence systems. It addresses accountability, lifecycle control, risk classification, data governance, security, human oversight, supplier dependency, monitoring, assurance, and retirement.

The framework treats data as the primary risk surface. Model behaviour, system autonomy, tool access, and output quality are governed through the controls applied to data, identity, system boundaries, lifecycle evidence, and accountable decision-making.

---

## Scope

This framework applies to AI systems that are developed, configured, procured, deployed, integrated, embedded, or materially used by an adopting organization.

It applies to:

- Machine learning systems.
- Generative AI systems.
- Retrieval-augmented generation systems.
- Predictive models.
- Classification and scoring systems.
- Decision-support systems.
- Autonomous or semi-autonomous agents.
- AI-enabled security, finance, HR, customer, logistics, legal, compliance, and operational systems.
- AI services operated by third parties.

---

## Governance objectives

1. Maintain an authoritative AI system inventory.
2. Classify AI systems by risk, data sensitivity, autonomy, impact, and operating context.
3. Validate lawful, authorized, and appropriate data use.
4. Establish accountable owners for each AI system.
5. Control access to models, prompts, datasets, retrieval stores, tools, logs, and outputs.
6. Address prompt injection, data poisoning, model inversion, membership inference, leakage, unsafe tool use, and shadow AI.
7. Maintain evidence for review, audit, assurance, and risk acceptance.
8. Define monitoring, incident response, exception, and decommissioning requirements.
9. Separate legal obligation, regulatory interpretation, industry practice, and architectural recommendation.

---

## AI lifecycle model

| Lifecycle Stage | Governance Requirement | Evidence Class |
| --- | --- | --- |
| Intake | Proposed AI system is recorded before use. | Intake form, business justification, owner assignment. |
| Classification | Risk, data sensitivity, autonomy, user population, and impact are classified. | Risk tiering record, classification decision. |
| Data Review | Data origin, permitted use, provenance, lineage, retention, and deletion are assessed. | Data assessment, lineage record, license or rights review. |
| Impact Assessment | Privacy, security, legal, ethical, operational, resilience, and supplier risks are evaluated. | AI impact assessment, residual risk decision. |
| Design and Configuration | Controls are defined for identity, access, logging, model behaviour, prompts, tools, retrieval, and data flows. | Architecture record, control design, threat model. |
| Testing and Validation | Functionality, safety, security, privacy, bias, misuse, and failure modes are tested. | Test plan, test result, defect log. |
| Approval | Accountable roles approve use, conditions, controls, and residual risk. | Approval record, exception record where applicable. |
| Deployment | System is released with monitoring, support, incident response, and change control. | Deployment record, monitoring plan. |
| Monitoring | Performance, drift, misuse, leakage, incidents, and control exceptions are reviewed. | Monitoring log, incident record, periodic review. |
| Change | Material changes trigger reassessment. | Change record, reassessment, approval update. |
| Retirement | Access, data, integrations, model endpoints, retrieval stores, and logs are retired or retained under defined rules. | Retirement checklist, deletion or retention attestation. |

---

## Risk classification criteria

AI systems should be classified using criteria including:

- Data sensitivity.
- Personal data involvement.
- Sensitive attribute processing.
- Business criticality.
- Safety impact.
- Financial impact.
- Legal or regulatory impact.
- Customer, employee, or public impact.
- Degree of automation.
- Human oversight quality.
- External model or supplier dependency.
- Tool or action execution capability.
- Internet exposure.
- Prompt, retrieval, or plugin exposure.
- Ability to affect access, entitlement, pricing, eligibility, safety, security, or employment decisions.

---

## Control domains

| Domain | Required Control Intent |
| --- | --- |
| Accountability | Each AI system has an owner, risk accountable role, control owner, and support model. |
| Inventory | AI systems are recorded with lifecycle status, purpose, data categories, integrations, suppliers, and approvals. |
| Data Governance | Data provenance, lineage, classification, permitted use, retention, deletion, and access are governed. |
| Security | Identity, access, logging, encryption, secrets, endpoint controls, network boundaries, and tool permissions are enforced. |
| AI Threat Management | Prompt injection, data poisoning, model inversion, membership inference, leakage, unsafe tool use, and shadow AI are addressed. |
| Human Oversight | Human review is defined where outputs can affect rights, access, safety, eligibility, finances, or material operations. |
| Supplier Governance | External AI services are reviewed for data handling, retention, training use, subcontracting, resilience, security, and exit. |
| Documentation | Model purpose, limitations, data sources, test results, intended use, prohibited use, and monitoring are documented. |
| Monitoring | Usage, drift, failures, incidents, abuse, anomalous outputs, and control exceptions are monitored. |
| Incident Response | AI-related incidents are classified, escalated, contained, investigated, and recorded. |
| Decommissioning | AI systems are retired with data, access, integrations, logs, and supplier commitments addressed. |

---

## Shadow AI control boundary

Unapproved AI services, browser extensions, coding agents, meeting assistants, model APIs, data analysis services, prompt repositories, and document summarization services must be governed as shadow AI unless they have completed intake, classification, data review, and approval.

The control boundary must cover:

- User accounts.
- Enterprise identity federation.
- Data uploaded to external services.
- Prompt and conversation retention.
- Training or improvement use by providers.
- Browser extensions and plugins.
- API keys and service accounts.
- Code repositories and development tooling.
- Sensitive documents and regulated data.

---

## Assurance requirements

AI governance assurance should include:

- AI system inventory review.
- Sampling of impact assessments.
- Review of high-risk systems.
- Data lineage verification.
- Supplier assurance review.
- Security testing review.
- Monitoring and incident review.
- Exception register review.
- Deletion and retention verification.
- Control owner attestation where appropriate.
- Audit procedure review per [`ai/procedure-ai-audit.md`](procedure-ai-audit.md).

---

## Limitations

This framework does not create legal compliance by itself. Adopting organizations must validate applicable laws, sector expectations, data residency, processing roles, supplier terms, and deployment-specific risks.

---

**End of Document**
