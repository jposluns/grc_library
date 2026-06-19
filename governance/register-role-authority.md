# Role Authority Register

**Document Title:** Role Authority Register\
**Document Type:** Register\
**Version:** 1.3.1\
**Date:** 2026-06-19\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`governance/framework-human-capital-and-ethical-conduct.md`](framework-human-capital-and-ethical-conduct.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual\
**Repository Path:** [`governance/register-role-authority.md`](register-role-authority.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register defines generic governance roles used across the GRC Documentation Library. Roles are deliberately organisation-neutral and must not be replaced with named individuals in the public repository.

---

## Authority register

| Role | Primary Accountability | Typical Approval Authority |
| --- | --- | --- |
| Governing Body | Oversight of enterprise risk, compliance, security, privacy, resilience, and technology governance. | Charters, risk appetite, major risk acceptance. |
| Board of Directors | The organisation's board (or equivalent governing body where the term applies). Specific board-level approvals such as risk appetite statements and material policy adoption. | Board-approved risk appetite, board-reviewed material exceptions. |
| Board Risk Committee | Board-level subcommittee accountable for risk-appetite oversight, material-risk acceptance, and consolidated enterprise risk reporting. In organisations without a discrete Board Risk Committee, the full board or audit committee exercises this authority (see [`governance/guideline-minimum-viable-governance-structure.md`](guideline-minimum-viable-governance-structure.md) for consolidation patterns). | Risk appetite approval, material exception approval, escalated high-risk AI exception approval. |
| Enterprise Risk Committee (ERC) | Executive-level forum accountable for enterprise risk oversight delegated by the Board Risk Committee, cross-domain risk co-ordination, KRI trend review, and risk-reporting integrity. Meets at least quarterly. | Risk methodology adoption, cross-domain risk decisions, recommendations to the Board Risk Committee. |
| Executive Management | Executive accountability for policy adoption, resourcing, and operating effectiveness. | Enterprise policies, material exceptions, strategic risk decisions. |
| Chief Information Officer | Information and technology governance, architecture, operational technology risk, and digital stewardship. | Technology policies, service governance, architecture exceptions. |
| Chief Technology Officer | Engineering, architecture, technology selection, development practice, and platform direction. | Architecture standards, technology radar, engineering exceptions. |
| Chief Information Security Officer | Information security programme, security risk, control assurance, incident governance, and security standards. | Security standards, security exceptions, incident response procedures. |
| Chief Risk Officer | Enterprise risk methodology, risk appetite alignment, risk aggregation, and risk reporting. | Enterprise risk framework, risk taxonomy, risk reporting. |
| Chief Compliance Officer | Compliance management, obligation tracking, control assurance, and regulatory response coordination. | Compliance policy, obligation register, compliance assurance plan. |
| Chief Privacy Officer | Privacy governance, personal data protection, impact assessments, and data subject rights. | Privacy policy, impact assessment procedure, breach response procedure. |
| Chief Data Officer | Data governance, data quality, lifecycle management, data lineage, and data stewardship. | Data governance standards, classification model, retention model. |
| Chief Audit Executive | Internal audit function head; audit planning, audit assurance, and audit-committee reporting. | Audit plan, audit charter, audit findings. |
| AI Governance Lead | Umbrella AI governance role chairing the AI governance function and coordinating the AI Governance Approver, AI Data Steward, and AI System Inventory Keeper. Typically the AI Governance Council secretariat. | AI governance framework, AI impact assessment, AI exceptions. |
| AI Governance Approver | Approval decisions for AI policies, frameworks, standards, deployment gates, foundation-model selection, risk-classification approvals, and material lifecycle changes. | AI policy approvals, deployment decisions, exception approvals, model-selection sign-off. |
| AI Data Steward | Training-data governance, dataset acceptance, deletion-propagation, lineage tracking, sensitive-content controls, and dataset documentation (datasheets). | Dataset acceptance, deletion authorisation, lineage records. |
| AI System Inventory Keeper | Maintenance of the AI System Register, Model Registry, MCP server register, model cards, system cards, and cross-references between AI inventories and adjacent registers (ADM, resilience, supplier). | Inventory updates, model card and system card maintenance, register reconciliation. |
| Legal Counsel | Legal interpretation, contractual obligations, regulatory privilege, and legal risk review. | Legal position statements, regulatory interpretation, contract exceptions. |
| Internal Audit | Independent assessment of governance, control design, control operating effectiveness, and evidence. | Audit plan, audit report, assurance findings. |
| System Owner | Accountability for a system, service, platform, model, or application across its lifecycle. For an action-capable AI agent, the System Owner (or a designated AI System Owner) is the named accountable owner of the agent's autonomous envelope; accountability for actions the agent performs does not transfer to the agent (`AGENT-PROD-05` in the AI and Agentic Development Security Standard). | System risk acceptance, operating procedures, evidence maintenance, agent autonomous-envelope accountability. |
| Data Owner | Accountability for a data set, data classification, lawful basis, authorized use, and retention. | Data use approval, data sharing, retention exceptions. |
| Control Owner | Ownership of control implementation, monitoring, evidence, exception handling, and remediation. | Control evidence, control design changes, control remediation. |
| Process Owner | Ownership of a business or technical process and its operational controls. | Process procedures, operational exceptions, improvement actions. |
| Supplier Owner | Ownership of supplier relationship, due diligence, contractual controls, performance, and exit planning. | Supplier risk acceptance, supplier review, supplier exit plan. |
| Supplier Risk Maintainer | Maintenance of supplier-related governance artefacts (supplier risk register, due-diligence procedure, supplier audit procedure, supplier-resilience monitoring, concentration register). Distinct from the Supplier Owner role, which is per-supplier; this role maintains the cross-supplier governance content. | Supplier-governance artefact updates; supplier inventory consistency. |
| Resilience Owner | Ownership of business continuity, recovery objectives, testing, and recovery evidence. | Continuity plans, recovery tests, resilience exceptions. |
| Security Owner | Ownership of security controls and incident response within a specific scope (a service, a platform, a programme). Distinct from CISO (organisation-wide). | Security control evidence, scope-level security exceptions, incident response within scope. |
| Communications Owner | Ownership of crisis-communication and incident-communication content and channels. | Communications plans, customer notifications, post-incident communications. |
| IT Operations Lead | Day-to-day IT operations leadership including incident response, change execution, and operations governance. | Operations procedures, operational exceptions, runbook approval. |
| AI Risk Maintainer | Maintenance of AI-specific risk artefacts (AI risk register, AI risk methodology annex, AI impact assessment templates). | AI risk register updates, AI methodology updates. |
| AI Security Maintainer | Maintenance of AI-specific security artefacts (AI red-team report templates, AI vendor security questionnaire, AI dataset datasheets, MCP server register, AI access and agent permissions standard, AI incident response plan, AI inference cost governance standard, model registry, AI adversarial evaluation suite). Distinct from the CISO (organisation-wide security) and the AI Governance Approver (AI policy approval); this role maintains the cross-AI security governance content. | AI security artefact updates; AI security content consistency. |
| Assurance Metrics Maintainer | Maintenance of digital trust and assurance metrics registers. | Metrics catalogue updates. |
| Control Framework Maintainer | Maintenance of the cross-framework alignment matrix and the reverse framework control crosswalk. | Cross-framework matrix updates, control mapping updates. |
| Document Owner | Maintenance of a governance document, metadata, review cycle, and related artefacts. | Minor document updates, review records. |

---

## RACI pattern

| Activity | Accountable | Responsible | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Approve enterprise policy | Executive Management | Document Owner | Legal, Risk, Compliance, Security, Privacy | Affected stakeholders |
| Approve standard | Domain Executive or Delegate | Control Owner | Legal, Risk, Compliance, Security, Privacy | Process owners |
| Approve procedure | Process Owner | Control Owner | Security, Privacy, Compliance | Operational teams |
| Approve exception | Risk Accountable Role | Request Owner | Legal, Security, Privacy, Compliance | Control Owner, Audit where applicable |
| Maintain register | Register Owner | Process Owner | Control Owner, Data Owner | Governance stakeholders |
| Perform assurance review | Internal Audit or Assurance Function | Control Owner | Risk, Compliance, Security, Privacy | Governing Body |

---

## Maintenance rules

1. Roles must remain generic.
2. One organisation may combine roles, but the public library must not assume a specific reporting structure.
3. Approval authority should be adjusted by adopting organisations according to law, regulation, sector, size, and risk appetite.
4. Named individuals, job incumbents, email addresses, and internal team names must not be added to this public register.

---

**End of Document**
