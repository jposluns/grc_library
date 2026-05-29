# Citation Verification Specification

**Document Title:** Citation Verification Specification\
**Document Type:** Specification\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py), [`specification-ingestion.md`](../specification-ingestion.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to publisher source patterns or verification methodology\
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

## 3. Why "spot sampling" is not sufficient

An earlier proposal was to sample N citations per phase. That proposal is rejected. For a reference library that is intended to be adopted, partial verification has the wrong failure mode: a citation that is wrong but un-sampled stays wrong, propagates to every adopter, and is invisible to the maintainer because the audit reports "sample clean."

The methodology in this specification verifies **every** entry. The cost is bounded (the register is finite) and the value (a citation register that is verifiable rather than asserted) justifies the cost.

---

## 4. Threat model

The verification process must defend against:

| Threat | Description | Defence |
| --- | --- | --- |
| **Adversarial poisoning** | Content seeded specifically to corrupt AI knowledge or to misrepresent reputable standards. | Publisher-only primary sources; never trust LLM summaries, AI-generated content, or content of unknown provenance. |
| **SEO and content-farm spam** | Automatically generated material with confident-sounding wrong claims. | Restrict verification to a closed allow-list of canonical publisher domains. |
| **Lookalike domains** | Sites mimicking the publisher to mislead readers. | Domain match against the publisher's known canonical domain; TLS verification recorded. |
| **AI summarisation drift** | A search-result summary that paraphrases content incorrectly. | Capture the exact text of the publisher page, not a summary. |
| **Honest staleness** | Outdated mirrors or cached copies. | Prefer the publisher's current catalogue page; record the fetch date. |
| **Publisher silently amending the page later** | Page content changes after verification, making the verification log unreproducible. | Wayback Machine snapshot URL recorded alongside the live URL. |
| **Verifier-side hallucination** | The verifier (whether human or LLM) interprets the publisher page incorrectly. | Captured-text rule (the page's words, not the verifier's paraphrase) plus second-pair-of-eyes spot-check. |
| **Single-source dependency** | Only one source on Earth says X; we trust it. | Confidence rating that distinguishes corroborated from single-source-only entries. |

---

## 5. Trust tiers and source rules

### 5.1 Trust tiers

| Tier | Source | Use in verification |
| --- | --- | --- |
| **Tier 1: Publisher canonical** | The standard publisher's own canonical domain (see §6 for the allow-list). | The only source that counts as primary verification. |
| **Tier 2: Authoritative secondary** | National standards bodies republishing publisher catalogue metadata (ANSI, BSI, DIN, AFNOR, SIS, CSA Group, etc.); official government catalogues (FedRAMP marketplace, EUR-Lex for EU regulations, Federal Register for US, gazettes for other jurisdictions). | Corroboration only. Cannot replace Tier 1. |
| **Tier 3: Industry-credible secondary** | Reputable professional bodies' summary pages, peer-reviewed academic indexes, government regulator pages summarising third-party standards. | Used only for orientation and triangulation. Not a verification of record. |
| **Untrusted** | Wikipedia, blogs, security-vendor articles, AI-generated summaries, SEO content farms, social media, forums, lookalike domains. | Never cited as verification. May not contribute confidence. |

### 5.2 Publisher-only primary rule

Every register entry must be verified against the publisher's own canonical domain. Where the publisher's standard content is paywalled, the publisher's **catalogue metadata page** (typically free, showing standard ID, title, edition, year, supersedence) is the primary source. We verify the metadata, not the content.

### 5.3 Corroboration rule

Where Tier 2 corroboration is available (a national standards body republishing the same catalogue entry), record it. Where it is not available (newer or sector-specific standards), the entry is marked as single-source.

### 5.4 No mediated verification

The verifier does not ask another LLM, does not consult AI-generated summaries, does not treat their own prior belief as a check. Verification is "publisher page text against our claim", not "search-engine top result agrees with our claim."

### 5.5 Domain match

For each verification, the live URL must match the publisher's known canonical domain (per §6 allow-list). TLS connection state is recorded. Lookalike domains are flagged and not used.

---

## 6. Publisher allow-list

The verification process operates against an explicit allow-list of publisher canonical domains. Additions to the allow-list are recorded in this specification with the date and the standard or family of standards that necessitated the addition.

### 6.1 Initial allow-list

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

### 6.2 Additions

A standard or regulation cited in the library that is not covered by an allow-list entry triggers a methodology update. The new publisher domain is added to §6.1 in a new revision of this specification, with the date and rationale.

---

## 7. Verification procedure

### 7.1 Pre-verification

Before fetching any page:

1. Identify the standard's publisher and the publisher's canonical domain (per §6).
2. Identify the publisher's catalogue URL pattern (for example, `iso.org/standard/<n>.html` for ISO standards).
3. Confirm the claim in the canonical citations register that is being verified: Standard ID, current version, publication date, topic, superseded versions.

### 7.2 Fetch

1. Fetch the publisher's catalogue page for the standard.
2. Verify the response is from the allow-listed domain (no redirect to a non-allow-listed domain except where the publisher's own subdomain is in the allow-list).
3. Verify TLS is in use (any non-TLS or certificate-warning page is flagged and not used).
4. Capture the page text as it pertains to the claim being verified: standard ID as the publisher writes it, full title, edition, year, supersedence.
5. Where available, capture a corroborating Tier 2 reference (for example, the ANSI catalogue entry for the same standard).
6. Capture a `web.archive.org` snapshot URL for the publisher page on the verification date. Where no snapshot exists, request one to be created and record the resulting snapshot URL.

### 7.3 Compare

1. Compare the publisher's metadata against the register entry field by field.
2. Each divergence is logged: register said X, publisher said Y, source URL, captured snippet.
3. The verifier does not "interpret" the publisher's wording. The wording is captured verbatim; interpretation is a separate downstream step.

### 7.4 Record

For every entry, a row is appended to the Citation Verifications Register with the fields defined in §8.

### 7.5 Reconcile

After a verification batch:

1. Where the publisher's metadata differs from the register, the register is updated to match the publisher; the prior register value is recorded in the verifications log as superseded.
2. Where a register superseded-versions list is found incomplete, it is updated.
3. Where the register cites a standard that the publisher does not show (does not exist; ID is wrong), the register entry is flagged for removal and downstream library references are searched.
4. Standards-currency linter is rerun. Downstream references to the corrected version are fixed.

### 7.6 Spot-check

After each verification sub-phase, the maintainer (a human) personally spot-checks at least five entries by opening the recorded URLs and reading the publisher page. The spot-check confirms that the verifier's captured text matches what the page currently says. Any divergence stops the methodology and triggers a methodology review.

---

## 8. Citation Verifications Register fields

Each row in the Citation Verifications Register records:

| Field | Description |
| --- | --- |
| Standard ID | Identifier as it appears in the Canonical Citations Register. |
| Verified Field | Which field of the canonical-citations entry was verified (existence / version / publication-date / supersedence / topic / ID format). For full-row verification, this is "all." |
| Publisher | Publisher name. |
| Primary URL | The publisher's canonical-domain URL fetched. |
| Wayback URL | The web.archive.org snapshot URL captured at verification time. |
| Secondary URL | Optional Tier 2 corroborating URL. |
| Captured text | Verbatim publisher page text supporting the claim. |
| Result | Match / Diverged / Not found. |
| Divergence detail | If Diverged: register said X; publisher said Y. |
| Confidence | A (publisher + Tier 2 corroborating), B (publisher only), C (secondary-only, publisher offline or paywalled with no catalogue), D (un-verifiable). |
| Date checked | ISO 8601 date of the verification. |
| Verifier | Identifier of the verifier (role, system identifier, or "maintainer"). |
| Notes | Anything else worth recording. |

---

## 9. Confidence ratings

| Rating | Definition | Treatment |
| --- | --- | --- |
| A | Publisher primary + at least one Tier 2 corroboration. | Trusted for routine use; re-verify per §11. |
| B | Publisher primary only (no Tier 2 corroboration available). | Trusted; flagged as single-source in the register; re-verify per §11. |
| C | Only Tier 2 or Tier 3 sources available (publisher offline, paywalled with no catalogue page, or otherwise un-fetchable). | Trusted with reduced confidence; the captured text is preserved; the entry remains in the register but the confidence rating is visible. |
| D | Un-verifiable: standard not found at the publisher; no corroborating source; or the publisher-page text materially diverges from the register. | The register entry is flagged for resolution. Either the entry is corrected to match the publisher, or the entry is removed and downstream references rewritten. |

---

## 10. Disposition of D-rated entries

A D-rated entry is one the verifier could not confirm. The library does not silently retain D-rated entries; they are either corrected to a verifiable form or removed.

1. The entry is flagged in the Canonical Citations Register.
2. The maintainer reviews and decides: correction (re-verify under the corrected form) or removal.
3. If removed: the standards-currency linter run identifies downstream library content that referenced the removed standard. Each reference is reviewed and rewritten or removed.
4. The decision and outcome are recorded in the verifications log with a `Resolution` entry.

---

## 11. Verification freshness

Citations age. Standards are revised, superseded, withdrawn, or renumbered.

- Each register entry is re-verified every 12 months from its last `Date checked`.
- A linter (`lint-citation-verification-freshness`) is added in a subsequent phase. It reads the Citation Verifications Register, computes per-entry age, and flags any entry whose latest verification is older than 12 months.
- Re-verification produces a new row in the verifications log; the prior row is retained as historical evidence.
- Re-verification on demand is also permitted: any change to the canonical-citations register entry, or any external report of a publisher revision, triggers re-verification.

---

## 12. Non-deferrable rules

The following rules are not subject to convenience-driven exception:

1. Publisher is the only primary source.
2. Captured text is the publisher's actual words, not a summary.
3. Wayback snapshot URL is recorded for every verification.
4. Human spot-check follows every verification batch.
5. D-rated entries are resolved, not retained.
6. AI-generated content is never a verification source, regardless of which AI generated it.
7. The verifier's prior belief is not a verification.

---

## 13. Out-of-scope acknowledgements

This specification does not address:

- **Verification of standard content** versus the library's interpretation of it. A standard's text may legitimately be subject to different reasonable interpretations; this specification does not adjudicate. Where the library makes a claim about what a standard requires, that claim is the library's interpretation, not a verified statement of the standard's text.
- **Verification of regulator interpretations**. Where the library characterises a regulator's position, the source is the regulator's published material; the verifier captures that material's text but does not adjudicate regulatory disputes.
- **Translations**. Publishers issuing standards in multiple languages may have non-identical wording across languages. The verifier captures the publisher's English-language page where one exists, and notes where it does not.

---

## 14. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | Annex A.5.9 | Inventory of information and other assets (the canonical citations register is itself an information asset). |
| ISO 9001:2015 | Documented information control | Practice analogue for verifiable, dated, recorded factual claims. |
| Library Charter | [`governance/charter-governance-library.md`](charter-governance-library.md) | Library quality and integrity obligations. |

---

**End of Document**
