# Reference-version currency and missing references (reference)

**Read this when an externally-versioned reference (a standard, framework, or dataset) becomes
load-bearing for a task, like a skill.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries the
lean always-on core (the `_ref`-required fail-loud principle, the "consult the index, verify
upstream this turn, act only after both" gist, the superseded-version prohibition, and the
acquire-or-pause rule for a not-held reference); this file carries the full detail and rationale.
Relocated from CLAUDE.md by roadmap C part 2 (the activity-scoped rule loader); the always-on
residue kept inline in CLAUDE.md is deliberate defence-in-depth and is not a duplication to trim.

This is the project-specific operationalization of the `evidence-grounded-completion` rule's
external-version-currency corollary, for the `grc_library_ref` reference base.

## The `_ref`-required loud gate (full mechanism)

`_ref` is a REQUIRED maintainer-orchestrator dependency; its absence fails LOUD (§1.19.7
`_ref`-required gate). Reference-checking against the held ground truth is critical to content
correctness, so for the maintainer a missing `grc_library_ref` is a broken setup to FIX, never a
state to silently work around. `/resume` step 3 acts on `detect-env`'s `ref_availability` decision:
on `maintainer` identity with `_ref` NOT readable it HALTs and surfaces the `--add-dir` fix, and no
reference-dependent (content) work proceeds until access is granted and the session re-resumed. The
sibling-reaching tools' graceful degradation (`lint_common.resolve_sibling` no-op, §1.19.2) is
ADOPTER-ONLY: an adopter legitimately has no `_ref` (the committed reference-acquisition manifest +
`/adopt` `.ref` bootstrap cover it), so graceful there is correct, whereas for the maintainer it
would mask the missing dependency. (There is no `_ref`-specific PreToolUse hook; the mechanical
enforcement is `detect-env`'s `ref_availability` HALT plus `/resume` step 3 acting on it.)

## The check order, whenever an externally-versioned reference (a standard, framework, or dataset such as MITRE ATT&CK / ATLAS, ISO, CSA, NIST) is load-bearing for a task

1. **Find what `grc_library_ref` holds, via its index, not a guess.** Consult the `grc_library_ref`
   reference index ([`grc_library_ref/INDEX.md`](../../grc_library_ref/INDEX.md),
   `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`,
   `grc_library_ref/COVERAGE-MAP.md`) to find the held artefact and its recorded version. (MITRE
   lives under `grc_library_ref/frameworks/`, not `grc_library_ref/standards/`.) **A held /
   not-held claim is EXECUTED, not narrated:** run `python3 tools/ref-holds.py <query>` and quote
   its output (HELD with the path, or NOT-FOUND-IN-INDEX), never a partial filename grep. A `grep`
   may FIND a file, but its ABSENCE from a partial/filtered grep never proves not-held. This is the
   same executed-not-narrated forcing function as `audit-delivery-status.py` for delivery-status
   claims, and the `evidence-grounded-completion` "inventory/absence claims require the index, not a
   partial look" corollary.
2. **Validate the current version upstream this turn.** The authoritative answer to "is this
   current?" is the upstream / primary source (the vendor's releases page or repository), never the
   `grc_library_ref` copy, a stored note, or memory. `grc_library_ref` is believed-current STORAGE,
   not a version authority.
3. **Act only after both.**

## On discovering upstream is newer than `grc_library_ref` holds (the version-update SOP)

- Updating `grc_library_ref` is part of SOP, via the superseded-archival workflow (download the new
  version into `grc_library_ref`; keep the old but move its files, extracted text plus original,
  into `grc_library_ref`'s retained-version store `grc_library_ref/.superseded/` (bucket-mirrored
  layout and `REGISTER.md` per `grc_library_ref` `CONTRIBUTING.md`); update `catalogue.yml` and the
  index docs).
- **If the update needs a license or a maintainer download** (cannot be auto-fetched, or egress is
  blocked), **pause and ask the maintainer.** On no response, apply the graceful-degradation
  default: defer the current item and move on to the next independent item (record it in
  `grc_library_private/.working/pending-decisions.md`).
- **Never write or rely on a superseded version unless the maintainer explicitly authorizes**
  working from the older one. A register row, a citation, or a mapping must carry the
  upstream-confirmed current version, or the item waits.

## Missing-reference-document SOP (maintainer-directed 2026-07-12)

When a task needs a load-bearing reference (a standard, regulation, RTS/ITS, framework, or dataset a
citation or attributed value depends on) that `grc_library_ref` does not hold, follow the pack's
missing-load-bearing-reference corollary in
[`evidence-grounded-completion`](../.claude/rules/governance/evidence-grounded-completion.md) (its
`## Un-observable state, inventory, and external-version currency` section; TODO 3.53): PAUSE,
attempt acquisition, then named options on failure. The project instantiation:

1. **Attempt the ingest into `grc_library_ref`** (drop in `ingest/`, dedupe, identify, route to the
   right bucket, extract to `--full-text.md`, catalogue in `catalogue.yml`, regenerate the indexes,
   run the ref gate), then continue against the now-held source. The `grc_library_ref` write is a
   cross-repo PR (writes to the sibling `grc_library_ref` repo go through its own PR, not a direct push).
2. **On acquisition failure** (egress-blocked, licensed/paywalled): the unattended DEFAULT is
   defer-and-skip via the roughly-2-minute graceful-degradation timer, recording the deferral in
   `grc_library_private/.working/pending-decisions.md` as deferred-blocked, routing around to the
   next independent item, and holding anything that depends on it. Attended, surface named options:
   the maintainer downloads or provides the document (the usual resolution when licensed or
   egress-blocked); defer; or reword so the artefact does not depend on it, or cite
   corroboratively-only with an accepted-unverified tracker.

Routing a `source-not-held` finding without first attempting the download is the shortcut this
forecloses.
