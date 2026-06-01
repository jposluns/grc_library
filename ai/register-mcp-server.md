# Model Context Protocol Server Register

**Document Title:** Model Context Protocol Server Register\
**Document Type:** Register\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/register-model-registry.md`](register-model-registry.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`dev-security/claude-rules/ai/mcp-security.md`](../dev-security/claude-rules/ai/mcp-security.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Quarterly and continuously updated upon server registration, change, or retirement\
**Repository Path:** [`ai/register-mcp-server.md`](register-mcp-server.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register inventories Model Context Protocol (MCP) servers the organisation operates internally, consumes from third parties, or permits AI assistants to invoke. MCP is the canonical pattern for exposing tools, data sources, and capabilities to AI agents; each MCP server is a security boundary that must be governed, monitored, and reviewed.

A populated MCP server register identifies real servers, suppliers, and capabilities and is sensitive operational data; populate, classify, and store internally.

---

## Scope

This register covers:

1. **First-party MCP servers** developed and operated by the organisation.
2. **Third-party MCP servers** consumed from suppliers, whether hosted by the supplier or self-hosted from supplier-published code.
3. **Open-source MCP servers** in production use.
4. **Developer-environment MCP servers** that AI coding assistants connect to during software development.
5. **Customer-deployed MCP servers** the organisation distributes as part of its product (where applicable).

It does not cover ad-hoc experimentation by individual developers; experimental servers are scoped to the developer's environment and do not connect to production data or systems.

---

## Register schema

Each row is one MCP server. Mandatory fields:

| Field | Description |
| --- | --- |
| Server ID | Unique stable identifier |
| Server name | Internal name; not vendor name in the public template |
| Provider | First-party team or third-party supplier |
| Tier | Tier classification (Critical, High, Moderate, Low) per the same scheme as the supplier risk register |
| Hosting | Supplier-hosted, organisation-hosted, developer-workstation-hosted |
| Endpoint | Internal endpoint identifier; private record |
| Protocol version | MCP protocol version supported |
| Authentication | Authentication mechanism (token, mTLS, OAuth, no-auth restricted to local) |
| Encryption in transit | Yes / configurable / no |
| Permitted capabilities | The explicit list of tools, resources, or prompts the server exposes |
| Capability risk classification | Per the agentic development security standard: Read-only Low; Write Low; Write Sensitive; Destructive |
| Required confirmation mode | Per-action, Per-session, Asynchronous approval, None |
| Data scope | What data the server can read, write, or expose |
| Personal data exposure | Yes / no; data categories if yes |
| Identity propagation | How the user-on-whose-behalf identity flows through the server |
| Rate and chain-length limits | Per server limits |
| Cost model | Pricing or cost-per-invocation where applicable |
| Audit logging | Log content and retention |
| Owner role | Role accountable for the server |
| Approving authority | Role that approved the server's use |
| Connected AI systems | AI System Register cross-references |
| Connected models | Model Registry cross-references |
| Connected suppliers | Supplier Risk Register cross-references where applicable |
| Status | Approved-for-use, evaluation, suspended, retired |
| Last security review | Date and outcome |
| Next review due | |
| Restricted uses | Uses for which the server must not be used |
| Customer-facing transparency | Whether the server's role is disclosed in the customer-facing experience |

---

## Approval categories

| Category | Definition | Approval requirement |
| --- | --- | --- |
| Tier 1 Critical | Servers exposing production data, customer data, or destructive capabilities | AI Security Maintainer plus CISO; impact assessment; supplier review where applicable |
| Tier 2 High | Servers exposing internal-sensitive data or write actions within a single system | AI Security Maintainer plus service-owner |
| Tier 3 Moderate | Read-only servers on Confidential data | AI Security Maintainer or delegated reviewer |
| Tier 4 Low | Read-only servers on Public data; developer-environment local servers | Service-owner approval; recorded in the register |

---

## Server-security baseline

Every approved server satisfies:

| Control area | Requirement |
| --- | --- |
| Authentication | Authenticated by default; unauthenticated only where the server is bound to localhost and the user owns the workstation |
| Encryption | TLS for non-local servers; mTLS where Tier 1 |
| Authorisation | The server applies the user-on-whose-behalf authorisation; agent identity alone does not unlock data |
| Input validation | The server validates inputs against the declared schema; rejects out-of-schema requests |
| Output sanitisation | Where the server returns data fed into downstream model context, the data is delimited and identified as untrusted to mitigate indirect prompt injection |
| Rate limiting | Per-client rate limit enforced; chain-length limit where applicable |
| Logging | Per-invocation logging with the user identity, agent identity, tool, arguments (sanitised), outcome |
| Secrets handling | No secrets in server source; secrets accessed from the secrets management service per invocation |
| Supply chain | First-party servers follow the secure development standard; third-party servers follow the AI vendor security questionnaire |
| Vulnerability management | Server software patched on the cadence in the vulnerability management procedure |
| Threat model | Documented threat model per Tier 1 server; reviewed annually |

---

## Operating expectations

1. A server is not connected to a production AI system without an approved register row in status Approved-for-use.
2. Material changes to permitted capabilities (new tool, new data scope, new identity model) trigger a register update and a re-review at the original approval level.
3. Third-party MCP servers acquired or updated are reviewed before each acquisition or version increment.
4. Open-source MCP servers are pinned to a specific version and hash; new versions are reviewed before adoption.
5. Developer-environment local servers are documented; their configuration must not include access to production data unless explicitly approved.
6. Customer-facing AI experiences that use MCP servers are disclosed in the customer-facing privacy notice and the algorithmic transparency register where required.

---

## Coordination with adjacent governance

| Adjacent | Coordination point |
| --- | --- |
| AI access and agent permissions standard | Agent tool allow-list enumerates the MCP servers and their capabilities |
| Agentic development security standard | Server-implementation security baseline |
| Cross-domain coordination procedure | MCP-server-implicated incidents route through the AI incident response plan |
| Supplier security and privacy assurance standard | Third-party MCP server suppliers are governed by the supplier programme |
| Claude-rules MCP security file | First-party MCP servers use the claude-rules [`mcp-security.md`](../dev-security/claude-rules/ai/mcp-security.md) as the development baseline |
| Cost governance standard | MCP server invocation cost feeds the AI cost-governance register |

---

## Operating metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Approved-server coverage | Percentage of MCP servers connected to production AI systems with an Approved-for-use row in this register | 100% |
| Review currency | Percentage of Tier 1 and Tier 2 servers with a review completed in the past 6 months | At least 95% |
| Unauthorised-tool-call rate | Tool invocations rejected at the server boundary as out-of-allow-list per 10 thousand invocations | Trend-monitored; persistent increase triggers a capability-list review |
| Identity propagation coverage | Percentage of tool invocations carrying a verified user-on-whose-behalf identity | 100% for production |
| Server-incident count | MCP-server-related incidents per quarter | Trend-monitored |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| MCP specification | Open standard | Protocol baseline |
| ISO/IEC 42001:2023 | §8 operation | AI management system |
| OWASP LLM Top 10 | LLM06 excessive agency; LLM03 supply chain | Agentic and supply-chain risks |
| MITRE ATLAS | Tool-abuse tactics | Adversarial ML |
| NIST AI RMF | MANAGE | AI risk management |
| NIST SP 800-53 Rev 5 | AC, AU, SI, SR families | Access, audit, integrity, supply chain |
| ISO/IEC 27001:2022 | A.5, A.8, A.5.19 to A.5.22 | Information security baseline including supplier security |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. MCP and the broader agentic ecosystem are rapidly evolving; the register and the security baseline expect to evolve. Adopting organisations validate the current MCP specification, the supplier landscape, and the threat-model assumptions at each review cycle.

---

**End of Document**
