# Repository tooling

This directory contains repository quality tooling. The scripts are intentionally minimal: they run with the standard Python 3 interpreter, take no third-party dependencies, and are designed to be invoked locally, by pre-commit, or by CI.

## Scripts

| Script | Purpose |
| --- | --- |
| `lint-metadata.py` | Asserts the canonical 13-field metadata block on every active document, validates Document Type against the allowed list, checks `Version` (semver) and `Date` (ISO 8601), asserts role-based Owner and Approving Authority, asserts `License` equals `CC0 1.0 Universal`, asserts Repository Path matches the file's actual path, and asserts filename prefix matches Document Type. |
| `lint-language.py` | Audits em and en dashes, British `-ise` endings, bare `ensure` or `ensures` without `that`, sentence-case heading rule (H2 to H6), and leaked sanitisation-table source terms outside the ingestion specification. Skips fenced code blocks and the specs' own rule statements. |
| `lint-links.py` | Validates that every relative markdown link target inside the repository resolves to a file that exists. External links (http, https, mailto, tel, ftp) and fragment-only anchors are ignored. Skips fenced code blocks. |
| `lint-structure.py` | Asserts that every active markdown file appears in its domain README's Active Documents table and in `governance/register-document-index-and-classification.md`, and that every reference in those tables points to a file that exists. |

## Running

Run from the repository root:

```
python3 tools/lint-metadata.py
python3 tools/lint-language.py
python3 tools/lint-links.py
python3 tools/lint-structure.py
```

Each script prints `OK: ...` on a clean run and exits zero. On findings it prints a grouped report and exits one. Optionally pass file or directory paths to restrict scope:

```
python3 tools/lint-language.py ai security
```

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
