# Canonical Citations Register

**Document Title:** Canonical Citations Register 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-28 
**Owner:** Governance Library Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`governance/register-glossary.md`](register-glossary.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/charter-governance-library.md`](charter-governance-library.md), [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py) 
**Classification:** Public 
**Category:** Core Governance 
**Review Frequency:** Quarterly, and upon publication of a superseding version of any listed standard 
**Repository Path:** [`governance/register-canonical-citations.md`](register-canonical-citations.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register is the positive list of canonical citations used across the GRC Documentation Library. It records, for each cited standard, regulation, framework, or specification:

- The standard or regulation identifier.
- The current published version that the library cites.
- The publication date.
- A short topic descriptor.
- Known superseded versions (so the standards-currency linter can flag stale references).

The companion linter [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py) parses this register and uses it to detect:

- References to superseded versions where a current version is recorded here.
- References including "(draft)" markers where the current version has been published.

The register is the single source of truth. When a new version of a standard is published, update this register first; the linter will then flag remaining references to the prior version across the library.

---

## Conventions

- **Standard ID**: the canonical short identifier as the standard publisher writes it (for example, `ISO/IEC 27001` rather than `ISO 27001`).
- **Current version**: year, year-month, or version number as the publisher writes it.
- **Publication date**: ISO 8601 year or year-month where known.
- **Topic**: one-line descriptor.
- **Superseded versions**: comma-separated list of prior version markers the linter should flag if encountered. Includes prior years (`2013`) and prior phrasing (`draft 2024`, `draft`, `2024 draft`).
- "-" in any column means "not applicable" or "none recorded".

When citing a standard in library content, use the **Standard ID** plus the **Current version** in the format the publisher uses (for example, `ISO/IEC 42006:2025`, `NIST SP 800-53 Rev 5`). The linter relies on this exact format.

---

## ISO / IEC standards

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| ISO/IEC 27001 | 2022 | 2022-10 | Information security management systems: requirements | 2013 |
| ISO/IEC 27002 | 2022 | 2022-02 | Information security controls | 2013 |
| ISO/IEC 27005 | 2022 | 2022-10 | Information security risk management | 2018 |
| ISO/IEC 27017 | 2015 | 2015-12 | Cloud-service-specific information security controls | - |
| ISO/IEC 27018 | 2019 | 2019-01 | Protection of personally identifiable information in public clouds acting as PII processors | - |
| ISO/IEC 27033 | 2020 | 2020 | Network security architecture and segmentation | - |
| ISO/IEC 27036-2 | 2014 | 2014-08 | Information security for supplier relationships | - |
| ISO/IEC 27701 | 2019 | 2019-08 | Privacy information management extension to ISO/IEC 27001 | - |
| ISO 22301 | 2019 | 2019-10 | Business continuity management systems | - |
| ISO 31000 | 2018 | 2018-02 | Risk management: principles and guidelines | - |
| ISO/IEC 38500 | 2024 | 2024 | Governance of IT for the organization | 2015 |
| ISO/IEC 23894 | 2023 | 2023-02 | AI risk management guidance | - |
| ISO/IEC 42001 | 2023 | 2023-12 | AI management systems: requirements | - |
| ISO/IEC 42005 | 2025 | 2025-05 | AI system impact assessment | - |
| ISO/IEC 42006 | 2025 | 2025 | Requirements for bodies providing audit and certification of AI management systems | draft, draft 2024, 2024 draft |
| ISO 28000 | 2022 | 2022-03 | Security management systems for the supply chain | 2007 |
| ISO 28001 | 2007 | 2007 | Best practices for implementing supply chain security | - |
| ISO 15489 | 2016 | 2016-04 | Records management | - |
| ISO 50001 | 2018 | 2018-08 | Energy management systems | - |
| ISO/IEC 5259 | 2024 | 2024 | Data quality for AI and machine learning | - |
| ISO 37301 | 2021 | 2021-04 | Compliance management systems | - |
| ISO 37001 | 2025 | 2025 | Anti-bribery management systems | 2016 |
| ISO/IEC 17021 | 2015 | 2015 | Conformity assessment: requirements for bodies providing audit and certification of management systems | - |

## NIST publications

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| NIST SP 800-34 | Rev 1 | 2010-05 | Contingency Planning Guide for Federal Information Systems | - |
| NIST SP 800-53 | Rev 5 | 2020-09 | Security and Privacy Controls for Information Systems and Organizations | Rev 4 |
| NIST SP 800-88 | Rev 1 | 2014-12 | Media sanitization | - |
| NIST SP 800-207 | (1.0) | 2020-08 | Zero Trust Architecture | - |
| NIST CSF | 2.0 | 2024-02 | Cybersecurity Framework | 1.1 |
| NIST AI RMF | 1.0 | 2023-01 | AI Risk Management Framework | - |
| NIST AI 600-1 | 1.0 | 2024-07 | Generative AI Profile for AI RMF | - |
| NIST SP 800-218 | 1.1 | 2022-02 | Secure Software Development Framework (SSDF) | 1.0 |
| NIST SP 800-161 | Rev 1 | 2022-05 | Cybersecurity Supply Chain Risk Management | Rev 0 |

## EU regulations and directives

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| EU AI Act | Regulation 2024/1689 | 2024-07 | AI regulation | - |
| EU NIS 2 Directive | Directive 2022/2555 | 2022-12 | Cybersecurity of network and information systems | NIS Directive 2016/1148 |
| EU DORA | Regulation 2022/2554 | 2022-12 | Digital Operational Resilience Act (financial-services) | - |
| EU GDPR | Regulation 2016/679 | 2016-04 | General Data Protection Regulation | Directive 95/46/EC |
| EU eIDAS | Regulation 2024/1183 (eIDAS 2) | 2024-04 | Electronic identification and trust services | Regulation 910/2014 (eIDAS 1) |
| EU EECC | Directive 2018/1972 | 2018-12 | European Electronic Communications Code | - |
| EU MDR | Regulation 2017/745 | 2017-04 | Medical Device Regulation | Directive 93/42/EEC |
| EU IVDR | Regulation 2017/746 | 2017-04 | In-Vitro Diagnostic Regulation | Directive 98/79/EC |
| EU UCC | Regulation 952/2013 | 2013-10 | Union Customs Code | - |

## North-American regulations and frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| US HIPAA | 1996 (with HITECH 2009 and Omnibus 2013 amendments) | - | Health Insurance Portability and Accountability Act | - |
| US HITECH | 2009 | 2009 | Health Information Technology for Economic and Clinical Health Act | - |
| US SOX | 2002 | 2002-07 | Sarbanes-Oxley Act | - |
| US CCPA | 2018 (CPRA amendments 2020) | 2018 | California Consumer Privacy Act | - |
| US FedRAMP | Rev 5 | 2023 | Federal Risk and Authorization Management Program (rev 5 alignment with NIST SP 800-53 Rev 5) | Rev 4 |
| US CMMC | 2.0 | 2024 | Cybersecurity Maturity Model Certification | 1.0, 1.02 |
| Canada CPPA | 2022 (pending enactment) | 2022 | Consumer Privacy Protection Act | PIPEDA (pending replacement) |
| Canada PIPEDA | 2000 (with 2015 DBSA amendments) | 2000 | Personal Information Protection and Electronic Documents Act | - |
| Canada AIDA | 2022 (pending enactment) | 2022 | Artificial Intelligence and Data Act | - |
| Quebec Law 25 | 2021 (phased in 2022-2024) | 2021 | An Act to modernize legislative provisions as regards the protection of personal information | - |

## Other privacy regulations

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| UK GDPR | 2018 (Data Protection Act 2018) | 2018 | UK General Data Protection Regulation | - |
| Brazil LGPD | 2018 (in force 2020) | 2018 | Lei Geral de Proteção de Dados | - |
| China PIPL | 2021 | 2021-11 | Personal Information Protection Law | - |
| Switzerland nFADP | 2023 | 2023-09 | New Federal Act on Data Protection (revDSG) | FADP 1992 |
| Saudi Arabia PDPL | 2023 | 2023-09 | Personal Data Protection Law | - |
| Singapore PDPA | 2012 (with 2020 amendments) | 2012 | Personal Data Protection Act | - |
| Australia Privacy Act | 1988 (with 2024 amendments) | 1988 | Privacy Act | - |

## CSA frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| CSA CCM | v4.1 | 2024 | Cloud Controls Matrix | v3.0.1, v4.0 |
| CSA AICM | v1.0.3 | 2025 | AI Controls Matrix | v1.0.0, v1.0.1, v1.0.2 |
| CSA STAR | continuous | - | Security, Trust, Assurance and Risk programme | - |

## ISACA frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| COBIT | 2019 | 2018-11 (with Design Guide and Implementation Guide updates 2019, 2020) | Control Objectives for Information and Related Technologies | COBIT 5, COBIT 4.1, COBIT 2025 (hallucinated) |

## Cybersecurity adversary frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| MITRE ATT&CK | v15 | 2024-10 | Adversary Tactics, Techniques, and Common Knowledge | - |
| MITRE ATLAS | v4.7 | 2024 | Adversarial Threat Landscape for AI Systems | - |

## OWASP

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| OWASP Top 10 | 2021 | 2021 | Top 10 web application security risks | 2017 |
| OWASP LLM Top 10 | 2025 | 2025 | Top 10 LLM application risks | 2023 |
| OWASP ASVS | 4.0.3 | 2021 | Application Security Verification Standard | 3.0 |
| OWASP SAMM | 2.0 | 2020 | Software Assurance Maturity Model | 1.5 |

## Customs and trade

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| WCO SAFE Framework | 2021 | 2021 | World Customs Organization Framework of Standards to Secure and Facilitate Global Trade | 2018 |
| BASC International Standard | v6 (2023) | 2023 | Business Alliance for Secure Commerce international security standard | v5 |
| CTPAT MSC | 2020 | 2020 | Customs-Trade Partnership Against Terrorism Minimum Security Criteria | - |

## Sector-specific (energy, telecom, finance)

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| NERC CIP | 014-3 (latest revision) | various | North American Electric Reliability Corporation Critical Infrastructure Protection standards | - |
| PCI DSS | 4.0.1 | 2024-06 | Payment Card Industry Data Security Standard | 3.2.1, 4.0 |
| IEC 62443 | 2018 onwards | - | Industrial automation and control systems security | - |
| Basel III | 2017 (with 2023 finalisation, in force 2025) | - | Banking regulation framework | Basel II |

## OECD and global

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| OECD AI Principles | 2024 (updated) | 2024 | AI policy principles | 2019 |
| OECD Privacy Guidelines | 2013 (revised) | 2013 | Privacy and transborder data flows | 1980 |
| WTO TFA | 2017 | 2017 | Trade Facilitation Agreement | - |

## ICAO and IMO

| Standard ID | Current version | Publication date | Topic | Superseded versions |
| --- | --- | --- | --- | --- |
| ICAO Doc 10026 | 2nd edition | 2024 | Manual on Aviation Security | 1st edition |
| ICAO Doc 10055 | 2024 | 2024 | Aviation Cybersecurity Strategy | - |
| IMO Resolution MSC-FAL.1/Circ.3 | Rev 2 | 2022-06 | Maritime cyber risk management guidelines | Rev 1 |

---

## Maintenance

- When a new version of a listed standard is published, update the **Current version** and **Publication date** columns and add the prior version to **Superseded versions**.
- When a standard is added to the library's citation usage, add an entry here before the citing PR merges.
- The linter is permissive: it flags only patterns explicitly listed here as superseded. To catch a stale citation, the prior version must be listed under **Superseded versions**.
- Periodic review: at least quarterly, plus on publication of any major superseding version.

---

**End of Document**
