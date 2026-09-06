# Corpus-Management pack (`.corpus-management/`)

**Status: SKELETON (umbrella 4.1, PR-1).** This directory reserves the structure of a standalone,
adoptable Corpus-Management pack. PR-1 ships an inert scaffold only: no clauses have been transferred,
no gates or hooks are installed, and generation is disabled. Enforcement and the compiler arrive in PR-2.

## What this is
A **thin, adoptable layer** for keeping a documentation corpus internally consistent (metadata shape,
section model, citation currency, cross-links), built on top of the **AIQT generic core** rather than
duplicating it. The generic file/text/date/git/metadata primitives come from the vendored
`aiqt_corpus` module (dependency-model B; see `vendor/aiqt/`); this pack adds only the corpus-specific
policy: the fixed metadata structure, the register grammar, and the corpus gates/hooks. AIQT provides
policy-free primitives, not a corpus compiler; this pack is that compiler's source of record.

## Source-of-record discipline
`.corpus-management/` is the **authoritative source**. Once PR-2 installs the compiler, generated
outputs (rules, CLAUDE.md blocks, gate/hook wiring) are produced FROM this tree and are **never edited
directly**; edit the source here and regenerate. A drift gate will enforce byte-parity.

## Scan boundary (why this directory is exempt from corpus-content gates)
This is pack SOURCE, not corpus content, so the corpus-content validators do not select it (a
root-anchored exemption, matched on the first path component only, so nested lookalikes such as
`governance/.corpus-management/` are NOT exempt). The security and cross-cutting operational audits
(secrets, PII, internal-references, external-link-domains, narrative-boundary, and prose dash-style)
**still apply** to this tree; the exemption is from corpus-document-model validation only, not a blanket
skip. (The stdlib-only-imports gate scans this tree once the pack ships Python, in PR-2.)

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
- **PR-1 (this):** inert scaffold + the root-anchored scan-boundary exemption + scope tests.
- **PR-2:** the compiler + the first generated vertical slice + the mandatory drift gate.
- **Phase-2b: SKIP.** **Gate-98 (vendored-core digest): CORPUS interim.** **Publication: deferred (P4).**

See `core/manifest.toml` for the machine-readable pack descriptor.
