# AIQT cross-family CI kit (Levels 2 and 3)

Version: 1.0.0 (plain semver; the AIQT release train assigns release versioning once
it exists)
Status: Phase-1 kit; consumes the AIQT review contract (`../review-contract.md`) and
its schemas (`../schemas/`).

The GitHub-automatic second opinion: on every non-draft, same-repository pull request
authored with one AI family, the OTHER family's official vendor Action runs a
full-harness advisory review and posts one consolidated comment. Cross-family only:
the authoring family is never its own reviewer. The review is ADVISORY: it never
blocks, never requests changes, and the decision always returns to the developer.

## What ships

- `workflows/aiqt-review-claude-on-codex.yml`: Claude reviews Codex-authored changes.
- `workflows/aiqt-review-codex-on-claude.yml`: Codex reviews Claude-authored changes.
- `prompts/aiqt-review.md`: the one canonical brief both lanes render.

Install: copy the two workflow files into `.github/workflows/`, copy the prompt file
to `.github/codex/prompts/aiqt-review.md`, add the secrets below, and adjust the
family-detection filters if your branch or bot conventions differ (adopters whose
tooling labels PRs can swap the filter for a label check in one line).

## Reviewer runtime

Both lanes run the vendor's FULL coding-agent harness (repository read, search,
verify at source), never a bare diff-in-prompt call, with diff-focused briefs and
on-demand repository access, per the review contract's runtime section. Reviewer
models are PINNED in each workflow's `env:` block; bump them deliberately and record
the bump (the AIQT release record formalizes this once the release train exists;
until then, record the bump where your project records versioned decisions).

## The secrets this kit names

These are the names the wizard's key-loading step and the doctor's secrets check
(exists-unread, never fetched or printed) look for:

- `CLAUDE_CODE_OAUTH_TOKEN` (Claude lane, subscription path) or `ANTHROPIC_API_KEY`
  (Claude lane, metered path)
- `OPENAI_API_KEY` (Codex lane, metered)

## Level 2 (personal repository)

Auth, per vendor:

- **Claude lane.** Two supported paths. (1) Subscription OAuth token: run
  `claude setup-token` locally and store the result as the `CLAUDE_CODE_OAUTH_TOKEN`
  repository secret; runs then use your Claude subscription instead of metered API
  billing. The token is tied to the person who minted it, which is exactly right at
  Level 2. (2) Metered API key: store `ANTHROPIC_API_KEY`. The workflow supplies the
  OAuth secret when present and the API key otherwise; verify the action's precedence
  in its current documentation if you set both.
- **Codex lane.** The official action authenticates with `OPENAI_API_KEY` (metered).
  A ChatGPT-plan path exists for trusted private runners (the vendor's CI auth
  guide); this kit documents it and defaults to the API key.

Spend awareness: metered lanes append a spend note to every comment, and both lanes
cancel superseded runs (`concurrency`) and honour a `[skip aiqt]` marker in the PR
title.

## Level 3 (organization rollout)

The workflow YAML is unchanged. What changes is the secret plane:

1. Create the secrets ONCE at organization level, sourced from workspace- or
   project-scoped team keys so spend is attributable to the team. Do NOT roll a
   personal OAuth token up to Level 3: it is bound to one person's subscription; the
   org path is an API key (or federation, below).
2. Set each org secret's visibility to "Selected repositories" and enumerate the
   rollout repositories; never "All repositories" on a mixed organization.
3. Delete the Level-2 repository secrets when a repository joins the org rollout (a
   repository secret silently shadows the org secret of the same name).
4. Team cost visibility: both vendors' dashboards report the scoped keys' spend at
   team granularity; review monthly.
5. Optional hardening: workload identity federation removes the static key entirely
   where the vendor supports it (organization-side configuration required); it is an
   API-billing path.

## Evidence (full artefacts, log-aligned)

The PR comment is a VIEW, never the record. Each lane uploads the rendered brief,
the reviewer's raw output, and the SARIF-lite findings block as workflow artifacts
(GitHub's run-attached archives), with retention aligned to the adopting project's
AIQT log policy. TODAY (until the AIQT logs-and-metrics document ships) the kit
default is 90 days; choose your window deliberately and record the choice. The
finding and verdict shapes are the AIQT review contract's schemas (`../schemas/`).

## Scope guards, stated

- Fork PRs never run (secrets safety; the `if:` filter checks the head repository).
  Do not widen with `pull_request_target`.
- A PR matching neither family filter gets no automatic second opinion; that is the
  launch scope, not a defect.
- The PR diff is untrusted input: briefs frame it as data under review, the Codex
  lane runs `sandbox: read-only`, and the Claude lane grants no custom GitHub App
  token.
