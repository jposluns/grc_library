# Cloud Exit and Data Portability Standard

**Document Title:** Cloud Exit and Data Portability Standard\
**Document Type:** Standard\
**Version:** 1.1.2\
**Date:** 2026-07-01\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md)\
**Classification:** Public\
**Category:** Supply Chain\
**Review Frequency:** Annual\
**Repository Path:** [`supply-chain/standard-cloud-exit-and-data-portability.md`](standard-cloud-exit-and-data-portability.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the requirements for planning, managing, and executing the exit from any cloud service provider or SaaS platform, and for ensuring portability of organisational data and workloads between platforms. It ensures that the organisation is not locked into any single cloud provider without a documented exit path, and that all cloud contracts include minimum data portability and deletion rights.

---

## 2. Scope

1. Applies to all cloud services, SaaS platforms, and managed services hosting organisational data or running organisational workloads.
2. Covers data portability requirements, exit planning obligations for new and existing contracts, and the process for executing a planned or emergency exit.
3. Applies to IT Operations, infrastructure programme teams, and Procurement when evaluating or contracting new cloud services.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CISO** | Owns this standard; approves cloud exit plans and any waiver of portability requirements. |
| **IT Operations / Cloud Team** | Maintains exit plans for all in-scope cloud services; executes exit procedures when required. |
| **Procurement / Legal** | Ensures that data portability and exit rights are included in all cloud and SaaS contracts before signature. |
| **Internal Audit** | Reviews exit plan currency and contract compliance annually. |

---

## 4. Contract requirements

All new cloud and SaaS contracts must include the following provisions before signature. Procurement must confirm their presence; contracts without these provisions require CISO approval before execution.

1. **Data export right:** The provider must allow the organisation to export all data in a documented, machine-readable, non-proprietary format at any time during the contract term and for a minimum of 90 days following contract termination.

2. **Data deletion confirmation:** Upon contract termination, the provider must confirm in writing that all organisational data has been deleted from their systems within a defined period, including backups.

3. **Exit assistance:** For Tier 1 and Tier 2 services (per the Asset Inventory Register), the contract must include a minimum 90-day exit assistance period during which the provider supports migration activities.

4. **No data lock-in:** Proprietary data formats that would prevent reasonable portability are not acceptable for Confidential or business-critical data without an approved migration path documented at contract entry.

---

## 5. Cloud exit plan requirements

An exit plan must exist for every cloud service hosting Tier 1 or Tier 2 assets. Exit plans are maintained by IT Operations and reviewed annually.

Each exit plan must document:

1. The target alternative platform or self-hosted option.
2. The data export method and format.
3. Estimated time to complete a full migration.
4. Dependencies that would be affected during migration (integrations, downstream systems, customers).
5. The last date the exit plan was tested or validated.

Exit plans for Tier 3 and Tier 4 services are recommended but not mandatory. New Tier 1 and Tier 2 services must have an exit plan documented before entering production.

---

## 6. Data portability standards

Data stored in cloud platforms must be exportable in open or widely supported formats:

| Data Type | Required Export Format |
| --- | --- |
| Structured data (databases) | SQL dump, CSV, or JSON; proprietary binary formats require a documented migration tool |
| Email and calendar | PST, MBOX, or EML for email; iCal for calendar |
| Documents and files | Native format or PDF; documents must be exportable via platform-provided tools |
| Infrastructure configuration | Infrastructure-as-code (e.g., Terraform, ARM templates, or equivalent); configuration must be version-controlled |
| Logs and audit data | JSON or CSV with defined schema; data must be exportable to meet retention requirements |

---

## 7. Exit triggers

An exit plan must be activated when any of the following occur:

- A provider announces service discontinuation.
- A provider is acquired and the acquirer is assessed as a security or compliance risk.
- Contractual terms change materially and negotiation fails.
- A security incident at the provider results in confirmed or suspected organisational data exposure.
- The CISO determines that continued use of the service presents unacceptable risk.

Emergency exits follow the Incident Response and Crisis Management escalation paths as appropriate.

---

## 8. Exceptions

Where a cloud provider cannot meet the contract requirements in this standard, for example, a commodity SaaS tool with no data export capability, the service may still be used for non-Confidential, non-Restricted data with CISO approval and a documented risk acceptance in the Exception Register.

---

## 9. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CSA CCM v4.1 | IPY-01 through IPY-04: Interoperability and Portability | Cloud exit and portability controls |
| ISO/IEC 27001:2022 | Annex A.5.20: Addressing Security in Supplier Agreements | Supplier contract requirements |
| NIST SP 800-53 | SA-9: External System Services | Third-party cloud service controls |
| GDPR (2018) | Article 20: Data Portability | Personal data portability rights |
| ENISA Cloud Computing | Exit and Portability Recommendations | Cloud exit planning guidance |

---

**End of Document**
