# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

**Worker-provenance convention (decided 2026-07-23, TODO 3.19):** a reference to a scratch-side worker result or manifest is written as plain backticked text in a `repo:path` form (naming the scratch repo and the result file), never a cross-repo markdown link. A cross-repo relative link target resolves only against a fresh sibling checkout at `main`, not a stale local tree, and cross-repo links are un-gate-checkable; the plain-text form keeps the provenance readable and grep-able without the fragility.

## 2026-07-27, Library Version 2026.07.700, PR #1210 (close TODO 3.120: gate 50 Check 1 third `pending` state)

Gate 50's QA-cadence parity Check 1 ([`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py)) was satisfied by a validate-pr row's PRESENCE, so an honest `DISPATCHED, RESULT PENDING` row read GREEN while that PR's `/validate-pr` had never actually run, the silence-reads-as-health shape that let validate-pr-1173 and validate-pr-1180 sit unconsumed across sessions (both since consumed at #1206). This closes the mechanical half of the pair whose convention half shipped in #1178 (CLAUDE.md close-out item 3 and the pack `session-lifecycle` rule, section 5), explicitly the weaker half until now. Sequencing constraint satisfied: #1176's own QA has returned and its row is resolved, so the gate lands green on the live ledger.

### Changed
- [`tools/lint-bookkeeping-parity.py`](../../tools/lint-bookkeeping-parity.py): a THIRD validate-pr row state, `pending`. `PENDING_FINDINGS` matches a `DISPATCHED` / `RESULT PENDING` / leading-`PENDING` Findings-cell marker and `RETURNED_MARK` matches `RETURNED`; `parse_validate_pr_status` classifies a row `pending` only when the pending marker is present AND `RETURNED` is absent, so a returned row that merely mentions the word "dispatched" in its prose is NOT pending (the reality fixture). `qa_cadence_findings` Check 1 flags a `pending` in-window PR (below the highest) as a stranded QA order, while the single highest PR stays in-flight-exempt (its QA batches into the not-yet-existent next PR, the same demotion trigger the highest-PR exemption already uses). The module docstring's Check 1 exemption list and the inline classifier comment document the third state.
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md): the §6 gate-50 detailed prose gains the `pending` third-state sentence (a new FAIL condition, not an exemption); Version 1.17.34 -> 1.17.35.

### Added
- [`tests/test_linters.py`](../../tests/test_linters.py) `BookkeepingParityTests`: three reality-fixture regressions, a pending in-window row FAILS Check 1 (stranded), a pending highest-PR row is in-flight-exempt, and the classifier treats a `RETURNED`-mentioning-`dispatched` row as `normal` (not `pending`). Class 35 -> 38.

### Verification
- Gate 50 rc=0 on the live ledger (all in-window validate-pr rows are RETURNED; no false positive), gate 64 detailed-prose presence rc=0, `BookkeepingParityTests` 38/38, language lint on the spec rc=0.
- The delivery tray (47 files) was reconciled against current HEAD via the worker tray-classification: every QA finding is consumed or routed to a tracked TODO; the tray is a filing backlog, not a QA backlog, so no undelivered QA finding blocks this change.
- #1209's post-merge validate-pr had no delivery artefact; with the worker fleet out (all six accounts, both families, every tier reporting no eligible capacity), it was self-run inline via an in-session subagent (mandatory-QA outranks mandatory-offload on this conflict), and its result is batched into this PR's validate-pr row.
- **Pre-push skeptical verifier (in-session, refute-briefed, active-QA-gate change): UPHELD.** All three intents verified true (highest-PR in-flight-exempt, RETURNED-not-pending, in-window-pending-FAILS), boundaries and arm-ordering correct, fixtures non-tautological. It surfaced four latent false-PASS (safe-direction) findings, none a defect in the added logic: three recall gaps ROUTED to new TODO 3.150 (recall brittleness, `NOT RUN` subsumption-arm collision, multi-row stale-overwrite), and finding #4, that PRs 1169-1172 and 1179 carry genuinely-unconsumed validate-pr rows aged below the gate's CHANGELOG-root window (real QA-cadence debt, substance largely covered but the formal per-PR validate-pr never returned), ROUTED to the next PR as a dedicated QA-catch-up.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

## 2026-07-27, Library Version 2026.07.699, PR #1209 (close TODO 3.126: open-findings disposition-token structural fix)

The [`.working/open-findings.md`](../open-findings.md) guard's Disposition cell was free prose the check could not reliably read: an earlier test only asked that the cell START with a terminal word, so `ROUTED nowhere yet, near 3.145`, a lone `FIXED`, and `FIXED in #1208` (a ref reachable only past prose) all passed while saying nothing checkable; and the #1208 defect showed a literal `|` in a Finding cell shifts the columns so a valid row is mis-read. This is a STRUCTURAL fix (validate-pr-1178 F-1: the input, not a third round of matcher hardening, was the problem), with two grammar decisions the maintainer made 2026-07-27 (recorded in the private design-decisions record).

### Changed
- [`.claude/hooks/block-on-open-findings.py`](../../.claude/hooks/block-on-open-findings.py): a disposition GRAMMAR (`disposition_valid`). `FIXED`/`ROUTED` must carry a ref (`#\d+`, a `\d+\.\d+[a-z]?` item, or a `TODO`-qualified item) ADJACENT to the terminal word, whitespace or markup only between, so a scanned-for-past-prose ref does not count. `REFUTED`/`ACCEPTED` machine-require only the terminal WORD and keep prose (per the ledger legend). `parse_open_rows` now splits on UNESCAPED pipes so a cell may carry `\|`, and a row whose column count is not five yields `disposition=None`, which `undispositioned` treats as a fail-closed block rather than mis-reading a middle fragment (the #1208 pipe defect). The in-file self-test grew 20 -> 31, including the #1208 pipe reality fixture and both grammar directions.
- [`.working/open-findings.md`](../open-findings.md): the legend documents the grammar; the 48 accumulated dispositioned rows in `## Open` were MOVED to `## Closed today` (the intended lifecycle, and Closed-today is not grammar-checked, an archive), leaving `## Open` holding only genuinely-open findings (now zero). The `FIXED in #N` rows were nudged to the adjacent `FIXED #N` form in the move.

### Verification
- The migration was a DETERMINISTIC script with a re-parse check, not a hand edit: 0 findings lost (every pre-migration Open finding present in the post-migration Open + newly-moved Closed-today), 0 undispositioned rows in Open, 55 well-formed 4-column Closed-today rows.
- Hook self-test 31/31; the full linter regression suite (which runs the hook's `--self-test`) rc=0; the live hook reports 0 undispositioned errors against the migrated ledger.
- **Dual-family adversarial verify** (this change is the PR-BLOCKING guard, so both the false-PASS and false-BLOCK directions were briefed): findings dispositioned before merge.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

## 2026-07-27, Library Version 2026.07.698, PR #1208 (close TODO 3.115: four gate-44 fail-open routes)

Closes four fail-open routes in gate 44's subsection-representation check (TODO 3.115). `content_tokens` strips non-prose so a token surviving only in metadata cannot falsely "represent" a skill subsection the paired command actually omits. The four routes were constructs that survived the strip set. All four fixes are PREVENTIVE (zero-verdict-change: no current PAIRS command file triggers any new strip, so the gate stays green and no live verdict moves).

### Changed
- [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py): four route fixes. (14) `strip_front_matter`, a block-scanning helper (not a regex) so a document OPENING with a `---` thematic break is not swallowed as front matter, which a naive `\A---.*?---` form would do; (15) `strip_metadata_table_cells`, which blanks only a leading-pipe row's cells whose whole content is one machine-identifier atom (a path or a three-plus-segment slug), so an inline pipe list in prose and a one-hyphen compound like `fan-out` stay prose (a PARTIAL close, residual stated in the docstring); (16) `LINK_TARGET_RE` and `IMAGE_RE` widened to balance one parenthesis level (one defect that sat in two patterns; a legacy fallback alternative is kept so the pattern never strips LESS than before); (17) a quote-aware `HTML_TAG_RE` anchored on `=`, so a quote counts as an attribute delimiter only when it opens a value (an apostrophe in prose near `<...>` is not eaten), again with a legacy fallback. Plus stale prefix-match docstring and comment cleanup: `token_present` already did exact matching at the parent, so the change corrects two surviving references to the removed shared-five-character-prefix rule.
- [`tests/test_linters.py`](../../tests/test_linters.py): four fixtures in `PairedSkillStepParityTests` (class 17 -> 21) plus the shared `SKILL_ONE_SUBSECTION` constant. Each fixture carries a positive leak assertion, an end-to-end `unrepresented_subsections` flag, and negative controls (the thematic break, the `fan-out` cell, the parenthetical after a link, the apostrophe near a placeholder).
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md): gate 44's §6 detailed narrative rewritten to a ten-item enumeration in the code's actual strip order, and two live textual defects fixed (a clause doubled in one sentence, and a `.,` typo), and the route-(b) enumeration item softened from "machine-identifier atom" to a shape-heuristic phrasing after the verify (below). `Version` 1.17.32 -> 1.17.34, `Date` to 2026-07-27.
- [`TODO.md`](../../TODO.md): §3.115 deleted; successor §3.148 opened for the two routes of the class still open (an indented code block; a semantic-metadata word-cell), carrying the "no completeness claim, ordinal only" instruction and a note on a pre-existing §5-grouped-summary accuracy gap left out of scope. [`.working/DONE.md`](../DONE.md): the 3.115 (#1208) closure entry.

### Verification
- **Deterministic apply**: the re-verified candidate diff (byte-identical base per the pre-apply re-verify) was applied via `git apply`, then re-parsed and mutation-checked at source. Each of the four fixes, when its strip is reverted in an imported copy, LEAKS the token, so the fixtures genuinely catch a regression (not tautological).
- Gate 44 green (13 pairs, zero-verdict-change); full linter regression suite `rc=0`; gates 64 (detailed-prose presence) and 77 (gate-name citation inventory) green after the spec edit.
- The reissued Claude re-verify also caught a PRE-EXISTING (not fix-introduced) test defect and it was fixed here: `PairedSkillStepParityTests` defined `test_runs_clean_on_corpus_at_head` twice, so Python kept the later (a mis-placed collection-enumeration smoke test) and the parity gate's own HEAD-smoke test never ran. The collection-enumeration method was renamed, restoring the parity smoke test (class 21 -> 22 tests).
- **Dual-family adversarial verify** (the sensitive active-QA-gate tier), and both families earned their cost by catching OVER-strips (false positives) the pre-apply re-verify had missed. The **Codex** verifier caught an ERROR: `SLUG_ONLY_CELL_RE`'s `\S*/\S*` branch treated an ordinary English slash-compound (`read/write`, `input/output`) in a table cell as a path and blanked it, so a command representing a `### Read Write` subsection via that cell would be wrongly flagged. Fixed pre-merge by requiring a path indicator on the slash branch, with a new negative-control fixture. The **Claude** verifier corroborated it and EXTENDED it to a latent WARN: the three-plus-segment branch is a shape heuristic that cannot distinguish a machine-id slug from a multi-segment English compound (`state-of-the-art`), so such a compound in a cell is a latent over-strip. Fixed by correcting the docstring and spec over-claim ("machine-identifier atom" softened to "identifier-shaped atom, a shape heuristic") and tracking the residual in TODO 3.148, since no reliable syntactic signal separates the two and it is latent (zero current PAIRS files carry such a cell, so the zero-verdict-change headline holds). Both findings are recorded in [`.working/open-findings.md`](../open-findings.md), FIXED in this PR.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

## 2026-07-27, Library Version 2026.07.697, PR #1207 (/sitrep planning refinement + #1206 QA batch)

Pure-bookkeeping PR. No corpus or code change.

### Changed
- [`TODO.md`](../../TODO.md): TODO 3.142 (the future `/sitrep` situation-report command) gains two refinements captured from prototyping its output when the maintainer requested a live sitrep before the tool existed, then directed they be recorded in the planning: (1) the tool must READ LIVE state from the existing instruments ([`audit-worker-saturation.py`](../../tools/audit-worker-saturation.py), [`collect-deliveries.py`](../../tools/collect-deliveries.py), the ledgers, [`next-prs.txt`](../next-prs.txt), [`merge-bypass-log.md`](../merge-bypass-log.md), [`session-handoff.md`](../session-handoff.md)), never the orchestrator's in-context memory, so every line is verifiable; (2) the usage footer must keep MEASURED (durations) and ESTIMATED (self-reported tokens) figures in separate columns, never summed, report a gap as UNKNOWN not zero, and never fabricate a total, which is the concrete dependency on TODO 3.131's per-worker logging (that logging is what turns the token column from UNKNOWN into measured).
- [`.working/validate-pr/history.md`](../validate-pr/history.md), [`.working/improvement-log.md`](../improvement-log.md), [`.working/merge-bypass-log.md`](../merge-bypass-log.md): #1206's validate-pr row (RETURNED PASS, 0 findings, SHIP; the worker re-read both stranded 1173/1180 deliveries at source) plus its retro and merge-bypass rows.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to the current queue (#1208 = the 3.115 gate-44 fail-opens).

### Verification
- The /sitrep TODO addition is dash-free and its instrument and rule links resolve.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

## 2026-07-27, Library Version 2026.07.696, PR #1206 (QA-cadence catch-up)

Pure-bookkeeping PR: brings the per-PR QA cadence and the delivery-tray backlog up to date. No corpus or code change.

### Changed
- [`.working/validate-pr/history.md`](../validate-pr/history.md): added #1205's post-merge validate-pr row (RETURNED PASS, 0 findings, SHIP; offloaded to jeff-mailz/claude with `--not-account security-work`, the first production dogfood of impl-3111's independence exclusion). Updated the two stranded rows the tray re-reconciliation surfaced: **1173** (was PENDING) to RETURNED PASS with 2 low notes; **1180** (was DISPATCHED) to RETURNED PASS with F-1 (warning) routed to TODO 3.127. The 1173 row was also completed from 5 cells to the 7-column format.
- [`.working/improvement-log.md`](../improvement-log.md): #1205 retro row (the dual-family verify caught a fail-closed gap a single lens missed; the guard-inputs pattern, validate input existence/authority not only its shape).
- [`.working/merge-bypass-log.md`](../merge-bypass-log.md): #1205's `--admin --squash` merge row, from the observed CI state (merge commit `df0e8d82`, all three checks SUCCESS).
- [`TODO.md`](../../TODO.md): 3.127 gains the concrete below-composer residual route that validate-pr-1180 F-1 confirmed (`manage-workers.py:242` last-two-rules heuristic; the structural fix is to anchor on the border PAIR).
- [`.working/session-handoff.md`](../session-handoff.md): reconciled the current-truth snapshot (green-at `df0e8d82` #1205, library 2026.07.696 / README 1.10.57) and the next-actions queue (#1207 = the 3.115 gate-44 fail-opens, re-verified apply-ready).
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to the current queue.

### Verification
- The two consumed QA results were re-read at source before dispositioning (1173 PASS + 2 notes; 1180 F-1 -> TODO 3.127, which already tracked the submit_state residual). No error-severity finding.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

## 2026-07-27, Library Version 2026.07.695, PR #1205 (impl-3111: exec-dispatch verifier-independence dispatch)

### Added
- [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py) (project-only fleet machinery; not pack material): account-keyed verifier-independence dispatch, closing TODO 3.111. Three CLI flags: `--not-worker <id>` and `--not-account <acct>` (exclude an account from the dispatch pool), and `--require-worker <id>` (target the account that minted an id, sugar over `--account`). The purpose is that a skeptical verifier, a re-verify, or a `/validate-pr` is never routed to the account that authored or already verified the work under review.
- `worker_id_to_key(worker_id)`: resolves a minted `{family}-{account}-{stamp}-{4hex}` id back to its durable `(account, family)` key (hyphenated accounts intact via a greedy `.+` against a fixed trailing anchor); returns `None` on a non-parsing id. Independence keys on `(account, family)`, never the ephemeral per-run worker-id, which encodes nothing routable.
- `resolve_exclusions(not_workers, not_accounts, family, known_accounts)`: returns `(excluded, unresolved, unknown)`. A cross-family `--not-worker` id is ignored (irrelevant by design).
- 17 new self-test cases (39 -> 56): fail-closed on unparseable AND on unregistered tokens, independence-deadlock vs empty-pool vs contradiction, cross-family-ignored, hyphenated/stamp-embedded account resolution.

### Changed
- `eligible_accounts` / `select_account` / `pick_account` / `dispatch`: thread an `exclude_accounts` filter, applied AFTER the family/model/availability funnel so `--dry-run` reports an independence-excluded account distinctly from an unavailable one. `pick_account` reports CONTRADICTION (target also excluded) and INDEPENDENCE-DEADLOCK (pool emptied by exclusions) distinctly from a genuine empty pool. The no-exclusion path is behaviourally byte-equivalent to the parent.
- [`TODO.md`](../../TODO.md): 3.146's heading corrected to the inherited-default-ACL cause (was the refuted "umask 0002" cause; `validate-pr-1204` N1, the heading lagged #1204's corrected body).

### Fixed
- **Fail-closed on a zero-match exclusion (open-findings, error).** As first written, `resolve_exclusions` validated only that a token PARSED, not that its account existed in the config, so a well-formed exclusion matching zero configured accounts (a mistyped `worka` for `work-a`, or a renamed/removed account, or a `--not-worker` id whose account left config) silently no-op'd at rc=0 while reporting the exclusion as applied. That silently defeats the independence control: the operator believes they excluded the authoring account, but the real account (correct name) stays eligible and the verifier lands back on it. Fixed: `resolve_exclusions` now takes `known_accounts` (config accounts for the family, availability-independent so a limited account is still a valid exclusion target) and the CLI FAILS CLOSED (`ap.error`, rc=2) on any zero-match exclusion, for both `--not-worker` and `--not-account`, with messages distinguishing unparseable from unregistered.

### Verification
- Self-test 56/56. Live CLI smoke tests: both original silent-no-op scenarios now rc=2, the control (a real configured account) still rc=0 and shifts the pick.
- **Dual-family adversarial verification** (the fleet-safety-critical tier, per the defence-in-depth default). Base commit reviewed by an independent Codex worker (jeff-mailz, refute-briefed) AND an independent Claude worker (security-work, refute-briefed); the two INDEPENDENTLY converged on the same root defect (Codex graded error, Claude graded warn) and prescribed the same fix. A single Claude re-verify on the fixed state (security-work) found no surviving defect and no regression, probing availability-independent membership, missing-field/None accounts, cross-family name collision, false-positive fail-closed, regex round-tripping, and the no-`--family` path.
- The pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

### Discipline observation
- The dual-family adversarial verify earned its cost again: both families converged on the SAME finding (strong corroboration), and a single-lens verify (Claude alone, which graded it a warn) would still have surfaced it here, but the convergence is the signal that the finding is real rather than a lens artefact. The fix is the exact one both prescribed; recording it against both.
- **Verifier-independence usage convention (for the new mechanism):** a re-verify or adversarial audit names the account to exclude via `--not-account`, defaulting to the account that produced the verdict under review; and per the TODO 3.111 folded insight, the exclusion is populated from DROP-authorship and TODO-source-authorship, not only delivery-authorship. This is orchestrator usage discipline layered on the mechanism (to be carried into the private orchestrator runbook).

## 2026-07-27, Library Version 2026.07.694, PR #1204 (record the concurrency-validation decisions; batch #1203 QA)

### Changed

- [`TODO.md`](../../TODO.md) **3.147** (worker OAuth token-refresh): folded in the maintainer-decided fix design (option 1.1, write-back) refined for the multi-worker case. The refinement is MEASURE-FIRST (does a refresh rotate the refresh token; what is the access-token TTL versus a run length), then: if refresh tokens do NOT rotate, plain per-worker write-back under the account lock is safe; if they DO rotate (likely, since a lapsed account needs a full re-login), SERIALIZE the refresh (the orchestrator refreshes the base token once before each concurrent batch so no worker rotates mid-run), with a single-per-account token broker as the heavier fallback for runs that outlive the access token.
- [`TODO.md`](../../TODO.md) **3.146** (check_perms group-writable recurrence): **corrected the root cause** from umask to the inherited **default POSIX ACL** (verified at source: `grc_library` carries `default:mask::rwx` / `default:group::r-x`, and the kernel ignores umask for files created under a default ACL, so new files get an ACL `mask::rw-` and display group-writable whatever the umask; the EFFECTIVE group permission is `r--`, so the files are already read-only and check_perms over-flags the mask). Maintainer-decided fix (option 2.1): lower the `default:mask` on the two READ-ONLY trees at the source AND make check_perms read the effective ACL group permission via `getfacl` (defence in depth). This corrects the umask-based fix 3.146 originally proposed.
- Fleet config (in the private worker-accounts store, pushed separately): after the same-account concurrency validated clean at 4 concurrent workers on one account, the maintainer set two max-concurrent-1 fallback accounts (jposluns-work-claude, jeff-posluns-codex) and raised the other four accounts to 4 for a testing window; the roadmap fallback rule was updated to supersede the earlier conservative ramp. Re-evaluate once 3.147 lands.

### Verification

- All 78 gates + PR-time checks green (both runners, unpiped). No corpus document or code changed: only the backlog, the README version surfaces, the CHANGELOG pair, and the batched `.working/` QA records. The three decisions were produced by the same-account concurrency test (4 workers concurrent on one account, zero output corruption) and its real worker-research deliverables (the impl-3111 design, the umask/ACL analysis that refuted the umask hypothesis, and the Week-of-07-13 CHANGELOG reconstruction). The #1203 QA rows (validate-pr, retro, bypass) batch in here per recursion-avoidance.

## 2026-07-27, Library Version 2026.07.693, PR #1203 (repair the Week-of-2026-07-13 root-CHANGELOG history loss; token-refresh follow-up)

### Fixed

- [`CHANGELOG.md`](../../CHANGELOG.md): **surgical repair of a root-history loss** (the sanctioned root-edit class: fixing an AI error). The **Week of 2026-07-13** weekly roll-up block had collapsed to only PR #1055, silently dropping about **189 PRs (#866-#1054)** from the root, which the root-never-loses-history invariant forbids. The block now reads **Week of 2026-07-13 (PRs #866-#1055)** with a reconstructed two-paragraph thematic summary (the reference-breadth section-3.57 close-out, three deep-assessment rounds r3/r4/r5 and their FR-200-to-219 remediations, jurisdiction/matrix-fit/crypto accuracy work, the grclibrary.ai website, the section-1.19 privatization and adopter-portability sprint, the credit-offload design, gates 69-72 and the section-1.22 self-guards, and validation sweeps 101-115). The adjacent **Week of 2026-07-06** header is corrected from `#667-#855` to **`#667-#865`** (PRs #856-#865, dated 07-12, belong to it and had been dropped), with a one-line close naming their theme (the CHANGELOG plain-language rework completion and the change-tracking convention flip). Reconstruction was drafted by a worker and **verified at source** by the orchestrator: #866-#1055 confirmed as exactly 190 PRs present with no gaps, and the themes spot-checked against the actual squash-merge subjects (#866 EDPB reference-breadth, #950 the website, #1000 Sweep 111, #1037 the tiered-CHANGELOG migration).

### Added

- [`TODO.md`](../../TODO.md) **3.147**: the worker OAuth token-refresh does not persist. The exec'd-worker wrapper's `--worker-id` path snapshots the account config dir (including the token), runs claude against the throwaway snapshot, and deletes it, so a mid-run token refresh is lost and the base token is never renewed, which is why worker accounts expire about 1-2h after re-auth (observed 2026-07-27 across jposluns-work, security-work, jeff-mailz). The snapshot isolation that makes same-account concurrency safe is what breaks refresh persistence. Options (write-back, periodic base refresh, API keys, or accept manual re-auth) recorded for a maintainer decision. P3 counter 3.147 -> 3.148.

### Verification

- All 78 gates + PR-time checks green (both runners, unpiped). The CHANGELOG-hygiene preflight passes (no dashes, path-shaped references linked). This repair was validated during the same-account-concurrency test that also produced the reconstruction draft as a real worker deliverable (4 workers ran concurrently on jposluns-work with zero output corruption). The #1202 QA rows batch in here per recursion-avoidance.

## 2026-07-27, Library Version 2026.07.692, PR #1202 (exec-dispatch registry fails closed on a corrupt inflight.json; TODO 3.145)

### Fixed

- [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py): the in-flight concurrency registry read now **fails CLOSED on a corrupt registry file** (TODO 3.145, the GATE before per-account concurrency > 1). `_read_inflight` distinguishes a MISSING file (`FileNotFoundError` -> `[]`, so the first-ever dispatch still allows) from a CORRUPT one (unparseable JSON, a non-FileNotFound `OSError`, a non-list, **or a list whose elements are not objects** -> raise the new `InflightCorruptError`). `_reserve_slot` refuses the dispatch on corruption with an operator message naming the file and **leaves the file in place** (no fail-open zeroing, riding the existing NOT-DISPATCHED path); `_release_slot` **no-ops** on corruption, so a corrupt registry during a release cannot wipe live co-tenant entries. Self-test **31 -> 39**. Applied from the delivered worker candidate (preserved in the private worker-deliveries store) with orchestrator re-verification of the logic at source; the #1199 registry (`_reap`, `_inflight_key`, `_max_concurrent`, `--worker-id`) is byte-identical outside the four touched functions and the self-test.

### Verification

- **Dual independent adversarial verifiers, one per family (defence in depth for a fleet-safety gate):** a Claude verifier (jeff-mailz) UPHELD all six refute-claims (SHIP); a Codex verifier (jeff-mailz) caught a real gap the Claude one only grazed, a JSON list of NON-OBJECTS (`[1,2,3]`) passed the `isinstance(list)` check and then crashed `_reap` with an uncaught `AttributeError` on `e.get(...)` instead of failing closed. The orchestrator **re-verified the Codex finding at source** (reproduced the AttributeError), FIXED it (`_read_inflight` now requires a list of objects), and added reality-fixture self-tests (scalar-list refuses + release tolerated). This resolves both fail-opens tracked in [`.working/open-findings.md`](../open-findings.md) (the RESERVE fail-open and the Sweep-125-W1 RELEASE co-tenant-wipe) plus the scalar-list crash. All 78 gates pass; self-test 39/39. Pre-push guard green both runners.
- The #1201 QA rows batch in here per recursion-avoidance: `validate-pr-1201` RETURNED PASS (0 error / 0 warning / 1 pre-existing note) in [`.working/validate-pr/history.md`](../validate-pr/history.md); the `/retro` row in [`.working/improvement-log.md`](../improvement-log.md); and #1201's merge-bypass-log row in [`.working/merge-bypass-log.md`](../merge-bypass-log.md).

### Changed

- [`TODO.md`](../../TODO.md): **3.145 rotated to [`DONE.md`](../DONE.md)** (closed by this PR); **3.146 opened** for the umask-`0002` recurrence the fix's own `check_perms` run surfaced (new files in the READ-ONLY repos come out group-writable; needs a durable maintainer umask fix, e.g. `0027`, in the orchestrator's launcher). P3 counter 3.146 -> 3.147.

## 2026-07-27, Library Version 2026.07.691, PR #1201 (2026-07-27 morning resume close-out)

### Added

- **Sweep 125** row in [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the loop-break corpus-wide `/validate` over the #1195..#1199 deltas (base `79578c6e`=#1194, head `e554f1b7`=#1199, 18 files) at the 2026-07-27 morning `/resume`, the compensating control for the #1200 session-closing handoff. OFFLOADED via [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py) to jposluns-work/opus (~16m), consumed under ELEVATED QA (first QA-kind delivery from this account+model this session): the orchestrator independently re-derived the mechanical baseline (all 78 gates green on the writable checkout, the worker's 77/78 being the known read-only-`tests/tmp/` gate-36 artefact with 0 AssertionError) and re-verified the one warning at source. **0 error / 1 warning / 7 note. PASS-with-findings; all 4 asserted-clean surfaces CORROBORATED, ZERO contradicted, so the loop-break control for #1200 PASSES.**

### Changed

- [`.working/session-handoff.md`](../session-handoff.md): advanced the Resume cursor to Sweep 125; added a 2026-07-27 morning-resume progress note to the current Next-actions block; **pruned per the keep-current-plus-one-prior discipline** (deleted the oldest PRIOR-session Next-actions block and the #1177 Asserted-expectations block, 121 lines; their narrative is durably recorded in CHANGELOG / DONE / [`pending-decisions.md`](../pending-decisions.md) / git history, migrate-before-delete confirmed).
- [`.working/session-state.md`](../session-state.md): acquired the concurrency lease for `claude/resume-2026-07-27` and swapped the operating mode `overnight-unattended` -> `attended-autonomous` (maintainer present, daytime).
- [`TODO.md`](../../TODO.md): folded the triaged inbox-drop insights into existing items, 3.128 (the `audit-token-spend` first-match root cause + heading-anchor fix pointer), 3.111 (exclude a worker by drop-authorship and TODO-source-authorship, the prio-0 self-verify deadlock, plus the old-tool `cmd_claim` stamp-storm), and 3.118 (a rebased manage-workers apply-candidate pointer); and **corrected 3.145 to fold in Sweep 125's W1** (the RELEASE co-tenant-wipe fail-open, distinct from and worse than the tracked RESERVE one; "RELEASE may stay best-effort" was wrong, the fix must no-op RELEASE on corruption, which the delivered candidate does).
- Cleared the accumulated worker-exchange backlog: **12 unprocessed inbox drops** triaged and moved to the file-drop `done/drops` archive (benign id-churn, verify-independence recurrences from the superseded file-drop fleet, and old-tool defects, all dispositioned); **5 open scratch maintainer-alert-channel alerts cleared** on maintainer authorization (three verify-independence recurrences tracked in TODO 3.111/3.113 with insights folded in; two confirmed resolved); and a Codex-worker cross-runtime orchestration planning framework **routed to the private store** (INDEX row + roadmap-G note) on maintainer direction.

### Fixed

- [`.working/merge-bypass-log.md`](../merge-bypass-log.md): added the #1200 bypass-log row. The prior session's session-closing handoff merged via the `--admin` bypass, but a handoff PR cannot honestly log its own not-yet-completed merge, so per the go-forward practice the row is added in this following change from the OBSERVED `gh pr checks 1200` state (all three checks green: Lint markdown corpus, Web generator health, Cloudflare Pages; merge commit `8094b06d`). This clears gate 50's Check 6 and the paired gate-36 regression test that runs the bookkeeping-parity linter against HEAD.
- [`.working/open-findings.md`](../open-findings.md): recorded Sweep 125's W1 (the `_release_slot` co-tenant-wipe fail-open, re-verified at source against `main`) as a routed warning, ROUTED to TODO 3.145 (folded in; moot at cap 1, already resolved by the delivered registry-hardening candidate; gates the concurrency-enable, not any merge).

### Verification

- Pre-push guard green (run_all_audits.sh all 78 gates + run-pr-time-checks.sh, both standalone, unpiped). No corpus document or code file changed: only `.working/` records, the backlog, and the README version surfaces, plus the CHANGELOG pair. **Loop-break:** this is the first PR of the resumed session (the `/validate` close-out), not a handoff PR, so it carries its own per-PR QA in the normal way. The Sweep 125 result and its findings are dispositioned above.

## 2026-07-27, Library Version 2026.07.690, PR #1200 (session-closing handoff at #1199)

### Changed

- Session-closing handoff at #1199 (overnight-unattended; evidence-triggered wind-down on the legitimate A12 basis, threshold met plus a named RM-10 pipe-mask slip, after an un-instrumented-basis attempt was correctly reversed first; both logged in the private autonomous-decisions-log). Refreshes [`.working/session-handoff.md`](../session-handoff.md) with the current-session Next-actions and Asserted-expectations blocks and the green-at `e554f1b7` snapshot; releases the concurrency lease in [`.working/session-state.md`](../session-state.md); refreshes [`.working/next-prs.txt`](../next-prs.txt) and appends the morning-deferred queue to [`.working/pending-decisions.md`](../pending-decisions.md). Names the morning worker pre-queue: the #1199 PR-scoped validation (vpr-1199b), the delivered 3.145 fail-closed-registry candidate, and the delivered 3.133 close-out-tool draft, all preserved under the private worker-deliveries store.

### Verification

- Pre-push guard green (run_all_audits.sh + run-pr-time-checks.sh, both standalone, unpiped). No corpus document or code file changed: only `.working/` records and the four version surfaces. Loop-break: this handoff PR skips its own trailing validate-pr and retro; the compensating control is the morning corpus-wide validate over the #1195 to #1199 window.

## 2026-07-27, Library Version 2026.07.689, PR #1199 (exec-dispatch per-account concurrency registry + worker-id)

### Changed

- [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py): moves per-account concurrency-cap ENFORCEMENT off the wrapper's per-account flock and into an in-flight registry (TODO 3.141, the orchestrator half). A worker-built candidate (self-test extended from 17 to 31 checks, all passing), applied verbatim and skeptical-verified. The additions: an in-flight JSON registry under `JOB_DIR` guarded by a separate never-rewritten `inflight.lock`; `_reserve_slot` performing reap-count-refuse-or-append in ONE exclusive flock critical section (no check-then-act TOCTOU), holding the lock only for the reserve/release and never across the job's `subprocess.run`; pid-liveness reaping (`os.kill(pid, 0)`, the dispatcher's own pid as the liveness token) with a 24h absolute stale ceiling as the only time-rule; `_release_slot` freeing the slot on the dispatch EXIT path; a per-config-dir registry key (account+family, so a claude and a codex job on one subscription do not share a cap); a default of 1 when `max_concurrent` is absent (byte-equivalent to prior behaviour); and `--worker-id` now passed through to the (already backward-compatible) root wrappers.

### Not yet enabled (deliberate)

- Concurrency stays at `max_concurrent` 1 in the account config. Turning it on is a SEPARATE, careful step (bump one claude + one codex account to 2 per the overnight fallback rule, verify one isolated dispatch, then run the duplicate-real-task validation protocol). This PR lands the capability only.

### Also (batched #1198 QA)

- The #1198 merge-bypass row, the retro-1198 row. The validate-pr-1198 row is added on its return.

### Verification

- `python3 tools/exec-dispatch.py --self-test`: OK (31 checks). Dry-run account selection regression clean. `tools/run_all_audits.sh`: all 78 gates pass; pre-push guard green both runners. A skeptical verifier reviewed the concurrency logic pre-merge.

## 2026-07-27, Library Version 2026.07.688, PR #1198 (weekly CHANGELOG roll-up + #1197 over-collapse correction)

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the completed week's daily lines (2026-07-22 through 07-26) are rolled into one `**Week of 2026-07-20 (PRs #1056-#1194)**` summary block, per the weekly roll-up discipline. Root history is summarized in place, never removed; the 2026-07-27 entries (#1195, #1196, #1197, #1198) stay per-PR as the current day. No mirror sweep is needed (the week's detailed entries were already swept in #1191 and #1197).

### Fixed

- **#1197 over-collapse (validate-pr-1197 scope + orchestrator-found).** #1197's daily-rollup root collapse used the end-boundary `**Week of 2026-07-13**`, so it replaced not only the sixteen 2026-07-26 per-PR entries (#1179-#1194) but also the 07-22/23/24/25 daily-summary lines between them and the week block, removing four daily summaries rather than summarizing them (a transient never-remove violation; git history retains them). This weekly block RESTORES the 07-22..07-25 content in aggregate, so the corrected end state summarizes the whole week in place. Retro-1197 records the lesson (a range-replace must end at the immediate next entry, not a distant section header).

### Also (batched #1197 QA)

- The #1197 merge-bypass row, the retro-1197 row, and the open-findings warning for the over-collapse (FIXED here). The validate-pr-1197 row is added on its return.

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass (gate 59 mirror-parity green). Pre-push guard green on both runners.

## 2026-07-27, Library Version 2026.07.687, PR #1197 (2026-07-26 daily CHANGELOG roll-up)

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the sixteen 2026-07-26 per-PR root entries (#1179 through #1194) are collapsed into one daily-summary line (`**2026-07-26 | 2026.07.684 | PRs #1179-#1194 (16 PRs)**`), per the daily roll-up discipline (D9). Root history is summarized in place, never removed; the 2026-07-27 entries (#1195, #1196) stay per-PR as the current day.

### Removed (swept to the private archive)

- The sixteen matching detailed-mirror entries (#1179 through #1194) are swept verbatim to [`grc_library_private/changelog-archive/2026-07-detailed-1179-through-1194.md`](../../../grc_library_private/changelog-archive/2026-07-detailed-1179-through-1194.md) and pruned from the in-repo mirror, so the gate-59 mirror-parity floor moves to #1195 (the swept entries fall out of scope, not flagged missing). The in-repo mirror now holds only the current week (#1195, #1196). Coupled operation: root roll-up plus mirror sweep move together.

### Also (batched into this close-out)

- TODO **3.144** added (multi-orchestrator / self-refreshing orchestration), a SCOPE/SPEC-GATED `needs-decision` item capturing the 2026-07-27 design discussion (Form 1 one-shot auto-handoff, Form 2 primary-plus-standby, the unix-socket transport lean, and the hard parts) for maintainer scoping before any build; P3 counter advanced to 3.145.
- #1196 QA rows batched (merge-bypass row, validate-pr-1196 row + record, retro-1196 row).
- validate-pr-1196 N1 fixed: [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) US 'behavioral' to Canadian 'behavioural'; and a duplicate table header in [`.working/open-findings.md`](../open-findings.md) (introduced by an earlier insert) removed.

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass (gate 59 mirror-parity green after the coupled sweep). Pre-push guard green on both runners.

## 2026-07-27, Library Version 2026.07.686, PR #1196 (origin paragraph + resume/compaction codifications)

Overnight bookkeeping bundle: the corpus-origin narrative, the persistence-of-directives codifications the maintainer asked for this session, two newly-registered backlog items, and #1195's QA rows.

### Added

- [`CHANGELOG.md`](../../CHANGELOG.md) `Week of 2026-05-25`: the maintainer-approved two-paragraph origin story (the corpus's pre-2009 practitioner roots, the hand-tended-to-AI-managed transition with a required Human In The Loop, and the ambition to distil the disciplines into a portable pack), with "replicable pack of rules" linked to the pack README.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): a high-placed rule (before `## Project`) to RE-READ the `_private` READ-THIS-FIRST list and the private roadmap file after every `/resume` AND especially after every conversation compaction, plus a directive-persistence protocol (when the maintainer gives direction, check if it is logged, assess cross-session persistence, and if it persists log it in the IMPORTANT place before acting). Mirrored by a re-read note at the top of the `_private` READ-FIRST block.
- [`TODO.md`](../../TODO.md): `3.142` (`/sitrep` situation-report command, recovered after being dropped in the emergency wind-down) and `3.143` (worker-account onboarding process + add-account script, for the accounts arriving tomorrow); P3 counter advanced to 3.144. Both umbrella A.

### Changed

- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) worker-offload rule lead-in: "two-part hard rule" corrected to "the hard rule ... expanded to six points" (validate-pr-1195 W1, the stale-descriptor-after-body-growth class).
- [`.working/session-state.md`](../session-state.md): Operating-mode set to `overnight-unattended`; lease and heartbeat refreshed.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to the current queue.

### Also (batched #1195 QA)

- The #1195 merge-bypass row, the validate-pr-1195 row + record ([`2026-07-27-PR-1195.md`](../validate-pr/2026-07-27-PR-1195.md), 0 error / 1 warning / 1 note, offloaded to a worker), the retro-1195 row, and the W1 open-findings row (FIXED here).

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass. Pre-push guard green on both runners.

## 2026-07-27, Library Version 2026.07.685, PR #1195 (post-wind-down resume close-out)

The first-PR close-out of the 2026-07-26 post-emergency-wind-down resume. Batches the Sweep 124
close-out, #1194's QA rows, one backlog re-scope, a new Priority-1 series, and two maintainer-directed
codifications.

### Added

- **TODO Priority-1 series 1.26** (goal-description umbrella + phases 1.26.1 to 1.26.4): consolidate,
  harmonize, and distribute the quality machinery across AI toolchains (deduplicate/simplify the
  machinery; integrate the community's CC BY-SA ShareAlike contributions from team members and adopters
  on local/custom models; reach true public-pack parity; distribute aligned packs, Codex first, then a
  generic tool-agnostic form). ON HOLD pending all Priority-3 tooling. Placed at the top of P1; P1
  counter advanced to 1.27.

### Changed

- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Communication conventions`:** the no-diff rule is
  strengthened to a mechanical command-level ban (maintainer-directed 2026-07-26, after repeated
  violations): never run a command whose output is a +/- unified diff (`git diff` / `git show <commit>`
  without `--stat`/`--name-only`); inspect changes with `--stat`/`--name-only`, `git status --short`,
  `grep`/`wc`, or a targeted read.
- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Mandatory worker offload`:** the worker-first
  doctrine (maintainer-directed 2026-07-26): if a worker CAN do it, a worker DOES it (no self-run);
  spawn on demand with [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py) and never gate offload
  on a `list-workers` count of zero; 20-minute reissue to another account; super-sensitive tasks go to
  BOTH a Codex and a Claude worker; keep the fleet busy (one on QA, the rest pre-loading the next items);
  and a privacy note that worker ids in the public repo are anonymized aliases only.
- **[`TODO.md`](../../TODO.md) section 3.128** re-scoped to the per-worker-display residual with a STATUS
  line marking W1/W2 FIXED in #1189 (Sweep 124 W1; the item's prose had contradicted the shipped code).

### Also (batched close-out bookkeeping)

- Sweep 124 recorded in [`validate-sweeps/history.md`](../validate-sweeps/history.md) (0 error / 1
  warning / 1 note; the #1185 to #1194 window ships clean; all asserted-clean claims corroborated, zero
  contradicted) and the handoff Resume cursor advanced to Sweep 124.
- #1194's QA rows batched: the merge-bypass row, the validate-pr-1194 row (subsumed by Sweep 124), the
  retro-1194 row, and the two Sweep 124 findings recorded and dispositioned in
  [`open-findings.md`](../open-findings.md).
- Handoff Current-truth snapshot version tokens reconciled to the #1195 head; the keep-current-plus-one
  block prune is deferred to the session-closing handoff.

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass (standalone).
- Pre-push guard (both runners) green before push.
