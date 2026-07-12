# Removed from skills/guardrail-review/SKILL.md (pack-hygiene scrub)

Each entry below preserves, verbatim, a passage removed from the skill during the
generalize-in-place scrub, with the generic replacement that took its place. Concrete
project values now live only in the skill's "Project wiring" section.

## Overview, paragraph 1 (concrete wiring-surface examples)

```
the wiring surfaces that keep all three in lock-step (a gate declared across the CI workflow, the local runner, the pre-commit config, and the audit-programme spec; a rule mirrored from the pack into the local rules copy and enumerated in three places; a skill paired with a slash command and registered for step-parity). The mechanical parity gates verify that these surfaces agree by identity and count: the gate names match across four surfaces, the rule mirror is byte-identical, the skills directory matches the README tree, the paired step-identifiers match.
```

Generic replacement: "(a gate declared across every parity surface the project maintains; a rule mirrored from the pack into a local rules copy and enumerated wherever the project lists its rules; a skill paired with a slash command and registered for step-parity)" and "the gate names match across their surfaces, ... the skills directory matches the enumeration tree"; the concrete four-surface list and enumeration surfaces moved to the project-wiring section.

## When to Use, auto-prompt bullet (cadence-currency gate)

```
gate 60 (guardrail-review cadence currency) compares the live machinery inventory (the gate, rule, skill, and command counts) against the newest history row's as-of counts, passing with a warning while the summed per-axis drift is 1 or 2 and failing the build once the drift reaches 3, so a deferred review is mechanically forced before the machinery drifts far.
```

Generic replacement: "a cadence-currency backstop gate (named in the project wiring) compares the live machinery inventory against the newest history row's as-of counts, passing with a warning while the drift stays small and failing the build once the drift crosses the gate's threshold, so a deferred review is mechanically forced before the machinery drifts far."; the gate number and drift thresholds moved to the project-wiring section.

## When to Use, NOT bullet (parity-gate enumeration)

```
- **NOT** as a substitute for the mechanical parity gates (35 gate-name parity, 37 claude-rules-sync, 39 gate-count consistency, 41 collection-enumeration, 44 paired-skill step-parity). Those run every PR and catch identity/count drift mechanically; guardrail-review is the semantic layer above them, not a replacement for them.
```

Generic replacement: "the mechanical parity gates named in the project wiring"; the numbered gate list moved to the project-wiring section.

## Process step 1, baseline paragraph (runner and history-aware gates)

```
Run `tools/run_all_audits.sh` and confirm it exits 0. The mechanical parity gates (35, 37, 39, 41, 44) must be green before the semantic review begins: a red parity gate is an identity/count defect to fix mechanically first, not a structural finding for this skill. (The baseline run includes the git-history-aware gates 31 and 40; if the clone is shallow they misfire, so confirm `git rev-parse --is-shallow-repository` prints `false`, and `git fetch --unshallow` first if it does not.)
```

Generic replacement: "Run the project's full audit suite (the mechanical baseline runner named in the project wiring) ... The mechanical parity gates named in the project wiring must be green ... (Where the baseline run includes git-history-aware gates, a shallow clone makes them misfire, so confirm ...)"; the runner path and all gate numbers moved to the project-wiring section.

## Process step 1, inventory bullets (concrete paths and surfaces)

```
- **Governance rules**: the files under `dev-security/claude-rules/governance/` and their `.claude/rules/governance/` mirror, plus the three enumeration surfaces (pack README tree, pack `CLAUDE.md`, project `.claude/CLAUDE.md`).
- **Skills**: the directories under `dev-security/claude-rules/skills/`, each with its `derives_from` parent, its slash-command counterpart (if paired), its PAIRS registration, and its README-tree entry.
- **Gates**: the audit gates declared across the four parity surfaces (CI workflow, runner, pre-commit, audit-programme spec §6), each with its linter and the discipline it enforces.
```

Generic replacement: "the pack's rule files, their project-local mirror, and every enumeration surface that lists them (the concrete surfaces are named in the project wiring)", "its pairing registration, and its enumeration-tree entry", and "the project's parity surfaces (named in the project wiring)"; the concrete directory paths, the PAIRS registry name, and the four-surface list moved to the project-wiring section.

## Process step 2, gap lens (ledger paths)

```
a recurring failure mode (visible in `.working/improvement-log.md` or `.working/hallucination-metrics.md`) that no rule names and no gate catches?
```

Generic replacement: "(visible in the failure-mode ledgers named in the project wiring)"; the two ledger paths moved to the project-wiring section.

## Process step 2, drift lens (dated incident)

```
(The recurring real instance: a convention revised in the rule but left stale in a one-line enumeration description, which the resume `/validate` of 2026-06-23 caught in the pack README.)
```

Generic replacement: "(The recurring real instance in the parent library: a convention revised in the rule but left stale in a one-line enumeration description, caught only later by a routine content sweep.)"; the sweep date and pack-README locus are project history.

## Process step 5, Record (record path and project-history attribution)

```
Write a per-run record (in this project `.working/guardrail-reviews/YYYY-MM-DD-rN.md`) with one section per lens (overlap, gap, drift), an orchestrator-synthesis-and-verification section, and a findings-routed section.
```

```
a record written from fix intent rather than from the diff is the record-asserts-unapplied-fix escape a pre-push verifier caught in this project's history, and the false claim propagates to every surface that restates the record's counts.
```

Generic replacement: "(at the per-run record path named in the project wiring)" and "caught in the parent library's history"; the record path moved to the project-wiring section.

## Common Rationalizations, gap row (ledger names)

```
| "There is no gap; everything important has a gate." | "Important" is the judgment under review. Check `improvement-log.md` and `hallucination-metrics.md` for recurring failure modes; a pattern with no rule and no gate is a gap regardless of how it felt. |
```

Generic replacement: "Check the failure-mode ledgers named in the project wiring for recurring failure modes"; the ledger names moved to the project-wiring section.

## See Also, deep-qa-review entry (four-surface phrasing)

```
- Related skill [`deep-qa-review`](../deep-qa-review/SKILL.md) (`/full-qa`): its audit-programme-integrity subagent (C) checks the four-surface parity within a trust-recovery window; guardrail-review generalizes that check to the standing machinery and adds the overlap and gap lenses.
```

Generic replacement: "checks the gate-wiring parity within a trust-recovery window"; the four-surface count is the parent library's wiring.

## Why this skill exists (growth counts and dated incident)

```
The governance machinery of this project grew from five rules to thirteen, from a handful of skills to twenty-one, and from a dozen gates to sixty-eight, each addition wired across multiple surfaces. The mechanical parity gates grew alongside it and reliably catch identity and count drift: a gate missing from one of its four surfaces, a rule mirror that fell out of sync, a skill absent from the README tree. What they cannot catch is the slow architectural erosion that comes with growth: two rules that have come to overlap, a discipline added to a CLAUDE.md section that no gate ever enforced, a one-line rule description that drifted in meaning from the rule it describes while the mechanical mirror check stayed green. Each of those is a structural defect invisible to a string-matcher and visible to a designer reading the machinery as a system. The resume `/validate` of 2026-06-23 caught a concrete instance (a routing convention revised in the rule but left stale in two pack-README enumeration descriptions); guardrail-review is the standing, periodic review that hunts that class deliberately rather than waiting for a content sweep to stumble on it.
```

Generic replacement: "The governance machinery of the parent library grew severalfold across its rules, skills, and gates" (the growth lesson kept, the counted trajectory archived here); "one of its parity surfaces" and "the enumeration tree" for the four-surface and README-tree phrasings; and "A routine content sweep in the parent library caught a concrete instance (a routing convention revised in the rule but left stale in two enumeration descriptions)" for the dated sweep sentence.
