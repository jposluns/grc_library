# Physical Site Continuity Plan

**Document Title:** Physical Site Continuity Plan\
**Document Type:** Plan\
**Version:** 1.0.3\
**Date:** 2026-07-02\
**Owner:** Resilience Owner\
**Approving Authority:** Executive Management\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](policy-business-continuity-and-disaster-recovery.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md), [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md), [`resilience/guideline-emergency-response-and-protective-actions.md`](guideline-emergency-response-and-protective-actions.md), [`resilience/procedure-crisis-management-eoc-activation.md`](procedure-crisis-management-eoc-activation.md), [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material change to the site, its workforce, its infrastructure, or its risk profile\
**Repository Path:** [`resilience/plan-physical-site-continuity.md`](plan-physical-site-continuity.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This plan defines how a specific physical site (office, data centre, warehouse, operational facility) maintains essential operations and supports a controlled return to baseline when the site is disrupted. It covers protective actions during the event, partial-operations posture during recovery, alternate-site activation when relocation is required, and full restoration. It is a sister plan to the IT disaster recovery plan and the business continuity and crisis management plan; it does not replace either.

Each in-scope site has its own instantiation of this plan with site-specific values populated.

---

## Scope

This plan applies to disruptions affecting a specific site's ability to operate normally. In-scope events include but are not limited to: fire, power loss, water ingress, structural damage, HVAC failure, telecommunications outage at the site, security event affecting access, civil-disturbance access denial, extreme weather, evacuation order, environmental contamination, and prolonged site-utility failure.

It does not cover pandemic-style workforce-unavailability events (see [`resilience/plan-pandemic-continuity.md`](plan-pandemic-continuity.md)) or pure IT failure where the site is operational but a system has failed (see [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md)).

---

## Site profile (per instantiation)

| Field | Description |
| --- | --- |
| Site name | Canonical site name; not the postal address in the public CC BY-SA 4.0 version |
| Function | Office, data centre, warehouse, operational facility, hybrid |
| Criticality tier | Tier from the BIA |
| Headcount range | Approximate occupancy; not actual address-level employee count |
| Critical functions hosted | Functions whose continuity depends on this site |
| Dependencies on this site | Other sites, suppliers, customers that rely on this site |
| Alternate site(s) | Identified primary and secondary alternates for relocation |
| Recovery objectives | Site-specific RTO and RPO if applicable |

---

## Disruption response posture

The plan operates in four postures based on disruption severity.

| Posture | Trigger | Operational state |
| --- | --- | --- |
| Posture A: Protective actions in place | Active event requiring immediate occupant protection (fire alarm, security threat, extreme weather warning) | Evacuation or shelter-in-place per the emergency response and protective actions guideline; no operational activity until life-safety is confirmed |
| Posture B: Partial operations on site | Event resolved or contained; partial site access restored | Designated essential functions resume on site; remainder remote where possible |
| Posture C: Site closed; operations relocated | Site not safely usable; alternate-site activation required | Personnel and critical equipment relocated; site closed until restoration |
| Posture D: Restoration in progress | Site repairable; planned phased reopening | Phased return per restoration plan with safety re-confirmations |

The Resilience Owner declares the posture in consultation with the Executive Sponsor, Facilities, and Security. Posture A defers to life-safety authority (typically the building fire warden or equivalent).

---

## Activation criteria

| Trigger | Initial posture |
| --- | --- |
| Confirmed fire, smoke, or detector activation | A |
| Confirmed gas leak or hazardous-material release | A |
| Confirmed active security threat at the site | A |
| Extreme-weather warning at orange/red equivalent | A or B per local authority advisory |
| Sustained loss of power, water, sanitation, or HVAC beyond defined tolerance | B or C |
| Structural damage discovered after inspection | C |
| Telecommunications outage affecting all site connectivity | B if operations can continue offline; C if not |
| Public-health advisory for the site (e.g. contamination) | C |
| Civil disturbance preventing site access | B or C per the impact assessment |

---

## Protective actions

This section defers to [`resilience/guideline-emergency-response-and-protective-actions.md`](guideline-emergency-response-and-protective-actions.md) for the operational steps. Each site's instantiation of this plan adds:

| Item | Site-specific content |
| --- | --- |
| Evacuation routes and assembly points | Site map references (held internally) |
| Shelter-in-place locations | Specific designated areas |
| Roll-call procedure | Method for confirming all occupants are accounted for |
| Fire warden roster | Roles, not named individuals, in the public version |
| First aid responder roster | Roles |
| Visitor and contractor accountability | How non-employees are tracked during evacuation |
| Accessibility considerations | Routes and assistance plans for occupants with disabilities |
| Notification to emergency services | Designated role; specific information to provide |
| Notification to the Resilience Owner | Designated role; channel; expected response time |
| Notification to the next-of-kin coordination function | Designated role for casualty scenarios |

---

## Partial operations on site (Posture B)

When the site is partially usable:

1. Safety re-confirmation completed by Facilities and Security before any function resumes.
2. Essential functions identified per the BIA resume on site; others remain remote.
3. Reduced occupancy posture applied where the impacted area constrains capacity.
4. Communication to occupants on the partial-operations posture, expected duration, and access rules.
5. Continuous monitoring of the underlying cause for relapse risk.

---

## Alternate-site activation (Posture C)

When the site is unusable:

| Step | Action | Owner |
| --- | --- | --- |
| 1 | Declare Posture C; confirm with Executive Sponsor | Resilience Owner |
| 2 | Activate primary alternate site per the alternate-site agreement | Facilities |
| 3 | Notify the workforce of the relocation including reporting location, timing, and what to bring | Communications Lead |
| 4 | Relocate critical physical equipment per the recovery runbook | Operations |
| 5 | Activate identity and access at the alternate site | IT Operations and Security |
| 6 | Activate communications channels and call-routing at the alternate site | IT Operations |
| 7 | Notify customers and partners of the alternate site if their contact channels are affected | Communications Lead |
| 8 | Notify suppliers whose service depends on physical access | Supplier Risk Maintainer |
| 9 | Notify the insurer per the policy notification window | Finance / Risk |
| 10 | Notify the regulator if the site disruption is reportable under any applicable regime | Legal and Compliance |

Each alternate site has its own contractual or operational arrangement and a pre-tested activation procedure. The primary alternate is reachable within a defined transit window from the primary site; the secondary alternate is in a different risk geography.

---

## Restoration and return (Posture D)

When the site is again usable:

1. Independent safety inspection by qualified Facilities personnel and external inspector if required.
2. Building services (power, water, HVAC, fire suppression, communications) re-validated.
3. Cleaning and decontamination completed if applicable.
4. Phased return: essential functions first; others by tier.
5. Workforce communication on return timing, transit support, and any temporary protocol changes.
6. Closure check: confirm essential services were maintained throughout (continuity test pass) and document any service gaps.
7. After-action lessons-learned cycle (see [`resilience/template-lessons-learned.md`](template-lessons-learned.md)).
8. Insurance claim and recovery accounting.
9. Update the site profile and the plan if the event exposed gaps.

---

## Workforce well-being

| Item | Required content |
| --- | --- |
| Critical-incident support | Counselling and employee assistance programme activation for serious events |
| Casualty support | Coordination with HR and Legal; family-liaison role if applicable |
| Return-to-work accommodations | For occupants affected by the event |
| Transit and lodging support | Where the alternate site requires travel or temporary accommodation |
| Continuity of pay | Confirm no disruption to payroll during site closure |

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| Resilience Owner | Plan owner; declares postures |
| Executive Sponsor | Approves Posture C activation, alternate-site selection, public communications |
| Facilities | Site safety, alternate-site activation, restoration |
| Security | Site security, threat assessment, access control |
| HR | Workforce communication, well-being, casualty support |
| IT Operations | Communications and identity continuity |
| Communications Lead | Workforce and external communication |
| Legal | Insurance, regulator engagement, contractual obligations |
| Finance | Insurance claim, recovery accounting |

---

## Operating expectations

1. The plan is exercised at minimum annually as a tabletop scenario per site (Tier 1 sites; Tier 2 sites biennially).
2. Evacuation and shelter-in-place drills follow local statutory frequency.
3. Alternate-site activation is tested at minimum every two years for Tier 1 sites.
4. The site profile is reviewed annually and updated within 10 business days of material change.
5. The plan is held both digitally and in printed form at the site and at the alternate site.
6. The plan is consistent with the BCM plan and the IT DR plan; ambiguous events default to convening the Joint Command per the cross-domain coordination procedure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | §8.4 Business continuity procedures | Site continuity |
| ISO 22322:2015 | Public warning | Notification and warning |
| ISO 22320:2018 | Emergency management | Coordination |
| Local fire and building codes | Per jurisdiction | Life safety |
| Local occupational health and safety law | Per jurisdiction | Employer obligations |
| Insurance policy terms | Per policy | Notification windows |
| DORA | Article 12 ICT business continuity policy | Where applicable |
| NIS 2 | Article 21(2)(c) Business continuity | Where applicable |

---

## Limitations

This plan is a CC BY-SA 4.0 baseline. Adopting organizations populate site-specific values (alternate-site addresses, rosters, evacuation routes, equipment inventories) in private instantiations of this plan. The plan is not safety advice and is not a substitute for a qualified safety professional, a building-control inspection, or insurance-specific guidance. Life-safety decisions are governed by the qualified site emergency response role per local statute.

---

**End of Document**
