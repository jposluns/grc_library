# OT/ICS Security Standard

**Document Title:** OT/ICS Security Standard\
**Document Type:** Standard\
**Version:** 1.0.1\
**Date:** 2026-05-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`operations/standard-network-security-and-segmentation.md`](../standard-network-security-and-segmentation.md), [`operations/procedure-change-management-and-configuration-control.md`](../procedure-change-management-and-configuration-control.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md), [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](../../compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](../../compliance/logistics/annex-logistics-sector-requirements.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and upon material change to IEC 62443, NIST SP 800-82, or sector-specific OT regulations\
**Repository Path:** [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard establishes mandatory security requirements for Operational Technology (OT) environments operated by the organisation, including Industrial Control Systems (ICS), Supervisory Control and Data Acquisition (SCADA), Distributed Control Systems (DCS), Programmable Logic Controllers (PLCs), Human-Machine Interfaces (HMIs), Building Management Systems (BMS), and Safety Instrumented Systems (SIS).

The standard codifies the conceptual model introduced in [`annex-ot-security-overview.md`](annex-ot-security-overview.md) into auditable control requirements. It applies to every OT zone and conduit under the organisation's control and to vendor and integrator activities that affect those zones and conduits.

The standard aligns to IEC 62443 (primary) and NIST SP 800-82 Rev 3 (secondary). Where sector-specific regulation (NERC CIP for North American electricity; sector annexes for transportation, healthcare, energy) imposes additional requirements, the sector annex extends this standard.

---

## 2. Scope

### 2.1 In scope

This standard applies to:

- All ICS, SCADA, DCS, PLC, HMI, and engineering-workstation assets operated by the organisation or its subsidiaries.
- All SIS in the organisation's process facilities, with safety regulations taking precedence where conflict arises.
- All BMS deployments where they manage facility infrastructure (HVAC, fire/life-safety, physical access control, smart-building automation).
- All conduits (logical communication channels) connecting OT zones to each other, to IT networks, or to external networks.
- All vendor, integrator, and third-party activities that access, modify, or extend the above.

### 2.2 Out of scope

This standard does not cover:

- General IT security controls (the universal baseline applies; this standard layers OT-specific overlays).
- Functional safety design itself (governed by IEC 61511 / IEC 61508; this standard governs the security of safety systems, not the safety design).
- Medical-device security (governed by healthcare-sector annexes; medical-device control is OT-adjacent but regulated separately).
- Vehicle-embedded control systems outside facility operations.

### 2.3 Exceptions

Where an OT system cannot meet a requirement of this standard because of vendor lock-in, legacy constraints, or safety-regulation precedence, an exception must be filed per [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md) with compensating controls documented and approved.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns this standard; approves OT zone definitions, security-level targets, and exceptions. Reviews OT incident reports. |
| **OT Security Lead** | Day-to-day OT security operations; maintains zone-and-conduit inventory; oversees SL-T setting and SL-A verification. Reports to CISO. Where the organisation does not have a dedicated OT Security Lead, the role merges with Security Owner per [`governance/register-role-authority.md`](../../governance/register-role-authority.md). |
| **Plant Manager / Operations Director** | Accountable for safe and continuous operation; signs off on changes affecting production zones; coordinates with OT Security Lead on outage windows. |
| **Process Safety Engineer** | Accountable for SIS integrity and safety-related changes; consulted on any security change affecting safety-instrumented functions. |
| **Control System Engineer** | Implements and maintains OT control systems; executes hardening, patching, and configuration changes per this standard. |
| **IT Security Operations Centre (SOC)** | Monitors OT-aware telemetry feeding into the SIEM; escalates OT alerts to the OT Security Lead and Plant Manager. |
| **Supplier Owner** | Manages vendor and integrator contracts and access governance per [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), with OT-specific additions in section 11 below. |

---

## 4. Definitions

Terms used in this standard are defined in the library glossary ([`governance/register-glossary.md`](../../governance/register-glossary.md)). Key terms used here include: OT, ICS, IACS, SCADA, DCS, PLC, HMI, BMS, SIS, SIL, SL-T, SL-A, SL-C, Purdue model, IT/OT convergence.

---

## 5. Zone-and-conduit architecture

### 5.1 Zone definition (62443-3-2)

5.1.1 Every OT asset under organisational control must be assigned to a zone. No OT asset may exist outside a zone.

5.1.2 Each zone must have:

- A unique zone identifier.
- A named zone owner (role per the role authority register, not an individual).
- A defined asset list (devices, systems, software, processes).
- A defined logical and physical boundary.
- A documented security policy stating permitted activities within the zone and at the boundary.
- A risk assessment per IEC 62443-3-2 producing the zone's Security Level Target (SL-T).

5.1.3 The zone inventory must be maintained in the OT Asset Inventory and Lifecycle Register ([`operations/ot/register-ot-asset-inventory-and-lifecycle.md`](register-ot-asset-inventory-and-lifecycle.md)).

5.1.4 Zones must be reviewed at least annually, on any material change to the underlying system, and following any cyber or safety incident affecting the zone.

### 5.2 Conduit definition (62443-3-2)

5.2.1 Every inter-zone communication channel must be modelled as a conduit. No inter-zone traffic may exist outside a conduit.

5.2.2 Each conduit must have:

- A unique conduit identifier.
- A named conduit owner.
- Endpoints (the zones the conduit connects).
- Permitted protocols, ports, application messages, and direction (uni- or bi-directional).
- A risk assessment producing the conduit's SL-T.
- Documented security controls applied at each endpoint (filtering, authentication, encryption, monitoring, logging).

5.2.3 Conduits between OT zones and IT zones must terminate in a DMZ (commonly Purdue Level 3.5) and must not permit direct OT-to-IT or IT-to-OT traffic.

5.2.4 Conduits between OT zones and external networks (internet, vendor remote-access providers, cloud services) require explicit CISO approval and are governed by section 11 below.

### 5.3 Risk assessment

5.3.1 Each zone and conduit risk assessment must follow IEC 62443-3-2 and must consider:

- Cyber consequence (compromise of confidentiality, integrity, availability).
- Safety consequence (physical injury, environmental harm).
- Production consequence (downtime, product quality, regulatory impact).
- Threat actor capability range (SL 1 through SL 4 per IEC 62443-3-3).
- Existing controls and their effectiveness.

5.3.2 Risk assessments must be repeated at least every three years, on material system change, on threat-landscape change, and following any incident in scope.

5.3.3 Risk-assessment outputs feed into the enterprise risk register per [`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md).

### 5.4 Purdue model alignment

5.4.1 Adopters with established Purdue Enterprise Reference Architecture deployments must map Purdue layers to IEC 62443 zones. The mapping is documented in the zone inventory.

5.4.2 The Purdue model is informative, not mandatory. New OT architectures should follow IEC 62443 zone-and-conduit thinking directly; legacy Purdue deployments are accepted but must be mapped.

---

## 6. Security-level achievement

### 6.1 Security Level Target (SL-T)

6.1.1 Each zone and conduit must have an assigned SL-T value in the range SL 1 through SL 4 per IEC 62443-3-3:

| SL | Protection against |
| --- | --- |
| **SL 1** | Casual or coincidental violation. |
| **SL 2** | Intentional violation by simple means, low resources, generic skills. |
| **SL 3** | Intentional violation by sophisticated means, moderate resources, IACS-specific skills. |
| **SL 4** | Intentional violation by sophisticated means, extended resources, IACS-specific skills, high motivation (nation-state grade). |

6.1.2 SL-T must be set on the basis of the zone or conduit risk assessment, not arbitrarily. CISO approval is required for SL-T assignment.

6.1.3 Zones containing or conduits carrying communications for SIS or other safety-critical functions must have SL-T of at least SL 3 unless the risk assessment justifies SL 2 with documented compensating controls.

6.1.4 Zones containing critical national infrastructure functions in scope of NERC CIP, NIS 2, or equivalent regulation must have SL-T set per the regulatory requirement, with the regulation taking precedence over internal risk-based setting where the regulation is more stringent.

### 6.2 Security Level Achieved (SL-A)

6.2.1 SL-A for each zone and conduit must be measured at least annually and after any material change.

6.2.2 SL-A measurement uses the foundational requirements in IEC 62443-3-3:

| FR | Foundational Requirement |
| --- | --- |
| **FR 1** | Identification and Authentication Control (IAC). |
| **FR 2** | Use Control (UC). |
| **FR 3** | System Integrity (SI). |
| **FR 4** | Data Confidentiality (DC). |
| **FR 5** | Restricted Data Flow (RDF). |
| **FR 6** | Timely Response to Events (TRE). |
| **FR 7** | Resource Availability (RA). |

6.2.3 SL-A is the lowest SL achieved across the seven foundational requirements. A zone with FR 1 at SL 3, FR 2 at SL 2, and all others at SL 3 has SL-A of SL 2.

6.2.4 When SL-A is less than SL-T, the gap must be tracked in the CAPA Register per [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md), with a remediation plan and target date.

### 6.3 Security Level Capability (SL-C)

6.3.1 OT components procured by the organisation must have a documented SL-C from the vendor stating the security level they are capable of achieving when correctly configured. Components without a stated SL-C may be procured only with CISO approval and documented compensating controls.

6.3.2 For each OT component in the asset inventory, the SL-C must be recorded alongside the SL-A of the zone or conduit the component supports. The SL-A of a zone or conduit cannot exceed the lowest SL-C of any component contributing to it.

6.3.3 Vendor SL-C claims must be verified during procurement and on material vendor change (firmware revision, product line transition).

---

## 7. OT-specific access control

### 7.1 Identity management

7.1.1 Every OT user account must be uniquely attributable to an identifiable person or service. Generic shared accounts ("operator", "engineer", "admin") are prohibited except where vendor or safety constraints make individual accounts technically infeasible; in such cases, compensating physical-access logging must be in place.

7.1.2 OT identity sources are governed by [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md). OT engineering workstations that are domain-joined fall under the same IAM standard with the OT-specific overlays in this section.

7.1.3 Service accounts used by OT controllers, historians, and middleware must be:

- Documented in the asset inventory.
- Provisioned with the minimum privilege required.
- Rotated on a defined schedule (annual at minimum; more frequent where vendor support permits).
- Excluded from interactive login where technically possible.

### 7.2 Authentication

7.2.1 Multi-factor authentication is required for:

- All remote access into any OT zone.
- All access to engineering workstations capable of modifying PLC or controller logic.
- All access to safety-related configuration interfaces.
- All access to the OT DMZ (Purdue Level 3.5) from the IT side.

7.2.2 Where MFA is technically infeasible (legacy HMI without MFA support; vendor-supplied appliance without MFA capability), the affected access must be confined to a physical-access-controlled location and logged via compensating controls (video, badge readers, witness presence).

7.2.3 Default vendor credentials must be changed before any OT component is connected to a zone. The change must be verified during commissioning.

### 7.3 Authorisation and privilege

7.3.1 Privilege levels for OT users must be enumerated:

- **Operator**: read access to HMI displays; ability to issue routine commands (start, stop, setpoint changes within defined ranges) but not to modify configuration or logic.
- **Maintenance**: above, plus diagnostic access and limited configuration changes within defined ranges.
- **Engineer**: above, plus logic and configuration changes (PLC programming, HMI screen development, alarm reconfiguration).
- **Administrator**: above, plus system-wide configuration and identity-management changes.
- **Safety Engineer**: separate privilege track for SIS modifications, with mandatory dual-approval per safety-management practice.

7.3.2 Privilege is assigned to roles, not individuals. Individuals are added to roles per the access-control procedure ([`security/procedure-access-control.md`](../../security/procedure-access-control.md)).

7.3.3 Privileged Access Management ([`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md)) applies to Engineer, Administrator, and Safety Engineer roles. Privileged sessions must be recorded.

### 7.4 Vendor and integrator remote access

7.4.1 Vendor and integrator remote access into OT zones is prohibited by default. Where required for support or maintenance:

- Access must be approved by the OT Security Lead and the affected Plant Manager.
- Access must be time-bounded (the session has a start time, expected duration, and automatic disconnect).
- Access must be authenticated with MFA at the OT DMZ ingress point.
- Access must be logged and the session recorded.
- Access must use a jump host that the organisation controls, not direct vendor-to-OT-zone tunnels.
- Vendor accounts used for the session must be unique to the vendor representative (not shared vendor accounts).

7.4.2 Persistent vendor connections (always-on cellular modems, dedicated VPN tunnels) require explicit CISO approval, must terminate in the OT DMZ, and must include the controls above.

7.4.3 Vendor access reviews are conducted at least quarterly to confirm continued business justification.

---

## 8. Network controls

### 8.1 Segmentation

8.1.1 Network segmentation at conduit boundaries is mandatory. Acceptable boundary mechanisms include firewalls, unidirectional gateways (data diodes), and protocol-aware OT firewalls. Layer-2 separation alone is not sufficient where conduits cross trust boundaries.

8.1.2 The boundary between IT and OT must use a defined DMZ. Direct IT-to-OT or OT-to-IT connections without DMZ traversal are prohibited.

8.1.3 East-west traffic within an OT zone may be permitted by zone policy. Inter-zone traffic must traverse a conduit and meet conduit policy.

### 8.2 Protocol governance

8.2.1 Permitted OT protocols (Modbus, DNP3, EtherNet/IP, PROFINET, OPC UA, BACnet, etc.) must be enumerated per conduit. Unenumerated protocols are prohibited at the conduit boundary.

8.2.2 Where protocol versions offer authentication or encryption (for example, OPC UA with security policy enabled), the authenticated and encrypted version must be used. Where the protocol is insecure by design (Modbus, classic DNP3) and replacement is infeasible, compensating segmentation and monitoring controls are mandatory.

8.2.3 Tunnelling OT protocols over IT-network paths must use authenticated and encrypted tunnels.

### 8.3 Wireless OT

8.3.1 Wireless connectivity within OT zones requires CISO approval. Where permitted:

- WPA3-Enterprise (or stronger) encryption with mutual authentication.
- Network segmentation from wired OT networks where practical.
- Continuous monitoring for rogue access points.
- Documented coverage area to constrain attack surface.

8.3.2 Wireless connectivity to safety-instrumented systems is prohibited.

---

## 9. Endpoint and host hardening

### 9.1 Configuration baselines

9.1.1 Engineering workstations, HMI hosts, historians, and other OT-purpose IT hosts must follow hardening baselines per [`operations/standard-production-security-requirements.md`](../standard-production-security-requirements.md) with the OT-specific exceptions documented per host.

9.1.2 Default configuration on PLCs, RTUs, and embedded OT components must be changed during commissioning. Changes follow vendor guidance where the vendor has explicit hardening recommendations; otherwise the OT Security Lead determines the configuration.

9.1.3 Removable media use within OT zones is prohibited except via a sanctioned media-staging process at the DMZ (incoming media scanned and converted to read-only on transfer into the OT zone). Vendors arriving with maintenance media must use the sanctioned process.

### 9.2 Patching

9.2.1 OT components must have a documented patching cadence appropriate to the asset type, vendor support, and risk profile. Monthly patching as practised in IT environments is not assumed; OT patching is typically aligned with planned production-maintenance windows.

9.2.2 Patches must be tested in a representative non-production OT environment before production deployment, except where vendor explicitly permits direct production patching.

9.2.3 Where patching is not feasible (vendor end-of-support, safety-regulation prohibition, legacy OS), compensating controls must be documented: tighter segmentation, host-based monitoring, application allow-listing, or removal-from-network where practical.

9.2.4 Vulnerability scanning of OT components must not use active scanning approaches that risk disrupting industrial processes. Passive scanning or vendor-confirmed safe active techniques are mandatory in production OT zones.

### 9.3 Anti-malware

9.3.1 Anti-malware is required on OT hosts where vendor support permits without disrupting safety or control functions.

9.3.2 Where anti-malware is technically infeasible on a host (constrained CPU/memory, vendor restriction), the host must be protected by network-layer detection at the zone boundary and removable-media controls per 9.1.3.

---

## 10. Monitoring, logging, and detection

### 10.1 OT-aware telemetry

10.1.1 OT environments must produce telemetry suitable for security monitoring. Minimum telemetry includes:

- Authentication events on engineering workstations, HMIs, jump hosts.
- Configuration changes on PLCs, controllers, HMIs.
- Network traffic at conduit boundaries (NetFlow or equivalent).
- Process-anomaly indicators where the OT system supports them.
- SIS bypass and force conditions.

10.1.2 OT telemetry must integrate with the central SIEM ([`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md)) either directly or via an OT-specific collection layer that aggregates into the SIEM.

10.1.3 The SOC must have analysts trained in OT-aware monitoring. OT alerts that the SOC cannot resolve within 15 minutes are escalated to the OT Security Lead and, for production-impacting indicators, the Plant Manager.

### 10.2 Time synchronisation

10.2.1 All OT components capable of receiving time synchronisation must be synchronised to a common reliable time source (typically NTP from a hardened internal time server, with the internal server upstream from a verified external source). Clock skew greater than 5 minutes triggers an alert.

10.2.2 Safety-critical components must use a clock source whose disruption cannot cause unsafe behaviour. Where a safety component cannot accept network time, it uses a locally trusted source.

### 10.3 Log retention

10.3.1 OT security logs must be retained for at least 3 years, with longer retention where sector regulation requires it (NERC CIP, sector-specific). Retention is recorded in the records retention standard ([`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)).

10.3.2 Logs from safety systems are retained per the applicable safety regulation, which typically exceeds general security log retention.

---

## 11. Vendor and supplier requirements

### 11.1 Supplier qualification

11.1.1 OT integrators, maintainers, and product vendors are qualified through the supplier due diligence procedure ([`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md)) with the following OT-specific additions:

- Evidence of alignment to IEC 62443-2-4 (security programme requirements for IACS service providers).
- Stated SL-C for products supplied (per section 6.3).
- Documented vulnerability-disclosure process for vendor products.
- Evidence of vendor staff training in OT security relevant to the services provided.

11.1.2 Tier 1 OT vendors (those with direct access to safety-critical or revenue-critical OT zones) require enhanced due diligence including on-site visits where feasible.

### 11.2 Vendor product lifecycle

11.2.1 Vendor product end-of-support dates must be tracked in the OT asset inventory. Assets approaching vendor end-of-support require a refresh plan or a documented exception with compensating controls.

11.2.2 Vendor security patches, firmware updates, and configuration changes received from a vendor must be verified for authenticity (signed updates, hash verification, secure delivery channel) before application.

### 11.3 Vendor contractual requirements

11.3.1 OT vendor contracts must include:

- Right to audit the vendor's security practices.
- Notification timeline for vulnerabilities discovered in supplied products.
- Notification timeline for security incidents at the vendor that may affect supplied products or services.
- Cooperation obligation for incident response at the organisation's facility.
- Return-of-equipment and data-destruction obligations at contract termination.

---

## 12. Safety integration

### 12.1 SIS-BPCS separation

12.1.1 Safety Instrumented Systems (SIS) must be logically and, where feasible, physically separated from Basic Process Control Systems (BPCS). Shared zones containing both SIS and BPCS require explicit safety-engineering and CISO approval.

12.1.2 Network conduits carrying SIS traffic must have SL-T of at least SL 3 (per 6.1.3).

12.1.3 Diagnostic and engineering access to SIS is restricted to the Safety Engineer privilege track (per 7.3.1) and follows safety-management dual-approval requirements.

### 12.2 Safety-related change control

12.2.1 Changes to SIS configuration, logic, or hardware require safety-engineering review in addition to the change-management procedure ([`operations/procedure-change-management-and-configuration-control.md`](../procedure-change-management-and-configuration-control.md)).

12.2.2 Safety-regulation requirements (IEC 61511 management of change clauses) take precedence over the library's general change-management requirements where the safety regulation is more restrictive.

### 12.3 HAZOP and LOPA coordination

12.3.1 Process Hazard Analysis (HAZOP) and Layer of Protection Analysis (LOPA) outputs that identify cyber threats as initiating events must inform the security risk assessment (section 5.3). Cyber-specific consequences must be incorporated into the LOPA.

12.3.2 The OT Security Lead participates in HAZOP and LOPA reviews where cyber considerations are in scope.

---

## 13. Recovery

### 13.1 Backup of OT configuration

13.1.1 PLC logic, HMI configuration, historian databases, SIS configuration, and other OT system configuration must be backed up on a schedule appropriate to the rate of change, at least quarterly.

13.1.2 Backups must be stored offline or in an isolated zone such that a compromise of the production OT zone does not corrupt the backups.

13.1.3 Backup integrity must be verified by periodic restore testing in a representative environment.

### 13.2 Recovery objectives

13.2.1 OT systems have Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) per the resilience standard ([`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md)) with OT-specific RTOs that may extend to days where the cyber incident requires physical-site access, vendor coordination, and safety verification before production resumption.

13.2.2 Recovery from a cyber incident affecting safety-instrumented systems requires safety-engineering verification before the safety function is returned to service.

---

## 14. Audit and assurance

### 14.1 Internal audit

14.1.1 OT zones and conduits are audited per [`compliance/standard-internal-audit.md`](../../compliance/standard-internal-audit.md) with the following OT-specific additions:

- Audit frequency at least annually for zones with SL-T of SL 3 or SL 4.
- Audit frequency at least every 18 months for zones with SL-T of SL 1 or SL 2.
- Audit must include verification of the SL-A measurement and the SL-A-to-SL-T gap.
- Audit must include verification of vendor access logs and quarterly access review records.

### 14.2 Independent verification

14.2.1 Zones with SL-T of SL 3 or SL 4 require independent verification of SL-A at least every three years. Independent verification may be performed by an internal team functionally independent of OT operations or by a qualified third-party assessor.

### 14.3 Continuous improvement

14.3.1 OT incidents and audit findings feed into the CAPA process ([`compliance/procedure-capa.md`](../../compliance/procedure-capa.md)). OT-specific patterns are reviewed annually by the CISO and OT Security Lead to identify systemic improvements.

---

## 15. Framework alignment

| Framework | Reference | Relevance to this standard |
| --- | --- | --- |
| IEC 62443-1-1 | Concepts and models | Section 4 definitions, zone-and-conduit terminology |
| IEC 62443-2-1 | Establishing an IACS security programme | Sections 3 governance, 14 audit |
| IEC 62443-2-4 | Service providers | Section 11 vendor and supplier requirements |
| IEC 62443-3-2 | Security risk assessment for system design | Section 5 architecture and risk assessment |
| IEC 62443-3-3 | System security requirements and security levels | Section 6 security-level achievement |
| IEC 62443-4-1 | Secure product development lifecycle | Section 11.1 supplier qualification |
| IEC 62443-4-2 | Technical security requirements for IACS components | Section 6.3 SL-C; section 9 endpoint hardening |
| NIST SP 800-82 Rev 3 | Guide to Operational Technology (OT) Security | Cross-reference throughout; secondary alignment |
| NIST SP 800-53 Rev 5 | Security and Privacy Controls | Underlying control catalogue (control mappings inherit from main library) |
| ISO/IEC 27001:2022 | ISMS requirements | ISMS scope when extended to OT |
| ISO/IEC 27019:2024 | Information security controls for the energy utility industry | Energy-sector ICS extension |
| IEC 61511 / IEC 61508 | Functional safety | Section 12 safety integration; safety-regulation precedence |
| NERC CIP | Critical Infrastructure Protection | North American electricity sector (see energy-and-utilities annex) |
| NIST SP 800-207 | Zero Trust Architecture | Conceptual alignment for IT/OT convergence layers (Purdue 3.5 and above) |

---

**End of Document**
