# Secrets Management Rules

These rules apply to all code in all languages. There are no exceptions without explicit CIO/CISO approval.

---

## Absolute Prohibitions

Never place the following in source code, config files tracked in version control, Dockerfiles, CI/CD definitions, log output, or error messages:

- Passwords and passphrases
- API keys and API tokens
- OAuth client secrets
- Database connection strings containing credentials
- Private keys (RSA, EC, PGP)
- TLS/SSL private key material
- JWT signing secrets
- Webhook signing secrets
- SMTP credentials
- Cloud provider access keys and secret access keys
- Service account JSON credential files
- Session tokens
- Encryption keys and initialization vectors

---

## Required Approach by Context

| Context | Store Secrets Here |
| --- | --- |
| Cloud workloads | Platform secrets management service (key vault) accessed via managed identity — no credential required in code |
| On-premises applications | PAM vault with credential injection at runtime — the application never knows the credential value |
| CI/CD pipelines | CI/CD platform native secrets (masked variables, secrets manager integration) — never in pipeline YAML |
| Local development | `.env` file that is listed in `.gitignore`. Confirm `.gitignore` exists before creating `.env`. |
| Workflow automation | Platform-native secrets references. Never in workflow definition files tracked in source control. |
| API gateway configuration | Secrets-management-backed named values. Never plain text in gateway policy definitions. |

---

## Secret Detection in Code Review

When reviewing code, flag any of the following patterns as a **Critical security finding**:

```python
# Prohibited patterns (any language equivalent)
password = "actual_password_here"
api_key = "sk-..."
token = "ghp_..."
secret = "xxxxxxxxxxxxxxxx"
conn_str = "Server=...;Password=..."
private_key = "-----BEGIN RSA PRIVATE KEY-----"
```

Treat discovered secrets as **compromised immediately**, regardless of whether the code is in production. The secret must be rotated before any other remediation step.

---

## Secret Rotation Design Requirement

Secret rotation must not require a code deployment. If rotating a secret requires:
- A code change
- A build
- A deployment pipeline execution

Then the secrets management design is wrong. Fix the design.

Correct pattern: read the secret from the secrets management service at startup or request time. The secret reference in code points to a location in the vault, not to the secret value.

---

## Git History

Secrets committed to git history remain exposed even after the offending commit is removed from the HEAD. If a secret is found in git history:
1. Rotate the secret immediately — assume it is compromised.
2. Use `git filter-repo` or an equivalent tool to purge the secret from history.
3. Force-push the purged history to all remotes.
4. Invalidate all existing clones — notify all repository contributors.

Secret scanning tools must be configured to scan all historical commits, not just new commits.

---

## `.env` File Rules

`.env` files for local development are permitted under these conditions:
1. The file is listed in `.gitignore` — verify this before creating the file.
2. The file contains only development/test credentials, never production credentials.
3. The file is never committed — configure pre-commit hooks to block `.env` commits.
4. A `.env.example` file with placeholder values (not real values) may be committed as documentation.

---

## Framework Alignment

| Requirement | OWASP ASVS | OWASP Top 10 | NIST SSDF | CSA CCM |
| --- | --- | --- | --- | --- |
| No hardcoded secrets | V2.10 | A07 | PW.8.2 | CEK-10–21 |
| Secret rotation without deployment | V2.10 | A07 | — | CEK-17 |
| Secret scanning in CI/CD | V2.10 | A07 | PW.8 | CCC-07 |