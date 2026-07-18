---
name: adopt
description: Run-once onboarding for a fork that adopts this governance-corpus-plus-pack project. A maintainer's clone carries accumulated operational working-state (audit-trail registers, session handoff, a next-actions queue, per-document review anchors) that is meaningless to a fresh adopter; this skill resets that machinery-core working-state to clean adopter baselines, settles how the adopter will handle the absent sibling repositories (their own, or self-contained on the in-repo placeholders), strips maintainer-only operational residue, and records the adopter's choices in a committed adopt-config so the resume step proceeds in adopter-mode without re-asking. It runs ONLY on an adopter clone (a fork origin), never on the maintainer's own repo or a maintainer's fresh-machine clone, and only once (an existing adopt-config short-circuits it).
derives_from: ../../governance/session-lifecycle.md
---

# Adopt (run-once fork onboarding)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Operator classifier: `tools/detect-env.py` (its `probe_identity` block prints an
  `operator_identity` of `maintainer` / `maintainer-fresh-machine` / `adopter`,
  by the git `origin` remote against `jposluns/grc_library` plus sibling presence).
- Adopt-config: `.claude/adopt-config.json` (committed by the adopter; its presence
  marks the fork adopted and is what the resume step reads to skip re-onboarding).
- Sibling placeholders: the in-repo `.ref` / `.scratch` / `.private` stubs that stand
  in for `grc_library_ref` / `grc_library_scratch` / `grc_library_private` when a
  sibling is absent (guarded by the sibling-repo stub-guard gate).
- Machinery-core working-state (the reset target): the gate-read `.working/` files
  that a maintainer's clone fills with operational history, enumerated in step 3.
- Resume wiring: `.claude/commands/resume.md` proposes `/adopt` when the classifier
  says `adopter` and no adopt-config exists; once the config is present, resume
  proceeds in adopter-mode.
- Reference-acquisition manifest + bootstrap planner (sibling model, enrichment): the public
  bibliography `/adopt` can bootstrap an EXTERNAL `.ref` from (`docs/reference-acquisition-manifest.md`),
  and the planner `tools/adopt-bootstrap-ref.py` that categorizes it into auto-fetchable /
  free-manual / licensed-manual (TODO section 1.19.7). Adopters substitute their own equivalents.

An adopting project maps each bullet to its own classifier, config, placeholders,
working-state, and resume flow; the procedure below refers to them generically.

## Overview

The project is designed to be cloned and run by a fork (the corpus, the pack, the full
audit toolchain, and the gates all run sibling-free, the adopter-clone portability
invariant). But a maintainer's clone also carries operational WORKING-STATE that is the
maintainer's, not the adopter's: the audit-trail registers (validation-sweep history,
per-PR validate-pr history, the retrospective log, the credit-offload metrics), the
session handoff and its next-actions queue, the closed-work ledger, the pending-decisions
and verifier-override queues, the deep-assessment register, and the per-document
review-anchor state. Carried into an adopter fork unchanged, that state is at best noise
(a next-actions queue for work the adopter is not doing) and at worst misleading (a
session handoff asserting surfaces clean that the adopter has since changed).

`/adopt` is the run-once onboarding that resolves this. It confirms the clone is genuinely
an adopter fork (not the maintainer's repo, and not a maintainer's fresh-machine clone
that merely has not fetched its siblings yet), settles how the adopter will handle the
absent sibling repositories, resets the machinery-core working-state to clean baselines the
adopter starts fresh from, strips maintainer-only operational content, and records the
adopter's choices in a committed adopt-config. After it runs once, the resume step reads
the config and proceeds in adopter-mode without re-asking.

It is deliberately conservative: it runs only on a confirmed adopter clone, only once, and
it resets working-state to EMPTY baselines rather than fabricating adopter history. It
seeds nothing else in the first cut (no starter backlog, no example sweeps); the adopter
builds their own history from a clean slate. It never deletes the corpus, the pack, the
tooling, or the gates, which are the product the adopter came for.

## When to Use

- On the FIRST resume of a freshly-cloned adopter fork, when the operator classifier
  reports `adopter` and no adopt-config exists (the resume step proposes it).
- Ad-hoc, when an adopter wants to re-baseline their working-state (with the maintainer's
  or their own governance authority's awareness, since it clears working history).

Do NOT use it on the maintainer's own repo, on a maintainer's fresh-machine clone (the
fix there is to clone the siblings, not to reset working-state), or a second time on an
already-adopted fork (the existing adopt-config short-circuits it).

Execute the onboarding per the seven-step process:

### 1. Confirm this is an adopter clone, and that adoption has not already run

Run the operator classifier (`tools/detect-env.py`) and read its `operator_identity`.
Proceed ONLY if it is `adopter`. If it is `maintainer`, STOP (this is the maintainer's
repo). If it is `maintainer-fresh-machine`, STOP and advise cloning the sibling
repositories instead (a fresh maintainer clone is not an adopter; resetting its
working-state would destroy the maintainer's audit trail). If an adopt-config already
exists, STOP (the fork is already adopted; re-baselining is the ad-hoc case above and
needs explicit confirmation). A misclassification in the dangerous direction (a maintainer
treated as adopter) is foreclosed by the classifier's host-pinned origin match, but confirm
the classification with the operator before any reset.

### 2. Choose the sibling model

Ask the adopter how they will handle the three sibling repositories, and record the choice:

- **Own siblings**: the adopter maintains their own reference base, worker-exchange, and
  private-operational repositories beside the clone. `/adopt` points the resolver at them
  (or leaves them to be cloned); the in-repo placeholders remain as the sibling-free
  fallback.
- **Self-contained**: the adopter runs on the clone alone, relying on the in-repo
  placeholders and (for the reference base) the reference-acquisition manifest. Advisory
  tools that reach a sibling degrade to a clean no-op; the corpus and gates run green
  regardless.

This is an authorial decision for the adopter; surface both options with their consequences
and do not pick silently.

### 3. Reset the machinery-core working-state to clean adopter baselines

For each machinery-core working-state surface, clear the maintainer's accumulated content
to an empty or stub baseline the adopter starts fresh from, preserving each file's required
SHAPE (headers, metadata blocks, table headers, and the lifecycle fields the gates
validate) while emptying its DATA rows. Seed nothing else in the first cut. The surfaces:
the session-concurrency lease and the session handoff (reset to a clean stub with a
released lease and an empty queue); the audit-trail registers (validation-sweep history,
per-PR validate-pr history, the retrospective log, the credit-offload metrics, the
reference-audit history and per-document state) reset to their header plus an empty table;
the closed-work ledger and the next-actions projection emptied; the pending-decisions and
verifier-override queues emptied to their `Status: empty` form; the overnight-work file
reset to its stub; the deep-assessment register emptied; and the detailed CHANGELOG mirror
reset to an empty current-week. Do NOT reset the corpus, the pack, the tooling, the gates,
the root CHANGELOG, or the version surfaces (the adopter inherits the version lineage).
Clearing the pending-decisions and verifier-override queues and the deep-assessment register
is a SANCTIONED exception to the pack's never-silently-drop-a-pending-item invariants, scoped
to a confirmed adopter clone (the queued items are the maintainer's, meaningless to the
adopter) and confirmed with the operator in step 1; it is not a breach of those invariants.
Read each surface before clearing it and preserve the shape its consumer requires, but note
the verification asymmetry: for the GATED surfaces (the session lease, gate 63; the
validate-pr history, gate 50) the step-7 green sweep confirms the shape, while the MAJORITY
are gate-exempt `.working/` files no gate reads, so their shape preservation is
convention-verified only and the adopter's first `/resume` is the real check. Preserve each
exempt surface's parseable shape deliberately rather than relying on the sweep to catch a
malformed one.

### 4. Handle the sibling placeholders per the chosen model

Apply the step-2 choice. For **own siblings**, record the adopter's sibling locations so the
resolver and the resume step find them, and (for the reference base) optionally bootstrap the
adopter's EXTERNAL `grc_library_ref` sibling from the reference-acquisition manifest. The
bootstrap planner `tools/adopt-bootstrap-ref.py` (portable procedure; adopters run their own
equivalent) reads the committed public manifest and emits a categorized acquisition plan
(`--json` for the assistant to drive): **auto-fetchable** (FREE and an upstream URL is
recorded), **free-manual** (FREE but no URL recorded yet), and **licensed-manual** (LICENSED).
Drive the bootstrap from that plan: WebFetch each **auto-fetchable** source INTO the adopter's
EXTERNAL `grc_library_ref` sibling, and list the **free-manual** + **licensed-manual** entries
for the adopter to acquire by hand (freely, or lawfully under the issuer's licence). The
planner itself NEVER fetches, downloads, or writes: it reads only the manifest's bibliographic
metadata, so the network + write side stays in the assistant layer where the human is in the
loop, and the copyright boundary is explicit (only FREE sources are auto-fetched; LICENSED
items are never redistributed). For
**self-contained**, keep the in-repo placeholders as-is; the reference-acquisition manifest
(and the same planner) serves as a bibliography the adopter can use to build an external
reference base later
(converting to the own-siblings model). In BOTH models the fetched reference text goes into
an EXTERNAL sibling, NEVER into the in-repo `.ref` stub: the in-repo
`.ref` / `.scratch` / `.private` always stay stub-only, so the stub-guard gate passes (a
fetch into the in-repo `.ref` would hard-fail that gate and break step 7's green sweep).

### 5. Strip maintainer-only machinery

Remove or neutralize any residual maintainer-only operational content that should not carry
into an adopter fork: pointers to the maintainer's private-operational repository, the
maintainer's personal contact and watermark tokens, and any maintainer-specific runbook
references that the corpus and gates do not depend on. Do not touch the governance pack, the
gates, or the corpus; this step is scoped to operational residue, not product.

### 6. Record the adopt-config

Write and commit the adopt-config (`.claude/adopt-config.json`) recording the adopter's
choices, so the resume step proceeds in adopter-mode without re-asking. The minimal schema:
`mode` (`"adopter"`), `adopted_at` (the UTC date), `sibling_choice`
(`"own-siblings"` | `"self-contained"`), and `adopt_config_version` (an integer, `1`). The
committed config is the durable marker that this fork is adopted; its presence is what
step 1 and the resume step read to skip re-onboarding.

### 7. Verify and report

Confirm the reset clone still passes the full audit sweep (it must, sibling-free, per the
adopter-clone portability invariant), confirm the resume step now reports adopter-mode and
does not re-propose `/adopt`, and report to the adopter what was reset, the sibling model
recorded, and the location of the committed adopt-config. If any gate fails after the reset,
a GATED working-state surface was cleared past the shape its gate requires; restore that
surface's required shape (header, metadata, lifecycle fields) and re-run before declaring the
onboarding complete. The green sweep confirms only the gated surfaces; for the gate-exempt
`.working/` majority the sweep is silent, so also parse-check the reset gate-exempt surfaces
(or confirm the adopter's first `/resume` reads them cleanly), since a malformed one would
otherwise surface only on that first resume, past this verification.

The onboarding terminates when the working-state is reset to clean baselines, the sibling
model is settled and recorded, the adopt-config is committed, and the sweep is green; it is
a single run-once pass, not a cadence and not a fix-to-fixed-point loop.

## Prohibited anti-patterns

- **Running on a non-adopter clone.** Resetting a maintainer's (or a maintainer
  fresh-machine's) working-state destroys the audit trail; step 1's classification gate
  exists to prevent it, and a classification is confirmed with the operator, never assumed.
- **Fabricating adopter history.** The reset produces EMPTY baselines, not invented sweeps,
  retros, or backlog; a clean slate is honest, a fabricated history is not.
- **Clearing a working-state surface past its required shape.** A gate validates each
  surface's shape (headers, metadata, lifecycle fields); emptying the DATA is correct,
  destroying the SHAPE breaks the gate. Read before clearing.
- **Deleting product.** The corpus, the pack, the tooling, the gates, and the version
  lineage are what the adopter adopted; `/adopt` never touches them.
- **Silently picking the sibling model.** It is the adopter's authorial choice; surface
  both options with consequences.
- **Re-running on an already-adopted fork without confirmation.** The committed adopt-config
  short-circuits `/adopt`; a re-baseline clears working history and needs explicit
  governance-authority confirmation.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Clean-baseline onboarding of a forked control set | PO.1, PO.5 | GRC-01, CCC-01 | A.5.1, A.5.4 |
| Authorial choices recorded before action | PO.5 | GRC-04 | A.5.4 |
| Audit-trail integrity (no fabricated history) | PS.1, RV.1 | LOG-02, GRC-05 | A.8.15, A.5.36 |
| Scope-bounded reset (product preserved) | PO.5 | CCC-02, CCC-03 | A.5.4, A.8.32 |

The skill expresses the same audit-trail-integrity principle as the rest of the pack, at the
fork-onboarding boundary: an adopter starts from an honest clean baseline with its choices
recorded, never from the maintainer's working-state carried in unchanged or from a fabricated
history.
