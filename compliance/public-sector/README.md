# Public Sector Compliance

**Document Title:** Public Sector Compliance README\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-28\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md), [`compliance/public-sector/annex-fedramp-requirements.md`](annex-fedramp-requirements.md), [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Compliance: Public Sector\
**Review Frequency:** Annual and upon material change to a covered regulation\
**Repository Path:** [`compliance/public-sector/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This directory contains public-sector compliance content of the library: sector-wide regulatory requirements that apply to government agencies, public bodies, and private organisations serving the public sector (for example, cloud-service providers to federal agencies under FedRAMP).

Content here is sector-conditional. Organisations outside the public sector and not providing services to the public sector can omit this directory entirely without affecting the rest of the library's coherence.

---

## Applicability

This directory applies to organisations operating as any of the following:

- Government agencies and public bodies at any level (federal, national, regional, local).
- State-owned enterprises and public-sector corporations.
- Cloud-service providers offering services to government agencies (FedRAMP authorisation, equivalent authorisations).
- Service providers and contractors to government agencies in scope of public-sector procurement and cyber-hygiene requirements.

---

## Documents in this directory

| Document | Type | Description |
| --- | --- | --- |
| [`annex-public-sector-requirements.md`](annex-public-sector-requirements.md) | Annex | Public-sector regulatory landscape across jurisdictions: procurement requirements, records management, freedom-of-information obligations, accessibility, and public-sector-specific cyber-hygiene frameworks. |
| [`annex-fedramp-requirements.md`](annex-fedramp-requirements.md) | Annex | US Federal Risk and Authorization Management Program (FedRAMP) requirements for cloud-service providers to US federal agencies. |

---

## Future-coverage placeholders

Country-level public-sector overlays. Candidates for future addition include UK Government Cyber Security Strategy and GovAssure, EU eIDAS public-sector authentication, Canada IT Standards for federal departments, Australia ISM (Information Security Manual) and PSPF (Protective Security Policy Framework), and other jurisdiction-specific frameworks as adopting organisations require.

---

## Relationship to the main library

The main library is sector-agnostic and applies to all adopting organisations. This directory's content extends but does not contradict the main library. Where a public-sector regulation requires specific control language, evidence formats, or operating cadences, the relevant annex states those requirements explicitly. Where the regulation's controls coincide with main-library controls, the main-library control remains the implementation; the annex documents how the implementation maps to the regulation's expectations.

Adopting organisations operating in the public sector or providing services to it consume:

1. The main library as the baseline.
2. The public-sector overview annex ([`annex-public-sector-requirements.md`](annex-public-sector-requirements.md)) for sector-wide requirements.
3. The regulation-specific annexes for the regulations the organisation is in scope for (for example, FedRAMP for US federal cloud providers).

---

## Licence boundary

All content is original and released under CC0 1.0 Universal. Annexes reference regulations and standards by name and section identifier; the underlying regulation text itself is not reproduced.

---

**End of Document**
