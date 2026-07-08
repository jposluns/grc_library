# /matrix-fit run: closing whole-matrix semantic-fit audit (2026-06-30)

Detail record for the FR-167 closing whole-matrix `/matrix-fit` (closure item (a), the "matrix completion" close-check). History row: [`history.md`](history.md). Closing PR: #490.

This file is maintainer working state, exempt from corpus audit gates. `path:line` references are accurate as-of write-time (`fef6a58` plus this PR's fix).

## Scope and mechanical baseline

- **Scope**: the whole compliance matrix [`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md) plus the per-document framework-alignment tables (the "matrix completion" cadence).
- **Mechanical baseline**: `tools/run_all_audits.sh` = all 57 gates pass at `fef6a58` (the post-#489 state). A fit pass judges among rows that already pass the existence gates 48/49/54.
- **Reference base**: [`tools/ccm_aicm_reference.py`](../../tools/ccm_aicm_reference.py) (CSA CCM v4.1 + AICM v1.1 codes and titles), [`tools/nist_csf_reference.py`](../../tools/nist_csf_reference.py) (NIST CSF 2.0 category titles), and the reference-base standards extracts. Judges read control TITLES from these, never from memory.

## Worklist (Step 2)

`python3 tools/audit-matrix-semantic-fit.py` (AICM-scoped since #449, `4c632ec`: `KNOWN_TITLES` loads `AICM_V11`, `scan_matrix` reads the "CSA AICM v1.1" column) produced a recall-oriented worklist of overlap-0 rows: **62 compliance-matrix rows + 16 per-document framework-table rows = 78 candidate rows**. A worklisted row is a focus candidate (no lexical anchor between document subject and cited control titles), not a confirmed defect.

## Judge dispatch (Step 3)

Five independent judge subagents, each briefed to judge every cited CCM/AICM/CSF code against its source control TITLE and report `mismatch` / `loose-supporting` with quoted title + `path:line`:

- Slice A: matrix rows :54-:113 (16 rows). Return: 0 mismatch; 2 soft loose-supporting (A&A-01 on :61 ESG, STA-01/GV.SC on :60 Sustainability).
- Slice B: matrix rows :114-:170 (14 rows). Return: 0 mismatch; 2 loose-supporting (ID.AM on :149 PQC, ID.IM on :170 Acceptance Into Service).
- Slice C: matrix rows :182-:275 (18 rows). Return: 0 mismatch; 0 reportable loose-supporting (one awareness note: LOG-15/LOG-16 on :194 Observability fit iff the doc covers AI I/O monitoring).
- Slice D: matrix rows :309-:381 (14 rows). Return: 0 mismatch; 4 loose-supporting (MDS-03 on :312 ADR, AIS-05 on :349 AI-algorithmic-compliance checklist, BCR-01 and STA-11 on :372 AI-inference-cost).
- Slice E: 16 per-document framework-table rows. Return: **2 mismatch** (AIS-01 and HRS-01 on `operations/register-asset-inventory.md`); 4 loose-supporting (DSP-07 as a blanket code on media-handling and endpoint-decommissioning rows; DSP-02 on the LINDDUN privacy row of the threat-modelling standard; I&S-09 on the logging-and-monitoring standard).

## Apply-time verification (Step 4)

The orchestrator re-read the one confirmed-mismatch source before treating it as a finding (judge output is research, not finding):

- Confirmed at [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md):125 the cell read `| CSA CCM v4.1 | AIS-01 / HRS-01 | Cloud asset inventory and management |`.
- Confirmed titles in [`tools/ccm_aicm_reference.py`](../../tools/ccm_aicm_reference.py): `AIS-01` = "Application and Interface Security Policy and Procedures"; `HRS-01` = "Background Screening Policy and Procedures". Both unrelated to an asset inventory.
- Identified the correct controls: `DCS-06` = "Assets Classification" and `DCS-07` = "Assets Cataloguing and Tracking" (the CCM v4.1 asset-inventory family, peer to the row's ISO A.5.9 / NIST CM-8 / COBIT BAI09).
- Cross-corroborated against the compliance matrix's own row for the same document: [`compliance/matrix-grc-compliance-alignment.md`](../../compliance/matrix-grc-compliance-alignment.md):196 maps `Register: Asset Inventory` to `DCS-06, DCS-07, UEM-04`. The matrix (authoritative) and the per-document table disagreed; the per-document table was wrong.
- Parallel-occurrence check: `AIS-01 / HRS-01` co-occurs nowhere else in the corpus (single occurrence; grep confirmed).

## Triage and fix (Step 5)

- **Fixed in-window**: corrected the per-document cell to `DCS-06 / DCS-07`, co-bumped `register-asset-inventory.md` Version 1.0.4 to 1.0.5 and Date to 2026-06-30, regenerated `taxonomy.yml` then `docs/maturity-scorecard.md`. This aligns the per-document table with the matrix and the canonical CCM controls (the stricter-safe, standard-supported correction).
- **Not changed (loose-supporting)**: every loose-supporting flag above is a defensible supporting mapping (the cited code is a reasonable secondary control even where a more precise one exists). Per the skill these are recorded for awareness, not routed as mismatches; per the overnight directive, ambiguous re-mappings are not auto-applied. None rises to a mismatch on apply-time re-read.

## Result

- The compliance matrix **proper** is clean: 0 mismatches across all 62 worklisted rows.
- The per-document framework-alignment tables surfaced **1 confirmed mismatch**, fixed.
- FR-167 closure item **(a)** (the closing whole-matrix `/matrix-fit`) is complete. Closure item **(b)** (matrix gap-fill, add rows for substantive documents not yet rowed) remains; FR-167 stays open.
