# /claim-fit run record: one-time Tier-A adoption pass (2026-07-04)

Frozen-state archive per the `.working/` convention; cross-references accurate as-of write-time.

## Scope and baseline

The one-time full Tier-A pass shipping with the `/claim-fit` skill (S3 PR B). Scope: the whole Tier-A census, 11 value-attribution claims from `python3 tools/audit-claim-precision.py --scratch /home/user/grc_library_scratch --tier A` (census: 11 Tier-A + 119 Tier-B; Tier B not sampled this run, the adoption pass is Tier-A-complete by design and the per-batch cadence samples Tier B going forward). Mechanical baseline: `tools/run_all_audits.sh` exit 0 (65/65) on the branch state before the semantic read. Reference base: scratch `ref/` at `e3a088f` (#102); all 11 claims' primary named sources held except UK GDPR and PIPL (see source-not-held).

## Judge dispatch and verdicts

One citation-precision judge subagent over all 11 claims, four-valued verdict vocabulary, every verdict quoting the held source passage (or the failed index lookup). Orchestrator apply-time re-verification: every `mis-attributed` and `informed-not-prescribed` passage re-read in the held texts before treatment as a finding (GDPR Art 33(1) at `:3296`, Art 33(2) at `:3303`, ISO/IEC 42001 retention-and-disposition at `:1097`, EU AI Act Annex IV heading at `:8015`, Art 18 ten-year documentation at `:4146`, Art 19 six-month log minimum at `:4175`; all confirmed).

Verdicts (per source-half):

- **prescribed (12 source-halves)**: GDPR 72-hour breach notification (energy annex :99; startup roadmap :197); GDPR one-month-plus-two DSAR windows (privacy policy :117; DSAR template :85); CCPA/CPRA 45-day and 45+45 extension (both carriers); PIPEDA 30-day (both carriers); GDPR Art 15 access and Art 16 rectification (DSR rows :60/:61); PIPEDA Sch 1 cl 4.9 / 4.9.5 (DSR rows).
- **informed-not-prescribed (4)**: the ISO/IEC 42001 half of the three 7-year retention carriers (requires retention and disposition control, states no period); the DORA reporting windows (the held Level 1 text mandates the report structure and delegates the time limits to the Art 20 RTS, which is not held; the corpus row's "(subject to RTS / ITS)" hedge already signals the delegation, so NO text change; the RTS is queued as a source-drop request).
- **mis-attributed (4)**: the EU AI Act Annex IV half of the three 7-year carriers (Annex IV is the technical-documentation content list and carries no retention obligation; the Act's actual figures are 10 years for provider documentation, Art 18, and at least six months for logs, Art 19, neither 7 years); the 24-hour supplier-notification KPI "per GDPR Article 33(2)" (the article sets "without undue delay").
- **source-not-held (4)**: UK GDPR Arts 15/16 (only the UK DPA 2018 is held, which does not reproduce them) and PIPL Arts 45/46 (a catalogued coverage gap, `ref/COVERAGE-MAP.md` maintainer-drop row). Not adjudicated from memory; queued as source-drop requests.

## Sibling-carrier grep (class width)

Bare-token grep (`7 year|seven year` x `42001`; `33(2)`) widened the fix set beyond the census: the retention register's AI decision-log row (`governance/register-data-retention-schedule.md:108`) asserted "the 7-year floor the citing AI standards state", and the supplier-assurance DPA table (`supply-chain/standard-supplier-security-and-privacy-assurance.md:91`) mapped the 24-hour contractual clock to Art 33(2) without qualification. Verified clean: `governance/register-data-retention-schedule.md:105` (anchored on the internal §4.7.1 floor), `ai/procedure-ai-audit.md:108` and `ai/checklist-ai-algorithmic-compliance.md:99` (anchored on the internal floor / register row), and `privacy/procedure-data-protection-and-privacy-breach-response.md:93/:192` (the §6.3 note already states the operationalization relationship correctly). The pre-push verifier then caught a SIXTH carrier the orchestrator's grep missed because its token pair differs (`governance/register-data-retention-schedule.md:104`, "AI Impact Assessments | 7 years | EU AI Act Article 9", the Act containing no 7-year figure and Article 9 being the risk-management article); fixed in the same PR (register 1.0.16), the same re-ground shape. Flagged for the first per-batch cadence, NOT fixed this run: the register's :106/:107 rows (5 years x "EU AI Act", the same family at a different value) and `governance/standard-records-retention-and-destruction.md:135/:142` (Tier-B soft alignments, "per ISO/IEC 42001 §9" and Annex IV traceability).

## Fixes applied (in-window, attribution phrasing only; no value changed)

Per the FR-120 fix precedent (#294: keep the value as the library's own convention, correct the attribution):

1. `operations/procedure-security-monitoring-and-alert-management.md:298` (1.3.6 to 1.3.7): 7-year retention restated as the organization's canonical period; ISO/IEC 42001 requires retention without prescribing a period; the EU AI Act's log-keeping minimum is shorter.
2. `supply-chain/procedure-third-party-ai-due-diligence.md:130` and `:190` (1.0.4 to 1.0.5): both supplier obligations restated as the organization's contractual floor with the same qualification; the Annex IV attributions removed.
3. `governance/register-data-retention-schedule.md:108` (1.0.14 to 1.0.15): the basis cell re-grounded on "informed by ISO/IEC 42001's retention requirements and the EU AI Act's documentation and log-keeping obligations (Articles 18 and 19), neither of which prescribes the 7-year figure"; the "floor the citing AI standards state" clause corrected.
4. `privacy/procedure-data-protection-and-privacy-breach-response.md:339` (1.4.22 to 1.4.23): the KPI's "(per GDPR Article 33(2))" corrected to "(the contractual operationalization of GDPR Article 33(2)'s 'without undue delay' standard)".
5. `supply-chain/standard-supplier-security-and-privacy-assurance.md:91` (1.1.6 to 1.1.7): the DPA-table requirement cell gains "(the contractual operationalization of the without-undue-delay standard)".
6. `governance/register-data-retention-schedule.md:104` (1.0.15 to 1.0.16, the verifier-caught sixth carrier): the AI-Impact-Assessments basis cell re-grounded as the organization's canonical assessment-retention floor "informed by the EU AI Act Article 9 risk-management obligations (which prescribe no retention period)".

Taxonomy regenerated first, then portal; both `--check` exit 0. No value was changed anywhere; every 7-year and 24-hour figure stands as the organization's canonical/contractual choice, now attributed honestly. Post-fix census re-run (verifier-corrected characterization, computed by running the extractor at both tree states): 8 Tier-A rows, from 11 minus FOUR dropped (the three reworded retention carriers AND the reworded breach-response KPI row no longer match the extractor's value-attribution shape) plus ONE new entrant (the retention register's reworded :108 basis cell now pairs the value and source in one clause, an honestly-hedged standing judge-candidate by design, alongside the DORA row's hedge).

## Routed and queued (not fixed in-window)

- **Source-drop requests to the maintainer** (three): the DORA Article 20 RTS on incident-report time limits (would let a future pass verify the 4h/72h/1-month figures the annex states under its RTS hedge); the UK GDPR consolidated text; the PIPL text (already a catalogued gap). Until these land, the affected attributions stand on their existing hedges and the not-held sources stay unjudged.
- **Currency observation**: the judged `legislation/` and `standards/` catalogue items carry no `last_checked` field, so the scratch 7-day currency throttle has never stamped them; noted for the scratch curation queue (Mode A work, not this repo's).

## Notes

The design entry's early candidates were all confirmed, with one sharpened: the Annex IV half of the 7-year carriers is `mis-attributed` (no retention obligation at all in Annex IV), not merely informed-not-prescribed. Two absent sources (UK GDPR, PIPL) drove all four source-not-held verdicts.
