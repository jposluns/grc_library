# Removed from skills/deep-assessment/SKILL.md (pack-hygiene scrub)

Each entry preserves, verbatim, project-specific text removed in the generalize-in-place
pass, with the replacement it received. The concrete names now live in the file's
"Project wiring" section.

## Overview, design-rules paragraph: inventory-source parenthetical

```
list; step 1 re-derives the live instrument inventory from the repo at run time
(`tools/run_all_audits.sh`, `.claude/commands/`, the audit-programme specification's
gate inventory). The live inventory of quality machinery IS the scope by construction:
```

Replaced by: "(from the runner scripts, command directory, and specification gate inventory named in the project wiring)".

## Overview, design-rules paragraph: `/screen-publications` provenance parenthetical

```
added to the phase-3 invocations by this duty, as `/screen-publications` (from the
#722 publications-screening cadence) is here.
```

Replaced by: "added to the phase-3 invocations by this duty, as `/screen-publications` was when its cadence shipped." (the PR-numbered cadence provenance is project history).

## Overview, design-rules paragraph: register path

```
Second, phase state lives in a
durable register (`.working/deep-assessment/register.md`), so the pass survives session
boundaries and a bare re-invocation resumes rather than restarts.
```

Replaced by: "a durable register (the phase-state register named in the project wiring)".

## Process step 1: register read and per-run record path

```
Read `.working/deep-assessment/register.md`. If a run is `in-progress`, resume at its
next incomplete phase; otherwise open a new run row and a per-run record file
(`.working/deep-assessment/<YYYY-MM-DD-rN>.md`, the dated-file convention the
fitness-review records use; the non-dated `register.md` stays in-repo by design).
```

Replaced by: "Read the phase-state register named in the project wiring. ... a per-run record file (the dated per-run record pattern named in the project wiring; the non-dated register stays in-repo by design)."

## Process step 1: sibling-repo names

```
all
three repos present (`grc_library`, `grc_library_ref`, `grc_library_scratch`), and the
session-concurrency interlock satisfied.
```

Replaced by: "the corpus repo, the reference base, and the worker exchange (as named in the project wiring) all present".

## Process step 1: inventory-derivation source list

```
Derive the live instrument inventory from the
repo, not from this skill's text: the gate list from `tools/run_all_audits.sh`, the
PR-time checks from `tools/run-pr-time-checks.sh`, the skill and command set from
`.claude/commands/` and the pack skills directory, the advisory tools from `tools/`,
and the specification's gate inventory section.
```

Replaced by: "the gate list from the audit runner, the PR-time checks from the delta runner, the skill and command set from the command directory and the pack skills directory, the advisory tools from the tools directory, and the specification's gate inventory section (each named in the project wiring)".

## Process step 2: runner and sibling-gate names

```
Run, standalone and unpiped: `tools/run_all_audits.sh`, `tools/run-pr-time-checks.sh`,
the linter regression suite, both generator `--check` invocations, and each sibling
repo's `tools/validate.py`.
```

Replaced by: "the audit runner and the PR-time delta runner (named in the project wiring), the linter regression suite, every generator `--check` invocation, and each sibling repo's own validation gate" (the count word "both" also genericized to "every" per the count-free design rule).

## Process step 3: advisory-aids list

```
Run the advisory aids whose outputs feed later
phases (`verify-reference-modules.py`, `audit-brief-freshness.py`, `residual-scan.py`
and `tension-scan.py` over the ledgers).
```

Replaced by: "(the phase-3 advisory aids named in the project wiring, including the ledger scanners)".

## Process step 4: gate-efficacy tool names

```
(a)
**blind-spot map**: run `tools/audit-gate-blindspots.py` to compute, from every
linter's own exemption configuration, which repo surfaces are scanned by which gates
and which are scanned by none; every fully-unscanned surface gets a manual review
noted in the run record. (b) **mutation probe**: in a DISPOSABLE copy of the repo
outside the working tree, seed defect variants per gate class with
`tools/audit-gate-mutation.py` and confirm each gate detects its class at pattern
```

Replaced by: "the blind-spot mapping tool named in the project wiring" and "the mutation-probe tool named in the project wiring".

## Verification: dated record directory

```
- The register shows every phase `complete` (or `deferred` with a maintainer-visible
  reason), each with a dated record file in `.working/deep-assessment/`.
```

Replaced by: "each with a dated record file at the per-run record location named in the project wiring".

## See Also: advisory-tools bullet with repo-relative links

```
- The advisory tools [`tools/audit-gate-blindspots.py`](../../../../tools/audit-gate-blindspots.py)
  and [`tools/audit-gate-mutation.py`](../../../../tools/audit-gate-mutation.py) with its
  variant library [`tools/gate-mutation-variants.json`](../../../../tools/gate-mutation-variants.json)
  (phase 4's deterministic halves; not gates; always exit 0 on completion of their
  report, 2 only on a safety refusal or internal error).
```

Replaced by: "The gate-efficacy tools named in the project wiring (phase 4's deterministic halves; not gates; always exit 0 on completion of their report, 2 only on a safety refusal or internal error)."
