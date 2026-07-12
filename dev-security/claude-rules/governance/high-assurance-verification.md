# High-Assurance Verification for Sensitive Changes

Most changes are adequately protected by the routine layers: the research-assistant discipline (workers research, the orchestrator re-reads and authors), the mechanical gates, and the per-change and periodic sweeps. A small subset of changes is not. When a change carries a *correctness* property that no gate can check, is large or delicate enough that a hand-edit is itself a defect risk, and would be costly to get wrong because the artefact is cited or relied on downstream, the routine layers leave a real gap: a wrong value passes every gate, reads as plausible, and ships.

High-assurance verification is the response: a deliberate, heavier pre-apply harness, invoked for the sensitive subset, that layers independent adversarial verification and a deterministic apply on top of the routine research-and-author flow, so apply-correctness does not rest on the orchestrator's in-context precision. It is the *proactive* counterpart to [`trust-recovery-escalation.md`](trust-recovery-escalation.md): trust-recovery is the reactive, post-failure re-examination of a window of work whose process integrity has lapsed; this rule is the before-the-fact assurance that keeps a high-stakes change from becoming such a failure in the first place. It is a heavier tier above the routine [`ai-assistant-workflow-disciplines.md`](ai-assistant-workflow-disciplines.md) research-assistant discipline, not a replacement for it.

The rule applies to any project where an AI assistant ships changes whose correctness a mechanical gate cannot fully verify. The failure mode it prevents is observed directly: a plausible-but-wrong value that survives every existence check because the check confirms the value is *well-formed*, not that it is *right*.

---

## What makes a change sensitive (the trigger)

The harness is not for every change; invoking it everywhere is its own failure (it is expensive, and indiscriminate use erodes the signal that an item is genuinely high-stakes). A change is sensitive, and warrants the harness, when all three conditions hold:

1. **Gate-blind correctness.** A wrong value is a *correctness* defect that no mechanical gate catches. The canonical shape is a *fit* or *semantic* property: an existence gate confirms the value is in the right catalogue and well-formed, but cannot confirm it is the *right* value for its context. (The motivating case: a control code that exists, is in the correct framework, passes the existence gate, and is still the wrong control for the row's document.)
2. **Delicate scale.** The change is large or structurally delicate enough that a hand-edit is itself a meaningful defect risk: a wide reshape of a single artefact, a bulk mapping, a many-row or many-cell edit where a transposition or an off-by-one is easy and not gate-caught.
3. **High escaped-error cost.** The artefact is citable, cross-linked, or relied on downstream, so an escaped error propagates: a corpus document other documents cite, a mapping table consumed by adopters, a normative value reproduced elsewhere.

When all three hold, escalate to the harness. When only one or two hold, the routine layers are the right tool, and the harness is over-engineering. When uncertain, the cheaper move is to apply the harness (a false escalation costs tokens; a false de-escalation ships a defect), but record the judgement so the threshold stays calibrated.

The maintainer may direct the harness for any change regardless of these conditions; the conditions are the assistant's *default* trigger, not a ceiling on the maintainer's discretion.

---

## The harness: five stages

The harness composes five stages. Stages 3 and 5 are what distinguish it from the routine research-and-author flow; the rest are the routine flow done deliberately.

1. **Research fan-out.** Dispatch parallel research workers to produce the candidate values (per the research-assistant discipline). Workers produce research, not final prose; the orchestrator remains the author.

2. **Mechanical signal pass over the candidates, especially the negatives.** Run a deterministic search (a `grep`, a script) over the candidate set to surface anything the research may have under-examined. The highest-value target is the *negatives*: the items a worker marked "no fit" / "N/A" / "no change". A negative reached by inference from a title or adjacent metadata, rather than by opening the source, is the dominant first-pass miss; the signal pass routes every negative that carries a signal of the target attribute to a verifier read. (This is the "open-on-negative-with-signal" discipline: a negative verdict on a candidate bearing a signal of the target attribute must be grounded in opening the source, not inferred.)

3. **Independent adversarial verification.** Dispatch separate verifier workers, blind to each other and to the research workers' reasoning, each with an adversarial brief to *refute*, not to confirm. The two complementary lenses:
   - A **false-negative** verifier: re-read everything marked negative ("N/A" / "no change") and hunt for the ones that should have been positive (the misses).
   - A **false-positive** verifier: judge every assigned value against ground truth (the source title, the canonical definition) and hunt for the ones that are over-assigned or mis-fit.
   The verifiers are independent because a verifier that sees the research worker's rationale inherits its blind spots. Each verdict must quote the ground-truth source. When more than one failure mode is plausible, give each verifier a distinct lens rather than running identical ones; diversity of lens catches what redundancy cannot.

4. **Programmatic invariant check where mechanical truth exists.** For any property a deterministic check *can* verify (an identifier is in the canonical set, a count matches, a flag is set), run that check and require it to pass. This is the existence-gate floor under the semantic verification above it; it does not replace stages 3 or 5.

5. **Deterministic scripted apply, then re-parse.** Do not hand-edit the sensitive artefact. Drive the apply with a dry-run-validated, idempotent-guarded script keyed on an explicit map (source location to verified value), then re-parse the rendered artefact and confirm every applied value matches the verified map. This is the stage that makes apply-correctness *independent of the orchestrator's in-context precision*: a 200-row reshape applied by hand depends on the orchestrator not transposing a single cell across a long edit; the same reshape applied by a re-parsed script does not. The script and its dry-run output are part of the record.

The stages are applied in order, but stage 2's negatives feed stage 3's false-negative verifier, and stage 4's mechanical floor runs before stage 5's apply. A finding at any stage loops back: a stage-3 miss is corrected and re-verified before the apply, not patched in afterward.

**Guard-first sequencing.** When the change has a mechanical gate that *will* exist for it (an existence gate for the value class), land the gate before the data, so the data is validated as it lands rather than retrofitted. The gate is the floor; the harness is the semantic layer above it.

---

## Persistence between sessions

A sensitive change is often not a single session's work: the trigger is recognized in one session, the harness runs across one or more, and the closing verification (or a periodic re-check) falls in a later session. So the harness needs a durable record that survives a session boundary, not only an in-session note.

The mechanism is a persistent register in the consuming project's working state (this rule ships in the pack; the project chooses the register's path). The register records, per sensitive item: the item and why it is sensitive (which of the three conditions), the harness stages run and their outcomes (workers, verifier findings, invariant checks, the apply script and its re-parse result), the status (`pending` / `in-progress` / `verified` / `deferred`), and any follow-up (a closing re-check, a cadence). A `verified` row is the audit trail that the harness ran and what it found; a `pending` or `in-progress` row is a standing instruction to a future session that the item is not yet cleared.

The register is surfaced at session resume, alongside the other standing registers (the pending-decisions queue, the matrix-fit history), so a future session sees the open sensitive items before it starts the queued work and does not lose track of an item mid-harness across a session boundary. An item is removed from the active register (or marked `verified` and retained for the record) only when its harness is complete; the assistant does not silently drop a `pending` item, exactly as it does not drop a pending decision.

This persistence is what makes the harness a *recurring* activity rather than a one-off: the register carries the open items forward, and the resume step re-surfaces them, so the discipline is re-applied as needed across sessions without depending on the assistant's memory of a prior session.

---

## Prohibited anti-patterns

- **Skipping the harness on a sensitive item because the routine layers "probably caught it".** The three conditions define when the routine layers are insufficient; "probably" is the inference the harness exists to replace with verification.
- **Confirming instead of refuting in the verifier stage.** A verifier briefed to confirm finds confirmation; the adversarial brief (hunt the misses, hunt the over-assignments) is what surfaces the defects. A verifier that returns "all correct" without having tried to refute has not run stage 3.
- **Letting a verifier see the research worker's rationale.** Independence is the point; a verifier that inherits the research reasoning inherits its blind spots and rubber-stamps them.
- **Inferring a negative from a title.** A "no fit" / "N/A" verdict on a candidate that carries a signal of the target attribute, reached without opening the source, is the dominant first-pass miss; the signal pass and the false-negative verifier exist to catch it, and skipping them reintroduces it.
- **Hand-editing the sensitive artefact.** A wide hand-edit makes apply-correctness depend on the orchestrator not slipping across a long edit; the deterministic-apply-plus-re-parse stage is what removes that dependency. "I will just edit it carefully" is the failure mode this stage prevents.
- **Declaring the apply correct from the script running, without the re-parse.** The script running is not evidence the rendered artefact matches the verified map; the re-parse is. (This is [`evidence-grounded-completion.md`](evidence-grounded-completion.md) at the apply boundary.)
- **Losing a pending item across a session boundary.** An in-progress harness not recorded in the persistent register is invisible to the next session; the register entry is what carries it forward.
- **Invoking the harness indiscriminately.** Applying it to changes that do not meet the three conditions is expensive and erodes the signal that an item is genuinely sensitive; the trigger is a gate, not a default-on.

---

## Relationship to the rest of the pack

This rule occupies a distinct niche; the delineations are deliberate:

- **[`trust-recovery-escalation.md`](trust-recovery-escalation.md)** is the *reactive* tier: a white-box re-examination of a window of work *after* discipline failures have put the maintainer's confidence in question. This rule is the *proactive* tier: the pre-apply assurance that keeps a high-stakes change from becoming that failure. Both use independent adversarial review; they differ in when they fire (before the change versus after the lapse) and in scope (one sensitive change versus a window of work).
- **[`ai-assistant-workflow-disciplines.md`](ai-assistant-workflow-disciplines.md)** is the routine multi-PR flow (research-assistant, pipeline, apply-time correction). This rule is a heavier tier *above* it for the sensitive subset: it does not relax the routine apply-time verification, it adds independent adversarial verification and a deterministic apply on top.
- **[`evidence-grounded-completion.md`](evidence-grounded-completion.md)** governs every assertion's grounding. This rule's stage 5 re-parse and stage 3 quote-the-source requirements are that rule applied at the apply and verification boundaries of a sensitive change.
- **The mechanical gates** are the existence floor (stage 4). This rule is the semantic layer above them, for the fit/correctness properties the gates by construction cannot check.

The harness's *executable* form (a skill with a slash-command entry point that runs the five stages) is the ergonomic companion to this rule; this rule states the discipline (when and why), and the skill states the procedure (how). Where the skill exists, the rule's stages and the skill's steps are kept in parity.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Independent verification before a high-stakes change | RV.1, RV.2 | GRC-05, A&A-04 | A.5.35, A.5.36 | V1.1, V14.1 |
| Adversarial review proportional to risk | PO.5, RV.1 | GRC-04, GRC-05 | A.5.4, A.5.35 | V1.1 |
| Deterministic, repeatable apply (no ad-hoc hand edit) | PO.5, PW.4 | CCC-01 to 04 | A.8.32 | V14.2 |
| Findings and verifications traceable to a record | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15, A.5.36 | V14.1 |

The rule expresses the same audit-trail-integrity principle as the rest of the pack, applied at the highest-stakes boundary: a sensitive change's correctness must be traceable to an independent verification and a deterministic apply, not to the orchestrator's confidence that it got the edit right.
