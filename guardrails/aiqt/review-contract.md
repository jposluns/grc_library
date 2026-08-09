# AIQT cross-family review contract (v1)

Version: 1.0.1 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 contract; every AIQT adoption level, from copy-in pack use through the
local CLI and the CI-integrated tiers, consumes this document and its paired schemas.
Changes here are breaking for every consumer and follow the AIQT release process.

## 1. Posture

A reviewer REFUTES. It hunts what the author missed, verifies rather than confirms,
and runs read-only against a pinned revision pair. The review is ADVISORY: the
verdict returns to the developer, never a silent block.

## 2. Reviewer runtime (harness and context)

- The reviewer runs as its vendor's FULL coding-agent harness (repository read,
  search, verify at source), never a bare diff-in-prompt call. This matches the
  dogfooded quality bar the contract was proven against.
- Context tier: the DIFF plus on-demand repository access; the harness fetches what
  it needs. No whole-repo upload, no pre-built context pack.
- Read-only is contractual: a reviewer never mutates the repository, its branches,
  or its working tree.

## 3. The refute brief (per-change default, code teams)

The `{family}` and revision slots are filled by the dispatching level (the local
CLI, or the CI integration).

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
| `tool` | string | reviewer id in the `{family}-{change-id}` shape: a lowercase family token, a hyphen, then the change id (pattern-enforced) |
| `ruleId` | string | short kebab-case class label, stable within a review |
| `level` | enum | `error` / `warning` / `note` |
| `location` | string | `path:line`, fresh at the reviewed SHA, never a stale or remembered anchor |
| `fingerprint` | string | `ruleId:path:line`; the ruleId lowercase, the path verbatim as it appears in the diff, the line as digits, no spaces around the colons |
| `evidence` | string | verbatim quote from the reviewed revision |
| `impact` | string | one line (single-line enforced), the concrete consequence |
| `recommendation` | string | one line (single-line enforced), the concrete fix |

A finding failing schema validation is returned to the reviewer for repair, up to
the same 3-try cap that governs auto-fix; exhausting the cap downgrades the finding
to a hypothesis attachment (it never enters the validated set silently).

## 5. Verdict envelope

Normative machine form: `schemas/verdict.schema.json`. Field contract:

| Field | Type | Requirement |
| --- | --- | --- |
| `verdict` | enum | `SHIP` / `HOLD`; advisory, the decision returns to the developer |
| `counts` | object | findings by level: `{ "error": n, "warning": n, "note": n }`; must equal the paired finding set (pairing defined below) |
| `proof_of_run` | object | `files_read` (int), `commands_run` (list of strings), `checks_passed` (list of strings); a bare verdict with no proof of run is a red flag, not a pass |
| `head` / `base` | string | the reviewed SHA pair, 7 to 40 lowercase hex characters, so the record is reproducible |
| `model` | string | the resolved model id actually used (see Pinning) |

A verdict never travels alone: it is PAIRED with its finding set in the same
delivery, as separate documents by design (the schemas deliberately embed neither
in the other, so each stays independently validatable). The counts rule binds the
pair, and a companion validator in the parent GRC Library repository enforces it
mechanically (`tools/validate-review-artifacts.py --kind verdict <envelope>
--findings <set>`; the validator is not part of this pack's file set).

## 6. Consumption

Findings are VALIDATED before action: the consuming assistant re-verifies each
finding at source before acting on it. Auto-fix defaults ON, is user-configurable,
and caps at 3 tries on the same change; the cap firing raises a LOUD alert and
returns the decision to the developer. A zero-finding SHIP is trusted on its
proof_of_run, exactly like a clean QA delivery.

## 7. Panel composition

| Trigger | Panel | Rationale |
| --- | --- | --- |
| Per-change (routine CI review) | CROSS-FAMILY ONLY: the other family reviews; the authoring model is not re-run | the delta wanted is the different-family perspective; the author just did the work |
| Promotion (major/minor bump or management-defined event) | FULL PANEL: every supported family INCLUDING the developer's own model | a fresh-context adversarial pass by the own model is distinct from its in-flight self-review; apples-to-apples at the release gate; affordable because promotion is rare |

## 8. Families

The launch set is Claude + Codex. A family is a named entry in `families.json`
(id, invocation adapter, auth mode) consumed by the brief template's `{family}`
slot and the panel table. Adding a family adds an entry, never a contract change;
the full panel is defined as all SUPPORTED families at run time, so it widens
automatically.

## 9. Model pinning

Reviewer models PIN per AIQT release: each release names the exact model id per
family, and bumps are deliberate and tested. The RELEASE RECORD carries the change:
the pinned model id per family for that release, kept with the release notes (a
release-governance document, forthcoming, formalizes its format). Verdicts compare
across time only within a pinned model; the envelope's `model` field records what
actually ran.

## 10. Evidence and retention

Full artefacts, log-aligned: the SARIF-lite report, the rendered brief, and the
verdict envelope persist as the CI platform's run-attached artefact archives
(GitHub's "workflow artifacts" is one such feature) or as local run records, with
retention matched to the consuming project's
AIQT log policy. A PR comment is a VIEW of the record, never the record.

## 11. Numbering tie-in

Reviewer findings that mature into guardrails enter the AIQT numbering and
provenance-header lifecycle: sequential `AIQT-######` identifiers for vetted
guardrails, `LOCAL-######` for a project's own, each carrying its own version.
The contract itself carries no numbering fields.
