# Python Security Rules

These rules apply to all Python code. They supplement the core rules in `core/`.

---

## Secrets: python specific

```python
# NEVER: hardcoded in code
DATABASE_URL = "postgresql://user:password@host/db"
API_KEY = "sk-..."

# NEVER: environment variables set inline in code
os.environ['SECRET'] = "value"  # Wrong context

# CORRECT: read from environment, validated at startup
import os
api_key = os.environ.get('API_KEY')
if not api_key:
    raise EnvironmentError("API_KEY is not set")

# CORRECT: read from secrets management service
# Use the cloud provider SDK with managed identity
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
secret = client.get_secret("api-key").value
```

`.env` file for local dev: use `python-dotenv` with `load_dotenv()`. Confirm `.env` is in `.gitignore`. Never use production credentials in `.env`.

---

## SQL injection: python specific

```python
# NEVER: string formatting
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)    # % formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")       # f-string
cursor.execute("SELECT * FROM users WHERE id = " + str(user_id)) # concatenation

# CORRECT: parameterized (psycopg2, sqlite3, etc.)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# CORRECT: ORM (SQLAlchemy)
user = session.query(User).filter(User.id == user_id).first()
# Never use text() with f-strings:
# session.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))  # WRONG
```

---

## Command injection: python specific

```python
# NEVER: shell=True with user input
import subprocess
subprocess.run(f"process {user_input}", shell=True)  # Command injection risk
os.system(f"process {user_input}")                   # Prohibited

# CORRECT: argument list, shell=False
subprocess.run(["process", user_input], shell=False, check=True)

# NEVER: eval or exec with user input
eval(user_expression)   # Code injection
exec(user_code)         # Code injection
```

---

## Path handling: python specific

Resolve an untrusted name against a resolved base directory and verify containment before opening it. A string-prefix check or `os.path.join()` alone does not establish containment. Containment of the resolved path is necessary but not sufficient against symlink attacks: the check-then-open sequence is racy whenever any directory in the path (the base or any ancestor) is attacker-writable, because a component can be swapped for a symlink between the check and the open, and `O_NOFOLLOW` rejects only a symlink in the final pathname component. Where the directory tree is not fully trusted, open each component relative to a trusted directory file descriptor with `O_NOFOLLOW` (openat semantics via `os.open(..., dir_fd=...)`) rather than a single `os.open` on the whole path; otherwise ensure that no directory in the resolved path, including all ancestors, is attacker-writable.

```python
from pathlib import Path

BASE_DIR = Path("/app/uploads").resolve()
candidate = (BASE_DIR / untrusted_name).resolve()

if not candidate.is_relative_to(BASE_DIR):  # is_relative_to: Python 3.9+
    raise ValueError("path escapes the allowed base directory")
```

## Temporary files: python specific

Use `tempfile` so that temporary files and directories are created with unpredictable names and safely scoped lifetimes. Never construct a predictable `/tmp` filename or use a check-then-open sequence. (Reopening a `NamedTemporaryFile` by name while it is still open can fail on Windows under the default delete-and-share semantics; where a cross-platform reopen-by-name is required, pass `delete=False` and clean up explicitly, or use the `TemporaryDirectory` form below, which avoids the issue.)

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile() as tmp:
    tmp.write(data)
    tmp.flush()
    process_file(tmp.name)

with tempfile.TemporaryDirectory() as tmpdir:
    path = Path(tmpdir) / "data.bin"
    path.write_bytes(data)
    process_file(path)
```

## URL scheme validation: python specific

Allowlist URL schemes before using a user-provided URL. Outbound web requests use HTTPS unless an explicitly reviewed requirement permits another scheme. Scheme validation does not replace the host, resolved-IP, and redirect controls in `core/owasp.md`.

```python
from urllib.parse import urlsplit

ALLOWED_SCHEMES = {"https"}

def validate_outbound_url(raw: str) -> str:
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("URL scheme is not allowed")
    if not parsed.hostname:
        raise ValueError("URL hostname is required")
    return raw
```

## Cryptography: python specific

```python
# CORRECT: use the cryptography library
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
key = os.urandom(32)  # 256-bit key
iv = os.urandom(12)   # 96-bit nonce
cipher = AESGCM(key)
ciphertext = cipher.encrypt(iv, plaintext, associated_data)

# CORRECT: password hashing with argon2-cffi
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)
ph.verify(hash, password)  # Raises exception on failure

# PROHIBITED
import hashlib
hashlib.md5(password.encode()).hexdigest()    # Broken for passwords
hashlib.sha256(password.encode()).hexdigest() # Not suitable for passwords (fast hash, no salt)

# PROHIBITED: use secrets module, not random, for security tokens
import random
token = random.randbytes(32).hex()  # NOT cryptographically secure

# CORRECT
import secrets
token = secrets.token_hex(32)
```

### Constant-time secret comparisons

Use `hmac.compare_digest()` for attacker-observable equality checks of MACs (including HMAC-based webhook signatures) and secret tokens. It does NOT verify public-key signatures such as ECDSA or RSA-PSS: those require the algorithm's own verify operation over the message, not a byte comparison. Do not use `==` for the equality checks it does cover. Passwords remain subject to the password-hashing library's verification function.

```python
import hmac

if not hmac.compare_digest(provided_signature, expected_signature):
    raise ValueError("invalid signature")
```

---

## Dependency management

```
# requirements.txt: pin ALL versions in production
requests==2.31.0 # Correct: exact version
requests>=2.0 # Prohibited: floating range in production

# Use pip-audit or equivalent for SCA
pip install pip-audit
pip-audit
```

Never install packages using `pip install <name>` without first verifying the package exists in PyPI and is the intended package. Dependency confusion and typosquatting are real supply-chain attacks.

---

## Deserialization

```python
# NEVER: unpickling untrusted data
import pickle
data = pickle.loads(untrusted_bytes)  # Arbitrary code execution risk

# NEVER: yaml.load with untrusted data
import yaml
data = yaml.load(untrusted_string)  # Arbitrary code execution risk

# CORRECT: safe alternatives
import yaml
data = yaml.safe_load(untrusted_string)  # Uses SafeLoader

import json
data = json.loads(untrusted_string) # Safe: no code execution
```

---

## Dynamic imports: python specific

Never pass a user-controlled value directly to `__import__()` or `importlib.import_module()`. Where runtime plugin selection is required, map an external identifier through a fixed allowlist and import only the mapped module name.

```python
import importlib

ALLOWED_PARSERS = {
    "csv": "app.parsers.csv_parser",
    "json": "app.parsers.json_parser",
}

module_name = ALLOWED_PARSERS.get(user_choice)
if module_name is None:
    raise ValueError("parser is not allowed")

parser = importlib.import_module(module_name)
```

## Security-sensitive type comparisons: python specific

Do not use truthiness or cross-type equality to make authentication or authorization decisions. Python treats some distinct values as equal, including `False == 0` and `True == 1`. Validate the exact expected type at the boundary and use explicit sentinel comparisons.

```python
if type(access_granted) is not bool:
    raise TypeError("access_granted must be a boolean")

if access_granted is not True:
    deny_access()

if token is None:
    deny_access()
```

## XML parsing (XXE)

```python
# NEVER: vulnerable XML parsers with external entity processing
from xml.etree import ElementTree as ET
ET.parse(untrusted_xml)  # May be safe by default but verify

# CORRECT: use defusedxml for untrusted XML
import defusedxml.ElementTree as ET
ET.fromstring(untrusted_xml)  # Protects against XXE
```

---

## Flask / django security notes

**Flask:**
- Set `SECRET_KEY` from environment, not hardcoded: used for session signing
- Enable CSRF protection (`flask-wtf` or equivalent)
- Use `flask-talisman` or set security headers manually
- Never set `debug=True` in production

**Django:**
- Never commit `SECRET_KEY` to version control
- Set `DEBUG = False` in production settings
- Use `ALLOWED_HOSTS`: never `['*']` in production
- Enable `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`

---

## SAST tools for python

Recommended: Bandit, Semgrep (with Python security rulesets). Run in CI/CD on every commit to protected branches.

```bash
bandit -r . -l -i
semgrep --config=p/python-security .
```

---

## Framework alignment

Supplements `core/` rules. Python-specific controls implement:
- OWASP ASVS V2 (Input Validation), V11 (Cryptography), V6 (Authentication)
- OWASP Top 10 A05 (Injection), A04 (Cryptographic Failures)
- NIST SSDF PW.6 (Code Reviews), PW.8 (Automated Testing)