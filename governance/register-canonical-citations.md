# Canonical Citations Register

**Document Title:** Canonical Citations Register\
**Document Type:** Register\
**Version:** 1.5.15\
**Date:** 2026-07-07\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-glossary.md`](register-glossary.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Quarterly, and upon publication of a superseding version of any listed standard\
**Repository Path:** [`governance/register-canonical-citations.md`](register-canonical-citations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

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

Entries in this register are subject to publisher-source verification under the Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)). Verification results are recorded row-by-row in the Citation Verifications Register. Until an entry is verified there, it carries no recorded factual provenance beyond having been written into this register; the verification process is the control that converts written entries into evidence-bearing entries.

---

## Conventions

- **Standard ID**: the canonical short identifier as the standard publisher writes it (for example, `ISO/IEC 27001` rather than `ISO 27001`).
- **Current version**: year, year-month, or version number as the publisher writes it.
- **Publication date**: ISO 8601 year or year-month where known.
- **Topic**: one-line descriptor.
- **Superseded versions**: comma-separated list of prior version markers the linter should flag if encountered. Includes prior years (`2013`) and prior phrasing (`draft 2024`, `draft`, `2024 draft`).
- **Upstream check location**: the authoritative upstream page where the current version is published and can be re-checked (the publisher's catalogue page, the official register or EUR-Lex / legislation ELI page, or the project's releases page). This is where a maintainer goes to confirm currency; it is deliberately a stable "where to check" pointer, not a deep version-specific link. `-` means no confirmed location is recorded yet (see the next column).
- **Last verified (UTC)**: the UTC date on which the Upstream check location was last fetch-confirmed against the recorded Current version, or `needs-reconfirm` when currency has not been confirmed this cycle. `needs-reconfirm` is an honest deferral, not a defect: it covers both entries never yet verified and entries whose upstream blocks automated fetch (as of the 2026-06-30 population, `iso.org`, the IEC webstore, and several government sources such as `hhs.gov`, `nerc.com`, `tsa.gov`, `planalto.gov.br`, and `wcoomd.org` returned HTTP 403 / JS-gated responses to automated fetch, so their rows carry `needs-reconfirm` rather than an unconfirmed URL; a maintainer with a browser, or a future cycle with different egress, fills these).
- "-" in any column means "not applicable" or "none recorded".

When citing a standard in library content, use the **Standard ID** plus the **Current version** in the format the publisher uses (for example, `ISO/IEC 42006:2025`, `NIST SP 800-53 Rev. 5`). The linter relies on this exact format.

**Version-currency cadence (advisory, not a gate).** The `Upstream check location` and `Last verified (UTC)` columns operationalize the `evidence-grounded-completion` rule's external-version-currency corollary: the **upstream source is the only authority** on whether a version is current; a stored note, a cached copy, or a `grc_library_ref` holding is believed-current STORAGE, never a version authority. Whenever a row is **load-bearing for a task** and its `Last verified (UTC)` is `needs-reconfirm` or older than **one week**, re-check the Upstream check location before relying on the row, and update `Last verified (UTC)` (and the version columns, if the upstream has moved) in that PR. This is a discipline cued by the column, not a CI gate: a hard gate would fail whenever egress is blocked (an environment condition, not a defect), so the check is advisory like the matrix-fit worklist. The full operational procedure (find what is held via the index, verify upstream this turn, act only after both; and the superseded-archival workflow for `grc_library_ref`) lives in [`specification-citation-verification.md`](specification-citation-verification.md).

**Scope (extended)**: this register's primary scope is formal standards, regulations, and Acts. As of 2026-06-22 the scope is extended to include **soft-law supervisory guidance** (Article 29 Working Party Guidelines, EDPB opinions and guidelines, ICO codes of practice, ANPD orientation documents, and equivalent supervisory-authority-issued guidance documents that the corpus cites by name). Soft-law entries follow the same column structure with the publisher being the supervisory authority and the "Current version" being the published revision number (e.g., `rev.01`). Soft-law guidance is typically referenced for interpretive guidance on a formal regulation; the register's role is to anchor the citation and flag stale revisions.

---

## ISO / IEC standards

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| ISO/IEC 27001 | 2022 | 2022-10 | Information security management systems: requirements | 2013 | - | needs-reconfirm |
| ISO/IEC 27002 | 2022 | 2022-02 | Information security controls | 2013 | - | needs-reconfirm |
| ISO/IEC 27005 | 2022 | 2022-10 | Information security risk management | 2018 | - | needs-reconfirm |
| ISO/IEC 27017 | 2015 | 2015-12 | Cloud-service-specific information security controls | - | - | needs-reconfirm |
| ISO/IEC 27018 | 2025 | 2025-08 | Protection of personally identifiable information in public clouds acting as PII processors | 2019 | - | needs-reconfirm |
| ISO/IEC 27019 | 2024 | 2024-10 | Information security controls for the energy utility industry (Edition 2; based on ISO/IEC 27002:2022 with 12 additional energy-sector controls) | 2017 | - | needs-reconfirm |
| ISO/IEC 27033-1 | 2015 | 2015 | Network security - Part 1: Overview and concepts (the roadmap part of the multi-part ISO/IEC 27033 series on network security architecture and segmentation; confirmed unchanged 2021) | 2009 | https://www.iso.org/standard/63461.html | verified 2026-06-30 |
| ISO/IEC 27036-2 | 2022 | 2022-06 | Cybersecurity - Supplier relationships - Part 2: Requirements (Edition 2; cancels and replaces the 2014 first edition) | 2014 | https://www.iso.org/standard/82060.html | verified 2026-06-30 |
| ISO/IEC 27036-3 | 2023 | 2023-06 | Cybersecurity - Supplier relationships - Part 3: Guidelines for hardware, software, and services supply chain security | 2013 | - | needs-reconfirm |
| ISO/IEC 27036-4 | 2016 | 2016-10 | Information security for supplier relationships - Part 4: Guidelines for security of cloud services | - | - | needs-reconfirm |
| ISO/IEC 27701 | 2025 | 2025-10 | Privacy information management system (PIMS); standalone standard since the 2025 revision (previously an extension to ISO/IEC 27001 in the 2019 edition; transition deadline October 2028) | 2019 | - | needs-reconfirm |
| ISO 22301 | 2019 | 2019-10 | Business continuity management systems | - | - | needs-reconfirm |
| ISO 31000 | 2018 | 2018-02 | Risk management: principles and guidelines | - | - | needs-reconfirm |
| ISO/IEC 38500 | 2024 | 2024 | Governance of IT for the organization | 2015 | - | needs-reconfirm |
| ISO/IEC 23894 | 2023 | 2023-02 | AI risk management guidance | - | - | needs-reconfirm |
| ISO/IEC 42001 | 2023 | 2023-12 | AI management systems: requirements | - | - | needs-reconfirm |
| ISO/IEC 42005 | 2025 | 2025-05 | AI system impact assessment | - | - | needs-reconfirm |
| ISO/IEC 42006 | 2025 | 2025 | Requirements for bodies providing audit and certification of AI management systems | draft, draft 2024, 2024 draft | - | needs-reconfirm |
| ISO 28000 | 2022 | 2022-03 | Security management systems for the supply chain | 2007 | - | needs-reconfirm |
| ISO 28001 | 2007 | 2007 | Best practices for implementing supply chain security | - | - | needs-reconfirm |
| ISO 15489 | 2016 | 2016-04 | Records management | - | - | needs-reconfirm |
| ISO 50001 | 2018 | 2018-08 | Energy management systems | - | - | needs-reconfirm |
| ISO/IEC 5259 | 2024 | 2024 | Data quality for AI and machine learning | - | - | needs-reconfirm |
| ISO 37301 | 2021 | 2021-04 | Compliance management systems | - | - | needs-reconfirm |
| ISO 37001 | 2025 | 2025-02 | Anti-bribery management systems - Requirements with guidance for use (Edition 2; transition deadline February 2027; changes from 2016 edition are not extensive) | 2016 | - | needs-reconfirm |
| ISO/IEC 17021 | 2015 | 2015 | Conformity assessment: requirements for bodies providing audit and certification of management systems | - | - | needs-reconfirm |

## NIST publications

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| NIST SP 800-34 | Rev. 1 | 2010-05 | Contingency Planning Guide for Federal Information Systems | - | https://csrc.nist.gov/pubs/sp/800/34/r1/final | 2026-06-30 |
| NIST SP 800-53 | Rev. 5 | 2020-09 | Security and Privacy Controls for Information Systems and Organizations | Rev. 4 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | 2026-06-30 |
| NIST SP 800-61 | Rev. 3 | 2025-04 | Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile) | Rev. 2, Rev. 1 | https://csrc.nist.gov/pubs/sp/800/61/r3/final | 2026-06-30 |
| NIST SP 800-63B | Rev. 4 | 2025-07 | Digital Identity Guidelines: Authentication and Authenticator Management (part of SP 800-63 Rev. 4 family) | Rev. 3 | https://csrc.nist.gov/pubs/sp/800/63/b/4/final | 2026-06-30 |
| NIST SP 800-88 | Rev. 2 | 2025-09 | Media sanitization (Rev. 2 reframes around an enterprise media-sanitization programme and defers sanitization-technique detail to IEEE 2883, NSA specifications, or an organizationally-approved standard, retaining only cryptographic erase directly) | Rev. 1 | https://csrc.nist.gov/pubs/sp/800/88/r2/final | verified 2026-06-30 |
| NIST SP 800-207 | (1.0) | 2020-08 | Zero Trust Architecture | - | https://csrc.nist.gov/pubs/sp/800/207/final | 2026-06-30 |
| NIST CSF | 2.0 | 2024-02 | Cybersecurity Framework | 1.1 | https://www.nist.gov/cyberframework | 2026-06-30 |
| NIST AI RMF | 1.0 | 2023-01 | AI Risk Management Framework | - | https://www.nist.gov/itl/ai-risk-management-framework | 2026-06-30 |
| NIST AI 600-1 | 1.0 | 2024-07 | Generative AI Profile for AI RMF | - | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | 2026-06-30 |
| NIST SP 800-218 | 1.1 | 2022-02 | Secure Software Development Framework (SSDF) | 1.0 | https://csrc.nist.gov/pubs/sp/800/218/final | 2026-06-30 |
| NIST SP 800-161 | Rev. 1 | 2022-05 (with 2024-11 update) | Cybersecurity Supply Chain Risk Management | Rev. 0 | https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final | 2026-06-30 |
| NIST SP 800-82 | Rev. 3 | 2023-09 | Guide to Operational Technology (OT) Security (formerly Guide to Industrial Control Systems Security) | Rev. 2, Rev. 1 | https://csrc.nist.gov/pubs/sp/800/82/r3/final | 2026-06-30 |

## IEEE standards

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| IEEE 2883 | 2022 | 2022-08 | IEEE Standard for Sanitizing Storage (the Clear / Purge / Destruct sanitization categories and per-technology technique requirements; the technique standard NIST SP 800-88 Rev. 2 now defers to) | - | https://standards.ieee.org/ieee/2883/10277/ | verified 2026-06-30 |

## EU regulations and directives

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| EU AI Act | Regulation 2024/1689 | 2024-07 | AI regulation | - | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 2026-06-30 |
| EU NIS 2 Directive | Directive 2022/2555 | 2022-12 | Cybersecurity of network and information systems | NIS Directive 2016/1148 | https://eur-lex.europa.eu/eli/dir/2022/2555/oj | 2026-06-30 |
| EU DORA | Regulation 2022/2554 | 2022-12 | Digital Operational Resilience Act (financial-services) | - | https://eur-lex.europa.eu/eli/reg/2022/2554/oj | 2026-06-30 |
| EU GDPR | Regulation 2016/679 | 2016-04 | General Data Protection Regulation | Directive 95/46/EC | https://eur-lex.europa.eu/eli/reg/2016/679/oj | 2026-06-30 |
| EU Data Act | Regulation (EU) 2023/2854 | 2023-12 | Data Act (harmonized rules on fair access to and use of data; main provisions applicable from 12 September 2025) | - | https://eur-lex.europa.eu/eli/reg/2023/2854/oj | 2026-06-30 |
| EU eIDAS | Regulation 910/2014 as amended by Regulation 2024/1183 (eIDAS 2) | 2024-04 (latest amendment) | Electronic identification and trust services | - | https://eur-lex.europa.eu/eli/reg/2014/910/oj | 2026-06-30 |
| EU EECC | Directive 2018/1972 | 2018-12 | European Electronic Communications Code | - | https://eur-lex.europa.eu/eli/dir/2018/1972/oj | 2026-06-30 |
| EU MDR | Regulation 2017/745 | 2017-04 | Medical Device Regulation | Directive 93/42/EEC | https://eur-lex.europa.eu/eli/reg/2017/745/oj | 2026-06-30 |
| EU IVDR | Regulation 2017/746 | 2017-04 | In-Vitro Diagnostic Regulation | Directive 98/79/EC | https://eur-lex.europa.eu/eli/reg/2017/746/oj | 2026-06-30 |
| EU UCC | Regulation 952/2013 | 2013-10 | Union Customs Code | - | https://eur-lex.europa.eu/eli/reg/2013/952/oj | 2026-06-30 |

## North-American regulations and frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| US HIPAA | 1996 (with HITECH 2009 and Omnibus 2013 amendments); HIPAA Security Rule NPRM issued by HHS OCR on 27 December 2024, published in the Federal Register on 6 January 2025, comment period closed 7 March 2025 with approximately 5,000 comments. The NPRM would (among other changes) make encryption of ePHI and multi-factor authentication mandatory, eliminate the "required vs addressable" implementation-specification distinction, and require an annually-refreshed asset inventory and ePHI network map. Final rule pending as of May 2026 | - | Health Insurance Portability and Accountability Act | - | - | needs-reconfirm |
| US HITECH | 2009 | 2009 | Health Information Technology for Economic and Clinical Health Act | - | https://www.govinfo.gov/app/details/PLAW-111publ5 | 2026-06-30 |
| US SOX | 2002 | 2002-07 | Sarbanes-Oxley Act | - | https://www.govinfo.gov/app/details/PLAW-107publ204 | 2026-06-30 |
| US CCPA | 2018 (CPRA amendments 2020) | 2018 | California Consumer Privacy Act | - | https://oag.ca.gov/privacy/ccpa | 2026-06-30 |
| Illinois BIPA | 2008 as amended by Illinois SB 2979 (signed 2 August 2024 and effective immediately), which limits damages to a "single recovery" per BIPA §15(b) and §15(d) violation type per individual and recognizes electronic written release | 2008 | Biometric Information Privacy Act (740 ILCS 14/) | - | https://www.ilga.gov/Legislation/ILCS/Articles?ActID=3004&ChapterID=57 | 2026-06-30 |
| Colorado AI Act | 2024 (Colorado SB 24-205, signed 17 May 2024). Original effective date 1 February 2026; postponed by Colorado SB 25B-004 (signed 28 August 2025) to 30 June 2026. Enforcement effectively frozen by U.S. District Court for the District of Colorado on 27 April 2026 pending litigation (xAI v. Colorado). following the Governor's Working Group framework (17 March 2026), the legislature repealed and re-enacted SB 24-205 via Colorado SB 26-189 (Automated Decision-Making Technology), signed into law May 2026, with revised automated-decision-making requirements and a revised effective date of 1 January 2027 | 2024-05-17 | Colorado Consumer Protections for Artificial Intelligence (SB 24-205) as re-enacted by SB 26-189 | - | https://leg.colorado.gov/bills/sb24-205 | 2026-06-30 |
| US FedRAMP | Rev. 5 | 2023 | Federal Risk and Authorization Management Program (rev 5 alignment with NIST SP 800-53 Rev. 5) | Rev. 4 | https://www.fedramp.gov/ | 2026-06-30 |
| US CMMC | 2.0 | 2024 | Cybersecurity Maturity Model Certification | 1.0, 1.02 | - | needs-reconfirm |
| Canada CPPA | Lapsed 2025-01-06 (Bill C-27 died on prorogation; no replacement bill introduced as of 2026-05) | 2022 (proposed) | Consumer Privacy Protection Act (never enacted) | n/a; PIPEDA remains in force | https://www.parl.ca/legisinfo/en/bill/44-1/c-27 | 2026-06-30 |
| Canada PIPEDA | 2000 (with 2015 DBSA amendments) | 2000 | Personal Information Protection and Electronic Documents Act | - | https://laws-lois.justice.gc.ca/eng/acts/p-8.6/ | 2026-06-30 |
| Canada AIDA | Lapsed 2025-01-06 (Bill C-27 died on prorogation; per June 2025 ministerial statement, AIDA will not return in its original form) | 2022 (proposed) | Artificial Intelligence and Data Act (never enacted) | n/a; no federal AI law enacted | https://www.parl.ca/legisinfo/en/bill/44-1/c-27 | 2026-06-30 |
| Quebec Law 25 | 2021 (phased in 2022-2024) | 2021 | An Act to modernize legislative provisions as regards the protection of personal information | - | - | needs-reconfirm |

## Other privacy regulations

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| UK GDPR | 2018 (DPA 2018) as amended by Data (Use and Access) Act 2025 (c. 18), royal assent 19 June 2025; main data-protection provisions commenced 5 February 2026 (Commencement No. 6 Regulations 2026) | 2018 | UK General Data Protection Regulation (retained EU GDPR as amended by the Data Protection Act 2018 and the Data (Use and Access) Act 2025) | - | https://www.legislation.gov.uk/eur/2016/679/contents | 2026-06-30 |
| Brazil LGPD | 2018 (in force 2020) | 2018 | Lei Geral de Proteção de Dados | - | - | needs-reconfirm |
| Resolution CD/ANPD No. 15/2024 | 2024 | 2024-04-26 | ANPD Security Incident Communication Regulation (RCIS): 3-business-day breach notification to the ANPD and data subjects, staged communication, doubled deadlines for small-scale agents (the resolution is enacted "de 24 de abril de 2024"; this column records the later DOU publication date) | - | https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis | 2026-07-07 |
| China PIPL | 2021 | 2021-11 | Personal Information Protection Law | - | - | needs-reconfirm |
| China Cross-Border Data Provisions (2024) | 2024-03-22 (immediate effect) | 2024-03-22 | Provisions on Promoting and Regulating the Cross-Border Flow of Data (CAC); revises personal-data export thresholds and exemptions; extends CAC security-assessment validity from two to three years | - | https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm | 2026-06-30 |
| Switzerland nFADP | 2023 | 2023-09 | New Federal Act on Data Protection (revDSG) | FADP 1992 | - | needs-reconfirm |
| Saudi Arabia PDPL | 2023 | 2023-09 | Personal Data Protection Law | - | - | needs-reconfirm |
| Singapore PDPA | 2012 (with 2020 amendments) | 2012 | Personal Data Protection Act | - | - | needs-reconfirm |
| Australia Privacy Act | 1988 (with 2024 amendments) | 1988 | Privacy Act | - | https://www.legislation.gov.au/C2004A03712/latest | 2026-06-30 |
| India DPDPA | 2023 (Act enacted 2023-08-11); Digital Personal Data Protection Rules 2025 notified 13 November 2025 by MeitY with phased commencement (Data Protection Board provisions immediate; consent-manager registration after 12 months; remainder after 18 months) | 2023-08-11 | Digital Personal Data Protection Act 2023 plus the Digital Personal Data Protection Rules 2025 | - | - | needs-reconfirm |
| Malaysia PDPA | 2010 (Act 709) as amended by Personal Data Protection (Amendment) Act 2024 (Act A1727); phased commencement: tranche 1 from 1 January 2025, tranche 2 from 1 April 2025, tranche 3 (including the mandatory DPO appointment and 72-hour breach notification) from 1 June 2025. DPO and breach-notification Guidelines issued 25 February 2025 | 2010 | Personal Data Protection Act (Malaysia) | - | https://www.pdp.gov.my/ppdpv1/en/akta/pdp-act-2010-en/ | 2026-06-30 |

## CSA frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| CSA CCM | v4.1 | 2024 | Cloud Controls Matrix | v3.0.1, v4.0 | https://cloudsecurityalliance.org/research/cloud-controls-matrix | 2026-06-30 |
| CSA AICM | v1.1 | 2026 | AI Controls Matrix | v1.0.0, v1.0.1, v1.0.2, v1.0.3 | https://cloudsecurityalliance.org/artifacts/ai-controls-matrix | 2026-06-30 |
| CSA STAR | continuous | - | Security, Trust, Assurance and Risk programme | - | https://cloudsecurityalliance.org/star | 2026-06-30 |

## ISACA frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| COBIT | 2019 | 2018-11 (with Design Guide and Implementation Guide updates 2019, 2020) | Control Objectives for Information and Related Technologies. Note: COBIT 2025 is not a published version; the hallucination is enforced by [`tools/lint-citations.py`](../tools/lint-citations.py). | COBIT 5, COBIT 4.1 | https://www.isaca.org/resources/cobit | 2026-06-30 |

## Cybersecurity adversary frameworks

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| MITRE ATT&CK | v19.1 | 2026-05 | Adversary Tactics, Techniques, and Common Knowledge | v15 | https://attack.mitre.org/resources/updates/ | 2026-06-30 |
| MITRE ATLAS | v2026.06 | 2026-06 | Adversarial Threat Landscape for AI Systems | v2026.05 | https://github.com/mitre-atlas/atlas-data | 2026-07-01 |
| STRIDE | continuous | 1999 | Six-category threat taxonomy (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) introduced by Kohnfelder and Garg at Microsoft; integrated into the Microsoft Security Development Lifecycle (SDL) Threat Modeling Tool | - | https://owasp.org/www-community/Threat_Modeling_Process | 2026-06-30 |
| LINDDUN | v3.0 | 2023 | Seven-category privacy threat taxonomy (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance) maintained by KU Leuven imec-DistriNet | v2.0 (2015) | https://linddun.org/ | 2026-06-30 |
| AVID | continuous | 2023 | AI Vulnerability Database, an open knowledge base of AI failure modes and harms (avidml.org) | - | https://avidml.org/ | 2026-06-30 |
| MLCommons AILuminate | v1.0 | 2024 | AI risk taxonomy and benchmark, 14-category hazard taxonomy | - | https://mlcommons.org/benchmarks/ailuminate/ | 2026-06-30 |
| HarmBench | continuous | 2024-02 | Standardized evaluation framework for automated red-teaming methods against LLMs and defences | - | https://github.com/centerforaisafety/HarmBench | 2026-06-30 |
| OWASP GenAI Security Project | continuous | 2024 | Working-group output covering GenAI security risks, controls, and reference test cases (genai.owasp.org) | - | https://genai.owasp.org/ | 2026-06-30 |

## OWASP

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| OWASP Top 10 | 2025 | 2025-11 | Top 10 web application security risks (Eighth edition; new categories include "Software Supply Chain Failures" evolving from "Vulnerable and Outdated Components"; A02 "Security Misconfiguration" moved up from #5 in 2021 to #2 in 2025) | 2021, 2017 | https://owasp.org/www-project-top-ten/ | 2026-06-30 |
| OWASP LLM Top 10 | 2025 | 2025 | Top 10 LLM application risks | 2023 | https://genai.owasp.org/llm-top-10/ | 2026-06-30 |
| OWASP Agentic AI Top 10 | 2026 | 2026 | Top 10 risks for agentic AI systems | - | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ | 2026-06-30 |
| OWASP MCP Top 10 | 2025 | 2025 | Security risks for Model Context Protocol integrations | - | https://owasp.org/www-project-mcp-top-10/ | 2026-06-30 |
| OWASP ASVS | 5.0.0 | 2025-05 | Application Security Verification Standard (released May 2025 at Global AppSec EU Barcelona; ~350 requirements across 17 chapters in a three-tier model) | 4.0.3, 4.0, 3.0 | https://owasp.org/www-project-application-security-verification-standard/ | 2026-06-30 |
| OWASP SAMM | 2.0 | 2020 | Software Assurance Maturity Model | 1.5 | https://owaspsamm.org/ | 2026-06-30 |

## Customs and trade

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| WCO SAFE Framework | 2021 | 2021 | World Customs Organization Framework of Standards to Secure and Facilitate Global Trade | 2018 | - | needs-reconfirm |
| BASC International Standard | v6 (2022) | 2022 | Business Alliance for Secure Commerce international security standard | v5 | https://www.wbasco.org/en/certification/basc-certification | 2026-06-30 |
| CTPAT MSC | 2020 | 2020 | Customs-Trade Partnership Against Terrorism Minimum Security Criteria | - | - | needs-reconfirm |

## Sector-specific (energy, telecom, finance)

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| NERC CIP | Standards family CIP-002 through CIP-014 (each standard has its own revision number) | various per individual standard | North American Electric Reliability Corporation Critical Infrastructure Protection standards family | - | - | needs-reconfirm |
| PCI DSS | 4.0.1 | 2024-06 | Payment Card Industry Data Security Standard | 3.2.1, 4.0 | https://www.pcisecuritystandards.org/document_library/ | 2026-06-30 |
| IEC 62443-1-1 | 2009 | 2009 | Industrial communication networks: Security: Part 1-1: Concepts and models | - | https://webstore.iec.ch/publication/7029 | 2026-06-30 |
| IEC 62443-2-1 | 2024 | 2024 | Security for industrial automation and control systems: Part 2-1: Establishing an IACS security programme | 2010 | - | needs-reconfirm |
| IEC 62443-2-4 | 2023 | 2023 | Security for industrial automation and control systems: Part 2-4: Security programme requirements for IACS service providers | 2015 | - | needs-reconfirm |
| IEC 62443-3-2 | 2020 | 2020 | Security for industrial automation and control systems: Part 3-2: Security risk assessment for system design | - | - | needs-reconfirm |
| IEC 62443-3-3 | 2013 | 2013 | Security for industrial automation and control systems: Part 3-3: System security requirements and security levels | - | https://webstore.iec.ch/en/publication/7033 | 2026-06-30 |
| IEC 62443-4-1 | 2018 | 2018 | Security for industrial automation and control systems: Part 4-1: Secure product development lifecycle requirements | - | - | needs-reconfirm |
| IEC 62443-4-2 | 2019 | 2019 | Security for industrial automation and control systems: Part 4-2: Technical security requirements for IACS components | - | - | needs-reconfirm |
| IEC 61511 | 2016 (Edition 2, Amendment 1 in 2017) | 2016 | Functional safety: Safety instrumented systems for the process industry sector | Edition 1 (2003) | - | needs-reconfirm |
| IEC 61508 | 2010 | 2010 | Functional safety of electrical/electronic/programmable electronic safety-related systems | 1998 | - | needs-reconfirm |
| ISO 16484 | parts published 2010 to 2020 | various | Building automation and control systems (BACS) | - | - | needs-reconfirm |
| ASHRAE 135 | 2020 (with subsequent addenda) | 2020 | BACnet protocol for building automation and control networks (incl. BACnet/SC) | - | https://www.ashrae.org/technical-resources/bookstore/bacnet | 2026-06-30 |
| NIST SP 1900 series | 2023 | 2023 | Smart-building cybersecurity and IoT guidance | - | - | needs-reconfirm |
| NFPA 72 | 2025 | 2025 | National Fire Alarm and Signaling Code | 2022, 2019 | https://www.nfpa.org/codes-and-standards/nfpa-72-standard-development/72 | 2026-06-30 |
| EN 54 | series, current parts published 2017 to 2023 | various | Fire detection and fire alarm systems (European standard series) | - | - | needs-reconfirm |
| TSA Pipeline Security Directive | SD02 (with subsequent revisions) | 2021 (initial; revised through 2024) | US Transportation Security Administration pipeline cybersecurity requirements | - | - | needs-reconfirm |
| Basel III | 2017 (with 2023 finalization, in force 2025) | - | Banking regulation framework | Basel II | https://www.bis.org/bcbs/basel3.htm | 2026-06-30 |

## OECD and global

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| OECD AI Principles | 2019 Recommendation as updated 2024 | 2019 (original); 2024 (update) | AI policy principles | - | https://oecd.ai/en/ai-principles | 2026-06-30 |
| OECD Privacy Guidelines | 2013 (revised) | 2013 | Privacy and transborder data flows | 1980 | - | needs-reconfirm |
| WTO TFA | 2017 | 2017 | Trade Facilitation Agreement | - | https://www.wto.org/english/tratop_e/tradfa_e/tradfa_e.htm | 2026-06-30 |

## ICAO and IMO

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| ICAO Doc 10026 | 2nd edition | 2024 | Manual on Aviation Security | 1st edition | - | needs-reconfirm |
| ICAO Doc 10055 | 2024 | 2024 | Aviation Cybersecurity Strategy | - | https://www.icao.int/aviation-cybersecurity/strategy | 2026-06-30 |
| IMO Resolution MSC-FAL.1/Circ.3 | Rev. 3 | 2025-04 | Maritime cyber risk management guidelines | Rev. 2, Rev. 1 | https://www.imo.org/en/OurWork/Security/Pages/Cyber-security.aspx | 2026-06-30 |

## AI safety evaluation programmes

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| UK AISI inspect_evals | continuous | 2024 | UK AI Safety Institute community evaluation catalogue running on Inspect AI harness; hosts third-party benchmarks including AgentDojo, AgentHarm, StrongREJECT | - | https://ukgovernmentbeis.github.io/inspect_evals/ | 2026-06-30 |
| Meta CyberSecEval | v4 | 2025 | Offensive cyber benchmark covering ATT&CK compliance, FRR, secure code generation, prompt injection, code interpreter abuse, X86-64 CTF, spear phishing, autonomous offensive cyber ops, AutoPatch, CyberSOCEval | v3, v2, v1 | https://github.com/meta-llama/PurpleLlama/tree/main/CybersecurityBenchmarks | 2026-06-30 |
| NIST SP 800-218A | Final | 2024 | Secure Software Development Practices for Generative AI and Dual-Use Foundation Models (SSDF profile) | - | https://csrc.nist.gov/pubs/sp/800/218/a/final | 2026-06-30 |

## AI security tooling references

This section records open-source AI security projects referenced by library content as defensive-pattern exemplars or as concrete tooling choices. Unlike standards, these are versioned software projects; the Current version column records the version current at registration. Re-verification cadence is annual per the Citation Verification Specification, with on-demand re-verification when a referencing library document is updated.

| Project | Current version | Registration date | Topic | License | Status notes | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Trusted-AI ART | v1.20.1 | 2025-07 | Adversarial Robustness Toolbox: evasion, poisoning, extraction, inference attacks and defences across classical ML and DL | MIT | Linux Foundation flagship | https://github.com/Trusted-AI/adversarial-robustness-toolbox/releases | 2026-06-30 |
| IBM HEART | v0.7.0 | 2025-07 | Hardened Extension of ART for DoD MAITE-aligned T&E | MIT | Curated ART subset | https://github.com/IBM/heart-library | 2026-06-30 |
| AIJack | continuous | 2024 | ML privacy and federated-learning attack/defence library | Apache 2.0 | - | https://github.com/Koukyosyumei/AIJack | 2026-06-30 |
| HarmBench framework | continuous | 2024-02 | 18-method automated red-team benchmark with R2D2 defence recipe | MIT | - | https://github.com/centerforaisafety/HarmBench | 2026-06-30 |
| Meta PurpleLlama | continuous | 2024 | Llama Guard safeguard models, Code Shield, CyberSecEval harness | MIT (SDK) + Llama Community License (Llama Guard / Prompt Guard weights) | - | https://github.com/meta-llama/PurpleLlama | 2026-06-30 |
| NVIDIA NeMo Guardrails | continuous | 2024 | Programmable rails framework (Input / Output / Dialog / Retrieval / Execution) | Apache 2.0 | - | https://github.com/NVIDIA/NeMo-Guardrails/releases | 2026-06-30 |
| Guardrails AI | continuous | 2024 | RAIL validator framework with Hub of pluggable validators | Apache 2.0 | - | https://github.com/guardrails-ai/guardrails/releases | 2026-06-30 |
| Protect AI llm-guard | continuous | 2024 | 16 input + 22 output scanners covering PII, secrets, toxicity, prompt injection, malicious URLs | MIT | - | https://github.com/protectai/llm-guard | 2026-06-30 |
| Protect AI rebuff | archived | 2023 | Multi-layer prompt injection detector (heuristics, vector-DB, LLM detector, canary tokens) | Apache 2.0 | Archived May 2025 | https://github.com/protectai/rebuff | 2026-06-30 |
| Protect AI modelscan | continuous | 2024 | ML model file scanner for pickle, H5, Keras, SavedModel | Apache 2.0 | - | https://github.com/protectai/modelscan/releases | 2026-06-30 |
| picklescan | continuous | 2024 | Pickle opcode-stream analyzer; underpins Hugging Face Hub-side scanning | MIT | - | https://github.com/mmaitre314/picklescan/releases | 2026-06-30 |
| Trail of Bits fickling | continuous | 2024 | Pickle decompiler, symbolic tracer, runtime import-hook with severity tiers | LGPL-3.0 | Copyleft caution for redistribution | https://github.com/trailofbits/fickling/releases | 2026-06-30 |
| Giskard | continuous | 2024 | AI testing platform with 55 probes across 11 categories; native AVID export | Apache 2.0 | - | https://github.com/Giskard-AI/giskard-oss/releases | 2026-06-30 |
| Confident AI deepteam | continuous | 2025 | Open-source LLM red-team framework with 50+ vulnerability categories incl. agentic-specific | Apache 2.0 | - | https://github.com/confident-ai/deepteam/releases | 2026-06-30 |
| promptfoo | continuous | 2024 | LLM eval and red-team with 71 plugin categories + 30 attack strategies; multi-framework compliance mapping | MIT | - | https://github.com/promptfoo/promptfoo/releases | 2026-06-30 |
| NVIDIA garak | continuous | 2024 | LLM vulnerability scanner with 40+ probe families | Apache 2.0 | - | https://github.com/NVIDIA/garak/releases | 2026-06-30 |
| Microsoft PyRIT | continuous | 2024 | Python Risk Identification Tool for GenAI red teaming with 75+ converters | MIT | - | https://github.com/microsoft/PyRIT/releases | 2026-06-30 |
| ETH Zurich AgentDojo | continuous | 2024 | Benchmark of tool-using LLM agents in simulated environments under prompt injection | MIT | Hosted on inspect_evals | https://github.com/ethz-spylab/agentdojo | 2026-06-30 |
| Vigil-LLM | continuous | 2023 | Prompt-injection and jailbreak detection toolkit; YARA + transformer + canary | Apache 2.0 | Alpha; dormant/unmaintained since 2024-01 (repository not archived on GitHub) | https://github.com/deadbits/vigil-llm | 2026-06-30 |
| Stacklok CodeGate | archived | 2024 | Local privacy and security gateway between IDE AI coding assistants and LLM providers | Apache 2.0 | Archived June 2025 | https://github.com/stacklok/codegate | 2026-06-30 |
| ClawGuard | continuous | 2026 | Runtime security sidecar daemon for tool-augmented LLM agents (OpenClaw) | MIT | V1.0 May 2026 | https://github.com/Claw-Guard/ClawGuard | 2026-06-30 |
| Lasso MCP Gateway | continuous | 2024 | Plugin-based local intermediary between MCP clients and downstream MCP servers with guardrail plugins | MIT | - | https://github.com/lasso-security/mcp-gateway | 2026-06-30 |
| jackhhao llm-warden | continuous | 2024 | Single-purpose jailbreak-prompt classifier | MIT | - | https://github.com/jackhhao/llm-warden | 2026-06-30 |
| TikiTribe claude-secure-coding-rules | continuous | 2024 | Claude Code secure-coding-rules repository with AI/agent/MCP/RAG security baselines | MIT | Referenced in dev-security CI gates | https://github.com/TikiTribe/claude-secure-coding-rules | 2026-06-30 |
| Wiz secure-rules-files | continuous | 2024 | Language and framework baseline rules for AI coding assistants | MIT | - | https://github.com/wiz-sec-public/secure-rules-files | 2026-06-30 |
| Kariedo claude-code-security-rules | continuous | 2024 | Modular Claude Code rules using @-syntax import | MIT | - | https://github.com/Kariedo/claude-code-security-rules | 2026-06-30 |
| awesome-ai-security | continuous | 2024 | Curated index of AI security, LLM security, prompt injection, red teaming, guardrail, and ML supply chain resources (approximately 20 categories) | CC0-1.0 | CC0; suitable for direct library reuse | https://github.com/brinhosa/awesome-ai-security | 2026-06-30 |

---

## Soft-law supervisory guidance

Soft-law guidance documents issued by supervisory authorities, regulators, or international working groups. Cited for interpretive guidance on formal regulations the corpus references.

| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |
|---|---|---|---|---| --- | --- |
| WP243 (Article 29 Working Party Guidelines on Data Protection Officers) | rev.01 | 2017-04 | Guidelines on Data Protection Officers ('DPOs') under GDPR Articles 37-39; endorsed by EDPB in May 2018 as part of the EDPB's adoption of WP29 guidelines. Cited for Article 38(6) conflict-of-interest interpretation. | WP243 (initial 2016-12 draft) | https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/index_en.htm | 2026-06-30 |
| WP216 (Article 29 Working Party Opinion 05/2014 on Anonymisation Techniques) | Original (no later revision) | 2014-04 | Opinion on anonymization vs pseudonymization, the singling-out / linkability / inference re-identification tests, adopted 10 April 2014 under Directive 95/46/EC and read across to the GDPR. Cited for anonymization thresholds. | - | https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/index_en.htm | 2026-06-30 |
| WP248 rev.01 (Article 29 Working Party Guidelines on Data Protection Impact Assessment) | rev.01 | 2017-10 | Guidelines on DPIA and determining whether processing is 'likely to result in a high risk' for the purposes of Regulation 2016/679 (GDPR Article 35), as last revised and adopted 4 October 2017; endorsed by the EDPB. Cited for DPIA methodology and the high-risk criteria. | WP248 (4 April 2017 first adoption) | https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/index_en.htm | 2026-06-30 |
| EDPB Guidelines 07/2020 (concepts of controller and processor in the GDPR) | Version 2.1 | 2021-07 | The controller, joint-controller, and processor concepts under the GDPR; Version 2.1 adopted 7 July 2021 after public consultation. Cited for controller / processor determination. | - | https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en | 2026-06-30 |
| EDPB Guidelines 3/2018 (territorial scope of the GDPR, Article 3) | Version 2.1 | 2019-11 | The establishment criterion and the targeting criterion for GDPR territorial scope (Article 3); Version 2.1 adopted 12 November 2019. Cited for extraterritorial applicability. | - | https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en | 2026-06-30 |
| EDPB Opinion 28/2024 (data protection aspects of AI models) | Original (no later revision) | 2024-12 | Whether an AI model trained on personal data can be anonymous, the legitimate-interest legal basis across AI development and deployment, and the consequences of unlawful processing in training; adopted 17 December 2024. Cited for AI-model data-protection analysis. | - | https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en | 2026-06-30 |

---

## Maintenance

- When a new version of a listed standard is published, update the **Current version** and **Publication date** columns, add the prior version to **Superseded versions**, and refresh **Last verified (UTC)** to the date the new version was confirmed upstream.
- When a standard is added to the library's citation usage, add an entry here before the citing PR merges, including its **Upstream check location** (fetch-confirmed) and **Last verified (UTC)** (or `needs-reconfirm` if it could not be confirmed at add time).
- **Version-currency re-check (advisory):** when a row is load-bearing and its **Last verified (UTC)** is `needs-reconfirm` or more than one week old, re-check the **Upstream check location** before relying on it and refresh the date in that PR (see the Conventions cadence note and [`specification-citation-verification.md`](specification-citation-verification.md)). This is a discipline, not a CI gate.
- The linter is permissive: it flags only patterns explicitly listed here as superseded. To catch a stale citation, the prior version must be listed under **Superseded versions**.
- Periodic review: at least quarterly, plus on publication of any major superseding version.

---

**End of Document**
