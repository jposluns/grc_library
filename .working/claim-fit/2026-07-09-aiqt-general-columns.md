# /claim-fit run: AIQT principle document general-framework columns (2026-07-09)

**Scope.** The accepted-unverified tracker queued as TODO 3.21: the general-framework
columns (NIST SSDF, CSA CCM, ISO/IEC 27001) of the AIQT principle document
[`governance/principle-integrity-and-trustworthiness.md`](../../governance/principle-integrity-and-trustworthiness.md)
§ Framework alignment (and the paired AIQT-facet mapping table), which the AIQT PR 2
gate-d approval accepted as corpus-convention with source-text verification queued. The
AI-assurance columns (NIST AI RMF 1.0 / ISO/IEC 42001:2023 / ISO/IEC TR 24028:2020) were
already source-text-verified in AIQT PR 2 (#711) and are out of this scope.

**Worklist.** 25 code citations across the 12 general-framework cells, from the Fable
`aiqt-general-columns-claimfit` verification delivery (scratch `claimfit321-delivery`),
each judged against the held SSDF (OSCAL catalogue), CCM v4.1.0 (CSV rows), and ISO/IEC
27001:2022 (Annex A extract) texts. Read basis: grc_library `011c219` (#713),
grc_library_ref `7a598a0` (#28).

**Judge + orchestrator re-verification.** The worker judged every cell four-valued
(`fits` / `informs` / `mis-attributed` / weak-fit) with a source quote. At apply time the
orchestrator re-verified the two findings against the held texts (validate-then-apply, and
the delivery's flag that the ISO Annex A extract is conversion-scrambled so pairings need
context reads, not line adjacency):

- **CCM LOG codes** confirmed against the authoritative in-repo validator
  [`tools/ccm_aicm_reference.py`](../../tools/ccm_aicm_reference.py) (the module gates 48/49
  enforce): `LOG-08 = "Audit Logs Sanitization"` (the mis-fit: scrubbing sensitive data,
  not audit-trail trust), `LOG-04 = "Audit Logs Access and Accountability"`,
  `LOG-10 = "Audit Records Protection"` (both fit audit-trail trust); `LOG-02 = "Audit Logs
  Protection"` retained.
- **ISO A.5.33** confirmed against the held ISO/IEC 27001:2022 extract by context read:
  the number `5.33` pairs with the title "Protection of records" and the operative text
  "Records shall be protected from loss, destruction, falsification, unauthorized access
  and unauthorized release" (falsification named explicitly, the no-fabrication anchor),
  a stronger fit for work-product integrity than A.8.34 (audit-test planning).

## Findings (2, disposed per the maintainer's overnight authorization #3)

- **F1 (Medium, class-wide): CCM LOG-08 mis-fit for audit-trail-warranted trust.** FIXED
  in the AIQT document: the audit-trail-trust rows (the facet-mapping Trust row and the
  Framework-alignment "Trust warranted by an audit trail" row) migrated
  `LOG-02, LOG-08, GRC-04` to `LOG-02, LOG-04, LOG-10, GRC-04`. The pack-wide
  `LOG-02, LOG-08` convention migration (the same pairing in the change-tracking,
  evidence-grounded-completion, and sibling pack-rule alignment tables) is the class-scope
  half and is folded into the GR-P2 rule condense per the maintainer's authorization (not
  this PR). Bare-token census of the pack-wide carriers deferred to the GR-P2 apply.
- **F2 (Low): ISO A.8.34 weak fit for work-product integrity.** FIXED in the AIQT
  document: the Integrity rows (facet-mapping Integrity row and Framework-alignment
  "Integrity of work product" row) swapped `A.8.34` to `A.5.33` "Protection of records".
  The pack apex rule's own row carries the same A.8.34 and is updated at the next
  pack-table pass (the GR-P2 class-scope note).

## No change

The remaining 21 citations judge `fits` or `informs`, consistent with the document's
corpus-convention labelling ("aligns with / is informed by, never is prescribed by"); no
attribution overstates a source. The corpus-convention caveat sentences (the paragraph
before the facet-mapping table and the closing paragraph) remain accurate and are
unchanged: this pass corrected two demonstrably mis-fit codes, it did not convert the
general column into a per-source-text prescriptive crosswalk. 0 `source-not-held` (SSDF,
CCM, and ISO 27001 are all held). TODO 3.21's accepted-unverified tracker closes on this
disposition.
