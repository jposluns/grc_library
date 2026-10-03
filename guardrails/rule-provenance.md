# Rule provenance register: the origin of each governance rule

**Document Type:** Provenance register\
**Version:** 1.2.6\
**Date:** 2026-10-02\
**Owner:** Governance Library Maintainer\
**Repository Path:** [`guardrails/rule-provenance.md`](rule-provenance.md)\
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

This register lives in the `guardrails/` directory and, per the parent
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
were added over the project's run as new assertion classes surfaced, joined on
2026-08-07 by the stated-intention section: a sentence about the actor's own next
action is a claim, so an intention stated and not carried out is a false statement.

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
cheapest place to catch defects. The commit-before-dispatch requirement (a QA verifier
is pinned to a revision, so the artefact under review must be committed before the
dispatch) was added in August 2026 after an expensive dual-family pass was dispatched
against an uncommitted artefact and bought one process finding and no content review.

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
above progress, progress above speed, and speed above cost. It began as a quality-first ordering with integrity
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

### `decision-classification-before-enacting`

Earned from a recurring failure the maintainer named directly: the assistant would DEFER a
queued or authorized item, or re-sequence, skip, or wind down, on an un-instrumented
internal-state justification ("heavy context", "too risky to do now", "better fresh later")
instead of either doing the work or asking. Deferral-with-no-question is worse than both valid
moves: it stalls the work and hands the maintainer nothing to act on, while dressing avoidance
up as prudence. The rule forces every point where work is about to NOT happen into exactly one
of three classifications (ACT, the default; ASK a specific named question while the maintainer
is reachable; or BLOCKED by a named, externally-observable blocker from a closed set), written
to the decision log BEFORE the decision is enacted so the classification is made at decision
time rather than rationalized after.

---

### `express-authorization-before-execution`

Up-front-codified against a named recurring failure the maintainer surfaced directly: a
conceptual or planning discussion, or a conditional / sequenced go ("deliver X, then wait,
then we proceed"), was repeatedly read as licence to begin executing work no authority had
expressly named. The rule holds the assistant in discussion mode (plans, candidate shapes,
questions, never edits or outward actions) until the responsible authority gives an express,
work-naming go, and treats a conditional go as authorizing only its first, unconditioned step.
Its closest kin is `decision-classification-before-enacting`, the act-boundary sibling: that
rule governs the decision to NOT do already-authorized work, and this one governs the mirror,
the decision to BEGIN work that is not yet authorized (it is that rule's ACT-branch entry
condition, an unauthorized start being an ASK, not an ACT). Convention-first, maintainer-directed
2026-07-23; a mechanical GO-ledger-keyed hook was considered and deliberately deferred.

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

## Pinned aiqt rules

<!-- AIQT-PROVENANCE-aiqt-BEGIN -->
### `00-project-integrity`

Upstream `.claude/rules/aiqt/00-project-integrity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `3cb951f3c0cbccc6a68feb7c6ba56ff0c02c27724c9aa665d7b87624b1c0fb3e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-citation-from-opened-file`

Upstream `.claude/rules/aiqt/10-ACCUR-citation-from-opened-file.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e3c4fb5b1fb13e8014beb2a81315090fbb37d38f8a9ee59485fe17b0c7b9ca39`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-claims-rest-on-observation`

Upstream `.claude/rules/aiqt/10-ACCUR-claims-rest-on-observation.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `81df92a591d35d1caa71e8cd27c352eeaf2037218c10e37f38b77e1513fa03ff`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-completeness-claim-enumerates-its-set`

Upstream `.claude/rules/aiqt/10-ACCUR-completeness-claim-enumerates-its-set.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `567f21bafa5e88a0b3dd305ea29b837d08e322107b77478cf278092913d0acea`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-corroborate-external-claims`

Upstream `.claude/rules/aiqt/10-ACCUR-corroborate-external-claims.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `14ecc6a4fa419a3b0b8223c9442b0f9c5ab7c32adeaa4e4a2b1fec1cf26b1fb9`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-count-carries-its-predicate`

Upstream `.claude/rules/aiqt/10-ACCUR-count-carries-its-predicate.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `b6b2317eccf36a090fa45ead79253aef1d4a53da999681873f0a201a4bb60d8f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-disclose-guard-residuals`

Upstream `.claude/rules/aiqt/10-ACCUR-disclose-guard-residuals.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `3b8bbb1a920a8c38d7763f6433eb457139c5dd814926559662dc8ffc0409271e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-evidence-grounded-completion`

Upstream `.claude/rules/aiqt/10-ACCUR-evidence-grounded-completion.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ef70b589312b5b37a02920f9f79e107265b806659c95e9ce529c931c26266161`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-guard-input-soundness`

Upstream `.claude/rules/aiqt/10-ACCUR-guard-input-soundness.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `8d21a518820de1d4b7f64f6551150a3eb020c9a40a2abc8bd7583a296b33549c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-measured-and-estimated-figures-stay-separate`

Upstream `.claude/rules/aiqt/10-ACCUR-measured-and-estimated-figures-stay-separate.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `2321618ff2db7ba71f4ae2cb7af4b88ee60e740faad4c51f3f176a8d352ff56a`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-no-fabrication`

Upstream `.claude/rules/aiqt/10-ACCUR-no-fabrication.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `45e14b4c516cbe6969867102c239f895e9047794a90231cf6a18b1db489f4a26`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-observe-before-asserting-behaviour`

Upstream `.claude/rules/aiqt/10-ACCUR-observe-before-asserting-behaviour.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7dacbce3d155aced6bcea0474834ca59907b4f4a38ba6556090fdb0ce6ec78e7`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-partial-read-is-not-the-whole`

Upstream `.claude/rules/aiqt/10-ACCUR-partial-read-is-not-the-whole.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `1c8eba842cf43ab8c8f2b8a6e691b967115f6f922cd264209644d3daa055ed1f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-read-before-characterizing`

Upstream `.claude/rules/aiqt/10-ACCUR-read-before-characterizing.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `0bc2aa52717e6ce8ab222b6009b650484484e7b658d99dc197a381611d518698`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-reference-capture`

Upstream `.claude/rules/aiqt/10-ACCUR-reference-capture.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `16771120832a089c77aa198360d27b1e1cd5e287fdb322ee0ffae42ddae0a3f2`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-reproduce-before-fix`

Upstream `.claude/rules/aiqt/10-ACCUR-reproduce-before-fix.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ba9cf2790a14e0b1b754fdd7924bf86b895c25043b9f2ee324579f9f8a568069`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-timestamp-from-clock`

Upstream `.claude/rules/aiqt/10-ACCUR-timestamp-from-clock.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `4cd20aa307683a46425e4c1e00f0da58ca05248f4a154fd771d6cf38430a1910`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-validate-inference-before-action`

Upstream `.claude/rules/aiqt/10-ACCUR-validate-inference-before-action.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `2981271ce9624a67f855d224b29fa51021e550b2a650b22c25223f3a70c91d3b`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-ACCUR-verify-fix-in-commit`

Upstream `.claude/rules/aiqt/10-ACCUR-verify-fix-in-commit.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `63e7417e1e0ea72fced7086898e2e459b933fdfe6fd364d00be009f73a07de50`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-anything-wrong-fixed-first`

Upstream `.claude/rules/aiqt/10-INTEG-anything-wrong-fixed-first.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7eae45965612b05da9802f2b211a4a58dba305f10b6e80e1514d09508b1d176c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-attestation-is-harness-owned`

Upstream `.claude/rules/aiqt/10-INTEG-attestation-is-harness-owned.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `dd3eab3381071080c059d31e998280fb3b29d5b07af6b3ea54a9ddbc7c8fa9b4`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-branch-and-merge-on-green`

Upstream `.claude/rules/aiqt/10-INTEG-branch-and-merge-on-green.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `0b6e3cffbdcb82c6d729fe68286c44db290ef6d55f172175b6db6e0edb87f905`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-branch-rooted-on-live-main`

Upstream `.claude/rules/aiqt/10-INTEG-branch-rooted-on-live-main.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f3197be5d8d73e4ea53880a44c227d390a9b4c08d99f4cc0d00bed8a29026024`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-check-fails-closed-on-unreadable`

Upstream `.claude/rules/aiqt/10-INTEG-check-fails-closed-on-unreadable.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `77b2e76a348f1468c55988ab1427e04511560c1479e0206aed88416deedacafd`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-commit-identity`

Upstream `.claude/rules/aiqt/10-INTEG-commit-identity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `04d66e54525d7ed4c8f1e7a1a5e7841e2fa6560430cdee4d2289a109614384d4`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-explicit-binding-over-ambient-context`

Upstream `.claude/rules/aiqt/10-INTEG-explicit-binding-over-ambient-context.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `42fadd1cf7769a4af1114d91d461114a1859e7fc3aee1fe5feb081e33e38bd79`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-gate-discipline`

Upstream `.claude/rules/aiqt/10-INTEG-gate-discipline.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `9a63652194fa01e678df4ee7043a086709382dbca362ae668691418535ca16c6`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-generated-artefact-source-only`

Upstream `.claude/rules/aiqt/10-INTEG-generated-artefact-source-only.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `42fb16d7257af3084dd556cd4ef4ac5053707ffd7aee70034843aab6673dfebc`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-licence-compatibility`

Upstream `.claude/rules/aiqt/10-INTEG-licence-compatibility.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `994e4425fa85075bfde2951bbd22c2fffd7e74da95b016ee61df4e462140a5b4`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-no-concealed-failure`

Upstream `.claude/rules/aiqt/10-INTEG-no-concealed-failure.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ee05fe9dd2edcba872cf7978870fa6eac20ba2578ee5a085293a4a6af18d3407`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-preserve-uncommitted-work`

Upstream `.claude/rules/aiqt/10-INTEG-preserve-uncommitted-work.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `079b701bb284cb830c73014d506e6ba92310483b83f09a6eeb24e4537e4a6cef`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-protected-branch-integrity`

Upstream `.claude/rules/aiqt/10-INTEG-protected-branch-integrity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `59c40e70c51a3915f791927248162ecff2887ec97ed65b428149b3d2c6d327cf`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-required-step-remains-required`

Upstream `.claude/rules/aiqt/10-INTEG-required-step-remains-required.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ef4e9c629f937cc69b33eecafe0d1fb53c5ee0b6bc397b5bc16e231f1b27e478`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-rerun-pass-is-still-failure`

Upstream `.claude/rules/aiqt/10-INTEG-rerun-pass-is-still-failure.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `39ade60ff7a2dfb27108061aa340f8e091118640e71d2c1f3e3bcb8dedeed92b`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-review-in-flight-pins-its-artefact`

Upstream `.claude/rules/aiqt/10-INTEG-review-in-flight-pins-its-artefact.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `66a13ad6f2a36a1362465ed34cdaa342bd53eee2b78d813c92d7fd6f8a2bed79`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-safe-retries`

Upstream `.claude/rules/aiqt/10-INTEG-safe-retries.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `edfecac461bab41a3514c596b291c453fe01f49bd8f5613b95cb2aac98829549`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-separate-task-changes`

Upstream `.claude/rules/aiqt/10-INTEG-separate-task-changes.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `a2e1df7edebc43fc90bf023efe316a2e3fc0aded3af28cc00936fcd50b513d52`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-stage-then-promote-on-green`

Upstream `.claude/rules/aiqt/10-INTEG-stage-then-promote-on-green.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `63e9d9d79d38c31e27f5720b85ab47c5222cf9f6428da67a3d699c31a42bd20e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-track-launched-work`

Upstream `.claude/rules/aiqt/10-INTEG-track-launched-work.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `1a6ce97b0599e10e961d0c99689fbaa583b37ea208386216e9cdf46e1ea5ab74`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-validation-gates-apply`

Upstream `.claude/rules/aiqt/10-INTEG-validation-gates-apply.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `dfe15564e51ddab6e19af6995ad8e072229b5ba9d233efad288bf2c91a7aa842`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-INTEG-workers-produce-inert-data`

Upstream `.claude/rules/aiqt/10-INTEG-workers-produce-inert-data.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `6a7623c04a8f3bf5df2aee76188f7dc1e199360ce532af9b82e424288e05af2e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-absolute-paths`

Upstream `.claude/rules/aiqt/10-QUALI-absolute-paths.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `11fb788e9b4da6deb19b0e2ccde54822a3dd084c9044a94c44acc4d189ad9e3e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-change-carries-check`

Upstream `.claude/rules/aiqt/10-QUALI-change-carries-check.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f0d64dd9542cc5c544853576120c7591f52a91d70c6838d609f02cc3cd87eb1f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-compatibility-or-migration`

Upstream `.claude/rules/aiqt/10-QUALI-compatibility-or-migration.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `172d1c6ae6f644bdcdad7a1a9d5a912cc94951ce2c63128a95b71ae5dd9ff9d1`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-confirm-execution-target`

Upstream `.claude/rules/aiqt/10-QUALI-confirm-execution-target.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `d5c77943670abf446d40b528e75b2e4226c1ff231c1347ea959dd1d782240f8f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-defence-in-depth-default`

Upstream `.claude/rules/aiqt/10-QUALI-defence-in-depth-default.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `869083e9ef683c85b8eb380961c656ce727214fa20b1d599c559559904c4e0d6`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-elapsed-aware-timer-restore`

Upstream `.claude/rules/aiqt/10-QUALI-elapsed-aware-timer-restore.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `62886e96c50d5d0728ef077f52115ef4806fd0eb1887e78270191451b970a3fc`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-findings-are-fixed-not-argued`

Upstream `.claude/rules/aiqt/10-QUALI-findings-are-fixed-not-argued.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `2422f9568c606f4e9f286c4f5b6c19e842fdee78b5a5e948cf4c71854dded45d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-goal-fidelity-across-trajectory`

Upstream `.claude/rules/aiqt/10-QUALI-goal-fidelity-across-trajectory.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `57eba929d16870f286470300a85da43683b5d14d71e7335cecda4d10daebc092`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-high-assurance-verification`

Upstream `.claude/rules/aiqt/10-QUALI-high-assurance-verification.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `5f97f7ebd69a8b825747c384fbc0ac5717a3ccfecb86641c672b93afb32b96fa`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-kill-timeout-exceeds-callee-wait`

Upstream `.claude/rules/aiqt/10-QUALI-kill-timeout-exceeds-callee-wait.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f0aad39bcc86943d8173636c4630cd081d388e063228ce682cb52f8dd0e2bb6c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-lightweight-verifier-workers`

Upstream `.claude/rules/aiqt/10-QUALI-lightweight-verifier-workers.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `8130dffb7ed200c34a55f877250082ea14036bce473cb6b34fe842cd07217572`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-match-surrounding-code`

Upstream `.claude/rules/aiqt/10-QUALI-match-surrounding-code.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `a5efa2d1c098f87119de27b85a57ba6dd72185a1f08acbbab4b8ff738363193c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-minimize-dependencies`

Upstream `.claude/rules/aiqt/10-QUALI-minimize-dependencies.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `52847a4bb4339269f413a5a857dc0d36206240a119c02fa43201c7682ae15fdb`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-self-guardrail-from-error`

Upstream `.claude/rules/aiqt/10-QUALI-self-guardrail-from-error.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f0bb93048360259f1ddf6e456c7b4a91d5414b649959397d382de14711b0a464`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-smallest-correct-change`

Upstream `.claude/rules/aiqt/10-QUALI-smallest-correct-change.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `52d59eb0d79af9a80aa6c529c197925f19d55c65bf730d32da4057fb547865c7`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-surface-counterproductive-instructions`

Upstream `.claude/rules/aiqt/10-QUALI-surface-counterproductive-instructions.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ed3443fb13e8dd7d19719c83d747153d27cc782ba278831180a817ede477bf4d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-test-hermeticity`

Upstream `.claude/rules/aiqt/10-QUALI-test-hermeticity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `76fcd50b0c87390e1bb75af0454edc76c3ff7c9147e1f9e3f1f87c849f37a0da`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-verifier-delivery-completeness`

Upstream `.claude/rules/aiqt/10-QUALI-verifier-delivery-completeness.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `15ff53ab46dba0a9908e39613b07ed56020b9340ac2f8c1c12fdc91220cab0b1`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-QUALI-verifier-diversity`

Upstream `.claude/rules/aiqt/10-QUALI-verifier-diversity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `b9d0fa9a991d84fbe673a56208ef0c3f63dbea20425ace2b8ff3d43cf7f4071d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-ai-toolchain-register`

Upstream `.claude/rules/aiqt/10-TRUST-ai-toolchain-register.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `3e52b6bf3d53bc55ab6231ec441c4e448875315361005d6b3c11a2492deec972`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-assess-advise-discussion-only`

Upstream `.claude/rules/aiqt/10-TRUST-assess-advise-discussion-only.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `10f5369a66ee5cc6b4c7e1d8c0bd0747bada6823d943d0ecfed15aa695d6797e`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-atomic-claim-from-pool`

Upstream `.claude/rules/aiqt/10-TRUST-atomic-claim-from-pool.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `4b797e29b0c95684ed6084d224fb461c9f6581e6e40279b85dfa743c9c42a0fe`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-change-record`

Upstream `.claude/rules/aiqt/10-TRUST-change-record.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `0f1974599cf36ae91ec0d06f303b58115814c59e39862975b21b8b36c90e2592`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-change-tracking-ext`

Upstream `.claude/rules/aiqt/10-TRUST-change-tracking-ext.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `fa3bba508acadc6ca5f710c341e02ba479ab56a8307efe3a1603af62a094e520`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-clarify-before-acting`

Upstream `.claude/rules/aiqt/10-TRUST-clarify-before-acting.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `06a68c8a599743de685c32c2b3070bfe219e8698b1374b2690393a661a962cd3`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-concurrency-lease`

Upstream `.claude/rules/aiqt/10-TRUST-concurrency-lease.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `20c201093daf82185da0b45339bfa565acc96a9d81b327580804c7976b99c2ae`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-continue-by-default`

Upstream `.claude/rules/aiqt/10-TRUST-continue-by-default.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7b8b07efdd4a13e18c140e625820a0b893c804f9e9a6931df747c3fd4662703b`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-express-authorization-before-execution`

Upstream `.claude/rules/aiqt/10-TRUST-express-authorization-before-execution.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `0b4b235c936219010fda0629e5820600042dd1649845fcdc40e57468426bb45d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-human-oversight-and-autonomy-threshold`

Upstream `.claude/rules/aiqt/10-TRUST-human-oversight-and-autonomy-threshold.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `500ec46b68c02422a357694f908dda4796e32e2d6092056509d94b63c2394c39`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-no-console-diff-dumps`

Upstream `.claude/rules/aiqt/10-TRUST-no-console-diff-dumps.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `308e6e2db143f234176832620768ea9e5d1b9b6ff8823f41e34fe692e637849d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-orchestrator-mistakes-register`

Upstream `.claude/rules/aiqt/10-TRUST-orchestrator-mistakes-register.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e65e499ccfb80d2d95aea11ec28e196043f109c66e3a4c9c7881de69f9514b0f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-reconcile-record-against-reality`

Upstream `.claude/rules/aiqt/10-TRUST-reconcile-record-against-reality.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `bffe77e19fcd63baccbc40d5f8abd92d518ac571f5e337f2c57b4f8d9dd9bbe7`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-records-first`

Upstream `.claude/rules/aiqt/10-TRUST-records-first.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ac5c8cfd3a376953a1ed0de2ad815605a7349e9d8666ae3111e3d70059ad31a7`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-session-close-on-green`

Upstream `.claude/rules/aiqt/10-TRUST-session-close-on-green.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `888ecba6a01eceddf160c102b1f9434f9ef16f7e18e775dbd9ce1bb5b2ff1e56`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-session-resume-from-handoff`

Upstream `.claude/rules/aiqt/10-TRUST-session-resume-from-handoff.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `9036dc8e9c4bddec87b50df099ee7b426f0c50cb9651c926375729a6c814d163`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-standing-constraints-persist`

Upstream `.claude/rules/aiqt/10-TRUST-standing-constraints-persist.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `29b79900c405646552937f27b434f2d4998e4b14158ddb82fdc43bd454b9c218`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-trust-recovery-escalation`

Upstream `.claude/rules/aiqt/10-TRUST-trust-recovery-escalation.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `8b0ac08aca16a572d07fa1c6a9a65d255be78532c2caed9edd43619819b62777`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `10-TRUST-trust-recovery-ext`

Upstream `.claude/rules/aiqt/10-TRUST-trust-recovery-ext.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ca2a29d56f95091c3f50db083deae2655f01b54d7d44e2686f8d29b45ada76ff`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `20-PROGR-decision-classification-before-enacting`

Upstream `.claude/rules/aiqt/20-PROGR-decision-classification-before-enacting.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `29b1c64bcb19fe0b05134db59c44a7cf8e15f2c0f8fa31a453cd54e678257cba`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `20-PROGR-repeated-failure-triggers-premise-review`

Upstream `.claude/rules/aiqt/20-PROGR-repeated-failure-triggers-premise-review.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `10f3addc005116937671bd2be90da3fde26828f6678226fb131ca4c500dcd7ac`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `30-SPEED-background-work-during-ci-waits`

Upstream `.claude/rules/aiqt/30-SPEED-background-work-during-ci-waits.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `bb9f3b8e737355cec4f8e48e81ffb645ac04eebf9b6fe4ab867709f781034c10`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `40-COST-cost-tier`

Upstream `.claude/rules/aiqt/40-COST-cost-tier.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `bf301122d02132e0d3a9f54988b2dbb645a1d07fee05b6676b9a6d18b888ea78`; Apache-2.0, upstream-owned. Local scope: unscoped.

<!-- AIQT-PROVENANCE-aiqt-END -->

## Pinned security rules

<!-- AIQT-PROVENANCE-security-BEGIN -->
### `SECA-resource-bounds`

Upstream `.claude/rules/security/SECA-resource-bounds.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `375447700ebc1747573126543b2b445f30616c29f87a215804a792150632e4b6`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECA-verified-restore-path`

Upstream `.claude/rules/security/SECA-verified-restore-path.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `efb7cc448342f497f3a73d7a9480976b546d0e596f032ae154cf36de5e9160e0`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-data-boundary`

Upstream `.claude/rules/security/SECC-data-boundary.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `8112e14e42ba88c5bad89d16183a7e38395e08a3d030b7062d2ad1527a641c86`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-egress-destinations`

Upstream `.claude/rules/security/SECC-egress-destinations.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `c1b18d883729b2f1871a3575265763fe5470ed1ebd90080e7bfa8e44e9a7f9f6`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-keep-secrets-out`

Upstream `.claude/rules/security/SECC-keep-secrets-out.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ed9b700dc61020f26f1fbc08d69823450809a44db0ebd990fe5e32b721dd8a54`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-least-privilege-retrieval`

Upstream `.claude/rules/security/SECC-least-privilege-retrieval.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `614ca3e928114e33bd238e1dcab39b7f4fec50ef8aada9ba11efdf89c30d4046`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-no-cross-context-bleed`

Upstream `.claude/rules/security/SECC-no-cross-context-bleed.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `4c35d3deddbe05cde0f59ed364610dd0e5b64eab05b02305d25df354ce4d5123`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-no-hidden-context-disclosure`

Upstream `.claude/rules/security/SECC-no-hidden-context-disclosure.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f6d9184d603b813bd0856de9290e8d38212720683f28274a78550ca9957fe698`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECC-rotate-leaked-secret`

Upstream `.claude/rules/security/SECC-rotate-leaked-secret.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `49c9030bb835ac27bac61350f8093ea4737ee69205b1dc17171efe2ff723393f`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-authentication`

Upstream `.claude/rules/security/SECI-authentication.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `72824b38e528d930f7c8752043c7377ab9a649f7be77df16ac50e7139499b181`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-authorization`

Upstream `.claude/rules/security/SECI-authorization.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `2e94a14bda0d0dd7293761463aa92ee1c2f9c22348e647f556d1d44c4b09f02c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-config-is-executable-trust-gate`

Upstream `.claude/rules/security/SECI-config-is-executable-trust-gate.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `d1163da189c678895879cc6048c03a56997cbac9fbd41d54968f50ef7d23714d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-cryptography`

Upstream `.claude/rules/security/SECI-cryptography.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `aecd04a29c4b0132ee3ddbec5b2220312d6fdbba149ea63b42d572f557cdc807`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-dependency-provenance`

Upstream `.claude/rules/security/SECI-dependency-provenance.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e7da6f0169d1b771456821bc569051e3582eaada65638955aff9723377168451`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-fail-closed`

Upstream `.claude/rules/security/SECI-fail-closed.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `04d7120445dec198c1550659972cf3363e9415c9686d4ed4b7fa9fb2741704fa`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-federated-identity-flow`

Upstream `.claude/rules/security/SECI-federated-identity-flow.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e1c0dae14b1204be462169b81743f010708c40e6277a396783d23154ab2e1855`; Apache-2.0, upstream-owned. Local scope: `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**`.

### `SECI-file-upload-handling`

Upstream `.claude/rules/security/SECI-file-upload-handling.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `31619a3ad20c7afd16cc84ce9f659a9ab010f2bd2eceb3993551335b0fc908e0`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-guardrail-config-integrity`

Upstream `.claude/rules/security/SECI-guardrail-config-integrity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `5ee165abb675a399e5884653c80b26567b29e08b2419e53470a195dbeb3d4362`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-human-authorization`

Upstream `.claude/rules/security/SECI-human-authorization.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `f9889b4752d978001803c78822b36af2447df00032a887af538decae4c54b411`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-input-validation`

Upstream `.claude/rules/security/SECI-input-validation.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `83c0ebf7d7efd8f557a05a10842824dccbf83734dd67978b6ae9329ab59120f0`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-inter-agent-trust`

Upstream `.claude/rules/security/SECI-inter-agent-trust.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `d0f3ec20a83fe33f723eb0d33356b1f9214a63c7933da78b2b079a82c57fcacb`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-key-management`

Upstream `.claude/rules/security/SECI-key-management.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `4e0d28e987ee8b2b2fddc43b8897fccc5e3922c1e4dae160c69f5dc86b618b6c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-least-privilege-tools`

Upstream `.claude/rules/security/SECI-least-privilege-tools.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `984745e42aa24a3ff8598be91abcb0e6388d3398eef2c8d3d6112e0eb0acb37c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-log-redaction`

Upstream `.claude/rules/security/SECI-log-redaction.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `b9077ec66be2225ff1453c61d77f564ef9e2efbee316007c2b57d0bfd9af8b4a`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-operator-deception`

Upstream `.claude/rules/security/SECI-operator-deception.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `c802446890d45f943fe6a83af57414ef42cb5717beea05c6c9054f27c619e465`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-output-encoding`

Upstream `.claude/rules/security/SECI-output-encoding.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `93572b31a1c8e475ec8ab4802da2975dfc63dfb19e70c49aec25e075162084f4`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-output-handling`

Upstream `.claude/rules/security/SECI-output-handling.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `0cad8990877f14074c63093154a447a4a7a0ad0b3f8b04f6006f6f830f27e749`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-pin-referenced-instructions`

Upstream `.claude/rules/security/SECI-pin-referenced-instructions.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e472b7766cb37f523dd6c36bc19134a8267a6e965de76a3c04c894e531b0bd1d`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-poisoning-resistance`

Upstream `.claude/rules/security/SECI-poisoning-resistance.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `dd5ed3e86c0cb3bfb99005751c887bb8d65f9a3d146f589c54b2b7be67c21562`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-prefer-removing-a-path`

Upstream `.claude/rules/security/SECI-prefer-removing-a-path.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7318a8f5900c32ac72f956831f2aa38fdd207daa9436547852f845263ff0e0a6`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-preview-has-no-side-effects`

Upstream `.claude/rules/security/SECI-preview-has-no-side-effects.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `6c7af5ac18f022e4f32f51bc23cda6f1f5deaa9c64461b15384cb012edc88a77`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-prompt-trust-hierarchy`

Upstream `.claude/rules/security/SECI-prompt-trust-hierarchy.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7029abad5eae7ac2c25f19bf7ac76ca1beb968b5b5029ba3b3e84b12ca48cfce`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-protect-audit-records`

Upstream `.claude/rules/security/SECI-protect-audit-records.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `e819796064dbfe636ace49f01c96c16c04c0a7aaf612a7cfee4aee5851b93961`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-reject-vulnerable-versions`

Upstream `.claude/rules/security/SECI-reject-vulnerable-versions.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7d1ed6a7d27fd70e4db10793336dfaf465fa0df8470ba1ca9a745f09582f088a`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-release-integrity`

Upstream `.claude/rules/security/SECI-release-integrity.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `935c1ee116427f64752e4343ba8172b1e9a5e8c591966bdf7ee1883f32411860`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-safe-deserialization`

Upstream `.claude/rules/security/SECI-safe-deserialization.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `ab862bb2e4e83cf198c0c087169122be26360395a3e97a90e858d492905419c5`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-secure-configuration`

Upstream `.claude/rules/security/SECI-secure-configuration.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `190917f3c1511a40aca3a3f6a65f72e430b725a3ad34a2d193ebfbe822f2f734`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-security-logging`

Upstream `.claude/rules/security/SECI-security-logging.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `cda2137d4626683a3762e9e71c9aa51baa8670c5b78be5091bdb5ebd46acc5c4`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-session-token-management`

Upstream `.claude/rules/security/SECI-session-token-management.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `78e3bb96a62f0d2a33bcc3d346503bc00ad387ee69926cd2f9f5b4c74ae200eb`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-ssrf-prevention`

Upstream `.claude/rules/security/SECI-ssrf-prevention.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `5b814dd41917601fd949fe32e025b0e8b11fee1c34a1e811506c064e59e9a34f`; Apache-2.0, upstream-owned. Local scope: `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**`.

### `SECI-symlink-resolution`

Upstream `.claude/rules/security/SECI-symlink-resolution.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `fec1beb6357dcdcfe6faf5f17f35fe045baa3c4340ff3352495828cd00e36a63`; Apache-2.0, upstream-owned. Local scope: `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.ts`, `**/*.tsx`, `**/*.jsx`, `**/*.html`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.toml`, `security/**`, `dev-security/**`, `ai/**`, `architecture/**`.

### `SECI-threat-model-boundaries`

Upstream `.claude/rules/security/SECI-threat-model-boundaries.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `377cd7ec6c5e0edf43103093ed413b330be661417d5c1c9701fd35c528b47911`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-tool-argument-validation`

Upstream `.claude/rules/security/SECI-tool-argument-validation.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `b1803500f22b1da3fb6a1eb77e0660a8431f0f5f9060d58f8a420753fd5f0458`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-untrusted-content`

Upstream `.claude/rules/security/SECI-untrusted-content.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `dd052fc57cec8a82405e2df68149a7346aeb6dd781a0d11f837ca11a4dc0ff1c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECI-verify-dependency-exists`

Upstream `.claude/rules/security/SECI-verify-dependency-exists.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `7a93b710f859a06b83f920266b6cd080afda5c38a1bdc881891dbadb062cad7b`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECP-data-minimization`

Upstream `.claude/rules/security/SECP-data-minimization.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `bef72daca0f70a0a0f0517fc805db090f0bc7e38e99552e6088d34a63ac5842c`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECP-data-residency-retention`

Upstream `.claude/rules/security/SECP-data-residency-retention.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `46935d7e78f3371f63dd6012491c2f3b98eed630e8c1dadfcd360145a023c54b`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECP-purpose-limitation`

Upstream `.claude/rules/security/SECP-purpose-limitation.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `b87293e42be693284e441088b0810b3aec17b5c403ad16bc7b606b49d0e94316`; Apache-2.0, upstream-owned. Local scope: unscoped.

### `SECP-synthetic-fixture-data`

Upstream `.claude/rules/security/SECP-synthetic-fixture-data.md`, commit `a3ff734ca855e4363f340eca52fbd87272c51854`; SHA-256 `27b27ca584b3f43f111051d861e316ae6f78a64373dcd2cb2197c6da241a7126`; Apache-2.0, upstream-owned. Local scope: unscoped.

<!-- AIQT-PROVENANCE-security-END -->

## Legacy procedure crosswalk

Maintainer D3 (2026-10-02): no procedure retires. These are principle mappings with retained detail, not equivalent renames. Read the complete local procedure at its compatibility trigger.

| Old rule | AIQT successor(s) | Retain as GRC procedure/requirement |
|---|---|---|
| `action-before-explanation-of-inaction` | `10-ACCUR-observe-before-asserting-behaviour`; `10-ACCUR-validate-inference-before-action`; `10-TRUST-human-oversight-and-autonomy-threshold`; `10-TRUST-continue-by-default` | The explicit **attempt authorized safe action before explaining inaction** protocol; execution-doubt versus decision-doubt ordering; event subscription/status-read and bounded polling procedures. |
| `ai-assistant-workflow-disciplines` | `10-ACCUR-evidence-grounded-completion`; `10-ACCUR-verify-fix-in-commit`; `10-INTEG-workers-produce-inert-data`; `10-INTEG-review-in-flight-pins-its-artefact`; `10-INTEG-separate-task-changes`; `10-INTEG-required-step-remains-required`; `10-QUALI-verifier-diversity`; `10-QUALI-high-assurance-verification`; `30-SPEED-background-work-during-ci-waits` | Worker correction metrics and versioned brief-update loop; verified partitioning and orchestrator-only shared surfaces; parallel research/serial apply; six-round/nine-converging-round loop; recorded overrides with revert paths and attended surfacing; five-part QA completion protocol; author/source/adapter/publication architecture and semantic catch-net. |
| `artefact-and-branch-discipline` | `10-INTEG-generated-artefact-source-only`; `10-INTEG-protected-branch-integrity`; `10-INTEG-branch-and-merge-on-green`; `10-INTEG-preserve-uncommitted-work`; `10-INTEG-gate-discipline` | Exact local-regenerate/CI-check procedure; version-monotonicity audit contract, preservation of both bumps during conflict resolution, and project-specific branch exceptions. |
| `change-tracking` | `10-TRUST-change-record`; `10-TRUST-change-tracking-ext`; `10-TRUST-records-first`; `10-TRUST-continue-by-default`; `10-TRUST-session-resume-from-handoff` | Root/detailed split, entry schemas and ceilings, roll-up/archive coupling, every-PR entry, touched-file links, TODO→DONE rotation and original IDs, next-N queue display, overnight `stub/in-flight/done` lifecycle. **Conflict:** AIQT’s release-significant-only public derivative does not replace GRC’s every-PR policy. |
| `clarify-before-acting` | `10-TRUST-clarify-before-acting`; `10-TRUST-standing-constraints-persist`; `10-TRUST-human-oversight-and-autonomy-threshold` | Compute-first before asking; bounded-default calibration; self-contained option/consequence format; applicable plan workflow, unexpected-state investigation, and scope-expansion protocol. |
| `decision-classification-before-enacting` | `20-PROGR-decision-classification-before-enacting`; `10-INTEG-anything-wrong-fixed-first`; `10-TRUST-continue-by-default`; `10-ACCUR-completeness-claim-enumerates-its-set` | Exact five-member blocker vocabulary; reachable authority must be asked; local write-before-enact and exhaustion-token machinery. |
| `evidence-grounded-completion` | `10-ACCUR-evidence-grounded-completion`; `10-ACCUR-claims-rest-on-observation`; `10-ACCUR-completeness-claim-enumerates-its-set`; `10-ACCUR-partial-read-is-not-the-whole`; `10-ACCUR-measured-and-estimated-figures-stay-separate`; `10-ACCUR-corroborate-external-claims`; `10-INTEG-gate-discipline` | Current-turn upstream currency check; acquire missing load-bearing references before merely routing them; durable tracker for accepted-unverified claims; external-link destination/content verification; subscription/polling procedures. |
| `express-authorization-before-execution` | `10-TRUST-express-authorization-before-execution`; `10-TRUST-assess-advise-discussion-only`; `10-TRUST-standing-constraints-persist` | Explicit conditional/sequenced-go procedure: the later gated step awaits confirmation. Adjacent/unnamed endorsement does not widen scope. |
| `gate-discipline` | `10-INTEG-gate-discipline`; `10-INTEG-validation-gates-apply`; `10-INTEG-check-fails-closed-on-unreadable`; `10-INTEG-rerun-pass-is-still-failure` | GRC’s **no exception register: fix or descope** policy, diagnose workflow, and applicable tool examples. AIQT’s recorded reduction authorization is not a new local bypass. |
| `high-assurance-verification` | `10-QUALI-high-assurance-verification`; `10-QUALI-verifier-diversity`; `10-ACCUR-evidence-grounded-completion` | Three-condition sensitive-change trigger; complete five-stage harness; negative-signal screening; independent false-positive/false-negative lenses; guard-first sequencing; dry-run/idempotent scripted apply and re-parse; persistent resume-visible register. |
| `project-integrity` | `00-project-integrity`; `10-ACCUR-no-fabrication`; `10-INTEG-no-concealed-failure`; `10-INTEG-gate-discipline`; `10-QUALI-defence-in-depth-default` | Checkpoint emission at task/plan, persistence, completion and tradeoff boundaries; minimum per-PR cadence and concrete self-acknowledgement. |
| `session-lifecycle` | `10-TRUST-session-resume-from-handoff`; `10-TRUST-reconcile-record-against-reality`; `10-TRUST-continue-by-default`; `10-TRUST-session-close-on-green`; `10-TRUST-concurrency-lease`; `10-TRUST-human-oversight-and-autonomy-threshold` | Operating-mode meanings and authorized transitions; timeout handling; handoff fields/retention; closing-QA compensating control; stalled-QA reissue and late-result consumption; lease lifecycle; bounded prequeue at closing merge SHA. **Superseded:** old fresh-session/session-depth wind-down permission, already overridden locally. |
| `surface-counterproductive-instructions` | `10-QUALI-surface-counterproductive-instructions`; `10-TRUST-clarify-before-acting` | Charitable interpretation; materiality threshold; surface once, respect informed authorized override, avoid repeated/trivial asks. |
| `trust-recovery-escalation` | `10-TRUST-trust-recovery-escalation`; `10-TRUST-trust-recovery-ext` | Maintainer invocation; forensic-then-persona suite; full-clone check; verify/dedupe and severity-tier all findings; combined-set sign-off including zero findings; hold before remediation/lessons/substantive work. |
| `validate-inference-before-action` | `10-ACCUR-validate-inference-before-action`; `10-ACCUR-guard-input-soundness`; `10-ACCUR-disclose-guard-residuals`; `20-PROGR-repeated-failure-triggers-premise-review`; `10-INTEG-explicit-binding-over-ambient-context`; `10-QUALI-absolute-paths` | Observer reality fixtures and observation/decision separation; mutation-harness positive/negative controls, semantic-effect screening and baseline proof; exact two-failure diagnosis protocol. |

Do not describe these rows as 15 equivalent renames. Several are one-to-many mappings with retained procedural obligations.
