# Provenance: the Clean Language skill (vendored)

This directory holds the Clean Language skill, vendored into grc_library from its upstream release.

- **Source (the pin):** github.com/jposluns/cleanlanguage (formerly `jposluns/ai-language`), release
  tag `v1.0.15`, commit `320b68567b3b5e307a59615d923d1bfe31282d17`, released 2026-11-08 (site:
  cleanlanguage.ai). Vendored on 2026-11-08, replacing version 1.0.8. Upstream now ships the skill
  inside a plugin: `SKILL.md` and `references/` come from `cleanlanguage/skills/cleanlanguage/`,
  `agents/openai.yaml` and the two icons under `assets/` are the plugin-level files, and `LICENSE`
  and `NOTICE.md` are the upstream repository-root files. Every file here except this one is
  byte-identical to its v1.0.15 upstream file.
- **Directory name and skill name:** the v1.0.15 `SKILL.md` frontmatter declares
  `name: cleanlanguage`, and this directory has the same name. It was renamed from
  `clean-language` on 2026-11-09 to match the upstream skill name. No upstream file names the
  directory it is installed in, so the rename changed no vendored file.
- **Copyright and licence:** Copyright (c) 2026 Jeff Posluns; see `LICENSE` and `NOTICE.md` beside
  this file. The skill is licensed CC BY-SA 4.0, the licence grc_library uses, under Jeff Posluns's
  own copyright and attribution. Vendoring keeps that copyright and attribution separate from the
  grc_library corpus copyright. The v1.0.15 attribution asks for "Changes were made." only when the
  material is modified; this copy is unmodified.
- **`NOTICE.md` is upstream bytes:** it is kept byte-identical so the drift check below can verify
  it. Its site-template and adopted-governance notes describe paths in the upstream repository
  (`assets/baseline/`, `.aiqt/`, `.claude/rules/aiqt/`, `.claude/rules/security/`,
  `plugin/aiqt-guardrails-hooks/` and `.aiqt/pin.toml`), not this one. They are left unedited,
  because an edit would make `NOTICE.md` differ from upstream and defeat the drift check. This file
  is the provenance record for the vendored copy.
- **Purpose:** apply the Clean Language standard to public-facing prose (README, CHANGELOG
  summaries, the grclibrary.ai website copy, the adopter guide), then check that no facts were lost.
  It is not for corpus document creation: the governance documents keep their fixed section model
  and `lint-language.py` house style. Maintainer-directed 2026-08-01.
- **Staying current (the update path):** upstream releases arrive without notice. Run
  [`.claude/skills/corpus-management/tools/check-clean-language-upstream.py`](../corpus-management/tools/check-clean-language-upstream.py)
  periodically. It compares the git blob SHA of every vendored file here with the upstream file
  (through `gh api`): the skill content, the agent file, the two icon assets, and the `LICENSE` and
  `NOTICE.md` legal files, so an upstream attribution or licence change is reported. Its `FILES` map
  holds each file's upstream path. On drift, fetch the changed files from upstream, update this
  record, and commit.
