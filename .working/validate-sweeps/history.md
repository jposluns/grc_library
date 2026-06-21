# Validation Sweep History

**Version:** 2.0.3\
**Date:** 2026-06-21\
**License:** CC BY-SA 4.0

Reverse-chronological table of every `/validate` invocation against this library. New rows on top. Each row is a summary; detail for findings-producing iterations lives in the per-iteration file linked from the **Detail** column.

See [`README.md`](README.md) for the failure-mode taxonomy (C1-C8), maintenance protocol, dispatch-declaration discipline, false-positive accept-list rules, dating discipline for deferred findings, and audit-gate exemption notes.

## Sweep entries

| Date | Sweep | Subagents | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|
| 2026-06-21 | 11 iter 1 | A, B, C | 8 (1H, 2M, 5L) | [#127](https://github.com/jposluns/grc_library/pull/127) | [`2026-06-21-sweep11-iter1.md`](2026-06-21-sweep11-iter1.md) | Post PRs #124-#126. Findings: fitness-report count mismatch across 6 surfaces (95/18/22/31/24 claimed vs 111/17/20/57/17 actual); audit-programme spec D1 description stale post-PR-#125 (didn't mention dual-entry); fourth-consecutive-sweep TODO drift on resume-state (B-1 through B-4). All in-window; all fixed. Pattern observation: TODO drift is now recurring; iter close-out reframes snapshot as "as-of-last-refresh" and queues Gate 45 (TODO staleness audit) as PR #128 to catch the harder shapes mechanically. |
| 2026-06-21 | 10 iter 3 | A, B, C | 1 (1M) | [#123](https://github.com/jposluns/grc_library/pull/123) | [`2026-06-21-sweep10-iter3.md`](2026-06-21-sweep10-iter3.md) | Post PRs #121-#122. Single recurring TODO resume-snapshot drift: `TODO.md:16` "Library version at HEAD" was one PR behind (PR #121 bumped library to .106 but the TODO refresh in the same PR captured pre-bump values). Subagent A/C zero findings; Subagent B caught it. Convergence delta: iter 2 had 7 findings, iter 3 has 1 — strong narrowing but not yet empty. |
| 2026-06-21 | 10 iter 2 | A, B, C | 7 (1H, 3M, 3L) | [#121](https://github.com/jposluns/grc_library/pull/121) | [`2026-06-21-sweep10-iter2.md`](2026-06-21-sweep10-iter2.md) | Post PRs #118-#120 (canonical activity restructure + TODO + fitness skill overnight). Findings: re-add preflight exemption for "Six rules" line (line_hash changed post PR #117); TODO resume-state snapshot stale (version + persona count drift since session-pause); CHANGELOG "version 1.0.0" claim for SKILL.md without frontmatter version; overnight-pr.md "in progress" status stale. All in-window; all fixed. |
| 2026-06-21 | 10 iter 1 | A, B, C | 6 (2H, 2M, 2L) | [#117](https://github.com/jposluns/grc_library/pull/117) | [`2026-06-21-sweep10-iter1.md`](2026-06-21-sweep10-iter1.md) | Post PRs #114-#116. Six in-window prose-drift findings: stale step counts in SKILL.md and slash command, stale subdir inventory in `.working/README.md`, three-way section-header drift, awkward possessive, stale "Four rules" → "Six rules". |
| 2026-06-21 | 9 iter 3 | A, B, C | 3 (1H, 1M, 1L) | [#113](https://github.com/jposluns/grc_library/pull/113) | — | PR #112 close-out's own prose self-contradictions: P6/P7 inversion in register entry, mis-attributed origin trigger in CLAUDE.md, missing 1.27.0 rollout extension. |
| 2026-06-21 | 9 iter 2 | A, B, C | 1 (C1) + 1 discipline | [#112](https://github.com/jposluns/grc_library/pull/112) | — | Subagent B caught parallel `42 corpus gates` at `tools/check-changelog-on-pr.py:5`; fix-completeness inference cascade led to 7th pack rule (`validate-inference-before-action`) and gate 39 P7. |
| 2026-06-20 | 9 iter 1 | A, B, then C (late) | 4 (C1, C2) + 1 discipline | [#110](https://github.com/jposluns/grc_library/pull/110), [#111](https://github.com/jposluns/grc_library/pull/111) | — | Orchestrator initially skipped Subagent C without authorisation (discipline failure); C dispatched on maintainer prompt, surfaced two C2 findings. Led to Rule 5.6 + gate 39 P6. |
| 2026-06-20 | 8 | A only | 0 | — | — | Thin sweep (B/C scope-skipped per pre-tool preamble — no surface changes since Sweep 7). Empty-delta convergence, fourth consecutive zero-finding. Pattern: 4+, 3, 1, 1, 0, 0, 0, 0. |
| 2026-06-20 | 7 | A only | 0 | — | — | Thin sweep (B/C scope-skipped). Empty-delta primary-stop fired on first observable empty-delta after PR #91 introduced the convergence-delta termination conditions. |
| 2026-06-20 | 6 | A, B, C | 0 | [#89](https://github.com/jposluns/grc_library/pull/89) (register + exemption) | — | Full sweep, zero corpus findings. One scanner candidate at sweep-history meta-quote, added to exemption file. |
| 2026-06-20 | 5 | A only | 0 | — | — | Thin closure sweep after Sweep 4 closure PRs. Maintainer's post-sweep observation drove PR #86 (scanner heuristics + exemption file). |
| 2026-06-20 | 4 | A, B, C | 1 (C1, in-window) + 1 (follow-up) | [#83](https://github.com/jposluns/grc_library/pull/83) | — | First sweep using four-rule synthesis rubric (PR #82). C1: pack version literal "1.22.0" in adopter guide. Classification-convention follow-up deferred. |
| 2026-06-20 | 3 | A, B, C | 1 (C3, in-window) | [#80](https://github.com/jposluns/grc_library/pull/80) | — | Same-day cross-surface naming drift: SKILL.md used `### 3.5.` while slash command used `3a.`. Renamed to `3a.` for parity. |
| 2026-06-20 | 2 | A, B, C | 3 (C1, C3, discipline self-violation) | [#76](https://github.com/jposluns/grc_library/pull/76) | — | Meta-ironic: the just-shipped `skill-authoring-discipline` skill violated its own rules (stale prose, missing bidirectional See Also, description word count). |
| 2026-06-20 | 1 | A, B, C | 4 (C3) | [#63](https://github.com/jposluns/grc_library/pull/63) | — | First-ever sweep. Caught prior-corpus-count "37" prose left behind by PR #61's cleanup pass. |

## Open deferred follow-ups

Findings the maintainer deferred to track-as-follow-up (out-of-window or scope-bounded). Each carries `surfaced: YYYY-MM-DD` and an optional `re-triage-by:` deadline. See [`README.md`](README.md) §"Dating discipline for deferred findings" for the discipline.

- **Sweep 3 follow-up**: cross-document term-and-identifier consistency gap (the prose-and-numbering-shaped C3 surface that mechanical gates 35/39/41 don't cover). Surfaced: 2026-06-20. Candidate for a future mechanical gate; deferred pre-convention so not retro-stamped with `re-triage-by:`.
- **Sweep 4 follow-up**: classification-convention documentation (the failure-mode-classes table did not explicitly document the primary-plus-secondary classification rule). Surfaced: 2026-06-20. Documented in this README's §"Classification convention" in Sweep 4 close-out; resolved.

## Recurring-class summary

Cumulative count of findings per primary class, across all sweeps:

| Class | Total (primary) | Last seen |
| --- | --- | --- |
| C1: stale-prose | 9 | Sweep 10 iter 1 |
| C3: multi-surface-incomplete | 6 | Sweep 3 |
| C8: term-drift | 1 | Sweep 10 iter 1 |
| Discipline self-violation | 3 | Sweep 9 iter 2 (fix-completeness inference) |

Other classes (C2, C4, C5, C6, C7): zero primary-class findings to date.

The discipline reached empty-delta steady-state at Sweeps 5-8 (four consecutive zero-finding) before PRs #109+ introduced new content. Findings since then are post-PR prose drift; PRs #110-#112 added structural defences (gate 39 P6/P7, Rule 5.6, the 7th pack rule). Sweep 10 iter 1's six findings were all in-window prose drift from the post-PR-#117 set; no new structural rule needed.

## False-positive memory entries

*(None yet recorded under the formalised Rules 6.1-6.3 discipline. Pre-existing exemptions are in [`tools/sweep-preflight-exemptions.json`](../../tools/sweep-preflight-exemptions.json) and are grandfathered.)*
