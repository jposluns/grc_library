# Overnight PR

**Status:** in-flight

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

## Current run (2026-07-03Z)

**Authorization:** maintainer-confirmed 2026-07-03T00:1xZ ("Confirming that you are in overnight mode as of the end of the current PR"), effective at the #589 merge. Scope: the full answered queue per the 2026-07-02 decision rounds (DPO role-separation sweep; coverage-gaps batch 3; the ad-hoc fit pass; FR-48 section-1.1 interleaved with section-3.15 machinery; the P2 net-new gap-fills 2.9/2.5/2.4/2.1/2.2 under the HA harness; the scratch SR wave + section-3.7 lease + 3.8 + 3.10). Full per-PR QA cadence; green CI = merge authority; authorial/irreversible/protected-tree decisions defer to [`pending-decisions.md`](pending-decisions.md).

**Progress:** PR #590 MERGED (7831284; its sweep's M-1, the sec-IR authority residual, fixed in #591). PR #591 (in flight): the coverage-gaps third batch (eight re-grades + the Brazil OEA row addition, every grade on a named batch-2 precedent) + the #590 QA trio. Original #590 note: PR #590 (in flight at first write): the DPO role-separation sweep (10 documents, 75 edits) + the section-2.13 PIA acceptance-authority fix (DPO advises, EC accepts) + the #589 QA trio. Four proceeded canonical/stricter-safe defaults logged in pending-decisions for morning confirm-or-redirect (charter interim-block reframe; breach-notification authority to the DPO per the charter's own Article 38(3) row; the PIA internal pathway rewired to Executive Committee acceptance with ERC oversight; the five core privacy-document Owner fields reconciled to the document index's Data Protection Officer).

---

Prior-run closure note: the 2026-07-02 overnight run (PRs #553 through #570, eighteen merges) ended when the maintainer awoke mid-M1 and switched the session to **daytime-unattended mode** by direct message; per the overnight protocol's awake-early exception this file was transitioned `in-flight` -> `stub` directly once its content was routed. The per-PR progress lives in `CHANGELOG.md` / [`DONE.md`](DONE.md) / git history; the run's authorization scope and the mode transition are preserved in this file's git history and summarized in [`session-handoff.md`](session-handoff.md); the three post-run maintainer directives (keep-tracked, mode-exit priority ordering, model tiering) are recorded in [`design-decisions.md`](design-decisions.md); the forward queue is in [`../TODO.md`](../TODO.md) and [`session-handoff.md`](session-handoff.md). One overnight authorization was SUPERSEDED before execution: the "EPUBs: untrack going forward and queue history-purge instructions" direction was replaced by the maintainer's 2026-07-02 morning decision to KEEP the scratch-repo ISO and EPUB files tracked (private-forever repository, exposure controls, watermarks always scrubbed); the supersession is recorded in [`pending-decisions.md`](pending-decisions.md) and the decision record in [`design-decisions.md`](design-decisions.md). The three still-standing morning items (the advisory-directive codification PR, the C3/C4/C5 proceeded stricter-safe defaults awaiting confirm-or-redirect, and the two stale June branches) remain open in `pending-decisions.md` and the session handoff.
