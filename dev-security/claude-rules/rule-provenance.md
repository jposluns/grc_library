# Rule provenance register: the origin of each governance rule

**Document Type:** Provenance register\
**Version:** 1.1.0\
**Date:** 2026-07-12\
**Owner:** Governance Library Maintainer\
**Repository Path:** [`dev-security/claude-rules/rule-provenance.md`](rule-provenance.md)\
**License:** CC BY-SA 4.0

---

## Purpose

Every governance rule in this pack comes out of the parent GRC library's
maintenance programme, but not all in the same way, and this register says which is
which. Some rules were earned directly from an incident: a failure happened, was
caught, and was codified so it could not silently recur. Others were codified up
front, in the pack's initial governance rollout, from failure classes the maintainer
set out to guard against before they occurred; several of those were later grounded
by real in-project events, and the entries below say so where the records support it.
The register exists so an adopting or forking maintainer can see how the rules grew,
and judge each rule's weight from the reality (or the deliberate design) behind it,
without inheriting the parent project's internal identifiers, records, or history.

Division of labour: this register is the adopter-facing summary. The rules
themselves carry only their operative core (the parent library moved the
why-narratives to its removal ledger, which carries the fuller stories), and the
parent's records remain the authority on detail; this register never supersedes
either, and the detailed lineage (specific changes, dates, registers) is
deliberately not restated here.

Entries are two to five sentences, narrative only. Where a date matters it is given at
month granularity; most entries need none.

This register lives in the `dev-security/claude-rules/` directory and, per the parent
library's exemption convention for this directory, carries the shorter header above
rather than the full corpus metadata block.

---

## Governance rules

### `gate-discipline`

Codified up front, in the pack's initial governance rollout, against the
best-known failure mode of any gated workflow: a failing check invites the fast
path (suppress the gate, skip the hook, lower the threshold, ship). Its original
rationale is a cost-asymmetry argument, not an incident record: the cost of fixing
the artefact is bounded, while the cost of a silenced gate compounds for every
future user. The rule fixes the response unconditionally: a failing gate is signal,
and the artefact gets fixed, with a slow, documented exception path for the
genuinely legitimate deviations.

### `change-tracking`

Codified up front for a documentation corpus where every document is a citable
artefact and "when did this change, and why" is asked months later, after the
original context is gone. The rule names silent changes, vague entries, and batched
retroactive entries as the classes that create archaeology cost, and forecloses
them by design: every change carries an entry, terse or substantive, with no skip
path. The two-file split (an adopter-facing summary and a maintainer-grade detailed
mirror) and the paired forward-looking-backlog and closed-work ledgers were then
grown and refined across the project's own run, as its version history records.

### `evidence-grounded-completion`

The pack's most-cited rule, created in the initial rollout to name the canonical
assistant failure in the abstract: declaring "done, all checks pass" from inference
rather than observation. The abstract failure then happened for real within weeks:
a multi-surface wiring change added a new audit gate to all but one of its parallel
declaration surfaces, and the session summarized the work as complete because the
audit "was passing earlier"; the omitted surface failed the next full run, and the
incident was memorialized as a worked example (now held, with the rest of the
narrative rationale, in the parent library's removal ledger). The verification protocol
(enumerate, re-read, quote, contradiction-search) is the rule's core; its
corollaries on un-observable state, inventory claims, and external-version currency
were added over the project's run as new assertion classes surfaced.

### `clarify-before-acting`

Codified up front against the silent authorial pick: a request with more than one
reasonable reading, resolved without surfacing the choice, discovered only when the
work has to be unwound. The rule's compute-first gate (retrieve a findable fact
instead of asking about it) was added later from a real event: a session asked the
maintainer to confirm a count the assistant had the tools to compute itself.

### `artefact-and-branch-discipline`

Codified up front against the two audit-trail failure classes every governed
corpus faces: hand-edits to generated artefacts (silently overwritten by the next
regeneration) and history rewrites on shared branches (breaking downstream clones
and the version-monotonicity contract). The rule fixes both as append-only
disciplines with narrow, documented exception paths.

### `action-before-explanation-of-inaction`

Added as the pack grew, to name the confidently-narrated-inaction failure mode:
the assistant explaining that an external action "is blocked" or "requires
approval" without having attempted it, where the attempt would have succeeded or
produced the real cause. The rule keys on the drafting moment (an inaction
explanation with no verifying attempt behind it) and pairs the safe-action protocol
with a strict name-and-ask protocol for destructive actions.

### `validate-inference-before-action`

Added in June 2026 after an inferred premise cascaded: a sweep orchestrator inferred
that nothing relevant had changed, skipped a reviewer on that basis, and the skipped
review would have caught a change that then required multiple follow-up fixes. The
rule requires a premise that drives an action to be validated by a concrete
observation first, because a wrong inference propagates into every downstream action
built on it.

### `ai-assistant-workflow-disciplines`

Distilled from a multi-week remediation campaign of thirty-plus changes driven by an
AI assistant with research workers in support. Each of the five disciplines encodes
one observed failure: worker confabulation (research-assistant discipline), serial
bottlenecks and state confusion (pipeline construction), stale worker claims caught at
apply time (apply-time correction), hard-to-review bundles (always split), and idle CI
waits (background work). The skeptical pre-push verification tiers were layered on
later, when change volume made an independent adversarial check before each push the
cheapest place to catch defects.

### `trust-recovery-escalation`

Earned the hard way: a session abbreviated a mandatory per-change QA step across
eleven consecutive changes, and the informal substitutes were invisible until the
maintainer caught the pattern. The recovery that followed (a forensic pass tuned to
AI failure classes, then a fresh-reader persona pass, every confirmed finding routed
with none dropped, terminating only on maintainer sign-off) was codified as the
escalation tier for any window of work whose process integrity is in question. Its
full-clone methodology rule was earned inside the first run, when a shallow clone
made history-aware gates emit a mass false positive.

### `project-integrity`

The apex rule, stating the ordering every other rule assumes: the non-negotiable tier
above speed, and speed above cost. It began as a quality-first ordering with integrity
non-negotiables and was renamed to the AIQT form (Accuracy, Integrity, Quality, Trust
as one co-equal top tier) in July 2026, at maintainer direction, so the facets that
were implicit became named and each maps to its enforcing machinery. Every clause in
its non-negotiables section traces to an observed pressure to trade correctness for
apparent completion.

### `surface-counterproductive-instructions`

Motivated by a literal reading that destroyed work: an instruction to wind down after
the current piece of work was taken to override newly-committed work, and the
committed work was reverted without a confirming question. The rule names the general
case (a clear instruction whose execution as given would be net-negative), requires
the concern to be surfaced once with named options, and forbids the silent
most-destructive-literal reading.

### `high-assurance-verification`

Earned during a wide, delicate reshape of a compliance mapping artefact whose
correctness no mechanical gate could check (a valid-looking control identifier can
still be the wrong control). The maintainer directed that integrity be produced by
independent rechecking rather than trusted to one careful pass; the resulting harness
(research fan-out, a mechanical pass over the negatives, two independent adversarial
verifiers, an invariant floor, a deterministic scripted apply with re-parse) caught
nine misses and three over-assignments a single pass had left standing, and was
codified with a persistent register so sensitive items survive session boundaries.

### `session-lifecycle`

The distillation of everything the parent project learned running multi-session AI
work: a wind-down instinct that was wrong far more often than right until it was
evidence-gated, an unattended run that idled overnight on a question its standing
priorities already answered, a handoff snapshot falsified by the very change that
refreshed it, and a double-resume risk identified before any
concurrency lease existed to guard it. The rule packages the resulting apparatus (durable handoff,
explicit operator-set modes, graceful degradation, the green-merge close with a
compensating control, the advisory lease) as one portable discipline.

---

## Procedure skills (origin notes)

The pack's skills wrap the rules above into runnable procedures; most inherit their
provenance from their `derives_from` rule. The ones with a distinct origin story:

- **matrix-fit**: created after a forensic pass found valid-but-wrong control codes
  (identifiers that exist in the right catalogue and are still the wrong control for
  the row) that no existence gate could catch; the semantic-fit cadence is the durable
  answer to that gate-blind class.
- **claim-fit**: created after a corpus sentence attributed a specific fixed value to
  named standards that do not prescribe one (the "attributed value, silent source"
  class); the precision cadence judges each attributed value against the held source
  text.
- **validation-sweep and its PR-scoped sibling**: grew from recurring small drift
  (stale counts, stale references) that per-change review kept missing; the sweep is
  the periodic instrument, the PR-scoped form its per-change companion.
- **deep-qa-review and library-fitness-review**: the two halves of the trust-recovery
  suite (see the trust-recovery-escalation entry above), kept as standing skills so
  the recovery instrument does not have to be reinvented under pressure.
- **reference-audit**: created when a maintainer-flagged case showed that nothing
  mechanical asks whether the corpus engages the best of the sources available to
  the project, in either direction, a class no citation gate can see; the breadth
  cadence is the standing answer to that question.
- **guardrail-review**: created when the project's own quality machinery had grown
  substantially across its rules, skills, and gates and nothing examined the
  machinery itself for overlap, gaps, and drift.
- **deep-assessment**: the rare-cadence, maintainer-invoked whole-project pass, born
  from the observation that the gates check the corpus and the skills check the gates'
  outputs, but nothing routinely examines the quality system from outside it.
- **validate-inference and surface-instruction-concern**: created together when a
  guardrail review found the derived-skill coverage gap: the two rules
  most often needed at a specific drafting moment (an unvalidated premise about to
  drive an action; a clear instruction about to execute a foreseeable harm) had no
  workflow wrapper, while weaker candidates did.
- **publication-screening**: created when an untrusted-publications bucket joined the
  reference base, as the admission-control layer for content that could otherwise
  steer authoring through bias or embedded instructions.

---

## Maintaining this register

When a rule or skill is added to the pack, add its entry here in the same change
(the skill-authoring discipline's parallel-surface step names this register as one
of its surfaces). Keep entries at this
register's granularity: the story, not the records. If an entry's event is ever needed
in full detail, the parent library's history and working records hold it.
