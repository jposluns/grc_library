# Incident Response Procedure

**Document Title:** Incident Response Procedure
**Document Type:** Procedure
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Security Owner
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `security/policy-information-security.md`, `security/standard-logging-and-monitoring.md`, `resilience/framework-business-continuity-and-resilience.md`, `resilience/procedure-security-incident-reporting-and-escalation.md`, `resilience/plan-crisis-communication.md`, `resilience/procedure-data-protection-and-privacy-breach-response.md`
**Classification:** Public
**Category:** Resilience
**Review Frequency:** Annual and upon material incident, threat, system, supplier, AI, privacy, or regulatory change
**Repository Path:** `resilience/procedure-incident-response.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This procedure defines a reusable incident response lifecycle for identifying, triaging, containing, eradicating, recovering from, documenting, and learning from security, privacy, technology, supplier, operational, and AI-related incidents.

---

## Scope

This procedure applies to incidents affecting confidentiality, integrity, availability, privacy, safety, operations, suppliers, cloud services, AI systems, logs, identities, data stores, applications, infrastructure, or critical business services.

---

## Incident Response Lifecycle

| Phase | Activities | Outputs |
| --- | --- | --- |
| Preparation | Define roles, playbooks, evidence handling, communications, monitoring, access, and tooling. | Response plan, contact roles, playbooks, evidence procedures. |
| Detection and Triage | Identify event, validate severity, assess scope, classify incident, and preserve evidence. | Triage record, severity classification, evidence hold. |
| Containment | Limit harm, isolate affected assets, restrict access, disable unsafe functions, and coordinate supplier action. | Containment record, access changes, supplier escalation. |
| Eradication | Remove threat, correct weakness, revoke credentials, patch, reconfigure, or disable unsafe capability. | Eradication record, remediation actions. |
| Recovery | Restore services, validate integrity, monitor recurrence, and confirm business acceptance. | Recovery validation, return-to-service approval. |
| Post-Incident Review | Identify root causes, control gaps, failed assumptions, evidence gaps, and corrective actions. | Lessons learned, corrective action log, risk updates. |

---

## Severity Factors

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

## Evidence Requirements

Maintain incident record, timeline, affected assets, affected data categories, severity decision, containment actions, evidence index, communications, supplier records, recovery validation, legal or privacy decisions where applicable, corrective actions, and closure approval.

---

## Limitations

This procedure is a public-domain baseline. Adopting organizations must define specific playbooks, detection rules, contact lists, legal review process, regulatory notification procedure, and forensic evidence handling internally.

---

**End of Document**
