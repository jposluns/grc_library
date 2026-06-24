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

## Design decisions made

_(accumulates; routed to design-decisions.md in morning processing)_

- **DD-overnight-1 (gate-48 coverage gap)**: gate 48 is token-scoped and structurally cannot catch bare domain-code mentions (`CSA CCM IVS`, framework-coverage family lists, domain-by-domain crosswalk rows). PR-A fixes the content residuals; the durable mechanical fix (extend gate 48 to flag bare known-bad domain codes in CCM/CSA context) is queued as a new TODO item alongside S4. Building it = candidate overnight M item.

## Morning-review list (defaults taken / items deferred / needs maintainer decision)

_(accumulates)_

## Open ambiguities / build progress

_(accumulates; pure-noise build-progress discarded in morning processing)_
