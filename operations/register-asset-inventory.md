# Asset Inventory Register

**Document Title:** Asset Inventory Register  
**Document Type:** Register  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Officer  
**Approving Authority:** Chief Information Officer  
**Related Documents:** [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`operations/procedure-patch-management.md`](procedure-patch-management.md), [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md), [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md)  
**Classification:** Public  
**Category:** Operations  
**Review Frequency:** Continuous (automated) with quarterly manual validation  
**Repository Path:** [`operations/register-asset-inventory.md`](register-asset-inventory.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This register defines the schema, governance, and classification model for the organisational Asset Inventory. The Asset Inventory is the authoritative record of all IT hardware, software, cloud resources, data assets, and AI systems owned, managed, or used by the organisation. It supports risk assessments, vulnerability management, disaster recovery planning, and compliance activities.

---

## Scope

Covers all organisational assets including:
- Physical hardware: servers, workstations, laptops, mobile devices, network devices, printers.
- Software: operating systems, applications, databases, development tools, cloud services.
- Cloud resources: virtual machines, containers, cloud storage, managed services.
- Data assets: datasets, databases, backups, archives.
- AI systems: ML models, automated decision engines, generative AI tools.
- Operational technology (OT) where applicable.

---

## Asset Classification

| Classification | Description | Examples |
| --- | --- | --- |
| **Tier 1 — Mission Critical** | Assets whose failure causes immediate operational halt or significant customer impact | Core ERP, identity systems, production network infrastructure |
| **Tier 2 — Essential** | Assets whose failure causes significant operational disruption within 24 hours | Email platform, financial systems, primary data systems |
| **Tier 3 — Important** | Assets whose failure causes limited disruption; recoverable within 72 hours | Reporting tools, collaboration platforms, departmental applications |
| **Tier 4 — Non-Critical** | Assets whose failure has minimal operational impact | Development environments, test systems, legacy archives |

---

## Asset Record Schema

Each asset record must contain the following fields:

| Field | Description |
| --- | --- |
| **Asset ID** | Unique identifier |
| **Asset Name** | Descriptive name |
| **Asset Type** | Hardware / Software / Cloud Resource / Data Asset / AI System |
| **Classification Tier** | Tier 1–4 (from table above) |
| **Data Classification** | Public / Internal / Confidential / Restricted |
| **Owner** | Role title of responsible party |
| **Custodian** | Team or individual managing the asset operationally |
| **Location** | Physical location, data centre, or cloud region |
| **Platform / Environment** | Production / DR / Development / Test |
| **Version / Build** | Current version or build number |
| **Licence** | Licence type, expiry date, and seat count (software) |
| **Vendor / Manufacturer** | Supplier name |
| **Support Status** | Supported / End-of-Support / End-of-Life |
| **End-of-Life Date** | Known or estimated end-of-life |
| **Last Vulnerability Scan** | Date of most recent vulnerability scan |
| **Last Patched** | Date of most recent security patch |
| **Backup Status** | Backup schedule, last successful backup, RPO |
| **DR Classification** | Tier 1–4 aligned to IT DR Plan |
| **Date Added** | Date asset entered inventory |
| **Last Reviewed** | Date of most recent manual validation |

---

## Governance

### Ownership

- The CIO owns the Asset Inventory and is accountable for its completeness.
- IT Operations maintains the inventory on a day-to-day basis using automated discovery tooling integrated with the IT Asset Management System.
- Each asset must have a named owner (role title) who is responsible for its currency, security, and lifecycle management.

### Automated Discovery

- Automated discovery tools scan the network and cloud environments continuously to detect new, changed, or removed assets.
- Unregistered assets detected by automated discovery are flagged as unauthorised and reviewed within 2 business days.
- Cloud resource tagging standards enforce mandatory owner, classification, and environment tags on all cloud assets.

### Manual Validation

- Asset owners validate their asset records quarterly to confirm accuracy.
- IT Operations conducts a full inventory reconciliation annually, comparing automated discovery results against the registered inventory.
- Discrepancies are investigated and resolved within 10 business days.

### Unauthorised Assets

- Assets detected in the environment that are not in the inventory are treated as potentially unauthorised.
- Unauthorised assets are quarantined from network access pending investigation.
- Investigation determines whether the asset is approved (and must be registered) or unauthorised (and must be removed).

---

## Lifecycle Management

| Lifecycle Stage | Trigger | Action |
| --- | --- | --- |
| **Registered** | Asset acquired or deployed | Add to inventory with all required fields |
| **Active** | Asset in production use | Monitor, patch, and review per asset tier requirements |
| **End-of-Support** | Vendor ends support | Risk assessment; migration or exception required |
| **Decommissioning** | Asset replaced or retired | Secure data destruction; remove from inventory |
| **Decommissioned** | Asset removed from service | Retain record for audit for minimum 3 years |

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | Annex A.5.9 — Inventory of Information and Other Assets | Asset inventory requirement |
| ISO/IEC 27002:2022 | §5.9–5.10 | Asset ownership and acceptable use |
| NIST SP 800-53 | CM-8 — Information System Component Inventory | Asset inventory controls |
| COBIT 2025 | BAI09 — Manage Assets | IT asset lifecycle management |
| CSA CCM v5 | AIS-01 / HRS-01 | Cloud asset inventory and management |

---

**End of Document**
