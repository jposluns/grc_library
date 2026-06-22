# OT Incident Response Procedure

**Document Title:** OT Incident Response Procedure\
**Document Type:** Procedure\
**Version:** 1.0.1\
**Date:** 2026-06-22\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../../resilience/procedure-security-incident-reporting-and-escalation.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/template-lessons-learned.md`](../../resilience/template-lessons-learned.md), [`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md), [`compliance/annex-nis-2-implementation.md`](../../compliance/annex-nis-2-implementation.md), [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](../../compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and following any material OT incident or change to IEC 62443 / NIST SP 800-82\
**Repository Path:** [`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This procedure defines the operational sequence for responding to security incidents in Operational Technology (OT) environments. It extends the general security incident response procedure ([`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)) with OT-specific considerations: safety-first decision-making, vendor coordination, longer recovery windows, and integration with safety management.

The procedure applies to any incident affecting an OT zone, conduit, or supporting infrastructure under the OT/ICS Security Standard ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)). Where a cyber incident has potential safety consequences, this procedure governs the cyber response while the organisation's safety-management procedure governs the safety response; the two run in parallel with the safety procedure taking precedence on any conflict.

---

## 2. Scope

### 2.1 In scope

- Confirmed or suspected cyber compromise of any OT zone, conduit, engineering workstation, HMI, historian, controller, SIS, or BMS asset.
- Unexpected behaviour in OT systems that may indicate compromise (anomalous process values, unexpected commands, configuration changes outside the change record, alarm flooding).
- Detected adversary presence in IT zones that have a conduit to any OT zone.
- OT vendor or integrator incidents (compromise of vendor systems, supply-chain incidents) where the vendor has access to or supplies systems for the organisation's OT environment.
- Loss-of-view or loss-of-control events with potential cyber causation.

### 2.2 Out of scope

- Pure IT incidents with no OT conduit (governed by the base security incident response procedure).
- Process-safety incidents with no cyber causation suspected (governed by the safety-management procedure, with this procedure invoked only if cyber causation becomes a hypothesis during investigation).
- Physical-security incidents at OT facilities without cyber overlap (governed by physical-security and facility-management procedures).

### 2.3 Precedence

Where this procedure conflicts with the safety-management procedure, the safety procedure takes precedence. Where it conflicts with sector-regulator-mandated reporting timelines (NERC CIP, NIS 2 essential-entity reporting, sector-specific), the regulator timeline takes precedence.

---

## 3. Guiding principles

The following principles apply throughout the procedure and override individual step instructions where a conflict arises.

### 3.1 Safety first

If at any time during response the responder believes that continuing a containment, eradication, or recovery action could create a safety hazard, the action is paused immediately and escalated to the Process Safety Engineer. Production-safety risk is not exchanged for cyber-containment speed.

### 3.2 Availability constraints

OT systems often cannot be taken offline for forensic preservation in the way IT systems can. Forensic actions must be planned to minimize production disruption. Where preservation conflicts with availability, the OT Security Lead documents the decision and the trade-off accepted.

### 3.3 Vendor coordination

Many OT systems are vendor-controlled. Vendor involvement is often mandatory for diagnostic access and recovery. Vendor coordination must begin early, ideally at first triage, not at the recovery stage.

### 3.4 Evidence preservation

Volatile OT evidence (memory state of controllers, transient communications, alarm queues) is lost rapidly. Where lawful and operationally feasible, preserve volatile evidence before issuing containment commands that may alter system state.

### 3.5 No silent remediation

Operators, engineers, or vendors who observe suspected compromise must report rather than attempt silent fix. The procedure depends on early reporting.

---

## 4. Roles

| Role | OT incident responsibility |
| --- | --- |
| **Incident Commander (CISO or delegate)** | Overall response leadership; authorises declaration, escalation, containment actions with production impact, and recovery sign-off. |
| **OT Security Lead** | OT-specific triage and technical response; primary interface to the IT SOC and to Control System Engineers. Reports to Incident Commander. |
| **Plant Manager / Operations Director** | Accountable for production state during the incident; authorises any production-impacting containment action; coordinates manual fallback if invoked. |
| **Process Safety Engineer** | Accountable for safety state; authorises any action that could affect safety-instrumented functions; consulted on every containment action affecting SIS or shared SIS/BPCS infrastructure. |
| **Control System Engineer** | Executes technical actions on OT systems under direction from OT Security Lead; provides system-state information; coordinates with vendor. |
| **IT Security Operations Centre (SOC)** | Provides initial detection and triage; correlates OT alerts with IT-side telemetry; supports forensics on IT-side conduit endpoints. |
| **Vendor Liaison** | OT vendor or integrator point-of-contact; coordinates vendor diagnostic and recovery activity per the standard's vendor remote-access controls. |
| **Communications Owner** | Manages internal and external communications including regulatory notifications. |
| **Legal Counsel** | Advises on regulatory notification obligations, evidence handling, vendor contractual cooperation. |
| **External IR Partner** | Engaged at the Incident Commander's discretion for P1 incidents requiring specialist OT-IR capability. |

---

## 5. Severity classification

OT incident severity uses the base severity scale from [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md) with OT-specific triggers added.

| Severity | OT-specific trigger criteria |
| --- | --- |
| **P1: Critical** | Confirmed adversary presence in a production OT zone with SL-T ≥ SL 3. Compromise of a SIS or potential to affect safety. Loss-of-view or loss-of-control on a production process. Cyber-related production outage of a critical site. |
| **P2: High** | Suspected adversary presence in a production OT zone. Anomalous control commands not attributable to scheduled changes. Cyber compromise of an OT vendor with active access. Confirmed compromise in an OT DMZ. Loss-of-view or loss-of-control on a non-critical process. |
| **P3: Medium** | Unauthorised configuration change detected post-event. Compromise of an engineering workstation with no evidence of further movement. Failed authentication storm against an OT identity surface. |
| **P4: Low** | Single suspicious event without corroboration. Policy violation (for example, unsanctioned removable media use) with no compromise evidence. |

Classification is initial; severity is re-evaluated at each phase of the procedure.

---

## 6. Phase 1: Detection and triage

### 6.1 Detection sources

OT incidents may be detected through:

- SIEM alerts on OT-aware telemetry (per the OT/ICS Security Standard section 10).
- Plant operator reports of unexpected behaviour (alarm flooding, unexplained setpoint changes, HMI display anomalies).
- Control System Engineer reports of configuration drift or unexplained changes.
- Vendor notification of a relevant vulnerability or vendor-side compromise.
- External threat intelligence indicating a campaign relevant to the OT environment.
- Regulator or sector-coordinator (for example, E-ISAC for North American electricity) notification.

### 6.2 Initial triage

6.2.1 Within 15 minutes of detection of a candidate OT incident, the IT SOC or detecting party:

- Records the detection in the incident-tracking system.
- Assigns an initial severity using the criteria in section 5.
- Notifies the OT Security Lead.

6.2.2 The OT Security Lead within 30 minutes of notification:

- Confirms or revises severity.
- Notifies the Plant Manager of the affected facility.
- For P1 and P2 incidents, notifies the Incident Commander.
- For incidents affecting safety-instrumented systems or with potential safety consequence, notifies the Process Safety Engineer immediately regardless of severity.

### 6.3 Initial situational awareness

Within the first hour of confirmed incident classification, the OT Security Lead determines:

- Which OT zones and conduits are affected.
- Whether SIS or other safety-critical functions are involved.
- Whether the production process is currently controllable (loss-of-view / loss-of-control assessment).
- Whether the suspected vector is internal, vendor-related, or supply-chain-related.
- What vendor coordination is likely to be required.

This situational awareness drives the containment plan in Phase 2.

---

## 7. Phase 2: Containment

### 7.1 Containment decision framework

Containment actions in OT carry production-impact risk that does not arise in IT. The Incident Commander, OT Security Lead, Plant Manager, and (where safety is implicated) Process Safety Engineer must jointly decide between containment options.

| Option | When appropriate | Trade-offs |
| --- | --- | --- |
| **Isolate at conduit** | Adversary movement contained; production continues on isolated zone. | May lose IT-side visibility into OT state; vendor remote access may be impacted. |
| **Block specific protocols or commands** | Adversary technique is protocol-specific; broader connectivity acceptable. | Requires protocol-aware enforcement; legitimate traffic may be inadvertently blocked. |
| **Revoke compromised credentials** | Identity-based compromise. | Active operator sessions may be terminated; production handover required. |
| **Move to manual control** | Confidence that automated control is compromised; manual fallback exists. | Production rate typically reduced; safety review required before invoking. |
| **Controlled shutdown** | Continued operation would create unsafe condition or unacceptable adversary persistence. | Production loss; restart costs; safety-sequence compliance required. |
| **Take no immediate action; monitor closely** | Containment risk exceeds incident risk in the short term; need for evidence preservation. | Adversary may progress; requires intensive monitoring. |

### 7.2 Safety-instrumented system containment

7.2.1 Any containment action affecting SIS or shared SIS/BPCS infrastructure requires explicit Process Safety Engineer approval before execution.

7.2.2 SIS bypass conditions detected during the incident are documented and reported in safety-management channels in addition to the security incident record.

### 7.3 Vendor remote-access containment

7.3.1 On declaration of any P1 or P2 incident, vendor remote-access sessions to the affected zones are terminated and re-establishment is prohibited until the OT Security Lead approves resumption.

7.3.2 Vendor remote-access logs covering the period of suspected compromise are preserved before terminating sessions where possible.

### 7.4 Evidence preservation during containment

7.4.1 Before issuing containment commands that may alter OT state, the Control System Engineer attempts (where lawful and operationally safe) to:

- Capture controller state dumps using vendor-supported methods.
- Capture HMI screen state.
- Capture network-traffic snapshots from conduit boundaries.
- Document the alarm queue contents.

7.4.2 Where preservation and containment conflict on time, the Incident Commander decides. The decision is documented in the incident record.

7.4.3 Evidence is stored per the records retention standard ([`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)) with longer retention for safety-implicated incidents per applicable safety regulation.

---

## 8. Phase 3: Eradication

### 8.1 Adversary removal

8.1.1 Eradication of adversary presence from OT zones must be planned with vendor involvement where the affected components are vendor-controlled. Direct unilateral remediation on vendor-controlled systems risks voiding support contracts and may introduce safety hazard.

8.1.2 Eradication actions must consider:

- Whether compromised firmware on PLCs, controllers, or RTUs requires re-flashing from known-good images.
- Whether configuration of engineering workstations, HMIs, and historians requires rebuild from baselines.
- Whether credentials (operator, engineer, service-account, vendor) need rotation.
- Whether network controls (firewall rules, segmentation policies) need tightening to prevent recurrence.

### 8.2 Verification before recovery

8.2.1 Before exiting eradication, the OT Security Lead verifies:

- No indicators of compromise remain in the affected zones (forensic verification).
- All credentials with potential exposure have been rotated.
- All vendor remote-access paths used during the incident have been disabled or re-secured.
- Configuration baselines have been restored on affected hosts.
- Detection coverage for the observed adversary techniques has been added or tuned.

8.2.2 For SIS-affecting incidents, additional verification by the Process Safety Engineer is required before any safety function is returned to service.

---

## 9. Phase 4: Recovery

### 9.1 Recovery decision authority

9.1.1 Recovery of production OT systems to service requires Incident Commander approval. For incidents affecting safety, joint approval by Incident Commander and Process Safety Engineer is required.

9.1.2 The Plant Manager confirms operational readiness for recovery (manual-control handover completed, recovery procedures rehearsed, operators briefed).

### 9.2 Recovery procedure

9.2.1 Recovery proceeds in a sequence that minimizes safety risk:

1. Verify SIS functions are operational and uncompromised.
2. Verify monitoring and alerting are restored.
3. Verify control system integrity (configuration match to known-good baselines).
4. Restore communications conduits in a controlled sequence.
5. Restore vendor remote access only after explicit Incident Commander approval and re-secured access controls.
6. Re-enable automated control on a phased basis with manual oversight initially.
7. Confirm process stability for a defined observation period before declaring full recovery.

9.2.2 The recovery sequence is documented in the incident record. Any deviation from the sequence requires Incident Commander approval.

### 9.3 Recovery time expectations

9.3.1 OT recovery is typically longer than IT recovery for the same severity class. Recovery objectives accepted for planning purposes:

| OT scenario | Indicative recovery window |
| --- | --- |
| Engineering workstation rebuild from baseline | Hours |
| HMI rebuild and reconfiguration | Hours to a day |
| Controller firmware re-flash (vendor coordination required) | Days |
| Multi-site OT compromise (full recovery) | Days to weeks |
| SIS-implicated incident (with safety-engineering re-verification) | Days minimum |

These windows are indicative; the resilience domain's BC/DR standard ([`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md)) governs binding RTOs at zone level.

---

## 10. Phase 5: Post-incident

### 10.1 Lessons learned

10.1.1 Within 10 business days of recovery, the Incident Commander convenes a lessons-learned review using the template at [`resilience/template-lessons-learned.md`](../../resilience/template-lessons-learned.md). The review must include the OT Security Lead, Plant Manager, Process Safety Engineer, Control System Engineer involved, IT SOC analyst lead, and Vendor Liaison.

10.1.2 The review specifically considers:

- Detection: was the incident detected at the earliest possible point?
- Triage: was severity classified correctly?
- Decisions: were containment and recovery decisions documented with rationale?
- Coordination: did the OT, IT, safety, and vendor teams coordinate effectively?
- Outcome: was production restored safely and within objective windows?
- Standards: do any controls in [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md) need revision in light of the incident?

10.1.3 The review's output feeds into the CAPA register ([`compliance/procedure-capa.md`](../../compliance/procedure-capa.md)) for tracked remediation actions and into the enterprise risk register ([`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md)) for residual risk re-assessment.

### 10.2 Safety review integration

10.2.1 Where the incident had or could have had safety consequences, the lessons-learned output also feeds into the next scheduled HAZOP and LOPA reviews for the affected process. Cyber threat vectors identified become initiating events in the safety analysis.

10.2.2 SIS modifications identified as necessary follow the safety-management change-control process, not the general change-management procedure.

### 10.3 Standards and library updates

10.3.1 Where the incident demonstrates that a library standard, procedure, or guideline requires update, the Document Owner of the affected artefact files an issue and proposes a revision.

10.3.2 Glossary, canonical-citations, or coverage-gap register updates triggered by the incident are filed at the same time.

---

## 11. Communications

### 11.1 Internal communications

11.1.1 Internal communications during OT incidents are governed by the cross-domain incident coordination procedure ([`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md)). OT-specific additions:

- Plant operations leadership is notified at incident declaration regardless of severity.
- Safety management is notified within 1 hour for any SIS-implicated or safety-consequential incident.
- Executive leadership is notified for P1 and P2 incidents per the incident escalation matrix ([`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md)).

11.1.2 No public-facing statement about an OT incident is issued without Communications Owner approval and Legal Counsel review.

### 11.2 External communications

11.2.1 Regulatory reporting obligations vary by jurisdiction and sector. The Communications Owner and Legal Counsel determine applicability and timing for each incident. Common OT-relevant reporting regimes:

- **NERC CIP** (North American electricity): EOP-004-4 emergency reporting; CIP-008 reportable cyber security incidents.
- **EU NIS 2** (essential or important entities): 24-hour early warning, 72-hour incident report, 1-month final report per the NIS 2 implementation annex ([`compliance/annex-nis-2-implementation.md`](../../compliance/annex-nis-2-implementation.md)).
- **Sector-specific transport regulators**: TSA pipeline directives (US), maritime cyber reporting (IMO Resolution MSC-FAL.1/Circ.3), aviation cyber reporting (ICAO Doc 10055).
- **Privacy regulators**: where the OT incident affects personal data (operator credentials, employee records on engineering workstations) per the privacy breach response procedure ([`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md)).

11.2.2 Sector coordinator reporting (E-ISAC for North American electricity; WaterISAC for US water sector; equivalent ISACs by sector) is voluntary but encouraged and may be required by sector-specific obligations the adopter participates in.

### 11.3 Vendor communications

11.3.1 Vendor notification of incidents affecting their supplied systems is required per contractual obligations established in the OT/ICS Security Standard section 11.3.

11.3.2 Where the vendor itself is the source or vector (vendor system compromise, supply-chain incident), vendor incident response cooperation is invoked per contract.

---

## 12. Forensics in OT

### 12.1 Constraints

OT forensics operates under constraints that do not apply to IT forensics:

- **Production cannot generally be paused for imaging.** Forensic capture must be planned to occur within available maintenance windows or on isolated representative systems.
- **Vendor-controlled systems may not permit deep forensic access** without vendor support. Vendor cooperation is part of the forensic plan.
- **Some OT components have no persistent storage to image.** Forensic evidence comes from network traffic captures, alarm-and-event logs, and configuration snapshots rather than disk images.
- **Volatile evidence is the rule, not the exception.** Capture is opportunistic; lost evidence is lost forever.

### 12.2 Acceptable forensic actions

12.2.1 Network-traffic capture at conduit boundaries is acceptable during incidents without operational impact.

12.2.2 Configuration snapshots of PLCs, HMIs, and engineering workstations using vendor-supported tools are acceptable without operational impact.

12.2.3 Memory or disk imaging of OT components that requires the component to be taken offline must be planned with Plant Manager approval and (for safety-critical components) Process Safety Engineer approval.

12.2.4 Where deep forensics requires sending components to a third-party laboratory, the vendor and the safety regulator (where applicable) must be consulted.

### 12.3 Chain of custody

12.3.1 OT forensic evidence is subject to the same chain-of-custody discipline as IT evidence per the base incident response procedure. The OT Security Lead is the custodian of OT-specific evidence.

12.3.2 Evidence retention duration is governed by the records retention standard with safety-regulation precedence where applicable.

---

## 13. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | Establishing an IACS security programme | Incident management within IACS programme |
| NIST SP 800-82 Rev. 3 | Guide to Operational Technology (OT) Security | Incident handling guidance for OT |
| NIST SP 800-61 Rev. 3 | Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile) | Base IR lifecycle (preparation, detection and analysis, containment, eradication and recovery, post-incident); Rev. 3 also maps these activities to the six functions of NIST CSF 2.0 |
| ISO/IEC 27035 | Information security incident management | Broader incident management framework |
| IEC 61511 | Functional safety: Safety instrumented systems for the process industry sector | Safety-management precedence on SIS-implicated incidents |
| NERC CIP-008 | Cyber security incident reporting and response planning | North American electricity reporting requirements |
| EU NIS 2 Directive | Cybersecurity of network and information systems | EU essential-entity reporting timelines |
| TSA Pipeline Security Directives | Sector-specific incident reporting | US pipeline operators |
| IMO MSC-FAL.1/Circ.3 | Maritime cyber risk management | Maritime sector incident considerations |

---

**End of Document**
