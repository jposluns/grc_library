# Security Requirements for This Project

This file encodes security requirements that apply to all code written, reviewed, or suggested in this Claude Code session. These requirements are not advisory: they are mandatory constraints.

When you write code, check it against these requirements before presenting it. When you review code, flag any violation as a security finding with severity and remediation guidance.

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

For agentic systems, see additional rules in [`ai/agent-security.md`](ai/agent-security.md). 
For MCP servers, see [`ai/mcp-security.md`](ai/mcp-security.md). 
For RAG systems, see [`ai/rag-security.md`](ai/rag-security.md).

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

## Development-governance discipline

When working on a governed codebase (one with CI gates, audit programmes, branch protections, generated artefacts, or a change-tracking convention), apply the rules in `governance/`. The currently-shipped governance rules are:

- [`governance/gate-discipline.md`](governance/gate-discipline.md): never weaken or delete a gate to silence a failure; fix the artefact. Targeted suppressions need a documented rationale on the same line; blanket suppressions are prohibited. Exception path is the project's exception register, not a unilateral suppression.
- [`governance/change-tracking.md`](governance/change-tracking.md): every change to user-visible content carries a CHANGELOG entry by default. The entry records date, version, structured sections (Added/Changed/Removed/Fixed/Security), linked file references, the "why" (not only the "what"), and verification evidence. The opt-out path is a documented `Changelog: skip (reason: ...)` trailer, reviewer-approved; silence is never the answer.
- [`governance/evidence-grounded-completion.md`](governance/evidence-grounded-completion.md): never declare work "done", "fixed", "ready", "shipped", or any synonym, and never assert a factual property of an artefact you have not read (that a file contains, lacks, or requires something), without first running the verification protocol (enumerate files in scope, re-read each in full, quote supporting lines, search for falsifying evidence, distinguish mechanical-gate verification from semantic verification, state unverified items explicitly). The vocabulary of completion, and any state assertion made in research, assessment, planning, or review, are flags that the protocol must precede; the protocol is mechanical so it can be checked without subjective judgement.
- [`governance/clarify-before-acting.md`](governance/clarify-before-acting.md): when a request has more than one reasonable interpretation, or an external value the request does not pin down is required to proceed, surface the ambiguity in one sentence and ask before acting. Use sensible defaults only for choices where a wrong guess is bounded to a quick edit; ask before defaulting for choices with consequences beyond this PR (target branch, public API shape, dependency, breaking change).
- [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md): generated artefacts are read-only (edit the source, run the generator, commit both halves together; CI verifies via `--check` mode); protected branches are append-only (no direct push; no force-push; PR-only merges). The version-monotonicity contract depends on branch protection as its primary defence and the audit as its backstop.
- [`governance/action-before-explanation-of-inaction.md`](governance/action-before-explanation-of-inaction.md): never explain why an external action cannot or will not proceed without first attempting it (when safe and reversible) or naming it and asking (when destructive). The trigger surface is the moment a draft contains "X is blocked / waiting on / requires / would fail" attached to an action not attempted this turn; the protocol is the reversibility gate (classify as safe-or-destructive), then the corresponding action (attempt the safe action and report the real result, or name the destructive action and ask). Execution doubt is resolved by trying; decision doubt remains in the clarify-before-acting rule's scope.

The phased governance rollout announced at pack version 1.6.0 completed at 1.11.0 with the first five rules above. Pack version 1.21.0 added the sixth rule (`action-before-explanation-of-inaction.md`) as a post-rollout extension after a recurring AI-coding-assistant failure mode (narrating reasons to wait instead of attempting the cheap, reversible action that would resolve the doubt) was observed in production sessions.

---

## Framework basis

These requirements implement controls from:
- OWASP Top 10:2025 (eighth edition; supersedes 2021)
- OWASP LLM Top 10
- OWASP MCP Top 10
- OWASP ASVS v5.0.0
- NIST SSDF (SP 800-218 and SP 800-218A: Generative AI Profile)
- CSA CCM v4 / AICM v1
- ISO/IEC 27001:2022 Annex A
- CISA Secure by Design principles
- SLSA (Supply-chain Levels for Software Artifacts)

For detailed requirements, see [`dev-security/standard-developer-security-requirements.md`](../standard-developer-security-requirements.md) in the GRC library.