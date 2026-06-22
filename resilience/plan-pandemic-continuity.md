# Pandemic Continuity Plan

**Document Title:** Pandemic Continuity Plan\
**Document Type:** Plan\
**Version:** 1.0.4\
**Date:** 2026-06-22\
**Owner:** Resilience Owner\
**Approving Authority:** Executive Management\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](policy-business-continuity-and-disaster-recovery.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md), [`resilience/plan-crisis-communication.md`](plan-crisis-communication.md), [`resilience/procedure-cross-domain-incident-coordination.md`](procedure-cross-domain-incident-coordination.md), [`security/standard-remote-working-security.md`](../security/standard-remote-working-security.md), [`security/policy-byod.md`](../security/policy-byod.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material public-health, supplier, workforce, or facility change\
**Repository Path:** [`resilience/plan-pandemic-continuity.md`](plan-pandemic-continuity.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This plan defines the organisation's continuity posture for a pandemic or other prolonged workforce-impacting disruption (severe respiratory disease, novel infectious outbreak, prolonged civil unrest affecting facility access, prolonged extreme weather affecting commuting). It covers staged activation, workforce health, remote-work scaling, supplier impact, facility and operational adjustments, essential-service prioritisation, communications, deactivation, and learning. It is a sister plan to the IT disaster recovery plan and the business continuity and crisis management plan.

---

## Scope

This plan applies to any disruption that materially affects the available workforce or its physical access to facilities for a sustained period (more than two weeks). It is activated when public-health authorities or government bodies issue formal advisories or directives, or when internal monitoring confirms a workforce-availability degradation that exceeds defined thresholds.

It does not cover the technical recovery of failed systems (the IT DR plan applies) nor the crisis governance overlay (the BCM plan applies). It integrates with both.

---

## Activation stages

The plan operates in five stages. Movement between stages is decided by the Resilience Owner with Executive Sponsor approval based on the activation criteria.

| Stage | Activation criteria | Posture |
| --- | --- | --- |
| Stage 0: Monitor | Public-health surveillance signal or external advisory at heightened level | No operational change; intelligence collection |
| Stage 1: Prepare | Sustained surveillance signal; specific risk to the organisation's workforce or facilities | Communication primers; remote-work readiness verified; PPE and supplies inventory checked |
| Stage 2: Activate | Formal public-health authority advisory or directive; first workforce impact observed | Remote-work shift for non-essential on-site roles; visitor restrictions; travel constraints |
| Stage 3: Sustained operations | Disruption confirmed; workforce-availability projected impact above thresholds | Essential-services-only operational mode; rotational on-site staffing; supplier impact assessment |
| Stage 4: Recovery | Sustained improvement; advisories relaxed | Phased return to baseline; workforce well-being focus; lessons-learned commissioning |

---

## Workforce health

| Item | Required content |
| --- | --- |
| Health-and-safety responsibilities | Employer obligations under local occupational health and safety law |
| Vaccination and prophylaxis | Recommendation, support, or requirement per applicable law and organisational policy |
| Sick-leave policy adjustments | Extended sick leave; remote-work-while-recovering options; quarantine pay |
| Mental health support | Employee assistance programme; manager training on prolonged-disruption stress signs |
| Personal protective equipment | PPE provided where required for on-site roles |
| On-site protocols | Density limits, ventilation, sanitation, hygiene, testing if applicable |
| Reasonable accommodations | For at-risk workers, carers, and those with disabilities |
| Privacy | Health information collected only with lawful basis; minimized; restricted access |

---

## Remote-work scaling

| Item | Required content |
| --- | --- |
| Capacity check | Existing remote-work entitlement and platform capacity; gap analysis |
| Device provisioning | Plan to provision managed devices to roles that lack them; BYOD policy as a fallback |
| Network capacity | VPN and secure-access capacity scaling per the operations team |
| Identity provider scaling | Authentication platform capacity confirmation |
| Collaboration platform scaling | Video and messaging platform capacity confirmation |
| Help-desk scaling | Surge plan for the IT service desk |
| Training | Manager training for remote-team management; employee training for remote-work basics |
| Security posture | Remote-working security standard applies; no relaxation under pandemic conditions |

---

## Essential-service prioritisation

Each business function is classified by criticality. During Stage 3 the organisation operates essential services only.

| Tier | Definition | Posture under Stage 3 |
| --- | --- | --- |
| Essential | Service the organisation must maintain regardless of workforce availability (e.g. customer-facing payment processing, regulatory reporting, safety functions) | Continue with rotational staffing and supplier coverage |
| Important | Service the organisation should maintain if workforce permits | Continue at reduced capacity; defer non-urgent activity |
| Deferrable | Service the organisation can suspend | Suspend with communicated restart criteria |

Each in-scope function maps to one of these tiers in the business impact analysis. The BIA is the source of truth; this plan operationalises it.

---

## Supplier and supply-chain impact

| Item | Required content |
| --- | --- |
| Supplier-status monitoring | Active monitoring of critical suppliers' continuity posture |
| Contractual force-majeure handling | Legal review of clauses likely to be invoked |
| Alternate-supplier activation | Plan to activate pre-identified alternates per the supplier risk register |
| Concentration-risk review | Per the concentration risk register; pandemic concentration risks include geographically clustered suppliers |
| Sub-processor disruption | Privacy implications for personal data processing |
| Logistics and physical supply | For organisations with physical supply chains, transport and customs continuity |
| Critical-component stocking | Where authorised, advance procurement of critical components |

---

## Facility and operational adjustments

| Item | Required content |
| --- | --- |
| Facility-access policy | Visitor restrictions, contractor restrictions, contractor-credential verification |
| Density limits | Per local public-health advisory and risk assessment |
| Ventilation and sanitation | Per local public-health advisory |
| Site closure decision rules | Criteria for closing a site temporarily or fully |
| Mail and physical-document handling | Triage and decontamination protocols if applicable |
| Travel restrictions | Domestic and international; per public-health and government advisory |
| Event policy | In-person event suspension criteria |
| Customer-visit policy | Site visit suspension and virtual alternative |

---

## Communications

| Audience | Channel | Cadence | Content |
| --- | --- | --- | --- |
| Employees | Email; collaboration platform; town halls | Weekly during active stages | Stage, expectations, support, well-being |
| Customers | Status page; email; in-product | At stage transitions and at material changes | Service availability, alternative channels, expected duration |
| Regulators | Per regulator | Per regulatory expectation | Continuity status |
| Suppliers | Account manager channels | As needed | Coordination on continuity |
| Public and media | Per the crisis communication plan | As needed | Sanitised, board-approved |

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| Resilience Owner | Plan owner; activates and moves between stages with Executive Sponsor approval |
| Executive Sponsor | Approves stage transitions, essential-service tier overrides, public statements |
| HR Lead | Workforce health, sick-leave, accommodations, mental-health support |
| IT Operations | Remote-work scaling, capacity, help-desk surge |
| Information Security | Maintains security posture during scaling; coordinates remote-work security |
| Data Protection Officer | Lawful basis for any health-data collection; cross-border transfer review if applicable |
| Communications Lead | All audiences; board approval for public statements |
| Legal Counsel | Employment law, contract law, regulatory engagement |
| Facilities | Site decisions, density, sanitation |
| Supplier Risk Maintainer | Supplier impact and alternates |

---

## Deactivation and recovery

Deactivation criteria are public-health-authority guidance plus internal indicators (workforce availability restored above threshold; supplier continuity normal). Recovery is staged:

1. Phased return to baseline operations.
2. Restoration of deferred services.
3. Workforce well-being check-ins and accommodation review.
4. Supplier baseline reassessment.
5. Lessons-learned cycle within 20 business days of full deactivation.

---

## Operating expectations

1. The plan is exercised at minimum annually as a tabletop scenario.
2. Stage 1 readiness is verified quarterly.
3. The BIA is refreshed annually with explicit pandemic-scenario consideration.
4. The plan is integrated with the IT DR plan and the BCM plan; ambiguous activations default to convening the Joint Command per the cross-domain coordination procedure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | All clauses | Continuity programme |
| ISO 22332:2021 | Developing business continuity plans and procedures | Plan structure |
| WHO Pandemic Influenza Risk Management | Global guidance | Public-health alignment |
| US Department of Labor OSHA pandemic guidance | OSHA | Workforce health |
| UK HSE pandemic guidance | HSE | Workforce health |
| EU NIS 2 | Article 21(2)(c) Business continuity | EU essential entities |
| DORA | Article 12 ICT business continuity policy | Financial sector |

---

## Limitations

This plan is a CC BY-SA 4.0 baseline. Adopting organisations populate the activation thresholds, the essential-service tier mapping, the supplier alternate list, the contact roster, the facility-access protocols, and the communications templates from their environment and local public-health guidance. The plan is not medical advice and is not a substitute for occupational health and safety counsel.

---

**End of Document**
