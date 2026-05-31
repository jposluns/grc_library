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
token = random.token_hex(32)  # NOT cryptographically secure

# CORRECT
import secrets
token = secrets.token_hex(32)
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
- OWASP ASVS V5 (Input Validation), V6 (Cryptography), V2 (Authentication)
- OWASP Top 10 A03 (Injection), A02 (Cryptographic Failures)
- NIST SSDF PW.6 (Code Reviews), PW.8 (Automated Testing)