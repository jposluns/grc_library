# Transportation and Logistics Sector GRC Requirements Annex

**Document Title:** Transportation and Logistics Sector GRC Requirements Annex  
**Document Type:** Annex  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Compliance Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md), [`compliance/register-ctpat-compliance-controls.md`](register-ctpat-compliance-controls.md), [`compliance/register-pip-compliance-controls.md`](register-pip-compliance-controls.md), [`compliance/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md), [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md)  
**Classification:** Public  
**Category:** Compliance — Sector-Specific  
**Review Frequency:** Annual and upon material regulatory change, new TSA directive, or significant security incident in the sector  
**Repository Path:** [`compliance/annex-transportation-and-logistics-sector-requirements.md`](annex-transportation-and-logistics-sector-requirements.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This annex identifies the additional GRC obligations that apply to organisations operating in the transportation and logistics sector. It maps applicable regulatory frameworks to the core GRC library controls and identifies gap areas requiring sector-specific supplementation.

This annex applies where an organisation:
- Operates as a freight forwarder, customs broker, third-party logistics provider (3PL), or fourth-party logistics provider (4PL)
- Operates road, rail, air, or maritime transportation services
- Manages warehousing, distribution centres, or cross-docking operations
- Operates port, airport, or intermodal terminal infrastructure
- Provides technology platforms for transportation management, track and trace, or customs processing
- Participates in trusted-trader programmes (CTPAT, AEO-S, PIP, BASC, NEEC, OEA)

**Note on trusted-trader programme compliance:** CTPAT, AEO-S, PIP, BASC, and other trade compliance programme requirements are documented in detail in the supply chain domain. This annex addresses cybersecurity-specific regulatory obligations from transportation sector authorities that apply beyond trade compliance programmes.

---

## Regulatory Landscape Overview

### United States

| Regulation / Directive | Authority | Mode / Scope |
|---|---|---|
| **TSA Security Directive SD 02C** — Pipeline Cybersecurity | Transportation Security Administration (TSA) | Critical pipeline operators |
| **TSA Security Directive SD-1580/82-2022-01** — Surface Transportation Cybersecurity | TSA | Passenger and freight railroad carriers; owner-operators of highways |
| **TSA Security Directive SD-1582-21-01** — Freight Rail Cybersecurity | TSA | Freight railroad carriers; rail transit; designated categories |
| **TSA Security Directive — Aviation Cybersecurity** | TSA | Airport operators; aircraft operators; last-mile delivery involving air |
| **USCG Maritime Cybersecurity (NVIC 01-20)** | U.S. Coast Guard | Maritime Transportation Security Act (MTSA) facility owners and operators; vessel operators |
| **DOT Cybersecurity Strategy** | U.S. Dept of Transportation | All DOT-regulated entities |
| **FMCSA — Electronic Logging Devices (ELD)** | Federal Motor Carrier Safety Administration | Commercial motor vehicle operators |
| **CBP — CTPAT** | U.S. Customs and Border Protection | Importers, exporters, customs brokers, freight forwarders, carriers |
| **FAA Cybersecurity** | Federal Aviation Administration | Aviation operators; air traffic management |
| **Sanderson Act / Rail Safety** | FRA | Freight rail operators |

### Canada

| Regulation / Programme | Authority | Scope |
|---|---|---|
| **Transport Canada Cybersecurity** | Transport Canada | Aviation, marine, rail, and road operators |
| **Canadian Aviation Security Regulations (CASR)** | Transport Canada | Air carriers; aerodrome operators |
| **Marine Transportation Security Act / Regulations (MTSR)** | Transport Canada | Vessels; marine facilities; ports |
| **PIP — Partners in Protection** | CBSA | Freight importers; carriers; customs brokers |
| **Canadian Rail Safety Act** | Transport Canada | Federally regulated railways |
| **PIPEDA / CPPA** | OPC | All personal data processing |

### United Kingdom

| Regulation / Guidance | Authority | Scope |
|---|---|---|
| **Network and Information Systems (NIS) Regulations 2018** | NCSC / DSIT | Digital Service Providers; Operators of Essential Services (OES) including transport |
| **CAA CAP 1753 — Aviation Cyber Security** | Civil Aviation Authority | UK aviation entities; airlines; ANSPs; airports |
| **DfT Cyber Security Code of Practice for Vehicles** | Department for Transport | Connected and automated vehicle manufacturers |
| **UK AEO-S** | HMRC | Customs operators; logistics providers |
| **Port Security Regulations** | DfT / Home Office | Port facility operators |
| **UK GDPR** | ICO | All personal data |
| **HMRC Customs Obligations** | HMRC | All customs operators post-Brexit |

### European Union

| Regulation / Directive | Authority | Scope |
|---|---|---|
| **NIS 2 Directive (2022/2555)** | National competent authorities | Essential entities including road transport, rail, air, maritime, port facilities, logistics |
| **EU Aviation Security Regulation (EC) 300/2008** | EASA / national authorities | Air carriers; airports; cargo operators |
| **EASA AMC 20-42 — Aviation Cybersecurity** | EASA | Aviation organisations; airspace users |
| **EU Maritime Security (Regulation 725/2004)** | EMSA / national authorities | Ships; port facilities |
| **ITS Regulation 2021/575** | European Commission | Intelligent transport systems |
| **EU AI Act (High Risk — Annex III)** | EU AI Office | AI in critical transport infrastructure management |
| **AEO (EU UCC Art 38)** | National customs authorities | Customs operators |

### Global / International

| Standard / Programme | Body | Scope |
|---|---|---|
| **ICAO Doc 10026 — Aviation Security** | International Civil Aviation Organization | States; aviation operators |
| **ICAO Doc 10055 — Aviation Cybersecurity Strategy** | ICAO | States; airlines; ANSPs; airports |
| **IMO Resolution MSC-FAL.1/Circ.3** — Maritime Cyber Risk Management | International Maritime Organization | Shipping companies; port operators |
| **IMO MSC-FAL.1/Circ.3 Rev 1** | IMO | Incorporated into ISM Code |
| **IATA Cyber Security Guidance** | International Air Transport Association | IATA member airlines; handling agents |
| **WCO SAFE Framework** | World Customs Organization | All customs operators |
| **ISO 28000:2022** — Supply chain security | ISO | Supply chain organisations |
| **ISO 28001** — Best practices for implementing supply chain security | ISO | Customs clearance verification |
| **ISO/SAE 21434** — Road Vehicle Cybersecurity Engineering | ISO / SAE | Vehicle OEMs; automotive supply chain |
| **UNECE WP.29 / R155** — Cybersecurity Management System for vehicles | UNECE | Vehicle manufacturers selling in participating markets |

---

## Key Regulatory Requirements

### TSA Cybersecurity Directives (US Surface Transportation and Pipeline)

TSA Security Directives for surface transportation (freight rail, highway) and pipelines mandate specific cybersecurity measures. Key requirements applicable across directives:

| Requirement | Detail | GRC Library Mapping |
|---|---|---|
| **Cybersecurity Incident Reporting** | Report cybersecurity incidents to CISA within 24 hours | [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) — supplement with CISA reporting procedure |
| **Cybersecurity Point of Contact** | Designate and report to TSA a primary and alternative cybersecurity point of contact | Role designation procedure |
| **Cybersecurity Gap Assessment** | Complete TSA-prescribed cybersecurity gap assessment | [`compliance/template-trade-compliance-gap-assessment.md`](template-trade-compliance-gap-assessment.md) — supplement with TSA-specific assessment |
| **Cybersecurity Incident Response Plan** | Develop and implement a cybersecurity incident response plan | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) |
| **Cybersecurity Management Plan** | Implement specific measures including: (1) network segmentation; (2) access controls; (3) continuous monitoring; (4) patch management | [`security/policy-information-security.md`](../security/policy-information-security.md); [`security/procedure-access-control.md`](../security/procedure-access-control.md); [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) |
| **Annual assessment** | Annual cybersecurity assessment and update | [`compliance/standard-internal-audit.md`](standard-internal-audit.md) |

**CISA Reporting Timeline:** Cybersecurity incidents affecting transportation critical infrastructure must be reported to CISA within 24 hours of discovery under CIRCIA (Cyber Incident Reporting for Critical Infrastructure Act).

### EU NIS 2 — Transportation Essential Entities

Under NIS 2, transportation entities in the following sub-sectors are classified as **essential entities** and subject to the highest tier of obligations:

- Air transport (airlines, airports, air traffic management)
- Rail transport (railway infrastructure managers; railway undertakings)
- Water transport (inland waterway transport; sea and coastal water transport; ports; vessels)
- Road transport (road authorities; operators of intelligent transport systems)
- Post and courier services (where meeting size thresholds)

**Key NIS 2 cybersecurity obligations for essential entities:**

| NIS 2 Article | Obligation | GRC Library Mapping |
|---|---|---|
| Art 21 — Cybersecurity risk management | Risk-proportionate technical and organisational measures across 10 minimum areas | [`security/policy-information-security.md`](../security/policy-information-security.md); [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) |
| Art 21(2)(a) — Policies on risk analysis | Documented policies on risk analysis and information system security | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md) |
| Art 21(2)(b) — Incident handling | Incident detection and response | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) |
| Art 21(2)(c) — Business continuity | BCM, backup management, DR, crisis management | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md); [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) |
| Art 21(2)(d) — Supply chain security | Security policies for suppliers and service providers | [`supply-chain/standard-third-party-risk.md`](../supply-chain/standard-third-party-risk.md); [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) |
| Art 21(2)(e) — Secure development | Security in network and information systems acquisition, development, maintenance | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md) |
| Art 21(2)(f) — Vulnerability handling | Vulnerability disclosure and patch management | [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) |
| Art 21(2)(g) — Cybersecurity training | Cybersecurity hygiene and training | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) |
| Art 21(2)(h) — Cryptography | Policies on use of cryptography and encryption | [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md) |
| Art 21(2)(i) — Human resources security | Personnel security, access control, asset management | [`security/procedure-access-control.md`](../security/procedure-access-control.md); [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) |
| Art 21(2)(j) — Multi-factor authentication | MFA / continuous authentication where appropriate | [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) |
| Art 23 — Incident notification | Report significant incidents to national CSIRT within 24 hours (initial); 72 hours (assessment); 1 month (final report) | [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) — supplement with NIS 2 notification templates |

**NIS 2 Penalties:** Essential entities — up to €10M or 2% of global annual turnover (whichever is higher).

### IMO Maritime Cyber Risk Management

IMO Resolution MSC-FAL.1/Circ.3 (incorporated into ISM Code as of 1 January 2021) requires shipping companies to incorporate cyber risk management into their Safety Management Systems.

| IMO Requirement | GRC Library Mapping |
|---|---|
| Identify systems and assets supporting shipping operations | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) — supplement for OT/operational technology assets |
| Assess cyber risks to identified systems | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md) |
| Protect against identified risks | [`security/policy-information-security.md`](../security/policy-information-security.md) |
| Detect cyber events | [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) |
| Respond and recover from cyber incidents | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md); [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) |
| Incorporate into ISM Code and Document of Compliance | Supplement: ISM Code cyber annex |

**Critical OT systems requiring risk assessment:** ECDIS (navigation); GPS/AIS; GMDSS (communications); cargo management systems; engine monitoring; access control systems.

### ICAO Aviation Cybersecurity (Doc 10055)

ICAO's Aviation Cybersecurity Strategy requires states and aviation organisations to implement cybersecurity measures across the aviation ecosystem. Key areas:

| ICAO Area | Requirement | GRC Library Mapping |
|---|---|---|
| Governance | Cybersecurity governance framework; designated accountable executive | [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md) |
| Risk management | Cyber risk identification and mitigation | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) |
| Incident management | Aviation-specific incident response; reporting to national aviation authority | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) — supplement with CAA/FAA notification procedure |
| Supply chain | Cybersecurity requirements for aviation suppliers | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) |
| Training and awareness | Aviation-specific cybersecurity training | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) |
| Resilience | Cyber resilience for safety-critical systems | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) |

**CAA CAP 1753 (UK):** The UK Civil Aviation Authority's aviation cybersecurity framework aligns with ICAO Doc 10055 and maps to the CAF (Cyber Assessment Framework). UK aviation organisations must demonstrate compliance through CAF self-assessment.

### HMRC Post-Brexit Customs Obligations (UK)

Following the UK's departure from the EU, all organisations moving goods between the UK and EU must comply with UK customs requirements administered by HMRC. Key technology-related obligations:

| Obligation | Detail | GRC Library Mapping |
|---|---|---|
| **Customs Declaration Service (CDS)** | Electronic customs declarations must be filed through CDS | Systems compliance with CDS API requirements |
| **CHIEF to CDS migration** | All declarants must have migrated from CHIEF to CDS | Systems audit and update |
| **AEO-S status maintenance** | UK AEO-S requires ongoing compliance with HMRC security criteria | [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md); [`compliance/procedure-aeo-it-self-assessment.md`](procedure-aeo-it-self-assessment.md) |
| **TSP (Trusted Smart Freight)** | HMRC's Trusted Smart Freight partnerships for digital customs | Emerging obligation — monitor HMRC guidance |
| **GDPR / UK GDPR for shipment data** | Personal data in shipping documents (consignee names, etc.) | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) |

---

## Operational Technology (OT) and Industrial Control System Security

Transportation and logistics operators frequently operate Operational Technology (OT) environments including warehouse management systems, automated sorting and conveyor systems, port terminal operating systems, fleet telematics, and vehicle electronic systems. These environments require additional security considerations:

| OT Security Area | Requirement | Key Standards |
|---|---|---|
| **OT asset inventory** | Separate inventory for OT/ICS assets; asset classification including safety-critical designation | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) — supplement with OT asset schema |
| **IT/OT network segmentation** | Strict network segmentation between IT and OT environments; unidirectional gateways where feasible | [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md) — supplement with OT segmentation controls |
| **OT patch management** | Modified patch management considering OT availability requirements; vendor-approved patches; extended testing cycles | Supplement SCA standard with OT patching procedure |
| **OT incident response** | Separate or integrated incident response procedures accounting for OT safety implications | Supplement [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) with OT safety overlay |
| **Supply chain for OT** | Security assessment of OT vendors; software integrity verification | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) — supplement with OT vendor criteria |

**Applicable OT standards:**
- IEC 62443 (Industrial Automation and Control Systems Security) — primary OT security standard
- NIST SP 800-82 Rev 3 — Guide to OT Security
- CPNI / NCSC — Operational Technology Security guidance (UK)
- CISA ICS-CERT guidance (US)

---

## Connected and Automated Vehicles

For organisations operating or managing connected vehicle fleets:

| Obligation | Standard / Regulation | Scope |
|---|---|---|
| Cybersecurity Management System (CSMS) | UNECE WP.29 / UN Regulation 155 | New vehicle type approvals in participating markets (EU, UK, Japan, Korea, others); effective for new types 2022; all new vehicles 2024 |
| Software Update Management System (SUMS) | UNECE WP.29 / UN Regulation 156 | As above |
| Vehicle cybersecurity engineering | ISO/SAE 21434 | Vehicle OEMs; Tier 1/2 suppliers |
| Fleet telematics data protection | UK GDPR; GDPR | Processing location and driver data from fleet telematics |

---

## Gap Analysis: Core Library vs. Transportation Requirements

| Gap Area | Applicable Regulation | Action Required |
|---|---|---|
| TSA cybersecurity incident reporting to CISA (24-hour) | TSA Security Directives; CIRCIA | Supplement [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) with CISA reporting runbook |
| NIS 2 incident notification templates and reporting to national CSIRT | EU NIS 2 Art 23 | Create NIS 2 incident notification templates per Member State |
| CAF self-assessment procedure | UK CAA CAP 1753 | Create CAF self-assessment procedure aligned to CAP 1753 |
| IMO ISM Code cyber annex | IMO MSC-FAL.1/Circ.3 | Create ISM Code cyber risk management annex (maritime operators) |
| OT asset inventory and segmentation standards | IEC 62443; NIST SP 800-82 | Supplement asset register and security standards with OT-specific requirements |
| OT incident response procedure | IEC 62443; TSA Directives | Supplement incident response procedure with OT safety considerations |
| UNECE R155 CSMS documentation | UNECE WP.29 R155 | Create CSMS documentation framework (vehicle fleet operators/manufacturers) |
| HMRC CDS API compliance | HMRC CDS | Verify customs declaration systems are CDS-compliant; maintain API access credentials |
| CIRCIA cyber incident reporting procedure | CIRCIA; TSA | Create CIRCIA-compliant reporting procedure for US critical infrastructure |
| Aviation cybersecurity programme | ICAO Doc 10055; CAA CAP 1753 | Create aviation cybersecurity programme document (aviation operators) |

---

## Trade Compliance and Customs Security Integration

The transportation and logistics sector is the primary sector affected by trusted-trader and trade compliance programme requirements. The following documents in the core GRC library provide detailed compliance controls:

| Programme | Documents |
|---|---|
| CTPAT (US) | [`compliance/register-ctpat-compliance-controls.md`](register-ctpat-compliance-controls.md); [`supply-chain/register-ctpat-compliance-controls.md`](../supply-chain/register-ctpat-compliance-controls.md) |
| AEO-S (UK) | [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md); [`compliance/procedure-aeo-it-self-assessment.md`](procedure-aeo-it-self-assessment.md) |
| PIP (Canada) | [`compliance/register-pip-compliance-controls.md`](register-pip-compliance-controls.md) |
| BASC (Latin America) | [`compliance/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md); [`compliance/register-basc-it-compliance-kpis.md`](register-basc-it-compliance-kpis.md); [`compliance/policy-basc.md`](policy-basc.md) |
| All programmes — alignment matrix | [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md) |
| Trade compliance gap assessment | [`compliance/template-trade-compliance-gap-assessment.md`](template-trade-compliance-gap-assessment.md) |

---

## Priority Implementation Sequence

For transportation and logistics organisations building sector-specific GRC compliance:

1. **Immediate (core baseline):**
   - Confirm CTPAT / AEO-S / PIP / BASC certification status and gap-fill using existing compliance domain documents
   - Assess NIS 2 applicability and determine entity classification (essential / important)
   - Identify applicable TSA Security Directives or IMO obligations

2. **Within 90 days:**
   - Complete NIS 2 cybersecurity risk management gap assessment
   - Establish CISA / national CSIRT incident reporting procedure
   - OT asset inventory for logistics automation or vessel systems

3. **Within 12 months:**
   - Complete NIS 2 compliance programme
   - Annual trade compliance programme assessments (CTPAT profile update; AEO-S self-assessment)
   - OT security programme aligned to IEC 62443

---

**End of Document**
