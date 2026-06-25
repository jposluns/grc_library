<!-- OVERNIGHT-PR-IN-FLIGHT -->
# Overnight PR

**Status:** in-flight

A maintainer-authorized autonomous overnight session is active (started 2026-06-25,
maintainer pre-sleep). This file carries its authorization scope, the decision set
resolved before sleep, the running order, build progress, and surfaced ambiguities.
The next-morning processing routes this content to the durable ledgers and resets the
file to `stub` (gate 46 enforces the lifecycle).

## Authorization scope (maintainer, 2026-06-25 pre-sleep)

Maintainer is asleep. Autonomous run authorized with green-CI = merge authority,
per-PR `/validate-pr` + `/retro` (no skip, no abbreviation), and the standing
overnight conflict rule (stricter-is-safer + evidence; document each choice; skip to
morning anything lacking both bases). All file-mutating tracks below are
maintainer-authorized to run unattended ("All authorized, run top-down").

Top priority, maintainer's words: "I would like the multi-session capabilities
developed so that we can start using them tomorrow. Once that's done, begin with
FR-167 and then highest priority items that you are able to complete without asking
me questions or needing my permission to write a file."

## Decision set (resolved via two AskUserQuestion rounds, 2026-06-25)

Recorded here durably so the run survives a mid-night compaction.

1. **Running order**: (1) Sweep 42 `/validate` (loop-break control for handoff #327);
   (2) §4.11 multi-session capability IN FULL; (3) FR-167 with project-gov-separation
   Phase 1 PULLED AHEAD of remaining FR-167 batches; (4) highest-priority autonomous
   items.
2. **Multi-session gate scope**: build the WHOLE bookkeeping-parity gate family
   tonight — pre-push-runner gate FIRST (it protects the pulled-ahead Phase-1
   migration), then worker-provenance + §4.6 QA-cadence + §4.10 rotation gates,
   co-designed as one family, each told the pre-push-runner gate already exists.
3. **External-collaborator worker**: codify BOTH worker primitives; seed scratch and
   make in-session fan-out usable now; the separate-session external-collaborator
   path is fully documented and ready for the maintainer to provision a worker
   account tomorrow (read `grc_library` / write `grc_library_scratch` only) to
   activate. (Scratch WRITE access from this environment is confirmed.)
4. **FR-58 inheritance vocabulary**: apply the canonical 3-label scheme corpus-wide —
   `library-internal` (cross-references between library docs), `template`
   (adopter-fillable content), `reference` (external-standard/source content cited,
   not authored) — with per-doc apply-time verification; surface any doc that does not
   fit cleanly.
5. **Write scope**: ALL authorized to run top-down — project-gov Phase-1 migration,
   FR-30/31/32/34/71/72 net-new docs, deepen-all thin baselines (FR-15/24/63/74/154),
   FR-73 (independent ethics panel), FR-145 (keep both + crosswalk), FR-167 batches.
6. **Carried pre-decisions** (from `design-decisions.md` "Overnight unattended run
   authorizations" 2026-06-23, still in force): FR-30/31/32/34/71/72 author all six
   (one PR each, mirror same-type docs, anchored to named external standards); FR-70
   crypto/blockchain domain DEFERRED to a dedicated session; FR-73 = standing
   independent AI Ethics Panel; FR-144 internal-clock floor already resolved;
   FR-143 escalation chain DPO→CISO→CRO.
7. **Q3 (earlier round)**: deepen ALL the thin-baseline cluster (override the
   "calibrate, several are deliberate baselines" note); Q2: project-gov separation
   Phase 1 pulled ahead of remaining FR-167 batches.

## Owed bookkeeping (fold into the first substantive PR)

- Record a #328 `/validate-pr` history row noting Sweep 42 subsumption (no per-PR ledger gap).
- Apply approved DD-12 decision: broaden DD-12 in TODO from `PR.IP`-only to ALL
  CSF-1.1 carriers (`PR.IP`, `ID.SC`, `ID.BE`, `RS.RP`, `DE.DP`, `PR.AC`, `PR.PT`, ...);
  queue a new item to extend gate 49 (or a sibling) to validate framework codes in
  per-document framework-reference tables, not only the central matrix. Known carriers:
  `risk/standard-third-party-and-supply-chain-risk.md`:230 (`ID.SC`);
  `operations/procedure-security-monitoring-and-alert-management.md`:333/336/337 (`RS.RP`/`DE.DP`).
- Refresh `session-handoff.md` to post-#328.

## Reference files supplied (authoritative sources, de-risk no-fabrication)

NIST CSWP.29 (CSF 2.0), CCM/CAIQ v4.1 bundle, AICM v1.1, AI Security Checklist —
maintainer-attached uploads. Use at apply-time for the work that needs them
(FR-167 supply-chain CCM/ISO/NIST cells; DD-12 CSF migration; AI-domain content).

## Build progress (running log; newest at bottom)

- 2026-06-25: session started; state verified (main @ 6d3d23c / #328, 49/49 green,
  Library 2026.06.307 / pack 1.49.9 / README 1.9.178, clone unshallowed); this file
  set to in-flight.
- 2026-06-25: scratch `ref/` seeding (maintainer-requested, with a second batch of
  reference uploads). Assessed all 9 supplied references + the 4 earlier ones; built a
  categorized `ref/` tree (standards-frameworks / csa-ccm-aicm / ai-security /
  threat-intel-reports) with a calibrated `ref/README.md` (citable-primary vs
  orientation-only). Seeded the TEXT indexes via the GitHub MCP API (root README,
  ref/README, .gitignore). The reference BINARIES (~34 MB) could NOT be pushed: the
  git proxy 403s all writes to `grc_library_scratch` after the first (see
  third-party-issues.md 2026-06-25). Maintainer directed: defer, they re-upload
  tomorrow. Binary tree is built+committed locally, ready to push when the restriction
  clears. `grc_library` writes are unaffected (overnight branch pushed fine).
- 2026-06-25: **Sweep 42 `/validate` complete** (loop-break control for #327; covers
  #323-#328). Mechanical baseline 49/49. Full 3-subagent dispatch (A/B/C). Findings: ONE
  genuine in-window low (`guardrail-review/SKILL.md`:93 "forty-eight"->"forty-nine", gate
  count word-form lag from #325; gate-39-blind) FIXED on this branch; ONE low note
  (`session-handoff.md`:84 stale `/resume` step ref after #328 renumber; .working/
  frozen-state, fix at handoff refresh). Subagent C 0 findings (gate 49 four-surface
  parity, NIST ref 22-cat clean, linter+regression pass). 17-cell NIST remap verified
  semantically sound. Matrix CSF-1.1 clean. No asserted-expectations contradiction (no
  escalation). All 9 pre-flight candidates dismissed. OWED: Sweep 42 history row + detail
  file (batch into first PR).
- 2026-06-25: **scratch ref/ knowledge base** (maintainer iterated the design live across
  several messages). DELIVERED via MCP text path (git proxy blocks scratch writes):
  (1) text-extracted all 13 supplied binaries (pymupdf/openpyxl) into AI-readable form
  (PDF->md, XLSX->per-sheet CSV with greppable Control IDs); (2) two-bucket TRUST model
  per maintainer direction: `ref/standards/` (NIST CSF, CSA CCM/AICM/CAIQ; trusted,
  cite-as-authoritative) vs `ref/publications/` (vendor explainers, surveys, threat
  reports, CSA interpretive guidance; UNTRUSTED by default, assess + screen for poisoning
  before use); (3) `originals/` manifest dirs per bucket for the pending binaries;
  (4) per-directory READMEs (files + origin + trust class); (5) **worker onboarding
  `CLAUDE.md`** at scratch root (operating model, hard invariants, standards, canonical-
  pack pointers — the maintainer-flagged worker-safety requirement). Framework + worker
  CLAUDE.md SEEDED (scratch commits aa4ac10/864988c/1f0add8/470b093). The ~2.84MB text
  extracts are STAGED locally (committed in the session scratch-seed repo), pending a
  working scratch-write path or maintainer binary re-upload (offered).
- 2026-06-25: **PR #329 MERGED** (Sweep 42 close-out + resume bookkeeping; green CI,
  squash `86b9d81`). Its `/validate-pr` ran: 1 in-window Medium (orchestrator wrote
  `RS.RP`→`RC.RP` from memory in the DD-12 broaden; reference says `RS.MA`),
  apply-time-verified + fixed; 1 low note accepted. `/retro` logged the
  control-code-from-memory orchestrator-prose pattern + proposed improvement. Rows + fix
  batched into PR-2.
- 2026-06-25: **PR-2 / #330 (multi-session codification, part 1)** assembled: new runbook
  `.working/multi-session-orchestration.md` (1.0.0); worker-brief-template 1.1.0->1.2.0
  (Model-B worker section + corrected stale `PR.IP` guidance now that gate 49 enforces CSF
  2.0 in the matrix); carries the #329 QA rows + the DD-12 `RS.RP`->`RS.MA` fix. Library
  308->309, README 1.9.180. About to run verification + push + PR.
- 2026-06-25: **#330 MERGED** (green CI, squash `93567f4`); its `/validate-pr` returned
  **0 findings** (PR.IP correction complete on both surfaces, CSF codes verified real,
  runbook consistent); `/retro` clean (positive counter-instance).
- 2026-06-25: **SESSION WIND-DOWN.** Deliberate close at a clean boundary (very long
  context; the remaining §4.11 gate family + FR-167 are high-complexity/high-stakes and
  better fresh, per Quality>Speed + session-migration discipline). Session-closing handoff
  **PR #331** lands this overnight session's working-state on `main` (handoff full refresh
  + batched #330 QA rows). **overnight-pr.md STAYS in-flight**: the overnight authorization
  CONTINUES into the next session for the queued remainder. The next `/resume` runs Sweep 43
  (loop-break control for #331), then continues the queue: PR-3 SOP → gate family
  (pre-push-runner first) → project-gov-sep Phase 1 → FR-167 batch 4 → decided items.
- 2026-06-25: **Overnight outcome**: scratch exchange repo set up (framework + worker
  CLAUDE.md seeded; extracts staged for maintainer re-upload); Sweep 42 done; #329 + #330
  merged + QA'd; multi-session capability core (runbook + worker brief) delivered. NOT yet
  done (queued): the §4.11 SOP + gate family, FR-167, the decided content items. Maintainer
  tomorrow: re-upload scratch binaries; provision the external-worker account.
- 2026-06-25: **NEXT RESUME SESSION started** (continued from handoff #334 via `/resume`).
  State verified: main/feature @ `9d36f41` (#334), 49/49 green (matches green-at-`33c770b`),
  Library 2026.06.313 / pack 1.49.11 / README 1.9.184, clone unshallowed. §4.11 parts 1-3
  (runbook #330, light SOP #332, pre-push-runner gate #333) confirmed DONE. **Resume
  clarification batch answered (2026-06-25):** (1) **standing authority CONFIRMED operative
  for this session** — continue unattended, green-CI=merge, per-PR `/validate-pr`+`/retro`,
  stricter-is-safer+evidence on conflicts, recorded running order (project-gov Phase 1 →
  §4.11 worker-provenance gate family → FR-167 → decided content); (2) **maintainer will
  re-attach the CCM/AICM/NIST references this session**, so FR-167 batch 4 STAYS in the
  running order (verified at session start that scratch `ref/` still holds only manifest
  stubs; reach batch 4 after Phase 1 + the gate family, by which point the refs should be
  available; verify presence before authoring any batch-4 cell). About to run the mandatory
  **Sweep 44** (loop-break `/validate` control for handoff #334, covering the #332/#333
  deltas).
- 2026-06-25: **FR-167 references RE-ATTACHED by maintainer** (Q2 answer in action):
  CCM/CAIQ v4.1 Bundle, AICM v1.1, NIST CSWP.29 (CSF 2.0). Extracted to greppable text in
  the session scratchpad `fr167-refs/` (`CCM_v4_1.txt`, `AICM_v1_1.txt`,
  `NIST_CSWP_29_CSF2.0.txt`; originals + full bundle PDFs alongside). These are the
  authoritative apply-time sources for FR-167 batch 4 (supply-chain) CCM/ISO/NIST cells and
  the DD-12 CSF-1.1→2.0 migration. (Scratchpad is session-durable; if a later session needs
  them, re-attach. The scratch-repo binary seed remains blocked by the git-proxy 403 and is
  separate maintainer/infra work.) **FR-167 batch 4 is unblocked.**
- 2026-06-25: **Maintainer task queued**: add **Philip Veilleux** (`@menoche`,
  https://github.com/menoche) to the AUTHORS.md "Acknowledged contributors" list; bundle
  into the first resume-bookkeeping PR (NOT the project-gov Phase 1 migration PR, which stays
  surgically scoped). Versioned doc → bump AUTHORS.md Version + Date in the same commit.
- 2026-06-25: **#335 MERGED** (resume bookkeeping; green CI, squash `1c01e80`). AUTHORS.md
  +Philip Veilleux (`1.1.2`→`1.1.3`); batched the clean Sweep 44 row. `/validate-pr` **0
  findings**; `/retro` clean (caught + corrected my own apply-time CHANGELOG overclaim before
  commit). Library `2026.06.313`→`2026.06.314`.
- 2026-06-25: **#336 MERGED** — the major milestone: **project-governance separation Phase 1**
  (green CI, squash `b09375d`). Executed the §8.1 citation-verification cluster migration:
  `git mv` 6 artefacts `governance/`→ new audited `.project-governance/` dir + README index;
  severed 7 corpus→project citations (one-way dependency rule); re-pointed 2 path-targeted
  linters + added `.project-governance` to 9 content linters (§6.3 full-audit, resolving the
  §6.3-vs-§7.3 spec gap stricter+evidenced, surfaced to maintainer); generators exclude it by
  include-list design; taxonomy/portal/scorecard regenerated. Built via the research-assistant
  discipline (read-only research subagent → exhaustive migration map → orchestrator apply-time
  verification → both runners). `/validate-pr` **0 error/0 warning/1 cosmetic note** (§4
  one-way-dependency invariant confirmed clean by direct grep + Subagent A); `/retro` logged
  the spec-gap + the cosmetic CHANGELOG-lead-wording note. Library `2026.06.314`→`2026.06.315`.
  Closes R2.
- 2026-06-25: **SESSION WIND-DOWN.** Deliberate close at a clean boundary on Quality > Speed:
  the major Phase-1 migration (deferred by two prior sessions for freshness) is shipped green,
  and the remaining queue (§4.11 worker-provenance gate family, FR-167's 8 batches, decided
  content) is a large series better served fresh in a heavy-context session. Session-closing
  handoff **PR #337** lands this session's working-state on `main` (handoff full refresh +
  batched #336 QA rows). **overnight-pr.md STAYS in-flight**: the overnight authorization
  CONTINUES into the next session for the queued remainder. The next `/resume` runs **Sweep 45**
  (loop-break control for #337, over the #335/#336 deltas), then continues the queue:
  §4.11 worker-provenance gate → FR-167 batch 4 → decided content. **Maintainer items**:
  re-attach FR-167 refs (ephemeral scratchpad) or seed scratch; provision external-worker
  account; review the §6.3-vs-§7.3 spec-gap decision.

- 2026-06-25: **NEXT RESUME SESSION started** (continued from handoff #339 via `/resume`).
  State verified: main/feature @ `203ca06` (#339), 49/49 green (descendant of green-at-`bac5ddb`),
  Library 2026.06.318 / pack 1.49.11 / README 1.9.189, clone unshallowed; no drift. **Resume
  clarification batch answered (2026-06-25):** (1) **standing unattended authority CONFIRMED
  operative for this session** — green-CI=merge, per-PR `/validate-pr`+`/retro` (no abbreviation),
  stricter-is-safer+evidence on conflicts, skip-to-morning anything lacking both bases;
  (2) **running order this session = FR-167 batch 4 FIRST** (after the mandatory Sweep 46), to use
  the freshly re-attached but session-ephemeral references (NIST CSWP.29, CCM/CAIQ v4.1, AICM v1.1)
  before they expire (they expired unused the prior two sessions), THEN the §4.11 worker-provenance
  / bookkeeping-parity gate (needs no references), then the decided content items. About to run the
  mandatory **Sweep 46** (loop-break `/validate` control for handoff #339, covering the #338 delta).

## Surfaced ambiguities / morning-review items

- **Scratch binary seed deferred** (infra): git-proxy 403s scratch writes after the
  first push; maintainer will re-upload the reference binaries tomorrow. Text indexes
  are already up; the binary tree is staged locally. No decision needed; flagged for
  awareness.
