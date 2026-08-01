# Provenance: the Clean Language skill (vendored)

This directory is the Clean Language skill, VENDORED into grc_library from its upstream source.

- **Source:** github.com/jposluns/ai-language, `clean-language/` (site: cleanlanguage.ai).
- **Copyright / licence:** Copyright (c) 2026 Jeff Posluns; see `LICENSE` and `NOTICE.md` beside this
  file. This skill is NOT relicensed to grc_library's CC BY-SA 4.0; it retains its own licence, the same
  vendoring stance as the third-party overlay under `.claude/rules/external/`.
- **Installed:** 2026-08-01, from the CURRENT upstream. The ephemeral checkout it was first drawn from
  was already STALE (five of six files had advanced), so every file here was re-fetched from upstream and
  verified in-sync by git blob SHA.
- **Purpose:** apply the Clean Language standard to PUBLIC-FACING prose (README, CHANGELOG summaries, the
  grclibrary.ai website copy, the adopter guide), then validate no facts were lost. NOT for corpus
  document creation (the governance documents keep their fixed section model and `lint-language.py` house
  style). Maintainer-directed 2026-08-01.
- **Staying current (P-1.13):** the upstream advances without a heads-up. Run
  [`tools/check-clean-language-upstream.py`](../../../tools/check-clean-language-upstream.py) to compare
  every file here against upstream (via `gh api` blob SHAs); it reports any DRIFT. A MONTHLY time-bounded
  follow-up in `TODO.md` re-surfaces this at `/resume`, so a drift is noticed without the maintainer having
  to remember. On drift, re-fetch the changed files from upstream (`gh api repos/jposluns/ai-language/
  contents/clean-language/<file> --jq .content | base64 -d > <installed>`) and commit.
