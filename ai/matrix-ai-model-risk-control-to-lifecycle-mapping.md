# AI Model Risk Control to Lifecycle Mapping Matrix

**Document Title:** AI Model Risk Control to Lifecycle Mapping Matrix\
**Document Type:** Matrix\
**Version:** 1.0.0\
**Date:** 2026-05-27\
**Owner:** AI System Inventory Keeper\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material model, data, framework, threat, or assurance change\
**Repository Path:** [`ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`](matrix-ai-model-risk-control-to-lifecycle-mapping.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This matrix maps AI model risk control areas to lifecycle stages and evidence classes. It consolidates model risk mapping into a single original CC0 artefact without reproducing third-party framework control text.

---

## Lifecycle mapping

| Control Area | Design | Data Preparation | Development | Validation | Deployment | Monitoring | Re-evaluation | Retirement | Evidence Class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Approved purpose and prohibited use | Required | Review | Review | Validate | Approve | Monitor | Review | Archive | Use case record, approval record. |
| Data provenance and permitted use | Define | Required | Review | Validate | Approve | Monitor | Review | Retain or delete | Data provenance record, rights review. |
| Data lineage | Define | Required | Required | Validate | Approve | Monitor | Review | Retain or delete | Data lineage record. |
| Data classification | Define | Required | Review | Validate | Approve | Monitor | Review | Retain or delete | Classification record. |
| Interpretability expectations | Define | Review | Develop | Validate | Approve | Monitor | Review | Archive | Model card, interpretability evidence. |
| Representation and bias review | Define | Required | Review | Validate | Approve | Monitor | Review | Archive | Representation analysis, bias review. |
| Adversarial robustness | Define | Review | Develop | Required | Approve | Monitor | Re-test | Archive | Adversarial evaluation summary. |
| Prompt injection testing | Define | Review | Develop | Required | Approve | Monitor | Re-test | Retire controls | Test result, threat model. |
| Data poisoning review | Define | Required | Review | Validate | Approve | Monitor | Review | Retain or delete | Data quality and contamination review. |
| Model inversion and membership inference exposure | Define | Review | Review | Validate | Approve | Monitor | Re-test | Archive | Privacy and security test summary. |
| Retrieval leakage control | Define | Required | Develop | Validate | Approve | Monitor | Review | Delete stores where applicable | Retrieval permission review. |
| Unsafe tool use control | Define | Review | Develop | Validate | Approve | Monitor | Review | Revoke access | Tool permission review. |
| Human oversight | Define | Review | Design | Validate | Approve | Monitor | Review | Archive | Oversight model, escalation procedure. |
| Monitoring and drift detection | Define | Review | Develop | Validate | Approve | Required | Review | Archive | Monitoring plan, drift records. |
| Incident response linkage | Define | Review | Review | Validate | Approve | Required | Review | Archive | Incident playbook link, incident record. |
| Supplier model governance | Define | Required | Review | Validate | Approve | Monitor | Review | Exit or delete | Supplier assessment, contract controls. |
| Retirement and deletion | Define | Review | Review | Validate | Approve | Monitor | Review | Required | Retirement checklist, deletion attestation. |

---

## Framework alignment notes

External framework alignment should be recorded at a high level using framework names, domains, and evidence categories only. Do not reproduce third-party control statements, questionnaire text, implementation guidance, audit guidance, or metrics catalogues unless the material is confirmed CC0-compatible.

Suggested alignment families include AI management, AI risk management, information security, privacy, cloud controls, adversarial AI, LLM risk, secure engineering, supplier governance, and operational resilience.

---

## Maintenance rules

1. Add new control areas only where they materially improve lifecycle traceability.
2. Keep evidence classes generic and organisation-neutral.
3. Do not use this matrix to imply certification, compliance, or operating effectiveness.
4. Update related AI model risk documents when lifecycle stages or control areas change.

---

**End of Document**
