# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

## 2026-06-01, Library Version 2026.05.141

Phase 3 of the dev-security pack scope expansion: second governance rule lands.

### Added

- [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) — new pack rule codifying "every change to user-visible content carries a CHANGELOG entry by default." The rule specifies what an entry must contain (date and version header, structured sections following Keep a Changelog, linked file references, the "why" not only the "what", verification evidence, phase context for multi-PR rollouts), the sanctioned opt-out path (a `Changelog: skip (reason: ...)` trailer in the commit or PR description, reviewer-approved), prohibited anti-patterns (silent changes, vague entries, batched-up entries, retroactive entries, entries with unlinked file references, misclassified breaking changes, verbatim commit-message copy, gate bypass via `--no-verify`), the three mechanical CI gates that enforce the discipline (delta gate, link-coverage gate, version-monotonicity gate), tool-specific guidance (git trailers, monorepo coordination, generated CHANGELOGs, document corpora), an exception-handling protocol consistent with the gate-discipline rule, and framework alignment (NIST SSDF PO.5/PS.1/RV.1/RV.2, CSA CCM CCC-01-04/LOG-02/LOG-08, ISO 27001 A.5.4/A.8.15/A.8.27/A.8.32). Generalises this project's D1 CHANGELOG-on-PR delta gate, the CHANGELOG link-coverage audit, and the version-monotonicity audit into a portable, pack-distributable discipline applicable to any project with a CHANGELOG.
- [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.8.0. "Pack scope" section updated to list both shipped governance rules with their pack-version timing. Directory-structure ASCII tree shows the change-tracking rule populated alongside gate-discipline. "Rule files and their scope" table gains a new row for the change-tracking rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a second bullet for the change-tracking rule with a one-line summary of its contract. Downstream adopters who drag the payload now inherit both governance rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/change-tracking.md bullet; pack-version paragraph updated from 1.7.0 to 1.8.0 and notes the second governance rule.
- [`README.md`](README.md): library version bumped 2026.05.140 to 2026.05.141; README version bumped 1.7.133 to 1.7.134.

### Phased rollout context

This is Phase 3 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract; Phase 2 (Library 2026.05.140) shipped gate-discipline. Phases 4 through 6 will add: evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives under `dev-security/claude-rules/governance/` and is scanned by [`tools/lint-language.py`](tools/lint-language.py); ran the linter standalone on the file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The project consumption copy lives in the exempt `.claude/` subtree. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.140

Phase 2 of the dev-security pack scope expansion: first governance rule lands.

### Added

- [`dev-security/claude-rules/governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md) — new pack rule codifying "never weaken or delete a gate to silence a failure; fix the artefact." The rule enumerates prohibited responses to a failing gate (`--no-verify`, severity-threshold lowering, exemption-list dumping, blanket suppressions, assertion-to-logging downgrades, marking real gates non-required, exit-code swallowing, flake-normalisation), correct responses in order of preference (fix the artefact; fix the gate if it is wrong; documented temporary exception; environmental re-run), tool-specific anti-patterns (git, lint, type-check, tests, CI/CD config, generator-output drift), an exception-handling protocol that the rule is consistent with, and framework alignment (OWASP ASVS, NIST SSDF, CSA CCM, ISO 27001). Generalises the project's `## Boundaries` rule ("Never weaken or delete an audit gate to make a document pass; fix the document") into a portable, pack-distributable form applicable to any project with CI gates, audit programmes, or branch protections.
- [`.claude/rules/governance/gate-discipline.md`](.claude/rules/governance/gate-discipline.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.7.0. "Pack scope" section updated from "will live under" to "lives under" the `governance/` subdirectory; explicit reference to the first landed rule. Directory-structure ASCII tree now shows the gate-discipline rule populated. "Rule files and their scope" table gains a new row for the gate-discipline rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) gains a new "## Development-governance discipline" section before "## Framework basis" referencing the new rule. Downstream adopters who drag the pack drop-in payload into their project now inherit the gate-discipline rule alongside the existing security rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list gains the new governance/gate-discipline.md bullet; preamble paragraph updated from "pack version 1.6.0 announces" to "pack version 1.7.0 covers ... 1.7.0 delivered the first governance rule." Subsequent governance rules to be listed as they land.
- [`README.md`](README.md): library version bumped 2026.05.139 to 2026.05.140; README version bumped 1.7.132 to 1.7.133.

### Phased rollout context

This is Phase 2 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract. Phases 3 through 6 will add: change-tracking discipline, evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives in the exempt `dev-security/claude-rules/` subtree and is not subject to corpus linters; the project consumption copy lives in the exempt `.claude/` subtree and is likewise not subject to corpus linters. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.139

Phase 1 of the dev-security pack scope expansion: announce broadened contract from security-only to security + development-governance discipline.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.6.0 (2026-06-01). The opening "What are these files?" section now describes the pack as carrying "security and development-governance context" rather than security context alone. A new "Pack scope" section near the top of the README articulates the two scope families (security/compliance under `core/`, `ai/`, `pipeline/`, `languages/`; development-governance discipline under a new `governance/` subdirectory) and the reason the pack directory name remains `dev-security/` (developer discoverability — developers shop for "security rules," not for "GRC rules" or "development discipline"). The directory-structure ASCII tree now includes the `governance/` subdirectory as an announced-but-unpopulated entry; the tree is the directory layout contract for the phased rollout.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) `## Security requirements` heading renamed to `## Security and governance requirements`; a new paragraph below the existing rule-file bullets announces the pack's broader contract and clarifies that this project's loaded rules are unchanged in Phase 1 (this project's own governance discipline is already encoded in the existing `## Boundaries` and `## Behavioral rule` sections plus the 32-gate audit programme).

### Phased rollout context

This is the first of a six-phase rollout that broadens the [`dev-security/claude-rules/`](dev-security/claude-rules/README.md) pack from security-only to security + development-governance discipline:

1. **Phase 1 (this release).** Announce the broadened contract; introduce the governance subdirectory in the documented layout. No new rule files.
2. **Phase 2.** Add a gate-discipline rule that codifies "never weaken or delete a gate to silence a failure; fix the artefact" as a portable pack rule.
3. **Phase 3.** Add a change-tracking discipline rule that codifies the CHANGELOG-on-PR pattern with opt-out trailers, citing the D1 delta gate shipped in Library 2026.05.138.
4. **Phase 4.** Add an evidence-grounded-completion rule that lifts the user-level Rule 6 ("completion claims require evidence-grounded verification") into a portable, shareable rule.
5. **Phase 5.** Add a clarify-before-acting rule that lifts the Karpathy-adapted rule from this project's [`.claude/CLAUDE.md`](.claude/CLAUDE.md) into a portable pack file.
6. **Phase 6.** Add an artefact-and-branch-discipline rule that bundles no-hand-editing-generated-artefacts, no-direct-push-to-protected-branches, and the version-monotonicity contract.

Each phase is shipped as its own pull request with its own CHANGELOG entry and library version bump. Per-PR cycle cost is accepted as the price of better per-rule reviewability and assurance.

### Verification

Full 32-gate audit programme passes standalone immediately before commit; new D1 CHANGELOG-on-PR delta gate (Library 2026.05.138) passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.138

CHANGELOG enforcement gate and prior-PR catch-up entry.

### Added

- New CI-only delta gate **D1: CHANGELOG-on-PR check** ([`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py)) that fails a pull request when the diff against the merge-base with the target branch does not include [`CHANGELOG.md`](CHANGELOG.md). An opt-out trailer `Changelog: <one-line-reason>` in any commit message body in the PR range satisfies the gate. The gate runs only on `pull_request` events in [`.github/workflows/quality.yml`](.github/workflows/quality.yml); it is not part of the 32-gate corpus audit programme and is exempt from gate 31's name-parity audit because its inputs (git history range, PR base ref) are unavailable in [`tools/run_all_audits.sh`](tools/run_all_audits.sh) and [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml) checkout step now uses `fetch-depth: 0` so the delta gate can resolve the merge-base.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6.1 documents the new PR-only delta gate category and the opt-out trailer convention.

### Changed

- Catch-up entry for prior PR #5 ([`d1fb4d0`](https://github.com/jposluns/grc_library/commit/d1fb4d0)): added a "Behavioral rule: clarify before acting" section to [`.claude/CLAUDE.md`](.claude/CLAUDE.md), adapted from [Karpathy's "Think Before Coding" CLAUDE.md rule](https://github.com/multica-ai/andrej-karpathy-skills) (MIT-licensed). The rule was merged without a CHANGELOG entry; this entry records it retroactively. The new D1 gate above prevents this miss from recurring.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green. The new D1 gate is exercised by this PR itself: this PR modifies [`CHANGELOG.md`](CHANGELOG.md), so D1 passes; if it had not, D1 would have blocked merge.

---

## 2026-05-31, Library Version 2026.05.137

Corpus-wide hyperlink sweep and TODO.md cleanup.

### Changed

- Converted 414 unlinked backtick-wrapped file references to markdown links across 48 files (root specs, governance, compliance, security, privacy, resilience, operations, supply-chain, dev-security, ai, docs, tools). Detection extends the existing [`tools/lint-changelog-link-coverage.py`](tools/lint-changelog-link-coverage.py) regex across every markdown file. Resolution order: relative to source dir, relative to repo root, tail-path match, then unique-basename fallback. Adopter-project filenames (Claude rule files, AGENTS files, package manifests), placeholder patterns containing angle brackets / braces / wildcards, command-line invocations, and references to deleted or external-project files are intentionally left as code-formatted text. 43 residual code-formatted references remain by design.
- Removed stale CC0-era artefacts from [`TODO.md`](TODO.md): P1/P2/P3 placeholder sections (phase references no longer mapped to the public-release history), P6.2 OT/ICS (verifiably complete in [`operations/ot/`](operations/ot/)), and phase-number prefixes on Decisions log entries. Rephrased P6.1 to focus on the remaining multi-cloud governance gap (per-cloud baselines already shipped in [`dev-security/`](dev-security/)). Nuanced P5.7 (Saudi Arabia annex exists; Argentina/Mexico in the Latin America annex) and P5.8 (US/China AI rules already partially covered in the respective privacy annexes).

### Fixed

- One-line content-generation typo in [`tools/README.md`](tools/README.md) introduced by an earlier direct-to-main MCP push: line 28 `# restrict scope to specific paths` corrected to `# regen-and-check`.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.

---

## Initial public release (2026-05-31, Library Version 2026.05.136): CC BY-SA 4.0

First public commit of the Governance, Risk, and Compliance Documentation Library, published under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). See [`LICENSE`](LICENSE) for the full legal code and [`NOTICE.md`](NOTICE.md) for the repository's external-reference boundary.

### Acknowledgements

The substance of this library draws on knowledge, experience, war stories, and patient mentorship accumulated over more than two decades by a community of GRC and security practitioners, with roots going back to the early 2000s. See [`AUTHORS.md`](AUTHORS.md) for the acknowledged contributors and the maintainer's attribution preference.

Corrections, contributions, and additional acknowledgements are welcomed via the workflow in [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.
