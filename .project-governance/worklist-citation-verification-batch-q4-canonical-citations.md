# Citation Verification Worklist - Batch Q4: Remaining Canonical Citations

**Document Title:** Citation Verification Worklist: Batch Q4 (Remaining Canonical Citations)\
**Document Type:** Worklist\
**Version:** 1.0.7\
**Date:** 2026-07-01\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](../governance/specification-citation-verification.md), [`governance/template-citation-verification-worklist.md`](../governance/template-citation-verification-worklist.md), [`.project-governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md), [`.project-governance/register-citation-verification-bundle.md`](register-citation-verification-bundle.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** This worklist is a per-batch working artefact; the authoritative record is the Citation Verifications Register.\
**Repository Path:** [`.project-governance/worklist-citation-verification-batch-q4-canonical-citations.md`](worklist-citation-verification-batch-q4-canonical-citations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

Verification batch Q4 covers the 82 canonical citation entries that are not in scope of the Q2 (ISO/IEC, 24 entries) or Q3 (tooling provenance, 55 entries) batches. Together with Q2 and Q3, this completes the human-verifier workflow for the entire canonical citations register and tooling landscape register.

Per the Citation Verification Specification ([`specification-citation-verification.md`](../governance/specification-citation-verification.md)) §8 and the AI/human operating model in §3, the AI verifier has pre-filled this worklist's expected publisher URLs, expected values, and field-to-verify columns. The human verifier executes the browser fetches, captures verbatim text, submits Wayback snapshots, assigns confidence ratings, and signs the captured-by column.

---

## 2. Execution guidance

Work by publisher cluster (sections below) rather than alphabetically. Each section corresponds to one publisher and can be executed in one browser-tab session.

For each row:

1. Open the **Expected primary URL** in a browser. Confirm domain match and TLS.
2. Locate the publisher-page text supporting the **Expected value**. Copy verbatim into **Captured text**.
3. Submit the URL to `https://web.archive.org/save/<url>` and record the resulting snapshot URL in **Wayback URL**.
4. Compare publisher metadata to **Expected value**; record **Result** (Match / Diverged / Not found) and any **Divergence detail**.
5. Assign **Confidence** per Citation Verification Specification §10.
6. Sign **Captured by**.

At batch close: notify AI verifier with completed worklist. AI verifier transcribes into Citation Verifications Register and proposes any register corrections.

Particular-attention flags (entries where AI-verifier confidence is lowest):

- **OWASP Agentic AI Top 10 2026**: confirm published; release timing uncertain.
- **OWASP MCP Top 10 2025**: confirm published.
- **Meta CyberSecEval v4**: confirm v4 is current (v3 was earlier).
- **MITRE ATT&CK v19.1**: verified current 2026-06-28 against the upstream authority (was v15; attack-stix-data release v19.1, 2026-05-12).
- **MITRE ATLAS v2026.06**: re-verified current 2026-07-01 (#512) against the upstream authority; the 2026-06-28 batch check had found v2026.05 current (was v4.7; atlas-data new YAML/CalVer format v6.0.0), and the v2026.06 monthly content update published 2026-06-30 superseded it.
- **CSA AICM v1.1**: verify current version.
- **Basel III**: multiple amendments since 2017; verify current state.
- **NFPA 72 2025**: confirm 2025 edition published.

---

## 3. Worklist (by publisher cluster)

### 3.1 NIST cluster (10 entries): publishers `nvlpubs.nist.gov`, `csrc.nist.gov`, `nist.gov`

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NIST SP 800-34 | https://csrc.nist.gov/pubs/sp/800/34/r1/final | all | Rev. 1, 2010-05, Contingency Planning Guide for Federal Information Systems |  |  |  |  |  |  |
| NIST SP 800-53 | https://csrc.nist.gov/pubs/sp/800/53/r5/final | all | Rev. 5, 2020-09, Security and Privacy Controls; supersedes Rev. 4 |  |  |  |  |  |  |
| NIST SP 800-88 | https://csrc.nist.gov/pubs/sp/800/88/r1/final | all | Rev. 1, 2014-12, Media sanitization |  |  |  |  |  |  |
| NIST SP 800-207 | https://csrc.nist.gov/pubs/sp/800/207/final | all | 1.0, 2020-08, Zero Trust Architecture |  |  |  |  |  |  |
| NIST CSF | https://www.nist.gov/cyberframework | all | 2.0, 2024-02, Cybersecurity Framework; supersedes 1.1 |  |  |  |  |  |  |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | all | 1.0, 2023-01, AI Risk Management Framework |  |  |  |  |  |  |
| NIST AI 600-1 | https://csrc.nist.gov/pubs/ai/600/1/final | all | 1.0, 2024-07, Generative AI Profile for AI RMF |  |  |  |  |  |  |
| NIST SP 800-218 | https://csrc.nist.gov/pubs/sp/800/218/final | all | 1.1, 2022-02, Secure Software Development Framework (SSDF); supersedes 1.0 |  |  |  |  |  |  |
| NIST SP 800-218A | https://csrc.nist.gov/pubs/sp/800/218/a/final | all | Final, 2024, Secure SDF GenAI profile |  |  |  |  |  |  |
| NIST SP 800-161 | https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final | all | Rev. 1, 2022-05, Cybersecurity Supply Chain Risk Management; supersedes Rev. 0 |  |  |  |  |  |  |
| NIST SP 800-82 | https://csrc.nist.gov/pubs/sp/800/82/r3/final | all | Rev. 3, 2023-09, Guide to OT Security; supersedes Rev. 2, Rev. 1 |  |  |  |  |  |  |

### 3.2 EU regulations and directives (9 entries): publisher `eur-lex.europa.eu`

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EU AI Act | https://eur-lex.europa.eu/eli/reg/2024/1689 | all | Regulation 2024/1689, 2024-07, AI regulation |  |  |  |  |  |  |
| EU NIS 2 Directive | https://eur-lex.europa.eu/eli/dir/2022/2555 | all | Directive 2022/2555, 2022-12; supersedes NIS Directive 2016/1148 |  |  |  |  |  |  |
| EU DORA | https://eur-lex.europa.eu/eli/reg/2022/2554 | all | Regulation 2022/2554, 2022-12, Digital Operational Resilience Act |  |  |  |  |  |  |
| EU GDPR | https://eur-lex.europa.eu/eli/reg/2016/679 | all | Regulation 2016/679, 2016-04, General Data Protection Regulation; supersedes Directive 95/46/EC |  |  |  |  |  |  |
| EU eIDAS | https://eur-lex.europa.eu/eli/reg/2024/1183 | all | Regulation 2024/1183 (eIDAS 2), 2024-04; supersedes Regulation 910/2014 (eIDAS 1) |  |  |  |  |  |  |
| EU EECC | https://eur-lex.europa.eu/eli/dir/2018/1972 | all | Directive 2018/1972, 2018-12, European Electronic Communications Code |  |  |  |  |  |  |
| EU MDR | https://eur-lex.europa.eu/eli/reg/2017/745 | all | Regulation 2017/745, 2017-04, Medical Device Regulation; supersedes Directive 93/42/EEC |  |  |  |  |  |  |
| EU IVDR | https://eur-lex.europa.eu/eli/reg/2017/746 | all | Regulation 2017/746, 2017-04, In-Vitro Diagnostic Regulation; supersedes Directive 98/79/EC |  |  |  |  |  |  |
| EU UCC | https://eur-lex.europa.eu/eli/reg/2013/952 | all | Regulation 952/2013, 2013-10, Union Customs Code |  |  |  |  |  |  |

### 3.3 North-American regulations (10 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US HIPAA | https://www.hhs.gov/hipaa/index.html | all | 1996 (with HITECH 2009 and Omnibus 2013 amendments) |  |  |  |  |  |  |
| US HITECH | https://www.hhs.gov/hipaa/for-professionals/special-topics/hitech-act-enforcement-interim-final-rule/index.html | all | 2009, HITECH Act |  |  |  |  |  |  |
| US SOX | https://www.congress.gov/bill/107th-congress/house-bill/3763 | all | 2002-07, Sarbanes-Oxley Act |  |  |  |  |  |  |
| US CCPA | https://oag.ca.gov/privacy/ccpa | all | 2018 (with CPRA 2020 amendments) |  |  |  |  |  |  |
| US FedRAMP | https://www.fedramp.gov/rev5-baselines/ | all | Rev. 5, 2023, aligned with NIST SP 800-53 Rev. 5; supersedes Rev. 4 |  |  |  |  |  |  |
| US CMMC | https://dodcio.defense.gov/CMMC/ | all | 2.0, 2024, Cybersecurity Maturity Model Certification; supersedes 1.0, 1.02 |  |  |  |  |  |  |
| Canada CPPA | https://www.parl.ca/legisinfo/en/bill/44-1/c-27 | all | 2022 (pending enactment); replaces PIPEDA |  |  |  |  |  |  |
| Canada PIPEDA | https://laws-lois.justice.gc.ca/eng/acts/P-8.6/ | all | 2000 (with 2015 DBSA amendments) |  |  |  |  |  |  |
| Canada AIDA | https://www.parl.ca/legisinfo/en/bill/44-1/c-27 | all | 2022 (pending enactment), Artificial Intelligence and Data Act |  |  |  |  |  |  |
| Quebec Law 25 | https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1 | all | 2021 (phased in 2022-2024), An Act to modernize legislative provisions as regards protection of personal information |  |  |  |  |  |  |

### 3.4 Other privacy regulations (7 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UK GDPR | https://www.legislation.gov.uk/ukpga/2018/12/contents | all | 2018 (Data Protection Act 2018), UK GDPR |  |  |  |  |  |  |
| Brazil LGPD | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm | all | 2018 (in force 2020), Lei Geral de Proteção de Dados |  |  |  |  |  |  |
| China PIPL | (search npc.gov.cn for "Personal Information Protection Law 2021") | all | 2021-11, Personal Information Protection Law |  |  |  |  |  |  |
| Switzerland nFADP | https://www.fedlex.admin.ch/eli/cc/2022/491/en | all | 2023-09, New Federal Act on Data Protection; supersedes FADP 1992 |  |  |  |  |  |  |
| Saudi Arabia PDPL | https://sdaia.gov.sa/en/SDAIA/about/Files/PersonalDataEnglishV2.pdf | all | 2023-09, Personal Data Protection Law |  |  |  |  |  |  |
| Singapore PDPA | https://www.pdpc.gov.sg/Overview-of-PDPA/The-Legislation/Personal-Data-Protection-Act | all | 2012 (with 2020 amendments), Personal Data Protection Act |  |  |  |  |  |  |
| Australia Privacy Act | https://www.oaic.gov.au/privacy/the-privacy-act | all | 1988 (with 2024 amendments), Privacy Act |  |  |  |  |  |  |

### 3.5 CSA / ISACA frameworks (4 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CSA CCM | https://cloudsecurityalliance.org/research/cloud-controls-matrix | all | v4.1, 2024, Cloud Controls Matrix; supersedes v3.0.1, v4.0 |  |  |  |  |  |  |
| CSA AICM | https://cloudsecurityalliance.org/research/ai-controls-matrix | all | v1.0.3, 2025, AI Controls Matrix; supersedes v1.0.0, v1.0.1, v1.0.2 |  |  |  |  |  |  |
| CSA STAR | https://cloudsecurityalliance.org/star | all | Continuous, Security Trust Assurance and Risk programme |  |  |  |  |  |  |
| COBIT | https://www.isaca.org/resources/cobit | all | 2019, 2018-11 (with Design/Implementation Guide updates 2019, 2020); supersedes COBIT 5, COBIT 4.1; "COBIT 2025" is hallucinated |  |  |  |  |  |  |

### 3.6 Cybersecurity adversary frameworks (6 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MITRE ATT&CK | https://attack.mitre.org/ | all | v19.1, 2026-05 (verified current 2026-06-28; was v15, 2024-10) |  |  |  |  |  |  |
| MITRE ATLAS | https://atlas.mitre.org/ | all | v2026.05, 2026-05 (verified current 2026-06-28; superseded 2026-06-30 by v2026.06, re-verified 2026-07-01 per #512; was v4.7, 2024) |  |  |  |  |  |  |
| AVID | https://avidml.org/ | all | continuous, 2023, AI Vulnerability Database |  |  |  |  |  |  |
| MLCommons AILuminate | https://mlcommons.org/benchmarks/ailuminate/ | all | v1.0, 2024, AI risk taxonomy and benchmark with 14-category hazard taxonomy |  |  |  |  |  |  |
| HarmBench | https://www.harmbench.org/ | all | continuous, 2024-02, Standardized evaluation framework |  |  |  |  |  |  |
| OWASP GenAI Security Project | https://genai.owasp.org/ | all | continuous, 2024 |  |  |  |  |  |  |

### 3.7 OWASP (6 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OWASP Top 10 | https://owasp.org/Top10/ | all | 2021; supersedes 2017 (note: 2025 edition may now be current) |  |  |  |  |  |  |
| OWASP LLM Top 10 | https://genai.owasp.org/llm-top-10/ | all | 2025; supersedes 2023 |  |  |  |  |  |  |
| OWASP Agentic AI Top 10 | https://genai.owasp.org/owasp-top-10-for-agentic-ai/ | all | 2026 (confirm published) |  |  |  |  |  |  |
| OWASP MCP Top 10 | https://owasp.org/www-project-mcp-top-10/ | all | 2025 (confirm published) |  |  |  |  |  |  |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | all | 4.0.3, 2021; supersedes 3.0 (note: v5 may now be released) |  |  |  |  |  |  |
| OWASP SAMM | https://owaspsamm.org/ | all | 2.0, 2020; supersedes 1.5 |  |  |  |  |  |  |

### 3.8 Customs and trade (3 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WCO SAFE Framework | https://www.wcoomd.org/en/topics/facilitation/instrument-and-tools/frameworks-of-standards/safe_package.aspx | all | 2021, WCO SAFE Framework of Standards; supersedes 2018 |  |  |  |  |  |  |
| BASC International Standard | https://www.wbasco.org/en/programs-of-certification | all | v6 (2023); supersedes v5 |  |  |  |  |  |  |
| CTPAT MSC | https://www.cbp.gov/border-security/ports-entry/cargo-security/ctpat | all | 2020, Minimum Security Criteria |  |  |  |  |  |  |

### 3.9 Sector-specific: IEC 62443 family (7 entries): publisher `webstore.iec.ch`

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IEC 62443-1-1 | https://webstore.iec.ch/publication/7029 | all | 2009, Concepts and models |  |  |  |  |  |  |
| IEC 62443-2-1 | https://webstore.iec.ch/publication/61337 | all | 2024, IACS security programme; supersedes 2010 |  |  |  |  |  |  |
| IEC 62443-2-4 | https://webstore.iec.ch/publication/63752 | all | 2023, Service providers; supersedes 2015 |  |  |  |  |  |  |
| IEC 62443-3-2 | https://webstore.iec.ch/publication/30727 | all | 2020, Security risk assessment for system design |  |  |  |  |  |  |
| IEC 62443-3-3 | https://webstore.iec.ch/publication/7033 | all | 2013, System security requirements and security levels |  |  |  |  |  |  |
| IEC 62443-4-1 | https://webstore.iec.ch/publication/33615 | all | 2018, Secure product development lifecycle requirements |  |  |  |  |  |  |
| IEC 62443-4-2 | https://webstore.iec.ch/publication/34421 | all | 2019, Technical security requirements for IACS components |  |  |  |  |  |  |

### 3.10 Sector-specific: functional safety + BMS + fire + pipeline + banking (10 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IEC 61511 | https://webstore.iec.ch/publication/24241 | all | 2016 (Edition 2, Amendment 1 in 2017); supersedes Edition 1 (2003) |  |  |  |  |  |  |
| IEC 61508 | https://webstore.iec.ch/publication/22273 | all | 2010, Functional safety; supersedes 1998 |  |  |  |  |  |  |
| ISO 16484 | https://www.iso.org/standard/72074.html | all | Parts published 2010 to 2020, BACS |  |  |  |  |  |  |
| ASHRAE 135 | https://www.ashrae.org/technical-resources/bookstore/standard-135 | all | 2020 (with addenda), BACnet protocol |  |  |  |  |  |  |
| NIST SP 1900 series | https://www.nist.gov/programs-projects/cyber-physical-systems | all | 2023, Smart-building cybersecurity and IoT |  |  |  |  |  |  |
| NFPA 72 | https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=72 | all | 2025, National Fire Alarm and Signaling Code; supersedes 2022, 2019 |  |  |  |  |  |  |
| EN 54 | https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:6196,25 | all | Series, current parts published 2017 to 2023 |  |  |  |  |  |  |
| TSA Pipeline Security Directive | https://www.tsa.gov/sites/default/files/sd-pipeline-2021-02c.pdf | all | SD02 (with subsequent revisions), 2021 initial, revised through 2024 |  |  |  |  |  |  |
| Basel III | https://www.bis.org/basel_framework/ | all | 2017 (with 2023 finalisation, in force 2025); supersedes Basel II |  |  |  |  |  |  |
| NERC CIP | https://www.nerc.com/pa/Stand/Pages/CIPStandards.aspx | all | 014-3 (latest revision), various |  |  |  |  |  |  |
| PCI DSS | https://www.pcisecuritystandards.org/document_library/?category=pcidss | all | 4.0.1, 2024-06; supersedes 3.2.1, 4.0 |  |  |  |  |  |  |

### 3.11 OECD and global / ICAO / IMO (6 entries)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OECD AI Principles | https://oecd.ai/en/ai-principles | all | 2024 updated, AI policy principles; supersedes 2019 |  |  |  |  |  |  |
| OECD Privacy Guidelines | https://www.oecd.org/digital/ieconomy/privacy-guidelines.htm | all | 2013 revised, Privacy and transborder data flows; supersedes 1980 |  |  |  |  |  |  |
| WTO TFA | https://www.wto.org/english/tratop_e/tradfa_e/tradfa_e.htm | all | 2017, Trade Facilitation Agreement |  |  |  |  |  |  |
| ICAO Doc 10026 | https://store.icao.int/en/doc-10026-manual-on-aviation-security | all | 2nd edition, 2024; supersedes 1st edition |  |  |  |  |  |  |
| ICAO Doc 10055 | https://store.icao.int/en/aviation-cybersecurity-strategy-doc-10055 | all | 2024, Aviation Cybersecurity Strategy |  |  |  |  |  |  |
| IMO Resolution MSC-FAL.1/Circ.3 | https://www.imo.org/en/OurWork/Security/Pages/Cyber-security.aspx | all | Rev. 2, 2022-06, Maritime cyber risk management guidelines; supersedes Rev. 1 |  |  |  |  |  |  |

### 3.12 AI safety evaluation programmes (3 entries; note that AI tooling references cluster separately covered in Q3)

| Standard ID | Expected primary URL | Field(s) | Expected value | Captured text | Wayback URL | Result | Captured by | Confidence | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UK AISI inspect_evals | https://inspect.aisi.org.uk/evals/ | all | Continuous, 2024, UK AI Safety Institute community evaluation catalogue |  |  |  |  |  |  |
| Meta CyberSecEval | https://github.com/meta-llama/PurpleLlama/tree/main/CybersecurityBenchmarks | all | v4, 2025, Offensive cyber benchmark; supersedes v3, v2, v1 |  |  |  |  |  |  |
| NIST SP 800-218A | https://csrc.nist.gov/pubs/sp/800/218/a/final | all | Final, 2024, Secure SDF GenAI profile (duplicate of NIST cluster row; verify once) |  |  |  |  |  |  |

---

## 4. Total verification rows

| Cluster | Entry count |
| --- | --- |
| 3.1 NIST | 11 |
| 3.2 EU regulations and directives | 9 |
| 3.3 North-American regulations | 10 |
| 3.4 Other privacy regulations | 7 |
| 3.5 CSA / ISACA | 4 |
| 3.6 Cybersecurity adversary frameworks | 6 |
| 3.7 OWASP | 6 |
| 3.8 Customs and trade | 3 |
| 3.9 IEC 62443 family | 7 |
| 3.10 Sector-specific (functional safety + BMS + fire + pipeline + banking + NERC + PCI) | 11 |
| 3.11 OECD / global / ICAO / IMO | 6 |
| 3.12 AI safety evaluation programmes | 3 |
| **Total Q4** | **83** |

(83 not 82: NIST SP 800-218A appears both in NIST cluster and AI safety evaluation cluster; verify once and cross-reference both register entries.)

---

## 5. Closing notes

| Field | Value |
| --- | --- |
| Batch identifier | Q4 - Remaining Canonical Citations |
| Standards in batch | 82 unique (83 worklist rows with one cross-cluster overlap) |
| Batch opened | 2026-05-30 |
| Batch closed |  |
| Spot-check entries (per Citation Verification Specification §8.6) |  |
| Spot-check verifier |  |
| Recorded register rows |  |

---

## 6. After batch close

When the batch is complete:

1. The human verifier notifies the AI verifier with the completed worklist.
2. The AI verifier appends one row per worklist row to the Citation Verifications Register, faithfully reproducing the captured text.
3. The AI verifier proposes any corrections to the Canonical Citations Register for human approval (e.g., updating "current version" or "publication date" where the publisher page differs).
4. The AI verifier identifies any downstream library references that need updating to match corrected register values.

---

**End of Document**
