# Network Security and Segmentation Standard

**Document Title:** Network Security and Segmentation Standard 
**Document Type:** Standard 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material platform or regulatory change 
**Repository Path:** [`operations/standard-network-security-and-segmentation.md`](standard-network-security-and-segmentation.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## 1. Purpose

This standard defines requirements for network security architecture, segmentation, and perimeter controls across on-premises and cloud environments. It establishes technical and procedural controls for securing organisational networks, including requirements for network segmentation, firewall configuration, intrusion detection and prevention, and secure connectivity.

Network design must limit blast radius and systematically close lateral movement pathways identified during a prior ransomware incident. Requirements cover corporate, cloud, hybrid, and BASC-certified logistics and customs network environments.

---

## 2. Scope

1. Applies to all networks, connections, and communication channels transmitting or storing organisational or trade data, including all on-premises networks, cloud virtual networks, and all interconnected environments.
2. Covers BASC-certified logistics and customs systems in Latin America (Colombia, Mexico, Peru, Chile); corporate LAN, WAN, and VPN; cloud and virtualized networks; wireless, remote, and partner connectivity.
3. Covers network zone design, segmentation requirements, firewall policy, remote access, wireless, and inter-zone traffic controls.
4. Applies to all employees, contractors, and third parties who connect to corporate or third-party certified networks.
5. Applies to the infrastructure programme from initial design. All new network architecture must conform before production deployment.

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
| BASC / Logistics | BASC-certified logistics, cargo, and customs systems | Isolated from non-certified environments; inter-zone access requires CISO and Regional BASC Officer authorization |

### 4.1 Key segmentation requirements

- Non-production environments must be air-gapped from PROD. No direct network path between TEST/DEV and PROD is permitted without a change-controlled deployment process. This control directly addresses lateral movement pathways exploited during a prior ransomware incident.
- Domain controllers must reside in a dedicated protected subnet. Inbound access is restricted to domain-joined systems on approved management protocols (LDAP/S, Kerberos, DNS).
- RDP and SSH access to servers must originate from the Management zone or a designated jump host. Direct inbound RDP from user endpoints to production servers is prohibited.
- All outbound internet traffic from servers must route through a proxy or firewall with application-layer inspection.
- BASC trade and customs networks must operate under validated segmentation architectures ensuring physical or logical isolation from non-certified environments, in accordance with BASC International Standard Section 6.

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

### 5.3 BASC customs communications

- BASC customs communication channels (e.g., EDI, customs API gateways) must be secured with TLS 1.3 or stronger and validated PKI certificates.
- Firewall configurations for BASC-certified operations must include customs and cargo logging policies meeting BASC Section 6 documentation controls.

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

### 7.2 BASC logistics and customs networks

- BASC logistics and customs networks must have dedicated intrusion-detection sensors monitoring for:
 - Unauthorized customs system access
 - Cargo manifest tampering
 - Unauthorized network segmentation bypass
- All BASC intrusion logs must be retained for at least seven years in tamper-evident archives.

### 7.3 AI-assisted network defence

- AI analytics tools may be deployed to continuously evaluate traffic for anomaly detection, drift patterns, or behaviour consistent with adversarial attacks.
- AI tools must produce explainable results for all autonomous actions and must integrate with SOC dashboards.
- AI-driven alerts involving trade or customs networks must be labelled as BASC Security Events and escalated to Regional BASC Officers.

---

## 8. Remote access and secure connectivity

### 8.1 Remote access

- VPN or Zero-Trust Network Access (ZTNA) solutions are the approved mechanisms for remote access to on-premises and sensitive resources. Solutions must enforce device health checks, MFA, and continuous session validation.
- VPN authentication requires enterprise identity provider MFA.
- Split tunnelling: traffic to internal resources must route through VPN.
- Direct internet breakout for cloud productivity platform traffic is permitted for performance optimization.
- RDP and SSH to production systems via the public internet without VPN is prohibited.
- Direct remote access to BASC trade or customs networks is prohibited unless authorized in writing by the CISO and the relevant Regional BASC Officer.

### 8.2 Partner and supplier connectivity

- Partner and supplier connections must be isolated using virtual network peering, firewalls, or secure APIs.
- Partner connections must be reviewed at least annually and terminated when the business relationship ends.

### 8.3 Wireless access

- Wireless access points within logistics or customs facilities must use WPA3-Enterprise encryption and must maintain logs for all authenticated sessions.

---

## 9. Encryption and data protection

- All network traffic must be encrypted using industry-approved algorithms (TLS 1.3, IPsec AES-256).
- Encryption keys for BASC customs communications must be issued and managed under BASC-approved PKI or WCO SAFE-compliant authority.
- Data packets containing customs or cargo information must be classified as Restricted and routed through secure tunnels monitored by the SOC.
- Cryptographic controls must follow the Encryption and Key Management Policy.

---

## 10. BASC trade-network security controls

### 10.1 Facility and network controls

BASC-certified facilities and logistics networks must implement:

- Perimeter monitoring (CCTV integrated with IDS)
- Cargo and seal-tracking telemetry with audit trails
- Customs-document integrity verification through checksum or equivalent integrity validation

### 10.2 Compliance audits

BASC Section 6 compliance audits must verify:

- Log completeness and retention for customs systems
- Encryption and PKI validation for customs communications
- Physical access control to networking and logistics hubs

### 10.3 Incident response

Any detected BASC trade-network anomaly must trigger the Security Incident Response Procedure within 2 hours of discovery.

---

## 11. Monitoring, testing, and continuous improvement

- The SOC must continuously monitor network performance, intrusion alerts, and access logs.
- Penetration tests, vulnerability scans, and BASC trade-network inspections must occur at least annually.
- Quarterly reviews must validate ZTNA configuration effectiveness.
- Lessons learned and audit findings must be recorded in the risk register and fed into the continual improvement cycle.

---

## 12. Framework alignment

| Framework | Reference |
|---|---|
| ISO/IEC 27001:2022 | A.8.20, A.8.21, A.8.22: Network Controls |
| ISO/IEC 27033:2020 | Network Security Architecture and Segmentation |
| NIST SP 800-53 | SC-7: Boundary Protection |
| NIST SP 800-207 | Zero Trust Architecture |
| COBIT 2019 | DSS05: Manage Security Services |
| CSA CCM v4.1 | IVS-06, IVS-07: Network Architecture and Segmentation |
| CIS Controls v8 | Control 12: Network Infrastructure Management |
| BASC International Standard (v6 2023) | Trade and Customs Network Security |
| WCO SAFE Framework (2021) | Supply Chain Security |
| ISO 28000:2022 | Security Management for the Supply Chain |
| EU NIS 2 Directive (2023) | Network and Information Systems Security |

---

*This document is released under the CC0 1.0 Universal Public Domain Dedication. To the extent possible under law, all copyright and related rights are waived.*



**End of Document**
