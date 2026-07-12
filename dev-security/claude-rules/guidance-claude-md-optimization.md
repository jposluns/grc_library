# Optimizing a CLAUDE.md: keep-and-condense with a removal ledger

A `CLAUDE.md` (or any always-loaded rules file: `.cursorrules`, `AGENTS.md`, a
`.github/copilot-instructions.md`) is read on every turn, so its length is a standing tax
on the context budget. As a project accumulates conventions, the file grows, and the growth
is mostly rationale, war-stories, and provenance accreting around a smaller core of
actionable rules. Past a certain size the file starts to work against itself: the assistant
that must hold all of it loses focus on the rules that actually govern behaviour (the
context-flooding failure mode the `external/addyosmani/context-engineering.md` overlay
names).

This guidance describes how to condense such a file without losing a rule, and how to make
the condense reversible so a wrong cut can be caught and undone. It is a maintainer-facing
method, not a coding-time rule; it is invoked when a maintainer decides a rules file has
grown unwieldy, not on every PR.

The method has three parts: a keep-or-cut taxonomy, a removal ledger, and a verification
that targets the one failure that matters.

---

## When to condense (and when not to)

Condense when the file has grown to the point where a reader cannot hold its actionable
rules in view, and the growth is dominated by explanatory prose rather than by new rules.
The signal is qualitative (the maintainer reads it and judges it bloated), not a hard line
count; a dense 600-line file can be fine and a padded 300-line one can be due.

Do not condense as a routine or automatic pass. A condense is a deliberate, maintainer-directed
act, because deciding what is actionable versus what is rationale is a judgment call that
changes what the assistant is told to do. Treat it the way the `clarify-before-acting` rule
treats any authorial choice: the maintainer directs it, and the maintainer chooses the
depth (a light trim versus an aggressive keep-only-rules condense).

Do not condense by relocating rules to other files and calling the file shorter. Moving a
rule out of the always-loaded file changes whether the assistant sees it; that is a
behavioural change wearing a formatting change's clothing. Condensing means removing
non-actionable prose from the file, not redistributing actionable prose out of it.

---

## The keep-or-cut taxonomy

**Keep (actionable content the assistant acts on):**

- Rules and prohibitions ("never push directly to `main`", "bump Version and Date in the
  same commit").
- Procedure steps, in order, with the commands that execute them.
- Commands, file paths, gate names and numbers, thresholds, and other concrete values.
- Boundaries and the conditions that trigger an escalation or a clarification.
- Pointers to the authoritative source of a rule (so the short form does not become the
  only form).

**Cut (explanatory content the assistant does not act on):**

- Rationale and motivation ("why this rule exists", the cost-benefit argument behind it).
- War-stories and incident narratives (the specific session or PR that motivated a rule).
- Provenance and attribution that does not change what to do.
- Duplication: a rule stated in full in the file and also stated in full in the
  authoritative pack source. Keep one full statement (the source) and a one-line pointer in
  the always-loaded file.

The test for a given paragraph: if the assistant deleted it, would any action change? If
yes, it is actionable, keep it. If the paragraph only explains or justifies an action stated
elsewhere, it is a candidate to cut. When a cut is genuinely ambiguous, keep it; the cost of
a kept paragraph is a few tokens, the cost of a dropped rule is a behaviour regression.

---

## The removal ledger

Every cut is recorded in a removal ledger (a working-state file at a location the project
designates, outside the always-loaded context), so the condense is reversible and its bets
are falsifiable. Each ledger entry records:

- **What was removed**, quoted verbatim (so the original can be restored byte-for-byte). A
  fenced code block preserves the text exactly and, in projects whose prose-hygiene gate
  exempts code blocks, lets the ledger hold forbidden punctuation (em-dashes in the original)
  without tripping the gate.
- **Why it was removed** (which taxonomy category it fell into).
- **The expected gain** (what the removal buys: focus, length, reduced duplication).
- **The potential risk** (what could go wrong if the cut was a mistake).
- **The evidence the removal was wrong** (the concrete, observable signal that, if it
  appears, means the cut text should be restored or should inspire a new rule). This is the
  load-bearing field: it converts a silent deletion into a falsifiable bet.

The ledger is not a one-time artefact. Review it on a cadence (this project reviews it at
each retrospective and during the periodic hallucination-metrics pass): scan the open
entries, and if an entry's "evidence the removal was wrong" signal has appeared, advise the
maintainer to restore the cut or to author a new, tighter rule that addresses the gap.
Record the disposition in the entry. The ledger thus makes a condense a hypothesis under
ongoing test, not an irreversible loss.

The removal ledger is the change-tracking discipline applied to deletions: the same
audit-trail principle that requires a CHANGELOG entry for what shipped requires a recorded,
reviewable rationale for what was removed.

---

## Verifying the condense

A condense has exactly one failure that matters: a dropped actionable rule. The verification
targets that failure directly, per the `evidence-grounded-completion` protocol (do not assert
"no rule was lost" from the impression that the diff looked safe).

Two complementary checks:

1. **Actionable-token survival.** Enumerate the concrete, greppable tokens the file carried
   (command names, file paths, gate numbers, thresholds, rule keywords) and confirm each
   still appears in the condensed file or in the authoritative source the condensed file now
   points to. A token that vanished from both is a dropped rule.
2. **Section-by-section old-versus-new walk.** Read the pre-condense file and the
   post-condense file in parallel, section by section, and confirm every actionable rule,
   step, boundary, and value in the old version is present (in full or as a pointer) in the
   new one. The only tokens that should disappear without a pointer are the ones the ledger
   records as intentional cuts.

If the project's rules file is mechanically gated (a corpus audit, a lint suite), run the
gate on the condensed file as well; but the gate proves only what it checks. "The gate
passes" is not "no rule was lost", because most gates do not check for a missing rule. The
two checks above are the semantic layer the gate does not provide.

---

## Relationship to the rest of the pack

- `evidence-grounded-completion`: the verification above is that rule's protocol (enumerate,
  re-read, contradiction-search, distinguish mechanical from semantic) applied to a condense.
- `change-tracking`: the removal ledger is the audit-trail discipline applied to deletions;
  the condense itself also carries a normal CHANGELOG entry.
- `clarify-before-acting`: a condense is maintainer-directed, and its depth is a choice the
  maintainer makes, not a default the assistant picks.
- `artefact-and-branch-discipline`: do not condense a generated file; condense its source
  and regenerate.

---

## Worked example

This library condensed its own project `.claude/CLAUDE.md` from 881 to 634 lines (about 28
percent) under a maintainer "keep actionable rules, cut rationale, war-stories, and
duplication" directive. The largest single cut replaced the full descriptions of the pack's
governance rules with one-line purposes plus a pointer to the pack README (the rules are
stated in full there, so the always-loaded file carried a duplicate). A version-bump
operationalization that a newly-added pre-push guard had mechanized collapsed to a one-line
pointer at the guard. Every cut was recorded in the project's removal ledger with
its verbatim original and falsification signal; the verification was an actionable-token
survival grep plus a section-by-section walk, both finding zero dropped rules, plus a green
run of the corpus audit. The condensed file kept all of its section headers and every
procedure step; only non-actionable prose left the file.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Recorded rationale for a removal | PO.5, RV.2 | CCC-01 to 03 | A.5.4, A.8.32 |
| Audit trail of what was removed and why | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15 |
| Verification before claiming completeness | RV.1, RV.2 | GRC-05 | A.5.36 |

---

## Why this guidance exists

An always-loaded rules file degrades in a predictable direction: it accretes the rationale
for each rule alongside the rule, and the rationale eventually outweighs the rules. Trimming
it is obvious; trimming it without losing a rule, and without the loss being silent and
irreversible, is the hard part. The removal ledger is the mechanism that makes a condense
safe to attempt: every cut is recorded with the signal that would prove it wrong, and the
cadence review turns those signals into restorations or new rules. A condense without a
ledger is a one-way deletion the maintainer cannot audit; a condense with one is a reversible
hypothesis the project keeps testing.
