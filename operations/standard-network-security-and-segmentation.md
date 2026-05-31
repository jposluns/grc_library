# Network Security and Segmentation Standard

**Document Title:** Network Security and Segmentation Standard\
**Document Type:** Standard\
**Version:** 1.4.0\
**Date:** 2026-05-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-network-security-and-segmentation.md`](standard-network-security-and-segmentation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines requirements for network security architecture, segmentation, and perimeter controls across on-premises and cloud environments. It establishes technical and procedural controls for securing organisational networks, including requirements for network segmentation, firewall configuration, intrusion detection and prevention, and secure connectivity.

Network design must limit blast radius and systematically close lateral movement pathways commonly exploited in major security incidents. Requirements cover corporate, cloud, and hybrid network environments. Sector-specific overlays apply per [`compliance/`](../compliance/).

---

## 2. Scope

1. Applies to all networks, connections, and communication channels transmitting or storing organisational data, including all on-premises networks, cloud virtual networks, and all interconnected environments.
2. Covers corporate LAN, WAN, and VPN; cloud and virtualised networks; wireless, remote, and partner connectivity.
3. Covers network zone design, segmentation requirements, firewall policy, remote access, wireless, and inter-zone traffic controls.
4. Applies to all employees, contractors, and third parties who connect to corporate or third-party certified networks.
5. Applies to the infrastructure programme from initial design. All new network architecture must conform before production deployment.

Sector-specific overlays (for example, BASC for trade and logistics operations) apply where the organisation participates in a programme covered by a sector annex; see [`compliance/`](../compliance/).

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Information Security Officer (CISO) | Owns this standard; approves network architecture changes, zone boundary decisions, and all inter-zone access rules. |
| IT Operations / Network Team | Implements and maintains network segmentation; manages firewall rule sets; validates zone compliance. |
| Infrastructure Programme Team | Designs new network architecture in accordance with this standard. |
| Security Operations Centre (SOC) | Continuously monitors network traffic, intrusion alerts, and access logs; investigates security events per defined SLAs. |
| Internal Audit | Reviews network segmentation compliance and firewall rule base at least annually. |

---

## 4. Network zone model

All zone boundaries operate on a **default-deny** basis. Inter-zone communication requires explicit approved rules.

| Zone | Description | Permitted Inbound |
|---|---|---|
| Internet / Untrusted | External internet and untrusted networks | To DMZ only; no direct access to internal zones |
| DMZ | Internet-facing services (web, API, VPN concentrators) | Internet to published services; internal to DMZ management only |
| Production (PROD) | Core production servers, databases, ERP, integration layer | From internal user zone via authorized protocols; from DMZ only via explicit rules |
| Management | Network management, monitoring, backup infrastructure | From privileged admin workstations only; PAM-controlled |
| Test / Dev (TEST / DEV) | Non-production environments | No inbound from PROD; no outbound to PROD except via approved change-controlled deployment paths |
| User (Corporate) | End-user endpoints | Access to approved services in PROD and internet via proxy |

Sector-specific zone overlays (for example, dedicated zones for trade, customs, or operational technology systems) apply where the organisation participates in a sector programme that requires them; see [`compliance/`](../compliance/) for sector-specific zone requirements.

### 4.1 Key segmentation requirements

- Non-production environments must be air-gapped from PROD. No direct network path between TEST/DEV and PROD is permitted without a change-controlled deployment process. This control prevents lateral movement, a common attack progression in major security incidents.
- Domain controllers must reside in a dedicated protected subnet. Inbound access is restricted to domain-joined systems on approved management protocols (LDAP/S, Kerberos, DNS).
- RDP and SSH access to servers must originate from the Management zone or a designated jump host. Direct inbound RDP from user endpoints to production servers is prohibited.
- All outbound internet traffic from servers must route through a proxy or firewall with application-layer inspection.

---

## 5. Firewall and perimeter security

### 5.1 General requirements

- All perimeter gateways must enforce deny-by-default rules and allow only approved, documented traffic.
- Firewalls must support stateful inspection, intrusion prevention, and content filtering.
- Configuration changes must be approved through change-management workflows.

### 5.2 Rule management

- All firewall rules must have a documented business justification, named owner, and scheduled review date.
- Rules are reviewed at least annually. Any rule without a current owner or justification must be disabled pending review.
- Emergency rule additions require CISO notification within 24 hours and a formal change ticket within 5 business days.

### 5.3 Sector-specific channel overlays

Where the organisation participates in a sector programme that requires specific channel hardening for inter-organisation data exchange (for example, customs API gateways, healthcare data exchange, financial-services messaging), the corresponding sector annex states the additional requirements. See [`compliance/`](../compliance/).

---

## 6. Cloud network security

- Network security groups (NSGs) must be applied at the subnet level on all cloud virtual networks.
- A cloud firewall or equivalent web application firewall (WAF) must be deployed for all internet-facing workloads.
- Private endpoints must be used for cloud PaaS services (storage, secrets management service, databases) wherever technically available.
- Virtual network peering between production and non-production subscriptions is prohibited.

---

## 7. Intrusion detection, prevention, and monitoring

### 7.1 General IDS/IPS requirements

- IDS and IPS systems must monitor all network traffic and integrate with the central SIEM.
- The SOC must investigate alerts within 15 minutes for high-severity events and within 1 hour for medium-severity events.

### 7.2 Sector-specific intrusion detection overlays

Sector programmes may require additional intrusion-detection coverage with specific signatures, retention periods, and alert-escalation paths. See [`compliance/`](../compliance/) for sector-specific overlays where the organisation participates in a covered programme.

### 7.3 AI-assisted network defence

- AI analytics tools may be deployed to continuously evaluate traffic for anomaly detection, drift patterns, or behaviour consistent with adversarial attacks.
- AI tools must produce explainable results for all autonomous actions and must integrate with SOC dashboards.
- AI-driven alerts within sector-specific networks (where the organisation participates in a covered programme) must be labelled according to the relevant sector annex's classification and escalated per the annex's escalation path.

---

## 8. Remote access and secure connectivity

### 8.1 Remote access

- VPN or Zero-Trust Network Access (ZTNA) solutions are the approved mechanisms for remote access to on-premises and sensitive resources. Solutions must enforce device health checks, MFA, and continuous session validation.
- VPN authentication requires enterprise identity provider MFA.
- Split tunnelling: traffic to internal resources must route through VPN.
- Direct internet breakout for cloud productivity platform traffic is permitted for performance optimization.
- RDP and SSH to production systems via the public internet without VPN is prohibited.
- Direct remote access to networks operating under a sector programme that requires elevated authorisation (for example, customs, trade, or operational-technology networks) is prohibited unless authorised in writing by the CISO and the role designated by the relevant sector annex.

### 8.2 Partner and supplier connectivity

- Partner and supplier connections must be isolated using virtual network peering, firewalls, or secure APIs.
- Partner connections must be reviewed at least annually and terminated when the business relationship ends.

### 8.3 Wireless access

- Wireless access points within sensitive operational facilities (for example, those covered by a sector programme) must use WPA3-Enterprise encryption and must maintain logs for all authenticated sessions per the relevant sector annex.

---

## 9. Encryption and data protection

- All network traffic must be encrypted using industry-approved algorithms (TLS 1.3, IPsec AES-256).
- Cryptographic controls must follow the Encryption and Key Management Policy.

Where the organisation participates in a sector programme that mandates additional cryptographic controls (for example, customs-data PKI, healthcare-data exchange), the corresponding sector annex states the additional requirements.

---

## 10. Monitoring, testing, and continuous improvement

- The SOC must continuously monitor network performance, intrusion alerts, and access logs.
- Penetration tests and vulnerability scans must occur at least annually.
- Quarterly reviews must validate ZTNA configuration effectiveness.
- Lessons learned and audit findings must be recorded in the risk register and fed into the continual improvement cycle.

Sector-specific testing or inspection cadences (for example, sector-mandated trade-security audits) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).

---

## 11. Framework alignment



| Framework | Reference |
|---|---|
| ISO/IEC 27001:2022 | A.8.20, A.8.21, A.8.22: Network Controls |
| ISO/IEC 27033:2020 | Network Security Architecture and Segmentation |
| NIST SP 800-53 | SC-7: Boundary Protection |
| NIST SP 800-207 | Zero Trust Architecture |
| COBIT 2019 | DSS05: Manage Security Services |
| CSA CCM v4.1 | IVS-06, IVS-07: Network Architecture and Segmentation |
| CIS Controls v8 | Control 12: Network Infrastructure Management |
| EU NIS 2 Directive (Directive (EU) 2022/2555) | Network and Information Systems Security |

Sector-specific framework alignments (for example, BASC International Standard v6 2023 for trade and customs network security; WCO SAFE Framework for supply chain security; ISO 28000:2022 for supply chain security management) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).

---

*This document is released under the CC BY-SA 4.0 licence. To the extent possible under law, all copyright and related rights are waived.*



**End of Document**
