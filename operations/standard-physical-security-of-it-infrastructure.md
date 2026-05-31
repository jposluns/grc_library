# Physical Security of IT Infrastructure Standard

**Document Title:** Physical Security of IT Infrastructure Standard\
**Document Type:** Standard\
**Version:** 1.3.0\
**Date:** 2026-05-27\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/standard-network-security-and-segmentation.md`](standard-network-security-and-segmentation.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-physical-security-of-it-infrastructure.md`](standard-physical-security-of-it-infrastructure.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Scope boundary

Covers physical security controls for IT infrastructure owned and operated by the CIO's office. Covers server rooms, network closets, camera and NVR systems, and IT equipment. Broader facility physical security, building access systems, perimeter fencing, guard services, visitor management, is outside IT scope and governed by Facilities and Operations.

---

## Purpose

Defines minimum physical security requirements for IT infrastructure areas under direct control of the CIO. Ensures that hardware, cabling, and IT equipment are protected from unauthorized physical access, tampering, environmental hazards, and theft. Supports the Information Security Policy and the Standard: Cloud Security Configuration Baseline (which governs logical controls). Aligns to ISO/IEC 27001:2022 Annex A.7 (Physical Controls) within IT scope.

---

## Scope

1. Applies to all IT infrastructure areas under CIO management including the primary data centre server room, network closets, UPS and power distribution equipment, and IT equipment rooms at all office locations.
2. Covers access control to IT rooms, camera surveillance systems and NVR infrastructure, environmental monitoring, equipment handling, and clean desk requirements for IT operations areas.
3. Does not govern building perimeter access, parking areas, reception, or non-IT physical security: those are Facilities responsibilities.

---

## Governance

| Role | Responsibility |
|---|---|
| CISO | Owns this standard; approves access to server rooms and IT equipment rooms; reviews access logs. |
| IT Operations | Manages physical access controls to IT rooms; operates and maintains camera and NVR systems; responds to physical security incidents. |
| Facilities (coordination only) | Coordinates on building access infrastructure where IT room access is integrated with the broader building access system. Does not govern IT room access decisions. |
| Internal Audit | Reviews IT room access logs and physical security control compliance annually. |

---

## 1. Server room and data centre physical access

Access to the primary data centre server room and all IT equipment rooms is restricted to authorized IT Operations personnel.

| Control | Requirement |
|---|---|
| Access authorization | Access granted by CISO or designated IT Operations lead. Access list reviewed quarterly and immediately upon departure of any authorized individual. |
| Access mechanism | Physical access requires a credential (key card, PIN, or key) separate from general office access. Multi-factor physical access (card plus PIN) required for the primary data centre server room. |
| Visitor and contractor access | Vendors, contractors, and visitors must be accompanied by an authorized IT Operations staff member at all times inside IT infrastructure areas. Unescorted access not permitted. Visitor access logged. |
| Access logging | All physical access events logged electronically or manually. Logs retained for 2 years per the Records Retention Schedule and reviewed monthly by IT Operations. |
| Tailgating prevention | Personnel must not permit others to follow them through access-controlled doors. Anti-tailgating procedures covered in the Security Awareness and Training Standard. |

---

## 2. Camera surveillance and NVR systems

The organisation operates IP camera systems at office and data centre locations under IT Operations management.

| Control | Requirement |
|---|---|
| Coverage | Camera coverage must include all entry and exit points to IT infrastructure areas, server room floors, and any area where IT equipment is staged or stored. |
| NVR access | Network Video Recorder (NVR) systems are on a dedicated management VLAN within the Management network zone per the Network Security and Segmentation Standard. NVR administrative access restricted to IT Operations and governed by the PAM Standard (PIM-activated credentials). |
| Footage retention | Camera footage retained for a minimum of 90 days. Footage relevant to a security incident is preserved for the duration of the investigation and any subsequent legal or regulatory proceedings. |
| Footage access | Access to camera footage restricted to the CISO and designated IT Operations personnel. Requests from other parties (HR, Legal, law enforcement) require CISO approval and documentation. |
| Privacy notice | Camera surveillance in workplaces disclosed to employees per applicable privacy law. Notices posted at surveilled locations. The Privacy Management Programme governs privacy obligations associated with surveillance data. |
| System health monitoring | NVR system health and camera feed status monitored by IT Operations. Camera outages treated as P3 incidents, remediated within 48 hours. Outages affecting IT room coverage treated as P2. |

---

## 3. Environmental controls

IT Operations is responsible for:

1. Ensuring HVAC or dedicated cooling systems serving IT rooms are operational and maintained. Cooling failures in the primary data centre server room treated as P2 incidents.
2. Monitoring temperature and humidity in the server room. Alerts configured to notify IT Operations if temperature exceeds 27°C or humidity exceeds 60%.
3. Ensuring fire suppression systems in IT rooms are tested annually. IT Operations coordinates with Facilities for testing scheduling.
4. Ensuring UPS systems protecting IT equipment are tested and load-verified at minimum annually.

---

## 4. Equipment handling

IT equipment entering or leaving an IT infrastructure area must be logged in the asset register before removal. Equipment removed without an asset register update is treated as potential theft and investigated as a P2 incident. Decommissioned equipment must be sanitized per the Media Handling and Transport Procedure before leaving IT custody.

---

## 5. Clean desk and clear screen

IT Operations areas and the server room must maintain a clean desk policy. Printed documents containing Confidential or Restricted data must not be left unattended on desks in shared IT areas. Workstations in IT areas lock automatically after 15 minutes of inactivity per the endpoint compliance policy. Personnel must manually lock the screen when leaving a workstation unattended.

---

## Framework alignment

| Framework | Reference |
|---|---|
| ISO/IEC 27001:2022 | Annex A.7: Physical Controls (server room and IT equipment scope only) |
| NIST SP 800-53 | PE-2, PE-3, PE-6: Physical Access Authorization, Control, and Monitoring |
| CSA CCM v4.1 | IVS-03: Infrastructure and Virtualization Security: Physical Security |
| CTPAT Minimum Security Criteria | Physical Access Controls for IT Systems |
| Canada PIP | Physical Security of IT Infrastructure |

---

*This document is released under CC BY-SA 4.0. No rights reserved.*



**End of Document**
