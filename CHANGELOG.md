# Changelog

All notable changes to this repository are recorded in this file as one compact entry per change: a `date | version | PR` header followed by a short, plain-language summary a general reader can follow. The full maintainer-grade detail for each change (the Added / Changed / Removed / Fixed / Security / Verification sections) is kept in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) and in git history; that mirror is how this project's maintainer tracks the full audit trail. The convention is project-specific; forks may delete `.working/` and adopt their own approach to detailed change tracking. The mechanics are documented in the [`change-tracking` governance rule](dev-security/claude-rules/governance/change-tracking.md).
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

**2026-07-13 | 2026.07.382 | PR #894** - Ran the round-3 deep assessment's fresh-reader review (the fitness pass): ten reviewers each read the whole library from a different reader's point of view (an executive, a security lead, an auditor, a privacy officer, a newcomer, and so on), with the maintainer's own assumptions deliberately stripped out. They surfaced 20 genuine issues that the mechanical checks cannot see, almost all of one kind: the same rule stated with a different number or scope in two or more documents. The two most important: the internal-audit standard describes the audit function's independence as reporting only to an executive committee, with no line to the board or audit committee (which other documents assume exists); and three documents set different remediation deadlines for the same severity of software-dependency vulnerability (30 vs 14 days for High). Others include a leftover permission for the older TLS 1.2 encryption in one procedure that two stronger documents forbid, certificate key-size and password rules that differ between an operational document and the governing standard, a data-subject-request procedure that omits the tighter Brazil and Mexico response deadlines its own country annexes document, and a board/CEO reader group the navigation portal serves but the README does not advertise. All 20 were verified against the live text and recorded for the maintainer to decide on; none was changed in this pass (the "which number is right" calls are the maintainer's). Also recorded the prior PR's post-merge quality checks and corrected a small internal status-tracking slip that pass flagged. Process and review only; no adopter-facing content changed yet.

**2026-07-13 | 2026.07.381 | PR #893** - Ran the round-3 deep assessment's forensic quality pass (six independent reviewers over this session's work and the quality machinery). Five came back clean: stale references, audit-programme parity and counts, citation accuracy against the held sources, generated-artefact sync, and the QA-discipline record all sound. The sixth caught one genuine citation-precision defect from an earlier change this session: the citation-register entry for an EU consent guideline gave its Version 1.1 date as 4 May 2020 in one cell while its own note and the held source's version history date Version 1.1 to 13 May 2020 (4 May was the original Version 1.0). Corrected the register entry and the one document that cites it to state both dates precisely. Also recorded the prior PR's post-merge quality checks. Process, plus one small citation-date correction; nothing else adopter-facing changed.

**2026-07-13 | 2026.07.380 | PR #892** - Continued round 3 of the deep assessment with two more of its semantic checks. The publications-screening check found nothing to do (every reference-base publication is already screened; none pending). The whole-matrix control-fit check judged all 84 matrix and per-document rows that lack an obvious keyword overlap between the document and its cited control, against the actual control titles: every one is a correct or defensibly-supporting mapping, zero wrong-control findings, so the library's control-code mappings remain sound. Also recorded the prior PR's post-merge quality checks. Process/housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.379 | PR #891** - Continued round 3 of the deep assessment with the citation-precision check (claim-fit) over this session's newly-added citations. The one specific-value claim it flagged, Canada's 24-month breach-record retention duty cited to the Breach of Security Safeguards Regulations, was confirmed accurate word-for-word against the held regulation; the earlier-noted question about the AICPA criteria (the reference copy on file is an older edition than the version cited) was recorded as a known, already-tracked source-acquisition item, with no library value resting on the unheld text. Also completed the documentation fix begun in the prior PR by correcting two further internal descriptions (a gate docstring and a changelog-check docstring) that still described the old changelog-entry style, found via a full sweep for that stale wording, and recorded the prior PR's post-merge quality checks. Process/housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.378 | PR #890** - Ran the structural-integrity review of the governance machinery (the guardrail review) as part of round 3 of the deep assessment. The rules, skills, and audit gates came back cleanly non-overlapping (every apparent overlap is deliberate, documented layered defence). The review did surface that a recent changelog-format change had left three internal descriptions (two tool docstrings and one passage of the audit-programme specification) still describing the old entry-header style even though the code already handles both styles; those were corrected here so a future maintainer cannot mistakenly narrow the check and reintroduce a bug the gate exists to catch. Other structural suggestions (a safeguard against accidentally editing on the main branch, a small ordering check for one internal register, and two housekeeping dispositions) were recorded for maintainer decision. Also recorded the prior PR's post-merge quality checks. Process/housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.377 | PR #889** - Advanced the round-3 deep assessment's checks on the audit programme itself (Phase 4). The gate blind-spot map came back clean (no non-exempt document falls outside every gate that could scan it), and a mutation probe run on a throwaway copy of the repository confirmed the gates still catch what they are meant to: 15 deliberately planted defects were all detected by the right gate and 5 clean controls all passed, with no false alarms, so gate detection width is intact. Also recorded the prior PR's post-merge quality checks and corrected a cosmetic ordering slip in the assessment's own register table. Process/housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.376 | PR #888** - Opened round 3 of the whole-project deep assessment (the maintainer-invoked, periodic top-to-bottom review of the library's own quality system, which terminates only on the maintainer's sign-off). Re-derived the live inventory of quality machinery directly from the repository (69 audit gates, 23 skills, 13 governance rules, 14 commands, 9 advisory tools), confirmed the mechanical baseline is green across the library and both companion repositories, and recorded that this session's clean corpus-wide validation sweep serves as the assessment's validation-of-record. The heavier semantic checks (citation-fit sampling, reference-breadth, adopter-readiness, and gate-effectiveness probing) run next; the run is recorded so it can resume across sessions. Also folded in the prior PR's post-merge quality-check results. Process/housekeeping only; nothing adopter-facing changed.

**2026-07-13 | 2026.07.375 | PR #887** - First PR of the resumed session: ran the corpus-wide validation sweep (Sweep 101) over the previous session's changes (#852 through #886) and it came back clean, no errors or warnings, confirming the library stayed internally consistent across that window. Routed one low-risk note to the backlog (the reference copy held for the AICPA Trust Services Criteria is an earlier edition than the version the citation register names, though the citation itself is accurate and was confirmed against the publisher this session), recorded the sweep, pruned the resume record to its current-plus-one-prior window, and re-acquired the session working-lease. Housekeeping only; nothing adopter-facing changed.

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

