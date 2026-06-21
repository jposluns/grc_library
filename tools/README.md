# Repository tooling

This directory contains repository quality tooling. The scripts are intentionally minimal: they run with the standard Python 3 interpreter, take no third-party dependencies, and are designed to be invoked locally, by pre-commit, or by CI.

## Scripts

The library's audit programme consists of **45 gates** (linters, build-and-check generators, and the linter regression test suite). The canonical inventory of every gate, with its name, script, and category, is maintained in [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6. Gate 35 (gate-name parity audit) enforces that the §6 inventory, the CI workflow, the local runner, and the pre-commit config declare identical gates with identical names; the inventory is the single source of truth.

To see the current gate set in one place, run [`tools/run_all_audits.sh`](run_all_audits.sh) or read the §6 table.

Each individual linter is self-documenting via its module docstring (`python3 tools/<script>.py --help` where supported, or read the docstring directly). The shared helper module is [`tools/lint_common.py`](lint_common.py); the regression test suite is at [`tools/run-linter-regression.py`](run-linter-regression.py) with fixtures under [`tests/test_linters.py`](../tests/test_linters.py).

## Running

Run the full audit programme from the repository root:

```
bash tools/run_all_audits.sh
```

This runs all 45 gates in the order defined in [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6 and aggregates results. Use `FAIL_FAST=1 bash tools/run_all_audits.sh` to stop on first failure.

Individual scripts also run standalone:

```
python3 tools/lint-metadata.py
python3 tools/lint-language.py ai security    # restrict scope to specific paths
python3 tools/build-taxonomy.py --check        # regen-and-check
```

Each script prints `OK: ...` on a clean run and exits zero. On findings it prints a grouped report and exits one (or two for environmental failure, e.g., a missing register).

To regenerate the auto-generated artefacts after editing metadata, run without `--check`:

```
python3 tools/build-taxonomy.py
python3 tools/build-portal.py
```

The portal generator depends on the taxonomy; always regenerate the taxonomy first.

## Pre-commit integration

[`.pre-commit-config.yaml`](../.pre-commit-config.yaml) at the repository root wires all 45 gates as local hooks. Install once:

```
pip install pre-commit
pre-commit install
```

Subsequent commits run the full 45-gate audit programme before the commit is finalised. Run on demand against the entire corpus:

```
pre-commit run --all-files
```

## Continuous integration

[`.github/workflows/quality.yml`](../.github/workflows/quality.yml) runs the same 45 gates on every push to `main` and on every pull request. The CI environment uses Python 3.11 from `actions/setup-python`. No third-party dependencies are installed.

## Exemptions

- Draggable AI-context rule files under `dev-security/claude-rules/` are exempt from the metadata and structural audits because they serve a different purpose (loaded into AI coding sessions, not consumed as governance documents).
- Tooling docs in this directory and adopter docs in `docs/` are exempt from the structural audit.
- The deprecated [`privacy/annex-regional-privacy-requirements.md`](../privacy/annex-regional-privacy-requirements.md) is exempt from the structural audit (retained for history; superseded by [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md) and the jurisdiction subfolder).

## Exploratory tools (not gates)

Some scripts in this directory are exploratory tools the maintainer runs on demand rather than verification gates wired into the audit programme. They exit 0 on every run (they surface findings; they do not fail). The set:

- [`tools/detect-collection-candidates.py`](detect-collection-candidates.py): heuristic detector for new candidate collections that should be added to gate 41 (Collection-enumeration consistency audit). Walks candidate-source roots, scores each subdirectory's items against corpus markdown files for coverage, and surfaces candidates with rationale for the maintainer to triage one-by-one. Companion to gate 41's hard-coded configuration.
