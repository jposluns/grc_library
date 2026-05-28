# Repository tooling

This directory contains repository quality tooling. The scripts are intentionally minimal: they run with the standard Python 3 interpreter, take no third-party dependencies, and are designed to be invoked locally, by pre-commit, or by CI.

## Scripts

| Script | Purpose |
| --- | --- |
| `lint-metadata.py` | Asserts the canonical 13-field metadata block on every active document, validates Document Type against the allowed list, checks `Version` (semver) and `Date` (ISO 8601), asserts role-based Owner and Approving Authority, asserts `License` equals `CC0 1.0 Universal`, asserts Repository Path matches the file's actual path, and asserts filename prefix matches Document Type. |
| `lint-language.py` | Audits em and en dashes, British `-ise` endings, bare `ensure` or `ensures` without `that`, sentence-case heading rule (H2 to H6), and leaked sanitisation-table source terms outside the ingestion specification. Skips fenced code blocks and the specs' own rule statements. |
| `lint-links.py` | Validates that every relative markdown link target inside the repository resolves to a file that exists. External links (http, https, mailto, tel, ftp) and fragment-only anchors are ignored. Skips fenced code blocks. |
| `lint-structure.py` | Asserts that every active markdown file appears in its domain README's Active Documents table and in `governance/register-document-index-and-classification.md`, and that every reference in those tables points to a file that exists. |
| `lint-citations.py` | Denylist-based audit flagging known-hallucinated or known-stale framework version strings (for example, "COBIT 2025" when ISACA's current version is COBIT 2019). |
| `lint-roles.py` | Asserts that every Owner and Approving Authority value across active documents is defined in `governance/register-role-authority.md` (plus a small set of exemptions). |
| `lint-shall-near-uncertainty.py` | Detects mandatory-requirement language ("shall", "must") sitting near uncertainty markers ("may", "should consider", "to be determined") within the same sentence; flags ambiguous obligations. |
| `lint-standards-currency.py` | Positive-list audit. Parses `governance/register-canonical-citations.md` and flags references to versions listed as superseded in the canonical register. Complementary to `lint-citations.py`: the denylist tool catches hallucinations; the currency tool catches stale-but-real references. |
| `check-review-cadence.py` | Per-document review cadence audit. Compares each document's `Date` field and `Review Frequency` field against the current date; flags documents past their review window. |
| `build-taxonomy.py` | Generates the machine-readable `taxonomy.yml` registry from the canonical metadata block of every active artefact. Running with `--check` asserts the on-disk taxonomy is in sync with current document metadata; suitable for CI and pre-commit. |
| `build-portal.py` | Generates `docs/portal.md` (adopter portal keyed by audience) and `docs/maturity-scorecard.md` (per-document maturity classification) from `taxonomy.yml`. Running with `--check` asserts both derived files are in sync; suitable for CI and pre-commit. |

## Running

Run from the repository root:

```
python3 tools/lint-metadata.py
python3 tools/lint-language.py
python3 tools/lint-links.py
python3 tools/lint-structure.py
python3 tools/build-taxonomy.py --check
```

Each script prints `OK: ...` on a clean run and exits zero. On findings it prints a grouped report and exits one. Optionally pass file or directory paths to restrict the lint scripts' scope:

```
python3 tools/lint-language.py ai security
```

To regenerate the taxonomy after editing artefact metadata, run without `--check`:

```
python3 tools/build-taxonomy.py
python3 tools/build-portal.py
```

The portal generator depends on the taxonomy; always regenerate the taxonomy first.

## Pre-commit integration

`.pre-commit-config.yaml` at the repository root wires all four scripts as local hooks. Install once:

```
pip install pre-commit
pre-commit install
```

Subsequent commits run all four audits before the commit is finalised. Run on demand against the entire corpus:

```
pre-commit run --all-files
```

## Continuous integration

`.github/workflows/quality.yml` runs the same four audits on every push to `main` and on every pull request. The CI environment uses Python 3.11 from `actions/setup-python`. No third-party dependencies are installed.

## Exemptions

- Draggable AI-context rule files under `dev-security/claude-rules/` are exempt from the metadata and structural audits because they serve a different purpose (loaded into AI coding sessions, not consumed as governance documents).
- Tooling docs in this directory and adopter docs in `docs/` are exempt from the structural audit.
- The deprecated `privacy/annex-regional-privacy-requirements.md` is exempt from the structural audit (retained for history; superseded by `privacy/annex-privacy-jurisdiction-index.md` and the jurisdiction subfolder).
