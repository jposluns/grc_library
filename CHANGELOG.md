# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

## 2026-06-01, Library Version 2026.05.144

Phase 6 (final) of the dev-security pack scope expansion: fifth and last governance rule lands; the phased rollout announced at pack version 1.6.0 is complete.

### Added

- [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) — new pack rule codifying two related disciplines that protect a project's audit trail: (1) generated artefacts are read-only (never hand-edit; always regenerate from the source; commit source plus generated output together; CI verifies via `--check` mode); (2) protected branches are append-only (no direct push; no force-push; PR-only merges). The rule defines what counts as a generated artefact (build outputs, schema dumps, taxonomies, doc portals, lockfiles, generated tests), what counts as a protected branch (default branch, release branches, long-lived integration branches), the required workflows for each, prohibited anti-patterns (hand-editing generated files to skip a regeneration round-trip, regenerating in CI to bypass the drift check, stripping `--check` jobs, direct push to protected branches, force-push that drops version-bearing commits, merging without going through the PR mechanism), the version-monotonicity contract that binds branch protection as the primary defence and the version-monotonicity audit as the backstop, tool-specific guidance (CI invocation patterns, branch-protection settings checklist, lockfile updates, long-lived integration branches), exception-handling protocols for both generated-artefact and branch-protection exceptions (governance-authority approval, tracked-issue link, preservation of pre-rewrite refs under `refs/preservation/`, post-rewrite re-audit), and framework alignment (NIST SSDF PO.5/PW.4/PS.1/RV.1; CSA CCM CCC-01-04/AIS-04/LOG-02/LOG-08; ISO 27001 A.5.4/A.8.15/A.8.32; SLSA Level 2-3). Pack-distributable form of this project's `## Boundaries` rules on generated files and direct pushes to `main`; generalises into a project-agnostic discipline.
- [`.claude/rules/governance/artefact-and-branch-discipline.md`](.claude/rules/governance/artefact-and-branch-discipline.md) — project consumption copy.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.11.0. "Pack scope" section reflects rollout completion (all five governance rules shipped); directory-structure ASCII tree shows the five-rule governance subdirectory marked as "rollout complete"; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fifth bullet for the artefact-and-branch-discipline rule. Closing paragraph updated to announce rollout completion.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/artefact-and-branch-discipline.md bullet; pack-version paragraph updated from 1.10.0 to 1.11.0 and notes the phased rollout is complete with the five governance rules shipped. The new rule explicitly cross-references this project's `## Boundaries` rules on generated files ([`taxonomy.yml`](taxonomy.yml), the `docs/` portal, scorecards) and on direct pushes to `main` as the source material.
- [`README.md`](README.md): library version bumped 2026.05.143 to 2026.05.144; README version bumped 1.7.136 to 1.7.137.

### Phased rollout context

This is Phase 6 of 6, the final phase. With this release the phased governance rollout announced at pack version 1.6.0 is complete: gate-discipline (1.7.0), change-tracking (1.8.0), evidence-grounded-completion (1.9.0), clarify-before-acting (1.10.0), and artefact-and-branch-discipline (1.11.0). Future pack work may add rules under `governance/` as the discipline expands, but the planned set is shipped.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file with zero findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff). The version-monotonicity audit confirms the library version sequence 2026.05.139 through 2026.05.144 across the six phases is strictly monotonic.

---

## 2026-06-01, Library Version 2026.05.143

Phase 5 of the dev-security pack scope expansion: fourth governance rule lands.

### Added

- [`dev-security/claude-rules/governance/clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md) — new pack rule codifying "when a request has more than one reasonable interpretation, or an external value the request does not pin down is required to proceed, surface the ambiguity in one sentence and ask before acting." The rule defines five ambiguity-detection categories (multi-interpretation requests, missing external values, project-convention choices, trade-offs, unclear world state), distinguishes when to ask versus when to use sensible defaults (ask when a wrong choice produces unwindable work or has consequences beyond this PR; default when a convention exists and the wrong-guess cost is bounded), specifies how to ask (one sentence, named alternatives, recommended option labelled and listed first, consequence stated), enumerates prohibited anti-patterns (silently picking, asking after acting, asking trivia, hiding ambiguity in narration, treating prior authorisation as durable when scope changed, leading-recommendation theatre, questions that require scrolling), gives tool-specific guidance for AI coding assistants (structured-question primitives, plan mode, investigation-first when state is unclear, scope-creep surfacing), enumerates exception cases (pre-authorised durable instructions like a project CLAUDE.md memory file, emergency response, reversible exploration), and provides framework alignment (NIST SSDF PO.1/PO.5/RV.1/RV.2, CSA CCM GRC-01/GRC-04/IAM-09/TVM-01/CCC-01-03, ISO 27001 A.5.1/A.5.4/A.5.15/A.5.18/A.5.27/A.8.16/A.8.32). Pack-distributable form of this project's `## Behavioral rule: clarify before acting` section; generalises that rule into a project-agnostic discipline.
- [`.claude/rules/governance/clarify-before-acting.md`](.claude/rules/governance/clarify-before-acting.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.10.0. "Pack scope" section now lists four shipped governance rules with their pack-version timing and names the final rollout rule (artefact-and-branch discipline) as the next phase. Directory-structure ASCII tree shows all four populated; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fourth bullet for the clarify-before-acting rule.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/clarify-before-acting.md bullet; pack-version paragraph updated from 1.9.0 to 1.10.0 and lists all four shipped governance rules. The new rule explicitly cross-references this project's `## Behavioral rule: clarify before acting` section as the source.
- [`README.md`](README.md): library version bumped 2026.05.142 to 2026.05.143; README version bumped 1.7.135 to 1.7.136.

### Phased rollout context

This is Phase 5 of 6. The final phase will add artefact-and-branch discipline (the unifying rule covering "never hand-edit generated artefacts; never push directly to protected branches; respect version-monotonicity"), completing the planned governance overlay.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file; one finding ("optimise" -> "optimize") fixed before the audit sweep. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.142

Phase 4 of the dev-security pack scope expansion: third governance rule lands.

### Added

- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) — new pack rule codifying "never declare work done, fixed, ready, shipped, or any synonym without evidence." The rule defines what counts as a completion claim (state assertions a reader will rely on, including "good catch" used to acknowledge a user-reported issue), enumerates the synonym vocabulary that triggers the protocol, specifies the six-step verification protocol (enumerate files in scope, re-read each in full, quote supporting lines with path-and-line-number citations, proactively search for contradictions, distinguish mechanical gate verification from semantic verification, state unverified items explicitly), enumerates prohibited anti-patterns (declaring victory in the response that carries failing evidence, treating user silence as confirmation, relying on prior runs, premature "good catch", pipe-masked exit codes, conflating "I edited the file" with "the file is correct"), gives tool-specific guidance for AI coding assistants (reading tool results before composing summaries, waiting for async work, `set -o pipefail` and `${PIPESTATUS[@]}` for pipe-masked exit codes, stop hooks, self-honesty in summaries), the exception-handling protocol for impractical re-reads, and framework alignment (NIST SSDF RV.1/RV.2/PO.5/PS.1, CSA CCM GRC-04/GRC-05/LOG-02/LOG-08, ISO 27001 A.5.4/A.5.36/A.8.15, OWASP ASVS V1.1/V14.1). Pack-distributable form of the user-level Rule 6 added 2026-05-31 in the maintainer's private global Claude Code memory file; generalises that rule into a portable, project-agnostic discipline.
- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.9.0. "Pack scope" section now lists three shipped governance rules with their pack-version timing; directory-structure ASCII tree shows all three populated; "Rule files and their scope" table gains a new row. The scope-bullet contract description rephrased from "agent-collaboration discipline" to its two component rules (evidence-grounded completion and clarify-before-acting) so the broadened contract is concretely visible.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a third bullet for the evidence-grounded-completion rule with a one-line summary of the six-step protocol. Downstream adopters who drag the payload now inherit all three governance rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/evidence-grounded-completion.md bullet; pack-version paragraph updated from 1.8.0 to 1.9.0 and lists all three shipped governance rules. The project's user-level Rules 1-5 (verification before dependent actions, tool-result authority, async waiting, pre-commit-hook respect, self-honesty) and Rule 6 (the evidence-grounded completion rule itself) are referenced as the pre-existing per-user discipline that this pack rule now codifies for cross-project adoption.
- [`README.md`](README.md): library version bumped 2026.05.141 to 2026.05.142; README version bumped 1.7.134 to 1.7.135.

### Phased rollout context

This is Phase 4 of 6. Phases 5 through 6 will add: clarify-before-acting discipline, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). Searched the new file for the synonym vocabulary the rule itself defines (`done`, `complete`, `fixed`, etc.) and confirmed all occurrences are either in the rule's own enumeration of trigger words or in prose that names the failure mode rather than claiming the rule's own work is done; the rule does not falsify itself. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

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
