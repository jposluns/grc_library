# Claude Code Security Rules: Usage Guide

**Document Title:** Claude Code Security Rules Usage Guide\
**Document Type:** Guideline\
**Version:** 1.72.3\
**Date:** 2026-10-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Parent-library related documents:** `dev-security/standard-developer-security-requirements.md`, `dev-security/standard-devops-security-requirements.md`, `dev-security/guideline-ai-coding-assistant-security.md`, `ai/standard-ai-and-agentic-development-security.md`\
**Canonical parent-repository path:** [`guardrails/README.md`](README.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Monthly, and upon material threat, tooling, or framework change\
**Confidentiality:** Public\
**GRC-original license:** CC BY-SA 4.0\
**Pinned AIQT snapshot license:** Apache-2.0

---

**Pinned AIQT runtime adoption.** This installation uses 132 pinned AIQT rules (83 AIQT principles + 49 security rules), 15 retained GRC compatibility procedures, and 24 skills. The exact upstream commit is `a3ff734ca855e4363f340eca52fbd87272c51854`, recorded in `vendor/aiqt/RULES.json` and `vendor/aiqt/PIN.toml`; it is not a tagged release. The legacy procedures remain mandatory at their activity boundary; none retires. GRC-original material retains CC BY-SA 4.0. The upstream-owned pinned snapshot in `guardrails/aiqt-rules/` and its local rule derivatives are separately licensed Apache-2.0; retain the verbatim upstream LICENSE and NOTICE in that directory. GRC owns its compatibility rule and the retained legacy procedures. Authority: maintainer decisions D1-D3, 2026-10-02 12:27Z.

## What are these files?

The `guardrails/` directory contains a set of Markdown files designed to be loaded into [Claude Code](https://code.claude.com/docs/en/claude-code) sessions as security and development-governance context. When Claude Code reads these files, either via a `CLAUDE.md` in your project root, via `.claude/rules/*.md` files with optional path-scoped frontmatter, or by referencing a file with an `@` mention (or adding a directory with the `--add-dir` CLI flag), they encode security, compliance, and development-governance requirements as persistent context that the AI coding assistant applies during development.

These are **draggable rule files**: copy any subset into your project's Claude Code context and Claude will apply those security and governance requirements to code it writes, reviews, and suggests.

---

## Pack scope

The pack covers two areas:

1. **Security and compliance.** Hardcoded-secrets prevention, input validation, cryptography, authentication, OWASP/ASVS alignment, AI/agent/MCP/RAG security, CI/CD pipeline gates, language-specific security patterns. Lives under `core/`, `ai/`, `pipeline/`, and `languages/`.
2. **Development-governance discipline.** Rules that govern how an AI coding assistant collaborates on a governed codebase: gate discipline, change-tracking discipline, evidence-grounded completion, clarify-before-acting on ambiguous requests, artefact-and-branch discipline, action-before-explanation-of-inaction, validate-inference-before-action, AI-assistant workflow disciplines (research-assistant, pipeline construction, apply-time correction, always-split, CI-wait productivity), the trust-recovery escalation tier, the project-integrity apex rule (the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost), surfacing counterproductive instructions before acting on them, high-assurance verification for sensitive changes (independent adversarial verification plus a deterministic apply, persisted across sessions), and the session-lifecycle and operating-modes discipline for multi-session work (durable handoff, explicit operator-set modes, graceful degradation, evidence-gated wind-down, the green-merge close, and a concurrency lease). Lives under `governance/`.

The pack also ships **Claude Code Skills** (`SKILL.md` workflow format) under `skills/`, derived from selected governance rules. The canonical rule remains the source of truth for normative content (framework alignment, exception handling, rationale); the skill is the workflow wrapper (when to invoke, what steps in what order, what verification confirms completion). The directory tree below lists the current set; per-version shipping history lives in the parent library's `CHANGELOG.md` and in git history.

The pack originated inside a parent GRC library as the operational layer that allowed the maintainer to keep that corpus consistent with Claude Code participating in PRs; the pack stands alone without it. Every governance rule in the pack was shaped by the parent library's real maintenance practice, some earned directly from incidents and some codified up front against known failure classes (several later grounded by real events); the pack is the library's lessons learned, made portable. Each rule's origin is summarized in the pack's own provenance register, [`rule-provenance.md`](rule-provenance.md), with the detailed lineage preserved in the parent library's records.

## Three ways to use this pack

This pack supports three adoption paths, all first-class:

1. **Inside the parent GRC library, as-shipped.** No action required. If you fork the whole parent repository, the pack is already wired into `.claude/rules/` (via the sync audit in `tools/lint-claude-rules-sync.py`) and the skills are discoverable to Claude Code as the parent library is.

2. **Inside a fork of the parent GRC library.** Same as above, plus organization-specific overlays. An adopting organization forks, substitutes organization-specific values across the corpus, and inherits the pack as the operational discipline its Claude Code sessions apply. See the parent library's `docs/adopter-guide.md` for the full path (Mode A).

3. **As a standalone Claude Code baseline pack, on any project.** A Claude Code baseline pack, usable on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. Take this directory only and drop it into your project's Claude Code context. The setup generator at [`setup-generator-prompt.md`](setup-generator-prompt.md) automates this; the manual paths are documented in the "How to use" section below. The pack ships with its own version sequence so consumers in this mode can track pack updates without needing to track the parent library's version.

The third mode began as an emergent use adopted by developers in practice and is supported as a first-class path alongside the fork-the-whole-repo path; a standalone adopter needs nothing from the parent library. Provenance is what makes the pack credible as a standalone artefact: the pack's provenance register, [`rule-provenance.md`](rule-provenance.md), summarizes each rule's origin, a real maintenance event where one exists and an honest up-front codification where that is the truth, without the parent project's internal detail.

---

## The AIQT baseline (copy-paste starter)

Adopting nothing else from this pack, a project can still adopt its apex ordering. Paste this at the top of your project's `CLAUDE.md` (or equivalent assistant instructions file):

```markdown
## The AIQT Principle (apex rule)

**(Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost.** The four facets form one
non-negotiable top tier with no internal ranking; the tier outranks progress, progress
outranks speed, and speed outranks cost. "Done faster", "done cheaper", or "done sooner"
is never a reason for "done worse". Progress (decide and act when the answer is derivable;
do not spin or grind marginal work when a clean handoff is available) and Speed (latency)
are the throughput tier below the AIQT tier, and neither ever reduces verification.

- **Accuracy**: every claim matches its source; every state assertion rests on an
  observation, not an inference. If a fact is unknown, say so.
- **Integrity**: no stubbed or simulated results presented as finished work, no
  suppressed or weakened checks, no fabrication, no silent changes; failing states
  are surfaced, never concealed.
- **Quality**: the work meets the project's own standard of craft and passes its
  checks, run on the final state, unpiped.
- **Trust**: warranted by the record, granted by the human. Every claim traceable to
  evidence; overrides logged; failures reported plainly.

If satisfying this tier conflicts with a deadline or a budget, halt and escalate the
tradeoff; do not resolve it silently in favour of progress, speed, or cost.

Checkpoint (start of task, before commit, before any "done" claim):
`AIQT check: (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost. Non-negotiable.`
```

The honest caveat, stated so adopters do not mistake a preamble for a control: a principle in an instructions file guides behaviour but does not enforce it. The enforcement is mechanical (CI gates, audit scripts, branch protection) and procedural (the rest of this pack's rules); this baseline is the ordering they all assume. Start with the baseline, then adopt the rules and gates that make it stick.

---

## Directory structure

```text
guardrails/
├── README.md                   This file
├── CLAUDE.md                   Root file: copy the WHOLE guardrails/ dir (Option 1), not this file alone
├── setup-generator-prompt.md   AI-assisted setup generator prompt for downstream consumers
├── vetting-log.md              Maintainer vetting log for the external rule sources referenced below
├── rule-provenance.md          Per-rule provenance register: each governance rule's origin, incident-earned or up-front-codified, without parent-project internals
├── guidance-claude-md-optimization.md  Maintainer guidance: condense a CLAUDE.md without losing a rule
├── aiqt-rules/                 Upstream Apache-2.0 pinned snapshot
│   ├── aiqt/
<!-- AIQT-TREE-aiqt-BEGIN -->
│   │   ├── 00-project-integrity.md
│   │   ├── 10-ACCUR-citation-from-opened-file.md
│   │   ├── 10-ACCUR-claims-rest-on-observation.md
│   │   ├── 10-ACCUR-completeness-claim-enumerates-its-set.md
│   │   ├── 10-ACCUR-corroborate-external-claims.md
│   │   ├── 10-ACCUR-count-carries-its-predicate.md
│   │   ├── 10-ACCUR-disclose-guard-residuals.md
│   │   ├── 10-ACCUR-evidence-grounded-completion.md
│   │   ├── 10-ACCUR-guard-input-soundness.md
│   │   ├── 10-ACCUR-measured-and-estimated-figures-stay-separate.md
│   │   ├── 10-ACCUR-no-fabrication.md
│   │   ├── 10-ACCUR-observe-before-asserting-behaviour.md
│   │   ├── 10-ACCUR-partial-read-is-not-the-whole.md
│   │   ├── 10-ACCUR-read-before-characterizing.md
│   │   ├── 10-ACCUR-reference-capture.md
│   │   ├── 10-ACCUR-reproduce-before-fix.md
│   │   ├── 10-ACCUR-timestamp-from-clock.md
│   │   ├── 10-ACCUR-validate-inference-before-action.md
│   │   ├── 10-ACCUR-verify-fix-in-commit.md
│   │   ├── 10-INTEG-anything-wrong-fixed-first.md
│   │   ├── 10-INTEG-attestation-is-harness-owned.md
│   │   ├── 10-INTEG-branch-and-merge-on-green.md
│   │   ├── 10-INTEG-branch-rooted-on-live-main.md
│   │   ├── 10-INTEG-check-fails-closed-on-unreadable.md
│   │   ├── 10-INTEG-commit-identity.md
│   │   ├── 10-INTEG-explicit-binding-over-ambient-context.md
│   │   ├── 10-INTEG-gate-discipline.md
│   │   ├── 10-INTEG-generated-artefact-source-only.md
│   │   ├── 10-INTEG-licence-compatibility.md
│   │   ├── 10-INTEG-no-concealed-failure.md
│   │   ├── 10-INTEG-preserve-uncommitted-work.md
│   │   ├── 10-INTEG-protected-branch-integrity.md
│   │   ├── 10-INTEG-required-step-remains-required.md
│   │   ├── 10-INTEG-rerun-pass-is-still-failure.md
│   │   ├── 10-INTEG-review-in-flight-pins-its-artefact.md
│   │   ├── 10-INTEG-safe-retries.md
│   │   ├── 10-INTEG-separate-task-changes.md
│   │   ├── 10-INTEG-stage-then-promote-on-green.md
│   │   ├── 10-INTEG-track-launched-work.md
│   │   ├── 10-INTEG-validation-gates-apply.md
│   │   ├── 10-INTEG-workers-produce-inert-data.md
│   │   ├── 10-QUALI-absolute-paths.md
│   │   ├── 10-QUALI-change-carries-check.md
│   │   ├── 10-QUALI-compatibility-or-migration.md
│   │   ├── 10-QUALI-confirm-execution-target.md
│   │   ├── 10-QUALI-defence-in-depth-default.md
│   │   ├── 10-QUALI-elapsed-aware-timer-restore.md
│   │   ├── 10-QUALI-findings-are-fixed-not-argued.md
│   │   ├── 10-QUALI-goal-fidelity-across-trajectory.md
│   │   ├── 10-QUALI-high-assurance-verification.md
│   │   ├── 10-QUALI-kill-timeout-exceeds-callee-wait.md
│   │   ├── 10-QUALI-lightweight-verifier-workers.md
│   │   ├── 10-QUALI-match-surrounding-code.md
│   │   ├── 10-QUALI-minimize-dependencies.md
│   │   ├── 10-QUALI-self-guardrail-from-error.md
│   │   ├── 10-QUALI-smallest-correct-change.md
│   │   ├── 10-QUALI-surface-counterproductive-instructions.md
│   │   ├── 10-QUALI-test-hermeticity.md
│   │   ├── 10-QUALI-verifier-delivery-completeness.md
│   │   ├── 10-QUALI-verifier-diversity.md
│   │   ├── 10-TRUST-ai-toolchain-register.md
│   │   ├── 10-TRUST-assess-advise-discussion-only.md
│   │   ├── 10-TRUST-atomic-claim-from-pool.md
│   │   ├── 10-TRUST-change-record.md
│   │   ├── 10-TRUST-change-tracking-ext.md
│   │   ├── 10-TRUST-clarify-before-acting.md
│   │   ├── 10-TRUST-concurrency-lease.md
│   │   ├── 10-TRUST-continue-by-default.md
│   │   ├── 10-TRUST-express-authorization-before-execution.md
│   │   ├── 10-TRUST-human-oversight-and-autonomy-threshold.md
│   │   ├── 10-TRUST-no-console-diff-dumps.md
│   │   ├── 10-TRUST-orchestrator-mistakes-register.md
│   │   ├── 10-TRUST-reconcile-record-against-reality.md
│   │   ├── 10-TRUST-records-first.md
│   │   ├── 10-TRUST-session-close-on-green.md
│   │   ├── 10-TRUST-session-resume-from-handoff.md
│   │   ├── 10-TRUST-standing-constraints-persist.md
│   │   ├── 10-TRUST-trust-recovery-escalation.md
│   │   ├── 10-TRUST-trust-recovery-ext.md
│   │   ├── 20-PROGR-decision-classification-before-enacting.md
│   │   ├── 20-PROGR-repeated-failure-triggers-premise-review.md
│   │   ├── 30-SPEED-background-work-during-ci-waits.md
│   │   ├── 40-COST-cost-tier.md
<!-- AIQT-TREE-aiqt-END -->
│   ├── security/
<!-- AIQT-TREE-security-BEGIN -->
│   │   ├── SECA-resource-bounds.md
│   │   ├── SECA-verified-restore-path.md
│   │   ├── SECC-data-boundary.md
│   │   ├── SECC-egress-destinations.md
│   │   ├── SECC-keep-secrets-out.md
│   │   ├── SECC-least-privilege-retrieval.md
│   │   ├── SECC-no-cross-context-bleed.md
│   │   ├── SECC-no-hidden-context-disclosure.md
│   │   ├── SECC-rotate-leaked-secret.md
│   │   ├── SECI-authentication.md
│   │   ├── SECI-authorization.md
│   │   ├── SECI-config-is-executable-trust-gate.md
│   │   ├── SECI-cryptography.md
│   │   ├── SECI-dependency-provenance.md
│   │   ├── SECI-fail-closed.md
│   │   ├── SECI-federated-identity-flow.md
│   │   ├── SECI-file-upload-handling.md
│   │   ├── SECI-guardrail-config-integrity.md
│   │   ├── SECI-human-authorization.md
│   │   ├── SECI-input-validation.md
│   │   ├── SECI-inter-agent-trust.md
│   │   ├── SECI-key-management.md
│   │   ├── SECI-least-privilege-tools.md
│   │   ├── SECI-log-redaction.md
│   │   ├── SECI-operator-deception.md
│   │   ├── SECI-output-encoding.md
│   │   ├── SECI-output-handling.md
│   │   ├── SECI-pin-referenced-instructions.md
│   │   ├── SECI-poisoning-resistance.md
│   │   ├── SECI-prefer-removing-a-path.md
│   │   ├── SECI-preview-has-no-side-effects.md
│   │   ├── SECI-prompt-trust-hierarchy.md
│   │   ├── SECI-protect-audit-records.md
│   │   ├── SECI-reject-vulnerable-versions.md
│   │   ├── SECI-release-integrity.md
│   │   ├── SECI-safe-deserialization.md
│   │   ├── SECI-secure-configuration.md
│   │   ├── SECI-security-logging.md
│   │   ├── SECI-session-token-management.md
│   │   ├── SECI-ssrf-prevention.md
│   │   ├── SECI-symlink-resolution.md
│   │   ├── SECI-threat-model-boundaries.md
│   │   ├── SECI-tool-argument-validation.md
│   │   ├── SECI-untrusted-content.md
│   │   ├── SECI-verify-dependency-exists.md
│   │   ├── SECP-data-minimization.md
│   │   ├── SECP-data-residency-retention.md
│   │   ├── SECP-purpose-limitation.md
│   │   ├── SECP-synthetic-fixture-data.md
<!-- AIQT-TREE-security-END -->
├── core/                       Security and compliance rules (secrets, auth, input validation, crypto, OWASP)
│   ├── secrets.md              Never hardcode credentials, keys, or tokens
│   ├── authentication.md       Secure authentication and session requirements
│   ├── input-validation.md     Input validation and output encoding
│   ├── cryptography.md         Approved algorithms and key handling
│   └── owasp.md                OWASP Top 10:2025 and ASVS v5 alignment rules
├── governance/                 Development-governance discipline (initial rollout complete at pack 1.11.0; extended at 1.21.0, 1.27.0, 1.36.0, 1.47.0, 1.49.0, 1.51.0, 1.52.0, and 1.59.0)
│   ├── gate-discipline.md                       Never weaken a gate to silence a failure; fix the artefact
│   ├── change-tracking.md                       Every PR carries an entry (terse OK for ancillary changes); no skip path
│   ├── evidence-grounded-completion.md          No completion claim or unread-artefact state assertion without enumerated, re-read, quoted, contradiction-searched evidence; plus un-observable-state, inventory, and external-version-currency corollaries
│   ├── clarify-before-acting.md                 Surface ambiguity in one sentence and ask; never silently pick
│   ├── artefact-and-branch-discipline.md        Generated artefacts are read-only; protected branches are append-only
│   ├── action-before-explanation-of-inaction.md No inferred reasons for why an external action cannot proceed; attempt the safe action and report the real result, or name the destructive action and ask
│   ├── validate-inference-before-action.md      Validate any inferred premise via tool call before the action that depends on it; cascade failures are what the rule prevents
│   ├── ai-assistant-workflow-disciplines.md     Five disciplines for an AI assistant driving multi-PR work (research-assistant, pipeline construction, apply-time correction, always-split, CI-wait productivity), the commit-before-dispatch immutable-basis requirement, plus the layered skeptical pre-push verification standard (tiered verifier subagents, six-iteration cap (nine unattended while converging), logged overrides)
│   ├── trust-recovery-escalation.md             Escalation tier when discipline failures need a white-box re-examination: the /full-qa + /fitness suite, every finding routed tiered by severity, maintainer sign-off terminates
│   ├── project-integrity.md                     Apex rule: the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost, non-negotiable; orders the other rules under a single priority on the optimization-dimension axis
│   ├── surface-counterproductive-instructions.md A clear instruction can still be wrong: surface a counterproductive one (efficiency/quality/work-loss/stale-state) and confirm before acting; never silently take a harmful literal reading or revert committed work
│   ├── high-assurance-verification.md           Heavier pre-apply harness for sensitive changes (gate-blind/delicate/costly): research fan-out, signal pass over negatives, two or more independent adversarial verifiers, programmatic floor, deterministic apply plus re-parse; persisted across sessions, proactive counterpart to trust-recovery
│   ├── session-lifecycle.md                     Session-lifecycle and operating-modes discipline: durable reconciled handoff record, explicit operator-set modes (attended / attended-autonomous / unattended), graceful degradation for blocked decisions with an absolute reversibility gate, evidence-gated wind-down (continue is the default), the green-merge close with its loop-break compensating control, and an advisory concurrency lease
│   ├── decision-classification-before-enacting.md Classify a significant autonomous decision (one that disposes of a queued item or bends the plan) ACT / ASK / BLOCKED against a closed, externally-observable blocker set, written before enacting; never a hold on un-instrumented internal state
│   └── express-authorization-before-execution.md Execution of a plan-initiating unit of work begins only on an express, work-naming authorization; a discussion is not a go, and a conditional go authorizes only its first step; the pause-before-acting family's entry-condition member
├── ai/
│   ├── ai-security.md          LLM and AI application security requirements
│   ├── agent-security.md       Agentic workflow security and trust boundaries
│   ├── rag-security.md         Retrieval-augmented generation data controls
│   └── mcp-security.md         Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md           CI/CD security gates and pipeline controls
├── aiqt/                       Cross-family review machinery (contract, schemas, families, setup)
│   ├── review-contract.md      The cross-family skeptical review contract (v1)
│   ├── config-format.md        The adopter config.md spec: layout, bounded write set, consent
│   ├── setup-wizard.md         Re-runnable onboarding wizard (writes only config.md)
│   ├── doctor.md               Read-only health checks (incl. bounded-write-set verification)
│   ├── families.json           Reviewer family registry (Claude, Codex; extensible)
│   ├── ci-kit/                 CI integration kit
│   │   ├── README.md           Kit runbook: secrets, per-vendor auth, evidence policy
│   │   ├── prompts/
│   │   │   └── aiqt-review.md  The one canonical review brief both lanes render
│   │   └── workflows/
│   │       ├── aiqt-review-claude-on-codex.yml   Claude reviews Codex-authored changes
│   │       └── aiqt-review-codex-on-claude.yml   Codex reviews Claude-authored changes
│   └── schemas/                SARIF-lite interchange schemas
│       ├── finding.schema.json   Per-finding record schema
│       └── verdict.schema.json   Verdict envelope schema
├── skills/                     Claude Code Skills (SKILL.md format) derived from selected pack rules
│   ├── evidence-grounded-completion/SKILL.md          Six-step verification protocol before any completion claim or unread-artefact state assertion
│   ├── gate-discipline-diagnose/SKILL.md              Diagnose-then-fix-the-artefact response to a failing gate
│   ├── clarify-before-acting/SKILL.md                 One-sentence ambiguity surfacing with named alternatives
│   ├── action-before-explanation-of-inaction/SKILL.md Reversibility-gate protocol before any "X is blocked because Y" clause attached to an external action
│   ├── change-tracking-write-entry/SKILL.md           Entry-writing workflow that satisfies the delta gate, link-coverage gate, and version-monotonicity audit in one pass
│   ├── validate-inference/SKILL.md                    Premise-validation workflow (name, cost, validate, act, record) before an action depends on an unobserved state claim
│   ├── surface-instruction-concern/SKILL.md           Stop-consider-confirm protocol before executing a clear but counterproductive instruction
│   ├── artefact-discipline-check/SKILL.md             Routing workflow that redirects a hand-edit of a generated file (or a protected-branch operation) to the correct path
│   ├── validation-sweep/SKILL.md                      Project-wide regression sweep as a follow-up after any issue identified and corrected; loops until clean
│   ├── validation-sweep-pr-scoped/SKILL.md            PR-scoped validation sweep run as the PR's finalizing step; Subagent A on the PR's diff plus a cross-reference check; runs before merge to catch per-PR drift before it compounds
│   ├── citation-quote-verification/SKILL.md           Verify cited quotes match source text at the cited location; catches what citation-format and currency linters cannot
│   ├── fresh-reader-validation/SKILL.md               Dispatch a fresh subagent to read a new or substantively-revised document and surface tacit-context gaps
│   ├── skill-authoring-discipline/SKILL.md            Apply the pack's structural template and validate trigger accuracy when adding a new skill
│   ├── library-fitness-review/SKILL.md                Whole-corpus library-quality review with a project-defined catalogue of persona reviewers; periodic deliverable, not a per-PR gate
│   ├── deep-qa-review/SKILL.md                        Trust-recovery deep-QA forensic pass; six AI-failure-pattern subagents over a PR window; pairs with library-fitness-review; findings routed tiered by severity, maintainer sign-off terminates
│   ├── pr-retrospective/SKILL.md                      Retrospective on each PR as its finalizing step; appends to the improvement-log register; recurring patterns surface as candidates for pack-rule updates or worker-brief additions
│   ├── guardrail-review/SKILL.md                      Periodic structural-integrity review of the governance machinery (rules, skills, gates, wiring surfaces) for overlap / gap / drift the mechanical parity gates cannot see; maintainer-triggered + auto-prompt on machinery change
│   ├── matrix-fit/SKILL.md                            Cadenced semantic-fit audit of the compliance matrix and per-document framework tables; catches the gate-blind "valid code, wrong control" class the existence gates cannot; after each batch that adds or edits mapping rows, at completion of a mapping surface, and ad-hoc
│   ├── claim-fit/SKILL.md                             Cadenced citation-precision audit of normative-attribution claims; catches the gate-blind "attributed value, silent source" class the existence and citation gates cannot; one-time Tier-A pass at adoption + after normative-value batches + periodic Tier-B coverage sweep + ad-hoc
│   ├── high-assurance-verification/SKILL.md           Heavier pre-apply harness for a sensitive change (gate-blind, delicate-at-scale, costly): research fan-out, signal pass over the negatives, two or more independent adversarial verifiers, an invariant floor, and a deterministic scripted apply plus re-parse; the executable form of the high-assurance-verification rule
│   ├── deep-assessment/SKILL.md                       Rare, maintainer-invoked whole-project deep assessment; composes the semantic instruments by invocation and adds the lenses the routine cadence does not apply to itself (gate-efficacy probing, blind-spot mapping, ground-truth sampling, adoptability and pipeline integrity, QA-ledger meta-audit); count-free and inventory-deriving, register-backed and re-entrant, completion-standard-terminated (no separate sign-off, since it composes only established validate-and-fix QA processes); derives_from trust-recovery-escalation
│   ├── reference-audit/SKILL.md                        Cadenced reference-breadth audit between project claims and an available reference base, both directions; catches the gate-blind "held but unused" class (surfaced by the parent GRC library's SP 800-154 lesson); full, per-touch, and new-ingest modes with project-defined evidence tiers; dispatches a semantic judge over the configured audit worklist; derives_from evidence-grounded-completion
│   ├── publication-screening/SKILL.md                  Screening protocol for untrusted publications before their content informs project work; provenance + mechanical instruction-content scan + trusted-source corroboration, four-valued verdict (screened/pending/quarantined/discard-candidate) in the project's configured screening register; admission control, never a trust upgrade; derives_from evidence-grounded-completion
│   └── adopt/SKILL.md                                  Run-once onboarding for a confirmed fork of a project distributing this pack; resets inherited machinery-core working-state to clean adopter baselines (or treats an absent working-state tree as already clean, creating only the adopter-local state a versioned consumer requires), settles the optional-dependency model (own external dependencies vs self-contained), removes maintainer-only residue, records the choices in the project's committed adoption marker the resume mechanism reads; fork-only, once; derives_from session-lifecycle
└── languages/
    ├── python.md                Python-specific security patterns and anti-patterns
    ├── typescript.md            TypeScript / Node.js security patterns
    ├── csharp.md                C# / .NET security patterns (server-side)
    ├── java.md                  Java / Spring security patterns (server-side)
    ├── go.md                    Go security patterns
    ├── swift.md                 Swift / iOS (and Objective-C) mobile security patterns
    ├── kotlin.md                Kotlin / Android (and Java for Android) mobile security patterns
    ├── react-native.md          React Native (with or without Expo) cross-platform mobile security patterns
    ├── flutter.md               Flutter / Dart cross-platform mobile security patterns
    ├── dotnet-maui.md           .NET MAUI (and Blazor Hybrid) cross-platform mobile security patterns
    └── capacitor-ionic.md       Capacitor / Ionic (WebView-based hybrid) cross-platform mobile security patterns
```

---

## How to use

### Pinned runtime installation

Use the exact inventory and declared scope insertions in `vendor/aiqt/RULES.json`.
Copy `guardrails/aiqt-rules/aiqt/` and `guardrails/aiqt-rules/security/` into
`.claude/rules/`, preserving upstream frontmatter, including corpus-id and mappings.
Insert the declared paths into the existing block for the three scoped security rules;
never add a second frontmatter block. Keep LICENSE and NOTICE beside the vendored
snapshot. Do not fetch a moving head or install the snapshot README as a rule.

In GRC, `.claude/rules/governance-compatibility.md` is generated from
`.claude/references/governance-compatibility.md` plus the retained overlays.
Keep all legacy governance bodies under `.claude/references/governance/` and
read them at the mandatory compatibility triggers. Do not copy `governance/`
wholesale into `.claude/rules/` or import all the references at startup.
The existing core/language/pipeline mirrors and all skills remain available.
Standalone adopters must review GRC-specific overlays and supply their own wiring;
the GRC compatibility output is not a portable export.

### Selective GRC security modules

The following optional modules retain their existing terms and scope:
```bash
# For a Python web API with AI features
cp path/to/guardrails/core/secrets.md .claude/rules/
cp path/to/guardrails/core/input-validation.md .claude/rules/
cp path/to/guardrails/ai/ai-security.md .claude/rules/
cp path/to/guardrails/languages/python.md .claude/rules/
```

Then reference them in your project's `CLAUDE.md`:
```markdown
See .claude/rules/ for security requirements that apply to all code in this project.
```

### Option 3: add to existing claude.md

Copy the content of specific rule files into your existing `CLAUDE.md` under a `## Security Requirements` heading.

### Option 4: path-scoped rules (most context-efficient)

Place rule files in `.claude/rules/` with optional `paths:` YAML frontmatter so Claude Code loads them only when reading matching files. Rules without `paths:` load at launch; rules with `paths:` load conditionally:

```markdown
---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python security rules
(content from guardrails/languages/python.md)
```

This is the "L4 abstracted" pattern: language-specific or component-specific rules apply only when relevant, keeping the always-loaded `CLAUDE.md` lean.

### AGENTS.md interop

If your project already has an `AGENTS.md` for other coding agents (Codex, Cursor, OpenCode, Zed), add `@AGENTS.md` at the top of `CLAUDE.md`, or symlink one to the other, so both tools read the same instructions without duplicating content.

---

## Rule files and their scope

| File | When to Use |
| --- | --- |
| [`core/secrets.md`](core/secrets.md) | All projects. No exceptions. |
| [`core/authentication.md`](core/authentication.md) | Any project with user login, service accounts, or APIs |
| [`core/input-validation.md`](core/input-validation.md) | Any project processing external input |
| [`core/cryptography.md`](core/cryptography.md) | Any project storing data, using passwords, or transmitting data |
| [`core/owasp.md`](core/owasp.md) | Web applications and APIs (covers OWASP Top 10) |
| [`ai/ai-security.md`](ai/ai-security.md) | Any project using LLMs, AI APIs, or AI-generated content |
| [`ai/agent-security.md`](ai/agent-security.md) | Agentic systems, multi-agent workflows, autonomous task execution |
| [`ai/rag-security.md`](ai/rag-security.md) | Retrieval-augmented generation (RAG) systems |
| [`ai/mcp-security.md`](ai/mcp-security.md) | Projects building or consuming MCP servers |
| [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md) | DevOps/platform engineers configuring CI/CD |
| [`governance/gate-discipline.md`](governance/gate-discipline.md) | Any project with CI gates, audit programmes, or branch protections (i.e., all of them) |
| [`governance/change-tracking.md`](governance/change-tracking.md) | Any project with a CHANGELOG (or that should have one); especially projects with downstream consumers who need to read change history |
| [`governance/evidence-grounded-completion.md`](governance/evidence-grounded-completion.md) | Any project where an AI coding assistant participates (because the failure mode this rule prevents is dominant for AI assistants); doubly relevant for projects with audit programmes that gate completion claims. Its un-observable-state, inventory, and external-version-currency corollaries extend the discipline to internal-state, collection-inventory, and upstream-version assertions |
| [`governance/clarify-before-acting.md`](governance/clarify-before-acting.md) | Any project where an AI coding assistant participates; especially projects with multiple active branches, conventions that vary by request type, or trade-offs the user reasonably wants to weigh in on |
| [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md) | Any project with generated artefacts (build outputs, schema dumps, taxonomies, doc portals, lockfiles) or protected branches with branch-protection rules; doubly relevant for projects with version-monotonicity contracts |
| [`governance/action-before-explanation-of-inaction.md`](governance/action-before-explanation-of-inaction.md) | Any project where an AI coding assistant participates and may need to explain why an external action (a PR merge, a deploy, a permission check, a CI run) is not proceeding; especially projects with branch protections, CI gates, or MCP integrations where the temptation to infer a "system says no" reason without checking is highest |
| [`governance/validate-inference-before-action.md`](governance/validate-inference-before-action.md) | Any project where an AI coding assistant orchestrates multi-step workflows (sweep cycles, audit cascades, multi-PR series) and may infer a premise (state unchanged since prior run, fix complete after one occurrence, prior approval extends to current scope) to drive an action; the rule fires when inference replaces verification at any decision boundary |
| [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md) | Any project where an AI coding assistant drives substantive multi-PR work over a long session with research-helper subagents and CI gating. The rule covers research-assistant verification, pipeline PR construction, apply-time worker correction, "split when in doubt", productive CI-wait use, and the commit-before-dispatch requirement that a QA basis be an immutable revision, plus the layered skeptical pre-push verification standard (tiered refute-briefed verifier subagents, the six-iteration finding loop (nine unattended while converging), never-silent overrides); surfaces when the orchestrator is dispatching multiple workers in parallel, when changes might be bundled, when idle during CI, or when pasting worker prose unverified |
| [`governance/trust-recovery-escalation.md`](governance/trust-recovery-escalation.md) | Any project where an AI coding assistant ships work across multiple changes with a maintainer in the loop; the escalation tier invoked when accumulated discipline failures (abbreviated or skipped QA across changes, a skipped verification that reached the shared pipeline, a cascaded unvalidated inference) put a maintainer's confidence in a window of work in question and a heavier white-box re-examination is warranted |
| [`governance/project-integrity.md`](governance/project-integrity.md) | Any project where an AI coding assistant participates; the apex rule fixing the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost, invoked at every point where those dimensions are in tension (deadline, token, or throughput pressure tempting a quality or integrity compromise) |
| [`governance/surface-counterproductive-instructions.md`](governance/surface-counterproductive-instructions.md) | Any project where an AI coding assistant executes requestor instructions; fires when a clear instruction's execution as given would be net-negative (destroy work already done, lower quality, waste effort, contradict a stated goal, or rest on a stale-state belief), so the assistant surfaces the concrete cost with named options and confirms before acting |
| [`governance/high-assurance-verification.md`](governance/high-assurance-verification.md) | Any project where an AI coding assistant ships changes whose correctness a mechanical gate cannot fully verify; the heavier pre-apply harness for a sensitive change (gate-blind on correctness, delicate at scale, costly to get wrong), adding independent adversarial verification and a deterministic apply on top of the routine research-and-author flow |
| [`governance/session-lifecycle.md`](governance/session-lifecycle.md) | Any project running multi-session AI-assisted work; the RESUME / WORK / CLOSE lifecycle apparatus, a durable reconciled handoff record, explicit operator-set operating modes (fully attended / attended-autonomous / unattended), graceful degradation for blocked operator decisions with an absolute reversibility gate, evidence-gated wind-down (continue is the default), the closing green-merge with its loop-break compensating control, and an advisory concurrency lease |
| [`governance/decision-classification-before-enacting.md`](governance/decision-classification-before-enacting.md) | Any project where an AI coding assistant makes autonomous decisions that dispose of queued or authorized work or bend the plan (a defer, re-sequence, wind-down, skip, or an authorial choice made without asking); the rule classifies each such decision as exactly one of ACT / ASK / BLOCKED and requires it to be written before it is enacted, with a BLOCKED decision naming a blocker from a closed, externally-observable set, so an un-instrumented internal-state hold cannot pass as a considered decision |
| [`governance/express-authorization-before-execution.md`](governance/express-authorization-before-execution.md) | Any project where an AI coding assistant might begin executing work (edits, commits, outward actions) off the back of a planning discussion or a conditional go rather than an express, work-naming authorization; the rule holds the assistant in discussion mode until the responsible authority gives an express go that names the work, and treats a conditional or sequenced go as authorizing only its first step |
| [`languages/python.md`](languages/python.md) | Python codebases |
| [`languages/typescript.md`](languages/typescript.md) | TypeScript / Node.js codebases |
| [`languages/csharp.md`](languages/csharp.md) | C# / .NET codebases |
| [`languages/java.md`](languages/java.md) | Java / Spring Boot codebases |
| [`languages/go.md`](languages/go.md) | Go codebases |
| [`languages/swift.md`](languages/swift.md) | iOS applications written in Swift or Objective-C; covers platform-specific secure coding and native-layer controls |
| [`languages/kotlin.md`](languages/kotlin.md) | Android applications written in Kotlin or Java; covers platform-specific secure coding and native-layer controls |
| [`languages/react-native.md`](languages/react-native.md) | React Native (with or without Expo) cross-platform mobile applications; covers cross-platform and native-layer controls as applied through the JavaScript bridge |
| [`languages/flutter.md`](languages/flutter.md) | Flutter / Dart cross-platform mobile applications; covers cross-platform and native-layer controls as applied through Flutter's platform-channel bridge |
| [`languages/dotnet-maui.md`](languages/dotnet-maui.md) | .NET MAUI (and Blazor Hybrid) cross-platform mobile applications; covers cross-platform and native-layer controls as applied through MAUI's handler architecture and the Mono / .NET runtime |
| [`languages/capacitor-ionic.md`](languages/capacitor-ionic.md) | Capacitor / Ionic (WebView-based hybrid) cross-platform mobile applications; covers cross-platform and native-layer controls as applied through Capacitor's WebView and plugin architecture; carries forward web-stack rules from [`languages/typescript.md`](languages/typescript.md) and `core/owasp.md` because the WebView is the application UI |
| [`aiqt-rules/aiqt/00-project-integrity.md`](aiqt-rules/aiqt/00-project-integrity.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-citation-from-opened-file.md`](aiqt-rules/aiqt/10-ACCUR-citation-from-opened-file.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-claims-rest-on-observation.md`](aiqt-rules/aiqt/10-ACCUR-claims-rest-on-observation.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-completeness-claim-enumerates-its-set.md`](aiqt-rules/aiqt/10-ACCUR-completeness-claim-enumerates-its-set.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-corroborate-external-claims.md`](aiqt-rules/aiqt/10-ACCUR-corroborate-external-claims.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-count-carries-its-predicate.md`](aiqt-rules/aiqt/10-ACCUR-count-carries-its-predicate.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-disclose-guard-residuals.md`](aiqt-rules/aiqt/10-ACCUR-disclose-guard-residuals.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-evidence-grounded-completion.md`](aiqt-rules/aiqt/10-ACCUR-evidence-grounded-completion.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-guard-input-soundness.md`](aiqt-rules/aiqt/10-ACCUR-guard-input-soundness.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-measured-and-estimated-figures-stay-separate.md`](aiqt-rules/aiqt/10-ACCUR-measured-and-estimated-figures-stay-separate.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-no-fabrication.md`](aiqt-rules/aiqt/10-ACCUR-no-fabrication.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-observe-before-asserting-behaviour.md`](aiqt-rules/aiqt/10-ACCUR-observe-before-asserting-behaviour.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-partial-read-is-not-the-whole.md`](aiqt-rules/aiqt/10-ACCUR-partial-read-is-not-the-whole.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-read-before-characterizing.md`](aiqt-rules/aiqt/10-ACCUR-read-before-characterizing.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-reference-capture.md`](aiqt-rules/aiqt/10-ACCUR-reference-capture.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-reproduce-before-fix.md`](aiqt-rules/aiqt/10-ACCUR-reproduce-before-fix.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-timestamp-from-clock.md`](aiqt-rules/aiqt/10-ACCUR-timestamp-from-clock.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-validate-inference-before-action.md`](aiqt-rules/aiqt/10-ACCUR-validate-inference-before-action.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-ACCUR-verify-fix-in-commit.md`](aiqt-rules/aiqt/10-ACCUR-verify-fix-in-commit.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-anything-wrong-fixed-first.md`](aiqt-rules/aiqt/10-INTEG-anything-wrong-fixed-first.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-attestation-is-harness-owned.md`](aiqt-rules/aiqt/10-INTEG-attestation-is-harness-owned.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-branch-and-merge-on-green.md`](aiqt-rules/aiqt/10-INTEG-branch-and-merge-on-green.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-branch-rooted-on-live-main.md`](aiqt-rules/aiqt/10-INTEG-branch-rooted-on-live-main.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-check-fails-closed-on-unreadable.md`](aiqt-rules/aiqt/10-INTEG-check-fails-closed-on-unreadable.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-commit-identity.md`](aiqt-rules/aiqt/10-INTEG-commit-identity.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-explicit-binding-over-ambient-context.md`](aiqt-rules/aiqt/10-INTEG-explicit-binding-over-ambient-context.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-gate-discipline.md`](aiqt-rules/aiqt/10-INTEG-gate-discipline.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-generated-artefact-source-only.md`](aiqt-rules/aiqt/10-INTEG-generated-artefact-source-only.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-licence-compatibility.md`](aiqt-rules/aiqt/10-INTEG-licence-compatibility.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-no-concealed-failure.md`](aiqt-rules/aiqt/10-INTEG-no-concealed-failure.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-preserve-uncommitted-work.md`](aiqt-rules/aiqt/10-INTEG-preserve-uncommitted-work.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-protected-branch-integrity.md`](aiqt-rules/aiqt/10-INTEG-protected-branch-integrity.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-required-step-remains-required.md`](aiqt-rules/aiqt/10-INTEG-required-step-remains-required.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-rerun-pass-is-still-failure.md`](aiqt-rules/aiqt/10-INTEG-rerun-pass-is-still-failure.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-review-in-flight-pins-its-artefact.md`](aiqt-rules/aiqt/10-INTEG-review-in-flight-pins-its-artefact.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-safe-retries.md`](aiqt-rules/aiqt/10-INTEG-safe-retries.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-separate-task-changes.md`](aiqt-rules/aiqt/10-INTEG-separate-task-changes.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-stage-then-promote-on-green.md`](aiqt-rules/aiqt/10-INTEG-stage-then-promote-on-green.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-track-launched-work.md`](aiqt-rules/aiqt/10-INTEG-track-launched-work.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-validation-gates-apply.md`](aiqt-rules/aiqt/10-INTEG-validation-gates-apply.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-INTEG-workers-produce-inert-data.md`](aiqt-rules/aiqt/10-INTEG-workers-produce-inert-data.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-absolute-paths.md`](aiqt-rules/aiqt/10-QUALI-absolute-paths.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-change-carries-check.md`](aiqt-rules/aiqt/10-QUALI-change-carries-check.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-compatibility-or-migration.md`](aiqt-rules/aiqt/10-QUALI-compatibility-or-migration.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-confirm-execution-target.md`](aiqt-rules/aiqt/10-QUALI-confirm-execution-target.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-defence-in-depth-default.md`](aiqt-rules/aiqt/10-QUALI-defence-in-depth-default.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-elapsed-aware-timer-restore.md`](aiqt-rules/aiqt/10-QUALI-elapsed-aware-timer-restore.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-findings-are-fixed-not-argued.md`](aiqt-rules/aiqt/10-QUALI-findings-are-fixed-not-argued.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-goal-fidelity-across-trajectory.md`](aiqt-rules/aiqt/10-QUALI-goal-fidelity-across-trajectory.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-high-assurance-verification.md`](aiqt-rules/aiqt/10-QUALI-high-assurance-verification.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-kill-timeout-exceeds-callee-wait.md`](aiqt-rules/aiqt/10-QUALI-kill-timeout-exceeds-callee-wait.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-lightweight-verifier-workers.md`](aiqt-rules/aiqt/10-QUALI-lightweight-verifier-workers.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-match-surrounding-code.md`](aiqt-rules/aiqt/10-QUALI-match-surrounding-code.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-minimize-dependencies.md`](aiqt-rules/aiqt/10-QUALI-minimize-dependencies.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-self-guardrail-from-error.md`](aiqt-rules/aiqt/10-QUALI-self-guardrail-from-error.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-smallest-correct-change.md`](aiqt-rules/aiqt/10-QUALI-smallest-correct-change.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-surface-counterproductive-instructions.md`](aiqt-rules/aiqt/10-QUALI-surface-counterproductive-instructions.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-test-hermeticity.md`](aiqt-rules/aiqt/10-QUALI-test-hermeticity.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-verifier-delivery-completeness.md`](aiqt-rules/aiqt/10-QUALI-verifier-delivery-completeness.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-QUALI-verifier-diversity.md`](aiqt-rules/aiqt/10-QUALI-verifier-diversity.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-ai-toolchain-register.md`](aiqt-rules/aiqt/10-TRUST-ai-toolchain-register.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-assess-advise-discussion-only.md`](aiqt-rules/aiqt/10-TRUST-assess-advise-discussion-only.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-atomic-claim-from-pool.md`](aiqt-rules/aiqt/10-TRUST-atomic-claim-from-pool.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-change-record.md`](aiqt-rules/aiqt/10-TRUST-change-record.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-change-tracking-ext.md`](aiqt-rules/aiqt/10-TRUST-change-tracking-ext.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-clarify-before-acting.md`](aiqt-rules/aiqt/10-TRUST-clarify-before-acting.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-concurrency-lease.md`](aiqt-rules/aiqt/10-TRUST-concurrency-lease.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-continue-by-default.md`](aiqt-rules/aiqt/10-TRUST-continue-by-default.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-express-authorization-before-execution.md`](aiqt-rules/aiqt/10-TRUST-express-authorization-before-execution.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-human-oversight-and-autonomy-threshold.md`](aiqt-rules/aiqt/10-TRUST-human-oversight-and-autonomy-threshold.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-no-console-diff-dumps.md`](aiqt-rules/aiqt/10-TRUST-no-console-diff-dumps.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-orchestrator-mistakes-register.md`](aiqt-rules/aiqt/10-TRUST-orchestrator-mistakes-register.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-reconcile-record-against-reality.md`](aiqt-rules/aiqt/10-TRUST-reconcile-record-against-reality.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-records-first.md`](aiqt-rules/aiqt/10-TRUST-records-first.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-session-close-on-green.md`](aiqt-rules/aiqt/10-TRUST-session-close-on-green.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-session-resume-from-handoff.md`](aiqt-rules/aiqt/10-TRUST-session-resume-from-handoff.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-standing-constraints-persist.md`](aiqt-rules/aiqt/10-TRUST-standing-constraints-persist.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-trust-recovery-escalation.md`](aiqt-rules/aiqt/10-TRUST-trust-recovery-escalation.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/10-TRUST-trust-recovery-ext.md`](aiqt-rules/aiqt/10-TRUST-trust-recovery-ext.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/20-PROGR-decision-classification-before-enacting.md`](aiqt-rules/aiqt/20-PROGR-decision-classification-before-enacting.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/20-PROGR-repeated-failure-triggers-premise-review.md`](aiqt-rules/aiqt/20-PROGR-repeated-failure-triggers-premise-review.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/30-SPEED-background-work-during-ci-waits.md`](aiqt-rules/aiqt/30-SPEED-background-work-during-ci-waits.md) | Apache-2.0; All activities |
| [`aiqt-rules/aiqt/40-COST-cost-tier.md`](aiqt-rules/aiqt/40-COST-cost-tier.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECA-resource-bounds.md`](aiqt-rules/security/SECA-resource-bounds.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECA-verified-restore-path.md`](aiqt-rules/security/SECA-verified-restore-path.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-data-boundary.md`](aiqt-rules/security/SECC-data-boundary.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-egress-destinations.md`](aiqt-rules/security/SECC-egress-destinations.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-keep-secrets-out.md`](aiqt-rules/security/SECC-keep-secrets-out.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-least-privilege-retrieval.md`](aiqt-rules/security/SECC-least-privilege-retrieval.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-no-cross-context-bleed.md`](aiqt-rules/security/SECC-no-cross-context-bleed.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-no-hidden-context-disclosure.md`](aiqt-rules/security/SECC-no-hidden-context-disclosure.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECC-rotate-leaked-secret.md`](aiqt-rules/security/SECC-rotate-leaked-secret.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-authentication.md`](aiqt-rules/security/SECI-authentication.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-authorization.md`](aiqt-rules/security/SECI-authorization.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-config-is-executable-trust-gate.md`](aiqt-rules/security/SECI-config-is-executable-trust-gate.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-cryptography.md`](aiqt-rules/security/SECI-cryptography.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-dependency-provenance.md`](aiqt-rules/security/SECI-dependency-provenance.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-fail-closed.md`](aiqt-rules/security/SECI-fail-closed.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-federated-identity-flow.md`](aiqt-rules/security/SECI-federated-identity-flow.md) | Apache-2.0; `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**` |
| [`aiqt-rules/security/SECI-file-upload-handling.md`](aiqt-rules/security/SECI-file-upload-handling.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-guardrail-config-integrity.md`](aiqt-rules/security/SECI-guardrail-config-integrity.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-human-authorization.md`](aiqt-rules/security/SECI-human-authorization.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-input-validation.md`](aiqt-rules/security/SECI-input-validation.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-inter-agent-trust.md`](aiqt-rules/security/SECI-inter-agent-trust.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-key-management.md`](aiqt-rules/security/SECI-key-management.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-least-privilege-tools.md`](aiqt-rules/security/SECI-least-privilege-tools.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-log-redaction.md`](aiqt-rules/security/SECI-log-redaction.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-operator-deception.md`](aiqt-rules/security/SECI-operator-deception.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-output-encoding.md`](aiqt-rules/security/SECI-output-encoding.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-output-handling.md`](aiqt-rules/security/SECI-output-handling.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-pin-referenced-instructions.md`](aiqt-rules/security/SECI-pin-referenced-instructions.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-poisoning-resistance.md`](aiqt-rules/security/SECI-poisoning-resistance.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-prefer-removing-a-path.md`](aiqt-rules/security/SECI-prefer-removing-a-path.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-preview-has-no-side-effects.md`](aiqt-rules/security/SECI-preview-has-no-side-effects.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-prompt-trust-hierarchy.md`](aiqt-rules/security/SECI-prompt-trust-hierarchy.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-protect-audit-records.md`](aiqt-rules/security/SECI-protect-audit-records.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-reject-vulnerable-versions.md`](aiqt-rules/security/SECI-reject-vulnerable-versions.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-release-integrity.md`](aiqt-rules/security/SECI-release-integrity.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-safe-deserialization.md`](aiqt-rules/security/SECI-safe-deserialization.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-secure-configuration.md`](aiqt-rules/security/SECI-secure-configuration.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-security-logging.md`](aiqt-rules/security/SECI-security-logging.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-session-token-management.md`](aiqt-rules/security/SECI-session-token-management.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-ssrf-prevention.md`](aiqt-rules/security/SECI-ssrf-prevention.md) | Apache-2.0; `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**` |
| [`aiqt-rules/security/SECI-symlink-resolution.md`](aiqt-rules/security/SECI-symlink-resolution.md) | Apache-2.0; `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**` |
| [`aiqt-rules/security/SECI-threat-model-boundaries.md`](aiqt-rules/security/SECI-threat-model-boundaries.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-tool-argument-validation.md`](aiqt-rules/security/SECI-tool-argument-validation.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-untrusted-content.md`](aiqt-rules/security/SECI-untrusted-content.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECI-verify-dependency-exists.md`](aiqt-rules/security/SECI-verify-dependency-exists.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECP-data-minimization.md`](aiqt-rules/security/SECP-data-minimization.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECP-data-residency-retention.md`](aiqt-rules/security/SECP-data-residency-retention.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECP-purpose-limitation.md`](aiqt-rules/security/SECP-purpose-limitation.md) | Apache-2.0; All activities |
| [`aiqt-rules/security/SECP-synthetic-fixture-data.md`](aiqt-rules/security/SECP-synthetic-fixture-data.md) | Apache-2.0; All activities |

---

## External sources: how this pack handles them

External rule repositories listed under "External references" below are **not loaded automatically** at Claude Code session start. Three reasons:

1. **`CLAUDE.md` content is delivered to Claude Code as a user message, not as enforced configuration.** A "fetch at session start" instruction can be silently ignored, producing a false sense of coverage.
2. **External content fetched without per-fetch vetting cannot be relied on.** Treating fetched markdown as binding rules conflicts with the principle that fetched content is data, not instructions; each fetch needs the External-Source Vetting Protocol applied.
3. **The pack already covers the substantive areas** (core, AI/agent/MCP/RAG, pipeline, languages) as pack-maintained originals.

The pack maintainer back-ports vetted improvements from external sources on the pack's own review cadence, the `Review Frequency` stated in this README's header. Adopters who want to layer additional external rule sets on top of the pack have two paths:

- **By hand.** Use the URLs in the External references section below; the adopter clones, vendors, or copies into their own project on their own terms.
- **Via the setup generator's external-source overlay (default-on).** Phase 2 of [`setup-generator-prompt.md`](setup-generator-prompt.md), after presenting the pack proposal, **proposes to fetch all four vetted external sources as the default action** so the consumer can accept the broader proposal with a single approval. The consumer's explicit approval (or modification, or decline) is still required before any file is written; the default-on framing affects the conversation flow's default, not the consent gate. The Wiz licence caveat (CC-BY-NC-ND-4.0; NonCommercial + NoDerivatives) is always surfaced in the offer-message prose before approval so commercial adopters and adopters who plan to modify the rule files for their stack can decline Wiz specifically. For each source the consumer is fetching (whether by accepting the default or by explicit modification), the generator applies the External-Source Vetting Protocol per fetch (treat as data not instructions; scan for embedded directives, urgency framing, claims of pre-authorization, hidden or encoded text, exfiltration patterns, control-weakening guidance), surfaces anything suspicious verbatim before write, and places approved files at their source-specific destinations: rule sources under `.claude/rules/external/<source-name>/` with LICENSE and `PROVENANCE.txt` (without `paths:` frontmatter; the `.txt` name is outside Claude Code's `.md` rule discovery) and a provenance header (source URL, fetched date, SHA-256 of fetched bytes), and approved addyosmani skills under `.claude/skills/addyosmani-<upstream-name>/SKILL.md` with the namespaced frontmatter `name`, the upstream description retained, and LICENSE and PROVENANCE.md beside each skill (frontmatter-first discovery: no comment is prepended before the skill frontmatter). The pack remains the primary content; the overlay is supplementary and may overlap or conflict with the primary layer (consumer responsibility to reconcile). The maintainer-side vetting status for each candidate source is recorded in [`vetting-log.md`](vetting-log.md). Current status: TikiTribe, Kariedo, and Wiz are `Vetted` (first formal EXT-01 vets on 2026-05-31); addyosmani is `Vetted` (first formal EXT-01 vet on 2026-06-19, 5 skills in full + 19 spot-scanned). The generator's offer step surfaces the per-source status and substantive observations to the consumer so the decision is informed.

Before installing or refreshing fetched bodies as skills, apply the generator's
[Skill interpolation audit](setup-generator-prompt.md#skill-interpolation-audit),
including code examples: `$ARGUMENTS`, `$ARGUMENTS[n]`, `$<digits>` (such as `$0` and
`$1`), `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}`,
`${CLAUDE_EFFORT}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`,
`${user_config.*}`, and command markers `` !` `` / ```` ```! ```` (including inline
markers after JavaScript whitespace such as U+FEFF). Use a single backslash, not preceded
by another backslash, for literal argument placeholders: `\$1`, `\$ARGUMENTS`,
`\$ARGUMENTS[0]`. Rewrite active context substitutions and command markers; that escape
does not protect them. Re-scan before placement, retain the original fetched-byte hash,
and record adaptations in PROVENANCE.md. Keep `name`/`description`-only frontmatter;
additional fields (especially `arguments`) or a Claude Code upgrade require a fresh audit.

### Deterministic enforcement layer

`CLAUDE.md` and `.claude/rules/*.md` are the behavioural guidance layer. For controls that must hold regardless of what Claude decides, use `.claude/settings.json` `permissions.deny` rules and `PreToolUse` hooks. Consult the current official Claude Code documentation for the supported settings and hook schemas.

Python hook launchers in the parent GRC library use `/usr/bin/python3 -I`.
Adopters must set their own absolute interpreter path in every command in
`.claude/settings.json` if Python lives elsewhere, for example
`/opt/reviewed/python3.12 -I "$CLAUDE_PROJECT_DIR"/.claude/hooks/clock-inject.py`.
Keep the basename `python3` or `python3.N` and the isolation flag; bare
`python3`, `PATH=`, loader-related assignments and shell wrappers are refused.
The only modelled assignment is `ORCH_LEASE_FILE="$CLAUDE_PROJECT_DIR"/literal/path`:
the name and equals sign are unquoted, and the exact double-quoted prefix is
immediately followed by a literal path. Both clock commands retain
`ORCH_LEASE_FILE="$CLAUDE_PROJECT_DIR"/../private/session-state.md` so session elapsed
time works outside the project. The unused `ORCH_STORE_ROOT` assignment is dropped.
Children inherit the selected absolute interpreter through
`sys.executable` and also use `-I`.

Use a literal script path starting with exactly
`"$CLAUDE_PROJECT_DIR"/.claude/hooks/` followed by a literal path. The shipped
commands use this anchor and work from any directory when the harness sets
`CLAUDE_PROJECT_DIR` to the absolute project root. The reviewed loader still
refuses a symlinked project root or hook/helper path. Such a refusal exits 2, which
blocks every PreToolUse call and every turn end while it persists; launch the
harness from the real (non-symlinked) project path.
Every token after the script is checked too. Expansions are allowed only in the
script anchor and the modelled lease assignment above. All other expansions,
redirections (including here-strings and fd duplication), `-X`, `-W`, `-c`, `-m`
and stdin scripts are refused. Relative script paths are refused. Check the configuration
with `python3 tools/lint-hooks-syntax.py --launcher-isolation` before starting
a new session. Gate 95's default syntax check remains separate.

Stop's optional producer must be a Python producer, launched with the same
interpreter and `-I`; a shell producer needs an explicitly reviewed adapter.
Missing or refused backlog-tool helpers leave the producer indeterminate and
Stop fail-open. Each emits a one-line stderr notice naming the helper and reason;
Stop uses its existing bounded diagnostic transport.

## Generate your files (AI-assisted setup)

[`setup-generator-prompt.md`](setup-generator-prompt.md) is a portable prompt for your own Claude Code session. It analyzes your project, proposes a tailored setup, and creates files only after your approval; it does not act blindly.

### Local mode vs fetch mode

The generator works whether or not you have the pack on disk:

- **Local mode** (when the generator's probe finds a local pack on disk, at `guardrails/` in your project root or in one of the nearby locations it checks): reads pack content from disk. The generator fetches only [`guardrails/README.md`](README.md) from the canonical source to compare versions and warn you if your local pack is stale.
- **Fetch mode** (when no local pack is detected, or you elect it after a staleness check): reads the pack live from the GRC Library's first-party canonical source on every needed file. No local download required. **Default canonical URL prefix**: `https://raw.githubusercontent.com/jposluns/grc_library/main/guardrails/`. The generator asks you to confirm or substitute this URL before any fetch, so the trust decision is explicit. If you have forked the GRC Library to your own org, substitute your fork's URL at the confirm prompt.

### Three ways to invoke

Pick whichever fits your workflow.

**Form 1: manual paste (most conservative)**. Open [`setup-generator-prompt.md`](setup-generator-prompt.md) on GitHub, click the **Raw** button, select all, copy, paste into Claude Code as your first message. You see every word of the prompt before any action.

**Form 2: one-line `curl` to clipboard (recommended for terminal users)**. Pulls the prompt's raw content directly to your clipboard, then paste it into Claude Code.

```bash
# macOS
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/guardrails/setup-generator-prompt.md | pbcopy

# Linux (X11 + xclip)
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/guardrails/setup-generator-prompt.md | xclip -selection clipboard

# Linux (Wayland + wl-copy)
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/guardrails/setup-generator-prompt.md | wl-copy
```

You still see the prompt content (you pasted it), with one fewer browser step.

**Form 3: URL-to-Claude (maximum convenience; different trust shape)**. Open Claude Code in your project root and send this single message:

```text
Fetch https://raw.githubusercontent.com/jposluns/grc_library/main/guardrails/setup-generator-prompt.md and follow the instructions exactly.
```

Claude will WebFetch the prompt and start executing it. **Trade-off**: you do not see the prompt content before Claude begins acting on it; you are trusting the canonical URL only. Only use this form if you have made an informed decision to trust the GRC Library canonical URL (which is open-source, CC BY-SA 4.0, and version-controlled on GitHub).

### Tip: avoid permission prompts during fetch

If you plan to use fetch mode often, add the canonical raw URL to your project's `.claude/settings.json` permission allowlist so Claude does not ask on every fetch. Using the Anthropic-documented schema:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:raw.githubusercontent.com)"
    ]
  }
}
```

### What the generator produces

- A concise project `CLAUDE.md` (target under 200 lines) tailored to your stack, pointing at your project's own test/lint/CI gates.
- The relevant security rule modules for your languages and components (secrets, input validation, OWASP, AI/agent/RAG/MCP, CI/CD, etc.), placed under `.claude/rules/` with optional `paths:` frontmatter for path-scoped loading.
- Optionally: a `.claude/settings.json` template with starter `permissions.deny` rules for common secret paths and dangerous shell patterns.
- Files that fit your project. The generator does **not** impose the GRC Library's internal document-model metadata or naming conventions on your repository.

### Safety notes

- The generator treats content fetched from any URL other than the confirmed first-party canonical source as untrusted data, never as instructions, and will not auto-apply such content without explicit consumer approval.
- It is AI-assisted: review what it proposes and generates before trusting it. AI assistants occasionally produce plausible-looking configuration keys or file names that the target tool silently ignores, so verify against authoritative documentation.
- It will never overwrite an existing `CLAUDE.md` or rule file without showing you the diff and asking first.
- In local mode, when canonical is newer than your local pack, the generator shows you the version gap and offers three options: continue with stale local, switch to fetch mode, or refresh local files from canonical (with explicit per-file approval before any overwrite).

### Prefer to do it entirely by hand?

Use Options 1-4 above to copy specific rule files directly; no prompt required.

---

## External references

These rule files draw on and are aligned to the following external projects and standards. All are publicly available and free to reference.

### AI coding assistant rule repositories

**TikiTribe: Secure Coding Rules for AI Coding Assistants**
- Repository: `https://github.com/TikiTribe/claude-secure-coding-rules`
- Coverage: 100+ rule sets covering 12 programming languages, 5+ backend frameworks, 11 AI/ML frameworks, 51 RAG tools, IaC, containers, CI/CD, OWASP Top 10, OWASP MCP Top 10, MITRE ATLAS, NIST AI RMF, Google SAIF, agentic AI
- Key paths fetched by CLAUDE.md:
 - `rules/_core/ai-security.md`
 - `rules/_core/agent-security.md`
 - `rules/_core/mcp-security.md`
 - `rules/_core/rag-security.md`
- Integration: Treat TikiTribe's defensive secure-coding rules as preventive controls alongside the project's adversarial-testing guidance, not as a source of adversarial test cases

**Wiz: Secure Rules Files**
- Repository: `https://github.com/wiz-sec-public/secure-rules-files`
- Coverage: Baseline rules compatible with Claude, Cursor, and Copilot; organized by programming language and framework; open source; AI-generated and human-verified
- Use: Language-specific rules as a second layer over this pack's language files

**Kariedo: Claude Code Security Rules**
- Repository: `https://github.com/kariedo/claude-code-security-rules`
- Coverage: Core universal security practices, language-specific rules (Python, JavaScript, Java, PHP, Ruby, Rust, C), common vulnerability prevention, uses `@`-syntax import system for modular organization
- Use: Alternative modular rule set for projects needing broader language coverage

**addyosmani: Agent Skills**
- Repository: `https://github.com/addyosmani/agent-skills`
- Coverage: 24 engineering-workflow skills organized by development phase (Define, Plan, Build, Verify, Review, Ship). Includes a `security-and-hardening` skill (STRIDE-per-trust-boundary, Mandatory / Approval-Gated / Prohibited tier model, OWASP prevention patterns, LLM-output handling), a `code-review-and-quality` skill (five-axis review), and a `ci-cd-and-automation` skill (quality-gate pipeline configuration)
- Use: Complementary engineering-discipline overlay; scope is engineering workflow not GRC governance. Uses Claude Code's Skills `SKILL.md` discovery format (frontmatter `name:` + `description:`) rather than the rule / `@`-import patterns the other three sources use
- License: **MIT**
- Local installation in this repository: five of the upstream skills (`ci-cd-and-automation`, `code-review-and-quality`, `context-engineering`, `security-and-hardening`, `using-agent-skills`) are installed under `.claude/skills/addyosmani-<name>/SKILL.md`, each with the `addyosmani-` prefix on its frontmatter `name`, the upstream description retained, the body preserved except for documented interpolation escapes or rewrites, and LICENSE and PROVENANCE.md beside the skill. These five locally installed skills are distinct from upstream's larger skill collection and from the first-party pack skill collection

**awesome-claude-code (community curation)**
- Repository: `https://github.com/hesreallyhim/awesome-claude-code`
- Coverage: Community-curated index of Claude Code skills, hooks, slash commands, agent orchestrators, applications, and plugins
- Use: Discovery resource for additional skills/hooks/MCP integrations beyond the security-rules scope of this pack

---

### OWASP projects

**OWASP Top 10 for Web Applications (2025 current; 2021 superseded)**
- URL: `https://owasp.org/www-project-top-10/`
- Direct application: [`core/owasp.md`](core/owasp.md)

**OWASP Top 10 for Large Language Model Applications (2026)**
- URL: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md), [`ai/rag-security.md`](ai/rag-security.md)

**OWASP MCP Top 10 (Model Context Protocol)**
- URL: `https://owasp.org/www-project-mcp-top-10/`
- Direct application: [`ai/mcp-security.md`](ai/mcp-security.md), [`core/owasp.md`](core/owasp.md)

**OWASP Application Security Verification Standard (ASVS) v5.0.0**
- URL: `https://owasp.org/projects/asvs`
- Direct application: [`core/owasp.md`](core/owasp.md), [`core/authentication.md`](core/authentication.md), [`core/cryptography.md`](core/cryptography.md)

**OWASP Cheat Sheet Series**
- URL: `https://cheatsheetseries.owasp.org/`
- Use: Fetch the cheat sheet for specific security topics during development sessions

**OWASP Software Assurance Maturity Model (SAMM)**
- URL: `https://owasp.org/www-project-samm/`
- Use: Programme-level maturity assessment for development security practices

**OWASP Web Security Testing Guide (WSTG)**
- URL: `https://owasp.org/www-project-web-security-testing-guide/`
- Use: Testing methodology reference for manual security testing

---

### NIST frameworks

**NIST SSDF: Secure Software Development Framework (SP 800-218)**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/final`
- Coverage: Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV)
- Direct application: all rule files in `core/` and `pipeline/`

**NIST SP 800-218A: Generative AI Profile**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/a/final`
- Coverage: Augments SP 800-218 with AI model development practices; AI-specific secure development tasks
- Direct application: all rule files in `ai/`

**NIST AI Risk Management Framework (AI RMF 1.0)**
- URL: `https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf`
- Coverage: Govern, Map, Measure, Manage functions for AI systems
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md)

---

### MITRE frameworks

**MITRE ATLAS (Adversarial Threat Landscape for AI Systems)**
- URL: `https://atlas.mitre.org/`
- Coverage: 16 tactics and 84+ techniques for AI-specific attacks (data poisoning, adversarial examples, prompt injection, model extraction, ML supply chain)
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md), [`ai/rag-security.md`](ai/rag-security.md), [`ai/mcp-security.md`](ai/mcp-security.md)

**MITRE CWE Top 25 Most Dangerous Software Weaknesses**
- URL: `https://cwe.mitre.org/top25/`
- Coverage: Annual list of the most dangerous software weaknesses based on CVE data
- Direct application: [`core/input-validation.md`](core/input-validation.md), [`core/cryptography.md`](core/cryptography.md)

---

### Government and standards body guidance

**CISA Secure by Design**
- URL: `https://www.cisa.gov/resources-tools/resources/secure-by-design`
- Coverage: Three principles: take ownership of customer security outcomes, embrace radical transparency, lead from the top; shift-left approach; secure default configuration
- Direct application: [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md), [`core/owasp.md`](core/owasp.md)

**SLSA: Supply-chain Levels for Software Artifacts**
- URL: `https://slsa.dev/`
- Coverage: v1.2; a Build track (L0 to L3: build-platform trustworthiness and provenance) and a Source track (L1 to L4: source history and provenance, enforced organizational controls, and code review)
- Direct application: [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md), [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md)

**Google Secure AI Framework (SAIF)**
- URL: `https://saif.google/`
- Coverage: Secure development, deployment, and monitoring for AI systems; mitigates model stealing, data poisoning, prompt injection, and information extraction
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md)

**CIS Benchmarks**
- URL: `https://www.cisecurity.org/cis-benchmarks`
- Coverage: Consensus-based configuration baselines for OS, containers, cloud platforms, databases, and network devices
- Use: Reference for hardening production environments where AI-assisted code is deployed

---

### Cloud security alliance

**CSA Cloud Controls Matrix (CCM) v4.1.0**
- URL: `https://cloudsecurityalliance.org/research/cloud-controls-matrix/`
- Coverage: 207 controls across 17 domains
- Direct application: framework alignment tables in all `core/` rule files

**CSA AI Controls Matrix (AICM) v1.1.0**
- URL: `https://cloudsecurityalliance.org/research/ai-controls-matrix/`
- Coverage: 247 controls across 18 domains (CCM's 17 plus the AI-specific Model Development and Security (MDS) domain)
- Direct application: framework alignment tables in all `ai/` rule files

---

## Parent-repo dependencies

This pack is documentation and operational discipline; three things it references live in the parent grc_library repository, not inside `guardrails/`, and do not travel when the pack is dragged into another project as a standalone bundle. A standalone adopter should know:

- **The audit toolchain.** The gates this pack documents (the `tools/` linters and audits, run by the parent repository's CI and pre-commit config) are parent-repo tooling; they are named here for provenance but are not shipped in the pack. An adopter who wants the mechanical enforcement installs the parent repository or reimplements the gates; the rules themselves apply without them.
- **The project slash commands.** The review cadences the pack refers to (for example validate, validate-pr, matrix-fit, claim-fit, reference-audit, screen-publications, deep-assessment, high-assurance, adopt, and the workflow commands) are project commands defined in the parent repository's `.claude/commands/`, with the corresponding skill bodies shipping in this pack under `skills/` (the `guardrails/skills/` tree), not Claude Code built-ins. Where a pack skill ships a `SKILL.md`, that skill body already provides the `/name` behaviour; the remaining command stubs are parent-only, and an adopter who wants them installs the parent repository.
- **The private reference base.** The citation and control-code cadences (matrix-fit, claim-fit, reference-audit, screen-publications, and deep-assessment) check corpus claims against a held reference base that is not redistributable and does not ship with the pack. An adopter either builds a reference base of their own or runs those cadences in a structure-only mode that checks form without adjudicating against held source text.

---

## Licence

GRC-original material is released under CC BY-SA 4.0. The upstream-owned `aiqt-rules/` snapshot and its runtime copies are separately Apache-2.0; preserve its verbatim LICENSE and NOTICE.

External repositories (TikiTribe, Kariedo, addyosmani, Wiz) maintain their own licenses: check each repository before redistribution.

---

**End of Document**
