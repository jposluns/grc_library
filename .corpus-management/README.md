# Corpus-Management pack (`.corpus-management/`)

**Status: ACTIVE (umbrella 4.1, compile PR-11).** This directory is the structure of a standalone,
adoptable Corpus-Management pack. PR-2 shipped the compiler, the first generated slice (the CLAUDE.md
generated-artefacts instruction block, transferred verbatim), and the mandatory drift gate (grc gate
99); PR-3 transferred the first authoring rule (the corpus language convention) as a generated
file-kind rule, the first live use of the rules-sync gate's compiler-owned recognition; PR-4
transferred the second authoring rule (the corpus authoring conventions) as the second file-kind
rule. The gate register carries seven gate transfers (lint-language, grc gate 2, compile PR-5; lint-unbalanced-fences, grc gate 66, compile PR-6; lint-nested-markdown-links, grc gate 68, compile PR-7; lint-ungated-dashes, grc gate 82, compile PR-8; lint-bare-normative-shall, grc gate 56, compile PR-9; lint-links, grc gate 3, compile PR-10; lint-required-sections, grc gate, compile PR-11); no hooks have been transferred yet.

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
- **PR-4:** the second clause-transfer wave: the `authoring-conventions` file-kind rule (the corpus authoring conventions, transferred from the CLAUDE.md `## Conventions` section), the pack's second file-kind rule. SHIPPED.
- **PR-5:** the gate-wave opened: the first gate transfer (lint-language, grc gate 2), the engine moved to the pack tools/ as source of record behind a thin Model-2 wrapper, the gate register populated with compiler validation, and the id-history charter widened to pack-ids. SHIPPED.
- **PR-6:** the second gate transfer (lint-unbalanced-fences, grc gate 66), same Model-2 wrapper shape as PR-5. SHIPPED.
- **PR-7:** the third gate transfer (lint-nested-markdown-links, grc gate 68), same Model-2 wrapper shape as PR-5/6, enforcing the new markdown-link-integrity clause. First transfer sequenced by the gate-homes.toml classification. SHIPPED.
- **PR-8:** the fourth gate transfer (lint-ungated-dashes, grc gate 82), Model-2 pattern, REUSING the existing language-convention clause (no new clause/rule, unlike PR-6/PR-7). SHIPPED.
- **PR-9:** the fifth gate transfer (lint-bare-normative-shall, grc gate 56), Model-2 pattern, enforcing the new normative-wording clause (the FR-44 must-over-shall convention). The grc-specific EXEMPT_FILES filter moved to the wrapper so the engine is REPO_ROOT-free. SHIPPED.
- **PR-10:** the sixth gate transfer (lint-links, grc gate 3, broken-internal-link audit), Model-2 pattern, enforcing the new markdown-link-resolution clause. Engine made repo_root-free (the containment check took a repo_root parameter). SHIPPED.
- **PR-11:** the seventh gate transfer (lint-required-sections, required-sections-by-doctype audit), Model-2 pattern, enforcing the new required-sections clause. The engine takes the section MODEL (required_map) + repo_root as parameters (config-free); the grc REQUIRED_SECTIONS model stays in the wrapper. SHIPPED.
- **PR-12 (next):** further corpus-bucket gate transfers (clean ALLOW-mapped candidates: lint-citations, lint-roles, lint-section-placement, lint-stub-documents, ...) and/or the vocabulary/config split to `defaults/grc/` (Phase-4).
- **Phase-2b: SKIP.** **Gate-98 (vendored-core digest): CORPUS interim.** **Publication: deferred (P4).**

See `core/manifest.toml` for the machine-readable pack descriptor.
