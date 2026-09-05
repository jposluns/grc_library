#!/usr/bin/env python3
"""Delta gate D14: class-completeness attestation reproduce-check (P-1.67).

THE CLASS IT MECHANIZES. The recurring "fix the cited instance, miss the siblings" failure
(sibling-completeness): a defect named by a bracketed class token is fixed where it was
cited while the same wording survives elsewhere in the corpus (#1955/#1957/#1981/#1982/#1983
all auto-graduated this way). The open-findings ledger's attestation grammar (P-1.67) makes
the class check part of the FIXED disposition; this gate is the fail-closed verifier.

WHAT IT CHECKS. For each row of the ledger's `## Open` OR `## Closed today` table (both,
because a fixed finding is dispositioned and MOVED to `## Closed today` in the same PR, so an
Open-only scan would miss exactly the rows it verifies) whose Found date is on or after
the SHIP-DATE FLOOR (dynamic floor: pre-mechanization rows are never retro-failed), whose
disposition is a valid `FIXED <ref>` (3.126 grammar), and whose Finding cell LEADS with a
bracketed class token:
  1. GRAMMAR (fail-closed): the Disposition cell must carry a `[class: "<token>" @ <count>]`
     attestation or a `[class-exempt: <reason>]` clause with a reason from the closed set.
  2. REPRODUCE: for a `[class: ...]` clause, re-run the shared class-completeness matcher
     for the attested token over the GIT-TRACKED corpus markdown set and FAIL when the
     occurrence count EXCEEDS the attested count (a sibling survived or a new instance crept
     in) or when any corpus file is unreadable (a path escape: the completeness claim cannot
     be reproduced over an incompletely readable set). A count at or below the attested
     value passes: only growth fails.

GUARD-INPUT DISCIPLINE. The token and count are AUTHOR-DECLARED (emitted by
tools/check-class-completeness.py --attest): the finding prose has no authority to answer
"which distinctive string identifies this class", so this gate RE-RUNS the declared probe
and never re-judges relatedness. Stable unrelated matches are inside the attested count and
never fire; growth requires an explicit re-attestation, which IS the class re-check.

FAIL-CLOSED, WITH ITS SCOPE STATED. On a resolvable ledger, any malfunction of this gate's
own inputs (an unloadable grammar module, an unenumerable git-tracked set, an unreadable
ledger) FAILS the check rather than passing it. The ledger is maintainer working state
resolved through lint_common.resolve_working, so on public CI and adopter clones it is
legitimately ABSENT and the gate no-ops (exit 0), the same graceful degradation every
`.working/`-reading gate takes; the fail-closed property therefore binds where the ledger
exists, the maintainer's pre-push runner. Residue, stated honestly (codex/claude QA #1989
iter-2; CLOSED by P-1.70 parts 1-2, #1994 follow-up): a MALFORMED row (cell count != 5 after
border-trim) has no trustworthy cell, so the parser blanks its Found and nulls its Disposition.
This gate now FAILS-CLOSED on any such row in either scanned section (no in_window call: the
blanked Found cannot be trusted), after the 6 pre-existing malformed `## Closed today` rows were
repaired (the appended-disposition shape, not an unescaped pipe). The heterogeneous QA sub-tables
live OUTSIDE the scanned `## Open`/`## Closed today` sections, so fail-closed cannot false-positive
on them. ONE residue remains (b, below): residue (a), a WELL-FORMED finding-row mis-filed OUTSIDE the
scanned sections, is now CLOSED by the P-1.70 part-2b mis-filed-row detector (``misfiled_finding_rows``
in the hook; a date|severity|-leading, column-0, non-fenced row that appears BEFORE the real
`## Closed today` archive opens, in the preamble above `## Open` OR orphaned between `## Open` and
`## Closed today` by a phantom heading, fails this gate closed). Stopping at the real `## Closed today`
is deliberate (the pre-landing sweep found the ledger's legitimate dated `## YYYY-MM-DD` archive uses
the same schema; see the hook fn for
the stated archive/fused-line residues). (b) the malformed-WRAPPER false-pass is NARROWED, not fully closed, it survives only the
contrived case of a malformed `[class:` wrapper together with any valid `[class-exempt:]` reason,
whether embedded in the wrapper token OR standalone/adjacent in the cell (a malformed wrapper yields
empty class_spans, so an adjacent exempt is matched too; author-run tooling, adversarial-only), ACCEPTED.

SINGLE GRAMMAR OWNER. The row parser and the attestation grammar are loaded from the
open-findings hook itself (importlib), and the matcher from check-class-completeness.py, so
there is exactly ONE parser and ONE matcher; this gate re-implements neither.

Usage:
    python3 tools/check-class-attestation-on-pr.py
    python3 tools/check-class-attestation-on-pr.py --floor 2026-09-04
    python3 tools/check-class-attestation-on-pr.py --self-test

Exit codes: 0 all pass (or no resolvable ledger); 1 findings; 2 environmental failure
(unloadable grammar/matcher module, unreadable ledger, unenumerable git-tracked set) on a
resolvable ledger, fail-closed.
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT, resolve_working  # noqa: E402

HOOK_REL = Path(".claude") / "hooks" / "block-on-open-findings.py"
MATCHER_REL = Path("tools") / "check-class-completeness.py"

# The mechanization's DYNAMIC ACTIVATION FLOOR (UTC). Only FIXED class rows (in `## Open` or
# `## Closed today`) whose Found date is ON OR AFTER this date are reproduce-checked, so the
# ledger's pre-P-1.67 rows are never retro-failed.
#
# Set to the DAY AFTER this gate merges, NOT the merge date: the FIXED class rows already in
# the ledger that were authored on the merge day (2026-09-04) BEFORE the attestation grammar
# existed, and the Found cell is day-granular, so a merge-date floor could not tell those
# pre-grammar rows apart from post-grammar rows added the same day, and would retro-fail
# them. Choosing day-after exempts all of the merge day, which is the price of the
# no-retro-fail property.
#
# DISCLOSED RESIDUE (codex/gemini QA #1989): a NEW class finding added AND fixed without
# attestation on the merge day itself, after this gate merges, is exempt forever (Found
# dates are permanent). The window is at most the few hours between merge and 00:00 UTC, it
# is self-closing (no new merge-day rows can be created after that), and while such a row
# remains in `## Open` the open-findings hook still emits its (date-unwindowed) advisory
# warning for it (that advisory does not fire once the row is moved to `## Closed today`,
# the hook's parser being Open-only). The retroactive
# attestation of the 15 pre-grammar rows is tracked as P-1.69; once they are attested or
# archived out of the scanned sections, this floor can be tightened to the merge date and
# the residue eliminated.
SHIP_FLOOR = datetime.date(2026, 9, 5)

FOUND_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _load(path: Path, name: str):
    """Load a repo module by path (the lint-audit-spec-detailed-prose precedent for
    cross-file loading of a hyphen-named tool). Raises on any load failure; the caller
    converts that to the fail-closed exit."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def in_window(found_cell: str, floor: datetime.date) -> bool:
    """PURE. True when the row's Found date is on or after the floor, OR unparseable.

    Fail-closed direction: a row that cannot PROVE it predates the mechanization is
    checked. The blanked Found cell of a malformed row never reaches here (its
    disposition is None, so it is failed closed before the window test, P-1.70 #1995)."""
    # F5 (codex QA #1989): require the Found cell to be EXACTLY one ISO date (full match of
    # the stripped cell), so an annotated or multi-date cell ("copied 2026-09-04; actual
    # 2026-09-05", "2026-09-04 typo") cannot let its FIRST embedded date falsely prove the
    # row predates the floor. Anything that is not a clean single ISO date is in-window and
    # fails closed.
    m = FOUND_DATE_RE.fullmatch((found_cell or "").strip())
    if not m:
        return True
    try:
        return datetime.date.fromisoformat(m.group(1)) >= floor
    except ValueError:
        return True


def evaluate(rows_full: list, hook, probe, floor: datetime.date = SHIP_FLOOR):
    """PURE decision core (the thin observers live in main; this is the testable half).

    rows_full: [(found, severity, finding, disposition)] from the hook's
        ``parse_dispositioned_rows_full`` (Open + Closed today; the caller in ``main`` supplies
        it, so D14 sees a fixed row whether or not it has been moved to Closed).
    hook: the loaded open-findings hook module, the single grammar owner
        (``is_fixed_disposition``, ``leading_class_token``, ``class_attestation_state``,
        ``extract_class_attestation``, ``CLASS_EXEMPT_REASONS``).
    probe: probe(token) -> (count, occurrences, skipped) over the attest file set;
        occurrences are (relpath, lineno, line) triples, skipped the unreadable relpaths.

    Returns (failures, notes): failures fail the gate; notes are surfaced but do not.
    """
    failures: list[str] = []
    notes: list[str] = []
    for found, _sev, finding, disp in rows_full:
        if disp is None:
            # FAIL-CLOSED (P-1.70): a malformed row (cell count != 5 after border-trim) has no
            # trustworthy cell, so the parser blanked its Found and nulled its Disposition; it must
            # NOT be skipped. No in_window() call: windowing on the blanked Found would trust an
            # untrustworthy cell. The heterogeneous QA sub-tables live OUTSIDE the scanned
            # `## Open` / `## Closed today` sections, so this cannot false-positive on them.
            failures.append(
                f"malformed ledger row (cell count != 5; an unescaped `|` must be written `\\|`, and "
                f"a superseding disposition REPLACES the Disposition cell, never appends after the "
                f"row's trailing `|`): {finding[:120]!r}. If this is a deliberate different-schema "
                f"sub-table, it does not belong in `## Open` or `## Closed today`; place it in a "
                f"dated archive section."
            )
            continue
        if not hook.is_fixed_disposition(disp):
            continue
        if not hook.leading_class_token(finding):
            continue
        if not in_window(found, floor):
            continue
        state = hook.class_attestation_state(disp)
        if state == "none":
            failures.append(
                f"unattested FIXED class row {finding[:120]!r}: no "
                '[class: "<token>" @ <count>] or [class-exempt: <reason>] clause. Run '
                'python3 tools/check-class-completeness.py --attest "<distinctive-token>" '
                f"and paste the emitted clause into the Disposition cell, or use "
                f"[class-exempt: {'|'.join(hook.CLASS_EXEMPT_REASONS)}] where no textual "
                f"class exists."
            )
            continue
        if state == "multi":
            failures.append(
                f"more than one class/exempt clause on FIXED row {finding[:100]!r}: exactly "
                f"one [class: ...] or [class-exempt: ...] clause is allowed per row."
            )
            continue
        if state == "bad-exempt":
            failures.append(
                f"invalid class-exempt reason on FIXED row {finding[:100]!r}: the reason "
                f"must come from the closed set {', '.join(hook.CLASS_EXEMPT_REASONS)}."
            )
            continue
        if state == "exempt":
            continue
        extracted = hook.extract_class_attestation(disp)
        if extracted is None:  # defensive: state 'class' implies a match
            failures.append(f"unextractable [class: ...] clause on row {finding[:100]!r}.")
            continue
        token, attested = extracted
        count, occurrences, skipped = probe(token)
        if skipped:
            failures.append(
                f"path escape reproducing the class probe for {token!r}: {len(skipped)} "
                f"corpus file(s) unreadable ({', '.join(skipped[:5])}); the completeness "
                f"claim cannot be reproduced over an incompletely readable set."
            )
            continue
        if count > attested:
            where = "\n".join(
                f"    {rel}:{ln}: {txt[:100]}" for rel, ln, txt in occurrences[:10]
            )
            failures.append(
                f"class-completeness regression for {token!r} (row {finding[:80]!r}): "
                f"{count} occurrence(s) now vs {attested} attested. Occurrences:\n{where}\n"
                f"  Fix or route each new occurrence in this PR, or re-attest (re-run "
                f"--attest and update the clause) after confirming the growth is a "
                f"legitimate unrelated sense."
            )
    return failures, notes


def _self_test() -> int:
    import tempfile

    checks: list[tuple[str, bool]] = []
    hook = _load(REPO_ROOT / HOOK_REL, "boof_for_d14_selftest")
    matcher = _load(REPO_ROOT / MATCHER_REL, "ccc_for_d14_selftest")
    floor = datetime.date(2026, 9, 4)

    def ledger(*rows: tuple[str, str, str, str]) -> str:
        head = ("## Open\n"
                "| Found | Severity | Finding | Source | Disposition |\n"
                "| --- | --- | --- | --- | --- |\n")
        return head + "".join(
            f"| {fd} | {sev} | {fi} | probe | {d} |\n" for (fd, sev, fi, d) in rows
        )

    def run(txt: str, probe):
        return evaluate(hook.parse_dispositioned_rows_full(txt), hook, probe, floor)

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        # REALITY FIXTURE (the CE3/CE3-CASP sibling-completeness shape): the cited
        # instance was fixed and ATTESTED AT 1, while two sibling occurrences of the
        # same distinctive wording SURVIVE elsewhere in the corpus (3 in total).
        (root / "a.md").write_text(
            "The non-EU/UK scoping caveat applies here.\n", encoding="utf-8")
        (root / "b.md").write_text(
            "Sibling one: non-EU/UK scoping caveat.\n"
            "Sibling two: non-EU/UK scoping caveat.\n", encoding="utf-8")
        files = matcher.corpus_files(root)

        def probe(token: str):
            occ, skipped = matcher.find_occurrences([token], files, root=root)
            return len(occ[token]), occ[token], skipped

        fails, _ = run(ledger(("2026-09-04", "warning",
                               "[CE3-CASP] monitoring-notice lawful-basis overclaim",
                               'FIXED #1984 [class: "non-EU/UK scoping caveat" @ 1]')), probe)
        checks.append(("reality-fixture-surviving-siblings-fail",
                       len(fails) == 1 and "3 occurrence(s) now vs 1 attested" in fails[0]))

        fails, _ = run(ledger(("2026-09-04", "warning", "[CE3-CASP] overclaim",
                               'FIXED #1984 [class: "non-EU/UK scoping caveat" @ 3]')), probe)
        checks.append(("attested-at-true-count-passes", fails == []))

        fails, _ = run(ledger(("2026-09-04", "warning", "[CE3-CASP] overclaim",
                               'FIXED #1984 [class: "non-EU/UK scoping caveat" @ 5]')), probe)
        checks.append(("count-decrease-passes-only-growth-fails", fails == []))

        fails, _ = run(ledger(("2026-09-04", "warning", "[CE3-CASP] unattested fix",
                               "FIXED #1984")), probe)
        checks.append(("unattested-in-window-fails",
                       len(fails) == 1 and "unattested FIXED class row" in fails[0]))

        fails, _ = run(ledger(("2026-09-04", "note", "[one-off] no textual class",
                               "FIXED #1985 [class-exempt: non-textual]")), probe)
        checks.append(("closed-set-exemption-passes", fails == []))

        fails, _ = run(ledger(("2026-09-04", "warning", "[bad] off-set reason",
                               "FIXED #1985 [class-exempt: too-hard]")), probe)
        checks.append(("off-set-exemption-fails",
                       len(fails) == 1 and "closed set" in fails[0]))

        fails, _ = run(ledger(("2026-09-04", "warning", "[multi] two clauses",
                               'FIXED #1985 [class: "x" @ 1] [class-exempt: singleton]')), probe)
        checks.append(("iter3-multi-clause-row-fails",
                       len(fails) == 1 and "more than one" in fails[0]))

        fails, _ = run(ledger(("2026-08-01", "warning", "[old-class] pre-floor row",
                               "FIXED #1900")), probe)
        checks.append(("pre-floor-row-exempt-dynamic-floor", fails == []))

        fails, _ = run(ledger(("undated", "warning", "[odd] unparseable Found",
                               "FIXED #1984")), probe)
        checks.append(("unparseable-found-is-in-window-fail-closed", len(fails) == 1))

        fails, _ = run(ledger(("copied 2026-09-04; actual 2026-09-05", "warning",
                               "[annot] annotated multi-date Found", "FIXED #1984")), probe)
        checks.append(("F5-annotated-found-is-in-window-fail-closed", len(fails) == 1))
        fails, _ = run(ledger(("2026-09-04 typo", "warning",
                               "[annot2] trailing-annotation Found", "FIXED #1984")), probe)
        checks.append(("F5-trailing-annotation-found-in-window-fail-closed", len(fails) == 1))

        fails, _ = run(ledger(("2026-09-04", "warning", "[E9] routed class",
                               "ROUTED TODO 3.73")), probe)
        checks.append(("routed-class-row-out-of-scope", fails == []))

        fails, _ = run(ledger(("2026-09-04", "warning", "unclassed finding",
                               "FIXED #1987")), probe)
        checks.append(("unclassed-fixed-row-out-of-scope", fails == []))

        def skipping_probe(token: str):
            return 0, [], ["bad.md"]

        fails, _ = run(ledger(("2026-09-04", "warning", "[CE3-CASP] overclaim",
                               'FIXED #1984 [class: "non-EU/UK scoping caveat" @ 3]')),
                       skipping_probe)
        checks.append(("skipped-file-is-a-path-escape-failure",
                       len(fails) == 1 and "path escape" in fails[0]))

        malformed = ("## Open\n"
                     "| Found | Severity | Finding | Source | Disposition |\n"
                     "| --- | --- | --- | --- | --- |\n"
                     "| 2026-09-04 | error | a cell with a raw | pipe | probe | FIXED #9 |\n")
        fails, notes = run(malformed, probe)
        checks.append(("malformed-row-fails-closed",
                       len(fails) == 1 and notes == [] and "malformed ledger row" in fails[0]))

        # P-1.70 reality fixture: the OBSERVED corruption shape (a superseding disposition appended
        # after the row's trailing `|`, making a 6th cell) inside `## Closed today` must FAIL-CLOSED,
        # not skip (the residue this closes; the hook's blocking path is `## Open`-only).
        closed_malformed = ("## Closed today\n"
                            "| Found | Severity | Finding | Source | Disposition |\n"
                            "| --- | --- | --- | --- | --- |\n"
                            "| 2026-09-02 | error | some finding | codex | ROUTED interim | FIXED #123\n")
        fails, notes = run(closed_malformed, probe)
        checks.append(("malformed-closed-today-appended-disposition-fails-closed",
                       len(fails) == 1 and notes == [] and "malformed ledger row" in fails[0]))

        # MOVE-TO-CLOSED EVASION (gemini QA #1989): a FIXED class row that the maintainer
        # dispositioned AND relocated to `## Closed today` in the same PR must STILL be
        # reproduce-checked; scanning only `## Open` would let a surviving sibling escape.
        closed_led = ("## Open\n"
                      "| Found | Severity | Finding | Source | Disposition |\n"
                      "| --- | --- | --- | --- | --- |\n"
                      "## Closed today\n"
                      "| Found | Severity | Finding | Source | Disposition |\n"
                      "| --- | --- | --- | --- | --- |\n"
                      "| 2026-09-04 | warning | [CE3-CASP] moved-to-closed same PR | probe | "
                      'FIXED #1984 [class: "non-EU/UK scoping caveat" @ 1] |\n')
        fails, _ = run(closed_led, probe)
        checks.append(("closed-today-row-is-checked-not-evaded",
                       len(fails) == 1 and "3 occurrence(s) now vs 1 attested" in fails[0]))

        # Escaped-pipe round trip: the cell carries `\|`, the extraction unescapes, and
        # the probe matches the literal `|` in the corpus.
        (root / "c.md").write_text("a weird | token line\n", encoding="utf-8")
        files = matcher.corpus_files(root)
        fails, _ = run(ledger(("2026-09-04", "warning", "[pipe-class] escaped pipe",
                               'FIXED #1990 [class: "weird \\| token" @ 1]')), probe)
        checks.append(("escaped-pipe-token-round-trips", fails == []))

        # P-1.70 part-2b: the mis-filed-row detector fires end-to-end. A finding-row spliced into a
        # legend section, and a row after a phantom backtick-`## ` heading, are both detected; a clean
        # all-in-scope ledger yields none; the severity vocabulary is pinned against silent drift.
        _mf_fix = (
            "## Disposition values\n"
            "| 2026-09-03 | error | a preamble mis-filed row | probe | FIXED #1 |\n"
            "## Closed today` and the row is deleted.\n"
            "| 2026-09-03 | error | after phantom | probe | FIXED #2 |\n"
            "## Open\n"
            "| Found | Severity | Finding | Source | Disposition |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 2026-09-05 | error | clean in-scope | probe |  |\n"
            "## Closed today\n"
            "| 2026-09-04 | error | a real closed row | probe | FIXED #8 |\n"
            "## 2026-08-24 archived QA record\n"
            "| 2026-08-24 | error | a legitimately archived row | probe | FIXED #9 |\n"
        )
        checks.append(("part-2b-detects-misfiled-and-post-phantom-rows",
                       len(hook.misfiled_finding_rows(_mf_fix)) == 2))
        checks.append(("part-2b-clean-ledger-has-no-misfiled",
                       hook.misfiled_finding_rows(
                           ledger(("2026-09-04", "error", "[x] a thing", "FIXED #1"))) == []))
        checks.append(("part-2b-severity-vocab-pinned",
                       tuple(hook.SEVERITIES) == ("error", "warning", "note")))

        # codex QA #1996 MED-3: exercise the D14 fail-closed BRANCH itself (not just the pure fn), by
        # patching the module-global resolve_working to a temp ledger and calling main(). Removing the
        # `if misfiled: return 1` branch in main would flip rc_misfiled to 0 and fail this check.
        _mod = sys.modules[__name__]
        _saved_rw = _mod.resolve_working
        try:
            _mf_led = root / "misfiled-ledger.md"
            _mf_led.write_text(
                "## Disposition values\n"
                "| 2026-09-03 | error | a mis-filed preamble row | probe | FIXED #1 |\n"
                "## Open\n"
                "| Found | Severity | Finding | Source | Disposition |\n"
                "| --- | --- | --- | --- | --- |\n"
                "## Closed today\n",
                encoding="utf-8")
            _mod.resolve_working = lambda _name: _mf_led
            _rc_misfiled = main(["check-class-attestation-on-pr.py"])
            _clean_led = root / "clean-ledger.md"
            _clean_led.write_text(
                "## Open\n"
                "| Found | Severity | Finding | Source | Disposition |\n"
                "| --- | --- | --- | --- | --- |\n"
                "## Closed today\n",
                encoding="utf-8")
            _mod.resolve_working = lambda _name: _clean_led
            _rc_clean = main(["check-class-attestation-on-pr.py"])
        finally:
            _mod.resolve_working = _saved_rw
        checks.append(("part-2b-D14-branch-fails-closed-on-misfiled", _rc_misfiled == 1))
        checks.append(("part-2b-D14-branch-passes-a-clean-ledger", _rc_clean == 0))

    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"check-class-attestation-on-pr self-test: FAIL {bad}")
        return 1
    print(f"check-class-attestation-on-pr self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--floor", default=None,
                    help="override the ship-floor date (YYYY-MM-DD); default "
                         f"{SHIP_FLOOR.isoformat()}")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in self-test on constructed fixtures and exit")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    floor = datetime.date.fromisoformat(args.floor) if args.floor else SHIP_FLOOR

    ledger = resolve_working("open-findings.md")
    if ledger is None:
        print("D14 class-completeness attestation: no open-findings ledger resolvable "
              "(public CI / adopter clone); nothing to check (exit 0).")
        return 0

    try:
        hook = _load(REPO_ROOT / HOOK_REL, "block_on_open_findings_for_d14")
        matcher = _load(REPO_ROOT / MATCHER_REL, "check_class_completeness_for_d14")
    except Exception as exc:
        print(f"D14 FAIL (fail-closed): cannot load the grammar/matcher module ({exc}).",
              file=sys.stderr)
        return 2

    try:
        ledger_text = ledger.read_text(encoding="utf-8")
        rows_full = hook.parse_dispositioned_rows_full(ledger_text)
    except Exception as exc:
        print(f"D14 FAIL (fail-closed): cannot read/parse {ledger} ({exc}).",
              file=sys.stderr)
        return 2

    # P-1.70 part-2b: mis-filed finding-row detector (fail-closed). A finding-row (date|severity|-
    # leading, column 0, not fenced/backtick-quoted) that sits OUTSIDE '## Open' / '## Closed today'
    # is invisible to this gate AND the open-findings hook (the 2026-09-05 legend-splice corruption).
    # UNWINDOWED, deliberately: a row's LOCATION is not a permanent property like its Found date, so
    # the ship floor does not apply (windowing on the Found cell of a mis-filed row would trust a cell
    # the corruption context taints, the same reasoning that removed in_window from the malformed
    # branch). RESIDUE: a fused-onto-prose or severity-mangled row escapes the fingerprint (stated in
    # the hook fn; a strict subset of the class, ACCEPTED).
    misfiled = hook.misfiled_finding_rows(ledger_text)
    if misfiled:
        print(f"D14 FAIL (fail-closed): {len(misfiled)} finding-row(s) mis-filed OUTSIDE "
              f"'## Open' / '## Closed today' in {ledger} (invisible to the hook and D14). "
              "Move each into a scanned section:", file=sys.stderr)
        for _ln, _sec, _line in misfiled[:8]:
            print(f"  - line {_ln} (under {_sec or 'no scanned heading'}): {_line[:100]}",
                  file=sys.stderr)
        return 1

    try:
        files = matcher.attest_file_set()
    except Exception as exc:
        print(f"D14 FAIL (fail-closed): cannot enumerate the git-tracked corpus file set "
              f"({exc}); the reproduce-probe must count over the same set the attestation "
              f"counted over.", file=sys.stderr)
        return 2

    def probe(token: str):
        occ, skipped = matcher.find_occurrences([token], files)
        return len(occ[token]), occ[token], skipped

    failures, notes = evaluate(rows_full, hook, probe, floor)
    for n in notes:
        print(f"  note: {n}")
    if failures:
        print(f"D14 class-completeness attestation: {len(failures)} failure(s):",
              file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("D14 class-completeness attestation: OK "
          f"(floor {floor.isoformat()}, {len(files)} git-tracked corpus files in the probe set)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
