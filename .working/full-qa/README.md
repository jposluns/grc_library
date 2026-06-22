# Full-QA / deep-qa-review activity

Per-run records of the `/full-qa` (canonical skill name `deep-qa-review`) forensic
quality-assurance pass. `/full-qa` is the trust-recovery escalation tier's
AI-failure-pattern lens: a six-subagent forensic review (A recent-PR deep review,
B corpus-wide stale-reference, C audit-programme integrity, D citation forensic,
E generator-output forensic, F discipline-violation forensic) over a defined PR
window plus the files those PRs reference. It pairs with `/fitness` (ten persona
lenses) to form the two-skill trust-recovery suite.

This directory is maintainer working state, exempt from corpus audit gates per the
`.working/` directory exemption. Records are frozen-state archives: `path:line`
references are accurate as-of write-time, not maintained against later corpus
changes.

## Convention

- One record per run: `YYYY-MM-DD-iterN.md` (UTC date per `.claude/CLAUDE.md`).
- Sections: Trigger & state snapshot; one section per subagent (A-F); Orchestrator
  synthesis & apply-time verification; Findings routed; Resulting PR; Trust-recovery
  framing.
- Every finding carries a `path:line` quote; findings without quoted evidence are
  hypotheses, re-dispatched, not recorded as findings.
- Confirmed findings route to TODO P1 top tagged `[full-qa]`, regardless of
  severity; the maintainer triages. The pass terminates only on explicit maintainer
  sign-off of the combined trust-recovery TODO P1 additions.

## Methodology note (binding on every run)

The pass MUST run on a full (non-shallow) clone. `git log --follow` on a shallow
clone mis-attributes last-commit dates and makes the git-history-aware gates
(gate 31 document-date-staleness, gate 40 version-bump-recency) emit false
positives. Verify `git rev-parse --is-shallow-repository` is `false` (or run
`git fetch --unshallow`) before running `tools/run_all_audits.sh` or any
subagent that reasons over `git log --follow`. Iteration 1 (2026-06-22) caught
this when Subagent C reported a 153-document gate-31 failure that did not
reproduce on the unshallowed clone.

## History

| Date | Run | Subagents | Findings | Detail |
|---|---|---|---|---|
| 2026-06-22 | iter1 | A-F | 5 confirmed (3 treatment-vocab errors, 1 docstring note, 1 corrective-record warning); 1 false positive caught (gate-31 shallow-clone artifact); 1 known-issue dedup (EDPB register = P7 B2) | [`2026-06-22-iter1.md`](2026-06-22-iter1.md) |
