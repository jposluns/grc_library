# Tabletop Exercise Template

**Document Title:** Tabletop Exercise Template\
**Document Type:** Template\
**Version:** 1.1.0\
**Date:** 2026-10-20\
**Owner:** Resilience Owner\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md), [`resilience/register-resilience-metrics-and-testing-log.md`](register-resilience-metrics-and-testing-log.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material change to scenario library, regulatory expectation, or organizational structure\
**Repository Path:** [`resilience/template-tabletop-exercise.md`](template-tabletop-exercise.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines a reusable structure for designing, running, and learning from tabletop exercises. It supports the resilience testing programme by providing the scenario template, injects schedule, evaluation criteria, and after-action format that the Resilience Owner uses to commission each exercise. Adopting organizations select a scenario, populate the placeholders, and run the exercise.

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
| Annual PCI DSS incident response plan test (Requirement 12.10.2; only where PCI DSS applies) | Tabletop whose objectives and injects together cover every Requirement 12.10.1 plan element |
| After a real incident | Tabletop replaying the incident to validate updated procedures |
| New executive sponsor or coordinator role | Tabletop to onboard the role with their team |

---

## Scenario library (illustrative; expand per organization)

| Scenario class | Examples |
| --- | --- |
| Ransomware | Encryption of production data; double extortion with public leak threat; supply-chain ransomware via a managed service provider |
| Personal data breach | Misconfigured cloud storage; insider exfiltration; phishing-led credential theft and data access |
| AI security incident | Indirect prompt injection in a customer-facing assistant; data poisoning in a training pipeline; agent tool abuse |
| Operational outage | Cloud region failure; DNS failure; identity provider outage; database corruption |
| Supplier failure | Critical SaaS supplier insolvency; supplier data breach affecting the organization; supplier ransom incident |
| Physical event | Office fire; data centre power loss; flooding; pandemic; civil disturbance |
| Regulatory action | Enforcement notice; supervisory authority inspection; subpoena |
| Crisis convergence | Ransomware with personal data exposure with media leak with regulator notification simultaneously |

---

## Exercise design

### Objectives

Each exercise has between three and five specific objectives. Objectives are testable; "raise awareness" is not. The examples below are a menu: select or adapt three to five of them, or write equivalents for the scenario.

1. Validate that the Joint Command convenes within 60 minutes of P1 declaration.
2. Validate that the hand-off checklist from Security to Privacy completes without omission.
3. Validate that the regulatory notification decision is reached within the 24-hour early-warning window under NIS 2 (for a financial entity in scope of DORA: that a simulated initial notification is submitted to the Exercise Director, without contacting any real authority, as early as possible and within the Article 5 limits of Delegated Regulation (EU) 2025/301, that is within four hours of classifying the incident as major and no later than 24 hours from awareness or, where the incident is first classified as major more than 24 hours after awareness, within four hours of that classification).
4. Validate that the communications lead can produce an approved holding statement within 90 minutes.
5. Identify single points of failure in the supplier escalation path.
6. Identify recovery-time assumptions for the affected service that participants cannot support, and refer them to a recovery test.

### Participants

| Role | Required for | Notes |
| --- | --- | --- |
| Exercise Director | All exercises | Not a participating role; runs the exercise, delivers injects |
| Incident Coordinator | Multi-domain exercises | Per the cross-domain coordination procedure |
| Primary-domain Lead | Per the scenario domain | E.g. CISO for security; Data Protection Officer for privacy |
| Participating-domain Lead(s) | Per scenario | |
| Communications Lead | Most scenarios | |
| Legal Lead | Scenarios with regulatory or contractual exposure | |
| Supplier or service-provider representative | Scenarios that depend on a critical service provider or product supplier | Takes part where the contract and the supplier allow; otherwise the Exercise Director plays the supplier through injects |
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
| T+0 (alternative) | Event-reporting channel | Service desk or SOC | Staff member or external party reports a suspicious observation | Report acknowledged and triaged; reporter receives feedback |
| T+15 | Phone | CISO | Severity escalation prompt | CISO declares P1, convenes Joint Command |
| T+30 | Chat / collaboration platform | Data Protection Officer | Personal data implicated | Privacy stream activates per breach response procedure |
| T+60 | Email | Communications Lead | Journalist enquiry received | Communications produces holding statement |
| T+90 | Phone | Legal | Regulator initiating contact | Legal evaluates obligations; coordinates with Comms |
| T+120 | Chat / collaboration platform | Incident Coordinator | Supplier confirms data exposure | Supplier stream activates; hand-off checklist |
| T+150 | Phone | Executive Sponsor | Board member asking for briefing | Executive briefing materials produced |
| T+180 | Email | All | Exercise wrap-up | Participants pause for debrief |

Adopting organizations populate the table with scenario-specific inject content. Use the alternative T+0 inject when the exercise also tests the event-reporting channel, including reports from external parties and feedback to the reporter.

---

## Evaluation criteria

The Exercise Director scores against the declared objectives using a structured rubric.

| Criterion | Score: 1 (Below) | Score: 3 (Meets) | Score: 5 (Exceeds) |
| --- | --- | --- | --- |
| Time to convene Joint Command | More than 60 minutes from declaration | 30 to 60 minutes | Under 30 minutes |
| Hand-off checklist completion | Items missed; rework required | All items completed correctly | All items completed and gaps in source procedure noted for improvement |
| Decision quality | Decisions reversed during exercise; clear gaps | Decisions documented with rationale; minor adjustments | Decisions documented, traceable, and proactively communicated |
| Communication clarity | Conflicting messages observed; missed approvals | Single source of truth; approvals followed | Communication anticipates and pre-empts likely questions |
| Regulatory timing | Window missed | Window met with margin | Window met early; informed regulator pre-emptively |
| Tolerance for disruption or impact tolerance (only where one is set, e.g. under OSFI E-21 or PRA SS1/21) | Assessed outcome breaches the tolerance, or cannot be assessed | Assessed outcome stays within tolerance; risks to remaining within it recorded | Within tolerance with margin; each recorded risk has a corrective action |
| Documentation quality | Incomplete or absent | Complete to the standard | Complete, signed, and feeding the corrective action register |

---

## After-action report

Within 10 business days of the exercise:

| Field | Required content |
| --- | --- |
| Exercise ID | Unique identifier in the resilience metrics and testing log |
| Scenario | Brief description |
| Scenario assumptions and tolerance assessment | Assumptions made in scenario design; where a tolerance for disruption or impact tolerance is set, the assessed result and any identified risk to remaining within it |
| Date and duration | When and how long |
| Participants | Roles and named individuals in internal use |
| Objectives | The declared objectives |
| Inject schedule | Final schedule as run |
| Findings against each objective | Met, Partially Met, Not Met, with evidence |
| Requirement 12.10.1 element coverage | Only where the exercise is the annual PCI DSS plan test: each Requirement 12.10.1 element and the objective or inject that tested it |
| Plan deviations | Each point where participants departed from the documented plan or procedure, with the reason and any follow-up |
| Strengths | What worked well |
| Gaps identified | Procedural, technical, communication, supplier, regulatory |
| Corrective actions | Action, owner role, deadline, including actions agreed with participating suppliers; tracked in the corrective action register |
| Risk register updates | New or updated risk entries |
| Procedure changes | Specific procedure amendments to propose |
| Score summary | Per criterion plus an overall posture statement |
| External evaluator comment | If applicable |
| Exercise conduct feedback | Participant feedback, collected at the debrief, on how the exercise itself was run |
| Approval | Resilience Owner and Executive Sponsor sign-off |

---

## Operating expectations

1. The annual exercise plan is reviewed by the Resilience Owner and approved by the Executive Sponsor.
2. Each exercise has a planned objective set defined before injects are written.
3. Exercises are not gating events for promotions or punitive performance reviews; safe-to-fail framing applies.
4. After-action reports are classified per the source-data sensitivity; aggregate findings inform the resilience metrics register and the governance review.
5. Corrective actions from exercises are tracked to closure with the same rigour as from real incidents.
6. Participants are briefed at the start that the scenario is an exercise, and every inject and simulated external contact is marked as exercise traffic. The Exercise Director holds end-of-exercise and emergency-stop protocols and stops the exercise if any action could spill over into live operations or reach people outside the exercise.

---

## Framework alignment

Regulatory rows apply only where the adopting organization is in scope of the regime; rows marked "only for" or "only where" state that scope.

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | §8.5 Exercising and testing | Continuity programme exercising |
| ISO/IEC 27001:2022 | A.5.30 ICT readiness | Resilience testing |
| ISO/IEC 27035-2:2023 | §11.2.3 Conducting an exercise | Awareness that the scenario is an exercise; briefing on exercise goals; conduct feedback |
| ISO/IEC 27031:2025 | §11.2.6 Managing an exercise | End-of-exercise and emergency-stop protocols |
| NIST SP 800-84 | §4.2 to §4.5 (design, develop, conduct, evaluate the tabletop exercise) | US federal exercise guidance |
| NIST SP 800-61 Rev. 3 | Table 2, ID.IM-02 note N1 (exercises prepare staff and involved third parties, such as critical service providers and product suppliers) | Supplier and service-provider participation |
| NIST CSF 2.0 | ID.IM-02 (improvements from security tests and exercises, including those done with suppliers and relevant third parties) | Exercise-derived improvement |
| NIST SP 800-184 | §3.1 Validating Recovery Capabilities | Testing recovery-time assumptions |
| DORA | Article 24(1), 24(5), 25(1) | Digital operational resilience testing |
| DORA RTS (EU) 2025/301 | Article 5(1)(a) initial-notification time limit (Article 5(2) covers later classification as major) | Notification timing in exercise objectives; only for financial entities in scope of DORA |
| NIS 2 | Article 21(2)(f) | Effectiveness assessment |
| NIS 2 Implementing Regulation (EU) 2024/2690 | Annex points 3.1.3 and 3.5.5 | Testing incident-handling roles, responsibilities and procedures at planned intervals; only for the entity types listed in its Article 1 |
| OSFI Guideline E-21 | Principle 8 and §3.3 Scenario testing | Scenario testing within tolerances for disruption; only for OSFI-regulated financial institutions |
| PRA SS1/21 | Chapter 6, paragraph 6.3 | Documenting scenario assumptions and risks to remaining within impact tolerances; only for the firms listed in SS1/21 paragraph 1.3 (UK banks, building societies, PRA-designated investment firms and CRR consolidation entities; UK Solvency II firms, the Society of Lloyd's and its managing agents) |
| PCI DSS v4.0.1 | Requirement 12.10.2 | Annual incident response plan test covering every Requirement 12.10.1 element; only where PCI DSS applies |
| TIBER-EU | ECB framework | Threat-led testing |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. Adopting organizations populate scenarios, injects, and participants from their environment. Live-fire exercises require additional safety, communication, and regulator-coordination planning not covered here. The template is not a substitute for the resilience testing procedure or regulator-specific testing methodologies. A tabletop exercise alone does not validate recovery capability: discussion shows whether plans are reasonable and roles are understood, while recovery is validated by technical restoration, failover, or recovery tests under [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md). Framework alignment rows for a specific regime apply only where the adopting organization is in scope; running this template does not by itself demonstrate compliance with any of them.

---

**End of Document**
