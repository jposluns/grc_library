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
