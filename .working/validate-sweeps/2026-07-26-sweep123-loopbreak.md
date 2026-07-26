---

# GRC Corpus-Wide Loop-Break `/validate` - Findings Report

**Scope:** Compensating control for the #1184 session-closing handoff (which skipped its trailing per-PR QA).
**Repo:** `/home/grc/grc_library` @ pinned `dd50cf4a` (`git cat-file -t` → `commit`; `rev-parse HEAD` → `dd50cf4a986aded4a0efaac3e4ca24092f2e830c`).
**Delta window:** base `e7eea68e` (#1180) → head `dd50cf4a` (#1184), merges #1181/#1182/#1183/#1184.
**Posture:** READ-ONLY. Write-probe to `tests/tmp/` → `Permission denied` (confirmed no corpus write access).
**Date:** 2026-07-26.

## Verdict: **CLEAN** - zero genuine misses, zero contradictions of asserted-clean claims.

0 error / 0 warning / 1 note. The single note is an **environment artifact of the read-only sandbox**, not a corpus defect, and contradicts no asserted claim. All four targeted confirmations pass with proof-of-run. The loop-break control for #1184 **PASSES**.

---

## Findings

### NOTE-1 - Linter regression suite (1 gate) is not runnable in the read-only worker sandbox (environment, not corpus)
- **Severity:** note (environment artifact; **not** a finding against the corpus)
- **Path:** `tools/run-linter-regression.py` (invoked as gate "Linter regression test suite", `tools/run_all_audits.sh:124`)
- **Evidence:** `run_all_audits.sh` reports **gates 1-78 all `OK`**, then `1 of 78 audit gate(s) failed: - Linter regression test suite`. Direct run: `FAILED (errors=242)`, every error being `PermissionError: [Errno 13] Permission denied: '/home/grc/grc_library/tests/tmp/…'` (the suite writes fixtures to `tests/tmp/`, which this worker cannot write - `ls -ld tests/tmp` → `drwxr-s---`, write-probe denied) or `could not locate the grc_library_ref index … looked for /home/grc/grc_library_ref` (ref sibling not at the expected path). No error is a corpus-content assertion failure.
- **Why not a MISS:** the handoff asserts green "on both runners (78 gates + all PR-time checks)"; those runners had write access. The 78 corpus-content gates independently pass here. Not-testable-in-sandbox, routes to nothing.

*(No error/warning findings surfaced.)*

---

## Targeted confirmations (with proof-of-run)

### 1. #1181 ledger repair is FAITHFUL - **CONFIRMED**
Every restored row traces to real git history; nothing invented, nothing lost.
- **Sweep 91 (the overwrite recovery):** `git merge-base --is-ancestor e94b6923 dd50cf4a` → **YES** (`e94b6923` = "#721 Sweep-91 close-out", a real ancestor). Two distinctive substrings of the head Sweep 91 row (`OVERNIGHT-SWAP handoff PR #720…`, `no close-vs-start drift); clone non-shallow. Pre-flight: 400 files, 33 suppressed, 9 candidates`) are present **verbatim** in `e94b6923`. At the pre-repair parent `13861709^` the row was **ABSENT** (`grep -c '| 91 iter 1 '` → 0); at head it is **PRESENT**. In `e94b6923` the physical line matching `91 iter 1` carries 3 `iter` tokens (the fusion state), consistent with the de-fusion story.
- **Sequence integrity:** sweeps run **9→122 with no gaps** (91 and 92 both present); the only repeats are legitimate multi-iteration rows (9/10 iter 1/2/3).
- **matrix-fit half:** the two restored rows (FR-167 batch 11 privacy, batch 10 ai) are the exact split of the fused `-` line into two `+` lines, with a proper **version co-bump 1.0.13→1.0.14 / date 2026-07-24→2026-07-26**.
- **worker-prompt-log half:** 20 added `|`-rows, all timestamped **2026-07-26** (in the takeover-session window); these are the 5 keystroke-injection records recovered from the stash (never committed by design - the independent adversarial pre-push verifier, `verify-1181-ledger-repair`, is the recorded control for those).

### 2. #1182 and #1183 landed clean - **CONFIRMED**
- **#1182** (`2995788f`): `validate-pr/history.md:16` → **PASS with 1 info finding** (F-1, the lease-quote `(daytime)` gloss), **fixed in #1183**. Bypass row present (`merge-bypass-log.md:38`, `--admin --squash`, green CI). CHANGELOG `2026.07.672`.
- **#1183** (`2c594d03`): `validate-pr/history.md:15` → **RETURNED CLEAN, 0 findings**; guardrail-review r16 present and COHERENT. Bypass row present (`:37`). CHANGELOG `2026.07.673`.

### 3. Machinery inventory 78/15/24/16 - **CONFIRMED** (each from its source of truth)
- **78 gates:** `grep -c 'run_gate ' run_all_audits.sh` → **78**; suite runs gates 1-78 contiguous, no hole.
- **15 rules:** `ls dev-security/claude-rules/governance/*.md | grep -iv README | wc -l` → **15**.
- **24 skills:** `ls -d dev-security/claude-rules/skills/*/ | wc -l` → **24**.
- **16 commands:** `ls .claude/commands/*.md | wc -l` → **16**.
- **Independent cross-checks (lens B):** gate 39 (`lint-gate-count-consistency.py`) exits 0 - *"collection-count references consistent across 564 files (gates 78, governance rules 15, skills 24…)"*; spec §6 inventory = 78 rows; guardrail r16 token = *"78 gates / 15 rules / 24 skills / 16 commands."* All agree.

### 4. Sweep fail-open (TODO 3.129) is REAL and UNFIXED at head - **CONFIRMED (unfixed)**
`tools/sweep-working-records-to-private.py` gates every destructive prune on **`is_file()` existence, never content**:
- verify-before-prune checks at `:674`, `:678`, `:684` (changelog-details / records / rollup-rows) and helper `oneoff_missing_from_archive` at `:200` all test only `if not p.is_file()`.
- No size/hash/content comparison exists between the working file and its archived copy before destruction at `:735 f.unlink()` / `:742 shutil.rmtree(...)`. The re-parse assertions (`:706-731`) validate only the *in-repo mirror's* internal consistency, not archive fidelity.
- `TODO.md:644` §3.129 is **OPEN**. A present-but-empty/truncated/stale archive copy passes the guard and the working original is destroyed → data loss. **Do not run `--prune` until 3.129 lands.**

---

## Asserted-expectations cross-check
Source: `.working/session-handoff.md` "Asserted expectations (2026-07-26 ORCHESTRATOR-TAKEOVER session close)" (lines 171-196).

| Asserted claim | Result |
|---|---|
| #1181 ledger repair: pre-push guard green (78) + independent adversarial verify (nothing invented/lost; Sweep 91 orphan byte-identical) + post-merge validate-pr; merged `13861709` | **CORROBORATED** (Conf. 1; validate-pr row 17; 78 gates OK) |
| #1182 reconciliation: validate-pr PASS (1 info, fixed in #1183); merged `2995788f` | **CORROBORATED** (Conf. 2) |
| #1183 `/restore-broken` + r16: independent pre-push verify CLEAN + r16 COHERENT + post-merge validate-pr CLEAN; merged `2c594d03` | **CORROBORATED** (Conf. 2) |
| Machinery 78 gates / 15 rules / 24 skills / 16 commands; library `2026.07.673`, README `1.10.34` | **CORROBORATED** - counts exact; `.673`/`1.10.34` is the as-of-#1183 snapshot (guardrail r16); head is `2026.07.674`/`1.10.35` after #1184's one-patch bump (consistent, not a contradiction) |
| Worker-access permission model correct across five dirs; three control scripts in `/home/grc` (root:root 0700; `check_perms.sh` 0500) | **NOT-TESTABLE** - those dirs/scripts are outside the repo tree and outside this read-only worker's reach |
| NOT-asserted-clean: sweep `--prune` fail-open (3.129) REAL and UNFIXED | **CORROBORATED** as still-open (Conf. 4) |

**No asserted-clean surface is contradicted → zero genuine misses to escalate.** Parity extras verified: #1184's validate-pr row is the recorded **SKIPPED handoff-PR exception** (loop-break, `validate-pr/history.md:14`), and gate 50 (in the 78-OK set) holds; #1184's own bypass row is written by the next session (expected lag), not a gap.

---

## Proof-of-run (commands + key outputs)
```
git -C … cat-file -t dd50cf4a                       → commit
git -C … log --oneline e7eea68e..dd50cf4a           → 4 merges #1181..#1184 (as scoped)
grep -c 'run_gate ' run_all_audits.sh               → 78
ls claude-rules/governance/*.md | grep -iv README|wc → 15
ls -d claude-rules/skills/*/ | wc -l                → 24
ls .claude/commands/*.md | wc -l                    → 16
lint-gate-count-consistency.py                      → exit 0 (78/15/24, 564 files)
run_all_audits.sh                                   → gates 1-78 OK; regression-suite gate errors = sandbox write-perm only
git merge-base --is-ancestor e94b6923 dd50cf4a      → YES (real ancestor #721)
show 13861709^:…validate-sweeps → grep '91 iter 1'  → 0 (absent pre-repair)
HEAD …validate-sweeps → sweeps 9..122, no gaps
sweep-working-records-to-private.py :200/:674/:678/:684 → is_file() only; :735 unlink / :742 rmtree
TODO.md:644 §3.129                                  → OPEN
tests/tmp write-probe                               → Permission denied (read-only confirmed)
```

## Token-spend estimate
**~92k tokens (estimate, not instrumented).** Composition: ~50k reading persisted tool-results (session-handoff 49.8KB + two large diff dumps) + ~30k audit/grep command outputs + ~12k reasoning/report. No subagents dispatched (single-context read-only sweep). Label: **estimate**, derived from observed tool-result sizes; not a measured meter reading.

<!-- END OF DELIVERY -->
