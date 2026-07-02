# Cross-file section-reference gate: design, FP lessons, and pause record

**Status:** PAUSED pending FR-48 §1.1 completion (maintainer-directed 2026-07-02). Build and
ship the gate against the FULLY-NUMBERED corpus, not the mid-migration one. This file preserves
the design, the corpus survey, and the two false-positive lessons so resuming is fast; the gate
MUST be re-run and re-verified against the post-FR-48 corpus (the corpus changes materially as
the ~13 remaining hard-class docs are renumbered).

This file is maintainer working state, exempt from corpus audit gates.

## Why paused (the sequencing dependency)

The numbers-phase gate validates that every cross-file `Section N` / `§N` reference resolves to a
real heading in the target document. It can only check refs to *numbered* targets. During the
FR-48 renumber migration the corpus is in mixed states, which has two consequences that make
building the gate now premature:

1. **Incomplete coverage that looks green.** Refs into not-yet-numbered deferred docs are skipped
   (the unnumbered-target rule), so a gate shipped mid-migration would pass while silently not
   covering those refs.
2. **One genuine blocking finding, coupled to FR-48.** A corpus-wide run found exactly one
   unresolvable ref: `risk/procedure-risk-acceptance.md:41` cites `policy-exception-and-risk-
   acceptance-management.md §2.2`, but that policy has no `§2.2` (unnumbered H2s, flat H3s that
   reset per H2). That policy is on the FR-48 §1.1 deferred hard-class worklist; the citer is one
   of its lockstep inbound `§N` refs and resolves when the policy is renumbered. Fixing the citer
   standalone now would be re-touched by that renumber (throwaway).

Building after FR-48 gives full coverage, resolves the blocker for free, and avoids locking the
design to a transitional corpus. During FR-48, run the (preserved) gate ADVISORY-ly after each
renumber to catch the #548-class cross-file remap miss mechanically.

## Design (from the 2026-07-02 corpus survey; strict, low-false-positive)

**INCLUDE (fire only on these two high-confidence, resolvable-target classes):**

1. **Adjacent-link class**, in NON-TABLE lines only: a `§N` / `Section N` whose target doc is named
   by a markdown `.md` link within the same clause (within ~40 chars, no intervening pipe). Resolve
   the link, check the cited number is a heading in the target.
2. **Binding-declaration class**: a file carrying the sentinel `Section numbers below refer to that
   standard.` on a line that also links a target `.md` binds every subsequent bare `§N` / `Section
   N` in that file to that target. Six `dev-security/claude-rules/languages/*.md` files bind to
   `standard-mobile-application-security.md` this way (the #548 miss class).

**EXCLUDE (each is a documented recall cost, not a gap to close by loosening the gate):**

- **Table rows** (any line containing `|`): removes the ~150-row compliance-matrix + per-doc
  framework-table FP surface (external-framework clause numbers in cells next to a corpus-doc
  link). This is the single largest FP source; the non-negotiable exclusion.
- **External-standard context**: a line naming ISO / NIST / OWASP / GDPR / BASC / `Clause` /
  `Article` / `SP 800` etc. (its `§N` cites the external standard).
- **Unnumbered targets**: if the resolved target has zero numbered headings, skip (mirrors
  `lint-intra-doc-refs.py`'s early return; a numbered ref to an unnumbered target is not a
  stale-heading case).
- **Bare `§N` / `Section N` with no adjacent link and no active binding**: an intra-doc ref that
  `lint-intra-doc-refs.py` owns.
- **Name-based refs** (`§Governance`): no number to resolve.
- **Range second endpoints** (`Section 4-12`): only the first captured endpoint is checked.

**Reuse:** `lint-intra-doc-refs.py`'s heading-number regex (`^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]`) for `extract_sections`; `lint-section-anchors.py`'s `(base_dir / target_rel).resolve()` + `exists()` for target resolution; `lint_common` (`iter_markdown_targets`, `iter_non_code_lines`, `read_text_safe`, `REPO_ROOT`, `DEFAULT_EXEMPT_DIRS`). Add `CHANGELOG.md` to `EXEMPT_FILES`.

## The two false-positive lessons (from testing the first cut against the corpus)

Both were caught by running the gate on the corpus BEFORE wiring (test-first). Re-apply when
re-instantiating:

1. **Binding target = the `.md` link nearest-BEFORE the sentinel, not the first link on the line.**
   The language rule files list sibling docs (`typescript.md`, `swift.md`, `kotlin.md`) before the
   standard they bind to; the first-link heuristic resolved the binding to a sibling file (63 FPs).
   Fix: among links whose end precedes the sentinel match, take the last.
2. **Skip targets with zero numbered headings** (`if not target_sections: continue`). A `§7` ref to
   `procedure-library-quality-and-review-cadence.md` (all-unnumbered H2s) is not a stale ref; it is
   a ref to an unnumbered doc. Skipping mirrors `lint-intra-doc-refs.py`.

After both fixes the corpus-wide run returned exactly one finding (the `§2.2` blocker above), and
the gate correctly SKIPPED the in-table `§3` cross-file ref inside the same exception policy
(table-row exclusion working).

## Delivery shape when resumed (unchanged from the handoff plan)

Two PRs, always-split: numbers-phase gate first (this design), then a names-phase gate second
(FP-tuned: a ref pairing a number with a quoted heading title matches the target's actual heading).
Each is a new gate: full four-surface wiring (workflow / runner / pre-commit / §6 spec table + §5
grouped-list + §6 detailed-prose pair) + a regression fixture + a pre-push skeptical (or
high-assurance) verifier. Re-run corpus-wide and re-verify against the post-FR-48 corpus before
wiring; the gate ships green only when the corpus is clean of unresolvable cross-file refs.
