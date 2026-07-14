# Cloudflare Pages setup runbook, grclibrary.ai public site (TODO section 2.4)

**Version:** 1.0.3\
**Date:** 2026-07-14\
**License:** CC BY-SA 4.0

Maintainer-facing runbook for standing up (and re-deploying) the public landing site
at `grclibrary.ai` on Cloudflare Pages. It records the SETTLED, repo-side design (the
`.web/` generator shipped in the website-build PR) and the account-side steps the
maintainer performs in the Cloudflare dashboard. This file is maintainer working state,
exempt from corpus audit gates.

**Division of labour.** The assistant builds and maintains everything repo-side (the
`.web/` generator, the page template, the generator-health CI check). The account-side
actions below (creating the Pages project, DNS, the custom domain, the publish
go-decision) are the maintainer's: they require the maintainer's Cloudflare account, and
no Cloudflare API token is placed in the assistant's execution environment. The assistant
guides the maintainer step-by-step through the dashboard.

**Verify-against-live-docs discipline.** Cloudflare's dashboard labels, build-image
language versions, the build-watch-path feature and its bypass thresholds, and deploy-hook
rate limits are vendor-set and change over time. Every such value below is marked
**[confirm live]** and must be confirmed against the current Cloudflare dashboard or
`developers.cloudflare.com` at setup time, not asserted from memory.

---

## What is being deployed

- A two-page static site at `grclibrary.ai` (a landing page and an about/contributors page), rendered by [`.web/build.py`](../.web/build.py)
  from the LIVE corpus at build time (document counts, per-domain breakdown, document-type
  chips, and the library CalVer are recomputed from [`taxonomy.yml`](../taxonomy.yml) and
  [`README.md`](../README.md); nothing is hardcoded).
- The rendered output is a build artefact under `.web/dist/` (git-ignored, never committed).
  Only the generator, the page templates, and the shared partials (under
  [`.web/templates/`](../.web/templates/)) are tracked. Cloudflare rebuilds the page from the live corpus on each deploy; the edge
  cache is the "cached copy, refreshed on change" behaviour.
- **Content boundary:** the generator's only inputs are `taxonomy.yml`, `README.md`, and
  the page templates, and its only outputs are the landing page and the about page. It never reads `.working/`,
  `.claude/`, `tools/`, `tests/`, `.github/`, or the private sibling repositories, so no
  internal or working-state content can reach the public site through it.

## Prerequisites

- The `grclibrary.ai` zone is on the maintainer's Cloudflare account (PRO plan), so the
  zone-level WAF, managed rules, and rate limiting apply and DNS is managed in-Cloudflare.
- The GitHub repository `jposluns/grc_library` is accessible to Cloudflare Pages (the
  Cloudflare GitHub app is installed / authorized for the repo).

## Step-by-step (Cloudflare dashboard)

1. **Create the Pages project.** Workers and Pages -> Create -> Pages -> Connect to Git ->
   select `jposluns/grc_library`. **[confirm live]** the exact menu path and labels.
2. **Production branch.** Set the production branch. **Maintainer decision** (default and
   recommendation: `main`, so every merge to `main` auto-rebuilds the site; choose a
   dedicated release branch instead only if you want to gate publish timing separately from
   `main`).
3. **Build settings.**
   - Framework preset: **None**.
   - Build command: `python3 .web/build.py`
   - Build output directory: `.web/dist`
   - Root directory: repository root (leave as `/`).
   - **[confirm live]** that the Cloudflare Pages build image provides `python3` and which
     version; the generator is stdlib-only (no `requirements.txt`, no third-party
     dependencies), so no dependency-install step is needed, but the build image must have
     a Python 3 interpreter on PATH. If a language/version pin is required, set it per the
     current Cloudflare Pages docs (for example a `.tool-versions` / `.python-version` file
     or a build-environment variable).
4. **Build watch paths (avoid wasted builds).** Configure include/exclude path globs so only
   content-affecting changes trigger a build. **[confirm live]** the feature name, location,
   and any large-commit / large-file bypass thresholds (vendor-set).
   - Include: the published content directories. Each `<domain>/README.md` now feeds that
     domain's on-site page (its `## Purpose` intro), so the eleven domain directories are
     load-bearing for a rebuild, not only for the register counts. Plus `.web/` (the
     generator and templates) and `taxonomy.yml` / `README.md`.
   - Exclude: `tools/`, `tests/`, `.working/`, `.claude/`, `.github/`.
5. **First deploy.** Trigger the initial deployment; confirm the build log shows the
   generator's summary line (`web-generator OK: ... N documents ...`) and the deploy
   publishes `.web/dist/`.
6. **Custom domain.** Pages project -> Custom domains -> add `grclibrary.ai` (and `www` if
   wanted, with a redirect to the apex or vice-versa). Because the zone is already on
   Cloudflare, the DNS record is created and proxied automatically (no external CNAME, which
   avoids the certificate / DNS-check breakage seen when GitHub Pages sits behind the
   Cloudflare proxy). **[confirm live]** the exact custom-domain flow.
7. **Publish go-decision (maintainer).** The site is a preview until the maintainer decides
   to publish. Until then keep the custom domain unattached or the project access-restricted
   per preference.

## Optional: scheduled rebuild

If time-sensitive currency is wanted beyond push-triggered rebuilds, a deploy hook can be
called from a scheduled Cloudflare Worker (cron). **[confirm live]** deploy-hook creation
and its rate limits before relying on a schedule.

## Content-security note

The page makes no external requests (all CSS and JS inline, system fonts only, no external
images or fonts), so it renders identically behind a strict Content-Security-Policy and does
not wait on any CDN. A strict CSP at the zone level is compatible with the page as shipped.

## Re-deploy / maintenance

- The site auto-rebuilds from the live corpus on each push to the production branch (subject
  to the watch paths). No manual regeneration is needed; the generator recomputes every figure.
- If the generator-health CI check (`.github/workflows/web-generator-health.yml`) fails on a
  PR, the corpus changed in a way the generator can no longer parse (a renamed metadata field,
  a moved file, a taxonomy schema change); fix the generator's parsing before the change
  reaches the production branch, so a red production deploy is avoided.

## Open maintainer items (to confirm before publish)

- The production branch name (step 2).
- The Cloudflare Pages project settings, confirmed against the current dashboard (steps 3-4,
  the **[confirm live]** items).
- The About-page bio prose and the CGEIT / CISSP credentials in
  [`.web/templates/about.html`](../.web/templates/about.html) (carried verbatim
  from the maintainer's staged design; they and the LinkedIn / GitHub links are the only personal
  detail on the site, and go public only on the maintainer's deploy go).
