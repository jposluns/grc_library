# Annex: Trade and Supply-Chain Continuity Controls

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | Trade and Supply-Chain Continuity Controls |
| **Document Type** | Annex |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Chief Risk Officer (CRO) |
| **Approving Authority** | Chief Information Officer (CIO) |
| **Related Documents** | Framework: Business Continuity & Resilience; Policy: Business Continuity and Disaster Recovery; Standard: Business Continuity & Disaster Recovery; Plan: Business Continuity & Crisis Management; Guideline: Emergency Response & Protective Actions; Procedure: Business Impact Analysis |
| **Classification** | Public – Open Access |
| **Category** | Supply-Chain Resilience / Trade Security |
| **Review Frequency** | Annual or following regulatory or operational change |
| **Repository Path** | /resilience/annex-trade-and-supply-chain-continuity-controls.md |
| **Confidentiality** | None (Public Domain, CC0 License) |

---

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

---

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Risk Officer (CRO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Compliance Officer (CCO) |  |  |
| Chief Legal Officer / General Counsel (CLO/GC) |  |  |

---

## Purpose

This annex defines the controls and requirements for maintaining trade-security and supply-chain continuity under globally recognized programs, including **BASC**, **WCO SAFE**, **ISO 28000**, **PIP (Canada)**, **CTPAT (United States)**, **NEEC (Mexico)**, **OEA (Brazil)**, and **AEO/AEO-S (European Union and United Kingdom)**.  
It ensures that customs, logistics, and supplier-managed processes remain secure, traceable, and operational during disruptions.

---

## Scope

- Applies to all logistics operations, customs transactions, and third-party providers involved in global trade.  
- Encompasses inbound, outbound, and trans-shipment logistics in all operational regions.  
- Incorporates the standards of **BASC**, **PIP**, **CTPAT**, **NEEC**, **OEA**, and **AEO/AEO-S** for international interoperability.  
- Recognizes mutual-recognition arrangements across **Asia-Pacific**, **Middle East**, **Africa**, and **Oceania**, including the **Australian Trusted Trader (ATT)**, **UAE AEO**, **Saudi Customs AEO**, and **EAC AEO Program**.  
- Integrates with enterprise continuity governance and risk-management programs.

---

## Objectives

1. Maintain uninterrupted trade operations during disruptions and emergencies.  
2. Demonstrate compliance with all recognized international customs and trade-security frameworks.  
3. Reduce risk of cargo compromise, customs delay, and data loss across the logistics chain.  
4. Support audit readiness for multi-region customs programs and certification renewals.

---

## Control Domains

| Domain | Control Requirement | Framework Alignment |
|---------|--------------------|--------------------|
| **1. Trade-Security Governance** | Maintain documented trade-security and continuity policies aligned with BASC, PIP, and CTPAT. | BASC §1, ISO 28000 §4, PIP §3, CTPAT §5.1 |
| **2. Cargo Integrity and Inspection** | Verify cargo integrity at transfer points using tamper-evident seals and BASC/CTPAT inspection standards. | BASC §6.1, PIP §5.3, CTPAT §6.1, WCO SAFE Pillar II |
| **3. Personnel Screening and Access Control** | Conduct background checks and access control consistent with BASC, PIP, and NEEC. | BASC §5.1, ISO 28000 §7, PIP §4.2, NEEC §3.4 |
| **4. Data Protection and Customs Information Security** | Secure customs data with encryption, restricted access, and traceable logs. | WCO SAFE §5.3, ISO 27001 A.8, BASC §6.3, PIP §6.2 |
| **5. Supplier and Partner Assurance** | Validate partners against PIP, NEEC, OEA, or equivalent AEO certifications; include continuity clauses in contracts. | BASC §7.2, PIP §8.1, NEEC §6.1, COBIT APO10 |
| **6. Customs Communication and Notification** | Notify customs authorities within 24 hours of trade disruption, breach, or major deviation. | BASC §6.4, WCO SAFE Pillar III, PIP §7.3, CTPAT §7.2 |
| **7. Physical Facility Security** | Maintain perimeter defenses, CCTV, access logs, and lighting per BASC, PIP, and ISO 28000. | BASC §5.2, ISO 28000 §8.2, PIP §5.1, NEEC §4.1 |
| **8. Incident and Breach Response** | Integrate trade incidents with Security Incident Reporting & Escalation and Crisis Management procedures. | BASC §6.5, ISO 22301 §8, PIP §6.4, CTPAT §6.3 |
| **9. Continuity of Trade Operations** | Establish alternate carriers, ports, and customs brokers; test backup communication with customs. | ISO 22301 §8.3, BASC §6.6, PIP §9.1, OEA §3.4 |
| **10. Training and Awareness** | Conduct annual training on trade-security and customs continuity, including BASC, PIP, and CTPAT expectations. | BASC §4.1, ISO 28000 §7.3, PIP §10.2 |
| **11. Supply-Chain Risk Assessment** | Assess route, supplier, and regional risks; maintain risk register with mitigation measures. | ISO 31000 §6, ISO 28000 §6.1, PIP §2.4, NEEC §5.1 |
| **12. Customs Data Recovery and Validation** | Backup customs and cargo records daily; validate recovery through continuity exercises. | BASC §6.7, COBIT DSS04.03, PIP §6.6, CTPAT §9.2 |
| **13. Cross-Border Collaboration** | Support mutual recognition and coordination across AEO, ATT, OEA, and EAC programs. | WCO SAFE Pillar III, PIP §9.4, CTPAT §8.1, ATT §5.3 |
| **14. Metrics and Reporting** | Track compliance audit results, cargo incidents, and customs-communication KPIs. | ISO 22301 §9, COBIT MEA01, PIP §11.1, BASC §8.1 |

---

## Integration with Business Continuity and Disaster Recovery

- Trade, customs, and logistics continuity must be integrated within enterprise BCP and DR frameworks.  
- Customs platforms, cargo-tracking systems, and logistics APIs are classified as **Tier 1 critical systems** for recovery prioritization.  
- BASC, PIP, CTPAT, and NEEC audit results must inform Business Impact Analyses and continuity-test design.  
- Alternate logistics routing, bonded warehouse operations, and emergency customs workflows must be reviewed annually.

---

## Reporting and Oversight

- The **Chief Risk Officer (CRO)**, supported by **Regional BASC, PIP, and NEEC Compliance Officers**, oversees trade-continuity implementation.  
- Quarterly reports submitted to the **Enterprise Risk Committee (ERC)** include:  
  - BASC, PIP, CTPAT, and customs audit summaries with open items.  
  - Results of data recovery, system testing, and partner verification.  
  - Trends in trade incidents and preventive controls.  
  - Supply-chain risk-register updates and mitigations.

---

## Continuous Improvement

Trade and supply-chain incidents, audit findings, and test outcomes feed into improvement programs via:  
- The Corrective and Preventive Action Procedure  
- The Continuous Improvement Register Procedure  
- The Digital Trust Performance Framework  

Corrective actions remain open until validated as effective by audit or test confirmation.

---

## References and Framework Alignment

| Framework | Reference | Objective |
|------------|------------|-----------|
| **BASC International Standard v6 (2023)** | Trade and Customs Security | Defines global trade-security and continuity requirements. |
| **PIP (Canada) – Partners in Protection Program** | Trade-Chain Security Guidelines | Establishes Canadian customs-security and continuity standards. |
| **CTPAT (United States)** | Customs Trade Partnership Against Terrorism | Defines U.S. supply-chain security and mutual recognition with PIP and BASC. |
| **NEEC (Mexico)** | Nuevo Esquema de Empresas Certificadas | Defines Mexican customs and logistics certification standards aligned with WCO SAFE. |
| **OEA (Brazil / MERCOSUR)** | Operador Econômico Autorizado | Establishes South American trade-security and continuity controls. |
| **AEO / AEO-S (EU & UK)** | Authorized Economic Operator – Security & Safety | Provides EU/UK customs-compliance standards aligned with WCO SAFE. |
| **WCO SAFE Framework (2021)** | Authorized Economic Operator Security Framework | Global standard for secure and resilient international trade. |
| **ISO 28000:2022** | Supply-Chain Security and Resilience | Provides requirements for secure and continuous supply-chain operations. |
| **ISO 22301:2019** | Business Continuity Management Systems | Integrates supply-chain continuity into organizational resilience. |
| **COBIT 2025** | DSS04 – Manage Continuity | Embeds trade-continuity assurance into enterprise governance. |
| **CSA CCM v5** | BCR-06 – Supply-Chain Resilience | Defines control expectations for logistics and cloud-supply environments. |
| **ATT (Australia)** | Australian Trusted Trader | Establishes secure and compliant supply-chain standards for Oceania. |
| **UAE / Saudi AEO Programs** | Regional AEO Mutual Recognition | Defines Middle East trade-security alignment under WCO SAFE. |
| **EAC AEO Program (East Africa)** | East African Community Authorized Economic Operator Program | Regional framework for trade-security and customs resilience. |
| **OECD 2026 Digital Security Principles** | Principle 7 – Resilient Digital Economy | Promotes transparency and cross-border cooperation in digital trade. |

---

## Definitions

Key terms and acronyms used in this document are defined in the **Resilience Terms and Definitions Register**, which provides standardized terminology for all Business Continuity, Disaster Recovery, and Crisis Management artefacts.

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.

---

**End of Document**
