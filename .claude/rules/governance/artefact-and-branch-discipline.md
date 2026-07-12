# Artefact and Branch Discipline

Two related disciplines protect a project's audit trail:

1. **Generated artefacts are read-only.** Never hand-edit; always regenerate from the source. The generator is the canonical statement of how the artefact derives from the source.
2. **Protected branches are append-only.** Never push directly to a protected branch; never rewrite its history. The branch is the canonical statement of what the project's history looks like.

Both rules exist because the audit trail depends on the artefact and the branch faithfully reflecting the change history. A hand-edit to a generated file or a force-push to a protected branch breaks that contract.

This rule applies to human developers and to AI coding assistants equally. AI assistants face the discipline more often because the failure modes (hand-editing a generated file to "save a regeneration" round-trip, force-pushing past a failing check to "save a rebase") look like progress when they are actually defects.

---

## What counts as a generated artefact

The category is broader than "the build output" alone. Treat as generated:

- **Build outputs**: compiled binaries, bundled assets, transpiled code.
- **Schema dumps**: database schemas, OpenAPI specs, GraphQL SDLs derived from code annotations.
- **Taxonomies, indexes, scorecards**: derived from source documents via a build script.
- **Documentation portals**: HTML or static-site output generated from Markdown sources.
- **Lockfiles**: with the caveat that lockfile updates happen via the package manager (`npm install`, `pip-compile`, `cargo update`), not by hand. Hand-edited lockfiles are anti-pattern.
- **Generated tests or fixtures**: snapshot tests, contract-test artefacts, fixtures derived from a schema.

If a file is produced by running a command against other files, it is generated. The CI `--check` for that file's drift is the mechanism that enforces the discipline.

---

## What counts as a protected branch

- **The default branch** (`main`, `master`, `trunk`).
- **Release branches** that downstream consumers track (`release/X.Y`, `stable`, `production`).
- **Long-lived integration branches** that other PRs target (`develop`, `staging`).

Short-lived feature branches are not protected; force-push to a feature branch you own is normal git workflow. The discipline applies to branches whose history other people (or other automation) depend on.

---

## Required workflow

### Generated artefacts

1. **Edit the source**, not the artefact.
2. **Run the generator locally** to refresh the artefact.
3. **Commit source and generated output together** in the same commit, so the diff shows both halves.
4. **CI runs the generator in `--check` mode** and fails the build on drift.

The discipline is symmetric: developers regenerate before committing; CI verifies they did. Neither side regenerates *in place of* the other.

### Protected branches

1. **Develop on a feature branch** named after the change (`fix-401-on-stale-session`, not `temp` or `dev`).
2. **Open a PR** against the protected branch.
3. **Merge through the PR mechanism** (squash, merge-commit, or rebase, per project convention).
4. **Force-push to a feature branch you own is acceptable** for legitimate rebasing or cleanup. Force-push to a protected branch is not.

---

## Prohibited anti-patterns

### Generated artefacts

- **Hand-editing a generated file** to "save a regeneration round-trip." The next regeneration will silently overwrite the hand-edit; the divergence between source and artefact is invisible until then.
- **Regenerating in CI** to bypass the `--check`. This defeats the drift check by construction: every run "passes" because CI just produced the file it is checking. See the gate-discipline rule.
- **Stripping the generator-output `--check` job** from CI. Same anti-pattern, blunter. The check exists because the drift it catches is real; removing the check normalizes the drift.
- **Partial generation**: running the generator, then hand-fixing the parts it got wrong. The right fix is to the generator, not to the artefact.
- **Committing the regenerated artefact without re-running** when the source has changed. The pre-commit drift check is the last line of defence against this; do not bypass it with `--no-verify`.

### Protected branches

- **Direct push** to a protected branch, bypassing the PR mechanism.
- **Force-push** (`git push --force`, `--force-with-lease`) to a protected branch. Rewrites history that downstream branches and CI runs depend on; can drop version-bearing commits and trigger the version-monotonicity audit.
- **`git reset --hard` followed by push** to undo a CI failure on a protected branch. The CI failure is signal; the reset hides it.
- **Merging without going through the PR mechanism**: bypasses the review and the required checks. The PR mechanism is the gate; merging around it is gate bypass.
- **Demoting required checks to optional** to merge. See the gate-discipline rule: never weaken a gate to silence a failure.
- **Squash-merging when project convention requires merge-commits** (or vice versa). Match the project's convention; do not silently swap merge styles.

---

## Version monotonicity contract

When a project carries version-bearing artefacts (per-document versions, library versions, CHANGELOG entries, schema versions), the version numbers must strictly increase in the order their bumps appear in history. The contract requires:

- **A version-monotonicity audit** that runs on every PR and on the protected branch after merge.
- **Branch protection** that prevents force-push to the protected branch, so version-bearing commits cannot be silently rewritten or dropped.
- **Merge-conflict resolution** that preserves both version bumps when two branches bump the same artefact. Dropping one bump in a conflict resolution is a defect the audit catches.

The audit is a backstop. The primary defence is branch protection. If branch protection is absent or weak, the audit is the only thing standing between the project and a silently-rewritten version history; treat it as such.

---

## Tool-specific guidance

### Generated artefacts in CI

The pattern is symmetric between local and CI:

```
# Local (developer): regenerate, then commit source plus output.
python3 tools/build-taxonomy.py
git add taxonomy.yml ai/ compliance/   # source and output together
git commit

# CI (verification): regenerate in --check mode; fail on drift.
python3 tools/build-taxonomy.py --check
```

CI must use `--check` (or `--diff`, depending on the generator), not the bare command. If the generator does not support a `--check` mode, add one before relying on it for CI; do not let CI regenerate-in-place.

### Branch protection settings

For a protected branch, configure (in the order of importance):

- **Required PR review**: minimum 1 reviewer; 2 for security-sensitive repositories.
- **Required status checks**: every CI gate that the project's audit programme requires.
- **Prevent force-push**: branch protection rule.
- **Prevent branch deletion**: branch protection rule.
- **Restrict who can merge**: limit to maintainers if the project has a maintainer set, or to repository administrators otherwise.

A "protected" branch with no actual rule enforcement is decoration. The branch's name and the project's documented intent are not enforcement; the branch protection settings are.

### Lockfile updates

Lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) are generated, but the generator is the package manager rather than a custom script. The rule:

- **Run the package manager** to update the lockfile when dependencies change.
- **Commit the lockfile** in the same commit as the dependency change.
- **Never hand-edit** a lockfile to resolve a conflict; re-run the package manager.
- **CI should fail** if the committed lockfile diverges from what the package manager produces for the committed manifest.

### Long-lived integration branches

Some projects use a `develop` or `staging` branch between feature branches and `main`. The discipline applies to those branches:

- Treat them as protected.
- Force-push to them is the same anti-pattern as force-push to `main`.
- The version-monotonicity contract still applies; if `staging` accumulates version bumps before they reach `main`, the audit must validate the staging history.

---

## Exception-handling protocol

There are legitimate exceptions to both halves of this rule:

### Generated-artefact exception

If the generator is fundamentally broken for a specific case and must be patched, the right response is to fix the generator and regenerate, not to hand-edit the output. But if the generator fix is non-trivial and time-sensitive (a release blocker), the exception path is:

1. Document the technical reason the generator cannot be fixed in this PR.
2. File a tracked issue for the generator fix with a remediation deadline.
3. Hand-edit the artefact in the PR with a comment marking the patch and linking the tracked issue.
4. The pre-commit drift check fails; the maintainer overrides it with `--no-verify` *only with the documented exception link in the commit message* (see the gate-discipline rule's exception register).
5. Before the deadline, fix the generator, regenerate, and remove the hand-edit comment.

### Branch-protection exception

If a protected branch must be force-pushed (a credential leaked into history; a copyright violation must be expunged; a malformed merge corrupted the branch), the exception path is:

1. Document the technical reason the force-push is necessary.
2. Get explicit approval from the governance authority (CISO for security, maintainer for project-internal cases).
3. Notify all repository collaborators in advance so they can rebase or re-clone.
4. Perform the force-push; preserve the pre-rewrite ref under a `refs/preservation/` namespace so the original history is auditable.
5. The version-monotonicity audit must be re-run after the rewrite to confirm no version-bearing commits were dropped.

Both exception paths are slow by design; the friction is proportional to the residual risk.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | SLSA |
| --- | --- | --- | --- | --- |
| Generator-output discipline | PO.5, PW.4 | CCC-01 to 04, AIS-04 | A.8.32 | Level 2 |
| Branch protection | PO.5 | CCC-04 | A.8.32 | Level 2 |
| Audit-trail preservation | PS.1, RV.1 | LOG-02, LOG-04, LOG-10 | A.8.15 | Level 3 |
| Change classification of forced rewrites | PO.5 | CCC-02, CCC-03 | A.5.4, A.8.32 | N/A |
