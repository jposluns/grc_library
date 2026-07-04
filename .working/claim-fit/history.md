# Claim-Fit Citation-Precision Audit History

**Version:** 1.0.1\
**Date:** 2026-07-04\
**License:** CC BY-SA 4.0

Reverse-chronological table of every `/claim-fit` invocation against this library. New rows on top. Each row summarises one cadenced citation-precision audit of normative-attribution claims; detail for findings-producing runs lives in a per-run file `YYYY-MM-DD-<scope>.md` linked from the **Detail** column. A zero-finding run gets a history row with `Detail` = `none`.

`/claim-fit` judges the gate-blind FR-120 "attributed value, silent source" class (a sentence ties a specific value to a named normative source whose citation passes the existence and citation gates, but the source does not prescribe the attributed value). It is the precision layer on top of the citation gates, not a substitute for them. See the [`claim-fit` SKILL](../../dev-security/claude-rules/skills/claim-fit/SKILL.md) for the six-step process and the [`/claim-fit`](../../.claude/commands/claim-fit.md) slash command. Cadence: the one-time full Tier-A pass at adoption, after any batch that adds or edits normative-value claims, and ad-hoc.

This file is maintainer working state, exempt from corpus audit gates.

## Run entries

| Date | Scope | Worklist | Judge | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|---|
| 2026-07-04 | One-time Tier-A adoption pass (whole census; Tier B not sampled, per-batch cadence covers it going forward) | 11 Tier-A rows from `audit-claim-precision.py --tier A` (census 11 A + 119 B); sibling-carrier bare-token greps widened the fix set by two carriers the single-clause extractor cannot see | One citation-precision judge subagent, four-valued verdicts, every verdict quoting the held source passage; orchestrator re-read every candidate passage before treatment | 12 source-halves `prescribed`; 4 `informed-not-prescribed` (the ISO/IEC 42001 half of the three 7-year carriers; the DORA windows, whose existing RTS hedge already signals the delegation, no text change); 4 `mis-attributed` FIXED in-window (the Annex IV half of the 7-year carriers, Annex IV carrying no retention obligation; the 24-hour KPI "per Article 33(2)", the article setting "without undue delay"); 4 `source-not-held` (UK GDPR Arts 15/16, PIPL Arts 45/46, queued as source drops with the DORA RTS) | S3 PR B (this PR) | [`2026-07-04-tier-a-adoption-pass.md`](2026-07-04-tier-a-adoption-pass.md) | Five documents corrected across six carrier locations (attribution phrasing only, per the FR-120 precedent; no value changed): the ops monitoring procedure, the third-party-AI due-diligence procedure (both lines), the retention register's AI-log basis cell plus its AI-Impact-Assessments row (the sixth carrier, verifier-caught at a differing token pair), the breach-response KPI row, and the supplier-assurance DPA table. All design-entry early candidates confirmed; the Annex IV half sharpened to mis-attributed. Three source-drop requests to the maintainer (DORA Art 20 RTS, UK GDPR, PIPL); a scratch currency note (no `last_checked` on the judged legislation/standards items); the register :106/:107 rows and two records-retention Tier-B alignments flagged for the first per-batch cadence. |
