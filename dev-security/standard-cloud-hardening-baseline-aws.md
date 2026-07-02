# AWS Cloud Hardening Baseline Standard

**Document Title:** AWS Cloud Hardening Baseline Standard\
**Document Type:** Standard\
**Version:** 0.0.8\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material change to the cloud provider service catalogue, baseline benchmark releases, or organizational use of new service classes\
**Repository Path:** [`dev-security/standard-cloud-hardening-baseline-aws.md`](standard-cloud-hardening-baseline-aws.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the hardening baseline for Amazon Web Services environments operated by or on behalf of the organization. It expresses outcomes and control intent in vendor-neutral language and references AWS service classes by their generic role rather than reproducing vendor configuration guidance verbatim.

---

## 2. Scope

This standard applies to:

1. AWS accounts owned by the organization.
2. AWS organization structures, control towers, and landing zones used to host organizational workloads.
3. Workloads operated by the organization in AWS, regardless of whether the workload itself is open source or proprietary.
4. AWS infrastructure-as-code that provisions or configures the above.

It does not cover the contractual relationship with the provider, which is governed by the supplier security and privacy assurance standard.

### 2.1 Scope boundary with the operations cloud configuration baseline

This standard governs workload-level cloud hardening: application accounts/subscriptions/projects, the IaC that provisions them, in-workload IAM, workload network segmentation, encryption, secrets, and operational hardening. Enterprise-tenant concerns (identity-provider tenant, organization/management-group hierarchy, tenant-wide policies, productivity SaaS, email and collaboration platforms, cross-tenant administration) are governed by [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md). A workload conforms to both: the enterprise-tenant rules in the operations baseline, and the workload-level rules here.

---

## 3. Baseline alignment

The standard aligns to the CIS AWS Foundations Benchmark and to the AWS Well-Architected Security Pillar without reproducing benchmark content verbatim. Adopting organizations confirm current versions of those baselines at each review.

---

## 4. Account structure and identity

| Control area | Requirement |
| --- | --- |
| Multi-account structure | Workloads, environments (production, non-production), and trust tiers separated into distinct accounts; central audit, log, and security accounts |
| Root account | Root credentials secured with strong multi-factor authentication; root use minimized; root events alerted |
| Identity provider | Federated identity is the default; standing IAM users discouraged; identity centralized in a directory or workforce identity service |
| Permissions model | Least privilege; permission sets defined centrally; wildcard resource grants prohibited in production |
| Cross-account access | Role assumption with least privilege; external IDs and session policies used; standing cross-account trust minimized |
| Service-account credentials | Short-lived credentials via role assumption preferred over long-lived access keys; access keys rotated and alerted on age |
| Privileged role separation | Break-glass roles separated; use is logged and reviewed |

---

## 5. Detective controls and logging

| Control area | Requirement |
| --- | --- |
| Management-plane audit log | Enabled in all accounts; logs forwarded to a central, write-once destination |
| Multi-region coverage | Audit logging configured for all active regions; new-region activation triggers automatic enablement |
| Log integrity | Log integrity validation enabled; tampering detection alerted |
| Data-plane logging | Object-level and access logging enabled for storage resources holding sensitive data |
| Network flow logging | VPC flow logs and equivalent enabled where the cost-benefit profile justifies |
| Threat detection service | Provider threat detection enabled organization-wide; findings forwarded to the central detection pipeline |
| Configuration tracking | Configuration recording enabled organization-wide; baseline rules evaluate continuous compliance |
| Security posture aggregator | Findings from multiple sources aggregated centrally; routed to the SOC ticketing scheme |

---

## 6. Preventive controls

| Control area | Requirement |
| --- | --- |
| Service control policies | Organization-level guardrails block use of disallowed services, regions, and dangerous actions |
| Region restriction | Workloads constrained to approved regions matching the data residency profile |
| Public access blocks | Default-blocking of public access on storage services at the account or organization level |
| Permissions boundary | Permissions boundaries enforce maximum privilege ceilings for delegated administration |
| Prevention of detection-control tampering | Modification or disablement of audit log, threat detection, or configuration tracking blocked at the organization level |
| Outbound network egress | Egress to public networks goes through inspected, controlled paths; default routes are not internet-default for sensitive subnets |

---

## 7. Network

| Control area | Requirement |
| --- | --- |
| Network segmentation | Workloads placed in subnets aligned with their trust tier; public, private, and isolated subnets distinguished |
| Default network | Default networks deleted or unused; project-specific networks provisioned |
| Security groups | Least privilege; no 0.0.0.0/0 inbound for administrative ports |
| Cross-VPC connectivity | Transit gateway or central inspection account topology; spoke-to-spoke routed through inspection where required |
| Private connectivity to services | Private endpoints used for managed services where supported; data does not traverse the public internet between organizational components |
| DNS hygiene | Private DNS used internally; DNS query logging enabled for sensitive zones |
| Edge protection | Web application firewall and DDoS protection in front of internet-facing services; rate limiting tuned per the API security standard |

---

## 8. Data protection

| Control area | Requirement |
| --- | --- |
| Encryption at rest | Default encryption enabled for all data services; customer-managed keys for sensitive data |
| Key management | Keys managed in the key management service; rotation policies aligned with the cryptographic key lifecycle |
| Cross-region key replication | Where keys protect multi-region workloads, replication and recovery paths documented |
| Encryption in transit | TLS enforced for all listener configurations; deprecated protocols disabled |
| Data classification tags | Resources tagged with the data classification handled; controls applied per the data classification standard |
| Object lifecycle | Lifecycle policies enforce retention and deletion per the records retention schedule |
| Backup | Backups configured per the backup and recovery procedure; backup vault separated from primary account |
| Cross-account replication | Cross-account, cross-region replication for high-availability data; aligned to the business continuity strategy |

---

## 9. Compute

| Control area | Requirement |
| --- | --- |
| Virtual machine images | Approved, hardened, regularly updated images only; image provenance verified |
| Instance metadata service | Instance metadata service v2 enforced; v1 disabled |
| Disk encryption | Compute storage volumes encrypted at rest by default |
| Patching | Patch baseline applied via automation per the patch management procedure |
| Shell and remote access | Direct SSH or remote-desktop minimized; managed session services used; sessions logged |
| Container compute | Container compute aligned to the container and image security standard |
| Serverless compute | Function permissions least-privilege; secrets sourced from the secrets management service; runtime versions current |
| Bastion and jump | Where bastion or jump topology exists, sessions are recorded; ephemeral access preferred |

---

## 10. Storage

| Control area | Requirement |
| --- | --- |
| Object storage | Block public access by default; bucket policies versioned and reviewed; access logging enabled |
| Block storage | Encryption enabled; snapshots scoped and access-controlled |
| File storage | Encryption enabled in transit and at rest; access via private endpoints |
| Database storage | Managed databases with encryption, automated backup, network restriction, parameter hardening, and audit logging enabled |
| Archive storage | Archive tier used per the records retention schedule; legal-hold controls available |

---

## 11. Secrets and credentials

| Control area | Requirement |
| --- | --- |
| Secret storage | Secrets in the managed secrets service or parameter store with encryption; never in environment variable definitions in code |
| Rotation | Automated rotation for credentials with managed-service support; manual-rotation tracking for others |
| Access | Per-secret IAM policy; least privilege; audit logged |
| Detection | Code repositories, CI logs, container layers, and instance metadata scanned for inadvertent secret exposure |
| Static keys | Long-lived IAM access keys avoided; where unavoidable, age limits enforced and alerted |

---

## 12. Monitoring, detection, and response

| Control area | Requirement |
| --- | --- |
| Detection | Threat detection service enabled; custom detections aligned to the organization's threat model |
| Alerting | Critical findings route to the SOC ticketing scheme; on-call paged where required |
| Investigation tooling | Investigation tooling configured (audit log lake, query interface) |
| Response automation | Pre-approved playbooks for common findings; automation accountability separated from response decision |
| Forensic readiness | Snapshot and isolation capabilities tested; chain-of-custody process documented per the incident response procedure |

---

## 13. Supplementary services

| Service class | Requirement |
| --- | --- |
| Container orchestrator | Per the container and image security standard; orchestrator API endpoints not public |
| Serverless platform | Least-privilege execution roles; concurrency limits set; cold-start authentication validated |
| API gateway | Per the API security standard |
| Edge and content delivery | Origin access restricted; field-level encryption where appropriate; signed URL handling reviewed |
| Email and messaging | Sending identities restricted; SPF, DKIM, DMARC configured per the email security standard |
| AI and ML services | Per the AI standards, including data residency and training-data isolation |

---

## 14. Tagging and inventory

| Control area | Requirement |
| --- | --- |
| Mandatory tags | Owner, environment, data classification, application, cost-centre |
| Tag enforcement | Provisioning gated on mandatory tags; non-compliant resources flagged |
| Inventory | Central inventory of all accounts, regions, and resources; reconciled with the configuration management database |
| Stale-resource cleanup | Unused resources identified and decommissioned; orphaned IAM, security groups, and storage are reviewed regularly |

---

## 15. Provisioning and change

| Control area | Requirement |
| --- | --- |
| Infrastructure as code | Production infrastructure provisioned via IaC; manual console changes treated as incidents in production |
| Change pipeline | IaC changes follow the secure code review procedure |
| Drift detection | Drift between IaC state and live state detected and reconciled |
| Landing-zone automation | Account provisioning automated; baseline controls deployed at account creation |
| Production change windows | Per the change management procedure |

---

## 16. Incident readiness

| Control area | Requirement |
| --- | --- |
| Account compromise playbook | Documented; tested; includes credential revocation, snapshot, isolation, and forensic preservation |
| Region failover | Tested per the business continuity strategy where regional resilience is required |
| Provider incident channel | Subscribed; routed to the SOC ticketing scheme |
| Tabletop exercises | At least annually; covers loss of management plane, data exfiltration, and credential compromise |

---

## 17. Operating expectations

1. Baseline coverage is verified continuously through configuration tracking and posture management.
2. Deviations are tracked as exceptions with risk acceptance recorded per the security exceptions process.
3. New AWS services are reviewed before adoption against the baseline and against the supplier security and privacy assurance standard.
4. Annual review aligns the baseline with the current CIS benchmark and the current AWS Well-Architected guidance.

---

## 18. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CIS AWS Foundations Benchmark | Current version | AWS hardening baseline |
| AWS Well-Architected Security Pillar | Current version | Provider design guidance |
| NIST SP 800-53 Rev. 5 | AC, AU, SC, CM, IR families | US baseline |
| NIST CSF 2.0 | Identify, Protect, Detect, Respond, Recover | Risk function alignment |
| ISO/IEC 27001:2022 | A.5, A.8 (selected) | Information security management |
| CSA CCM v4.1 | IAM, I&S, LOG, GRC | Cloud control matrix |
| PCI DSS v4 | Selected requirements where the environment processes cardholder data | Card data baseline |
| EU AI Act, GDPR | Privacy framework | Privacy compliance |

---

## 19. Limitations

This standard is a CC BY-SA 4.0 baseline expressed in vendor-neutral terms. AWS service names, console paths, and configuration parameters change frequently; specific implementation details are confirmed against current vendor documentation by the implementing engineer. The standard expresses outcomes and control intent, not provider-specific commands.

---

**End of Document**
