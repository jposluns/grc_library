# Breach Notification Regulator Register Template

**Document Title:** Breach Notification Regulator Register Template\
**Document Type:** Template\
**Version:** 1.0.1\
**Date:** 2026-07-02\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material regulatory change or new processing jurisdiction\
**Repository Path:** [`privacy/template-breach-notification-regulator-register.md`](template-breach-notification-regulator-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork. See the [role authority register](../governance/register-role-authority.md) for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template is an adopter-fillable register of the breach-notification obligations that bind the organization, one row per applicable regulator. It exists to close a specific gap: the breach-response procedure assesses notifiability at the time of a breach, but each regulator's deadline and trigger differ, and the organization has no single instrument recording, per regulator, **the regulatory deadline alongside an internal target deadline** that is set tighter than the regulatory one. Without that internal target, the organization has no operational clock of its own and risks managing each breach to the external deadline, leaving no margin.

The register records, for each regulator the organization is subject to: the jurisdiction, the governing law, the regulatory authority, the notification trigger, the regulatory deadline, the individual-notification requirement, and the organization's own internal target. The internal target is what the incident team actually runs to; the regulatory deadline is the legal backstop. The register lets the organization act within the **strictest applicable requirement** when a single breach engages more than one regime at once.

A populated register reflects the organization's regulatory footprint; complete it as a working document and keep it current.

## Scope

This register covers every breach-notification regime that applies to the organization's processing, determined by its establishments, the residence of the data subjects whose personal data it processes, and any sector-specific or contractual notification obligations. The applicable regimes are *[adopter-defined]* and are derived from the organization's [global regulatory applicability register](../compliance/register-global-regulatory-applicability.md).

This register is the per-regulator obligations record. It does not replace the [breach-response procedure](procedure-data-protection-and-privacy-breach-response.md), which governs detection, containment, the per-breach notifiability assessment, notification content, and recordkeeping; this register is the reference the procedure's notification-assessment step consults to determine deadlines and the controlling (strictest) requirement.

## How to use this register

1. **Populate one row per applicable regulator.** Derive the applicable set from the global regulatory applicability register and from sector-specific and contractual obligations. Add a row for each.
2. **Record the regulatory deadline and trigger exactly, and confirm them against the current authoritative source.** Notification deadlines and triggers change; confirm each against the regulator's current published requirement, not from memory or this template's illustrative rows.
3. **Set an internal target tighter than the regulatory deadline.** The internal target (*[adopter-defined]*) builds in margin for assessment, approval, and submission. Set it per regulator, or set one organization-wide internal target that satisfies the strictest applicable regulatory deadline.
4. **Identify the controlling requirement when more than one regime applies.** When a single breach engages multiple regimes, the organization acts within the **strictest applicable requirement** (the earliest deadline and the broadest notification obligation across the engaged rows).
5. **Review on the cadence and on change.** Re-confirm the register annually and whenever a regulator changes a requirement or the organization enters a new processing jurisdiction.

## The register

Replace the illustrative rows below with the organization's own. The illustrative rows are drawn from the jurisdiction examples in the breach-response procedure and are **not** authoritative; confirm every value against the current source for the organization's regimes.

| Jurisdiction / scope | Governing law | Regulatory authority | Notification trigger | Regulatory deadline | Individual-notification requirement | Internal target *[adopter-defined]* |
| --- | --- | --- | --- | --- | --- | --- |
| *[example]* European Union | GDPR Arts. 33 to 34 | Lead supervisory authority | Risk to the rights and freedoms of natural persons | 72 hours from becoming aware | Without undue delay where high risk to individuals | *[e.g. 48 hours to internal sign-off]* |
| *[example]* United Kingdom | UK GDPR Arts. 33 to 34 | Information Commissioner's Office (ICO) | Same threshold as EU GDPR | 72 hours from becoming aware | Without undue delay where high risk | *[adopter-set]* |
| *[adopter row]* | | | | | | |
| *[adopter row]* | | | | | | |
| *[adopter row]* | | | | | | |

> **Note on the "becoming aware" clock.** Where a regime starts its clock from the point the organization becomes aware of the breach (as the GDPR does), record in the breach record the moment awareness was established, because that moment, not the moment the breach occurred, starts the regulatory and internal clocks. A processor's delay in notifying the organization consumes part of the organization's own budget; the controlling supplier-notification timeline is governed by the [breach-response procedure](procedure-data-protection-and-privacy-breach-response.md).

## Internal target and the strictest-applicable-requirement rule

The internal target is the operational deadline the incident team runs to; it is set tighter than the regulatory deadline so that assessment, approval, and submission complete with margin before the legal backstop. When a single breach engages more than one regime:

- The controlling **regulatory deadline** is the earliest across the engaged rows.
- The controlling **individual-notification requirement** is the broadest across the engaged rows (notify if any engaged regime requires it).
- The **internal target** is set to satisfy the controlling regulatory deadline with margin.

The organization acts within the strictest applicable requirement; meeting the strictest deadline and the broadest obligation satisfies the others.

## Maintenance and review

The Data Protection Officer owns this register and keeps it current. Legal Counsel confirms the regulatory deadlines and triggers against authoritative sources. The register is reviewed on the cadence above and is the reference the [breach-response procedure](procedure-data-protection-and-privacy-breach-response.md) notification-assessment step consults.

## Limitations

This template is a CC BY-SA 4.0 structural baseline and is not legal advice. Breach-notification law is jurisdiction-specific and changes without notice; the illustrative rows are not authoritative and must not be relied on. Adopting organizations determine which regimes bind them, populate the register from the current authoritative source for each regime, set their internal targets, and obtain qualified legal counsel for notifiability determinations and submissions. The register records obligations; the [breach-response procedure](procedure-data-protection-and-privacy-breach-response.md) governs how the organization acts on them.

---

**End of Document**
