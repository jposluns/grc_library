# Changelog

All notable changes to this repository are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](specification-master-project.md) section 4.5.

## 2026-06-02, Library Version 2026.06.8

Mobile-app security work, Phase 6 of 8: .NET MAUI pack rule file.

### Added

- [`dev-security/claude-rules/languages/dotnet-maui.md`](dev-security/claude-rules/languages/dotnet-maui.md) — new pack rule file for .NET MAUI applications (including Blazor Hybrid). The existing [`languages/csharp.md`](dev-security/claude-rules/languages/csharp.md) remains the server-side C# rule file. Covers secure-storage delegation (`SecureStorage` and encrypted SQLite over `Preferences` and unencrypted SQLite), cross-platform handlers and dependency-service trust boundary (narrow validated APIs; Blazor Hybrid `IJSRuntime` interop boundary), network (certificate pinning via custom `RemoteCertificateValidationCallback`), backend attestation through platform-conditional `IAttestationService` implementations, build hardening and release configuration (csproj `PropertyGroup` settings for iOS / Android release; ProGuard / R8 enable; trimming review; hot-reload kept to debug), deep links via MAUI Shell with App Links / Universal Links, permissions (`Permissions.RequestAsync<>` with narrow scope), in-app purchases (`Plugin.InAppBilling` / `Xamarin.Essentials.InAppPurchase` with backend verification of platform receipt / `purchaseToken`), logging and crash-reporter redaction, and Blazor Hybrid WebView specifics (`MarkupString` hazards, CSP delivery via host page).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.16.0`. Directory-structure ASCII tree gains an entry for [`languages/dotnet-maui.md`](dev-security/claude-rules/languages/dotnet-maui.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.7 → 2026.06.8`; README `1.7.145 → 1.7.146`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: zero findings first attempt. Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 7, 10, 13, 14 point at actual content. The opening hybrid-framework rule restates Section 13's "shifts layers, doesn't remove controls" applied to MAUI's specific architecture (Mono / .NET runtime + handler pattern). The version-date consistency audit (gate 29) confirms `2026.06.8` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased rollout context

Phase 6 of 8. Phase 7 completes the mobile-app work with Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.7

Mobile-app security work, Phase 5 of 8: Flutter pack rule file.

### Added

- [`dev-security/claude-rules/languages/flutter.md`](dev-security/claude-rules/languages/flutter.md) — new pack rule file for Flutter applications written in Dart. Covers secure-storage delegation (`flutter_secure_storage` + `sqflite_sqlcipher` over `shared_preferences` and unencrypted sqflite), platform channels and FFI as trust boundaries (with Kotlin native-side validation examples), network (`http_certificate_pinning` for Tier 1 / Tier 2), backend attestation forwarded through a Flutter package, debug-tooling exclusion (`kReleaseMode` gating, `--obfuscate --split-debug-info` for release builds, Dart DevTools restricted to debug / profile), OTA updates (Shorebird as the signed-payload option; raw code-OTA prohibited by Apple / Google store terms by default), deep links (App Links / Universal Links over custom schemes), permissions (narrow scope via `permission_handler`), in-app purchases (`in_app_purchase` plugin with backend verification of `serverVerificationData`), and logging / crash-reporter redaction.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.15.0`. Directory-structure ASCII tree gains an entry for [`languages/flutter.md`](dev-security/claude-rules/languages/flutter.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.6 → 2026.06.7`; README `1.7.144 → 1.7.145`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: zero findings first attempt. Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 10, 13, 14 point at actual content. The opening hybrid-framework rule mirrors the standard's Section 13 opener applied to Flutter's specific architecture (platform channels and Dart runtime). The version-date consistency audit (gate 29) confirms `2026.06.7` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased rollout context

Phase 5 of 8. Phases 6-7 add .NET MAUI and Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.6

Mobile-app security work, Phase 4 of 8: React Native pack rule file.

### Added

- [`dev-security/claude-rules/languages/react-native.md`](dev-security/claude-rules/languages/react-native.md) — new pack rule file for React Native applications (with or without Expo). Implements Section 13 (hybrid frameworks) of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) plus the native-layer sections as they apply through the JS bridge. Covers secure-storage delegation (`react-native-keychain` and encrypted MMKV over `AsyncStorage` and the unencrypted MMKV constructor), JS bridge as a trust boundary (legacy bridge and JSI / TurboModule), network with certificate pinning (`react-native-ssl-pinning`), backend attestation forwarded through a thin native module, debug-tooling exclusion (`__DEV__` dead-code elimination; Flipper / Reactotron / react-native-debugger guarded), over-the-air updates (CodePush, EAS Update, Shorebird) with signed payloads and no-new-permissions rule, deep links (Universal Links / App Links over custom schemes), permissions (rationale must match actual data flow), in-app purchases (`react-native-iap`, `expo-in-app-purchases`, RevenueCat — backend verification of `transactionReceipt` / `purchaseToken` required regardless), and crash-reporter PII redaction. Closing section covers Expo-specific notes (`expo-secure-store`, EAS Build signing, EAS Update channels).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.14.0`. Directory-structure ASCII tree gains an entry for [`languages/react-native.md`](dev-security/claude-rules/languages/react-native.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.5 → 2026.06.6`; README `1.7.143 → 1.7.144`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: one finding caught and fixed pre-audit (one em-dash in the RevenueCat parenthetical; restructured into two sentences). Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 10, 13, 14 point at actual content. The opening hybrid-framework rule ("React Native shifts the layer at which a control is implemented; it does not remove the control") quotes the standard's Section 13 opener. The version-date consistency audit (gate 29) confirms `2026.06.6` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 4 of 8. Phases 5-7 add Flutter, .NET MAUI, and Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.5

Mobile-app security work, Phase 3 of 8: Android pack rule file.

### Added

- [`dev-security/claude-rules/languages/kotlin.md`](dev-security/claude-rules/languages/kotlin.md) — new pack rule file for Android applications written in Kotlin or Java. Covers secure storage (`EncryptedSharedPreferences`, `EncryptedFile`, manifest backup posture), cryptography (Android Keystore with StrongBox for Tier 1, AES-GCM, `SecureRandom`), authentication and local biometrics (`BiometricPrompt` with `CryptoObject` binding, `setInvalidatedByBiometricEnrollment`, Custom Tabs for OAuth), network and Network Security Configuration (cleartext denied, user-CA trust off, OkHttp `CertificatePinner` and `<pin-set>`), backend attestation (Play Integrity with backend verification), platform interaction (App Links over custom schemes, explicit intents for cross-app data, logging redaction), `WebView` hardening (origin allow-list, narrow `addJavascriptInterface`, file-access flags off), permissions and privacy (narrow scope, Photo Picker preference), distribution and signing (Play App Signing, ProGuard / R8, R8 mapping file preservation), in-app billing (`purchaseToken` server-side verification, acknowledgement gating), and reverse-engineering resistance (root detection as signal, R8 obfuscation, Frida / Xposed hook detection for Tier 1). Every section cross-references the implementing section of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md). The opening note clarifies that [`languages/java.md`](dev-security/claude-rules/languages/java.md) remains the server-side Java rule file and is distinct from the Android-Java patterns documented here.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.13.0`. The directory-structure ASCII tree gains an entry for [`languages/kotlin.md`](dev-security/claude-rules/languages/kotlin.md). The "Rule files and their scope" table gains a new row.
- [`README.md`](README.md): library version `2026.06.4 → 2026.06.5`; README version `1.7.142 → 1.7.143`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file: zero findings on first attempt (no em-dashes, no `-ise` verbs, no bare "ensure", no sanitisation terms). Re-read the file in full to confirm each Section cross-reference points at actual content of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): Sections 2, 3, 4, 5 (including the new attestation row from Phase 1), 6, 7, 9, 10, 14. The version-date consistency audit (gate 29) confirms `2026.06.5` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 3 of 8 in the mobile-app security work. Phases 4-7 add the cross-platform pack rule files: React Native, Flutter, .NET MAUI, Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.4

Mobile-app security work, Phase 2 of 8: first per-language pack rule file for mobile.

### Added

- [`dev-security/claude-rules/languages/swift.md`](dev-security/claude-rules/languages/swift.md) — new pack rule file for iOS applications written in Swift or Objective-C. Covers secure storage (Keychain accessibility classes, Data Protection classes, backup exclusion), cryptography (CryptoKit, Secure Enclave, `SecRandomCopyBytes`), authentication and local biometrics (biometry as step-up not sole credential, `ASWebAuthenticationSession`, biometry-current-set binding), network and ATS (scoped exceptions, certificate pinning via `URLSessionDelegate`), backend attestation (App Attest with backend verification), platform interaction (Universal Links over custom schemes, OSLog privacy markers), `WKWebView` hardening (origin allow-list, restricted bridges), App Tracking Transparency (honest prompts), code signing and distribution, in-app purchases (server-side `jwsRepresentation` verification per the new Section 14), and reverse-engineering resistance (jailbreak detection as a signal, compiler hardening defaults). Every section cross-references the implementing section of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.12.0`. The directory-structure ASCII tree gains an entry for the new file [`languages/swift.md`](dev-security/claude-rules/languages/swift.md); the existing entries for [`languages/csharp.md`](dev-security/claude-rules/languages/csharp.md) and [`languages/java.md`](dev-security/claude-rules/languages/java.md) are clarified as "(server-side)" to distinguish them from the new mobile-language rule files arriving in this and subsequent phases. The "Rule files and their scope" table gains a new row for the swift rule.
- [`README.md`](README.md): library version `2026.06.3 → 2026.06.4`; README version `1.7.141 → 1.7.142`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file. Two findings caught and fixed pre-audit: one `-ise` verb (`recognising` → "with the caveat that") and one em-dash (replaced with a sentence break). Re-read the swift.md file in full to confirm each Section cross-reference points at the actual content of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): Section 2 storage, Section 3 cryptography, Section 4 auth, Section 5 network plus the new attestation row, Section 6 platform interaction, Section 7 MASVS-R, Section 9 distribution, Section 10 privacy, and Section 14 IAP (added in Phase 1). The version-date consistency audit (gate 29) confirms `2026.06.4` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 2 of 8 in the mobile-app security work. Phases 3-7 add the remaining per-language pack rule files: Kotlin, React Native, Flutter, .NET MAUI, Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.3

Mobile-app security work, Phase 1 of 8: expand the mobile standard with three substantive additions that close 2024-2026 currency gaps. Per-doc version bumped `1.0.1 → 1.1.0` (minor bump per semver for added sections).

### Added

- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) Section 5 gains a new "Backend attestation" row: iOS App Attest / DeviceCheck and Android Play Integrity for Tier 1 / Tier 2 backends, server-side verification, short-lived tokens, replay-protected. The attestation requirement is anchored to the existing sensitivity-tier model in Section 1; previously absent.
- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) **new Section 13: hybrid and cross-platform frameworks**, naming React Native, Flutter, .NET MAUI, Capacitor / Ionic explicitly. Eight control rows covering secure storage delegation (the `react-native-keychain` / `flutter_secure_storage` / MAUI `SecureStorage` pattern over framework defaults like `AsyncStorage`), JS-or-Dart bridge as a trust boundary, native module review, debug-tooling exclusion in release builds, over-the-air update integrity (CodePush, EAS Update, Shorebird, Appflow Live Updates), Content Security Policy in wrapped WebViews, framework currency, and framework-specific build hardening. The opening paragraph states the rule that hybrid frameworks shift layers but do not reduce the set of controls.
- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) **new Section 14: in-app purchases and receipt validation**. Eight control rows covering server-side validation against StoreKit / Google Play Developer API / Microsoft Store services, replay protection, price-tier validation, subscription state polling, sandbox-vs-production environment routing, refund / chargeback honour, restore-purchase flow constraints, and the boundary with side-loaded or web-checkout paths.

### Changed

- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) per-document version `1.0.1 → 1.1.0`. "Operating expectations" section grows from 4 items to 7, adding bullets for annual attestation-flow verification (item 5), hybrid framework currency verification per release (item 6), and per-release IAP receipt-validation exercise (item 7).
- [`README.md`](README.md): library version `2026.06.2 → 2026.06.3`; README version `1.7.140 → 1.7.141`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the modified standard; no findings (no em-dashes, no `-ise` verbs, no bare "ensure", no sanitisation terms). Re-read the full standard after edits to confirm no contradiction between the new Section 5 attestation row, the new Section 13 hybrid-framework section, and the existing tier model in Section 1: Tier 1 and Tier 2 attestation requirements in Section 5 align with Section 1's sensitivity-tier definitions; Section 13's opening "do not reduce the set of controls" statement is consistent with Sections 2-10 remaining in force. The version-monotonicity audit (gate 13) confirms `1.0.1 < 1.1.0`. The version-date consistency audit (gate 29) confirms library `2026.06.3` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 1 of 8 in the mobile-app security work. Phase 0 ratified all v0.0.1 files to v1.0.1. Phases 2-7 add per-language pack rule files (Swift, Kotlin, React Native, Flutter, .NET MAUI, Capacitor / Ionic) that cite the now-complete standard.

---

## 2026-06-02, Library Version 2026.06.2

Mobile-app security work, Phase 0 of 8: project-wide ratification signal. All documents previously at v0.0.1 are bumped to v1.0.1 to signal that the content is no longer "first draft" status and is ratified for downstream use.

### Changed

- 54 documents bumped from `v0.0.1` to `v1.0.1`. Mechanical version-string + date-field change only; no content edits. Domains touched: `ai/` (5), `architecture/` (6), `compliance/` (1), `dev-security/` (2), `docs/` (1), `governance/` (7), `operations/` (4), `privacy/` (8), `resilience/` (5), `risk/` (4), `security/` (6), `supply-chain/` (5), plus repo-root [`CONTRIBUTING.md`](CONTRIBUTING.md). Each file's `**Date:**` field updated to `2026-06-02` to anchor the next review cycle.
- [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated from the bumped metadata (CI `--check` mode would have failed otherwise per the gate-discipline rule).
- [`README.md`](README.md): library version bumped `2026.06.1` to `2026.06.2`; README version bumped `1.7.139` to `1.7.140`; date updated `2026-06-01` to `2026-06-02` (calendar rolled over).

### Why this is mechanical, not a content review

A 54-file content re-read is impractical in a single phase. Per the [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md) rule, the verification scope is stated explicitly: this PR is a ratification signal, not a quality review. The version bump asserts "the maintainer considers these documents ready for downstream use as of `2026-06-02`"; it does not assert "every line has been re-read and verified." Subsequent reviews on each document's own review cadence (per [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md)) provide the per-document content audit.

### Phased rollout context

This is Phase 0 of 8 in the mobile-app security work. Phases 1-7 follow:
1. Mobile standard expansion (App Attest, hybrid frameworks, IAP receipt validation).
2-7. Per-language pack rule files: Swift, Kotlin, React Native, Flutter, .NET MAUI, Capacitor/Ionic.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The version-monotonicity audit (gate 13) confirms all 54 per-document bumps are increases (`0.0.1 < 1.0.1`). The version-date consistency audit (gate 29, shipped yesterday) confirms today's library version `2026.06.2` matches today's calendar month `2026-06`. The two generator-drift gates (30, 31) pass after regenerating [`taxonomy.yml`](taxonomy.yml) and the portal artefacts in this commit. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.06.1

Make the project's strict-mode stance on exceptions explicit in [`.claude/CLAUDE.md`](.claude/CLAUDE.md), and document the `refs/preservation/` convention for the rare case of a legitimate protected-branch force-push. Both additions close gaps identified by the new pack governance rules: three pack rules reference a project "exception register" that this project does not maintain (the absence was implicit; now it is explicit), and one pack rule names the `refs/preservation/` namespace as the audit-trail convention for force-push exceptions (the convention is now documented so it can be followed without invention).

### Changed

- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) `## Boundaries` section gains two new bullets:
  - The first bullet makes explicit that this project offers no exception path for the audit gates or the pack rules under [`.claude/rules/governance/`](.claude/rules/governance/). The three pack rules that reference "the project's exception register" as an opt-out channel ([`gate-discipline`](.claude/rules/governance/gate-discipline.md), [`change-tracking`](.claude/rules/governance/change-tracking.md), [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md)) find no such register; the strict-mode default each pack rule's exception section falls back to is the project's stance. This restates the absence so it is read as policy rather than oversight.
  - The second bullet documents the `refs/preservation/<short-reason>-<YYYY-MM-DD>/<original-ref-name>` namespace and the protected-branch force-push procedure from [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md): document the technical reason, obtain governance-authority approval, notify collaborators, preserve the pre-rewrite ref, re-run the version-monotonicity audit. Costs nothing while not invoked; expensive to invent under pressure.
- [`README.md`](README.md): library version bumped `2026.06.0` to `2026.06.1` (same calendar month, patch counter increments per [`specification-master-project.md`](specification-master-project.md) section 4.5). README version bumped `1.7.138` to `1.7.139`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The new bullets in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) reside in the exempt `.claude/` subtree (per the `DEFAULT_EXEMPT_DIRS` constant in [`tools/lint_common.py`](tools/lint_common.py)), so the corpus linters do not scan them, but I re-read the two bullets in full to confirm they consistently describe what the pack rules say. The new gate 29 (Version-date consistency audit) passes: the bumped version `2026.06.1` matches today's date `2026-06-01` and the [`README.md`](README.md) field matches this CHANGELOG entry. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff). No infrastructure changes (no gate added, no rule file added); this is a pure governance-stance documentation change.

---

## 2026-06-01, Library Version 2026.06.0

Add a mechanical version-date consistency gate; bump to `2026.06.0` per [`specification-master-project.md`](specification-master-project.md) section 4.5; record the six-phase month discontinuity inherited from prior PRs.

### Added

- New gate 29: **Version-date consistency audit** ([`tools/lint-version-date-consistency.py`](tools/lint-version-date-consistency.py)) and its regression fixtures in [`tests/test_linters.py`](tests/test_linters.py). The gate enforces two invariants: (1) the most recent CHANGELOG section heading's date `YYYY-MM` must equal its `Library Version` `YYYY.MM`; (2) the [`README.md`](README.md) `**Library Version:**` field must equal the most recent CHANGELOG heading's version. The two CHANGELOG and README values are textually adjacent (same headings, same metadata block), so the comparison is purely lexical: no git plumbing, no commit-timestamp parsing, no CI-clock-vs-author-clock concerns.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6 inventory table: the new gate is inserted at position 29; the four gates previously at positions 29-32 (Machine-readable taxonomy in sync, Adopter portal and maturity scorecard in sync, Gate-name parity audit, Linter regression test suite) are renumbered to 30-33. Narrative text and the cross-references in sections 2 and 6.1 updated to reflect the new numbering.
- All four audit-programme surfaces ([`.github/workflows/quality.yml`](.github/workflows/quality.yml), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`.pre-commit-config.yaml`](.pre-commit-config.yaml), and the spec inventory above) gain the new gate in the same ordered position, so the gate-name parity audit (now gate 32) remains clean.
- Inline `gate-32` regression-test-suite references in [`tools/lint-acronym-consistency.py`](tools/lint-acronym-consistency.py), [`tools/lint-citation-verification-freshness.py`](tools/lint-citation-verification-freshness.py), [`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py), [`tools/lint-roles.py`](tools/lint-roles.py), [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py), [`tools/lint-structure.py`](tools/lint-structure.py), [`tools/lint-tooling-provenance-freshness.py`](tools/lint-tooling-provenance-freshness.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/run-linter-regression.py`](tools/run-linter-regression.py), and [`tests/README.md`](tests/README.md) updated to `gate-33` to track the regression suite's new position.
- Gate-count references "32 gates / 32-gate" updated to "33 gates / 33-gate" in [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md), and the runner header in [`tools/run_all_audits.sh`](tools/run_all_audits.sh).
- [`README.md`](README.md): library version bumped `2026.05.144` to `2026.06.0` (the calendar-month component now matches today's date per [`specification-master-project.md`](specification-master-project.md) section 4.5; the patch counter resets to 0 because the month rolled over). README version bumped `1.7.137` to `1.7.138`.

### Corrective note: six-phase month discontinuity

The six phases of the dev-security pack scope expansion that landed on 2026-06-01 (library versions `2026.05.139` through `2026.05.144`, see the entries below this one in this file) all used the `2026.05.x` patch lineage, inherited from the prior PR's `2026.05.138` baseline. The [`specification-master-project.md`](specification-master-project.md) section 4.5 CalVer rule is that `YYYY.MM` is the year and month of the *merge to `main`*, with the patch counter resetting to 0 when the month rolls over. All six merges occurred on 2026-06-01 and should have started at `2026.06.0` and counted up. The existing version-monotonicity audit (gate 13) treats `2026.05.x` as monotonic (tuple comparison: `(2026, 5, 144) < (2026, 6, 0)`) and did not catch the month mismatch.

Per the [`artefact-and-branch-discipline`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) rule shipped in Phase 6 (no force-push to protected branches), the six historical entries are not rewritten. Each entry's `Date:` field already records the correct calendar date (2026-06-01), so a reader cross-referencing the section heading can see what actually happened. From this entry forward the project follows section 4.5 strictly, and the new gate 29 enforces it mechanically.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The new gate, run standalone on the current working tree, transitions from `FAIL` (against the pre-bump README + CHANGELOG state) to `PASS` (against the bumped state in this PR). The two new regression tests in [`tests/test_linters.py`](tests/test_linters.py) (`test_date_version_month_mismatch_flagged`, `test_readme_changelog_version_drift_flagged`) pass under `python3 -m unittest tests.test_linters.VersionDateConsistencyTests`. The gate-name parity audit (now gate 32) confirms the four surfaces all declare the new gate at the same ordered position. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.144

Phase 6 (final) of the dev-security pack scope expansion: fifth and last governance rule lands; the phased rollout announced at pack version 1.6.0 is complete.

### Added

- [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) — new pack rule codifying two related disciplines that protect a project's audit trail: (1) generated artefacts are read-only (never hand-edit; always regenerate from the source; commit source plus generated output together; CI verifies via `--check` mode); (2) protected branches are append-only (no direct push; no force-push; PR-only merges). The rule defines what counts as a generated artefact (build outputs, schema dumps, taxonomies, doc portals, lockfiles, generated tests), what counts as a protected branch (default branch, release branches, long-lived integration branches), the required workflows for each, prohibited anti-patterns (hand-editing generated files to skip a regeneration round-trip, regenerating in CI to bypass the drift check, stripping `--check` jobs, direct push to protected branches, force-push that drops version-bearing commits, merging without going through the PR mechanism), the version-monotonicity contract that binds branch protection as the primary defence and the version-monotonicity audit as the backstop, tool-specific guidance (CI invocation patterns, branch-protection settings checklist, lockfile updates, long-lived integration branches), exception-handling protocols for both generated-artefact and branch-protection exceptions (governance-authority approval, tracked-issue link, preservation of pre-rewrite refs under `refs/preservation/`, post-rewrite re-audit), and framework alignment (NIST SSDF PO.5/PW.4/PS.1/RV.1; CSA CCM CCC-01-04/AIS-04/LOG-02/LOG-08; ISO 27001 A.5.4/A.8.15/A.8.32; SLSA Level 2-3). Pack-distributable form of this project's `## Boundaries` rules on generated files and direct pushes to `main`; generalises into a project-agnostic discipline.
- [`.claude/rules/governance/artefact-and-branch-discipline.md`](.claude/rules/governance/artefact-and-branch-discipline.md) — project consumption copy.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.11.0. "Pack scope" section reflects rollout completion (all five governance rules shipped); directory-structure ASCII tree shows the five-rule governance subdirectory marked as "rollout complete"; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fifth bullet for the artefact-and-branch-discipline rule. Closing paragraph updated to announce rollout completion.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/artefact-and-branch-discipline.md bullet; pack-version paragraph updated from 1.10.0 to 1.11.0 and notes the phased rollout is complete with the five governance rules shipped. The new rule explicitly cross-references this project's `## Boundaries` rules on generated files ([`taxonomy.yml`](taxonomy.yml), the `docs/` portal, scorecards) and on direct pushes to `main` as the source material.
- [`README.md`](README.md): library version bumped 2026.05.143 to 2026.05.144; README version bumped 1.7.136 to 1.7.137.

### Phased rollout context

This is Phase 6 of 6, the final phase. With this release the phased governance rollout announced at pack version 1.6.0 is complete: gate-discipline (1.7.0), change-tracking (1.8.0), evidence-grounded-completion (1.9.0), clarify-before-acting (1.10.0), and artefact-and-branch-discipline (1.11.0). Future pack work may add rules under `governance/` as the discipline expands, but the planned set is shipped.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file with zero findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff). The version-monotonicity audit confirms the library version sequence 2026.05.139 through 2026.05.144 across the six phases is strictly monotonic.

---

## 2026-06-01, Library Version 2026.05.143

Phase 5 of the dev-security pack scope expansion: fourth governance rule lands.

### Added

- [`dev-security/claude-rules/governance/clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md) — new pack rule codifying "when a request has more than one reasonable interpretation, or an external value the request does not pin down is required to proceed, surface the ambiguity in one sentence and ask before acting." The rule defines five ambiguity-detection categories (multi-interpretation requests, missing external values, project-convention choices, trade-offs, unclear world state), distinguishes when to ask versus when to use sensible defaults (ask when a wrong choice produces unwindable work or has consequences beyond this PR; default when a convention exists and the wrong-guess cost is bounded), specifies how to ask (one sentence, named alternatives, recommended option labelled and listed first, consequence stated), enumerates prohibited anti-patterns (silently picking, asking after acting, asking trivia, hiding ambiguity in narration, treating prior authorisation as durable when scope changed, leading-recommendation theatre, questions that require scrolling), gives tool-specific guidance for AI coding assistants (structured-question primitives, plan mode, investigation-first when state is unclear, scope-creep surfacing), enumerates exception cases (pre-authorised durable instructions like a project CLAUDE.md memory file, emergency response, reversible exploration), and provides framework alignment (NIST SSDF PO.1/PO.5/RV.1/RV.2, CSA CCM GRC-01/GRC-04/IAM-09/TVM-01/CCC-01-03, ISO 27001 A.5.1/A.5.4/A.5.15/A.5.18/A.5.27/A.8.16/A.8.32). Pack-distributable form of this project's `## Behavioral rule: clarify before acting` section; generalises that rule into a project-agnostic discipline.
- [`.claude/rules/governance/clarify-before-acting.md`](.claude/rules/governance/clarify-before-acting.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.10.0. "Pack scope" section now lists four shipped governance rules with their pack-version timing and names the final rollout rule (artefact-and-branch discipline) as the next phase. Directory-structure ASCII tree shows all four populated; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fourth bullet for the clarify-before-acting rule.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/clarify-before-acting.md bullet; pack-version paragraph updated from 1.9.0 to 1.10.0 and lists all four shipped governance rules. The new rule explicitly cross-references this project's `## Behavioral rule: clarify before acting` section as the source.
- [`README.md`](README.md): library version bumped 2026.05.142 to 2026.05.143; README version bumped 1.7.135 to 1.7.136.

### Phased rollout context

This is Phase 5 of 6. The final phase will add artefact-and-branch discipline (the unifying rule covering "never hand-edit generated artefacts; never push directly to protected branches; respect version-monotonicity"), completing the planned governance overlay.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file; one finding ("optimise" -> "optimize") fixed before the audit sweep. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.142

Phase 4 of the dev-security pack scope expansion: third governance rule lands.

### Added

- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) — new pack rule codifying "never declare work done, fixed, ready, shipped, or any synonym without evidence." The rule defines what counts as a completion claim (state assertions a reader will rely on, including "good catch" used to acknowledge a user-reported issue), enumerates the synonym vocabulary that triggers the protocol, specifies the six-step verification protocol (enumerate files in scope, re-read each in full, quote supporting lines with path-and-line-number citations, proactively search for contradictions, distinguish mechanical gate verification from semantic verification, state unverified items explicitly), enumerates prohibited anti-patterns (declaring victory in the response that carries failing evidence, treating user silence as confirmation, relying on prior runs, premature "good catch", pipe-masked exit codes, conflating "I edited the file" with "the file is correct"), gives tool-specific guidance for AI coding assistants (reading tool results before composing summaries, waiting for async work, `set -o pipefail` and `${PIPESTATUS[@]}` for pipe-masked exit codes, stop hooks, self-honesty in summaries), the exception-handling protocol for impractical re-reads, and framework alignment (NIST SSDF RV.1/RV.2/PO.5/PS.1, CSA CCM GRC-04/GRC-05/LOG-02/LOG-08, ISO 27001 A.5.4/A.5.36/A.8.15, OWASP ASVS V1.1/V14.1). Pack-distributable form of the user-level Rule 6 added 2026-05-31 in the maintainer's private global Claude Code memory file; generalises that rule into a portable, project-agnostic discipline.
- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.9.0. "Pack scope" section now lists three shipped governance rules with their pack-version timing; directory-structure ASCII tree shows all three populated; "Rule files and their scope" table gains a new row. The scope-bullet contract description rephrased from "agent-collaboration discipline" to its two component rules (evidence-grounded completion and clarify-before-acting) so the broadened contract is concretely visible.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a third bullet for the evidence-grounded-completion rule with a one-line summary of the six-step protocol. Downstream adopters who drag the payload now inherit all three governance rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/evidence-grounded-completion.md bullet; pack-version paragraph updated from 1.8.0 to 1.9.0 and lists all three shipped governance rules. The project's user-level Rules 1-5 (verification before dependent actions, tool-result authority, async waiting, pre-commit-hook respect, self-honesty) and Rule 6 (the evidence-grounded completion rule itself) are referenced as the pre-existing per-user discipline that this pack rule now codifies for cross-project adoption.
- [`README.md`](README.md): library version bumped 2026.05.141 to 2026.05.142; README version bumped 1.7.134 to 1.7.135.

### Phased rollout context

This is Phase 4 of 6. Phases 5 through 6 will add: clarify-before-acting discipline, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). Searched the new file for the synonym vocabulary the rule itself defines (`done`, `complete`, `fixed`, etc.) and confirmed all occurrences are either in the rule's own enumeration of trigger words or in prose that names the failure mode rather than claiming the rule's own work is done; the rule does not falsify itself. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.141

Phase 3 of the dev-security pack scope expansion: second governance rule lands.

### Added

- [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) — new pack rule codifying "every change to user-visible content carries a CHANGELOG entry by default." The rule specifies what an entry must contain (date and version header, structured sections following Keep a Changelog, linked file references, the "why" not only the "what", verification evidence, phase context for multi-PR rollouts), the sanctioned opt-out path (a `Changelog: skip (reason: ...)` trailer in the commit or PR description, reviewer-approved), prohibited anti-patterns (silent changes, vague entries, batched-up entries, retroactive entries, entries with unlinked file references, misclassified breaking changes, verbatim commit-message copy, gate bypass via `--no-verify`), the three mechanical CI gates that enforce the discipline (delta gate, link-coverage gate, version-monotonicity gate), tool-specific guidance (git trailers, monorepo coordination, generated CHANGELOGs, document corpora), an exception-handling protocol consistent with the gate-discipline rule, and framework alignment (NIST SSDF PO.5/PS.1/RV.1/RV.2, CSA CCM CCC-01-04/LOG-02/LOG-08, ISO 27001 A.5.4/A.8.15/A.8.27/A.8.32). Generalises this project's D1 CHANGELOG-on-PR delta gate, the CHANGELOG link-coverage audit, and the version-monotonicity audit into a portable, pack-distributable discipline applicable to any project with a CHANGELOG.
- [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.8.0. "Pack scope" section updated to list both shipped governance rules with their pack-version timing. Directory-structure ASCII tree shows the change-tracking rule populated alongside gate-discipline. "Rule files and their scope" table gains a new row for the change-tracking rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a second bullet for the change-tracking rule with a one-line summary of its contract. Downstream adopters who drag the payload now inherit both governance rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list adds the new governance/change-tracking.md bullet; pack-version paragraph updated from 1.7.0 to 1.8.0 and notes the second governance rule.
- [`README.md`](README.md): library version bumped 2026.05.140 to 2026.05.141; README version bumped 1.7.133 to 1.7.134.

### Phased rollout context

This is Phase 3 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract; Phase 2 (Library 2026.05.140) shipped gate-discipline. Phases 4 through 6 will add: evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives under `dev-security/claude-rules/governance/` and is scanned by [`tools/lint-language.py`](tools/lint-language.py); ran the linter standalone on the file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The project consumption copy lives in the exempt `.claude/` subtree. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.140

Phase 2 of the dev-security pack scope expansion: first governance rule lands.

### Added

- [`dev-security/claude-rules/governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md) — new pack rule codifying "never weaken or delete a gate to silence a failure; fix the artefact." The rule enumerates prohibited responses to a failing gate (`--no-verify`, severity-threshold lowering, exemption-list dumping, blanket suppressions, assertion-to-logging downgrades, marking real gates non-required, exit-code swallowing, flake-normalisation), correct responses in order of preference (fix the artefact; fix the gate if it is wrong; documented temporary exception; environmental re-run), tool-specific anti-patterns (git, lint, type-check, tests, CI/CD config, generator-output drift), an exception-handling protocol that the rule is consistent with, and framework alignment (OWASP ASVS, NIST SSDF, CSA CCM, ISO 27001). Generalises the project's `## Boundaries` rule ("Never weaken or delete an audit gate to make a document pass; fix the document") into a portable, pack-distributable form applicable to any project with CI gates, audit programmes, or branch protections.
- [`.claude/rules/governance/gate-discipline.md`](.claude/rules/governance/gate-discipline.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.7.0. "Pack scope" section updated from "will live under" to "lives under" the `governance/` subdirectory; explicit reference to the first landed rule. Directory-structure ASCII tree now shows the gate-discipline rule populated. "Rule files and their scope" table gains a new row for the gate-discipline rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) gains a new "## Development-governance discipline" section before "## Framework basis" referencing the new rule. Downstream adopters who drag the pack drop-in payload into their project now inherit the gate-discipline rule alongside the existing security rules.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (project): rule-file list gains the new governance/gate-discipline.md bullet; preamble paragraph updated from "pack version 1.6.0 announces" to "pack version 1.7.0 covers ... 1.7.0 delivered the first governance rule." Subsequent governance rules to be listed as they land.
- [`README.md`](README.md): library version bumped 2026.05.139 to 2026.05.140; README version bumped 1.7.132 to 1.7.133.

### Phased rollout context

This is Phase 2 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract. Phases 3 through 6 will add: change-tracking discipline, evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives in the exempt `dev-security/claude-rules/` subtree and is not subject to corpus linters; the project consumption copy lives in the exempt `.claude/` subtree and is likewise not subject to corpus linters. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.139

Phase 1 of the dev-security pack scope expansion: announce broadened contract from security-only to security + development-governance discipline.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.6.0 (2026-06-01). The opening "What are these files?" section now describes the pack as carrying "security and development-governance context" rather than security context alone. A new "Pack scope" section near the top of the README articulates the two scope families (security/compliance under `core/`, `ai/`, `pipeline/`, `languages/`; development-governance discipline under a new `governance/` subdirectory) and the reason the pack directory name remains `dev-security/` (developer discoverability — developers shop for "security rules," not for "GRC rules" or "development discipline"). The directory-structure ASCII tree now includes the `governance/` subdirectory as an announced-but-unpopulated entry; the tree is the directory layout contract for the phased rollout.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) `## Security requirements` heading renamed to `## Security and governance requirements`; a new paragraph below the existing rule-file bullets announces the pack's broader contract and clarifies that this project's loaded rules are unchanged in Phase 1 (this project's own governance discipline is already encoded in the existing `## Boundaries` and `## Behavioral rule` sections plus the 32-gate audit programme).

### Phased rollout context

This is the first of a six-phase rollout that broadens the [`dev-security/claude-rules/`](dev-security/claude-rules/README.md) pack from security-only to security + development-governance discipline:

1. **Phase 1 (this release).** Announce the broadened contract; introduce the governance subdirectory in the documented layout. No new rule files.
2. **Phase 2.** Add a gate-discipline rule that codifies "never weaken or delete a gate to silence a failure; fix the artefact" as a portable pack rule.
3. **Phase 3.** Add a change-tracking discipline rule that codifies the CHANGELOG-on-PR pattern with opt-out trailers, citing the D1 delta gate shipped in Library 2026.05.138.
4. **Phase 4.** Add an evidence-grounded-completion rule that lifts the user-level Rule 6 ("completion claims require evidence-grounded verification") into a portable, shareable rule.
5. **Phase 5.** Add a clarify-before-acting rule that lifts the Karpathy-adapted rule from this project's [`.claude/CLAUDE.md`](.claude/CLAUDE.md) into a portable pack file.
6. **Phase 6.** Add an artefact-and-branch-discipline rule that bundles no-hand-editing-generated-artefacts, no-direct-push-to-protected-branches, and the version-monotonicity contract.

Each phase is shipped as its own pull request with its own CHANGELOG entry and library version bump. Per-PR cycle cost is accepted as the price of better per-rule reviewability and assurance.

### Verification

Full 32-gate audit programme passes standalone immediately before commit; new D1 CHANGELOG-on-PR delta gate (Library 2026.05.138) passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.138

CHANGELOG enforcement gate and prior-PR catch-up entry.

### Added

- New CI-only delta gate **D1: CHANGELOG-on-PR check** ([`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py)) that fails a pull request when the diff against the merge-base with the target branch does not include [`CHANGELOG.md`](CHANGELOG.md). An opt-out trailer `Changelog: <one-line-reason>` in any commit message body in the PR range satisfies the gate. The gate runs only on `pull_request` events in [`.github/workflows/quality.yml`](.github/workflows/quality.yml); it is not part of the 32-gate corpus audit programme and is exempt from gate 31's name-parity audit because its inputs (git history range, PR base ref) are unavailable in [`tools/run_all_audits.sh`](tools/run_all_audits.sh) and [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml) checkout step now uses `fetch-depth: 0` so the delta gate can resolve the merge-base.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6.1 documents the new PR-only delta gate category and the opt-out trailer convention.

### Changed

- Catch-up entry for prior PR #5 ([`d1fb4d0`](https://github.com/jposluns/grc_library/commit/d1fb4d0)): added a "Behavioral rule: clarify before acting" section to [`.claude/CLAUDE.md`](.claude/CLAUDE.md), adapted from [Karpathy's "Think Before Coding" CLAUDE.md rule](https://github.com/multica-ai/andrej-karpathy-skills) (MIT-licensed). The rule was merged without a CHANGELOG entry; this entry records it retroactively. The new D1 gate above prevents this miss from recurring.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green. The new D1 gate is exercised by this PR itself: this PR modifies [`CHANGELOG.md`](CHANGELOG.md), so D1 passes; if it had not, D1 would have blocked merge.

---

## 2026-05-31, Library Version 2026.05.137

Corpus-wide hyperlink sweep and TODO.md cleanup.

### Changed

- Converted 414 unlinked backtick-wrapped file references to markdown links across 48 files (root specs, governance, compliance, security, privacy, resilience, operations, supply-chain, dev-security, ai, docs, tools). Detection extends the existing [`tools/lint-changelog-link-coverage.py`](tools/lint-changelog-link-coverage.py) regex across every markdown file. Resolution order: relative to source dir, relative to repo root, tail-path match, then unique-basename fallback. Adopter-project filenames (Claude rule files, AGENTS files, package manifests), placeholder patterns containing angle brackets / braces / wildcards, command-line invocations, and references to deleted or external-project files are intentionally left as code-formatted text. 43 residual code-formatted references remain by design.
- Removed stale CC0-era artefacts from [`TODO.md`](TODO.md): P1/P2/P3 placeholder sections (phase references no longer mapped to the public-release history), P6.2 OT/ICS (verifiably complete in [`operations/ot/`](operations/ot/)), and phase-number prefixes on Decisions log entries. Rephrased P6.1 to focus on the remaining multi-cloud governance gap (per-cloud baselines already shipped in [`dev-security/`](dev-security/)). Nuanced P5.7 (Saudi Arabia annex exists; Argentina/Mexico in the Latin America annex) and P5.8 (US/China AI rules already partially covered in the respective privacy annexes).

### Fixed

- One-line content-generation typo in [`tools/README.md`](tools/README.md) introduced by an earlier direct-to-main MCP push: line 28 `# restrict scope to specific paths` corrected to `# regen-and-check`.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.

---

## Initial public release (2026-05-31, Library Version 2026.05.136): CC BY-SA 4.0

First public commit of the Governance, Risk, and Compliance Documentation Library, published under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). See [`LICENSE`](LICENSE) for the full legal code and [`NOTICE.md`](NOTICE.md) for the repository's external-reference boundary.

### Acknowledgements

The substance of this library draws on knowledge, experience, war stories, and patient mentorship accumulated over more than two decades by a community of GRC and security practitioners, with roots going back to the early 2000s. See [`AUTHORS.md`](AUTHORS.md) for the acknowledged contributors and the maintainer's attribution preference.

Corrections, contributions, and additional acknowledgements are welcomed via the workflow in [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.
