# OWASP Top 10 and ASVS Alignment Rules

These rules map OWASP Top 10 risks to specific coding requirements. For each risk, the concrete prohibition and required pattern are listed.

**Editions covered:**
- OWASP Top 10:2025 (eighth edition, released November 2025): `https://owasp.org/Top10/2025/`. The prior 2021 edition (now superseded) remains accessible at `https://owasp.org/Top10/2021/` for transition reference.
- OWASP ASVS v5.0.0: `https://owasp.org/www-project-application-security-verification-standard/`
- OWASP MCP Top 10: `https://owasp.org/www-project-mcp-top-10/`

The 2025 edition moves Supply Chain Failures to A03 (previously tracked as A06 Vulnerable and Outdated Components). Rules in this file apply regardless of edition: the underlying security principles are stable.

---

## A01: broken access control

**What goes wrong**: Application trusts client-supplied data (user ID, role, tenant) to make authorization decisions without server-side verification.

**Required pattern**:
- Enforce authorization server-side on **every request**: never rely on client claims
- Verify the authenticated user's identity against the requested resource on every operation
- Default deny: deny unless explicitly authorized
- Implement RBAC at the API layer, not only at the UI layer
- Insecure direct object references: validate that the ID in the request belongs to the authenticated user before acting on it

**Prohibited patterns**:
```
# Prohibited: trusting user-supplied role
if request.params['role'] == 'admin': allow()

# Prohibited: no ownership check
GET /api/documents/{id}   # Returns document for any authenticated user, regardless of ownership
```

---

## A02: cryptographic failures

See [`core/cryptography.md`](cryptography.md) for full requirements. Key rules:
- No plaintext storage of sensitive data (passwords, payment data, credentials)
- No deprecated algorithms (MD5, SHA-1, DES, RC4)
- No hardcoded keys or IVs
- TLS 1.2 minimum on all connections transmitting sensitive data (the ASVS baseline; this pack's canonical mandate in [`core/cryptography.md`](cryptography.md) is TLS 1.3, with TLS 1.2 and earlier prohibited)
- Password hashing: Argon2id or bcrypt only

---

## A03: injection

See [`core/input-validation.md`](input-validation.md) for full requirements. Key rules:
- Parameterized queries only: no string concatenation for SQL, LDAP, XPath
- Reject invalid input: do not sanitize and continue
- Context-aware output encoding for all output contexts
- Never pass user input to shell commands without allowlist validation

---

## A04: insecure design

**Required pattern**:
- Threat model every new feature that handles Confidential data, authentication, or external integrations. The library's [`security/standard-threat-modelling.md`](../../../security/standard-threat-modelling.md) defines the STRIDE-per-trust-boundary methodology and the Mandatory / Approval-Gated / Prohibited disposition model the threat-modelling workshop applies to each identified threat.
- Apply defense-in-depth: multiple independent security controls, not a single gate
- Design for failure securely: when a component fails, it should fail closed, not open

**Prohibited patterns**:
- "We'll add security later": security controls must be in the design, not retrofitted
- Single-point authentication where one bypass path circumvents all controls
- Trust-on-first-use without subsequent verification

---

## A05: security misconfiguration

**Required pattern**:
- Disable or remove all default accounts, default passwords, and example configurations before deployment
- Remove development features, debug endpoints, and diagnostic interfaces before production
- Error responses must not reveal software version, stack trace, or system configuration
- Keep all software and libraries updated: run SCA in CI/CD

**Prohibited patterns**:
- Default administrative credentials left unchanged
- Directory listing enabled on web server
- Verbose error messages revealing stack traces to external callers
- CORS wildcard in production (`Access-Control-Allow-Origin: *`)

---

## A06: vulnerable and outdated components

**Required pattern**:
- SCA (Software Composition Analysis) scan on every build
- Fail the build on Critical CVEs; High CVEs require tracked remediation within 14 days
- Verify dependency names exist in approved registries before installing (AI-suggested packages can be hallucinated)
- SBOM generated for every production release

**Prohibited patterns**:
- Using a library with a known Critical CVE
- Installing packages from unverified sources
- Floating version pins (e.g., `>=1.0`) in production: use pinned versions

---

## A07: identification and authentication failures

See [`core/authentication.md`](authentication.md) for full requirements. Key rules:
- MFA mandatory: no bypass paths
- Session tokens: 128-bit entropy minimum; expire on logout; never in URLs
- Brute-force protection on all authentication endpoints
- Generic error messages for authentication failures

---

## A08: software and data integrity failures

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

## A09: security logging and monitoring failures

**Required pattern**:
- Log: all authentication events; authorization failures; all access to Confidential/Restricted data; significant configuration changes; all API calls with caller, endpoint, response code, timestamp
- Forward all logs to SIEM: not only to local files
- Test that alerts fire for critical events

**Prohibited patterns**:
- No logging on authentication failures
- Logging passwords, tokens, or PII
- Logs that are modifiable by the actor who generated them

---

## A10: server-side request forgery (SSRF)

**Required pattern**:
- Validate all URL inputs against an allowlist of permitted domains or IP ranges before making outbound requests
- Block requests to internal and reserved IP ranges. **IPv4**: `10.0.0.0/8` (RFC 1918 private), `172.16.0.0/12` (RFC 1918 private; spans `172.16.0.0` through `172.31.255.255`), `192.168.0.0/16` (RFC 1918 private), `169.254.0.0/16` (link-local; RFC 3927; also covers AWS/GCP/Azure cloud-instance-metadata at `169.254.169.254`), `127.0.0.0/8` (loopback; RFC 1122), `100.64.0.0/10` (CGNAT; RFC 6598). **IPv6**: `::1/128` (loopback; RFC 4291), `fc00::/7` (unique local addresses / ULA; RFC 4193), `fe80::/10` (link-local; RFC 4291; also covers IPv6 cloud-instance-metadata variants such as `fd00:ec2::254` on AWS).
- Do not follow redirects automatically when the redirect destination is user-controlled
- Use a separate egress network policy to block outbound requests to internal services from web-facing applications

**Prohibited patterns**:
```python
# Prohibited: fetching user-supplied URL without validation
url = request.params['callback_url']
requests.get(url)  # SSRF risk
```

---

---

## A03:2025: software supply chain failures (new in 2025)

In the 2025 edition, supply chain failures are elevated to A03.

**What goes wrong**: Compromised or malicious dependencies, build systems, update mechanisms, or AI-hallucinated package names introduce malicious code into the supply chain.

**Required pattern**:
- SCA scan on every build; fail on Critical CVE
- SBOM generated for every production release
- Verify dependency names exist in approved registries before installing: AI-suggested packages can be hallucinated
- Pin exact versions in lockfiles committed to source control
- Sign all production build artefacts (SLSA provenance)
- Verify checksums on all downloaded packages and build artefacts

**Prohibited patterns**:
- Installing packages without lockfiles
- Unsigned artefacts deployed to production
- Floating version pins (`>=1.0`) in production
- Packages installed from unverified registries

---

## OWASP MCP top 10 quick reference

Security risks for systems using the Model Context Protocol (MCP). Full detail in [`ai/mcp-security.md`](../ai/mcp-security.md).

| Risk | What Goes Wrong | Key Control |
| --- | --- | --- |
| MCP01 Tool Poisoning | Malicious tool descriptions manipulate AI decisions | Verify tool registry; validate tool descriptions before use |
| MCP02 Insecure Authentication | Unauthenticated tool endpoints allow unauthorized access | Require auth on every tool call; OAuth 2.0 scopes |
| MCP03 Tool-Call Injection | Adversarial data in tool inputs/outputs manipulates execution | Sanitize all content before using as tool arguments; never trust retrieved content as instructions |
| MCP04 Resource Injection | Malicious URIs or resource identifiers exfiltrate data | Validate all URI inputs against allowlist; no internal path exposure |
| MCP05 Excessive Tool Scope | Tools expose capabilities beyond their stated purpose | Least-privilege tool definitions; no shell/arbitrary filesystem access |
| MCP06 Model Misbinding | Wrong model version used silently | Explicit model version pinning; verify model identity at session start |
| MCP07 Prompt-State Manipulation | Crafted sequences alter model behaviour across turns | Log full conversation context; alert on anomalous instruction patterns |
| MCP08 Insecure Memory | Persistent memory leaks sensitive state across sessions | Clear sensitive state on session end; apply TTL to memory entries |
| MCP09 Covert Channel Abuse | Steganographic or timing attacks exfiltrate data | Audit and rate-limit all outbound calls from agent; alert on unusual output patterns |
| MCP10 Uncontrolled Recursion | Agent loops or excessive tool calls exhaust resources | Max chain-depth limit; token budget; circuit breaker on error loops |

---

## OWASP ASVS v5.0.0 quick reference by level

| ASVS Area | Level 1 (Minimum) | Level 2 (Standard) | Level 3 (Advanced) |
| --- | --- | --- | --- |
| V2 Authentication | MFA, basic session management | Phishing-resistant MFA, credential management | Full authn assurance, hardware key |
| V3 Session | Basic invalidation | Absolute timeout, rotation | Full session assurance |
| V5 Validation | Input type checking | Schema validation, reject invalid | Full allowlist validation |
| V6 Cryptography | Approved algorithms | Key management | HSM, formal key lifecycle |
| V9 Communication | TLS required | TLS 1.2+, cert validation | TLS 1.3, cert pinning |
| V13 API | Auth on all endpoints | Full schema validation | Rate limit, API versioning |

Default target: ASVS Level 2 for all applications handling Confidential or Restricted data. The V9 level cells restate the ASVS progression verbatim; the pack's own transport-security floor is TLS 1.3 at every level, per [`core/cryptography.md`](cryptography.md).

ASVS v5.0.0 reference: `https://owasp.org/www-project-application-security-verification-standard/`

---

## Framework alignment

| OWASP Risk | ISO 27001 | NIST SSDF | CSA CCM |
| --- | --- | --- | --- |
| A01 Access Control | A.5.15 to 5.18 | PW.6 | IAM-04 to 05 |
| A02 Cryptography | A.8.24 | PW.7 | CEK-01 to 21 |
| A03 Injection | A.8.28 | PW.6 | AIS-02 |
| A04 Insecure Design | A.8.25 to 8.27 | PW.1 to PW.4 | AIS-01 |
| A05 Misconfiguration | A.8.9 | PW.9 | CCC-07 |
| A06 Outdated Components | A.8.8 | PO.5, PW.4 | TVM-06 |
| A07 Auth Failures | A.5.17 | N/A | IAM-13 to 15 |
| A08 Integrity | A.8.27 | DS.2 | CCC-04 to 05 |
| A09 Logging | A.8.15 to 8.16 | RV.1 | LOG-01 to 13 |
| A10 SSRF | A.8.28 | PW.6 | AIS-02 |