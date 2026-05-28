# Azure Cloud Hardening Baseline Standard

**Document Title:** Azure Cloud Hardening Baseline Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** Annual and upon material change to the cloud provider service catalogue, baseline benchmark releases, or organisational use of new service classes 
**Repository Path:** [`dev-security/standard-cloud-hardening-baseline-azure.md`](standard-cloud-hardening-baseline-azure.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the hardening baseline for Microsoft Azure environments operated by or on behalf of the organisation. It expresses outcomes and control intent in vendor-neutral language and references Azure service classes by their generic role rather than reproducing vendor configuration guidance verbatim.

---

## Scope

This standard applies to:

1. Azure tenants and subscriptions owned by the organisation.
2. Management group hierarchies, landing zones, and Cloud Adoption Framework constructs used to host organisational workloads.
3. Workloads operated by the organisation in Azure, regardless of whether the workload itself is open source or proprietary.
4. Azure infrastructure-as-code that provisions or configures the above.

It does not cover the contractual relationship with the provider, which is governed by the supplier security and privacy assurance standard.

---

## Baseline alignment

The standard aligns to the CIS Microsoft Azure Foundations Benchmark and to the Microsoft Cloud Security Benchmark without reproducing benchmark content verbatim. Adopting organisations confirm current versions of those baselines at each review.

---

## Section 1: tenant, subscription, and identity

| Control area | Requirement |
| --- | --- |
| Management group hierarchy | Workloads, environments (production, non-production), and trust tiers separated; landing zone topology applied |
| Subscription naming and ownership | Each subscription has a documented owner, environment, and purpose |
| Identity provider | The organisation's Azure Active Directory tenant is the primary identity provider; identity federation centralized |
| Global administrator accounts | Standing global administrators minimized; break-glass accounts separated, multi-factor protected, and monitored |
| Conditional access | Risk-based policies applied; legacy authentication blocked; device-trust requirements enforced for privileged access |
| Privileged identity | Privileged Identity Management or equivalent used for just-in-time privilege; standing assignments prohibited for sensitive roles |
| Application registrations | Reviewed for excessive permissions and consent risk; unused registrations removed |
| Service principals and managed identities | Managed identities preferred over secret-based service principals; remaining secrets rotated and inventoried |

---

## Section 2: detective controls and logging

| Control area | Requirement |
| --- | --- |
| Activity log | Subscription activity logs forwarded to a central, write-once destination |
| Sign-in and audit logs | Azure Active Directory sign-in and audit logs forwarded to the central destination |
| Multi-region coverage | Diagnostic settings enabled across regions where workloads operate |
| Diagnostic settings | Diagnostic logs enabled for sensitive resource classes; routing centralized |
| Security posture aggregator | Defender for Cloud or equivalent enabled across subscriptions; findings forwarded to the SOC ticketing scheme |
| Network telemetry | NSG flow logs or equivalent enabled where the cost-benefit profile justifies |
| Configuration recording | Azure Policy and Resource Graph used to evaluate continuous compliance |
| Log retention | Retention aligned to the logging standard; immutable copies as required |

---

## Section 3: preventive controls

| Control area | Requirement |
| --- | --- |
| Azure Policy | Organisation-level policies enforce allowed services, regions, SKUs, and dangerous-action restrictions |
| Region restriction | Workloads constrained to approved regions matching the data residency profile |
| Public access blocks | Default-blocking of public network access on storage and database services where supported |
| Resource locks | Locks applied to critical resources to prevent accidental deletion |
| Prevention of detective-control tampering | Modification or disablement of audit log forwarding, security posture, or policy enforcement restricted at the management-group level |
| Outbound network egress | Egress routed through controlled, inspected paths; default routes are not internet-default for sensitive subnets |

---

## Section 4: network

| Control area | Requirement |
| --- | --- |
| Network segmentation | Workloads placed in virtual networks and subnets aligned with their trust tier |
| Hub-and-spoke or virtual WAN | Central inspection topology; spoke-to-spoke traffic routes through the hub where required |
| Network security groups | Least privilege; no internet inbound for administrative ports |
| Application security groups | Used to abstract identity from address ranges |
| Private endpoints | Used for managed services where supported; data stays on the Microsoft backbone |
| DNS hygiene | Private DNS zones used internally; DNS query logging where the cost-benefit profile justifies |
| Edge protection | Web application firewall and DDoS Protection Standard in front of internet-facing services |
| Cross-tenant connectivity | Reviewed; ExpressRoute, VPN, and peering configurations documented |

---

## Section 5: data protection

| Control area | Requirement |
| --- | --- |
| Encryption at rest | Default encryption enabled; customer-managed keys for sensitive data |
| Key management | Keys held in Key Vault with HSM-backing where required; rotation aligned with the cryptographic key lifecycle |
| Cross-region key configuration | Multi-region key handling documented; recovery paths tested |
| Encryption in transit | TLS enforced for all listener configurations; deprecated protocols disabled |
| Data classification tags | Resources tagged with the data classification; controls applied per the data classification standard |
| Object lifecycle | Storage lifecycle management enforces retention and deletion per the records retention schedule |
| Backup | Recovery Services and Backup vaults configured per the backup and recovery procedure; immutability where required |
| Geo-redundant storage | Geo-redundant storage for high-availability data; aligned to the business continuity strategy |

---

## Section 6: compute

| Control area | Requirement |
| --- | --- |
| Virtual machine images | Approved, hardened, regularly updated images only; image provenance verified |
| Instance metadata service | Instance metadata access restricted at the workload level; IMDS protections applied |
| Disk encryption | OS and data disks encrypted; customer-managed keys for sensitive workloads |
| Patching | Update Manager applied per the patch management procedure |
| Remote access | Just-in-time VM access used; sessions logged; direct administrative SSH and RDP minimized |
| Container compute | Azure Kubernetes Service and Container Apps aligned to the container and image security standard |
| Serverless compute | Function permissions least-privilege; secrets from Key Vault; runtime versions current |
| Bastion topology | Azure Bastion or equivalent used; ephemeral access preferred |

---

## Section 7: storage

| Control area | Requirement |
| --- | --- |
| Blob storage | Block public access by default; firewall and private endpoint restrictions; access logging enabled |
| Disk storage | Encryption enabled; snapshot access controlled |
| File storage | Encryption in transit and at rest; access via private endpoints |
| Managed databases | SQL Database, Cosmos DB, PostgreSQL Flexible Server, and equivalents with encryption, automated backup, network restriction, parameter hardening, and audit logging enabled |
| Archive storage | Cool and archive tiers used per the records retention schedule; legal-hold controls available |

---

## Section 8: secrets and credentials

| Control area | Requirement |
| --- | --- |
| Secret storage | Secrets in Key Vault with appropriate access policies or role-based access; not in app settings or environment definitions |
| Rotation | Automated rotation where supported; manual-rotation tracking for others |
| Access | Role-based access on a per-vault basis; least privilege; access logged |
| Detection | Code repositories, CI logs, container layers, and VM extensions scanned for inadvertent secret exposure |
| Service principal secrets | Avoided where managed identities are available; remaining secrets age-limited |

---

## Section 9: monitoring, detection, and response

| Control area | Requirement |
| --- | --- |
| Threat detection | Defender for Cloud plans enabled across resource types; custom detections aligned to the organisation's threat model |
| SIEM | The Azure-native SIEM (Sentinel) or equivalent ingests Azure telemetry; analytics rules tuned |
| Alerting | Critical findings route to the SOC ticketing scheme; on-call paged where required |
| Response automation | Pre-approved playbooks; automation accountability separated from response decision |
| Forensic readiness | Snapshot, isolation, and quarantine capabilities tested; chain-of-custody documented per the incident response procedure |

---

## Section 10: supplementary services

| Service class | Requirement |
| --- | --- |
| Container orchestrator | Per the container and image security standard; API server endpoints not public |
| Serverless platform | Least-privilege managed identity; concurrency limits set; cold-start authentication validated |
| API Management | Per the API security standard |
| Edge and CDN | Origin access restricted; signed URL handling reviewed |
| Communication services | Sending identities restricted; SPF, DKIM, DMARC configured per the email security standard |
| AI and ML services | Azure OpenAI, Cognitive Services, Machine Learning aligned to the AI standards, including data residency and content-filter configuration |
| Logic Apps and Power Platform | Connectors inventoried; consent risk reviewed; data loss prevention policies configured |

---

## Section 11: tagging and inventory

| Control area | Requirement |
| --- | --- |
| Mandatory tags | Owner, environment, data classification, application, cost-centre |
| Tag enforcement | Provisioning gated on mandatory tags; non-compliant resources flagged via Azure Policy |
| Inventory | Resource Graph queries reconcile inventory with the configuration management database |
| Stale-resource cleanup | Unused resources identified and decommissioned; orphaned RBAC assignments and network artefacts reviewed regularly |

---

## Section 12: provisioning and change

| Control area | Requirement |
| --- | --- |
| Infrastructure as code | Production infrastructure provisioned via IaC (Bicep, Terraform, ARM); manual portal changes treated as incidents in production |
| Change pipeline | IaC changes follow the secure code review procedure |
| Drift detection | Drift between IaC state and live state detected and reconciled |
| Landing-zone automation | Subscription provisioning automated; baseline controls deployed at vending time |
| Production change windows | Per the change management procedure |

---

## Section 13: incident readiness

| Control area | Requirement |
| --- | --- |
| Tenant compromise playbook | Documented; tested; includes credential revocation, conditional access overrides, snapshot, isolation, and forensic preservation |
| Region failover | Tested per the business continuity strategy where regional resilience is required |
| Provider incident channel | Subscribed; Service Health and Defender for Cloud signals routed to the SOC ticketing scheme |
| Tabletop exercises | At least annually; covers loss of identity plane, data exfiltration, and credential compromise |

---

## Operating expectations

1. Baseline coverage is verified continuously through Azure Policy compliance and Defender for Cloud secure score signals.
2. Deviations are tracked as exceptions with risk acceptance recorded per the security exceptions process.
3. New Azure services are reviewed before adoption against the baseline and against the supplier security and privacy assurance standard.
4. Annual review aligns the baseline with the current CIS benchmark and Microsoft Cloud Security Benchmark.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CIS Microsoft Azure Foundations Benchmark | Current version | Azure hardening baseline |
| Microsoft Cloud Security Benchmark | Current version | Provider design guidance |
| Azure Well-Architected Security Pillar | Current version | Architecture guidance |
| NIST SP 800-53 Rev 5 | AC, AU, SC, CM, IR families | US baseline |
| NIST CSF 2.0 | Identify, Protect, Detect, Respond, Recover | Risk function alignment |
| ISO/IEC 27001:2022 | A.5, A.8 (selected) | Information security management |
| CSA CCM v5 | IAM, IVS, LOG, GRC | Cloud control matrix |
| PCI DSS v4 | Selected requirements where the environment processes cardholder data | Card data baseline |
| EU AI Act, GDPR | Privacy framework | Privacy compliance |

---

## Limitations

This standard is a public-domain baseline expressed in vendor-neutral terms. Azure service names, portal paths, and configuration parameters change frequently; specific implementation details are confirmed against current vendor documentation by the implementing engineer. The standard expresses outcomes and control intent, not provider-specific commands.

---

**End of Document**
