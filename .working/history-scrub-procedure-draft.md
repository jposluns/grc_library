# History-scrub procedure draft (TODO §1.19.13, Phase 6; maintainer-gated, LAST)

**Status: DRAFT for maintainer review. Do NOT execute any step without explicit
maintainer authorization.** This is a protected-branch history rewrite; the
[`artefact-and-branch-discipline`](../.claude/rules/governance/artefact-and-branch-discipline.md)
force-push exception path governs, and its friction is deliberate. This file is the prepared
input so the eventual Phase-6 execution is a review-and-run, not a design-from-scratch.

## Why this exists

§1.19.8/9 MOVE the operational-narrative docs out of the public tree to `_private`, but a
move alone leaves the full prior content in public git HISTORY (the §1.19 #1 LOCKED design
point): the 2026-07-17 cold-sales email mined the public `.working/` tree, and history
remains minable after a plain move. §1.19.13 is the REAL purge. It is gated LAST because a
history rewrite is the highest-unwind-cost action in the project and must not run until the
moves (§1.19.8/9) have landed and settled.

## Precondition gate (all must hold before proposing execution)

1. §1.19.8 (relocate living docs to `_private` + reference repointing) is MERGED and green.
2. §1.19.9 (dated-archive sweep to `_private`) is MERGED and green.
3. The public working tree no longer references the moved docs by a resolvable path (the D7
   runbook token dropped; the roughly 5 non-exempt markdown-linkers reduced to bare
   code-spans; advisory-tool references repointed to `_private`), confirmed by a bare-token
   grep over ALL file types (the file-type-width close-out axis), zero live path-resolving
   references.
4. A full (non-shallow) clone is confirmed (`git rev-parse --is-shallow-repository` returns
   false) so history-aware audits and the rewrite operate on complete history.

## Worklist (what to purge from history)

The §1.19.8 move-list, exactly (the scrub target IS the move-list, per the §1.19 LOCKED
design). The relocated files whose prior public-history content is purged: `third-party-issues`,
`credit-offload-design`, `credit-offload-metrics`, `maintainer-egress-requests`,
`cloudflare-pages-setup`, `design-decisions`, `multi-session-orchestration`,
`hallucination-metrics`, `high-assurance/register`, the two `*-considerations` ledgers,
`deferred-protected-changes`, `register-main-branch-protection`, `session-length-considerations`,
`cross-file-section-ref-gate-design`. Confirm the live move-list against TODO §1.19 at
execution time; the TODO is the authority if the list has drifted.

## Procedure (the artefact-and-branch-discipline force-push exception path)

1. **Document the technical reason** (this file) and obtain **explicit governance-authority
   (maintainer) approval** for the rewrite. No approval, no rewrite.
2. **Notify collaborators / other sessions in advance** so they re-clone or rebase; confirm
   no unmerged `origin/claude/*` sibling branch is in flight (the concurrency-lease
   cross-check), since a rewrite while a feature branch is open orphans that branch.
3. **Preserve the pre-rewrite ref** under `refs/preservation/history-scrub-<YYYY-MM-DD>/main`
   (and push the preservation ref) BEFORE the rewrite, so the original history stays
   auditable and recoverable.
4. **Rewrite** with `git filter-repo --path <each worklisted path> --invert-paths` (the
   modern replacement for `filter-branch`; it removes the paths across ALL history). Stage
   the full path list from the worklist above and inspect the rewritten history before
   pushing.
5. **Re-run the version-monotonicity audit** (gate 45 and the history-aware trio) on the
   rewritten branch to confirm no version-bearing commit was dropped or reordered.
6. **Force-push** the rewritten `main` (the one sanctioned protected-branch force-push, under
   this documented exception), then have every clone re-fetch or re-clone.
7. **Verify the purge**: `git log -p --all -- <path>` for each worklisted path returns zero
   remaining content; spot-check that a distinctive sensitive string (a mined narrative
   phrase) returns zero hits across the rewritten history.

## Residual-risk note (honest)

- A history rewrite cannot un-publish what was already cloned, forked, mirrored, or indexed
  before the rewrite (cached views, forks, search indexes). The scrub reduces future
  minability of the canonical repo; it does not guarantee erasure from third parties that
  already fetched. Anything that is a genuine SECRET (rather than merely sensitive narrative)
  is rotated, not just scrubbed; a secret should never have been committed, and the scrub is
  for operational-narrative sensitivity, not a secret-rotation substitute.
- The rewrite invalidates all outstanding open PRs and branches; time it for a quiet
  boundary.
