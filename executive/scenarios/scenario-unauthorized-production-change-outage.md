# When an unauthorized production change takes a critical service down

**Document Title:** When an unauthorized production change takes a critical service down\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-unauthorized-production-change-outage.md`](scenario-unauthorized-production-change-outage.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/procedure-release-management.md`](../../operations/procedure-release-management.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), [`operations/standard-service-level-management.md`](../../operations/standard-service-level-management.md), [`operations/register-it-operations-kpis.md`](../../operations/register-it-operations-kpis.md), [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-032\
**Last Reviewed:** 2026-09-13

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

Under time pressure, an operator applies a firewall or access-control change directly to a production system to resolve an urgent request, bypassing the change process. The change disrupts a critical service. This scenario walks the event through the controls the operations corpus sets, to show a governing body where each engages and what evidence a well-run response leaves behind.

## How the event unfolds

The change was made outside the process, not through it. An emergency-change path exists in the corpus for a change required to resolve or prevent a critical service outage or active security incident; the failure here is that the process was bypassed, not that no fast path was available. What follows is either an outage caught quickly through detection and reversed under control, or one found late by a client and resolved by improvisation.

## Where the corpus controls engage

- **The control bypassed.** The [production security requirements standard](../../operations/standard-production-security-requirements.md) is the control the change went around: it requires firewall and access-control changes to go through a reviewed, documented change request.
- **The gate it should have passed.** The [change-management and configuration-control procedure](../../operations/procedure-change-management-and-configuration-control.md) is where the change should have been classified, approved, and recorded, including through its emergency-change path for a critical outage or active security incident.
- **Restoration.** The [release-management procedure](../../operations/procedure-release-management.md) is where a rollback or forward-fix plan is defined: rollback reverses the change through its pre-tested mechanism, and a forward-fix is deployed where rollback is not viable, the basis for restoring the service under control.
- **Detection.** The [security-monitoring and alert-management procedure](../../operations/procedure-security-monitoring-and-alert-management.md) is where a firewall or access-control change made outside an approved window raises an alert, and where events are correlated and driven to closure, rather than waiting for a client to report it.
- **Service impact.** The [service-level-management standard](../../operations/standard-service-level-management.md) is where, if the disruption misses an availability or resolution target with no approved exclusion, the resulting breach is detected and escalated.
- **Governance visibility.** The [IT-operations KPI register](../../operations/register-it-operations-kpis.md) is where the availability and change indicators that carry the event into governance reporting are defined.
- **Scoping the impact.** The [asset inventory register](../../operations/register-asset-inventory.md) is the estate record used to identify and scope the affected systems; the configuration baseline and its drift records establish what was changed.

## What good looks like

The unauthorized change raised an alert, and where it missed a service target the service-level breach was recorded, rather than a client call being the first signal. The configuration and change records showed what was changed and by whom. The service was restored through the defined rollback or forward-fix plan rather than by improvisation. The event reached governance through the operations indicators on their cadence. Each of those is a control the organization can point to and evidence.

## Evidence to request

- The alert record and its correlation and closure, from the monitoring workflow.
- Any service-level breach record and the escalation it triggered.
- The change record that should have existed, and the configuration baseline showing the unauthorized change against it.
- The rollback or forward-fix record for the restoration.
- The asset-inventory extract used to scope the affected systems.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the availability and change KPI targets, the service tiers and SLA terms, the change-classification levels, the restore and recovery cadences, and the register schemas live in the linked documents and are not restated here. This page carries composite claims: the sequence it describes across the bypassed control, the change gate, reversal, detection, service impact, governance visibility, and scoping requires validation by the adopting organization against its own arrangements. The scenario is illustrative and makes no likelihood claim; a real event's facts determine which controls engage and how.

**End of Document**
