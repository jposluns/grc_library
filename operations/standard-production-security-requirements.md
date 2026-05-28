# Production Security Requirements

**Document Title:** Production Security Requirements  
**Document Type:** Standard  
**Version:** 1.1.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md), [`dev-security/standard-security-quick-reference.md`](../dev-security/standard-security-quick-reference.md)  
**Classification:** Public  
**Category:** Operations  
**Review Frequency:** Annual and upon material platform or regulatory change  
**Repository Path:** [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

This standard defines security requirements for production infrastructure and operations. It covers the controls that govern how production systems are secured, monitored, changed, and recovered. For deployment pipeline and DevOps controls, see the DevOps Security Requirements Standard.

---

## 1. Network Security Operations

**VLAN and ACL compliance:** The current infrastructure Low Level Design is the authoritative network baseline. No ACL or firewall changes are permitted without a documented change request reviewed by the network and security teams. All rule changes are logged with business justification, approver, and effective date.

**DNS security:** Internal DNS must have query logging enabled and forwarded to the SIEM.

**TLS certificate management:** Internal services use an internal PKI (two-tier hierarchical CA). External-facing services use an approved external CA — a jurisdiction-appropriate CA is preferred for data residency alignment. Self-signed certificates are prohibited in Production. A certificate inventory must be maintained. Alerts fire at 60 days and 30 days before expiry. Certificate expiry in production is a critical incident.

**Remote access:** All on-premises remote administration must originate from a Privileged Access Workstation (PAW) or approved jump host on the Management VLAN. Direct RDP/SSH from general workstations is prohibited. External vendor access must use the approved path or VPN with MFA, subject to PAM workflow.

**Framework:** CSA CCM I&S-03, I&S-06, I&S-08, I&S-09

---

## 2. Backup and Recovery Operations

**Infrastructure:** Dedicated backup infrastructure with a hardened, immutable repository is required. All production workloads must be covered by active backup jobs. Coverage is audited monthly.

**Targets:** RPO 1 hour. RTO 4 hours baseline. Application-specific targets must be confirmed with application owners and documented.

**Immutability:** The primary backup repository must have immutability enforced. Attempted deletions must be blocked and alerted in the SIEM. An off-site copy must also be immutable. Backup admin identities must not be Domain Admins and must be vaulted in PAM.

**Restore testing:** Automated restore tests must run at minimum weekly. Evidence must be retained. A failed restore test is a P2 incident. The DR runbook must be tested quarterly.

**Framework:** CSA CCM BCR-08, BCR-09, BCR-10

---

## 3. Security Monitoring and Incident Response

### 3.1 SIEM Alert Coverage

The following alert categories must be configured and tested before any system goes to production:

- Failed authentication (brute-force threshold)
- Privileged access outside approved change windows
- Multiple failed PAM login attempts
- Emergency account usage
- PAM bypass
- New admin account creation
- Directory service and trust changes (GPO, FSMO, trust modifications)
- Firewall rule changes
- Backup failure
- Certificate near-expiry (60 and 30 days)
- Endpoint protection alerts
- DNS anomalies

### 3.2 Pre-Go-Live Security Validation

The following must be evidenced before any system promotes to production. These criteria apply to any infrastructure programme or platform deployment regardless of scale.

1. **Trust configuration:** SID filtering confirmed, selective authentication confirmed, Kerberos-first confirmed.
2. **NTLM audit:** No NTLMv1; NTLM fallback restricted.
3. **Tier isolation:** Cross-tier logon attempts denied.
4. **PAM workflow:** Approval, credential injection, rotation, and session recording confirmed.
5. **Network segmentation:** Allow-listed flows succeed; blocked flows verified blocked.
6. **Backup immutability:** Deletion blocked; restore test successful.
7. **SIEM:** Critical event categories visible with correct alert routing.
8. **Break-glass:** Emergency accounts functional; alerts fire on use.

**Framework:** CSA CCM LOG-01 through LOG-14, SEF-01 through SEF-10

### 3.3 Incident Response Obligations

Do not isolate or reimage systems without direction from the incident commander. Evidence preservation takes priority over service recovery in the first hour. Escalate immediately to the CIO and security leadership. The IR partner (where contracted) is notified by the security leadership for P1 incidents — current partner details are maintained in the operational state register. All IR actions must be logged with timestamps.

---

## 4. Patch and Vulnerability Management

| Severity | SLA |
| --- | --- |
| Critical (CVSS 9.0–10.0) | 24 hours if actively exploited; 72 hours if publicly disclosed; 7 days otherwise |
| High (CVSS 7.0–8.9) | 14 days |
| Medium (CVSS 4.0–6.9) | 30 days |
| Low (CVSS 0.1–3.9) | 90 days or next maintenance window |

Authenticated vulnerability scans must run at minimum weekly. Results must be reviewed within 48 hours. Critical findings trigger immediate alert. No EOL OS, middleware, or runtime versions are permitted in production. Upgrade plans must be initiated at minimum 6 months before any EOL date.

**Framework:** CSA CCM TVM-03 through TVM-12

---

## 5. Change Management

| Change Type | Approval | CAB Review |
| --- | --- | --- |
| Standard (pre-approved, low-risk) | Team lead | No |
| Normal | Delegated authority | Yes |
| Emergency | CIO or equivalent | Retrospective within 24 hours |
| High-risk (identity, PAM, PKI, production network) | CIO or CISO | Yes |

All production changes must be executed through the approved IaC pipeline. Direct manual production changes are prohibited except in declared incidents and must be codified within 24 hours. Every CAB-reviewed change must include a tested rollback plan.

**Framework:** CSA CCM CCC-01 through CCC-09

---

## 6. Infrastructure Programme Security Gate Requirements

Any infrastructure programme delivering or replacing production infrastructure must produce evidence against the following security acceptance criteria at defined phase gates before proceeding to the next phase.

| Phase | Description | Security Acceptance Criteria |
| --- | --- | --- |
| Mobilisation | Access and governance established | Access controls confirmed; security responsibilities assigned; governance documentation in place |
| Core platform | Compute, storage, and network baseline operational | Hypervisor or compute cluster operational; storage redundancy confirmed; VLANs and ACL baseline applied; PAW/jump host paths operational |
| Identity baseline | Directory and authentication services live | Directory services live; GPOs applied; LDAP signing enforced; admin tier separation verified; MFA enforced at all access points |
| Application readiness | Application platforms and data tiers in place | Database and application tiers deployed; backup hooks active; audit logging confirmed; database audit logging enabled |
| Security baseline sign-off | GO/NO-GO gate before production | All items in §3.2 evidenced; segmentation validated; SIEM ingestion confirmed; PAM workflow validated; backup immutability validated; break-glass accounts tested |
| Production go-live | Production cutover | UAT signed off; change window approved; rollback plan confirmed |

---

## 7. Documentation Requirements

The following must be maintained as living artefacts:

- Network architecture diagram (updated within 30 days of any change)
- VLAN and subnet register
- ACL and firewall rule register with business justification
- Server and VM inventory with OS version, patch level, and endpoint protection coverage status
- Certificate inventory with expiry dates
- Backup coverage register
- PAM account register
- SIEM alert rule register
- DR runbook with last tested date

---

## 8. Cloud Security Configuration

**Subscription and tenant governance:** All cloud subscriptions must be under the enterprise identity provider tenant. Cloud policy enforces mandatory configurations including encryption, tagging, allowed regions, and network restrictions. Resource locks must be applied to critical production infrastructure.

**Conditional Access:** All Conditional Access policies are defined and enforced centrally by the enterprise identity platform. Application and infrastructure teams must not design around Conditional Access.

**RBAC:** Custom roles are preferred over built-in where built-in roles grant excess permissions. Owner/Contributor at subscription level must be minimised. All assignments should use Privileged Identity Management (PIM) eligible assignments where possible. A quarterly review is mandatory.

**Secrets management:** Every application has its own secrets vault. No cross-application sharing for Confidential or Restricted secrets. Soft delete and purge protection must be enabled. Diagnostic logs must be forwarded to the SIEM. Firewall rules must restrict network access.

**Endpoint protection and SIEM:** Enterprise endpoint protection must be deployed on all servers. Hybrid server management is required for all on-premises servers enrolled in cloud management. All endpoint protection alerts must be forwarded to the SIEM. SIEM workspace deletion is restricted to break-glass roles.

**Framework:** CSA CCM I&S-01 through I&S-09, LOG-01 through LOG-14

---

## 9. On-Premises Middleware Security

This section applies to all on-premises middleware platforms — message brokers, integration servers, EDI platforms, and equivalent — regardless of vendor or product.

### Service Account Isolation

Each functional role within a middleware platform must use a dedicated, purpose-specific service account. No single service account may span multiple functional roles (inbound processing, outbound delivery, orchestration, tracking, and administrative functions must each have their own account). All middleware service account credentials must be stored in the PAM vault and subject to the standard rotation schedule.

### Database Access

Middleware platforms that use dedicated databases for message routing, configuration, tracking, and business activity data must enforce least-privilege database access per component. Runtime processing accounts must not hold administrative database permissions. Administrative accounts for middleware configuration databases must be separate from runtime service accounts. Database authentication must use Windows Authentication (Kerberos) or Managed Identity where supported. Username/password database authentication for middleware service accounts is prohibited.

### Inbound Adapter Security

All receive locations or inbound adapters serving external or non-internal sources must enforce authentication. Anonymous inbound connections from external sources are prohibited. File transfer receive adapters must use SFTP or explicit FTPS. HTTP/SOAP adapters must enforce TLS 1.2 minimum. TLS 1.0 and 1.1 must be disabled at the OS level.

### Partner and Certificate Management

Third-party integration certificates (AS2, SFTP, TLS mutual auth) must have a documented renewal process initiated at minimum 60 days before expiry. SIEM alerts must fire at 60 and 30 days before expiry. Certificates must be stored in the approved certificate or PAM vault, not hardcoded in application configuration.

### Administrative Access

Middleware management consoles and administrative interfaces must be restricted to named administrators, accessed from PAW or jump host only. Administrative group membership must be reviewed quarterly. Direct access from general workstations is prohibited.

### Monitoring and Observability

All middleware servers must be enrolled in endpoint protection tooling and onboarded to cloud-based hybrid server management. Event logs must be forwarded to the SIEM. Health, activity, and tracking databases must be monitored for anomalous patterns.

### Migration to Cloud Integration Platforms

When migrating from on-premises middleware to cloud integration platforms:

- All migrated workflows must comply with developer security requirements from day one; no legacy credential patterns carry over.
- Partner certificates and agreements must be migrated to the approved cloud certificate and integration store.
- Parallel operation of on-premises and cloud paths during transition must have a documented cutover date and rollback plan — indefinite parallel operation is not permitted.

---

## 10. EOL — Production Obligations

The EOL classification policy and remediation SLAs are defined in the Security Baseline Standard. Production and infrastructure obligations:

- The infrastructure lead maintains the runtime EOL tracking register for all on-premises and production systems, reviewed at each quarterly security review.
- SIEM analytics rules must fire at 180 days, 90 days, and 30 days before any runtime reaches EOL.
- For on-premises systems (database servers, OS, middleware): upgrade plans must be initiated by Class 3 (180 days before EOL). Systems at Class 1 must be on emergency remediation with monthly status reported to the CIO.
- No EOL OS, middleware, or database versions are permitted in production without a documented CIO-approved exception and compensating controls.

---

## Framework Alignment

| Control Area | ISO 27001:2022 | CSA CCM v4 | NIST SP 800-53 | NIST SSDF |
| --- | --- | --- | --- | --- |
| Network security | A.8.20–8.23 | I&S-01–09 | SC-7, SC-8 | — |
| Backup and recovery | A.8.13–8.14 | BCR-08–10 | CP-9, CP-10 | — |
| Monitoring and incident response | A.8.15–8.16, A.5.24–5.28 | LOG-01–14, SEF-01–10 | IR-1–8, SI-4 | RV.1 |
| Vulnerability management | A.8.8 | TVM-03–12 | RA-5, SI-2 | PO.5 |
| Change management | A.8.32 | CCC-01–09 | CM-3, CM-5 | — |
| Certificate management | A.8.24 | CEK-01–21 | SC-12, SC-17 | — |
| Access control | A.5.15–5.18 | IAM-01–14 | AC-2, AC-6 | PW.6 |
| EOL and lifecycle | A.8.8 | TVM-01–02 | SA-22 | PO.5 |



**End of Document**
