# Logistics Sector Compliance

**Document Title:** Logistics Sector Compliance README 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-28 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md), [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md) 
**Classification:** Public 
**Category:** Compliance: Logistics Sector 
**Review Frequency:** Annual and upon material change to any covered programme or addition of a new programme 
**Repository Path:** [`compliance/logistics/README.md`](README.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This directory contains the logistics-sector compliance content of the library: sector-wide requirements that apply to organisations operating in transportation, warehousing, freight forwarding, customs brokerage, and supply-chain logistics, plus the trusted-trader programme overlays that such organisations may participate in.

Content here is sector-conditional. Organisations outside the logistics sector can omit this directory entirely without affecting the rest of the library's coherence.

---

## Applicability

This directory applies to organisations operating in any of the following capacities:

- Freight forwarders, customs brokers, third-party logistics providers (3PL), fourth-party logistics providers (4PL).
- Road, rail, air, or maritime transportation services.
- Warehousing, distribution centres, cross-docking operations.
- Port, airport, or intermodal terminal infrastructure.
- Technology platforms for transportation management, track-and-trace, or customs processing.
- Participants in trusted-trader programmes covered below.

---

## Sector overview

| Document | Description |
| --- | --- |
| [`annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md) | Logistics sector regulatory landscape, transport authority obligations, and cross-programme requirements. Read this first. |
| [`template-trade-compliance-gap-assessment.md`](template-trade-compliance-gap-assessment.md) | Generic trade-compliance gap assessment template usable across any trusted-trader programme. |

---

## Trusted-trader programmes covered

Each programme below has its own artefacts in this directory. Organisations adopt the programmes relevant to the jurisdictions in which they operate.

### BASC (Business Alliance for Secure Commerce)

Multi-country private trade-security programme, predominantly Latin American, recognized within the WCO SAFE Framework.

| Document | Type | Description |
| --- | --- | --- |
| [`annex-basc-programme-overview.md`](annex-basc-programme-overview.md) | Annex | Programme overview, applicability, and relationship to the main library. |
| [`policy-basc-information-security.md`](policy-basc-information-security.md) | Policy | BASC-specific information-security policy. |
| [`register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md) | Register | BASC IT and information-security responsibilities. |
| [`register-basc-it-compliance-kpis.md`](register-basc-it-compliance-kpis.md) | Register | BASC IT compliance monitoring and KPIs. |

### CTPAT (US Customs-Trade Partnership Against Terrorism)

US Customs and Border Protection (CBP) voluntary trusted-trader programme.

| Document | Type | Description |
| --- | --- | --- |
| [`register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md) | Register | CTPAT IT and cybersecurity compliance controls. |
| [`register-ctpat-united-states-msc-controls.md`](register-ctpat-united-states-msc-controls.md) | Register | CTPAT Full Minimum Security Criteria (MSC) controls. |

### PIP (Canada Partners in Protection)

Canada Border Services Agency (CBSA) trusted-trader programme.

| Document | Type | Description |
| --- | --- | --- |
| [`register-pip-canada-controls.md`](register-pip-canada-controls.md) | Register | PIP IT and cybersecurity compliance controls. |

### AEO (United Kingdom Authorised Economic Operator)

HMRC and Border Force trusted-trader programme, AEO-S security and safety strand.

| Document | Type | Description |
| --- | --- | --- |
| [`annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) | Annex | UK AEO-S IT and cybersecurity requirements. |
| [`procedure-aeo-united-kingdom-self-assessment.md`](procedure-aeo-united-kingdom-self-assessment.md) | Procedure | UK AEO IT self-assessment procedure. |

---

## Future-coverage placeholders

The WCO AEO Compendium lists approximately 94 operational or under-development AEO and equivalent trusted-trader programmes globally. The library presently covers four of them (BASC multi-country, CTPAT-US, PIP-Canada, AEO-UK). Future additions follow the same naming convention (`<doctype>-<programme>-<jurisdiction>-<scope>.md`). Candidates for future addition include AEO European Union, NEEC and OEA Mexico, Australian Trusted Trader (ATT), Secure Trade Partnership (STP) Singapore, AEO Japan, AEO Korea, Secure Exports Scheme (SES) New Zealand, and others as adopting organisations require.

---

## Relationship to the main library

The main library is sector-agnostic and applies to all adopting organisations. This directory's content extends but does not contradict the main library. Where a programme requires specific control language, evidence formats, or operating cadences, the programme's artefacts state those requirements explicitly. Where a programme's controls coincide with main-library controls (access management, logging, incident response), the main-library control remains the implementation; the programme artefact documents how the implementation maps to the programme's expectations.

Adopting organisations operating in the logistics sector consume:

1. The main library as the baseline.
2. The logistics sector overview annex ([`annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md)) for sector-wide requirements.
3. The programme-specific artefacts for the programmes the organisation participates in.

---

## Licence boundary

All content is original and released under CC0 1.0 Universal. Programme artefacts reference each programme's standards and criteria by name and section identifier; the underlying programme text itself is not reproduced.

---

**End of Document**
