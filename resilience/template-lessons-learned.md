# Lessons Learned Template

**Document Title:** Lessons Learned Template 
**Document Type:** Template 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Resilience Owner 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md), [`governance/procedure-continuous-improvement-register.md`](../governance/procedure-continuous-improvement-register.md), [`resilience/template-tabletop-exercise.md`](template-tabletop-exercise.md) 
**Classification:** Public 
**Category:** Resilience 
**Review Frequency:** Annual and upon material change to the post-incident review process 
**Repository Path:** [`resilience/template-lessons-learned.md`](template-lessons-learned.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This template defines the format of a lessons-learned report produced after a significant event: a real incident, a tabletop exercise, a recovery test, a regulatory inspection, or a major change with material disruption. The lessons-learned report is the durable record that drives systemic improvement; it is distinct from a single-domain post-incident review (PIR) in that it integrates findings across response streams and feeds the corrective action register.

A populated lessons-learned report identifies real events and is sensitive operational material. This public CC0 template intentionally contains no example values for any field.

---

## Scope

This template covers cross-stream lessons-learned reports for:

1. P1 and P2 incidents in any domain.
2. Multi-domain incidents coordinated under the cross-domain coordination procedure.
3. Cross-domain tabletop exercises and full-scale exercises.
4. Recovery tests that revealed material gaps.
5. Regulatory inspections, supervisory reviews, or auditor findings of material weakness.
6. Major change events with material customer or operational disruption.

Single-domain PIRs use the domain-specific format; this template is for cross-stream learning.

---

## Report sections

### Section 1: Event identification

| Field | Description |
| --- | --- |
| Event ID | Unique identifier; cross-reference to the incident record or exercise record |
| Event type | Incident, exercise, recovery test, regulatory event, change event |
| Date and duration | Start and end of the event |
| Severity | Highest applicable severity across all streams |
| Domains involved | Security, privacy, supplier, AI, operations, communications, legal, executive |
| Authoring role | Lead author and contributors |
| Approval | Resilience Owner and Executive Sponsor |
| Distribution | Roles and groups the report is shared with |
| Classification | Per the source-data sensitivity |

### Section 2: Executive summary

A one-page summary covering:

1. What happened, in plain language, in two to four sentences.
2. The scope of impact (customers, systems, regulators, partners).
3. The root cause in one sentence; contributing factors in three to five bullets.
4. The headline outcomes of the response (positive and negative).
5. The two or three most important systemic actions resulting from the event.

This section is the only section a busy executive reads; treat it accordingly.

### Section 3: Timeline reconstruction

A chronological narrative with UTC timestamps. Each entry records:

| Field | Description |
| --- | --- |
| Timestamp (UTC) | When the event occurred |
| Domain | The response stream the event belongs to |
| Actor | Role that took the action or to whom it happened |
| Action or event | What occurred |
| Source of truth | Where the timestamp comes from (log, ticket, decision register, communication) |

The timeline includes pre-event signals where applicable (alerts that were missed, anomalies that were normal at the time).

### Section 4: Root cause and contributing factors

| Element | Description |
| --- | --- |
| Proximate cause | The immediate technical or human action that triggered the event |
| Underlying cause | The systemic condition that allowed the proximate cause to have impact |
| Contributing factors | Specific conditions that worsened the event or slowed the response |
| Counterfactual analysis | What would have prevented the event (with high confidence) and at what cost |
| Process-not-people framing | Each finding states the system condition; named individuals are not the cause framing |

### Section 5: What worked

Items that succeeded or unexpectedly mitigated impact. This section is mandatory; absence of positive findings is itself a finding.

### Section 6: Gaps identified

Grouped by category:

| Category | Examples |
| --- | --- |
| Detection | Alert missing; alert fired but routed to a stale queue; signal-to-noise ratio too low |
| Triage | Severity miscalled; escalation delayed; ownership unclear |
| Containment | Containment too aggressive or too cautious; coordination overhead delayed action |
| Investigation | Evidence not captured; logs insufficient; lineage broken |
| Recovery | Runbook stale; dependency missed; validation gap |
| Communication | Customer confusion; regulator surprised; internal misalignment |
| Decision-making | Decisions reversed; authority unclear; documentation absent |
| Tooling | Tool gap; tool failure; alert fatigue |
| Procedure | Procedure unclear; procedure missing; procedure conflicted with another procedure |
| Training | Role unfamiliar with their part; new joiner not exercised |
| Supplier | Supplier slow; supplier escalation path stale; supplier evidence gap |
| Cross-domain coordination | Hand-off checklist incomplete; joint command convene time exceeded |

Each gap is concrete and testable. "Improve communication" is not a gap; "the customer status-page update lagged the internal status by 90 minutes during the active window" is.

### Section 7: Corrective actions

Each action is recorded as a row tracked in the corrective action register.

| Field | Description |
| --- | --- |
| Action ID | Unique identifier in the corrective action register |
| Action description | Specific, observable change |
| Linked gap | Reference to the gap identified above |
| Owner role | Role accountable for delivery |
| Implementation deadline | Calendar date |
| Acceptance criteria | How to know the action is closed |
| Risk if not delivered | What the residual risk is if the action lapses |
| Status | Open, In progress, Done, Cancelled with rationale |

Actions are SMART: specific, measurable, achievable, relevant, time-bound.

### Section 8: Procedure and control changes

| Change | Affected document | Type | Tracking |
| --- | --- | --- | --- |
| Procedure amendment | E.g. `security/procedure-security-incident-response.md` | Patch or minor version bump | Tracked in the document index |
| New procedure or template | E.g. a new tabletop scenario | New artefact starting at 0.0.1 | Added to index and domain README |
| Control update | E.g. new SIEM rule | Per the control's source of truth | Tracked in the control register |
| Risk register entry | New or revised risk | Per risk procedure | Tracked in the risk register |

### Section 9: Communication of lessons

| Audience | Channel | Content | Owner |
| --- | --- | --- | --- |
| Executive Sponsor and board | Briefing | Executive summary | Resilience Owner |
| Participating-domain Leads | Workshop | Full report | Authoring role |
| Wider operational team | Internal write-up | Sanitised summary | Domain Leads |
| Customers | Per the communications policy | Sanitised public-facing summary if material | Communications Lead |
| Regulator | Per the regulatory requirement | Required content | Legal Lead |
| Peer organisations and information-sharing groups | Per the policy | Sanitised TLP-amber content | Threat intelligence operator |

### Section 10: Metric impact

| Metric | Definition | Pre-event baseline | Post-event update | Delta |
| --- | --- | --- | --- | --- |
| Mean time to detect | Time from event onset to detection | Baseline | Current | Delta |
| Mean time to convene | Time from declaration to Joint Command convene | Baseline | Current | Delta |
| Mean time to contain | Time from declaration to containment | Baseline | Current | Delta |
| Mean time to recover | Time from declaration to full service | Baseline | Current | Delta |
| Notification-window adherence | Percentage of regulatory windows met | Baseline | Current | Delta |
| Customer satisfaction or trust signal | Per organisation's measurement | Baseline | Current | Delta |

### Section 11: Approval and signature

The Resilience Owner and Executive Sponsor sign the report. Where the event involved personal data, the Privacy Officer co-signs. Where the event involved a supplier, the Supplier Risk Maintainer co-signs.

---

## Operating expectations

1. The lessons-learned report is initiated within 5 business days of event closure for P1 and P2 events, and within 10 business days for exercises.
2. Final report is published within 20 business days of initiation; longer windows require Executive Sponsor approval.
3. Reports are stored in a location accessible to authorised roles only; classification per source-data sensitivity.
4. Corrective actions are tracked monthly until closure; ageing actions are escalated to the Executive Sponsor.
5. The aggregate of corrective actions feeds the governance review and the resilience metrics register.
6. Annual review identifies systemic patterns across the year's lessons-learned reports.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27035-3 | Information security incident response | Incident learning |
| ISO 22301:2019 | §10 Improvement | Continuity improvement |
| NIST SP 800-61 Rev 2 | §3.5 Post-incident activity | Lessons learned activity |
| DORA | Article 13 Learning and evolving | Financial-sector learning |
| NIS 2 | Article 21(2)(f) Effectiveness assessment | Effectiveness review |
| ISO 9001:2015 | §10.2 Nonconformity and corrective action | Quality management |

---

## Limitations

This template is a public-domain baseline. Adopting organisations adapt the section structure to their existing PIR and CAPA workflows; the integration point with the corrective action register is the most important consistency element. The template is not a substitute for a formal regulatory after-action submission, nor a substitute for a forensic investigation report when one is required.

---

**End of Document**
