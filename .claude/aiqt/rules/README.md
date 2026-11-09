# Generated rule tree

These rules are GENERATED from `.aiqt/core/rules/` by `tools/gen_rules.py` and are checked in CI for drift.
Do not hand-edit `aiqt/` or `security/` here; edit the source and regenerate. The two-axis taxonomy:
`aiqt/` is numbered by AIQT priority (NN-CODE-slug; the apex is 00-project-integrity), `security/` is coded
by the CIA-plus-privacy model with family-namespaced codes SECC/SECI/SECA/SECP (Confidentiality, Integrity,
Availability, Privacy; CODE-slug), so no security code collides with an AIQT facet. The naming convention
for a coded subject family is a 3-letter family code plus a 1-letter facet letter, uppercase and hyphenless,
so a facet is always the single token before the first hyphen. Vendored packs live under `external/` and
are never touched.
