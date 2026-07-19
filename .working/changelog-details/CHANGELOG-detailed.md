# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

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

## 2026-07-18, Library Version 2026.07.526, PR #1038

Wires the maintainer-alert watchdog channel into the orchestrator's operating discipline (maintainer-directed 2026-07-18). Assistant-guidance and working-state only; no corpus or website content changed.

### Added
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Credit-offload mode`: a "Maintainer-alert watchdog channel" bullet codifying the SOP. The maintainer-alert channel file (a scratch-repo out-of-band alert channel credit-offload workers append to, watched by the maintainer directly) is read at every task boundary. Attended mode: an open alert is PRIORITY (assess, fix what the orchestrator can, then at the next maintainer prompt inform plus ask via a choices-question whether to clear, the maintainer deciding). Overnight mode: fix what is safely fixable plus record for morning, no blocking prompt, no autonomous clear.

### Changed
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md) step 3: the credit-offload coordination-plane read now also reads the maintainer-alert channel file and runs the maintainer-alert process (resume is a task boundary).
- Cross-repo (pushed separately): the design-of-record mirror in the private companion repo (the credit-offload design-of-record, section "Maintainer alert channel (watchdog)", Version 1.3.3 to 1.3.5) and the scratch-side convention (the scratch maintainer-alert channel file's "How to read" section plus the scratch queue protocol readme) were updated to the same SOP; a stale scratch pointer to the old public working-state design-of-record path was corrected to the private-repo home. The three 2026-07-18 watchdog alerts (A, B, C) were assessed, advised to the maintainer, and cleared on maintainer authorization.

### Verification
- `tools/run_all_audits.sh` 72/72; pre-push guard green. Multi-surface consistency self-checked: CLAUDE.md, the resume command, the private-repo mirror, and the scratch convention describe the same SOP; no em-dashes or en-dashes; the private-repo reference is bare-name so gate 70 (sibling-repo stub-guard) stays clean.

### Also carries (recursion-avoidance)
PR #1037's QA batch: the validate-pr row (worker-b, offloaded) and the retro row.

## 2026-07-18, Library Version 2026.07.525, PR #1037

Section 1.19.10 slice 2: the one-time tiered public-changelog migration, and the close of TODO section 1.19.10. The public root now keeps only a recency-tiered projection; the full per-PR record moves to the private companion repo as its durable source. Working-state and versions; no corpus or website content changed.

### Changed
- [`CHANGELOG.md`](../../CHANGELOG.md): migrated from the full per-PR list (1020 compact entries) to the tiered public form (the maintainer-approved model locked at the #1020 handoff, generated by [`tools/build-public-changelog.py`](../../tools/build-public-changelog.py)). The current ISO week (2026-07-13 to 2026-07-18, 181 entries plus this PR's entry) is kept per-PR VERBATIM. Each of the six older completed weeks (weeks of 2026-07-06, 2026-06-29, 2026-06-22, 2026-06-15, 2026-06-01, and 2026-05-25) is collapsed to ONE authored accomplishments paragraph of at most four sentences, headed `**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**` (the two oldest, pre-PR-number weeks are headed by version range). No week older than three months exists yet, so there are zero monthly-tier paragraphs.

### Added
- In the private companion repo (grc_library_private, cross-repo, pushed separately): a full-per-PR-source file under its archive tree, a verbatim snapshot of the full 1020-entry per-PR root at the migration, carrying a provenance header. This is the durable full per-PR source the tiered public root derives from, so no per-PR detail is lost when the public root is tiered or when section 1.19.13 later scrubs public git history. It sits under the archive tree, which the private repo's validate gate secret-exempts (swept public content).

### Verification
- Conservation (data-safe): the current-week block (header plus 181 entries) in the new root is BYTE-IDENTICAL to the live root's lines 1 to 366 (`diff` clean); zero older per-PR entry lines leaked into the current block; the six weekly headers are present with correct PR or version ranges; zero `TIER-SCAFFOLD` comments and zero raw bullet lines remain; zero em-dashes or en-dashes. The private-repo source snapshot's body is byte-identical to the pre-migration public root (1020 entries).
- Provenance (research-assistant discipline): the six weekly accomplishment paragraphs were re-authored by the orchestrator, NOT pasted. Worker-20260716-b (Opus 4.8, routine) produced a research-seed DRAFT of the six summaries from the projection tool's raw per-PR bullets (order `research-changelog-weekly-summaries`); the orchestrator then read all 839 older-week bullets across the six weeks itself, verified every named document, annex, correction, and count against the source bullets, and authored the final prose (for example substituting the measured-safe "dozens" for the draft's un-tallied "roughly forty" renumbered documents).
- Pre-push guard green; skeptical pre-push verifier (substantive/destructive tier).

### Also carries (recursion-avoidance)
PR #1036's QA batch: the validate-pr row (worker-a, routine, SHIP, 1 informational note, plus the migration-integrity report confirming no corpus corruption post-`_private`-migration) and the retro row.

## 2026-07-18, Library Version 2026.07.524, PR #1036

Section 1.19.10 slice 1b: a data-integrity fix to the slice-1 projection tool, prerequisite for the slice-2 migration. Tooling only; no corpus or website content changed.

### Fixed
- [`tools/build-public-changelog.py`](../../tools/build-public-changelog.py): the slice-1 `ENTRY_RE` required a `| PR #N` segment, so the oldest 34 root entries (2026-05-31 to 2026-06-19, the pre-PR-number era, form `**YYYY-MM-DD | VERSION** - summary`) were silently DROPPED from the projection. The `| PR #N` segment is now optional (`group(3)` is None for a no-PR entry); a no-PR entry buckets by date like any other, its scaffold bullet is version-tagged (`- vVERSION: ...`), and an all-no-PR week's header carries a version range (`(versions X to Y)`) instead of a PR range. Conservation now holds over ALL entries: the live root's 1019 entries project to 180 current + 839 weekly bullets = 1019, zero dropped (was 985 projected + 34 dropped). Self-test gains a no-PR case (parse, tiering, version-range header, version-tagged bullet, and a 6-in / 6-out conservation assertion).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 72/72; the tool's `--self-test` 3/3; the tool is still non-destructive (not run on the real root; the migration is slice 2). Stdlib-only (gate 71).
- Pre-push skeptical verifier (refute-briefed, read-only shared tree): CONFIRMED-CORRECT on all six axes. Regex parses both forms and is adversarially safe (the `[^|]` version class means the PR number stays bound to the header even when a summary contains a literal `PR #` or a pipe); the old-vs-new parity check found the broadening is a strict superset (all 985 with-PR lines parse byte-identically, 0 old-only drops); full conservation on the real root is 1019 = 180 current + 839 bullets (805 PR-tagged + 34 version-tagged), each entry in exactly one tier, 0 drop / 0 dup.

### Discipline observation
The slice-1 verifier returned CONFIRMED-CORRECT but MISSED this drop because it defined its conservation universe as PR#-bearing lines only (984 = 179 + 805, true for that subclass but blind to the 34 no-PR entries). A conservation / no-loss check is only as complete as its universe definition; the true universe was all 1019 entries. The defect surfaced from EXAMINING the scaffold's actual weekly buckets before running the destructive slice-2 migration (the oldest bucket was week 06-15 / #38, with nothing for 05-31 to 06-14). Reinforces: define a conservation check's universe as the full entry set, not a regex-matched subclass; and examine a generated artefact's real output before a destructive migration consumes it.

### Also carries (recursion-avoidance)
PR #1035's QA batch: the validate-pr row and the retro row.

## 2026-07-18, Library Version 2026.07.523, PR #1035

Section 1.19.10 slice 1 (non-destructive machinery): the tiered public-CHANGELOG projection scaffold tool. Tooling only; no corpus or website content changed.

### Added
- [`tools/build-public-changelog.py`](../../tools/build-public-changelog.py): projects the root CHANGELOG's per-PR compact entries into the locked tiered public form (TODO §1.19.10). Current ISO week kept per-PR verbatim; older weeks within 3 months collapse to a weekly paragraph header (`**Week of YYYY-MM-DD (PRs #N-#M)**`); older than 3 months to a monthly paragraph (`**YYYY-MM (PRs #N-#M)**`). It is a SCAFFOLD generator: a week holds dozens of PRs and an at-most-4-sentence accomplishments paragraph is an AUTHORED condensation, so the tool emits the tier structure plus a placeholder carrying the PR range and the raw per-PR summaries as material for the slice-2 migration to author. Not a CI `--check` gate (the per-PR source moves to the private repo under §1.19.10; no public gate may reach a private sibling). `--dry-run` / `--emit` / `--self-test` (3 cases). Stdlib-only (gate 71).

### Changed
- [`tools/check-changelog-length-on-pr.py`](../../tools/check-changelog-length-on-pr.py): a docstring note recording the tiered-model D8 interaction (see Discipline observation).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 72/72; the tool's `--self-test` 3/3 and `--dry-run` rc 0; [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) clean. The tool is advisory (not run on the real root in this PR; not wired into any gate).
- Pre-push skeptical verifier (refute-briefed, read-only shared tree): CONFIRMED-CORRECT on all seven axes. Notably: the projection partitions the live root's 984 entries into 179 current + 805 weekly-bullet + 0 monthly with ZERO loss or duplication (each entry in exactly one tier); the ISO-week boundaries are correct and no week is split across the 3-month line; and the root has 0 legacy non-compact entries, so the slice-2 migration will drop nothing.

### Discipline observation
The locked #1020 design said §1.19.10 "reshapes D8", but on inspection D8's `ENTRY_RE` matches ONLY the per-PR compact header, so the weekly (`**Week of ...**`) and monthly (`**YYYY-MM ...**`) paragraph headers are ALREADY out of D8's scope with no change; only the current-week per-PR tier is length-gated, which is the intended behaviour. Documented in the D8 tool rather than changing it. This is the source-verify-the-spec-mechanics discipline (a co-designed spec can name a change that turns out unnecessary once the target is read).

## 2026-07-18, Library Version 2026.07.522, PR #1034

Section 1.19.9 PR B2: runs the dated-archive migration (aged working-records to grc_library_private), the current-week window, maintainer-approved. **Closes TODO §1.19.9.** Working-state only; no corpus or website content changed.

### Changed
- Ran the generalized sweep tool ([`tools/sweep-working-records-to-private.py`](../../tools/sweep-working-records-to-private.py)) emit-verify-prune. Moved to the grc_library_private archive (committed + pushed there, its validate gate clean) and pruned from grc_library: **189** completed-week detailed-CHANGELOG entries, **53** dated per-run QA record files, and **1,217** aged roll-up rows (659 from the validate-pr history, 558 from the improvement-log) older than the current ISO week. In-repo now: mirror 178 entries, validate-pr 177 rows, improvement-log 165 rows (the current week). 29 now-absent history.md Detail-column links delinked.
- The private archive received an archive subtree (changelog-details weekly files, records, per-register roll-up-row weekly files); the private repo's validate gate exempts that archive subtree from its secret pre-screen (swept grc_library working-state QA content that grc_library itself secret-exempts), and its INDEX gained an archive note. That is a grc_library_private-side change (pushed separately).

### Verification
- Data-safety, run in order: the archive was emitted, committed, pushed to grc_library_private, and its validate gate ran clean BEFORE the prune; the prune verified every archived artefact present and every rewrite passed its re-parse assertion (the mirror and both registers: kept == original minus swept, zero residual sweepable), all assertions before any write. Everything also remains in grc_library git history.
- Post-prune [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) **72/72**: gate 50's PR-A per-register dynamic floor and gate 59's mirror cutoff scope the swept rows and entries out of scope (not missing), exactly as the guard-first PR A + PR B1 prepared.
- A dedicated data-loss-focused pre-push verifier did a row-by-row set reconciliation (multiset difference on full-line fingerprints) and returned **CONFIRMED-CORRECT on all seven axes**: every pre-prune row and entry is either kept in-repo (current week) or in exactly one archive file (older), NONE lost or duplicated; all 53 record files byte-identical in the archive; all 29 delinks correct; the diff is working-state-only.

### Also carries (recursion-avoidance)
PR #1033's QA batch: the validate-pr row (offloaded to worker-b, consumed under elevated QA, CLEAN, graduating worker-b to routine) and the retro row.

## 2026-07-18, Library Version 2026.07.521, PR #1033

Section 1.19.9 PR B1 (tool-only; the destructive initial migration RUN is PR B2): generalizes the working-records sweep tool so the dated-archive sweep can move aged roll-up rows to the private companion repo. Tooling and working-state only; no corpus or website content changed.

### Changed
- Renamed [`tools/sweep-working-records-to-private.py`](../../tools/sweep-working-records-to-private.py) (from the -to-scratch name) and repointed its destination convention from the scratch exchange repo to the private companion repo, matching where section 1.19.8 relocated the operational state.
- Added an aged roll-up-ROW sweep for the two gate-50 registers (the validate-pr history and the improvement-log): a new `partition_rollup_rows` keeps the current ISO week's dated rows in-repo and sweeps older rows to the private archive, so gate 50's PR-A dynamic per-register floor scopes a swept-out PR out of scope rather than flagging it missing. The other history registers keep their rows in-repo (guardrail-reviews for the gate-60 newest-row safety; the rest have no dynamic cutoff prepared); their dated per-run files still sweep as before.
- Data-safety strengthened for rows: `--emit-archive` writes per-register weekly roll-up-row archive files; `--prune` verifies every archived week-file is present and runs a per-register re-parse assertion (kept row count equals original minus swept, and the kept text re-partitions to zero further sweepable rows) alongside the existing mirror assertion, with ALL assertions before any write so a mismatch aborts with nothing changed.
- Docstring rewritten; `--self-test` added (3 roll-up-row cases). References repointed in the backlog, the changelog-mirror-parity gate docstring, the change-tracking overlay, CLAUDE.md, and two working-state READMEs (a bare-token scratch-to-private pass fixed the destination-name tokens the tool-name repoint first missed); frozen audit-trail records keep the old tool name.

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 72/72; the sweep tool `--self-test` 3/3 and `--dry-run` rc 0; [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) clean. The tool is advisory (not wired into any gate).
- Pre-push skeptical verifier (refute-briefed, read-only shared tree): the row-sweep machinery is CONFIRMED-CORRECT on every data-loss / corruption axis (the line-level partition preserves headers, separators, prose, and recent rows; each row is a single physical line; the re-parse assertions reconstruct the kept set; emit-verify-prune runs all assertions before any write). It also surfaced the two normal close-out gaps (the #1032 validate-pr row and this #1033 detailed entry, both now present) and the scratch-to-private prose-staleness in the changed READMEs and docstring (fixed).

### Also carries (recursion-avoidance)
PR #1032's QA batch: the validate-pr row (offloaded to worker-a, consumed under routine QA, CLEAN) and the retro row.

## 2026-07-18, Library Version 2026.07.520, PR #1032

Section 1.19.9 PR A (guard-first): the bookkeeping-parity gate (gate 50) Check 1 gains a dynamic per-register floor, so the upcoming dated-archive sweep (PR B) can move AGED roll-up rows out of the in-repo history registers to the private companion repo without Check 1 flagging the swept PRs as missing their validate-pr / retro rows. Tooling and working-state only; no corpus or website content changed.

### Changed
- [`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py): new `effective_floor(present_prs, floor=INCEPTION)` helper returning `max(floor, min(present_prs))` (empty-guarded), mirroring gate 59's `effective_cutoff`. Check 1 (`qa_cadence_findings`) now computes a per-register floor for the validate-pr-history and improvement-log registers independently and skips a PR below its register's floor: a row swept to the private repo drops below the floor and is out of scope, not flagged missing. The two registers sweep independently, so each gets its own floor (a single combined floor would keep the higher-floored register in scope below its own oldest row and re-introduce false missing-row findings). The root CHANGELOG (Check 1's universe set) keeps every PR, so the asymmetry is exactly gate 59's. Docstring updated (the Check-1 window bound and a new exemption bullet).
- [`TODO.md`](../../TODO.md): section 1.19.9 annotated with the two-PR split and the source-verified gate-grouping correction (only gate 50 needs the floor; gate 60 reads the newest guardrail-review row only, so its obligation is sweep-safety not a cutoff; D5 reads only the current PR diff, so it needs no change; the spec's "50, 60, D5" list was inexact).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 72/72 (behaviour unchanged: with the live registers both floors equal INCEPTION 329, since validate-pr rows begin #183 and retro rows #213); [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) clean.
- Two regression tests added in [`tests/test_linters.py`](../../tests/test_linters.py) (`BookkeepingParityTests`, 29/29): a swept-below-floor PR is out of scope, and a genuine miss above the floor still flags.
- Pre-push skeptical verifier (refute-briefed, read-only shared tree) probed over-suppression, under-suppression, the empty-register edge, the exemption interactions, the floor source, and the behaviour-unchanged claim: CONFIRMED-CORRECT on every point, no defect. The one honest limitation (a genuine QA-cadence miss strictly below the register floor becomes invisible AFTER the sweep) is the accepted gate-59-parallel design trade, dormant until PR B, and does not weaken any check pre-sweep.

## 2026-07-18, Library Version 2026.07.519, PR #1031

Cleans the last stale references left by the §1.19.8 operational-state privatization arc (which relocated 19 living operational docs from the public working-state tree to the private companion repo across #1028/#1029/#1030). Closes the seven findings from the maintainer-directed §1.19.8-change-set deep-assessment (offloaded to a credit-offload worker, pinned to #1030's merge SHA; the scratch deep-assessment record), plus six same-class stragglers the #1031 pre-push skeptical verifier and a class-width re-grep surfaced. Tooling / pack / assistant-guidance / working-state only; no corpus or website content changed.

### Fixed
- **W1 (dead scan constants):** [`tools/tension-scan.py`](../../tools/tension-scan.py) and [`tools/residual-scan.py`](../../tools/residual-scan.py) each carried a constant (`SCANNED_FILES` / `LEDGER_PATHS`) pointing at a working-state doc the parent relocated; both entries dropped, and the two docstrings that echoed them corrected (residual-scan's LEDGER-surface list, tension-scan's historical census count reworded to "then-six").
- **W2 (pack-skill portability):** three distributable pack skills named old working-state paths for relocated docs whose paired commands were repointed to the private repo. [`dev-security/claude-rules/skills/high-assurance-verification/SKILL.md`](../../dev-security/claude-rules/skills/high-assurance-verification/SKILL.md), [`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](../../dev-security/claude-rules/skills/guardrail-review/SKILL.md), and [`dev-security/claude-rules/skills/pr-retrospective/SKILL.md`](../../dev-security/claude-rules/skills/pr-retrospective/SKILL.md) now name the moved register/ledger by portable role (no hard working-state path, and no leak of the private-repo path into the distributable pack), keeping concrete in-repo paths for docs that did not move. Pack version bumped 1.62.1 to 1.62.2 with a version-history row.
- **W3 (gate FAIL message):** [`tools/lint-overnight-file.py`](../../tools/lint-overnight-file.py)'s guidance message repointed from a relocated design-record path to the generic "the design-decisions record".
- **N1 (tool docstrings):** five docstrings across [`tools/audit-brief-freshness.py`](../../tools/audit-brief-freshness.py), [`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py), [`tools/lint-cross-file-section-refs.py`](../../tools/lint-cross-file-section-refs.py), and [`tools/lint-session-state.py`](../../tools/lint-session-state.py) repointed from relocated design-record paths to generic phrasing; docstring-only, no runtime change.
- **N2 (assurance-predicate divergence):** [`tools/detect-env.py`](../../tools/detect-env.py)'s private-repo presence predicate aligned to `is_dir() and any(iterdir())` (with `except OSError: present = False`), matching the PreToolUse hook and the pre-push guard; all three assurance layers now agree that "present" means a non-empty directory.
- **N3 / N4 (CLAUDE.md wording):** the adopter branch in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) no longer tells the adopter to read the private-repo INDEX it lacks ("the concerns this directive names above"), and the "does not enumerate the private repo's internal structure" over-claim is softened to "keeps its enumeration minimal (a few command steps still name the specific operational file they read)".
- **Same-class stragglers (pre-push verifier + class-width re-grep):** the [`/guardrails`](../../.claude/commands/guardrails.md) command (paired command of the fixed guardrail-review skill) repointed its bare moved-ledger mention to the private repo; and two pre-existing #1030 minimization residuals the deep-assessment's working-state-prefix hunt missed by bare-basename width, a session-metrics reference in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) collapsed to the bare concern-stem (matching its siblings) and one in [`.claude/commands/resume.md`](../../.claude/commands/resume.md) genericized to "the session-metrics ledger".

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) reports 72/72; [`tools/detect-env.py`](../../tools/detect-env.py) `--self-test` passes 6/6 (identity and availability classification unaffected by N2); [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) clean.
- Class-width residual re-grep (bare-token plus file-type width) over the operational surfaces (tools, the assistant-config tree, the pack, CLAUDE.md): zero dead relocated-doc paths and zero in-repo-implying bare-basename references remain; the only surviving session-metrics filename reference is resume.md's correctly-repointed private-repo functional pointer.
- Pre-push skeptical verifier (refute-briefed, read-only on the shared tree) confirmed all seven finding-fixes correct and surfaced the same-class stragglers, all fixed and re-verified in-window.

### Discipline observation
The §1.19.8-change-set deep-assessment (maintainer-directed, offloaded, consumed under elevated QA) and the #1030 minimization both ran a working-state-path-prefix-oriented reference hunt, which by construction misses the same doc referenced by BARE BASENAME or by bare concern-stem, and misses the paired COMMAND of an edited SKILL. The #1031 pre-push verifier plus a class-width (bare-token plus file-type plus sibling-command) re-grep caught what both prior passes missed, reaffirming the independent-adversarial-verifier value and the close-out checklist's file-type-width and section-orphan grep lines. No new gate warranted (the surfaces are gate-exempt assistant-config / working-state / pack by design; a gate would be decorative per gate-discipline).

## 2026-07-18, Library Version 2026.07.518, PR #1030

Closes TODO §1.19.8: the `_private`-pointer minimization (the maintainer-approved hybrid), the third and final PR of the §1.19.8 close-out (after the relocation #1028 and the layered assurance #1029). Working-state / assistant-guidance / one spec reference; no other corpus or website content changed.

**The design (maintainer-approved 2026-07-18).** From the `_private` minimization assessment: ONE CLAUDE.md delegation directive replaces the scattered inline `_private` pointers and points at the `_private` INDEX dispatcher (shipped #1029 Part 0). The directive states the identity behaviour (maintainer: read the INDEX, clone-if-absent-on-a-fresh-VM, fail loud; adopter: skip, redirect to the in-repo `.private` placeholder, or create their own) and the read-evidence discipline (a claim "per `_private`" must quote the source). The hybrid keeps the functional command reads explicit.

**What changed.**
- **The operating CLAUDE.md:** added the one delegation directive; the 19 inline `_private` path-pointers collapsed to bare concern-name code-spans (the reader goes via the directive + INDEX). Net `_private` path-pointers in CLAUDE.md: one (the directive's INDEX).
- **The three rules-governance overlays + the audit-programme spec:** their four + one `_private` path-pointers stripped to bare concern-names.
- **The three commands** (resume / retro / high-assurance): a one-line `_private` opener each (maintainer fail-loud / adopter choice); they KEEP their functional reads (index-routed), per the hybrid.
- **TODO / `.working`:** Category-D pointers left as self-resolving per the assessment (out of the hybrid's scope).

**Deterministic + verified.** The strip was a dry-run-validated scripted transform (24 code-spans), then a whole-repo bare-token re-grep across all file types confirmed the only remaining `_private` path-pointers are the one directive INDEX, the seven command functional reads, and the frozen `.working` + TODO Category-D set (the #1028 lesson: verify the transform, do not trust it).

### Added
- The operating CLAUDE.md: the delegation-directive section ("Operational state lives in grc_library_private").

### Changed
- The operating CLAUDE.md: 19 inline `_private` path-pointers collapsed to bare concern-names.
- The three rules-governance overlays + [the audit-programme spec](../../governance/specification-audit-programme.md): five `_private` path-pointers stripped to bare concern-names (spec Version+Date co-bump to 1.17.13; taxonomy + scorecard regenerated).
- The resume / retro / high-assurance commands: a one-line `_private` opener each.
- [TODO.md](../../TODO.md): §1.19.8 rotated to DONE (item deleted; the `§1.19.8` cross-references de-sectioned to `1.19.8` to avoid intra-doc-ref orphans); §3.100 recreated (a section-rotation drift had dropped the Quebec-re-ingest row).

**PR #1029 QA batch (recursion-avoidance).** This PR carries #1029's per-PR QA:
- [validate-pr history](../validate-pr/history.md): #1029 validate-pr row (OFFLOADED to a worker; consumed under elevated QA).
- [improvement log](../improvement-log.md): #1029 `/retro` row.

### Verification
- `run_all_audits` 72/72; the delegation directive + strip verified by a whole-repo bare-token re-grep (zero residual path-pointers beyond the directive INDEX, the kept command reads, and Category-D); a skeptical pre-push verifier ran on the diff.

## 2026-07-18, Library Version 2026.07.517, PR #1029

The layered fail-loud assurance for `grc_library_private`, and bringing `_private` under its own gate + CI (closes TODO §1.19.11). Guard-first: the assurance lands before the later §1.19.8 minimization makes `_private` load-bearing via the CLAUDE.md delegation directive. Working-state / tooling / hooks; no corpus or website content changed.

**The concern (maintainer-directed 2026-07-18).** An AI "trying to be helpful" might ignore `_private` being inaccessible, or skip it and reconstruct its content from memory, instead of using it or failing loud. `_private` holds the maintainer orchestrator's operational state, so for the maintainer a missing `_private` is a broken setup to FIX (clone it), never to silently work around. Honest limit: machinery guarantees `_private` is present-or-fail-loud and makes skip-and-hallucinate a caught discipline failure, but cannot PROVE the AI internalized the content (evidence-discipline plus the verifier cover that residual).

**The layers.**
- `detect-env` emits a `private_availability` decision (mirroring `ref_availability`): maintainer + `_private` absent gives HALT (LOUD); `maintainer-fresh-machine` gives clone-first; `adopter` is graceful (offered a choice). A `--self-test` covers six cases.
- `/resume` step 3 acts on the decision: HALT loud for the maintainer, clone-first on a fresh machine, graceful for an adopter.
- A PreToolUse hook (`block-operational-without-private`) blocks Edit/Write when the origin is the maintainer repo AND `_private` is genuinely absent. It fails OPEN on any uncertainty (a hook bug must never brick the session) and leaves Read/Bash available so the clone remediation works. Registered on the Edit|Write matcher; six-case self-test.
- The pre-push guard refuses a push (exit 4) on the maintainer's own clone when `_private` is absent (the Bash-write path the hook does not gate); identity-conditional, adopter and CI exempt.

**Part 0: `_private` under its own protections (the §1.19.11 half, shipped `_private`-side).** `grc_library_private` gained a stdlib-only validate gate (no-secrets, house style, authored-doc link integrity with a frozen-moved-doc exemption, INDEX completeness), a CI workflow, a CLAUDE.md, a refreshed README, and the INDEX dispatcher. A skeptical verifier caught a REAL defect, five `-ise` stems that never fired (British inserts an "i" before "se"), plus an INDEX substring hole and secrets-coverage gaps; all fixed and re-verified (targets caught, zero false positives on always-British safe words).

### Added
- The PreToolUse Edit/Write hook `block-operational-without-private` (with a six-case self-test), registered in [`.claude/settings.json`](../../.claude/settings.json) on the Edit|Write matcher.
- In [detect-env](../../tools/detect-env.py): a `private_availability_decision` plus a `--self-test`, and `grc_library_private` added to the probed siblings.
- In `grc_library_private` (pushed `_private`-side): the INDEX dispatcher, a stdlib-only validate gate, its CI workflow, and a CLAUDE.md.

### Changed
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): step 3 now acts on the `private_availability` decision.
- [`tools/pre-push-guard.sh`](../../tools/pre-push-guard.sh): an identity-conditional `_private`-required refuse (exit 4) on the maintainer's own clone.
- [`README.md`](../../README.md): version bump.
- [`TODO.md`](../../TODO.md): §1.19.11 rotated to DONE (item deleted; the design-note reference de-sectioned to avoid an intra-doc-ref orphan).

**PR #1028 QA batch (recursion-avoidance).** This PR carries #1028's per-PR QA:
- [validate-pr history](../validate-pr/history.md): #1028 validate-pr row (OFFLOADED to worker-20260716-b, consumed under elevated QA, CLEAN 0 findings; worker-B delivery 1 this session, corroborated by the pre-merge adversarial verifiers).
- [improvement log](../improvement-log.md): #1028 `/retro` row.

### Verification
- `run_all_audits` 72/72; the hook (7 cases), detect-env (6 cases), and `_private`-gate self-tests all green; the hook's live sanity check allows (session not bricked, `_private` present). The high-assurance nature (a session-tool-blocking hook plus operating-instruction wiring) was handled defensively: fail-open on any hook malfunction, deny only on confirmed maintainer-plus-`_private`-absent. A skeptical pre-push verifier traced every hook path and confirmed NO bricking risk (all uncertainty fails open; Read/Bash stay ungated for the clone remediation), and cleared the PR. One LOW hardening it flagged was applied: the maintainer-origin match (in both the hook and the pre-push guard) is boundary-anchored on a `/` or `:`, so a pathological fork owner ending in `jposluns` is not misread as the maintainer and wrongly blocked; an added self-test case covers it.

## 2026-07-18, Library Version 2026.07.516, PR #1028

TODO §1.19.8 Phase-2 relocation: moves the living operational-state documents out of the public working-state tree into the `grc_library_private` companion repo, and repoints the references to them. A working-state / assistant-guidance PR; no corpus or website content changed. The `_private`-integration wiring (the resume provisioning and the advisory-tool rewiring) is deliberately DEFERRED (see below).

**The relocation.** The 19 move-list documents (`third-party-issues`, `credit-offload-design`, `credit-offload-metrics`, `maintainer-egress-requests`, `cloudflare-pages-setup`, `design-decisions`, `multi-session-orchestration`, `hallucination-metrics`, the high-assurance register, the two considerations ledgers, `deferred-protected-changes`, `register-main-branch-protection`, `session-length-considerations`, `cross-file-section-ref-gate-design`, `change-impact-surface-map-draft`, `history-scrub-procedure-draft`, `claudemd-trim-review-draft`, `session-metrics`) were received into `grc_library_private` at commit `c2daf53` (cross-repo, direct-push) and DELETED from this repo's working-state tree. The obsolete `fr48-deferred-worklist` was deleted outright (not moved). `worker-brief-template` is NOT in this PR (it goes to `grc_library_scratch`, a separate scratch-side change).

**The reference repointing (the LOCKED three-bucket rule).** A deterministic scripted transform (dry-run-validated, then applied) converted the markdown-link references to the moved docs into bare code-spans naming the new home under `grc_library_private`, so no link resolves to a now-absent target (gate 3 stays green) and each reference is honest about the doc's new location. The two pre-push adversarial verifiers then caught the references the link-form transform did not reach (the PROJECT-OVERLAY blocks in the local rules tree, a bare-code-span TODO reference, and two live handoff pointers; see the discipline observation below). The final **measured** tally is **51 code-span repoints across nine files**: the operating CLAUDE.md (19), the resume command (5), the retro command (1), the high-assurance command (1), the three local rules-governance PROJECT-OVERLAY blocks (`ai-assistant-workflow-disciplines` 2, `gate-discipline` 1, `high-assurance-verification` 1), the audit-programme spec (1), TODO (18), and the two live standing-section pointers in the handoff (2). The adopter-facing root CHANGELOG's **16** historical references to the moved docs (across four docs) were instead reworded to **plain prose**, not code-spans: the public changelog should not point readers at the private repo, and a path-shaped code-span there fails the CHANGELOG link-coverage gate. The local rules and command tree is gate-3-exempt; the public files (TODO and the spec) are the gate-critical ones the transform kept resolving-link-free.

**The D7 version-token drop.** The D7 handoff-snapshot freshness PR-time check carried a `runbook` SURFACES entry pointing at the now-moved `multi-session-orchestration` runbook. Since that doc moved to the private repo (out of the public repo D7 scans), the `runbook` entry and its docstring line were REMOVED; D7 no longer validates a runbook version token. The `HandoffSnapshotOnPrTests` real-repo path-resolution test now passes (it had failed on the absent runbook path).

**The deferred integration-wiring (maintainer-directed 2026-07-18).** The item's remaining scope, the resume clone-if-absent and `--add-dir` provisioning for the private repo and the advisory-tool rewiring (`tension-scan` and `residual-scan` `resolve_sibling` for the moved `hallucination-metrics` ledger), is the `_private`-integration surface the maintainer wants MINIMIZED and centralized (ideally one CLAUDE.md directive that delegates to the private repo). Building that wiring now would be redone by the minimization design, so it is held for the upcoming discussion. §1.19.8 stays OPEN; this PR lands the irreversible structural relocation only. The `tension-scan` and `residual-scan` `hallucination-metrics` classification entries were left in place (inert, since the file is gone from this repo's tree; rewired in the deferred step) and the stale moved-doc mentions in other tool docstrings are part of the same deferred pass.

### Removed
- The 19 move-list documents from the working-state tree (relocated to `grc_library_private`) and the obsolete `fr48-deferred-worklist` (deleted).
- The D7 check tool's `runbook` SURFACES entry + its docstring line (D7 drops the moved-doc version token).

### Changed
- The operating CLAUDE.md, the resume / retro / high-assurance command files, the three local rules-governance PROJECT-OVERLAY blocks, [the audit-programme spec](../../governance/specification-audit-programme.md), [TODO.md](../../TODO.md), and [the session handoff](../session-handoff.md): 51 moved-doc references repointed to bare `grc_library_private` code-spans (per-file counts above).
- [The root CHANGELOG](../../CHANGELOG.md): 16 historical moved-doc references (four docs) reworded to plain prose (public changelog does not point at the private repo).
- [TODO.md](../../TODO.md): §1.19.8 annotated (relocation DONE; integration-wiring PENDING, deferred to the minimization discussion).
- [The audit-programme spec](../../governance/specification-audit-programme.md): Version+Date co-bump (1.17.11 -> 1.17.12) for the repointed reference (a versioned-doc body change); taxonomy + scorecard regenerated.
- Root CHANGELOG entries for PR #975, #980, #981, #983, #984: compacted to the 100-word ceiling. Their dead moved-doc links (fixed as part of this relocation) put them in the diff, exposing a pre-existing D8 length violation (109 to 151 words); the full detail remains in this mirror and git history.
- [TODO.md](../../TODO.md): §3.101 opened (the D7 handoff-snapshot check is a silent no-op on the current two-line handoff format, discovered at this PR's guard); the stale P3 next-item-number marker corrected.

**Discipline observation (apply-time verifier catches).** The link-form scripted transform under-reached, and the two pre-push adversarial verifiers plus the orchestrator's own whole-repo bare-token re-grep caught four classes before push: (1) **four missed PROJECT-OVERLAY repoints** in the local rules-governance tree (the overlay blocks were not in the transform's target-file set, though their sibling CLAUDE.md and command surfaces were repointed, confirming intent) [missed-reference verifier]; (2) **accounting inaccuracy** in the drafted #1028 prose, a fabricated "49" (unmeasured; the true measured figure is 51 code-spans plus 16 CHANGELOG prose), "7 CHANGELOG code-spans" (actually prose), and a "15 TODO" that counted lines not references (17, now 18) [repoint-correctness verifier, the meta-prose measured-not-inferred guard]; (3) **two live strays the link-form regex missed**, a bare code-span in TODO §3.82 and two live standing-section pointers in the handoff (the missed-reference verifier wrongly cleared the handoff; the orchestrator's independent bare-token re-grep caught them, a class-width re-verify); (4) a **stale "15 KEEP" count** in the relocated `claudemd-trim-review-draft` [validate-pr on #1027, Finding 1], fixed in the private repo. All fixed in-window before push. The transform correctly left the project-agnostic pack skill sources, the frozen working-state historical archives, and the deferred advisory-tool constants untouched.

**PR #1027 QA batch (recursion-avoidance).** This PR carries #1027's per-PR QA:
- [validate-pr history](../validate-pr/history.md): #1027 validate-pr row (2 Low findings; both fixed in-window in this PR).
- [improvement log](../improvement-log.md): #1027 `/retro` row.

### Verification
- `run_all_audits` green 72/72 (gate 3 links, gate 36 regression, D7, gate 37 pack-parity over the overlay edits, and the CHANGELOG link-coverage gate all pass); the repoint was a deterministic scripted transform re-parsed after apply; two skeptical adversarial verifiers (missed-reference and broken/wrong-repoint lenses) run pre-push, their findings validated and fixed, then re-verified by whole-repo bare-token re-grep. The high-assurance register entry for this sensitive change is recorded in the private repo.

## 2026-07-18, Library Version 2026.07.515, PR #1027

Records the completed TODO §1.19.12 CLAUDE.md sensitivity-trim review (maintainer-confirmed, attended). A working-state PR; no corpus or website content changed.

**The review.** The classification locked in #1025 (over the then-30 sections) was walked section-by-section with the maintainer (AskUserQuestion batches: the 2 MOVE + the lean-MOVE SPLITs, then the smaller SPLITs, then the KEEP group). Every verdict was confirmed, with **one change**: the "Date and timezone convention" section is **KEEP whole** (the maintainer chose to keep the maintainer-side America/Toronto note public), not the draft's SPLIT. The two sections the #1026 bundle added were classified in the same pass: **Boundaries -> SPLIT** (item 11's cross-repo-write private-sibling repo names + the `/home/jposluns/` path move; the generic write-safety principle and the other boundaries stay public) and **QA-activity completion standard -> KEEP** (portable, with a pack-rule twin). `/screen-publications` KEEP was confirmed (its body was re-read in #1025: no private pointer). **Final classification: 32 sections, 2 MOVE / 17 KEEP / 13 SPLIT.**

**Status.** [`claudemd-trim-review-draft.md`](../claudemd-trim-review-draft.md) is now marked REVIEWED + maintainer-confirmed FINAL; it is the input to the Phase-5 CLAUDE.md trim (the content move to `_private`, sequenced with §1.19.8; the operating CLAUDE.md stays public, so only the MOVE + SPLIT-flagged content moves). §1.19.12 stays OPEN until that apply.

### Changed
- [`.working/claudemd-trim-review-draft.md`](../claudemd-trim-review-draft.md): status LOCKED -> REVIEWED-FINAL; Date/timezone SPLIT -> KEEP; split the "Version-bump / Boundaries" row (Version-bump KEEP, Boundaries SPLIT for item 11); added the QA-completion-standard KEEP row; resolved the /screen-publications note; tally 30 (2/15/13) -> 32 (2/17/13).
- [`TODO.md`](../../TODO.md): §1.19.12 annotation LOCKED -> REVIEWED + maintainer-confirmed FINAL.

**PR #1026 QA batch (recursion-avoidance).** This PR carries #1026's per-PR QA:
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1026 validate-pr row.
- [`.working/improvement-log.md`](../improvement-log.md): #1026 `/retro` row.

### Verification
- The review outcome is a recorded maintainer confirmation, not a corpus change; `run_all_audits.sh` green; per-PR `/validate-pr` + `/retro`. The Phase-5 apply (the actual CLAUDE.md content move) is separate, sequenced with §1.19.8.

## 2026-07-18, Library Version 2026.07.514, PR #1026

Applies three staged protected-file changes from [`deferred-protected-changes.md`](../deferred-protected-changes.md) (maintainer-authorized on the VM, attended; the maintainer directed "protected bundle now, before §1.19.8"). CLAUDE.md, the `ai-assistant-workflow-disciplines` pack rule (both trees), and working-state; no corpus or website content changed.

**Item 11 (closes TODO §1.15): cross-repo write-safety convention line.** Added a `## Boundaries` bullet to the operating CLAUDE.md: before every Write/Edit and every repo-mutating git command across the colocated repos (`grc_library` / `grc_library_ref` / `grc_library_scratch` / `grc_library_private`), confirm the target repo (`git rev-parse --show-toplevel` for git, or route through `tools/repo-guard.sh <repo> -- <cmd>`; the absolute-path prefix for Write/Edit) and prefix git sequences with `cd /home/jposluns/<repo> &&`. This is §1.15 part (b); part (a) (`tools/repo-guard.sh` + `RepoGuardTests`) shipped in #1013, so **§1.15 is now complete and rotated to DONE** (the P1 count drops to five machinery items).

**Item 12: QA-activity completion standard.** Added a `## QA-activity completion standard` section to the operating CLAUDE.md (the five conditions for a QA activity to be COMPLETE: sanctioned formal shape; every finding terminally triaged, none dropped; worker positives re-verified at source; the history row recorded; deferred fixes documented; plus the sign-off condition for the heaviest tiers; and the standing "fixing QA issues outranks build/tooling/content" priority). The same standard, project-agnostically, was added to the ai-assistant-workflow-disciplines pack rule in BOTH trees (`dev-security/claude-rules/` and the `.claude/rules/` copy; verified byte-identical, gate 37; the language linter clean on the new pack prose before commit). Codifies the standing QA-completion discipline (the durable form previously only in the orchestrator memory `qa-findings-are-top-priority`).

**Item 15: currency fix.** Reworded the two operating-CLAUDE.md lines that described the §3.93(c) scratch-queue auto-fetch backstop as "queued"/"is queued"; it shipped scratch-side 2026-07-18, so both now read as shipped (factual-staleness fix; CLAUDE.md is gate-exempt, so nothing was failing).

**Assessment note (maintainer-directed).** Items 11 and 12 ADD content to CLAUDE.md, so the §1.19.12 sensitivity-trim classification (locked in #1025 over the prior 30 sections) will be RE-RUN over the updated CLAUDE.md to classify the two new sections (the cross-repo-write Boundaries bullet, which names the private siblings + the maintainer path, is a SPLIT candidate; the QA-completion-standard section is a portable KEEP candidate) before the one-by-one review.

### Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): added the cross-repo write-safety Boundaries bullet (item 11) and the `## QA-activity completion standard` section (item 12); reworded the two §3.93(c) currency lines (item 15).
- [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](../../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) and its [`.claude/rules/` copy](../../.claude/rules/governance/ai-assistant-workflow-disciplines.md): added the project-agnostic `## QA-activity completion standard` section (byte-identical; gate 37).
- [`TODO.md`](../../TODO.md): §1.15 deleted (rotated to DONE); P1 machinery-item count six -> five.

**PR #1025 QA batch (recursion-avoidance) + its finding-fixes.** This PR carries #1025's per-PR QA (validate-pr + retro rows) AND fixes the four in-window findings #1025's validate-pr surfaced (1 warning + 3 notes, all working-state, no corpus/tool defect):
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1025 validate-pr row.
- [`.working/improvement-log.md`](../improvement-log.md): #1025 `/retro` row.
- [`.working/session-state.md`](../session-state.md): re-reconciled the `Current-task` line (W-1, the #619 append-not-reconcile: removed the stale "pending-decisions EMPTY", "§1.19.12 HELD", and "daytime-unattended" tail clauses that the #1025 front-only reconcile left); updated `Active-session` to this branch; re-stamped the heartbeat.
- [`.working/pending-decisions.md`](../pending-decisions.md): marked `:333` RESOLVED (maintainer chose SEF-06 + SEF-07 via AskUserQuestion; apply pending in a dedicated PR), queue back to empty.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): clarified the #1025 entry's "SEF-02" -> "SEF-02, SEF-03" imprecision (N-3).

### Verification
- the language linter clean on the new pack prose (before commit); the two pack copies byte-identical (gate 37); `run_all_audits.sh` green; a refute-briefed skeptical verifier on the diff (the one DEFECT-FOUND it raised, the not-yet-added #1025 QA rows, is resolved by adding them here; all 7 other targets clean); per-PR `/validate-pr` + `/retro`.

## 2026-07-18, Library Version 2026.07.513, PR #1025

Locks the TODO §1.19.12 CLAUDE.md sensitivity-trim classification (maintainer-approved, attended) and records the return to attended-autonomous mode. A working-state PR; no corpus or website content changed.

**§1.19.12 classification LOCKED.** The maintainer reviewed and approved the sensitivity-trim classification ("proceed and lock classifications first", 2026-07-18, attended). The classification (30 CLAUDE.md sections: 2 MOVE / 15 KEEP / 13 SPLIT, broad-trim lean) is locked in [`claudemd-trim-review-draft.md`](../claudemd-trim-review-draft.md) as the input to the Phase-5 CLAUDE.md trim (the actual content move to `_private`, sequenced with the §1.19.8 relocation; the operating CLAUDE.md stays public, so only the MOVE/SPLIT-flagged content moves). The three strictness calls were resolved to the broad-trim-as-drafted lean: (1) provenance tails KEEP (not the stricter split-out; the maintainer may tighten at apply); (2) `/screen-publications` KEEP (re-read of the live body confirmed no `_private` pointer / no maintainer-machine / dated-directive content, only the portable screening cadence + a reference-base-register pointer + a PR-provenance tail); (3) the session-migration checklist applies bullet-wise, not as a block move. §1.19.12 stays OPEN until the Phase-5 trim is applied.

**Mode.** The maintainer returned ~14:00Z and set attended-autonomous; the `Operating-mode` lease field was flipped from `daytime-unattended` (the field had gone stale while the maintainer was out, which had blocked `AskUserQuestion`), the lease heartbeat re-stamped, and the `Current-task` reconciled to the §1.19.x close-out plan.

**One open decision logged.** A `/matrix-fit`-cadence finding from the SEF-07 batch: `operations/procedure-security-monitoring-and-alert-management.md:333` maps "Alert triage and response" to CSA CCM `SEF-02, SEF-03`, where `SEF-02` (= "Service Management Policy and Procedures") is the wrong control, same class as the #1022 SEF-07 fix. Recommended remap `SEF-02, SEF-03` -> `SEF-06` "Event Triage Processes" + `SEF-07` "Incident Management and Response"; NOT auto-applied (expert-review-facing semantic-fit call), logged in [`pending-decisions.md`](../pending-decisions.md) for the maintainer's disposition.

### Changed
- [`.working/session-state.md`](../session-state.md): `Operating-mode` `daytime-unattended` -> `attended-autonomous`; heartbeat re-stamped; `Current-task` reconciled to the §1.19.x close-out.
- [`.working/claudemd-trim-review-draft.md`](../claudemd-trim-review-draft.md): status DRAFT -> LOCKED (maintainer-approved); decision points resolved.
- [`TODO.md`](../../TODO.md): §1.19.12 annotated CLASSIFICATION LOCKED (stays open until the Phase-5 apply).
- [`.working/pending-decisions.md`](../pending-decisions.md): logged the open `:333` SEF-02 control-fit decision.

**PR #1024 QA batch (recursion-avoidance).** This PR carries #1024's per-PR QA:
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1024 validate-pr row.
- [`.working/improvement-log.md`](../improvement-log.md): #1024 `/retro` row.

### Verification
- Working-state + version surfaces only; `run_all_audits.sh` green; per-PR `/validate-pr` + `/retro`. The §1.19.12 lock is a recorded maintainer approval, not a corpus change; the actual CLAUDE.md trim is Phase-5.

## 2026-07-18, Library Version 2026.07.512, PR #1024

Closes TODO §1.21 (P1, machinery): three non-existent ISO/IEC 27002:2022 sub-controls in the logging-and-monitoring standard. A single-corpus-document citation-accuracy fix; no website content changed.

**The defect.** [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md)'s `## Framework alignment` control-mapping table (which claims ISO/IEC 27002:2022) cited `§8.15.3` (Time synchronization), `§8.15.5` (Central collection and retention), and `§8.15.7` (Access and protection). ISO/IEC 27002:2022 controls are FLAT, there is no `8.15.x` sub-numbering (held `8.15.3` returns 0 hits; the standard's table of contents lists only `8.15 Logging`, `8.16 Monitoring activities`, `8.17 Clock synchronization`).

**The fix (verified at held source).** Time synchronization -> **§8.17** "Clock synchronization" (the held 8.15 guidance itself cross-references 8.17 for time-source synchronization). Central collection and retention -> **§8.15** "Logging", and Access and protection -> **§8.15** "Logging": in 27002:2022 log storage, retention, protection, and analysis are all subsections *within* the single 8.15 "Logging" control (the held text has a dedicated "Protection of logs" subsection and cross-references 5.28 for retention), so 8.15 is the correct primary control for both rows and no better-fitting control exists. The `§8.15` (Log management) and `§8.16` (Monitoring and alerting) rows were already correct and unchanged. Surfaced OUT-OF-WINDOW by the Sweep-112 delivery-1 false-negative auditor (routed to §1.21); it is the incomplete-cross-file-harmonization sibling of the §1.17 W2 `8.15.3`->`8.17` fix (#1001), which corrected the same error in the sibling [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md).

### Changed
- [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md): the three framework-alignment ISO/IEC 27002 cells corrected (`8.15.3`->`8.17`, `8.15.5`->`8.15`, `8.15.7`->`8.15`). Version `1.4.13` -> `1.4.14`, Date -> 2026-07-18.
- [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the Version bump (portal.md byte-identical).

**PR #1023 QA batch (recursion-avoidance).** This PR carries #1023's per-PR QA:
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1023 validate-pr row.
- [`.working/improvement-log.md`](../improvement-log.md): #1023 `/retro` row.

### Verification
- A skeptical verifier confirmed all three corrections against the held ISO/IEC 27002:2022 text (`8.15.x` non-existent; `8.17` = Clock synchronization; both `-> 8.15` remaps correct with no better control), plus completeness (no residual sub-numbered ISO citation in the file) and bookkeeping (Version+Date co-bump, artefacts in sync). `run_all_audits.sh` green; per-PR `/validate-pr` + `/retro`.

## 2026-07-18, Library Version 2026.07.511, PR #1023

Closes TODO §1.20 (P1, machinery): the `adopt-preflight-guard` live-smoke test was not adopter-portable. A tests-and-working-state PR; no corpus or website content changed.

**The defect.** `tests/test_linters.py` `AdoptPreflightGuardTests.test_live_repo_refuses_on_maintainer_clone` shelled out to the real `classify()` and asserted the guard exits 3 (REFUSE). That holds on a maintainer clone and in CI (both classify non-adopter), but a genuine ADOPTER clone classifies `adopter`, so `adopt-preflight-guard.py` correctly exits 0 (proceed) and the hardcoded `== 3` assertion fails. An adopter running `run-linter-regression` would see that one test fail, breaking the adopter-clone portability invariant (validate-pr-1019's environment-artefact caveat, which is exactly how a worker's `adopter`-classified nested clone surfaced it).

**The fix.** The test now reads the live classification and asserts the guard's exit is CONSISTENT with it: `rc == 0` iff `classify() == "adopter"`, else `rc == 3`. This is portable, a maintainer / fresh-machine / CI clone -> non-adopter -> rc 3; a genuine adopter clone -> rc 0; a failed or missing probe -> `None` (not `"adopter"`) -> the fail-safe rc 3. The test is renamed `test_live_repo_guard_consistent_with_classification` to reflect the environment-agnostic assertion. `main()`'s contract (`return 0` iff `classify() == "adopter"`, else `3`) is unchanged, so this only fixes the test, not the guard.

### Changed
- [`tests/test_linters.py`](../../tests/test_linters.py): rewrote the adopt-preflight live-smoke test to assert rc-consistency with the live `detect-env` classification (portable across clone types) and renamed it accordingly.
- [`TODO.md`](../../TODO.md): deleted §1.20 (rotated to DONE); bumped the stale "Next item number" pointer `1.21` -> `1.22` (a #1021 omission: §1.21 was assigned without bumping the pointer); updated the P1 point-fix enumeration to drop the now-closed §1.20.

**PR #1022 QA batch (recursion-avoidance).** This PR carries #1022's per-PR QA:
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1022 validate-pr row.
- [`.working/improvement-log.md`](../improvement-log.md): #1022 `/retro` row.

### Verification
- The rewritten test exercises the real `classify()` shell-out; it passes on this maintainer clone (classify -> non-adopter -> guard rc 3 -> assert rc 3). The full `run_all_audits.sh` (gate 36 linter-regression) is green. Skeptical verifier not required for a test-portability fix beyond the regression run itself; per-PR `/validate-pr` + `/retro`.

## 2026-07-18, Library Version 2026.07.510, PR #1022

The SEF-07 CSA CCM control-code remap (the deep-assessment r5 Medium-1 finding, maintainer-directed to `SEF-07` as the fresh-session first fix; pending-decisions morning-review item). A corpus citation correction.

**The defect.** The incident-escalation SOP's `## Framework alignment` table cited `CSA CCM v4.1 | SEF-02: Incident Management`, and its row in the document-index register cited `CSA CCM SEF-02`. But held CSA CCM v4.1.0 (catalogue CSV:601) defines `SEF-02` as "Service Management Policy and Procedures", an IT-service-management control, not an incident-management one; the mislabel also invented the title "Incident Management". The correct control for a cloud-incident-escalation SOP is `SEF-07` "Incident Management and Response" (CSV:618: "Define, implement and evaluate processes, procedures and technical measures for timely and effective response to security incidents in accordance with incident categories and severity levels").

**Scope discipline.** A corpus-wide grep found the citation at exactly the two fixed sites plus FIVE other corpus `SEF-02` carriers (measured by a corpus-wide grep over markdown, excluding the working tree and the root changelog: 5), all correctly LEFT after verification: `compliance/matrix-grc-compliance-alignment.md:191,192` cite `SEF-02` for the IT-Service-Management framework and the Service-Level-Management standard (CORRECT, that is exactly what SEF-02 is); `security/procedure-security-incident-response.md:330` and `compliance/matrix-grc-compliance-alignment.md:147` cite `SEF-01, SEF-02, ...` in incident-management-policy contexts (SEF-02 defensible alongside SEF-01); and `operations/procedure-security-monitoring-and-alert-management.md:333` cites `SEF-02, SEF-03` for "Alert triage and response", where SEF-06 "Event Triage Processes" + SEF-07 would fit better, a distinct semantic-fit judgment noted for a future `/matrix-fit` pass, out of scope for this scoped r5 fix. (A historical root-changelog entry also mentions SEF-02; excluded.)

### Changed
- [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md): `SEF-02: Incident Management` -> `SEF-07: Incident Management and Response` in the framework-alignment table. Version `1.2.6` -> `1.2.7`, Date -> 2026-07-18.
- [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md): the incident-escalation-matrix row's `CSA CCM SEF-02` -> `CSA CCM SEF-07`. Version `1.27.86` -> `1.27.87`, Date -> 2026-07-18.
- [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the two Version bumps (portal.md byte-identical).

**PR #1021 QA batch (recursion-avoidance) + its two remediation fixes.** This PR also carries #1021's per-PR QA and fixes the two in-window findings its `/validate-pr` surfaced:
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #1021 validate-pr row (SHIP, 1 warning + 1 note, both fixed here); Version `1.2.782` -> `1.2.783`.
- [`.working/improvement-log.md`](../improvement-log.md): #1021 `/retro` row; Version `1.0.716` -> `1.0.717`.
- [`TODO.md`](../../TODO.md): fixed the stale P1 count prose (W-1) - "six open items" reworded to "six standing machinery/guardrail items alongside short-lived point-fix items (currently §1.20, §1.21)", so the enumeration is no longer contradicted by the uncounted §1.20/§1.21.
- [`.working/session-handoff.md`](../session-handoff.md): marked the retained 2026-07-17 block's prune-note historical (N-1, #619 reconcile), since #1021 dropped the 2026-07-16c blocks it said to keep.

### Verification
- The `SEF-07` title verified against the held CSA CCM v4.1.0 catalogue (`grc_library_ref/frameworks/CSA/CCM/CSA-CCM-v4.1.0-catalogue__CCM.csv:618`); `SEF-02` = "Service Management Policy and Procedures" (CSV:601) confirmed as the wrong control. `SEF-07` already exists in the gate-48 reference module, so gate 48 accepts it. A corpus-wide `SEF-02` grep confirmed no other incorrect carrier. Skeptical verifier + per-PR `/validate-pr` + `/retro`.

## 2026-07-18, Library Version 2026.07.509, PR #1021

The Sweep 112 loop-break close-out and the first PR of the 2026-07-18 resumed session (`/resume` from #1020, on the VM, gh-CLI, daytime-unattended). Records the corpus-wide `/validate` that is the loop-break compensating control for session-closing handoff PR #1020 (which skipped its trailing `/validate-pr` + `/retro`). Working-state and version surfaces only; no corpus or website content changed.

**Sweep 112 outcome.** Offloaded to `worker-20260716-a` (Opus 4.8) as the pre-positioned blocking priority-0 order `sweep-112-validate` pinned to `56889588`/#1020, over the #1000..#1019 deltas (diff base #999 `65c5075b`). Consumed under full ELEVATED QA (worker-a's delivery 1 this fresh session, so the session-scoped `(worker+model)` trust window re-establishes): the worker's proof-of-run is genuine (~240K tokens, A/B/C subagent returns); the orchestrator independently re-derived the mechanical facts (HEAD `56889588` = #1020 = pinned SHA; baseline **72/72** on the maintainer clone; counts 13 rules / 24 skills / 15 commands / 18 document-types; four-surface parity 72; versions library `2026.07.508` / pack `1.62.1` / spec `1.17.11`), all EXACT-MATCH; the three superseded-citation residual greps (`23.3`, `ID.AM-3`, `8.15.3`) returned zero live carriers; and a dedicated delivery-1 false-negative auditor independently re-verified all four changed citations at held source and returned CLEAN-CONFIRMED. The worker's 71/72 (versus the maintainer clone's 72/72) is the known-open §1.20 origin-dependent adopt-preflight test on the worker's `adopter`-classified nested clone, honestly disclosed, EXPECTED not a discrepancy. **0 error / 0 warning / 0 new in-window findings; all #1000-#1019 asserted-clean surfaces corroborated, 0 contradicted; the loop-break control for #1020 PASSES.** worker-a stays ELEVATED (1 of 2-to-3 clean elevated passes this session).

**S112-1 (out-of-window, routed).** The delivery-1 auditor also surfaced one out-of-window citation error (the file was not in the #1000-#1019 delta, so the sweep correctly did not flag it, and it does not refute the delta-clean verdict): [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md) lines 140-142 cite three non-existent ISO/IEC 27002:2022 sub-controls (`§8.15.3` time synchronization, `§8.15.5` central collection and retention, `§8.15.7` access and protection) in a table that claims 27002:2022, whose controls are flat (held `8.15.3` returns 0 hits). Orchestrator-re-verified at the held standard: time synchronization is `§8.17` "Clock synchronization"; the other two fold into `§8.15` "Logging". Routed to new TODO §1.21 for a dedicated fix (two rows are a semantic-fit call warranting a skeptical verifier). This is the incomplete-cross-file-harmonization sibling of the §1.17 W2 `8.15.3`->`8.17` fix (#1001).

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): pruned to keep-current-plus-one-prior (dropped the 2026-07-16c #985-#991 "Next actions" / "State snapshot" / "Asserted expectations" blocks); prepended the Sweep 112 row to the Resume-cursor (demoting Sweep 111 to Prior).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): prepended the Sweep 112 row (CLEAN PASS, loop-break for #1020 passes, S112-1 routed); Version `2.0.111` to `2.0.112`.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the missing #1020 handoff-exemption row (`SKIPPED (handoff-PR exception)` in the Findings cell). The prior session omitted this row, so gate 50 (bookkeeping-parity) flagged #1020 the moment this PR demoted it from the highest-numbered (in-flight-exempt) PR, the #445/#450 recurrence class; caught at this PR's pre-push audit and fixed in-window. Version `1.2.781` to `1.2.782`.
- [`.working/session-state.md`](../session-state.md): acquired the concurrency lease for this session (`Active-session` = `claude/resume-sweep112-closeout`, `Status: active`, `Operating-mode: daytime-unattended`, fresh heartbeat); recorded worker-a at 1 clean elevated pass, worker-b free/unvalidated.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to drop the consumed Sweep-112 item and show the fresh queue.

### Added
- [`TODO.md`](../../TODO.md): new §1.21 (P1, the S112-1 ISO/IEC 27002:2022 control-number accuracy fix in the logging-and-monitoring standard).

### Verification
- `tools/run_all_audits.sh` = **72/72** standalone on the maintainer clone (independent of the worker's run). Clone non-shallow. The consume applied the elevated-QA delivery-1 protocol (proof-of-run genuineness, independent mechanical re-derivation, a dedicated false-negative auditor, every changed citation re-verified at held source). Per the session-boundary loop-break, the compensating control for #1020 is this recorded corpus-wide sweep; this close-out PR itself takes the normal per-PR `/validate-pr` + `/retro` (it is not a session-closing handoff).

## 2026-07-18, Library Version 2026.07.508, PR #1020

Session-closing handoff for the 2026-07-17b resumed session (`/resume` from #999; merged #1000-#1019). Working-state and version surfaces only; no corpus or website content changed. Per the session-boundary loop-break, this PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (pre-positioned as **Sweep 112** at this wind-down, over the #1000..#1019 deltas, pinned to #1020's merge SHA).

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): added the 2026-07-17b "Next actions" CLOSING + LOCKED "NEXT SESSION" blocks, the "State snapshot" block, and the "Asserted expectations" block; set "Open decisions" to the wind-down EMPTY status. The next `/resume` prunes to keep-current-plus-one-prior.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to the fresh-session LOCKED order (consume Sweep 112 -> fix SEF-07 + §1.20 -> protected-apply bundle -> §3.22 D7 -> §1.19.x Phase 2).
- [`.working/session-metrics.md`](../session-metrics.md): one row for this session (measured-versus-not-instrumented discipline; the offload plane's ~2.85M est. tokens conserved recorded as a conserved-token proxy, not a fabricated in-session subagent total).
- [`.working/session-state.md`](../session-state.md): concurrency lease RELEASED (`Active-session: none`, `Status: released`, fresh heartbeat).

### Added (batched QA for PR #1019, per recursion-avoidance)
- [`.working/validate-pr/history.md`](../validate-pr/history.md): the #1019 `/validate-pr` row.
- [`.working/improvement-log.md`](../improvement-log.md): the #1019 `/retro` row.
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md): the session-final roll-up.
- [`.working/DONE.md`](../DONE.md) and [`TODO.md`](../../TODO.md): §3.100 closed and rotated; §1.20 added to P1 (the [`tools/adopt-preflight-guard.py`](../../tools/adopt-preflight-guard.py) test-portability regression surfaced by validate-pr-1019).
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): r5 recorded SIGNED OFF.
- [`.working/pending-decisions.md`](../pending-decisions.md): wind-down EMPTY status; the morning decisions (Quebec RESOLVED, §1.14 CONFIRMED, r5 SIGNED OFF, SEF-07 chosen) recorded.

### Verification
- The pre-push guard (`run_all_audits.sh` at 72 gates + `run-pr-time-checks.sh` D1-D8) green standalone; D7 handoff-snapshot freshness confirms the version tokens on the "Current truth" line (library `2026.07.508`, README `1.9.869`, pack `1.62.1`, spec `1.17.11`). No skeptical verifier (pure bookkeeping tier).

## 2026-07-18, Library Version 2026.07.507, PR #1019

Maintainer-authorized correction of a live Quebec Law 25 citation error (the HIGH morning-review escalation). The daytime maintainer directed "fix the HIGH quebec law issue first"; this is the corpus fix.

### Fixed
- [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md) lines 30 and 60: the Quebec Law 25 (CQLR c. P-39.1) privacy-impact-assessment duty was cited as "s. 23.3", which is WRONG (s. 23.3 does not exist in P-39.1; ss. 23/24 belong to the public-sector Act A-2.1). Corrected to "**s. 3.3**", matching the annex's own "s. N" style and the correct citation the other Canada documents already carry (the DPIA template, the privacy-impact procedure, and the document-index register all read "3.3 / §3.3"). Version 1.1.3 to 1.1.4, Date to 2026-07-18 (co-bumped in the body-change commit); the taxonomy, portal, and maturity-scorecard artefacts regenerated.

### Root cause and evidence
- The "23.3" came from PDF margin-note corruption in the held reference source (a stray "2"/"0" from the rotated "2021, c. 25" annotation prepended to "3.3."), shipped into the annex by PR #973 (2026-07-16). A pre-push skeptical verifier caught it overnight (2026-07-18); s. 3.3 is confirmed three ways: the held statute's own s. 3.4 body cross-references "section 3.3", the even-numbered header series is clean, and the offloaded validate-pr-1012 confirmed at upstream LégisQuébec (HTTP 200, zero occurrences of "23.3"). A corpus-wide grep confirmed these two annex lines were the only wrong carriers.

### Changed
- [`TODO.md`](../../TODO.md): §3.84 deleted (closed) and rotated to [`.working/DONE.md`](../DONE.md); the clean-source re-ingest stays open as §3.100.
- [`.working/pending-decisions.md`](../pending-decisions.md): the HIGH morning-review Quebec entry marked RESOLVED (fix applied, PR #1019), original retained for the audit trail.
- [`.working/session-state.md`](../session-state.md): Operating-mode overnight-unattended to daytime-unattended (maintainer-directed 2026-07-18 ~07:02 EDT).

### QA batch (recursion-avoidance)
- Batches PR #1018's `/validate-pr` (validate-pr-1018, offloaded worker-b, CLEAN) and `/retro` rows.

### Verification
- All 72 audit gates pass; changelog preflight clean; pre-push guard both runners green; a refute-briefed skeptical verifier on the diff. Library 2026.07.507, README 1.9.868.
- Follow-up (next, this session): the maintainer uploaded a clean Quebec Law 25 to the reference base's ingest area; §3.100 will ingest it, superseded-archive the corrupted held file, and re-verify s. 3.3 against the now-clean held source (closing the "no clean held-source re-verification possible" caveat that made this fix maintainer-gated).

## 2026-07-18, Library Version 2026.07.506, PR #1018

Close-out consolidation: rotate TODO §3.93 to DONE and batch PR #1017's QA (working-state only; no corpus change). §3.93 (stale-scratch-coordination-read recurrence-prevention) is now fully complete: parts (a) the sync-scratch-every-PR close-out line and (b) the `/resume` step-3 + `## Credit-offload mode` fetch-before-read mandate were already applied in the project CLAUDE.md (prior session), and part (c) shipped scratch-side (a `grc_library_scratch` PR: the credit-offload queue tool's `list-workers` / `list-pending` now best-effort fetch origin and read the shared `origin/main` queue and workers state via `git show` NON-MUTATINGLY, with a local-working-tree fallback; the field parser refactored into a text-core variant; only the two LIST commands changed).

### Changed
- [`TODO.md`](../../TODO.md): §3.93 deleted (closed) and rotated to [`.working/DONE.md`](../DONE.md); §3.92 annotated (part (b) tool-side shipped in #1017, `/adopt` invocation staged deferred item 14).
- [`.working/DONE.md`](../DONE.md): §3.93 close entry (keyed PR #1018 + the scratch PR).
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 15 stages the daytime protected cleanup of two now-stale project-CLAUDE.md lines that still call §3.93(c) "queued" (factual staleness only; CLAUDE.md is gate-exempt, so nothing fails).

### QA batch (recursion-avoidance)
- Batches PR #1017's `/validate-pr` (validate-pr-1017, offloaded worker-b, CLEAN, the adopt-guard fail-safe re-derived by code + test + empirical refuse) and `/retro` rows.

### Verification
- All 72 audit gates pass; changelog preflight clean; pre-push guard both runners green. This is a pure grc_library bookkeeping / rotation PR (no code, no corpus); the §3.93(c) code change was verified and shipped in the scratch PR (the scratch validate gate green + both list commands manually exercised). Library 2026.07.506, README 1.9.867.

### Discipline observation
- The §3.93(c) scratch change was orchestrator-authored (not offloaded), so it carries no credit-offload metrics row; it is exchange-channel tooling maintenance under the orchestrator's scratch write authority. The grc_library-side closure (this PR) is where §3.93 rotates to DONE, since the scratch PR cannot write grc_library.

## 2026-07-18, Library Version 2026.07.505, PR #1017

TODO §3.92 part (b): a mechanical pre-flight adopter-clone guard for `/adopt` (tooling only). `/adopt` resets the machinery-core working-state to adopter baselines, which is destructive on the wrong clone; the dangerous direction was defended by convention (host-pinned origin match, step-1 operator confirmation, config short-circuit, git-revertability). This adds a mechanical gate on top.

### Added
- [`tools/adopt-preflight-guard.py`](../../tools/adopt-preflight-guard.py): a fail-safe helper that shells out to [`tools/detect-env.py`](../../tools/detect-env.py) (the single source of truth for operator classification), reads `identity.classification`, and exits 0 ONLY on `adopter`; any other outcome, a `maintainer` / `maintainer-fresh-machine` classification, an undetermined identity, a probe failure, or malformed probe output, exits 3 (REFUSE, so `/adopt`'s reset does not run). It makes no independent classification decision (the logic stays in one place). Exit 2 on an internal error (probe not locatable). Not an audit gate; not wired into CI.
- [`tests/test_linters.py`](../../tests/test_linters.py) `AdoptPreflightGuardTests` (5): adopter -> 0; maintainer / fresh-machine / undetermined(None) -> 3 (the fail-safe); and a live smoke test that the real shell-out + parse classifies this maintainer clone non-adopter and REFUSES (exit 3). Decision tests monkeypatch the module-global `classify`.

### Changed
- [`TODO.md`](../../TODO.md) §3.92: part (b) tool-side SHIPPED annotation; the protected `/adopt` step-1 invocation staged (deferred item 14); part (c) remains, §3.92 stays open.
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 14 stages wiring the guard into the adopt SKILL + command step 1 (run the guard before the reset; a non-zero exit hard-stops `/adopt`), keeping the existing operator confirmation as defence in depth.

### Verification
- `python3 -m unittest tests.test_linters.AdoptPreflightGuardTests`: 5/5. The guard REFUSES (exit 3) on this maintainer clone (correct). All 72 gates pass; changelog preflight clean; pre-push guard both runners green; a refute-briefed skeptical verifier pre-push.
- Batches PR #1016's `/validate-pr` (validate-pr-1016, offloaded) and `/retro` rows.

### Discipline observation
- Composes with #1016: the guard reuses the environment probe's classification (enhanced in #1016) rather than re-deriving it, so the maintainer-vs-adopter decision has one source of truth across the origin probe, the adopt-config flag, and this guard. Part-b tool-side ships now; the protected `/adopt` invocation stages, the same part-ships / invocation-stages pattern as §1.15a and §3.92(a).

## 2026-07-18, Library Version 2026.07.504, PR #1016

TODO §3.92 part (a): mechanical adopt-config validity flag in the environment probe [`tools/detect-env.py`](../../tools/detect-env.py) (tooling only). The `/resume` adopter-path currently decides "already onboarded?" by an assistant file-presence check on the adopter onboarding config; the config is machine-consumed (`sibling_choice` drives the sibling model) but the decision was prose, not tool-driven. This adds the mechanical backstop the resume prose already anticipated.

### Added
- [`tools/detect-env.py`](../../tools/detect-env.py) `_adopt_config_status()` + an `ADOPT_CONFIG` path constant and `VALID_SIBLING_CHOICES = ("own-siblings", "self-contained")`: parses the adopter onboarding config and returns `(present, valid)`, where valid requires parseable JSON with `mode == "adopter"` AND a recognized `sibling_choice` (the schema the adopt SKILL step 6 writes). `probe_identity` now emits `adopt_config_present` and `adopt_config_valid` in the identity block, and the human-readable output gains an Adopt-config line. **Additive: the origin/operator classification logic is untouched** (an unparseable / wrong-mode / bad-choice / non-object config is present-but-invalid; absent is `(False, None)`).
- [`tests/test_linters.py`](../../tests/test_linters.py) 5 new `DetectEnvIdentityTests` methods: absent -> `(False, None)`; both valid `sibling_choice` values -> `(True, True)`; malformed JSON -> `(True, False)`; wrong/missing mode, bad/missing choice, and non-object -> `(True, False)`; and `probe_identity` emits both fields with classification unchanged. Monkeypatch `ADOPT_CONFIG` to a temp file, save/restore.

### Changed
- [`TODO.md`](../../TODO.md) §3.92: part (a) tool-side SHIPPED annotation; the protected resume-command consumer edit staged (deferred item 13); parts (b)/(c) remain, §3.92 stays open.
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 13 stages the resume-command step-3 rework to drive the adopter-path off the emitted flags (same three outcomes; only the fact-source moves from assistant-inference to tool-output), and drops the now-shipped "queued hardening TODO §3.92" parenthetical.

### Verification
- `python3 -m unittest tests.test_linters.DetectEnvIdentityTests`: 16/16 (11 existing + 5 new). `detect-env.py --json` emits the two fields, classification `maintainer` unchanged, rc 0. All 72 gates pass; changelog preflight clean; pre-push guard both runners green; a refute-briefed skeptical verifier pre-push.
- Batches PR #1015's `/validate-pr` (validate-pr-1015, offloaded) and `/retro` rows.

### Discipline observation
- Additive, no-live-session-risk choice: the environment probe runs only at the next `/resume`, and the change adds fields without touching classification, so it carries no risk to the active session's coordination (unlike editing the in-session-used credit-offload queue tool). The resume consumer defers cleanly (staged), the same part-a-ships / part-b-stages pattern as §1.15a.

## 2026-07-18, Library Version 2026.07.503, PR #1015

Audit gate 72 (Citation-currency-cadence audit), TODO §1.14 Layer A (tooling; the spec is the only corpus doc touched, for its gate inventory). The canonical-citations register carries a `Last verified (UTC)` date per source (the SR-1 field: present but inert). This egress-free gate mechanizes it, warning when a source has drifted past its per-trust-tier re-check window, the TIME axis of currency, complementing gate 6 (version axis) and gate 5 (enumeration axis). Designed from the offloaded `seed-114` research seed (worker-a), re-authored by the orchestrator.

### Added
- [`tools/lint-citation-currency-cadence.py`](../../tools/lint-citation-currency-cadence.py) (gate 72): a table-aware register parser (handles the 7-column standard and 8-column AI-tooling schemas; `Last verified (UTC)` is the last cell in both), a dual date-format parser ("verified YYYY-MM-DD" and bare "YYYY-MM-DD"), a heading-to-trust-tier map over all 19 register sub-tables, and per-tier windows (legislation 180d, standards + frameworks 365d, datasets + tooling 90d). ADVISORY (WARN) mode: prints findings, always exits 0. Egress-free (pure date arithmetic; no network). 175 rows all within window at merge.
- [`tests/test_linters.py`](../../tests/test_linters.py) `CitationCurrencyCadenceTests` (4): fresh-row-passes; past-window-row-warns-but-exit-0; both-date-formats-detected; live-register-within-windows (guard-first, green on HEAD). Monkeypatches `CANONICAL_REGISTER` and `_today_utc` (fixed date) with save/restore for determinism and isolation.

### Changed
- Four-surface wiring (gate 72): [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh), [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml), and [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (§5 group-3 "Content drift defence" membership + clause, §6 inventory row 72, §6 detailed "Gate 72 is ..." paragraph). Spec Version 1.17.10 to 1.17.11 (body change); [`taxonomy.yml`](../../taxonomy.yml) + [`docs/portal.md`](../../docs/portal.md) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first).
- Gate-count ripple 71 to 72: [`TODO.md`](../../TODO.md) §3.89-adjacent parity line "71/71/71/71 as of gate 71" to "72/72/72/72 as of gate 72"; gate 39 (count consistency) green, and a proactive bare-token grep across all file types confirmed zero stale "71" gate-count residuals.
- [`TODO.md`](../../TODO.md) §1.14: Layer A SHIPPED annotation; §1.14 stays open for Layer B (egress upstream sweep, deferred, DD-10).
- [`.working/pending-decisions.md`](../pending-decisions.md): a PROCEEDED / stricter-safe-default morning-review entry logs the authorial choices (per-tier windows + WARN-vs-FAIL = WARN) for maintainer confirm-or-redirect.

### Design decisions (logged for maintainer confirmation)
- **WARN mode, deliberately (not a soft rollout).** The register's own version-currency-cadence note establishes that a hard gate would fail whenever egress is blocked (an environment condition). A staleness check inherits that: a row goes stale precisely because it could not be re-checked upstream, so blocking a merge on staleness would penalize the environment. Flipping any tier to FAIL is a one-line change once the maintainer confirms an egress-aware exemption.
- **Per-tier windows are conservative stricter-safe defaults, dormant today** (all 175 rows verified within ~18 days, so none is near any window >= 90d); they only bite as rows age, by which point the maintainer's confirmation applies.
- Scope: all 19 register sub-tables including the 8-column AI-tooling table (90d, fastest-moving). Layer B (upstream fetch) stays deferred: egress-required, a separate scheduled sweep, never this read-only lint CI.

### Verification
- All 72 audit gates pass (gate 39 count consistency confirms the 72-ripple; gate 35 four-surface parity 72/72/72/72; gate 64 §6 detailed-prose presence; gate 36 regression suite includes the new tests). Changelog preflight clean; pre-push guard both runners green; a refute-briefed skeptical verifier pre-push.
- Batches PR #1014's `/validate-pr` (validate-pr-1014, offloaded worker-b, CLEAN) and `/retro` rows.

### Discipline observation
- Research-assistant discipline: the gate design was offloaded (`seed-114`, worker-a) and re-authored, not pasted; the seed's schema survey (174 rows, all `last_checked` populated, no cadence field) and guard-first analysis were independently re-verified against the live register (the gate found 175 rows, reconciling the seed's 174 by surfacing a 19th sub-table "Soft-law supervisory guidance" the seed's heading count missed, which the orchestrator then mapped explicitly).

## 2026-07-18, Library Version 2026.07.502, PR #1014

Maintainer-requested overnight prep-drafts for the §1.19 operational-state privatization work (working-state only; no corpus change). The maintainer directed, at the overnight transition, that the §1.19.12/13 (and §1.18) drafts be prepared during the overnight run so the daytime apply is quick. This PR lands those drafts and stages the QA-completion codification.

### Added
- [`.working/claudemd-trim-review-draft.md`](../claudemd-trim-review-draft.md) (§1.19.12, Phase 5 MAINTAINER ACTION): a sensitivity-classification worklist over CLAUDE.md's 30 sections (2 MOVE / 15 KEEP / 13 SPLIT, broad-trim lean), with the sensitive part named for each SPLIT and the maintainer strictness-decision points. Seeded by the offloaded `seed-119-12-claudemd-trimlist` research order (worker-20260716-b) and orchestrator-re-authored + spot-checked against the live CLAUDE.md structure (research-assistant discipline). A discussion input, NOT an applied trim.
- [`.working/history-scrub-procedure-draft.md`](../history-scrub-procedure-draft.md) (§1.19.13, Phase 6 maintainer-gated): the force-push git-history-scrub procedure, with a precondition gate (§1.19.8/9 merged; no live path references; full clone), the worklist (= the §1.19.8 move-list), the artefact-and-branch-discipline steps (`git filter-repo --invert-paths`, `refs/preservation/`, version-monotonicity re-run, verify-purge), and a residual-risk note.
- [`.working/change-impact-surface-map-draft.md`](../change-impact-surface-map-draft.md) (§1.18, first-pass scope): per-change-type surface maps (new gate / new pack rule / new skill / count change), the existing-partial-coverage fold-in (gates 35/39/37, D6), the D8 worked example, and open scoping questions for the maintainer.

### Changed
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): new item 12 stages the protected apply of the QA-activity completion standard (a `## QA-activity completion standard` CLAUDE.md subsection + the portable pack-rule half in `ai-assistant-workflow-disciplines`); the durable form already landed in the orchestrator memory.
- [`TODO.md`](../../TODO.md) §1.19.12 / §1.19.13 / §1.18: each annotated with a PREP pointer to its draft (still held for attended apply).
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md): the `seed-119-12` research seed recorded as delivered + consumed (~70K, worker-b), and validate-pr-1013 (~110K, worker-b routine) added to the 2026-07-17b roll-up.

### Verification
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green (71 gates); changelog preflight clean. Working-state + CHANGELOG + README + TODO only; no corpus, no `.web/`, no generated artefact.
- Batches PR #1013's `/validate-pr` (validate-pr-1013, offloaded worker-b, CLEAN, 7 empirical repo-guard exit-path tests) and `/retro` rows.

### Discipline observation
- Credit-offload: the §1.19.12 trim-list was OFFLOADED as a research seed (worker-b, `seed-119-12`) and re-authored at apply per the research-assistant discipline (the worker's classification is a hypothesis; the orchestrator's verdicts are after checking each section). This is the intended research-stage-parallel / apply-stage-serial shape.
- No protected file was edited: all four privatization payloads are `.working/` drafts or staging entries; the protected CLAUDE.md + pack applies (deferred items 11 and 12) remain for the daytime attended run.

## 2026-07-18, Library Version 2026.07.501, PR #1013

Cross-repo write-safety guard, TODO §1.15a part (a) (tooling + working-state only; no corpus change). The maintainer-orchestrator works across colocated repos (`grc_library`, `grc_library_ref`, `grc_library_scratch`, `grc_library_private`) and the `Bash` tool persists a `cd` across calls, so a cwd-dependent repo-mutating git command can silently target the wrong repository (observed 2026-07-15: a `grc_library`-intended `git checkout main && git pull` ran in `grc_library_scratch`). This PR ships the mechanical half.

### Added
- [`tools/repo-guard.sh`](../../tools/repo-guard.sh): a fail-loud wrapper, `tools/repo-guard.sh <expected-repo-basename> -- <command...>`. It refuses (exit 3, command NOT run) when `git rev-parse --show-toplevel`'s basename does not match the asserted repo, or when the cwd is not inside a git work tree; on a match it `exec`s the command, so the command's own exit code passes through. Exit 2 on usage error (missing assertion, missing `--`, empty command). It is a utility wrapper, NOT an audit gate: not wired into `run_all_audits.sh`, never runs in CI.
- [`tests/test_linters.py`](../../tests/test_linters.py) `RepoGuardTests`: three cases (match runs and passes the command's exit code through; mismatch refuses without running, verified by a sentinel file that must NOT be created; usage errors exit 2).

### Changed
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 11 stages part (b), the protected project CLAUDE.md convention line (confirm the target repo before every Write/Edit and every repo-mutating git command; route git sequences through the wrapper or an explicit `cd`), for the daytime apply. Also a stale-number note on item 9 (its "gate 70 / 69-to-70" figures predate gates 70/71; the applier recomputes to gate 72 / 71-to-72).
- [`TODO.md`](../../TODO.md) §1.15a: annotated part (a) SHIPPED, part (b) STAGED; §1.15a closes when part (b) applies.

### Fixed
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): corrected the PR #1012 detailed entry, which credited "upstream CanLII"; the independent validate-pr-1012 re-verification showed CanLII returned a 403 bot-challenge and LégisQuébec (HTTP 200) is the confirming upstream source.

### Verification
- Manual path testing of `repo-guard.sh`: match (exit 0, command ran, exit code passed through), mismatch (exit 3, command NOT run), not-in-work-tree (exit 3), usage errors (exit 2). `RepoGuardTests` 3/3 pass in the linter-regression suite.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green; a pre-push skeptical verifier on the diff.

### Discipline observation
- Recursion-avoidance: this PR batches PR #1012's `/validate-pr` (validate-pr-1012, offloaded, CLEAN, independently confirming the Quebec Law 25 s. 3.3 escalation at held source + upstream LégisQuébec) and `/retro` rows.
- Credit-offload: the §1.19.12 CLAUDE.md trim-list was dispatched as a research seed to worker-b (`seed-119-12-claudemd-trimlist`) during this PR; consumed and re-authored in the next PR (§1.19.12/13 prep-drafts).

## 2026-07-18, Library Version 2026.07.500, PR #1012

Quebec Law 25 citation-accuracy escalation (working-state only; no corpus change). The §3.84 attempt to "correct" the Quebec Law 25 PIA citation "3.3" -> "23.3" was ABANDONED (not merged) when its pre-push skeptical verifier proved the premise INVERTED: **s. 3.3 is the correct in-force PIA-duty section**; "23.3" does not exist in P-39.1 (ss. 23/24 are the public-sector Act A-2.1). The held reference source's "23.3." header is PDF margin-note corruption (a stray digit from the rotated "2021, c. 25" annotation). Confirmed by the statute's own s. 3.4 cross-reference to "section 3.3", the clean alternating header series (3.2/3.4/3.6), and upstream LégisQuébec (the official Quebec-government source, fetched HTTP 200 by the offloaded validate-pr-1012; CanLII returned a Cloudflare bot-challenge 403 and did not contribute). (Correction, PR #1013: this entry originally credited "upstream CanLII"; the independent re-verification showed CanLII 403'd and LégisQuébec is the confirming source.) This fooled both the earlier orchestrator re-verification and the #973 worker QA.

### Changed
- [`.working/pending-decisions.md`](../pending-decisions.md): a HIGH/ESCALATION morning-review item records the finding, the SHIPPED "s. 23.3" error in [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md) lines 30 + 60 (from PR #973), the corrupted-source root cause, and the recommended maintainer-gated remediation (revert the annex to "s. 3.3" + re-ingest a clean source); §2.22 Canada apply is DEFERRED (blocked on this).
- [`TODO.md`](../../TODO.md): §3.84 rewritten with the reversed premise (the 3 target docs correctly read "3.3" on main and are left as-is; the real error is the #973-shipped annex "23.3", maintainer-gated); new §3.100 to re-ingest a clean Quebec Law 25 P-39.1 source (the held PDF extract has margin-note-corrupted headers).

### Verification
- The correct section (3.3) was confirmed at the held statute's OWN running text (s. 3.4 body references "section 3.3"; the section after the PIA duty is header "3.4", not "23.4") plus the verifier's upstream CanLII check. The §3.84 corpus edits were reverted (the branch abandoned); `main`'s three §3.84 docs are unchanged at "3.3".
- **#1011 QA batch (recursion-avoidance) carried here:** the validate-pr-1011 SHIP row + the retro-1011 row.
- Working-state only; no corpus, pack, tooling, or website content changed. Pre-push guard green.

### Discipline observation
- A held PDF-extract header can be corrupted; two separate held-source verifications (the #973 worker + the orchestrator's own §3.84 re-verification) were fooled by reading the corrupted "23.3." header at face value. The catch came from the skeptical verifier cross-checking the statute's INTERNAL cross-references + the upstream source, not the extracted header. Lesson folded into §3.100 and the retro.

## 2026-07-18, Library Version 2026.07.499, PR #1011

Sibling-reaching advisory-tool graceful degradation (TODO §3.91) + check-portability scope note (TODO §3.90). Assessed all six maintainer-cadence tools that reach `grc_library_ref` for adopter portability; three crashed on an absent reference base and were fixed, the other three already degraded.

### Changed
- Graceful no-op exit 0 on an absent DEFAULT reference base (adopter clone), added to [`tools/audit-reference-breadth.py`](../../tools/audit-reference-breadth.py), [`tools/audit-reference-acquisition-gaps.py`](../../tools/audit-reference-acquisition-gaps.py), and [`tools/scan-publication-instruction-content.py`](../../tools/scan-publication-instruction-content.py) (each previously raised `RuntimeError`). The guard fires only for the default ref-base with no override; an explicit `--ref-base`/`--files` still proceeds and errors on a typo (typo guard preserved). Already-graceful (unchanged): `audit-claim-precision`, `verify-reference-modules`, `audit-register-currency` (SKIP / advisory exit 0).
- [`tools/check-portability.sh`](../../tools/check-portability.sh): all six tools added to the degradation loop; the header documents the relative-clone scope (§3.90: an absolute-path sibling-reach is out of this loop's scope, covered by each tool's own explicit-path handling).

### Verification
- All six tools confirmed to no-op exit 0 in a sibling-free clone and to proceed normally with `_ref` present (the fixed three re-verified both ways). `check-portability.sh` re-run post-commit. All 71 gates green; pre-push guard PASS.
- Ground-truth-first: each tool was RUN sibling-free before editing (evidence, not inference); the §3.91 item's full six-tool enumeration was used, not the check-portability header's partial three-tool list.
- **#1010 QA batch (recursion-avoidance) carried here:** the validate-pr-1010 SHIP row + the retro-1010 row.
- Tooling only; no corpus, pack, or website content changed.

## 2026-07-18, Library Version 2026.07.498, PR #1010

Gate 61 external-path robustness guard (TODO §3.98, deep-assessment r5 Low-3). A cosmetic-only nit: the findings-print loop of [`tools/lint-cobit-iso31000-citations.py`](../../tools/lint-cobit-iso31000-citations.py) called `path.relative_to(REPO_ROOT)` unguarded, which raises `ValueError` on a target outside the repo (a hand-invocation with a finding). Never triggered in the runner/CI (always repo-relative), but fixed for robustness.

### Changed
- [`tools/lint-cobit-iso31000-citations.py`](../../tools/lint-cobit-iso31000-citations.py): added a `_display_path` helper (try `relative_to(REPO_ROOT).as_posix()`, fall back to the absolute POSIX path on `ValueError`) and used it in the findings-print loop.

### Added
- A `test_display_path_guards_external` regression test in [`tests/test_linters.py`](../../tests/test_linters.py) (`CobitIso31000CitationsTests`): in-repo path renders relative, an out-of-repo path renders absolute with no `ValueError`. (The synthetic module load registers the module in `sys.modules` so its `@dataclass` annotations resolve under Python 3.14, and de-registers it in a `finally`.)

### Verification
- All 71 audit gates pass; gate 61 still clean on HEAD; the new test passes. Pre-push guard green.
- **#1009 QA batch (recursion-avoidance) carried here:** the validate-pr-1009 SHIP row + the retro-1009 row.
- Tooling only; no corpus, pack, or website content changed.

## 2026-07-18, Library Version 2026.07.497, PR #1009

Gate 71, the stdlib-only import audit (TODO §3.95, maintainer-approved). Closes the blind spot that let #1006's generator ship `import yaml` and fail only in CI: `check-portability.sh` clones sibling-free but runs under the maintainer's Python, so it tests sibling-ABSENCE, not the stdlib-only environment. The corpus now runs **71** audit gates.

### Added
- [`tools/lint-stdlib-only-imports.py`](../../tools/lint-stdlib-only-imports.py) (gate 71): AST-parses every runnable-toolchain Python file (`tools/`, `tests/`, `.web/`) and fails any imported ROOT module not in `sys.stdlib_module_names`, not a first-party in-repo module (the stem of a scanned `.py`, e.g. `lint_common` or the reference modules), and not in the explicit `ALLOWED_THIRD_PARTY` allow-list (empty; the toolchain is pure stdlib). Static AST (not grep) sees the real import graph incl. lazy imports. Runs inside `run_all_audits.sh`, so it catches a third-party import at every commit, earlier than CI. Sanctioned exception = an `ALLOWED_THIRD_PARTY` entry with a rationale (gate-discipline exception pattern).
- `StdlibOnlyImportsTests` (4) in [`tests/test_linters.py`](../../tests/test_linters.py): flags a third-party import (top-level + lazy + from-import), passes stdlib + first-party sibling imports, and asserts the live HEAD tree is clean; the temp-tree tests save/restore `REPO_ROOT` (test isolation).

### Changed
- Four-surface wiring: [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh), [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml), and the [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 inventory table (row 71) + §6 detailed prose (the gate-71 paragraph) + §5 grouped list (added to group 5, "Programme and index integrity"). Parity re-derives to 71/71/71/71 (gate 35).
- [`TODO.md`](../../TODO.md): §3.95 closed (rotated to [`DONE.md`](../DONE.md)); §3.99's parity-count updated to 71/71/71/71.

### Verification
- All 71 audit gates pass (gate 71 green on HEAD: 111 toolchain files, all stdlib/first-party). Regression suite includes `StdlibOnlyImportsTests` 4/4. `check-portability.sh` re-run post-commit (gate 71 needs no siblings; it degrades cleanly / runs green sibling-free). A gate-20 (mandatory-verb-near-uncertainty) false trip from a "must ... TODO" adjacency in the new §6 prose was reworded to declarative before the suite went green.
- **#1008 QA batch (recursion-avoidance) carried here:** the validate-pr-1008 SHIP row + the retro-1008 row.
- Tooling only; no corpus, pack, or website content changed. Pre-push guard green.

## 2026-07-18, Library Version 2026.07.496, PR #1008

Records the **deep-assessment r5** offloaded read-only probe pass (worker `worker-20260716-a`, pinned `a42a2a0b` / #1006) and routes its findings (Phase 7). The clean phases: mechanical baseline 70/70 + 412 regression tests, blind-spot map 0, mutation probe 15/0/5/0 (disposable clone), four-surface parity 70/70/70/70, reference modules match held source, full-history secret scan + PII watermark clean, 809-row QA-ledger meta-audit honest. Finding set (orchestrator-re-verified at source): 2 confirmed corpus (1 Medium, 1 Low) + 5 Low informational/tracked/robustness; **no High**. Phase 8 HOLDS for maintainer sign-off.

### Added
- [`.working/deep-assessment/2026-07-18-r5.md`](../deep-assessment/2026-07-18-r5.md): the r5 per-run detail (findings, orchestrator source-re-verification, clean-surface proof-of-run).
- [`TODO.md`](../../TODO.md) §3.98 (gate-61 `ValueError` guard, r5 Low-3) and §3.99 (parity-gate exclusion allow-lists + PR-only delta gates unguarded, r5 Low-4).

### Changed
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): r5 row added (Status in-progress, P7 routing this PR, P8 holds for sign-off) + the r5 per-run paragraph.
- [`.working/pending-decisions.md`](../pending-decisions.md): a `## MORNING-REVIEW PENDING (2026-07-18 overnight run)` section carries the r5 sign-off hold and the Medium-1 CSA CCM SEF-02 remap decision (recommend SEF-07 "Incident Management and Response"; NOT applied unattended, a semantic-fit call on an expert-review-facing table).
- [`TODO.md`](../../TODO.md) §1.16: noted the 3 additional COBIT carriers (APO02/07/11) + a DSS02 instance r5 confirmed (Low-1 folds in; the corpus-wide re-derive covers them, recount at build).

### Verification
- The two corpus findings re-verified at source by the orchestrator: SEF-02 corpus line verbatim at `security/sop-incident-escalation-matrix.md:97`; held SEF-02 title = "Service Management Policy and Procedures" (CCM CSV:601); gate count re-derived = 70. The worker's proof-of-run is genuine (path:line, disposable-clone mutation probe, SHA-reachability ladder), so the clean/zero-finding results are trusted (routine-consume + positives-re-verified).
- **#1007 QA batch (recursion-avoidance) carried here:** the validate-pr-1007 SHIP row and the retro-1007 row.
- Working-state only; no corpus, pack, tooling, or website content changed. Pre-push guard green.

## 2026-07-18, Library Version 2026.07.495, PR #1007

§1.19.7 (c) the `/adopt` `.ref` bootstrap, completing the `_ref`-integration umbrella (the last §1.19 Phase-1 item; parts (a)+(b) shipped in #1006, the `_ref`-required loud gate in #1005, the `_ref` `acquisition` field in `grc_library_ref` #88). Also closes §1.12 (subsumed) and §3.18 (maintainer-decided), and queues three follow-ups surfaced by the #1006 fix.

### Added
- [`tools/adopt-bootstrap-ref.py`](../../tools/adopt-bootstrap-ref.py): a stdlib-only, network-free, write-free planner. It reads the committed public [`docs/reference-acquisition-manifest.md`](../../docs/reference-acquisition-manifest.md) and categorizes the 632 trusted-bucket sources into **auto-fetchable** (FREE + an upstream URL), **free-manual** (FREE, no URL recorded), and **licensed-manual** (LICENSED); `--json` for the `/adopt` assistant to drive. It NEVER fetches, downloads, or writes (reads only bibliographic metadata), so the network + write side and the copyright boundary stay in the human-in-the-loop assistant layer. Adopter-portable: reads only the in-repo manifest, so it runs on a bare clone with no siblings. Live run: 8 auto-fetchable / 526 free-manual / 98 licensed-manual = 632.
- `AdoptBootstrapRefTests` (3) in [`tests/test_linters.py`](../../tests/test_linters.py): manifest-table parse + three-way categorization; render carries the guardrail; a missing manifest returns exit 2.

### Changed
- [`dev-security/claude-rules/skills/adopt/SKILL.md`](../../dev-security/claude-rules/skills/adopt/SKILL.md) step 4 concretized: the own-siblings bootstrap now drives from the planner's categorized plan (WebFetch each auto-fetchable source INTO the adopter's EXTERNAL `grc_library_ref`, list the free-manual + licensed-manual for manual acquisition), with the copyright guardrail explicit (only FREE auto-fetched; LICENSED never redistributed; never the in-repo `.ref` stub). The Project-wiring bullet names the planner. Pack README [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md) `1.62.0` to `1.62.1` (patch) + a `## Version history` row (D6).
- [`TODO.md`](../../TODO.md): **§1.19.7 closed** (rotated to [`DONE.md`](../DONE.md)); **§1.12 closed** (part 2 done by D8, part 1 subsumed by §1.19.10's weekly collapse, maintainer-confirmed); **§3.18 closed** (maintainer decided publications stay excluded from `/reference-audit` until screened); added **§3.95** (stdlib-only import gate), **§3.96** (test-isolation `mock.patch` convention), **§3.97** (`grc_library_ref` `upstream_url` enrichment for FREE entries).

### Verification
- All 70 audit gates pass; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green. `AdoptBootstrapRefTests` 3/3. [`tools/lint-language.py`](../../tools/lint-language.py) clean on the new pack prose (run before first commit).
- The planner is stdlib-only (`argparse`, `json`, `re`, `sys`, `pathlib`) and does not reach a sibling (it reads the committed in-repo manifest), so it needs no `check-portability` degradation entry; it runs green sibling-free.
- **#1006 QA batch (recursion-avoidance) carried here:** the validate-pr-1006 SHIP row ([`.working/validate-pr/history.md`](../validate-pr/history.md)) and the retro-1006 row ([`.working/improvement-log.md`](../improvement-log.md)), plus the credit-offload-metrics validate-pr-1006 row. validate-pr-1006 was a CLEAN PASS (worker-b routine consume; a full 632-row classification cross-check, 0 mismatch).
- A refute-briefed skeptical verifier ran pre-push on the planner + SKILL diff.

### Notes
- Most FREE trusted-bucket sources lack a recorded `upstream_url` (only 8 of 534, all legislation), so the auto-fetchable set is small; §3.97 tracks the `grc_library_ref` `upstream_url` enrichment that would grow it.

## 2026-07-17, Library Version 2026.07.494, PR #1006

The §1.19.7 reference-acquisition manifest: the grc_library half of the `_ref`-integration umbrella (the `_ref` `acquisition` field landed in `grc_library_ref` PR #88). A generator produces a public bibliography of the corpus's citation-source reference base, so a fork can acquire what the corpus cites. Only (c) the `/adopt` `.ref` bootstrap remains in §1.19.7 (its own PR); §1.19.7 stays open.

### Added
- [`tools/build-reference-manifest.py`](../../tools/build-reference-manifest.py) - reads `grc_library_ref`'s trusted-bucket catalogue (standards/frameworks/legislation/programs) + the `acquisition` field and writes the committed manifest. `lint_common.resolve_sibling("ref")`-guarded: it no-ops (exit 0) when `_ref` is absent (an adopter's portable clone), so it is NEVER a CI gate and the sibling-independence invariant holds. Copyright guardrail: reads only catalogue bibliographic metadata (title/issuer/version/url/acquisition), never the held `--full-text` files. `--check` is the maintainer-side drift check. Emits a 13-field metadata block + a `## Overview` orientation section (so the generated docs/ file satisfies the metadata and required-sections gates as the other generated docs do); Version is a schema constant, Date is the reference base's max currency date (deterministic, so `--check` is stable).
- [`docs/reference-acquisition-manifest.md`](../../docs/reference-acquisition-manifest.md) - the generated public bibliography: 632 trusted-bucket sources (534 FREE / 98 LICENSED), grouped by bucket. Worker-drafted classification (research seed `manifest-1197-draft`), orchestrator-re-verified with the FFIEC/PCI/CMU-SEI over-calls corrected LICENSED->FREE.
- [`tests/test_linters.py`](../../tests/test_linters.py) - `ReferenceManifestGeneratorTests`: `render()` output shape (metadata block, `## Overview`, deterministic Date, row acquisition class, total) + sibling-free graceful degradation (main() returns 0 for default and `--check`).

### Changed
- Generated-artefact exemptions for the new `docs/` file, matching how the existing generated docs are handled: [`tools/lint-language.py`](../../tools/lint-language.py) (`GENERATED_DOCS`), [`tools/lint-metadata.py`](../../tools/lint-metadata.py) (`PREFIX_EXEMPT_BASENAMES` for the doc-type-prefix check; the 13-field block is emitted, not exempted), [`tools/lint-acronym-consistency.py`](../../tools/lint-acronym-consistency.py), [`tools/lint-external-link-domains.py`](../../tools/lint-external-link-domains.py) (the issuer URLs are not allow-list-bound), [`tools/lint-orphan-documents.py`](../../tools/lint-orphan-documents.py) (reached by `/adopt` + purpose), [`tools/lint-version-bump-recency.py`](../../tools/lint-version-bump-recency.py) + [`tools/lint-document-date-staleness.py`](../../tools/lint-document-date-staleness.py) (the manifest content advances with the reference base, not per grc_library PR).
- [`tools/check-portability.sh`](../../tools/check-portability.sh) - the generator joined the sibling-reaching-tool degradation loop (asserts it no-ops exit 0 in a sibling-free clone).
- [`TODO.md`](../../TODO.md) - §1.19.7 (a)/(b) marked SHIPPED; only (c) `/adopt` bootstrap remains, so §1.19.7 is NOT closed.

### Verification
- All 70 audit gates pass with the new generated `docs/` file (the 5 content gates it initially tripped, metadata / language / acronym / external-link / orphan, plus required-sections, resolved by the emitted metadata block + `## Overview` and the generated-artefact exemptions).
- `ReferenceManifestGeneratorTests` 3/3 OK; the degradation test proves `main()` returns 0 sibling-free, and a `_parse_catalogue` test locks the stdlib parser (below).
- **CI caught a stdlib-only violation** (a second pre-merge catch): the generator originally `import yaml`ed to read the reference catalogue, but the audit toolchain is stdlib-only and CI has no PyYAML, so the regression suite errored `No module named 'yaml'`. `check-portability` did not catch it (it tests sibling-ABSENCE, not the stdlib-only environment; the local Python has PyYAML). Replaced with a minimal stdlib `_parse_catalogue` (the catalogue's shape is fixed and regular), including YAML double-quote unescape so `\"` resolves to `"` (verified byte-identical to the prior `yaml.safe_load` output via `--check` zero-drift, and confirmed to load + parse + render with `yaml` blocked to mimic CI).
- `check-portability.sh` confirms the generator degrades gracefully (verified post-commit, since it clones the committed HEAD). The post-commit run also CAUGHT a test-isolation regression: `test_degrades_when_ref_absent` monkeypatched the shared `lint_common.resolve_sibling` without restoring it, and because `ReferenceManifestGeneratorTests` sorts before `ResolveSiblingTests`, the pollution made 3 later `ResolveSiblingTests` fail sibling-free (origin/main passed the identical clone, isolating it as this PR's regression). Fixed by save/restore in the test's `finally`; both classes now pass in the polluting order (differential-clone verification).
- Recursion-avoidance batch: PR #1005's `/validate-pr` and `/retro` rows are carried here.
- No corpus document body changed; the one new `docs/` file is a generated artefact. Pre-push guard green.

## 2026-07-17, Library Version 2026.07.493, PR #1005

The §1.19.7 `_ref`-required loud gate (maintainer-directed 2026-07-17). Reference-checking against the held ground truth in `grc_library_ref` is critical to the maintainer-orchestrator's content work, so a missing `_ref` must FAIL LOUD and be fixed, not be silently worked around. Graceful degradation of the sibling-reaching tools (`lint_common.resolve_sibling` no-op, §1.19.2) was designed for the ADOPTER portability case; for the maintainer it would mask a broken dependency (the drift/hallucination risk `_ref` exists to prevent). The gate is identity-keyed off `detect-env`'s existing maintainer/adopter classification, so it adds the loud maintainer-side check WITHOUT weakening the sibling-independence invariant (adopters stay graceful; `check-portability.sh` + gate 70 unaffected). This is the loud-gate part of the §1.19.7 `_ref`-integration umbrella; the manifest/generator/`acquisition`-field parts remain open, gated on the worker manifest draft, so §1.19.7 is NOT closed.

### Added
- [`tools/detect-env.py`](../../tools/detect-env.py) - a `ref_availability_decision(classification, ref_readable)` helper and a `ref_availability` entry in the resume-step decisions: `maintainer` + `_ref` unreadable -> `HALT (LOUD)`; `maintainer-fresh-machine` + `_ref` unreadable -> "clone `_ref` first"; `adopter` + `_ref` absent -> "ok (graceful, expected)"; `_ref` readable -> "ok"; and an unknown/undetermined classification -> `HALT (LOUD)` fail-safe (never silently takes the adopter graceful path, correct-by-construction if the closed `probe_identity` set ever changes). Never crashes the resume step (inside the existing try/except).
- [`tests/test_linters.py`](../../tests/test_linters.py) - 5 `DetectEnvIdentityTests` cases for `ref_availability_decision` (maintainer-halts-loud, fresh-machine-clone-first, adopter-graceful, readable-ok-for-all, unknown-identity-fails-safe-loud).

### Changed
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md) - step 3 now acts on the `ref_availability` decision: on a `HALT (LOUD)` it STOPS and surfaces the `--add-dir` fix, with no reference-dependent (content) work until `_ref` access is granted and the session re-resumed. Distinguished explicitly from the adopter graceful-degradation path.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) - a `_ref`-is-a-required-maintainer-dependency principle added to `## Reference-version currency` (fails loud for the maintainer; graceful is adopter-only).
- [`TODO.md`](../../TODO.md) - §1.19.7 rewritten as the `_ref`-integration umbrella (scope = trusted buckets; the `acquisition` field as source-of-truth in `_ref`; the generator + drift-check + `/adopt` bootstrap; this loud gate marked SHIPPED); NOT closed (manifest parts pending the draft).

### Verification
- `python3 -m unittest tests.test_linters.DetectEnvIdentityTests` 11/11 OK (6 existing + 5 new); the detect-env probe runs and emits `ref_availability: ok (grc_library_ref readable)` in this maintainer session.
- A refute-briefed skeptical verifier reviewed the gate (the decision logic, the resume hard-halt, and that the adopter graceful path / sibling-independence is preserved).
- Recursion-avoidance batch: PR #1004's `/validate-pr` and `/retro` rows are carried here.
- No corpus document or generated artefact touched. Pre-push guard green.

## 2026-07-17, Library Version 2026.07.492, PR #1004

Website fix (maintainer-flagged, not critical): on the For-AI page the hero heading "Learning governance and security from this corpus." overflowed the coloured hero band on the maintainer's iPad, the "ty" of "security" spilling into the next section. Cause: the heading ([`.web/templates/for-ai.html`](../../.web/templates/for-ai.html)) joins "Learning governance and security" with `&nbsp;` into one unbreakable ~31-character token, which defeats the `.hero h1` `max-width: 18ch` + `text-wrap: balance` wrapping, so at tablet width the token, sized by the `font-size: clamp(2.15rem, 5.6vw, 4rem)`, rendered wider than the padded band and overflowed. Fix per maintainer direction (decrease the hero heading size): lower the clamp's `vw` term and floor so the token fits at tablet widths, leaving the `4rem` desktop cap unchanged.

### Changed
- [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) - `.hero h1` font-size `clamp(2.15rem, 5.6vw, 4rem)` to `clamp(1.7rem, 4.3vw, 4rem)`. The reduction is concentrated on tablet and narrow widths (where the overflow occurred); the desktop cap stays `4rem`, so wide screens are visually unchanged. Shared `.hero h1` rule, so every hero page inherits the slightly-smaller tablet heading.

### Notes
- The underlying `&nbsp;`-defeats-`max-width:18ch` interaction (which also affects very narrow phone widths) is NOT changed here, to keep the fix to the maintainer's stated remedy (font-size) without altering the heading's line-break design. If the maintainer wants the heading to wrap into the intended narrow balanced block instead, removing the intra-phrase `&nbsp;` is the follow-up.
- Verified visually on the maintainer's device pending (the orchestrator cannot render the iPad viewport); the clamp reduction gives comfortable margin at 768 to 1024 CSS px by calculation.

### Verification
- `python3 .web/build.py --check` rc 0; the new clamp `clamp(1.7rem, 4.3vw, 4rem)` is present in the built pages and the old value is gone (0 residual).
- `.web/dist` is gitignored (Cloudflare rebuilds from the template); the committed change is the shared style partial only.
- Recursion-avoidance batch: PR #1003's `/validate-pr` and `/retro` rows are carried here.
- No corpus document, generated artefact, or gate touched. Pre-push guard green.

## 2026-07-17, Library Version 2026.07.491, PR #1003

Codifies the "sync scratch every PR" discipline (TODO §3.93 parts (a) and (b)), the recurrence-prevention for a maintainer-flagged mistake that fired twice (2026-07-16 and again at this resume): the local `grc_library_scratch` checkout does not auto-sync, but the credit-offload reads (the `workers/` liveness registry, `queue/`, `results/`) operate on it, so a worker delivery pushed to scratch `origin/main` is invisible until the orchestrator fetches. At this resume that produced a wrong "both workers stale, Sweep-111 order unclaimed" report and a needless worker-restart ask, when worker-a had already delivered on `origin/main`. A dedicated memory already existed and did not prevent recurrence, so the fix is a forcing function in the standing surfaces rather than another note.

### Changed
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) - added the primary **sync-scratch-every-PR** bullet to the `## Session migration and PR close-out checklist` (fetch and hard-reset the scratch checkout to `origin/main` at every close-out, delivery pending or not), and an orchestrator **coordination-plane-read** bullet to the `## Credit-offload mode` section (fetch scratch before any `list-workers` / `list-pending` / `results/` read, and per-tick inside any poll loop; never characterize worker/queue/result state from an un-synced checkout).
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md) - the step-3 credit-offload check now fetches and hard-resets the scratch checkout before `list-workers` / `list-pending` / `results/`.

### Notes
- This is §3.93 parts (a) and (b) only. Part (c), the mechanical backstop that makes the scratch queue tool's read subcommands auto-fetch origin, is a separate `grc_library_scratch` PR (a cross-repo change), so **TODO §3.93 stays open** until (c) lands; not rotated to DONE.
- The behavioural fix is already in force this session (scratch is fetched before every coordination read); this PR makes it durable across sessions.

### Verification
- Recursion-avoidance batch: PR #1002's `/validate-pr` row (offloaded to worker-b, elevated-QA delivery 3, CLEAN PASS, clears the 2-to-3 floor to routine trust) and `/retro` row are carried here.
- No corpus document, generated artefact, or gate touched (a `.claude/` AI-guidance codification plus the QA batch); no per-document version bump needed. Pre-push guard green.

## 2026-07-17, Library Version 2026.07.490, PR #1002

Website fix (maintainer-flagged): the "For AI" and "Contributors" links appeared to vanish from the landing-page Contents sidebar. Diagnosis (evidence-grounded): both links are present in the live DOM (confirmed by fetching the live site, sidebar lines 527-528) and in a fresh [`.web/build.py`](../../.web/build.py) render, so nothing hides them. The cause is the sticky sidebar's viewport-height cap with inner scroll (`max-height: calc(100vh - 2.5rem); overflow-y: auto` at `min-width: 1080px`, in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html)): as the Contents nav grew (Get-started sub-links, 11 domain links, 6 Standards sub-groups across the recent website PRs) it now exceeds the viewport on typical laptops, so its last two entries (For AI, Contributors) scroll below the sidebar's inner fold. Per maintainer direction, the fix makes the For-AI page reachable independently of the sidebar rather than reworking the sidebar: add a "For AI" link to the site-wide footer, where "About and contributors" already lives.

### Changed
- [`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html) - added a `For AI` link (to `/for-ai/`) in the footer Project column, immediately before "About and contributors" (mirroring the sidebar's For AI then Contributors order). The footer is a shared partial, so the link now renders on all 32 full site pages.

### Verification
- [`.web/build.py`](../../.web/build.py) rebuilt 35 pages; the new footer link is present in all 32 full HTML pages (the other 3 generated outputs, robots.txt / sitemap.xml / llms.txt, carry no footer).
- The generator's `--check` mode returned rc 0 (corpus parses, every page renders).
- The generated site directory is gitignored (Cloudflare Pages rebuilds from the template at deploy), so the committed change is the template partial only.
- No corpus document, generated artefact, or gate touched, and no per-document version bump needed. The residual sidebar-overflow root cause is tracked as TODO §3.94. Pre-push guard green.

## 2026-07-17, Library Version 2026.07.489, PR #1001

Applies the deep-assessment r4 confirmed gate-blind citation-accuracy fixes (TODO §1.17), which the maintainer signed off at the 2026-07-17b `/resume`, together with the same-class Sweep 110 finding S110-1. All four are gate-blind: the citation, currency, and control-code gates validate that a source exists and a code is well-formed, not that the cited value is the right one. Each was re-verified at the held source, and a refute-briefed skeptical verifier checked the set before push.

### Changed
- [`dev-security/standard-api-security.md`](../../dev-security/standard-api-security.md) §7 (W1) - the TLS 1.3 cipher-suite cell no longer attributes `TLS_CHACHA20_POLY1305_SHA256` to NIST SP 800-52 Rev. 2 §3.3.1 (which enumerates only the AES-GCM/CCM suites); the two AES-GCM suites are cited to 800-52r2 and ChaCha20-Poly1305 is noted as an RFC 8446 AEAD suite not enumerated by 800-52r2. Version 0.0.10 to 0.0.11.
- [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md) §12 (N2 + W2) - the NIST CSF column's CSF 1.1-legacy subcategory IDs are remapped to CSF 2.0 (the library is pinned to 2.0) with a maintainer-confirmed best-fit + category-level-fallback mapping: `DE.CM-7` to `DE.CM-09` (log ingestion; and AI-assisted detection), `DE.CM-1` to `DE.CM` at category level (time synchronization has no 2.0 subcategory; ISO 8.17 is its anchor), `DE.CM-3, DE.CM-4` to `DE.CM-09, DE.AE-02` (alert rules), `RS.CO-1` to `RS.MA-02` (automated ticket creation), `RS.CO-3` to `RS.MA-04` (escalation, an exact 2.0 match); and the ISO/IEC 27002:2022 cell for time synchronization corrected from the non-existent `8.15.3` to `8.17` (Clock synchronization). Version 1.3.7 to 1.3.8.
- [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) §-framework-alignment (S110-1) - the NIST CSF 2.0 cell's `ID.AM-3, Software asset inventory` corrected to `ID.AM-02` (software inventory; `ID.AM-03` is network/data-flow representations), fixing both the wrong subcategory and the unpadded 1.1-style format. Version 1.1.6 to 1.1.7.
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) - regenerated after the three per-document Version bumps (taxonomy first, then the portal/scorecard derivation).
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md) - r4 Phase 8 and Status set to `signed-off` with the maintainer sign-off note; the remaining r4 candidates (W5, W6, N1/N3/N4-N12, the OSCAL-vs-CSWP-29 note) route to their trackers.
- [`TODO.md`](../../TODO.md) - §1.17 closed and rotated to [`DONE.md`](../DONE.md); the P1 count prose updated (eight to seven open items).

### Verification
- Each fix re-verified at held source: W1 against NIST SP 800-52 Rev. 2 §3.3.1; N2 against the held CSF 2.0 core (CSWP-29) subcategory enumeration; W2 against ISO/IEC 27002:2022 (8.15 Logging has no 8.15.3; 8.17 is Clock synchronization); S110-1 against CSWP-29 ID.AM-02/ID.AM-03.
- Bare-token residual greps clean in all three touched docs and corpus-wide (the only other carriers of the old tokens are TODO §1.17's own finding text, which this PR removes).
- A refute-briefed skeptical verifier reviewed the four fixes + the N2 mapping before push.
- The N2 mapping style (best-fit + category fallback) was maintainer-confirmed via `AskUserQuestion`.
- Recursion-avoidance batch: PR #1000's `/validate-pr` row and `/retro` row are carried in this PR.
- Pre-push guard (`run_all_audits.sh` 70/70 + `run-pr-time-checks.sh`) green before push.

## 2026-07-17, Library Version 2026.07.488, PR #1000

First PR of the 2026-07-17b resumed session (`/resume` from the session-closing handoff #999; on the VM, gh-CLI, no GitHub MCP; attended-autonomous). The loop-break Sweep 111 close-out: consumes the pre-positioned corpus-wide `/validate` and records its clean result, acquires the concurrency lease, and queues a recurrence-prevention backlog item. Working-state only; no corpus or website content changed.

### Changed
- [`.working/session-state.md`](../session-state.md) - lease ACQUIRED for this session (`Active-session: claude/resume-sweep111-closeout`, `Status: active`, fresh `2026-07-17T21:01:10Z` heartbeat, `Operating-mode: attended-autonomous`); `Current-task` and `Worker-dispatches` rewritten for the 2026-07-17b session (both workers start UNVALIDATED per the session-scoped trust model; worker-a ELEVATED at 1 of 2-to-3 after serving Sweep 111).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) - added the Sweep 111 row (Version `2.0.110` to `2.0.111`).
- [`.working/session-handoff.md`](../session-handoff.md) - advanced the machine-readable resume cursor to Sweep 111 (Sweep 110 demoted to `Prior:`); no session-block prune needed (already at current + 1 prior).

### Added
- [`TODO.md`](../../TODO.md) §3.93 - "Sync scratch every PR + fetch-before-read the credit-offload coordination plane", the recurrence-prevention item for the maintainer-flagged stale-scratch-read mistake (P3 `Next item number:` counter advanced `3.93` to `3.94`).

### Verification
- **Sweep 111 (loop-break control for #999): CLEAN PASS.** Offloaded to `worker-20260716-a` (Opus 4.8) as blocking prio-0 order `sweep-111-validate` pinned `65c5075b`/#999, deltas #992..#998. Consumed under full ELEVATED QA (worker-a delivery 1 this fresh session): proof-of-run genuine (~296K tokens, A/B/C returns); independent re-derivation of HEAD/baseline `70/70`/pre-flight 422-32-11/four-surface parity 70/counts 13-24-15-18/versions all EXACT-MATCH; a dedicated delivery-1 false-negative auditor (10 adversarial checks) returned CLEAN VERDICT HOLDS. 0 error / 0 warning / 0 new findings; the 2 notes (S111-1 = r4 §1.17 N2/W2, S111-2 = S110-1) are known-tracked and EXPECTED. All #992-#998 asserted-clean surfaces corroborated, 0 contradicted.
- **Discipline observation (self-caught, routed §3.93):** at this resume the orchestrator first read the scratch coordination plane from the un-synced LOCAL scratch checkout (16 commits behind `origin/main`) and wrongly reported both workers stale and the Sweep-111 order unclaimed, when worker-a had already delivered on `origin/main`. A scratch `git fetch` corrected it. This is a recurrence of the 2026-07-16 stale-read mistake; the fix (sync scratch every PR + a queue-tool auto-fetch) is queued as §3.93.
- Pre-push guard (`run_all_audits.sh` 70/70 + `run-pr-time-checks.sh`) green before push.

## 2026-07-17, Library Version 2026.07.487, PR #999

Session-closing handoff for the 2026-07-17 resumed session (`/resume` from #991; merged #992-#998, the §1.19 operational-state-privatization Phase-1 execution sprint). Working-state only; no corpus or website content changed. Per the loop-break, this handoff PR takes NO trailing `/validate-pr` + `/retro` (the compensating control is the next `/resume`'s corpus-wide Sweep 111 `/validate`, pre-positioned as an offload at this wind-down and cross-checked against the refreshed `## Asserted expectations`).

### Changed

- [`.working/session-handoff.md`](../session-handoff.md): refreshed and RECONCILED for the 2026-07-17 close (new "Next actions" closing + next-session blocks, State snapshot, and Asserted-expectations sub-block; the version snapshot reconciled to library `2026.07.487` / pack `1.62.0` / spec `1.17.9` / gate 70 / 24 skills / 15 commands), and PRUNED per keep-current-plus-one-prior (dropped the 2026-07-16b #969-#983 blocks; kept 2026-07-17 + 2026-07-16c).
- [`.working/session-metrics.md`](../session-metrics.md): a 2026-07-17 row (measured FLOOR ~1,653K post-compaction orchestrator subagent tokens across the 4 pre-push verifiers + 3 r11 guardrail lenses; ~1.24M offloaded-worker credits conserved across 8 passes; orchestrator main-loop `not instrumented`).
- [`.working/session-state.md`](../session-state.md): lease RELEASED (`Status: released`, `Active-session: none`), heartbeat re-stamped, Current-task marked CLOSED.
- The #998 QA batch: [`.working/validate-pr/history.md`](../validate-pr/history.md) (`1.2.761`) the validate-pr-998 SHIP row (worker-a, 3rd elevated pass -> routine) + the #999 handoff-exempt `SKIPPED` row; [`.working/improvement-log.md`](../improvement-log.md) (`1.0.696`) the #998 retro; [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.12`) the validate-pr-998 ledger row + the ~1.24M session-final roll-up.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed (§1.19.7 leads; #998 merged, #999 handoff closing).
- [`README.md`](../../README.md): Library `2026.07.486` -> `2026.07.487`, README `1.9.847` -> `1.9.848`. No corpus-document body or generated-artefact change.

### Verification

- The pre-push guard (`run_all_audits` 70/70 + D1-D8) is run green standalone before push. Per the handoff-PR exception (a maintainer-authorized standing rule, PR-workflow step 5a loop-break), this PR skips its own `/validate-pr` + `/retro`; the gate-50 handoff marker (`SKIPPED`, handoff) is in this PR's [`validate-pr/history.md`](../validate-pr/history.md) row Findings cell. The wind-down was maintainer-chosen (an `AskUserQuestion` at the Phase-1/Phase-2 boundary) on the rising caught-slip density on #998 plus the heavy chained Phase-2 series ahead; quality held (net zero adopter escapes across #992-#998).

## 2026-07-17, Library Version 2026.07.486, PR #998

The sixth Phase-1 deliverable of the §1.19 operational-state-privatization track (closes TODO §1.19.6): the run-once `/adopt` fork-onboarding skill + command, plus the origin-matcher hardening queued from #997 and the `/resume` adopter-path wiring. Seventh PR of the 2026-07-17 resumed session. No corpus or website content changed.

### Added

- [`dev-security/claude-rules/skills/adopt/SKILL.md`](../../dev-security/claude-rules/skills/adopt/SKILL.md) (the twenty-fourth pack skill) + [`.claude/commands/adopt.md`](../../.claude/commands/adopt.md) (slash command `/adopt`): the run-once onboarding for a fork adopting the project. Seven steps: confirm the clone is a genuine adopter (not the maintainer's repo or a fresh-machine clone) and adoption has not already run; choose the sibling model (own siblings vs self-contained); reset the machinery-core `.working/` working-state to clean adopter baselines (a sanctioned, adopter-clone-only exception to the never-drop invariants); handle the sibling placeholders (fetched reference text always goes into an EXTERNAL sibling, never the in-repo `.ref` stub, so gate 70 stays green); strip maintainer-only residue; record a committed adopt-config under `.claude/` (fields `mode`/`adopted_at`/`sibling_choice`/`adopt_config_version`); verify + report. `derives_from` [`session-lifecycle.md`](../../dev-security/claude-rules/governance/session-lifecycle.md). Never touches the corpus, pack, tooling, gates, or version lineage.
- [`tests/test_linters.py`](../../tests/test_linters.py): `DetectEnvIdentityTests` extended for the hardened matcher (now 6 tests: the reject set adds the non-GitHub-host and 3-segment cases that the host-pin now correctly rejects).

### Changed

- [`tools/detect-env.py`](../../tools/detect-env.py): `_origin_is_maintainer` hardened from an `endswith("/owner/repo")` match to a host-pinned exact `owner/repo`-parse (host must be `github.com`, path exactly two segments), closing the two theoretical false-maintainer classifications noted at #997 (a non-GitHub host with the maintainer owner; a malformed 3-segment path) now that §1.19.6 makes the classification load-bearing. The probe's docstring + adopter decision string updated to name the now-built `/adopt` (they previously pointed at a not-yet-built command, a stale forward-pointer the guardrail-review drift lens caught).
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): step 3 wires the adopter-path, act on the probe's `operator_identity`: an un-onboarded `adopter` HALTs and proposes `/adopt`; an `adopter` with a well-formed adopt-config proceeds in adopter-mode; a MALFORMED adopt-config is surfaced and re-proposes `/adopt`; a probe error leaves identity UNDETERMINED (ask, do not assume); `maintainer-fresh-machine` clones siblings, never `/adopt`.
- [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py): PAIRS registry extended with the `adopt` pair (steps 1-7 match on both surfaces).
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): skill-tree adds `adopt`; pack Version `1.61.6` -> `1.62.0` (minor; new skill) + a version-history row.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): the credit-offload command-count note updated (grc_library slash commands now 15).
- [`README.md`](../../README.md): Library `2026.07.485` -> `2026.07.486`, README `1.9.846` -> `1.9.847`. No corpus-document body or generated-artefact change (no taxonomy/portal/scorecard regen).

### Verification

- `tools/run_all_audits.sh` = **70/70** (working tree; the new skill+command drove gate-60 machinery-drift to 3, which is reset by the mandated guardrail-review r11 history row). The 6 `DetectEnvIdentityTests` pass under gate 36; the paired-skill-parity, collection-enumeration, gate-count, and derives-from gates green with the new skill.
- **Mandated `/guardrails` review (r11)**: the `/adopt` machinery addition drove gate-60 drift to 3 (gates 69->70 in #995 + skills 23->24 + commands 14->15), auto-prompting a formal three-lens (overlap/gap/drift) review, recorded in [`.working/guardrail-reviews/history.md`](../guardrail-reviews/history.md) + [`2026-07-17-r11.md`](../guardrail-reviews/2026-07-17-r11.md). It found six issues fixed in-window (the gate-70 `.ref`-bootstrap contradiction in step 4; the unstated never-drop exception in step 3; the malformed-adopt-config + detect-env-error `resume` branches; the non-gated-shape verification asymmetry; the stale detect-env forward-pointer; the frontmatter step-5 omission) and routed three hardenings to TODO §3.92 (mechanical adopt-config validation, an optional maintainer-clone pre-flight guard, the classification-coupling note).
- The pre-push guard (`run_all_audits` + D1-D8) is run green standalone before push; a refute-briefed skeptical verifier reviewed the diff. Batches PR #997's `/validate-pr` (worker-b, routine, SHIP clean) + `/retro`. This is a normal (non-handoff) PR, so its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.485, PR #997

The fifth Phase-1 deliverable of the §1.19 operational-state-privatization track (closes TODO §1.19.5): an origin-identity probe so the resume step can tell a maintainer clone from an adopter fork. Sixth PR of the 2026-07-17 resumed session. Detection only; the `/resume` adopter-path wiring lands in §1.19.6. No corpus or website content changed.

### Added

- [`tools/detect-env.py`](../../tools/detect-env.py): a `probe_identity(siblings)` classifier plus `_origin_url()` / `_origin_is_maintainer(url)` helpers and a `MAINTAINER_ORIGIN_OWNER_REPO` constant. It classifies the operator by the git `origin` remote: `maintainer` (origin is the canonical repo AND a sibling is readable), `maintainer-fresh-machine` (origin is the canonical repo but no sibling is readable, a fresh clone, NOT an adopter), or `adopter` (a fork origin, or none). `_origin_is_maintainer` matches both the HTTPS and SSH remote forms case-insensitively, tolerates a trailing `.git` / slash, and requires the owner boundary so a same-repo-name fork under a different owner does not match. The probe result feeds a new `operator_identity` line in the profile's decisions block and a printed profile line; the module docstring records the new probe.
- [`tests/test_linters.py`](../../tests/test_linters.py): a `DetectEnvIdentityTests` class (6 tests): the HTTPS/SSH/`.git`/case-insensitive match set, the fork/different-repo/absent reject set, and the four classifications (maintainer, maintainer-fresh-machine, adopter-fork, adopter-no-origin) driven by monkeypatching the module's `_origin_url`. Run under gate 36.

### Changed

- [`README.md`](../../README.md): Library `2026.07.484` -> `2026.07.485`, README `1.9.845` -> `1.9.846`. No corpus-document body or generated-artefact change (no taxonomy/portal/scorecard regen).

### Verification

- `tools/run_all_audits.sh` = **70/70** (working tree); the new `DetectEnvIdentityTests` (6) pass under gate 36's suite. [`tools/detect-env.py`](../../tools/detect-env.py) was smoke-tested on the VM and correctly classifies it `maintainer` (origin `jposluns/grc_library`, siblings present). The full sweep caught a PII-gate hit on an email-shaped `git@<host>` docstring example (the SSH-URL illustration), fixed by rewording the example before commit.
- The pre-push guard (`run_all_audits` + D1-D8) is run green standalone before push; a refute-briefed skeptical verifier reviewed the diff. Batches PR #996's `/validate-pr` + `/retro`. This is a normal (non-handoff) PR, so its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.484, PR #996

The fourth Phase-1 deliverable of the §1.19 operational-state-privatization track (closes TODO §1.19.2): uniform graceful-degradation for the advisory tools that reach a sibling repo, so a fork that clones only the public repo runs them without a spurious error. Fifth PR of the 2026-07-17 resumed session. No corpus or website content changed.

### Added

- [`tools/lint_common.py`](../../tools/lint_common.py): a shared `resolve_sibling(name)` helper (locate the real `../grc_library_<ref|scratch|private>` checkout, or `None`) and a companion `sibling_placeholder_present(name)` (whether the committed in-repo `.<name>` stub is present, which distinguishes an expected portable-clone `None` from a broken checkout). Module docstring Scope-notes updated to describe both.
- [`tests/test_linters.py`](../../tests/test_linters.py): a `ResolveSiblingTests` class (6 tests): unknown-name `ValueError`; real-sibling-vs-absent resolution; placeholder present/absent; and three `ref-holds` integration tests (graceful exit 0 on a portable clone with the `.ref` stub but no real sibling; exit 2 when neither the sibling nor the stub is present; exit 2 when a real `grc_library_ref` dir exists but is corrupt, lacking its index, the pre-push-verifier NOTE-2 edge). Run under gate 36.

### Changed

- [`tools/ref-holds.py`](../../tools/ref-holds.py): the default ref-root lookup now goes through `resolve_sibling("ref")`. When the real `grc_library_ref` is absent and no explicit `--ref-root` was given, it degrades to an advisory no-op (exit 0) if the `.ref` placeholder confirms a portable clone, instead of the former exit-2 error. An explicit `--ref-root` that does not resolve still errors (exit 2), as before. The graceful branch is gated on `resolve_sibling("ref") is None` (the real sibling dir genuinely absent), so a corrupt/partial real `grc_library_ref` (dir present but missing its index) still errors rather than being silently masked (the pre-push-verifier NOTE-2 edge).
- [`tools/audit-brief-freshness.py`](../../tools/audit-brief-freshness.py) and [`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py): the default scratch lookup now goes through `resolve_sibling("scratch")` (they already exited 0 on an absent sibling; this centralizes the location logic and adds a placeholder-aware advisory note). Their explicit `--scratch` / `GRC_SCRATCH_PATH` overrides are unchanged.
- [`tools/check-portability.sh`](../../tools/check-portability.sh): extended (now covers TODO §1.19.1 and §1.19.2) to also run the three sibling-reaching advisory tools in the sibling-free clone and assert each degrades to exit 0; header and verdict updated accordingly.
- [`README.md`](../../README.md): Library `2026.07.483` -> `2026.07.484`, README `1.9.844` -> `1.9.845`. No corpus-document body or generated-artefact change (no taxonomy/portal/scorecard regen).

### Discipline observation

- **Scope corrected at build (six tools -> three).** The locked design named six sibling-reaching advisory tools; a read-before-editing pass found only three reach a sibling today. `credit-offload-queue` is scratch-side (a worker tool in `grc_library_scratch`, not a `grc_library` tool, so a `grc_library` helper cannot serve it), and [`tools/residual-scan.py`](../../tools/residual-scan.py) / [`tools/tension-scan.py`](../../tools/tension-scan.py) read only in-repo working-state files today (they become sibling-reaching only in Phase 2 §1.19.8/9, when their [`.working/hallucination-metrics.md`](../../.working/hallucination-metrics.md) target moves to `_private`, and get wired then). Wiring the other three now would have added dead no-op code; the stricter-safe reading was taken and the §1.19.2 TODO scope note corrected. Surfaced to the maintainer.

### Verification

- `tools/run_all_audits.sh` = **70/70** (working tree); the new `ResolveSiblingTests` (6) pass under gate 36's suite. The three tools were smoke-tested on the VM (siblings present, normal behaviour) and `ResolveSiblingTests` proves the absent-sibling graceful path (and the corrupt-sibling error path) deterministically via a monkeypatched `REPO_ROOT`.
- A refute-briefed skeptical verifier reviewed the diff and caught three real items, all fixed here before push: a D8 length overrun in this entry's first-draft root sentence (53 words); the `ref-holds` corrupt-real-sibling masking edge (NOTE-2, now gated on `resolve_sibling("ref") is None`); and a portability-scope over-claim, six further `grc_library_ref`-reaching maintainer-cadence tools being deferred to TODO §3.91 (not adopter-blocking, they are skill-invoked, not gates). The pre-push guard (`run_all_audits` + D1-D8) is run green standalone before push. Batches PR #995's `/validate-pr` (offloaded to `worker-20260716-b`, its elevated-window delivery 3, SHIP clean, consumed under elevated QA with independent re-derivation of the mechanical facts) + `/retro`. This is a normal (non-handoff) PR, so its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.483, PR #995

The third Phase-1 deliverable of the §1.19 operational-state-privatization track (closes TODO §1.19.4): the hard sibling-repo stub-guard gate. Fourth PR of the 2026-07-17 resumed session. The corpus gate count rises 69 -> 70.

### Added

- [`tools/lint-sibling-placeholders.py`](../../tools/lint-sibling-placeholders.py) (gate 70, "Sibling-repo stub-guard audit"): enforces that each in-repo `.ref` / `.scratch` / `.private` placeholder directory (a) exists, (b) contains exactly one entry, its README stub, (c) whose first line is the `<!-- SIBLING-PLACEHOLDER: <name> -->` marker, and (d) is at most 25 lines, so no reference-base, worker-exchange, or private-operational payload can leak into the public repo through a placeholder. It scans only the three in-repo placeholder dirs, never the real sibling repos. The enforcement half of the §1.19.1 sibling-independence invariant.
- [`tests/test_linters.py`](../../tests/test_linters.py): a 7-case `SiblingPlaceholderTests` regression class (HEAD smoke test + good-stub pass + missing-dir / extra-payload / missing-marker / wrong-token / over-length fail cases). `check_placeholder` was refactored to take a `dir_path` so the fail cases run against temp dirs.

### Changed

- Four-surface gate wiring (gate-35 parity) + spec: [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh), [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml), and [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (§6 inventory row 70 + §6 detailed prose + §5 group 6 "Security and privacy"). The gate is named **"Sibling-repo stub-guard audit"** (not "Sibling-placeholder...") deliberately: "placeholder" is a gate-9 uncertainty marker, and the §6 table row sits within gate-9's 2-line window of the must-laden "Most gates..." paragraph, so a "placeholder" in the row name would trip gate 9; the detailed prose likewise avoids mandatory verbs (`must`/`shall`) next to the "placeholder"/"TODO" markers. No change to gate 9 itself.
- [`tools/lint_common.py`](../../tools/lint_common.py): refreshed the module Scope-notes docstring to enumerate all 8 `DEFAULT_EXEMPT_DIRS` (the 5 originals + the 3 sibling-placeholder dirs added in #994) and reframe the "further via `exempt_dirs`" statement, fixing validate-pr-994's NOTE-1 (a paired-surface docstring lag).
- [`TODO.md`](../../TODO.md): rotated `§1.19.4` to DONE (deleted the subsection; parent range now "§1.19.2 and §1.19.5 through §1.19.13"; the design-lock block's §1.19.4 clause reworded to drop the dangling token, recording the naming rationale).
- **Batched PR #994's QA:** the validate-pr-994 SHIP-with-NOTE row in [`validate-pr/history.md`](../validate-pr/history.md) (`1.2.756` -> `1.2.757`), the #994 `/retro` row in [`improvement-log.md`](../improvement-log.md) (`1.0.691` -> `1.0.692`), and the [`credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.7` -> `1.0.8`) validate-pr-994 ledger row + ~703K roll-up.
- [`README.md`](../../README.md): Library `2026.07.482` -> `2026.07.483`, README `1.9.843` -> `1.9.844`.
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) Version `1.17.8` -> `1.17.9` (its body changed: the gate-70 §6 row + detailed prose + §5 group). Generated artefacts regenerated: [`taxonomy.yml`](../../taxonomy.yml) (spec version row) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md); `docs/portal.md` unchanged.

### Verification

- `tools/run_all_audits.sh` = **70/70** (gate 70 wired + green). Gate 70 proven both directions: clean PASS on the live placeholders, and a non-vacuous FAIL on an injected payload file (exit 1) and via the 7 regression tests (all pass). Gate 9 (mandatory-near-uncertainty) re-confirmed clean after the naming + prose fix; gate 35 four-surface parity holds with the renamed gate.
- validate-pr-994 consumed under ELEVATED QA (worker-b delivery 2): proof-of-run genuine, NOTE-1 re-verified real at source and fixed here. The pre-push guard (run_all_audits 70/70 + D1-D8) was green standalone before push; a refute-briefed skeptical verifier reviewed the diff. Normal (non-handoff) PR; its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.482, PR #994

The second Phase-1 deliverable of the §1.19 operational-state-privatization track (closes TODO §1.19.3): the in-repo sibling-repo placeholder stubs and their exemption. Third PR of the 2026-07-17 resumed session. §1.19.4 (the hard stub-guard gate) follows next; the placeholders ship one PR ahead of their guard because they are exempt content nothing edits in the interim.

### Added

- [`.ref/README.md`](../../.ref/README.md), [`.scratch/README.md`](../../.scratch/README.md), [`.private/README.md`](../../.private/README.md): three in-repo placeholder directories, each holding ONLY a README stub. Each stub carries a `<!-- SIBLING-PLACEHOLDER: <name> -->` marker (line 1), names the real sibling repo it stands in for (`grc_library_ref` / `grc_library_scratch` / `grc_library_private`) and its purpose, and gives an adopter/AI note (point your own sibling, or leave the stub and the dependent advisory tools skip cleanly). Each is <= 25 lines with no payload (the §1.19.4 gate will enforce this). They implement the resolution order real-sibling -> in-repo placeholder -> no-op for a fork that clones only the public repo.

### Changed

- [`tools/lint_common.py`](../../tools/lint_common.py): added `.ref`, `.scratch`, `.private` to `DEFAULT_EXEMPT_DIRS` (with a comment pointing at the stub-guard gate), so the content gates skip the placeholder dirs while the dedicated gate guards them.
- [`TODO.md`](../../TODO.md): rotated `§1.19.3` to DONE (deleted the subsection; updated the §1.19 parent to record the placeholder stubs shipped in #994); recorded the **full Phase-1 build design LOCKED** (all of §1.19.2-§1.19.7, from the 2026-07-17 design session) in the §1.19 parent so the remaining PRs build to it.
- [`README.md`](../../README.md): Library `2026.07.481` -> `2026.07.482`, README `1.9.842` -> `1.9.843`.
- **Batched PR #993's QA** (offloaded, consumed this PR): the `validate-pr-993` SHIP row in [`validate-pr/history.md`](../validate-pr/history.md) (`1.2.755` -> `1.2.756`; worker-a delivery 2, elevated window, 0/0/0) and the #993 `/retro` row in [`improvement-log.md`](../improvement-log.md) (`1.0.690` -> `1.0.691`); the [`credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.6` -> `1.0.7`) validate-pr-993 ledger row + roll-up (~583K gross this session). Routed one validate-pr-993 FYI, `check-portability.sh` covers relative sibling-reaches only, to new TODO §3.90.

### Verification

- `tools/run_all_audits.sh` = 69/69 (no count change; the placeholders are exempt content, no new gate this PR). `tools/check-portability.sh` (the §1.19.1 tool) still PASSES: the placeholders travel with a sibling-free clone and are exempt, so all 69 gates stay green with no sibling present.
- The pre-push guard (run_all_audits 69/69 plus D1-D8) was green standalone before push. Normal (non-handoff) PR; its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.481, PR #993

The first Phase-1 deliverable of the §1.19 operational-state-privatization + adopter-clone-portability track (closes TODO §1.19.1), plus consumption of PR #992's post-merge QA and the corrections it surfaced. Second PR of the 2026-07-17 resumed session.

### Added

- [`tools/check-portability.sh`](../../tools/check-portability.sh): the sibling-independence portability check. It git-clones the repo's HEAD into a fresh temp dir with NO `grc_library_ref`/`grc_library_scratch`/`grc_library_private` sibling present and runs `run_all_audits.sh` there, asserting all 69 gates pass. This makes explicit and locally-reproducible the guarantee that a fork reaching no sibling repo runs the full toolchain green (CI already runs sibling-free on the GitHub runner; this reproduces that locally, where the maintainer's checkout HAS the siblings). Deliberately NOT wired into `run_all_audits.sh` (recursive) or a per-PR gate (CI already enforces it); it is an on-demand maintainer/adopter tool. **Verified both directions:** PASS on the real corpus (69/69 in a sibling-free clone) and a proven non-vacuous FAIL (an injected sibling-reach in a scenario clone makes the check fail, exit 1), so it is not a vacuous test.
- [`TODO.md`](../../TODO.md) `§3.89`: routed the D7-inert observation the validate-pr-992 delivery-1 auditor surfaced (D7 parses only the first `Current truth` line, but the handoff's version tokens live on a `Version snapshot` sub-bullet, so D7 validates 0 tokens and is effectively inert; pre-existing, not a #992 defect; fix + non-vacuous regression fixture queued).

### Changed

- [`TODO.md`](../../TODO.md): rotated `§1.19.1` to DONE (deleted the subsection; reworded the two live citers, the parent range and the §1.19.10 "per §1.19.1", to name the sibling-independence invariant / `tools/check-portability.sh` without a dangling intra-doc §-anchor); bumped "Next item number" 3.89 -> 3.90.
- **Consumed `validate-pr-992` (worker-b, OFFLOADED, ELEVATED window, its 1st QA-kind delivery this session):** SHIP with one in-window WARNING (W1). W1 = the worker-a trust-tier miscount (the #992 records relaxed worker-a to routine by counting last-session elevated passes; the window is session-scoped and resets each session, so worker-a is ELEVATED 1-of-2-to-3). This was the ORCHESTRATOR's own self-catch, independently corroborated by the worker with CLAUDE.md line cites. **Corrected this PR** across all six carriers: [`.working/session-state.md`](../session-state.md), [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md), [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md), [`.working/session-handoff.md`](../session-handoff.md) (the Resume cursor), [`.working/next-prs.txt`](../next-prs.txt), and the #992 entry in this mirror. A delivery-1 false-negative auditor (orchestrator-run) found no additional substantive miss, only a trivial `175`->`174` handoff-line-count slip (**FIXED this PR** in the #992 detailed entry) and the pre-existing D7 observation (routed to §3.89 above).
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (`1.2.754` -> `1.2.755`): the validate-pr-992 SHIP-with-W1 row.
- [`.working/improvement-log.md`](../improvement-log.md) (`1.0.689` -> `1.0.690`): the #992 `/retro` row.
- [`.working/DONE.md`](../DONE.md): the §1.19.1 closure entry (keyed to #993).
- [`.working/session-state.md`](../session-state.md): lease heartbeat re-stamped, `Active-session` -> `claude/todo-1-19-1-portability-test`, Current-task updated to #993, worker-b recorded as ELEVATED (1 of 2-to-3 this session, validate-pr-992).
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.5` -> `1.0.6`): the validate-pr-992 ledger row (~132K conserved, net-negative this delivery vs the ~255K one-time delivery-1 auditor) and the 2026-07-17 roll-up (~491K gross).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (`2.0.109` -> `2.0.110`): the worker-a trust-tier correction applied to the Sweep 110 row (Version re-bumped because the row's body changed again in this PR).
- [`README.md`](../../README.md): Library `2026.07.480` -> `2026.07.481`, README `1.9.841` -> `1.9.842`.

### Verification

- `tools/check-portability.sh` PASS-case: `run_all_audits.sh` = 69/69 in a sibling-free clone (exit 0). Non-vacuity: a scenario clone with an injected `grc_library_ref` reach in `run_all_audits.sh` made the check FAIL (exit 1, "PORTABILITY: FAIL rc=42"), confirming it detects a sibling reach.
- validate-pr-992 consumed under full ELEVATED QA (proof-of-run genuine ~132K; mechanical facts independently re-derived; W1 re-verified as the orchestrator's own self-catch; a delivery-1 false-negative auditor found no additional substantive miss). worker-b is at 1 of 2-to-3 clean elevated passes this session.
- The pre-push guard (run_all_audits **70/70** plus the D1-D8 PR-time checks) was green standalone before push. The audit-programme spec's Version was co-bumped (`1.17.8` -> `1.17.9`) for its body change and the taxonomy + maturity-scorecard regenerated (the pre-push skeptical verifier caught the initially-missed spec Version bump, a gate-40 catch, pre-push). This is a normal (non-handoff) PR, so its own `/validate-pr` + `/retro` batch into the next PR.

## 2026-07-17, Library Version 2026.07.480, PR #992

The Sweep 110 loop-break corpus-wide `/validate` close-out, the first PR of the 2026-07-17 resumed session (`/resume` from #991). Records the offloaded, elevated-QA-validated Sweep 110 result and its triage, the locked `§1.19.x` design decisions from the continued operational-state-privatization discussion, the `§3.87` worker-exchange transport design, the handoff prune, and the lease acquire. This is a normal (non-handoff) PR, so it takes its own `/validate-pr` + `/retro`, which batch into the next PR.

### Added

- [`TODO.md`](../../TODO.md) `§1.17` sub-item (d): routed Sweep-110 finding **S110-1** (`dev-security/standard-software-composition-analysis.md:253` cites `ID.AM-3, Software asset inventory` in a NIST CSF 2.0 cell; software inventory is CSF 2.0 `ID.AM-02` and `ID.AM-03` is network/data-flow representations), orchestrator-re-verified at held CSWP-29 (lines 791/793); same CSF-subcategory-accuracy class as N2/W2, gate-49/54-blind, NOT r4-gated.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (`2.0.108` -> `2.0.109`): the Sweep 110 row (0 error / 1 warning / 2 note; loop-break control for #991 PASSES).

### Changed

- [`TODO.md`](../../TODO.md) `§1.19`: recorded the three formerly-open items as LOCKED at this resume. **#7** (`§1.19.11`) = a minimal `_private` `validate` gate (secrets/PII + house-style) + README + CLAUDE.md. **#8** (`§1.19.10`) = a tiered public root CHANGELOG projection (current week per-PR 1-2 sentences at max 30 words/sentence; weeks < 3 months to one <=4-sentence weekly paragraph; > 3 months to monthly), event-driven weekly cycle, maintainer-side generated projection (NOT a CI gate, source moves to `_private` per `§1.19.1`), per-PR + full detail move to `_private`, folds in `§1.12` and reshapes D8, git-history minability accepted. **worker-lean = REJECTED** (worker inputs stay in scratch, `_private` orchestrator-only, the least-privilege read surface); the move-list `worker-brief-template`-to-scratch caveat resolved accordingly.
- [`TODO.md`](../../TODO.md) `§3.87`: extended with the maintainer-co-designed control-plane / data-plane transport (a unix domain socket `/tmp/grc_exchange/orchestrator.sock` as the control plane, `/tmp/grc_exchange/` as the data plane, filesystem-as-durable-state-of-record with socket-down fallback to inbox polling, same-VM-only, directory + socket names confirmed).
- [`CHANGELOG.md`](../../CHANGELOG.md) + this mirror: fixed Sweep-110 finding **S110-2**, the #986 entry mis-quoted the charter's deleted COBIT title as "Managed Data"; the charter cell at base `28d4146b` read `APO14: Manage Data` (an imperative-drift rendering), so both surfaces are reworded to the accurate deleted value (the canonical-title parenthetical is unchanged and correct). Because the S110-2 edit re-touched the #986 root entry (147 words, pre-dating the D8 ceiling), the root #986 summary was compressed to <= 100 words to satisfy D8, a small in-scope down-payment on §1.12 (its full detail already lives in this mirror).
- [`.working/session-handoff.md`](../session-handoff.md): PRUNED per the keep-current-plus-1-prior discipline (dropped the #964-#967 blocks from the Next-actions, State-snapshot, and Asserted-expectations stacks, 174 -> 151 lines; no dangling supersede pointer); advanced the Resume cursor to Sweep 110.
- [`.working/session-state.md`](../session-state.md): lease ACQUIRED (`Active-session: claude/resume-sweep110-validate`, `Status: active`, fresh heartbeat, `Operating-mode: attended-autonomous`); worker-20260716-a stays ELEVATED this session (1 of 2-to-3 clean elevated passes; sweep-110 is its 1st this session, the session-scoped window having reset). NOTE: an earlier version of this entry wrongly said "re-graduated to routine" by counting last-session passes; corrected in #993 (the window resets each session by construction).
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.4` -> `1.0.5`): the `sweep-110-validate` ledger row (~359K gross) and a 2026-07-17 per-session roll-up row.
- [`README.md`](../../README.md): Library `2026.07.479` -> `2026.07.480`, README `1.9.840` -> `1.9.841`.

### Verification

- Sweep 110 consumed under ELEVATED QA (worker-a on the post-reset window, delivery 3): proof-of-run genuine (~359K, A ~103K / B ~79K / C ~66K subagent returns + `path:line` evidence); base #984 `28d4146b`, baseline 69/69, pre-flight 421/33/11, four-surface parity 69, counts 13/23/14/18, and versions independently re-derived EXACT-MATCH; every finding (S110-1 at held CSWP-29, S110-2 at the charter's base-SHA cell + held COBIT title, S110-3 = the pre-declared known-open N2) re-verified at source. No red flag, so no separate adversarial auditor; worker-a stays ELEVATED this session (1 of 2-to-3; the window is session-scoped). **Loop-break control for #991 PASSES**; asserted-expectations all corroborated, 0 contradicted.
- The pre-push guard (run_all_audits 69/69 plus the D1-D8 PR-time checks) was green standalone before push; the CHANGELOG preflight was clean on the added lines. No corpus-document body or generated-artefact change (no taxonomy/portal/scorecard regen needed).

## 2026-07-17, Library Version 2026.07.479, PR #991

Session-closing handoff PR for the 2026-07-16c resumed session (`/resume` from #984, PRs #985-#990). Its purpose is to land the session's working-state on `main` as a green merge so the next `/resume` rebuilds from `main`, and to document the maintainer-co-designed operational-state-privatization spec as a Priority-1 multi-phase backlog item. Per the loop-break it takes no trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate`, pre-positioned at wind-down as an offloaded worker order.

### Added

- [`TODO.md`](../../TODO.md) `§1.19` (parent) plus phased deliverables `§1.19.1` through `§1.19.13`: privatize the maintainer's operational state and process narrative (the surface a 2026-07-17 cold-sales email mined from public `.working/`) WITHOUT reducing what an adopter gets, and make the public repo robustly clonable-and-usable by a fork that reaches no sibling repo (`_ref` / `_scratch` / `_private`). Co-designed with the maintainer across a considerations discussion; locked items include the sibling-independence invariant + portability test (`§1.19.1`), placeholder stub dirs + a hard-blocking stub-guard gate (`§1.19.3`/`§1.19.4`), `detect-env` maintainer/adopter origin-identity detection (`§1.19.5`), a `/adopt` run-once onboarding skill (`§1.19.6`), a `.ref` bootstrap for adopters (`§1.19.7`), and the move-list + reference-repointing rules (`§1.19.8`). Execution is FRESH next session; the `§1.19.x` discussion CONTINUES on `/resume` at the still-open items recorded at `§1.19` (#7 `_private` hygiene / `§1.19.11`, #8 public-changelog weekly-rollup / `§1.19.10`, and the worker-read-only-`_private` lean).

### Changed

- [`.working/session-handoff.md`](../session-handoff.md): prepended the 2026-07-16c Next-actions, State-snapshot (library `2026.07.479`, spec `1.17.8`, gate 69, D1-D8), and Asserted-expectations blocks (scoped to what this session mechanically verified; KNOWN-OPEN carried forward: the r4 W1/N2/W2 corpus citations remain unfixed, tracked at `§1.17`).
- [`.working/session-metrics.md`](../session-metrics.md) (`1.0.61` -> `1.0.62`): one row for the 2026-07-16c session (6 PRs + this handoff; measured orchestrator-subagent FLOOR ~216K, the rest offloaded; ~793K est. credits conserved across 7 offloaded passes).
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (`1.0.3` -> `1.0.4`): added the six missing 2026-07-16c `/validate-pr` delivery rows (985-990) and corrected the per-session roll-up from ~207K (Sweep 109 only) to ~793K gross across 7 passes.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (-> `1.2.754`): the validate-pr-990 SHIP row (worker-a 2nd post-reset PASS, consumed clean) and the #991 SKIPPED / handoff-exception row (marker in the Findings cell per the gate-50 convention).
- [`.working/improvement-log.md`](../improvement-log.md) (-> `1.0.689`): the #990 `/retro` row.
- [`.working/session-state.md`](../session-state.md): lease RELEASED (`Status: released`, `Active-session: none`, `Operating-mode` retained); gate 63 green.
- [`README.md`](../../README.md): Library `2026.07.478` -> `2026.07.479`, README `1.9.839` -> `1.9.840`.

### Verification

- The pre-push guard (run_all_audits 69/69 plus the D1-D8 PR-time checks) was green standalone before push; the CHANGELOG preflight was clean on the added lines. No corpus-document body or generated-artefact change (no taxonomy, portal, or scorecard regen needed). This handoff PR intentionally skips its own `/validate-pr` + `/retro` (loop-break); the compensating control is the next `/resume`'s corpus-wide `/validate`.

## 2026-07-17, Library Version 2026.07.478, PR #990

Two mistake-prevention fixes for errors flagged this session (the AskUserQuestion-in-unattended blunder and the ISO-27002 partial-grep error), plus the PR #989 QA batch.

### Added

- [`tools/ref-holds.py`](../../tools/ref-holds.py): forcing-function aid (advisory, not a gate) answering held/not-held for `grc_library_ref` from its INDEX/catalogue (quoted output), never a partial filename grep (Mistake 2). Self-test 3/3; a `ref-holds` `27002` query returns HELD, the exact check that would have prevented the ISO-27002 error.
- [`.claude/hooks/block-askuserquestion-unattended.py`](../../.claude/hooks/block-askuserquestion-unattended.py): PreToolUse hook (matcher `AskUserQuestion`) that blocks the call when the session `Operating-mode` is unattended (Mistake 1); fail-open on any read failure; self-test 4/4. Registered in [`.claude/settings.json`](../../.claude/settings.json).
- [`.working/session-state.md`](../session-state.md) `**Operating-mode:**` field, gate-63-validated (`fully-attended` / `attended-autonomous` / `overnight-unattended` / `daytime-unattended`).

### Changed

- [`tools/lint-session-state.py`](../../tools/lint-session-state.py) (gate 63): `Operating-mode` added as a required + value-validated field; docstring updated. [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (1.17.7 to 1.17.8): the gate-63 prose (both the §5 grouped narrative and the §6 detailed paragraph) updated from five to six fields including `Operating-mode`. [`tests/test_linters.py`](../../tests/test_linters.py): the `VALID_LEASE` fixture gains the field, plus two new gate-63 tests (invalid mode flagged; unattended mode passes). Generated artefacts regenerated.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): the executed-not-narrated rule for held/not-held claims (quote `ref-holds`, never a partial grep) in the reference-currency section; the mechanical-backstop rule (the `Operating-mode` field + the hook) in the no-idle-stop section.
- **validate-pr-989 NOTE-1 fixed in-window:** the r4 W2 CONFIRMED-at-held-source disposition was propagated to the two stale surfaces ([`2026-07-16-r4.md`](../deep-assessment/2026-07-16-r4.md) and the [`register.md`](../deep-assessment/register.md) r4 row), which had lagged at "SOURCE-NOT-HELD".
- #989 QA batch: the validate-pr-989 SHIP row (worker-b delivery-3, graduated to routine) + the #989 retro row; session-state lease re-stamped and updated.

### Verification

- the `ref-holds` self-test 3/3 (plus a live `27002` HELD query); the hook self-test 4/4; gate 63 green on the live lease; the linter regression suite (385 tests) green; the settings file is valid JSON. Pre-push guard (run_all_audits + D1-D8 + history-aware trio) green.
- validate-pr-989 (worker-b, delivery-3, elevated) returned SHIP with one NOTE (the r4 W2 paired-surface lag), re-verified at source and fixed here; worker-b graduated to routine trust (3 clean elevated passes: sweep-109, the deep-assessment continuation, validate-pr-989).

## 2026-07-17, Library Version 2026.07.477, PR #989

CHANGELOG length delta gate D8 (the enforcement for the recurring root-entry drift), the deep-assessment r4 continuation consume, and the PR #988 QA batch.

### Added

- [`tools/check-changelog-length-on-pr.py`](../../tools/check-changelog-length-on-pr.py) (delta gate D8): fails a PR whose newly-added root CHANGELOG entry summary exceeds 100 words or has a sentence over 45 words. Forward-only (added lines only), like the D3 dash gate; history untouched. Inline self-test 4/4; verified it catches the #985 drift (237 words / 62-word sentence). Root cause it fixes: the prior length check ([`tools/audit-changelog-entry-length.py`](../../tools/audit-changelog-entry-length.py)) was advisory-only, wired into no gate, so nothing failed CI when an entry drifted (three recurrences: #887-901, #902-914, #919-986).
- [`TODO.md`](../../TODO.md) §1.17: the r4 confirmed gate-blind citation fixes (W1 NIST cipher-suite, N2 CSF subcategories, W2 ISO 27002 clause), holding for r4 sign-off.

### Changed

- D8 wiring across surfaces: [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh), [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), `WORKFLOW_DELTA_GATE_STEPS` in [`tools/lint-audit-gate-parity.py`](../../tools/lint-audit-gate-parity.py), and [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (D8 table row + prose; Version 1.17.6 to 1.17.7). D1-D7 range claims updated to D1-D8 in [`tools/pre-push-guard.sh`](../../tools/pre-push-guard.sh) and the active CLAUDE.md. The advisory tool's docstring now names D8 as its enforcing sibling.
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md) + [`2026-07-16-r4.md`](../deep-assessment/2026-07-16-r4.md): r4 continuation recorded (phases 3-7 complete via worker-b; Phase 8 holds for maintainer sign-off); findings routed.
- [`TODO.md`](../../TODO.md): P3 `Next item number` counter 3.87 to 3.89 (the validate-pr-988 W1 fix set it to 3.88, then the new §3.88 item advanced it to 3.89); §1.17 (r4 citation fixes) and §3.88 (worker-registry stale-entry prune) added; §1.12 annotated (part 2 satisfied by D8). §1.16 is a #988 item, not touched here.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (to 1.2.752): validate-pr-987 + validate-pr-988 rows. [`.working/improvement-log.md`](../improvement-log.md) (to 1.0.687): #987 + #988 retro rows. [`.working/session-state.md`](../session-state.md): lease heartbeat + worker-dispatches.

### Verification

- Parity gates green (gate 35: 69 gates across four surfaces; spec-prose: 8 delta checks narrated and registry-matched). Pre-push guard (run_all_audits + PR-time D1-D8 + history-aware 45/40/31) green.
- Worker QA consumed under elevated windows: validate-pr-987 (worker-a delivery-3, a confirmed enumeration miss caught by re-derivation, window RESET + escalated); deep-assessment r4 continuation (worker-b delivery-2, findings re-verified at held source, W1/N2/W2 all confirmed); validate-pr-988 (worker-a first post-reset, PASS, caught the real P3-counter defect). W2 was corrected from an initial wrong "source-not-held" call after the maintainer flagged that ISO/IEC 27002:2022 IS held (an absence-from-partial-grep error, now codified against).

## 2026-07-17, Library Version 2026.07.476, PR #988

TODO §2.22 first bite (a sector-neutral Canada comparator row), plus the local-VM worker-exchange transport design record, a routed QA finding (§1.16), and PR #987's `/validate-pr` + `/retro` batch.

### Added

- [`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md) (Version 0.0.9 to 0.0.10): TODO §2.22 (A2). A labelled sector-neutral comparator row after the AIS-13 row in the framework-alignment table, citing the Canadian TBS Guide on the Use of Agentic AI for its bounded-autonomy (labelled activity-permission levels, tight tool/data/scope limits, accountable agent owners) and recoverability (pausable agents, tamper-evident logging) principles, marked advisory and not binding on an external adopter. Verified against the held TBS Guide on the Use of Agentic AI full-text in the `grc_library_ref` Canada-TBS frameworks bucket. Sector-neutrality respected: Canada-specific instrument placed as a labelled comparator, not a primary anchor. Generated artefacts regenerated.
- [`.working/design-decisions.md`](../design-decisions.md): the "Local-VM exchange transport for credit-offload" design (maintainer-directed 2026-07-17): a `/tmp/grc_exchange` shared-directory transport (per-worker inbox/outbox/heartbeat, push plus stale-reclaim assignment, no crash backup, coexisting with the git-`scratch` cloud transport via [`tools/detect-env.py`](../../tools/detect-env.py)) for the all-on-one-VM case, replacing the git round-trips that are pure overhead on one VM. Resolves TODO §3.85.
- [`TODO.md`](../../TODO.md): new §3.87 (build the local-VM exchange transport, credit-offload thread-6, resolves §3.85; P3 counter to 3.88); new §1.16 (COBIT management-objective title normalization plus a title-text validation gate, routed from validate-pr-987 N1; P1 counter to 1.17).

### Changed

- [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.750 to 1.2.751): the validate-pr-987 SHIP row (N1 routed to §1.16; records the elevated-QA-caught worker-a enumeration miss and window reset).
- [`.working/improvement-log.md`](../improvement-log.md) (1.0.685 to 1.0.686): the PR #987 `/retro` row.
- [`.working/session-state.md`](../session-state.md): lease re-stamped to `claude/canada-2226-agentic`; Current-task and Worker-dispatches updated (worker-a elevated window RESET on the d3 miss).
- [`.working/next-prs.txt`](../next-prs.txt): cycled to the next queue (CHANGELOG remediation now leads).

### Verification

- validate-pr-987 (worker-a delivery-3) SHIP verdict independently re-derived correct (self-test 5/5, APO14 canonical title, both #987 changes). Elevated-QA mechanical re-derivation caught a confirmed miss (N1 enumeration 32/25 vs true 35/28); worker-a window reset and escalated to the maintainer (see §1.16 and the validate-pr row).
- A2 comparator row verified against the held TBS source; `run_all_audits.sh` + `run-pr-time-checks.sh` green; CHANGELOG root written in the short compact form per the 2026-07-17 maintainer directive.

## 2026-07-17, Library Version 2026.07.475, PR #987

Delivery-status tooling fix (closes TODO §3.61) plus a QA-surfaced gate-blind COBIT title fix, and batches PR #986's `/validate-pr` + `/retro`.

### Fixed

- [`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py): TODO §3.61. `classify()` now returns `(bucket, low_confidence)`; a PENDING or APPLIED verdict resting ONLY on a recyclable section-number token (no stable FR/SR/GR coded id) is flagged LOW-CONFIDENCE, because a renumbered/recycled section number can map to a different current item than the delivery intended (the 2026-07-16 gr-gap `3.15` -> MITRE-ATLAS and etsi `3.16` -> CHANGELOG mis-maps). A coded-id match stays high-confidence. The report headline carries a low-confidence count and each flagged row a verify note; the module docstring documents the confidence model. Self-test extended (5 of 5 pass).
- [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md) (Version 1.0.4 to 1.0.5): validate-pr-986 Note-1. The COBIT process-alignment table's APO14 row listed the title as "Managed AI"; the canonical COBIT 2019 title is "Managed Data" (a substitution error, gate-blind since gate 61 validates code existence not title accuracy). Corrected; a corpus-wide `Managed AI` grep confirmed line 308 was the only COBIT-title carrier (the other hits are legitimate prose about managed AI services). Generated artefacts regenerated.

### Changed

- [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.749 to 1.2.750): the validate-pr-986 SHIP row (Note-1 fixed in-window).
- [`.working/improvement-log.md`](../improvement-log.md) (1.0.684 to 1.0.685): the PR #986 `/retro` row.
- [`TODO.md`](../../TODO.md): TODO §3.61 closed (deleted); [`.working/DONE.md`](../DONE.md) gains the §3.61 rotation.
- [`.working/session-state.md`](../session-state.md): concurrency-lease heartbeat re-stamped; Active-session `claude/delivery-status-coded-id`.
- Library CalVer `2026.07.474` to `2026.07.475`; [`README.md`](../../README.md) README Version `1.9.835` to `1.9.836`.

### Verification

- `audit-delivery-status.py --self-test`: 5 of 5 pass; the live report now flags the 8 section-token-only PENDING deliveries as LOW-CONFIDENCE (the gr-gap / etsi recycled-token class).
- validate-pr-986 (worker-20260716-a, elevated delivery-2, PASS): MF1 re-verified at the held COBIT source; Note-1 (this PR's register fix) re-verified real at source before applying.
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before the first commit; pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green.

## 2026-07-17, Library Version 2026.07.474, PR #986

Consumes the four delivered worker quality-assurance passes (`matrix-fit-full-pass`, `canada-matrix-fit`, `claim-fit-tier-a-pass`, `screen-publications-pending`) and fixes the one defect surfaced (MF1). Also batches PR #985's `/validate-pr` + `/retro`. The QA-passes-first ordering is maintainer-directed (a QA delivery may contain a must-fix, so it is consumed ahead of build/tooling work).

### Fixed

- [`ai/charter-ai-governance-council.md`](../../ai/charter-ai-governance-council.md) (Version 1.2.7 to 1.2.8): **MF1** (from `matrix-fit-full-pass`, worker-20260716-a). The charter's sole COBIT alignment row cited `APO14 "Manage Data"` (an imperative-drift rendering of the canonical title "Managed Data") for a document whose subject is the AI Governance Council, a governance/oversight BODY (Mandate = "provide oversight of AI system risk and compliance"). Corrected to `EDM01 "Ensured Governance Framework Setting and Maintenance"`, the on-point COBIT objective for establishing and maintaining a governance body; re-verified against the held COBIT reference module (APO14 = "Managed Data"; EDM01 = "Ensured Governance Framework Setting and Maintenance") with gate 61 (COBIT citation-existence) green. Generated artefacts regenerated.

### Changed

- [`.working/matrix-fit/history.md`](../matrix-fit/history.md) (Version 1.0.10 to 1.0.11): two rows recording the consumption of `matrix-fit-full-pass` (1 mis-fit MF1 fixed; compliance matrix 0 mis-fits, 64/64 rows / 402/402 codes) and `canada-matrix-fit` (0 mis-fits; 23 Canada citations well-fitted; feeds §2.22).
- [`.working/claim-fit/history.md`](../claim-fit/history.md) (Version 1.0.10 to 1.0.11): a row recording `claim-fit-tier-a-pass` (8 of 8 Tier-A attributions accurate: 7 prescribed, 1 informed-not-prescribed already correctly handled; 0 defects).
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.748 to 1.2.749): PR #985's `/validate-pr` row (SHIP; 1 low note, Note-1, routed to TODO §3.86). Offloaded to `worker-20260716-a` as its first QA-kind delivery this session, consumed under elevated QA (delivery-1): mechanical facts independently re-derived, Note-1 re-verified real at the held statute; worker-a elevated delivery-1 PASS.
- [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.683 to 1.0.684): PR #985's `/retro` row (committed earlier on this branch).
- [`TODO.md`](../../TODO.md): new §3.86 (CCPA dollar-threshold CPI-adjustment caveat, corpus-wide, low priority) routing Note-1; the Priority-3 next-item counter advanced to 3.87.
- [`.working/session-state.md`](../session-state.md): concurrency-lease heartbeat re-stamped; Active-session updated to `claude/pr985-qa-and-next`.
- Library CalVer `2026.07.473` to `2026.07.474`; [`README.md`](../../README.md) README Version `1.9.834` to `1.9.835`.

### Verification

- The publications-screening pass (`screen-publications-pending`) reported the register fully drained (25/25 screened, 0 pending); no corpus action. Its bonus whole-bucket scan surfaced only benign extraction artefacts (zero-width / soft-hyphen), no injection content.
- MF1 re-verified at source before apply (the worker-a QA consume discipline); Note-1 re-verified real at the held Civil Code §1798.140(d)(1)(A) (line 256, the "as adjusted pursuant to Section 1798.199.95" clause), and routed rather than fixed in isolation per the worker's consistency caution (the same clause is elided wherever the corpus cites the threshold).
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before the first commit; pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green; gate 61 (COBIT) green after the MF1 code substitution.

### Note (QA-passes-first ordering, maintainer-directed)

- Every delivered QA pass is assessed FIRST and any surfaced fix outranks build/tooling/content work. This PR is that pass; MF1 was bumped ahead of the §2.22 Canada apply as the one must-fix among the four consumed QA deliveries.

## 2026-07-17, Library Version 2026.07.473, PR #985

The Sweep 109 validation close-out (the loop-break compensating control for session-closing handoff PR #984, which skipped its trailing `/validate-pr` + `/retro`), covering the #969..#984 delta window. The first OFFLOADED-then-elevated-QA-validated sweep of the 2026-07-16c resumed session.

### Changed

- [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md) (Version 1.2.3 to 1.2.4): the California cybersecurity-audit threshold parenthetical (section 7120) now states BOTH section 7120(b) triggers, where it previously rendered only the (b)(2) prong. The fix (finding S109-N1, surfaced by the elevated-QA adversarial auditor) is a summary-completeness precision tightening, not a citation error (the sentence already defers to "the section 7120 thresholds" as authoritative). Verified at the held CCPA Regulations section 7120(b) (two independent triggers) and Civil Code section 1798.140(d)(1)(A) (">USD 25 million gross revenue", held file line 256) and (d)(1)(C) ("derives 50 percent or more of annual revenue from selling or sharing personal information", lines 258 to 259).
- Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) after the per-document version bump.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (Version 2.0.107 to 2.0.108): the Sweep 109 row.
- [`.working/session-handoff.md`](../session-handoff.md): advanced the Resume cursor to Sweep 109, and PRUNED the 2026-07-15 #955-#962 per-session stack (the Next-actions / State-snapshot / Asserted-expectations blocks) per keep-current-plus-one-prior.
- [`.working/session-state.md`](../session-state.md): concurrency lease ACQUIRED for branch `claude/resume-sweep109-validate` (Status active, fresh heartbeat) for the 2026-07-16c resumed session.
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (Version 1.0.2 to 1.0.3): the `sweep-109-validate-2` consume row (~207K gross; net materially lower this delivery due to the one-time new-worker elevated-QA cost) plus a new per-session roll-up row for the 2026-07-16c session.
- Library CalVer `2026.07.472` to `2026.07.473`; [`README.md`](../../README.md) README Version `1.9.833` to `1.9.834`.

### Added

- [`.working/validate-sweeps/2026-07-16-sweep109-iter1.md`](../validate-sweeps/2026-07-16-sweep109-iter1.md) (new): the Sweep 109 per-iteration detail (worker B's A/B/C returns, the orchestrator elevated-QA synthesis, and the S109-N1 note plus fix).

### Verification

- Sweep 109 was OFFLOADED to credit-offload `worker-20260716-b` (Opus 4.8) as order `sweep-109-validate-2`, pinned to `28d4146b`/#984. (The pre-positioned `sweep-109-validate` came back BLOCKED on an unreachable pinned SHA before the maintainer had the worker clones resynced, so it was re-enqueued.) Worker B returned ZERO findings; the asserted-expectations cross-check was ALL corroborated / 0 contradicted; the loop-break control for #984 PASSES.
- Consumed under new-worker ELEVATED QA (fresh session, worker B's first QA-kind delivery): proof-of-run genuine; the orchestrator INDEPENDENTLY re-derived HEAD `28d4146b`, baseline 69/69, pre-flight 421/33/11, four-surface parity 69, and counts 13/23/14 (all EXACT-MATCH to the worker's claims); and a dedicated adversarial false-negative auditor re-verified every load-bearing CCPA citation and Quebec Law 25 figure at the held source, returning NO MISSED FINDING. Worker B elevated-QA: PASS (1 of 2-3 clean passes before routine trust).
- The one note the elevated-QA auditor raised (S109-N1) was verified at source and fixed in-window (see Changed above).
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before the first commit; pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green; a refute-briefed skeptical verifier ran on the annex diff before push.
- Per the loop-break, the prior session-closing handoff (#984) took no `/validate-pr` + `/retro`; this Sweep 109 IS that compensating control, so there is no #984 per-PR QA row to batch.

### Note (maintainer directives codified cross-repo)

- Two maintainer directives were codified in `grc_library_scratch` (the worker-exchange repository, not this repository, so no `grc_library` surface changed): the `/credit-offload` worker command now (1) resync-CHECKs whether it can reach the pinned `grc_library` revision when a worker picks up a task (delivering a BLOCKED result rather than running against a stale revision), and (2) staggers worker check-ins at 5/N-minute offsets across N live workers.

## 2026-07-16, Library Version 2026.07.472, PR #984

Session-closing handoff for the 2026-07-16b resumed session (#969-#983). Working-state only; no corpus, website, or gate change. Per the loop-break this PR takes no trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 109), PRE-POSITIONED as an offloaded worker order at this wind-down (the maintainer's optimization).

### Changed

- [`.working/session-handoff.md`](../session-handoff.md): new Next-actions / State-snapshot / Asserted-expectations blocks for #969-#983 - the large maintainer-authorized resume queue (the worker-process-improvement brief incl. the two open item-1 findings; the §2.22 Canada corpus apply; the 3 DELIVERED AI-annex seeds to build with the high-assurance harness; ETSI §3.14; the P6 builds; the deferred-protected backlog; the r4 deep-assessment continuation), green-at `69439833`. The older #955-#962 per-session blocks are left for the next `/resume` to prune (keep-current+1; over-retention is harmless).
- [`.working/session-state.md`](../session-state.md): concurrency lease RELEASED (Status `released`, Active-session `none`, heartbeat re-stamped).
- [`.working/session-metrics.md`](../session-metrics.md) (Version 1.0.60 to 1.0.61): the session row (QA dominantly OFFLOADED, so orchestrator-subagent tokens are a ~555K floor, not a total; ~1.98M est. orchestrator credits conserved across ~17 offloaded passes; the degradation-triggered wind-down recorded).
- Batched PR #983's `/validate-pr` (SHIP, offloaded to worker-b) into [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.747 to 1.2.748) and its `/retro` into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.682 to 1.0.683).
- Library CalVer `2026.07.471` to `2026.07.472`; [`README.md`](../../README.md) README Version `1.9.832` to `1.9.833`.

### Verification

- The wind-down was degradation-TRIGGERED (a false "test-proven, 5/5 PASS" claim on the item-1 helper fix, disproven by its refute-briefed skeptical verifier: the test was vacuous and there was a Medium abort-path bug). The buggy item-1 fix is UNMERGED (on scratch branch `helper-deliver-nondestructive-heartbeat-scope`); the two findings are recorded in the handoff for a fresh session to fix before merge.
- The asserted-expectations block records what this session mechanically verified (per-PR QA #969-#983, the CCPA §7121 anchors at the held source, the reference-base #87 gate-green) and the soft spots explicitly NOT asserted clean (item-1 buggy, §2.22 unapplied, the annexes unbuilt, the r4 phases 3-6 pending).
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before commit; pre-push guard (`run_all_audits.sh` + PR-time checks) green.

## 2026-07-16, Library Version 2026.07.471, PR #983

Working-state bookkeeping batch assembled during the unattended run, to record session state durably (against compaction) before the §2.22 corpus apply. No corpus, website, or gate change.

### Added

- [`.working/deep-assessment/2026-07-16-r4.md`](../deep-assessment/2026-07-16-r4.md) (new): the dated per-run record for `/deep-assessment` run **r4**, the first OFFLOADED deep-assessment (read-only probe phases run by credit-offload worker `worker-20260716-b`). PARTIAL and re-entrant: phases 1 / 2 / 4a / the phase-3 advisory aids COMPLETE (corpus GREEN 69/69, reference-modules clean, ledgers honest); the heavy phase-3 instruments + 4b/4c/4d + 5 + 6 deferred whole (not abbreviated).

### Changed

- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): new r4 row (Status in-progress; findings F-P2-1 + OBS-1; Phase 8 holds for maintainer sign-off) + per-run prose. The continuation (phases 3/4b-d/5/6) is to be enqueued after the §2.22 apply.
- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (Version 1.0.1 to 1.0.2): four consume rows (currency-classify ~85K, deep-assessment-r4-probe ~170K, ingest-prep ~140K, validate-pr-982 ~70K); roll-up updated to **~1.98M** est. orchestrator tokens conserved (17 with figures + 4 not captured).
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.746 to 1.2.747): the #982 `/validate-pr` row (SHIP; §7121 re-verified at source), AND the frozen #976 row's §7120->§7121 phasing correction (the phasing/timing is section 7121; §7120 is the threshold section), with an inline correction note.
- [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.681 to 1.0.682): the #982 `/retro` row (a 2nd-occurrence sub-section citation-precision pattern, after the (a)(16)->(a)(15) fix).
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): the frozen #976 detailed entry's "section 7120 ... phasing" disambiguated to "section 7120 thresholds and the section 7121 ... phasing".
- [`.working/credit-offload-design.md`](../credit-offload-design.md) (Version 1.3.2 to 1.3.3) and the [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) credit-offload section (maintainer-authorized protected edit): codify the **wind-down pre-positioning** of the resume corpus-wide `/validate` (enqueue it at wind-down pinned to the handoff-merge SHA so a worker can run it in the between-session gap; `/resume` checks the results plane first; best-effort, never trusts a stale/absent result).
- [`.working/maintainer-egress-requests.md`](../maintainer-egress-requests.md) (Version 1.0.1 to 1.0.2): queued a COMPLETE re-download of the AI Strategy FPS 2025-2027 full-text page (the fresh 2026-07-16 capture was a 17-page subset of the held 38-page version); moved the fulfilled Canada §2.22 block to Fulfilled.
- [`.working/session-state.md`](../session-state.md) + [`.working/next-prs.txt`](../next-prs.txt): refreshed; recorded the maintainer's four pre-loaded unattended-run decisions and the ordered NEXT queue (worker-process brief first).
- Library CalVer `2026.07.470` to `2026.07.471`; [`README.md`](../../README.md) README Version `1.9.831` to `1.9.832`.

### Verification

- Every finding recorded (F-P2-1, OBS-1) was re-verified at source by the orchestrator before recording; F-P2-1's fix (ref PR #87) was confirmed by the reference-base validation gate going green (696 items).
- The §7120->§7121 correction was verified against the held CCPA Regulations §7121 "Timing Requirements" and applied to every phasing carrier in the two frozen records (leaving the correct threshold references to §7120).
- The metrics roll-up arithmetic re-checked (prior ~1.51M + ~465K = ~1.98M).
- CLAUDE.md addition checked for em/en dashes and British spelling (the addition is clean; the file's other em-dashes are pre-existing and gate-exempt); [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before commit; pre-push guard green.

## 2026-07-16, Library Version 2026.07.470, PR #982

Precision tightening in the United States privacy annex: the California cybersecurity-audit phasing sentence now carries the per-tier measurement years. Surfaced by PR #976's `/validate-pr` NOTE 1 (tracked in TODO §2.23) and folded in for the expert review. Corpus body change (one annex), no gate or website change.

### Changed

- [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md) (Version 1.2.2 to 1.2.3): the cybersecurity-audit first-audit phasing sentence previously gave the three deadlines and dollar bands but named the measurement year only for the first tier (2026 revenue). Added the measurement years for the other two tiers: the 2029-04-01 deadline keys to a business's 2027 annual gross revenue (USD 50 to 100 million) and the 2030-04-01 deadline to its 2028 revenue (under USD 50 million). Deadlines and dollar bands were already correct, so this is precision, not a substance change.
- [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the Version bump ([`docs/portal.md`](../../docs/portal.md) carries no per-document version, so it is byte-identical and not in the diff).
- Batched PR #981's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md).
- [`TODO.md`](../../TODO.md) §2.23: the "Precision follow-up" (per-tier cyber-audit measurement years) is marked applied; the statute-currency half of §2.23 remains separately open.
- Library CalVer `2026.07.469` to `2026.07.470`; [`README.md`](../../README.md) README Version `1.9.830` to `1.9.831`.

### Verification

- The per-tier measurement years were re-verified at the CURRENT held source (the reference base's CCPA Regulations full-text extract, effective 2026-01-01), section 7121 "Timing Requirements" (April 1, 2028 keyed to 2026 revenue "more than one hundred million"; April 1, 2029 keyed to 2027 revenue "between fifty [and one hundred million]"; April 1, 2030 keyed to 2028 revenue "less than fifty million"), not from the finding note. (The phasing/timing is section 7121; section 7120 is the audit-requirement/threshold section. The annex body cites the "sections 7120 to 7124" range and attributes only the thresholds to 7120, so it is accurate; this precision was confirmed by the pre-push verifier.)
- Currency: the CPPA final regulations effective 2026-01-01 are the current version (the superseded 2025 draft is retained under `grc_library_ref/.superseded/`); the held current file was used.
- A refute-briefed skeptical verifier reviewed the one-line annex change and the version/generator co-bumps before push.
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before commit; pre-push guard (`run_all_audits.sh` + PR-time checks) green.

## 2026-07-16, Library Version 2026.07.469, PR #981

Records the `grc_library` side of the completed reference-acquisition task. The reference documents themselves were acquired by the credit-offload research workers and ingested into the private reference base as `grc_library_ref` pull requests #85 (four EDPB / WP29 GDPR soft-law items) and #86 (three Brazil ANPD resolutions, Argentina Decreto 1558/2001, and the Quebec anonymization regulation); `/tmp/grc_library_ref` was re-synced. This PR captures what belongs in `grc_library`: the sources that could not be fetched, the metrics-ledger consume rows, and the previous PR's quality-assurance result. Working-state and bookkeeping only; no corpus, website, or gate change.

### Added

- [`.working/maintainer-egress-requests.md`](../maintainer-egress-requests.md) (Version 1.0.0 to 1.0.1): a new "Egress-blocked ref-acquisition sources" block with the three items the workers could not fetch from this VM and deliberately did not substitute with an unofficial copy: Brazil ANPD Resolução CD/ANPD nº 32/2026 (in.gov.br, blocked), the US NYDFS Virtual Currency Regulation 23 NYCRR Part 200 (BitLicense; the full text is behind govt.westlaw.com), and Colombia Decreto Único Reglamentario 1074 de 2015 (funcionpublica.gov.co, unreachable). Each names its authoritative host and why the automated fetch failed; destination is `grc_library_ref/ingest/`.

### Changed

- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (Version 1.0.0 to 1.0.1): four consume rows added, `validate-pr-980` (~72K) plus the three `ref-acquire-*` research orders (token spend not captured), and the roll-up updated to **~1.51M estimated orchestrator tokens conserved (13 with figures + 4 not captured)**. The rise from ~1.44M is entirely the newly-consumed `validate-pr-980` pass; the #980 point-in-time records (its own CHANGELOG entry and improvement-log row) correctly stay at ~1.44M.
- [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.679 to 1.0.680): the PR #980 retro row's session-tally figure harmonized `~1.37M` to `~1.44M` (its point-in-time #980 truth), part of the validate-pr-980 finding fix.
- [`.working/session-state.md`](../session-state.md) and [`.working/next-prs.txt`](../next-prs.txt): rewritten fresh to the current state (merged #969-#980 + ref #85/#86, ref-acquisition COMPLETE, roll-up ~1.51M, heartbeat re-stamped, `Active-session: ref-acq-closeout-egress-metrics`), which also clears their stale `~1.37M` figures (the other two of the three surfaces the #980 quality-assurance pass flagged).
- Batched PR #980's `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.744 to 1.2.745) and its `/retro` row (already present) into [`.working/improvement-log.md`](../improvement-log.md).
- Library CalVer `2026.07.468` to `2026.07.469`; [`README.md`](../../README.md) README Version `1.9.829` to `1.9.830`.

### Fixed

- The validate-pr-980 LOW finding (`bookkeeping/session-tally-figure-drift`): three working-state surfaces (the session-state lease, the next-PRs file, the improvement-log #980 row) still read `~1.37M` while the ledger and #980 CHANGELOG read `~1.44M`. All three corrected (the two live-tally surfaces to the current `~1.51M` via their fresh rewrites, the point-in-time #980 row to `~1.44M`). Re-verified by a bare-token grep confirming the session-metrics ledger's `1.37M` is the unrelated 2026-06-27 batch-10 research figure and correctly untouched.

### Verification

- The three egress-blocked items were each confirmed unreachable from this environment before routing (in.gov.br HTTP 000, govt.westlaw.com 403, funcionpublica.gov.co HTTP 000); no unofficial substitute was ingested and no URL was fabricated.
- The metrics roll-up arithmetic re-checked: prior ~1.44M + validate-pr-980 ~72K = ~1.51M; the row count (13 with figures + 4 not captured) recounted against the ledger.
- validate-pr-980 was offloaded to `worker-20260716-b` (Opus 4.8, ROUTINE consume, 8th delivery); its one LOW finding re-verified at source and fixed here.
- New CHANGELOG prose checked for em/en dashes and British spelling; [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run before commit; pre-push guard (`run_all_audits.sh` + PR-time checks) green.

## 2026-07-16, Library Version 2026.07.468, PR #980

Adds a maintainer-requested credit-offload metrics tab: a running record of what the workers have done and, per session, the estimated orchestrator credits conserved by offloading passes to them. Working-state, design-of-record, and one CLAUDE.md convention line; no corpus, website, or gate change.

### Added

- [`.working/credit-offload-metrics.md`](../credit-offload-metrics.md) (new, Version 1.0.0): the running ledger. One row per offloaded delivery (order, kind, command, worker + model, the worker's best-effort estimated token spend as a conservative proxy for **estimated orchestrator credits conserved**, the consuming PR, and notes) plus a per-session roll-up. Backfilled for this session (12 deliveries with figures + 1 not captured; roll-up ~1.44M estimated orchestrator tokens conserved across the this-session-consumed set). The metric definition carries three explicit caveats: it is an estimate (workers cannot read an exact in-session count), credit-offload shifts cost across accounts rather than reducing total spend, and worker-spend is a conservative proxy (the Sweep-108 self-run comparable ~609K exceeded the ~237K worker spend).

### Changed

- [`.working/credit-offload-design.md`](../credit-offload-design.md) (Version 1.3.1 to 1.3.2): the `## Metrics and reporting` section now documents the orchestrator-side running tab, the ledger plus a short chat tally at each major activity (a worker delivering, a PR finishing), the metric, and the no-per-DONE-line choice.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Credit-offload mode`: a new "Metrics tab" bullet codifying the convention (maintainer-directed 2026-07-16; a protected-file touch, authorized on the local VM for the requested feature).
- Batched PR #979's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.678 to 1.0.679) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md).
- Library CalVer `2026.07.467` to `2026.07.468`; [`README.md`](../../README.md) README Version `1.9.828` to `1.9.829`.

### Verification

- The maintainer chose the shape (ledger + chat surface, no per-DONE line) and the metric (estimated orchestrator credits conserved) via `AskUserQuestion`; the design honours both.
- The backfill figures were read from each worker result's proof-of-run/token-spend section; four research deliveries carried no figure and are recorded as `not captured` (an honest gap, not zero).
- New prose (ledger, design-of-record section, CLAUDE.md bullet) checked for em/en dashes and British spelling before commit (CLAUDE.md is gate-exempt, so the check is manual there).
- Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean.

## 2026-07-16, Library Version 2026.07.467, PR #979

CCPA §2.23 slice 4 (breadth): adds the relevant final-CCPA-regulation section citations to four privacy framework-alignment tables, completing the `ccpa-regs-2026-alignment` regulations-alignment (the primary carriers were slices 1-3). Low-risk citation-breadth additions; every section anchor re-verified at the held regs and a refute-briefed skeptical verifier returned SHIP.

### Changed

- [`privacy/framework-consent-management.md`](../../privacy/framework-consent-management.md) (Version 1.0.9 to 1.0.10): the CCPA/CPRA framework-alignment row now cites 11 CCR s. 7004 (methods for submitting CCPA requests and obtaining consumer consent, including symmetry-in-choice and no-dark-patterns).
- [`privacy/framework-childrens-data.md`](../../privacy/framework-childrens-data.md) (Version 1.0.8 to 1.0.9): added a "CCPA / CPRA minor provisions" framework-alignment row citing 11 CCR ss. 7070-7072 (parental consent under 13 (s. 7070), affirmative opt-in for consumers at least 13 and under 16 (s. 7071), notices to consumers under 16 (s. 7072)).
- [`privacy/register-cookie-and-tracker.md`](../../privacy/register-cookie-and-tracker.md) (Version 1.0.5 to 1.0.6): the CCPA/CPRA row now cites 11 CCR ss. 7025-7026 (opt-out preference signals / the Global Privacy Control, and requests to opt out of sale/sharing).
- [`privacy/template-dsar-workflow.md`](../../privacy/template-dsar-workflow.md) (Version 1.1.4 to 1.1.5): the CCPA/CPRA row now cites 11 CCR s. 7021 (request-handling timelines) and ss. 7221-7222 (ADMT opt-out and access).
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the four Version bumps.
- [`TODO.md`](../../TODO.md) §2.23: the CCPA REGULATIONS-alignment half is now COMPLETE (primary carriers + breadth); the statute-currency half remains separately open.
- Batched PR #978's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.677 to 1.0.678) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md).
- Library CalVer `2026.07.466` to `2026.07.467`; [`README.md`](../../README.md) README Version `1.9.827` to `1.9.828`.

### Verification

- Each cited section's subject re-verified against the held CCPA regs body (s. 7004 consent methods; s. 7025 opt-out preference signals / GPC; s. 7026 opt-out of sale/sharing; s. 7070/7071/7072 minors bands and mechanic; s. 7021 timelines; ss. 7221-7222 ADMT).
- One refute-briefed skeptical verifier (external-facing citation tier) returned SHIP (all section subjects match, the minors age-bands correct, no overstatement, each edit alters only the CCPA/CPRA row).
- Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean.

## 2026-07-16, Library Version 2026.07.466, PR #978

CCPA §2.23 slice 3: propagates the final California CCPA regulations to the remaining primary carriers, the jurisdiction index, the privacy-notice template, and the data-subject-rights procedure. Completes the primary-carrier set of the `ccpa-regs-2026-alignment` delivery (slices 1-2 were the US annex and the ADM register). Every anchor and timeline re-verified at the held regs; a refute-briefed skeptical verifier returned SHIP.

### Changed

- [`privacy/annex-privacy-jurisdiction-index.md`](../../privacy/annex-privacy-jurisdiction-index.md) (Version 1.0.13 to 1.0.14): the cross-jurisdiction table's United States AI-obligation cell (C5) expanded from "ADMT opt-out (CPRA)" to "ADMT pre-use notice, opt-out, and access (final CCPA Regs 11 CCR ss. 7220-7222, eff 2026-01-01, compliance 2027-01-01)".
- [`privacy/template-privacy-notice.md`](../../privacy/template-privacy-notice.md) (Version 1.0.6 to 1.0.7): the automated-decision-making section (C6) gained a California pre-use-notice element (11 CCR s. 7220, may be provided in the Notice at Collection) covering the consumer's rights to opt out of and access the ADMT.
- [`privacy/procedure-data-subject-rights-management.md`](../../privacy/procedure-data-subject-rights-management.md) (Version 1.6.9 to 1.6.10): the "California (CCPA / CPRA) basis" paragraph (A5) gained the distinct CCPA ADMT rights beyond the GDPR-style human review, a right to opt out of ADMT (11 CCR s. 7221; opt-out given effect no later than 15 business days from receipt, s. 7221(n)) and a right to access ADMT (s. 7222), with the s. 7021 request-handling timeline (receipt confirmed no later than 10 business days; substantive response no later than 45 calendar days, extendable once to a 90-day maximum).
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the three Version bumps.
- Batched PR #977's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.676 to 1.0.677) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md).
- Library CalVer `2026.07.465` to `2026.07.466`; [`README.md`](../../README.md) README Version `1.9.826` to `1.9.827`.

### Verification

- Every anchor re-verified at the held CCPA regs: ss. 7001, 7220, 7221, 7221(n), 7222, 7021, Article 11; the 15-business-day opt-out-effect deadline (s. 7221(n)); the s. 7021 timeline (10 business days receipt confirmation, 45 calendar days response, 90-day maximum); the pre-use-notice-in-Notice-at-Collection permission (s. 7220); the 2026-01-01 / 2027-01-01 dates.
- One refute-briefed skeptical verifier (substantive external-facing corpus tier) returned SHIP; all edits touched only California CCPA context (no Canadian-CPPA / Bill-C-27 conflation).
- Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean.

## 2026-07-16, Library Version 2026.07.465, PR #977

CCPA §2.23 slice 2: aligns the automated-decision-making register to the final California CCPA regulations, correcting a statute-citation error and adding the CCPA ADMT subject rights. Continues the `ccpa-regs-2026-alignment` worker delivery (slice 1 = #976, the US privacy annex). Every anchor was re-verified at the held source and a refute-briefed skeptical verifier returned SHIP.

### Changed

- [`privacy/register-automated-decision-making.md`](../../privacy/register-automated-decision-making.md) (Version 1.0.6 to 1.0.7):
  - **Framework-alignment table, the "CCPA / CPRA" row (A4 accuracy fix + C4 currency):** corrected the enabling-statute citation from `Section 1798.185(a)(16)` to `Cal. Civ. Code s. 1798.185(a)(15)` (verified against the held statute: `(a)(15)` is "regulations governing access and opt-out rights with respect to a business' use of automated decisionmaking technology"; `(a)(16)` is the law-enforcement-investigation paragraph), and added the now-final operative regulations (11 CCR Article 11, ss. 7200-7222, effective 2026-01-01, compliance by 2027-01-01). Touched ONLY the California CCPA/CPRA row, NOT the Canadian "CPPA Section 19 (proposed)" (Bill C-27) row (acronym-collision guard).
  - **Subject rights section (A5):** added a California-CCPA item, the register's subject-rights list was GDPR-framed (human review, explanation, rectification) and did not carry the distinct CCPA ADMT rights. New item 8 states that for an ADMT making a "significant decision" (11 CCR s. 7001), subjects additionally have a pre-use notice (s. 7220), a right to opt out of ADMT (s. 7221), and a right to access ADMT (s. 7222), with the human-appeal exception in place of the opt-out (s. 7221(b)(1)), handled via the DSR workflow within the applicable regulatory window; compliance by 2027-01-01.
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the Version bump.
- [`TODO.md`](../../TODO.md) §2.23: status updated (regs-alignment half in progress, slices 1-2 done, slice 3 + breadth remaining; the statute-currency half still open).
- Batched PR #976's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.675 to 1.0.676) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md).
- Library CalVer `2026.07.464` to `2026.07.465`; [`README.md`](../../README.md) README Version `1.9.825` to `1.9.826`.

### Verification

- The `(a)(15)` fix and every regulation anchor (ss. 7001, 7200-7222, 7220, 7221, 7222, 7221(b)(1)) were re-verified against the held CCPA statute and regulations full-text extracts in `grc_library_ref`; the held regs themselves cite "s. 1798.185(a)(15) and Article 11", closing the loop.
- One refute-briefed skeptical verifier (substantive external-facing corpus tier) returned SHIP (no overclaim in item 8, human-appeal correctly framed as an alternative to the opt-out, acronym-collision confirmed avoided).
- Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean.

## 2026-07-16, Library Version 2026.07.464, PR #976

Aligns the United States privacy jurisdiction annex to the FINAL California CCPA regulations (11 CCR Division 6 Chapter 1, effective 2026-01-01), the first slice of the TODO §2.23 CCPA alignment (the `ccpa-regs-2026-alignment` worker delivery). Every section anchor, figure, and date was independently re-verified against the held regulation text before authoring, currency was confirmed upstream this cycle (cppa.ca.gov, which, unlike canada.ca, is fetchable from this environment), and a refute-briefed skeptical verifier returned SHIP.

### Changed

- [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md) (Version 1.2.1 to 1.2.2): the CCPA regulations are now final, not "under development" / "draft".
  - The state-laws CCPA bullet now states the CPPA final regulations (11 CCR Division 6 Chapter 1) took effect 2026-01-01, adding ADMT, risk-assessment, and cybersecurity-audit rules, with ADMT compliance for a significant decision required no later than 2027-01-01.
  - The "CCPA/CPRA automated decision-making" subsection was rewritten from draft framing into three source-anchored final-regulation bullets: **ADMT** (Article 11, sections 7200 to 7222: a pre-use notice (section 7220), a right to opt out of ADMT (section 7221), a right to access ADMT (section 7222), a human-appeal exception in place of the opt-out (section 7221(b)(1)), and the "significant decision" definition from section 7001, whose enumeration replaces the prior imprecise "employment, credit, health, housing, education" list); **risk assessments** (Article 10, sections 7150 to 7157, conducted *before initiating* the section 7150(b)-triggered processing); and **cybersecurity audits** (Article 9, sections 7120 to 7124), corrected from the prior text that conflated the audit and the risk assessment into one "before processing" test: the audit is a distinct, threshold-based, periodic obligation (section 7120 thresholds of 250,000 consumers or households, or 50,000 sensitive-PI consumers) with first audits phased by revenue (2028-04-01 / 2029-04-01 / 2030-04-01).
- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (Version 1.5.37 to 1.5.38): added a "US CCPA Regulations 2026" row (11 CCR Div 6 Ch 1, effective 2026-01-01, ADMT compliance 2027-01-01), distinct from the existing CCPA statute row; upstream check location `cppa.ca.gov/regulations/`, verified 2026-07-16.
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the two Version bumps (taxonomy first, then portal/scorecard; both `--check` clean).
- Batched PR #975's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.674 to 1.0.675) and its `/validate-pr` row into [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.739 to 1.2.740, a zero-findings pass; worker-b's elevated-QA window completed at 3 of 2-to-3, now routine). Marked the §3.83 validate-before-deliver nit CLOSED (the `/credit-offload` command now forces a pre-`deliver` scratch-gate house-style pass, done scratch-side this turn).
- Library CalVer `2026.07.463` to `2026.07.464`; [`README.md`](../../README.md) README Version `1.9.824` to `1.9.825`.

### Verification

- Every CCPA regulation anchor was re-verified against the held `grc_library_ref` full-text extract of the final CCPA Regulations, 11 CCR Div 6 Ch 1 (article headings, section numbers, the section 7001 "significant decision" enumeration, the section 7150 "before initiating" trigger, the section 7120 thresholds and the section 7121 2028-2030 phasing (the timing section; §7120->§7121 disambiguated in #983), the 2027-01-01 ADMT compliance date). The CCPA statute `(a)(15)`-vs-`(a)(16)` fix and the ADM register / DSR procedure carriers are NOT in this PR; they are the next §2.23 slice.
- Upstream currency confirmed this cycle via `cppa.ca.gov/regulations/` (CCPA Regulations effective 2026-01-01, from the September 2025 rulemaking package covering ADMT, risk assessments, cybersecurity audits, and insurance).
- One refute-briefed skeptical verifier (substantive external-facing corpus tier) returned SHIP after independently re-deriving every anchor; its one non-blocking fidelity note ("or households" on the 250,000 threshold) was applied.
- Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean.

## 2026-07-16, Library Version 2026.07.463, PR #975

Establishes a standing maintainer-egress channel and defers the TODO §2.22 Canada.ca reference-utilization apply on a confirmed currency blocker. Working-state and backlog only; no corpus, website, or gate change.

### Added

- [`.working/maintainer-egress-requests.md`](../maintainer-egress-requests.md) (new, Version 1.0.0): a standing queue of reference documents the assistant cannot fetch from this environment (egress-blocked hosts such as canada.ca, or paywalled/licensed sources). Per item it records the exact instrument title, issuing body, the held edition the ref base records, the ref path, the reason needed, and a URL only where a verified one is available (no fabricated URLs). Destination confirmed as `grc_library_ref/ingest/`. First batch: the ~16 Canada.ca instruments the §2.22 apply cites (the TBS AI/security/privacy suite, CCCS ITSP.80.022, OPC principles/disposal, the GC AI-program provenance sources, plus a note that CCCS ITSP.50.103 is not held). Maintainer-directed 2026-07-16.

### Changed

- [`TODO.md`](../../TODO.md) §2.22 status line: **DEFERRED-BLOCKED on currency.** canada.ca returns a WAF access-rejection to this environment (confirmed 2026-07-16 against `tbs-sct.canada.ca`; the DD-10 egress limitation), so neither the orchestrator nor a worker can re-verify the in-force versions of the 49 Canada.ca sources at apply, and the apply is bound for a Canada expert review. The maintainer elected to personally download fresh copies (via the egress-requests file); §2.22 proceeds (split into per-domain PRs, respecting the sector-neutrality placement caveat and the register-canonical-citations row precondition) once they land.
- [`.working/pending-decisions.md`](../pending-decisions.md): added the §2.22 deferral entry (what blocks it, the maintainer decision, what unblocks it).
- Batched PR #974's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.673 to 1.0.674): a two-friction row (the #974 next-prs miss; worker-b's house-style-tripping delivered result prose), both caught in-window, both routed.
- **Consumed the offloaded `validate-pr-974` result** (worker-b delivery 2, graduated elevated QA) and recorded its row in [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.738 to 1.2.739). It returned **one real finding (F1, LOW)**: the credit-offload design-of-record claim-precedence bullet OVERCLAIMED the serve-loop (it asserted a non-blocking priority-1 `/validate-pr` is taken "regardless of role", but the `/credit-offload` command elevates only `blocking` orders above the role-kind preference). Re-verified at the scratch command source and **fixed here**: [`.working/credit-offload-design.md`](../credit-offload-design.md) (Version 1.3.0 to 1.3.1) narrowed to the loop's actual guarantee, with the optional "give all priority-1 orders precedence over role" strengthening tracked in §3.83; and the #974 root + detailed CHANGELOG echoes of the overclaim corrected in place (the #974 detailed "does not overclaim" bullet carries an explicit flagged correction). The offload independence caught an overclaim the orchestrator introduced and missed; worker-b's elevated-QA window is now 2 of 2-to-3 (a correct finding is a sound pass, not a reset).
- [`TODO.md`](../../TODO.md) §3.83: folded in two credit-offload tooling nits (the scratch `/credit-offload` delivery step does not force a pre-`deliver` validate run, so a worker can push a house-style-tripping result that reddens scratch CI; and the serve-loop should give all priority-1 orders, not only `blocking` ones, precedence over the role preference, the F1 strengthening). §3.85: folded in `validate-pr-974` OBS-B (the shared `/tmp` cache is not writable across Unix users, so a per-worker read-clone is needed for permission isolation too, applying to both the `grc_library` and `grc_library_ref` caches).
- Refreshed [`.working/next-prs.txt`](../next-prs.txt) and the [`.working/session-state.md`](../session-state.md) lease (heartbeat, unattended-mode note, merged-through #974, worker-b elevated-QA 2-of-2-to-3).
- Library CalVer `2026.07.462` to `2026.07.463`; [`README.md`](../../README.md) README Version `1.9.823` to `1.9.824`.

### Verification

- Confirmed the canada.ca block first-hand (a WebFetch of a `tbs-sct.canada.ca` document URL returned a WAF access-rejection) rather than asserting the block from the worker's report alone.
- Pulled the ~16 instruments' exact titles and held editions from the `grc_library_ref` catalogue; listed the two URL leads that extraction produced reliably and left the rest as title-only (no fabricated URLs).
- Working-state + backlog + version + CHANGELOG only; no corpus body, gate, or generated artefact touched. Pre-push guard (69 gates + PR-time checks) green; the CHANGELOG preflight aid clean. Bookkeeping tier, so no standing skeptical verifier.

## 2026-07-16, Library Version 2026.07.462, PR #974

Codifies two credit-offload worker-behaviour models into the design of record and opens a backlog item to close a reference-read gap the codification surfaced. Working-state and backlog only; no corpus, website, or gate change.

### Added

- [`.working/credit-offload-design.md`](../credit-offload-design.md) design-of-record (Version 1.2.0 to 1.3.0): a `## Worker allocation and specialization (one-at-a-time + role-based soft split)` section (one order at a time; the maintainer's initial hard QA/research split refined into a SOFT split that prefers the worker's `role` but falls back to any eligible order so a live worker never idles beside serveable work; the egress-natural bias, research needs egress and qa is `egress-none`; and the claim precedence, where a blocking order outranks the role preference), and a `### Reference-read basis and multi-worker resync` subsection recording the current shared-`/tmp/grc_library_ref` read gap (a ref update mid-order silently changes what a running worker reads, since the ref read is not pinned to the order's `grc_library_ref_sha` the way the `grc_library` read is) and the target per-order-pinned model. Also extended the order-schema prose to list `capability-needs` and to name the worker-registry `role` attribute.
- [`TODO.md`](../../TODO.md) §3.85 (credit-offload thread-5): the worker reference-read model + multi-worker resync coordination item that closes the gap the design-doc subsection documents; P3 `Next item number` counter advanced 3.85 to 3.86.

### Changed

- Batched PR #973's `/retro` row into [`.working/improvement-log.md`](../improvement-log.md) (Version 1.0.672 to 1.0.673): a clean row (no new pattern, no proposed improvement; the first worker-sourced corpus edit was first-pass clean through preflight, the guard, and the verifier, and proved the worker-delivery consume path for corpus edits).
- Recorded PR #973's OFFLOADED `/validate-pr` result in [`.working/validate-pr/history.md`](../validate-pr/history.md) (Version 1.2.737 to 1.2.738): a zero-findings pass by credit-offload worker `worker-20260716-b`, which was worker-b's FIRST QA delivery and therefore validated under FULL ELEVATED QA (proof-of-run genuineness; independent re-derivation of the SHAs and diff scope, all exact-match; re-verification of all four Quebec Law 25 figures at the held CQLR P-39.1 source; and a dedicated adversarial false-negative auditor returning WORKER-CLEAN-CONFIRMED). This is what unblocks #974 (gate 50 requires the per-PR QA row before the next PR can ship).
- Refined [`TODO.md`](../../TODO.md) §3.84 with two verified observations from that `/validate-pr` pass: OBS-1 added a second `section 3.3` carrier (`privacy/template-dpia.md:25`, not only :204), and OBS-2 resolved the item's original "confirm 12.1" uncertainty (s. 12.1 IS the automated-decision-making provision per the held source, so the ADM citation is correct and only the PIA `3.3` -> `23.3` correction is needed).
- Library CalVer `2026.07.461` to `2026.07.462`; [`README.md`](../../README.md) README Version `1.9.822` to `1.9.823`.

### Verification

- The design-doc claim-precedence prose was cross-checked against the actual `grc_library_scratch` credit-offload serve-loop command and corrected to match it (an over-specific "then oldest-queued" tiebreak the loop does not instruct was removed) before commit. (Correction flagged in #975: a SECOND overclaim of the same class survived this cross-check, the "non-blocking priority-1 `/validate-pr` taken regardless of role" claim, which the serve-loop makes only for `blocking` orders; it was caught by `validate-pr-974` (worker-b, F1) and fixed in #975. This bullet's original "does not overclaim" assertion was therefore not fully accurate as of #974.)
- Working-state + backlog + version + CHANGELOG only; no corpus body, gate, or generated artefact touched. Pre-push guard (69 gates + PR-time checks D1-D7 and gates 45/40/31) green; the CHANGELOG preflight aid clean. Quick-fix/bookkeeping tier, so no standing skeptical verifier (per the tiered pre-push standard).

## 2026-07-16, Library Version 2026.07.461, PR #973

Corrects a material Quebec Law 25 penalty-structure error and two related accuracy issues in the Canada privacy jurisdiction annex, applied from a credit-offload worker's `canada-annexes-source-verification` research delivery after the orchestrator independently re-verified every corrected figure against the held Quebec Law 25 text (the research-assistant discipline; expert-review-facing Canada content, high accuracy bar). Corpus content changed (one privacy annex + regenerated artefacts).

### Fixed
- [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md) Quebec Law 25:
  - **Penalty structure (material):** the annex presented the CAI administrative monetary penalty as two tiers with a "CAD 25 million or 4% (more serious)" second tier. That figure is the PENAL FINE (s. 91), not a second administrative tier. Corrected per held s. 90.12 to a single administrative cap (the greater of CAD 10 million or 2% of worldwide turnover; natural persons up to CAD 50,000), and moved the CAD 25M / 4% figure to the penal-fine line (s. 91: organizations CAD 15,000 to 25,000,000 or, if greater, 4% of worldwide turnover; natural persons CAD 5,000 to 100,000). Resolves the double-count.
  - **PIA scope:** narrowed the general PIA duty from "any project involving personal information" to the held s. 23.3 scope ("acquire, develop, or overhaul an information system or electronic service delivery system involving personal information"), at both the key-provisions bullet and the PIA line, and noted the separate s. 17 cross-border-transfer PIA.
  - Version 1.1.2 to 1.1.3; Date to 2026-07-16.

### Changed
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the annex Version bump (taxonomy first, then portal/scorecard; both `--check` clean).
- Batched PR #972's `/validate-pr` + `/retro` rows, and fixed its `/validate-pr`'s two in-window findings: the [`TODO.md`](../../TODO.md) P3 "Next item number" counter (left at `3.82` though #972 assigned §3.82 AND §3.83; a permanent-numbering-rule violation risking number recycling) advanced to `3.85`, and the [`.working/session-state.md`](../session-state.md) Current-task line (stale, still referencing "#971") refreshed to the current state.
- [`TODO.md`](../../TODO.md): added §3.84 (a pre-existing Quebec Law 25 PIA/ADM citation-section inconsistency, "s. 3.3"/"12.1" vs the held s. 23.3 / s. 17, in three other documents, surfaced by this PR's verifier as an out-of-scope observation; routed as a reference-alignment follow-up).
- Library CalVer `2026.07.460` to `2026.07.461`; [`README.md`](../../README.md) README Version `1.9.821` to `1.9.822`.

### Verification
- Every corrected figure independently re-verified at the held source: s. 90.12 (single admin cap, greater of CAD 10M or 2%, natural persons CAD 50,000), s. 91 (penal fine, orgs CAD 15,000-25,000,000 or 4%, natural persons CAD 5,000-100,000), s. 23.3 (system-project PIA scope) all confirmed verbatim against `grc_library_ref` Quebec Law 25. A refute-briefed skeptical verifier checked faithfulness + any residual/parallel carrier of the old framing corpus-wide.
- `tools/run_all_audits.sh` + `tools/run-pr-time-checks.sh` green at the pre-push guard; generators `--check` clean.
- The worker's other findings (citation-breadth additions; the AI-annex fourth-review confirmation; the not-held/upstream flags: AIDA lapse currency, EU adequacy, the Quebec 60-day biometric notice living in the unheld LCCJTI, the ref INDEX "third-review" descriptor defect) are recorded for follow-up, not applied here (this PR is the verified accuracy corrections only). This PR's own `/validate-pr` is OFFLOADED to the credit-offload qa worker.

## 2026-07-16, Library Version 2026.07.460, PR #972

Adds two credit-offload-thread backlog items and batches PR #971's post-merge QA. Working-state and [`TODO.md`](../../TODO.md) only; no corpus or website content changed.

### Added
- [`TODO.md`](../../TODO.md) **§3.82** (credit-offload worker degradation check + in-session self-restart): give workers a named degradation signal and a lightweight self-restart (`/clear` then re-invoke `/credit-offload`, which re-registers and reconciles held orders via the fencing-token hook), since a worker holds no durable authorial state and needs no orchestrator-style handoff (maintainer-flagged 2026-07-16).
- [`TODO.md`](../../TODO.md) **§3.83** (worker-lifecycle-hooks verifier follow-up): the narrow shared-VM worktree-prune TOCTOU race the adversarial verifier flagged (re-fetch the keep-set before pruning, or per-worker worktree caches) plus two nits, documented in the scratch repo's queue-protocol README.

### Changed
- [`.working/validate-pr/history.md`](../validate-pr/history.md): batched the #971 row (self-run, since the worker was on the maintainer's priority acquisition tasks). Version 1.2.735 to 1.2.736.
- [`.working/improvement-log.md`](../improvement-log.md): batched the #971 `/retro` row. Version 1.0.670 to 1.0.671.
- [`.working/session-state.md`](../session-state.md): lease heartbeat re-stamp + `Active-session` update.
- [`.working/next-prs.txt`](../next-prs.txt): cycled forward.
- Library CalVer `2026.07.459` to `2026.07.460`; [`README.md`](../../README.md) README Version `1.9.820` to `1.9.821`.

### Verification
- `tools/run_all_audits.sh` 69/69 + `tools/run-pr-time-checks.sh` green at the pre-push guard (bookkeeping-tier; no separate pre-push verifier). #971's self-run `/validate-pr` Subagent A result batched here.
- No corpus document body changed; no per-document Version/Date bump; no generated-artefact regeneration. This PR's own QA batches forward per recursion-avoidance.

## 2026-07-16, Library Version 2026.07.459, PR #971

The **Sweep 108 `/validate` close-out** (the loop-break compensating control for session-closing handoff PR #968), plus the two validated worker findings applied and PR #970's post-merge QA batched. Working-state and [`TODO.md`](../../TODO.md) only; no corpus or website content changed. Sweep 108 was the FIRST OFFLOADED corpus-wide `/validate` (run on worker `worker-20260716-a`, orchestrator-validated under full elevated QA including an adversarial auditor that returned WORKER-CLEAN-CONFIRMED); the loop-break control for #968 passes.

### Changed
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): added the Sweep 108 row (0 error / 0 warning / 1 note; offloaded + orchestrator-validated; loop-break for #968 passes); Version 2.0.106 to 2.0.107.
- [`.working/session-handoff.md`](../session-handoff.md): advanced the Resume-cursor to Sweep 108 (gate 45), and **pruned** the per-session blocks to keep current + 1 prior (retained the #964-#967 and #955-#962 stacks; dropped the #943-#953 website-session Next-actions / State-snapshot / Asserted-expectations blocks, whose narrative is preserved in the CHANGELOG, DONE, sweep history, and git).
- [`TODO.md`](../../TODO.md): applied the two validated Sweep-108 / validate-pr-969 worker findings to §3.80: the phase-1 completion date `2026-07-15` to `2026-07-16` (the UTC date; scratch PR #168 merged 2026-07-15 21:51 EDT = 2026-07-16 01:51 UTC), and added the omitted `verify` to the offloadable-pass list (matching the design doc and CLAUDE.md). Added §2.23 (CCPA statute eff. 2026-01-01 currency + alignment review, blocked on the ref ingestion; maintainer-flagged 2026-07-16).
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the #970 row (self-run PR-scoped sweep; the worker was on the maintainer's priority Canada + CCPA-ingestion work). Version 1.2.734 to 1.2.735.
- [`.working/improvement-log.md`](../improvement-log.md): added the #970 `/retro` row (logs the process-PR-QA-spend-vs-busy-single-worker pattern). Version 1.0.669 to 1.0.670.
- [`.working/session-state.md`](../session-state.md): re-stamped the lease heartbeat, moved `Active-session` to `claude/sweep108-closeout`, recorded the close-out state and the CCPA ref-update tracking.
- [`.working/next-prs.txt`](../next-prs.txt): cycled forward.
- Library CalVer `2026.07.458` to `2026.07.459`; [`README.md`](../../README.md) README Version `1.9.819` to `1.9.820`.

### Verification
- `tools/run_all_audits.sh` 69/69 and `tools/run-pr-time-checks.sh` green at the pre-push guard (bookkeeping-tier close-out; no separate pre-push skeptical verifier). Gate 45 confirms the Resume-cursor matches the new Sweep 108 history row.
- The Sweep 108 result was independently validated before this close-out recorded it (SHAs, counts, gate 54, and pre-flight all exact-match; the one note re-verified at source; adversarial auditor WORKER-CLEAN-CONFIRMED). The two applied findings were each re-verified at source, and the phase-1 date resolution was confirmed against the actual scratch #168 merge timestamp.
- No corpus document body changed; no per-document Version/Date bump; no generated-artefact regeneration. This close-out's own `/validate-pr` + `/retro` batch forward per recursion-avoidance.

## 2026-07-16, Library Version 2026.07.458, PR #970

Codifies the **credit-offload new-worker QA-trust-tier policy** (maintainer-directed 2026-07-16, after the first live worker's first QA deliveries) and batches PR #969's offloaded-and-validated post-merge QA rows. `.claude/` + `.working/` only; no corpus or website content changed. Context: this session's Sweep 108 `/validate` and #969 `/validate-pr` were both offloaded to worker `worker-20260716-a` (Opus 4.8) and independently validated by the orchestrator (delivery 1 under full elevated QA including an adversarial auditor that returned WORKER-CLEAN-CONFIRMED; delivery 2 under graduated elevated QA); the worker is validated-as-working and the loop-break control for #968 passes (its close-out is the next PR).

### Added
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Credit-offload mode`: a "New-worker QA-trust tiers (ELEVATED then routine)" bullet. A worker's clean QA result is a trust assertion, re-established each session and keyed on `(worker-id + model)` (a model change re-triggers it); it applies to QA-kind deliveries only (research/draft seeds already get full re-authoring at apply). The first 2-to-3 QA-kind deliveries per `(worker + model)` per session get elevated QA (proof-of-run genuineness, independent re-derivation of mechanical facts, re-verify every finding, and a graduated adversarial auditor: full auditor on delivery 1, steps 1-to-3 on 2-to-3). The count is a floor not a cap; any confirmed miss/sham/scope-error resets the window, escalates, and marks the worker unvalidated. Honest limitation stated (raises the bar, does not guarantee detection; independent re-derivation is the load-bearing guard).

### Changed
- [`.working/credit-offload-design.md`](../credit-offload-design.md): added the "New-worker QA-trust tiers" subsection to the trust model (the design-of-record for the CLAUDE.md bullet); Version 1.1.0 to 1.2.0.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the #969 row, recording that its `/validate-pr` was OFFLOADED to `worker-20260716-a` (scratch order `validate-pr-969`), returned 1 note (`verify` enum drift, routed to the Sweep 108 close-out), and was validated under elevated QA; the worker also caught a real orchestrator error (a SHA-field typo in the order). Version 1.2.733 to 1.2.734.
- [`.working/improvement-log.md`](../improvement-log.md): added the #969 `/retro` row (the credit-offload machine exercised end-to-end; the offload's independence caught an orchestrator error the inline verifier could not see). Version 1.0.668 to 1.0.669.
- [`.working/session-state.md`](../session-state.md): re-stamped the lease heartbeat, moved `Active-session` to `claude/credit-offload-worker-qa-policy`, and recorded the worker-validation state and the elevated-QA-window count (2 of 2-to-3 done, both clean).
- [`.working/next-prs.txt`](../next-prs.txt): cycled forward (Sweep 108 close-out next).
- Library CalVer `2026.07.457` to `2026.07.458`; [`README.md`](../../README.md) README Version `1.9.818` to `1.9.819`.

### Verification
- `tools/run_all_audits.sh` 69/69 and `tools/run-pr-time-checks.sh` green at the pre-push guard. A refute-briefed skeptical verifier ran on the policy prose (CLAUDE.md bullet + design-doc subsection internally consistent, no QA-skip loophole introduced).
- The worker-validation evidence backing the #969 QA row: independent re-derivation of the worker's Sweep 108 claims (the five in-window SHAs, counts 13/23/14/18, gate 54 clean 336 docs, pre-flight 421/11/33) all exact-match; the one Sweep 108 note (phase-1 date drift) and the one validate-pr-969 note (`verify` enum drift) both re-verified real at source; an adversarial false-negative auditor returned WORKER-CLEAN-CONFIRMED.
- No corpus document body changed; no per-document Version/Date bump; no generated-artefact regeneration. This PR's own `/validate-pr` + `/retro` batch forward per recursion-avoidance.

## 2026-07-16, Library Version 2026.07.457, PR #969

Applies credit-offload **phase 3** (the deferred-protected-changes staging item 10; maintainer-authorized attended on the VM): the orchestrator-side wiring of the multi-worker QA-and-research offload queue into the resume flow and the project instructions. First PR of the 2026-07-16 resumed session; the mandatory loop-break Sweep 108 `/validate` (#964..#968) is itself OFFLOADED to the live worker `worker-20260716-a` as the credit-offload test (enqueued as the blocking, priority-0 order `sweep-108-validate` on `grc_library_scratch`), so its close-out (the sweep row + handoff prune) lands when the worker delivers, not in this PR. `.claude/` + `.working/` + backlog only; no corpus or website content changed.

### Added
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a new `## Credit-offload mode` section (after `## Multi-session orchestration`) codifying the orchestrator-side discipline: the offloadable read-only pass set vs what stays orchestrator-side (authoring/apply/route/merge + the pre-push skeptical verifier per §3.81); the worker-availability gate (enqueue when >= 1 live worker, self-run on an empty pool, best-effort and never a QA skip); the blocking resume `/validate` vs the non-blocking per-PR passes; the consume/trust discipline (re-verify positives, trust clean, orchestrator writes the audit-trail rows); the honest cost-shifting limitation; the `/tmp/grc_library_ref` worker-read-copy re-sync obligation; and the note that the `/credit-offload` worker command lives in `grc_library_scratch`, so the `grc_library` slash-command count is unchanged (still 14).

### Changed
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): step 6 now leads with the credit-offload check (read the scratch `workers/` registry; with a live worker, enqueue the loop-break `/validate` as a blocking priority-0 order pinned to the resume `main` SHA, wait on the results plane, consume + re-verify positives + record the sweep row; with 0 workers or a stale order, self-run inline); step 3 gains a credit-offload queue/results check alongside the brief-freshness and delivery-status probes.
- [`.working/credit-offload-design.md`](../credit-offload-design.md): Status to IN USE, phase 3 marked APPLIED and phase 2 marked under live test; added the worker wind-down/re-register design-of-record note (the two light hooks, worktree cleanup on wind-down/crash and reconcile-on-re-register, plus the serve-loop self-refresh and the intra-order-checkpoint non-goal) from `worker-20260716-a`'s `worker-lifecycle-winddown` design assessment; Version 1.0.1 to 1.1.0.
- [`TODO.md`](../../TODO.md): §3.80 phase-3 sub-item rotated to APPLIED; phase 2 marked in-progress (the two hooks + self-refresh + live write-path test); §3.80 stays open pending phase-2 hardening.
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 10 rotated out (landed note added to the summary); items 6, 8, 9 remain.
- [`.working/session-state.md`](../session-state.md): ACQUIRED the concurrency lease for `claude/credit-offload-phase3` (`Status: active`, fresh heartbeat); Current-task and Worker-dispatches updated for this session.
- Library CalVer `2026.07.456` to `2026.07.457`; [`README.md`](../../README.md) README Version `1.9.817` to `1.9.818`.

### Verification
- `tools/run_all_audits.sh` 69/69 and `tools/run-pr-time-checks.sh` green at the pre-push guard. A refute-briefed skeptical verifier ran on the resume-flow prose change (the `/resume` step-6/step-3 edits and the new CLAUDE.md section read coherently end-to-end and are internally consistent with the design of record and the mandatory-QA discipline).
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration.
- This PR's own `/validate-pr` (the Subagent-A analysis pass) is OFFLOADED to the worker (the credit-offload model) and consumed at the next PR boundary; the `/retro` stays orchestrator-side (a reflective pass, not in the offloadable set, like the audit-trail-row writing). Both rows batch forward per recursion-avoidance.

## 2026-07-16, Library Version 2026.07.456, PR #968

Session-closing handoff for the 2026-07-16 resumed session (`/resume` from #963; merged #964-#967 plus `grc_library_scratch` #166-#170). Working-state only; no corpus or website content changed. Per the loop-break, this handoff PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 108), which cross-checks the Asserted-expectations block this PR records.

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): prepended this session's Next-actions (CLOSING + the NEXT-SESSION plan, whose first substantive task is credit-offload phase 3, ask the maintainer about the deferred-protected-changes staging item 10 first), State-snapshot, and Asserted-expectations blocks.
- [`.working/overnight-pr.md`](../overnight-pr.md): reset from a stale `in-flight` (left by a 2026-07-15 #929-#936 run that was never routed) to `stub`, per the mode-exit "route and reset the overnight file" cleanup; the #929-#936 content was build-progress narrative already recorded per-PR, no un-routed design decision remained.
- [`.working/session-state.md`](../session-state.md): RELEASED the concurrency lease (`Active-session: none`, `Status: released`, fresh heartbeat).
- [`.working/session-metrics.md`](../session-metrics.md): added this session's row (measured ~1.32M subagent tokens across 7 re-retrievable dispatches, all re-retrievable so a true total not a floor; orchestrator tokens `not instrumented`); Version 1.0.59 to 1.0.60.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the #967 row (SHIP, 0 findings) and the #968 handoff row (SKIPPED, handoff-PR exception in the Findings cell); Version 1.2.732 to 1.2.733.
- [`.working/improvement-log.md`](../improvement-log.md): added the #967 `/retro` row (no #968 `/retro` per the loop-break); Version 1.0.667 to 1.0.668.
- [`.working/next-prs.txt`](../next-prs.txt): cycled to the next session's queue (Sweep 108, then credit-offload phase 3).
- Library CalVer `2026.07.455` to `2026.07.456`; [`README.md`](../../README.md) README Version `1.9.816` to `1.9.817`.

### Verification
- `tools/run_all_audits.sh` 69/69 at the pre-push guard. PR #967's PR-scoped sweep returned SHIP / 0 findings. This handoff PR skips its own trailing QA (loop-break); the next `/resume` runs Sweep 108 over #964..#968.
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration. The credit-offload build lives on `grc_library_scratch` (#166-#170); phase 3 is staged for maintainer review as the deferred-protected-changes staging item 10.

## 2026-07-16, Library Version 2026.07.455, PR #967

Adds the Canada.ca reference-utilization plan to the backlog (Canada-priority for the imminent expert review) and batches PR #966's post-merge QA. Working-state records and backlog only; no corpus or website content changed. Second PR of the overnight run, after the credit-offload build.

### Added
- [`TODO.md`](../../TODO.md) §2.22 (Priority 2, `H`, `L`): Canada.ca reference utilization, systematic engagement of the 49 newly-held Canada.ca authoritative sources (ref PRs #80/#81/#82: the TBS AI-governance suite, OSFI B-13/E-23, the Privacy Act / OPC / PIPEDA set, ITSG-33 / CCCS ITSP.80.022 / the GC cloud profile / the Pan-Canadian Trust Framework, and the TBS public-sector policy/directive suite) across the Canada AI annex, the privacy annex, the compliance matrix, and the security baselines, flagged Canada-priority because Canadian experts review the corpus in the next few days. Its research half is delivered as three priority-1 credit-offload seeds on `grc_library_scratch` (`canada-ca-reference-breadth`, `canada-annexes-source-verification`, `canada-matrix-fit`) for tomorrow's workers; the apply is orchestrator validate-then-apply per delivery. P2 counter advanced to 2.23.

### Changed
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the PR #966 row (see the row for the sweep outcome).
- [`.working/improvement-log.md`](../improvement-log.md): added the PR #966 `/retro` row (three guard-caught authoring slips incl. a new row-merge sub-shape that reinforces TODO §3.73; WATCH continues).
- [`.working/next-prs.txt`](../next-prs.txt), [`.working/session-state.md`](../session-state.md): overnight queue + lease heartbeat.
- Library CalVer `2026.07.454` to `2026.07.455`; [`README.md`](../../README.md) README Version `1.9.815` to `1.9.816`.

### Fixed
- [`.working/credit-offload-design.md`](../credit-offload-design.md) (the 2 low-severity notes PR #966's PR-scoped sweep found, both in this gate-exempt working doc): (1) a broken internal section-anchor, the Status line pointed at `## Build status` but the section is titled `## Build phases`; (2) a build-status overstatement, the Status line read "phases 2-3 partially built" while phase 3 is STAGED not built (per the doc's own Build-phases section and TODO §3.80). The Status line and the Phase 1/2 markers were reworded to the accurate current state (phases 1 and the initial phase-2 worker command built on scratch PR #168, a worker testable; phase 2 write-path hardening pending; phase 3 staged). Version 1.0.0 to 1.0.1.

### Verification
- `tools/run_all_audits.sh` 69/69 at the pre-push guard. PR #966's PR-scoped sweep (Subagent A, read-only-git on the #966 squash) found 2 low-severity self-consistency notes in the new credit-offload design doc, both fixed in this PR (see Fixed); all other classes clean (TODO consistency, version/date coherence, the improvement-log row separation, CHANGELOG hygiene).
- The three Canada credit-offload seeds were queued on scratch (PRs #168 and #169) and the queue helper's read commands smoke-tested; the Canada apply work is orchestrator validate-then-apply once the workers deliver.
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration.

## 2026-07-16, Library Version 2026.07.454, PR #966

Records the credit-offload design (maintainer-co-designed across the 2026-07-15 session) and opens its backlog, and batches PR #965's post-merge QA. Working-state records and backlog only; no corpus or website content changed. This is the first PR of the overnight run (maintainer entered overnight mode 2026-07-15).

### Added
- [`.working/credit-offload-design.md`](../credit-offload-design.md): the design of record for credit-offload, a multi-worker QA + research queue on `grc_library_scratch` that offloads the read-only analysis passes and research/drafting seeds to worker sessions on other accounts. Covers the offloadable/on-account split, the scratch-git-coordination + `/tmp` clone-cache topology (split-brain-free across a VM+cloud worker mix), the lease/fencing lifecycle (5-min heartbeat / 20-min stale; fencing token rejects a stale worker's late delivery), the `workers/` liveness registry + best-effort/self-run fallback, token-budget-aware graceful checkout (best-effort, fencing backstop), the order schema, metrics, and the phased build. Version 1.0.0.
- [`TODO.md`](../../TODO.md): three items. §1.15 (Priority 1, cross-repo write-safety guardrail: a fail-loud repo-asserting git wrapper + a standing confirm-the-repo-before-write convention, prompted by the 2026-07-15 cwd-persistence incident where a grc_library-intended `git checkout main && git pull` ran in `grc_library_scratch`). §3.80 (the credit-offload build, phased; phase 1 built on scratch, phase 3 staged). §3.81 (periodic reassessment of keeping the pre-push verifier on-account). P1 counter advanced to 1.16; P3 counter to 3.82.

### Changed
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): staged item 10, the credit-offload phase-3 orchestrator-side wiring (a worker-availability check in the `/resume` command plus a blocking loop-break `/validate` enqueue; a credit-offload-mode section in the project CLAUDE.md instructions), for maintainer review rather than unattended application (maintainer-directed 2026-07-15). On overnight exit the assistant pauses and reminds the maintainer to read this staged file, which lives in the `grc_library` repo's working state.
- [`.working/multi-session-orchestration.md`](../multi-session-orchestration.md): added a credit-offload cross-reference to the design doc; Version 1.1.8 to 1.1.9.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the PR #965 row (Subagent A SHIP, 0 findings); Version 1.2.730 to 1.2.731.
- [`.working/improvement-log.md`](../improvement-log.md): added the PR #965 `/retro` row (the read-before-asserting win on the AICM defect; a WATCH on pending-decisions-entry staleness, 2nd occurrence); Version 1.0.665 to 1.0.666.
- [`.working/next-prs.txt`](../next-prs.txt), [`.working/session-state.md`](../session-state.md): overnight queue + lease heartbeat.
- Library CalVer `2026.07.453` to `2026.07.454`; [`README.md`](../../README.md) README Version `1.9.814` to `1.9.815`.

### Verification
- `tools/run_all_audits.sh` 69/69 at the pre-push guard; `/validate-pr` #965 returned SHIP / 0 findings; the AICM-resolution re-verification confirmed all 7 codes against the held CSA AICM v1.1.0 titles.
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration. The credit-offload phase-1/2 build (the scratch queue + `/credit-offload` worker command) lands separately on `grc_library_scratch`.

## 2026-07-15, Library Version 2026.07.453, PR #965

Batches PR #964's post-merge QA and closes task 1 ("correct issues") of the 2026-07-15 resumed session's maintainer-set running order. Working-state records only; no corpus or website content changed.

### Changed
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the PR #964 row (Subagent A SHIP, 0 findings, read-only-git on squash `9e5c7e5`); Version 1.2.729 to 1.2.730.
- [`.working/improvement-log.md`](../improvement-log.md): added the PR #964 `/retro` row (two guard-caught authoring slips, the bookkeeping-authoring-slip WATCH continues; a process note that a pending-decisions entry can go stale when its fix ships without rotating the entry out); Version 1.0.664 to 1.0.665.
- [`.working/pending-decisions.md`](../pending-decisions.md): marked the "LIVE fabricated-AICM-code defect" entry RESOLVED. The defect was already fixed in **PR #939** ("AICM matrix-fit: remap 7 fabricated codes to real AICM v1.1.0 codes"), which performed exactly the `/matrix-fit` remap the entry called for; the entry was never rotated out. The maintainer chose `/matrix-fit` for this at the Sweep 107 resume, unaware it was fixed; the orchestrator re-verified all seven current codes against the held CSA AICM v1.1.0 catalogue titles (GRC-09 Acceptable Use of the AI Service, DSP-07 Data Protection by Design and Default, AIS-10 Output Validation, AIS-15 Prompt Differentiation, AIS-11 Agents Security Boundaries, TVM-13 Guardrails, SEF-08 Security Breach Notification), all fit; gate 48 passes. A fresh full `/matrix-fit` skill run was skipped under the maintainer's credit-conservation directive. TODO §3.43 (gate-48 Check-6, the `AI-`-prefix lookbehind blindness) is now unblocked (the corpus is clean).
- [`.working/next-prs.txt`](../next-prs.txt): advanced to the post-task-1 queue.
- Library CalVer `2026.07.452` to `2026.07.453`; [`README.md`](../../README.md) README Version `1.9.813` to `1.9.814`.

### Verification
- `tools/run_all_audits.sh` 69/69 at the pre-push guard; `/validate-pr` #964 returned SHIP / 0 findings.
- The seven AICM codes were re-verified by reading the held [`grc_library_ref`](../../../grc_library_ref) CSA AICM v1.1.0 catalogue CSV titles against each control-area row; the fit is sound and matches PR #939's remap.
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration.

## 2026-07-15, Library Version 2026.07.452, PR #964

Resume of a fresh attended-autonomous session from session-closing handoff PR #963, on the VM (gh-CLI, no GitHub MCP). This is the `/resume` first PR: the mandatory loop-break Sweep 107 corpus-wide `/validate` close-out over the #955..#963 delta window, plus the lease acquire and cursor advance. One low-severity in-window finding, fixed here.

### Fixed
- **The §2.4 closed-section prose-orphan (Sweep 107 finding B-1, in-window, contradicts an asserted-clean claim).** PR #960 closed TODO §2.4 (the grclibrary.ai public site) and rotated it to [`.working/DONE.md`](../DONE.md), but its residual grep searched only the `§2.4` glyph form inside [`TODO.md`](../../TODO.md). Three live carriers of the differently-keyed prose form `(TODO section 2.4)` survived, in file types the glyph-scoped grep never reached:
  - [`.web/build.py`](../../.web/build.py) line 2 (module docstring),
  - [`.github/workflows/web-generator-health.yml`](../../.github/workflows/web-generator-health.yml) line 4 (comment),
  - [`.working/cloudflare-pages-setup.md`](../cloudflare-pages-setup.md) line 1 (runbook title).
  The stale `(TODO section 2.4)` pointer is dropped from all three (the surrounding prose already fully describes each file, and the durable provenance lives in the DONE ledger and this mirror). The two frozen historical carriers further down in this file (the PR4 navigation-sidebar follow-up and the feature-card-links follow-up narrative, both describing work that was tracked under §2.4 at the time) are correctly LEFT as as-of-write-time narrative per the frozen-`.working`-record convention. This is the reference-key-width + file-type-width axes of the CLAUDE.md §N-orphan cross-FILE cleanup guard; §2.6 residual is genuinely 0.

### Changed
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): prepended the Sweep 107 iter-1 row; Version 2.0.105 to 2.0.106.
- [`.working/session-handoff.md`](../session-handoff.md): advanced the Resume-cursor `Last validation sweep` line to Sweep 107 (demoting the prior chain to `Prior:`). The per-session blocks were already at the keep-current-plus-one-prior retention (the #955-#962 and #943-#953 blocks; no older per-session blocks remained to prune).
- [`.working/session-state.md`](../session-state.md): ACQUIRED the concurrency lease (`Active-session: claude/resume-sweep107-validate`, `Status: active`, fresh heartbeat) and recorded the maintainer-set running order for this session.
- [`.working/next-prs.txt`](../next-prs.txt): cycled to this session's queue.
- Library CalVer `2026.07.451` to `2026.07.452`; [`README.md`](../../README.md) README Version `1.9.812` to `1.9.813`.

### Added
- [`.working/validate-sweeps/2026-07-15-sweep107-iter1.md`](../validate-sweeps/2026-07-15-sweep107-iter1.md): the Sweep 107 iter-1 detail file (trigger, the three A/B/C subagent returns verbatim, orchestrator synthesis, resulting PR).

### Verification
- Sweep 107 baseline: `tools/run_all_audits.sh` = 69/69 OK at `23087a3`/#963 (a descendant of the closing session's asserted green-at `674914b`/#962; no close-vs-start drift), clone non-shallow.
- Three read-only A/B/C subagents dispatched: **A** 0 findings (all four asserted-clean claims confirmed), **B** 1 note (the B-1 §2.4 orphan, fixed here) with all other corpus-wide classes refuted clean, **C** 0 findings (four-surface parity 69, counts 69/13/23/14/18 live-vs-prose consistent, [`tools/build-taxonomy.py`](../../tools/build-taxonomy.py) / [`tools/build-portal.py`](../../tools/build-portal.py) `--check` EXIT=0, regression 383 OK, #963 handoff exemption marker correct).
- Asserted-expectations cross-check: B-1 contradicts the closing session's "§2.4/§2.6 residual 0 across the whole repo" claim (a genuine low-severity miss, escalated and fixed); all other asserted-clean surfaces corroborated, 0 contradicted. Loop-break control for #963 PASSES.
- No corpus document body changed, so no per-document Version/Date bump and no generated-artefact regeneration were required (the three edited files are internal tooling / working-state, not versioned corpus documents).

## 2026-07-15, Library Version 2026.07.451, PR #963

Session-closing handoff for the 2026-07-15 resumed session (`/resume` from #954; merged #955-#962). Working-state only; no corpus or website content changed.

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): added this session's Next-actions (CLOSING + NEXT-SESSION-overnight), State-snapshot, and Asserted-expectations blocks; pruned the per-session stacks to keep current + #954 (dropped the #942 and #917 blocks), per the keep-current-plus-one-prior discipline.
- [`.working/session-metrics.md`](../session-metrics.md): added this session's row (measured subagent-token FLOOR ~1.92M across 10 re-retrievable post-compaction dispatches; orchestrator tokens `not instrumented`; pre-compaction dispatches excluded rather than fabricated).
- [`.working/session-state.md`](../session-state.md): RELEASED the concurrency lease (`Active-session: none`, `Status: released`).
- [`.working/next-prs.txt`](../next-prs.txt): cycled to the overnight session's queue.

### Added (batched PR #962 QA)
- [`.working/validate-pr/history.md`](../validate-pr/history.md): the #962 `/validate-pr` row (SHIP, 0 findings), plus this handoff PR's own `SKIPPED (handoff-PR exception)` row (the loop-break marker gate 50 reads).
- [`.working/improvement-log.md`](../improvement-log.md): the #962 `/retro` row.

### Verification / loop-break
- Per the session-closing handoff loop-break, this PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 107) over #955..#963, cross-checked against the #963 Asserted-expectations block.
- Pre-push guard green (69/69 + PR-time checks D1-D7); green-at `674914b`/#962 = 69/69; library CalVer 2026.07.451, README 1.9.812.

## 2026-07-15, Library Version 2026.07.450, PR #962

Public-site For-AI citation clarity + two maintainer-flagged P3 backlog items. Website template and backlog only; no corpus content changed. Also batches PR #961's post-merge QA.

### Changed
- [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html): the two AI-documentation-practice entries dropped their opaque academic author-citations for plain-language source references. "Model Cards (Mitchell et al., 2019), the origin of the model-card practice" becomes "Model Cards, from the 2019 research paper that introduced the practice"; "Datasheets for Datasets (Gebru et al., 2018), the origin of the dataset-datasheet practice" becomes "Datasheets for Datasets, from the 2018 research paper that introduced it" (the maintainer's "name the source plainly" option). `.web/build.py --check` EXIT=0; the old author-et-al forms have 0 residual in the rendered site.

### Added
- [`TODO.md`](../../TODO.md) §3.78 (website: link each skill to its SKILL.md file, not the bare skill directory) and §3.79 (give corpus coverage to the For-AI "named, not yet covered" instruments, then sync the page; corpus-first, tied to the §2.17-2.21 jurisdiction annexes). Both tagged as the maintainer's prioritized P3 items (2026-07-15); the P3 `Next item number` counter advanced to 3.80.

### Verification
- PR #961 `/validate-pr` (Subagent A, refute-briefed, read-only-git on `5a48c7a`): SHIP, 0 findings; history row added to [`validate-pr/history.md`](../validate-pr/history.md). PR #961 `/retro`: row added to [`improvement-log.md`](../improvement-log.md).
- Pre-push guard green; library CalVer 2026.07.450, README 1.9.811.

## 2026-07-15, Library Version 2026.07.449, PR #961

Two small public-site copy and style tweaks (maintainer-directed 2026-07-15). Website templates only; no corpus content changed. Also batches PR #960's post-merge QA.

### Changed
- [`.web/templates/about.html`](../../.web/templates/about.html): the `.m-name` span "Jeff Posluns, CGEIT, CISSP" now wraps ", CGEIT, CISSP" in a nested `<span class="m-certs">`, so the name and the certifications can carry different sizes.
- [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html): added `.m-name .m-certs { font-size: 0.5em; font-weight: 600; }` after the `.m-name` rule. At `0.5em` the certifications render at half the name's font size, so their uppercase cap-height is about half the visual height of "Jeff Posluns" (cap-height scales linearly with font-size), matching the maintainer's "about half the visual size" direction; the weight is eased from the name's 700 to 600 so the small caps read as a deliberate suffix.
- [`.web/templates/landing.html`](../../.web/templates/landing.html): the §01 lede reworded from "It is not advice or a product; it is a public corpus, released under CC BY-SA 4.0, that [audiences] can adopt from directly and tailor to their own context." to the positive form "It is a public corpus of openly-licensed reference documentation, released under CC BY-SA 4.0, that [audiences] can freely read, cite, adopt, and tailor to their own context." (maintainer's Option B). Removes the "not X; it is Y" contrast framing the house style avoids; the same information (public corpus, openly licensed, freely usable by the listed audiences) is carried positively.

### Verification
- The web generator [`.web/build.py`](../../.web/build.py) `--check` returned EXIT=0; the rendered `dist/about/index.html` carries `Jeff Posluns<span class="m-certs">, CGEIT, CISSP</span>` (name full-size, certs half-size).
- Pre-push guard green; library CalVer 2026.07.449, README 1.9.810.

## 2026-07-15, Library Version 2026.07.448, PR #960

Maintainer-flagged TODO stale-item cleanup (notably the public-site items) plus the PR #959 QA close-out. No corpus content changed.

### Changed
- [`TODO.md`](../../TODO.md) + [`.working/DONE.md`](../DONE.md): closed §2.4 (public presence at grclibrary.ai) and §2.6 (Cloudflare build-watch-paths) to the DONE ledger. §2.4 is built and live and the maintainer confirmed it done 2026-07-15 (remaining: the maintainer-owned publish go-decision, and the separately-tracked §2.15 standards-linking; the About credential-strip styling is actioned in #961). §2.6's build-watch-paths were applied in the maintainer console 2026-07-15 (recorded closed at the #954 handoff but never rotated). Reworded the six now-dangling `§2.4` references (the intra-doc-ref gate would otherwise flag them once the heading is gone): §1.12 (its "after the website work" deferral lifted, now ready), §2.15, §3.74, §3.75, and §4.9 (heading + body).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the Sweep 106 row's leading tally "0 error / 1 warning / 0 note" corrected to "1 note" (its own body cell, the detail file, the commit message, and CHANGELOG-detailed all already said one note, from Subagent C's routed handoff-snapshot-lag note; the #959 `/validate-pr` finding). Version 2.0.104 -> 2.0.105.

### Added
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #959 `/validate-pr` row (Subagent A, 1 Low `.working/` finding = the tally above, fixed here; all corpus surfaces clean). Version 1.2.725 -> 1.2.726.
- [`.working/improvement-log.md`](../improvement-log.md): #959 `/retro` row (the bookkeeping-authoring-slip class; both this session's slips caught in-window). Version 1.0.660 -> 1.0.661.

### Verification
- Bookkeeping-tier PR (no corpus content). `§2.4`/`§2.6` residual grep across TODO: 0. The assembled TODO/DONE rows were re-read for boundary integrity before commit (the #959 `/retro` lesson). Pre-push guard green (the intra-doc-ref gate, gate 45 TODO-staleness, and gate 50 bookkeeping-parity all pass); library CalVer 2026.07.448, README 1.9.809.

## 2026-07-15, Library Version 2026.07.447, PR #959

The Sweep 106 loop-break corpus-wide `/validate` close-out (the compensating control for session-closing handoff PR #954): corrects one in-window finding and batches PR #958's post-merge QA. Sweep record: [`2026-07-15-sweep106-iter1.md`](../validate-sweeps/2026-07-15-sweep106-iter1.md).

### Fixed
- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) line 148 (the canonical citations register): the Treasury Board Directive on Automated Decision-Making row labelled the 24 June 2025 -> 24 June 2026 compliance transition as "**third-review** amendments announced 8 October 2024"; corrected to "**fourth-review**". This is the same ordinal error PR #955 fixed in the Canada AI annex and PR #956 in the AI-and-privacy procedure; it survived here on a third carrier because it used the hyphenated `third-review`, which the earlier space-form "third review" grep did not match (a separator-tolerance gap). The 24 June 2025 transition is the fourth review, double-confirmed via PR #955's maintainer-verified conclusion and an upstream check this turn; the 8 October 2024 announcement date is retained as the fourth-review announcement (consistent with the maintainer-verified evidence that the third review's amendments were effective 25 April 2023, so cannot also have been announced October 2024). The row is re-stamped `verified 2026-07-15`. Version 1.5.36 -> 1.5.37, Date 2026-07-15; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (version-only, stays Baseline).

### Verification
- Sweep 106 (`/validate`), three subagents (A recent-PR deep review, B corpus-wide stale-reference, C audit-programme integrity): 0 error / 1 warning (A-1, fixed here) / 1 note (C, the `.working/` handoff snapshot lag, routed to the session-closing handoff refresh). All 11 pre-flight candidates confirmed legitimate prose. Counts 13 rules / 23 skills / 69 gates verified; both generators `--check` EXIT 0. Loop-break control for #954 PASSES.
- PR #958 `/validate-pr` (Subagent A, refute-briefed, read-only-git on `b1828c6`): PASS, 0 findings; history row added. PR #958 `/retro`: row added to [`improvement-log.md`](../improvement-log.md).
- Pre-push guard (full 69-gate audit suite + PR-time checks) green; library CalVer 2026.07.447, README 1.9.808.

## 2026-07-15, Library Version 2026.07.446, PR #958

Date-anchored the AIA question counts in the Canada AI regulatory annex so they age visibly rather than silently. Maintainer-directed (the annex faces a Canada AI Alliance expert review). Also batches PR #957's post-merge QA per recursion-avoidance.

### Changed
- [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md) line 39: the AIA parenthetical "(the counts as of the current release; the government revises the question set over time)" changed to "(as of the 2026-05-28 version of the tool; TBS revises the question set over time)". The 65 risk / 41 mitigation counts are unchanged and correct; the held `grc_library_ref` AIA overview page (`Date modified: 2026-05-28`) states verbatim "It is composed of 65 risk questions and 41 mitigation questions". The edit replaces the undated "current release" with the source's version date so a reader can see when the counts were current, and so a future revision to the question set makes the annex visibly (not silently) stale. Version 1.0.1 -> 1.0.2, Date 2026-07-15; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (version-only, no maturity-status transition; the annex stays Baseline).

### Verification
- The AIA counts and date were verified against the held Treasury Board AIA overview page in the `grc_library_ref` reference base (the Canada-TBS frameworks bucket, `Date modified: 2026-05-28`; body "It is composed of 65 risk questions and 41 mitigation questions"). The source was already held in the reference base (catalogued 2026-07-10); it is not new to this PR.
- PR #957 `/validate-pr` (Subagent A, refute-briefed, read-only-git on squash `a3f93b1`): PASS, 0 findings; history row added to [`validate-pr/history.md`](../validate-pr/history.md). PR #957 `/retro`: row added to [`improvement-log.md`](../improvement-log.md).
- Pre-push guard (full audit suite + PR-time checks) green; library CalVer 2026.07.446, README 1.9.807.

## 2026-07-15, Library Version 2026.07.445, PR #957

Four public-site text/typography fixes (website templates only; no corpus content changed). Also batches PR #956's post-merge QA per recursion-avoidance.

### Changed
- [`.web/templates/landing.html`](../../.web/templates/landing.html): the hero `<h1>` "Governance documentation, engineered like software." now breaks only after "documentation," (each phrase held on one line via `&nbsp;` plus an explicit `<br>`), removing the mid-phrase wraps after "Governance" and "engineered".
- [`.web/templates/landing.html`](../../.web/templates/landing.html) and [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html): the §01 heading "A reference library you can cite, not just read." now fills the line greedily (a `nobalance` class opting that one heading out of `text-wrap: balance`) instead of splitting after "you".
- [`.web/templates/about.html`](../../.web/templates/about.html): "with over thirty years of leadership" changed to "with thirty years of leadership".
- [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html): the hero `<h1>` keeps each colour on one line ("Learning governance and security" in white via `&nbsp;`, "from this corpus." in orange), removing the mid-phrase wraps after "learning" and "governance".

### Verification
- The web generator [`.web/build.py`](../../.web/build.py) `--check` returned EXIT=0; all four edits were confirmed in the rendered `dist/` (landing hero two-line, §01 one-line, about "thirty years", for-ai colour-per-line).
- PR #956 `/validate-pr` (Subagent A, read-only-git on `a761c05`): PASS, 0 findings; history row added. PR #956 `/retro`: row added to [`improvement-log.md`](../improvement-log.md).
- Pre-push guard green (full audit + PR-time checks); library CalVer 2026.07.445, README 1.9.806.

## 2026-07-15, Library Version 2026.07.444, PR #956

Fixes the same "third review" factual error that PR #955 corrected in the Canada AI annex, now in [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../../ai/procedure-integrated-ai-and-privacy-assessment.md), surfaced by PR #955's post-merge `/validate-pr` cross-reference check (maintainer chose fix-now). Also batches PR #955's post-merge QA records per recursion-avoidance.

### Changed
- [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../../ai/procedure-integrated-ai-and-privacy-assessment.md) line 76: "current version dated 24 June 2025, following the directive's **third review**" corrected to "**fourth review**". The 24 June 2025 version of the TBS Directive on Automated Decision-Making is the fourth review (canada.ca "Progress on AI in government"); the third review took effect 25 April 2023. Version 0.1.0 -> 0.1.1, Date 2026-07-15; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated.

### Verification (PR #955 QA batched here per recursion-avoidance)
- PR #955 `/validate-pr` (Subagent A, read-only-git on squash `1c4ec69`): PASS, 0 error / 0 warning / 1 low cosmetic note; its cross-reference check surfaced this procedure-doc error (out-of-window). Record: [`2026-07-15-PR-955.md`](../validate-pr/2026-07-15-PR-955.md); history row added.
- PR #955 `/retro`: row added to [`improvement-log.md`](../improvement-log.md) (the fact-correction-scope observation; the first-ever verifier override, a false-positive "trusted" refuted against the canada.ca Overview page and maintainer-confirmed "responsible", logged in [`verifier-overrides.md`](../verifier-overrides.md)).
- `tools/run_all_audits.sh` + `tools/run-pr-time-checks.sh` green (see the PR's checks); library CalVer 2026.07.444, README 1.9.805.

## 2026-07-15, Library Version 2026.07.443, PR #955

Corrected and expanded [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md) ahead of a review by Canada AI Alliance readers. The annex's pre-existing instruments were fact-checked against the full-text primary sources held in the `grc_library_ref` reference base (the TBS Directive on Automated Decision-Making, the AIA questionnaire and tool page, the Scope Guide, the Generative-AI Guide, the ISED Voluntary Code, the AI for All strategy, Ontario Bill 194 / EDSTA, OSFI Guideline E-23, and CAN/DGSI 101:2025), by three independent adversarial fact-checkers, plus an upstream canada.ca confirmation of the two date/ordinal items. The newly-added AI Strategy for the Federal Public Service 2025-2027 and Government of Canada AI Register are NOT held in the reference base; their facts (publication dates, the four principles, the register) were verified against the canada.ca source pages provided for this change. The document was in good shape: the AIA 65-risk / 41-mitigation question counts, the human-final-decision-at-Levels-III-and-IV point, the TBS in-force dates, the FASTER principles, the Voluntary Code's six outcomes, the six AI for All pillars (launched 4 June 2026, confirmed against the Prime Minister's release), the Ontario citation and not-in-force status, the OSFI E-23 dates (published 11 September 2025, effective 1 May 2027), and CAN/DGSI 101:2025 all verified correct. One real error and two imprecisions were corrected, and one coverage gap was filled.

### Changed
- **Treasury Board Directive review ordinal (accuracy fix, the one error an expert reader would catch).** The annex attributed the 24 June 2025 to 24 June 2026 compliance transition to the Directive's "third review". Per the canada.ca "Progress on AI in government" page, the third review's amendments took effect 25 April 2023 (with October 2023 / April 2024 transitions), and the current directive text (documentID 32592, versionID 4) carrying the 24 June 2025/2026 transition is the **fourth review**. Changed "third review" to "fourth review".
- **"Scaled to an impact level" over-generalization.** The requirements sentence presented the whole list as scaled by impact level; the Directive's Appendix C scales only some requirements (notice, explanation, peer review, GBA Plus, training, human involvement, approval), while others (the AIA itself, testing and monitoring, recourse, legal review, reporting) are baseline. Reworded to "some obligations scaled to the impact level and others applied as a baseline".
- **Limitations, impact-level scaling.** A limitation bullet listed "the impact-level requirement scaling" among detail "not fixed in the primary text"; the scaling is in fact set in the Directive's Appendix C. Removed it from that list and added a clause noting where it is fixed.

### Added
- **AI Strategy for the Federal Public Service 2025-2027 section.** Added a section on the TBS AI Strategy for the Federal Public Service 2025-2027 (published 4 March 2025; four principles: human-centred, collaborative, ready, responsible; a strategy and policy direction for federal institutions' own AI adoption, not an obligation on external adopters), noting its Government of Canada AI Register transparency deliverable (published as an MVP on 28 November 2025). Added a corresponding adopter-role bullet and a framework-alignment table row (NIST AI RMF Govern; ISO/IEC 42001 Clause 5).

### Verification
- Three adversarial fact-check subagents verified their assigned clusters against the held primary sources (quoting the source for each verdict); the orchestrator re-read every finding at apply time and confirmed the two date/ordinal items upstream on canada.ca (the "third review" = April 2023 announcement and the "Progress on AI in government" page naming the fourth review).
- Per-document `Version` bumped 0.0.2 -> 1.0.1 (maintainer-directed promotion) and `Date` set to 2026-07-15; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first).
- A pre-push skeptical verifier reviewed the diff; [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) and [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh) green (see the PR's checks). The verifier raised one HIGH finding (that the FPS fourth principle should read "trusted", not "responsible"); it was refuted against the canada.ca Overview page's Principles section and maintainer-confirmed as "responsible", and logged as the first reviewed entry in [`verifier-overrides.md`](../verifier-overrides.md).

## 2026-07-15, Library Version 2026.07.442, PR #954

`.working/` session-closing handoff for the 2026-07-15 long resumed website session (#943-#953). Batches PR #953's `/validate-pr` (history row + record file [`2026-07-15-PR-953.md`](../validate-pr/2026-07-15-PR-953.md)) and its `/retro` row; fixes the #953 `/validate-pr` warning W-1 (the [`session-state.md`](../session-state.md) Current-task / Worker-dispatches prose was a PR stale after the heartbeat re-stamp); refreshes [`session-handoff.md`](../session-handoff.md) with new Next-actions, State-snapshot, and Asserted-expectations blocks for this session (green-at `b82475b`/#953 = 69/69) and adds the [`session-metrics.md`](../session-metrics.md) row; and RELEASES the concurrency lease ([`session-state.md`](../session-state.md), Status released, Active-session none). Per the loop-break, this session-closing handoff PR takes no trailing `/validate-pr` + `/retro` (compensating control = the next `/resume`'s corpus-wide `/validate`, Sweep 106, over #943..#954). Working-state + version + CHANGELOG only; no corpus document or website content changed.

## 2026-07-15, Library Version 2026.07.441, PR #953

Website batch item 4 (Option A): a per-type listing page for each of the 17 document types, with the landing page's "By document type" chips now linking to them. Also batches #952's QA.

### Added
- One listing page per document type at `types/<slug>/index.html` (17 pages: standard, procedure, annex, register, template, framework, policy, guideline, plan, matrix, specification, charter, guide, sop, checklist, principle, roadmap), generated from the live taxonomy by a new [`.web/templates/type.html`](../../.web/templates/type.html) template plus a `type_pages` computation and a per-type render loop in [`.web/build.py`](../../.web/build.py). Each page carries a one-line description of the type (a new `TYPE_SCOPE` map, with the Procedure/SOP, Plan/Roadmap, Guideline/Guide, and Template descriptions following the "Type selection guidance" in [`specification-ingestion.md`](../../specification-ingestion.md)) and lists every document of that type across all domains, each row tagged with its domain and linking to its GitHub source, sorted by domain then title. A build-time check fails if a taxonomy type has no `TYPE_SCOPE` entry, and an assertion guards each per-type count against the taxonomy. The new pages are automatically included in `sitemap.xml`.

### Changed
- The landing page's "By document type" chips are now links to the corresponding per-type page (`<a class="type-chip" href="/types/<slug>/">`), previously inert `<span>` elements (`render_type_chips` in [`.web/build.py`](../../.web/build.py); hover and link styling added in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html)).
- Moved the shared document-list CSS (`.doc-index` / `.doc-row` / `.doc-type` / `.doc-title`) into [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) so the per-domain and per-type pages draw from one definition, and removed the now-duplicated block from [`.web/templates/domain.html`](../../.web/templates/domain.html) (a DRY move, no visible domain-page change).
- On a type page, a root-level document (the two library-wide specification docs) shows a "library" domain tag rather than the internal "root".

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 69/69; [`.web/build.py`](../../.web/build.py) `--check` EXIT=0 (now 35 pages, up from 18).
- Rendered the site to a scratch dir and confirmed: 17 type pages generated; all 17 landing chips link to a real per-type page (slug matches path, including `SOP` -> `sop`); per-type `<li>` row counts match the taxonomy (Standard 62; SOP 2; Checklist, Principle, Roadmap 1 each; Specification 5 including the 2 root specs shown as "library"); the domain pages still render their list styled after the CSS move; each type page has a unique title, description, and canonical URL.
- Refute-briefed skeptical pre-push verifier on the feature diff.

### Discipline observation
- Batches #952's `/validate-pr` (0 findings, 2 non-defect notes) and `/retro`. Per the #952 retro's process note, this PR's title omits the trailing `(#N)` (the `gh` squash-append adds the PR number, so a title carrying it produced the doubled `(#N) (#N)` merge subjects seen earlier this session).

## 2026-07-15, Library Version 2026.07.440, PR #952

Website batch item 3 (landing content polish): an orange eyebrow tagline above every landing section, and the out-of-place green check-marked "machine-auditable" closing line converted to a boxed call-to-action. Also fixes the #951 `/validate-pr` warning (the Priority-3 `Next item number` counter) and batches #951's QA.

### Changed
- Added a brass (orange) eyebrow tagline above each landing section that lacked one, matching the existing "For AI-assisted teams" eyebrow on the governance-pack section, in [`.web/templates/landing.html`](../../.web/templates/landing.html): §01 "Reference-grade", §02 "Your entry points", §03 "Governed like code", §05 "The full corpus", §06 "Grounded in the standards", §07 "Open for reuse". The §04 governance-pack section already carried one. Taglines are count-free (no hard-coded figures) to avoid drift.
- Converted the lone green check-marked closing line of the "machine-auditable by construction" section (the `verified-note` span) into a boxed call-to-action styled like that page's "See the full pack" CTA (`pack-cta`), reading "See the audit programme: every gate, every PR" and linking to the [audit-programme specification](../../governance/specification-audit-programme.md), so it matches the surrounding standard-text style instead of standing out as a green line ([`.web/templates/landing.html`](../../.web/templates/landing.html)).

### Removed
- The now-unused `.verified-note` and `.verified-note .tick` CSS rules from [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) (their only consumer was the converted line). The `--verified` colour token is retained as a theme-palette entry across the light/dark variants.

### Fixed
- Advanced the Priority-3 `**Next item number:**` counter in [`TODO.md`](../../TODO.md) from 3.77 to 3.78, closing the #951 `/validate-pr` warning W-1 (the counter was not advanced in the same edit that added §3.77).

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 69/69 (via [`tools/tail-safe.sh`](../../tools/tail-safe.sh)); [`.web/build.py`](../../.web/build.py) `--check` EXIT=0 (18 pages).
- Rendered the site to a scratch dir and confirmed the six new eyebrows render, the boxed CTA replaces the green line (0 `verified-note` residual anywhere), and the CTA target resolves.
- Refute-briefed skeptical pre-push verifier on the diff (substantive multi-section template change).

### Discipline observation
- The #951 warning W-1 (counter not advanced when §3.77 was added) is the first occurrence of a new paired-surface shape introduced by the 2026-07-15 permanent-numbering counter convention: adding a numbered item is now a two-surface edit (the item + the section's `Next item number`). Recorded in the #951 retro for pattern-watch; a mechanical backstop is proposed there if it recurs.

## 2026-07-15, Library Version 2026.07.439, PR #951

Added per-page contents sidebars to the For-AI, per-domain, and Contributors pages of the public site, refined the sidebar scrollspy so grid-row-peer nav items highlight together, and DRY'd the shared sidebar CSS into the common head stylesheet. This is item 2 of the maintainer's website-adjustment batch (the requested sidebars, items 3 and 4). It also folds in the #950 `/validate-pr` fix and batches #950's post-merge QA rows.

### Added
- Contents sidebars (a `<nav class="sidenav">` plus the `.shell` grid wrapper) on [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html) (How an AI can learn / Obligations documented / Resource index / License and reuse), [`.web/templates/about.html`](../../.web/templates/about.html) (The maintainer / Contributors), and [`.web/templates/domain.html`](../../.web/templates/domain.html), the shared template behind all 11 per-domain pages (About this domain / Documents), each matching the existing landing and pack sidebars, with a back-to-library cross-link.

### Changed
- Moved the sidebar CSS (`.shell`, `.sidenav`, `.sidenav-inner`, `.sidenav-h`, the sub-link and active-state rules, the anchor `scroll-margin-top`, and the wide-screen sticky-grid media query) into one shared block in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html); removed the now-duplicated inline `<style>` block from [`.web/templates/landing.html`](../../.web/templates/landing.html); and reduced [`.web/templates/pack.html`](../../.web/templates/pack.html)'s inline block to only its deliberate non-sticky override (the pack page's long 13-rule + 23-skill index must scroll with the page, not clip to an internal scroll box). One definition now drives all five sidebar-bearing pages.
- Refined the scrollspy in [`.web/templates/partials/script.html`](../../.web/templates/partials/script.html): it now reads live element positions and highlights every nav target within 4px of the winning (lowest-in-view) position, so grid-row peers highlight together. On a wide layout the six Standards sub-groups lay out three-per-row, so "Information security / AI governance / NIST cybersecurity" light as a group and likewise "Data-protection law / EU regulation / Security frameworks" (the maintainer's request); on a narrow layout the grid collapses to one column, the tops diverge, and it degrades to a single active link. Also reworded a stale `(TODO 2.16)` comment.

### Fixed
- Wrapped three bare `.web/templates/*` code-spans in the PR #950 detailed-changelog entry ([`.web/templates/landing.html`](../../.web/templates/landing.html), [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html), [`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html)) in markdown links, closing the single low finding from #950's `/validate-pr`.

### Verification
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 69/69 (run via [`tools/tail-safe.sh`](../../tools/tail-safe.sh), exit preserved); [`.web/build.py`](../../.web/build.py) `--check` EXIT=0 (18 pages render); [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) and `python3 -m unittest tests.test_linters` ([`tests/test_linters.py`](../../tests/test_linters.py)) both rc=0.
- Rendered the site to a scratch dir and confirmed each of the five sidebar pages carries exactly one `.shell`/`.sidenav`, the shared CSS block appears once per page (from head-style), the landing inline duplicate is gone, and the pack non-sticky override is present.
- Skeptical pre-push verifier (refute-briefed, independent subagent): no defect across CSS cascade / pack-clipping non-regression (the pack override wins by source order at equal specificity, so the long index does not clip), structural `<div>` balance on all pages, landing de-dup completeness, scrollspy correctness (keep-prior-on-empty, the 4px band excludes a tall parent section, the sub-link parent map is correct, no ReferenceError, degrades to single-highlight), anchor resolution, and generator health. Caveat: this is a static/cascade analysis; the live-browser visual (sticky behaviour, the 4px peer grouping) is verified by cascade reasoning, not runtime observation.

### Discipline observation
- The #950 `/validate-pr` finding (three bare `.web/templates/*.html` paths) traced to a mechanical gap: the CHANGELOG link gate [`tools/lint-changelog-link-coverage.py`](../../tools/lint-changelog-link-coverage.py) and its pre-commit aid [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) share a `FILE_EXTENSIONS` tuple that lacks `.html`/`.css`/`.js`, so web-template path references escape the linking gate. Routed to TODO §3.77 (add the extensions in both files, kept in sync, with a fixture); this entry links every `.html` path by hand in the meantime.
- The "About credential-strip" sub-item once planned for this batch had no maintainer instruction behind it in the session record; the maintainer's bio credentials (CGEIT, CISSP) are accurate and conventionally presented, so they are left unchanged, an authorial call for the maintainer to make explicitly if desired.

## 2026-07-15, Library Version 2026.07.438, PR #950

Website "License" spelling fix (maintainer-directed site adjustment 1 of a batch), a folded-in generator-docstring reword, and the batched post-merge QA for PR #949. Website template + working-state only; no corpus document body changed.

### Changed

- **"License" (s) throughout the visible site text**, replacing the mixed "Licence" (c). The maintainer flagged the "Licence" spelling; confirmed it is the outlier, not a convention: the corpus uses "License" (s) ~183 times (the per-document `**License:**` metadata field, the [`LICENSE`](../../LICENSE) file, Creative Commons' own name) vs "Licence" (c) ~19, and [`tools/lint-language.py`](../../tools/lint-language.py) enforces neither. Edited the user-visible text only, across [`.web/templates/landing.html`](../../.web/templates/landing.html) (the §07 "License & reuse" heading, the sidebar and stat and body prose, the CC-license link text), [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html) (the §04 "License and reuse" heading + body), and [`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html) ("License & attribution" + the License link, which propagates to every page). Left internal, non-visible identifiers unchanged (the `#licence` anchor ids, the `.licence-note`/`.licence-fine` CSS classes, the `creativecommons.org/licenses/` URLs, the `rel="license"` and JSON-LD `"license"` which already use s): renaming them is churn with no user-facing benefit and the maintainer's concern was the visible word. Verified by render: user-visible "Licence"/"licence" (c) = 0 on the landing, For-AI, and about pages; only "License"/"license" (s) remains visible.
- Updated a generator-docstring provenance pointer in [`.web/build.py`](../../.web/build.py) from an old backlog-section id to the shipping PR #941 (the #949 `/validate-pr` out-of-window note-1). No backlog change in this PR; the referenced item was already handled in #949.

### QA (batched per recursion-avoidance)

- PR #949 `/validate-pr`: 0 in-window findings (2 low out-of-window/non-actionable notes; note-1, the generator-docstring provenance ref, is reworded here). Zero-finding history row + [`improvement-log.md`](../improvement-log.md) retro row batched into this PR.

### Verification

- `.web/build.py --check` EXIT=0; render confirms visible "License" (s) only. No corpus document body changed. Library CalVer `2026.07.437` -> `2026.07.438`, README Version `1.9.798` -> `1.9.799`. Pre-push guard green. First of a maintainer-directed website-adjustment batch (this = item 1; items 2-8 follow as their own PRs, §2.4 publish last).

## 2026-07-15, Library Version 2026.07.437, PR #949

TYPE_ORDER drift guard between the two document-ordering generators (TODO §3.76), the TODO->DONE rotation of §3.76 and §2.16, and the batched post-merge QA for PR #948. Test + working-state only; no corpus document body changed.

### Added

- **`GeneratorSortKeyParityTests`** in [`tests/test_linters.py`](../../tests/test_linters.py) (the regression suite run by the linter-regression runner and gate 36). It asserts, by text extract with no import coupling, that [`tools/build-taxonomy.py`](../../tools/build-taxonomy.py) (which orders [`taxonomy.yml`](../../taxonomy.yml)) and [`.web/build.py`](../../.web/build.py) (which orders the website domain pages) carry (a) an identical `TYPE_ORDER` rank tuple and (b) a matching secondary per-domain sort key: case-insensitive title (`.lower()`) plus a repo-relative-path tiebreaker. Scope widened from a rank-only guard by Sweep 105 finding A-1 (identical `TYPE_ORDER` but a divergent case-sensitive vs case-insensitive secondary key that made the on-site order diverge from the canonical taxonomy). Added `import re`. Guard-validity checked: the test passes on the current aligned generators and fails on a simulated TYPE_ORDER swap or a case-sensitive-key regression. An interim regex bug in the test itself (a non-greedy match truncated the sort-key tuple at the inner paren) was caught by running the test and fixed (capture-to-end-of-line).

### Changed

- **TODO->DONE rotation** ([`TODO.md`](../../TODO.md) + [`DONE.md`](../DONE.md)): §3.76 rotated (closed here); **§2.16 rotated (its residual shipped in PR #948 but the rotation was missed there; corrected here)**, and the stale TODO "adoption follow-up §2.16" forward-reference reworded (§2.16 complete: nesting #941, residual #948).

### QA (batched per recursion-avoidance)

- PR #948 `/validate-pr`: 0 findings attributable to #948 (the gate-36 regression FAIL the subagent observed was the orchestrator's in-flight §3.76 test edit on this branch, a read-only-git shared-tree concurrency artefact, out-of-window). Zero-finding history row + [`improvement-log.md`](../improvement-log.md) retro row batched here; the retro logged the §2.16 rotation-miss (a residual-completion rotation slip, corrected in this PR).

### Verification

- `python3 -m unittest tests.test_linters.GeneratorSortKeyParityTests` passes (2 tests); the full linter-regression runner exits 0 with the new test integrated; the audit suite is 69/69 (gate 36 exercises the suite). No corpus document body changed. Library CalVer `2026.07.436` -> `2026.07.437`, README Version `1.9.797` -> `1.9.798`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.436, PR #948

Landing-page left-nav enhancement, the TODO §2.16 residual (Get-started nesting + scrollspy), plus the batched post-merge QA for PR #947. Website template + generator only; no corpus document body changed.

### Added

- **Get-started nesting.** Added `id="gs-*"` jump-target ids to the six "Get started" `.feat` cards in [`.web/templates/landing.html`](../../.web/templates/landing.html) `<section id="start">`, and nested six indented `<a class="sub" href="#gs-*">` links under "Get started" in the landing sidebar (matching the existing domains-under-"By domain" and Standards sub-link nesting).
- **Scrollspy** in the shared [`.web/templates/partials/script.html`](../../.web/templates/partials/script.html): an IntersectionObserver highlights the sidebar link whose section or sub-item is currently in view (top-band rootMargin), selecting the lowest in-view target so a nested sub-item wins over its tall parent section, and also lighting the parent section link when a sub-item is active. The parent-of-a-sub-link mapping is derived from the sidebar DOM order (sub-links follow their parent), so it stays correct if the sidebar changes. Guarded (`navLinks.length && "IntersectionObserver" in window`), so it no-ops on pages without a `.sidenav-inner` of on-page anchors and degrades gracefully to plain static anchor links; it is appended inside the existing theme-toggle IIFE (the page already ran that script), and the live site's CSP is report-only with inline script permitted, so the earlier CSP concern is cleared.
- Active-state CSS (`.sidenav-inner a.active`, `.sub.active`) and `scroll-margin-top` for anchor targets in `landing.html`.

### QA (batched per recursion-avoidance)

- PR #947 `/validate-pr`: 0 findings. Zero-finding history row + [`.working/improvement-log.md`](../improvement-log.md) retro row batched into this PR.

### Verification

- A refute-briefed skeptical verifier returned **SHIP-WITH-NOTES** (2 non-blocking notes): the script comment overstated the landing-only scope (the pack sidebar also runs the harmless observer, no active-state CSS there), and the original `min-top` selection let the parent section shadow nested sub-items. **Both were fixed in-window before push**: the comment was corrected, and the selection was changed to pick the lowest in-view target plus light the parent (so sub-items highlight as intended). `node --check` on the rewritten script body: OK (valid ES5, theme toggle unaffected). `.web/build.py --check` EXIT=0; render confirms 6/6 gs ids + 6 sub-links, all 19 landing `#`-anchors resolve, and the shared script no-ops on the about/for-ai/domain pages. `tools/run_all_audits.sh` 69/69. Library CalVer `2026.07.435` -> `2026.07.436`, README Version `1.9.796` -> `1.9.797`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.435, PR #947

Attribution/citation link on the landing page (a maintainer-directed website request, maintainer-chosen approach) plus the batched post-merge QA for PR #946. Website template + working-state only; no corpus document body changed.

### Changed

- **"GRC Library" in the landing §07 "Licence & reuse" section now links to [`AUTHORS.md`](../../AUTHORS.md)** on GitHub. The maintainer wanted the attribution text ("you attribute the GRC Library as the source") to point at a nicely-formatted, human-readable attribution file (the machine-readable [`CITATION.cff`](../../CITATION.cff) is not that). Advised and maintainer-confirmed (Option A): reuse the existing AUTHORS.md, which already carries the attribution posture, a "How to cite" section with ready APA and BibTeX citations, the AI-assistance disclosure, and the contributors list, rather than create a new dedicated citation file that would duplicate that content.
- Harmonized the landing "For AI" sidebar link from `/for-ai` to `/for-ai/` (a trailing-slash consistency fix, the #946 `/validate-pr` cosmetic non-finding), matching the sitemap and canonical URLs.

### QA (batched per recursion-avoidance)

- PR #946 `/validate-pr`: 0 findings (the AI-friendliness feature was also skeptical-verified SHIP pre-merge). Zero-finding history row + [`.working/improvement-log.md`](../improvement-log.md) retro row batched into this PR. The retro logged a 1st-occurrence behavioural note: a `.web/` generator change that emits a new external URL/namespace (here the sitemap `www.sitemaps.org` namespace) should add the domain to the external-link allow-list in the same PR.

### Verification

- `.web/build.py --check` EXIT=0; temp render confirms the §07 "GRC Library" link resolves to AUTHORS.md and the "For AI" sidebar link now carries the trailing slash. AUTHORS.md confirmed present at the repository root. No corpus document body changed. Library CalVer `2026.07.434` -> `2026.07.435`, README Version `1.9.795` -> `1.9.796`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.434, PR #946

AI-training-friendliness feature for the public site (a maintainer-directed and maintainer-plan-approved website addition), plus the batched post-merge QA for PR #945. Website generator + templates only; no corpus document body changed.

### Added

- **New "For AI" page** [`.web/templates/for-ai.html`](../../.web/templates/for-ai.html) (rendered to `/for-ai/`), linked from the landing-page sidebar. Its hero first paragraph addresses human readers (what the page is, why it exists, how it aims to help AI systems be better-governed), then four sections: §01 how an AI can best learn from the corpus (repo, [`taxonomy.yml`](../../taxonomy.yml), portal, matrices, the AI domain, the rule-pack, each linked to GitHub); §02 a descriptive-fact framing of the obligations the corpus documents; §03 a wide resource index in five groups (AI governance/risk frameworks, AI security, AI legislation by jurisdiction, AI data quality/documentation/transparency, foundational security/privacy/risk standards), each linked entry pointing to the corpus's own coverage and each named-only instrument clearly flagged as not-yet-documented-here; §04 licence and reuse (CC BY-SA 4.0, attribution). **Framing discipline:** the whole page is descriptive/documentary, never imperative toward the reading AI, so it cannot read as prompt injection (the maintainer's explicit concern); a skeptical verifier confirmed every sentence passes the true/false register test.
- **robots.txt** (generated by `render_robots_txt()` in [`.web/build.py`](../../.web/build.py)): welcomes AI and search crawlers, naming 23 known AI/training crawlers with `Allow: /` then an allow-all wildcard group, and advertises the sitemap. Deliberately permissive, replacing the restrictive platform-managed default (maintainer decision: explicit named list + wildcard).
- **sitemap.xml** (`render_sitemap()`): lists every rendered HTML page (built from the page set, so a new page is listed automatically).
- **llms.txt** (`render_llms_txt()`, the llmstxt.org convention): a curated Markdown map of the site and corpus for language models (Core / AI governance / Optional sections), descriptive register.
- **schema.org `Dataset` JSON-LD + `rel="license"`** in the landing-page head, marking the corpus as an openly-licensed (CC BY-SA 4.0), freely-reusable dataset (name, url, sameAs the repo, licence, isAccessibleForFree, version from CalVer, creator, keywords).

### Changed

- [`.web/build.py`](../../.web/build.py): added `for-ai.html` to `PAGES`; added the `AI_CRAWLER_USER_AGENTS` constant and the three emitter functions; `render_site` appends robots.txt / sitemap.xml / llms.txt after the dead-value check; docstring updated to record the new page and the three generated outputs and to reaffirm the content-boundary allow-list.
- [`.web/templates/landing.html`](../../.web/templates/landing.html): added the `/for-ai/` sidebar link and the JSON-LD + licence-link head metadata.
- [`tools/lint-external-link-domains.py`](../../tools/lint-external-link-domains.py): added `sitemaps.org` / `www.sitemaps.org` to the allow-list (the XML namespace URI required in the generated sitemap.xml). A protocol namespace, not a citation publisher, so the citation-verification spec §7 is not updated, following the existing grclibrary.ai precedent in the same list.

### Verification

- Skeptical verifier verdict **SHIP**, 0 error / 0 warning / 2 cosmetic notes: (1) an llms.txt For-AI link lacked a trailing slash vs the sitemap (harmonized to `/for-ai/` in this PR); (2) two legacy crawler tokens in the allow-list (kept; harmless, they exclude no one under the wildcard). Confirmed clean: documentary/non-imperative framing (the maintainer's key concern), all 34 corpus links + 10 llms.txt links resolve to real paths, legal-status claims accurate against the linked annexes, no private `grc_library_ref` exposure, `render_sitemap` built from the HTML pages only, JSON-LD parses and its fields are accurate, and no leftover placeholders in any rendered file.
- Apply-time corrections to the research input: the AI-doc count (~45) was dropped in favour of a qualitative description (taxonomy shows 47, and a hard count would go stale); the AICM version string was omitted (named the instrument only); a bad research path (the AI-security-tooling-landscape register mis-homed under ai/) was corrected to its real location under governance/; external instrument URLs were NOT shipped (named by canonical identifier instead) to avoid any unverified link.
- `.web/build.py --check` EXIT=0 (15 HTML pages + robots.txt + sitemap.xml + llms.txt); temp render confirms all outputs. `.web/` is not wired into the corpus audit gates, so no gate is affected. Library CalVer `2026.07.433` -> `2026.07.434`, README Version `1.9.794` -> `1.9.795`. Pre-push guard green.

### QA (batched per recursion-avoidance)

- PR #945 `/validate-pr`: 0 findings (clean; the #944 next-prs note confirmed fixed). Zero-finding history row + [`.working/improvement-log.md`](../improvement-log.md) retro row batched into this PR.

## 2026-07-15, Library Version 2026.07.433, PR #945

Landing "By domain" (§05 register) section text clarity (a maintainer-directed website request) plus the batched post-merge QA for PR #944.

### Changed

- **Doc-count text moved out of the table as a section-intro paragraph.** In [`.web/templates/landing.html`](../../.web/templates/landing.html) the §05 "The corpus, by domain" section previously carried its document count only as a `<table>` `<caption>` ("{{DOC_TOTAL}} documents across {{DOMAIN_COUNT}} governance domains, counts from the generated taxonomy"). Per the maintainer, that text now renders as a `<p class="lede">` section-intro paragraph ABOVE the table, matching every other section's intro-paragraph style, and the table caption is removed. New intro: "The corpus spans {{DOC_TOTAL}} documents across {{DOMAIN_COUNT}} governance domains. Every count here is recomputed from the generated taxonomy on each change, so the numbers stay current."
- **Below-table note reworded for clarity and up-sized to the section-paragraph style.** The note previously read "Domain counts total {{DOMAIN_DOC_TOTAL}}; a further {{ROOT_COUNT}} programme-level specification documents sit at the corpus root, for {{DOC_TOTAL}} in all." (class `register-note`, 0.86rem, faint), which read oddly because the headline says {{DOC_TOTAL}} (312) while the note led with {{DOMAIN_DOC_TOTAL}} (310). Reworded to explain the gap plainly and set to `class="lede"` (1.15rem, matching the intro paragraph, per the maintainer's "match the text size of the paragraph before the table"): "The per-domain counts in the table sum to {{DOMAIN_DOC_TOTAL}}; the remaining {{ROOT_COUNT}} of the {{DOC_TOTAL}} total documents are programme-level specifications that sit at the corpus root rather than inside any one domain." The `.register-note` CSS is retained (still used on the pack page); the now-orphaned `table.register caption` CSS is left in place (harmless scoped selector, in the shared partial).
- Trimmed [`.working/next-prs.txt`](../next-prs.txt) line 1 back under the ~120-char console-statusline budget (the #944 `/validate-pr` note N-1; it had grown to 150 chars).

### QA (batched per recursion-avoidance)

- PR #944 `/validate-pr`: 0 error / 0 warning / 1 note (the next-prs.txt overlength above, fixed here); pack-card links, targets, version bumps, CHANGELOG parity, and batched #943 QA all verified clean. Record: [`.working/validate-pr/2026-07-15-PR-944.md`](../validate-pr/2026-07-15-PR-944.md); history row + [`.working/improvement-log.md`](../improvement-log.md) retro row batched into this PR.

### Verification

- `.web/build.py --check` EXIT=0; a temp render confirms the §05 section now shows the intro lede above the table (no caption), the reworded note below (rendered numbers 312 / 11 / 310 / 2), both at lede size. No corpus document body changed (website template + working-state only). Library CalVer `2026.07.432` -> `2026.07.433`, README Version `1.9.793` -> `1.9.794`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.432, PR #944

Pack-page card links (a maintainer-directed website request) plus the batched post-merge QA for PR #943.

### Changed

- **Pack-page "Three ways to use it" cards now link (website consistency).** The three `.mode` cards in the §02 section of [`.web/templates/pack.html`](../../.web/templates/pack.html) had a plain-text kicker (`.m-k`: "As shipped" / "With overlays" / "Standalone") and no link, unlike every card on the landing page (whose `.feat` kicker `.k > a` links to the most-relevant document). Wrapped each pack-card kicker in a link, matching the landing pattern exactly (the landing "How it's built" kickers "Structured" / "Cross-linked" / "Practical" are the same shape, abstract labels linking to relevant docs): **As shipped** -> the repository (to fork), `https://github.com/jposluns/grc_library`; **With overlays** -> the adopter guide, [`docs/adopter-guide.md`](../../docs/adopter-guide.md); **Standalone** -> the pack directory, [`dev-security/claude-rules`](../../dev-security/claude-rules) (the one directory to drop into any project). No CSS change was needed: the global anchor style is brass with hover-underline and `.mode .m-k` is already brass, so the kicker link renders consistently with the landing kicker links. Verified by a temp render (all 3 links present and correct) and `.web/build.py --check` (EXIT=0). Card 2's target (adopter guide vs pack README) was the one judgment call, resolved to the adopter guide as the canonical "adopt in a fork" resource.

### Fixed

- Corrected a meta-prose count conflation in the PR #943 Sweep 105 detail file (the #943 `/validate-pr` Subagent A note N-1): "All 6 pre-flight FP candidates" -> "All 11 pre-flight candidates (across 6 files)", reconciling with the file's own "11 candidates" and the history row. Gate-exempt `.working/` frozen record; no adopter or correctness impact.

### QA (batched per recursion-avoidance)

- PR #943 `/validate-pr`: 0 error / 0 warning / 1 note (the N-1 count conflation above, fixed here); the A-1 sort-key fix independently re-verified correct (0/12 domains diverging post-fix). Record: [`.working/validate-pr/2026-07-15-PR-943.md`](../validate-pr/2026-07-15-PR-943.md); history row + [`.working/improvement-log.md`](../improvement-log.md) retro row batched into this PR.

### Verification

- `.web/build.py --check` EXIT=0 (312 documents, 14 pages, library 2026.07.432); temp render confirms the 3 pack-card kicker links. No corpus document body changed (website template + working-state only). Library CalVer `2026.07.431` -> `2026.07.432`, README Version `1.9.792` -> `1.9.793`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.431, PR #943

The `/resume` loop-break **Sweep 105** corpus-wide `/validate` close-out for the just-closed 2026-07-15 long resumed session (the compensating control for session-closing handoff PR #942, which skipped its trailing `/validate-pr` + `/retro`), covering the **#918..#942** delta window. Full three-subagent A/B/C dispatch, all read-only-git on the shared tree.

### Fixed

- **A-1 (website domain-page ordering; the sweep's one finding).** [`.web/build.py`](../../.web/build.py) sorted each domain's documents within a type by a case-SENSITIVE title key (`d["title"]`), while [`tools/build-taxonomy.py`](../../tools/build-taxonomy.py) sorts case-INSENSITIVELY with a repo-path tiebreaker (`title.lower(), rel`). With `TYPE_ORDER` byte-identical between the two generators, the *secondary* key still diverged, so the on-site domain pages presented a different within-type reading order than the canonical taxonomy and portal ordering (e.g. the compliance page listed "eIDAS Sector Requirements Annex" last, after all uppercase-initial titles, instead of among the E-annexes). Aligned the generator's sort key to `(TYPE_RANK..., d["title"].lower(), d["path"])`, matching the taxonomy generator. Verified: `.web/build.py --check` EXIT=0; a temp render now orders "eIDAS ... Annex" among the E-annexes (DORA -> eIDAS -> Energy). Cosmetic (ordering only; no data loss, no wrong document, no broken link) but user-visible on the live site. This finding CONTRADICTED the #942 handoff's asserted-clean "#940 ... consistent" claim (the "TYPE_ORDER IDENTICAL" sub-claim held; the "consistent" header was the miss), so it is a genuine miss of the closing session's self-assessment, escalated and fixed in-window.

### Changed

- Widened TODO §3.76 (the TYPE_ORDER DRY guard) so its scope is the WHOLE per-domain sort key (primary rank plus the secondary tiebreaker), not only the `TYPE_ORDER` tuple, per the A-1 lesson.
- Advanced the resume cursor and added the Sweep 105 row + detail file ([`.working/validate-sweeps/2026-07-15-sweep105-iter1.md`](../validate-sweeps/2026-07-15-sweep105-iter1.md)); bumped [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) to 2.0.103.
- Pruned [`.working/session-handoff.md`](../session-handoff.md) per the keep-current-plus-one-prior discipline (kept the #942 and #917 session blocks; dropped the #901-#913 sweep102 blocks) and neutralized the resulting dangling "#914" pointer.
- Acquired the concurrency lease ([`.working/session-state.md`](../session-state.md): Status active, Active-session `claude/resume-sweep105-validate`, fresh heartbeat).

### Verification

- Mechanical baseline **69/69** at #942 (`7651a1b`), a descendant of the asserted green-at `3fc2a0c`/#941; no close-vs-start drift; clone non-shallow.
- Sweep result: **0 error / 1 warning / 0 note** (A: 1 warning [A-1, fixed]; B: 0; C: 0). Pre-flight 421 files, 11 candidates all the collection-count-word false-positive class, dismissed by all three subagents. Asserted-expectations cross-check: A-1 contradicts the "#940 consistent" claim (escalated + fixed); all other asserted-clean surfaces corroborated, 0 further contradictions. **Loop-break control for #942 PASSES.**
- Subagent B confirmed corpus-wide: fabricated-AICM residue 0, no closed-section orphans in gate-exempt carriers, counts 69/13/23/14/18, no website content-boundary leak. Subagent C confirmed four-surface parity at gate 69, the #933 gate-69 widening reflected in all free-prose surfaces, regression suite 381 EXIT=0, both generators `--check` EXIT=0.
- No corpus document body changed (the A-1 fix is to the `.web/` generator, not a versioned corpus document; `.web/dist/` is git-ignored and rebuilt on deploy; the taxonomy source already sorted correctly). Library CalVer `2026.07.430` -> `2026.07.431`, README Version `1.9.791` -> `1.9.792`. Pre-push guard green.

## 2026-07-15, Library Version 2026.07.430, PR #942

Session-closing handoff (terse; working-state only, no corpus content changed). The 2026-07-15 long resumed session (overnight #929-#936 + attended wind-down #937-#941, merged through #941) lands its working state on `main` as a green merge so the next session resumes from the branch. This PR: refreshes [`.working/session-handoff.md`](../session-handoff.md) (a new State snapshot + Asserted-expectations + Next-actions block, leading with the maintainer's directive to review the deployed grclibrary.ai site first; green-at `3fc2a0c`/#941 = 69/69); adds the [`.working/session-metrics.md`](../session-metrics.md) row (measured post-compaction subagent floor ~1.98M across ~11 dispatches; pre-compaction dispatches excluded, not fabricated; orchestrator not instrumented); batches PR #941's `/validate-pr` (SHIP 0/0/0) + `/retro`; and RELEASES the concurrency lease ([`.working/session-state.md`](../session-state.md): Status released, Active-session none). Per the closing-handoff loop-break (PR-workflow step 5a exception) it takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` over the #918..#942 deltas, cross-checked against this handoff's Asserted-expectations. Pre-push guard (`tools/run_all_audits.sh` 69/69 + PR-time checks) green.

## 2026-07-15, Library Version 2026.07.429, PR #941

Landing-page left-nav two-level nesting (TODO §2.16, maintainer-directed this session). Website template + generator only; no corpus document content changed.

### Changed

- [`.web/templates/landing.html`](../../.web/templates/landing.html): the left contents nav was a flat "Contents" group (7 section links) followed by a separate flat "Domains" group, so the nav ENDED with the 11 domains and the Standards / Licence links sat above them (the maintainer read this as "ends with domains, no Standards/Licence"). Rebuilt into a two-level quick-nav: the 11 domains now render as indented sub-links directly under the "By domain" link (the separate "Domains" group is gone), the six Standards sub-groups render as short indented sub-links under "Standards" (anchored to new `std-*` ids added to the six sub-group headings), Licence is kept, and a new **Contributors** link (to `/about`, the about/contributors page) is added at the end. The nav now flows What it is, Get started, How it's built, Governance pack, By domain (+ 11 domains), Standards (+ 6 sub-groups), Licence, Contributors.
- [`.web/build.py`](../../.web/build.py) `render_sidenav_domains`: the domain links now carry `class="sub"` (indented sub-links nested under "By domain") instead of a flat group.
- Added a `.sidenav-inner a.sub` CSS rule (indent + lighter weight) for the nested sub-links.
- **Scrollspy active-highlighting and Get-started-step nesting are deferred** as the §2.16 residual (scrollspy is a new inline-JS addition on an otherwise script-free page and wants a Content-Security-Policy check first; Get-started nesting needs ids on the six step cards). §2.16 stays open for those; the shipped structural nesting is recorded in [`.working/DONE.md`](../DONE.md).

### Fixed

- **Concurrency-lease append-not-reconcile (the #940 `/validate-pr` warning, third occurrence this session).** #940 updated the lease tail / Active-session / heartbeat but left the Current-task LEAD carrying a #939-era snapshot (wrong branch, stale merged-through and green-at). The whole Current-task field in [`.working/session-state.md`](../session-state.md) was REWRITTEN wholesale (the adopted durable control: rewrite the entire field on each update, never patch individual sentences), so no carried sentence can go stale. Logged as a `[3rd-occurrence]` graduated control in the #940 `/retro`.

### Verification

- `.web/build.py --check` OK (generator-health, all 14 pages render); a temp build confirms the rendered nav order (By domain, then the 11 domains as `class="sub"`, then Standards + the 6 `std-*` sub-links, then Licence, then Contributors -> `/about`). Pre-push guard (`tools/run_all_audits.sh` 69/69 + PR-time checks) green; one refute-briefed skeptical verifier on the nav change. The deployed grclibrary.ai domain pages + landing nav update on merge (Cloudflare Pages rebuilds; `.web/dist/` is git-ignored).
- Batched PR #940's post-merge QA: the #940 `/validate-pr` row (SHIP-WITH-NOTES, 1 warning fixed here) in [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.708) and the `/retro` row in [`.working/improvement-log.md`](../improvement-log.md) (1.0.644).

## 2026-07-15, Library Version 2026.07.428, PR #940

Domain-page document ordering: alphabetical -> a logical reading progression, applied in BOTH the taxonomy source generator and the website generator (maintainer-chosen "source + type-priority sort", 2026-07-15). Tooling only; no corpus document content changed.

### Changed

- [`.web/build.py`](../../.web/build.py) (the website generator, the surface the maintainer reviews): its per-domain page list was sorted by `(type-string, title)`, i.e. by type name ALPHABETICALLY, so Annex / Charter / Framework floated to the top, which is the "order doesn't seem right" that was observed. Changed to sort by a `TYPE_RANK` reading-progression rank, so each domain page now reads govern -> define -> do -> reference (Charter/Policy, then Framework/Standard, then Procedure/Guide, then Register/Template/Annex), alphabetical by title within a type. **This website-generator sort is what actually reorders the published pages**: the generator filters the taxonomy to a domain and then re-sorts, so taxonomy row order alone would not have changed the pages (a correction to an earlier assumption that the source order propagates).
- [`tools/build-taxonomy.py`](../../tools/build-taxonomy.py): added the same `TYPE_ORDER`/`TYPE_RANK` rank and an `_order_key(path)` that sorts by (domain, type-rank, title, path); `iter_all_docs()` now returns `sorted(set(files), key=_order_key)` instead of `sorted(set(files))`. This puts the taxonomy source itself into the same logical order, so the source file reads consistently with the pages (the maintainer's "source" choice). An unlisted type sorts last (rank = len). The rank is replicated in the two generators because `.web/` is a standalone stdlib-only tool isolated from `tools/`; the two copies MUST stay in sync, and a consistency guard is queued (TODO §3.76).
- [`docs/portal.md`](../../docs/portal.md) (sorts by audience then type/title) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) (sorts by path) order INDEPENDENTLY of taxonomy row order, so both are UNCHANGED by this PR (git status confirms neither moved); that is correct, they carry their own intentional orders. The order-insensitive lint consumers (version-bump-recency, listing-surface-completeness, gate parity, changelog-link, preflight) use the document set, not its order. Domains keep their alphabetical grouping; the only inter-domain move is the two root `specification-*.md` files sorting among the r-domains in the taxonomy source.

### Verification

- Lossless re-sort of the taxonomy source: the set of `- path:` entries is unchanged (312 before and after; `git diff` shows 181 moved positions, net zero added/removed). `build-taxonomy.py --check` and `build-portal.py --check` clean (drift gates confirm deterministic reproducibility). `.web/build.py --check` OK (generator-health, all 14 pages render), and a temp build confirms each domain page now lists in type-rank order (ai: Charter, Charter, Policy, Framework..., Standard...). Regression suite OK; [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 69/69. One refute-briefed skeptical verifier checked the taxonomy re-sort's losslessness, within-domain type-order correctness across multiple domains, determinism, domain-grouping preservation, and full type coverage (ZERO findings).
- Batched PR #939's post-merge QA: the #939 `/validate-pr` row (SHIP, 0 findings) in [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.707) and the `/retro` row in [`.working/improvement-log.md`](../improvement-log.md) (1.0.643).

## 2026-07-15, Library Version 2026.07.427, PR #939

Resolves three maintainer decisions from the attended wind-down and batches PR #938's QA. The one corpus-content change is the AICM citation fix.

### Fixed

- **Live AICM citation defect (the §3.43 matrix-fit, maintainer-approved).** The `## Framework alignment` table in [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md) cited 7 fabricated codes in its `CSA AICM` column. Each was remapped to the best-fit REAL AICM v1.1.0 control, judged against the held CSA AICM v1.1.0 catalogue titles: AI tool authorization `AI-GOV-01`->`GRC-09` (Acceptable Use of the AI Service); Data handling for AI inputs `AI-DATA-01`->`DSP-07` (Data Protection by Design and Default); Code review of AI output `AI-SEC-02`->`AIS-10` (Output Validation); Prompt injection awareness `AI-SEC-03`->`AIS-15` (Prompt Differentiation); Agentic use controls `AI-GOV-03`->`AIS-11` (Agents Security Boundaries); Deterministic enforcement `AI-SEC-04`->`TVM-13` (Guardrails); Incident reporting `AI-INC-01`->`SEF-08` (Security Breach Notification). gate 48 was blind to the fabricated codes because the leading `AI-` defeated its `CODE_RE` lookbehind (the §3.43 class). The guideline doc Version bumped 1.3.5->1.3.6, Date to 2026-07-15; taxonomy + portal + scorecard regenerated (taxonomy first) to pick up the version.

### Changed

- **TODO §3.47 rescoped (maintainer):** strip only the date / `Surfaced #N` / `Mined (sweep N)` / PR-number / maintainer-directed provenance and KEEP the `(was X.Y)` renumber breadcrumbs, per the #929 convention that existing breadcrumbs stay for resolvability. Still attended-preferred (a large single-file editorial sweep), queued not run.
- **TODO §3.8 closed as won't-do (maintainer):** gates 31 and 40 keep their per-document `--follow` git subprocess rather than batching into one `git log --name-only` pass; correctness/history-fidelity outranks the guard's runtime (AIQT tier). Rotated to [`.working/DONE.md`](../DONE.md); no code change.

### Verification

- [`tools/lint-ccm-aicm-citations.py`](../../tools/lint-ccm-aicm-citations.py) (gate 48) rc=0 (420 files, all CCM/AICM citations valid); each new code confirmed present + in-range in the held AICM v1.1.0 reference; a refute-briefed skeptical verifier checked the 7 remaps (real codes, in-range, semantic fit, no collateral edit). `build-taxonomy.py --check` and `build-portal.py --check` clean after regen. Pre-push guard (`tools/run_all_audits.sh` + PR-time checks) green.
- Batched PR #938's post-merge QA: the #938 `/validate-pr` row (SHIP-WITH-NOTES, 2 cosmetic notes fixed in-batch) in [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.706) and the `/retro` row in [`.working/improvement-log.md`](../improvement-log.md) (1.0.642).

## 2026-07-15, Library Version 2026.07.426, PR #938

Working-state / bookkeeping tier. Batches PR #937's post-merge QA and routes a backlog scope-conflict; no corpus, tooling, gate, or generated-artefact change.

- Batched PR #937's `/validate-pr` (Subagent A, SHIP-WITH-NOTES: one in-window working-state warning) into [`.working/validate-pr/history.md`](../validate-pr/history.md) (1.2.705) and its `/retro` into [`.working/improvement-log.md`](../improvement-log.md) (1.0.641). The warning (`session-state-append-not-reconcile`) was that #937 reconciled the [`.working/session-state.md`](../session-state.md) Current-task LEAD but left the carried TAIL asserting "HOLDING / queue EXHAUSTED" and listing the now-done §3.10 as deferred; fixed in this batch (tail reconciled; HOLDING/EXHAUSTED dropped, §3.10 removed, §3.43 recast as blocked, green-at bumped to `191699c`).
- Routed a backlog scope-conflict in [`TODO.md`](../../TODO.md) §3.47: its plan to strip residual `(was X.Y)` renumber breadcrumbs contradicts the #929 permanent-numbering convention (which states "existing breadcrumbs stay for resolvability"). Annotated §3.47 with the conflict and the need for a maintainer rescope; noted it is also a large attended-preferred editorial sweep (~85 items, weak mechanical verification), not an unattended-overnight item.
- Recorded the overnight hold rationale in the lease and [`.working/next-prs.txt`](../next-prs.txt): after an evidence-based item-by-item reassessment (each blocker verified by reading the item), no cleanly-buildable-unattended HA item remains (§3.43 blocked on the AICM matrix-fit decision, §3.47 scope-conflict, §3.8 maintainer trade-off, §3.60/§3.73 fresh-session dispositions, rest protected/egress/source/maintainer/attended-website). Session holds in overnight mode per the maintainer's "stay in overnight mode until morning".

### Verification

- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean on the added lines; pre-push guard ([`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 69/69 + PR-time checks) green. Bookkeeping tier, so no pre-push HA verifier (the mechanical gates plus the next PR's `/validate-pr` are the QA of record); #938's own `/validate-pr` + `/retro` batch into the next substantive PR.

## 2026-07-15, Library Version 2026.07.425, PR #937

Fence-predicate consolidation (TODO §3.10, closes it): the fenced-code-block skip check is now a single shared `lint_common.is_fence_line()` predicate that recognizes both backtick and tilde fences, closing the GR-4 tilde-blindness class in which six linters ignored `~~~` fences and could stick in code mode to EOF (or scan content they should skip). Latent on the current corpus (zero tilde fences), so no document's audit result changes; the fix is a robustness hardening. Also batches PR #936's post-merge QA and routes a live citation defect surfaced during the §3.43 FP-census. Overnight run, high-assurance tier.

### Changed

- Added a shared fence predicate `is_fence_line(line)` to [`tools/lint_common.py`](../../tools/lint_common.py) (True when the left-stripped line starts with three backticks or three tildes) and refactored the existing `iter_non_code_lines` generator to call it, so there is one source of truth for fence detection.
- Routed eight linters' in-code-block skip loops through the shared predicate, replacing their private inline checks. Six were TILDE-BLIND before this change (a `~~~` fence was not recognized): [`tools/lint-changelog-link-coverage.py`](../../tools/lint-changelog-link-coverage.py), [`tools/lint-directional-dependency.py`](../../tools/lint-directional-dependency.py), [`tools/lint-document-control-codes.py`](../../tools/lint-document-control-codes.py) (gate 54), [`tools/lint-document-iso-annex-a.py`](../../tools/lint-document-iso-annex-a.py) (gate 58), [`tools/lint-links.py`](../../tools/lint-links.py), and [`tools/lint-shall-near-uncertainty.py`](../../tools/lint-shall-near-uncertainty.py). Two were already tilde-aware inline and are converted for consolidation (behaviour-preserving): [`tools/lint-ccm-aicm-citations.py`](../../tools/lint-ccm-aicm-citations.py) and [`tools/lint-cobit-iso31000-citations.py`](../../tools/lint-cobit-iso31000-citations.py). Gate 66's [`tools/lint-unbalanced-fences.py`](../../tools/lint-unbalanced-fences.py) is intentionally left (it is the fence-balance gate with its own width/pairing semantics).
- Rotated TODO §3.10 to [`.working/DONE.md`](../DONE.md) (the P3 counter is unchanged; a closed number retires, it does not renumber).

### Added

- Two regression tests in [`tests/test_linters.py`](../../tests/test_linters.py): `test_is_fence_line_predicate` (both fence characters, info strings, indentation, and negatives including inline code, a two-character run, and an empty line) and the guard-first `test_shall_near_uncertainty_inside_tilde_fence_ignored` (a shall-near-uncertainty phrase inside a `~~~` fence must be skipped; this test fails against the old tilde-blind code and passes now, a non-vacuous proof).

### Notes (finding routed, not fixed here)

- The §3.43 FP-census (run to design the deferred gate-48 Check 6) surfaced a live citation defect: the `## Framework alignment` table in [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md) has a `CSA AICM` column citing seven fabricated codes (`AI-GOV-01`, `AI-DATA-01`, `AI-SEC-02`, `AI-SEC-03`, `AI-GOV-03`, `AI-SEC-04`, `AI-INC-01`), none of which is a valid AICM v1.1.0 code (confirmed against the CSA AICM v1.1.0 catalogue held in `grc_library_ref`). gate 48 is blind to them by construction (the leading `AI-` defeats its `CODE_RE` lookbehind, the exact §3.43 class). The fix is a semantic matrix-fit judgment (which real AICM code per row), so it is routed to [`.working/pending-decisions.md`](../pending-decisions.md) for the maintainer (recommended: run `/matrix-fit` on the table), not guessed unattended. §3.43's guard-first build is blocked on this resolution and annotated accordingly in TODO.

### Verification

- Two independent adversarial HA verifiers (a behaviour-divergence lens and a coverage-completeness lens), read-only-git on the shared tree, each returned ZERO findings: the change is behaviour-preserving on every carrier except the intended latent tilde-awareness, no tilde-blind carrier was missed (full enumeration of every fence literal across the `tools/` linter sources), and the guard-first fixture is non-vacuous.
- Full regression suite 381 tests OK (was 379; plus the two new tests); `tools/run_all_audits.sh` 69/69; corpus behaviour unchanged (zero tilde fences in the corpus, so no document's result moves).
- Batched PR #936 QA: the #936 `/validate-pr` (Subagent A, SHIP 0/0/0) row in [`.working/validate-pr/history.md`](../validate-pr/history.md) and the `/retro` row in [`.working/improvement-log.md`](../improvement-log.md).

## 2026-07-15, Library Version 2026.07.424, PR #936

Overnight resting-point close-out. Working-state and backlog only; no corpus document, template, gate, tool, or generated artefact changed.

### Changed
- **Refreshed [`next-prs.txt`](../next-prs.txt)** to the queue-exhausted / daytime-priority state, fixing the PR #935 `/validate-pr` warning (W1): #935 did not touch the file, so its first line still listed §3.38 and §3.22 as the immediate overnight-safe "next" while #935's own conclusion had deferred both and declared the overnight-safe queue exhausted (the PR-workflow-step-6 "a PR shipped without refreshing next-prs" signal). The refreshed file records the full deferral rationale (protected / attended-for-quality / egress / maintainer-decision / source-gated) and the daytime-return priority.

### Notes
- **Overnight run summary.** This run merged #929 (the TODO permanent-numbering framework: never-recycled numbers + per-section counters), #930-#932 (the massive-item TODO-split wave: split §3.57/§3.62/§3.63/§3.68, §2.4, and §2.5 so completed components moved to the DONE ledger and only remaining parts stayed, §2.5's workstreams re-homed into new §2.17-§2.21), #933 (the gate 69 widening to catch `TODO item N.M`, §3.50), #934 (§3.34 go-forward preflight link-resolution check), #935 (staged the §3.22/§3.12 protected machinery for daytime + the §3.38 assessment), and this #936 close-out. Every substantive PR ran two independent high-assurance verifiers plus a post-merge `/validate-pr`; every finding was caught pre-push or fixed in the batching PR; net zero adopter-facing escapes.
- **Resting point (still in overnight mode).** The cleanly-unblocked overnight-safe queue is exhausted. Every remaining item is deferred for a specific quality or authorization reason (not a depth excuse): protected `.claude/`/pack items (daytime auth, drafted in [`deferred-protected-changes.md`](../deferred-protected-changes.md) items 6/8/9); attended/fresh-context-for-quality items where a hasty change would risk a real defect (per the apex AIQT rule); egress / cross-repo; maintainer-decision; and source-gated content. Per the maintainer's instruction the session stays in overnight mode (no wind-down, no handoff) and resumes building if the maintainer redirects or a further unblocked item surfaces.

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green. Working-state / bookkeeping tier (next-prs refresh + QA rows + version bumps), so no pre-push HA verifier per the tiered standard; the batched PR #935 `/validate-pr` (SHIP-WITH-NOTES, its next-prs warning fixed here) is the QA of record.
- **PR #935 post-merge validation** (Subagent A, read-only-git on `4a6a668`): SHIP-WITH-NOTES, 0 error / 1 warning (the next-prs staleness fixed here) / 0 note; batched here.

## 2026-07-15, Library Version 2026.07.423, PR #935

Overnight preparation PR: staged the remaining protected-surface machinery items for the daytime apply (per the overnight protocol's "draft the content in advance" direction) and recorded an assessment of the one FP-delicate gate item. Working-state and backlog only; no corpus document, template, gate, tool logic, or generated artefact changed.

### Added
- Two prepared items in [`deferred-protected-changes.md`](../deferred-protected-changes.md) for the daytime protected-backlog clearance:
  - **Item 8 (§3.22):** the D7 handoff-snapshot marker fix, fully drafted, the non-protected tool + test halves (redirect `snapshot_line()` to the `Version snapshot` sub-line the #746 restructure moved the tokens onto; update the D7 test fixtures to the two-line shape) plus the protected `.claude/` config's D7-note reword (the reason it defers, and why the whole item applies together to avoid a multi-surface inconsistency).
  - **Item 9 (§3.12):** the See-Also parity gate (new gate 70), design + full surface list (the new linter, the four wiring surfaces, the fixture, and the 69-to-70 gate-count ripple that reaches the protected `.claude/` config).

### Changed
- **§3.22 and §3.12** annotated in [`TODO.md`](../../TODO.md) as overnight-deferred, each pointing at its drafted [`deferred-protected-changes.md`](../deferred-protected-changes.md) item.
- **§3.38** annotated with a 2026-07-15 assessment: gate 39's mechanizable count-idioms are largely already covered, the digit forms by patterns P1-P8 (P8 handles `N automated audits`, with a bare `N audits` deliberately excluded as FP-unsafe) and the word forms by P9-P12; the FP-safe residual is narrow (a digit `N governance rules` sibling of P11) and needs a careful attended per-idiom census, and the un-gateable free-prose half stays dropped per the maintainer's 2026-07-10 disposition. No gate change made (rushing an FP-delicate multi-pattern gate this deep in the session would risk a false-positive; AIQT over Speed).

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; the three TODO annotations and the two staging items are well-formed; the staging surface is under `.working/` (not protected). Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green.
- **Two independent high-assurance verifiers** (correctness + completeness): honoring the maintainer's "high assurance for all" over the default working-state / bookkeeping tier, scoped to the accuracy of the drafted D7-fix + See-Also-gate approaches and the §3.38 assessment (that P8-P12 do cover the claimed idioms).
- **PR #934 post-merge validation** (Subagent A, read-only-git on `99f3a5b`): batched here.

### Notes
- Overnight run. After this PR, the overnight-safe unblocked queue is exhausted: the remaining items are protected (§3.22/§3.12, drafted here for daytime), attended (§3.34 historical-dangler cleanup, §3.73 self-deferring FP-free-detector design), FP-delicate (§3.38 residual), or source/egress-gated. The session stays in overnight mode per the maintainer's instruction, holding at this clean state, and continues if a further unblocked item is identified.

## 2026-07-15, Library Version 2026.07.422, PR #934

Advanced backlog item §3.34 (detailed-mirror markdown-link resolution) by shipping its go-forward half, and folded in the batched PR #933 cosmetic note. Tooling + backlog only; no corpus document, template, or generated artefact changed (no spec change this PR, so no taxonomy regen).

### Changed
- **Go-forward link-resolution check added to [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py)** (advancing §3.34): the aid now flags any newly-added CHANGELOG line (root or detailed mirror) that introduces an in-repo relative markdown-link target which does not resolve to an existing file, resolved relative to the source file's own directory. Excluded (per §3.19 and by construction): cross-repo / out-of-repo targets (a sibling repo such as `grc_library_ref`, an `inbox/` worker-provenance path, or any target resolving outside the repo), external `http(s)` / `mailto:` / anchor targets, and links inside a code span (an illustrative `[text](url)`). This check has NO authoritative gate behind it, the detailed mirror is `.working/`-exempt from the corpus broken-link gate, so it is the sole guard; verified FP-safe by a 10-case behaviour test (resolving in-repo links pass; dangling, cross-repo, external, anchor, and code-span-illustrative correctly classified).

### Fixed
- **PR #933 post-merge note (in-window, cosmetic).** The gate-69 docstring in [`tools/lint-positional-backlog-tokens.py`](../../tools/lint-positional-backlog-tokens.py) had a fourth in-file carrier (the scope-summary line) still naming two qualifier forms after #933 widened the detection to three; brought into parallelism with the lead example, the regex comment, and the §6 narrative.

### Notes
- **§3.34 stays OPEN.** The go-forward half (this check) closes the new-dangling-link gap. A census of the existing mirror found about 23 dangling in-repo links (mostly `.working/` sibling-file references written as a bare filename without the leading `../`, so they resolve inside the changelog-details directory instead of one level up, plus about 2 illustrative link-syntax false-positives to leave code-spanned); that per-link historical cleanup, and then enabling a full-mirror (not only added-lines) scan, remain under §3.34 for an attended / fresh-context session. Recorded there so the finding is tracked, not lost.

### Verification
- The new check's 10-case behaviour test passed (see [`TODO.md`](../../TODO.md) §3.34 for the census result); [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) run over this PR's own added CHANGELOG lines is clean (dogfooded, every link target here resolves). Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green. The aid is not wired into the regression suite (it is git-diff-based, like its existing untested dash / unlinked-ref checks), so the new check is verified by the behaviour test rather than a suite fixture, consistent with the aid's pattern.
- **Two independent high-assurance verifiers** (correctness + completeness, refute-briefed, read-only-git): scoped to the new check's FP-safety (no legitimate link newly flagged), its cross-repo / code-span exclusions, and the §3.34 partial-progress framing.
- **PR #933 post-merge validation** (Subagent A, read-only-git on `09c3102`): SHIP-WITH-NOTES; the one cosmetic docstring-parallelism note fixed here.

## 2026-07-15, Library Version 2026.07.421, PR #933

Widened audit gate 69's detection to catch the `TODO item N.M` phrasing, closing backlog item §3.50. Gate-logic + tooling + backlog; the only corpus change is the gate-69 description in the audit-programme spec (a gate-description update; no corpus requirement or normative content changed).

### Changed
- **Gate 69 detection widened** in [`tools/lint-positional-backlog-tokens.py`](../../tools/lint-positional-backlog-tokens.py): the `POSITIONAL_REF` regex now accepts an optional `item(s)` qualifier between `TODO` and the section token (`TODO(?:\s+[Ii]tems?)?`), so `TODO item 3.4` is flagged as a positional reference (previously only `TODO §N` / `TODO N.M` / `backlog item PN.M` matched). The comment and module docstring were updated to describe the widened form and the FP guard. The §6 gate-69 narrative in [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (Version 1.17.5 to 1.17.6) was updated to list the `TODO item N.M` example; taxonomy/portal/scorecard regenerated from the spec bump.

### Added
- Two regression fixtures in [`tests/test_linters.py`](../../tests/test_linters.py): `test_positional_todo_item_dotted_flagged` (the `TODO item 3.4` detect case) and `test_todo_item_prose_without_token_not_flagged` (the `TODO item covers ...` clean case, the FP guard).

### Removed
- Backlog item §3.50 (rotated to [`DONE.md`](../DONE.md)); its P3 number retires.

### Verification
- **FP analysis (the crux of the widen-vs-document decision):** a corpus census over the gate-scanned set found ZERO live `TODO item <token>` carriers, and confirmed the existing `... TODO item covers ...` prose (register-coverage-gaps) has no section token after `item` so the widening does not newly-flag it. A 9-case behaviour test on the widened regex passed (target forms match, all FP prose forms and the bare-single-digit `TODO item 3` do not), and the gate stays 0 over the corpus.
- Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69 (gate 69 green, gate 36 regression suite green with the 2 new fixtures, gate 39 count-phrasing green); the linter regression suite (`python3 -m unittest tests.test_linters`) = 379 tests OK. Pre-push guard green.
- **Two independent high-assurance verifiers** (correctness + completeness, refute-briefed): scoped to the regex change, the FP-safety, the fixture coverage, and the spec/docstring completeness.
- **PR #932 post-merge validation** (Subagent A, read-only-git on `a62418e`): SHIP, 0 findings; batched here.

### Notes
- Overnight run, high-assurance harness. §3.50's directive allowed either widening (with FP analysis) or documenting the omission as intentional; the FP analysis was clean, so the widening was applied. Next: the remaining self-contained P3 gate/tooling HA candidates (§3.12 See-Also parity gate, §3.34 detailed-mirror link-resolution); §3.73 self-defers to a fresh session per its own build note.

## 2026-07-15, Library Version 2026.07.420, PR #932

Third TODO-split-hygiene PR (permanent-numbering hygiene): split the §2.5 AI-domain-delta umbrella. This is the "split into components" case (as distinct from the §2.4/§3.x trim-in-place): §2.5's remaining distinct workstreams re-home into their own new-numbered items, and the §2.5 umbrella is retired. Working-state and backlog only; no corpus document, template, or generated artefact changed.

### Changed
- **§2.5** (AI-domain post-plan delta) retired as an umbrella. Its landed workstreams (Workstream A EU/CA fold-ins A.1-A.5, #843/#844/#847/#849; Workstream C residuals C.1/#850, C.3/#850, C.4-resolved) rotated to [`DONE.md`](../DONE.md). Its number 2.5 is retired (never reused, per the permanent-numbering rule).

### Added
- Five new P2 items re-homed from §2.5, each drawing the next number from the P2 counter (advanced 2.17 -> 2.22): **§2.17** AI jurisdiction annex California CCPA/ADMT (was Workstream A.6, binding, egress-gated dates), **§2.18** South Korea AI Basic Act annex (was B.1, held primary), **§2.19** Singapore Model AI Governance Framework annex (was B.2, held primary), **§2.20** ref-side `last_checked` sweep for the 6 EU/CA AI sources (was C.2, cross-repo), **§2.21** further AI-jurisdiction annexes deferred pending held sources (was B.3, source-gated, cross-refs §5.9).
- A DONE-ledger entry recording the executed delta and the re-homing map.

### Fixed
- **§N-orphan cleanup (the retire-a-section guard).** Repointed the live cross-file reference in [`.working/high-assurance/register.md`](../high-assurance/register.md) from "TODO §2.5 Workstreams A.6 and B" to "TODO §2.17 / §2.18 / §2.19" (the re-homed item numbers), so the HA register's `pending` AI-annex rows no longer dangle on the retired §2.5. Whole-repo grep confirmed this was the only live dangling reference (the other §2.5 hits are a different document's section, NIST 600-1 §2.5, or frozen historical records).

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; [`tools/lint-cross-file-section-refs.py`](../../tools/lint-cross-file-section-refs.py) (gate 62) rc=0; P2 now carries no §2.5 (0 residual heading), §2.4 -> §2.6 adjacency clean (the anomalous `---` removed), the five new items well-formed with `(severity, effort)` tags, counter at 2.22. Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green.
- **Two independent high-assurance verifiers** (correctness + completeness lenses, refute-briefed, read-only-git): scoped to confirm every landed workstream is genuinely merged, every remaining workstream is re-homed (none dropped), the §2.5 retirement left no dangling reference, and no adjacent item was disturbed.
- **PR #931 post-merge validation** (Subagent A, refute-briefed, read-only-git on `e75f045`): SHIP, 0 findings; batched here.

### Notes
- Overnight run, high-assurance harness on every item. This completes the massive-item split wave (§3.57/§3.62/§3.63/§3.68 in #930, §2.4 in #931, §2.5 here). Next: the self-contained P3 gate/tooling HA candidates (§3.12, §3.34, §3.50, §3.73).

## 2026-07-15, Library Version 2026.07.419, PR #931

Second TODO-split-hygiene PR (permanent-numbering hygiene): split the §2.4 website-umbrella item. Working-state and backlog only; no corpus document, template, or generated artefact changed. §2.4 keeps its permanent number; no new items (counters unchanged).

### Changed
- **§2.4** (public presence at grclibrary.ai) trimmed from the long #919-#928 build-narrative to a lean statement of current state (built and live on Cloudflare Pages) plus only its remaining maintainer-gated items: further live-review fixes, the confirmed follow-ups §2.15 (standards-list source links) and §2.16 (two-level nav), the §2.6 Cloudflare-console watch-paths action, the publication go-decision (branch name, project settings, About credential strip), and the DRY-sidebar-CSS cleanup. Stays ATTENDED-ONLY and OPEN until publish.

### Added
- A DONE-ledger entry ([`DONE.md`](../DONE.md)) recording the completed website build effort (the live-review round #919-#924, the adoption round #925-#926, and the nav-consistency fixes #928), marked as a partial rotation (§2.4 stays open until the maintainer's publish go).

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; §2.4 keeps heading number 2.4 (no renumber); the §2.15/§2.16/§2.6 cross-references resolve; the DONE entry matches the trimmed residual. Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green.
- **Two independent high-assurance verifiers** (correctness + completeness lenses, refute-briefed, read-only-git): scoped to confirm the rotated build rounds are genuinely merged/live, no remaining maintainer-gated item was dropped, and no adjacent item was disturbed.
- **PR #930 post-merge validation** (Subagent A, refute-briefed, read-only-git on `26620e3`): batched here per recursion-avoidance.

### Notes
- Overnight run, high-assurance harness on every item. The companion §2.5 AI-domain-delta split (which re-homes its remaining workstreams into new-numbered items and retires the §2.5 umbrella) is the next PR.

## 2026-07-15, Library Version 2026.07.418, PR #930

First application of the new permanent-numbering hygiene (maintainer-directed 2026-07-15): split four massive partially-done backlog items so their completed components rotate to [`DONE.md`](../DONE.md) and only each item's open residual remains in [`TODO.md`](../../TODO.md). Working-state and backlog only; no corpus document, template, or generated artefact changed. Each item keeps its permanent number (no renumbering); no new items, so the counters are unchanged.

### Changed
- **§3.57** (reference-breadth new-ingest apply) trimmed from the full #866-#883 apply-wave narrative to just its open residual, the deferred matrix TSC-column mapping (a `/matrix-fit` single-file sensitive change). The apply wave (High EDPB-privacy cluster + the version-sensitive rows, each held-source-verified and upstream-currency-confirmed) rotated to DONE.
- **§3.62** (guardrail-review r10 proposals) trimmed to its one open proposal, G1 (the branch-to-main edit-guard hook, a maintainer decision). The resolved proposals (G3 built as gate 50 Check 5 in #913, G5 EXPIRED in #909, the gate-41 docstring symmetry in #909) rotated to DONE.
- **§3.63** (reference-audit FULL findings) trimmed to its one residual, the RB-ETSI-104128 secondary see-also in the AI security-and-risk standard's alignment table. The resolved findings (RB-FFIEC-CAT currency fix #899, the RB-ETSI primary see-also #907) rotated to DONE.
- **§3.68** (vuln-remediation-SLA SoT) trimmed to the four ROUTED divergent-value carriers that need a maintainer judgment call (pentest, supplier-tier, patch-exception-deferral, BASC-KPI); its heading was refocused off the now-rotated conversions. The clear stricter-safe conversions (#912) rotated to DONE.

### Added
- Four DONE-ledger entries in [`DONE.md`](../DONE.md), each marked as a partial rotation (the item stays open for its named residual), keyed to the split items.

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; §3.62's G3/G5/Overlap bullets removed with G1 retained; §3.68 carries a single routed-carriers header; no `### N.M` heading deleted or renumbered (the four items keep their numbers). Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green.
- **Two independent high-assurance verifiers** (correctness + completeness lenses, refute-briefed, read-only-git): scoped to confirm no open residual was dropped, every rotated component is genuinely complete (evidence: the cited merged PRs), each DONE entry is accurate, and no unrelated item was disturbed.
- **PR #929 post-merge validation** (Subagent A, refute-briefed, read-only-git on `f8917b7`): SHIP, 0 findings; batched here per recursion-avoidance.

### Notes
- This is the first split PR; the two P2 umbrellas (§2.4 website, §2.5 AI-domain delta) are the next split (they need more judgment, §2.5's remaining workstreams re-home into their own new-numbered items). Overnight run, high-assurance harness on every item.

## 2026-07-15, Library Version 2026.07.417, PR #929

TODO numbering-convention change, a gate-69 rationale consistency fix in one governance spec (the new never-recycle rule made the old "positions renumber as the backlog is worked" rationale stale), and the batched PR #928 post-merge QA. Touches [`TODO.md`](../../TODO.md), `.working/` records, one governance spec ([`specification-audit-programme.md`](../../governance/specification-audit-programme.md)), the [`tools/lint-positional-backlog-tokens.py`](../../tools/lint-positional-backlog-tokens.py) docstring, and the taxonomy / portal / scorecard regenerated from the spec's version bump.

### Changed
- **TODO item numbers are now permanent and never recycled** (maintainer-directed 2026-07-15). The header numbering convention in [`TODO.md`](../../TODO.md) is rewritten: a number is a permanent id, not a reusable position; each priority section carries a `Next item number:` counter, maintained on every TODO edit; new and split-out items each draw the next number and advance the counter; a closed item's number retires with it; existing items are not renumbered on reorganization (renumbering would break the CHANGELOG / DONE / handoff references pointing at them). The `(was X.Y)` renumber-breadcrumb practice is discontinued (existing breadcrumbs stay for resolvability). A matching bullet was added to the Standing conventions section. Motivation: a number should map to exactly one item across the file's whole history so lookups are unambiguous (the historical grep found numbers recycled well past the visible set, e.g. P2 to 2.14, P4 to 4.28).
- **Per-section counters added** to all seven priority headings, seeded to the true historical max + 1 so no new item reuses a past number: P1 1.14, P2 2.15, P3 3.75, P4 4.29, P5 5.10, P6 6.6, P7 7.6 (each then advanced by the items this PR adds).

### Added
- Four maintainer-confirmed backlog items, each drawing its number from the new counters (which advanced accordingly):
  - **§1.14** (P1) external-source currency detection: a Layer-A egress-free cadence gate (mechanizing SR-1 + §3.9) plus a Layer-B scheduled egress sweep that fetches upstream signals and notifies on change, with auto-update under QA. (Counter advanced to 1.15.)
  - **§2.15** (P2) landing-page standards list: link each item to its authoritative source, freely-available sources to the primary document, licensed / ISO to the official catalogue / abstract page, never bypassing a paywall; URLs sourced from the `grc_library_ref` catalogue and verified upstream. (Counter advanced through 2.16.)
  - **§2.16** (P2) landing-page left nav: a two-level nested quick-nav (nest the 6 Get-started steps + the 11 domains + any Standards sub-groups, with scrollspy highlighting). (Counter advanced to 2.17.)
  - **§3.75** (P3) website-to-corpus link integrity: a generated committed link manifest (the reverse map) + an egress-free resolution gate + resolve-by-stable-doc-id for auto-update on rename. (Counter advanced to 3.76.)

### Fixed
- **PR #928 post-merge review (in-window, internal-only).** The #928 detailed-CHANGELOG entry said "all 18 feature cards consistent" when only 15 of the 18 use the `.k`-link + unlinked-`<h3>` pattern (the 3 pack-teaser cards deliberately carry no `.k` link); corrected here.
- **Pre-push high-assurance verifier findings (all fixed here, before push).** (i) The P1 section intro said "one open item"; it now reads "three open items" (§1.1, §1.12, §1.14, the last added by this PR), the count-next-to-enumeration class both verifiers flagged, and the same class this line set out to fix. (ii) The P6 counter was mis-seeded to 6.7 because a seeding grep false-matched a document-section token "§6.6"; corrected to 6.6 (P6's true historical-max item is 6.5). (iii) Multi-surface convention consistency: the gate-69 rationale in [`specification-audit-programme.md`](../../governance/specification-audit-programme.md) and the [`tools/lint-positional-backlog-tokens.py`](../../tools/lint-positional-backlog-tokens.py) docstring still read "positions renumber as the backlog is worked", which the new never-recycle rule contradicts; both are re-based on number-retirement-on-close plus pre-convention historical renumbering (the gate stays justified, so no gate logic changed). (iv) Added the missing severity token to each of the four new items (the `(id, severity, effort)` convention).

### Verification
- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (gate 45) rc=0; all seven counters present; the numbering-convention sentence, the standing-convention bullet, and the four new items present. One governance spec changed ([`specification-audit-programme.md`](../../governance/specification-audit-programme.md), Version 1.17.4 to 1.17.5, Date 2026-07-15); taxonomy / portal / scorecard regenerated from that bump (gates 33/34 `--check` clean). Full [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) = 69/69; pre-push guard green.
- **Two independent high-assurance verifiers** (correctness lens + completeness lens, refute-briefed, read-only-git): both SHIP-WITH-NOTES. Between them they caught the P1 count (three not two), the P6 counter off-by-one, the two stale gate-69 rationale surfaces, and the missing severity tokens, all fixed above and re-verified. Confirmed clean: the never-recycle invariant holds for all seven sections (no counter is at or below any number ever used), no existing item was renumbered, no content was dropped, and all gates are green.
- **PR #928 post-merge validation** (Subagent A, refute-briefed, read-only-git on `7479db5`): SHIP-WITH-NOTES, 0 error / 0 warning / 1 note (the "all 18" count, fixed here); record at [`2026-07-15-PR-928.md`](../validate-pr/2026-07-15-PR-928.md).

### Notes
- This is the permanent-numbering framework; the companion follow-up (splitting the massive partially-done items, §2.4 / §2.5 / §3.57 / §3.68 / §3.62 / §3.63, so completed components rotate to DONE and only the remaining parts stay, each drawing fresh counter numbers) is the next PR. The four website / tooling items recorded here (§1.14, §2.15, §2.16, §3.75) are the maintainer-confirmed outputs of the live-site-review discussion.

## 2026-07-15, Library Version 2026.07.416, PR #928

Three follow-up fixes to the public grclibrary.ai site from the maintainer's live review, plus the batched PR #927 post-merge QA. Template-scoped ([`.web/templates/landing.html`](../../.web/templates/landing.html) and [`.web/templates/pack.html`](../../.web/templates/pack.html)); the generator was not touched and no corpus document changed.

### Changed
- **Hero CTAs made comprehensive.** The landing hero now carries five buttons covering the page's main sections: "Get started" (`#start`, primary), "How it's built" (`#build`), "The governance pack" (`/pack`, internal), "Browse the domains" (`#register`), and "Standards" (`#standards`). Previously the hero under-represented the page; the maintainer asked for it to be comprehensive and to link the pack page.
- **Get-started cards aligned to the page's card pattern.** The six "Get started" cards now use the same shape as the feature cards in sections 01/03/04: the `.k` keyword is the link (to the corpus document), the `<h3>` is an unlinked statement. They previously used a different colour/style, "Begin 1/2/3" and "Use 1/2/3" placeholder titles, and an inconsistent link structure; the maintainer flagged the inconsistency.

### Fixed
- **Pack-page sidebar now lists all 23 skills.** The wide-screen `.sidenav` in [`.web/templates/pack.html`](../../.web/templates/pack.html) had `max-height: calc(100vh - 2.5rem)` + `overflow-y: auto` + `position: sticky`, which hid roughly 21 of the 23 skills behind an internal scroll region. Those three properties are removed from the `@media (min-width:1080px)` block so all 13 rules and 23 skills render inline in the contents sidebar; the `.shell` grid and the rest of the layout are unchanged.
- **PR #927 post-merge review.** Zero findings (SHIP, 0/0/0); the row is recorded and batched here.

### Verification
- The generator's `--check` is rc=0 (14 pages, no leftover placeholders). On the landing page the Get-started section has six `.k` links and zero linked `<h3>` (matching sections 01/03/04; 15 of the 18 feature cards use this `.k`-link + unlinked-`<h3>` pattern, the 3 pack-teaser cards deliberately carry no `.k` link), the hero has exactly five CTAs whose four `#` anchor ids each exist once and whose `/pack` target renders, and zero off-site-vs-internal `target=_blank` contradictions. On the pack page all 13 rule + 23 skill links resolve to files on disk, and `max-height`/`overflow-y`/`position: sticky` have zero residual in the page CSS. Full `tools/run_all_audits.sh` = 69/69.
- **PR #928 skeptical verifier** (refute-briefed, read-only-git): **SHIP, 0 blocking / 0 material findings, 1 informational note** (the landing page keeps its on-page `id="pack"` teaser section while the hero CTA routes to the standalone `/pack` page, intentional per the change description). Visual/responsive appearance (CTA wrap at five buttons, sidebar inline flow) is not browser-verifiable on the build host; the maintainer reviews the live preview.
- **PR #927 post-merge validation** (Subagent A, refute-briefed, read-only-git on `2d164c6`): SHIP, 0 error / 0 warning / 0 note; batched here per recursion-avoidance.

### Notes
- These are §2.4 website follow-ups from the live-review loop; §2.4 stays open until the publish go. The DRY-the-sidebar-CSS cleanup (landing/pack duplication) remains a tracked follow-up. Per the maintainer's changelog-length feedback, the root entry for this PR is deliberately terse; the deferred remediation of the over-long recent root entries (#921 onward) and the length-guard strengthening are tracked as TODO §1.12, to run after the website work.

## 2026-07-15, Library Version 2026.07.415, PR #927

Working-state close-out: a new backlog item and the batched PR #926 QA; nothing adopter-facing changed.

- Added backlog item §2.6: the maintainer-console Cloudflare build-watch-paths action (include the 11 domain directories), deferred to the next computer session; the last open §2.4 build item before the publish go.
- Corrected the fourth generator help-text page-set carrier (the argparse description) that the #925 docstring sweep missed; a full-file grep confirms all four carriers now include the pack page.
- Batched PR #926's post-merge validation (Subagent A, read-only-git on `76bbbcd`): SHIP-WITH-NOTES, 0 error / 0 warning / 1 note (the argparse carrier, fixed here); record at [`2026-07-15-PR-926.md`](../validate-pr/2026-07-15-PR-926.md). README 2026.07.415 / 1.9.776.

## 2026-07-15, Library Version 2026.07.414, PR #926

The public landing-page restructure (backlog section 2.4, closing the adoption round), plus the batched PR #925 post-merge QA. Landing-page-scoped; no corpus document changed and no generated artefact was touched. This completes the website effort (PR #921 through #926).

### Changed
- **New "Get started" section, placed third** in [`.web/templates/landing.html`](../../.web/templates/landing.html) (right after "What it is"), with six cards linking to material already in the corpus: find your path ([`docs/decision-tree.md`](../../docs/decision-tree.md)), see it done ([`docs/worked-example-adoption.md`](../../docs/worked-example-adoption.md)), start from a template ([`docs/template-quickstart.md`](../../docs/template-quickstart.md)), map your obligations ([`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md)), adopt the whole programme ([`docs/adopter-guide.md`](../../docs/adopter-guide.md)), and assess your maturity ([`docs/template-maturity-self-assessment.md`](../../docs/template-maturity-self-assessment.md)). The hero's primary button is now "Get started". Nothing new was authored; every card links to an existing document.
- **Governance-pack section slimmed to a teaser.** It now shows three highlight rule cards (project-integrity, gate-discipline, evidence-grounded-completion) and a "See the full pack: 13 rules and 23 skills" link to the `/pack` page (internal); the other three rule cards moved to `/pack` in PR #925.
- **Licence split into its own closing section.** The former section 06 "Use it, adapt it, cite it" (which opened with the licence) became section 07 "Licence & reuse" at the very end, carrying the CC BY-SA intro and the ShareAlike explanation only; its three adopt cards folded into "Get started". Sections renumbered 01-07 (what / get-started / how-it's-built / pack / by-domain / standards / licence); the sidebar and the shared footer nav ([`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html)) were updated to match, and no `#adopt` anchor is left dangling.

### Removed
- The now-unused `.adopt-grid` / `.adopt-card` CSS in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) (orphaned when the adopt cards moved into "Get started", which uses the existing `.feat-grid`). No template references them.

### Fixed
- **PR #925 post-merge review (both in-window, internal-only).** The [`.web/build.py`](../../.web/build.py) module docstring's page-set enumeration omitted the pack page in three carriers; the pack page is now listed in all three. And the concurrency-lease `Current-task` in [`.working/session-state.md`](../../.working/session-state.md) was one PR behind; it is refreshed to the current state.

### Verification
- The generator's `--check` is rc=0 (14 pages, no leftover placeholders); the landing page has exactly seven sections numbered 01-07 in order, every sidebar anchor resolves to a section, no `#adopt` remains, all six Get-started links and the three pack-rule links resolve, and the `/pack` teaser is an internal link. Full `tools/run_all_audits.sh` = 69/69.
- **PR A skeptical verifier** (refute-briefed, read-only-git): **SHIP, 0 defects** across seven checks, including content-preservation: the ShareAlike licence block is byte-identical to before, and all three former adopt actions survive as Get-started cards. Visual/responsive appearance was not browser-verified (no browser on the build host); the maintainer reviews the live preview.
- **PR #925 post-merge validation** (Subagent A, refute-briefed, read-only-git on `e50fc22`): SHIP-WITH-NOTES, 0 error / 0 warning / 2 note (the docstring and the lease), both FIXED here; record at [`2026-07-15-PR-925.md`](../validate-pr/2026-07-15-PR-925.md).

### Notes
- This closes the §2.4 website effort. The remaining §2.4 items are maintainer-only (confirm the Cloudflare build-watch-paths include the 11 domain directories, and the publish go-decision); §2.4 stays open until publish. One small cleanup is tracked: DRY the landing/pack contents-sidebar CSS into the shared partial (currently duplicated per-page).

## 2026-07-15, Library Version 2026.07.413, PR #925

A dedicated `/pack` page on the public site for the AI-assistant governance pack (backlog section 2.4, the adoption round), plus the batched PR #924 post-merge QA. No corpus document changed and no generated artefact was touched.

### Added
- **The governance-pack page** at `pack/index.html`, from a new template [`.web/templates/pack.html`](../../.web/templates/pack.html) registered in [`.web/build.py`](../../.web/build.py)'s `PAGES` (14 pages total). It frames the pack as the portable operating-discipline layer distilled from running an AI-managed project, distinct in kind from the GRC corpus, and presents: the three adoption modes taken from the pack README (fork-as-shipped, fork-with-overlays, standalone-baseline); all 13 governance rules, each with a one-line purpose and a link to its file; and all 23 skills grouped by purpose (validation and QA, semantic-fit and reference audits, escalation and high-assurance, rule-companion disciplines), each linked. A contents sidebar lists every rule and every skill as an at-a-glance reference (a visual index of the pack's breadth). The rule/skill inventory is curated static template content, consistent with the landing page's hardcoded standards bibliography; every one of the 38 GitHub link targets was cross-checked to exist on disk.
- The site footer's "Governance pack" link (in [`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html)) now points to `/pack`, so the page is reachable site-wide. The landing §03's repoint to `/pack` and the §03 slim are deferred to the next PR (the landing restructure).

### Verification
- The generator's `--check` is rc=0 (14 pages render, no leftover placeholders); the generator's diff is exactly the one `PAGES` line, no new file read or directory walk (content boundary unchanged). All 13 rule links and 23 skill links resolve to real files/dirs; 13 distinct rule targets, 23 distinct skills (groups 6+4+3+10), no dead links, no omissions. Full `tools/run_all_audits.sh` = 69/69.
- **PR B skeptical verifier** (refute-briefed, read-only-git on the pack page): SHIP-WITH-NOTES, 0 critical / 0 high. One Medium accuracy finding, the `ai-assistant-workflow-disciplines` one-line description had named the fifth discipline wrong (it listed "tiered skeptical verification," which the rule explicitly says is a standard layered on top, not one of the five; the real fifth is productive use of CI-wait windows), FIXED here. One informational note, the landing/pack contents-sidebar CSS is duplicated per-page (flagged in-file; a tracked follow-up to DRY it into the shared partial). The 12 other rule one-liners and the three adoption modes verified faithful to their sources.
- **PR #924 post-merge validation** (Subagent A, refute-briefed, read-only-git on `7be28de`): SHIP, 0 error / 0 warning / 0 note; record at [`2026-07-15-PR-924.md`](../validate-pr/2026-07-15-PR-924.md). The live-tree "14 pages" vs #924's "13 pages" was confirmed a concurrent-run artefact, not a defect.

### Notes
- UTC rolled over to 2026-07-15 during this PR (the maintainer's local clock was still 2026-07-14 evening); per the project's UTC date convention this entry, the bumped Dates, and the QA records use 2026-07-15, while the prior same-session PRs #921-#924 remain 2026-07-14.
- Next in the adoption round: the landing restructure (one 6-card Get-started section placed 3rd, the CC BY-SA licence split into its own closing section, §03 slimmed to a `/pack` teaser, sidebar + footer nav updated).

## 2026-07-14, Library Version 2026.07.412, PR #924

A contents-navigation sidebar on the public landing page (backlog section 2.4, the fourth maintainer-review PR, completing the live-review round), plus the batched PR #923 post-merge QA. No corpus document changed and no generated artefact was touched; the change is landing-page-scoped, so the about and domain pages are untouched.

### Added
- **Landing-page contents navigation.** [`.web/templates/landing.html`](../../.web/templates/landing.html) gains a `<nav class="sidenav">` listing the six on-page section links (What it is, How it's built, Governance pack, By domain, Standards, Adopt), a Domains heading, and the eleven domain-page links (generated by a new `SIDENAV_DOMAINS` value from `render_sidenav_domains` in [`.web/build.py`](../../.web/build.py)). By default (phone / iPad-portrait) it renders as a boxed in-flow Contents panel near the top of the page, so a visitor sees the site's breadth up front; on wide screens (a `min-width: 1080px` CSS-grid shell) the same nav becomes a sticky left sidebar beside the content. The styles live in a landing-page-scoped `<style>` block, so the about and domain pages are unaffected; the masthead and footer stay full-bleed (outside the shell).

### Fixed
- **PR #923 post-merge review, both in-window and internal-only.** The #923 detailed-CHANGELOG entry said "16 target files"; corrected to the 14 distinct target files (15 card links, with STRUCTURED and STYLE both pointing at the master spec). And `render_domain_doc_rows`'s docstring in [`.web/build.py`](../../.web/build.py) still described the old two-element row (title plus a separate GitHub link); it now describes the single title-as-link row.

### Verification
- The generator's `--check` is rc=0 (13 pages render, no leftover placeholders); the landing page has exactly one shell and one sidenav, six section links (each resolving to a real page section) and eleven domain links (each to a real rendered domain page); the about and domain pages carry no shell, sidenav, or `SIDENAV_DOMAINS`. Full `tools/run_all_audits.sh` = 69/69.
- **PR 4 skeptical verifier** (refute-briefed, read-only-git on `93a1453`): **SHIP, 0 defects** across seven adversarial axes (generator intact, other pages unaffected, 11 domain links correct, section anchors resolve, CSS balanced and scoped, content boundary unchanged, link hygiene clean). Visual and responsive appearance was not browser-verified (no browser on the build host); the maintainer reviews it on the live preview.
- **PR #923 post-merge validation** (Subagent A, refute-briefed, read-only-git on `63b8b42`): SHIP-WITH-NOTES, 0 error / 0 warning / 2 note (F1 the "16" count, F2 the docstring), both FIXED here; record at [`2026-07-14-PR-923.md`](../validate-pr/2026-07-14-PR-923.md).

### Notes
- This completes the §2.4 website live-review round (PR #921 polish, PR #922 per-domain pages, PR #923 title-links + spacing, PR #924 contents sidebar), all merged and auto-deployed. The remaining §2.4 items are the maintainer's Cloudflare console actions (confirm the build-watch-paths include the 11 domain directories) and the publish go-decision; the item stays open until publish.

## 2026-07-14, Library Version 2026.07.411, PR #923

Title-as-link across the public `grclibrary.ai` site plus a domain-page spacing fix (backlog section 2.4, the third maintainer-review PR), and the batched PR #922 post-merge QA (which folded in two in-window fixes). No corpus document changed and no generated artefact was touched.

### Changed
- **Landing-page feature-card titles are now links.** Each of the 15 feature-card keyword labels in [`.web/templates/landing.html`](../../.web/templates/landing.html) links (new tab) to the corpus page it asserts, per the maintainer-approved mapping: STRUCTURED and STYLE to [`specification-master-project.md`](../../specification-master-project.md); CROSS-LINKED to [`docs/portal.md`](../../docs/portal.md); PRACTICAL to [`docs/adopter-guide.md`](../../docs/adopter-guide.md); INTEGRITY to [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md); CITATIONS to [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md); ALIGNMENT to [`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md); GENERATED to [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md); TESTED to [`tests/README.md`](../../tests/README.md); and the six governance-pack rule names to their identically-named rule files in the claude-rules governance pack.
- **Domain-page document names are the links.** [`.web/build.py`](../../.web/build.py)'s per-domain document rows now render the document NAME as the link to its GitHub source (new tab, with a small external-jump arrow); the previous separate "GitHub" link is removed (one link per row, better for screen readers).
- **Domain-page spacing tightened.** [`.web/templates/domain.html`](../../.web/templates/domain.html)'s page-scoped styles reduce the section and hero vertical padding and the inter-element margins, scoped to the domain pages only so the content-rich landing page is unchanged, so the document list is reachable without much scrolling, notably on an iPad (maintainer-flagged).

### Fixed
- **PR #922 post-merge review, both in-window.** The deploy runbook [`.working/cloudflare-pages-setup.md`](../../.working/cloudflare-pages-setup.md) Overview still described a two-page site with a two-file input allow-list; it now describes the 13-page site and the domain-README inputs (runbook 1.0.3 to 1.0.4). And [`.web/build.py`](../../.web/build.py)'s `read_domain_purpose` passed `re.split` maxsplit positionally (a Python 3.13-plus DeprecationWarning); it now uses the keyword form.

### Verification
- The generator's `--check` is rc=0 (13 pages render) and emits no DeprecationWarning under `-W always`. All 15 landing card labels render as links to the intended targets (the 14 distinct target files, 15 links with STRUCTURED and STYLE both pointing at the master spec, confirmed to exist); every off-site link carries `target="_blank" rel="noopener"` and every internal anchor lacks it; the domain document rows carry no separate "GitHub" link. Full `tools/run_all_audits.sh` = 69/69; the external-link lint passes with `grclibrary.ai` allow-listed.
- **PR #922 post-merge validation** (Subagent A, refute-briefed, read-only-git on `34496d0`): SHIP-WITH-NOTES, 0 error / 2 warning / 0 note (F1 runbook Overview, F2 the `re.split` deprecation), both FIXED here; record at [`2026-07-14-PR-922.md`](../validate-pr/2026-07-14-PR-922.md).

### Notes
- Card-title link tier: these 15 links are static references to pre-verified corpus files (the 14 distinct targets confirmed present) plus one mechanical generator tweak, verified by render, full-file grep, and the suite rather than a separate skeptical-verifier subagent. STYLE was linked to the master spec per the maintainer, not left unlinked.
- Follow-up queued and maintainer-approved: a sticky left navigation sidebar (the six section links plus a Domains heading and the 11 domain links) that collapses to a boxed Contents panel on narrow screens, to show the site's breadth up front (PR4; TODO section 2.4).

## 2026-07-14, Library Version 2026.07.410, PR #922

Per-domain pages for the public `grclibrary.ai` site (backlog section 2.4, the second of the two maintainer-review PRs), plus a hero-paragraph width fix and the batched PR #921 QA. The generator now renders one page per corpus domain (13 pages in all: the landing page, the about page, and 11 domain pages); no corpus document changed and no generated artefact was touched. The site stays preview-until-publish on the maintainer's go.

### Added
- **A page per governance domain** (11 pages), rendered by [`.web/build.py`](../../.web/build.py) from a new shared-layout template [`.web/templates/domain.html`](../../.web/templates/domain.html). Each page carries: the domain's Purpose intro extracted from its own domain README (a list-lead-in Purpose, the dev-security case, folds the following list items' lead-in sentences in so no dangling colon renders); the domain's full document list (title and type from [`taxonomy.yml`](../../taxonomy.yml), sorted by type then title), each document linking to its GitHub source in a new tab; and per-page SEO metadata (a page title, a meta description, and a canonical URL on the site domain). The 11 pages hold 310 documents in total, matching the register counts; the 2 root specification documents correctly have no domain page.

### Changed
- **Register-table domain links.** The landing page's section-04 register now links each domain name to its on-site domain page.
- **Hero intro paragraph fills the column width.** `.hero .dek` in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) dropped its `max-width: 60ch` cap for `max-width: none`, so the first paragraph on every page (landing, about, and the 11 domain pages) fills to the same width as the section paragraphs and the card grid instead of wrapping short. Maintainer-flagged; the companion to PR #921's `.lede` fix.
- **Generator help-text plurality sweep.** [`.web/build.py`](../../.web/build.py)'s module docstring and argparse description now describe the landing, about, and per-domain pages (was "landing + about pages" in several places; also "figure on the page" to "on the pages", "seeded the template" to "seeded the templates", "the two pages cannot drift" to "the pages cannot drift"). This closes PR #921's post-merge validation note (the full-file-grep completeness lesson) and reflects the now-larger page set.
- **Content boundary widened, deliberately and minimally.** The generator's read allow-list now includes the eleven domain READMEs (public corpus content; only the Purpose paragraph is used); the docstring's CONTENT BOUNDARY section records the addition. It still never walks the repository and never reads `.working/`, `.claude/`, `tools/`, `tests/`, `.github/`, or the sibling repositories.
- **Allow-listed the project's own site domain.** [`tools/lint-external-link-domains.py`](../../tools/lint-external-link-domains.py) gained the `grclibrary.ai` domain for the canonical URLs the domain pages emit (the project's own public site, not a citation publisher, so the citation-verification specification is unchanged; no gate weakened).

### Fixed
- **Attribute-context and href hardening** (PR2 skeptical-verifier low findings): the escaping helper now also escapes the double-quote so it is safe in an attribute context, and the document-link URL is escaped. Not exploitable today (taxonomy paths and curated scope strings are clean); a latent-gap close. The stale `parse_taxonomy` docstring (it now also returns the title) was corrected.

### Verification
- The generator's `--check` mode is rc=0 (corpus parses, 13 pages render); a full render wrote 13 pages. Per-domain document-row counts equal the taxonomy per-domain counts and sum to 310; every GitHub link on domain page X points into the X directory (no cross-page bleed; a document in a subdirectory, such as the privacy jurisdiction annexes, resolves correctly). There are 0 external links without a new-tab attribute and 0 internal anchors with one; 0 working-state, private-tree, email, or absolute-path leaks across the 11 domain pages. Full `tools/run_all_audits.sh` = 69/69.
- **PR2 skeptical verifier** (refute-briefed, read-only-git): SHIP-WITH-NOTES, 0 critical / 0 high, 0 content-boundary leaks. One Medium (the dev-security dangling-colon intro) FIXED here by the list-lead-in fold; two Lows (attribute escaping; the stale docstring) FIXED here. Re-verified: the dev-security intro now renders as a complete sentence and the other 10 intros are unchanged.
- **PR #921 post-merge validation** (Subagent A, refute-briefed, read-only-git on `389e8e9`): SHIP-WITH-NOTES, 0 error / 0 warning / 1 note (the docstring carriers), FIXED here; record at [`2026-07-14-PR-921.md`](../validate-pr/2026-07-14-PR-921.md).

### Notes
- Follow-up queued (maintainer-directed 2026-07-14): make the landing-page feature-card titles (STRUCTURED, CROSS-LINKED, PRACTICAL, INTEGRITY, CITATIONS, and the rest) link to the corpus page each asserts or accomplishes. The orchestrator will present the proposed card-to-link mapping for maintainer review before implementing it (tracked in TODO section 2.4).

## 2026-07-14, Library Version 2026.07.409, PR #921

Maintainer-review polish of the public `grclibrary.ai` site (the two-page site shipped in #919-#920), plus the batched PR #920 post-merge QA. Three visible fixes (paragraph width, stat-cell overflow, new-tab external links), three housekeeping items (generator help text, runbook pointer, dead CSS), and no corpus-content or generated-artefact change. The site remains preview-until-publish on the maintainer's go; it is already live on Cloudflare Pages with the custom domain grclibrary.ai assigned.

### Changed
- **Section body paragraphs fill the column width.** `.lede` in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) dropped its `max-width: var(--measure)` (64ch) reading cap for `max-width: none`, so the landing page's section paragraphs (sections 01, 02, 03, 05, 06) fill to the same right edge as their headings and the card grid below them instead of wrapping short. (The About page's section 02 already used this treatment from #920; the shared partial now matches, and the maintainer confirmed this full-width intent twice.)
- **Word-valued stat cells no longer overflow.** Added `.stat .num:not(.tnum) { font-size: clamp(1.15rem, 2.4vw, 1.55rem); line-height: 1.15; }` in the same partial, so the two control-band cells whose value is a word ("Continuous", "CC BY-SA", which carry `.num` without the tabular-numeral `.tnum`) are sized down to fit their box, while the numeric cells (312, 11) keep the large `.num` size.
- **All off-site links open in a new tab.** Added `target="_blank" rel="noopener"` to every external link across both pages and the shared footer: the Creative Commons licence link in [`.web/templates/landing.html`](../../.web/templates/landing.html) and [`.web/templates/partials/footer.html`](../../.web/templates/partials/footer.html), the governance-pack link, and the About page's LinkedIn, GitHub, contributing-guide, and seven contributor-profile links in [`.web/templates/about.html`](../../.web/templates/about.html). Internal anchors and root-relative links are unchanged. (Scope note: the maintainer named the licence and domain links; this applied the same rule to every off-site link for consistency.)
- **Generator help text pluralized.** [`.web/build.py`](../../.web/build.py) module docstring (first line and the output-is-ephemeral line) and the argparse `description` now say the generator renders the landing and about pages ("templates" plural), correcting three singular carriers the two-page restructure left stale (the in-window note from #920's post-merge sweep, fixed here across all three).
- **Deploy runbook pointer.** The pre-publish checklist in [`.working/cloudflare-pages-setup.md`](../../.working/cloudflare-pages-setup.md) now points at [`.web/templates/about.html`](../../.web/templates/about.html) for the bio and credentials (moved there in #920), not the landing page; Version 1.0.1 to 1.0.2.

### Removed
- **Dead CSS.** The unused `.m-creds` and `.m-creds span` rules in [`.web/templates/partials/head-style.html`](../../.web/templates/partials/head-style.html) (the maintainer credential-strip styling, orphaned when #920 moved the bio to the About page and dropped the strip markup) were removed. No template references `.m-creds` (grep-confirmed 0).

### Fixed
- The one in-window finding from #920's post-merge PR-scoped sweep (the singular-form generator docstring carriers) is fixed here at class width (all three carriers), not just the cited line.

### Verification
- [`.web/build.py`](../../.web/build.py) `--check` rc=0 (corpus parses, both pages render); a full render wrote 2 pages. Contradiction greps all clean: 0 external links without `target="_blank"` in the templates, 0 internal anchors with `target="_blank"`, 0 residual `.m-creds`, 0 residual singular "landing page" in the generator. Full `tools/run_all_audits.sh` = 69/69 after the edits. Rendered output confirmed to carry the CSS changes and the new-tab attributes on the licence link, the footer licence link, and a contributor handle.
- **PR #920 post-merge PR-scoped sweep** (Subagent A, refute-briefed, read-only-git on `8315c78`): SHIP-WITH-NOTES, 0 error / 0 warning / 3 note. N1 docstring lag fixed here; N2 name-form (the "Jeff Posluns" byline versus the [`AUTHORS.md`](../../AUTHORS.md) "Jeffrey Posluns" long form) is the maintainer's intended public byline, no action; N3 three citation-edition doubts (ISO/IEC 27018:2025, NIST SP 800-88 Rev. 2, CSA CCM v4.1) REFUTED against [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) as current, recently-verified editions. Content boundary re-confirmed clean; record at [`.working/validate-pr/2026-07-14-PR-920.md`](../validate-pr/2026-07-14-PR-920.md).

### Notes
- Run by the resumed VM orchestrator session after the cloud session (`claude/cloudflare-public-website-2d7sis`) that merged #918 to #920 crashed mid-work; this session took over the abandoned lease (120-plus minutes stale, branch fully merged) at the maintainer's direction. The corpus-wide `/resume` `/validate` was deliberately skipped and surfaced: the prior session crashed rather than closing via a QA-skipping handoff PR, so the loop-break trigger is absent, and `main` was green 69/69 with #918 and #919 fully QA'd and #920's QA carried here. PR2 will add the per-domain pages, the register-table domain links, and per-page SEO metadata.

## 2026-07-14, Library Version 2026.07.408, PR #920

Restructured the public `grclibrary.ai` site from a single landing page into two pages that share one single-source layout: the landing page and a new About & contributors page. The maintainer bio moved off the landing page onto the About page, which also acknowledges the project's named contributors with links to their GitHub profiles. Also aligned the landing page's ISO/IEC 5259 citation to the register form (maintainer-directed), reformatted the console statusline projection to a compact form (maintainer-directed), and batched PR #919's post-merge QA. No corpus document changed and no generated artefact was touched; the public site is still preview-only (the Cloudflare deploy is held for the maintainer's go).

### Added

- [`.web/templates/about.html`](../../.web/templates/about.html): the new About and contributors page (the site's second page, at the /about route). It carries the maintainer bio (moved verbatim from the landing page's former §07, credentials on the name line as "Jeff Posluns, CGEIT, CISSP"), a contributors-and-acknowledgements section, and a professional invitation for any acknowledged or new contributor to submit a pull request adding a short bio. The contributor list (seven names, first-name-ordered, each with a link to the contributor's GitHub profile) is drawn from the repository's own [`AUTHORS.md`](../../AUTHORS.md); names are real-person detail the maintainer explicitly authorized listing, and no bio text is fabricated (bios arrive only by contributor-submitted PR). The maintainer email is deliberately NOT on the page.
- The four shared layout partials under [`.web/templates/partials/`](../../.web/templates/partials/): [`head-style.html`](../../.web/templates/partials/head-style.html) (the inline CSS), [`topbar.html`](../../.web/templates/partials/topbar.html) (the masthead document-control strip), [`footer.html`](../../.web/templates/partials/footer.html), and [`script.html`](../../.web/templates/partials/script.html) (the theme-toggle script). Both pages include these from the single source, so the shared chrome cannot drift between the two pages.

### Changed

- [`.web/build.py`](../../.web/build.py): refactored from single-page to two-page rendering. New `load_partials()` reads the four partials; `figure_values()` returns the seven corpus placeholders (`CALVER`, `DOC_TOTAL`, `DOMAIN_COUNT`, `DOMAIN_DOC_TOTAL`, `ROOT_COUNT`, `DOMAIN_ROWS`, `TYPE_CHIPS`); `render_page()` does a two-pass placeholder substitution (partials first, then corpus figures, because the topbar and footer partials themselves carry `CALVER` / `DOC_TOTAL` / `DOMAIN_COUNT`); `render_site()` loops the page list and asserts every corpus value is used by at least one page. An unknown or leftover placeholder is a hard error. The content boundary is UNCHANGED: the generator still reads EXACTLY the taxonomy, the README, and the templates and partials under [`.web/templates/`](../../.web/templates/), and its only outputs are the two pages; the About page's content is static template prose (bio and contributors), adding no new input to the allow-list. The docstring was updated to describe the two-page site.
- [`.web/templates/landing.html`](../../.web/templates/landing.html): the inline CSS, masthead, footer, and theme script were replaced by the four partial placeholders (single-source with the About page); the former §07 "About the maintainer" section was removed (its content moved to the About page); the wordmark was wrapped in a home link; and the footer navigation links were repointed to absolute-from-root targets, with the former About link now pointing at the About page.
- Landing-page §05 standards list: no citation-form change (net). A #920 attempt to render ISO/IEC 5259 without its year (matching the register's bare Standard-column identifier) and to expand OWASP ASVS 5.0 to 5.0.0 was reverted to the #919 rendering (ISO/IEC 5259:2024 and OWASP ASVS 5.0) after the maintainer set the release-year form as the norm and directed a holistic repo-wide standardization review, registered as [TODO section 3.74](../../TODO.md). Citation-form is deferred to that review rather than changed piecemeal here.
- Statusline projection format, [`.working/next-prs.txt`](../next-prs.txt) plus the codifying convention in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (PR-workflow step 6): the first line was reformatted to a compact form of roughly 120 characters or under, each item a very brief few-word description, with at least three items, because the console `next:` statusline surfaces only the first line and truncates it at roughly 120 characters (the prior verbose line was cut off mid-sentence). Longer detail and the further-out queue moved to the following `# then:` comment line, which the statusline does not surface. Maintainer-directed 2026-07-14.
- [`.working/cloudflare-pages-setup.md`](../cloudflare-pages-setup.md): updated the "what is being deployed", tracked-files, and content-boundary lines from a single landing page to the two-page static site (landing plus about/contributors), and from "the template" to "the page templates and shared partials".
- [`.working/third-party-issues.md`](../third-party-issues.md): recorded (with a version bump) the commit-signing behaviour observed in this session type: the signing key is absent, so feature-branch commits are GitHub-Unverified, while the squash-merge produces a GitHub-signed (Verified) commit on `main`; amending cannot sign, so branches are not rewritten for it.
- **Batched #919 QA (recursion-avoidance):** the #919 `/validate-pr` history row and its per-PR detail file [`.working/validate-pr/2026-07-14-PR-919.md`](../validate-pr/2026-07-14-PR-919.md), and the #919 `/retro` row in [`.working/improvement-log.md`](../improvement-log.md).

### Verification

- **Deterministic template split, proven by render + diff.** The landing-to-partials split was driven so the rendered landing page differs from the pre-refactor baseline in exactly the four intended ways (the four partial substitutions and the §07 removal), confirmed by rendering both and diffing. `python3 .web/build.py --check` parses and computes clean, and a full render produces `index.html` plus `about/index.html`.
- **Content-boundary re-scan of BOTH rendered pages.** No leak patterns: no email address, no `.working/` or `.claude/` path or content, no sibling-repo name, no absolute filesystem path; the only `jposluns` occurrences are the intended LinkedIn, GitHub, and CONTRIBUTING links. The About page's contributor GitHub links resolve to the handles recorded in [`AUTHORS.md`](../../AUTHORS.md).
- No corpus-document body changed; no generated artefact (taxonomy, portal, scorecard) was touched, so none was regenerated. Gate count stays 69 (the website is not an audit gate).
- **#919 `/validate-pr` (Subagent A, refute-briefed, read-only-git on the #919 merge `1850276a`): SHIP**, 0 error / 0 warning / 2 note. The public-site content boundary is CLEAN (the generator reads a three-file allow-list, walks nothing, and the rendered template leaks no email, internal path, sibling-repo, or absolute path); every landing-page citation matches the register; and the batched #918 phantom-catch correction is complete with the gate-50 Findings cell provably untouched. Of the two notes: F1 (the #919 root CHANGELOG entry's "six records ... reworded" count imprecision, adopter-facing) is FIXED here; F2 (the OWASP ASVS `5.0` vs `5.0.0` version-form nicety, within tolerance) is deferred to the TODO section 3.74 standardization review rather than changed piecemeal. Detail in [`2026-07-14-PR-919.md`](../validate-pr/2026-07-14-PR-919.md).
- The pre-push guard's D2 check caught a missed Version bump on [`.working/cloudflare-pages-setup.md`](../cloudflare-pages-setup.md) (its body changed in this PR but its Version stayed 1.0.0); bumped to 1.0.1 (Date already today). This is the versioned-`.working`-file co-bump miss the #910 retro flagged; re-verified green after the fix.
- **Pre-push skeptical verifier (refute-briefed, read-only-git on the #920 diff `1850276a..HEAD`): SHIP**, no blocking finding. The public-site content boundary was verified at three levels (the [`.web/build.py`](../../.web/build.py) source reads only the taxonomy + README + the fixed partials and templates, with no repo walk, subprocess, or network; a template-tree leak grep; and a scan of the actual rendered bytes of both pages, no leak and no leftover placeholder); the seven contributor names and GitHub handles match [`AUTHORS.md`](../../AUTHORS.md) exactly and no maintainer email appears on either page; the restructure is byte-faithful (the §05 standards list and the moved chrome CSS are byte-identical to the #919 base, so the citation revert is provably net-zero); and the F1 fix is confirmed live in the #919 root entry. Two non-blocking NOTES: (1) the maintainer bio's professional claims are self-authored content on the maintainer's own site (surfaced for a pre-deploy accuracy confirm, not a defect); (2) the unused `.m-creds` CSS carried verbatim in the faithful chrome move is pre-existing dead CSS (cosmetic; a follow-up cleanup, not a #920 regression).
- Gated by the pre-push guard ([`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) then [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh)) and [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py), each run standalone and unpiped before this PR's push; the push proceeds only on a green guard.

## 2026-07-14, Library Version 2026.07.407, PR #919

The public `grclibrary.ai` landing-site build (backlog §2.4), plus the in-window correction of PR #918's audit trail that its post-merge `/validate-pr` surfaced. The website is a new build surface (a generator, a page template, and a separate CI health check); it publishes no adopter-facing corpus content and adds no corpus document. Housekeeping and a new build surface only.

### Added

- [`.web/build.py`](../../.web/build.py): a stdlib-only static-site generator that renders the public landing page from the LIVE corpus at build time. Every corpus figure (the document total, the per-domain breakdown, the document-type chips) is recomputed from [`taxonomy.yml`](../../taxonomy.yml) and the library CalVer is read from [`README.md`](../../README.md); nothing is hardcoded. `--check` mode parses-and-renders without writing, for the CI health check. Content boundary: the generator reads EXACTLY three inputs (the taxonomy, the README, and the template) and never walks the repository or reads `.working/`, `.claude/`, `tools/`, `tests/`, `.github/`, or the private sibling repositories, so no internal or working-state content can reach the public page through it.
- [`.web/templates/landing.html`](../../.web/templates/landing.html): the self-contained landing page (all CSS and JS inline, system fonts, no external requests, theme-aware light and dark), with seven corpus-derived placeholders the generator substitutes.
- [`.github/workflows/web-generator-health.yml`](../../.github/workflows/web-generator-health.yml): a coupling-breakage detector that runs `.web/build.py --check` on push-to-`main` and on pull requests, so a corpus change that the generator can no longer parse is caught at PR time rather than as a red production deploy. It is deliberately SEPARATE from [`quality.yml`](../../.github/workflows/quality.yml) and is NOT one of the audit-programme gates (the four-surface parity gate counts only that workflow's gates, so the gate count stays 69); least-privilege (`contents: read`), SHA-pinned actions.
- [`.working/cloudflare-pages-setup.md`](../cloudflare-pages-setup.md): the maintainer runbook for standing up and re-deploying the site on Cloudflare Pages; every vendor-specific value is marked `[confirm live]`.
- [`.gitignore`](../../.gitignore): ignores `.web/dist/` (the rendered output is an ephemeral build artefact, never committed; Cloudflare rebuilds it from the live corpus on each deploy).

**Worker provenance:** [`inbox/grclibrary-landing-page/MANIFEST.md`](../../../grc_library_scratch/inbox/grclibrary-landing-page/MANIFEST.md) (the finalized landing-page design and build spec; the worker had read-only `grc_library` access and produced a design deliverable, not a corpus diff. The orchestrator authored the `.web/` generator and template per its delivered build spec, recomputing every figure from the live taxonomy, then independently re-verified the content boundary, the rendered figures, and every §05 standard edition against [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md)).

### Fixed

- **PR #918 phantom-catch correction** (batched here per recursion-avoidance, as #918's `/validate-pr` in-window finding). #918 had recorded a 5th "fix", a latent gate-50 Check-1 failure in which #917's exemption row was said to lack the recognized marker. The #918 `/validate-pr` (Subagent A), re-verified by the orchestrator on three legs, refuted it: #917's Findings cell (`c[4]`, the cell gate 50 reads) already carried the recognized marker at the parent `9cb42fe`; the #918 edit had landed in the Touched-files cell (`c[3]`, which gate 50 does not read); `parse_validate_pr_status` reads `c[4]`. No latent failure existed and #917 was always handoff-exempt; the genuine #918 fix count is four. Corrected the six carriers of the false claim ([`CHANGELOG.md`](../../CHANGELOG.md), this mirror's #918 entry, [`.working/validate-sweeps/2026-07-14-sweep104-iter1.md`](../validate-sweeps/2026-07-14-sweep104-iter1.md), and the [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) Sweep 104 row) and reverted the redundant `c[3]` edit in [`.working/validate-pr/history.md`](../validate-pr/history.md) (the `c[4]` marker left untouched, so gate 50 still classifies #917 handoff-exempt). The immutable `1ae6e7a` commit-message body also carries the claim and cannot be rewritten; this entry is the correction of record. Root cause: an inferred-as-verified state assertion (characterizing a table cell without reading the actual Findings cell), logged in the #918 `/retro` row.

### Changed

- [`.web/templates/landing.html`](../../.web/templates/landing.html) §06: reworded "across all eleven domains" to "across every governance domain", removing the single corpus-coupled prose count the generator does not drive via a placeholder (the website verifier's one NOTE: latent drift, currently accurate). Every other corpus figure on the page is generator-driven.
- **Batched #918 QA**: the #918 `/validate-pr` history row and its per-PR detail file [`.working/validate-pr/2026-07-14-PR-918.md`](../validate-pr/2026-07-14-PR-918.md) (1 warning + 1 dependent note, the phantom-catch above), and the #918 `/retro` row in [`.working/improvement-log.md`](../improvement-log.md) (the inferred-as-verified lesson).

### Verification

- **Website skeptical verifier: SHIP** (no blocking finding across six refutation targets: the content-leak boundary holds; figures are exact [312 documents, 310 across 11 domains plus 2 root, 17 document types]; `--check` efficacy holds; every §05 edition matches the register; HTML is valid and self-contained; CI parity is intact at 69 gates and the separate workflow does not perturb four-surface parity). Its one NOTE (the §06 count) is addressed above.
- `python3 .web/build.py --check` OK after the §06 reword (312 documents, 11 domains, 17 document types, library `2026.07.406` at author time).
- The #918 `/validate-pr` Subagent A ran read-only-git on the #918 diff and confirmed the four genuine #918 fixes CLEAN; a corpus-wide grep over all `.md` file types confirmed zero live residual of the phantom claim outside the corrected surfaces, and the unrelated #452 and #588 historical hits untouched.
- No corpus-document body changed; no generated artefact (taxonomy, portal, scorecard) was touched, so none was regenerated.
- Gated by the pre-push guard ([`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) then [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh)) and [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py), each run standalone and unpiped before this PR's push; the push proceeds only on a green guard.

## 2026-07-14, Library Version 2026.07.406, PR #918

First PR of the 2026-07-14 resumed session (`claude/cloudflare-public-website-2d7sis`; ATTENDED, maintainer-scoped to a SINGLE task, the §2.4 Cloudflare public-website build, then back to a VM). The mandatory loop-break `/validate` (**Sweep 104**) over the #915..#917 delta window, plus the in-window documentation-accuracy fixes it surfaced. Housekeeping + audit-tool-docstring accuracy only; no corpus-document body changed.

### Changed

- **Ran Sweep 104** (loop-break compensating control for session-closing handoff PR #917), full three-subagent A/B/C dispatch over #915..#917. Mechanical baseline 69/69 at `9cb42fe`/#917 (a descendant of the asserted green-at `7596f18`/#916; no close-vs-start drift). **A: 2 note / B: 2 note / C: 1 warning; 0 error, no High/Medium.** Loop-break control for #917 PASSES; all #917 asserted expectations corroborated, 0 contradicted; the #916 CHANGELOG reformat re-verified fact-for-fact against the detailed mirror with gate-59 headers byte-identical. Detail in [`.working/validate-sweeps/2026-07-14-sweep104-iter1.md`](../validate-sweeps/2026-07-14-sweep104-iter1.md); history row in [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md).
- **C-1 (warning) fixed**: [`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py) module-docstring header "The four checks:" corrected to "The five checks:" (it enumerates five; Check 5 shipped in #913, the §6 spec prose was fixed in #915, but this sibling docstring header was missed). Gate 50 re-run standalone: OK.
- **A-1, A-2, B-1 (note) fixed** in the advisory [`tools/audit-changelog-entry-length.py`](../../tools/audit-changelog-entry-length.py) docstring/regex: (A-1) the sentence-vs-total framing reworded so the 67-140 figure reads as a total-word range, not a single-sentence figure, dropping the contradictory "140-word sentence under the 130-word total ceiling"; (A-2) the sentence-splitter regex extended from `[.)"']` to `[.?!)"']` so `?`/`!` terminators split correctly, which makes the docstring's "false positive not possible, only false negative" claim true (the change only adds split points, the false-negative-safe direction), with the comment and docstring reconciled; (B-1) the docstring's recycled `§1.2` provenance reference replaced with "PR #916, the root-CHANGELOG reformat" (the §-close cleanup discipline). `--self-test` 6/6; live run unchanged (867 entries, densest sentence PR #909 at 60 words).
- **Close-out re-baseline "catch" (WITHDRAWN as a PHANTOM; corrected in PR #919)**: this entry originally recorded a 5th in-window fix, a supposed latent gate-50 Check-1 failure in which PR #917's handoff-exemption row was said to "lack" the recognized marker. That was wrong. The #918 `/validate-pr` (Subagent A) refuted it on three legs, each re-verified by the orchestrator against the actual files: (1) at the parent `9cb42fe`, #917's **Findings cell** (field `c[4]`, the cell gate 50 reads) already carried `SKIPPED (handoff-PR exception)`; (2) the orchestrator had instead read the **Touched-files cell** (`c[3]`, which begins "SESSION-CLOSING HANDOFF PR" and which gate 50 never reads), and the "fix" edited `c[3]`, leaving `c[4]` byte-identical in the #918 diff; (3) gate 50's `parse_validate_pr_status` reads `c[4]`, which matched all along, so #917 was always classified handoff-exempt. No latent failure ever existed. The genuine #918 in-window fix count is **four** (C-1 + A-1/A-2/B-1); this 5th item is withdrawn and the redundant `c[3]` edit is reverted in #919. Root cause: an inferred-as-verified state assertion (characterizing a table cell without reading the actual Findings cell), the class [`evidence-grounded-completion`](../../dev-security/claude-rules/governance/evidence-grounded-completion.md) exists to prevent; logged in the #918 `/retro` row and the [`.working/validate-pr/2026-07-14-PR-918.md`](../validate-pr/2026-07-14-PR-918.md) record.
- **B-2 (note, OUT-OF-WINDOW) routed** to the maintainer, not fixed here: `compliance/procedure-capa.md:126` a "Source" field points at the Internal Audit Standard §1.2 *Domain* table (a possible semantic mismatch); low-confidence, pre-existing, gates 62/65 green, semantic-fit not gate-checkable. Default disposition: leave/track.
- **Resume bookkeeping**: pruned [`.working/session-handoff.md`](../session-handoff.md) to keep-current-plus-one-prior (kept #917 + #914, dropped the 2026-07-13 #887-#900 session's Next-actions / State-snapshot / Asserted-expectations blocks; neutralized the dangling "#900 ... below" pointer; recorded the maintainer's Cloudflare-only redirect and the Sweep-104 result); ACQUIRED the concurrency lease [`.working/session-state.md`](../session-state.md) for this branch (`Status: active`, fresh heartbeat); refreshed [`.working/next-prs.txt`](../next-prs.txt) to the website-build -> Cloudflare-walkthrough queue.

### Verification

- `tools/run_all_audits.sh` = 69/69 on the committed state (the genuine changes are a gate-module docstring and an advisory-tool docstring/regex; no gate behaviour changed), including with the #918 CHANGELOG entry present so gate 50 Check 1 sees #917 demoted from highest-numbered. That pass held because #917's Findings cell already carried the handoff marker (per the withdrawn item above); the redundant `c[3]` Touched-files edit was a no-op and is reverted in #919.
- `tools/audit-changelog-entry-length.py --self-test` 6/6; gate 50 ([`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py)) standalone OK.
- Pre-push guard (`tools/run_all_audits.sh` + `tools/run-pr-time-checks.sh`) green.
- Per the loop-break, the prior session-closing handoff PR #917 took no trailing `/validate-pr` + `/retro`; this Sweep 104 IS that compensating control. This #918 PR is a routine (non-handoff) PR; its own `/validate-pr` + `/retro` batch into the next PR per recursion-avoidance.

## 2026-07-14, Library Version 2026.07.405, PR #917

Session-closing handoff for the 2026-07-14 resumed session (`claude/resume-sweep103-validate` + the §1.2 and handoff branches; attended-autonomous on the VM). Housekeeping + working-state only; no corpus-document body changed.

### Changed

- **Batched #916's post-merge QA**: the `/validate-pr` record + history row (2 in-window note findings) and the `/retro` row, plus the two fixes: F1 the guard-tool docstring's stale "74-147" old-range figure corrected to "67-140" ([`tools/audit-changelog-entry-length.py`](../../tools/audit-changelog-entry-length.py), the correction not propagated when DONE/detailed were fixed), and F2 the detailed-mirror #916 entry's new-range "62-79" corrected to "62-80" (#912's D2 reword had pushed the max to 80).
- **Recorded the §3.73 design-defer** in [`TODO.md`](../../TODO.md) §3.73: the ledger-table-row-integrity gate's naive column-count check is NOT FP-free (a prototype flags ~50 legitimate unescaped-prose-pipe rows across the `.working/` ledgers), and the escaped-defect signature needs a smarter detector (mid-row row-start pattern + per-ledger sequence-gap); build deferred to a fresh session, interim safe row-insert technique codified.
- **Refreshed [`.working/session-handoff.md`](../session-handoff.md)**: prepended this session's Next-actions (CLOSING #915-#917 + NEXT-SESSION Sweep 104), State-snapshot (version snapshot reconciled to library `2026.07.405` / README `1.9.766`, green-at `7596f18`/#916 = 69/69), and Asserted-expectations blocks (scoped to what #915/#916 mechanically verified, with the deferred items listed as explicit NOT-asserted-clean soft spots). Per the discipline the handoff only PREPENDS; the next `/resume` prunes to keep-current-plus-one-prior.
- **Added the [`.working/session-metrics.md`](../session-metrics.md) row** (~1h35m elapsed; 2 substantive PRs; 8 subagents; ~1.68M measured subagent tokens, a real sum since the active window had no compaction; orchestrator tokens `not instrumented`).
- **Released the concurrency lease** [`.working/session-state.md`](../session-state.md) (`Status: released`, `Active-session: none`).
- **Refreshed [`next-prs.txt`](../next-prs.txt)** to the next-session queue (Sweep 104 -> §3.73 build + low-risk cleanup -> protected machinery -> routed forks -> attended backlog).

### Verification

- All 69 gates pass; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green. Per the loop-break, this session-closing handoff PR takes NO trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 104) over the #915..#917 delta window, cross-checking this handoff's `## Asserted expectations` block.

### Discipline observation

The wind-down was maintainer-confirmed (twice, via `AskUserQuestion`) on a named mid-run degradation signal: the SAME table-row-insert operation clobbered an adjacent ledger row four times this session (F1@#915 escaped to main and was caught post-merge; the #915 detailed-mirror header and the #914 validate-pr row caught by #916's post-commit audit; the #916 validate-pr row caught by an explicit read-back), plus meta-prose measurement slips (D1/D2, F1/F2@#916). All were caught (net zero adopter escape), but the first-pass mechanical precision on that one operation was failing repeatedly, distinct from the caught-slip density that is not a wind-down trigger. Interim mitigation codified in the #916 retro: insert a ledger row by anchoring the `Edit` on the HEADER line and appending the new row after it, never matching-and-re-appending the next row's leading cells.



## 2026-07-14, Library Version 2026.07.404, PR #916

P1 §1.2 (maintainer-flagged 2026-07-14): the root [`CHANGELOG.md`](../../CHANGELOG.md) entries for #902-#914 had reverted to long, dense, semicolon-chained run-on sentences (67-140 words) a general reader cannot follow, re-introducing the exact drift #908 had just fixed for #887-#901. This PR reformats them and strengthens the guardrail, and carries the batched #915 post-merge QA.

### Changed

- **Reformatted the root CHANGELOG #902-#914 entries** to the compact plain-language form (two plain sentences each, 62-80 words, down from 67-140-word semicolon-chains). Each compression was research-drafted then verified by the orchestrator against the detailed-mirror entry (the research-assistant discipline, as #908 did for #887-#901). Every `**YYYY-MM-DD | X.Y.Z | PR #N**` header is byte-unchanged, so gate-59 mirror-header-parity holds; only the summary prose after `** - ` changed. The detailed-mirror entries are untouched (they remain the full audit trail).
- **Strengthened the advisory guard** [`tools/audit-changelog-entry-length.py`](../../tools/audit-changelog-entry-length.py) (closes TODO §1.2): added a longest-single-sentence signal (`--sentence-warn`, default 65 words) alongside the existing total-word signal, because the #902-#914 drift entries were each a dense single sentence UNDER the 130-word total ceiling, i.e. the word-count-only check missed them. The sentence splitter is crude-by-design (splits on a period-then-space boundary) so it can only under-split (a false negative), never over-flag. Still advisory (exit 0, not gate-wired); self-test extended to 6 cases (adds a dense-run-on-under-the-word-ceiling case and a two-short-sentences-clean case). Live run against the reformatted CHANGELOG is clean (densest sentence now 60 words).
- **Batched #915 post-merge QA** (the Sweep 103 `/validate` close-out; `/validate-pr` + `/retro` rows). The `/validate-pr` caught two in-window `.working/` bookkeeping issues, both gate-blind and both FIXED here:
  - **F1 (warning, table-row-join):** the Sweep 103 row I prepended to [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) merged onto one physical line with the retained Sweep 102 row (the new row lacked the trailing line break), so the Sweep 102 row lost its `| Date | Sweep |` identifier columns. Escaped to `main` because that ledger is not read by gate 50 and the post-edit self-check was skipped. Split back into two well-formed rows (Sweep 102 identifier restored).
  - **F2 (note, Low, paired-surface-value-lag):** `session-handoff.md:38` still read "171+ PRs behind" while #915 freshly wrote "185" elsewhere; reconciled to 185 (and the inherited duplicate `(3)` list marker relabelled).
- **Routed a machinery proposal to TODO §3.73** (from the #915 `/retro` auto-graduation): a structural ledger-table-row-integrity check over the reverse-chronological `.working/` bookkeeping tables. F1 is the FIRST escape of the table-row-join class (all prior occurrences self-caught pre-commit), which refutes the #891 retro's "no gate, the self-check catches it" disposition.

### Verification

- `tools/run_all_audits.sh` all 69 gates pass (post-fix); `tools/audit-changelog-entry-length.py --self-test` 6/6 OK; the live guard run is clean. Root CHANGELOG dash-free; every path-shaped reference in the added detailed lines is a markdown link.
- A pre-push skeptical verifier reviewed the reformat faithfulness (against the detailed mirror) and the guard's sentence logic.

## 2026-07-14, Library Version 2026.07.403, PR #915

First PR of the 2026-07-14 resumed session (`claude/resume-sweep103-validate`, resumed from #914; attended-autonomous, on the VM): the loop-break corpus-wide validation **Sweep 103** over the #901..#914 delta window (the compensating control for session-closing handoff PR #914, which skipped its trailing `/validate-pr` + `/retro`), plus the one in-window finding it surfaced, the handoff prune, the lease ACQUIRE, and the resume-decision bank.

### Changed

- **Sweep 103 result (loop-break control for #914 PASSES).** Full three-subagent A/B/C dispatch over #901..#914. Mechanical baseline **69/69** at `f40a042`/#914 (a descendant of the closing session's asserted green-at `c7ee14f`/#913; no close-vs-start drift); clone non-shallow. Pre-flight: 421 files, 33 suppressed, 11 candidates, all the collection-count-word false-positive class, dismissed by all three subagents. **A: 0** (every substantive #901-#914 edit source-verified: OWASP ASVS 5.0.0 sub-reqs verbatim against held text, all 11 ISO/IEC 20000-1 clauses against the held 2018 TOC, the FR-201 vuln-SLA single-source conversions, TLS/CA/password against the governing policies, LGPD Art. 19 / LFPDPPP Art. 31 verbatim, gate 50 Check 5 logic + fixtures). **B: 0 genuine misses** (all changed values grepped corpus-wide across all file types with zero surviving old-form residual outside the by-design deferred forks §3.66/3.68/3.70/3.71). **C: 1 in-window `note`** (fixed below). **Asserted-expectations cross-check: all CORROBORATED, 0 contradicted.** Detail: [`.working/validate-sweeps/2026-07-14-sweep103-iter1.md`](../validate-sweeps/2026-07-14-sweep103-iter1.md).
- **Fixed the one Sweep 103 finding** (gate-50 §6 detailed-prose completeness, in-window from #913): [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 gate-50 paragraph enumerated internal checks 3 (worker-provenance) and 4 (version-history parity) but not the fifth check added in #913 (the deep-assessment register row-order guard). Added a fifth-check sentence matching the checks-3/4 precedent (register run-number ascending monotonicity, FP-free, register-less forks yield no findings, no count change, the no-count-ripple precedent). Not a genuine miss (gate 35's four-surface parity checks only the §6 table, green at 69; the detailed prose was not in the closing session's asserted-clean set), but the same free-prose slip-class Sweep 77 caught for gate 57. Spec Version `1.17.3` -> `1.17.4`, Date 2026-07-14; [`taxonomy.yml`](../../taxonomy.yml) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated in sync.
- **Pruned [`.working/session-handoff.md`](../session-handoff.md)** per the keep-current-plus-one-prior discipline: deleted the 2026-07-12/13 (#886) Next-actions, State-snapshot, and Asserted-expectations blocks; retained the #914 (current) and #900 (prior) blocks; reworded the two dangling "supersedes ... below" superseding pointers to "(pruned at the Sweep 103 resume)"; advanced the Resume-cursor "Last validation sweep" to Sweep 103.
- **Banked the resume decisions** in [`.working/pending-decisions.md`](../pending-decisions.md) (durable across compaction): mode = attended-autonomous; running order = follow the handoff order; FR-205 MFA (§3.69) = option A (harmonize to user+remote, phishing-resistant for privileged); remaining routed forks = stricter-safe-where-defensible with genuine authorial calls routed.
- **ACQUIRED the concurrency lease** [`.working/session-state.md`](../session-state.md) (`Active-session: claude/resume-sweep103-validate`, `Status: active`, fresh heartbeat); added the Sweep 103 row + Version bump to [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md); refreshed [`next-prs.txt`](../next-prs.txt).

### Verification

- Mechanical baseline and post-fix re-baseline both **69/69** (`tools/run_all_audits.sh`); regression suite 377 OK; both generators `--check` in sync. A pre-push skeptical verifier reviewed the spec §6 addition.
- Per the loop-break, this is the first PR of the resumed session (NOT a session-closing handoff), so it takes its own post-merge `/validate-pr` + `/retro`, batched into the next PR per recursion-avoidance.

## 2026-07-14, Library Version 2026.07.402, PR #914

Session-closing handoff for the 2026-07-14 unattended/overnight r3-remediation session (resumed from #900; 13 merged PRs #901-#913; 0 adopter escapes). Housekeeping + working-state only; no corpus-document body changed.

### Changed

- Refreshed [`.working/session-handoff.md`](../session-handoff.md): prepended this session's Next-actions (CLOSING #901-#914 + NEXT-SESSION Sweep 103), State-snapshot (version snapshot reconciled to library `2026.07.402` / README `1.9.763` / pack `1.61.6` / spec `1.17.3` / gate 69, green-at `c7ee14f`/#913 = 69/69), and Asserted-expectations blocks (scoped to what this session mechanically verified, with the routed forks + protected machinery listed as explicit NOT-asserted-clean soft spots for Sweep 103). Per the discipline the handoff only PREPENDS; the next `/resume` prunes to keep-current-plus-one-prior.
- Added the [`.working/session-metrics.md`](../session-metrics.md) row (measured post-compaction floor ~3.2M subagent tokens across ~18 dispatches; pre-compaction dispatches excluded rather than fabricated; orchestrator main-loop not instrumented).
- Released the concurrency lease [`.working/session-state.md`](../session-state.md) (`Status: released`, `Active-session: none`).
- Refreshed [`next-prs.txt`](../next-prs.txt) to the next-session queue (Sweep 103 -> protected machinery -> routed forks -> cleanup).

### Verification

- Batched #913's `/validate-pr` (0 findings) history row + `/retro` row. This #914 handoff records its OWN [`validate-pr/history.md`](../validate-pr/history.md) exemption row (`SKIPPED (handoff-PR exception)` in the Findings cell) IN ITS OWN DIFF, so gate 50 does not flag it when the next PR demotes #914 from highest-numbered (the recurring #445/#821/#900 handoff-no-row miss, avoided here). Per the loop-break, this closing PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide Sweep 103 over #901..#914, cross-checked against the Asserted-expectations block. Pre-push guard green; a skeptical verifier reviewed the handoff refresh (prune correctness, snapshot reconciliation, exemption row, lease release). Library `2026.07.402`; README `1.9.763`.

### Discipline observation

The wind-down was maintainer-chosen at a status check (surfaced via `AskUserQuestion` with the honest justification + named options), not taken unilaterally: this session's layered verification held (0 adopter escapes across 13 PRs) but the first-pass-catch rate escalated to a genuine correctness defect (#913's fork-safe crash, verifier-caught), a named precision-strain signal. The recommendation carried into the handoff: the remaining protected machinery (G1, handoff-D-check) and the authorial forks are better handled with fresh precision.

## 2026-07-14, Library Version 2026.07.401, PR #913

Deep-assessment r3 machinery: the G3 register row-ordering guard (TODO §3.62 G3, maintainer-authorized at the 2026-07-14 resume, overriding the #888 low-value WATCH), plus the batched #912 QA.

### Added

- **Gate 50 Check 5, deep-assessment register row-order** ([`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py)): a new internal check of the bookkeeping-parity gate that flags a run-table row in [`.working/deep-assessment/register.md`](../../.working/deep-assessment/register.md) whose run number is not strictly greater than the previous run row's (the #888 mis-order class). Implemented as a fifth check WITHIN gate 50 rather than a standalone new gate, the same no-count-ripple precedent as Check 4 (#444): no gate-count change, no four-surface parity re-wiring, no §6 spec enumeration change (gate 50's spec presence is the generic "Bookkeeping-parity audit" inventory row + the §5 group summary, both of which already cover it). A standalone new gate was deliberately NOT chosen: the register is a low-churn 3-row ledger, so a new gate's permanent maintenance + gate-count ripple would be net-negative for the value. FP-free / precision-first (flags only a non-increasing run number); an empty or register-less input yields no findings (fork-safe). Closes the one-of-a-pair gap: the register's sibling structured-bookkeeping files were already gated (the detailed mirror by gate 59, the concurrency lease by gate 63) while the register was not.

### Verification

- Gate 50 runs clean on the current corpus with Check 5 active (the live register is correctly ascending). Four regression fixtures added to [`tests/test_linters.py`](../../tests/test_linters.py) `BookkeepingParityTests` (ascending-passes, mis-order-flags, duplicate-flags, empty-passes); all 27 gate-50 tests pass. The pre-push guard is green (69/69, incl. gate 36 which exercises the new fixtures, and gate 35 which confirms no four-surface parity change from the check addition). A skeptical verifier reviewed the check logic + the no-ripple claim and CAUGHT one real defect (fixed in-window): the initial register read used `read_text_safe(...) or ""`, but `read_text_safe` catches only decode errors (not `FileNotFoundError`) and the read sat outside main()'s FileNotFoundError guard, so a fork that keeps `.working/` but lacks the register would have crashed rather than yielding no findings (falsifying the fork-safe claim); the fix guards the read with an explicit `.is_file()` check, verified to yield no findings on a missing register.

### Batched #912 QA

The #912 `/validate-pr` (0 findings) history row + `/retro` row. Library `2026.07.401`; README `1.9.762`.

### Discipline observation

The maintainer authorized building G1/G3/handoff-D-check at the 2026-07-14 resume; G3 is the one overnight-buildable member (G1 is a `.claude/hooks/` PreToolUse hook and the handoff-D-check requires a [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) + pack-skill recursion-avoidance convention change, both protected-tree edits deferred to a daytime/authorized apply). Building G3 as a gate-50 check (not a standalone gate) is the implementation choice that honors "build G3" while avoiding the net-negative new-gate overhead the guardrail-review's value-flag warned of, resolved by the maintainer's explicit build authorization.

## 2026-07-14, Library Version 2026.07.400, PR #912

FR-201 vulnerability-remediation-SLA single-source-of-truth completion (TODO §3.68, partial), plus the batched #911 QA. A #912 research worker ran a full-corpus carrier enumeration; the FR-201 (#904) "no other document still diverges" claim was over-stated (the §3.68 note's "9-doc scope" missed several carriers). SoT = [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md) section 2 (Critical 24h/72h/7d graded by exploitation, High 14, Med 30, Low 90).

### Changed (clear stricter-safe conversions to cite the SoT)

- [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md) (1.1.8 -> 1.1.9): the full 4-row SLA table (a verbatim-equivalent restatement) replaced with a governing citation to the SoT (kept the surrounding scan-frequency/EOL prose).
- [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md) (1.0.5 -> 1.0.6): KEPT the operational classification table (its Trigger Condition and Authorization columns are load-bearing operational detail the SoT does not carry) and added a governing note re-anchoring the Deployment-Timeline column to the SoT section 2 (the doc already prose-cited the SoT at :21; the values were still restated in the table).
- [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md) (1.0.8 -> 1.0.9): section 4.5.3 "Critical, 7 days; High, 14 days" restatement -> citation of the SoT. This was a dev-security carrier FR-201 (#904) LEFT unconverted (FR-201's scope caught the SCA standard + dev-requirements but not this policy).
- [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) (1.0.5 -> 1.0.6): the #904 F-1 carrier ":103 Critical patches within 15 days or fewer" (LOOSER than the SoT's 7-day Critical worst case) -> citation of the SoT (stricter-safe; the doc's :101 already deferred to the standard in prose, so the looser value contradicted its own reference).
- taxonomy/scorecard regenerated for the four bumps.

### Routed (divergent values needing maintainer judgment; NOT guessed)

Recorded in TODO §3.68 (kept open as partial) for maintainer decision, per the overnight defer-and-skip discipline (these are authorial, not mechanical conversions):
- `security/standard-penetration-testing-and-red-team.md:88-96`: prose claims alignment with the vuln procedure but the values are LOOSER (High 30d vs 14, Med 60d vs 30); the alignment claim is inaccurate either way. Stricter-safe option (tighten to align) vs intentional-longer-window option (reword the claim) is the maintainer's call.
- `supply-chain/standard-supplier-security-and-privacy-assurance.md:45,60`: third-party supplier-tier bars, intentionally a separate scale from the internal SLA; policy question only, do NOT auto-convert.
- `operations/procedure-patch-management.md:117`: exception-deferral maximums disagree with the SoT section 6 exception table; reconcile which mapping is authoritative.
- `compliance/logistics/register-basc-it-compliance-kpis.md:31,38`: KPI-embedded 7d/14d (consistent); low-priority optional drift-hardening.

### Verification

Research-worker full-corpus enumeration + orchestrator re-read of every converted carrier against the SoT section 2 values (confirmed each restatement was verbatim-equivalent before replacing it with a citation; confirmed the two looser carriers, software-evaluation :103 and policy 4.5.3, defer to the stricter SoT). The sanctioned model restatement ([`dev-security/standard-security-quick-reference.md`](../../dev-security/standard-security-quick-reference.md), which restates the table WITH a governing citation) was left as the intended pattern. Pre-push guard green; a skeptical verifier reviewed the conversions + the routing completeness.

### Batched #911 QA

Fixed the three #911 `/validate-pr` record-hygiene findings (all Low, in-window): F1 the detailed-CHANGELOG #911 "### Fixed" lead count "Six ... across five" -> "Eleven ... across seven documents"; F3 the doc-index register's change-mgmt row bare "ISO/IEC 20000" -> "ISO/IEC 20000-1" (register 1.27.85 -> 1.27.86, regenerated); F2 the stale "6 clause fixes" in next-prs.txt dropped in the rewrite. #911 `/validate-pr` history row + per-PR record + `/retro` row added. Library `2026.07.400`; README `1.9.761`.

### Discipline observation

The §3.68 note (written from the FR-201 verifier's pass) named 3 carriers; the #912 worker's full-corpus enumeration found ~8 actionable, so a prior "find-every-carrier" claim was itself carrier-incomplete. This is why §3.68 dispatched a fresh whole-corpus worker rather than trusting the note's named set, the same lesson as the #911 register carrier. The clear stricter-safe conversions were applied; the value-divergences that need authorial judgment (is a longer pentest window intentional? should supplier bars tighten?) were routed, not guessed, per the overnight defer-and-skip discipline.

## 2026-07-14, Library Version 2026.07.399, PR #911

ISO/IEC 20000-1:2018 clause-attribution accuracy pass (TODO §3.72, routed from #910's reference-breadth research), plus the batched #910 QA. A full-cluster `/claim-fit` over all 9 operations docs citing 20000-1, judged against the held source TOC.

### Fixed

Eleven ISO/IEC 20000-1 clause citations corrected across seven documents (six operations docs plus the governance doc-index register; each Version+Date co-bumped; taxonomy + scorecard regenerated). All held clause titles verified verbatim against the held ISO/IEC 20000-1:2018 full-text in the `grc_library_ref` reference base this turn:

- [`operations/standard-capacity-and-performance-management.md`](../../operations/standard-capacity-and-performance-management.md) (1.0.4 -> 1.0.5): `§8.6 Service management` -> **§8.4.3 Capacity management**. Doubly wrong: §8.6's held title is "Resolution and fulfilment", and "Service management" is not a held clause title at any level (fabricated); capacity management is §8.4.3.
- [`operations/standard-observability-and-telemetry.md`](../../operations/standard-observability-and-telemetry.md) (0.0.5 -> 0.0.6): `§8.6 Service management` -> **§9.1 Monitoring, measurement, analysis and evaluation** (the closest defensible home; observability/telemetry has no dedicated 20000-1 clause, and §8.6 is wrong).
- [`operations/standard-service-level-management.md`](../../operations/standard-service-level-management.md) (1.0.4 -> 1.0.5): the alignment-table `§8.3 Service Level Management` and the prose `§8.3` -> **§8.3.3 Service level management** (§8.3 is "Relationship and agreement"; SLM is the §8.3.3 subclause).
- [`operations/procedure-release-management.md`](../../operations/procedure-release-management.md) (1.0.2 -> 1.0.3): imprecise `Service management requirements` -> **§8.5.3 Release and deployment management**.
- [`operations/standard-it-financial-management.md`](../../operations/standard-it-financial-management.md) (1.0.3 -> 1.0.4): imprecise `Service financial management` -> **§8.4.1 Budgeting and accounting for services**.
- [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md) (1.3.2 -> 1.3.3): four Framework-alignment cells under a column headed bare "ISO/IEC 20000" (no `-1`), which the initial `grep 20000-1` file-discovery MISSED (caught by the pre-push skeptical verifier). Configuration management `§8.5` -> **§8.2.6 Configuration management** (wrong-clause: §8.5 is "Service design, build and transition"; config mgmt is §8.2.6); Change management / Emergency change / CAB governance `§8.5` -> **§8.5.1 Change management** (precise home); column header "ISO/IEC 20000" -> "ISO/IEC 20000-1".
- [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md):273 (1.27.84 -> 1.27.85): the doc-index register's Service Level Management Standard row cited `ISO/IEC 20000-1:2018 §8.3` (coarse, a paired-surface mirror of the SLM doc this pass tightened) -> **§8.3.3**. Caught by the re-verify (outside the 9-doc operations scope; a whole-corpus `ISO/IEC 20000-1 ... §` grep surfaced it). Its sibling row :274 (KPIs register -> §9.1 Monitoring, measurement, analysis and evaluation) is CORRECT and left unchanged.

### Not changed (deliberate)

- [`operations/standard-site-reliability-engineering.md`](../../operations/standard-site-reliability-engineering.md):218 cites 20000-1 at document level ("Service management requirements") with no §-number; SRE is not a named 20000-1 clause, so it is left as document-level rather than forcing a spurious clause (no wrong §number to fix).
- [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md):92 and [`operations/register-it-operations-kpis.md`](../../operations/register-it-operations-kpis.md):21 already cite 20000-1 correctly (document-level).

### Bookkeeping

Closed TODO §3.72 -> DONE; `/claim-fit` history row + detail file [`2026-07-14-iso20000-1-clause-accuracy.md`](../claim-fit/2026-07-14-iso20000-1-clause-accuracy.md). Batched #910 `/validate-pr` (0 findings) history row + `/retro`. Library `2026.07.399`; README `1.9.760`.

### Verification

Research-worker `/claim-fit` pass + orchestrator re-verification: the orchestrator independently re-read the held 20000-1:2018 clause-8 subclause titles this turn (not trusting the worker's TOC extraction) before authoring each correction. Pre-push guard green. The pre-push skeptical verifier CAUGHT two carriers the initial pass missed (the change-management doc's four §8.5 cells under a bare "ISO/IEC 20000" column, and the governance doc-index register's SLM §8.3 row outside the 9-doc operations scope); both fixed in-window. A whole-corpus `ISO/IEC 20000-1 ... §` grep and a bare "ISO/IEC 20000" §-grep now confirm every clause-carrying 20000-1 citation is consistent with the held TOC (0 residual). Total: 11 clause corrections across 7 docs.

### Discipline observation

The intent was find-every-carrier at ROUTING time (#910 declined to fix the 2 spot-caught mis-attributions piecemeal and routed the whole 9-doc cluster here), but the pass ITSELF then hit a narrower carrier-incompleteness: the file-discovery `grep 20000-1` did not match the change-management doc's bare "ISO/IEC 20000" (no `-1`) column header, so 1 of the 9 in-scope docs was silently skipped and its initial record wrongly said "cites no 20000-1 clause". The pre-push skeptical verifier caught it (a wrong-clause Configuration-management -> §8.5 among the missed cells), it was fixed in-window, and the records were corrected. ROOT-CAUSE LESSON (for the retro): a clause-accuracy pass's file-discovery grep must use the BARE standard token ("ISO/IEC 20000"), never the part-qualified form ("20000-1"), because a doc can cite the standard's clauses under a label that omits the part number; the part-qualified grep drops that carrier. This is the bare-token-width discipline applied to file DISCOVERY, not only to contradiction search. Every finding was caught in-window (0 adopter escapes); the recurrence is the authoring-side pattern-width the layered verification then corrected.

## 2026-07-14, Library Version 2026.07.398, PR #910

ISO/IEC 20000 family reference-breadth review (TODO §3.67, maintainer-added), plus the batched #909 QA. One informative corpus citation added; the review's honest bottom line is that the corpus already engages ISO/IEC 20000-1 well.

### Added

- **ISO/IEC TS 20000-11:2021 see-also** in [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md) (Framework-alignment table, between the 20000-1 and ITIL 4 rows; doc 1.0.5 -> 1.0.6, taxonomy + scorecard regenerated). The framework's Purpose states it bridges ISO/IEC 20000-1:2018 and ITIL 4, and TS 20000-11 is exactly "Guidance on the relationship between ISO/IEC 20000-1 and service management frameworks: ITIL" (title verified verbatim against the held source). Added as an INFORMATIVE row (its Relevance cell reads "Informative: bridges the Part-1 requirements and the ITIL 4 process model this framework adopts"), not a normative compliance row, per its guidance nature.

### Changed

- **Batched #909 `/validate-pr` F1 fix:** reworded [`.working/session-handoff.md`](../../.working/session-handoff.md):52 from a bare `§3.64` reference (dead after #909 rotated §3.64 to DONE) to "§3.64 (Phase-4/5, since fully resolved and rotated to DONE in #909)". The #909 orphan grep had wrongly treated the LIVING session-handoff.md as a frozen dated register.

### Bookkeeping

- **TODO §3.67 closed** (ISO 20000 review done) and rotated to the DONE ledger; the reference-audit run recorded in [`.working/reference-audit/history.md`](../../.working/reference-audit/history.md) + a detail file. The §3.63 RB-ETSI secondary see-also was decoupled from §3.67 back to §3.63 (its origin). **TODO §3.72 added** (route the incidental 20000-1 clause-mis-attribution finding to a full-cluster `/claim-fit` pass over the 9 docs citing 20000-1, rather than a piecemeal 2-of-9 fix).
- Batched #909 `/validate-pr` history row + per-PR record + `/retro` row. Library `2026.07.398`; README `1.9.759`.

### Verification

- The ISO 20000 review used the research-assistant discipline: a worker ran the reference-audit new-ingest pass and produced a ranked candidate table; the orchestrator verified the one applied candidate (TS 20000-11 title + fit) against the held source and the live doc before authoring, and confirmed the assessed-not-added candidates (20000-10 has no natural terms-section home; TS 20000-15 lower fit) against the anti-stuffing guard. The clause-mis-attribution finding was NOT fixed here (routed to §3.72) precisely because the worker spot-checked only 3 of 9 docs and a piecemeal fix would repeat the carrier-incomplete trap. Pre-push guard green; a skeptical verifier reviewed the corpus addition + the §3.67 close.

### Discipline observation

The honest few-finding outcome is the reference-audit working correctly: a new authoritative family landed, and the disciplined result was one informative see-also plus a routed accuracy finding, not a table full of new "compliance" rows. Loading the guidance/vocabulary/TS parts as alignment rows would have been citation-stuffing (the GRC-library-not-implementation-guide guard the maintainer set).

## 2026-07-14, Library Version 2026.07.397, PR #909

Deep-assessment r3 machinery, the low-precision set (the maintainer-decided cleanups from the r3 guardrail/dead-gate findings), plus the batched #908 QA. Closes TODO §3.64 (its last open bullet resolves here; the cluster rotates to the DONE ledger). NO corpus-document body changed.

### Changed

- **Gate 25 dormant-scaffold retirement (DA-gate25-scaffold, TODO §3.64):** removed the three dormant P1/P2/P3-acknowledgement `TERM_PATTERNS` from [`tools/lint-cross-doc-numbers.py`](../../tools/lint-cross-doc-numbers.py). They were added narrow per the Phase 23.26 false-positive analysis and matched 0 corpus documents, so they added no protection while implying coverage the gate did not provide (the r3 dead-gate deep pass surfaced this). Reconciled the paired surfaces: the module docstring (dropped the P1/P2/P3 "terms tracked" list and the forward-scaffold rationale, keeping the empirical no-broaden note) and the [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 design-principle example at the "Conservative scope over false positives" bullet, which had cited the scaffold as a live zero-tracking example. The gate stays ACTIVE on its GDPR-breach-notification term; the regression fixture exercises only that term, so it is unaffected. Maintainer decision (2026-07-14): RETIRE.
- **Gate-41 docstring cross-reference symmetry (r3 guardrail overlap sub-note, TODO §3.62):** added a "Companion note (gate 39 symmetry)" to [`tools/lint-collection-enumeration-consistency.py`](../../tools/lint-collection-enumeration-consistency.py) pointing at gate 39 ([`tools/lint-gate-count-consistency.py`](../../tools/lint-gate-count-consistency.py)), which mirrors this gate's collection-source list. Gate 39's docstring already named gate 41; the reverse pointer was missing, so a future editor of gate 41 had no pointer to the shared collection-source logic. Documentation symmetry only.
- **G5 #376 register candidate expiry (r3 guardrail G5, TODO §3.62):** stamped the disposition on the improvement-log #376 register row and the §3.62 G5 bullet: CODIFIED + EXPIRED as a standalone candidate. Its mechanizable half shipped as gate 50 **Check 4** (version-history parity, #444, the #372 surface); its residual free-prose half is held by the paired-surface-lag convention (the CLAUDE.md close-out checklist). Corrected the §3.62 bullet's imprecise "Check 1" characterization to Check 4 (Check 1 is the QA-cadence-parity §4.6 surface).

### Removed

- The three dormant P1/P2/P3-acknowledgement patterns from gate 25 (see Changed).

### Verification

- Gate 25 runs clean post-retirement (1 tracked term, GDPR-breach-notification; 423 files scanned). The [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 edit bumped that doc 1.17.2 to 1.17.3 (Date 2026-07-14) with [`taxonomy.yml`](../../taxonomy.yml) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (the version-bump-recency gate 40 + the gate-36 regression caught the initial missed bump pre-push; fixed by amend). The pre-push guard is green (69/69 + PR-time checks); the linter-regression suite passes (the gate-25 fixture is GDPR-only). A pre-push skeptical verifier reviewed the gate-logic change and the multi-surface reconciliation.
- TODO §3.64 rotated to the DONE ledger (all 5 bullets resolved: DA-ASVS #902, DA-DORA-A12 #899/#900, DA-AIACT-A26 #899, DA-ISO20000 #907, DA-gate25-scaffold #909); §3.66 (the DA-ASVS Class 2 continuation) re-pointed from "§3.64" to "the r3 DA-ASVS remap #902"; §N-orphan grep confirms no live §3.64 reference remains in TODO (the `.working/` r3 audit-trail records retain their historical §3.64 references, as moment-in-time frozen state).
- Batched #908 `/validate-pr` (0 findings) history row + `/retro` row.

### Discipline observation

The G5 disposition applied the measured-not-inferred guard: the register row and the §3.62 bullet both characterized the #376 mechanizable half as gate 50 "Check 1", but reading the gate 50 source confirmed it is Check 4 (Check 1 is the QA-cadence surface); the disposition corrected the characterization from the source rather than transcribing the stale note (which the pending-decisions bank had also carried as "Check 1"). The gate-25 retirement exercised the audit-gate-change-completeness checklist for a detection-logic change: code + module docstring + §6 spec surface reconciled, fixture confirmed unaffected.

## 2026-07-14, Library Version 2026.07.396, PR #908

CHANGELOG-hygiene PR (closes TODO §3.65) plus the batched #907 post-merge QA.

### Changed

- **Root CHANGELOG compact-form reformat (TODO §3.65):** reformatted the root [`CHANGELOG.md`](../../CHANGELOG.md) entries for PRs #887-#901 from the long multi-sentence paragraphs they had drifted to (109-262 words, the deep-assessment r3 session's reversion) back to the adopted compact one-line form (`**date | version | PR #N** - one-sentence summary`). A research worker drafted the compressions from each entry's detailed-mirror content; the orchestrator verified each against the detailed mirror before applying and dropped one worker-added claim ("regenerating the derived artefacts" on #890) that the source entry did not support. Headers (date/version/PR tokens) are byte-unchanged, so gate 59 mirror-header-parity is unaffected; the detailed mirror is untouched (it already holds the full detail). Compact form preserves no less information: the full audit trail stays in the detailed mirror and git history.
- **TODO §3.63 / §3.64 in-place resolution markers (batched #907 `/validate-pr` F1/F2):** the r3-routed-findings clusters mark bullets `RESOLVED #NNN` in place (not per-bullet DONE-rotation, which the whole cluster gets when its last bullet resolves). #907's `/validate-pr` found the DA-ISO20000 (§3.64) bullet still carried its now-false "could not be judged against ground truth" text and the RB-ETSI-104128 (§3.63) bullet's "add see-also" prose was stale after #907 shipped the primary see-also. Marked DA-ISO20000 `RESOLVED #907` with the false claim corrected, and rescoped RB-ETSI to its remaining secondary [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md) alignment-table target (folded into §3.67). Subagent A's literal delete+DONE recommendation was validated against and adjusted to the cluster's in-place convention (the orchestrator validates verifier recommendations, not auto-applies them).

### Added

- **Advisory length guard [`tools/audit-changelog-entry-length.py`](../../tools/audit-changelog-entry-length.py) (TODO §3.65):** a light `audit-*` advisory (exit 0 always; NOT wired into the audit runner, the CI workflow, or pre-commit, so the parity gates 35/36 do not adopt it) that WARNs on any root entry whose summary exceeds `--word-warn` words (default 130). The threshold clears the legitimate compact-but-multi-item ceiling (the current longest is #906 at 104 words) with margin, catching the 150-262-word drift while not false-positiving on legitimate batch entries. No existing gate covers this (gate 59 checks header parity only); making it a hard gate would be a decorative gate (the compact/long boundary is a judgement call). Inline `--self-test` (5 cases pass); live run clean (858 entries scanned, full recall confirmed).

### Verification

- Advisory tool self-test 5/5 pass; live run over the reformatted file reports 0 entries over threshold (longest #906 at 104 words). All 69 gates pass (pre-push guard). CHANGELOG root+detailed parity holds (headers unchanged by the reformat). Preflight-changelog clean (compact lines dash-free, path references linked).
- Batched #907 QA: `/validate-pr` per-PR record [`2026-07-14-PR-907.md`](../validate-pr/2026-07-14-PR-907.md) + history row (2 in-window TODO findings fixed here; 2 out-of-window notes routed); `/retro` row (the stale-state-on-in-place-resolution observation, single occurrence = watch).

### Discipline observation

The reformat used the research-assistant discipline for a bulk editorial compression (worker drafts, orchestrator verifies each against the source and authors), catching one worker embellishment at apply-time (#890's unsupported artefact-regen claim). The §3.65 close-out exercised the §N-orphan cross-file grep: the only live-§ carrier outside the closing PR's own records was this new tool's own docstring, reworded to drop the live-§ pointer.

## 2026-07-14, Library Version 2026.07.395, PR #907

Two reference-breadth items unblocked by the ISO/IEC 20000 family landing in `grc_library_ref` (#79), plus the completion of the FR-210 title canonicalization the #906 `/validate-pr` flagged.

### Changed

- **RB-ETSI-104128 (deep-assessment r3 section 3.63):** added **ETSI TR 104 128** (Securing AI (SAI): Implementation guidance for the baseline cyber security requirements for AI) as a corroborative see-also in [`ai/guide-ai-security-technical-implementation.md`](../../ai/guide-ai-security-technical-implementation.md)'s standards-references list. It is the paired IMPLEMENTATION guidance for the ETSI EN 304 223 baseline that the AI security standards already anchor to; added as an informative see-also, NOT a normative anchor. Title verified verbatim against the held ref catalogue. Version 1.3.3 to 1.3.4.
- **DA-ISO20000 (deep-assessment r3 section 3.64) RESOLVED:** the ISO/IEC 20000-1:2018 citation in [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md) (framework-alignment table) is now verifiable against the now-held source (previously only ISO/IEC 20000-10 was held). Verified correct (20000-1:2018 = the service-management-system requirements standard, the right one for "ITSM framework compliance") and tightened the reference-cell descriptor "IT Service Management Systems" to the precise Part-1 title "Service management system requirements (Part 1)". Version 1.0.4 to 1.0.5.
- **FR-210 completion:** fixed the one bare "GRC Manager" residual at [`compliance/standard-internal-audit.md`](../../compliance/standard-internal-audit.md):432 (section 10.4 CAPA closure) that #906's canonicalization missed and its `/validate-pr` caught (the whole-line count-grep hid it because the line also carries the fixed "CAE/GRC Programme Manager" form); token-level `grep -oE 'GRC Manager'` is now 0 in the doc. Version 1.2.1 to 1.2.2.
- taxonomy/scorecard regenerated.

### Verification

- RB-ETSI + DA-ISO20000: both edits verbatim-verified against the held ref catalogue this turn (ETSI TR 104 128 title at catalogue:2488; ISO/IEC 20000-1:2018 Part-1 title at catalogue:2142), non-normative (see-also + title precision), so quick-fix-tier with the post-merge `/validate-pr` as the independent check.
- FR-210 residual: token-level `grep -oE` confirms 0 bare "GRC Manager" remaining in the internal-audit standard; TODO section 3.71 (the corpus-wide title sweep) annotated that internal-audit is now fully canonicalized and out of that sweep's scope by completion.
- All 69 gates pass. Batches PR #906's `/validate-pr` (1 in-window Low finding = the FR-210 residual, fixed here) + `/retro` (the carrier-completeness pattern's grep-form sub-lesson: count with token-level `grep -oE`, not whole-line `grep -vE`, for within-line renames).

### Discipline observation

The DA-ISO20000 resolution is the missing-reference SOP working end-to-end: the r3 finding could not be judged against ground truth when only ISO/IEC 20000-10 was held; the maintainer ingested the 20000-1 family; the resume resynced the ref; the citation was then verified and tightened against the held source. The FR-210 residual is the fourth carrier-completeness catch of the session and refined the discipline to a concrete grep-form rule (token-level count for co-occurring old/new forms); every instance was caught by the per-PR `/validate-pr`, none reached the adopter-facing corpus.

## 2026-07-14, Library Version 2026.07.394, PR #906

r3 fresh-reader review (fitness) tail remediation: the remaining medium and low findings, in one batch. (FR-207/209/213 were done in #899; FR-214/215/217/219 are routed as design/enhancement forks.)

### Changed

- **FR-206 (DSR statutory clocks):** added Brazil LGPD 15-day confirmation/access (Art. 19) and Mexico LFPDPPP 20-day ARCO determination (Art. 31), with a strictest-applicable-window rule, to [`privacy/template-dsar-workflow.md`](../../privacy/template-dsar-workflow.md) (SLA cell), [`privacy/procedure-data-subject-rights-management.md`](../../privacy/procedure-data-subject-rights-management.md) (a "Brazil and Mexico fixed windows" note), and [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md) (the DSR-timeframe bullet, the third carrier the verifier's find-every-carrier surfaced). The operational docs previously ran only the GDPR/CCPA/PIPEDA windows while naming LGPD/PIPL in scope.
- **FR-208 (AI-IR Joint Command):** [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md) now defines the previously-undefined "Joint Command" at its first use, via cross-reference to the "Joint command structure" in [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md) (timings consistent: 60 minutes = 1 hour).
- **FR-210 (internal-audit CAE-fallback self-review):** [`compliance/standard-internal-audit.md`](../../compliance/standard-internal-audit.md) section 2.1 corrected the CAE-fallback title "GRC Manager" to the canonical "GRC Programme Manager" and added a self-review carve-out (where that role acts as CAE fallback, the continuous-assurance/control-testing programmes it owns are audited by external auditors under section 2.3(d), preserving the section 2.3 independence rule); the 13 same-document "CAE/GRC Manager" residuals were canonicalized to "CAE/GRC Programme Manager" for self-consistency (the verifier's F-1).
- **Four documentation-hygiene fixes:** FR-211 review-schedule-register adopter note ([`governance/procedure-library-quality-and-review-cadence.md`](../../governance/procedure-library-quality-and-review-cadence.md)); FR-212 cloud entry-point cross-reference ([`docs/adopter-guide.md`](../../docs/adopter-guide.md) to decision-tree section 5.2); FR-216 advisory guideline "must transition" to "should transition" ([`resilience/guideline-emergency-response-and-protective-actions.md`](../../resilience/guideline-emergency-response-and-protective-actions.md), the safety "must not" lines unchanged); FR-218 README acronym/regulator lookup now routes to both the glossary and the key-terms register.
- Version+Date co-bumps on 8 corpus docs (dsar-workflow 1.1.4, dsr-management 1.6.9, privacy-policy 1.4.15, ai-ir 1.0.8, internal-audit 1.2.1, quality-cadence 1.0.20, adopter-guide 1.3.13, emergency-guideline 1.0.2); taxonomy/scorecard regenerated.

### Routed (not changed this PR)

- FR-214 (uniform "Governance Library Maintainer" approving authority, corpus-wide metadata design), FR-215 (phishing-resistant privileged MFA, an enhancement, folds with the FR-205 decision), FR-217 (supplier-questionnaire Yes/No format), FR-219 (portal Board/CEO lane altitude, generated-artefact design) surfaced for maintainer decision. Verifier find-every-carrier follow-up: F-1b, roughly 60 corpus-wide "GRC Manager" title residuals in other docs, routed to TODO section 3.71 (a separate canonicalization sweep).

### Verification

- Substantive-tier skeptical verifier (refute-briefed, per-fix + find-every-carrier): VERDICT SHIP the 7 edits (all values source-correct against the held annexes/register/policy; cross-refs resolve; FR-216 correctly scoped to the one advisory "must"). Two completeness findings were FIXED in-batch rather than deferred (applying the concept-wide find-every-carrier discipline the #904/#905 retros firmed): F-2 (the privacy-policy DSR-clock carrier) and F-1 (the internal-audit same-document title residuals). F-1b (corpus-wide title sweep) routed to TODO section 3.71.
- All 69 gates pass. Batches PR #905's `/validate-pr` (F-1 completion-claim-width note, softened in-window) + `/retro` (the completion-claim-width pattern, 3rd occurrence, convention firmed).

### Discipline observation

This batch is where the #904/#905 concept-wide find-every-carrier lesson paid off: the verifier's per-value/per-title carrier hunt caught a third DSR-clock carrier (privacy policy) and 13 same-document title residuals that a value-specific or cited-line-only grep would have missed, and both were fixed in-batch rather than shipped carrier-incomplete. The subagent's residual COUNT (17) was recounted before fixing (actual 13, 0 bare), per the recount-not-transcribe discipline.

## 2026-07-14, Library Version 2026.07.393, PR #905

FR-202/203/204 (deep-assessment r3 fitness, the value cluster): reconciled three divergent operational security values to their governing authorities. FR-205 (MFA scope) was deliberately NOT changed, routed as a genuine authorial fork.

### Changed

- **FR-202 (TLS):** [`operations/procedure-media-handling-and-transport.md`](../../operations/procedure-media-handling-and-transport.md) section 5.3 removed the "TLS 1.2 may be used where a documented technical constraint prevents 1.3" exception; now TLS 1.3 only, "TLS 1.0, 1.1, and 1.2 must not be used", citing the encryption policy section 4 (which mandates TLS 1.3-or-stronger for data in transit). This closed the last permissive TLS-1.2 carrier among the GRC governance documents (the two OWASP ASVS-baseline lines in [`dev-security/claude-rules/core/owasp.md`](../../dev-security/claude-rules/core/owasp.md) are deliberately retained per the documented pack decision, each with an inline caveat that the pack's canonical mandate is TLS 1.3; they represent the external ASVS baseline, not an org mandate). Version 1.3.7 to 1.3.8.
- **FR-203 (CA key size):** [`operations/standard-certificate-authority-management.md`](../../operations/standard-certificate-authority-management.md) certificate key-size minimum raised from "2048-bit RSA or P-256 ECDSA" to "4096-bit RSA or P-384 ECDSA", per the encryption policy section 6 (Cryptographic algorithms: RSA-4096, ECC P-384 or stronger) and the cryptographic-key-lifecycle framework. Version 1.3.4 to 1.3.5. (The citation section was corrected in-window from section 4 to section 6, the actual home of the asymmetric-key mandate, on the skeptical verifier's catch.)
- **FR-204 (password):** [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) aligned to the authoritative password standard: "Minimum 14 characters" to "14 for standard accounts; 20 for privileged accounts (per the authentication-and-password-management standard)"; "No reuse of the last 10 passwords" to "last 12 passwords". Version 1.0.2 to 1.0.3.
- taxonomy/scorecard regenerated for the three bumps.

### Routed (not changed this PR)

- **FR-205 (MFA scope):** GENUINE FORK. `security/standard-authentication-and-password-management.md:60` mandates MFA "for all accounts" while the IAM and information-security policies scope it to "all privileged accounts and remote access". Not a clean stricter-safe default ("all accounts" literally includes non-interactive service accounts that use managed identity, not MFA). Routed to [`pending-decisions.md`](../pending-decisions.md) + TODO section 3.69 with three named options (recommended: harmonize to "all user/interactive accounts + all remote access, privileged phishing-resistant").
- **FR-203 find-every-carrier follow-up:** the verifier's corpus-wide pass found two dev-security crypto GUIDANCE tables (`standard-security-quick-reference.md:182`, `standard-developer-security-requirements.md:149`) that approve EC P-256 (policy mandates P-384+); a policy-vs-dev-guidance-layer fork routed to TODO section 3.70 (maintainer decides tighten vs accept P-256), rather than silently fixed (avoiding both the FR-127 carrier-incomplete miss and an over-strict guess).

### Verification

- Substantive-tier skeptical verifier (refute-briefed, corpus-wide find-every-carrier per value): VERDICT SHIP after two in-window actions (both done): (1) the CA citation section-4-to-6 correction; (2) the P-256 carriers routed to section 3.70. Find-every-carrier CLEAN for TLS (media-handling was the last permissive carrier among the GRC governance documents; the two deliberately-retained OWASP ASVS-baseline lines in the pack carry an explicit TLS-1.3 canonical-mandate caveat) and password (only the standard + the fixed procedure carry specific values); the DKIM 2048-bit key is different-semantic (correctly untouched). Governing values confirmed verbatim (encryption policy section 4 TLS-1.3, section 6 RSA-4096/P-384; auth standard 14/20 + last-12). FR-205 confirmed untouched. All 69 gates pass.
- Batches PR #904's `/validate-pr` (0 in-window; 1 out-of-window F-1, a 15-day-Critical carrier in `standard-software-evaluation-acceptance-and-lifecycle.md:103` that #904's completion claim over-stated, routed to section 3.68) + `/retro` (the value-completion-claim over-statement pattern, 2nd occurrence, concept-wide find-every-carrier discipline reinforced).

### Discipline observation

The verifier's concept-wide find-every-carrier is the discipline reinforced by the #904 F-1 miss (a value-completion claim must rest on a concept-wide grep, not the known divergent values). Here it worked: it surfaced the two P-256 dev-guidance carriers and the CA citation-section error before push. Both routings (FR-205, the P-256 tables) are genuine forks surfaced for maintainer decision rather than guessed, per the GRC-not-solutioning and route-genuine-forks directives.

## 2026-07-14, Library Version 2026.07.392, PR #904

FR-201 (deep-assessment r3 fitness High): resolved the divergent vulnerability-remediation SLAs. The finding: normative docs set different remediation deadlines for the same CVSS bands (SCA standard High 30 / Medium 90 / Low 180 days; the vulnerability-management procedure High 14 / Medium 30 / Low 90; developer-security requirements High 14). Fix: designate [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md) section 2 the SINGLE SOURCE OF TRUTH (Critical 24h/72h/7d by exploitation status, High 14, Medium 30, Low 90 days) and convert the divergent restatements to citations. (Note: the SoT band is High/Medium/Low = 14/30/90; the Critical tier is exploitation-graded, correcting the "Crit/High/Med" shorthand used when the decision was first framed.)

### Changed

- [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) section 4.2: removed the divergent SLA table (High 30 / Medium 90 / Low 180) and deferred remediation timelines to the vuln-management procedure section 2, retaining the SCA-specific severity-to-escalation table; the two mean-time-to-remediate KPIs aligned to the SoT's own programme metrics (Critical 5 days, High 12 days), replacing the earlier looser 7/30-day values.
- [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md): the SCA-scan row cites the vuln-management procedure section 2 SLAs instead of restating "14 days".
- [`dev-security/standard-security-quick-reference.md`](../../dev-security/standard-security-quick-reference.md) section 9: values kept for quick lookup (already matched the SoT), with an added citation designating the vuln-management procedure section 2 authoritative and governing on any discrepancy.
- Versions: SCA 1.1.5 to 1.1.6, developer-security-requirements 1.1.7 to 1.1.8, quick-reference 1.1.8 to 1.1.9; taxonomy/scorecard regenerated.

### Verification

- Substantive-tier skeptical verifier (refute-briefed, with a corpus-wide find-every-carrier pass): VERDICT SHIP. The find-every-carrier pass confirmed NO remaining divergent vuln-remediation-SLA carrier corpus-wide (production-security-requirements + patch-management restate the table but MATCH the SoT; policy-secure-development, devops-security-requirements, and pack files all consistent; the different-semantic values [SBOM-provision 30d, pentest-finding remediation, exception-max-duration windows, EOL runtime windows, supplier contractual minimums] correctly untouched). Two in-window completions from the verifier's notes: the MTTR-metric alignment (SCA MTTR set to the SoT's OWN metrics 5/12, not the SLA deadlines 7/14, verified against the held source before applying) and the ops-doc single-source follow-up routed to TODO section 3.68.
- All 69 gates pass. Batches PR #903's `/validate-pr` (0 in-window findings) + `/retro`.

### Discipline observation

The verifier's find-every-carrier pass is the FR-201 analogue of the DA-DORA-A12 lesson: the finding named 3 docs, but the real divergence was one (SCA); dev-requirements and quick-reference already matched the SoT, and two ops docs restate-but-match (drift risk, routed to section 3.68). The MTTR-metric note (my first fix tied SCA's mean-time metric to the SLA deadline rather than the SoT's own tighter metric) was caught by the verifier and corrected in-window: a single-source reconciliation must align a metric to the source's metric, not to the adjacent SLA. The SLA-value shorthand correction (High/Med/Low = 14/30/90, not Crit/High/Med) is recorded so the audit trail carries the accurate band.

## 2026-07-14, Library Version 2026.07.391, PR #903

FR-200 (deep-assessment r3 fitness High): reconciled [`compliance/standard-internal-audit.md`](../../compliance/standard-internal-audit.md)'s reporting/independence structure to the corpus's canonical governance. The finding: the standard's section-2.3 independence named only the Enterprise Risk Committee (ERC) as the CAE's reporting/escalation line, with no functional line to the board or audit committee, contradicting the compliance policy (which already requires internal audit to "report directly to the Board Audit Committee", [`policy-compliance-and-audit-management.md`](../../compliance/policy-compliance-and-audit-management.md) section 4.3.1) and the assurance map ([`risk/register-assurance-map.md`](../../risk/register-assurance-map.md), which assumes a board/audit-committee).

### Changed

- Section 2.3(b) Structural independence: the CAE/GRC Manager now reports functionally to the Board Audit Committee (with the no-separate-committee consolidation fallback per the minimum-viable-governance guideline) and administratively to senior leadership, per policy section 4.3.1; the ERC escalation for operational risk matters is retained.
- Section 2.1: added a functional-reporting bullet (Annual Audit Plan + significant findings to the Board Audit Committee), labelled distinct from the ERC operational-status line.
- Section 4.1: the Annual Audit Plan is now reviewed by the ERC and approved by the Board Audit Committee (per policy section 4.2.1), completing the reconciliation.
- Section 7.1: critical-finding escalation now routes to the ERC and the Board Audit Committee within 2 business days (per policy section 4.6.2).
- Version 1.1.0 to 1.2.0, Date 2026-07-14; taxonomy/scorecard regenerated.

### Verification

- Substantive-tier skeptical verifier (refute-briefed): VERDICT SHIP on the core section-2.1/section-2.3 change (cited source policy section 4.3.1 matches verbatim, both cross-references resolve, the IIA functional/administrative split is correct and not swapped, no new contradiction). It flagged the section-4.1 plan-approval and section-7.1/6.8 escalation surfaces as pre-existing ERC-only (out of the minimal FR-200 scope). The orchestrator completed the section-4.1 + section-7.1 reconciliation IN-WINDOW (reconcile-to-canonical against the verifier-confirmed policy section 4.2.1/4.6.2) rather than ship the standard with a new internal inconsistency (the new section-2.3 Board-Audit-Committee functional line vs section-4.1 ERC-approves-the-plan), per the find-every-carrier discipline. Section-6.8 full-report distribution to the ERC is left as-is (adequately covered by section-2.1's significant-findings-to-Board-Audit-Committee summary line).
- All 69 gates pass (pre-push guard). Batches PR #902's `/validate-pr` (0 findings; the DA-ASVS high-assurance harness held through merge) + `/retro` rows.

### Discipline observation

The verifier SHIP'd the minimal change but flagged the partial reconciliation; completing it in-window (rather than only routing a follow-up TODO) avoids the DA-DORA-A12 carrier-incomplete pattern (a finding fixed at the cited surface while sibling carriers keep the old value). The reconciliation targets the corpus's own canonical values (policy section 4.2.1/4.6.2), so it is reconcile-to-canonical, not a new authorial choice, which is why it was safe to complete unattended.

## 2026-07-14, Library Version 2026.07.390, PR #902

The DA-ASVS remap (deep-assessment r3 Phase-5 High finding): corrected the OWASP ASVS cross-references across the dev-security domain and the rules pack from the superseded 4.0.3 chapter/sub-requirement numbering to the current 5.0.0 scheme. ASVS 5.0.0 (30 May 2025, current stable, reconfirmed upstream this session) fully reorganized the chapters, so every 4.0.3 chapter number pointed at the wrong 5.0.0 chapter. Applied under the high-assurance verification harness (registered in [`.working/high-assurance/register.md`](../high-assurance/register.md)).

### Changed

- Corpus dev-security docs: [`standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md) section-19 framework-alignment table + inline (Secure SDLC V1 to V15, Authentication V2 to V6, Secrets V3 to V13, Input validation V5 to "V2, V1", Cryptography V6 to V11, Error/logging V7 to V16, Dependency management V3 to V15, API security "V3, V13" to V4); [`standard-security-baseline-and-standards-reference.md`](../../dev-security/standard-security-baseline-and-standards-reference.md) section-12 table (the 5th carrier the r3 finding did not name: Data classification V9 to V14, Identity+access "V2, V4" to "V6, V8", Network security V9 to V12, Logging V7 to V16, Cryptography V6 to V11); [`procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md) (V1 Architecture to V15, V14 Configuration to V13). Each Version+Date co-bumped; taxonomy/scorecard regenerated.
- Rules pack ([`dev-security/claude-rules/`](../../dev-security/claude-rules/) + the [`.claude/rules/`](../../.claude/rules/) mirrors for input-validation/secrets/python): core/owasp.md quick-reference table (V2/V3/V5/V6/V9/V13 to V6/V7/V2/V11/V12/V4), core/input-validation.md (SQLi V5.3 to V1.2.4, command-injection to V1.2.5, output-encoding to V1.1/V1.2.1, file-upload V12 to V5.2), core/secrets.md (V2.10 to V13.3.x), core/cryptography.md (algorithm V6.2 to V11.3, key-management V6.4 to V13.3, password-hashing V2.4 to V11.4.2, TLS V9 to V12, RNG V6.3 to V11.5), core/authentication.md (MFA V2.1 to V6.5, session V3 to V7, service-auth V2.10 to V13.3, directory V2.8 to V6.8, brute-force V2.2 to V6.3), languages/java.md + go.md + csharp.md + typescript.md + python.md. Pack README 1.61.5 to 1.61.6 + version-history row.

### Deferred

- Class 2: the roughly-40 generic V1.1/V14.1/V14.2 ASVS citations in the 9 governance rules (dual-tree) + 3 SKILL.md + threat-modelling are generic PROCESS alignments with no clean 5.0.0 home; deferred to a maintainer-decided pass (TODO section 3.66). The maintainer expanded scope mid-harness to include the pack + the sub-req level, then, on the sub-req research revealing the governance-generic shape, re-scoped Class 2 out to avoid fabricating precision.

### Verification

- High-assurance harness (5 stages, per the register): upstream currency reconfirmed (ASVS 5.0.0 current, WebSearch); 2 research workers (chapter + sub-req); 2 independent adversarial verifiers (false-negative miss-hunt + false-positive over-assignment) which CONVERGED 0-missed-carriers-corpus-wide / 0-wrong-targets (MASVS correctly excluded as a distinct standard; meaning-shift traps re-homed correctly against the held 5.0.0 source: TLS V9 to V12, crypto V6 to V11, secrets V2.10 to V13.3, session V3 to V7, file-upload V12 to V5.2, XXE to V1.5.1, path-traversal to V5.3.2, dependency to V15.2); the 4 flagged low-confidence cells resolved to defensible primaries (key-management V13.3 not V11.6, brute-force V6.3 not V2.4, service-auth V13.3, directory V6.8). Deterministic scripted apply keyed on explicit cell strings (69 mappings, dry-run each exactly-1-match, applied 69/69, re-parse 0 residual; NO blanket token sweep, so the pack README frozen version-history rows are untouched). Invariant floor: all 69 gates pass (gate 37 mirror-sync + gate 35 parity included).
- Batches PR #901's `/validate-pr` (2 notes, both `.working/`-scope: F1 the #900 State-snapshot partial-reconcile FIXED in the #901-checkpoint commit on this branch, F2 the D7 two-line-layout no-op = already-tracked section 3.22) + `/retro` (the handoff-no-row miss WATCH from #822 fired at #900/#901, 3rd occurrence, graduated to the proposed handoff-self-row D-check) rows.

### Discipline observation

The maintainer's mid-harness scope expansion (include pack + sub-req) then re-scope (defer the governance-generic Class 2) is `surface-counterproductive-instructions` working in both directions: the sub-req research surfaced that roughly-40 governance citations had no clean 5.0.0 home, I surfaced that rather than fabricate precision, and the maintainer re-scoped. The maintainer's steer "this is GRC documentation, not a technical solution" (dropping the proposed FR-202 TLS proxy compensating-control note) is recorded as a standing preference in memory. The deterministic-apply-plus-re-parse made the 69-cell apply's correctness independent of orchestrator in-context precision across a large multi-file edit, which is the point of the high-assurance apply stage.

## 2026-07-14, Library Version 2026.07.389, PR #901

The first PR of the 2026-07-14 resumed session (`claude/resume-sweep102-validate`, resumed from #900): the mandatory loop-break corpus-wide `/validate` (Sweep 102) over the #887..#900 deltas of the 2026-07-13 deep-assessment r3 session, the compensating control for session-closing handoff PR #900 (which skipped its trailing `/validate-pr` + `/retro`). Subagents clean (0 error / 0 warning / 0 escalate-class); the close-out mechanical re-baseline then caught one in-window bookkeeping omission (PR #900's handoff-exemption row was missing), fixed here. The loop-break control for #900 PASSES.

### Fixed

- [`.working/validate-pr/history.md`](../validate-pr/history.md): added the **PR #900 handoff-exemption row** (`SKIPPED (handoff-PR exception)` in the Findings cell). #900 (the prior session's session-closing handoff) omitted its own exemption row (the recurring handoff-no-row miss, same shape as #821->#822): while #900 was the highest-numbered merged PR gate 50 exempted it as in-flight, and the omission surfaced the moment this PR's CHANGELOG entry demoted it, failing gate 50 (bookkeeping-parity) and, downstream, the gate-36 `test_runs_clean_on_corpus_at_head` regression smoke test in this PR's pre-push guard. Adding the row resolves both. This is the loop-break compensating control working: the semantic subagents were clean, and the close-out mechanical re-baseline caught the prior handoff's bookkeeping omission.

### Changed

- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the Sweep 102 iter-1 row (subagents 0/0/0 + the 1 mechanical handoff-row finding fixed this PR; Version 2.0.97 to 2.0.98). Three subagents A/B/C dispatched; all clean.
- [`.working/session-handoff.md`](../session-handoff.md): Resume cursor advanced to Sweep 102 (Sweep 101 demoted to prior); the #900 State-snapshot green-at annotated with the resume state; PRUNED per keep-current-plus-one-prior (the #851 session's Next-actions, State-snapshot, and Asserted-expectations blocks deleted; the #886 block's dangling supersede-pointer neutralized to "pruned at the Sweep 102 resume").
- [`.working/session-state.md`](../session-state.md): lease ACQUIRED (`Active-session: claude/resume-sweep102-validate`, `Status: active`, fresh heartbeat).
- [`.working/pending-decisions.md`](../pending-decisions.md): the 2026-07-14 resume-round decisions banked (mode unattended/overnight; the r3 High remediation dispositions FR-200/201/202-205 and DA-ASVS Secrets->V13; the machinery decisions G1/G3/G5/gate-25; DA-ISO20000 deferred pending purchase; overnight scope).
- [`.working/next-prs.txt`](../next-prs.txt): cycled forward (the completed handoff dropped; DA-ASVS now leads the queue).
- README Library Version 2026.07.388 to 2026.07.389; README Version 1.9.749 to 1.9.750.

### Verification

- Sweep 102: mechanical baseline 69/69 at `95a2772`/#900 (verified this resume, non-shallow clone). Pre-flight scanner: 421 files, 11 candidates all the collection-count-word false-positive class, dismissed by all three subagents. Subagent A (recent-PR) verified all 9 #899/#900 corpus edits at source (the DORA Article 11/12 split corroborated against held DORA text, EU AI Act Article 26/53/55/Annex XI, EDPB 05/2020 date precision, FFIEC CAT retirement) with Version+Date co-bumps and generated artefacts in sync; Subagent B (stale-reference) confirmed the DA-DORA-A12 and DA-AIACT-A26 corpus residuals both 0 and no count drift (13/23/14 and gate 69 re-derived); Subagent C (audit-programme) confirmed four-surface parity at gate 69, gate-count consistency, the #890 dual-header drift-cluster complete across docstrings/spec/code, the #897 nightly-sweep full-SHA pin, and the regression suite 373 OK. Asserted-expectations cross-check: all CORROBORATED, 0 contradicted.
- The r3 HIGH findings (DA-ASVS, FR-200/201, FR-202..205, remaining mediums/lows) are known-open per the #900 handoff and NOT asserted clean, so out-of-scope for this sweep as expected.
- The first pre-push guard run flagged gate 50 (bookkeeping-parity) and, downstream, the gate-36 `test_runs_clean_on_corpus_at_head` smoke test, both from the missing #900 handoff-exemption row (the Fixed section above); after adding the row the re-run passes all 69 gates standalone. Both generator `--check`s in sync (no per-document body change this PR, working-state and version surfaces only). Subagent C's earlier standalone regression run reported 373 OK because it ran before #901's CHANGELOG entry demoted #900 from highest-numbered, so gate 50 still exempted #900 as in-flight at that time.

### Discipline observation

This is the loop-break compensating control for #900: the session-closing handoff PR skipped its own `/validate-pr` + `/retro`, and this corpus-wide `/validate` re-examines the whole delta window rather than only #900's diff, cross-checking against the handoff's asserted-expectations. The one scope note (Subagent A found the AICPA TSP 100 register row was added out-of-window at #876, not this delta) is a brief-scoping correction, not a corpus defect; the RB-6(e) AICPA held-edition item remains separately tracked from Sweep 101. Per recursion-avoidance this Sweep 102 close-out is the first PR of the resumed session and also acquires the lease and prunes the handoff.

## 2026-07-14, Library Version 2026.07.388, PR #900

The session-closing handoff for the 2026-07-13 resumed session (`claude/resume-sweep101-validate` + the deep-assessment r3 branches, #887-#900), the corpus-wide completion of the DA-DORA-A12 fix that PR #899's `/validate-pr` found carrier-incomplete, and PR #899's batched QA. Per the loop-break, this session-closing handoff PR takes NO trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 102) over #887..#900.

### Changed

- [`resilience/plan-pandemic-continuity.md`](../../resilience/plan-pandemic-continuity.md) (line 180) + [`resilience/plan-physical-site-continuity.md`](../../resilience/plan-physical-site-continuity.md) (line 198): the "Article 12 ICT business continuity policy" DORA mislabel corrected to "Article 11 ICT business continuity policy" (Art 11 is the business-continuity-policy home and fits these continuity-plan crosswalk rows; Art 12 is backup/restoration/recovery). Completes DA-DORA-A12 corpus-wide (3 carriers; #899 fixed the recovery-runbook carrier to Art 12, this PR fixes the two continuity-plan carriers to Art 11), after #899's `/validate-pr` caught the fix as carrier-incomplete (the find-every-carrier scope-width miss). Corpus-wide grep: 0 residual mislabel. Versions: pandemic-continuity 1.0.6 to 1.0.7, physical-site-continuity 1.0.3 to 1.0.4; taxonomy/portal/scorecard regenerated.
- [`.working/session-handoff.md`](../session-handoff.md): prepended this session's Next-actions, State-snapshot, and Asserted-expectations blocks (the r3 sign-off, the mechanical-batch remediation, the Highs routed to a fresh session, and the DORA corpus-wide completion); the Asserted-expectations block scopes the known-open r3 Highs as NOT-asserted-clean so the Sweep-102 cross-check does not misread them as misses.
- [`.working/session-state.md`](../session-state.md): lease RELEASED (`Status: released`, `Active-session: none`). [`.working/session-metrics.md`](../session-metrics.md): this session's row (measured-where-clean, not-fabricated where a running tally was not armed). [`TODO.md`](../../TODO.md) §3.64: the DA-DORA-A12 note completed to the 3-carrier corpus-wide resolution.
- README Library Version 2026.07.387 to 2026.07.388; README Version 1.9.748 to 1.9.749.

### Verification

- All 69 audit gates pass standalone (pre-push guard); both generator `--check`s in sync after the two continuity-plan Version bumps. The DA-DORA-A12 corpus-wide grep for "Article 12 ICT business continuity" returns 0 residual.
- The two continuity-plan carriers were verified in context before relabeling (both are business-continuity crosswalk tables alongside "NIS 2 Article 21(2)(c) Business continuity", so Art 11 is the correct DORA reference, matching the recovery-runbook's Art-12 choice for the recovery context).
- PR #899's `/validate-pr` returned 1 in-window warning (the DA-DORA-A12 carrier-incompleteness), fixed here; its other checks passed (the six fixes accurate, generators in sync, backlog reconciled, #898 QA present).

### Discipline observation

The DA-DORA-A12 carrier-incompleteness is the find-every-carrier / bare-token-width scope-width miss (a named close-out-checklist class): #899 fixed the one cited line and declared the finding resolved WITHOUT the corpus-wide bare-token grep the checklist requires; the per-PR `/validate-pr`'s corpus-wide grep caught it, and #900 completes it. Logged in the #899 retro as the reinforced habit (a mislabel/token correction is not "resolved" until a corpus-wide grep of the old form returns zero). This is the session-closing handoff: the deep-assessment r3 is SIGNED OFF, the clear-mechanical batch remediated, and the Highs (DA-ASVS high-assurance + FR-200/FR-201) handed to a fresh session; PR #900's own QA is intentionally absent per the loop-break, with Sweep 102 as the compensating control.

## 2026-07-13, Library Version 2026.07.387, PR #899

The maintainer-signed-off `/deep-assessment` r3 clear-mechanical remediation batch (six findings), the r3 sign-off record, and PR #898's batched QA. The maintainer signed off on the r3 finding set via `AskUserQuestion` ("Sign off; mechanical now, Highs fresh") and directed the clear-mechanical batch this session; the DA-ASVS High + the FR-200 / FR-201 Highs were routed to a fresh session.

### Changed

- [`README.md`](../../README.md) (two audience enumerations) + [`tools/build-portal.py`](../../tools/build-portal.py) (the module docstring + the emitted portal-overview string): added the Board / CEO audience (second, after CIO, matching the AUDIENCES order) so the enumerations match the portal the generator already produces (FR-207). Regenerated [`docs/portal.md`](../../docs/portal.md) accordingly.
- [`docs/template-implementation-roadmap.md`](../../docs/template-implementation-roadmap.md) (lines 77, 260, 273): three "quickstart(-template) composition" carriers corrected to "startup-roadmap composition", matching the authoritative step 1 (the 24-module catalogue lives in the startup roadmap, not the quickstart) (FR-209). Version 1.0.7 to 1.0.8.
- [`privacy/jurisdictions/annex-privacy-mexico.md`](../../privacy/jurisdictions/annex-privacy-mexico.md): dropped the stale "documents that still name INAI ... reconciled separately" clause (the only other INAI reference is already on the 2025 regime), keeping the forward-looking "this annex governs on divergence" rule (FR-213). Version 0.0.1 to 0.0.2.
- [`compliance/financial-services/annex-financial-services-sector-requirements.md`](../../compliance/financial-services/annex-financial-services-sector-requirements.md) (line 75): the FFIEC Cybersecurity Assessment Tool row now marks it retired 31 August 2025 and notes the FFIEC suggests institutions may consider industry-developed resources such as the Cyber Risk Institute Cyber Profile and the CIS Critical Security Controls (verified against ffiec.gov this session; the FFIEC's language is the non-binding "may consider", not a directive) (RB-FFIEC-CAT). Version 1.0.9 to 1.0.10.
- [`resilience/template-recovery-runbook.md`](../../resilience/template-recovery-runbook.md) (line 173): the DORA row label corrected from "Article 12 ICT business continuity policy" to "Article 12 backup, restoration, and recovery procedures" (Art 12's real subject; the business-continuity policy is Art 11) (DA-DORA-A12). Version 1.0.4 to 1.0.5.
- [`ai/standard-ai-inference-cost-governance.md`](../../ai/standard-ai-inference-cost-governance.md) (line 213): the EU AI Act row Article-26 parenthetical corrected from "deployer obligations including efficient use" to "deployer obligations", and the GPAI reference to "Articles 53, 55 (GPAI provider obligations, including the Annex XI technical documentation)" (the verified home of the GPAI documentation duties) (DA-AIACT-A26). Version 0.0.6 to 0.0.7.
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated (taxonomy first, then portal + scorecard) for the five per-document Version bumps and the FR-207 portal-overview prose change.
- [`.working/deep-assessment/register.md`](register.md): r3 row Status to `signed-off`, P8 to complete, with the maintainer sign-off recorded. [`.working/fitness-reviews/history.md`](../fitness-reviews/history.md): FR-207/209/213 to `closed` (#899). [`TODO.md`](../../TODO.md) §3.63/§3.64: RB-FFIEC-CAT, DA-DORA-A12, DA-AIACT-A26 annotated RESOLVED #899. [`.working/DONE.md`](../DONE.md): PR #899 entry.
- README Library Version 2026.07.386 to 2026.07.387; README Version 1.9.747 to 1.9.748.

### Verification

- **Each fix verified at source before applying** (apply-time discipline). The one precision claim considered for addition (an "energy-consumption" locator on the AI Act GPAI row) was NOT shipped because the exact wording could not be grep-confirmed in the held AI Act; the shipped reference is "Annex XI technical documentation", which IS verified in the held text (the GPAI providers' Annex XI technical-documentation duty under Article 53). The other five fixes are prose/label/enumeration corrections against already-verified findings.
- All 69 audit gates pass standalone (pre-push guard). Both generator `--check`s exit 0 after the regeneration (taxonomy first, then portal + scorecard). Five per-document Version+Date co-bumps present (D2/D4). A pre-push skeptical verifier subagent reviewed the whole diff (refute-briefed).
- Each finding's backlog row was updated to reflect the fix; the DA-ASVS High + FR-200/FR-201 Highs remain open and routed to a fresh session.

### Discipline observation

This is the post-sign-off remediation of the r3 assessment: the maintainer signed off and directed the ordering, and only the clear-mechanical subset was applied this session (the High / high-assurance / authorial-decision items were deferred to a fresh session per the sign-off). The one apply-time restraint worth noting: a tempting precision addition (the AI Act energy-consumption locator) was pared back to the grep-verifiable "Annex XI technical documentation" rather than shipped on the subagent's characterization, keeping the remediation itself to the evidence-grounded standard the assessment enforces. PR #899's own `/validate-pr` + `/retro` ride the next PR (the session-closing handoff).

## 2026-07-13, Library Version 2026.07.386, PR #898

The `/deep-assessment` r3 Phase 7 (routing consolidation) and Phase 8 (presentation for maintainer sign-off), plus PR #897's batched QA. **Phases 1 to 7 of r3 are COMPLETE; the run is at Phase 8, HOLDING for explicit maintainer sign-off.**

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](2026-07-13-r3.md): Phase 7 header PENDING to COMPLETE with the full consolidated finding set (a sign-off-ready summary: fitness FR-200 to FR-219, reference-audit §3.63, guardrails §3.62, Phase-4/5 §3.64, the clean closures, and a recommended remediation ordering); Phase 8 restated as HOLD-for-sign-off (presented, not self-closed).
- [`.working/deep-assessment/register.md`](register.md): r3 row P7 to complete (P1-P7 complete, P8 pending, HOLDS for sign-off); the narrative UPDATE clause reconciled to "through #898" (Phase 6 + 7 complete), fixing the paired-surface status lag PR #897's `/validate-pr` flagged.
- README Library Version 2026.07.385 to 2026.07.386; README Version 1.9.746 to 1.9.747.

### Verification

- No corpus document body changed; no new subagents dispatched (Phase 7 consolidates already-verified, already-routed findings; Phase 8 presents). All 69 audit gates pass standalone (pre-push guard).
- The consolidated finding set restates only findings already apply-time-verified and routed in prior r3 PRs (#888-#897); no new claim is introduced. The one in-window fix this PR (the register UPDATE-clause reconcile) was verified against the register row + the dated file (all three now agree: Phases 1-7 complete, Phase 8 holds).
- PR #897's `/validate-pr` returned 1 in-window note (the register narrative-phase lag), fixed here; its other seven checks passed (F-1 SHA-pin byte-exact vs the main quality workflow, CHANGELOG parity, version chain, hallucination-metrics framing, #896 QA rows).

### Discipline observation

Phase 8 is the discipline's terminal gate: the run HOLDS for explicit maintainer sign-off and does NOT self-close, even though the remaining substantive findings are the deep-assessment's whole purpose. The consolidated set is presented in chat via a structured sign-off request; no r3 remediation (the DA-ASVS high-assurance remap, the FR-200..219 fixes) begins until the maintainer signs off and directs the ordering. The paired-surface status-lag caught by #897's `/validate-pr` (register row advanced without its narrative clause) is the recurring named class, logged in the #897 retro with the register-specific reconcile habit; the mechanical backstop (the per-PR `/validate-pr`) caught it, as designed. PR #898's own `/validate-pr` + `/retro` ride the first post-sign-off remediation PR (there is no next substantive PR until the maintainer breaks the hold, the same in-flight tail as any pause point).

## 2026-07-13, Library Version 2026.07.385, PR #897

The `/deep-assessment` r3 Phase 6 (adoptability, pipeline integrity, QA-ledger meta-audit), COMPLETE; its one Low finding (F-1) fixed in-window; and PR #896's batched QA. Phases 1 to 6 of r3 are now COMPLETE.

### Security

- [`.github/workflows/nightly-sweep.yml`](../../.github/workflows/nightly-sweep.yml): SHA-pinned `actions/checkout` (`34e114876b0b11c390a56381ad16ebd13914f8d5` # v4) and `actions/setup-python` (`a26af69be951a213d495a4c3e4e4022e16d87065` # v5), matching the main quality workflow, resolving Phase-6 finding F-1 (the workflow tag-pinned these two actions while the main workflow SHA-pins them, a self-inconsistency against the repo's own strict SHA-pin rule). Same versions, pinned by commit; behaviour-preserving, security-positive. Low severity (read-only token, no secrets, `permissions: {}`).

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](2026-07-13-r3.md): Phase 6 header PENDING to COMPLETE with the full result (pipeline integrity, QA-ledger meta-audit, adoptability). [`.working/deep-assessment/register.md`](register.md): r3 row P6 to complete (Phases 1-6 complete; Phase 7 next).
- [`.working/hallucination-metrics.md`](../hallucination-metrics.md): refreshed the Current-state header + a #887-#896 session-window summary (the r3 Phase-6 meta-audit flagged it at its opportunistic-update threshold); worker-draft class unmoved, orchestrator-side zero shipped escapes this session.
- README Library Version 2026.07.384 to 2026.07.385; README Version 1.9.745 to 1.9.746.

### Verification

- **Phase 6 (2 subagents + inline platform checks):** pipeline-integrity subagent found 1 Low (F-1, fixed here) + 0 critical: the main quality workflow hardening sound (SHA-pinned actions, `contents: read`, `pull_request` not `pull_request_target`, safe env-var handling of the one `github.event.*` use), full-history secret/PII scan CLEAN across 1123 commits (every hit a documented example / linter fixture / canonical placeholder / the maintainer's published-and-allowlisted contact), guard/hook chain fail-loud (RM-10 fail-closed, pipe-guard self-test 14 blocked / 17 allowed), `.gitattributes` export-ignore correct. Branch protection verified inline via `gh api`: the active "Main Protection" ruleset enforces pull-request (1 approval), the `Lint markdown corpus` required check, required signatures, and deletion protection. QA-ledger meta-audit subagent: the QA record is HONEST (every merged PR #880-#895 has a formal `/validate-pr` + `/retro` row, #886 handoff-exempt correctly marked in the Findings cell, zero sham markers in-window, zero uncaught shipped escape, registers consistent). Adoptability: the bare-clone on-ramp resolves end-to-end (0 dead links across README / portal-273 / quickstart-13 / decision-tree-89 / adopter-guide-40).
- All 69 audit gates pass standalone (pre-push guard). The only corpus-visible change is the workflow SHA-pin (F-1); no corpus document body changed. The nightly-sweep workflow runs only on schedule/dispatch, so it is not exercised by this PR's CI.

### Discipline observation

Phase 6 completes r3's evidence-gathering: Phases 1 to 6 done, with the finding set consolidated for Phase 7 routing and Phase 8 sign-off. The QA-ledger meta-audit is the honest-backstop step (it audits whether the QA record itself is genuine, not just whether the corpus is clean) and returned HONEST, including the transparently-retained far-out-of-window Sweep-22 abbreviation incident as an integrity-positive. F-1 is the only Phase-6 fix and is clear-mechanical; every substantive r3 finding (DA-ASVS, the fitness contradictions, the reference-audit items) remains HELD for maintainer sign-off. Next: Phase 7 (consolidate and route the whole r3 finding set) and Phase 8 (present for sign-off; the only terminal state).

## 2026-07-13, Library Version 2026.07.384, PR #896

The `/deep-assessment` r3 Phase 4 (dead-gate/coverage deep pass, COMPLETE) and Phase 5 (ground-truth citation sampling, COMPLETE), their routed findings, and PR #895's batched QA.

### Added

- TODO §3.64 [`TODO.md`](../../TODO.md) routing the Phase-4/5 findings (HOLD for r3 Phase-8 sign-off): DA-ASVS (High, high-assurance-class), DA-DORA-A12 (Medium), DA-AIACT-A26 (Low), DA-ISO20000 (Low, reference-acquisition), DA-gate25-scaffold (Low, re-scope machinery).
- A DA-ASVS row in [`.working/high-assurance/register.md`](../high-assurance/register.md) (status `pending`, Version 1.0.19 to 1.0.20): the ASVS 4.0.3-to-5.0.0 chapter remap is a sensitive change (gate-blind, multi-document, adopter-consumed) warranting the full harness, with the verified 5.0.0 chapter map and the one unresolved Secrets-management chapter call recorded.

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](2026-07-13-r3.md): Phase 4 header SUBSTANTIALLY-COMPLETE to COMPLETE with the dead-gate result; Phase 5 header PENDING to COMPLETE with the 20-citation sample result and the three verified discrepancies.
- README Library Version 2026.07.383 to 2026.07.384; README Version 1.9.744 to 1.9.745.

### Verification

- **Phase 4 (dead-gate/coverage):** a subagent classified all 69 gates against their linter logic, exempt/scope sets, regression fixtures, and (for narrow-scope gates) a live standalone run. Zero genuinely-dead gates: 57 ACTIVE, 12 PREVENTIVE-WORKING, none empty-scope or subsumed. One Low re-scope observation (gate 25's three dormant P1/P2/P3 scaffold sub-patterns inside an otherwise-active gate), orchestrator-verified against the linter docstring and a standalone run ("1 tracked term(s); scanned 423 files").
- **Phase 5 (ground-truth sampling):** a fresh stratified 20-citation sample across 11 domains + 2 jurisdiction annexes, judged against held reference-base text; 16 FAITHFUL, 3 DISCREPANCY, 1 SOURCE-NOT-HELD, 0 CURRENCY-UNCONFIRMED. All three discrepancies orchestrator-verified at source before routing: DA-ASVS verified against the held OWASP ASVS 5.0.0 chapter list (which states "V1 Architecture chapter has been removed", confirming the 4.0.3-to-5.0.0 renumber); DA-DORA-A12 verified against the held DORA (the ICT business continuity policy is "referred to in Article 11", Article 12 is backup/restoration); DA-AIACT-A26 verified against the held AI Act (Article 26 is deployer obligations, no efficiency clause).
- All 69 audit gates pass standalone (pre-push guard). No corpus document body changed (this PR is the deep-assessment record + routing + #895 QA).

### Discipline observation

Phase 5 is the pass that justifies the whole deep-assessment: on a corpus that passes all 69 gates and that three prior citation passes this session (Sweep 101, `/claim-fit`, `/full-qa`) found clean, a fresh stratified ground-truth sample still surfaced a systematic version-mismatch (DA-ASVS) that every gate is blind to. The finding is the demonstrated-weakest-dimension class (citation-attribution / version currency) and is correctly routed to the high-assurance harness rather than a mid-assessment quick edit, because the remap is delicate (one control area has no clean 5.0.0 chapter) and multi-document. r3 Phases 1 to 5 are now COMPLETE; Phase 6 (adoptability, pipeline integrity, ledgers) is next, then Phase 7 routing and Phase 8 sign-off (HELD).

## 2026-07-13, Library Version 2026.07.383, PR #895

The `/deep-assessment` r3 Phase-3 final semantic instrument, `/reference-audit` FULL both-directions, its two routed findings, and PR #894's batched QA. Phase 3 of r3 is now COMPLETE.

### Added

- Reference-breadth run record [`.working/reference-audit/2026-07-13-full.md`](../reference-audit/2026-07-13-full.md) (FULL both-directions, deep-assessment r3 Phase-3): 588 in-scope reference items / 405 corpus docs (210 well-cited, 111 thin, 161 uncited, 106 no-key); deliberate high-value authoritative-tier sample across four judges (AI-security, financial-services, assurance/SOC, threat-modeling+new-ingest), sample stated. History row added to [`.working/reference-audit/history.md`](../reference-audit/history.md) (first recorded `/reference-audit` run; Version 1.0.0 to 1.0.1).
- TODO §3.63 [`TODO.md`](../../TODO.md) routing the two findings (HOLD for r3 Phase-8 sign-off): RB-ETSI-104128 (Low, held-but-unused) and RB-FFIEC-CAT (Medium, currency).

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](2026-07-13-r3.md): `/reference-audit` marked COMPLETE with the routed-finding summary; Phase 3 header changed IN PROGRESS to COMPLETE (all eight semantic instruments run).
- README Library Version 2026.07.382 to 2026.07.383; README Version 1.9.743 to 1.9.744.

### Verification

- All 69 audit gates pass standalone (pre-push guard). No corpus document body changed (this PR is the reference-audit record + routing + #894 QA); no generated-artefact regen needed.
- **Findings apply-time-verified before routing.** ETSI TR 104 128 confirmed held in the grc_library_ref catalogue and the target [`ai/guide-ai-security-technical-implementation.md`](../../ai/guide-ai-security-technical-implementation.md) (lines 625 to 627) confirmed to cite NIST but no ETSI. FFIEC CAT currency confirmed against the PRIMARY source (ffiec.gov, this turn): the FFIEC sunset the CAT on 31 Aug 2025, successors CRI Cyber Profile + CIS CSC; the corpus `annex-financial-services-sector-requirements.md:75` presents it as current. ISO 5259-5 confirmed already tracked at the live TODO §3.42 (deduped, not duplicated). RB-6(e) confirmed no-corpus-value-at-risk (the SOC judge enumerated every corpus AICPA-TSC citation at the edition-stable criteria/CC-group level).

### Discipline observation

`/reference-audit` FULL is the last of the r3 Phase-3 semantic instruments; Phase 3 is COMPLETE. The pass confirms the corpus reference-breadth is strong (2 genuine findings on a 588-item base, one of them a currency slip rather than a breadth gap). The RB-6(e) resolution is a clean closure of a question three prior passes (Sweep 101, `/claim-fit`, `/full-qa`) left open by finding the held-edition mismatch but not testing whether any attributed value depended on it. r3 Phase 8 remains HELD; next are the Phase-4 dead-gate/coverage deep pass and Phases 5-6.

## 2026-07-13, Library Version 2026.07.382, PR #894

The `/deep-assessment` r3 Phase-3 (and Phase-6 adoptability) `/fitness` fresh-reader persona pass, its finding set routed to the r3 finding set (HOLD for maintainer sign-off), the in-window fix of the status-lag warning PR #893's `/validate-pr` raised, and PR #893's batched QA.

### Added

- Fitness review report [`.working/fitness-reviews/2026-07-13-r1.md`](../fitness-reviews/2026-07-13-r1.md): ten personas (P1 to P10), whole corpus, maintainer mental model stripped. 20 findings routed FR-200 to FR-219 (2 High, 9 Medium, 9 Low) plus 4 FYI recorded, all Pass-1 orchestrator-verified at source, none fixed in-window (the value contradictions are authorial), HOLD for maintainer sign-off at r3 Phase 8. The 20 open-backlog rows added to [`.working/fitness-reviews/history.md`](../fitness-reviews/history.md) with a history row.
- PR #893 per-PR validation record [`.working/validate-pr/2026-07-13-PR-893.md`](../validate-pr/2026-07-13-PR-893.md) and its history row; PR #893 `/retro` row in [`.working/improvement-log.md`](../improvement-log.md).

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](2026-07-13-r3.md) `/fitness` marked COMPLETE with the routed finding summary; the Phase-3 PENDING enumeration reworded to drop `/full-qa` and `/fitness` (both now complete), leaving only `/reference-audit` plus the ledger aids (the fix of PR #893's `/validate-pr` status-lag warning).
- README Library Version 2026.07.381 to 2026.07.382; README Version 1.9.742 to 1.9.743.

### Verification

- All 69 audit gates pass standalone (pre-push guard: `run_all_audits.sh` plus `run-pr-time-checks.sh` D1 to D7). No corpus document body changed; no generated-artefact regen needed (this PR is bookkeeping plus the fitness report).
- Every routed finding re-read at its cited `path:line` in the live corpus before routing (verdict tags in the report). Load-bearing dedup: FR-202 (TLS 1.2 in [`operations/procedure-media-handling-and-transport.md`](../../operations/procedure-media-handling-and-transport.md)) confirmed a fresh carrier of the closed FR-127 by `git blame` (the carrier is from the initial release 03ca390, predating the PR #193 FR-127 fix), so the FR-127 corpus-wide TLS reconciliation was carrier-incomplete.

### Discipline observation

The `/fitness` pass is a deep-assessment member (proactive, not a trust-recovery trigger). Its dominant finding class is gate-blind cross-document value drift: an operational or dedicated document restates an authoritative value that diverges (FR-201 to FR-205). The standardization recommendation (a single-source-of-truth convention for cross-document control values, and a bare-token corpus-wide grep at value-contradiction fix time) is recorded in the report for maintainer decision. r3 Phase 8 remains HELD; `/reference-audit` FULL is the last pending Phase-3 instrument.

## 2026-07-13, Library Version 2026.07.381, PR #893

The `/deep-assessment` r3 Phase-3 `/full-qa` forensic pass (six subagents), its one in-window citation-date fix, and PR #892's batched QA.

### Changed

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) + [`privacy/framework-consent-management.md`](../../privacy/framework-consent-management.md): the `/full-qa` Subagent-A finding fix. The EDPB Guidelines 05/2020 register row contradicted itself on the Version 1.1 date (current-version cell "adopted 4 May 2020" vs its own superseded cell + the held version-history table "13 May 2020"; 4 May 2020 is Version 1.0). Both surfaces reworded to the precise, version-history-grounded form ("adopted 4 May 2020 as Version 1.0; Version 1.1 formatting corrections 13 May 2020"). Register Version `1.5.35` to `1.5.36`; consent-management Version `1.0.8` to `1.0.9`; both Dates already 2026-07-13.
- [`taxonomy.yml`](../../taxonomy.yml) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the two Version bumps.
- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): Phase 3 `/full-qa` marked COMPLETE.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #892 row (0 findings); Version 1.2.659 to 1.2.660.
- [`.working/improvement-log.md`](../improvement-log.md): #892 `/retro` row; Version 1.0.598 to 1.0.599.
- [`README.md`](../../README.md): library CalVer 2026.07.380 to 2026.07.381; README Version 1.9.741 to 1.9.742.

### Added

- [`.working/full-qa/2026-07-13-iter1.md`](../full-qa/2026-07-13-iter1.md): the `/full-qa` per-run record (6 subagents A-F; 1 warning fixed in-window + notes).

### Verification

- **`/full-qa` (Phase-3, 6 subagents):** A (recent-PR deep review) surfaced 1 warning (the EDPB 05/2020 v1.1 date self-contradiction, in-window #867) FIXED here; B (stale-reference) 0 actionable across 5 classes; C (audit-programme) 0, four-surface parity 69 + counts + no-logic-weakened confirmed; D (citation forensic) 0 net-new (every §3.57 citation verbatim-corroborated against held sources; AICPA = known RB-6(e)); E (generated-artefact) 0, both generator `--check` exit 0; F (discipline) 0 R-findings, #887-#891 QA pairing complete, r3 Phase 8 held. C and F were re-dispatched after their first instances died on API connection errors (environment, not defect).
- The one finding was orchestrator-verified against the held version-history table before fixing; the fix is source-grounded (v1.1 = 13 May 2020 formatting corrections; v1.0 = 4 May 2020 adoption).
- Pre-push guard green (all 69 gates + D1-D7). This PR gets its own post-merge `/validate-pr` + `/retro`.

### Discipline observation

The `/full-qa` forensic pass earned its keep: five lenses confirmed the corpus and machinery sound, and the sixth (recent-PR deep review) caught a citation-precision date self-contradiction that all the per-PR sweeps and the earlier /claim-fit had waved through, because the held source's cover page and its version-history table disagree on the v1.1 date and the #867 apply copied the cover date. This is the exact gate-blind class the AI-failure-pattern forensic lens exists to catch, and it lands in this session's demonstrated-weakest dimension (citation-attribution), now clean after the fix.

## 2026-07-13, Library Version 2026.07.380, PR #892

The `/deep-assessment` r3 Phase-3 `/screen-publications` (satisfied no-op) and whole-matrix `/matrix-fit` passes, plus PR #891's batched QA. No corpus-document body changed.

### Changed

- [`.working/matrix-fit/history.md`](../matrix-fit/history.md): the whole-matrix `/matrix-fit` r3 run row (0 mismatches across 84 worklisted rows); Version 1.0.9 to 1.0.10.
- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): Phase 3 `/screen-publications` (no pending pubs) and `/matrix-fit` (0 mismatches) marked COMPLETE.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #891 row (0 findings); Version 1.2.658 to 1.2.659.
- [`.working/improvement-log.md`](../improvement-log.md): #891 `/retro` row (the row-append join-error 3rd-occurrence pattern, self-caught); Version 1.0.597 to 1.0.598.
- [`README.md`](../../README.md): library CalVer 2026.07.379 to 2026.07.380; README Version 1.9.740 to 1.9.741.

### Verification

- **`/screen-publications` (Phase-3):** the reference base's publications register has ZERO `pending` rows (all 25 data rows `screened`, from the r2 wave + prior), so the publications-screening coverage is satisfied with no ref-side change.
- **`/matrix-fit` whole-matrix (Phase-3):** [`tools/audit-matrix-semantic-fit.py`](../../tools/audit-matrix-semantic-fit.py) produced an 84-row worklist (matrix + per-doc framework-alignment rows lacking a lexical anchor); 2 judge subagents (42+42), refute-briefed, judged every cited control's TITLE (verified against the in-repo reference modules) against its row's document subject: **0 mismatches**, all `fits` or defensible `loose-supporting`. Consistent with the r1/r2 near-zero matrix-mismatch baseline.
- **#891 post-merge `/validate-pr`:** 0 defects, all six items PASS (batched here).
- Pre-push guard green (all 69 gates + D1-D7). This PR gets its own post-merge `/validate-pr` + `/retro`.

### Discipline observation

Both Phase-3 semantic passes this PR came back clean (`/screen-publications` nothing-pending; `/matrix-fit` 0 mismatches), reinforcing that the corpus's citation and control-code fit is sound (the earlier drift and reference-base-fidelity findings were about DESCRIPTIONS of the machinery and a held-edition gap, not corpus content accuracy). The r3 finding set so far: the AICPA held-edition item (RB-6(e), routed) and the guardrail-review machinery proposals (§3.62, routed); the content-accuracy instruments (`/validate`, `/claim-fit`, `/matrix-fit`) are clean.

## 2026-07-13, Library Version 2026.07.379, PR #891

The `/deep-assessment` r3 Phase-3 `/claim-fit` pass, the completion of the prior PR's drift fix (two more same-class carriers), and PR #890's batched QA. No corpus-document body changed (the two tool docstrings are not versioned documents).

### Changed

- [`tools/lint-version-date-consistency.py`](../../tools/lint-version-date-consistency.py) (gate-29 docstring) + [`tools/check-changelog-on-pr.py`](../../tools/check-changelog-on-pr.py) (D1 docstring): the drift-cluster COMPLETION. #890 fixed the three surfaces the r10 drift lens named; #890's `/validate-pr` Subagent A caught that gate 29's docstring was a 4th same-class carrier (stated only the legacy `## ...` header while the code matches both forms), and the orchestrator's bare-token find-every-carrier grep of `tools/` surfaced a 5th (the changelog-check gate's docstring, "lead-paragraph summaries"). Both reworded to the current compact-entry description. The drift cluster is now complete across five surfaces.
- [`.working/claim-fit/history.md`](../claim-fit/history.md): the `/claim-fit` r3 run row (net new findings 0); Version 1.0.8 to 1.0.9.
- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): Phase 3 `/claim-fit` marked COMPLETE.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #890 row (1 warning fixed in-branch); Version 1.2.657 to 1.2.658.
- [`.working/improvement-log.md`](../improvement-log.md): #890 `/retro` row (the drift-completeness recurrence); Version 1.0.596 to 1.0.597.
- [`README.md`](../../README.md): library CalVer 2026.07.378 to 2026.07.379; README Version 1.9.739 to 1.9.740.

### Added

- [`.working/validate-pr/2026-07-13-PR-890.md`](../validate-pr/2026-07-13-PR-890.md): the #890 post-merge `/validate-pr` record (1 warning fixed here + 5 confirming notes).

### Verification

- **`/claim-fit` r3 (Phase-3):** the `audit-claim-precision.py --tier A` worklist surfaced 8 corpus-wide Tier-A claims; the one introduced by this session's §3.57 batch (SOR/2018-64 24-month breach-record retention at `register-canonical-citations.md:145` + its Canada-annex carrier) is `prescribed`, confirmed verbatim against the held SOR/2018-64 s.6(1). The AICPA TSP 100 row is a `source-not-held` verdict (register cites the 2022-revised-POF edition; `grc_library_ref` holds the March-2020 edition), ALREADY-ROUTED to TODO RB-6(e). The other §3.57 citations are Tier-B soft-alignment already Sweep-101-verified. Net new findings: 0.
- **Drift completion:** all five descriptive surfaces now name both header forms; re-verified (root CHANGELOG is 100% compact; each gate's code matches both).
- **#890 `/validate-pr`:** 1 in-window warning (incomplete drift remediation) FIXED here + a 2nd same-class carrier found by the find-every-carrier grep, also fixed; 5 confirming notes.
- Pre-push guard green (all 69 gates + D1-D7). This PR gets its own post-merge `/validate-pr` + `/retro`.

### Discipline observation

Two lessons this PR. (1) The drift fix inherited the r10 lens's NAMED-surface enumeration (three) instead of re-running a find-every-carrier grep, so it was two surfaces short; the fix is to treat a lens's named surfaces as a floor and re-grep at bare-token width (the standing completeness discipline, applied one level up). (2) The improvement-log row-append join error recurred (a ` | ` where a newline belonged), self-caught by the pipe-count check; this row-append class is now frequent enough this session to warrant the standing mitigation of always placing a literal newline before the preserved next-row-start when appending a table row via Edit.

## 2026-07-13, Library Version 2026.07.378, PR #890

The `/deep-assessment` r3 Phase-3 `/guardrails` pass of record (guardrail-review r10), plus the in-window drift fix it surfaced, plus PR #889's batched QA. One corpus document (the audit-programme specification) changed; regenerated artefacts accordingly.

### Changed

- [`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py) + [`tools/lint-changelog-mirror-header-parity.py`](../../tools/lint-changelog-mirror-header-parity.py) + [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md): the drift-lens cluster fix. All three described the root CHANGELOG's per-entry header in the superseded `## YYYY-MM-DD, Library Version X, PR #N` form (and "lead-paragraph summaries"), while the gates' code already matches BOTH that legacy form and the compact `**date | version | PR #N**` form the TODO 3.16 reformat introduced. Reworded all three to name both forms, so a future maintainer cannot "correct" the code back to a `##`-only regex and reintroduce the orphaned-header defect gate 59 exists to catch. Spec Version `1.17.1` to `1.17.2`, Date to 2026-07-13.
- [`taxonomy.yml`](../../taxonomy.yml) + [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated for the spec Version bump (taxonomy first, then the derived artefacts).
- [`TODO.md`](../../TODO.md): new §3.62 routing the guardrail-review r10 machinery proposals (G1 branch-to-main hook, G3 register-ordering guard, G5 #376 expire-or-rescope, the gate-41 docstring symmetry nit) as maintainer-decision proposals; G2/G4 cross-referenced as already-tracked.
- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): Phase 3 `/guardrails` marked COMPLETE.
- [`.working/guardrail-reviews/history.md`](../guardrail-reviews/history.md): r10 row; Version 1.0.11 to 1.0.12.
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #889 row (0 findings); Version 1.2.656 to 1.2.657.
- [`.working/improvement-log.md`](../improvement-log.md): #889 `/retro` row; Version 1.0.595 to 1.0.596.
- [`README.md`](../../README.md): library CalVer 2026.07.377 to 2026.07.378; README Version 1.9.738 to 1.9.739.

### Added

- [`.working/guardrail-reviews/2026-07-13-r10.md`](../guardrail-reviews/2026-07-13-r10.md): the guardrail-review r10 per-run record (overlap 0 genuine / gap 2 warnings + 3 notes / drift 3 warnings fixed in-window).

### Verification

- **Guardrail-review r10 (Phase-3 `/guardrails` of record):** three lens subagents over the live machinery (69 gates / 13 rules / 23 skills / 14 commands / 9 advisory tools). Overlap 0 genuine findings (every layered defence self-delineated). Gap 2 warnings + 3 notes routed. Drift 3 warnings, a single-root-cause compact-CHANGELOG descriptive-surface cluster, FIXED in-window and re-verified (root CHANGELOG has zero `## ...` headers; the gates' code matches both forms). Each finding orchestrator-re-verified at source before action.
- **#889 post-merge `/validate-pr`:** 0 error / 0 warning / 0 findings, all six directed items PASS (batched here).
- Pre-push guard green (all 69 gates + D1-D7); the spec Version bump's regenerated artefacts pass gates 33/34. This PR gets its own post-merge `/validate-pr` + `/retro`.

### Discipline observation

The drift cluster is the mirror image of a well-functioning reformat: the #855/#857 compact-CHANGELOG change correctly updated all the CODE and the primary prose, but three secondary DESCRIPTIVE surfaces (two tool docstrings + one spec narrative) lagged, below the parity gates' resolution (gates 35/39 check the §6 table identity and row count, not header-format prose). Fixing them in-window follows the deep-assessment clear-mechanical-in-window convention; the machinery-change proposals (a HEAD==main edit guard, a register-ordering check) are routed for maintainer decision, not applied autonomously, per the guardrail-review skill.

## 2026-07-13, Library Version 2026.07.377, PR #889

Advances the deep-assessment r3 Phase 4 (audit-programme audit) and batches PR #888's post-merge QA. No corpus, pack, or taxonomy content changed.

### Added

- [`.working/validate-pr/2026-07-13-PR-888.md`](../validate-pr/2026-07-13-PR-888.md): the #888 post-merge `/validate-pr` record (0 error / 0 warning / 1 note, all six directed items PASS; the note is the register row-ordering slip, fixed in this PR).

### Changed

- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): Phase 4 updated to SUBSTANTIALLY COMPLETE, recording the blind-spot map (CLEAN) and the gate-mutation probe result (15 detected / 0 missed / 5 clean-pass / 0 false-positive on a disposable clone), plus the Sweep-101-confirmed four-surface parity; the dead-gate/coverage deep pass remains a re-entrant PENDING sub-item.
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): r3 row P4 pending to in-progress; **corrected the table row-ordering** (the r3 row had been inserted between r1 and r2; moved to after r2 so the table reads r1/r2/r3, matching the register's chronological-ascending convention).
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #888 row (1 note, fixed in-branch); Version 1.2.655 to 1.2.656.
- [`.working/improvement-log.md`](../improvement-log.md): #888 `/retro` row (the register-ordering slip as the 2nd occurrence of the structural-bookkeeping-edit class, a SIGNAL per the #887 WATCH; caught post-merge by the sweep); Version 1.0.594 to 1.0.595.
- [`README.md`](../../README.md): library CalVer 2026.07.376 to 2026.07.377; README Version 1.9.737 to 1.9.738.

### Verification

- **Phase 4 gate-efficacy (deep-assessment r3):** the blind-spot map probe returned CLEAN (0 non-exempt markdown outside all scope-derivable gates; `.claude/` 1 + `.working/` 113 known-by-design exempt). The gate-mutation probe on a `DISPOSABLE-COPY-OK`-marked clone: **15 detected / 0 missed / 5 clean-pass / 0 false-positive / 0 unjudgeable** (every synthetic defect caught by the intended gate; every clean control passed). Four-surface parity re-derived by Sweep 101 Subagent C (gate 35, 69 gates identical across all four surfaces).
- #888's one post-merge finding (register row-ordering) was orchestrator-verified and FIXED in this PR (grep confirms row order r1/r2/r3).
- This PR gets its own post-merge `/validate-pr` + `/retro` (batched into the next PR). Pre-push guard green.

### Discipline observation

The r3 register-ordering slip is the 2nd occurrence of the structural-bookkeeping-edit class (the #887 clobbers were the 1st) and is recorded as a SIGNAL, not yet a 3-PR pattern. Unlike the #887 clobbers (gate-caught pre-push), this one was caught POST-merge by #888's `/validate-pr` sweep, so it briefly reached `main` (zero functional impact, self-labelled rows). The reinforced technique note (confirm a bookkeeping file's ordering convention before inserting a row) is in the #888 retro row.

## 2026-07-13, Library Version 2026.07.376, PR #888

Opens run r3 of the whole-project `/deep-assessment` (maintainer-invoked at the 2026-07-13 resume, confirmed via `AskUserQuestion`). This PR records Phases 1-2 (run-state/inventory + mechanical baseline) and the Phase-3 `/validate` of record, opens the re-entrant register row, and batches PR #887's post-merge QA rows. No corpus, pack, or taxonomy content changed.

### Added

- [`.working/deep-assessment/2026-07-13-r3.md`](../deep-assessment/2026-07-13-r3.md): the r3 per-run detail file (Phases 1-2 complete; Phase 3 in progress with Sweep 101 as the `/validate` of record; Phases 4-8 pending; holds for maintainer sign-off).
- [`.working/validate-pr/2026-07-13-PR-887.md`](../validate-pr/2026-07-13-PR-887.md): the #887 post-merge `/validate-pr` record (0 error / 0 warning / 1 no-action frozen-record note; all six directed items PASS).

### Changed

- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): opened the r3 row (P1/P2 complete, P3 in-progress, P4-P8 pending, Status in-progress) with its per-run detail paragraph; live inventory recorded as 69 gates / 14 commands / 23 skills / 13 governance rules / 9 advisory tools (derived from the repo at `a5d2edd`, not remembered).
- [`.working/validate-pr/history.md`](../validate-pr/history.md): #887 row (1 no-action note; batched here); Version 1.2.654 to 1.2.655.
- [`.working/improvement-log.md`](../improvement-log.md): #887 `/retro` row (two self-caught pre-merge block-edit clobbers, both gate-caught; first occurrence of that class, WATCH not a pattern); Version 1.0.593 to 1.0.594.
- [`README.md`](../../README.md): library CalVer 2026.07.375 to 2026.07.376; README Version 1.9.736 to 1.9.737.

### Verification

- **Phase 1** (COMPLETE): non-shallow clone; all three repos present; lease held; live inventory derived from the repo (not remembered); HEAD `a5d2edd` (#887).
- **Phase 2** (COMPLETE): `tools/run_all_audits.sh` = all 69 gates pass at `a5d2edd` (resume + #887 post-merge baseline); regression suite exit 0 in isolation; generator `--check`s (gates 33/34) within the 69; PR-time checks D1-D7 green via the pre-push guard; sibling `grc_library_ref` validation gate OK (613 items) and `grc_library_scratch` validation gate OK. Green-at `a5d2edd` = 69/69, all sibling + generator checks clean.
- **Phase 3** (IN PROGRESS): the `/validate` of record is Sweep 101 (clean, 0 error / 0 warning / 2 note, loop-break control for #886 PASSED, asserted-expectations all corroborated). The heavy fan-out (`/full-qa`, `/fitness`, whole-matrix `/matrix-fit`, Tier-A+B `/claim-fit`, `/reference-audit` FULL, `/screen-publications`, `/guardrails`, advisory aids) is pending and runs re-entrantly.
- This r3-opening PR gets its own post-merge `/validate-pr` + `/retro` (batched into the next PR). Pre-push guard green.

### Discipline observation

The r3-opening lands the batched #887 QA promptly (rather than letting it ride an indefinitely-later PR) AND establishes the re-entrant Phase-1/2 checkpoint on `main`, so the multi-session deep assessment can resume cleanly at Phase 3 via the register. The deep assessment is count-free and inventory-deriving by design: Phase 1 re-derives the live instrument set from the repo, so the assessment's scope is whatever quality machinery exists at run time (any instrument added since r2 is covered automatically).

## 2026-07-13, Library Version 2026.07.375, PR #887

First PR of the 2026-07-13 resumed session (`claude/resume-sweep101-validate`): the loop-break corpus-wide `/validate` (Sweep 101) close-out, the compensating control for session-closing handoff PR #886 (which skipped its trailing per-PR QA). No corpus, pack, or taxonomy content changed.

### Added

- [`.working/validate-sweeps/2026-07-13-sweep101-iter1.md`](../validate-sweeps/2026-07-13-sweep101-iter1.md): the Sweep 101 iteration-1 detail file (six H2 sections: trigger/state, the three verbatim subagent returns, orchestrator synthesis, resulting PR).
- [`TODO.md`](../../TODO.md): RB-6 bullet (e), the AICPA TSP 100 held-edition mismatch routed from Sweep 101 (the register cites the upstream-verified 2022-revised-POF edition; the copy held in `grc_library_ref` is the earlier March-2020 edition). Reference-base fidelity item, flagged for the `/deep-assessment` `/reference-audit` + `/claim-fit` passes; low risk (register-only citation, real-world-accurate).

### Changed

- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): new Sweep 101 row on top (2 note, 0 error / 0 warning; loop-break control for #886 PASSES); file Version 2.0.96 to 2.0.97.
- [`.working/session-handoff.md`](../session-handoff.md): advanced the Resume-cursor "Last validation sweep" line to Sweep 101; **pruned** per the keep-current-plus-one-prior discipline (deleted the #833/sweep98 Next-actions and State-snapshot blocks and the #828-#832 asserted-expectations block; retained the #886 and #851 sessions); reworded the #851 block's now-dangling "supersedes the #833 ... below" pointer to "(pruned at the Sweep 101 resume)"; reconciled the current-truth version tokens (library `2026.07.375`, README `1.9.736`) and green-at (`fbd0162`/#886 = 69/69) to this PR's state.
- [`.working/session-state.md`](../session-state.md): concurrency lease ACQUIRED (`Active-session: claude/resume-sweep101-validate`, `Status: active`, fresh heartbeat `2026-07-13T19:06:32Z`); Current-task refreshed to the resumed-session state; gate 63 passes.
- [`README.md`](../../README.md): library CalVer 2026.07.374 to 2026.07.375; README Version 1.9.735 to 1.9.736.

### Verification

- **Sweep 101 result: 0 error / 0 warning / 2 note.** Full three-subagent A/B/C dispatch over the #852..#886 window (base `6fd59c7`/#851, HEAD `fbd0162`/#886). Mechanical baseline 69/69 at HEAD (no close-vs-start drift; clone non-shallow). Pre-flight: 421 files, 33 suppressed, 11 candidates, all the collection-count-word false-positive class, dismissed. Asserted-expectations cross-check: all CORROBORATED, 0 contradicted; loop-break control for #886 PASSES; zero in-window escaped defects.
- Subagent A held-verified every newly-cited §3.57 instrument's version/date/anchor against the held source text and confirmed the 3 self-caught slips (#879/#882/#884) left zero residual; B refuted the closed-§ (§3.58/§3.59), count-drift, instrument-version-drift, and cross-tree-codification classes corpus-wide; C confirmed four-surface parity at gate 69, gate-37 17/0 overlay (marker only in `.claude` copies), gate 60 clean, the compact-CHANGELOG-header parity-linter widening EXPANDED-not-weakened (fixtures + §6 narrative in lock-step), counts 69/13/23/14/18, spec 1.17.1, pack 1.61.5.
- The one in-window note (AICPA held-edition mismatch, `register-canonical-citations.md:196`) was orchestrator-verified against the held file and ROUTED to TODO RB-6(e); the other note (a frozen-record count-attribution scoping imprecision in the handoff, endpoint 147 correct) is no-action.
- This PR gets its own post-merge `/validate-pr` + `/retro` (batched into the next PR per recursion-avoidance); it is a normal close-out PR, not the session-closing handoff.
- Pre-push guard (`run_all_audits.sh` 69/69 + `run-pr-time-checks.sh`) green.

### Discipline observation

The AICPA note is the reference-base-fidelity class: a citation can be real-world-accurate and upstream-verified while the reference base holds an earlier edition of the cited work. The right move was to route (attempt acquisition of the true edition per the missing-reference SOP, then reconcile the row's provenance) rather than either hot-fix the register (the citation is correct) or ignore it (a future verifier checking the register against the held source would see a mismatch). It is deliberately handed to the upcoming `/deep-assessment` `/reference-audit`/`/claim-fit` passes, which are the formal instrument for this exact class.

## 2026-07-13, Library Version 2026.07.374, PR #886

Session-closing handoff PR for the 2026-07-12/13 resumed session (`claude/resume-sweep100-validate` + follow-ups, #852-#885). Lands working-state on `main` as a green merge so the next `/resume` rebuilds from the shared branch. No corpus, pack, or taxonomy content.

### Changed

- [`.working/session-handoff.md`](session-handoff.md): prepended this session's new current set (Next-actions block, State snapshot, Asserted-expectations block) per the refresh discipline; the next-session queue leads with the loop-break Sweep 101 then the maintainer-asked `/deep-assessment` components. The prior (#851) blocks become the 1-prior set; the next `/resume` prunes to keep current + 1 prior.
- [`.working/session-state.md`](session-state.md): concurrency lease RELEASED (`Status: released`, `Active-session: none`, fresh heartbeat); gate 63 passes.
- [`.working/session-metrics.md`](session-metrics.md): added this session's row (34 PRs #852-#885 + this handoff; zero escaped defects; subagent-token total not asserted because the session spans multiple compactions, per the measured-not-fabricated discipline).
- [`.working/next-prs.txt`](next-prs.txt): refreshed to the session-close state, leading the next `/resume` with Sweep 101 + the `/deep-assessment` components.
- [`README.md`](../../README.md): library CalVer 2026.07.373 to 2026.07.374; README Version 1.9.734 to 1.9.735.

### Verification

- Batches PR #885's `/validate-pr` (clean, 0 findings) and `/retro` rows.
- **This session-closing handoff PR takes NO trailing `/validate-pr` or `/retro`** (the loop-break exception): running them would spawn a records-then-merge loop with no terminating next PR at the session boundary. Recorded in [`validate-pr/history.md`](validate-pr/history.md) with the gate-50 marker (SKIPPED + handoff-PR exception). The compensating control is stronger: the next `/resume` runs a full corpus-wide `/validate` (Sweep 101) over the #852..#886 window and cross-checks the Asserted-expectations block.
- Green-at `503fda1` (#885) = 69/69; this PR is working-state + version + CHANGELOG only, so `main` stays 69/69 at the descendant merge. Pre-push guard green.

### Discipline observation

The session wound down on an explicit maintainer signal (not an assistant-initiated wind-down), after the overnight-safe queue was fully drained and every remaining item was maintainer-gated (fresh-session `/deep-assessment`, the deferred sensitive matrix-column, attended-only builds). The heavy `/deep-assessment` parts were deliberately NOT run deep in this long unattended session: they are routed to a fresh-session formal run per the skill's fresh-context, sign-off-terminated design, which the maintainer's "on resume we can do the /deep-assessment components" confirms.

## 2026-07-13, Library Version 2026.07.373, PR #885

Bookkeeping PR: records the scratch worker-exchange branch cleanup (the §3.58 follow-up) and batches PR #884's QA rows. No corpus, pack, or taxonomy content; the cleanup itself is on the `grc_library_scratch` repo (remote branch deletions, no content change), recorded here for the audit trail.

### Changed

- `grc_library_scratch` remote branches: deleted 38 stale delivery / assessment branches, each VERIFIED to have a merged pull request (so its content is preserved on scratch `main` and in history). Method: pruned local remote-tracking refs, intersected the live remote-branch set with the merged-PR head-ref set (`gh pr list --state merged`), confirmed every deletion candidate was in the merged set (a definitive `grep -Fxvf` check, zero not-merged), and there were no open scratch PRs. Three branches were deliberately LEFT: `claude/repo-access-test-ymk53f` (an unmerged test branch, no merged PR) and the two `worker-20260703-a` branches (`corpus-skill-distillation`, `gr-gap-1-register-population`) whose research deliveries are still PENDING per [`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py) (items 4.1 and 3.15, not yet consumed). This completes the scratch-branch cleanup the §3.58 delivery reconciliation left open (the maintainer's "clean up scratch as consumed" directive).

### Verification

- Each deleted branch confirmed merged (content on scratch `main`) before deletion; the two pending-research worker branches and the test branch were preserved. No open scratch PR existed, so no branch a PR depended on was removed.
- Bookkeeping-tier; no corpus/pack/taxonomy content, so no per-document version bump, taxonomy regeneration, or standing verifier.
- Batches PR #884's `/validate-pr` (clean, 0 findings) and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The cleanup was done verified-safe rather than bulk: branch deletion is destructive, so only branches with a confirmed merged PR (content demonstrably preserved on `main`) were deleted, and the pending-research and test branches were left for attended disposition rather than swept. The first batch push surfaced stale local remote-tracking refs (branches already deleted upstream), fixed by a `fetch --prune` before recomputing the live delete set, so no "ref does not exist" churn reached the final deletion.

## 2026-07-13, Library Version 2026.07.372, PR #884

Bookkeeping PR: batches PR #883's QA rows and records the read-only deep-assessment parts run per the maintainer's fallback directive. No corpus, pack, or taxonomy content.

### Changed

- [`.working/pending-decisions.md`](pending-decisions.md): added a `## Deep-assessment fallback` section recording the maintainer's 2026-07-13 directive ("if you run out of things to do, pick the most appropriate parts of a deep assessment ... we seek perfection"), the read-only parts run and their results, and the heavier parts routed to a maintainer-invoked fresh-session formal `/deep-assessment`.
- [`TODO.md`](../../TODO.md) §3.57: deleted a stale trailing sentence (the #883 `/validate-pr` finding) that still described Brazil Resolution 4/2023 as a future "can ride a later Brazil-annex PR" candidate after the same paragraph had already marked it applied in #883, an internal contradiction. The paragraph now reads only the accurate "applied in #883 / one deferred matrix-TSC-column residual" text.

### Verification (deep-assessment read-only parts run this turn)

- **Gate blind-spot map** ([`tools/audit-gate-blindspots.py`](../../tools/audit-gate-blindspots.py)): CLEAN, zero non-exempt markdown files scanned by zero scope-derivable gates (`.claude/` and `.working/` are convention-exempt by design). No finding.
- **Delivery-pipeline reconciliation** ([`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py)): 15 in the review set (11 PENDING + 4 UNMAPPED), all the pure-research seeds kept in the §3.58 disposition, mapping to open backlog items awaiting their scheduled builds (P6 new-domain, P4 adopter, FR-59, 3.15/3.16 crosswalks). Expected post-§3.58 state; no "backlog cleared" claim.
- **Deferred to a fresh-session formal `/deep-assessment`** (routed in pending-decisions): the gate-mutation probe (its disposable-clone setup was denied unattended), `/claim-fit` + `/matrix-fit` semantic-fit sampling (confirmatory, the citation verifiers already checked each row pre-push), `/reference-audit` FULL mode, and the adoptability persona pass. These are the heavier parts the skill designs to run fresh + attended.
- Bookkeeping-tier; no corpus/pack/taxonomy content, so no per-document version bump, taxonomy regeneration, or standing verifier.
- Batches PR #883's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The maintainer's fallback directive was applied conservatively: only the READ-ONLY, low-risk deep-assessment probes were run unattended (a clean gate blind-spot map, the expected delivery-pipeline state), and every heavier part that either needs blocked setup, benefits from fresh context, or would only confirm what the pre-push verifiers already checked was routed to a maintainer-invoked formal `/deep-assessment` rather than started deep in a long unattended session. This respects the skill's fresh-session, sign-off-terminated design while still surfacing the read-only findings the directive sought.

## 2026-07-13, Library Version 2026.07.371, PR #883

TODO §3.57 Medium follow-up applied: Brazil ANPD Resolution CD/ANPD No. 4/2023 (sanctions dosimetry) cited in the Brazil privacy annex and added to the citation register, with upstream currency confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #882 QA rows.

### Changed

- [`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md) (Enforcement and fines): a new bullet cites Resolution CD/ANPD No. 4/2023 (of 24 February 2023, the Regulation on Dosimetry and Application of Sanctions) as establishing the parameters and criteria the ANPD applies to calculate the base value of a fine and to apply the LGPD Article 52 sanctions, where the section previously listed only the Article 52 ceilings. Notes that 4/2023 amended the fiscalization-and-sanctioning-process regulation approved by Resolution CD/ANPD No. 1/2021, with a verification note (verified 2026-07-13; DOU 27 February 2023; in force). Doc Version bumped 1.1.5 to 1.1.6, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new row after Resolution CD/ANPD No. 18/2024, `Resolution CD/ANPD No. 4/2023` / `2023` / `2023-02-27` / topic the ANPD dosimetry-and-sanctions-application regulation (base-fine calculation and LGPD Article 52 sanctions; amends Resolution 1/2021). The Publication-date cell uses full-precision 2023-02-27 to match the sibling ANPD rows (a verifier observation applied). Register Version bumped 1.5.34 to 1.5.35.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation).** WebSearch against the ANPD (gov.br) and Brazilian legal sources confirmed Resolução CD/ANPD nº 4, de 24 February 2023, is the Regulamento de Dosimetria e Aplicação de Sanções, published in the Diário Oficial da União on 27 February 2023, establishing the parameters and criteria for calculating the base value of fines and applying the Article 52 sanctions, and that it amended the fiscalization-and-sanctioning-process regulation approved by Resolution CD/ANPD No. 1/2021 (of 28 October 2021). In force.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the annex + register change (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#882).
- Register per-document Version bumped 1.5.34 to 1.5.35; Brazil annex 1.1.5 to 1.1.6; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 147 standards) and citation linters pass.
- Batches PR #882's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

This clears the last citation-apply residual of the §3.57 reference-breadth work (the Medium Brazil follow-up that surfaced in the delivery beyond the maintainer's named `[V]` set). The distinction the bullet draws, that the Article 52 percentages are statutory maximums while 4/2023 supplies the base-value calculation methodology, is the load-bearing precision: a reader should not read the ceilings as the fine-setting rule. §3.57 now has a single remaining residual, the deferred matrix TSC-column mapping (a single-file sensitive change for a `/matrix-fit` follow-up, not a citation apply), so the item is narrowed further but not closed.

## 2026-07-13, Library Version 2026.07.370, PR #882

TODO §3.57 `[V]` row applied (the last of the maintainer's named set): EDPB Guidelines 8/2022 (identifying the lead supervisory authority) cited in the EU privacy annex and added to the citation register, with upstream currency confirmed this turn against the primary-source PDF version-history table. Corpus-body change (substantive tier: one refute-briefed verifier pre-push, which caught and reverted a mid-apply version slip), plus the batched #881 QA rows.

### Changed

- [`privacy/jurisdictions/annex-privacy-european-union.md`](../../privacy/jurisdictions/annex-privacy-european-union.md) (Applicable laws and regulatory authorities): the one-stop-shop / lead-supervisory-authority bullet now cites the EDPB Guidelines 8/2022 on identifying a controller or processor's lead supervisory authority (Version 2.1, adopted 28 March 2023 with a minor correction of 28 September 2023, a targeted update superseding the Article 29 Working Party guidelines WP244 rev.01) as setting out the main-establishment test, where it previously asserted the main-establishment rule with no source. Doc Version bumped 1.1.5 to 1.1.6, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new row in the EDPB Guidelines cluster, `EDPB Guidelines 8/2022 (identifying the lead supervisory authority)` / `Version 2.1` / `2023-09` / topic the main-establishment test for the GDPR one-stop-shop; superseded-versions cell records Version 1.0 (10 October 2022), Version 2.0 (28 March 2023), and WP244 rev.01, mirroring the sibling 01/2022 row's treatment of a minor-correction version. Matches the cluster's convention (general EDPB guidelines URL, bare Last-verified date). Register Version bumped 1.5.33 to 1.5.34.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation), against the primary source.** WebSearch confirmed Guidelines 8/2022 is the EDPB guideline on identifying a controller or processor's lead supervisory authority and that it supersedes WP244 rev.01. On the version token there was a mid-apply slip: an incomplete WebSearch summary ("final version, Version 2") led to first writing Version 2.0, and the delivery candidate's "v2.1" was wrongly "corrected" to v2.0. The pre-push verifier flagged it, and a direct read of the primary-source PDF (cover page plus the page-2 version-history table) confirmed the current version is **2.1** (minor correction to footnote 12, 28 September 2023, over Version 2.0 of 28 March 2023, over Version 1.0 of 10 October 2022). The candidate was right; the register and annex were corrected to Version 2.1 before push.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the annex + register change (read-only-git), with special attention to the version (2.0 vs 2.1), plus a separate `/validate-pr` Subagent A on the prior PR (#881).
- Register per-document Version bumped 1.5.33 to 1.5.34; EU annex 1.1.5 to 1.1.6; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 146 standards) and citation linters pass.
- Batches PR #881's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

All seven rows of the maintainer's named §3.57 `[V]` set are now applied (#876 to #882), each with upstream currency confirmed this turn per the VM directive rather than routed, and each refute-verified; the §3.57 backlog item itself stays open on two residuals (below), so there is no DONE rotation in this PR. The version episode here is the inverse of the earlier AICPA/SOR catches and the sharper lesson: a delivery candidate's version token is a hypothesis, but so is a WebSearch SUMMARY. The candidate's "v2.1" was correct; an incomplete WebSearch summary ("final version, Version 2") led to wrongly "correcting" it to v2.0, and only a direct read of the primary-source PDF version-history table (prompted by the pre-push verifier) settled it at v2.1. Lesson: for a specific version token, the authoritative source is the publisher's own version-history page or PDF, not a search-result summary that can elide a minor `.1` correction, and a candidate value should not be "corrected" downward without primary-source evidence at least as strong as the value being overwritten. TODO §3.57 stays open on two residuals (the Medium Brazil 4/2023 sanctions-dosimetry follow-up and the deferred matrix TSC-column mapping), so it is narrowed rather than closed this PR.

## 2026-07-13, Library Version 2026.07.369, PR #881

TODO §3.57 `[V]` row applied: NIS2 Commission Implementing Regulation (EU) 2024/2690 named in the NIS2 implementation annex and added to the citation register, with upstream currency and legal basis confirmed this turn, a load-bearing entity-scope caveat, and a factual locator correction. Corpus-body change (substantive tier, escalated to TWO independent verifier lenses given the correction plus scope caveat), plus the batched #880 QA rows.

### Changed

- [`compliance/annex-nis-2-implementation.md`](../../compliance/annex-nis-2-implementation.md): Commission Implementing Regulation (EU) 2024/2690 is now named in three places, the Article 21 cybersecurity-risk-management-measures section (it specifies the technical and methodological requirements of the Article 21(2) measures), the Article 23(3) significance-threshold section (it specifies the concrete significant-incident parameters under Article 23(11)), and the framework-alignment table. Each carries the load-bearing scope caveat that 2024/2690 binds only the specific digital-infrastructure and digital-service entity types in its scope (DNS providers and TLD name registries, cloud, data-centre and content-delivery-network providers, managed-service and managed-security-service providers, online marketplaces, online search engines, social-networking platforms, and trust-service providers), NOT all NIS2 entities. The framework-alignment row's locator was also CORRECTED: it read "Article 21(5) and 27", but the act's legal basis is Article 21(5) and 23(11) of Directive (EU) 2022/2555 (Article 27 is the entity-registry provision, not the implementing-act empowerment). Doc Version bumped 1.2.0 to 1.2.1, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new EU-block row after the NIS 2 Directive, `EU NIS 2 Implementing Regulation` / `Commission Implementing Regulation (EU) 2024/2690` / `2024-10` / topic the Article 21(2) technical requirements and Article 23(3) significant-incident parameters for the in-scope entity types only (adopted 17 October 2024; basis Article 21(5) and 23(11)). Register Version bumped 1.5.32 to 1.5.33.

### Verification

- **Upstream currency and legal basis confirmed this turn (the `[V]` obligation).** WebSearch confirmed 2024/2690 was adopted 17 October 2024 (published 18 October 2024) "pursuant to Articles 21(5), first subparagraph and 23(11), second subparagraph, of Directive (EU) 2022/2555", establishing the technical and methodological requirements of the Article 21(2) measures and specifying the significant-incident cases under Article 23(3); and that its scope is the specific digital entity types listed above. The locator correction (21(5)+23(11), not 21(5)+27) is confirmed against the regulation's own legal basis. The EUR-Lex ELI page is JS-gated to automated fetch, so the confirmation rests on the WebSearch of the regulation's preamble and multiple authoritative summaries (ENISA, national regulators).
- **Escalated verification (err-toward-quality directive).** Because this row combined a factual correction with a load-bearing scope caveat, it drew TWO independent refute-briefed verifier lenses: an accuracy lens (the locator correction, dates, attributions, register-row form) and a scope/completeness lens (the entity-scope list, whether any edit over-reaches to imply all-NIS2 applicability, and internal consistency with the annex's entity-classification table), plus a separate `/validate-pr` Subagent A on the prior PR (#880).
- Register per-document Version bumped 1.5.32 to 1.5.33; NIS2 annex 1.2.0 to 1.2.1; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 145 standards) and citation linters pass.
- Batches PR #880's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

This row is the clearest case in the `[V]` wave for the escalated (two-lens) verification: it does not merely add a citation but CORRECTS an existing factual error (the "Article 27" locator) and asserts a scope boundary a reader could otherwise over-read (the annex's entity-classification table lists Essential/Important entities broadly, whereas 2024/2690 binds only a digital-service subset). A single confirm-oriented pass could rubber-stamp both the correction and the caveat; two adversarial lenses, one probing the correction's own accuracy and one probing whether the caveat is complete and non-contradictory with the rest of the annex, is the proportionate response to a change that both fixes a fact and fences a scope. Both lenses returned no blocking finding but each surfaced one precision improvement, both applied per the err-toward-quality directive: the scope lens caught that "DNS and TLD providers" loosely reads to include registrars (out of 2024/2690's scope) and is inconsistent with the annex's own line-33 term, corrected to "DNS providers and TLD name registries" (matching the regulation and the annex); the accuracy lens caught a Standard-ID spacing inconsistency ("EU NIS2 Implementing Regulation" vs the sibling "EU NIS 2 Directive"), harmonized to "EU NIS 2 Implementing Regulation". Both fixes were propagated across all carriers (the corpus edit and this CHANGELOG entry) by a whole-changeset grep.

## 2026-07-13, Library Version 2026.07.368, PR #880

TODO §3.57 `[V]` row applied: EDPB Opinion 28/2024 (data protection aspects of AI models) cited in the Privacy and Data Governance Policy §4.7, with currency re-confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #879 QA rows.

### Changed

- [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md) §4.7 (AI training data governance): a new bullet cites the EDPB Opinion 28/2024 on data protection aspects of AI models (adopted 17 December 2024) as the authoritative EU guidance on the two questions the section turns on, the legal basis for processing personal data to develop or deploy an AI model (including legitimate interest) and whether an AI model or its training data can be anonymous (the basis for the reidentification-risk assessment already in the section). This is an additive breadth citation: the opinion is already engaged elsewhere in the corpus (the legitimate-interest-assessment template), and §4.7's training-data lawful-basis and anonymization clauses are exactly what it addresses. Doc Version bumped 1.4.13 to 1.4.14, Date to 2026-07-13.
- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): the existing EDPB Opinion 28/2024 row's Last-verified cell refreshed from 2026-06-30 to 2026-07-13 (bare-date form, matching the adjacent EDPB Guidelines rows; the row already existed from the 2026-06-30 register population; no new row and no other cell changed). Register Version bumped 1.5.31 to 1.5.32.

### Verification

- **Upstream currency re-confirmed this turn (the `[V]` obligation + the register's own load-bearing-row re-check cadence).** WebSearch against the EDPB site and legal-analysis sources confirmed Opinion 28/2024 was adopted 17 December 2024, remains the current EDPB guidance, and has NOT been superseded (a February 2025 CNIL recommendation set and a September 2025 CJEU pseudonymisation judgment exist but do not supersede the opinion). The register's "Original (no later revision)" version is therefore still correct; only the Last-verified date advanced.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the policy + register change (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#879).
- Register per-document Version bumped 1.5.31 to 1.5.32; policy 1.4.13 to 1.4.14; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency and citation linters pass.
- Batches PR #879's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

This row exercised the register's own version-currency cadence (a load-bearing `[V]` row older than one week is re-checked before reliance, and its Last-verified advanced in the same PR), not just the citation gates: the opinion was already registered, so the work was to confirm it is still current before leaning a new citation on it, then record that re-confirmation. Distinguishing "cite a held-and-registered source after a fresh currency check" from "add a new register row" kept the change minimal (one refreshed cell, not a duplicate row). The refute-verifier raised two non-blocking observations, both applied per the "err toward quality" directive: the refreshed cell was written bare (2026-07-13) to match the adjacent EDPB Guidelines rows, and the §4.7 closing sentence was softened from "made against that Opinion" to "made by reference to that Opinion" to avoid over-claiming the opinion's (non-binding, interpretive) legal force.

## 2026-07-13, Library Version 2026.07.367, PR #879

TODO §3.57 `[V]` row applied: Canada Breach of Security Safeguards Regulations (SOR/2018-64) cited in the Canada privacy annex and added to the citation register, with upstream currency confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #878 QA rows.

### Changed

- [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md): the breach-of-security-safeguards bullet now cites the Breach of Security Safeguards Regulations (SOR/2018-64, in force 1 November 2018) for the regulation-level obligations the statute's s. 10.1 threshold does not spell out: the prescribed content of the OPC report and the individual notification, and the duty to keep a record of EVERY breach of security safeguards (whether or not it met the real-risk-of-significant-harm reporting threshold) for 24 months after the day the organization determines the breach occurred. Carries a verification note (verified against the consolidated Justice Laws text 2026-07-13, in force since 2018-11-01, no amendment). Doc Version bumped 1.1.1 to 1.1.2, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new row after Canada PIPEDA, `Canada Breach of Security Safeguards Regulations` / `SOR/2018-64` / `2018-11` / topic the PIPEDA breach regulation (prescribed report and notification content plus the 24-month breach-record retention). Gives the standards-currency linter an anchor for the newly-named citation.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation).** WebSearch against the Justice Laws site (laws-lois.justice.gc.ca), the Canada Gazette, and CanLII confirmed SOR/2018-64 is the Breach of Security Safeguards Regulations under PIPEDA, in force 1 November 2018, with no substantive amendment; and that the 24-month record-retention duty applies to every breach of security safeguards, not only reportable ones. PIPEDA (and thus this regulation) remains in force after the CPPA/Bill C-27 lapse.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the annex + register change (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#878).
- Register per-document Version bumped 1.5.30 to 1.5.31; Canada annex 1.1.1 to 1.1.2; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 144 standards) and citation linters pass. `laws-lois.justice.gc.ca` is already on the external-link-domain allowlist (the PIPEDA row uses it).
- Batches PR #878's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The citation distinguishes the regulation-level duty (24-month record of EVERY breach, prescribed content) from the Act-level s. 10.1 reporting threshold already in the bullet, so a reader does not read the 24-month record obligation as applying only to reportable breaches; the "whether or not it met the reporting threshold" clause is the load-bearing precision, confirmed against the regulation text this turn. The pre-push refute-verifier caught a stale "current to 2026-03-31" consolidation date in the draft verification note (drawn from a WebSearch snippet; a direct WebFetch of the live Justice Laws page showed "current to 2026-05-26"). Rather than substitute the newer date (which self-stales at the next site reconsolidation), the drift-prone "current to" claim was dropped entirely across all four carriers it had reached (the annex note, the TODO §3.57 annotation, and two CHANGELOG-detailed lines, caught by a whole-changeset bare-token grep), keeping only the durable legal facts (in force 2018-11-01, no subsequent amendment). Lesson: a Justice-Laws "current to" date is a site-consolidation marker that drifts independently of the regulation, so it does not belong in a citation's verification note; the register row's "verified 2026-07-13" already captures the verification date.

## 2026-07-13, Library Version 2026.07.366, PR #878

TODO §3.57 `[V]` row applied: Brazil ANPD Resolution CD/ANPD No. 18/2024 (the encarregado/DPO regulation) cited in the Brazil privacy annex and added to the citation register, with upstream currency confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #877 QA rows.

### Changed

- [`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md): the Data Protection Officer bullet now cites Resolution CD/ANPD No. 18/2024 (of 16 July 2024, the Regulation on the activities of the encarregado) as the ANPD rule operationalizing the appointment, definition, attributions, and performance of the encarregado under LGPD Article 41, where it previously cited only the LGPD articles. Carries a verification note (confirmed against the ANPD's official regulations publication 2026-07-13; enacted 16 July 2024, DOU 17 July 2024, in force, no amendment), matching the annex's established citation style for the other ANPD resolutions it names (15/2024, 2/2022, 19/2024). Doc Version bumped 1.1.4 to 1.1.5, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new row after Resolution CD/ANPD No. 15/2024, `Resolution CD/ANPD No. 18/2024` / `2024` / `2024-07-17` (DOU) / topic the ANPD encarregado (DPO) regulation under LGPD Article 41. Mirrors the existing 15/2024 row's style; gives the standards-currency linter an anchor for the newly-named citation.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation).** WebSearch against the ANPD (gov.br) and Brazilian legal sources confirmed Resolução CD/ANPD nº 18, de 16 de julho de 2024, is the encarregado regulation, published in the Diário Oficial da União on 17 July 2024, in force since publication, with no amendment surfaced.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the annex + register change (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#877).
- Register per-document Version bumped 1.5.29 to 1.5.30; Brazil annex 1.1.4 to 1.1.5; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 143 standards) and citation linters pass. `gov.br` is already on the external-link-domain allowlist.
- Batches PR #877's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The citation was tied precisely to LGPD Article 41 (the encarregado provision) rather than the annex bullet's broader "Articles 41 to 43" header, since the resolution regulates the encarregado function specifically; over-attributing it to the whole 41-to-43 range (which also covers agent liability) would have been a scope overstatement. A Medium follow-up candidate from the same delivery (Resolution CD/ANPD No. 4/2023, the sanctions-dosimetry rule, for the annex's enforcement section) was recorded in TODO §3.57 for a later Brazil-annex PR rather than bundled here, keeping this PR to the single named High row.

## 2026-07-13, Library Version 2026.07.365, PR #877

TODO §3.57 `[V]` row applied: Commission Implementing Decision (EU) 2021/915 (the controller-processor standard contractual clauses) named in the Article 28 DPA template and added to the citation register, with upstream currency confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #876 QA rows.

### Changed

- [`privacy/template-dpa-article-28.md`](../../privacy/template-dpa-article-28.md): Section 11 (Form and signature) now names the Commission controller-processor SCC set as Commission Implementing Decision (EU) 2021/915 (adopted under Article 28(7)), where it previously said only "record the SCC set and version used"; a new framework-alignment row cites the same instrument. Both carry the accuracy guard that 2021/915 is distinct from the Chapter V transfer clauses in Commission Implementing Decision (EU) 2021/914 (the decision's own recitals state its clauses cannot be used as Chapter V transfer clauses, so this is the correct instrument for the Article 28 processing contract and must not be conflated with the transfer SCCs). Doc Version bumped 1.0.1 to 1.0.2, Date to 2026-07-13.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new EU-block row (after EU GDPR), `EU Controller-Processor SCCs` / current version `Commission Implementing Decision (EU) 2021/915` / `2021-06` / topic the Article 28(7) GDPR and Article 29(7) Regulation (EU) 2018/1725 controller-processor SCCs, with the same not-a-transfer-mechanism guard in the topic cell. This gives the standards-currency linter an anchor for the newly-named citation.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation).** WebSearch against EUR-Lex and legal-analysis sources confirmed 2021/915 was adopted 4 June 2021, published in the Official Journal 7 June 2021, entered into force 27 June 2021, and has not been amended since; and that 2021/915 is the controller-processor set (Article 28) while 2021/914 is the separate international-transfer set (Chapter V), not swapped.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the doc + register change (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#876).
- Register per-document Version bumped 1.5.28 to 1.5.29; DPA template 1.0.1 to 1.0.2; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated (taxonomy first), both `--check` clean. Standards-currency (now 142 standards) and citation linters pass. `eur-lex.europa.eu` is already on the external-link-domain allowlist.
- Batches PR #876's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The delivery candidate's explicit accuracy guard (2021/915 must NOT be routed to the cross-border-data-flow register, because its own recital bars its use as a Chapter V transfer instrument) was carried into both the doc text and the register topic cell, so a future reader cannot conflate the Article 28 processing SCCs with the Chapter V transfer SCCs. This is the value-attribution-precision lesson from the earlier EDPB bundles applied proactively: name the exact instrument and fence off the adjacent-but-wrong one in the same edit.

## 2026-07-13, Library Version 2026.07.364, PR #876

TODO §3.57 `[V]` row applied: AICPA Trust Services Criteria (TSP Section 100) added to the canonical-citations register, with upstream currency confirmed this turn. Corpus-body change (substantive tier: one refute-briefed verifier pre-push), plus the batched #875 QA rows.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a new `## AICPA assurance criteria` block (placed after the ISACA-frameworks / COBIT block) with one row, `AICPA TSP Section 100` / current version `2017 Trust Services Criteria (with revised points of focus, 2022)` / topic the SOC 2 subject-matter criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy). This closes a genuine internal inconsistency: the Trust Services Criteria are cited across the corpus (audit-planning, audit-evidence-package "SOC 2 CC6.1", regulator-interaction) and AICPA is an approved publisher-source in the citation-verification specification, but the register carried no AICPA / TSC row, so the standards-currency linter could not track a stale TSC reference. The row now gives it that anchor.

### Changed

- [`TODO.md`](../../TODO.md) §3.57: AICPA TSP 100 moved from routed-to-maintainer to APPLIED (#876). Per the maintainer's 2026-07-13 direction, the assistant now confirms the `[V]` rows' currency itself via WebSearch/WebFetch (the VM directive) rather than routing them; the annotation records this and lists the remaining `[V]` rows still to apply, each with its own currency confirmation.

### Verification

- **Upstream currency confirmed this turn (the `[V]` obligation).** WebSearch plus a WebFetch of the AICPA resource page confirmed the current form is the 2017 Trust Services Criteria with revised points of focus (2022), and that the 2022 update revised the points of focus, not the criteria themselves; corroborated by the Deloitte DART index of the same TSP Section 100 title. No AICPA TSC version newer than the 2017-criteria-with-2022-POF form exists as of this session.
- Substantive-tier: one skeptical refute-briefed verifier subagent on the register row (read-only-git), plus a separate `/validate-pr` Subagent A on the prior PR (#875).
- Register per-document Version bumped 1.5.27 to 1.5.28; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated in that order (taxonomy first), both `--check` clean. Standards-currency and citation linters pass with the new row. `aicpa-cima.com` is already on the external-link-domain allowlist.
- Batches PR #875's `/validate-pr` and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The `[V]` flag did exactly its job: it gated the row on a real upstream check rather than a catalogue assumption, and the maintainer's VM directive (retrieve and verify yourself, do not defer a retrievable check) is what let the row be applied this session instead of routed. The publication-date cell records the year with the revised-points-of-focus annotation rather than a fabricated month, since the publisher page gives no exact month for the 2022 revision (accuracy over completeness). The superseded-versions cell is `-` rather than an unverified predecessor designation.

## 2026-07-13, Library Version 2026.07.363, PR #875

Delivery-pipeline reconciliation (TODO §3.58) closed on the grc_library side under the maintainer's disposition rule, plus the batched #874 QA rows. Bookkeeping; no corpus, pack, or taxonomy content.

### Changed

- [`TODO.md`](../../TODO.md): §3.58 (delivery-pipeline reconciliation) rotated out and into [`DONE.md`](DONE.md). The maintainer's disposition rule on waking, for scratch deliveries older than five days keep ONLY pure-research seeds and discard the rest, was executed in `grc_library_scratch` PR #164 (merged), which removed the five consumed / stale-non-pure-research inbox drops (`gr-10-history-gate-batching`, `changelog-root-reformat-build`, `atlas-crosswalk-317`, `ai-gaps-expansion-plan`, the `claude-pack-hygiene` programme) and annotated the claims-ledger and coverage dispositions, keeping the pure-research seeds as input. A new §3.61 was added for the residual tooling weakness the reconciliation surfaced (the recycled-number token map in the delivery-status tool), so it is tracked rather than dropped.
- [`TODO.md`](../../TODO.md) §3.57 naming harmonized (a #874 `/validate-pr` finding): both short forms of the standard-contractual-clauses decision now read "Commission Implementing Decision (EU) 2021/915" (was mixed "Implementing Decision" / "Commission Decision").
- [`.working/pending-decisions.md`](pending-decisions.md): the delivery-pipeline-reconciliation entry marked RESOLVED with the maintainer's rule and the scratch #164 execution; original entry retained for the audit trail.

### Fixed

- [`.working/session-state.md`](session-state.md): the Current-task PR-count for the overnight segment (a #874 `/validate-pr` finding) corrected to 13 (the range #862-#874 is 13 PRs; the superseded text said 17). The Current-task field was also refreshed to the attended focus and de-bloated (the stale overnight tail trimmed; per-PR detail lives in the PRIOR blocks and the audit trail).

### Verification

- Bookkeeping-tier; no corpus, pack, or taxonomy content, so no per-document version bump, taxonomy regeneration, or standing verifier. Gate 63 (session-state lease shape) passes standalone.
- Batches PR #874's `/validate-pr` (two in-window gate-exempt findings, both fixed here, recorded at [`.working/validate-pr/2026-07-13-PR-874.md`](validate-pr/2026-07-13-PR-874.md)) and `/retro` rows.
- The pre-push guard (full audit suite plus PR-time checks) is green.

### Discipline observation

The §3.58 reconciliation confirmed the value of the maintainer's describe-the-work-against-the-current-backlog rule over the delivery-status tool's token map: recycled section numbers made the token map unreliable, which is exactly why the disposition was age-plus-purity rather than a token lookup. The tool weakness is now a tracked item (§3.61) rather than an unrecorded gap. The two #874 `/validate-pr` findings were both in gate-exempt prose and both fixed in this next PR per recursion-avoidance, so nothing escaped; the count error was caught by an independent read of the very field it lived in.

## 2026-07-13, Library Version 2026.07.362, PR #874

§3.57 reference-breadth close-out for the overnight run (bookkeeping): record which citation rows are applied and route the remaining version-sensitive rows to the maintainer.

### Changed

- [`TODO.md`](../../TODO.md) §3.57 annotated: the `lc` (held, currency-confirmed) rows are APPLIED, the four High EDPB-privacy citations (#866-#869) plus the Medium EDPB 07/2022 (#873); the REMAINING rows are all version-sensitive `[V]` and are routed to the maintainer for upstream-currency confirmation. Notably AICPA TSP 100 (to the citation register) is a genuine internal inconsistency, the Trust Services Criteria are cited corpus-wide but absent from the register, held at the 2017 criteria with 2022 revised points of focus but `[V]`, so its register "current version" should be set only after the maintainer's upstream re-confirm.

### Verification

- Bookkeeping-tier (TODO annotation plus batched QA rows); no corpus, pack, or taxonomy content, so no per-document version bump, taxonomy regeneration, or standing verifier.
- The overnight-safe §3.57 slice (five `lc` citations) is complete; the `[V]` rows are consistently routed with the other `[V]` §3.57 items (upstream currency needs egress / a fresh session, which the `[V]` flag demands and the overnight run cannot satisfy).
- Batches PR #873's `/validate-pr` (clean) and `/retro` rows.

### Discipline observation

Honest saturation of the overnight-safe reference-breadth scope. Rather than auto-apply the `[V]` AICPA row on a catalogue-check-as-currency basis (inconsistent with routing the other `[V]` rows, and the `[V]` flag exists precisely because the Trust-Services-Criteria 2017-criteria-plus-2022-POF versioning needs upstream confirmation), the row is routed to the maintainer with its assessment. Integrity over Speed: a register "current version" is a currency ground-truth that must rest on a real upstream check, not a deferred assumption.

## 2026-07-13, Library Version 2026.07.361, PR #873

Reference-breadth apply (TODO §3.57), a Medium held-verifiable citation: cite EDPB Guidelines 07/2022 (certification as a tool for transfers) in the transfer-impact-assessment template.

### Changed

- [`privacy/template-transfer-impact-assessment.md`](../../privacy/template-transfer-impact-assessment.md): the §2 transfer-tool cell (which flagged the certification mechanism, Article 46(2)(f), as carrying a distinct effectiveness analysis but cited no guidance) now cites **EDPB Guidelines 07/2022 on certification as a tool for transfers (Version 2.0, adopted 14 February 2023)** as the authoritative guidance, and a `## Framework alignment` row was added. Additive precision on the certification case (the template already attributes its six-step methodology to EDPB Recommendations 01/2020). Confirmed not already cited. Version 1.0.2 to 1.0.3.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a register row for EDPB 07/2022 (Version 2.0, 2023-02), soft-law supervisory-guidance scope. Version 1.5.26 to 1.5.27.

### Verification

- Scope-level citation (the guideline's own titled subject is certification as a transfer tool, confirmed at held line 55, "certification as a new transfer mechanism"), self-grounded by reading the held source's subject and version-history directly rather than the worklist characterization.
- Version fresh-read from the held version-history: v2.0 = 14 February 2023 (after public consultation), v1.0 = 14 June 2022 (for public consultation). The register superseded cell states the v1.0 date exactly as the held source records it.
- Currency: held at v2.0; ref-catalogue `last_checked` 2026-07-12; not re-verified upstream this turn (recorded as the register Last-verified date).
- Confirmed the template did not already cite EDPB 07/2022 (grep clean at apply); artefacts regenerated after the two per-document Version bumps.
- Skeptical pre-push verifier (substantive tier; citation-accuracy-focused, read-only git): NO defect (refutation exhausted). Citation accuracy CONFIRMED against the held source, the guideline's subject is certification as a transfer mechanism under Articles 42(2) and 46(2)(f) (held lines 55 to 57), and the distinct-effectiveness-analysis / authoritative-guidance framing is grounded (held 70-71, 392-398, 575) and correctly scoped as soft-law existence-tier guidance, not a specific attributed value. Version accurate (v2.0 14 February 2023, v1.0 14 June 2022 for public consultation, register cell an exact match); uncited before; register 7-column well-formed with an honest Last-verified 2026-07-12; versions and artefacts consistent. The lone gate-36 FAIL was the concurrent-run artefact (the suite passes standalone, 373 tests OK). This scope-level, self-grounded citation landed clean with no finding, confirming the self-grounding discipline.
- Batches PR #872's `/validate-pr` and `/retro` rows.

### Discipline observation

A Medium §3.57 citation beyond the four High EDPB `lc` bundles. Lower mis-attribution risk than the cluster (scope-level: the guideline is cited for its own titled subject, not for a specific attributed value), and self-grounded by a direct held-source read of the subject and version-history, applying the accumulated citation lessons (fresh-read the version-history; no phrasing pattern-match).

## 2026-07-13, Library Version 2026.07.360, PR #872

Backlog reconciliation (bookkeeping): record the §3.60 scope assessment and narrow §3.56 to defer its stale cosmetics grab-bag.

### Changed

- [`TODO.md`](../../TODO.md): §3.60 (per-run fixture tempdir) annotated with the 2026-07-13 assessment, the fix is entangled at roughly 14 test-fixture sites (content-embedded paths, path-based assertions, and the orphan-test's dependence on the fixture directory being outside the referenced corpus), so it is a dedicated multi-site refactor for a fresh session, not the small change first assumed; the #870/#871 awareness-mitigation is the interim control. §3.56(c) annotated: two flagged cosmetics are already resolved or mislocated, the rest need the Phase-4 acceptance detail plus target-file reading, so the (c) grab-bag is deferred to a single attended pass rather than overnight archaeology.

### Verification

- Bookkeeping-tier change (TODO annotations plus batched QA rows); no corpus, pack, or taxonomy content, so no per-document version bump, taxonomy regeneration, or standing verifier (the mechanical gates and the post-merge /validate-pr are the controls, per the tiered verification standard's quick-fix / bookkeeping tier).
- Batches PR #871's `/validate-pr` (clean) and `/retro` rows.

### Discipline observation

An honest-assessment PR: rather than force the §3.60 refactor or the stale §3.56 cosmetics under overnight time pressure, both were assessed and their true scope and state recorded so a fresh attended session tackles them correctly. This applies the evidence-grounded-completion "state the scope, do not overclaim" discipline to backlog items whose overnight-doability turned out lower than their one-line estimate.

## 2026-07-13, Library Version 2026.07.359, PR #871

Read-only-git subagent rule, pack-distribution half (TODO §3.59 remainder; completes and closes §3.59). The project surfaces landed in #870; this adds the project-agnostic discipline to the distributable pack rule so fork adopters inherit it.

### Changed

- [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](../../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) and its project-side mirror copy (gate-37 parity): a new "Dispatched subagents inspect version control read-only (shared-tree safety)" subsection in the skeptical pre-push verification section, a dispatched verifier or validation subagent sharing the orchestrator's working tree inspects history read-only and never moves the tree's branch or HEAD, plus the concurrency-artefact note (shared-fixture race; not-yet-committed-sibling flag). Project-agnostic (the #866 incident lineage stays in the project surfaces, not the pack body). Pack 1.61.4 to 1.61.5 (patch; no new rule or skill) with a version-history row.
- [`.claude/CLAUDE.md`](../CLAUDE.md): the §3.59 forward-pointer added in #870 (which read "the pack half of this codification ... is TODO §3.59") reworded to note the pack half landed in #871, the §N-orphan cross-file cleanup for the section this PR closes.

### Verification

- Gate-37 parity: the subsection is byte-identical in both trees; the pack copy carries no project attribution (the #866 reference is deliberately omitted from the pack body, per the pack-hygiene zero-project-flavour convention).
- Derived artefacts regenerated after the pack README Version bump.
- Skeptical pre-push verifier (substantive tier; read-only git): gate-37 parity byte-identical (both trees), pack project-agnosticism clean (no #866 or project token in the pack subsection or the 1.61.5 history row), rule accurate and coherent. Caught TWO §N-orphan defects from this PR's own §3.59 closure, both FIXED pre-push: (1) [HIGH, gate-18-blocking] the new §3.60 item carried bare `§3.59` references that no longer resolve after the §3.59 heading was rotated to DONE, reworded to name the codification by description plus PR numbers; (2) [gate-blind] the CLAUDE.md forward-pointer added in #870 ("is TODO §3.59") was stale after the close, reworded to "landed in #871". A whole-repo grep confirmed zero residual `§3.59` in gated surfaces. All other axes clean; the gate-36/50 concurrency artefacts did not fire this run.
- Batches PR #870's `/validate-pr` and `/retro` rows.
- Closes TODO §3.59 (project surfaces in #870 plus this pack half); rotated to the DONE ledger. The secondary concurrent-suite fixture-race observation from §3.59 is spun off as the new TODO §3.60 (a per-process fixture-tempdir tooling fix, non-urgent), rather than falsely bundled into the close.

### Discipline observation

Completes §3.59, the read-only-git codification, across both the project surfaces (#870) and the distributable pack (#871). The rule's motivating incident (#866) is a project fact recorded in the project surfaces and the improvement-log; the pack body states the discipline project-agnostically.

## 2026-07-13, Library Version 2026.07.358, PR #870

Codify the read-only-git rule for validation and verifier subagents (TODO §3.59, project surfaces). Prevents the #866 shared-tree branch-collision from recurring.

### Changed

- [`.claude/commands/validate-pr.md`](../../.claude/commands/validate-pr.md) and [`.claude/commands/validate.md`](../../.claude/commands/validate.md): the Subagent-A / fan-out dispatch steps now carry a read-only-git constraint, dispatched subagents inspect version history read-only (`git show` / `git diff` / `git log`) and MUST NOT `git checkout` / `switch` / `reset` / `stash` on the shared working tree (the orchestrator may be on a concurrent feature branch), plus a note that a transient `tests/tmp` regression FAIL or a gate-50 not-yet-batched-later-PR flag is a concurrent-run artefact.
- [`.claude/CLAUDE.md`](../CLAUDE.md): a standing read-only-git-subagent note at PR-workflow step 5a, referencing the #866 collision.
- [`TODO.md`](../../TODO.md) §3.59 narrowed: the project surfaces are done here; the pack-distribution half (the `ai-assistant-workflow-disciplines` rule, both trees) remains.

### Verification

- The #866 collision (a /validate-pr subagent's `git checkout` switched the orchestrator's branch, mis-branching a commit onto local `main`; caught fail-loud at PR-create, repaired, remote `main` never polluted) is the motivating incident, recorded in the #866 /retro.
- Project-surface-only change (`.claude/` command stubs + CLAUDE.md + TODO); no corpus-document body, no pack rule, no gate wiring, so no per-document version bump, taxonomy regeneration, or gate-37 parity concern.
- Skeptical pre-push verifier (substantive tier): NO defect (refutation exhausted). The read-only-git rule is accurately stated on all three surfaces (no `checkout`/`switch`/`reset`/`stash`; use `git show`/`git diff`/`git log`), the #866 incident description is faithful to the improvement-log ledger, and the note forbids only branch/HEAD-moving commands (the stubs' legitimate read-only `git diff`/`git log` survive, no contradiction). Confirmed `.claude`-only scope (`git diff --name-only main` = the two command stubs, CLAUDE.md, the `.working` records, TODO, README, CHANGELOG; NO corpus doc, pack file, or generated taxonomy/portal change), §3.59 correctly narrowed (project surfaces done, pack half remaining, no false DONE rotation), bookkeeping clean, gate 44 (paired-skill step-parity) unaffected by the in-step prose, 69/69 standalone.
- Batches PR #869's `/validate-pr` and `/retro` rows.

### Discipline observation

Lower-accuracy-risk process codification, a deliberate pivot from the citation-attribution work (which drew 2 MEDIUM + 2 LOW verifier catches across the four EDPB bundles, all corrected) to process cleanup after completing the EDPB `lc` cluster. The pack-distribution half is left as the narrowed §3.59 for a fresher moment, since it involves gate-37 parity plus a pack version bump across the both-trees rule.

## 2026-07-13, Library Version 2026.07.357, PR #869

Reference-breadth apply (TODO §3.57), bundle 4 (the last held-verifiable EDPB `lc` High row): cite EDPB Guidelines 9/2022 in the breach-response procedure. Completes the EDPB privacy-guideline cluster (4/2019, 05/2020, 01/2022, 9/2022).

### Changed

- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md): cited **EDPB Guidelines 9/2022 on personal data breach notification (Version 2.0, adopted 28 March 2023)** in the `### 6.3` Article 33(2) note (the "becoming aware" doctrine and 72-hour clock, and the processor-to-controller Article 33(2) obligation) and the `## 12` EU/UK framework-alignment row. Confirmed not already cited. Version 1.4.28 to 1.4.29.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a register row for EDPB 9/2022 (Version 2.0, 2023-03), soft-law supervisory-guidance scope. Version 1.5.25 to 1.5.26.

### Verification

- Both attributions were read against the held source this turn: the "becoming aware / without undue delay / not later than 72 hours" doctrine (held paragraph 35, line 467) and the Article 33(2) processor-becomes-aware obligation (held paragraph 44, line 550).
- Version: v2.0 (28 March 2023, adopted after public consultation); v1.0 (10 October 2022) was an updated version of the Article 29 Working Party guidelines WP250 rev.01, issued for a targeted public consultation. The superseded cell states v1.0's date and WP250-rev.01 lineage exactly as the held version-history records them (verified against the held source at line 36, not a catalogue summary).
- Currency: held at v2.0; ref-catalogue `last_checked` 2026-07-12; not re-verified upstream this turn (recorded as the register Last-verified date).
- Confirmed the procedure did not already cite EDPB 9/2022 (the only prior "EDPB" mention is a body reference in the §6.2 table); artefacts regenerated after the two per-document Version bumps.
- Skeptical pre-push verifier (substantive tier; citation-accuracy-focused, read-only git): citation content CLEAN, both attributions verbatim-supported in the held source (the "becoming aware / without undue delay / not later than 72 hours" doctrine at held paragraph 35, line 467; the Article 33(2) processor-becomes-aware obligation at held paragraph 44, line 550), with the 72-hour controller clock and the processor obligation kept correctly distinct (no mis-coupling this bundle). Version accurate; register row well-formed; uncited before; no dashes or path-spans. One LOW prose-imprecision it flagged, the Verification clause implied the held version-history lacked a v1.0 date, but it records 10 October 2022 (held line 36); corrected here, and the register superseded cell now states that verified date. The #868 QA rows it flagged as pending were added after it ran (both present; gate 50 clears).
- Batches PR #868's `/validate-pr` and `/retro` rows.

### Discipline observation

Bundle 4 completes the held-verifiable EDPB `lc` cluster. The two lessons from bundles 2 and 3 (no register-phrasing pattern-match; verify each attribution's semantic-fit coupling against the held text) were applied at authoring: the "becoming aware" and Article 33(2) attributions were coupled exactly as the held source couples them (paragraphs 35 and 44), and the v1.0 superseded cell asserts no date the held version-history does not give. The §3.57 version-sensitive `[V]` jurisdiction rows and the stale / recycled scratch deliveries remain routed to the maintainer.

## 2026-07-13, Library Version 2026.07.356, PR #868

Reference-breadth apply (TODO §3.57), bundle 3 of the EDPB privacy cluster: cite EDPB Guidelines 01/2022 (right of access) in the data-subject-rights procedure.

### Changed

- [`privacy/procedure-data-subject-rights-management.md`](../../privacy/procedure-data-subject-rights-management.md): cited **EDPB Guidelines 01/2022 on data subject rights, Right of access (Version 2.1, 30 May 2024; adopted 28 March 2023)** at `### 6.3 Redaction of third-party data` (the Article 15(4) third-party-rights limit, applied by redaction) and `### 7.2 Article 12(5) assessment checklist` (the manifestly-unfounded-or-excessive assessment and the controller's burden), and added it to the `## 11 Framework alignment` "Access and transparency" row. Confirmed not already cited. Version 1.6.7 to 1.6.8.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a register row for EDPB 01/2022 (Version 2.1, 2024-05), soft-law supervisory-guidance scope. Version 1.5.24 to 1.5.25.

### Verification

- Each attributed element was read against the held source this turn: scope of the right of access (held lines 112 to 113), "copy" as the main modality plus the layered approach (141, 148), the Article 15(4) third-party-rights limit (177), and Article 12(5) manifestly unfounded or excessive (185).
- Version accuracy corrected against the held version-history (not the catalogue summary): v1.0 = 18 January 2022 (for public consultation), v2.0 = 28 March 2023 (adoption after consultation), v2.1 = 30 May 2024 (minor corrections). The catalogue's "v2.1 adopted 28 March 2023" conflates v2.0's adoption date; the register row and the citation use the held version-history's accurate framing. This is the bundle-2 lesson applied directly, verify the held version-history rather than trusting a catalogue summary or pattern-matching an adjacent guideline.
- Currency: held at v2.1; ref-catalogue `last_checked` 2026-07-12; not re-verified upstream this turn (recorded as the register Last-verified date).
- Confirmed the procedure did not already cite EDPB 01/2022 (grep clean at apply); artefacts regenerated after the two per-document Version bumps.
- Skeptical pre-push verifier (substantive tier; citation-accuracy-focused, read-only git): core citation accuracy SUPPORTED (Art 15(4) at held line 177, "copy" modality 141, layered approach 146-151, Art 12(5) + controller's burden 185-193, all confirmed against the held source) and version accuracy CONFIRMED against the held version-history (v1.0 18 January 2022 public consultation, v2.0 28 March 2023 adoption, v2.1 30 May 2024 minor corrections; the catalogue "v2.1 adopted 28 March 2023" conflation correctly avoided). ONE MEDIUM caught and FIXED pre-push: the §6.3 inline prose wrongly COUPLED the guideline's "layered approach" (a comprehension modality for large data sets, held 146-151) to the Article 15(4) third-party reconciliation function, which the source assigns to partial redaction (held 182-184); reworded to attribute the limit to redaction-not-refusal and drop the mis-coupling (the register row and this entry's Changed bullet had already listed the two correctly as separate scope items). All bookkeeping clean; 69/69 standalone.
- Batches PR #867's `/validate-pr` and `/retro` rows.

### Discipline observation

Bundle 3 of the EDPB cluster, one document per PR. The held-version-history read caught a catalogue-vs-document version discrepancy (v2.1 is the 30 May 2024 minor-corrections revision, not the 28 March 2023 adoption), the direct payoff of the bundle-2 superseded-cell lesson: on version-bearing citations, the held document's own version-history is authoritative over a catalogue summary. Bundle 4 (breach, EDPB 9/2022) follows as its own PR; the version-sensitive `[V]` jurisdiction rows remain routed to the maintainer.

## 2026-07-13, Library Version 2026.07.355, PR #867

Reference-breadth apply (TODO §3.57), bundle 2 of the EDPB privacy cluster: cite EDPB Guidelines 05/2020 in the consent-management framework.

### Changed

- [`privacy/framework-consent-management.md`](../../privacy/framework-consent-management.md): cited **EDPB Guidelines 05/2020 on consent under Regulation 2016/679 (Version 1.1, adopted 4 May 2020)** in the `## Validity standard` section (the conditionality and unambiguous-indication elements) and the `## Cookie consent under ePrivacy` paragraph (scrolling and continued browsing failing the unambiguous-indication standard), and added a `## Framework alignment` table row. Confirmed not already cited. Version 1.0.7 to 1.0.8.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a register row for EDPB 05/2020 (Version 1.1, 2020-05), soft-law supervisory-guidance scope. Version 1.5.23 to 1.5.24.
- [`TODO.md`](../../TODO.md) §3.59: codify the read-only-git rule for validation / verifier subagent briefs (the process fix for the #866 branch-collision, where a subagent's `git checkout` on the shared tree mis-branched a commit; now briefed read-only per dispatch, this item makes it durable).

### Verification

- The document's Validity-standard elements (freely given / no bundling / no pre-ticked boxes; unambiguous / inactivity-not-consent) and its cookie section (pre-ticked, scroll-to-consent, and consent walls not valid) map to EDPB 05/2020's conditionality (paragraphs 38 to 41), unambiguous-indication requirement (paragraph 86), and scrolling example (example 16), confirmed against the held source's revision record this turn.
- Currency: held at v1.1; the ref catalogue `last_checked` is 2026-07-12 (the worklist `lc` flag); an adopted-final guideline, not re-verified upstream this turn (recorded as the register Last-verified date).
- Confirmed the consent framework did not already cite EDPB 05/2020 (grep clean at apply). Derived artefacts regenerated after the two per-document Version bumps.
- Skeptical pre-push verifier (substantive tier; refute-briefed, citation-accuracy-focused): core citation accuracy SUPPORTED on all axes, the three attributed EDPB 05/2020 elements each confirmed against the held source (conditionality / bundling-not-freely-given at held paras 25 to 38; unambiguous clear-affirmative-act with inactivity-and-pre-ticked-boxes-not-consent at held lines 802 to 803; scrolling and continued browsing not valid at held Example 16, line 855), version consistent (v1.1, adopted 4 May 2020, matching the catalogue), uncited before. ONE MEDIUM defect CAUGHT and FIXED before push: the register superseded-cell wrongly stated v1.0 was "for public consultation" (an incorrect pattern-match from the #866 4/2019 two-stage case), but the held version-history shows v1.0 was the 4 May 2020 adoption and v1.1 the 13 May 2020 formatting corrections; the cell was corrected to that, grounded in the verifier's quoted held version-history. The gate-36 audit FAIL the verifier observed was a concurrent-test-run race on the shared `tests/tmp` fixtures (re-run standalone clean), not a #867 defect.
- Batches PR #866's `/validate-pr` and `/retro` rows.

### Discipline observation

Bundle 2 of the EDPB cluster, one document per PR (accuracy-critical citation work, verified against the held source). Bundles 3 (access, EDPB 01/2022) and 4 (breach, EDPB 9/2022) follow as their own PRs; the version-sensitive `[V]` jurisdiction rows remain routed to the maintainer's fresh-context / high-assurance category.

## 2026-07-13, Library Version 2026.07.354, PR #866

Reference-breadth apply (TODO §3.57), bundle 1 of the EDPB privacy cluster: cite EDPB Guidelines 4/2019 in the privacy-by-design framework. The reference-breadth new-ingest worklist (scratch #163, delivered 2026-07-12) flagged that the privacy-by-design framework operationalizes GDPR Article 25 but did not cite the European Data Protection Board's authoritative Article 25 guideline, which is held in `grc_library_ref`.

### Changed

- [`privacy/framework-privacy-by-design.md`](../../privacy/framework-privacy-by-design.md): cited **EDPB Guidelines 4/2019 on Article 25 Data Protection by Design and by Default (Version 2.0, adopted 20 October 2020)** in the `## Legal basis: GDPR Article 25` section (as the authoritative supervisory interpretation, the effective-implementation duty, the design and default elements, and continual review of the measures' effectiveness) and added a row to the `## Framework alignment` table. Confirmed not already cited. Version 1.0.2 to 1.0.3.

### Added

- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md): a canonical-citations register row for EDPB Guidelines 4/2019 (Version 2.0, 2020-10), under the register's soft-law supervisory-guidance scope, grouped with the other EDPB guideline rows. Version 1.5.22 to 1.5.23.

### Verification

- The citation is grounded in the held EDPB 4/2019 full-text in `grc_library_ref`: the attributed elements ("effective implementation of the data-protection principles", the "design and default elements", and "regularly reviewing the effectiveness of the chosen measures and safeguards") were read against the held text this turn and match.
- Source hold and currency: EDPB 4/2019 is held at the cited v2.0; the ref catalogue's `last_checked` confirmed the held adopted-final edition current on 2026-07-12 (the worklist `lc` flag). It was NOT re-verified upstream this turn (an adopted-final guideline, stable since 2020; currency rests on the 2026-07-12 ref-base confirmation, recorded as the register row's Last-verified date rather than a fabricated today's-date verification).
- Confirmed the privacy-by-design framework did not already cite EDPB 4/2019 (grep clean at apply).
- Derived artefacts regenerated after the two per-document Version bumps (taxonomy, then portal and scorecard).
- Skeptical pre-push verifier (substantive tier; refute-briefed, citation-accuracy-focused): NO defect across all 8 axes. Citation accuracy SUPPORTED, the independent verifier re-read the held EDPB 4/2019 source and confirmed every attributed element appears verbatim or near-verbatim (held lines 103, 104, 108-109, 107-108): "effective implementation of the data protection principles", "Article 25 prescribes both design and default elements", "regularly reviewing the effectiveness of the chosen measures and safeguards", and "before processing, and also continually at the time of processing". Version consistent (v2.0 adopted 20 October 2020 across the inline cite, the table row, the register row, the held title page, and the catalogue `checked_edition`). Confirmed uncited before. Register row well-formed and honest (Last-verified 2026-07-12 mirrors the catalogue `last_checked`; the superseded v1.0 cell matches the held version history without fabricating a date). All 69 gates pass. The two process notes (commit-before-guard; fill this verdict slot) were handled before push.
- Batches PR #865's `/validate-pr` (clean) and `/retro` rows.

### Discipline observation

Reference-breadth apply, first bundle, narrowed to ONE document (one EDPB citation plus its register anchor) rather than the whole four-document EDPB cluster the §3.57 plan bundles, for exhaustive per-citation verification on accuracy-critical citation work. The worklist is research (a hypothesis); the citation was authored only after re-reading the target section, confirming it was uncited, and verifying the attributed elements against the held source text. The remaining three EDPB `lc` rows (consent 05/2020, access 01/2022, breach 9/2022) and the version-sensitive `[V]` jurisdiction-annex rows follow as their own bundles; the `[V]` rows need upstream currency confirmation and are the maintainer's fresh-context / high-assurance category.

## 2026-07-13, Library Version 2026.07.353, PR #865

Change-tracking two-file-split how-to harmonized to the compact go-forward format (the #864 follow-on), plus a recorded delivery-pipeline reconciliation.

### Changed

- [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md) and its project-side mirror copy (gate-37 parity): the "In the root file" step of the two-file-split how-to now points at the compact one-line form as the recommended go-forward root-summary shape (cross-referencing the current-week-model section that #864 flipped), replacing the bare "write the lead paragraph only" instruction that lagged the 1.61.3 model-section flip. This closes the #864 `/validate-pr` informational note (the how-to-lag observation). Pack 1.61.3 to 1.61.4 (patch; no new rule or skill) + version-history row.

### Added

- [`TODO.md`](../../TODO.md) §3.58 (paired with a [`pending-decisions.md`](../../.working/pending-decisions.md) entry for maintainer disposition): a delivery-pipeline reconciliation item. When the post-3b overnight queue reached the "apply-ready scratch deliveries" tier, the pipeline proved not cleanly apply-ready: TODO-number recycling (§1.2, §3.15, §3.19) makes the token-based delivery mapping unreliable, the `worker-20260703-a` deliveries are 10 days old, and `changelog-root-reformat-build` is already consumed (built #855 through #862). Auto-applying misnumbered or drifted deliveries unattended was declined (Integrity over Speed); the reconciliation and per-delivery APPLY / SUPERSEDE / DISCARD disposition is routed to the maintainer.

### Verification

- Gate-37 parity preserved: the how-to edit is byte-identical in both change-tracking rule copies; the overlay block is untouched.
- Line 169 (the no-detailed-mirror fork option's "lead-paragraph summaries only") deliberately left unchanged: it describes a fork variant, not the main convention.
- Derived artefacts regenerated after the pack README Version bump (taxonomy, then portal and scorecard).
- Skeptical pre-push verifier (substantive tier; refute-briefed): NO defect across all 7 axes. Gate-37 parity byte-identical on the how-to edit (md5 match); the load-bearing "do NOT carry the structured sections into the root file" invariant preserved verbatim and the "see the current-week-model section above" cross-reference resolves; pack project-agnosticism clean (no attribution in the edit or the 1.61.4 history row); every §3.58 / pending-decisions claim independently corroborated (current §3.15 = MITRE ATLAS and §3.19 = worker-provenance-link, so the recycled-number claim holds; §3.58 is genuinely new; `changelog-root-reformat` is consumed, its tool built #855; the delivery-status tool output matches the record); version/bookkeeping consistent; no dashes or unlinked path-spans. The commit-before-history-aware-checks note is handled by the standard commit-then-guard flow.
- Batches PR #864's `/validate-pr` (clean; 1 informational note, which is this PR's how-to fix) and `/retro` rows.

### Discipline observation

Paired-surface-lag follow-through: #864 flipped the model-description surface (the current-week-model section) but not the paired authoring how-to (the two-file-split step); #864's own `/validate-pr` caught the lag as an informational note, and this PR closes it. Tiering held at substantive (one refute-briefed verifier), not the high-assurance harness: a one-line how-to harmonization plus a backlog record rests on no gate-blind correctness property and no delicate scale, so the harness's three-condition trigger is not met. This tiering judgement (substantive rather than the literal five-stage harness for the small post-wave cleanups) is being surfaced to the maintainer for confirm-or-redirect.

## 2026-07-13, Library Version 2026.07.352, PR #864

Change-tracking authoring-convention flip: the compact one-line root-entry format is now documented as the standard go-forward shape. The 3b plain-language wave (#855-#862) converted the whole root CHANGELOG back-catalogue to the compact `**date | version | PR** - summary` form; this PR reconciles the guidance to that reality (the prior text called the compact form "a distinct reformat step the project may choose ... NOT adopted yet").

### Changed

- [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md) and its project-side mirror copy (gate-37 parity): the compact one-line root-entry format is documented as the recommended go-forward shape for the root file once entry volume makes the lead-paragraph-per-entry form unwieldy, replacing the "distinct reformat step the project may choose; until then keep the lead-paragraph form" framing. The pack rule stays project-agnostic (a project MAY adopt it; the baseline lead-paragraph form remains valid), and reformatting an existing back-catalogue is still a distinct one-time step.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) detailed-mirror current-week-sweep close-out bullet: the compact format is now marked ADOPTED (the 3b wave converted the back-catalogue; every new root entry uses the one-line form), replacing "NOT adopted yet ... root entries keep the header-plus-lead form". TODO 3.16's only residual is the deferred maintainer-gated git-history collapse.
- Pack metadata Version 1.61.2 to 1.61.3 (patch; no new rule or skill) with a new 1.61.3 version-history row.

### Verification

- Gate-37 parity preserved: the two change-tracking rule copies received the identical line-37 edit; the project copy's overlay block is untouched.
- Line 20 (the two-file-split "lead-paragraph summary" description) deliberately left unchanged: the rule reads coherently as a lead-paragraph baseline plus the compact one-line recommended go-forward as volume grows, so no cascade of terminology edits was needed.
- Derived artefacts regenerated after the pack README Version bump (taxonomy, then portal and scorecard).
- Skeptical pre-push verifier (substantive tier; refute-briefed): NO content defect across all 8 axes. Gate-37 parity confirmed byte-identical on the edited line between the two rule copies; class-definition coherence preserved (the compact form is a conditional rendering of the same summary, not a new content class, so the summary-vs-sections split holds everywhere); pack project-agnosticism clean (no project attribution in the rule-body edit or the new 1.61.3 version-history row); the CLAUDE.md "ADOPTED" claim independently confirmed true (0 full-body per-entry headers remain in the root CHANGELOG); version/bookkeeping correct; no dashes or unlinked path-spans in added lines. The two procedural findings were resolved before push (this verdict replaced the placeholder; the staged work was then committed so the pre-push guard exercises the history-aware gates 40/31/45 and D2/D4/D6 against the real committed diff).
- Batches PR #863's `/validate-pr` and `/retro` rows.

### Discipline observation

Convention-catches-up-to-reality edit: the compact format was already the live root shape after the 3b wave, but the change-tracking rule and the CLAUDE.md close-out bullet still described it as deferred and not-yet-adopted. This PR reconciles the documented convention to the shipped reality, the paired-surface-lag guard applied to a convention rather than a value.

## 2026-07-13, Library Version 2026.07.351, PR #863

SP 800-154 "held source" wording accuracy (TODO §1.2, a recycled number; pack-hygiene Phase-4 routed, protected-file class). The `/reference-audit` guidance used NIST SP 800-154 as its motivating example and described it as a "held source" and as a source that "sits in the reference base". SP 800-154 was never finalized (a withdrawn NIST draft) and is not held in `grc_library_ref` (re-verified this turn: absent from the ref catalogue, indexes, and disk). Reframed as a relevant-but-unavailable source that *surfaced* the general "held but unused" class; the class definition itself (an authoritative held source no corpus document engages, and the reverse) was already accurate and is unchanged. The first post-3b protected-cleanup PR under the maintainer's 2026-07-13 overnight authorization.

### Changed

- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Reference-breadth cadence`: the class-definition parenthetical no longer calls SP 800-154 "an authoritative held source". The class is now defined generically (an authoritative source the reference base holds that no corpus document engages, and the reverse), and a following sentence frames the SP 800-154 lesson accurately as a relevant-but-unavailable source (never finalized).
- [`.claude/commands/reference-audit.md`](../../.claude/commands/reference-audit.md): "the gate-blind SP 800-154 class, 'held but unused'" reworded to "the gate-blind 'held but unused' class the SP 800-154 lesson surfaced", so the class is no longer named after SP 800-154 and SP 800-154 is no longer implied to sit in the reference base.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): the skill-tree line ("(the SP 800-154 lesson)" to "(surfaced by the SP 800-154 lesson)") and the 1.57.0 version-history row (the "an authoritative held source" attribution corrected; SP 800-154 named as a relevant-but-unavailable source, never finalized). Pack metadata Version 1.61.1 to 1.61.2 (patch; no new rule or skill) with a new 1.61.2 version-history row.

### Verification

- SP 800-154 hold status re-verified this turn: absent from the `grc_library_ref` catalogue, its indexes, and the acquisition queue, and absent from disk (a name search returned nothing). Confirms the not-held premise the correction rests on.
- Bare-token-width grep for "held source" across all scanned file types confirmed the remaining occurrences (the root changelog "deepened against held sources", the rule-provenance register and the claim-fit skill "against the held source", the deep-assessment skill "held source texts", and the reference-audit skill body) are all accurate uses (sources the base genuinely holds), not SP 800-154, and are left unchanged.
- The distributable reference-audit skill body was confirmed already genericized (no "SP 800-154" mention; the class defined accurately), so no pack-skill body edit was needed.
- Derived artefacts regenerated after the pack README Version bump (taxonomy first, then portal and scorecard).
- Skeptical pre-push verifier (substantive tier; refute-briefed): NO substantive defect across all 7 axes (reframe accuracy, class-definition coherence, completeness at bare-token / all-file-type width, the not-held premise re-confirmed in `grc_library_ref`, version/bookkeeping integrity, dashes/paths, TODO/DONE rotation). The verifier independently confirmed SP 800-154 appears in the ref base only as citations inside other held NIST docs, never as its own held source, and that the distributable reference-audit skill body is already genericized (zero SP 800-154 mentions).
- Batches PR #862's `/validate-pr` (clean, 0 findings) and `/retro` rows.

### Discipline observation

Semantic-fit correction on a protected pack surface: the inaccuracy was not the class (real and correctly defined) but its EXEMPLAR. SP 800-154 is a poor exemplar of "held but unused" because it was never held; the fix decoupled the exemplar from the class rather than editing the class. The recycled §1.2 number (old §1.2 = per-document ISO Annex A validity, gate 58, closed in #509) is cross-referenced in the DONE entry so the two are not conflated. Tiering judgement: substantive tier (one refute-briefed verifier), not the high-assurance harness, because the change is 4 hand-verifiable wording edits resting on a single checkable fact (SP 800-154 not held), failing the harness's "delicate scale" trigger.

## 2026-07-13, Library Version 2026.07.350, PR #862

CHANGELOG plain-language rework, stage 3b batch 7, the FINAL batch (TODO 3.16). Completes the wave: every root CHANGELOG entry is now a compact one-line plain-language summary.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the last 119 full-bodied root entries (PR #132 down to #38, plus the 34 earliest PR-less releases down to the initial public release) collapsed to jargon-free one-line summaries. With this batch the entire history is converted; no full-body entries remain. Full bodies preserved in this detailed mirror + git history.
- Root [`CHANGELOG.md`](../../CHANGELOG.md) intro: removed the now-obsolete transitional clause ("many of the older entries still carry their original longer form"), since the conversion is complete.
- Library CalVer `2026.07.349` to `2026.07.350`; README Version `1.9.710` to `1.9.711`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content), transposition-guarded, with the 34 PR-less early entries keyed by their unique date+version and the initial-release entry preserving the CC BY-SA 4.0 first-public-release fact. A skeptical faithfulness verifier checked the substantive entries and the PR-less/initial-release cluster against their live bodies and scanned all 119 for leakage. Verdict: NO defect, COMPLETE coverage (all 119 verified, not sampled, incl. every PR-less entry and the initial release); PR-less matching + transposition cleared row-by-row through the backfill cluster; initial release preserves "first public release" + CC BY-SA 4.0; jargon/dash/path/"gate" scan clean. One non-finding tightened before apply (#73's "collection-drift detector" reworded to "detector for new candidate collections" to match the tool's actual function). Applied via the deterministic self-verifying script. Batches #861's `/validate-pr` (0 findings) + `/retro`.

### Notes

- **The stage-3b plain-language wave (TODO 3.16) is complete** across seven batches (#856, #857, #858, #859, #860, #861, #862): every historical root CHANGELOG entry now carries a compact `date | version | PR` header plus a short plain-language summary a general reader can follow, with the full maintainer-grade detail retained in this mirror and in git history. TODO 3.16's reformat-and-compression scope is complete; the item is narrowed to its one deferred, maintainer-gated residual (a git-history collapse for true clone / fork cleanliness, a protected-branch rewrite left for an explicit maintainer decision), not rotated to DONE. This PR receives its own post-merge `/validate-pr` + `/retro`, batching into the next PR.

## 2026-07-13, Library Version 2026.07.349, PR #861

CHANGELOG plain-language rework, stage 3b batch 6 (TODO 3.16). Batch 6 of ~7.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the next 120 root entries (PR #254 down to #133, the non-existent #217 and #136 skipped) collapsed from full bodies to jargon-free one-line summaries appended to the compact header, blank-line-separated. Full bodies preserved in this detailed mirror + git history. (Batch count and range stated exactly.)
- Library CalVer `2026.07.348` to `2026.07.349`; README Version `1.9.709` to `1.9.710`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content), transposition-guarded (each summary written against its own header's body, the explicit guard after the batch-5 swap). A skeptical faithfulness verifier sampled the substantive entries and specifically re-checked the duplicate-version backfill cluster (#169-#175, the swap-risk spot) against their live bodies, and scanned all 120 for leakage. Verdict: NO misrepresentation (the #169-#175 duplicate-version cluster explicitly cleared as swap-free; ~50 entries sampled, all faithful on scope/counts/standard-and-GDPR-article attributions). One accepted LOW note: 8 summaries use the plain-English word "section" (a README section, a charter section), which is adopter-comprehensible and not the banned "§N / TODO section" internal-reference token, so no fix. Applied via the deterministic self-verifying script. Batches #860's `/validate-pr` (0 findings) + `/retro`.

### Notes

- This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 7 (the final batch, which includes the earliest PR-less entries).

## 2026-07-13, Library Version 2026.07.348, PR #860

CHANGELOG plain-language rework, stage 3b batch 5 (TODO 3.16). Batch 5 of ~7.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the next 120 root entries (PR #374 down to #255) collapsed from full bodies to jargon-free one-line summaries appended to the compact header, blank-line-separated. Full bodies preserved in this detailed mirror + git history. (Batch count and range stated exactly, per the measured-not-inferred count discipline.)
- Library CalVer `2026.07.347` to `2026.07.348`; README Version `1.9.708` to `1.9.709`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content); subagent self-scan confirmed no dashes, no "gate" word, no jargon/path-spans. A skeptical faithfulness verifier sampled the substantive entries (the CPPA-to-PIPEDA scrub, CSA Cloud Controls Matrix reconciliations, TLS 1.3 migration, risk-vocabulary harmonizations, retention reconciliations, compliance-matrix domain expansions) against their live bodies and scanned all 120 for leakage. Verdict: 1 HIGH defect, fixed before apply, the #259 and #260 summaries were transposed (the substantive risk-scoring-scale realignment #260 had been mislabeled internal "no published document changed", and the internal overnight-run-init #259 carried #260's substantive text); swapped back to the correct pairing. No other defect (56 entries sampled, all other summaries faithful on scope/counts/attribution; 120-summary jargon/dash/path/"gate" scan clean). This is the catch the verify-before-apply gate exists for: a substantive corpus change would otherwise have shipped labelled "no published document changed". Applied via the deterministic self-verifying script. Batches #859's `/validate-pr` (0 findings) + `/retro`.

### Notes

- This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 6.

## 2026-07-13, Library Version 2026.07.347, PR #859

CHANGELOG plain-language rework, stage 3b batch 4 (TODO 3.16). Batch 4 of ~7.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the next 120 root entries (PR #495 down to #375, the abandoned #422 having no entry) collapsed from full bodies to jargon-free one-line summaries appended to the compact header, blank-line-separated. Full bodies preserved in this detailed mirror + git history. (Per the measured-not-inferred count discipline, this entry states the exact batch count and range rather than a drift-prone cumulative running total.)
- Corrected the #858 detailed-mirror entry's cumulative figure from the batch-arithmetic "360 of ~838" to the measured "363 of 842" (the count class the #858 `/validate-pr` flagged).
- Library CalVer `2026.07.346` to `2026.07.347`; README Version `1.9.707` to `1.9.708`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content); the subagent's own scan confirmed no dashes, no "gate" word, no jargon/path-spans. A skeptical faithfulness verifier sampled the substantive entries (compliance-matrix domain fills, control-code/citation/date corrections, the FR-48 renumbering run, the Risk-Committee naming fixes) against their live bodies and scanned all 120 for leakage. Verdict: no faithfulness misrepresentation (65 PRs sampled, all faithful), 1 LOW hygiene finding (the #484 summary carried "decision gates", legitimate M&A terminology but the banned literal "gate" token), reworded to "decision points" before apply. Applied via the deterministic self-verifying script. Batches #858's `/validate-pr` (1 LOW note, fixed here) + `/retro`.

### Notes

- This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 5.

## 2026-07-13, Library Version 2026.07.346, PR #858

CHANGELOG plain-language rework, stage 3b batch 3 (TODO 3.16), plus a maintainer-directed backlog expansion. Batch 3 of ~7.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the next 120 root entries (PR #615 down to #496) collapsed from full bodies to jargon-free one-line summaries appended to the compact header, blank-line-separated. 363 of 842 entries are now plain-language; #495 and older keep their full bodies pending later batches. Full bodies preserved in the detailed mirror + git history.
- [`TODO.md`](../../TODO.md) §4.5: broadened, at maintainer direction, from "fork-facing guidance + scripts for building an own reference base" to an **adopter reference-base specification** that an adopter's AI assistant can follow to assemble its own base (adopters do not receive `grc_library_ref`). Now leads with the AI-buildable spec, an enumerated public-source list, a suggested paid-source list (budget-permitting), and, as the headline value, the corpus-to-sources relevance map (which standards, legislation, and frameworks bear on each corpus document, already curated and gate-kept, so a trusting adopter need not rediscover it).
- Library CalVer `2026.07.345` to `2026.07.346`; README Version `1.9.706` to `1.9.707`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content). A skeptical faithfulness verifier sampled the substantive entries (incl. the FR-48 section-renumbering run, retention reconciliations, citation/version corrections, the DPO role split) against their live bodies and scanned all 120 for jargon/dash/path-span leakage. Verdict: 4 LOW findings, no high or medium: three scope/attribution imprecisions (a "five risk documents" over-generalization, an understated domain list, a wrong "continuity" domain) and one jargon leak (the word "gate"); ALL FIXED in the source summaries before the apply. The §4.5 edit was checked clean against the TODO-scanning gates (positional-token, gate-count-phrasing, staleness). Applied via the deterministic self-verifying script. Batches #857's `/validate-pr` (1 LOW note, fixed here: the root CHANGELOG intro's "a few of the oldest" undercounted the un-converted tail, reworded to "many of the older entries"; the detailed-mirror wording was already accurate) + `/retro`.

### Notes

- This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 4.

## 2026-07-13, Library Version 2026.07.345, PR #857

CHANGELOG plain-language rework, stage 3b batch 2 (TODO 3.16), plus the format-description intro updates the maintainer flagged. Batch 2 of ~7.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the next 120 root entries (PR #735 down to #616) collapsed from full bodies to jargon-free one-line summaries appended to the compact header, blank-line-separated. 240 of ~838 entries are now plain-language; #615 and older keep their full bodies pending later batches. Full bodies preserved here + in git history.
- Root [`CHANGELOG.md`](../../CHANGELOG.md) intro and this detailed mirror's intro: rewritten to describe the new compact one-line plain-language format (a `date | version | PR` header plus a short summary a general reader can follow), replacing the old "lead-paragraph summaries" description, with a note that the historical long tail is being converted in batches (maintainer-flagged).
- [`tools/lint-orphan-documents.py`](../../tools/lint-orphan-documents.py) (gate 26): added the root [`RESUME.md`](../../RESUME.md) manual entry point to the exempt set. The collapse removed the batch-2 CHANGELOG body that carried its only markdown-linked inbound reference, orphaning it; the file is a session-resume entry point reached by filename convention (like the other exempt root entry points), so relying on an incidental CHANGELOG link was fragile. Correct classification, not a gate weakening.
- Library CalVer `2026.07.344` to `2026.07.345`; README Version `1.9.705` to `1.9.706`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of verified content). A skeptical verifier body-compared all 32 substantive entries plus 17 internal, scanned all 120 for jargon/dash/path-span leakage (zero hits), and confirmed the high-stakes attributions (ISO/IEC 42001 vs 27001, PCI DSS 4.0.1, the Quebec 72-hour fabrication fix, Brazil resolution 19/2024, the never-finalized SP 800-154 to OWASP substitution, the MITRE ATLAS corpus-vs-pack split): NO DEFECT FOUND (no fix needed this batch). Applied via the deterministic, self-verifying migration script. Batches #856's `/validate-pr` (0 findings) + `/retro`.

### Notes

- This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 3. The change-tracking pack rule's authoring-convention description (documenting compact as the go-forward root shape) remains a deferred follow-up; the parsers accept both forms so mixed authoring is safe meanwhile.

## 2026-07-13, Library Version 2026.07.344, PR #856

CHANGELOG plain-language rework, stage 3b batch 1 (TODO 3.16). The first of ~7 batches: the newest 120 root CHANGELOG entries (PR #855 down to #736) had their long maintainer-grade bodies collapsed into a single-line, jargon-free summary appended to the compact header (`**date | version | PR #N** - summary`), blank-line-separated per the change-tracking compact-format spec. The full bodies remain in this detailed mirror and in git history. Internal/bookkeeping entries collapse to one terse sentence; adopter-facing/substantive entries to a fuller two-sentence summary (the maintainer-confirmed "compact + plain, flat, more detail on substantive" format).

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): 120 entries (#855..#736) collapsed to plain-language one-line summaries; bodies removed (preserved here + git history). Older entries (#735 and down) keep their full bodies pending later batches.
- Library CalVer `2026.07.343` to `2026.07.344`; README Version `1.9.704` to `1.9.705`.

### Verification

- Summaries drafted by a research subagent from the existing bodies (compression of already-verified content, not new claims), re-verified by the orchestrator (13 spot-checks) and a skeptical verifier (36-entry weighted sample). The verifier found the change mechanically sound (839 = 839 entries, contiguous #736..#855, every entry has a summary, no body left behind, no dashes, no jargon/path-span/token leakage) and 35/36 faithful; the one finding (a standard misattribution in the #831 summary, ISO/IEC 42001 vs 27001) was FIXED before apply. The apply used a deterministic, self-verifying script (refuses on any dropped/reordered entry, dash, or unlinked path-span). Batches #855's `/validate-pr` + `/retro` rows.

### Notes

- The deterministic apply helper lives in the session scratchpad (a one-time migration tool); the reviewable artefacts are the CHANGELOG diff and the drafted summaries. This PR receives its own post-merge `/validate-pr` + `/retro`, batching into batch 2.

