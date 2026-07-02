# Gate Discipline

Never weaken or delete a gate to silence a failure. Fix the artefact that is failing.

A "gate" is any deterministic pass/fail check that guards a workflow:
- CI lint rules, type checks, test suites, coverage thresholds
- Security scans (SAST, SCA, secret scanners, IaC scanners, container image scans)
- Audit programmes (custom linters, schema validators, contract tests)
- Pre-commit hooks
- Required-review and required-status-check branch protections
- Generator-output `--check` modes and drift detectors

When a gate fails, it is reporting a real defect in the artefact. The cost of the defect, typically far higher than the cost of fixing it, is what justifies the gate's existence. Disabling the gate to ship the artefact monetizes the gate's cost (slow CI, blocked commits) while throwing away its benefit (the deferred cost of the defect plus every future defect the gate would have caught).

This rule applies equally to human developers and to AI coding assistants. An AI assistant that responds to a failing gate by suppressing it is, in this respect, indistinguishable from a junior developer who does the same; the resolution is identical: fix the artefact, not the gate.

---

## Prohibited responses to a failing gate

These responses must never be the resolution for a failing gate without explicit, documented approval from the responsible governance authority (CISO, library maintainer, or the designated reviewer named in the relevant policy):

- **`--no-verify` on `git commit`**. Bypasses pre-commit hooks. Use only when a hook is itself broken and you have a separate plan to fix the hook.
- **Force-pushing past a failing required check**. Defeats branch protection by construction. Force-push to a protected branch is prohibited; force-push to a feature branch is acceptable for legitimate rebasing but not as a workaround for a failing check.
- **Lowering a severity threshold to silence a finding**. Changing "fail on High" to "fail on Critical" silences the High finding rather than fixing it. Severity thresholds are policy decisions, not knobs for individual PRs.
- **Adding the failing file or rule to an exemption list or allowlist**. Allowlists exist for the small population of legitimate exceptions documented in the policy. Drive-by additions when something is inconvenient defeat the audit programme's invariants.
- **Deleting failing test cases**. A test that is currently failing is signal. Either the test is correct (fix the code) or the test is wrong (fix or remove the test for a documented reason recorded in the same commit, and update the test plan).
- **Lowering coverage or quality thresholds in CI config to make a PR pass**. Same anti-pattern as severity thresholds, applied to coverage.
- **Adding blanket suppression directives** (`# noqa`, `// eslint-disable`, `// @ts-ignore`, `// @ts-nocheck`, `# type: ignore`, `# nosec`, `pragma: no cover`) without a documented rationale on the same line. Targeted suppressions with a one-line rationale are sometimes legitimate; blanket file-level or repository-level suppressions are not.
- **Replacing an assertion with logging**. A logged warning is not the same as a failed check. The pipeline keeps running; the defect ships.
- **Marking a CI job non-required to dodge branch protection**. If a check is worth running, it is worth blocking on. Demoting a required check to optional is a policy change subject to the same review as any other policy change.
- **Wrapping a check in `|| true`, `set +e`, `try/except: pass`, or `set -e` removal**. Any pattern that swallows the gate's exit code defeats it.
- **Re-running CI until it passes by coincidence**. Treating intermittent failures as "flakes" without diagnosis hides real race conditions and timing-dependent defects.

---

## Correct responses to a failing gate

In order of preference:

1. **Fix the artefact**. Almost always the right answer. The gate exists because the defect class matters; the defect class is present in this artefact; fix it.
2. **If the gate is wrong** (genuine false positive, stale rule, environmental fluke), fix the gate. Document why in the same commit. Treat the gate-fix as a substantive change subject to the same review discipline as any other code change.
3. **If the gate is right but the artefact cannot be fixed in this PR** (cross-team coordination, tooling limitation, downstream migration, vendor patch outstanding), file a tracked issue with a remediation deadline, add a documented exception with the issue link as justification, and surface the exception in the next governance review. The exception is temporary by construction; renewal requires re-approval.
4. **If the artefact and the gate are both correct and the failure is environmental** (CI runner OOM, network flake, transient dependency outage), re-run. If the flake recurs, document it so the gate can be hardened; do not normalize re-running as a strategy.

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

If a pre-commit hook is failing legitimately, fix the underlying issue and create a new commit. If the hook itself is broken, fix the hook in its own commit and explain why in the message.

### Linting (Python example; same principle in every language)

```python
# PROHIBITED: blanket suppression
# ruff: noqa
# flake8: noqa

# PROHIBITED: line-level suppression with no rationale
result = some_call()  # noqa

# ACCEPTABLE: targeted suppression with documented rationale on the same line
result = some_call(default=mutable_default)  # noqa: B008 (mutable default intentional per ADR-0042)
```

### Type checking

```typescript
// PROHIBITED: file-level type-check disable
// @ts-nocheck

// PROHIBITED: line-level ignore with no rationale
const value = parseInput(raw) as MyType; // @ts-ignore

// ACCEPTABLE: targeted with rationale
const value = parseInput(raw) as MyType; // parseInput guarantees runtime shape per its contract test
```

### Test suites

```python
# PROHIBITED: silencing a failing test to make CI green
@pytest.mark.skip
def test_authorization_blocks_cross_tenant_access():
    ...

# CORRECT: investigate. The test is either:
#   - revealing a real authorization defect (fix the code), or
#   - itself wrong (fix or remove for a documented reason recorded in the commit message)
```

### CI/CD configuration

```yaml
# PROHIBITED: making a real gate non-required
- name: Security scan
  run: security-scan
  continue-on-error: true   # gate is now decorative

# PROHIBITED: swallowing exit codes in the script
- name: Lint
  run: ruff check . || true

# CORRECT: gate fails the job; fix the artefact or the gate
- name: Security scan
  run: security-scan
```

### Generator-output drift checks

```bash
# PROHIBITED: regenerating the artefact in CI to make the drift check pass
python3 build-taxonomy.py        # in CI: defeats the check

# CORRECT: the local maintainer regenerates and commits the regenerated artefact;
# CI runs --check mode and fails on uncommitted drift
python3 build-taxonomy.py --check  # in CI: reports drift, blocks merge
```

---

## Exception-handling protocol

Some controls have legitimate exception paths. The exception process is not a bypass; it is a separate, slower control with its own assurance:

1. The requestor documents the technical reason fixing the artefact is impractical in this PR.
2. The requestor proposes a remediation deadline (default 30 days; longer requires governance authority approval).
3. The responsible governance authority reviews and approves, modifies, or denies.
4. The approved exception is recorded in the project's exception register with the approver, date, scope, and deadline.
5. The PR carries a link to the exception entry.
6. Before the deadline, the requestor either remediates or requests renewal; unrenewed exceptions automatically lapse and the next CI run blocks.

If the project does not have an exception register, the exception is not available; fix the artefact.

---

## Framework alignment

| Requirement | OWASP ASVS | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- | --- |
| No bypass of security gates | V14.2 | PO.5, PW.7 | CEK-10 to 21, CCC-04 | A.8.28 |
| Documented exceptions to controls | V1.1 | PO.5 | GRC-04 | A.5.4 |
| Gate-effectiveness review | V14.1 | RV.1 | GRC-05 | A.5.36 |
| Change-management for control modifications | V1.1 | PO.5 | CCC-01 to 03 | A.5.4 |

---

## Why this rule exists

Audit and governance programmes derive their value from being unconditional. A "gate" that can be silenced when inconvenient is not a gate; it is decoration. The maintainability cost of fixing the artefact is bounded and accrues to the team that introduced the defect. The cost of letting one defect through accrues to every future user of the artefact and compounds with every subsequent defect the gate would have caught. The asymmetry justifies the discipline.

The exception process exists precisely so that legitimate, time-bounded deviations are possible without normalizing bypass as a routine response. If the exception process feels burdensome, that is the control working as designed: the friction is proportional to the residual risk of holding a known defect open.

For AI coding assistants specifically: when a gate fails, do not propose suppressing it as a first move. Diagnose the failure, propose a fix to the artefact, and surface the choice to the human operator. If the operator wants to suppress, that decision is theirs, documented under the exception process; it is not yours to make unilaterally.
