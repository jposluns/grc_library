Invoke the `pr-retrospective` skill defined in this project's pack at [`dev-security/claude-rules/skills/pr-retrospective/SKILL.md`](../../dev-security/claude-rules/skills/pr-retrospective/SKILL.md). Slash-command entry point is `/retro`; the underlying skill name remains `pr-retrospective` (the descriptive name documents the workflow's purpose, the slash command is the ergonomic verb). Execute the post-merge retrospective per the six-step process the skill encodes:

**`_private` (read first).** This command reads and appends the hallucination-metrics record in `grc_library_private` (via its INDEX; the CLAUDE.md `_private` delegation directive is the general rule). On the maintainer orchestrator, if `_private` is absent, FAIL LOUD, clone it or grant access, and do NOT reconstruct its content from memory. On an adopter clone `_private` is absent by design: redirect to the in-repo `.private` placeholder or create your own.

1. **Identify the PR and its inputs**: capture PR number, merge commit SHA, FR(s) closed (if any), the `/validate-pr` findings just returned (0 findings, N findings with categories, or out-of-window observations), any apply-time worker corrections logged in `grc_library_private/hallucination-metrics.md` during the PR, and recently-shipped PRs in the same cluster (for pattern surfacing).

2. **Identify what went well**: one short observation (1-2 sentences). If nothing notable, record "Routine; no notable highlight."

3. **Identify friction**: one short observation (1-2 sentences). If no friction, record "No friction observed."

4. **Surface patterns (if any)**: a single occurrence is observation, second is signal, third is pattern. Record the pattern only when the friction in this PR matches friction seen in a recent PR (≤5 PRs prior). When a pattern's recurrence count reaches three or more distinct PRs, it AUTO-GRADUATES to a gate-or-convention proposal in step 5 (name the false-positive-free gate that would extinguish it, or a convention line where no gate fits), because checklist prose reduces but does not stop a thrice-recurring class.

5. **Propose improvement (if any)**: name a concrete candidate (new audit gate, pack-rule update, worker-brief template addition). Candidates go in the register; the next planning cycle picks them up if priority warrants. Leave blank if no pattern surfaced.

6. **Disposition scan (closure discipline)**: if the just-merged PR codified or routed any earlier register row's candidate, append the disposition token to that row's Proposed-improvement cell per the register's disposition convention (`CODIFIED in <carrier>`, `ROUTED to <destination>`, `REJECTED (<reason>)`, `EXPIRED (<date>)`, or `WATCH (fires on <n>th occurrence)`; a non-empty cell with no token is pending). When the PR performed an authorized protected-file touch, grep the pending cells for carrier phrases ("next authorized touch", "row is the carrier", "next CLAUDE.md-touching") and confirm the touch carried them or record why not. Rejection and expiry of aged candidates are maintainer calls: propose, never silently drop.

**Surface Pattern and Proposed-improvement entries in chat** (per the chat-surfacing discipline shared with `/validate` and `/validate-pr`). The maintainer should see proposed improvements at the moment they're identified, not on next deep-dive into the working-state archive. Clean-PR retrospectives (no friction, no pattern) get a one-sentence chat acknowledgement.

**Batching into the next PR**. The register-row append is a content change; per the batching rule, the register-row commit is **batched into the next PR**, whatever its substantive purpose. The retrospective is conducted immediately after `/validate-pr`; only the register-row commit is deferred. A retrospective that surfaces a candidate improvement deserving its own PR DOES trigger that PR — but the substance of that PR is the improvement itself; the register row bundles in alongside.

**No orchestrator-side skip discretion.** Same discipline as `/validate-pr`: every merged PR gets a `/retro` entry, even when the retrospective conclusion is "nothing new to learn." Zero-content entries serve as proof-of-discipline. Skipping is a policy deviation requiring maintainer authorization.

Append the entry to [`.working/improvement-log.md`](../../.working/improvement-log.md) with columns `Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement`. New rows on top (reverse-chronological).

Report back: the entry as written; if a Pattern or Proposed-improvement surfaced, the chat-surface text; the path to the register file.
