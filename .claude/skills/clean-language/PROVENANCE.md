# Provenance: the Clean Language skill (vendored)

This directory is the Clean Language skill, VENDORED into grc_library from its upstream source.

- **Source:** github.com/jposluns/cleanlanguage, `clean-language/` (site: cleanlanguage.ai).
- **Copyright / licence:** Copyright (c) 2026 Jeff Posluns; see `LICENSE` and `NOTICE.md` beside this
  file. The skill is licensed CC BY-SA 4.0 (the SAME licence grc_library uses), but under Jeff Posluns's
  OWN copyright and attribution, which are PRESERVED here rather than folded into the grc_library corpus
  copyright. That distinct-copyright-and-attribution preservation, not a different licence, is the point
  of vendoring it, the same stance as the third-party overlay under `.claude/rules/external/`.
- **`NOTICE.md` is kept BYTE-IDENTICAL to upstream** (so the monthly drift check below can verify it):
  its inherited line `See .claude/rules/governance/PROVENANCE.md for details` refers to UPSTREAM's repo
  layout and does NOT resolve in this repo; the provenance record for the vendored copy is THIS file
  (`.claude/skills/clean-language/PROVENANCE.md`). The pointer is left as-is rather than edited, because
  editing it would diverge `NOTICE.md` from upstream and defeat the drift check (codex vpr1328 finding 4).
- **The vendored `SKILL.md` `Github:` pointer is left at the UPSTREAM repo name** (the
  pre-rename name it carries at line 11) for the SAME reason as `NOTICE.md`: `SKILL.md` is in
  the drift check's `FILES` map (compared by git blob SHA), so editing it here would diverge it
  from upstream and produce a permanent false DRIFT (claude vpr-1468 finding 1). The 2026-08-09
  upstream-repo rename to `jposluns/cleanlanguage` was applied ONLY to THIS repo's own records
  (this `PROVENANCE.md` and `tools/check-clean-language-upstream.py`, neither in `FILES`); the
  vendored `SKILL.md` continues to track upstream, whose own `SKILL.md` still carries the old
  name until upstream updates it. The GitHub rename redirects the API path, so the checker's
  `cleanlanguage` path resolves.
- **Installed:** 2026-08-01, from the CURRENT upstream. The ephemeral checkout it was first drawn from
  was already STALE (five of the six skill-content files had advanced), so every file here was re-fetched from upstream and
  verified in-sync by git blob SHA.
- **Purpose:** apply the Clean Language standard to PUBLIC-FACING prose (README, CHANGELOG summaries, the
  grclibrary.ai website copy, the adopter guide), then validate no facts were lost. NOT for corpus
  document creation (the governance documents keep their fixed section model and `lint-language.py` house
  style). Maintainer-directed 2026-08-01.
- **Staying current (P-1.13):** the upstream advances without a heads-up. Run
  [`tools/check-clean-language-upstream.py`](../../../tools/check-clean-language-upstream.py) to compare
  EVERY vendored file here against upstream (via `gh api` blob SHAs): the skill content, the two icon
  assets under `assets/`, AND the `LICENSE` / `NOTICE.md` legal files, so an upstream attribution or
  licence change is not silent. It reports any DRIFT. A MONTHLY time-bounded follow-up in `TODO.md`
  re-surfaces this at `/resume`, so a drift is noticed without the maintainer having to remember. The
  upstream paths differ by file (skill content under `clean-language/`, but `LICENSE` / `NOTICE.md` are
  upstream REPO-ROOT files); the tool holds each file's correct upstream path. On drift, re-fetch the
  changed files from upstream (`gh api repos/jposluns/cleanlanguage/contents/<upstream-path> --jq .content
  | base64 -d > <installed>`) and commit.
