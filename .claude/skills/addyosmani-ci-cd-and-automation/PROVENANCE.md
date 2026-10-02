# Overlay provenance and precedence

This directory is a **supplementary** third-party skills overlay, not part of the
primary GRC governance pack. The primary pack under
[`guardrails/`](../../../guardrails/) is the
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

- `../addyosmani-security-and-hardening/SKILL.md` line 306 and lines 358-363 (under the edition label on line 356)
  use OWASP Top 10 for LLM Applications (2025) identifiers. In the held 2026 edition the same
  risks carry these identifiers: LLM01 (Prompt Injection) and LLM02 (Sensitive Information
  Disclosure) are unchanged; 2025 LLM03 (Supply Chain, line 306) is LLM04:2026, since in 2026
  LLM03 is Excessive Agency, the sense the primary pack uses; LLM05 is LLM10:2026 (Improper
  Output Handling); LLM06 is LLM03:2026 (Excessive Agency); LLM07 is LLM08:2026 (Hidden Context
  Exposure, renamed and broadened from System Prompt Leakage); LLM08 is LLM09:2026 (Vector and
  Embedding Weaknesses); and LLM10 is LLM06:2026 (Unbounded Consumption).
- Lines 42 and 306 also cite OWASP Top 10 (web) 2021 identifiers without an edition. The
  primary pack uses the 2025 web edition, in which A04 (Insecure Design, line 42) is
  A06:2025, and A06 (Vulnerable Components, line 306) is expanded into A03:2025 (Software
  Supply Chain Failures). For both lists, use the current identifiers when mapping this
  guidance to the held frameworks; the primary pack wins on conflict.
- The upstream file (addyosmani/agent-skills, `skills/security-and-hardening/SKILL.md` on
  `main`, checked on 2026-09-27) has been reorganized but still carries the same identifiers,
  so a refresh from source changes nothing. The file is not a near-duplicate of the primary
  pack, so it is kept with this divergence recorded. Re-check upstream at the next overlay
  review; dropping the file remains an overlay-review choice.
- This installation carries five of the upstream skills, so some of their pointers do not resolve here.
  `../addyosmani-security-and-hardening/SKILL.md` lines 79 and 424 and `../addyosmani-code-review-and-quality/SKILL.md` lines 317-318 point to
  `references/security-checklist.md` and `references/performance-checklist.md`, relative paths carried
  over from the upstream skills; the directory does not carry those files. `../addyosmani-code-review-and-quality/SKILL.md`
  line 76 says to see `performance-optimization`, `../addyosmani-ci-cd-and-automation/SKILL.md` line 191 names the
  `debugging-and-error-recovery` skill, and `../addyosmani-using-agent-skills/SKILL.md` routes to 19 skills in its
  quick-reference table (and elsewhere in that file) that are not here. For security
  review, use the primary pack's rules instead (they win on conflict); the primary pack has no
  performance-review equivalent. Vendoring the missing files under the upstream licence remains an
  overlay-review choice.

- Local divergence from upstream (2026-10-02):
  `../addyosmani-security-and-hardening/SKILL.md` line 88 stores `\$1` in place of
  upstream `$1`. Claude Code 2.1.287 removes this escape at invocation, preserving
  the SQL positional parameter. The other four bodies need no interpolation changes.

## Local installation (2026-10-02)

These five skills moved from rules to .claude/skills/addyosmani-<name>/.
Their frontmatter names have the addyosmani- prefix; their descriptions and
bodies retain the recorded upstream content except for the escape above. Invoke installed skills using
that prefix when upstream text refers to an unprefixed name. The line numbers
above still refer to the preserved skill files. Each skill carries a copy of
this record and the upstream LICENSE. Only skill discovery metadata loads
at startup; skill bodies load when invoked. The recorded original-byte
SHA-256 values describe the fetched upstream files, not these local copies.
