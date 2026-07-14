# Developer Security Requirements

**Document Title:** Developer Security Requirements\
**Document Type:** Standard\
**Version:** 1.1.7\
**Date:** 2026-07-14\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-security-quick-reference.md`](standard-security-quick-reference.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** 6 to 12 months and upon material threat, tooling, or framework change\
**Repository Path:** [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

These requirements are design constraints that apply from the first line of code. Failure to meet them should block production promotion. For a quick-reference version, see the Security Quick Reference standard. For AI-specific security requirements, see the AI and Agentic Development Security Standard.

---

## 2. Secure development lifecycle

### 2.1 Requirements phase

Before design begins, document: what data the feature creates, reads, updates, or deletes and its classification; who needs access and under what conditions; what external systems or APIs are involved; whether personal data is processed (Privacy Impact Assessment required); whether AI/ML is used (AI controls matrix requirements apply from this point).

### 2.2 Threat modelling

Mandatory for: any new application or service; any new API endpoint handling Confidential or Restricted data; any authentication or authorization mechanism; any integration with external systems; any AI/ML component; any significant change to a security-sensitive component. Use STRIDE methodology. Document, review with the security team, and retain as evidence. Update when design changes materially.

*CCM: TVM-04 / AICM: TVM-12*

### 2.3 Pre-production gate (acceptance into service)

Before production promotion, the following must be demonstrated:

1. All threat model findings addressed or formally accepted with documented rationale.
2. SAST results reviewed: no unmitigated Critical or High findings.
3. SCA results reviewed: no unmitigated Critical CVEs in dependencies.
4. Security test evidence present in pipeline.
5. Data classification confirmed and enforced in code.
6. Secrets confirmed absent from code, config files, and build artefacts.
7. Logging and monitoring hooks confirmed operational.
8. For AI/ML features: AI risk classification completed, AI controls matrix requirements verified.
9. Privacy Impact Assessment completed where personal data is involved.
10. Architecture sign-off from CIO or designated security architect for net-new systems.

*CCM: AIS-06 / COBIT: BAI07*

---

## 3. Authentication requirements

### 3.1 Identity provider

An enterprise identity provider (IdP) is the authority for all user-facing authentication. Custom authentication mechanisms or local user stores must not be implemented.

### 3.2 MFA

Mandatory. Enforced at the identity platform layer. Applications must not provide any bypass or fallback path that circumvents MFA.

### 3.3 Service authentication

Use one of: platform managed identity (preferred for cloud workloads); PAM-vaulted service account with credential injection; OAuth 2.0 client credentials flow with registered application identity. Shared secrets in code or config are prohibited.

### 3.4 Application onboarding: authentication gate

Any application onboarding to a production environment must meet the following authentication requirements before production access is granted. These are hard gates: production access is denied without them.

- UPN/SSO authentication fully implemented and tested. SAMAccountName-only authentication is prohibited.
- All directory integration binds use LDAPS (port 636). Plain LDAP binds on port 389 are prohibited.
- All service account credentials stored in the PAM vault or platform secrets management service. No hard-coded credentials in any form.
- Database connections use Kerberos authentication or managed identity where the platform supports it. Username/password SQL authentication is prohibited for service accounts.

### 3.5 Authentication patterns by application type

**Customer-facing portals and external user interfaces:** External users must authenticate via the organization's external identity management platform with MFA enforced. No custom authentication mechanisms or local user stores. Customer data isolation must be enforced server-side on every API call regardless of frontend claims.

**Internal applications:** Enterprise IdP SSO with Conditional Access. No bypass paths that circumvent MFA.

**Mobile applications:** Platform-provided authentication SDK (e.g., MSAL or equivalent) with secure token storage only. Authentication tokens must not be stored in unencrypted local storage. Refresh token rotation must be implemented.

**API gateway integrations:** OAuth 2.0 client credentials flow validated by IdP token validation policy at the gateway layer. App roles defined per operation. Every operation enforces the minimum required role. API subscription keys are an additional layer only: not the sole authentication mechanism.

### 3.6 Session management

Tokens: minimum 128 bits entropy; invalidated on logout; absolute timeouts (8 hours standard, 1 hour elevated privilege); never in URLs or logs; refresh tokens rotatable and revocable.

*CCM: IAM-13, IAM-14, IAM-15*

---

## 4. Authorization requirements

- All RBAC enforced server-side. Client-side checks are UI affordances, not security controls.
- Authorization decisions made on every call: no implicit allow.
- Default deny: access is denied unless explicitly granted.
- Separation of duties for financial, operational, and security-critical functions.

*CCM: IAM-04, IAM-05*

---

## 5. Secrets management

**Absolute rule: no secrets in code, config files in version control, build scripts, Dockerfiles, CI/CD definitions, or log output.** Violations found in code review are treated as compromised immediately.

| Environment | Approved Store |
| --- | --- |
| Cloud workloads | Platform secrets management service (e.g., cloud key vault) via managed identity |
| On-premises applications | PAM vault: per PAM standard |
| CI/CD pipelines | CI/CD platform service connections or equivalent pipeline secrets mechanism |
| Application runtime | Managed identity for secrets access, or PAM credential injection |
| Workflow automation | Secrets management references or platform-native secure secret injection. Never plain-text in configuration files tracked in version control. |
| API gateway named values | Secrets management-backed values only. Never hardcoded plain text in gateway policies. |
| Developer local testing | Developer's own isolated secrets vault instance or local `.env` file that is `.gitignored`. Never in source code. |
| Python workloads | No secrets in settings files tracked in version control. Database connections use managed identity or secrets references. |

Secret rotation must work without a code deployment. Hard-coded secrets that require a deployment to rotate are a design failure. Secret scanning must be configured in all repositories including historical commits.

*CCM: CEK-10 through CEK-21*

---

## 6. Input validation and output encoding

- Validate all external input: type, length, format, range. Reject malformed input: do not sanitize it.
- Server-side validation is mandatory. Client-side is UX only.
- Parameterized queries only. String concatenation to build SQL, LDAP, or XPath queries is prohibited.
- Context-aware output encoding for all output contexts (HTML, JSON, XML, SQL, command-line, log).
- File uploads: validate by content (not extension); limit size; store outside web root; scan before processing; never execute.
- APIs: validate all request parameters, headers, and bodies against defined schema. Unknown fields rejected. Request size limits enforced.
- Browser-delivered web applications enforce a Content-Security-Policy that disallows inline script by default and adopts Trusted Types (`require-trusted-types-for 'script'`) where the runtime supports it, to contain DOM-based cross-site scripting.
- Web responses set the transport and content-type hardening headers: Strict-Transport-Security with a long `max-age` and `preload`; `X-Content-Type-Options: nosniff`; and `frame-ancestors` (or `X-Frame-Options`) to prevent clickjacking.

*CCM: AIS-02 / OWASP ASVS V2, V1*

---

## 7. Cryptography requirements

| Use Case | Approved | Prohibited |
| --- | --- | --- |
| Symmetric encryption | AES-256-GCM | DES, 3DES, RC4, Blowfish |
| Asymmetric encryption | RSA-4096, EC P-256/P-384 | RSA < 2048 |
| Key exchange | ECDHE, DHE | Static RSA, DH < 2048 |
| Hashing (integrity) | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Password hashing | Argon2id, bcrypt (cost ≥12) | MD5, SHA-256 (unsalted), plain text |
| TLS | TLS 1.3 (or stronger), aligned to [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) §4 (Encryption standards) canonical mandate | SSL, TLS 1.0, TLS 1.1, TLS 1.2 |
| Certificate signing | SHA-256 RSA or ECDSA | SHA-1 |

Keys must not be hardcoded. Store in approved secrets management service. Key rotation must be supported without downtime.

*CCM: CEK-01 through CEK-21*

---

## 8. CORS policy

Wildcard CORS origins (`origins: "*"`) are prohibited in all production APIs and services. This applies to all web applications, REST APIs, function-as-a-service, and workflow HTTP triggers. The correct pattern is an explicit allow-list of permitted origins, stored in application configuration and enforced at the application layer. CORS policy configuration is a security-sensitive change and must pass code review before deployment. CORS misconfiguration is a High finding in the acceptance-into-service gate.

*CCM: AIS-02*

---

## 9. Security testing requirements

| Test Type | When | Pipeline Gate |
| --- | --- | --- |
| SAST | Every commit to protected branch | Fail on Critical or High |
| SCA (dependency scan) | Every build | Fail on Critical CVE; High: remediate within 14 days |
| Container image scan | Every image build | Fail on Critical CVE in image or layer |
| DAST | Before production promotion; quarterly in production | OWASP Top 10 minimum |
| Penetration test | Before first production deployment; annually thereafter | Third-party qualified tester |

An SBOM must be generated for every production release and retained. See penetration testing and red team programme standard for full programme requirements.

*CCM: AIS-05, TVM-07*

---

## 10. Dependency and open-source governance

- Source from approved, trusted registries only.
- Before adding any dependency: confirm active maintenance (last release within 24 months); compatible licence; no Critical/High CVEs; no supply chain compromise flags.
- SCA scanning covers transitive dependencies.
- GPL/AGPL licenses require Legal approval before use in commercial software. Apache 2.0, MIT, BSD generally approved.
- AI-suggested dependency names must be verified to exist in approved registries before installation (hallucinated package names are an active supply-chain attack vector).
- Python: a dependency management tool is required (pinned requirements.txt or equivalent). SCA scanning covers Python packages.

*CCM: TVM-06, AIS-04 / SLSA Level 2+*

---

## 11. Secure coding practices

### 11.1 Code review

All code reviewed by at least one peer before merging to a protected branch. Security-sensitive code requires a security-focused review. Reviewer must not be the author. Code review must check for: hard-coded secrets; missing input validation; missing authorization checks; insecure direct object references; error handling that leaks sensitive information; logging that captures personal or sensitive data.

### 11.2 Error handling

Error messages returned to callers must not disclose stack traces, system names, IP addresses, paths, database schema, or authentication mechanism details. Log full error server-side. Return a generic error with a correlation ID.

### 11.3 Logging

Must not capture passwords, payment data, full personal records, session tokens, or encryption keys. Every significant security event must be logged per the security baseline logging requirements.

### 11.4 AI-generated code

Subject to identical review, testing, and quality requirements as human-written code. Check specifically for: hard-coded credentials; outdated cryptographic patterns; missing input validation; incorrect authorization patterns; hallucinated security controls that appear correct but are not.

---

## 12. AI and machine learning development requirements

For detailed AI security requirements, see the AI and Agentic Development Security Standard. That standard supersedes this section for AI/ML-specific controls.

### 12.1 AI risk classification

Required before any AI feature enters development. High-impact AI systems additionally require: AI impact assessment; bias and fairness assessment; explainability assessment; human oversight mechanism; ethics review.

### 12.2 Training data

- Classified under the organization's data classification scheme.
- Kept separate from production data unless a documented, approved process is in place.
- Provenance documented.
- Personal data in training datasets requires PIA and explicit legal basis.

### 12.3 AI acceptable use

Developers must not use AI tools to: generate synthetic data mimicking real personal data without approval; bypass access controls or security review steps; process Confidential or Restricted data in external AI services without a data processing agreement and CIO approval.

### 12.4 AI threat testing

Before any AI feature enters production, adversarial testing for AI-specific threats must be conducted:
- Prompt injection attacks (direct and indirect)
- Data exfiltration through model outputs
- Tool-call manipulation in agentic systems
- Model inversion and membership inference risks
- Output validation failures

Reference adversarial test frameworks include OWASP LLM Top 10, MITRE ATLAS, and open-source adversarial testing utilities such as TikiTribe (for MCP server security, tool-call injection resistance, and agentic workflow attack surface enumeration).

---

## 13. API security requirements

- Authentication required on all endpoints handling non-public data.
- OAuth 2.0 with PKCE for user-delegated flows. OAuth 2.0 client credentials for service-to-service. API keys must not be the sole authentication mechanism for sensitive operations.
- Rate limiting on all external-facing endpoints.
- Input validation per §6 for all parameters, headers, query strings, and bodies.
- Responses must not include more data than the caller is authorized to receive.
- API versioning with documented end-of-life dates. Deprecated versions monitored for continued use.
- OpenAPI documentation maintained. Security schemes documented.

*CCM: AIS-08*

---

## 14. Data handling in code

- Data minimization is a legal requirement under PIPEDA and Quebec Law 25.
- Production data must not be copied to Test or Dev. Documented data masking or synthetic data generation is required.
- Log files must not contain unmasked personal data.
- Data retention periods must be implemented in application logic. Delete or anonymize at end of retention period. Refer to the data retention schedule register.

*CCM: DSP-15, DSP-16*

---

## 15. Workflow automation security requirements

### 15.1 Secrets

Secrets in workflow configuration files are prohibited. All secrets must use platform-native secrets management references or equivalent secure secret injection. Any confirmed plain-text credential in a workflow must be treated as compromised and rotated immediately.

### 15.2 Runtime

All workflow runtimes must be on a supported, non-EOL version. Any runtime reaching EOL must be upgraded per the EOL policy in the security baseline standard.

### 15.3 Notification and approval recipients

Hardcoded personal email addresses as error notification or approval recipients are prohibited. All recipients must be a distribution list or role-based address.

### 15.4 Workflow routing integrity

Every routing case must point to an enabled, active target workflow. Routing to disabled workflows causes silent data loss. Routing production traffic to test endpoints is prohibited.

### 15.5 Parameterization

Hardcoded entity identifiers (customer IDs, account IDs, tenant identifiers) are prohibited. Use configurable parameters. Static date boundaries are prohibited; use relative date expressions.

### 15.6 OAuth connection re-authorization

OAuth-based platform connections expire periodically (typically every 90 days). A quarterly re-authorization audit of all OAuth-type connections is mandatory.

---

## 16. Robotic process automation (RPA) security requirements

- RPA bots run under a dedicated service account, not a personal account.
- Service account registered in PAM vault and subject to rotation policy.
- Host machine enrolled in endpoint detection and response (EDR) tooling.
- Desktop flow run history retained and accessible for audit.

---

## 17. Framework and runtime EOL: developer requirements

The EOL classification policy and remediation SLAs are defined in the Security Baseline Standard. Developer obligations:

- All applications must declare their runtime versions explicitly. Undeclared or floating runtime versions are prohibited in production.
- When a runtime enters Class 3 (within 180 days of EOL), create an upgrade task in the team backlog.
- When a runtime is Class 2 (within 90 days of EOL or already EOL), the upgrade must be in active development with a target completion date.
- When a runtime is Class 1 (over 12 months EOL with qualifying CVE), the service must be in emergency remediation. No new feature development occurs until the runtime is upgraded.
- CI/CD pipelines must not deploy code to a runtime version classified as EOL by organizational policy.
- AI-generated code suggestions to use deprecated or EOL package versions must be rejected.

---

## 18. Application production onboarding: security prerequisites

All of the following must be validated before any application onboards to a production environment. These are hard gates: production access is denied until each item is confirmed.

- UPN/SSO authentication fully implemented and tested (no SAMAccountName-only dependency)
- All directory binds use LDAPS (port 636). No plain LDAP.
- All service credentials in platform secrets management service or PAM vault. No hard-coded credentials.
- SAST, SCA, and secret scanning passing in CI/CD pipeline.
- Threat model documented and reviewed.
- Data flow documentation produced.
- Privacy Impact Assessment completed where personal data is processed.
- Database deployed in an isolated network segment with no direct internet access.
- SBOM generated for the release.
- Integration endpoints documented and firewall/ACL rules approved.
- Application service owner entry populated in the application registry.

---

## 19. Framework alignment

| Control Area | ISO/IEC 27001/27002 | CSA CCM v4.1 | NIST SSDF | OWASP ASVS | OWASP Top 10 |
| --- | --- | --- | --- | --- | --- |
| Secure SDLC | A.8.25 to 8.26 | AIS-01 to 06 | PW.1 to PW.4 | V15 | N/A |
| Authentication | A.5.15 to 5.18 | IAM-13 to 15 | N/A | V6 | A01, A07 |
| Secrets management | A.8.10 to 8.11 | CEK-10 to 21 | PW.8 | V13 | A02 |
| Input validation | A.8.28 | AIS-02 | N/A | V2, V1 | A03 |
| Cryptography | A.8.24 | CEK-01 to 21 | N/A | V11 | A02 |
| Error handling and logging | A.8.16 | LOG-01 to 13 | N/A | V16 | A09 |
| Security testing | A.8.29 | AIS-05, TVM-07 | VE.1 to VE.3 | All levels | All |
| Dependency management | A.8.8 | TVM-06, AIS-04 | PO.5 | V15 | A06 |
| API security | A.8.24 | AIS-08 | N/A | V4 | A01, A02 |
| AI/ML security | N/A | AICM TVM-12 | N/A | N/A | OWASP LLM Top 10 |

---

**End of Document**
