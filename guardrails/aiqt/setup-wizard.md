# AIQT setup wizard

Version: 1.0.0 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 procedure; re-runnable; executed by the adopter's assistant. Writes
ONLY `.working/aiqt/config.md` (the user-owned file). It never writes into
`.working/aiqt/core/` (the updater's territory) and never touches a secret value.

On a re-run the wizard first shows the memory refresh: per enabled capability, what you
decided, when, why, and usage since (read from config.md). Then:

1. **Fast path.** "Use the recommended setup?" One confirmation sets: Level0 On, Level1
   Automatic at pre-push, Level2 Off (offered again when a key is loaded), AutoFix On,
   SpendNudge On. Before the confirmation the wizard states plainly: "Auto-fix is on by
   default: the first findings from a CI review may arrive already part-fixed by your
   assistant, capped at three tries before it asks you."
2. **Custom path.** One screen per capability: the two-to-three-sentence capability
   description, then the cost model at the point of choice (local review is
   plan-included; CI review is metered per run, with the spend nudge on by default).
3. **Key loading (the metered CI levels).** The wizard NEVER touches the key value. It
   prints the exact steps (repository Settings, Secrets and variables, Actions; or
   `gh secret set <name>`, using the secret name the CI integration kit defines) and
   then runs the doctor's exists-unread check to confirm placement without ever reading
   the value.
4. **Egress consent.** One prompt per origin actually contacted, recorded as ordinary
   `EgressConsent` settings in config.md: github.com (release and drift checks),
   aiqt.ai (the versioned `aiqt-X.Y.Z.zip` and the unversioned `aiqt.zip`, which is by
   contract byte-equal to the latest versioned one), cleanlanguage.ai
   (`cleanlanguage.zip`, always-latest by the same contract). Denied egress degrades
   gracefully: the bundled latest-known copy stands and the doctor notes its age.
5. **Exit.** Writes config.md (comment blocks regenerated; Decided-when/why stamped;
   hand-edited rows preserved), prints one line per capability, and points at the
   doctor for a health read.
