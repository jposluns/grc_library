# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-19, Library Version 2026.07.538, PR #1050

Public tail of the credit-offload liveness bundle (whose scratch and `_private` halves landed separately: scratch PR #173 for the idle-liveness heartbeat plus the progress / session-start registry fields, and two `grc_library_private` direct pushes for the design-of-record and the elevated-QA-window change), plus the follow-ups the PR #1049 `/validate-pr` surfaced.

### Added
- **TODO §3.103** (widen the decision-log deferral-trigger keyword set): the [`block-unjustified-decision.py`](../../.claude/hooks/block-unjustified-decision.py) hook checks for a forbidden internal-state justification only when the added text also carries a narrow deferral keyword (`blocked` / `defer` / `wind down` / `wind-down` / `skip`), so a deferral phrased with a synonym escapes it. The item widens that set, and the mirrored `_DL_FORBIDDEN` check in the `_private` validate, to the common deferral synonyms while keeping the two in exact parity. Routed from the #1049 `/validate-pr` NOTE.

### Changed
- **TODO §3.87** (credit-offload local-VM exchange transport): added the **programmatic worker-restart** refinement (maintainer-directed 2026-07-19). Once the broker / socket control channel exists, the orchestrator can restart a wedged worker by driving it to `/clear` then `/credit-offload`, instead of the current mode-dependent restart-advice. This rests on an **asymmetric-trust rule**: the orchestrator may feed commands into a worker session, but a worker's output is always DATA the orchestrator validates, never a prompt or command it obeys, which bounds the blast radius of a confused or compromised worker.

### Fixed
- **CLAUDE.md decision-guardrail wording** (the #1049 `/validate-pr` in-window NOTE): the description of the [`block-unjustified-decision.py`](../../.claude/hooks/block-unjustified-decision.py) hook said it refuses a log write that "cites a forbidden internal-state justification" UNCONDITIONALLY, but the hook correctly scopes that check to deferral / hold entries (an internal-state word in an ACT entry is not a deferral justification). Reworded the line to describe the scoped behaviour and cross-referenced §3.103.

### Verification
- The PR #1049 `/validate-pr` (self-run refute-briefed Subagent A on squash `eb6a302d`) returned SHIP 0 error / 0 warning / 1 note; the note is fixed in-window here and its keyword-widening residual is queued as §3.103.
- `_private` change (separate direct pushes, not in this diff): the elevated-QA trust window tightened from a 2-to-3 floor to **1 clean elevated pass** per `(worker + model)` per session (maintainer-directed), reset-on-miss unchanged; and a stale cross-reference (to the public CLAUDE.md, in the `_private` credit-offload design-of-record) repointed to the orchestrator-claude operational doc.
- The full audit suite is green (all 72 gates) at push; the pre-push guard (D1-D8 plus the history-aware 45 / 40 / 31) was run standalone.

### Worker provenance
- None; orchestrator-authored. The scratch-side liveness code was unit-tested in isolation before scratch PR #173 merged.

## 2026-07-19, Library Version 2026.07.537, PR #1049

Ships the decision-guardrail self-guard (maintainer-designed 2026-07-19), against a recurring failure the maintainer named: the assistant DEFERS a queued or authorized item, or winds down / re-sequences / skips, on an un-instrumented internal-state justification (context weight, a long turn, too-risky-to-do-now, do-it-fresh-later) INSTEAD of doing the work or asking a specific question. Deferral-with-no-question is strictly worse than both valid moves: it stalls the work and hands the maintainer nothing to act on. Assistant-guidance, tooling, and working-state only; no corpus or website content changed.

### Added
- [`.claude/hooks/block-unjustified-decision.py`](../../.claude/hooks/block-unjustified-decision.py) (new PreToolUse hook on Edit and Write) and its wiring in [`.claude/settings.json`](../../.claude/settings.json). It fires only on a write to the private autonomous-decisions log and BLOCKS an added entry that lacks a `- **Classification:**` line, names a BLOCKED blocker-type outside the closed set (`maintainer-decision-unreachable` / `irreversible-needs-confirmation` / `failing-check` / `source-unavailable` / `maintainer-directed-hold`), or cites a forbidden internal-state justification. Fail-open; 9-case `--self-test` wired into the regression suite via [`tests/test_linters.py`](../../tests/test_linters.py). Proven in production: it blocked a doc-heavy first draft of the log and allowed the clean one.
- A write-before-enact autonomous-decisions log in the private companion repo (indexed in the private INDEX; a `check_autonomous_decisions_log` gate added to the private validate tool mirrors the hook as the CI floor). Every SIGNIFICANT autonomous decision (disposing of a queued or authorized item, or changing the plan, not a routine step) is written there classified BEFORE it is enacted.
### Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a new `## Decision discipline: act, ask, or name a blocker (write-before-enact)` section codifying the ACT / ASK / BLOCKED rubric, the 'attended = ask, do not defer' rule, and the write-before-enact log discipline.
### Also carries (recursion-avoidance)
The PR #1048 `/validate-pr` history row + `/retro` row, and the in-window fix from that validate-pr: the [`tools/build-public-changelog.py`](../../tools/build-public-changelog.py) module docstring updated to describe the FOUR-tier daily model (it had been left at THREE tiers after the daily-tier change).
### Verification
- `tools/run_all_audits.sh` green (72/72; regression suite includes the new hook self-test); the private validate tool green (the log passes the new check); the hook self-test is 9/9. Pre-push guard (D1-D8 + history-aware trio) green.

## 2026-07-19, Library Version 2026.07.536, PR #1048

Changes the public root CHANGELOG's current-week block to the DAILY model (TODO section 1.22.5, maintainer-directed, public-facing only). No corpus content or website changed.

### Changed
- The public root [`CHANGELOG.md`](../../CHANGELOG.md) current-week block now follows a DAILY model: the current day (2026-07-19, PRs #1039-#1048) stays per-PR verbatim; each of the six previous days still in the week condenses to ONE plain-language daily summary paragraph (`**YYYY-MM-DD (PRs #A-#B)** - ...`, a paragraph header out of the D8/gate-59 per-PR scope, like the weekly paragraphs); older weeks and months keep the existing weekly/monthly tiers. 183 per-PR root entries (2026-07-13 to 2026-07-18, #856-#1038) were condensed into the six summaries. The summaries were worker-drafted (`research-changelog-daily-summaries`), orchestrator re-verified, and applied by a deterministic script that asserts every removed per-PR entry is covered by a daily summary's PR range (no silent drop).
- The detailed mirror [`.working/changelog-details/CHANGELOG-detailed.md`](../../.working/changelog-details/CHANGELOG-detailed.md) was pruned of the same 07-13-to-07-18 entries so its oldest in-repo entry is #1039; the gate-59 mirror-parity cutoff (`max(CUTOFF_PR, oldest in-repo mirror PR)`) therefore floors to #1039 and the daily-condensed period is out of parity scope. Per the maintainer (public-facing only), the pruned detail is preserved in git history rather than swept to the private archive (no private-repo write).
- [`tools/build-public-changelog.py`](../../tools/build-public-changelog.py) gains the daily tier: `tier_of` now classifies the current day as `current` (per-PR) and each previous day in the week as `daily` (one summary paragraph), threading the `as-of` day; `project`/`plan_counts` emit and count the daily tier; the self-test covers it (3/3 green).

### Also carries (recursion-avoidance)
The PR #1047 `/validate-pr` (CLEAN) history row + record and the PR #1047 `/retro` row (the version-bookkeeping-sequencing lesson), plus the session-handoff §1.22.2 NEXT-list reconciliation.

### Verification
- `tools/run_all_audits.sh` green (72/72): gate 59 (mirror header-parity) confirms root and mirror match for the 9 PRs at/above #1039; D8 scans only those 9 per-PR entries (the daily summaries are out of scope); the scaffold-tool self-test is 3/3. Pre-push guard (D1-D8 + history-aware trio) green.

## 2026-07-19, Library Version 2026.07.535, PR #1047

Root `.directories` cleanup (TODO section 1.22.2, the maintainer's 2026-07-19 delete directive, which expanded the original README-reword scope). The three in-repo sibling placeholder stub directories are removed from the public repo root because the sibling repositories are SEPARATE repos beside this one at origin, not shipped inside it; the public root should not carry stub dirs that make them look shipped. No corpus content or website changed.

### Removed
- The three in-repo placeholder stub directories `.ref/`, `.private/`, `.scratch/` (each was a single marker-stamped README file). The real siblings (`grc_library_ref` / `grc_library_scratch` / `grc_library_private`) are separate repos; the maintainer runs them beside this clone, and an adopter opts into an in-repo stub via `/adopt` rather than receiving a shipped one.

### Changed
- [`tools/lint-sibling-placeholders.py`](../../tools/lint-sibling-placeholders.py) (gate 70) from must-exist to GUARD-IF-PRESENT-AS-STUB: an ABSENT slot is OK (no finding); a slot PRESENT and declaring itself a stub (a README file whose first line is the `<!-- SIBLING-PLACEHOLDER: <name> -->` marker) is still enforced stub-shape (exactly one README file, within 25 lines) so an adopter-created stub cannot grow into payload; a slot PRESENT but NOT a declared stub (a functional sibling checkout) is out of scope. The gate now passes trivially in the maintainer repo (all three absent) and is really a post-adoption payload-creep guard for an adopter on the in-repo stub model.
- The gate-70 regression fixture [`tests/test_linters.py`](../../tests/test_linters.py) (`SiblingPlaceholderTests`, 8 tests): the missing-dir / missing-marker / wrong-token cases flip from flagged to OK-or-skipped, a functional-dir skip case is added, and the marked-stub payload-creep and over-length cases are retained.
- The gate-70 §5 grouped-list and §6 detailed-prose in [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) reworded to guard-if-present-as-stub (Version 1.17.14).
- [`/adopt`](../../.claude/commands/adopt.md) now CREATES the in-repo stubs on request (self-contained model) instead of keeping shipped ones, and offers a functional-in-repo-sibling option; reframed across the pack skill [`dev-security/claude-rules/skills/adopt/SKILL.md`](../../dev-security/claude-rules/skills/adopt/SKILL.md) (pack `1.62.3`), the command stub, and the bootstrap planner [`tools/adopt-bootstrap-ref.py`](../../tools/adopt-bootstrap-ref.py).
- [`tools/lint_common.py`](../../tools/lint_common.py) `DEFAULT_EXEMPT_DIRS` comment + `sibling_placeholder_present` docstring (the slots are no longer always shipped, kept exempt so an adopter-materialized slot is still skipped by the content gates), [`tools/detect-env.py`](../../tools/detect-env.py) adopter messages, and the [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) adopter note all reframed. `resolve_sibling` confirmed read-only (never writes to a placeholder), satisfying the original §1.22.2 confirmation.

### Also carries (recursion-avoidance)
The PR #1046 `/validate-pr` (CLEAN, 0 findings) history row and the PR #1046 `/retro` row (which captured the maintainer's PR-splitting calibration feedback as the lesson).

### Verification
- `tools/run_all_audits.sh` green (72/72; gate 70 passes with the slots absent, the `SiblingPlaceholderTests` fixture is 8/8, and the `AdoptBootstrapRefTests` guardrail assertion was updated to the reworded message). The pre-push guard (D1-D8 + the history-aware trio) green.

## 2026-07-19, Library Version 2026.07.534, PR #1046

Lands the PR #1045 quality-assurance batch (recursion-avoidance) and two maintainer-requested backlog captures. Working-state and backlog only; no corpus or website content changed.

### Added
- TODO section 4.29 (`/adopt` adjustment + non-destructive tooling-update mode): a re-run flag letting an adopter fork change earlier `/adopt` choices and pull updated TOOLING from a newer `grc_library` origin without clobbering their edited CORPUS files, applied non-destructively and reversibly, with the portable operational instruments (the degradation-watch log, the credit-offload / session-lifecycle machinery, the QA cadences) surfaced as adopter-usable guidance or documented as maintainer-only. Maintainer-directed 2026-07-19.
- TODO section 2.24 (Governance Relationship and Flow Modelling Framework): a turnkey scoped spec for a new governance `Framework`-type document standardizing GRC entity relationships as directed `SOURCE VERB DESTINATION` flows, plus a reframing edit to the existing [`governance/framework-document-architecture-and-interrelationship.md`](../../governance/framework-document-architecture-and-interrelationship.md). Scoped from a maintainer proposal (assessed and reconciled against the existing framework doc), all six scope decisions maintainer-confirmed: layered general-method-plus-corpus-application; prose core plus one non-normative schema example; focused canonical verb set; the existing hierarchy reframed as one viewpoint; text-only in the corpus with adopter diagram guidance; the existing `Framework` type with adopter type guidance. Author later in the content tier.

### Changed
- Fixed a pre-existing stale Priority-2 backlog counter (the `Next item number` said 2.23 while section 2.23 already existed; corrected to 2.25, past the new section 2.24).
- Two PR #1045 validate-pr fixes (both gate-exempt, low severity): the detailed-mirror PR #1045 entry's `4 hook self-tests` reworded to `the new hook's --self-test passes (12 cases)` (a measured-not-inferred count-drift, 3rd occurrence of that class); and TODO section 3.80's stale `## Credit-offload mode` locus (it named the public [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) where PR #1044 had moved the section to the private orchestrator extension, group A1) repointed, with the PR #1045 `0 stale pointers remain` claim honestly softened.

### Also carries (recursion-avoidance)
The PR #1045 validate-pr history row + record file and the PR #1045 retro row (which also appends the disposition token to the PR #1044 retro row: the self-guard bundle CODIFIED PR #1044's proposed improvement).

### Verification
- Pre-push guard (`run_all_audits.sh` 72/72 + D1-D8 + the history-aware trio) green; the CHANGELOG preflight aid clean. Working-state / backlog only; no gate, corpus, or behaviour change.

## 2026-07-19, Library Version 2026.07.533, PR #1045

Ships the self-guard bundle (maintainer-directed), against the 2026-07-19 failure where the orchestrator substituted intent for action (it resubmitted a wrong-cwd command seven times, editing only the command description, and reflexively blamed session length on a short session). Assistant-guidance, tooling, and working-state only; no corpus or website content changed.

### Added
- [`.claude/hooks/block-repeated-tool-failure.py`](../../.claude/hooks/block-repeated-tool-failure.py) (new PreToolUse hook on Bash and AskUserQuestion) and [`.claude/hooks/_hook_state.py`](../../.claude/hooks/_hook_state.py) (a shared, stdlib-only, fail-open block-state helper). GUARD 1 (repeat-block loop-breaker): blocks a byte-identical resubmission (trailing whitespace aside) of a command a sibling guard just blocked, with a message to read the literal command string and change its STRUCTURE. GUARD 2 (diagnosis circuit-breaker): after two consecutive same-class blocks it requires a written mechanism-diagnosis before any retry and points at the degradation-watch log. Fail-open throughout; state is a gitignored JSONL under `.claude/hooks/.state/`. Verified: the new hook's `--self-test` passes (12 cases), an end-to-end integration test breaks the seven-times-resubmit loop at attempt 2, a structural fix (added cd) is correctly allowed, and a new [`tests/test_linters.py`](../../tests/test_linters.py) regression method wires the self-test into the suite.
- A private degradation-watch log ([`degradation-watch-log.md`](../../../grc_library_private/degradation-watch-log.md)) with an explicit THRESHOLD (a session is not long or heavy unless a few hours have elapsed AND at least one compaction), a validation discipline the orchestrator follows before ever asserting session-length or degradation, and an honest evidence seed (this session's start plus the two length-claims it made and rejected). Indexed in the private INDEX; group A12 in the private orchestrator extension carries the discipline.

### Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): new `## Self-verification: intent is not action` section (read-back before every sibling-repo or previously-blocked command; never narrate a change as made unless the artefact shows it; git status clean before a PR).
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): the lease-acquire step now appends a `session-start` row to the degradation-watch log.
- The three existing guard hooks ([`block-wrong-repo-tool.py`](../../.claude/hooks/block-wrong-repo-tool.py), [`block-verification-pipes.py`](../../.claude/hooks/block-verification-pipes.py), [`block-answered-question.py`](../../.claude/hooks/block-answered-question.py)) each record their block (wrapped so a failure never breaks the existing block); [`.claude/settings.json`](../../.claude/settings.json) wires the new hook FIRST on the Bash and AskUserQuestion matchers; `.gitignore` excludes the state dir.
- Three #1044-escape stale cross-file pointers fixed (the section-1.19.12 trim moved content to the private repo but these still pointed at the public [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md)): [`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py) (to A2), [`tools/audit-brief-freshness.py`](../../tools/audit-brief-freshness.py) (to A3), and [`TODO.md`](../../TODO.md) (to A1). A comprehensive whole-repo re-grep confirmed the touched-file pointers clean; the post-merge `/validate-pr` then found one further moved-section residual (TODO section 3.80's `## Credit-offload mode` locus, an historical APPLIED-phase line), corrected in the next PR.

### Also carries (recursion-avoidance)
PR #1044's quality-assurance batch: the validate-pr-1044 history row (OFFLOADED to worker-a under elevated QA; it found F1/F2 in the tool docstrings and MISSED F3 in TODO, which the orchestrator's whole-repo grep caught, worker-a's 2nd miss this session, still UNVALIDATED) and the #1044 retro row.

### Verification
- `tools/run_all_audits.sh` green (72/72, incl. gate 71 stdlib-only on the two new hooks); the linter regression suite passes; the new hook's `--self-test` passes (12 cases); the integration test confirms the loop-break. An independent adversarial verifier ran on the guard machinery (false-positive risk, fail-open, wiring, coherence): it returned CLEAN with one MEDIUM message-coherence finding (GUARD 1's remediation example was hardcoded to the wrong-repo class, "add a cd", but the guard fires for the pipe-guard and answered-question classes too, so a pipe-guard block could misdirect the fix), fixed in-window by branching the concrete steer on the recorded blocking-hook class (with a class-agnostic fallback) and locking it with a regression test (`test_steer_is_class_specific`).

## 2026-07-19, Library Version 2026.07.532, PR #1044

Applies TODO section 1.19.12: the CLAUDE.md sensitivity-trim. Moves the operational mechanics and war-story content out of the public [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (1699 to 1262 lines) into the private companion repo, keeping every portable governance rule public. Also carries the Sweep 114 loop-break `/validate` close-out for the session-closing handoff PR #1043. Assistant-guidance, working-state, and versions only; no corpus or website content changed.

### Added
- A new private operational extension of CLAUDE.md ([`orchestrator-claude.md`](../../../grc_library_private/orchestrator-claude.md) in the private companion repo), loaded every `/resume` on the maintainer orchestrator only. It holds the operational mechanics and orchestrator disciplines trimmed from the public file, grouped A1 through A11 by source section (credit-offload, multi-session orchestration, session close-out bookkeeping, deep-assessment and reference operational detail, operating modes, wind-down metric pointers, cross-repo safety, private-store pointers). The private INDEX indexes it and `/resume` step 2 loads and follows it as if it were part of CLAUDE.md.

### Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): trimmed 1699 to 1262 lines. The two MOVE-whole sections (the PR #441 condense note; the Credit-offload-mode section) and the SPLIT-flagged operational and war-story spans across 14 sections move to the private repo; every portable rule (the AIQT primordial rule, the PR-workflow steps, the anti-drift greps, version-bump discipline, Boundaries, the QA cadences, the QA-activity completion standard, clarify-before-acting, the security-rules index, the language/testing/date/communication conventions) stays public. Per the maintainer-confirmed classification (32 sections, 2 MOVE / 17 KEEP / 13 SPLIT). One dangling reference fixed (the QA-completion "consume discipline" pointer made self-contained), plus two verifier-flagged cosmetics (an orphaned RM-10 label, a stray whitespace line).
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): step 2 now loads the private [`orchestrator-claude.md`](../../../grc_library_private/orchestrator-claude.md) as the operational extension (maintainer only; adopters have no private repo and skip it).
- The private removal ledger ([`claude-md-considerations.md`](../../../grc_library_private/claude-md-considerations.md)) gains the section 1.19.12 archive block (33 entries, verbatim war-stories plus restore-signals, for the restore-watch cadence); the private INDEX indexes the new auto-loaded extension.
- [`TODO.md`](../../TODO.md): section 1.19.12 closed and rotated to [`DONE.md`](../DONE.md) (only the maintainer-gated section 1.19.13 remains in the 1.19 series); the F1 rotation-debris line (section 1.22.6) deleted; three section-1.19.12 cross-references updated.

### Discipline and method
The apply was worker-drafted (worker-20260716-a produced a deterministic line-range apply script, the candidate files, and a re-parse proof) and orchestrator-AUDITED: the script was run on live source and cross-checked against the worker candidate (differing only at the one redacted watermark line), every removed rule-language line was adjudicated as a legitimate move (not a dropped rule), the extension's LOAD content was confirmed byte-verbatim against the removed spans, and the trim was independently verified by an in-session full-access adversarial verifier (CONFIRMED-CLEAN) plus an offloaded worker-b public-side QA.

### Also carries (the Sweep 114 loop-break close-out for PR #1043)
The Sweep 114 corpus-wide `/validate` over the #1040..#1043 deltas (offloaded to worker-20260716-b, consumed under elevated QA): PASS, one in-window warning F1 (TODO section 1.22.6 rotation debris, fixed here) plus three informational notes; all #1040 to #1042 asserted-clean surfaces corroborated, 0 contradicted. Recorded in [`validate-sweeps/history.md`](../validate-sweeps/history.md) (Sweep 114). This PR also prunes the session handoff (keep current plus one prior) and acquires the concurrency lease.

**Worker provenance:** [`inbox/worker-20260716-a/apply-119-12-trim/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260716-a/apply-119-12-trim/MANIFEST.md) (the apply-draft delivery this PR applied).

### Verification
- `tools/run_all_audits.sh` green (72/72) on the trimmed CLAUDE.md; the private repo [`tools/validate.py`](../../../grc_library_private/tools/validate.py) green (no secrets or PII, house-style clean, all internal links resolve, INDEX covers every operational doc). Two independent adversarial verifiers on the trim (in-session full-access, CONFIRMED-CLEAN; plus the offloaded worker-b public-side QA).

## 2026-07-19, Library Version 2026.07.531, PR #1043

Session-closing handoff for the 2026-07-19 resumed session (an EARLY wind-down on a named-degradation signal, converted to a proper session-closing handoff, per the discipline this PR codifies). Assistant-guidance, working-state, and versions only; no corpus or website content changed.

### Added / Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (`## No idle-stop in unattended mode` area): codifies the **degradation-auto-handoff discipline**, on a genuine named-degradation trigger in UNATTENDED mode, WIND DOWN PROPERLY (execute a session-closing handoff: green merge + full handoff refresh + lease release), do NOT "pause" mid-turn. The wind-down framework's surface-via-AskUserQuestion path is the ATTENDED path (and is blocked in unattended mode), so the unattended path on a degradation trigger is the automatic session-closing handoff. Also polished a comma-splice in the §1.15a wrong-repo-hook note (a validate-pr-1042 non-finding).
- [`TODO.md`](../../TODO.md): added §3.102 (pack-distribute the degradation-auto-handoff discipline into the `session-lifecycle` pack rule, both trees).
- [`session-handoff.md`](../session-handoff.md): refreshed for session close, the CLOSING block + NEXT SESSION queue (apply the 5 delivered research seeds first), the State-snapshot (green-at #1043), and this session's Asserted-expectations block.
- [`session-state.md`](../session-state.md): RELEASED the concurrency lease (Status released, Active-session none, Operating-mode attended-autonomous for the next session); worker-a recorded UNVALIDATED (validate-pr-1041 miss).

### Also carries (recursion-avoidance)
PR #1042's QA batch: the `/validate-pr` row (SELF-RUN formal Subagent A, CLEAN 0/0/0) and the `/retro` row.

### Wind-down record (honest)
The trigger was a density of SELF-CAUGHT slips in one enormous un-reset marathon turn (a `git reset --hard origin/main` on a feature branch, the scratch-sync reflex misapplied; and 5 command-composition slips where the newly-built wrong-repo hook correctly blocked bare sibling-tool invocations that relied on a persisted cwd) plus this conversation's extreme length, NOT diffuse degradation, the slips were specific and fixable (lessons in the #1042 retro: always explicit-`cd` for sibling tools; never `reset --hard` a feature branch; edit the command string not just its description). The maintainer flagged (a) that hitting issues should have triggered a proper wind-down not a mid-turn pause (fixed by the codification above) and (b) that 3 PRs is atypically early for degradation (correct, the real residual was un-reset context length, so a fresh `/resume` is the clean insurance).

### Loop-break note
Per the session-closing-handoff exception this PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next session's corpus-wide `/validate` over the #1040..#1043 deltas, cross-checked against the Asserted-expectations block.

### Verification
- `tools/run_all_audits.sh` + the pre-push guard green (72/72 + D-series).

## 2026-07-19, Library Version 2026.07.530, PR #1042

Adds the wrong-repo tool guardrail (TODO §1.22.1, maintainer-directed 2026-07-19) after the orchestrator ran the scratch-side credit-offload-queue helper from the `grc_library` cwd (a silent file-not-found from the wrong repo). Tooling, assistant-guidance, and working-state only; no corpus or website content changed.

### Added
- [`.claude/hooks/block-wrong-repo-tool.py`](../../.claude/hooks/block-wrong-repo-tool.py): a PreToolUse Bash hook that inspects the command, and for each `tools/<name>.(py|sh)` invoked at command position that is ABSENT in the project repo's tools dir but PRESENT in a sibling repo's, BLOCKS (exit 2) naming the correct repo. Allows any command containing an explicit `cd` (the author is managing cwd deliberately), a tool that exists locally, a tool absent everywhere (new-tool creation), and a filename mentioned only as an argument. Fail-open, adopter-safe (no-op if no sibling tools dirs). 8 inline self-tests, all pass.

### Changed
- [`.claude/settings.json`](../../.claude/settings.json): wired the hook as a second Bash PreToolUse hook (alongside the pipe-guard).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): added the read-side-companion note to the §1.15a cross-repo Boundaries bullet (run scratch / `_ref` / `_private` tools with an explicit `cd` prefix, which the hook allows).
- [`TODO.md`](../../TODO.md): rotated §1.22.1 out (closed here, into DONE); refined §3.87 (the unix-socket transport) with the maintainer-directed 2026-07-19 assessment (worth building; the turn-based-session -> broker-daemon constraint; single `orchestrator.sock` client-server vs per-instance sockets; scratch reduced-not-eliminated for cross-VM + audit; shared read-only SHA-pinned worktrees vs an unsafe shared live repo; a phased build).

### Also carries (recursion-avoidance)
PR #1041's `/retro` row (in [`improvement-log.md`](../improvement-log.md)). PR #1041's `/validate-pr` row is OFFLOADED to worker-a (order `validate-pr-1041`, pinned to #1041's merge SHA) and is consumed into this PR at push time under elevated QA (worker-a's first QA delivery this session).

### Discipline observation (self-inflicted, self-caught, no escape)
While mid-build I ran `git fetch && git reset --hard origin/main` on this FEATURE BRANCH, applying the scratch-checkout-sync reflex (correct for the wipeable scratch checkout) to a feature branch with uncommitted work, which reverted the settings.json wiring (the untracked hook file survived; no commits were lost since the branch had none). Recovered by re-adding the wiring and committing the core immediately. Lesson: the `git reset --hard origin/main` sync pattern is ONLY for the scratch checkout; NEVER run it on a `grc_library` feature branch (it discards uncommitted work). This is the exact cross-context-command hazard the §1.15a / §1.22.1 guardrails address, ironically hit while building §1.22.1; recorded for the retro.

### Verification
- Hook `--self-test`: 8/8 pass. End-to-end: the exact slip (running the scratch-side credit-offload-queue helper from the `grc_library` cwd) BLOCKS naming the `grc_library_scratch` sibling; a local tool and a `cd`-prefixed command ALLOW. The hook fired correctly in production on a real scratch-tool invocation during this session.
- `tools/run_all_audits.sh` + the pre-push guard green; the settings file parses as valid JSON.

## 2026-07-19, Library Version 2026.07.529, PR #1041

Adds the answered-question guardrail (TODO section 1.22.6, maintainer-directed 2026-07-19) after the assistant re-asked the maintainer four content forks (section 3.68 vuln-SLA, section 3.69 MFA scope, section 3.70 asymmetric-key minimums, the standards-rendering item) whose decisions were already recorded in the pending-decisions queue. Assistant-guidance, tooling, and working-state only; no corpus or website content changed.

### Added
- [`.claude/hooks/block-answered-question.py`](../../.claude/hooks/block-answered-question.py): a PreToolUse hook on `AskUserQuestion` that extracts a question's distinctive keys (section numbers written with the section glyph or the word "section", and coded backlog ids like `FR-205`), greps the decision stores (the pending-decisions queue, the private design-decisions record, and the DONE ledger), and BLOCKS (exit 2) the question when a key already appears, printing the matched store line. Fail-open on parse/read failure or absent stores (adopter-safe). 12 inline self-tests (`--self-test`), all pass.
- [`tools/decisions-search.py`](../../tools/decisions-search.py): the on-demand forcing-function search (a section number, a coded id, or a free-text phrase); the same executed-not-narrated pattern as the audit-delivery-status and ref-holds tools. Stdlib-only.

### Changed
- [`.claude/settings.json`](../../.claude/settings.json): wired the new hook as a second `AskUserQuestion` PreToolUse hook (alongside the unattended guard).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): added a "Search decisions before asking (the answered-question guardrail)" clause to the clarify-before-acting section.
- [`TODO.md`](../../TODO.md): added section 1.22.6 (this guardrail, closed here and rotated to DONE) and section 1.22.7 (the maintainer-directed single "Maintainer or Egress Gated" no-priority section with numbered items, for overnight); section 1.22.7 revised per the maintainer's mid-build clarification (one combined section, each item numbered so the maintainer can reference "I did item N").
- [`.working/pending-decisions.md`](../pending-decisions.md): recorded this session's Round-1 confirmations (section 1.14 confirmed-as-shipped, section 1.1 design-overnight, section 1.18 scope+D8-pilot-overnight) and noted the four content forks are already-recorded and confirmed for overnight execution.
- [`.working/DONE.md`](../DONE.md): rotated section 1.22.6 in.

### Verification
- Hook `--self-test`: 12/12 pass (2 added by the verifier fix). End-to-end: a `§3.69` question BLOCKS (exit 2, prints the recorded MFA decision); a novel key-free question ALLOWS (exit 0); a novel `SEF-07` control-code question ALLOWS (exit 0, the over-block fix); `FR-205` still BLOCKS (exit 2). `decisions-search.py 3.69` returns the recorded decision lines (exit 0); `3.999` returns none (exit 1).
- **Skeptical verifier (substantive/protective machinery) run pre-push: no push-blocking defect, but it surfaced a real over-block class, FIXED here.** The coded-id regex was `[A-Z]{1,4}-\d+`, which matched corpus control codes (`SEF-07`, `IAM-09`) and hyphen-numeric statute codes (`A-2.1`), so a genuinely novel security/privacy question mentioning one would be false-blocked. Tightened to the known backlog-id prefixes (`FR`/`SR`/`GR`/`DD`/`RB`/`FIT`/`FQ`/`GAP`/`P`); section-number detection covers the rest. Also documented the verifier's second residual (the live `AskUserQuestion` payload schema is unverified from here; if it nests questions differently the hook fail-opens to a no-op, so the CLAUDE.md discipline and the on-demand decisions-search tool are the load-bearing control and the hook is defence-in-depth).
- `tools/run_all_audits.sh` and the pre-push guard green (the first guard run correctly FAILED on the gate-50 finding below, which this PR then fixed); the settings file parses as valid JSON.

### Also carries (recursion-avoidance)
PR #1040's QA batch: the `/validate-pr` row (SELF-RUN formal Subagent A on the #1040 working-state diff) and the `/retro` row. **F1** from validate-pr-1040 (LOW-MED): #1040 added top-level P1 §1.22 but left the P1 "Next item number" counter at `1.22` (`TODO.md:27`); per the never-recycle convention the next P1 section would collide. Re-verified at source and FIXED here (counter -> `1.23`). The gate-50 pre-push guard independently caught the missing #1040 QA rows before push, which this batch supplies.

## 2026-07-19, Library Version 2026.07.528, PR #1040

Resume close-out for the 2026-07-19 session (`/resume` from the session-closing handoff #1039; on the VM, gh-CLI, no GitHub MCP; STARTS attended-autonomous). Working-state and versions only; no corpus or website content changed.

### Changed
- [`session-handoff.md`](../session-handoff.md): recorded the Sweep 113 result in the Resume-cursor "Last validation sweep" line; added a current-session Next-actions block (the maintainer-directed privatization/guardrail-tightening block that outranks the queue) and a current-session State-snapshot block (live versions for the D7 gate); PRUNED per keep-current-plus-1-prior (deleted the four 2026-07-17 #992-#999 session blocks: the CLOSING + NEXT-SESSION Next-actions pair, the State-snapshot, and the Asserted-expectations sub-block); kept the #1021-#1039 and #1000-#1020 stacks.
- [`session-state.md`](../session-state.md): ACQUIRED the concurrency lease (Active-session `claude/resume-sweep113-closeout`, Status active, fresh heartbeat); refreshed Current-task and Worker-dispatches for the fresh session (both workers Opus 4.8; worker-b at 1 clean elevated pass this session via Sweep 113; worker-a unvalidated this session).
- [`validate-sweeps/history.md`](../validate-sweeps/history.md): prepended the Sweep 113 row (Version 2.0.113 to 2.0.114).
- [`TODO.md`](../../TODO.md): added section 1.22 (the this-session privatization/guardrail block: the guardrail hook, the placeholder-README fix, the `.working` cycle-out mechanism, the cross-repo reference-existence advisory tool, the daily-tier changelog refinement). Recorded `.project-governance/` = KEEP (maintainer-confirmed after reviewing the design + gate-53-retirement cost).

### Verification
- Sweep 113 (loop-break `/validate` over #1021..#1039, offloaded to worker-b, pinned to #1039 `130540cc`) consumed under ELEVATED QA: proof-of-run genuine, mechanical facts independently re-derived (72/72, four-surface parity 312/310/269/39, counts 13/24/15/18, versions EXACT-MATCH), the two changed citation families independently re-greped clean, and a dedicated delivery-1 false-negative auditor returned CLEAN in-delta. 0/0/0/0; all #1021-#1038 asserted-clean surfaces corroborated, 0 contradicted. Loop-break control for #1039 PASSES.
- `tools/run_all_audits.sh` 72/72; pre-push guard green.

### Loop-break note
Per the resume protocol this is the first PR of the resumed session; it is NOT the session-closing handoff, so it takes its own per-PR QA at the next boundary via recursion-avoidance. It carries no prior-PR QA batch because #1039 (the prior session's closing handoff) was itself loop-break-exempt and its compensating control (Sweep 113) is recorded here.

## 2026-07-19, Library Version 2026.07.527, PR #1039

Session-closing handoff for the 2026-07-18b resumed session (merged #1021-#1038: the section 1.19.8/9/10 operational-state privatization Phase 2/3, plus the maintainer-alert watchdog SOP #1038). Refreshes [`session-handoff.md`](../session-handoff.md) with this session's Next-actions, State-snapshot, and Asserted-expectations blocks; refreshes the private-repo session-metrics row; releases the concurrency lease ([`session-state.md`](../session-state.md), Status released, Active-session none). Batches PR #1038's quality-assurance (validate-pr worker-b + retro). **Also fixes F1** (caught by validate-pr-1038's §1.19.x-extra-care review, MEDIUM sop-consistency, re-verified at source): [`.claude/commands/resume.md`](../../.claude/commands/resume.md) step 3 still directed the orchestrator to CLEAR assessed alerts autonomously, contradicting the maintainer-decides-clearing CLAUDE.md bullet and the scratch protocol (an inconsistency introduced when the SOP was refined and resume.md was not re-reconciled); reworded to "inform the maintainer and ask via a choices-question whether to clear, clearing only if the maintainer directs; overnight = fix-safe + record, no clear". The worker logged F1 to the scratch maintainer-alert channel out-of-band (the watchdog working as designed). Per the loop-break this PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next session's corpus-wide Sweep 113 `/validate` (pre-positioned over the #1021..#1038 deltas, pinned to this merge SHA). Assistant-guidance, working-state, and versions only; no corpus or website content changed.
