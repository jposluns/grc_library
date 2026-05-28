# Sector Annexes

**Document Title:** Sector Annexes Domain README 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-28 
**Owner:** Governance Library Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`README.md`](../README.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`compliance/README.md`](../compliance/README.md) 
**Classification:** Public 
**Category:** Sector Annex 
**Review Frequency:** Annual and upon material change to a sector-specific programme covered here 
**Repository Path:** [`sectors/README.md`](README.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This directory contains sector-conditional governance content: artefacts that apply only to organisations participating in a specific sectoral, geographic, or programmatic regime. Sector annexes are optional; organisations that do not participate in a covered programme can omit the corresponding annex entirely without affecting the rest of the library's coherence.

Sector annexes are organized by the programme they implement. Each programme has its own sub-directory with a local README and the annex documents that implement that programme.

---

## Active sector annexes

| Sector / programme | Path | Applicability |
| --- | --- | --- |
| BASC (Business Alliance for Secure Commerce) | [`sectors/basc/`](basc/) | Organisations pursuing or maintaining BASC International Standard certification (typically Latin American trade and logistics operators). |

## Active documents

| Type | Title | Path |
| --- | --- | --- |
| Policy | BASC Information Security Policy | [`sectors/basc/policy-basc-information-security.md`](basc/policy-basc-information-security.md) |
| Register | BASC IT and Information Security Responsibilities | [`sectors/basc/register-basc-it-responsibilities.md`](basc/register-basc-it-responsibilities.md) |
| Register | BASC IT Compliance Monitoring and KPIs | [`sectors/basc/register-basc-it-compliance-kpis.md`](basc/register-basc-it-compliance-kpis.md) |

---

## Relationship to the main library

The main library is organisation-neutral and sector-agnostic. Where sector-specific content was historically embedded in core domain documents (security, risk, governance, compliance), it has been extracted to this directory and the core documents have been generalized.

Adopting organisations:

1. Adopt the main library as the baseline.
2. Adopt the sector annexes relevant to their operating context.
3. Annex content extends but does not contradict the main library.

Where a sector annex restates a control because the sector's regulator requires it in specific terms, the annex is the authoritative version for that sector; the main-library control remains in effect for the organisation's other operations.

---

## Licence and neutrality posture

All sector annexes are released under CC0 1.0 Universal alongside the rest of the library. Sector-specific content remains organisation-neutral: it describes how a sector programme is implemented in general terms rather than how any specific organisation has implemented it.

---

## Adding a new sector annex

New sector annexes are added when the library has substantive content for a sector programme that is not appropriate to embed in the main domains. The decision to add a sector annex follows the same governance as adding a new domain.

Each new sector annex must include:

1. A sub-directory under `sectors/` named for the programme.
2. A README in that sub-directory describing the programme, its applicability, and the documents it contains.
3. Updates to the governance index.
4. Updates to this README.

---

**End of Document**
