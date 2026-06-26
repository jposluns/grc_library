# `.working/validate-sweeps/`: Maintainer Working State

This subdirectory holds project-specific working state for the `validation-sweep` discipline. The discipline itself (failure-mode taxonomy, maintenance protocol, accept-list rules, dispatch-declaration discipline) is template content and lives in the [`validation-sweep` skill](../../dev-security/claude-rules/skills/validation-sweep/SKILL.md) in the dev-security claude-rules pack; the files here are *our* log of *our* sweeps performed against THIS library.

Adopters cloning the library inherit no historical sweep entries (their own sweep history starts at zero when they first invoke `/validate` in their own fork).

## Files in this subdirectory

| File | Purpose |
|---|---|
| `README.md` | This file: static convention info that applies to every sweep |
| `history.md` | Reverse-chronological table of every sweep iteration: date, sweep ordinal, finding counts, resulting PR, one-line summary. New rows at top. |
| `YYYY-MM-DD-sweepN-iterM.md` | Per-iteration detail file. **Created only when the iteration produced findings.** Captures full subagent transcripts, orchestrator synthesis, and actions. Zero-finding iterations leave only a row in `history.md`. |

## Per-iteration detail file format

When an iteration produces findings, the per-iteration record uses six H2 sections in this order, comma form:

1. `## Trigger & state snapshot`, what triggered this iteration; library/pack version/gate-count/skill-count/rule-count at HEAD; iteration ordinal within the sweep
2. `## Subagent A, Recent-PR deep review`, verbatim return from subagent A
3. `## Subagent B, Corpus-wide stale-reference sweep`, verbatim return from subagent B
4. `## Subagent C, Audit-programme integrity reviewer`, verbatim return from subagent C
5. `## Orchestrator synthesis`, in-window classification, severity adjudication, dedupe choices, debate outcomes, actions decided
6. `## Resulting PR`, link to the close-out PR, or `none, zero findings`

Filename `YYYY-MM-DD-sweepN-iterM.md` where `N` is the sweep ordinal (continues the numbering in `history.md`) and `M` is the iteration within that sweep.

## Why this split (history table + optional per-iteration detail)

- The table is a fast scan of "what sweeps ran and when, with what outcome". The maintainer reading `history.md` learns the trend without paging through verbose entries.
- The detail files are the persistent archive of subagent reports + synthesis for sweeps that actually surfaced findings. Reconstructible audit trail for those sweeps.
- Zero-finding iterations leave no detail file because there is no substantive content beyond "we ran the sweep and it was clean". The history row records the iteration occurred and reached steady state; that is enough.

## Failure-mode classes (mirror of the validation-sweep skill's catalogue)

The eight classes the sweep targets, as a stable identifier set used in `history.md` entries:

| Class | Shape |
| --- | --- |
| C1: stale-prose | Stale gate-counts / version-mentions in prose |
| C2: mis-attribution | Citation of "step X" / "section Y" where cited content does not match source |
| C3: multi-surface-incomplete | Change updates N-1 of N surfaces |
| C4: inferred-state-assertion | Claim about file contents without re-reading |
| C5: version-bump-omission | Non-exempt document changed without `Version:` bump |
| C6: generated-artefact-lag | Source edited but generator not re-run |
| C7: stale-docstring | Linter/script docstring no longer matches code |
| C8: term-drift | Different files use different terms for same concept |

### Classification convention: primary plus optional secondary

A finding may belong to more than one class at once. A multi-surface miss that surfaces as stale prose is both C3 (mechanism) and C1 (symptom).

1. **Each finding is tagged with a primary class** that names its dominant mechanism (the root cause an audit gate would target to prevent recurrence).
2. **Each finding may optionally carry one or more secondary classes** that name the symptom shape a reader would notice first.
3. **The recurring-class summary tracks primary-class counts** (these are what mechanical defences should target). Secondary classes are tracked in per-iteration detail files when relevant.
4. **Per-iteration entries record findings as `primary [+ secondary]`** (e.g. `C3+C1` for a multi-surface miss that surfaced as prose drift, or just `C1` for a pure stale-prose finding).

Historical entries from Sweeps 1-4 were classified before this convention; their primary classes are preserved as-is. The convention applies forward from Sweep 5.

## Dispatch declaration (Rule 5.6)

Every sweep iteration that produces a per-iteration detail file must declare which subagents were dispatched, e.g. `Subagents dispatched: A, B, C` for a full sweep; `Subagents dispatched: A only; B and C scope-skipped per maintainer authorisation [link or quote]` for a thin sweep. Per the SKILL's Rule 5.6, a subagent's silent absence cannot be reconstructed later; the dispatch declaration is the enforcement point. Convention applies forward from 2026-06-20.

## False-positive memory (accept-list discipline, Rules 6.1-6.3)

Findings the maintainer triages as not-a-real-finding should not be re-surfaced. Each accept-list entry carries a fingerprint, an `accepted_on` date, an `expires` date (default `accepted_on + 90 days`), and a one-line rationale. On `expires` the entry is re-triaged, not auto-renewed. The net-negative invariant (Rule 6.3) requires `|accept-list|` to not grow net of fixes across a sweep close.

The pre-flight scanner's machine-readable counterpart is [`tools/sweep-preflight-exemptions.json`](../../tools/sweep-preflight-exemptions.json), which suppresses known false-positive shapes at scanner time before they reach a subagent. The two surfaces share the same Rules 6.1-6.3 discipline.

## Dating discipline for deferred findings

Findings the maintainer defers (out-of-window, track-as-follow-up, or otherwise not actioned in the surfacing PR) accumulate ageing risk: without a date stamp, a 6-month-old follow-up is indistinguishable from a 6-day-old one.

- **`surfaced: YYYY-MM-DD` on every deferred finding entry.** ISO 8601, sortable lexicographically. The date is when the sweep first surfaced the finding, not when the maintainer noticed.
- **`re-triage-by: YYYY-MM-DD` is optional and defaults to `surfaced + 30 days`.** Mirrors the GitHub `actions/stale` 30-day default and the project's existing exception-register default in [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md). When the deadline passes, the maintainer either re-triages (record a `re-triaged: YYYY-MM-DD` line), closes the follow-up, or extends `re-triage-by` with a one-line rationale.
- **Gate 43 ([`tools/lint-followup-ageing.py`](../../tools/lint-followup-ageing.py)) enforces** this discipline by scanning `history.md` for `re-triage-by:` deadlines past `today()` with no fresh `re-triaged:` trailer.

Sources: Wikipedia `{{citation needed|date=...}}` maintenance-template convention; GitHub `actions/stale` 30-day default; Self-Admitted Technical Debt (SATD) issue-tracker dating (Bavota and Russo, arXiv:2007.01568); ISO 8601 audit-trail encoding. Recreated as CC BY-SA 4.0 prose; no external rule files imported.

## Audit-gate exemption

The `.working/` directory tree is in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. Files here are exempt from corpus audit gates: broken-link drift, language-style drift, citation staleness, orphan status are expected and do not fail CI. Gate 43 (`lint-followup-ageing`) is the single exception that intentionally scans into `.working/validate-sweeps/history.md` for the deferred-finding ageing discipline.

## Adopter guidance

If you fork this library:
- **The convention** (this README, the SKILL.md, the slash command) is template content. Adopt it directly.
- **The contents of `history.md` and any per-iteration files** are upstream maintainer's working state. You may keep them as historical reference of the upstream discipline in action, or delete and start fresh from your first `/validate` invocation. Either is fine.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Audit trail of verification activity | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15 |
| Trend analysis of defect categories | RV.1 | GRC-05 | A.5.36 |
| Documented false-positive handling | PO.5 | GRC-04 | A.5.4 |
