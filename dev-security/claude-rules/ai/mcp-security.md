# Model Context Protocol (MCP) Security Rules

Apply these rules to all code that builds, operates, or consumes MCP servers. MCP servers expose tools and resources to AI models: their security posture directly determines what an AI agent can and cannot do.

---

## MCP server authentication and authorization

- **All MCP servers must require authentication**: no unauthenticated tool endpoints
- Implement per-tool authorization: not every caller with access to the server should be able to call every tool
- Use OAuth 2.0 or equivalent for MCP server authentication where the protocol supports it
- Validate the caller's identity and authorization on **every tool call**, not just at connection time
- Implement scopes or roles for tool access: high-risk tools (write, delete, execute) require elevated scope

---

## Tool exposure minimization

- Expose **only the tools necessary** for the specific agent or use case: do not expose a general-purpose tool set
- Do not expose tools that provide shell access, arbitrary file system access, or arbitrary network access unless specifically required and tightly scoped
- Review the full tool list from the model's perspective: if the model can use a combination of tools to perform an unintended privileged action, that is a security vulnerability
- Implement tool-level audit logging: log every tool call with caller identity, arguments, and result

---

## Input validation on tool arguments

MCP tool handlers must validate all input from the model before acting on it:

- Validate argument types, ranges, and formats against the tool's defined schema
- Reject tool calls with unexpected or out-of-range arguments: do not attempt to sanitize and continue
- Validate file paths: reject path traversal attempts (`../`), absolute paths outside the intended scope, and symlinks to sensitive directories
- Validate identifiers (resource IDs, user IDs, account IDs) against a list of values the calling user is authorized to access: do not trust model-provided IDs without server-side authorization check
- Apply rate limits per tool, per calling agent, and globally

---

## Preventing tool-call injection

Tool-call injection occurs when adversarial content in the environment causes the model to make tool calls the user did not intend.

- **Sanitize document and resource content** before including it in MCP resource responses: strip content that could carry instruction-like patterns
- **Validate tool call arguments** for injection payloads: check string arguments for command injection, SQL injection, path traversal
- **Do not allow tool results to modify tool definitions or available tool sets** at runtime
- Log and alert on unusual tool-call patterns: rapid-fire calls, calls with boundary-case arguments, calls to sensitive tools from unexpected sessions

**Recommended testing**: TikiTribe provides MCP-specific exploit payloads and fuzzing utilities for tool-call injection, privilege escalation through tool composition, and resource handler injection.

---

## Resource handler security

MCP resource handlers expose data to the model. Treat them as APIs:

- Apply authorization to all resource URIs: validate that the caller is allowed to access the requested resource
- Implement URI validation: reject malformed URIs, path traversal, and out-of-scope resource references
- Do not expose internal configuration, credentials, or system state as resources
- Implement content-type validation: return only the expected data type for each resource
- Rate-limit resource reads per session

---

## Transport security

- MCP servers must use TLS 1.3 (or stronger) for all transport
- Validate TLS certificates: do not use `verify=False` or equivalent in MCP clients
- Do not expose MCP servers on public networks without an authentication gateway in front

---

## Tool result sanitization

Tool results returned to the model are part of the model's context and can carry prompt injection payloads:

- Sanitize tool results that originate from external data sources (databases, files, web responses, API calls)
- Mark tool results as "data" not "instructions" using clear delimiters in the prompt structure
- Log tool results that contain suspicious instruction-like patterns for security review

---

## Privileged MCP operations

Some MCP tools may execute privileged operations (database writes, system configuration, external API calls). For these tools:

- Require a separate elevated authorization scope
- Implement a confirmation step: the tool should present what it is about to do and require explicit human approval before executing
- Implement idempotency or dry-run mode where possible: allow the model to preview an operation before committing it
- Implement hard transaction limits (e.g., maximum rows affected, maximum financial value) that cannot be exceeded regardless of model instruction

---

## MCP server lifecycle and inventory

- Maintain an inventory of all MCP servers in production, including: server name and version, tools exposed, authorization model, data accessed, owning team
- Review the tool inventory quarterly: decommission tools no longer in use
- Apply the same vulnerability management process to MCP servers as to other production services (patch, scan, penetration test)

---

## Adversarial testing

Before deploying any MCP server to production, conduct:

| Test | Description |
| --- | --- |
| Tool-call injection | Craft tool arguments designed to exploit handler logic |
| Path traversal | Test file-handling tools with `../` and absolute path arguments |
| SQL injection via tool arguments | If tools query a database, test string arguments for injection |
| Authorization bypass | Test whether a caller with tool access can access resources beyond their authorization |
| Tool composition attacks | Test whether combining multiple tools allows unintended privileged operations |
| Resource injection | Inject prompt injection payloads into resource content and verify they are not acted on |

**TikiTribe** provides MCP-specific attack payloads and test harnesses. Run TikiTribe's MCP exploit suite as part of pre-production security testing.

---

## Framework alignment

| Requirement | OWASP LLM Top 10 | MITRE ATLAS | CSA AICM | NIST AI RMF |
| --- | --- | --- | --- | --- |
| Tool authentication | LLM06 | AML.T0048 | IAM-04 | Govern 1.4 |
| Tool-call injection | LLM01, LLM06 | AML.T0051 | TVM-12 | Measure 2.5 |
| Input validation | LLM06 | N/A | AIS-02 | Manage 1.3 |
| Transport security | N/A |: | I&S-09 | N/A |
| Privileged operations | LLM06 | AML.T0054 | GVN-05 | Govern 6.2 |
| Resource authorization | LLM06, LLM08 | AML.T0048 | IAM-05 | Manage 1.3 |