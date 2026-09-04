# ETSI Securing-AI Baseline Alignment Matrix

**Document Title:** ETSI Securing-AI Baseline Alignment Matrix\
**Document Type:** Matrix\
**Version:** 0.0.1\
**Date:** 2026-09-04\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md), [`ai/guide-ai-security-technical-implementation.md`](guide-ai-security-technical-implementation.md), [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon a change to the ETSI Securing-AI baseline, its guidance, or a mapped carrier document\
**Repository Path:** [`ai/matrix-etsi-sai-baseline-alignment.md`](matrix-etsi-sai-baseline-alignment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This matrix maps the ETSI EN 304 223 V2.1.1 (2025-12) Securing-AI (SAI) baseline, its 13 principles across five secure-lifecycle phases, to the library's AI security carrier documents, and records where coverage is partial or absent. It gives a single auditable surface for baseline coverage and for the gaps and partial-coverage areas that further AI-assurance content would fill. It is an original CC BY-SA 4.0 crosswalk: it references ETSI provision identifiers and the corpus carriers that implement them, without reproducing third-party standard text.

The baseline is normative (EN 304 223 states `shall` and `should` provisions). The ETSI TR 104 128 V1.1.1 (2025-05) implementation guide and the ETSI GR SAI group-report family are informative companions (see the note at the end); a mapping to an informative companion is an orientation, never an obligation, and is marked as such.

---

## Baseline structure

EN 304 223 organizes its provisions under 13 principles grouped into five secure-lifecycle phases, and names five stakeholder roles (Developer, System Operator, Data Custodian, End-user, Affected Entity). Each provision carries a `shall` (mandatory) or `should` (recommended) modality.

| Phase | Principles |
| --- | --- |
| 5.1 Secure Design | P1 Raise awareness; P2 Design for security; P3 Evaluate the threats and manage the risks; P4 Enable human responsibility |
| 5.2 Secure Development | P5 Identify, track and protect assets; P6 Secure the infrastructure; P7 Secure the supply chain; P8 Document data, models and prompts; P9 Conduct appropriate testing and evaluation |
| 5.3 Secure Deployment | P10 Communicate with End-users and Affected Entities |
| 5.4 Secure Maintenance | P11 Maintain security updates and mitigations; P12 Monitor the system's behaviour |
| 5.5 Secure End of Life | P13 Proper data and model disposal |

---

## Alignment map

Legend: **Covered** (a carrier substantively implements the provision); **Covered (deep)** (the corpus exceeds the baseline); **Partial** (carried by a generic or adjacent surface, or a specific sub-provision is thin); **Gap** (no corpus carrier). The corpus spine is [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), whose Section 4 minimum-requirements track the baseline closely.

| Principle (phase) | Key EN 304 223 provisions | Status | Corpus carrier (document, section) |
| --- | --- | --- | --- |
| P1 Raise awareness (5.1) | 5.1.1-1, 5.1.1-2.2 (AI-security training content) | Partial | [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md) carries generic security training; no AI-security-specific curriculum requirement |
| P2 Design for security (5.1) | 5.1.2-2 (withstand adversarial attack and failure), -1 (design assessment), -3 (design audit trail), -4/-7 (component due diligence), -6 (least privilege) | Covered | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) Section 4.5; [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md); [`ai/template-ai-vendor-security-questionnaire.md`](template-ai-vendor-security-questionnaire.md) |
| P3 Evaluate the threats and manage the risks (5.1) | 5.1.3-1/-3/-4 (threat modelling; poisoning, inversion, membership inference) | Covered (deep) | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) Section 4.5; [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md); [`ai/guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md) |
| P3 (5.1) | 5.1.3-2 (communicate unresolved threats to End-users through System Operators) | Gap | Threat catalogues and controls are carried, but not the Developer-to-System-Operator-to-End-user communication chain for threats that cannot be resolved |
| P4 Enable human responsibility (5.1) | 5.1.4-1/-3 (oversight), -2 (explainable output), -5 (prohibited uses) | Covered | [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md); [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md) |
| P5 Identify, track, protect assets (5.2) | 5.2.1-1/-2 (asset inventory, version control), -4 (protect sensitive data, weight confidentiality) | Covered | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) Section 4.1; [`ai/register-model-registry.md`](register-model-registry.md) |
| P5 (5.2) | 5.2.1-3/-3.1 (AI-tailored disaster recovery, known-good-state restore) | Partial | [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md) Recover phase (validate the model on the eval suite before restoration, canary rollout, incremental re-enable) carries AI-tailored recovery; no standalone AI disaster-recovery plan document |
| P6 Secure the infrastructure (5.2) | 5.2.2-1/-3 (access-control frameworks, dedicated environments), -2 (API rate limit), -5 (incident recovery), -6 (cloud contract) | Covered | [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md); [`ai/guide-ai-security-technical-implementation.md`](guide-ai-security-technical-implementation.md); [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md) |
| P6 (5.2) | 5.2.2-4 (implement and publish an AI vulnerability-disclosure policy) | Gap | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md) covers internal-scan triage and remediation and expressly excludes the receipt-and-disclosure process; no published AI vulnerability-disclosure policy |
| P7 Secure the supply chain (5.2) | 5.2.3-1 (secure supply chain) | Covered (deep) | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) Section 4.9; [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) |
| P7 (5.2) | 5.2.3-3 (re-run evaluations on adopted released models) | Partial | Testing in [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); no explicit obligation to re-run evaluations on a third-party released model before adoption |
| P7 (5.2) | 5.2.3-2/-2.1/-2.2 (document, and share with End-users, the justification for adopting an undocumented or unsecured component) | Gap | Vendor questionnaires and model cards exist; no obligation to document and share that justification with End-users |
| P8 Document data, models, prompts (5.2) | 5.2.4-1/-2 (audit trail, provenance) | Covered | [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md); [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md) |
| P8 (5.2) | 5.2.4-1.2 (cryptographic hashing of model components) | Partial | [`ai/register-model-registry.md`](register-model-registry.md) records a model-weight cryptographic hash, and [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) SUPPLY-SEC-05 validates a provider checksum before deployment (mapped there to 5.2.4-1.2); the developer-side obligation to release hashes for downstream verification is thinner |
| P8 (5.2) | 5.2.4-3 (prompt and config change-audit log) | Partial | [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) PROMPT-SEC-01 requires a version-controlled prompt registry with tracked, approved changes; no change-audit-log framed to the full config surface |
| P9 Testing and evaluation (5.2) | 5.2.5-1 (security-assessment testing), -4 (outputs resist reverse engineering) | Covered (deep) | [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); [`ai/guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md) |
| P9 (5.2) | 5.2.5-2.1 (independent security testers), 5.2.5-3 (Developer-to-System-Operator findings transfer) | Partial | Testing is assigned to internal development and QA teams; tester independence and the findings-transfer step are not established as requirements |
| P10 Communicate with End-users and Affected Entities (5.3) | 5.3.1-1 (data-use disclosure), 5.3.1-2.1 (appropriate-use and limitations guidance), 5.3.1-3 (incident communication) | Partial | [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md) carries intended-use and limitations; [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md) carries incident communication to affected AI actors; no consolidated System-Operator communication obligation |
| P10 (5.3) | 5.3.1-2.2 (proactively inform End-users of security-relevant updates) | Gap | No carrier for a proactive security-update notice to End-users |
| P11 Maintain security updates (5.4) | 5.4.1-2 (major update triggers new testing) | Covered | [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) regression and retest schedule |
| P11 (5.4) | 5.4.1-1/-1.1 (provide and notify security updates, contingency where none is possible), -3 (support for evaluating model changes) | Gap | Retest-on-major-update (5.4.1-2) is covered above; no carrier for the provide-and-notify-update obligation or the no-update contingency |
| P12 Monitor the system's behaviour (5.4) | 5.4.2-1..-4 (logging; anomaly, drift, poisoning detection; internal-state monitoring) | Covered | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md); [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) |
| P13 Proper disposal (5.5) | 5.5.1-1/-2 (secure transfer and disposal, decommission with Data Custodians) | Partial | [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) Section 4.11 carries retirement and deletion controls; Data-Custodian involvement and the transfer-of-ownership step are not established |

---

## Gap register

The baseline provisions below have no corpus carrier (genuine gaps) or only partial coverage. They are the candidate scope for further AI-assurance content, ranked within each group by normative weight (mandatory `shall` provisions first). Coverage was judged at the sub-provision level, so a principle can be covered on its core provisions and still carry a gap on a specific sub-provision.

### Genuine gaps (no corpus carrier)

1. **P6, implement and publish an AI vulnerability-disclosure policy** (5.2.2-4, `shall`). The internal vulnerability-management procedure expressly excludes the receipt-and-disclosure process; no published AI disclosure policy exists.
2. **P11, provide and notify security updates** (5.4.1-1, 5.4.1-1.1, `shall`; 5.4.1-3, `should`). Retest-on-major-update is covered; the obligation to provide and notify updates, and to plan for the no-update-possible case, has no carrier.
3. **P10, proactive security-update notice to End-users** (5.3.1-2.2, `shall`). No carrier requires the System Operator to proactively inform End-users of security-relevant updates.
4. **P7, share the justification for adopting an undocumented or unsecured component with End-users** (5.2.3-2/-2.1/-2.2, `shall`). No obligation to document and share that justification with End-users.
5. **P3, communicate unresolved threats to End-users** (5.1.3-2, `shall`). Threat catalogues are carried; the Developer-to-System-Operator-to-End-user communication chain for threats that cannot be resolved is not.

### Partial coverage (thin or adjacent)

6. **P1, AI-security-specific training content** (5.1.1-1, 5.1.1-2.2, `shall`). A generic training standard exists; no AI-security curriculum requirement.
7. **P5, AI-tailored disaster recovery and known-good-state restore** (5.2.1-3, `shall`; 5.2.1-3.1, `should`). The incident-response Recover phase carries AI-tailored recovery; no standalone AI disaster-recovery plan document.
8. **P8, developer-side release of model-component hashes** (5.2.4-1.2, `shall`). The consumer side is carried (model-weight hash on record, provider checksum validated); the developer-side release-of-hashes obligation is thinner.
9. **P13, Data-Custodian involvement in decommissioning** (5.5.1-1, 5.5.1-2, `shall`). Retirement and deletion controls are carried; Data-Custodian involvement and the transfer-of-ownership step are not established.
10. **P7, re-run evaluations on adopted released models** (5.2.3-3, `shall`). A testing standard exists; no explicit obligation to re-run evaluations on a third-party released model before adoption.
11. **P9, independent security testers and findings transfer** (5.2.5-2.1, `should`; 5.2.5-3, `shall`). Testing is assigned to internal teams; tester independence and the Developer-to-System-Operator findings transfer are not established.
12. **P8, prompt and configuration change-audit log** (5.2.4-3, `should`). A version-controlled prompt registry with tracked, approved changes is carried; a change-audit-log framed to the full configuration surface is thinner.

Principles P2, P4, and P12 are covered in full; P3, P5, P7, P8, and P9 are covered on their core provisions with the residuals listed above. The library is notably deeper than the baseline on adversarial testing and on access and agent-permission granularity; those are strengths, not gaps.

## Framework alignment notes

- **Normative weight.** EN 304 223 is a European Norm; its `shall` and `should` provisions are citable as a normative anchor. The TR 104 128 guide and the ETSI GR SAI reports are informative; a mapping to them is an orientation, and this matrix marks informative sources as see-also rather than as an obligation.
- **Distributed traceability.** Several carrier documents already cite specific EN 304 223 provisions in their own `Framework alignment` tables (for example [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) and [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md)). This matrix is the index across those carriers; the per-document tables are the distributed record.
- **Informative companion reports.** The ETSI GR SAI group-report family (Threat Ontology, Data Supply Chain Security, Mitigation Strategy, Role of Hardware, Explicability and Transparency) provides informative threat and mitigation taxonomies. Their themes are substantially reflected in the corpus AI-security content surveyed above; hardware and confidential-computing for AI is the thinnest theme. These reports are informative see-also, not baseline requirements.

---

## Maintenance rules

1. Re-map on any change to EN 304 223, its provision numbering, or a mapped carrier document.
2. Keep the status judgements evidence-based: a claimed carrier must substantively cover the cited provision, and a claimed gap must be absent from the corpus.
3. Do not use this matrix to imply certification, conformity assessment, or operating effectiveness against the ETSI baseline.
4. When a gap-register item is closed by new content, move it from the gap register to the alignment map in the same change.

---

**End of Document**
