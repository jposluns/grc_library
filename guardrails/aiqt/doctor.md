# AIQT doctor

Version: 1.0.6 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 procedure; READ-ONLY and re-runnable; one summary line per check;
non-zero exit only on a definite fault (degraded-but-working states report and exit 0).
The doctor writes nothing: not config, not core, not secrets. Where a check depends on
an AIQT artefact that has not shipped yet, the check states what it does TODAY and what
it upgrades to, and reports an explicit status rather than staying silent.

1. **Config parseable.** Every settings line in `.working/aiqt/config.md` matches the
   grammar, including the dotted-qualifier production (one qualifier level; the first
   dot separates the setting name from the lowercase hostname qualifier); guardrail
   rows well-formed; unknown keys flagged, never deleted.
2. **Bounded write set.** The security property: the two automated AIQT writers each
   stay within their own root, the UPDATER within `.working/aiqt/core/` (behaviour-bearing
   guardrail content) and the review RUNTIME within `.working/aiqt/findings/` plus the
   config-file Usage section (operational records that never alter guardrail content),
   two auditable rules an adopter can verify at any time. The findings records are
   operational and are explicitly OUT of the managed-file scan's scope below. TODAY
   (no component-header grammar or managed-component manifest has shipped yet): the
   check verifies that `core/` exists wherever the config declares AIQT installed, and
   reports an explicit NOT-YET-ENFORCEABLE status for the outside-core managed-file
   scan, naming the artefact it waits on. It upgrades TWICE: first, when the layer
   conventions document ships the component-header marker, the check scans for
   header-bearing files outside `core/`; second, when the updater ships the
   managed-component manifest, the check walks the manifest as the authoritative
   managed set. From the header-marker upgrade onward, a managed file found outside
   `core/` is a definite fault (non-zero exit), never a degraded state.
3. **Secrets exist, unread.** For each enabled metered level, the named secret is
   present (`gh secret list` shape); the value is never fetched or printed. The secret
   names are the CI kit's (`ci-kit/README.md`): `CLAUDE_CODE_OAUTH_TOKEN` or
   `ANTHROPIC_API_KEY` for the Claude lane, `OPENAI_API_KEY` for the Codex lane; a
   repository with no CI level enabled reports an explicit NOT-CONFIGURED status
   (never silent, never a fault).
4. **Origins reachable** (granted-consent origins only, per the `EgressConsent.<origin>`
   settings). The HEAD probe applies only to origins with a NAMED distribution
   artefact: today that is aiqt.ai (the versioned `aiqt-X.Y.Z.zip` and the unversioned
   `aiqt.zip`) and cleanlanguage.ai (`cleanlanguage.zip`). github.com carries no
   doctor-checkable artefact today (its consent is exercised by CI and updater
   fetches), so the doctor reports it as consent-recorded, no-artefact-to-check, an
   explicit status, never a silent skip. The probe upgrades to HEADing the versions
   manifest when the release train publishes one. On failure report
   degraded-but-working with the bundled copy's age.
5. **Versions-manifest diff.** TODAY (until the release train publishes the versions
   manifest): report the installed `AIQTVersion` and the bundled copy's age as an
   explicit NOT-CONFIGURED status. It upgrades to: fetch the versions manifest
   (repository source of truth, aiqt.ai mirror); diff installed rows against current;
   print a summary only: N current, N updatable-auto, N held (pin, skip, or
   AutoUpdate=No), N security-advisory, LOUD if any advisory sits on a held row.
   Per-row action belongs to the updater; the doctor only reports.
6. **Level wiring.** For each ENABLED level, its OWN trigger surface exists, per the
   level definitions: Level 1 set to `Automatic`, the pre-push hook is installed
   (`OnRequest` has no standing surface, and the check reports valid-config, no
   standing surface for it, explicitly; `Off` disables the level, and a disabled
   level's surfaces are not checked); Level 2 enabled, the workflow file is present
   on the default branch; Level 3 enabled, the org secret is visible to the
   repository. Where review artefacts are
   present, they validate against the shipped contract (`review-contract.md`) and its
   schemas (`schemas/finding.schema.json`, `schemas/verdict.schema.json`).
7. **Zip byte-equality.** Where both an unversioned and a versioned artefact are
   reachable (`aiqt.zip` vs the latest `aiqt-X.Y.Z.zip`; `cleanlanguage.zip` likewise),
   verify byte-equality: the unversioned form IS the latest by contract, so inequality
   is a distribution fault to report loudly. Version identity comes from inside the
   artefact, never the filename.
8. **Findings queue health.** Read `.working/aiqt/findings/QUEUE.md` (the findings-loop
   document defines it) and report the unconsumed count, the oldest unconsumed age, and
   the resurface-due count. Read-only; staleness is surfaced here, never auto-consumed.
   A repository with no queue file reports an explicit NOT-CONFIGURED status (the local
   runtime creates it at its first review run).
