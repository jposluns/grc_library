# Cryptography Rules

---

## Algorithm selection: use these

| Purpose | Required Algorithm | Prohibited |
| --- | --- | --- |
| Symmetric encryption | AES-256-GCM (authenticated) | DES, 3DES, RC4, Blowfish, AES-ECB |
| Asymmetric encryption | RSA-4096, EC P-256, EC P-384 | RSA < 2048, EC P-192 |
| Key exchange | ECDHE, DHE (DH group ≥ 2048 bits) | Static RSA, DH < 2048 |
| Password hashing | Argon2id (preferred), bcrypt (cost ≥ 12) | MD5, SHA-1, SHA-256 (unsalted), SHA-512 (unsalted) |
| Integrity hashing | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Digital signatures | ECDSA P-256/P-384, RSA-PSS-4096 | RSA-PKCS1v1.5 < 2048, SHA-1 signatures |
| TLS version | TLS 1.3 (or stronger) | SSL 2.0, SSL 3.0, TLS 1.0, TLS 1.1, TLS 1.2 |
| TLS certificate | SHA-256 RSA or ECDSA | SHA-1 signed certificates |
| HMAC | HMAC-SHA-256, HMAC-SHA-384 | HMAC-MD5, HMAC-SHA-1 |

---

## AES modes

- **GCM (Galois/Counter Mode)**: Use this. Provides authenticated encryption: integrity is built in. Required for all new development.
- **CBC**: Permitted only for legacy interoperability where GCM is not possible. Requires a separate HMAC for authentication. Requires unpredictable IVs.
- **ECB**: Prohibited. ECB does not use an IV and reveals data patterns. Never use for any purpose.

---

## Password hashing

Passwords must never be stored as plaintext, encrypted (reversible), or with a general-purpose hash function.

```python
# Correct: Argon2id
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)

# Correct: bcrypt with cost ≥ 12
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Prohibited
hashlib.sha256(password.encode()).hexdigest()   # No salt, fast hash
hashlib.md5(password.encode()).hexdigest()       # Broken
```

---

## Key management

Keys must never be hardcoded in source code, configuration files, or build artefacts. Store keys in the organisation's approved secrets management service.

Key lifecycle requirements:
- **Generate** keys using a cryptographically secure random number generator (CSPRNG): not `random`, not `Math.random()`
- **Store** keys in the approved key vault or HSM: never in code, config, or databases in plaintext
- **Rotate** keys on a defined schedule and on suspected compromise
- **Rotation without downtime**: the application must support reading a new key while decrypting legacy data with the old key
- **Retire** keys that are no longer needed: delete from vault after confirming no data remains encrypted with that key

---

## Initialization vectors (IV) and nonces

- IVs must be randomly generated for each encryption operation using a CSPRNG
- IVs must never be hardcoded or predictable
- IVs must never be reused with the same key (reuse breaks GCM security)
- For GCM: 96-bit (12-byte) IV is recommended; never exceed 2^32 operations per key/IV combination

---

## TLS configuration

When configuring TLS in application code or infrastructure:

```
Minimum version:   TLS 1.3 (TLS 1.2 and earlier prohibited)
Certificate:       SHA-256 RSA or ECDSA; valid from approved CA; not self-signed in production
Cipher suites:     Prefer ECDHE-based forward-secret suites
Validation:        Always validate peer certificates; never disable certificate validation
```

Never set `verify=False`, `ssl.CERT_NONE`, `InsecureSkipVerify: true`, or equivalent in production code.

---

## Random number generation

Use a cryptographically secure random number generator for all security-relevant randomness:

| Language | Secure | Insecure |
| --- | --- | --- |
| Python | `secrets` module, `os.urandom()` | `random` module |
| JavaScript/Node | `crypto.randomBytes()`, `crypto.getRandomValues()` | `Math.random()` |
| C# | `RandomNumberGenerator` (System.Security.Cryptography) | `System.Random` |
| Java | `SecureRandom` | `java.util.Random` |

---

## Post-quantum readiness

Current public-key cryptography (RSA, ECDSA, ECDH) is vulnerable to cryptographically relevant quantum computers. Organisations should:
- Inventory all systems using public-key cryptography
- Prioritize migration for long-lived data and long-lived certificates
- Monitor NIST post-quantum cryptography standardization (ML-KEM, ML-DSA, SLH-DSA)
- Plan for hybrid classical/post-quantum schemes during migration

This is a planning requirement, not an immediate implementation requirement, except for systems with data sensitivity requiring 10+ year protection.

---

## Framework alignment

| Requirement | OWASP ASVS | NIST SP 800-131A | CSA CCM | ISO 27001 |
| --- | --- | --- | --- | --- |
| Algorithm selection | V6.2 | Full document | CEK-01 to 03 | A.8.24 |
| Key management | V6.4 | SP 800-57 | CEK-09 to 21 | A.8.24 |
| Password hashing | V2.4 | N/A | IAM-07 | A.5.17 |
| TLS configuration | V9.1 to V9.3 | SP 800-52 | IVS-09 | A.8.24 |
| Random number generation | V6.3 | N/A | CEK-03 | A.8.24 |