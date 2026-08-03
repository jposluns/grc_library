# OWASP Top 10 and ASVS Alignment Rules

These rules map OWASP Top 10 risks to specific coding requirements. For each risk, the concrete prohibition and required pattern are listed.

**Editions covered:**
- OWASP Top 10:2025 (eighth edition; final release published January 2026): `https://owasp.org/Top10/2025/`. The prior 2021 edition (now superseded) remains accessible at `https://owasp.org/Top10/2021/` for transition reference.
- OWASP ASVS v5.0.0: `https://owasp.org/www-project-application-security-verification-standard/`
- OWASP MCP Top 10: `https://owasp.org/www-project-mcp-top-10/`

The sections below follow the 2025 ordering. Two 2021 categories were restructured for 2025: Server-Side Request Forgery (2021 A10) is rolled into A01 Broken Access Control, and Software Supply Chain Failures (A03) expands the former A06 Vulnerable and Outdated Components; Mishandling of Exceptional Conditions is new at A10. The underlying security principles are stable across editions.

---

## A01:2025 broken access control

**What goes wrong**: Application trusts client-supplied data (user ID, role, tenant) to make authorization decisions without server-side verification.

**Required pattern**:
- Enforce authorization server-side on **every request**: never rely on client claims
- Verify the authenticated user's identity against the requested resource on every operation
- Default deny: deny unless explicitly authorized
- Implement RBAC at the API layer, not only at the UI layer
- Insecure direct object references: validate that the ID in the request belongs to the authenticated user before acting on it
- Apply least privilege to every user, service, and workload identity: grant only the permissions required for its defined operations, and prohibit wildcard or standing elevated permissions unless explicitly justified and reviewed.

**Prohibited patterns**:
```
# Prohibited: trusting user-supplied role
if request.params['role'] == 'admin': allow()

# Prohibited: no ownership check
GET /api/documents/{id}   # Returns document for any authenticated user, regardless of ownership
```

**Server-Side Request Forgery (SSRF)** is rolled into Broken Access Control in the 2025 edition (it was a standalone A10 in 2021): an attacker who controls a URL the server fetches can reach internal services the request was never authorized to reach.
- Validate all URL inputs against an allowlist of permitted domains or IP ranges before making outbound requests
- Block requests to internal and reserved IP ranges. **IPv4**: `10.0.0.0/8` (RFC 1918 private), `172.16.0.0/12` (RFC 1918 private; spans `172.16.0.0` through `172.31.255.255`), `192.168.0.0/16` (RFC 1918 private), `169.254.0.0/16` (link-local; RFC 3927; also covers AWS/GCP/Azure cloud-instance-metadata at `169.254.169.254`), `127.0.0.0/8` (loopback; RFC 1122), `100.64.0.0/10` (CGNAT; RFC 6598). **IPv6**: `::1/128` (loopback; RFC 4291), `fc00::/7` (unique local addresses / ULA; RFC 4193), `fe80::/10` (link-local; RFC 4291; also covers IPv6 cloud-instance-metadata variants such as `fd00:ec2::254` on AWS).
- Do not follow redirects automatically when the redirect destination is user-controlled
- Use a separate egress network policy to block outbound requests to internal services from web-facing applications
```python
# Prohibited: fetching user-supplied URL without validation
url = request.params['callback_url']
requests.get(url)  # SSRF risk
```

---

## A02:2025 security misconfiguration

**Required pattern**:
- Disable or remove all default accounts, default passwords, and example configurations before deployment
- Remove development features, debug endpoints, and diagnostic interfaces before production
- Error responses must not reveal software version, stack trace, or system configuration
- Keep all software and libraries updated: run SCA in CI/CD
- Protect every state-changing browser request that uses cookie-based or other ambient credentials against CSRF. Use framework CSRF middleware or an unpredictable token bound to the user session; verify `Origin` or `Referer` where appropriate; never use GET for state changes. `SameSite` is defence in depth, not a replacement for CSRF-token validation.
- Set session cookies with `Secure`, `HttpOnly`, and `SameSite=Lax` or `Strict`. Use `SameSite=None` only when cross-site use is required, and only with `Secure`.
- Send a restrictive `Content-Security-Policy`, `Strict-Transport-Security` after the service is fully HTTPS, `X-Content-Type-Options: nosniff`, and clickjacking protection through CSP `frame-ancestors` and/or `X-Frame-Options`. Do not disable these headers for convenience.
- Never disable, bypass, or suppress authentication, authorization, validation, TLS, logging, or another security control for convenience. Any exception requires documented scope, responsible-authority approval, compensating controls, and an expiry or review date.

**Prohibited patterns**:
- Default administrative credentials left unchanged
- Directory listing enabled on web server
- Verbose error messages revealing stack traces to external callers
- CORS wildcard in production (`Access-Control-Allow-Origin: *`)

---

## A03:2025 software supply chain failures

New category name in 2025: it expands the former A06 Vulnerable and Outdated Components to cover the whole ecosystem of dependencies, build systems, and distribution infrastructure.

**What goes wrong**: Compromised or malicious dependencies, build systems, update mechanisms, or AI-hallucinated package names introduce malicious code into the supply chain.

**Required pattern**:
- SCA (Software Composition Analysis) scan on every build; fail the build on Critical CVEs; High CVEs require tracked remediation within 14 days
- Verify dependency names exist in approved registries before installing: AI-suggested packages can be hallucinated
- Pin exact versions in lockfiles committed to source control
- SBOM generated for every production release
- Sign all production build artefacts (SLSA provenance) and verify checksums on all downloaded packages and build artefacts

**Prohibited patterns**:
- Using a library with a known Critical CVE
- Installing packages without lockfiles, or from unverified registries
- Floating version pins (e.g., `>=1.0`) in production: use pinned versions
- Unsigned artefacts deployed to production

---

## A04:2025 cryptographic failures

See [`core/cryptography.md`](cryptography.md) for full requirements. Key rules:
- No plaintext storage of sensitive data (passwords, payment data, credentials)
- No deprecated algorithms (MD5, SHA-1, DES, RC4)
- No hardcoded keys or IVs
- TLS 1.2 minimum on all connections transmitting sensitive data (the ASVS baseline; this pack's canonical mandate in [`core/cryptography.md`](cryptography.md) is TLS 1.3, with TLS 1.2 and earlier prohibited)
- Password hashing: Argon2id (preferred), scrypt, or bcrypt; PBKDF2 (high iteration count) where FIPS-140 compliance is required

---

## A05:2025 injection

See [`core/input-validation.md`](input-validation.md) for full requirements. Key rules:
- Parameterized queries only: no string concatenation for SQL, LDAP, XPath
- Reject invalid input: do not sanitize and continue
- Context-aware output encoding for all output contexts
- Never pass user input to shell commands without allowlist validation

---

## A06:2025 insecure design

**Required pattern**:
- Threat model every new feature that handles sensitive data, authentication, or external integrations. Follow the adopting project's threat-modelling standard. In the parent GRC library, `security/standard-threat-modelling.md` defines the STRIDE-per-trust-boundary methodology and the Mandatory / Approval-Gated / Prohibited disposition model applied to each identified threat.
- Apply defense-in-depth: multiple independent security controls, not a single gate
- Design for failure securely: when a component fails, it should fail closed, not open
- Record security-relevant design decisions and trade-offs, including the threat, selected control, residual risk, owner, and review point.
- Turn threat-model abuse cases into tests and exercise each security control with representative known attack patterns before release.

**Prohibited patterns**:
- "We'll add security later": security controls must be in the design, not retrofitted
- Single-point authentication where one bypass path circumvents all controls
- Trust-on-first-use without subsequent verification

---

## A07:2025 authentication failures

See [`core/authentication.md`](authentication.md) for full requirements. Renamed from Identification and Authentication Failures in 2021. Key rules:
- MFA mandatory: no bypass paths
- Session tokens: 128-bit entropy minimum; expire on logout; never in URLs
- Brute-force protection on all authentication endpoints
- Generic error messages for authentication failures

---

## A08:2025 software or data integrity failures

**Required pattern**:
- Verify signatures or checksums on downloaded packages and build artefacts
- Use lockfiles (package-lock.json, requirements.txt with pinned versions, Gemfile.lock) committed to source control
- CI/CD pipelines must not be modifiable without source control review
- SBOM maintained for all production software

**Prohibited patterns**:
- Installing dependencies without a lockfile
- Unsigned build artefacts deployed to production
- CI/CD pipeline definitions that can be modified without code review

---

## A09:2025 security logging & alerting failures

Renamed from Security Logging and Monitoring Failures in 2021 to emphasize alerting: logging without alerting rarely induces action on a security event.

**Required pattern**:
- Log: all authentication events; authorization failures; all access to data classified as sensitive under the adopting project's scheme (Confidential or Restricted in the parent GRC library); significant configuration changes; all API calls with caller, endpoint, response code, timestamp
- Forward all logs to SIEM: not only to local files
- Test that alerts fire for critical events

**Prohibited patterns**:
- No logging on authentication failures
- Logging passwords, tokens, or PII
- Logs that are modifiable by the actor who generated them

---

## A10:2025 mishandling of exceptional conditions

New category in 2025: improper error handling, logical errors, and failing open when a system meets an abnormal condition it did not anticipate.

**Required pattern**:
- Handle every exceptional and error condition explicitly; on an error in a security decision (authentication, authorization, validation), **fail closed**, never fail open
- Do not swallow exceptions silently: an unhandled or discarded error is a decision to proceed in an unknown state
- Keep internal error detail (stack traces, system paths, schema) out of responses to external callers; return a generic message and a correlation id, and log the detail server-side (see A02 Security Misconfiguration)
- Validate the assumptions a control-flow path depends on rather than assuming the happy path; handle the abnormal branch deliberately

**Prohibited patterns**:
```python
# Prohibited: swallowing the error and continuing in an unknown state
try:
    authorized = check_authorization(user, resource)
except Exception:
    authorized = True   # fails OPEN on error

# Prohibited: empty catch that discards the failure
try:
    verify_signature(artifact)
except Exception:
    pass   # proceeds as if verification succeeded
```

---

## OWASP MCP top 10 quick reference

Security risks for systems using the Model Context Protocol (MCP). Full detail in [`ai/mcp-security.md`](../ai/mcp-security.md).

| Risk | What Goes Wrong | Key Control |
| --- | --- | --- |
| MCP01 Token Mismanagement & Secret Exposure | Hard-coded credentials, long-lived tokens, or secrets stored in model memory or protocol logs expose connected systems | Store secrets in a vault; short-lived scoped tokens; keep secrets out of prompts, memory, and logs |
| MCP02 Privilege Escalation via Scope Creep | Loosely-defined MCP permissions expand over time, granting agents excessive capability | Least-privilege scopes; periodic scope review; deny self-granted or widening permissions |
| MCP03 Tool Poisoning | An adversary compromises tools, plugins, or their outputs to inject malicious or misleading context | Verify the tool registry; validate tool descriptions and outputs before use; treat tool output as untrusted |
| MCP04 Software Supply Chain Attacks & Dependency Tampering | A compromised dependency alters agent behaviour or introduces execution-level backdoors | Pin and verify dependencies; require signed artifacts; maintain an SBOM and scan for tampering |
| MCP05 Command Injection & Execution | The agent constructs and executes commands, shell, API calls, or code from untrusted input without validation | Never build commands from untrusted input; parameterize; no shell or arbitrary filesystem or code execution |
| MCP06 Intent Flow Subversion | Malicious instructions embedded in retrieved context hijack the agent's intent flow toward an attacker goal | Treat retrieved context as data, never instructions; separate instruction and data channels; verify intent |
| MCP07 Insufficient Authentication & Authorization | MCP servers, tools, or agents fail to verify identity or enforce access controls | Require authentication on every tool call; OAuth scopes; verify identity for every agent and service |
| MCP08 Lack of Audit and Telemetry | Limited telemetry from MCP servers and agents impedes investigation and incident response | Immutable audit logs of tool invocations, context changes, and user-agent interactions; alert on anomalies |
| MCP09 Shadow MCP Servers | Unapproved or unsupervised MCP deployments operate outside formal security governance | Inventory and govern all MCP deployments; block unapproved servers; no default credentials or open configs |
| MCP10 Context Injection & Over-Sharing | Shared, persistent, or under-scoped context windows leak sensitive information across tasks, users, or agents | Scope and isolate context per task, user, and agent; apply TTL; clear sensitive state on session end |

---

## OWASP ASVS v5.0.0 quick reference by level

| ASVS Area | Level 1 (Minimum) | Level 2 (Standard) | Level 3 (Advanced) |
| --- | --- | --- | --- |
| V6 Authentication | MFA, basic session management | Phishing-resistant MFA, credential management | Full authn assurance, hardware key |
| V7 Session | Basic invalidation | Absolute timeout, rotation | Full session assurance |
| V2 Validation | Input type checking | Schema validation, reject invalid | Full allowlist validation |
| V11 Cryptography | Approved algorithms | Key management | HSM, formal key lifecycle |
| V12 Communication | TLS required | TLS 1.2+, cert validation | TLS 1.3, cert pinning |
| V4 API | Auth on all endpoints | Full schema validation | Rate limit, API versioning |

Default target: ASVS Level 2 for all applications handling data classified as sensitive under the adopting project's scheme (Confidential or Restricted in the parent GRC library). The V12 level cells restate the ASVS progression verbatim; the pack's own transport-security floor is TLS 1.3 at every level, per [`core/cryptography.md`](cryptography.md).

ASVS v5.0.0 reference: `https://owasp.org/www-project-application-security-verification-standard/`

---

## Framework alignment

The OWASP Risk column follows the 2025 ordering. (The ISO 27001 / NIST SSDF / CSA CCM mapping values are unchanged from the prior edition and are reviewed separately.)

| OWASP Risk | ISO 27001 | NIST SSDF | CSA CCM |
| --- | --- | --- | --- |
| A01 Broken Access Control (incl. SSRF) | A.5.15 to 5.18 | PW.6 | IAM-04 to 05 |
| A02 Security Misconfiguration | A.8.9 | PW.9 | CCC-07 |
| A03 Software Supply Chain Failures | A.8.8 | PO.5, PW.4 | TVM-06 |
| A04 Cryptographic Failures | A.8.24 | PW.7 | CEK-01 to 21 |
| A05 Injection | A.8.28 | PW.6 | AIS-02 |
| A06 Insecure Design | A.8.25 to 8.27 | PW.1 to PW.4 | AIS-01 |
| A07 Authentication Failures | A.5.17 | N/A | IAM-13 to 15 |
| A08 Software or Data Integrity Failures | A.8.27 | PS.2 | CCC-04 to 05 |
| A09 Security Logging & Alerting Failures | A.8.15 to 8.16 | RV.1 | LOG-01 to 13 |
| A10 Mishandling of Exceptional Conditions | A.8.28 | PW.5 | AIS-04 |
