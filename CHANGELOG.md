# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5. The changelog records phase-level changes, not per-document version bumps.

## Phase 23.19 (2026-05-30, Library Version 2026.05.35): Intra-document section reference audit

Second Tier 2 linter. Adds [`tools/lint-intra-doc-refs.py`](tools/lint-intra-doc-refs.py), the 20th linter. Validates that intra-document references like "§5.4" or "Section 11.3" resolve to a real heading in the same document.

### What the linter does

- Extracts numeric section identifiers from headings of the form `## N. Title`, `### N.N Title`, `#### N.N.N Title`, `## Section N: title`.
- Finds intra-document references of the form `§N`, `§N.N`, `§N.N.N`, `Section N`, `Section N.N`, `Section N.N.N` in the document body.
- Skips references in cross-document contexts (heuristic): preceded by `.md`, `](`, doctype words like "Standard"/"Procedure"/"Specification", or framework-mapping table rows containing ISO/NIST/OWASP/COBIT/etc. keywords.
- Fails if a remaining reference's identifier doesn't match a heading in the same document.

### Why it exists

A control referencing "per §5.1.2" is unenforceable if §5.1.2 was removed or renumbered. Caught Phase 23.4 manually; should be caught automatically going forward.

### Source-content adjustment

One table cell in [`governance/register-ai-security-tooling-landscape.md`](governance/register-ai-security-tooling-landscape.md) referenced "§20" in a way that the linter could not disambiguate (no doctype word on the line). Updated to read "AI agentic dev security standard §20" for clarity and to satisfy the linter's cross-doc detection.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 20 gates.

### Verification

Positive case: 331 files scanned, all intra-doc refs resolve. Negative case: synthetic file with broken §5 reference correctly fails.

### Library version

`2026.05.34` to `2026.05.35`. README `1.7.27` to `1.7.28`.

All 20 audits clean.

## Phase 23.18 (2026-05-30, Library Version 2026.05.34): Section anchor reference audit

First Tier 2 linter (structural coherence). Adds [`tools/lint-section-anchors.py`](tools/lint-section-anchors.py), the 19th linter. Validates that markdown links of the form `[text](path#anchor)` resolve to a real heading in the target file.

### What the linter does

Parses all markdown links in artefact documents. For each link containing a `#anchor`:

1. Resolves the link target (same-document anchors use the current file; cross-document anchors use the relative path).
2. Reads the target file and extracts all headings (h1-h6).
3. Slugifies each heading per GitHub-flavoured markdown rules: lowercase, spaces → hyphens, strip non-alphanumeric (except hyphens, underscores), collapse consecutive hyphens.
4. Fails if the `#anchor` does not match any heading slug in the target.

Skips external links (http/https/mailto) and links to files that don't exist (already caught by [`lint-links.py`](tools/lint-links.py)).

### Why it exists

The existing [`lint-links.py`](tools/lint-links.py) checks that the target file exists but not the section anchor. Section renumbers or heading rewrites silently break navigation. Phase 23.4 renumbered §33 → §34 — that was caught only because I checked manually. With this linter, future renumber-without-update would fail at PR time.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 19 gates.

### Verification

Positive case: 333 files scanned, 35 `#anchor` links all resolve. Negative case: synthetic file with `#nonexistent-section` correctly fails with "no heading slugifies to #nonexistent-section".

### Library version

`2026.05.33` to `2026.05.34`. README `1.7.26` to `1.7.27`.

All 19 audits clean.

## Phase 23.17 (2026-05-30, Library Version 2026.05.33): Stub document audit

Tier 1 linter (final in tier) from the audit-roadmap. Adds [`tools/lint-stub-documents.py`](tools/lint-stub-documents.py), the 18th linter in the audit suite. Catches stub documents masquerading as production library content.

### What the linter does

Counts substantive words in document body (after metadata block, excluding code blocks). Flags documents under the threshold (currently 100 words) or containing stub-indicator phrases like `[content to be added]`, `[to be defined]`, `details forthcoming`, `to be completed in a later phase`.

Exemptions:
- Templates, worklists (legitimately short with placeholder content).
- Domain READMEs, [`NOTICE.md`](NOTICE.md), [`AUTHORS.md`](AUTHORS.md), [`CITATION.cff`](CITATION.cff) (indexes / short by design).
- Documents marked `Classification: Deprecated` (deliberate short redirect notices).

### Why it exists

Catches abandoned stubs and "[to be added]" placeholders that escape into production. Closes the gap between "the file exists" and "the file is substantive."

### Tier 1 complete

This is the fifth and final Tier 1 linter (placeholder, monotonicity, date format, license consistency, stub documents). Library audit suite has grown from 12 to 18 gates across phases 23.12 through 23.17.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 18 gates.

### Verification

Positive case: linter passes on 284 scanned files (the deprecated annex was exempted via `Classification: Deprecated` rule, not via filename exemption). Negative case: synthetic 6-word stub correctly fails.

### Library version

`2026.05.32` to `2026.05.33`. README `1.7.25` to `1.7.26`.

### Next

Phase 23.18 begins Tier 2 (structural coherence). First: section anchor validator.

All 18 audits clean.

## Phase 23.16 (2026-05-30, Library Version 2026.05.32): License consistency audit

Tier 1 linter from the audit-roadmap. Adds [`tools/lint-license-consistency.py`](tools/lint-license-consistency.py), the 17th linter in the audit suite. Enforces that every artefact document's `**License:**` field is exactly `CC0 1.0 Universal`.

### What the linter does

Parses every line beginning with `**License:**` across all markdown files. Strips the CommonMark hard-break backslash. Fails on any value that differs from the canonical `CC0 1.0 Universal`.

Catches drift like `CC0-1.0`, `CC0 1.0`, `Creative Commons Zero`, `Public Domain`.

Exempts [`NOTICE.md`](NOTICE.md), which deliberately qualifies its License field ("CC0 1.0 Universal for original repository content only") to distinguish the library's CC0 dedication from external materials referenced by name. The exemption is documented in the linter source.

### Why it exists

The library's CC0 dedication is a legal commitment. License-claim drift weakens the commitment. Currently [`lint-metadata.py`](tools/lint-metadata.py) validates the field is present; this linter validates the value is canonical.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 17 gates.

### Verification

Positive case: linter passes on 332 scanned files. Negative case: synthetic metadata with `CC0-1.0` correctly fails.

### Library version

`2026.05.31` to `2026.05.32`. README `1.7.24` to `1.7.25`.

All 17 audits clean.

## Phase 23.15 (2026-05-30, Library Version 2026.05.31): Metadata date format audit

Tier 1 linter from the audit-roadmap. Adds [`tools/lint-date-format.py`](tools/lint-date-format.py), the 16th linter in the audit suite. Enforces ISO 8601 (YYYY-MM-DD) format for `**Date:**` metadata fields across all artefact markdown files.

### What the linter does

Parses every line beginning with `**Date:**` in every markdown file. Strips CommonMark hard-break backslash. Validates the value:

- Must match `YYYY-MM-DD` pattern.
- Year must be in range 1900-2100.
- Must be a real calendar date (rejects `2026-02-30`, `2026-13-01`).
- Must have zero-padded month and day (rejects `2026-5-30`, `2026-05-3`).

Exempts the literal placeholder values `YYYY-MM-DD` and `<YYYY-MM-DD>` (which appear in example/template metadata blocks documenting the expected format).

Scope deliberately limited to metadata `Date:` fields. Does not enforce ISO format for inline dates in prose (which would produce false positives on legitimate phrasings like "the EU AI Act 2024").

### Why it exists

Machine-parseable dates enable downstream tooling (review-cadence tracking, age-based reporting). The existing metadata linter validates presence but not parseability.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 16 gates.

### Verification

Positive case: linter passes on 333 scanned files. Negative case: synthetic metadata with `30/05/2026` correctly fails with "not ISO 8601 YYYY-MM-DD" finding.

### Library version

`2026.05.30` to `2026.05.31`. README `1.7.23` to `1.7.24`.

All 16 audits clean.

## Phase 23.14 (2026-05-30, Library Version 2026.05.30): Library and document version monotonicity audit

Tier 1 linter from the audit-roadmap. Adds [`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py), the 15th linter in the audit suite. Enforces that the library's CalVer in [`README.md`](README.md) and per-document SemVer in metadata never decrease relative to the prior committed state.

### What the linter does

Compares the working tree's versions against `origin/main` (when on a feature branch) or `HEAD~1` (when on main or when origin/main is unavailable). Returns failure if any version went backwards:

- **Library CalVer**: parses `**Library Version:** YYYY.MM.patch` from [`README.md`](README.md) at both states; fails if current is strictly less than prior.
- **Per-document SemVer**: parses `**Version:** x.y.z` from every artefact markdown file at both states; fails if any document's version decreased on a change that committed.

Skip cases:
- [`README.md`](README.md) — covered by the library check.
- [`CHANGELOG.md`](CHANGELOG.md) — no version metadata field.
- Files that didn't exist at the prior ref (new files; no comparison possible).

### Why it exists

CalVer is meaningful only if it can't go backwards. Forgetting to bump on a content change, or accidentally rewriting an older value, would silently corrupt the version sequence. The linter prevents either error from reaching main.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 15 gates.

### Verification

Linter passes on current state (CalVer 2026.05.29 ≥ 2026.05.28). Parser logic verified against synthetic regression case (2026.05.05 < 2026.05.10 correctly detected).

### Library version

`2026.05.29` to `2026.05.30`. README `1.7.22` to `1.7.23`.

All 15 audits clean.

## Phase 23.13 (2026-05-30, Library Version 2026.05.29): Placeholder leakage detector

Tier 1 linter from the audit-roadmap. Adds [`tools/lint-placeholder-leakage.py`](tools/lint-placeholder-leakage.py), the 14th linter in the audit suite. Catches `TODO`, `TBD`, `FIXME`, `XXX`, `<YYYY-MM-DD>`-style placeholder markers, `(placeholder)`, `[Unverified]`, and "Coming soon" in production library documents.

### What the linter does

Scans all `.md` files in the repo for placeholder markers. Templates, worklists, the [`TODO.md`](TODO.md) file itself, files describing the placeholder patterns (specifications, language linter, this linter source), the coverage-gaps register (which uses `TODO P5.x` as cross-references to priorities), the decision tree (which references both), and the `claude-rules` directory (code-syntax placeholders) are exempt by design.

Detects each pattern via word-boundary regex; reports per-line findings with the matched marker label. Skips fenced code blocks. Returns exit code 1 on findings.

### Why it exists

A library that ships with `TODO: define threshold` in a security control is one adopter compliance failure away from reputational damage. The existing [`lint-shall-near-uncertainty.py`](tools/lint-shall-near-uncertainty.py) catches these only when adjacent to a mandatory verb. This linter catches them anywhere outside the exempt set.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml). Audit suite is now 14 gates.

### Verification

Linter passes on current library (284 files scanned, 0 findings). Negative-case test (synthetic file with `TODO: fix this`) correctly fails.

### Library version

`2026.05.28` to `2026.05.29`. README `1.7.21` to `1.7.22`.

All 14 audits clean.

## Phase 23.12 (2026-05-30, Library Version 2026.05.28): CHANGELOG link enforcement linter

Adds [`tools/lint-changelog-link-coverage.py`](tools/lint-changelog-link-coverage.py), the 13th linter in the audit suite. Enforces that every backtick-wrapped file reference in [`CHANGELOG.md`](CHANGELOG.md) is wrapped in a markdown link, locking in the navigation convention established in Phase 23.11.

### What the linter does

For [`CHANGELOG.md`](CHANGELOG.md):

- Walks the file outside fenced code blocks (code-block examples are excluded).
- Identifies backtick-wrapped strings that look like file paths: containing a directory separator and ending in a recognized extension (.md, .py, .yaml, .yml, .json, .txt, .cff, .toml), or matching a known top-level filename (README, NOTICE, LICENSE, etc.).
- Flags every such reference that is NOT already wrapped in a markdown link.
- Returns exit code 1 with per-line findings on failure; exit code 0 on success.

### CI integration

Added to [`.github/workflows/quality.yml`](.github/workflows/quality.yml) as a new gate after the review-cadence check and before the taxonomy / portal sync checks. The library's audit suite now has 13 gates running on every push to main and every pull request.

### What this phase does NOT include

- The linter is scoped to [`CHANGELOG.md`](CHANGELOG.md). It does not enforce link-coverage across the whole library. Other documents already use markdown links by convention, validated by `lint-links`; the CHANGELOG was the gap.
- No retroactive enforcement on prior CHANGELOG entries (already done in Phase 23.11).

### Library version

`2026.05.27` to `2026.05.28`. README `1.7.20` to `1.7.21`.

### Next

Companion advisory (this turn) covers additional linter rules that would improve consistency, credibility, and security of the library. The maintainer chooses which to implement.

All 13 audits clean.

## Phase 23.11 (2026-05-30, Library Version 2026.05.27): CHANGELOG file references converted to clickable links

Maintenance phase. Converts every backtick-wrapped file reference in [`CHANGELOG.md`](CHANGELOG.md) to a markdown link, making it navigable to the referenced file from any GitHub or markdown-rendering interface.

### Why this update exists

Earlier phases recorded file references in [`CHANGELOG.md`](CHANGELOG.md) as code-formatted text (backticks only). A reader wanting to navigate from a CHANGELOG entry to the referenced file had to copy the path and paste it elsewhere. The reference was visible but not actionable. This phase makes every file reference in the CHANGELOG a one-click navigation.

### What was changed

- Every backtick-wrapped path with at least one directory separator (`ai/...`, `governance/...`, `tools/...`, etc.) converted from `` `path` `` to `` [`path`](path) ``.
- Bare filenames (no directory prefix) resolved against the repository file tree and linked to their actual paths. 328 unambiguous bare-filename references were resolved automatically; one ambiguous reference remained code-formatted (the underlying ambiguity will be handled if the reference is ever made specific).
- The dotfile [`.pre-commit-config.yaml`](.pre-commit-config.yaml) was linked manually (file-system traversal skipped it by default).

Total file references now linked in [`CHANGELOG.md`](CHANGELOG.md): 414. All 12 audits pass; the link linter validated that every new link resolves to an existing file.

### What this phase does NOT include

- No content changes to any phase entry. Wording is preserved exactly; only the markdown formatting changed.
- No linter rule added to enforce this going forward. A future maintenance pass could add a CHANGELOG-link linter; for now the link linter catches broken links in CHANGELOG content the same way it catches broken links in any other markdown file.

### Library version

`2026.05.26` to `2026.05.27`. README `1.7.19` to `1.7.20`.

### Next

No further phase queued. The Phase 23 sequence and the Phase Q-track verification queues stand as previously described.

All 12 audits clean.

## Phase 23.10 (2026-05-30, Library Version 2026.05.26): Tooling-register provenance and time-bounding

Addresses a credibility concern raised after Phase 23.9: the AI Security Tooling Landscape Register asserted capabilities for 55 projects without recording when each project was assessed or how a future reader could verify what was assessed. Phase 23.10 adds a per-entry Provenance block to every entry with traceability anchors, and extends the Citation Verification Specification to govern the tooling register's re-verification cadence.

### Why this update exists

The tooling register (created Phase 23.7) recorded project scope, license, library reference status, capabilities, and GRC concerns surfaced. It did not record:

- The URL each claim came from.
- The date each project was assessed.
- Which project version or branch state was reflected in the recorded capabilities.
- Any integrity anchor (commit SHA, content hash) for the assessed state.
- Any third-party-attested record (Wayback snapshot URL) for the assessed state.

Without these, a reader in 2027 cannot tell whether an entry reflects the project as it existed at registration or as it has evolved. The user raised this concern; this phase addresses it.

### What was added

#### Per-entry Provenance block (55 entries)

Each entry now carries a six-field Provenance block:

- **Source URL**: canonical project URL captured at assessment (GitHub repository for OSS, vendor product page for commercial). AI-captured.
- **Version at assessment**: release tag, version string, or "default branch HEAD" recorded at assessment. AI-captured.
- **Date assessed**: ISO 8601 date the Wave 1 or Wave 2 agent fetched the source. AI-captured (2026-05-30 for all current entries).
- **Integrity anchor**: commit SHA (GitHub) or SHA-256 of captured page content (web). **Human-pending** (the AI verifier records "pending human verification"; the human verifier fills this from the live source).
- **Wayback snapshot URL**: `web.archive.org` snapshot of the source URL at assessment date. **Human-pending** (web.archive.org is blocked in the AI sandbox).
- **Verification status**: `AI-captured-pending-human-verification` (all current entries), `human-verified` (terminal state after human verification), or `re-verification-due` (past the cadence).

#### Schema description update

The register's §3 (How to read this register) now describes the Provenance block with full field semantics and explains why each field exists.

#### Re-verification cadence

The register's §7 (Maintenance) now specifies:

- Active open-source projects: 6 months.
- Archived or unmaintained projects: 12 months.
- Commercial vendor entries: 6 months.
- Triggering events forcing immediate re-verification: project archival, license change, vendor acquisition, major version release with material capability change.

Status transition rules are codified explicitly.

#### Citation Verification Specification update

[`specification-citation-verification.md`](governance/specification-citation-verification.md) §12 (Verification freshness) restructured into 12.1 (Canonical Citations Register, 12-month cadence) and 12.2 (AI Security Tooling Landscape Register, 6-month cadence). The tooling register's shorter cadence reflects that tooling versions, capabilities, licenses, and lifecycle status change faster than standards.

#### New worklist

[`governance/worklist-citation-verification-batch-q3-ai-tooling.md`](governance/worklist-citation-verification-batch-q3-ai-tooling.md) (Worklist doctype, v1.0.0) created with all 55 entries pre-filled with the AI-captured fields. Human verifier fills the Captured commit SHA / page SHA-256, Wayback snapshot URL, Captured by, Verification status, and Date checked columns.

#### Planned linter

A linter ([`tools/lint-tooling-provenance-freshness.py`](tools/lint-tooling-provenance-freshness.py)) is planned to flag entries whose latest `Date assessed` is past the cadence. The Citation Verification Specification §12 documents the planned linter. Implementation is queued and is not blocking for this phase.

### Honest constraint

The AI verifier (this assistant) cannot complete provenance verification because:

- `web.archive.org` is blocked at the harness level.
- Commit SHA capture against a live source requires authoritative-source access the AI verifier does not have.
- The methodology bars AI from primary verification by design.

All 55 current Provenance blocks are therefore marked `AI-captured-pending-human-verification`. The Q3 worklist is the handoff artefact for human verification. The register's claims do not become "verified" until the human verifier completes the worklist; at that point each entry's `Verification status` transitions to `human-verified`.

### Cross-references updated

- [`governance/register-ai-security-tooling-landscape.md`](governance/register-ai-security-tooling-landscape.md) (1.0.0 to 1.1.0): 55 Provenance blocks injected; §3 schema description updated; §7 maintenance section now specifies cadence and status transitions.
- [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md) (1.1.0 to 1.2.0): §12 restructured into 12.1 (citations, 12-month) and 12.2 (tooling, 6-month).
- [`governance/worklist-citation-verification-batch-q3-ai-tooling.md`](governance/worklist-citation-verification-batch-q3-ai-tooling.md) (v1.0.0, new): 55-entry worklist.
- [`governance/README.md`](governance/README.md) (1.7.0 to 1.8.0): worklist added.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.3 to 1.27.4): worklist indexed; tooling-register index entry updated with provenance reference.
- Main README (Library 2026.05.25 to 2026.05.26; README 1.7.18 to 1.7.19).

### Library version

`2026.05.25` to `2026.05.26`. README `1.7.18` to `1.7.19`.

### Next

When human verification capacity is available, the Q3 worklist can be executed. The Q2 worklist (24 ISO/IEC citation verifications) remains in queue from earlier; the maintainer chooses whether to run Q2 or Q3 first.

All 12 audits clean.

## Phase 23.9 (2026-05-30, Library Version 2026.05.25): AI-driven offensive security tooling governance

Final phase of the Phase 23 sequence from the external-project assessment. Adds a new §33 to [`standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) codifying governance for AI-driven offensive security agents (PentestGPT, PentAGI, Strix, HexStrike AI, BurpGPT, and equivalents). The existing §33 "Verification and enforcement" renumbers to §34 (additive, no internal cross-references affected).

### Why this section exists

AI-driven penetration testing and offensive security agents are a category that did not exist when the prior AI security standard was first written. They straddle two existing governance regimes:

- The Penetration Testing and Red Team Standard ([`security/standard-penetration-testing-and-red-team.md`](security/standard-penetration-testing-and-red-team.md)) governs the offensive activity.
- The agent-permissions and agentic-security controls in this standard govern the agent itself.

Neither regime alone is sufficient for AI-driven offensive tools, which carry the threat surface of both. Wave 2 research surfaced seven concrete examples (PentestGPT, PentAGI, AI-OPS, HackSynth, HexStrike AI, BurpGPT, Strix), with diverse autonomy levels, CI/CD integration patterns, and vendor data-handling postures.

### New controls (§33, 10 controls)

- **OFFAI-SEC-01**: Authorisation under the Penetration Testing and Red Team Standard required before any use. Unauthorised use = security testing incident.
- **OFFAI-SEC-02**: AI-driven offensive tools are agents; library's agent permission model takes precedence over vendor's assumed autonomy.
- **OFFAI-SEC-03**: CI/CD-integrated AI-driven offensive tools (Strix-pattern) execute under dedicated service identities with PAM-vaulted credentials.
- **OFFAI-SEC-04**: Auditable evidence of every action; SIEM forwarding.
- **OFFAI-SEC-05**: Vendor telemetry and data residency posture must satisfy the regulatory regime of in-scope targets and data.
- **OFFAI-SEC-06**: Vendor-claimed metrics treated as marketing-grade unless backed by reproducible academic benchmarks (the PentestGPT XBOW pattern vs the HexStrike vendor-claimed pattern).
- **OFFAI-SEC-07**: LLM-driven planning subject to prompt-injection threat model. Sandbox isolation per §32; plan validation per action against engagement scope.
- **OFFAI-SEC-08**: AI-driven findings subject to same triage as human-driven findings. Characteristic AI failure modes (hallucinated vulnerabilities, misidentified target systems, fabricated proof-of-concept artefacts) require operator verification.
- **OFFAI-SEC-09**: Tool autonomous mode must not bypass §24 human-approval gates.
- **OFFAI-SEC-10**: Licence review per open-source licence policy. AGPLv3 / GPL-3.0 tools restricted for embedding; permissive licences preferred (the HackSynth AGPLv3 caution surfaced in Wave 2).

### Numbering note

The previous §33 "Verification and enforcement" renumbers to §34. No internal cross-references reference these section numbers, so the renumber is safe; no downstream library document is affected.

### What this phase does NOT include

- No new tools cited beyond what's already in the canonical citations register and tooling landscape register.
- No new doctype; controls live in the existing standard.

### Cross-references updated

- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) (1.6.0 to 1.7.0): new §33; previous §33 renumbered to §34.
- Main README (Library 2026.05.24 to 2026.05.25; README 1.7.17 to 1.7.18).

### Library version

`2026.05.24` to `2026.05.25`. README `1.7.17` to `1.7.18`.

### Phase 23 sequence status

Phase 23 sequence complete. Final delivery summary:

- 23.0 — collapsed (no current references needed correction)
- 23.1 — Runtime input/output processing controls (AI-SEC-INP-06 through 09, AI-SEC-OUT-05 / 06)
- 23.2 — Dev-side AI input/output scanning controls
- 23.3 — ML model file scanning (SUPPLY-SEC-07)
- 23.4 — Agentic, RAG, MCP, multimodal threat expansion (TC-12 through 16; AGENT-SEC-15 / 16 / 17; RAG-SEC-10 / 11 / 12; MCP-SEC-08 / 09 / 10; RUNTIME-SEC-07 / 08)
- 23.5 — Classical ML adversarial taxonomy (§5 restructured into 6 subsections)
- 23.6 — Framework alignment citations (35+ new register entries)
- 23.7 — AI Security Tooling Landscape Register (55 entries, the post-research master index)
- 23.8 — AI observability OSS reference architecture (OBS-SEC-03 / 04)
- 23.9 — AI-driven offensive security tooling governance (§33, OFFAI-SEC-01 through 10)

Total: 9 merged PRs (#63 through #71). Total new controls and threat classes: 47. New register: 1. New citations queued for verification: 35+.

### Next

The Phase 23 sequence is complete. Subsequent work depends on user direction:

- Resume Phase Q2 citation verification (35+ new citations from Phase 23.6 are queued).
- Or proceed with other tracks pending in the project roadmap.

All 12 audits clean.

## Phase 23.8 (2026-05-30, Library Version 2026.05.24): AI observability OSS reference architecture

Eighth content phase from the external-project assessment. Adds two new controls to [`standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) §20 (AI observability and telemetry) referencing open-source AI observability platforms as concrete reference architectures.

### Why these controls exist

The prior §20 codified what AI telemetry should be captured (per-event field requirements and destinations) and that PII must be masked. It did not articulate the capability requirements of the observability tooling itself, nor reference OSS platforms that implement the pattern. Wave 2 research surfaced LangSmith, Langfuse, Phoenix, and Helicone as the main open-source AI observability platforms. They share a structural pattern (OpenTelemetry / OpenInference tracing, evaluator integration, prompt versioning, data-masking hooks) that organisations adopting library content need codified.

### New controls

- **OBS-SEC-03**: AI observability tooling capability requirements. Structured trace recording with LLM/agent semantic conventions; hash-based content recording with authorised-operator unmasking; evaluator integration for continuous risk signals (hallucination, toxicity, refusal-rate); SDK-side or proxy-side data masking; self-hosting option for data-residency contexts. Reference platforms named (vendor-neutral phrasing): Langfuse (Apache 2.0, self-hostable), Phoenix (Elastic License 2.0, OpenTelemetry-native), Helicone (Apache 2.0, provider-key vault).
- **OBS-SEC-04**: Vendor proxies acting as AI gateways are themselves observability surfaces. Logs from such proxies are inventoried with the same governance as the application telemetry platform.

### What this phase does NOT include

- No new external citations (already added in Phase 23.6).
- No reference to commercial AI observability vendors in the standard (LangSmith is closed-source SaaS; mention deferred to the tooling landscape register).

### Cross-references updated

- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) (1.5.0 to 1.6.0).
- Main README (Library 2026.05.23 to 2026.05.24; README 1.7.16 to 1.7.17).

### Library version

`2026.05.23` to `2026.05.24`. README `1.7.16` to `1.7.17`.

### Next

Phase 23.9: AI pentest agent governance. Final phase in the agreed sequence. Addresses PentestGPT, PentAGI, Strix, HexStrike, BurpGPT as a new governance category requiring positioning in the AI security standard and dev-security domain.

All 12 audits clean.

## Phase 23.7 (2026-05-30, Library Version 2026.05.23): AI Security Tooling Landscape Register

Seventh content phase from the external-project assessment. The post-research master index deliverable. Adds a new Register documenting the AI security tooling landscape as surveyed in Wave 1 and Wave 2 of the assessment — 55 entries across 9 categories with scope, license, library reference status, key capabilities, and GRC concern surfaced for each.

### Purpose of this register

Unlike the Canonical Citations Register (which records authoritative citations used in library content), this register is a landscape catalogue. It serves:

- **Adopter orientation**: concrete tooling choices implementing the abstract controls in library standards.
- **Future-content backing**: tools and threat-class definitions that converge across multiple independent projects.
- **GRC gap traceability**: audit trail back to why each control or threat class exists in the library.

It is **not** a recommendation list or endorsement.

### Structure

Nine categories covering 55 entries:

- **5.1** Application-side runtime defence (open-source) - 12 projects: PROMPTPurify, llm-guard, rebuff, ClawGuard, CourtGuard, NeMo Guardrails, Guardrails AI, Vigil-LLM, CodeGate, llm-warden, LocalMod, Meta PurpleLlama bundle.
- **5.2** Testing, red-team, and benchmark tools - 18 projects: promptfoo, garak, pyrit, deepteam, PISmith, promptmap, AgentDojo, HarmBench, ART, HEART, Open-Prompt-Injection, ARTKIT, Giskard, FuzzyAI, LLMFuzzer, AIJack, AIAPwn, inspect_evals.
- **5.3** ML supply chain scanners - 3 projects: modelscan, picklescan, fickling.
- **5.4** AI observability platforms - 4 projects: LangSmith, Langfuse, Phoenix, Helicone.
- **5.5** MCP security - 1 project: Lasso MCP Gateway.
- **5.6** Dev-rules and coding-assistant baselines - 3 projects: TikiTribe, Wiz, Kariedo.
- **5.7** AI pentest agents (open-source) - 7 projects: PentestGPT, PentAGI, AI-OPS, HackSynth, HexStrike AI, BurpGPT, Strix.
- **5.8** Commercial runtime guardrails - 6 vendors: Lakera Guard, PromptArmor, HiddenLayer AIM, CalypsoAI, Mindgard, SplxAI (public-doc depth only).
- **5.9** Resource indexes - 1: awesome-ai-security.

### GRC gap traceability table

§6 of the register cross-references the 27 gaps surfaced by these projects against the phases that closed them (Phases 23.1 through 23.6) and identifies the projects surfacing each gap. Pending Phase 23.8 and 23.9 gaps are also enumerated with their source projects.

### URL corrections recorded

Three project URLs initially proposed during Wave 2 research turned out to be wrong; the register records the canonical URLs:
- `0v3rride/AI-OPS` (404) → canonical: `antoninoLorenzo/AI-OPS`
- `HSEcurity/hacksynth` (does not exist) → canonical: `aielte-research/HackSynth`
- `c0d3-mast3r/AIAPwn` (the URL given to assess) → canonical: `karimhabush/aiapwn`

Two project name collisions disambiguated:
- "PromptArmor" the YC W24 startup vs "PromptArmor" the ICLR 2026 research defence (arXiv 2507.15219).
- `Repello-AI/llm-warden` (404) and `Vectorial1024/LocalMod` (404) — canonical paths recorded.

### Project status flags

Tools known to be archived, unmaintained, or facing license cautions are flagged:
- rebuff (archived May 2025)
- CodeGate (archived June 2025)
- Vigil-LLM (alpha, archived)
- LLMFuzzer (unmaintained)
- fickling (LGPL-3.0 copyleft caution)
- HackSynth (AGPLv3 copyleft caution)
- promptmap (GPL-3.0 license caution for CC0 library)
- Phoenix (Elastic License 2.0; not OSI-approved)

### Vendor acquisitions affecting positioning

- Lakera → Check Point (Nov 2025)
- SplxAI → Zscaler (pending/announced)

### Cross-references updated

- [`governance/register-ai-security-tooling-landscape.md`](governance/register-ai-security-tooling-landscape.md) (v1.0.0, new): 55-entry landscape catalogue.
- [`governance/README.md`](governance/README.md) (1.6.0 to 1.7.0): new register listed.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.2 to 1.27.3): new register indexed.
- Main README (Library 2026.05.22 to 2026.05.23; README 1.7.15 to 1.7.16).

### Library version

`2026.05.22` to `2026.05.23`. README `1.7.15` to `1.7.16`.

### Next

Phase 23.8: AI observability OSS reference architecture (LangSmith, Langfuse, Phoenix, Helicone) — small touch to operations and AI standards.

All 12 audits clean.

## Phase 23.6 (2026-05-30, Library Version 2026.05.22): Framework alignment updates

Sixth content phase from the external-project assessment. Extends the Canonical Citations Register with new authoritative references and a new AI security tooling references section. All new entries are queued for citation verification under the Citation Verification Specification methodology (the Q-track).

### Why this update exists

Phases 23.1 through 23.5 added controls referencing defensive patterns and external standards in standard prose without adding the citations to the register. This phase brings the register up to date with what those standards now cite.

### New citations added

**Cybersecurity adversary frameworks** (4 additions):
- AVID (AI Vulnerability Database, avidml.org)
- MLCommons AILuminate v1.0
- HarmBench
- OWASP GenAI Security Project

**OWASP** (2 additions):
- OWASP Agentic AI Top 10 2026
- OWASP MCP Top 10 2025

**AI safety evaluation programmes** (new section, 3 entries):
- UK AISI inspect_evals
- Meta CyberSecEval v4
- NIST SP 800-218A (Secure SDF GenAI profile)

**AI security tooling references** (new section, 26 entries) — open-source AI security projects referenced by library content as defensive-pattern exemplars or concrete tooling choices: Trusted-AI ART, IBM HEART, AIJack, HarmBench framework, Meta PurpleLlama, NVIDIA NeMo Guardrails, Guardrails AI, Protect AI llm-guard, Protect AI rebuff (archived), Protect AI modelscan, picklescan, Trail of Bits fickling, Giskard, Confident AI deepteam, promptfoo, NVIDIA garak, Microsoft PyRIT, ETH Zurich AgentDojo, Vigil-LLM (archived), Stacklok CodeGate (archived), ClawGuard, Lasso MCP Gateway, jackhhao llm-warden, TikiTribe claude-secure-coding-rules, Wiz secure-rules-files, Kariedo claude-code-security-rules, awesome-ai-security (CC0-1.0; suitable for direct library reuse).

### Verification status

**Important caveat**: all new citations in this phase are recorded with the AI verifier's best-effort metadata from Wave 1 and Wave 2 research. Per the Citation Verification Specification §3.5, these are pending human-verifier confirmation through subsequent verification batches. The register entries are positive (they exist in the register) but they carry no verification log entry yet. Adoption of any citation should treat the register entry as a starting point pending verification.

The AI tooling section is structurally different from the standards sections: it records software projects with versions current at registration time, archive/active status flagged for tools known to be no longer maintained, and license noted (LGPL-3.0 for fickling flagged for copyleft caution). Re-verification cadence for the tooling section is annual.

### What this phase does NOT include

- Verification rows in [`register-citation-verifications.md`](governance/register-citation-verifications.md) for the new entries. Those will be added when verification batches resume (originally scoped as Phase Q2 ISO/IEC batch, currently paused per the user's pause-and-ask instruction).
- No content changes to any AI or dev-security standard. Citations recorded here exist to back the controls already added in Phases 23.1 through 23.5.

### Cross-references updated

- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (1.3.0 to 1.4.0): four new sections / extensions; 35+ new entries.
- Main README (Library 2026.05.21 to 2026.05.22; README 1.7.14 to 1.7.15).

### Library version

`2026.05.21` to `2026.05.22`. README `1.7.14` to `1.7.15`.

### Next

Phase 23.7: master project index register. Documents every project surfaced across Wave 1 and Wave 2 research (52 projects) with scope, capabilities, library reference status, and GRC concern surfaced. This is the post-research artefact you requested separately and is itself a CC0 reference deliverable.

All 12 audits clean.

## Phase 23.5 (2026-05-30, Library Version 2026.05.21): Classical ML adversarial taxonomy

Fifth content phase from the external-project assessment. Significantly expands the AI Model Risk Standard §5 (Robustness and adversarial testing) with a structured taxonomy distinguishing LLM threats from classical ML threats, federated-learning threats, defence categories, adaptive-attacker testing, and operational robustness. Codifies the threat surface that ART (Trusted-AI Adversarial Robustness Toolbox), AIJack, HEART, and HarmBench collectively cover.

### Why this expansion exists

The library has been overwhelmingly LLM-centric. The previous §5 named "data poisoning, model inversion, membership inference, training data leakage, input perturbation sensitivity, unauthorized model or data extraction" at one-line granularity. The Wave 2 research (ART, AIJack, HEART) demonstrated that the classical-ML adversarial surface has structure that organisations operating non-LLM models need codified.

### What was added

Section 5 restructured into six numbered subsections:

- **5.1 LLM and generative-system threats** (12 named categories including agentic Goal Theft, Inter-Agent Communication Compromise, multimodal injection, hallucinated security controls).
- **5.2 Classical ML threats** (4 named attack classes — evasion, poisoning, extraction, inference — with the canonical attack family enumeration that ART codifies: FGSM, PGD, Carlini-Wagner, BoundaryAttack, HopSkipJump, SquareAttack, AdversarialPatch, DPatch, BadDet variants, CopycatCNN, KnockoffNets, MIFace, membership inference variants, attribute inference, model inversion, database reconstruction).
- **5.3 Federated-learning threats** (DBA, model replacement, free-rider, label-leakage via norm-attack, gradient inversion variants).
- **5.4 Defence categories** (preprocessor, postprocessor, adversarial training, transformer defences, detectors, privacy defences, output egress controls, certified defences).
- **5.5 Adaptive-attacker testing** (required where the deployed model class is vulnerable to RL-trained adversaries; cadence per ADTEST-SEC-01).
- **5.6 Out-of-distribution and operational robustness** (across all model classes).

### Coverage rationale

The deny-list of attack families in 5.2 is not exhaustive; it codifies the canonical attack categories that converge across ART (the Linux Foundation flagship), AIJack (privacy + FL), and HEART (DoD MAITE T&E). Organisations operating classical ML can use this taxonomy as the structural basis for their adversarial test programme and then map specific tool choices below it. The control remains vendor-neutral: ART, AIJack, HEART, or equivalent tools may be used.

### What this phase does NOT include

- No new external citations in the framework-alignment list (deferred to Phase 23.6).
- No per-attack control IDs (e.g., MODEL-RISK-EV-01) — the taxonomy is descriptive of test scope, not prescriptive at the per-attack level. Per-attack mandates would be excessive for a vendor-neutral baseline.

### Cross-references updated

- [`ai/standard-ai-model-risk.md`](ai/standard-ai-model-risk.md) (1.0.0 to 1.1.0): §5 substantially expanded.
- Main README (Library 2026.05.20 to 2026.05.21; README 1.7.13 to 1.7.14).

### Library version

`2026.05.20` to `2026.05.21`. README `1.7.13` to `1.7.14`.

### Next

Phase 23.6: framework alignment updates. Adds new entries to [`register-canonical-citations.md`](governance/register-canonical-citations.md) (AVID, MLCommons AILuminate, UK AISI inspect_evals, OWASP Agentic AI Top 10 2026, CyberSecEval, HarmBench, ART, modelscan, picklescan, fickling, NeMo Guardrails, Guardrails AI, llm-guard, Giskard, deepteam, awesome-ai-security). Each new citation enters the citation verifications queue per the Q-track methodology.

All 12 audits clean.

## Phase 23.4 (2026-05-30, Library Version 2026.05.20): Agentic, RAG, MCP, and multimodal threat expansion

Fourth content phase from the external-project assessment. Significantly expands the AI and Agentic Development Security Standard threat coverage in four areas where the previous threat model named risks at high level but did not codify the operational defences. All changes are additive to existing controls; no prior IDs are renumbered.

### Why these expansions exist

The Wave 1 and Wave 2 research surfaced four convergent gap areas across multiple independent projects (deepteam, promptfoo, agentdojo, Lasso MCP Gateway, garak, pyrit, llm-guard, NeMo Guardrails):

1. **Agentic vulnerabilities at deepteam-level granularity**: the prior standard had TC-04 Tool Misuse and TC-08 Agent Privilege Escalation but did not name Goal Theft, Drift, Inter-Agent Communication Compromise, or RL-trained adaptive adversaries.
2. **RAG test categories**: the prior standard had `RAG-SEC-01` to 09 covering ingestion governance but did not explicitly distinguish three test obligations (poisoning, document exfiltration, source attribution) that promptfoo and agentdojo treat as separate.
3. **MCP tool metadata as a content surface**: the prior standard had `MCP-SEC-01` to 07 covering server access and tool authentication but did not address the tool description itself as an injection vector (the Lasso MCP Gateway pattern).
4. **Multimodal threats**: the prior standard was text-LLM-centric. Image, audio, video, document, OCR, and QR-code inputs are increasingly used and were not addressed.

### New threat classes

Added to §6:

- **TC-12 Tool Metadata Poisoning**: tool description as injection vector.
- **TC-13 Multimodal Injection**: adversarial content in non-text modalities.
- **TC-14 Agentic Goal Theft and Drift**: acute substitution and gradual divergence of agent objective.
- **TC-15 Inter-Agent Communication Compromise**: lateral propagation between agents.
- **TC-16 Adaptive / RL-Trained Adversary**: static defensive test suites insufficient at adaptive-attacker iteration rate.

### New controls

- **AGENT-SEC-15** Goal stability multi-turn testing.
- **AGENT-SEC-16** Inter-agent communication authentication and content-shape validation.
- **AGENT-SEC-17** Modality-appropriate filters required at each modality entry point.
- **RAG-SEC-10** RAG poisoning test obligation.
- **RAG-SEC-11** RAG document exfiltration test obligation.
- **RAG-SEC-12** RAG source attribution test obligation.
- **MCP-SEC-08** Tool description content scanning at server-load time.
- **MCP-SEC-09** Tool description hash pinning to detect rug-pull pattern.
- **MCP-SEC-10** Tool-name shadowing detection across MCP servers.
- **RUNTIME-SEC-07** Multimodal content filtering per modality (image, audio, video, PDF/Office, OCR, QR).
- **RUNTIME-SEC-08** Modality-cross-contamination acknowledgement.

### What this phase does NOT include

- No new external citations introduced (deferred to Phase 23.6 per the agreed sequence).
- No expansion of [`guide-ai-adversarial-test-reference.md`](ai/guide-ai-adversarial-test-reference.md) with new test categories yet — that follows in a later phase if test-case granularity in the standard alone proves insufficient.

### Cross-references updated

- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) (1.4.0 to 1.5.0): 5 new threat classes, 11 new controls.
- Main README (Library 2026.05.19 to 2026.05.20; README 1.7.12 to 1.7.13).

### Library version

`2026.05.19` to `2026.05.20`. README `1.7.12` to `1.7.13`.

### Next

Phase 23.5: classical ML adversarial taxonomy in [`standard-ai-model-risk.md`](ai/standard-ai-model-risk.md) (ART, AIJack, HEART-derived); the library is currently LLM-centric and lacks codification of evasion, poisoning, extraction, inference attacks, and federated-learning attacks for classical ML deployments.

All 12 audits clean.

## Phase 23.3 (2026-05-30, Library Version 2026.05.19): ML model file scanning

Third content phase from the external-project assessment. Adds a new control `SUPPLY-SEC-07` to the AI and Agentic Development Security Standard §18, mandating byte-level scanning of serialized ML model files for unsafe operators before adoption or production load. This closes a long-standing gap where the library covered model artefact provenance and checksums (`SUPPLY-SEC-04`, `-05`, `-06`) and the `trust_remote_code=False` requirement (`P-14`) but did not codify content scanning of serialized model artefacts themselves.

### Why this control exists

Serialized ML model files in pickle and pickle-derived formats execute arbitrary Python code at load time via the `__reduce__` mechanism. Three open-source scanners surfaced during Wave 1 and Wave 2 research codify the operator deny-list pattern at production-credible depth:

- **modelscan** (Apache-2.0): four-tier severity covering pickle, H5, Keras, SavedModel; explicit Critical / High / Medium operator categories.
- **picklescan** (MIT): pickle opcode-stream analyser with explicit unsafe-globals deny-list; underpins Hugging Face Hub-side scanning.
- **fickling** (LGPL-3.0): pickle decompiler and symbolic tracer; runtime import-hook with severity tiers.

The detection categories above are not exclusive to any one of these tools; the deny-list converges across them. The control codifies the converged minimum coverage.

### What the control mandates

- **In-scope file formats** explicitly enumerated: pickle and derivatives, PyTorch, H5, Keras V3, TensorFlow SavedModel, NumPy object arrays.
- **Out-of-scope formats** explicitly acknowledged: ONNX, Safetensors, GGUF, TensorRT plan files (lower attack surface; weight manipulation theoretical but not addressed by file-content scanning).
- **Critical-severity detection categories** (deployment blocking): Python builtins enabling code execution, OS/process/network modules, debug/runtime modules, serialisation re-entry, reflection, Keras Lambda layers with code objects.
- **High and Medium tiers** with appropriate handling.
- **Adoption gate** at model registry entry for every artefact from outside the organisation.
- **Production-load gate** combining scanner-aware loaders with `trust_remote_code=False`.
- **Exception path** with CISO approval and compensating controls.

### What this phase does NOT include

No tool-specific mandate (vendor-neutral as per library convention). Tool selection is at the organisation's discretion. The deny-list categories are the minimum coverage requirement.

### Cross-references updated

- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) (1.3.0 to 1.4.0): new `SUPPLY-SEC-07` control added to §18.
- Main README (Library 2026.05.18 to 2026.05.19; README 1.7.11 to 1.7.12).

### Citation note

References to modelscan, picklescan, and fickling are in the CHANGELOG and rationale paragraphs, not in the standard's framework-alignment table. Direct external tool references will be added to the canonical citations register in Phase 23.6 (framework alignment updates) and queued for citation verification.

### Library version

`2026.05.18` to `2026.05.19`. README `1.7.11` to `1.7.12`.

### Next

Phase 23.4: agentic vulnerability taxonomy expansion, RAG test category split (poisoning + exfiltration + source-attribution), tool-metadata poisoning, multimodal threat section.

All 12 audits clean.

## Phase 23.2 (2026-05-30, Library Version 2026.05.18): Dev-side AI input/output scanning controls

Second content phase from the external-project assessment. Extends the AI Coding Assistant Security Guideline with three new sections promoting prior "awareness" guidance to operational scanning controls, and codifying session isolation and vendor-telemetry monitoring as first-class concerns.

### Why these controls exist

The prior guideline acknowledged prompt-injection vectors in code comments, test data, dependencies, and issue trackers but stopped at developer awareness. The Wave 1 and Wave 2 project research confirmed that organisations operating AI coding assistants need active scanning controls operating on the files the assistant reads and the code it produces, regardless of developer attention. Equivalent runtime scanning is the architectural pattern of CodeGate, ClawGuard, Lasso MCP Gateway, llm-guard, and Vigil-LLM applied at the developer's pipeline rather than the application's.

The previous guideline also addressed vendor telemetry as a policy concern only ("verify data residency before use"). Operating practice from CodeGate, Helicone, and similar tools indicates telemetry must be monitored as an ongoing operational concern, not a procurement checkbox.

### New sections

- **Defensive scanning of AI coding assistant inputs and outputs**:
  - Input scanning of files before AI consumption (forged chat-template tokens, instruction-override patterns, steganographic Unicode, hidden HTML comments, embedded URLs)
  - Output scanning of AI-generated code before commit (suspicious URLs, LLM-API key patterns, hallucinated imports, hallucinated security controls, exfiltration-style egress, comment-embedded instructions)
- **Session isolation, vendor telemetry, and egress monitoring**:
  - Session isolation across customer codebases / confidentiality classifications / regulated-data scopes
  - Vendor telemetry inventory in the approved-tools register
  - Egress monitoring at the network layer where operationally available
  - Insider-bypass risk recognition

### Cross-references with Phase 23.1

The dev-side scanning controls here mirror the application-side controls added in Phase 23.1 (`AI-SEC-INP-06` through `INP-09`, `AI-SEC-OUT-05` and `OUT-06`). The pattern is consistent: the application standard governs runtime defences in production AI systems; the dev guideline governs equivalent defences in the developer pipeline.

### Cross-references updated

- [`dev-security/guideline-ai-coding-assistant-security.md`](dev-security/guideline-ai-coding-assistant-security.md) (1.0.1 to 1.1.0): three new sections added; existing "Prompt injection awareness" section retained as orientation.
- Main README (Library 2026.05.17 to 2026.05.18; README 1.7.10 to 1.7.11).

### Library version

`2026.05.17` to `2026.05.18`. README `1.7.10` to `1.7.11`.

### Next

Phase 23.3: ML model file scanning (`SUPPLY-SEC-07` in [`standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) §18) covering serialized-model byte-level scanning with operator deny-list pattern from modelscan / picklescan / fickling.

All 12 audits clean.

## Phase 23.1 (2026-05-30, Library Version 2026.05.17): Runtime input/output processing controls

First content phase derived from the deep external-project assessment of 52 AI security tools. Adds six new mandatory controls to the AI and Agentic Development Security Standard codifying defensive techniques surfaced consistently across multiple independent projects (PROMPTPurify, llm-guard, ClawGuard, NeMo Guardrails, Vigil-LLM, Lasso MCP Gateway, Guardrails AI). The controls fill gaps where the standard previously named threats but did not mandate the specific defensive techniques.

### Why these controls exist

The library's prior `AI-SEC-INP-01` to `INP-05` and `AI-SEC-OUT-01` to `OUT-04` covered the main input/output boundaries with content-safety service, native role separation, structural delimiters, token budget, PII detection, schema validation, no-eval, HTML escape, and downstream-URL allow-listing. They did not codify:

- Unicode-class normalisation as a proactive control (the threat is acknowledged in TC-01 and tested in DPI-08 and IPI-03, but normalisation as a mandate is absent).
- Forged chat-template token neutralisation (`<|im_start|>`, `[INST]`, `<<SYS>>`, etc.) before tokenisation.
- Per-call nonces for structural delimiters (static markers are vulnerable to adversary pre-inclusion).
- A distinct flag-only tripwire-regex layer feeding rate limits and SIEM.
- URL allow-list validation in rendered AI output (silent-exfil vectors via markdown images and tracking links).
- Auto-fetch disabling at the rendering layer for markdown/HTML output.

Cross-project evidence supporting each addition is recorded in the Phase Q2-prep aftermath research notes.

### New controls

- **AI-SEC-INP-06**: Unicode normalisation (NFKC + zero-width/format strip + BIDI removal + homoglyph folding + combining-mark collapse + per-sink length cap). Aligns with Unicode Technical Standard 39 and Annex 15.
- **AI-SEC-INP-07**: Forged chat-template token neutralisation; non-exhaustive token list maintained per deployed model family.
- **AI-SEC-INP-08**: Per-call nonce fences for structural delimiters, replacing static markers.
- **AI-SEC-INP-09**: Flag-only tripwire-regex layer distinct from content safety filter and ML classifier.
- **AI-SEC-OUT-05**: Outbound URL allow-list validation for rendered AI output across markdown, HTML, and CSS surfaces.
- **AI-SEC-OUT-06**: Auto-fetch disabling or constrained allow-listing at the rendering layer for markdown/HTML output.

### What this phase does NOT include

Phase 23.1 deliberately limits scope to the runtime input/output processing controls. Subsequent phases per the agreed sequence cover:

- 23.2: dev-side AI input/output scanning controls
- 23.3: ML model file scanning (`SUPPLY-SEC-07`)
- 23.4: agentic vulnerability taxonomy expansion, RAG test category split, tool-metadata poisoning, multimodal threat section
- 23.5: classical ML adversarial taxonomy in [`standard-ai-model-risk.md`](ai/standard-ai-model-risk.md)
- 23.6: framework alignment updates (AVID, MLCommons, UK AISI, OWASP Agents 2026, CyberSecEval, HarmBench)
- 23.7: master project index register (the post-research artefact)
- 23.8: AI observability OSS reference architecture
- 23.9: AI pentest agent governance

### Cross-references updated

- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) (1.2.0 to 1.3.0): six new controls added to §7.
- Main README (Library 2026.05.16 to 2026.05.17; README 1.7.9 to 1.7.10).

### Citation note

These new controls do not introduce new external citations; they implement defensive patterns from authoritative sources already cited (OWASP LLM Top 10, NIST AI RMF, Unicode Technical Standards). Specific external tool references will be added in Phase 23.6 (framework alignment updates) and queued for citation verification.

### Library version

`2026.05.16` to `2026.05.17`. README `1.7.9` to `1.7.10`.

### Next

Phase 23.2: dev-side AI input/output scanning controls in [`guideline-ai-coding-assistant-security.md`](dev-security/guideline-ai-coding-assistant-security.md).

All 12 audits clean.

## Phase Q2-prep (2026-05-29, Library Version 2026.05.16): Q2 worklist prepared; Worklist doctype added

Prepares the first verification batch under the Citation Verification Specification. The AI verifier has pre-filled the worklist for 24 ISO and ISO/IEC entries; the human verifier will execute the browser fetches, capture verbatim text, and assign confidence ratings per Citation Verification Specification §3.4 and §8.2 to §8.3.

### What this phase includes

- Adds the `Worklist` doctype to the library (17th doctype). Worklists are per-batch working artefacts derived from a Template; distinct from Templates (which are reusable blanks) and from Registers (which are persistent authoritative records).
- Updates the metadata linter ([`tools/lint-metadata.py`](tools/lint-metadata.py)) to accept the new doctype with the `worklist-` filename prefix.
- Updates the master project specification and ingestion specification to list the new doctype and provide selection guidance.
- Adds the first batch worklist itself: 24 ISO and ISO/IEC entries pre-filled with publisher, expected primary URLs (best-effort), expected values from the canonical citations register, and parsing gotchas (URL patterns, status field interpretation, multi-part standards handling, entries warranting particular human attention).

### What this phase does NOT include

- No actual verification has been performed. The captured-text columns in the worklist are empty and will be filled by the human verifier.
- No corrections to the Canonical Citations Register. Corrections (if any) are proposed at batch close after the human verifier's captured text is in hand.
- No rows in the Citation Verifications Register. Rows are appended at batch close after human verification.

### Six entries flagged for particular human attention

The AI verifier has called out six register entries where its training-time confidence is lowest and the human's verification is most consequential: ISO/IEC 42005 (publication date claim), ISO/IEC 42006 (post-draft publication state), ISO 37001 (2025 edition claim), ISO/IEC 38500 (2024 edition claim), ISO/IEC 5259 (multi-part series year handling), ISO/IEC 27033 (multi-part series with later editions on some parts). These flags are orientation for the human verifier; the publisher page remains authoritative.

### New file

- [`governance/worklist-citation-verification-batch-q2-iso-iec.md`](governance/worklist-citation-verification-batch-q2-iso-iec.md) (v1.0.0, Worklist doctype): 5 numbered sections including the 24-row worklist table.

### Doctype change

- [`tools/lint-metadata.py`](tools/lint-metadata.py): `ALLOWED_TYPES` extended from 16 to 17; `TYPE_TO_PREFIX` adds `Worklist: worklist-`.
- [`specification-ingestion.md`](specification-ingestion.md) (1.5.0 to 1.6.0): doctype list extended; Template-vs-Worklist selection guidance added.
- [`specification-master-project.md`](specification-master-project.md) (1.3.1 to 1.4.0): doctype list extended.

### Cross-references updated

- [`governance/README.md`](governance/README.md) (1.5.0 to 1.6.0): worklist listed in Active documents.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.1 to 1.27.2): worklist indexed.

### Library version

`2026.05.15` to `2026.05.16`. README `1.7.8` to `1.7.9`.

### Next

Phase Q2 execution: human verifier (maintainer) fills the captured-text and confidence columns in the worklist by browsing to each publisher page, capturing verbatim text, and submitting Wayback snapshots. At batch close, the AI verifier transcribes into the Citation Verifications Register and proposes any Canonical Citations Register corrections for human approval.

All 12 audits clean.

## Phase Q1.1 (2026-05-29, Library Version 2026.05.15): AI/Human Verifier Operating Model

Sub-phase of the quality-system track. Formalises the AI/human split in the Citation Verification methodology after empirical testing revealed environmental constraints in the AI verifier's sandbox.

### Why this exists

Empirical test of the AI verifier's environment found:

- `WebFetch` to publisher canonical domains (iso.org, nist.gov, iec.ch, ietf.org) returns HTTP 403 Forbidden.
- `WebFetch` to `web.archive.org` is explicitly blocked at the harness level.
- `WebSearch` is available but returns search snippets and possibly AI-generated summaries, neither of which qualifies as a primary verification source under §6.4 of the specification.

Continuing with the AI verifier as primary would have meant assembling verification rows from search snippets and AI judgement — exactly the AI-mediated verification the methodology explicitly forbids. That would put a false-confidence seal on the register. The honest path is to disclose the split, codify it in the specification, and treat the AI/human division as a feature of the methodology rather than a workaround.

### Methodology changes

- **Specification updated to v1.1.0**: new §3 "Operating model and verifier roles" with six subsections covering rationale, role definitions, AI verifier responsibilities, human verifier responsibilities, environmental constraints disclosure, and the worklist artefact.
- **Verification procedure (§8) restructured per step**: each procedure step now identifies whether AI or human verifier performs it. Pre-verification and recording are AI; fetch, compare, and spot-check are human; reconcile is AI-proposes-human-approves.
- **Verifications register schema (§9) extended**: two new fields, `Captured by` (identifies the human verifier who fetched the publisher page) and `Recorded by` (identifies the actor who appended the row, typically the AI verifier acting clerically). A row whose `Captured by` value implies AI primary capture is invalid.
- **Threat model (§5) extended**: new "role conflation" threat row addressing the risk that a verification row obscures whether primary text was captured by human or AI.
- **Non-deferrable rules (§13) extended**: rule 8 "AI verifier does not perform primary verification"; rule 9 "Environmental capability of the AI verifier is disclosed, not worked around silently."
- **Confidence ratings (§10) and verification freshness (§12) renumbered**: was §9 and §11 in v1.0.0.

### New file

- [`governance/template-citation-verification-worklist.md`](governance/template-citation-verification-worklist.md) (v1.0.0, Template doctype): per-batch worklist enforcing the AI/human split. AI pre-fills Standard ID, Publisher, Expected primary URL, Field(s) to verify, Expected value. Human fills Captured text (verbatim), Wayback URL, Secondary URL, Result, Captured by, Confidence. AI transcribes into the verifications register at batch close.

### Credibility framing

The split is documented in the specification itself rather than as an implementation note, so that any future reader can see:

- Which verification steps were performed by an AI and which by a human.
- The specific environmental constraints that necessitated the split at the time of writing.
- That the methodology survives capability changes (the AI verifier's role expands or shrinks per §3.5 disclosures over time).

The Citation Verifications Register's `Captured by` field is the in-row evidence of which actor performed the integrity-bearing step on each row.

### Cross-references updated

- [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md) (1.0.0 to 1.1.0): operating-model section added; procedure restructured; schema extended; threat model extended; non-deferrable rules extended; internal section numbering shifted by 1 from §4 onward.
- [`governance/register-citation-verifications.md`](governance/register-citation-verifications.md) (1.0.0 to 1.1.0): schema updated for `Captured by` and `Recorded by`; section references updated to renumbered specification sections.
- [`governance/README.md`](governance/README.md) (1.4.0 to 1.5.0): worklist template added.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.0 to 1.27.1): worklist template indexed; verifications-register references updated.

### Library version

`2026.05.14` to `2026.05.15`. README `1.7.7` to `1.7.8`.

### Next

Phase Q2: the first verification batch (ISO/IEC and ISO standards, approximately 24 entries). AI verifier prepares the batch worklist; human verifier (maintainer or delegate) executes the fetches and captures.

All 12 audits clean.

## Phase Q1 (2026-05-29, Library Version 2026.05.14): Citation Verification Methodology and Register

First sub-phase of a quality-system track (Phase Q, distinct from numbered content phases). Establishes a factual-verification control over the Canonical Citations Register: every citation is to be verified against the publisher's own canonical domain with verbatim text capture and a Wayback Machine snapshot URL recorded as a third-party evidence anchor.

This phase adds the methodology and the empty register. Actual verification of the 96 existing canonical citations is performed in subsequent sub-phases (Phase Q2 onward), batched by publisher cluster to keep PRs reviewable.

### Why this exists

Audit assessment identified that the twelve automated linters verify structural integrity but not factual accuracy. A citation can pass every linter while being factually wrong about a standard's existence, version, or publication date. Standards-currency linter trusts the Canonical Citations Register as the source of truth; the register itself was populated by the maintainer and carries no recorded factual provenance. This control closes that gap.

### Decision: full verification, not sampling

An earlier proposal to spot-sample N citations per phase was rejected. Sampling has the wrong failure mode for a reference library: a citation that is wrong but un-sampled stays wrong and propagates to every adopter, invisible under a "sample clean" report. Every entry will be verified.

### Threat model addressed

The methodology explicitly defends against:

- Adversarial AI-knowledge poisoning (content seeded to corrupt LLM knowledge of standards).
- SEO and content-farm spam producing confident-sounding wrong claims.
- Lookalike domains mimicking publisher sites.
- AI summarisation drift (paraphrased content that diverges from the source).
- Honest staleness in mirrors or caches.
- Publisher silently amending pages after verification (mitigated by Wayback snapshot capture).
- Verifier-side hallucination (mitigated by verbatim text capture and human spot-check).
- Single-source dependency (mitigated by Tier 2 corroboration where available).

### New files

- [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md) (v1.0.0, Specification doctype): 14 sections covering purpose, scope, threat model, trust tiers, publisher allow-list (28 publishers initially), verification procedure (pre-verification, fetch, compare, record, reconcile, spot-check), verifications register schema, confidence ratings (A/B/C/D), disposition of D-rated entries, verification freshness (12-month re-verification cadence), non-deferrable rules, and out-of-scope acknowledgements.
- [`governance/register-citation-verifications.md`](governance/register-citation-verifications.md) (v1.0.0, Register doctype): append-only verification log with the 14-field schema, D-rated resolutions log, and coverage-summary table. Initially empty.

### Non-deferrable rules established

- Publisher canonical domain is the only primary source.
- Captured text is the publisher's actual words, not a summary.
- Wayback snapshot URL is recorded for every verification.
- Human spot-check (5+ entries per batch) follows every verification batch.
- D-rated entries are resolved (corrected or removed), not retained.
- AI-generated content is never a verification source.
- The verifier's prior belief is not a verification.

### Cross-references updated

- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (1.2.0 to 1.3.0): related-documents updated; forward reference to the verification specification and register added to the Purpose section.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.5 to 1.27.0): both new documents indexed.

### Library version

`2026.05.13` to `2026.05.14`. README `1.7.6` to `1.7.7`.

### Next

Phase Q2: verification batch 1 (ISO/IEC and ISO standards, approximately 24 entries) against the publisher's catalogue pages.

All 12 audits clean.

## Phase 22.6 (2026-05-29, Library Version 2026.05.13): Building Management Systems (BMS) Overlay Annex

Sixth and final sub-phase of the Phase 22 OT depth track. Adds the BMS overlay annex, which identifies BMS-specific positions over the OT/ICS Security Standard rather than duplicating it. BMS are a subset of OT and remain governed by the OT/ICS Security Standard; this annex captures the deltas driven by life-safety integration, tenant impact, AHJ oversight, and the multi-vendor smart-building integration pattern.

### New file

- [`operations/ot/annex-bms-overlay.md`](operations/ot/annex-bms-overlay.md) (v1.0.0, Annex doctype): 12 numbered sections covering purpose, scope (in-scope, out-of-scope, boundary cases), BMS-vs-process-control differences, life-safety integration (non-interference principle, fire-system integration constraints, emergency operation override), AHJ coordination, BMS protocol governance (BACnet incl. BACnet/SC, LON, KNX, Modbus in BMS, proprietary protocols), multi-vendor coordination, tenant and occupancy data privacy, smart-building cloud integration, asset / change / incident overlay specifics, framework alignment, and cross-reference summary.

### Key overlay positions established

- **Non-interference principle**: cyber controls must not interfere with operation or response time of life-safety functions; containment actions affecting fire alarm, evacuation, or emergency lighting require Facilities Manager and (where required) AHJ authorisation.
- **AHJ as approval authority**: changes to AHJ-regulated fire and life-safety equipment are at minimum Normal (typically Safety-related) in the change category model; AHJ notification or approval status is tracked on the change record.
- **BACnet/SC preference**: where BACnet/SC is supported by deployed equipment, it must be enabled and unauthenticated BACnet/IP disabled at the conduit.
- **OT-1 + S-B default for life-safety-integrated BMS**: BMS controllers integrated with fire or life-safety functions are OT-1 (critical control) and at least S-B (safety-adjacent); engineered life-safety functions are S-A.
- **Smart-building cloud through OT DMZ**: cloud integration terminates at Purdue level 3.5, never directly in OT zones.
- **Tenant and occupancy data are privacy-relevant**: BMS that captures identifiable presence, badge events, or per-tenant data is subject to the privacy policy and records-of-processing inventory.

### Multi-vendor coordination codified

BMS deployments are routinely multi-vendor (primary BMS, HVAC, fire, access, lighting, metering vendors). Security responsibility per subsystem is captured in the supplier register and contracts; each vendor has separate remote-access credentials, sessions, and audit trails; coordinated changes are managed jointly through the OT Change Management Procedure.

### Framework alignment additions

ISO 16484, ASHRAE 135 (BACnet), NIST SP 1900 series (smart buildings), NFPA 72 (US fire alarm code, 2025 edition), EN 54 series (European fire detection and fire alarm), TSA Pipeline Security Directive, ISO/IEC 27018 / 27701 (privacy in cloud / PIMS), GDPR / UK GDPR / CCPA.

### Cross-references updated

- [`operations/ot/README.md`](operations/ot/README.md) (1.4.0 to 1.5.0): annex added to Active documents; Phase 22 marked complete.
- [`operations/README.md`](operations/README.md) (1.2.4 to 1.2.5): annex added to OT sub-directory artefacts table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.4 to 1.26.5): annex added.
- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (1.1.0 to 1.2.0): ISO 16484, ASHRAE 135, NIST SP 1900 series, NFPA 72, EN 54, TSA Pipeline Security Directive added.

### Library version

`2026.05.12` to `2026.05.13`. README `1.7.5` to `1.7.6`.

### Phase 22 status

Phase 22 (OT depth) complete: six sub-phases delivered (overview annex, OT/ICS Security Standard, OT Incident Response, OT Change Management, OT Asset Inventory and Lifecycle Register, BMS overlay). Subsequent OT expansion will be driven by adopter feedback and sector-specific requirements.

### Next

Tier 6 remaining items (cloud overlays beyond OT, identity depth, PQC deepening, cross-framework matrix expansion) or sector-track work, at user direction.

All 12 audits clean.

## Phase 22.5 (2026-05-29, Library Version 2026.05.12): OT Asset Inventory and Lifecycle Register

Fifth sub-phase of Phase 22. Defines the schema, governance, classification, and lifecycle model for OT assets, supplementing the general operations asset inventory and providing the authoritative record on which zone-and-conduit governance, OT change management, OT incident response, and OT vulnerability and patch management depend.

### New file

- [`operations/ot/register-ot-asset-inventory-and-lifecycle.md`](operations/ot/register-ot-asset-inventory-and-lifecycle.md) (v1.0.0, Register doctype): 12 numbered sections covering purpose, scope, roles, governance principles, classification (operational criticality, safety relevance, zone trust level), asset record schema (8 field groups), lifecycle states with explicit end-of-support and legacy-OS handling, inventory operations (discovery, reconciliation, unauthorized assets, secure decommissioning), retention, metrics, framework alignment, and cross-reference summary.

### Three-dimension OT classification

- **Operational criticality**: OT-1 (Critical control) to OT-4 (Peripheral).
- **Safety relevance**: S-A (Safety-Instrumented) / S-B (Safety-Adjacent) / S-C (Safety-Independent), independent of criticality.
- **Zone trust level**: Security Level Target (SL-T 1 to 4) of hosting zone with asset-level Security Level Capability (SL-C) tracking.

### Lifecycle states codified

Planned, Commissioning, Active, End-of-Support, Decommissioning, Decommissioned. End-of-Support is a managed state, not a defect: vendor end-of-support routinely precedes economic replacement by years in OT. Required artefacts when an asset enters End-of-Support: vendor announcement citation, compensating-controls package, risk-register entry, refresh-plan record. Legacy-OS handling codified separately with explicit network minimisation, allowlisting preference over signature AV, and heightened detection.

### Discovery and reconciliation

- **Passive discovery** is the default for live OT networks; active scanning restricted to vendor-confirmed safe paths and prohibited on SIS without Process Safety Engineer approval.
- **Reconciliation cadence**: monthly for OT-1 and OT-2, quarterly for OT-3 and OT-4.
- **Unauthorized assets**: investigation pathway with safety-preserving isolation; production-safe isolation only.
- **Secure decommissioning**: 6-step sequence preserving final configuration backup, credential revocation, topology update, and physical removal aligned with the media handling procedure.

### Asset record schema (8 field groups)

Identification, Location and zone, Classification, Ownership and operation, Lifecycle, Security state, Backup and recovery, Administrative. Vendor-managed and vendor end-of-support tracking are first-class fields.

### Framework alignment

IEC 62443-2-1, IEC 62443-3-2, IEC 62443-3-3, NIST SP 800-82 Rev 3, ISO/IEC 27001:2022 A.5.9, ISO/IEC 27019:2017, NERC CIP-002, NERC CIP-010, IEC 61511, EU NIS 2, TSA Pipeline Security Directive.

### Cross-references updated

- [`operations/ot/standard-ot-ics-security.md`](operations/ot/standard-ot-ics-security.md) (1.0.0 to 1.0.1): §5.1.3 placeholder replaced with direct link to the new register.
- [`operations/ot/README.md`](operations/ot/README.md) (1.3.0 to 1.4.0): register added to Active documents; Phase 22.5 removed from Planned section.
- [`operations/README.md`](operations/README.md) (1.2.3 to 1.2.4): register added to OT sub-directory artefacts table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.3 to 1.26.4): register added.

### Library version

`2026.05.11` to `2026.05.12`. README `1.7.4` to `1.7.5`.

### Next

Phase 22.6: BMS-specific overlay annex (HVAC, access control, fire/life-safety integration considerations).

All 12 audits clean.

## Phase 22.4 (2026-05-29, Library Version 2026.05.11): OT Change Management Procedure

Fourth sub-phase of Phase 22. Extends the general change management and configuration control procedure with OT-specific requirements: extended change windows aligned to production-maintenance schedules, mandatory vendor coordination, regression testing for safety-critical functions, and integration with safety management of change (MOC) under IEC 61511 where the change affects Safety Instrumented Systems.

### New file

- [`operations/ot/procedure-ot-change-management.md`](operations/ot/procedure-ot-change-management.md) (v1.0.0, Procedure doctype): 15 numbered sections covering purpose, scope (with safety-management precedence rule), roles, guiding principles, change categories, change-request content and timeline, OT risk assessment, OT-specific testing, OT-CAB approval, implementation, verification, backout, documentation and audit trail, metrics, and framework alignment.

### Guiding principles established

- **Production-first scheduling**: changes are scheduled into existing production maintenance windows; cyber-driven windows outside production maintenance require explicit business and safety justification.
- **Mandatory vendor coordination**: for vendor-controlled systems (DCS, PLC firmware, BMS controllers), no change without documented vendor approval or vendor-supplied patch package.
- **Test before production**: every change tested in sandbox, test bench, or representative non-production zone before production deployment, with cyber, safety, and performance regression suites.
- **Reversibility**: every change has a documented backout plan tested in non-production where feasible.
- **Safety integration**: where a change affects a Safety Instrumented System, the safety-management-of-change (MOC) process under IEC 61511 takes precedence over IT-style change governance.
- **No silent change**: undocumented field changes are tracked and remediated; cumulative drift drives baseline-reconciliation activity.

### Change categories codified

Five categories defined: Standard (pre-approved low-risk), Normal (assessed and OT-CAB-approved), Emergency (containment or safety-driven, expedited), Vendor-driven (vendor patch or firmware), and Safety-related (any change touching SIS, safety functions, or interlocks).

### OT-CAB approval

OT Change Advisory Board defined with composition (OT Security Lead, Plant Manager, Process Safety Engineer for safety-related, Control System Engineer, Vendor Liaison where applicable, CISO delegate). Decision criteria: production maintenance window alignment, risk-tier appropriate testing, vendor concurrence, backout plan tested, safety MOC closed where required.

### Risk assessment framework

Four-dimension risk model: cyber impact, safety impact, availability impact, vendor-support impact. Four-tier classification (low, moderate, high, critical) with mandatory testing depth and approval routing per tier.

### Testing framework

Three test environment types codified: sandbox (lab-isolated, vendor-supplied or self-built), test bench (replica of production for HMI / historian / engineering workstation changes), and non-production zone (live mirror for end-to-end validation). Cyber regression, safety-function regression, and performance regression suites required per tier.

### Framework alignment

IEC 62443-2-1 (programme element), IEC 62443-3-3 (system requirements where change introduces new controls), NIST SP 800-82 Rev 3 (configuration management section), ISO/IEC 27001 A.5.37 and A.8.32, IEC 61511 (mandatory MOC integration for SIS), NERC CIP-010, ITIL 4 (change-enablement practice), EU NIS 2.

### Cross-references updated

- [`operations/ot/README.md`](operations/ot/README.md) (1.2.0 to 1.3.0): procedure added to Active documents; Phase 22.4 removed from Planned section.
- [`operations/README.md`](operations/README.md) (1.2.2 to 1.2.3): procedure added to OT sub-directory artefacts table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.2 to 1.26.3): procedure added.

### Library version

`2026.05.10` to `2026.05.11`. README `1.7.3` to `1.7.4`.

### Next

Phase 22.5: OT Asset Inventory and Lifecycle Register (long-lifecycle assets, legacy OS handling, vendor-support state).

All 12 audits clean.

## Phase 22.3 (2026-05-29, Library Version 2026.05.10): OT Incident Response Procedure

Third sub-phase of Phase 22. Adds the operational sequence for responding to OT security incidents, extending the general security incident response procedure with OT-specific considerations.

### New file

- [`operations/ot/procedure-ot-incident-response.md`](operations/ot/procedure-ot-incident-response.md) (v1.0.0, Procedure doctype): 13 numbered sections covering purpose, scope, guiding principles, roles, severity classification, the five response phases (detection and triage, containment, eradication, recovery, post-incident), communications, forensics in OT, and framework alignment.

### Guiding principles established

- **Safety first**: any response action that could create a safety hazard is paused and escalated to the Process Safety Engineer. Production-safety risk is not exchanged for cyber-containment speed.
- **Availability constraints**: forensic actions planned to minimize production disruption; trade-offs documented when preservation and availability conflict.
- **Vendor coordination**: vendor involvement begins at triage, not at recovery.
- **Evidence preservation**: volatile OT evidence captured where lawful and operationally safe before containment commands alter state.
- **No silent remediation**: operators and engineers report rather than attempt silent fix.

### Five phases codified

1. **Detection and triage**: 15-minute SOC acknowledgement, 30-minute OT Security Lead engagement, immediate Process Safety Engineer notification for safety-implicated incidents.
2. **Containment**: six-option decision framework (isolate at conduit, block protocols, revoke credentials, manual control, controlled shutdown, monitor closely) with explicit trade-offs; SIS containment requires Process Safety Engineer approval; vendor remote-access sessions terminated on P1/P2 declaration.
3. **Eradication**: vendor-coordinated adversary removal; configuration rebuild from baselines; credential rotation; verification before recovery exit.
4. **Recovery**: sequenced restoration prioritising SIS verification, then monitoring, then control integrity, then conduits; Incident Commander approval required; joint approval with Process Safety Engineer for safety-implicated recoveries. Indicative recovery windows acknowledging OT-extended timelines (hours to weeks).
5. **Post-incident**: 10-business-day lessons-learned review; CAPA register entries; HAZOP and LOPA integration where safety implicated.

### Communications and forensics frameworks

- **Regulatory reporting**: NERC CIP EOP-004-4 and CIP-008 (North American electricity), EU NIS 2 timelines (24-hour early warning, 72-hour report, 1-month final), TSA pipeline directives, IMO maritime cyber, ICAO aviation cyber, privacy regulators where personal data affected.
- **Sector coordinators**: E-ISAC, WaterISAC, sector ISAC participation.
- **OT forensics constraints**: production cannot generally be paused for imaging; vendor cooperation required; some components have no persistent storage; volatile evidence is the rule.

### Severity classification extended

OT-specific triggers added to base P1–P4 scale: SIS compromise, loss-of-view/loss-of-control events, anomalous control commands, OT vendor compromise, OT DMZ compromise.

### Cross-references updated

- [`operations/ot/README.md`](operations/ot/README.md) (1.1.0 → 1.2.0): procedure added to Active documents; Phase 22.3 removed from Planned section.
- [`operations/README.md`](operations/README.md) (1.2.1 → 1.2.2): procedure added to OT sub-directory artefacts table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.1 → 1.26.2): procedure added.

### Library version

`2026.05.9` → `2026.05.10`. README `1.7.2` → `1.7.3`.

### Next

Phase 22.4: OT Change Management Procedure (extended change windows, vendor approval, regression testing for safety-critical functions).

All 12 audits clean.

## Phase 22.2 (2026-05-29, Library Version 2026.05.9): OT/ICS Security Standard

Second sub-phase of Phase 22. Codifies the concepts introduced in the Phase 22.1 overview annex into auditable control requirements.

### New file

- [`operations/ot/standard-ot-ics-security.md`](operations/ot/standard-ot-ics-security.md) (v1.0.0, Standard doctype): 15 numbered sections covering purpose, scope, governance, definitions, zone-and-conduit architecture, security-level achievement, OT-specific access control, network controls, endpoint and host hardening, monitoring/logging/detection, vendor and supplier requirements, safety integration, recovery, audit and assurance, framework alignment.

### Key requirements established

- **Zone-and-conduit architecture** (IEC 62443-3-2): every OT asset assigned to a zone; every inter-zone communication modelled as a conduit; risk assessment per zone and conduit; SL-T setting with CISO approval; annual review.
- **Security level achievement** (IEC 62443-3-3): SL-T set per risk; SL-A measured at least annually against the seven foundational requirements; SL-A < SL-T tracked in CAPA register; SL-C required of procured components.
- **OT-specific access control**: unique attributable accounts; MFA mandatory for remote access, engineering workstations, safety-system configuration, and IT-to-OT DMZ ingress; vendor remote access prohibited by default with explicit approval, time-bounding, jump-host enforcement, and session recording.
- **Network controls**: segmentation at conduit boundaries (firewalls, data diodes, protocol-aware OT firewalls); IT-OT DMZ mandatory; enumerated protocol allowlist; wireless prohibited to SIS.
- **Endpoint hardening**: configuration baselines; default vendor credentials changed; removable media via sanctioned media-staging only; passive vulnerability scanning required.
- **Patching**: cadence aligned with planned production windows, not monthly; test in representative non-production before production deployment; compensating controls where patching infeasible.
- **Monitoring**: authentication events, configuration changes, conduit-boundary traffic, process-anomaly indicators, SIS bypass conditions all into central SIEM; SOC analysts trained in OT; OT alerts escalated within 15 minutes.
- **Vendor governance**: IEC 62443-2-4 alignment required; vendor product SL-C documented; right-to-audit, vulnerability-disclosure, and incident-cooperation contractual requirements.
- **Safety integration**: SIS-BPCS separation; SL-T of at least SL 3 for SIS conduits; safety-engineering review for SIS changes; cyber considerations folded into HAZOP and LOPA.
- **Recovery**: configuration backups offline or in isolated zone; quarterly minimum cadence; restore testing; OT-specific RTO that may extend to days for cyber incidents requiring vendor coordination.
- **Audit**: SL-T ≥ SL 3 zones audited annually; SL-T ≤ SL 2 zones audited every 18 months; independent SL-A verification every three years for SL-T ≥ SL 3.

### Convention captured

The standard accepts that safety-regulation precedence applies where conflict arises (IEC 61511 management of change overrides general change-management requirements where the safety regulation is more restrictive).

### Cross-references updated

- [`operations/ot/README.md`](operations/ot/README.md) (1.0.0 → 1.1.0): standard added to Active documents; Phase 22.2 removed from Planned section.
- [`operations/README.md`](operations/README.md) (1.2.0 → 1.2.1): standard added to OT sub-directory artefacts table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.26.0 → 1.26.1): standard added to index.

### Library version

`2026.05.8` → `2026.05.9`. README `1.7.1` → `1.7.2`.

### Next

Phase 22.3: OT Incident Response Procedure (safety-first response, vendor coordination, longer recovery windows).

All 12 audits clean.

## Phase 22.1 (2026-05-29, Library Version 2026.05.8): OT security overview and foundations

First sub-phase of Phase 22 (operational technology depth). Establishes the foundation for OT security content: a new `operations/ot/` sub-directory, an overview annex, expanded glossary entries, and expanded canonical-citations entries for the IEC 62443 family and NIST SP 800-82 Rev 3.

### New sub-directory

- `operations/ot/` — Operational Technology home under the existing operations domain. Sub-directory selected over a new top-level `/ot/` domain because OT is operationally related to IT and integrating them into one domain reflects the IT/OT convergence reality.

### New files

- [`operations/ot/README.md`](operations/ot/README.md) (v1.0.0, Register doctype): sub-directory home, applicability, scope, planned-content roadmap, cross-domain relationships, reference-standards index, adopter guidance.
- [`operations/ot/annex-ot-security-overview.md`](operations/ot/annex-ot-security-overview.md) (v1.0.0, Annex doctype): foundational concepts annex. Eight sections covering OT scope and definitions, OT-versus-IT critical differences, primary reference frameworks (IEC 62443, NIST SP 800-82, IEC 61511/61508, NERC CIP), the zone-and-conduit model, OT-specific risk considerations, cross-domain relationships, frequently asked questions, and framework alignment.

### Glossary additions

- [`governance/register-glossary.md`](governance/register-glossary.md) (1.0.0 → 1.1.0): added IACS, BMS, HMI, IT/OT convergence, PLC, Purdue model, SCADA, SIL, SIS, SL-A, SL-C, SL-T, SP 800-82. Expanded ICS and OT entries with full definitions. Disambiguated DCS (CCM domain vs Distributed Control System).

### Canonical citations additions

- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (1.0.0 → 1.1.0): added NIST SP 800-82 Rev 3, IEC 62443-1-1, 2-1, 2-4, 3-2, 3-3, 4-1, 4-2, IEC 61511, IEC 61508. Replaced the single placeholder IEC 62443 entry with the family.

### Other updates

- [`operations/README.md`](operations/README.md) (1.1.0 → 1.2.0): added "Sub-directories" section listing `operations/ot/`.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.25.3 → 1.26.0): new index row for the OT overview annex.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): OT/ICS row updated from `Referenced / Planned / TODO P6.2` to `Partial / In library / Phase 22 in progress` with link to `operations/ot/`.

### Doctrinal choices recorded

- **Sub-directory under operations**, not new top-level `/ot/` domain. Reflects the IT/OT convergence reality that the modern adopter governs both.
- **OT (not OT/ICS) as the umbrella term**, following NIST SP 800-82 Rev 3 nomenclature (renamed from "ICS Security" to "OT Security" in 2023). ICS, SCADA, DCS, PLC, BMS, SIS are all subsumed.
- **IEC 62443 as primary alignment**, NIST SP 800-82 Rev 3 as secondary. Both authoritative; IEC 62443 has broader international applicability.

### Library version

`2026.05.7` → `2026.05.8`. README `1.7.0` → `1.7.1`.

### Next

Phase 22.2 (OT/ICS Security Standard) will codify the segmentation, zone-and-conduit, security-level, and access-control requirements introduced conceptually in the overview annex.

All 12 audits clean.

## Phase 21.9 (2026-05-29, Library Version 2026.05.5): Metadata line-break convention library-wide

Library-wide rollout of the metadata-block line-break convention pilot tested in Library Version 2026.05.4 (PR #50). All governance documents now use the CommonMark §6.7 backslash-newline hard-line-break marker (`\`) between metadata fields, replacing the previous single-trailing-space pattern that GitHub correctly rendered as a soft line break (collapsing the metadata block into one paragraph).

### Why this change

Before this phase, every metadata block in every document ended each line with a single trailing space, which is **not** a valid CommonMark hard line break. CommonMark §6.7 requires either two-or-more trailing spaces or a literal backslash. GitHub correctly rendered the broken markup as one continuous paragraph, with metadata fields running together. The defect was invisible until viewed on GitHub.

### Why backslash-newline rather than two trailing spaces

A pure-CommonMark alternative without HTML mixing. The two-trailing-space variant is invisible in source and gets stripped by most editors on save (this is almost certainly how the original defect was introduced). The backslash is a real character, visible in source, and editor-safe. Pure-markdown renderers (Pandoc, LaTeX converters, static-site generators with HTML disabled) preserve hard line breaks via backslash but may strip raw `<br>` tags.

### Scope of change

- **290 files** had their metadata-block line endings converted from `Value ` (trailing space) to `Value\` (backslash before newline). The final line of each block does not require the marker because the following blank line and `---` separator create a paragraph break.
- The conversion was mechanical; no content semantics changed.

### Tooling updates

- **[`tools/lint-metadata.py`](tools/lint-metadata.py)**: new `check_line_break_markers` function asserts every metadata line (except the last) ends with `\`. Applied to every active document and to domain README files. `extract_metadata` updated to strip the trailing backslash when capturing field values.
- **[`tools/build-taxonomy.py`](tools/build-taxonomy.py)**: `extract_metadata` updated to strip the trailing backslash.
- **[`tools/check-review-cadence.py`](tools/check-review-cadence.py)**: same fix.
- **[`tools/lint-roles.py`](tools/lint-roles.py)**: role-extraction normalisation strips trailing backslash.
- **[`tools/lint-filename-title-alignment.py`](tools/lint-filename-title-alignment.py)**: title parser strips trailing backslash.

### Specification updates

- **[`specification-ingestion.md`](specification-ingestion.md)** (1.4.3 → 1.5.0): canonical metadata template updated to show the backslash-newline convention. Explanatory notes added: marker required on every line except the last; do not use two trailing spaces (invisible and fragile); the audit enforces.

### Pilot before rollout

Library Version 2026.05.4 (PR #50) applied the convention only to the main README so the rendering could be visually verified on GitHub before library-wide application. With confirmation, this phase applied the convention to all 290 remaining documents.

### Library version

`2026.05.4` → `2026.05.5`. README `1.6.4` → `1.6.5`. Specification-ingestion `1.4.3` → `1.5.0` (minor version bump because of the convention change).

All 12 audits clean.

## Phase 21.8 (2026-05-29, Library Version 2026.05.3): Adopter decision tree

Eighth sub-phase of Phase 21 (foundations before content expansion).

Eighth sub-phase of Phase 21 (foundations before content expansion). Second of two Priority 3 strategic-capability items. Closes the Priority 3 tier.

### New file

- [`docs/decision-tree.md`](docs/decision-tree.md): structured navigator answering "I have these characteristics; which library documents should I read first, in what order?". Eight sections:
  1. Adopter dimensions (size, sector, jurisdiction, regulated activities, technology footprint).
  2. Universal baseline (23 documents every adopter reads, in order).
  3. Sector-conditional content (7 sector profiles).
  4. Jurisdiction-conditional content (privacy jurisdictions, cross-sector horizontal regulations, trusted-trader programmes).
  5. Capability-conditional content (AI, cloud, software development, identity, OT).
  6. Phased adoption suggestions (30-day starter, 90-day implementation, 180-day expansion).
  7. Frequently asked navigation questions with concrete worked examples (50-person fintech in EU; 200-person 3PL in US/Canada/Mexico; 5-person UK SaaS; multinational healthcare; AI product builder).
  8. Pointer to gap register and TODO for unanswered questions.

### Convention

The decision tree references the glossary (Phase 21.2), the coverage gap register (Phase 21.7), and the document index register so that adopters can navigate between the structured reading order and the underlying source documents. It is informational and is not a tracked governance artefact (lives in `docs/` alongside the adopter guide).

### Result

The library now has a complete adopter-facing navigation stack:

- [`README.md`](README.md) for overview.
- [`docs/adopter-guide.md`](docs/adopter-guide.md) for general adoption principles.
- [`docs/decision-tree.md`](docs/decision-tree.md) for structured reading order based on adopter profile (this PR).
- [`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) for the auto-generated portal and scorecard.
- [`governance/register-glossary.md`](governance/register-glossary.md), [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md), and [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) for reference.

### TODO

Priority 3.1 (adopter decision tree) removed. Priority 3 tier complete. Tier 4 (adopter UX) and Tier 5 (content expansion) remain.

### Library version

`2026.05.2` → `2026.05.3`.

All 12 audits clean.

## Phase 21.7 (2026-05-29, Library Version 2026.05.2): Coverage gap analysis register

Seventh sub-phase of Phase 21 (foundations before content expansion). First of two Priority 3 strategic-capability items. Introduces the library's honest disclosure of what it does **not** yet cover so adopters can set expectations and contributors can target gaps.

### New file

- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) (v1.0.0, Register doctype): structured catalogue of gaps across five dimensions.

### Coverage dimensions

1. **Industry sectors**: six sectors with `compliance/<sector>/` sub-directories recorded as Substantive; manufacturing, retail, hospitality, education recorded as Deferred (TODO P6); defence, mining, agriculture, real estate, media, gaming, cannabis recorded as Out of scope with rationale.
2. **Jurisdictions** (privacy, trade-security trusted-trader programmes, financial services, healthcare, AI): explicit Coverage and Status per jurisdiction. 25 privacy jurisdictions Substantive; 4 of approximately 94 trusted-trader programmes Substantive; the remaining 90+ Planned (TODO P5.1) or Deferred.
3. **Regulations and frameworks referenced but not detailed**: 12 instruments with their depth of treatment.
4. **Cloud and platform providers**: provider-agnostic content Substantive; AWS/Azure/GCP/Kubernetes/SaaS-specific overlays Deferred (TODO P6.1).
5. **Technical capability areas**: 19 capabilities with Coverage classification (Substantive / Partial / Referenced / None).
6. **Document-type capability gaps**: 7 doctype gaps recorded (adopter quickstart templates, interactive maturity assessment, implementation roadmaps, decision tree, etc.).

### Convention established

Coverage status uses four values: *Substantive*, *Partial*, *Referenced*, *None*. Lifecycle status uses *In library*, *Planned*, *Deferred*, *Out of scope*. The register is the source of truth for "is X covered?" questions.

### Cross-references updated

- [`governance/README.md`](governance/README.md): register entry added to Active Documents.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.25.2 → 1.25.3): entry added.
- [`TODO.md`](TODO.md): P3.1 (coverage gap register) removed; remaining P3.2 (adopter decision tree) renumbered to P3.1.

### Library version

`2026.05.1` → `2026.05.2`.

All 12 audits clean.

## Phase 21.6 (2026-05-28, Library Version 2026.05.1): Filename and Document Title alignment audit

Sixth sub-phase of Phase 21. Closes the final Priority 2 item: an audit that catches typos and copy-paste defects where a file's name and its Document Title diverge.

### New file

- [`tools/lint-filename-title-alignment.py`](tools/lint-filename-title-alignment.py): permissive linter. For each active document, normalises both the filename's stem (after the doctype prefix) and the Document Title into a token set, and flags files where the two sets share **no** significant content words after normalisation. Honours a synonym table for legitimate acronym-in-filename / expansion-in-title patterns (SBOM, CAPA, FedRAMP, SOX, AEO, CTPAT, PIP, BASC, DORA, NIS, AI, and others).

### Result on initial run

- One match initially detected: [`supply-chain/register-sbom.md`](supply-chain/register-sbom.md) (filename uses the acronym, title uses the expansion "Software Bill of Materials Register"). Resolved by adding the SBOM → "software bill of materials" mapping to the synonym table. All 269 active documents now pass.
- No content changes to the corpus; the existing filenames and titles were already aligned once acronym synonyms were recognised.

### Tooling integration

- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new "Filename and Document Title alignment audit" step added between the standards-currency audit and the role audit. The library now runs **12 audits** per PR.
- [`tools/README.md`](tools/README.md): scripts table updated.

### Convention captured

The synonym table in the new linter doubles as a quick reference for which acronyms the library accepts in filenames. Adding new acronym-spelled filenames (for example, future country programmes) should update the synonym table at the same time.

### TODO

Priority 2.1 (filename ↔ Document Title alignment audit) removed. Priority 2 tier now complete.

All 12 audits clean. Library Version: 2026.05.1.

## Phase 21.5 (2026-05-28, Library Version 2026.05.0): Library-level CalVer versioning adopted

Fifth sub-phase of Phase 21 (foundations before content expansion). Resolves the absence of a library-level versioning scheme noted during Phase 20 review. Until now, each document carried its own semantic version, but the library as a whole had no declared version, leaving adopters to reference commit SHAs.

### Scheme adopted

Calendar Versioning (CalVer) of the form `YYYY.MM.patch`:

- `YYYY` is the four-digit year of the most recent merge to `main`.
- `MM` is the two-digit month of the most recent merge to `main`.
- `patch` is a sequential counter that increments on every merge to `main` within the same `YYYY.MM` window. It resets to `0` when the month rolls over.

Rationale for CalVer over SemVer:

- The library evolves continuously through small phased PRs rather than discrete versioned releases.
- The most useful question for an adopter is "how recent is this snapshot?", not "is this backwards-compatible?".
- The patch counter records cumulative churn within a month, surfacing the high merge frequency that semantic versioning would obscure.
- No judgment is needed to decide between major/minor/patch bumps; the scheme is mechanical.

### Files updated

- [`specification-master-project.md`](specification-master-project.md) (1.2.7 → 1.3.0): new section 4.5 "Library versioning" documenting the scheme, rationale, recording location, maintenance procedure, and relationship to per-document semantic versioning.
- [`README.md`](README.md) (1.5.4 → 1.6.0): metadata block restructured. The previous `**Version:**` field is renamed to `**README Version:**` (clarifying it tracks the README content, not the library). A new `**Library Version:**` field is introduced and set to the initial value `2026.05.0`. An explanatory sentence below the metadata block points to the specification.
- [`CHANGELOG.md`](CHANGELOG.md) (this file): preamble updated to reference the new versioning scheme. Phase headings now include the Library Version in effect at the time of the phase's completion.

### Initial value

The library version is initialised at `2026.05.0` by this Phase 21.5. Future PRs merged to `main` will increment the patch counter (2026.05.1, 2026.05.2, etc.) within the same calendar month. When the calendar month changes, the next merge sets the version to `YYYY.MM.0`.

### Maintenance

Each PR that merges to `main` updates [`README.md`](README.md)'s `Library Version` field as part of the PR. The audit suite does not automatically enforce monotonicity, but reviewers verify the bump is present before approving the PR.

### TODO

Priority 2.1 (library-level versioning policy) removed. Remaining P2 items: 2.1 (was 2.2) filename ↔ Document Title alignment audit.

All eleven audits clean.

## Phase 21.4 (2026-05-28): Related-Documents reciprocity rule considered and dropped

Fourth sub-phase of Phase 21 (foundations before content expansion). A draft reciprocity linter was implemented and empirically tested against the library; the test revealed 1,269 non-reciprocal Related-Documents references across 266 of 280 active documents.

### Finding

The library's actual convention is **asymmetric** Related Documents: each document lists "what this document consumes / relates to from its own perspective", not "the complete bidirectional graph". Authors curate Related Documents to be useful to a reader of that document, not to satisfy graph symmetry. This is a reasonable convention.

### Decision

The strict-reciprocity rule was dropped. Three reasons:

1. The convention is established and reasonable; enforcing strict reciprocity would require either rewriting 1,269 cross-references (mostly noise) or adopting an exemption-marker mechanism on every legitimately one-way reference (also extensive).
2. The underlying concern (catching half-updated cross-references during refactors) is already covered by [`lint-links.py`](tools/lint-links.py) (broken-link detection), which would catch the kind of file-rename mishap that drove this proposal.
3. A narrower doctype-pair rule (Framework↔Standard, Policy↔Standard, Charter↔Framework) was considered but rejected: the marginal value over [`lint-links.py`](tools/lint-links.py) does not justify the maintenance cost of a curated rule set with many exemptions.

### Recorded in TODO

The decision is also recorded in a new `## Decisions log` section in [`TODO.md`](TODO.md) so the rationale is preserved if the question recurs.

### Result

No linter added. No code changes other than the TODO and CHANGELOG entries. Priority 2 list renumbered: former 2.2 (library-level versioning) becomes 2.1; former 2.3 (filename/title alignment) becomes 2.2.

## Phase 21.3 (2026-05-28): Standards-currency checker and canonical citations register

Third sub-phase of Phase 21 (foundations before content expansion). Introduces a positive-list catalogue of canonical standards citations and a new linter that detects stale references against it. Resolves the highest-leverage consistency risk identified during Phase 20 review: standards citations drifting as new versions are published.

### New files

- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (v1.0.0, Register doctype): positive list of standards citations across ISO/IEC, NIST, EU regulations and directives, North-American regulations, other privacy regulations, CSA frameworks, ISACA frameworks, MITRE adversary frameworks, OWASP, customs and trade, sector-specific standards, OECD, and ICAO/IMO. ~81 standards entries. For each: current version, publication date, topic, and known superseded versions for the linter to flag.
- [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py) (new audit): permissive linter. Parses the canonical citations register and flags references to versions listed as superseded. The register is the source of truth; new standards added to the catalogue extend the linter's coverage automatically. Complementary to [`lint-citations.py`](tools/lint-citations.py) (denylist for hallucinations) rather than replacing it.

### Existing-content fixes triggered by the new linter

Initial run of the new linter detected two stale citations:

- [`governance/framework-human-capital-and-ethical-conduct.md`](governance/framework-human-capital-and-ethical-conduct.md) (1.0.0 → 1.0.1): "ISO 37001:2016" → "ISO 37001:2025" (ISO 37001 was revised and republished in February 2025).
- [`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md) (1.0.0 → 1.0.1): same correction.

### Tooling integration

- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new "Standards-currency audit" step added to the CI pipeline. The library now runs 11 audits on every PR and push.
- [`tools/README.md`](tools/README.md): scripts table expanded to document all linters including the new standards-currency one (previously listed only 4 of the 8 scripts).
- [`tools/lint-citations.py`](tools/lint-citations.py): PATH_EXEMPTIONS extended to include [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (the canonical register intentionally documents hallucinated/superseded strings as part of its scope).

### Cross-references updated

- [`governance/README.md`](governance/README.md): canonical citations register entry added to Active Documents.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.25.1 → 1.25.2): canonical citations register entry added.
- [`TODO.md`](TODO.md): P1.1 (standards-currency checker + canonical citations catalogue) removed; Priority 1 tier now complete.

### Result

Every PR adding new content will now have its standards citations automatically checked against the canonical register. When a new version of a listed standard is published, updating the register's "Superseded versions" column will surface every stale citation in the library on the next CI run.

All eleven audits clean.

## Phase 21.2 (2026-05-28): Glossary and acronym index

Second sub-phase of Phase 21 (foundations before content expansion). Introduces a single canonical resolved reference for the acronyms and external-domain terms used throughout the library.

### New file

- [`governance/register-glossary.md`](governance/register-glossary.md) (v1.0.0, Register doctype): alphabetical glossary covering ~150 acronyms and external terms used by the library, including regulatory bodies (HMRC, CBSA, CBP, OCC, PRA, FCA, MAS, FSA, NERC, TSA, etc.), regulations (GDPR, CPPA, CCPA, PIPL, LGPD, AIDA, DORA, HIPAA, HITECH, MDR, IVDR, SOX, etc.), frameworks and standards (WCO SAFE, ISO 27001 family, NIST AI RMF, COBIT, MITRE ATT&CK, MITRE ATLAS), sector programmes (AEO-UK, CTPAT, PIP, BASC, NEEC, ATT, STP, SES), CSA CCM domain codes (AAC, AIS, BCR, CCC, CEK, DCS, DSP, GRC, HRS, IAM, IPY, IVS, LOG, SEF, STA, TVM, UEM), CSA AICM, library role acronyms (AIGC, ERC, BCM, DPO), and common technical/security/governance acronyms (IAM, PAM, ZTNA, SBOM, SCA, SAST, SIEM, MFA, PKI, HSM, RPO, RTO, KRI, KPI, RACI, etc.).

The glossary also includes a doctype reference section explaining the library's doctype vocabulary (Annex, Charter, Framework, Guideline, Matrix, Plan, Policy, Procedure, Register, Roadmap, SOP, Specification, Standard, Template).

### Scope distinction established

Two related registers now serve complementary purposes:

- **[`register-glossary.md`](governance/register-glossary.md)** (new): acronyms and external-domain terms (regulations, standards, frameworks, regulators, sector programmes, technical concepts).
- **[`register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md)** (existing, 1.1.0 → 1.1.1): library-internal GRC concepts (Audit, Authorize, Control, Owner roles, Exception, etc.).

Both registers now cross-reference each other and explain their scope distinction in their Purpose sections.

### Cross-references updated

- [`governance/README.md`](governance/README.md): glossary entry added to the Active Documents table.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.25.0 → 1.25.1): glossary entry added.
- [`TODO.md`](TODO.md): P1.1 (glossary) removed; remaining P1 items renumbered.

All ten audits clean.

## Phase 21.1 (2026-05-28): Backlog file established

First sub-phase of Phase 21 (project foundations before content expansion). Introduces [`TODO.md`](TODO.md) at the repository root as the canonical living backlog. Completed work is recorded here in [`CHANGELOG.md`](CHANGELOG.md); pending work is recorded in [`TODO.md`](TODO.md). The two files together form the project's working history-and-future record.

### New file

- [`TODO.md`](TODO.md) (root, no metadata block per convention for root meta-files): seeded with the prioritised enhancement list discussed during Phase 20 review. Six priority tiers from foundations (glossary, standards-currency checker) through content expansion (logistics country additions, financial-services regulators, healthcare/energy/telecom/public-sector country overlays, AI jurisdictions, privacy jurisdiction gaps) to domain-level expansion (cloud, OT/ICS, identity, PQC, cross-framework matrix expansion).

### Rationale

The project has been growing in scope across Phases 19 and 20 with a number of deferred items captured only in conversation. Capturing them in a tracked file in the repository ensures:
- Continuity across sessions, contributors, and AI-assisted authorship cycles.
- Honest disclosure of what's queued versus what's done.
- A natural prioritisation framework before scaling country and sector content.

### Convention established

Root-level meta-files ([`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md), [`TODO.md`](TODO.md)) are maintained at a simpler standard than tracked governance artefacts: no full 13-field metadata block, no per-document version tracking, no taxonomy or portal inclusion. They are informational and operate as project meta-infrastructure rather than tracked GRC content.

All ten audits clean.

## Phase 20.2 (2026-05-28): Other industry-sector sub-directories

Second sub-phase of Phase 20. Phase 20.1 established the `compliance/<sector>/` sub-directory pattern for logistics. Phase 20.2 applies the same pattern to the remaining five industry sectors so that all sector-conditional compliance content lives under its respective sector sub-directory.

### Sub-directories created

- `compliance/financial-services/` — banks, investment firms, insurers, payment institutions, financial-market infrastructures.
- `compliance/healthcare/` — healthcare providers, payers, medical-device manufacturers, healthcare technology platforms.
- `compliance/energy-and-utilities/` — electricity, gas, water, district heating, renewable-energy operators.
- `compliance/telecommunications/` — telecom network operators, ISPs, internet exchange points, electronic communications service providers.
- `compliance/public-sector/` — government agencies, public bodies, and cloud-service providers to public sector.

Each sub-directory has a [`README.md`](README.md) (v1.0.0) describing the sector, applicability, the artefacts within, and future-coverage placeholders for country/regulator-specific overlays.

### Files moved

| Origin | Destination | Notes |
| --- | --- | --- |
| [`compliance/annex-financial-services-sector-requirements.md`](compliance/annex-financial-services-sector-requirements.md) | [`compliance/financial-services/annex-financial-services-sector-requirements.md`](compliance/financial-services/annex-financial-services-sector-requirements.md) | Path move; version bump |
| [`compliance/annex-dora-implementation.md`](compliance/annex-dora-implementation.md) | [`compliance/financial-services/annex-dora-implementation.md`](compliance/financial-services/annex-dora-implementation.md) | EU financial-services regulation; path move |
| [`compliance/annex-sox-itgc.md`](compliance/annex-sox-itgc.md) | [`compliance/financial-services/annex-sox-itgc.md`](compliance/financial-services/annex-sox-itgc.md) | US financial-services regulation; path move |
| [`compliance/annex-healthcare-sector-requirements.md`](compliance/annex-healthcare-sector-requirements.md) | [`compliance/healthcare/annex-healthcare-sector-requirements.md`](compliance/healthcare/annex-healthcare-sector-requirements.md) | Path move |
| [`compliance/annex-energy-and-utilities-sector-requirements.md`](compliance/annex-energy-and-utilities-sector-requirements.md) | [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md) | Path move |
| [`compliance/annex-telecommunications-sector-requirements.md`](compliance/annex-telecommunications-sector-requirements.md) | [`compliance/telecommunications/annex-telecommunications-sector-requirements.md`](compliance/telecommunications/annex-telecommunications-sector-requirements.md) | Path move |
| [`compliance/annex-public-sector-requirements.md`](compliance/annex-public-sector-requirements.md) | [`compliance/public-sector/annex-public-sector-requirements.md`](compliance/public-sector/annex-public-sector-requirements.md) | Path move |
| [`compliance/annex-fedramp-requirements.md`](compliance/annex-fedramp-requirements.md) | [`compliance/public-sector/annex-fedramp-requirements.md`](compliance/public-sector/annex-fedramp-requirements.md) | US federal cloud regulation; path move |

### Held at `compliance/` root (horizontal cross-sector regulation)

- [`compliance/annex-nis-2-implementation.md`](compliance/annex-nis-2-implementation.md) — EU NIS 2 Directive applies to "essential and important entities" across energy, transport, banking, healthcare, digital infrastructure, and other sectors. Not naturally one sector. Stays at root.

### Library-wide cross-reference updates

- All references to the eight moved files (across ~10 documents) updated to new paths.
- Internal sibling references within moved files updated from `../security/` to `../../security/` style (the files are now one level deeper).
- Internal compliance-sibling references in moved files updated from `(filename.md)` to `(../filename.md)`.
- [`compliance/README.md`](compliance/README.md) (1.3.0 → 1.4.0): sector sub-directory table expanded to list all six sectors; per-sector artefact tables added.

### Result

The compliance domain now consistently organises sector-specific content under sub-directories: `logistics/`, `financial-services/`, `healthcare/`, `energy-and-utilities/`, `telecommunications/`, `public-sector/`. The pattern scales to new sectors (when added) and to country-specific regulator overlays within each sector (as adopters require).

All ten audits clean. Taxonomy and portal regenerated.

## Phase 20.1 (2026-05-28): Logistics sector consolidation

First sub-phase of Phase 20 (compliance sub-directory restructure). Phase 12.3 had moved BASC into a new `/sectors/` top-level directory, which was inconsistent with the established pattern of sector-specific content living in `/compliance/` (where AEO-UK, CTPAT, PIP, and the sector annexes already lived). Phase 20.1 reverses that misstep and establishes the `compliance/<sector>/` sub-directory pattern, beginning with logistics.

### What changed

The library now hosts all trade-and-logistics sector-conditional content in a single `compliance/logistics/` sub-directory. The `/sectors/` directory has been deleted entirely.

### Files moved into `compliance/logistics/`

| Origin | Destination | Notes |
| --- | --- | --- |
| [`sectors/basc/policy-basc-information-security.md`](sectors/basc/policy-basc-information-security.md) | [`compliance/logistics/policy-basc-information-security.md`](compliance/logistics/policy-basc-information-security.md) | Path move; version 1.1.1 |
| [`sectors/basc/register-basc-it-responsibilities.md`](sectors/basc/register-basc-it-responsibilities.md) | [`compliance/logistics/register-basc-it-responsibilities.md`](compliance/logistics/register-basc-it-responsibilities.md) | Path move; version 1.1.1 |
| [`sectors/basc/register-basc-it-compliance-kpis.md`](sectors/basc/register-basc-it-compliance-kpis.md) | [`compliance/logistics/register-basc-it-compliance-kpis.md`](compliance/logistics/register-basc-it-compliance-kpis.md) | Path move; version 1.1.1 |
| [`sectors/basc/README.md`](sectors/basc/README.md) | [`compliance/logistics/annex-basc-programme-overview.md`](compliance/logistics/annex-basc-programme-overview.md) | Doctype conversion (Register → Annex); content preserved; version 1.1.0 |
| [`compliance/annex-transportation-and-logistics-sector-requirements.md`](compliance/annex-transportation-and-logistics-sector-requirements.md) | [`compliance/logistics/annex-logistics-sector-requirements.md`](compliance/logistics/annex-logistics-sector-requirements.md) | Renamed; sector overview; title shortened to "Logistics Sector GRC Requirements Annex"; version 1.0.1 |
| [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](compliance/annex-aeo-s-it-cybersecurity-requirements.md) | [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md) | Renamed for jurisdiction clarity; title "UK AEO-S IT and Cybersecurity Requirements"; version 1.0.1 |
| [`compliance/procedure-aeo-it-self-assessment.md`](compliance/procedure-aeo-it-self-assessment.md) | [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md) | Renamed; title "UK AEO IT Self-Assessment Procedure"; version 1.0.1 |
| [`compliance/register-ctpat-it-controls.md`](compliance/register-ctpat-it-controls.md) | [`compliance/logistics/register-ctpat-united-states-it-controls.md`](compliance/logistics/register-ctpat-united-states-it-controls.md) | Renamed; title "US CTPAT IT and Cybersecurity Compliance Controls Register"; version 1.0.2 |
| [`compliance/register-pip-compliance-controls.md`](compliance/register-pip-compliance-controls.md) | [`compliance/logistics/register-pip-canada-controls.md`](compliance/logistics/register-pip-canada-controls.md) | Renamed; title "Canada PIP IT and Cybersecurity Compliance Controls Register"; version 1.0.1 |
| [`supply-chain/register-ctpat-full-msc-controls.md`](supply-chain/register-ctpat-full-msc-controls.md) | [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](compliance/logistics/register-ctpat-united-states-msc-controls.md) | Cross-domain move; renamed; title "US CTPAT Full Minimum Security Criteria Controls Register"; version 1.0.2 |
| [`compliance/template-trade-compliance-gap-assessment.md`](compliance/template-trade-compliance-gap-assessment.md) | [`compliance/logistics/template-trade-compliance-gap-assessment.md`](compliance/logistics/template-trade-compliance-gap-assessment.md) | Path move; version 1.0.1 |

### New files

- [`compliance/logistics/README.md`](compliance/logistics/README.md) (new, v1.0.0): sector home, programme index, applicability, future-coverage placeholders.

### Files deleted

- [`sectors/README.md`](sectors/README.md) and [`sectors/basc/README.md`](sectors/basc/README.md): content preserved as [`annex-basc-programme-overview.md`](compliance/logistics/annex-basc-programme-overview.md) and consolidated into the new [`compliance/logistics/README.md`](compliance/logistics/README.md).
- `sectors/` directory removed entirely.

### Library-wide cross-reference updates

- All `[\`sectors/\`](../sectors/)` pointers (44 across the library, introduced in Phase 19.1/19.4) updated to point to `[\`compliance/\`](../compliance/)`.
- All references to renamed files (CTPAT/AEO/PIP/transport-annex/trade-template) updated to new paths and filenames.
- [`supply-chain/README.md`](supply-chain/README.md) (1.2.0 → 1.3.0): CTPAT MSC register row removed (file moved to compliance/logistics/); trusted-trader programme list replaced with a pointer to `compliance/logistics/`.
- [`compliance/README.md`](compliance/README.md) (1.2.0 → 1.3.0): restructured to describe the root-vs-sector layer separation; logistics sub-directory artefacts listed; pending Phase 20.2 sector moves flagged.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.24.2 → 1.25.0): all moved/renamed entries updated; category labels normalised from "Sectors" to "Compliance" for the BASC artefacts.
- [`README.md`](README.md) (1.5.3 → 1.5.4): document-count description updated to reference compliance sub-directories rather than `/sectors/`.
- [`specification-master-project.md`](specification-master-project.md) (1.2.6 → 1.2.7): repository directory listing and domain table updated.
- [`docs/adopter-guide.md`](docs/adopter-guide.md): "The sectors directory" section replaced with "Sector-conditional content".

### Tooling update

- [`tools/lint-structure.py`](tools/lint-structure.py): removed `sectors` from the `DOMAINS` list (the directory no longer exists). The structural-membership rule now requires that all `compliance/logistics/*` files are referenced by [`compliance/README.md`](compliance/README.md), which they are.

### Result

The library now has one consistent home for sector-conditional compliance content. The logistics sub-directory pattern is established and ready to scale to the 90+ AEO/equivalent trusted-trader programmes globally. Future country-specific programme additions (Mexico NEEC, Australia ATT, Singapore STP, EU AEO, Japan AEO, etc.) drop into `compliance/logistics/` with no additional structural change.

The Phase 20.2 sub-phase will apply the same sub-directory pattern to the other industry sectors (financial-services, healthcare, energy-and-utilities, telecommunications, public-sector).

All ten audits clean. Taxonomy and portal regenerated.

## Phase 19.6 (2026-05-28): ISO/IEC 42005 and 42006 topic-attribution correction

Phase 19 sub-phase 6, resolving the topic-attribution concern flagged in the Phase 19.4 changelog. ISO/IEC 42006:2025 covers "Requirements for bodies providing audit and certification of artificial intelligence management systems" — that is, requirements for accreditation bodies who audit and certify AIMS implementations against ISO/IEC 42001. It is the AIMS analogue of ISO/IEC 27006 (which provides the equivalent requirements for ISO/IEC 27001 audit bodies). The standard covering AI impact assessment guidance is ISO/IEC 42005:2025, published in May 2025.

Several documents in the library had been authored before ISO/IEC 42005 was published and had assigned the AI Impact Assessment topic to ISO 42006 by mistake. Phase 19.6 corrects the attribution.

### Citations corrected (topic was impact-assessment, attribution moved to ISO/IEC 42005:2025)

- [`ai/procedure-ai-evaluation.md`](ai/procedure-ai-evaluation.md) (1.0.1 → 1.0.2): framework alignment row updated to "ISO/IEC 42005:2025 | AI system impact assessment | Risk and bias evaluation".
- [`ai/standard-ai-testing-validation-and-documentation.md`](ai/standard-ai-testing-validation-and-documentation.md) (1.0.0 → 1.0.1): Purpose paragraph alignment list and framework alignment row both updated to ISO/IEC 42005:2025.
- [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md) (1.3.1 → 1.3.2): Step 5 consultation rule ("AIGC conducts additional review per ISO 42006") and the framework-mapping table row ("AI Impact Assessment | ISO 42006") both updated to ISO/IEC 42005:2025.
- [`security/policy-acceptance-into-service.md`](security/policy-acceptance-into-service.md) (1.0.0 → 1.0.1): rule 4.3 ("AI Impact Assessments must evaluate transparency, fairness, and explainability per ISO 42006") updated to ISO/IEC 42005:2025.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.24.1 → 1.24.2): three index rows updated where the document's topic is impact assessment — AI System Impact Assessment Procedure, AI Testing/Validation/Documentation Standard, AI Evaluation Procedure.

### Citations clarified (topic was audit/certification, attribution retained as ISO 42006 with status updated)

- [`ai/register-model-registry.md`](ai/register-model-registry.md) (0.0.1 → 0.0.2): "ISO/IEC 42006 | AI system audit | Audit baseline" updated to "ISO/IEC 42006:2025 | Requirements for AIMS audit and certification bodies | Audit baseline" to make the actual scope of the standard explicit. The model registry's use of ISO 42006 for audit-baseline context is correct.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): two index rows where the topic is audit/certification — AI System Audit and Certification Framework, Model Registry — kept ISO 42006 attribution and updated to "ISO/IEC 42006:2025".

### Standards now correctly cited in the library

| Standard | Scope | Citation context |
|---|---|---|
| ISO/IEC 42001:2023 | AI management system requirements | All AI governance, lifecycle, and assurance documents |
| ISO/IEC 42005:2025 | AI system impact assessment guidance | Impact assessment procedure, evaluation procedure, testing-validation-documentation standard, privacy impact procedure, acceptance-into-service policy |
| ISO/IEC 42006:2025 | Requirements for bodies providing audit and certification of AIMS | AI System Audit and Certification Framework, Model Registry, document index rows for audit-related artefacts |

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.5 (2026-05-28): Document count and BrE licence normalisation

Phase 19 sub-phase 5. Two low-severity findings.

### L-1: README document count

- [`README.md`](README.md) (1.5.2 → 1.5.3, patch-level per the main-README rule): the document count description said "approximately **240 documents**". Actual count: 282 documents in active domain directories (`ai/`, `architecture/`, `compliance/`, `dev-security/`, `governance/`, `operations/`, `privacy/`, `resilience/`, `risk/`, `security/`, `supply-chain/`, `sectors/`), excluding domain READMEs. Updated to "approximately **280 documents**" — still an approximation as the description states, with the actual count expected to fluctuate as Phase 19 sub-phases progress.

### L-2: BrE licence noun normalisation (body content)

The library uses Oxford English (BrE word stems + `-ize` verb endings). The noun `license` in body content was inconsistent with the convention — BrE uses `licence` for the noun and `license` for the verb. The metadata field name `License` and the [`LICENSE`](LICENSE) repository-root file are GitHub conventions left as-is.

Files updated:

- [`NOTICE.md`](NOTICE.md) (1.0.0 → 1.0.1): title and 3 body usages (incl. document title "External Reference Materials and Licence Boundaries").
- [`README.md`](README.md) (1.5.2 → 1.5.3): 2 body usages plus the L-1 count change.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): 3 body usages (no metadata block; not version-tracked).
- [`specification-master-project.md`](specification-master-project.md) (1.2.5 → 1.2.6): Review Frequency field reference and one body usage.
- [`specification-ingestion.md`](specification-ingestion.md) (1.4.2 → 1.4.3): Review Frequency field reference, section heading "Licence compatibility rules", and 2 body usages.
- [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md): 2 body usages (no metadata block; not version-tracked).
- [`ai/framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md) (1.1.0 → 1.1.1): 1 body usage.
- [`ai/README.md`](ai/README.md): section heading "Licence boundary".
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.24.0 → 1.24.1): 1 body usage.
- [`governance/README.md`](governance/README.md): section heading "Licence boundary" and 1 body usage.
- [`governance/charter-governance-library.md`](governance/charter-governance-library.md) (1.1.0 → 1.1.1): Review Frequency field reference, 3 body usages, and 1 role-name body usage ("Licence Reviewer").
- [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) (1.1.1 → 1.1.2): 1 body usage.
- [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) (1.3.1 → 1.3.2): section heading "Licence" and 1 body usage.
- [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md) (1.4.0 → 1.4.1): section heading "Licence".
- [`compliance/financial-services/annex-financial-services-sector-requirements.md`](compliance/financial-services/annex-financial-services-sector-requirements.md) (1.0.0 → 1.0.1): 1 body usage.
- [`compliance/register-compliance-obligations-template.md`](compliance/register-compliance-obligations-template.md) (1.0.1 → 1.0.2): 1 body usage.
- [`dev-security/standard-developer-security-requirements.md`](dev-security/standard-developer-security-requirements.md) (1.0.0 → 1.0.1): 1 body usage.
- [`dev-security/standard-security-quick-reference.md`](dev-security/standard-security-quick-reference.md) (1.0.0 → 1.0.1): 2 body usages.
- [`dev-security/standard-software-composition-analysis.md`](dev-security/standard-software-composition-analysis.md) (1.1.0 → 1.1.1): section heading and 11 body usages (table column header "Licence Category", row headers, and inventory obligations bullets).
- [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) (1.0.0 → 1.0.1): 1 body usage.
- [`dev-security/standard-devops-security-requirements.md`](dev-security/standard-devops-security-requirements.md) (1.0.1 → 1.0.2): 1 body usage.
- [`dev-security/guideline-ai-coding-assistant-security.md`](dev-security/guideline-ai-coding-assistant-security.md) (1.0.1 → 1.0.1 — already bumped in Phase 19.4): 1 body usage (checklist label).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): section heading "Licence".
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md): 1 body usage (no metadata block; not version-tracked).
- [`dev-security/claude-rules/pipeline/cicd-gates.md`](dev-security/claude-rules/pipeline/cicd-gates.md): 1 body usage (no metadata block; not version-tracked).
- [`dev-security/claude-rules/ai/ai-security.md`](dev-security/claude-rules/ai/ai-security.md): 2 body usages (no metadata block; not version-tracked).
- [`operations/standard-certificate-authority-management.md`](operations/standard-certificate-authority-management.md) (1.3.0 → 1.3.1): 2 body usages.
- [`operations/register-asset-inventory.md`](operations/register-asset-inventory.md) (1.0.0 → 1.0.1): 1 body usage (table row label).
- [`resilience/README.md`](resilience/README.md): section heading "Licence boundary".
- [`sectors/README.md`](sectors/README.md): section heading "Licence and neutrality posture".
- [`compliance/logistics/annex-basc-programme-overview.md`](compliance/logistics/annex-basc-programme-overview.md): section heading "Licence boundary".
- [`security/README.md`](security/README.md): section heading "Licence boundary".
- [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md) (1.3.2 → 1.3.3): section heading "Licence".
- [`security/procedure-onboarding-and-offboarding.md`](security/procedure-onboarding-and-offboarding.md) (1.0.0 → 1.0.1): 1 body usage.
- [`supply-chain/README.md`](supply-chain/README.md): section heading "Licence boundary".

Additionally, the `Unlicenced` spelling in [`standard-software-composition-analysis.md`](dev-security/standard-software-composition-analysis.md) was corrected to `Unlicensed` (BrE/AmE shared participle adjective form; `Unlicenced` is non-standard in both).

### Not converted

- `License` as the metadata field name (defined library convention): kept (specification-master-project.md, specification-ingestion.md, instruction-ai-document-ingestion.md, docs/adopter-guide.md, tools/README.md).
- The [`LICENSE`](LICENSE) repository-root file: GitHub convention; kept.
- `licensed` (past-participle adjective): same spelling in BrE and AmE; kept.

### Result

Body content is now consistent BrE: `licence` (noun) and `license` (verb), parallel to the existing `practice/practise`, `defence/defend`, `analyse/analysis` patterns. The metadata field name `License` and the [`LICENSE`](LICENSE) file remain as GitHub-convention exceptions, documented above.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.4 (2026-05-28): Standards-currency and BASC-residue cleanup

Phase 19 sub-phase 4. Three findings from the exhaustive re-audit: an obsolete ISO 42006 status reference; a guideline document containing 11 normative `must` statements that belong in a standard, not a guideline; and additional baseline `Regional BASC Compliance Officer` references that Phase 12.3 and Phase 19.1 had not reached.

### M-1: ISO/IEC 42006 status correction

- [`ai/framework-ai-system-audit-certification.md`](ai/framework-ai-system-audit-certification.md) (1.0.0 → 1.0.1): the framework cited "ISO/IEC 42006 (draft 2024)" in its framework alignment table and "the ISO/IEC 42006 draft AI audit requirements" in its Purpose. The standard was published in 2025; references updated to "ISO/IEC 42006:2025".

A separate concern was flagged but not silently corrected: several documents (notably [`procedure-ai-evaluation.md`](ai/procedure-ai-evaluation.md), [`standard-ai-testing-validation-and-documentation.md`](ai/standard-ai-testing-validation-and-documentation.md), multiple register-document-index rows, [`procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md), and [`policy-acceptance-into-service.md`](security/policy-acceptance-into-service.md)) cite "ISO 42006" with the topic attribution "AI Impact Assessment". ISO/IEC 42006:2025 is the standard for bodies providing audit and certification of AI management systems; the AI-impact-assessment standard is ISO/IEC 42005:2025. Whether to retain the existing citations or correct them to ISO 42005 is left for the user's review in a subsequent pass — the topic-attribution correction is materially distinct from a status update.

### M-2: AI coding assistant guideline `must` → `should`

- [`dev-security/guideline-ai-coding-assistant-security.md`](dev-security/guideline-ai-coding-assistant-security.md) (1.0.0 → 1.0.1): 11 normative `must` statements softened to `should` so the document language matches its Guideline doctype. The substantive content (security rules loaded before generating code; tool access scoped to the minimum necessary; no standing write access to production; no direct push to main without human review; agentic sessions logged; destructive actions require human confirmation) is retained — only the modal verb is changed. Adopters who wish to enforce these requirements upgrade the document to a Standard or Policy in their own copy of the library.

### M-3: BASC baseline residue cleanup

Phase 12.3 moved BASC to a sector overlay, and Phase 19.1 closed four files. The exhaustive re-audit found 13 additional documents that still treated `Regional BASC Compliance Officer` as a baseline role or that retained dedicated BASC sections. Phase 19.4 cleans those:

- [`governance/framework-metrics-monitoring-and-performance-reporting.md`](governance/framework-metrics-monitoring-and-performance-reporting.md) (1.0.0 → 1.0.1)
- [`governance/framework-continuous-assurance-and-improvement.md`](governance/framework-continuous-assurance-and-improvement.md) (1.0.0 → 1.0.1)
- [`compliance/policy-legal-and-regulatory-compliance.md`](compliance/policy-legal-and-regulatory-compliance.md) (1.0.0 → 1.0.1)
- [`supply-chain/procedure-supplier-audit.md`](supply-chain/procedure-supplier-audit.md) (1.0.1 → 1.0.2)
- [`operations/procedure-media-handling-and-transport.md`](operations/procedure-media-handling-and-transport.md) (1.3.0 → 1.3.1)
- [`operations/procedure-security-monitoring-and-alert-management.md`](operations/procedure-security-monitoring-and-alert-management.md) (1.3.0 → 1.3.1)
- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) (1.4.0 → 1.4.1)
- [`security/sop-incident-escalation-matrix.md`](security/sop-incident-escalation-matrix.md) (1.2.0 → 1.2.1)
- [`security/framework-cryptographic-key-lifecycle.md`](security/framework-cryptographic-key-lifecycle.md) (1.0.0 → 1.0.1)
- [`security/standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md) (1.4.0 → 1.4.1)
- [`security/policy-network-communications-security.md`](security/policy-network-communications-security.md) (1.0.0 → 1.1.0): had a dedicated `BASC trade-network security controls` section with multiple programme-specific requirements; replaced with a `Sector-programme network security overlays` section that defers to `sectors/`. Minor version bump because the change replaced a numbered section.
- [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md) (1.3.1 → 1.3.2)
- [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md) (1.3.0 → 1.3.1)
- [`security/standard-data-classification-and-handling.md`](security/standard-data-classification-and-handling.md) (1.3.0 → 1.3.1): the dedicated `BASC and regional trade data handling` section was generalised to `Sector-programme data handling overlays` with deference to `sectors/`.

### Result

Across the four post-12.3 cleanup phases (12.3 initial, 19.1, 19.4), the BASC overlay is now consistently positioned: BASC appears as a named example of a sector programme in the running text, never as a baseline role, scoping assumption, or unconditional framework requirement. Where the user's organisation participates in BASC, the `compliance/logistics/` annex remains the authoritative source for the additional controls, roles, and timeframes.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.3 (2026-05-28): Role authority register completions

Phase 19 sub-phase 3. Two high-severity findings from the exhaustive re-audit: documents named "AI Security Maintainer" as Owner or Approving Authority on 10+ files but the role had no definition in the authoritative register (it was only suppressed via a linter exemption); documents named "Board Risk Committee" and "Enterprise Risk Committee (ERC)" as approval bodies but the register had no entry for either.

### Changes

- [`governance/register-role-authority.md`](governance/register-role-authority.md) (1.2.0 → 1.3.0): added three new authority-register entries — AI Security Maintainer (with explicit demarcation from CISO and AI Governance Approver), Board Risk Committee (board-level risk-appetite oversight, with consolidation pointer to the minimum-viable governance guideline), and Enterprise Risk Committee / ERC (executive-level forum delegated by the Board Risk Committee).
- [`tools/lint-roles.py`](tools/lint-roles.py): removed the AI Security Maintainer linter exemption because the role is now in the register itself; known-role count rose from 40 to 42.

### Result

The library's authoritative role definitions now match its actual role usage. Linter exemptions no longer mask undefined roles. Adopters reading the role authority register get the complete set of roles the library references, with explicit demarcation where roles could be confused.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.2 (2026-05-28): Sanitisation residue cleanup

Phase 19 sub-phase 2. Three findings from the exhaustive re-audit involved content that revealed the original drafting organisation's specific operating context where a CC0-licensed reusable template should use generic placeholder phrasing.

### Files updated

- [`privacy/register-cross-border-data-flow.md`](privacy/register-cross-border-data-flow.md) (1.0.0 → 1.0.1): the Data Residency example column referenced "US East data centre", a specific cloud region tied to one organisation's deployment. Replaced with the generic placeholder "Cloud region in destination country (specify provider and region)" so adopters fill in their own residency without first having to overwrite a residual example.
- [`supply-chain/template-supplier-security-questionnaire.md`](supply-chain/template-supplier-security-questionnaire.md) (1.0.0 → 1.0.1): five question rows used "our organisation" / "our data" / "our personal data" — first-person pronouns that read as residue from a specific organisation's internal version of the questionnaire. The document's own Purpose section already uses the formulation "the Organisation"; questions 1.5, 1.6, 7.4, 8.3, 9.1, and 9.5 are now consistent with that convention. Sample notification text in [`register-subprocessor-template.md`](supply-chain/register-subprocessor-template.md) was deliberately left in first person because the "we/our" appears inside a quoted email body the organisation sends to its customers — first-person pronouns are correct in that quoted speech.

### Result

Adopters cloning the library no longer encounter a specific cloud-region example or first-person "our organisation" phrasing in templates intended to be filled in or issued from the adopter's own organisational context.

Taxonomy and portal regenerated. All ten audits clean.

## Phase 19.1 (2026-05-28): BASC migration completion

Phase 19 sub-phase 1. The Phase 12.3 sector annex migration (in which BASC was moved from being treated as an organisation-wide baseline standard to being a sector overlay invoked only where the organisation participates in the BASC programme) was incomplete: four active documents retained content that scoped the organisation to BASC, named "Regional Compliance Officers" as a baseline role, or aligned the document's own framework table to BASC/WCO SAFE/ISO 28000 unconditionally. Phase 19.1 cleans that residue.

### Files updated

- [`operations/standard-network-security-and-segmentation.md`](operations/standard-network-security-and-segmentation.md) (1.3.0 → 1.4.0): removed BASC/Latin America scoping, the "BASC / Logistics" network zone row, the dedicated "BASC trade-network security controls" section, and the unconditional BASC/WCO SAFE/ISO 28000 framework rows; sector overlays now invoked via `sectors/` pointers throughout. Also generalised "prior ransomware incident" references to industry-experience phrasing.
- [`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md) (1.0.1 → 1.1.0): removed BASC from baseline framework alignment statement, baseline security-certification list, and References section; removed "Regional Compliance Officers" governance row; converted "BASC Compliance" evidence row, "BASC and regional compliance integration" step, contractual review clauses, and re-audit triggers to sector-conditional formulations.
- [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md) (1.1.0 → 1.2.0): generalised the Purpose paragraph that referenced "a prior security incident" requiring "approximately a 30-day phased recovery" to industry-experience phrasing about phased recovery from major security incidents, since adopting organisations must calibrate RTO/RPO, tier assignments, and phasing to their own incident history and risk appetite rather than to the original drafting organisation's history.
- [`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md) (1.3.0 → 1.4.0): removed BASC/Latin America scope item content, "Regional Compliance Officers" governance row, the "BASC Trade and Customs" retention row, and the unconditional BASC/WCO SAFE framework alignment rows; sector overlays now invoked via `sectors/` pointers throughout.

### Result

The four documents that still implicitly assumed BASC participation now read consistently with the sector-overlay pattern established in Phase 12.3: BASC appears only as an illustrative example of "a sector programme an organisation may participate in", parallel with CTPAT, AEO, PIP, HIPAA, and financial-services overlays.

Taxonomy regenerated. All ten audits clean.

## Phase 18 (2026-05-28): BrE/AmE spelling normalisation

Resolves the final editorial finding from the next-passes list (item 1.1). The library now uses consistent Oxford English (BrE word stems + -ize verb endings) throughout active content.

### Conversion applied

`organization*` → `organisation*` across active content (713 replacements across 191 files), preserving 18 proper-noun occurrences (World Customs Organization, International Maritime Organization, International Civil Aviation Organization, ISO's full title "International Organization for Standardization", and COBIT 2019 process names containing "Organizational").

### Library posture

The library now consistently uses Oxford English: BrE word stems (organisation, behaviour, centre, labelling, programme, colour, favour, honour) with -ize verb endings (organize, recognize, prioritize, etc.). The language linter continues to enforce the -ize ending convention and now benefits from the consistent BrE word stems.

### Not converted

- `license` (verb and noun) and the LICENSE file: GitHub convention; metadata field name; left as-is.
- `program` (technical contexts): the library already uses `programme` consistently in governance/operational contexts.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 17 (2026-05-28): Adopter-facing content

Adds the adopter-facing content identified by the next-passes list. Closes items 5.2 (decision tree), 5.3 (maturity progression), 5.5 (library health report template), and 5.6 (content feedback channel).

### Adopter guide enhancements

[`docs/adopter-guide.md`](docs/adopter-guide.md): two new substantial sections added.

- **Applicability decision tree**: a table of yes/no questions mapping organisational characteristics (handles personal data? operates AI? cloud workloads? customer-facing services? BASC certification? sector regulation?) to the library domains and sector annexes that apply. Enables adopters to quickly determine which subset of the library is relevant to their operating context.
- **Maturity progression**: explicit guidance keyed to the three tiers from the minimum-viable governance structure guideline. Tier 1 starter set lists 15 specific documents to adopt first; Tier 2 growth set adds the next layer; Tier 3 enterprise set adopts the full library. Each tier maps to the corresponding governance forum structure.
- **Sectors directory note**: brief sub-section noting that most organisations will skip `/sectors/` entirely.

### New artefact

- [`governance/template-library-health-report.md`](governance/template-library-health-report.md) (v0.0.1): eleven-section template for the quarterly library health report referenced (but previously not templated) by the Phase 11 library quality and review cadence procedure. Sections cover identification, executive summary, the ten-audit status table, content additions and retirements, review cadence state, drift hot-spots, incidents and lessons, contributor activity, adopter signal, next-period plan, and sign-off. Worked example fragment included.

### Content feedback channel

- [`CONTRIBUTING.md`](CONTRIBUTING.md): new "Reporting content issues without contributing a fix" section. Defines six issue categories (factual error, cross-document inconsistency, sanitisation residue, ambiguous responsibility, unsafe guidance, operational unrealism). Provides a non-PR channel for readers to raise concerns. Security-related defects continue to route through [`SECURITY.md`](SECURITY.md).

### Registry updates

- [`governance/README.md`](governance/README.md) (v1.2.0 → v1.3.0): new template added.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (v1.23.0 → v1.24.0): new row.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 16 (2026-05-28): CCM v4.1 domain code corrections

Resolves four CCM domain-code findings surfaced by the Phase 15 citation deep-dive. The Phase 12.1 corrective pass fixed the version string ("CSA CCM v5" → "CSA CCM v4.1") but did not migrate the v3-era domain codes that CSA renamed during the v3 → v4 transition. Three documents also used a domain code (TIM) that has never existed in any CCM version.

### Domain code corrections

Primary CSA sources (Cloud Controls Matrix and CAIQ v4.1 artifact; CCM v4.1 transition blog; CSF Tools CCM v4 reference) confirm the CCM v4.1 has exactly 17 domains: AIS, AAC, BCR, CCC, CEK, DCS, DSP, GRC, HRS, IAM, IPY, IVS, LOG, SEF, STA, TVM, UEM. The library used four codes that do not appear in this list:

| Stale code | Corrected to | Rationale |
| --- | --- | --- |
| GRM (Governance and Risk Management) | GRC (Governance, Risk, Compliance) | Renamed in v3 → v4 transition |
| EKM (Encryption and Key Management) | CEK (Cryptography, Encryption, Key Management) | Renamed and broadened in v3 → v4 transition |
| END (Endpoint Security) | UEM (Universal Endpoint Management) | Renamed and re-scoped in v3 → v4 transition |
| TIM (Threat Intelligence Management) | TVM (Threat and Vulnerability Management) | TIM never existed in any CCM version; threat intelligence is part of TVM |

### Replacements applied

25 replacements across 10 files. Specific numeric controls (GRM-12 → GRC-12, EKM-01 → CEK-01, etc.) substituted where the v3 control numbering plausibly maps to the v4 domain code with the same numeric sequence. TIM references — for which no number mapping is sound because the domain did not exist — rewritten to generic TVM domain references rather than swapping the prefix.

Affected files: [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md), [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md), [`security/procedure-cryptographic-key-operations.md`](security/procedure-cryptographic-key-operations.md), [`security/procedure-key-escrow-and-recovery.md`](security/procedure-key-escrow-and-recovery.md), [`security/framework-cryptographic-key-lifecycle.md`](security/framework-cryptographic-key-lifecycle.md), [`operations/standard-certificate-authority-management.md`](operations/standard-certificate-authority-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](operations/procedure-threat-intelligence-and-siem-operations.md), plus the framework alignment annotations on a small number of other files.

### Citation denylist extended

[`tools/lint-citations.py`](tools/lint-citations.py) extended with four new denylist entries (`CCM GRM`, `CCM EKM`, `CCM END`, `CCM TIM`) so the v3-era codes cannot be reintroduced silently.

### Not corrected (verified accurate)

- **CSA AICM v1.0.3**: confirmed real by CSA's official AICM artifact page. The Phase 15 audit flagged this as suspect; primary-source verification confirms the patch version is current. No change.
- **SEF-01 to SEF-10**: source evidence is ambiguous (some sources say 8 SEF controls, others say 10). Leaving the library's SEF-01 to SEF-10 reference unchanged pending unambiguous primary-source confirmation.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 15 (2026-05-28): Minimum-viable governance structure guideline

Resolves the forum-proliferation audit finding by adding a new adopter-facing guideline that shows how the library's 13+ named forums can be implemented at three maturity tiers (minimum viable, mid-market, enterprise / regulated). The library's individual documents continue to reference the formal forum names; this guideline shows the consolidation patterns that preserve the responsibilities for smaller adopters.

### New document

- [`governance/guideline-minimum-viable-governance-structure.md`](governance/guideline-minimum-viable-governance-structure.md) (v0.0.1): three-tier structure (Tier 1: 2-3 forums; Tier 2: 4-6 forums; Tier 3: 8-12 forums) mapping the library's formal forum names to consolidated bodies. Per-tier consolidation table, seat-name mapping by role group (senior executive, AI sub-roles, ownership, maintainer), and mapping-document worked example.

### Registry updates

- [`governance/README.md`](governance/README.md) (v1.1.0 → v1.2.0): new guideline added to active documents.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (v1.22.0 → v1.23.0): new row added.

Taxonomy, portal, and maturity scorecard regenerated.

A separate (in-flight) citation verification deep-dive is running for items 7.1-7.4 of the next-passes list; any resulting corrections will be applied in a future phase.

## Phase 14 (2026-05-28): Provisional-draft and ownership cleanup

Resolves three lingering status-uncertainty items and tightens AIGC ownership clarity.

### Provisional-draft banners removed

Three documents previously carried "Document Status: Provisional" banners with "Target formal review: Q3 2026" framing. The banners over-claimed uncertainty against the library's posture (every active document is intended as public-domain reference baseline). Removed; the substantive Limitations sections in each document remain.

- [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md) (v1.0.0 → v1.1.0): banner removed.
- [`supply-chain/standard-cloud-exit-and-data-portability.md`](supply-chain/standard-cloud-exit-and-data-portability.md) (v1.0.0 → v1.1.0): banner removed.
- [`security/sop-incident-escalation-matrix.md`](security/sop-incident-escalation-matrix.md) (v1.1.0 → v1.2.0): banner removed.

### AIGC ownership reconciliation

[`ai/charter-ai-governance-council.md`](ai/charter-ai-governance-council.md) (v1.1.0 → v1.2.0): new "Roles outside the council that report into it" sub-section in the Composition section. Documents how the three Phase 12.8 sub-roles (AI Governance Approver, AI Data Steward, AI System Inventory Keeper) report into the council via the AI Governance Lead secretariat. Charter administrative ownership (CIO), governance decisions (Council), and per-system approvals (Approver under delegated council authority) are explicitly disambiguated.

### Material change cross-references

Three operational triggers that say "material change" without specifying thresholds now point at the authoritative thresholds table:

- [`ai/charter-ai-governance-council.md`](ai/charter-ai-governance-council.md) §1: "Review material changes to deployed AI models" → cross-references the Material change thresholds table in the AI governance framework.
- [`ai/standard-ai-security-and-risk.md`](ai/standard-ai-security-and-risk.md) §6.1: "AI systems must be tested before release and after material change" → same cross-reference.
- [`ai/procedure-ai-evaluation.md`](ai/procedure-ai-evaluation.md) Step 5: "Rejected systems require material changes and full re-evaluation" → same cross-reference.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 13 (2026-05-28): Tooling hardening — two new linters and full audit-suite wire-up

Resolves the audit blind-spots that allowed the Phase 12 defect set to accrete: the linter suite now catches the patterns Phase 12 had to fix manually. The audit suite grows from 8 to 10 audits, all wired into pre-commit and CI.

### New linters

- [`tools/lint-shall-near-uncertainty.py`](tools/lint-shall-near-uncertainty.py) (new): detects mandatory `shall`/`must`/`will` requirements within 2 lines of uncertainty markers (`[Unverified]`, `TBD`, `TODO`, `FIXME`, `XXX`, `Draft <year/proper-noun>`, `placeholder`, `[Draft N Reference]`). Would have caught the Phase 12.5 finding before merge. Returns non-zero on findings.

- [`tools/lint-roles.py`](tools/lint-roles.py) (new): parses every `**Owner:**` and `**Approving Authority:**` value from document metadata blocks and verifies the value is either defined in [`governance/register-role-authority.md`](governance/register-role-authority.md) or in the linter's `EXTRA_KNOWN_ROLES` exemption set (for cross-functional bodies, alias roles, and named maintainer functions). Detects undefined-role usage that creates governance ambiguity. Skips obvious template placeholders (`<role title>`, `Role Name`, bracketed text).

### Role authority register expanded

- [`governance/register-role-authority.md`](governance/register-role-authority.md) (v1.1.0 → v1.2.0): nine additional roles added that were used in document metadata but not previously defined: Board of Directors, Chief Technology Officer, Chief Audit Executive, Security Owner, Communications Owner, IT Operations Lead, AI Risk Maintainer, Assurance Metrics Maintainer, Control Framework Maintainer. Total known roles in scanned files: 40 (was 22).

### Tooling pipeline wire-up

- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): extended to run all 10 audits locally on commit. Previously ran 6 (missing the four newer linters added in Phases 11, 12.1, 13).
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): extended to run all 10 audits in CI on push to main and on every PR.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): local-audit instructions extended to list all 10 audits.

### Result

The audit pipeline now catches:
1. Metadata block defects (lint-metadata).
2. Language and style defects including em/en dashes, BrE `-ise` endings, bare `ensure`, sanitisation residue, heading-case violations (lint-language).
3. Broken internal links (lint-links).
4. Structural defects such as documents missing from their domain README (lint-structure).
5. Hallucinated or stale framework version citations (lint-citations).
6. Undefined Owner/Approving Authority roles in metadata (lint-roles).
7. Mandatory requirements next to uncertainty markers (lint-shall-near-uncertainty).
8. Overdue document reviews past the action threshold (check-review-cadence).
9. Taxonomy drift between source documents and the auto-generated registry (build-taxonomy --check).
10. Portal and maturity-scorecard drift (build-portal --check).

Taxonomy regenerated. No content changes beyond the role-register expansion.

## Phase 12.10 (2026-05-28): Editorial and terminology consolidation

Resolves the remaining medium and low-severity findings from the comprehensive audit. Closes the corrective campaign at Phase 12.

### Term definitions added

- [`governance/register-key-terms-and-definitions.md`](governance/register-key-terms-and-definitions.md) (v1.0.0 → v1.1.0): 18 new term definitions added to close terminology drift:
  - AI lexicon: AI Agent, AI Capability, AI Service, AI System (refined), Foundation Model, Model — each formally distinguished so the reader can determine whether a ChatGPT API integration is an AI system, an AI service, a capability, or an agent.
  - Approval verbs: Approve, Audit, Authorize, Monitor, Review — each formally distinguished against the others.
  - Event vs Incident: Event = observation; Incident = triaged event meeting criteria.
  - Risk Appetite vs Risk Tolerance: Appetite = strategic/board statement; Tolerance = operational threshold.
  - Log: distinguished from Monitor, Audit, Review.
  - Supplier / Third Party / Vendor: defined with explicit canonical-preference note (library prefers "supplier" as the general term; "third party" reserved for legal-contractual contexts; "vendor" reserved for technology-supplier contexts).

### "Ensures compliance" phrasing replaced

[`governance/register-data-retention-schedule.md`](governance/register-data-retention-schedule.md), [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md), [`privacy/policy-privacy-and-data-governance.md`](privacy/policy-privacy-and-data-governance.md) (two instances): "ensures that compliance" replaced with "supports the organization's compliance" / "oversees compliance" so the library does not overclaim a guarantee CC0 baseline content cannot deliver.

### MASVS terminology clarification

[`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): a note added clarifying that MASVS v2 reorganised operational test groupings into MAS Testing Profiles in MASTG; the L1/L2/R concepts remain as verification-level shorthand used by this standard.

### RFC 7807 ↔ RFC 9457

[`architecture/standard-api-design.md`](architecture/standard-api-design.md): RFC 7807 reference annotated with the note that RFC 9457 supersedes it; both are listed in the framework alignment table.

### "Widely adopted" claims date-stamped

[`privacy/jurisdictions/annex-privacy-united-states.md`](privacy/jurisdictions/annex-privacy-united-states.md): "voluntary, widely adopted" → "voluntary; broadly adopted in US enterprise practice as of 2026".
[`privacy/jurisdictions/annex-privacy-singapore.md`](privacy/jurisdictions/annex-privacy-singapore.md): same pattern applied to the PDPC Model Governance Framework reference.

### AI-assistance transparency note

[`CONTRIBUTING.md`](CONTRIBUTING.md): new "AI-assisted authorship" section declaring that a substantial portion of the library was authored with AI assistance and then human-reviewed. Contributors are reminded that they remain accountable for content, that framework citations must be verified against primary sources (the citation linter prevents known-hallucination reintroduction but does not substitute for new-citation verification), and that organisation-neutrality must be preserved.

### Supplier Risk Maintainer role formalised

[`governance/register-role-authority.md`](governance/register-role-authority.md): "Supplier Risk Maintainer" added as a role distinct from "Supplier Owner" (the latter is per-supplier; the former maintains the cross-supplier governance content). Resolves the audit finding that "Supplier Risk Maintainer" was used as a metadata owner in supply-chain documents without being defined in the role authority register.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.9 (2026-05-28): AI procedure realism

Resolves six AI realism findings from the comprehensive audit. The AI domain now reads as more operationally honest about what is enforceable, what is best-effort, and what the procedure mechanics actually look like.

### Eval cadence realism

- [`ai/procedure-foundation-model-lifecycle.md`](ai/procedure-foundation-model-lifecycle.md) (v0.0.1 → v0.0.2) Step 5: "Eval suite regression run at least monthly" recalibrated to "at minimum quarterly; monthly where the eval-suite cost and infrastructure permit". Eval scope, sample size, and the metrics evaluated are explicitly required to be documented per model so the cadence is substantive rather than nominal.

### Material change thresholds harmonised

- [`ai/framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md) (v1.0.0 → v1.1.0): new "Material change thresholds" sub-section under the lifecycle model. Defaults specified across eight dimensions: capability performance (≥5%), cost (≥20%, consistent with the AI cost governance standard), user population, data category, tool surface, provider version, regulatory environment, supplier change. Two or more dimensions crossing simultaneously is material regardless of individual magnitude.

### Agent self-protection threat model

- [`ai/standard-ai-access-and-agent-permissions.md`](ai/standard-ai-access-and-agent-permissions.md) (v0.0.1 → v0.0.2): new §4.1.1 "Agent self-protection (defence in depth)". Seven controls covering allow-list enforcement point (outside the model, not by it), tool-registration boundary, schema validation, untrusted-content marker, cross-tool data-flow control, privilege-escalation prevention, and high-priority logging. Cross-reference to OWASP MCP Top 10 risk categories added.

### Identity propagation mechanics

- [`ai/standard-ai-access-and-agent-permissions.md`](ai/standard-ai-access-and-agent-permissions.md) §4.3.1: four concrete propagation patterns documented (Token Exchange RFC 8693, OAuth On-Behalf-Of, workload-identity-with-claim-propagation, step-up at the boundary), each with a "when appropriate" guideline. Boundary-validation requirements expanded with signature/issuer, audience, lifetime, subject-vs-agent, tenant scoping, replay protection. Token-format defaults documented (JWT per RFC 7519 with JWT BCP per RFC 8725; alternatives permitted).

### Deletion-propagation honest scope

- [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md) (v0.0.1 → v0.0.2) Step 6: new "Limits of deletion propagation (honest scope)" table distinguishing guaranteed outcomes (dataset removal, embeddings in active vector stores, backup copies at cycle) from best-effort outcomes (production-served models trained on the data, fine-tunes and adapters) from out-of-scope (external models the organisation does not control). Adopting organisations are explicitly enjoined to distinguish what they can guarantee from what is best-effort when communicating to data subjects and regulators.

### Hard cost ceiling enforcement architecture

- [`ai/standard-ai-inference-cost-governance.md`](ai/standard-ai-inference-cost-governance.md) (v0.0.1 → v0.0.2): new §3.1 "Enforcement architecture". Four layers documented in ordering preference: application middleware per-request gating (required and primary), provider rate-limit configuration (secondary safeguard), provider commitment ceiling (backstop), post-billing reconciliation (detective). Hard kill switch implementation explicitly placed in the application middleware layer; documented fallback behaviour (non-AI response, cached value, explicit message) when the switch is toggled. Kill-switch operation tested per the resilience programme.

### Coordination

The five AI documents touched in this phase are now individually operationally executable; an adopting organisation reading any one of them finds explicit mechanism, not just intent.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.8 (2026-05-28): AI Governance Maintainer role split

Resolves the role-bandwidth-overload finding by splitting the overloaded `AI Governance Maintainer` role into three named roles, each with a clearly bounded scope. The umbrella `AI Governance Lead` role retained as the secretariat / chair function on the AI Governance Council.

### New roles defined in [`governance/register-role-authority.md`](governance/register-role-authority.md) (v1.0.0 → v1.1.0)

- **AI Governance Approver** — approval decisions for AI policies, frameworks, standards, deployment gates, foundation-model selection, risk-classification approvals, and material lifecycle changes.
- **AI Data Steward** — training-data governance, dataset acceptance, deletion-propagation, lineage tracking, sensitive-content controls, and dataset documentation (datasheets).
- **AI System Inventory Keeper** — maintenance of the AI System Register, Model Registry, MCP server register, model cards, system cards, and cross-references between AI inventories and adjacent registers (ADM, resilience, supplier).

The umbrella `AI Governance Lead` role description updated to declare it as the AIGC secretariat role coordinating the three sub-roles.

### Documents reassigned

40 occurrences of `AI Governance Maintainer` across 19 files mapped to the appropriate new role.

Owner-field reassignments by responsibility area:

- **AI Governance Approver** (the policy/framework/decision standards): [`ai/README.md`](ai/README.md), [`ai/framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md), [`ai/framework-ai-model-risk.md`](ai/framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](ai/standard-ai-model-risk.md), [`ai/standard-ai-inference-cost-governance.md`](ai/standard-ai-inference-cost-governance.md), [`ai/procedure-foundation-model-lifecycle.md`](ai/procedure-foundation-model-lifecycle.md), [`ai/procedure-ai-model-risk-assessment.md`](ai/procedure-ai-model-risk-assessment.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](supply-chain/procedure-third-party-ai-due-diligence.md). Governance index rows for [`ai/policy-ai-compliance.md`](ai/policy-ai-compliance.md), [`ai/framework-ai-system-audit-certification.md`](ai/framework-ai-system-audit-certification.md), [`ai/checklist-ai-algorithmic-compliance.md`](ai/checklist-ai-algorithmic-compliance.md) also reassigned.
- **AI Data Steward** (training-data, datasheet): [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md), [`ai/template-dataset-datasheet.md`](ai/template-dataset-datasheet.md).
- **AI System Inventory Keeper** (registries, cards, lifecycle mapping): [`ai/register-model-registry.md`](ai/register-model-registry.md), [`ai/template-ai-system-register.md`](ai/template-ai-system-register.md), [`ai/template-model-card.md`](ai/template-model-card.md), [`ai/template-system-card.md`](ai/template-system-card.md), [`ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`](ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md).

Body-content references in seven files retargeted to the appropriate sub-role per responsibility area:

- [`ai/procedure-foundation-model-lifecycle.md`](ai/procedure-foundation-model-lifecycle.md): candidate-list maintenance → AI System Inventory Keeper.
- [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md): dataset acceptance and recording → AI Data Steward.
- [`ai/standard-ai-inference-cost-governance.md`](ai/standard-ai-inference-cost-governance.md): cost-dashboard ownership and anomaly summary → AI Governance Approver.
- [`ai/template-dataset-datasheet.md`](ai/template-dataset-datasheet.md): dataset sign-off role → AI Data Steward.
- [`ai/register-model-registry.md`](ai/register-model-registry.md): quarterly registry review → AI System Inventory Keeper.
- [`privacy/register-automated-decision-making.md`](privacy/register-automated-decision-making.md): cross-register consistency owner → AI System Inventory Keeper.
- [`resilience/register-resilience-metrics-and-testing-log.md`](resilience/register-resilience-metrics-and-testing-log.md): AI resilience metric owner → AI System Inventory Keeper.

A reader of any AI document now sees a single, scope-appropriate role; no role is asked to be the owner of approvals, data stewardship, and inventory maintenance simultaneously.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.7 (2026-05-28): Scope matrices for paired standards

Resolves three scope-collision findings from the comprehensive audit by adding explicit scope-boundary clauses to each affected document pair.

### Cloud baselines — operations vs dev-security

- [`operations/standard-cloud-security-configuration-baseline.md`](operations/standard-cloud-security-configuration-baseline.md) (v1.3.0 → v1.4.0): new §2.1 "Scope boundary with dev-security cloud hardening baselines" with a per-subject table mapping enterprise-tenant administration (this standard) to workload-level concerns (dev-security baselines).
- [`dev-security/standard-cloud-hardening-baseline-aws.md`](dev-security/standard-cloud-hardening-baseline-aws.md) (v0.0.1 → v0.0.2): new "Scope boundary with the operations cloud configuration baseline" sub-section.
- [`dev-security/standard-cloud-hardening-baseline-azure.md`](dev-security/standard-cloud-hardening-baseline-azure.md) (v0.0.1 → v0.0.2): same.
- [`dev-security/standard-cloud-hardening-baseline-gcp.md`](dev-security/standard-cloud-hardening-baseline-gcp.md) (v0.0.1 → v0.0.2): same.

A workload now reads as conforming to both standards with a clear division of authority.

### Logging vs observability — routing rule

- [`security/standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md) (v1.3.0 → v1.4.0): new "Scope boundary with the operations observability and telemetry standard" sub-section with an event-class routing table. Security-relevant events route to SIEM; operational signals route to observability; dual-purpose events emitted to both with shared trace identifiers. Also: BASC residue in the Scope section (caught here, missed by Phase 12.3) replaced with a sector-overlay pointer.
- [`operations/standard-observability-and-telemetry.md`](operations/standard-observability-and-telemetry.md) (v0.0.1 → v0.0.2): reciprocal note pointing back to the security standard's routing table.

### API design vs API security — approval sequence

- [`architecture/standard-api-design.md`](architecture/standard-api-design.md) (v0.0.1 → v0.0.2): new "Relationship to the API security standard and approval sequence" sub-section documenting the design-gate → threat-model-gate → implementation sequence.
- [`dev-security/standard-api-security.md`](dev-security/standard-api-security.md) (v0.0.1 → v0.0.2): reciprocal sub-section with the same sequence; conditional-endorsement loop documented for cases where a security finding requires reshaping the contract.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.5 / 12.6 (2026-05-28): [Unverified] tags, phantom dependency, internal hostname

Resolves the `[Unverified]`-tag-in-mandatory-policy finding, the phantom "IT Operations Documentation Framework" dependency, and the internal-looking hostname in an AI code example. Bundled as a single change for compactness.

### `[Unverified]` tags removed from mandatory policy text

- [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) (v1.0.0 → v1.0.1):
  - §7.1: removed `[Unverified]` marker and softened "shall implement" to "may implement"; the machine-readable exception registry is reclassified as a recommended practice rather than a mandatory `shall` obligation.
  - §7 heading updated from "(future readiness)" to "(recommended where automation is practical)".
  - References table: removed `[Unverified]` qualifier on the NIST AI RMF 1.0 entry.
  - Compliance mapping table: replaced `[Draft 2026 Reference]` / `[Unverified]` cells with concrete framework references for the recommended-registry row.
- [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md) (v1.0.0 → v1.0.1):
  - §5.3: removed `[Unverified]` marker; reframed as a where-cost-justifies recommendation.
  - References list: removed the "Draft 2026 ISO 37301 Revision" `[Unverified]` entry.

### Phantom "IT Operations Documentation Framework" dependency resolved

- [`compliance/policy-compliance-and-audit-management.md`](compliance/policy-compliance-and-audit-management.md) §2.4: replaced the reference with concrete pointers to [`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md) (for retention) and [`operations/framework-it-service-management.md`](operations/framework-it-service-management.md) (for ITSM-aligned documentation).
- [`resilience/plan-it-disaster-recovery.md`](resilience/plan-it-disaster-recovery.md): same reference replaced with a concrete pointer to the recovery runbook template.

### Internal hostname in AI code example replaced with generic placeholders

- [`ai/guide-ai-security-technical-implementation.md`](ai/guide-ai-security-technical-implementation.md) (v1.3.0 → v1.3.1) line 493: `Server=db-server.internal;Database=AppDB` replaced with `Server=[DATABASE_HOSTNAME];Database=[DATABASE_NAME]`. The example continues to demonstrate the prohibited pattern but no longer reads as sanitisation residue from an internal codebase.

### Citation denylist extended

[`tools/lint-citations.py`](tools/lint-citations.py) denylist now also pins "Draft 2026 ISO 37301" and "IT Operations Documentation Framework" so neither can be reintroduced silently.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.4 (2026-05-28): Third-party risk standard consolidation

Resolves the duplicate-authority finding identified by the comprehensive audit. Per the user's decision to merge, the two parallel third-party risk standards are consolidated into a single document in the risk domain.

### Merged

- [`risk/standard-third-party-and-supply-chain-risk.md`](risk/standard-third-party-and-supply-chain-risk.md) (v1.0.0 → v1.1.0): becomes the sole, master third-party-and-supply-chain risk standard for the library. Augmented with the supply-chain document's lifecycle content: an explicit AI service-provider contract-clause sub-section (dataset lineage, model validation per ISO/IEC 42001 §9, ethical sourcing, no-training-on-customer-data, deprecation notice, cross-border mechanism); supporting-tooling references in the monitoring section (TPRAQ, security-rating services, threat intelligence); a dedicated Offboarding and contract termination section; framework alignment expanded with ISO/IEC 27036-3, NIST SP 800-161r2, COBIT 2019 APO10, and CSA CCM v4.1 STA-02. A `supersedes` sentence references the deleted file.

### Deleted

- [`supply-chain/standard-third-party-risk.md`](supply-chain/standard-third-party-risk.md) (was v1.0.0): consolidated into the risk-domain master per the audit recommendation.

### Cross-references updated

21 files updated to point at the consolidated risk-domain standard. Affected directories: compliance/, dev-security/, governance/, operations/, security/, supply-chain/.

- Governance index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (v1.21.0 → v1.22.0): the supply-chain duplicate row removed; risk-domain row retained.
- Supply-chain README (v1.1.0 → v1.2.0): supply-chain TPR row removed from active documents.

### Result

A reader looking for the third-party risk standard now finds one canonical document, with consistent tier criteria, lifecycle, and ownership. The CRO is the named owner. The operational procedures in `supply-chain/` continue to implement the lifecycle steps.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.3 (2026-05-28): BASC migration to /sectors/ domain (organisation-neutrality)

Resolves the organisation-neutrality violation identified by the comprehensive audit. The library declared itself "organization-neutral" in [`README.md`](README.md) while three core policy documents explicitly scoped themselves to "BASC-certified logistics operations in Latin America (Colombia, Mexico, Peru, Chile)" and the compliance domain hosted a BASC-specific policy and two BASC registers as if universal content.

### Structural change

New top-level directory `/sectors/` created for optional, programme-conditional governance content. Organisations not participating in a covered sector programme can omit the corresponding annex entirely without affecting the main library.

- [`sectors/README.md`](sectors/README.md) (new, v1.0.0): domain register describing the sector-annex pattern, applicability rules, and relationship to the main library.
- [`compliance/logistics/annex-basc-programme-overview.md`](compliance/logistics/annex-basc-programme-overview.md) (new, v1.0.0): BASC sub-register describing applicability and listing active BASC documents.

### Files moved (git history preserved via `git mv`)

- [`compliance/policy-basc.md`](compliance/policy-basc.md) → [`compliance/logistics/policy-basc-information-security.md`](compliance/logistics/policy-basc-information-security.md) (v1.0.0 → v1.1.0; renamed to reflect canonical naming; Category updated from "Compliance Management" to "Sector Annex"; cross-references updated)
- [`compliance/register-basc-it-responsibilities.md`](compliance/register-basc-it-responsibilities.md) → [`compliance/logistics/register-basc-it-responsibilities.md`](compliance/logistics/register-basc-it-responsibilities.md) (v1.0.0 → v1.1.0; same updates)
- [`compliance/register-basc-it-compliance-kpis.md`](compliance/register-basc-it-compliance-kpis.md) → [`compliance/logistics/register-basc-it-compliance-kpis.md`](compliance/logistics/register-basc-it-compliance-kpis.md) (v1.0.0 → v1.1.0; same updates)

### BASC scoping stripped from main-domain documents

- [`security/policy-information-security.md`](security/policy-information-security.md): scope section, governance section, network section (4.1, 4.3, 4.4), data section (7.1, 7.2, 7.3), incident section (9.1, 9.2), framework alignment (line 145) — generalised; sector overlay pointer added. Inline NIST AI RMF 1.1 reference (missed by Phase 12.1 because of bare "AI RMF" form) corrected to NIST AI RMF 1.0.
- [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md): scope section generalised; sector overlay pointer added.
- [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md): scope section generalised; sector overlay pointer added.
- [`governance/standard-records-retention-and-destruction.md`](governance/standard-records-retention-and-destruction.md): BASC-specific Section 6 generalised into "sector-specific retention overlays" with pointer to `/sectors/` and the transportation-and-logistics sector annex in `/compliance/`.

### Cross-references updated

Cross-references to old BASC paths updated in: [`compliance/README.md`](compliance/README.md) (v1.1.0 → v1.2.0), [`compliance/annex-transportation-and-logistics-sector-requirements.md`](compliance/annex-transportation-and-logistics-sector-requirements.md), [`compliance/matrix-grc-compliance-alignment.md`](compliance/matrix-grc-compliance-alignment.md), [`compliance/register-ctpat-it-controls.md`](compliance/register-ctpat-it-controls.md), [`compliance/register-pip-compliance-controls.md`](compliance/register-pip-compliance-controls.md), [`compliance/template-trade-compliance-gap-assessment.md`](compliance/template-trade-compliance-gap-assessment.md), [`governance/matrix-reverse-framework-control-crosswalk.md`](governance/matrix-reverse-framework-control-crosswalk.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (v1.20.0 → v1.21.0; three BASC rows reclassified from Compliance to Sectors domain), [`supply-chain/README.md`](supply-chain/README.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](supply-chain/matrix-supply-chain-security-programme-alignment.md), [`supply-chain/register-ctpat-full-msc-controls.md`](supply-chain/register-ctpat-full-msc-controls.md).

### Tooling updates

`sectors` added to the DOMAINS / scan-path lists in [`tools/build-taxonomy.py`](tools/build-taxonomy.py), [`tools/lint-structure.py`](tools/lint-structure.py), [`tools/lint-metadata.py`](tools/lint-metadata.py), [`tools/lint-language.py`](tools/lint-language.py), [`tools/lint-links.py`](tools/lint-links.py), [`tools/lint-citations.py`](tools/lint-citations.py), [`tools/check-review-cadence.py`](tools/check-review-cadence.py). New denylist entry in [`tools/lint-citations.py`](tools/lint-citations.py) for bare "AI RMF 1.1" form to complement the existing "NIST AI RMF 1.1" entry.

### Top-level updates

- [`README.md`](README.md) (v1.5.1 → v1.5.2, patch per the standing rule): new `/sectors/` directory entry added to the repository structure; document-count statement updated to mention the optional sector-annex domain.
- [`specification-master-project.md`](specification-master-project.md) (v1.2.4 → v1.2.5): `/sectors/` added to the directory listing and the domain purpose summary.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.2 (2026-05-28): AI Governance Council operationalisation

Resolves the charter status whereby the AI Governance Council was declared "in formation" with full operationalisation targeted for Q3 2026 while 16+ AI documents referenced its approval as binding. The council is now an active governance body.

- [`ai/charter-ai-governance-council.md`](ai/charter-ai-governance-council.md) (v1.0.0 → v1.1.0): the "in formation" note removed. Composition table restated with eleven active seats: Chair (Chief Information Security Officer), Deputy Chair (Chief Information Officer), and members covering Chief Technology Officer, Chief Financial Officer, Chief Human Resources Officer, General Counsel, Chief Privacy Officer, Chief Risk Officer, AI Governance Lead (secretariat), Business Domain Representative (rotating), and Independent External Adviser (standing observer). The Chair confirms each meeting's roster; where a seat is unfilled the role's delegate or an acting appointee designated by the Chair exercises the responsibility. Quorum is the Chair (or Deputy Chair) plus four members.

The charter now reads as an active body; all downstream AI documents that reference AIGC approval as binding are unblocked. No other document changes were required; the existing dependency chain assumes the council can act, which is now true.

Taxonomy, portal, and maturity scorecard regenerated.

## Phase 12.1 (2026-05-28): Framework citation corrections

Corrects three repository-wide framework citation hallucinations identified by the comprehensive audit (Phase 11 follow-up).

- **COBIT 2025 → COBIT 2019**: 132 replacements across 78 files. ISACA's current published COBIT version is COBIT 2019; "COBIT 2025" does not exist. Process identifiers cited alongside (APO01, APO14, BAI09, MEA01, MEA02, APO06, APO07, etc.) are valid COBIT 2019 process IDs.
- **CSA CCM v5 → CSA CCM v4.1**: 115 replacements across 75 files. CSA's current Cloud Controls Matrix version is v4.1; "CCM v5" does not exist. Domain identifiers cited alongside (AIS, DSP, GOV, GRM, SEF, IVS, IAM, LOG, IPY, TIM, EKM, END, TVM, SR) are valid CCM v4 domain prefixes.
- **NIST AI RMF 1.1 → NIST AI RMF 1.0 (with AI 600-1 GenAI Profile)**: 1 replacement in [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md). NIST AI RMF was published as version 1.0; the Generative AI Profile is published as NIST AI 600-1.

New tool: [`tools/lint-citations.py`](tools/lint-citations.py) — stdlib-only Python linter that pins known-hallucinated framework strings on a denylist and reports any reintroduction. Exits non-zero on findings; suitable for CI integration. Denylist currently covers the three patterns above. [`CONTRIBUTING.md`](CONTRIBUTING.md) updated to list the linter in the local audit suite (now 8 audits).

Historical CHANGELOG entries are preserved verbatim; their descriptions reference the strings as they existed at the time, which the linter exempts.

Source verification: ISACA COBIT page, CSA CCM artifacts page, NIST CSRC.

## Phase 11 (2026-05-28): Continuous quality and review cadence (3 new documents + cadence checker)

Codifies the library maintenance practice with three new governance artefacts and a new audit tool. Closes the continuous-quality phase of the advisory review.

- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md): eight-step procedure covering schedule establishment, overdue detection, per-document review (currency, framework alignment, cross-reference, sanitisation, language, disposition, record), disposition application, derived-artefact maintenance, the standing audit suite (now seven audits), periodic library-level review (quarterly/semi-annual/annual cadences), and drift handling.
- [`governance/register-document-review-schedule.md`](governance/register-document-review-schedule.md): schedule schema with eleven fields, review-frequency normalisation table, six status values (Current, Due-soon, Overdue, Action-threshold, Blocked, Retired), maintenance rules, operating cadence, integration with tooling, and reporting outputs.
- [`governance/template-document-review-record.md`](governance/template-document-review-record.md): six-section per-document review record (identification, assessment of thirteen items, findings, disposition, actions, sign-off), style and length expectations, worked example.

New tool:

- [`tools/check-review-cadence.py`](tools/check-review-cadence.py): stdlib-only Python script that parses each active document's Date and Review Frequency metadata, computes next-review-due dates, and reports overdue and past-action-threshold entries with configurable warn-window and action-threshold parameters. Returns non-zero when documents are past the action threshold to gate CI.

Supporting changes:

- Governance README bumped 1.0.3 to 1.1.0 (minor: three substantive new rows).
- Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.19.0 to 1.20.0 (minor: three substantive new rows).
- Specification master bumped 1.2.3 to 1.2.4 (patch: architecture domain added to the repository structure listing).
- [`CONTRIBUTING.md`](CONTRIBUTING.md) updated to list the full seven-audit suite local contributors should run.
- Language linter exemption list extended to include the document review record template (which references the "ensure that" rule explicitly).
- Taxonomy, portal, and maturity scorecard regenerated.

Baseline: 266 active documents scanned by the cadence checker; all current except 1 due-soon (a monthly-cadence operations register) and 2 event-driven.

## Phase 10 (2026-05-28): Architecture domain (8 new documents)

Establishes the new `/architecture/` domain. Each new artefact starts at version 0.0.1 per the ingestion specification.

- [`architecture/README.md`](architecture/README.md): domain register with 8 active documents and 6 domain-coverage areas.
- [`architecture/framework-enterprise-architecture.md`](architecture/framework-enterprise-architecture.md): ten-section framework (principles, viewpoints, capability model, target-state and transition, governance forum, roles, deliverables, integration with adjacent programmes, fitness functions, operating expectations) aligned to TOGAF, ISO/IEC/IEEE 42010, IT4IT, C4, DDD, Team Topologies, Wardley mapping, and Accelerate research.
- [`architecture/standard-architecture-decision-records.md`](architecture/standard-architecture-decision-records.md): ten-section ADR standard (principles, when to write, template, status lifecycle, review and approval, storage, integration with adjacent processes, AI-aware practice, quality expectations, anti-patterns).
- [`architecture/standard-reference-architecture.md`](architecture/standard-reference-architecture.md): ten-section reference-architecture practice (principles, classes, structure, maturity scale, authoring, consumption, deviation handling, maintenance, governance integration, quality expectations).
- [`architecture/standard-technology-radar.md`](architecture/standard-technology-radar.md): ten-section radar standard (principles, four rings, quadrants, blip structure, lifecycle, governance, criteria, relationship to other artefacts, AI radar handling, exceptions).
- [`architecture/procedure-architecture-review.md`](architecture/procedure-architecture-review.md): eight-step architecture review procedure with reviewer assignment, dispositions, decision recording, implementation oversight, closure and learning, plus appeal process.
- [`architecture/standard-api-design.md`](architecture/standard-api-design.md): fourteen-section API design standard (principles, style choice, REST conventions, contract and schema, identifiers, errors, versioning, time and units, documentation, pagination, idempotency, AI-callable APIs, customer-facing APIs, governance).
- [`architecture/standard-data-architecture.md`](architecture/standard-data-architecture.md): fourteen-section data architecture standard (principles, domains and ownership, classification, schemas and contracts, integration, quality, lineage, lifecycle, analytical and AI platforms, sharing, master and reference data, governance forum, relationship to adjacent artefacts, anti-patterns).
- [`architecture/standard-integration-architecture.md`](architecture/standard-integration-architecture.md): fourteen-section integration standard (principles, pattern selection, classes, contracts, event-driven, synchronous, batch, webhooks, AI provider integration, observability, reliability patterns, security overlay, governance, anti-patterns).

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.18.0 to 1.19.0 (minor: eight substantive new rows). Top-level README bumped 1.5.0 to 1.5.1 (patch: domain listing and document-count update). Tooling ([`tools/build-taxonomy.py`](tools/build-taxonomy.py), [`tools/lint-structure.py`](tools/lint-structure.py), [`tools/lint-metadata.py`](tools/lint-metadata.py), [`tools/lint-language.py`](tools/lint-language.py), [`tools/lint-links.py`](tools/lint-links.py)) updated to include the new domain in their scan lists. Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.9 (2026-05-28): Risk and governance (4 new documents)

Closes four risk and governance content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- [`risk/template-operational-risk-register.md`](risk/template-operational-risk-register.md): ten-section operational risk register template (identification, scope and assumptions, risk entries, risk taxonomy, assessment scales, control linkage, scenario and emerging-risk linkage, loss events and near-misses, aggregation and reporting, integration), with a Basel-aligned taxonomy of thirteen categories and a worked example.
- [`risk/register-scenario-risk-catalogue.md`](risk/register-scenario-risk-catalogue.md): scenario catalogue covering eleven classes (cyber attack, AI-specific, technology failure, supplier failure, people and conduct, external event, financial market, regulatory, reputational, climate-related, concurrent) with a reference set of fifty scenarios; severity calibration (moderate, severe-but-plausible, extreme); seven uses of the catalogue.
- [`risk/template-board-risk-report.md`](risk/template-board-risk-report.md): fourteen-section board-facing risk report template (cover, executive summary, risk appetite and tolerance, top enterprise risks, emerging risks, incidents and near-misses, regulatory and external environment, supplier and concentration, AI and emerging-technology risk, resilience and continuity, assurance, risk culture, board decisions requested, appendices) with style guidance, cadence, and preparation process.
- [`risk/register-assurance-map.md`](risk/register-assurance-map.md): assurance map applying the three-lines model across twelve domains with a six-level assurance rating scale (green, amber-1, amber-2, red, not applicable, out of cycle), fourteen-activity taxonomy, governance forum, integration with the assurance plan, gap-management process, and a worked example.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.17.0 to 1.18.0 (minor: four substantive new rows). Risk README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.8 (2026-05-28): Operations (5 new documents)

Closes five operations content gaps identified in the advisory review.

- [`operations/standard-observability-and-telemetry.md`](operations/standard-observability-and-telemetry.md): fourteen sections covering principles, service-level signals, metrics, logs, distributed tracing, error and exception telemetry, events, synthetic and real-user monitoring, dashboards and alerting, privacy and data classification, cost governance, AI and ML telemetry, tooling and platform, testing.
- [`operations/standard-site-reliability-engineering.md`](operations/standard-site-reliability-engineering.md): twelve sections covering principles, SLOs and SLIs, error budget policy, reliability practices, change-related risk, incident management, on-call, toil management, runbooks, AI service reliability, tooling and platform, governance.
- [`operations/standard-capacity-and-performance-management.md`](operations/standard-capacity-and-performance-management.md): twelve sections covering principles, capacity classes (eight), demand forecasting, capacity planning, performance objectives and measurement, performance testing, scaling, capacity for resilience, third-party and vendor capacity, cost governance, governance forum, AI inference capacity.
- [`operations/procedure-release-management.md`](operations/procedure-release-management.md): nine-step procedure (planning, build and packaging, pre-production validation, authorisation, deployment, verification, stabilisation, rollback or forward-fix, closure and learning), release classes (routine, expedited, emergency, standard repeatable), seven role definitions, coordination with seven adjacent procedures, six deployment strategies.
- [`operations/standard-it-financial-management.md`](operations/standard-it-financial-management.md): twelve sections covering principles, cost taxonomy, attribution, budgeting, monitoring and forecasting, optimisation, vendor commitment management, AI cost governance, sustainability considerations, governance, integration with related programmes, financial reporting and compliance.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.16.0 to 1.17.0 (minor: five substantive new rows). Operations README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.7 (2026-05-28): DevSecOps (7 new documents)

Closes seven developer-security content gaps identified in the advisory review.

- [`dev-security/standard-api-security.md`](dev-security/standard-api-security.md): twelve sections covering lifecycle gates, authentication, authorisation, input validation, transport, rate limiting and abuse prevention, observability and logging, gateway management, third-party API consumption, AI-exposed APIs, GraphQL-specific controls, event-driven and webhook security.
- [`dev-security/standard-container-and-image-security.md`](dev-security/standard-container-and-image-security.md): ten sections covering image build, registry management, runtime security, orchestrator hardening, developer workflow, serverless containers, supply-chain integrity (SBOM, signing, attestation), vulnerability management, data handling, incident readiness.
- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): twelve sections aligned to OWASP MASVS v2 (L1, L2, R) with four-tier sensitivity mapping; covers storage, cryptography, authentication, network, platform interaction, code quality and resilience, third-party SDKs, store and distribution, privacy (including children's data), testing, incident readiness.
- [`dev-security/procedure-secure-code-review.md`](dev-security/procedure-secure-code-review.md): seven-step procedure (pre-review preparation, reviewer assignment, reviewer evaluation, reviewer dispositions, author response, merge gate, post-merge actions), ten evaluation categories (secrets, input handling, authentication and authorisation, cryptography, data, errors and logging, dependencies, IaC and platform, AI components, change hygiene), AI-assisted and AI-generated code considerations.
- [`dev-security/standard-cloud-hardening-baseline-aws.md`](dev-security/standard-cloud-hardening-baseline-aws.md): thirteen sections covering account structure and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, tagging and inventory, provisioning and change, incident readiness; aligned to CIS AWS Foundations Benchmark and AWS Well-Architected Security Pillar.
- [`dev-security/standard-cloud-hardening-baseline-azure.md`](dev-security/standard-cloud-hardening-baseline-azure.md): thirteen sections covering tenant, subscription, and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, tagging and inventory, provisioning and change, incident readiness; aligned to CIS Microsoft Azure Foundations Benchmark and the Microsoft Cloud Security Benchmark.
- [`dev-security/standard-cloud-hardening-baseline-gcp.md`](dev-security/standard-cloud-hardening-baseline-gcp.md): thirteen sections covering organisation, folder, and identity, detective controls and logging, preventive controls, network, data protection, compute, storage, secrets and credentials, monitoring and detection, supplementary services, labelling and inventory, provisioning and change, incident readiness; aligned to CIS Google Cloud Platform Foundations Benchmark and the Google Cloud Architecture Framework security pillar.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.15.0 to 1.16.0 (minor: seven substantive new rows). Dev-security README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion; removed completed items from the planned expansion list). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.6 (2026-05-28): Security (7 new documents)

Closes seven security content gaps identified in the advisory review.

- [`security/framework-zero-trust-architecture.md`](security/framework-zero-trust-architecture.md): seven principles, seven pillars (identity, devices, networks, applications and workloads, data, visibility and analytics, automation and orchestration), policy-engine input model, four-stage maturity ladder.
- [`security/standard-email-security.md`](security/standard-email-security.md): eight sections covering outbound authentication (SPF/DKIM/DMARC/BIMI/MTA-STS), inbound controls, anti-phishing and BEC, outbound controls, user-facing controls, secure-email-gateway requirements, AI-generated and AI-processed considerations, incident response.
- [`security/standard-soc-operating-model.md`](security/standard-soc-operating-model.md): four capability tiers, staffing model (nine roles), tool stack (fourteen tool categories), coverage hours, detection engineering practices, threat hunting, intelligence integration, on-call governance, metrics, supplier-managed-SOC requirements, continuous improvement.
- [`security/standard-saas-security-posture-management.md`](security/standard-saas-security-posture-management.md): ten sections covering inventory, configuration baselines, continuous posture monitoring, SaaS-to-SaaS integration risk, third-party application access, shadow-SaaS detection, SaaS-to-SaaS supplier risk, data protection within SaaS, incident readiness, lifecycle.
- [`security/framework-insider-risk-programme.md`](security/framework-insider-risk-programme.md): five insider risk categories, governance model with Insider Risk Steering Committee, four pillars (prevention, detection, response, learning), eleven privacy and due-process safeguards, deliberate out-of-scope exclusions, coordination with eight adjacent programmes, metrics.
- [`security/standard-endpoint-hardening.md`](security/standard-endpoint-hardening.md): twelve sections covering identity and authentication, device integrity, software and configuration, EDR, data protection, network and connectivity, privileged access workstations, developer workstations, BYOD and unmanaged devices, mobile devices, kiosks and shared devices, lifecycle.
- [`security/procedure-key-escrow-and-recovery.md`](security/procedure-key-escrow-and-recovery.md): three key categories (productivity-data, operational service, root and signing), escrow architectures per category, recovery triggers, dual-control matrix, Category 3 ten-step ceremony, authorisation flow, post-recovery actions, lost or compromised key handling, post-quantum considerations.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.14.0 to 1.15.0 (minor: seven substantive new rows). Security README bumped 1.1.1 to 1.2.0 (minor: substantive section expansion).

## Phase 9.5 (2026-05-28): AI (10 new documents)

Closes ten AI content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- [`ai/plan-ai-incident-response.md`](ai/plan-ai-incident-response.md): AI-specific incident classes and triggers, P1 to P4 severity criteria, seven-phase lifecycle with AI-specific actions at each phase, coordination with security and privacy streams, evidence requirements.
- [`ai/template-dataset-datasheet.md`](ai/template-dataset-datasheet.md): ten-section datasheets-for-datasets template covering motivation, composition, collection process, preprocessing and labelling, uses, distribution, maintenance, ethical considerations, provenance and lineage, signatures.
- [`ai/register-model-registry.md`](ai/register-model-registry.md): comprehensive model inventory with 30-field schema, six lifecycle states (Research, Evaluation, Staging, Production, Deprecated, Retired), backward and forward lineage tracking, integration with eleven adjacent governance artefacts.
- [`ai/procedure-foundation-model-lifecycle.md`](ai/procedure-foundation-model-lifecycle.md): seven-step lifecycle for foundation-model consumption (identify, pre-engagement evaluation, contractual integration, deployment, ongoing monitoring, version transition, exit), seven AI-specific contract clauses, seven risk vectors with mitigations.
- [`ai/template-ai-vendor-security-questionnaire.md`](ai/template-ai-vendor-security-questionnaire.md): nine-section AI-specific extension to the general supplier questionnaire covering provider profile, training-data provenance, customer data handling, model security, tool and agent capabilities, evaluation and assurance, compliance and transparency, incident response, continuity and exit.
- [`ai/standard-ai-access-and-agent-permissions.md`](ai/standard-ai-access-and-agent-permissions.md): eight sections covering principles (six), human access to AI capabilities, service-to-AI access, AI-to-tool access for agentic systems (with tool allow-list, capability scopes, identity propagation, three confirmation modes, rate and chain-length limits, logging), AI-to-data access, AI-to-AI access, access review cadence, incident-time controls.
- [`ai/register-mcp-server.md`](ai/register-mcp-server.md): MCP server inventory with 25-field schema, four-tier approval categories, server-security baseline (eleven control areas), coordination with seven adjacent governance artefacts.
- [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md): ten-step procedure covering source identification, sensitive-content removal, consent and subject-rights mechanism, approval to train, lineage tracking, deletion propagation with SLAs, supplier-provided training data, synthetic data, retrieval index content, periodic review.
- [`ai/standard-ai-inference-cost-governance.md`](ai/standard-ai-inference-cost-governance.md): ten sections covering principles, budgeting and allocation, cost ceilings and rate limits, model-choice criteria, monitoring and anomaly response (dual-routed financial and security), feature lifecycle controls, agent and autonomous workflow controls, customer-facing transparency, provider-side cost-management, reporting.
- [`ai/template-ai-red-team-report.md`](ai/template-ai-red-team-report.md): nine-section red team engagement report covering engagement profile, methodology, structured findings (with twelve-field-per-finding schema), coverage assessment against OWASP LLM Top 10 and MITRE ATLAS, positive observations, recommendations, validation and retest, distribution, signatures.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.13.0 to 1.14.0 (minor: ten substantive new rows). AI README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion).

## Phase 9.4 (2026-05-28): supply chain (5 new documents)

Closes five supply-chain content gaps identified in the advisory review.

- [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](supply-chain/procedure-fourth-party-and-nth-party-risk.md): tiered visibility expectations (T1 fourth-party plus selected nth-party; T2 material fourth-party; T3 sub-processor only); six-step procedure (identify, assess, monitor, escalate, treat, record).
- [`supply-chain/register-concentration-risk.md`](supply-chain/register-concentration-risk.md): six concentration dimensions (service-class, shared sub-tier, geographical, jurisdiction, vendor-family, intra-group); register schema with treatment options; coordination with the critical-ICT-third-party regime.
- [`supply-chain/register-sbom.md`](supply-chain/register-sbom.md): three SBOM acquisition paths (build-time, supplier-provided, post-deployment); register schema with CycloneDX / SPDX / VEX support; linkage to vulnerability management and acceptance gates; customer transparency under EU CRA and EO 14028.
- [`supply-chain/template-supplier-offboarding-evidence.md`](supply-chain/template-supplier-offboarding-evidence.md): eight-section offboarding record covering relationship identification, access revocation (ten access types), data return and destruction (eight categories), service-continuity handover, residual obligations (ten obligation types), contract closure, post-exit review, approval set.
- [`supply-chain/standard-supplier-resilience-monitoring.md`](supply-chain/standard-supplier-resilience-monitoring.md): five signal categories (continuity testing, incident, financial-health, control and assurance, external-environment); tier-based monitoring posture; signal source diversity; coordination with the concentration register and the critical-ICT-third-party regime.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.12.0 to 1.13.0 (minor: five substantive new rows). Supply-chain README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion).

## Phase 9.3 (2026-05-28): resilience templates and plans

Closes five resilience content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- [`resilience/template-tabletop-exercise.md`](resilience/template-tabletop-exercise.md): scenario design, scenario library (eight classes from ransomware to crisis convergence), objectives, participants, format options, inject schedule template, six-criterion evaluation rubric, after-action report structure.
- [`resilience/template-recovery-runbook.md`](resilience/template-recovery-runbook.md): per-system runbook with ten sections (system identification, dependencies, detection and declaration, pre-recovery checks, recovery steps, validation, communications, rollback, closure and learning, test history).
- [`resilience/template-lessons-learned.md`](resilience/template-lessons-learned.md): cross-stream lessons-learned report with eleven sections (event identification, executive summary, timeline reconstruction, root cause and contributing factors, what worked, gaps identified across twelve categories, corrective actions, procedure and control changes, communication of lessons, metric impact, approval).
- [`resilience/plan-pandemic-continuity.md`](resilience/plan-pandemic-continuity.md): five-stage activation model (Monitor, Prepare, Activate, Sustained operations, Recovery), workforce health, remote-work scaling, essential-service prioritisation, supplier and supply-chain impact, facility and operational adjustments, communications, deactivation and recovery.
- [`resilience/plan-physical-site-continuity.md`](resilience/plan-physical-site-continuity.md): four-posture model (Protective actions, Partial operations on site, Site closed, Restoration), activation criteria, protective actions (deferring to the emergency response guideline), alternate-site activation (ten-step procedure), restoration and return, workforce well-being.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.11.0 to 1.12.0 (minor: five substantive new rows). Resilience README bumped 1.1.1 to 1.2.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 9.2 (2026-05-28): compliance sector and regime expansion

Closes seven sector and regime content gaps identified in the advisory review. Each new annex starts at version 0.0.1 per the ingestion specification.

- [`compliance/public-sector/annex-fedramp-requirements.md`](compliance/public-sector/annex-fedramp-requirements.md): applicability triggers, authorisation route selection (JAB, Agency, FedRAMP Tailored, FedRAMP Ready), baseline selection mapped to FIPS 199, library coverage per NIST SP 800-53 Rev 5 control family, eight named library gaps requiring additional documentation (SSP, ConMon, POA&M, SAR/SAP, OMB M-22-09 reporting, FIPS-validated cryptography, federal personnel investigations, CUI handling).
- [`compliance/financial-services/annex-dora-implementation.md`](compliance/financial-services/annex-dora-implementation.md): per-pillar mapping for ICT risk management (Articles 5 to 16), ICT-related incident reporting (Articles 17 to 23 with 4-hour, 72-hour, one-month windows), digital operational resilience testing including TLPT under TIBER-EU, ICT third-party risk including Article 30 minimum clauses and the critical-ICT-third-party Oversight Framework, information and intelligence sharing.
- [`compliance/annex-nis-2-implementation.md`](compliance/annex-nis-2-implementation.md): entity classification (Essential and Important under Annexes I and II), per-sub-measure mapping of Article 21 risk-management measures, Article 20 management body responsibilities and training, the four-stage incident reporting regime under Articles 23 to 25 (early warning, incident notification, intermediate, final), six library gaps requiring additional documentation.
- [`compliance/public-sector/annex-public-sector-requirements.md`](compliance/public-sector/annex-public-sector-requirements.md): eight overlay areas (freedom of information, accessibility under WCAG 2.2 AA and EN 301 549, public procurement, records management, audit and external scrutiny, ethics and lobbying, AI in the public sector, official languages), library coverage per overlay, seven library gaps.
- [`compliance/telecommunications/annex-telecommunications-sector-requirements.md`](compliance/telecommunications/annex-telecommunications-sector-requirements.md): seven overlay areas (sector cybersecurity, lawful interception, data retention, sector customer privacy, emergency calling and resilience, vendor and supply-chain restrictions, numbering and addressing resources), regime references for EU EECC, EU NIS 2, UK Telecommunications (Security) Act 2021, US CALEA, FCC, and equivalents.
- [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md): six overlay areas (critical-infrastructure cybersecurity baselines, OT and ICS cybersecurity, physical-cyber convergence, sector incident reporting, supplier and component security, resilience and continuity), per-control area mapping for OT including network segmentation, OT vulnerability management, vendor remote access to OT, OT incident response.
- [`compliance/financial-services/annex-sox-itgc.md`](compliance/financial-services/annex-sox-itgc.md): ICFR scope determination, four ITGC domains (access to programs and data, program changes, program development, computer operations) with library coverage per control objective, auditor-expected artefacts beyond the library, coordination with adjacent regimes (SOC 1, PCI DSS, GDPR, NIST CSF, ISO 27001).

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.10.0 to 1.11.0 (minor: seven substantive new rows). Compliance README bumped 1.0.1 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Drift fixes (2026-05-28): repository structure documentation and AI ingestion instruction refresh

A post-Phase-9.1 drift audit identified six stale items in the meta files that had fallen out of sync with the repository state during Phases 1, 6, 7, and 9.1. Fixed in this commit:

- [`README.md`](README.md): Repository structure block now lists the infrastructure directories (`tools/`, `docs/`, `.github/`, [`taxonomy.yml`](taxonomy.yml), hygiene files). Document count claim refreshed from approximately 200 to approximately 215. Core reference set table expanded with three privacy templates (ROPA, privacy notice, DSAR workflow) added in Phase 9.1. Version 1.4.2 to 1.5.0 (minor).
- [`specification-master-project.md`](specification-master-project.md): Section 4 expanded to distinguish governance-artefact directories from repository infrastructure directories. Version 1.2.2 to 1.2.3 (patch).
- [`specification-ingestion.md`](specification-ingestion.md): Repository domains section gained a note enumerating the infrastructure paths that are out of scope for ingestion and exempt from the structural audit. Version 1.4.1 to 1.4.2 (patch).
- [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md): refreshed end to end. Now references the current 16-type vocabulary, the type-selection guidance, the audit scripts, the taxonomy and portal generators, the CHANGELOG update obligation, and the rules for retiring or superseding documents.
- [`tools/lint-language.py`](tools/lint-language.py): added the AI ingestion instruction file to the exempt list for the self-referential `ensure` rule, consistent with the existing exemptions for both specifications.

The convention going forward is to update CHANGELOG.md in the same commit as the substantive phase change.

## Phase 9.1 (2026-05-28): privacy templates, registers, framework, and standard

Closes eight long-standing privacy content gaps identified in the advisory review. Each new artefact starts at version 0.0.1 per the ingestion specification.

- [`privacy/template-record-of-processing-activities.md`](privacy/template-record-of-processing-activities.md): GDPR Article 30 ROPA template with controller and processor views.
- [`privacy/template-privacy-notice.md`](privacy/template-privacy-notice.md): twelve required content blocks satisfying GDPR Articles 13 and 14, UK GDPR, LGPD, CPPA, PIPL, CCPA, and equivalents; just-in-time variant included.
- [`privacy/template-dsar-workflow.md`](privacy/template-dsar-workflow.md): seven-stage DSAR lifecycle with identity verification trust levels, twenty-one-field request record schema, and six operational metrics.
- [`privacy/framework-consent-management.md`](privacy/framework-consent-management.md): consent capture, validity standard, granularity rules, withdrawal, refresh and expiry conditions, ePrivacy and cookie consent alignment.
- [`privacy/register-automated-decision-making.md`](privacy/register-automated-decision-making.md): ADM and profiling register schema, registration triggers, coordination with the AI System Register.
- [`privacy/register-cookie-and-tracker.md`](privacy/register-cookie-and-tracker.md): seven-category tracker taxonomy, eighteen-field schema, quarterly-scan operating expectation, dark-pattern prohibitions.
- [`privacy/standard-pseudonymisation-and-anonymisation.md`](privacy/standard-pseudonymisation-and-anonymisation.md): permitted techniques including k-anonymity (k at minimum 5), l-diversity, t-closeness, differential privacy, synthetic data; five-tier residual-risk classification.
- [`privacy/framework-childrens-data.md`](privacy/framework-childrens-data.md): per-jurisdiction age thresholds, age-assurance approaches, parental consent verification, ten design defaults, profiling and ADM restrictions.

Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.9.0 to 1.10.0 (minor: eight substantive new rows). Privacy README bumped 1.0.0 to 1.1.0 (minor: substantive section expansion). Taxonomy, portal, and maturity scorecard regenerated.

## Phase 8 (2026-05-28): operational usefulness uplift

- [`resilience/procedure-cross-domain-incident-coordination.md`](resilience/procedure-cross-domain-incident-coordination.md) expanded from 92 to 264 lines: domain ownership decision rule, joint command structure, coordination lifecycle, five hand-off checklists, severity rules across streams, joint decision log, cross-stream evidence handling, communication boundaries, joint post-incident review, joint exercises, metrics. Version 1.0.1 to 1.1.0 (minor).
- Tool acceptance criteria sections added with six-column purpose/output/integration/success/escalation tables:
  - [`dev-security/standard-software-composition-analysis.md`](dev-security/standard-software-composition-analysis.md) §8 (ten criteria). Version 1.0.0 to 1.1.0 (minor).
  - [`ai/guide-ai-adversarial-test-reference.md`](ai/guide-ai-adversarial-test-reference.md) Red team methodology subsection (PyRIT, Garak, promptfoo, manual practitioner). Version 1.2.2 to 1.3.0 (minor).
  - [`ai/guide-ai-security-technical-implementation.md`](ai/guide-ai-security-technical-implementation.md) §A7 (SAST, prompt regression, LLM scanner, AI red team automation, cloud guardrails, AI-aware monitoring). Version 1.2.1 to 1.3.0 (minor).
- Targeted measurable-verb pass on three Standards in `operations/`, `security/`, `dev-security/`. Defensible conditional usage left intact.
- [`tools/build-portal.py`](tools/build-portal.py): generates [`docs/portal.md`](docs/portal.md) (audience-keyed navigation) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) (per-document maturity classification) from [`taxonomy.yml`](taxonomy.yml). Wired into CI and pre-commit.
- Phase 8.5 (per-document adoption notes) deliberately deferred; [`docs/worked-example.md`](docs/worked-example.md) already covers end-to-end adaptation.

## Phase 7 (2026-05-28): machine-readable taxonomy and reverse framework crosswalk

- [`tools/build-taxonomy.py`](tools/build-taxonomy.py): generates [`taxonomy.yml`](taxonomy.yml) from canonical metadata of every active artefact (3,690+ lines). `--check` mode wired into CI and pre-commit.
- [`governance/matrix-reverse-framework-control-crosswalk.md`](governance/matrix-reverse-framework-control-crosswalk.md) (v0.0.1): inverts the forward matrix to answer "given an external control identifier, which library documents address it". Coverage: ISO 27001:2022 Annex A, ISO 42001:2023, NIST CSF 2.0, NIST SP 800-53 Rev 5, NIST AI RMF, CSA CCM v5, EU AI Act, GDPR / UK GDPR, DORA, NIS 2, OWASP LLM Top 10, MITRE ATLAS, CTPAT MSC, BASC v6, WCO SAFE.
- [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) updated to cross-reference the reverse matrix; pair-consistent.
- Document index [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) bumped 1.8.6 to 1.9.0 (minor: substantive new index row for the reverse crosswalk).

## Phase 6 (2026-05-28): automation, validation, repository hygiene

- Three new audit scripts added: [`tools/lint-metadata.py`](tools/lint-metadata.py) (13-field canonical metadata block, allowed types, semver, ISO 8601 dates, role-based ownership, License field, repository-path consistency, filename prefix), [`tools/lint-links.py`](tools/lint-links.py) (every relative markdown link resolves), [`tools/lint-structure.py`](tools/lint-structure.py) (every active file appears in its domain README and in the document index, and every reference resolves). These complement [`tools/lint-language.py`](tools/lint-language.py) from Phase 5.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): GitHub Actions workflow running all four audits on push to `main` and on every pull request.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): local hooks wiring the same audits.
- Repository hygiene files: [`CONTRIBUTING.md`](CONTRIBUTING.md) (contribution workflow, metadata rules, style rules, filename rules), [`SECURITY.md`](SECURITY.md) (how to report content accuracy defects, CC0 licence concerns, organisation or personal data leakage, broken external links, and tooling defects), [`CHANGELOG.md`](CHANGELOG.md) (this file), [`docs/adopter-guide.md`](docs/adopter-guide.md) (fork and adapt walkthrough), [`docs/worked-example.md`](docs/worked-example.md) (end-to-end draft-to-CC0-artefact walkthrough).
- Conformance bugs surfaced by the new auditors fixed: three compliance files with plain-text Repository Path links converted to canonical markdown links, one risk template misclassified as Register corrected to Template, master specification gained the four missing canonical metadata fields, twenty-five privacy jurisdiction annexes had a broken self-folder reference repaired, two domain READMEs and one index row reconciled. All version increments patch.

## Phase 5 (2026-05-28): heading style normalisation, language audit, lint tooling

Normalises section heading case across the corpus (24 lettered subsections in [`ai/guide-ai-security-technical-implementation.md`](ai/guide-ai-security-technical-implementation.md), 5 in [`ai/guide-ai-adversarial-test-reference.md`](ai/guide-ai-adversarial-test-reference.md), and the `Step N:` and `Category N:` patterns in 17 procedure / guideline / plan / register files). Codifies the sentence-case rule and other language conventions in both specifications. Introduces [`tools/lint-language.py`](tools/lint-language.py).

## Phase 4 (2026-05-28): near-duplicate reconciliation

Retires the older, weaker governance-domain policy in favour of the newer risk-domain policy as the canonical enterprise governance and risk management policy. Migrates the control-area mapping table into [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md). Retires the governance-domain supplier security and privacy assurance procedure; migrates its metrics block into the supply-chain Standard. 37 inbound references redirected; 2 files deleted; 40+ files modified.

## Phase 3 (2026-05-28): duplicate filename resolution

Three duplicate-filename pairs resolved. Renames preserve git history.

- [`security/procedure-incident-response.md`](security/procedure-incident-response.md) and [`resilience/procedure-incident-response.md`](resilience/procedure-incident-response.md) renamed to [`security/procedure-security-incident-response.md`](security/procedure-security-incident-response.md) and [`resilience/procedure-cross-domain-incident-coordination.md`](resilience/procedure-cross-domain-incident-coordination.md). The resilience procedure refocused as the cross-domain coordination layer that delegates technical IR to the security procedure.
- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) and [`resilience/procedure-data-protection-and-privacy-breach-response.md`](resilience/procedure-data-protection-and-privacy-breach-response.md) consolidated: AI-specific assessment block migrated into a new section 4.3 of the privacy procedure; resilience-domain duplicate deleted.
- [`compliance/register-ctpat-compliance-controls.md`](compliance/register-ctpat-compliance-controls.md) and [`supply-chain/register-ctpat-compliance-controls.md`](supply-chain/register-ctpat-compliance-controls.md) renamed to [`compliance/register-ctpat-it-controls.md`](compliance/register-ctpat-it-controls.md) and [`supply-chain/register-ctpat-full-msc-controls.md`](supply-chain/register-ctpat-full-msc-controls.md) to make their distinct scopes explicit.

## Phase 2 (2026-05-28): filename, type, and cross-reference reconciliation

Brings every file into compliance with the now-expanded specification. Two files renamed via `git mv` to add correct type prefixes (`plan-` and `template-`). Seven files reclassified to their canonical Document Type. Three references to the superseded [`privacy/annex-regional-privacy-requirements.md`](privacy/annex-regional-privacy-requirements.md) redirected to [`privacy/annex-privacy-jurisdiction-index.md`](privacy/annex-privacy-jurisdiction-index.md). Microsoft PyRIT references rewritten under open-source framing. 12 inbound references updated.

## Phase 1 (2026-05-28): document-type expansion

Adds Standard Operating Procedure (SOP), Roadmap, and Guide to the controlled vocabulary of allowed document types. Removes the prior prohibition on SOP. Adds type-selection guidance distinguishing Procedure from SOP, Plan from Roadmap, and Guideline from Guide. Repairs the document hierarchy tables in the governance charter and the document architecture framework which were previously missing Specification, Annex, and Checklist.

## Earlier history (before 2026-05-28)

Repository established as a public-domain CC0 GRC documentation library. Initial corpus included approximately 200 documents across ten domains: AI governance, compliance, developer security, governance, operations, privacy (with a 26-jurisdiction subfolder), resilience, risk, security, and supply chain. The earlier history is preserved in the git log; this changelog adopts phase-level granularity starting from 2026-05-28.
