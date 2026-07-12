# Removed from skills/reference-audit/SKILL.md (pack-hygiene scrub)

Each entry preserves the original project-specific text verbatim, with one line naming
what replaced it in the generalized skill. The concrete tool paths, state-file and
run-record locations, reference-base repository name and indexes, and trust-tier bucket
assignments now live in the skill's `## Project wiring` section; the entries below are
the in-body occurrences that were genericized.

## Frontmatter `description` (project-specific clauses)

```
description: Cadenced reference-breadth audit between the corpus and the held reference base, in both directions. Catches the gate-blind SP 800-154 class, "held but unused": an authoritative source sits in the reference base while corpus documents that its content would materially improve never engage it, and, in the reverse direction, a corpus document is touched while newly ingested or updated reference material that bears on it goes unnoticed. Run it exhaustively (the FULL mode, a deep-assessment member and a standing cadence), per touched corpus document (the per-touch mode, delta-filtered against a per-document state file), and per reference ingest (the new-ingest mode). It dispatches a semantic judge over the recall-oriented worklist that `tools/audit-reference-breadth.py` produces, adjudicating each candidate pairing against the held source text and the corpus document, then routes confirmed improvements under the normal triage. It catches what the citation gates structurally cannot: breadth needs a judgement about what a document SHOULD engage, not a check of what it already cites.
```

Replaced by: the class named generically as the "held but unused" class (the SP 800-154
incident naming is project history) and the tool path replaced with "the project's
recall-oriented triage tool".

## Overview, paragraph 2 (dated motivating incident)

```
The class is not hypothetical. The motivating incident (maintainer-directed 2026-07-07):
NIST SP 800-154's guidance was relevant to held corpus content while the corpus did not
engage it, and nothing in the audit programme could have said so.
```

Replaced by: "The class is not hypothetical. The motivating incident in the parent
library: a held authoritative source's guidance was relevant to corpus content while
the corpus did not engage it, and nothing in the audit programme could have said so."

## Overview, paragraph 3 (tool path and sibling-repo naming)

```
`reference-audit` is the semantic-judge half of a two-part instrument whose
recall-oriented triage half is the advisory tool `tools/audit-reference-breadth.py`
(explicitly NOT a gate; always exits 0; CI cannot host the check because the ground
truth lives in the sibling private reference repo).
```

Replaced by: "the advisory worklist tool named in the project wiring (explicitly NOT a
gate; always exits 0; CI cannot host the check because the ground truth lives in the
separate reference base, outside the corpus repository)".

## Overview, paragraph 4 (dated trust-tier decision and publications narrative)

```
Trust tiers are load-bearing (maintainer decisions, 2026-07-08).
```

```
The publications bucket is EXCLUDED by default (screen-first tier; the
`publication-screening` process (`/screen-publications`) now exists, so its inclusion
awaits the screening wave that flips `pending` register rows to `screened` plus the
maintainer's inclusion decision).
```

Replaced by: "Trust tiers are load-bearing maintainer decisions." (the tier rules
themselves are retained in full as normative content) and "The publications bucket is
EXCLUDED by default (screen-first tier: an item becomes a candidate only after the
`publication-screening` process (`/screen-publications`) flips its screening-register
row to `screened`, plus the maintainer's inclusion decision)." (the "now exists" /
"screening wave" narrative is project history).

## When to Use (per-touch and new-ingest flag mentions)

```
- **Per-touch mode on every substantive corpus-document PR**: when a PR touches a
  corpus document's body, run the tool in `--docs` mode for the touched documents.
```

```
- **New-ingest mode after reference-base changes**: when the reference base ingests or
  updates items, run `--ref-since <sha>` (or `--ref-items <substring>`) to list the
  corpus documents each changed item topically matches and does not cite, and judge
  those pairings.
```

Replaced by: "change" for "PR", and the concrete flags replaced with "the triage tool in
its per-touch form" and "the triage tool in its new-ingest form (scoped to the reference
delta)"; the flags are listed in the project wiring.

## Process step 1 (audit-runner path and reference-base index paths)

```
new-ingest with the reference delta) and confirm `tools/run_all_audits.sh` exits 0
first; a breadth pass proposes additions to a corpus that already passes its gates.
Confirm the reference base is available and locate it via its indexes
(`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`,
`grc_library_ref/SECTION-INDEX.md`, `grc_library_ref/COVERAGE-MAP.md`); the per-source
```

Replaced by: "confirm that the project's full audit suite exits 0 first" and "Confirm
that the reference base named in the project wiring is available and locate held items
via its indexes".

## Process step 2 (invocation line, alias-map path, PR wording)

```
Run `python3 tools/audit-reference-breadth.py --ref-base
<path-to-grc_library_ref-checkout>` in the mode's form: bare for FULL; `--docs <path>
[<path> ...]` for per-touch; `--ref-since <sha>` or `--ref-items <substring>` for
new-ingest.
```

```
NO-KEY rows on non-book items are alias-curation work for
`tools/reference-breadth-aliases.json` (fix the alias in the same run); NO-KEY on books
is expected. In per-touch mode, an empty candidate set for every touched document ends
the run at this step with a one-line note in the PR's QA trail; no judge is dispatched
on an empty set.
```

Replaced by: "Run the triage tool named in the project wiring, pointed at the reference
base, in the mode's form" (concrete flags in the wiring), "the curated alias map named
in the project wiring", and "the change's QA trail".

## Process step 6 (state-refresh flags and state-file path)

```
found empty), run the tool again with `--docs <touched paths> --update-state` so the
state file (`.working/reference-audit/doc-state.md`) records the reference-base HEAD
each document was audited against, and commit the state refresh with the PR's QA batch.
```

Replaced by: "run the triage tool again in its state-refresh form for the touched
documents so the per-document state file named in the project wiring records the
reference-base HEAD each document was audited against, and commit the state refresh
with the change's QA batch".

## Process step 7 (run-record path and scratch-archive sweep note)

```
Write the run to `.working/reference-audit/` as a dated per-run record file
(`YYYY-MM-DD-<scope>.md`, swept to the scratch archive under the current-week model)
```

Replaced by: "Write the run to the run-record directory named in the project wiring as
a dated per-run record file (`YYYY-MM-DD-<scope>.md`)"; the scratch-archive current-week
sweep is the parent library's record-retention convention, noted on the run-record
bullet in the project wiring.

## Red Flags (state-refresh flag)

```
- Skipping the `--update-state` refresh after a per-touch adjudication.
```

Replaced by: "Skipping the state-refresh step after a per-touch adjudication."

## Verification (audit-runner path and PR wording)

```
- The mode and scope were named and the mechanical baseline was clean
  (`tools/run_all_audits.sh` exit 0) before the semantic read.
```

```
- The per-document state was refreshed for the run's scope and committed with the
  run's PR batch.
```

Replaced by: "(the project's full audit suite exited 0)" and "the run's change batch".

## See Also (three project-wired bullets)

```
- The advisory tool [`tools/audit-reference-breadth.py`](../../../../tools/audit-reference-breadth.py):
  the recall-oriented triage step that feeds this skill's worklist (not a gate; always
  exits 0; `--docs` for per-touch with `--update-state` for the delta anchor,
  `--ref-since` / `--ref-items` for new-ingest, `--include-publications` only under an
  explicit screening decision), with its curated alias map
  [`tools/reference-breadth-aliases.json`](../../../../tools/reference-breadth-aliases.json).
- The advisory tool [`tools/audit-reference-acquisition-gaps.py`](../../../../tools/audit-reference-acquisition-gaps.py):
  the complementary cited-but-not-held direction to this skill's breadth judgement. Where
  this skill and `audit-reference-breadth.py` ask whether the corpus USES what the base
  holds, the acquisition tool asks whether the corpus CITES a source the base does NOT
  hold (an acquisition candidate for the ref-base acquisition queue and the maintainer
  source-drop list), diffing the corpus canonical-citations register against the ref
  catalogue. Also advisory, never a gate; always exits 0.
- The reference base: the `grc_library_ref` repo located via its indexes, with the
  per-source currency confirmation, the superseded-archival workflow, and the
  trust-bucket rules the `grc_library_ref` repo's own conventions define.
```

Replaced by: the same three bullets rewritten to name each instrument generically as
"named in the project wiring", with the concrete paths, links, flags, and the
`grc_library_ref` repository name carried in the project wiring section.
