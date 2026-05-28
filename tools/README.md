# Repository tooling

This directory contains repository quality tooling. Tools are intentionally minimal: they run with the standard Python 3 interpreter, take no third-party dependencies, and are designed to be invoked locally or wired into CI in a later phase.

## lint-language.py

Audits the corpus for language and style rule violations defined in `specification-master-project.md` Section 6 and `specification-ingestion.md` Language requirements:

- Em dashes and en dashes.
- British `-ise` endings (use `-ize` instead).
- Bare `ensure` or `ensures` without `that`.
- Section headings (H2 through H6) that fail the sentence-case rule after stripping common numbering prefixes (`A1.`, `1.1`, `Step 1:`, `Category 1:`).
- Sanitisation-table source terms appearing outside the ingestion specification.

The audit skips fenced code blocks and the specifications' own self-referential statements of the rules. It accepts a small allowlist of canonical lowercase project names (e.g. `promptfoo`, `garak`).

Run from the repository root:

```
python3 tools/lint-language.py
```

Optionally pass file or directory paths to restrict the scope:

```
python3 tools/lint-language.py ai security
```

The script exits zero on a clean run and non-zero when findings are reported, so it can be used directly in pre-commit or CI configurations.

## Planned tooling

A complementary `lint-metadata.py` (asserts the 13-field metadata block, allowed document types, ISO 8601 dates, role-only Owner and Approving Authority, and the License field) is in scope for the automation phase of the improvement plan. CI integration will follow once both scripts are in place.
