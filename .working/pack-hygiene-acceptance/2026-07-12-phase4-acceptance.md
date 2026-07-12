# §4.8 pack adoption-hygiene: Phase 4 acceptance sweep + routed-findings triage + close-out (2026-07-12)

Closes the four-phase pack adoption-hygiene programme (§4.8). Phases 1-3 merged
(#835-#840, #842, #845). This record is the Phase-4 acceptance sweep, the routed-findings
triage, and the programme close-out.

## 1. Acceptance sweep (decision-record PLAN section 12): PASS

- **Internal-reference pattern sweep over the pack:** the six scrubbed governance rules
  under `dev-security/claude-rules/governance/` carry ZERO out-of-pack relative links
  (`grep '](../../'` = 0) and ZERO "(in this project ...)" wiring instantiations. Two
  benign residual hits are NOT violations and were deliberately not targeted: a hypothetical
  "PR #158/#147" cross-reference EXAMPLE in `ai-assistant-workflow-disciplines.md` (teaching
  content, not a project instantiation) and `.claude/`/`.working/` as backticked CATEGORY
  names in `change-tracking.md` (generic examples). The Phase-3 skeptical verifier classified
  both INFO.
- **Sanctioned carriers only:** project references survive only in the two sanctioned
  carriers (the pack README version-history date/version columns; the skills' labelled
  `## Project wiring` sections). Gate 37 (claude-rules-sync) validates the pack/`.claude`
  sync and the overlay convention; it is green.
- **core/ ai/ languages/ pipeline/ byte-identical:** untouched by the scrub (the #845 diff
  contained no file under those pack subtrees).
- **Every removed passage in the ledger:** RM-SCRUB-1 holds the fourteen verbatim originals
  (Phase-3 verifier confirmed 1:1 against the six-rule diff).
- **All gates green:** 69/69 on `main` at the Phase-3 merge.
- **README claims true:** confirmed by the Phase-3 verifier (the "zero out-of-pack links /
  fourteen wirings / in-sync overlays" claims hold).

## 2. Routed-findings triage (from the worker's scoped-assessment-record; none dropped)

The worker's own 3-iteration fix loop applied ~25 in-window accuracy fixes into the delivered
Phase-2/3 payloads (all merged) and closed within the cap. The residual ROUTED items are
triaged here:

- **Packaging-model decisions (MAINTAINER, feed the public-site §2.4):** ~60 relative links
  escape the pack directory (Related Documents, the parent CHANGELOG as the pack's declared
  change-history source of truth, corpus cross-links); slash-command stubs are parent-only
  (not shipped with the pack); `/matrix-fit` and `/claim-fit` ground truth lives in a private
  reference base; `/add-files` in the pack README is unverified against current Claude Code
  command names. → tracked in TODO as the pack-distribution-packaging decision tied to §2.4.
- **Proposed cheap mechanizations (3):** a linter scanning skill bodies outside the wiring
  section for internal-reference tokens (convention-erosion guard); an instrument mapping
  "gate N (name)" citations in wiring sections/stubs to the §6 inventory (renumbering guard);
  the provenance register as a gate-41 enumeration surface (a new rule cannot ship without its
  entry). → tracked in TODO as guardrail-machinery candidates.
- **Apply-time command-stub co-updates (2):** the `/fitness` stub's ten-persona step heading;
  the `/retro` stub's concrete register format. → tracked in TODO (small).
- **Pre-existing accuracy items (small cleanup):** vetting-log "Spot-scanned" vocabulary +
  line-254 summary; the validation-sweep zero-finding record/register contradiction (pre-scrub);
  the session-lifecycle "prevented by luck" phrasing; `.working/README.md` activities inventory
  stale for 8 pre-existing subdirectories; adoption-path numbering (pack 1/2/3 vs adopter-guide
  A/B/C); root-README "claude.md" lowercase option headings. → tracked in TODO.
- **SP 800-154 "held source" accuracy item (MAINTAINER, protected-file):** the parent
  `.claude/CLAUDE.md` and pack rows describe SP 800-154 as a "held source" against a
  never-held / never-finalized record. → surfaced to the maintainer; tracked in TODO as a
  protected-file accuracy correction.
- **Two defensible-judgement flags (surfaced for the maintainer, NOT silently accepted):** the
  pack README twin's "shaped by the parent library's real maintenance practice" (holds on the
  weaker authored-within-a-live-programme reading, self-disclosed inline); "authoritative" for
  the reference-audit motivating source (inherited tier vocabulary; the verifier's zero-slack
  alternative is "an authoritative publisher's guidance"). → maintainer's call, tracked.

## 3. Programme close-out

- TODO §4.8 rotated to DONE (the four-phase programme is complete).
- §4.1 (corpus-management shareable skill) unblocks: its distillation source (the condensed
  governance rules) is now merged and adoption-clean.
- The public-site item (§2.4) may now feature and link a clean, project-agnostic merged pack;
  the packaging-model decisions above are its inputs.
