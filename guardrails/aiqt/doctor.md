# AIQT doctor

Version: 1.0.1 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 procedure; READ-ONLY and re-runnable; one summary line per check;
non-zero exit only on a definite fault (degraded-but-working states report and exit 0).
The doctor writes nothing: not config, not core, not secrets. Where a check depends on
an AIQT artefact that has not shipped yet, the check states what it does TODAY and what
it upgrades to, and reports an explicit status rather than staying silent.

1. **Config parseable.** Every settings line in `.working/aiqt/config.md` matches the
   grammar; guardrail rows well-formed; unknown keys flagged, never deleted.
2. **Bounded write set.** No AIQT-managed file exists outside `.working/aiqt/core/`.
   TODAY (until the updater's managed-component manifest ships): the managed set is
   every AIQT-header-bearing file in the repository, and the check verifies none exists
   outside `core/`, and that nothing under `core/` claims to be user-owned. It upgrades
   to walking the managed-component manifest when the updater ships it. This is the
   mechanical form of the security property stated in the configuration format:
   automated AIQT writes are limited to the `core/` directory, one auditable rule an
   adopter can verify themselves at any time. A managed file found outside `core/` is a
   definite fault (non-zero exit), not a degraded state.
3. **Secrets exist, unread.** For each enabled metered level, the named secret is
   present (`gh secret list` shape); the value is never fetched or printed. The secret
   names come from the CI integration kit; until it ships, this check reports an
   explicit NOT-CONFIGURED status (never silent, never a fault).
4. **Origins reachable** (granted-consent origins only, per the `EgressConsent.<origin>`
   settings). TODAY: HEAD the distribution artefacts the consent step names at each
   granted origin; it upgrades to HEADing the versions manifest when the release train
   publishes one. On failure report degraded-but-working with the bundled copy's age.
5. **Versions-manifest diff.** TODAY (until the release train publishes the versions
   manifest): report the installed `AIQTVersion` and the bundled copy's age as an
   explicit NOT-CONFIGURED status. It upgrades to: fetch the versions manifest
   (repository source of truth, aiqt.ai mirror); diff installed rows against current;
   print a summary only: N current, N updatable-auto, N held (pin, skip, or
   AutoUpdate=No), N security-advisory, LOUD if any advisory sits on a held row.
   Per-row action belongs to the updater; the doctor only reports.
6. **Level wiring.** For each ENABLED level, its OWN trigger surface exists, per the
   level definitions: Level 1 enabled, the pre-push hook is installed; Level 2 enabled,
   the workflow file is present on the default branch; Level 3 enabled, the org secret
   is visible to the repository. A disabled level's surfaces are not checked. Where
   review artefacts are present, they validate against the shipped contract
   (`review-contract.md`) and its schemas (`schemas/finding.schema.json`,
   `schemas/verdict.schema.json`).
7. **Zip byte-equality.** Where both an unversioned and a versioned artefact are
   reachable (`aiqt.zip` vs the latest `aiqt-X.Y.Z.zip`; `cleanlanguage.zip` likewise),
   verify byte-equality: the unversioned form IS the latest by contract, so inequality
   is a distribution fault to report loudly. Version identity comes from inside the
   artefact, never the filename.
