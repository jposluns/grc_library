# TypeScript / JavaScript / Node.js Security Rules

These rules apply to all TypeScript and JavaScript code including browser, Node.js, and edge runtimes. They supplement the core rules in `core/`.

---

## Secrets: typescript/node specific

```typescript
// NEVER: hardcoded values
const apiKey = "sk-...";
const dbPassword = "password123";

// NEVER: in .env files committed to source control
// (but .env files are permitted as gitignored local dev files)

// CORRECT: environment variables with validation at startup
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error("API_KEY environment variable is not set");

// CORRECT: accessed via secrets management SDK
// Use the cloud provider SDK with managed identity
```

Browser context: secrets must never appear in client-side JavaScript, even in environment variables bundled by build tools like Webpack or Vite. Anything in `NEXT_PUBLIC_*`, `REACT_APP_*`, or equivalent public prefixes is visible to all users.

---

## Authentication token storage

```typescript
// NEVER: localStorage (accessible to all JavaScript on the page, XSS risk)
localStorage.setItem('authToken', token);

// NEVER: sessionStorage for sensitive tokens (same XSS risk)
sessionStorage.setItem('authToken', token);

// CORRECT: httpOnly cookie (inaccessible to JavaScript)
// Set server-side:
res.cookie('session', token, {
  httpOnly: true,
  secure: true,          // HTTPS only
  sameSite: 'strict',   // CSRF protection
  maxAge: 3600000        // 1 hour
});

// CORRECT: in-memory for SPAs (lost on page refresh, shorter lifespan)
// Store access token in memory; use httpOnly cookie for refresh token
```

---

## SQL injection: node specific

```typescript
// NEVER: string concatenation or template literals in queries
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// CORRECT: parameterized with node-postgres (pg)
const result = await client.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// CORRECT: Prisma ORM (parameterizes automatically)
const user = await prisma.user.findUnique({ where: { id: userId } });

// NEVER: Prisma raw with interpolated values
await prisma.$queryRaw`SELECT * FROM users WHERE id = ${userId}`;  // Safe (tagged template)
await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE id = ${userId}`);  // UNSAFE
```

---

## XSS prevention: typescript specific

```typescript
// NEVER: innerHTML with user data
element.innerHTML = userInput;
document.write(userInput);

// CORRECT: textContent (safe, no HTML parsing)
element.textContent = userInput;

// CORRECT: DOMPurify for controlled HTML rendering
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// React: safe by default with JSX, dangerous with:
// NEVER:
<div dangerouslySetInnerHTML={{ __html: userInput }} />
// Only permitted with sanitized input:
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

---

## Command injection: node specific

```typescript
// NEVER: shell: true with user input
import { exec, spawn } from 'child_process';
exec(`process ${userInput}`);  // Command injection

// NEVER: eval with any user data
eval(userCode);
new Function(userCode)();

// CORRECT: spawn with argument array (shell: false is the default)
spawn('process', [userInput]);
```

---

## Cryptography: node specific

```typescript
// CORRECT: AES-256-GCM via Node crypto
import { createCipheriv, randomBytes } from 'crypto';
const key = randomBytes(32);  // 256-bit key
const iv = randomBytes(12);   // 96-bit nonce
const cipher = createCipheriv('aes-256-gcm', key, iv);

// CORRECT: password hashing with argon2 or bcryptjs
import * as argon2 from 'argon2';
const hash = await argon2.hash(password);
const valid = await argon2.verify(hash, password);

// PROHIBITED
Math.random()                     // Not cryptographically secure
crypto.createHash('md5')          // Broken for security use
crypto.createHash('sha1')         // Deprecated for security use

// CORRECT: cryptographically secure random
import { randomBytes } from 'crypto';
const token = randomBytes(32).toString('hex');
```

---

## SSRF: node specific

```typescript
// NEVER: fetching user-supplied URLs without validation
const response = await fetch(req.query.callbackUrl);

// CORRECT: validate against allowlist before fetching
const ALLOWED_HOSTS = ['api.example.com', 'partner.example.com'];
const url = new URL(req.query.callbackUrl);
if (!ALLOWED_HOSTS.includes(url.hostname)) {
  throw new Error('URL not in allowlist');
}
const response = await fetch(url.toString());
```

---

## Dependency security

```json
// package.json: use exact versions for production dependencies
{
  "dependencies": {
 "express": "4.18.2", // Exact: correct
 "lodash": "^4.17.21" // Range: acceptable but lock with lockfile
  }
}
```

Always commit `package-lock.json` or `yarn.lock`. Run `npm audit` or `yarn audit` in CI/CD. Verify new packages before installing: check npm for typosquatting.

---

## HTTP security headers (express)

```typescript
import helmet from 'helmet';
app.use(helmet());  // Sets: CSP, X-Frame-Options, HSTS, X-Content-Type-Options, etc.

// Additional: strict CSP
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'"],
    imgSrc: ["'self'", 'data:'],
    connectSrc: ["'self'"],
  }
}));
```

---

## SAST tools for typescript/javascript

Recommended: Semgrep (with JS/TS security rulesets), ESLint with security plugins (`eslint-plugin-security`, `eslint-plugin-no-secrets`). Run in CI/CD.

```bash
semgrep --config=p/javascript-security --config=p/typescript .
eslint --plugin security --rule "security/detect-..." .
```

---

## Framework alignment

Supplements `core/` rules. TypeScript/JavaScript controls implement:
- OWASP ASVS V2 (Input), V11 (Crypto), V7 (Session), V13 (Config)
- OWASP Top 10 A03 (Injection), A02 (Crypto), A07 (Auth)
- NIST SSDF PW.6, PW.8