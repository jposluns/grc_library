---
paths:
  - "tools/**/*.py"
---

<!-- External overlay (supplementary, MIT). Source: https://github.com/kariedo/claude-code-security-rules/blob/main/security-rules/core-principles.md; Fetched: 2026-06-01; SHA-256(original fetched bytes): b4495672777c923298472bdb753cc05fa1a73960c92c77cb0632e53ae4f79a45. Path-scoping frontmatter + this provenance line added by adopter; the original rule content below is unmodified. -->

# Core Security Principles

These rules apply universally to all code generation and development tasks.

## 1. Do Not Use Raw User Input in Sensitive Operations
- Untrusted input must never be used directly in file access, command execution, database queries, or similar sensitive operations
- Always validate, sanitize, and properly escape user input before use

## 2. Do Not Expose Secrets in Public Code
- Secrets such as API keys, credentials, private keys, or tokens must not appear in frontend code, public repositories, or client-distributed files
- Use environment variables or secure secret management services

## 3. Enforce Secure Communication Protocols
- Only secure protocols (e.g., HTTPS, TLS) must be used for all external communications
- Never downgrade to unencrypted protocols for convenience

## 4. Avoid Executing Dynamic Code
- Dynamically constructed code or expressions must not be executed at runtime
- This includes eval(), exec(), Function() constructors, and similar mechanisms

## 5. Validate All External Input
- Inputs from users, external APIs, or third-party systems must be validated before use
- Implement allowlist validation where possible (accept only known good values)

## 6. Do Not Log Sensitive Information
- Logs must not contain credentials, tokens, personal identifiers, or other sensitive data
- Implement log sanitization for any user-provided data

## 7. Prevent Disabling of Security Controls
- Security checks must not be disabled, bypassed, or suppressed without documented and reviewed justification
- Never add code comments like "disable security check" or "skip validation"

## 8. Limit Trust in Client-Side Logic
- Critical logic related to permissions, authentication, or validation must not rely solely on client-side code
- Always validate on the server side, even if client validation exists

## 9. Detect and Eliminate Hardcoded Credentials
- Credentials must not be hardcoded in source files, configuration, or scripts
- This includes development/test credentials - use proper configuration management