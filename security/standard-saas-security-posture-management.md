# SaaS Security Posture Management Standard

**Document Title:** SaaS Security Posture Management Standard\
**Document Type:** Standard\
**Version:** 1.0.4\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to SaaS portfolio, threat-pattern, or platform-native posture controls\
**Repository Path:** [`security/standard-saas-security-posture-management.md`](standard-saas-security-posture-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the security posture management of the organization's SaaS portfolio: inventory, configuration baselines, continuous posture monitoring, SaaS-to-SaaS integration risk, third-party application access, shadow-SaaS detection, and offboarding. It complements the supplier programme (which addresses contractual and assurance posture) with the technical and configuration posture of SaaS in use.

---

## 2. Scope

This standard applies to every SaaS application used by the organization, regardless of:

1. Procurement path (sanctioned procurement, departmental purchase, individual subscription expensed back to the organization).
2. Tier (mission critical, important, productivity, niche).
3. Authentication path (federated SSO, social login, password-based).
4. Data sensitivity (personal data, business-sensitive, public).

It does not duplicate the cloud security configuration baseline standard (which covers IaaS and PaaS); it overlays SaaS-specific requirements on the broader cloud posture.

---

## 3. SaaS inventory

| Control area | Requirement |
| --- | --- |
| Authoritative inventory | Every SaaS application is inventoried with name, primary owner role, business purpose, data classification, user population, contract reference, and procurement status |
| Discovery sources | Inventory is fed by: identity provider applications, expense data, network egress telemetry, browser-based discovery, finance system data |
| Discovery cadence | Continuous where automated; quarterly review of consolidated inventory |
| Shadow-SaaS handling | Discovered unsanctioned SaaS triggers a procurement and security review; data migration to sanctioned alternatives or formal sanctioning |
| Decommissioned applications | Retired applications recorded with offboarding evidence |
| Customer-of-the-organization SaaS | Where the organization's own SaaS product is in scope, the inventory annotates it as out of scope for this internal-use standard |

---

## 4. Configuration baselines

Each Tier 1 (mission critical) and Tier 2 (important) SaaS application has a documented configuration baseline. The baseline covers, at minimum:

| Configuration area | Required baseline content |
| --- | --- |
| Identity and authentication | SSO via the enterprise identity provider; phishing-resistant MFA where the SaaS supports it; legacy authentication disabled; SCIM-based provisioning where available |
| Authorization and roles | Documented role-to-permission mapping; least-privilege roles defined; admin role minimization |
| External sharing | Sharing controls aligned with the data classification standard; external collaboration scope explicit |
| Data classification awareness | Sensitive-data labelling integrated where the SaaS supports it; per-class handling enforced |
| Audit logging | Native audit log enabled at the highest sensible level; export to the SIEM |
| Anomaly detection | SaaS-native detection (impossible travel, suspicious access, mass-download) enabled and routed to the SOC |
| Data residency | Data residency selected per organization policy where the SaaS supports the choice |
| API and integration | Documented integrations; OAuth scope minimization; webhook validation |
| Encryption | Encryption at rest enabled by default; encryption in transit enforced; customer-managed keys where the SaaS supports and the risk model requires |
| Backup and recovery | Native backup, retention, and restore tested; export capability validated |
| Mobile and unmanaged-device access | Per the BYOD policy; conditional access enforces device posture |
| Network restrictions | IP-allow-list applied where the SaaS supports it and the use case justifies it |
| Public sharing | Disabled by default; documented exceptions only |

The configuration baseline is captured per application; deviation requires risk acceptance per the exception process.

---

## 5. Continuous posture monitoring

| Control area | Requirement |
| --- | --- |
| Posture management capability | SSPM tooling deployed against Tier 1 and Tier 2 SaaS; manual posture verification for Tier 3 |
| Drift detection | Configuration drift from baseline detected and alerted within the SLA defined per tier |
| Remediation SLA | Tier 1 drift remediated within 5 business days; Tier 2 within 10 business days; Tier 3 within 20 business days |
| Posture report | Quarterly posture report per Tier 1 and Tier 2 application reviewed by the application owner and the security architecture function |
| Trend monitoring | Drift frequency per application is a leading indicator of configuration discipline; trend reviewed at the annual application review |
| User-onboarded automations | Tracking of user-created automations (Power Automate flows, Zapier, native automation) where they can affect data movement |

---

## 6. SaaS-to-SaaS integration risk

OAuth-grant-based SaaS-to-SaaS integrations expand the trust boundary. The standard applies the following controls.

| Control area | Requirement |
| --- | --- |
| Integration inventory | Every approved SaaS-to-SaaS integration is inventoried with the OAuth scopes granted, the principal that granted them, the business purpose, and the data exposure profile |
| Scope minimization | Integrations approved with the minimum OAuth scope required for the use case |
| Admin-consent governance | Admin-consent flows govern broad-scope integrations; standing user-consent for broad scopes prohibited |
| App allow-list | Approved-integration allow-list applied where the platform supports it |
| Periodic review | Integration list reviewed quarterly; stale integrations revoked |
| Token lifetime | Refresh-token lifetimes constrained per tenant policy |
| Anomalous-consent detection | Sudden mass-consent or anomalous-app-consent patterns alerted to the SOC |
| Third-party app risk scoring | Where SSPM tooling provides app risk scoring, scores reviewed before approval |

---

## 7. Third-party application access

Where employees, contractors, or partners use third-party applications to access organizational SaaS data:

| Control area | Requirement |
| --- | --- |
| Approved-marketplace applications | Pre-approved marketplace applications listed with their permitted use |
| Browser extension governance | Extensions with access to organization SaaS data managed; user-installed extensions reviewed |
| Personal-account separation | Personal accounts and organization accounts not interchangeable in any sanctioned client |
| Account-linking restrictions | Personal-account linking to organizational identities prohibited where it creates data leakage paths |
| Conditional access | Conditional access enforces the same posture for third-party clients as for first-party clients where the integration model supports it |

---

## 8. Shadow-SaaS detection and management

| Control area | Requirement |
| --- | --- |
| Detection sources | Egress telemetry; CASB; expense data; identity provider sign-in data; DNS data |
| Triage | Detected shadow SaaS reviewed within 5 business days; owner identified; data exposure assessed |
| Disposition | Three outcomes: formal sanctioning (procurement and baseline applied), migration to sanctioned alternative, block at the egress and identity provider |
| Communication | The line manager and end user are informed of the disposition with the rationale |
| Aggregate reporting | Quarterly shadow-SaaS report to the Executive Sponsor highlighting volume, risk, and remediation status |
| Continuous education | Awareness modules cover shadow-SaaS risks and the sanctioning path |

---

## 9. SaaS-to-SaaS supplier risk

| Control area | Requirement |
| --- | --- |
| Supplier programme integration | Every sanctioned SaaS application is in the supplier risk register at the appropriate tier |
| SOC 2 and equivalent currency | Per the supplier security and privacy assurance standard |
| Concentration analysis | SaaS suppliers feed the concentration risk register where multiple critical functions share an underlying provider |
| Vendor breach response | Supplier-disclosed breaches affecting a SaaS application trigger the incident response procedure |
| Lifecycle change | SaaS-supplier ownership changes (merger, acquisition, change of control) trigger supplier-risk reassessment |
| Exit strategy | Per the supplier exit and data return procedure; SaaS-specific data-portability tested |

---

## 10. Data protection within SaaS

| Control area | Requirement |
| --- | --- |
| Sensitivity labelling | Where the SaaS supports labelling, labels applied per the data classification standard |
| Data loss prevention | SaaS-native DLP enabled where available; integrated with the enterprise DLP per the DLP standard |
| Retention and disposal | Retention configured per the data retention schedule |
| Personal-data handling | Cross-reference to the ROPA where personal data is processed |
| Backup independence | For Tier 1 SaaS, an independent backup capability is operated where contractual and technical constraints permit |

---

## 11. Incident readiness

| Control area | Requirement |
| --- | --- |
| Tenant-level alerting | Per-tenant security alerts route to the SOC |
| Native incident response capability | Each Tier 1 SaaS has a documented incident playbook covering credential compromise, mass data movement, integration abuse |
| Forensic readiness | Native audit logs retained per the logging standard; export capability tested annually |
| Supplier-assist channel | Direct support channels documented and tested |
| Cross-tenant compromise scenarios | Where the SaaS is multi-tenant, the playbook addresses supplier-side disclosure of cross-tenant events |

---

## 12. Lifecycle

| Stage | Required action |
| --- | --- |
| Procurement | Supplier security and privacy assurance review; configuration baseline drafted; impact on the data-residency posture assessed |
| Onboarding | SSO and SCIM provisioning configured; baseline applied; SSPM monitoring enabled; users trained |
| Operation | Continuous posture monitoring; quarterly review; configuration baseline updates |
| Material change | Provider release-notes monitoring; baseline updated where the release exposes new controls or risks |
| Renewal | Supplier reassessment; baseline reverified; pricing and use review |
| Offboarding | Per the supplier exit and data return procedure; SaaS-specific data export and destruction |

---

## 13. Operating expectations

1. SaaS application onboarding requires both procurement and security gates before sanctioning.
2. The Tier 1 and Tier 2 baseline catalogue is reviewed annually for currency.
3. SSPM tooling deployment is owned by the security architecture function; tool selection follows the tool acceptance criteria pattern.
4. The organization does not assume that out-of-the-box SaaS configuration is secure; defaults are reviewed and hardened during onboarding.

---

## 14. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.5.19 to A.5.22 (supplier relationships), A.5.23 (cloud services) | Supplier and cloud security |
| CSA Cloud Controls Matrix v4.1 | Multiple domains | Cloud control baseline |
| CSA Security Trust Assurance and Risk (STAR) | CSA | SaaS provider assurance |
| NIST CSF 2.0 | PROTECT, DETECT | Posture and monitoring |
| NIST SP 800-204D | Strategies for Integrating Software Supply Chain Security | Supply-chain context |
| OWASP SaaS Application Security Checklist | OWASP | Practical checklist alignment |
| MITRE ATT&CK (Cloud) | Tactics and techniques | Threat coverage |

---

## 15. Limitations

This standard is a CC BY-SA 4.0 baseline. SaaS portfolios and platform-native controls evolve rapidly; configuration baselines are continuously updated. Tooling specifically labelled SSPM is one implementation; the standard's requirements can also be met through a combination of CASB, native cloud controls, and bespoke automation. Adopting organizations select tooling per the tool acceptance criteria.

---

**End of Document**
