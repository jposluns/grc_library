# AIQT configuration format (`.working/aiqt/config.md`)

Version: 1.0.3 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 format; the setup wizard writes it, the doctor reads it, the updater
reads it and never writes it. Changes here are breaking for every consumer and follow
the AIQT release process.

One file records what you decided, when, why, and how you have used it. Every setting
is a comment block followed by one parseable line. Hand-editing is a first-class path:
the wizard re-reads and never clobbers a hand edit silently.

## 1. Where AIQT lives, and what may write where

The AIQT home in an adopter repository is `.working/aiqt/`:

- `.working/aiqt/config.md` is USER-OWNED. The wizard writes it with your answers; you
  may hand-edit it at any time; the updater never writes it.
- `.working/aiqt/core/` is the updater's SOLE write root: every AIQT-managed component
  the updater installs or refreshes lives under it, and nothing else does.

Stated plainly for security-minded adopters: automated AIQT writes are limited to the
`core/` directory by design. The boundary is one auditable rule (the updater refuses to
write outside `.working/aiqt/core/`), and the doctor's bounded-write-set check verifies
the resulting state, on the honest ladder its own text states: what it can prove today,
and the stronger scans it upgrades to as the component marker and managed-component
manifest ship. Your files, and your config, are structurally out of the updater's reach.

## 2. Grammar

- One setting per line: `Key=Value`, no spaces around `=`. `#` opens a trailing comment.
- A key is a Name optionally followed by ONE dot-qualifier, where a setting family has
  one entry per instance (egress consent is the Phase-1 case). The parse is
  deterministic: the FIRST dot separates the name from the qualifier, and every later
  dot belongs to the qualifier, which is how multi-dot hostnames parse. The qualifier
  is a lowercase hostname token (`a-z`, `0-9`, with internal dots and hyphens
  permitted; no spaces; lowered on parse). Exactly one qualifier level exists.
- A comment BLOCK precedes each setting, in the config file itself, with no exceptions:

    <!-- What: <one plain-language sentence>.
         Options: <closed set, each with a clause>.
         Default and why: <one sentence; cost note where the setting is metered>.
         Decided: <YYYY-MM-DD> via <wizard-fast-path | wizard-custom | hand-edit>. Why: <recorded reason>. -->
    SettingName=Value

- Tables use pipe rows. Unknown keys are PRESERVED by every tool (the doctor flags,
  never deletes).

## 3. Settings (the Phase-1 catalogue)

This section is a CATALOGUE of the Phase-1 settings, not config syntax: in the config
file itself, every one of these settings carries its own comment block per the grammar
above (the worked example below shows the literal form).

| Setting | Values | Default | Notes |
| --- | --- | --- | --- |
| `AIQTVersion` | release version | installed release | a snapshot manifest of component versions |
| `Level0` | `On` | `On` | built-in review conventions; always On while AIQT is installed |
| `Level1` | `Off`, `OnRequest`, `Automatic` | `Automatic` | local second opinion (the cross-family CLI); Automatic fires only at `Level1Steps` |
| `Level1Steps` | comma list of steps | `pre-push` | high-value steps only by default |
| `Level2` | `Off`, `On` | `Off` | per-change second opinion in CI (metered; the spend nudge applies) |
| `Level3` | `Off`, `On` | `Off` | organization-wide CI review (admin-loaded org secret) |
| `Level4` | `Unavailable` | `Unavailable` | a future capability; present so the ladder reads completely |
| `AutoFix` | `Off`, `On` | `On` | validate first, fix up to 3 tries, then a loud alert |
| `PromotionPanel` | `Off`, `On` | `Off` | full model panel at major and minor bumps (metered, rare by design) |
| `SpendNudge` | `Off`, `On` | `On` | remind the user to check metered spend when CI review runs |
| `EgressConsent.<origin>` | `granted`, `denied` | asked, never defaulted | ONE ORIGIN PER ENTRY; see below |

Egress consent entries are ordinary settings, ONE ORIGIN PER ENTRY, each with its own
comment block recording when and why it was granted or denied:

    EgressConsent.github.com=granted
    EgressConsent.aiqt.ai=granted
    EgressConsent.cleanlanguage.ai=denied

The tooling contacts an origin only while its entry reads `granted`; a denied origin
degrades gracefully (the bundled latest-known copy stands, and the doctor reports its
age instead of fetching). Consent is never written by default: the wizard asks per
origin, on the fast path too.

## 4. Guardrail table

One row per installed guardrail, vetted and local alike; BOTH kinds carry their own
version. Identity is SEQUENTIAL (`AIQT-000001` upward for vetted guardrails,
`LOCAL-000001` upward per project); an originating pull request, where one exists, is
CORRELATION METADATA in the Origin column and in the guardrail's own header, never the
identity, so adopters not hosted on GitHub are served identically.

    | Id | Version | AutoUpdate | UpdatePolicy | Origin |
    | AIQT-000001 | 2026.08.001 | Yes | auto | core |
    | AIQT-000124 | 2026.07.003 | No | pin@2026.07.003 | contributed, guardrails#456, was LOCAL-000012, @user |
    | LOCAL-000002 | 2026.08.001 | n/a | local | authored by this project's assistant, 2026-08-05 |

Semantics:

- `AutoUpdate=No` is SELF-SET only: the wizard never mass-disables; the user edits the
  row deliberately.
- `UpdatePolicy` is `auto | offer | pin@<ver> | skip`; LOCAL rows are never touched by
  the updater.
- Security advisories auto-apply by default. Where a row carries `AutoUpdate=No`, the
  runtime raises a LOUD alert naming the advisory and asking the user to change the
  override or investigate and fix themselves. Never a silent force-install.

## 5. Usage history (appended by the runtime, never the wizard)

    ## Usage
    | Date | Capability | Runs | Findings | Fixed | Metered cost note |

## 6. Worked example (abbreviated; every setting carries its block)

    <!-- What: local second opinion by the other model family.
         Options: Off (never), OnRequest (you ask), Automatic (fires at Level1Steps).
         Default and why: Automatic at pre-push; plan-included, catches what the author's family misses.
         Decided: 2026-08-09 via wizard-fast-path. Why: recommended setup accepted. -->
    Level1=Automatic

    <!-- What: which local steps fire the automatic second opinion.
         Options: any comma list of hook steps.
         Default and why: pre-push only; the highest-value step, no per-edit noise.
         Decided: 2026-08-09 via wizard-fast-path. Why: recommended setup accepted. -->
    Level1Steps=pre-push

    <!-- What: consent to contact github.com (release and drift checks).
         Options: granted (contact while granted), denied (bundled copy stands).
         Default and why: none; consent is asked per origin, never defaulted.
         Decided: 2026-08-09 via wizard-fast-path. Why: adopter granted at setup. -->
    EgressConsent.github.com=granted

    | Id | Version | AutoUpdate | UpdatePolicy | Origin |
    | AIQT-000001 | 2026.08.001 | Yes | auto | core |
    | LOCAL-000001 | 2026.08.001 | n/a | local | authored by this project's assistant, 2026-08-09 |

    ## Usage
    | Date | Capability | Runs | Findings | Fixed | Metered cost note |
    | 2026-08-09 | Level1 pre-push | 1 | 2 | 2 | none (plan-included) |
