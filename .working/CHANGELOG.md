# Changelog

This file records the GRC Library's changes as weekly summaries, one section per ISO week that had changes, newest first. Until a week is rolled up, each pull request merged in it also has its own line above that week's summary. The library as a whole is versioned by Calendar Versioning (CalVer).

**2026-11-18 | 2026.11.97 | PR #33** - tools: Tool messages, labels, tests, help text and comments drop internal work identifiers, each replaced by a phrase naming what it guards. The todo-number permanence gate reads private backlog exemptions from the private sibling, and its exemption rows are checked against their documented form. Gate 62 refuses a local-section exception path whose parenthesized link is never closed, skipping parentheses in code spans or escaped, with a stated residual for a code span that also encloses the link. The compiler refuses a symlinked core at its own pre-check.
**2026-11-14 | 2026.11.96 | PR #32** - review fixes for PR #31. Supply-chain: the programme matrix's PIP Risk Assessment mark, which PR #31 raised from partial to required, now cites the Partners in Protection (PIP) security requirements (a written risk assessment reviewed at least once per year). Governance: the 17 retired-gate tombstone rows drop their basis clauses, keeping date, reason and earlier name. Tools and tests: the attribution check's comment names its seven text views, the IT-6 test docstring and guard describe the row as it was, and internal work references leave comments and a fixture.
**2026-11-14 | 2026.11.95 | PR #31** - train: five changes land together. Supply-chain: AEO and C-TPAT documents give HMRC handbook sections 8.9 to 8.12 their should-framing, C-TPAT IT and PIP registers mark controls Not assessed, and healthcare, FedRAMP and third-party risk documents correct mappings and wording. Governance: the coverage gap and BASC KPI registers are corrected, the document index rewords its expansion backlog note, the glossary adds ETSI, and the citation file updates its document count. AI: 11 AI Act citations note the Digital Omnibus amendments (Regulation (EU) 2026/1744). Tools: the pull request attribution check is ported. Governance: 17 retired gates record earlier names and basis.
**2026-11-13 | 2026.11.94 | PR #30** - tools: Gate 107 no longer reads external standard section numbers copied into the generated taxonomy and narrative data as stale backlog references. In those two files it sets aside only the bare section form and still reports every TODO-, P-TODO- and backlog-qualified form. It also treats GFM as a document-section cue, and the audit programme specification states the rule and its residue.
**2026-11-12 | 2026.11.93 | PR #29** - tests: Comments, docstrings, self-test labels, fixture names and messages in the linter tests, nine tools, a hook and the site generator drop internal work references and review labels, with no change in behaviour. Two notes in the corpus-management pack's id history do the same, and the pack moves to 0.23.6.
**2026-11-12 | 2026.11.92 | PR #28** - governance: Registers, the citation verification specification, the ETSI baseline matrix and the audit programme specification drop history wording and name the heading of each section they cite. The audit programme specification and the cross-file gates' documentation say that gate 62 checks every table cell, and state what gate 65 adds; the corpus-management pack moves to 0.23.5.
**2026-11-12 | 2026.11.91 | PR #27** - tests: Two tests check that the CHANGELOG mirror header-parity audit (gate 59) reads this repository's detailed changelog mirror in the shared operational store, never the predecessor repository's legacy mirror there. One checks the path the gate resolves; the other gives the gate a store holding only the legacy mirror, which it does not read. The gate's store lookup now takes its path from its one mirror-path constant.
**2026-11-12 | 2026.11.90 | PR #26** - tests: The pre-push guard's gate 36 summary line for shard checkouts it could not remove no longer says "(named above)", and the six tests that read the line check its full ending. Comments and docstrings in the pre-push guard fast-path tests now describe the subreaper launcher's exit status, the other processes the class starts, and when the non-dumpable process is part of the report's inventory.
**2026-11-12 | 2026.11.89 | PR #25** - governance: Executive narrative pages drop the Review Record field, and the narrative tools, engines and web template follow, so every narrative page and gate now uses the 7-field extension the specification describes. The generated narrative registry moves to schema version 2 without the field, and the corpus-management pack moves to 0.23.4.
**2026-11-12 | 2026.11.88 | PR #24** - governance: The executive narrative specification and its subtype template describe a 7-field narrative extension without the Review Record field, and no longer point at review evidence held outside the library. The audit programme specification counts 7 narrative extension fields. The narrative pages and tools still carry the field until the next pull request moves them.
**2026-11-12 | 2026.11.87 | PR #23** - tests: The secrets and PII gates refuse by name, with exit 2, a listed file that is gone when they read it, as six other gates already do, so a test fixture deleted mid-walk no longer stops them with a traceback. The test suite README names the eight gates that refuse such a file and the twelve that can still stop on one.
**2026-11-12 | 2026.11.86 | PR #22** - tests: The linter tests drop an unused helper for driving the merge-when-green tool, and the captured error text it used; no test called it.
**2026-11-12 | 2026.11.85 | PR #21** - tests: Test case labels and assertion messages in the linter tests and web draft tests drop review-round and reviewer-family prefixes, review notes and decision references, and the pack-version assertion message opens by describing 0.23.3, the version it asserts.
**2026-11-12 | 2026.11.84 | PR #20** - tools: A new test checks that when a listed path cannot be resolved, the shared listing helper does not count the missing file as vanished and the read error still surfaces. The web build's comment names the two library root specifications, governance/specification-master-project.md and governance/specification-ingestion.md.
**2026-11-12 | 2026.11.83 | PR #19** - tools: The listing-surface suggester reports the corpus generators for a root-level path the taxonomy builder already lists, and for any other path without a domain it says to add it to the root-specification list and that the library specifications sit in governance/. Comments and docstrings in four gates and the web build name those specifications by that home instead of the repository root, and the pack moves to 0.23.3.
**2026-11-12 | 2026.11.82 | PR #18** - tools: The stub-document and orphan-document gates no longer walk the test suite's tests/tmp scratch tree, so a fixture left there by an interrupted test run is never reported. A file either gate lists and then finds gone when it reads it is refused by name with exit 2, never a traceback or a silent pass.
**2026-11-12 | 2026.11.81 | PR #17** - governance: The audit programme specification names the individually listed corpus documents (README, NOTICE, the master-project, ingestion and executive-narrative governance specifications, and the AI document-ingestion instruction) where it described root-level corpus documents, and the AI security tooling register says TikiTribe is referenced most often in the AI security technical implementation guide and the AI adversarial test reference guide.
**2026-11-12 | 2026.11.80 | PR #16** - governance: Documents and tooling text that still placed the library specifications and the changelog at the repository root now name their homes in governance/ and .working/CHANGELOG.md. The document register rule no longer exempts the specifications, the review cadence and review schedule list the files that sit at the root, the portal and README describe the third adoption mode as the pinned AIQT runtime only, and an overstated citation claim is corrected.
**2026-11-11 | 2026.11.79 | PR #15** - tools: Comments and docstrings in the corpus-management tools, pack sources and git hooks drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Code is unchanged; the test file's pins and pack-version assertion follow the edited files, and the pack moves to 0.23.2.
**2026-11-11 | 2026.11.78 | PR #14** - tests: Comments and docstrings in the linter tests and web draft tests take the low-severity wording fixes left by the earlier test batches: unscoped past observations, rewraps and leftover labels. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.77 | PR #13** - tests: Comments and docstrings in the web draft tests drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.76 | PR #12** - tests: Comments and docstrings in the linter tests from the taxonomy framework tests to the corpus-management scan-scope tests drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.75 | PR #11** - tests: Comments and docstrings in the last part of the linter tests, from the pack-activation tests to the end of the file, drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.74 | PR #10** - tests: Comments and docstrings in the linter tests from the dash-scope tests to the taxonomy walk-scope tests drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.73 | PR #9** - tests: Comments and docstrings in the linter tests from the alignment-register tests to the pre-push guard tests drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.72 | PR #8** - tests: Comments and docstrings in the regression-gate, standards-currency and release-delta test files, and in the first 8,422 lines of the linter tests, drop internal work IDs, decision records and review history, and restate past incidents as the earlier repository's history. Test code, string literals and text that tests read from source are unchanged.
**2026-11-11 | 2026.11.71 | PR #7** - tools: run-shell-stubbed.py now reads each process's /proc stat file without strict UTF-8 decoding, so a process whose name holds a non-UTF-8 byte no longer crashes the tool's self-test or the regression gate. Two other stat reads in the tool get the same fix; one of them had silently returned no result. New tests cover all three reads with a fake /proc tree whose process names hold non-UTF-8 bytes.
**2026-11-10 | 2026.11.70 | PR #6** - docs: The corpus-management sources, specifications, procedures, tests README, Clean Language provenance note and relationship-model source drop internal references and review history. Specifications and procedures restate past incidents as earlier-repository history. The core rules and pack READMEs state that gate 99 owns only SKILL.md and rule-index.md in the skill directory. The tools README and audit programme document the stray-scan shipped-entry skip. The licence draft's carve-outs name the Apache-2.0 AIQT rule snapshot and release manifest, not MIT overlays or skills. The ingestion specification and adopter guide describe per-pull-request changelog entries and weekly summaries. The pack README gains release history and reference sections.
**2026-11-10 | 2026.11.69 | PR #5** - docs: Removes or replaces internal decision records, IDs, private names, AI conventions and review history in public files. In the AI security tooling landscape register, LocalMod becomes Surveyed only, PISmith Referenced as exemplar, seven observability and pentest-agent entries move to Cited and Strix gains Cited, closing backlog item 4.32. Other entries name the covering register, standard or control (CodeGate only in part). The master specification corrects its gate 59 and changelog-format descriptions, and the backlog its gate 90 description. The notice and two specifications name the transition clause's OSFI quotations. The PR #1 line and six weekly summary lines change.
**2026-11-10 | 2026.11.68 | PR #4** - docs: The authors page and the README credit now name the maintainer as Jeff Posluns; the citation file and the BibTeX entry keep the formal given name. The authors page also notes that more than 50 contributors, reviewers, and editors have worked on the library. The authors and notice pages drop sentences that cited internal decisions; they and the README licence paragraph state the AI-assistant rules licence in plain terms and name the folder that holds its LICENSE and NOTICE files.
**2026-11-10 | 2026.11.67 | PR #3** - tests: The pre-push guard tests no longer depend on the developer's environment, host load or the clock. Every Python process they start runs isolated, with a built environment and a lifetime the test controls; waits use the guard's own clock or generous bounds; the shard tests reap every process they start; and the leftover-scan tests read only their own fixture. A run as root skips only the checks that need an unprivileged user.

**2026-11-09 | 2026.11.66 | PR #1** - tools: Gate 59 checks that this changelog and its detailed private copy list the same pull requests, and now works in the new repository, where pull request numbers restart at #1. Root summary lines accept only plain letters, digits and simple punctuation, so no markup can hide an old record. GitHub now runs 1 small pull-request check, the full suite runs on the local server and reports a local-quality status that merging requires, and the nightly sweep stays.

## Week of 2026-11-09

- The library now lives in a new repository whose history starts fresh: the rebuilt library is published as a single commit.
- The audit tools, project specifications and registers, adopter guides, generated data and tests now live together under .claude/skills/corpus-management/ as the corpus-management skill, at pack version 0.23.0. The 12 governance domains are unchanged.
- The AIQT rule set (https://aiqt.ai) is pinned as the governance baseline, replacing the earlier guardrails pack, and version 1.0.15 of the Clean Language writing skill is bundled.
- The audit programme runs 95 gates. Its 16 retired gate numbers (32, 42, 43, 44, 46, 50, 51, 60, 63, 74, 76, 80, 83, 95, 103 and 105) stay listed as tombstones and are never reused. Their tombstones give the reasons: 8 gates read maintainer files kept outside the public repository, 6 checked skill or rule files that left the public repository, and gates 95 and 105 were retired as numbered. The hook checks of gates 95 and 105 continue, re-scoped, in gate 111.
- Tooling: the reference manifest schema is at version 1.0.1, the document date check now reaches the specifications and adopter guides in their new place, and the review-cadence and standards-currency checks reach the specifications there; the adopter guides stay outside those 2 checks, as before.

## Week of 2026-11-02

- The rebuilt grclibrary.ai became the live site. The week built it from a draft up: landing, browse, search, document, decision and crosswalk pages, a dark mode, a Standards and frameworks page, site-wide fixes, and a build guard that refuses unrecorded links to the library's source repository.
- Customs and trade-security accuracy: WCO SAFE claims were swept against the held 2025 text, the Supply Chain Security Programme Alignment Matrix's WCO SAFE column now follows Annex IV of the Framework with a stated rule for required and partial marks, and BASC, PIP, NEEC and UK AEO Security and Safety claims follow the held texts.
- UK AEO-S and HMRC statements in twelve documents were corrected against the newly ingested HMRC Customs Technical Handbook (AEO), and the US CTPAT Minimum Security Criteria register now says plainly that the library holds no complete CBP criteria text, with every control Not assessed until an adopter records evidence.
- Quebec Law 25 is now cited as the Act respecting the protection of personal information in the private sector (CQLR c. P-39.1), as amended by S.Q. 2021, c. 25, and the citation-verification specification calls it a statute, not a regulation.
- Tooling and audit gates: the reference-acquisition manifest was regenerated after the HMRC handbook ingest, the internal checks now report what they cannot evaluate instead of passing silently, the pre-push check reports leftovers and failures in plain messages, and new tests guard the WCO SAFE matrix key and the UK programme name spellings.

## Week of 2026-10-26

- Accuracy corrections against held sources: China's Cybersecurity Law stated under its amended numbering, HIPAA breach-notification deadlines stated as the regulation sets them including the law-enforcement delay, GDPR territorial scope stated with all three routes, SOC 2 report types stated as the AICPA guide defines them, and Brazil's LGPD corrected across five privacy and AI documents including its parental consent rule.
- The EU AI Act's serious-incident reporting routes are stated in full, including the narrower scope for AI in medical devices and the deployer's fallback when the provider cannot be reached, and three documents now cite only the parts of the EU Digital Operational Resilience Act their text records, with ICT contract terms separated by criticality tier.
- New coverage: an Ecuador privacy annex on the country's 2021 data protection law and its implementing regulation, and a Canadian federal security and cyber baseline, with many security documents mapped to held Government of Canada sources across governance, logging, incident response, patching, cloud, networking and secure development.
- Citation currency: citations of eight frameworks now name the versions the library uses, six ISO 19011 citations name its 2026 edition, the audit evidence package template supports a SOC 2 Type I report as well as Type II, and eight requirement sentences now say must instead of should or may not.
- One rule now governs short, attributed quotation of government, regulatory and openly licensed texts, and the library's relationship model gained GDPR, NIS 2, NIST Secure Software Development Framework and LGPD links to the documents that implement them.
- Audit tooling: a new gate checks that every Markdown table row has as many cells as its header, the library's tools run under Python's isolated mode so a stray file cannot replace a standard module, and several checks now refuse unreadable inputs instead of skipping them.

## Week of 2026-10-19

- Statutory deadlines now read as the held laws set them: UK GDPR request clocks and extensions under Article 12A, the UK's Articles 22A to 22D on automated decisions, and the EU two-month extension for five more data subject rights; the breach response procedure adds eleven held-source requirements with citations.
- AI documents state the EU AI Act tiers, general-purpose AI systemic-risk classification and fine rules as the held regulation and its 2026 amendment do, the corpus names its two AI risk scales distinctly, and a new AI assurance case procedure and template were added, with evaluation uncertainty reported in the testing standard.
- Security floors rose: Diffie-Hellman groups of at least 3072 bits, 4096-bit RSA email signing keys, key-recovery approvals brought within role authority, and incidents involving personal data now reach the Data Protection Officer at any severity.
- Citation and reference updates: the register gained dozens of NIST publication rows and the international AI governance instruments (the UNESCO recommendation, the G7 Hiroshima code of conduct, the Council of Europe framework convention and the OECD principles), the cloud-exit standard now maps GDPR Article 28(3)(g) and the EU Data Act switching provisions, and the FDA premarket cybersecurity guidance is cited accurately.
- Tooling and audit gates: red-team and PyRIT runs are scoped by their stated trigger, four workforce-monitoring sources were registered and cited with pinpoints, and range-reading and reference checks now refuse unreadable or ambiguous inputs.

## Week of 2026-10-12

- Incident clocks and incident command were reconciled across the security, operations, risk, compliance and AI documents: one severity scale, approval required for every downgrade, the Data Protection Officer's command role in privacy breaches stated, and outage triggers tied to the ISO/IEC 27035-1 meaning of a security incident.
- Cryptographic key destruction was rewritten: destruction covers every copy of a secret or private key, honours legal holds and investigations, records a per-copy destruction record, and ephemeral key-agreement keys run under approved protocols only; media sanitization follows IEEE 2883-2022.
- Citation precision: the ISO/IEC 27035 series is cited by part, framework-alignment tables in about twenty documents gained pinpointed ISO, NIST, EDPB and BASC references, and reference titles across eight documents now match their published texts.
- Licence footers in nineteen documents lost wording that contradicted CC BY-SA 4.0.
- Website and tooling: the site's For-AI resource lists are now verified against the citation register, the site states the AIQT priority rule as written and shows current standard editions, and many checks gained fail-closed input handling.

## Week of 2026-10-05

- A short internal-tooling week of tooling hardening: the automated hooks load reviewed sources only and launch with an isolated interpreter.
- The shell-stub test runner gained a self-test with supervised liveness ceilings and named failures, and diagnostic delivery now survives restricted environments.

## Week of 2026-09-28

- Breach and privacy rules now follow the held law texts, including Indonesia's 3 x 24-hour breach deadline, the GDPR clock stated in full, and corrections for the EU, UK, Brazil, India, Canada, Singapore, Australia, South Korea, Turkey, US healthcare and New York annexes.
- NIS 2 guidance now classifies entities by Article 3, not the sector annex, and UK references name the Information Commission as the regulator from 30 September 2026.
- Evidence, records and cryptographic keys under a legal hold are protected before destruction, with hold releases in writing, and servers connecting AI tools must authenticate every network connection.
- The always-loaded instruction files shrank sharply as the pinned AIQT rules (https://aiqt.ai) replaced the legacy governance rules.
- New checks catch unnamed missing-source claims, non-Canadian spellings, stale citations and unreadable files, and thirty AI tooling and evaluation sources were re-checked upstream in the register.

## Week of 2026-09-21

- The AI jurisdiction library gained annexes on Singapore's agentic-AI framework, United States federal executive-branch AI policy, Malaysia's national AI guidelines and the UK's principles-based framework, and the decision tree now routes readers to every AI-jurisdiction annex.
- Security baselines moved to SHA-512 or BLAKE2b-512 integrity hashing and message authentication with keys of at least 256 bits, service-account passwords now rotate at least annually, every production Model Context Protocol server must be registered and security-reviewed, and a Jakarta EE application security standard was added.
- Citation currency and precision: ISO/IEC 27001, 27002, 42001 and other ISO families were pinned to their current editions, SLSA and NIST SP 800-53 references name their versions, and sentences that overstated what ISO/IEC 42001, ISO 31000 and ISO/IEC 23894 require were corrected.
- Privacy and regulatory pages sharpened: MiCA, DORA, NIS 2 and eIDAS qualifications, Kenya and Peru annex precision, the Japan annex follows the official APPI translation, and the Canada public-sector annex gained federal and British Columbia access and privacy baselines.
- The relationship model grew with batches of verified control-framework mappings, and change-classification and BYOD rules were made consistent across their carrying documents.
- Tooling: a new gate keeps account names and private identifiers out of public files, merge checks were tightened, and many linters now refuse explicit inputs they cannot examine.

## Week of 2026-09-14

- A large citation-precision pass narrowed framework references in dozens of risk, resilience, operations, architecture, governance, compliance, development-security and supply-chain documents to the specific clauses, subcategories and controls each document engages.
- Privacy jurisdiction annexes were corrected against held statutes, unheld regulator-AI claims were hedged across more than a dozen jurisdictions, and the fabricated APEC CBPR 2.0 designation was corrected in nine documents.
- The FedRAMP annex moved to the 2026 Consolidated Rules structure and its documentation model, and the supplier-offboarding template was completed against its exit procedure with tiered deadlines and evidence rows.
- Reference breadth grew with held NIST, ISO/IEC 27035-4, DORA technical-standard, Singapore IMDA agentic-AI and OWASP testing citations in about twenty documents, and the EU general-purpose AI code is stated as voluntary, not binding.
- The compliance finding-tier scheme became consistently five-tier, and the relationship model gained its first substantial slices of verified relationships.
- Behind the scenes, dozens of corpus quality-check engines moved into the standalone reusable pack with behaviour unchanged.

## Week of 2026-09-07

- A corpus-wide control-citation accuracy campaign: cybersecurity-framework governance mappings were narrowed to genuine cybersecurity-governance content, cloud provider-to-customer controls were removed from internal documents including range citations that had swept them in, and dozens of alignment-table cells were corrected to the sub-clauses and safeguards each row matches.
- Privacy jurisdiction annexes were deepened to their statutes: Singapore, South Korea, South Africa, Thailand, New Zealand and Kenya gained their core obligations and data-subject rights, and GDPR-shaped language was reconciled to the held texts across a dozen more jurisdictions, including Brazil, Switzerland, Saudi Arabia, the UAE and Mexico.
- Crypto-asset governance was built out with standards for service-provider vetting, smart-contract and oracle risk, and a domain inventory register, plus deepened MiCA white-paper and market-abuse annex coverage mapped to the held technical standards.
- The executive layer grew with board-facing sets for enterprise risk, IT operations and secure development, continuity and supplier-concentration narratives, and a crypto-asset oversight wave.
- The FedRAMP annex gained its 2026 route-selection and documentation model, MITRE ATLAS agentic-threat updates were engaged, and a new gate audits provider-directional control ranges.

## Week of 2026-08-31

- Five new governance foundations: standards for how a successor AI model establishes its standing on evidence, for temporary and self-expiring emergency authority, for monitoring integrity, and for semantic continuity across model retirement, together with a charter for what a chartered AI actor may and may not decide.
- A workforce network-monitoring compliance suite was added: presence-inference limits, telemetry and inspection controls, a legitimate-interest assessment annex, a works-council consultation procedure and an employee notice, with retention classes and jurisdiction sections to match.
- A crypto-asset and blockchain governance domain opened with a digital-asset custody standard and its own matrix section, and new jurisdiction annexes covered Chile, Peru and Colombia privacy law, South Korea, Illinois and Texas AI law, and a MiCA mapping.
- A source-verified accuracy campaign re-mapped the BASC trade-security citations to the two held instruments across more than twenty documents and the master matrix, and corrected fabricated or mis-fitted control codes in many framework-alignment tables.
- AI total-cost-of-ownership and assurance-evidence frameworks were added, along with CCPA penalty, risk-assessment and automated-decision currency fixes and the UK GDPR's Articles 22A to 22D.
- The standalone Corpus-Management pack consolidation began, vendoring the shared audit-tool core behind digest and drift gates.

## Week of 2026-08-24

- Source-verified corrections ran day after day: EU AI Act classifications, deployer duties, risk tiers and territorial scope were made precise against the current Act, attribution overclaims were corrected so documents distinguish what regulations prescribe from what the organization chooses, and retention, recovery, offboarding and supplier figures were reconciled across domains.
- The exception-authority programme aligned waiver and deviation clauses across the corpus to a single canonical risk-tier approval model, and made two prohibitions absolute: an AI assistant modifying production without human review, and Restricted data on a personal device.
- Access rules tightened: standing privileged access is prohibited wherever just-in-time activation is available, involuntary-termination deprovisioning follows an explicit tiered model, and remote working was reconciled with the bring-your-own-device policy.
- Five new governance foundations closed the week: a principle that capability is never authority, a consolidated AI human-oversight standard, a fail-closed automation principle, a delegation-of-authority standard, and an agentic response model that reserves containment for human authorization.
- Citation currency: OWASP LLM Top 10 remapped to the 2026 edition, CVSS standardized on v4.0, SBOM and EU Cyber Resilience Act obligations stated precisely, and GDPR Article 22 scope corrected.
- The changelog itself was restructured into plain-language weekly summaries, with that style codified as a standing rule, and the adopter on-ramp was improved so a fresh fork clone configures cleanly.

## Week of 2026-08-17

- The website's ground-up redesign reached staging, with on-site pages for all 313 documents, client-side search, need-based path pages and an executive reading room, and the executive shell went live in staging.
- Regulatory-scope accuracy sharpened across the NIS 2, HIPAA and EU AI Act references, including authority attribution and Article 6 bounding in the sector annexes.
- New executive narratives covered identity-provider compromise, release-signing-key compromise, jurisdictional data-service redesign, privileged-access assurance and record retention through destruction.
- A Governance Relationship and Flow Modelling Framework was created and graduated to a generated model with its own gate, and a Canada public-sector GRC annex was begun.
- Consistency fixes reconciled the GDPR breach-notification trigger, document-index owner roles, entitlement-review cadences and the exception-renewal model, and the register corrected Basel III milestones and LINDDUN categories.

## Week of 2026-08-10

- Canada and India content was corrected against held sources: fabricated Partners in Protection material was quarantined, PIPEDA's scope was corrected to commercial activities and federal works, Quebec Law 25 triggers and section citations were fixed, the lapsed Bill C-27 (CPPA and AIDA) is stated accurately in the past tense, and India DPDPA penalties, roles, transfer model and consent framing now follow the Act.
- Canada legal currency recorded the successor private-sector privacy bill (C-36, PPCDA), and the Canada privacy annex was deepened from the held bill text.
- Seven new executive pages were published (oversight question sets, scenarios, a decision narrative and a lifecycle journey), with a de-reproduction pass so executive pages point at sources rather than restating them.
- Citation accuracy continued corpus-wide: ISO 27001:2022 clause corrections, ISO/IEC 42001 clause attributions, Singapore PDPA penalty figures, UK transfer citations moved to UK GDPR Chapter V, withdrawn NIST controls remapped and unevidenced SLSA version tokens dropped.
- NIS 2 Article 23(4) notification sequencing was corrected across the compliance and operations documents, including the trust-service derogation.
- On process, the Five Rules of AIQT were adopted for the project, the public backlog moved to an index form with permanent identifiers, and a licence misstatement in the tooling was corrected to CC BY-SA 4.0.

## Week of 2026-08-03

- A new executive narrative layer began: board-level briefs on AI in production, incident readiness, data governance, resilience and supply-chain oversight, with an authoring specification and six new gates guarding narrative metadata, boundaries, vocabulary and disclaimers.
- The EU AI Act was reconciled across the AI and privacy documents for the in-force Digital Omnibus amendments, including the live Article 27 fundamental-rights impact assessment deadlines.
- A broad source-verified accuracy pass covered Vietnam's new data protection law, Chile's Law 21.719, ISO 19011's 2026 edition, the FAIR taxonomy, CIS Controls v8.1, the current DMARC RFC and dozens of control-code fits.
- The portable governance rules were given a machine-validated publication manifest and readied for standalone publication; they are now published by the AIQT project (https://aiqt.ai).
- The remainder was tooling and safeguard hardening, including daily and weekly roll-up discipline for this changelog.

## Week of 2026-07-27

- Working records and operational material moved out of the public tree, slimming it to the corpus, the audit gates, the rules now published by the AIQT project (https://aiqt.ai), and the commands an adopter actually clones and runs.
- Accuracy fixes modernized the OWASP Web Top 10 rules to the 2025 edition, resolved a self-contradictory AI-logging guidance (security events always logged, content redacted unless an authorized exception applies), made NIST SSDF identifiers valid, and repaired fabricated product call-outs and unsafe cryptography examples in the developer-security rules.
- Citation corrections covered the GDPR breach clock, NIST CSF, ISO/IEC 27002 and NIS 2, and a closing wave fixed CSA CCM and AICM control citations, source-verified.
- The AIQT priority rule gained Progress: accuracy, integrity, quality and trust rank above progress, then speed, then cost.
- New audit gates arrived for NIST SSDF control-identifier validity and for em and en dashes on ungated surfaces, the public backlog split into a guarded two-list model, and the governance rules, since published by the AIQT project (https://aiqt.ai), were generalized to be project-agnostic.

## Week of 2026-07-20

- Newly acquired references were cited across the privacy and security documents: Brazilian adequacy currency, Latin American transfer mechanisms, New York financial-services regulations, OWASP AI security sources and the OWASP Top 10 for Agentic Applications, with the OWASP MCP Top 10 anchoring the MCP security section.
- New annexes covered California's CCPA automated decision-making technology regulations and Singapore's generative-AI governance framework, and the AI policy recorded the Texas and Illinois AI statutes.
- Generic OWASP ASVS citations were remapped to 5.0.0, MITRE ATLAS currency was mapped to the 2026 release, post-quantum cryptography guidance was deepened, and the developer cryptography floors rose to P-384 and RSA-4096.
- Legal-accuracy corrections stated the EU AI Act's Article 18 retention as a floor, removed a fabricated NIST title from two documents, and added the CCPA revenue threshold's inflation-adjustment caveat.
- The remainder was rule work now carried by the AIQT project (https://aiqt.ai) and new audit gates, including a permanence rule that backlog numbers are never recycled.

## Week of 2026-07-13

- The public grclibrary.ai website shipped: a static-site generator producing per-domain and per-document pages, client-side search, a For-AI page with machine-readable dataset metadata, and a build health check in CI.
- The reference-breadth stream concluded: EDPB guidelines and opinions, the NIS 2 implementing regulation, Brazilian ANPD resolutions, Canada's breach-of-safeguards regulations and the AICPA Trust Services Criteria were cited and registered.
- Assessment findings were remediated, including the OWASP ASVS 4.0.3 to 5.0.0 chapter remap and TLS, certificate-key-size and password values reconciled to their governing authorities.
- Jurisdiction accuracy sharpened across Canada and Quebec, including Law 25 penalty and privacy-impact-assessment citations, and the final California CCPA regulations were applied across the US annex, registers, notice template and rights procedure.
- Underneath ran an internal-architecture sprint on adopter portability: a portability check, internal safeguards, a reference-acquisition manifest generator and a run-once fork-onboarding command.

## Week of 2026-07-06

- The corpus's heaviest AI-governance week: new documents on AI value-and-decision governance, synthetic-content provenance, an AI maturity model, data-quality and readiness, and board oversight, with the existing AI documents deepened against held ISO, NIST, OECD, UNESCO and OWASP sources.
- The EU General-Purpose AI Code of Practice was incorporated chapter by chapter, and EU AI Act accuracy was sharpened, including the Article 73 reporting deadline corrected corpus-wide.
- Jurisdiction and sector annexes were added or deepened: Canada, Australia, Colorado, Mexico, New York City Local Law 144, US HIPAA healthcare, eIDAS 2, DORA and NIS 2.
- A new Principle document type was introduced, ranking accuracy, integrity, quality and trust above speed, and speed above cost: the AIQT principle.
- This changelog was reworked into a compact plain-language form across its full history, and new gates checked document-type parity and nested links.

## Week of 2026-06-29

- Dozens of documents were renumbered to the library's uniform section scheme, spelling was harmonized to Canadian orthography (about 2,000 changes across roughly 330 documents), and requirement wording standardized on must.
- A citation-accuracy stream relisted jointly issued standards to their ISO/IEC form, corrected COBIT and ISO 31000 citations, and migrated PCI DSS references to v4.0.1.
- Cross-document conflicts were reconciled to the stricter or canonical value across retention periods, breach and data-subject-request clocks, and risk scoring, and the operational-technology corpus was validated against NIST SP 800-82r3 and ISO 27019.
- New adopter instruments arrived: a privacy-by-design framework, legitimate-interest and transfer-impact assessment templates, a sanctions and export-control screening standard, an M&A due-diligence procedure, a breach-notification regulator register and an AI ethics review panel charter.

## Week of 2026-06-22

- The compliance alignment matrix was expanded domain by domain toward the full document set, with mis-fitting control codes corrected against their source catalogues.
- A corpus-wide citation-accuracy stream fixed CSA Cloud Controls Matrix references, migrated the NIST Cybersecurity Framework to 2.0, and raised transport security to TLS 1.3 corpus-wide.
- Fabricated legal content was corrected, notably Canada's never-enacted CPPA relisted as the in-force PIPEDA across twenty-nine documents, and an invented PIPEDA 72-hour breach target was removed.
- New privacy instruments shipped: a GDPR joint-controller arrangement template, an EU representative appointment process, PIPL cross-border transfer mechanics, a DPO independence and conflict-of-interest framework, and a child-consent age table per Member State.
- Cross-document conflicts were reconciled to canonical values across risk scoring, log retention, data-subject-request records and disaster-recovery backup cadences.

## Week of 2026-06-15

- Mostly internal process and tooling: the mechanical corpus-review capability was built up, this changelog was split and this file kept the public summary, and many audit checks and authoring rules were added.
- Adopter templates arrived: a ten-minute quickstart, a maturity self-assessment, an implementation roadmap, an audit evidence package and a GDPR Article 35 data-protection-impact-assessment template.
- Corpus reconciliation propagated the five-level data-classification scheme, standardized requirement language, and raised retention and transport-security values to their canonical floors, including seven-year retention for corrective-action and internal-audit records.

## Week of 2026-06-01

- Mostly internal rules and tooling work: the developer rules, now published by the AIQT project (https://aiqt.ai), broadened from security-only coverage to development governance, and metadata-rendering and change-tracking gates were added.
- The main corpus-facing addition was a set of per-framework mobile secure-coding rules (Swift, Kotlin, React Native, Flutter, .NET MAUI, and Capacitor or Ionic) plus a currency update to the mobile application security standard.

## Week of 2026-05-25

- The Governance, Risk and Compliance Documentation Library had its first public release, under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) licence.
- A corpus-wide sweep hyperlinked unlinked file references, and stale pre-release artefacts were cleaned from the backlog.
