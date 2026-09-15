# Corpus-Management pack (`.corpus-management/`)

**Status: ACTIVE (umbrella 4.1, compile PR-24).** This directory is the structure of a standalone,
adoptable Corpus-Management pack. PR-2 shipped the compiler, the first generated slice (the CLAUDE.md
generated-artefacts instruction block, transferred verbatim), and the mandatory drift gate (grc gate
99); PR-3 transferred the first authoring rule (the corpus language convention) as a generated
file-kind rule, the first live use of the rules-sync gate's compiler-owned recognition; PR-4
transferred the second authoring rule (the corpus authoring conventions) as the second file-kind
rule. The gate register carries nineteen gate transfers (lint-language, grc gate 2, compile PR-5; lint-unbalanced-fences, grc gate 66, compile PR-6; lint-nested-markdown-links, grc gate 68, compile PR-7; lint-ungated-dashes, grc gate 82, compile PR-8; lint-bare-normative-shall, grc gate 56, compile PR-9; lint-links, grc gate 3, compile PR-10; lint-required-sections, grc gate 19, compile PR-11; lint-citations, grc gate 5, compile PR-12; lint-section-placement, grc gate 38, compile PR-13; lint-shall-near-uncertainty, grc gate 9, compile PR-14; lint-todo-marked-done, grc gate 57, compile PR-15; lint-positional-backlog-tokens, grc gate 69, compile PR-16; lint-stub-documents, grc gate 16, compile PR-17; lint-filename-title-alignment, grc gate 7, compile PR-18; lint-standards-currency, grc gate 6, compile PR-19; lint-directional-dependency, grc gate 53, compile PR-20; lint-roles, grc gate 8, compile PR-21; lint-placeholder-leakage, grc gate 12, compile PR-22; lint-gate-count-consistency, grc gate 39, compile PR-23); no hooks have been transferred yet.

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
- **PR-12:** the eighth gate transfer (lint-citations, grc gate 5, framework-citation denylist audit), Model-2 pattern, enforcing the new citation-denylist clause. Engine takes the DENYLIST + PATH_EXEMPTIONS + repo_root as parameters (config-free); the grc denylist stays in the wrapper. SHIPPED.
- **PR-13:** the ninth gate transfer (lint-section-placement, grc gate 38, section-order audit), Model-2 pattern, enforcing the new section-placement clause. Engine config-free (PLACEMENT_RULES + repo_root params); grc rules stay in the wrapper. SHIPPED.
- **PR-14:** the tenth gate transfer (lint-shall-near-uncertainty, grc gate 9), Model-2 pattern, enforcing the new shall-near-uncertainty clause. Marker patterns + window in the engine (generic check); grc exempt-files filter in the wrapper (engine repo_root-free). SHIPPED.
- **PR-15:** the eleventh gate transfer (lint-todo-marked-done, grc gate 57), Model-2 pattern, enforcing the new todo-forward-only clause. Cleanest yet: fully-generic check (no config), only the scan target in the wrapper. SHIPPED.
- **PR-16:** the twelfth gate transfer (lint-positional-backlog-tokens, grc gate 69), Model-2 pattern. FIRST direct-call-coupled transfer: the wrapper keeps a check_file SHIM (exempt-check + engine check) for a direct-call regression test, establishing the pattern for direct-call-coupled gates. SHIPPED.
- **PR-17:** the thirteenth gate transfer (lint-stub-documents, grc gate 16), Model-2 pattern, enforcing the new no-stub-documents clause. Stub-phrase list + threshold in the engine; target selection in the wrapper. SHIPPED.
- **PR-18:** the fourteenth gate transfer (lint-filename-title-alignment, grc gate 7), Model-2 pattern. Most param-heavy yet (synonyms + doctypes + min-overlap params); DOCTYPES stays a wrapper module attribute for the gate-67 cross-check. SHIPPED.
- **PR-19:** the fifteenth gate transfer (lint-standards-currency, grc gate 6), Model-2 pattern. Most-involved yet: engine gets compile+check+run (compiled patterns + counts + repo_root params); wrapper keeps the canonical-register parse + the --root fixture-isolation override + error paths. SHIPPED.
- **PR-20:** the sixteenth gate transfer (lint-directional-dependency, grc gate 53), Model-2 pattern. Bespoke marker-aware fence handling + a 9-case self-test moved to the engine (project_gov_dir param); --self-test delegates. SHIPPED.
- **PR-21:** the seventeenth gate transfer (lint-roles, grc gate 8, Owner/Approving-Authority role audit), Model-2 pattern, enforcing the new role-authority clause. Engine holds the pure metadata-value check (patterns + is_placeholder + check_file + reporting run, known + repo_root params, bare relative_to like gate 56); the wrapper keeps the role-authority register parse (load_known_roles) + the EXTRA_KNOWN_ROLES allow-list + the register-prerequisite exit 2 + the --root override (proven by PR-19). SHIPPED.
- **PR-22:** the eighteenth gate transfer (lint-placeholder-leakage, grc gate 12, placeholder-leakage audit), Model-2 pattern, enforcing the new placeholder-leakage clause. PATTERNS marker set + fence-aware scan + reporting run (repo_root param, try/except display fallback) in the engine; the exempt policy + iter_targets in the wrapper. The lint-pii-in-content cross-reference proved to be prose-only (no code coupling). SHIPPED.
- **PR-23:** the nineteenth gate transfer (lint-gate-count-consistency, grc gate 39), Model-2 pattern, enforcing the new gate-count-consistency clause. The HEAVIEST transfer (569L): PATTERNS + word-number machinery + scan_file (version-history aware; patterns anchored) moved byte-verbatim (diff-verified each block); the wrapper keeps the §6-spec parse + collection dirs + a scan_file shim for the importlib direct-load test. Completes the clean ALLOW-mapped tranche. SHIPPED.
- **PR-24 (Phase-4 PR-A):** the reference-vocabulary profile ENABLER, opening the Phase-4 genericize wave. A concern-agnostic `tools/profile_loader.py` (versioned TOML profiles under `defaults/grc/<concern>.toml`, key-level-replace adopter overlay, fail-closed envelope + regex-table compilation), the first shipped profile (`defaults/grc/citations.toml`, the framework-citation denylist mirrored VERBATIM from gate 5), the `core/profiles.toml` register, gate-99 profile validation (validate-when-declared; profiles are validated SOURCE, never owned/generated), and loader + compiler tests. Behaviourally INERT: gate 5 keeps its wrapper config until PR-B migrates it; a parity test bounds the two-place window. SHIPPED.
- **PR-25 (next):** Phase-4 PR-B, the first gate migration onto the profile loader (gate 5 citations: engine reads the profile, wrapper config removed, scan-scope ALLOW coupling handled deliberately) OR the heavier non-ALLOW corpus-bucket gates (the SHARED/SAFETY-mapped class, careful individual handling per gate-homes.toml).
- **Phase-2b: SKIP.** **Gate-98 (vendored-core digest): CORPUS interim.** **Publication: deferred (P4).**

See `core/manifest.toml` for the machine-readable pack descriptor.
