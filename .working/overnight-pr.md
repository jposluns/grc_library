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
4. **ISO currency ruling.** The held `grc_library_ref` ISO standards were downloaded in the past few weeks; the maintainer authoritatively confirms them current as of **2026-07-01**. Stamp held ISO standards `last_checked: 2026-07-01` on that authority (the maintainer is the authoritative source for their own downloads; this replaces the iso.org check that 403s). This unblocks the SR-1 `last_checked` backfill for held ISO standards.
5. **SP 800-154 defect: replace with a finalized source.** The corpus cites NIST SP 800-154 (Data-Centric System Threat Modeling, never finalized, 2016 draft) in 2 supplementary-framework lists (measured; the harvest scoping's "3x" was wrong). Re-ground those in a finalized held source where one covers the same ground, and drop the 800-154 citation (corpus PR). Substitute choice DEFERRED to the maintainer (no finalized NIST 1:1 exists).
6. **Complete ref ingestion of everything relevant, then pivot to corpus.** Ref quality feeds corpus quality, so finish the relevant ref ingestion (RFC-0006 draft; GSA FedRAMP OSCAL baselines; Tier-C NIST ~30; draft-watch items IR 8596 / COSAiS / Privacy Framework 1.1, ingest-as-draft + finalization watch; SR-1 backfill; SR-2/SR-3 ref tooling) then pivot to the corpus queue. Under cross-repo parallelism these overlap rather than strictly sequence.

**Build progress (updated as PRs land):**

- grc_library_ref PRs merged this session: #5-13 (NIST harvest, ~65 net-new), #14-19 (OWASP: Top 10:2025, API, Proactive Controls, ASVS, SAMM, WSTG, Cheat Sheets, MASVS, MASTG, CycloneDX), #20 (MITRE CWE/CAPEC/D3FEND), #21 (FedRAMP 2026 into programs/FedRAMP/), #22 (CycloneDX 1.7 -> 1.7.1 re-point), #23 (FedRAMP RFC-0006 draft-as-published). Tier-C NIST (9 docs) staged on branch nist-tierc-batch, pending verify+merge. GSA Rev5 OSCAL HELD (source repo 404 / deprecated; maintainer decision). CycloneDX 1.7.1 applied.
- grc_library_scratch: PR #108 (worker-exchange-only reframe, split 3b).
- grc_library corpus PRs this session: #687 (Sweep-88 + TODO 1.12), #688/#689 (reference-library split re-point).

**Ref queue remaining (Phase A, cross-repo-parallel with corpus):** RFC-0006 draft-as-published; GSA FedRAMP OSCAL baselines; Tier-C NIST (~30); draft-watch (IR 8596, COSAiS, Privacy Framework 1.1); SR-1 last_checked backfill (ISO 2026-07-01 + reachable-source currency); SR-2 publications screening-record check; SR-3 binary-scan coverage widening (load-bearing scrub-promise enforcement).

**Corpus queue (Phase B):** this bookkeeping PR (batched #687-689 validate-pr/retro rows + retro-row-malformation fix + RB TODO + NIST currency/vocab notes + SP 800-154 TODO + draft-watch TODO); SP 800-154 replace; fast-follow #6 (ref license/access_tier schema codification + citation-not-embed gate + forkability note); egress-unblocked items (1.11 Brazil, non-iso.org currency rows, legislation deepenings 2.1-batch-2/2.2/2.8/2.10/2.12/2.13 + jurisdiction annexes); non-legislation (#8: FR-63, 3.16/3.17, small P3/P4); scratch coverage-refresh sync (#10).

**Open ambiguities / maintainer items surfaced:** the CycloneDX 1.7.1 re-point is applied (#22); the FedRAMP standalone RFC-0006 draft-as-published ingest is directed (in the ref queue); the fast-follow license-schema shape (formal `license:` field vs codify the established omit-both / public_domain / proprietary convention) defaults to codify-the-convention unless redirected; the FedRAMP 2026 evolving-preview re-snapshot cadence is a low-priority currency-watch to establish.

<!-- OVERNIGHT-PR-STUB -->

## Last run closure note: 2026-07-06 overnight (routed by PR #673, the morning-processing PR)

The 2026-07-06 overnight run (resume session `claude/resume-tl5rez`) shipped PRs #667 through #671: TODO 3.21 close (#667) and its 3.21(d) follow-through (#668, `PCI DSS v4` to `v4.0.1`), the TODO 1.9 PreToolUse-hook-firing root-cause record (#669), the TODO 3.15 #637 F4/F6 acronym-linter digit-initial widening (#670), and the TODO 3.15 r4 G-7 QA-report intake runbook subsection (#671). Each shipped with its own DONE entry and per-PR `/validate-pr` + `/retro` rows.

Content routing (morning-processing):
- **Design decisions** to [`design-decisions.md`](design-decisions.md): the PCI DSS "full latest version" citation-form standing preference (recorded in-run under #668); the 3.21(a) bare `C-TPAT` choice was a per-item maintainer decision recorded in [`DONE.md`](DONE.md) #667, not a standing principle. No un-routed design decision remained.
- **Closed work** to [`DONE.md`](DONE.md): routed per-PR during the run (#667 through #671 each added its entry).
- **Queued follow-ups** to [`../TODO.md`](../TODO.md): none new. The 3.21(a) matrix framework-key full-name-consistency observation was deliberately NOT raised as an item absent a signal (recorded here for provenance only).
- **Deferred to the daytime protected-backlog** ([`deferred-protected-changes.md`](deferred-protected-changes.md)): the `/claim-fit` cadence clause (item 5, content-ready) and TODO 3.15 #637 F3 (D5 eighth closure-form, protected-entangled: the "seven closure forms" count in the protected `.claude/CLAUDE.md` must co-update to eight in the same PR). Both cleared in the daytime session that follows this reset.
- **Noise discarded**: the build-progress and files-modified lists.

Maintainer items surfaced from the run: the morning time-decay-on-publications recommendation (delivered); the two-PDF scratch `publications/` assessment (net no ingest, one duplicate, one low-value); the #670 lowercase-tolerant-inline-pattern rejection (surfaced to confirm or reopen); and the TODO 1.9 close-vs-track disposition (held in [`pending-decisions.md`](pending-decisions.md)).
