# Design Decisions

Reference log of design decisions made during the project's evolution. Captures decisions that shaped how the corpus is structured, how the audit programme behaves, how slash commands and skills relate, how working state is managed, and which proposals were explicitly dropped with rationale.

This file complements [`DONE.md`](DONE.md) (which records shipped backlog items) and [`../CHANGELOG.md`](../CHANGELOG.md) (which records file-by-file change detail). Design decisions belong here because:

- They are decisions, not items. They don't get "closed" the way a TODO entry does.
- They are findable on demand. Future sessions or future maintainers asking "why does X work this way?" need a single place to look.
- They include decisions that produced no PR (e.g. proposals considered and explicitly dropped) as well as decisions embodied in shipped work.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

The ordering below is loosely thematic rather than chronological. New decisions append to the relevant section.

---

## Multi-session / multi-worker orchestration model (decided across a prior read-only session and 2026-06-24; codification queued)

_Recovered to `main` in PR #316 from the unmerged prior-session commit `da8e051` on `origin/claude/resume-review-h95prg`, where it had been stranded (the session paused before it reached a merged PR). The TODO §4.11 codification track points here as the authoritative source._

These decisions are recorded here ahead of their codification PRs (the runbook, worker-brief override, SOP adjustment, and worker-provenance gate) so they survive on `main` independently of any single session's prompt. The codification track executes them; this entry is the durable source.

**Scratch repo (`grc_library_scratch`, private).** Serves two purposes: (a) the cross-session / worker EXCHANGE channel, and (b) a home for true ephemera (raw tool dumps, in-flight worker research/diffs, a partition claims-ledger). It is NOT a second home for maintainer state. Invariants: scratch is an inbox, not a bypass (content flows scratch -> orchestrator validation/QA -> main); nothing authoritative lives only in scratch; scratch is wipeable; workers may be granted write to scratch ONLY (least-privilege, they never hold main-repo credentials).

**Model B (partitioned-branch parallel).** Workers edit verified-disjoint file partitions; a single orchestrator owns ALL shared surfaces (the four version surfaces, root+detailed CHANGELOG, generated artefacts, TODO/DONE, handoff, QA ledgers) and is the sole merge authority. Workers DELIVER DIFFS, never merge. For each diff the orchestrator FIRST validates and QA-checks it (re-reads every changed line, re-verifies citations and control identifiers, runs the relevant audit gates on the candidate) and ONLY THEN, on a clean result, applies it by committing body+Version+Date+CHANGELOG in ONE commit (preserves gate 40's commit-by-commit check). A diff that fails validation/QA is REJECTED and returned to the worker, never applied. Corpus-wide sweeps/renames/convention migrations and the single-file FR-167 matrix are NOT partitionable, single-session only.

**HARD INVARIANT (no-bypass).** Validation and QA are a GATE ON APPLY, not a post-merge step. Worker/scratch provenance NEVER reduces the QA a change receives, it only ADDS a pre-apply screen ON TOP of the normal pipeline. Every integrated PR still runs the full post-commit `run_all_audits.sh` + pre-push `run-pr-time-checks.sh` + CI + formal `/validate-pr` + `/retro`, identically to a hand-authored PR. There is no "trusted worker" fast path.

**Two worker primitives (BOTH supported; decided 2026-06-24).** The model spans two distinct execution primitives, and the runbook must distinguish them:
1. **In-session subagent fan-out** (the existing research-assistant discipline): `Agent` subagents launched inside the orchestrator's own session. They share the orchestrator's container and credentials, produce research/draft diffs, and are bounded by the existing research-assistant rules. Default first move for partitionable backlog work the orchestrator drives directly.
2. **Separate-session external-collaborator workers**: another person, using their own Claude Code session under their own account, granted read-only access to `grc_library` and read/write access to `grc_library_scratch` ONLY. This is the primitive the least-privilege / scratch-only-write invariants above are written for (the external worker never holds `grc_library` write credentials; they deliver diffs via scratch, and the orchestrator validates-then-applies). This resolves the earlier feasibility question: least-privilege workers are NOT in-session subagents (which share creds) but separate credentialed sessions.

**Scratch-vs-`.working/` test.** "Does a gate read it, will a queued gate read it, or is it the QA/audit record of a corpus change? -> stays in `.working/`. Truly ephemeral with no audit role -> scratch." Grep-confirmed gate-load-bearing `.working/` files that must NOT move to scratch: `changelog-details/CHANGELOG-detailed.md` (D1/D3), `validate-sweeps/history.md` (gate 45 + lint-followup-ageing), `overnight-pr.md` (lint-overnight-file); also `validate-pr/`, `improvement-log.md`, and `DONE.md` are bound to the queued §4.6/§4.10 gates. The `.working/` audit trail STAYS; adopter-irrelevance is already handled by the `.working/` gate exemption + documented deletability.

**Gate-family coherence (decided 2026-06-24, Option A).** The pre-push-runner gate (folding the history-aware gate 40 version-bump-recency and gate 31 date-staleness checks into `tools/run-pr-time-checks.sh`, surfaced by the #314 `/retro`) is kept SEPARATE and built FIRST, because it is orthogonal (local-runner history-awareness, not worker provenance) and protects the upcoming Phase-1 migration. The next-session worker-provenance gate (codification deliverable 4) is to be co-designed with the queued §4.6 (QA-cadence) and §4.10 (rotation) gates as one "post-merge bookkeeping parity" family, and is to be TOLD that the pre-push-runner gate already exists so it extends rather than duplicates it. All such gates are honest backstops (gate-discipline): they enforce the PRESENCE of the verification record and provenance attestation, NOT semantic correctness; the primary control remains the orchestrator's validate-then-apply screen plus `/validate-pr` + maintainer sign-off.

**Bookkeeping-parity gate, pinned design + historical-irregularity map (2026-06-25; design groundwork done, BUILD deferred fresh on a Quality > Speed wind-down).** The build was started this session, then deliberately wound down at a clean boundary (a late-session table-edit slip in the #338 `/retro` row plus the heavy session context were a degradation signal; the maintainer chose wind-down). The design below is pinned so the next session builds it correctly and fast.

- **Scope (maintainer-decided 2026-06-25, "option 1, stage it"):** build the two checks with live surfaces NOW; the worker-provenance check is a present-but-dormant stub that activates once a "worker-delivered" marking convention + the external-collaborator primitive exist (no surface to test against yet, so do not fabricate an attestation format).
- **One linter `tools/lint-bookkeeping-parity.py`** (the next gate number; READ the live count from `tools/run_all_audits.sh` at build time, do not assume it is 50), four-surface wiring + regression fixtures, modelled on `tools/lint-todo-staleness.py` (gate 45, the closest analogue: it also reads `CHANGELOG.md` + the `.working/` history files and lives in both `run_all_audits.sh` and the pre-push runner).
- **Check 1, QA-cadence parity (§4.6):** derive the merged-PR list from `CHANGELOG.md` `## YYYY-MM-DD, Library Version X, PR #N` headers. For each PR N with `INCEPTION <= N < max(PR)`: require a row in `.working/validate-pr/history.md` AND in `.working/improvement-log.md`, UNLESS N is handoff-exempt or carries a maintainer-exception. **Exempt the single highest-numbered PR** (its rows legitimately batch into the next PR per recursion-avoidance). Detect handoff PRs by their explicit validate-pr exemption row (the cell contains `SKIPPED` and/or `handoff-PR exception`); a handoff PR is exempt from BOTH the findings-row and the retro-row requirement. Honor a maintainer-exception/subsumption trailer in the row Summary cell.
- **Check 2, TODO/DONE rotation parity (§4.10):** precision-first / FP-free (the S5 gate-48 precedent). Flag only the unambiguous rotation-failure shapes the change-tracking rule explicitly prohibits: a TODO backlog bullet carrying a self-completion marker (`SHIPPED in #N` / `DONE in #N` / `Status: (completed|done|shipped)` / a `[done]`/`[shipped]`/`[x]` suffix / a strikethrough `~~...~~` on the bullet). Descriptive "batch 1 shipped in #275" inside a still-open item's prose is NOT a flagged shape (no marker), so it does not false-positive.
- **Check 3, worker-provenance (dormant stub):** documents its activation condition (a marking convention + the external-worker primitive); a no-op until then.
- **Handoff-PR exemption MUST be designed in** (the gate must not fail on a session-closing handoff PR's legitimately-absent `/validate-pr`+`/retro` rows).
- **HISTORICAL-IRREGULARITY MAP (verified by a coverage script 2026-06-25; the gate must NOT false-positive on these):**
  - `.working/validate-pr/history.md` rows start at PR **#183**; `.working/improvement-log.md` rows start at PR **#213**. Set `INCEPTION` no earlier than the later of these, and ideally to a recent known-clean frontier; with the gaps below handled, a baseline around **#329** is clean for both files. Confirm at build time by re-running the coverage script.
  - **Handoff PRs MISSING their exemption row** (a real pre-existing bookkeeping gap, NOT a defect to chase): **#300, #322, #334** are session-closing handoff PRs whose `SKIPPED`/`handoff-PR exception` row was never recorded in `validate-pr/history.md`, so the gate cannot auto-detect them as handoffs. Handle via an explicit known-handoff allowlist constant OR an inception baseline above #334. (The detected-handoff set as of this session: #255, #268, #270, #274, #297, #305, #311, #319, #327, #331, #337.)
  - **#328 is a subsumption special-case:** its `/validate-pr`+`/retro` were "NOT run (session force-stopped after merge); SUBSUMED by Sweep 42", recorded as a maintainer-authorised note row in `validate-pr/history.md` (and NO `improvement-log` row). The gate must treat a subsumption-note row as satisfying the requirement (same shape as the maintainer-exception trailer), and must not require a retro row for it.
  - **`improvement-log.md` PR column has a MIXED format:** some rows `338`, others `#333` (leading `#`). The parser must strip an optional leading `#` (`#?(\d+)`). `CHANGELOG.md`'s `PR #N` header and `validate-pr/history.md`'s bare-number PR column are both uniform.
- **Regression fixture** should cover: a missing validate-pr row (fail), a missing retro row (fail), a handoff PR with an exemption row (pass), the highest-PR batch-lag exemption (pass), a subsumption-note row (pass), a clean rotation vs a strikethrough-marked TODO bullet (fail vs pass).

## Overnight unattended run authorizations (decided 2026-06-23, maintainer pre-sleep)

The maintainer authorized an autonomous overnight run through the P1/P2 (then P3/P4)
backlog, with green-CI = merge authority and the hard rule that any `/validate-pr` or
`/validate` finding is fixed immediately before the next planned PR. The formal decisions
resolved before sleep (so the run would not stall on them):

- **New-document criticals (FR-30/31/32/34/71/72)**: author all six unattended, each its
  own PR, mirroring an existing same-type document and anchored to its named external
  standard (GDPR Art 28 / Art 25 / Art 6(1)(f); EDPB Recommendation 01/2020; M&A
  due-diligence; OFAC/sanctions/export-control).
- **FR-70 crypto-asset / blockchain domain (XL)**: deferred to a dedicated session
  (domain-level shaping is the maintainer's; not a fit for unattended work).
- **Cross-document value conflicts**: resolve **stricter-is-safer + evidence**, toward the
  more conservative value where one is clearly safer, and toward the external-standard- or
  already-canonical-internal-source-supported value where one governs; document each choice;
  skip any pick lacking both bases to morning. (Consistent with the locked-criticals pattern:
  TLS 1.3 everywhere, 1h RPO binding, 3y DSAR.)
- **FR-143 supplier-onboarding escalation chain**: the circular `DPO → CISO → Data Protection
  Officer` (supplier-onboarding-security-review:139) becomes **`DPO → CISO → CRO`** (CRO is the
  terminal risk authority in the same matrix's Tier-1 row, so internally consistent).
- **FR-140 adopter starter-set**: **strict nesting with the quickstart 6-artefact "core baseline
  floor" canonical**, Tier-1 (15) ⊇ the 6 (incl. IAM + acceptable-use, which Tier 1 currently
  omits); decision-tree (23) ⊇ 15; README core-reference (~37) ⊇ 23; reconcile the quickstart vs
  startup-roadmap 6th-artefact naming to the quickstart's.
- **FR-73 AI ethics**: introduce a **standing independent AI Ethics Panel**, a subcommittee
  operationally independent of the AI Governance Council's risk/compliance function, with a
  documented challenge mechanism and the ability to escalate dissent.
- **FR-144 breach individual-notification clock**: add an internal floor, "without undue delay,
  and in any event within 72 hours of the high-risk determination", mirroring the GDPR authority
  clock (stricter rule; resolved without a separate maintainer decision).
- **FR-58 inheritance vocabulary**: skipped to morning 2026-06-23 as a taxonomy-design task;
  **resolved 2026-06-25** (maintainer, during the continued overnight run) to apply the canonical
  **3-label scheme** corpus-wide: `library-internal` (cross-references between library documents),
  `template` (adopter-fillable content), and `reference` (external-standard / source content cited,
  not authored), with per-document apply-time verification (surface any document that does not fit
  cleanly). Tracked as the disposition on TODO P1 FR-58.
- **Deepen-all thin baselines** (decided 2026-06-25, maintainer, continued overnight run):
  override the earlier "calibrate first, several are deliberately-thin baselines" guidance; deepen
  ALL of the thin-baseline cluster (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational
  depth rather than treating any as an intentional baseline. Tracked as the disposition on the
  corresponding TODO P2 items.

---

## Working state and `.working/` convention

### `.working/` top-level convention (decided 2026-06-21, PRs #114-#118)

Maintainer working state: not corpus content; not for adopter consumption; exempt from corpus audit gates (in `DEFAULT_EXEMPT_DIRS`); frozen-state archive (cross-references accurate as-of write-time; staleness expected). Top-level dot-prefix matches the existing tooling-dir convention (`.git/`, `.github/`, `.claude/`).

### Canonical activity layout under `.working/<activity>/` (decided PR #118)

Each subdirectory contains:

- `README.md`, static convention info (what the activity is, file format spec, taxonomies, protocols, framework alignment, fork guidance)
- `history.md`, reverse-chronological table (new rows on top); columns: Date | Sweep/Run | Subagents | Findings | Resulting PR | Detail | Summary
- `YYYY-MM-DD-<run-id>.md`, per-run detail file, **only created when findings exist**
- `Subagents` column declares dispatch (Rule 5.6) for every row including zero-finding runs

### Template content vs project-application (decided PR #116)

`governance/` holds template content (specifications, frameworks, registers as document-type templates that adopters cite); `.working/` holds project-specific application of those templates (our log of our sweeps, our verification campaign progress, our branch-protection snapshot).

### Fork-time guidance for `.working/` (decided PR #114)

Adopters cloning the library may delete `.working/` outright or keep it as historical reference. Both fine. Adopters should not extend the upstream `.working/` with their own working state; fresh `.working/` for their own outputs preserves audit trails on both sides.

### Top-level single-file ledgers vs activity subdirectories (decided PRs #131, #134)

`.working/` content takes one of two shapes: activity subdirectories with the canonical `<activity>/{README, history, detail-files}` layout, OR single-file top-level ledgers for content that doesn't fit the activity-subdirectory shape (a growing list, a single-purpose register, a reference log). [`DONE.md`](DONE.md) is the first such ledger (PR #131); [`design-decisions.md`](design-decisions.md) (this file) is the second (PR #134). The Top-level files table in [`README.md`](README.md) enumerates them.

---

## Slash commands, skills, and the validation-sweep / fitness-review surface

### Slash commands vs skill names are independent identifiers (decided PR #115)

Short ergonomic verbs for slash commands (`/validate`, `/fitness`); descriptive names for skills (`validation-sweep`, `library-fitness-review`). The slash command file wraps the skill invocation.

### Subagent dispatch (Rule 5.6) audit trail (decided PR #111)

Every validation-sweep iteration declares which subagents were dispatched in the `Subagents` column of [`validate-sweeps/history.md`](validate-sweeps/history.md). Cannot reconstruct silent skips later.

### Convergence-delta termination (decided PR #115; validation-sweep)

Empty-delta primary stop; patience-plateau secondary (2 consecutive iterations no shrinkage); hard-ceiling 6 iterations.

### Per-iteration detail files: comma form for H2 headings (decided PR #118)

Gate-2 enforces no em-dashes; comma is the canonical form across SKILL.md, slash command, and [`validate-sweeps/README.md`](validate-sweeps/README.md).

### Fitness review persona model: 10 personas (decided PR #120)

The skill dispatches ten persona reviewers in parallel: the original prompt's seven plus three high-value additions.

| # | Persona | Scope | Provenance |
|---|---------|-------|------------|
| 1 | First-time executive reader | Strategic comprehension, purpose, audience, decision points | Original 7 |
| 2 | Security practitioner | Technical security adequacy, OWASP/ASVS alignment, threat-model coverage | Original 7 |
| 3 | GRC practitioner | Governance/risk/compliance discipline, control objectives, evidence paths | Original 7 |
| 4 | Auditor / assurance reviewer | Audit-readiness: testable controls, evidence locations, exception handling | Original 7 |
| 5 | Policy and standards editor | Editorial: naming conventions, requirement-language consistency, terminology | Original 7 |
| 6 | Process owner / operational user | Usability for actual execution: roles, procedures, checklists, decision points | Original 7 |
| 7 | Skeptical reader | Ambiguity, contradictions, gaps, unusable content, "so what?" tests | Original 7 |
| 8 | **Adoption practitioner** | Closest to library's real use case: someone actually setting up a GRC programme from this | Added: the original 7 evaluate the library FROM a perspective; this one tests USING the library. Different lens. |
| 9 | **Privacy / data protection officer** | Privacy domain depth: DPO-specific obligations, jurisdiction-aware controls, data-subject rights | Added: privacy is a large library surface; GRC practitioner covers it only at programme level, not DPO-specific |
| 10 | **Newcomer / onboarding engineer** | Zero-knowledge reader: jargon-free comprehension, onboarding friction | Added: executive persona assumes business literacy; this one is true zero-knowledge |

**Cap at 10**: more personas dilutes each subagent's focus and inflates synthesis. Further additions surface as a follow-up PR.

#### Personas deliberately EXCLUDED from PR #120

Recorded so future "should we add persona X?" questions don't re-litigate from scratch:

- **Security architect**: overlap with security practitioner; the latter's scope was widened to include architecture.
- **AI ethics reviewer**: overlap with GRC practitioner's coverage of AI governance content.
- **Accessibility reviewer**: would warrant a separate "documentation accessibility" review skill; out of fitness-review scope.
- **Legal counsel**: substantive interpretation of jurisdiction-specific law is beyond a quality-review skill.
- **Translation / localization reviewer**: only relevant if the library is being prepared for translation; deferred until that's planned.

### Fitness review severity model (decided PR #120)

SARIF-lite (High / Medium / Low / FYI) with `[critical]` flag inside the High tier for audit-failure / regulatory-exposure / control-failure-class findings. Format: `[high][critical] file:line — description`.

### Fitness review output structure (decided PR #120)

Single combined file per run at [`fitness-reviews/YYYY-MM-DD-rN.md`](fitness-reviews/) (canonical activity layout per PR #118). Eight H2 sections following the original prompt:

1. `## Executive Summary`
2. `## Review Method`
3. `## Page-by-Page Findings`
4. `## Cross-Library Findings`
5. `## Severity Model`
6. `## Recommendations` (priority-grouped)
7. `## Standardization Recommendations`
8. `## Remediation Backlog` (discrete IDs `FR-1`, `FR-2`, ...)

Optional `## Final Assessment` if the prompt's section 9 produces actionable content; otherwise folded into section 1.

### Fitness review cadence triggers (decided PR #120)

Documented in the skill's When-to-Use section:

- After major changes (new domain dir, new document type, ≥3 governance rule additions, major restructure)
- Quarterly minimum (default if no major changes triggered it)
- Pre-publication / pre-external-share
- Manual trigger at any time

### Fitness review scope boundaries (decided PR #120)

Deliberate scope boundaries documenting what the skill is NOT:

- **Not a per-PR gate** (the validation-sweep skill is). Fitness review runs on demand or periodically, not on every PR.
- **Not a security audit** (that's `security-review` skill territory).
- **Not a citation-verification campaign** (that has its own register and worklist process).
- **Not a fact-check of external standards** (per Citation Verification Specification §14, the library does not verify standard content vs. library interpretation).
- **Not enforced by a mechanical gate**; it's a deliverable that informs human prioritization.

### Trust-recovery findings routing: severity-tiered, not all-to-top-priority (decided 2026-06-22, maintainer direction; implementation queued)

The `trust-recovery-escalation.md` rule (pack 1.47.0, signed off 2026-06-22) originally routed **every confirmed finding to the backlog's top-priority tier regardless of severity**. Maintainer revised this 2026-06-22 (this session): trust-recovery findings route **tiered by severity, High[critical] and High to the top-priority tier, Medium and Low to the next-priority tier (this project: P1 and P2 respectively)**, while keeping the core principle (nothing the assistant judges trivial is silently *dropped*; it is routed at the severity-appropriate tier) and the maintainer-sign-off termination. Scope (maintainer: "routing flag only"): the routing **convention** changes across the canonical surface list (kept in lock-step with the TODO codification item), the `trust-recovery-escalation.md` rule **and its `.claude/rules/` mirror**; the `deep-qa-review` SKILL + `/full-qa` command; the `library-fitness-review` SKILL + `/fitness` command; the pack `CLAUDE.md` + project `.claude/CLAUDE.md` rule-description bullets; and the pack README (check/update); the **general TODO P1/P2/P3 structure is unchanged**. Implementation note: the pack rule/SKILLs stay project-agnostic ("top-priority tier" / "next-priority tier"); the project-specific P1/P2 mapping lives in `.claude/CLAUDE.md` + TODO. Queued as the next substantive PR (the 8-surface revision); the `/fitness` routing-flag amendment (TODO trust-recovery codification item) folds into it.

---

## CHANGELOG and TODO/DONE conventions

### PR sequencing principle (durable, restated PRs #114-#130)

"More PRs, keep each one clean." Favor small focused PRs over bundled ones. Validation sweeps run between substantive PRs.

### CHANGELOG split convention (decided PR #125)

Root [`../CHANGELOG.md`](../CHANGELOG.md) keeps the lead paragraph only; structured sections + verification evidence + discipline observations move to [`changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md). Going forward, every PR writes BOTH. PR-time gate (`check-changelog-on-pr.py`) enforces dual-entry. The general `.working/` audit exemption is preserved for everything else.

### Two-file CHANGELOG dual-entry enforcement (decided PR #125)

The PR-time delta gate `check-changelog-on-pr.py` requires BOTH the root CHANGELOG and the detailed mirror to be in the diff (lock-step). Modifying one without the other fails the gate. The opt-out `Changelog: <reason>` trailer in any commit message satisfies the gate regardless of split.

### Session-state snapshot as-of-last-refresh (decided PR #127, mechanically enforced via gate 45 in PR #128)

The resume snapshot (the version snapshot and the sweep cursor) is intentionally frozen at session-pause time. (It was originally the "Session resume metadata" subsection of [`../TODO.md`](../TODO.md); relocated to the "Resume cursor" section of [`session-handoff.md`](session-handoff.md) in PR #413 so `TODO.md` stays purely forward-looking, with gate 45's sweep-cursor check re-pointed to read the cursor from the handoff.) The version snapshot and the sweep-cursor each drift forward as the project advances; that drift is expected and not a defect. Gate 45 (TODO staleness audit) catches the harder shapes (a queued PR already merged, checked in `TODO.md`; a sweep cursor behind history, checked in `session-handoff.md`) mechanically; other drift is informational.

### TODO/DONE rotation discipline (decided PR #131)

TODO is forward-looking only. When a PR closes a TODO item, the item is removed from TODO in the same PR and an entry is added to [`DONE.md`](DONE.md) (the closed-TODO ledger). Both edits live in the same commit so reviewers see the rotation in one place. Historical state ("PRs completed this session", "Key design decisions made this session") has no place in TODO; it belongs in DONE or in this design-decisions file.

### After-merge list-next-5-PRs discipline (decided PR #131)

When a PR merges, the next action is to consult TODO's forward-looking section and list the upcoming five planned PRs in the chat. New items surfaced during the just-finished work are added to TODO before the list is published. Surfacing the queue lets the maintainer redirect early.

---

## Audit programme architecture

### Subagent dispatch and silent-skip prevention (decided PR #111)

See "Subagent dispatch (Rule 5.6) audit trail" above. Recording for cross-reference: Rule 5.6 was the seed of the broader "every action driven by inference must record what was validated" principle that later became the `validate-inference-before-action.md` pack rule.

### Wrapper-script-plus-corpus-runner discipline (decided PR #128)

Local PR-time discipline requires running BOTH [`../tools/run_all_audits.sh`](../tools/run_all_audits.sh) (corpus gates) AND [`../tools/run-pr-time-checks.sh`](../tools/run-pr-time-checks.sh) (PR-only delta gates D1 + D2 + D3, plus the history-aware gates 45 + 40 + 31) before push. The two runners together cover every gate the CI workflow runs. Structural fix for the PR-time-delta-gate omission failure mode that surfaced in PR #127's first push. (Gates 40 and 31 were folded into the pre-push runner per the "Gate-family coherence (Option A)" decision above; they also run in `run_all_audits.sh`, but re-invoking them pre-push makes the runner a complete commit-graph-aware guard for large multi-commit or file-move changes such as the governance Phase-1 migration.)

### Decorative gate-count narrations forbidden in prose (decided PR #130)

Phrases like `"the N-gate audit programme"`, `"all N gates"`, `"gates 1-N"` are removed from corpus prose. The spec §6 inventory in [`../governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) is the canonical single source for both the gate list and the current count; downstream prose points to §6 instead of repeating the count. Gate 39 (cross-file gate-count consistency audit) retained as the defence against new decorations creeping back in.

### Gate 48 (CCM/AICM citation-accuracy) is token-scoped; the bare-domain-code class is gate-blind (DD-overnight-1, surfaced Sweep 36, recorded 2026-06-24)

Gate 48 checks `<DOMAIN>-<NN>` control tokens and `| CODE | title |` rows against the fair-use CCM v4.1.0 / AICM v1.1.0 reference, but it is structurally blind to **bare domain-code and domain-name mentions** in prose, framework-coverage family lists, the glossary, and domain-by-domain crosswalks (a row reading `Infrastructure and Virtualization Security`, or a list naming `IVS`, carries no `<DOMAIN>-<NN>` token for the gate to parse). The #298/#301 reconciliation and the Sweep 36/37 residuals both lived in this blind spot. The durable mechanical fix is queued as TODO §4.5 **S5** (extend gate 48 to flag bare known-bad CCM domain codes in a CCM/CSA context, with care to avoid false positives on `.NET`, currency `AUD`, corpus-internal `MODEL-GOV`/`AI-GOV`, and "government" prose). Until S5 ships, the orchestrator's unfiltered standalone-token grep (the #301 retro discipline) is the working control.

### R1 working-state relocation closed "won't-move" (decided 2026-06-24, maintainer)

The XS "Working-state relocation" item to move `tools/sweep-preflight-exemptions.json` into `.working/validate-sweeps/` was closed **won't-move**. The file is the pre-flight scanner's exemption config and the scanner ([`../tools/sweep-preflight-scanner.py`](../tools/sweep-preflight-scanner.py)) lives in `tools/`; co-locating the config with the tool is correct for adopters (who take the pack and its tools), and moving it into `.working/` would either bake a `.working/` path into the two distributable pack SKILLs that reference it (`validation-sweep`, `validation-sweep-pr-scoped`) or require genericizing their prose. Keeping it in `tools/` avoids both. The original "co-locate with the validate-sweeps activity" premise did not weigh the distributable-pack coupling. (R2, the citation-verification cluster relocation, remains deferred in TODO with a related convention-conflict noted.)

### The #376 paired-surface mechanical check: extend gate 50 (not a new gate), and only the mechanizable half (design scoped 2026-06-27, build deferred)

The recurring "update-one-of-a-pair" failure (a change updates one field of a paired structure and drops the sibling) split into two halves with different mechanizability, so the "extend gate 50 vs new gate" fork the #376 retro left open is resolved as follows:

- **Mechanizable half (a), the metadata-Version-to-version-history-row pair.** The #372 miss (the pack [`README.md`](../dev-security/claude-rules/README.md) metadata `Version` moved to `1.49.18` with no matching `## Version history` row) is a pure presence-of-a-paired-record check: for every file that carries both a metadata `Version` field and a `## Version history` table, the metadata `Version` value must appear as a row in that table. This is exactly gate 50's ([`lint-bookkeeping-parity.py`](../tools/lint-bookkeeping-parity.py)) family (its checks 1-2 enforce presence of paired bookkeeping records, not their semantic correctness), so it lands as **gate 50 check 4**, NOT a new numbered gate. Decisive consequences: no gate-count change (54 stays 54; extending an existing gate's internal checks is the gate-48 "two checks to four checks" precedent, #308/#309), no four-surface re-wiring (gate 50 is already wired), so the count-bump ripple does not fire. The build is a single `version_history_parity_findings()` function plus a regression fixture plus the gate-50 §6 spec-narrative note; precision-first and FP-free per the gate-48 S5 / gate-50 check-2 precedent (flag only a metadata `Version` with no matching history row; tolerate history rows with no current metadata match, which are the normal historical rows).

- **Non-mechanizable half (b), the coded-value-to-description-prose pair.** The #371/#374 miss (a control-code migration `RC.IM` to `ID.IM` left the word "recovery" in the paired description cell) is semantic prose drift, not a presence check, and is NOT mechanizable (a gate cannot tell whether a description still echoes the old code's meaning). It stays a convention: the CLAUDE.md close-out-checklist paired-surface bullet (instance b) plus worker-brief DO rail 8 already carry it.

**Built in PR #444** (2026-06-28) as gate 50 check 4 (`version_history_parity_findings()` plus four regression tests plus the §6 narrative note), per the resolved design above: precision-first, FP-free, no new numbered gate, no gate-count ripple. The original deferral note (the gate-logic precision is degradation-sensitive and best authored on fresh context) is retained for provenance.

---

## Language and style

### Canadian-first language convention (decided PR #133)

The library uses **Canadian English first, Commonwealth (UK / Australian) English second, other dialects last**. Canadian English shares the `-ize` / `-ization` orthography with American English (the Oxford convention adopted in Canadian usage), so the [`../tools/lint-language.py`](../tools/lint-language.py) `-ize` rule is the Canadian-orthography manifestation of the convention, not a generic American mandate. Where Canadian English has no opinion, Commonwealth forms are preferred; where neither has an opinion, other dialects' usage is acceptable. Em-dashes (`—`) and en-dashes (`–`) are forbidden in prose regardless of dialect; use commas, colons, or parentheses.

### FR-167 compliance-matrix authoring conventions (2026-06-27, routed from the overnight run)

The compliance-alignment matrix ([`../compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md)) is authored against the trusted scratch `ref/standards/` source extracts. Two conventions emerged across the FR-167 batches and the 2026-06-27 trust-recovery pass:

- **The trade-column (CTPAT / PIP / BASC v6 / WCO SAFE / AEO-S) convention varies by matrix section.** Governance-domain rows are mostly N/A across the five customs and trade columns; Security-domain rows populate them via the ICT-security and AEO-S requirement-area lens. Before authoring a domain's trade columns, read that domain's existing rows and follow their convention rather than defaulting to N/A. The 2026-06-27 maintainer redirect populated three governance rows that carry incidental BASC and WCO content (continuous-assurance, metrics-monitoring, data-retention-schedule), so "governance is always N/A" is a default, not a rule; populate where the document's own body or alignment table grounds the mapping (no fabricated chapter or clause numbers).
- **Validate every code's semantic fit against the source control TITLE, not just its existence.** The "valid code, wrong control" class (a real catalogue code that is the wrong control for the row) is gate-blind: gates 48, 49, and 54 check existence and catalogue membership, never semantic fit. The 2026-06-27 trust-recovery `/full-qa` found eight such defects in the matrix and seven source documents whose own framework tables carried the same class. The durable guard is the worker-brief standards-validation rails (9 and 10) plus apply-time title-checking against the source extracts, not a mechanical gate (semantic fit is impractical to gate).

---

## Decisions explicitly dropped

Items considered and explicitly not pursued, with rationale. Recorded so the reasoning is preserved if the question recurs.

### Strict Related-Documents reciprocity dropped

Original plan: add a linter enforcing that if document A's Related Documents lists B, then B's Related Documents lists A. Empirical run found 1,269 non-reciprocal references across 266 of 280 active documents.

The library's actual convention is **asymmetric** Related Documents: each document lists "what this document consumes / relates to from its own perspective", not "the complete bidirectional graph". This is a reasonable, content-author-friendly convention.

The underlying concern (catching half-updated cross-references during refactors) is already covered by [`../tools/lint-links.py`](../tools/lint-links.py) (broken-link detection).

Decision: dropped. Not pursued in narrower form (doctype-pair rules) because the marginal value over [`../tools/lint-links.py`](../tools/lint-links.py) does not justify the maintenance cost of a curated rule set with many exemptions.

### Cross-document numerical coherence shipped as scaffold

Original plan in the audit-roadmap: a linter that flags numerical drift on canonical-term thresholds (RTO, RPO, P1/P2/P3/P4 acknowledgement times, retention periods) across documents.

Empirical analysis found that incident-severity terminology (P1/P2/P3/P4) legitimately carries different numeric values per SLA dimension: acknowledgement time, resolution time, escalation interval, notification time. A naive "same Pn = same value" check would false-positive on legitimate per-dimension variation.

Decision: ship as scaffold (regex framework with unit normalization and aggregation), with the term set widened incrementally as empirical data warranted. The scaffold's progression:

- Phase 23.26 added P1/P2/P3 acknowledgement-time patterns as scaffolding (each requires a Pn-prefix-with-explicit-acknowledgement-time prose shape on the same line; the patterns match 0 documents on the current corpus by design, since the corpus carries Pn-acknowledgement times in tabular form rather than the strict prose shape).
- Phase 23.35 added the GDPR breach-notification-hours pattern after empirical confirmation that 8 or more documents reference the statutory 72-hour deadline and all agree on the value.

The current scaffold tracks four terms (P1/P2/P3 acknowledgement-time patterns plus GDPR-breach-notification-hours); see `TERM_PATTERNS` in [`../tools/lint-cross-doc-numbers.py`](../tools/lint-cross-doc-numbers.py) for the live set. The linter's docstring documents why RTO, RPO, retention periods, P4 acknowledgement, NIS 2 reporting windows, and DORA reporting windows are deliberately NOT curated (each is either context-dependent, has multiple legitimate per-deadline sub-patterns that need separate regex, or appears too few times in the corpus to justify a curated pattern).

Honest scope management is preferred over either (a) silently producing false positives or (b) defining the term set without sufficient operational data. The maintainer revisits the term set when corpus evolution introduces a new prose shape that warrants pattern coverage.

### Phase-completion gating requires the full audit-programme sweep

A prior bundled commit's pre-merge audit pass omitted several gates and consequently merged five audit-gate violations (filename/doctype prefix mismatch on the bundle index, 15 em-dash language findings, one broken intra-repo link, one mislabelled hallucinated framework version, one unresolved intra-document reference). All were caught and corrected in the immediately following cleanup.

Decision: phase-completion gating requires the full audit-programme sweep ([`../tools/run_all_audits.sh`](../tools/run_all_audits.sh); see [`../governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6 for the canonical inventory) to pass locally before any push. The pre-commit hook configuration operationalizes this in git itself.

The convention is: at each commit, the maintainer (or AI verifier) runs every gate in a single batch (not a selective subset) and only proceeds to push when zero violations remain.

### No verification of standard content versus library interpretation

When the AI Security Tooling Landscape Register was created, it asserted capability claims for each project. The Citation Verification Specification §14 explicitly excludes "verification of standard content versus the library's interpretation of it" from the methodology scope.

Decision: verification covers metadata (existence, version, publication date, supersedence, ID format) and integrity anchors (commit SHA, Wayback snapshot URL). It does NOT verify that the library's prose interpretation of a project's capabilities is accurate. That would require the library to engage in interpretation disputes with project authors; the methodology stays at the citation-metadata layer.

### FR-104: Decision-tree per-regulation context not pursued (decided 2026-06-22)

Fitness review 2026-06-22 r1 surfaced FR-104 (medium severity): the decision-tree in [`docs/decision-tree.md`](../docs/decision-tree.md) §1.4 lists seven regulations as bullet-list choices without per-regulation context describing what each covers. The finding proposed adding a one-line descriptor per regulation so a newcomer choosing among them has framing.

Decision: not pursued. The decision tree's audience is a reader who is already navigating toward a specific regulation; the descriptor-per-regulation would inflate the section without changing the navigation outcome (the reader still chooses the regulation that applies to them). The per-regulation framing lives in each regulation's dedicated annex, which is where a newcomer who needs the context will land regardless.

### FR-130: Decision-tree portal entry-point reorder not pursued (decided 2026-06-22)

Fitness review 2026-06-22 r1 surfaced FR-130 (medium severity): [`docs/decision-tree.md`](../docs/decision-tree.md) lines 107-120 list the README as the first entry point and the portal as item 8 of 8, which one persona felt delayed encounter with the portal navigational surface. The finding proposed moving the portal to item 1.

Decision: not pursued. The README is the canonical first-encounter surface for adopters cloning the library; the decision tree's ordering reflects that intent. The portal is a secondary navigational artefact useful once a reader has the corpus open, and its position at item 8 reflects discovery sequencing (read the README, then explore via the portal). Reordering would invert the intent. PR #200 explicitly preserved the existing pattern when closing the adjacent FR-132.

---

## Session-concurrency safety: a session-state lease + git cross-check (design captured 2026-06-26; BUILD deferred to a later session)

_Captured at the maintainer's request during the `claude/session-state-safety-vzsj19` session. The maintainer's concern: "if I make a mistake and resume a session when you are still running in another, there could be corruption." The maintainer proposed a `.working/session-state.md` tracking main-session and worker states, plus a freshness signal ("a time stamp on each PR or something") to identify stale sessions. This entry records the recommended design so the next session implements it; the build is intentionally NOT done in the capturing session (the maintainer asked to "consider the best option and add your thoughts to the decisions file for the next resume")._

### The problem

The handoff / resume model assumes strictly **serial** sessions: a session ends by landing a green session-closing handoff PR on `main`, and the next session's `/resume` rebuilds state from `main`. Nothing today detects or prevents a **concurrent** session. If the maintainer starts a second session (sends `/resume`, or opens a fresh container) while a prior session is still live, two orchestrators run at once. The realistic failure modes:

- **Shared-`main`-surface clobbering.** Both sessions eventually merge to `main` and both write the shared state surfaces: `session-handoff.md`, `TODO.md`, `DONE.md`, `validate-sweeps/history.md`, the detailed CHANGELOG mirror, and the four version surfaces (library CalVer + README Version + per-document Version/Date). Two merges racing these produce lost edits, conflicting refreshes, and **version-monotonicity collisions** (two sessions both bumping CalVer to the same value, which gate 40 / the monotonicity audit would then flag, but only after the damage).
- **Feature-branch isolation is partial, not total.** Each session gets a uniquely-suffixed branch (this session: `claude/session-state-safety-vzsj19`), so direct git-object collisions on the branches themselves are unlikely. The corruption surface is the shared state and the version registers that *both* sessions write *through their merges*, not the branch commits.
- **A "paused" session is not an idle session.** The stop-hook auto-commits AND pushes uncommitted work at every turn-end (see the handoff's "Known environment behaviours"). A session the maintainer believes is parked can still push on its next turn, so "I'll just resume; the other one is sitting still" is unsafe.

### Options considered

- **(A) Explicit lease file only (`.working/session-state.md`), the maintainer's suggestion.** The active orchestrator writes a lease (session id = branch name, status, a heartbeat UTC stamp, the active worker dispatches and their partitions); `/resume` reads it first and holds if it shows an un-released session. Pro: explicit, human-readable, and it naturally carries the "main-session AND worker states" the maintainer asked for. Con: the lease lives on the feature branch until merged, so a brand-new session reading `main` sees only the *last-merged* lease, not the in-flight session's branch-local heartbeat. On its own it cannot see a session that started after the last merge.
- **(B) Git-state cross-check only.** On `/resume`, `git fetch`, enumerate remote `claude/*` branches ahead of `main`, and read their newest commit timestamps; a recent unmerged branch implies a live session. Pro: authoritative *external* timestamps (commit times are not something the assistant has to remember to write), and it sees across sessions because the stop-hook pushes branches to `origin`. Con: heuristic (an abandoned-weeks-ago branch is a false positive), and it carries no worker state.
- **(C) Both: lease file as the declared state, git cross-check as the external verification. RECOMMENDED.** This is the `validate-inference-before-action` pattern applied to "is another session live": the lease is the *claim*, the live remote git state is the *observation* that confirms or refutes it. The lease (refreshed onto `main` at each PR close-out, like the handoff) records the last-merged session's close and the worker dispatches; `/resume` ALSO fetches and inspects live remote `claude/*` branches for recent unmerged activity. A concurrent session is detected when EITHER the lease is not `released` with a fresh heartbeat, OR a remote `claude/*` branch other than the one being resumed has a commit inside the staleness window. The git check catches the crash case (a session that died before writing or releasing its lease); the lease carries the clean-close bookkeeping and the worker state.

### Recommended mechanism (C), concretely

- **New file `.working/session-state.md`** (gate-exempt under the `.working/` exemption). Fields: `Active-session:` (branch name or `none`), `Status:` (`active` | `winding-down` | `released`), `Last-heartbeat-UTC:` (a `date -u` stamp, the authoritative-clock note below), `Current-task:` (one line), `Worker-dispatches:` (list of worker-id, partition, status, cross-referencing the scratch `claims-ledger.md`).
- **Acquire** at session start, right after the `/resume` orientation: write `Active-session: <this branch>`, `Status: active`, heartbeat = `date -u`.
- **Refresh** the heartbeat at each PR close-out (cheap; folds into the existing handoff-refresh batch). Optionally each turn (the stop-hook persists it for free).
- **Release** in the session-closing handoff PR: `Status: released`, `Active-session: none`. A cleanly-closed session therefore leaves a `released` lease on `main`.
- **`/resume` new step 0 (before reading the handoff):**
  1. `git fetch origin`, read `.working/session-state.md` from `main`.
  2. If `Status` is not `released` AND `Last-heartbeat-UTC` is within the staleness window: a session is likely live. HOLD and surface ("branch X looks active, last heartbeat T, N minutes ago; confirm it is closed before I proceed"). Do not proceed without explicit maintainer confirmation.
  3. Cross-check git: list `origin/claude/*` branches ahead of `main`; for any branch other than the one being resumed, read its newest commit time. A commit inside the staleness window triggers the same HOLD + surface (this is the crash-case net: the lease may never have been written or released).
  4. If the lease is `released` (or stale beyond the window) AND no recent unmerged sibling branch exists: safe. Record acquisition and continue the normal resume.

### The freshness / "stale session" signal (the maintainer's "timestamp on each PR")

Two-tier, and the maintainer's instinct is correct: **git commit / PR timestamps are the authoritative external clock**; the lease heartbeat is the finer-grained in-session clock.

- Use **commit time** (git) as the source of truth on the cross-check path: it cannot drift from reality and does not depend on the assistant remembering to write it.
- Use the **heartbeat** for the declared-state path (the lease).
- The **staleness window** is the threshold that separates "live" from "abandoned". On a not-`released` lease whose heartbeat is OLDER than the window, surface it as an abandoned-session takeover decision ("prior session appears abandoned, heartbeat N old, branch unmerged; take over? (recommended) / investigate / leave it") rather than auto-proceeding or auto-blocking.

### Honest limitations (state plainly, do not oversell)

- This is an **advisory interlock, not a hard mutex.** No atomic cross-container lock primitive is available, so two sessions started within the same heartbeat window, before either writes its lease, can still both proceed. The mechanism shrinks the vulnerable window from "always" to "both start within the staleness window AND the git cross-check misses", which covers the realistic accidental-double-resume the maintainer is worried about. It does not defeat a determined simultaneous launch.
- The lease on `main` only reflects the *last-merged* session; the **git cross-check is the part that sees an in-flight session** (its branch is on `origin` because the stop-hook pushes). The two halves of (C) are not redundant; each covers the other's blind spot.
- A mechanical **well-formedness gate** (a lint mirroring `lint-overnight-file`, failing on a malformed or missing `session-state.md`) is worth adding to keep the file honest, but it CANNOT enforce the interlock itself (CI runs per-branch and cannot see across concurrent sessions); it only guards the file's shape.

### Build plan for the implementing session (NOT the capturing one)

1. Create `.working/session-state.md` with the field schema and an initial `released` / `Active-session: none` stub.
2. Add `/resume` **step 0** (the lock check above) to [`.claude/commands/resume.md`](../.claude/commands/resume.md).
3. Wire the acquire / refresh / release writes into the session lifecycle and document them in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)'s `## Session migration and PR close-out checklist` section and the handoff's "How to resume".
4. Decide and (if chosen) build the well-formedness gate, four-surface-wired with a regression fixture, per the standard new-gate recipe. If built, it pairs with the §4.6 / §4.10 / §4.17 bookkeeping-parity gate family.
5. Integrate worker state: `session-state.md`'s `Worker-dispatches` summarizes the current orchestrator's launched workers and partitions, cross-referencing the scratch `claims-ledger.md`, so a resuming orchestrator knows what is mid-flight.

### Open sub-decisions for the maintainer (confirm at the implementing session)

- **Staleness window value** (proposed default: 60 minutes; long enough not to false-positive on a session that is thinking or waiting on CI, short enough that a truly-dead session does not block for hours).
- **Hard-block vs advisory-warn** on a fresh-heartbeat `active` lease (proposed: advisory HOLD requiring explicit maintainer confirmation, because the assistant cannot truly know the other session is dead, and a hard block would strand the maintainer if a session crashed without releasing).
- **Whether to add the well-formedness gate now or defer** it as a follow-up.
