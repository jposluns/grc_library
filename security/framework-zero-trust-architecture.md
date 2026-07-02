# Zero Trust Architecture Framework

**Document Title:** Zero Trust Architecture Framework\
**Document Type:** Framework\
**Version:** 0.0.4\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/policy-network-communications-security.md`](policy-network-communications-security.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md), [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material architectural, threat, or regulatory change\
**Repository Path:** [`security/framework-zero-trust-architecture.md`](framework-zero-trust-architecture.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework defines the organization's approach to zero trust architecture (ZTA): the principles, pillars, control patterns, and migration model that bring identity, device, network, application, data, and workload controls into a coherent posture where trust is never implicit. It supports the migration from perimeter-based security to a model in which every request is authenticated, authorized, and continuously evaluated.

---

## Scope

This framework applies to all corporate, production, partner-integrated, and customer-facing environments. It applies to human and non-human identities (service accounts, agents, automation), to managed and unmanaged devices, to internal and external network paths, and to all workloads regardless of hosting model (cloud, on-premises, hybrid, edge).

---

## Principles

| Principle | Statement |
| --- | --- |
| Never trust, always verify | Every access request is authenticated and authorized regardless of source network |
| Least privilege | Access is granted at the smallest scope and shortest duration consistent with the task |
| Assume breach | Defences are designed assuming the adversary is already inside; lateral movement is constrained |
| Verify explicitly | Authentication and authorization use multiple signals including identity, device posture, location, and behaviour |
| Continuous evaluation | Trust is re-evaluated during a session; static-at-login trust is insufficient |
| Per-resource policy | Policy is enforced as close to the protected resource as possible, not at a perimeter |
| Identity as the new perimeter | The identity layer is the primary policy boundary for human and non-human actors |

---

## Pillars

The framework adopts seven pillars consistent with the CISA Zero Trust Maturity Model.

### Pillar 1: Identity

| Capability | Maturity expectation |
| --- | --- |
| Identity provider consolidation | Single enterprise identity provider for human and non-human identities; reduced standing identities |
| Authentication strength | Phishing-resistant multi-factor authentication (FIDO2, platform authenticators) for privileged and sensitive access; risk-based MFA for general access |
| Just-in-time access | Standing access removed where activation-based access is feasible |
| Session-level signals | Risk scoring at each authentication and material session event |
| Non-human identity | Service identities issued, scoped, rotated; workload identity used where supported |

### Pillar 2: Devices

| Capability | Maturity expectation |
| --- | --- |
| Device inventory | Authoritative inventory of every device that connects to organization resources |
| Compliance enforcement | Policy-based access controls deny non-compliant devices |
| Posture evaluation | Continuous posture (patch level, encryption, EDR health) feeds the policy engine |
| Bring-your-own device | BYOD posture model defined and enforced where the BYOD policy permits |
| Embedded and IoT | Inventory and segmentation specifically for embedded and IoT devices |

### Pillar 3: Networks

| Capability | Maturity expectation |
| --- | --- |
| Macro-segmentation | Production, development, and operations environments separated at the network layer |
| Micro-segmentation | Workload-to-workload communication explicitly allowed; default deny |
| Encryption in transit | TLS 1.3 or stronger for east-west and north-south traffic; mTLS for high-sensitivity service-to-service |
| Software-defined access | Replaces VPN where feasible; application-level access without network-level access |
| DNS security | DNS resolution monitored; protected against tunnelling, exfiltration, and DGA patterns |
| Egress controls | Production egress restricted; allow-list for required external destinations |

### Pillar 4: Applications and workloads

| Capability | Maturity expectation |
| --- | --- |
| Application identity | Each application has a service identity and a documented purpose |
| Access broker | Application access mediated by an access broker that enforces policy |
| Application security testing | Per the dev-security standards |
| Workload attestation | Workloads attest their integrity before receiving secrets or sensitive data |
| Container and serverless security | Per the container and serverless platform configuration baselines |
| AI access | AI capabilities integrated through the AI access and agent permissions standard |

### Pillar 5: Data

| Capability | Maturity expectation |
| --- | --- |
| Data classification | Per the data classification and handling standard |
| Data discovery | Automated discovery of sensitive data across cloud and on-premises stores |
| Encryption at rest | Standard for all Confidential and Restricted classifications; key management per the cryptographic framework |
| Data loss prevention | Per the DLP standard |
| Rights management | Information rights management for highly sensitive content where the workflow supports it |
| Data movement controls | Egress from data stores instrumented and policy-controlled |

### Pillar 6: Visibility and analytics

| Capability | Maturity expectation |
| --- | --- |
| Telemetry coverage | Identity, device, network, application, and data events centralized in the SIEM |
| Anomaly detection | Behavioural baselines and anomaly detection across users, devices, and workloads |
| Detection content | Use-case-driven detection content reviewed quarterly |
| Continuous monitoring | Per the logging and monitoring standard |
| AI-aware detection | AI-specific detection content per the AI incident response plan |

### Pillar 7: Automation and orchestration

| Capability | Maturity expectation |
| --- | --- |
| Policy as code | Access policy expressed and version-controlled |
| Automated response | Containment actions automated for defined triggers; gated with human approval where impact is material |
| Identity lifecycle automation | Provisioning and deprovisioning automated from the authoritative source |
| Certificate and secret rotation | Automated; lifecycle integrated with the cryptographic key lifecycle framework |
| Posture remediation | Automated remediation for common non-compliance patterns |

---

## Policy engine

The framework requires a logical policy engine that evaluates each access request using:

| Input signal | Source |
| --- | --- |
| User identity and group | Enterprise identity provider |
| Authentication strength | Identity provider claim |
| Session risk | Risk engine signals (location, device, behaviour) |
| Device posture | Endpoint management and compliance signals |
| Resource sensitivity | Data classification metadata or application risk tier |
| Operation requested | Read, write, administer, export |
| Time | Business-hour and after-hour policy variations |
| Geographic location | IP-based; risk-adjusted |
| Prior-session anomalies | Behavioural baseline deviations |

The policy engine produces an allow, allow-with-step-up, monitor, or deny decision. Decisions are logged with the inputs that produced them to support audit and incident investigation.

---

## Migration model

Zero trust is a multi-year journey. The framework adopts a four-stage maturity ladder.

| Stage | Posture |
| --- | --- |
| Stage 0: Traditional | Perimeter-based; trust by network location; standing privileged access |
| Stage 1: Initial | MFA broadly deployed; basic device compliance; segmented production environments |
| Stage 2: Advanced | Conditional access on critical apps; phishing-resistant MFA for privileged access; central SIEM with key use cases; micro-segmentation in highest-criticality workloads |
| Stage 3: Optimal | Continuous evaluation; phishing-resistant MFA universal; just-in-time privileged access; software-defined access replaces VPN for managed paths; AI-aware detection content; policy as code |

The Chief Information Security Officer publishes an annual maturity assessment per pillar; the assessment drives the security architecture roadmap.

---

## Coordination with adjacent domains

| Adjacent | Coordination point |
| --- | --- |
| Identity and access management policy | Identity pillar baseline |
| Authentication and password management standard | Authentication strength requirements |
| Privileged access management standard | Just-in-time and standing access |
| Network communications security policy | Network pillar baseline |
| Network security and segmentation standard | Macro and micro-segmentation |
| Cloud security configuration baseline | Workload and application controls in cloud |
| Endpoint management procedure | Device pillar baseline |
| BYOD policy | Device pillar for unmanaged devices |
| Data classification and handling standard | Data pillar baseline |
| Data loss prevention standard | Data egress controls |
| Logging and monitoring standard | Visibility and analytics pillar |
| AI access and agent permissions standard | AI identity and capability boundary |
| Secure development standards | Application pillar baseline |

---

## Operating expectations

1. Each architecture initiative documents its zero trust impact in the architecture decision record.
2. New cloud, SaaS, or platform onboarding is assessed against the seven pillars during acceptance into service.
3. The Chief Information Security Officer maintains the maturity assessment and the roadmap.
4. Cross-domain coordination (network, identity, endpoint, data, AI) is owned by a designated security architecture function.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST SP 800-207 | Zero Trust Architecture | Authoritative US federal model |
| NIST SP 800-207A | Zero Trust Architecture for Cloud-native and Hybrid Environments | Cloud-native pattern |
| CISA Zero Trust Maturity Model 2.0 | CISA | Maturity ladder |
| OMB M-22-09 | Federal Zero Trust Strategy | US federal direction |
| DoD Zero Trust Reference Architecture | US DoD | Defence-sector model |
| ISO/IEC 27001:2022 | Annex A | Underlying controls |
| ISO/IEC 27036 | Information security for supplier relationships | Supplier integration |
| CSA Software-Defined Perimeter | CSA | Network pillar |
| NIST CSF 2.0 | All functions | Cross-walk |

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. Zero trust maturity is incremental; the framework defines direction and pillars rather than a one-time deployment. Adopting organizations sequence the migration according to their risk appetite, technology landscape, and operational tolerance. The framework is not a product or platform mandate; it is a control-pattern reference.

---

**End of Document**
