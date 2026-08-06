Render the backlog "pipeline" view the maintainer wants (maintainer-directed 2026-08-06). A project-only command (it reads THIS project's `TODO.md` + `grc_library_private/P-TODO.md` + `grc_library_private/.working/DONE.md`), not a portable pack skill. It changes no state.

**`_private` (read first).** Reads the private backlog + DONE ledger via the `_private` delegation directive. On the maintainer orchestrator, if `_private` is absent, FAIL LOUD and clone it; do not reconstruct from memory. On an adopter clone, `_private` is absent by design: the view degrades to the public `TODO.md` only.

## What it does

Show a scannable, one-line-per-item roadmap: the 5 most-recently-completed items at the top (`[x]`), then the current umbrella's upcoming items up to 20 (filling from the next planned items when the umbrella is short). NOT a table.

## Arguments

- `/pipeline` (no arg): the CURRENT umbrella (the one being actively worked) up to 20, then fill.
- `/pipeline <topic>` (e.g. `/pipeline website`, `/pipeline P-1.25`): scope to that umbrella/goal.

## Process

1. **Generate the skeleton** with the tool: `python3 tools/audit-backlog-actionability.py --pipeline --umbrella "<current-or-arg>"`. It enumerates from the authoritative item SET (never fabricating an id), expands `- **P-x.y**` bullet sub-items under an umbrella heading, groups by umbrella, and renders a TRUNCATED, blocked-excluded VIEW (not the completeness enumeration the default `audit-backlog-actionability.py` mode produces), best-effort as `<id> <checkbox> [PR####] <type-guess> - <10-word title>`. The 5 recent-done come from `DONE.md`.
2. **Determine the CURRENT umbrella** (for the no-arg default): the umbrella of the active work, from `grc_library_private/.working/next-prs.txt`'s first item (the tool's file-order default is a fallback, not the "current" judgement). Pass it as `--umbrella`.
3. **Refine the tool's rough output** (the tool is a deterministic backbone; polish the semantic parts):
   - **Done-marking:** the tool marks a bullet `[ ]` even if it is actually closed (a closed sub-item may still sit in an umbrella's plan list). Cross-check each id against `DONE.md`; a closed item is `[x] PR####`. (Flag stale done-bullets for rotation.)
   - **Type:** fix a wrong `<type-guess>` to the right one word (`content`/`website`/`tool`/`gate`/`rule`/`validation`/`ops`).
   - **Description:** rewrite to a clean **≤10-word** phrase (the tool truncates; make it read well).
   - **Fill:** when the current umbrella has <20 open items, fill from the next planned batch in `next-prs.txt`. If those items are not yet formal backlog ids (e.g. AIQT C1-C5 live only in `strategy/`), show them by their working id and note they need promotion to `P-TODO` to enumerate natively.
4. **Render** exactly: `<id> <checkbox> <PR####-if-done> <type> - <description ≤10 words>`; 5 recent done first, blank line, then upcoming grouped by umbrella (blank line between umbrellas). No table.

## Notes

The format is also codified in the assistant memory `pipeline-view-format`, so the view survives where this command is unavailable; keep that memory in parity with the step-4 format on any format change (no gate guards a memory surface). The tool's `--self-test` covers the enumeration/formatting logic.
