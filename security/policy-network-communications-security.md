# Network Communications Security Policy

**Document Title:** Network Communications Security Policy\
**Document Type:** Policy\
**Version:** 1.1.4\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md), [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material network, architecture, or regulatory change\
**Repository Path:** [`security/policy-network-communications-security.md`](policy-network-communications-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This policy defines the technical and procedural controls for securing organisational networks across on-premise, cloud, and hybrid environments.

It establishes requirements for network segmentation, firewall configuration, intrusion detection and prevention, and secure connectivity, ensuring protection of corporate and cloud networks. Sector-specific overlays (for example, BASC for trade and logistics networks) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## Scope

1. Applies to all networks, connections, and communication channels that transmit or store organisational data.
2. Covers:
 - Corporate LAN, WAN, and VPN infrastructure.
 - Cloud and virtualized networks.
 - Wireless, remote, and partner connectivity.
3. Applies to all employees, contractors, and third parties who connect to corporate or third-party certified networks.
4. Encompasses both internal traffic and external connectivity to partners, customers, and authorities.
5. Sector-specific scope extensions (for example, BASC logistics, customs, and cargo networks) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns network security strategy, policy enforcement, and monitoring of networks. |
| **Chief Information Officer (CIO)** | Provides resources and strategic oversight for network infrastructure and architecture. |
| **Network Security Manager** | Implements segmentation, firewall, VPN, and IDS/IPS configurations. |
| **Security Operations Centre (SOC)** | Monitors traffic, alerts, and anomalies using SIEM and AI-assisted analytics. |
| **System and Application Owners** | Validate that network configurations support required data classifications and encryption levels. |
| **Internal Audit** | Performs periodic verification of firewall and segmentation effectiveness across enterprise environments and any sector-programme environments the organisation participates in. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who ensures that BASC-certified networks follow customs-security and cargo-integrity controls) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 1. Network segmentation and architecture

1.1 The network must be segmented into zones based on business function, sensitivity, and regulatory requirements. Sector-programme zones (for example, BASC customs and logistics segments) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

1.2 Segmentation must isolate:
- Corporate systems.
- AI and analytics environments.
- Public-facing services and DMZ.
- Sector-programme systems (where the organisation participates in a covered programme, per the relevant sector annex).

1.3 Inter-zone communication must be restricted and logged, requiring explicit access rules approved by the CISO.

---

## 2. Firewall and perimeter security

2.1 All perimeter gateways must enforce deny-by-default rules and allow only approved, documented traffic.

2.2 Firewalls must support stateful inspection, intrusion prevention, and content filtering.

2.3 Configuration changes must be approved through change-management workflows per the Change Management and Configuration Control Procedure.

2.4 Sector-programme communication channels (for example, customs EDI and customs API gateways where the organisation participates in BASC) must be secured per the relevant sector annex's requirements (typically TLS 1.3 or stronger with validated PKI certificates); see [`compliance/`](../compliance/).

2.5 Firewall configurations for sector-programme operations must include the logging policies stated by the relevant sector annex.

---

## 3. Intrusion detection, prevention, and monitoring

3.1 IDS and IPS systems must monitor all network traffic and integrate with the central SIEM.

3.2 SOC must investigate alerts within 15 minutes for high-severity and 1 hour for medium-severity events.

3.3 Sector-programme networks (for example, BASC logistics and customs networks where the organisation participates in BASC) must have the additional intrusion-detection sensors and retention periods stated by the relevant sector annex; see [`compliance/`](../compliance/).

---

## 4. Secure connectivity and remote access

4.1 All remote connections must use VPN or Zero-Trust Network Access (ZTNA) solutions enforcing device health, MFA, and continuous session validation.

4.2 Direct remote access to networks operating under a sector programme that requires elevated authorisation (for example, BASC trade or customs networks where the organisation participates in BASC) is prohibited unless authorised in writing by the CISO and the sector-conditional role defined by the relevant sector annex; see [`compliance/`](../compliance/).

4.3 Partner and supplier connections must be isolated using virtual network peering, firewalls, or secure APIs.

4.4 Wireless access points within sensitive operational facilities (for example, those covered by a sector programme such as BASC logistics or customs facilities) must use WPA3-Enterprise encryption and maintain logs for all authenticated sessions per the relevant sector annex; see [`compliance/`](../compliance/).

---

## 5. Encryption and data protection

5.1 All network traffic must be encrypted using industry-approved algorithms (TLS 1.3, IPsec AES-256).

5.2 Cryptographic controls must follow the Encryption and Key Management Policy.

5.3 Where the organisation participates in a sector programme that mandates additional cryptographic controls (for example, BASC-approved PKI or WCO SAFE-compliant authority for customs communications), the corresponding sector annex states the additional requirements, key custody, and routing controls; see [`compliance/`](../compliance/).

---

## 6. AI-assisted network defence

6.1 AI analytics must continuously evaluate traffic for anomaly detection, drift patterns, or suspicious behaviour consistent with adversarial AI attacks.

6.2 AI tools must produce explainable results for all autonomous actions and integrate with SOC dashboards.

6.3 AI-driven alerts involving sector-programme networks (for example, BASC trade or customs networks where the organisation participates in BASC) must be labelled according to the sector annex's classification scheme and escalated to the sector-conditional role defined by the annex for verification; see [`compliance/`](../compliance/).

---

## 7. Sector-programme network security overlays

Where the organisation participates in a sector programme that imposes additional network-security controls (for example, BASC and WCO SAFE for trade and logistics networks requiring perimeter monitoring, cargo and seal-tracking telemetry, customs-document integrity verification, and PKI controls for customs communications), the corresponding sector annex defines the additional control requirements, audit cadence, and incident-response timeframes. See [`compliance/`](../compliance/) for the sector annex applicable to the organisation's covered programmes.

---

## 8. Monitoring, testing, and continuous improvement

8.1 The SOC must continuously monitor performance, intrusion alerts, and access logs.

8.2 Penetration tests and vulnerability scans must occur at least annually; sector-programme inspections occur at the cadence stated in the relevant sector annex.

8.3 Quarterly reviews must validate ZTNA configuration effectiveness.

8.4 Lessons learned and audit findings feed into the Continuous Improvement programme and CAPA process.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27033-1:2015 | Network Security Architecture | Network architecture, segmentation, secure connectivity |
| ISO/IEC 27001:2022 | A.8.20 to 21: Network security, network segmentation | Network security policy obligations |
| COBIT 2019 | DSS05: Managed Security Services | Network security governance and service management |
| NIST SP 800-207 | Zero Trust Architecture | ZTNA principles, continuous validation |
| CSA CCM v4.1 | I&S-01: Network Security and Virtualization Controls | Cloud and virtualized network security |
| EU NIS 2 Directive (Directive (EU) 2022/2555) | Critical Network Security Requirements | Critical infrastructure network obligations |

Sector-specific framework alignments (for example, BASC v6 (2022) Section 6, WCO SAFE Framework (2021), and ISO 28000:2022 for trade and customs network security) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

**End of Document**
