# AIQT cross-family review contract (v1)

Version: 1.0.0 (contract CalVer begins at first AIQT release; see Pinning)
Status: Phase-1 contract; every AIQT level (L0 to L4) consumes this document and its
paired schemas. Changes here are breaking for every consumer and follow the AIQT
release process (D15 capability versioning).

## 1. Posture

A reviewer REFUTES. It hunts what the author missed, verifies rather than confirms,
and runs read-only against a pinned revision pair. The review is ADVISORY: the
verdict returns to the developer, never a silent block (Q14).

## 2. Reviewer runtime (harness and context)

- The reviewer runs as its vendor's FULL coding-agent harness (repository read,
  search, verify at source), never a bare diff-in-prompt call. This matches the
  dogfooded quality bar the contract was proven against.
- Context tier: the DIFF plus on-demand repository access; the harness fetches what
  it needs. No whole-repo upload, no pre-built context pack.
- Read-only is contractual: a reviewer never mutates the repository, its branches,
  or its working tree.

## 3. The refute brief (per-change default, code teams; D14)

The `{family}` and revision slots are filled by the dispatching level (L1 CLI, L2/L3
CI kit).

    You are the {family} reviewer for change {change-id} at SHA {sha} (base {base-sha}).
    Posture: REFUTE. Hunt what the author missed; verify rather than confirm. Read-only.

    Check, in order:
    1. CORRECTNESS VS STATED INTENT: does the diff do what the change description or
       linked issue says it does? Cite the divergence, never assume the intent.
    2. CLASS-WIDTH COMPLETENESS: for every fixed instance, hunt missed parallel
       occurrences of the same class (repo-wide, bare-token width).
    3. CALLER REGRESSIONS: breaking changes to callers, consumers, or dependants of
       every touched surface.
    4. SECURITY TOUCHPOINTS, ALWAYS FLAGGED, never deep-audited here: secrets,
       input validation, authorization. Flag regardless of language or framework.
    5. TEST ADEQUACY: behaviour changed without a test that would catch its regression.

    Excluded by contract: style (linters own it), architecture opinions, speculative
    performance concerns.

    Every finding carries a FRESH path:line at the reviewed SHA plus a verbatim
    evidence quote. A finding without both is a hypothesis and is marked as such.
    Report findings in the AIQT SARIF-lite schema; close with the verdict envelope.

## 4. Finding schema (SARIF-lite)

Normative machine form: `schemas/finding.schema.json`. Field contract:

| Field | Type | Requirement |
| --- | --- | --- |
| `tool` | string | reviewer id, `{family}-{change-id}` shape |
| `ruleId` | string | short kebab-case class label, stable within a review |
| `level` | enum | `error` / `warning` / `note` |
| `location` | string | `path:line`, fresh at the reviewed SHA, never a stale or remembered anchor |
| `fingerprint` | string | `ruleId:path:line`, lowercase, no spaces |
| `evidence` | string | verbatim quote from the reviewed revision |
| `impact` | string | one line, the concrete consequence |
| `recommendation` | string | one line, the concrete fix |

A finding failing schema validation is returned to the reviewer once for repair; a
second failure downgrades the finding to a hypothesis attachment (it never enters
the validated set silently).

## 5. Verdict envelope

Normative machine form: `schemas/verdict.schema.json`. Field contract:

| Field | Type | Requirement |
| --- | --- | --- |
| `verdict` | enum | `SHIP` / `HOLD`; advisory, the decision returns to the developer (Q14) |
| `counts` | object | findings by level: `{ "error": n, "warning": n, "note": n }`; must equal the attached finding set |
| `proof_of_run` | object | `files_read` (int), `commands_run` (list of strings), `checks_passed` (list of strings); a bare verdict with no proof of run is a red flag, not a pass |
| `head` / `base` | string | the reviewed SHA pair, so the record is reproducible |
| `model` | string | the resolved model id actually used (see Pinning) |

## 6. Consumption (D18/Q5)

Findings are VALIDATED before action: the consuming assistant re-verifies each
finding at source before acting on it. Auto-fix defaults ON, is user-configurable,
and caps at 3 tries on the same change; the cap firing raises a LOUD alert and
returns the decision to the developer. A zero-finding SHIP is trusted on its
proof_of_run, exactly like a clean QA delivery.

## 7. Panel composition (D10)

| Trigger | Panel | Rationale |
| --- | --- | --- |
| Per-change (L2/L3 routine) | CROSS-FAMILY ONLY: the other family reviews; the authoring model is not re-run | the delta wanted is the different-family perspective; the author just did the work |
| Promotion (major/minor bump or management-defined event) | FULL PANEL: every supported family INCLUDING the developer's own model | a fresh-context adversarial pass by the own model is distinct from its in-flight self-review; apples-to-apples at the release gate; affordable because promotion is rare |

## 8. Families (D13)

The launch set is Claude + Codex. A family is a named entry in `families.json`
(id, invocation adapter, auth mode) consumed by the brief template's `{family}`
slot and the panel table. Adding a family adds an entry, never a contract change;
the full panel is defined as all SUPPORTED families at run time, so it widens
automatically.

## 9. Model pinning

Reviewer models PIN per AIQT release: each release names the exact model id per
family, bumps are deliberate and tested, and the release record carries the change.
Verdicts compare across time only within a pinned model; the envelope's `model`
field records what actually ran.

## 10. Evidence and retention

Full artifacts, log-aligned: the SARIF-lite report, the rendered brief, and the
verdict envelope persist as workflow artifacts (CI) or run records (local), with
retention matched to the consuming project's AIQT log policy. A PR comment is a
VIEW of the record, never the record.

## 11. Numbering tie-in (D23)

Reviewer findings that mature into guardrails enter the AIQT-/LOCAL- numbering and
provenance-header lifecycle. The contract itself carries no numbering fields.
