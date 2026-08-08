# AIQT doctor

Version: 1.0.0 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 procedure; READ-ONLY and re-runnable; one summary line per check;
non-zero exit only on a definite fault (degraded-but-working states report and exit 0).
The doctor writes nothing: not config, not core, not secrets.

1. **Config parseable.** Every settings line in `.working/aiqt/config.md` matches the
   grammar; guardrail rows well-formed; unknown keys flagged, never deleted.
2. **Bounded write set.** No AIQT-managed file exists outside `.working/aiqt/core/`:
   the doctor walks the AIQT manifest of managed components and verifies every managed
   path resolves under `core/`, and that nothing under `core/` claims to be user-owned.
   This is the mechanical form of the security property stated in the configuration
   format: automated AIQT writes are limited to the `core/` directory, one auditable
   rule an adopter can verify themselves at any time. A managed file found outside
   `core/` is a definite fault (non-zero exit), not a degraded state.
3. **Secrets exist, unread.** For each enabled metered level, the named secret is
   present (`gh secret list` shape); the value is never fetched or printed.
4. **Origins reachable** (granted-consent origins only, per the `EgressConsent`
   settings). HEAD the versions manifest at each; on failure report
   degraded-but-working with the bundled copy's age.
5. **Versions-manifest diff.** Fetch the versions manifest (repository source of truth,
   aiqt.ai mirror); diff installed rows against current; print a summary only: N
   current, N updatable-auto, N held (pin, skip, or AutoUpdate=No), N security-advisory,
   LOUD if any advisory sits on a held row. Per-row action belongs to the updater; the
   doctor only reports.
6. **Level wiring.** For each enabled level, its trigger surface exists: the pre-push
   hook installed; the workflow file present on the default branch; the org secret
   visible to the repository. Review artefacts validate against the shipped contract
   (`review-contract.md`) and its schemas (`schemas/finding.schema.json`,
   `schemas/verdict.schema.json`).
7. **Zip byte-equality.** Where both an unversioned and a versioned artefact are
   reachable (`aiqt.zip` vs the latest `aiqt-X.Y.Z.zip`; `cleanlanguage.zip` likewise),
   verify byte-equality: the unversioned form IS the latest by contract, so inequality
   is a distribution fault to report loudly. Version identity comes from inside the
   artefact, never the filename.
