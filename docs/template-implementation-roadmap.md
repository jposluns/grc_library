# Adopter Implementation Roadmap Template

**Document Title:** Adopter Implementation Roadmap Template\
**Document Type:** Template\
**Version:** 1.0.7\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/template-quickstart.md`](template-quickstart.md), [`docs/template-startup-roadmap.md`](template-startup-roadmap.md), [`docs/template-maturity-self-assessment.md`](template-maturity-self-assessment.md), [`docs/adopter-guide.md`](adopter-guide.md), [`docs/decision-tree.md`](decision-tree.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Adopter Experience\
**Review Frequency:** Annual, and on material change to the startup-roadmap-template module catalogue\
**Repository Path:** [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template helps an adopter sequence the modules selected via [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) into 90-day, 180-day, and one-year phases. The roadmap is composition-aware: it does not assume a fixed adopter profile, it works from the modules the adopter actually picked.

### Where this fits among the adopter entry points

The canonical front door for adopters is [`docs/portal.md`](portal.md) (audience-keyed grouping by role). This roadmap template is one of five deeper-dive paths that branch off the portal; it answers "over what calendar should I roll the programme out?". The other four are [`docs/adopter-guide.md`](adopter-guide.md) (fork-and-adapt principles), [`docs/template-quickstart.md`](template-quickstart.md) (what to copy on Day 1), [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) (the long-form module-composition workbook), and [`docs/decision-tree.md`](decision-tree.md) (sequenced reading order). The portal's "Other entry points and when to use them" table picks the right path by question; see the portal Overview.

Each phase has a primary goal, a defendable end-state, and concrete acceptance criteria. The aim is not to copy artefacts faster but to reach a defensible posture against the organization's actual exposure within bounded calendar time.

A roadmap is a forecast, not a contract. Real adoptions slip; the value of the template is the sequence and the milestones, not the precise dates.

---

## Scope

This template applies to:

- An adopter starting from scratch (no prior library adoption) and planning a first-year rollout.
- An adopter consolidating an existing partial adoption against the library's structure.
- An adopter preparing a board, audit committee, or regulator-facing communication about the adoption plan.

It does not apply to programmes that are already past Year 1 and operating in steady state; those programmes use the maturity self-assessment template to drive ongoing investment.

---

## How to use this template

1. **Complete the startup-roadmap composition first.** Run through [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) and identify the core baseline plus the activity / data / audience / regulatory modules and the GRC-capacity tier that apply. The roadmap below sequences those modules; it cannot tell you which to pick.
2. **Choose the calendar pace** matching the capacity tier:
   - **E1 (founder part-time)**: extended pace (Phase 1 lasts 6 months, Phase 2 lasts 6 months, full Year 1 is the steady state).
   - **E2 (light, 1 to 2 people)**: standard pace (90 / 180 / 365).
   - **E3 (standard, 3 to 10 people)**: accelerated pace (60 / 120 / 365).
   - **E4 (department)**: parallel pace (Phase 1 and Phase 2 overlap; 60 / 90 / 270).
3. **Walk through the phase sections** below, mapping each phase's activity to the modules you picked.
4. **Record the milestones** in the recording-template section at the end.
5. **Review against the maturity self-assessment** at the end of each phase; the assessment is the source of truth for "are we done with this phase".

---

## Phase 1: Floor (Days 1 to 90 at E2 pace)

### Primary goal

Reach the core-baseline defensible posture. The organization can answer the most-likely first-contact questions (an incident, an audit, a customer security questionnaire, a regulator notification) from documented artefacts rather than from individual recall.

### Defendable end-state at Phase 1 close

| Question a stakeholder might ask | Is there a documented answer? |
| --- | --- |
| Where is our information-security policy? | Yes; copied, customized, signed off. |
| Who owns our access controls? | Yes; named in the artefact's metadata. |
| What do we do when an incident happens? | Yes; the procedure is copied and at desk-check level tested. |
| What personal data do we hold and how do we handle it? | Yes; privacy policy customized; record of processing populated; home-jurisdiction annex adopted. |
| What are our top operational risks? | Yes; risk register populated with the actual top 10. |

### Activities (in sequence)

1. **Days 1 to 14: copy and orient.** Clone the library or fork the relevant subset. Read [`docs/adopter-guide.md`](adopter-guide.md). Run the quickstart-template composition to identify the modules. Identify the named owners for the core baseline artefacts.
2. **Days 14 to 45: customize the core baseline.** Adapt the six core-baseline artefacts to the organization. Replace placeholders; update role names; verify the home-jurisdiction privacy annex; populate the risk register with real risks (not aspirational ones).
3. **Days 45 to 60: customize high-priority Dimension A and B modules.** A1 if there is custom development. B1 if there is customer data. The most-likely modules at this stage map to incidents the organization actually faces.
4. **Days 60 to 80: name owners and approving authorities.** Every adopted artefact carries an owner and an approving authority in its metadata block. Day 60 is when this becomes load-bearing; Phase 1 cannot close without it.
5. **Days 80 to 90: desk-check the incident-response procedure.** A short tabletop with the named owners; document the result.

### Acceptance criteria

- All six core-baseline artefacts are customized, signed off, and have a named owner in the metadata.
- The high-priority A and B modules are also customized and have owners.
- An initial maturity-self-assessment is recorded; expectation is most domains at Tier 1 to 2.
- The incident-response procedure has been desk-check tested at least once.

### Acceptance signals (anti-signals to watch)

- "We will customize it later" against any baseline artefact. Phase 1 cannot close on this.
- "We will populate the risk register when we have time." The register is part of the baseline. Populate it.
- Adopted artefacts where the owner is "TBD" or "the leadership team". An artefact without a single named owner has no owner.

---

## Phase 2: Operational (Days 91 to 180 at E2 pace)

### Primary goal

Operationalize the artefacts adopted in Phase 1. The artefacts exist; in Phase 2 they are used. Reviews happen on schedule. Findings get tracked. Activity creates artefact updates.

### Defendable end-state at Phase 2 close

| Question a stakeholder might ask | Is there a documented answer? |
| --- | --- |
| When was your information-security policy last reviewed? | Yes; the review record is captured per the template, with a date. |
| Have you tested your incident-response procedure? | Yes; a tabletop result is documented, including lessons learned. |
| What is the current top risk and what are you doing about it? | Yes; the risk register has been refreshed at least once since Phase 1 close; treatment plans exist for the top 5. |
| Are your access controls reviewed? | Yes; at least one access-review cycle has happened. |
| Do you have a vendor inventory? | Yes; B-Dimension and C-Dimension modules driving this are operational. |

### Activities (in sequence)

1. **Days 91 to 105: stand up the review cadence.** Copy [`governance/template-document-review-record.md`](../governance/template-document-review-record.md) or equivalent. Schedule the first review wave for the artefacts adopted in Phase 1; aim to complete the first wave within the phase.
2. **Days 105 to 135: layer the Phase 1 modules at depth.** Customize the artefacts in the chosen modules that were deprioritized in Phase 1. Specifically: framework documents (where the GRC capacity tier supports them), the procedures behind the policies, and the registers behind the procedures.
3. **Days 135 to 150: add the Dimension C, D modules.** Audience-shaped artefacts (B2B vendor questionnaires, B2C breach-notification flows) and sector-overlay content (compliance folders).
4. **Days 150 to 165: run the first incident-response tabletop end-to-end.** Not a desk-check; a full scenario walk with the responding roles in attendance.
5. **Days 165 to 180: refresh the maturity self-assessment.** Compare scores to the Phase 1 baseline; document the trajectory.

### Acceptance criteria

- A documented review-cadence schedule covers every adopted artefact.
- At least one review wave has been completed; findings are tracked.
- The Phase 2 maturity self-assessment shows movement from the Phase 1 baseline (median domain score moved up by at least one tier, or specific domains explicitly held at Phase 1 levels with rationale).
- The incident-response tabletop produced an artefact-update list, and the updates are scheduled.

### Acceptance signals (anti-signals to watch)

- Documents adopted in Phase 1 with zero review-record entries by Phase 2 close. The artefacts are not operational; they are decorative.
- A maturity score that did not change from Phase 1. Either the assessment was too lenient at Phase 1, or Phase 2 was not effective.
- The same incident-response findings recurring across multiple tabletops. The findings are not being acted on; either fix that or formally accept the residual risk.

---

## Phase 3: Year-1 close (Days 181 to 365 at E2 pace)

### Primary goal

Reach a steady-state programme. By Phase 3 close, the programme runs on its own cadence; the adoption phase has ended. The organization can produce a Year-1 retrospective grounded in operational data, not anecdote.

### Defendable end-state at Phase 3 close

| Question a stakeholder might ask | Is there a documented answer? |
| --- | --- |
| What did the programme produce in Year 1? | Yes; a Year-1 report covers review completion, finding closure, control test results, and maturity progression. |
| What are the Year-2 priorities? | Yes; informed by the Year-1 self-assessment and by gaps the operational data surfaced. |
| Where is the programme weakest? | Yes; the self-assessment identifies low-Tier domains and the rationale for not yet investing there. |
| Are there programme-improvement actions in flight? | Yes; the continuous-improvement register or equivalent is populated. |

### Activities (in sequence)

1. **Days 181 to 230: deepen the modules that surfaced gaps in Phase 2.** The maturity self-assessment from Phase 2 close identifies specific domains where the median score is low. Target Phase 3 work at those domains, not at adding new modules.
2. **Days 230 to 270: introduce the first measurement layer.** A small set (fewer than 10) of programme metrics: review-completion rate, finding-closure time, control-test pass rate, top-risk treatment-plan status. The capacity tier determines how rich the measurement infrastructure is; E2 capacity ships with a quarterly dashboard updated by hand; E3 to E4 can automate. Refer to the maturity self-assessment Tier 4 guidance for the criteria a measurement layer should meet.
3. **Days 270 to 330: run the first programme-level review.** Convene the governance forum with the metrics, the maturity-assessment trajectory, and the artefact-update backlog. Make Year-2 prioritization decisions in the review.
4. **Days 330 to 365: publish the Year-1 retrospective and the Year-2 plan.** A short document summarizing what shipped, what slipped, what the programme learned, and where the next year's investment goes.

### Acceptance criteria

- A Year-1 report exists and is signed off by the governance authority.
- A Year-2 plan exists and is sequenced (which modules deepen, which are added, which are deprioritized).
- The maturity self-assessment trajectory is documented across Phase 1, 2, and 3.
- At least one programme-level review has happened with the operational data as its primary input.

### Acceptance signals (anti-signals to watch)

- The Year-1 retrospective relies on individual recall. The programme has not produced operational data; Phase 2's measurement layer never came online.
- The Year-2 plan duplicates the Year-1 plan with later dates. Year 1 did not surface enough learning to change the plan; either the assessment was too lenient or the work did not happen.
- Maturity scores at Phase 3 close are unchanged from Phase 1. The programme has been static; either retire the programme or fundamentally re-scope it.

---

## Capacity-tier pace adjustments

The phase sequence above is presented at the **E2** (light, 1 to 2 people) pace as the default reference. Other capacity tiers adjust the calendar:

### E1 Pace (founder part-time)

- Phase 1: 6 months instead of 3.
- Phase 2: 6 months instead of 3.
- Phase 3: not a distinct phase; the programme stays at Phase 2 maturity through Year 1 and ratchets to Phase 3 in Year 2.
- Acceptance criteria are unchanged; only the calendar is.

### E2 Pace (light)

- The reference pace. 90 / 180 / 365.

### E3 Pace (standard, 3 to 10 people)

- Phase 1: 60 days instead of 90.
- Phase 2: 120 days instead of 180.
- Phase 3: same Year-1 close at 365 days.
- The accelerated pace assumes per-domain owners are in place from Day 1.

### E4 Pace (department)

- Phase 1 and Phase 2 overlap; from Day 30 onwards the team is doing both customization and operational running in parallel.
- Phase 1 close at Day 60; Phase 2 close at Day 90; steady-state from Day 270; Year-1 retrospective at Day 365.
- The parallel pace assumes the department is fully staffed from Day 1.

### Pace adjustment for composition complexity

The pace adjusts further based on how many modules the composition includes:

- **Few modules** (~10 or fewer): the reference pace works.
- **Many modules** (~15 or more): add 30 days to each phase regardless of capacity tier.
- **Modules with subject-matter complexity** (heavy regulatory exposure D3 to D4, AI development A4, government data B6): add 30 to 60 days to Phase 2 for subject-matter validation.

---

## Recording template

Below is a template for recording the roadmap. Replace the placeholders.

```
Adopter: <organization>
Plan date: <YYYY-MM-DD>
Composition: <core baseline + A1, A3, B1, B4, D1, E2> (example)
Capacity tier: <E1/E2/E3/E4>
Calendar pace: <chosen pace>

Phase 1 milestone dates:
- Phase 1 start: <YYYY-MM-DD>
- Customization complete: <YYYY-MM-DD>
- Owner assignment complete: <YYYY-MM-DD>
- Incident-response desk-check: <YYYY-MM-DD>
- Phase 1 close (maturity assessment 1): <YYYY-MM-DD>

Phase 2 milestone dates:
- Phase 2 start: <YYYY-MM-DD>
- Review cadence operational: <YYYY-MM-DD>
- Module depth-second-pass complete: <YYYY-MM-DD>
- Incident-response tabletop: <YYYY-MM-DD>
- Phase 2 close (maturity assessment 2): <YYYY-MM-DD>

Phase 3 milestone dates:
- Phase 3 start: <YYYY-MM-DD>
- Measurement layer online: <YYYY-MM-DD>
- Programme-level review: <YYYY-MM-DD>
- Year-1 retrospective published: <YYYY-MM-DD>
- Year-2 plan signed off: <YYYY-MM-DD>

Risks to the plan:
- <named risk>: <owner, mitigation>
- ...

Slippage log (updated as Phase 1 / 2 / 3 close):
- <milestone> slipped <N> days; reason: <text>
```

A complete roadmap document is short. Long roadmaps are a Phase 1 anti-signal; the value is in the milestone and acceptance-criteria discipline, not the prose.

---

## Review questions

When planning a roadmap, answer the following before committing to dates:

1. Have we completed the quickstart composition first? The roadmap sequences modules; if the modules are not identified, the roadmap cannot be sequenced.
2. Have we matched the calendar pace to our GRC capacity tier? E1 organizations using the E3 pace will fail Phase 1.
3. Have we adjusted the pace for composition complexity? Heavy regulatory exposure or many modules need more calendar time.
4. Have we identified the named owners for the Phase 1 work? Phase 1 does not close without owners.
5. Have we agreed which Phase 2 module-depth-second-pass items are in scope? Adding modules in Phase 2 is fine; doing so without a deliberate decision is not.
6. Have we scheduled the maturity self-assessments (one per phase)? Without the assessments, the programme cannot tell whether it is on track.

---

## Maintenance

This template is updated when:

- The quickstart template's module catalogue changes (the roadmap sequences the modules; if the catalogue changes, the roadmap may need adjustment).
- The maturity self-assessment template's tier definitions change (the roadmap references them).
- Adopter feedback identifies a Phase pattern that consistently underestimates or overestimates calendar time.

Major version bumps to this template are warranted when the three-phase structure itself is replaced (e.g. a four-phase or two-phase alternative is adopted as default). Minor bumps cover pace-adjustment refinements, acceptance-criteria additions, and worked-example updates.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
