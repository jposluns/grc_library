# Google Cloud Platform Hardening Baseline Standard

**Document Title:** Google Cloud Platform Hardening Baseline Standard\
**Document Type:** Standard\
**Version:** 0.0.2\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material change to the cloud provider service catalogue, baseline benchmark releases, or organisational use of new service classes\
**Repository Path:** [`dev-security/standard-cloud-hardening-baseline-gcp.md`](standard-cloud-hardening-baseline-gcp.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the hardening baseline for Google Cloud Platform environments operated by or on behalf of the organisation. It expresses outcomes and control intent in vendor-neutral language and references GCP service classes by their generic role rather than reproducing vendor configuration guidance verbatim.

---

## Scope

This standard applies to:

1. GCP organisation, folder, and project structures owned by the organisation.
2. Landing-zone and Cloud Foundation Toolkit constructs used to host organisational workloads.
3. Workloads operated by the organisation in GCP, regardless of whether the workload itself is open source or proprietary.
4. GCP infrastructure-as-code that provisions or configures the above.

It does not cover the contractual relationship with the provider, which is governed by the supplier security and privacy assurance standard.

### Scope boundary with the operations cloud configuration baseline

This standard governs workload-level cloud hardening: application accounts/subscriptions/projects, the IaC that provisions them, in-workload IAM, workload network segmentation, encryption, secrets, and operational hardening. Enterprise-tenant concerns (identity-provider tenant, organisation/management-group hierarchy, tenant-wide policies, productivity SaaS, email and collaboration platforms, cross-tenant administration) are governed by [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md). A workload conforms to both: the enterprise-tenant rules in the operations baseline, and the workload-level rules here.

---

## Baseline alignment

The standard aligns to the CIS Google Cloud Platform Foundations Benchmark and to the Google Cloud Architecture Framework security pillar without reproducing benchmark content verbatim. Adopting organisations confirm current versions of those baselines at each review.

---

## Section 1: organisation, folder, and identity

| Control area | Requirement |
| --- | --- |
| Resource hierarchy | Organisation, folders, and projects separate workloads, environments, and trust tiers; landing-zone topology applied |
| Project ownership | Each project has a documented owner, environment label, and purpose |
| Identity provider | Google Workspace or federated IdP is the source of identity; consumer Google accounts not used for organisational workloads |
| Super administrator accounts | Super administrators minimized; break-glass accounts separated, multi-factor protected, and monitored |
| IAM model | Least privilege; primitive roles (Owner, Editor, Viewer) avoided on production; predefined and custom roles preferred |
| Service accounts | Per-workload service accounts; default service accounts not used; service-account keys avoided in favour of workload identity, identity federation, or impersonation |
| Privilege elevation | Just-in-time access requested through Privileged Access Manager or equivalent; standing privileged assignments minimized |
| OAuth consent | Internal-only consent screen for organisational applications; external consent reviewed |

---

## Section 2: detective controls and logging

| Control area | Requirement |
| --- | --- |
| Cloud Audit Logs | Admin Activity, Data Access, System Event, and Policy Denied logs enabled organisation-wide and forwarded to a central, write-once destination |
| Data Access logs | Enabled selectively for sensitive resources, balancing cost and visibility |
| Sink configuration | Aggregated sinks at the organisation level route logs to the central destination |
| Log retention | Retention aligned to the logging standard; immutable copies as required |
| Security Command Center | Premium or Enterprise tier enabled organisation-wide; findings forwarded to the SOC ticketing scheme |
| Network telemetry | VPC Flow Logs enabled where the cost-benefit profile justifies |
| Configuration recording | Organisation Policy and Asset Inventory used to evaluate continuous compliance |

---

## Section 3: preventive controls

| Control area | Requirement |
| --- | --- |
| Organisation Policy | Constraints enforce allowed services, regions, locations, and dangerous-action restrictions at the organisation level |
| Region restriction | Workloads constrained to approved regions matching the data residency profile |
| VPC Service Controls | Service perimeters protect sensitive data services from data exfiltration |
| Public IP restriction | Public IPs restricted on VMs and managed services where supported |
| External access | External IAM grants restricted via domain-restricted-sharing policy |
| Prevention of detective-control tampering | Modification or disablement of audit logs, organisation policy, or Security Command Center restricted at the organisation level |
| Default network removal | Default network deleted; project-specific networks provisioned |

---

## Section 4: network

| Control area | Requirement |
| --- | --- |
| Shared VPC | Shared VPC used for centralized network governance where applicable |
| Network segmentation | Workloads placed in subnets aligned with their trust tier |
| Firewall rules | Least privilege; no 0.0.0.0/0 inbound for administrative ports; hierarchical firewall policies enforce organisation-wide rules |
| Private Google Access | Private Google Access and Private Service Connect used where supported; data does not traverse the public internet between organisational components |
| Cross-region connectivity | Cloud Interconnect, HA VPN, or peering configurations documented and reviewed |
| DNS hygiene | Private DNS zones used internally; DNS logging where the cost-benefit profile justifies |
| Edge protection | Cloud Armor and Cloud CDN configured for internet-facing services; rate limiting tuned per the API security standard |
| Identity-Aware Proxy | IAP used in preference to public exposure for internal applications where appropriate |

---

## Section 5: data protection

| Control area | Requirement |
| --- | --- |
| Encryption at rest | Default encryption enabled; customer-managed encryption keys (CMEK) for sensitive data |
| Key management | Keys held in Cloud KMS with HSM backing where required; rotation aligned with the cryptographic key lifecycle |
| External keys | Cloud External Key Manager used where keys must remain under external custody |
| Encryption in transit | TLS enforced for all listener configurations; deprecated protocols disabled; Google-fronted backbone preferred |
| Data classification labels | Resources labelled with the data classification; controls applied per the data classification standard |
| Object lifecycle | Cloud Storage lifecycle policies enforce retention and deletion per the records retention schedule |
| Backup | Backup and DR Service or equivalent per the backup and recovery procedure; immutability where required |
| Multi-region storage | Multi-region or dual-region storage for high-availability data; aligned to the business continuity strategy |
| Sensitive data discovery | Sensitive Data Protection (formerly DLP) used to discover and classify sensitive data |

---

## Section 6: compute

| Control area | Requirement |
| --- | --- |
| Virtual machine images | Approved, hardened, regularly updated images only; image provenance verified; Shielded VMs and Confidential VMs used where appropriate |
| Instance metadata service | Metadata access restricted; legacy v0.1 metadata disabled |
| Disk encryption | Persistent disks encrypted; CMEK for sensitive workloads |
| Patching | OS Config Patch service applied per the patch management procedure |
| Remote access | OS Login enforced; Identity-Aware Proxy used for SSH and RDP; direct administrative access minimized; sessions logged |
| Container compute | GKE clusters aligned to the container and image security standard; private clusters preferred; workload identity used for pod-to-service authentication |
| Serverless compute | Cloud Run, Cloud Functions, and App Engine with least-privilege service accounts; secrets sourced from Secret Manager; runtime versions current |
| Bastion topology | Where bastion topology exists, sessions are recorded; ephemeral access preferred |

---

## Section 7: storage

| Control area | Requirement |
| --- | --- |
| Cloud Storage | Uniform bucket-level access enabled; public access prevention enforced; bucket policies versioned and reviewed |
| Persistent disks | Encryption enabled; snapshot access controlled |
| Filestore | Encryption in transit and at rest; access via private endpoints |
| Managed databases | Cloud SQL, Spanner, BigQuery, Firestore, and equivalents with encryption, automated backup, network restriction, parameter hardening, and audit logging enabled |
| Archive storage | Archive and coldline tiers used per the records retention schedule; bucket lock and retention policies available for legal hold |

---

## Section 8: secrets and credentials

| Control area | Requirement |
| --- | --- |
| Secret storage | Secrets in Secret Manager with CMEK where appropriate; not in environment variable definitions in code |
| Rotation | Automated rotation where supported; manual-rotation tracking for others |
| Access | Per-secret IAM; least privilege; access audit-logged |
| Detection | Code repositories, CI logs, container layers, and instance metadata scanned for inadvertent secret exposure |
| Service-account keys | Avoided where workload identity federation is available; remaining keys age-limited and rotated |

---

## Section 9: monitoring, detection, and response

| Control area | Requirement |
| --- | --- |
| Threat detection | Security Command Center Premium or Enterprise tier with Threat Detection, Container Threat Detection, and Event Threat Detection enabled |
| SIEM integration | Findings exported to the organisation's SIEM via Pub/Sub or direct sink |
| Alerting | Critical findings route to the SOC ticketing scheme; on-call paged where required |
| Response automation | Pre-approved playbooks; automation accountability separated from response decision |
| Forensic readiness | Snapshot and isolation capabilities tested; chain-of-custody documented per the incident response procedure |

---

## Section 10: supplementary services

| Service class | Requirement |
| --- | --- |
| Container orchestrator | GKE per the container and image security standard; control plane not public on internet |
| Serverless platform | Least-privilege service account; concurrency limits set; cold-start authentication validated |
| API Gateway | Per the API security standard |
| Edge and CDN | Origin access restricted; signed URL handling reviewed |
| Pub/Sub messaging | Topic and subscription IAM least-privilege; CMEK for sensitive payloads |
| AI and ML services | Vertex AI, Gemini API, and managed AI services aligned to the AI standards, including data residency and content-safety configuration |
| BigQuery analytics | Column-level access controls, row-level security, and policy tags applied for sensitive data |

---

## Section 11: labelling and inventory

| Control area | Requirement |
| --- | --- |
| Mandatory labels | Owner, environment, data classification, application, cost-centre |
| Label enforcement | Provisioning gated on mandatory labels; non-compliant resources flagged via Organisation Policy |
| Inventory | Cloud Asset Inventory queries reconcile inventory with the configuration management database |
| Stale-resource cleanup | Unused resources identified and decommissioned; orphaned IAM bindings, firewall rules, and storage reviewed regularly |

---

## Section 12: provisioning and change

| Control area | Requirement |
| --- | --- |
| Infrastructure as code | Production infrastructure provisioned via IaC (Terraform, Config Connector, Deployment Manager); manual console changes treated as incidents in production |
| Change pipeline | IaC changes follow the secure code review procedure |
| Drift detection | Drift between IaC state and live state detected and reconciled |
| Landing-zone automation | Project provisioning automated; baseline controls deployed at vending time |
| Production change windows | Per the change management procedure |

---

## Section 13: incident readiness

| Control area | Requirement |
| --- | --- |
| Organisation compromise playbook | Documented; tested; includes credential revocation, IAM rollback, snapshot, isolation, and forensic preservation |
| Region failover | Tested per the business continuity strategy where regional resilience is required |
| Provider incident channel | Subscribed; Personalised Service Health and Security Command Center signals routed to the SOC ticketing scheme |
| Tabletop exercises | At least annually; covers loss of identity plane, data exfiltration, and credential compromise |

---

## Operating expectations

1. Baseline coverage is verified continuously through Organisation Policy compliance and Security Command Center posture signals.
2. Deviations are tracked as exceptions with risk acceptance recorded per the security exceptions process.
3. New GCP services are reviewed before adoption against the baseline and against the supplier security and privacy assurance standard.
4. Annual review aligns the baseline with the current CIS benchmark and Google Cloud Architecture Framework guidance.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CIS Google Cloud Platform Foundations Benchmark | Current version | GCP hardening baseline |
| Google Cloud Architecture Framework, Security Pillar | Current version | Provider design guidance |
| NIST SP 800-53 Rev 5 | AC, AU, SC, CM, IR families | US baseline |
| NIST CSF 2.0 | Identify, Protect, Detect, Respond, Recover | Risk function alignment |
| ISO/IEC 27001:2022 | A.5, A.8 (selected) | Information security management |
| CSA CCM v4.1 | IAM, IVS, LOG, GRC | Cloud control matrix |
| PCI DSS v4 | Selected requirements where the environment processes cardholder data | Card data baseline |
| EU AI Act, GDPR | Privacy framework | Privacy compliance |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline expressed in vendor-neutral terms. GCP service names, console paths, and configuration parameters change frequently; specific implementation details are confirmed against current vendor documentation by the implementing engineer. The standard expresses outcomes and control intent, not provider-specific commands.

---

**End of Document**
