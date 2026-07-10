# /matrix-fit run: source-doc framework tables (deep-assessment r1 R11)

**Date:** 2026-07-10
**Scope:** the 27 source-document framework-alignment table rows on the semantic-fit worklist (per-document COBIT/CCM/CSF/AICM tables), the follow-on the r1 matrix-fit deferred (it judged the 66 compliance-matrix rows only). Closes TODO §3.25.
**Mechanical baseline:** 67/67 green at HEAD `dcd3267` (#768) before the pass; 67/67 green after fixes.
**Reference base:** the gate-validated in-repo modules ([`tools/ccm_aicm_reference.py`](../../tools/ccm_aicm_reference.py) CCM v4.1 + AICM v1.1, [`tools/cobit_iso31000_reference.py`](../../tools/cobit_iso31000_reference.py), [`tools/nist_csf_reference.py`](../../tools/nist_csf_reference.py)). Every judgement quotes a source control TITLE read from these this run.
**Resulting PR:** #769.

## Worklist

`python3 tools/audit-matrix-semantic-fit.py --source-docs-only` produced 27 rows / 74 code-instances (all overlap-0 lexical candidates; a worklisted row is a focus candidate, not a confirmed defect).

## Judges

Two independent judge subagents, partitioned cleanly by document (11 docs / 16 docs), each briefed to refute (hunt genuine wrong-control mismatches), each quoting the code, its held source title, and `path:line`. Combined: 65 code-instances judged, 33 fits, 20 loose-supporting, **12 mismatch**. Every mismatch was apply-time-verified by the orchestrator against the reference module title AND the actual row before routing.

## Confirmed mismatches (12), all fixed in-window

Each verified against the held CCM v4.1 title; matrix corroboration noted where the compliance matrix (r1-judged) already carries the correct control.

| # | Location | Wrong code (title) | Correct code (title) | Corroboration |
|---|---|---|---|---|
| 1 | `dev-security/standard-quality-assurance-and-testing.md:128` | SEF-06 'Event Triage Processes' (label fabricated as "Testing and Quality Assurance") | CCC-02 'Quality Testing' | matrix:349 already maps this doc to CCC-02 |
| 2 | `security/standard-logging-and-monitoring.md:139` (Log management) | I&S-09 'Network Defense' | LOG-01 'Logging and Monitoring Policy and Procedures' | matrix:143 maps this doc to LOG-01/02/03/04 |
| 3 | `security/standard-logging-and-monitoring.md:141` (Central collection and retention) | SEF-01 'Security Incident Management Policy and Procedures' | LOG-02 'Audit Logs Protection' | matrix:143 |
| 4 | `security/standard-logging-and-monitoring.md:143` (AI system traceability) | I&S-09 'Network Defense' | LOG-12 'Transaction/Activity Logging' | matrix:143 |
| 5 | `security/standard-logging-and-monitoring.md:144` (Monitoring and alerting) | SEF-01 'Security Incident Management Policy and Procedures' | LOG-03 'Security Monitoring and Alerting' (near-verbatim) | matrix:143 |
| 6 | `security/standard-threat-modelling.md:179` (Design-time threat analysis) | CCC-06 'Change Management Baseline' (kept AIS-04) | TVM-04 'Threat Analysis and Modelling' | matrix:168 already carries TVM-04 |
| 7 | `security/standard-threat-modelling.md:180` (Documented data-flow diagrams) | CCC-04 'Unauthorized Change Protection' | TVM-04 'Threat Analysis and Modelling' | matrix:168 |
| 8 | `security/standard-threat-modelling.md:183` (Abuse-case authoring) | CCC-06 'Change Management Baseline' | TVM-04 'Threat Analysis and Modelling' | matrix:168 |
| 9 | `security/standard-threat-modelling.md:184` (Privacy threat modelling, LINDDUN) | DSP-02 'Secure Disposal' | DSP-08 'Data Privacy by Design and Default' | held title |
| 10 | `operations/procedure-media-handling-and-transport.md:288` (Physical transport and chain of custody) | DSP-07 'Data Protection by Design and Default' | DCS-05 'Secure Media Transportation Policy and Procedures' (exact) | held title |
| 11 | `operations/procedure-media-handling-and-transport.md:291` (Sanitization and destruction) | DSP-07 'Data Protection by Design and Default' | DSP-02 'Secure Disposal' | held title |
| 12 | `operations/procedure-endpoint-management-and-device-compliance.md:308` (Decommissioning and media sanitization) | DSP-07 'Data Protection by Design and Default' | DSP-02 'Secure Disposal' | held title |

Paired-surface carrier fixed: the logging doc's purpose prose (`security/standard-logging-and-monitoring.md:23`) cited "CSA CCM v4.1 I&S-09 and SEF-01"; reworded to "LOG-01 and LOG-03". The QA-testing doc's document-index register row (`governance/register-document-index-and-classification.md:299`) carried "CSA CCM SEF-06"; corrected to "CSA CCM CCC-02".

## Invalid-code-family discovery (ISM): 8 instances remapped in-window (maintainer-directed fold-in)

A separate class the pass surfaced: an invalid `ISM-01/02/03/04/05/10/12` code family cited in columns headed "CSA CCM v4.1" across two documents, none of which are CCM v4.1 domains (CCM has no ISM domain; confirmed zero ISM entries in the reference module). Every instance passed all gates (the control-code existence gate skips a token whose prefix it does not recognize as CCM). The maintainer directed folding the code remaps into R11 (with the gate-hardening routed separately to TODO §3.40).

| Location | Row | Invalid code | Remap (held-verified) |
|---|---|---|---|
| `security/policy-information-security.md:136` | Governance and ISMS | ISM-01 | GRC-01 'Governance Program Policy and Procedures', GRC-05 'Information Security Program' |
| `security/policy-information-security.md:137` | Asset Management | ISM-02 | DCS-06 'Assets Classification', DCS-07 'Assets Cataloguing and Tracking' |
| `security/policy-information-security.md:140` | Vulnerability and Patch | ISM-04 | TVM-03 'Vulnerability Identification', TVM-08 'Vulnerability Remediation Schedule' |
| `security/policy-information-security.md:141` | Incident Management | ISM-05 | SEF-01 'Security Incident Management Policy and Procedures', SEF-07 'Incident Management and Response' |
| `security/policy-information-security.md:142` | AI Model Security | ISM-10 | N/A (CCM v4.1 has no AI-model control; the AI controls live in AICM v1.1, a different matrix than this "CSA CCM v4.1" column) |
| `security/policy-information-security.md:143` | Continuous Improvement | ISM-12 | N/A (CCM v4.1 has no continual-improvement control; the row already carries COBIT MEA01) |
| `security/standard-logging-and-monitoring.md:140` | Time synchronization | ISM-04 | LOG-06 'Clock Synchronization' (exact) |
| `security/standard-logging-and-monitoring.md:142` | Access and protection | ISM-03 | LOG-04 'Audit Logs Access and Accountability' |

The two `N/A` cells are the honest, non-fabricating choice (stricter-safe): no CCM v4.1 control genuinely covers AI model security or ISMS continual improvement, and forcing an AICM code into a CCM v4.1 column would be a new header mismatch. Surfaced for maintainer redirect.

## Routed (not fixed): TODO §3.40 and §3.41

- **§3.40** (gate blind-spot): harden the CCM/AICM control-code existence gate to flag a control-code-shaped token in a CSA-CCM framework-as-column cell whose prefix is not a known CCM/AICM domain (the ISM class), with a regression fixture. Deep-assessment r2 candidate.
- **§3.41** (loose-supporting improvements + media matrix reconciliation): the 20 loose-supporting rows the judges flagged as defensible-but-improvable (media DSP-07 blanket column, endpoint TVM-06, library-cadence APO01, records-retention DSP-02 vs the fuller DSP-16 plus its inaccurate printed title), and two matrix-vs-per-doc CCM divergences: media-handling (matrix:188 DSP-04/DSP-05 vs per-doc DSP-07/DCS-05/DSP-02) and threat-modelling (matrix:168 still carries CCC-06 after R11 removed it from the doc's own column, surfaced by the R11 pre-push verifier). Quality/consistency reconciliations, not correctness defects.

## Termination

Single advisory pass. Worklist judged, 12 confirmed mismatches fixed, 8 ISM invalid codes remapped, 2 residue classes routed to TODO. Mechanical baseline re-confirmed 67/67 green after fixes.
