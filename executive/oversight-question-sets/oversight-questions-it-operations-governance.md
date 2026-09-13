# What the governing body should ask about the organization's change control, patch posture, estate inventory, monitoring, and service performance

**Document Title:** What the governing body should ask about the organization's change control, patch posture, estate inventory, monitoring, and service performance\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/register-it-operations-kpis.md`](../../operations/register-it-operations-kpis.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/oversight-question-sets/oversight-questions-it-operations-governance.md`](oversight-questions-it-operations-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Oversight Question Set\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md), [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/procedure-release-management.md`](../../operations/procedure-release-management.md), [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md), [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md), [`operations/standard-service-level-management.md`](../../operations/standard-service-level-management.md), [`operations/register-it-operations-kpis.md`](../../operations/register-it-operations-kpis.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-031\
**Last Reviewed:** 2026-09-13

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Context for these questions

Each question below is paired with the evidence a strong answer produces, and routes to the corpus document that governs it. The evidence is the organization's own populated artifact (its change records, its inventory extract, its KPI dashboard), not the routed corpus template or standard, which is the governing schema rather than evidence of the organization's state. A governing body learns more from the evidence a question produces than from an assurance that a control exists.

## Questions

**Theme: governance model and estate. Do we run operations under one controlled model, over a known estate?**

- *Do all our IT operational processes run under one governance model rather than team by team?* A strong answer produces the organization's operating ITSM process model and process ownership, run per the [IT service-management framework](../../operations/framework-it-service-management.md), and the records that show operational processes run under it, not a description of separate team practices.
- *Can we produce a current, authoritative inventory of the assets we operate?* A strong answer produces the [asset inventory](../../operations/register-asset-inventory.md) extract reconciled against discovered hardware and software, not a spreadsheet of unknown currency.

**Theme: change and release control. Are production changes authorized and reversible?**

- *For each recent production change, was it classified, approved, and given a rollback or forward-fix plan appropriate to its risk before it went live?* A strong answer produces the [change-management](../../operations/procedure-change-management-and-configuration-control.md) records and the [release-management](../../operations/procedure-release-management.md) records showing classification, approval, and the rollback or forward-fix plan, not an assurance that changes are controlled.
- *How would we find a change that reached production without going through the process?* A strong answer produces the configuration baseline and change records the [change-management and configuration-control procedure](../../operations/procedure-change-management-and-configuration-control.md) maintains, and the firewall and ACL change logging the [production security requirements standard](../../operations/standard-production-security-requirements.md) defines together with the infrastructure-as-code pipeline it requires, the record set an out-of-process change would be absent from.

**Theme: vulnerability and patch posture. Are known weaknesses worked through a defined process?**

- *For our known vulnerabilities, is each moving through a defined identify-to-verify process rather than ad hoc?* A strong answer produces the patch-compliance dashboard and deployment records the [patch-management procedure](../../operations/procedure-patch-management.md) defines, showing the current patch posture and what has been deployed and verified.
- *Do we test restores and disaster recovery on a defined cadence?* A strong answer produces the restore and recovery test records the [production security requirements standard](../../operations/standard-production-security-requirements.md) requires.

**Theme: detection and monitoring. Would we see an operational or security fault, and act on it?**

- *Are security events from our production systems collected, correlated, and driven to closure or escalation?* A strong answer produces the alert-to-closure records from the [security-monitoring and alert-management procedure](../../operations/procedure-security-monitoring-and-alert-management.md), not an assurance that monitoring is in place.
- *Is our current operational-security state recorded in one authoritative place?* A strong answer produces the current-state entries of the [IT-security-operations register](../../operations/register-it-security-operations.md).

**Theme: service performance and measurement. Are targets managed and reported to us?**

- *Are service targets set, breaches detected and escalated, and performance reported to this body?* A strong answer produces the SLA breach records and corrective-action logs the [service-level-management standard](../../operations/standard-service-level-management.md) identifies, the service-level performance against the agreed targets, and the [IT-operations KPI](../../operations/register-it-operations-kpis.md) dashboard for the period.

**A weak answer in any theme:** an assurance in place of a record. "Change is controlled" with no change record; "the estate is known" with no reconciled inventory; "we monitor" with no alert-to-closure evidence; "service is good" with no performance against targets.

## Evidence to request

- The organization's operating ITSM process model and process ownership, and the reconciled asset-inventory extract.
- The change-management and release records for recent production changes, with classification, approval, and the rollback or forward-fix plan.
- The patch-compliance dashboard and deployment records, and the restore and recovery test records.
- The security-monitoring alert-to-closure records, and the IT-security-operations register current-state entries.
- The SLA breach records and corrective-action logs, the service-level performance against targets, and the IT-operations KPI dashboard for the period.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the change-classification levels, the patch-remediation timelines, the KPI targets and availability thresholds, the service tiers and SLA terms, and the register schemas live in the linked documents and are not restated here. This page carries composite claims: the division of oversight it describes across the ITSM framework, inventory, change, release, patch, production-security, monitoring, security-operations, service-level, and measurement controls requires validation by the adopting organization against its own arrangements.

**End of Document**
