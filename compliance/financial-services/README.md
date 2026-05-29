# Financial Services Sector Compliance

**Document Title:** Financial Services Sector Compliance README\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-28\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/financial-services/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md), [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Compliance: Financial Services Sector\
**Review Frequency:** Annual and upon material change to a covered regulation\
**Repository Path:** [`compliance/financial-services/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This directory contains financial-services-sector compliance content of the library: sector-wide regulatory requirements and jurisdiction-specific regulation overlays that apply to organisations operating as regulated financial-services entities, financial-market infrastructures, or service providers to regulated financial-services entities.

Content here is sector-conditional. Organisations outside the financial-services sector can omit this directory entirely without affecting the rest of the library's coherence.

---

## Applicability

This directory applies to organisations operating as any of the following:

- Banks, building societies, credit unions, and other deposit-taking institutions.
- Investment firms, broker-dealers, asset managers, fund administrators, and custodians.
- Insurance and reinsurance undertakings, and their intermediaries.
- Payment institutions, e-money issuers, and payment-system operators.
- Stock exchanges, clearing houses, central securities depositories, and other financial-market infrastructures.
- ICT third-party service providers to regulated financial-services entities (in scope for DORA and equivalent frameworks).

---

## Documents in this directory

| Document | Type | Description |
| --- | --- | --- |
| [`annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md) | Annex | Financial-services sector regulatory landscape, prudential and conduct regulator obligations, and cross-jurisdiction requirements. |
| [`annex-dora-implementation.md`](annex-dora-implementation.md) | Annex | EU Digital Operational Resilience Act (DORA) implementation overlay. |
| [`annex-sox-itgc.md`](annex-sox-itgc.md) | Annex | US Sarbanes-Oxley (SOX) IT general controls overlay for publicly-traded entities. |

---

## Future-coverage placeholders

Country-level financial-regulator overlays for jurisdictions where the organisation operates. Candidates for future addition include UK PRA/FCA, EU EBA/ESMA/EIOPA per-jurisdiction implementations, US OCC/FRB/FDIC/SEC/FINRA, Canada OSFI, Australia APRA, Singapore MAS, Japan FSA, and others as adopting organisations require.

---

## Relationship to the main library

The main library is sector-agnostic and applies to all adopting organisations. This directory's content extends but does not contradict the main library. Where a financial-services regulation requires specific control language, evidence formats, or operating cadences, the relevant annex states those requirements explicitly. Where the regulation's controls coincide with main-library controls (access management, logging, incident response), the main-library control remains the implementation; the annex documents how the implementation maps to the regulation's expectations.

Adopting organisations operating as regulated financial-services entities consume:

1. The main library as the baseline.
2. The financial-services sector overview annex ([`annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md)) for sector-wide requirements.
3. The regulation-specific annexes for the regulations the organisation is in scope for.

---

## Licence boundary

All content is original and released under CC0 1.0 Universal. Annexes reference regulations and standards by name and section identifier; the underlying regulation text itself is not reproduced.

---

**End of Document**
