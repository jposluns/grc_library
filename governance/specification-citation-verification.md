# Citation Verification Specification

**Document Title:** Citation Verification Specification\
**Document Type:** Specification\
**Version:** 1.2.0\
**Date:** 2026-05-29\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py), [`specification-ingestion.md`](../specification-ingestion.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to publisher source patterns, AI verifier environmental capabilities, or verification methodology\
**Repository Path:** [`governance/specification-citation-verification.md`](specification-citation-verification.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## 1. Purpose

This specification defines how citations recorded in the Canonical Citations Register ([`register-canonical-citations.md`](register-canonical-citations.md)) are verified against authoritative publisher sources, how verification results are logged in the Citation Verifications Register ([`register-citation-verifications.md`](register-citation-verifications.md)), and how verification confidence is recorded and refreshed.

It exists because the library's audit programme (the twelve automated linters) verifies structural integrity but does not verify factual accuracy. A citation can pass every linter while being factually wrong about a standard's existence, version, or publication date. This specification provides the missing factual control.

---

## 2. Scope

### 2.1 In scope

- Every entry in the Canonical Citations Register.
- New citations added to that register in subsequent phases (each addition triggers verification before the linter trusts it).
- Standards, regulations, frameworks, protocols, and specifications cited by name and version anywhere in the library that map to a register entry.

### 2.2 Out of scope

- The content of standards (we verify the standard exists and has the recorded version; we do not verify the substance of the standard against the library's interpretation).
- Internal cross-references between library documents (covered by `lint-links`).
- Citations to URLs in library content (the library convention is to cite by standard ID, not URL).

---

## 3. Operating model and verifier roles

### 3.1 Why this section exists

This specification was first written assuming a single verifier role with full web access. In practice, verification work is performed across two actors with different capabilities and trust profiles: an AI verifier (the maintainer's AI assistant operating in a sandboxed environment with restricted outbound network access) and a human verifier (the maintainer or a delegated human reviewer with an ordinary browser).

This section codifies the split. It exists not because the AI/human split is a compromise of the methodology, but because honest disclosure of *which actor performed which step* is itself a credibility control. A reader of the Citation Verifications Register must be able to tell, for any row, whether the captured text was taken by a human reading the publisher's page directly or by an AI reading a search snippet. Conflating the two would dilute the trust value of every row.

### 3.2 Verifier roles

| Role | Capabilities | Trust profile |
| --- | --- | --- |
| **Human verifier** (maintainer or delegated reviewer) | Unrestricted browser access; can fetch publisher pages directly under TLS; can submit and retrieve Wayback Machine snapshots. | Bears integrity responsibility for verbatim text capture and confidence rating. The verification of record. |
| **AI verifier** (maintainer's AI assistant) | Operates in a sandboxed environment with restricted outbound network access. Cannot fetch publisher pages directly. Cannot fetch or submit Wayback Machine snapshots. May use Web Search for orientation only. | Performs worklist preparation and clerical recording of human-captured text. Does not perform primary verification. |

### 3.3 AI verifier responsibilities

The AI verifier:

1. **Prepares the per-batch verification worklist**: identifies the publisher canonical URL pattern, the expected catalogue URL for each Standard ID in the batch, the field(s) to be checked, and any known parsing gotchas. Output is a markdown worklist per the worklist template ([`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md)).
2. **Reviews the human verifier's captured text**: confirms the captured text supports the claim the verifier intended to record; flags anomalies (the page text appears to contradict the claim, the text appears to be a summary rather than primary, the URL is not allow-listed).
3. **Records the verification row** in the Citation Verifications Register, faithfully reproducing the human-captured text without summarisation.
4. **Identifies downstream impact**: where a verification finds the register entry should be corrected, the AI verifier identifies the library content that references the corrected entry and proposes the fixes for human approval.
5. **Does not** perform primary verification, claim AI agreement as verification, or summarise publisher text.

### 3.4 Human verifier responsibilities

The human verifier:

1. **Fetches the publisher page** from the URL in the worklist using an ordinary browser under TLS.
2. **Confirms domain identity**: that the page is served by the expected publisher and not a lookalike (URL bar shows expected domain; TLS certificate matches publisher; page chrome matches publisher norms).
3. **Captures verbatim text**: copies the exact publisher-page text that supports (or refutes) the claim being verified. Does not paraphrase.
4. **Submits a Wayback Machine snapshot** of the publisher page on the verification date and records the resulting snapshot URL. Where a snapshot already exists for the verification date, that one is acceptable.
5. **Assigns the confidence rating** per §11 (A, B, C, or D).
6. **Returns the captured artefacts** to the AI verifier for recording, or records them directly in the verifications register. Either way, the `Captured by` field of the resulting row identifies the human verifier as the source.

### 3.5 Environmental constraints disclosure

The following constraints in the AI verifier's environment were observed at the time this specification was first written (2026-05-29). They are recorded here for transparency; future capability changes are tracked by version bump.

- `WebFetch` to publisher canonical domains (iso.org, nist.gov, iec.ch, ietf.org, others tested) returns HTTP 403 Forbidden.
- `WebFetch` to `web.archive.org` is explicitly blocked at the harness level.
- `WebSearch` is available but returns: result titles and URLs (page-derived), result snippets (page-derived but partial), and search-engine summaries (which may be AI-generated and are explicitly not a verification source under §6.4).
- No persistent browser session is available to the AI verifier.

The operating principle is that any capability the AI verifier discovers it lacks is added here on first detection rather than worked around silently. A future AI environment with broader access may collapse some AI/human responsibilities back together; until then, the split in §3.3 and §3.4 stands.

### 3.6 Worklist artefact

Each verification batch produces a worklist as a working artefact. The template is at [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md). The template specifies the columns the AI verifier pre-fills and the columns the human verifier fills.

A worklist is not retained indefinitely after the batch is closed; the authoritative record is the Citation Verifications Register. However, in-flight worklists may be committed to the repository for shared visibility during a multi-session batch.

---

## 4. Why "spot sampling" is not sufficient

An earlier proposal was to sample N citations per phase. That proposal is rejected. For a reference library that is intended to be adopted, partial verification has the wrong failure mode: a citation that is wrong but un-sampled stays wrong, propagates to every adopter, and is invisible to the maintainer because the audit reports "sample clean."

The methodology in this specification verifies **every** entry. The cost is bounded (the register is finite) and the value (a citation register that is verifiable rather than asserted) justifies the cost.

---

## 5. Threat model

The verification process must defend against:

| Threat | Description | Defence |
| --- | --- | --- |
| **Adversarial poisoning** | Content seeded specifically to corrupt AI knowledge or to misrepresent reputable standards. | Publisher-only primary sources; never trust LLM summaries, AI-generated content, or content of unknown provenance. |
| **SEO and content-farm spam** | Automatically generated material with confident-sounding wrong claims. | Restrict verification to a closed allow-list of canonical publisher domains. |
| **Lookalike domains** | Sites mimicking the publisher to mislead readers. | Domain match against the publisher's known canonical domain; TLS verification recorded; human verifier confirms URL-bar and certificate chrome. |
| **AI summarisation drift** | A search-result summary that paraphrases content incorrectly. | Capture the exact text of the publisher page, not a summary. Primary verification is performed by the human verifier (per §3.4), not by an AI reading a search snippet. |
| **Honest staleness** | Outdated mirrors or cached copies. | Prefer the publisher's current catalogue page; record the fetch date. |
| **Publisher silently amending the page later** | Page content changes after verification, making the verification log unreproducible. | Wayback Machine snapshot URL recorded alongside the live URL. |
| **Verifier-side hallucination** | The verifier (whether human or LLM) interprets the publisher page incorrectly. | Captured-text rule (the page's words, not the verifier's paraphrase) plus second-pair-of-eyes spot-check. AI verifier is barred from primary verification (per §3.3). |
| **Single-source dependency** | Only one source on Earth says X; we trust it. | Confidence rating that distinguishes corroborated from single-source-only entries. |
| **Role conflation** | A row in the verifications register is recorded without distinguishing whether the captured text came from a human reading the publisher page or an AI reading a search snippet. | Mandatory `Captured by` field on every row; AI verifier never asserts itself as the captor of primary text. |

---

## 6. Trust tiers and source rules

### 6.1 Trust tiers

| Tier | Source | Use in verification |
| --- | --- | --- |
| **Tier 1: Publisher canonical** | The standard publisher's own canonical domain (see §7 for the allow-list). | The only source that counts as primary verification. |
| **Tier 2: Authoritative secondary** | National standards bodies republishing publisher catalogue metadata (ANSI, BSI, DIN, AFNOR, SIS, CSA Group, etc.); official government catalogues (FedRAMP marketplace, EUR-Lex for EU regulations, Federal Register for US, gazettes for other jurisdictions). | Corroboration only. Cannot replace Tier 1. |
| **Tier 3: Industry-credible secondary** | Reputable professional bodies' summary pages, peer-reviewed academic indexes, government regulator pages summarising third-party standards. | Used only for orientation and triangulation. Not a verification of record. |
| **Untrusted** | Wikipedia, blogs, security-vendor articles, AI-generated summaries, SEO content farms, social media, forums, lookalike domains. | Never cited as verification. May not contribute confidence. |

### 6.2 Publisher-only primary rule

Every register entry must be verified against the publisher's own canonical domain. Where the publisher's standard content is paywalled, the publisher's **catalogue metadata page** (typically free, showing standard ID, title, edition, year, supersedence) is the primary source. We verify the metadata, not the content.

### 6.3 Corroboration rule

Where Tier 2 corroboration is available (a national standards body republishing the same catalogue entry), record it. Where it is not available (newer or sector-specific standards), the entry is marked as single-source.

### 6.4 No mediated verification

The verifier does not ask another LLM, does not consult AI-generated summaries, does not treat their own prior belief as a check. Verification is "publisher page text against our claim", not "search-engine top result agrees with our claim."

### 6.5 Domain match

For each verification, the live URL must match the publisher's known canonical domain (per §7 allow-list). TLS connection state is recorded. Lookalike domains are flagged and not used.

---

## 7. Publisher allow-list

The verification process operates against an explicit allow-list of publisher canonical domains. Additions to the allow-list are recorded in this specification with the date and the standard or family of standards that necessitated the addition.

### 7.1 Initial allow-list

| Publisher | Canonical domain | Standards covered |
| --- | --- | --- |
| ISO | `iso.org` | ISO and ISO/IEC standards. |
| IEC | `iec.ch` | IEC standards (including 62443, 61511, 61508). |
| NIST | `nist.gov`, `csrc.nist.gov`, `nvlpubs.nist.gov` | NIST SP, NIST CSF, NIST AI RMF, NIST FIPS. |
| ASHRAE | `ashrae.org` | ASHRAE 135 (BACnet) and related. |
| NFPA | `nfpa.org` | NFPA 72 and related fire-and-life-safety codes. |
| CEN/CENELEC | `cencenelec.eu`, `cen.eu`, `cenelec.eu` | EN series. |
| IETF | `ietf.org`, `rfc-editor.org`, `datatracker.ietf.org` | RFCs. |
| W3C | `w3.org` | W3C recommendations. |
| OASIS | `oasis-open.org` | OASIS standards. |
| Cloud Security Alliance | `cloudsecurityalliance.org` | CSA CCM, AICM, STAR. |
| ISACA | `isaca.org` | COBIT. |
| MITRE | `attack.mitre.org`, `cve.mitre.org`, `cwe.mitre.org` | ATT&CK, CVE, CWE. |
| NIST FedRAMP | `fedramp.gov` | FedRAMP. |
| US Federal | `federalregister.gov`, `congress.gov`, `whitehouse.gov`, `cisa.gov`, `tsa.gov`, `dhs.gov`, `hhs.gov`, `ftc.gov`, `sec.gov` | US federal regulation and directives. |
| EU | `eur-lex.europa.eu`, `digital-strategy.ec.europa.eu`, `enisa.europa.eu` | EU regulations, directives, ENISA. |
| UK | `legislation.gov.uk`, `ico.org.uk`, `ncsc.gov.uk` | UK regulation and ICO/NCSC. |
| Canada | `laws-lois.justice.gc.ca`, `gazette.gc.ca`, `priv.gc.ca`, `cyber.gc.ca` | Canadian federal regulation and OPC. |
| Quebec | `legisquebec.gouv.qc.ca` | Quebec provincial regulation (Law 25). |
| WCO | `wcoomd.org` | WCO SAFE Framework, AEO, customs. |
| ICAO | `icao.int` | International civil aviation. |
| IMO | `imo.org` | International maritime. |
| BIS | `bis.org` | Basel framework. |
| NERC | `nerc.com` | NERC CIP. |
| AICPA | `aicpa.org`, `aicpa-cima.com` | SOC reporting standards. |
| Brazil | `gov.br`, `planalto.gov.br` | Brazilian federal regulation (LGPD). |
| Singapore | `pdpc.gov.sg` | Singapore PDPA. |
| Australia | `oaic.gov.au` | Australian privacy. |
| Switzerland | `admin.ch`, `edoeb.admin.ch` | Swiss nFADP. |
| China | `npc.gov.cn` | Chinese regulation (PIPL). |
| Saudi Arabia | `sdaia.gov.sa` | Saudi PDPL. |
| Wayback Machine | `web.archive.org` | Third-party snapshot capture (not a primary source; an evidence anchor). |

The allow-list itself is subject to the same verification discipline as register entries: each domain mapping ("publisher P is hosted at domain D") becomes a verifiable claim. Allow-list verifications use the same workflow as standard verifications and are recorded in the Citation Verifications Register with `Standard ID` set to the publisher name and `Verified Field` set to "allow-list domain mapping."

### 7.2 Additions

A standard or regulation cited in the library that is not covered by an allow-list entry triggers a methodology update. The new publisher domain is added to §7.1 in a new revision of this specification, with the date and rationale.

---

## 8. Verification procedure

The procedure below specifies, for each step, which verifier performs it. Steps assigned to the AI verifier are clerical or worklist-preparation tasks. Steps assigned to the human verifier are integrity-bearing tasks.

### 8.1 Pre-verification (AI verifier)

Before any fetch is requested:

1. Identify the standard's publisher and the publisher's canonical domain (per §7).
2. Identify the publisher's catalogue URL pattern (for example, `iso.org/standard/<n>.html` for ISO standards).
3. Read the claim in the canonical citations register that is being verified: Standard ID, current version, publication date, topic, superseded versions.
4. Pre-fill the worklist row per the worklist template: Standard ID, Publisher, Expected primary URL, Field(s) to verify, Expected value (from register).

### 8.2 Fetch (human verifier)

1. Open the publisher's catalogue page from the worklist URL in a browser.
2. Verify the response is from the allow-listed domain (no redirect to a non-allow-listed domain except where the publisher's own subdomain is in the allow-list).
3. Verify TLS is in use (any non-TLS or certificate-warning page is flagged and not used).
4. Capture the page text as it pertains to the claim being verified: standard ID as the publisher writes it, full title, edition, year, supersedence. Capture verbatim.
5. Where available, also capture a corroborating Tier 2 reference (for example, the ANSI catalogue entry for the same standard).
6. Submit a `web.archive.org` snapshot of the publisher page on the verification date. Record the resulting snapshot URL. Where a snapshot already exists for that date, the existing snapshot URL is acceptable.

### 8.3 Compare (human verifier)

1. Compare the publisher's metadata against the register entry field by field.
2. Each divergence is logged: register said X, publisher said Y, source URL, captured snippet.
3. The verifier does not "interpret" the publisher's wording. The wording is captured verbatim; interpretation is a separate downstream step.

### 8.4 Record (AI verifier)

1. The AI verifier reads the human verifier's captured text from the worklist (or accepts it as supplied directly).
2. The AI verifier appends a row to the Citation Verifications Register with the fields defined in §9, faithfully reproducing the captured text.
3. The `Captured by` field is set to identify the human verifier.
4. The AI verifier does not summarise, paraphrase, or "tidy" the captured text.

### 8.5 Reconcile (AI verifier, with human approval)

After a verification batch:

1. Where the publisher's metadata differs from the register, the AI verifier proposes register edits to match the publisher; the human verifier approves each before commit. The prior register value is recorded in the verifications log as superseded.
2. Where a register superseded-versions list is found incomplete, it is updated.
3. Where the register cites a standard that the publisher does not show (does not exist; ID is wrong), the register entry is flagged for removal and downstream library references are searched.
4. Standards-currency linter is rerun. Downstream references to the corrected version are fixed.

### 8.6 Spot-check (human verifier)

After each verification sub-phase, the human verifier (the maintainer or a delegated reviewer who did not perform the original verification in that batch) personally spot-checks at least five entries by opening the recorded URLs and reading the publisher page. The spot-check confirms that the captured text matches what the page currently says. Any divergence stops the methodology and triggers a methodology review.

---

## 9. Citation Verifications Register fields

Each row in the Citation Verifications Register records:

| Field | Description |
| --- | --- |
| Standard ID | Identifier as it appears in the Canonical Citations Register. For allow-list domain-mapping verifications, the publisher name. |
| Verified Field | Which field of the canonical-citations entry was verified (existence / version / publication-date / supersedence / topic / ID format / allow-list domain mapping). For full-row verification, this is "all." |
| Publisher | Publisher name. |
| Primary URL | The publisher's canonical-domain URL fetched. |
| Wayback URL | The web.archive.org snapshot URL captured at verification time. |
| Secondary URL | Optional Tier 2 corroborating URL. |
| Captured text | Verbatim publisher page text supporting the claim. |
| Captured by | Identifier of the human verifier who fetched the page and captured the text (per §3.4). Where this column reads "AI" or any value implying primary capture by AI, the row is invalid and treated as un-verified. |
| Result | Match / Diverged / Not found. |
| Divergence detail | If Diverged: register said X; publisher said Y. |
| Confidence | A (publisher + Tier 2 corroborating), B (publisher only), C (secondary-only, publisher offline or paywalled with no catalogue), D (un-verifiable). |
| Date checked | ISO 8601 date of the verification. |
| Recorded by | Identifier of the verifier who appended the row to the register (typically the AI verifier acting as recorder). |
| Notes | Anything else worth recording. |
| Resolution | For D-rated rows: what was done (corrected / removed / pending). Empty for A, B, C ratings. |

---

## 10. Confidence ratings

| Rating | Definition | Treatment |
| --- | --- | --- |
| A | Publisher primary + at least one Tier 2 corroboration. | Trusted for routine use; re-verify per §12. |
| B | Publisher primary only (no Tier 2 corroboration available). | Trusted; flagged as single-source in the register; re-verify per §12. |
| C | Only Tier 2 or Tier 3 sources available (publisher offline, paywalled with no catalogue page, or otherwise un-fetchable). | Trusted with reduced confidence; the captured text is preserved; the entry remains in the register but the confidence rating is visible. |
| D | Un-verifiable: standard not found at the publisher; no corroborating source; or the publisher-page text materially diverges from the register. | The register entry is flagged for resolution. Either the entry is corrected to match the publisher, or the entry is removed and downstream references rewritten. |

---

## 11. Disposition of D-rated entries

A D-rated entry is one the verifier could not confirm. The library does not silently retain D-rated entries; they are either corrected to a verifiable form or removed.

1. The entry is flagged in the Canonical Citations Register.
2. The maintainer reviews and decides: correction (re-verify under the corrected form) or removal.
3. If removed: the standards-currency linter run identifies downstream library content that referenced the removed standard. Each reference is reviewed and rewritten or removed.
4. The decision and outcome are recorded in the verifications log with a `Resolution` entry.

---

## 12. Verification freshness

Citations age. Standards are revised, superseded, withdrawn, or renumbered. Tooling moves faster than standards; the cadence differs by register.

### 12.1 Canonical Citations Register (12-month cadence)

- Each entry in the Canonical Citations Register is re-verified every 12 months from its last `Date checked`.
- A linter (`lint-citation-verification-freshness`) is added in a subsequent phase. It reads the Citation Verifications Register, computes per-entry age, and flags any entry whose latest verification is older than 12 months.
- Re-verification produces a new row in the verifications log; the prior row is retained as historical evidence.
- Re-verification on demand is also permitted: any change to the canonical-citations register entry, or any external report of a publisher revision, triggers re-verification.

### 12.2 AI Security Tooling Landscape Register (6-month cadence)

Provenance entries in the AI Security Tooling Landscape Register ([`register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md)) use a shorter cadence because tooling versions, capabilities, licenses, and lifecycle status change faster than standards:

- **Active open-source projects**: re-verification every 6 months.
- **Archived or unmaintained projects**: re-verification every 12 months (archive status reconfirmed).
- **Commercial vendor entries**: re-verification every 6 months (vendor product pages change frequently; Wayback snapshot is the integrity anchor).
- **Triggering events forcing immediate re-verification**: project archival, license change, vendor acquisition, major version release with material capability change.

A planned linter (`lint-tooling-provenance-freshness`) reads the tooling register's per-entry Provenance block and flags entries whose latest `Date assessed` is past the cadence above.

---

## 13. Non-deferrable rules

The following rules are not subject to convenience-driven exception:

1. Publisher is the only primary source.
2. Captured text is the publisher's actual words, not a summary.
3. Wayback snapshot URL is recorded for every verification.
4. Human spot-check (at least five entries) follows every verification batch.
5. D-rated entries are resolved, not retained.
6. AI-generated content is never a verification source, regardless of which AI generated it.
7. The verifier's prior belief is not a verification.
8. The AI verifier does not perform primary verification (per §3.3). Primary verification is the human verifier's responsibility (per §3.4). A row whose `Captured by` field implies AI primary capture is invalid.
9. Environmental capability of the AI verifier is disclosed (§3.5), not worked around silently.

---

## 14. Out-of-scope acknowledgements

This specification does not address:

- **Verification of standard content** versus the library's interpretation of it. A standard's text may legitimately be subject to different reasonable interpretations; this specification does not adjudicate. Where the library makes a claim about what a standard requires, that claim is the library's interpretation, not a verified statement of the standard's text.
- **Verification of regulator interpretations**. Where the library characterises a regulator's position, the source is the regulator's published material; the verifier captures that material's text but does not adjudicate regulatory disputes.
- **Translations**. Publishers issuing standards in multiple languages may have non-identical wording across languages. The verifier captures the publisher's English-language page where one exists, and notes where it does not.

---

## 15. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | Annex A.5.9 | Inventory of information and other assets (the canonical citations register is itself an information asset). |
| ISO 9001:2015 | Documented information control | Practice analogue for verifiable, dated, recorded factual claims. |
| Library Charter | [`governance/charter-governance-library.md`](charter-governance-library.md) | Library quality and integrity obligations. |

---

**End of Document**
