# OT Asset Inventory and Lifecycle Register

**Document Title:** OT Asset Inventory and Lifecycle Register\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md), [`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md), [`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md), [`operations/register-asset-inventory.md`](../register-asset-inventory.md), [`operations/procedure-patch-management.md`](../procedure-patch-management.md), [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and upon material change to IEC 62443-2-1, NIST SP 800-82 Rev 3, or material change to OT estate composition\
**Repository Path:** [`operations/ot/register-ot-asset-inventory-and-lifecycle.md`](register-ot-asset-inventory-and-lifecycle.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## 1. Purpose

This register defines the schema, governance, classification, and lifecycle model for the organisation's Operational Technology (OT) asset inventory. The OT asset inventory is the authoritative record of all OT hardware, firmware, software, network components, and supporting infrastructure within scope of the OT/ICS Security Standard ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)).

The OT inventory supplements (and where conflict arises, supersedes for OT scope) the general operations asset inventory ([`operations/register-asset-inventory.md`](../register-asset-inventory.md)). OT assets carry attributes (zone membership, Security Level Capability, vendor support state, safety relevance, control-loop role) that the general schema does not represent.

This register is the foundation for OT zone-and-conduit governance, vulnerability management, patching cadence, vendor end-of-support tracking, and OT incident response triage. Without an accurate OT inventory the controls in the OT/ICS Security Standard cannot be enforced or audited.

---

## 2. Scope

### 2.1 Assets in scope

- **Control assets**: PLCs, RTUs, DCS controllers, safety controllers, intelligent electronic devices (IEDs), variable-frequency drives with network interfaces, motor controllers, instrument controllers.
- **Supervisory and HMI assets**: SCADA servers, HMIs, engineering workstations, operator consoles, historian servers, alarm servers, batch servers.
- **Safety Instrumented System (SIS) assets**: logic solvers, safety I/O modules, safety-rated PLCs, partial-stroke testing devices, fire and gas controllers.
- **OT network assets**: industrial switches, routers, firewalls between zones, OT-aware deep-packet inspection sensors, jump hosts, OT-DMZ servers.
- **OT software**: firmware images, PLC programs, HMI projects, SCADA configurations, historian schemas, engineering software licences.
- **Field devices with network interfaces**: smart sensors, smart transmitters, wireless field instruments, asset-management gateways.
- **Building Management System (BMS) assets**: BMS controllers, HVAC controllers, access-control panels, fire-life-safety panels (cyber-relevant portions), lighting controllers, smart-building gateways.
- **Vendor-managed assets in OT zones**: any device installed and operated under vendor maintenance contract that resides in or communicates with an OT zone.

### 2.2 Assets out of scope

- Pure IT assets in business networks not communicating with OT zones (covered by [`operations/register-asset-inventory.md`](../register-asset-inventory.md)).
- Medical devices governed by medical device regulations (MDR/IVDR); these are tracked in healthcare-sector inventories.
- Generic office equipment colocated in plant offices but not connected to OT networks.

### 2.3 Boundary cases

- **Engineering workstations domain-joined to corporate Active Directory**: in scope of this register because they connect to OT zones; identity controls follow the general identity standard with OT-specific overlay.
- **Cloud-hosted historians and analytics**: in scope; the OT zone they receive data from is recorded as their source, and the cloud-hosting relationship is recorded as a conduit (per IEC 62443-3-2).
- **Vendor remote-access infrastructure**: in scope where it terminates inside an OT zone; out of scope where it terminates only in the OT DMZ.

---

## 3. Roles and accountability

| Role | Accountability |
| --- | --- |
| Chief Information Security Officer | Owns this register and the OT inventory completeness. |
| OT Security Lead | Day-to-day inventory maintenance, reconciliation, and accuracy. |
| Plant Manager (per site) | Site-level inventory accuracy and approval of plant-side asset entries. |
| Process Safety Engineer | Validates safety-relevant tagging (SIS, safety functions, interlocks). |
| Control System Engineer | Provides technical inventory data for controllers, HMIs, and engineering workstations. |
| Vendor Liaison | Maintains vendor-support state, end-of-support tracking, and vendor-managed asset records. |
| Internal Audit | Periodically tests inventory accuracy against the field. |
| IT Operations (Asset Management) | Reconciles OT inventory with general asset inventory to avoid gaps and duplicates. |

---

## 4. Inventory governance principles

- **Authoritative by design**: this register and the records it governs are the authoritative source for OT-asset-related decisions in change, vulnerability, incident, and patch management.
- **Field-truth reconciliation**: the inventory must reflect what is physically present in the field. Documented assets without field presence and field assets without documented record are equally defects.
- **Passive discovery preferred**: discovery on OT networks uses passive monitoring (span ports, network taps, OT-aware sensors). Active scanning is restricted to assets and zones where the asset vendor has confirmed it as safe.
- **Long lifecycles acknowledged**: 15-25 year operating lifetimes are the norm. End-of-support is treated as a managed state, not a defect requiring immediate replacement.
- **Safety attributes are first-class**: the safety relevance of every asset is a tracked attribute, not derived information.
- **No silent assets**: an asset that cannot be attributed to a zone, owner, and lifecycle state is treated as unauthorized pending resolution.

---

## 5. OT asset classification

OT assets are classified along three independent dimensions: operational criticality, safety relevance, and zone trust level. Vulnerability prioritisation, patching cadence, and change rigour are derived from the combination.

### 5.1 Operational criticality

| Tier | Description | Examples |
| --- | --- | --- |
| OT-1 (Critical control) | Direct control of physical processes whose failure halts production or causes physical damage. | DCS controllers for primary process loops, PLCs governing safety-critical interlocks, primary SCADA. |
| OT-2 (Essential supervisory) | Supervisory or auxiliary control whose failure causes production degradation within hours. | HMIs, historian servers, alarm management, engineering workstations. |
| OT-3 (Supporting) | Auxiliary systems whose failure does not immediately halt or degrade production. | BMS for non-critical building functions, secondary historians, reporting servers. |
| OT-4 (Peripheral) | Indirect OT-connected systems whose failure has minimal operational impact. | Smart-building lighting, comfort HVAC, asset-tracking gateways. |

### 5.2 Safety relevance

| Class | Description |
| --- | --- |
| S-A (Safety-Instrumented) | Asset is part of a Safety Instrumented System under IEC 61511. |
| S-B (Safety-Adjacent) | Asset is not part of an SIS but a failure or compromise could defeat or bypass a safety function. |
| S-C (Safety-Independent) | Asset is independent of safety functions; no credible path to a safety event. |

### 5.3 Zone trust level

Aligned to the Security Level Target (SL-T) assigned to the zone hosting the asset, per the OT/ICS Security Standard §6.1. Records `SL-T 1` to `SL-T 4` and the corresponding Security Level Capability (SL-C) of the asset itself.

---

## 6. OT asset record schema

Every OT asset has a record with the following fields. Fields are grouped for clarity; the implementation may store them in any structure that preserves attribute integrity.

### 6.1 Identification

| Field | Description |
| --- | --- |
| OT Asset ID | Unique identifier within the OT inventory (distinct from general IT inventory ID). |
| Asset Name | Descriptive name. |
| Vendor Tag / Serial | Vendor-assigned tag, serial number, or model identifier. |
| Asset Type | Controller / HMI / Engineering Workstation / Historian / SCADA Server / Safety Logic Solver / Field Device / OT Network Device / OT-DMZ Server / BMS Component / Other. |
| Make and Model | Manufacturer and model number. |
| Firmware Version | Current firmware or operating-system version. |
| Application Version | Vendor application or runtime version (where distinct from firmware). |

### 6.2 Location and zone

| Field | Description |
| --- | --- |
| Site | Plant, facility, or installation. |
| Physical Location | Building, room, cabinet, or rack identifier. |
| OT Zone | Zone identifier per IEC 62443-3-2 (linked to zone-and-conduit register). |
| Purdue Level | Level 0 / 1 / 2 / 3 / 3.5 (OT-DMZ) / 4 / 5. |
| IP Address(es) | Routable and non-routable addresses on OT networks. |
| Network Interfaces | Quantity, type (Ethernet, serial, wireless), protocols. |

### 6.3 Classification

| Field | Description |
| --- | --- |
| Operational Criticality Tier | OT-1 / OT-2 / OT-3 / OT-4 (per §5.1). |
| Safety Class | S-A / S-B / S-C (per §5.2). |
| Zone SL-T | Security Level Target of zone. |
| Asset SL-C | Security Level Capability of asset. |
| Data Classification | Classification of process data the asset handles. |

### 6.4 Ownership and operation

| Field | Description |
| --- | --- |
| Asset Owner (Role) | Role title accountable for the asset. |
| Custodian | Team or role operationally responsible. |
| Vendor / Integrator | Supplier or systems integrator. |
| Maintenance Contract | Contract identifier, scope, and counterparty. |
| Vendor-Managed | Yes / No. If Yes, vendor-management terms recorded. |

### 6.5 Lifecycle

| Field | Description |
| --- | --- |
| Lifecycle State | Planned / Commissioning / Active / End-of-Support / Decommissioning / Decommissioned (per §7). |
| In-Service Date | Date placed into production. |
| Vendor End-of-Support Date | Vendor-published date or "Unknown" (recorded as a tracked gap). |
| Internal End-of-Support Date | Date at which the organisation plans to retire the asset, if different. |
| Decommission Date | Date removed from service, where applicable. |

### 6.6 Security state

| Field | Description |
| --- | --- |
| Patch State | Current patch level or firmware version and date applied. |
| Last Vulnerability Assessment | Date of most recent vulnerability assessment relevant to this asset. |
| Known CVEs | Identifiers of known unpatched vulnerabilities with risk-acceptance reference. |
| Compensating Controls | Where vulnerabilities cannot be remediated, the compensating controls in force. |
| Configuration Baseline | Reference to current configuration baseline (per change procedure §6). |
| Last Change | Reference to most recent OT change record. |

### 6.7 Backup and recovery

| Field | Description |
| --- | --- |
| Configuration Backup | Status, last backup date, location of backup. |
| Firmware Backup | Status, last backup date, location of backup (for assets supporting firmware extraction). |
| Recovery Time Objective | From OT business-impact analysis. |
| Recovery Point Objective | From OT business-impact analysis. |
| Disaster-Recovery Tier | Linked to IT DR plan tier where applicable. |

### 6.8 Administrative

| Field | Description |
| --- | --- |
| Date Added | Date of inventory entry. |
| Last Reviewed | Date of most recent manual validation. |
| Source | Discovery method (manual entry, passive discovery, vendor import, commissioning record). |
| Notes | Free-text notes capturing material context (legacy OS, known constraints, exception references). |

---

## 7. Lifecycle states

OT lifecycle differs from IT lifecycle in two respects: lifetimes are longer (15-25 years versus 3-7 years), and end-of-support is a managed state rather than a defect.

### 7.1 State definitions

| State | Definition | Required action |
| --- | --- | --- |
| Planned | Asset is procured or specified but not yet on site. | Pre-commissioning security review per OT/ICS Security Standard. |
| Commissioning | Asset installed and undergoing factory acceptance test (FAT), site acceptance test (SAT), and initial configuration. | Acceptance into service review; baseline established. |
| Active | Asset operating in production. | Routine controls per OT/ICS Security Standard. |
| End-of-Support | Vendor support has ended or is announced to end within the planning horizon. | Documented exception with compensating controls; refresh plan recorded; risk-register entry. |
| Decommissioning | Asset is being removed from service. | Secure decommissioning per §8.4. |
| Decommissioned | Asset removed from service; record retained for audit. | Retention per §9. |

### 7.2 End-of-support handling

OT vendors routinely end support for control systems while the systems remain operational and economically valuable for years afterwards. Replacement may be capital-intensive and operationally disruptive. The library does not require immediate replacement on end-of-support; it requires the state to be tracked and risk-managed.

When an asset enters End-of-Support state:

- The vendor end-of-support date is recorded with citation to vendor announcement.
- A compensating-controls package is documented: heightened segmentation, additional monitoring, restricted change scope, restricted remote access, hardened backup posture.
- A risk-register entry is opened against the asset or asset class.
- A refresh plan is recorded with target timeline; absence of plan is itself a tracked finding.
- Vendor end-of-support state does not trigger automatic change of operational criticality or safety classification; those remain as they are.

### 7.3 Legacy operating-system handling

OT assets routinely run unsupported operating systems (legacy Windows versions, vendor-proprietary OSes, real-time kernels with limited update channels). Where the OS is end-of-life but the asset must remain in service:

- The unsupported OS is recorded explicitly in the asset record.
- Network exposure is minimized through segmentation and conduit restrictions.
- Anti-malware controls compatible with OT availability requirements are applied (allowlisting preferred over signature-based AV where allowlisting is supported).
- Removable media controls are tightened per the OT/ICS Security Standard.
- The asset is monitored under heightened scrutiny by OT-aware detection.
- Where vendor extended-support contracts are available, their state is tracked.

---

## 8. Inventory operations

### 8.1 Discovery

- **Passive discovery**: OT-aware network sensors observe traffic in OT zones and identify assets by protocol fingerprint, MAC address, vendor identifier, and behavioural pattern. Passive discovery is the default for live OT networks.
- **Active scanning**: permitted only where the asset vendor has confirmed scanning safety, the scanning tool is OT-aware, and the scan is scheduled within an approved change window. Active scanning of safety-instrumented systems is generally prohibited; exceptions require Process Safety Engineer approval.
- **Vendor data import**: vendor asset-management platforms (engineering software, vendor cloud portals) are integrated where available. Imports are reconciled, not trusted.
- **Manual entry**: commissioning data is captured manually at site acceptance test. Field walkdowns are conducted where automated discovery is incomplete or unsafe.

### 8.2 Reconciliation

- Inventory records are reconciled against discovery results monthly for OT-1 and OT-2 assets, quarterly for OT-3 and OT-4 assets.
- Discrepancies (asset in field but not in inventory, asset in inventory but not in field, mismatched firmware version, mismatched zone) are logged and resolved.
- Material reconciliation findings escalate to the OT Security Lead and (for safety-relevant assets) the Process Safety Engineer.

### 8.3 Unauthorized assets

- Assets discovered in OT zones that are not in the inventory are treated as potentially unauthorized.
- Network-level isolation is applied where it can be done without affecting production safety; isolation that risks safety requires Process Safety Engineer approval.
- Investigation determines whether the asset is approved (and must be registered), in error (vendor-installed test equipment left behind, for example), or unauthorized (and must be removed under controlled conditions).
- Unauthorized-asset incidents are linked to the OT incident response procedure.

### 8.4 Secure decommissioning

OT-asset decommissioning is more constrained than IT-asset decommissioning. Physical removal often occurs during plant turnaround. Data sanitisation considerations are limited (most OT components store configuration rather than personal or sensitive data), but configuration extraction for forensic and operational continuity is critical.

Decommissioning steps:

1. Final configuration backup retained per retention policy.
2. Credentials and certificates revoked.
3. Network membership removed; firewall and switch configurations updated.
4. Physical asset removed; storage components sanitised or destroyed per the media handling procedure.
5. Inventory record transitioned to Decommissioned state with date.
6. Zone and conduit records updated to reflect topology change.

---

## 9. Retention

| Record state | Retention period |
| --- | --- |
| Active asset records | While in service. |
| Decommissioned asset records | Minimum 7 years from decommission, or longer where regulatory or warranty obligations require. |
| Configuration baselines | Two prior baselines retained while asset is active; final baseline retained per Decommissioned record retention. |
| Discovery and reconciliation logs | Minimum 3 years. |

Sector regulation may extend retention (NERC CIP, EU NIS 2, certain pipeline and water-utility regimes). Sector-specific retention overrides the library default upward, never downward.

---

## 10. Metrics

| Metric | Definition | Indicative target |
| --- | --- | --- |
| Inventory coverage | Percentage of discovered OT assets present in inventory. | At or above 98% on monthly reconciliation. |
| Inventory accuracy | Percentage of inventory records validated against field within review cadence. | At or above 95%. |
| End-of-support assets without refresh plan | Count of assets in End-of-Support state without a documented refresh plan or compensating-controls package. | Zero. |
| Unauthorized-asset detection-to-resolution | Median time from unauthorized-asset detection to resolution (registered, removed, or accepted with risk entry). | Within 10 business days. |
| Legacy-OS asset coverage | Percentage of legacy-OS OT assets with compensating-controls package documented. | 100%. |
| Backup currency | Percentage of OT-1 and OT-2 assets with configuration backup within target age. | 100% within target age per asset type. |

Metric definitions feed into the IT Operations KPI register ([`operations/register-it-operations-kpis.md`](../register-it-operations-kpis.md)) and the OT Security Lead's reporting to the CISO and Plant Manager.

---

## 11. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443-2-1 | IACS security programme: asset identification | Inventory programme element. |
| IEC 62443-3-2 | Zone and conduit definition | Zone membership is an asset attribute. |
| IEC 62443-3-3 | System security requirements | Asset SL-C tracking. |
| NIST SP 800-82 Rev 3 | OT security guide: inventory and asset management | Aligned. |
| ISO/IEC 27001:2022 | Annex A.5.9 Inventory of information and other assets | Aligned, extended for OT. |
| ISO/IEC 27019:2017 | Energy utility extensions | Sector overlay where applicable. |
| NERC CIP-002 | BES Cyber System categorisation | North American electricity sector. |
| NERC CIP-010 | Configuration change management and vulnerability assessments | Configuration baseline tracking. |
| IEC 61511 | Functional safety - process sector | Safety classification field. |
| EU NIS 2 | Essential and important entity obligations | Inventory underpins risk management and incident reporting obligations. |
| TSA Pipeline Security Directive | Asset inventory requirement | US pipeline sector. |

---

## 12. Cross-reference summary

- **OT/ICS Security Standard** ([`operations/ot/standard-ot-ics-security.md`](standard-ot-ics-security.md)): defines control requirements; this register defines the inventory on which those controls operate.
- **OT Change Management Procedure** ([`operations/ot/procedure-ot-change-management.md`](procedure-ot-change-management.md)): change records reference asset records; configuration baselines are maintained per asset.
- **OT Incident Response Procedure** ([`operations/ot/procedure-ot-incident-response.md`](procedure-ot-incident-response.md)): triage and containment depend on accurate zone and asset records.
- **General asset inventory** ([`operations/register-asset-inventory.md`](../register-asset-inventory.md)): non-OT scope; reconciliation prevents duplication and gaps.
- **Patch Management Procedure** ([`operations/procedure-patch-management.md`](../procedure-patch-management.md)): OT patch decisions reference asset state, SL-C, and vendor support state.
- **Vulnerability Management Procedure** ([`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md)): OT vulnerability handling references asset criticality and safety class.
- **Supplier Due Diligence** ([`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md)): vendor-managed asset records integrate with supplier records.
- **IT Disaster Recovery Plan** ([`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md)): OT DR tiering is recorded as an asset attribute.

---

**End of Document**
