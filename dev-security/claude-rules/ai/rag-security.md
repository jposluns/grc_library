# RAG (Retrieval-Augmented Generation) Security Rules

Apply these rules to all code that builds or operates retrieval-augmented generation systems: semantic search over documents, vector database retrieval, hybrid search pipelines, and any system that augments model context with retrieved content.

---

## Core Threat Model for RAG Systems

RAG systems have a unique attack surface: adversarial content in the retrieval corpus can reach the model's context and influence its behaviour (indirect prompt injection). Every document in the corpus is a potential attack vector if it contains adversarial instructions. Treat the retrieval pipeline as a trust boundary.

---

## Document Ingestion Security

Before indexing any document:

- **Classify the document** — apply the organization's data classification scheme to determine who can retrieve it
- **Validate the source** — documents from untrusted sources (user uploads, external URLs, scraped content) require elevated scrutiny
- **Scan for prompt injection payloads** — run content through an injection detector before indexing
- **Strip active content**: scripts, macros, embedded code, and executable content must be removed before indexing
- **Validate file type by content** (magic bytes), not by extension — before conversion and chunking

---

## Authorization on Retrieval

The retrieval layer must enforce the same authorization as the underlying data:

- A user with read access to Confidential documents must not retrieve Restricted documents through the RAG system
- Apply document-level access control to retrieval results — filter results to only those the requesting user is authorized to access
- Do not cache retrieval results across users — per-user retrieval with per-user authorization
- Log all retrieval operations: query, returned document IDs, user identity, session ID

---

## Chunk and Embedding Security

- Do not include metadata that reveals classification or access control details in chunks sent to the model — handle classification enforcement in the retrieval layer, not in the model context
- Do not embed secrets, credentials, or PII in the vector index — strip these before chunking
- If using a third-party embedding model or embedding API, apply the same data residency and data processing agreement requirements as for any other AI service

---

## Indirect Prompt Injection via Retrieved Content

Adversarial documents in the corpus can instruct the model to take unintended actions.

- **Delimit all retrieved content clearly** in the prompt — use explicit delimiters that distinguish retrieved context from user instructions:
  ```
  <retrieved_context>
  [document content here]
  </retrieved_context>
  ```
- **Instruct the model** in the system prompt not to follow instructions found in retrieved content
- **Monitor for anomalous outputs** that suggest the model is acting on retrieved instructions rather than user instructions
- **Test with adversarial documents** — insert documents containing injection payloads into the test corpus and verify the model ignores them

**Recommended**: Use TikiTribe's RAG-specific injection test suite to generate realistic adversarial document payloads and validate retrieval pipeline resilience.

---

## Vector Database Security

- Apply authentication and authorization to all vector database connections
- Do not expose the vector database directly to the internet — access through the application layer only
- Encrypt the vector index at rest using approved encryption (AES-256)
- Enforce network segmentation — the vector database should only be accessible from the RAG application service, not directly from the internet or from development environments
- Implement access logging on the vector database — log all queries, insertions, and deletions

---

## Query Security

- Validate and sanitize user queries before embedding — reject queries that exceed token limits or contain injection payloads
- Implement rate limiting on retrieval queries per user and globally
- Do not include the raw user query in audit logs if it may contain sensitive personal data — log a sanitized or hashed version
- Implement query rewriting carefully — model-rewritten queries can be used to exfiltrate information through the retrieval system

---

## Cross-Tenant Isolation in Multi-Tenant RAG

If the RAG system serves multiple tenants or user groups:

- Enforce strict document namespace separation — tenant A's corpus must not be retrievable by tenant B
- Validate tenant context on every retrieval request — never trust a tenant identifier from the model or the user without server-side validation against the authenticated session
- Audit cross-tenant retrieval attempts — log and alert on any attempt to retrieve documents from a namespace the user is not authorized to access
- Test isolation with adversarial cross-tenant retrieval probes

---

## Data Retention in RAG Systems

- Apply the organization's data retention schedule to the retrieval corpus — documents past their retention date must be deleted from the index
- Implement a deletion pipeline: when a document is deleted from the source system, it must be removed from the vector index within a defined SLA
- Test that deletion is complete — verify that deleted documents are no longer retrievable after removal

---

## Framework Alignment

| Requirement | OWASP LLM Top 10 | MITRE ATLAS | CSA AICM | NIST AI RMF |
| --- | --- | --- | --- | --- |
| Indirect prompt injection | LLM01 | AML.T0051 | TVM-12 | Measure 2.5 |
| Sensitive disclosure via retrieval | LLM02 | AML.T0024 | DSP-05 | Measure 2.7 |
| Retrieval authorization | LLM06, LLM08 | AML.T0048 | IAM-04 | Manage 1.3 |
| Training/corpus poisoning | LLM03, LLM04 | AML.T0020 | DSP-05 | Govern 1.7 |
| Data retention | LLM02 | — | DSP-07 | Manage 2.2 |