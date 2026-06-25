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

## Surfaced ambiguities / morning-review items

- **Scratch binary seed deferred** (infra): git-proxy 403s scratch writes after the
  first push; maintainer will re-upload the reference binaries tomorrow. Text indexes
  are already up; the binary tree is staged locally. No decision needed; flagged for
  awareness.
