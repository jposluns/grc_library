# Changelog

All notable changes to this repository are recorded in this file as lead-paragraph summaries. Detailed maintainer-level entries (full Added / Changed / Removed / Fixed / Security / Verification sections per change) are kept in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md). This is how this project's maintainer tracks the full audit trail. The convention is project-specific; forks may delete `.working/` and adopt their own approach to detailed change tracking. The mechanics are documented in the [`change-tracking` governance rule](dev-security/claude-rules/governance/change-tracking.md).

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

## 2026-06-21, Library Version 2026.06.132, PR #150

Closes **FR-45** (high, ⚠️ confirmed-with-modification). RFC 2119 vocabulary tightening in two security standards: [`security/standard-authentication-and-password-management.md`](security/standard-authentication-and-password-management.md) §"Password requirements" and [`security/standard-remote-working-security.md`](security/standard-remote-working-security.md) §8.2 both used "may not" where the intent is a prohibition. Pass-1 flagged the drift under a strict RFC 2119 reading: "may not" admits a permissible-negative-possibility interpretation distinct from MUST NOT. Both lines now read "must not be" to match each file's prevailing normative verb ("must" appears 5 times in the password standard and 24 times in the remote-working standard; "shall" is essentially absent from both). Per-doc `1.0.1 → 1.0.2` in each file; library `2026.06.131 → 2026.06.132`. Backlog 100 → 99 open.

---

## 2026-06-21, Library Version 2026.06.131, PR #149

Closes **FR-21** (high[critical]). [`compliance/register-compliance-obligations-template.md`](compliance/register-compliance-obligations-template.md) Source Reference field tightened so register citations resolve to a single unambiguous source location: revised description plus a new "Source Reference granularity requirements" sub-section listing minimum-precision patterns (with acceptable / unacceptable examples) for NIST publications, ISO/IEC standards, statutes, COBIT, PCI DSS, CSA CCM, contracts, and voluntary commitments. Closes a register-defeating ambiguity. Per-doc `1.0.2 → 1.0.3`; library `2026.06.130 → 2026.06.131`. Backlog 101 → 100 open.

---

## 2026-06-21, Library Version 2026.06.130, PR #148

Sweep 12 iteration 1 close-out. Three in-window findings from subagents A/B (C zero findings):
- **(H)** [`risk/policy-enterprise-governance-and-risk-management.md`](risk/policy-enterprise-governance-and-risk-management.md): Owner CIO → CRO + governance table CRO row added + CIO row reshaped. PR #143 had only fixed the companion standard; the policy retained the contradiction.
- **(M)** [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md) §2.2: cross-reference added to the new sampling-justification field in [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md) (PR #144 added the field but didn't update the procedure).
- **(L)** [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) §5.2: reciprocal "related risk acceptance ID" field added; closes the latent bidirectional-asymmetry follow-up noted in PR #146's detailed CHANGELOG.

Detail report at [`.working/validate-sweeps/2026-06-21-sweep12-iter1.md`](.working/validate-sweeps/2026-06-21-sweep12-iter1.md). Library `2026.06.129 → 2026.06.130`.

---

## 2026-06-21, Library Version 2026.06.129, PR #147

Closes **FR-3** (high, newcomer-onboarding). New "New to GRC? Start here" section added to [`README.md`](README.md) between the metadata header and §Purpose. The block expands the acronym (the README's title carries `GRC` but never defines it), defines Governance / Risk / Compliance in plain language for a reader unfamiliar with the discipline, names the adjacent domains the library treats as siblings (security, privacy, resilience, supplier governance, AI governance), and signposts five role/intent-keyed next steps (first-time visitor, adopter, auditor, maintainer, glossary-lookup). README per-doc `1.8.84 → 1.9.0` (minor: new top-level section). Library `2026.06.128 → 2026.06.129`. Backlog 102 → 101 open.

---

## 2026-06-21, Library Version 2026.06.128, PR #146

Closes **FR-96** (high, ⚠️ confirmed-with-modification). [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md) "Required record fields" gains a `Related exception register entry` field — the ID of the corresponding entry in the exception register if the acceptance derives from a policy/control exception, or `None` if pure risk acceptance. The linkage makes the two registers cross-traversable for audit traceability. Per-doc `1.0.0 → 1.0.1`; library `2026.06.127 → 2026.06.128`. Backlog 103 → 102 open.

---

## 2026-06-21, Library Version 2026.06.127, PR #145

Closes **FR-95** (high). [`risk/template-enterprise-risk-register.md`](risk/template-enterprise-risk-register.md) Acceptance section now requires a `Compensating Controls` field. The procedure already required compensating-controls analysis per [`risk/procedure-risk-acceptance.md`](risk/procedure-risk-acceptance.md) §5; the template now records each control with a brief note on how it offsets the un-treated risk so the acceptance record is self-contained and auditable. Per-doc `1.0.1 → 1.0.2`; library `2026.06.126 → 2026.06.127`. Backlog 104 → 103 open.

---

## 2026-06-21, Library Version 2026.06.126, PR #144

Closes **FR-22** (high). [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md) operating-evidence section now requires a mandatory `Sampling justification` field per test (population size, sample size, selection method, confidence-level assumption, citation to [`compliance/procedure-control-testing.md`](compliance/procedure-control-testing.md) §2.2 sample-size table). "100% population review" is the explicit response when sampling doesn't apply. External auditors now see the statistical-basis justification for every sample without reconstructing it from peer documents. Per-doc `1.0.0 → 1.0.1`; library `2026.06.125 → 2026.06.126`. Backlog 105 → 104 open.

---

## 2026-06-21, Library Version 2026.06.125, PR #143

Closes FR-9 (high[critical]) and FR-10 (high) together — both relate to Chief Risk Officer presence in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md). The standard's `Owner` field changes from "Chief Information Officer" to "Chief Risk Officer"; §3 Governance gets a new CRO row scoped to risk strategy, risk appetite stewardship, and ERM programme outcomes; the pre-existing CIO row is reshaped to "provides executive support on technology-risk integration". Per-doc `1.3.3 → 1.3.4`; library `2026.06.124 → 2026.06.125`. Backlog 107 → 105 open.

---

## 2026-06-21, Library Version 2026.06.124, PR #142

First fitness-remediation PR. Closes four unambiguous quick-win findings at maintainer direction while the maintainer reviews the broader 111-item backlog: **FR-13** disambiguates `CPPA` in [`risk/standard-enterprise-risk-management.md`](risk/standard-enterprise-risk-management.md) §10 framework alignment table; **FR-54 / FR-55** add an explicit doctype-prefix mapping table to [`specification-master-project.md`](specification-master-project.md) §4.3 covering all 17 doctypes; **FR-103** adds a Chief Compliance Officer row to the Continuous Assurance framework's governance table. Backlog totals updated: 93 immediate-priority + 14 deferred = 107 open (4 closed). Library `2026.06.123 → 2026.06.124`.

---

## 2026-06-21, Library Version 2026.06.123, PR #141

Pass-2 of the fitness review (per the discipline in PR #139). Surfaced the four Pass-1 buckets to the maintainer via structured triage; outcomes: ✅ batch (91) accepted with Low tier deferred; ⚠️ batch (16) accepted with orchestrator's modifications; 🤔 batch (2) — FR-14 resolved to ✅ with library-wide CMMI propagation plan, FR-110 to ✅ at Medium; ❌ batch (2) reshaped (FR-43 kept at High[critical] with corrected 5-level-standard vs 4-level-subset framing; FR-53 downgraded to Low as metadata-field-unification question). New "Fitness review backlog" section in [`TODO.md`](TODO.md) groups all 111 FR-IDs by severity tier with brief summaries for High[critical] and High items; **no remediation begins until maintainer directs**. Also corrects PR #140's narrative miscount (93/14 → 91/16). Library `2026.06.122 → 2026.06.123`.

---

## 2026-06-21, Library Version 2026.06.122, PR #140

Pass-1 verification (per the discipline introduced in PR #139) applied to the existing 111 FR-N findings in [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md). Five verification-task subagents dispatched in parallel; each performed direct source re-reads (no persona role) and applied one verdict tag per finding. Aggregate: **93 ✅ confirmed-as-stated / 14 ⚠️ confirmed-with-modification / 2 🤔 ambiguous-needs-maintainer / 2 ❌ rejected**. New §8.5 "Pass-1 Verification Results" added to the report with verdict table + per-bucket summary. Pass-2 (maintainer-interactive bucket processing) is the next queued PR. Library `2026.06.121 → 2026.06.122`.

---

## 2026-06-21, Library Version 2026.06.121, PR #139

Amends the `library-fitness-review` skill (`/fitness`) to introduce the unverified→confirmed labelling discipline. Subagent findings are now `verification: unverified` at output time; Pass-1 (orchestrator re-reads cited source and tags `✅` / `⚠️` / `❌` / `🤔`); Pass-2 (maintainer-interactive bucket processing). Triage by severity applies only to confirmed findings, which produce TODO entries carrying FR-N ID + run reference + verification date. SKILL.md Step 5 restructured into four sub-steps; [`.claude/commands/fitness.md`](.claude/commands/fitness.md) updated in parallel (paired-skill step-parity gate); [`.working/fitness-reviews/README.md`](.working/fitness-reviews/README.md) workflow rewritten. The existing 111 findings in [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md) retroactively marked `verification: unverified` pending Pass-1 in the next PR. Pack `1.33.0 → 1.34.0`; library `2026.06.120 → 2026.06.121`.

---

## 2026-06-21, Library Version 2026.06.120, PR #138

Rotates the five shipped Priority 4 items (P4.1 through P4.5) from [`TODO.md`](TODO.md) into [`.working/DONE.md`](.working/DONE.md) as `### TODO P4.x` entries cross-referenced to the original "Shipped 2026-06-20 as ..." framing. P4.6 (corpus-management discipline as a shareable skill) remains forward-looking. Also removes the Sweep 4 follow-up historical note from "Open follow-ups from validation sweeps" (resolved and previously noted as no-longer-tracked). Closes the TODO content cleanup queued since PR #135. Library `2026.06.119 → 2026.06.120`.

---

## 2026-06-21, Library Version 2026.06.119, PR #137

New audit gate 46 ([`tools/lint-overnight-file.py`](tools/lint-overnight-file.py)) plus stub-format [`.working/overnight-pr.md`](.working/overnight-pr.md) plus pack rule amendment documenting the overnight-work protocol. The file's `Status:` field encodes lifecycle: `stub` (no overnight in flight, default) and `in-flight` (active session) pass; `done` (ended, awaiting morning processing) fails. The three-state field preserves the overnight workflow (overnight PRs land with `in-flight`) while applying mechanical pressure for morning processing once the session ends. Pack rule [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) gains a new "Overnight-work protocol" subsection under PR finalization protocol; mirrored to [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md). Pack `1.32.0 → 1.33.0`; spec `1.13.1 → 1.14.0`; library `2026.06.118 → 2026.06.119`.

---

## 2026-06-21, Library Version 2026.06.118, PR #135

Restructures the working-state ledgers: new [`.working/design-decisions.md`](.working/design-decisions.md) file becomes the home for design-decision content; the "Design decisions made" section is rotated out of [`.working/DONE.md`](.working/DONE.md) (which is now strictly closed-TODO items); fitness-skill-specific decisions migrate out of the project's overnight-PR working file; TODO's "Decisions log" section migrates in as "Decisions explicitly dropped"; the overnight-PR working file is deleted as its substantive content has been routed and its procedural content has no forward-looking value. [`TODO.md`](TODO.md) "Notes on maintenance" updated to reflect the DONE-and-design-decisions routing. Maintainer-confirmed overnight-protocol-with-stub-and-gate standard added to TODO queued sequence as the next PR. Library `2026.06.117 → 2026.06.118`.

---

## 2026-06-21, Library Version 2026.06.117, PR #134

Gate 45 (TODO staleness audit) regex tightened to eliminate a false positive. The earlier `[^\n]{0,80}` window between "next/queued/pending" markers and `PR #<digit>` matched any digit-bearing PR ref within 80 characters, including historical parenthetical references in queued-item descriptions (e.g. `**Next, PR #N: TODO content cleanup.** Maintainer-surfaced (2026-06-21, during PR #133):`). The tighter character class `[\s,:—–-]*` allows only whitespace, commas, colons, and dashes between the marker and the digit-bearing PR ref, so the queued PR must be the immediately-following PR target. False-positive eliminated; real-drift cases (`Next, PR #128`, `Next — PR #128`, `queued PR #128`) still match. Post-PR-#133 merge `push`-event run on `main` failed on this false positive; this PR is the small focused fix.

---

## 2026-06-21, Library Version 2026.06.116, PR #133

Documents the project's language convention as **Canadian English first, Commonwealth (UK / Australian) English second, other dialects last**. Canadian English shares the `-ize` / `-ization` orthography with American English (the Oxford convention adopted in Canadian usage), so the [`tools/lint-language.py`](tools/lint-language.py) enforcement is the Canadian-orthography manifestation of the convention, not a generic American mandate. Doc-only change: linter docstring, [`.claude/CLAUDE.md`](.claude/CLAUDE.md) Conventions section, and [`CONTRIBUTING.md`](CONTRIBUTING.md) Style requirements rewritten to lead with the convention statement. No linter behaviour change. CONTRIBUTING `1.1.0 → 1.2.0`; library `2026.06.115 → 2026.06.116`.

---

## 2026-06-21, Library Version 2026.06.115, PR #132

Adds [Ryk Edelstein](https://github.com/fedelst) to the Acknowledged contributors list in [`AUTHORS.md`](AUTHORS.md). First PR exercising the post-PR-#131 steady-state TODO/DONE rotation discipline (item rotated from TODO to DONE in the same commit). Includes a one-time bootstrap correction: PR #131 itself is added to DONE retroactively, since it created DONE but did not record its own entry.

---

## 2026-06-21, Library Version 2026.06.114, PR #131

Introduces [`.working/DONE.md`](.working/DONE.md), the closed-TODO ledger, and rotates all historical "PRs completed this session" entries (PRs #110-#130) and "Key design decisions made this session" subsections out of [`TODO.md`](TODO.md) into DONE. TODO is now forward-looking only. Pack rule [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) gains a "PR finalization protocol" section documenting three disciplines: TODO is forward-looking (delete-on-close, no strikethroughs); DONE complements CHANGELOG (CHANGELOG by PR, DONE by closed item); after-merge protocol of listing the next-N planned PRs from TODO. [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR workflow extended with two new steps capturing both disciplines durably. Pack `1.31.0 → 1.32.0`; library `2026.06.113 → 2026.06.114`.

---

## 2026-06-21, Library Version 2026.06.113, PR #130

Removes decorative gate-count narrations from prose throughout the corpus and tooling. Phrases like "the 45-gate audit programme", "all 45 gates", "gates 1-45", and "45 corpus gates" are now "the audit programme", "every gate", "all corpus gates", and "the corpus gates" respectively; the spec §6 inventory remains the canonical single source for the count. Eleven prose locations updated across seven files. Implements the maintainer's just-surfaced proposal that decorative counts add no information beyond what readers can derive from the inventory table, and add real cost on every gate-add PR (PR #128 cascaded ten N-gate references across seven files; PR #129 cascaded one more). Gate 39 (cross-file gate-count consistency) remains as the defence against new decorations creeping back in.

---

## 2026-06-21, Library Version 2026.06.112, PR #129

Post-PR-#128 catch-up: [`TODO.md`](TODO.md) still framed PR #128 as "Next" after PR #128 merged, which the brand-new gate 45 (TODO staleness audit) correctly flagged on the post-merge `main` `push`-event run. Fixes the TODO drift: PR #128 moved to PRs-completed list with its summary; queued sequence rebased to start with the fitness-skill amendment; version-snapshot refreshed to 2026.06.111; the maintainer's two design proposals (DONE.md ledger; decorative-gate-count cleanup) recorded as queued follow-ups. This is the first instance of gate 45 catching exactly the failure mode it was built to catch — its own PR's lingering "queued" framing.

---

## 2026-06-21, Library Version 2026.06.111, PR #128

New audit gate 45 (TODO staleness audit) plus a PR-time-checks wrapper script. Gate 45 mechanically catches the two TODO drift shapes that recurred across four consecutive validation sweeps (queued PR already merged; sweep cursor behind history); the wrapper [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh) bundles the two PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR version-bump) and gate 45 into one local runner the maintainer invokes before push. Together with [`tools/run_all_audits.sh`](tools/run_all_audits.sh), the two runners cover every gate the CI workflow runs. The two-runner split is a structural fix for the version-bump-omission failure mode that surfaced in PR #127's first push: every gate now has a local invocation path. Spec [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 inventory extended; [`TODO.md`](TODO.md) preamble amended to note the narrow gate-45 exception to TODO's "informational only" status; [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR workflow updated to require both runners. New TODO P4.6 records the "corpus-management discipline as a shareable skill" follow-up the maintainer authorised, scheduled after the fitness backlog closes.

---

## 2026-06-21, Library Version 2026.06.110, PR #127

Sweep 11 iteration 1 close-out. Eight in-window findings actioned: corrected the fitness report's count mismatch across six surfaces (95/18/22/31/24 → mechanically-tabulated 111/17/20/57/17); updated [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) D1 description for dual-entry post-PR-#125; refreshed TODO and reframed its session-pause snapshot as "as-of-last-refresh" (one-time convention amendment to address the four-consecutive-sweep recurring drift); softened workflow ordering in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md); renamed [`.working/README.md`](.working/README.md) "Created by" column to "Origin"; bumped library version.

---

## 2026-06-21, Library Version 2026.06.109, PR #125

Splits the CHANGELOG into a two-file convention: root file carries lead-paragraph summaries (adopter-facing); detailed mirror in a working directory carries full structured-section entries (maintainer-grade). Historical content preserved verbatim in the detailed mirror; root file trimmed to first paragraphs (2926 lines → 675 lines). Delta gate extended to require both files move in lock-step. Change-tracking governance rule amended; pack version 1.30.0 → 1.31.0. First PR using the dual-entry convention; this entry dogfoods it.

---

## 2026-06-21, Library Version 2026.06.108, PR #124

First-ever invocation of the `library-fitness-review` skill (`/fitness`). Ten persona subagents dispatched in parallel. Aggregate raw findings 145; after dedupe approximately 95 unique. Severity distribution: 18 high[critical] / 22 high / 31 medium / 24 low.

---

## 2026-06-21, Library Version 2026.06.107, PR #123

Sweep 10 iteration 3 close-out: one in-window Medium finding actioned. Convergence-delta narrowing from iter 2's 7 findings to iter 3's 1.

---

## 2026-06-21, Library Version 2026.06.106, PR #121

Sweep 10 iteration 2 close-out: seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120).

---

## 2026-06-21, Library Version 2026.06.105, PR #120

Adds a new `library-fitness-review` skill to the `dev-security/claude-rules/` pack, invoked via the `/fitness` slash command. The skill is a comprehensive whole-corpus library-quality review dispatching ten persona reviewers in parallel (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Designed as a periodic deliverable (after major changes or quarterly minimum), not a per-PR gate; complements the per-PR `validation-sweep` skill (`/validate`). Output is an 8-section combined report with a discrete remediation backlog. This PR was authored end-to-end during an overnight session under explicit maintainer authorisation; see [`.working/overnight-pr.md`](.working/overnight-pr.md) for the decision log.

---

## 2026-06-21, Library Version 2026.06.104, PR #118

Restructured `.working/validate-sweeps/` to the canonical `<activity>/{README,history,detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory going forward. The validation-sweep history file moves into the subdirectory; verbose static content (failure-mode taxonomy, maintenance protocol, accept-list rules, dating discipline, framework alignment) moves to the subdirectory's README; the history file becomes a slim reverse-chronological table; per-iteration detail files are created only when findings exist.

---

## 2026-06-21, Library Version 2026.06.103, PR #117

Sweep 10 iteration 1 close-out: six in-window prose drift findings actioned, all introduced or made visible by the three-PR `.working/` sequence (PRs #114-#116).

---

## 2026-06-21, Library Version 2026.06.102, PR #116

Move the validation-sweep history file from `governance/` to `.working/`. The file is project-specific application of the validation-sweep discipline, not template content for adopters; per the framing established with the maintainer, application belongs in `.working/`. Template content (the failure-mode class taxonomy, the maintenance protocol, the false-positive accept-list rules, the dispatch-declaration discipline) lives in the [`validation-sweep` SKILL.md](dev-security/claude-rules/skills/validation-sweep/SKILL.md) in the pack; adopters get the discipline from the SKILL.md and start their own history file from zero in their fork.

---

## 2026-06-21, Library Version 2026.06.101, PR #115

`/validate` slash-command rename + per-iteration record convention. Second of the four-PR sequence around `.working/` (PR #114 shipped the infrastructure; this PR populates the first subdirectory and adds the persistent-record discipline to the validation-sweep skill).

---

## 2026-06-21, Library Version 2026.06.100, PR #114

Establishes the `.working/` top-level convention for maintainer working state. First of a four-PR sequence: this PR ships the infrastructure; subsequent PRs (`/validate` rename + per-run records, `/fitness` skill, changelog-details migration) populate the convention with content.

---

## 2026-06-21, Library Version 2026.06.99, PR #113

Sweep 9 iteration 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 actioned.

---

## 2026-06-21, Library Version 2026.06.98, PR #112

Sweep 9 iteration 2 closure + seventh governance rule ([`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md)).

---

## 2026-06-20, Library Version 2026.06.97, PR #111

Sweep 9 closure: Subagent C findings actioned + structural prevention of unauthorised subagent skips.

---

## 2026-06-20, Library Version 2026.06.96, PR #110

Validation-sweep finding (post-P4.5 sweep, Subagent B): two stale "42 gates" prose references that gate 39 missed. Plus a related pattern-set extension to close the gap going forward.

---

## 2026-06-20, Library Version 2026.06.95, PR #109

TODO P4.5: audit evidence package template. **Fifth and last of the Priority 4 items in sequence.**

---

## 2026-06-20, Library Version 2026.06.94, PR #108

Rename the adopter quickstart template from its prior "by-profile" filename to [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer feedback: the file is no longer a per-profile template (after the P4.1 rewrite to activity-modular shape in PR #105), so the prior filename was misleading. The document title was already "Adopter Quickstart Template" so no title change is needed.

---

## 2026-06-20, Library Version 2026.06.93, PR #107

TODO P4.4: regulator interaction templates. Fourth of five Priority 4 items.

---

## 2026-06-20, Library Version 2026.06.92, PR #106

TODO P4.3: implementation roadmap template. Third of five Priority 4 items.

---

## 2026-06-20, Library Version 2026.06.91, PR #105

Heavy rewrite of [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer's feedback on PR #103: the six fixed profiles (small business, mid-market regulated industry, multi-national enterprise, public-sector adopter, healthcare adopter, financial-services adopter) were too rigid; companies do not fit into the categories, and the same category contains very different operational realities.

---

## 2026-06-20, Library Version 2026.06.90, PR #104

TODO Priority 4.2: adopter maturity self-assessment template. Second of five Priority 4 items in sequence.

---

## 2026-06-20, Library Version 2026.06.89, PR #103

TODO Priority 4.1: adopter quickstart template per profile. First of five Priority 4 items the maintainer authorised in sequence.

---

## 2026-06-20, Library Version 2026.06.88, PR #102

Register-to-TODO alignment for [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) §6 (Document-type capability gaps). The register-vs-TODO diff (per the maintainer's "complete everything that isn't yet logged in TODO" instruction) found three drift items in §6; all are resolved here by lightweight bookkeeping updates rather than substantive document creation.

---

## 2026-06-20, Library Version 2026.06.87, PR #101

Refresh the `Cross-document numerical coherence shipped as scaffold` entry in [`TODO.md`](TODO.md)'s Decisions log. The prior text described the linter as tracking "0 terms" and the framework as "in place for future term curation"; that description is stale relative to the implementation. The scaffold has been progressively widened since the decision was logged: Phase 23.26 added P1/P2/P3 acknowledgement-time patterns as scaffolding, Phase 23.35 added the GDPR breach-notification-hours pattern after empirical confirmation. The current scaffold tracks four terms; the [`tools/lint-cross-doc-numbers.py`](tools/lint-cross-doc-numbers.py) docstring documents why each candidate (RTO, RPO, retention, P4, NIS 2, DORA) was considered and excluded with rationale.

---

## 2026-06-20, Library Version 2026.06.86, PR #100

**Closes the three-item queued-session backlog**: new audit gate 44 (paired-skill step-parity audit), third and last of the items announced in the maintainer's status summary (after PR #98 PF-04 stale-version-literal scanner extension and PR #99 gate 43 follow-up ageing audit). Mechanises the cross-document term-and-identifier consistency check the validation-sweep history register flagged as a recurring gap.

---

## 2026-06-20, Library Version 2026.06.85, PR #99

New audit gate 43: follow-up ageing audit. Mechanises Rule 3 of the maintenance-tag dating discipline introduced in PR #90 (the convention shipped without a mechanical gate; this PR adds it). Second of three queued session items.

---

## 2026-06-20, Library Version 2026.06.84, PR #98

Pre-flight scanner pattern set extended. Adds **PF-04 stale-version-literal**: catches phrases like "currently 1.22.0" / "the current 1.22.0" / "now at 1.22.0" / "now on 1.22.0" where the captured version does not match any of the canonical library, README, pack, or spec versions. Motivated by the Sweep 4 finding in `docs/adopter-guide.md:57` ("ships with its own version sequence (currently `1.22.0`)"); the new pattern would have caught that finding mechanically rather than requiring semantic triage. First of the three queued session items announced in the maintainer's status summary.

---

## 2026-06-20, Library Version 2026.06.83, PR #97

Validation-sweep maintenance-protocol change plus retroactive CHANGELOG prune. Maintainer observed that zero-finding sweeps were producing standalone PRs with full CHANGELOG entries that contained no user-visible content, distracting from substantive entries. The convention is revised: **zero-finding sweeps leave no trace** (no register entry, no CHANGELOG entry, no standalone PR; the convergence-delta trend lives in the iteration counter, not in a per-sweep record).

---

## 2026-06-20, Library Version 2026.06.82, PR #96

Validation-sweep enhancement, seventh and last from the late-research-findings queue. **Closes the queue.** Adds the hold-the-line ratcheting-baseline discipline to step 6 (Triage) of the SKILL: fingerprint-not-count, expiry plus rationale, net-negative invariant on sweep close. This is the "largest" tier (after the smallest four: synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta; and the medium two: multi-agent debate, SARIF-lite).

---

## 2026-06-20, Library Version 2026.06.80, PR #94

Validation-sweep enhancement, sixth of seven from the late-research-findings queue. Adds the SARIF-lite output format to step 4 of the SKILL: each subagent finding is a fenced markdown block with six labelled lines (tool / ruleId / level / location / fingerprint / rubric) plus an evidence paragraph. Closes the "medium" tier of the queue (after Rule 5.5 multi-agent debate in PR #93); only the "largest" tier (hold-the-line ratcheting baselines) remains.

---

## 2026-06-20, Library Version 2026.06.79, PR #93

Validation-sweep enhancement, fifth of seven from the late-research-findings queue. Adds Rule 5.5 to the synthesis rubric: single-round asymmetric debate for high-divergence disagreement between subagents. First of the "medium" tier (after the smaller-scope patterns 1-4).

---

## 2026-06-20, Library Version 2026.06.77, PR #91

Validation-sweep enhancement, fourth of seven from the late-research-findings queue. Replaces the fixed 3-iteration cap in step 7 with a principled three-condition termination: empty-delta primary stop, patience-plateau secondary stop, and a 6-iteration hard ceiling as runaway guard. Closes the last of the "smallest" tier in the queue (synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta).

---

## 2026-06-20, Library Version 2026.06.76, PR #90

Validation-sweep enhancement, third of seven from the late-research-findings queue. Adds the Wikipedia-style maintenance-tag dating convention to the sweep-history register's Maintenance protocol, closing the gap where deferred findings accumulated without ageing signal.

---

## 2026-06-20, Library Version 2026.06.74, PR #88

Validation-sweep enhancement, second of seven from the late-research-findings queue. Adds a pre-tool verification preamble to the subagent fan-out discipline in step 4 of the validation-sweep skill. Closes the gap where subagents could make redundant or misdirected tool calls without an auditable justification trace.

---

## 2026-06-20, Library Version 2026.06.72, PR #86

Validation-sweep pre-flight scanner: noise-reduction enhancement. Across Sweeps 3, 4, and 5, the same 12-13 candidate findings re-surfaced on every run and were re-triaged as false positives every time. The maintainer asked: should the scanner be enhanced so it does not keep tagging the same shapes? Chose option 3 of the named alternatives: both heuristics and an exemption file.

---

## 2026-06-20, Library Version 2026.06.71, PR #85

Closes the Sweep 4 out-of-window classification-convention follow-up. The maintainer's decision (asked-and-answered, option "both, with primary tag"): a finding may carry more than one failure-mode class; one is tagged primary (the dominant mechanism) and one or more may be tagged secondary (the symptom shape). Historical entries from Sweeps 1-3 are not retro-applied; the convention applies from Sweep 5 onwards.

---

## 2026-06-20, Library Version 2026.06.69, PR #83

Validation Sweep 4 in-window finding (C1 stale-prose): the adopter-guide's Mode C section says the pack "ships with its own version sequence (currently `1.22.0`)" but the pack is at 1.26.6. Surfaced by Subagent B of the Sweep 4 fan-out; the new synthesis rubric tagged this `R` (read-verified), severity `should-fix-this-PR`. Fix uses number-stable wording rather than bumping the literal so the same drift does not recur on the next pack bump.

---

## 2026-06-20, Library Version 2026.06.68, PR #82

Validation-sweep enhancement, first of seven from the late-research-findings queue. Adds a deterministic four-rule synthesis rubric to step 5 of the validation-sweep skill. Closes the prior gap where the parent's synthesis after subagent fan-out was ad-hoc and unreproducible across sweeps.

---

## 2026-06-20, Library Version 2026.06.66, PR #80

Validation-sweep self-finding from the post-PR-79 sweep: cross-surface step-numbering drift. PR #78 introduced the deterministic pre-flight scanner as `### 3.5.` in [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and as `3a.` in [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): same logical step, two different identifiers across parallel surfaces. Surfaced by subagent A of the validation-sweep fan-out (Medium severity, in-window finding).

---

## 2026-06-20, Library Version 2026.06.65, PR #79

Validation-sweep enhancement 4 of 4 from the process-assessment review: nightly scheduled mechanical sweep on `main`. Closes the original four-enhancement queue; the late-research-findings queue (SARIF, hold-the-line, multi-agent debate, maintenance-tag dating, pre-tool verification, synthesis rubric, convergence-delta termination) plus the queued pre-flight pattern-set extension follow in subsequent PRs.

---

## 2026-06-20, Library Version 2026.06.64, PR #78

Validation-sweep enhancement 3 of 4 from the process-assessment review: deterministic pre-flight scanner. The fourth (nightly scheduled sweep) follows in PR #79; then the late-research-findings queue.

---

## 2026-06-20, Library Version 2026.06.63, PR #77

Two validation-sweep discipline enhancements from the maintainer's process-assessment review. Other enhancements (deterministic pre-flight scanner; nightly scheduled sweep) follow in subsequent PRs.

---

## 2026-06-20, Library Version 2026.06.62, PR #76

Validation-sweep cleanup after the morning's `/validation-sweep` run on the post-PR-75 state surfaced two High-severity findings, both meta-ironic instances of the new [`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) skill catching itself violating its own rules. Plus one Medium-severity stale-prose finding from the sibling sweep.

---

## 2026-06-20, Library Version 2026.06.61, PR #75

Add three new skills to the dev-security/claude-rules/ pack, recreated as in-house CC BY-SA 4.0 content from cross-source research. The maintainer authorised the research-then-recreate pattern after a survey of Claude Code Skills on GitHub (kfchou/wiki-skills MIT, anthropics/skills Apache 2.0, obra/superpowers MIT, plus a Sushegaad GRC-content pack) identified three gaps in the existing pack worth filling without importing additional external overlays.

---

## 2026-06-20, Library Version 2026.06.60, PR #74

Layer 3 of the validation programme — invocation-pattern documentation. The validation-sweep skill (shipped in PR #62) is now discoverable via a project slash command and cross-referenced bidirectionally from related skills.

---

## 2026-06-20, Library Version 2026.06.59, PR #73

Wire the collection-candidate detector (shipped in PR #72) to run automatically on PRs that modify the pack. The detector was previously on-demand only; per the maintainer's clarification, it should also fire automatically whenever there is a new addition or an updated pack.

---

## 2026-06-20, Library Version 2026.06.58, PR #72

Add a companion exploratory tool to gate 41 (Collection-enumeration consistency audit): [`tools/detect-collection-candidates.py`](tools/detect-collection-candidates.py). Phase 2 of the Layer 2 / 3 deliverable the maintainer authorised during gate 41's design (PR #69). Gate 41 enforces drift discipline on a hard-coded list of collections; this tool surfaces NEW candidate collections by heuristic scan so the maintainer can triage them one-by-one and add approved candidates to gate 41's configuration.

---

## 2026-06-20, Library Version 2026.06.57, PR #71

Add gate 42 (**External-overlay license consistency audit**). Closes the licence-validation loop the maintainer specified: every file in the repository now has its licence mechanically validated against the appropriate expectation. Gate 15 already enforced the project's `CC BY-SA 4.0` requirement on the corpus's own content; gate 42 extends the same discipline to the external overlay at [`.claude/rules/external/`](.claude/rules/external/), where files retain their source project's licence rather than the project's own.

---

## 2026-06-20, Library Version 2026.06.56, PR #70

Minor formatting cleanup in a historical CHANGELOG entry for prose consistency. No content or behaviour changes.

---

## 2026-06-20, Library Version 2026.06.55, PR #69

Add gate 41 (**Collection-enumeration consistency audit**) — Layer 2 / 3 of 3 in the validation programme. The linter walks a hard-coded configuration of "collections" (currently: pack governance rules and pack skills), each declaring a canonical source-of-truth directory and one or more enumeration locations elsewhere in the corpus. For each collection, the linter compares the canonical set against each enumeration set and flags missing-or-extra items.

---

## 2026-06-20, Library Version 2026.06.54, PR #68

Three discipline + tooling improvements informed by the CI failures across PRs #65 and #67. The maintainer's post-CI assessment identified that (1) git-history-aware gates need post-commit re-audit, not just pre-push; (2) gate 40's regression test was weak (only asserted "runs clean on HEAD", didn't verify failure detection); (3) metadata bumps need automatic taxonomy/portal regeneration to avoid the cascade observed in PR #67. This entry lands all three.

---

## 2026-06-20, Library Version 2026.06.53, PR #67

Add a new audit gate (#40): **Corpus version-bump-recency audit**. Layer 2 deliverable 2b of 3 in the validation programme (Layer 1: the `validation-sweep` skill in PR #62; 2a: the D2 PR-only delta gate in PR #65; this PR: the corpus-side counterpart). The new linter uses `git log -G` pickaxe matching to compare, for each versioned document, the SHA of the most-recent commit that touched the file at all against the SHA of the most-recent commit that modified a Version metadata line. If they differ, the body has changed since the last Version bump; the gate fails.

---

## 2026-06-20, Library Version 2026.06.52, PR #66

End-of-day validation-sweep cleanup and discipline update. After eight PRs landed today (#59 through #65), the maintainer invoked the [`validation-sweep`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) skill as a follow-up. Two parallel subagent sweeps (8-PR deep review + corpus-wide stale-reference scan) surfaced three findings (one stale comment, one CHANGELOG narrative error, one pre-existing §5 categorisation gap). The maintainer responded with a discipline update for the skill: action all findings regardless of whether they were introduced today, and change the skill's focus window from "past 24 hours" to "past two calendar days" so out-of-window findings get **surfaced as questions rather than auto-deferred**. This entry closes all three findings and lands the skill update.

---

## 2026-06-20, Library Version 2026.06.51, PR #65

Add a new PR-only delta gate (**D2: Per-PR version-bump check**). Layer 2 deliverable 2 of 3 in the validation programme, shipped as a §6.1 delta gate alongside the existing D1 CHANGELOG-on-PR check. The new gate compares each markdown file modified in a PR between its merge-base and head, reading the `**Version:**` field at each, and fails if a file's body changed but its Version did not bump. Catches the per-document-version-bump-omission class of defect that the §6 monotonicity audit (gate 13) cannot detect: gate 13 confirms versions strictly increase across the corpus, but cannot tell whether a particular file should have bumped on a particular PR.

---

## 2026-06-20, Library Version 2026.06.50, PR #64

Add a new audit gate (#39): **Cross-file gate-count consistency audit**. This is Layer 2 gate 1 of 3 in the validation programme. The gate scans the corpus for prose phrases that reference an audit-programme gate count and compares the captured number against the canonical row count of the §6 inventory. Any mismatch is flagged. The gate would have caught all seven stale "37-gate" references PR #59 missed, the two PR #61 missed (caught later by PR #63), and the nine additional stale "32-gate" references this PR's own first run surfaced in rule prose and tooling docs.

---

## 2026-06-20, Library Version 2026.06.49, PR #63

Dogfood-cleanup pass: the first run of the `validation-sweep` skill (shipped in PR #62) on the post-PR-61 main state found four sibling defects that PR #61's "cleanup all stale 37-gate references" pass had missed. This entry records what the dogfood run caught, and the small cleanup PR that closes them. The finding is itself a positive signal: shipping the skill in PR #62 led directly, on its first invocation, to surfacing two High-severity references that the unaided multi-PR cleanup had not caught. The Layer 2 gate-39 candidate (cross-file gate-count consistency) would have caught both mechanically.

---

## 2026-06-20, Library Version 2026.06.48, PR #62

Add the `validation-sweep` skill to the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack: a corpus-wide regression sweep designed to run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. The skill operationalises the worked example added to `evidence-grounded-completion` in PR #60 (and corrected in PR #61) at corpus scope: combines the mechanical audit suite ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) — the canonical 38-gate full-audit invocation) with a structured semantic fan-out across parallel subagents (recent-PR deep review, corpus-wide stale-reference sweep, audit-programme integrity check), and loops until the cycle returns clean.

---

## 2026-06-20, Library Version 2026.06.47, PR #61

Cleanup pass after PR #59 and PR #60, surfaced by a recursive consistency review the maintainer requested before resuming Phase A work. Two failure shapes were found: (1) PR #60's worked example for `evidence-grounded-completion` mis-attributed the citing rule (claimed "step 4 of the verification protocol: when in doubt, re-run the verification standalone" — but step 4 is "Proactively search for contradictions", and the "when in doubt" phrasing is from the user-level Claude Code memory file's Rule 1.4 (outside this repository), not from the pack rule); (2) PR #59 added gate 38 to the §6 inventory and the four parity surfaces but missed seven downstream prose references in five files that still said "37 gates", and the spec's §5 categorisation was left without a slot for gate 38. The irony is that PR #60 shipped a worked example about exactly this multi-surface-omission failure mode and itself committed the mis-attribution variant of it.

---

## 2026-06-20, Library Version 2026.06.46, PR #60

Memorialise the multi-surface gate-parity failure mode as a worked example in the `evidence-grounded-completion` governance rule. The rule already names the abstract failure (claiming a gate suite passes from inference rather than from running it on the final state); the worked example grounds the abstraction in the concrete shape it took in practice — a session wiring a new gate into N–1 of N parallel surfaces and prepping the work for the next operator without re-running the audit, with the gate-name-parity gate catching the omission when the next session ran the full audit. The lesson generalises beyond audit gates to any work that touches parallel surfaces (mirror-sync, generator-output drift, polyglot lockfiles, cross-package version registers).

---

## 2026-06-20, Library Version 2026.06.45, PR #59

Add a new audit gate (#38) — the Section placement audit — that codifies two placement conventions a corpus-wide section-ordering survey found universally observed: orientation sections (Purpose, Scope, Overview, Applicability, Introduction, Executive Summary) must appear in the top three `##` sections, and Licence and Version-history sections must appear in the bottom three. The gate catches future drift mechanically without requiring per-doctype canonical-order codification. Library version `2026.06.44 → 2026.06.45`; audit-programme specification version `1.5.0 → 1.6.0` (minor bump: new gate added); README version `1.8.0 → 1.8.1` (patch: library-version-only bump).

---

## 2026-06-19, Library Version 2026.06.44, PR #58

Two coordinated cleanups in one PR: (1) move the root [`README.md`](README.md) "Licence and third-party reference boundary" section to the bottom of the file so it aligns with the placement convention every other README and the audit-programme survey found universal across the corpus; (2) update five places across the corpus where the external-rule-sources list still enumerated three names (TikiTribe, Wiz, Kariedo) instead of four (TikiTribe, Kariedo, addyosmani, Wiz). Library version `2026.06.43 → 2026.06.44`.

---

## 2026-06-19, Library Version 2026.06.43, PR #57

Restructure the [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) so the action-oriented content (scope, ways to use, directory structure, how to use, rule files) appears first and the historical reference content (per-version shipping log) appears near the bottom. The dense `## Pack scope` section that grew over many small additions is trimmed to the load-bearing content; the historical detail it carried (per-version shipping history, framing of the rollout's completion, enumeration of every skill that has ever shipped) is moved into a new compact `## Version history` table near the end of the README.

---

## 2026-06-19, Library Version 2026.06.42, PR #56

Tidy the [`README.md`](README.md) Mode C ("Adopt the pack only") paragraph: add a one-click link to the AI-assisted installer and remove the inline search-terms sentence that has become redundant with the GitHub repository topics and the [`CITATION.cff`](CITATION.cff) keywords shipped in PR #55. Two prose edits to the same paragraph; no structural changes.

---

## 2026-06-19, Library Version 2026.06.41, PR #55

Acknowledge the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack across the project's attribution and contribution surfaces, and enrich [`CITATION.cff`](CITATION.cff) with pack-specific search-term keywords so the pack is discoverable to readers who arrive looking for Claude Code rules or skills rather than for GRC content. Continues the reframe shipped in PR #54 by ensuring the pack is named in the attribution surfaces, not only in the positioning prose. Prose-only across five files; no structural changes.

---

## 2026-06-19, Library Version 2026.06.40, PR #54

Reframe the project's stated positioning to make explicit a dual-deliverable model that has been emerging across recent pack releases. The library is both (a) a CC BY-SA 4.0 GRC corpus and (b) a reference implementation showing how to maintain such a corpus with AI assistance, where the audit toolchain under [`tools/`](tools/) and the operational pack under [`dev-security/claude-rules/`](dev-security/claude-rules/) are the operational layer. The reframe also explicitly names a third, emergent adoption mode: the pack is usable as a standalone Claude Code baseline on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. No structural changes; prose-only across six framing surfaces.

---

## 2026-06-19, Library Version 2026.06.39, PR #53

Wrap the two remaining workflow-shaped governance rules as Claude Code Skills, closing out the post-S.3 evaluation that [`TODO.md`](TODO.md) recorded as deferred-until-trigger. Pack version `1.21.0 → 1.22.0` (minor bump, additive). The trigger condition (the next time the maintainer touched the skills pack) fired with PR #52; this PR acts on it by choosing the "Add both" outcome from the evaluation's possible outcomes.

---

## 2026-06-19, Library Version 2026.06.38, PR #52

Add a sixth governance rule to the `dev-security/claude-rules/` pack: [`governance/action-before-explanation-of-inaction.md`](dev-security/claude-rules/governance/action-before-explanation-of-inaction.md), the pack-distributable form of the user-level Rule 8 added on 2026-06-19. The discipline: never explain why an external action cannot or will not proceed without first attempting it (when the action is safe and reversible) or naming it and asking (when it is destructive). The phased governance rollout announced at pack version 1.6.0 completed at 1.11.0 with the first five rules; this entry extends the set post-rollout after a recurring AI-coding-assistant failure mode was observed in production sessions (narrating a reason to wait — "the PR is blocked because it needs a reviewer" — instead of attempting the cheap, reversible action that would have produced a real result).

---

## 2026-06-19, Library Version 2026.06.37, PR #50

Make every file under `docs/` carry the canonical 13-field metadata block, so the `docs/` tree is governed by the same audit programme as the rest of the corpus rather than carved out as a partial exemption with a per-file allowlist. Two hand-authored reference documents are promoted from informational aids to controlled artefacts; the two generator outputs ([`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) acquire metadata emitted by the generator itself. The previous mechanism, a `docs/` directory exemption in [`tools/lint-metadata.py`](tools/lint-metadata.py) with a `FORCE_INCLUDE_PATHS` carve-out for [`docs/worked-example.md`](docs/worked-example.md), is retired in favour of uniform enforcement.

---

## 2026-06-19, Library Version 2026.06.36, PR #49

Agent-production-authority controls, part C of three: operational closure. Completes the set begun in PR #47 (core control and evidence home) and PR #48 (governance integration). This part connects a harmful or unauthorised agent action to its reversal in incident response, and records the agentic standard in the cross-framework alignment matrix.

---

## 2026-06-19, Library Version 2026.06.35, PR #48

Agent-production-authority controls, part B of three: governance integration. Part A (PR #47) placed the `AGENT-PROD-01` to `AGENT-PROD-06` controls and their evidence home; this part wires the production-authority precondition into the acceptance-into-service gate, anchors it at the AI-governance framework tier, and binds the standing accountability to a named role. No new control language is introduced; each edit references the `AGENT-PROD-*` controls from part A so the gate is enforced at the formal acceptance decision, named in the framework that governs AI approval, and owned by an accountable human in the authority register.

---

## 2026-06-19, Library Version 2026.06.34, PR #47

Agent-production-authority controls, part A of the three-part set from the agentic-governance assessment: the core control, its evidence home, and the access-standard wiring. The governing principle is that autonomous agents do not receive production authority until reversibility, auditability, accountability, and permission boundaries are designed, tested, and governed; authority sits in the system boundary, the permissions model, the approval path, the immutable audit trail, the reversal mechanism, and a named accountable human, never in the agent. This closes the assessment's identified gap: the corpus treated reversibility as a classification input to an approval decision, not as a designed-and-tested precondition for production authority, and it did not consolidate the four properties into a single gate wired to acceptance-into-service.

---

## 2026-06-19, Library Version 2026.06.33, PR #46

Consistency follow-up to PR #45: broaden the summary surfaces that describe the evidence-grounded-completion rule, so they match the rule's scope after PR #45 extended it from completion claims to any state assertion. PR #45 deliberately left these surfaces untouched on the reasoning that each named the rule by its primary purpose and "remained accurate"; a subsequent read (prompted by the maintainer's "always confirm" instruction) showed that reasoning was an unverified inference that did not fully hold. Specifically, the pack's distributable governance instruction file made an explicit trigger claim ("the vocabulary of completion is a flag that the protocol must precede") that the broadened rule outgrew, and the project instruction file linked the rule only to user-level Rule 6 when a user-level Rule 7 now also exists. This PR corrects the surfaces that made trigger or linkage claims and broadens the lossy summaries for consistency.

---

## 2026-06-19, Library Version 2026.06.32, PR #45

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule from "evidence before completion claims" to "evidence before any state assertion." A session failure prompted this: during a governance assessment the assistant asserted that two templates "need new fields" and that a cross-framework matrix "needs control mappings" without having read those files; a later read confirmed the templates but showed the matrix operated at a different granularity than asserted. The existing rule did not fire because these were mid-analysis state assertions, not completion claims ("done", "fixed", "ready"). The rule's machinery (read, quote, contradiction-search, label-the-unverified) was already the right discipline; only its stated trigger was too narrow.

---

## 2026-06-19, Library Version 2026.06.31, PR #44

New audit gate (gate 37), **Claude-rules local-copy sync audit**, closing the systemic drift class the regression audit identified. The project keeps copies of a subset of the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack under `.claude/rules/` so a Claude Code session loads them as context. Both trees are exempt from the corpus linters, so until now nothing caught a local copy drifting from its pack source — the exact gap that let the evidence-grounded-completion local copy fall out of sync (fixed manually in PR #41) and would have re-opened on the next pack edit. This gate makes that drift class mechanically detectable.

---

## 2026-06-19, Library Version 2026.06.30, PR #43

Security fix: harden the gate-21 (Secret pattern audit) private-key detection regex, which had a false-negative gap. The maintainer's regression-audit review asked whether the example was RSA-specific; investigation found the detection regex itself enumerated five algorithm tokens (`RSA|DSA|EC|OPENSSH|PGP`) and consequently MISSED three real PEM private-key header forms (named here by their PEM label only, without the dash-fenced envelope, so this entry does not itself reproduce a scanner-detectable string): the bare `PRIVATE KEY` label (PKCS#8 unencrypted, the most common modern serialization and OpenSSL's default); the `ENCRYPTED PRIVATE KEY` label (PKCS#8 encrypted); and the `PGP PRIVATE KEY BLOCK` label (the real PGP header; the old regex's `PGP` branch matched a non-existent `PGP PRIVATE KEY` form and missed the actual one with the ` BLOCK` suffix). A PKCS#8 private key pasted into any corpus document would have passed gate 21 undetected.

---

## 2026-06-19, Library Version 2026.06.29, PR #42

Regression-audit fix: correct three stale gate-count references in the project instruction file [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md). All three said "32 gates" / "32-gate audit programme"; the audit programme has grown well past 32 (it was already past 32 before this session, and is 36 as of PR #37). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit found it.

---

## 2026-06-19, Library Version 2026.06.28, PR #41

Regression-audit fix: re-sync the project-local copy of the evidence-grounded-completion rule with its pack source. PR #38 added two subsections ("API polling and webhook subscriptions", "No decorative external links") to the pack source at [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) but did not propagate the change to the project-local copy at [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md). The two files are intended to be byte-identical (the local copy is the one a Claude Code session loads as session-start context; the pack copy is the distributable source). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit's `diff` of source against local copy found it.

---

## 2026-06-19, Library Version 2026.06.27, PR #40

Regression-audit fix: correct a stale gate-number reference in the docstring of [`tools/run-linter-regression.py`](tools/run-linter-regression.py). The docstring claimed "the audit programme's gate 35 invokes this script"; PR #37's gate renumber (35 → 36 gates) moved the linter regression test suite from gate 35 to gate 36, but the docstring was not updated. The docstring is a Python comment, not markdown, so no corpus gate scans it; the regression audit found it.

---

## 2026-06-19, Library Version 2026.06.26, PR #39

Regression-audit fix: correct stale gate-number and pack-version references in [`TODO.md`](TODO.md) left behind by the PR #37 gate renumber (35 → 36 gates, which shifted the Skill derives-from reference audit from gate 31 to gate 32) and the PR #38 pack bump (`1.20.0 → 1.20.1`). A full-repository regression audit found these references in the "Pack and tooling extension" section of [`TODO.md`](TODO.md); they were never updated when the underlying gate number and pack version changed.

---

## 2026-06-19, Library Version 2026.06.25, PR #38

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule with two new "Tool-specific guidance" subsections capturing two failure modes that surfaced in this session: a polling-pattern failure (raw `curl` against the unauthenticated GitHub API exhausted the 60-requests-per-hour-per-IP cap mid-session, after which every call returned HTTP 403, every iteration produced a Python `JSONDecodeError`, the loop never saw `completed`, and silent indefinite looping followed) and a URL-hallucination failure (auto-piloting from the project's file-path-link convention to a tool-name reference, inventing a plausible-looking documentation path under a real domain that did not in fact exist). Both lessons sit under §"Tool-specific guidance for AI coding assistants" next to the existing "Pipe-masked exit codes" subsection, with which they share the shape: a verification's actual outcome can be hidden by the way the verification is run.

---

## 2026-06-19, Library Version 2026.06.24

Option B from the S.4 follow-up: close the audit-coverage gap that allowed the S.2 and S.4 PRs to substantively edit governance documents without bumping the per-document `Date` metadata. New audit gate 31, **Document Date staleness audit**, compares each in-scope markdown file's `**Date:**` metadata to the file's most-recent git commit date (committer date in UTC) and fails when the metadata lags by more than `--max-lag-days` (default 1). Historical drift is grandfathered via a `--baseline-date` flag (default `2026-06-19`); the audit only enforces on commits at or after the baseline so the audit's introduction does not block CI on the 233-file pre-existing backlog identified at design time.

---

## 2026-06-19, Library Version 2026.06.23

S.4 backfill: correct per-document Date and Version metadata on five governance files that were substantively edited in the S.4 PR (library version `2026.06.21`, shipped 2026-06-19) without their per-document metadata being bumped. The omission violated the [`specification-ingestion.md`](specification-ingestion.md) contract that every substantive content change must update the document's Date to the current date and bump its Version per the disposition (patch for minor revision, minor for material revision). No existing audit gate caught the omission; the gap is acknowledged here and is closed by the follow-up audit-gate work tracked separately.

---

## 2026-06-19, Library Version 2026.06.22

S.4 follow-up: move the speculative "fourth skill" narrative out of the merged S.3 and S.4 CHANGELOG entries (where it violated Keep a Changelog's retrospective-only convention) and into [`TODO.md`](TODO.md) as a proper plan with a decision trigger, the empirical evidence to weigh at the trigger, an enumerated candidate set, and a selection criterion. The original CHANGELOG sentences pre-committed the project to a specific candidate (`change-tracking-write-entry`) without acknowledging the equally-strong alternative (`artefact-discipline-check`) or defining what "proven their format in practice" actually means; the TODO entry now records both and the criterion for choosing.

---

## 2026-06-19, Library Version 2026.06.21

Phase S.4 of the addyosmani agent-skills integration plan: add a new audit gate that enforces the derive-and-cite contract between skills and pack rules. The gate verifies that every skill document under [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/) declares a `derives_from:` YAML frontmatter field whose value resolves to an existing pack rule, closing the maintenance loop opened in S.3 (skill workflows reference canonical rules rather than duplicate them).

---

## 2026-06-19, Library Version 2026.06.20

Phase S.3 of the addyosmani agent-skills integration plan: introduce a third pack-content type, **Claude Code Skills** in the Skills workflow format (one SKILL-named file per skill), under a new `skills/` subdirectory. Three skills land in this PR, each derived from an existing governance rule with the rule remaining as the source of truth for normative content.

---

## 2026-06-19, Library Version 2026.06.19

Phase S.2 of the addyosmani agent-skills integration plan: cherry-pick the STRIDE-per-trust-boundary framing and the three-tier disposition model from the addyosmani `security-and-hardening` overlay into a new library-canonical Standard, then add surgical "See also" cross-references from two existing documents.

---

## 2026-06-19, Library Version 2026.06.18

Phase S.1 of the addyosmani agent-skills integration plan: add `addyosmani/agent-skills` as the fourth external rule source the pack vouches for, fully vet 5 of its 24 skills, copy those 5 plus the upstream MIT licence file into this project's overlay directory, and announce the fourth source through the setup-generator's offer flow.

---

## 2026-06-03, Library Version 2026.06.17

Update the main-branch-protection register to reflect the bypass-actor configuration added on 2026-06-02. Closes the silent-drift gap between the register's claim ("bypass-actor list is empty") and the live ruleset state.

---

## 2026-06-02, Library Version 2026.06.16

Phase D.1 of the follow-up plan: give five previously-exempt repo-root meta files their own canonical 13-field metadata block and bring them under the corpus metadata audit. Closes the inconsistency where [`README.md`](README.md) carried a metadata block but other adjacent repo-root files did not.

---

## 2026-06-02, Library Version 2026.06.15

Phase C.1 of the follow-up plan: document the `main` branch-protection configuration as a governance register so it can be audited from the repository rather than from a privileged settings-page view.

---

## 2026-06-02, Library Version 2026.06.14

Phase B.1 of the follow-up plan: promote the metadata-line-breaks scanner methodology developed during the rendering-cleanup PRs (#23, #24, #25) into a 34th audit gate. This catches the soft-wrap rendering bug class going forward in CI rather than relying on ad-hoc scans.

---

## 2026-06-02, Library Version 2026.06.13

Phase A.1 of the follow-up plan: fix the underlying defect in the version-monotonicity audit that caused two real problems earlier today. The audit's regex previously matched any `**Version:** x.y.z` line in a Markdown file regardless of context, including lines inside fenced code blocks. This let (a) Phase 0's bulk sed sweep match a template field in [`CONTRIBUTING.md`](CONTRIBUTING.md), and (b) the audit block the cleaner revert in PR #24.

---

## 2026-06-02, Library Version 2026.06.12

Three additional files from a tightened metadata-rendering scan that my original scanner missed. Closes the metadata-rendering cleanup with **zero** remaining flagged files corpus-wide.

---

## 2026-06-02, Library Version 2026.06.11

Third and final file from the metadata-rendering scan: [`CONTRIBUTING.md`](CONTRIBUTING.md). Backslash fix plus a Version-field placeholder change that resolves an underlying gap exposed by today's investigation.

---

## 2026-06-02, Library Version 2026.06.10

Fix metadata-rendering bug in two files where consecutive metadata lines lacked the trailing `\` line-break that this corpus uses to force hard wraps. Without it, GitHub soft-wraps the metadata block into a single paragraph, making it unreadable. A full-corpus scan found exactly three affected files; two are fixed in this PR ([`CONTRIBUTING.md`](CONTRIBUTING.md) follows in a separate PR because its metadata block is a contributor template with its own Version-field considerations).

---

## 2026-06-02, Library Version 2026.06.9

Mobile-app security work, Phase 7 of 8 (final): Capacitor / Ionic pack rule file. The mobile-app security work announced as the 8-phase plan is complete with this release.

---

## 2026-06-02, Library Version 2026.06.8

Mobile-app security work, Phase 6 of 8: .NET MAUI pack rule file.

---

## 2026-06-02, Library Version 2026.06.7

Mobile-app security work, Phase 5 of 8: Flutter pack rule file.

---

## 2026-06-02, Library Version 2026.06.6

Mobile-app security work, Phase 4 of 8: React Native pack rule file.

---

## 2026-06-02, Library Version 2026.06.5

Mobile-app security work, Phase 3 of 8: Android pack rule file.

---

## 2026-06-02, Library Version 2026.06.4

Mobile-app security work, Phase 2 of 8: first per-language pack rule file for mobile.

---

## 2026-06-02, Library Version 2026.06.3

Mobile-app security work, Phase 1 of 8: expand the mobile standard with three substantive additions that close 2024-2026 currency gaps. Per-doc version bumped `1.0.1 → 1.1.0` (minor bump per semver for added sections).

---

## 2026-06-02, Library Version 2026.06.2

Mobile-app security work, Phase 0 of 8: project-wide ratification signal. All documents previously at v0.0.1 are bumped to v1.0.1 to signal that the content is no longer "first draft" status and is ratified for downstream use.

---

## 2026-06-01, Library Version 2026.06.1

Make the project's strict-mode stance on exceptions explicit in [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md), and document the `refs/preservation/` convention for the rare case of a legitimate protected-branch force-push. Both additions close gaps identified by the new pack governance rules: three pack rules reference a project "exception register" that this project does not maintain (the absence was implicit; now it is explicit), and one pack rule names the `refs/preservation/` namespace as the audit-trail convention for force-push exceptions (the convention is now documented so it can be followed without invention).

---

## 2026-06-01, Library Version 2026.06.0

Add a mechanical version-date consistency gate; bump to `2026.06.0` per [`specification-master-project.md`](specification-master-project.md) section 4.5; record the six-phase month discontinuity inherited from prior PRs.

---

## 2026-06-01, Library Version 2026.05.144

Phase 6 (final) of the dev-security pack scope expansion: fifth and last governance rule lands; the phased rollout announced at pack version 1.6.0 is complete.

---

## 2026-06-01, Library Version 2026.05.143

Phase 5 of the dev-security pack scope expansion: fourth governance rule lands.

---

## 2026-06-01, Library Version 2026.05.142

Phase 4 of the dev-security pack scope expansion: third governance rule lands.

---

## 2026-06-01, Library Version 2026.05.141

Phase 3 of the dev-security pack scope expansion: second governance rule lands.

---

## 2026-06-01, Library Version 2026.05.140

Phase 2 of the dev-security pack scope expansion: first governance rule lands.

---

## 2026-06-01, Library Version 2026.05.139

Phase 1 of the dev-security pack scope expansion: announce broadened contract from security-only to security + development-governance discipline.

---

## 2026-06-01, Library Version 2026.05.138

CHANGELOG enforcement gate and prior-PR catch-up entry.

---

## 2026-05-31, Library Version 2026.05.137

Corpus-wide hyperlink sweep and TODO.md cleanup.

---

## Initial public release (2026-05-31, Library Version 2026.05.136): CC BY-SA 4.0

First public commit of the Governance, Risk, and Compliance Documentation Library, published under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). See [`LICENSE`](LICENSE) for the full legal code and [`NOTICE.md`](NOTICE.md) for the repository's external-reference boundary.
