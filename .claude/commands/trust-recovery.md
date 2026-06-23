Run the trust-recovery escalation suite: the heavier, white-box re-examination invoked when accumulated AI-assistant discipline failures put a maintainer's confidence in a *window* of work in question (per the [`trust-recovery-escalation.md`](../rules/governance/trust-recovery-escalation.md) governance rule). This is a convenience wrapper that runs the two-skill suite in order; it does not replace either skill, and it does not self-authorize (the maintainer invokes it and names the PR window).

Execute in order:

0. **Verify a full (non-shallow) clone before any history-aware step**: run `git rev-parse --is-shallow-repository`; if `true`, `git fetch --unshallow`. On a shallow clone `git log --follow` mis-attributes file dates and makes gates 31/40 emit false positives. This is the binding methodology rule the suite shares; do it once, up front, before either pass.

1. **Run [`/full-qa`](full-qa.md) first** (the `deep-qa-review` AI-failure-pattern forensic pass) over the maintainer-named PR window plus the files those PRs reference. It is the smaller, faster, AI-pattern-tuned lens; run it first. Surface its confirmed findings inline and route them to the backlog tiered by severity (High[critical] and High to the top-priority tier / P1, Medium and Low to the next tier / P2, tagged `[full-qa]`, none dropped) per the rule's routing convention.

2. **Then run [`/fitness`](fitness.md)** (the `library-fitness-review` fresh-reader persona pass) over the whole corpus, with its step-5.5 trust-recovery routing flag active (findings tiered the same way, tagged `[fitness]`). It is the broader, slower lens; run it second. Surface findings as it completes; do not wait for both passes before routing.

3. **Hold for maintainer sign-off.** The suite terminates only when the maintainer reviews the combined routed additions (from both passes) and explicitly signs off, not on an empty finding-set. Do not proceed to codification of lessons or to remediation until sign-off; an empty finding-set still requires the maintainer's acknowledgement that confidence is restored.

After sign-off, codify the process lessons per the rule's "After sign-off" protocol (formalize any ad-hoc forensic pass as a skill; bake any methodology lesson into the relevant skill; the durable backstop for the triggering failure class is a mechanical gate, not the suite alone).

This wrapper is a thin sequencer over [`/full-qa`](full-qa.md) and [`/fitness`](fitness.md); the two underlying skills hold the authoritative step detail, evidence bars, and subagent dispatch discipline. See the [`trust-recovery-escalation.md`](../rules/governance/trust-recovery-escalation.md) rule for the trigger classes, the findings-routing convention, and the sign-off discipline.
