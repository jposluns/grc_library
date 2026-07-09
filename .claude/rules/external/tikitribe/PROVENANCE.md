# Overlay provenance and precedence

This directory is a **supplementary** third-party rules overlay, not part of the
primary GRC governance pack. The primary pack under
[`dev-security/claude-rules/`](../../../../dev-security/claude-rules/) is the
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
