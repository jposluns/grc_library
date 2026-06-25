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
- 2026-06-25: NEXT: Sweep 42 `/validate` (mandated loop-break control), then the
  §4.11 multi-session capability + gate family, then FR-167, then decided items.

## Surfaced ambiguities / morning-review items

- **Scratch binary seed deferred** (infra): git-proxy 403s scratch writes after the
  first push; maintainer will re-upload the reference binaries tomorrow. Text indexes
  are already up; the binary tree is staged locally. No decision needed; flagged for
  awareness.
