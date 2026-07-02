# Document Architecture and Interrelationship Framework

**Document Title:** Document Architecture and Interrelationship Framework\
**Document Type:** Framework\
**Version:** 1.1.2\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/register-role-authority.md`](register-role-authority.md), [`governance/procedure-continuous-improvement-register.md`](procedure-continuous-improvement-register.md), [`governance/framework-sustainability-and-responsible-technology.md`](framework-sustainability-and-responsible-technology.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material repository structure change\
**Repository Path:** [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework defines how documents in the GRC Documentation Library relate to each other. It establishes a hierarchy that connects governance authority to policies, standards, procedures, plans, evidence, metrics, and cross-framework mappings.

The framework provides a reusable architecture for organizations that need a coherent policy corpus rather than a collection of disconnected documents.

---

## Scope

This framework applies to all repository documents in the `governance`, `risk`, `compliance`, `security`, `ai`, `operations`, `resilience`, `privacy`, `supply-chain`, and `dev-security` domains.

It governs:

- Document type selection.
- Parent and dependent document relationships.
- Metadata requirements.
- Cross-domain dependencies.
- Evidence traceability.
- Mapping to external frameworks and regulatory regimes.
- Version and review dependencies.

---

## Document hierarchy

| Level | Type | Function | Parent Relationship | Output |
| --- | --- | --- | --- | --- |
| 1 | Charter | Defines authority and governance lifecycle. | Repository root authority. | Mandate, scope, principles, approval model. |
| 2 | Framework | Defines domain operating model. | Derived from charter. | Scope, lifecycle, domain roles, integration points. |
| 3 | Policy | States binding intent. | Derived from charter or framework. | Mandatory principles and governance commitments. |
| 4 | Standard | Defines measurable requirements. | Implements one or more policies. | Control baselines and acceptance criteria. |
| 5 | Procedure | Defines multi-actor or cross-functional execution steps. | Implements a standard or policy. | Workflow, inputs, outputs, approvals, records. |
| 6 | SOP | Defines a single-actor or narrow team sequence for one repeatable task. | Implements a procedure, standard, or policy at task level. | Task steps, owner, inputs, outputs, evidence. |
| 7 | Plan | Defines coordinated response or recovery actions. | Implements resilience, incident, migration, or continuity requirements. | Activation criteria, roles, communications, recovery actions. |
| 8 | Roadmap | Defines a multi-phase forward strategy tied to a strategic outcome. | Derived from a policy, framework, or charter that sets the strategic direction. | Phased milestones, dependencies, decision points, target state. |
| 9 | Guideline | Provides advisory implementation detail. | Interprets policy or standard requirements. | Options, examples, interpretation support. |
| 10 | Guide | Provides technical reference material organized for adoption. | Supports a policy, standard, or guideline with reference patterns. | Patterns, examples, configuration models, implementation walkthroughs. |
| 11 | Register | Records authoritative structured data. | Supports frameworks, policies, standards, and procedures. | Inventory, obligation, risk, exception, evidence, or metric records. |
| 12 | Matrix | Maps relationships. | Supports assurance and traceability. | Control, risk, obligation, evidence, and lifecycle mapping. |
| 13 | Specification | Defines technical or structural requirements. | Supports artefact creation, interface definition, or evidence structure. | Field definitions, schema, structural rules, acceptance criteria. |
| 14 | Template | Provides reusable record format. | Supports procedures, plans, or registers. | Forms, logs, assessments, questionnaires, and evidence capture structures. |
| 15 | Annex | Provides supplementary domain-specific guidance. | Subordinate to a parent framework, policy, or standard. | Jurisdiction, sector, or regime overlay content. |
| 16 | Checklist | Provides a structured verification list. | Supports a procedure, standard, or gate review. | Verification items, completion criteria, sign-off evidence. |
| 17 | Worklist | Provides a time-bounded execution checklist for a specific verification, remediation, or campaign batch. | Supports a procedure, register, or specification with a finite scope of work. | Numbered work items, expected values, verifier notes, completion log. |

---

## Relationship rules

1. Every framework must identify its governing charter or parent framework.
2. Every policy must identify the framework or charter that authorizes it.
3. Every standard must identify at least one parent policy.
4. Every procedure must identify the standard or policy that it implements.
5. Every SOP must identify the procedure, standard, or policy whose task it operationalizes.
6. Every plan must identify the event, condition, or lifecycle stage that activates it.
7. Every roadmap must identify the policy, framework, or charter that sets its strategic outcome.
8. Every guideline must identify the policy or standard requirement it interprets.
9. Every guide must identify the policy, standard, or guideline whose adoption it supports.
10. Every register must identify the process or control family that maintains it.
11. Every matrix must identify each mapped source and target class.
12. Every specification must identify the artefact class, interface, or evidence structure it governs.
13. Every template must identify the record, evidence, or workflow it captures.
14. Every annex must identify the parent framework, policy, or standard to which it is subordinate.
15. Every checklist must identify the procedure, standard, or gate it verifies.

---

## Cross-domain dependencies

| Source Domain | Dependent Domain | Typical Dependency |
| --- | --- | --- |
| Governance | All domains | Charter, document control, role authority, definitions, classification, metrics. |
| Risk | Governance | Risk appetite, exception acceptance, enterprise risk reporting. |
| Compliance | Governance, Risk | Obligations register, audit evidence, CAPA linkage to risk register. |
| AI | Privacy | Personal data, training data, inference data, sensitive attributes, data subject rights. |
| AI | Supply Chain | External model providers, cloud-hosted inference, managed platforms, third-party datasets. |
| AI | Resilience | Model service continuity, dependency failure, recovery objectives, emergency shutdown, degraded mode. |
| AI | Dev Security | AI-specific developer security requirements, LLM security rules, agent security patterns. |
| Privacy | Supply Chain | Processor/subprocessor due diligence, transfer assessment, breach notification, deletion assurance. |
| Supply Chain | Resilience | External dependency concentration, recovery commitments, exit plans, supply-chain continuity. |
| Operations | Security | Infrastructure security standards, monitoring requirements, change control alignment. |
| Dev Security | Security | Secure development policy alignment, code-level control requirements. |
| Resilience | Governance | Metrics, exceptions, risk register updates, governance review. |

---

## Evidence flow

Evidence flows upward from operational execution to governance reporting:

1. Procedures and templates create records.
2. Registers consolidate records into authoritative inventories or logs.
3. Matrices map records to controls, obligations, risks, and lifecycle stages.
4. Metrics registers evaluate coverage, effectiveness, timeliness, and residual exposure.
5. Frameworks use those outputs for governance review and improvement.

Evidence examples include policy approval records, control assessment results, access reviews, impact assessments, model cards, supplier reviews, business continuity tests, incident records, exception approvals, deletion attestations, and risk acceptance decisions.

---

## External framework mapping rules

External mappings must be original summaries or identifiers. They must not copy restricted third-party control text, questionnaire text, guidance text, or metrics catalogue text.

Mappings should use the following pattern:

| Field | Requirement |
| --- | --- |
| Reference Family | Name of framework, standard, regulatory regime, or assurance family. |
| Reference Identifier | Public identifier where allowed, such as section, domain, control family, or publication number. |
| Mapping Type | Legal obligation, regulatory interpretation, industry practice, architectural recommendation, or evidence category. |
| Applicability Condition | Deployment, data, sector, jurisdiction, processing role, or service condition that activates relevance. |
| Repository Artefact | Document path in this repository. |
| Evidence Class | Record type that would support implementation in an adopting organization. |
| Limitation | Statement that mapping does not prove compliance or certification. |

---

## Document review dependencies

A change in one document may require review of other documents.

| Change Trigger | Review Required |
| --- | --- |
| Charter change | All frameworks and registers. |
| Framework change | Dependent policies, standards, procedures, registers, and matrices. |
| Policy change | Dependent standards, procedures, plans, templates, and training material. |
| Standard change | Procedures, evidence templates, metrics, and assurance tests. |
| Regulatory change | Applicability register, affected policies, affected standards, and mappings. |
| External framework version change | Cross-framework matrix, affected domains, and evidence expectations. |
| AI threat pattern change | AI security standard, AI risk procedure, supplier framework, privacy policy, and resilience framework. |

---

## Quality control

Before publication, each document must be checked for:

- Correct metadata.
- Correct repository path.
- No real organization names.
- No real person names.
- No internal identifiers.
- No copied restricted third-party text.
- Role-based ownership and approval.
- Clear parent and dependent artefacts.
- Accurate distinction between obligation, interpretation, practice, and recommendation.

---

**End of Document**
