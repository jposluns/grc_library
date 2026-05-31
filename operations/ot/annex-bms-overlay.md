# Building Management Systems (BMS) Overlay Annex

**Document Title:** Building Management Systems (BMS) Overlay Annex\
**Document Type:** Annex\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md), [`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md), [`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md), [`operations/ot/register-ot-asset-inventory-and-lifecycle.md`](register-ot-asset-inventory-and-lifecycle.md), [`operations/standard-physical-security-of-it-infrastructure.md`](../standard-physical-security-of-it-infrastructure.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and upon material change to ISO 16484, ASHRAE 135 (BACnet), IEC 62443, or applicable fire and life-safety codes\
**Repository Path:** [`operations/ot/annex-bms-overlay.md`](annex-bms-overlay.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This annex provides BMS-specific security considerations that overlay the OT/ICS Security Standard ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)). BMS are a subset of OT and are governed by that standard; this annex identifies where BMS environments need additional or differentiated controls due to life-safety integration, tenant impact, regulatory authority oversight, and the characteristic vendor and integration patterns of modern smart-building deployments.

The annex does **not** replace the OT/ICS Security Standard for BMS scope. It identifies the deltas. Where the OT/ICS Security Standard is silent or insufficient, this annex provides the BMS-specific position.

---

## 2. Scope

### 2.1 BMS components in scope

- **BMS head-end / supervisor servers**: Niagara, Metasys, EBI, Apogee, Insight, Desigo CC, and equivalent.
- **Direct Digital Controllers (DDC)** and equivalent field controllers.
- **HVAC controllers**: chiller plant, air-handling units (AHUs), variable air volume (VAV) boxes, fan-coil controllers.
- **Lighting control systems**: networked lighting controllers, occupancy sensors, daylight harvesting, emergency lighting interfaces.
- **Access control systems** (physical access): door controllers, badge readers, intrusion detection panels, where cyber-connected and integrated with the BMS.
- **CCTV and video surveillance systems** where integrated with BMS or shared OT network.
- **Fire alarm and life-safety systems** (cyber-connected portions only): fire alarm control panels with network interfaces, smoke management controls, voice evacuation systems. Note: the fire-detection function itself is governed by fire codes; this annex addresses only cyber-connected aspects.
- **Elevator / lift control systems** where cyber-connected (destination dispatch, BMS integration, remote diagnostics).
- **Energy management systems**: building-level meters, submetering, demand-response interfaces.
- **Smart-building gateways**: BMS-to-cloud connectors, IoT aggregators, occupancy analytics platforms.

### 2.2 Out of scope

- Stand-alone fire detection and suppression devices not network-connected; these are governed entirely by fire codes and the Authority Having Jurisdiction (AHJ).
- Pure facilities management software with no controller interface (facility-management ticketing, work-order systems).
- Tenant-owned in-suite equipment unless integrated with the landlord BMS.

### 2.3 Boundary cases

- **Mixed-use buildings** (residential, commercial, industrial): BMS scope follows the operational function; industrial-process control is governed by the OT/ICS Security Standard without this overlay.
- **Data centre BMS** (cooling, power, environmental monitoring): in scope; the BMS controls supporting the data centre are themselves OT and are subject to both this annex and the physical-infrastructure standards.
- **Co-managed buildings** (managed by a third-party facilities operator): the contractual responsibility split is recorded in the asset inventory; security accountability is determined per the supplier due-diligence procedure.

---

## 3. Why BMS differs from process-control OT

BMS share OT characteristics (physical-world impact, long lifecycles, availability priority) but differ from process-control OT in operationally significant ways:

| Dimension | Process-control OT | BMS |
| --- | --- | --- |
| Ownership | IT/OT or engineering function | Often facilities management, not IT |
| Vendor pattern | Few primary control vendors per site | Multi-vendor: HVAC, lighting, fire, access, often per subsystem |
| Protocols | Process protocols (Modbus, EtherNet/IP, Profinet, DNP3) | Building protocols (BACnet, LON, KNX, M-Bus, Modbus) |
| Life-safety integration | SIS is typically separated from process control | Fire and life-safety often share network with comfort BMS |
| Regulatory authority | Process safety regulators, energy regulators | Authority Having Jurisdiction (AHJ) for fire, building codes, accessibility |
| Data sensitivity | Process data | Occupancy, badge, presence, and tenant data: privacy-relevant |
| IT/OT convergence | Increasing but typically managed | Most pronounced (smart-building IoT, cloud analytics) |
| Patching cadence | Production windows, vendor-coordinated | Often deferred indefinitely; tenant-impact constrained |

These differences shape the overlay controls in this annex.

---

## 4. Life-safety integration

The dominant concern in BMS security is that controls and incident response must not interfere with the operation or response time of life-safety functions (fire detection, alarm, evacuation, smoke management, refuge areas, emergency lighting).

### 4.1 Non-interference principle

- Cyber controls must be designed so that under any failure or attack condition, life-safety functions continue to operate or fail to a safe state per the fire code design.
- Containment actions (network isolation, credential revocation, system shutdown) that could affect fire alarm transmission, evacuation signalling, or emergency lighting are not permitted without explicit authorisation from facilities management and, where required, the AHJ.
- The incident response procedure ([`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md)) is extended for BMS incidents: any containment action affecting fire or life-safety systems requires Facilities Manager and (where local regulations require) AHJ notification.

### 4.2 Fire system integration constraints

- Cyber-connected portions of fire alarm systems are typically required by code to be listed and tested as a system. Changes (including patches) may invalidate listing or require AHJ re-acceptance.
- Patch and change governance for fire-system network interfaces follows the OT Change Management Procedure with the addition: any change affecting code-listed equipment requires written approval from the fire system vendor and, where required, AHJ notice or re-acceptance.
- Network segmentation must preserve the fire system's required communication paths (panel-to-monitoring-centre, panel-to-evacuation, panel-to-smoke-management).

### 4.3 Emergency operation override

- BMS must have a documented emergency-operation mode that overrides routine cyber controls (for example, badge-reader fail-safe behaviour during evacuation) and is exercised under the Business Continuity Plan.
- The override mechanism is a tracked asset; its integrity is verified during the annual continuity exercise.

---

## 5. Authority Having Jurisdiction (AHJ) coordination

In many jurisdictions, the AHJ has approval authority over fire-system and life-safety changes. The library does not displace AHJ authority.

- The OT Change Management Procedure ([`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md)) is extended for BMS scope: change records for AHJ-regulated equipment must capture AHJ notification or approval status.
- Cyber-security-driven changes to AHJ-regulated systems are not "Standard" changes; they are at minimum Normal, and typically Safety-related, in the change category model.
- AHJ contact information and notification routes are maintained in the supplier and regulator contact register of the relevant resilience plan.

---

## 6. BMS protocol governance

BMS protocols carry historical assumptions of trusted networks. The OT/ICS Security Standard §8.2 (Protocol governance) applies; this annex adds BMS-specific protocol guidance.

### 6.1 BACnet (ASHRAE 135)

- BACnet/IP carries no authentication or integrity protection in its base form. Where used, segmentation and conduit controls per IEC 62443-3-2 are mandatory.
- **BACnet/SC** (Secure Connect, ASHRAE 135-2020 Addendum) provides TLS-based authentication and integrity for BACnet. Where BACnet is used and BACnet/SC is supported by the deployed equipment, BACnet/SC must be enabled and BACnet/IP-without-SC disabled across the conduit.
- BACnet broadcast distribution beyond the BMS zone is prohibited.

### 6.2 LON (LonWorks / LonTalk)

- LON has limited native security. Where used, segmentation is mandatory and protocol-aware filtering at conduit boundaries is required.

### 6.3 KNX

- KNX/IP in its base form is unauthenticated. KNX Secure (KNX/IP Secure, KNX Data Secure) provides authentication and integrity; where supported, it must be enabled.

### 6.4 Modbus in BMS

- Modbus RTU and Modbus TCP frequently appear in BMS contexts (chiller plants, energy meters). Modbus protocol governance per the OT/ICS Security Standard applies without modification.

### 6.5 Proprietary vendor protocols

- Vendor-proprietary protocols are documented in the asset inventory with whatever security properties the vendor publishes. Where the vendor publishes no security properties, the protocol is treated as unauthenticated.

---

## 7. Multi-vendor coordination

BMS deployments are routinely multi-vendor: a primary BMS supplier integrates HVAC, lighting, fire, access, and metering subsystems supplied by other vendors. Security responsibility must be unambiguous.

- The asset inventory records the primary vendor and the integrator for every BMS asset.
- Security responsibility for each subsystem is captured in the supplier register and supplier contract.
- Vendor remote access is governed by the OT/ICS Security Standard §7.4 without exception; each vendor has separate remote-access credentials, sessions, and audit trails.
- Coordinated changes (a patch to one subsystem that requires concurrent change in another) are managed through the OT Change Management Procedure with all affected vendors as participants.

---

## 8. Tenant and occupancy data

BMS routinely capture data that is privacy-relevant: badge events, presence sensing, occupancy heatmaps, in-suite environmental readings, energy consumption per tenant.

- Where personal data is captured (badge identifiers tied to identifiable individuals, video footage, individual presence), the privacy policy ([`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md)) applies and the BMS deployment must be reflected in the records-of-processing inventory.
- Data minimisation is preferred: presence aggregation at floor or zone level is preferred over per-desk per-person tracking, unless a documented purpose requires the finer granularity.
- Retention of presence, occupancy, and badge-event data is recorded in the data-retention schedule with a retention period justified by purpose.
- Where the BMS exports data to a vendor cloud (analytics, fault detection, energy optimisation), the cloud transfer is treated as a third-party data transfer with the supplier due-diligence procedure applied and contractual data-processing terms in place.

---

## 9. Smart-building cloud integration

Modern BMS frequently extend into vendor cloud services for analytics, predictive maintenance, fault detection, and energy optimisation.

- The cloud integration is recorded in the asset inventory as a conduit per IEC 62443-3-2.
- Cloud integration must terminate in the OT DMZ (Purdue level 3.5), not directly in OT zones.
- The vendor cloud is subject to the supplier due-diligence procedure including cloud security configuration baseline applicability.
- Data flowing to the cloud is subject to the data-classification and privacy controls.
- Vendor remote access via the cloud is treated as remote access under the OT/ICS Security Standard §7.4: explicit authorisation per session, audit trail, time-bounded.

---

## 10. Asset, change, and incident overlay specifics

This annex does not duplicate the relevant standard, procedure, or register; it identifies the BMS-specific positions that those documents either invoke or accommodate.

### 10.1 Asset inventory overlay

The asset record schema in the OT Asset Inventory and Lifecycle Register applies to BMS without modification. The following fields carry BMS-specific interpretation:

- **Operational Criticality Tier**: BMS controllers for life-safety integration are OT-1; comfort BMS without life-safety integration may be OT-2 or OT-3 per impact analysis; smart-building peripheral devices (occupancy sensors, environmental sensors) are typically OT-4.
- **Safety Class**: BMS controllers integrated with fire or life-safety functions are S-B (safety-adjacent) at minimum; controllers that are part of an engineered life-safety function are S-A; comfort-only BMS without life-safety integration are S-C.
- **Maintenance Contract**: the AHJ-listing or code-acceptance state, where applicable, is recorded alongside the maintenance contract.

### 10.2 Change-management overlay

- BMS changes affecting fire or life-safety systems are Safety-related per the OT Change Management Procedure §5.5 and are subject to AHJ coordination per §5 of this annex.
- BMS changes affecting tenant-impacting functions (HVAC during occupied hours, lighting in occupied spaces, access control during business hours) are scheduled per tenant communication agreements; outside-tenant-hours scheduling is preferred.
- Vendor-driven changes to BMS subsystems are common; the Vendor Liaison role applies per the OT Change Management Procedure.

### 10.3 Incident response overlay

- BMS incidents potentially affecting fire or life-safety systems are P1 by default in the OT Incident Response Procedure severity model. Containment must not interfere with life-safety function operation; see §4 of this annex.
- Notification routes include the Facilities Manager and, where local regulations require, the AHJ.
- Forensics on AHJ-regulated equipment may require AHJ presence or notification; this is captured in the incident communications plan.

---

## 11. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443 family | OT security baseline | BMS is OT; the full family applies. |
| NIST SP 800-82 Rev 3 | OT security guide | Aligned. |
| ISO 16484-1 to -7 | Building Automation and Control Systems (BACS) | BMS engineering and integration standard. |
| ASHRAE 135 (BACnet) | BACnet protocol | Including BACnet/SC for secure BACnet. |
| NIST SP 1900 series | Smart Buildings | Smart-building IoT considerations. |
| NFPA 72 | National Fire Alarm and Signaling Code | Fire alarm system integration constraints (US context; equivalent codes elsewhere). |
| EN 54 series | Fire detection and fire alarm systems | European fire alarm equipment standards. |
| ISO/IEC 27001:2022 | A.5.9, A.8.32 | Asset inventory and change management. |
| ISO/IEC 27018 / 27701 | Privacy in cloud / privacy information management | Tenant and occupancy data where transferred to cloud or processed at scale. |
| GDPR / UK GDPR / CCPA | Privacy regulation | Where personal data (badge events, identifiable presence) is processed. |
| Applicable building codes | Jurisdiction-specific | Listing and acceptance constraints on fire and life-safety. |

---

## 12. Cross-reference summary

- **OT/ICS Security Standard** ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)): the baseline this annex overlays.
- **OT Change Management Procedure** ([`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md)): extended by §5 (AHJ coordination) and §10.2 of this annex.
- **OT Incident Response Procedure** ([`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md)): extended by §4 (non-interference) and §10.3 of this annex.
- **OT Asset Inventory and Lifecycle Register** ([`operations/ot/register-ot-asset-inventory-and-lifecycle.md`](register-ot-asset-inventory-and-lifecycle.md)): BMS-specific interpretation of fields per §10.1.
- **Privacy Policy** ([`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md)): applies to tenant and occupancy data.
- **Supplier Due Diligence** ([`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md)): applies to BMS vendor and cloud integration.
- **Physical Security Standard** ([`operations/standard-physical-security-of-it-infrastructure.md`](../standard-physical-security-of-it-infrastructure.md)): boundary with physical access control where the BMS hosts access control.

---

**End of Document**
