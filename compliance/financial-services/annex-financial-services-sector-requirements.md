# Financial Services Sector GRC Requirements Annex

**Document Title:** Financial Services Sector GRC Requirements Annex\
**Document Type:** Annex\
**Version:** 1.0.9\
**Date:** 2026-07-12\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`compliance/register-compliance-obligations-template.md`](../register-compliance-obligations-template.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material regulatory change in applicable jurisdictions\
**Repository Path:** [`compliance/financial-services/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex identifies the additional GRC obligations that apply to organizations operating in or adjacent to the financial services sector. It maps applicable regulatory frameworks to the core GRC library controls and identifies gap areas requiring sector-specific supplementation.

This annex applies where an organization:
- Is a regulated financial institution (bank, insurer, investment firm, payment institution, e-money institution)
- Provides technology or operational services to regulated financial institutions as a critical third party
- Handles payment card data (triggering PCI DSS obligations regardless of sector)
- Is subject to anti-money laundering obligations by virtue of its business activities

---

## Regulatory landscape overview

### European union

| Regulation / Directive | Scope | Effective |
|---|---|---|
| **DORA**: Digital Operational Resilience Act (Regulation (EU) 2022/2554) | Financial entities and critical ICT third-party service providers (CTPPs) operating in or serving the EU financial sector | 2025-01-17 |
| **NIS 2 Directive** (Directive 2022/2555) | Financial sector entities classified as essential entities | October 2024 (transposition) |
| **GDPR** | All personal data processing | May 2018 |
| **PSD2 / PSD3** | Payment services providers; open banking | Ongoing |
| **AML Directives (AMLD6)** | Financial institutions; certain high-value goods dealers | Ongoing |
| **MiFID II / MiFIR** | Investment firms; trading venues | Ongoing |
| **Basel III / CRR3** | Credit institutions; capital and operational risk | 2025 onwards |

### United kingdom

| Regulation / Guidance | Authority | Scope |
|---|---|---|
| **FCA Operational Resilience Policy Statement (PS21/3)** | Financial Conduct Authority | FCA-authorized firms; Important Business Services |
| **PRA Supervisory Statement SS1/21** | Prudential Regulation Authority | PRA-regulated firms; operational resilience |
| **FCA/PRA Cyber and Technology Resilience** | FCA / PRA | Firms' technology risk governance and outsourcing |
| **UK GDPR** | ICO | All firms processing personal data in the UK |
| **Money Laundering Regulations 2017 (as amended)** | HMRC; FCA | All regulated financial sector firms |
| **Critical Third Parties (CTPs) regime** (FSMA 2023; PS24/16 joint BoE/PRA/FCA, November 2024) | Bank of England; FCA; PRA | Designated critical technology providers to UK financial sector |
| **SYSC: Senior Management Arrangements** | FCA Handbook | Senior Manager functions; accountability |

### Canada

| Regulation / Guideline | Authority | Scope |
|---|---|---|
| **OSFI Guideline B-13: Technology and Cyber Risk Management** | Office of the Superintendent of Financial Institutions | Federally regulated financial institutions (FRFIs) |
| **OSFI Guideline B-10: Third-Party Risk Management** | OSFI | FRFIs |
| **OSFI Guideline B-7: Derivatives** | OSFI | FRFIs |
| **FINTRAC**: Proceeds of Crime (Money Laundering) and Terrorist Financing Act | FINTRAC | All reporting entities under the Act |
| **PIPEDA** | OPC / Privacy Commissioner | All organizations processing Canadians' personal data |
| **CSA (investment) obligations** | Canadian Securities Administrators | Federally registered investment dealers |

### United states

| Regulation / Framework | Authority | Scope |
|---|---|---|
| **GLBA**: Gramm-Leach-Bliley Act Safeguards Rule (16 CFR Part 314) | FTC; federal banking regulators | Financial institutions; those significantly engaged in financial activities |
| **23 NYCRR 500**: NY DFS Cybersecurity Regulation | NY Department of Financial Services | Covered entities with NY DFS licence or charter |
| **FFIEC IT Examination Handbook** | FFIEC | US banks and credit unions |
| **FFIEC Cybersecurity Assessment Tool (CAT)** | FFIEC | US depository institutions |
| **Interagency safety-and-soundness, information-security, and third-party-risk expectations** | Office of the Comptroller of the Currency (OCC); Federal Reserve Board (FRB); Federal Deposit Insurance Corporation (FDIC) | Federally supervised banks and holding companies; technology risk, information security, and third-party risk |
| **SOX**: Sarbanes-Oxley Act Section 302/404 | SEC; PCAOB | Publicly listed companies in the US |
| **Bank Secrecy Act / AML obligations** | FinCEN | Banks; money services businesses; broker-dealers |
| **PCI DSS v4.0.1** | PCI SSC | Any organization storing, processing, or transmitting payment card data |

### Asia-pacific

| Regulation / Guidance | Authority | Scope |
|---|---|---|
| **Technology Risk Management (TRM) Guidelines; Notice on Cyber Hygiene** | Monetary Authority of Singapore (MAS) | Financial institutions regulated in Singapore; technology and cyber risk management |
| **Prudential Standard CPS 234 (Information Security); CPS 230 (Operational Risk Management)** | Australian Prudential Regulation Authority (APRA) | APRA-regulated entities (banks, insurers, superannuation); information security and operational resilience |
| **Supervisory Policy Manual: technology and operational risk modules** | Hong Kong Monetary Authority (HKMA) | Authorized institutions in Hong Kong; technology risk and operational resilience |
| **Guidelines on system risk and cybersecurity for financial institutions** | Japan Financial Services Agency (JFSA / FSA) | Financial institutions supervised in Japan; system risk and cybersecurity |

### Switzerland

| Regulation / Guidance | Authority | Scope |
|---|---|---|
| **Circular on operational risks and resilience** | Swiss Financial Market Supervisory Authority (FINMA) | FINMA-supervised banks, insurers, and financial institutions; operational risk and resilience |

> **Note:** The instruments named in the Asia-Pacific and Switzerland subsections are named structurally to map the regulators and their supervisory domains. The specific current instrument titles, versions, and effective dates change over time and are confirmed by the adopting organization against each regulator's current published requirements; this annex does not pin or reproduce them.

### Global / cross-jurisdictional

| Framework | Body | Scope |
|---|---|---|
| **FATF Recommendations** | Financial Action Task Force | AML/CFT obligations globally |
| **SWIFT Customer Security Programme (CSP)** | SWIFT | All SWIFT members and users |
| **Basel Operational Resilience Principles** | Basel Committee on Banking Supervision (BCBS) | Banks and supervisors globally |
| **CPMI-IOSCO Principles for FMIs** | BIS / IOSCO | Financial market infrastructures |

---

## Key regulatory requirements

### DORA: digital operational resilience act (EU)

DORA applies to approximately 22 categories of EU financial entities and to ICT third-party service providers designated as Critical (CTPPs). Key requirements:

| DORA Pillar | Requirement | GRC Library Mapping |
|---|---|---|
| **ICT Risk Management (Arts 5 to 16)** | Documented ICT risk management framework; asset inventory; protection and prevention measures; detection; response and recovery; communication | [`security/policy-information-security.md`](../../security/policy-information-security.md); [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md); [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md); [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md) |
| **ICT Incident Classification and Reporting (Arts 17 to 23)** | Classify incidents as major or non-major; report major ICT incidents to competent authority with an initial notification within 4 hours of classification as major and no later than 24 hours from awareness, an intermediate report within 72 hours of the initial notification, and a final report no later than one month after the intermediate report (windows per the RTS in Delegated Reg (EU) 2025/301) | [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md); [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md): supplement with DORA reporting templates |
| **Digital Operational Resilience Testing (Arts 24 to 27)** | Threat-Led Penetration Testing (TLPT) every 3 years for significant entities; regular vulnerability assessments and scenario-based testing | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md): supplement with TLPT protocol; penetration test programme |
| **Third-Party ICT Risk (Arts 28 to 44)** | Documented ICT third-party risk management strategy; due diligence; contractual provisions; exit strategies; CTPP oversight framework | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md); [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md); [`supply-chain/standard-cloud-exit-and-data-portability.md`](../../supply-chain/standard-cloud-exit-and-data-portability.md) |
| **Information Sharing (Art 45)** | Voluntary cyber threat intelligence sharing arrangements | Supplement with threat intelligence sharing policy |

**DORA Contract Provisions (Art 30):** ICT contracts with ICT third-party providers must include:
- Full service description and SLAs
- Data location and processing provisions
- Incident notification obligations
- Cooperation with supervisory authority
- Exit and termination provisions; reversibility
- Audit rights including supervisory authority access

### UK FCA/PRA operational resilience

| Requirement | Core Obligation | GRC Library Mapping |
|---|---|---|
| **Important Business Services identification** | Map all services important to customers and financial stability | [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md): supplement with Important Business Services register |
| **Impact tolerances** | Set maximum tolerable disruption for each Important Business Service (time and quality thresholds) | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md); [`resilience/procedure-business-impact-analysis.md`](../../resilience/procedure-business-impact-analysis.md) |
| **Mapping and testing** | Map people, processes, technology, facilities, and information supporting each service; stress test against disruption scenarios | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md); [`resilience/procedure-business-impact-analysis.md`](../../resilience/procedure-business-impact-analysis.md) |
| **Self-assessment** | Annual self-assessment of operational resilience capability against impact tolerances | [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](../logistics/procedure-aeo-united-kingdom-self-assessment.md): adapt template |

### OSFI b-13 (canada: frfis)

OSFI B-13 applies to all federally regulated financial institutions in Canada. Key outcomes:

| B-13 Domain | Outcome Required | GRC Library Mapping |
|---|---|---|
| **Governance** | Technology and cyber risk oversight at Board level; CRO accountability; technology risk appetite | [`risk/policy-enterprise-governance-and-risk-management.md`](../../risk/policy-enterprise-governance-and-risk-management.md); [`risk/template-risk-appetite-statement.md`](../../risk/template-risk-appetite-statement.md) |
| **Technology Asset Management** | Complete, accurate technology asset inventory | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) |
| **Technology and Cyber Risk Management** | Risk identification, assessment, treatment aligned to enterprise framework | [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md); [`risk/procedure-risk-assessment-methodology.md`](../../risk/procedure-risk-assessment-methodology.md) |
| **Cyber Resilience** | Cyber resilience strategy; incident response; threat intelligence; recovery capability | [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md); [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) |
| **Third-Party Technology Risk** | Technology risk management for all third-party technology arrangements | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md); [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) |

### NY DFS 23 NYCRR 500 (US)

| Requirement | Detail | GRC Library Mapping |
|---|---|---|
| **CISO appointment** | Qualified CISO; annual report to Board | Role definition in security domain |
| **Penetration testing** | Annual penetration test; bi-annual vulnerability assessment | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md): supplement with pen test programme |
| **Multi-factor authentication** | MFA required for access to non-public information systems | [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) |
| **Encryption** | Encryption of non-public information in transit and at rest | [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md) |
| **Incident notification** | Notice to NYDFS within 72 hours of determining a Cybersecurity Event occurred | [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md): supplement with NYDFS notification runbook |
| **Cybersecurity policy** | Documented policy covering all 15 required areas | [`security/policy-information-security.md`](../../security/policy-information-security.md): verify coverage of all 15 areas |
| **Access controls** | Privileged access management; periodic review | [`security/procedure-access-control.md`](../../security/procedure-access-control.md); [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) |
| **Third-party service provider policy** | Written policy governing third-party security | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md) |

### PCI DSS v4.0.1

PCI DSS applies to any organization that stores, processes, or transmits payment card data. Key requirements across the 12 PCI DSS requirements:

| PCI DSS Requirement Group | Core Obligation | GRC Library Mapping |
|---|---|---|
| **Req 1 to 2: Network Security** | Firewalls; secure configurations; no vendor defaults | [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md) |
| **Req 3 to 4: Protect Cardholder Data** | Encryption of stored PAN; TLS in transit | [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md) |
| **Req 5 to 6: Vulnerability Management** | Antivirus; secure development; patch management | [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md); [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) |
| **Req 7 to 8: Access Control** | Least privilege; unique user IDs; MFA | [`security/procedure-access-control.md`](../../security/procedure-access-control.md); [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) |
| **Req 9: Physical Security** | Physical access controls to cardholder data environments | Physical security controls |
| **Req 10: Logging and Monitoring** | Audit logs; log review; SIEM | [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) |
| **Req 11: Security Testing** | Penetration testing; internal and external vulnerability scans | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) |
| **Req 12: Security Policy** | Information security policy; risk assessment; incident response | Core GRC library policies |

**PCI DSS v4.0.1 new requirements (effective 2025):**
- Targeted risk analysis for customized approach controls
- Multi-factor authentication expanded to all CDE access
- Phishing-resistant MFA for interactive logins
- Ecommerce scripts (payment page scripts) monitored for changes

### AML / CFT requirements

For organizations subject to AML obligations (banks, money service businesses, certain freight/customs operators under FATF Recommendation 22):

| Obligation | Requirement | GRC Library Supplement Needed |
|---|---|---|
| **Customer Due Diligence (CDD)** | Verify customer identity; assess business purpose; identify beneficial owners | Supplement: CDD procedure |
| **Enhanced Due Diligence (EDD)** | Enhanced measures for high-risk customers, PEPs, high-risk countries | Supplement: EDD procedure |
| **Transaction Monitoring** | Monitor transactions for suspicious activity | Supplement: Transaction monitoring programme |
| **Suspicious Activity Reporting (SAR)** | File SARs with FINTRAC / FinCEN / NCA within prescribed timelines | Supplement: SAR filing procedure |
| **Record Retention** | AML records retained for 5 to 7 years depending on jurisdiction | [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md): verify AML retention periods |
| **Staff Training** | AML training for all relevant staff | [`governance/framework-human-capital-and-ethical-conduct.md`](../../governance/framework-human-capital-and-ethical-conduct.md): ensure that AML training is included |

---

## Gap analysis: core library vs. financial services requirements

The following controls are required by financial services regulations but are not fully addressed by the core GRC library. Supplement with sector-specific procedures as needed.

| Gap Area | Applicable Regulation(s) | Action Required |
|---|---|---|
| DORA ICT incident reporting templates and EIOPA/EBA/ESMA regulatory reporting | DORA Arts 19 to 23 | Create DORA incident reporting procedure and templates |
| Important Business Services register | UK FCA/PRA PS21/3 | Create Important Business Services register and impact tolerance documentation |
| TLPT (Threat-Led Penetration Testing) protocol | DORA Art 26; CBEST (UK) | Create TLPT governance procedure |
| DORA third-party ICT provider contract register | DORA Art 28 | Supplement supplier register with DORA-specific fields |
| AML / CFT policy, CDD, EDD, SAR procedures | FATF; BSA; AMLD6; MLRs 2017 | Create AML programme documents |
| GLBA Safeguards Rule annual report | GLBA | Create annual GLBA compliance attestation procedure |
| PCI DSS targeted risk analysis procedure | PCI DSS v4.0.1 Req 12.3 | Create PCI DSS risk analysis procedure |
| SOX IT General Controls documentation | SOX Section 404; PCAOB AS 2201 | Create ITGC documentation framework |
| OSFI B-13 Board-level technology risk reporting | OSFI B-13 | Create technology risk Board report template |
| SWIFT CSP annual attestation | SWIFT CSP | Create SWIFT CSP attestation procedure |

---

## Priority implementation sequence

For organizations entering the financial services sector or achieving DORA compliance:

1. **Immediate (before go-live or regulatory deadline):**
 - Establish ICT risk management framework (DORA / OSFI B-13 / GLBA baseline)
 - Identify and document Important Business Services and impact tolerances
 - Execute PCI DSS scoping and initiate Qualified Security Assessor (QSA) engagement
 - Establish AML programme if obligated

2. **Within 90 days:**
 - Complete DORA third-party ICT provider inventory and contractual uplift
 - Establish DORA incident reporting workflow
 - Complete NY DFS / GLBA policy coverage verification

3. **Within 12 months:**
 - Complete first TLPT or equivalent penetration testing cycle
 - Achieve PCI DSS certification (if card data in scope)
 - Complete OSFI B-13 / FCA/PRA self-assessment

---

**End of Document**
