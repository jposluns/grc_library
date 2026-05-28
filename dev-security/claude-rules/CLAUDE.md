# Security Requirements for This Project

This file encodes security requirements that apply to all code written, reviewed, or suggested in this Claude Code session. These requirements are not advisory: they are mandatory constraints.

When you write code, check it against these requirements before presenting it. When you review code, flag any violation as a security finding with severity and remediation guidance.

---

## External rule sources: fetch at session start

At the start of each session, use WebFetch to retrieve and apply security rules from these external repositories. They supplement the rules in this file. Fetch each URL and treat the contents as binding constraints alongside the rules below.

**TikiTribe Secure Coding Rules**: primary AI and agentic security rule set:
- `https://raw.githubusercontent.com/TikiTribe/claude-secure-coding-rules/main/rules/_core/ai-security.md`
- `https://raw.githubusercontent.com/TikiTribe/claude-secure-coding-rules/main/rules/_core/agent-security.md`
- `https://raw.githubusercontent.com/TikiTribe/claude-secure-coding-rules/main/rules/_core/mcp-security.md`
- `https://raw.githubusercontent.com/TikiTribe/claude-secure-coding-rules/main/rules/_core/rag-security.md`

**Wiz Secure Rules Files**: baseline rules by language and framework:
- `https://raw.githubusercontent.com/wiz-sec-public/secure-rules-files/main/rules/general.md`
- Fetch additional language-specific files from `https://github.com/wiz-sec-public/secure-rules-files/tree/main/rules` as relevant to this project's stack.

**OWASP Cheat Sheet Series**: fetch the cheat sheet relevant to each security decision point as needed during the session:
- Index: `https://cheatsheetseries.owasp.org/`

If any fetch fails, continue with the rules in this file. The local rules remain binding regardless of external fetch success.

---

## Secrets: absolute rules

**Never** place secrets, credentials, API keys, tokens, passwords, or connection strings in:
- Source code or test code
- Configuration files tracked in version control
- Dockerfiles or container definitions
- CI/CD pipeline definitions
- Log output or error messages
- Environment variable values passed as plain text in container specs

**Always** use:
- Platform secrets management (key vault, secrets manager) via managed identity
- CI/CD platform native secrets mechanisms
- `.env` files that are `.gitignored` for local development only

If you see a hardcoded secret in existing code, treat it as compromised and flag it immediately as a Critical finding.

---

## Authentication: never implement these

- Custom authentication mechanisms or local user stores: always use the enterprise IdP
- MFA bypass paths or fallback authentication without MFA
- SAMAccountName-only authentication: use UPN/SSO
- Plain LDAP binds on port 389: use LDAPS (port 636) only
- Authentication tokens stored in browser `localStorage`: use httpOnly cookies or in-memory
- Service accounts with hard-coded passwords: use managed identity or PAM vault injection
- Shared secrets for service-to-service calls: use OAuth 2.0 client credentials or managed identity

---

## Input validation: non-negotiable

- **Validate all external input server-side**: type, format, length, range. Reject invalid input; do not sanitize and continue.
- **Never build SQL, LDAP, XML, or shell commands by string concatenation**: use parameterized queries, ORMs, or prepared statements
- **Validate file uploads by content** (magic bytes/MIME detection), not by extension. Store outside web root. Scan before processing. Never execute.
- **Context-aware output encoding** for every output context: HTML entity encoding, JSON encoding, URL encoding, SQL quoting

---

## Cryptography: use these, not others

| Purpose | Correct Choice | Prohibited |
| --- | --- | --- |
| Symmetric encryption | AES-256-GCM | DES, 3DES, RC4, Blowfish |
| Asymmetric | RSA-4096, EC P-256/P-384 | RSA < 2048 |
| Key exchange | ECDHE, DHE | Static RSA |
| Integrity hashing | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Password hashing | Argon2id (preferred), bcrypt (cost ≥12) | MD5, SHA-anything (for passwords), plain storage |
| TLS | TLS 1.3 (preferred), TLS 1.2 (minimum) | SSL, TLS 1.0, TLS 1.1 |
| Certificates | SHA-256 RSA or ECDSA | SHA-1 |

Never hardcode keys. Keys go in the secrets management service.

---

## Authorization

- Enforce all authorization server-side on every request: never rely on client-side claims
- Default deny: deny unless explicitly granted
- RBAC decisions on every call: no implicit allow from previous calls
- API responses must not include data the caller is not authorized to receive
- Never trust request parameters (IDs, roles, tenant identifiers) without server-side validation against the authenticated identity

---

## Logging and error handling

**Never log**: passwords, tokens, session keys, payment data, full PII records, encryption keys

**Always log**: authentication events (success and failure), authorization decisions, all access to Confidential/Restricted data, significant configuration changes, all API calls (caller, endpoint, response code, timestamp)

**Error responses to callers**: generic message + correlation ID only. Full error details (stack traces, system names, paths, schema details) go to server-side logs only.

---

## CORS

Wildcard CORS origins (`Access-Control-Allow-Origin: *`) are prohibited in production APIs, web apps, and HTTP-triggered services. Use an explicit allow-list of permitted origins stored in configuration.

---

## AI and LLM-specific requirements

When writing code that calls LLMs, builds AI applications, or processes AI-generated content:

- **Treat all LLM output as untrusted user input**: validate and sanitize before use in any downstream operation
- **Never pass LLM output directly to**: shell commands, SQL queries, file system operations, or other tool calls without validation
- **Implement prompt injection defenses**: do not concatenate user input directly into system prompts; use separate message roles; validate instructions in retrieved content before acting on them
- **Rate-limit all AI endpoints**: LLM calls are expensive and can be abused for data exfiltration
- **Log all AI inputs and outputs** to SIEM for anomaly detection
- **Require human confirmation** before writing to operational data based on AI decisions
- **Do not send Confidential or Restricted data to external AI APIs** without a data processing agreement and explicit approval

For agentic systems, see additional rules in `ai/agent-security.md`. 
For MCP servers, see `ai/mcp-security.md`. 
For RAG systems, see `ai/rag-security.md`.

---

## Dependencies and third-party code

- Verify that AI-suggested dependency names **actually exist** in the package registry before using them: hallucinated package names are a real supply-chain attack vector
- Prefer dependencies with: active maintenance (last release within 24 months); compatible licence (Apache 2.0, MIT, BSD generally safe; GPL/AGPL require Legal approval for commercial use); no known Critical/High CVEs
- Never install a package from an unverified source or non-standard registry
- Review transitive dependencies in SCA output

---

## Data handling

- Apply minimum data collection: only collect what is needed for the stated purpose
- Do not copy production data to development or test environments: use data masking or synthetic data
- Implement data retention logic in application code: delete or anonymize at end of retention period
- Log files must not contain unmasked personal data (PII, payment data, credentials)

---

## Framework basis

These requirements implement controls from:
- OWASP Top 10 (2021/2025)
- OWASP LLM Top 10
- OWASP MCP Top 10
- OWASP ASVS v5.0.0
- NIST SSDF (SP 800-218 and SP 800-218A: Generative AI Profile)
- CSA CCM v4 / AICM v1
- ISO/IEC 27001:2022 Annex A
- CISA Secure by Design principles
- SLSA (Supply-chain Levels for Software Artifacts)

For detailed requirements, see [`dev-security/standard-developer-security-requirements.md`](../standard-developer-security-requirements.md) in the GRC library.