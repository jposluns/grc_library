# Overnight PR

**Status:** in-flight

## Authorization scope (2026-06-24)

Maintainer authorized an autonomous overnight run of ~8 hours (typed `/resume`, then asleep). **Goal:** close out ALL the XS and S items, and as many of the Medium (M) items as possible, from [`../TODO.md`](../TODO.md), for the maintainer to review in the morning. Standing maintainer-authorized autonomous window; every per-PR discipline (formal `/validate-pr` + `/retro`, post-commit `run_all_audits.sh`, pre-push `run-pr-time-checks.sh`, CI-green-then-merge, always-split) runs unabbreviated.

Directional-choice policy (maintainer asleep):
- (a) If TODO records a maintainer disposition, proceed on it.
- (b) If a NEW directional choice is needed and a wrong guess is bounded to a quick edit: make a documented sensible default, state it in the PR description, add it to the morning-review list below.
- (c) If a wrong guess would be costly/hard to unwind (breaking change, deletion, public-API or precedence decision): defer to morning.
- No fabrication, ever — egress-gated citation items (B2, DD-10) defer rather than invent.

## Session log (PRs shipped)

_(updated as PRs merge)_

- Sweep 36 (`/validate`) — loop-break control for handoff PR #300. 3 subagents dispatched (A/B/C). C clean. A+B+orchestrator apply-time grep found a real in-window finding-class: the #298/#299 CCM/AICM reconciliation claimed "0 residual" but was TOKEN-scoped (gate 48 checks `<DOMAIN>-<NN>` and `| CODE | title |` rows only), so it left **bare CCM domain-code mentions** (IVS, NET, GOV, AUD, EKM) in framework-coverage tables + glossary + a domain-by-domain crosswalk, plus AICM/CCM **version-currency strings** (AICM v1.0.3, CCM v4.0) uncorrected. Orchestrator grep found MORE than the subagents (the EKM crosswalk row, the numbered GOV/AUD COBIT/CCM crosswalk) — the very incomplete-sweep lesson. → PR-A (close-out).
  - Separate finding (different theme): guardrail-review/SKILL.md:93 word-form "forty-seven"→"forty-eight" (gate-39 can't parse word-forms; TODO §4.8 gap). → PR-B.
  - Surfaced for morning (out-of-window, judgment needed): operations/standard-physical-security-of-it-infrastructure.md:108 cites "I&S-03: ... Physical Security" but I&S-03 = "Network Security" (physical security is the DCS domain) — looks like a control mis-citation; correct replacement (DCS-NN?) needs determination. See morning-review list.

### Shipped
- **PR #301** (MERGED) — Sweep 36 close-out: CCM/AICM citation residual completion (13 corpus docs + pack README; IVS→I&S, GOV→GRC, AUD→A&A, EKM→CEK, NET removed, AICM v1.0.3→v1.1). All 48 gates green; `/validate-pr` clean; `/retro` recorded (pattern: unfiltered-grep discipline). Library 2026.06.279, pack 1.49.5.
- **PR #302** (MERGED) — Sweep 36 follow-up: guardrail-review word-form gate count forty-seven→forty-eight; carried batched #301 QA rows. Library 2026.06.280, pack 1.49.6. (`/validate-pr` clean; `/retro`: recurring CHANGELOG em-dash pattern.)
- **PR #303** (MERGED) — Day-1-floor risk-artefact drift, option A: startup-roadmap risk floor artefact aligned to the quickstart/Tier 1 policy. Closed the `(M, XS)` TODO item; partially resolved FR-140. (`/validate-pr` clean; `/retro`: dash-grep applied successfully.)
- **PR #304** (in flight) — R3 relocation: register-main-branch-protection.md → .working/ (PR #116 precedent); carries batched #303 QA rows. Library 2026.06.282. Closes R3; R1 deferred (pack-design), R2 pending (heavy).

### Relocations R1/R2/R3 — sequencing decision (overnight)
- **R3** (`governance/register-main-branch-protection.md` → `.working/`): clean corpus-doc move, NO pack coupling (PR #116 precedent). Proceed overnight.
- **R1** (`tools/sweep-preflight-exemptions.json` → `.working/validate-sweeps/`): functionally safe (scanner opens the path directly, verified), BUT the file is referenced from TWO distributable pack SKILLs (`validation-sweep`, `validation-sweep-pr-scoped`). Pointing pack SKILLs at a `.working/` path is a pack-design call (adopters may delete `.working/`); the "XS" label likely didn't weigh this. See morning-review for the decision needed.
- **R2** (6-file citation cluster → `.working/citation-verifications/`): maintainer already flagged as the heavy/risky one (own PR, extra grep care). Attempt overnight only after R3/R1 resolved; defer if ripple is large.

## Design decisions made

_(accumulates; routed to design-decisions.md in morning processing)_

- **DD-overnight-1 (gate-48 coverage gap)**: gate 48 is token-scoped and structurally cannot catch bare domain-code mentions (`CSA CCM IVS`, framework-coverage family lists, domain-by-domain crosswalk rows). PR-A fixes the content residuals; the durable mechanical fix (extend gate 48 to flag bare known-bad domain codes in CCM/CSA context) is queued as a new TODO item alongside S4. Building it = candidate overnight M item.

## Morning-review list (defaults taken / items deferred / needs maintainer decision)

1. **Probable control mis-citation (out-of-window, surfaced by Sweep 36, NOT fixed):** `operations/standard-physical-security-of-it-infrastructure.md:108` cites "I&S-03: Infrastructure and Virtualization Security: Physical Security", but the catalogue title of I&S-03 is "Network Security", and physical/datacenter security is the CCM `DCS` (Datacenter Security) domain. Looks like the wrong control/domain for a physical-security doc. Correct replacement needs your judgment (a DCS control? drop the number?), so I left it rather than guess. Also: `operations/standard-cloud-security-configuration-baseline.md:195` carries the old "Infrastructure and Virtualization Security" domain *name* alongside correct I&S codes (softer domain-name-currency refresh; could ride the same fix).
2. **R1 relocation needs a pack-design decision (deferred):** moving `tools/sweep-preflight-exemptions.json` → `.working/validate-sweeps/` is functionally safe, but the file is referenced from two *distributable* pack SKILLs (`validation-sweep`, `validation-sweep-pr-scoped`). Options: (a) point the pack SKILLs at the new `.working/` path (consistent with their existing project-path style, but bakes a `.working/` path into the distributable pack, which adopters may delete); (b) genericize the SKILL prose to not hardcode the path; (c) keep the exemption file in `tools/` and close R1 as "won't-move" (the `tools/` location is arguably better for adopters). I deferred rather than guess on distributable pack content. R3 (clean corpus move) and R2 (heavy, your flagged own-PR) are handled separately.

## Open ambiguities / build progress

_(accumulates; pure-noise build-progress discarded in morning processing)_
