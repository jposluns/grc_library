# Cross-Domain Incident Coordination Procedure

**Document Title:** Cross-Domain Incident Coordination Procedure\
**Document Type:** Procedure\
**Version:** 1.1.1\
**Date:** 2026-06-22\
**Owner:** Resilience Owner\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](procedure-security-incident-reporting-and-escalation.md), [`resilience/plan-crisis-communication.md`](plan-crisis-communication.md), [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md), [`security/sop-security-ticket-reporting-scheme.md`](../security/sop-security-ticket-reporting-scheme.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material incident, threat, system, supplier, AI, privacy, or regulatory change\
**Repository Path:** [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how an incident is coordinated across domains when more than one response stream is involved: information security, privacy, supplier, AI, operations, communications, legal, and executive. It provides the common lifecycle, the domain-ownership decision rule, the joint command structure, and the hand-off checklists that the domain-specific procedures build on.

This procedure does not replace the domain-specific procedures. Technical security incident handling is governed by [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). Personal data breach assessment and regulatory notification are governed by [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md). Supplier-originated incidents draw on [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md). AI-related incidents draw on [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md). This procedure governs the joint, cross-stream coordination among them.

---

## Scope

This procedure applies whenever an incident triggers, or is likely to trigger, response activity in more than one domain. Typical triggers include personal data exposure during a security incident, supplier-originated incidents with downstream customer impact, AI system incidents that affect personal data or operational services, and operational incidents that escalate to crisis governance. Single-domain incidents continue to be handled within the responsible domain's procedure.

---

## Domain ownership decision rule

Each incident is assigned a primary owning domain and zero or more participating domains. The owning domain runs the technical response. Participating domains run their own parallel streams with their own deliverables, coordinated through this procedure.

| Incident class | Primary owning domain | Participating domains (typical) |
| --- | --- | --- |
| Confirmed or suspected security breach without personal data exposure | Security | Operations, Communications |
| Security breach with personal data exposure | Security (technical) and Privacy (notification stream) jointly | Communications, Legal, Operations |
| Personal data disclosure without security breach (e.g. accidental email, lost device with encrypted data) | Privacy | Security (if security control gap), Legal |
| Supplier breach affecting organisation data | Supplier (coordination with supplier) | Security, Privacy, Legal, Communications |
| AI system safety or security incident not involving personal data | AI | Security, Operations, Legal |
| AI system incident involving personal data | AI and Privacy jointly | Security, Communications, Legal |
| Operational service outage with no security or privacy implication | Operations | Communications, Resilience (if continuity activated) |
| Operational service outage with security or privacy implication | Operations and Security or Privacy jointly | Communications, Resilience, Legal |
| Pandemic, physical site, or workforce disruption | Resilience | Operations, Communications, HR, Legal |
| Regulator-initiated investigation triggering operational response | Compliance and Legal jointly | Privacy, Security, Communications |
| Crisis-level incident (any class above declared at P1 with material reputational, regulatory, or service impact) | Resilience activates the crisis governance overlay; primary domain ownership continues underneath | All applicable domains |

If a domain is unsure whether it owns an incident, default to declaring jointly and resolving the primary owner at the first coordination call. Do not delay containment to resolve ownership.

---

## Joint command structure

When two or more domains are participating, the coordination is run by an **Incident Coordinator** appointed at the start of the incident. The Coordinator does not direct technical response inside any domain; the Coordinator manages cross-stream timing, decisions, and communications.

| Role | Selection rule | Responsibilities |
| --- | --- | --- |
| Incident Coordinator | Resilience Owner for P1; primary-domain lead otherwise | Owns the cross-stream timeline, the joint decision log, and the communication cadence. Convenes coordination calls. Escalates blockers to the Executive Sponsor. |
| Primary-domain Lead | Set by the domain procedure (e.g. CISO for security, Privacy Officer for privacy, Supplier Risk Maintainer for supplier) | Runs the technical response within their domain. Reports status into each coordination call. |
| Participating-domain Lead(s) | Same selection rule per participating domain | Runs parallel response within their domain. Hands off evidence and decisions to the Primary-domain Lead as needed. |
| Communications Lead | Communications Owner | Owns external messaging, regulator-facing messaging, employee messaging, and customer messaging. Coordinates with Legal and primary-domain Leads on content approval. |
| Legal Lead | Legal Counsel | Owns regulatory notification determinations, privilege decisions, litigation hold, and contractual notice obligations. |
| Executive Sponsor | Designated by role per severity (CISO or Privacy Officer for P2; CIO for P1 affecting multiple domains; CEO for crisis-level events) | Approves decisions that exceed Coordinator authority. Owns the executive briefing line. |
| Evidence Custodian | SOC or domain-specific custodian | Owns the evidence index across all streams. Maintains chain of custody for forensic, legal, and audit purposes. |

For P1 events, the Incident Coordinator and Executive Sponsor are notified within 15 minutes of declaration. The Joint Command convenes within 1 hour of declaration.

---

## Coordination lifecycle

The coordination lifecycle mirrors the domain procedures but layers cross-stream synchronisation points on top.

| Phase | Cross-stream activities | Outputs |
| --- | --- | --- |
| Preparation | Maintain the coordination roster, contact register, decision log template, communication templates, joint exercise schedule, and after-action format. | Coordination roster, register, templates, exercise log. |
| Declaration | Confirm cross-domain trigger, appoint Incident Coordinator, declare participating domains, open the joint decision log, schedule the first coordination call. | Declaration record, joint decision log opened. |
| Joint triage | Each participating domain confirms its own triage, severity, and immediate containment needs. Coordinator confirms domain assignments per the ownership decision rule. | Joint triage record, severity decision, ownership confirmation. |
| Synchronised containment | Each domain executes containment per its own procedure; cross-stream decisions (e.g. service shutdown, supplier isolation, AI tool suspension) routed through the Coordinator. | Containment timeline, cross-stream decisions recorded. |
| Investigation | Each domain investigates within its scope; Coordinator owns the consolidated timeline, the shared evidence index, and the cross-domain root cause draft. | Consolidated timeline, joint evidence index, root cause draft. |
| Notification and communication | Privacy and Legal own regulatory notification streams; Communications owns external messaging. All public statements approved by Executive Sponsor. | Notification records, communication log, approval evidence. |
| Recovery and validation | Each domain validates within its scope; Coordinator confirms cross-domain dependencies are satisfied before return to service. | Recovery validation by domain, joint return-to-service approval. |
| Joint post-incident review | Multi-domain PIR within 10 business days of closure for P1 and P2 events. Output is one consolidated PIR; per-domain PIRs feed into it. | Joint PIR report, corrective action register, lessons learned. |
| Closure | All domains confirm independent closure criteria are met; Executive Sponsor signs joint closure. | Joint closure record, residual risk acceptance. |

---

## Hand-off checklists

These checklists govern the transitions between streams. The Coordinator confirms each item before the hand-off completes.

### Security to Privacy hand-off (when personal data is implicated)

1. Confirmed scope of personal data potentially exposed, by data category and approximate volume.
2. Forensic evidence of access, exfiltration, or modification, with timestamps in UTC.
3. List of affected data subjects, processing roles, and jurisdictions, to the extent known.
4. Suspected attack vector and time-of-first-compromise estimate to support the "becoming aware" determination under GDPR Article 33.
5. Containment status: whether the breach is contained and whether further data is at risk.
6. Authorisation for the Privacy stream to take parallel actions (e.g. request supplier preservation, contact the Privacy regulator).

### Security to Supplier hand-off (when a supplier or processor is implicated)

1. Identity of the supplier, the affected service, and the data or systems involved.
2. Whether the supplier has been notified, by whom, when, and through which contractual channel.
3. Required preservation actions and the contractual deadline for them.
4. Whether supplier access should be restricted or revoked, and the authority to do so.
5. Evidence the supplier is expected to provide and the format and deadline.
6. Communication boundary: who at the supplier and at the organisation may discuss the incident, and what is on or off the record.

### Security to AI hand-off (when an AI system is implicated)

1. AI system identifier, model identifier, version, and provider, from the AI system register.
2. Affected capabilities (prompt, retrieval, agent tool use, training pipeline, inference endpoint).
3. Specific AI risks engaged (prompt injection, indirect injection, data poisoning, model inversion, membership inference, retrieval leakage, unsafe tool execution, training data leakage).
4. Decision on capability suspension: which AI capabilities are suspended pending investigation, by whose authority.
5. Whether training, fine-tuning, or retrieval pipelines must be paused.
6. Whether supplier model provider must be notified per contract and within what window.

### Privacy to Communications hand-off (when external notification is required)

1. Confirmed scope and severity of the personal data breach.
2. Regulatory notifications submitted or scheduled, by jurisdiction, with submission timestamps and reference numbers.
3. Whether data subject notification is required, the population, the channel, and the timing.
4. Approved messaging content from Legal, including any required regulator-approved language.
5. Embargo, sequencing, and channel rules (e.g. regulator before public, customers before media, employees before external).
6. Escalation path if a journalist, regulator, or customer initiates contact ahead of the planned sequence.

### Any domain to Resilience hand-off (crisis activation)

1. Trigger met for crisis governance under [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md): material reputational, regulatory, service, or safety impact.
2. Crisis Coordinator named; Executive Sponsor identified.
3. Continuity activation needed (yes / no), and if yes which services are affected.
4. Communication state: existing approvals, current messaging, embargo posture.
5. Open decisions requiring crisis-level authority.
6. Resource needs: staffing, supplier engagement, external counsel, external IR partner.

---

## Severity rules across streams

Severity is determined inside each domain by its own procedure. When the same event has different severities in different domains, the **highest** applicable severity governs the coordination cadence. The Incident Coordinator records the per-domain severities and the governing severity in the joint decision log.

| Joint coordination severity | Coordination call cadence | Executive Sponsor cadence | Joint PIR deadline |
| --- | --- | --- | --- |
| P1 Critical | Every 2 hours during active response | Briefed at declaration and at least every 4 hours | Within 5 business days of closure |
| P2 High | Every 8 business hours during active response | Briefed at declaration and daily | Within 10 business days of closure |
| P3 Medium | Daily during active response | Briefed at declaration and at closure | Within 15 business days of closure |
| P4 Low | At Coordinator discretion | Closure-only briefing | At Coordinator discretion |

---

## Joint decision log

The Joint decision log is the authoritative cross-stream record for the incident. It is maintained by the Incident Coordinator and includes:

| Field | Description |
| --- | --- |
| Decision ID | Unique identifier within the incident |
| Timestamp (UTC) | When the decision was made |
| Decision | The decision text |
| Domains affected | Which response streams are bound by the decision |
| Decision authority | Role that approved the decision |
| Rationale | One- or two-sentence justification |
| Dissent (if any) | Any participating-domain Lead who disagreed and the alternative they proposed |
| Implementation owner | Role responsible for executing the decision |
| Status | Pending, In progress, Done, Reversed |

Decisions reversed during the incident are not deleted; the reversal is logged as a new entry referencing the original.

---

## Cross-stream evidence handling

The Evidence Custodian maintains a single evidence index spanning all streams. Each item in the index records source, collection timestamp, custodian, integrity hash where applicable, and the streams that depend on it.

Evidence that crosses streams (for example, a SIEM extract used by Security, Privacy, and Legal) is captured once and referenced by all consuming streams. The Custodian is responsible for chain of custody across the full incident lifecycle, including hand-off to external forensic providers or law enforcement.

Retention follows the strictest applicable rule across streams: typically seven years per the records retention standard, longer where litigation hold or regulatory investigation applies.

---

## Communication boundaries

Cross-stream communication discipline reduces leakage and conflicting messages.

1. Internal communication about an active incident is restricted to the joint roster plus role-specific need-to-know.
2. External communication outside the approved channels is prohibited. Customer, regulator, journalist, and partner contact is routed to the Communications Lead.
3. Supplier communication during an active supplier-implicated incident is routed through the Supplier-domain Lead with copy to the Coordinator.
4. Legal privilege is preserved where applicable; the Legal Lead designates which communications are privileged and which are not.
5. No public statement about the incident is made without Executive Sponsor approval and Legal review.

---

## Joint post-incident review

The Joint PIR is a single consolidated post-incident review that supersedes per-domain PIRs for cross-domain incidents. Per-domain PIR inputs feed into it. The Joint PIR covers:

1. Timeline reconstruction across all streams, with UTC timestamps.
2. Per-domain root cause and the consolidated root cause where applicable.
3. Control gaps identified, by domain and by control family.
4. Coordination effectiveness: hand-off latency, decision quality, communication clarity, dissent handling.
5. Detection effectiveness across streams: which stream detected first, mean time to detect by domain.
6. Containment effectiveness across streams: time to contain by domain, presence of any cross-stream delay.
7. Notification compliance: deadline adherence by regulation and by jurisdiction.
8. Corrective actions, with named role owners, deadlines, and tracking in the corrective action register.
9. Risk register updates across the affected domains.
10. Recommendations for procedure or control changes.

The Joint PIR is owned by the Incident Coordinator, signed by the Executive Sponsor, and provided to Internal Audit. The PIR report classification follows the highest classification of its source domains, typically Restricted in adopting organisations.

---

## Joint exercises

Cross-stream coordination must be exercised at minimum annually. Exercises rotate through scenario classes: security plus privacy, security plus supplier, AI plus security plus privacy, operational outage plus crisis activation. Each exercise produces an after-action report tracked in the resilience metrics register, and corrective actions feed the corrective action register.

---

## Metrics

The Incident Coordinator reports cross-stream coordination metrics at the quarterly governance review:

| Metric | Definition | Target |
| --- | --- | --- |
| Cross-stream incident count | Total incidents in the period that triggered coordination | Trend-monitored |
| Joint Command convene time (P1) | Minutes from declaration to first Joint Command call | At most 60 minutes |
| Hand-off completeness | Percentage of hand-offs where every checklist item was confirmed | At least 95% |
| Joint PIR completion rate (P1 and P2) | Percentage completed within the deadline above | At least 95% |
| Decision-reversal rate | Joint decisions reversed during the incident | Trend-monitored; persistent increase triggers procedure review |
| Coordination satisfaction (post-incident survey) | Participating-domain Lead feedback on coordination effectiveness | At least 4 of 5 on a 5-point scale |
| Cross-stream exercise rate | Cross-stream exercises completed against the annual plan | 100% |

---

## Evidence requirements

Maintain joint declaration record, coordination roster snapshot, joint decision log, consolidated timeline, joint evidence index, per-domain hand-off checklists with completion signatures, communication log, notification submissions, joint PIR report, joint closure record, residual risk acceptance.

---

## Framework alignment

| Control area | Framework reference |
| --- | --- |
| Incident management programme | ISO/IEC 27035; ISO/IEC 27001:2022 A.5.24 to A.5.28 |
| Business continuity coordination | ISO 22301:2019 §8.4 |
| Cybersecurity incident handling | NIST SP 800-61 Rev. 3 |
| Personal data breach coordination | GDPR Articles 33 to 34; UK GDPR Articles 33 to 34; PIPL Article 57; LGPD Articles 48 to 49 |
| Operational resilience incident coordination | DORA Pillar 2; NIS 2 Articles 23 to 25 |
| Cloud incident management | CSA CCM v4.1 SEF domain |
| AI security incident response | NIST AI RMF MANAGE; ISO/IEC 42001:2023 §9 |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline for cross-stream coordination. Adopting organisations must define the named individual or role behind each Lead title, the contact register, the cadence calendar, the joint exercise scenarios, the communication channels, and the evidence repository. Regulatory notification windows referenced here are illustrative; adopting organisations must validate the windows applicable to their jurisdictions, sectors, processing roles, and contractual obligations.

---

**End of Document**
