# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Last-heartbeat-UTC:** 2026-07-15T17:13:10Z

**Current-task:** RELEASED. The 2026-07-15 resumed session (`/resume` from #942), attended-autonomous on the VM, gh-CLI (no GitHub MCP), worked the maintainer's **website-adjustment batch** (website priority) and is closing with this handoff PR (#954). Merged this session: Sweep 105 close-out #943; pack card-links #944; landing §05 lede #945; For-AI page + robots/sitemap/llms #946; AUTHORS attribution link #947; §2.16 residual #948; §3.76 parity guard #949; "License" spelling #950; **item 2 sidebars + DRY sidebar CSS + scrollspy trio-highlight #951; item 3 landing eyebrows + green-check->boxed CTA #952; item 4 per-type listing pages + linked "By document type" chips #953.** This closing PR (#954) batches #953's QA (`/validate-pr` W-1 + `/retro`), FIXES W-1 (this prose refresh), releases the lease, and refreshes the handoff. **Maintainer-applied out-of-band:** the Cloudflare Pages build-watch-paths config (`\.web/*, taxonomy.yml, README.md, */README.md`) was updated by the maintainer 2026-07-15; item closed. **NEXT SESSION:** batch item (5) **§2.15 standards-source links** via the maintainer-chosen approach (POPULATE `grc_library_ref/catalogue.yml` with verified `upstream_url` for the ~50 landing standards FIRST, as a `grc_library_ref` PR, then link the site from it), a ~50-URL cross-repo external-verification workstream, no guessed URLs; then item (6) §3.75 web->corpus link-integrity gate; THEN the maintainer-gated §2.4 publish go. Tooling follow-up §3.77 (CHANGELOG link-gate `.html`/`.css`/`.js` extensions).

**Worker-dispatches:** across this session each substantive PR got a refute-briefed skeptical verifier (all clean, no defect) plus a post-merge `/validate-pr` Subagent A (read-only-git): #951 verifier + sweep (W-1 P3-counter, fixed #952); #952 verifier + sweep (0 findings, 2 non-defect notes incl. the doubled-PR-suffix, fixed by dropping `(#N)` from PR titles from #953); #953 verifier (no defect, 9 targets) + sweep (W-1 session-state prose staleness, fixed this PR). The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

This file is the session-concurrency lease: the declared half of the two-part interlock
that protects the shared `main` state surfaces (the session handoff, [`../TODO.md`](../TODO.md),
[`DONE.md`](DONE.md), the QA history registers, the detailed CHANGELOG mirror, and the four
version surfaces) from a second orchestrator session resuming while a prior one is still
live. The full design, including the honest limitation that this is an advisory interlock
and not a hard mutex, is recorded in [`design-decisions.md`](design-decisions.md) under
"Session-concurrency safety".

Lifecycle (audit gate 63 enforces the SHAPE; the `/resume` step-0 procedure enforces the
interlock, because CI runs per-branch and cannot see across concurrent sessions):

- **Acquire**: at session start, right after the `/resume` step-0 check passes, the
  session writes `Active-session: <its branch>`, `Status: active`, and a fresh
  `date -u +%Y-%m-%dT%H:%M:%SZ` heartbeat.
- **Refresh**: the heartbeat is re-stamped at each PR close-out (it batches into the
  recursion-avoidance refresh alongside the session handoff).
- **Release**: the session-closing handoff PR sets `Status: released` and
  `Active-session: none`, so a cleanly-closed session leaves a released lease on `main`.

The declared state above is only the LAST-MERGED session's view. The other half of the
interlock is external: `/resume` step 0 also runs a `git fetch` cross-check of unmerged
`origin/claude/*` branches for commits inside the 60-minute staleness window (the crash
net for a session that died without releasing). Status `active` or `winding-down` with a
heartbeat inside the window means a session is likely live: HOLD and surface to the
maintainer; do not proceed on a timeout. A not-`released` lease with a heartbeat OLDER
than the window is surfaced as an abandoned-session takeover decision instead.
