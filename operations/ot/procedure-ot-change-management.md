# OT Change Management Procedure

**Document Title:** OT Change Management Procedure\
**Document Type:** Procedure\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md), [`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md), [`operations/procedure-change-management-and-configuration-control.md`](../procedure-change-management-and-configuration-control.md), [`operations/procedure-patch-management.md`](../procedure-patch-management.md), [`security/policy-acceptance-into-service.md`](../../security/policy-acceptance-into-service.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), [`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md), [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](../../compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and following any material OT change-induced incident or change to IEC 62443 / IEC 61511 / NIST SP 800-82\
**Repository Path:** [`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## 1. Purpose

This procedure defines change management for Operational Technology (OT) environments. It extends the general change management and configuration control procedure ([`operations/procedure-change-management-and-configuration-control.md`](../procedure-change-management-and-configuration-control.md)) with OT-specific requirements: extended change windows aligned with production-maintenance schedules, mandatory vendor coordination for vendor-controlled systems, regression testing for safety-critical functions, and integration with safety-management of change (MOC) under IEC 61511 where the change affects Safety Instrumented Systems.

The procedure applies to any change affecting an OT zone, conduit, controller, HMI, engineering workstation, historian, BMS, or SIS asset within the scope of the OT/ICS Security Standard ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)).

---

## 2. Scope

### 2.1 Changes in scope

This procedure governs:

- **Configuration changes**: PLC logic, HMI screen content, SCADA tag definitions, alarm setpoints, control-loop tuning, network-policy entries on OT firewalls.
- **Patch and firmware updates**: controller firmware, HMI software, historian software, engineering-workstation operating system or application patches.
- **Hardware changes**: controller replacement, sensor or actuator replacement, network-equipment swap-out, addition or removal of OT assets.
- **Network architecture changes**: zone-and-conduit redesign, segmentation changes, addition or removal of conduits, vendor remote-access path changes.
- **Identity and access changes**: addition or removal of OT users, privilege changes, service-account changes, vendor-account provisioning or revocation.
- **Vendor-driven changes**: any change instigated by an OT vendor or integrator including maintenance visits and remote interventions.

### 2.2 Out of scope

- Pure IT changes with no OT zone or conduit (governed by the general change management procedure).
- Emergency incident response actions (governed by the OT Incident Response Procedure; changes made during incident response are post-event recorded against this procedure for traceability).
- Routine operator setpoint changes within sanctioned ranges (governed by operations procedures, not security change management).

### 2.3 Safety-management precedence

Where a change affects Safety Instrumented Systems (SIS) or other safety-critical functions, IEC 61511 management of change requirements apply in addition to this procedure. The safety-management process takes precedence on any conflict. Cyber-specific elements (security testing, security verification) are integrated into the safety-management process rather than run in parallel.

---

## 3. Roles

| Role | OT change management responsibility |
| --- | --- |
| **OT Security Lead** | Reviews all OT changes for security impact; approves changes affecting zone-and-conduit architecture, vendor remote access, or OT security telemetry; chairs the OT Change Advisory Board (OT-CAB). |
| **Plant Manager / Operations Director** | Authorises any production-impacting change; coordinates production-maintenance windows; signs off on operational readiness. |
| **Process Safety Engineer** | Mandatory reviewer for any change affecting SIS, shared SIS/BPCS infrastructure, or safety-relevant control loops; coordinates with IEC 61511 management-of-change process. |
| **Control System Engineer** | Designs, tests, and implements OT changes under direction from the requestor; produces the technical change package including test results. |
| **Change Requester** | Originates the change request; documents business or operational justification, scope, risk, and backout plan. |
| **OT-CAB** | Change Advisory Board for OT changes. Composition includes the OT Security Lead (chair), Plant Manager or delegate, Process Safety Engineer (for safety-relevant changes), Control System Engineer, and Vendor Liaison where vendor-controlled systems are affected. Equivalent to the general CAB for OT scope. |
| **Vendor Liaison** | Coordinates vendor involvement in vendor-controlled changes; obtains vendor approval where vendor support contracts require it; documents vendor change instructions. |
| **CISO** | Approves emergency changes; approves changes affecting SL-T or SL-A determinations; reviews change-management metrics annually. |
| **Internal Audit** | Reviews change records and OT-CAB minutes for compliance with this procedure. |

---

## 4. Guiding principles

### 4.1 Production-first scheduling

OT changes are scheduled into planned production-maintenance windows wherever feasible. The IT pattern of frequent, automated, low-ceremony changes does not apply to production OT. Adopters set their own production cadence (annual major maintenance is common in process industries; quarterly may apply in less safety-critical environments).

### 4.2 Vendor coordination from the outset

Vendor-controlled systems require vendor involvement from the planning stage, not just implementation. Vendor approval is sought before formal change request submission where the support contract requires it.

### 4.3 Test before production

OT changes must be tested in a representative environment before production application. "Representative" means a test bench, simulator, or non-production zone configured equivalently to the target zone. Direct production changes are permitted only where the change is reversible, low risk, and explicitly authorised by the OT-CAB.

### 4.4 Reversibility planning

Every change request must document a backout plan. Where a change is irreversible (firmware re-flash without backup of prior firmware, hardware replacement without preserved spares, configuration changes whose prior state cannot be restored), the irreversibility is disclosed in the change request and weighed in OT-CAB approval.

### 4.5 Safety integration

Safety-relevant changes are governed by the IEC 61511 management-of-change process. Cyber-specific elements are folded into that process rather than run separately. The Process Safety Engineer is mandatory reviewer.

### 4.6 No silent change

Every change is recorded in the OT change register. Operators, engineers, and vendors who observe undocumented changes report rather than approve in retrospect.

---

## 5. Change categories

### 5.1 Standard change

Pre-approved, low-risk, repeatable changes. The OT-CAB pre-approves a catalogue of standard-change types annually. Examples:

- Operator account additions/removals within sanctioned roles.
- HMI screen tweaks that do not affect alarm logic.
- Updates to non-safety alarm thresholds within sanctioned ranges.
- Application of vendor-released patches that the OT-CAB has pre-approved for routine application.

Standard changes follow the request-implement-record flow without per-change OT-CAB approval. Standard-change catalogue is reviewed annually.

### 5.2 Normal change

The default category. Any change not on the standard-change catalogue and not meeting emergency criteria. Goes through the full change request, risk assessment, OT-CAB approval, test, implement, verify cycle described in this procedure.

### 5.3 Emergency change

Changes required to respond to an active incident or safety hazard. Authorised by the CISO (cyber emergency) or Plant Manager (safety emergency) with retrospective OT-CAB review within 5 business days.

Emergency change requirements:

- Documented in the incident or change record at the time of execution.
- Backout plan, if any, documented at the time of execution or noted as not feasible.
- Retrospective review identifies any standing-change opportunity to avoid future emergency invocation.

### 5.4 Vendor-driven change

Any change instigated by an OT vendor or integrator. Categorized as Normal or Emergency per the actual change content. Vendor must follow this procedure (via Vendor Liaison) even when vendor support contract terms differ.

### 5.5 Safety-related change

Any change affecting SIS, shared SIS/BPCS infrastructure, or other safety-relevant control loops. Subject to IEC 61511 management of change in addition to this procedure. Process Safety Engineer review is mandatory; vendor coordination is mandatory where the safety system is vendor-controlled. Cannot be a Standard change.

---

## 6. Change request

### 6.1 Request content

Each OT change request must include:

- **Change identifier**: unique ID from the change-management system.
- **Requester**: the role or function originating the change.
- **Change category**: Standard / Normal / Emergency / Safety-related.
- **Scope**: affected zones, conduits, components, with explicit asset-identifier references from the OT asset inventory.
- **Business or operational justification**: why the change is needed.
- **Technical description**: what is being changed, in what state-from / state-to terms.
- **Risk assessment**: cyber, safety, operational, and reputational impact assessment (section 7).
- **Test plan**: how the change will be validated before production application (section 8).
- **Implementation plan**: who, when, in what sequence, with what production-window arrangement.
- **Backout plan**: how to return to the prior state if the change fails. Where backout is not feasible, the irreversibility is declared.
- **Verification plan**: how successful implementation will be confirmed.
- **Vendor involvement**: which vendor activities are required, with vendor approval evidence where applicable.

### 6.2 Submission timeline

| Category | Submission timeline ahead of intended implementation |
| --- | --- |
| Standard | Just-in-time submission acceptable; records made at execution |
| Normal | Minimum 10 business days; longer for major changes |
| Emergency | At time of execution or as soon as feasible thereafter |
| Safety-related | Per IEC 61511 management-of-change cycle (typically longer than Normal; safety review depth determines lead time) |

### 6.3 Change register

All change requests are recorded in the OT change register, which is maintained alongside the asset inventory in the OT Asset Inventory and Lifecycle Register (Phase 22.5 deliverable). Until that register is established, the change register is maintained in the general change-management system with an OT-scope flag.

---

## 7. Risk assessment

### 7.1 Risk-assessment dimensions

Each Normal, Emergency, and Safety-related change request must be assessed across four dimensions:

| Dimension | Considerations |
| --- | --- |
| **Cyber** | Effect on SL-A; new attack surface; conduit changes; identity changes; vendor-access changes. |
| **Safety** | Effect on SIS or safety functions; HAZOP/LOPA implications; safety-regulation triggers. |
| **Operational** | Production downtime; product-quality effect; alarm-management effect; operator-training need. |
| **Reputational and regulatory** | Sector-regulator notification triggers; customer-contract implications; environmental release potential. |

### 7.2 Risk-tier output

The assessment produces a risk tier driving the depth of review and the OT-CAB composition required:

| Tier | Criteria | Review depth |
| --- | --- | --- |
| **Tier 1: Critical** | Affects SIS; affects multiple zones; affects SL-T of any zone; vendor-irreversible. | Full OT-CAB; Process Safety Engineer mandatory; CISO sign-off. |
| **Tier 2: High** | Single zone, single conduit, or single component with material cyber-impact. | Full OT-CAB; CISO informed. |
| **Tier 3: Moderate** | Confined to a single asset with no SL or conduit impact. | OT Security Lead and Control System Engineer sign-off; OT-CAB informed. |
| **Tier 4: Low** | Maps to a standard-change template. | Standard-change flow per section 5.1. |

### 7.3 Cyber risk specifics

7.3.1 Where a change modifies the configuration of a component contributing to a zone's SL-A, the change must include a re-measurement of the zone's SL-A after implementation. If the post-change SL-A falls below SL-T, the gap is recorded in the CAPA register.

7.3.2 Changes that introduce new conduits to external networks (internet, vendor remote access, cloud services) are Tier 1 by default unless the OT-CAB documents a lower tier with rationale.

---

## 8. Testing

### 8.1 Test-environment requirements

OT changes are tested before production application using one or more of:

- **Sandbox or simulator**: vendor-provided simulator, digital twin, or virtualised representation of the target system. Suitable for logic-only changes (PLC programs, HMI screen logic).
- **Engineering test bench**: physical hardware-in-the-loop test environment. Required for changes involving hardware, firmware, or low-level protocol behaviour.
- **Representative non-production zone**: a production-shadow zone configured equivalently to the target zone. Required for changes affecting zone-and-conduit architecture or multi-component interactions.

8.1.1 Test environments must be maintained in configuration parity with production. Configuration drift between test and production invalidates test results.

### 8.2 Cyber regression testing

8.2.1 Each Tier 1 and Tier 2 change must include cyber regression testing to confirm that existing security controls remain functional after the change. The cyber regression suite covers, at minimum:

- Authentication and authorisation enforcement on affected interfaces.
- Conduit-boundary enforcement (firewall rules, protocol restrictions).
- Logging continuity (no gaps introduced).
- SIEM integration continuity.
- Privileged access controls.

8.2.2 Cyber regression results are attached to the change record.

### 8.3 Safety regression testing

8.3.1 Safety-related changes must include safety-function regression testing per IEC 61511 management-of-change requirements. The testing scope, depth, and pass criteria are determined by the Process Safety Engineer.

8.3.2 Safety regression results are attached to the change record and to the safety-management record.

### 8.4 Performance and timing regression

8.4.1 Where the change affects deterministic real-time behaviour (control-loop latency, sample rates, communication timing), performance regression testing must confirm that timing requirements remain met.

8.4.2 Performance regression failures are blocking for production application.

---

## 9. Approval

### 9.1 OT-CAB cadence

The OT-CAB meets at least monthly and on demand for emergency or major changes. Standing agenda includes review of pending Normal and Safety-related changes, retrospective review of Emergency changes since last meeting, and annual review of the standard-change catalogue.

### 9.2 Approval criteria

The OT-CAB approves a change request when it confirms:

- Risk assessment is complete and the risk tier is appropriate.
- Test plan is appropriate to the risk tier and test results are satisfactory.
- Implementation plan does not conflict with production schedule or other scheduled changes.
- Backout plan is documented (or irreversibility is explicit and accepted).
- Verification plan is concrete.
- Vendor coordination is complete (where applicable).
- Process Safety Engineer has signed off (where safety-relevant).
- CISO has signed off (where SL-T or SL-A is affected, or for Tier 1 changes).

### 9.3 Conditional approval

The OT-CAB may approve subject to conditions (additional test cases, expanded backout plan, restricted implementation window). Conditions are tracked in the change record and verified before implementation begins.

### 9.4 Rejection and resubmission

Rejected requests return to the requester with rationale. Resubmission requires addressing the OT-CAB's concerns and goes through the full cycle again.

---

## 10. Implementation

### 10.1 Production-window scheduling

10.1.1 Implementation occurs during a production-maintenance window approved by the Plant Manager. Windows are scheduled in advance with change requests aligned to the window.

10.1.2 Where a Normal change requires implementation outside the next scheduled window (urgency, vendor availability), the Plant Manager authorises an out-of-window implementation specifically.

### 10.2 Implementation team

10.2.1 Implementation is performed by the Control System Engineer with witnesses from the OT Security Lead's team and (where safety-relevant) the Process Safety Engineer's team.

10.2.2 Vendor personnel implementing the change must operate under the vendor remote-access controls of the OT/ICS Security Standard section 7.4 or under in-person supervision at the site.

### 10.3 Privileged session capture

10.3.1 Implementation sessions on engineering workstations or vendor-supplied tools are recorded per the privileged access management standard ([`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md)). Session recordings are retained per the records retention standard ([`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)).

### 10.4 Real-time monitoring

10.4.1 During implementation, the IT SOC and (where staffed) the OT Security Lead monitor for anomalies that may indicate that the change is causing unintended effects.

10.4.2 If anomalies are detected during implementation, the implementation pauses and the OT-CAB Chair (or delegate) decides whether to continue, backout, or escalate.

---

## 11. Verification

### 11.1 Functional verification

11.1.1 After implementation, the Control System Engineer verifies that the change produces the intended functional behaviour. Verification is per the verification plan submitted with the change request.

### 11.2 Cyber verification

11.2.1 The OT Security Lead verifies that:

- SL-A measurements for affected zones and conduits remain at or above SL-T (or, if below, the gap is recorded per section 7.3.1).
- New conduits are configured per the change package.
- Identity and access changes are reflected in the IAM systems.
- Logging and SIEM integration remain functional.

### 11.3 Safety verification

11.3.1 For safety-related changes, the Process Safety Engineer verifies that safety functions remain operational and meet their assigned Safety Integrity Level (SIL). Sign-off is required before the safety function is returned to service.

### 11.4 Verification record

11.4.1 Verification results are attached to the change record. The change is closed only after all verification activities are signed off.

---

## 12. Backout

### 12.1 Backout triggers

12.1.1 Backout is invoked when:

- The change produces unintended effects detected during implementation or verification.
- A safety hazard arises from the change.
- The change cannot be completed within its authorised window.

### 12.2 Backout authorisation

12.2.1 Backout is authorised by the OT-CAB Chair (or delegate) for non-safety changes and jointly with the Process Safety Engineer for safety-related changes.

### 12.3 Backout execution

12.3.1 Backout follows the documented plan from the change request. Where the documented plan cannot be executed (unexpected dependencies, missing artefacts), the situation becomes an incident and the OT Incident Response Procedure ([`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md)) is invoked.

### 12.4 Post-backout review

12.4.1 Any change that triggers backout receives a post-backout review at the next OT-CAB meeting. The review identifies whether the testing process should be strengthened, the risk assessment was incomplete, or the change scope should be revised.

---

## 13. Documentation and audit trail

### 13.1 Change record retention

13.1.1 OT change records (request, approvals, test results, implementation evidence, verification, any backout) are retained per the records retention standard with longer retention for safety-related changes per applicable safety regulation. North-American electricity-sector operators retain per NERC CIP-010 requirements where applicable.

### 13.2 Configuration baseline management

13.2.1 Every approved and implemented change updates the affected component's configuration baseline. The OT Asset Inventory and Lifecycle Register (Phase 22.5 deliverable) is the canonical source of baselines.

13.2.2 Configuration baselines (PLC logic, HMI screens, firewall rule sets) are version-controlled with each version tied to the change record that introduced it. Engineering workstations maintain the source-of-truth files; production controllers reflect the deployed version.

### 13.3 Audit access

13.3.1 Internal Audit accesses OT change records on request without restriction. Audit findings related to OT change management feed into the CAPA register.

13.3.2 Sector regulators with audit rights (NERC, NIS 2 competent authorities, sector inspectors) access OT change records per regulatory requirement.

---

## 14. Metrics

### 14.1 OT change KPIs

The OT Security Lead reports the following monthly:

| Metric | Target |
| --- | --- |
| Change-success rate (changes implemented without backout) | ≥ 95% |
| Emergency-change rate (emergency changes as % of total) | ≤ 5% |
| Unauthorised-change detection rate (changes detected post-event without prior approval) | Trend toward zero |
| OT-CAB meeting attendance (mandatory members) | ≥ 90% |
| Mean time from change request to OT-CAB review | ≤ 10 business days for Normal |
| Vendor-driven change traceability (vendor changes with complete records) | 100% |

### 14.2 Annual review

The OT Security Lead and CISO review change-management metrics annually and identify systemic improvement opportunities. Outputs feed into the continual improvement programme and CAPA register.

---

## 15. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | Establishing an IACS security programme | Change-management requirements within IACS programme |
| IEC 62443-3-3 | System security requirements and security levels (SR 3.4 Software and information integrity; SR 7.6 Network and security configuration settings) | Configuration management technical requirements |
| NIST SP 800-82 Rev 3 | Guide to Operational Technology (OT) Security | OT change-management guidance |
| ISO/IEC 27001:2022 | A.5.37 Documented operating procedures; A.8.32 Change management | ISMS change-management baseline |
| IEC 61511 | Functional safety: Safety instrumented systems for the process industry sector | Management of change for SIS (mandatory integration) |
| NERC CIP-010 | Configuration change management and vulnerability assessments | North-American electricity sector (cross-reference in energy-and-utilities annex) |
| ITIL 4 | Change enablement practice | General change management baseline |
| EU NIS 2 Directive | Cybersecurity of network and information systems | Change-management evidence for essential-entity audits |

---

**End of Document**
