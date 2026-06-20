# Energy and Utilities Sector Requirements Annex

**Document Title:** Energy and Utilities Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.4\
**Date:** 2026-06-20\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/annex-nis-2-implementation.md`](../annex-nis-2-implementation.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material sector-regulator, IEC 62443, or critical-infrastructure-protection-standard change\
**Repository Path:** [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](annex-energy-and-utilities-sector-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how organisations operating in energy generation, transmission, distribution, supply, oil and gas, drinking water, waste water, and district heating can use the core library while satisfying the overlay obligations imposed by sector-specific regulators and standards. It covers operational technology (OT) and industrial control system (ICS) cybersecurity, critical-infrastructure-protection standards, sector incident reporting, physical-cyber convergence, and supplier and component security particular to energy and utilities.

This annex does not reproduce the text of NERC CIP, IEC 62443, ENTSO-E network codes, or national sector law. Adopting entities consume those from the official source.

---

## Applicability triggers

This annex applies where the organisation operates or supports:

1. Electricity generation, transmission, or distribution above any nationally defined threshold.
2. Natural gas, LNG, or hydrogen transmission, distribution, or storage.
3. Oil refining, transport, or storage.
4. Drinking water supply or waste water treatment.
5. District heating and cooling.
6. Renewable energy generation at utility scale.
7. Nuclear power, fuel cycle, or radioactive waste management.
8. Smart-grid services, meter operation, virtual power plant aggregation, or distributed energy resource management at scale.

Subsector-specific obligations vary materially. The annex identifies overlay areas common across the sector.

---

## Overlay area 1: critical-infrastructure cybersecurity baselines

| Regime | Applicability | Library support |
| --- | --- | --- |
| NERC CIP (CIP-002 through CIP-014) | Bulk Electric System in North America | Library provides NIST-aligned baselines; the entity layers the CIP requirements per Cyber Asset categorisation |
| EU NIS 2 | Energy and water sectors as Essential entities | See [`compliance/annex-nis-2-implementation.md`](../annex-nis-2-implementation.md) |
| US TSA Pipeline Security Directives and Rail Cybersecurity Directives | Critical pipelines and rail | Library supports; entities follow the directive's specific identification of measures and reporting |
| IEC 62443 series | ICS / OT cybersecurity | Architectural alignment in library; per-zone and per-conduit requirements layered |
| UK NIS (post-NIS 2 timeline) | Operators of essential services in energy, water | National competent authority guidance |
| Canada CER, NEB-equivalent cybersecurity | Federally regulated pipelines | National regulator guidance |
| AEMO and AER cybersecurity guidance | Australian electricity market | National regulator guidance |

---

## Overlay area 2: OT and ICS cybersecurity

The IT-OT boundary is the defining technical risk of the sector. The library provides IT-centric controls; OT-specific overlay is required.

| OT control area | Library support and overlay |
| --- | --- |
| Network segmentation between corporate IT and OT (Purdue model zones) | [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md); entities implement the Purdue Level 3.5 DMZ and below per IEC 62443-3-3 |
| OT asset inventory including device firmware versions and PLC programme versions | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) extended with OT-specific fields (vendor, firmware, last-patched, network address, function) |
| OT vulnerability management with availability-first patching cadence | [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md) and [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md) extended; OT typically requires longer patching windows and pre-tested patches |
| Privileged access to engineering workstations and HMIs | [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md); jump-host and recorded sessions for OT access |
| Removable media controls for OT engineering workstations | [`operations/procedure-media-handling-and-transport.md`](../../operations/procedure-media-handling-and-transport.md) |
| Safety-instrumented system (SIS) independence | Outside library scope; sector engineering safety standard |
| OT monitoring and anomaly detection | Library logging and monitoring extended with OT-specific protocols (Modbus, DNP3, IEC 61850, BACnet, ICCP, OPC UA) |
| Backup and restore of PLC and HMI configurations | [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md) extended for OT configuration backup |
| Vendor remote access to OT systems | [`security/standard-remote-working-security.md`](../../security/standard-remote-working-security.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md); OT vendor access typically requires escorted, time-boxed, recorded sessions |
| OT incident response with safety-first decision rules | [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md) extended; OT incident response prioritises safety and continuity over technical containment |

---

## Overlay area 3: physical-cyber convergence

Energy and utilities operations integrate physical and cyber security.

| Obligation | Library support |
| --- | --- |
| Physical perimeter, access control, surveillance for substations and facilities | [`operations/standard-physical-security-of-it-infrastructure.md`](../../operations/standard-physical-security-of-it-infrastructure.md) extended for industrial sites |
| Combined physical-cyber incident playbook | [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md) and [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md) extended for converged incidents |
| Drone, intrusion, and tamper detection | Outside library scope; site-specific |
| Coordination with law enforcement and national security services | Outside library scope |

---

## Overlay area 4: sector incident reporting

Reporting obligations vary; the entity may be required to report to multiple authorities for the same incident.

| Reporting recipient | Typical trigger | Window (illustrative) |
| --- | --- | --- |
| National sector regulator (e.g. UK Ofgem, US FERC, EU national NIS competent authority) | Cybersecurity or operational incident affecting service | 24 hours to 72 hours per national rule |
| National CSIRT under NIS 2 | Significant cybersecurity incident | Early warning within 24 hours of awareness |
| Reliability authority (e.g. NERC) | CIP-008-required incident criteria | One hour after determination |
| Privacy supervisor | Personal data breach | 72 hours under GDPR; equivalents elsewhere |
| Stock-exchange disclosure | Material adverse event for listed entities | Per listing rules |

Library coverage: [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../../resilience/procedure-security-incident-reporting-and-escalation.md). Adopting entities maintain a per-incident reporting matrix mapping the regulatory recipients to the incident class and the report content required.

---

## Overlay area 5: supplier and component security

Energy and utilities supply chains include vendor-specific national-security considerations.

| Obligation | Library support |
| --- | --- |
| Approved-vendor list for OT components (relays, PLCs, RTUs, IEDs, SCADA systems) | [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) |
| Vendor cybersecurity attestation per IEC 62443-4-1 (product development) and 4-2 (component requirements) | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md) plus IEC-specific evidence |
| SBOM for ICS and embedded components | [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) |
| Vendor escort and supervised access for maintenance | [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../../supply-chain/procedure-supplier-ongoing-monitoring.md) |
| Country-of-origin restrictions where required by national security | Per national rules (US Executive Orders on bulk-power-system equipment, equivalents) |

---

## Overlay area 6: resilience and continuity

Energy and utilities outages have direct safety and societal impact; resilience is regulated and audited.

| Obligation | Library support |
| --- | --- |
| Service continuity and restoration plans | [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) |
| Mutual-aid arrangements with peer operators | Outside library scope; sector agreement |
| Black-start capability and grid restoration plans | Outside library scope; sector technical standard |
| Annual exercise per the regulator (e.g. NERC GridEx) | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) |
| Reliability reporting | Per the reliability authority |

---

## Library gaps requiring additional documentation

1. **OT asset inventory** with OT-specific attributes (firmware, PLC programme version, function, network zone).
2. **OT cybersecurity programme** at IEC 62443-2-1 level.
3. **OT incident response playbook** with safety-first decision rules.
4. **Physical-cyber converged incident procedure.**
5. **Per-regulator incident reporting matrix.**
6. **Approved-vendor list for OT components** with country-of-origin annotations where required.
7. **Black-start and grid restoration plans** (electricity sector).
8. **Annual GridEx-equivalent exercise plan.**

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IEC 62443 series | International | OT and ICS cybersecurity |
| ISA 62443 | ISA-aligned to IEC 62443 | OT cybersecurity in North American practice |
| NERC CIP | CIP-002 through CIP-014 | Bulk electric system cybersecurity (North America) |
| NIS 2 | (EU) 2022/2555 | EU essential entities including energy and water |
| US TSA Pipeline Security Directives | TSA SDs | Pipelines |
| US TSA Rail Cybersecurity Directives | TSA SDs | Rail |
| EU Critical Entities Resilience Directive | (EU) 2022/2557 | Physical and operational resilience |
| US Executive Orders on bulk-power-system equipment | EO 13920 and successors | Supply-chain security |
| ENTSO-E Network Codes | EU electricity codes | Cross-border cybersecurity in electricity |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. Energy and utilities cybersecurity is highly regulated and varies materially by subsector and jurisdiction. Operating technology requires specialist engineering that goes beyond the library's IT-centric baseline. Safety, reliability, and continuity obligations are typically the dominant constraint; cybersecurity decisions defer to engineering safety where they conflict. Adopting entities engage sector-specialist counsel, OT cybersecurity engineering, and the regulator. This annex is not legal advice and does not establish compliance.

---

**End of Document**
