# Overlay provenance and precedence

This directory is a **supplementary** third-party rules overlay, not part of the
primary GRC governance pack. The primary pack under
[`guardrails/`](../../../../guardrails/) is the
authoritative source.

- **Precedence:** on any conflict between this overlay and the primary GRC pack, the
  **primary pack wins**. The overlay adds engineering-practice guidance that overlaps
  or supplements the primary layer; it never overrides it.
- **Source and licence:** `tikitribe` (see this directory's `LICENSE` for the upstream
  licence and attribution). Content is used under that licence.
- **Pruning / refresh stance:** the overlay is reviewed at each periodic pack review.
  A near-duplicate wrapper that the primary pack already covers is a prune candidate;
  a stale upstream file is refreshed from the source or dropped rather than allowed to
  diverge silently. The overlay may be pruned or refreshed independently of the primary
  pack.

## Known divergence from the primary pack (recorded 2026-09-24)

- `github-actions.md` lines 77, 936 and 937 use pre-v1.2 SLSA level names ("SLSA Level 4:
  Pinned Dependencies", "SLSA Level 2: Signed Provenance", "SLSA Level 3: Non-falsifiable
  Provenance"). SLSA v1.2 organizes requirements into Build and Source tracks, and the primary
  pack uses that wording, which wins on conflict.
- The upstream file (TikiTribe/claude-secure-coding-rules, `rules/cicd/github-actions/CLAUDE.md`,
  checked on 2026-09-24) carries the same lines, so a refresh from source changes nothing. The
  file is not a near-duplicate of the primary pack, so it is kept. Re-check upstream at the next
  overlay review; dropping the file remains an overlay-review choice.
