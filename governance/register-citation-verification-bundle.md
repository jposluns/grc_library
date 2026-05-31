# Citation Verification Bundle Index

**Document Title:** Citation Verification Bundle Index\
**Document Type:** Register\
**Version:** 1.0.1\
**Date:** 2026-05-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md), [`governance/worklist-citation-verification-batch-q2-iso-iec.md`](worklist-citation-verification-batch-q2-iso-iec.md), [`governance/worklist-citation-verification-batch-q3-ai-tooling.md`](worklist-citation-verification-batch-q3-ai-tooling.md), [`governance/worklist-citation-verification-batch-q3-1-new-citations.md`](worklist-citation-verification-batch-q3-1-new-citations.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Per-campaign; updated when new verification batches are queued or completed\
**Repository Path:** [`governance/register-citation-verification-bundle.md`](register-citation-verification-bundle.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This index consolidates the four pending citation verification batches (Q2, Q3, Q3.1, Q4) into a single navigable bundle. It exists so the human verifier can execute the verification campaign in one focused session (typically over a few days) without losing context between batches.

The bundle covers everything in the library that requires human-verifier confirmation per the [Citation Verification Specification](specification-citation-verification.md): existing canonical citations from earlier phases, the Phase 23.7 tooling-register provenance, and the Phase 23.6 new canonical citations.

---

## 2. Bundle scope

| Batch | Worklist file | Entries | Purpose |
| --- | --- | --- | --- |
| **Q2** | [`worklist-citation-verification-batch-q2-iso-iec.md`](worklist-citation-verification-batch-q2-iso-iec.md) | 24 | ISO and ISO/IEC standards in the canonical citations register |
| **Q3** | [`worklist-citation-verification-batch-q3-ai-tooling.md`](worklist-citation-verification-batch-q3-ai-tooling.md) | 55 | AI Security Tooling Landscape Register per-entry Provenance blocks |
| **Q3.1** | [`worklist-citation-verification-batch-q3-1-new-citations.md`](worklist-citation-verification-batch-q3-1-new-citations.md) | 6 | New canonical citations added in Phase 23.6 that do not overlap Q3 |
| **Q4** | [`worklist-citation-verification-batch-q4-canonical-citations.md`](worklist-citation-verification-batch-q4-canonical-citations.md) | 82 | Remaining canonical citations register entries (NIST, EU, North American, sector-specific, OWASP, customs/trade, OECD, ICAO/IMO, CSA, ISACA, MITRE, AICPA, jurisdiction-specific privacy regulations) |

**Total unique entries to verify: ~167.** (Three Phase-23.6 citations - HarmBench, Meta CyberSecEval, UK AISI inspect_evals - overlap Q3 tool entries; their verification work is performed once and recorded against both registers.)

---

## 3. Recommended execution order

The order minimises context-switching between publisher types and lets the human verifier build momentum on similar sources before moving to the next category.

1. **Day 1 - Q2 ISO/IEC** (24 entries). All entries share the `iso.org` publisher; the URL pattern is consistent. The human verifier learns the ISO catalogue navigation pattern once and reuses it across all 24 rows.
2. **Day 2 - Q3.1 truly new citations** (6 entries). Small batch; covers AVID, MLCommons, OWASP, NIST. Different publishers per entry but each is straightforward.
3. **Days 3-4 - Q3 tooling-register provenance** (55 entries). Most are GitHub repositories; the verification pattern is "view the repo, copy commit SHA, submit Wayback snapshot". Six commercial vendor entries follow a slightly different pattern (web pages instead of repos).
4. **Days 5-7 - Q4 remaining canonical citations** (82 entries). Largest batch; spans NIST publications, EU regulations, North American regulations, other privacy regulations, OWASP, customs/trade, OECD, ICAO/IMO, CSA, ISACA, MITRE adversary frameworks, AICPA, jurisdiction-specific privacy. Publishers vary per entry; the human verifier moves between catalogue sites (csrc.nist.gov, eur-lex.europa.eu, etc.) and reads the URL pattern per row.

**Optional optimisation**: while running Q3, the human verifier can ALSO record the canonical-citations register verification for the overlapping entries (see §5 below) to avoid having to revisit the same publishers later.

---

## 4. Per-batch quick reference

### 4.1 Q2 - ISO and ISO/IEC

- **Publisher**: ISO at `iso.org` (catalogue metadata pages).
- **Common URL pattern**: `https://www.iso.org/standard/<publication-id>.html`
- **Six entries flagged for particular attention** (per Q2 worklist §3.6): ISO/IEC 42005, ISO/IEC 42006, ISO 37001, ISO/IEC 38500, ISO/IEC 5259, ISO/IEC 27033. AI verifier's training-time confidence is lowest on these.
- **Output**: 24 rows in the verifications register; canonical-citations updates where divergence found.

### 4.2 Q3 - AI Security Tooling Landscape Register

- **Publishers**: 49 GitHub repositories + 6 commercial vendor product pages.
- **Common URL pattern**: `https://github.com/<owner>/<repo>` for OSS; vendor product page URLs as recorded in the Provenance blocks.
- **Integrity anchor**: commit SHA of default branch (GitHub) or SHA-256 of captured page content (web).
- **Output**: 55 verifications register rows; Provenance block updates for each tooling-register entry (Integrity anchor and Wayback URL filled in; Verification status transitions to `human-verified`).

### 4.3 Q3.1 - New canonical citations (non-overlapping)

- **Publishers**: AVID, MLCommons, OWASP, NIST.
- **Common URL pattern**: varies per publisher; URLs in the worklist.
- **Output**: 6 verifications register rows; canonical-citations register updates where divergence found.

### 4.4 Q4 - Remaining canonical citations

- **Publishers**: NIST (csrc.nist.gov), EU (eur-lex.europa.eu), various national / sector regulators, OWASP, OECD, ICAO/IMO, CSA, ISACA, MITRE, AICPA, jurisdiction-specific privacy regulators.
- **URL patterns**: vary per publisher. Each worklist row carries the expected primary URL; where the URL is unknown the row instructs the verifier to search the publisher's site.
- **Output**: ~82 verifications register rows; canonical-citations register updates where divergence found.
- **Note**: this is the largest batch and spans the broadest set of publishers. Pacing across 3-5 days is realistic.

---

## 5. Overlap mapping (Q3 ↔ canonical-citations register)

The Phase 23.6 canonical citations register additions in the AI security tooling references section all overlap Q3 tooling-register entries. When the human verifier processes Q3 for one of these tools, they simultaneously verify the canonical-citations register entry for the same tool. To avoid double-recording, the table below maps each canonical-citations register entry to its Q3 row.

| Canonical citations register entry | Q3 worklist section ID | Tool |
| --- | --- | --- |
| Trusted-AI ART | 5.2.9 | ART (Adversarial Robustness Toolbox) |
| IBM HEART | 5.2.10 | IBM HEART |
| AIJack | 5.2.16 | AIJack |
| HarmBench framework | 5.2.8 | HarmBench |
| Meta PurpleLlama | 5.1.12 | PurpleLlama bundle (incl. Llama Guard, CyberSecEval, Code Shield) |
| NVIDIA NeMo Guardrails | 5.1.6 | NeMo Guardrails |
| Guardrails AI | 5.1.7 | Guardrails AI |
| Protect AI llm-guard | 5.1.2 | llm-guard |
| Protect AI rebuff | 5.1.3 | rebuff (archived) |
| Protect AI modelscan | 5.3.1 | modelscan |
| picklescan | 5.3.2 | picklescan |
| Trail of Bits fickling | 5.3.3 | fickling |
| Giskard | 5.2.13 | Giskard |
| Confident AI deepteam | 5.2.4 | deepteam |
| promptfoo | 5.2.1 | promptfoo |
| NVIDIA garak | 5.2.2 | garak |
| Microsoft PyRIT | 5.2.3 | PyRIT |
| ETH Zurich AgentDojo | 5.2.7 | AgentDojo |
| Vigil-LLM | 5.1.8 | Vigil-LLM (archived) |
| Stacklok CodeGate | 5.1.9 | CodeGate (archived) |
| ClawGuard | 5.1.4 | ClawGuard |
| Lasso MCP Gateway | 5.5.1 | Lasso MCP Gateway |
| jackhhao llm-warden | 5.1.10 | LLM Warden |
| TikiTribe claude-secure-coding-rules | 5.6.1 | TikiTribe |
| Wiz secure-rules-files | 5.6.2 | Wiz |
| Kariedo claude-code-security-rules | 5.6.3 | Kariedo |
| awesome-ai-security | 5.9.1 | awesome-ai-security |
| UK AISI inspect_evals | 5.2.18 | UK AISI inspect_evals |
| Meta CyberSecEval | 5.1.12 | PurpleLlama bundle (CyberSecEval is one component of the bundle row at 5.1.12) |

For each overlap entry: the verification evidence captured during Q3 (commit SHA, Wayback URL, captured text) satisfies the canonical-citations register verification at the same time. The AI verifier records two rows in the verifications register: one with `Standard ID` = tooling-register section ID (e.g., `5.2.9`), one with `Standard ID` = canonical-citations register entry name (e.g., `Trusted-AI ART`).

Note: the canonical citations register has separate entries for HarmBench and Meta CyberSecEval (in addition to the rows now in the table above). Verify once during Q3, record under both Standard IDs.

---

## 6. Workflow per verification session

Recommended workflow for the human verifier:

1. **Open the bundle index** ([this file](register-citation-verification-bundle.md)) to see batches and execution order.
2. **Open the worklist for the current batch** (e.g., [Q2 worklist](worklist-citation-verification-batch-q2-iso-iec.md)).
3. **For each row**:
   1. Open the Expected primary URL in a browser.
   2. Capture the verbatim publisher text into the worklist row.
   3. Submit the page to web.archive.org/save and paste the snapshot URL.
   4. For GitHub entries, copy the commit SHA of the default branch from the repo page.
   5. Compare against the Expected value. Note any divergence.
   6. Assign Confidence (A/B/C/D per Citation Verification Specification §10).
   7. Sign the row with your identifier.
4. **At end of session**, save the worklist and notify the AI verifier (via chat or commit). The AI verifier appends rows to the Citation Verifications Register, updates the canonical citations register (where divergence found), and updates the tooling register's Provenance blocks (for Q3 entries).

---

## 7. Tools and resources

- **Wayback Machine submission**: `https://web.archive.org/save/<publisher-url>`. Wait for the snapshot to complete; record the resulting URL.
- **GitHub commit SHA capture**: from the repo page, the latest commit on the default branch is shown at the top of the file listing. Copy the full 40-character SHA.
- **Web page content hash**: for commercial vendor pages, save the page HTML and compute SHA-256 (e.g., `curl -L <url> | shasum -a 256`).
- **Spot-check buddy**: at end of each batch, the human verifier (or a delegated reviewer) spot-checks 5+ rows from that batch by re-opening the URLs and confirming the captured text still matches the live page. This is the spot-check requirement defined in [`specification-citation-verification.md`](specification-citation-verification.md) §8.6.

---

## 8. Post-bundle status update

When all four batches are complete, the following library state updates apply:

- **[`register-citation-verifications.md`](register-citation-verifications.md)**: ~85 new rows.
- **[`register-canonical-citations.md`](register-canonical-citations.md)**: corrections applied where divergence was found.
- **[`register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md)**: 55 Provenance blocks transitioned from `AI-captured-pending-human-verification` to `human-verified`.
- **`lint-citation-verification-freshness.py`** engages with real entries (currently passes vacuously).
- **`lint-tooling-provenance-freshness.py`** transitions from "55 entries within window" to "55 entries human-verified within window".

The three worklist files can be retained for evidence or archived; the authoritative records are the registers.

---

## 9. After the bundle

With Q4 included in this bundle, the campaign covers the entire canonical citations register (162 entries) plus the AI Security Tooling Landscape Register's 55 Provenance blocks. No further verification batches are queued at the time of writing.

Subsequent work would be re-verification at the 12-month cadence (canonical citations) or 6-month cadence (active tooling provenance) per the Citation Verification Specification §12. The corresponding freshness linters ([`tools/lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py) and [`tools/lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py)) will engage when an entry crosses its cadence threshold.

---

**End of Document**
