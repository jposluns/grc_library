# Public Sector GRC Requirements Annex

**Document Title:** Public Sector GRC Requirements Annex 
**Document Type:** Annex 
**Version:** 0.0.2 
**Date:** 2026-05-28 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md) 
**Classification:** Public 
**Category:** Compliance: Sector-Specific 
**Review Frequency:** Annual and upon material public-records law, accessibility, or procurement guidance change 
**Repository Path:** [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This annex identifies the obligations that overlay the core GRC library when an entity is a public sector body or a contractor providing services to one. It covers freedom of information, accessibility, public procurement, records management, audit and transparency, official languages, lobbying and ethics, and the elevated expectations on technology, AI, and data protection that public sector buyers and citizens apply.

This annex is jurisdictionally agnostic; adopting entities map the local statute (national, regional, or municipal) to each overlay area.

---

## Applicability triggers

This annex is relevant where the entity is:

1. A national, regional, or local government body.
2. A public authority or arms-length body funded substantially by public money.
3. A contractor performing services that involve handling government records, citizen data, or public-facing service delivery.
4. A grant recipient subject to public-procurement-style obligations through the grant agreement.
5. A public-private partnership or commissioned operator of public services.

---

## Overlay area 1: freedom of information and transparency

Public sector bodies are typically subject to a freedom-of-information regime that gives citizens a right of access to records held by the public authority, with limited exemptions.

| Obligation | Library support |
| --- | --- |
| Maintain records in a form that supports timely retrieval | `governance/standard-records-retention-and-destruction.md`, `governance/register-data-retention-schedule.md`, `operations/register-asset-inventory.md` |
| Respond to access requests within the statutory window | Library does not provide a FOI workflow; adopting entities use a public-records-request workflow analogous to the DSAR template but adapted to FOI exemptions |
| Apply statutory exemptions consistently | Requires legal-team workflow per jurisdiction |
| Publish defined classes of information proactively | Requires a publication scheme specific to the entity |
| Maintain a disclosure log | Operational record outside library scope |

Common regimes: FOIA (US federal), Freedom of Information Act 2000 (UK), Access to Information Act (Canada), various sub-national equivalents.

---

## Overlay area 2: accessibility

Public sector digital services typically have legal accessibility obligations beyond private-sector norms.

| Obligation | Library support |
| --- | --- |
| Digital services meet defined accessibility standard | Library does not contain an accessibility standard; adopting entities adopt WCAG 2.1 AA or 2.2 AA as the baseline (EN 301 549 in the EU) |
| Accessibility statement published per public-facing service | Adopting entities maintain a per-service statement |
| Annual accessibility review and remediation plan | Library audit and CAPA procedures support the recurring review |

Common regimes: Web Accessibility Directive (EU 2016/2102) with EN 301 549; Americans with Disabilities Act and Section 508 (US); Accessibility for Ontarians with Disabilities Act (Ontario); equivalents elsewhere.

---

## Overlay area 3: public procurement

Public procurement is highly regulated. The library supports supplier governance but the public-procurement layer adds:

| Obligation | Library support |
| --- | --- |
| Procurement above threshold follows the statutory tender process | Outside library scope |
| Tender documents include security, privacy, accessibility, sustainability requirements | `supply-chain/template-supplier-security-questionnaire.md` provides the security baseline; entities extend per procurement policy |
| Supplier conflict-of-interest declarations | Requires per-procurement workflow |
| Modern-slavery and labour-rights statements | Library supports as part of supplier due diligence |
| Subcontracting transparency and prompt-payment obligations | Outside library scope |
| Standstill period and appeals process | Outside library scope |

Common regimes: EU Public Procurement Directives (2014/24/EU, 2014/25/EU, 2014/23/EU); US Federal Acquisition Regulation; UK Procurement Act 2023; equivalents elsewhere.

---

## Overlay area 4: records management

Public sector records are subject to mandatory archival and destruction rules.

| Obligation | Library support |
| --- | --- |
| Records retention schedule approved by the national archives authority | `governance/standard-records-retention-and-destruction.md`, `governance/register-data-retention-schedule.md` provide the structure; entities map to the archive-authority-approved schedule |
| Disposal scheduled with archival authority approval | Library disposal evidence supports this |
| Permanent records transferred to the archive | Outside library scope; per-archive workflow |
| Open data publication where appropriate | Per the entity's open-data strategy |

Common regimes: National Archives (UK), National Archives and Records Administration (US), Library and Archives Canada, equivalents elsewhere.

---

## Overlay area 5: audit and external scrutiny

Public sector bodies face external audit by an auditor-general or equivalent.

| Obligation | Library support |
| --- | --- |
| Internal audit consistent with public-sector standards | `compliance/standard-internal-audit.md`, `compliance/procedure-audit-planning.md` provide the baseline; entities extend per public-sector internal audit standards (e.g. IIA Public Sector Standards) |
| External audit cooperation | Operational, not template-driven |
| Reporting to legislative bodies | Per the entity's governance |
| Performance audits | Per the auditor-general's programme |

---

## Overlay area 6: ethics, lobbying, and conflict of interest

Public sector roles attract ethics rules that exceed private-sector norms.

| Obligation | Library support |
| --- | --- |
| Code of conduct and conflict-of-interest declaration | `governance/framework-human-capital-and-ethical-conduct.md` provides the baseline; entities adopt the specific civil-service or political-office code |
| Lobbying register and meetings disclosure | Outside library scope; per-jurisdiction register |
| Post-employment restrictions | Per the entity's HR and ethics policy |
| Gift and hospitality register | Per the entity's ethics policy |

---

## Overlay area 7: AI in the public sector

AI used in public-sector decision-making attracts heightened expectations.

| Obligation | Library support |
| --- | --- |
| AI impact assessment with public-interest test | `ai/procedure-ai-system-impact-assessment.md`, `privacy/register-automated-decision-making.md` provide the baseline; entities extend with public-interest test specific to their mandate |
| Transparency on use of AI in decisions | `ai/framework-ai-model-documentation-and-transparency.md`, `privacy/template-privacy-notice.md` |
| Human oversight on consequential decisions | `ai/charter-ai-governance-council.md`, `ai/standard-ai-and-agentic-development-security.md` |
| Algorithmic transparency register publication | Outside library scope; per-jurisdiction register (e.g. UK Algorithmic Transparency Recording Standard, French Republic algorithm register) |

---

## Overlay area 8: official languages

Where the jurisdiction has multiple official languages, public sector communications must respect language obligations.

| Obligation | Library support |
| --- | --- |
| Public-facing artefacts produced in all official languages | Outside library scope; per-jurisdiction translation policy |
| Service delivery in the citizen's chosen official language | Per the entity's policy |

---

## Library gaps requiring additional documentation

1. **Freedom-of-information request workflow** with statutory windows, exemption taxonomy, and disclosure log.
2. **Accessibility programme** at WCAG 2.1 AA or 2.2 AA with per-service statements and remediation tracking.
3. **Public procurement procedure** above and below the statutory thresholds applicable to the jurisdiction.
4. **Records management schedule** approved by the national archive authority.
5. **Algorithmic transparency register** where the entity is subject to such a regime.
6. **Open data publication policy and dataset register.**
7. **Lobbying and gift / hospitality registers.**

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| WCAG 2.2 AA | W3C | Digital accessibility |
| EN 301 549 | ETSI | EU public-sector ICT accessibility |
| ISO 15489 | International | Records management |
| ISO 19011:2018 | International | Audit management |
| OECD Recommendation on Public Service Leadership | OECD | Public-sector ethics |
| UN Principles on Effective Governance for Sustainable Development | UN | Public-sector governance |
| OECD Recommendation on Artificial Intelligence | OECD | Public-sector AI |
| ISO/IEC 42001:2023 | International | AI management system |

---

## Limitations

This annex is a public-domain navigation aid. Public-sector compliance requires the entity to map every overlay area to the specific statute, regulation, and ministerial guidance applicable in its jurisdiction. The library does not replace the national archives schedule, the accessibility statement, the procurement code, the freedom-of-information workflow, or the algorithmic transparency register. Adopting entities consult their own legal counsel, internal audit, and the supervising public-sector authority. This annex is not legal advice.

---

**End of Document**
