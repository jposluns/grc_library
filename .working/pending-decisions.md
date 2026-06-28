# Pending Decisions

**Status:** empty.

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (for example because the `AskUserQuestion` primitive errors, a transient
permission-stream failure), it records the decision here and continues, rather than
stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Entries

_No pending decisions._

The previously-queued entries were all resolved and rotated out at the 2026-06-28
resume (this Sweep-73 close-out PR):

- **TODO §4.10 (TODO/DONE rotation gate) design disposition**, RESOLVED: the maintainer
  chose **Option B (the "marked-done detector")** over deferral or the FP-prone id-cross-check
  (Option A). The build is queued in this session's guard-rails phase; the decision is recorded
  inline in TODO §4.10.
- **MITRE ATLAS scratch version update**: the grc_library register half is done and
  authoritative (`register-canonical-citations.md` ATT&CK `v19.1` / ATLAS `v2026.05`). **Scope
  update (maintainer, 2026-06-28 resume): this session now owns BOTH repos and may write to
  scratch** (superseding the earlier "another session owns scratch"). So the scratch half (archive
  the deprecated ATLAS `v5.6.0` into `ref/.superseded/`, store upstream `v2026.05`, refresh
  `catalogue.yml`) is now THIS session's to do, via MCP PR to the scratch branch
  `claude/resume-todo-prioritization-i4sl26`; folded into the §4.26 scratch track alongside the
  per-reference `last_checked` fields (fed by the in-flight version-currency research worker).
  **Maintainer directive (2026-06-28): ATLAS is publicly available; update it in the scratch repo
  at next convenience.** Queued as a scratch PR (archive the deprecated `v5.6.0` into
  `ref/.superseded/`, store upstream `v2026.05` as-is, refresh `catalogue.yml`); not blocking the
  grc_library queue, scheduled at a convenient seam (likely with or right after the FR-167 AICM
  column work, which also draws on the scratch `ref/standards/CSA/` extracts).
- **The four #428 PRI-\* CCM mappings** (GRC-06 / DSP-12 / DSP-10 / charter DSP-domain),
  RESOLVED: maintainer-confirmed 2026-06-28, no changes.

The audit trail for the rotated entries lives in the relevant TODO items, the CHANGELOG and
its detailed mirror, [`DONE.md`](DONE.md), and git history.
