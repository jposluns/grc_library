# Session Handoff

**Purpose.** This file is the single resume point for a new Claude Code session. It is refreshed at every PR close-out so that opening a fresh session and continuing requires only one instruction from the maintainer (see "How to resume"). It exists because long sessions degrade (context dilution, lossy compaction, state drift, error compounding); a fresh session that rebuilds state from this file plus the durable repo artefacts is more reliable than a long one running on accumulated memory. The mechanisms and mitigations are written up generically in `grc_library_private/session-length-considerations.md`. This file is maintainer working state, exempt from corpus audit gates per the `.working/` exemption.

This is an **as-of-last-refresh snapshot**, not a live-HEAD claim. Versions and counts drift forward as work advances; always verify against live files before relying on them.

## How to resume (the one command)

In a new session, the maintainer sends only: **`/resume`** (or "read `.working/session-handoff.md` and continue").

On `/resume`, the assistant:
0. **Runs the concurrency lease check FIRST** (`/resume` step 0, shipped with the section-3.7 interlock): read [`session-state.md`](session-state.md) from `main` and git-cross-check unmerged `origin/claude/*` sibling branches; 60-minute staleness window, advisory HOLD on a live signal (never proceed on a timeout); ACQUIRE the lease on proceeding. Gate 63 guards the lease file's shape.
1. Reads this file in full, including the **"Known environment behaviours"** section below.
2. Reads `.claude/CLAUDE.md` (the PRIMORDIAL RULE and project disciplines), the most recent few `CHANGELOG.md` entries, and **`grc_library_private/third-party-issues.md`**.
2a. **Loads the `grc_library_ref` reference index into memory** (`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`, `grc_library_ref/COVERAGE-MAP.md`) so the reference set and its versions are known before any task; the index, not a guessed path, is authoritative for the reference set and its locations. See `/resume` command's Reference-knowledge-base step and the `## Reference-version currency` SOP in `.claude/CLAUDE.md`.
3. Runs `git rev-parse --is-shallow-repository` (unshallow with `git fetch --unshallow` if `true`, **before any history-aware audit**), then `tools/run_all_audits.sh` to confirm the corpus is green, and `git log --oneline -5` to confirm HEAD.
4. Verifies the version/count snapshot below against live files.
4a. **Batches the unattended-run clarifications up front (maintainer-directed 2026-06-25)**: before resuming the queue, asks the maintainer (via `AskUserQuestion`, batched into as few rounds as possible) every decision that would let the session run unattended longer, pre-populating decisions for **all Priority 1 and Priority 2 backlog items** and **the next 10-plus planned PRs** (including any outside P1/P2, e.g. the FR-167 batches). Compute-don't-ask first (ask only genuine authorial decisions, not what the assistant can verify); record the answers in the next-actions queue so they survive a mid-session compaction; mark deferrals and route around them. See `/resume` command step 5 for the authoritative form.
5. **Runs a full corpus-wide `/validate` as the first substantive task** (the loop-break compensating control for whatever session-closing handoff PR last closed, which skips its trailing `/validate-pr` + `/retro`): full A/B/C subagent dispatch over the closing session's delta window, recorded in [`validate-sweeps/history.md`](validate-sweeps/history.md) and the Resume-cursor section above. **Cross-check the findings against the "Asserted expectations" section below**: a contradiction of an asserted-clean touched surface is a genuine miss, escalated; an ordinary finding routes to the backlog. Standing invariants to confirm: the corpus is CSF-1.1-clean (gate 54, 0 carriers; a carrier in a per-document NIST table is a genuine finding, not residue); four-surface parity at the current gate count (gate 35); the gate/rule/skill/command counts (gate 39 + prose). The specific sweep number and delta window are in the current "Next actions" block below.
6. **Prunes this file as part of that first `/validate` close-out PR** (keep current + 1 prior, per `## Refresh and pruning discipline` below), so the handoff does not accumulate stale session history across resumes.
7. Continues from "Next actions" below.

## Resume cursor (machine-readable)

This is the relocated home of the former `## Session resume metadata` block (moved out of
[`TODO.md`](../TODO.md) in PR #413 so TODO stays purely forward-looking). The sweep cursor below is
read by [`tools/lint-todo-staleness.py`](../tools/lint-todo-staleness.py) (gate 45), which flags it
if it falls behind [`validate-sweeps/history.md`](validate-sweeps/history.md). The full sweep history
lives in that history file; the live per-session state (branch, versions, counts, green-at-`<sha>`) is
in the "Next actions" blocks below and is an as-of-last-refresh snapshot (drift forward is expected).

- **Last validation sweep**: Sweep 122 iter 1 (2026-07-25c; the loop-break corpus-wide `/validate` over the **#1169..#1177** deltas (base `02a820a8`=#1168, head `c3cefd8f`=#1177, 9 commits / 50 files) at the 2026-07-25c `/resume` from the #1177 session-closing handoff. **PRE-QUEUED at the prior session's wind-down** under the discipline #1177 codified, so it was already in flight at resume: the first firing of that discipline. OFFLOADED to `opus-20260725T121943Z-78ff` (Opus 5) as blocking prio-0 `sweep122-resume-validate` pinned `c3cefd8f`, consumed under ELEVATED QA. **0 error / 0 warning / 3 note. PASS, ZERO genuine misses; loop-break control for #1177 PASSES.** Mechanical baseline worker-re-derived in an isolated pinned clone: 78/78 (suite exit 0, no FAIL lines, gate numbers 1..78 with no hole), self-tests 47/47, 34/34, 44/44, 17/17, `_scratch` filedrop 112/112; all five asserted-clean claims CONFIRMED, zero contradicted. The headline is a ROUTED DECISION that converges with a maintainer directive given independently at the same resume: gate 50 Check 1 is satisfied by row PRESENCE, so #1176's honest `DISPATCHED, RESULT PENDING` row satisfies it and **the parity gate reads green while #1176's QA has never run**. #1178 codifies the convention half and states that the mechanical half is not yet built. Both notes were orchestrator-re-measured, not accepted: the `9/4/14/6 (total 33)` figures misattribute a 6 to a tool absent from its own report (real sum 27), and `73 across 21 tools` overstates coverage because 10 of the 21 probes are VOID, so the 73 spans 11 measured tools and the other 10 are UNKNOWN not zero. The second was a live defect in the probe's summary line (measured numerator over attempted denominator), FIXED in #1178. Worker source `/home/grc/grc_working/inbox/deliveries/opus-20260725T121943Z-78ff__sweep122-resume-validate.md`. Prior: Sweep 120 iter 1 (2026-07-25; the loop-break corpus-wide `/validate` over the **#1105..#1150** deltas (base `b5c08643`=#1104, head `1b8cb202`=#1150, 46 commits / 128 files) at the 2026-07-25 `/resume` from the #1150 session-closing handoff. OFFLOADED to worker-20260716-a as blocking prio-0 `sweep-120-validate` pinned `1b8cb202`, the FIRST sweep delivered over the same-VM file-drop transport. **1 error / 12 warning / 17 note (30 findings). PASS with findings.** Mechanical baseline GREEN and worker-re-derived in its own pinned clone: 77/77, 474-test regression rc 0, both generator `--check` gates in sync, non-shallow (1327 commits); counts 77/15/24/15/18. **Asserted-expectations cross-check: all testable assertions CORROBORATED, 0 CONTRADICTED, so NO miss-signal; loop-break control for #1150 PASSES.** Yield concentrates in two families the per-PR QA structurally could not see: **F1** the `/home/grc` migration landed its narrative but not its wiring (the error plus the hooks warning, FIXED this close-out: `.claude/CLAUDE.md` three prescriptions, `tools/repo-guard.sh`, `.claude/settings.json` statusLine, and five PreToolUse hooks moved to the path-derived `parents[2]` root pattern; a new surface-map row E prevents recurrence), and **F2** two new AI-jurisdiction annexes shipped without the coverage surfaces that name them (five warnings, ROUTED). Hazard link settled by the orchestrator under its own account: `/home/jposluns/grc_library/.git` does not exist, so a prescribed-form command would fail loudly, not silently mutate a backup. 25 findings ROUTED to TODO by severity, none dropped. Worker source `/home/grc/grc_working/opus/outbox/worker-20260716-a/sweep-120-validate.md`. Prior: Sweep 119 iter 1 (2026-07-23b; the loop-break corpus-wide `/validate` over the **#1068..#1104** deltas (base #1067 `3ceb0c54`, head #1104 `b5c08643`) at the 2026-07-23b `/resume` from the #1105 session-closing handoff. OFFLOADED to worker-20260716-b as blocking prio-0 `sweep-119-validate` pinned `b5c08643` (a `main` SHA, per the SHA-pinning practice adopted after alert 2026-07-23-a; ref `924a32e`), consumed under ELEVATED QA (worker-b delivery 1 this fresh session). **CLEAN PASS, 0 error / 0 warning / 0 note.** Baseline **73/73** at the pinned SHA (orchestrator-re-run at HEAD #1105, matches); counts 73/14/24/15/18; four-surface parity 73; gate 54 CSF-clean; gate 37 dual-tree sync; generated artefacts in sync; 457-test regression rc 0. The #1097 vuln-SLA values, #1101 14th-rule wiring, #1102 GAP-1 + pack-parity clauses, and #1104 change-impact map re-verified at source; the one subagent MEDIUM (supplier Tier-1 High=90d) DISMISSED as the maintainer-decided value (pending-decisions §3.68b). All #1101-#1104 asserted-clean surfaces CORROBORATED, 0 contradicted; the pack-README rule-scope-table missing 14th-rule row is the pre-declared known-open drift (§1.18 PR-2), not a miss. **Loop-break control for #1105 PASSES.** No detail file (worker source `grc_library_scratch:results/sweep-119-validate.md`). _(Prior-chain trimmed at the Sweep 121 resume: entries from Sweep 118 back are duplication of [`validate-sweeps/history.md`](validate-sweeps/history.md), which this cursor already names as the full record, so the chain keeps current plus two priors. Nothing is lost; gate 45 reads only the leading sweep number.)_

## Next actions (the queue for the next session)

**RESEQUENCED at the 2026-07-25c `/resume` (#1178). Two maintainer decisions this session move to the
front of the queue and supersede the ordering below for their own items only; everything else keeps
its accepted order.**

1. **Repair the six fused ledger rows, then land TODO 3.73's gate.** The maintainer chose
   repair-first-then-gate. Four of the six fusions DROPPED a row's identifier, so QA audit trail is
   lost, not merely mis-rendered: reconstruct Sweeps 88, 86, 27 and the unidentified one (plus the
   matrix-fit batch) from git history and the per-run detail files, repair all six, then land the
   detector green with no grandfathered exemption set.
2. **TODO 3.122, get `validate-pr-1176` to RETURN.** The order is queued, pinned `462352b1`,
   blocking prio 0, and has NO eligible claimant: both codex workers declined on a documented
   independence conflict and both opus workers are chain-adjacent. A fresh codex worker was
   requested from the maintainer. If none serves it, the orchestrator runs it directly, per the
   rule #1178 adds. It closes on the RESULT, never on a re-dispatch.
3. **TODO 3.120, gate 50 Check 1's third `pending` state.** Sequenced strictly AFTER item 2,
   because it cannot land green until #1176's row is resolved.
4. **Standing this session (maintainer-directed 2026-07-25c):** nudge stale or stopped workers via
   tmux injection (`python3 tools/manage-workers.py --send wake --session <pane>`), rather than
   waiting for them to revive. Two codex sessions had heartbeated exactly once and stopped; a nudge
   revived one. Note the tool's attribution reports AMBIGUOUS or UNKNOWN for the codex panes, so a
   `wake` needs `--force`, which is safe because `wake` is non-destructive.
5. **Unprocessed at close of this PR:** 30 tray deliveries and 8 inbox drops (four worker-raised
   `issue-*`, all four read and dispositioned in [`open-findings.md`](open-findings.md); the other
   four are larger codex framework and continuation documents, still unread). Each drop must be
   MOVED to `done/drops/<YYYY-MM>/` once processed, since location is the only processed-marker.

Then the previously accepted ordering resumes.

**The maintainer ACCEPTED this ordering on 2026-07-25 and it supersedes any earlier queue here.**
Standing sequencing preference, recorded the same day: work everything doable in Priority 1 and
Priority 3 BEFORE starting Priority 2, because P1 is fix-errors and P3 is cleanup-and-tooling while
P2 is content build-out. The one qualification, which the maintainer accepted: item 2.25.3's
RESEARCH is offloaded to workers continuously, since worker capacity is elastic and otherwise idle,
so it advances without displacing P1/P3 orchestrator work.

Items 1 and 2 were COMPLETED in the closing PR, so the queue starts at 3.

1. ~~Run the overdue CHANGELOG condensation (07-22/23/24)~~ DONE in the closing PR.
2. ~~Codify wind-down worker pre-queueing as a standing process~~ DONE in the closing PR.
3. **3.73** ledger-row-fusion gate. Sequenced AHEAD of other tooling: the class escaped to main
   once (#915) and the exposure is active. A design candidate is PRE-QUEUED as
   `design-3.73-ledger-row-gate`.
4. **3.92.a** make `/resume` consume the adopt-config flags `detect-env.py` already emits (it
   references them ZERO times today, so the onboarding decision is still a file-presence check).
5. Fix `submit_state` returning UNVERIFIED when the composer is not in the captured pane tail.
6. Make the disposition token mandatory in `/retro` rows (this unblocks 3.6 later).
7. **3.12** See-Also reciprocity gate, once `measure-3.12-seealso` confirms it lands green.
8. **3.31** per-touch reference-audit delta check, with a metadata-only carve-out.
9. Fix `audit-backlog-actionability.py` over-reporting `maintainer-decision` (it does not
   cross-check the decision stores, so it inflates the blocked count).
10. **3.56** re-triage the pack cleanups once `recover-3.56-scope` returns their scope.
11. **1.23** trust-recovery build. The ONLY actionable P1 item.
12. **3.119** codex workers run unguarded; the hook port is absent.
13. Close the 78 positional-reference defects across 59 files, then gate the pattern.
14. **3.117** a maintainer-placed inbox drop is invisible to every instrument.

Items 15 to 24 are in [`next-prs.txt`](next-prs.txt): 3.113, 2.25.3 (Canada AI cluster), 3.88,
3.115, 2.25.3 (OSFI), 3.60, 3.118, 2.25.3 (ITSG/CCCS), 3.114, 2.25.3 (Privacy Act/OPC/PIPEDA).

## State snapshot (2026-07-24/25 SESSION-CLOSING at #1150, with its Version line reconciled forward to #1168; on the VM)

> **Heading corrected at the Sweep 121 resume.** This block was written as the #1150 closing snapshot, and #1168 then edited its Version-snapshot line in place to describe #1168 instead of adding a snapshot of its own, so the heading said #1150 while one line inside said #1168. That is the append-not-reconcile shape, the same family as Sweep 121's F-1. The heading now says what the block actually is; the Version line is left as #1168 wrote it, because it is the accurate one. The next session-closing handoff writes a proper current snapshot rather than editing this one again.

- **Current truth (verify against live files at `/resume`, which now runs from `/home/grc`)**:
  - **Session / mode:** resumed from #1105; long ATTENDED run; the WORKER-WIRING / same-VM file-drop-transport session; SESSION-CLOSING at #1150. Lease RELEASED; the next `/resume` sets its own mode. **PATH MIGRATION: the next session runs from `/home/grc/grc_library`; all sibling repos are at `/home/grc/` (off `/home/jposluns`, moved to backup); UPDATE ALL `/home/grc` repos at `/resume` FIRST (they may be stale).**
  - **Version snapshot (D7 validates these tokens):** library `2026.07.665`, README `1.10.26` (as of the Sweep 121 close-out PR #1169, which carries this line; the prior session merged #1151 through #1168); pack `1.65.14` (last touched at the #1150 handoff's F1 §4.9 fix; unchanged through this run and #1169, neither of which touches a pack file). Counts independently re-measured by the orchestrator at the Sweep 121 resume and matching the worker's proof-of-run, re-verify again at the next resume: gate **77**, rules **15**, skills **24**, commands **15**, Document-types **18**.
  - **Green-at:** the #1149 merge `3ac1f555` (77/77; pre-push guard green). This #1150 handoff is working-state + the F1/F2 fix + CHANGELOG + version only; `main` stays 77/77 at its descendant merge.
  - **Shipped this session (grc_library + siblings):** #1106-#1150 (full list in [`CHANGELOG.md`](../CHANGELOG.md) / [`DONE.md`](DONE.md)), headline the trust-recovery build (#1147 `audit-validation-coverage.py`, #1148 deep-assessment restructure) and the WORKER-WIRING (`_scratch` #174 transport-aware `/credit-offload`, `_scratch` #175 Codex onboarding core, `grc_library` #1149 command-lockstep fix, #1150 this handoff).
  - **File-drop transport EMPIRICALLY LIVE at close:** `credit-offload-filedrop.py list-workers` showed `worker-20260716-a` (opus) + `codex-mailz-a` (codex) heartbeating via `/home/grc/grc_working`; the `init` layout is pre-provisioned; a real order (`fd-verify-1149-deepassess`) was dispatched to codex to demonstrate the end-to-end loop.
  - **Workers / research:** opus-a, opus-b, and `codex-mailz-a` (family codex, role any). `validate-pr-1149` (git-scratch) delivered CLEAN and was consumed + batched into #1150. PENDING CONSUME next session: `fd-verify-1149-deepassess` (file-drop `codex/outbox`, the first end-to-end file-drop delivery). Re-verify positives at source.
  - **Queue:** the NEXT SESSION block above (update `/home/grc` repos; Sweep 120 loop-break `/validate` over #1106..#1150; consume the offloaded QA; PR-2b Codex `.codex/` hooks + filedrop `list-results`/`self-test` + `orchestrator-claude.md` dispatch mechanics; §1.22.3-b v2; `_ref` branch-protection).

## State snapshot (2026-07-23 SESSION-CLOSING at #1105; on the VM)

- **Current truth (verify against live files at `/resume`)**:
  - **Session / mode:** resumed from #1066 (merged the pending #1067 first); opened OVERNIGHT then ATTENDED-autonomous with heavy maintainer direction; SESSION-CLOSING at #1105. Lease RELEASED (`Status: released`, `Active-session: none`); the next `/resume` sets its own mode.
  - **Version snapshot (D7 validates these tokens):** library `2026.07.592`, README `1.9.953` (the #1106 resume close-out bumps them one patch past the #1105 handoff); pack `1.63.2` (last touched at #1104's D6 change-tracking clause); spec unchanged; gate **73**, rules **14**, skills **24**, commands **15**, Document-types **18** (all mechanically re-verified: `ls` counts + `lint-gate-count-consistency.py`).
  - **Green-at:** the #1104 merge `b5c08643` (73/73; `validate-pr-1104` CLEAN 0/0). This #1105 handoff is working-state + CHANGELOG + version only; `main` stays 73/73 at its descendant merge.
  - **Shipped this session (grc_library):** #1067 (prior resume close-out, merged first) through #1104, notably the **14th rule** #1101, the **Task-1 close** #1102, the two **P3 closes** #1103, and **§1.18 PR-1** #1104; plus the `grc_library_scratch` scratch-CI changed-file-scoping fix (`fec60cac`) and the P1/§1.18/scratch-CI interactive scoping.
  - **Workers / research:** both worker-20260716-a and -b live Opus 4.8. Delivered and banked in `grc_library_scratch:results/` for next session: the **1.1 gate-design seed** (`research-1.1-discussion-execution-gate`), the **Singapore 2.19** (`research-singapore-219`) + **California 2.17** (`research-2.17-california-ai-annex`) annex research (apply, serial), and the **#1104 validate-pr** (CLEAN, batched into this #1105 PR). No open `MAINTAINER_ALERT`.
  - **Queue:** the NEXT SESSION block above (Sweep 119 loop-break `/validate`; then §1.18 PR-2 guard-first gate; the 1.1 design review; the 2.19/2.17 annexes; then P2 by severity + P3). `pending-decisions.md` holds the OWASP ASI08/09/10 decision. 1.19.13 held (first-thing-in-a-morning + ask-at-overnight-mode-change); 1.22.3(b) DONE-sweep cutoff = daily.

## Asserted expectations (session close-out convention)

**Session of 2026-07-25, PRs #1169 to #1177 (this closing PR).** What this session MECHANICALLY
verified, scoped to what it touched. The receiving `/resume` `/validate` cross-checks these: a
finding that CONTRADICTS a claim here is a genuine miss to escalate, not an ordinary finding.

**Asserted clean.** All 78 gates pass on the closing tree, and the pre-push guard (both runners)
passed before each of #1175 and #1176. Self-tests at close: `manage-workers` 47/47,
`audit-token-spend` 34/34, `audit-worker-saturation` 44/44, `audit-selftest-discriminability`
17/17, and in `_scratch` `credit-offload-filedrop` 112/112. Gate 50 including its new Check 6
passes, so every in-window merged PR has both a `/validate-pr` row and a bypass-log row.
`governance/specification-audit-programme.md` carries ZERO `TODO section` citations (measured).
The `.claude/rules/` and pack trees are in sync (gate 37).

**NOT asserted clean, and these are the soft spots to probe first.**
1. **Per-tool discriminability figures.** They were wrong twice in one day and corrected twice.
   The figures 9/4/14/6 (total 33) come from each tool's OWN summary line at #1176. Any count in
   this repository derived from a grep over a tool's output should be distrusted: that mechanism
   produced three wrong counts of mine on 2026-07-25.
   > **CORRECTED at the Sweep 122 close-out (#1178), and it was wrong a fourth time.** The claim
   > above is left as written because it is the record of what was asserted; this note is the
   > correction. Sweep 122 found, and the orchestrator re-measured from a fresh probe run rather
   > than accepting the delivery, that `audit-selftest-discriminability.py` appears **zero** times
   > in its own report, so no figure of 6 is attributable to it. The two tools that do report 6 are
   > `audit-delivery-status.py` and `audit-inbox-drops.py`, neither of them among the named four.
   > The three real figures are 9 (`audit-worker-saturation`), 4 (`audit-token-spend`) and 14
   > (`manage-workers`), summing to **27, not 33**. A probe omitting itself is very likely by
   > design; the defect is attributing a count to a tool the report does not measure, which is the
   > fourth instance of the very mechanism this soft-spot sentence warns about.
2. **`submit_state` indeterminacy.** It returns UNVERIFIED whenever the composer box is not in the
   captured pane tail, which happened repeatedly against live codex panes. Prompts DID submit each
   time (verified by eye). Queue item 5 fixes it. Until then, treat a tmux nudge as unconfirmed.
3. **73 NOT-DETECTED guards across 21 self-tested tools.** Known and unaddressed; only the four
   worker tools have been examined in detail.
   > **CORRECTED at the Sweep 122 close-out (#1178): the denominator overstates the coverage.**
   > Re-measured from a fresh probe run: 21 tools were probed, but **10 of those probes are VOID**
   > (the positive control did not fire, so the probe cannot see a failing self-test and would
   > report nothing evidential). A void block carries no figures at all, so the 73 spans the **11
   > tools the run could MEASURE**, and the exposure across the other 10 is **UNKNOWN, not zero**.
   > "73 across 21" therefore reads as full coverage of 21 tools when the true figure is larger by
   > an unmeasured amount. The void set: `audit-changelog-entry-length`, `audit-matrix-semantic-fit`,
   > `audit-register-currency`, `audit-validation-coverage`, `check-changelog-length-on-pr`,
   > `detect-env`, `lint-gate-citation-inventory`, `lint-skill-internal-refs`,
   > `lint-web-corpus-links`, `ref-holds`. This was a live defect in the probe's own summary line,
   > which divided a measured numerator by an attempted denominator; **FIXED in #1178**, so a future
   > run states the split itself and no reader has to re-derive it.
4. **The deferred-review closures.** Six backlog items were closed on evidence gathered this
   session. `validate-pr-1176` is PRE-QUEUED and asks for those closures to be judged
   adversarially, because a wrongly-closed item is invisible afterwards.
5. **The 78 positional-reference defects** across 59 files are MEASURED and UNFIXED (queue item 13).

**Green at `c009e041`** (this closing PR's head before merge): `tools/run_all_audits.sh` reports all 78
gates passing; `tools/pre-push-guard.sh` green on both runners.

**PRE-QUEUED worker orders awaiting the next resume** (name them so a missing delivery is
distinguishable from one never ordered): `validate-pr-1176` (blocking, prio 0, codex family),
`design-3.73-ledger-row-gate` (opus). Still in flight from this session: `fnaudit-sweep121`,
`selftest-gaps-workers-deliveries`, `recover-3.56-scope`, `measure-3.12-seealso`,
`research-2.21-texas-traiga`, `hunt-order-premise-gaps`, `selftest-gaps-saturation-inbox`.

## Open decisions awaiting maintainer

- **QUEUE STATUS 2026-07-18b (wind-down): EMPTY (no blocking pending decision).** [`pending-decisions.md`](pending-decisions.md) is empty. This session's maintainer directions are DECIDED, not pending, and captured in the "Next actions" block above: **§1.19.12 DEFERRED** to a fully-awake session (unhurried surgical time; locked classification ready), **§1.19.13 GATED** (LAST), **both workers stay Opus 4.8** (Fable-5 experiment deferred), the **§1.19.x-moves worker-QA extra-care** directive, the **maintainer-alert SOP** now live, and the **operating-mode transition** (resume starts attended-autonomous, switches to overnight-unattended in a few hours). The maintainer-alert channel had its 3 morning alerts cleared, then validate-pr-1038 logged one new alert **F1** (the resume.md/CLAUDE.md clearing-authority inconsistency, FIXED in #1039); F1 is surfaced for the maintainer's clear-decision (may carry into next session if undecided at close). No decision is carried forward as blocking. The entries below are the durable historical decision record (mostly long-RESOLVED), retained per keep-current-plus-prior and pruned at resume; none is live.
- **RESOLVED (2026-07-01 at `/resume`; recorded in [`pending-decisions.md`](pending-decisions.md)):** the two 2026-07-01 pending decisions were answered by the maintainer. (1) **§3.2 detailed-CHANGELOG-mirror header-parity** = **cutoff-scoped gate** (accept the 3 pre-split-era missing headers #268/#353/#462 as an exemption; scope the parity gate from a cutoff PR forward; FP-free, no retroactive edit). (2) **§3.3 citation-verification recording-model** = **consistency cross-check, no register row** (register-vs-held-extract check surfacing/fixing mismatches only; the §9 human-primary-capture trust model unchanged). Both are now **P3 tooling** work, scheduled after the P1 FR-48 rename per the maintainer's post-P1 = P3-tooling direction.
- **OPEN (surfaced 2026-07-01): FR-70 source gate.** FR-70 (crypto-asset / blockchain governance, XL, H[critical], authorized this run via the harness) is source-gated: the high-assurance harness for a H[critical] regulatory domain needs ground truth that is not yet available (reference-base work tracked separately in the reference repo). Needs the maintainer to supply the missing primary sources, OR authorize authoring the crypto-regulatory core from training knowledge (advised against), OR redirect.
- **§6.3-vs-§7.3 audit-scope spec gap**: **CLOSED in #338.** Sweep 45 found that #336's "added to all 9 explicit-list content linters" enumeration was incomplete: gate 31 (date-staleness) and gate 10 (review-cadence), two more explicit-allow-list content gates, silently skipped the dir (gate 31 a clear §6.3 violation since §6.3 names "date currency"). #338 added `.project-governance` to both (with a scope-coverage regression test each) and amended the spec with **§7.4**, which enumerates the explicit-allow-list content-linter completeness obligation (the maintainer chose, 2026-06-25, to include gate 10 and to amend the spec). The maintainer-decided spec amendment closes the decision; the **directory-scan-scope parity meta-check** (TODO P2) is the queued mechanical backstop that would have caught this class.
- **R2 relocation**: CLOSED by principle in #314 (the project-governance separation spec classifies the 6-file citation-verification cluster as project governance, so it migrates in Phase 1). The Phase-1 migration, the queued directional-dependency gate (§7.3), and the 2 deferred §5.3 classifications are now forward-looking TODO items, not open decisions awaiting the maintainer.
- **FR-167 mapping gate (asked 2026-06-24)**: RESOLVED, built as gate 49 (#325 ISO + NIST well-formedness; #326 NIST category membership + 17-cell remap closing §4.6a). The control-code-validity gate catches hallucinated/mistyped codes; semantic mapping correctness remains the orchestrator's apply-time job. No longer awaiting.
- **DD-12 scope**: RESOLVED + APPLIED (#329, maintainer-approved "broaden + extend gate 49"). DD-12 in TODO is broadened from `PR.IP`-only to all CSF-1.1 carriers (`PR.IP`/`ID.SC`/`ID.BE`/`RS.RP`/`DE.DP`/`PR.AC`/`PR.PT`/...; `RS.RP`→mainly `RS.MA`), and a **gate-49-extension** TODO item is queued (validate framework codes in per-document reference tables, not only the central matrix; build the scanner first, then gate the migration). Both are now forward-looking TODO items, not open decisions. The migration itself (corpus-wide, non-partitionable) is queued.
- **Publications-assessment process (§4.12, surfaced + queued 2026-06-25)**: a maintainer-directed process to assess reference-base publications for useful info AND detect poisoning/false info before it informs corpus work, queued as TODO §4.12 (not yet built). Forward-looking, not an open decision.
- **Maintainer actions still pending**: (a) **seed the reference binaries** durably (git-proxy blocks writes), belt-and-suspenders ONLY: the in-repo reference modules gates 48/49 use are the authoritative validators, so FR-167 batch 5+ code validity is gate-protected without them; re-attach only if a worker wants the source text; (b) **provision the least-privilege external-worker account** (read `grc_library` / write `grc_library_scratch` only), this is the gating action for both the separate-session worker primitive (§4.11) and the queued **§4.4** worker-ready brief staging / `/subagent` capability. Neither blocks the next session's queue (in-session `Agent` fan-out works for FR-167 today).
- The larger-track decisions (FR-167 batches 4..N, the High[critical] net-new docs, the L/XL items) remain queued and scheduled deliberately.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Codification COMPLETE. Not re-triggered since; quality held throughout the 2026-06-24 overnight run, morning continuation, and the resume session (Sweep 38 + close-out #312, both warnings fixed first try, post-commit + pre-push green).

## Known environment behaviours (read before assuming working-tree state)

- **The stop-hook auto-commits AND pushes uncommitted changes on turn-end.** The working tree is auto-persisted to the feature branch; verify `git log` rather than assuming edits are held locally.
- **The squash-merge commit on `main` shows locally as `E noreply@github.com`** (GitHub's own merge commit; Verified in the GitHub UI, not locally verifiable). After syncing the branch to `main` the tip equals `origin/main`; **do NOT `git commit --amend`** it (that rewrites merged `main` history). Set `git config user.email noreply@anthropic.com && git config user.name Claude` so your own feature-branch commits are attributed correctly.
- **A squash-merge makes the local feature branch diverge from `main`** (the squash commit is new; the local pre-squash commit is its content but a different SHA), so `git merge --ff-only origin/main` fails after a merge; use `git reset --hard origin/main` to re-sync the feature branch (the local commit's content is in the squash, preserved in reflog).
- **The GitHub MCP server can disconnect mid-session** (it did 2026-06-24 after #304, blocking #305's open/merge). `git push` over HTTPS keeps working; only the MCP-routed GitHub-API operations are affected. If `mcp__github__*` tools vanish: keep committing and pushing via `git`, record the pending-merge state in the handoff, and resume the PR lifecycle when MCP returns. Do NOT merge by any non-MCP path. Full writeup: [`third-party-issues.md`](third-party-issues.md).
- **The commit-signing server can 503**, distinguish from a real defect (gates 31/40 pass on the real corpus while gate 36's failures are `git commit` subprocess errors); re-run after a pause. Full writeup: [`third-party-issues.md`](third-party-issues.md).
- **The clone may start shallow**; `git fetch --unshallow` before any history-aware audit (gates 31/40).
- **The `Bash` tool's working directory can reset to a non-repo directory between calls** (observed twice this session after long async-subagent gaps: a bare `git ...` failed with "not a git repository"). Prefix git-command sequences with `cd /home/user/grc_library &&` rather than assuming the cwd persisted.
- **After a post-merge sync you are ON `main`; `git checkout -B <feature-branch>` BEFORE building the next PR.** The post-merge sync (`git checkout main && git pull origin main`) leaves you on `main`. If you then build and `git commit` the next PR without switching branches, you commit to local `main` (which the stop-hook flags as an unverified commit ahead of `origin/main`), and a subsequent `git push -u origin <feature-branch>` pushes the STALE feature-branch ref (still at the prior PR's pre-squash commit), so the PR opens with an empty/wrong diff. This happened on the #361 handoff (the commit landed on local `main` as `2b589cd`; recovery was `git checkout -B <feature> <commit>` to repoint the feature branch, `git branch -f main origin/main` to undo the local-main commit, then a force-push of the feature branch). Recovery is clean and on-branch (no `main` push, no shared-history rewrite), but the fix is cheaper than the catch: switch to the feature branch immediately after the sync.
- **An execution-environment probe now exists; the `/resume` step 3 runs it.** `python3 tools/detect-env.py` (TODO 3.18, shipped) profiles the transport/tooling assumptions that diverge between the managed cloud sandbox and the local VM (gh presence/auth/rate, sibling-repo access with launch-bound fix lines, per-family egress classes, the stop-hook and pipe-guard as ASSISTANT-PROBE lines the script cannot self-observe); the `/resume` step-3 wiring reads its profile to pick the PR mechanism, the CI/merge transport, the commit-push mode, and the pipe-guard expectation. It never self-grants access (`--add-dir` / `settings.local.json` fixes are surfaced to the maintainer; they bind at launch). Observed VM profile: gh authenticated, GraphQL pool healthy, pipe-guard fires, `grc_library_ref`/`grc_library_scratch` readable, iso.org 403 and planalto.gov.br unreachable.
- **After a squash-merge, the stop-hook flags the GitHub merge commit as Unverified; do NOT amend it.** When the designated branch is restarted from the merged `main` (`git checkout -B <feature> origin/main`), its tip becomes GitHub's squash-merge commit (committer `noreply@github.com`), which the stop-hook reports as Unverified and suggests amending. DECLINE the amend: amending rewrites already-merged `main` history (forbidden), and GitHub signs its own merge commits (they show Verified on the platform; the local `%G?` check cannot see that). The flag clears once the next authored commit lands on the branch. (Observed at #681; predictably recurs each merge on the reused branch.)
- **Operating-mode mechanics** (set 2026-06-26, codified in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) #349): green CI = standing merge authority (merge green PRs and proceed without per-merge approval), stricter-is-safer always, and the pending-decisions / 2-minute-timeout graceful-degradation mechanism ([`pending-decisions.md`](pending-decisions.md)). The `/resume` command has a step 7 that checks `pending-decisions.md` before the queue. **Current mode: ATTENDED-AUTONOMOUS (maintainer-set 2026-07-05, the `claude/resume-tl5rez` resumed session, Q1=A)**: green CI = merge authority (merge own green PRs and proceed, decisions surfaced by exception); full per-PR `/validate-pr` + `/retro` always; stricter-is-safer always. This is NOT overnight/daytime-unattended, so there is no skip-to-morning or timeout-to-default path; genuine maintainer decisions are asked, not deferred. This session's queue (Q2=A): clear the four resolved-but-unexecuted pending items + the coverage-refresh scratch sync + the small P3 items, then P2 2.1. Egress re-tested at resume (Q3=try-then-defer): egress is up (control host loaded) but planalto.gov.br 503'd and iso.org 403'd, so the upstream-verification items (1.11 Brazil verification, 1.5's 51 needs-reconfirm rows, FR-70 sources) STAY DEFERRED; the Brazil annotation proceeds. The mode-exit priority ordering (overnight cleanup, then fixes, then tooling and protections, then new work) is codified in `.claude/CLAUDE.md`.

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Speed > Cost; the AIQT tier non-negotiable. Emit the AIQT-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **`lint-language` pre-flight on new pack prose** before the first commit (catches em-dashes / British `-ise`). (Relevant for DD-4/5's `go.md` rewrite.)
- **Pre-commit dash-grep on new root `CHANGELOG.md` lines** (`grep -nP '[\x{2013}\x{2014}]'`, the codepoint form; the older byte-sequence form `\xe2\x80\x93|\xe2\x80\x94` matches nothing in a UTF-8 locale and returns a false-clean, confirmed 2026-07-10, so use the codepoint form or `LC_ALL=C` with the byte form): the D3 dash gate is PR-time only, so a late-assembled CHANGELOG entry can slip an em-dash that surfaces at pre-push; grep the added lines before the first commit. The same false-clean bit the sweep94 detail file (em-dashes pasted verbatim from subagent returns), caught by gate 51.
- **Grep-after-wiring / convention change**: after editing a restated-across-surfaces value, `grep` the OLD form across the full changed file AND every sibling surface; zero hits before commit.
- **Corpus-wide-grep / special-case-the-edge / find-every-carrier**: a mechanical bulk edit (a rename, a relabel, a title alignment) must verify EVERY adjacent field, special-case the known edge cases (e.g. preserve rating "Critical" while fixing impact-5; the DD-2/3/11 grep found a 4th carrier beyond the 3 named), and search corpus-wide for the OLD form, not apply one convenient rule uniformly.
- **Sweep close-out bookkeeping triplet**: a `/validate` close-out PR regenerates the generated artefacts (after per-doc version bumps), advances the TODO sweep cursor (gate 45 + the gate-36 TodoStaleness regression both enforce it), and bumps `validate-sweeps/history.md`'s own Version. The post-commit audit catches all three; doing them pre-commit avoids the fail-then-fix loop.
- **60-second** paired fallback timer after every `subscribe_pr_activity`.
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation. **One standing exception**: the session-closing handoff PR skips both (loop-break); the compensating control is the corpus-wide `/validate` that `/resume` runs first. (This exception is now generalized into the pack layer, #305.)
- **PR close-out checklist** (the degradation guard): prior PR's `/validate-pr` row AND `/retro` row both batched in; closed TODO items rotated to DONE (every path-shaped code span in a CHANGELOG entry linked, changed or merely mentioned); stale-count check if an enumerated collection changed; session-handoff.md refreshed.
- **Self-assess for degradation / session-continuation SOP**: the default is to CONTINUE. Wind down ONLY on actual drift/hallucination/mistakes the QA layer did not catch; work size/shape, session length, and "a large / substantial / fresh-context-best series remains" are NOT triggers (corrected #460, maintainer 2026-06-29: about 13 of the last 15 proposed handoffs were the wrong call). A large series ahead is worked PR-by-PR with skeptical verifier subagents sustaining quality, not handed off. Steady-state misses the per-PR `/validate-pr` catches are NOT drift. The assistant may OFFER a handoff for the maintainer to consider before a substantial/critical/long piece of work begins, as a non-default suggestion (the maintainer chooses; absent a choice, continue). **When a handoff IS warranted (genuine degradation evidence), do NOT take it silently: run the `## Wind-down decision framework` in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)** (surface the justification + a per-PR likelihood assessment of the next-five PRs + named options A handoff / B recommended additional PRs / C higher-risk order / D the Ulysses-pact impulse-check; roughly-2-minute timer defaulting to handoff on no answer; codified #375, corrected #460).
- **Compute-don't-ask**: before surfacing a question, apply a "can I compute/verify this myself?" gate; surface only the result or a decision that genuinely needs maintainer judgement. (Counterpart: surface a genuine design tradeoff before building, as S5's FP surface was surfaced with named options rather than guessed.)

## Refresh and pruning discipline

**Refresh (at session close).** This file is refreshed at every PR close-out (post-merge), as part of the recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The session-closing handoff PR prepends this session's new blocks (the "Next actions" narrative block, the "State snapshot", and the "Asserted expectations" block) as the new *current* set.

**Prune (at resume, in the first PR).** Because the closing session only ever *adds*, the per-session blocks would otherwise accumulate without bound and bury the load-bearing state (the file's one job is a fast, reliable single resume point). So the receiving session prunes, as part of its first PR (the `/validate` close-out, per `## How to resume` step 6):

- **Retention: keep current + 1 prior.** Keep the most-recent session's blocks and the single immediately-prior session's blocks in each per-session stack (the "Next actions" narrative blocks, the "State snapshot" blocks, the "Asserted expectations" blocks). Delete everything older. Also delete superseded one-off "Next-session queue" / dated "This session's work" sections.
- **Keep the standing sections in full** (not per-session): the header / `## How to resume` / `## Resume cursor`, the `## Open decisions awaiting maintainer`, `## Trust-recovery state`, `## Known environment behaviours`, `## Standing disciplines`, and this section. These are durable reference, not session narrative.
- **Neutralize the dangling "supersedes ... below" pointer.** After deleting the oldest per-session blocks, the newly-oldest-retained block's own `**Superseding note:** ... supersedes the #<pruned> block below` clause now points at a block that no longer exists. Reword that one clause (drop "below", mark it "(pruned at the Sweep N resume)") so the prune does not leave a dangling internal pointer (the #852 `/validate-pr` note-2 finding).
- **Migrate-before-delete (the safety rule).** Before deleting a block, confirm any load-bearing item it carries that is NOT recorded elsewhere (an open decision, a pending maintainer action) has been migrated to `## Open decisions awaiting maintainer` / [`TODO.md`](../TODO.md) / [`pending-decisions.md`](pending-decisions.md). The durable record of pruned session *narrative* already lives in [`CHANGELOG.md`](../CHANGELOG.md) + its detailed mirror, [`DONE.md`](DONE.md), [`validate-sweeps/history.md`](validate-sweeps/history.md), [`session-metrics.md`](session-metrics.md), and git history, so narrative is safe to drop; only un-recorded forward-looking items need migrating.

The companion close-out-checklist line and the `/resume` command step encode this so it is a standing convention, not a one-off. This convention was added 2026-06-28 by maintainer direction after the file reached 426 lines / 47 stacked session blocks; the first prune cut it to ~120.
