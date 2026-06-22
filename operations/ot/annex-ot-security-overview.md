# Operational Technology Security Overview Annex

**Document Title:** Operational Technology Security Overview Annex\
**Document Type:** Annex\
**Version:** 1.0.2\
**Date:** 2026-06-22\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/ot/README.md`](README.md), [`operations/README.md`](../README.md), [`operations/standard-network-security-and-segmentation.md`](../standard-network-security-and-segmentation.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](../../compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](../../compliance/logistics/annex-logistics-sector-requirements.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`governance/register-glossary.md`](../../governance/register-glossary.md)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and upon material change to IEC 62443 or NIST SP 800-82\
**Repository Path:** [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This annex provides the conceptual foundation for the library's Operational Technology (OT) security content. It defines OT scope, distinguishes OT from IT, introduces the dominant reference frameworks (IEC 62443 and NIST SP 800-82), and explains the zone-and-conduit model that underpins OT network architecture.

The annex is the **first read** for any adopter operating OT environments. The standards, procedures, and registers in this sub-directory build on the concepts defined here.

---

## 2. Scope and definitions

### 2.1 What OT is

**Operational Technology (OT)** is hardware and software that detects or causes change through the direct monitoring or control of physical devices, processes, and events. OT covers:

- **Industrial Control Systems (ICS)**: SCADA, Distributed Control Systems (DCS), Programmable Logic Controllers (PLCs), Human-Machine Interfaces (HMI), and engineering workstations.
- **Safety Instrumented Systems (SIS)**: separate systems that bring a process to a safe state on detection of hazardous conditions, governed by IEC 61511 / IEC 61508 and rated by Safety Integrity Level (SIL 1 to SIL 4).
- **Building Management Systems (BMS)**: HVAC, lighting, fire/life-safety, physical access control, and smart-building infrastructure.
- **Transportation control systems**: rail signalling, port and terminal automation, air traffic management adjacents.
- **Connected devices in physical processes**: IIoT (Industrial Internet of Things) sensors and actuators where they participate in OT control loops.

OT excludes pure information systems (databases, document management, email, business analytics) that do not interact with physical processes.

### 2.2 OT versus IT: the three critical differences

| Dimension | IT (typical) | OT (typical) |
| --- | --- | --- |
| **Failure consequence** | Data loss, service downtime, financial loss | Physical damage, environmental harm, loss of life |
| **CIA prioritisation** | Confidentiality, Integrity, Availability (in order) | Availability, Integrity, Confidentiality (reversed) |
| **Asset lifecycle** | 3 to 7 years; patched monthly | 15 to 25 years; often unpatchable; legacy OS |
| **Patching cadence** | Monthly, automated | Annual at most, requires production window, vendor coordination |
| **Network model** | Open, internet-connected, dynamic | Segmented, often air-gapped historically (less so now with IT/OT convergence) |
| **Change tolerance** | Frequent deployments accepted | Change is risk; extensive testing and approval required |
| **Default trust** | Zero trust target; assume breach | Trust within segmented zones; control at boundaries |
| **Real-time constraints** | Latency tolerance varies | Deterministic real-time often required; security overhead constrained |

These differences are not absolute; modern OT increasingly resembles IT in connectivity and architecture (IT/OT convergence). But the operational consequences of OT failures keep the prioritisation distinct.

### 2.3 What this annex does not cover

- **Pure IT controls**: the universal baseline in the main library applies. This annex covers OT-specific overlays only.
- **Medical-device security**: covered under healthcare-sector compliance (MDR/IVDR). OT-adjacent but governed by different regulatory frameworks.
- **Vehicle-embedded systems**: outside current library scope.
- **Sector-specific regulations**: covered in the relevant sector annex (energy-and-utilities, logistics, telecommunications).

---

## 3. Primary reference frameworks

### 3.1 IEC 62443

IEC 62443 (formerly ISA-99) is the international standard family for industrial automation and control system security. It is the dominant reference for OT security globally.

Key parts cited in this annex:

| Part | Scope |
| --- | --- |
| **62443-1-1** | Concepts and models. Foundational vocabulary including zones, conduits, security levels. |
| **62443-2-1** | Establishing an IACS security programme. The "ISMS for OT" specification. |
| **62443-2-4** | Security programme requirements for IACS service providers (integrators, maintainers). |
| **62443-3-2** | Security risk assessment for system design. The zone-and-conduit risk assessment methodology. |
| **62443-3-3** | System security requirements and security levels (SL 1 to SL 4). |
| **62443-4-1** | Secure product development lifecycle requirements (for vendors). |
| **62443-4-2** | Technical security requirements for IACS components (for vendors and integrators). |

### 3.2 NIST SP 800-82 Rev. 3

NIST Special Publication 800-82 Rev. 3 (September 2023) is "Guide to Operational Technology (OT) Security". Rev. 3 was renamed from "Guide to Industrial Control Systems (ICS) Security" to reflect the broader OT scope.

NIST SP 800-82 Rev. 3 is non-binding guidance but widely adopted in US federal and US-regulated industries. It maps OT controls to NIST SP 800-53 Rev. 5 (the general security and privacy control catalogue) with OT-specific tailoring.

The library uses IEC 62443 as the primary alignment and NIST SP 800-82 Rev. 3 as the secondary alignment.

### 3.3 IEC 61511 / IEC 61508 (functional safety)

These standards govern Safety Instrumented Systems (SIS). They define Safety Integrity Levels (SIL 1 through SIL 4) measuring the reliability of safety functions. The library treats SIS security as a sub-topic of OT security with explicit acknowledgement that safety regulations (not security regulations) are the dominant constraint on SIS modifications.

### 3.4 NERC CIP (North American electricity sector)

NERC CIP Critical Infrastructure Protection standards apply to the North American Bulk Electric System. They are sector-specific (energy) and jurisdiction-specific (US, Canada, parts of Mexico). Detailed coverage lives in [`compliance/energy-and-utilities/`](../../compliance/energy-and-utilities/); this OT annex provides only cross-reference acknowledgement.

---

## 4. The zone-and-conduit model

The IEC 62443 zone-and-conduit model is the foundation of OT network architecture. Adopters must understand it before applying any of the standards, procedures, or registers in this sub-directory.

### 4.1 Zones

A **zone** is a grouping of physical or logical assets that share security requirements. Zones are bounded by their security requirement, not by network topology. A zone has:

- An owner (a person or role accountable for the zone's security state).
- A defined set of assets (devices, systems, software, people, processes).
- A risk assessment that produces a Security Level Target (SL-T).
- A security policy specifying what is permitted within the zone and at its boundary.

### 4.2 Conduits

A **conduit** is a logical grouping of communication channels that connect two or more zones. Conduits carry traffic between zones; they are the security control points where zone-to-zone communication is permitted, monitored, and authenticated. A conduit has:

- An owner.
- A defined set of communication channels (network protocols, ports, application messages).
- A risk assessment that produces a Security Level Target (SL-T) appropriate to the traffic it carries.
- A security policy specifying what traffic is permitted, encrypted, authenticated, and logged.

### 4.3 Security Levels (SL)

IEC 62443 defines four security levels matching the sophistication of the threat that the zone or conduit's security must withstand:

| Level | Protection against |
| --- | --- |
| **SL 1** | Casual or coincidental violation. |
| **SL 2** | Intentional violation by simple means, low resources, generic skills, low motivation. |
| **SL 3** | Intentional violation by sophisticated means, moderate resources, IACS-specific skills, moderate motivation. |
| **SL 4** | Intentional violation by sophisticated means, extended resources, IACS-specific skills, high motivation (nation-state-grade adversaries). |

For each zone or conduit, the adopter sets:

- **SL-T (Security Level Target)**: the required protection level given the risk assessment.
- **SL-A (Security Level Achieved)**: the protection level actually attained by the deployed implementation.
- **SL-C (Security Level Capability)**: the protection level the component is capable of supporting when correctly configured.

A zone or conduit is **compliant** when SL-A ≥ SL-T and the SL-C of every contributing component supports SL-A.

### 4.4 The Purdue model layered architecture

The Purdue Enterprise Reference Architecture (Purdue model) is a hierarchical reference architecture for ICS network segmentation. It defines six layers:

| Level | Layer | Typical contents |
| --- | --- | --- |
| **5** | Enterprise Network | Business systems, ERP, email |
| **4** | Site Business Network | Site IT systems, business-facing applications |
| **3.5** | DMZ between OT and IT | Patching servers, historians replicated for IT use, jump hosts |
| **3** | Site Operations | OT historians, engineering workstations, master servers |
| **2** | Area Supervisory Control | HMI, SCADA supervisory, area-level operations |
| **1** | Basic Control | PLCs, RTUs, controllers |
| **0** | Physical Processes | Sensors, actuators, motors, valves, the physical process itself |

The library aligns with IEC 62443's zone-and-conduit model (which is doctrinally compatible with the Purdue layers but more flexible). Adopters with established Purdue deployments map their layers to IEC 62443 zones during the risk assessment defined in 62443-3-2.

---

## 5. OT-specific risk considerations

Adopters performing risk assessment for OT environments must consider these OT-specific factors that do not arise in IT contexts:

| Risk consideration | OT-specific factor |
| --- | --- |
| **Safety consequence** | OT incidents can injure or kill. Risk assessments must include safety analysis (HAZOP, LOPA) alongside cyber-risk analysis. Safety regulations may override security recommendations. |
| **Vendor lock-in** | OT systems are typically vendor-controlled. Patches require vendor approval; reverse-engineering is often prohibited. Vendor lifecycle governance is critical. |
| **Legacy OS** | OT systems often run unpatched legacy Windows or proprietary OS. Network isolation and host-hardening compensate where patching is impractical. |
| **Protocol vulnerabilities** | OT protocols (Modbus, DNP3, EtherNet/IP, PROFINET, OPC UA pre-encryption) are typically insecure by design. Network segmentation and protocol-aware monitoring compensate. |
| **Long change windows** | Maintenance outages may be annual. Patching schedules must align with production planning. |
| **Recovery time** | Recovery from a successful OT incident may require physical access to remote sites, vendor on-site presence, and days-to-weeks of effort, not hours. RTOs are typically longer than IT equivalents. |
| **Third-party access** | OT integrators, maintenance vendors, and remote-support providers regularly access OT environments. Vendor access governance is more critical than for IT. |
| **IT/OT convergence** | Modern OT environments are increasingly connected to IT and the internet. Many historical air-gap assumptions are no longer valid. Architecture must assume connected, not isolated. |

The [`OT/ICS Security Standard`](standard-ot-ics-security.md) codifies these into specific control requirements; this annex notes them as concepts.

---

## 6. Cross-domain relationships

| Library domain | OT relationship |
| --- | --- |
| **Security** | OT-specific incident response builds on the general procedure ([`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)) with safety-first additions. |
| **Operations** | OT-specific change management builds on the general change procedure ([`operations/procedure-change-management-and-configuration-control.md`](../procedure-change-management-and-configuration-control.md)) with longer windows and vendor coordination. |
| **Operations: network segmentation** | The OT/ICS Standard's zone-and-conduit model extends the general network segmentation standard ([`operations/standard-network-security-and-segmentation.md`](../standard-network-security-and-segmentation.md)). |
| **Resilience** | OT recovery objectives are longer; the resilience domain's BC/DR templates accommodate OT-specific RTO/RPO. |
| **Compliance: energy-and-utilities** | Energy-sector OT (electricity, gas, water, pipelines) is in scope for NERC CIP and equivalents; the sector annex references this OT sub-directory for technical specifics. |
| **Compliance: logistics** | Port, terminal, freight rail, warehouse automation systems are OT; the logistics sector annex references this sub-directory. |
| **Compliance: healthcare** | Medical-device control is OT-adjacent. The healthcare sector annex governs MDR/IVDR specifics; this annex governs underlying OT security concepts. |
| **Supply chain** | OT vendor governance is a special case of supplier governance. IEC 62443-2-4 specifies OT-specific supplier-security requirements. |

---

## 7. Frequently asked questions

**Is air-gapping enough?**

Historically, air-gapping was the dominant OT control. In modern environments, true air-gapping is rare: maintenance laptops, USB drives, remote-support modems, vendor connections, and IIoT sensors all create paths. The library treats air-gapping as a defence-in-depth contributor, not a primary control. IEC 62443 zone-and-conduit segmentation (and assumption of connection) is the modern baseline.

**Where does IT security stop and OT security start?**

The library's position: there is no clean stop point. IT and OT controls overlap and reinforce each other. The OT-specific overlays in this sub-directory cover what differs (safety, lifecycle, change tolerance, recovery time). The universal baseline (security/, operations/, governance/) covers the rest. Adopters apply both.

**Do we need a separate OT SOC?**

Depends on scale. Small OT footprints can be monitored by the existing SOC with OT-trained analysts and OT-aware tooling. Large OT footprints (utilities, multi-plant manufacturers) often warrant a dedicated OT SOC for response-time, vendor-coordination, and safety reasons. The [`OT Incident Response Procedure`](procedure-ot-incident-response.md) discusses the trade-offs.

**Does Zero Trust apply to OT?**

Conceptually yes, but with OT-specific adaptations. NIST SP 800-207 Zero Trust principles apply (verify explicitly, least privilege, assume breach), but the deterministic real-time constraints, legacy components, and vendor-controlled systems limit some Zero Trust implementations. The library acknowledges Zero Trust as a target architecture for OT/IT convergence layers (Purdue 3.5 and above) while accepting that lower OT layers may use traditional segmentation pragmatically.

---

## 8. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443-1-1 | Concepts and models | Primary alignment: zones, conduits, security levels |
| IEC 62443-2-1 | Establishing an IACS security programme | OT security programme governance |
| IEC 62443-3-2 | Security risk assessment for system design | OT risk assessment methodology |
| IEC 62443-3-3 | System security requirements and security levels | Security level definitions (SL 1 to 4) |
| NIST SP 800-82 Rev. 3 | Guide to Operational Technology (OT) Security | US federal guidance; OT-specific tailoring of SP 800-53 |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Underlying control catalogue |
| ISO/IEC 27001:2022 | Information security management systems | ISMS scope when extended to OT |
| ISO/IEC 27019:2024 | Information security controls for the energy utility industry | Energy-sector ICS extension to ISO/IEC 27002 |
| IEC 61511 / IEC 61508 | Functional safety | Safety Instrumented Systems specifics |
| NERC CIP | Critical Infrastructure Protection | North American electricity sector; see energy-and-utilities annex |

---

**End of Document**
