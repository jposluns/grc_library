# Reference-audit records

Per-run records for the `/reference-audit` cadenced skill (the reference-breadth audit
between the corpus and the held reference base, both directions; skill at
[`dev-security/claude-rules/skills/reference-audit/SKILL.md`](../../dev-security/claude-rules/skills/reference-audit/SKILL.md)).

Layout, per the current-week `.working` model:

- `history.md` (non-dated, stays in-repo): one row per run, appended always, including
  zero-finding and empty-candidate runs (the proof-of-discipline).
- `doc-state.md` (non-dated live surface, stays in-repo): maps each corpus document to
  the `grc_library_ref` commit it was last audited against; the per-touch mode's delta
  anchor. Rewritten by `tools/audit-reference-breadth.py --update-state`; committed
  with the touching PR's QA batch. Never hand-edit a SHA.
- `YYYY-MM-DD-<scope>.md` (dated per-run detail files): written when a run has
  findings; swept to the scratch weekly archive by
  `tools/sweep-working-records-to-scratch.py` under the current-week model.
