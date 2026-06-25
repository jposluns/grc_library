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
- **Cross-document value conflicts**: resolve **stricter-is-safer + evidence** — toward the
  more conservative value where one is clearly safer, and toward the external-standard- or
  already-canonical-internal-source-supported value where one governs; document each choice;
  skip any pick lacking both bases to morning. (Consistent with the locked-criticals pattern:
  TLS 1.3 everywhere, 1h RPO binding, 3y DSAR.)
- **FR-143 supplier-onboarding escalation chain**: the circular `DPO → CISO → Data Protection
  Officer` (supplier-onboarding-security-review:139) becomes **`DPO → CISO → CRO`** (CRO is the
  terminal risk authority in the same matrix's Tier-1 row, so internally consistent).
- **FR-140 adopter starter-set**: **strict nesting with the quickstart 6-artefact "core baseline
  floor" canonical** — Tier-1 (15) ⊇ the 6 (incl. IAM + acceptable-use, which Tier 1 currently
  omits); decision-tree (23) ⊇ 15; README core-reference (~37) ⊇ 23; reconcile the quickstart vs
  startup-roadmap 6th-artefact naming to the quickstart's.
- **FR-73 AI ethics**: introduce a **standing independent AI Ethics Panel** — a subcommittee
  operationally independent of the AI Governance Council's risk/compliance function, with a
  documented challenge mechanism and the ability to escalate dissent.
- **FR-144 breach individual-notification clock**: add an internal floor — "without undue delay,
  and in any event within 72 hours of the high-risk determination" — mirroring the GDPR authority
  clock (stricter rule; resolved without a separate maintainer decision).
- **FR-58 inheritance vocabulary**: **skipped to morning** as a taxonomy-design task that
  propagates across many documents and needs maintainer discussion.

---

## Working state and `.working/` convention

### `.working/` top-level convention (decided 2026-06-21, PRs #114-#118)

Maintainer working state: not corpus content; not for adopter consumption; exempt from corpus audit gates (in `DEFAULT_EXEMPT_DIRS`); frozen-state archive (cross-references accurate as-of write-time; staleness expected). Top-level dot-prefix matches the existing tooling-dir convention (`.git/`, `.github/`, `.claude/`).

### Canonical activity layout under `.working/<activity>/` (decided PR #118)

Each subdirectory contains:

- `README.md` — static convention info (what the activity is, file format spec, taxonomies, protocols, framework alignment, fork guidance)
- `history.md` — reverse-chronological table (new rows on top); columns: Date | Sweep/Run | Subagents | Findings | Resulting PR | Detail | Summary
- `YYYY-MM-DD-<run-id>.md` — per-run detail file, **only created when findings exist**
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

The `trust-recovery-escalation.md` rule (pack 1.47.0, signed off 2026-06-22) originally routed **every confirmed finding to the backlog's top-priority tier regardless of severity**. Maintainer revised this 2026-06-22 (this session): trust-recovery findings route **tiered by severity — High[critical] and High to the top-priority tier, Medium and Low to the next-priority tier (this project: P1 and P2 respectively)** — while keeping the core principle (nothing the assistant judges trivial is silently *dropped*; it is routed at the severity-appropriate tier) and the maintainer-sign-off termination. Scope (maintainer: "routing flag only"): the routing **convention** changes across the canonical surface list (kept in lock-step with the TODO codification item) — the `trust-recovery-escalation.md` rule **and its `.claude/rules/` mirror**; the `deep-qa-review` SKILL + `/full-qa` command; the `library-fitness-review` SKILL + `/fitness` command; the pack `CLAUDE.md` + project `.claude/CLAUDE.md` rule-description bullets; and the pack README (check/update); the **general TODO P1/P2/P3 structure is unchanged**. Implementation note: the pack rule/SKILLs stay project-agnostic ("top-priority tier" / "next-priority tier"); the project-specific P1/P2 mapping lives in `.claude/CLAUDE.md` + TODO. Queued as the next substantive PR (the 8-surface revision); the `/fitness` routing-flag amendment (TODO trust-recovery codification item) folds into it.

---

## CHANGELOG and TODO/DONE conventions

### PR sequencing principle (durable, restated PRs #114-#130)

"More PRs, keep each one clean." Favor small focused PRs over bundled ones. Validation sweeps run between substantive PRs.

### CHANGELOG split convention (decided PR #125)

Root [`../CHANGELOG.md`](../CHANGELOG.md) keeps the lead paragraph only; structured sections + verification evidence + discipline observations move to [`changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md). Going forward, every PR writes BOTH. PR-time gate (`check-changelog-on-pr.py`) enforces dual-entry. The general `.working/` audit exemption is preserved for everything else.

### Two-file CHANGELOG dual-entry enforcement (decided PR #125)

The PR-time delta gate `check-changelog-on-pr.py` requires BOTH the root CHANGELOG and the detailed mirror to be in the diff (lock-step). Modifying one without the other fails the gate. The opt-out `Changelog: <reason>` trailer in any commit message satisfies the gate regardless of split.

### Session-state snapshot as-of-last-refresh (decided PR #127, mechanically enforced via gate 45 in PR #128)

The "Session resume metadata" subsection in [`../TODO.md`](../TODO.md) is intentionally frozen at session-pause time. The version snapshot and the sweep-cursor each drift forward as the project advances; that drift is expected and not a defect. Gate 45 (TODO staleness audit) catches the harder shapes (queued PR already merged; sweep cursor behind history) mechanically; other drift is informational.

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

---

## Language and style

### Canadian-first language convention (decided PR #133)

The library uses **Canadian English first, Commonwealth (UK / Australian) English second, other dialects last**. Canadian English shares the `-ize` / `-ization` orthography with American English (the Oxford convention adopted in Canadian usage), so the [`../tools/lint-language.py`](../tools/lint-language.py) `-ize` rule is the Canadian-orthography manifestation of the convention, not a generic American mandate. Where Canadian English has no opinion, Commonwealth forms are preferred; where neither has an opinion, other dialects' usage is acceptable. Em-dashes (`—`) and en-dashes (`–`) are forbidden in prose regardless of dialect; use commas, colons, or parentheses.

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

### FR-104 — Decision-tree per-regulation context not pursued (decided 2026-06-22)

Fitness review 2026-06-22 r1 surfaced FR-104 (medium severity): the decision-tree in [`docs/decision-tree.md`](../docs/decision-tree.md) §1.4 lists seven regulations as bullet-list choices without per-regulation context describing what each covers. The finding proposed adding a one-line descriptor per regulation so a newcomer choosing among them has framing.

Decision: not pursued. The decision tree's audience is a reader who is already navigating toward a specific regulation; the descriptor-per-regulation would inflate the section without changing the navigation outcome (the reader still chooses the regulation that applies to them). The per-regulation framing lives in each regulation's dedicated annex, which is where a newcomer who needs the context will land regardless.

### FR-130 — Decision-tree portal entry-point reorder not pursued (decided 2026-06-22)

Fitness review 2026-06-22 r1 surfaced FR-130 (medium severity): [`docs/decision-tree.md`](../docs/decision-tree.md) lines 107-120 list the README as the first entry point and the portal as item 8 of 8, which one persona felt delayed encounter with the portal navigational surface. The finding proposed moving the portal to item 1.

Decision: not pursued. The README is the canonical first-encounter surface for adopters cloning the library; the decision tree's ordering reflects that intent. The portal is a secondary navigational artefact useful once a reader has the corpus open, and its position at item 8 reflects discovery sequencing (read the README, then explore via the portal). Reordering would invert the intent. PR #200 explicitly preserved the existing pattern when closing the adjacent FR-132.
