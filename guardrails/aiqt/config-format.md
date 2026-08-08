# AIQT configuration format (`.working/aiqt/config.md`)

Version: 1.0.0 (plain semver; the AIQT release train assigns release versioning once it
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
write outside `.working/aiqt/core/`), and the doctor verifies the resulting state
mechanically (no AIQT-managed file outside `core/`; see the doctor's bounded-write-set
check). Your files, and your config, are structurally out of the updater's reach.

## 2. Grammar

- One setting per line: `Key=Value`, no spaces around `=`. `#` opens a trailing comment.
- A comment BLOCK precedes each setting:

    <!-- What: <one plain-language sentence>.
         Options: <closed set, each with a clause>.
         Default and why: <one sentence; cost note where the setting is metered>.
         Decided: <YYYY-MM-DD> via <wizard-fast-path | wizard-custom | hand-edit>. Why: <recorded reason>. -->
    SettingName=Value

- Tables use pipe rows. Unknown keys are PRESERVED by every tool (the doctor flags,
  never deletes).

## 3. Settings (Phase-1 set)

    AIQTVersion=1.0.1              # installed release (a snapshot manifest of component versions)
    Level0=On                      # built-in review conventions; always On while AIQT is installed
    Level1=Off|OnRequest|Automatic # local second opinion (the cross-family CLI); Automatic fires only at Level1Steps
    Level1Steps=pre-push           # comma list; high-value steps only by default
    Level2=Off|On                  # per-change second opinion in CI (metered; the spend nudge applies)
    Level3=Off|On                  # organization-wide CI review (admin-loaded org secret)
    Level4=Unavailable             # a future capability; present so the ladder reads completely
    AutoFix=On                     # validate first, fix up to 3 tries, then a loud alert
    PromotionPanel=Off|On          # full model panel at major/minor bumps (metered, rare by design)
    SpendNudge=On                  # remind the user to check metered spend when CI review runs
    EgressConsent=github.com:granted,aiqt.ai:granted,cleanlanguage.ai:granted

Egress consent lines are ordinary settings: one origin per entry, `granted` or
`denied`, recorded with the same comment-block provenance as every other setting. The
tooling contacts an origin only while its entry reads `granted`; a denied origin
degrades gracefully (the bundled latest-known copy stands, and the doctor reports its
age instead of fetching).

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

## 6. Worked example (abbreviated)

    <!-- What: local second opinion by the other model family.
         Options: Off (never), OnRequest (you ask), Automatic (fires at Level1Steps).
         Default and why: Automatic at pre-push; plan-included, catches what the author's family misses.
         Decided: 2026-08-09 via wizard-fast-path. Why: recommended setup accepted. -->
    Level1=Automatic
    Level1Steps=pre-push

    | Id | Version | AutoUpdate | UpdatePolicy | Origin |
    | AIQT-000001 | 2026.08.001 | Yes | auto | core |
    | LOCAL-000001 | 2026.08.001 | n/a | local | authored by this project's assistant, 2026-08-09 |

    ## Usage
    | Date | Capability | Runs | Findings | Fixed | Metered cost note |
    | 2026-08-09 | Level1 pre-push | 1 | 2 | 2 | none (plan-included) |
