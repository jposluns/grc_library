# Decision Classification Before Enacting

Before enacting a significant autonomous decision, classify it, in writing, as exactly one of ACT, ASK, or BLOCKED, and for BLOCKED name the blocker from a closed, externally-observable set. The classification is written before the decision is enacted, not narrated after it.

This rule exists because the failure it prevents is subtle and self-justifying: an assistant defers a queued item, re-sequences the plan, winds down, or skips work on an un-instrumented internal-state rationale ("this is getting heavy", "better done fresh later", "too risky to do now"), and the deferral looks like prudence while it is really avoidance. Deferral-with-no-decision is strictly worse than both valid moves: it stalls the work AND hands the responsible authority nothing to act on.

A significant autonomous decision is one that disposes of a queued or authorized item, or changes the plan: a defer, a re-sequence, a wind-down, a skip, or an authorial choice made without asking. A routine execution step (the next edit, the next verification, the next commit in an already-decided sequence) is not a decision in this sense; this rule governs the moments the plan itself bends.

The rule applies to human collaborators and to AI coding assistants. It binds more often on AI assistants, because the failure mode (dressing an un-instrumented "I should stop here" up as a considered call) is exactly what an assistant reaches for when the work ahead feels large.

---

## The three classifications

At the moment the assistant is about to NOT do a queued or authorized item, or to change the plan, it classifies the reason as exactly one of the following, and there is no fourth:

- **ACT**: there is no real blocker, so do it. This is the default, and the right answer far more often than the instinct to pause suggests.
- **ASK** a specific, named question: the decision is genuinely the responsible authority's to make. While that authority is reachable, the assistant ASKS the question; it never records a defer in place of a reachable question.
- **BLOCKED**, naming a blocker-type from a CLOSED, externally-observable set: `maintainer-decision-unreachable`, `irreversible-needs-confirmation`, `failing-check`, `source-unavailable`, `maintainer-directed-hold`. A blocker-type outside the set, or an un-instrumented internal-state justification (context heaviness, a felt sense of degradation, "do it fresh later"), is not a valid BLOCKED reason.

The closed set is the discipline's load-bearing part: a consuming project adapts the specific names to its own authority and tooling, but the invariant is that the set is closed and every member is EXTERNALLY OBSERVABLE (someone other than the assistant could confirm it). Un-instrumented internal state is never a valid basis for a hold (the [`evidence-grounded-completion`](evidence-grounded-completion.md) rule's un-observable-state corollary). In any attended mode, a decision that is the authority's is ASKED while they are reachable, never deferred.

---

## Write before enact

The classification is written down BEFORE the decision is enacted, not narrated after it as a rationalization. Writing-before-enacting is the forcing function: a self-justifying non-decision does not survive being written against the closed vocabulary, because there is no honest classification for "I will quietly not do this because it feels like a lot". Making the record at decision time is what turns the classification into a decision rather than an after-the-fact story a reader cannot distinguish from one.

A BLOCKED entry that rests on a set-completeness claim (everything remaining is blocked, the queue is exhausted, nothing is actionable) additionally carries the full enumeration burden the [`evidence-grounded-completion`](evidence-grounded-completion.md) rule places on a set-completeness claim: enumerate every member of the set through its index, give each a disposition, and show the enumeration. It also carries the higher evidence bar that rule's asymmetric-skepticism clause places on a claim that licenses LESS work: when the evidence is only partial, the required default is to CONTINUE on the highest-priority open item, never to stop.

---

## Finding something wrong is not a decision point: finish the task, then fix it

There is one situation where the three classifications do not apply, because only one action is
available. **The moment anything wrong is found, the obligation is to finish the unit of work in hand
and then FIX it, and nothing that is not the fix, or part of the fix, proceeds ahead of it.**

"Anything wrong" is deliberately the widest wording: an issue, a defect, an error, an inaccuracy, a
fault, a wrong figure, a stale instruction, a misleading name, an overstated claim, a write that
silently did nothing. It does not matter how small it looks, who found it, or whether it has a severity
yet. **Grading a defect is one of the ways of not fixing it**, so the severity assessment comes after
the fix decision rather than gating it.

"Finish the current task" is narrow: complete the unit already in hand so nothing is left half-applied,
then fix. It does not license finishing a comfortable stretch of adjacent work, starting the next
change, running another analysis pass, or writing up what was found.

**Why this needs saying, when it sounds obvious.** The failure is never a decision to ignore a defect.
It is one of these, and each feels like diligence at the time:

- **Aestheticising it.** Rendering findings as a table, a count, or a comparison, and letting the tidy
  summary stand in for the fix. A defect formatted well reads as a defect handled.
- **Noticing and carrying on.** Describing the problem accurately, even recording it, and continuing
  with the work in flight. Accurate description is the most convincing substitute for action.
- **Grading instead of repairing.** Characterizing severity, blast radius or class while the defect
  stays live.
- **Routing what could be fixed.** Sending a fixable finding to the backlog because the backlog is a
  legitimate destination for what genuinely cannot be fixed now.

**Against the rubric.** "Found a defect and continued" is never an ACT, since the queued work was not
what the discovery made necessary. It is not an ASK, since fixing your own defect needs no authority.
And it cannot be BLOCKED, because the blocker set is closed and contains no entry for it. There is no
classification under which it is legitimate, which is precisely why it needs stating: the rubric would
otherwise appear to permit it by silence.

**Where a fix genuinely cannot be made now** (it needs an authority's decision, a source that is
unavailable, or it lives in a repository this actor cannot write), it is ROUTED with its severity and
its blocker named, and the routing is the terminal disposition. That is the narrow exception, and the
test for it is whether the fix is impossible rather than merely inconvenient.

---

## Prohibited anti-patterns

- **Deferral with no question.** Recording a defer when the decision is the authority's and the authority is reachable. Ask the specific question instead.
- **Internal-state holds.** Classifying a hold on "heaviness", "context depth", "I feel degraded", or "best done fresh": none is externally observable, so none is a valid BLOCKED reason. A hold needs a named signal from the closed set.
- **Narrate-after instead of write-before.** Enacting the decision and then explaining it. The classification is a pre-condition of enacting, not a caption on it.
- **A blocker-type outside the closed set.** Inventing a blocker name to fit a decision the closed vocabulary would reject; the point of the closed set is that it cannot be widened to launder an internal-state hold.
- **A stop justified by an unshown set-completeness claim.** "Everything is blocked" used to license stopping, without the enumeration; the asymmetric-skepticism bar is higher, not lower, for a claim that does less work.

---

## Relationship to the rest of the pack

This rule consolidates a decision-time discipline that sits at the intersection of three others and is owned in full by none:

- [`action-before-explanation-of-inaction`](action-before-explanation-of-inaction.md) governs the execution-versus-decision distinction and the reversibility gate for an external action; a BLOCKED classification here IS an inaction explanation that must name a blocker, so the two compose.
- [`clarify-before-acting`](clarify-before-acting.md) governs the ASK path: surface a named-option question on a genuine ambiguity or an authorial choice.
- [`evidence-grounded-completion`](evidence-grounded-completion.md) supplies the un-observable-state, set-completeness, and asymmetric-skepticism principles the BLOCKED path leans on.

What none of them states as such, and this rule adds, is the write-BEFORE-enact ordering and the closed, externally-observable blocker vocabulary, applied to every significant plan-bending decision. It builds directly on [`evidence-grounded-completion`](evidence-grounded-completion.md)'s un-observable-state corollary (an un-instrumented internal state is never assertable and never a valid trigger to stop, hold, or defer) and pairs with the wind-down discipline in [`session-lifecycle`](session-lifecycle.md) (a wind-down is a plan-bending decision, so it is classified and written before it is taken).

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Decision classified before enacting | RV.1 | GRC-05 | A.5.36 | V15.1, V16.2 |
| Closed, externally-observable blocker vocabulary | PO.5, RV.2 | GRC-04 | A.5.4 | V15.1 |

The rule expresses the same audit-trail-integrity principle as the rest of the pack, at the decision-intake boundary: a decision that bends the plan must be traceable to a classification made and recorded before the action, against a closed vocabulary, not to an after-the-fact rationalization that a reader cannot tell apart from a real decision.

<!-- PROJECT-OVERLAY: not part of the distributable pack -->

## Project overlay (grc_library wiring and lineage; local copy only)

- The write-before-enact decisions log is `grc_library_private/autonomous-decisions-log.md`: every significant autonomous decision is classified (an `ACT` / `ASK` / `BLOCKED: <type>` line) and written there before it is enacted. The closed blocker set is as in the rule body (`maintainer-decision-unreachable`, `irreversible-needs-confirmation`, `failing-check`, `source-unavailable`, `maintainer-directed-hold`).
- Mechanical backstop: the [`block-unjustified-decision.py`](../../hooks/block-unjustified-decision.py) PreToolUse hook refuses a log write that lacks a `**Classification:**` line, names a blocker-type outside the closed set, or (in a deferral or hold entry) cites a forbidden internal-state justification; a `grc_library_private` validate check gates the log's shape in parity with the hook.
- The set-completeness / anti-false-completeness half is enforced by [`tools/audit-backlog-actionability.py`](../../../tools/audit-backlog-actionability.py) (the enumeration tool the hold path must quote) plus the same hook's exhaustion guard (a hold justified by a set-completeness claim is refused unless it embeds a fresh full-audit token matching the live backlog count).
- Project instantiation: the CLAUDE.md `## Decision discipline: act, ask, or name a blocker (write-before-enact)` and `## Backlog-status characterization is the audit tool's output` sections.
