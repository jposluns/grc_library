# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only the lead-paragraph summary of each entry; this file is the maintainer-grade audit trail.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-09, Library Version 2026.07.209, PR #721

The `/resume` Sweep-91 close-out, the first PR of the 2026-07-08/09 overnight backlog run (on the local NUC `nuc125h-a`; protected-apply authorized as local-instance per the recorded overnight authorizations). Working-state, version-surface, and CHANGELOG only; no corpus document body changed.

### Added
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the Sweep 91 row (subagents A, B, C; 0 findings; Detail `none`, Resulting-PR this close-out). Zero-finding sweep, so no per-iteration detail file is written. Own Version `2.0.85` to `2.0.86`.

### Changed
- [`.working/session-state.md`](../session-state.md): the concurrency lease ACQUIRED for `claude/resume-sweep91-validate` (`Active-session` set, `Status: active`, fresh heartbeat `2026-07-09T01:25:22Z`, `Current-task` set to the overnight-run summary, `Worker-dispatches` refreshed to record the unmerged Fable/Opus delivery branches the START-side check surfaced and the 3.16/3.17 delivery status change).
- [`.working/session-handoff.md`](../session-handoff.md): the Resume-cursor "Last validation sweep" advanced to Sweep 91 (Sweep 90 demoted to "Prior"); pruned per the current + 1 prior retention discipline (the sweep88 `claude/sweep88-todo112-nuc-resume` asserted-expectations block removed; its forward items are all already recorded in the retained sweep90/sweep89 blocks, [`TODO.md`](../../TODO.md), and [`.working/pending-decisions.md`](../pending-decisions.md), so nothing needed migrating).

### Verification
- Sweep 91 loop-break `/validate`: mechanical baseline `tools/run_all_audits.sh` reported all 67 gates pass at `ca33c49` (matches the asserted green-at `0f1c41b`/#719 = 67/67, of which `ca33c49` is a descendant; no close-vs-start drift). Clone confirmed non-shallow. Three subagents (recent-PR deep review of the #714..#719 delta, corpus-wide stale-reference sweep, audit-programme integrity reviewer) each returned 0 findings; the 9 pre-flight-scanner candidates were all the standing comparative/historical false-positive class ("two skills"/"two rules", the "five to twelve ... to twenty ... to sixty-seven" growth narrative). No asserted-expectation contradiction of any #714-#719 claimed-clean surface; the loop-break compensating control for #720 PASSES.
- The [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) START-side worker-collision check ran once at resume: every overnight-queue item is worker-DELIVERED apply-work (its delivery branch exists in `grc_library_scratch`), so there is no build collision.

### Discipline observation
- The START-side check surfaced a state drift the #720 handoff did not yet record: the scratch claims ledger and coverage index on scratch `main` are stale (newer claim rows live on the unmerged `fable-claims-batch`, `fable-claims-batch2`, and `fable-claims-batch3` branches), and the 3.16 ETSI-SAI and 3.17 MITRE-ATLAS crosswalks are now DELIVERED (their `worker/etsi-sai-crosswalk-316`, `worker/fix-etsi316-bare-ensure`, and `worker/atlas-crosswalk-317` branches exist), moving them from the handoff's "in-flight, do not touch" into the apply queue at lower priority. Recorded in the lease file's `Worker-dispatches` line; the scratch coverage-refresh sync remains queued.

## 2026-07-09, Library Version 2026.07.208, PR #720

Session-closing OVERNIGHT-SWAP handoff for the 2026-07-08/09 resumed session (#714-#719). Working-state + version-surface + CHANGELOG only; no corpus document body changed. The session's last act: land its working-state on `main` as a green merge so the next session (an OVERNIGHT BACKLOG run) resumes from `main`, not from an unmerged branch.

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): refreshed to the closing state. The sweep90 START next-actions block is replaced by a CLOSING block carrying the full overnight backlog queue (2.11 publications-screening two-repo, the FR-59/60/74/154/41/DORA/NIS2 research-authoring set, 3.21 the AIQT-columns claim-fit cell + pack-wide LOG-migration, 3.18 env-detection, the GR-P1/P2/P3-5 pack rules, SR-3 cross-repo, the deferred fragments, and the DO-NOT-TOUCH list); this session's `## Asserted expectations` block (#714-#719) is prepended; the Current-truth snapshot line is reconciled to the #720 head (library `2026.07.208`, README `1.9.569`, pack `1.57.0`, audit-spec `1.16.61`, gate 67, suite 350, and the green-at `0f1c41b` = 67/67 baseline).
- [`.working/session-state.md`](../session-state.md): the concurrency lease RELEASED (`Active-session: none`, `Status: released`, fresh heartbeat `2026-07-09T00:59:55Z`, Current-task closed to the release summary + next-session overnight-run pointer).
- [`.working/session-metrics.md`](../session-metrics.md): one row prepended for this session (about 2h52m lease-bounded elapsed; 6 merged PRs #714-#719 plus this handoff; subagent tokens `not precisely captured across the multi-compaction session` per the measured-versus-not-instrumented discipline; orchestrator tokens `not instrumented`). Version `1.0.42` to `1.0.43`.
- [`.working/pending-decisions.md`](../pending-decisions.md): the four overnight-run authorizations recorded as resolved (scope backlog-only; autonomy fix/route/APPLY-protected-local-instance-only; 3.21 cell + pack-wide; big/cross-repo apply).
- [`.working/validate-pr/history.md`](../validate-pr/history.md): the #720 handoff row added with the gate-50-recognized `SKIPPED (handoff-PR exception)` marker in the Findings cell.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): PR #719's `/validate-pr` count-fix batched in (the non-reproducible "265 of 315 docs" parenthetical in the #719 glossary-row entry made qualitative, the measurement-basis-dependent count class); its `/validate-pr` + `/retro` rows batch in via the history/improvement-log surfaces above.

### Verification
[`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) 67/67 standalone at the #720 head (working-state + version-surface + CHANGELOG only, so the corpus is unchanged from the green-at `0f1c41b` #719 baseline; `main` stays 67/67 at #720's descendant merge). [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) clean on the added lines; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`, D1-D7) green. D7 validates the handoff Current-truth version tokens against the live headers. Library `2026.07.207` to `2026.07.208`; README `1.9.568` to `1.9.569`.

### Notes
Per the standing loop-break handoff-PR exception (PR-workflow step 5a; the [`ai-assistant-workflow-disciplines`](../../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) pack rule), this PR runs NO trailing `/validate-pr` or `/retro`: doing so would begin a post-merge validate-then-PR loop with no terminating next substantive PR at the session boundary. The compensating control is stronger, the next `/resume`'s corpus-wide `/validate` over the #714..#719 deltas, cross-checked against this session's `## Asserted expectations` block and the green-at baseline. The session shipped #714-#719 all with full per-PR QA and zero escaped findings.

## 2026-07-09, Library Version 2026.07.207, PR #719

Applies the Fable `adopter-experience-sabe-batch` delivery (TODO 4.6 S-a/S-b/S-e; edit-payload delivery, no candidate files, so the orchestrator authored the three edits).

### Changed
- [`README.md`](../../README.md): S-b, a routing-table row pointing to [`docs/decision-tree.md`](../../docs/decision-tree.md) (validated linked zero times in the README at the read basis, reachable only via the portal).
- [`governance/register-glossary.md`](../../governance/register-glossary.md): S-e, a legend row for the "Governance Library Maintainer" meta-role (a role not a named person: the party accountable for the library's integrity and the Approving Authority on the majority of the corpus, with per-document Owner and Approving-Authority values otherwise distributed across the domain roles the content addresses, including CIO as the second-most-common approving authority and not an anomaly, per the audit's S-e correction; an adopter substitutes its own owner). The row was refined at apply time from the delivered candidate after the pre-push verifier flagged a metadata tension: an orchestrator recount confirmed the maintainer is the Approving Authority on the large majority of the corpus (CIO the clear second) while Owner is domain-distributed, which the candidate's "governance artefacts vs corpus content" split had mis-framed. The exact ratio is left qualitative here because it is measurement-basis-dependent (taxonomy versus raw metadata-block scans give different denominators); the shipped glossary row is qualitative for the same reason. Version `1.4.8` to `1.4.9`.
- [`tools/build-portal.py`](../../tools/build-portal.py): S-a, a generator change, a new "Board / CEO" audience tuple (governance Charter plus the board-risk-report template plus the compliance-alignment Matrix) and an inline `(maturity: ...)` tag on every entry render reusing the existing `classify_maturity`, plus an Overview sentence explaining the tag. The delivery's `title_contains` selector was dropped (not supported by `matches_selector`, which keys on domain / type / path_prefix), and the compliance selector was corrected from the non-existent compliance-Framework type to the Matrix that actually carries compliance standing.
- [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md), and [`taxonomy.yml`](../../taxonomy.yml): regenerated (taxonomy-first for the glossary Version bump, then portal and scorecard for the generator change).
- [`TODO.md`](../../TODO.md): §4.6 S-a/S-b/S-e closed and rotated to DONE; §4.6 stays open (S-c/S-d pending their separate worker-20260703-a deliveries, S-f a design item).
- [`.working/validate-pr/history.md`](../validate-pr/history.md) and [`.working/improvement-log.md`](../improvement-log.md): PR #718's 0-finding `/validate-pr` row and its `/retro` row batched in.

### Verification
`tools/run_all_audits.sh` 67/67 standalone; both generators `--check` green after the taxonomy-first regen; the S-a Board/CEO section eyeballed (three exec-facing docs, the Governance Library Charter, the GRC Compliance Alignment Matrix, and the Board Risk Report Template, each carrying a maturity tag). Library `2026.07.206` to `2026.07.207`; README `1.9.567` to `1.9.568`.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/adopter-experience-sabe-batch/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/adopter-experience-sabe-batch/MANIFEST.md) (Fable delivery, scratch #124). The orchestrator authored the three edits from the payload, adapting S-a's selectors to the live `matches_selector` vocabulary (dropping the unsupported `title_contains`, correcting the compliance type to Matrix), tested the generator, eyeballed the Board/CEO section, and re-ran both generator `--check` modes green.

## 2026-07-09, Library Version 2026.07.206, PR #718

Applies the Fable `reference-acquisition-gap-build` delivery (TODO 3.20 bullet 1, the not-held-source-detection residual of the `/reference-audit` build). Tool-only core; the pack cross-reference sentence deferred.

### Added
- [`tools/audit-reference-acquisition-gaps.py`](../../tools/audit-reference-acquisition-gaps.py): an advisory dev-aid (not a gate; exit 0 clean, 2 on error) that diffs the corpus canonical-citations register against the `grc_library_ref` catalogue and worklists cited-but-not-held standards as acquisition candidates, feeding the ref-base acquisition queue. FULL / `--section` / `--include-tooling` modes; identifier-key plus topic-expansion matching; reuses [`tools/reference-breadth-aliases.json`](../../tools/reference-breadth-aliases.json) (no new alias file); the opposite direction to [`tools/audit-reference-breadth.py`](../../tools/audit-reference-breadth.py). Re-run read-only at apply time against the live corpus register and ref catalogue: exit 0, worklist reproduced (a worklist size, not a defect count; the documented acronym/expansion residual over-reports and the judge clears it).

### Changed
- [`TODO.md`](../../TODO.md): the §3.20 not-held-source-detection bullet closed and rotated to DONE; the publications-bucket-inclusion bullet (the TODO 2.11 dependency) stays open, so §3.20 remains open.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) and [`.working/improvement-log.md`](../improvement-log.md): PR #717's 0-finding `/validate-pr` row and its `/retro` row batched in.

### Verification
`tools/run_all_audits.sh` 67/67 standalone; the language linter clean on the tool docstring; the tool re-run read-only (exit 0, worklist reproduced). No pack version change (a `tools/` add). The reference-audit skill and command cross-reference sentence (delivery item B1, a pack plus `.claude/` edit) is deferred to a later deliberate pack-touching batch; TODO 3.20 bullet 1 closes on the tool existing, not on B1. Library `2026.07.205` to `2026.07.206`; README `1.9.566` to `1.9.567`.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/reference-acquisition-gap-build/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/reference-acquisition-gap-build/MANIFEST.md) (Fable delivery, scratch #121). The orchestrator placed the tool verbatim, re-ran it read-only against the live corpus register and the ref catalogue to reproduce the worklist and confirm exit 0, and lint-language-checked the docstring; the B1 pack sentence deferred.

## 2026-07-08, Library Version 2026.07.205, PR #717

Adds gate 67, the Document-Type enumeration parity audit, closing the gate-blind class the #711/#712 cascade exposed. Bundles PR #716's `/validate-pr` F1 entry-count fix and its QA rows.

### Added
- [`tools/lint-doctype-parity.py`](../../tools/lint-doctype-parity.py): gate 67. Treats [`tools/lint-metadata.py`](../../tools/lint-metadata.py) `ALLOWED_TYPES` + `TYPE_TO_PREFIX` as the canonical Document-Type set and asserts every other enumeration surface agrees: the second linter's `DOCTYPES` set (exact equality), the required-sections linter's enforced keys (validity: a key must be a canonical type; absence is not-enforced by design), every canonical type name present as a bounded table cell or list item on the four name-enumerating surfaces (README `## Document types`, the ingestion spec list, the two `Document hierarchy` tables), and every canonical prefix present on the three prefix-enumerating surfaces (master-spec §4.3, the AI-ingestion instruction, CONTRIBUTING). A diverging surface is the failure; the fix is the surface, never the gate.
- [`tests/test_linters.py`](../../tests/test_linters.py): `DoctypeParityTests` (3 tests: positive baseline, the `name_is_cell` cell-vs-prose robustness distinction, and a monkeypatched synthetic-missing-type detection test). Suite 347 to 350.

### Changed
- Wired gate 67 across all four parity surfaces: [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml), [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh), [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml), and the [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 inventory table, §5 grouped list, and §6 detailed prose (both the description and appended-order sentences gate 64 requires); audit-programme spec Version `1.16.60` to `1.16.61`.
- [`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](../../dev-security/claude-rules/skills/guardrail-review/SKILL.md): the growth-narrative gate count refreshed sixty-six to sixty-seven (gate 39 currency; an incidental one-word fix, no pack-version bump).
- The bundled PR #716 `/validate-pr` finding F1 (entry-count off by one): corrected "five entries" to "four entries (#715, #713, #696, #685)" across the four surfaces that carried it (root [`CHANGELOG.md`](../../CHANGELOG.md), this mirror, [`.working/validate-pr/history.md`](../validate-pr/history.md), [`.working/validate-pr/2026-07-08-PR-715.md`](../validate-pr/2026-07-08-PR-715.md)); the 16-link / 9-target counts were already correct.
- [`.working/session-state.md`](../session-state.md): lease heartbeat re-stamped; Current-task notes #716 merged and PR 3 (this gate) in flight.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) and [`.working/improvement-log.md`](../improvement-log.md): PR #716's `/validate-pr` row (1 finding) and `/retro` row batched in; each Version bumped. The #716 per-PR record [`.working/validate-pr/2026-07-08-PR-716.md`](../validate-pr/2026-07-08-PR-716.md) added.

### Verification
`tools/run_all_audits.sh` 67/67 standalone (gate 35 four-surface parity, gate 39 count consistency, and gate 64 detailed-prose all green with the new gate); the regression suite runs 350 tests OK; a controlled synthetic mutation confirmed the gate detects an un-propagated type across all eight surfaces and passes clean on revert; pre-push guard green. A refute-briefed skeptical verifier confirmed all six claims (surface coverage, four-surface wiring, count currency, the F1 entry-count fix, the regression test, links and versions) and raised one note-level finding, a latent whole-file-scan false-pass vector (verified not present on the current corpus), accepted and tracked as the region-scoping hardening in TODO 3.23 with a limitation note added to the gate docstring. This closes the ALLOWED_TYPES-parity-gate candidate from the #711/#712 retros. Library `2026.07.204` to `2026.07.205`; README `1.9.565` to `1.9.566`.

## 2026-07-08, Library Version 2026.07.204, PR #716

Maintainer-directed convention addition: the worker-collision START-side check (nothing in the queueing flow otherwise makes a fresh session look at scratch for an in-flight worker claim or a pending delivery before it starts building a TODO item, so it could begin building an item a worker already holds or has delivered). Plus the bundled PR #715 `/validate-pr` F1 fix and F2 tracking.

### Changed
- [`TODO.md`](../../TODO.md): a "Start-side worker-collision check" bullet added to `## Queueing rules`, before starting any item, check the scratch claims ledger and coverage index for an in-flight claim or a pending inbox delivery covering it; a claimed or delivered item is apply-work (validate-then-apply on the delivery), not build-work; the check fires whenever the queue is resumed mid-session, not only at `/resume`.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a start-side-check paragraph added to `## Multi-session orchestration`, stated as the start-side complement to the close-out `Worker-brief coverage pairing` line (protected-file edit, authorized by the maintainer's 2026-07-08 directive that requested this addition; noted in the PR body).
- [`.working/multi-session-orchestration.md`](../multi-session-orchestration.md): a "Start-side collision check" bullet added to §5 with the operational form (an in-flight claim is a claims-ledger row; a delivered item is a worker-inbox package or a re-pointed coverage row; state is derived from artefacts per §5.1; the check fires mid-session, not only at `/resume`). Version `1.1.7` to `1.1.8`.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): PR #715 `/validate-pr` finding F1 fixed at the width of the class, 16 dangling bare-relative link targets (9 distinct: session-handoff, session-state, validate-pr/history, improvement-log, pending-decisions, session-metrics, overnight-pr, validate-sweeps/history, and one dated sweep file) across four entries (#715 with 4, #713 with 3, #696 with 5, #685 with 4) rewritten from bare to `../`-prefixed, re-verified with a resolution scan to 0 dangling remaining (gate-blind: `.working/` is broken-link-exempt).
- [`.working/session-state.md`](../session-state.md): lease heartbeat re-stamped; Current-task notes #715 merged and PR 3 in flight.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) and [`.working/improvement-log.md`](../improvement-log.md): PR #715's `/validate-pr` row (2 findings) and its `/retro` row batched in; each Version bumped.

### Added
- [`.working/validate-pr/2026-07-08-PR-715.md`](../validate-pr/2026-07-08-PR-715.md): the #715 findings-producing per-PR validation record.
- [`TODO.md`](../../TODO.md) §3.22: the cross-repo worker-provenance-link convention-review item (PR #715 F2; maintainer-directed tracking, 2026-07-08).

### Verification
`tools/run_all_audits.sh` 66/66 standalone; the language linter run on the new CLAUDE and runbook prose before the first commit (no em/en dashes, `-ize` orthography; my additions clean, the 23 findings it reported are pre-existing gate-exempt CLAUDE dashes, out of scope); pre-push guard green. No corpus-document body changed (the three carriers are TODO, the CLAUDE instructions, and the runbook, none a versioned corpus document); no TODO rotation (a convention addition, not a backlog-item close). Library `2026.07.203` to `2026.07.204`; README `1.9.564` to `1.9.565`.

## 2026-07-08, Library Version 2026.07.203, PR #715

Applies the Fable `resume-pointer` worker delivery: a repo-root manual resume entry point. Batches PR #714's QA rows.

### Added
- [`RESUME.md`](../../RESUME.md): a manual resume entry point for environments where the `/resume` slash command is not discovered (the NUC's Claude Code does not load this project's `.claude/commands/`). It is a POINTER, delegating to [`.claude/commands/resume.md`](../../.claude/commands/resume.md) (the protocol) and [`.working/session-handoff.md`](../session-handoff.md) (the live per-session queue), copying neither, so a resume started from it runs the same current protocol and reads the same live queue as `/resume`. Root placement needs no gate-config change: the content gates are allow-list-scoped to the domain dirs plus `.project-governance`, so a root file no linter names is not subject to the 13-field metadata block or the section model (the same basis on which the root CONTRIBUTING and SECURITY files sit at root without one); the whole-repo-walk gates (language, em/en dash, broken-link, secrets, PII) do see it and pass on the clean pointer prose.

### Changed
- [`.working/session-state.md`](../session-state.md): lease heartbeat re-stamped to `2026-07-08T21:28:51Z`; Current-task notes #714 merged and PR 2 in flight.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) and [`.working/improvement-log.md`](../improvement-log.md): PR #714's 0-finding `/validate-pr` row and its `/retro` row batched in (recursion-avoidance); each file's Version bumped.

### Verification
`tools/run_all_audits.sh` 66/66 standalone with the new pointer file present (confirms the allow-list prediction: no new whole-repo-walk gate failure). Pre-push guard green. No per-document Version or Date (the pointer carries no metadata block); no TODO rotation (a maintainer-directed convenience addition, not a backlog item). Library `2026.07.202` to `2026.07.203`; README `1.9.563` to `1.9.564`.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/resume-pointer/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/resume-pointer/MANIFEST.md) (merged scratch-side as PR #114). The candidate pointer file was placed verbatim after the orchestrator verified its two link targets resolve, its style-cleanliness (no em/en dashes; `ensures that`), and the allow-list gate reasoning; the full audit re-run with the file present confirmed 66/66.

## 2026-07-08, Library Version 2026.07.202, PR #714

The `/resume` Sweep-90 close-out for the 2026-07-08 resumed session (`claude/resume-sweep90-validate`): the loop-break corpus-wide `/validate` over the #700..#712 deltas, the compensating control for the #713 session-closing handoff PR (which skipped its trailing `/validate-pr` + `/retro`).

### Changed
- [`specification-master-project.md`](../../specification-master-project.md): §4.4 "Type selection guidance" gains a "Principle versus Charter versus Policy" disambiguation bullet (finding A-1; the new Principle Document Type's semantic adjacency to Charter and Policy had no §4.4 rule). Version `1.6.10` to `1.6.11`, Date `2026-07-08`.
- [`tools/lint-guardrail-cadence.py`](../../tools/lint-guardrail-cadence.py): the `INVENTORY_RE` illustrative `e.g.` comment (finding B-1) rewritten from hardcoded counts ("18 skills / 11 commands", re-staled by the #706/#707 skill and command additions) to count-free placeholder tokens, so it stops re-staling on every inventory change. Comment-only; the regex is unchanged, so linter behaviour is unaffected.
- [`.working/session-handoff.md`](../session-handoff.md): sweep cursor advanced to Sweep 90; pruned to current + 1 prior (the #685/#686 asserted-expectations block, the #687-#698 State-snapshot block, and the #699 + 2026-07-07 next-actions blocks removed, all durably recorded in DONE / CHANGELOG / the sweep history); a new CURRENT next-actions block plus a State-snapshot block prepended for this session, carrying the queue (PR 2 the resume-pointer apply, PR 3 the worker-collision start-side check, then the AIQT scratch one-liner, the first FULL `/reference-audit`, the ALLOWED_TYPES parity gate, the 3.16/3.17 fuller alignment maps).
- [`.working/session-state.md`](../session-state.md): concurrency lease ACQUIRED (`Active-session: claude/resume-sweep90-validate`, `Status: active`, fresh heartbeat, refreshed Current-task and Worker-dispatches).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the Sweep 90 row prepended; Version `2.0.84` to `2.0.85`.
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated after the master-spec version bump above.

### Added
- [`.working/validate-sweeps/2026-07-08-sweep90-iter1.md`](../validate-sweeps/2026-07-08-sweep90-iter1.md): the per-iteration detail file (the three subagent returns plus the orchestrator synthesis).

### Verification
Sweep 90 ran the full three-subagent dispatch (A recent-PR deep review, B corpus-wide stale-reference sweep, C audit-programme integrity). A: 0 escalated findings plus 1 out-of-window note (A-1); B: 1 in-window note (B-1); C: 0 findings. All three asserted-clean claims from the #700-#712 session (AIQT reframe complete, gate 42-to-44 correction complete, Principle propagated to all enumeration surfaces, counts 66/12/20/13/18, principle-doc §4 mappings claim-fit-verified against the held NIST AI RMF 1.0 / ISO/IEC TR 24028:2020 §5.3 / ISO/IEC 42001:2023 sources) were independently corroborated, so the loop-break compensating control PASSES. `tools/run_all_audits.sh` 66/66 standalone post-commit; `tools/run-pr-time-checks.sh` green (D7 validates the handoff Current-truth version tokens against live headers). Library `2026.07.201` to `2026.07.202`; README `1.9.562` to `1.9.563`.

## 2026-07-08, Library Version 2026.07.201, PR #713

Session-closing handoff for the 2026-07-08 resumed session (which shipped #700 through #712, all with full per-PR QA and zero escaped findings).

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): Current-truth refreshed to the closing state (merged through #712; green-at `bc01515` = 66/66; library `2026.07.201` / README `1.9.562` / pack `1.57.0`; gate 66 / rules 12 / skills 20 / commands 13 / Document-types 18); the next-session queue rewritten (the AIQT scratch one-liner; the first FULL `/reference-audit`; the invoke-only first `/deep-assessment`; the ALLOWED_TYPES-parity gate; changelog PR 3); this session's `## Asserted expectations` block prepended.
- [`.working/session-state.md`](../session-state.md): the concurrency lease RELEASED (`Status: released`, `Active-session: none`).
- [`.working/session-metrics.md`](../session-metrics.md): this session's row prepended (measured floor across the 16 retrievable post-compaction subagents; the pre-compaction subagents not re-retrievable, recorded as a floor per the measured-not-fabricated discipline).

### Verification
- Per the standing handoff-PR exception (the loop-break), this PR runs NO trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` over the #700..#712 deltas, cross-checked against the asserted expectations. The handoff's `/validate-pr` history row carries the gate-50-recognized `SKIPPED (handoff-PR exception)` marker in its Findings cell.
- Batches PR #712's `/validate-pr` (0 in-window findings) and `/retro` rows. `tools/run_all_audits.sh` = 66/66; the pre-push guard green. Working-state + version-surface + CHANGELOG only (no corpus document body).

Library `2026.07.200` to `2026.07.201`.

## 2026-07-08, Library Version 2026.07.200, PR #712

Hot-fix for the #711 post-merge `/validate-pr` Medium finding: the new "Principle" Document Type was registered in [`tools/lint-metadata.py`](../../tools/lint-metadata.py) (#711) but not propagated to the other surfaces that enumerate the allowed-type set. This propagates it everywhere.

### Changed
- [`specification-master-project.md`](../../specification-master-project.md) §4.3 allowed-types table, [`specification-ingestion.md`](../../specification-ingestion.md) allowed-types list, and [`instruction-ai-document-ingestion.md`](../../instruction-ai-document-ingestion.md) (types + `principle-` prefix): Principle added.
- [`tools/lint-filename-title-alignment.py`](../../tools/lint-filename-title-alignment.py): `principle` added to its `DOCTYPES` set (docstring "17 to 18"), which had SILENTLY SKIPPED the new principle-typed doc and violated its documented cover-all-ALLOWED_TYPES invariant; the linter now checks the doc (confirmed). [`tools/lint-required-sections.py`](../../tools/lint-required-sections.py) docstring notes Principle among the not-enforced types.
- The two "Document hierarchy" tables ([`governance/charter-governance-library.md`](../../governance/charter-governance-library.md) and [`governance/framework-document-architecture-and-interrelationship.md`](../../governance/framework-document-architecture-and-interrelationship.md)): Principle inserted at level 2 (after Charter, as the foundational cross-cutting principles the frameworks/policies/standards operationalize), the rows below renumbered to 3-18 (verified contiguous in both tables). Both docs Version+Date co-bumped, plus the two specs.
- [`governance/principle-integrity-and-trustworthiness.md`](../../governance/principle-integrity-and-trustworthiness.md): the numbered analytical section renamed "## 4. Framework alignment" to "## 4. Trustworthiness-vocabulary alignment" to disambiguate from the conventional trailing "## Framework alignment" end-table (the #711 Low duplicate-heading note); Version 0.0.1 to 0.0.2.
- [`README.md`](../../README.md) (the `## Document types` table) and [`CONTRIBUTING.md`](../../CONTRIBUTING.md) (the filename-prefix list): Principle added; the pre-existing `Worklist` / `worklist-` omission (stale in both since the initial public release, an untracked enumeration pair never in the type-set lockstep) fixed in the same pass, so both enumerations are now complete. CONTRIBUTING Version 1.2.3 to 1.2.4.

### Verification
- `tools/run_all_audits.sh` = 66/66; the filename-title linter now covers the principle doc (was silently skipped); both hierarchy tables verified levels 1-18 contiguous with Principle at 2; the taxonomy, portal, and scorecard regenerated after the version bumps. A substantive-tier refute verifier ran pre-push and caught that the first pass had missed two further enumeration surfaces (the README `## Document types` table and the CONTRIBUTING filename-prefix list, both also latently missing `Worklist`); both were fixed before push, and a completeness re-grep confirms zero type-enumeration or prefix-list surface now omits Principle.
- The ALLOWED_TYPES-to-prose parity gate (the gate-blind class this finding exposed, the ~8 doc-type-enumeration surfaces with no parity check) is proposed in the #711 `/retro` row as a maintainer-decision machinery candidate.
- Batches PR #711's `/validate-pr` (1 Medium + 2 Low, this PR is the fix) and `/retro` rows.

Library `2026.07.199` to `2026.07.200`.

## 2026-07-08, Library Version 2026.07.199, PR #711

AIQT PR 2 (maintainer-directed, gate-d approved): the corpus **AIQT Principle** document, the citable adopter-facing counterpart to the #705 pack apex rule, carrying the source-verified framework alignment the apex rule refers to but deliberately does not restate.

### Added
- [`governance/principle-integrity-and-trustworthiness.md`](../../governance/principle-integrity-and-trustworthiness.md): a new governance document (Document Type **Principle**, Version 0.0.1) stating the AIQT Principle ((Accuracy = Integrity = Quality = Trust) > Speed > Cost, the four co-equal non-negotiable facets), a per-facet section (definition + enforcing machinery), the priority-ordering and escalation posture, adoption guidance, and a §4 framework-alignment table mapping each facet to the AI-assurance vocabularies (NIST AI RMF 1.0, ISO/IEC 42001:2023, ISO/IEC TR 24028:2020) plus the general assurance frameworks. Section model and 13-field metadata mirrored from the governance framework documents.
- The **Principle** Document Type registered in [`tools/lint-metadata.py`](../../tools/lint-metadata.py) (`ALLOWED_TYPES` + the `principle-` filename prefix in `TYPE_TO_PREFIX`; docstring count 17 to 18), a one-off type alongside the corpus's existing Roadmap / Checklist / Worklist singletons. Maintainer-chosen (register a new type) over reusing an existing type.

### Changed
- [`governance/README.md`](../../governance/README.md) (Active-documents table row) and [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md) (index row) reference the new document; both Version+Date co-bumped. The taxonomy, portal, and maturity-scorecard generated artefacts were regenerated after the version bumps.
- [`TODO.md`](../../TODO.md): added section 3.21, the accepted-unverified tracker to claim-fit-verify the general-framework columns (SSDF / CCM / ISO 27001) against their source texts (the AI-assurance columns were verified this PR; the general columns are corpus-convention, labelled as such in the doc).

### Verification
- The §4 AI-assurance mappings are claim-fit-verified against the held source full-texts, with three deliberate source-honest caveats: Integrity has no direct NIST AI RMF characteristic (anchored on ISO/IEC TR 24028 §5.3 moral/ethical integrity, not the CIA-sense clause 3.21); Accuracy aligns with NIST *Valid and Reliable* only at the concept level ("informed by", not "prescribed by"); the general-framework columns are corpus-convention, not source-text-verified this PR (queued as TODO 3.21). Produced via a research subagent, orchestrator-re-verified key quotes against the held texts, then a combined claim-fit + refute verifier pre-push.
- `tools/run_all_audits.sh` = 66/66 (the metadata gate accepts the new Principle type; the structural-index gate sees the new doc in both index surfaces; taxonomy in sync). Style clean (no em/en-dashes, `-ize`, no bare "ensure"). Library / README bumped; the new doc at 0.0.1.
- Batches PR #710's `/validate-pr` (1 Low note) and `/retro` rows, the #710 detailed-entry relative-link fix, and the r6-G1 deferral note on TODO 3.15.

Library `2026.07.198` to `2026.07.199`.

## 2026-07-08, Library Version 2026.07.198, PR #710

Codifies the r6 guardrail-review gap finding **G2** (routed to TODO 3.15 in #707; maintainer directed "codify both" the r6 findings): the worker-brief gate-number-verification rail.

### Changed
- [`.working/worker-brief-template.md`](../worker-brief-template.md): added DO-rail 14, requiring every gate NUMBER a delivery cites to be verified against the [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 inventory (and every asserted corpus-gate interaction by running the named gate) before propagating into prose. Sibling to rails 6, 9, and 10 (control-code verification); this rail is for gate numbers and asserted gate behaviour. Targets the gate-42/44 mislabel class that cost the #702/#703/#704 churn. Version `1.4.4` to `1.4.5`.
- [`TODO.md`](../../TODO.md): closed the 3.15 r6 G2 bullet (rotated to [`.working/DONE.md`](../DONE.md)); the sibling G1 (the per-touch backstop D8 check) stays open in 3.15 for its own PR.

### Verification
- `tools/run_all_audits.sh` 66/66; the pre-push guard green. Bookkeeping-tier change (a `.working` template prose rail); no standing verifier.
- Batches PR #709's `/validate-pr` (1 Low note) and `/retro` rows, and the #709 detailed-entry label fix ("all eight `RECORD_SUBDIRS` history files" to "the seven present", the #709 `/validate-pr` note).

Library `2026.07.197` to `2026.07.198`.

## 2026-07-08, Library Version 2026.07.197, PR #709

Resolves the #708 post-merge `/validate-pr` finding (the dangling-index-links regression) with the maintainer-chosen delink + sweep-tool fix, and enhances the sweep tool so future weekly sweeps self-heal.

### Changed
- [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py): added `delink_absent_history_links(root)`, which delinks (to plain text) each `RECORD_SUBDIRS` history-file Detail-column link whose dated target file is absent in-repo (swept to the archive), leaving the filename as a plain reference (the swept file lives in git history and the scratch archive). It runs at the end of `--prune` (so a future weekly sweep never leaves dangling index links) and is exposed as a new `--delink-history` mode (the idempotent, standalone form used to heal history files after a prune that predated this step). Idempotent: a link whose target is still present in-repo (a current-week record) is untouched.
- The six history-file indexes under `.working/{validate-pr,validate-sweeps,guardrail-reviews,fitness-reviews,claim-fit,matrix-fit}/`: 217 now-absent links delinked to plain text (206 same-dir Detail-column + 11 cross-subdir Detail/Summary references; the #708 sweep's dangling links, gate-blind because `.working/` is exempt from gate 3).

### Verification
- `--delink-history` delinked 217 links total: 206 same-dir Detail-column links, then 11 cross-subdir path-prefixed references (a relative `..`-prefixed target into a sibling record subdir) after a pre-push verifier found the first regex matched only date-prefixed targets and the regex was broadened (with a URL guard). A comprehensive re-scan of the seven present `RECORD_SUBDIRS` history files (every dated-`.md` link, any form, resolved relative to each file; the full-qa and deep-assessment subdirs hold no history.md, so the delink loop correctly skips them) confirms 0 dangling remain; a further run delinks 0 (idempotent). Surgical: the current-week PR-708 record link is preserved (target present); a swept June record link (the PR-187 record) is now plain text (target absent). `tools/run_all_audits.sh` = 66/66.
- Batches PR #707's and PR #708's `/validate-pr` and `/retro` rows (the recursion-avoidance batch); the #708 `/validate-pr` history row and record now cite #709 as the closing PR, and the #708 `/retro` proposed-improvement (1) is dispositioned CODIFIED in #709.

Library `2026.07.196` to `2026.07.197`.

## 2026-07-08, Library Version 2026.07.196, PR #708

CHANGELOG restructure PR 2 (TODO 3.19, maintainer "Option A" 2026-07-08): the initial current-week sweep. The detailed-CHANGELOG mirror and the per-run records now keep only the CURRENT ISO week in-repo; everything older lives in the `grc_library_scratch` frozen archive as weekly Monday-dated files.

### Changed
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): rewritten to the current week via `tools/sweep-working-records-to-scratch.py --prune` (which kept 41 entries, #667 through #707); with this PR's own #708 entry the mirror now holds 42 (week of 2026-07-06 Monday; #667 through #708). The in-memory re-parse assertion passed (the constructed mirror re-parses to exactly the kept set, no dropped or duplicated entry).

### Removed
- 647 pre-current-week detailed-CHANGELOG entries (5 weeks: 2026-05-25 / 06-01 / 06-15 / 06-22 / 06-29) and 204 dated per-run record files under `.working/{validate-pr,validate-sweeps,full-qa,fitness-reviews,guardrail-reviews,claim-fit,matrix-fit,deep-assessment,reference-audit}/`, swept to the scratch archive. Each subdir's history and README files, and other non-dated operational files, stay in-repo. Removed content remains in git history (the durable copy) and in the scratch archive (the browsable copy).

### Verification
- Lossless: 647 archived detailed entries == 647 swept (per-week 2 + 25 + 145 + 261 + 214); 204 record files archived == 204 removed. The scratch side landed first ([`grc_library_scratch` PR #113](https://github.com/jposluns/grc_library_scratch/pull/113), archive verified present, 209 files) so `--prune --verify-archived` had a complete archive to check against before removing anything in-repo.
- `--prune` refused-unless-archived and re-parse-assertion safety rails both exercised; `tools/run_all_audits.sh` = 66/66 post-prune (gate 59 mirror parity holds under its dynamic floor `max(CUTOFF_PR, oldest PR in mirror)`, now anchored at #667).
- The scratch `archive/` was exempted from the scratch validate gate's Check 5 (watermark PII) and Check 6 (house style) in scratch PR #113; the exemption is load-bearing (the archive carries incidental `/home/jposluns/` command-output paths and 4 files with historical em-dashes, preserved as-is in the private frozen archive per Option A). The root changelog keeps its full history unchanged (its compact-reformat is PR 3, deferred).
- Batches PR #707's `/validate-pr` (0 findings) and `/retro` rows.

Library `2026.07.195` to `2026.07.196`.

## 2026-07-08, Library Version 2026.07.195, PR #707

Reference-audit PR B (closes TODO 2.14): the `/reference-audit` cadenced skill and slash command, completing the two-PR build begun by the advisory tool in PR A (#706). This is the reference-BREADTH layer above `/matrix-fit` (control-code fit) and `/claim-fit` (claim precision): it dispatches a semantic judge over the recall-oriented worklist the tool produces, judging in both directions whether the corpus engages the best held authoritative sources per topic (the gate-blind "held but unused" SP 800-154 class). The gate-60 auto-fired guardrail review r6 rides in this PR; its drift fixes and inventory-token refresh are recorded below.

### Added
- [`dev-security/claude-rules/skills/reference-audit/SKILL.md`](../../dev-security/claude-rules/skills/reference-audit/SKILL.md): the cadenced skill (7 steps), `derives_from` [`evidence-grounded-completion.md`](../../dev-security/claude-rules/governance/evidence-grounded-completion.md). Four-valued verdicts (`adopt-citation` / `adopt-content` / `recommend` / `no-fit`); tier-by-bucket ceilings (standards, frameworks, legislation, programs authoritative; templates content-only; books recommendation-only, never authoritative; publications excluded pending screening); FULL / per-touch / new-ingest cadences.
- [`.claude/commands/reference-audit.md`](../../.claude/commands/reference-audit.md): the `/reference-audit` slash command, step-identifier parity with the skill (steps 1-7).

### Changed
- [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py): PAIRS registry extended with the reference-audit skill/command pair (gate 44).
- [`dev-security/claude-rules/skills/deep-assessment/SKILL.md`](../../dev-security/claude-rules/skills/deep-assessment/SKILL.md) and [`.claude/commands/deep-assessment.md`](../../.claude/commands/deep-assessment.md): the phase-3 semantic-instrument list extended to invoke `/reference-audit` in FULL mode (both surfaces).
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): pack `1.56.0` to `1.57.0` (minor, new skill) with the skills-tree entry and the 1.57.0 version-history row (D6 co-bump); the twentieth-skill count applied.
- [`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](../../dev-security/claude-rules/skills/guardrail-review/SKILL.md): growth-narrative count `nineteen` to `twenty` (gate-39-blind word-form).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): added the `## Reference-breadth cadence (/reference-audit)` section and a PR-close-out per-touch reference-breadth obligation bullet; the PRIMORDIAL-intro conflict-axis phrase harmonized to the AIQT tier.
- [`TODO.md`](../../TODO.md): closed 2.14 (rotated to [`.working/DONE.md`](../../DONE.md)); added section 3.20 (`/reference-audit` build residuals: not-held-source detection, publications-after-2.11) and two section-3.15 `[guardrails]` bullets from the r6 review; the P2/P3 backlog-totals summary line reconciled (P2 to 9 open, P3 to 9 items).
- [`.claude/settings.json`](../../.claude/settings.json) and [`.working/next-prs.txt`](../next-prs.txt): a session-convenience status-line config (the maintainer's `/statusline` request) rendering the upcoming-five-PRs queue from that file; bundled here rather than split as a trivial, no-gate-impact working-state change.

### Fixed
- **Guardrail review r6, drift finding D1 (AIQT partial migration).** #705's `/validate-pr` asserted the AIQT migration complete, but its completion grep was phrasing-specific (`>` form only) and missed the variant phrasings. Four live carriers migrated: [`dev-security/claude-rules/governance/surface-counterproductive-instructions.md`](../../dev-security/claude-rules/governance/surface-counterproductive-instructions.md) and its byte-identical [`.claude/rules/` mirror](../../.claude/rules/governance/surface-counterproductive-instructions.md) (the "Quality versus Speed versus Cost" governed-tradeoff clause to "among the AIQT tier, Speed, and Cost"), the pack [`CLAUDE.md`](../../dev-security/claude-rules/CLAUDE.md) rules-index bullet (to "the AIQT-tier / Speed / Cost tradeoff"), and [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) wind-down section (the "Quality > Speed remains the tiebreaker" heading to "The AIQT tier above Speed remains the tiebreaker"). A post-edit bare-token grep confirms zero live carriers remain (only the rule's provenance paragraph and the #705 CHANGELOG entry, both whitelisted by design).
- **Guardrail review r6, drift finding D2 (deep-assessment description).** The one-sentence description and command opener enumerated six composed instruments while phase-3 (correctly) composes seven; `/reference-audit` added to both enumerations.
- The #706 CHANGELOG leads' "always exit 0" characterization (batched #706 `/validate-pr` note) reworded to "exit 0 on a clean run and 2 on error" in both surfaces, harmonizing the lead with the same entry's documented SIGPIPE correction.

### Verification
- `tools/run_all_audits.sh` green post-fix (gate 60 now passes on the r6 token refresh 66/12/20/13; parity gates 35/37/39/41/44 green; the two surface-counterproductive-instructions rule copies byte-identical per gate 37).
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) run standalone/unpiped; a substantive-tier refute-briefed verifier dispatched on the diff.
- Bare-token completion grep (`quality (>|&gt;|versus|vs) speed`) re-run post-fix: zero live carriers, only whitelisted survivors.
- Every drift/gap finding orchestrator-re-verified at source before action (the r6 record documents each grep).
- A substantive-tier pre-push refute verifier caught one in-window miss: the P2/P3 backlog-totals summary line was stale after 2.14's close and 3.20's add (the recurring #692/#693 backlog-totals-lag class); fixed before push (P2 to 9 open items dropping 2.14, P3 to 9 items adding 3.20) and re-verified. It also noted the statusline config bundled without a CHANGELOG mention, now recorded above.

### Guardrail review r6 (rides in this PR)
Auto-fired by gate 60 (drift 4: skills 18 to 20, commands 11 to 13, the deep-assessment and reference-audit skill+command pairs). Four findings, 0 cross-lens duplicates: overlap 0; drift D1 (AIQT partial migration, Low-Medium, fixed above), drift D2 (deep-assessment description, Low, fixed above); gap G1 (the per-touch reference-breadth obligation's "queued TODO item" backstop was a phantom, Medium-High) and gap G2 (the worker-brief gate-number-verification rail uncodified since #702, Low-Medium) both routed to TODO 3.15 `[guardrails]` as maintainer-decision machinery proposals (G1's false-claim half fixed in-window by adding the real TODO item). Record: [`.working/guardrail-reviews/2026-07-08-r6.md`](../guardrail-reviews/2026-07-08-r6.md); history row appended.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/reference-audit-build/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/reference-audit-build/MANIFEST.md) (merged scratch-side as PR #111, gate-label-corrected in #112). The skill and command were copied from the delivery and the orchestrator authored the wiring, verifying every anchor against live main and every gate number against the specification §6.

## 2026-07-08, Library Version 2026.07.194, PR #706

The reference-breadth advisory tool (TODO 2.14 PR A of two; PR B ships the skill, command, and wiring). An orchestrator dev-aid in the `audit-*.py` mould (exit 0 on a clean run and 2 on error, not a gate, no gate-surface wiring or regression fixture). Applied from a Fable worker delivery under validate-then-apply; the tool re-run at apply time and its figures recounted.

### Added
- [`tools/audit-reference-breadth.py`](../../tools/audit-reference-breadth.py) (mode 755): measures how the corpus uses the held `grc_library_ref` reference base and emits a recall-oriented breadth worklist for the `/reference-audit` skill's semantic judge. FULL mode (whole corpus and in-scope reference base), per-touch mode (`--docs`, optional `--update-state`), and new-ingest mode (`--ref-since` / `--ref-items`); tier-by-bucket semantics; a catalogue parser keyed to the generated format; identifier-shape key derivation plus the curated aliases; topic-overlap-ranked candidates; per-document delta state.
- [`tools/reference-breadth-aliases.json`](../../tools/reference-breadth-aliases.json): curated citation-key aliases for the measured non-book no-key set (legislation, programs, templates); books deliberately un-aliased (recommendation tier, engaged by topic rather than cited by identifier).
- [`.working/reference-audit/README.md`](../reference-audit/README.md), [`history.md`](../reference-audit/history.md), and [`doc-state.md`](../reference-audit/doc-state.md): the run-record stubs (the history header mirrors claim-fit; the doc-state prose is byte-identical to the tool's `--update-state` output, so the first per-touch run produces a rows-only diff).

### Changed
- [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py): `reference-audit` added to `RECORD_SUBDIRS` (dated per-run records sweep to the scratch archive; the non-dated README, history, and doc-state stubs stay in-repo by the dated-filename rule).
- [`README.md`](../../README.md): library CalVer `2026.07.193` to `2026.07.194`, README Version `1.9.554` to `1.9.555`.

### Verification
- The tool re-run at apply time (FULL mode, read-only, exit 0): 343 in-scope reference items (books 22, frameworks 70, legislation 40, programs 15, standards 180, templates 16; publications excluded) over 382 corpus documents; classification 128 well-cited, 62 thin, 131 uncited, 22 no-key. These are the orchestrator's recount at `1ed5524` / ref `7a598a0`, not the worker's transcription. The aliases JSON parses; the tool parses (stdlib-only Python 3.11).
- The advisory-tool precedent holds (no gate wiring, no regression fixture; the same `audit-*.py` mould as the other advisory tools). `tools/run_all_audits.sh`: all 66 gates pass with the new files present.
- Apply-time correction (a pre-push verifier catch): the tool's docstring claimed it "always exits 0", but a truncated-pipe consumer (`| head`) raised `BrokenPipeError` and exited 120 with a traceback. Added a `signal.signal(signal.SIGPIPE, signal.SIG_DFL)` guard at `main()` start and softened the docstring, so a broken pipe now terminates cleanly via SIGPIPE (no traceback) and the standalone run stays exit 0.
- Batches PR #705's `/validate-pr` (0 findings) and `/retro` rows.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/reference-audit-build/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/reference-audit-build/MANIFEST.md) (merged scratch-side as PR #111, gate-label-corrected in #112). The worker tested the tool with six read-only mode runs (six defects found and fixed before delivery); the orchestrator re-ran FULL mode and recounted every figure.

## 2026-07-08, Library Version 2026.07.193, PR #705

Codifies the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Speed > Cost, as the pack's apex rule (PR 1 of the AIQT work; the corpus principle document is PR 2). Applied from the Fable aiqt-codification delivery under validate-then-apply; the maintainer confirmed the inner-bracket form (no outer brackets) and the three world-facing wordings (checkpoint line, apex-rule headline, README baseline block) before the first commit.

### Changed
- [`dev-security/claude-rules/governance/project-integrity.md`](../../dev-security/claude-rules/governance/project-integrity.md) and its [`.claude/rules/`](../../.claude/rules/governance/project-integrity.md) mirror (identical, gate-37-synced, both in this commit): the full amended text. Title, opening ordering paragraph, the four-facet section (each facet mapped to its enforcing machinery), the priority-enforcement section, and the checkpoint reframed to AIQT; the two known misreadings foreclosed; the integrity non-negotiables (section 3), the escalation protocol (section 4), and the cadence (section 5) carried over verbatim; the filename unchanged so all pack cross-references keep resolving; a provenance paragraph records the superseded `Quality > Speed > Cost` formulation once by design.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): the PRIMORDIAL RULE heading (`, THE AIQT PRINCIPLE` appended), the ordering statement (now naming the four facets), the priority-enforcement bullets, the escalation and cadence lines, the checkpoint chant (`Integrity check:` to `AIQT check:`), the `INTEGRITY > SPEED > COST` proactive-assessment reference, and the rules-index project-integrity bullet.
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): the step-8 PRIMORDIAL-RULE standing-disciplines reference.
- [`dev-security/claude-rules/CLAUDE.md`](../../dev-security/claude-rules/CLAUDE.md): the apex-rule index bullet.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): the category-2 blurb, the rule-tree apex line, and the applicability row migrated; Version `1.55.0` to `1.56.0` with the paired Version-history row (D6); and a new copy-paste AIQT baseline starter section (the maintainer-approved world-facing form 3).
- [`dev-security/claude-rules/governance/surface-counterproductive-instructions.md`](../../dev-security/claude-rules/governance/surface-counterproductive-instructions.md) and its `.claude/rules/` mirror: the project-integrity cross-reference line (both trees, gate-37-synced).
- [`README.md`](../../README.md): library CalVer `2026.07.192` to `2026.07.193`, README Version `1.9.553` to `1.9.554`.
- [`.working/session-handoff.md`](../session-handoff.md): the Standing-disciplines PRIMORDIAL-RULE line migrated to AIQT (a live-guidance surface, not a frozen record); the Current-truth snapshot reconciled to this PR's head.

### Verification
- Bracket form: inner brackets only around the four co-equal facets, `(Accuracy = Integrity = Quality = Trust)`, maintainer-confirmed; no outer brackets; applied consistently across every live surface (the title uses a comma lead-in to avoid a nested parenthesis).
- Gate number: the `.claude/rules` copy-sync gate is gate 37 (verified against the audit-programme specification §6; the delivery's apply-note had labeled it gate 44, corrected here per the #703 apply-time-verify-gate-numbers rail).
- Completion check (whole-repo grep, the #703/#704 lesson): the only surviving old-token strings (`Quality > Speed > Cost`, `INTEGRITY > SPEED > COST`, `Integrity check:`, `Project integrity absolute`) are the rule's provenance paragraph (both trees), the pack README version-history rows, the pack CLAUDE.md rollout narrative, and the frozen root changelog and working-state records, all whitelisted by design; no unmigrated live carrier remains.
- The language gate was run on all touched pack prose before the first commit (clean). `tools/run_all_audits.sh`: all 66 gates pass, including gate 37 (the two identical project-integrity copies) and gate 35 (four-surface parity). No hook or tool consumes the literal `Integrity check:` chant (grep of `.claude/hooks/` and `tools/`).
- Batches PR #704's `/validate-pr` (0 findings) and `/retro` rows.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/aiqt-codification/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/aiqt-codification/MANIFEST.md) (merged scratch-side as PR #110, gate-label-corrected in scratch #112). A research delivery verified and applied by the orchestrator: the amended rule and the surface rewrites are orchestrator-authored from the candidate with the maintainer-confirmed inner-bracket form and the gate-37 copy-sync correction integrated, not pasted.

## 2026-07-08, Library Version 2026.07.192, PR #704

Completes the #703 paired-skill parity gate-number correction, which #703's own post-merge `/validate-pr` found incomplete (three carriers survived a scope-limited verification grep). Prose/working-state accuracy correction; no functional or gate-logic change.

### Fixed
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md) (the #702 entry's Verification line): "Gate 42 (10 pairs, matching steps)" corrected to Gate 44 (the material carrier #703 missed, a fourth line in the very #702 entry #703 claimed to have fully corrected).
- [`.working/session-state.md`](../session-state.md) and [`.working/session-handoff.md`](../session-handoff.md): the `gate-42 PAIRS registration` phrase corrected to gate 44 (transient working-state carriers).
- Confirmed by a comprehensive whole-repo grep (`gate[ -]42`, all file types, case-insensitive) that every remaining `gate 42` string is either the legitimate external-overlay-licence-audit gate 42 (spec definition, the preflight-scanner comment, and frozen historical CHANGELOG entries) or a corrected-from quote in the #702/#703/#704 correction meta-prose; no live surface asserts the parity gate is gate 42.

### Verification
- `tools/run_all_audits.sh`: all 66 gates pass. Root and detailed CHANGELOG carry #704/#703/#702 in parity (gate 59).
- Root cause recorded (`/retro`): #703's verification grep used a hand-listed path subset (excluding the detailed mirror and working-state) rather than a whole-repo scope, the completion-verification scope-width failure the PR-close-out checklist names; #704's grep is whole-repo.
- Batches PR #703's `/validate-pr` (the incomplete-correction finding) and `/retro` rows.
- Quick-fix / prose-correction tier: no standing verifier (the completion is a mechanical whole-repo grep confirmed clean).

## 2026-07-08, Library Version 2026.07.191, PR #703

Corrects the gate-number mislabel PR #702 introduced (a #702 `/validate-pr` in-window warning). The paired-skill step-parity gate is canonically gate 44; #702 labeled it `gate 42` (which is the external-overlay licence-consistency audit) in five live carriers. Prose-only accuracy correction; no functional or gate-logic change.

### Fixed
- [`CHANGELOG.md`](../../CHANGELOG.md) (the #702 root lead) and this detailed mirror (three lines of the #702 detailed entry): `gate 42` corrected to gate 44 where it names the paired-skill step-parity registry and check.
- [`.working/DONE.md`](../DONE.md) (the #702 entry): the paired-skill registry reference corrected from gate 42 to gate 44.
- Verified by grep that no parity-gate `gate 42` mislabel remains in any live surface and that the historical `gate 42` references (the real licence-consistency audit, in frozen CHANGELOG and `.working/` records) are untouched; the correct number confirmed against [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) §6 ("Gate 44 is a paired-skill step-parity audit"; "Gate 42 is an external-overlay licence consistency audit") and [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh).

### Changed
- [`README.md`](../../README.md): library CalVer `2026.07.190` to `2026.07.191`, README Version `1.9.551` to `1.9.552`.

### Verification
- `tools/run_all_audits.sh`: all 66 gates pass. Root and detailed CHANGELOG carry #703, #702, #701 in parity (gate 59).
- Batches PR #702's `/validate-pr` (one in-window warning, the gate-number mislabel fixed here) and `/retro` (the second-occurrence signal on apply-time verification of worker claims about the corpus's own machinery) rows.
- Quick-fix / prose-correction tier: no standing verifier (the correct gate number is a mechanical fact confirmed against the spec §6).

## 2026-07-08, Library Version 2026.07.190, PR #702

The `/deep-assessment` skill, command, register, and hooks (PR B of the two-PR deep-assessment integration; PR A shipped the advisory tools in #701). Applied from the same Fable worker delivery under validate-then-apply, with three maintainer-directed post-#695 integration deltas and one maintainer-directed coverage codification folded in.

### Added
- [`dev-security/claude-rules/skills/deep-assessment/SKILL.md`](../../dev-security/claude-rules/skills/deep-assessment/SKILL.md): the rare, maintainer-invoked, multi-session whole-project deep-assessment skill (eight-step process; count-free and inventory-deriving; register-backed and re-entrant; sign-off-terminated). `derives_from` [`trust-recovery-escalation.md`](../../dev-security/claude-rules/governance/trust-recovery-escalation.md).
- [`.claude/commands/deep-assessment.md`](../../.claude/commands/deep-assessment.md): the paired `/deep-assessment` slash command (step identifiers 1 to 8 matching the SKILL for gate 44).
- [`.working/deep-assessment/register.md`](../deep-assessment/register.md): the durable run register (one row per run; `in-progress` rows resume; rows close only on maintainer sign-off).

### Changed
- [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py): gate-44 PAIRS registry extended with the deep-assessment pair (10 pairs; gate 44 confirms matching step-identifier sets).
- [`.claude/commands/resume.md`](../../.claude/commands/resume.md): step 7 extended to surface an `in-progress` deep-assessment run register at resume, alongside the other standing registers.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): Version `1.54.7` to `1.55.0` (minor, new skill) with the paired Version-history row (D6); the skills directory tree gained the deep-assessment entry (gate 41).
- [`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](../../dev-security/claude-rules/skills/guardrail-review/SKILL.md): the growth-narrative skill count advanced from eighteen to nineteen (the gate-39 count-consistency carrier).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a new whole-project-deep-assessment section (maintainer-approved this session), describing the instrument, its rare-invoked non-cadenced nature, the register and resume surfacing, and the coverage obligation.
- [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py): `deep-assessment` added to `RECORD_SUBDIRS`, so the dated per-run records join the weekly sweep to the scratch archive (the non-dated register stays in-repo).
- [`README.md`](../../README.md): library CalVer `2026.07.189` to `2026.07.190`, README Version `1.9.550` to `1.9.551`.

### Post-#695 integration deltas (maintainer-directed)
- Per-run records are dated files beside the register (the fitness-review `YYYY-MM-DD-rN` naming), not per-run directories; the SKILL step-1 / step-8 / Verification wording, the command step-1 wording, and the register per-run-detail line were adjusted accordingly. The non-dated register is in-repo by design.
- `deep-assessment` added to `RECORD_SUBDIRS` (above) so its dated records sweep with the others.
- One model-agnostic model-tiering sentence added to SKILL step 3 with a mirrored clause in command step 3 (orchestration and finding-adjudication on the strongest available model tier, wide fan-out readers on a cheaper tier, mechanical phases model-indifferent). The clause introduces no capitalized step token, so gate-44 parity is unaffected.

### Coverage obligation (maintainer-directed 2026-07-08)
- Codified in the SKILL (the design-rules paragraph) and the CLAUDE.md section: the count-free, inventory-deriving design makes the live inventory of quality machinery the assessment scope by construction, so any future quality-check process, tool, gate, skill, or check is included automatically; and adding a quality-check instrument carries the reciprocal duty to keep the pass covering it (a new gate gains a mutation-probe variant, a new command or skill joins the phase-3 invocation set, a new advisory tool joins the phase-3 aids).

### Verification
- `tools/run_all_audits.sh`: all 66 gates pass on the working tree. Gate 44 (10 pairs, matching steps), gate 41 (skills-tree enumeration), gate 39 (skill count 19), and gate 32 (`derives_from` resolves) all green. The language gate was run on the SKILL, command, and register before the first commit (clean). Gate 60 warns at drift 2 (skills and commands each plus one, under the fail-3 threshold) and passes; the guardrail-review inventory token self-updates at the next `/guardrails` run, not hand-edited.
- Batches PR #701's `/validate-pr` (0 findings) and `/retro` rows.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/deep-assessment-build/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/deep-assessment-build/MANIFEST.md) (merged scratch-side as PR #109), the same delivery as PR A. The four staged-default open decisions were confirmed by the maintainer at apply time (command name `/deep-assessment`, `derives_from` trust-recovery-escalation, no TODO item, and the model-tiering sentence added in this PR); the SKILL and command are orchestrator-authored from the candidate files with the post-#695 deltas and the coverage codification integrated, not pasted.

## 2026-07-08, Library Version 2026.07.189, PR #701

The two advisory gate-efficacy tools for the upcoming `/deep-assessment` cadence (PR A of the two-PR deep-assessment integration; PR B ships the skill, command, register, and hooks). Both are orchestrator dev-aids in the `audit-*.py` mould (exit 0 after their report, not audit gates, no gate-surface wiring or regression fixture; the same shape as the other `audit-*.py` advisory tools). Applied from a Fable worker delivery under validate-then-apply: both tools re-run at apply time and every cited figure recounted against the live checkout (the worker's figures were not transcribed).

### Added
- [`tools/audit-gate-blindspots.py`](../../tools/audit-gate-blindspots.py): derives, per gate wired into `tools/run_all_audits.sh`, that gate's effective scan scope by static inspection of its module source (three classes: common-discovery, target-scoped, not-derivable), then inverts the union to report the markdown surfaces no scope-derivable gate scans. Static-inspection-approximate by construction (stated in the module docstring); the report is a triage aid for the deep-assessment run's manual-review list, never a coverage proof.
- [`tools/audit-gate-mutation.py`](../../tools/audit-gate-mutation.py): seeds defect variants into a DISPOSABLE repo copy and reports which gates detect them, probing gate detection WIDTH (the property the one-fixture-per-rule regression suite does not exercise). A three-condition safety refusal (a `DISPOSABLE-COPY-OK` marker at the target root, the target not being this tool's own repository, and a clean target git tree) makes it a hard exit 2 rather than ever mutating a live checkout; it reverts every variant after running.
- [`tools/gate-mutation-variants.json`](../../tools/gate-mutation-variants.json): the starter variant library (10 variants over 5 gates: the language, unbalanced-fences, secrets-in-content, links, and metadata linters), each a hypothesis about the gate's intended detection scope; dash characters are JSON-escaped so the file itself carries no literal dash.

### Changed
- [`tools/lint-secrets-in-content.py`](../../tools/lint-secrets-in-content.py): added the variant library to `EXEMPT_FILES`. Apply-time correction (the worker verified the delivery against the scratch gate, not this corpus's secret-pattern gate): the variant library's documentation-format payloads (AWS's canonical `AKIAIOSFODNN7EXAMPLE` example key, at two lines) matched the AWS-Access-Key-ID pattern and failed the gate. The gate's own design exempts files that "document secret formats by design" and already exempts the linter regression test fixture file for exactly this reason (fixture content deliberately embedding pattern-shaped strings); the variant library is the identical fixture case, so this is the documented legitimate-exception path, not a gate weakening. No detection-logic change, so no four-surface or §6-narrative update (the gate-21 narrative does not enumerate exempt files).
- [`README.md`](../../README.md): library CalVer `2026.07.188` to `2026.07.189`, README Version `1.9.549` to `1.9.550`.

### Verification
- Both tools re-run by the orchestrator at apply time (recount, not transcription). Blind-spot map: 66 runner gates (32 common-discovery, 16 target-scoped, 18 not-derivable) over 685 tracked markdown files; 0 non-exempt markdown surfaces scanned by zero scope-derivable gates; known-by-design gate-blind exempt trees `.claude/` 1 and `.working/` 246 files. Mutation probe (against a fresh disposable clone with the marker): 8 detected, 2 clean-pass, 0 missed, 0 false-positive, 0 unjudgeable over the 10-variant library; the disposable copy verified clean (only the marker) after the run; the safety refusals exercised (no-marker and dirty-tree both hard-refuse). The worker's figures (682 tracked / `.working/` 244 at `6e21845`) differ from these because the corpus grew; the shipped figures are the orchestrator's recount at `f0c7be9`.
- `tools/run_all_audits.sh`: all 66 gates pass on the working tree with the three new files and the `EXEMPT_FILES` addition present (the first run failed only on the secret-pattern gate, resolved by the exemption above).
- Batches PR #700's `/validate-pr` (0 findings) and `/retro` rows.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260708-fable/deep-assessment-build/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260708-fable/deep-assessment-build/MANIFEST.md) (merged scratch-side as PR #109; a research delivery verified and applied by the orchestrator, not pasted). The manifest's count-correction flag (66 runner gates, not the earlier 67) and its four staged-default open decisions were confirmed at apply time; the mutation probe's disclosed worker-side incident (a development-build revert loop that once ran against a clean live local checkout, restored byte-identical) is the reason the shipped tool carries the third clean-tree safety condition.

## 2026-07-08, Library Version 2026.07.188, PR #700

The `/resume` close-out for the 2026-07-08 attended-autonomous daytime session (resumed from the #699 session-closing handoff). Runs Sweep 89 (the loop-break corpus-wide `/validate` over the #687..#699 deltas, the compensating control for the #699 handoff's skipped trailing QA), ends overnight mode, prunes the handoff, and acquires the concurrency lease. Sweep 89 returned one in-window warning (C-1), fixed here; no contradiction of any #687 to #698 asserted-clean surface, so the loop-break compensating control passes.

### Changed
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) (`1.16.59` to `1.16.60`): the C-1 fix. The §6 gate-59 detailed-prose narrative and its §5 grouped-list echo still described the static `CUTOFF_PR = 463` comparison boundary; PR #695 had replaced that with a dynamic floor (`effective cutoff = max(CUTOFF_PR, oldest PR still present in the in-repo detailed mirror)` under the current-week model) and updated the linter docstring but not the spec narrative. Both passages are rewritten to match the tool: the dynamic floor, the current-week sweep-to-scratch behaviour, the three pre-split-era exemptions (#268/#353/#462) sitting below the floor, and the honest boundary limitation (a dropped floor-defining oldest entry escaping detection, with the sweep tool's deterministic date partition + re-parse assertion and git history as compensating guards). Documentation only; no gate logic changed. Caught by Sweep 89 Subagent C; the audit-gate-change-completeness guard's "when the detection logic changes, the §6 narrative for that gate" surface, which gate 64 (detailed-prose presence) does not check for currency.
- [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated after the spec Version bump (taxonomy first, then the portal generator; [`docs/portal.md`](../../docs/portal.md) unchanged).
- [`.working/overnight-pr.md`](../overnight-pr.md): morning-processed to `Status: stub`, ending overnight mode. The 2026-07-07 and 2026-07-08 overnight run sections were routed (design decisions and closed work already in the durable ledgers via their in-run PRs; the deferred/blocked follow-ups in [`pending-decisions.md`](../pending-decisions.md) / TODO / the handoff; the reference-repo `license:`-schema and re-snapshot-cadence ambiguities noted as `grc_library_ref` concerns; build-progress noise discarded), and a single latest-run closure note replaces the prior one.
- [`.working/session-handoff.md`](../session-handoff.md): pruned to current plus one prior (deleted the `claude/grc-acquisition-reconfirm-brief-k8fppo` next-actions and state-snapshot blocks and the `claude/resume-chptc7` asserted-expectations block; migrate-before-delete confirmed no un-recorded load-bearing item was lost); prepended this session's CURRENT next-actions block and State snapshot; advanced the Resume-cursor to Sweep 89.
- [`.working/session-state.md`](../session-state.md): concurrency lease ACQUIRED (`Active-session: claude/resume-sweep89-deep-assessment`, `Status: active`, fresh heartbeat); Current-task and Worker-dispatches updated.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (`2.0.82` to `2.0.83`): the Sweep 89 row.
- [`README.md`](../../README.md): library CalVer `2026.07.187` to `2026.07.188`, README Version `1.9.548` to `1.9.549`.

### Added
- [`.working/validate-sweeps/2026-07-08-sweep89-iter1.md`](../validate-sweeps/2026-07-08-sweep89-iter1.md): the Sweep 89 per-iteration detail file (six H2 sections; the three subagent returns verbatim, orchestrator synthesis, resulting PR).

### Verification
- Sweep 89: all three subagents dispatched (A recent-PR, B corpus-wide stale-reference, C audit-programme integrity); A and B 0 findings, C 1 in-window warning (C-1) fixed here. Pre-flight scanner 9 candidates, all false positives (comparative/historical phrasing). C-1 validated at source (the gate-59 linter docstring lines 43-72 versus the two spec passages) before the fix; post-fix zero-residual grep of the old static framing confirmed (0 hits for the pre-#695 phrasing; the 3 remaining `463` mentions are the correct floor-baseline usages).
- `tools/run_all_audits.sh` re-run standalone after the edits (below).
- Per-PR QA cadence: this is a normal (non-handoff) PR, so its own `/validate-pr` + `/retro` run after merge and batch into the next PR (Fable PR A).

## 2026-07-08, Library Version 2026.07.187, PR #699

Session-closing handoff PR for the 2026-07-08 OVERNIGHT NUC session (which merged PRs #694 through #698, on the long NUC session that resumed 2026-07-07). Working-state and version-surface only; no corpus normative content changed. Per the standing loop-break exception (PR-workflow step 5a; the `ai-assistant-workflow-disciplines` pack rule) this handoff runs no trailing `/validate-pr` or `/retro`; the compensating control is the next session's `/resume` corpus-wide `/validate` over the #687..#699 deltas, cross-checked against this session's asserted-expectations block.

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): refreshed to the closing state, a CLOSING next-actions block (the maintainer's next-session directive plus the seven deferred questions/clarifications with a recommendation each), the reconciled State snapshot (merged-through #698, versions, green-at-`b516ad9`), and this session's Asserted-expectations block. Not pruned (pruning is the next `/resume`'s job, per the refresh-and-pruning discipline).
- [`.working/session-state.md`](../session-state.md): concurrency lease RELEASED (`Active-session: none`, `Status: released`, heartbeat re-stamped `2026-07-08T11:39:01Z`); the Current-task narrative reconciled to the session's closing arc.
- [`.working/session-metrics.md`](../session-metrics.md) (`1.0.40` to `1.0.41`): added the 2026-07-07-to-2026-07-08 NUC-session row (12 main-repo PRs #687-#698 plus this handoff; subagent-token floor 165,537, the one post-compaction return, the rest pre-compaction and honestly excluded; orchestrator tokens `not instrumented`).
- [`.working/overnight-pr.md`](../overnight-pr.md): recorded the #699 wind-down note; kept `Status: in-flight` (gate 46 passes) for the next session to morning-process as part of ending overnight mode.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (`1.2.473` to `1.2.474`): the #698 `/validate-pr` row (1 immaterial NOTE) and the #699 handoff `SKIPPED (handoff-PR exception)` row.
- [`.working/improvement-log.md`](../improvement-log.md) (`1.0.417` to `1.0.418`): the #698 `/retro` row.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): reworded PR #698's Verification bullet (the #698 `/validate-pr`'s one in-window NOTE: the README catalogue row bumped only Version, not Date, which was already 2026-07-08 from #697 the same UTC day; the "co-bumped" wording was imprecise, the resulting state correct and gate 31 green).
- [`README.md`](../../README.md) (`1.9.547` to `1.9.548`; Library Version `2026.07.186` to `2026.07.187`): the once-per-PR version-surface bump.

### Verification
- 66/66 audit gates plus the pre-push guard green (the #698 `/validate-pr` Subagent A confirmed `All 66 audit gates passed`, EXIT=0 at the pre-handoff `main` `b516ad9`; #699 changes only working-state, version surfaces, and CHANGELOG, so the corpus stays 66/66 at #699's descendant merge). No corpus document body changed. Gate 50 recognizes the #699 handoff-exemption marker in the validate-pr history Findings cell; gate 46 passes on the `in-flight` overnight-PR file; gate 63 passes on the `released` lease.

### Discipline observation
- The one #698 `/validate-pr` finding was an immaterial prose imprecision in #698's own detailed-CHANGELOG Verification bullet ("Version and Date co-bumped" when only Version changed). It is exactly the meta-prose-state-claim class the close-out checklist guards (a bookkeeping-authoring claim not measured against the actual diff); caught by the refute-briefed Subagent A, reworded here per the findings-batch discipline. Immaterial (the resulting state was correct, gate 31 green), so no hot-fix; folded into this handoff.
- The #698 `/validate-pr` was RUN (a refute-briefed Subagent A) rather than marked SUBSUMED into the compensating control, even though #698 is bookkeeping and subsumption would have been gate-50-legitimate: erring on the caution-and-integrity side of the overnight directive, a cleanly-wound-down session clears its owed per-PR QA. Only the #699 handoff's OWN trailing QA takes the loop-break exemption.

## 2026-07-08, Library Version 2026.07.186, PR #698

Folds in PR #697's out-of-window `/validate-pr` notes, batches its QA, and records the deferral of the GR-8-follow-on-A register-ageing advisory tool. Working-state and README-discoverability only; no corpus normative content changed.

### Changed
- [`README.md`](../../README.md) (`1.9.546` to `1.9.547`): added a repository-hygiene-files catalogue row for the new adoption worked example beside the ingestion one (the #697 `/validate-pr` out-of-window discoverability note), and labelled the ingestion row "(ingestion)" for symmetry.
- [`.working/session-state.md`](../session-state.md): the Current-task narrative reconciled to the post-#697 state (FR-63 closed; #695 / #696 / #697 merged; changelog PR 2 / PR 3, the alignment maps, the register-ageing tool, and the egress items all blocked or deferred), heartbeat re-stamped.
- [`TODO.md`](../../TODO.md) §3.15: recorded that the register-ageing advisory tool was prototyped and deferred, with the design finding.
- Batched PR #697 [`/validate-pr`](../validate-pr/history.md) and [`/retro`](../improvement-log.md) rows; [`.working/overnight-pr.md`](../overnight-pr.md) build-progress plus an honest queue-state note.

### Verification
- 66/66 audit gates plus the pre-push guard green. No corpus document body changed except the README catalogue row (README Version bumped; Date already 2026-07-08 from #697, same UTC day, so no Date change; gate 31 green). The register-ageing tool prototype was reverted (not shipped); the tree carries no partial tool.

### Discipline observation
- The register-ageing tool was built, tested, and DEFERRED rather than shipped. Its output over-flagged (roughly 78 in-window false-positive habit-notes even with a cutoff) because the disposition-token heuristic cannot distinguish a formal pending candidate from an adopted-in-place habit or convention note. Shipping an over-flagging advisory would erode trust in its output (the opposite of the precise brief-freshness sibling it was modelled on), so per Quality over Speed it was deferred with a recorded design finding (a formal-candidate classifier or a structured register marker is needed) rather than forced through at the tail of a long session. The two actionable #697 out-of-window notes were folded in; the third (Related-Documents symmetry) was left informational (not gate-enforced; the wiring was deliberately scoped to the worked-example and adopter-guide pair).

## 2026-07-08, Library Version 2026.07.185, PR #697

FR-63 (TODO §2.7): adds a narrative adoption worked example complementing the ingestion worked example, following one fictional adopter (reusing the startup-roadmap Example 1 mid-size SaaS) from clone through the Day-1 floor and the staged Phase 1 / Phase 2 programme with file-by-file decisions. Applied from a research delivery; closes TODO §2.7 / FR-63.

### Added
- [`docs/worked-example-adoption.md`](../../docs/worked-example-adoption.md) (new; Document Type Guide; `1.0.0`): the adoption worked example. Mirrors [`docs/worked-example.md`](../../docs/worked-example.md)'s Guide shape (13-field metadata, narrative sections, Common pitfalls, Summary, no End-of-Document marker). References (does not duplicate) the quickstart, both roadmaps, the decision tree, and the adopter guide.

### Changed
- [`docs/worked-example.md`](../../docs/worked-example.md) (`1.0.3` to `1.0.4`): added the companion to Related-Documents and a one-line ingestion-vs-adoption companion pointer in the intro.
- [`docs/adopter-guide.md`](../../docs/adopter-guide.md) (`1.3.9` to `1.3.10`): added the companion to Related-Documents.
- [`tools/lint-metadata.py`](../../tools/lint-metadata.py): added the new document's basename to `PREFIX_EXEMPT_BASENAMES` (the docs/ meta-doc naming class; the sibling worked-example, adopter-guide, and decision-tree Guides are already members, since a Type-Guide document otherwise requires a `guide-` filename prefix).
- [`TODO.md`](../../TODO.md): §2.7 deleted (closed), the line-47 apply-ready phrase and the P2 backlog-totals (11 to 10 open) reconciled; [`.working/DONE.md`](../DONE.md) gains the closure entry.
- Bookkeeping: batched PR #696 [`/validate-pr`](../validate-pr/history.md) and [`/retro`](../improvement-log.md) rows; [`.working/overnight-pr.md`](../overnight-pr.md) build-progress; [`.working/session-state.md`](../session-state.md) lease refresh.

### Verification
- 66/66 audit gates + the pre-push guard green. The new document passes gate 1 (via the meta-doc class exemption) and gate 2 (its "Step N:" headings were CONFORMED to sentence-case by capitalizing the first word after the label, not exempted, because this document does not demonstrate the house-style rules the way the ingestion worked example does). Every referenced corpus file was verified to exist. docs/ meta-docs are not taxonomy-tracked, so the generated taxonomy, portal, and scorecard are unchanged.

### Worker provenance
- **Worker provenance:** applied from [`inbox/worker-20260703-a/fr-63-adoption-worked-example/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260703-a/fr-63-adoption-worked-example/MANIFEST.md) (a research delivery, not final prose). The delivery was 77 commits stale (staged against `ede2e3b`); a fresh-context re-read reconciled current state and drafted, and the orchestrator re-verified and authored the final prose under the language gate.

### Discipline observation
- The stale scaffold's wiring plan (add the companion to the adopter entry-point lists) was CORRECTED at apply-time: the fresh-context re-read established that doing so would force a "five to six" count cascade across five entry-point lists plus hardcoded text in the portal generator, and would misclassify a walkthrough as a composition path. The mutual-Related-Documents-pointer wiring (matching how the ingestion worked example is already wired) was used instead. Two scaffold items the orchestrator verified rather than trusted: the IAM-policy Owner role (confirmed "Chief Information Security Officer"), and the new-document version start (resolved to `1.0.0`: zero `0.0.x` documents exist in the taxonomy, and this document ships as an active, maintainer-approved artefact).

## 2026-07-08, Library Version 2026.07.184, PR #696

TODO 1.11 residual: confirms the ANPD Resolution CD/ANPD No. 15/2024 "deadlines doubled for small-scale agents" sub-clause against the resolution text, the last open residual of the Brazil citation verification (the six citations and the base deadlines were primary-verified in #691). Secondary-tier confirmation; TODO 1.11 stays open, narrowed to a primary-source re-confirmation.

### Changed
- [`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md) (`1.1.2` to `1.1.3`): the "pending confirmation against the full Resolution 15/2024 text" caveat replaced with the confirmed reading, Article 6 §8 doubles both the ANPD-notification deadline (3 to 6 business days) and the 20-business-day complementary-information window (to 40), and Article 9 §6 doubles the data-subject-notification deadline (3 to 6 business days), "contados em dobro para os agentes de pequeno porte" (small-scale-agent definition per Resolution CD/ANPD No. 2/2022), plus an honest note that this is verified against independent reproductions and a primary `.gov` / Diário Oficial re-confirmation remains pending.
- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.26` to `1.4.27`): the Brazil breach-matrix cell's "pending confirmation" sub-clause updated to the confirmed state (Article 6 §8 and Article 9 §6, "contados em dobro"; primary re-confirmation pending), matching the annex.
- [`TODO.md`](../../TODO.md): item 1.11 narrowed (the doubling confirmed against the resolution text 2026-07-08; the only residual is a primary-source re-confirmation, recorded as the accepted-unverified tracker); the phantom-`3.4` positional pointer at line 7 repointed to `3.1` (the #695 `/validate-pr` out-of-window note).
- [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated from the two version bumps.
- Bookkeeping: [`.working/pending-decisions.md`](../pending-decisions.md) (the changelog-restructure PR-2 blocked / PR-3 deferred records, Status now 1 pending); [`.working/overnight-pr.md`](../overnight-pr.md) 2026-07-08 build-progress; [`.working/session-state.md`](../session-state.md) lease refresh; batched #695 [`/validate-pr`](../validate-pr/history.md) and [`/retro`](../improvement-log.md) rows.

### Verification
- The doubling was verified against THREE consistent reads of the resolution text: a research worker's two independent legislation-reproduction sources plus the orchestrator's independent re-fetch of one of them (legisweb id=458235). Article 6 §8 ("Os prazos constantes no caput e no § 3º deste artigo são contados em dobro para os agentes de pequeno porte") and Article 9 §6 ("O prazo constante no caput deste artigo é contado em dobro para os agentes de pequeno porte") were quoted verbatim, consistent across sources, with consistent article numbering.
- The ANPD's own incident-communication page (`www.gov.br/anpd/.../comunicado-de-incidente-de-seguranca-cis`, the register's recorded upstream URL) reproduces only the base 3-business-day and 20-business-day deadlines, NOT the small-agent doubling (it is a summary page), so it neither confirms nor refutes the sub-clause; the full-text primary sources (the Diário Oficial original and a state-gov PDF mirror) were unreachable this session (ECONNREFUSED / 403 / 404). The confirmation is therefore SECONDARY-tier, and TODO 1.11 is kept open for a primary re-confirmation (the accepted-unverified tracker).
- Pre-push guard green (66/66 audit gates + D1-D7 + history-aware 31/40/45); [`tools/build-taxonomy.py`](../../tools/build-taxonomy.py) and [`tools/build-portal.py`](../../tools/build-portal.py) regenerated then `--check`-clean.

### Discipline observation
- Research-assistant discipline applied end to end: the worker surfaced quoted candidate text from primary-reproduction sources; the orchestrator independently re-fetched to re-verify before authoring, and did NOT overclaim primary-tier verification the sources did not support. The primary-tier gap is recorded honestly (annex, matrix, and TODO 1.11 all carry the "primary re-confirmation pending" note) rather than papered over, per accuracy-over-completeness.

## 2026-07-08, Library Version 2026.07.183, PR #695

CHANGELOG-restructure machinery, step 1 of the maintainer-directed current-week model (TODO 3.19). Adds a dynamic cutoff to the mirror header-parity gate (59), the data-safe sweep tool [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py), a [`.gitattributes`](../../.gitattributes) `export-ignore` on the working-state directory, and the model documentation; no data is moved yet. Tooling and working-state records only; no corpus normative content changed.

### Added
- [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py): the current-week sweep tool (not an audit gate; an orchestrator follow-up step). Identifies the completed-week detailed-CHANGELOG entries and the pre-current-week dated per-run record files (the `history.md` indexes, operational files, and READMEs stay in-repo), and offers `--dry-run` (default), `--emit-archive DIR` (write the weekly Monday-dated archives + copy record files to the scratch archive), and `--prune` (rewrite the in-repo mirror to current-week-only + delete the swept record files). Data-safe: `--prune` requires `--verify-archived DIR` and refuses unless every artefact already exists in the archive.
- [`.gitattributes`](../../.gitattributes): `export-ignore` on the working-state directory so `git archive` exports/release tarballs are fork-clean (the TODO 3.19 resolution). Scope note in-file: this affects `git archive` only, not `git clone`/history.

### Changed
- [`tools/lint-changelog-mirror-header-parity.py`](../../tools/lint-changelog-mirror-header-parity.py) (gate 59): the fixed `CUTOFF_PR` is now a FLOOR; the effective cutoff is `max(CUTOFF_PR, oldest PR still in the in-repo mirror)` (new `effective_cutoff`). A swept (scratch-only) entry is out of parity scope rather than flagged missing, while a genuine in-window drift still fails. On the current unswept mirror the effective cutoff resolves to 463, i.e. behaviour is identical to before.
- [`.working/changelog-details/README.md`](README.md): documents the current-week model, the sweep tool, and the dynamic gate-59 cutoff.
- [`.working/overnight-pr.md`](../overnight-pr.md), [`.working/session-state.md`](../session-state.md): the 2026-07-08 overnight-run authorization and the refreshed concurrency lease (overnight mode, this branch, fresh heartbeat).
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 7 stages the change-tracking rule/skill + CLAUDE.md descriptive edits and the per-PR sweep-step wiring for the daytime apply.
- [`TODO.md`](../../TODO.md): adds P3 item 3.19 (the restructure, its remaining PRs, and the supersedes-the-full-migration note) and corrects the stale P3 backlog-totals count (was "5 items" listing a phantom 3.4 and omitting 3.16/3.17/3.18; now 8 items).

### Verification
- Gate 59 test class passes (10 tests, including 2 new dynamic-cutoff cases: a swept root-only entry above the fixed floor is NOT flagged; a genuine in-window miss still IS). `effective_cutoff` confirmed = 463 on the current mirror (no behaviour change now).
- Sweep tool exercised read-only: `--dry-run` (29 current-week entries kept, 647 swept across 5 weeks, 204 record files); `--emit-archive` to a scratchpad dir with a round-trip integrity check (676 original entry headers == 676 kept+archived, 0 lost, 0 bodies dropped); `--prune` guard refuses (exit 1, touches nothing) without a complete `--verify-archived` archive, and the `--prune` rewrite carries a post-rewrite re-parse assertion that aborts before any deletion if the constructed mirror would drop or duplicate an entry.
- Full `run_all_audits.sh` + `run-pr-time-checks.sh` (the pre-push guard) green.

### Why this is a separate PR
Machinery first, no data moved: the dynamic gate + the sweep tool + the export-ignore are fully in-repo and CI-verifiable in isolation, so the sensitive cross-repo data movement (PR 2) and the large root reformat (PR 3+) land on a proven foundation.

## 2026-07-08, Library Version 2026.07.182, PR #694

Follow-up corrections from the `/full-qa` review of PR #693. Completes the organization-neutrality terminology reframe across the quality-review documents, clears stale references to the retired organization-specific check (a tool docstring, the audit-programme gate-2 narrative, a linter exemption comment), disambiguates a duplicated section title, and reconciles the working-state handoff snapshot. Documentation, comment, and working-state records only; no corpus normative content changed. Batches PR #693's `/validate-pr` (QA performed via `/full-qa`; 6 findings, all fixed here) and `/retro` rows.

## 2026-07-08, Library Version 2026.07.181, PR #693

Update and clarification of reference information. Clarifies reference-handling documentation and working-state records, and retires an obsolete organization-specific check in favour of the general organization-neutral contribution rule. No corpus normative content changed; the documentation model, gates, and framework alignments are unaffected.

## 2026-07-07, Library Version 2026.07.180, PR #692

Citation cleanup + batched #691 `/validate-pr` fixes. See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary.

### Changed
- [`security/standard-threat-modelling.md`](../../security/standard-threat-modelling.md) (`1.0.4` to `1.0.5`) and [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md) (`1.27.60` to `1.27.61`): the 2 `NIST SP 800-154` supplementary-framework references replaced with the OWASP Threat Modeling Cheat Sheet (never-finalized draft to finalized source; maintainer Q3 choice). SP 800-154 now has 0 corpus occurrences.
- [`TODO.md`](../../TODO.md): 1.11 rescoped to its residual (the small-agent-doubling sub-clause of Resolution 15/2024) since the verification landed in #691; the stale `19/2023` corrected to `19/2024` (F1). Added item 2.14, the `/reference-audit` cadenced skill (maintainer-directed).

### Fixed
- **#691 `/validate-pr` F1 (Medium)**: TODO 1.11 reconciled and the surviving `19/2023` at `TODO.md:41` corrected (the completion-scope class recurring inside the backlog file, which the pre-push corpus grep excluded).
- **#691 `/validate-pr` F2 (Low)**: the #691 detailed-CHANGELOG Verification line said 3 docs were version-bumped when 4 were; corrected to 4.

### Removed
- TODO 1.13 (SP 800-154 replacement), closed and rotated to [`.working/DONE.md`](../../.working/DONE.md).

### Batched QA rows
- The #691 [`/validate-pr`](../validate-pr/history.md) history row (2 in-window findings F1 + F2, fixed here) and the #691 [`/retro`](../improvement-log.md) row (the recurring completion-scope pattern + the maintainer gap-first lesson).

### Verification
- Full pre-push guard green; a skeptical verifier subagent ran pre-push. Per-document Version + Date co-bumped on the 2 touched corpus/register docs; [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) regenerated; library CalVer `2026.07.179` to `2026.07.180`, README `1.9.540` to `1.9.541`.

## 2026-07-07, Library Version 2026.07.179, PR #691

Brazil ANPD citation verification (TODO 1.11) + batched #690 `/validate-pr` fixes. See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary. All six Brazilian citations verified against Planalto / gov.br/anpd primary sources this turn (NUC egress reaches them; only iso.org 403s).

### Changed (verified against primary sources 2026-07-07)
- [`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md) (`1.1.1` to `1.1.2`): removed the pending-verification annotations on the Lei No. 15.352/2026 / Medida Provisória No. 1.317/2025 / LGPD Article 55-A block (all confirmed on planalto.gov.br) and on Resolution CD/ANPD No. 15/2024 + No. 2/2022 (confirmed on gov.br/anpd); added the confirmed dates (Lei 25 February 2026, Res 15/2024 24 April 2024, Res 2/2022 27 January 2022).
- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md) (`1.4.25` to `1.4.26`): removed the broad pending annotations on the two Resolution 15/2024 citations (the breach-notification table's Brazil row and the notification-clocks bullet), added the verified-2026-07-07 marker.
- [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) (`1.5.14` to `1.5.15`): Resolution CD/ANPD No. 15/2024 row `Last verified (UTC)` 2026-07-02 to 2026-07-07 (currency axis only; no content caveat, per the register's two-axis convention).

### Fixed
- **Citation correction**: the standard-contractual-clauses instrument is Resolution CD/ANPD **No. 19/2024** (23 August 2024), not No. 19/2023 (a year error); corrected at all three live occurrences: two in [`privacy/jurisdictions/annex-privacy-brazil.md`](../../privacy/jurisdictions/annex-privacy-brazil.md) and one in the cross-jurisdiction summary table of [`privacy/annex-privacy-jurisdiction-index.md`](../../privacy/annex-privacy-jurisdiction-index.md) (`1.0.9` to `1.0.10`, the third caught by the pre-push skeptical verifier as a corpus-wide-completion-scope miss and fixed before push).
- **#690 `/validate-pr` W1**: `SP 800-154` occurrence count corrected 3 to 2 (measured via grep, matching the validate-pr's independent count) across TODO 1.13, both CHANGELOG #690 entries, and [`.working/overnight-pr.md`](../overnight-pr.md); characterization corrected too (2 framework-list enumerations, not "3 authoritative citations").
- **#690 `/validate-pr` N1**: [`.working/overnight-pr.md`](../overnight-pr.md) #22 status reconciled (in-flight to merged) and build-progress refreshed (#23 merged, Tier-C staged, GSA held).

### Retained caveat
- The "deadlines doubled for small-scale agents" sub-clause of Resolution 15/2024 stays flagged pending confirmation against the full resolution text (the only Brazil item not grounded on a primary page this turn).

### Batched QA rows
- The #690 [`/validate-pr`](../validate-pr/history.md) history row (2 in-window findings W1 + N1, fixed here) and the #690 [`/retro`](../improvement-log.md) row.

### Verification
- Full pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green; a skeptical verifier subagent ran pre-push (substantive corpus citation change). Per-document Version + Date co-bumped on the 4 touched corpus/register docs (annex, jurisdiction-index, procedure, register); library CalVer `2026.07.178` to `2026.07.179`, README `1.9.539` to `1.9.540`.

## 2026-07-07, Library Version 2026.07.178, PR #690

Overnight-run setup and accumulated-bookkeeping flush. See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary. `.working/` + [`TODO.md`](../../TODO.md) + version surfaces only; no corpus document body changed.

### Changed
- [`.working/overnight-pr.md`](../overnight-pr.md) `stub` to `in-flight`, filled with the 2026-07-07 overnight authorization scope (6 numbered directives: autonomous overnight; cross-repo parallelism with serial ref-catalogue merges; all-reachable-source egress; the ISO-current-as-of-2026-07-01 ruling; SP 800-154 replace; complete-relevant-ref-then-pivot), the build-progress ledger (ref PRs #5-22, scratch #108, corpus #687-689), and the remaining ref + corpus queues. The overnight morning-processing PR routes this content and resets to `stub` (gate 46 lifecycle).

### Added
- [`TODO.md`](../../TODO.md) **1.13**: replace the never-finalized `SP 800-154` (Data-Centric System Threat Modeling, 2016 IPD, no final) citations (2 occurrences, both framework-list enumerations) with a finalized source and drop the draft citation (maintainer Q3 decision 2026-07-07; NIST-harvest-surfaced).
- [`TODO.md`](../../TODO.md) **RB-6**: reference-base currency + draft watch (the IR 8596 / COSAiS / Privacy Framework 1.1 draft-watch; the FedRAMP 2026 evolving-preview re-snapshot cadence).
- [`TODO.md`](../../TODO.md) 1.11 (Brazil ANPD) annotated unblocked by the reachable NUC egress.

### Fixed
- [`.working/improvement-log.md`](../improvement-log.md): the #688 and #689 `/retro` rows were malformed (the #688 row's leading `| 2026-07-07 | #688 |` cells were lost, mashing it onto the #689 line, and both rows merged their Pattern and Proposed-improvement cells into one). Split into correct rows; all four recent rows now parse as 7 columns (verified by pipe-count).

### Batched QA rows
- The #687 (0 findings), #688 (2 warning + 1 note, one root miss fixed in #689), and #689 (0 findings) [`/validate-pr`](../validate-pr/history.md) rows and their [`/retro`](../improvement-log.md) rows, accumulated across the reference-library split PRs per recursion-avoidance.

### Verification
- `tools/run_all_audits.sh` all gates green on the committed state; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green. No corpus document body changed, so no per-document version bump; library CalVer `2026.07.177` to `2026.07.178` and README `1.9.538` to `1.9.539`.

## 2026-07-07, Library Version 2026.07.177, PR #689

Completes the reference-library split cutover 3b (the grc_library re-point). See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary. PR #688's "every live surface" re-point claim was falsified by its own post-merge `/validate-pr`: the surface-discovery grep was Markdown-only, so it missed a `.py` tool + prose.

### Fixed

- **`tools/verify-reference-modules.py` re-pointed to `grc_library_ref`** ([`tools/verify-reference-modules.py`](../../tools/verify-reference-modules.py)). This live maintainer dev-aid (the code-set parity check that confirms the in-repo `ccm_aicm_reference.py` / `nist_csf_reference.py` / `cobit_iso31000_reference.py` modules match the source extracts) named the reference base at the old `grc_library_scratch/ref/` location 5 times and assumed the `ref/`-prefix bucket layout the split eliminated. Re-pointed: docstring bucket paths drop the `ref/` prefix (buckets at the `grc_library_ref` root); `locate_source` default `../grc_library_scratch/ref` (+ the stale `/home/user/...` absolute) replaced with `../grc_library_ref`; env `GRC_SCRATCH_REF` renamed `GRC_REF_ROOT`; the back-compat parent-resolution, SKIP notice, and drift/OK messages re-pointed. The source-extract path MAP (`frameworks/CSA/...`, `standards/NIST/...`) was already root-relative, so it is unchanged. A live run resolves `../grc_library_ref` and reports all five modules match CCM v4.1.0, AICM v1.1.0, NIST CSF 2.0, COBIT 2019, and ISO 31000:2018.
- **Runbook §6 obligation-1** ([`.working/multi-session-orchestration.md`](../../.working/multi-session-orchestration.md)): three residual "scratch base"/"scratch source" phrases describing the parity aid re-pointed to `grc_library_ref` (the section's surrounding prose was already re-pointed in #688); `Version 1.1.5` to `1.1.6`.
- **CHANGELOG overclaim corrected**: #688's "every live surface" claim is acknowledged as incomplete (it missed the two surfaces above) and completed here.

### Verification

- Corpus-wide completion grep at **full file-type width** (`tools/`, `governance/`, `docs/`, all domain dirs, `.claude/`, the runbook, not Markdown alone): the only remaining live reference-base residuals were `verify-reference-modules.py` + the runbook 3 phrases, both fixed here. `tools/audit-brief-freshness.py` references `grc_library_scratch` for the WORKER-EXCHANGE (staged briefs, `research/COVERAGE.md`), correctly retained as scratch (confirmed at source: not the reference base).
- `python3 tools/verify-reference-modules.py` exit 0, resolves `../grc_library_ref`, all modules match; no scratch residual in the tool.
- `tools/run_all_audits.sh` = 66/66 green on the committed state; pre-push guard green (D1-D7). Library `2026.07.176` to `.177`, README `1.9.537` to `.538`.
- Per-PR `/validate-pr` + `/retro` for this PR run after merge and batch into the next PR.

## 2026-07-07, Library Version 2026.07.176, PR #688

Reference-library split, cutover step 3b (the grc_library re-point). See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary. The reference base was split out of `grc_library_scratch/ref/` into the dedicated private `grc_library_ref` repo (step 3a: its own `validate.py` gate green, generated artefacts verified byte-identical to scratch modulo the prefix, CI + PR round-trip verified). This PR re-points every live grc_library reference to the new location. Location/name change only; no normative, trust, currency, or step content changed.

### Changed

- **Governance corpus (2 versioned docs).** [`governance/specification-citation-verification.md`](../../governance/specification-citation-verification.md) §6.6 (title "Local reference base (the scratch `ref/` tree)" to "... (the `grc_library_ref` repo)") plus its §12.3 and superseded-archival references; `Version 1.2.8` to `1.2.9`, `Date` to 2026-07-07. [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) currency-SOP reference; `Version 1.5.13` to `1.5.14`, `Date` to 2026-07-07. Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) (taxonomy first).
- **Protected `.claude/` + pack.** The `## Reference-version currency` SOP in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md); the reference-knowledge-base step in [`.claude/commands/resume.md`](../../.claude/commands/resume.md); the [`matrix-fit`](../../dev-security/claude-rules/skills/matrix-fit/SKILL.md) and [`claim-fit`](../../dev-security/claude-rules/skills/claim-fit/SKILL.md) skills and their commands. Maintainer-authorized (the full-cutover go-ahead). Pack `1.54.6` to `1.54.7` (patch; version-history row added).
- **The claim-fit triage tool** [`tools/audit-claim-precision.py`](../../tools/audit-claim-precision.py): `find_scratch` to `find_ref_base` (default `REPO_ROOT.parent / "grc_library_ref"`, detection by `catalogue.yml` at root), `held_families` reads `INDEX.md`/`catalogue.yml` at root (was `ref/INDEX.md`/`ref/catalogue.yml`), flag `--scratch` renamed `--ref-base` and env `GRC_SCRATCH_PATH` to `GRC_REF_PATH`, docstring/messages re-pointed. The claim-fit skill + command prose updated to match the flag rename. Self-test passes; a live run against the `grc_library_ref` default resolves held-state.
- **Working-state.** §6 of [`.working/multi-session-orchestration.md`](../../.working/multi-session-orchestration.md) re-headed to describe the reference base living in `grc_library_ref` (buckets at root), preserving the trust-split / ingestion / currency-SOP / superseded-archival content; ref-write mechanics re-pointed to `grc_library_ref` via `gh` PR while worker-exchange write mechanics stay scratch; `Version 1.1.4` to `1.1.5`. The standing reference-index pointer in [`.working/session-handoff.md`](../../.working/session-handoff.md); the ref-base pointers in [`.working/worker-brief-template.md`](../../.working/worker-brief-template.md).
- **[`TODO.md`](../../TODO.md).** Re-pointed the reference-base path mentions and re-headed the "Scratch reference-base work" block to "Reference-base work (`grc_library_ref`)", preserving the closed items' historical scratch-PR provenance (they were done pre-split on scratch) and re-pointing the open SR-1/2/3 to `grc_library_ref` (SR-3's stale scratch `validate.py` line numbers generalized to by-name references, since grc_library_ref's `validate.py` dropped the worker-exchange checks 14/15). The forker-own-`ref/`-tree convention (§4.5 / §5.x) left generic (it describes what a forker builds, not the maintainer's base).

### Fixed

- **Pre-existing gate-23 false-positive.** The §3.18 TODO item (added earlier this session, uncommitted at #687) contained the literal `settings.local.json`, whose `settings.local` substring gate 23 (Internal references audit) read as an internal `.local` mDNS hostname. Reworded to "a machine-local, git-ignored settings-override file" (the exact filename is named when the env-detection PR is built). Surfaced by the 3b re-point's audit run (65/66); it was absent at HEAD `df04241` because §3.18 was not part of #687.

### Not touched (scope)

- Frozen archives (the `.working/validate-*`, `full-qa`, `matrix-fit`/`claim-fit` records, `design-decisions`, CHANGELOG, DONE, and the pack README version-history table rows) record the old scratch location as-of-write-time and are preserved verbatim.
- Scratch worker-exchange references (`inbox/`, `requests/`, `research/`, `claims-ledger.md`, `COVERAGE.md`, worker write-access) stay `grc_library_scratch`; only the reference-base role moved.

### Verification

- `tools/run_all_audits.sh` = 66/66 green on the committed state (gate 23 clean after the §3.18 reword; gates 3/33/34/40 + intra-doc-ref confirm the re-pointed links, generated-artefact sync, and version bumps). Clone non-shallow.
- `audit-claim-precision.py` self-test passes; live run against the `grc_library_ref` default resolves held-state (was UNKNOWN); no scratch/ref residual in the tool.
- Zero residual `grc_library_scratch/ref` path in the re-pointed live files (frozen archives excluded by design); the two governance docs' meaning preserved (currency SOP, trust model, check order unchanged).
- A refute-briefed skeptical verifier reviewed the diff pre-push (substantive multi-surface + versioned-corpus + protected-pack change). Pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh` D1-D7 incl. the D7 handoff-token check) green, run standalone and unpiped.
- Per-PR `/validate-pr` + `/retro` for this PR run after merge and batch into the next PR.

## 2026-07-07, Library Version 2026.07.175, PR #687

Sweep-88 close-out and `/resume` first PR for the 2026-07-07 resumed session (`claude/sweep88-todo112-nuc-resume`, DAYTIME-UNATTENDED, on the maintainer's NUC). Runs the loop-break corpus-wide `/validate` (Sweep 88) over the #685 to #686 deltas, the compensating control for session-closing handoff PR #686, and fixes both of its two out-of-window low-severity findings. See the root [`CHANGELOG.md`](../../CHANGELOG.md) for the lead summary.

### Fixed

- **TODO 1.12 (annual-review-domain-scope): the annual-review procedure omitted architecture from its Scope domain enumeration.** [`governance/procedure-grc-programme-management-and-annual-review.md`](../../governance/procedure-grc-programme-management-and-annual-review.md) §2.1 (line 29) listed 10 governance domains and omitted architecture, while its two sibling "spans all governance domains" completeness enumerations both carry 11 including architecture ([`governance/standard-maturity-assessment-methodology.md`](../../governance/standard-maturity-assessment-methodology.md) and [`governance/framework-governance-performance-and-improvement.md`](../../governance/framework-governance-performance-and-improvement.md), the latter fixed in #685); `architecture/` is a real corpus domain dir, so a procedure asserting it spans ALL library documents cannot omit it. Added `architecture` to the Scope enumeration (placed to match the framework-governance tail ordering), bringing all three completeness enumerations to 11 domains. Bumped the procedure `1.0.7` to `1.0.8` and Date to 2026-07-07 in the same commit, and regenerated [`taxonomy.yml`](../../taxonomy.yml) then [`docs/portal.md`](../../docs/portal.md) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) (taxonomy first, then the taxonomy-derived artefacts). Provenance: #685's owed `/validate-pr` finding A-1, re-surfaced by Sweep 88 exactly as the k8fppo asserted-expectations predicted.
- **Stale illustrative inventory comment in the guardrail-cadence linter.** [`tools/lint-guardrail-cadence.py`](../../tools/lint-guardrail-cadence.py) line 74 carried an `e.g.` regex-format illustration reading `"inventory 59 gates / 12 rules / 17 skills / 10 commands"`; the example numbers were stale against the live inventory. Refreshed to `66 gates / 12 rules / 18 skills / 11 commands`. Not a currency claim and gate-exempt (a Python comment), so no gate tripped; refreshed to keep the illustration accurate and stop the next sweep re-flagging it. Provenance: Sweep 88 Subagent C.

### Changed

- **[`.working/session-handoff.md`](../../.working/session-handoff.md) pruned and reconciled** per the `/resume` first-PR discipline: prepended this session's Next-actions and State-snapshot blocks (with the reconciled Current-truth line: merged through #687, library `2026.07.175`, README `1.9.536`, gate/suite/rules/skills/commands 66/346/12/18/11), pruned the oldest block in each per-session stack to keep current + 1 prior (removed the `claude/resume-chptc7` Next-actions and State-snapshot blocks and the `claude/resume-tl5rez` asserted-expectations block, all durably recorded in CHANGELOG / DONE / the validate-sweeps history / git), advanced the sweep cursor to Sweep 88, and reconciled the operating mode to DAYTIME-UNATTENDED and the reference-base framing to the scratch -> scratch + `grc_library_ref` split (superseding the #686 single-scratch-reference framing). Migrate-before-delete confirmed: the pruned blocks carried no un-recorded forward-looking item (their Sweep records are in the history file, their decisions are historical/superseded, the DD-10 git-proxy note is a cloud-only issue moot on the NUC).
- **[`.working/session-state.md`](../../.working/session-state.md) concurrency lease ACQUIRED**: `Active-session` set to `claude/sweep88-todo112-nuc-resume`, `Status: active`, fresh heartbeat, `Current-task` updated to the NUC daytime-unattended state and the split-first queue.
- **[`TODO.md`](../../TODO.md)**: deleted the §1.12 item (closed); rotated to [`.working/DONE.md`](../../.working/DONE.md).
- **[`.working/validate-sweeps/history.md`](../../.working/validate-sweeps/history.md)** (`2.0.80` to `2.0.81`): added the Sweep 88 iter 1 row; detail in [`.working/validate-sweeps/2026-07-07-sweep88-iter1.md`](../../.working/validate-sweeps/2026-07-07-sweep88-iter1.md).

### Verification

- Mechanical baseline `tools/run_all_audits.sh` = 66/66 green at `df04241` (resume baseline) and re-run green on the committed state before push. Clone non-shallow. [`tools/run-linter-regression.py`](../../tools/run-linter-regression.py) exit 0.
- Sweep 88: full three-subagent dispatch (A recent-PR, B corpus stale-reference, C audit-programme integrity); pre-flight scanner 9 candidates all dismissed as false positives (comparative/current-count wording); 2 distinct findings after dedupe, both out-of-window and low-severity, both fixed this PR; no asserted-expectation contradiction; the loop-break compensating control for #686 PASSES.
- Generated-artefact regen order honoured (taxonomy first, then portal/scorecard); the taxonomy/scorecard/portal diffs are the single procedure version/date bump plus the regen-date headers, verified.
- Pre-push: `tools/pre-push-guard.sh` (corpus gates from HEAD + the PR-time delta checks D1-D7 plus the history-aware 45/40/31 against the merge base) run standalone and unpiped before the push.
- Per-PR QA (this is not a session-closing handoff PR): the formal `/validate-pr` + `/retro` run after merge and batch into the next PR.

## 2026-07-07, Library Version 2026.07.174, PR #686

Session-closing handoff PR for the `claude/grc-acquisition-reconfirm-brief-k8fppo` session. The session resumed from #684, ran the loop-break Sweep 87 (shipped as #685), and authored the maintainer-directed maximal-scope acquisition-and-reconfirm brief into `grc_library_scratch` (scratch PR #107) alongside the owed coverage-sync (scratch PR #106). A mid-session GitHub-MCP token expiry plus git-push credential outage took the PR and merge pipeline down, so the overnight run was transferred to the maintainer's NUC egress instance (working `gh` CLI and egress); connectivity was restored at wind-down, the two scratch PRs were self-merged (per the maintainer's Q4=B direction), and the session closes here.

### Changed

- [`.working/session-handoff.md`](../../.working/session-handoff.md): reconciled the k8fppo Next-actions and State-snapshot blocks to the closing and NUC-transfer state (the MCP and git outage resolved at wind-down, scratch #106 and #107 self-merged, the overnight queue handed to the NUC); prepended the k8fppo asserted-expectations block; updated the Current-truth version tokens to this PR's values (D7-validated).
- [`.working/session-state.md`](../../.working/session-state.md): released the concurrency lease (Active-session none, Status released, fresh heartbeat `2026-07-07T01:04:49Z`); reconciled the Current-task and Worker-dispatches lines to the closing state.
- [`.working/session-metrics.md`](../../.working/session-metrics.md): added the k8fppo session row (measured-floor 1,281,483 subagent tokens across 5 subagents; version `1.0.38` to `1.0.39`).

### Added

- [`.working/validate-pr/2026-07-07-PR-685.md`](../../.working/validate-pr/2026-07-07-PR-685.md): the per-PR record for #685's owed `/validate-pr` (refute-briefed Subagent A; 1 out-of-window finding, 0 in-window; cross-reference check 0 breaks).
- Rows in [`.working/validate-pr/history.md`](../../.working/validate-pr/history.md): the #685 row (1 finding, routed) and the #686 row (handoff-PR exception marker in the Findings cell); version `1.2.461` to `1.2.462`.
- The #685 `/retro` row in [`.working/improvement-log.md`](../../.working/improvement-log.md): records the fix-at-class-width recurrence (the #685 Sweep-87 fix asserted "no parallel enumeration carrier survives" but a third carrier survived); version `1.0.405` to `1.0.406`.
- Item 1.12 in [`TODO.md`](../../TODO.md): the routed annual-review architecture-omission fix (Priority 1, precisely scoped to [`governance/procedure-grc-programme-management-and-annual-review.md`](../../governance/procedure-grc-programme-management-and-annual-review.md) line 29; the class was verified bounded to three domain-model enumerations by a corpus-wide family grep).

### Verification

- Pre-push guard green: `tools/run_all_audits.sh` 66/66 plus `tools/run-pr-time-checks.sh` (D1 to D7, including D7 handoff-snapshot freshness against the reconciled Current-truth tokens). No corpus document body changed, so no per-document `Version` or `Date` bump and no generated-artefact regeneration were required (a [`taxonomy.yml`](../../taxonomy.yml) / [`docs/portal.md`](../../docs/portal.md) / [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) `--check` stays clean).
- Per the standing loop-break exception this session-closing handoff PR takes no trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 88 over the #685 to #686 deltas), which runs on the maintainer's NUC and cross-checks against this session's asserted-expectations block.

## 2026-07-06, Library Version 2026.07.173, PR #685

Sweep-87 close-out and `/resume` first PR for the 2026-07-06 resumed session (`claude/grc-acquisition-reconfirm-brief-k8fppo`). Runs the loop-break corpus-wide `/validate` (Sweep 87) over the #680 to #683 deltas and applies the single note-level finding it surfaced.

### Changed

- [`governance/framework-governance-performance-and-improvement.md`](../../governance/framework-governance-performance-and-improvement.md) (`1.0.5` to `1.0.6`): added `architecture` to the Scope line's governance-domain enumeration (from 10 to 11 domains), aligning it to the authoritative [`governance/standard-maturity-assessment-methodology.md`](../../governance/standard-maturity-assessment-methodology.md):34 and [`docs/template-maturity-self-assessment.md`](../../docs/template-maturity-self-assessment.md) (Section 9: Architecture domain), both of which enumerate architecture; `architecture/` is a genuine corpus domain directory. Sweep-87 Subagent A finding A-F1, validated at source (the framework had zero mentions of architecture; the derived standard and the template both list it) and fixed at the width of the finding (the only two domain-list enumerations already included architecture, so no parallel carrier survives).
- [`taxonomy.yml`](../../taxonomy.yml), [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md): regenerated (taxonomy first, then the scorecard which derives from it) to reflect the framework's `1.0.6` bump; `build-taxonomy.py --check` and `build-portal.py --check` clean post-regen.
- [`.working/session-handoff.md`](../session-handoff.md): pruned per the `/resume` first-PR discipline (keep current + 1 prior in each per-session stack: the 2026-07-05 `claude/resume-tl5rez` Next-actions, State-snapshot, and #645-#659 Asserted-expectations blocks removed); prepended this session's Next-actions and State-snapshot blocks; advanced the Resume cursor to Sweep 87; corrected the environment prediction (cloud, not local).
- [`.working/session-state.md`](../session-state.md): acquired the concurrency lease (`Active-session` to this branch, `Status: active`, fresh heartbeat `2026-07-06T23:17:40Z`).
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (`2.0.79` to `2.0.80`) and the new detail file [`.working/validate-sweeps/2026-07-06-sweep87-iter1.md`](../validate-sweeps/2026-07-06-sweep87-iter1.md): the Sweep-87 row and per-iteration record.

### Verification

- Mechanical baseline: `tools/run_all_audits.sh` green 66/66 at `ba58958` before the fix; re-run after the fix + regen (pre-push guard).
- Sweep 87: full three-subagent dispatch (A, B, C); A 1 note (fixed), B 0, C 0; no asserted-expectation contradiction of any #684 claimed-clean surface.
- Per-PR QA for this substantive PR (`/validate-pr` + `/retro`) batches into the next PR per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.172, PR #684

Session-closing handoff for the 2026-07-06 resumed session (`claude/resume-chptc7`, #680 to #683). Working-state and version surfaces only; the session-closing handoff PR skips its own trailing `/validate-pr` and `/retro` per the loop-break exception.

### Changed

- [`.working/session-handoff.md`](../session-handoff.md): reconciled the top `Current truth` to merged-through-#683 and session CLOSED (lease released), with the D7 tokens at the #684 state (library `2026.07.172`, README `1.9.533`, validate-pr history `1.2.461`, improvement-log `1.0.405`) and green-at `8af65ea`; prepended this session's `## Asserted expectations` block (#680 to #683); recorded that the next `/resume` is from a LOCAL environment and runs Sweep 87 first.
- [`.working/session-metrics.md`](../session-metrics.md) (`1.0.37` to `1.0.38`): added the session row (5 PRs #680 to #684; 4 post-compaction subagents measured at 1,246,902 tokens, a floor because the about 6 pre-compaction subagents' figures are not in the resumed context; orchestrator tokens not instrumented; about 3h40m elapsed).
- [`.working/session-state.md`](../session-state.md): RELEASED the concurrency lease (`Status: released`, `Active-session: none`, heartbeat re-stamped).
- [`.working/validate-pr/history.md`](../validate-pr/history.md) (`1.2.460` to `1.2.461`): the #684 handoff-exemption row (`SKIPPED (handoff-PR exception)` in the Findings cell, the gate-50-recognized marker).
- Bumped the library CalVer to `2026.07.172` and the README Version to `1.9.533`.

### Verification

- Working-state and version surfaces only; no corpus document body, gate, or code changed. Pre-push guard green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1 through D7 plus the history-aware 45/40/31), run standalone and unpiped. D7 confirms the nine labelled handoff tokens match the live headers at the #684 head.
- Per the loop-break exception this PR takes no trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume`'s corpus-wide `/validate` (Sweep 87), stronger than a per-PR sweep because it re-examines the whole corpus.

### Discipline observation

- Batches the #683 [`/validate-pr`](../validate-pr/history.md) (0 findings) and [`/retro`](../improvement-log.md) rows per recursion-avoidance.
- The maintainer requested the handoff after #683; #683 was this session's last substantive PR. The next `/resume` is from a local machine rather than this cloud environment, so the cloud-specific known-environment behaviours must be re-verified there.

## 2026-07-06, Library Version 2026.07.171, PR #683

FR-23 audit-evidence assembler verification (TODO 2.6): recorded, per evidence item, whether a control's status is independently verified or a management assertion, closing the package template's verify-versus-aggregate silence; applied from the scratch-inbox worker research delivery.

### Changed

- [`compliance/template-audit-evidence-package.md`](../../compliance/template-audit-evidence-package.md) (`1.0.5` to `1.1.0`): added a `Verification basis` field (Independently verified / Owner-asserted / Auditor-to-verify) to both the `### Implementation evidence` and `### Operating evidence` per-control blocks, each naming the supporting independent test (per [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md), tester not the control owner) or the asserting control owner; added a fourth confirmation to the package-level assembler statement (an owner-asserted status is not presented as independently verified without a supporting test); and inserted a review question (item 5, list renumbered 1 to 9).
- [`compliance/standard-internal-audit.md`](../../compliance/standard-internal-audit.md) (`1.0.6` to `1.1.0`): added section 8.4 (verification basis in assembled evidence packages) carrying the same three-value independently-verified / owner-asserted / auditor-to-verify distinction on the auditor side, extending the Evidence-Based Approach principle and the section 8.1 interview-corroboration rule; added the evidence-package template to Related Documents.
- [`docs/template-maturity-self-assessment.md`](../../docs/template-maturity-self-assessment.md) (`1.1.0` to `1.1.1`): the batched #682 Note-3 fix, added [`governance/standard-maturity-assessment-methodology.md`](../../governance/standard-maturity-assessment-methodology.md) to Related Documents (reciprocity; the standard already listed the template).
- Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) after the two compliance-document bumps (taxonomy first; the maturity template's bump is under `docs/`, which is not taxonomy-tracked); all three generators are `--check`-clean.
- Rotated TODO 2.6 (FR-23) to [`.working/DONE.md`](../DONE.md); the batched #682 [`/validate-pr`](../validate-pr/history.md) (3 notes) and [`/retro`](../improvement-log.md) rows.
- Bumped the library CalVer to `2026.07.171` and the README Version to `1.9.532`.

### Verification

- The gap was re-verified real at apply-time (the template named an assembler/owner/reviewer sign-off and an assembler statement about assembly and disclosure, but recorded no per-status verification basis). The independent-testing linkage was confirmed against [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md) (the tester is never the control owner); the Evidence-Based Approach principle and the interview-corroboration rule were confirmed in the internal-audit standard; the control-testing seam was held (referenced, not edited).
- A refute-briefed skeptical verifier reviewed the change pre-push (substantive tier) across eight categories and found it substantively clean, with one low-severity cross-surface completeness gap: section 8.4 framed the basis as a two-value binary while the template defines three values, omitting Auditor-to-verify. Fixed before push (section 8.4 now enumerates all three values) and re-verified by re-reading the reconciled section 8.4 against the template's fields.
- Pre-push guard green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1 through D7 plus the history-aware 45/40/31), run standalone and unpiped.
- **Worker provenance:** applied from [`inbox/worker-20260703-a/fr-23-audit-evidence/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260703-a/fr-23-audit-evidence/MANIFEST.md).

### Discipline observation

- Apply-time version reconciliation: the worker delivery (read at grc_library `ede2e3b`) recorded the template at `1.0.3`; live main had advanced it to `1.0.5`, reconciled to `1.1.0`.
- The batched #682 Note-3 (reciprocal Related-Documents) applied the paired-surface-completeness lesson from that PR's own retrospective.
- Batches the #682 [`/validate-pr`](../validate-pr/history.md) (3 notes) and [`/retro`](../improvement-log.md) rows per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.170, PR #682

FR-15 maturity-ladder methodology (TODO 2.5): added a governance methodology standard documenting the five-tier maturity ladder, the median-of-medians aggregation, its outlier-masking limitation, and a compensating floor-check, applied from the scratch-inbox worker research delivery.

### Added

- [`governance/standard-maturity-assessment-methodology.md`](../../governance/standard-maturity-assessment-methodology.md) (new, `1.0.0`): a governance-domain Standard mirroring [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)'s 13-field metadata block and Standard section model. It documents (section 4) the five-tier CMMI-lineage ladder (Initial, Managed, Defined, Quantitatively Managed, Optimized), (section 5) the median-of-medians aggregation and its median-versus-mean rationale, (section 6) the outlier-masking limitation (the same median robustness that resists a spurious low score also lets a single critically-weak domain not move the overall median), (section 7) the compensating floor-check (an absolute Tier-1 floor plus a relative two-tier-gap floor the assessor surfaces alongside the median, an assessor step that does not change the computation), (section 8) the disambiguation of programme maturity from the generated document-maturity scorecard and the shared tier vocabulary of the Digital Trust Index thresholds, and (section 9) the boundary that it documents maturity levels, not capability levels (the separate TODO 6.4 item).

### Changed

- [`docs/template-maturity-self-assessment.md`](../../docs/template-maturity-self-assessment.md) (`1.0.7` to `1.1.0`): a pointer to the new standard as the authoritative methodology; a floor-check line under `## Overall programme tier`; and assessor review question 6 (run the floor-check). The median scoring steps are unchanged; the minor bump reflects the new assessor step.
- [`governance/framework-governance-performance-and-improvement.md`](../../governance/framework-governance-performance-and-improvement.md) (`1.0.4` to `1.0.5`): a pointer from `### 2. Maturity assessment` to the new standard, and the standard added to `## Related Documents`. The tier table is unchanged (patch bump: a cross-reference addition, no new capability).
- [`governance/README.md`](../../governance/README.md) (`1.10.9` to `1.10.10`) and [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md) (`1.27.59` to `1.27.60`): the new standard added to each mechanical listing surface (gates 4 and 47 require every active document to be enumerated).
- [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md) (`1.1.0` to `1.1.1`): the batched #681 `/validate-pr` fix, section 8.1 `(risk and compliance)` to `(oversight functions)`, the umbrella term the register subsection and continuous-assurance section 4.4 already use for the Three Lines Model second line.
- Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) after the new document and the version bumps (taxonomy first); all three generators are `--check`-clean.
- Rotated TODO 2.5 (FR-15) to [`.working/DONE.md`](../DONE.md); the batched #681 [`/validate-pr`](../validate-pr/history.md) (1 note) and [`/retro`](../improvement-log.md) rows.
- Bumped the library CalVer to `2026.07.170` and the README Version to `1.9.531`.

### Verification

- The gap was re-verified real at apply-time: the five-tier ladder and the median-of-medians aggregation existed (the template and framework section 2), but no named methodology, no documented outlier-masking limitation, and no formal floor-check existed. The tier names were confirmed identical across the standard, framework section 2, and the template; the aggregation was confirmed against the template's scoring steps; the shared tier vocabulary of the Digital Trust Index thresholds was confirmed against [`governance/register-digital-trust-and-assurance-metrics.md`](../../governance/register-digital-trust-and-assurance-metrics.md); no new external citation was introduced (CMMI, COBIT 2019 MEA01, ISO/IEC 42001:2023 section 10, and ISO 9001:2015 sections 9 to 10 all reuse the corpus's established forms).
- A refute-briefed skeptical verifier reviewed the new standard, the four pointer edits, and the control-testing fix pre-push (substantive tier), across nine categories (aggregation correctness, tier definitions, floor-check arithmetic, the DTI seam, citation fabrication, the maturity disambiguation, the control-testing fix, house style, and metadata shape); it could not refute the change. It surfaced one non-blocking, pre-existing item: the corpus carries two glosses for ISO/IEC 42001:2023 section 10, so the new standard's section 11 was aligned to the framework's form (`section 10: AI Governance Improvement`) to avoid introducing a third variant. The corpus-wide two-gloss variance is surfaced to the maintainer, not resolved here (out of this PR's scope).
- Pre-push guard green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1 through D7 plus the history-aware 45/40/31), run standalone and unpiped.
- **Worker provenance:** applied from [`inbox/worker-20260703-a/fr-15-maturity-ladder-methodology/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260703-a/fr-15-maturity-ladder-methodology/MANIFEST.md).

### Discipline observation

- Apply-time version reconciliation: the worker delivery (read at grc_library #619 / `ede2e3b`) recorded the template and the performance framework at `1.0.x` / `1.0.3`; live main had advanced them to `1.0.7` / `1.0.4`, so the bumps were reconciled to the live values.
- The new document had to be added to two mechanical listing surfaces (the governance README and the document-index register); the working-tree audit caught the omission (gates 4 and 47 plus two ListingSurfaceCompleteness regression tests) before push, and it was fixed in the same PR.
- Batches the #681 [`/validate-pr`](../validate-pr/history.md) (1 in-window note, the control-testing second-line shorthand, fixed this PR) and [`/retro`](../improvement-log.md) rows per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.169, PR #681

FR-99 per-control effectiveness metrics (TODO 2.4): introduced a per-control effectiveness metric tied to the continuous-assurance model and the three lines of defence, applied from the scratch-inbox research delivery (Option A, register-extension plus cross-wiring).

### Added

- [`governance/register-digital-trust-and-assurance-metrics.md`](../../governance/register-digital-trust-and-assurance-metrics.md) (`1.0.4` to `1.1.0`): a `Per-control Effectiveness` row in `## Core metric categories` and a `## Per-control effectiveness metric` subsection defining the metric via the existing metric quality fields (an effectiveness band per control derived from its latest operating-effectiveness test result, deficiency recurrence signal, and open corrective-action state; owner is the control owner with second-line aggregation; cadence is the control's residual-risk testing frequency; threshold is expressed on the control-testing result-class bands; the consuming lines of defence are named), referencing the existing Three Lines Model definition.

### Changed

- [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md) (`1.0.8` to `1.1.0`): added the per-control effectiveness band as a Control Testing Register field (section 7.1) and a per-control measure in `## 8. Metrics`, derived from result, recurrence, and open corrective-action state, and consumed under the three lines of defence.
- [`governance/framework-continuous-assurance-and-improvement.md`](../../governance/framework-continuous-assurance-and-improvement.md) (`1.0.9` to `1.1.0`): added section 4.4 wiring the metric into the Performance Evaluation cycle and naming the first-, second-, and third-line consumption.
- [`governance/framework-metrics-monitoring-and-performance-reporting.md`](../../governance/framework-metrics-monitoring-and-performance-reporting.md) (`1.0.6` to `1.1.0`): added the per-control effectiveness band to the Compliance and Audit measurement domain.
- Regenerated [`taxonomy.yml`](../../taxonomy.yml) and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) after the four Version bumps (taxonomy first; [`docs/portal.md`](../../docs/portal.md) unchanged because it does not embed per-document versions); both generators are `--check`-clean.
- Rotated TODO 2.4 (FR-99) to [`.working/DONE.md`](../DONE.md); annotated the eleven legislation-citing deepenings (fr-59/60/74/41, the five jurisdiction annexes, dora, nis2) as deferred pending the maintainer's egress instance (maintainer decision 2026-07-06), and added the fr-59-surfaced Mexico-annex staleness (the annex describes the superseded 2010 LFPDPPP; correct to the 2025 law when egress confirms) as an accepted-unverified tracker under TODO 1.11.
- Bumped the library CalVer to `2026.07.169` and the README Version to `1.9.530`.

### Verification

- Gap re-verified real at apply-time (portfolio-level effectiveness metrics and per-control testing existed; a per-control ongoing effectiveness metric with three-lines-of-defence consumption did not). The result classes (Effective, Observation, Deficiency, Material Weakness) were confirmed against the control-testing procedure's section 4.1; the three-lines-of-defence line assignments were confirmed against the canonical Three Lines Model in the key-terms register and the assurance-map register Section 1; no new external citation was introduced (the existing definition is referenced).
- A refute-briefed skeptical verifier reviewed the four-file diff pre-push (substantive tier) and caught two gate-blind semantic defects, both fixed and re-verified before push: (1) the second-line enumeration in the register subsection and continuous-assurance section 4.4 dropped `legal` from the canonical Three Lines Model membership (added to both; the register reporting-audience field reworded to a clean second-line reference); (2) the register Target-or-threshold field said an Observation band triggers escalation while the Escalation-trigger field and the control-testing section 4.2 response exclude it (reconciled so an Observation band is below target but not automatically escalated). Pre-push guard green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1 through D7 plus the history-aware 45/40/31), run standalone and unpiped.
- **Worker provenance:** applied from [`inbox/worker-20260703-a/fr-99-control-effectiveness-metrics/MANIFEST.md`](../../../grc_library_scratch/inbox/worker-20260703-a/fr-99-control-effectiveness-metrics/MANIFEST.md).

### Discipline observation

- Apply-time version reconciliation: the worker delivery (read at grc_library #619) recorded the four files at `1.0.4` / `1.0.7` / `1.0.8` / `1.0.5`; live main had advanced three of them to `1.0.4` / `1.0.8` / `1.0.9` / `1.0.6`, so the bumps were reconciled to the live values (each to `1.1.0`).
- Batches the #680 [`/validate-pr`](../validate-pr/history.md) (0 findings) and [`/retro`](../improvement-log.md) rows per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.168, PR #680

Sweep 86 close-out (local project): the `/resume` loop-break corpus-wide `/validate` over the #662..#679 deltas, the compensating control for the #679 session-closing handoff (which skipped its trailing `/validate-pr` + `/retro`). Full three-subagent dispatch (A recent-PR deep review, B corpus-wide stale-reference sweep, C audit-programme integrity); baseline 66/66 at `ecb43fc`. The control PASSED: no in-window (#662-#679) regression and no contradiction of any #679 asserted expectation. Eight gate-blind ISO-designation findings surfaced across six F-classes (all pre-existing or marginal); this PR fixes three classes (F1/F3/F5), routes two (F2/F4), no-actions one (F6), and carries the resume-protocol bookkeeping.

### Fixed

- [`specification-master-project.md`](../../specification-master-project.md) (`1.6.7` to `1.6.8`): corrected `ISO/IEC 22301:2019` to `ISO 22301:2019` in the standards reference list. ISO 22301 (business continuity) is a single-body ISO standard (ISO/TC 292), not joint ISO/IEC. Found independently by Sweep-86 subagents A and B (deduped); corpus-wide scope was one outlier against 29 correct bare occurrences; git-dated to the initial public release and out of #663's joint-13 scope, so not a #663 regression, but the exact accuracy class the maintainer's #663 principle governs.
- [`compliance/register-compliance-obligations-template.md`](../../compliance/register-compliance-obligations-template.md) (`1.0.11` to `1.0.12`): corrected the Mapped-Controls filled example from `ISO 27001 Annex A.8.24` to `ISO/IEC 27001:2022 Annex A.8.24`, matching the file's own line-46 taught canonical citation form (A.8.24, Use of cryptography, is a valid 2022 Annex A control).
- [`tools/sweep-preflight-exemptions.json`](../../tools/sweep-preflight-exemptions.json): re-pointed two orphaned exemption entries whose `line_hash` no longer matched after #443 changed the pack README addyosmani-vet line from "18" to "19 spot-scanned" (the README entry `fe027c7d5c9f940d` to `b66b2387f8abbe5a` with its reason string corrected to "19"; the setup-generator entry `a07333ed580ba6f1` to `13314d43cfeabdc5`). The pre-flight scanner now suppresses six candidates by exemption file (the two false positives no longer re-surface); the other four entries were verified still-matching.

### Changed

- Regenerated [`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md), and [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md) (taxonomy first, then portal and scorecard) after the two per-document Version bumps; both generators are `--check`-clean.
- Pruned [`.working/session-handoff.md`](../session-handoff.md) per its keep-current-plus-one-prior discipline (deleted the two-prior #618-#643 session's Next-actions, State-snapshot, and Asserted-expectations blocks, migrating its load-bearing cadence notes forward), prepended the resumed session's Next-actions and State-snapshot blocks, advanced the sweep cursor to Sweep 86, and recorded the step-5 decisions (mode ATTENDED-AUTONOMOUS; the 30 scratch-inbox P2 applies this session; the 3.16 and 3.17 alignment maps surface-then-build; D8 rest-on-convention). The new Current-truth line carries the D7 tokens for this PR (library `2026.07.168`, README `1.9.529`; carried forward pack `1.54.6`, audit-spec `1.16.58`, runbook `1.1.4`, guardrail-history `1.0.6`, validate-pr history `1.2.456`, improvement-log `1.0.401`, claim-fit history `1.0.3`).
- ACQUIRED the [`.working/session-state.md`](../session-state.md) concurrency lease (`Active-session: claude/resume-chptc7`, `Status: active`, heartbeat re-stamped).
- Routed Sweep-86 F2 (the [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md) version-currency vs privacy-docs content-attribution signposting) to TODO 1.11, and F4 (generic-family `ISO 27001` references at the obligations template and [`NOTICE.md`](../../NOTICE.md)) to TODO 3.1; closed the TODO 3.15 D8 section-close-orphan candidate (rest-on-convention) and rotated it to [`.working/DONE.md`](../DONE.md).
- Added the Sweep-86 history row to [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md) (`2.0.78` to `2.0.79`) and the per-iteration detail file [`.working/validate-sweeps/2026-07-06-sweep86-iter1.md`](../validate-sweeps/2026-07-06-sweep86-iter1.md).
- Bumped the library CalVer to `2026.07.168` and the README Version to `1.9.529`.

### Verification

- Sweep 86 baseline 66/66 green at `ecb43fc`; the pre-flight scanner's 11 candidates were all FALSE POSITIVE (the standing growth-narrative class); the three subagents cross-checked against #679's asserted expectations with NO contradiction. Every finding was apply-time-verified by re-reading the cited source before disposition (F1 deduped A plus B; F6 confirmed a deliberate gate-58 both-form-input carve-out via the tool docstring and regex, not a defect).
- A refute-briefed skeptical verifier reviewed the F1 and F3 corpus-document designation changes and the bookkeeping diff pre-push (substantive tier).
- Pre-push guard green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1 through D7 plus the history-aware 45/40/31), run standalone and unpiped; D7 validates the refreshed handoff Current-truth tokens against the live headers at this PR's head.

### Discipline observation

- The Sweep-86 findings are all pre-existing or marginal gate-blind ISO-designation debt, not #662-#679 regressions; the loop-break compensating control's core job, catching anything the handoff PR hid, returned clean. The three fixes are applied under the maintainer's standing #663 accuracy principle; the two routed items feed the existing designation-accuracy backlog (TODO 3.1) and the Brazil verification (TODO 1.11). The count-vs-enumeration advisory (also census-vetoed) remains in TODO 3.15 awaiting the maintainer's confirm-to-close.

## 2026-07-06, Library Version 2026.07.167, PR #679

Session-closing handoff (local project): landed the 2026-07-06 daytime ATTENDED-AUTONOMOUS session's working-state (`claude/resume-tl5rez`, PRs #662-#678) on `main` as a green merge. Per the loop-break exception this PR runs no trailing `/validate-pr` or `/retro`; the compensating control is the next `/resume` corpus-wide `/validate` (Sweep 86 over the #662..#678 deltas), cross-checked against the `## Asserted expectations` block and the green-at-`0377f5d` baseline.

### Changed

- Refreshed [`.working/session-handoff.md`](../session-handoff.md): the `Current truth` snapshot reconciled to merged-through #678 / #679 session-closing, with the post-#679 D7 tokens (library `2026.07.167`, README `1.9.528`, validate-pr history `1.2.456`, improvement-log `1.0.401`; carried forward pack `1.54.6`, audit-spec `1.16.58`, runbook `1.1.4`, guardrail-history `1.0.6`, claim-fit history `1.0.3`), green-at `0377f5d`, operating mode session CLOSED, and the 2026-07-06 `## Asserted expectations` block prepended.
- Added the 2026-07-06 session row to [`.working/session-metrics.md`](../session-metrics.md) (17 PRs #662-#678 plus this #679 handoff; orchestrator main-loop tokens recorded as not instrumented, never fabricated).
- Recorded the #679 handoff-exemption row in [`.working/validate-pr/history.md`](../validate-pr/history.md) with the gate-50 marker (`SKIPPED` / `handoff-PR exception`) in the Findings cell.
- Carried the batched #678 `/validate-pr` (0 findings) history row and the #678 `/retro` row per recursion-avoidance.
- Bumped the library CalVer to `2026.07.167` and the README Version to `1.9.528`.

### Removed

- RELEASED the [`.working/session-state.md`](../session-state.md) concurrency lease (`Status: released`, `Active-session: none`, heartbeat re-stamped); the next session ACQUIRES at `/resume` step 0.

### Verification

- Pre-push guard (`tools/pre-push-guard.sh`) green: `run_all_audits.sh` (66/66) then `run-pr-time-checks.sh` (D1-D7 plus the history-aware 45/40/31), run standalone and unpiped. D7 validates the handoff's labelled version tokens against the live headers at the #679 head.
- No corpus body, gate, or code touched; working-state and version surfaces only. Session-closing handoff PR: no standing skeptical verifier and no trailing per-PR QA (the loop-break exception; compensating control is the next `/resume` corpus-wide `/validate`).

## 2026-07-06, Library Version 2026.07.166, PR #678

Working-state triage (local project): recorded the evidence-driven outcome of this session's three TODO 3.15 protection-tooling attempts and annotated their backlog bullets, and carried the batched #677 QA rows.

### Changed

- [`.working/design-decisions.md`](../../.working/design-decisions.md): added the dated decision "Two figure-drift tooling advisories census-vetoed; GR-GAP-1 register gate egress-gapped (2026-07-06)", plus its Index line. It records, with evidence: (1) the count-vs-enumeration advisory built this session flagged 63 candidates with zero true positives in the full-history FP census (dominant false class: a parenthetical that is a breakdown summing to the count), so it was discarded and the class rests on the #676 recount clause; (2) the section-close orphan advisory flagged 18 candidates with zero true positives on the #677 section-1.9 deletion (which the pre-push verifier had confirmed orphan-free), so it was discarded, with a narrower standing-scan retry recommended for maintainer adjudication; (3) GR-GAP-1 was validated-not-built because 17 of 49 cited `ISO(/IEC) NNNNN:YYYY` pairs lack a register row and the `ISO/IEC 29134` year conflict needs egress-gated currency confirmation. Meta-lesson recorded: free-prose-pattern advisories tend to fail their FP census because the signal is a semantic relationship; the census precondition caught this twice, working as designed.
- [`TODO.md`](../../TODO.md): annotated the three TODO 3.15 tooling bullets inline with the findings above (count-vs-enumeration: census-vetoed, rest on the recount clause, close candidate on maintainer confirm; D8 / GR-GAP-2 orphan check: census-vetoed as the event-triggered shape, narrower standing-scan retry recommended; GR-GAP-1: register-gap validated, sequenced behind egress-gated register population). Append-only edits (no bullet deleted).

### Batched bookkeeping

- Carries the #677 `/validate-pr` (0 findings) history row ([`.working/validate-pr/history.md`](../../.working/validate-pr/history.md), Version to 1.2.455) and the #677 `/retro` row ([`.working/improvement-log.md`](../../.working/improvement-log.md), Version to 1.0.400) per recursion-avoidance.

### Verification

- Two throwaway advisory tools (a count-vs-enumeration drift detector and a TODO-section-close orphan detector, both advisory `audit-*`-named tools) were built, self-tested, FP-censused over full corpus history, and DISCARDED when the census showed zero true positives; neither is in the final diff, so neither is linked here (the files no longer exist). This is the FP-census precondition working as designed (the count-vs-enumeration bullet made it a precondition; the orphan bullet's shape was decided at build time).
- Pre-push guard green standalone (66 gates + PR-time checks) required before push; [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) green before the first commit.
- Change tier: substantive (backlog triage plus a durable design decision). One skeptical verifier ran pre-push per the tiered standard.

## 2026-07-06, Library Version 2026.07.165, PR #677

Working-state close-out (local project): resolved the two outstanding maintainer decisions from the daytime session (close TODO 1.9 as a documented harness limitation; confirm the #670 lowercase-acronym-pattern rejection), reconciled the stale session handoff and concurrency lease, and batched the #676 `/validate-pr` and `/retro` outputs including the #636 disposition-token fix.

### Changed

- [`TODO.md`](../../TODO.md): deleted the P1 §1.9 section (RM-10 pipe-guardrail hardening) on the maintainer's close-as-harness-limitation decision; updated the Backlog-totals P1 line from 3 items to 2 (1.5 and 1.11 remain), naming #677 as 1.9's closing PR and pointing at the [`third-party-issues.md`](../../.working/third-party-issues.md) record.
- [`.working/DONE.md`](../../.working/DONE.md): added the PR #677 rotation entry for TODO 1.9, summarizing the pinned root cause (child sessions leave `CLAUDE_PROJECT_DIR` unset), the harness-level-fix conclusion, and the active compensating controls.
- [`.working/third-party-issues.md`](../../.working/third-party-issues.md): added a 2026-07-06 entry recording the PreToolUse-hook non-firing as a documented harness/environment limitation (Observed / Diagnosis-with-pinned-root-cause / How-distinguished-from-a-defect / Impact-resolution), so a future session does not re-diagnose the non-firing hook as a regression; Version 1.0.7 to 1.0.8, Date to 2026-07-06.
- [`.working/pending-decisions.md`](../../.working/pending-decisions.md): Status line to 0 pending; marked the TODO 1.9 entry RESOLVED inline (disposition A, close as documented harness limitation) and recorded the #670 lowercase-rejection maintainer confirmation (no reopen; the corpus-wide-evidence rejection in the #670 `/retro` row stands).
- [`.working/session-handoff.md`](../../.working/session-handoff.md): reconciled the `Current truth` snapshot line, which had lagged at #659-merged / #662-in-flight across the resumed session's 15 PRs, to merged-through #676 with #677 in flight, the resumed session's #662..#676 enumerated, the prior 2026-07-05 session marked historical, and every D7-labelled version token advanced to its post-#677 live value (library `2026.07.165`, README `1.9.526`, validate-pr history `1.2.454`, improvement-log `1.0.399`; pack/audit-spec/runbook/guardrail-history/claim-fit carried forward unchanged). The older per-session blocks are left for the next `/resume` prune (the pruning discipline's designated locus).
- [`.working/session-state.md`](../../.working/session-state.md): re-stamped the concurrency-lease heartbeat to 2026-07-06T16:14:01Z and rewrote `Current-task` to the active session's real state (shipped #662..#676, #677 in flight, 0 pending decisions).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): reworded one factual-staleness one-liner that this closure created (in the PR-workflow step-2 RM-10 pipe-guard paragraph, "the TODO 1.9 hook-firing residual" became "the hook-firing limitation later closed as TODO 1.9 in #677"), so the closed item is not described with an open-status word in a gate-blind file. This is the maintainer-pre-authorized protected-tree factual-staleness-one-liner class (2026-07-03 morning-round directive 6, each instance named in its PR CHANGELOG entry); it was surfaced by the pre-push skeptical verifier as an out-of-window note and folded in-window because #677 is the closure that created the staleness. The verifier confirmed the two [`block-verification-pipes.py`](../../.claude/hooks/block-verification-pipes.py) "TODO section 1.9" comments are code-provenance references, not open-status pointers, and left them.

### Fixed

- [`.working/improvement-log.md`](../../.working/improvement-log.md): appended `Disposition: CODIFIED in #676` to row #636 (the batched #676 `/validate-pr` FINDING 1). #676 codified the staged consolidated recount clause and tokened its ROUTED staging rows #631 and #633, but missed #636, which carried the same candidate as an `EXPEDITE` directive; the post-merge bare-token scan of all seven clause-referencing rows caught it. The scan also confirmed #634 is a different candidate (path-resolution fixture, F6 class) correctly left pending and #637/#639/#640/#641 carry `None new` needing no token.

### Verification

- Pre-push guard green standalone on the final state: all 66 audit gates pass, all PR-time checks pass (D1 through D7, and the history-aware gates 45/40/31). D7 (handoff-snapshot freshness) is the relevant gate here: it fires because the PR touches [`.working/session-handoff.md`](../../.working/session-handoff.md), and it validates each labelled version token on the reconciled `Current truth` line against that surface's live header at the PR head; the reconcile advanced every token to the post-#677 value so D7 passes.
- [`tools/preflight-changelog.py`](../../tools/preflight-changelog.py) green before the first commit (added CHANGELOG lines dash-free, path spans linked).
- Change tier: substantive (multi-surface working-state close-out with a P1 backlog closure). One skeptical verifier subagent ran pre-push per the tiered standard.

### Discipline observation

- The #636 disposition-scan miss is the `validate-inference-before-action` "validated the rows I was looking at, inferred the rest" shape applied to the register disposition scan: the orchestrator's mental model of the staged recount candidate was "#631/#633" across #674/#675/#676 (the #675 `/retro` row's own disposition note names only those two), so the #636 `EXPEDITE` carrier was never in view. The existing `/retro` step-6 carrier-phrase grep should have caught it (the #636 cell literally reads "land it at the NEXT authorized CLAUDE.md close-out-checklist touch"); logged as an OBSERVATION with the interim practice guard to run that grep at bare-token / comprehensive width across ALL register rows.
- The session-handoff reconcile is the reconcile-not-append discipline catching up after the resumed session skipped the mandated per-PR handoff refresh across #662..#676; the #674 `/validate-pr` had flagged the staleness out-of-window. D7 is version-tokens-only, so the prose-half reconcile (merged-through, the historical prior-session framing) is convention-guarded and was done by hand here.

## 2026-07-06, Library Version 2026.07.164, PR #676

`.claude/` change for local project (the third of the three daytime CLAUDE.md changes): codified the counts-adjacent-to-enumerations recount residual, folded into the existing Meta-prose bullet.

- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): extended the `Meta-prose state-claim measurement` PR close-out-checklist bullet with a compact sub-clause naming the #630/#631/#633 count-and-label granularity pattern: a count stated next to an enumeration at a different granularity, or a figure transcribed from a subagent's output, must be recounted from the enumeration in the same edit, with both granularities stated where a fix-count and a location-count diverge, and a subagent's arithmetic treated as a hypothesis, not a measurement.
- Rationale (subsumption): the #631 and #633 register candidates staged a "counts-adjacent-to-enumerations recount" clause and a broader "recount every figure" consolidation for the next authorized CLAUDE.md close-out-checklist touch. The apply-time check found the generic `Meta-prose state-claim measurement` guard (measure any artefact-state claim from the artefact, never from the mental model) already covered most of it, and the snapshot-reconcile half was already codified with D7 as its backstop; so #676 adds only the named granularity-divergence and recount-transcribed-figure residual as a fold, not a redundant standalone bullet (respecting the #441 condense directive). Both register candidates tokened CODIFIED in #676.
- No corpus body, gate, or generated artefact touched; protected-guidance tier. [`tools/lint-language.py`](../../tools/lint-language.py) clean on the added prose. A pre-push skeptical verifier (substantive tier) reviewed the diff.

**Batched bookkeeping.** Carries the #675 `/validate-pr` (0 findings) history row and the #675 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.163, PR #675

Tooling for local project (second protected-backlog PR of the 2026-07-06 daytime session): widened delta gate D5 with an eighth closure form and a form-6 markdown-link widening, closing the TODO 3.15 #637 F3 bullet.

### Changed
- [`tools/check-todo-rotation-on-pr.py`](../../tools/check-todo-rotation-on-pr.py): added an eighth pattern to `CLOSURE_PATTERNS`, the bare `TODO N.M ... closed/closure` phrasing (a decimal section token with no `section` word and no `§`, case-insensitive, forward-only, dot-between-digits tolerant), the #637 lead shape that matched none of forms 1 to 7; and widened the form-6 rotation-assertion pattern with a markdown-linked DONE target alternative for the #640 rotated-to-linked-path shape (the not-negation guard still fronts the whole clause). Docstring and module comment updated from seven to eight forms.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): the PR-workflow step-7 closure-form count updated from SEVEN to EIGHT, with form (8) added to the enumeration and the form-6 markdown-link widening noted (maintainer-authorized protected-tree touch).
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md): the §6 D5 narrative updated (count seven to eight, the eighth-form description, the form-6 widening note, and the census figures); Version and Date bumped.
- [`tests/test_linters.py`](../../tests/test_linters.py): `TodoRotationOnPrTests` gains three form-8 positive fixtures and one form-6-markdown-link positive fixture (genuine regressions, only the new forms reach them); the class docstring updated to eight forms.
- [`TODO.md`](../../TODO.md): the 3.15 #637 F3 bullet deleted (shipped) and rotated to [`.working/DONE.md`](../DONE.md) keyed by PR #675. TODO 3.15 stays open on its GR-8/GR-10/GR-GAP tooling bullets; the F3 diff-side-companion design proposal is subsumed by the still-open D8-candidate bullet.

### Verification
- Both new regexes were census-validated false-positive-free against the full CHANGELOG history (form 8: 16 genuine same-PR closures, zero negation false positives; form-6 link widening: 64 genuine linked rotation assertions, zero bug-matches; the census predates this PR and is recorded in the former F3 bullet). Direct regex checks confirm form 8 matches the bare phrasing and rejects past-closure narration where the closure word precedes the token, and the form-6 negation guard still excludes a linked target under a `NOT rotated` clause. `TodoRotationOnPrTests` passes (positives fire, negatives excluded). [`tools/lint-language.py`](../../tools/lint-language.py) clean on the added CLAUDE.md prose. A pre-push skeptical verifier (substantive tier) reviewed the diff. Pre-push guard green (both runners; gate 36 exercises the regression suite, gate 35 the parity surfaces).

**Batched bookkeeping.** Carries the #674 `/validate-pr` (0 in-window findings, one out-of-window handoff-staleness note) history row and the #674 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.162, PR #674

`.claude/` change for local project (first protected-backlog PR of the 2026-07-06 daytime session): added the `/claim-fit` cadence section to CLAUDE.md, completing the TODO 3.15 r5 close-out-clause bundle.

### Added
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a new `## Normative-attribution claim-precision cadence (/claim-fit)` section, placed sibling to and modeled on the existing `## Compliance-matrix semantic-fit cadence (/matrix-fit)` section (inserted between it and the "Reference-version currency" section). It documents the cadence for the `/claim-fit` citation-precision audit that catches the gate-blind "attributed value, silent source" FR-120 class (a specific value attributed to a named source the source does not prescribe): the four verdicts (`prescribed`, `informed-not-prescribed`, `mis-attributed`, `source-not-held`), the three-part run cadence (the one-time Tier-A adoption pass, the per-batch cadence, ad-hoc), the not-a-gate boundary, and the fix rules (an `informed-not-prescribed` finding fixes the attribution phrasing not the value; a `source-not-held` claim routes to the maintainer's source-drop queue). Links the [`claim-fit`](../../dev-security/claude-rules/skills/claim-fit/SKILL.md) skill and the [`tools/audit-claim-precision.py`](../../tools/audit-claim-precision.py) worklist tool.

### Changed
- [`TODO.md`](../../TODO.md): the 3.15 r5 close-out-clause bundle bullet (first three clauses shipped in #652/#659; the `/claim-fit` clause was the last) is deleted, having fully landed. TODO 3.15 stays open on its remaining bullets (the #637 F3 D5 eighth-form, GR-8 A/B, GR-10, GR-GAP-1, the fence-predicate and count-vs-enumeration advisories, the gate-66 shape call).
- [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md): item 5 rotated out (its `/claim-fit` clause landed); only item 6 (the GR-P design track) remains staged.
- [`.working/DONE.md`](../DONE.md): #674 entry added.

### Verification
- Apply-time verification of every factual claim in the section before commit: [`tools/audit-claim-precision.py`](../../tools/audit-claim-precision.py) and the [`claim-fit`](../../dev-security/claude-rules/skills/claim-fit/SKILL.md) SKILL both exist; the FR-120 example (180-day, NIST SP 800-53 CA-6, ISO/IEC 27001 Clause 9.2, neither prescribes) matches the SKILL's motivating incident; the four verdicts match the SKILL; the provenance (tool PR A #621, skill plus Tier-A adoption pass PR B #630) confirmed against the #621 and #630 CHANGELOG entries and DONE.md.
- [`tools/lint-language.py`](../../tools/lint-language.py) run on CLAUDE.md before the first commit: the added section carries zero em/en dashes and zero British `-ise` spellings (the pre-existing dash findings are long-standing lines elsewhere in this gate-exempt file). A pre-push skeptical verifier (substantive tier) reviewed the diff. Pre-push guard green (both runners).

**Batched bookkeeping.** Carries the #673 `/validate-pr` (0 findings) history row and the #673 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.161, PR #673

`.working/` for local project (overnight cleanup, the mode-exit priority-1 morning-processing PR): reset the overnight file and routed the 2026-07-06 overnight run's content. Terse entry (working-state only, adopter-invisible; no corpus body change).

- [`.working/overnight-pr.md`](../overnight-pr.md): reset `Status` from `in-flight` to `stub` and replaced the current-run section with a closure note. The 2026-07-06 overnight run (session `claude/resume-tl5rez`) shipped #667 through #671. Content routed: the PCI DSS "full latest version" citation-form preference already in [`.working/design-decisions.md`](../design-decisions.md) (under #668); closed work in [`.working/DONE.md`](../DONE.md) per-PR during the run; no new TODO follow-ups (the 3.21(a) matrix framework-key full-name-consistency observation was deliberately not raised absent a signal); build-progress and files-modified lists discarded as noise.
- Deferred to the daytime protected-backlog (now beginning): the `/claim-fit` cadence clause ([`.working/deferred-protected-changes.md`](../deferred-protected-changes.md) item 5) and TODO 3.15 #637 F3 (the D5 eighth-closure-form widening, protected-entangled because its closure-form count is restated in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md)).
- No gate, corpus body, generated artefact, or protected file touched; bookkeeping tier (no standing verifier). Gate 46 passes on `stub`.

**Batched bookkeeping.** Carries the #672 `/validate-pr` (0 findings) history row and the #672 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.160, PR #672

`.claude/` change for local project: added a `No idle-stop in unattended mode` guardrail clause to the "Attended-autonomous operating mode" section of [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (maintainer-authorized protected-tree touch, 2026-07-06). Protected-guidance change, adopter-invisible; no corpus body, no gate logic.

- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): inserted a `No idle-stop in unattended mode` paragraph at the end of the "Attended-autonomous operating mode" section, immediately before "Wind-down decision framework". It restates, at the point of the next-action decision, the invalid stop triggers the wind-down framework already forbids (context-heaviness, work-shape, un-instrumented internal state): in overnight or any unattended mode, never idle or stop to ask which authorized item to take next; proceed on the highest-priority authorized independent item at the appropriate skeptical-verifier tier; and confine a legitimate stop to a named-degradation trigger or a genuinely authorial decision handled through the graceful-degradation mechanism (a stricter-safe default, or defer-and-skip to the next independent item), never a blocking question that idles the run until the maintainer wakes. It names two caught pre-push slips, or any defect the guard or verifier catches before it escapes, as the verification layer working, not a degradation signal.
- Why: the wind-down section already forbade those triggers, but reading them there did not prevent acting against them. A 2026-07-06 overnight run stopped and asked the maintainer which authorized P2 item to take, idling the run. The gap was at the action boundary, so the rule is restated at the moment of the next-action decision, where the failure occurred.
- Verification: protected-guidance tier (no corpus body, no gate logic). The language linter was run on the changed file before the first commit; the added block carries zero em or en dashes and zero British `-ise` spellings (the pre-existing dash findings are long-standing lines elsewhere in this gate-exempt file, out of scope). Pre-push guard green (both runners).

**Batched bookkeeping.** Carries the #671 `/validate-pr` (0 findings) history row and the #671 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.159, PR #671

`.working/` and TODO for local project (fifth PR of the 2026-07-06 overnight run): codified the QA-report intake channel and recorded the D5-eighth-form daytime deferral. Terse entry (working-state + TODO, adopter-invisible; no corpus body change).

- Added [`.working/multi-session-orchestration.md`](../multi-session-orchestration.md) §5.2 "QA-report intake (the three-layer validation channel)", the TODO 3.15 r4 G-7 close. It codifies the three-layer intake a worker findings REPORT (as distinct from research or candidate diffs, the 5.1 input channel) passes through before any claimed finding drives a backlog entry or a fix: (1) the report is a hypothesis-set, acted on nowhere directly; (2) an independent validation subagent, blind to the report's reasoning, re-reads each cited source against the live artefact (the false-positive filter, the same apply-time re-verification `trust-recovery-escalation` requires); (3) a transcription-fidelity verifier confirms the orchestrator's transcription of each validated finding into the records matches what layer 2 validated (the report-to-record seam). Records that the channel was first exercised on the #626 intake, catching a defect at each of the three seams, and carries the maintainer's standing revisit note (2026-07-04) to assess the full-skill option on the channel's next recurrence.
- [`TODO.md`](../../TODO.md): the 3.15 r4 G-7 bullet deleted and rotated to [`.working/DONE.md`](../DONE.md) keyed by PR #671; the 3.15 #637 F3 bullet annotated with the census result (both the form-8 and form-6 widenings validated FP-clean against full CHANGELOG history) and marked DAYTIME-DEFERRED (protected-entangled: the closure-form count is restated in the protected [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md), which must co-update in the same PR, so the whole build waits for the daytime protected-backlog clearance rather than stranding a cross-surface count inconsistency overnight).
- No gate, corpus document body, generated artefact, or protected file touched. `.working/` runbook prose only, so bookkeeping tier (no standing verifier); gate 51 (working-tree prose hygiene) covers the added prose via the pre-push guard.

**Batched bookkeeping.** Carries the #670 `/validate-pr` (0 findings) history row and the #670 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.158, PR #670

Acronym-linter digit-initial blind spot closed (gate 20; the TODO 3.15 #637-verifier F4/F6 bullet), fourth PR of the 2026-07-06 overnight run. Substantive tooling change (gate detection-logic widening plus fixtures); one pre-push skeptical verifier.

### Changed

- [`tools/lint-acronym-consistency.py`](../../tools/lint-acronym-consistency.py): widened `GLOSSARY_ROW_RE` and `INLINE_DEF_RE` acronym-capture groups from `[A-Z]`-initial to `[A-Z0-9]`-initial, so digit-initial numeronym glossary rows (the register's `3PL`, and any future `2FA`-class entry) are parsed and their inline definitions matched rather than silently skipped. Before the widening, `3PL` (the register's only digit-initial term, at [`governance/register-glossary.md`](../../governance/register-glossary.md) line 48) was absent from the parsed glossary map, so every inline `(3PL)` definition was unchecked. The module docstring is updated to record digit-initial support AND to document that the deliberate Title-Case-expansion requirement in `INLINE_DEF_RE` is a false-positive control, not an oversight.

### Added

- [`tests/test_linters.py`](../../tests/test_linters.py): three `AcronymConsistencyTests` fixtures. `test_digit_initial_glossary_row_parsed_wrong_expansion_flagged` (a wrong Title-Case `3PL` expansion is now flagged, the regression test for the widening: it would pass-as-unflagged on the old `[A-Z]`-initial regex); `test_digit_initial_correct_expansion_not_flagged` (a correct Title-Case `3PL` definition is not over-flagged); `test_lowercase_prose_definition_deliberately_not_checked` (a lowercase running-prose parenthetical is deliberately not treated as a definition, locking in the false-positive control).

### Assessment (the paired "assess a lowercase-tolerant inline pattern" directive: REJECTED with evidence)

- The F4/F6 bullet's second directive was to assess a lowercase-tolerant inline-definition pattern (to catch canonical-order running-prose expansions such as `financial market infrastructure (FMI)` and `third-party logistics provider (3PL)`). Assessed corpus-wide and rejected: a lowercase-starting expansion run over-captures incidental leading context words. A corpus census confirmed the lowercase surface is large (a few hundred lowercase-word-preceding occurrences of a glossary acronym; the exact count is sensitive to the candidate pattern's word-run shape, so it is stated directionally rather than as a reproducible integer) and dominated by over-captures: under a partial-overlap flagging rule many consistent definitions would false-positive (the over-captured leading words show as non-overlapping), and even a zero-overlap flagging rule (mirroring the current Title-Case logic) false-positives on incidental parentheticals such as `"...candidates list" (STP)`. An initialism anchor that would make lowercase matching safe is unreliable for numeronyms (`3PL` / `2FA`, where the digit is not a word initial) and stopword-dropping acronyms (`CAPA` = "corrective and preventive action"). The Title-Case-expansion requirement is therefore a load-bearing precision control; it is documented as such rather than widened. Surfaced to the maintainer for confirmation (reopen if the partial-overlap design, with its added complexity and full-corpus FP census, is wanted).

### Verification

- Gate 20 green on the live corpus (the acronym linter exits 0; 395 files, 174 glossary entries, the widening adds `3PL` to the map with zero new findings because all corpus inline `(3PL)` / `(FMI)` usages are lowercase running prose, which the Title-Case-anchored `INLINE_DEF_RE` does not match). Full linter-regression suite green (346 tests, exit 0). Gate 20's four parity surfaces (workflow, runner, pre-commit, §6 table) and the §6 narrative are unchanged (a precision widening, not a scope change), so no parity-surface edit was required; the detection-logic-change surfaces (module docstring, regression fixtures) are both updated. No corpus document body, generated artefact, or enumerated-collection count changed. Pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green.

**Batched bookkeeping.** Carries the #669 `/validate-pr` (0 findings) history row and the #669 `/retro` row per recursion-avoidance.

## 2026-07-06, Library Version 2026.07.157, PR #669

`.working/` and TODO for local project (third PR of the 2026-07-06 overnight run): recorded the TODO 1.9 PreToolUse-hook-firing root-cause finding and deferred its disposition to the maintainer. The overnight read-only investigation pinned the mechanism: in a resumed/child session (`CLAUDE_CODE_CHILD_SESSION` set) `CLAUDE_PROJECT_DIR` is UNSET, so the [`.claude/settings.json`](../../.claude/settings.json) hook command (which interpolates that variable into the path of the [`.claude/hooks/block-verification-pipes.py`](../../.claude/hooks/block-verification-pipes.py) script) produces a nonexistent absolute path, `python3` cannot open it, and the Bash tool proceeds unblocked. No portable corpus-side fallback exists (`$PWD` defaults to `/home/user`; no other `CLAUDE_*` var carries the project path; `git rev-parse --show-toplevel` fails from `/home/user`), so the fix is harness-level. The hook script itself is correct (its `--self-test` passes: 14 blocked, 17 allowed). [`TODO.md`](../../TODO.md) 1.9 records the finding; a new [`.working/pending-decisions.md`](../pending-decisions.md) Pending entry carries the maintainer disposition (close as documented harness limitation vs track a harness-feedback filing; compensating controls, the RM-10 habit and the guard's pipe self-defence, remain active); 1.9 is NOT closed pending that decision. Terse entry (`.working/`/TODO-internal, adopter-invisible; no corpus body change). Carries the batched #668 `/validate-pr` (0 findings) + `/retro` rows.

## 2026-07-06, Library Version 2026.07.156, PR #668

PCI DSS version-label normalization, the TODO 3.21(d) follow-through, second PR of the 2026-07-06 overnight run. The maintainer clarified the standing preference the same night the 3.21 residuals were resolved: use the full latest version `PCI DSS v4.0.1`, with the family label `v4` acceptable only when quoting another document that references it.

### Changed

- **Three cloud-hardening baseline framework-alignment cells** normalized from the bare `PCI DSS v4` family label to `PCI DSS v4.0.1`: [`dev-security/standard-cloud-hardening-baseline-aws.md`](../../dev-security/standard-cloud-hardening-baseline-aws.md), [`dev-security/standard-cloud-hardening-baseline-azure.md`](../../dev-security/standard-cloud-hardening-baseline-azure.md), [`dev-security/standard-cloud-hardening-baseline-gcp.md`](../../dev-security/standard-cloud-hardening-baseline-gcp.md) (each `0.0.8` to `0.0.9`, Date 2026-07-06). Deterministic exact-string replacement (one cell per file, idempotence-guarded; verified zero bare `PCI DSS v4` residual in the three baselines and `v4.0.1` present in each).

### Unchanged (recorded)

- The citation-form template's discouraged-example `PCI DSS v4` at [`compliance/register-compliance-obligations-template.md`](../../compliance/register-compliance-obligations-template.md):49 is LEFT: it sits in the discouraged-examples column ("`PCI DSS`; `PCI DSS v4` (without requirement)"), illustrating the bad form, so normalizing it would defeat the example (the display-as-example carve-out, adjacent to the maintainer's quote-exemption). A corpus-wide scan confirmed these were the only bare `PCI DSS v4` occurrences outside gate-exempt `.working/`, CHANGELOG, and TODO surfaces.

### Added

- The standing PCI-DSS version-label preference recorded as a dated decision in [`.working/design-decisions.md`](../design-decisions.md) (`v4.0.1` default; family `v4` only when quoting another document; "full latest version" tracks future point releases with a currency re-verify), and the [`.working/pending-decisions.md`](../pending-decisions.md) 3.21(d) line re-resolved from "(d) leave" to normalize.

### Verification

- taxonomy + portal + scorecard regenerated (diff scoped to the three baselines' `0.0.9` / Date bumps); one pre-push skeptical verifier (substantive tier: corpus-document body change); pre-push guard (both runners) green.
- Batched (recursion-avoidance): the #667 `/validate-pr` history row (0 findings) + `/retro` row and the 3.21 decision reconciliation (committed on the branch before this entry).

## 2026-07-06, Library Version 2026.07.155, PR #667

TODO section 3.21 (citation and naming hygiene residuals) CLOSED, the first PR of the 2026-07-06 overnight run. The four decision-parked residuals were resolved on the maintainer's chat calls (a=A1, b=B2, c=C1, d=leave); (a), (b), (c) are corpus/tool changes outside the protected trees, so they were authorized to apply overnight, and (d) is no change.

### Changed

- **(a) Compliance-matrix C-TPAT framework-key cell.** [`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md) (`1.11.11` to `1.11.12`, Date 2026-07-06): the framework-column-key table cell reading "C-TPAT Minimum Security Criteria" (a verbatim CBP document-title quote) is normalized to the bare programme acronym `C-TPAT`, removing the document-title-quote shape that was the 3.21(a) concern. Observation recorded for the maintainer (non-blocking): that column's sibling cells carry fuller programme names (e.g. "Partners in Protection (Canada Border Services Agency)"), so bare `C-TPAT` is slightly less consistent with the column than a full "Customs-Trade Partnership Against Terrorism" expansion; the maintainer's informed A1 choice was bare `C-TPAT`, applied as chosen (a future full-name-consistency pass over the column is a possible new item, not raised absent a signal).
- **(b) FQ-F1 tool-string house-style.** The five identical PR-delta check-script error strings `In GitHub Actions, ensure actions/checkout uses fetch-depth: 0.` are reworded to `ensure that` ([`tools/check-changelog-dash-on-pr.py`](../../tools/check-changelog-dash-on-pr.py), [`tools/check-changelog-on-pr.py`](../../tools/check-changelog-on-pr.py), [`tools/check-date-cobump-on-pr.py`](../../tools/check-date-cobump-on-pr.py), [`tools/check-todo-rotation-on-pr.py`](../../tools/check-todo-rotation-on-pr.py), [`tools/check-version-bump-on-pr.py`](../../tools/check-version-bump-on-pr.py)). Deterministic exact-string replacement (one occurrence per file, idempotence-guarded, verified zero bare-form residual). These `.py` diagnostic strings are not scanned by [`tools/lint-language.py`](../../tools/lint-language.py) (which is why FQ-F1 was a manual residual, not a gate failure); the maintainer chose B2 (reword) over the carve-out. No behaviour change.
- **(c) FQ-B1 master-spec line-214 monotonicity claim.** [`specification-master-project.md`](../../specification-master-project.md) (`1.6.6` to `1.6.7`, Date 2026-07-06): the stale "The audit suite does not automatically enforce monotonicity" clause is replaced with the verifier's round-3 wording, which states that gate 13 (the library and document version-monotonicity audit) enforces non-decrease against the prior committed state and passes an unchanged value, so a missing library-version bump surfaces instead through the CHANGELOG-coupling gates 29 and 59 (which require each PR's entry to carry a strictly higher Library Version matching the README), and reviewers should still verify the bump. The asserted gate identities were re-verified against the linter docstrings before shipping (a claim precision check, since the sentence attributes specific behaviour to numbered gates): gate 13's docstring confirms it skips CHANGELOG.md and checks non-decrease; gate 29's invariant 2 couples the README Library Version to the latest CHANGELOG heading; gate 59's GR-1 extension asserts the CHANGELOG entries' Library-Version strict ordering.

### Unchanged (recorded)

- **(d) PCI DSS v4 cloud-baseline citations.** The three `PCI DSS v4` family-label citations in the AWS/Azure/GCP cloud-hardening baselines are left as-is: the maintainer chose to keep the current-family label over normalizing to `v4.0.1`. No code change; the residual closes as a decision.

### Removed

- **TODO section 3.21** deleted from [`TODO.md`](../../TODO.md) (all four residuals resolved), rotated to [`.working/DONE.md`](../DONE.md) keyed by PR #667. Cross-reference check before deletion: the only other `3.21` mentions are a frozen historical phrasing example inside the still-open D5-gate-design bullet and gate-exempt CHANGELOG history, so no live pointer is orphaned.

### Added

- Overnight-state file [`.working/overnight-pr.md`](../overnight-pr.md) transitioned `stub` to `in-flight` with the 2026-07-06 run's authorization scope, files-modified list, design decisions, and the deferred-protected queue; the `/claim-fit` cadence-section clause (the last TODO 3.15 r5 close-out item, a [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) protected change) drafted content-ready into [`.working/deferred-protected-changes.md`](../deferred-protected-changes.md) for the daytime apply.

### Verification

- `tools/run_all_audits.sh` (all gates) and `tools/run-pr-time-checks.sh` (D1-D7 plus the history-aware trio) run standalone and unpiped as the pre-push guard; taxonomy + portal + scorecard regenerated from the two metadata bumps (taxonomy diff scoped to only the matrix `1.11.12` and spec `1.6.7` version/date). One pre-push skeptical verifier (substantive tier: a corpus-document body change plus a spec reword plus tool edits).
- Batched (recursion-avoidance): the #666 `/validate-pr` history row (0 findings) and the #666 `/retro` row (interim commit `b37d610`).

