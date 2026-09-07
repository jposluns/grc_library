# Corpus-Management pack (`.corpus-management/`)

**Status: ACTIVE (umbrella 4.1, compile PR-4).** This directory is the structure of a standalone,
adoptable Corpus-Management pack. PR-2 shipped the compiler, the first generated slice (the CLAUDE.md
generated-artefacts instruction block, transferred verbatim), and the mandatory drift gate (grc gate
99); PR-3 transferred the first authoring rule (the corpus language convention) as a generated
file-kind rule, the first live use of the rules-sync gate's compiler-owned recognition; PR-4
transferred the second authoring rule (the corpus authoring conventions) as the second file-kind
rule. No corpus gates or hooks have been transferred into the pack registers yet.

## What this is
A **thin, adoptable layer** for keeping a documentation corpus internally consistent (metadata shape,
section model, citation currency, cross-links), built on top of the **AIQT generic core** rather than
duplicating it. The generic file/text/date/git/metadata primitives come from the vendored
`aiqt_corpus` module (dependency-model B; see `vendor/aiqt/`); this pack adds only the corpus-specific
policy: the fixed metadata structure, the register grammar, and the corpus gates/hooks. AIQT provides
policy-free primitives, not a corpus compiler; this pack is that compiler's source of record.

## Source-of-record discipline
`.corpus-management/` is the **authoritative source**. Generated outputs (rules, CLAUDE.md blocks,
gate/hook wiring) are produced FROM this tree by the compiler (`tools/corpus_mgmt_compiler.py`,
wrapped by the project's `tools/build-corpus-management.py`) and are **never edited directly**; edit
the source here and regenerate. The drift gate (grc gate 99, the wrapper's `--check` form) enforces
byte-parity with nothing stripped before comparison.

## Scan boundary (why this directory is exempt from corpus-content gates)
This is pack SOURCE, not corpus content, so the corpus-content validators do not select it (a
root-anchored exemption, matched on the first path component only, so nested lookalikes such as
`governance/.corpus-management/` are NOT exempt). The security and cross-cutting operational audits
(secrets, PII, internal-references, external-link-domains, narrative-boundary, and prose dash-style)
**still apply** to this tree; the exemption is from corpus-document-model validation only, not a blanket
skip. (The stdlib-only-imports and unused-import gates scan the pack's `tools/` tree, which ships
Python since PR-2.)

## Structure (fixed) vs vocabulary (configurable)
The metadata STRUCTURE is fixed (every document carries the same field set and section model, which is
what makes the corpus machine-auditable). The VOCABULARY (allowed values, jurisdiction lists, framework
identifiers) is configurable per adopter via profiles under `defaults/`.

## Reference and operational registers
Reference defaults ship under `defaults/grc/` and are overridable by an adopter. Operational registers
(a project's private working state) are **project-only** and are never shipped by this pack.

## Optional semantic add-ons
The reference-dependent semantic audits (matrix-fit, claim-fit, reference-audit) are OPTIONAL add-ons
that require an adopter to supply a reference base; they are listed in the manifest as available but
disabled in the skeleton.

## Rollout
- **PR-1:** inert scaffold + the root-anchored scan-boundary exemption + scope tests. SHIPPED.
- **PR-2:** the compiler + the first generated vertical slice + the mandatory drift gate (grc gate 99). SHIPPED.
- **PR-3:** the first clause-transfer wave: the `language-convention` file-kind rule generated to `.claude/rules/corpus-management/` (first live gate-37 recognition), plus the tree-child containment hardening (routed from #2038). SHIPPED.
- **PR-4 (this):** the second clause-transfer wave: the `authoring-conventions` file-kind rule (the corpus authoring conventions, transferred from the CLAUDE.md `## Conventions` section), the pack's second file-kind rule. SHIPPED.
- **PR-5 (next):** further clause transfers (per-clause file-kind rules); the tree-kind decision is deferred to the wave that needs it.
- **Phase-2b: SKIP.** **Gate-98 (vendored-core digest): CORPUS interim.** **Publication: deferred (P4).**

See `core/manifest.toml` for the machine-readable pack descriptor.
