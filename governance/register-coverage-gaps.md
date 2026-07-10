# Coverage Gap Analysis Register

**Document Title:** Coverage Gap Analysis Register\
**Document Type:** Register\
**Version:** 1.1.30\
**Date:** 2026-07-10\
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

This register is the library's honest disclosure of what it does **not** yet cover. It exists so that adopting organizations can determine whether the library addresses their domain, sector, jurisdiction, or regulatory regime before they invest in adoption, and so contributors know where additions would have the most impact.

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
  - *Partial*: materially addressed by shipped documents, broader or adjacent dedicated, while the row's named ask remains unshipped.
  - *Referenced*: named or cited but without operational detail.
  - *None*: not covered.
- **Status**: *In library*, *Planned*, *Deferred*, *Out of scope*.
- **Planned target**: phase number, a stable TODO backlog topic (`TODO backlog: <topic>`), a backlog candidate not currently scheduled (`Backlog candidate: <topic>`), or "n/a".

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
| Manufacturing (industrial, automotive, consumer goods) | Partial | Deferred | Backlog candidate: manufacturing sector overlay (not currently scheduled in TODO) | Re-graded None to Partial 2026-07-02 (the #581 sweep's I-1): the operations OT suite (six documents plus README, graded Substantive in section 5) addresses industrial and ICS environments within broader and adjacent dedicated documents; the manufacturing sector overlay itself remains the gap. Likely cross-cuts with logistics |
| Retail and consumer goods | None | Deferred | Backlog candidate: retail sector overlay (not currently scheduled in TODO) | E-commerce-specific compliance, payment, consumer protection |
| Hospitality and travel | None | Deferred | Backlog candidate: hospitality sector overlay (not currently scheduled in TODO) | PCI DSS-heavy; some overlap with retail |
| Education | None | Deferred | Backlog candidate: education sector overlay (not currently scheduled in TODO) | FERPA (US), student-data regulations per jurisdiction |
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

The library's privacy domain has 26 jurisdiction-specific annexes in [`privacy/jurisdictions/`](../privacy/jurisdictions/). Coverage of major jurisdictions is generally substantive; the gaps below are known.

| Jurisdiction | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Argentina (PDPA 2025 update) | Partial | Planned | TODO backlog: privacy jurisdiction gaps | Existing Latin America annex; Argentina-specific update pending |
| Saudi Arabia (PDPL 2023 update) | Partial | Planned | TODO backlog: privacy jurisdiction gaps | Existing annex; recent regulatory updates not yet reflected |
| Mexico (LFPDPPP 2025) | Substantive | In library | n/a | Dedicated standalone annex [`privacy/jurisdictions/annex-privacy-mexico.md`](../privacy/jurisdictions/annex-privacy-mexico.md) (2025 LFPDPPP, Secretaría Anticorrupción y Buen Gobierno authority, ARCO rights, UMA fines); the Latin America annex Mexico section defers to it |
| Israel | None | Deferred | TODO backlog: privacy jurisdiction gaps | Privacy Protection Law and 2024 amendments |
| Egypt | None | Deferred | TODO backlog: privacy jurisdiction gaps | PDPL 2020 |
| Bahrain | None | Deferred | TODO backlog: privacy jurisdiction gaps | PDPL 2018 |
| Russia | None | Out of scope | n/a | Sanctions environment; not appropriate to actively curate |

### 2.2 Trade-security jurisdictions (trusted-trader programmes)

The library currently covers 4 of approximately 94 trusted-trader programmes globally.

| Jurisdiction / programme | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| BASC (multi-country, predominantly Latin America) | Substantive | In library | n/a | [`compliance/logistics/`](../compliance/logistics/) |
| US CTPAT | Substantive | In library | n/a | IT controls + MSC controls |
| UK AEO | Substantive | In library | n/a | Annex + self-assessment procedure |
| Canada PIP | Substantive | In library | n/a | IT controls register |
| EU AEO (27 member states) | Referenced | Planned | TODO backlog: logistics country / programme expansion | High-priority addition; covers all EU. Re-graded None to Referenced 2026-07-02: mutual-recognition prose in the Canada PIP controls register and AEO (EU) columns and rows in the supply-chain programme-alignment matrix (the Union Customs Code row, the CTPAT and AEO-S mutual-recognition rows); arguably Partial on the matrix evidence, kept at the conservative grade until the dedicated annex ships |
| Mexico NEEC / OEA | Referenced | Planned | TODO backlog: logistics country / programme expansion | High-priority addition; NAFTA/USMCA partner. Re-graded None to Referenced 2026-07-03 (the #586 sweep's M-1): the supply-chain programme-alignment matrix carries a full NEEC programme-profile row, a NEEC domain column, shared-evidence rows, and application-priority and contacts rows (the columns-and-rows class that re-graded EU AEO), and the logistics README's candidates list and the glossary name the programme; unlike EU AEO it has no mutual-recognition pair rows, so the conservative grade holds until the dedicated annex ships |
| Brazil OEA (Operador Econômico Autorizado) | Referenced | Planned | TODO backlog: logistics country / programme expansion | Row added 2026-07-03 (the #586 sweep's M-1): the supply-chain programme-alignment matrix carries a full OEA programme-profile row, an OEA domain column, shared-evidence rows, two mutual-recognition rows (the AEO-S and EU AEO pairs), and application-priority and contacts rows (the columns-and-rows class that re-graded EU AEO, here including the pair rows EU AEO's own grade rested on); distinct from Mexico's programme of the same OEA name; kept at the conservative grade until the dedicated annex ships |
| Australia ATT (Australian Trusted Trader) | Referenced | Planned | TODO backlog: logistics country / programme expansion | High-priority addition. Re-graded None to Referenced 2026-07-03 (the #586 sweep's L-2): named in the logistics README's future-addition candidates list and the glossary (the candidates-list class that re-graded My Health Records); no operational detail |
| Singapore STP / STP-Plus | Referenced | Planned | TODO backlog: logistics country / programme expansion | High-priority addition. Re-graded None to Referenced 2026-07-03 (the #586 sweep's L-2): named in the logistics README's candidates list (STP) and the glossary (both STP and the STP-Plus enhanced tier); no operational detail |
| Japan AEO | Referenced | Planned | TODO backlog: logistics country / programme expansion | Re-graded None to Referenced 2026-07-03 (the #586 sweep's L-2): named in the logistics README's candidates list and in the supply-chain matrix's CTPAT mutual-recognition cell; no operational detail |
| Korea AEO | Referenced | Planned | TODO backlog: logistics country / programme expansion | Re-graded None to Referenced 2026-07-03 (the #586 sweep's L-2): named in the logistics README's candidates list and in the supply-chain matrix's CTPAT mutual-recognition cell; no operational detail |
| New Zealand SES (Secure Exports Scheme) | Referenced | Planned | TODO backlog: logistics country / programme expansion | Re-graded None to Referenced 2026-07-03 (the #586 sweep's L-2): named in the logistics README's candidates list and the glossary; no operational detail |
| China AEO | None | Planned | TODO backlog: logistics country / programme expansion |  |
| ~80 other WCO Member AEO programmes | None | Deferred | n/a | Cataloged in WCO AEO Compendium; added as adopters require |

### 2.3 Financial-services jurisdictions

| Jurisdiction / regulator | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| EU (DORA) | Substantive | In library | n/a | [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md) |
| US (SOX-ITGC) | Substantive | In library | n/a | [`compliance/financial-services/annex-sox-itgc.md`](../compliance/financial-services/annex-sox-itgc.md) |
| UK (PRA / FCA) | Partial | Planned | TODO backlog: financial-services country regulator overlays | Re-graded None to Partial 2026-07-02: the financial-services annex carries UK regime rows (FCA PS21/3, PRA SS1/21, the CTPs regime) plus a dedicated FCA/PRA operational-resilience mapping section; the dedicated regulator overlay remains the gap |
| US bank regulators (OCC, FRB, FDIC) | Referenced | Planned | TODO backlog: financial-services country regulator overlays | SOX covers reporting; bank-specific cyber expectations not yet detailed |
| US securities (SEC, FINRA) | Referenced | Planned | TODO backlog: financial-services country regulator overlays |  |
| Canada OSFI | Partial | Planned | TODO backlog: financial-services country regulator overlays | Re-graded None to Partial 2026-07-02: the financial-services annex carries Canada regime rows (B-13, B-10, B-7) plus a dedicated OSFI B-13 mapping section; the dedicated regulator overlay remains the gap |
| Australia APRA | Referenced | Planned | TODO backlog: financial-services country regulator overlays | Re-graded None to Referenced 2026-07-02: regime-table row in the financial-services annex (CPS 234, CPS 230), named structurally without operational detail per the annex's own Asia-Pacific note |
| Singapore MAS | Referenced | Planned | TODO backlog: financial-services country regulator overlays | Re-graded None to Referenced 2026-07-02: regime-table row in the financial-services annex (MAS TRM Guidelines, Cyber Hygiene Notice), named structurally without operational detail per the annex's own Asia-Pacific note |
| Japan FSA | Referenced | Planned | TODO backlog: financial-services country regulator overlays | Re-graded None to Referenced 2026-07-02: regime-table row in the financial-services annex (JFSA system-risk and cybersecurity guidelines), named structurally without operational detail per the annex's own Asia-Pacific note |
| Hong Kong HKMA | Referenced | Deferred | TODO backlog: financial-services country regulator overlays | Re-graded None to Referenced 2026-07-02: regime-table row in the financial-services annex (Supervisory Policy Manual technology and operational-risk modules), named structurally without operational detail per the annex's own Asia-Pacific note |
| Switzerland FINMA | Referenced | Deferred | TODO backlog: financial-services country regulator overlays | Re-graded None to Referenced 2026-07-02: regime-table row in the financial-services annex's Switzerland subsection (the FINMA operational-risks-and-resilience circular), named structurally without operational detail per the annex's own note |

### 2.4 Healthcare jurisdictions

| Jurisdiction / regulation | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| US HIPAA + HITECH | Substantive | In library | n/a | Dedicated US operational overlay [`compliance/healthcare/annex-healthcare-united-states.md`](../compliance/healthcare/annex-healthcare-united-states.md) (Security/Privacy/Breach/Enforcement rule-by-rule plus the NIST SP 800-66r2 crosswalk), the [HIPAA operational procedure](../compliance/healthcare/procedure-hipaa-operational-compliance.md), and the sector annex overview |
| EU MDR / IVDR | Referenced | Planned | TODO backlog: healthcare country regulator overlays |  |
| UK NHS DSPT | Partial | Planned | TODO backlog: healthcare country regulator overlays | Re-graded None to Partial 2026-07-02: healthcare-annex regime row plus a dedicated NHS DSPT mapping section (the 10 National Data Guardian standards mapped to library documents); the dedicated overlay remains the gap |
| Canada PHIPA and provincial frameworks | Referenced | Planned | TODO backlog: healthcare country regulator overlays | Re-graded None to Referenced 2026-07-02: healthcare-annex Canada regime rows name PHIPA and the provincial frameworks (Alberta PIPA and HIA, Manitoba and Nova Scotia PHIA); no operational mapping yet |
| Australia My Health Records Act | Referenced | Planned | TODO backlog: healthcare country regulator overlays | Re-graded None to Referenced 2026-07-02: named only in the healthcare README's future-coverage candidates list, the same evidence class the US-securities row's FINRA half already grades Referenced; the weakest re-grade of the batch, disclosed as such |

### 2.5 AI jurisdictions

The library cites the EU AI Act extensively in the AI domain. The `ai/jurisdictions/` structure (parallel to `privacy/jurisdictions/`) was founded by the EU AI Act annex; other AI jurisdictions remain source-gated.

| Jurisdiction | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| EU (AI Act 2024/1689) | Substantive | In library | n/a | Dedicated jurisdiction annex [`ai/jurisdictions/annex-ai-european-union.md`](../ai/jurisdictions/annex-ai-european-union.md) (per-regime consolidated view: operator roles, risk tiers, obligation chains, timeline, penalties), founding the `ai/jurisdictions/` structure |
| Canada AIDA | Referenced | Planned | TODO backlog: AI jurisdiction overlays |  |
| UK AI regulatory framework | Partial | Planned | TODO backlog: AI jurisdiction overlays | Re-graded None to Partial 2026-07-02: the AI compliance policy carries a dedicated UK subsection (7.3, AI Safety Institute and ICO commitments, UK GDPR and DPA 2018) and a framework-table row; the dedicated jurisdiction annex remains the gap |
| US state-by-state (Colorado; NYC bias audit, etc.) | Partial | In library (Colorado) | TODO backlog: AI jurisdiction overlays (other states) | Re-graded to Partial 2026-07-09: Colorado now has a dedicated two-regime jurisdiction annex [`ai/jurisdictions/annex-ai-us-colorado.md`](../ai/jurisdictions/annex-ai-us-colorado.md) (SB 24-205 re-enacted by SB 26-189: developer/deployer duties, consumer rights, meaningful human review, AG-exclusive enforcement, transition timeline); the NYC bias-audit law and other US states are not yet cited in any corpus document and remain the gap |
| China generative AI rules | Partial | Planned | TODO backlog: AI jurisdiction overlays | Re-graded None to Partial 2026-07-03 (the #586 sweep's M-2): the China privacy annex carries a described-obligations bullet for the Interim Measures for the Management of Generative AI Services plus dedicated Generative-AI obligations and enforcement subsections (the UK-AI-framework adjacent-dedicated-subsection pattern), and the jurisdiction index carries Generative-AI cells in its file, regime, and developments tables; unlike the Colorado basis there is no canonical-citations row, and the EU AI Act row's Referenced-on-heavy-citation stands as the disclosed neighbouring tension; the dedicated AI jurisdiction annex remains the gap |
| Korea AI framework | None | Planned | TODO backlog: AI jurisdiction overlays |  |

---

## 3. Regulations and frameworks referenced but not detailed

Regulations and frameworks named in the library but without dedicated operational treatment. Whether they need dedicated treatment depends on adopter demand.

| Instrument | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| ISO 9001 (quality management) | Referenced | Out of scope | n/a | Quality management is outside the library's information-security/GRC scope. Re-graded None to Referenced 2026-07-02 (the ISO 14001 row-shape parallel: a dated re-grade with Status staying Out of scope): the CAPA procedure operationalizes ISO 9001 clauses 10.2 and 10.3 as its primary source, and the library-quality cadence procedure plus further governance documents cite it in framework tables; arguably Partial on the CAPA evidence (the ITIL 4 row's shape), kept at the conservative grade since only two clauses of the QMS are operationalized; dedicated treatment stays out of scope |
| ISO 22301:2019 (business continuity) | Substantive | In library | n/a | Throughout resilience domain |
| ISO 31000:2018 (risk management) | Substantive | In library | n/a | Throughout risk domain |
| ISO 14001 (environmental management) | Referenced | Out of scope | n/a | ESG content references it (e.g. the IT-financial-management standard's sustainability crosswalk); not in scope for dedicated treatment. Re-graded None to Referenced 2026-07-02, resolving the row's own Notes contradiction |
| PCI DSS 4.0.1 | Referenced | Deferred | Backlog candidate: PCI DSS payments annex (not currently scheduled in TODO; the financial-services TODO item covers country regulators only) | Payments-specific; would fit under financial-services or as a sector annex |
| Basel III | Referenced | Deferred | Backlog candidate: Basel III banking annex (not currently scheduled in TODO; the financial-services TODO item covers country regulators only) | Banking-specific; would fit under financial-services |
| IEC 62443 (OT security) | Referenced | Planned | Backlog candidate: IEC 62443 depth annex (not currently scheduled in TODO; the OT suite itself shipped, see section 4) | High-priority for industrial/energy/logistics sectors |
| NERC CIP | Referenced | Planned | TODO backlog: energy and utilities country regulator overlays | High-priority for energy sector |
| SWIFT CSP (Customer Security Programme) | Referenced | Deferred | Backlog candidate: SWIFT CSP annex (not currently scheduled in TODO; the financial-services TODO item covers country regulators only). Re-graded None to Referenced 2026-07-02: the financial-services annex names SWIFT CSP in its regime table and attestation row ([`compliance/financial-services/annex-financial-services-sector-requirements.md`](../compliance/financial-services/annex-financial-services-sector-requirements.md)) | Financial-services payment networks |
| SOC 2 (Trust Services Criteria) | Referenced | Deferred | Backlog candidate: SOC 2 TSC-to-document mapping (not currently scheduled in TODO) | Named as a target attestation corpus-wide (the audit-evidence and regulator-interaction templates, the glossary, the maturity self-assessment) but no matrix maps the Trust Services Criteria (the CC-series common criteria plus the Availability, Confidentiality, Processing Integrity, and Privacy categories) to library documents; disclosure row added per deep-assessment r1 |
| ITIL 4 | Partial | Out of scope | n/a | Service management framework; operational rather than governance. Re-graded None to Partial 2026-07-02: [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md) consolidates the ITIL-based ITSM processes (SMO oversight, process ownership); dedicated ITIL-instrument treatment stays out of scope |
| TOGAF | Referenced | Out of scope | n/a | Architecture framework; operational. Re-graded None to Referenced 2026-07-02: framework-table rows in six shipped architecture documents (the enterprise-architecture framework, the reference-architecture standard, the architecture-review procedure, and three further standards); dedicated TOGAF treatment stays out of scope |
| COBIT 2019 | Substantive | In library | n/a | Cited throughout governance and compliance |

---

## 4. Cloud and platform providers

The library is cloud-provider-agnostic. Provider-specific guidance is recorded as a known gap.

| Provider / platform | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Provider-agnostic cloud guidance | Substantive | In library | n/a | Throughout operations and supply-chain |
| AWS-specific overlays | Partial | Deferred | Backlog candidate: per-cloud governance overlays (not currently scheduled in TODO; the multi-cloud TODO item covers only cross-cloud governance) | Re-graded None to Partial 2026-07-02: the AWS hardening baseline shipped as [`dev-security/standard-cloud-hardening-baseline-aws.md`](../dev-security/standard-cloud-hardening-baseline-aws.md), a dedicated per-cloud technical standard; the governance overlay itself remains the gap |
| Azure-specific overlays | Partial | Deferred | Backlog candidate: per-cloud governance overlays (not currently scheduled in TODO; the multi-cloud TODO item covers only cross-cloud governance) | Re-graded None to Partial 2026-07-02: the Azure hardening baseline shipped as [`dev-security/standard-cloud-hardening-baseline-azure.md`](../dev-security/standard-cloud-hardening-baseline-azure.md), a dedicated per-cloud technical standard; the governance overlay itself remains the gap |
| GCP-specific overlays | Partial | Deferred | Backlog candidate: per-cloud governance overlays (not currently scheduled in TODO; the multi-cloud TODO item covers only cross-cloud governance) | Re-graded None to Partial 2026-07-02: the GCP hardening baseline shipped as [`dev-security/standard-cloud-hardening-baseline-gcp.md`](../dev-security/standard-cloud-hardening-baseline-gcp.md), a dedicated per-cloud technical standard; the governance overlay itself remains the gap |
| Multi-cloud governance patterns | None | Deferred | TODO backlog: multi-cloud governance overlay |  |
| Kubernetes-specific governance | Partial | Deferred | Backlog candidate: Kubernetes-specific governance (not currently scheduled in TODO) | Could live in operations or dev-security. Re-graded None to Partial 2026-07-02 (initially Referenced; raised at the verifier's vocabulary check): [`dev-security/standard-container-and-image-security.md`](../dev-security/standard-container-and-image-security.md) carries Kubernetes-specific operational controls (the pod-security-standards baseline, host-namespace prohibitions, a full orchestrator-security section) and its framework table cites CIS benchmarks and the Kubernetes Pod Security Standards; dedicated Kubernetes governance remains the gap |
| Serverless / FaaS-specific governance | Partial | Deferred | Backlog candidate: serverless-specific governance (not currently scheduled in TODO) | Re-graded None to Partial 2026-07-02: [`dev-security/standard-container-and-image-security.md`](../dev-security/standard-container-and-image-security.md) carries a dedicated serverless-container-platforms section, and all three per-cloud hardening baselines carry serverless compute/platform control rows; dedicated FaaS governance remains the gap |
| SaaS-specific SPM (Security Posture Management) | None | Deferred | n/a | Adjacent to supply-chain domain |

---

## 5. Technical capability areas

| Area | Coverage | Status | Planned target | Notes |
| --- | --- | --- | --- | --- |
| Operational Technology (OT) security | Substantive | In library | n/a | [`operations/ot/`](../operations/ot/): overview annex (Phase 22.1), OT/ICS Security Standard (22.2), OT Incident Response Procedure (22.3), OT Change Management Procedure (22.4), OT Asset Inventory and Lifecycle Register (22.5), BMS Overlay Annex (22.6). IEC 62443 family and NIST SP 800-82 Rev. 3 catalogued in canonical citations. |
| Identity governance (workforce IAM) | Substantive | In library | n/a | Throughout security domain |
| Customer Identity (CIAM) | Referenced | Deferred | TODO backlog: identity-specific content depth | Adopter UX and consumer-data dimensions |
| Federated identity (SAML, OIDC) | Partial | In library | n/a | Referenced in IAM standards; dedicated patterns deferred |
| Quantum cryptography readiness | Substantive | In library | n/a | PQC roadmap exists; deepening is queued in the TODO backlog (quantum cryptography readiness deepening) |
| Post-quantum crypto migration playbook | Partial | Deferred | TODO backlog: quantum cryptography readiness deepening | Re-graded None to Partial 2026-07-03 (the #586 sweep's L-3): the shipped PQC roadmap carries a migration-scope table (per-function PQC targets and priorities) and a six-phase migration roadmap (per-phase deliverables through phase 5) (the Manufacturing adjacent-dedicated pattern; the sibling readiness row grades the same roadmap Substantive); the dedicated runbook-level migration playbook remains the gap |
| Crypto-agility patterns | None | Deferred | TODO backlog: quantum cryptography readiness deepening |  |
| AI/ML governance | Substantive | In library | n/a | Throughout AI domain |
| AI red-team methodology depth | Substantive | In library | n/a | Adversarial test reference, red team report template, agentic security standard with 16 threat classes, classical ML adversarial taxonomy, AI-driven offensive tool governance (§33 of agentic standard) all expanded across Phase 23 sub-phases |
| AI-driven offensive security tool governance | Substantive | In library | n/a | [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) §33 (OFFAI-SEC-01 to 10); tooling landscape register references PentestGPT, PentAGI, Strix, HexStrike AI, BurpGPT |
| ML model file scanning (pickle, H5, Keras, SavedModel) | Substantive | In library | n/a | SUPPLY-SEC-07 control in agentic standard; references modelscan, picklescan, fickling patterns |
| Multimodal AI threats (image, audio, video, OCR, PDF, QR) | Substantive | In library | n/a | RUNTIME-SEC-07 / 08 in agentic standard; TC-13 multimodal injection threat class |
| Agent goal stability and inter-agent communication compromise | Substantive | In library | n/a | AGENT-SEC-15 / 16; TC-14 / TC-15 threat classes |
| Classical ML adversarial taxonomy (evasion, poisoning, extraction, inference) | Substantive | In library | n/a | [`standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md) §3.5 restructured into 6 subsections covering ART/AIJack/HEART-equivalent threats |
| Citation verification methodology and freshness governance | Substantive | In library | n/a | [`specification-citation-verification.md`](specification-citation-verification.md); [`register-canonical-citations.md`](register-canonical-citations.md); [`lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py); [`lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py) |
| AI security tooling landscape (curated index) | Substantive | In library | n/a | [`register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md) with 55 entries across 9 categories, per-entry Provenance blocks |
| Audit programme (automated linting and conformance) | Substantive | In library | n/a | Audit programme running in CI on every PR (see [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6 for the canonical gate inventory and current gate count); coverage spans metadata integrity, language and style, reference integrity, content-drift defence, programme and index integrity, security and privacy, and freshness and lifecycle (see specification §5 for the functional categorization and §6 for the per-gate detail) |
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
| Adopter quickstart templates per profile | Partial | Planned | Backlog candidate: per-profile quickstarts (not currently scheduled in TODO). Re-graded None to Partial 2026-07-02: the general quickstart and the startup roadmap shipped in docs/ and serve the capability generically; the per-profile variants remain the gap |
| Interactive maturity assessment | Partial | Planned | Backlog candidate: interactive maturity assessment (not currently scheduled in TODO). Re-graded None to Partial 2026-07-02: the maturity self-assessment template ([`docs/template-maturity-self-assessment.md`](../docs/template-maturity-self-assessment.md)) and the static scorecard serve the assessment capability; interactivity itself remains the gap |
| Implementation roadmap templates | Partial | Planned | Backlog candidate: further roadmap templates (not currently scheduled in TODO). Re-graded None to Partial 2026-07-02: the implementation roadmap and the startup roadmap shipped in docs/; further profile- or sector-specific templates remain the gap |
| Decision-tree adopter navigator | Substantive | In library | [`docs/decision-tree.md`](../docs/decision-tree.md) |
| Worked examples / case studies | None | Out of scope | The library is organization-neutral; case studies would conflict with that posture |
| Regulator interaction templates (notification, attestation, response) | Substantive | In library | [`compliance/template-regulator-interaction.md`](../compliance/template-regulator-interaction.md) |
| Audit evidence package templates | Substantive | In library | [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md) |

---

## How this register is used

For adopters:

1. Search for the sector, jurisdiction, or regulation relevant to your organization.
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
