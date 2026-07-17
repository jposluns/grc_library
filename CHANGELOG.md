# Changelog

All notable changes to this repository are recorded in this file as one compact entry per change: a `date | version | PR` header followed by a short, plain-language summary a general reader can follow. The full maintainer-grade detail for each change (the Added / Changed / Removed / Fixed / Security / Verification sections) is kept in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) and in git history; that mirror is how this project's maintainer tracks the full audit trail. The convention is project-specific; forks may delete `.working/` and adopt their own approach to detailed change tracking. The mechanics are documented in the [`change-tracking` governance rule](dev-security/claude-rules/governance/change-tracking.md).
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

**2026-07-17 | 2026.07.492 | PR #1004** - Website: reduces the hero heading font-size clamp so the long "Learning governance and security" title on the For-AI page no longer overflows the coloured hero band on tablet-width screens; the desktop size cap is unchanged. Batches PR #1003's quality-assurance. Website template only; no corpus content changed.

**2026-07-17 | 2026.07.491 | PR #1003** - Codifies the "sync scratch every PR" discipline (TODO section 3.93 parts a and b) after a repeat stale-scratch-read mistake: adds it to the CLAUDE.md close-out checklist and credit-offload section, and to the /resume step-3 check, so worker/queue/result state is read from a freshly-fetched scratch checkout. Batches PR #1002's quality-assurance. Working-state and AI-guidance only; no corpus or website content changed.

**2026-07-17 | 2026.07.490 | PR #1002** - Adds a "For AI" link to the site-wide footer, next to "About & contributors", so the For-AI page stays reachable even when the long Contents sidebar overflows its viewport and its trailing links fall below the fold. Website template only; no corpus content changed.

**2026-07-17 | 2026.07.489 | PR #1001** - Applies the deep-assessment r4 citation-accuracy fixes (maintainer signed off): corrects a TLS cipher-suite attribution, remaps outdated NIST CSF subcategory codes to the current framework version in the monitoring procedure, fixes an ISO 27002 clause number, and corrects a software-inventory control code. Three standards documents updated; each fix verified against the held source with a skeptical verifier.

**2026-07-17 | 2026.07.488 | PR #1000** - Sweep 111 close-out for the resumed session: the loop-break validation over PRs #992-#998 passed clean (offloaded to a worker, confirmed under elevated review). Acquires the session concurrency lease and adds a backlog item to sync the scratch repo every PR. Working-state only; no corpus or website content changed.

**2026-07-17 | 2026.07.487 | PR #999** - Session-closing handoff for the 2026-07-17 resumed session (PRs #992-#998, the operational-state-privatization Phase-1 execution sprint). Refreshes the session handoff, asserted-expectations, and session-metrics; batches PR #998's quality-assurance; records the guardrail-review follow-ons (TODO section 3.92); and releases the concurrency lease. Working-state only; no corpus or website content changed.

**2026-07-17 | 2026.07.486 | PR #998** - Ships the sixth Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.6: the run-once `/adopt` fork-onboarding skill and slash command. It resets an adopter fork's machinery-core working-state to clean baselines, settles the sibling model, strips maintainer-only residue, and records the choices in a committed adopt-config the resume step reads. Also hardens the detect-env origin matcher, wires the resume adopter-path, and runs the mandated guardrail review (six in-window fixes, three hardenings routed). Batches PR #997's quality-assurance. No corpus or website content changed.

**2026-07-17 | 2026.07.485 | PR #997** - Ships the fifth Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.5: an origin-identity probe in the environment-detection tool. It classifies the operator as maintainer, adopter fork, or maintainer-on-a-fresh-machine by the git origin remote and sibling presence, so the resume step can pick the maintainer or adopter path. Detection only; the adopter onboarding flow is wired in section 1.19.6. Adds six unit tests. Batches PR #996's quality-assurance. No corpus or website content changed.

**2026-07-17 | 2026.07.484 | PR #996** - Ships the fourth Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.2: a shared sibling-repo resolver in the linter-commons module. The three advisory tools that reach a sibling repo today now no-op and exit clean when the sibling is absent, so a fork clone runs them without a spurious error. Scope was corrected at build from the design's six tools to those three. Also extends the portability check to prove it and adds unit tests. Batches PR #995's quality-assurance. No corpus or website content changed.

**2026-07-17 | 2026.07.483 | PR #995** - Ships the third Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.4: a new hard audit gate (gate 70, "Sibling-repo stub-guard audit"). It enforces that each in-repo .ref/.scratch/.private placeholder holds only a marker-stamped, length-capped README, so no reference, worker-exchange, or private-operational content can leak into the public repo through them. Wired across the four gate-parity surfaces plus the audit-programme spec and a regression fixture; the corpus now runs 70 audit gates. Also refreshes a stale exempt-directory docstring and batches PR #994's quality-assurance. No corpus or website content changed.

**2026-07-17 | 2026.07.482 | PR #994** - Ships the second Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.3: three in-repo placeholder directories (.ref, .scratch, .private), each holding only a marker-stamped README stub, added to the shared exempt-directory set. They stand in for the reference, worker-exchange, and private-state sibling repos so a fork that clones only the public repo resolves real-sibling, then placeholder, then a clean no-op. Also records the full locked Phase-1 build design (sections 1.19.2 through 1.19.7) for the remaining PRs. Tooling and working-state; no corpus or website content changed.

**2026-07-17 | 2026.07.481 | PR #993** - Ships the first Phase-1 deliverable of the operational-state-privatization track and closes TODO section 1.19.1: a `tools/check-portability.sh` check that clones the repo with no sibling repos present and confirms all 69 audit gates still pass. This guarantees a fork reaching no sibling repo runs the full toolchain green; verified both directions, including a non-vacuous failure test. Also consumes PR #992's quality-assurance, corrects a session-scoped worker trust-tier mislabel it surfaced, and routes a latent handoff-check gap (TODO section 3.89). Tooling and working-state; no corpus or website content changed.

**2026-07-17 | 2026.07.480 | PR #992** - The Sweep 110 loop-break validation close-out for the session resumed from PR #991: the corpus-wide validation sweep, offloaded to a worker and elevated-QA-consumed, passed with one out-of-window citation finding routed and one in-window changelog mis-quote fixed. Also records the locked design decisions from the operational-state-privatization discussion (the TODO section 1.19 open items and the worker-exchange transport), prunes the session handoff, and acquires the session lease. Working-state only; no corpus or website content changed.

**2026-07-17 | 2026.07.479 | PR #991** - Session-closing handoff for the 2026-07-16c resumed session (PRs #985-#990). Adds a maintainer-co-designed Priority-1 spec (new TODO section 1.19, phased deliverables 1.19.1 through 1.19.13) to privatize the maintainer's operational state and make the public repo robustly clonable by a fork that reaches no sibling repo. The design discussion continues on the next resume. Refreshes the session handoff, asserted-expectations, session-metrics, and credit-offload roll-up, batches PR #990's QA, and releases the concurrency lease. Working-state only; no corpus or website content changed.

**2026-07-17 | 2026.07.478 | PR #990** - Two mistake-prevention fixes for errors flagged this session. A new `ref-holds` forcing-function tool makes held/not-held claims about the reference base come from its index (quoted), not a partial grep. A PreToolUse hook blocks AskUserQuestion in unattended mode, keyed on a new gate-63-validated Operating-mode field in the session lease, so a blocking prompt cannot idle an unattended run. Batches PR #989's QA. Tooling and AI-assistant config; no substantive corpus content changed (only the audit-programme spec's gate-63 documentation).

**2026-07-17 | 2026.07.477 | PR #989** - Adds delta gate D8: a PR whose newly-added root CHANGELOG entry exceeds 100 words or has a sentence over 45 words now fails, so root summaries cannot drift back into long paragraphs (maintainer-directed; the prior length check was advisory-only and unenforced). Also records the deep-assessment r4 continuation (findings routed to TODO section 1.17, holding for sign-off), fixes a stale Priority-3 item-number counter that validate-pr-988 caught, and batches PR #988's QA. Tooling and working-state; no substantive corpus or website content changed (the only corpus edit is the audit-programme spec's D8 gate documentation).

**2026-07-17 | 2026.07.476 | PR #988** - Adds the Canadian TBS Guide on the Use of Agentic AI as a labelled sector-neutral comparator row in the AI access-and-agent-permissions framework table (TODO section 2.22, first bite; standard 0.0.9 to 0.0.10). Records the local-VM worker-exchange transport design (new TODO section 3.87, which supersedes section 3.85) and routes a quality-assurance finding on inconsistent COBIT objective titles to new TODO section 1.16. Batches PR #987's quality-assurance result (ship) and retrospective. One comparator row plus working-state; no other corpus or website content changed.

**2026-07-17 | 2026.07.475 | PR #987** - Delivery-status tooling fix (TODO section 3.61) plus a quality-assurance-surfaced citation fix. The delivery-status reconciliation tool now flags any pending or applied verdict resting only on a recyclable section-number token (no stable coded id) as LOW-CONFIDENCE, so a renumbered section number that now points at a different backlog item (the 2026-07-16 gr-gap and etsi token mis-maps) is surfaced for verification rather than trusted; a coded-id match stays high-confidence (self-test 5 of 5). Also fixes a pre-existing gate-blind COBIT title error that PR #986's quality-assurance pass surfaced (the compliance-controls-and-gap register listed COBIT APO14 as "Managed AI"; the canonical title is "Managed Data"), and batches PR #986's quality-assurance result (ship) and retrospective. Tooling plus one corpus title fix; no other corpus or website content changed.

**2026-07-17 | 2026.07.474 | PR #986** - Consumes the delivered worker quality-assurance passes and fixes the one defect they surfaced. The matrix-fit full pass found a single semantic mis-fit (MF1): the AI Governance Council charter's sole COBIT mapping cited APO14 "Manage Data" for what is a governance/oversight body; corrected to EDM01 "Ensured Governance Framework Setting and Maintenance" (charter 1.2.7 to 1.2.8). The claim-fit Tier-A, Canada matrix-fit, and publications-screening passes were all clean. Batches PR #985's quality-assurance result (ship; one low note routed to new TODO section 3.86) and its retrospective. Working-state plus one corpus control-code fix; no other content changed.

**2026-07-17 | 2026.07.473 | PR #985** - The Sweep 109 validation close-out (the loop-break compensating control for the prior session-closing handoff, PR #984), covering PRs #969 to #984. This sweep was offloaded to a credit-offload worker and consumed under elevated new-worker quality assurance (the mechanical facts were independently re-derived to an exact match, and a dedicated adversarial auditor re-verified every load-bearing California CCPA and Quebec Law 25 citation at the held source and found no missed finding); the loop-break control passes. The worker's sweep found nothing; the elevated-QA auditor surfaced one precision note, verified at source and fixed here: the United States privacy annex's California cybersecurity-audit threshold parenthetical now states both section 7120(b) triggers (a business that derives 50 percent or more of its annual revenue from selling or sharing personal information, and a business with over USD 25 million in annual gross revenue that also processed the personal information of 250,000 or more consumers or households or the sensitive personal information of 50,000 or more consumers), where it previously rendered only the second prong. Also prunes the session handoff to the two most-recent sessions, advances the validation cursor, acquires the concurrency lease for the resumed session, and records the credit-offload metrics row for the offloaded sweep. Two maintainer directives were also codified in the worker-exchange repository (not this repository): workers now verify they can reach the pinned corpus revision when picking up a task, and stagger their check-ins across the live worker fleet.

**2026-07-16 | 2026.07.472 | PR #984** - Session-closing handoff for the 2026-07-16b resumed session (#969-#983). Refreshes the handoff record ([`.working/session-handoff.md`](.working/session-handoff.md)) with new Next-actions, State-snapshot, and Asserted-expectations blocks (the large maintainer-authorized resume queue, the two open item-1 findings, green-at 69439833 = 69/69), adds the [`.working/session-metrics.md`](.working/session-metrics.md) row, batches PR #983's quality-assurance result and retrospective, and RELEASES the concurrency lease ([`.working/session-state.md`](.working/session-state.md)). The session wound down on a maintainer-authorized degradation signal (a false "test-proven" self-verification on a delicate helper fix, disproven by its verifier). Per the loop-break it takes no trailing per-PR validation sweep; the compensating control is the next session's corpus-wide validate (Sweep 109), pre-positioned here as an offloaded worker order. Working-state only; no corpus or website content changed.

**2026-07-16 | 2026.07.471 | PR #983** - Working-state bookkeeping batch for the unattended run. Records the first OFFLOADED deep-assessment (run r4, partial and re-entrant, run by a credit-offload worker) in [`.working/deep-assessment/register.md`](.working/deep-assessment/register.md) with its findings (one Medium, a reference-base validation gate-red already fixed in reference-base pull request #87; one advisory). Adds four consume rows to the credit-offload metrics ledger [`.working/credit-offload-metrics.md`](.working/credit-offload-metrics.md) (the per-session estimate rises to about 1.98 million orchestrator tokens conserved). Batches the previous pull request's quality-assurance result and retrospective. Corrects two earlier-session working records that cited the wrong regulation subsection for the CCPA cybersecurity-audit phasing (it is section 7121, "Timing Requirements", not section 7120 which is the threshold section). Codifies the wind-down pre-positioning of the resume validation sweep in [`.working/credit-offload-design.md`](.working/credit-offload-design.md) and the CLAUDE.md credit-offload section. Queues a complete re-download of one incompletely-captured reference page in [`.working/maintainer-egress-requests.md`](.working/maintainer-egress-requests.md). No corpus or website content changed.

**2026-07-16 | 2026.07.470 | PR #982** - Adds the per-tier measurement years to the California cybersecurity-audit phasing in the United States privacy annex ([`privacy/jurisdictions/annex-privacy-united-states.md`](privacy/jurisdictions/annex-privacy-united-states.md)), a precision tightening for the expert review surfaced by PR #976's validation. The held 11 CCR section 7121 (Timing Requirements) keys the 2029-04-01 first-audit deadline to a business's 2027 annual gross revenue and the 2030-04-01 deadline to its 2028 revenue (the 2028-04-01 tier already carried its 2026 measurement year). The deadlines and dollar bands were already correct, so this changes precision rather than substance; it was re-verified against the current held regulations (effective 2026-01-01). Also batches PR #981's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.469 | PR #981** - Records the repository side of the completed reference-acquisition task (the reference documents themselves were ingested into the private reference base as its own pull requests): adds the three sources that could not be fetched from this environment to the maintainer-egress request queue in [`.working/maintainer-egress-requests.md`](.working/maintainer-egress-requests.md) (a Brazilian data-protection resolution, a New York virtual-currency regulation, and a Colombian data-protection decree, none substituted with an unofficial copy), records the four newly-consumed worker deliveries in the credit-offload metrics ledger [`.working/credit-offload-metrics.md`](.working/credit-offload-metrics.md) (the per-session estimate rises to about 1.51 million orchestrator tokens conserved, from about 1.44 million, because this pull request also consumed the quality-assurance pass on the previous one), and applies that quality-assurance result (one low finding: three working-state surfaces still showed the older 1.37-million estimate, now corrected). Working-state and bookkeeping only; no corpus or website content changed. Also batches PR #980's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.468 | PR #980** - Adds a credit-offload metrics tab (maintainer-requested): a running ledger, [`.working/credit-offload-metrics.md`](.working/credit-offload-metrics.md), of what the offload workers have done and, per session, the estimated orchestrator credits conserved by offloading read-only quality-assurance and research passes to them, plus a short chat tally surfaced at each major activity (a worker delivering, a pull request finishing). The figure is always labelled an estimate (workers cannot read an exact token count) and carries the standing caveat that credit-offload shifts cost across accounts rather than reducing total spend. Backfilled for this session (about 1.44 million estimated orchestrator tokens conserved across the passes consumed so far). Codified in the credit-offload design of record and a CLAUDE.md convention line. Working-state and convention only; no corpus or website content changed. Also batches PR #979's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.467 | PR #979** - CCPA §2.23 slice 4 (breadth): adds the relevant final-CCPA-regulation section citations to four privacy framework-alignment tables, completing the regulations-alignment (the primary carriers were slices 1 to 3). The consent-management framework now cites the consumer-consent-method rules (11 CCR section 7004, symmetry in choice and no dark patterns); the children's-data framework gains a row for the minors sale/sharing mechanics (sections 7070 to 7072); the cookie-and-tracker register cites the opt-out preference signal / Global Privacy Control and sale/sharing opt-out (sections 7025 to 7026); and the data-subject-access-request workflow cites the request-handling timelines and the automated-decision-making opt-out and access sections. Every section anchor was re-verified at the held regulations and a skeptical verifier returned ship. Also batches PR #978's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.466 | PR #978** - CCPA §2.23 slice 3: propagates the final California CCPA regulations to the remaining primary carriers. The privacy jurisdiction index's United States row now names the ADMT pre-use-notice, opt-out, and access rights (11 CCR sections 7220 to 7222); the privacy-notice template's automated-decision-making section gains a California pre-use-notice element (section 7220); and the data-subject-rights procedure's California basis now carries the distinct CCPA automated-decision-making rights beyond the GDPR-style human review (a right to opt out, given effect within 15 business days, and a right to access, on the section 7021 request-handling timeline of 10 business days to confirm receipt and 45 calendar days to respond, extendable to 90). Completes the primary-carrier set of the CCPA regulations alignment (slices 1 to 2 were the US privacy annex and the automated-decision-making register); every anchor and timeline was re-verified at the held regulations and a skeptical verifier returned ship. Also batches PR #977's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.465 | PR #977** - CCPA §2.23 slice 2: aligns the automated-decision-making register to the final California CCPA regulations. Corrects a statute-citation error (the ADMT enabling paragraph is California Civil Code section 1798.185(a)(15), not (a)(16), which is the law-enforcement-investigation paragraph) and adds the now-final operative regulations (11 CCR Article 11, sections 7200 to 7222) to the framework-alignment row; and adds the distinct CCPA automated-decision-making subject rights (a pre-use notice, a right to opt out, a right to access, and a human-appeal exception in place of the opt-out) that the register's previously GDPR-framed rights list did not carry. Every anchor was re-verified at the held statute and regulations text, only the California row was touched (not the Canadian CPPA row), and a skeptical verifier returned ship. Continues the per-domain CCPA alignment (slice 1 was the US privacy annex, PR #976); the data-subject-rights procedure, jurisdiction index, and notice template follow. Also batches PR #976's retrospective and quality-assurance result.

**2026-07-16 | 2026.07.464 | PR #976** - Updates the United States privacy jurisdiction annex to the final California CCPA regulations (11 CCR Division 6 Chapter 1, effective 2026-01-01), replacing the prior "draft / under development" framing. Adds precise, source-verified rules for automated decision-making technology (ADMT, Article 11: pre-use notice, opt-out, access, and a human-appeal exception), risk assessments (Article 10, conducted before initiating high-risk processing), and cybersecurity audits (Article 9, a distinct threshold-based periodic audit with first reports phased 2028 to 2030), and corrects the annex's prior conflation of the audit and the risk assessment; the "significant decision" scope is corrected to the regulation's own enumeration. Records the 2026 CCPA Regulations in the canonical-citations register, with currency confirmed upstream this cycle. This is the first slice of the TODO §2.23 CCPA alignment (the annex cluster); the automated-decision-making register, the data-subject-rights procedure, and the remaining carriers follow. Also batches PR #975's retrospective and quality-assurance result. Every anchor was re-verified at the held regulation text, and a skeptical verifier returned ship.

**2026-07-16 | 2026.07.463 | PR #975** - Adds [`.working/maintainer-egress-requests.md`](.working/maintainer-egress-requests.md), a standing channel for reference documents the assistant cannot fetch from this environment (egress-blocked hosts, paywalled or licensed sources): the assistant lists the exact instruments and where to drop them, and the maintainer downloads them. Its first batch is the ~16 Canada.ca instruments the TODO §2.22 reference-utilization apply needs, because canada.ca blocks automated fetch here and that apply is bound for a Canada expert review, so currency must be maintainer-confirmed. TODO §2.22 is deferred until those downloads land (tracked in the pending-decisions queue and the §2.22 status line). Also batches PR #974's retrospective, records PR #974's offloaded quality-assurance result (a worker caught a real overclaim in #974's design-of-record edit, which this PR fixes and whose stale echoes in the #974 changelog entries this PR corrects in place), and folds two small worker-tooling follow-ups into the backlog. Working-state and backlog only; no corpus or website content changed.

**2026-07-16 | 2026.07.462 | PR #974** - Codifies the credit-offload worker-allocation model into the design of record (one order at a time; role-based soft specialization, where a worker prefers an order matching its role but falls back to any eligible order so a live worker never idles beside serveable work, and blocking orders outrank the role preference) and documents the worker reference-read gap: workers currently read the reference base from a single shared, manually re-synced copy rather than from a per-order pinned version, so a reference update mid-order silently changes what a running worker reads, with the target per-order-pinned model recorded. Adds backlog item 3.85 to close that gap; batches PR #973's post-merge retrospective; records PR #973's offloaded per-PR quality-assurance result (a credit-offload worker's zero-findings pass, which as the worker's first quality-assurance delivery was validated by the orchestrator under an elevated review including an independent adversarial auditor); and refines backlog item 3.84 with two verified observations from that pass. Working-state and backlog only; no corpus or website content changed.

**2026-07-16 | 2026.07.461 | PR #973** - Corrects a material Quebec Law 25 penalty-structure error and two related accuracy issues in the Canada privacy jurisdiction annex, ahead of an expert review. The annex had presented the "CAD 25 million or 4% of worldwide turnover" figure as a second, more-serious administrative-penalty tier; that figure is actually the penal fine (Law 25 s. 91), not an administrative penalty. Corrected to a single administrative monetary penalty (s. 90.12: the greater of CAD 10 million or 2% of turnover; natural persons up to CAD 50,000), with the CAD 25M / 4% figure moved to the penal-fine line where it belongs (s. 91, plus the natural-person range). Also narrowed the privacy-impact-assessment duty to its actual statutory scope (s. 23.3, information-system and electronic-service-delivery-system projects) and noted the separate cross-border-transfer assessment (s. 17). Applied from a credit-offload worker's research delivery after every corrected figure was independently re-verified against the held Law 25 text; annex v1.1.2 to 1.1.3. Also batches PR #972's post-merge QA.

**2026-07-16 | 2026.07.460 | PR #972** - Adds two credit-offload backlog items and batches PR #971's post-merge QA. A Priority-3 item to give credit-offload workers a degradation signal and a lightweight in-session self-restart (clear context, then re-invoke the worker command, which safely rejoins by reconciling any held work against its fencing token), since a worker holds no durable state and needs no full handoff; and a follow-up item for a narrow shared-VM worktree-cleanup race the worker-tooling review flagged. Backlog and working-state only; no corpus or website content changed.

**2026-07-16 | 2026.07.459 | PR #971** - The Sweep 108 validation close-out (the loop-break compensating control for the prior session-closing handoff, PR #968), covering PRs #964 to #968. This sweep was the first corpus-wide validation run offloaded to a credit-offload worker, and the orchestrator independently validated its result (re-derived counts, gates, and pre-flight all matched, and an adversarial auditor confirmed no missed findings); the loop-break control passes. Records the sweep-history row, advances the validation cursor, prunes the session handoff to the two most-recent sessions, and applies the two validated worker findings to the backlog (a credit-offload phase-1 completion date corrected to its UTC value, and an omitted offloadable-pass name added so the three surfaces agree). Also adds a backlog item to review the corpus's California CCPA/CPRA content against the newly-added 2026-01-01 CCPA statute once it finishes ingesting, and batches PR #970's post-merge QA. Working-state and backlog only; no corpus or website content changed.

**2026-07-16 | 2026.07.458 | PR #970** - Codifies a credit-offload new-worker QA-trust-tier policy and batches PR #969's post-merge QA. After the first live worker ran and independently checked out, the project instructions and the credit-offload design of record now require elevated orchestrator QA for the first two-to-three QA-kind deliveries from each worker each session (proof-of-run genuineness, independent re-derivation of the mechanical facts, re-verify every finding, and an adversarial auditor on the first delivery), re-established each session and keyed on the worker plus its model so a different model re-triggers it; after that window, routine QA (re-verify positives, trust clean-with-proof-of-run) applies. The count is a floor not a cap, and any confirmed miss or sham resets the window and flags the worker unvalidated. This session's worker was validated on that basis (its two offloaded QA passes were independently confirmed correct, including by an adversarial auditor). Project-instruction and working-state only; no corpus or website content changed.

**2026-07-16 | 2026.07.457 | PR #969** - Applies credit-offload phase 3, the orchestrator-side wiring of the multi-worker QA-and-research offload queue (maintainer-authorized). The resume flow now checks for a live worker and, when one is present, enqueues the mandatory loop-break validation sweep as a blocking offload order and consumes its verified result instead of self-running it, saving the orchestrator the large subagent-token cost; with no worker it self-runs as before (offload is best-effort, never a QA skip). Adds a Credit-offload mode section to the project instructions (the offloadable-pass set, the worker-availability gate, the re-verify-positives-and-trust-clean consume discipline, and the honest cost-shifting limitation), and records the design of record as phase-3-applied plus two worker-lifecycle hooks (worktree cleanup on wind-down, reconcile on re-register) and the intra-order-checkpoint non-goal from a worker's design assessment. This session's mandatory Sweep 108 validation is itself offloaded to the live worker as the credit-offload test. Project-instruction, working-state, and backlog only; no corpus or website content changed.

**2026-07-16 | 2026.07.456 | PR #968** - Session-closing handoff for the 2026-07-16 resumed session (#964-#967): refreshes the session handoff (new next-actions, state-snapshot, and asserted-expectations blocks), adds the session-metrics row, resets the stale overnight-run file to its idle state, releases the concurrency lease, and batches PR #967's post-merge QA (which returned zero findings). Per the loop-break, this handoff PR takes no trailing per-PR QA; the compensating control is the next resume's corpus-wide validation sweep. The session built the credit-offload multi-worker QA-and-research queue (phases 1 and 2, on the scratch exchange, so a worker is testable) and stocked it with five orders; the next session's first substantive task is credit-offload phase 3 (the orchestrator-side wiring staged this session for maintainer review). Working-state only; no corpus or website content changed.

**2026-07-16 | 2026.07.455 | PR #967** - Adds the Canada.ca reference-utilization plan to the backlog and batches PR #966's post-merge QA. The new Priority-2 TODO item (§2.22, flagged Canada-priority because Canadian experts review the corpus in the next few days) captures systematic engagement of the 49 newly-held Canada.ca authoritative sources (the Treasury Board AI-governance suite, OSFI B-13 and E-23, the Privacy Act and OPC and PIPEDA privacy set, the ITSG-33 and CCCS security baselines, and the public-sector policy and directive suite) across the Canada AI and privacy annexes, the compliance matrix, and the security baselines; its research half is delivered as three priority-1 credit-offload seeds (breadth, annex source-verification, matrix-fit) queued on the scratch exchange for tomorrow's workers. This PR also fixes two low-severity self-consistency notes that PR #966's post-merge sweep found in the new credit-offload design doc (a broken internal section-anchor and a build-status overstatement). Working-state records and backlog only; no corpus or website content changed.

**2026-07-16 | 2026.07.454 | PR #966** - Records the credit-offload design (a multi-worker QA and research queue that moves the read-only analysis passes, the validation sweeps and the semantic-fit cadences, plus research and drafting seeds, onto standing worker sessions on other accounts, so the orchestrator spends its usage credits only on author-apply-route-merge) as a working design of record, and opens the backlog for it. Adds three TODO items: a Priority-1 cross-repo write-safety guardrail (to prevent a working-directory-dependent git command silently targeting the wrong one of the three colocated repositories), the Priority-3 credit-offload build, and a periodic reassessment of keeping the pre-push verifier on the orchestrator account. Stages the credit-offload orchestrator-side wiring (which touches the resume flow and the project instructions) for maintainer review rather than applying it unattended. Also batches PR #965's post-merge QA (the PR-scoped validation sweep, which returned zero findings, and the retrospective). Working-state records and backlog only; no corpus or website content changed.

**2026-07-15 | 2026.07.453 | PR #965** - Batches PR #964's post-merge QA (the PR-scoped validation sweep, which returned zero findings, and the retrospective) and closes task 1 of the resumed session's running order. Records that the fabricated-AICM-code defect sitting in the pending-decisions queue (seven framework-alignment cells in the AI-coding-assistant-security guideline citing non-existent codes) was already fixed in PR #939, which remapped the seven cells to real CSA AICM v1.1.0 codes; the queue entry had simply never been rotated out after the fix shipped. All seven current codes were re-verified against the held AICM v1.1.0 catalogue titles (all fit) and the control-code validity gate passes, so no fresh matrix-fit sweep was run. Working-state records only; no corpus or website content changed.

**2026-07-15 | 2026.07.452 | PR #964** - Resume of a fresh session from PR #963: ran the mandatory loop-break Sweep 107 corpus-wide validation over the #955 to #963 delta window, acquired the concurrency lease, and advanced the validation-sweep cursor. The sweep found one low-severity in-window issue and fixed it: three internal files (the static-site generator docstring, the web-generator-health workflow comment, and the Cloudflare Pages setup runbook title) still carried a stale "(TODO section 2.4)" provenance pointer to a backlog item that was closed in PR #960, which the closing session's residual grep missed because it searched only the "§2.4" glyph form inside the backlog file; the stale pointer is dropped from all three. Everything else the sweep checked (the Canada AI annex accuracy, the fourth-review citation fix, the public-site text, and the audit-gate four-surface parity and counts) verified clean, and the loop-break control for PR #963 passes. Working-state and internal tooling only; no corpus or website content changed.

**2026-07-15 | 2026.07.451 | PR #963** - Session-closing handoff for the 2026-07-15 resumed session (#955-#962): refreshes the session handoff (new state, next-actions, and asserted-expectations blocks, pruned to keep the current + prior session), adds the session-metrics row, releases the concurrency lease, and batches PR #962's post-merge QA. Winds down to a fresh overnight session, which runs the loop-break Sweep 107 validation and then the version-maturation initiative. Per the loop-break, this handoff PR takes no trailing per-PR QA; the compensating control is the next resume's corpus-wide validation. Working-state only; no corpus or website content changed.

**2026-07-15 | 2026.07.450 | PR #962** - Public-site For-AI page: replaced the opaque academic citations "(Mitchell et al., 2019)" and "(Gebru et al., 2018)" on the Model Cards and Datasheets-for-Datasets entries with plain-language source references ("from the 2019 / 2018 research paper that introduced the practice"), so a general reader is not left with an unexplained author-year citation. Also queues two maintainer-flagged, P3-prioritized backlog items: §3.78 (link the website's skill entries to their SKILL.md file, not the bare directory) and §3.79 (give corpus coverage to the For-AI "named, not yet covered" instruments, then sync the page; corpus-first). Website template and backlog only; no corpus content changed. Also batches PR #961's post-merge QA.

**2026-07-15 | 2026.07.449 | PR #961** - Two small public-site copy and style tweaks. On the about page, the ", CGEIT, CISSP" credential suffix after the maintainer's name is now set at half the name's font size (a nested `.m-certs` span at `font-size: 0.5em`), so the uppercase certifications sit at about half the visual height of "Jeff Posluns" instead of matching it. On the landing page, the §01 lede is reworded from the "not advice or a product; it is a public corpus" contrast framing to a positive statement ("a public corpus of openly-licensed reference documentation ... that [the audiences] can freely read, cite, adopt, and tailor to their own context"). Website templates only; no corpus content changed. Also batches PR #960's post-merge QA.

**2026-07-15 | 2026.07.448 | PR #960** - Maintainer-flagged TODO stale-item cleanup plus the PR #959 QA close-out; no corpus content changed. Closed two done public-site backlog items to the DONE ledger: §2.4 (grclibrary.ai is built and live, maintainer-confirmed done 2026-07-15; the publish go-decision and the separately-tracked §2.15 standards-linking remain) and §2.6 (Cloudflare build-watch-paths, applied in the maintainer console). Reworded the six now-dangling `§2.4` references across the backlog (§1.12 unblocked; §2.15/§3.74/§3.75/§4.9). Also fixed a one-digit tally the #959 `/validate-pr` found in the Sweep 106 record ("0 note" to "1 note"; working-state only) and batched PR #959's `/validate-pr` + `/retro`.

**2026-07-15 | 2026.07.447 | PR #959** - Corrected a third carrier of the "third review" ordinal error, this time in the canonical citations register: its Treasury Board Directive on Automated Decision-Making row labelled the 24 June 2025 to 24 June 2026 compliance transition as "third-review amendments" when it is the fourth review (the same fix made in the Canada AI annex in PR #955 and the AI-and-privacy procedure in PR #956; this carrier used the hyphenated "third-review" spelling the earlier space-form grep missed). The 8 October 2024 announcement date is retained as the fourth-review announcement. Found by the loop-break corpus-wide validation sweep (Sweep 106) over PRs #943 to #958; also batches PR #958's post-merge QA. Register v1.5.36 to 1.5.37.

**2026-07-15 | 2026.07.446 | PR #958** - Date-anchored the Algorithmic Impact Assessment (AIA) question counts in the Canada AI regulatory annex ahead of an expert review: the "65 risk questions and 41 mitigation questions" figure is now attributed to the 2026-05-28 version of the Treasury Board AIA tool (the version held in the reference base, which states those counts verbatim) instead of an undated "current release", so the counts age visibly rather than silently as TBS revises the question set. The counts themselves are unchanged and correct. Annex v1.0.1 to 1.0.2. Also batches PR #957's post-merge QA (the PR-scoped validation sweep and the retrospective).

**2026-07-15 | 2026.07.445 | PR #957** - Four small public-site text fixes. The landing hero "Governance documentation, engineered like software." now sits on two lines (one per phrase, breaking only after "documentation,"); the §01 tagline "A reference library you can cite, not just read." now fills one line instead of splitting mid-phrase after "you"; the about page reads "thirty years of leadership" (was "over thirty years"); and the For-AI hero keeps each colour on its own line ("Learning governance and security" in white, "from this corpus." in orange). Website templates only; no corpus content changed. Also batches PR #956's post-merge QA (the PR-scoped validation sweep and the retrospective).

**2026-07-15 | 2026.07.444 | PR #956** - Corrected the same "third review" factual error in a second document (the integrated AI and privacy assessment procedure): the Treasury Board Directive's current (24 June 2025) version followed the directive's fourth review, not the third (which took effect April 2023), matching the Canada AI annex fix in PR #955. The error was surfaced by PR #955's post-merge cross-reference check. Also batches PR #955's post-merge QA records (the PR-scoped validation sweep and the retrospective, including the first-ever skeptical-verifier override entry).

**2026-07-15 | 2026.07.443 | PR #955** - Corrected and expanded the Canada AI regulatory annex ahead of an expert review. Fixed the Treasury Board Directive review ordinal (the 24 June 2025 to 24 June 2026 compliance transition is from the directive's fourth review, not the third, which took effect in April 2023); clarified that the directive's requirements are partly scaled to the impact level and partly applied as a baseline; corrected a limitation that wrongly placed the impact-level requirement scaling outside the primary text (it is set in the directive's Appendix C); and added a section on the AI Strategy for the Federal Public Service 2025-2027 and its Government of Canada AI Register transparency deliverable. Every instrument fact was verified against the held primary sources and confirmed on canada.ca.

**2026-07-15 | 2026.07.442 | PR #954** - Working-state close-out for the 2026-07-15 website session: batches PR #953's post-merge QA (`/validate-pr` + `/retro`), fixes the #953 `/validate-pr` warning (a session-state prose line left a PR stale after the heartbeat re-stamp), refreshes the session handoff and metrics, and releases the concurrency lease. Session-closing handoff PR; no corpus document or website content changed.

**2026-07-15 | 2026.07.441 | PR #953** - Added a listing page for each document type to the public site: the "By document type" chips on the landing page now link to a page that lists every document of that type (for example every Standard, or every Policy) across all domains, each linking to its source on GitHub, with a short description of what the type is. Also shared the document-list styling between the new per-type pages and the existing per-domain pages so both draw from one definition. Website template and generator only; no corpus document content changed.

**2026-07-15 | 2026.07.440 | PR #952** - Landing-page polish on the public site: added a short orange eyebrow tagline above every landing section (matching the existing "For AI-assisted teams" one on the governance-pack section), and turned the out-of-place green check-marked line at the end of the "machine-auditable by construction" section into a boxed call-to-action linking to the audit-programme documentation, so it matches the surrounding style. Removed the now-unused styling for the old green line, and advanced a backlog counter that a prior PR left un-incremented. Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.439 | PR #951** - Added a contents sidebar to the public site's "For AI", per-domain, and Contributors pages, matching the landing and pack pages, and refined the sidebar highlighting so navigation items that share a scroll position light up together (on a wide screen the three standards sub-groups shown side by side, "Information security / AI governance / NIST cybersecurity", now highlight as a group, and likewise the next three). Moved the shared sidebar styling into the common stylesheet so all five sidebar pages draw from one definition, with the pack page keeping its deliberate non-scrolling long index. Also linked three file paths in a prior detailed-changelog entry and batched PR #950's post-merge QA. Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.438 | PR #950** - Corrected the spelling of "License" on the public site: the visible text (the "License & reuse" section heading, the sidebar and footer links, and the body prose) now uses the "s" spelling throughout, matching the corpus's own dominant usage (the per-document metadata field, the LICENSE file, and Creative Commons' own name all use "License" with an s) instead of the mixed "Licence". Internal identifiers, CSS class names, and anchor links are left unchanged (not user-visible). Also reworded a stale backlog reference in a generator docstring and batched PR #949's post-merge QA. Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.437 | PR #949** - Added a regression-suite test that keeps the two document-ordering generators in sync (backlog item §3.76). The reading-progression order is defined in both the taxonomy generator and the website generator; the new test asserts they carry an identical type-order ranking and a matching secondary sort key (case-insensitive title with a path tiebreaker), so a future edit to one that misses the other fails the test rather than silently diverging on the site, the exact drift the Sweep 105 finding caught. Also rotated two completed backlog items to the DONE ledger (§3.76 here, and §2.16 whose residual shipped in PR #948 but was not rotated at the time) and batched PR #948's post-merge QA. Test and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.436 | PR #948** - Completed the landing-page left-nav enhancement (the §2.16 residual): the six "Get started" cards now have anchor ids and appear as indented sub-links under "Get started" in the sidebar (matching the domains-under-By-domain and Standards sub-link nesting), and the sidebar now has scrollspy highlighting, the link for the section or sub-item currently in view is highlighted as you scroll, with the parent section also lit when you are on one of its sub-items. The scrollspy is a small script added to the shared script file (the page already runs the theme-toggle script), degrades gracefully to plain static links if it does not run, and no-ops on pages without the sidebar. Also batched PR #947's post-merge QA. Website template and generator only; no corpus document content changed.

**2026-07-15 | 2026.07.435 | PR #947** - Linked the words "GRC Library" in the public landing page's "Licence & reuse" section to the repository's AUTHORS.md, so a reader who wants to attribute or cite the library reaches the human-readable attribution and how-to-cite page (with ready APA and BibTeX citations) directly; the machine-readable CITATION.cff already backs GitHub's "Cite this repository" button. Also harmonized the "For AI" sidebar link to a trailing slash for consistency and batched PR #946's post-merge QA. Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.434 | PR #946** - Made the public site (grclibrary.ai) friendlier to AI systems that read or train on the corpus. Added a new "For AI" page (linked from the landing sidebar) that describes, in plain descriptive language (never as an instruction to the reader, to avoid any prompt-injection reading), how an AI can best learn from this openly-licensed corpus, and indexes the AI-governance, AI-security, AI-legislation, data-quality, and foundational security/privacy resources the corpus documents, each linked to where the corpus covers it. Added a hand-authored robots.txt that explicitly welcomes AI and search crawlers (23 named crawlers plus an allow-all, replacing the restrictive platform default), a sitemap.xml listing every page, an llms.txt site map for language models, and schema.org Dataset/licence metadata on the landing page marking the corpus as an openly-licensed, freely-reusable dataset. Verified by a skeptical reviewer (documentary framing, link validity, legal-status accuracy, content boundary, and generator correctness all confirmed). Also batched PR #945's post-merge QA. Website generator and templates only; no corpus document content changed.

**2026-07-15 | 2026.07.433 | PR #945** - Reworked the "By domain" section text on the public landing page (grclibrary.ai) for clarity. The document count ("312 documents across 11 governance domains") is now a normal section-intro paragraph above the table, in the same style as the other sections, instead of a small table caption. The note below the table, which previously read "Domain counts total 310" (confusing, since the headline says 312), is reworded to explain the gap plainly: the per-domain rows sum to 310, and the other 2 of the 312 total documents are programme-level specifications at the corpus root, and it is set at the same text size as the section paragraphs. Also batched PR #944's post-merge QA. Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.432 | PR #944** - Gave the three "Three ways to use it" cards on the public governance-pack page (grclibrary.ai/pack) working links, matching the main site's card style: each card's small heading now links to the most relevant place on GitHub (the repository to fork, the adopter guide, and the pack directory to drop into any project). Previously those three cards had no link at all, unlike every other card on the site. Also batched the post-merge quality checks for PR #943 (a validation-record row and a retrospective row) and corrected a small internal miscount in the PR #943 sweep record (a candidate count that read "6" where the file elsewhere said "11"). Website template and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.431 | PR #943** - The `/resume` loop-break Sweep 105 validation close-out for the just-closed session (covering PRs #918 to #942). The corpus-wide sweep found one user-visible website defect: the domain pages on grclibrary.ai sorted documents within a type using case-sensitive titles, so a title like "eIDAS Sector Requirements Annex" sorted to the end of its group instead of alphabetically among the other E entries, diverging from the canonical taxonomy and portal order. Aligned the website generator's sort key to the case-insensitive, path-tiebroken key the taxonomy generator already uses, so the two now agree. Also recorded the sweep history and detail, pruned the session handoff to the two most-recent sessions, and re-acquired the concurrency lease for this session. Website generator and working-state only; no corpus document content changed.

**2026-07-15 | 2026.07.430 | PR #942** - Session-closing handoff for the 2026-07-15 long resumed session (overnight #929-#936 + attended wind-down #937-#941, merged through #941): refreshed the session-handoff record (new state snapshot, asserted expectations, and next-actions with the maintainer's "review the deployed site first" directive), added the session-metrics row, batched PR #941's post-merge QA, and released the concurrency lease. Per the session-closing loop-break this PR takes no trailing per-PR validation or retrospective; the next session's `/resume` corpus-wide validation is the compensating control. Working-state only; no corpus content changed.

**2026-07-15 | 2026.07.429 | PR #941** - Rebuilt the landing page's left navigation into a two-level quick-nav so it no longer ends with a flat list of domains: the 11 domains now nest as indented sub-links under "By domain", the six Standards sub-groups nest under "Standards", Licence is kept, and a new Contributors link (to the about page) is added at the end. Fixes the maintainer's observation that the nav appeared to end with the domains and not surface Standards or Licence clearly. Scrollspy highlighting and Get-started nesting remain as the §2.16 residual. Also fixes a working-state warning (the concurrency-lease task field was fully rewritten to end a recurring stale-snapshot pattern) and batches PR #940's post-merge QA. Website template and generator only; no corpus document content changed.

**2026-07-15 | 2026.07.428 | PR #940** - Reordered the per-domain document list on the website domain pages (and in the taxonomy source) from an alphabetical-by-type order to a logical reading progression (govern then define then do then reference: Charter/Policy, then Framework/Standard, then Procedure/Guide, then Register/Template/Annex, alphabetical by title within a type). The website generator previously sorted by type name alphabetically, so Annex and Charter floated to the top; it now sorts by a reading-progression rank, matched by the same rank in the taxonomy generator so the source file reads consistently with the pages. A lossless re-sort (all 312 documents preserved); the audit tools are order-insensitive. Also batches PR #939's post-merge QA. Tooling only; no corpus document content changed.

**2026-07-15 | 2026.07.427 | PR #939** - Fixed a live citation defect: 7 fabricated CSA AICM control codes in the AI Coding Assistant Security Guideline's framework-alignment table (the `AI-GOV`/`AI-DATA`/`AI-SEC`/`AI-INC` pseudo-codes) were remapped to real AICM v1.1.0 codes (a maintainer-approved matrix-fit judged against the held CSA catalogue: GRC-09, DSP-07, AIS-10, AIS-15, AIS-11, TVM-13, SEF-08). This was the live instance found during the §3.43 gate-48 FP-census; gate 48 was blind to it because its leading `AI-` defeated the code-detection lookbehind. Also recorded two maintainer backlog decisions (TODO §3.47 rescoped to keep `(was X.Y)` renumber breadcrumbs per the #929 convention; §3.8 closed as won't-do, keeping the per-document `--follow` git subprocess in gates 31/40 rather than trading history fidelity for speed) and batched PR #938's post-merge QA.

**2026-07-15 | 2026.07.426 | PR #938** - Batched PR #937's post-merge QA (one in-window working-state warning fixed: the session-state Current-task tail was reconciled after an earlier edit corrected only its opening) and routed a newly-found backlog scope-conflict (TODO §3.47's plan to strip `(was X.Y)` renumber breadcrumbs contradicts the #929 permanent-numbering convention, which keeps them; needs a maintainer rescope). Overnight run holds after an evidence-based item-by-item reassessment found no cleanly-buildable-unattended item remaining. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.425 | PR #937** - Consolidated the fenced-code-block skip check used across the linters onto a single shared `is_fence_line()` helper, closing a latent gap where six linters did not recognize tilde (`~~~`) code fences and could scan or skip the wrong content. Behaviour-preserving on the current corpus (no document uses tilde fences); verified by two independent reviewers, a new predicate test, and a guard-first fixture. Also batches PR #936's post-merge QA and routes a separately-found citation issue (fabricated AICM codes in one dev-security document) to the maintainer for review. Tooling and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.424 | PR #936** - Overnight resting-point close-out: refreshed the next-PRs queue file to the queue-exhausted / daytime-priority state (fixing a PR #935 staleness where it still listed now-deferred items as the immediate next) and batched PR #935's post-merge QA. The overnight run's cleanly-unblocked queue is exhausted, so the session holds in overnight mode. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.423 | PR #935** - Overnight preparation for the remaining machinery items: staged the two protected-surface P3 items (§3.22 the D7 handoff-snapshot marker fix and §3.12 the See-Also parity gate) into the deferred-protected-changes queue with drafted content for a quick daytime apply, since both touch the protected AI-assistant config that overnight mode cannot authorize. Also recorded an assessment of §3.38 (gate 39's mechanizable count-idioms are largely already covered by its existing patterns; the false-positive-safe residual needs a careful attended census). Batches PR #934's post-merge QA. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.422 | PR #934** - Extended the CHANGELOG pre-flight aid so it now flags a newly-added CHANGELOG line whose in-repo relative markdown-link target does not resolve (the detailed mirror is gate-exempt, so such a dangling link was previously ungated), advancing backlog item §3.34. Cross-repo, external, and code-span-illustrative links are excluded. A census also found about 23 pre-existing dangling links in the mirror, recorded under §3.34 as the remaining cleanup. Batches PR #933's post-merge QA. Tooling and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.421 | PR #933** - Widened audit gate 69 (the positional-backlog-token check) so it also catches the "TODO item N.M" phrasing, not just "TODO §N" and "backlog item PN.M" (closing backlog item §3.50). A corpus census confirmed the widening is false-positive-safe (no live carrier, and ordinary "TODO item covers ..." prose has no section token so it is not flagged), with two regression fixtures added and the audit-programme spec's gate-69 description updated to match. Batches PR #932's post-merge QA. Tooling and backlog only; no corpus requirement changed.

**2026-07-15 | 2026.07.420 | PR #932** - Split the §2.5 AI-domain-delta backlog item: its landed workstreams (the EU/CA source fold-ins A.1-A.5 and the currency residuals C.1/C.3/C.4) are recorded in the DONE ledger, and its remaining distinct workstreams are re-homed into five new-numbered P2 items, §2.17 (California), §2.18 (South Korea), §2.19 (Singapore), §2.20 (ref-side currency sweep), §2.21 (further deferred jurisdictions). The §2.5 umbrella is retired and its number will not be reused. Batches PR #931's post-merge QA. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.419 | PR #931** - Split the §2.4 website-umbrella backlog item: the completed build effort (the #919-#928 live-review and adoption rounds, now live on grclibrary.ai) is recorded in the DONE ledger, and §2.4 is trimmed to only its remaining maintainer-gated items (further review fixes, the §2.15/§2.16 follow-ups, the §2.6 console action, and the publish go-decision). §2.4 keeps its number and stays open until publish. Batches PR #930's post-merge QA. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.418 | PR #930** - Split four partially-done backlog items (§3.57 reference-breadth apply, §3.62 guardrail-review proposals, §3.63 reference-audit findings, §3.68 vuln-SLA conversions): their completed components are now recorded in the DONE ledger and only each item's open residual stays in TODO (each item keeps its permanent number and remains open). First application of the new permanent-numbering hygiene. Batches PR #929's post-merge QA. Working-state and backlog only; no corpus content changed.

**2026-07-15 | 2026.07.417 | PR #929** - Made TODO item numbers permanent and never recycled: each priority section now carries a "Next item number" counter, maintained on every edit, so new and split-out items each draw a fresh number and a lookup by number maps to exactly one item across the file's history. Recorded four maintainer-confirmed website and quality-tooling backlog items (standards-list source links, a website-to-corpus link-integrity gate, an external-source currency mechanism, and a two-level landing nav), refreshed one governance spec's audit-gate rationale to match the new rule, and batched PR #928's post-merge QA. No requirement or corpus content changed.

**2026-07-15 | 2026.07.416 | PR #928** - Three follow-up fixes to the public site from live review: the top-of-page buttons now cover all the main sections (including a link to the governance-pack page), the pack page's contents sidebar lists all 23 skills (a display bug had hidden most of them behind an internal scroll), and the "Get started" cards now match the styling and link pattern of the other cards on the page. No corpus document changed and no corpus content is published beyond the public links.

**2026-07-15 | 2026.07.415 | PR #927** - Added backlog item §2.6 (the maintainer-console Cloudflare build-watch-paths action for the 11 domain directories, deferred to the next computer session), corrected a fourth internal generator help-text page-set carrier the prior docstring sweep missed, and batched PR #926's post-merge QA. Working-state, backlog, and internal help-text only; nothing adopter-facing changed.

**2026-07-15 | 2026.07.414 | PR #926** - Restructured the public landing page around getting people started. A new "Get started" section now sits near the top (third), with six cards that walk a newcomer through adopting the library, find your path, see a worked example, start from a template, map your obligations, adopt the whole programme, and assess your maturity, each linking to the matching document already in the corpus. The governance-pack section is slimmed to three highlights that link to the full pack page, and the Creative Commons licence, previously the lead of the closing section, now has its own dedicated "Licence & reuse" section at the very end. The page navigation and footer were updated to match. No corpus document changed and no corpus content is published beyond the public links.

**2026-07-15 | 2026.07.413 | PR #925** - Added a dedicated governance-pack page to the public grclibrary.ai site. It presents the project's AI-assistant discipline layer, the rules and skills distilled from running the library, as something separate in kind from the GRC content: what it is, the three ways to adopt it, all 13 rules (each with a one-line purpose and a link to its source), and all 23 skills grouped by purpose, with a contents sidebar listing every rule and skill as an at-a-glance reference. The site footer now links to it. No corpus document changed and no corpus content is published beyond the public links.

**2026-07-14 | 2026.07.412 | PR #924** - Added a contents-navigation sidebar to the public landing page. On a phone or tablet it appears as a boxed "Contents" panel near the top, listing the six page sections and all eleven governance domains, so a visitor sees the site's breadth up front instead of a long unbroken scroll; on a wide screen the same navigation becomes a sticky sidebar beside the content. The other pages are unchanged. It also folds in the previous PR's post-merge review: a documentation count was corrected (fifteen card links to fourteen distinct files) and a generator docstring was refreshed. No corpus document changed and no corpus content is published beyond the public links.

**2026-07-14 | 2026.07.411 | PR #923** - Made the public site's titles into links and tightened the domain pages. On the landing page, each feature-card keyword (Structured, Cross-linked, Integrity, Citations, and the rest, plus the six governance-pack rule names) now links to the corpus page it refers to. On each domain page, the document name is now itself the link to that document's source on GitHub (the separate "GitHub" link is gone, and a small arrow marks the jump), and the vertical spacing between section separators was reduced so the document list is visible sooner, notably on a tablet. It also folds in the previous PR's post-merge review: the deploy runbook's overview was corrected to describe the full page set, and a deprecation warning in the site generator was fixed. No corpus document changed and no corpus content is published beyond the public links.

**2026-07-14 | 2026.07.410 | PR #922** - Added a page for each of the library's 11 governance domains to the public grclibrary.ai site. Every domain page opens with that domain's own purpose statement, then lists all of the domain's documents with a link to each document's source on GitHub; the domain names in the landing-page register now link to these pages, and each page carries its own search-engine title, description, and canonical address. Also corrected the hero intro paragraph on every page, which was wrapping short, to fill the column width like the section paragraphs (the companion to the previous PR's fix), and updated the site generator's help text to describe the now-larger page set. The site still publishes no adopter-facing corpus content beyond each domain's public purpose statement and adds no corpus document.

**2026-07-14 | 2026.07.409 | PR #921** - Polished the public grclibrary.ai site from a maintainer review. Body paragraphs in each section now fill the full column width, matching their headings and the card grid instead of wrapping short, and the summary "stat" boxes whose value is a word ("Continuous", "CC BY-SA") are sized so the word no longer overflows its box. Every off-site link on both pages, the Creative Commons licence, the governance-pack link, and the About page's LinkedIn, GitHub, contributing-guide, and contributor-profile links, now opens in a new browser tab rather than navigating away from the site. Housekeeping: the site generator's help text now says it renders two pages, the deploy runbook's pre-publish note points to the About page where the maintainer bio now lives, and a block of unused styling was removed. It also batches PR #920's post-merge validation, which shipped with notes only: one internal help-text lag was fixed here, and three standards editions the check queried were confirmed current against the citations register. No adopter-facing corpus content changed and no corpus document was added.

**2026-07-14 | 2026.07.408 | PR #920** - Restructured the public grclibrary.ai site into two pages that share one layout. The maintainer bio moved off the landing page onto a new About page, which also acknowledges the project's contributors by name with links to their GitHub profiles, drawn from the repository's own contributors list. The landing page's stylesheet, masthead, footer, and theme script became shared single-source pieces, so the two pages cannot drift apart. The console statusline projection of upcoming work was reformatted to a compact under-120-character line that shows at least three next items, and PR #919's post-merge validation records are batched in. A follow-up to review and standardize how the corpus references standards, toward the maintainer's preferred release-year form, was registered as TODO section 3.74. The site still publishes no adopter-facing corpus content and adds no corpus document.

**2026-07-14 | 2026.07.407 | PR #919** - Built the public grclibrary.ai landing-site generator (backlog section 2.4): a stdlib-only builder that renders one self-contained landing page from the live corpus at build time, recomputing every figure from the taxonomy and README so nothing is hardcoded, plus its page template, a separate generator-health CI check, and a Cloudflare Pages runbook; the rendered output is git-ignored and rebuilt on each deploy, and the page publishes no adopter-facing corpus content. It also corrected PR #918's audit trail: a "5th fix" #918 had claimed (a latent gate-50 failure) was refuted as a phantom by the post-merge validation, so the records carrying it are corrected to the true four-fix count: four are reworded, the redundant cell edit is reverted, and the immutable merge-commit message is noted as corrected of record here (a #919 post-merge validation note, fixed in PR #920).

**2026-07-14 | 2026.07.406 | PR #918** - First PR of the resumed session: ran corpus-wide validation Sweep 104 over the previous session's closing changes (#915-#917); the loop-break control passed with no adopter-facing escape and every asserted expectation corroborated. It fixed four in-window audit-tooling accuracy items: a stale "four checks" count in the bookkeeping-parity gate docstring, and three nits in the advisory changelog-length tool (a recycled section reference, a total-versus-single-sentence word conflation, and a splitter that skipped question and exclamation marks). It also pruned the resume handoff and re-acquired the concurrency lease; housekeeping only, nothing adopter-facing changed. (A fifth item this entry originally claimed, a "latent gate-50 failure" in a handoff record, was found to be a phantom by the next PR's post-merge validation and is corrected in PR #919.)

**2026-07-14 | 2026.07.405 | PR #917** - Session-closing handoff for the 2026-07-14 resumed session (two substantive PRs, #915 and #916, no adopter-facing escapes): batched #916's post-merge QA and its two fixes, recorded the §3.73 gate design-defer, refreshed the resume handoff and asserted expectations, added the session-metrics row, and released the concurrency lease. The maintainer chose the wind-down on a recurring mechanical-edit precision signal; per the loop-break this closing PR takes no trailing per-PR QA, and the next resume runs a corpus-wide validation sweep over #915 to #917. Housekeeping only, nothing adopter-facing changed.

**2026-07-14 | 2026.07.404 | PR #916** - Reformatted the root CHANGELOG entries for #902-#914 from dense semicolon-chained run-on sentences back to the compact plain-language form (closes TODO §1.2), and strengthened the advisory length guard to also flag any single sentence over 65 words, which the prior word-count-only check missed. Also fixed two bookkeeping items the #915 post-merge review caught (a merged table row in the sweep-history ledger and a stale count) and routed a proposed ledger-table-integrity check to TODO §3.73.

**2026-07-14 | 2026.07.403 | PR #915** - First PR of the resumed session: ran corpus-wide validation Sweep 103 over the previous session's r3-remediation changes (#901-#914) and found it clean except for one documentation-completeness note, fixed here (the audit-programme specification's plain-language description of gate 50 had not been extended to cover the deep-assessment register row-order check that shipped in #913). Also pruned the resume handoff to its two most-recent sessions and banked the session's resume decisions; housekeeping plus a one-sentence specification addition, nothing adopter-facing changed.

**2026-07-14 | 2026.07.402 | PR #914** - Session-closing handoff for the 2026-07-14 remediation session (13 merged PRs, #901-#913, with no adopter-facing escapes): refreshed the resume handoff and asserted expectations, added the session-metrics row, released the concurrency lease, and recorded this PR's handoff-exemption row. Per the loop-break, this closing PR takes no trailing per-PR QA; the next resume runs a corpus-wide validation sweep over #901 to #914 as the stronger compensating control. Housekeeping only, nothing adopter-facing changed.

**2026-07-14 | 2026.07.401 | PR #913** - Added an internal ordering check to the bookkeeping-parity gate that flags any deep-assessment register row whose run number is not greater than the previous row's. It was folded into the existing gate rather than shipped as a standalone new gate (avoiding net-negative maintenance on a small, low-churn table), raises no false positives, produces no findings for forks that lack the register, and ships with four regression fixtures. Also batched the prior PR's post-merge QA.

**2026-07-14 | 2026.07.400 | PR #912** - FR-201 vulnerability-remediation-SLA single-source completion (TODO §3.68, partial): a full-corpus recheck found the earlier claim that no other document diverged had been over-stated. Four clear carriers were re-anchored to the vulnerability-management procedure as the single source of truth (their divergent restatements replaced by citations or re-anchored via a governing note, one looser value tightened to match), and four genuinely divergent values needing maintainer judgment (including intentionally separate supplier-tier bars) were routed rather than changed. Also batched the prior PR's post-merge QA.

**2026-07-14 | 2026.07.399 | PR #911** - ISO/IEC 20000-1 clause-attribution accuracy pass (closes TODO §3.72): a full-cluster review of the operations documents citing ISO/IEC 20000-1:2018, judged against the held standard, corrected 11 clause citations across 7 documents. The most notable fixes were a fabricated clause label in two standards and a wrong-clause citation in the change-management procedure; every clause title was verified word-for-word against the held source. Also batched the prior PR's post-merge QA.

**2026-07-14 | 2026.07.398 | PR #910** - ISO/IEC 20000 family reference-breadth review (closes TODO §3.67): a reference-audit pass over the newly-held ISO 20000 family found the corpus already engages the normative ISO/IEC 20000-1 well, so only the single strongest addition was made, an informative see-also to ISO/IEC TS 20000-11:2021 (the standard-to-ITIL bridge) on the IT-service-management framework. An incidental clause-mis-attribution finding was routed to a separate full-cluster accuracy pass rather than fixed piecemeal. Also batched #909's post-merge QA.

**2026-07-14 | 2026.07.397 | PR #909** - Internal quality-machinery cleanup (closes TODO §3.64): retired three dormant pattern-checks in a cross-document numbering gate that matched no documents (so they added no protection while implying coverage; the gate stays active on its remaining GDPR breach-notification term), added a missing documentation cross-reference between two related gates, and formally closed a long-standing paired-surface improvement candidate whose mechanizable half had already shipped. Also batched the prior PR's post-merge QA. No adopter-facing content changed.

**2026-07-14 | 2026.07.396 | PR #908** - CHANGELOG hygiene (closes TODO §3.65): reformatted the root entries for PRs #887-#901 from long multi-sentence paragraphs back to the compact one-liner form (each compression verified against the detailed mirror), and added a light advisory tool that warns when a root entry runs too long (advisory only, not a CI gate). Also batched the prior PR's post-merge QA, fixing two in-window bookkeeping items.

**2026-07-14 | 2026.07.395 | PR #907** - Two reference-breadth items now that the ISO/IEC 20000 family is held: added ETSI TR 104 128 (securing-AI implementation guidance) as a corroborative see-also in the AI security implementation guide, and verified and tightened the IT-service-management framework's ISO/IEC 20000-1:2018 citation against the now-held source. Also completed an earlier internal-audit title canonicalization by fixing the one bare "GRC Manager" residual a prior review found.

**2026-07-14 | 2026.07.394 | PR #906** - Remediated the remaining medium and low findings from the fresh-reader review in one batch: added Brazil (15-day) and Mexico (20-day) data-subject-request clocks to the privacy documents (which had run only the GDPR, CCPA, and PIPEDA windows), defined the AI incident-response plan's "Joint Command" by cross-reference, fixed an internal-audit self-review gap and canonicalized a role title, and applied four documentation-hygiene fixes. Four further findings and a corpus-wide title sweep were routed for maintainer decision.

**2026-07-14 | 2026.07.393 | PR #905** - Reconciled three divergent operational security values to their governing policies: removed the last TLS 1.2 exception in the media-handling procedure (now TLS 1.3 only), raised the certificate-authority key-size minimum to 4096-bit RSA or P-384 ECDSA to match the encryption policy, and aligned the identity-management password rules (20-character minimum for privileged accounts, no reuse of the last 12) to the authoritative password standard. An MFA-scope divergence and two developer-guidance crypto tables that still allow P-256 were routed for maintainer decision.

**2026-07-14 | 2026.07.392 | PR #904** - Resolved conflicting vulnerability-remediation deadlines, where different documents set different timelines for the same severity, by making the vulnerability-management procedure the single source of truth (High 14, Medium 30, Low 90 days, with the Critical tier graded from 24 hours to 7 days by exploitation status) and converting the software-composition-analysis standard and developer-security requirements to cite it rather than restate their own looser values. A corpus-wide check confirmed no other document still diverged.

**2026-07-14 | 2026.07.391 | PR #903** - Reconciled the internal-audit standard's reporting structure to the corpus's canonical governance: internal audit now reports functionally to the Board Audit Committee (administrative line to senior leadership, with a fallback where no separate committee exists) and routes annual-plan approval and material-finding escalation to that committee. This resolves a deep-assessment finding that the standard had named only the Enterprise Risk Committee while the compliance policy and assurance map already assumed the audit-committee line.

**2026-07-14 | 2026.07.390 | PR #902** - Corrected the OWASP ASVS cross-references across the developer-security documents and the rules pack from the superseded 4.0.3 numbering to the current 5.0.0 scheme, which reorganized every chapter. Applied under the high-assurance process (two research passes, two independent adversarial checks that found no missed or wrong mappings, and a scripted apply); the generic governance-rule citations with no clean 5.0.0 equivalent were deferred to a separate maintainer-decided pass.

**2026-07-14 | 2026.07.389 | PR #901** - First PR of the resumed session: ran corpus-wide validation Sweep 102 over the prior session's deep-assessment round-3 changes (#887-#900), found it clean, and fixed one bookkeeping omission (PR #900's missing handoff-exemption row); housekeeping only, nothing adopter-facing changed.

**2026-07-14 | 2026.07.388 | PR #900** - Session-closing handoff for the 2026-07-13 session, plus a two-document follow-on correction completing the DORA article fix corpus-wide (Article 11, not 12, holds the ICT business-continuity policy in two business-continuity plans); housekeeping plus a label correction, nothing else adopter-facing changed.

**2026-07-13 | 2026.07.387 | PR #899** - Applied the maintainer-signed-off clear-mechanical remediation batch from the round-3 deep assessment: six small adopter-facing corrections (portal Board/CEO audience listing, implementation-roadmap composition pointer, a stale Mexico-annex note, the retired FFIEC assessment tool, a DORA article label, and an AI Act attribution), with the two High findings and the OWASP ASVS remap deferred to a fresh session.

**2026-07-13 | 2026.07.386 | PR #898** - Consolidated the round-3 deep assessment (Phase 7 routing) and presented the complete finding set for maintainer sign-off (Phase 8), with phases 1 to 7 now complete; the assessment holds for explicit sign-off with none of its findings acted on yet, so no adopter-facing content changed.

**2026-07-13 | 2026.07.385 | PR #897** - Completed Phase 6 of the round-3 deep assessment (adoptability, CI-pipeline integrity, and QA-ledger honesty, all found sound) and applied its one small fix, pinning two nightly-workflow actions by exact commit to match the main workflow; nothing adopter-facing changed.

**2026-07-13 | 2026.07.384 | PR #896** - Completed the round-3 deep assessment's dead-gate check (zero dead gates among the audit programme) and a ground-truth citation spot-check (16 of 20 faithful), recording three discrepancies for the maintainer, chiefly the systematic OWASP ASVS 5.0.0-baseline-versus-4.0.3-chapter-numbering mismatch; review only, nothing adopter-facing changed yet.

**2026-07-13 | 2026.07.383 | PR #895** - Ran the round-3 deep assessment's reference-breadth review, judging a high-value sample of the held sources against their text; use is strong, with two items routed to the maintainer (a current ETSI AI-security guidance held but uncited, and the retired FFIEC assessment tool still listed as current); review only, nothing adopter-facing changed yet.

**2026-07-13 | 2026.07.382 | PR #894** - Ran the round-3 deep assessment's fresh-reader fitness pass (ten reader personas) and surfaced 20 genuine cross-document consistency issues for the maintainer to decide, chiefly the internal-audit independence reporting line and divergent vulnerability-remediation deadlines; review only, nothing adopter-facing changed yet.

**2026-07-13 | 2026.07.381 | PR #893** - Ran the round-3 deep assessment's forensic quality pass (six reviewers); five came back clean and the sixth caught one citation-date defect, corrected here (an EU consent guideline's Version 1.1 is dated 13 May 2020, not 4 May); one small correction, nothing else adopter-facing changed.

**2026-07-13 | 2026.07.380 | PR #892** - Continued round 3 of the deep assessment with two semantic checks: publications-screening (nothing pending) and the whole-matrix control-fit check (all 84 non-obvious rows judged correct or defensibly supporting, zero wrong-control findings); process/housekeeping only, nothing adopter-facing changed.

**2026-07-13 | 2026.07.379 | PR #891** - Continued round 3 with the claim-fit citation-precision check (Canada's 24-month breach-record retention confirmed accurate) and completed the prior PR's documentation fix by correcting two more internal docstrings that still described the old changelog style; process/housekeeping only, nothing adopter-facing changed.

**2026-07-13 | 2026.07.378 | PR #890** - Ran the round-3 deep assessment's structural-integrity (guardrail) review of the governance machinery, finding rules, skills, and gates cleanly and deliberately layered, and corrected three internal descriptions (including the audit-programme specification) still describing the old changelog-header style.

**2026-07-13 | 2026.07.377 | PR #889** - Advanced the round-3 deep assessment's checks on the audit programme itself: the gate blind-spot map came back clean and a mutation probe confirmed detection width intact (15 planted defects all caught, 5 clean controls all passed); process/housekeeping only, nothing adopter-facing changed.

**2026-07-13 | 2026.07.376 | PR #888** - Opened round 3 of the whole-project deep assessment (maintainer-invoked, terminating only on sign-off): re-derived the live quality-machinery inventory, confirmed the mechanical baseline green across the library and both companion repositories, and recorded the run so it can resume across sessions; process/housekeeping only, nothing adopter-facing changed.

**2026-07-13 | 2026.07.375 | PR #887** - First PR of the resumed session: ran corpus-wide validation Sweep 101 over the prior session's changes (#852-#886), found it clean, and routed one low-risk note (the held AICPA Trust Services Criteria copy is an earlier edition than the cited version, though the citation itself is accurate); housekeeping only, nothing adopter-facing changed.

**2026-07-13 | 2026.07.374 | PR #886** - Session-closing handoff: refreshed the resume record (state snapshot, asserted-clean expectations, and a next-session queue that leads with the deep-assessment components the maintainer asked for on resume), added the session-metrics row, and released the concurrency lease. Housekeeping only; per the loop-break convention this closing PR takes no trailing per-PR quality sweep, because the next resume runs a full corpus-wide validation instead.

**2026-07-13 | 2026.07.373 | PR #885** - Housekeeping: removed 38 stale merged worker-exchange branches from the scratch repository (each verified to have a merged pull request, so its content is preserved on the scratch main branch and in history), completing the scratch cleanup the delivery reconciliation left open, and folded in the prior PR's post-merge quality-check results. Nothing adopter-facing changed.

**2026-07-13 | 2026.07.372 | PR #884** - Housekeeping: recorded the results of the read-only quality-system self-checks run per the maintainer's direction to run the appropriate parts of a deep assessment (the gate coverage map came back clean; the delivery pipeline is in its expected state), routed the heavier assessment parts to a future fresh-session run, and folded in the prior PR's post-merge quality-check results. Nothing adopter-facing changed.

**2026-07-13 | 2026.07.371 | PR #883** - Cited Brazil's ANPD fine-calculation regulation (Resolution CD/ANPD No. 4/2023, the Dosimetry and Application of Sanctions rule) in the Brazil privacy annex's enforcement section and added it to the citation register, so the annex explains how a fine's base value is set rather than only listing the statutory ceilings; confirmed current against the ANPD this session. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.370 | PR #882** - Cited the EU regulator's guidelines on identifying a company's lead data-protection supervisory authority (EDPB Guidelines 8/2022) in the EU privacy annex's one-stop-shop description and added them to the citation register, so the annex points to the actual main-establishment test rather than asserting it unsourced; confirmed current against the EDPB this session (Version 2.1, superseding the older WP244 guidance). This applies the last of the version-sensitive reference-breadth citations queued for this session. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.369 | PR #881** - Named the EU implementing regulation that sets NIS2's technical cybersecurity requirements and significant-incident thresholds (Commission Implementing Regulation (EU) 2024/2690) in the NIS2 implementation annex and citation register, with a clear note that it binds only certain digital-service and digital-infrastructure providers rather than all NIS2 entities, and corrected a wrong article reference in the annex's framework table; confirmed current against EUR-Lex this session. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.368 | PR #880** - Cited the EU regulator's opinion on personal data in AI models (EDPB Opinion 28/2024) in the privacy policy's AI-training-data section, pointing to the authoritative guidance on when AI training has a lawful basis and when a model can be considered anonymous; the opinion was already in the citation register, so its currency was re-confirmed this session and its verification date refreshed. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.367 | PR #879** - Cited Canada's Breach of Security Safeguards Regulations (SOR/2018-64) in the Canada privacy annex's breach section and added it to the citation register, capturing the 24-month breach-record retention duty and the prescribed report/notification content that the statute alone does not spell out; confirmed current against the Justice Laws site this session. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.366 | PR #878** - Cited Brazil's ANPD data-protection-officer regulation (Resolution CD/ANPD No. 18/2024) in the Brazil privacy annex's DPO section and added it to the citation register, so the annex points to the specific rule governing the encarregado's appointment and duties rather than the statute alone; confirmed current against the ANPD this session. Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.365 | PR #877** - Named the EU Commission's standard contractual clauses for controllers and processors (Commission Implementing Decision (EU) 2021/915) in the Article 28 data-processing-agreement template and added it to the citation register, so adopters have the specific clause set to reference; confirmed current against EUR-Lex this session, with an explicit note that this set is for the processing contract, not for cross-border transfers (a different clause set). Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.364 | PR #876** - Added the AICPA Trust Services Criteria (the SOC 2 subject-matter criteria) to the internal citation register, closing a genuine gap where those criteria were cited across the library but missing from the register that tracks citation currency. The current version was confirmed against the publisher's own page this session (the 2017 criteria with revised points of focus from 2022). Also folded in the prior PR's post-merge quality-check results.

**2026-07-13 | 2026.07.363 | PR #875** - Closed the worker-delivery reconciliation backlog item: applied the maintainer's disposition rule to the research-exchange deliveries (for anything older than five days, keep only pure-research seeds and discard the consumed or stale rest), recorded the residual tooling weakness for follow-up, and folded in the prior PR's post-merge quality-check results. Housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.362 | PR #874** - Recorded the reference-breadth citation work's status: the freely-verifiable EU-regulator guideline citations are all applied, and the remaining version-sensitive sources (including a genuine gap where a widely-cited assurance framework is missing from the internal citation register) are queued for maintainer review. Housekeeping only.

**2026-07-13 | 2026.07.361 | PR #873** - Added the EU regulator's guidance on certification as a data-transfer tool (EDPB Guidelines 07/2022) as a citation in the transfer-impact-assessment template, pointing to the authoritative source for that specific transfer mechanism's analysis.

**2026-07-13 | 2026.07.360 | PR #872** - Recorded two internal assessments in the backlog: a queued test-tooling fix turned out bigger than first scoped, and a small cosmetics cleanup is best done in an attended pass. Housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.359 | PR #871** - Added the same read-only workspace safety rule to the distributable governance pack (it was previously only in the project's own config), so teams adopting the pack inherit it. Internal tooling guidance; nothing adopter-facing in the corpus changed.

**2026-07-13 | 2026.07.358 | PR #870** - Added an internal safety rule so background review helpers only read version history, never switch branches, in the shared workspace. This prevents a rare mix-up (seen once and repaired) where a helper's branch switch could misplace a commit. Nothing adopter-facing changed.

**2026-07-13 | 2026.07.357 | PR #869** - Added the EU regulator's official breach-notification guidance (EDPB Guidelines 9/2022) as a citation in the breach-response procedure, completing the set of EU privacy-by-design, consent, access, and breach guideline citations.

**2026-07-13 | 2026.07.356 | PR #868** - Added the EU regulator's official guidance on the right of access (EDPB Guidelines 01/2022) as a citation in the data-subject-rights procedure, anchoring its third-party-redaction and manifestly-unfounded-request rules to the authoritative interpretation.

**2026-07-13 | 2026.07.355 | PR #867** - Added the EU regulator's official consent guidance (EDPB Guidelines 05/2020) as a citation in the consent-management framework, anchoring the document's consent-validity standard to the authoritative interpretation.

**2026-07-13 | 2026.07.354 | PR #866** - Added the EU regulator's official guidance on privacy by design (EDPB Guidelines 4/2019) as a citation in the privacy-by-design framework, so the document points to the authoritative interpretation of the GDPR Article 25 duty it operationalizes.

**2026-07-13 | 2026.07.353 | PR #865** - Tidied an internal how-to so the changelog authoring instructions point at the new compact one-line format, and recorded a maintainer follow-up to reconcile some older queued research deliveries. Nothing adopter-facing changed.

**2026-07-13 | 2026.07.352 | PR #864** - Documented the compact one-line changelog format as the project's standard going forward, now that the whole history has been converted to it. This is an internal authoring-convention note; nothing adopter-facing changed.

**2026-07-13 | 2026.07.351 | PR #863** - Fixed an inaccuracy in the project's internal reference-review guidance: a NIST document (SP 800-154) that was never finalized had been described as one the project holds, and is now described accurately as a relevant but unavailable source. No adopter-facing corpus content changed.

**2026-07-13 | 2026.07.350 | PR #862** - Converted the last of the older changelog entries to short summaries, completing the plain-language rework of the whole history; every entry is now a short summary a general reader can follow.

**2026-07-13 | 2026.07.349 | PR #861** - Converted another 120 older changelog entries to short summaries; only the earliest entries now remain in the long form.

**2026-07-13 | 2026.07.348 | PR #860** - Converted the next 120 older changelog entries to short summaries (the plain-language rework nears the end of the history).

**2026-07-13 | 2026.07.347 | PR #859** - Converted the next 120 older changelog entries (a further stretch of the plain-language rework) to short summaries.

**2026-07-13 | 2026.07.346 | PR #858** - Converted the next 120 older changelog entries to plain-language summaries, and expanded the backlog item for an adopter reference-base specification (public and paid source lists plus a corpus-to-sources relevance map).

**2026-07-13 | 2026.07.345 | PR #857** - Continued the plain-language changelog rework, converting the next 120 older entries to short summaries, and updated the changelog's own description of its format.

**2026-07-13 | 2026.07.344 | PR #856** - Rewrote the changelog's most recent entries as short, plain-language summaries a general reader can follow, keeping the full detail in the maintainer archive.

**2026-07-12 | 2026.07.343 | PR #855** - Internal reformatting of the changelog's historical entry headers to a shorter, uniform style, with no change to what the entries say.

**2026-07-12 | 2026.07.342 | PR #854** - Internal correction to the AI-assistant's instructions for waiting on automated checks, plus routine post-merge quality bookkeeping.

**2026-07-12 | 2026.07.341 | PR #853** - Internal maintenance to the AI-assistant's process notes on how it waits for automated checks to finish.

**2026-07-12 | 2026.07.340 | PR #852** - Routine corpus-wide validation review at the start of a work session; findings were minor and no published document changed.

**2026-07-12 | 2026.07.339 | PR #851** - Routine end-of-session handoff bookkeeping; no published document changed.

**2026-07-12 | 2026.07.338 | PR #850** - In the AI algorithmic-compliance checklist, an imprecise pointer to a specific clause of the IEEE 7000-2021 ethics standard was removed while the standard is kept as a general input. A separate check confirmed that the Canada Treasury Board automated-decision directive dates already in the corpus were current, so no other change was needed.

**2026-07-12 | 2026.07.337 | PR #849** - The AI model-documentation-and-transparency framework now incorporates the EU General-Purpose AI Code of Practice transparency chapter and its model documentation form, mapping that form's fields onto the corpus model-card sections. A provider of a general-purpose AI model can therefore satisfy the EU form by maintaining an extended model card.

**2026-07-12 | 2026.07.336 | PR #848** - Internal update to the AI-assistant workflow notes about keeping the upcoming-work list current.

**2026-07-12 | 2026.07.335 | PR #847** - The training-data-governance procedure and the AI compliance policy now incorporate the EU General-Purpose AI Code of Practice copyright chapter, covering copyright-compliance policy, lawful web crawling, and honouring machine-readable text-and-data-mining opt-outs. This gives adopters concrete copyright-duty guidance for organizations that provide general-purpose AI models.

**2026-07-12 | 2026.07.334 | PR #846** - Internal close-out and acceptance review of the programme that makes the AI-assistant governance rule pack reusable by outside adopters.

**2026-07-12 | 2026.07.333 | PR #845** - Internal restructuring of the AI-assistant governance rule pack to remove project-specific references so it is cleaner for outside adopters.

**2026-07-12 | 2026.07.332 | PR #844** - Three AI documents (foundation-model lifecycle, agentic-development security, and model-risk framework) now incorporate the EU General-Purpose AI Code of Practice safety-and-security chapter, including model-weight-security controls and systemic-risk expectations. The material is framed as the provider expectation an adopter can require of its AI suppliers, with a direct duty only where the organization's own model reaches that scale.

**2026-07-12 | 2026.07.331 | PR #843** - The EU jurisdiction annex and the AI compliance policy now reflect the European Commission's official guidelines on the definition of an AI system and on prohibited AI practices, including the seven-element definition test and the eight prohibited-practice categories. These are cited as non-binding interpretive guidance, with the binding rules anchored to the EU AI Act itself.

**2026-07-12 | 2026.07.330 | PR #842** - Internal work to generalize the AI-assistant governance rule pack's skills so they read as portable procedures for outside adopters.

**2026-07-12 | 2026.07.329 | PR #841** - Internal housekeeping: a maintainer-only file was marked as ignorable by adopters and two already-resolved backlog notes were cleared, with no published document changed.

**2026-07-12 | 2026.07.328 | PR #840** - Internal correction of an ISO 27001 control reference in two AI-assistant governance rules.

**2026-07-12 | 2026.07.327 | PR #839** - Internal tooling change adding support for project-specific overlay blocks in the local rule copies.

**2026-07-12 | 2026.07.326 | PR #838** - Internal cleanup of framework-reference labels and condensing of AI-assistant governance rules.

**2026-07-12 | 2026.07.325 | PR #837** - Internal condensing of several AI-assistant governance rules, moving background narrative out of the operative text.

**2026-07-12 | 2026.07.324 | PR #836** - Internal condensing of four more AI-assistant governance rules.

**2026-07-12 | 2026.07.323 | PR #835** - Internal condensing of four AI-assistant governance rules, moving explanatory narrative to an archive.

**2026-07-12 | 2026.07.322 | PR #834** - The financial-services sector-requirements annex now states both statutory bounds of the EU DORA major-incident initial-notification window (within 4 hours of classifying an incident as major, and no later than 24 hours from awareness), correcting a cell that gave only one. The intermediate and final reporting anchors and the governing EU regulation are also made precise, matching the dedicated DORA annex.

**2026-07-12 | 2026.07.321 | PR #833** - Routine overnight-session handoff bookkeeping; no published document changed.

**2026-07-12 | 2026.07.320 | PR #832** - Internal addition to an AI-assistant governance rule covering what to do when a needed reference source is not held.

**2026-07-12 | 2026.07.319 | PR #831** - Several ISO/IEC 42001 clause references in five AI jurisdiction annexes, and ISO/IEC 27001 clause references in the compliance matrix, were remapped to their correct clauses, and a note about the ISO/IEC 30111 vulnerability-handling standard in the vulnerability-management procedure was reworded to stop overstating that procedure's scope. These are citation-accuracy corrections, not changes to the underlying requirements.

**2026-07-12 | 2026.07.318 | PR #830** - Three documents gained supplementary references: the vulnerability-management procedure now notes ISO/IEC 30111, the threat-modelling standard notes the MITRE attack-pattern catalogue, and the backup-and-recovery procedure notes the NIST ransomware profile. Each is offered as an optional or supporting input, not a new mandatory requirement.

**2026-07-12 | 2026.07.317 | PR #829** - The DORA implementation annex's major-incident reporting windows were corrected and made precise against the governing EU technical standards, now stating both the 4-hour and 24-hour initial-notification bounds plus the intermediate and final report deadlines. The exact EU regulations and DORA articles for classification, reporting, and templates are now cited.

**2026-07-12 | 2026.07.316 | PR #828** - Routine start-of-session validation review; the few findings were minor and confined to internal tool notes, with no published document changed.

**2026-07-12 | 2026.07.315 | PR #827** - Routine session-closing handoff recording a maintainer sign-off on a whole-project review; no published document changed.

**2026-07-12 | 2026.07.314 | PR #826** - A governance framework document's ISO 37001 wording was softened from claiming compliance to describing alignment, and the repository structure map in the README was expanded to list more of its contents. These improve the accuracy of an anti-bribery conformance claim and the orientation a reader gets from the README.

**2026-07-12 | 2026.07.313 | PR #825** - A mislabeled ISO/IEC 42001 clause (whose actual title is AI system impact assessment) was corrected across seven AI framework-alignment tables and two related cross-reference documents, re-pointing documentation and operational rows to the correct clauses. This is a citation-accuracy fix affecting how those AI documents map to the standard.

**2026-07-11 | 2026.07.312 | PR #824** - Internal addition of an audit check that flags fragile backlog references in scanned prose; no published document requirement changed.

**2026-07-11 | 2026.07.311 | PR #823** - Internal record of a whole-project review awaiting maintainer sign-off; no published document changed.

**2026-07-11 | 2026.07.310 | PR #822** - Routine session-resume validation review that surfaced no issues; no published document changed.

**2026-07-11 | 2026.07.309 | PR #821** - Routine session-closing handoff and backlog consolidation; no published document changed.

**2026-07-11 | 2026.07.308 | PR #820** - Every remaining neutral listing of Canada's lapsed Artificial Intelligence and Data Act in the governance and security documents is now annotated as lapsed, completing a uniformity pass across the corpus. This ensures adopters do not read the lapsed proposal as a current obligation.

**2026-07-11 | 2026.07.307 | PR #819** - Internal addition to the AI-assistant close-out guidance on checking every form a closed reference is cited by.

**2026-07-11 | 2026.07.306 | PR #818** - Internal reference-repository corrections and a citation-register date sync; the substantive title and date fixes were made in the separate reference repository.

**2026-07-11 | 2026.07.305 | PR #817** - Internal advisory tool added to flag drift between the reference repository's currency records and the citation register.

**2026-07-11 | 2026.07.304 | PR #816** - Internal backlog bookkeeping closing a completed AI workstream; no published document changed.

**2026-07-11 | 2026.07.303 | PR #815** - A new framework document on AI value and decision governance was created, treating the value an organization pursues from AI and the quality of its AI decisions as governance evidence. It adds a value-maturity ladder, decision-record expectations, and a benefits taxonomy, cross-referencing existing AI ownership, KPI, audit, and cost documents rather than duplicating them.

**2026-07-11 | 2026.07.302 | PR #814** - Internal backlog bookkeeping and reference repointing; no published document body changed.

**2026-07-11 | 2026.07.301 | PR #813** - Internal documentation of the detailed changelog's current-week archiving model across the governance rule pack and workflow notes.

**2026-07-11 | 2026.07.300 | PR #812** - Internal addition to the AI-assistant guidance requiring completion searches to span all file types.

**2026-07-11 | 2026.07.299 | PR #811** - Internal backlog and workflow-note bookkeeping; no published document changed.

**2026-07-11 | 2026.07.298 | PR #810** - Canada's lapsed Artificial Intelligence and Data Act was still mapped as a live privacy-impact obligation in three privacy documents and hedged as pending in two governance registers; these were reconciled to the in-force instruments, Quebec Law 25 for the private sector and the federal Treasury Board automated-decision directive for federal institutions. This corrects the Canadian AI privacy-impact obligation adopters would rely on.

**2026-07-11 | 2026.07.297 | PR #809** - A new guideline on synthetic-content provenance was created, covering how to mark, detect, and disclose AI-generated output, anchored to the NIST synthetic-content report and the EU AI Act transparency obligation. It fills the technical how-to gap between the corpus's existing labelling policy and its regulatory statements.

**2026-07-11 | 2026.07.296 | PR #808** - Internal addition of an audit check that detects malformed nested markdown links; no published document requirement changed.

**2026-07-11 | 2026.07.295 | PR #807** - Internal repair of malformed links in historical changelog entries, plus a one-word consistency tweak to a security-baseline classification.

**2026-07-11 | 2026.07.294 | PR #806** - Across eight documents, Canada's lapsed Artificial Intelligence and Data Act and the rescinded US Executive Order 14110 were reworded from current obligations to their lapsed or rescinded status, citing the in-force Canadian directive and voluntary code instead. This prevents adopters from treating superseded instruments as live compliance targets.

**2026-07-11 | 2026.07.293 | PR #805** - Two privacy jurisdiction annexes were corrected: the Australia annex now states the accurate automated-decision transparency obligation and its 2026 commencement, and the Canada annex reframes the lapsed Bill C-27 proposals from anticipated to lapsed. This aligns the privacy annexes with the accurate framing used elsewhere in the corpus.

**2026-07-11 | 2026.07.292 | PR #804** - The citation year for the OECD AI Principles was harmonized to its current form (2019, updated 2024) across five AI documents. This corrects a stale revision year adopters would see in those documents.

**2026-07-11 | 2026.07.291 | PR #803** - The AI incident-response plan and the AI inference-cost-governance standard were deepened against held sources, adding an adversarial-attack taxonomy crosswalk, recognized incident-reporting channels, and a security-grounded rationale for cost ceilings. This gives adopters richer, standard-anchored operational guidance in those two areas.

**2026-07-11 | 2026.07.290 | PR #802** - The Canada and Australia AI instruments cited in the new jurisdiction annexes were enrolled in the canonical-citations register so their currency can be tracked, and several authoritative publisher domains were added to the link allow-list. This lets the corpus flag those instruments if they later change.

**2026-07-11 | 2026.07.289 | PR #801** - A new Australia AI jurisdiction annex was created, presenting Australia's voluntary, principles-based AI governance (the AI Ethics Principles, Voluntary AI Safety Standard, adoption guidance, and national plan) and its one binding automated-decision transparency duty under the Privacy Act. Each instrument's status as voluntary, strategy, or binding is stated accurately.

**2026-07-11 | 2026.07.288 | PR #800** - A new Canada AI jurisdiction annex was created, presenting Canada's patchwork AI governance (the binding federal automated-decision directive and its impact assessment, voluntary codes, and provincial and sector instruments) and noting that the proposed federal AI statute lapsed. It also corrects the in-force date framing of the federal directive in the AI system-impact-assessment procedure.

**2026-07-11 | 2026.07.287 | PR #799** - A new New York City jurisdiction annex was created covering the Local Law 144 automated-employment-decision-tool bias-audit law, including the annual audit, published-results, and candidate-notice requirements. A related citation-register row and cross-references were added, and an OECD principles citation year was corrected.

**2026-07-11 | 2026.07.286 | PR #798** - A new director-facing guide was created for board-level oversight of an organization's AI use, filling the gap left by the existing executive-level AI charters. It covers director duties, board AI literacy, risk appetite, a director question set, red flags, and reporting expectations, grounded in ISO and NIST AI-governance standards.

**2026-07-11 | 2026.07.285 | PR #797** - Four AI governance and ethics documents were expanded to add safety and environmental sustainability as first-class concerns and to anchor them to ISO, OECD, UNESCO, and NIST AI standards. The governance framework, AI risk register, ethics guideline, and ethics-panel charter each gained new domains, categories, or principles with standard-based alignment.

**2026-07-11 | 2026.07.284 | PR #796** - A new AI maturity-model framework was created to back the AI Governance Council's maturity measure, built as the AI-specific application of the corpus's existing maturity methodology with eight assessment domains. Its practices are adapted from the OWASP AI Maturity Assessment with attribution.

**2026-07-11 | 2026.07.283 | PR #795** - Eight AI security documents were anchored to the flagship ETSI baseline cyber-security standard and to further NIST and CSA AI-security sources, adding alignment content on asset inventory, least privilege, supply chain, adversarial testing, and agent security. Vendor and red-team templates also gained new alignment rows and questions.

**2026-07-11 | 2026.07.282 | PR #794** - Seven AI documents on testing, evaluation, transparency, and audit or certification were deepened against ISO and NIST standards, restructuring the transparency model, adding fairness and explainability methods, and grounding external certification in the ISO certification-body standard. The model-card and system-card templates gained fields for compute cost, environmental footprint, bias sources, and user controllability.

**2026-07-11 | 2026.07.281 | PR #793** - The seven model-risk documents were matured against the OSFI model-risk guideline and ISO and NIST AI standards, adding inherent-versus-residual risk rating, independent model-review triggers, automated-rollback requirements, and expanded model-registry inventory fields. This deepens the corpus's model-risk-management guidance for adopters.

**2026-07-11 | 2026.07.280 | PR #792** - A new AI data-quality and readiness-validation standard was created, setting the data-quality model, measures, lifecycle validation gates, and a sign-off gate a dataset must pass before large-scale training or use, grounded in ISO data-quality standards. Consuming documents (the training-data procedure and the dataset and system-register templates) were wired to it with new gates and fields.

**2026-07-11 | 2026.07.279 | PR #791** - The AI impact-assessment documents were matured against ISO/IEC 42005 and the integrated AI-and-privacy assessment router was generalized beyond the EU to add Canada and US limbs. New content includes a harms-and-benefits analysis, an operational impact-scoring model, and added checklist items.

**2026-07-11 | 2026.07.278 | PR #790** - Routine session-resume validation review plus acquisition of previously unheld reference sources into the reference repository; no published document changed.

**2026-07-10 | 2026.07.277 | PR #789** - Routine session-closing handoff summarizing the session's work; no published document changed.

**2026-07-10 | 2026.07.276 | PR #788** - Internal routing of seven unheld citations to the maintainer's acquisition queue; the references were confirmed accurate and left in place, with no published document changed.

**2026-07-10 | 2026.07.275 | PR #787** - The EU AI Act serious-incident reporting deadline was corrected corpus-wide from a wrong 15 business days to the statutory 15 days, adding the two shorter sub-deadlines the corpus had omitted, across three AI documents. A related general-purpose-AI computing threshold was confirmed against the Act with no change.

**2026-07-10 | 2026.07.274 | PR #786** - A misattributed citation (ISO/PAS 8800, which is actually a road-vehicle AI-safety specification rather than a responsible-innovation standard) was corrected across several documents, re-anchoring the responsible-AI-principles claims to the OECD, UNESCO, and Canadian ethics sources. This fixes a citation that was wrong on year, title, and subject.

**2026-07-10 | 2026.07.273 | PR #785** - The AI compliance policy's Canada content was reconciled to reflect that the proposed federal AI statute lapsed, aligning to the in-force federal directive and voluntary code, and a new section on US state and municipal AI laws (Colorado and New York City) was added. This corrects contradictory Canada framing and fills a US-state coverage gap.

**2026-07-10 | 2026.07.272 | PR #784** - In the AI and agentic-development security standard, a column of invalid, invented CSA control codes was remapped to real, verified CSA AI control-model controls across all its rows. This corrects control-code citations that looked valid but referenced nothing real.

**2026-07-10 | 2026.07.271 | PR #783** - Internal test-coverage addition for an audit check, plus a tool-comment wording fix; no published document changed.

**2026-07-10 | 2026.07.270 | PR #782** - Internal hardening of a control-code citation check and a fix to invalid control codes in two AI-assistant governance pack documents.

**2026-07-10 | 2026.07.269 | PR #781** - Control-code citations were re-anchored to their better-fitting CSA controls across six documents and the compliance matrix, and two genuine misattributions (an entire invalid endpoint control-code family and a key-destruction code) were corrected. All changes were verified against the held control catalogue.

**2026-07-10 | 2026.07.268 | PR #780** - Routine start-of-session validation review; the findings were confined to internal tool notes, with no published document changed.

**2026-07-10 | 2026.07.267 | PR #779** - End-of-session handoff bookkeeping only; no published document changed.

**2026-07-10 | 2026.07.266 | PR #778** - Internal reference-currency reconfirmation marking the EN 54 fire-detection standard series as verified in the citation register.

**2026-07-10 | 2026.07.265 | PR #777** - A citation error was corrected: an aviation-security reference wrongly given as ICAO Doc 10026 (which is actually a legal-commission report) was replaced with the correct, publicly citable ICAO Annex 17, in the citation register and the logistics sector annex. This fixes a wrong standard reference adopters would have followed.

**2026-07-10 | 2026.07.264 | PR #776** - Four dev-security, metrics, workforce, and cloud documents gained authoritative NIST and ISO citations, and two citation-precision fixes were applied (a corrected zero-trust title and a resolved cloud-controls registration). These strengthen the standard references adopters can rely on.

**2026-07-10 | 2026.07.263 | PR #775** - Six AI documents gained authoritative AI-governance, lifecycle, data, bias, transparency, and adversarial-attack standard citations from ISO and NIST. These add relevant held-source references the documents had not previously engaged.

**2026-07-10 | 2026.07.262 | PR #774** - Four resilience and enterprise-architecture documents gained NIST trustworthy-systems and cyber-resilience citations and an ISO storage-security citation. These add relevant authoritative references adopters can follow.

**2026-07-10 | 2026.07.261 | PR #773** - The security incident-response procedure gained NIST recovery and forensics citations and an ISO digital-evidence citation, closing a cross-reference gap with the privacy breach-response procedure. These strengthen the recovery and evidence-handling references.

**2026-07-10 | 2026.07.260 | PR #772** - Four identity-and-access-management documents gained ISO and NIST identity-management, access-management, identity-proofing, and cloud-access-control citations. These add authoritative references the identity documents had not engaged.

**2026-07-10 | 2026.07.259 | PR #771** - Three privacy documents gained ISO privacy-framework and personal-data-protection citations plus NIST privacy-engineering and differential-privacy citations. These add relevant authoritative references to the privacy guidance.

**2026-07-10 | 2026.07.258 | PR #770** - Three risk-management documents gained authoritative risk-technique and enterprise-risk citations from IEC and NIST. These add held-source references complementing the standards the documents already cite.

**2026-07-10 | 2026.07.257 | PR #769** - A semantic-fit review of framework-alignment tables corrected twelve valid-but-wrong control-code mappings across several security and operations documents, and an entire invalid control-code family cited as CSA controls was remapped to real controls. These are control-code accuracy corrections verified against the held catalogue.

**2026-07-10 | 2026.07.256 | PR #768** - Internal expansion of the audit-check testing library; no published document changed.

**2026-07-10 | 2026.07.255 | PR #767** - Internal continuous-integration workflow hardening with least-privilege permissions and pinned action versions.

**2026-07-10 | 2026.07.254 | PR #766** - Internal fix to the navigation-portal generator so AI jurisdiction annexes and the reverse crosswalk are listed for the compliance audience.

**2026-07-10 | 2026.07.253 | PR #765** - Internal update adding the publications-screening step to the whole-project review's instrument set in the governance pack.

**2026-07-10 | 2026.07.252 | PR #764** - Internal improvement to the document-date staleness check so it also catches future-dated documents.

**2026-07-10 | 2026.07.251 | PR #763** - Small accuracy fixes were applied: the US Colorado entry in the privacy jurisdiction index was refreshed to name the operative forward regime, a SOC 2 disclosure row was added to the coverage-gaps register, and some internal self-links were canonicalized. These keep the privacy and coverage references accurate for adopters.

**2026-07-10 | 2026.07.250 | PR #762** - Internal mining of the improvement and metrics logs to populate the backlog; no published document changed.

**2026-07-10 | 2026.07.249 | PR #761** - A start-of-session validation review corrected an EU AI Act article citation in the legal-and-regulatory-compliance policy, aligning a table row to Article 73 along with several internal reference fixes. This completes an accuracy correction begun in an earlier change.

**2026-07-10 | 2026.07.248 | PR #760** - Session-closing handoff following a whole-project review; no published document changed.

**2026-07-10 | 2026.07.247 | PR #759** - Three regulatory-mapping rows in the compliance matrix were corrected to use the on-point regulatory-mapping control code where off-subject codes had been used. This is a control-code accuracy fix in the matrix.

**2026-07-10 | 2026.07.246 | PR #758** - Two attribution-precision fixes were applied: the EU AI Act serious-incident citation in a compliance policy was narrowed to the correct article, and a governance framework's review-cadence wording was corrected to reflect that ISO 27001 prescribes review at planned intervals rather than a fixed annual cadence. These sharpen how the sources are attributed.

**2026-07-10 | 2026.07.245 | PR #757** - Stale EU AI Act structure references were corrected corpus-wide from the old proposal-era Title numbering to the enacted regulation's Chapter numbering across four documents. This fixes outdated citations to the AI Act's structure.

**2026-07-10 | 2026.07.244 | PR #756** - Internal restructuring of the backlog file so each item is one action; no published document changed.

**2026-07-10 | 2026.07.243 | PR #755** - A stale privacy-jurisdiction count was corrected from 25 to 26 across three navigation surfaces after a new jurisdiction annex was added. This keeps the coverage counts accurate for adopters.

**2026-07-10 | 2026.07.242 | PR #754** - Internal record of the first whole-project review and routing of its findings; no published document changed.

**2026-07-10 | 2026.07.241 | PR #753** - A validation review broadened the glossary's automated-decision-making-technology entry to note its use in California's privacy rules as well as Colorado's. This adds accuracy to a glossary definition adopters read.

**2026-07-10 | 2026.07.240 | PR #752** - Routine session-closing handoff; no published document changed.

**2026-07-09 | 2026.07.239 | PR #751** - A reference-currency sweep stamped dozens of citation-register entries as verified against their current versions and corrected five to their current instruments, cascading the World Customs Organization Framework update from its 2021 to 2025 edition across ten documents and updating NERC and TSA references. This brings the corpus's standard citations up to their current editions.

**2026-07-09 | 2026.07.238 | PR #750** - A new Mexico privacy jurisdiction annex was created for Mexico's 2025 personal-data-protection law, recording the changed regulator and the new penalty basis, and stale facts in the Latin America annex were corrected. This updates the corpus for a regime change adopters relying on Mexican privacy law need.

**2026-07-09 | 2026.07.237 | PR #749** - A new Colorado AI jurisdiction annex was created giving a two-regime view of Colorado's outgoing AI Act and incoming automated-decision-making law, with statutory duties, rights, and enforcement verified against the enacted texts. It was wired into the AI index, document index, decision tree, and glossary.

**2026-07-09 | 2026.07.236 | PR #748** - A validation review corrected a fabricated EU AI Act fine figure (from 1.5% to the correct 1%) in the EU privacy annex and cleared stale gap and absent claims in the decision tree that new annexes had made false. These fix real accuracy defects in published documents.

**2026-07-09 | 2026.07.235 | PR #747** - Session-closing handoff for the work session; no published document changed.

**2026-07-09 | 2026.07.234 | PR #746** - The Brazil privacy annex and breach-response procedure had their small-organization breach-deadline provisions upgraded to primary-source confirmation against the held official text, dropping the pending-verification notes, and a directive citation name was harmonized. This finalizes verified Brazilian breach-rule citations for adopters.

**2026-07-09 | 2026.07.233 | PR #745** - The whistleblower procedure's investigation-feedback ceiling was made operationally precise (feedback within a reasonable time not exceeding three months), now verified against the held EU Whistleblower Directive. This resolves a previously vague operational timeframe.

**2026-07-09 | 2026.07.232 | PR #744** - Bookkeeping-only change closing a backlog item as already satisfied; no published document changed.

**2026-07-09 | 2026.07.231 | PR #743** - A new EU AI Act jurisdiction annex was created, consolidating the corpus's scattered EU AI Act content into a single per-regime view of roles, risk tiers, provider and deployer duties, timeline, and penalties by cross-reference. It flags a pending, not-yet-adopted EU amendment as a tracked future change rather than treating it as law.

**2026-07-09 | 2026.07.230 | PR #742** - A new adopter guide on multi-entity adoption was created, adding guidance on adopting the library across a group or holding-company structure with three topologies and how versioning, role mapping, and jurisdictional layering behave per topology. It composes existing group-scope and versioning material rather than restating single-entity mechanics.

**2026-07-09 | 2026.07.229 | PR #741** - Bookkeeping-only quality-record corrections; no published document changed.

**2026-07-09 | 2026.07.228 | PR #740** - The EU electronic-identity and trust-services (eIDAS) annex was made discoverable by adding it to the decision-tree routing and a glossary entry, matching how its peer annexes are surfaced. This helps adopters find the annex through the corpus's navigation surfaces.

**2026-07-09 | 2026.07.227 | PR #739** - A new public-sector annex on the EU electronic-identification and trust-services framework (eIDAS2) was created, organized by role with by-role obligations for relying parties, trust-service providers, public bodies, and wallet providers, verified against the held regulation. It was wired into the public-sector index and document registers.

**2026-07-09 | 2026.07.226 | PR #738** - Five operational-precision fixes were applied across privacy, risk, supply-chain, resilience, and AI documents, replacing vague statements with concrete anchored ones (a harmonized data-subject-rights clock, an interim risk-containment authority, a tier-conditioned supplier remediation gate, continuity-metric derivation guidance, and an AI deployment-threshold obligation). One further item was deferred because its source was not yet held.

**2026-07-09 | 2026.07.225 | PR #737** - The NIS2 implementation annex gained two sections: how sector-specific EU law such as DORA displaces equivalent NIS2 obligations for financial entities, and the NIS2 supervision distinctions and administrative-fine floors. This completes the coordinated boundary between the NIS2 and DORA annexes.

**2026-07-09 | 2026.07.224 | PR #736** - The DORA implementation annex was deepened to operational sufficiency, adding detail on critical third-party ICT provider oversight, the register of contractual arrangements, threat-led penetration-testing scope, and how DORA relates to NIS2 as the more specific law. It cross-references existing supplier and exit instruments rather than duplicating them.

**2026-07-09 | 2026.07.223 | PR #735** - A new procedure was added that routes across four overlapping assessments a system can trigger at once (the GDPR data-protection impact assessment, the AI system impact assessment, the automated-decision register entry, and the EU AI Act fundamental-rights impact assessment), stating which are required for a given system and how they compose. It connects the existing register, template, and checklists to this router and treats the fundamental-rights assessment as a complement to, not a replacement for, the data-protection impact assessment.

**2026-07-09 | 2026.07.222 | PR #734** - The privacy impact and cross-border transfer procedure's EU section was deepened from a one-line placeholder into a full sequence for lawful international data transfers under the GDPR and the Schrems II ruling: a transfer-mechanism selection ladder, a six-step transfer risk assessment, supplementary measures, and a suspend-or-notify stop point. This gives adopters detailed operational EU transfer guidance matching the depth already present for China.

**2026-07-09 | 2026.07.221 | PR #733** - A new United States healthcare annex was added, mapping HIPAA into an operational regime: role determination, the Security and Privacy Rule safeguards, breach-notification mechanics and timelines, the tiered penalty structure, and a crosswalk to the library's controls. It gives US healthcare adopters a concrete HIPAA compliance map.

**2026-07-09 | 2026.07.220 | PR #732** - Adjusted the AI-assistant's wind-down and handoff guidance so session depth alone is not a reason to end a session.

**2026-07-09 | 2026.07.219 | PR #731** - A new healthcare procedure was added that operationalizes the HIPAA obligations tied to a clock or a required content (individual access, amendment, notice, six-year retention, the breach-determination test and notification deadlines, and business-associate agreement content). Adopters get executable, deadline-bearing HIPAA compliance steps.

**2026-07-09 | 2026.07.218 | PR #730** - Added an internal tool and discipline for reconciling the delivery pipeline's state from the record rather than from memory.

**2026-07-09 | 2026.07.217 | PR #729** - Internal tightening of a document-type consistency check plus minor reference-tool polish.

**2026-07-09 | 2026.07.216 | PR #728** - Widened the reference repository's binary-scan and orphan-detection coverage and cross-linked two internal tools.

**2026-07-09 | 2026.07.215 | PR #727** - Internal refinements to the governance rule pack's review and overlay-precedence conventions.

**2026-07-09 | 2026.07.214 | PR #726** - Began condensing the AI-assistant governance rules, moving background narrative to an archive while keeping the operative text.

**2026-07-09 | 2026.07.213 | PR #725** - Added a new AI-assistant governance rule covering session lifecycle and operating modes for multi-session work.

**2026-07-09 | 2026.07.212 | PR #724** - Added an internal environment-detection tool for session resume and refined an internal reference check.

**2026-07-09 | 2026.07.211 | PR #723** - In the integrity-and-trustworthiness principle document, two framework-alignment citations were corrected against the source texts: a Cloud Security Alliance audit-log control and an ISO/IEC 27001 records-protection control were re-pointed to the controls that actually fit. This corrects two control references in a published governance document.

**2026-07-09 | 2026.07.210 | PR #722** - Added a process, tool, and skill for screening untrusted third-party publications before they inform any work.

**2026-07-09 | 2026.07.209 | PR #721** - Routine start-of-session validation review during an overnight run; no published document changed.

**2026-07-09 | 2026.07.208 | PR #720** - Routine overnight-session closing handoff; no published document changed.

**2026-07-09 | 2026.07.207 | PR #719** - Several navigation and discoverability improvements were made to published materials: a routing row was added to the README's decision-tree table, a glossary legend entry was added for the library-maintainer role, and the navigation portal now includes a board and CEO audience section with a maturity tag on each entry. This helps adopters, including executive readers, find the right documents.

**2026-07-09 | 2026.07.206 | PR #718** - Added an advisory tool that lists cited standards the reference repository does not yet hold.

**2026-07-08 | 2026.07.205 | PR #717** - Added an internal consistency check that keeps the allowed document-type list in sync across the surfaces that enumerate it.

**2026-07-08 | 2026.07.204 | PR #716** - Added a start-side check so the AI-assistant does not rebuild work a pending delivery already covers, and repaired broken links in the maintainer's detailed changelog.

**2026-07-08 | 2026.07.203 | PR #715** - Added a small repository-root pointer file to help resume a work session where the resume command is not discovered.

**2026-07-08 | 2026.07.202 | PR #714** - Routine session-resume validation review, with minor fixes to an internal tool note and a document-type selection guidance bullet.

**2026-07-08 | 2026.07.201 | PR #713** - Routine session-closing handoff bookkeeping; no published document changed.

**2026-07-08 | 2026.07.200 | PR #712** - Propagated the newly added Principle document type across the internal lists, specifications, and hierarchy tables that enumerate document types.

**2026-07-08 | 2026.07.199 | PR #711** - A new governance document was added stating the library's guiding principle that accuracy, integrity, quality, and trust rank above speed, which ranks above cost, with each facet mapped to the AI-assurance frameworks (the NIST AI Risk Management Framework, ISO/IEC 42001, and ISO/IEC TR 24028). It also introduces a new Principle document type for the corpus.

**2026-07-08 | 2026.07.198 | PR #710** - Added an internal rule requiring the AI-assistant to verify a cited audit-check number before using it.

**2026-07-08 | 2026.07.197 | PR #709** - Fixed a maintainer-tool issue that had left broken links in internal index files after archiving.

**2026-07-08 | 2026.07.196 | PR #708** - Swept completed weeks of the maintainer's detailed changelog into the archive, keeping only the current week in-repo.

**2026-07-08 | 2026.07.195 | PR #707** - Added a recurring internal review skill that checks whether the corpus draws on the best available held sources.

**2026-07-08 | 2026.07.194 | PR #706** - Added an advisory tool measuring how well the corpus uses the reference sources the project holds.

**2026-07-08 | 2026.07.193 | PR #705** - Codified the accuracy-integrity-quality-over-speed-over-cost principle as the governance rule pack's top rule.

**2026-07-08 | 2026.07.192 | PR #704** - Completed an audit-check-number correction in changelog and working-state text that an earlier fix had left partial.

**2026-07-08 | 2026.07.191 | PR #703** - Corrected an audit-check number mislabeled in changelog and working-state text; no actual check changed.

**2026-07-08 | 2026.07.190 | PR #702** - Added a maintainer-invoked whole-project deep-assessment skill, command, and register.

**2026-07-08 | 2026.07.189 | PR #701** - Added two advisory tools that probe how well the audit checks themselves detect defects.

**2026-07-08 | 2026.07.188 | PR #700** - Routine session-resume validation review with one documentation-only audit-description update; no published document content changed.

**2026-07-08 | 2026.07.187 | PR #699** - Routine overnight-session closing handoff; no published document changed.

**2026-07-08 | 2026.07.186 | PR #698** - Batched routine post-merge quality bookkeeping and added a README catalogue row pointing to an adoption worked example.

**2026-07-08 | 2026.07.185 | PR #697** - A new narrative walkthrough was added following a fictional adopter from cloning the library through the first-day essentials and the first two phases of a rollout, with file-by-file decisions. It complements the existing ingestion walkthrough as a step-by-step adoption guide.

**2026-07-08 | 2026.07.184 | PR #696** - The Brazil privacy annex and the data-breach-response procedure were updated to reflect that Brazil's data-protection authority doubles the breach-notification deadlines for small-scale agents (to 6 and 40 business days), confirmed against the resolution text. This gives adopters the accurate small-agent deadlines, with a primary-source re-check still noted as pending.

**2026-07-08 | 2026.07.183 | PR #695** - Added the machinery for the current-week detailed-changelog model; no data was moved yet and no published document changed.

**2026-07-08 | 2026.07.182 | PR #694** - Follow-up wording fixes completing an organization-neutral terminology reframe in the quality-review materials; no published document content changed.

**2026-07-08 | 2026.07.181 | PR #693** - Clarified internal reference-handling documentation and retired an obsolete organization-specific contribution check.

**2026-07-07 | 2026.07.180 | PR #692** - Two citations to a never-finalized NIST draft on data-centric threat modelling were replaced with the OWASP Threat Modeling Cheat Sheet in the threat-modelling standard and the document index. Adopters now see a finalized, citable reference in place of an unpublished draft.

**2026-07-07 | 2026.07.179 | PR #691** - Six Brazilian statutory and regulatory citations were verified against their primary sources, and one year error was corrected (a standard-contractual-clauses resolution is from 2024, not 2023) in the Brazil privacy annex and the jurisdiction index. Pending-verification caveats were removed from the confirmed citations.

**2026-07-07 | 2026.07.178 | PR #690** - Overnight-run setup and accumulated bookkeeping flush; no published document changed.

**2026-07-07 | 2026.07.177 | PR #689** - Completed re-pointing internal tools and a runbook to the dedicated reference repository after the reference-library split.

**2026-07-07 | 2026.07.176 | PR #688** - Re-pointed corpus and internal references to the new dedicated reference repository; a location-and-name change only, with no content change.

**2026-07-07 | 2026.07.175 | PR #687** - Routine session-start validation review, with a trivial completeness fix adding the architecture domain to one governance procedure's scope list.

**2026-07-07 | 2026.07.174 | PR #686** - Session-closing handoff after a mid-session tooling outage moved the run to another machine; no published document changed.

**2026-07-06 | 2026.07.173 | PR #685** - Routine session-start validation review, with a trivial completeness fix adding the architecture domain to one governance framework's scope list.

**2026-07-06 | 2026.07.172 | PR #684** - Routine session-closing handoff; no published document changed.

**2026-07-06 | 2026.07.171 | PR #683** - The audit-evidence package template gained a per-status verification-basis field (independently verified, owner-asserted, or auditor-to-verify) and the internal-audit standard gained a matching verified-versus-asserted distinction. This stops an owner-asserted control status from being presented as if it were independently verified.

**2026-07-06 | 2026.07.170 | PR #682** - A new governance methodology standard was added documenting the five-tier maturity ladder, the median-of-medians aggregation used in self-assessment, that method's weakness of hiding a single very weak area, and a compensating floor-check the assessor reports alongside the median. Adopters get a documented maturity-assessment method with its limitation and safeguard spelled out.

**2026-07-06 | 2026.07.169 | PR #681** - A per-control effectiveness metric was introduced, defined in the trust-and-assurance metrics register from each control's latest test result, deficiency recurrence, and open corrective actions, and wired into the control-testing procedure and the assurance and metrics frameworks. Adopters get a per-control effectiveness measure tied to the three lines of defence.

**2026-07-06 | 2026.07.168 | PR #680** - Routine session-resume validation review, with three minor accuracy and cleanup fixes to standard designations and an example cell.

**2026-07-06 | 2026.07.167 | PR #679** - Routine session-closing handoff; no published document changed.

**2026-07-06 | 2026.07.166 | PR #678** - Recorded the outcomes of three internal protection-tooling attempts in the backlog.

**2026-07-06 | 2026.07.165 | PR #677** - Closed an internal guardrail item as a documented tool-environment limitation and reconciled the session handoff.

**2026-07-06 | 2026.07.164 | PR #676** - Folded a recount discipline into the AI-assistant's close-out checklist.

**2026-07-06 | 2026.07.163 | PR #675** - Widened an internal check that detects when a completed backlog item was recorded as done.

**2026-07-06 | 2026.07.162 | PR #674** - Added a citation-precision review-cadence section to the AI-assistant's process notes.

**2026-07-06 | 2026.07.161 | PR #673** - Overnight-run morning cleanup and bookkeeping reset; no published document changed.

**2026-07-06 | 2026.07.160 | PR #672** - Added a guardrail clause telling the AI-assistant not to idle or stop in unattended mode.

**2026-07-06 | 2026.07.159 | PR #671** - Recorded an internal quality-report intake process in the maintainer's runbook.

**2026-07-06 | 2026.07.158 | PR #670** - Fixed an internal acronym-consistency check so it also handles acronyms that start with a digit.

**2026-07-06 | 2026.07.157 | PR #669** - Recorded the root cause of an internal tool-hook issue and deferred its disposition; no published document changed.

**2026-07-06 | 2026.07.156 | PR #668** - The AWS, Azure, and GCP cloud-hardening baselines had their PCI DSS references made precise, from the family label version 4 to the current version 4.0.1. Adopters see the exact PCI DSS version in those baselines.

**2026-07-06 | 2026.07.155 | PR #667** - Citation and naming hygiene in published materials: a compliance-matrix framework label was shortened to plain C-TPAT, and the library specification's version-enforcement claim was corrected to name the checks that actually enforce it. Some internal tool error-message wording was also standardized; no requirements changed.

**2026-07-05 | 2026.07.154 | PR #666** - Corrected a stale factual one-liner in the AI-assistant's boundary notes.

**2026-07-05 | 2026.07.153 | PR #665** - Added a measure-before-you-claim bullet to the AI-assistant's close-out checklist.

**2026-07-05 | 2026.07.152 | PR #664** - The compliance matrix's ISO column header was harmonized to the joint ISO/IEC 27001:2022 designation, and the related validation check and its diagnostics were updated in step so the check keeps working. This is a designation-accuracy fix to a published matrix, with no change to the mapped controls.

**2026-07-05 | 2026.07.151 | PR #663** - Across 31 files, jointly issued standards were relisted from the single-body form (for example ISO 27001) to the correct joint form (ISO/IEC 27001), covering 13 confirmed-joint standards. Only the issuing-body designation changed, not any values, and single-body standards were deliberately left as-is.

**2026-07-05 | 2026.07.150 | PR #662** - The Brazil privacy annex and the breach-response procedure now carry a caveat that several recent (2023 to 2026) Brazilian data-protection instruments should be confirmed against the primary source before relying on the exact designation or figure. No figure or claim changed; the recent citations are just flagged as pending verification.

**2026-07-05 | 2026.07.149 | PR #661** - Routine session-resume close-out bookkeeping; no published document changed.

**2026-07-05 | 2026.07.148 | PR #660** - Routine session-closing handoff; no published document changed.

**2026-07-05 | 2026.07.147 | PR #659** - Added two close-out-checklist clauses to the AI-assistant's process notes.

**2026-07-05 | 2026.07.146 | PR #658** - Lightly restructured an internal design-decisions ledger with an index and a corrected ordering note.

**2026-07-05 | 2026.07.145 | PR #657** - Closed an internal checklist item and corrected a changelog narrative.

**2026-07-05 | 2026.07.144 | PR #656** - Named three governance-rule corollaries across the rule pack's index surfaces that had omitted them.

**2026-07-05 | 2026.07.143 | PR #655** - Added a cadence clause to an internal guardrail-review skill.

**2026-07-05 | 2026.07.142 | PR #654** - Refreshed MITRE ATLAS technique identifiers in the AI-assistant governance rule pack against the current release.

**2026-07-05 | 2026.07.141 | PR #653** - Codified two backlog-item lifecycle disciplines in the governance rule pack.

**2026-07-05 | 2026.07.140 | PR #652** - Switched operating mode and began clearing the deferred internal-file backlog; no published document changed.

**2026-07-05 | 2026.07.139 | PR #651** - Six acronyms used in the decision-tree guide that were neither expanded nor defined gained entries in the glossary so they now resolve. This closes small lookup gaps adopters would otherwise hit.

**2026-07-05 | 2026.07.138 | PR #650** - The ISO 27001 framework-table column headers in five documents were harmonized to the full ISO/IEC form. This is a designation-consistency fix with no change to the mapped controls.

**2026-07-05 | 2026.07.137 | PR #649** - Widened an internal standards-currency check to catch version labels written with a leading letter v.

**2026-07-05 | 2026.07.136 | PR #648** - Twelve citations to the superseded PCI DSS version 4.0 were migrated to the current version 4.0.1 across eight documents and the citation-form template. The cited requirements are unchanged (4.0.1 is an errata revision), only the version labels moved.

**2026-07-05 | 2026.07.135 | PR #647** - The compliance matrix and document index mappings for the AI Access and Agent Permissions Standard were corrected to the privileged-access ISO/IEC 27001 controls that match the document's own control table. This gives adopters accurate ISO mappings for that standard.

**2026-07-05 | 2026.07.134 | PR #646** - The patch-management procedure's single Critical patch deadline was split into two tiers to match the vulnerability-management procedure it operationalizes: a publicly-disclosed Critical with a proof of concept keeps a 72-hour deadline, while a Critical with no known exploitation gets 7 days. This removes a conflict where the two procedures gave different deadlines for the same case.

**2026-07-05 | 2026.07.133 | PR #645** - Routine session-resume validation review, with a documentation-only fix to an audit-programme description and a citation routed for maintainer verification; no published document content changed.

**2026-07-05 | 2026.07.132 | PR #644** - Routine session-closing handoff; no published document changed.

**2026-07-04 | 2026.07.131 | PR #643** - Refactored two internal cross-file reference checks to share their constants, preventing drift.

**2026-07-04 | 2026.07.130 | PR #642** - Extended an internal audit-specification consistency check to cover the pull-request-time delta checks.

**2026-07-04 | 2026.07.129 | PR #641** - Added an internal check for unbalanced code-fence markers that could hide content from other checks, and ran a scheduled guardrail review.

**2026-07-04 | 2026.07.128 | PR #640** - Renamed an internal audit check to accurately describe its NIST-only scope across the surfaces that name it.

**2026-07-04 | 2026.07.127 | PR #639** - Small citation and naming fixes in two procedures: an acronym was expanded at first use in the vulnerability-management procedure, and a partner-program name was normalized to the corpus-standard spelling in a supplier-monitoring procedure. These are readability and consistency fixes, not requirement changes.

**2026-07-04 | 2026.07.126 | PR #638** - A stale module count for the startup-roadmap was corrected from 23 to 24 in the navigation portal and the quickstart template. This keeps the count adopters see accurate.

**2026-07-04 | 2026.07.125 | PR #637** - The decision-tree guide dropped two maintainer-internal references from adopter-facing text, expanded two acronyms, and gained a note reconciling its organization-size bands with the adopter guide's, while the glossary gained matching entries for the two acronyms. These improve the clarity and consistency of the adopter-facing navigation materials.

**2026-07-04 | 2026.07.124 | PR #636** - The MITRE ATLAS technique references in the AI and agentic-development security standard were re-mapped to their current, correct identifiers against the latest ATLAS release. This corrects stale or wrong adversarial-technique citations adopters would follow.

**2026-07-04 | 2026.07.123 | PR #635** - Wired the pipe-guard self-tests into the regression suite and recorded a no-long-interval-check-in directive in the process notes.

**2026-07-04 | 2026.07.122 | PR #634** - Added a pull-request-time check that keeps the session-handoff version snapshot fresh.

**2026-07-04 | 2026.07.121 | PR #633** - An incorrect 72-hour Quebec (Law 25) breach-notification deadline was corrected to the statute's actual prompt-notification standard, which sets no fixed hour count, across five documents. This stops adopters from relying on a fabricated Quebec deadline.

**2026-07-04 | 2026.07.120 | PR #632** - Landed accumulated quality bookkeeping at a maintainer-requested queue pause; no published document changed.

**2026-07-04 | 2026.07.119 | PR #631** - Four privacy jurisdiction annexes (Japan, United States, Canada, and Brazil) were deepened to operational level, adding the breach-report clocks, data-subject-request timelines, and records obligations adopters actually run to, grounded in the primary laws. A pre-publication check also caught and began correcting a fabricated 72-hour Quebec breach deadline elsewhere in the corpus.

**2026-07-04 | 2026.07.118 | PR #630** - A citation-precision review corrected how several documents attribute values to sources: a 7-year AI-log retention period is now stated as the organization's own baseline that the cited standards inform but do not mandate, and a 24-hour supplier-notification clock as a contractual implementation of the GDPR's without-undue-delay standard. The attributed values are unchanged; only the claims about what the sources prescribe were corrected.

**2026-07-04 | 2026.07.117 | PR #629** - Applied an authorized bundle of edits to the AI-assistant process notes and widened the pipe-guard tooling.

**2026-07-04 | 2026.07.116 | PR #628** - Closed a retrospective-discipline item and processed the overnight run's morning bookkeeping.

**2026-07-04 | 2026.07.115 | PR #627** - Added an internal cross-file section-name consistency check and ran a guardrail review.

**2026-07-04 | 2026.07.114 | PR #626** - Validated an external quality report and routed its confirmed findings into the backlog.

**2026-07-04 | 2026.07.113 | PR #625** - Added an internal check ensuring every audit check has a description in the audit programme.

**2026-07-04 | 2026.07.112 | PR #624** - Fixed an internal cross-reference check seam and recorded several backlog items.

**2026-07-04 | 2026.07.111 | PR #623** - Added a pull-request-time check that a rule-pack version bump includes its version-history row.

**2026-07-04 | 2026.07.110 | PR #622** - Framework-table ISO 27001 headers were made edition-explicit (ISO/IEC 27001:2022) and several stray-punctuation cells in the compliance matrices were resolved (mostly to not-applicable, one to a checkmark), with a matrix legend repaired. These are designation and formatting accuracy fixes to published tables.

**2026-07-04 | 2026.07.109 | PR #621** - Added an advisory tool that flags claims attributing specific values to named standards; no corpus content changed yet.

**2026-07-03 | 2026.07.108 | PR #620** - Added tooling to block verification commands being piped in ways that hide failures; no published document changed.

**2026-07-03 | 2026.07.107 | PR #619** - Built and seeded the worker-ready research-brief staging and added an advisory freshness tool; no published document changed.

**2026-07-03 | 2026.07.106 | PR #618** - Recorded the design for staging worker-ready research briefs across the whole backlog; no published document changed.

**2026-07-03 | 2026.07.105 | PR #617** - A session-start validation-sweep close-out that doubled as a session-closing handoff; no published document changed.

**2026-07-03 | 2026.07.104 | PR #616** - Session-closing handoff for a maintainer-directed wind-down; no published document changed.

**2026-07-03 | 2026.07.103 | PR #615** - Routine tooling and working-note currency fixes carried over from a post-merge review; no published document changed.

**2026-07-03 | 2026.07.102 | PR #614** - Internal tooling repairs and working-note cleanup, including fixing a reference-lookup helper that a folder reorganization had broken.

**2026-07-03 | 2026.07.101 | PR #613** - Internal refactor consolidating duplicated version-field parsing in the audit tooling into one shared helper.

**2026-07-03 | 2026.07.100 | PR #612** - Internal activation of a check that flags whether AI-assistant research deliveries are properly attributed in the change record.

**2026-07-03 | 2026.07.99 | PR #611** - Internal session-coordination safeguard so two concurrent work sessions do not clash over shared files.

**2026-07-03 | 2026.07.98 | PR #610** - Internal audit check added to confirm that cross-document section references point to real headings, alongside a routine guardrail review.

**2026-07-03 | 2026.07.97 | PR #609** - Internal refinements to the AI-assistant's backlog-tracking and pre-push checks.

**2026-07-03 | 2026.07.96 | PR #608** - Routine morning wrap-up of an overnight work session; no published document changed.

**2026-07-03 | 2026.07.95 | PR #607** - The information security policy had its section headings and clause numbers renumbered to the library's uniform scheme. A control-mapping cell was also corrected to add the ISO/IEC 27002 cloud-services control, and no requirement changed.

**2026-07-03 | 2026.07.94 | PR #606** - The network and communications security policy was renumbered to the uniform section scheme. The change also corrected a mislabel where several security documents had tagged ISO/IEC 27002 controls with ISO/IEC 27001 Annex A numbering.

**2026-07-03 | 2026.07.93 | PR #605** - The secure development and engineering policy was renumbered to the uniform section scheme. A compliance-matrix note that understated the ISO/IEC 27001 clause range it covers was also corrected.

**2026-07-03 | 2026.07.92 | PR #604** - The legal and regulatory compliance policy was renumbered to the uniform section scheme. A control-mapping cell in the information security policy was also corrected to cite the right ISO/IEC 27001 Annex A controls.

**2026-07-03 | 2026.07.91 | PR #603** - The compliance and audit management policy was renumbered to the uniform section scheme, with references to it updated in four other documents. An over-broad ISO/IEC 27001 control range in the identity and access management policy was also narrowed to the correct controls.

**2026-07-03 | 2026.07.90 | PR #602** - The logging and monitoring standard was renumbered to the uniform section scheme, with citations to it updated in two operations procedures. Several stale cross-references and framework-mapping cells in related security documents were also corrected.

**2026-07-03 | 2026.07.89 | PR #601** - The data classification and handling standard was renumbered to the uniform section scheme. The identity and access management policy's framework table was also given an explicit ISO/IEC 27002:2022 edition label and had two control references corrected.

**2026-07-03 | 2026.07.88 | PR #600** - The identity and access management policy was renumbered to the uniform section scheme. This was a numbering-consistency change with no requirement change and no cross-references elsewhere needing updates.

**2026-07-03 | 2026.07.87 | PR #599** - The encryption and key management policy was renumbered to the uniform section scheme, with three dev-security documents' references to it updated to match. No requirement changed.

**2026-07-03 | 2026.07.86 | PR #598** - The acceptance into service policy was renumbered to the uniform section scheme. A wrong control-catalogue code for this document in the document index was also corrected, where a CSA code had been confused by an acronym clash.

**2026-07-03 | 2026.07.85 | PR #597** - The service level management standard was renumbered to the uniform section scheme. This was a numbering-consistency change with no requirement change and no cross-references elsewhere to update.

**2026-07-03 | 2026.07.84 | PR #596** - The exception and risk acceptance management policy was renumbered to the uniform section scheme, with references to it updated in five other documents. No requirement changed.

**2026-07-03 | 2026.07.83 | PR #595** - Internal tooling updates to the AI-assistant's backlog-rotation and audit-count checks.

**2026-07-03 | 2026.07.82 | PR #594** - The internal audit standard's own cross-references were standardized to the library's section-reference notation. No section numbers or requirements changed.

**2026-07-03 | 2026.07.81 | PR #593** - COBIT control-code citations were corrected across several compliance, risk, governance, and AI documents, with each kept or recoded to the control that actually fits its description (for example some rows moved to the assurance control MEA04). This corrects how those documents map to the COBIT framework.

**2026-07-03 | 2026.07.80 | PR #592** - A round of COBIT control-code corrections was applied across supplier, compliance, and governance documents so each citation matches the fitting control. The security incident-response procedure was also updated to add the data protection officer to an information-sharing list and to add Quebec's Law 25.

**2026-07-03 | 2026.07.79 | PR #591** - The security incident-response procedure's role table was corrected so regulatory notifications route through the data protection officer with legal approval. The library's internal coverage-tracking register was also re-graded for several trade and AI regimes and gained a Brazil customs-programme entry.

**2026-07-03 | 2026.07.78 | PR #590** - A composite CIO-acting-as-data-protection-officer role was replaced throughout the corpus with a distinct Data Protection Officer role across ten privacy, security, and governance documents (and a few more caught during review). This clarifies privacy accountability and separates the two roles in role tables and sign-off chains.

**2026-07-03 | 2026.07.77 | PR #589** - A retention standard's requirement for seven-year approval was narrowed to apply only to ad-hoc extensions beyond the schedule, not to schedule-defined values. A couple of internal pointer and record cleanups rode along.

**2026-07-02 | 2026.07.76 | PR #588** - COBIT control-code citations were corrected across the cross-framework matrix and several risk, exception, and supplier documents, moving each to its fitting control and restoring canonical control titles. An ISO 31000 clause number was also corrected.

**2026-07-02 | 2026.07.75 | PR #587** - A new audit check that verifies COBIT 2019 and ISO 31000 citations actually exist was added, and it immediately caught and fixed three invalid control or standard references in compliance, security, and privacy documents. This makes those framework citations verifiable and corrects them.

**2026-07-02 | 2026.07.74 | PR #586** - Internal re-grading of the library's coverage-tracking register for sixteen regimes and frameworks, with the coverage vocabulary refined; no published guidance changed.

**2026-07-02 | 2026.07.73 | PR #585** - The library standardized its document-lifecycle vocabulary on the word Superseded (replacing Deprecated) across the library charter, a report template, the adopter guide, and a build tool. Adopters following the adopter guide now use a dedicated Superseded status marker.

**2026-07-02 | 2026.07.72 | PR #584** - Internal updates to the AI-assistant's operating instructions, including making proactive assessment a standing default and adding a background-task check routine.

**2026-07-02 | 2026.07.71 | PR #583** - Internal tightening of a guardrail-review cadence check's failure threshold.

**2026-07-02 | 2026.07.70 | PR #582** - Internal advisory tool added to flag when a rewritten backlog or ledger entry claims completion while still carrying a pending marker.

**2026-07-02 | 2026.07.69 | PR #581** - Internal re-grading of eleven cells in the library's coverage-tracking register against verified corpus evidence.

**2026-07-02 | 2026.07.68 | PR #580** - Two AI-records retention rows in the data-retention schedule were recomposed so records are kept for a fixed floor or until five years after the system is decommissioned, whichever is longer, so no record is destroyed while its system still runs. Matching example values in two related standards were updated to the same wording.

**2026-07-02 | 2026.07.67 | PR #579** - Internal change moving document-lifecycle status out of the classification field into a dedicated status marker, with the affected checks and notes updated to match.

**2026-07-02 | 2026.07.66 | PR #578** - Internal fix to the local pre-commit check ordering so generated-file drift fails loudly instead of being silently regenerated.

**2026-07-02 | 2026.07.65 | PR #577** - Internal tooling that mechanizes the guardrail-review cadence as an audit check, plus minor retention-note cleanup.

**2026-07-02 | 2026.07.64 | PR #576** - The supplier-audit procedure gained a records-retention statement and the AI-audit procedure's retention wording was standardized to a seven-year minimum. Several internal consistency checks were also widened.

**2026-07-02 | 2026.07.63 | PR #575** - Internal tool added to re-scan the working tree for leftover instances of a just-corrected term, plus minor record cleanups including a corrected register name in the privacy charter.

**2026-07-02 | 2026.07.62 | PR #574** - A cleanup batch touched several documents: security-incident and AI-audit retention rows were raised or recomposed to stricter values, and hardcoded regional scope and sector examples in the privacy charter and risk-appetite template were genericized for adopters. A decision-tree phasing note was also clarified.

**2026-07-02 | 2026.07.61 | PR #573** - A batch of citation and terminology corrections: the Japanese privacy annex's transliteration of a legal term was fixed, and COBIT objective titles were corrected across three risk documents. It also carried internal spelling and tooling-note cleanups.

**2026-07-02 | 2026.07.60 | PR #572** - The data-subject-rights response clock was corrected to the statutory GDPR one-month deadline (extendable by two months) across the rights procedure, the request template, and the privacy policy. The PIPEDA 30-day clock was retained where it applies and the California 45-day window was added.

**2026-07-02 | 2026.07.59 | PR #571** - Routine morning processing of an overnight work session, routing its working state and fixing minor sweep findings; no published guidance changed.

**2026-07-02 | 2026.07.58 | PR #570** - Spelling across the whole corpus was harmonized to Canadian orthography (about 2000 changes over roughly 330 documents), and one privacy standard was renamed accordingly. This is an editorial consistency pass; old deep links to the renamed file will break.

**2026-07-02 | 2026.07.57 | PR #569** - Fifty-four grammatically incomplete ensure-that sentences were repaired across thirty-six documents, and a decision-tree answer plus several coverage-register cells were corrected. These are readability and accuracy fixes with no change to requirements.

**2026-07-02 | 2026.07.56 | PR #568** - Internal cleanup of stale backlog tokens and document counts in the coverage-tracking register, the generated portal page, and a few adopter guides.

**2026-07-02 | 2026.07.55 | PR #567** - Seven cross-document conflicts in operational documents were resolved to the stricter or canonical value, covering incident escalation timing, an MFA exception path, encryption requirements, incident-notification clocks, audit-finding severity mapping, compliance ownership, and risk-acceptance duration limits. This removes contradictions adopters would otherwise hit between documents.

**2026-07-02 | 2026.07.54 | PR #566** - Two citation values were reconciled corpus-wide: the BASC supply-chain standard version was standardized to Version 6 (2022) across sixteen references, and Brazil's LGPD breach-notification rule was corrected to the current ANPD resolution requiring notice within three business days. Both were confirmed against the primary sources.

**2026-07-02 | 2026.07.53 | PR #565** - Several framework-citation corrections were applied: an outdated CSA control family was dropped, a fabricated ISO/IEC 27001 Annex A control title was corrected to its real title, and nonexistent or non-canonical COBIT and ISO 31000 references were fixed. These improve citation accuracy in governance and matrix documents.

**2026-07-02 | 2026.07.52 | PR #564** - Data-subject-access-request handling was reconciled to the canonical procedure: the request template adopted the procedure's identity-verification levels and clocks, and the procedure now requires a second officer's written concurrence before any denial. Timing and authority conflicts between the two documents were resolved.

**2026-07-02 | 2026.07.51 | PR #563** - Retention-period conflicts were resolved to the safer value across audit, breach, and assessment records, with audit records held to a seven-year floor and assessment records recomposed so nothing is destroyed while its system still runs. This removes contradictory retention values between documents.

**2026-07-02 | 2026.07.50 | PR #562** - The corpus's three divergent risk-category schemes were reconciled to the canonical twelve-category set across the enterprise risk management standard and related risk documents, with no example categories lost. Several coupled fixes corrected risk-routing and scoring-band wording.

**2026-07-02 | 2026.07.49 | PR #561** - The risk-assessment methodology's risk-acceptance authority was realigned so High and Critical acceptances are approved by the Executive Committee or Board Risk Committee, matching the rest of the corpus. This closes the last two places that still named the old authority.

**2026-07-02 | 2026.07.48 | PR #560** - The risk-assessment methodology's residual-risk formula was replaced with the canonical re-scored model used by the enterprise risk standard and register template (residual likelihood times residual impact, with control effectiveness rated categorically). This removes a contradiction in how residual risk is calculated.

**2026-07-02 | 2026.07.47 | PR #559** - Internal broadening of a backlog-rotation check to recognize more coded closure markers.

**2026-07-02 | 2026.07.46 | PR #558** - Internal cleanup of stale references and pointers in tool comments and docstrings.

**2026-07-02 | 2026.07.45 | PR #557** - Internal audit check added to verify that changelog version numbers stay in strictly decreasing order.

**2026-07-02 | 2026.07.44 | PR #556** - Internal refactor introducing a shared metadata parser and making the document-date check fail loudly on malformed dates.

**2026-07-02 | 2026.07.43 | PR #555** - Internal regression tests added for the pre-push and change-time checks.

**2026-07-02 | 2026.07.42 | PR #554** - Internal routing of guardrail-review findings into the backlog as new tooling and rule work items.

**2026-07-02 | 2026.07.41 | PR #553** - Internal validation-sweep close-out and backlog bookkeeping; no published document changed.

**2026-07-02 | 2026.07.40 | PR #552** - Internal end-of-session handoff bookkeeping; no published document changed.

**2026-07-02 | 2026.07.39 | PR #551** - Internal intake of an external read-only audit's findings into the backlog, validated at source; no fixes applied yet.

**2026-07-02 | 2026.07.38 | PR #550** - Routine session-resume validation review that returned no findings; no published document changed.

**2026-07-02 | 2026.07.37 | PR #549** - Internal session-closing handoff bookkeeping; no published document changed.

**2026-07-02 | 2026.07.36 | PR #548** - The mobile application security standard was renumbered to the uniform section scheme, and the AI-assistant rule pack's many references to its sections were updated to match. No requirement changed.

**2026-07-02 | 2026.07.35 | PR #547** - The AI and agentic development security standard was renumbered to the uniform section scheme, mainly numbering its framework-alignment section and subsections. Its existing cross-references were already correct, so nothing else changed.

**2026-07-01 | 2026.07.34 | PR #546** - The developer security requirements standard was renumbered to the uniform section scheme, with references to it in two related documents updated to match. No requirement changed.

**2026-07-01 | 2026.07.33 | PR #545** - The production security requirements standard was renumbered to the uniform section scheme, with references to it in a related operations procedure updated to match. No requirement changed.

**2026-07-01 | 2026.07.32 | PR #544** - The privacy and data governance policy was renumbered to the uniform section scheme, with a reference to it in the data-subject-rights procedure updated to match. No requirement changed.

**2026-07-01 | 2026.07.31 | PR #543** - The AI security and risk standard was renumbered to the uniform section scheme, and its own internal crosswalk references were remapped to match. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.30 | PR #542** - The supplier resilience monitoring standard was renumbered to the uniform section scheme, including converting its numbered signal categories to numbered subsections. No requirement changed.

**2026-07-01 | 2026.07.29 | PR #541** - The security awareness and training standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.28 | PR #540** - The technology radar standard was renumbered to the uniform section scheme, with its two internal cross-references remapped. No requirement changed.

**2026-07-01 | 2026.07.27 | PR #539** - The integration architecture standard was renumbered to the uniform section scheme, with its two internal cross-references remapped. No requirement changed.

**2026-07-01 | 2026.07.26 | PR #538** - The AI inference cost governance standard was renumbered to the uniform section scheme, with one internal cross-reference remapped. No requirement changed.

**2026-07-01 | 2026.07.25 | PR #537** - The AI access and agent permissions standard was renumbered to the uniform section scheme, including its subsection tree. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.24 | PR #536** - The API security standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.23 | PR #535** - The observability and telemetry standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.22 | PR #534** - The capacity and performance management standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.21 | PR #533** - The records retention and destruction standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.20 | PR #532** - The software composition analysis standard was renumbered to the uniform section scheme, with a reference to it in a related guideline updated to match. No requirement changed.

**2026-07-01 | 2026.07.19 | PR #531** - The DevOps security requirements standard was renumbered to the uniform section scheme, with its one internal cross-reference remapped. No requirement changed.

**2026-07-01 | 2026.07.18 | PR #530** - The third-party and supply-chain risk standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.17 | PR #529** - The quality assurance and testing standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.16 | PR #528** - The authentication and password management standard was renumbered to the uniform section scheme, and its NIST reference cells were relabeled to name the standard inline so they read unambiguously. No requirement changed.

**2026-07-01 | 2026.07.15 | PR #527** - The digital twin and simulation governance policy was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.14 | PR #526** - The personnel security screening standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.13 | PR #525** - The AI testing, validation and documentation standard was renumbered to the uniform section scheme. No requirement changed and no other document cited its sections.

**2026-07-01 | 2026.07.12 | PR #524** - The AI model risk standard was renumbered to the uniform section scheme, with the one document that cited its sections updated to match. No requirement changed.

**2026-07-01 | 2026.07.11 | PR #523** - Internal refinements to the AI-assistant's wind-down and close-out instructions.

**2026-07-01 | 2026.07.10 | PR #522** - Internal cross-check confirming the citation register's recorded versions match the reference base; no mismatches found and no document changed.

**2026-07-01 | 2026.07.9 | PR #521** - Internal audit check added to confirm the public changelog and its maintainer archive carry the same per-change headers.

**2026-07-01 | 2026.07.8 | PR #520** - Twenty-eight policy and standard documents had their section headings renumbered to the library's uniform numbering scheme. This was a numbering-consistency pass limited to documents with no external cross-references, so no requirement changed.

**2026-07-01 | 2026.07.7 | PR #519** - Routine session-resume validation review that returned no findings; no published document changed.

**2026-07-01 | 2026.07.6 | PR #518** - Internal session-closing handoff bookkeeping; no published document changed.

**2026-07-01 | 2026.07.5 | PR #517** - A new governance procedure was added describing the seven-step process for moving the library from one edition of a cited external standard to a newer one. It gives adopters a documented method for standard-version transitions across the corpus.

**2026-07-01 | 2026.07.4 | PR #516** - Internal extension of the language check to also scan text emitted by the portal and taxonomy generators.

**2026-07-01 | 2026.07.3 | PR #515** - Internal addition to the citation-verification specification describing the reference base used as citation ground truth.

**2026-07-01 | 2026.07.2 | PR #514** - Routine session-resume validation review with two minor working-file fixes; no published guidance changed.

**2026-07-01 | 2026.07.1 | PR #513** - Internal session-closing handoff with a minor working-file consistency fix; no published document changed.

**2026-07-01 | 2026.07.0 | PR #512** - The citation register's MITRE ATLAS entry was updated to the current version (v2026.06) after re-checking the primary source. This keeps the corpus's MITRE ATLAS citation current.

**2026-06-30 | 2026.06.489 | PR #511** - Internal broadening of a count-consistency check to also catch collection counts (audit checks and rules) written as words.

**2026-06-30 | 2026.06.488 | PR #510** - Internal update to the skill-authoring checklist and a corrected count in a rule-pack narrative.

**2026-06-30 | 2026.06.487 | PR #509** - Internal audit check added to validate ISO/IEC 27001:2022 Annex A control codes wherever they appear in document framework tables.

**2026-06-30 | 2026.06.486 | PR #508** - Media-sanitization citations were updated to NIST SP 800-88 Revision 2 and a new reference to IEEE 2883:2022 was introduced, re-pointing the media-handling procedure and related documents to the current standards. This corrects and modernizes how sanitization techniques are cited.

**2026-06-30 | 2026.06.485 | PR #507** - The ISO/IEC 27036-2 supplier-relationships citation was upgraded from the 2014 edition to the current 2022 edition in the citation register and the supplier due-diligence procedure. This keeps that standard citation current.

**2026-06-30 | 2026.06.484 | PR #506** - A nonexistent ISO/IEC 27033:2020 citation was corrected to the real ISO/IEC 27033-1:2015 network-security standard across the citation register and two network-security documents. This fixes an invalid standard reference.

**2026-06-30 | 2026.06.483 | PR #505** - The citation register gained version-currency tracking (an upstream-check location and last-verified date for all 151 cited items) and seven citation corrections confirmed against primary sources. This helps keep the library's external-standard citations current and verifiable.

**2026-06-30 | 2026.06.482 | PR #504** - Internal change to an AI-assistant rule adding a compute-the-answer-before-asking step for findable facts.

**2026-06-30 | 2026.06.481 | PR #503** - Routine session-resume validation review with minor working-file fixes; no published document changed.

**2026-06-30 | 2026.06.480 | PR #502** - Internal session-closing handoff bookkeeping; no published document changed.

**2026-06-30 | 2026.06.479 | PR #501** - Internal broadening of a backlog-rotation check and a minor instruction reword.

**2026-06-30 | 2026.06.478 | PR #500** - Internal reformatting of the backlog file so every item is a uniform priority-numbered subsection.

**2026-06-30 | 2026.06.477 | PR #499** - A spelling check was fixed to catch a missed verb form, and the resulting twenty-four Commonwealth spellings across the corpus and rule pack were normalized to Canadian spelling. This is an editorial consistency fix.

**2026-06-30 | 2026.06.476 | PR #498** - Internal reorganization of the backlog into work-type priority tiers.

**2026-06-30 | 2026.06.475 | PR #497** - A new Adoption Disposition classification was added to the document index, labeling every active document as an adopter-customizable template, a library-internal file, or an as-cited reference. This lets adopters see at a glance which documents to adapt versus leave as-is.

**2026-06-30 | 2026.06.474 | PR #496** - Internal backlog-to-done bookkeeping correction for two completed items; no published document changed.

**2026-06-30 | 2026.06.473 | PR #495** - An audit checked the operational-technology security documents against the current NIST SP 800-82 Revision 3 and ISO/IEC 27019:2024 sources and found them sound. One clarifying sentence was added to an OT security overview stating that, per NIST guidance, human safety takes priority over protecting the process where safety and availability conflict.

**2026-06-30 | 2026.06.472 | PR #494** - The GRC compliance alignment matrix gained seven rows mapping the six operational-technology security documents and an AI security tooling register across its cloud-control, ISO/IEC 27001:2022, and NIST frameworks. This extends framework-alignment coverage to those previously unmapped documents.

**2026-06-30 | 2026.06.471 | PR #493** - A control-testing procedure mislabeled the Sarbanes-Oxley material-weakness concept as a section 103 construct, and it was corrected to section 404. This fixes an inaccurate statutory reference adopters rely on.

**2026-06-30 | 2026.06.470 | PR #492** - A control-testing procedure was expanded from a thin outline into a full operable procedure, adding tester independence, risk-based testing frequency and sampling, working-paper standards, result classification, remediation escalation, and a testing register and metrics. This gives adopters a usable control-testing methodology where before they had only named phases.

**2026-06-30 | 2026.06.469 | PR #491** - The GRC compliance alignment matrix gained seven rows for privacy, compliance, and AI documents that had shipped without matrix coverage. This closes gaps in the framework-alignment mapping.

**2026-06-30 | 2026.06.468 | PR #490** - A semantic-fit review of the compliance matrix found it clean and surfaced one mis-cited pair of cloud-control codes in a cloud asset-inventory register, corrected to the asset-classification and asset-cataloguing controls. This fixes a control mapping in that register's framework table.

**2026-06-30 | 2026.06.467 | PR #489** - Added cross-reference links so documents mentioning a transfer impact assessment now point to the new template.

**2026-06-30 | 2026.06.466 | PR #488** - The financial-services sector annex's regulator overview gained the prudential regulators it lacked, adding Asia-Pacific (Singapore, Australia, Hong Kong, Japan), Switzerland, and the US federal banking regulators. Each is named structurally with a note directing adopters to confirm the current instruments against the regulator.

**2026-06-30 | 2026.06.465 | PR #487** - A new adopter-fillable breach-notification regulator register template was added, recording each applicable regulator's deadline alongside a tighter internal target, and wired into the breach-response procedure. This gives adopters a single instrument to track per-regulator breach-notification obligations.

**2026-06-30 | 2026.06.464 | PR #486** - AI ethics review was split out of the AI Governance Council into a new independent AI Ethics Review Panel charter with a documented challenge-and-escalation mechanism. This gives adopters a structurally independent body that can challenge AI governance decisions on ethical grounds.

**2026-06-30 | 2026.06.463 | PR #485** - A new sanctions and export-control screening standard was added, covering the major sanctions and export-control regimes, denied-party and beneficial-ownership screening, and a screening workflow. This provides a dedicated control where the topic was previously handled only incidentally in other procedures.

**2026-06-30 | 2026.06.462 | PR #484** - A new mergers-and-acquisitions due-diligence procedure was added, defining transaction phases with decision points, a due-diligence checklist cross-referenced to governing documents, and a red-flag register. This fills a gap the governance programme referenced but never provided.

**2026-06-30 | 2026.06.461 | PR #483** - A new adopter-fillable transfer impact assessment template was added, operationalizing the six-step European Data Protection Board methodology for GDPR Chapter V restricted international transfers. This gives adopters a fill-in instrument grounded in GDPR Articles 44 to 49.

**2026-06-30 | 2026.06.460 | PR #482** - A new privacy-by-design framework was added, operationalizing GDPR Article 25 by mapping the seven foundational principles and the by-default dimensions to the organization's architecture and development workflows. This gives adopters a data-protection-by-design framework.

**2026-06-30 | 2026.06.459 | PR #481** - The two AI security standards gained a relationship section stating their scope boundaries and precedence, plus a crosswalk mapping one to the other. This resolves the ambiguity about which AI security standard governs a given topic, without changing any requirement.

**2026-06-30 | 2026.06.458 | PR #480** - A new adopter-fillable legitimate interest assessment template was added for the GDPR legitimate-interest legal basis, recording the three-part purpose, necessity, and balancing tests and related obligations. This gives adopters a fill-in instrument citing GDPR, UK GDPR, and ISO/IEC 27701:2025.

**2026-06-30 | 2026.06.457 | PR #479** - Fixed a malformed retrospective-log row and recorded routine post-merge quality bookkeeping.

**2026-06-30 | 2026.06.456 | PR #478** - Folded several apply-time process reminders into the AI-assistant instruction file.

**2026-06-30 | 2026.06.455 | PR #477** - Three lingering lowercase references to an executive risk committee were corrected to the canonical Enterprise Risk Committee in a data-loss-prevention standard and a board risk-report template, and a governance guideline's duplicate committee row was reconciled. This removes a committee-naming inconsistency across those documents.

**2026-06-30 | 2026.06.454 | PR #476** - Recorded a start-of-session validation review and added a missing descriptive paragraph for one check in the internal audit-programme specification.

**2026-06-29 | 2026.06.453 | PR #475** - Routine end-of-session handoff bookkeeping; no published document changed.

**2026-06-29 | 2026.06.452 | PR #474** - Corrected an AI-assistant close-out reminder about how one check's phrasing rule is scoped.

**2026-06-29 | 2026.06.451 | PR #473** - Codified two recurring close-out reminders in the AI-assistant instruction file.

**2026-06-29 | 2026.06.450 | PR #472** - Updated stale references in the AI-assistant instructions and a tool description after two backlog sections closed.

**2026-06-29 | 2026.06.449 | PR #471** - Closed a quality-cadence-enforcement backlog item and rotated it to the done ledger.

**2026-06-29 | 2026.06.448 | PR #470** - Brought the adopter guides under the house-style language check and fixed the accumulated style issues such as dashes, spelling variants, and heading case.

**2026-06-29 | 2026.06.447 | PR #469** - Added a pre-merge check that a change claiming to close a backlog item also rotates it between the backlog and done ledgers.

**2026-06-29 | 2026.06.446 | PR #468** - Added an audit check flagging a backlog item marked done in place instead of rotated to the done ledger.

**2026-06-29 | 2026.06.445 | PR #467** - Rotated a completed backlog item to the done ledger.

**2026-06-29 | 2026.06.444 | PR #466** - Added an audit check for stray mandatory shall wording left in the documents.

**2026-06-29 | 2026.06.443 | PR #465** - Recorded a start-of-session validation review and corrected a stale check-count figure in an internal skill description.

**2026-06-29 | 2026.06.442 | PR #464** - Routine end-of-session handoff bookkeeping for an unattended work session.

**2026-06-29 | 2026.06.441 | PR #463** - Consolidated five library-maintainer roles into the role authority register and emptied the tool allow-list that had held them.

**2026-06-29 | 2026.06.440 | PR #462** - Added an audit check that evidence-retention periods cited in three procedures match the canonical retention schedule.

**2026-06-29 | 2026.06.439 | PR #461** - Codified a standard of using skeptical reviewer sub-processes before pushing anything beyond a quick fix.

**2026-06-29 | 2026.06.438 | PR #460** - Corrected the session wind-down guidance so continuing work is the default and a handoff needs real evidence of trouble.

**2026-06-29 | 2026.06.437 | PR #459** - Acted on two process-improvement suggestions from a prior retrospective.

**2026-06-29 | 2026.06.436 | PR #458** - Completed the mandatory-verb harmonization by converting the remaining shall wording in a secure-development policy to must, recorded during a validation review.

**2026-06-29 | 2026.06.435 | PR #457** - Routine end-of-session handoff bookkeeping for an overnight correction batch.

**2026-06-29 | 2026.06.434 | PR #456** - Ten references to an executive risk committee across nine documents were corrected to the glossary-canonical Enterprise Risk Committee. This removes a committee-naming inconsistency spanning compliance, operations, and privacy documents.

**2026-06-29 | 2026.06.433 | PR #455** - Harmonized mandatory shall wording to must across seventeen documents to match the library's normative-language convention, with no change to any requirement.

**2026-06-29 | 2026.06.432 | PR #454** - Completed a rule-scope table in the distributable AI-assistant rule pack that had fallen behind as the pack grew.

**2026-06-29 | 2026.06.431 | PR #453** - Added a seventeenth skill to the distributable AI-assistant rule pack, the executable companion to its high-assurance-verification rule.

**2026-06-29 | 2026.06.430 | PR #452** - Corrected a mismatch between an AI-assistant instruction and the check that enforces it, for how a handoff exemption is recorded.

**2026-06-28 | 2026.06.429 | PR #451** - First step of a resumed overnight run: recorded a validation review and fixed two stale count figures in internal notes.

**2026-06-28 | 2026.06.428 | PR #450** - Added a twelfth governance rule to the distributable AI-assistant rule pack, standardizing an independent-verification method for sensitive changes.

**2026-06-28 | 2026.06.427 | PR #449** - Extended an advisory matrix worklist tool to cover the new AI-focused cloud-control column.

**2026-06-28 | 2026.06.426 | PR #448** - The compliance alignment matrix gained a CSA AICM version 1.1 column carrying the AI-specific cloud-control mappings, so the matrix now maps nine frameworks. This gives adopters AI-focused cloud-control coverage across the matrix.

**2026-06-28 | 2026.06.425 | PR #447** - Extended an audit check to validate the new AI-focused cloud-control matrix column before that column's data landed.

**2026-06-28 | 2026.06.424 | PR #446** - First step of a session: recorded a validation review, pruned the handoff record, and logged the session's decisions.

**2026-06-28 | 2026.06.423 | PR #445** - Session-closing handoff carrying one small addition to the AI-assistant close-out checklist about bare-token contradiction searches.

**2026-06-28 | 2026.06.422 | PR #444** - Extended an existing audit check to verify a metadata version also appears as a row in the document's version-history table.

**2026-06-28 | 2026.06.421 | PR #443** - Corrected a spot-scanned skill count from 18 to 19 across the distributable rule pack's vetting records.

**2026-06-28 | 2026.06.420 | PR #442** - Added a maintainer-facing guidance document to the distributable rule pack on the keep-and-condense method for an always-loaded instruction file.

**2026-06-28 | 2026.06.419 | PR #441** - Condensed the AI-assistant instruction file by about a quarter, keeping every rule and preserving the removed rationale in a separate ledger.

**2026-06-28 | 2026.06.418 | PR #440** - Fixed a bug in the pre-push quality-check script that let it pass even when an underlying check had failed.

**2026-06-28 | 2026.06.417 | PR #439** - Added a single pre-push script that chains the quality checks and stops on the first failure.

**2026-06-28 | 2026.06.416 | PR #438** - Recorded a validation review and renamed a shared-storage path across the AI-assistant guidance surfaces.

**2026-06-28 | 2026.06.415 | PR #437** - Session-closing handoff landing the working state as a green merge.

**2026-06-28 | 2026.06.414 | PR #436** - Backlog-hygiene housekeeping trimming completed items and recording a deferred decision.

**2026-06-28 | 2026.06.413 | PR #435** - The canonical-citations register's MITRE ATT&CK and MITRE ATLAS version entries were updated to the current upstream-verified releases, ATT&CK version 19.1 and the 2026.05 ATLAS release. This corrects stale framework-version references.

**2026-06-28 | 2026.06.412 | PR #434** - Codified a discipline against asserting states that cannot be observed, and added a reference-version-currency procedure, in the distributable rule pack and AI-assistant guidance.

**2026-06-28 | 2026.06.411 | PR #433** - Recorded a validation review, pruned the lengthy handoff record, and codified a handoff-pruning convention.

**2026-06-28 | 2026.06.410 | PR #432** - Routine end-of-session handoff bookkeeping.

**2026-06-28 | 2026.06.409 | PR #431** - Added an AI-assistant convention for interpreting suggest or advise and captured a backlog item.

**2026-06-28 | 2026.06.408 | PR #430** - Codified communication conventions in the AI-assistant instruction file.

**2026-06-28 | 2026.06.407 | PR #429** - A supplier-exit procedure's escalation step that pointed the responsible officer back to itself was retargeted to Legal and the contract owner, and a compliance-matrix pseudonymization row's loosely-fitting cloud-control code was replaced with a better-fitting one. Both fix issues adopters would otherwise inherit.

**2026-06-28 | 2026.06.406 | PR #428** - Seven invalid cloud-control-framework citations, referencing a privacy control domain that does not exist in CSA CCM version 4.1, were corrected to valid controls across three privacy documents. This fixes broken control-code references.

**2026-06-28 | 2026.06.405 | PR #427** - Five mis-cited cloud-control-framework codes, an outdated privacy control family and one wrong control, were corrected across two privacy procedures. This repairs invalid control-code citations.

**2026-06-28 | 2026.06.404 | PR #426** - Recorded a validation review and fixed two stale governance-rule count figures in internal notes.

**2026-06-28 | 2026.06.403 | PR #425** - Session-closing handoff bookkeeping that also ended overnight mode.

**2026-06-28 | 2026.06.402 | PR #424** - A governance glossary gained the Executive Leadership Team acronym, two soft-law rows in the canonical-citations register had their version cells clarified, and mixed mandatory verbs in two policies were harmonized to must. These are small consistency and completeness improvements to the published documents.

**2026-06-28 | 2026.06.401 | PR #423** - Added an eleventh governance rule to the distributable AI-assistant rule pack on surfacing counterproductive instructions before acting.

**2026-06-28 | 2026.06.400 | PR #421** - The README and adopter guide navigation was reconciled so the day-one starter set is presented ahead of the larger grow-toward catalogue, catalogue items are noted as discoverable by title, and seven thematic areas are distinguished from the eleven domain directories. This clarifies how a new adopter orients to the library.

**2026-06-28 | 2026.06.399 | PR #420** - The privacy jurisdiction index's EU AI Act timing was reworded to forward-looking, the Brazil annex gained a breach-notification entry, and India was added to the breach-response procedure's jurisdiction coverage. This corrects and extends jurisdiction-specific breach guidance.

**2026-06-28 | 2026.06.398 | PR #419** - The P1 and P2 post-incident-review deadline was harmonized to five business days across every procedure carrying it, and the emergency operations centre activation authority was named. This gives adopters consistent incident-review timing and a clear activation authority.

**2026-06-27 | 2026.06.397 | PR #418** - The remote-working standard now requires WPA3 for home networks, removing the WPA2 fallback with a carve-out for IoT that cannot support it, and the password-hashing floor was tightened to the encryption policy's Argon2id parameters. This raises the security floor adopters implement for remote work and password storage.

**2026-06-27 | 2026.06.396 | PR #417** - Session-closing handoff for a remediation work session.

**2026-06-27 | 2026.06.395 | PR #416** - The privacy jurisdiction index's India data-protection dates were corrected to the verified 13 November 2025 rules notification and its phased commencement. This fixes an inaccurate in-force date across the reconciled surfaces.

**2026-06-27 | 2026.06.394 | PR #415** - The P2 incident notification time to the security chief was reconciled to one hour, a superseded NIST SP 800-61 incident-handling title was corrected to its current form at three citing documents, and a severity crosswalk was added. This gives adopters consistent escalation timing and an accurate NIST reference.

**2026-06-27 | 2026.06.393 | PR #414** - Retention statements in the record-of-processing template, the consent-management framework, and the records-retention standard were reconciled to the canonical data-retention schedule. This removes conflicting retention periods across the privacy documents.

**2026-06-27 | 2026.06.392 | PR #413** - Backlog-hygiene housekeeping that relocated an internal metadata block and re-pointed a staleness check.

**2026-06-27 | 2026.06.391 | PR #412** - Several risk documents were reconciled to single canonical sources for the likelihood scale, the high-residual-risk acceptance authority, and the low-band treatment action. This removes cross-document conflicts in the risk-scoring and acceptance guidance.

**2026-06-27 | 2026.06.390 | PR #411** - Eight invalid control-code citations in the exception-and-risk-acceptance policy were corrected, a risk-register cross-reference was repointed to the canonical scoring grid, and three broken section references in the onboarding procedure were repaired. This fixes broken citations and references adopters rely on.

**2026-06-27 | 2026.06.389 | PR #410** - Session-closing handoff recording a maintainer-directed full quality-recovery review and the routing of its findings to the backlog.

**2026-06-27 | 2026.06.388 | PR #409** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.387 | PR #408** - Five European data-protection soft-law guidance documents, covering anonymization, data-protection impact assessments, controller and processor concepts, territorial scope, and AI models, were added to the canonical-citations register with verified titles and dates. This gives adopters authoritative soft-law references.

**2026-06-27 | 2026.06.386 | PR #407** - Recorded, in the backlog, findings from a read-only review of the reference library.

**2026-06-27 | 2026.06.385 | PR #406** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.384 | PR #405** - A new controller-to-processor data processing agreement template was added, consolidating the mandatory GDPR Article 28 processor clauses into one fill-in instrument. This provides the single agreement instrument that was previously scattered across several documents.

**2026-06-27 | 2026.06.383 | PR #404** - The compliance alignment matrix's privacy section grew from 2 to 42 rows, mapping the privacy documents and 25 per-country jurisdiction annexes to the control frameworks. This gives adopters comprehensive privacy-domain framework coverage.

**2026-06-27 | 2026.06.382 | PR #403** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.381 | PR #402** - The compliance alignment matrix gained an AI domain section mapping 34 AI documents to the cloud-control, ISO/IEC 27001:2022, and NIST frameworks. This gives adopters framework-alignment coverage of the AI domain.

**2026-06-27 | 2026.06.380 | PR #401** - Session-closing handoff that also recorded a standing instruction to consult the shared reference base for every task.

**2026-06-27 | 2026.06.379 | PR #400** - Recorded the design and deferral of a paired-surface mechanical check.

**2026-06-27 | 2026.06.378 | PR #399** - Built the compliance-matrix semantic-fit review capability and wired its cadence into the AI-assistant guidance.

**2026-06-27 | 2026.06.377 | PR #398** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.376 | PR #397** - The README core-reference catalogue row for the enterprise governance-and-risk policy was corrected to its full title and moved into the Risk block to match the document's home domain. This fixes a title and categorization error in the README.

**2026-06-27 | 2026.06.375 | PR #396** - Recorded a validation review and added a fork-facing reference-base capability to the backlog.

**2026-06-27 | 2026.06.374 | PR #395** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.373 | PR #394** - Added an advisory tool that worklists compliance-matrix rows lacking a lexical anchor between a document and its cited control titles.

**2026-06-27 | 2026.06.372 | PR #393** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.371 | PR #392** - Eight mis-fitting cloud-control codes in the compliance matrix were corrected against their source control titles, and the same class of mislabel was fixed in seven security and governance documents' own framework tables. This corrects control mappings adopters rely on across the matrix and those documents.

**2026-06-27 | 2026.06.370 | PR #391** - Added a maintainer development aid to verify the internal control-reference modules against their source catalogues, and codified a standards-validation discipline.

**2026-06-27 | 2026.06.369 | PR #390** - Hardened an audit check to catch AI-focused cloud-control codes wrongly placed in the base cloud-control column.

**2026-06-27 | 2026.06.368 | PR #389** - Session-closing handoff bookkeeping.

**2026-06-27 | 2026.06.367 | PR #388** - Recorded a backlog item on measuring the assistant's own token usage and its current infeasibility.

**2026-06-27 | 2026.06.366 | PR #387** - Made the shared reference base durable and set it to be consulted at session resume.

**2026-06-27 | 2026.06.365 | PR #386** - Session-closing handoff bookkeeping for an overnight matrix-expansion session.

**2026-06-27 | 2026.06.364 | PR #385** - The compliance alignment matrix's security section grew by 25 rows covering the cryptography, identity, endpoint, incident, and personnel documents, and several source documents' framework tables had mis-cited control codes corrected. This gives adopters comprehensive security-domain coverage plus fixed citations.

**2026-06-27 | 2026.06.363 | PR #384** - The compliance alignment matrix's governance section grew by 15 rows covering the governance frameworks, guidelines, procedures, and registers. This broadens governance-domain framework coverage for adopters.

**2026-06-27 | 2026.06.362 | PR #383** - The compliance alignment matrix's compliance section grew by 25 rows covering the audit and corrective-action documents, sector annexes (financial services, energy, healthcare, public sector, telecommunications), and trade-compliance documents. This gives adopters comprehensive compliance-domain coverage.

**2026-06-26 | 2026.06.361 | PR #382** - Session-closing handoff bookkeeping.

**2026-06-26 | 2026.06.360 | PR #381** - Resolved two document-classification decisions and moved the project's own review-schedule register out of the published corpus into project-internal space.

**2026-06-26 | 2026.06.359 | PR #380** - The compliance alignment matrix's operations section grew by 11 rows covering the IT service-management, reliability, and operations documents. This gives adopters operations-domain framework coverage.

**2026-06-26 | 2026.06.358 | PR #379** - Session-closing handoff bookkeeping.

**2026-06-26 | 2026.06.357 | PR #378** - The compliance alignment matrix's resilience section grew from 3 to 21 rows covering the continuity, disaster-recovery, crisis, and incident documents. This gives adopters comprehensive resilience-domain coverage.

**2026-06-26 | 2026.06.356 | PR #377** - Session-closing handoff that addressed one review finding and recorded a paired-surface pattern.

**2026-06-26 | 2026.06.355 | PR #376** - Built two paired-surface completeness reminders in the AI-assistant guidance and the worker brief.

**2026-06-26 | 2026.06.354 | PR #375** - Codified a session wind-down decision framework in the AI-assistant instruction file.

**2026-06-26 | 2026.06.353 | PR #374** - A routine corpus-wide review corrected a NIST Cybersecurity Framework mapping description in a corrective-action procedure so its wording matched the framework function the code had been remapped to. This was an accuracy fix to a framework-mapping label, with no requirement changed.

**2026-06-26 | 2026.06.352 | PR #373** - Routine end-of-session handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.351 | PR #372** - Added an internal audit check that verifies NIST Cybersecurity Framework version 2.0 control codes wherever they appear across the documents.

**2026-06-26 | 2026.06.350 | PR #371** - Outdated NIST Cybersecurity Framework version 1.1 control codes were migrated to the current version 2.0 across three documents (supply-chain risk, security monitoring, and corrective action). Their framework mappings now reference codes that exist in the current framework.

**2026-06-26 | 2026.06.349 | PR #370** - Added a corpus-wide scanner (not yet enforced) to inventory outdated NIST Cybersecurity Framework control codes across the documents.

**2026-06-26 | 2026.06.348 | PR #369** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.347 | PR #368** - Added a developer helper that checks new changelog lines for dashes and unlinked file references before a commit.

**2026-06-26 | 2026.06.346 | PR #367** - Brought the audit programme's internal category index up to date; no published document changed.

**2026-06-26 | 2026.06.345 | PR #366** - Added a per-change check that a document's date is updated whenever its version is bumped.

**2026-06-26 | 2026.06.344 | PR #365** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.343 | PR #364** - Made per-session token and time tracking a standing internal convention.

**2026-06-26 | 2026.06.342 | PR #363** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.341 | PR #362** - Added an internal audit check that forbids the deliverable documents from linking into the project's own governance records.

**2026-06-26 | 2026.06.340 | PR #361** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.339 | PR #360** - Added an internal audit check ensuring no content linter hardcodes the set of audited directories.

**2026-06-26 | 2026.06.338 | PR #359** - Refactored the audit tooling to draw its list of audited directories from a single source; behaviour unchanged.

**2026-06-26 | 2026.06.337 | PR #358** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.336 | PR #357** - Added an internal audit check forbidding dashes in the maintainer working-notes tree.

**2026-06-26 | 2026.06.335 | PR #356** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.334 | PR #355** - Captured a design for preventing two work sessions from corrupting shared state, and queued its build.

**2026-06-26 | 2026.06.333 | PR #354** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.332 | PR #353** - Bulk conversion of dashes to plain punctuation across the maintainer working-notes files.

**2026-06-26 | 2026.06.331 | PR #352** - Updated the AI-assistant rule pack's own templates to drop a dash from its documented conventions.

**2026-06-26 | 2026.06.330 | PR #351** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-26 | 2026.06.329 | PR #350** - Queued a multi-session research-brief capability and sharpened a changelog-hygiene backlog item.

**2026-06-26 | 2026.06.328 | PR #349** - Documented an attended-autonomous operating mode for the AI assistant and its decision-timeout mechanism.

**2026-06-25 | 2026.06.327 | PR #348** - Refreshed the internal worker-accuracy metrics to the current state.

**2026-06-25 | 2026.06.326 | PR #347** - Closed out an autonomous overnight run and routed its decisions into the durable internal ledgers.

**2026-06-25 | 2026.06.325 | PR #346** - Routine session-start validation review; the only findings were in maintainer working notes and were fixed, with no published document changed.

**2026-06-25 | 2026.06.324 | PR #345** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.323 | PR #344** - Ran the first structural-coherence review of the audit machinery and recorded routine quality bookkeeping; no published document changed.

**2026-06-25 | 2026.06.322 | PR #343** - Added an internal audit check that confirms the required quality-bookkeeping records exist for each change.

**2026-06-25 | 2026.06.321 | PR #342** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.320 | PR #341** - The GRC compliance alignment matrix gained comprehensive supply-chain coverage, with a row for each supply-chain document mapped across eight frameworks. Adopters now have framework mappings for the supply-chain documents, including customs and trade-security programs where they apply.

**2026-06-25 | 2026.06.319 | PR #340** - Routine session-start validation review; two minor overstatements in a test note and the handoff were corrected, with no published document changed.

**2026-06-25 | 2026.06.318 | PR #339** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.317 | PR #338** - Extended two audit checks to also scan the project-governance directory and recorded the completeness obligation; no published document requirement changed.

**2026-06-25 | 2026.06.316 | PR #337** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.315 | PR #336** - Moved this project's own citation-verification campaign records out of the published governance domain into a separate project-governance directory.

**2026-06-25 | 2026.06.314 | PR #335** - Added a contributor acknowledgement and recorded a routine validation review; no published document content changed.

**2026-06-25 | 2026.06.313 | PR #334** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.312 | PR #333** - Folded two history-aware checks into the pre-push runner so a single invocation covers them.

**2026-06-25 | 2026.06.311 | PR #332** - Added guidance to the AI-assistant rule pack making parallel research fan-out the default for partitionable work.

**2026-06-25 | 2026.06.310 | PR #331** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-25 | 2026.06.309 | PR #330** - Added an internal runbook and worker brief for multi-session, multi-worker orchestration.

**2026-06-25 | 2026.06.308 | PR #329** - Routine session-start validation review plus bookkeeping; the only fix was a stale count in an internal skill file, with no published document changed.

**2026-06-25 | 2026.06.307 | PR #328** - Added a session-start clarification step to the AI-assistant's resume workflow.

**2026-06-25 | 2026.06.306 | PR #327** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-24 | 2026.06.305 | PR #326** - The compliance matrix's NIST Cybersecurity Framework codes were updated from the older version 1.1 to current version 2.0 categories, with 17 cells remapped. The matrix's audit check now also verifies each code names a real version 2.0 category.

**2026-06-24 | 2026.06.304 | PR #325** - Added an internal audit check validating the framework control codes cited in the compliance matrix.

**2026-06-24 | 2026.06.303 | PR #324** - Documented a convention for recording what a session verified so the next session can cross-check it.

**2026-06-24 | 2026.06.302 | PR #323** - A corpus-wide review qualified three cells in the privacy jurisdiction index that had presented Canada's proposed CPPA law as operative, marking them as applying only if enacted. This corrects a regime-status overstatement to match the rest of the corpus.

**2026-06-24 | 2026.06.301 | PR #322** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-24 | 2026.06.300 | PR #321** - The library's adopter starter sets were reconciled so the Day-1 minimum is a strict subset of the larger Tier 1 set, which grew from 15 to 17 documents by adding the acceptable-use and identity-and-access-management policies. The starter-set counts and framing were harmonized across the quickstart, adopter guide, decision tree, and README.

**2026-06-24 | 2026.06.298 | PR #320** - Across 29 documents, references treating Canada's never-enacted CPPA as a current privacy law were corrected to PIPEDA, the in-force federal regime, with CPPA-specific mentions qualified as proposed or pending. The distinct California Privacy Protection Agency of the same acronym was left untouched.

**2026-06-24 | 2026.06.297 | PR #319** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-24 | 2026.06.296 | PR #318** - The Go security-configuration example and the supplier-security questionnaire were updated to require TLS 1.3, completing a move away from TLS 1.2. This finishes two transport-security surfaces left over from an earlier migration.

**2026-06-24 | 2026.06.295 | PR #317** - The compliance matrix gained comprehensive dev-security coverage, mapping all 17 dev-security documents across eight frameworks. Adopters now have framework mappings for the dev-security documents.

**2026-06-24 | 2026.06.294 | PR #316** - Recovered a stranded design record onto the main branch and queued a related codification track; no published document content changed.

**2026-06-24 | 2026.06.293 | PR #315** - A corpus-wide review corrected two long-standing errors in the compliance matrix: a WCO SAFE customs pillar was fixed to Customs-to-Business, and inconsistent no-mapping markers were normalized. These were accuracy fixes to the matrix present since first release.

**2026-06-24 | 2026.06.292 | PR #314** - Added a new governance specification defining the boundary between the reusable governance content the library publishes and the operational records of running the project. It sets a one-way dependency rule and classifies where each governance artefact belongs.

**2026-06-24 | 2026.06.291 | PR #313** - The compliance matrix's Risk section expanded from 3 to all 15 risk documents mapped across eight frameworks, and a WCO SAFE customs-pillar mislabelling was corrected matrix-wide. Adopters get comprehensive risk-domain framework mappings and a corrected customs pillar label.

**2026-06-24 | 2026.06.290 | PR #312** - A corpus-wide review corrected an AI risk register's impact scale label so its top level reads Catastrophic, matching the canonical risk scale. This aligned the register's scoring vocabulary with the rest of the risk documents.

**2026-06-24 | 2026.06.289 | PR #311** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-24 | 2026.06.288 | PR #310** - Four risk-scoring documents had their likelihood and impact scale labels harmonized to the canonical enterprise-risk scale, for example unifying impact level 5 as Catastrophic and standardizing the likelihood labels. This removes divergences that let the same risk score read differently across documents.

**2026-06-24 | 2026.06.287 | PR #309** - Enhanced an existing audit check to also flag bare, superseded cloud-controls domain codes.

**2026-06-24 | 2026.06.286 | PR #308** - Enhanced an existing audit check to compare cloud-controls titles against the correct catalogue for the section they appear in.

**2026-06-24 | 2026.06.285 | PR #307** - Morning processing of an overnight run: routed its notes into durable ledgers and closed a relocation decision; no published document changed.

**2026-06-24 | 2026.06.284 | PR #306** - A corpus-wide review corrected two operations documents' CSA Cloud Controls Matrix mappings: superseded version 4.0 domain names were updated to version 4.1, and a mis-cited network-security code used for physical security was corrected to the datacenter-security controls. These fix inaccurate framework citations.

**2026-06-24 | 2026.06.283 | PR #305** - Generalized a session-closing quality-review exception into the distributable AI-assistant rule pack for adopters.

**2026-06-24 | 2026.06.282 | PR #304** - Moved this repository's own branch-protection configuration snapshot out of the published corpus into maintainer working notes.

**2026-06-24 | 2026.06.281 | PR #303** - The startup roadmap's named Day-1 risk artefact was aligned to the quickstart and adopter guide, naming the enterprise governance and risk management policy. This resolves a divergence in which document the two on-ramps called the Day-1 risk starting point.

**2026-06-24 | 2026.06.280 | PR #302** - Corrected a stale audit-count phrase in an internal skill file; no published document changed.

**2026-06-24 | 2026.06.279 | PR #301** - A corpus-wide review corrected superseded and fabricated CSA Cloud Controls Matrix domain codes across 13 documents (for example the retired IVS domain updated to Infrastructure Security, and invented domains removed) and brought version strings current. These fix inaccurate cloud-controls framework citations.

**2026-06-24 | 2026.06.278 | PR #300** - A cloud-controls migration control's title in the compliance-controls register was corrected to its Cloud Controls Matrix version 4.1 wording. This citation-title accuracy fix was carried alongside session-closing bookkeeping.

**2026-06-24 | 2026.06.277 | PR #299** - A new audit check now validates that cited cloud-controls (CSA Cloud Controls Matrix and AI Controls Matrix) codes name real domains and correct titles, and the compliance-controls gap register's 54 control titles were aligned to the authoritative catalogues. Adopters get accurate control titles in that register.

**2026-06-24 | 2026.06.276 | PR #298** - Across 33 documents, incorrect cloud-controls citations were reconciled to the authoritative CSA catalogues: a fabricated governance domain was corrected to the real one, the superseded IVS domain updated to I&S, out-of-range codes fixed, and the AI Controls Matrix version brought current. This makes the corpus's cloud-controls citations accurate.

**2026-06-24 | 2026.06.275 | PR #297** - The asset inventory register's criticality tier labels were aligned to the Service Level Management standard's canonical labels, completing a cross-document harmonization. This gives consistent criticality terminology across the affected documents.

**2026-06-24 | 2026.06.274 | PR #296** - A cross-document consistency bundle corrected several items: an AI adversarial-test-category claim was made count-agnostic, a Japan APPI age claim was softened to match the law, a multi-domain post-incident-review deadline was fixed, recovery-tier labels were aligned, and IT and security log retention was widened to seven years to cover AI decision logs. These touch AI, privacy, resilience, records, and logging documents.

**2026-06-24 | 2026.06.273 | PR #295** - Refreshed the internal worker-accuracy metrics table from live records; no published document changed.

**2026-06-23 | 2026.06.272 | PR #294** - A seven-item governance and ESG bundle updated several documents: a 180-day exception-review interval was reframed as the library's own convention rather than attributed to standards that do not prescribe it, a stale CSA governance domain code was corrected, AI-log retention was reconciled to seven years, and qualitative double-materiality and ESG-escalation processes were added. These add content and fix attributions across governance, AI, and sustainability documents.

**2026-06-23 | 2026.06.271 | PR #293** - A corpus-wide review softened an inaccurate claim in two adopter-onboarding documents that the Day-1 starter set nests inside the Tier 1 set, stating the accurate partial overlap instead, and reconciled a breach-response role lead-in with its table. These correct onboarding and breach-response guidance.

**2026-06-23 | 2026.06.270 | PR #292** - A governance index row's descriptor for the BYOD policy was updated to note it now covers both mobile-application and mobile-device management. This kept the index accurate after the policy was broadened.

**2026-06-23 | 2026.06.269 | PR #291** - A six-item security bundle updated the encryption policy's password-hashing parameters to current OWASP guidance, reframed the BYOD policy to support both mobile-application and mobile-device management models, and added browser-hardening requirements (Content-Security-Policy and Strict-Transport-Security) to the developer-security standard. It also made incident, patch, and recovery documents more actionable across several security, privacy, and resilience files.

**2026-06-23 | 2026.06.268 | PR #290** - A ten-item bundle improved the adopter documentation: the contributing guide, adopter guide, quickstart, decision tree, and startup roadmap gained fork-merge and audit-relaxation guidance, overlapping-regulator guidance, starter-set nesting notes, and terminology clarifications. This makes onboarding and customization clearer.

**2026-06-23 | 2026.06.267 | PR #289** - A corpus-wide review generalized a mapping-table column in the cloud-security configuration baseline and named which CIS benchmark governs each section. This corrects the attribution of CIS benchmark areas.

**2026-06-23 | 2026.06.266 | PR #288** - A corrective-action procedure's timeline was corrected from 90 business days to 90 days to match the compliance policy it cites. This small consistency fix was carried with session-closing bookkeeping.

**2026-06-23 | 2026.06.265 | PR #287** - A seven-item assurance and audit bundle updated the internal-audit, corrective-action, assurance-map, change-management, cloud-baseline, glossary, and incident-response documents, adding a report-extension acknowledgement, an effectiveness-validation step, gap-closure sign-off, a compensating-control pathway, ISO and CIS mappings, a Three Lines Model definition, and incident-command checklists. These make the assurance and audit guidance more complete.

**2026-06-23 | 2026.06.264 | PR #286** - A corpus-wide review harmonized the operational-risk-register template's treatment-decision and status field definitions to the canonical enterprise-risk vocabulary. This gives consistent risk-register terminology.

**2026-06-23 | 2026.06.263 | PR #285** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-23 | 2026.06.262 | PR #284** - Five sample rows in the AI risk register were updated to the canonical Open status to match the field definition. This corrected example data left inconsistent by an earlier vocabulary change.

**2026-06-23 | 2026.06.261 | PR #283** - The AI risk register, AI risk-methodology annex, and enterprise-risk-register template had their treatment-option and status vocabularies aligned to the canonical enterprise-risk set (six treatment options and Open or Closed status). This gives consistent risk vocabulary across those documents.

**2026-06-23 | 2026.06.260 | PR #282** - Two AI assessment procedures gained roles-and-responsibilities subsections assigning an owner to each step, and a looping supplier-onboarding escalation path was corrected to end at the Chief Risk Officer. These add accountability and fix a broken escalation path.

**2026-06-23 | 2026.06.259 | PR #281** - Routine session-start validation review plus a backlog restructure; the only fixes were audit-reference mislabels in the backlog file, with no published document changed.

**2026-06-23 | 2026.06.258 | PR #280** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-23 | 2026.06.257 | PR #279** - The IT disaster-recovery plan's backup-requirements header was broadened from Tier 1 and 2 to all systems, since its bullets already span every tier. This corrected the stated scope.

**2026-06-23 | 2026.06.256 | PR #278** - Added a per-change check that new changelog lines follow the no-dash style, leaving historical entries untouched.

**2026-06-23 | 2026.06.255 | PR #277** - A corpus-wide review corrected five documents citing a nonexistent Cloud Controls Matrix version 5 to version 4.1 (one also fixing a stale domain code), and broadened the citation audit check to catch the spelled-out form. This fixes hallucinated framework-version citations.

**2026-06-23 | 2026.06.254 | PR #276** - Session-closing checkpoint bookkeeping and an update to the internal worker-brief template; no published document changed.

**2026-06-23 | 2026.06.253 | PR #275** - The compliance alignment matrix began a comprehensive expansion, adding the Architecture domain with eight documents mapped across all eight frameworks. This starts extending framework mappings from a curated subset toward the full document set.

**2026-06-23 | 2026.06.252 | PR #274** - Session-closing handoff bookkeeping; no published document changed.

**2026-06-23 | 2026.06.251 | PR #273** - Corrected a stale audit count in a health-report template and broadened the audit-count consistency check to catch its phrasing.

**2026-06-23 | 2026.06.250 | PR #272** - Added an internal audit check and helper that ensure every new document appears on the listing surfaces that should reference it.

**2026-06-23 | 2026.06.249 | PR #271** - A corpus-wide review corrected the IT disaster-recovery plan's Tier 2 backup cadence to every four hours to match its four-hour recovery-point objective, which had been left at daily. This removes a contradiction that would keep compliant Tier 2 systems in permanent escalation.

**2026-06-23 | 2026.06.248 | PR #270** - Session-closing handoff, a final validation review, and overnight-run processing; the one content decision was queued for later, with no published document changed.

**2026-06-23 | 2026.06.247 | PR #269** - Cleanup after a validation review: corrected a stale tool description, with the one corpus finding deferred; no published document changed.

**2026-06-23 | 2026.06.246 | PR #268** - Session-closing handoff bookkeeping for an authorized overnight run; no published document changed.

**2026-06-23 | 2026.06.245 | PR #267** - An invented 72-hour PIPEDA breach-reporting deadline was removed from the breach-response and incident-response procedures and replaced with the accurate as soon as feasible, no fixed statutory deadline. This corrects a fabricated Canadian regulatory deadline while leaving the genuine GDPR and Quebec 72-hour references intact.

**2026-06-23 | 2026.06.244 | PR #266** - A validation review fixed several consistency items, notably re-grounding a record-of-processing template's lawful-basis example on the in-force PIPEDA (from the not-in-force CPPA) and raising an identity-and-access log-retention floor to match the canonical retention schedule. These correct a legal basis and a retention value in published documents.

**2026-06-23 | 2026.06.243 | PR #265** - The IT disaster-recovery plan's Tier 1 backup cadence was changed to continuous or near-continuous protection to meet its one-hour recovery-point objective, replacing an impossible daily-backup requirement. This removes a self-contradiction for mission-critical systems.

**2026-06-23 | 2026.06.242 | PR #264** - Three privacy documents that cited Canada's never-enacted CPPA (with invented section numbers) as a live legal basis were corrected to the in-force PIPEDA Schedule 1 principles. This fixes a fabricated Canadian privacy legal basis in the data-subject-rights, breach-response, and privacy-governance documents.

**2026-06-23 | 2026.06.241 | PR #263** - Three documents that disagreed on how long data-subject-access-request records are kept were harmonized to three years, the value in the authoritative retention schedule. This gives a single consistent retention period.

**2026-06-23 | 2026.06.240 | PR #262** - Conflicting log-retention periods across the logging standard, records standard, and monitoring procedure were reconciled to defer to the tiered data-retention schedule as the authoritative source. This replaces three different answers with one, preserving the seven-year AI decision-log tier.

**2026-06-23 | 2026.06.239 | PR #261** - Every organization TLS-floor surface across the corpus was migrated to require TLS 1.3, with TLS 1.2 moved to the prohibited set, resolving self-contradictions on the minimum. Two surfaces representing an external baseline and a code example were deliberately deferred.

**2026-06-23 | 2026.06.238 | PR #260** - The enterprise-risk-management standard's risk-scoring scale (likelihood labels and score-to-rating bands) was realigned to the canonical risk-assessment methodology, and a risk-register template's stale likelihood labels were fixed. This ensures the same risk score no longer yields different ratings depending on which document is read.

**2026-06-23 | 2026.06.237 | PR #259** - Initiated an authorized autonomous overnight run and recorded its authorization and design decisions; no published document changed.

**2026-06-23 | 2026.06.236 | PR #258** - Distributed the project's apex integrity rule as a reusable governance rule in the AI-assistant rule pack for adopters.

**2026-06-23 | 2026.06.235 | PR #257** - Added a periodic structural-coherence review capability for the governance machinery to the AI-assistant rule pack.

**2026-06-23 | 2026.06.234 | PR #256** - A validation review corrected stale descriptions in the AI-assistant rule pack's readme; no published corpus document changed.

**2026-06-23 | 2026.06.233 | PR #255** - Session-closing handoff that added AI-assistant resume-hardening guardrails; no published document changed.

**2026-06-23 | 2026.06.232 | PR #254** - Internal addition of a convenience command that runs the AI-assistant's escalated quality-review steps in sequence.

**2026-06-22 | 2026.06.231 | PR #253** - Internal completion of a revision to how the AI-assistant's escalated review sorts findings, plus a log of a commit-signing service outage.

**2026-06-22 | 2026.06.230 | PR #252** - Internal revision of how the AI-assistant's escalated review sorts its findings by severity.

**2026-06-22 | 2026.06.229 | PR #251** - Internal record of the maintainer's backlog-priority decisions; no published document changed.

**2026-06-22 | 2026.06.228 | PR #250** - Routine start-of-session corpus-wide validation review; the only fix was a stale count in an internal AI-assistant instruction file.

**2026-06-22 | 2026.06.227 | PR #249** - Internal fix to the AI-assistant's end-of-session review process so it no longer loops at session boundaries.

**2026-06-22 | 2026.06.226 | PR #248** - Internal end-of-session handoff bookkeeping and a note on why long AI-assistant sessions degrade.

**2026-06-22 | 2026.06.225 | PR #247** - Internal addition of a session-handoff record and resume procedure for the AI-assistant; no published document changed.

**2026-06-22 | 2026.06.224 | PR #246** - Internal addition of a governance rule describing when the AI-assistant escalates to a heavier review after process lapses.

**2026-06-22 | 2026.06.223 | PR #245** - Internal addition of a top-priority integrity rule governing the AI-assistant's work.

**2026-06-22 | 2026.06.222 | PR #244** - Internal addition of a forensic quality-review procedure for the AI-assistant.

**2026-06-22 | 2026.06.221 | PR #243** - Internal run of a heavier quality-review suite after prior process lapses; findings were routed to the backlog and no published document changed.

**2026-06-22 | 2026.06.220 | PR #242** - A validation review found that a risk-treatment vocabulary update had not reached four risk documents (a policy, a methodology procedure, a register procedure, and a risk-register template). The canonical six treatment options and three treatment-status values were propagated into those documents so they agree.

**2026-06-22 | 2026.06.219 | PR #241** - Corrected the ISO 31000:2018 clause numbers cited in the cross-framework alignment matrix, and added an evidence-type column to the EU NIS 2 Directive Article 21.2 measures table. Adopters get accurate clause references and a clearer statement of what evidence each NIS 2 measure requires.

**2026-06-22 | 2026.06.218 | PR #240** - Added two fields to the key-risk-indicator register (who escalates a breached red threshold, and what evidence is captured on breach) and clarified in the assurance-map register that adopters supply their own control-identifier scheme. Adopters get clearer breach-escalation ownership and control-register guidance.

**2026-06-22 | 2026.06.217 | PR #239** - Aligned the risk-register procedure's risk-treatment options with the canonical six-option set in the enterprise-risk-management standard, noting that 'Monitor' and 'Further Analysis' are workflow states rather than treatment options. This removes a conflict between the two documents' vocabularies.

**2026-06-22 | 2026.06.216 | PR #238** - Resolved an internal inconsistency in the enterprise-risk-management standard by distinguishing the treatment option, the treatment-execution status, and the risk-record lifecycle status, and splitting the register's overloaded status field into three. This removes ambiguity about how to record an avoided or accepted risk.

**2026-06-22 | 2026.06.215 | PR #237** - Added a table of the digital-consent age (13 to 16) for each EU and EEA country under GDPR Article 8, with national-law citations, to the European Union privacy annex. Adopters operating across the EU can now apply the correct per-country age rather than a single figure.

**2026-06-22 | 2026.06.214 | PR #236** - Added a GDPR data-protection-officer independence cross-reference to the role-authority register and extended the citations register to cover soft-law supervisory guidance, adding the Article 29 Working Party data-protection-officer guidelines. Adopters get clearer DPO-independence pointers and a citable soft-law reference.

**2026-06-22 | 2026.06.213 | PR #235** - Sharpened the emergency-access provisions in the access-control procedure: defined the harm threshold, tied triggers to top-severity incidents, added a delegated security-lead role, resolved a revocation-timeline contradiction, and added an escalation chain. Adopters get concrete, non-contradictory emergency-access rules (with sample defaults to adjust on adoption).

**2026-06-22 | 2026.06.212 | PR #234** - Added a new capacity tier to the startup-roadmap template for organizations whose governance-risk-compliance function is entirely outsourced with no in-house staff. Such adopters now have a matching rung on the maturity ladder.

**2026-06-22 | 2026.06.211 | PR #233** - Strengthened the API-security standard with a requirement that JSON Web Token validators bind the algorithm to the key type (preventing a known confusion attack), plus detailed webhook-signing and replay-prevention rules. Adopters get more precise, attack-aware API-security requirements.

**2026-06-22 | 2026.06.210 | PR #232** - Improved the adopter guide by explaining early which of the two reference registers holds acronyms versus internal concepts, adding a reading-time estimate for the starter document set, and naming three documents to read first. Newcomers get a gentler on-ramp.

**2026-06-22 | 2026.06.209 | PR #231** - Clarified in the README that the audit toolchain is the maintainer's quality machinery and not something adopters must run, and repointed the quickstart's core-baseline risk anchor to the enterprise governance-and-risk policy. Adopters get accurate expectations and a consistent starter set.

**2026-06-22 | 2026.06.208 | PR #230** - Internal reorganization of the maintainer's backlog file into clean priority sections.

**2026-06-22 | 2026.06.207 | PR #229** - A validation review added three missing glossary entries (for authenticated encryption, critical information infrastructure operators, and a key-derivation function) and added a cross-reference in the privacy policy to the data-protection-officer conflict-of-interest material. Adopters get a more complete glossary and better-linked privacy guidance.

**2026-06-22 | 2026.06.206 | PR #228** - Added a framework to the privacy-management charter covering the GDPR Article 38 requirements for data-protection-officer independence and conflict of interest, including the risk of a CIO acting as interim data-protection officer and how to mitigate it. Adopters get concrete guidance on structuring the role compliantly across several privacy regimes.

**2026-06-22 | 2026.06.205 | PR #227** - Expanded China PIPL cross-border-transfer guidance in the privacy-impact-and-transfer procedure into a detailed workflow covering mechanism selection by data volume, separate consent, and local-storage duties, reflecting the 2024 data-flow provisions. Adopters transferring personal data out of China get a step-by-step compliance path.

**2026-06-22 | 2026.06.204 | PR #226** - Added a dedicated section to the privacy-management charter on appointing an EU representative under GDPR Article 27, covering the trigger criteria, exemptions, designation steps, and equivalents in other regimes. Adopters without an EU establishment get a clear appointment process.

**2026-06-22 | 2026.06.203 | PR #225** - Expanded the data-subject-rights procedure with a structured checklist for handling manifestly unfounded or excessive requests under GDPR Article 12(5), including the tests, the charge-or-refuse options, documentation, and cross-regime equivalents. Adopters get a defensible process for pushing back on abusive requests.

**2026-06-22 | 2026.06.202 | PR #224** - Added a new template for joint-controller arrangements under GDPR Article 26 and equivalent regimes, with a full responsibility-allocation table, liability terms, and a publication section. Adopters sharing controller responsibilities get a ready-to-adapt agreement.

**2026-06-22 | 2026.06.201 | PR #223** - Renamed a section heading from 'Governance' to 'Governance and accountability' across fourteen documents to match the form used elsewhere in the corpus. Adopters get consistent section naming across the library.

**2026-06-22 | 2026.06.200 | PR #222** - Corrected a cryptography row in the encryption-and-key-management policy that had conflated encryption, integrity, and key derivation under an ambiguous 'key hashing' phrase, replacing it with precise choices for each purpose. Adopters get technically correct cryptographic guidance.

**2026-06-22 | 2026.06.199 | PR #221** - Separated the GDPR Article 36 regulatory prior-consultation pathway from internal executive sign-off in the privacy-impact procedure, adding the trigger criteria, required content, and timeline, with non-EU equivalents. Adopters facing high residual assessment risk get a clear regulator-consultation process.

**2026-06-22 | 2026.06.198 | PR #220** - A validation review corrected two leftover 'Chief Privacy Officer' acronym references to 'Data Protection Officer' in a minimum-viable-governance guideline, completing an earlier rename. Adopters see consistent privacy-lead role naming.

**2026-06-22 | 2026.06.197 | PR #219** - Added a short role-name convention note to the top of twenty-four privacy-relevant documents, stating that Data Protection Officer is the canonical privacy-lead role and Chief Privacy Officer is an adopter substitution. Adopters landing directly in one of these documents see the convention inline.

**2026-06-22 | 2026.06.196 | PR #218** - Made Data Protection Officer the canonical privacy-lead role across the corpus (renamed from Chief Privacy Officer in seventy-three files), because the term has legislative force in many jurisdictions, with Chief Privacy Officer noted as an adopter substitution. Adopters get a globally applicable role name with clear substitution guidance.

**2026-06-22 | 2026.06.195 | PR #216** - Internal correction of a changelog count and a stale backlog sync reference.

**2026-06-22 | 2026.06.194 | PR #215** - Internal recording of a clean corpus validation review; no published document changed.

**2026-06-22 | 2026.06.193 | PR #214** - Internal morning cleanup after an overnight work session, routing notes and resetting the session file.

**2026-06-22 | 2026.06.192 | PR #213** - Internal addition of a post-merge retrospective process and improvement log for the AI-assistant.

**2026-06-22 | 2026.06.191 | PR #212** - Realigned two documents to the standard five-level CMMI maturity ladder (Initial, Managed, Defined, Quantitatively Managed, Optimized): the maturity self-assessment template's tier names and the digital-trust metrics register's threshold bands. Adopters get consistent maturity-level naming.

**2026-06-22 | 2026.06.190 | PR #211** - Unified the Risk Owner role across the enterprise-risk-management standard and the exception-and-risk-acceptance policy, adding a sixth accountability (validating the risk assessment behind an exception request) and a cross-reference. Adopters get one consistent definition of the Risk Owner.

**2026-06-22 | 2026.06.189 | PR #210** - Standardized 'Privacy Officer' to 'Chief Privacy Officer' across thirty-six documents, treating them as the same role. Adopters see consistent privacy-lead role naming.

**2026-06-22 | 2026.06.188 | PR #209** - Changed the review-frequency wording in two documents from 'annual or upon material change' to 'annual and upon material change', so both triggers are required. Adopters get a review cadence consistent with the rest of the corpus.

**2026-06-22 | 2026.06.187 | PR #208** - Standardized ISO/IEC 27001 control references to the 'Annex A.X' form matching the publisher's convention across the corpus. Adopters get citations that match the standard's own labeling.

**2026-06-22 | 2026.06.186 | PR #207** - Standardized NIST publication citations to the 'Rev. N' form with a period, matching NIST's convention, across fifty documents. Adopters get consistent, publisher-accurate NIST references.

**2026-06-22 | 2026.06.185 | PR #206** - Completed the private and reserved IP-range list for server-side-request-forgery defence (now covering both IPv4 and IPv6 with RFC citations) and enumerated the approved TLS 1.3 cipher suites and rejected categories in the API-security standard. Adopters get precise request-forgery and cipher-suite requirements.

**2026-06-22 | 2026.06.184 | PR #205** - Internal alignment of the AI-assistant pack's TLS guidance to the corpus encryption policy, plus routine count corrections.

**2026-06-22 | 2026.06.183 | PR #204** - Internal verification pass over a review's findings; no published document changed.

**2026-06-22 | 2026.06.182 | PR #203** - Restructured the privacy section of the adopter decision-tree so the full jurisdiction index (25 jurisdictions) is surfaced prominently rather than buried, keeping the four common Anglosphere picks as examples. Adopters more easily find the non-Anglosphere jurisdiction annexes.

**2026-06-22 | 2026.06.181 | PR #202** - Internal overnight-session wrap-up recording progress and open questions; no published document changed.

**2026-06-22 | 2026.06.180 | PR #201** - Raised the minimum TLS version to 1.3 or stronger in the developer-security-requirements and API-security standards, aligning them with the corpus encryption policy. Adopters get a consistent, current minimum transport-security version.

**2026-06-22 | 2026.06.179 | PR #200** - Added notes to the adopter decision-tree's orientation list explaining that acronyms are expanded on first use in the earliest-read documents, so the glossary is reserved for deeper documents. Adopters better understand when to reach for the glossary.

**2026-06-22 | 2026.06.178 | PR #199** - Added a table to the enterprise-risk-management standard mapping each Risk Owner accountability action to the evidence that proves it was performed. Adopters get an explicit evidence expectation for the Risk Owner role.

**2026-06-22 | 2026.06.177 | PR #198** - Added explicit Risk Owner review cadences by risk-score band (annual, quarterly, monthly) to the enterprise-risk-management standard, matching its score-threshold table. Adopters get clear review intervals for each severity.

**2026-06-22 | 2026.06.176 | PR #197** - Added the Risk Owner role to the canonical role-authority register (it previously existed only in the risk standard), with its accountabilities and approval authority, plus a reciprocal cross-reference. Adopters find the Risk Owner in the single source of truth for roles.

**2026-06-22 | 2026.06.175 | PR #196** - Expanded two acronyms (corrective-and-preventive-action and security-information-and-event-management) on first use in the README's repository-structure section. Newcomers reading the README are not stopped by undefined acronyms.

**2026-06-22 | 2026.06.174 | PR #195** - Raised the retention period for internal audit reports from five to seven years in the data-retention schedule, aligning it with the internal-audit standard's seven-year minimum. Adopters get a consistent audit-evidence retention period.

**2026-06-22 | 2026.06.173 | PR #194** - Raised the retention period for corrective-and-preventive-action records from five to seven years in the data-retention schedule, closing a break with the corrective-action procedure. Adopters keep remediation records at least as long as the findings they address.

**2026-06-22 | 2026.06.172 | PR #193** - Raised the encryption-in-transit expectation in the zero-trust-architecture framework from TLS 1.2 to TLS 1.3 or stronger, aligning it with the encryption policy. Adopters get a current minimum transport-security version in the zero-trust guidance.

**2026-06-22 | 2026.06.171 | PR #192** - Internal codification of a rule that folds validation findings into the next planned change to avoid a cascade of tiny follow-up changes.

**2026-06-22 | 2026.06.170 | PR #191** - Internal recording of a post-merge validation review that found nothing; no published document changed.

**2026-06-22 | 2026.06.169 | PR #190** - Internal fixes to review records plus new AI-assistant conventions on working in UTC and surfacing findings in chat.

**2026-06-22 | 2026.06.168 | PR #189** - Internal correction of review-record labeling and a stale note in the AI-assistant pack readme.

**2026-06-22 | 2026.06.167 | PR #188** - Internal end-of-day close-out recording a review and fixing review-record inconsistencies; no published document changed.

**2026-06-22 | 2026.06.166 | PR #187** - Internal codification of a rule that the AI-assistant may not skip the mandated post-merge quality review.

**2026-06-21 | 2026.06.165 | PR #186** - Internal corpus validation review; the only fixes were to AI-assistant tooling and pack files.

**2026-06-21 | 2026.06.164 | PR #185** - Internal recording of a post-merge validation review; no published document changed.

**2026-06-21 | 2026.06.163 | PR #184** - Internal addition of a worker-brief template and a protocol for improving it as the AI-assistant catches new error classes.

**2026-06-21 | 2026.06.162 | PR #183** - Internal addition of a per-change post-merge validation review procedure for the AI-assistant.

**2026-06-21 | 2026.06.161 | PR #182** - Internal editorial sweep removing a drift-prone category count from the audit-programme specification.

**2026-06-21 | 2026.06.160 | PR #181** - Internal corpus validation review; fixes were limited to a backlog note and an AI-assistant pack file.

**2026-06-21 | 2026.06.159 | PR #180** - Internal calibration of the AI-assistant's version-and-date bump discipline; no published document changed.

**2026-06-21 | 2026.06.158 | PR #179** - Shipped six document improvements: an exception-term rationale in the exception policy, control-testing evidence retention raised to seven years, a vendor product name genericized in the tabletop-exercise template, a NIST framework label normalized in the information-security policy, trade-programme acronyms expanded in the README, and a navigation pointer clarified in the decision-tree. Adopters get several accuracy and clarity fixes across these documents.

**2026-06-21 | 2026.06.157 | PR #178** - Defined the Risk Owner as a distinct role in the enterprise-risk-management standard and fixed several within-document risk-treatment vocabulary inconsistencies, including extending the register's treatment options to the full six. Adopters get a clearer role definition and consistent treatment terms.

**2026-06-21 | 2026.06.156 | PR #177** - Internal recording of the phased execution plan in the backlog file.

**2026-06-21 | 2026.06.155 | PR #176** - Internal addition of a governance rule describing five disciplines for the AI-assistant's multi-change work.

**2026-06-21 | 2026.06.154 | PR #175** - Internal reformatting of the maintainer's closed-work ledger to short one-line entries.

**2026-06-21 | 2026.06.154 | PR #174** - Internal change to the change-tracking rule replacing the skip option with a required terse entry for every change.

**2026-06-21 | 2026.06.153 | PR #173** - Internal backfill of two missing changelog entries.

**2026-06-21 | 2026.06.152 | PR #171** - Internal addition of an AI-assistant discipline for waiting on automated-check results.

**2026-06-21 | 2026.06.152 | PR #170** - Internal addition of an AI-assistant version-bump discipline note.

**2026-06-21 | 2026.06.153 | PR #172** - Made five polish improvements to the README: an acronym-heavy sentence became a bulleted list with expansions, a vague document count was replaced with a pointer to the machine-generated index, the version-policy note was folded into a table, the 'where to go next' guidance became a table, and the two version lines were demoted. Adopters get a clearer, less cluttered front page.

**2026-06-21 | 2026.06.152 | PR #169** - Improved the access-control procedure with a tiered escalation ladder for approval delays, four bounded acceptance criteria for access reviews, and explicit trigger conditions and revocation consequences for emergency access. Adopters get more precise access-control rules.

**2026-06-21 | 2026.06.150 | PR #168** - Expanded the data-classification enumeration in the BASC information-security policy from three levels to the canonical five, with a cross-reference to the data-classification standard. Adopters get a classification scheme consistent with the rest of the library.

**2026-06-21 | 2026.06.149 | PR #167** - A validation review corrected a stale file reference in the implementation-roadmap template and fixed a misstated ISO/IEC 29134 edition (2023 to the verifiable 2017) in the privacy-impact-assessment template and the document index. Adopters get accurate references and citations.

**2026-06-21 | 2026.06.148 | PR #166** - Split the overlong 'quickstart' into a genuine ten-minute quickstart and a renamed longer 'startup roadmap', preserving the detailed content and adding a true short on-ramp. Adopters get a real quick start plus the fuller roadmap when they need it.

**2026-06-21 | 2026.06.147 | PR #165** - Reconciled the library's several adopter entry points by declaring the portal the canonical front door and adding an 'other entry points and when to use them' table, with a matching preface in four adopter-facing documents. Adopters understand how the guides, quickstart, decision-tree, and roadmap relate.

**2026-06-21 | 2026.06.146 | PR #164** - Reconciled the data-classification levels across the corpus by propagating the canonical five-level scheme (Public, Controlled, Internal, Confidential, Restricted) into six documents that had listed only four, and marking the canonical standard authoritative. Adopters get one consistent classification scheme library-wide.

**2026-06-21 | 2026.06.145 | PR #163** - Internal reformatting of the maintainer's closed-work ledger headings for scannability.

**2026-06-21 | 2026.06.144 | PR #162** - Added a data-protection-impact-assessment template covering the three limbs of GDPR Article 35 (trigger checklist, high-risk criteria, mandatory content, and sign-off), with cross-regime framework alignment. Adopters can now evidence Article 35 compliance from a ready template.

**2026-06-21 | 2026.06.143 | PR #161** - Aligned the exception policy's approval pathway with the role-authority register's approval-accountability row, naming the tiered approvers and the adopter-tunable thresholds. Adopters get one consistent statement of who approves exceptions.

**2026-06-21 | 2026.06.142 | PR #160** - A validation review fixed requirement-language slips introduced the same day: a legacy 'shall' in the master specification and two prohibition uses of 'may not' in the exception policy, all converted to 'must' or 'must not'. Adopters get consistent normative wording.

**2026-06-21 | 2026.06.141 | PR #159** - Documented the library's requirement-language convention in the master specification: 'must' and 'must not' for requirements, 'should' for recommendations, 'may' for permissions, and 'shall' reserved for quoting external standards, citing RFC 2119. Adopters get an explicit, consistent normative vocabulary.

**2026-06-21 | 2026.06.140 | PR #158** - Resolved an apparent contradiction between the data-retention schedule (three years for security event logs) and the cloud-security baseline (90-day minimum) by reframing the 90 days as the forwarding floor and naming the central log system as the long-term retention authority. Adopters get consistent log-retention guidance across the two documents.

**2026-06-21 | 2026.06.139 | PR #157** - Added hard ceiling fields to the exception register (a maximum cumulative duration and a renewal-count limit) and a renewal-escalation pathway to the exception policy, preventing indefinite exception drift. Adopters get enforceable limits on how long an exception can persist.

**2026-06-21 | 2026.06.138 | PR #156** - Reordered the README's how-to-use step so it points readers to the audience-keyed portal first and the large document index second. Adopters get consistent signposting to the portal as the front door.

**2026-06-21 | 2026.06.137 | PR #155** - Rewrote the README's what-this-is section so the governance documentation corpus is the unambiguous headline product and the audit toolchain and rule pack are positioned as the maintenance layer beneath it. Adopters get a clearer statement of what the library primarily offers.

**2026-06-21 | 2026.06.136 | PR #154** - A validation review tightened prohibition wording in two AI-security documents, added escalation-owner and remediation-sign-off columns to the BASC IT-compliance performance-indicator register, and backfilled a document-history table. Adopters get consistent requirement wording and a fuller indicator register.

**2026-06-21 | 2026.06.135 | PR #153** - Added escalation-owner and remediation-sign-off columns to every table in the IT-operations performance-indicator register, drawing roles from the role-authority register. Adopters get clear accountability for breached and closed indicators.

**2026-06-21 | 2026.06.134 | PR #152** - Strengthened the corrective-and-preventive-action procedure with a five-criterion root-cause quality checklist and a hard ceiling on target-date extensions (escalating, then not permitted). Adopters get enforceable limits so findings cannot remain open indefinitely.

**2026-06-21 | 2026.06.133 | PR #151** - Made explicit in the privacy-breach-response procedure that a processor's contractual 24-hour notification clock starts at the processor's awareness of a breach, distinct from the controller's 72-hour clock under GDPR Article 33. Adopters get a clear two-clock model for breach-notification timelines.

**2026-06-21 | 2026.06.132 | PR #150** - Changed 'may not' to 'must not' where a prohibition was intended, in the authentication-and-password-management and remote-working-security standards. Adopters get unambiguous prohibition wording.

**2026-06-21 | 2026.06.131 | PR #149** - Tightened the source-reference field in the compliance-obligations register template so each citation resolves to one unambiguous location, adding minimum-precision patterns for NIST, ISO, statutes, COBIT, PCI DSS, and CSA CCM. Adopters get citations precise enough to be auditable.

**2026-06-21 | 2026.06.130 | PR #148** - A validation review completed several earlier fixes: it made the Chief Risk Officer the owner of the enterprise governance-and-risk policy, added a control-testing cross-reference, and added a reciprocal risk-acceptance link to the exception policy. Adopters get consistent ownership and cross-references.

**2026-06-21 | 2026.06.129 | PR #147** - Added a 'New to GRC? Start here' section to the README that expands the governance-risk-compliance acronym, defines the three terms in plain language, and signposts role-keyed next steps. Newcomers unfamiliar with the discipline get an orientation.

**2026-06-21 | 2026.06.128 | PR #146** - Added a field to the risk-acceptance procedure linking each acceptance to its related exception-register entry (or 'None'). Adopters can cross-traverse the risk-acceptance and exception registers for audit traceability.

**2026-06-21 | 2026.06.127 | PR #145** - Added a required compensating-controls field to the acceptance section of the enterprise-risk-register template. Adopters get a self-contained, auditable acceptance record showing how each un-treated risk is offset.

**2026-06-21 | 2026.06.126 | PR #144** - Added a mandatory sampling-justification field to the audit-evidence-package template (population, sample size, method, and confidence assumption). Adopters give external auditors the statistical basis for each sample without reconstruction.

**2026-06-21 | 2026.06.125 | PR #143** - Made the Chief Risk Officer the owner of the enterprise-risk-management standard, added a Chief-Risk-Officer governance row, and rescoped the Chief-Information-Officer row to technology-risk support. Adopters get correct executive ownership of the risk standard.

**2026-06-21 | 2026.06.124 | PR #142** - Closed four quick-win findings: disambiguated an acronym in the risk standard's framework-alignment table, added a document-type-prefix mapping table to the master specification, and added a Chief Compliance Officer row to the continuous-assurance framework. Adopters get clearer references and role coverage.

**2026-06-21 | 2026.06.123 | PR #141** - Internal triage of a review's findings into the backlog; no published document changed.

**2026-06-21 | 2026.06.122 | PR #140** - Internal verification pass over a review's findings; no published document changed.

**2026-06-21 | 2026.06.121 | PR #139** - Internal change to a review procedure adding a verify-before-acting labelling step.

**2026-06-21 | 2026.06.120 | PR #138** - Internal rotation of completed backlog items into the closed-work ledger.

**2026-06-21 | 2026.06.119 | PR #137** - Internal addition of an audit check that enforces the AI-assistant's overnight-work file lifecycle.

**2026-06-21 | 2026.06.118 | PR #135** - Internal restructuring of the maintainer's working-state files; no published document changed.

**2026-06-21 | 2026.06.117 | PR #134** - Internal fix to a backlog-staleness audit check to eliminate a false positive.

**2026-06-21 | 2026.06.116 | PR #133** - Internal documentation of the project's Canadian-English-first language convention, with no change to how the language check behaves.

**2026-06-21 | 2026.06.115 | PR #132** - Added a contributor to the acknowledgements list and made a one-time correction to the maintainer's closed-work ledger.

**2026-06-21 | 2026.06.114 | PR #131** - Internal creation of the maintainer's closed-work ledger and rotation of historical completed-work notes out of the backlog file.

**2026-06-21 | 2026.06.113 | PR #130** - Internal cleanup removing decorative audit-check-count phrases from document and tooling prose.

**2026-06-21 | 2026.06.112 | PR #129** - Internal backlog-currency fix correcting stale queue framing after the prior change merged.

**2026-06-21 | 2026.06.111 | PR #128** - Internal addition of an audit check that flags a stale backlog file, plus a wrapper script bundling the pre-push checks.

**2026-06-21 | 2026.06.110 | PR #127** - Internal validation close-out fixing count mismatches and wording in maintainer notes and specifications.

**2026-06-21 | 2026.06.109 | PR #125** - Internal restructuring of the changelog into a public summary file plus a maintainer-grade detailed mirror.

**2026-06-21 | 2026.06.108 | PR #124** - Internal first run of the whole-corpus fitness review, recording its findings for triage.

**2026-06-21 | 2026.06.107 | PR #123** - Internal validation close-out actioning a single minor finding.

**2026-06-21 | 2026.06.106 | PR #121** - Internal validation close-out actioning seven findings from a recent change sequence.

**2026-06-21 | 2026.06.105 | PR #120** - Internal addition of a whole-corpus fitness-review capability run by ten persona reviewers.

**2026-06-21 | 2026.06.104 | PR #118** - Internal reorganization of the maintainer's validation-review record layout.

**2026-06-21 | 2026.06.103 | PR #117** - Internal validation close-out fixing minor prose drift in maintainer files.

**2026-06-21 | 2026.06.102 | PR #116** - Internal relocation of the validation-review history into the maintainer working space.

**2026-06-21 | 2026.06.101 | PR #115** - Internal rename of a review command and addition of a per-run record convention.

**2026-06-21 | 2026.06.100 | PR #114** - Internal creation of the maintainer working-state directory convention.

**2026-06-21 | 2026.06.99 | PR #113** - Internal validation close-out actioning three documentation findings.

**2026-06-21 | 2026.06.98 | PR #112** - Internal validation close-out that also added a governance rule on validating assumptions before acting.

**2026-06-20 | 2026.06.97 | PR #111** - Internal validation close-out with a safeguard against skipping review steps.

**2026-06-20 | 2026.06.96 | PR #110** - Internal fix of two stale audit-check-count references and a broadened check to catch them.

**2026-06-20 | 2026.06.95 | PR #109** - A new audit-evidence-package template was added for adopters. It completed a planned set of adopter template additions.

**2026-06-20 | 2026.06.94 | PR #108** - Renamed the adopter quickstart template file to a clearer name, with no change to its content.

**2026-06-20 | 2026.06.93 | PR #107** - New regulator-interaction templates were added for adopters. They are part of a planned set of adopter template additions.

**2026-06-20 | 2026.06.92 | PR #106** - A new implementation-roadmap template was added for adopters. It is part of a planned set of adopter template additions.

**2026-06-20 | 2026.06.91 | PR #105** - The adopter quickstart template was heavily rewritten, replacing six fixed organization profiles with a more flexible activity-based structure. This better fits adopters whose circumstances do not match a preset category.

**2026-06-20 | 2026.06.90 | PR #104** - A new adopter maturity self-assessment template was added. It is part of a planned set of adopter template additions.

**2026-06-20 | 2026.06.89 | PR #103** - A new adopter quickstart template, organized by adopter profile, was added. It is the first of a planned set of adopter template additions.

**2026-06-20 | 2026.06.88 | PR #102** - Internal bookkeeping reconciling a coverage-gaps register with the backlog.

**2026-06-20 | 2026.06.87 | PR #101** - Internal refresh of a backlog decision note about a cross-document number-consistency check.

**2026-06-20 | 2026.06.86 | PR #100** - Internal addition of an audit check verifying that paired review skills stay step-for-step consistent.

**2026-06-20 | 2026.06.85 | PR #99** - Internal addition of an audit check that ages deferred follow-up items.

**2026-06-20 | 2026.06.84 | PR #98** - Internal extension of a pre-check to catch stale version numbers written inline.

**2026-06-20 | 2026.06.83 | PR #97** - Internal change so that review runs finding nothing no longer create standalone records.

**2026-06-20 | 2026.06.82 | PR #96** - Internal enhancement adding a no-backsliding baseline discipline to the corpus review.

**2026-06-20 | 2026.06.80 | PR #94** - Internal enhancement adding a structured finding-output format to the corpus review.

**2026-06-20 | 2026.06.79 | PR #93** - Internal enhancement adding a reviewer-disagreement resolution step to the corpus review.

**2026-06-20 | 2026.06.77 | PR #91** - Internal enhancement replacing the corpus review's fixed iteration cap with principled stop conditions.

**2026-06-20 | 2026.06.76 | PR #90** - Internal enhancement adding a dating convention for deferred review findings.

**2026-06-20 | 2026.06.74 | PR #88** - Internal enhancement adding a justification step before review sub-tasks make tool calls.

**2026-06-20 | 2026.06.72 | PR #86** - Internal noise-reduction change so the pre-check stops re-flagging the same known false positives.

**2026-06-20 | 2026.06.71 | PR #85** - Internal convention letting a review finding carry a primary and a secondary cause label.

**2026-06-20 | 2026.06.69 | PR #83** - A stale version reference in the adopter guide was reworded so it no longer names a specific pack version that had already moved on. This keeps the adopter guide accurate as versions change.

**2026-06-20 | 2026.06.68 | PR #82** - Internal enhancement adding a reproducible rule for combining review findings.

**2026-06-20 | 2026.06.66 | PR #80** - Internal review close-out fixing a cross-surface step-numbering inconsistency and updating the review discipline.

**2026-06-20 | 2026.06.65 | PR #79** - Internal enhancement adding a nightly scheduled run of the mechanical corpus review.

**2026-06-20 | 2026.06.64 | PR #78** - Internal enhancement adding a deterministic pre-check to the corpus review.

**2026-06-20 | 2026.06.63 | PR #77** - Internal addition of two discipline enhancements to the corpus review process.

**2026-06-20 | 2026.06.62 | PR #76** - Internal review close-out fixing three findings in the review-skill files.

**2026-06-20 | 2026.06.61 | PR #75** - Internal addition of three new AI-assistant skills to the developer rule pack, recreated as in-house content.

**2026-06-20 | 2026.06.60 | PR #74** - Internal wiring making the corpus-review skill discoverable via a command.

**2026-06-20 | 2026.06.59 | PR #73** - Internal change making a detector for new candidate collections run automatically on pack changes.

**2026-06-20 | 2026.06.58 | PR #72** - Internal addition of a tool that surfaces new candidate collections for the maintainer to review.

**2026-06-20 | 2026.06.57 | PR #71** - Internal addition of an audit check validating the licence on every file, including the third-party overlay.

**2026-06-20 | 2026.06.56 | PR #70** - Internal formatting cleanup of a historical changelog entry.

**2026-06-20 | 2026.06.55 | PR #69** - Internal addition of an audit check that keeps enumerated collections in sync with their source.

**2026-06-20 | 2026.06.54 | PR #68** - Internal tooling and discipline improvements informed by recent automated-check failures.

**2026-06-20 | 2026.06.53 | PR #67** - Internal addition of an audit check that flags a document whose body changed without a version bump.

**2026-06-20 | 2026.06.52 | PR #66** - Internal review close-out fixing three minor findings and updating the review skill's window.

**2026-06-20 | 2026.06.51 | PR #65** - Internal addition of a per-change check that a modified document also bumps its version.

**2026-06-20 | 2026.06.50 | PR #64** - Internal addition of an audit check that keeps audit-check-count references consistent across documents.

**2026-06-20 | 2026.06.49 | PR #63** - Internal cleanup from the first corpus-review run, fixing stale references a prior pass missed.

**2026-06-20 | 2026.06.48 | PR #62** - Internal addition of a corpus-wide regression-review skill to the developer rule pack.

**2026-06-20 | 2026.06.47 | PR #61** - Internal cleanup correcting a mis-attributed rule reference and several stale audit-check-count mentions.

**2026-06-20 | 2026.06.46 | PR #60** - Internal addition of a worked example to a governance rule about updating every parallel surface.

**2026-06-20 | 2026.06.45 | PR #59** - Internal addition of an audit check enforcing where orientation and licence sections sit in a document.

**2026-06-19 | 2026.06.44 | PR #58** - Internal README tidy-up moving the licence section to the bottom and correcting a list of external rule sources.

**2026-06-19 | 2026.06.43 | PR #57** - Internal restructuring of the developer rule pack's readme for readability.

**2026-06-19 | 2026.06.42 | PR #56** - Internal README tidy-up of the pack-adoption paragraph.

**2026-06-19 | 2026.06.41 | PR #55** - Internal update naming the developer rule pack in the project's attribution and citation metadata.

**2026-06-19 | 2026.06.40 | PR #54** - Internal reframing of the project's stated positioning as both a governance corpus and a reference implementation.

**2026-06-19 | 2026.06.39 | PR #53** - Internal wrapping of two governance rules as AI-assistant skills.

**2026-06-19 | 2026.06.38 | PR #52** - Internal addition of a governance rule on attempting an action before explaining why it cannot proceed.

**2026-06-19 | 2026.06.37 | PR #50** - Internal change bringing the docs directory under the same metadata audit as the rest of the corpus.

**2026-06-19 | 2026.06.36 | PR #49** - The AI agent production-authority controls were completed by linking a harmful or unauthorized agent action to its reversal in incident response. The agentic-development standard was also recorded in the cross-framework alignment matrix.

**2026-06-19 | 2026.06.35 | PR #48** - The AI agent production-authority controls were wired into the service-acceptance decision, the AI-governance framework, and a named accountable role. This ensures an autonomous agent gains production authority only through a governed approval path.

**2026-06-19 | 2026.06.34 | PR #47** - A new set of controls was added requiring that autonomous agents receive production authority only after reversibility, auditability, accountability, and permission boundaries are designed, tested, and governed. This closed a gap where the corpus had treated reversibility only as an input to an approval decision rather than a tested precondition.

**2026-06-19 | 2026.06.33 | PR #46** - Internal consistency fix broadening how a governance rule is described across its summary surfaces.

**2026-06-19 | 2026.06.32 | PR #45** - Internal extension of a governance rule to cover any claim about a document's state, not only completion claims.

**2026-06-19 | 2026.06.31 | PR #44** - Internal addition of an audit check that detects drift between the pack rules and their local copies.

**2026-06-19 | 2026.06.30 | PR #43** - Internal security fix hardening the secret-scanning check so it catches additional private-key formats.

**2026-06-19 | 2026.06.29 | PR #42** - Internal fix correcting stale audit-check-count references in the AI-assistant instruction file.

**2026-06-19 | 2026.06.28 | PR #41** - Internal re-sync of a local governance-rule copy with its pack source.

**2026-06-19 | 2026.06.27 | PR #40** - Internal fix correcting a stale audit-check number in a tool's code comment.

**2026-06-19 | 2026.06.26 | PR #39** - Internal fix correcting stale audit-check and version references in the backlog file.

**2026-06-19 | 2026.06.25 | PR #38** - Internal extension of a governance rule with guidance on polling failures and invented URLs.

**2026-06-19 | 2026.06.24** - Internal addition of an audit check that flags a document whose date lags behind its latest change.

**2026-06-19 | 2026.06.23** - Internal correction of date and version metadata on five governance files edited earlier.

**2026-06-19 | 2026.06.22** - Internal move of a speculative plan out of the changelog and into the backlog.

**2026-06-19 | 2026.06.21** - Internal addition of an audit check that every skill cites the governance rule it derives from.

**2026-06-19 | 2026.06.20** - Internal introduction of AI-assistant skills as a new content type in the developer rule pack, with three initial skills.

**2026-06-19 | 2026.06.19** - A new threat-modelling standard was created, adapting a per-trust-boundary threat analysis and a three-tier response model from a third-party security source. Two existing documents gained cross-references to it.

**2026-06-19 | 2026.06.18** - Internal addition of a fourth third-party rule source, vetting and importing five of its skills.

**2026-06-03 | 2026.06.17** - Internal update of the branch-protection register to match the live configuration.

**2026-06-02 | 2026.06.16** - Internal change bringing five repository-root files under the metadata audit.

**2026-06-02 | 2026.06.15** - Internal documentation of the branch-protection configuration as an auditable register.

**2026-06-02 | 2026.06.14** - Internal promotion of a metadata line-break scanner into a full audit check.

**2026-06-02 | 2026.06.13** - Internal fix so the version-monotonicity check ignores version lines inside code blocks.

**2026-06-02 | 2026.06.12** - Internal metadata-rendering fix to three more files, completing the cleanup.

**2026-06-02 | 2026.06.11** - Internal metadata-rendering fix to the contributing guide.

**2026-06-02 | 2026.06.10** - Internal fix of a metadata-block rendering bug in two files.

**2026-06-02 | 2026.06.9** - Internal addition of a Capacitor and Ionic secure-coding rule file, completing the mobile security work.

**2026-06-02 | 2026.06.8** - Internal addition of a .NET MAUI secure-coding rule file to the developer rule pack.

**2026-06-02 | 2026.06.7** - Internal addition of a Flutter secure-coding rule file to the developer rule pack.

**2026-06-02 | 2026.06.6** - Internal addition of a React Native secure-coding rule file to the developer rule pack.

**2026-06-02 | 2026.06.5** - Internal addition of an Android secure-coding rule file to the developer rule pack.

**2026-06-02 | 2026.06.4** - Internal addition of the first per-framework mobile secure-coding rule file to the developer rule pack.

**2026-06-02 | 2026.06.3** - The mobile application security standard gained three additions closing currency gaps for 2024 to 2026. This updates the mobile security guidance adopters follow.

**2026-06-02 | 2026.06.2** - Internal project-wide version bump signaling the documents are ratified beyond first-draft status.

**2026-06-01 | 2026.06.1** - Internal documentation of the project's no-exception stance and a force-push preservation convention.

**2026-06-01 | 2026.06.0** - Internal addition of a version-date consistency check and a calendar-version rollover.

**2026-06-01 | 2026.05.144** - Internal completion of the developer rule pack's governance-rule rollout with its fifth and last rule.

**2026-06-01 | 2026.05.143** - Internal addition of the fourth governance rule to the developer rule pack.

**2026-06-01 | 2026.05.142** - Internal addition of the third governance rule to the developer rule pack.

**2026-06-01 | 2026.05.141** - Internal addition of the second governance rule to the developer rule pack.

**2026-06-01 | 2026.05.140** - Internal addition of the first governance rule to the developer rule pack.

**2026-06-01 | 2026.05.139** - Internal announcement broadening the developer rule pack from security-only to security plus development governance.

**2026-06-01 | 2026.05.138** - Internal addition of a changelog-enforcement check and a catch-up entry.

**2026-05-31 | 2026.05.137** - Internal corpus-wide hyperlink sweep and backlog cleanup.

**2026-05-31 | 2026.05.136** - The first public release of the Governance, Risk, and Compliance Documentation Library. It was published under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) licence.

