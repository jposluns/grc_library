# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

**Worker-provenance convention (decided 2026-07-23, TODO 3.19):** a reference to a scratch-side worker result or manifest is written as plain backticked text in a `repo:path` form (naming the scratch repo and the result file), never a cross-repo markdown link. A cross-repo relative link target resolves only against a fresh sibling checkout at `main`, not a stale local tree, and cross-repo links are un-gate-checkable; the plain-text form keeps the provenance readable and grep-able without the fragility.

## 2026-07-28, Library Version 2026.07.717, PR #1228

Resume close-out for the 2026-07-28 attended-autonomous session (the first substantive-QA PR after the migration PR1 #1227 merge). It records the loop-break `/validate` compensating control, consumes #1227's post-merge dual-family validate-pr and fixes its in-window findings, and carries the session-resume bookkeeping.

### Added
- **Sweep 128 loop-break `/validate`** ([`.working/validate-sweeps/history.md`](../validate-sweeps/history.md)): the dual-family corpus-wide `/validate` over the #1217..#1225 deltas, the compensating control for the #1226 session-closing handoff (which skips its trailing `/validate-pr`). PASS: zero in-window ordinary findings, all 78 gates green, gate 54 CSF-clean, all three #1225 asserted-clean surfaces corroborated; loop-break control for #1226 PASSES. A codex `byte-identical` wording note was dismissed via the claude gate-37 cross-check (the two rule trees differ only by the sanctioned PROJECT-OVERLAY block gate 37 strips); a claude out-of-window note about the stale `.ref` acquisition manifest was routed to TODO RB-8.
- **RB-8** ([`TODO.md`](../../TODO.md)): regenerate the reference-acquisition manifest ([`tools/build-reference-manifest.py`](../../tools/build-reference-manifest.py)) when the reference base is next touched (a low-severity generated-artefact refresh).
- **#1226 and #1227 merge-bypass rows** ([`.working/merge-bypass-log.md`](../merge-bypass-log.md)): back-filled from the observed CI state (a session-closing handoff has no following PR of its own session, so #1226's row surfaces once #1227 demotes it; #1227's is the standard write-after-merge).

### Changed
- **Gate 60 spec section-6 sentence** ([`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md), Version 1.17.38): #1227 narrowed gate 60's fail-closed stance (an absent default-lookup history is now a skip) but left the section-6 sentence reading `a missing... history record fails closed`. Reworded so a row-less, token-less, or present-but-undecodable record fails closed while an ABSENT default history is a skip. Caught by BOTH families of #1227's post-merge validate-pr (a paired surface my #1227 grep, scoped to `guardrail` adjacency, missed in the long section-6 line).
- **Gate-43 no-op regression test** ([`tests/test_linters.py`](../../tests/test_linters.py), `WorkingResolveNoOpTests`): re-scoped from the generic `skipped` substring (which appears in gate 43's NORMAL OK line too, so the case bound nothing; codex + claude both caught it and claude mutation-proved it) to a `0 of N` scanned-zero assertion that a removed default-resolver branch would fail.
- **Detailed-mirror #1227 gate-60 bullet**: corrected the `no test covers the absent-history case` claim (the `WorkingResolveNoOpTests` class added in the same PR does cover it).
- **Concurrency lease** ([`.working/session-state.md`](../session-state.md)): ACQUIRED for this session (attended-autonomous). Plus the #1227 validate-pr + retro rows and the resume-cursor advance to Sweep 128.

### Routed to migration PR2
- **Gate 60 present-but-UNREACHABLE fail-closed gap** (codex Medium): `resolve_working`'s `cand.exists()` returns False for a present-but-permission-denied path, so gate 60 skips instead of failing closed. Harmless pre-move; activates once the history lives in `_private/.working/`. PR2 must distinguish absent (skip) from present-but-unreadable (fail-closed) at the private location, per the `validate-inference-before-action` guard-input discipline. Recorded in the `grc_library_private` migration plan.

### Verification
- All 78 gates green (pre-push guard, both runners); taxonomy/portal/scorecard regenerated after the spec Version bump. The re-scoped gate-43 test was verified to fail under the no-op-branch-removed mutation (codex's and claude's exact refutation).
- Dual-family post-merge validate-pr for #1227: both families delivered, corroborated the two shared findings, and confirmed the six-gate rewiring correct.

## 2026-07-28, Library Version 2026.07.716, PR #1227

Migration PR1 continuation: the remaining six `.working/`-reading gates now resolve their inputs through `lint_common.resolve_working` (the #1225 foundation helper), completing the gate-rewiring half of the `.working/`->`grc_library_private/.working/` privacy migration. All nine `.working/`-reading gates (the three from #1225 plus these six) now degrade gracefully: on the maintainer's machine the private sibling supplies the file and the gate enforces in full; in public CI or an adopter clone the input is absent and the gate no-ops with an honest skip line rather than failing or silently scanning nothing. The content move (PR2) follows.

### Changed
- **Gate 50 bookkeeping-parity** ([`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py)): its five `.working/` inputs (validate-pr history, improvement-log, detailed CHANGELOG mirror, deep-assessment register, merge-bypass log) route through `resolve_working`; each dependent check no-ops INDIVIDUALLY and the run reports which checks it skipped, while the two PUBLIC checks (TODO/DONE rotation, version-history parity) always run. Check 1 (QA-cadence) is all-or-nothing across its two registers (a half-run would be a false-positive storm). The closing OK line now enumerates only the checks that ran, and includes Check 6 (merge-bypass parity), which the old line silently omitted.
- **Gate 59 CHANGELOG-mirror-parity** ([`tools/lint-changelog-mirror-header-parity.py`](../../tools/lint-changelog-mirror-header-parity.py)): the DEFAULT detailed-mirror lookup routes through `resolve_working` (no-op on absent); an EXPLICIT `--root` stays verbatim for the regression fixtures. (Maintainer decision 2026-07-28: keep the mirror, move this gate `_private`-side in a later step.)
- **Gate 78 number-permanence** ([`tools/lint-todo-number-permanence.py`](../../tools/lint-todo-number-permanence.py)): the DEFAULT [`.working/DONE.md`](../DONE.md) lookup routes through `resolve_working`; an absent ledger downgrades the recycled-number check (A) to a reported skip while the counter check (B) still runs against the public TODO.md. An EXPLICIT `--root` keeps its verbatim missing-file exit 2 (the `--root` mutates this module's REPO_ROOT, not lint_common's, so it must NOT route through the helper). (Maintainer decision: keep gate 78 as the `_private`-side backstop, option a.)
- **Gate 60 guardrail-cadence** ([`tools/lint-guardrail-cadence.py`](../../tools/lint-guardrail-cadence.py)): MAINTAINER-RATIFIED narrowing of the documented fail-closed stance. The DEFAULT history lookup routes through `resolve_working` and no-ops on absent; the docstring is amended so an UNREADABLE (present-but-broken) history still fails closed while an ABSENT history is a skip (an adopter clone never owed the review). The stance change is recorded in the docstring, and the new `WorkingResolveNoOpTests` class (see Verification) adds a case that binds the absent-history skip.
- **Gate 43 followup-ageing** ([`tools/lint-followup-ageing.py`](../../tools/lint-followup-ageing.py)): a DEFAULT `.working/`-prefixed target routes through `resolve_working`; a new `scanned` counter makes the closing OK line report how many targets it actually read rather than claiming a skipped target was scanned.
- **Gate 51 working-prose-hygiene** ([`tools/lint-working-prose-hygiene.py`](../../tools/lint-working-prose-hygiene.py)): the DEFAULT scan root routes through `resolve_working(".")` and no-ops with an honest OK line when the tree is absent, rather than silently scanning zero files (a false green). Also a latent-crash fix: a new `display_path` helper renders a finding's path repo-relative inside the repo and absolute when in the private sibling, so `relative_to(REPO_ROOT)` no longer raises `ValueError` on every finding once the scanned files live in `_private`.

### Verification
- All 78 gates pass (`tools/run_all_audits.sh`); the six gates' existing regression classes pass, PLUS a new `WorkingResolveNoOpTests` class (7 cases) that PERSISTENTLY binds the DEFAULT no-op path of each rewired gate: it monkeypatches `resolve_working -> None`, runs each gate's default invocation, and asserts exit 0 plus an honest skip line, and it binds gate 51's `display_path` external-path branch. The prior fixtures exercised only the explicit `--root` path, so a broken default resolver could have passed silently; this closes that gap. Each gate is also confirmed to still ENFORCE on the live repo.
- Also adds the back-filled `#1226` merge-bypass-log row: a session-closing handoff has no following PR of its own session, so gate 50 surfaces the missing row only once #1227 demotes #1226 from highest-PR (the same retrospective-row case as #1168 and #1184).
- Dual-family adversarial verify (Claude + Codex) pre-push. The Codex lens's Medium coverage-gap finding (the default no-op paths were only empirically verified) is addressed by `WorkingResolveNoOpTests`; its High finding (the missing #1226 bypass row) is fixed here.
- The delivered per-gate worker draft (order `prequeue-migration-gates`) was re-verified at source and re-authored to the bare-literal `resolve_working("...")` form for consistency with the #1225 foundation, rather than the draft's `WORKING_SUBDIR`-removeprefix idiom.

## 2026-07-28, Library Version 2026.07.715, PR #1226

`.working/` changes for local project: session-closing handoff at an attended C1 wind-down (maintainer-directed, to avoid an emergency wind-down on the delicate `.working/`->`_private` migration continuation). Refreshed [`session-handoff.md`](../session-handoff.md) (new #1225 Next-actions / State-snapshot / Asserted-expectations blocks, pruned to current+1-prior, plus the operational lessons: exec-dispatch `--account` field-vs-id, the `is_orchestrator` guard, always `&&`-chain guard+push, dual-family QA codified, claude worker-liveness), released the [`session-state.md`](../session-state.md) lease, carried #1225's validate-pr/retro/bypass rows, and named the pre-queued migration-continuation orders (`prequeue-migration-gates` bo4cq5ed5, `prequeue-corpus-working-links` bhgbvq9v2, pinned 852ad467). The closing PR skips its trailing /validate-pr + /retro (loop-break; the next /resume's corpus-wide /validate is the compensating control).

## 2026-07-28, Library Version 2026.07.714, PR #1225

First implementation step of the maintainer-directed `.working/`->`grc_library_private/.working/` migration (privacy: `.working/` carried account identifiers and operational records adopters never need). The full gate-by-gate plan and the mid-implementation scope expansion (a 7th `.working`-reader, gate 60; the corpus->`.working` links gate 3 will flag; the gate-36 fixtures) live in the `grc_library_private` migration plan. This PR lands only the safe, non-breaking foundation; the remaining gates (50/59/78/60/43/51), the content move, and the `/resume` loud-fail gate follow in a fresh session.

### Added
- **`lint_common.resolve_working(relpath)`** ([`tools/lint_common.py`](../../tools/lint_common.py)): resolves a `.working/`-tree file, preferring `grc_library_private/.working/<relpath>`, falling back to the in-repo `.working/<relpath>`, else `None`. A reader that routes through it no-ops on `None` (the graceful-degradation contract for when `.working/` leaves the public repo: absent in public CI / an adopter clone, present on the maintainer's machine via the private sibling). Locked by a `ResolveSiblingTests.test_resolve_working_...` case.
### Changed
- **Three `.working/`-reading gates rewired to `resolve_working` with graceful degradation:** gate 63 [`lint-session-state.py`](../../tools/lint-session-state.py), gate 46 [`lint-overnight-file.py`](../../tools/lint-overnight-file.py), and gate 45 [`lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (its public [`TODO.md`](../../TODO.md) queued-PR check keeps running; only the sweep-cursor half no-ops). Each formerly ERRORED (exit 2) on the file's absence; that absence is now the expected public-clone state and no-ops (exit 0). All three still enforce today via the in-repo `.working/` fallback.

### Verification
- All three rewired gates run green against the present in-repo `.working/`; the helper's 3-way resolution is unit-tested. Carries #1224's dual-family validate-pr/retro/bypass close-out rows (recursion-avoidance). Pre-push guard green.

## 2026-07-28, Library Version 2026.07.713, PR #1224

Maintainer-flagged 2026-07-28: the forward-looking [`TODO.md`](../../TODO.md) contained items and prose stating they were closed, which belong in [`.working/DONE.md`](../../.working/DONE.md). This is the first of a short cleanup series and is SCOPED to the P1-intro and three specific inline closure notes; residual closure prose inside item BODIES (e.g. the item 2.1 body at `TODO.md:88`) is handled by the umbrella splits in the next PR, not this one, each item content-verified against current main by a worker and re-verified at source before applying.

### Changed
- **Priority-1 section intro rewritten.** The `## Priority 1` intro paragraph named `1.14` (which had moved to Priority 3) and `item 1.19 (closed 2026-07-25)` as *current* P1 holdings, implied none were open, and carried five closing-PR references, a closed-item roll-call `TODO.md:3` forbids. It now lists only open P1 work (the 1.26 quality-machinery series, 1.23, 1.19.13, and the egress-gated 1.22) with zero closing-PR references, verifiable line-by-line against the headings.
### Removed
- **Three inline closure notes** whose DONE entries already exist: `(The US HIPAA bullet closed in #733.)`, `(The EU eIDAS bullet closed in #739.)`, and `(Mexico's standalone annex shipped in #750.)` (their parent bullets stay open). DONE.md already records all three, so no rotation was needed.

### Added
- **TODO 3.185**, a low-priority tracker for the eight MEDIUM prose nuances the #1223 final dual-family verify deferred (maintainer-directed).

### Verification
- Content-verified apply-list (the original audit's DONE-status assumptions were corrected by a second worker pass); each removal re-verified at source. Carries #1223's validate-pr/retro/bypass close-out rows. Pre-push guard green (78 gates + D1-D9).

## 2026-07-28, Library Version 2026.07.712, PR #1223

Maintainer-directed 2026-07-28: codify the dual Claude+Codex QA that has been paying off (codex found the merged #1222 account-name leak, and this PR's own dual-family verify caught six defects across four rounds, each family surfacing what the other missed) so it is a standing default and need not be requested each time.

### Changed
- **High-assurance stage 3 requires dual-family verification.** [`governance/high-assurance-verification.md`](../../dev-security/claude-rules/governance/high-assurance-verification.md) (and its `.claude/rules/` copy, byte-identical per gate 37) now states the two independent adversarial verifiers ARE drawn from DIFFERENT model families (one Claude-family, one GPT/Codex-family), never two instances of one family: different families have systematically different blind spots, so a cross-family pair is stronger independence than same-family redundancy. Run the identical refute-brief to each and reconcile; a finding in only one family's delivery is triaged on its own merits, agreement is corroboration.
- **Substantive verifier tier defaults to a cross-family pair for consequential changes.** [`governance/ai-assistant-workflow-disciplines.md`](../../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) (both trees) adds that a consequential substantive change requires a cross-family verifier pair (the single-verifier count being the floor for an ordinary substantive change), per the high-assurance dual-family standard, as the default for validation and verification passes.
- **The executable high-assurance SKILL and its `/high-assurance` slash command, and the pack + project CLAUDE.md rule summaries,** were updated to match (stage/skill parity): the two adversarial verifiers are two separate-family workers, not same-session subagents.
- **Pack README** bumped to 1.65.19 with a `## Version history` row.

### Verification
- Both rule trees edited byte-identical above the PROJECT-OVERLAY (gate 37). Pre-push guard green (78 gates + D1-D9).

## 2026-07-28, Library Version 2026.07.711, PR #1222

Hardened the exec'd worker-dispatch pool so the orchestrator's own account is never used as a worker (maintainer-directed 2026-07-28, after a claude verifier was mistakenly dispatched to the `jeff-mailz` orchestrator account, both an independence violation and a burn of the scarce orchestrator credits the offload design exists to protect).

### Fixed
- **The exec-dispatch tool refuses `is_orchestrator` accounts.** [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py)'s `account_available()` now returns not-dispatchable for any account carrying `is_orchestrator: true`, with reason `orchestrator account, reserved (never dispatched as a worker)`. Because both dispatch paths (auto-pick via `eligible_accounts`/`pick_account`, and explicit `--account`) funnel through `account_available()`, one guard covers both. Only the claude `jeff-mailz` entry carries the flag, so both codex accounts (`jeff-mailz`, `jeff-posluns`) stay eligible, per the maintainer's directive that both codex are fine for workers.

### Verification
- `python3 tools/exec-dispatch.py --self-test` OK (61 checks, including 5 new orchestrator-guard cases: available-refused, claude-not-eligible, claude-target-refused, codex-still-eligible, codex-target-ok). Live `--dry-run` confirmed `jeff-mailz-claude` EXCLUDED with the reserved reason and the claude pick falling to `jposluns-work-claude`, while `jeff-mailz-codex` stays the codex pick.

## 2026-07-28, Library Version 2026.07.710, PR #1220

Routes the findings of the overnight component-by-component dual-family `/deep-assessment` (all six worker-capable components run, each on both a claude and a codex worker, reconciled with every positive re-verified at source).

### Added
- **33 TODO items (3.152 to 3.184)** in [`TODO.md`](../../TODO.md) capturing the deep-assessment yield, none dropped, per the QA-activity completion standard. Clusters: gate blind-spots (c2: register-vs-doc Owner divergences, crosswalk pair-consistency, matrix N/A escape, cross-doc statutory dates, role-vocabulary over body prose, metadata value sets); QA-ledger honesty (c3: gate-50 SUBSUMPTION and pipe-split fail-opens, an abbreviated-QA-of-record on a gate-logic change, ledger structure drifts); delivery-pipeline integrity (c4: the live `audit-worker-saturation` NO-WORKERS-from-unreadable-plane fail-open, `audit-delivery-status` single-plane, `collect-deliveries` TOCTOU/dry-run/collision); citation label-drift (c5: NIST SP 800-63B Rev.4-named-but-Rev.3-content, ISO 27033 title conflict, NIS2 Article-3 mis-reference, source-not-held acquisitions, a printed-title-vs-catalogue-title check); adoptability (c6: the `.working/`-delete false-safety and 23 broken links, pack drop-in leaks, adopter-vs-auditor contradictions); and (3.184) the corpus ISO citation currency updates enabled by the 2026-07-28 `_ref` ingest.

### Changed
- Batched #1219's post-merge dual-family `/validate-pr` row (HOLD, all findings resolved), `/retro` row, and merge-bypass row; rewrote the #1218 QA row's anticipatory "F7/F10 ROUTED" claim to cite the now-existing 3.161/3.164.

### Verification
- Every positive finding re-verified at source before routing (e.g. the 27 register-owner divergences spot-verified, the saturation fail-open reproduced live with the worker's own in-flight-registry entry, the A.6.2/A.6.7 and A.8.24 controls confirmed against corpus convention). Gate 50 clean; pre-push guard green (both runners, 78 gates). The recurring anticipatory-reference slip (writing "routed to TODO 3.X" before the item exists) is logged in the retro; this PR resolves the outstanding instances by creating the items first.

## 2026-07-28, Library Version 2026.07.709, PR #1219

Applied the confirmed, source-verified fixes from the overnight deep-assessment component-1 dual-family `/validate` (the two families were complementary: claude surfaced the citation errors, codex the docstring drift).

### Fixed
- **ISO/IEC 27001:2022 control-code corrections (3 remote-working/BYOD citations).** `A.6.2` (Terms and conditions of employment, the stale 2013-era code under which teleworking once sat) was cited for remote-working/BYOD in [`governance/matrix-reverse-framework-control-crosswalk.md`](../../governance/matrix-reverse-framework-control-crosswalk.md) (the `Remote working and BYOD` row) and [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md) (the BYOD Policy and Remote Working Security Standard rows). All three changed to `A.6.7` (Remote working), reconciling to the corpus's own authoritative [`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md), which already cites `A.6.7, A.8.1` for the same two documents. The fix is surgical: the legitimate employment-terms `A.6.2` uses (onboarding/offboarding, acceptable-use) were preserved, and a corpus-wide grep confirms zero remaining remote-working `A.6.2` carriers.
- **Secrets-management control correction.** [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md) mapped "Secrets management" to `A.8.10 to 8.11` (Information deletion / Data masking). Changed to `A.8.24` (Use of cryptography), the corpus's canonical control for secrets management (matching go.md/java.md and the row's own A02 column).
- **Stale delta-gate docstring.** [`tools/lint-audit-gate-parity.py`](../../tools/lint-audit-gate-parity.py) said "PR-only D1-D8 delta gates" and "contiguous D1..D8"; the implementation and the spec table carry D1..D9 (D9, the daily-changelog-rollup reminder, was added later). Docstring corrected to D1-D9, and the same fix applied to the spec gate-35 description (the "D1 to D8" spaced variant a re-verify caught) and the sibling references in pre-push-guard.sh, .claude/CLAUDE.md, and tests/test_linters.py.
- **Hook-count prose.** [`TODO.md`](../../TODO.md) §3.119 said "ten PreToolUse hooks"; there are 11 distinct PreToolUse block-hook files. Corrected to 11.

- **#1218 dual-family validate-pr corrections.** The post-merge validate-pr on the #1218 resume close-out (claude opus-5 authoritative + codex cross-reference, both HOLD) caught that the Sweep-127 row made ANTICIPATORY completion claims ('6 findings FIXED this session' against a follow-on PR that did not yet exist), a '6'-vs-'4' asserted-expectations miscount copied forward from Sweep 126, and a handoff D7 snapshot line whose prose ('#1217, one patch past 706') contradicted its own reconciled 708/69 tokens. All corrected across the sweep row, resume cursor, handoff snapshot, and detailed mirror; the pre-existing GFM-delimiter-placement and bypass-ordering findings routed to TODO. The #1218 validate-pr, retro, and merge-bypass rows are batched here.

### Changed
- Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) after the three per-document Version bumps.

### Verification
- Each citation finding re-verified at source before applying (the register/crosswalk vs the authoritative matrix, and `A.5.17`'s corpus usage). The word-count finding both families raised was REFUTED (the roll-up line is genuinely 76 whitespace-delimited words; the workers counted a narrower scope). Pre-push guard green (both runners, 78 gates); generator `--check` gates in sync.

## 2026-07-28, Library Version 2026.07.708, PR #1218

Overnight-session resume close-out (the first PR of the 2026-07-28 overnight-unattended session, resumed from the #1217 handoff).

### Changed
- Recorded **Sweep 127** in [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the DUAL-FAMILY loop-break corpus-wide `/validate` over the #1213..#1216 deltas (head `9fd2dd2d`=#1216), PRE-QUEUED at the #1217 wind-down and consumed at this overnight resume. Both families delivered; complementary yield (claude caught 3 ISO/IEC 27001:2022 A.6.2 to A.6.7 citation errors in remote-working/BYOD contexts plus a secrets A.5.17 warning; codex caught the [`tools/lint-audit-gate-parity.py`](../../tools/lint-audit-gate-parity.py) docstring D1-D8 to D1-D9 drift). All 4 #1216 asserted-expectations were CORROBORATED and ZERO contradicted; the citation errors are pre-existing latent defects in documents #1216 did not touch, so ordinary findings rather than misses. Loop-break control for #1217 PASSES. The 6 fixable findings are FIXED in the follow-on PR #1219; the remainder to be ROUTED to TODO in a subsequent routing PR.
- Advanced the Resume cursor to Sweep 127 and PRUNED [`.working/session-handoff.md`](../session-handoff.md) to current-plus-one-prior per per-session stack.
- Acquired the concurrency lease in [`.working/session-state.md`](../session-state.md) (Status active, overnight-unattended).

### Verification
- Pre-push guard green (both runners, 78 gates). The codex vpr-1216 HOLD (a read-only worker could not read the maintainer-private changelog archive) was RESOLVED by the orchestrator confirming the private changelog archive for 2026-07-27 holds all 20 swept #1195-#1214 entries.

## 2026-07-28, Library Version 2026.07.707, PR #1217 (2026-07-27b session-closing handoff)

Session-closing handoff for the 2026-07-27b session (`/resume` at 22:02Z, attended-autonomous winding to overnight). Working-state only; no corpus or code change.

### Changed
- Refreshed [`.working/session-handoff.md`](../session-handoff.md) with new Next-actions / State-snapshot / Asserted-expectations blocks for the 2026-07-27b close, carrying the maintainer-directed overnight plan: deep-assessment component-by-component DUAL-FAMILY (codex + claude) sequential over all worker-capable components, then `/fitness` broken out to the 10 personas each run by both families to compare. The 3.147 token-rotation measurement is flagged MORNING/ATTENDED-only (lockout risk), not overnight.
- Released the concurrency lease in [`.working/session-state.md`](../session-state.md) (Status: released, Active-session: none).
- Batched #1216's dual-family validate-pr (PASS) + retro + merge-bypass rows; refreshed [`.working/next-prs.txt`](../next-prs.txt).
- Pre-queued the overnight component-1 orders (`vda-c1-validate` claude + codex) and the `vpr-1216` dual-family orders.

### Verification
- Pre-push guard green (both runners, 78 gates) before push. #1216's validate-pr returned PASS (dual-family: claude authoritative 0e/0w/2-benign-notes; codex delivered as cross-reference, no contradicting finding).

## 2026-07-28, Library Version 2026.07.706, PR #1216 (2026-07-27 daily CHANGELOG roll-up)

D9 daily roll-up, past midnight UTC. Bookkeeping only.

### Changed
- [`CHANGELOG.md`](../../CHANGELOG.md): the 20 per-PR root entries for 2026-07-27 (PRs #1195-#1214, versions 2026.07.685 to 2026.07.704) collapsed into one 76-word daily roll-up line (`**2026-07-27 | 2026.07.685..2026.07.704 | PRs #1195-#1214 (20 PRs)** - ...`), keeping the adopter-facing root scannable.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): the matching 20 detailed-mirror entries pruned to the private changelog archive (grc_library_private, changelog-archive, the 2026-07-27-daily file) (data-safe: emitted + verified all 20 present before pruning), so the in-repo mirror holds the current window and gate 59 stays green (parity floor rises to #1215).

### Verification
- Gate 59 (mirror-header-parity) green after the sweep; the roll-up summary was drafted by an offloaded worker (range corrected to #1195-#1214) and verified at source (20 entries, dash-free, 76 words).
- Library 2026.07.705 to 2026.07.706, README 1.10.66 to 1.10.67 (Date 2026-07-28).
- Batches PR #1215's `/validate-pr` (dual-family) + `/retro` + merge-bypass rows.

## 2026-07-28, Library Version 2026.07.705, PR #1215 (pr-closeout.py: the PR close-out scaffolder, TODO 3.133)

Roadmap B efficiency tooling. Closes TODO 3.133 (the biggest per-PR efficiency lever).

### Added
- [`tools/pr-closeout.py`](../../tools/pr-closeout.py): the mechanical per-PR close-out scaffolder (938 lines, stdlib-only). It computes a merged PR's merge/base SHA and CI state (via git/gh, degrading gracefully), bumps every staged versioned file's Version AND Date, emits correctly-columned row templates for the backward surfaces (merge-bypass-log, validate-pr history + optional detail file, improvement-log) and the forward CHANGELOG root + detailed-mirror headers, and refreshes next-prs.txt. It names the two PR identities explicitly (backward rows describe the just-merged PR N; forward surfaces describe the PR M being assembled, default N+1 with a loud caveat) and ships a `--closeout-only` mode. Default mode is PREVIEW (writes nothing); mutations are dry-run-guarded and idempotent; ledger rows are anchored on the header line (never re-matching the next row, the fused-row mitigation). The orchestrator still AUTHORS all content; the tool removes the error-prone placement and the D2/D4/D7 co-bump trap.
- A regression test `test_pr_closeout_self_test` in [`tests/test_linters.py`](../../tests/test_linters.py), wiring the tool's 47-check `--self-test` into the linter-regression suite (gate 36) so it cannot rot.

### Verification / discipline observation
- **Dual-family review** (maintainer's new standing rule: all QA goes to both a claude and a codex worker). The claude lens caught a MUST-fix the self-test masked: `render_retro_row` emitted a BARE PR cell (`1214`) while the live improvement-log uses `#1213`, causing format drift and a double-insert risk (the idempotency token compared bare `1214`, so a house-format `#1214` row would not match). Fixed: `render_retro_row` now emits `#N`, the idempotency token is `f"#{merged_pr}"`, and the fixture was corrected to the `#N` convention so the test validates it. The codex lens wandered into reading skill files (a codex-focus issue, noted); the claude finding was the actionable one.
- Self-test 47/47 at HEAD; the wired regression test passes; stdlib-only (gate 71 safe); no language findings.
- Not run on real surfaces this PR; the #1214 close-out rows here were authored by hand, with the tool available for the next close-out.
- Library 2026.07.704 to 2026.07.705, README 1.10.65 to 1.10.66, Date 2026-07-28 (UTC rollover mid-session: forward surfaces dated 2026-07-28, #1214's backward merge-date rows stay 2026-07-27).
- Batches PR #1214's `/validate-pr` (PASS) + `/retro` + merge-bypass rows.
