# Certificate Authority Management Standard

**Document Title:** Certificate Authority Management Standard\
**Document Type:** Standard\
**Version:** 1.3.3\
**Date:** 2026-06-20\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md), [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-certificate-authority-management.md`](standard-certificate-authority-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

Defines requirements for establishing, operating, and maintaining the internal Certificate Authority (CA) infrastructure. Governs certificate issuance policy, CA hierarchy design, use-case scope, and the boundary between the internal CA and externally trusted commercial CAs. Supplements the Cryptographic Key Operations Procedure, which addresses day-to-day certificate lifecycle operations.

---

## 2. Scope

1. Applies to all certificate issuance by the internal CA infrastructure.
2. Covers four primary use cases: inter-server TLS (machine authentication); S/MIME email signing and encryption; code signing for internal use; client authentication (user and device certificates).
3. Applies to all IT Operations personnel and any third party operating CA components on behalf of the organisation.
4. Applies to all environments: DEV, TEST, and PROD. Separate issuing CAs are used per environment tier for production workloads; the root CA is shared.

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Information Security Officer (CISO) | Owns this standard; approves CA hierarchy design, certificate policy exceptions, and changes to the trust boundary between the internal CA and commercial CAs. |
| IT Operations / Security Engineering | Operates the CA infrastructure; manages issuing CA configuration in the endpoint management platform; processes certificate requests; maintains CA audit logs. |
| Identity / PKI Administrator | Configures and maintains the cloud-based PKI service in the endpoint management admin console; manages SCEP profiles and certificate templates; holds the CA creation permission in the enterprise identity provider. |
| Internal Audit | Reviews CA audit logs, certificate inventory, and issuance policy compliance annually. |

---

## 4. CA platform

The internal CA is implemented using a cloud-based PKI service, an endpoint management platform suite feature administered through the endpoint management admin console. This provides a fully cloud-hosted Root CA and Issuing CA hierarchy with no on-premises NDES servers, AD CS infrastructure, or hardware CA appliances required. The built-in SCEP service acts as the certificate registration authority for managed devices.

The cloud-based PKI service integrates natively with the enterprise identity provider and endpoint management platform, making it the appropriate choice for an endpoint management platform-first environment. A Bring Your Own CA (BYOCA) option is available if future requirements necessitate chaining to an existing on-premises root; this is not required at initial implementation.

**Licence requirement:** The cloud-based PKI service is an endpoint management platform suite add-on feature. Confirm that endpoint management platform suite licences are in place before provisioning CA infrastructure.

---

## 5. CA hierarchy design

### 5.1 Root CA

A single internal Root CA is created. The Root CA acts as the trust anchor for all internal certificates. It does not directly issue end-entity certificates; it issues only to Issuing CAs. The Root CA certificate must be distributed to all managed devices and domain-joined systems via trusted certificate profiles and Group Policy respectively.

### 5.2 Issuing cas

The cloud-based PKI service does not support the "Any Purpose" Extended Key Usage (EKU). Each Issuing CA must be scoped to a specific EKU set. The organisation therefore operates separate Issuing CAs for each primary use case. This provides issuance policy separation and limits blast radius if an Issuing CA is compromised.

| Issuing CA | EKU | Purpose | Recipients |
|---|---|---|---|
| TLS / Server Authentication CA | Server Authentication (1.3.6.1.5.5.7.3.1) | TLS certificates for inter-server communication, internal APIs, and internal web services. | Servers, VMs, internal services. |
| S/MIME CA | Secure Email (1.3.6.1.5.5.7.3.4) | S/MIME email signing and encryption for email client users. | End users on managed devices. |
| Code Signing CA | Code Signing (1.3.6.1.5.5.7.3.3) | Signing of internal scripts, automation, and software not distributed outside the organisation. | Development and operations personnel. |
| Client Authentication CA | Client Authentication (1.3.6.1.5.5.7.3.2) | Device certificates for 802.1X network access; user certificates for VPN and application authentication. | Managed devices and users. |

---

## 6. Use case scope and constraints

### 6.1 Inter-server TLS

The internal TLS Issuing CA issues certificates for server-to-server communication within infrastructure. These certificates are not trusted by external browsers. Any internet-facing service must use a commercially trusted CA.

### 6.2 S/MIME

The S/MIME Issuing CA issues email protection certificates to end users via SCEP profiles. Certificates are trusted only by recipients who have the internal Root CA in their trust store. External recipients will not automatically trust internally issued S/MIME certificates: commercially issued S/MIME certificates are required for cross-organisational S/MIME trust. Certificate profiles must comply with current S/MIME Baseline Requirements.

**Constraint:** Cloud-based PKI S/MIME deployment is limited to managed devices only.

### 6.3 Code signing

Issues certificates for signing internal scripts, PowerShell modules, automation workflows, and software packages used internally. Certificates are trusted only by systems with the internal Root CA installed.

**Hard boundary: publicly distributed software:** Code signing certificates from the internal CA are not trusted by external systems or software distribution platforms. Any software distributed outside the organisation must be signed using a publicly trusted commercial CA certificate. As of December 2025, publicly trusted code signing certificates are limited to 1-year validity per CA/Browser Forum requirements. This boundary is absolute.

### 6.4 Client authentication

Issues device certificates for 802.1X (Wi-Fi and wired) and user certificates for VPN and application authentication. Certificate deployment is managed via SCEP profiles assigned to device or user groups.

---

## 7. Certificate profile requirements

All SCEP certificate profiles deployed via the endpoint management platform must specify:

- Applicable Issuing CA
- Subject Name Format appropriate to use case (e.g., `CN={{DeviceName}}` for device certificates; `CN={{UserName}}, E={{EmailAddress}}` for S/MIME)
- Key Usage and EKU matching the Issuing CA's configured EKU
- Key Size minimum 2048-bit RSA or P-256 ECDSA
- Hash Algorithm SHA-256 or stronger
- Renewal Threshold at 20% of certificate validity or 30 days, whichever is greater

Certificate profiles must be reviewed and approved by the CISO or delegate before deployment. Changes follow the Change Management and Configuration Control Procedure.

---

## 8. Certificate validity periods

| Certificate Type | Validity Period | Renewal Trigger |
|---|---|---|
| Root CA certificate | 10 years | CIO and CISO approval; planned migration required. |
| Issuing CA certificate | 5 years | Automated renewal within cloud-based PKI service; CISO notified. |
| TLS server certificate | 1 year | Automated via SCEP profile at 20% remaining validity. |
| S/MIME user certificate | 1 year | Automated via SCEP profile; old encryption certificates retained for decryption. |
| Code signing certificate | 1 year | Manual renewal request via IT service desk. |
| Client authentication certificate | 1 year | Automated via SCEP profile at 20% remaining validity. |

---

## 9. Trust distribution

The Root CA certificate must be distributed to all systems that need to trust internally issued certificates:

- **Managed devices:** via trusted certificate profile
- **Domain-joined Windows systems:** via Group Policy
- **Servers, network devices, non-Windows endpoints:** via manual import

Trust distribution is a prerequisite for each use case going live.

---

## 10. S/MIME key history and encryption key retention

S/MIME encryption requires that old private keys are retained to decrypt email encrypted under previous certificates. When an S/MIME encryption certificate is renewed, the prior certificate and private key must be retained on the user's device.

---

## 11. CA audit logging

All CA operations are logged within the cloud-based PKI service and endpoint management platform audit log. Logs include:

- CA creation and modification events
- Certificate issuance, renewal, and revocation events
- SCEP profile assignment and delivery events
- Administrator access events

Audit logs are forwarded to SIEM via endpoint management diagnostic settings integration. CA audit logs are retained for 7 years. Access to cloud-based PKI configuration is restricted to designated administrators and governed by Privileged Identity Management (PIM).

---

## 12. Boundary between internal CA and commercial cas

| Use Case | CA Type | Rationale |
|---|---|---|
| Internal server-to-server TLS | Internal CA | Relying parties are managed systems with Root CA deployed. |
| Internet-facing TLS | Commercial CA (e.g., industry-standard commercial CA) | External browsers and clients do not trust the internal Root CA. |
| S/MIME for internal users communicating internally | Internal CA | All relying parties are managed and have Root CA trust. |
| S/MIME for external cross-organisational trust | Commercial CA | External recipients do not have the internal Root CA in their trust store. |
| Code signing for internal scripts and automation | Internal CA | Signed only for execution on managed systems with Root CA trust. |
| Code signing for publicly distributed software | Commercial CA (publicly trusted) | CA/Browser Forum requirement; internal CA is not publicly trusted. |
| Client authentication (device/user certificates) | Internal CA | Authentication endpoints are internal and configured to trust the internal Root CA. |

---

## 13. Framework alignment

| Framework | Reference |
|---|---|
| ISO/IEC 27001:2022 | A.8.24: Use of Cryptography |
| NIST SP 800-57 | Recommendation for Key Management |
| RFC 5280 | Internet X.509 PKI Certificate and CRL Profile |
| CA/Browser Forum Baseline Requirements | Code Signing Certificate Validity (1-year maximum as of December 2025) |
| S/MIME Baseline Requirements | Updated June 2025 |
| CSA CCM v4.1 | CEK-03: Encryption and Key Management: PKI |
| COBIT 2019 | DSS05: Manage Security Services |

---

*Licence: CC BY-SA 4.0. See [`LICENSE`](../LICENSE) in the repository root.*



**End of Document**
