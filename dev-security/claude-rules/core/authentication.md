# Authentication and Session Security Rules

---

## Identity Provider

Never implement custom authentication mechanisms or local user stores. All authentication must flow through the organization's enterprise identity provider (IdP). This applies to:
- Web application logins
- API authentication
- Mobile application authentication
- Service-to-service authentication

## MFA Requirements

Multi-factor authentication is mandatory for all human access. Applications must not provide:
- Password-only authentication paths
- SMS-only recovery flows as the sole second factor (phishing risk)
- "Remember this device for 30 days" options that eliminate the second factor entirely
- Administrative bypass paths that skip MFA

For Tier 0 access (identity systems, PAM, PKI infrastructure): phishing-resistant MFA only: FIDO2 security key or certificate-based authentication.

## Service-to-Service Authentication

| Caller Type | Required Pattern |
| --- | --- |
| Cloud workload to cloud service | Platform managed identity (no credentials in code) |
| On-premises to cloud | OAuth 2.0 client credentials with registered application identity stored in PAM vault |
| Service to service (general) | OAuth 2.0 client credentials flow, not API keys as sole mechanism |
| API gateway calls | OAuth 2.0 validated by IdP at gateway: subscription keys are additive, not primary |

Shared secrets and hardcoded service account passwords are prohibited for service-to-service authentication.

## Session Token Security

```
Minimum entropy:      128 bits
Storage (server):     Invalidated on logout; not reconstruct-able from output
Storage (client):     httpOnly cookies preferred; in-memory if SPA; never localStorage
Timeout:              8 hours absolute; 1 hour for elevated privilege sessions
Transmission:         Never in URLs, query strings, or log output
Refresh tokens:       Rotation on each use; revocable on logout or compromise
```

## Directory Integration

- LDAPS (port 636) only: plain LDAP (port 389) is prohibited
- UPN-based authentication: SAMAccountName-only is prohibited in new code
- Kerberos AES-256: RC4 Kerberos prohibited in new builds
- Service account directory binds must use dedicated service accounts in the PAM vault

## Authentication Error Handling

Authentication failures must return generic error messages to the caller. Do not reveal:
- Whether the username exists
- Whether the password was wrong vs. account locked
- The authentication mechanism details
- Internal system names or paths

Log full error details server-side with correlation ID. Return only a generic failure message with correlation ID to the caller.

## Brute-Force Protection

All login endpoints must implement:
- Account lockout or progressive delay after N failed attempts
- CAPTCHA or equivalent challenge after failed attempts from an IP
- Rate limiting per IP and per account
- Alerting to SIEM on anomalous failed authentication patterns

## Framework Alignment

| Requirement | OWASP ASVS | OWASP Top 10 | CSA CCM | ISO 27001 |
| --- | --- | --- | --- | --- |
| MFA enforcement | V2.1 | A07 | IAM-15 | A.5.17 |
| Session management | V3.1 to V3.5 | A07 | IAM-13 to 14 | A.8.2 |
| Service auth | V2.10 | A07 | IAM-09 | A.5.15 |
| Directory integration | V2.8 | A07 | IAM-01 | A.5.15 |
| Brute force | V2.2 | A07 | IAM-15 | A.8.3 |