# New Zealand Privacy Regulatory Requirements

**Document Title:** New Zealand Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.1\
**Date:** 2026-09-11\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-new-zealand.md`](annex-privacy-new-zealand.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in New Zealand under the Privacy Act 2020. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Privacy Act 2020**: In force 2020-12-01, replacing the Privacy Act 1993. Administered by the Office of the Privacy Commissioner (OPC).
- 13 Information Privacy Principles (IPPs) govern collection, use, disclosure, storage, and security of personal information.
- **Mandatory breach notification:** Agencies must notify the OPC and affected individuals of privacy breaches likely to cause serious harm as soon as practicable after becoming aware.
- **Extraterritorial reach:** Applies to any agency carrying on business in New Zealand, regardless of where they are based.
- **EU adequacy:** the EU has recognized New Zealand as providing an adequate level of protection, facilitating data flows from the EU into New Zealand (an inbound recognition under EU law, not a provision of the Privacy Act).

---

## Thirteen information privacy principles (IPPs)

New Zealand's Privacy Act 2020 (s. 22) sets thirteen information privacy principles governing an agency's handling of personal information. Each is mapped to the library control that carries it, or flagged as a New Zealand-specific gap.

| IPP (Privacy Act 2020, s. 22) | Library disposition |
| --- | --- |
| **IPP 1 - Purpose of collection**: personal information is collected only for a lawful purpose connected with a function or activity of the agency, and only where necessary for that purpose. | library purpose-limitation and data-minimization controls |
| **IPP 2 - Source of information**: personal information is collected directly from the individual concerned, subject to the enumerated exceptions. | library collection controls |
| **IPP 3 / 3A - Collection notice**: when collecting from the individual, the agency takes reasonable steps to make the individual aware of the collection, its purpose, recipients, and rights (IPP 3); IPP 3A extends notice obligations to information collected indirectly. | library privacy-notice controls (`privacy/template-privacy-notice.md`) |
| **IPP 4 - Manner of collection**: personal information is collected by lawful and fair means that are not unreasonably intrusive. | library collection controls |
| **IPP 5 - Storage and security**: the agency maintains reasonable security safeguards against loss, unauthorized access, use, modification, or disclosure. | library information-security controls (`security/`) |
| **IPP 6 - Access**: an individual is entitled to confirmation of and access to their personal information held by the agency. | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`) |
| **IPP 7 - Correction**: an individual may request correction of their personal information, and the agency attaches a statement of correction sought if it declines. | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`) |
| **IPP 8 - Accuracy before use**: the agency checks that personal information is accurate, up to date, complete, relevant, and not misleading before using or disclosing it. | library data-quality controls |
| **IPP 9 - Retention**: the agency does not keep personal information for longer than is required for the purposes for which it may lawfully be used. | library data-retention controls |
| **IPP 10 - Limits on use**: personal information obtained for one purpose is not used for another, subject to the enumerated exceptions. | library purpose-limitation controls |
| **IPP 11 - Limits on disclosure**: personal information is not disclosed except in accordance with the enumerated disclosure grounds. | library disclosure and third-party-sharing controls |
| **IPP 12 - Disclosure outside New Zealand**: an agency may disclose personal information to a foreign person or entity only in reliance on the specified IPP 11 grounds and where the IPP 12 conditions are met; the mechanics are set out in the cross-border transfer section below. | library cross-border-transfer controls |
| **IPP 13 - Unique identifiers**: an agency does not assign a unique identifier unless necessary for its functions, does not adopt another agency's identifier, and takes steps to minimize misuse. | library identifier-handling controls |

## AI and privacy obligations

- **IPP 1 (purpose of collection), IPP 6 (access), and IPP 10 (limits on use)** apply to personal information used in AI systems.
- The OPC has published guidance on responsible use of AI and application of IPPs to AI-assisted decision-making.
- **Automated decisions:** the Privacy Act 2020 contains no automated decision-making provision; an adopter applying the library's automated-decision controls does so as governance practice, not as a Privacy Act requirement.

---

## Cross-border transfer mechanisms

- **IPP 12** governs the disclosure of personal information to a foreign person or entity where the agency is relying on the IPP 11(1)(a), (c), (e), (f), (h), or (i) disclosure grounds (transfer to an agent for storage or processing is not a disclosure under s. 11(5)). In that case the disclosure is permitted only if: the individual authorizes it after being expressly informed the recipient may not provide comparable safeguards; or the recipient carries on business in New Zealand and the agency believes on reasonable grounds that, in relation to the information, the recipient is subject to the Act; or the agency believes on reasonable grounds that the recipient is subject to privacy laws with comparable safeguards, is a participant in a prescribed binding scheme, is subject to the privacy laws of a prescribed country and no prescribed limitation or qualification precludes the disclosure, or is otherwise required to provide comparable safeguards (IPP 12(1)(a)-(f)). These conditions do not apply to a disclosure relying on IPP 11(1)(e) or (f) where complying with them is not reasonably practicable (IPP 12(2)).
- The EU's adequacy recognition of New Zealand governs transfers from the EU into New Zealand under EU law; it is not an IPP 12 outbound-disclosure route. A country or a binding scheme is an IPP 12 route only when prescribed by New Zealand regulations (ss. 213-214).

---

## Enforcement and fines

- Criminal fines up to NZD 10,000 on conviction for the enumerated offences (s. 212), distinct from Human Rights Review Tribunal damages and the Commissioner's compliance-notice remedies.
- The Human Rights Review Tribunal may award damages for proven privacy interferences.
- The OPC may conduct investigations, issue compliance notices, and refer matters to the Director of Human Rights Proceedings.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
