# Overnight PR

**Status:** in-flight

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

## 2026-07-07 overnight run (NUC session, resume `remove-ref-worker-exchange-only` lineage)

**Authorization scope (maintainer-directed 2026-07-07 evening):**

1. **Overnight autonomous.** Keep working the authorized queue through the night; merge on green CI; skip-to-morning on any conflict; per-PR QA unabbreviated; stage protected-file (`.claude/`, pack) changes into [`deferred-protected-changes.md`](deferred-protected-changes.md) for daytime authorization. Overnight mode ends ONLY on an explicit maintainer signal, never a timeout.
2. **Cross-repo parallelism authorized.** Ref-base (`grc_library_ref`) ingestion runs via subagents concurrently with orchestrator corpus (`grc_library`) work (separate repos, separate catalogues/CI, no state collision). Integrity rule: ref MERGES stay serial on the ref catalogue (one ref worker in flight at a time, cut off the latest ref main, zero catalogue-conflict risk); apply-time verification + gate + CI run on every merge, ref or corpus. Quality > Speed > Cost is explicit and absolute.
3. **Egress: all reachable-source items proceed.** On the NUC, Planalto / ANPD / IEC-webstore return HTTP 200; only iso.org 403s automated fetch. So the egress-gated backlog proceeds for reachable sources (1.11 Brazil ANPD; non-iso.org currency rows; IEC-webstore-checkable items). Only strictly-iso.org-sourced items stay deferred (ISO version currency via iso.org + the ISO/IEC designation register's iso.org lookups).
4. **Reference-source currency ruling.** The maintainer authoritatively confirms the relevant reference sources current as of **2026-07-01** (the maintainer is the authoritative source for their own downloads; this replaces the iso.org check that 403s). This unblocks the SR-1 `last_checked` backfill (reference-base work tracked separately in the reference repo).
5. **SP 800-154 defect: replace with a finalized source.** The corpus cites NIST SP 800-154 (Data-Centric System Threat Modeling, never finalized, 2016 draft) in 2 supplementary-framework lists (measured; the earlier "3x" estimate was wrong). Re-ground those in a finalized source where one covers the same ground, and drop the 800-154 citation (corpus PR). Substitute choice DEFERRED to the maintainer (no finalized NIST 1:1 exists).
6. **Complete reference-base work, then pivot to corpus.** Reference quality feeds corpus quality, so finish the relevant reference-base work (tracked separately in the reference repo) then pivot to the corpus queue. Under cross-repo parallelism these overlap rather than strictly sequence.

**Build progress (updated as PRs land):**

- grc_library_ref: reference-base work merged this session (tracked separately in the reference repo).
- grc_library_scratch: PR #108 (worker-exchange-only reframe, split 3b).
- grc_library corpus PRs this session: #687 (Sweep-88 + TODO 1.12), #688/#689 (reference-library split re-point).

## 2026-07-08 overnight run (changelog-restructure + egress queue)

**Authorization scope (maintainer-directed 2026-07-08, "I'm going to sleep. Swap to overnight mode."):**

1. **Complete the changelog-restructure changes as discussed**, erring on the side of caution and integrity. The agreed design: (a) the detailed-CHANGELOG mirror + per-run records keep only the CURRENT WEEK in-repo, completed weeks swept to `grc_library_scratch` weekly Monday-dated archives (full per-PR sweep machinery); (b) the root `CHANGELOG.md` keeps full history but each entry compressed to 1-2 sentences in the compact `**date | version | PR** - summary` format; (c) `.gitattributes export-ignore` on `.working/` (the 3.19 resolution). Sequenced: PR 1 machinery (gate-59 dynamic cutoff + sweep tool + export-ignore + docs, no data moved); PR 2 the data-safe sweep (populate scratch archives, verify, prune) + per-PR sweep step; PR 3+ the root reformat then compression.
2. **Protected-file edits DEFERRED** per the standing overnight rule: the change-tracking rule/skill and CLAUDE.md descriptive edits (the model write-up + the per-PR sweep workflow step) are staged in [`deferred-protected-changes.md`](deferred-protected-changes.md), not applied overnight. The non-protected machinery (tools, `.gitattributes`, `.working/` docs, fixtures, corpus audit-programme narrative) ships now.
3. **Correct any issues first**, then proceed through the queue prioritizing **egress-needs** (the egress-gated backlog: TODO 1.5 / 1.11 residual / GR-GAP-1 / SR-1 and the 11 legislation deepenings, for reachable sources; iso.org-only items stay deferred). Standing overnight rules carry over: merge on green CI, per-PR QA unabbreviated, no idle-stop, stricter-is-safer, overnight mode ends only on an explicit maintainer signal.

**Build progress (2026-07-08 overnight, updated as PRs land):**

- PR #694 (pre-overnight, this session): `/full-qa` follow-up corrections merged.
- Changelog-restructure **PR 1 (machinery) MERGED as #695** (gate-59 dynamic cutoff + `tools/sweep-working-records-to-scratch.py` + `.gitattributes export-ignore` + model docs; pre-push skeptical verifier caught 2 findings (gate-59 floor-boundary limitation documented + a stale by-one count) both fixed and re-verified; a P7 gate-39 phrasing trip caught by the guard and fixed; CI green).
- Changelog-restructure **PR 2 (the sweep) BLOCKED** on a maintainer decision: staging the archive in scratch trips scratch's `validate.py` Check 5 (the `jposluns` maintainer-watermark token in historical entries) + Check 6 (dash/style). Recorded in [`pending-decisions.md`](pending-decisions.md) with options (recommend exempting the frozen `archive/` from scratch's checks). grc_library and scratch both left clean; no data moved.
- Changelog-restructure **PR 3 (root reformat + compress) DEFERRED** as a wide sensitive change (de-headings 679 entries + gate-parser changes + a 679-entry judgment compression), recommend attended / fresh-context per the err-on-caution directive. Recorded in `pending-decisions.md`.
- **Pivoted to the egress-prioritized queue** per the maintainer's directive: TODO 1.11 residual (the ANPD Resolution 15/2024 small-scale-agent deadline-doubling sub-clause) in flight on `2026-07-08-todo111-anpd-residual` (egress confirmed reachable this session). Carried the batched #695 `/validate-pr` + `/retro` rows and the PR-2/PR-3 deferral records.
- **#696 MERGED** (TODO 1.11 residual: the ANPD doubling confirmed at SECONDARY tier via three consistent reads of the resolution text, 1.11 kept OPEN for a primary re-confirmation; a skeptical verifier found no defect).
- **FR-63 (§2.7, adoption worked example) MERGED as #697** on `2026-07-08-fr63-adoption-worked-example`: authored the new [`docs/worked-example-adoption.md`](../docs/worked-example-adoption.md) from a fresh-context research delivery (the 77-commit-stale scaffold reconciled), wired via mutual Related-Documents pointers (the five-path entry-point-list cascade correctly avoided per the fresh re-read), closes §2.7 / FR-63; carried the batched #696 QA rows; a skeptical verifier found no defect.
- **#698 in flight** (`2026-07-08-qa-catalogue-batch`): folds in #697's out-of-window `/validate-pr` notes (the README companion-catalogue row + the session-state Current-task reconcile), batches #697's QA, and records the register-ageing tool (TODO 3.15) deferral (a prototype was built + tested but its heuristic over-flags adopted-habit notes; it needs a classifier-design refinement, so it was not shipped).
- **Queue state after #698 (honest):** the readily-actionable UNBLOCKED substantive queue is thin. The remaining items are blocked or deferred: changelog PR 2 (the sweep) on the scratch privacy-gate decision; changelog PR 3 (root reformat/compress) deferred as a wide sensitive change; the alignment maps (3.16 ETSI / 3.17 ATLAS) on surfaced-not-picked authorial alignment-shape and trust-tier decisions; the register-ageing tool on a classifier-design refinement; the egress-priority items (GR-GAP-1, the 11 legislation deepenings) on iso.org / the maintainer's egress instance. All are recorded in [`pending-decisions.md`](pending-decisions.md) / TODO for the maintainer's morning triage.
- **#699 SESSION-CLOSING HANDOFF (this PR), WIND-DOWN, maintainer-directed 2026-07-08 ("wind down and we'll start a new session. that session will end overnight mode, ask me the deferred questions, clarifications, and begin attended autonomous daytime mode").** This file stays `Status: in-flight` (gate 46 passes on `in-flight`); the NEXT session does the morning-processing (routes both the 2026-07-07 and 2026-07-08 run sections above to the ledgers, discards the build-progress noise, and resets this file to `stub`) AS PART OF ending overnight mode. The session-closing handoff #699 releases the lease and batches the #698 QA rows; per the loop-break it takes no trailing per-PR QA, the compensating control being the next `/resume`'s corpus-wide `/validate` over #687..#699. The maintainer's next-session directive (end overnight, morning-process this file, ask the deferred questions/clarifications, begin attended-autonomous daytime) is recorded in [`session-handoff.md`](session-handoff.md)'s CLOSING next-actions block.

**Reference-base queue remaining (Phase A, cross-repo-parallel with corpus):** reference-base work (tracked separately in the reference repo).

**Corpus queue (Phase B):** this bookkeeping PR (batched #687-689 validate-pr/retro rows + retro-row-malformation fix + reference-base and currency notes + SP 800-154 TODO); SP 800-154 replace; fast-follow #6 (reference-source schema codification + citation-not-embed gate + forkability note); egress-unblocked items (1.11 Brazil, non-iso.org currency rows, legislation deepenings 2.1-batch-2/2.2/2.8/2.10/2.12/2.13 + jurisdiction annexes); non-legislation (#8: FR-63, 3.16/3.17, small P3/P4); scratch coverage-refresh sync (#10).

**Open ambiguities / maintainer items surfaced:** the fast-follow license-schema shape (formal `license:` field vs codify the established convention) defaults to codify-the-convention unless redirected; a reference-source re-snapshot cadence is a low-priority currency-watch to establish.

<!-- OVERNIGHT-PR-STUB -->

## Last run closure note: 2026-07-06 overnight (routed by PR #673, the morning-processing PR)

The 2026-07-06 overnight run (resume session `claude/resume-tl5rez`) shipped PRs #667 through #671: TODO 3.21 close (#667) and its 3.21(d) follow-through (#668, `PCI DSS v4` to `v4.0.1`), the TODO 1.9 PreToolUse-hook-firing root-cause record (#669), the TODO 3.15 #637 F4/F6 acronym-linter digit-initial widening (#670), and the TODO 3.15 r4 G-7 QA-report intake runbook subsection (#671). Each shipped with its own DONE entry and per-PR `/validate-pr` + `/retro` rows.

Content routing (morning-processing):
- **Design decisions** to [`design-decisions.md`](design-decisions.md): the PCI DSS "full latest version" citation-form standing preference (recorded in-run under #668); the 3.21(a) bare `C-TPAT` choice was a per-item maintainer decision recorded in [`DONE.md`](DONE.md) #667, not a standing principle. No un-routed design decision remained.
- **Closed work** to [`DONE.md`](DONE.md): routed per-PR during the run (#667 through #671 each added its entry).
- **Queued follow-ups** to [`../TODO.md`](../TODO.md): none new. The 3.21(a) matrix framework-key full-name-consistency observation was deliberately NOT raised as an item absent a signal (recorded here for provenance only).
- **Deferred to the daytime protected-backlog** ([`deferred-protected-changes.md`](deferred-protected-changes.md)): the `/claim-fit` cadence clause (item 5, content-ready) and TODO 3.15 #637 F3 (D5 eighth closure-form, protected-entangled: the "seven closure forms" count in the protected `.claude/CLAUDE.md` must co-update to eight in the same PR). Both cleared in the daytime session that follows this reset.
- **Noise discarded**: the build-progress and files-modified lists.

Maintainer items surfaced from the run: the morning time-decay-on-publications recommendation (delivered); the reference-base publications assessment (net no ingest); the #670 lowercase-tolerant-inline-pattern rejection (surfaced to confirm or reopen); and the TODO 1.9 close-vs-track disposition (held in [`pending-decisions.md`](pending-decisions.md)).
