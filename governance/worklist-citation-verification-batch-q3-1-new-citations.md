# Citation Verification Worklist - Batch Q3.1: New canonical citations from Phase 23.6

**Document Title:** Citation Verification Worklist: Batch Q3.1 (New Canonical Citations)\
**Document Type:** Worklist\
**Version:** 1.0.1\
**Date:** 2026-05-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-citation-verification-bundle.md`](register-citation-verification-bundle.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** This worklist is a per-batch working artefact; it does not have a recurring review cadence. The authoritative record is the Citation Verifications Register.\
**Repository Path:** [`governance/worklist-citation-verification-batch-q3-1-new-citations.md`](worklist-citation-verification-batch-q3-1-new-citations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

Worklist for batch Q3.1: the 6 truly-new canonical citations added in Phase 23.6 that are not covered by the Q3 tooling-register provenance batch.

Phase 23.6 added 35 new entries to [`governance/register-canonical-citations.md`](register-canonical-citations.md): 26 are AI security tools that overlap with the Q3 tooling-register worklist (the human verifier captures evidence once and satisfies both registrations simultaneously, recorded via cross-reference notes in the master bundle index). The remaining 9 are non-tooling citations split as follows:

- **3 covered by Q3 as overlapping tool/programme entries**: HarmBench (Q3 5.2.8), Meta CyberSecEval (Q3 5.1.12 PurpleLlama bundle), UK AISI inspect_evals (Q3 5.2.18).
- **6 truly new in this Q3.1 worklist**: AVID, MLCommons AILuminate, OWASP GenAI Security Project, OWASP Agentic AI Top 10 2026, OWASP MCP Top 10 2025, NIST SP 800-218A.

---

## 2. How to use this worklist

For each row in §4:

1. Open the **Expected primary URL** in a browser. Confirm the page is served from the publisher's canonical domain under TLS.
2. Locate the page text identifying the standard / framework / programme by name and current version or status. Copy verbatim into **Captured text**.
3. Submit the publisher page to `https://web.archive.org/save/` and record the resulting snapshot URL.
4. Where Tier 2 corroboration is available (e.g., a registry catalogue entry), record in **Secondary URL**.
5. Compare publisher metadata against **Expected value** in the worklist. Note any divergence.
6. Assign **Confidence** per Citation Verification Specification §10.
7. Sign **Captured by**.

At batch close, the AI verifier appends rows to the Citation Verifications Register and proposes any necessary canonical-citations register updates.

---

## 3. Notes on the 6 entries

- **AVID** is a continuously-updated public knowledge base; the publisher page should describe the project rather than identify a single "current version".
- **MLCommons AILuminate** v1.0 was released in 2024; verify the version and publication date on the MLCommons page.
- **OWASP GenAI Security Project** is a working group with continuous output; verify the project's existence and current status on the OWASP page.
- **OWASP Agentic AI Top 10 2026** is a 2026 publication; verify it has been published (status `published` rather than `draft`).
- **OWASP MCP Top 10 2025** is a 2025 publication; same verification check.
- **NIST SP 800-218A** is the Secure SDF GenAI profile; verify "Final" status (vs draft) and 2024 publication date.

---

## 4. Worklist

| Standard ID | Publisher | Expected primary URL | Search fallback URL | Field(s) to verify | Expected value (from register) | Captured text (verbatim) | Wayback URL | Secondary URL | Result | Divergence detail | Captured by | Confidence | Date checked | Recorded into register | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVID | AVID community | `https://avidml.org/` | (search the publisher's site for "AVID AI Vulnerability Database") | all | continuous; 2023; AI Vulnerability Database, open knowledge base of AI failure modes and harms |  |  |  |  |  |  |  |  |  |  |
| MLCommons AILuminate | MLCommons | `https://mlcommons.org/benchmarks/ailuminate/` | (search the publisher site) | all | v1.0; 2024; AI risk taxonomy and benchmark, 14-category hazard taxonomy |  |  |  |  |  |  |  |  |  |  |
| OWASP GenAI Security Project | OWASP | `https://genai.owasp.org/` | `https://owasp.org/www-project-top-10-for-large-language-model-applications/` | existence, current status | continuous; 2024; GenAI security risks, controls, reference test cases |  |  |  |  |  |  |  |  |  |  |
| OWASP Agentic AI Top 10 2026 | OWASP | `https://owasp.org/www-project-agentic-ai-top-10/` | (search the publisher site) | publication status, version | 2026; Top 10 risks for agentic AI systems |  |  |  |  |  |  |  |  |  | Verify status (published / draft / under review). |
| OWASP MCP Top 10 2025 | OWASP | `https://owasp.org/www-project-mcp-top-10/` | (search the publisher site) | publication status, version | 2025; Security risks for Model Context Protocol integrations |  |  |  |  |  |  |  |  |  | Verify status. |
| NIST SP 800-218A | NIST | `https://csrc.nist.gov/pubs/sp/800/218/a/final` | (search the publisher site) | all | Final; 2024; Secure Software Development Practices for Generative AI and Dual-Use Foundation Models |  |  |  |  |  |  |  |  |  |  |

**Total entries in batch: 6.**

The other 26 AI security tooling references added in Phase 23.6 are verified as part of the Q3 batch ([`worklist-citation-verification-batch-q3-ai-tooling.md`](worklist-citation-verification-batch-q3-ai-tooling.md)); see the master verification-bundle index for the overlap mapping.

---

## 5. Closing notes

| Field | Value |
| --- | --- |
| Batch identifier | Q3.1 - New Canonical Citations |
| Standards in batch | 6 |
| Batch opened | 2026-05-30 |
| Batch closed |  |
| Spot-check entries |  |
| Spot-check verifier |  |
| Recorded register rows |  |

---

**End of Document**
