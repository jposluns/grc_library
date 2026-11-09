# Authoring conventions
- Mirror an existing same-type document's metadata and section shape rather than
  inventing one; changing the model means changing the linters that enforce it.
- External-standard citations must be accurate and current: `lint-citations.py` and
  `lint-standards-currency.py` reject hallucinated or stale references.
- Prose style is enforced by `lint-language.py`; do not fight the linter by hand.
