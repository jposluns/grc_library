# Tabletop Exercise Template

**Document Title:** Tabletop Exercise Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Resilience Owner\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md), [`resilience/register-resilience-metrics-and-testing-log.md`](register-resilience-metrics-and-testing-log.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material change to scenario library, regulatory expectation, or organisational structure\
**Repository Path:** [`resilience/template-tabletop-exercise.md`](template-tabletop-exercise.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines a reusable structure for designing, running, and learning from tabletop exercises. It supports the resilience testing programme by providing the scenario template, injects schedule, evaluation criteria, and after-action format that the Resilience Owner uses to commission each exercise. Adopting organisations select a scenario, populate the placeholders, and run the exercise.

---

## Scope

This template covers desk-based tabletop exercises (no system action; participants discuss responses) and simulation-style exercises (limited system or process action under controlled conditions). It does not cover full-scale live-fire exercises, which require additional safety, customer-impact, and regulatory considerations.

---

## When to use a tabletop exercise

| Trigger | Suggested exercise type |
| --- | --- |
| New procedure or material procedure revision | Tabletop covering the new procedure end to end |
| New product, service, or material technology change | Tabletop covering the change scenario |
| Annual cross-domain coordination test | Multi-domain tabletop (security + privacy + supplier + AI + resilience) |
| Regulator-mandated exercise (DORA, NIS 2, sector regulator) | Tabletop or simulation per the regulator's expectation |
| After a real incident | Tabletop replaying the incident to validate updated procedures |
| New executive sponsor or coordinator role | Tabletop to onboard the role with their team |

---

## Scenario library (illustrative; expand per organisation)

| Scenario class | Examples |
| --- | --- |
| Ransomware | Encryption of production data; double extortion with public leak threat; supply-chain ransomware via a managed service provider |
| Personal data breach | Misconfigured cloud storage; insider exfiltration; phishing-led credential theft and data access |
| AI security incident | Indirect prompt injection in a customer-facing assistant; data poisoning in a training pipeline; agent tool abuse |
| Operational outage | Cloud region failure; DNS failure; identity provider outage; database corruption |
| Supplier failure | Critical SaaS supplier insolvency; supplier data breach affecting the organisation; supplier ransom incident |
| Physical event | Office fire; data centre power loss; flooding; pandemic; civil disturbance |
| Regulatory action | Enforcement notice; supervisory authority inspection; subpoena |
| Crisis convergence | Ransomware with personal data exposure with media leak with regulator notification simultaneously |

---

## Exercise design

### Objectives

Each exercise has between three and five specific objectives. Objectives are testable; "raise awareness" is not. Examples:

1. Validate that the Joint Command convenes within 60 minutes of P1 declaration.
2. Validate that the hand-off checklist from Security to Privacy completes without omission.
3. Validate that the regulatory notification decision is reached within the 24-hour early-warning window under NIS 2.
4. Validate that the communications lead can produce an approved holding statement within 90 minutes.
5. Identify single points of failure in the supplier escalation path.

### Participants

| Role | Required for | Notes |
| --- | --- | --- |
| Exercise Director | All exercises | Not a participating role; runs the exercise, delivers injects |
| Incident Coordinator | Multi-domain exercises | Per the cross-domain coordination procedure |
| Primary-domain Lead | Per the scenario domain | E.g. CISO for security; Privacy Officer for privacy |
| Participating-domain Lead(s) | Per scenario | |
| Communications Lead | Most scenarios | |
| Legal Lead | Scenarios with regulatory or contractual exposure | |
| Executive Sponsor | P1-level scenarios | |
| Observer(s) | Recommended for all exercises | Note-takers; do not contribute to decisions |
| External Evaluator | Annual cross-domain exercises | Independent observer who scores against objectives |

### Format options

| Format | Duration | Best for |
| --- | --- | --- |
| Desk-based discussion | 1 to 2 hours | Single-domain or narrow-scope scenarios |
| Multi-injects walkthrough | 2 to 4 hours | Multi-domain coordination; severity escalation |
| Simulation with controlled system action | Half day | Testing tooling alongside procedure |
| Two-day exercise | 1 to 2 days | Crisis-level convergence with executive participation |

---

## Inject schedule

An inject is a piece of information delivered during the exercise to advance the scenario. Each inject has a time stamp (relative to exercise start), a delivery channel, a recipient role, and an expected response.

| Time | Channel | Recipient | Inject text | Expected response or behaviour |
| --- | --- | --- | --- | --- |
| T+0 | Email | SOC | Initial alert template | SOC triages and classifies |
| T+15 | Phone | CISO | Severity escalation prompt | CISO declares P1, convenes Joint Command |
| T+30 | Slack | Privacy Officer | Personal data implicated | Privacy stream activates per breach response procedure |
| T+60 | Email | Communications Lead | Journalist enquiry received | Communications produces holding statement |
| T+90 | Phone | Legal | Regulator initiating contact | Legal evaluates obligations; coordinates with Comms |
| T+120 | Slack | Incident Coordinator | Supplier confirms data exposure | Supplier stream activates; hand-off checklist |
| T+150 | Phone | Executive Sponsor | Board member asking for briefing | Executive briefing materials produced |
| T+180 | Email | All | Exercise wrap-up | Participants pause for debrief |

Adopting organisations populate the table with scenario-specific inject content.

---

## Evaluation criteria

The Exercise Director scores against the declared objectives using a structured rubric.

| Criterion | Score: 1 (Below) | Score: 3 (Meets) | Score: 5 (Exceeds) |
| --- | --- | --- | --- |
| Time to convene Joint Command | More than 90 minutes from declaration | 30 to 60 minutes | Under 30 minutes |
| Hand-off checklist completion | Items missed; rework required | All items completed correctly | All items completed and gaps in source procedure noted for improvement |
| Decision quality | Decisions reversed during exercise; clear gaps | Decisions documented with rationale; minor adjustments | Decisions documented, traceable, and proactively communicated |
| Communication clarity | Conflicting messages observed; missed approvals | Single source of truth; approvals followed | Communication anticipates and pre-empts likely questions |
| Regulatory timing | Window missed | Window met with margin | Window met early; informed regulator pre-emptively |
| Documentation quality | Incomplete or absent | Complete to the standard | Complete, signed, and feeding the corrective action register |

---

## After-action report

Within 10 business days of the exercise:

| Field | Required content |
| --- | --- |
| Exercise ID | Unique identifier in the resilience metrics and testing log |
| Scenario | Brief description |
| Date and duration | When and how long |
| Participants | Roles and named individuals in internal use |
| Objectives | The declared objectives |
| Inject schedule | Final schedule as run |
| Findings against each objective | Met, Partially Met, Not Met, with evidence |
| Strengths | What worked well |
| Gaps identified | Procedural, technical, communication, supplier, regulatory |
| Corrective actions | Action, owner role, deadline; tracked in the corrective action register |
| Risk register updates | New or updated risk entries |
| Procedure changes | Specific procedure amendments to propose |
| Score summary | Per criterion plus an overall posture statement |
| External evaluator comment | If applicable |
| Approval | Resilience Owner and Executive Sponsor sign-off |

---

## Operating expectations

1. The annual exercise plan is reviewed by the Resilience Owner and approved by the Executive Sponsor.
2. Each exercise has a planned objective set defined before injects are written.
3. Exercises are not gating events for promotions or punitive performance reviews; safe-to-fail framing applies.
4. After-action reports are classified per the source-data sensitivity; aggregate findings inform the resilience metrics register and the governance review.
5. Corrective actions from exercises are tracked to closure with the same rigour as from real incidents.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | §8.5 Exercising and testing | Continuity programme exercising |
| ISO/IEC 27001:2022 | A.5.30 ICT readiness | Resilience testing |
| NIST SP 800-84 | Test, Training, and Exercise Programs | US federal exercise guidance |
| DORA | Article 24 to 27 | Digital operational resilience testing |
| NIS 2 | Article 21(2)(f) | Effectiveness assessment |
| TIBER-EU | ECB framework | Threat-led testing |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. Adopting organisations populate scenarios, injects, and participants from their environment. Live-fire exercises require additional safety, communication, and regulator-coordination planning not covered here. The template is not a substitute for the resilience testing procedure or regulator-specific testing methodologies.

---

**End of Document**
