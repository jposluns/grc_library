# Reference-breadth run: RB-7 (aidefensematrix.com-surfaced AI-security frameworks)

**Date:** 2026-07-22 (UTC)\
**Mode:** new-ingest (four frameworks freshly ingested into `grc_library_ref`) + explicit held-item pass (two already-held-but-uncited items RB-7 named)\
**Scope:** the four aidefensematrix.com-surfaced AI-security frameworks the maintainer acquired and the orchestrator ingested, plus the two already-held items RB-7 flagged.\
**`grc_library_ref` at run:** newly-ingested items assessed against `_ref` post-ingest (Wiz discard-candidate later removed in `_ref` #100 `8126580`).\
**License:** CC BY-SA 4.0. Maintainer working state, exempt from corpus audit gates.

## Why this pass ran

RB-7 (maintainer-directed 2026-07-19, from the aidefensematrix.com gap analysis) named four
AI-security frameworks the matrix references that `grc_library_ref` did not hold and the corpus
did not substantively cite, plus two already-held-but-uncited items. The maintainer acquired the
four; the orchestrator ingested them into `grc_library_ref` and assessed where the corpus should
USE / CITE / REFERENCE each. A `--ref-since` new-ingest worklist by construction misses
held-but-uncited items, so the two RB-7-named held items were assessed in a separate explicit
held-item pass (the scoping-gap self-catch logged in the #1063 retro).

## Worklist and judge

Recall-oriented worklist scoped by the RB-7 item list (six named frameworks/sources), judged
against the held source TEXT and the live corpus documents, offloaded to research workers and
re-verified at held source by the orchestrator before every apply (the routine research-assistant
discipline; the #1060 full-column integration additionally ran the high-assurance two-verifier
harness). All held / not-held statuses executed with `ref-holds.py`, not narrated.

## Findings and disposition (finding to PR)

| Source | Held? | Disposition | PR |
|---|---|---|---|
| Google SAIF | cite-without-source (5 corpus cites, source not held) | acquired/ingested; existing SAIF citations substantiated; the "execution" overreach in the two dev-security README SAIF lines corrected (held source has "six core elements", no "execution" lifecycle stage) | #1058 |
| Canada GC/CCCS companions (C-1/C-2) | acquired | GC TBS VM Guideline companion note (`procedure-vulnerability-management.md`); CCCS ITSP.50.103 companion note (`standard-data-classification-and-handling.md`); the reference-audit's fabricated 48h/14d/30d matrix confirmed ABSENT and not applied | #1059 |
| OWASP AI Exchange + SANS Critical AI Security Guidelines | acquired | high-assurance full-column integration across 5 AI docs (matrix columns + framework rows); two independent adversarial verifiers pruned 2 over-assigned cells to N/A, replaced 1 over-generic anchor, dropped 1 redundant bullet | #1060 |
| (LatAm transfer mechanisms, RB-7 L-2/L-3) | held | Brazil Res CD/ANPD 32/2026 into the cross-border register + jurisdiction index; Colombia Decreto 1074/2015 Cap.25 + BCR into the LatAm annex | #1061 |
| (NYDFS financial-services, RB-7 N-1/N-2/N-3) | held | Part 504, 500.19 exemption thresholds, Part 500 annual-filing deadlines, 500.12 universal MFA into the financial-services annex | #1062 |
| NIST IR 8596 (Cyber AI Profile, draft IPRD) | held, draft | DRAFT-WATCH see-also in `register-ai-risk.md` (a draft CSF-2.0 profile, not an asset taxonomy; not the RB-7-named system register) | #1063 |
| OWASP Top 10 for Agentic Applications | held only as an untrusted AIUC-1 crosswalk | NO corpus-body citation; routed to `_private` egress-acquisition for the authoritative source (`register-canonical-citations.md:220` already tracks it by URL, register-only) | egress-gated (TODO RB-7 residual) |
| Cyber Defense Matrix (Sounil Yu) | acquired, organizing/navigational | assessed, no citation (parent organizing framework; no natural corpus home; anti-stuffing) | (none) |
| AI Defense Matrix itself | not acquired (maintainer decision) | a derivative CSF-2.0 by-asset-class mapping; YAML skipped | (none) |

## Residuals (egress-gated, on the `_private` queue)

1. OWASP Top 10 for Agentic Applications, authoritative source (cite the corpus body once ingested).
2. Colombia RNBD (Registro Nacional de Bases de Datos), Decreto 886 de 2014 (WAF-blocked 2026-07-22; assess for the LatAm privacy annex once acquired).

Both are tracked as the TODO RB-7 residual and on the `grc_library_private` maintainer-egress queue.
