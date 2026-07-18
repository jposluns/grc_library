# Gate Discipline

Never weaken or delete a gate to silence a failure. Fix the artefact that is failing.

A "gate" is any deterministic pass/fail check that guards a workflow: CI lint rules, type checks, test suites, coverage thresholds; security scans (SAST, SCA, secret scanners, IaC scanners, container image scans); audit programmes (custom linters, schema validators, contract tests); pre-commit hooks; required-review and required-status-check branch protections; generator-output `--check` modes and drift detectors.

A failing gate is reporting a real defect. The cost of the defect is higher than the cost of fixing it, which is what justifies the gate; disabling the gate to ship the artefact throws away that benefit. The rule binds human developers and AI assistants identically: fix the artefact, not the gate.

---

## Prohibited responses to a failing gate

Never resolve a failing gate by any of these without explicit, documented approval from the responsible governance authority (CISO, maintainer, or the reviewer the policy names):

- **`--no-verify` on `git commit`** (bypasses pre-commit hooks). Only when a hook is itself broken and you have a separate plan to fix the hook.
- **Force-pushing past a failing required check.** Force-push to a protected branch is prohibited; to a feature branch it is fine for rebasing but not as a workaround for a failing check.
- **Lowering a severity threshold to silence a finding** (e.g. "fail on High" to "fail on Critical"). Thresholds are policy, not per-PR knobs.
- **Adding the failing file or rule to an exemption list or allowlist.** Allowlists are for the documented legitimate exceptions, not drive-by additions.
- **Deleting failing test cases.** A failing test is signal: fix the code, or fix/remove the test for a documented reason recorded in the same commit and update the test plan.
- **Lowering coverage or quality thresholds** in CI config to make a PR pass.
- **Blanket suppression directives** (`# noqa`, `// eslint-disable`, `// @ts-ignore`, `// @ts-nocheck`, `# type: ignore`, `# nosec`, `pragma: no cover`) without a same-line rationale. Targeted suppressions with a one-line rationale are sometimes legitimate; blanket file- or repo-level ones are not.
- **Replacing an assertion with logging.** A logged warning is not a failed check; the defect ships.
- **Marking a CI job non-required** to dodge branch protection. Demoting a required check is a policy change subject to the same review as any other.
- **Wrapping a check in `|| true`, `set +e`, `try/except: pass`, or removing `set -e`.** Any pattern that swallows the exit code defeats the gate.
- **Re-running CI until it passes by coincidence.** Treating failures as "flakes" without diagnosis hides real race conditions.

---

## Correct responses to a failing gate

In order of preference:

1. **Fix the artefact.** Almost always right: the defect class matters, it is present, fix it.
2. **If the gate is wrong** (genuine false positive, stale rule, environmental fluke), fix the gate and document why in the same commit, as a substantive change under normal review.
3. **If the gate is right but the artefact cannot be fixed in this PR** (cross-team, tooling limitation, downstream migration, vendor patch outstanding), file a tracked issue with a remediation deadline, add a documented exception linking the issue, and surface it in the next governance review. The exception is temporary; renewal requires re-approval.
4. **If both artefact and gate are correct and the failure is environmental** (runner OOM, network flake, transient outage), re-run; if the flake recurs, harden the gate rather than normalizing re-runs.

A failure is signal. The first question is "what does it mean?", not "how do I make it go away?"

---

## Specific anti-patterns by tool

### Git

```bash
# PROHIBITED: bypassing pre-commit hooks
git commit --no-verify
# PROHIBITED: skipping commit signing where required
git commit --no-gpg-sign
# PROHIBITED: rewriting history to remove a failing-CI commit instead of fixing it
git reset --hard HEAD~1 && git push --force
```

If a pre-commit hook fails legitimately, fix the underlying issue and make a new commit. If the hook itself is broken, fix the hook in its own commit and explain why.

### Linting (Python example; same principle in every language)

```python
# PROHIBITED: blanket suppression
# ruff: noqa
# PROHIBITED: line-level suppression with no rationale
result = some_call()  # noqa
# ACCEPTABLE: targeted suppression with documented rationale on the same line
result = some_call(default=mutable_default)  # noqa: B008 (mutable default intentional per ADR-0042)
```

### Type checking

```typescript
// PROHIBITED: file-level disable  // @ts-nocheck
// PROHIBITED: line-level ignore with no rationale
const value = parseInput(raw) as MyType; // @ts-ignore
// ACCEPTABLE: targeted with rationale
const value = parseInput(raw) as MyType; // parseInput guarantees runtime shape per its contract test
```

### Test suites

```python
# PROHIBITED: silencing a failing test to make CI green
@pytest.mark.skip
def test_authorization_blocks_cross_tenant_access(): ...
# CORRECT: investigate. The test is revealing a real defect (fix the code) or is
# itself wrong (fix or remove for a documented reason recorded in the commit message).
```

### CI/CD configuration

```yaml
# PROHIBITED: making a real gate non-required
- name: Security scan
  run: security-scan
  continue-on-error: true   # gate is now decorative
# PROHIBITED: swallowing exit codes
- run: ruff check . || true
# CORRECT: gate fails the job; fix the artefact or the gate
- name: Security scan
  run: security-scan
```

### Generator-output drift checks

```bash
# PROHIBITED: regenerating the artefact in CI to make the drift check pass
python3 build-taxonomy.py            # in CI: defeats the check
# CORRECT: maintainer regenerates and commits; CI runs --check and fails on drift
python3 build-taxonomy.py --check
```

---

## Exception-handling protocol

**Strict mode is the default: if the project has no exception register, there is no exception path; fix the artefact.**

Some controls have a legitimate exception path. It is a separate, slower control, not a bypass:

1. The requestor documents why fixing the artefact is impractical in this PR.
2. The requestor proposes a remediation deadline (default 30 days; longer needs governance-authority approval).
3. The responsible authority approves, modifies, or denies.
4. The approved exception is recorded in the project's exception register with approver, date, scope, and deadline.
5. The PR links the exception entry.
6. Before the deadline the requestor remediates or requests renewal; unrenewed exceptions lapse and the next run blocks.

---

## Framework alignment

| Requirement | OWASP ASVS | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- | --- |
| No bypass of security gates | V14.2 | PO.5, PW.7 | CEK-10 to 21, CCC-04 | A.8.28 |
| Documented exceptions to controls | V1.1 | PO.5 | GRC-04 | A.5.4 |
| Gate-effectiveness review | V14.1 | RV.1 | GRC-05 | A.5.36 |
| Change-management for control modifications | V1.1 | PO.5 | CCC-01 to 03 | A.5.4 |

---

*The why-this-rule-exists narrative is retained in the parent library's removal ledger (the two-layer condense): it is motivating rationale, not operative instruction. The framework-alignment table above is kept in the rule (the pack README names the rule as the source of truth for framework alignment; it is distributed traceability, not cut).*

<!-- PROJECT-OVERLAY: not part of the distributable pack -->

## Project overlay (grc_library wiring and lineage; local copy only)

- The removal ledger the footer names: `grc_library_private/claude-rules-considerations.md`
  (this rule's why-section moved there in the GR-P2 two-layer condense, PR #726).
- This project offers NO exception register: a failing gate means fix the artefact
  or descope the PR (the strict-mode stance in the project CLAUDE.md Boundaries).
