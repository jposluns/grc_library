# Cross-Domain Incident Coordination Procedure

**Document Title:** Cross-Domain Incident Coordination Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Resilience Owner 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](procedure-security-incident-reporting-and-escalation.md), [`resilience/plan-crisis-communication.md`](plan-crisis-communication.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md), [`security/sop-security-ticket-reporting-scheme.md`](../security/sop-security-ticket-reporting-scheme.md) 
**Classification:** Public 
**Category:** Resilience 
**Review Frequency:** Annual and upon material incident, threat, system, supplier, AI, privacy, or regulatory change 
**Repository Path:** [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines how an incident is coordinated across domains when more than one response stream is involved: information security, privacy, supplier, AI, operations, communications, legal, and executive. It provides the common lifecycle, handoff points, and shared expectations that the domain-specific procedures build on.

This procedure does not replace the domain-specific procedures. Technical security incident handling is governed by [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). Personal data breach assessment and regulatory notification are governed by [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md). This procedure governs the joint, cross-stream coordination.

---

## Scope

This procedure applies whenever an incident triggers, or is likely to trigger, response activity in more than one domain. Typical triggers include personal data exposure during a security incident, supplier-originated incidents with downstream customer impact, AI system incidents that affect personal data or operational services, and operational incidents that escalate to crisis governance. Single-domain incidents continue to be handled within the responsible domain's procedure.

---

## Incident response lifecycle

| Phase | Activities | Outputs |
| --- | --- | --- |
| Preparation | Define roles, playbooks, evidence handling, communications, monitoring, access, and tooling. | Response plan, contact roles, playbooks, evidence procedures. |
| Detection and Triage | Identify event, validate severity, assess scope, classify incident, and preserve evidence. | Triage record, severity classification, evidence hold. |
| Containment | Limit harm, isolate affected assets, restrict access, disable unsafe functions, and coordinate supplier action. | Containment record, access changes, supplier escalation. |
| Eradication | Remove threat, correct weakness, revoke credentials, patch, reconfigure, or disable unsafe capability. | Eradication record, remediation actions. |
| Recovery | Restore services, validate integrity, monitor recurrence, and confirm business acceptance. | Recovery validation, return-to-service approval. |
| Post-Incident Review | Identify root causes, control gaps, failed assumptions, evidence gaps, and corrective actions. | Lessons learned, corrective action log, risk updates. |

---

## Severity factors

Incident severity should consider:

- Data sensitivity.
- Number of affected users or records.
- Business criticality.
- Safety impact.
- Legal or regulatory exposure.
- Supplier involvement.
- Service outage duration.
- Privileged access compromise.
- Identity or credential compromise.
- Ransomware, destructive activity, or data exfiltration.
- AI prompt injection, unsafe tool execution, data poisoning, model inversion, membership inference, retrieval leakage, or unauthorized training data exposure.

---

## Procedure

1. **Detect:** Receive alert, report, monitoring signal, supplier notice, user report, or anomaly.
2. **Triage:** Validate facts, scope, severity, affected data, affected systems, impacted services, and immediate containment needs.
3. **Assign:** Appoint incident lead, technical lead, communications lead, privacy lead, legal or compliance lead, supplier lead, and evidence custodian where applicable.
4. **Contain:** Execute containment actions proportionate to severity while preserving evidence and service continuity where feasible.
5. **Investigate:** Determine cause, timeline, affected assets, affected data, attacker or failure behaviour, control gaps, and evidence sufficiency.
6. **Eradicate:** Remove cause and unauthorized access paths, remediate vulnerabilities, disable unsafe AI functions, rotate credentials, update controls, or isolate suppliers.
7. **Recover:** Restore systems, data, integrations, monitoring, logging, and business process function. Validate integrity and security before return to service.
8. **Communicate:** Provide approved internal and external updates according to legal, privacy, contractual, regulatory, and executive communication requirements.
9. **Review:** Conduct post-incident review, assign corrective actions, update risk registers, and revise controls or procedures.
10. **Close:** Close only when evidence, remediation, communications, residual risk, and accountable approval are complete.

---

## Evidence requirements

Maintain incident record, timeline, affected assets, affected data categories, severity decision, containment actions, evidence index, communications, supplier records, recovery validation, legal or privacy decisions where applicable, corrective actions, and closure approval.

---

## Limitations

This procedure is a public-domain baseline. Adopting organizations must define specific playbooks, detection rules, contact lists, legal review process, regulatory notification procedure, and forensic evidence handling internally.

---

**End of Document**
