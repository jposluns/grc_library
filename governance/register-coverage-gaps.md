# Coverage Gap Analysis Register

**Document Title:** Coverage Gap Analysis Register\
**Document Type:** Register\
**Version:** 1.1.7\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-glossary.md`](register-glossary.md), [`README.md`](../README.md), [`TODO.md`](../TODO.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Quarterly, and upon completion of any phase that closes a recorded gap\
**Repository Path:** [`governance/register-coverage-gaps.md`](register-coverage-gaps.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the library's honest disclosure of what it does **not** yet cover. It exists so that adopting organisations can determine whether the library addresses their domain, sector, jurisdiction, or regulatory regime before they invest in adoption, and so contributors know where additions would have the most impact.

Coverage is recorded along five dimensions:

1. **Industry sectors**: vertical industry domains the library has or has not yet addressed.
2. **Jurisdictions**: country, regional, and supra-national regulatory regimes.
3. **Regulations and frameworks**: specific named instruments referenced in the library, with the depth of treatment recorded.
4. **Cloud and platform providers**: major hyperscalers and SaaS platforms.
5. **Technical capability areas**: domains within technology and operations.

Gaps may be **deliberately deferred** (recorded in [`TODO.md`](../TODO.md)), **out of scope** (not planned at all), or **in flight** (in active development on a feature branch).

This register is the source of truth for "is X covered?" questions. Where the library has substantive content, this register references it. Where it does not, this register says so.

---

## Conventions

For each entry:

- **Coverage**: one of *Substantive*, *Partial*, *Referenced*, *None*.
  - *Substantive*: one or more dedicated documents address the topic with sufficient depth for adoption.
  - *Partial*: addressed within broader documents; not given dedicated treatment.
  - *Referenced*: named or cited but without operational detail.
  - *None*: not covered.
- **Status**: *In library*, *Planned*, *Deferred*, *Out of scope*.
- **Planned target**: phase number, TODO priority, or "n/a".

---

## 1. Industry sectors

Industry sectors covered by `/compliance/<sector>/` sub-directories or otherwise addressed in the library.

| Sector | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Logistics (transportation, warehousing, freight forwarding, customs brokerage) | Substantive | In library | n/a | [`compliance/logistics/`](../compliance/logistics/) with BASC, CTPAT, AEO-UK, PIP overlays |
| Financial services (banks, investment, insurance, payment, FMI) | Substantive | In library | n/a | [`compliance/financial-services/`](../compliance/financial-services/) with DORA, SOX |
| Healthcare (providers, payers, medtech, healthcare platforms) | Substantive | In library | n/a | [`compliance/healthcare/`](../compliance/healthcare/) |
| Energy and utilities (electricity, gas, water, renewables) | Substantive | In library | n/a | [`compliance/energy-and-utilities/`](../compliance/energy-and-utilities/) |
| Telecommunications (telcos, ISPs, IXPs, electronic communications) | Substantive | In library | n/a | [`compliance/telecommunications/`](../compliance/telecommunications/) |
| Public sector (government agencies, public bodies, CSPs to public sector) | Substantive | In library | n/a | [`compliance/public-sector/`](../compliance/public-sector/) with FedRAMP |
| Manufacturing (industrial, automotive, consumer goods) | None | Deferred | TODO P6 | Likely cross-cuts with OT/ICS depth (TODO P6.2) and logistics |
| Retail and consumer goods | None | Deferred | TODO P6 | E-commerce-specific compliance, payment, consumer protection |
| Hospitality and travel | None | Deferred | TODO P6 | PCI DSS-heavy; some overlap with retail |
| Education | None | Deferred | TODO P6 | FERPA (US), student-data regulations per jurisdiction |
| Defence and aerospace | None | Out of scope | n/a | Highly jurisdiction- and clearance-specific; not appropriate for a CC BY-SA 4.0 library |
| Mining and extractive industries | None | Out of scope | n/a | Niche; would require subject-matter expertise the library does not have |
| Agriculture and food | None | Out of scope | n/a | Niche; HACCP and food-safety regulations are outside the library's information-security focus |
| Real estate and construction | None | Out of scope | n/a | Niche; minimal information-security overlap |
| Media and entertainment | None | Out of scope | n/a | Content licensing and IP-specific; outside library's scope |
| Gaming and online betting | None | Out of scope | n/a | Heavy jurisdictional regulation; specialized |
| Cannabis and regulated substances | None | Out of scope | n/a | Highly jurisdictional; specialized |

---

## 2. Jurisdictions

### 2.1 Privacy jurisdictions

The library's privacy domain has 25 jurisdiction-specific annexes in [`privacy/jurisdictions/`](../privacy/jurisdictions/). Coverage of major jurisdictions is generally substantive; the gaps below are known.

| Jurisdiction | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Argentina (PDPA 2025 update) | Partial | Planned | TODO P5.7 | Existing Latin America annex; Argentina-specific update pending |
| Saudi Arabia (PDPL 2023 update) | Partial | Planned | TODO P5.7 | Existing annex; recent regulatory updates not yet reflected |
| Mexico (LFPDPPP) | Partial | Planned | TODO P5.7 | Covered within Latin America annex; standalone annex possible |
| Israel | None | Deferred | TODO P5.7 | Privacy Protection Law and 2024 amendments |
| Egypt | None | Deferred | TODO P5.7 | PDPL 2020 |
| Bahrain | None | Deferred | TODO P5.7 | PDPL 2018 |
| Russia | None | Out of scope | n/a | Sanctions environment; not appropriate to actively curate |

### 2.2 Trade-security jurisdictions (trusted-trader programmes)

The library currently covers 4 of approximately 94 trusted-trader programmes globally.

| Jurisdiction / programme | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| BASC (multi-country, predominantly Latin America) | Substantive | In library | n/a | [`compliance/logistics/`](../compliance/logistics/) |
| US CTPAT | Substantive | In library | n/a | IT controls + MSC controls |
| UK AEO | Substantive | In library | n/a | Annex + self-assessment procedure |
| Canada PIP | Substantive | In library | n/a | IT controls register |
| EU AEO (27 member states) | None | Planned | TODO P5.1 | High-priority addition; covers all EU |
| Mexico NEEC / OEA | None | Planned | TODO P5.1 | High-priority addition; NAFTA/USMCA partner |
| Australia ATT (Authorised Trusted Trader) | None | Planned | TODO P5.1 | High-priority addition |
| Singapore STP / STP-Plus | None | Planned | TODO P5.1 | High-priority addition |
| Japan AEO | None | Planned | TODO P5.1 |  |
| Korea AEO | None | Planned | TODO P5.1 |  |
| New Zealand SES (Secure Exports Scheme) | None | Planned | TODO P5.1 |  |
| China AEO | None | Planned | TODO P5.1 |  |
| ~80 other WCO Member AEO programmes | None | Deferred | n/a | Cataloged in WCO AEO Compendium; added as adopters require |

### 2.3 Financial-services jurisdictions

| Jurisdiction / regulator | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| EU (DORA) | Substantive | In library | n/a | [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md) |
| US (SOX-ITGC) | Substantive | In library | n/a | [`compliance/financial-services/annex-sox-itgc.md`](../compliance/financial-services/annex-sox-itgc.md) |
| UK (PRA / FCA) | None | Planned | TODO P5.2 |  |
| US bank regulators (OCC, FRB, FDIC) | Referenced | Planned | TODO P5.2 | SOX covers reporting; bank-specific cyber expectations not yet detailed |
| US securities (SEC, FINRA) | Referenced | Planned | TODO P5.2 |  |
| Canada OSFI | None | Planned | TODO P5.2 |  |
| Australia APRA | None | Planned | TODO P5.2 |  |
| Singapore MAS | None | Planned | TODO P5.2 |  |
| Japan FSA | None | Planned | TODO P5.2 |  |
| Hong Kong HKMA | None | Deferred | TODO P5.2 |  |
| Switzerland FINMA | None | Deferred | TODO P5.2 |  |

### 2.4 Healthcare jurisdictions

| Jurisdiction / regulation | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| US HIPAA + HITECH | Referenced | Planned | TODO P5.3 | Cited in healthcare sector annex; dedicated detailed annex pending |
| EU MDR / IVDR | Referenced | Planned | TODO P5.3 |  |
| UK NHS DSPT | None | Planned | TODO P5.3 |  |
| Canada PHIPA and provincial frameworks | None | Planned | TODO P5.3 |  |
| Australia My Health Records Act | None | Planned | TODO P5.3 |  |

### 2.5 AI jurisdictions

The library cites the EU AI Act extensively in the AI domain but lacks dedicated per-jurisdiction AI annexes (parallel to the privacy/jurisdictions/ structure).

| Jurisdiction | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| EU (AI Act 2024/1689) | Referenced | Planned | TODO P5.8 | Heavy citation; dedicated jurisdiction annex would consolidate |
| Canada AIDA | Referenced | Planned | TODO P5.8 |  |
| UK AI regulatory framework | None | Planned | TODO P5.8 |  |
| US state-by-state (Colorado AI Act, NYC bias audit, etc.) | None | Planned | TODO P5.8 |  |
| China generative AI rules | None | Planned | TODO P5.8 |  |
| Korea AI framework | None | Planned | TODO P5.8 |  |

---

## 3. Regulations and frameworks referenced but not detailed

Regulations and frameworks named in the library but without dedicated operational treatment. Whether they need dedicated treatment depends on adopter demand.

| Instrument | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| ISO 9001 (quality management) | None | Out of scope | n/a | Quality management is outside the library's information-security/GRC scope |
| ISO 22301:2019 (business continuity) | Substantive | In library | n/a | Throughout resilience domain |
| ISO 31000:2018 (risk management) | Substantive | In library | n/a | Throughout risk domain |
| ISO 14001 (environmental management) | None | Out of scope | n/a | ESG content references it; not in scope for dedicated treatment |
| PCI DSS 4.0.1 | Referenced | Deferred | TODO P5.2 | Payments-specific; would fit under financial-services or as a sector annex |
| Basel III | Referenced | Deferred | TODO P5.2 | Banking-specific; would fit under financial-services |
| IEC 62443 (OT security) | Referenced | Planned | TODO P6.2 | High-priority for industrial/energy/logistics sectors |
| NERC CIP | Referenced | Planned | TODO P5.4 | High-priority for energy sector |
| SWIFT CSP (Customer Security Programme) | None | Deferred | TODO P5.2 | Financial-services payment networks |
| ITIL 4 | None | Out of scope | n/a | Service management framework; operational rather than governance |
| TOGAF | None | Out of scope | n/a | Architecture framework; operational |
| COBIT 2019 | Substantive | In library | n/a | Cited throughout governance and compliance |

---

## 4. Cloud and platform providers

The library is cloud-provider-agnostic. Provider-specific guidance is recorded as a known gap.

| Provider / platform | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Provider-agnostic cloud guidance | Substantive | In library | n/a | Throughout operations and supply-chain |
| AWS-specific overlays | None | Deferred | TODO P6.1 |  |
| Azure-specific overlays | None | Deferred | TODO P6.1 |  |
| GCP-specific overlays | None | Deferred | TODO P6.1 |  |
| Multi-cloud governance patterns | None | Deferred | TODO P6.1 |  |
| Kubernetes-specific governance | None | Deferred | TODO P6.1 | Could live in operations or dev-security |
| Serverless / FaaS-specific governance | None | Deferred | n/a |  |
| SaaS-specific SPM (Security Posture Management) | None | Deferred | n/a | Adjacent to supply-chain domain |

---

## 5. Technical capability areas

| Area | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Operational Technology (OT) security | Substantive | In library | n/a | [`operations/ot/`](../operations/ot/): overview annex (Phase 22.1), OT/ICS Security Standard (22.2), OT Incident Response Procedure (22.3), OT Change Management Procedure (22.4), OT Asset Inventory and Lifecycle Register (22.5), BMS Overlay Annex (22.6). IEC 62443 family and NIST SP 800-82 Rev 3 catalogued in canonical citations. |
| Identity governance (workforce IAM) | Substantive | In library | n/a | Throughout security domain |
| Customer Identity (CIAM) | Referenced | Deferred | TODO P6.3 | Adopter UX and consumer-data dimensions |
| Federated identity (SAML, OIDC) | Partial | In library | n/a | Referenced in IAM standards; dedicated patterns deferred |
| Quantum cryptography readiness | Substantive | In library | n/a | PQC roadmap exists; deepening planned in TODO P6.4 |
| Post-quantum crypto migration playbook | None | Deferred | TODO P6.4 |  |
| Crypto-agility patterns | None | Deferred | TODO P6.4 |  |
| AI/ML governance | Substantive | In library | n/a | Throughout AI domain |
| AI red-team methodology depth | Substantive | In library | n/a | Adversarial test reference, red team report template, agentic security standard with 16 threat classes, classical ML adversarial taxonomy, AI-driven offensive tool governance (§33 of agentic standard) all expanded across Phase 23 sub-phases |
| AI-driven offensive security tool governance | Substantive | In library | n/a | [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) §33 (OFFAI-SEC-01 to 10); tooling landscape register references PentestGPT, PentAGI, Strix, HexStrike AI, BurpGPT |
| ML model file scanning (pickle, H5, Keras, SavedModel) | Substantive | In library | n/a | SUPPLY-SEC-07 control in agentic standard; references modelscan, picklescan, fickling patterns |
| Multimodal AI threats (image, audio, video, OCR, PDF, QR) | Substantive | In library | n/a | RUNTIME-SEC-07 / 08 in agentic standard; TC-13 multimodal injection threat class |
| Agent goal stability and inter-agent communication compromise | Substantive | In library | n/a | AGENT-SEC-15 / 16; TC-14 / TC-15 threat classes |
| Classical ML adversarial taxonomy (evasion, poisoning, extraction, inference) | Substantive | In library | n/a | [`standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md) §5 restructured into 6 subsections covering ART/AIJack/HEART-equivalent threats |
| Citation verification methodology and freshness governance | Substantive | In library | n/a | [`specification-citation-verification.md`](specification-citation-verification.md); [`register-citation-verifications.md`](register-citation-verifications.md); [`register-canonical-citations.md`](register-canonical-citations.md); [`register-citation-verification-bundle.md`](register-citation-verification-bundle.md); [`lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py); [`lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py) |
| AI security tooling landscape (curated index) | Substantive | In library | n/a | [`register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md) with 55 entries across 9 categories, per-entry Provenance blocks |
| Audit programme (automated linting and conformance) | Substantive | In library | n/a | 40 gates running in CI on every PR (see [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6 for the canonical gate inventory); covers metadata, language, links, structure, citations, currency, filename/title, roles, uncertainty, CHANGELOG link coverage, placeholders, version monotonicity, date format, license consistency, stubs, section anchors, intra-doc refs, required sections, acronym consistency, secrets, PII, internal references, external link domains, cross-doc numbers, orphan documents, citation freshness, tooling freshness, version-date consistency, taxonomy/portal/scorecard regen-and-check, document Date staleness against git commit date, gate-name parity across surfaces, the linter regression test suite, claude-rules local-copy sync, section placement conventions, and cross-file gate-count consistency |
| MCP server security | Substantive | In library | n/a | Throughout AI domain; MCP-SEC-01 to 10 in agentic standard; [`register-mcp-server.md`](../ai/register-mcp-server.md); Lasso MCP Gateway pattern referenced |
| Generative AI specifically | Substantive | In library | n/a | Heavy coverage in AI domain |
| Synthetic data governance | Referenced | Deferred | n/a | Touched in AI data governance; could be dedicated |
| Data mesh / data product governance | None | Deferred | n/a | Architecture domain candidate |
| Privacy engineering patterns | Partial | In library | n/a | Privacy domain has principles and standards; pattern catalogue absent |
| Threat modelling methodologies | Referenced | Deferred | n/a | STRIDE, PASTA, ATT&CK-aligned; could be dedicated guide |
| Security chaos engineering | None | Out of scope | n/a | Emerging discipline; outside current scope |
| Bug bounty / responsible disclosure programmes | Partial | In library | n/a | Touched in security incident response; could be dedicated |

---

## 6. Document-type capability gaps

Within the library's doctype vocabulary, some types are under-represented relative to their natural use.

| Capability | Coverage | Status | Notes |
| --- | --- | --- | --- |
| Adopter quickstart templates per profile | None | Planned | TODO P4.1 |
| Interactive maturity assessment | None | Planned | TODO P4.2 (current scorecard is static) |
| Implementation roadmap templates | None | Planned | TODO P4.3 |
| Decision-tree adopter navigator | None | Planned | TODO P3.2 (Phase 21.8) |
| Worked examples / case studies | None | Out of scope | The library is organisation-neutral; case studies would conflict with that posture |
| Regulator interaction templates (notification, attestation, response) | Partial | Deferred | Some incident-notification language exists; consolidated template absent |
| Audit evidence package templates | Partial | Deferred | Per-control evidence is documented; consolidated audit-package templates absent |

---

## How this register is used

For adopters:

1. Search for the sector, jurisdiction, or regulation relevant to your organisation.
2. Read the **Coverage** and **Status** columns to set expectations.
3. Where coverage is *Substantive*, follow the link to the relevant library documents.
4. Where coverage is *None* or *Deferred*, check the **Planned target** column for the relevant TODO priority and consult [`TODO.md`](../TODO.md) for context.
5. Where coverage is *Out of scope*, expect the library to not address the topic; consider whether a parallel specialized resource is needed.

For contributors:

1. Identify *Planned* entries with TODO targets matching your contribution interest.
2. Update this register's **Coverage** and **Status** columns as part of the PR that closes a gap.
3. Add a new row when introducing coverage of a previously-unrecorded sector, jurisdiction, regulation, or capability.

---

## Maintenance

- Quarterly review by the Governance Library Maintainer to update statuses and add newly-identified gaps.
- Per-PR update when a phase closes a recorded gap.
- New rows may be added at any time when an adopter or contributor surfaces a gap not currently recorded.

---

**End of Document**
