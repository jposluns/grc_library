# Linter regression tests

This directory contains regression tests for the audit-programme linters
in [`tools/`](../tools/). Each test:

1. Constructs a minimal synthetic markdown fixture that should trigger
   exactly one linter rule.
2. Invokes the target linter against the fixture.
3. Asserts that the linter exits non-zero and emits a finding
   matching the expected pattern.

The tests exist to catch a class of defect that no other gate in the
audit programme can catch: a regression in a linter's own detection
logic. If a future refactor accidentally weakens a regex or breaks an
exemption list, the corpus may still happen to be clean (no false
positives), but the linter no longer detects the violation class it
exists to detect. The regression tests catch this.

## Scope

The default test shape is a **positive test**: a fixture containing
exactly one violation, asserting the linter exits non-zero and emits
the expected finding. The suite also includes **negative tests**
(fixtures whose content is permissible in context and must not be
flagged, such as a template placeholder inside a template file, or a
placeholder string inside a fenced code block), and **environmental
tests** (a linter that depends on an external register must exit 2,
not 1, when the register is missing). The audit programme itself
provides additional implicit negative coverage by running every
linter against the clean corpus on every commit and expecting exit 0.

## Running

```
python3 -m unittest tests.test_linters -v
```

or via the audit programme:

```
tools/run_all_audits.sh
```

The regression suite runs as gate 33 of the audit programme. See
[`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6.

## Fixture isolation

Each test creates its fixture in a per-test temporary directory under
[`tests/tmp/`](tmp/) (created on demand). The temporary file is deleted
after the test. Tests pass explicit file paths to the linter under
test, so the linter does not scan the rest of the repository during
the test.

Isolation is provided by two complementary mechanisms:

1. **Per-test cleanup**: each test's `tearDown` deletes its
   fixture file, and `tests/test_linters.py` has a module-level
   `tearDownModule` that wipes any remaining `*.md` from `tests/tmp/`.
2. **`.gitignore`**: `tests/tmp/` is gitignored so a leftover
   fixture from a crashed test never enters version control.

Linters themselves do NOT exempt `tests/tmp/`. If a fixture from a
crashed test were to remain in the directory, the main
`tools/run_all_audits.sh` sweep would see it. In practice
`setUpModule` cleans the directory at the start of each test run, so
the only window for contamination is during a single-test crash
without `tearDown` — and the next `setUpModule` removes the file.

## Coverage

Each linter has its own `LinterTestCase` subclass (e.g. `LanguageLinterTests`,
`SecretsLinterTests`); the linter under test is identified by the
enclosing class, and individual test methods are named
`test_<rule>_<expected_outcome>` (e.g. `test_em_dash_flagged`,
`test_template_placeholder_domain_allowed_in_template_file`). Every
linter in the audit programme has at least one positive test for its
primary rule. Additional rule-specific, negative, and environmental
tests can be added as maintenance reveals the need.
