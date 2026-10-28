# Network Security and Segmentation Standard

**Document Title:** Network Security and Segmentation Standard\
**Document Type:** Standard\
**Version:** 1.4.21\
**Date:** 2026-10-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md), [`compliance/public-sector/annex-canada-public-sector-requirements.md`](../compliance/public-sector/annex-canada-public-sector-requirements.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-network-security-and-segmentation.md`](standard-network-security-and-segmentation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines requirements for network security architecture, segmentation, and perimeter controls across on-premises and cloud environments. It establishes technical and procedural controls for securing organizational networks, including requirements for network segmentation, firewall configuration, intrusion detection and prevention, and secure connectivity.

Network design must limit blast radius and systematically close lateral movement pathways commonly exploited in major security incidents. Requirements cover corporate, cloud, and hybrid network environments. Sector-specific overlays apply per [`compliance/`](../compliance/).

---

## 2. Scope

1. Applies to all networks, connections, and communication channels transmitting or storing organizational data, including all on-premises networks, cloud virtual networks, and all interconnected environments.
2. Covers corporate LAN, WAN, and VPN; cloud and virtualized networks; wireless, remote, and partner connectivity.
3. Covers network zone design, segmentation requirements, firewall policy, remote access, wireless, and inter-zone traffic controls.
4. Applies to all employees, contractors, and third parties who connect to corporate or third-party certified networks.
5. Applies to the infrastructure programme from initial design. All new network architecture must conform before production deployment.

Sector-specific overlays (for example, BASC for trade and logistics operations) apply where the organization participates in a programme covered by a sector annex; see [`compliance/`](../compliance/).

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

Sector-specific zone overlays (for example, dedicated zones for trade, customs, or operational technology systems) apply where the organization participates in a sector programme that requires them; see [`compliance/`](../compliance/) for sector-specific zone requirements.

### 4.1 Key segmentation requirements

- Non-production environments must be segregated from PROD, using physically separate networks or separate logical networks. The only permitted network path between TEST/DEV and PROD is a change-controlled deployment process. This control prevents lateral movement, a common attack progression in major security incidents.
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
- Emergency rule additions follow the emergency change process in [`procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md) section 4; a firewall rule change is High-risk, so its permanent follow-up carries joint CISO and CIO approval.

### 5.3 Sector-specific channel overlays

Where the organization participates in a sector programme that requires specific channel hardening for inter-organization data exchange (for example, customs API gateways, healthcare data exchange, financial-services messaging), the corresponding sector annex states the additional requirements. See [`compliance/`](../compliance/).

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
- The SOC must investigate alerts on the severity-tiered service levels defined in the [Security Monitoring and Alert Management Procedure](procedure-security-monitoring-and-alert-management.md): critical within 15 minutes, high within 1 hour, and medium by the same business day.

### 7.2 Sector-specific intrusion detection overlays

Sector programmes may require additional intrusion-detection coverage with specific signatures, retention periods, and alert-escalation paths. See [`compliance/`](../compliance/) for sector-specific overlays where the organization participates in a covered programme.

### 7.3 AI-assisted network defence

- AI analytics tools may be deployed to continuously evaluate traffic for anomaly detection, drift patterns, or behaviour consistent with adversarial attacks.
- AI tools must produce explainable results for all autonomous actions and must integrate with SOC dashboards.
- AI-driven alerts within sector-specific networks (where the organization participates in a covered programme) must be labelled according to the relevant sector annex's classification and escalated per the annex's escalation path.

---

## 8. Remote access and secure connectivity

### 8.1 Remote access

- VPN or Zero-Trust Network Access (ZTNA) solutions are the approved mechanisms for remote access to on-premises and sensitive resources. Solutions must enforce device health checks, MFA, and continuous session validation.
- VPN authentication requires enterprise identity provider MFA.
- Split tunnelling: traffic to internal resources must route through VPN.
- Direct internet breakout for cloud productivity platform traffic is permitted for performance optimization.
- RDP and SSH to production systems via the public internet without VPN is prohibited.
- Direct remote access to networks operating under a sector programme that requires elevated authorization (for example, customs, trade, or operational-technology networks) is prohibited unless authorized in writing by the CISO and the role designated by the relevant sector annex.

### 8.2 Partner and supplier connectivity

- Partner and supplier connections must be isolated using virtual network peering, firewalls, or secure APIs.
- Partner connections must be reviewed at least annually and terminated when the business relationship ends.

### 8.3 Wireless access

- Wireless access points within sensitive operational facilities (for example, those covered by a sector programme) must use WPA3-Enterprise encryption and must maintain logs for all authenticated sessions per the relevant sector annex.

---

## 9. Encryption and data protection

- All network traffic must be encrypted using industry-approved algorithms (TLS 1.3, IPsec AES-256).
- Cryptographic controls must follow the Encryption and Key Management Policy.

Where the organization participates in a sector programme that mandates additional cryptographic controls (for example, customs-data PKI, healthcare-data exchange), the corresponding sector annex states the additional requirements.

---

## 10. Monitoring, testing, and continuous improvement

- The SOC must continuously monitor network performance, intrusion alerts, and access logs.
- Penetration tests and vulnerability scans must occur at least annually.
- Quarterly reviews must validate ZTNA configuration effectiveness.
- Lessons learned and audit findings must be recorded in the risk register and fed into the continual improvement cycle.

Sector-specific testing or inspection cadences (for example, sector-mandated trade-security audits) apply where the organization participates in a covered programme; see [`compliance/`](../compliance/).

---

## 11. Framework alignment



| Framework | Reference |
|---|---|
| ISO/IEC 27001:2022 | A.8.20, A.8.21, A.8.22: Network Controls |
| ISO/IEC 27033-1:2015 | Overview and concepts |
| NIST SP 800-53 Rev. 5 | SC-7: Boundary Protection |
| NIST SP 800-207 | Zero Trust Architecture |
| NIST SP 800-41 Rev. 1 | Guidelines on Firewalls and Firewall Policy |
| NIST SP 800-94 | Guide to Intrusion Detection and Prevention Systems (IDPS) |
| COBIT 2019 | DSS05: Managed Security Services |
| CSA CCM v4.1 | I&S-03, I&S-08, I&S-09: Network Security, Architecture, and Defense |
| CIS Controls v8.1 | Control 12: Network Infrastructure Management |
| EU NIS 2 Directive (Directive (EU) 2022/2555) | Network and Information Systems Security |
| CCCS ITSP.80.022, Baseline Security Requirements for Network Security Zones (version 2.0, effective 12 January 2021, per the held text) | §2.1, §2.2, §2.3, §3.2.1, §4.2.1, §4.3: Network security zone types, zone interface points, zone authority, and functional reference model |
| CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2 | BC.9.1 to BC.9.8: Establish basic perimeter defences |
| TBS Directive on Security Management, Appendix B | B.2.3.6.1 to B.2.3.6.3: System and communications protection |

**Canadian network-zone sources.** The three Canadian rows above are paraphrased from the held texts, with pinpoints. Each row cites the held edition; its currency is to be confirmed upstream before an adopter relies on it. ITSP.80.022 is written for IT solutions at the Unclassified, Protected A, and Protected B levels (its Overview); the Directive on Security Management applies to the organizations listed in section 6.1 of the Policy on Government Security (Directive 6.1) and takes effect on 1 July 2019 per the held text; the small and medium organizations baseline is a CCCS publication for small and medium organizations. The public-sector applicability model is in the [Canada Public Sector GRC Requirements Annex](../compliance/public-sector/annex-canada-public-sector-requirements.md); a mapping row here does not establish implementation or compliance.

- **Zone types (ITSP.80.022 §2.1).** ITSP.80.022 defines seven zone types: public, public access, operations, restricted, highly restricted, restricted extranet, and management. The section 4 zone model is the organization's own. Read against the §2.1 descriptions, Internet / Untrusted is closest to the public zone (§2.1.1), DMZ to the public access zone (§2.1.2), User (Corporate) to the operations zone (§2.1.3), Production to the restricted zone (§2.1.4), and Management to the management zone (§2.1.7). This correspondence is an inference, not a statement in the source, and ITSP.80.022 has no separate test and development zone type.
- **Zone interface points (ITSP.80.022 §2.2).** All data communication between zones "must be through" a zone interface point that connects only those two zones by a unique path. This supports the default-deny inter-zone rule in section 4 and the perimeter rules in section 5.1.
- **Zone authority (§2.3).** Each zone has an assigned network security zone authority accountable for its security requirements and practices; the held text says each zone "should have" its own authority and that one authority "may be responsible" for several zones. Section 3 of this standard gives the CISO approval of zone boundary decisions and inter-zone rules.
- **Shared end systems (ITSP.80.022 §4.2.1).** Shared end systems "must be configured and secured" so that they cannot route traffic between the zones they connect to, which supports the segmentation rules in section 4.1.
- **Principles and requirement structure (§3.2.1, §4.3).** Zones rest on discrete entry and exit points, traffic filtering and monitoring at those points, and authentication of network entities (§3.2.1). The per-zone baselines are organized into five requirement components: network interface, traffic control, network configuration, host configuration, and data protection (§4.3). The held extract ends at its References section and does not contain Annexes A to F, which carry the per-zone and zone-interface-point baseline requirements, so this standard maps to the body of ITSP.80.022 only.
- **Small and medium organizations baseline (§3.9).** Every BC.9 control uses "should": dedicated firewalls at the Internet boundary, with Internet-facing servers isolated (BC.9.1); a DNS firewall for outbound requests (BC.9.2); VPN with two-factor authentication for all remote access (BC.9.3); secure Wi-Fi, "preferably WPA2-Enterprise" (BC.9.4); public Wi-Fi that organizations "should never connect" to corporate networks (BC.9.5); firewall isolation of point-of-sale systems (BC.9.6); DMARC (BC.9.7); and email filtering at ingress and egress (BC.9.8). Sections 5.1, 8.1, and 8.3 correspond to BC.9.1, BC.9.3, and BC.9.4; section 8.3 requires WPA3-Enterprise in sensitive operational facilities, a stronger setting than the BC.9.4 preference. DNS security sits in the Networks pillar of the [Zero Trust Architecture Framework](../security/framework-zero-trust-architecture.md), and DMARC in section 5.1 of the [Cloud Security Configuration Baseline](standard-cloud-security-configuration-baseline.md).
- **Directive on Security Management, Appendix B.** Appendix B sets out mandatory procedures, written as imperatives without a modal verb. B.2.3.6.1 directs the definition and establishment of security zones that keep separation within physical and virtual IT environments, with protection commensurate with the threat, the sensitivity of the information, and the criticality of the services supported; B.2.3.6.2 restricts discrete external connections to departmental networks to the minimum necessary; and B.2.3.6.3 directs the use of encryption and network safeguards to protect the confidentiality of sensitive data sent across public, wireless, or other at-risk networks. These correspond to sections 4, 5, 8.2, and 9 of this standard.

Sector-specific framework alignments (for example, the applicable BASC International Security Standard (6.0.2 or 6.0.3) for trade and customs network security; WCO SAFE Framework for supply chain security; ISO 28000:2022 for supply chain security management) apply where the organization participates in a covered programme; see [`compliance/`](../compliance/).

ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating an ISO 28000 attribution here as verified. <!-- ref-absence: ISO 28000:2022 -->

---

*This document is released under the CC BY-SA 4.0 licence.*



**End of Document**
