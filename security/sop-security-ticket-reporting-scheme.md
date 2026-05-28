# Security Ticket Reporting Scheme

**Document Title:** Security Ticket Reporting Scheme 
**Document Type:** SOP 
**Version:** 1.1.0 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Security Officer 
**Related Documents:** [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual or upon significant change to vendor or tooling landscape 
**Repository Path:** [`security/sop-security-ticket-reporting-scheme.md`](sop-security-ticket-reporting-scheme.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This SOP defines the standard naming and reporting scheme for security incident tickets. A consistent naming convention allows the SOC and management to rapidly identify the vendor, ITSM ticket, and incident type without opening the full ticket record, improving communication speed during incident response.

---

## Ticket naming convention

When reporting security incidents to management or creating escalation records, the following naming format must be used:

```
[VENDOR-TAG] - [ITSM-TICKET-ID] [ALERT-NAME] - [AFFECTED-USER-OR-SYSTEM]
```

**Example:**
```
SOC - [IN-007456] Unfamiliar sign-in properties involving one user - j.smith@example.com
```

---

## Vendor tag assignment

Each security vendor or service partner is assigned a short tag (2 to 4 characters) used as the prefix in incident ticket names. Vendor tags are maintained by the CISO and reviewed annually.

| Vendor Category | Tag Assignment Approach |
| --- | --- |
| SOC / Managed Detection and Response (MDR) | Assigned at onboarding; reviewed annually |
| Network security / SD-WAN providers | Assigned at onboarding |
| Endpoint detection and response (EDR) platforms | Assigned at onboarding |
| Security testing partners | Assigned per engagement |
| Cloud security services | Assigned at onboarding |

The current vendor tag table is maintained in the IT Security Operations Register and is available to the SOC team. Tags are not included in this public document as the vendor register is operationally maintained.

---

## Naming format components

| Component | Description | Example |
| --- | --- | --- |
| **Vendor Tag** | 2 to 4 character code identifying the reporting vendor or service | `MDR`, `EDR`, `SOC` |
| **ITSM Ticket ID** | The organisation's ITSM portal ticket number in brackets | `[IN-007456]` |
| **Alert Name** | Full name of the alert or finding as reported by the vendor or tool | `Unfamiliar sign-in properties involving one user` |
| **Affected User or System** | Full name or system identifier of the affected entity | `j.smith@example.com` or `SRV-PROD-001` |

---

## Usage rules

1. **Begin with the vendor tag** that generated or reported the incident.
2. **Follow with a hyphen and the ITSM ticket number** from the ITSM portal in square brackets.
3. **Include the full alert name** as reported by the vendor or detection tool: do not abbreviate.
4. **End with the affected user or system** to allow rapid identification of impact scope.
5. If multiple users or systems are affected, note the primary affected party and add "(+N others)" as appropriate.
6. For incidents without a vendor (e.g., self-reported by staff), use `INT` as the vendor tag.

---

## Ticket creation requirements

All security incident tickets must be created in the ITSM portal before escalation to management. Verbal or informal reports must be formalized in the ITSM portal within 1 hour for P1/P2 incidents and within 4 hours for P3/P4 incidents.

The ticket must link to:
- The vendor alert or report (where applicable).
- The escalation record if escalation has occurred.
- Post-incident review findings upon closure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27035:2023 | Information Security Incident Management | Incident recording and reporting |
| NIST SP 800-61r3 | Computer Security Incident Handling Guide | Incident documentation standards |
| COBIT 2019 | DSS02: Manage Service Requests and Incidents | Incident tracking and reporting |

---

**End of Document**
