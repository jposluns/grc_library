# Operational Technology (OT)

**Document Title:** Operational Technology (OT) Sub-Directory README\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/README.md`](../README.md), [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md), [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md), [`compliance/energy-and-utilities/`](../../compliance/energy-and-utilities/), [`compliance/logistics/`](../../compliance/logistics/)\
**Classification:** Public\
**Category:** Operations: Operational Technology\
**Review Frequency:** Annual and upon material change to IEC 62443, NIST SP 800-82, or sector-specific OT regulations\
**Repository Path:** [`operations/ot/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This sub-directory contains the library's Operational Technology (OT) security content: governance, standards, and procedures for organisations that operate Industrial Control Systems (ICS), SCADA systems, Distributed Control Systems (DCS), Programmable Logic Controllers (PLCs), Building Management Systems (BMS), or other OT environments.

OT differs from IT in three operationally significant ways:

1. **Physical-world impact**: OT failures or compromises can cause property damage, environmental harm, or loss of life: not just data loss or service downtime. Safety is the dominant concern.
2. **Long asset lifecycles**: OT systems often operate for 15-25 years with limited patchability and frequent reliance on legacy operating systems and protocols.
3. **Availability over confidentiality**: traditional IT security prioritizes confidentiality first; OT environments prioritize availability and integrity, with confidentiality typically third.

These differences shape the security controls, incident response, change management, and asset lifecycle approaches collected in this sub-directory.

---

## Scope

The OT sub-directory covers:

- **Industrial Control Systems (ICS)**: SCADA, DCS, PLC-based control for manufacturing, energy, water, transportation, oil and gas.
- **Building Management Systems (BMS)**: HVAC, lighting, fire/life-safety, physical access control automation, smart-building infrastructure.
- **Safety Instrumented Systems (SIS)**: process-safety automation governed by IEC 61511 / IEC 61508.
- **Cross-cutting OT considerations**: network segmentation (Purdue model / IEC 62443 zones and conduits), OT-specific incident response, OT change management, OT asset inventory and lifecycle.

The sub-directory does **not** duplicate IT security content already in the library; it focuses on what is OT-specific. Where OT and IT controls converge (for example, identity and access management for OT engineering workstations that are domain-joined), the main library applies and the OT documents note any OT-specific overlay.

---

## Active documents

| Type | Title | Path |
| --- | --- | --- |
| Annex | OT Security Overview Annex | [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md) |

---

## Planned documents (Phase 22.2 onward)

- **Standard**: OT/ICS Security Standard (segmentation, zone-and-conduit model, security-level achievement, OT-specific access control). Phase 22.2.
- **Procedure**: OT Incident Response Procedure (safety-first response, vendor coordination, longer recovery windows). Phase 22.3.
- **Procedure**: OT Change Management Procedure (extended change windows, vendor approval, regression testing for safety-critical functions). Phase 22.4.
- **Register**: OT Asset Inventory and Lifecycle Register (long-lifecycle assets, legacy OS handling). Phase 22.5.
- **Annex**: BMS-specific overlay (HVAC, access control, fire/life-safety integration considerations). Phase 22.6.

---

## Relationship to other domains

This sub-directory cross-cuts with:

- **[`compliance/energy-and-utilities/`](../../compliance/energy-and-utilities/)**: utility OT (electricity grid, pipelines, water systems) is OT.
- **[`compliance/logistics/`](../../compliance/logistics/)**: port, terminal, freight rail, and warehouse automation systems are OT.
- **[`compliance/healthcare/`](../../compliance/healthcare/)**: medical-device control overlaps with OT but is governed by MDR/IVDR.
- **[`operations/standard-network-security-and-segmentation.md`](../standard-network-security-and-segmentation.md)**: general network segmentation; the OT sub-directory's standard extends this with the IEC 62443 zone-and-conduit model.
- **[`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)**: general incident response; the OT procedure (when added) extends with safety-first specifics.

---

## Reference standards

The OT sub-directory aligns to the following canonical standards (recorded in [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md)):

- **IEC 62443 family**: Industrial Automation and Control Systems Security. Primary alignment.
  - 62443-1-1: Concepts and models
  - 62443-2-1: Establishing an IACS security programme
  - 62443-2-4: Service providers
  - 62443-3-2: Security risk assessment for system design
  - 62443-3-3: System security requirements and security levels
  - 62443-4-1: Secure product development lifecycle
  - 62443-4-2: Technical security requirements for IACS components
- **NIST SP 800-82 Rev 3**: Guide to Operational Technology (OT) Security. Authoritative US federal guidance.
- **IEC 61511 / IEC 61508**: Functional safety for Safety Instrumented Systems and electrical/electronic/programmable safety systems.
- **NERC CIP**: for North American electricity reliability (cross-referenced from `compliance/energy-and-utilities/`).

---

## Adopter guidance

If you operate OT environments, read in this order:

1. [`operations/ot/annex-ot-security-overview.md`](annex-ot-security-overview.md): sector and concepts overview (this Phase 22.1 deliverable).
2. The general operations and security baselines first (universal baseline in [`docs/decision-tree.md`](../../docs/decision-tree.md)).
3. The OT-specific standard, procedures, and registers as they are added in Phases 22.2 onward.
4. Your relevant sector-compliance annex (energy-and-utilities, logistics, healthcare).

Organisations without OT environments can skip this sub-directory entirely.

---

**End of Document**
