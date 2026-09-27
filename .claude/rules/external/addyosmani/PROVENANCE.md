# Overlay provenance and precedence

This directory is a **supplementary** third-party rules overlay, not part of the
primary GRC governance pack. The primary pack under
[`guardrails/`](../../../../guardrails/) is the
authoritative source.

- **Precedence:** on any conflict between this overlay and the primary GRC pack, the
  **primary pack wins**. The overlay adds engineering-practice guidance that overlaps
  or supplements the primary layer; it never overrides it.
- **Source and licence:** `addyosmani` (see this directory's `LICENSE` for the upstream
  licence and attribution). Content is used under that licence.
- **Pruning / refresh stance:** the overlay is reviewed at each periodic pack review.
  A near-duplicate wrapper that the primary pack already covers is a prune candidate;
  a stale upstream file is refreshed from the source or dropped rather than allowed to
  diverge silently. The overlay may be pruned or refreshed independently of the primary
  pack.

## Known divergence from the primary pack (recorded 2026-09-27)

- `security-and-hardening.md` lines 356-363 use OWASP Top 10 for LLM Applications (2025)
  identifiers. The held 2026 edition keeps LLM01 (Prompt Injection) and LLM02 (Sensitive
  Information Disclosure), but maps 2025 LLM05 to LLM10:2026 (Improper Output Handling), LLM06
  to LLM03:2026 (Excessive Agency), LLM07 to LLM08:2026 (Hidden Context Exposure, renamed and
  broadened from System Prompt Leakage), LLM08 to LLM09:2026 (Vector and Embedding Weaknesses),
  and LLM10 to LLM06:2026 (Unbounded Consumption). Use the 2026 identifiers when mapping this
  guidance to the held framework; the primary pack wins on conflict.
- The upstream file (addyosmani/agent-skills, `skills/security-and-hardening/SKILL.md` on
  `main`, checked on 2026-09-26) has been reorganized but still carries the same 2025 mapping,
  so a refresh from source changes nothing. The file is kept with this divergence recorded.
  Re-check upstream at the next overlay review; dropping the file remains an overlay-review choice.
