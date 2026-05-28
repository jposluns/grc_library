# Data Protection and Privacy Breach Response Procedure

**Document Title:** Data Protection and Privacy Breach Response Procedure 
**Document Type:** Procedure 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Privacy Owner 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](procedure-security-incident-reporting-and-escalation.md), [`resilience/plan-crisis-communication.md`](plan-crisis-communication.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) 
**Classification:** Public 
**Category:** Resilience 
**Review Frequency:** Annual and upon material privacy, data protection, incident, AI, supplier, or regulatory change 
**Repository Path:** [`resilience/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines a reusable process for identifying, containing, assessing, escalating, documenting, notifying, remediating, and closing suspected or confirmed privacy and data protection breaches.

---

## Scope

This procedure applies to suspected or confirmed unauthorized access, disclosure, loss, alteration, destruction, retention failure, deletion failure, misuse, or exposure of personal data, sensitive data, regulated data, confidential data, employee data, customer data, AI data, prompts, outputs, retrieval stores, logs, or supplier-held records.

---

## Procedure

### Step 1: identify and report

Report suspected privacy or data protection breaches through the approved incident reporting path. Record the source, date, affected data classes, affected systems, supplier involvement, and immediate containment needs.

### Step 2: contain

Take proportionate containment actions to limit further access, disclosure, loss, alteration, or misuse while preserving evidence. Containment may include access removal, credential rotation, service isolation, supplier escalation, data flow suspension, AI system disablement, retrieval store restriction, or log preservation.

### Step 3: assess data impact

Assess affected data categories, number of affected records or individuals where known, sensitivity, identifiability, exposure duration, recipient or attacker access, cross-border implications, supplier handling, and likelihood of harm.

### Step 4: assess legal, regulatory, and contractual context

Determine whether legal, regulatory, contractual, customer, employment, sector, insurance, or data subject notification requirements may apply. This determination depends on jurisdiction, processing role, data category, harm threshold, affected population, and contractual commitments.

### Step 5: decide notification path

Document whether notification is required, not required, deferred pending investigation, or subject to legal privilege or further review. Notifications may include affected individuals, regulators, customers, suppliers, insurers, law enforcement, or internal governance roles.

### Step 6: remediate

Remediate control failures, access gaps, supplier issues, retention failures, deletion failures, AI data handling defects, logging gaps, monitoring gaps, or process failures identified during investigation.

### Step 7: close

Close the breach record only when facts, impact, notification decisions, remediation, residual risk, evidence, and approval are complete.

---

## AI and data-specific considerations

Where AI systems are involved, assess:

- Prompt or file data exposure.
- Output disclosure of personal or regulated data.
- Retrieval leakage.
- Training or tuning data exposure.
- Model inversion or membership inference risk.
- Data poisoning effects on impacted individuals.
- Supplier model or platform retention.
- Logs, embeddings, vectors, caches, monitoring records, and deletion feasibility.
- Provenance and lineage gaps.

---

## Minimum record fields

| Field | Description |
| --- | --- |
| Breach ID | Internal identifier. |
| Report Source | Role or channel reporting the issue. |
| Data Categories | Personal, sensitive, confidential, regulated, AI, employee, customer, supplier, or other. |
| Affected Systems or Suppliers | Generic system, service, supplier, or AI system category. |
| Incident Summary | Factual summary. |
| Containment Actions | Actions taken to limit exposure. |
| Impact Assessment | Data impact, harm likelihood, and uncertainty. |
| Notification Decision | Required, not required, pending, or deferred. |
| Remediation Actions | Actions required and owner role. |
| Residual Risk | Remaining exposure after response. |
| Closure Approval | Role approving closure. |

---

## Limitations

This procedure is a public-domain baseline and does not determine notification obligations. Adopting organizations must validate obligations against applicable laws, regulations, contracts, processing role, jurisdiction, data category, and facts.

---

**End of Document**
