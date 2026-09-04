# Mexico Privacy Regulatory Requirements

**Document Title:** Mexico Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.3\
**Date:** 2026-09-04\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/jurisdictions/annex-privacy-latin-america.md`](annex-privacy-latin-america.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy or regulatory change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-mexico.md`](annex-privacy-mexico.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines the privacy regulatory requirements applicable to the processing of personal data held by private parties in Mexico under the Federal Law on the Protection of Personal Data Held by Private Parties (Ley Federal de Protección de Datos Personales en Posesión de los Particulares, LFPDPPP). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

IMPORTANT currency note for adopters: Mexico enacted a **new** LFPDPPP, published in the Diario Oficial de la Federación (DOF) on 20 March 2025, which repealed the 2010 law. This annex reflects the 2025 regime. The older 2010-law-and-INAI framing in the [Latin America privacy annex](annex-privacy-latin-america.md) is superseded by this annex for Mexico.

---

## Applicable law and regulatory authority

- **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)**, new law published in the DOF on 20 March 2025 (TEXTO VIGENTE, last reform published DOF 14 November 2025), governing the processing of personal data by private parties (personas físicas y morales de carácter privado).
- **Regulatory authority: the Secretaría Anticorrupción y Buen Gobierno.** The 2025 regime assigns the data-protection authority function to the Secretaría, replacing the former Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales (INAI), which was extinguished as part of the constitutional and legislative reform; the Secretaría receives the transferred matters and files. Adopters that previously mapped obligations to INAI reassign them to the Secretaría.
- Public-sector processing is governed by a separate general law and is out of scope for this annex, which addresses private-party processing under the LFPDPPP.

The controlling text is the LFPDPPP itself; where this annex states an obligation, the article reference points to the enacted text, and an adopter confirms the current in-force version (the last reform date and the authority designation) against the primary source before relying on a specific value.

---

## Principles, lawful basis, and privacy notice

- **Principles** (Article 5): the processing of personal data is subject to the principles of licitud (lawfulness), consentimiento (consent), información (information), calidad (quality), finalidad (purpose), lealtad (loyalty), proporcionalidad (proportionality), and responsabilidad (accountability).
- **Consent** (Articles 7 to 9): processing requires the data subject's consent unless an exception applies; consent may be tacit or express depending on the data category, and processing of sensitive personal data requires the data subject's express written consent.
- **Privacy notice (aviso de privacidad)** (Articles 14 to 16): the responsable (controller) must make a privacy notice available to the data subject stating the identity of the controller, the purposes of processing, the options to limit use or disclosure, the means to exercise data-subject rights, and any transfers.

---

## Data-subject rights (ARCO)

The LFPDPPP grants the data subject the ARCO rights (Articles 21 to 34): **acceso** (access), **rectificación** (rectification), **cancelación** (cancellation), and **oposición** (opposition), plus the right to revoke consent. The responsable must communicate its determination on an ARCO request within a maximum of **twenty days** from receipt (Article 31), and, if the request is well founded, give effect to it within a further period set by the law. The 2025 law preserves the ARCO framework of the prior regime while reassigning the oversight and appeal functions to the Secretaría.

---

## Cross-border transfers

Transfers of personal data, whether domestic or international, are governed by Articles 35 and 36. A transfer to a third party (including a transfer abroad) generally requires that the privacy notice disclose the transfer and that the data subject consent, subject to the enumerated exceptions (for example, transfers required by law, to holding companies under common policies, or necessary for the performance of a contract in the data subject's interest). The transferee assumes the same obligations as the transferring controller.

---

## Security and breach

- **Security measures** (Article 18): the responsable must establish and maintain administrative, technical, and physical security measures to protect personal data against damage, loss, alteration, destruction, or unauthorized use, access, or processing.
- **Breach notification** (Article 19): security breaches occurring at any stage of processing that materially affect the data subjects' property or moral rights must be reported to the data subjects without delay, so that they can take measures to defend their rights.

---

## Enforcement and penalties

- **Enforcement** (Articles 55 to 59): the Secretaría conducts verification, adopts protective measures, and imposes sanctions through the procedures set out in the law; the data subject may bring a protection-of-rights proceeding.
- **Administrative fines**: the law sets fines expressed in multiples of the Unidad de Medida y Actualización (UMA), ranging up to **100 to 320,000 UMA** for the enumerated infringements, and provides that for infringements committed in the processing of **sensitive personal data** the sanctions may be increased up to twofold.
- **Criminal offences** (Articles 62 and 63): the law establishes criminal penalties (imprisonment) for a person who, being authorized to process personal data, causes a security breach for profit (Article 62), and for a person who processes personal data deceitfully for unlawful profit (Article 63).

The fine amounts are stated in UMA rather than a fixed peso figure because the UMA is indexed annually; an adopter converts to the current peso value using the UMA in force for the relevant year.

---

## Employment and workforce monitoring

Where the organization monitors the network and device activity of workers in Mexico, the processing of their personal data by a private party is governed by the LFPDPPP (the 2025 law) and, operationally, by the Workforce Network Monitoring Policy ([`security/policy-workforce-network-monitoring.md`](../../security/policy-workforce-network-monitoring.md)) and its supporting suite. The LFPDPPP has no employment-specific regime; workforce monitoring is subject to the law's general principles.

- **Purpose limitation and the general principles apply.** Monitoring must satisfy the principles of the LFPDPPP (Article 5), including finalidad (purpose), proporcionalidad (proportionality), calidad (quality), and licitud (lawfulness). A legitimate security aim states the purpose the monitoring serves; the purpose does not displace the requirement that the processing be limited to what is necessary and proportionate for that stated purpose, and monitoring data is not repurposed beyond the disclosed purposes.
- **Privacy notice (aviso de privacidad).** The responsable must make an aviso de privacidad available to workers before or at collection, stating the identity of the controller, the purposes of the monitoring, the means to exercise ARCO rights, the options to limit use or disclosure, and any transfers (Articles 14 to 16). This is the LFPDPPP counterpart to the workforce monitoring notice; the [Employee Monitoring Notice Template](../template-employee-monitoring-notice.md) provides content that is adapted to the aviso de privacidad form.
- **Consent and data-subject rights.** Under Article 7, all processing of personal data requires the data subject's consent unless a statutory exception in Article 9 applies; the LFPDPPP has no GDPR-style legitimate-interests basis. Workers retain the ARCO rights (access, rectification, cancellation, opposition; Articles 21 to 34) and the right to revoke consent (Article 7). Where the corpus's caution about the reliability of employment consent applies, the operative footing for monitoring is therefore not "general principles" but either an applicable Article 9 exception, most plausibly the exception for processing necessary to fulfil obligations arising from the legal relationship between the responsable and the worker (fact-dependent), or valid consent; the necessity and proportionality analysis in the [Legitimate Interest Assessment for Employment Monitoring Annex](../annex-legitimate-interest-employment-monitoring.md) is used only as an analytic aid for that assessment, adapted to the LFPDPPP's principles rather than to GDPR Article 6(1)(f).
- **Transfers.** Communication of monitored employee data to a third party or abroad is governed by the LFPDPPP transfer provisions (Articles 35 and 36), which generally require privacy-notice disclosure and consent subject to the enumerated exceptions, with the transferee assuming the same obligations.
- **Consultation, telemetry, and presence.** Where any representative-body or collective duty applies to introducing monitoring, it is determined and evidenced through the [Works Council and Employee Representative Consultation Procedure](../procedure-works-council-and-employee-representative-consultation.md). Connection metadata is governed by the [Network Telemetry and DPI Controls Standard](../standard-network-telemetry-and-dpi-controls.md) and presence signals by the [Presence Inference Limitations Standard](../standard-presence-inference-limitations.md), with the scope stated to workers mirroring the parent policy's in-scope and out-of-scope boundaries.

---

## Limitations

- This annex is a consolidating per-regime view of the private-sector LFPDPPP, not a substitute for the enacted law, its regulations, or legal advice; the controlling text is the LFPDPPP (DOF 20 March 2025, as last reformed).
- **Currency and authority.** The 2025 regime is recent and was itself reformed on 14 November 2025; the transfer of authority from the extinguished INAI to the Secretaría Anticorrupción y Buen Gobierno is part of a broader reform whose implementing regulations and institutional arrangements continue to settle. An adopter confirms the current authority, the last reform date, and any implementing regulation against the primary source before relying on a specific procedural detail.
- **Corpus cross-references.** On any divergence for Mexico private-sector processing between this annex and another corpus document, this annex governs the per-regime framing. Any residual reference to the former INAI reflects the pre-2025 regime; the current 2025 regime governs.
- Public-sector processing, the separate general transparency and public-data laws, and state-level rules are out of scope for this private-party annex.
