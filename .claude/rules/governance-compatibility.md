# GRC governance compatibility

AIQT rules at a3ff734ca855e4363f340eca52fbd87272c51854 are the portable
baseline. GRC retains the additional obligations below. Before the named
activity, read and apply its full procedure in .claude/references/governance/;
these are required procedures, not optional background. Do not import that
whole directory at startup. Existing project authorization, stricter QA,
changelog, operating-mode and no-exception policies remain in force.

Precedence for this migration: platform and maintainer instructions apply;
GRC's explicit local requirements supplement the pin. The current GRC
no-manufactured-winddown policy and AIQT continue-by-default supersede the old
session-depth/fresh-session triggers. The local attended-to-unattended timeout
exception remains; ending unattended mode requires the operator.
AIQT change-tracking-ext does not remove GRC's per-PR changelog obligation.
AIQT verifier-diversity does not reduce GRC's triple-family standard or authorize
a new fallback. Gate failures have no local exception-register bypass.

1. Gate failure: apply gate-discipline.md and its diagnose skill. Never weaken,
   bypass, suppress, or regenerate in CI to manufacture a pass. Fix or descope.
2. Change/PR/close-out: apply change-tracking.md and the PR-lifecycle playbook.
   Every PR has its appropriate terse/substantive entry; retain detailed records,
   linked touched files, verification and phase context, plain-language public
   summaries, coupled archive/roll-up, DONE by permanent original ID, forward-only
   TODO, next-N from the private Up-next queue, and the overnight Status lifecycle.
   Preserve coupled Version/Date bumps and monotonic version history.
3. Completion/state/reference claim: apply evidence-grounded-completion.md.
   Enumerate, read, quote, contradict, distinguish mechanical from semantic
   coverage, and disclose gaps. Use the authoritative index for inventories and
   current upstream authority for currency claims. Attempt acquisition of a
   missing load-bearing source before routing around it. Accepted-unverified
   claims require durable tracking. Verify an external link's destination and
   supporting content before including it. Prefer event subscriptions; required
   polling is authenticated, bounded and fail-loud, preserving error bodies.
4. Ambiguity: apply clarify-before-acting.md. Retrieve findable facts before
   asking; use documented reversible defaults. Surface material authorial choices
   and scope expansion before acting, with self-contained options, recommendation
   and consequences; honor standing authorization and the project's plan workflow.
5. Generation/branch/version work: apply artefact-and-branch-discipline.md.
   Edit source, regenerate locally, commit both, check drift in CI. Preserve
   version bumps through conflicts and use the documented protected-branch flow.
6. Inaction explanation: apply action-before-explanation-of-inaction.md.
   Attempt an authorized safe/reversible action before saying it cannot proceed;
   for destructive actions name the unattempted action and obtain required
   authorization. Decision ambiguity is resolved first. Quote actual failures.
7. Inference/guard/mutation/retry work: apply validate-inference-before-action.md.
   Keep observation separate from decisions; maintain reality fixtures and mutate
   the observer as well as the predicate. Calibrate mutation runs with positive
   and negative controls, prove baseline behavior, and mark non-semantic mutations
   INVALID. After two same-class failures, write the error, mechanism, fix and
   byte-level difference before another attempt. Use absolute execution targets.
8. Worker/QA/PR work: apply ai-assistant-workflow-disciplines.md.
   Workers research; the orchestrator verifies every surviving claim at apply time
   and authors the result. Log corrections and update/version the worker brief.
   Verify disjoint partitions and reserve shared surfaces; research in parallel,
   apply serially, integrate on green before the next apply. During CI, prepare
   read-only. Commit every reviewed artefact and companion before dispatch.
   Validate, fix and re-verify findings; cap rounds at six, nine only unattended
   while converging, with an unchanged finding stopping its loop. Log overrides
   with a revert path and surface them at the attended boundary.
   QA completes only with the formal run, all findings fixed/routed, positives
   reverified, a history row including zero findings, and documented deferrals.
   Reactive trust recovery adds human sign-off; proactive assessment does not.
9. Trust recovery: apply trust-recovery-escalation.md only on maintainer invocation.
   Run forensic then persona passes over the named window, using a full clone for
   history. Verify/dedupe findings and route every confirmed finding by severity.
   Hold for explicit combined-set sign-off, including a zero-finding result,
   before remediation, lessons or other substantive work.
10. Priority checkpoints: apply project-integrity.md. Emit the AIQT checkpoint at
    task/plan, persistence, completion and tradeoff boundaries, at least per PR,
    with a concrete self-acknowledgement. Never buy progress by reducing assurance.
11. Counterproductive instruction: apply surface-counterproductive-instructions.md.
    Interpret charitably; surface material downside once with concrete options.
    Respect an informed authorized override and avoid repeated or trivial asks.
12. Sensitive change: apply high-assurance-verification.md and /high-assurance
    when correctness is gate-blind, scale delicate and escaped-error cost high,
    or when directed. Preserve research, negative-signal screening, independent
    adversarial lenses, invariant checks, scripted dry-run/idempotent apply and
    re-parse, guard-first sequencing, and the persistent resume-visible register.
13. Resume/mode/close: apply session-lifecycle.md with the supersessions above.
    Reconcile the bounded handoff, acquire/refresh/release the lease, honor
    decision-timeout reversibility, and obtain delivered/dispositioned QA before
    closing. Reissue stalled read-only QA, consume late results as cross-checks,
    and preserve the documented closing-QA compensating control. Prequeue bounded
    research at the closing merge SHA and record dispatches as pending work.
14. Plan-bending decision: apply decision-classification-before-enacting.md.
    Write ACT/ASK/BLOCKED before enactment; use only the closed blocker vocabulary
    retained below, ask reachable authorities, and prove whole-set exhaustion.
15. Plan initiation: apply express-authorization-before-execution.md. A conditional
    go covers only the presently authorized step; await the required confirmation
    before the gated step. An adjacent or unnamed endorsement does not widen scope.

The following project overlays are retained from 9985b75f. Their old statements
that GRC authors all portable AIQT and guardrails is only an export target are
superseded for the imported AIQT snapshot: upstream owns those pinned bytes;
GRC owns local compatibility and its legacy publication sources. New portable
changes go through upstream review and a subsequent explicit re-pin. The old
source/adapter discipline still applies to GRC-authored publication material.

Maintainer decisions D1-D3 (2026-10-02 12:27Z) govern this cutover.
The AIQT snapshot is separately licensed Apache-2.0; its LICENSE and NOTICE
remain verbatim. No legacy procedure retires. In every retained procedure,
the worker-brief template is the operational store root worker-brief-template.md
(current store root /opt/grc/private), superseding the archived private/.working path.

## action-before-explanation-of-inaction.md

- Project instantiation: the CLAUDE.md `PR activity subscription discipline`
  (subscribe plus a 60-second fallback timer; the background-task check SOP).

## ai-assistant-workflow-disciplines.md

- **In-session subagent fan-out is DISABLED in this project** by the
  `block-orchestrator-self-qa.py` PreToolUse hook (matcher `Task|Agent|Workflow|SendMessage`): the in-session-subagent
  primitive in §2 above is a general adopter primitive, but `grc_library` uses ONLY the
  separate-session (orch-verify) primitive, via the global `orch-verify` dispatcher, because an in-session
  subagent bills the scarce orchestrator account. Consuming the once-only actor-created sentinel is
  the only in-session PATH to authorize such a dispatch, but the actor can create that sentinel with
  one `touch`, so it is a deliberate speed bump plus an audit record, not a security boundary.
  Project wiring only; the pack body keeps in-session fan-out for adopters.

- Worker-hallucination tracking artefact: `hallucination-metrics`.
- Worker-brief template: `/opt/grc/private/worker-brief-template.md`.
- Verifier-override register: `grc_library_private/.working/verifier-overrides.md` (surfaced at `/orch`).
- Exchange channel and runbook: `multi-session-orchestration` (the former `grc_library_scratch` exchange
  channel is RETIRED, maintainer-directed 2026-09-23; worker results return synchronously via orch-verify and
  guardrail seeds go to guardrails via `inbox-send`).
- Maintainer D2 (2026-10-02): upstream owns the pinned AIQT bytes; GRC owns compatibility and legacy publication procedures. Portable AIQT changes require upstream review and an explicit re-pin.
- Gate-37 instantiation: until the root `guardrails/` cutover, gate 37 preserves
  byte parity between the portable pack source and the project-local rule bodies
  (after stripping sanctioned local overlays). The migration EXTENDS that hard
  local check with the deterministic coding-adapter generator's `--check` mode and
  a publication manifest; it does not replace it with a network-dependent
  upstream-drift probe.

## artefact-and-branch-discipline.md

- Generated artefacts here: `tools/alignment_citation_ids.json` (regenerate via
  `tools/build-alignment-citation-registry.py`; its `--check` needs `grc_library_ref`, and gate 96
  re-verifies the committed counts and digests at load), `taxonomy.yml`, `narrative.yml`, `docs/portal.md`,
  `docs/maturity-scorecard.md`, `governance/relationship-model.generated.json`,
  the `## Number allocation` block in `TODO.md`, the section 7.1 publisher table in
  `governance/specification-citation-verification.md` (generated from its `json citation-publishers`
  block), the generated table of `.project-governance/register-historical-citation-exceptions.md`
  (from its `.toml` data file via `tools/build-historical-citation-exceptions.py`; gate 6 refuses drift), and every compiler-owned
  corpus-management output (the CLAUDE.md generated-artefacts block, the two prose rules and index in `.claude/rules/corpus-management/`, and the on-demand bodies in `.claude/references/corpus-management/`)
  (regenerate via `tools/build-taxonomy.py`,
  `tools/build-narrative-registry.py`, `tools/build-portal.py`,
  `tools/build-relationship-model.py`, `tools/build-todo-number-allocation.py`,
  `tools/build-corpus-management.py`, and `tools/build-citation-publishers.py`;
  gates 33, 85, 34, 93, 91, 99, and 102 run the `--check` forms).
- Protected-branch force-push procedure and `refs/preservation/` convention: the
  project CLAUDE.md Boundaries section.

## change-tracking.md

- Detailed mirror (Option C two-tier, maintainer-decided 2026-09-07): the LIVE mirror is `changelog-details/CHANGELOG-detailed.md` in the operational STORE, resolved by `lint_common.resolve_working` (store-first; by default `<repo-parent>/private/`), co-committed with the other working records (DONE, QA rows, bypass log). It is NOT at `grc_library_private/.working/changelog-details/` (that path is the retired transitional-fallback target; gate 59 and the roll-up tool both resolve via `resolve_working`, so they cannot disagree on the location).
- Completed periods are ROLLED UP in the root CHANGELOG (daily, then weekly) AND SWEPT to the canonical PUSHED archive `grc_library_private/changelog-archive/<date>-daily.md` (durable, since the store is local-only-no-origin). These two halves are COUPLED into ONE close-out operation by `grc_library_private/tools/rollup-changelog.py` (replacing the broken `sweep-detailed-mirror.py`): a root-only roll-up (which gate 59 then fails) or a mirror-only sweep can never be produced by the sanctioned path. A planned archive-coverage gate (defense-in-depth) would further assert that every rolled-up root period vouches for an existing archive file (closing the mirror-only silent-pass direction), with an exemption list for accepted history-only ranges (e.g. 2026-08-31, whose detail is fragmented in store git history); the coupled tool is the primary guard and already prevents the split-brain drift.
- Closed-work ledger: `grc_library_private/.working/DONE.md`; backlog: `TODO.md`; overnight file:
  `grc_library_private/.working/overnight-pr.md` (gate 46 enforces its Status lifecycle).
- The DONE worked example, concretely: PR #172 "FR-4+5+6+7+8: README polish bundle"
  (2026-06-21), five medium README findings closed in one PR.
- **After-merge next-N list source (this project):** the pack body's "list the upcoming next-N planned PRs from TODO" (`### After-merge`) reads, in this project, the `## Up next` queue at the top of the private `P-TODO.md` (the single ordered work queue across both backlogs; CLAUDE.md `## PR workflow` step 9). `TODO.md`'s Standing-conventions note and `.claude/playbooks/pr-lifecycle.md` are aligned to this; `/orch` itself continues from the handoff Next-actions, not this queue.

## clarify-before-acting.md

- Project instantiation: the CLAUDE.md `Behavioral rule: clarify before acting`
  section; the structured question primitive available here is `AskUserQuestion`.

## decision-classification-before-enacting.md

- The write-before-enact decisions log is `grc_library_private/autonomous-decisions-log.md`: every significant autonomous decision is classified (an `ACT` / `ASK` / `BLOCKED: <type>` line) and written there before it is enacted. The closed blocker set is as in the rule body (`maintainer-decision-unreachable`, `irreversible-needs-confirmation`, `failing-check`, `source-unavailable`, `maintainer-directed-hold`).
- Mechanical backstop: the [`block-unjustified-decision.py`](../hooks/block-unjustified-decision.py) PreToolUse hook refuses a log write that lacks a `**Classification:**` line, names a blocker-type outside the closed set, or (in a deferral or hold entry) cites a forbidden internal-state justification; a `grc_library_private` validate check gates the log's shape in parity with the hook.
- The set-completeness / anti-false-completeness half is enforced by [`tools/audit-backlog-actionability.py`](../../tools/audit-backlog-actionability.py) (the enumeration tool the hold path must quote) plus the same hook's exhaustion guard (a hold justified by a set-completeness claim is refused unless it embeds a fresh full-audit token matching the live backlog count).
- Project instantiation: the CLAUDE.md `## Decision discipline: act, ask, or name a blocker (write-before-enact)` and `## Backlog-status characterization is the audit tool's output` sections.

## evidence-grounded-completion.md

- The stated-intention rule's mechanical backstop here is the
  [`block-turn-end-with-outstanding-work.py`](../hooks/block-turn-end-with-outstanding-work.py)
  Stop hook: it refuses turn-end while any local branch (except `main` and recorded held branches) is ahead of `main` AND `git diff --quiet` reports a differing tree (a branch ahead of `main` but tree-identical, e.g. squash-merged-but-undeleted, is exempt; a diff-command error also leaves the branch reportable).
  It fails open, honours a one-shot `.allow-stop` escape
  FILE for a genuine block, and exempts deliberately-held branches through the `held-branches.txt`
  file; the hook mechanically checks only that each entry carries a YYYY-MM-DD-shaped token comparing lexically at or after today, while the reason and any decision-record citation are the instructed convention it does not verify.

- The broken-link audit the no-decorative-links section names is gate 3
  (repository-internal link audit, `tools/lint-links.py`); the domain allow-list
  gate is `tools/lint-external-link-domains.py`.

## gate-discipline.md

- The removal ledger the footer names: `claude-rules-considerations`
  (this rule's why-section moved there in the GR-P2 two-layer condense, PR #726).
- This project offers NO exception register: a failing gate means fix the artefact
  or descope the PR (the strict-mode stance in the project CLAUDE.md Boundaries).

## high-assurance-verification.md

- The persistent register: `high-assurance/register` (surfaced at
  `/orch` alongside the other standing registers).

## project-integrity.md

- The project instantiation is the PRIMORDIAL RULE section at the top of the
  project CLAUDE.md (the AIQT checkpoint line and cadence).

## session-lifecycle.md

- Handoff record: `grc_library_private/.working/session-handoff.md`; concurrency lease:
  `grc_library_private/.working/session-state.md` (gate 63 guards its shape); resume command: `/orch`.
- Pending decisions: `grc_library_private/.working/pending-decisions.md`; the timer default and the
  operating modes are operationalized in the project CLAUDE.md attended-autonomous,
  wind-down, and session-migration sections.
- Unattended-degradation auto-handoff (section 4): operationalized in the project
  CLAUDE.md's No idle-stop-in-unattended-mode item (item 4 of `## Attended-autonomous operating mode`) and the wind-down sections. The closing
  handoff is executed directly and takes no `AskUserQuestion` (the unattended hook
  blocks it anyway); the concrete close is a green merged PR plus a refreshed
  `grc_library_private/.working/session-handoff.md` (Next-actions, State-snapshot, Asserted-expectations,
  green-at-`<sha>`) and the `grc_library_private/.working/session-state.md` lease RELEASE.
- **No-manufactured-winddown interim supersession (2026-08-28).** The fleet share
  `10-TRUST-no-manufactured-winddown` is adopted as an interim local control in the project CLAUDE.md
  `## No manufactured wind-down` section, which SUPERSEDES this rule's §1 "prefer a fresh session"
  preference, its §4 "session depth is a legitimate CONTRIBUTING factor" clause (both OFFER sub-cases),
  and its "winding down on felt degradation or work shape" anti-pattern until the canonical
  guardrails/AIQT pack ships and reconciles. Read that CLAUDE.md section as governing on wind-down
  triggers. Overlay-only; the pack rule body is unchanged.
- **#5(b) attended->unattended timeout swap (2026-08-28).** The project CLAUDE.md §3
  graceful-degradation timeout now performs an ASSISTANT-INITIATED `Operating-mode` transition
  attended-autonomous -> daytime-unattended on a no-answer timeout (records the decision PENDING,
  continues), a NARROW project exception to §2's "mode transitions are operator acts", authorized by
  fleet directive #5(b). It is direction-limited: attended -> MORE-unattended ONLY, never ENDING
  unattended, so §2's hard clause ("ending an unattended mode is never a no-answer default or a
  timeout effect") is fully preserved. Swap-BACK to attended remains an operator act per §2:
  maintainer return does not itself restore attended mode (the block-askuserquestion-unattended.py
  message states that a lease more unattended than the fleet file ends only on an explicit
  operator instruction; since 2026-09-25 the hook also reads the canonical fleet mode file). Reversibility gate absolute:
  authorial / irreversible / outward decisions still defer-and-skip, never auto-proceed. Overlay-only;
  pack §2 body unchanged.

## surface-counterproductive-instructions.md

- Project instantiation: the CLAUDE.md communication conventions (proactive
  assessment as a standing default; "suggest"/"advise" invite assessment).

## trust-recovery-escalation.md

- Slash commands: the forensic pass is `/full-qa`, the persona pass is `/fitness`,
  the suite wrapper is `/trust-recovery` (all under `.claude/commands/`).

## validate-inference-before-action.md

- The register in which validation-sweep dispatch declarations are recorded
  (the skill's Rule 5.6): `grc_library_private/.working/validate-sweeps/history.md`.
- The repeated-failure circuit-breaker is backed by the
  [`block-repeated-tool-failure.py`](../hooks/block-repeated-tool-failure.py)
  PreToolUse hook, which mechanically refuses a byte-identical resubmit (GUARD 1) and, on
  two or more consecutive same-class blocks, escalates the refusal with a hard-stop
  instruction to WRITE a mechanism diagnosis before retrying (GUARD 2); the hook does not
  verify the diagnosis, and a command whose subject matches no recent blocked subject passes
  it, so writing and assessing the diagnosis is the discipline the hook prompts, not one it
  enforces. The degradation hypothesis, if raised, is recorded and assessed in
  `grc_library_private/degradation-watch-log.md` before it is asserted.
