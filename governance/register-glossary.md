# Glossary and Acronym Index

**Document Title:** Glossary and Acronym Index\
**Document Type:** Register\
**Version:** 1.4.26\
**Date:** 2026-11-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon introduction of new acronyms or domain terms\
**Repository Path:** [`governance/register-glossary.md`](register-glossary.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register resolves the **acronyms and external-domain terms** used throughout the GRC Documentation Library, primarily standards, regulations, frameworks, regulators, sector programmes, and well-known technical concepts. Where a term has a primary canonical document in the library, that document is cited.

The glossary is the single source of truth for acronym expansion. New documents should use a term's first occurrence to introduce the acronym (e.g., "Authorized Economic Operator (AEO)"), then use the acronym thereafter. The expansion shown here is the canonical form.

### Scope distinction

- This register (**Glossary and Acronym Index**) holds acronym expansions and brief term definitions, mostly for **external** terms (regulations, standards, frameworks, regulators, sector programmes, technical concepts).
- The companion [`register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md) (**Key Terms and Definitions Register**) defines **library-internal** GRC concepts (Audit, Authorize, Control, Owner roles, Exception, etc.): terms with specific meaning within the library's governance vocabulary that may differ from generic usage.

When in doubt: external term or acronym → this register. Internal governance concept → the key terms register.

---

## Convention

- Acronyms in **bold**.
- Expansion follows the acronym.
- A brief definition is provided where the expansion alone is insufficient.
- Where multiple expansions exist for the same acronym, the one used in this library is specified.
- "See" cross-references point to the canonical library document for the term.
- Rows in each section are sorted by term, ignoring case, character by character: a space or punctuation mark sorts before a digit, and a digit before a letter (so I&S precedes IACS, and SL-A precedes SLA).

---

## 0-9

| Term | Expansion / definition |
| --- | --- |
| **3PL** | Third-party logistics provider. An organization providing outsourced logistics services (transportation, warehousing, distribution, freight management) to shippers. |

## A

| Term | Expansion / definition |
| --- | --- |
| **ADMT** | Automated Decision-Making Technology. The organizing concept of Colorado's re-enacted AI statute (SB 26-189): technology that materially influences a consequential decision. See [`ai/jurisdictions/annex-ai-us-colorado.md`](../ai/jurisdictions/annex-ai-us-colorado.md). The same acronym is also used for California's CCPA regulations on automated decision-making technology, whose canonical home is [`ai/jurisdictions/annex-ai-us-california.md`](../ai/jurisdictions/annex-ai-us-california.md) (the US privacy annex keeps a brief privacy-context summary that points there). |
| **AEAD** | Authenticated Encryption with Associated Data. Symmetric encryption mode providing confidentiality, integrity, and authenticity in a single primitive. Canonical examples: AES-GCM (NIST SP 800-38D), AES-CCM, ChaCha20-Poly1305 (RFC 8439). |
| **AEO** | Authorized Economic Operator. The operator, not the programme: the WCO SAFE Framework (2025 edition) defines an AEO as "a party involved in the international movement of goods in whatever function that has been approved by or on behalf of a national Customs administration as complying with WCO or equivalent supply chain security standards". National customs authorities approve operators under national or regional Customs union AEO programmes (the Framework's Section VII, 2.1), which grant trade facilitation benefits. The Framework itself is not a programme: it provides baseline technical guidance for the implementation of AEO programmes at the global level and is designed to serve as a starting point for national AEO programme implementation. |
| **AEO-S** | Authorized Economic Operator Security and Safety. The UK AEO authorization for security and safety, which HMRC's criteria write as AEOS (UK HMRC AEO security and safety criteria handbook, §11.1). |
| **AI** | Artificial Intelligence. |
| **AI Act** | The EU Artificial Intelligence Act, Regulation (EU) 2024/1689, laying down harmonized rules on artificial intelligence. See [`ai/jurisdictions/annex-ai-european-union.md`](../ai/jurisdictions/annex-ai-european-union.md). |
| **AICM** | AI Controls Matrix. Cloud Security Alliance (CSA) framework of AI-specific controls. |
| **AIDA** | Artificial Intelligence and Data Act. Canadian federal legislation introduced in Bill C-27 (which lapsed at the January 2025 prorogation; per a June 2025 ministerial statement not held in the reference base, AIDA is reported not to return in its original form; confirm directly). Distinct from "AI Data Act" in some other contexts; the library uses AIDA for the Canadian Artificial Intelligence and Data Act only. <!-- ref-absence: AIDA ministerial statement --> |
| **AIGC** | AI Governance Council. Cross-functional governance forum defined in the library's AI charter. |
| **AIMS** | Artificial Intelligence Management System (per ISO/IEC 42001:2023). |
| **AIQT** | Accuracy, Integrity, Quality, Trust. The library's foundational production principle: the priority ordering (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost. See [`governance/principle-integrity-and-trustworthiness.md`](principle-integrity-and-trustworthiness.md). |
| **AIS** | AI System. A unit of AI capability tracked in the AI System Register. (CSA CCM also uses AIS as Application & Interface Security, the CCM domain covering application-layer controls; the library cites that domain explicitly where used.) |
| **ANPD** | Agência Nacional de Proteção de Dados, formerly the Autoridade Nacional de Proteção de Dados. Brazil's national data protection authority, created by Article 55-A of the LGPD. See [`privacy/jurisdictions/annex-privacy-brazil.md`](../privacy/jurisdictions/annex-privacy-brazil.md). |
| **ASD** | Australian Signals Directorate. Authority for the Australian Information Security Manual (ISM). |
| **ATT** | Australian Trusted Trader. Australia's AEO-equivalent trusted-trader programme. |

## B

| Term | Expansion / definition |
| --- | --- |
| **BAI** | (COBIT 2019) Build, Acquire, and Implement. One of the five COBIT process domains. |
| **BASC** | Business Alliance for Secure Commerce. International private supply-chain security certification, predominantly Latin American, run by the World BASC Organization (WBO), a member-led business organization. See [`compliance/logistics/annex-basc-programme-overview.md`](../compliance/logistics/annex-basc-programme-overview.md). |
| **BC** | Business Continuity. Appears in the BC/DR (Business Continuity / Disaster Recovery) and BC/CM (Business Continuity / Crisis Management) compounds. |
| **BCM** | Business Continuity Manager. Role accountable for business continuity programme execution. |
| **BCP** | Business Continuity Plan. |
| **BIA** | Business Impact Analysis. |
| **BMS** | Building Management System. A category of OT covering automated control of HVAC, lighting, fire/life-safety, physical access control, and other facility systems. Adjacent to but distinct from ICS. |

## C

| Term | Expansion / definition |
| --- | --- |
| **CAPA** | Corrective and Preventive Action. See [`compliance/procedure-capa.md`](../compliance/procedure-capa.md). |
| **CBP** | U.S. Customs and Border Protection. Administers CTPAT. |
| **CBSA** | Canada Border Services Agency. Administers PIP. |
| **CCM** | Cloud Controls Matrix. Cloud Security Alliance (CSA) framework. |
| **CCO** | Chief Compliance Officer. |
| **CCPA** | California Consumer Privacy Act. |
| **CDO** | Chief Data Officer. |
| **CEK** | (CSA CCM domain) Cryptography, Encryption & Key Management. |
| **CIA** | Confidentiality, Integrity, Availability. The classic information-security triad. |
| **CIAM** | Customer Identity and Access Management. |
| **CIIO** | Critical Information Infrastructure Operator. Chinese-law category under the Cybersecurity Law of China, which leaves the specific scope of critical information infrastructure to the State Council (Cybersecurity Law Article 33, in the amended numbering in force 1 January 2026; English rendering of the Chinese text, which is authoritative) and does not say who identifies a particular operator as a CIIO; an adopter confirms its CIIO status directly. Triggers mandatory CAC Security Assessment for outbound personal information transfers under PIPL Article 38 and a domestic-storage default under PIPL Article 40. |
| **CIO** | Chief Information Officer. |
| **CIP** | Critical Infrastructure Protection. NERC CIP is the canonical reference for North American electricity reliability. |
| **CISO** | Chief Information Security Officer. |
| **CM** | Crisis Management (in the BC/CM business-continuity-and-crisis-management pairing). |
| **CMS** | Compliance Management System (ISO 37301:2021-aligned). |
| **COBIT** | Control Objectives for Information and Related Technologies. ISACA framework. |
| **CPPA** | Consumer Privacy Protection Act (Canada); proposed in Bill C-27, which lapsed in 2025 (not in force). Distinct from CCPA and from the California Privacy Protection Agency. |
| **CPRA** | California Privacy Rights Act. Amends and expands the CCPA; operative since 2023. |
| **CRO** | Chief Risk Officer. |
| **CSA** | Cloud Security Alliance. |
| **CSP** | Cloud Service Provider. (In financial-services contexts, CSP also denotes SWIFT Customer Security Programme; that sector annex uses the SWIFT meaning explicitly.) |
| **CSV** | Comma-Separated Values (file format). |
| **CTO** | Chief Technology Officer. |
| **CTPAT** | Customs-Trade Partnership Against Terrorism. U.S. CBP voluntary trusted-trader programme. See [`compliance/logistics/register-ctpat-united-states-it-controls.md`](../compliance/logistics/register-ctpat-united-states-it-controls.md). |
| **CVE** | Common Vulnerabilities and Exposures. Vulnerability identifier maintained by the MITRE CVE Program; NIST publishes the related National Vulnerability Database (NVD), which builds on CVE. |

## D

| Term | Expansion / definition |
| --- | --- |
| **DCS** | Two distinct meanings disambiguated by context: (1) (CSA CCM domain) Datacenter Security; (2) (OT) Distributed Control System. The library uses CCM-DCS for the cloud-control-matrix domain and OT-DCS or "Distributed Control System" spelled out where the OT meaning is intended. |
| **DLP** | Data Loss Prevention. |
| **DORA** | Digital Operational Resilience Act (EU). Financial-services regulation. See [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md). |
| **DPA** | Data Processing Agreement. |
| **DPIA** | Data Protection Impact Assessment (GDPR Art 35). |
| **DPO** | Data Protection Officer. Canonical privacy-lead role in the library, following the statutorily-mandated title in GDPR Article 37, India DPDP Act 2023 §10, Malaysia PDPA (as amended), and similar regimes. LGPD Article 41 does not use that title; it requires the controller to appoint an *encarregado pelo tratamento de dados pessoais*, the equivalent role that this library maps to DPO. See [`register-role-authority.md`](register-role-authority.md) for the role definition and adopter-customization guidance. The North American variant "Chief Privacy Officer (CPO)" is an acceptable adopter substitution; some adopters maintain both DPO and CPO as distinct roles. |
| **DR** | Disaster Recovery. |
| **DSAR** | Data Subject Access Request. |
| **DSP** | (CSA CCM domain) Data Security and Privacy Lifecycle Management. Distinct from DCS (Datacenter Security) in CCM v4.1. |
| **DSPT** | Data Security and Protection Toolkit (UK NHS). |
| **DSR** | Data Subject Request. Broader than DSAR; includes erasure, rectification, portability, etc. |

## E

| Term | Expansion / definition |
| --- | --- |
| **EBA** | European Banking Authority. |
| **EDI** | Electronic Data Interchange. |
| **EECC** | European Electronic Communications Code. |
| **eIDAS** | electronic IDentification, Authentication and trust Services. EU Regulation (EU) No 910/2014 as amended by Regulation (EU) 2024/1183 ("eIDAS2"), covering electronic identification, trust services, and the EU Digital Identity Wallet. See [`compliance/public-sector/annex-eidas-requirements.md`](../compliance/public-sector/annex-eidas-requirements.md). |
| **EIOPA** | European Insurance and Occupational Pensions Authority. |
| **ELT** | Executive Leadership Team. |
| **ERC** | Enterprise Risk Committee. Executive-level forum delegated by the Board Risk Committee. See [`governance/register-role-authority.md`](register-role-authority.md). |
| **ERM** | Enterprise Risk Management. |
| **ESG** | Environmental, Social, and Governance. |
| **ESMA** | European Securities and Markets Authority. |

## F

| Term | Expansion / definition |
| --- | --- |
| **FedRAMP** | Federal Risk and Authorization Management Program. U.S. federal cloud-service authorization. See [`compliance/public-sector/annex-fedramp-requirements.md`](../compliance/public-sector/annex-fedramp-requirements.md). |
| **FERC** | Federal Energy Regulatory Commission (U.S.). |
| **FMCSA** | Federal Motor Carrier Safety Administration (U.S.). |
| **FMI** | Financial market infrastructure. Systems for clearing, settlement, and recording of payments, securities, and derivatives (payment systems, central securities depositories, securities settlement systems, central counterparties, trade repositories), per the CPMI-IOSCO Principles for Financial Market Infrastructures. |
| **FSA** | Financial Services Agency (Japan). |

## G

| Term | Expansion / definition |
| --- | --- |
| **GDPR** | General Data Protection Regulation (EU). |
| **GICS** | Global Industry Classification Standard. |
| **Governance Library Maintainer** | Meta-role, not a named individual: the party accountable for the library's own integrity (the maintainer of this repository), recorded as the Approving Authority on the majority of the corpus. It is not the sole role holder: per-document Owner and Approving-Authority values are otherwise distributed across the domain roles the content addresses (CISO, DPO, CIO, and others; CIO is the second-most-common approving authority and is not an anomaly). An adopting organization substitutes its own accountable owner when it adopts an artefact. |
| **GRC** | Governance, Risk, and Compliance. |

## H

| Term | Expansion / definition |
| --- | --- |
| **HIPAA** | Health Insurance Portability and Accountability Act (U.S.). |
| **HITECH** | Health Information Technology for Economic and Clinical Health Act (U.S.). |
| **HKDF** | HMAC-based Key Derivation Function. Extract-and-expand key derivation function per RFC 5869. The canonical mechanism for deriving sub-keys from existing high-entropy material (e.g., from an HSM-held master key); not appropriate for deriving keys from passwords (use Argon2id or scrypt for password-based KDFs). |
| **HMI** | Human-Machine Interface. The graphical operator interface to ICS/OT systems, typically running on a workstation that displays process state and accepts operator commands. |
| **HMRC** | His Majesty's Revenue and Customs (UK). Administers UK AEO and AEO-S. |
| **HSM** | Hardware Security Module. |

## I

| Term | Expansion / definition |
| --- | --- |
| **I&S** | (CSA CCM domain) Infrastructure Security. Renamed from the v4.0 IVS (Infrastructure and Virtualization Security) domain in CCM v4.1.0. |
| **IACS** | Industrial Automation and Control Systems. The scope term used by IEC 62443. A subset of OT focused on industrial automation. |
| **IAM** | Identity and Access Management. |
| **ICAO** | International Civil Aviation Organization. |
| **ICS** | Industrial Control System. A category within OT covering systems that control industrial processes (manufacturing, energy generation, water treatment, transportation). Common ICS types include SCADA, DCS (Distributed Control System), and PLC-based local control. |
| **ICT** | Information and Communications Technology. |
| **IDS** | Intrusion Detection System. |
| **IEC** | International Electrotechnical Commission. Co-publishes ISO/IEC standards. |
| **IMO** | International Maritime Organization. |
| **IPS** | Intrusion Prevention System. |
| **IPY** | (CSA CCM domain) Interoperability & Portability. |
| **ISACA** | Information Systems Audit and Control Association. Publishes COBIT. |
| **ISM** | Information Security Manual (Australia). |
| **ISO** | International Organization for Standardization. |
| **IT/OT convergence** | The progressive integration of Information Technology (IT) and Operational Technology (OT) networks, identities, and management tooling. Drives joint governance, network segmentation discipline, and unified incident response. |
| **ITGC** | Information Technology General Controls (SOX context). |
| **ITSM** | IT Service Management. |
| **IVDR** | In-Vitro Diagnostic Regulation (EU). |

## K

| Term | Expansion / definition |
| --- | --- |
| **KMS** | Key Management Service. |
| **KPI** | Key Performance Indicator. |
| **KRI** | Key Risk Indicator. |

## L

| Term | Expansion / definition |
| --- | --- |
| **LGPD** | Lei Geral de Proteção de Dados Pessoais, Lei nº 13.709/2018 (Brazilian general data protection law), as the ANPD's cookies guide names it (Guia orientativo: Cookies e proteção de dados pessoais, version 1.0, 2022). See [`privacy/jurisdictions/annex-privacy-brazil.md`](../privacy/jurisdictions/annex-privacy-brazil.md). |
| **LLM** | Large Language Model. |
| **LOG** | (CSA CCM domain) Logging and Monitoring. |

## M

| Term | Expansion / definition |
| --- | --- |
| **Marco Civil da Internet** | Brazilian Internet Act, Lei nº 12.965/2014: establishes principles, guarantees, rights and duties for the use of the internet in Brazil (Article 1). See [`privacy/jurisdictions/annex-privacy-brazil.md`](../privacy/jurisdictions/annex-privacy-brazil.md). |
| **MAS** | Monetary Authority of Singapore. |
| **MCP** | Model Context Protocol. Standard interface for AI model tool use; tracked in the library's MCP server register. |
| **MDR** | Medical Device Regulation (EU). |
| **METI** | Ministry of Economy, Trade and Industry (Japan). |
| **MFA** | Multi-Factor Authentication. |
| **MITRE ATLAS** | Adversarial Threat Landscape for AI Systems. MITRE-maintained AI adversary framework. |
| **MITRE ATT&CK** | Adversarial Tactics, Techniques, and Common Knowledge. MITRE-maintained adversary behaviour framework. |
| **ML** | Machine Learning (in AI/ML contexts). Also Most Likely, the central value in three-point (PERT) estimation used in quantitative risk analysis. |
| **MRA** | Mutual Recognition Arrangement (or Agreement) between Customs administrations. The WCO SAFE Framework (2025 edition) describes mutual recognition as "a broad concept whereby an action or decision taken or an authorization that has been properly granted by one Customs administration is recognized and accepted by another Customs administration". Example: the EU-US MRA, a concluded MRA in the WCO AEO Compendium (2020). |
| **MSC** | Minimum Security Criteria (CTPAT). |
| **MTSA** | Maritime Transportation Security Act (U.S.). |

## N

| Term | Expansion / definition |
| --- | --- |
| **NEEC** | Nuevo Esquema de Empresas Certificadas (Mexico), the name the library uses for Mexico's certified-companies trusted-trader scheme; no held source uses the name NEEC. The WCO AEO Compendium (2020) titles Mexico's programme Authorized Economic Operator, and the Mexico-Canada AEO mutual recognition arrangement benefits guide says that in Mexico the programme is known as Authorized Economic Operator; how NEEC relates to that programme is not confirmed by a held source. |
| **NERC** | North American Electric Reliability Corporation. Publishes NERC CIP standards. |
| **nFADP** | New Federal Act on Data Protection (Switzerland). Also referred to as revDSG (revidiertes Datenschutzgesetz). |
| **NIS 2** | EU Directive 2022/2555 on cybersecurity for network and information systems. Successor to NIS Directive 2016/1148. See [`compliance/annex-nis-2-implementation.md`](../compliance/annex-nis-2-implementation.md). |
| **NIST** | National Institute of Standards and Technology (U.S.). |
| **NIST AI RMF** | NIST AI Risk Management Framework. |
| **NIST CSF** | NIST Cybersecurity Framework. |
| **NSG** | Network Security Group (cloud-specific network access control). |

## O

| Term | Expansion / definition |
| --- | --- |
| **OCC** | Office of the Comptroller of the Currency (U.S.). |
| **OEA** | Operador Económico Autorizado (Spanish) or Operador Econômico Autorizado (Portuguese): Authorized Economic Operator. In the WCO AEO Compendium (2020), Bolivia titles its programme Operador Económico Autorizado (OEA), Chile titles its programme AEO Programme (Programa OEA) and El Salvador titles its programme El Salvador Authorized Economic Operator (OEA-SV); Argentina, Colombia, Mexico and Peru title theirs in English as an Authorized Economic Operator programme. In Mexico's entry the spelled-out Spanish term appears only in the address of a SAT web page, and the acronym OEA once, in its list of benefits (the assignment of an OEA specialist). Brazil's programme guide (Receita Federal do Brasil) names its programme the Programa Brasileiro de OEA. No other programme title in the Compendium uses the term. |
| **OECD** | Organisation for Economic Co-operation and Development. Publishes the OECD AI Principles. |
| **OSFI** | Office of the Superintendent of Financial Institutions (Canada). |
| **OT** | Operational Technology. Hardware and software that detects or causes change through direct monitoring and/or control of physical devices, processes, and events. Distinct from Information Technology (IT) by its real-world physical impact, safety implications, and typically longer asset lifecycles. Includes ICS, SCADA, DCS, PLCs, BMS, and other operational control systems. |
| **OWASP** | Open Worldwide Application Security Project (formerly Open Web Application Security Project). Publishes OWASP Top 10, OWASP LLM Top 10. |

## P

| Term | Expansion / definition |
| --- | --- |
| **PAM** | Privileged Access Management. |
| **PCI DSS** | Payment Card Industry Data Security Standard. |
| **PDPA** | Personal Data Protection Act. Used by several jurisdictions including Singapore, Thailand, and Argentina. |
| **PDPL** | Personal Data Protection Law. Used by several jurisdictions including Saudi Arabia, the United Arab Emirates, and Vietnam. |
| **PHIPA** | Personal Health Information Protection Act (Ontario, Canada). |
| **PIA** | Privacy Impact Assessment. |
| **PII** | Personally Identifiable Information. |
| **PIM** | Privileged Identity Management. |
| **PIP** | Partners in Protection (Canada). CBSA trusted-trader programme. See [`compliance/logistics/register-pip-canada-controls.md`](../compliance/logistics/register-pip-canada-controls.md). |
| **PIPEDA** | Personal Information Protection and Electronic Documents Act (Canada). The in-force federal private-sector privacy law; the proposed CPPA (Bill C-27) that would have replaced it lapsed in 2025. |
| **PIPL** | Personal Information Protection Law (China). |
| **PKI** | Public Key Infrastructure. |
| **PLC** | Programmable Logic Controller. An industrial computer used in OT/ICS to automate electromechanical processes. PLCs are foundational components of most ICS deployments. |
| **PoPIA** | Protection of Personal Information Act (South Africa). |
| **PPC** | Personal Information Protection Commission (Japan). |
| **PQC** | Post-Quantum Cryptography. |
| **PRA** | Prudential Regulation Authority (UK). |
| **PSPF** | Protective Security Policy Framework (Australia). |
| **Purdue model** | Reference architecture for ICS network segmentation, originally developed at Purdue University. Defines hierarchical zones: Level 0 (physical processes), Level 1 (basic control), Level 2 (area supervisory control), Level 3 (site operations), Level 3.5 (DMZ between OT and IT), Level 4 (site business network), Level 5 (enterprise IT). Foundational to IEC 62443 zone-and-conduit thinking. |

## R

| Term | Expansion / definition |
| --- | --- |
| **RACI** | Responsible, Accountable, Consulted, Informed. Role-mapping convention. |
| **RBAC** | Role-Based Access Control. |
| **RPO** | Recovery Point Objective. Maximum tolerable data loss measured backward from an incident. |
| **RTO** | Recovery Time Objective. The target time to restore a process, system, or service to an acceptable level. |

## S

| Term | Expansion / definition |
| --- | --- |
| **SaMD** | Software as a Medical Device. |
| **SAML** | Security Assertion Markup Language. |
| **SAST** | Static Application Security Testing. |
| **SBOM** | Software Bill of Materials. |
| **SCA** | Software Composition Analysis. |
| **SCADA** | Supervisory Control and Data Acquisition. A class of ICS used for high-level supervision and control of distributed industrial processes (oil and gas pipelines, electricity grids, water systems, rail networks). |
| **SCC** | Standard Contractual Clauses (GDPR cross-border transfers). |
| **SDLC** | Software Development Lifecycle. |
| **SEC** | U.S. Securities and Exchange Commission. |
| **SES** | Secure Exports Scheme (New Zealand). NZ's trusted-trader programme. |
| **SIEM** | Security Information and Event Management. |
| **SIL** | Safety Integrity Level. A safety classification from IEC 61508/IEC 61511 (SIL 1 through SIL 4) measuring the reliability required of a Safety Instrumented System. Distinct from IEC 62443 Security Levels (SL). |
| **SIS** | Safety Instrumented System. An OT/ICS system specifically designed to bring a process to a safe state when defined hazardous conditions are detected. SIS reliability is measured by SIL (Safety Integrity Level). |
| **SL-A** | Security Level Achieved (IEC 62443). The actual security level attained by a deployed zone or component. |
| **SL-C** | Security Level Capability (IEC 62443). The security level a component is capable of supporting when correctly configured. |
| **SL-T** | Security Level Target (IEC 62443). The security level a zone or conduit is required to achieve given its risk profile. SL-T values range from SL 1 (protection against casual or coincidental violation) through SL 4 (protection against intentional violation by skilled, well-resourced adversaries). |
| **SLA** | Service Level Agreement. |
| **SOC** | Security Operations Centre (operational context). Also System and Organization Controls, the AICPA's name for its suite of control examination services, of which SOC 2 is one. The library disambiguates by context. |
| **SOC 2** | System and Organization Controls 2 (AICPA SOC for Service Organizations: Trust Services Criteria): an examination of controls at a service organization relevant to security, availability, processing integrity, confidentiality or privacy. SOC 2 names the examination, not one type of it: a Type 1 examination covers the description of the system and the suitability of the design of controls, and a Type 2 examination also covers the operating effectiveness of those controls (AICPA DC 200, footnote 5). |
| **SOX** | Sarbanes-Oxley Act (U.S.). See [`compliance/financial-services/annex-sox-itgc.md`](../compliance/financial-services/annex-sox-itgc.md). |
| **SP 800-53** | NIST Special Publication 800-53: Security and Privacy Controls. |
| **SP 800-82** | NIST Special Publication 800-82: Guide to Operational Technology (OT) Security. Renamed from "Industrial Control Systems (ICS) Security" in Rev. 3 (2023) to reflect broader OT scope. |
| **SP 800-88** | NIST Special Publication 800-88: Media Sanitization. |
| **SSPL** | Server Side Public License. |
| **STA** | (CSA CCM domain) Supply Chain Management, Transparency, and Accountability. |
| **STP** | Secure Trade Partnership (Singapore). Singapore's trusted-trader programme. STP-Plus is the enhanced tier. |

## T

| Term | Expansion / definition |
| --- | --- |
| **TIA** | Transfer Impact Assessment (GDPR cross-border transfers post-Schrems II); see the [TIA template](../privacy/template-transfer-impact-assessment.md). |
| **TLS** | Transport Layer Security. |
| **TMS** | Transportation Management System. |
| **TPRM** | Third-Party Risk Management. |
| **TRA** | Transfer Risk Assessment (UK GDPR analogue of TIA). |
| **TSA** | Transportation Security Administration (U.S.). |
| **TVM** | (CSA CCM domain) Threat & Vulnerability Management. |

## U

| Term | Expansion / definition |
| --- | --- |
| **UCC** | Union Customs Code (EU). |
| **UEM** | (CSA CCM domain) Universal Endpoint Management. |

## V

| Term | Expansion / definition |
| --- | --- |
| **VEX** | Vulnerability Exploitability eXchange. Standard for declaring vulnerability applicability. |
| **VPN** | Virtual Private Network. |

## W

| Term | Expansion / definition |
| --- | --- |
| **WCO** | World Customs Organization. Publishes the WCO SAFE Framework and the AEO Compendium. |
| **WCO SAFE Framework** | World Customs Organization SAFE Framework of Standards to Secure and Facilitate Global Trade. Provides baseline technical guidance for the implementation of AEO programmes at the global level and is designed to serve as a starting point for national AEO programme implementation. |

## Z

| Term | Expansion / definition |
| --- | --- |
| **ZTNA** | Zero Trust Network Access. |

---

## Document-domain terms

Terms used by the library to classify its own artefacts.

| Term | Definition |
| --- | --- |
| **Annex** | A doctype for sector-specific, jurisdiction-specific, or programme-specific extensions to the core library. Conditional content. |
| **Charter** | A doctype establishing authority, mandate, and accountability for a function or body. |
| **Framework** | A doctype describing the structural relationships between artefacts in a domain. |
| **Guideline** | A doctype expressing recommended (non-mandatory) practice. Uses "should" rather than "must". |
| **Matrix** | A doctype mapping artefacts to external frameworks or to each other. |
| **Plan** | A doctype defining a sequence of activities, milestones, or recovery steps for a specific scenario. |
| **Policy** | A doctype expressing organizational position. Mandatory. Uses "must". |
| **Procedure** | A doctype defining an operational sequence of activities. |
| **Register** | A doctype maintaining a running record (inventory, list, index). |
| **Roadmap** | A doctype defining time-sequenced milestones for a programme. |
| **SOP** | Standard Operating Procedure. A doctype for compact operational guidance, typically in checklist form. |
| **Specification** | A doctype defining requirements for an artefact or process. |
| **Standard** | A doctype expressing required minimum requirements. Mandatory. Uses "must". |
| **Template** | A doctype providing reusable structural patterns for documents the adopter will create. |

---

## Maintenance

- Add new acronyms here when introduced into the library.
- When a term's canonical document changes path, update the cross-reference here.
- Remove acronyms only when no library document uses them.
- Definitions are intentionally brief; consult the linked canonical document for the full treatment.

---

**End of Document**
