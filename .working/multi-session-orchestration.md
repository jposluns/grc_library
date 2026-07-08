# Multi-session / multi-worker orchestration runbook

**Version:** 1.1.7\
**Date:** 2026-07-08\
**License:** CC BY-SA 4.0

The operational runbook for running `grc_library` work across multiple sessions and
multiple workers. It executes the design recorded in
[`design-decisions.md`](design-decisions.md) ("Multi-session / multi-worker
orchestration model"); that entry is the authoritative design, this file is the how-to.
Maintainer working state, exempt from corpus audit gates per the `.working/` exemption.

This runbook is the `grc_library`-side companion to the worker-facing `CLAUDE.md` seeded
at the root of the `grc_library_scratch` exchange repo (which any worker instance reads
first). This file is for the **orchestrator**; that file is for the **workers**.

---

## 1. Roles

- **Orchestrator.** One session (one Claude Code instance, or the maintainer driving one)
  that owns `grc_library` write access and is the sole merge authority. It dispatches
  workers, validates-and-QA-checks every delivered change, authors all final prose, runs
  the audit gates, commits, pushes, opens and merges PRs, and runs the per-PR QA
  (`/validate-pr` + `/retro`). There is exactly one orchestrator at a time.
- **Workers.** Producers of **research and candidate diffs**, never of merged changes.
  Two primitives (section 4). Workers hold write to `grc_library_scratch` ONLY, never to
  `grc_library`.

The orchestrator/worker split is the spine of the whole model: parallelism lives at the
worker (research) stage; seriality and authority live at the orchestrator (apply) stage.

---

## 2. The HARD INVARIANT (no-bypass)

**Validation and QA are a gate on APPLY, not a step after merge. Worker or scratch
provenance never reduces the QA a change receives; it only adds a pre-apply screen on top
of the normal pipeline.**

Concretely, every change a worker delivers, before it can land in `grc_library`:
1. The orchestrator re-reads every changed line in the target file at its live state.
2. Re-verifies every citation and control identifier against the reference modules
   (`tools/nist_csf_reference.py`, `tools/ccm_aicm_reference.py`,
   `governance/register-canonical-citations.md`) and the trusted `grc_library_ref/standards/` /
   `grc_library_ref/frameworks/` buckets (NOT `grc_library_ref/publications/`,
   which is untrusted, see section 6).
3. Runs the relevant audit gates on the candidate.
4. ONLY THEN, on a clean result, applies it by committing body + `Version` + `Date` +
   CHANGELOG in ONE commit (preserving gate 40's commit-by-commit check).

A diff that fails validation/QA is **rejected and returned to the worker, never applied**.
Every integrated PR still runs the full post-commit `run_all_audits.sh` + pre-push
`run-pr-time-checks.sh` + CI + formal `/validate-pr` + `/retro`, identically to a
hand-authored PR. **There is no "trusted worker" fast path.** The point of workers is to
parallelize the *research*, not to skip the *verification*.

---

## 3. Model B (partitioned-branch parallelism)

Workers edit verified-disjoint file partitions. The orchestrator owns ALL shared
surfaces and is the sole merge authority. Shared surfaces (never a worker's to touch):
the four version surfaces (per-doc `Version`/`Date`, library CalVer, README version, pack
version), root + detailed CHANGELOG, the generated artefacts (`taxonomy.yml`,
`docs/portal.md`, `docs/maturity-scorecard.md`), `TODO.md`/`DONE.md`, the session
handoff, and the QA ledgers (`validate-sweeps/`, `validate-pr/`, `improvement-log.md`).

Workers DELIVER DIFFS; the orchestrator applies them serially through the validate-then-apply
gate (section 2). Item A can be in the orchestrator's apply queue while worker B is still
researching item C; the parallelism is in research, the seriality is in apply.

### Model-B eligibility checklist (is this work partitionable?)

Partition ONLY when every box is checked:
- [ ] The work decomposes into a set of files that are **verified disjoint** (no two
      workers touch the same file; re-verify disjointness per wave, not once).
- [ ] No shared surface is edited by a worker (versions, CHANGELOG, artefacts, TODO/DONE,
      handoff, QA ledgers are orchestrator-only).
- [ ] The change is not a corpus-wide sweep, rename, or convention migration (those touch
      an unbounded, non-disjoint set, single-orchestrator-session only).
- [ ] The change is not the single-file FR-167 compliance matrix (one file, not
      partitionable; one orchestrator session).

The canonical NON-partitionable cases: corpus-wide sweeps/renames/convention migrations
(e.g. the DD-12 CSF-1.1 migration), the FR-167 matrix, and any gate-wiring PR (four
parallel surfaces that must move together). These stay single-session.

---

## 4. The two worker primitives

Both are supported; pick per the task.

### 4a. In-session subagent fan-out (default, available now)

`Agent` subagents launched inside the orchestrator's own session (the existing
research-assistant discipline, `ai-assistant-workflow-disciplines.md` §1). They share the
orchestrator's container and credentials, produce research/draft diffs, and are bounded by
the research-assistant rules and the worker-brief template
([`worker-brief-template.md`](worker-brief-template.md)). This is the default first move
for partitionable backlog work the orchestrator drives directly, and it is exercised
today (e.g. the FR-167 batch fan-outs, the validation-sweep A/B/C dispatch).

Because in-session subagents share the orchestrator's credentials, they are NOT the
least-privilege primitive; they are a parallelism primitive within one trusted session.

### 4b. Separate-session external-collaborator workers (needs maintainer provisioning)

Another person, using their own Claude Code session under their own account, granted
**read-only** access to `grc_library` and **read/write** access to `grc_library_scratch`
ONLY. This is the primitive the least-privilege / scratch-only-write invariants are
written for: the external worker never holds `grc_library` write credentials; it delivers
diffs via scratch (`inbox/<worker-id>/`), and the orchestrator validates-then-applies.

**Provisioning (maintainer action, not the assistant's):** create/grant a worker account
with the two scopes above. The worker reads the scratch root `CLAUDE.md` (its operating
contract) on first open. Until an account is provisioned, this primitive is documented and
ready but inactive; in-session fan-out (4a) covers partitionable work meanwhile.

---

## 5. Worker coordination and triggering

- **Claims ledger.** A durable `claims-ledger.md` in the scratch repo records each
  worker's partition claim before it starts. A worker reads the ledger at launch, claims
  its disjoint partition, and stays inside it. This is how disjointness is coordinated
  across workers that cannot see each other's sessions.
  On serial delivery merges that conflict on the ledger, the reconciliation rule is a
  timestamp-ordered UNION of the row sets keyed by work-unit id (every claim row from both
  sides is kept, ordered by claim timestamp); a conflict is never resolved by clobbering
  either side's rows.
- **Triggering default: human-on-demand.** The orchestrator (or maintainer) launches a
  wave of workers when there is partitionable work queued. This is the default and the
  safe baseline.
- **Event-driven / scheduled triggering is a capability-gated opt-in, NEVER a poll loop.**
  If (and only if) the harness exposes a wake-on-event primitive (a repo-event
  subscription), event-driven triggering may be enabled as an opt-in. A polling loop to
  "check for new worker deliveries" is forbidden (the same subscribe-over-poll discipline
  as `action-before-explanation-of-inaction.md` and the API-polling guardrails in
  `evidence-grounded-completion.md`). Absent an event primitive, use human-on-demand.

### 5.1 Worker-ready brief staging (the standing input channel; designed 2026-07-03, LIVE since the TODO section-4.4 slice-2/3/5 builds; slice 4 queued)

The standing target state: every TODO item has, in scratch, either a worker-ready brief
at `research/<work-unit-id>/brief.md` or a recorded not-eligible verdict in the coverage
index `research/COVERAGE.md`, so a worker session can pick up any unclaimed eligible item
without waiting on the orchestrator. The full decision record (the maintainer's three
answers plus the accepted design adjustments) is in
[`design-decisions.md`](design-decisions.md) under "Worker-ready brief staging"; the
operational rules:

- **Coverage rule (the TODO-add pairing).** When a TODO item is added, the orchestrator
  authors either its brief or its not-eligible verdict (with the reason) in the same
  close-out sync. Coverage is "every eligible item, verdict for the rest": corpus-wide
  sweeps, renames, convention migrations, and single-indivisible-artefact work are never
  briefed (section 3 eligibility governs). Verdicts are orchestrator-authored; workers
  may draft briefs, and the orchestrator verifies every brief before it lands.
- **Brief shape: pointer-heavy, content-light.** A brief carries the task statement, the
  exact main-repo target paths, the verified-disjoint partition, the `path:line` evidence
  requirement, the deliverable shape (research, not final prose), and a pointer to the
  scratch worker `CLAUDE.md` contract; it carries NO quoted lines, version numbers, or
  counts. The worker's mandatory fresh-read of live `main` carries semantic currency; the
  validate-then-apply gate (section 2) remains the correctness control, so a brief that
  lags a few PRs is safe to pick up.
- **Freshness stamp.** Each brief carries a `Verified-against:` line naming the main-repo
  PR number (or merge SHA) it was verified against plus the UTC date; the PR number makes
  staleness computable as "N PRs behind".
- **State is derived from artefacts, never a status field.** Brief present = ready; a
  `claims-ledger.md` row = claimed (the ledger is the single claim authority); a delivery
  in `inbox/<worker-id>/` = delivered pending apply; the orchestrator removes the WHOLE
  seed directory at DELIVERY time (maintainer-directed 2026-07-04: the entire
  `research/<work-unit-id>/` directory is deleted when the delivery merges, and the
  coverage row re-points at the inbox delivery path, so a consumed seed is never mistaken
  for an open one); the TODO item's own rotation to DONE still happens at the main-repo
  close = closed.
- **TODO is authoritative; briefs are a wipeable derived projection.** TODO wins on any
  conflict; this is what makes whole-backlog staging safe in a wipeable repo.
- **Sync cadence.** The orchestrator syncs the scratch brief tree whenever a main-repo PR
  carries a non-empty TODO delta (add, close, or material change), batched into that PR's
  close-out and shipped via the MCP-PR transport (the persist-to-`main` discipline in
  section 6). Bookkeeping-only PRs generate no sync.
- **Close-out ordering (the same-boundary state-drift guard).** Draft scratch-referencing
  bookkeeping prose (TODO research-state notes, handoff scratch facts, coverage-row
  pointers) AFTER the boundary's scratch merges complete, or re-verify each such line
  against scratch HEAD as the last pre-commit step: a boundary's own worker surge can move
  the state under prose drafted earlier in the same boundary (a brief recorded as staged
  is delivered and its seed removed before the commit assembles), the #624 verifier-caught
  drift.
- **Refresh: targeted-first, mechanical backstop.** The per-PR sync re-stamps the briefs
  it touches. A cross-repo advisory freshness check (target paths still exist on `main`,
  the TODO item still exists, stamp-age report) runs at `/resume` and on the maintainer's
  every-5-to-10-items cadence; it is orchestrator-side, not a CI gate, because neither
  repo's CI can see the other. A full re-verify pass runs only for briefs the check flags
  or whose stamp age exceeds the threshold (initially 15 to 20 PRs behind), plus after any
  structural TODO change (a renumber, a reorganization).
- **Enforcement is layered.** The scratch `validate.py` shape-checks briefs and the
  coverage index (same-repo, mechanical); the main-repo close-out checklist carries the
  pairing line; the `/resume` freshness check catches a missed sync at the next session
  boundary.

This subsection is the LIVE mechanism as of 2026-07-03: slices 1, 2, 3, and 5 of the
TODO section-4.4 build are shipped (the scratch `research/` tree, the coverage index
mapping the whole backlog, the gate shape-checks, the close-out pairing line, the
`/resume` freshness check, and the advisory freshness tool
`tools/audit-brief-freshness.py`). Workers pick up staged briefs per the scratch
`WORKER-ONBOARDING.md`; the ad hoc path remains only as the fallback for an item whose
brief has not yet been synced. Slice 4 (the `/subagent` entry command and the
least-privilege worker account) remains queued.

### 5.2 QA-report intake (the three-layer validation channel)

The brief-staging channel of 5.1 is the INPUT half (research and candidate diffs flowing
IN). This subsection covers the distinct case where a worker (or a separate QA run) returns
a findings REPORT rather than research: a list of claimed defects the orchestrator must act
on. A report is not a finding-set until it has been validated; the orchestrator processes
every such report through three layers before any claimed finding drives a backlog entry or
a fix, because each layer catches a defect class the others cannot:

1. **The worker report (claims).** The raw report is a set of HYPOTHESES, not findings
   (the research-assistant discipline of the pack's `ai-assistant-workflow-disciplines`
   rule, applied to reports as to research). Nothing in it is acted on directly.
2. **An independent validation subagent (the false-positive filter).** A separate subagent,
   blind to the report's reasoning, re-reads the cited source for each claimed finding and
   confirms or refutes it against the live artefact. This is the seam where worker false
   positives and over-classifications are caught (the same apply-time re-verification the
   `trust-recovery-escalation` rule requires before any finding is routed). A claim that
   survives is a candidate finding; a claim that does not is recorded as refuted, not routed.
3. **A transcription-fidelity verifier (the report-to-record seam).** Before the validated
   findings land in the backlog and the QA records, a third check confirms the
   orchestrator's TRANSCRIPTION of each validated finding (its severity, its location, its
   disposition) matches what layer 2 actually validated. This catches drift introduced by
   the orchestrator between validation and recording, a seam neither the worker nor the
   validator can see.

The channel was first exercised on the #626 QA-report intake, where it caught a defect at
each of the three seams (a report-side claim, a classification, and a transcription),
which is the evidence that the three layers are not redundant. Reports never take a
trusted-worker fast path: worker or scratch provenance never reduces the validation a
report receives, exactly as it never reduces the QA a change receives (the HARD INVARIANT
of section 2).

**Standing revisit note (maintainer-decided 2026-07-04).** This subsection is the
runbook-section form of the channel, chosen over a full slash-command skill for now because
the channel had run once. On the channel's NEXT recurrence, assess whether the full-skill
option (a dedicated slash command with its own dispatch and record surfaces, the
`/validate-pr` shape) would serve better than this prose form, and surface that assessment
to the maintainer rather than defaulting either way.

---

## 6. The reference knowledge base (the `grc_library_ref` repo)

The `grc_library_ref` repo is the shared reference knowledge base (buckets at its root),
split by **trust** (see `grc_library_ref/README.md`):
- **`grc_library_ref/standards/`**, accepted standards organized one directory per issuing body (ETSI,
  IEEE, ISO, NIST). **Trusted**: may be referenced as
  authoritative ground truth for citation/mapping work.
- **`grc_library_ref/frameworks/`**, industry / SDO frameworks and informative catalogues, one directory
  per issuer. **Trusted** (one tier below standards in the `grc_library_ref` trust model): citable
  by control/clause for citation/mapping work.
- **`grc_library_ref/legislation/`**, statutes and regulations organized by jurisdiction (with a
  `REGISTER.md` index). **Trusted but version-sensitive**: authoritative for the regime it
  records, but laws are amended and superseded, so confirm the in-force version / date before
  relying on a load-bearing legislative claim.
- **`grc_library_ref/publications/`**, vendor explainers, surveys, threat reports, interpretive
  guidance. **Untrusted by default**: an AI trust-boundary / attack surface (bias, error,
  or prompt-injection / poisoning). A worker or the orchestrator must assess a publication
  for relevance/accuracy AND screen it for poisoning/false info before its content informs
  corpus work; corroborate any load-bearing claim against a `grc_library_ref/standards/`,
  `grc_library_ref/frameworks/`, or `grc_library_ref/legislation/` source or another independent source. A formal publications-assessment
  process is queued (TODO §4.12). Never cite a publication as if it were a standard.

**Screening discipline.** Every publication remains screen-before-use regardless of bucket. The base is the durable, consult-first source for standards and legislation work, and for publications work as screened entries land.

**Standing instruction: reference the `grc_library_ref` base for EVERY task (maintainer-directed
2026-06-27).** Not only the recurring citation / control-code / FR-167-matrix cases: for any
task, before authoring or asserting, check whether the `grc_library_ref` base holds relevant
ground truth (a standard, a legislative regime, or a screened publication) and consult it. The
trust split governs how each bucket is used (standards trusted, legislation trusted but
version-checked, publications screened-not-trusted), but the default is to look, not to rely on
memory. This is the anti-drift / anti-hallucination reason the base exists.

Each `grc_library_ref` bucket has an `originals/` subdirectory for the source binaries (text extracts
are the seeded, AI-readable form; binaries are the provenance / re-extraction source). The
seeded extracts, plus their originals, live on `grc_library_ref` `main`. They
are the durable reference base for citation / control-code / standards work, complementing
the in-repo validator modules ([`tools/ccm_aicm_reference.py`](../tools/ccm_aicm_reference.py),
[`tools/nist_csf_reference.py`](../tools/nist_csf_reference.py)) that encode only codes and
titles: consult the extracts for the full control-specification text rather than re-uploading
binaries or relying on memory.

**Persist changes to `main`.** A change that should outlive the session, a `grc_library_ref`
reference seed, or a durable brief or claims-ledger update in `grc_library_scratch`, is merged to
that repo's `main`, not left on a feature branch. Both are wipeable working state and an ephemeral
container can reclaim an unmerged branch; each repo's `main` is the only durable location, and
`grc_library_ref` `main` is what the next session's `/resume` reference-loading step reads.
Mechanics: reference-base changes persist to `grc_library_ref` via a pull request (the
`gh` CLI, or the GitHub MCP `create_pull_request` + `merge_pull_request` where the MCP
transport is available, e.g. on environments where the local git proxy 403s direct pushes,
the documented [`third-party-issues.md`](third-party-issues.md) 2026-06-25 restriction).
Unlike the wipeable scratch exchange repo (which carries no CI), `grc_library_ref` carries
CI: its [`validate.py`](../../grc_library_ref/tools/validate.py) gate runs on every PR and
push to `main`, so a `grc_library_ref` PR must pass that gate before merge (it is not a bare
fast-forward).

**Standards-validation discipline (validate against the source, not only the derived
encoding).** When `grc_library_ref/standards/` or `grc_library_ref/frameworks/` content informs corpus work (citations, control-code
mappings, the FR-167 matrix batches are the recurring case), the source extracts are the
ground truth and the in-repo validator modules
([`tools/ccm_aicm_reference.py`](../tools/ccm_aicm_reference.py),
[`tools/nist_csf_reference.py`](../tools/nist_csf_reference.py),
[`tools/cobit_iso31000_reference.py`](../tools/cobit_iso31000_reference.py)) are a
*derived encoding* of codes and titles. Two obligations follow, because the citation gates
(48, 49, 54, 58, and 61) enforce only the derived encoding:

1. **Code-set parity (mechanical).** Run
   [`tools/verify-reference-modules.py`](../tools/verify-reference-modules.py) when doing
   standards work or when the `grc_library_ref` base is refreshed: it confirms the modules' code sets
   match the source extracts (CCM v4.1.0, AICM v1.1.0, and NIST CSF 2.0 in both directions;
   COBIT 2019 objectives in both directions plus practice-range closure; ISO 31000:2018 in
   the module-to-source direction only, per the aid's docstring). It is a dev-aid, not a
   CI gate (the `grc_library_ref` source is not present in this repo's CI), and
   it skips cleanly when the `grc_library_ref` base is absent. A drift means the modules (and so the
   gates that trust them) have diverged from the source; reconcile the module to the source.
2. **Semantic-fit against the source title, not the code number (judgment).** A code that
   *exists* (gate-valid) is not necessarily the *right* code: validate a mapping against the
   source control's TITLE and specification text (the `Control Title` / `Control
   Specification` columns of the CSA CSVs; the category name in the CSF text), not by
   inferring meaning from the code number. The recurring failure this prevents: a worker
   reads `SEF-02` and assumes "incident response" when the source title is "Service
   Management Policy and Procedures", or `LOG-08` as "log retention" when it is "Audit Logs
   Sanitization". Code-existence validation is necessary but not sufficient; the source
   title is the semantic check.
3. **CCM and AICM are distinct catalogues; never confuse them.** The CSA CCM v4.1.0 column
   of any mapping takes CCM v4.1 codes only; an AICM v1.1.0 code (the AI-only `MDS` domain
   is the canonical case) does not belong in a CCM-labelled column even though it is a real
   CSA control. Gate 49 enforces this mechanically for the central matrix's CCM column (an
   AICM-only code flags `ccm-aicm-confusion`); the discipline holds for every CCM/AICM
   surface, including per-document framework tables the gate does not yet cover.

The trust split above still governs: `grc_library_ref/standards/` and `grc_library_ref/frameworks/` are trusted
ground truth for these checks; `grc_library_ref/publications/` is screened-not-trusted and is never a
standards source.

**Version currency and the superseded-archival workflow (maintainer-directed 2026-06-28).**
The `grc_library_ref` base is believed-current STORAGE, not a version authority. The authoritative
answer to "is this the current version?" is always the upstream / primary source verified this
turn, never the `grc_library_ref` copy, a stored note, or memory (the pack
[`evidence-grounded-completion`](../dev-security/claude-rules/governance/evidence-grounded-completion.md)
rule's external-version-currency corollary; the project
[`.claude/CLAUDE.md`](../.claude/CLAUDE.md) `## Reference-version currency` SOP). The order
whenever an externally-versioned reference is load-bearing: (1) find what `grc_library_ref` holds via its
index ([`grc_library_ref/INDEX.md`](../../grc_library_ref/INDEX.md), `grc_library_ref/catalogue.yml`,
`grc_library_ref/SECTION-INDEX.md`), not a guessed path (MITRE lives under `grc_library_ref/frameworks/`, not
`grc_library_ref/standards/`); (2) verify the current version upstream this turn; (3) act only after both.

On discovering upstream is newer than `grc_library_ref` holds, the superseded-archival workflow:
1. Download the new version into `grc_library_ref` (egress permitting).
2. Keep the old version but move its files (extracted text plus the original binary) into `grc_library_ref`'s
   retained-version store `grc_library_ref/.superseded/` (bucket-mirrored layout and `REGISTER.md` per `grc_library_ref` `CONTRIBUTING.md`).
3. Update `grc_library_ref/catalogue.yml` and the index docs to the new version; record the upstream-check
   location and the last-verified date (the version-currency register, TODO §1.5).
4. The `grc_library_ref` write goes via a PR (the proxy transport restriction above).

If the new version requires a license or a maintainer download (it cannot be auto-fetched, or
egress is blocked per the DD-10 known issue), **pause and ask the maintainer for direction**; on
no response, apply the graceful-degradation default (defer the current item, record it in
[`pending-decisions.md`](pending-decisions.md), and move on to the next independent item). **Never
write or rely on a superseded version unless the maintainer explicitly authorizes** working from
the older one; otherwise the dependent item waits.

---

## 7. Prep / knowledge-base pre-load discipline

Before a worker wave, the orchestrator prepares the workers' inputs:
- **Triage-then-prep.** Decide which upcoming work is partitionable (section 3 checklist)
  before preparing inputs for it; do not prep non-partitionable work for fan-out.
- **Durable vs volatile.** Durable inputs (worker briefs in `grc_library_scratch`, reference
  extracts in `grc_library_ref`) persist in their repos; volatile inputs (one-shot research
  dumps) are ephemera, wipeable.
- **Rolling buffer.** Keep the apply queue non-empty by preparing the next wave's research
  while the current wave's diffs are being applied (the pipeline-PR-construction discipline),
  but do not over-prep (research drifts as `main` advances between dispatch and apply).
- **Per-wave disjointness re-verification.** Re-verify the partition is disjoint at the
  start of EACH wave (files may have moved/merged since the last wave); disjointness is not
  a one-time property.

---

## 8. Defense in depth (the layers that keep this safe)

1. **Least privilege.** External workers write to scratch only; never hold `grc_library`
   credentials.
2. **No-bypass apply gate** (section 2). Every change is validated-then-applied; provenance
   never reduces QA.
3. **The normal pipeline still runs.** Post-commit `run_all_audits.sh`, pre-push
   `run-pr-time-checks.sh`, CI, `/validate-pr`, `/retro` on every integrated PR.
4. **Trust-split reference base** (section 6). Standards trusted; publications screened.
5. **Worker onboarding contract** (scratch root `CLAUDE.md`). Every worker reads the hard
   invariants + standards before acting.
6. **Bookkeeping-parity gates** (gate 50 and its checks, including the worker-provenance
   marker check; shipped). Honest backstops
   that enforce the PRESENCE of the verification record + provenance attestation, not
   semantic correctness; the primary control remains the orchestrator's apply gate +
   `/validate-pr` + maintainer sign-off.

The layering is the point: no single layer is trusted to be sufficient. A worker could
ignore its `CLAUDE.md`; the apply gate still catches a bad diff. A reference publication
could be poisoned; the trust-split + corroboration catches it. The apply gate could miss
something; CI + `/validate-pr` + the maintainer catch it.

---

## 9. Quick start (orchestrator, in-session fan-out, available today)

1. Confirm the work is partitionable (section 3 checklist). If not, drive it single-session.
2. Build each worker's brief from [`worker-brief-template.md`](worker-brief-template.md)
   plus the PR-specific scope; include the relevant per-PR-class override.
3. Dispatch the workers in parallel (`Agent`), each scoped to its disjoint partition.
4. As each returns, apply the validate-then-apply gate (section 2): re-read, re-verify
   citations/codes against the reference modules + the trusted `ref/` buckets, run the gates, then
   apply body+Version+Date+CHANGELOG in one commit. Reject and return any diff that fails.
5. One PR per coherent unit (the "always split when in doubt" discipline); run the full
   pipeline + `/validate-pr` + `/retro` per PR.

For separate-session external workers (4b), the same loop applies, with the worker
delivering to `inbox/<worker-id>/` in scratch (a `MANIFEST.md` naming each target file,
the proposed change, and the evidence, per the scratch `WORKER-ONBOARDING.md`) and the
orchestrator pulling from there. **Marking convention (the gate-50 check-3 attestation):**
a PR that applies a scratch-inbox delivery carries a `**Worker provenance:**` line in its
detailed-mirror CHANGELOG entry naming the delivery path (normally
`inbox/<worker-id>/MANIFEST.md`), so provenance is traceable from the audit trail to the
delivery; gate 50 validates the marker's shape, and the close-out checklist guards the
unmarked-application residual.

---

## 10. What this runbook does NOT authorize

- No worker merges, ever. Workers deliver diffs; the orchestrator merges.
- No "trusted worker" fast path; the apply gate is unconditional.
- No partitioning of corpus-wide sweeps/renames/migrations or the FR-167 matrix.
- No poll loops for worker coordination; human-on-demand or a real event primitive only.
- No citing `grc_library_ref/publications/` as authoritative; standards only, publications screened.
- No external-worker activation without maintainer-provisioned least-privilege accounts.
