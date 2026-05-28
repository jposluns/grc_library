# Compliance Domain

**Document Title:** Compliance Domain README 
**Document Type:** Register 
**Version:** 1.3.0 
**Date:** 2026-05-28 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`README.md`](../README.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/logistics/README.md`](logistics/README.md) 
**Classification:** Public 
**Category:** Compliance Management 
**Review Frequency:** Annual and upon material regulatory or framework change 
**Repository Path:** [`compliance/README.md`](README.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This directory contains compliance management policies, registers, audit governance artefacts, cross-sector regulation annexes, and industry-sector compliance sub-directories. All content is released under CC0 1.0 Universal.

---

## Structure

The compliance domain has two layers:

1. **Root-level core compliance content**: policies, procedures, registers, and templates that apply across all sectors and organisations.
2. **Sector sub-directories**: sector-conditional content for organisations operating in a specific industry (logistics, financial services, healthcare, etc.). Most organisations adopt only the sub-directories matching their sector.

Cross-sector horizontal regulations that span multiple industries (for example, EU NIS 2) stay at the root.

---

## Core compliance documents (root)

| Type | Title | Path |
| --- | --- | --- |
| Policy | Compliance, Audit, and CAPA Management Policy | [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md) |
| Policy | Legal and Regulatory Compliance Policy | [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md) |
| Register | Global Regulatory Applicability Register | [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md) |
| Register | Compliance Obligations Register Template | [`compliance/register-compliance-obligations-template.md`](register-compliance-obligations-template.md) |
| Matrix | GRC Library Compliance Alignment | [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md) |
| Standard | Internal Audit Standard | [`compliance/standard-internal-audit.md`](standard-internal-audit.md) |
| Procedure | Audit Planning Procedure | [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md) |
| Procedure | Corrective and Preventive Action (CAPA) Procedure | [`compliance/procedure-capa.md`](procedure-capa.md) |
| Procedure | Control Testing Procedure | [`compliance/procedure-control-testing.md`](procedure-control-testing.md) |
| Annex | NIS 2 Implementation Annex (cross-sector EU) | [`compliance/annex-nis-2-implementation.md`](annex-nis-2-implementation.md) |

Pending sub-directory placement (currently at root, will move into sector sub-directories in Phase 20.2):

| Type | Title | Current Path |
| --- | --- | --- |
| Annex | Financial Services Sector GRC Requirements Annex | [`compliance/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md) |
| Annex | DORA Implementation Annex (EU financial-services) | [`compliance/annex-dora-implementation.md`](annex-dora-implementation.md) |
| Annex | SOX IT General Controls Annex (financial-services) | [`compliance/annex-sox-itgc.md`](annex-sox-itgc.md) |
| Annex | Healthcare Sector GRC Requirements Annex | [`compliance/annex-healthcare-sector-requirements.md`](annex-healthcare-sector-requirements.md) |
| Annex | Energy and Utilities Sector Requirements Annex | [`compliance/annex-energy-and-utilities-sector-requirements.md`](annex-energy-and-utilities-sector-requirements.md) |
| Annex | Telecommunications Sector Requirements Annex | [`compliance/annex-telecommunications-sector-requirements.md`](annex-telecommunications-sector-requirements.md) |
| Annex | Public Sector GRC Requirements Annex | [`compliance/annex-public-sector-requirements.md`](annex-public-sector-requirements.md) |
| Annex | FedRAMP Requirements Annex (US public-sector) | [`compliance/annex-fedramp-requirements.md`](annex-fedramp-requirements.md) |

---

## Sector sub-directories

| Sector | Path | Coverage |
| --- | --- | --- |
| Logistics | [`compliance/logistics/`](logistics/) | Transportation, warehousing, freight forwarding, customs brokerage; trusted-trader programmes (BASC, CTPAT, PIP, UK AEO). |

Future sector sub-directories (planned in Phase 20.2): `financial-services/`, `healthcare/`, `energy-and-utilities/`, `telecommunications/`, `public-sector/`.

### Logistics sub-directory artefacts

| Type | Title | Path |
| --- | --- | --- |
| Annex | Logistics Sector GRC Requirements Annex | [`compliance/logistics/annex-logistics-sector-requirements.md`](logistics/annex-logistics-sector-requirements.md) |
| Annex | BASC Programme Overview Annex | [`compliance/logistics/annex-basc-programme-overview.md`](logistics/annex-basc-programme-overview.md) |
| Policy | BASC Information Security Policy | [`compliance/logistics/policy-basc-information-security.md`](logistics/policy-basc-information-security.md) |
| Register | BASC IT and Information Security Responsibilities | [`compliance/logistics/register-basc-it-responsibilities.md`](logistics/register-basc-it-responsibilities.md) |
| Register | BASC IT Compliance Monitoring and KPIs | [`compliance/logistics/register-basc-it-compliance-kpis.md`](logistics/register-basc-it-compliance-kpis.md) |
| Annex | UK AEO-S IT and Cybersecurity Requirements | [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](logistics/annex-aeo-united-kingdom-cybersecurity.md) |
| Procedure | UK AEO IT Self-Assessment Procedure | [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](logistics/procedure-aeo-united-kingdom-self-assessment.md) |
| Register | US CTPAT IT and Cybersecurity Compliance Controls Register | [`compliance/logistics/register-ctpat-united-states-it-controls.md`](logistics/register-ctpat-united-states-it-controls.md) |
| Register | US CTPAT Full Minimum Security Criteria Controls Register | [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](logistics/register-ctpat-united-states-msc-controls.md) |
| Register | Canada PIP IT and Cybersecurity Compliance Controls Register | [`compliance/logistics/register-pip-canada-controls.md`](logistics/register-pip-canada-controls.md) |
| Template | Trade Compliance Programme Gap Assessment Template | [`compliance/logistics/template-trade-compliance-gap-assessment.md`](logistics/template-trade-compliance-gap-assessment.md) |

---

## Domain coverage

The compliance domain covers:

- **Compliance management systems**: obligations registers, legal and regulatory tracking, compliance risk assessment, and performance reporting.
- **Internal audit governance**: audit planning, audit execution criteria, independence requirements, finding classification, corrective and preventive action (CAPA) lifecycle.
- **Cross-sector horizontal regulations**: regulations that span multiple sectors (for example, EU NIS 2 Directive).
- **Industry-sector compliance**: sector-conditional sub-directories (currently `logistics/`) hosting sector overviews and programme-specific overlays (CTPAT, BASC, PIP, AEO, and others) for organisations operating in those sectors.
- **AI and algorithmic compliance auditing**: audit trails, transparency, bias assessment, and regulatory alignment for AI systems.
- **Regulatory applicability analysis**: structured approach to determining which legal regimes apply across jurisdictions, data categories, and processing roles.

---

**End of Document**
