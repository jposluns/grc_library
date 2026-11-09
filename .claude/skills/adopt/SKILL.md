---
name: adopt
description: Run-once onboarding for a fork of a project that ships this governance tooling. A maintainer's clone carries accumulated operational working-state that is meaningless to a fresh adopter; this skill either resets present working-state to clean adopter baselines or, when the configured working-state location is absent, treats it as already clean and creates only the adopter-local state a public versioned consumer requires, settles how the adopter will handle the project's optional external dependencies (their own, or self-contained with in-repo stubs /adopt creates or functional in-repo substitutes), strips maintainer-only operational residue, and records the adopter's choices in the project's committed adoption marker so later resumptions proceed in adopter mode without re-asking. It runs ONLY on a confirmed adopter fork (a fork origin), never on the upstream maintainer repository, and only once (an existing adoption marker short-circuits it).
---

# Adopt (run-once fork onboarding)

## Project wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository this skill runs with:

- Adopter-clone preflight: [`adopt-preflight-guard.py`](../corpus-management/tools/adopt-preflight-guard.py), the mechanical pre-flight `/adopt` step 1 invokes; it refuses (non-zero) unless the clone classifies as an adopter fork, so the destructive reset does not proceed on the wrong clone.
- Adoption marker: `.claude/adopt-config.json` (committed by the adopter; its presence marks the fork adopted and is what later resumptions read to skip re-onboarding).
- Optional external dependencies: an external reference base of held source texts and an external private store for operational records; the OPTIONAL in-repo `.ref` / `.scratch` / `.private` stubs that `/adopt` can create stand in for them when absent (not shipped by default; a present stub's shape is guarded by the stub-guard gate, guard-if-present-as-stub).
- Working-state (the reset target): the gate-read `.working/` files a maintainer's clone fills with operational history.
- Reference-acquisition manifest and bootstrap planner (dependency model, enrichment): the public bibliography [`reference-acquisition-manifest.md`](../corpus-management/registers/reference-acquisition-manifest.md) that `/adopt` can bootstrap an EXTERNAL reference base from, and the planner [`adopt-bootstrap-ref.py`](../corpus-management/tools/adopt-bootstrap-ref.py) that categorizes it into auto-fetchable / free-manual / licensed-manual.

An adopting project maps each bullet to its own preflight, marker, placeholders, and working-state; the procedure below refers to them generically.

## Overview

A project that distributes this tooling is designed to be cloned and run by a fork: its governed content, its audit tooling, and its gates all run without the maintainer's optional external dependencies (the adopter-clone portability invariant). But a maintainer's clone also carries operational WORKING-STATE that is the maintainer's, not the adopter's: audit-trail records, queues of planned work, and per-document review state. Carried into an adopter fork unchanged, that state is at best noise and at worst misleading (a record asserting surfaces clean that the adopter has since changed).

`/adopt` is the run-once onboarding that resolves this. It confirms the clone is genuinely an adopter fork (not the upstream maintainer's own repository), settles how the adopter will handle the optional external dependencies (an external reference base of held source texts, and an external private store for the adopter's own operational records), resets any present working-state to clean baselines the adopter starts fresh from, strips maintainer-only operational content, and records the adopter's choices in the committed adoption marker. After it runs once, the project's resume mechanism reads that marker and proceeds in adopter mode without re-asking.

It is deliberately conservative: it runs only on a confirmed adopter clone, only once, and it resets working-state to EMPTY baselines rather than fabricating adopter history. It seeds nothing else in the first cut (no starter backlog, no example records); the adopter builds their own history from a clean slate. It never deletes the governed project content, the tooling, or the gates, which are the product the adopter came for.

## When to Use

- On the FIRST working session of a freshly-cloned adopter fork, when the preflight classifies the clone as an adopter fork and no adoption marker exists.
- Ad-hoc, when an adopter wants to re-baseline their working-state (with their own governance authority's awareness, since it clears working history).

Do NOT use it on the upstream maintainer's own repository (the preflight refuses), or a second time on an already-adopted fork (the existing adoption marker short-circuits it).

Execute the onboarding per the seven-step process:

### 1. Confirm this is an adopter clone, and that adoption has not already run

Run the adopter-clone preflight named in the project wiring. Proceed ONLY when it confirms an adopter fork; on any other outcome (the upstream maintainer repository, an undetermined identity, or a probe failure) it refuses and `/adopt` STOPS, because the safe default for a destructive reset is to not run. If an adoption marker already exists, STOP (the fork is already adopted; re-baselining is the ad-hoc case above and needs explicit confirmation). Confirm the classification with the operator before any reset.

### 2. Choose the dependency model

Ask the adopter how they will handle each optional external dependency named in the project wiring, and record the choice:

- **External dependencies**: the adopter supplies its own external resources (a reference base of held source texts, a private store for operational records) and records their locations for the project's tooling.
- **Self-contained**: the adopter uses project-supported in-repository substitutes, placeholders, or clean no-op degradation for the optional resources it does not supply.

The dependency model is an authorial decision for the adopter; surface the supported options with their consequences and do not pick silently.

### 3. Reset the working-state to clean adopter baselines

First determine whether the configured working-state location is PRESENT. A fresh public clone may find it ABSENT (in this repository, `.working/` ships only placeholder backlog and change-record files, and the maintainer's operational records live outside the public tree). If it is ABSENT, treat working-state as ALREADY CLEAN. There is no maintainer history to read, clear, preserve, or reconstruct, and you do NOT recreate an absent working-state tree to reproduce a former inventory. Create only the adopter-local working-state your chosen dependency model (step 2) actually needs, deriving each file's SHAPE from the public versioned consumer (a gate, a tool, or a slash command) that reads it, never from a deleted file; if no public schema or template backs a former historical surface, create nothing and invent no history. Then continue to step 4. The rest of this step applies only when working-state is PRESENT.

For each working-state surface, clear the accumulated content to an empty or stub baseline the adopter starts fresh from, preserving each file's required SHAPE (headers, metadata blocks, table headers, and the lifecycle fields the gates validate) while emptying its DATA rows. Seed nothing else in the first cut. Enumerate the surfaces from the project's own configuration before clearing any of them. Do NOT reset the governed project content, the tooling, the gates, the primary change record, or the version surfaces (the adopter inherits the version lineage).

Read each surface before clearing it and preserve the shape its consumer requires, but note the verification asymmetry: for the GATED surfaces the step-7 sweep confirms the shape, while the surfaces no gate reads are convention-verified only, so the adopter's first working session is the real check. Preserve each gate-exempt surface's parseable shape deliberately rather than relying on the sweep to catch a malformed one, and never treat a gate as validation of a surface outside that gate's scope.

### 4. Handle the placeholders per the chosen model

Apply the step-2 choice. For **external dependencies**, record the adopter's configured locations so the project's tooling finds them, and (for a reference base) optionally bootstrap the adopter's EXTERNAL reference base from the acquisition manifest and bootstrap planner named in the project wiring. The planner reads the committed public manifest and emits a categorized acquisition plan (machine-readable, for the assistant to drive): **auto-fetchable** (freely redistributable and an upstream URL is recorded), **free-manual** (freely available but no URL recorded yet), and **licensed-manual** (licensed). Drive the bootstrap from that plan: fetch each **auto-fetchable** source INTO the adopter's EXTERNAL location, and list the **free-manual** and **licensed-manual** entries for the adopter to acquire by hand (freely, or lawfully under the issuer's licence). The planner itself NEVER fetches, downloads, or writes: it reads only the manifest's bibliographic metadata, so the network and write side stays in the assistant layer where the human is in the loop, and the copyright boundary is explicit (only freely redistributable sources are auto-fetched; licensed items are never redistributed).

For **self-contained**, the in-repo placeholders are NOT shipped, so `/adopt` CREATES the ones the adopter wants: a README-only stub per slot whose first line is the placeholder marker the stub-guard validator parses, which is what keeps the stub payload-free. That marker is a machine-read literal, so write exactly the form the validator parses: `<!-- SIBLING-PLACEHOLDER: <name> -->` as the stub README's first line, with `<name>` the slot token (`ref`, `scratch`, or `private`); the stub-guard gate then holds a declared stub to a README-only, line-capped shape. The acquisition manifest (and the same planner) then serves as a bibliography the adopter can use to build an external reference base later. Fetched content goes into an EXTERNAL location, NEVER into a declared in-repo STUB: a payload-bearing declared stub hard-fails the stub-guard validator and breaks step 7's green sweep. An adopter who instead wants a FUNCTIONAL in-repo substitute materializes a real directory at the slot, which is out of the stub-guard validator's scope (an unmarked, non-stub directory, so different guards or none apply).

### 5. Strip maintainer-only machinery

Remove or neutralize any residual maintainer-only operational content that should not carry into an adopter fork: pointers to maintainer-only stores, personal contact or watermark tokens, and maintainer-specific runbook references that configured product surfaces do not depend on. Do not touch the governance rules, their gates, or governed project content; this step is scoped to operational residue, not product.

### 6. Record the adoption marker

Write and commit the adoption marker named in the project wiring, recording the adopter's choices, so the project's resume mechanism proceeds in adopter mode without re-asking. The minimal schema records the mode, the adoption date in UTC, the step-2 dependency choice, and an integer marker-schema version. Those fields are machine-read, so use the exact names the project's own tooling parses; in this repository the marker is `.claude/adopt-config.json` and the fields are `mode` (`"adopter"`), `adopted_at` (the UTC date), `sibling_choice` (`"own-siblings"` | `"self-contained"`), and `adopt_config_version` (an integer, `1`). The committed marker is the durable signal that this fork is adopted; its presence is what step 1 and the resume mechanism read to skip re-onboarding.

### 7. Verify and report

Confirm that the reset clone passes the project's configured audit sweep with no external dependency present, that its resume mechanism reports adopter mode without re-proposing onboarding, and report what was reset, which dependency model was recorded, and where the adoption marker lives. If a gate fails, restore the affected surface's required shape and re-run it. Because a green sweep confirms only surfaces the configured gates cover, separately parse-check or exercise every reset state surface outside gate coverage before declaring onboarding complete.

The onboarding terminates when the working-state is reset to clean baselines, the dependency model is settled and recorded, the adoption marker is committed, and the sweep is green; it is a single run-once pass, not a cadence and not a fix-to-fixed-point loop.

## Prohibited anti-patterns

- **Running on a non-adopter clone.** Resetting the upstream maintainer's working-state destroys the audit trail; step 1's preflight exists to prevent it, and a classification is confirmed with the operator, never assumed.
- **Fabricating adopter history.** The reset produces EMPTY baselines, not invented records or backlog; a clean slate is honest, a fabricated history is not.
- **Clearing a working-state surface past its required shape.** A gate validates each gated surface's shape (headers, metadata, lifecycle fields); emptying the DATA is correct, destroying the SHAPE breaks the gate. Read before clearing.
- **Deleting product.** Governed project content, tooling, gates, and version lineage are product surfaces; `/adopt` never touches them.
- **Silently picking the dependency model.** It is the adopter's authorial choice; surface both options with consequences.
- **Re-running on an already-adopted fork without confirmation.** The committed adoption marker short-circuits `/adopt`; a re-baseline clears working history and needs explicit governance-authority confirmation.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Clean-baseline onboarding of a forked control set | N/A | GRC-01, CCC-01 | A.5.1, A.5.4 |
| Authorial choices recorded before action | N/A | GRC-04 | A.5.4 |
| Audit-trail integrity (no fabricated history) | N/A | LOG-02, GRC-05 | A.8.15, A.5.36 |
| Scope-bounded reset (product preserved) | N/A | CCC-02, CCC-03 | A.5.4, A.8.32 |

The skill expresses the same audit-trail-integrity principle as the rest of the tooling, at the fork-onboarding boundary: an adopter starts from an honest clean baseline with its choices recorded, never from the maintainer's working-state carried in unchanged or from a fabricated history.
