# Input Validation and Output Encoding Rules

---

## Core Principle

All external input is untrusted. Validate before processing. Encode before output. The boundary between trusted and untrusted is the application perimeter — everything that crosses it is untrusted.

---

## Input Validation Requirements

### Validate Everything from Outside the Trust Boundary

- HTTP request parameters (query string, path, headers, cookies, body)
- File uploads (name, content, size, MIME type)
- API request bodies and schema fields
- Data from external APIs and third-party services
- Data from databases where data may have originated externally
- Data from message queues, event streams, and webhooks
- AI/LLM-generated output (treated as untrusted — see ai/ai-security.md)

### Validation Rules

```
Type:    Validate the data type matches expected (string, integer, date, UUID)
Format:  Validate the format matches expected (email regex, date format, UUID pattern)
Length:  Enforce minimum and maximum length on all string inputs
Range:   Enforce minimum and maximum on all numeric inputs
Charset: Restrict character sets where applicable (alphanumeric only for IDs)
```

**Reject invalid input — do not sanitize and continue.** Sanitization is complex, error-prone, and creates a false sense of safety. Return a 400 Bad Request with a generic error message.

### Server-Side Validation is Mandatory

Client-side validation (JavaScript, HTML5 required attributes) is a UX improvement only. It provides zero security. All validation logic must exist server-side. Never skip server-side validation because client-side validation exists.

---

## Injection Prevention

### SQL Injection

**Always** use parameterized queries or prepared statements:

```python
# Correct
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Prohibited — string concatenation
cursor.execute("SELECT * FROM users WHERE id = " + user_id)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

This applies to: SQL; LDAP queries; XPath queries; NoSQL query constructors; search engine query strings.

### Command Injection

Never pass user input to shell commands. If a shell command is unavoidable:
- Use the language's subprocess API with argument lists (not shell=True)
- Allowlist the set of permitted values before constructing the command
- Never use `os.system()`, `exec()`, `eval()` with user input

### Path Traversal

When handling file paths from user input:
- Resolve the canonical path and verify it is within the allowed base directory
- Reject paths containing `../`, `..\\`, or null bytes
- Reject absolute paths unless explicitly required and the full path is validated

---

## Output Encoding

Output encoding must be **context-aware**. The encoding required depends on where the output appears.

| Output Context | Required Encoding |
| --- | --- |
| HTML body content | HTML entity encoding (`&`, `<`, `>`, `"`, `'`) |
| HTML attribute values | HTML attribute encoding |
| JavaScript string context | JavaScript/JSON string encoding |
| URL query parameters | URL percent encoding |
| CSS values | CSS hex encoding for non-alphanumeric characters |
| SQL strings (if not using parameterized) | Database-specific escaping — prefer parameterized |
| Log output containing user data | Strip or escape control characters and newlines |
| HTTP headers | Validate no CR/LF injection |

Use a well-maintained library for output encoding — do not implement encoding functions manually.

---

## File Upload Security

```
1. Validate MIME type by content (magic bytes) — not by file extension alone
2. Validate file size — enforce a maximum before reading content
3. Rename the file — never use the user-supplied filename on the server
4. Store outside the web root — the file must not be directly accessible via URL
5. Scan content — run antivirus/malware scan before processing
6. Never execute — the file must never be executed by the server
7. Serve through an application controller — not directly from the file system
```

---

## API Schema Validation

All API endpoints must validate:
- Request content type header
- Request body against the defined OpenAPI/JSON Schema
- Unknown fields are rejected (not silently ignored)
- Required fields are present
- Field lengths and value ranges
- Request size total (enforce a maximum request body size)

---

## Framework Alignment

| Requirement | OWASP ASVS | OWASP Top 10 | CSA CCM | NIST SSDF |
| --- | --- | --- | --- | --- |
| Input validation | V5.1–V5.3 | A03 | AIS-02 | PW.6 |
| SQL injection | V5.3 | A03 | AIS-02 | PW.6 |
| Command injection | V5.3 | A03 | AIS-02 | PW.6 |
| Output encoding | V5.3 | A03 | AIS-02 | PW.6 |
| File upload | V12.1–V12.3 | A04 | AIS-02 | PW.6 |
