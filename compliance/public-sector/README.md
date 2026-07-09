# Public Sector Compliance

**Document Title:** Public Sector Compliance README\
**Document Type:** Register\
**Version:** 1.0.2\
**Date:** 2026-07-09\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md), [`compliance/public-sector/annex-fedramp-requirements.md`](annex-fedramp-requirements.md), [`compliance/public-sector/annex-eidas-requirements.md`](annex-eidas-requirements.md), [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Compliance: Public Sector\
**Review Frequency:** Annual and upon material change to a covered regulation\
**Repository Path:** [`compliance/public-sector/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This directory contains public-sector compliance content of the library: sector-wide regulatory requirements that apply to government agencies, public bodies, and private organizations serving the public sector (for example, cloud-service providers to federal agencies under FedRAMP).

Content here is sector-conditional. Organizations outside the public sector and not providing services to the public sector can omit this directory entirely without affecting the rest of the library's coherence.

---

## Applicability

This directory applies to organizations operating as any of the following:

- Government agencies and public bodies at any level (federal, national, regional, local).
- State-owned enterprises and public-sector corporations.
- Cloud-service providers offering services to government agencies (FedRAMP authorization, equivalent authorizations).
- Service providers and contractors to government agencies in scope of public-sector procurement and cyber-hygiene requirements.

---

## Documents in this directory

| Document | Type | Description |
| --- | --- | --- |
| [`annex-public-sector-requirements.md`](annex-public-sector-requirements.md) | Annex | Public-sector regulatory landscape across jurisdictions: procurement requirements, records management, freedom-of-information obligations, accessibility, and public-sector-specific cyber-hygiene frameworks. |
| [`annex-fedramp-requirements.md`](annex-fedramp-requirements.md) | Annex | US Federal Risk and Authorization Management Program (FedRAMP) requirements for cloud-service providers to US federal agencies. |
| [`annex-eidas-requirements.md`](annex-eidas-requirements.md) | Annex | EU eIDAS (Regulation 910/2014 as amended by Regulation 2024/1183, the European Digital Identity Framework) requirements by role: wallet-relying party, trust-service provider, public-sector body, and wallet provider. |

---

## Future-coverage placeholders

Country-level public-sector overlays. EU eIDAS now has a dedicated annex ([`annex-eidas-requirements.md`](annex-eidas-requirements.md)). Candidates for future addition include UK Government Cyber Security Strategy and GovAssure, Canada IT Standards for federal departments, Australia ISM (Information Security Manual) and PSPF (Protective Security Policy Framework), and other jurisdiction-specific frameworks as adopting organizations require.

---

## Relationship to the main library

The main library is sector-agnostic and applies to all adopting organizations. This directory's content extends but does not contradict the main library. Where a public-sector regulation requires specific control language, evidence formats, or operating cadences, the relevant annex states those requirements explicitly. Where the regulation's controls coincide with main-library controls, the main-library control remains the implementation; the annex documents how the implementation maps to the regulation's expectations.

Adopting organizations operating in the public sector or providing services to it consume:

1. The main library as the baseline.
2. The public-sector overview annex ([`annex-public-sector-requirements.md`](annex-public-sector-requirements.md)) for sector-wide requirements.
3. The regulation-specific annexes for the regulations the organization is in scope for (for example, FedRAMP for US federal cloud providers).

---

## Licence boundary

All content is original and released under CC BY-SA 4.0. Annexes reference regulations and standards by name and section identifier; the underlying regulation text itself is not reproduced.

---

**End of Document**
