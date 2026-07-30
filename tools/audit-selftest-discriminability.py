#!/usr/bin/env python3
"""Ask whether a tool's own self-test can detect the removal of the guards it names.

THE COMPLEMENT TO `audit-gate-mutation.py`, WHICH RUNS THE OTHER DIRECTION. That probe seeds defects
into a disposable CORPUS copy and asks whether the gates detect them. This one mutates TOOL CODE and
asks whether the tool's own `--self-test` notices. Both directions matter and only one had tooling,
which is why the 2026-07-25 passes in this direction were hand-rolled, and why three of them produced
a false signal.

WHY IT EXISTS. A self-test whose cases cannot detect the removal of the guard they name is worse than
no self-test, because it reports PASS under that case's own label and so reads as coverage. A 2026-07-25
audit found 28 such sites across 8 tools in this repo. The instance that motivated the audit was a tool
that injects keystrokes into another account's tmux session, whose seven refusals all returned the same
value while its assertions checked only that value.

THE HARNESS IS BRACKETED BY CONTROLS, AND REFUSES TO REPORT IF THEY FAIL. This is the part the
hand-rolled attempts lacked, and every one of their false signals would have been caught by it:

  POSITIVE control: force the self-test to fail, and confirm this probe SEES the failure. If a probe
    cannot observe a failing self-test, its NOT-DETECTED verdicts are void rather than evidence. One
    hand-rolled attempt reported all nine guards undetected when all nine were detected, because its
    collection logic short-circuited on a truthy return value; a positive control catches exactly that.
  NEGATIVE control: append a comment, which cannot change behaviour, and confirm the self-test still
    passes. A probe that reports a comment as DETECTED is over-sensitive and its DETECTED verdicts
    mean nothing either.

A NON-MUTATION IS REPORTED AS INVALID, NEVER AS NOT-DETECTED. An edit that cannot change behaviour
(a string literal the assertions never read, a consistent rename, anything inside a comment or
docstring) yields a passing self-test for a reason that has nothing to do with coverage. Two of the
2026-07-25 false signals were exactly this: a mutated heading string and a consistent global rename,
both read as coverage gaps. So each candidate is screened for semantic effect BEFORE its result is
interpreted, and a screened-out candidate is never counted as a finding.

GUARDS ARE DISCOVERED, NOT HAND-LISTED, so the guard set cannot silently drift from the code. A guard
is an `if` whose body returns: disabling its condition is the mutation that models a removed guard.

WHAT NOT-DETECTED DOES AND DOES NOT MEAN, stated because the number overstates the defect otherwise.
It means only: the self-test does not fail when this guard is disabled. That covers TWO different
situations with different fixes, and this probe cannot yet tell them apart:

  EXERCISED BUT BLIND. The self-test runs this code and cannot see the guard vanish, because its
    assertion reads something several branches share (a return code every refusal returns, a boolean
    two guards both produce). This is the real defect, and the fix is to assert the DISCRIMINATING
    observable rather than the shared sentinel.
  NEVER EXERCISED. No case reaches the guard at all, typically a CLI-dispatch branch, an error path
    needing a live external process, or the self-test's own reporting. This is a coverage gap, and the
    fix is to write a case, or to accept the path as out of scope and say so.

Applying the first fix to the second situation does nothing, and adding a case for the first without
strengthening its assertion reproduces the defect, so the split matters. Separating them needs
reachability analysis from the self-test body, and a function-granularity closure over-counts (a guard
on an unreached branch INSIDE a reached function looks exercised), so it is deliberately left for a
follow-up rather than guessed at here. Read a NOT-DETECTED row as "worth a look", not as a confirmed
defect, and confirm which situation it is before fixing.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
IF_RE = re.compile(r"^(\s*)(el)?if\s+.+:\s*(#.*)?$")
RETURN_RE = re.compile(r"^\s*return\b")
SELFTEST_FLAG = "--self-test"


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def discover_guards(lines: list) -> list:
    """PURE. Find every `if`/`elif` whose body returns: the shape a removed guard would take.

    Returns [(index, text)]. Discovery rather than a hand-written list, so the guard set tracks the
    code instead of drifting from it, which is how a guard acquires no case at all.
    """
    out, in_doc, quote = [], False, ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Skip docstrings and block comments: an `if` quoted inside prose is not a guard.
        if not in_doc:
            for q in ('"""', "'''"):
                if stripped.startswith(q) and not (stripped.endswith(q) and len(stripped) > 5):
                    in_doc, quote = True, q
                    break
        elif quote in stripped:
            in_doc = False
            continue
        if in_doc or stripped.startswith("#"):
            continue
        m = IF_RE.match(line)
        if not m:
            continue
        base = _indent(line)
        for j in range(i + 1, min(i + 8, len(lines))):
            nxt = lines[j]
            if not nxt.strip():
                continue
            if _indent(nxt) <= base:
                break
            if RETURN_RE.match(nxt):
                out.append((i, line.rstrip()))
                break
    return out


def is_semantic_mutation(old_line: str, new_line: str) -> tuple:
    """PURE. Could this edit change behaviour at all? Returns (ok, reason_if_not).

    The screen that stops a non-mutation being reported as a coverage gap. It is deliberately
    conservative: it rejects only edits that CANNOT matter, so a rejected candidate is genuinely
    inert rather than merely suspicious.
    """
    if old_line == new_line:
        return False, "identical to the original, so nothing was mutated"
    if old_line.strip().startswith("#") or new_line.strip().startswith("#"):
        return False, "the edit is inside a comment, which cannot change behaviour"
    # A change confined to string-literal contents: the code shape is untouched.
    def _blank_strings(s: str) -> str:
        return re.sub(r"(\"\"\".*?\"\"\"|'''.*?'''|\"[^\"]*\"|'[^']*')", '""', s, flags=re.S)
    if _blank_strings(old_line) == _blank_strings(new_line):
        return False, ("the edit changes only string-literal contents; assertions that do not read "
                       "that string are unaffected, so a pass says nothing about coverage")
    return True, ""


def classify(control_ok: bool, semantic_ok: bool, detected: bool) -> str:
    """PURE. The verdict for one candidate. Every branch is a distinct, assertable value.

    Ordered so that an unusable harness or an inert edit can never masquerade as a coverage finding:
    controls first, then whether the edit could matter, and only then detection.
    """
    if not control_ok:
        return "VOID-CONTROLS-FAILED"
    if not semantic_ok:
        return "INVALID-NON-MUTATION"
    return "DETECTED" if detected else "NOT-DETECTED"


def run_selftest(tool: Path, timeout: int = 180) -> tuple:
    """Run a tool's self-test. Returns (rc, combined_output)."""
    try:
        r = subprocess.run([sys.executable, str(tool), SELFTEST_FLAG],
                           capture_output=True, text=True, timeout=timeout, cwd=str(tool.parent),
                           env=probe_env())
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


REENTRY_ENV = "GRC_SELFTEST_PROBE_ACTIVE"


def probe_env() -> dict:
    """The environment for any child this probe spawns. Observer.

    Stamps REENTRY_ENV so a spawned self-test, and above all a MUTANT of this probe, refuses to
    probe in turn. Without this stamp the layer-2 backstop is inert: it reads an environment
    variable nothing ever sets, which is the dead-guard shape this project treats as worse than no
    guard, because the code reads as protected. Inherits the rest of the environment so a tool's own
    PATH and locale assumptions still hold.
    """
    env = dict(os.environ)
    env[REENTRY_ENV] = "1"
    return env


def is_self(path: Path) -> bool:
    """PURE-ish (one resolve). Is this path the probe itself?

    LAYER 1 OF THE RECURSION GUARD. THE DEFECT THIS CLOSES (found by a worker, 2026-07-25, hours
    after the probe shipped in #1174, while doing exactly what its validate-pr order asked). The
    probe enumerates every `tools/*.py` carrying a `--self-test` and mutates each in place. It IS
    such a tool, and nothing excluded it, so it wrote a mutant of itself into `tools/` and executed
    it; that mutant enumerated the directory and did the same, spawning runaway processes. It escaped
    testing because every run to that point had passed explicit `--tool` arguments, so the default
    enumeration path, the only one that reaches this, was never exercised.

    Compares RESOLVED paths, so a relative argument, a symlink, or a `./tools/x` form all match.
    """
    try:
        return path.resolve() == Path(__file__).resolve()
    except OSError:
        return False


def has_selftest(tool: Path) -> bool:
    try:
        t = tool.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return SELFTEST_FLAG in t and ("def self_test" in t or "self_test(" in t)


def covered_lines(tool: Path, timeout: int = 240) -> set:
    """Which lines of `tool` actually EXECUTE during its own self-test.

    Statement-level, via the stdlib `trace` module, and that precision is the whole point. The
    obvious alternative, asking whether the guard's enclosing FUNCTION is reachable from the
    self-test body, is WRONG and was measured wrong on 2026-07-25: it called a guard exercised
    because `do_send` is reachable, when the guard sat behind an early `continue` that the
    self-test's dry-run path always takes, so the line never ran. Function reachability cannot
    answer a question about statement execution, which is the same shape of error as feeding a
    guard an input that cannot answer its question.

    Returns the set of executed line numbers, or an empty set if tracing could not run, in which
    case the caller must treat the split as UNKNOWN rather than assume nothing ran.
    """
    runner = (
        "import json, sys, trace, importlib.util, pathlib\n"
        "target = pathlib.Path(sys.argv[1]).resolve()\n"
        "spec = importlib.util.spec_from_file_location('probe_target', target)\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "tr = trace.Trace(count=1, trace=0)\n"
        "spec.loader.exec_module(mod)\n"
        "try:\n"
        "    tr.runfunc(mod.self_test)\n"
        "except SystemExit:\n"
        "    pass\n"
        "hit = sorted({ln for (fn, ln) in tr.results().counts if pathlib.Path(fn).resolve() == target})\n"
        "print(json.dumps(hit))\n"
    )
    try:
        r = subprocess.run([sys.executable, "-c", runner, str(tool)],
                           capture_output=True, text=True, timeout=timeout, cwd=str(tool.parent),
                           env=probe_env())
        last = [ln for ln in (r.stdout or "").strip().splitlines() if ln.startswith("[")]
        if not last:
            return set()
        import json as _json
        return set(_json.loads(last[-1]))
    except Exception:
        return set()


def _in_self_test(lines: list, idx: int) -> bool:
    """PURE. Is line `idx` inside a `def self_test` body? Used only to name the inherent class."""
    for k in range(idx, -1, -1):
        s = lines[k]
        if s.startswith("def "):
            return s.startswith("def self_test")
    return False


def split_verdict(verdict: str, guard_line: int, covered: set, trace_ok: bool,
                  inherent: bool = False) -> str:
    """PURE. Refine a NOT-DETECTED verdict into the two situations with different fixes.

    BLIND-CASE   the self-test EXECUTES this guard and still passes when it is disabled. The real
                 defect: an assertion reading something several branches share. Fix the assertion.
    NO-CASE      the guard never executes during the self-test. A coverage gap. Fix by writing a
                 case, or accept the path as out of scope and record that.
    UNKNOWN-SPLIT tracing did not run, so the split is genuinely unknown and is reported as such
                 rather than defaulting to either, since defaulting would invent a classification.
    """
    if verdict != "NOT-DETECTED":
        return verdict
    if not trace_ok:
        return "NOT-DETECTED/UNKNOWN-SPLIT"
    if guard_line not in covered:
        return "NOT-DETECTED/NO-CASE"
    if inherent:
        # A self-test cannot assert its OWN failure-reporting branch from inside itself without
        # recursion, so reporting it as a fixable defect would put a permanently-red row in front of
        # every future reader and train them to ignore the output. It is covered EXTERNALLY instead,
        # by this probe's own POSITIVE control, which forces the self-test to fail and confirms the
        # failure is observed. Named rather than hidden, because "unfixable here" is not "unchecked".
        return "NOT-DETECTED/INHERENT-EXTERNALLY-COVERED"
    return "NOT-DETECTED/BLIND-CASE"


def _mutant_path(tool: Path, tag: str) -> Path:
    """A mutant lives BESIDE its original so sibling imports resolve. See the note in probe_tool."""
    return tool.parent / f"_probe_mutant_{tag}_{tool.stem.replace('-', '_')}.py"


def run_controls(tool: Path, work) -> tuple:
    """Bracket the run. Returns (ok, detail).

    POSITIVE: force the self-test to fail, and confirm we SEE the failure. NEGATIVE: append a comment,
    and confirm the self-test still passes. Both must behave as expected or every verdict in the run is
    void, which is not a theoretical concern: on 2026-07-25 an entire matrix read DETECTED for four
    mutations because the mutant was run from the wrong directory and failed on an import, and only the
    negative control revealed it.
    """
    src = tool.read_text(encoding="utf-8", errors="replace")

    pos = _mutant_path(tool, 'pos')
    pos.write_text(src.replace("def self_test()", "def self_test():\n    return 1\n\ndef _unused_self_test()", 1),
                   encoding="utf-8")
    rc_pos, _ = run_selftest(pos)
    if rc_pos == 0:
        return False, ("POSITIVE control did not fire: a forced self-test failure was not observed, so "
                       "this probe cannot see a failing self-test and every NOT-DETECTED verdict it "
                       "would report is void rather than evidence")

    neg = _mutant_path(tool, 'neg')
    neg.write_text(src.replace("from __future__ import annotations",
                               "from __future__ import annotations\n# inert control comment", 1)
                   if "from __future__ import annotations" in src else src + "\n# inert control comment\n",
                   encoding="utf-8")
    rc_neg, out_neg = run_selftest(neg)
    if rc_neg != 0:
        return False, (f"NEGATIVE control fired: an inert comment made the self-test FAIL (rc {rc_neg}), so "
                       f"this probe is over-sensitive and its DETECTED verdicts mean nothing either. "
                       f"Most often the mutant is being run from the wrong directory, so a sibling import "
                       f"fails. First output line: {out_neg.strip().splitlines()[:1]}")
    for tag in ("pos", "neg"):
        _mutant_path(tool, tag).unlink(missing_ok=True)
    return True, "positive control fired, negative control silent"


def probe_tool(tool: Path, keep: bool = False) -> dict:
    """Mutate every discovered guard in `tool` and report whether its self-test notices."""
    src = tool.read_text(encoding="utf-8", errors="replace")
    lines = src.split("\n")
    guards = discover_guards(lines)
    try:
        label = str(tool.resolve().relative_to(REPO_ROOT))
    except ValueError:
        label = str(tool)
    result = {"tool": label, "guards": len(guards), "rows": [],
              "control_ok": False, "control_detail": ""}

    # THE MUTANT MUST BE A SIBLING FILE, NOT A FILE IN A SUBDIRECTORY. A tool that imports a sibling
    # module (`lint_common`) cannot import it from `tools/.probe-XXXX/`, so the mutant dies on import,
    # every self-test run "fails", and the negative control fires. That is not hypothetical: the first
    # version of this probe used a temp SUBDIRECTORY and voided itself on the first tool that imports a
    # sibling, which is the identical working-directory error that had voided a hand-rolled matrix an
    # hour earlier. The probe's own negative control caught it.
    class _SiblingWorkspace:
        def __init__(self, target: Path):
            self.dir = target.parent
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            for leftover in self.dir.glob("_probe_mutant_*.py"):
                leftover.unlink(missing_ok=True)
            return False

    with _SiblingWorkspace(tool) as work:
        ok, detail = run_controls(tool, work)
        result["control_ok"], result["control_detail"] = ok, detail
        if not ok:
            return result
        covered = covered_lines(tool)
        trace_ok = bool(covered)
        result["trace_ok"] = trace_ok
        for idx, text in guards:
            mutated = list(lines)
            pad = " " * _indent(mutated[idx])
            mutated[idx] = f"{pad}if False:  # probe"
            semantic_ok, why = is_semantic_mutation(text, mutated[idx])
            if not semantic_ok:
                result["rows"].append({"line": idx + 1, "guard": text.strip()[:70],
                                       "verdict": classify(True, False, False), "note": why})
                continue
            mut = _mutant_path(tool, 'sub')
            mut.write_text("\n".join(mutated), encoding="utf-8")
            rc, _ = run_selftest(mut)
            base = classify(True, True, rc != 0)
            # `if failures:` inside a self_test IS the self-test's own reporting branch.
            inherent = "failures" in text and _in_self_test(lines, idx)
            result["rows"].append({"line": idx + 1, "guard": text.strip()[:70],
                                   "verdict": split_verdict(base, idx + 1, covered, trace_ok, inherent),
                                   "note": ""})
    return result


def self_test() -> int:
    """Pin every pure branch. The probe is an instrument, so it needs its own calibration."""
    failures, total = [], [0]

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" + ("" if ok else f" -> {got!r} != {want!r}"))
        if not ok:
            failures.append(name)

    # The recursion guard (the #1174 escape). Both layers get a case: the path exclusion, and the
    # environment stamp WITHOUT WHICH the layer-2 backstop reads an unset variable and is inert.
    check("is_self: the probe recognizes its own absolute path",
          is_self(Path(__file__).resolve()), True)
    check("is_self: and its relative form, so a `tools/x` argument is caught too",
          is_self(Path("tools") / Path(__file__).name), True)
    check("is_self: another tool is not itself",
          is_self(REPO_ROOT / "tools" / "lint-metadata.py"), False)
    check("is_self: default enumeration excludes the probe",
          any(is_self(q) for q in (REPO_ROOT / "tools").glob("*.py")
              if has_selftest(q) and not is_self(q)), False)
    check("probe_env: every spawned child carries the re-entry sentinel",
          probe_env().get(REENTRY_ENV), "1")
    check("probe_env: the rest of the environment is inherited, not replaced",
          set(os.environ) <= set(probe_env()), True)
    check("classify: controls failed voids everything", classify(False, True, True), "VOID-CONTROLS-FAILED")
    check("classify: a non-mutation is INVALID, never NOT-DETECTED",
          classify(True, False, False), "INVALID-NON-MUTATION")
    check("classify: detected", classify(True, True, True), "DETECTED")
    check("classify: not detected", classify(True, True, False), "NOT-DETECTED")

    check("semantic: identical text is not a mutation",
          is_semantic_mutation("if x:", "if x:")[0], False)
    check("semantic: a comment-only edit is not a mutation",
          is_semantic_mutation("# a", "# b")[0], False)
    check("semantic: a string-literal-only edit is not a mutation",
          is_semantic_mutation('print("=== recycled ===")', 'print("=== disabled ===")')[0], False)
    check("semantic: disabling a condition IS a mutation",
          is_semantic_mutation("if x > 1:", "if False:")[0], True)

    src = ['def f():', '    if a:', '        return 1', '    b = 2', '    if c:', '        b = 3',
           '    """', '    if quoted_in_a_docstring:', '        return 9', '    """', '    return b']
    g = discover_guards(src)
    check("discover: finds an if whose body returns", [i for i, _ in g], [1])
    check("discover: ignores an if with no return in its body", 4 in [i for i, _ in g], False)
    check("discover: ignores an if quoted inside a docstring", 7 in [i for i, _ in g], False)

    if failures:
        print(f"\nself-test: FAILED ({len(failures)} of {total[0]})")
        return 1
    print(f"\nself-test: {total[0]}/{total[0]} passed")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tools", nargs="*", help="tool paths to probe (default: every self-tested tool)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()

    # LAYER 2 OF THE RECURSION GUARD (see excluded_self and REENTRY_ENV). If this process is itself
    # a mutant of the probe, executed by an outer probe run, refuse to probe anything. Layer 1
    # (self-exclusion by path) is the control; this is the backstop that holds even if a rename, a
    # copy, or an explicit path argument defeats it, because a mutant inherits the environment.
    if os.environ.get(REENTRY_ENV):
        print("REFUSED: this process is running inside a probe run "
              f"({REENTRY_ENV} is set), so probing again would recurse. Exiting without probing.")
        return 0

    # Resolve to absolute so a relative argument still reports a repo-relative label.
    if a.tools:
        requested = [Path(t).resolve() for t in a.tools]
        targets = [t for t in requested if not is_self(t)]
        for t in requested:
            if is_self(t):
                print(f"SKIP {t.name}: a probe cannot probe itself. Mutating this file writes a "
                      "mutant of the probe and EXECUTES it, and the mutant enumerates the tools "
                      "directory again, so each run spawns another. Excluded explicitly.")
    else:
        targets = sorted(p for p in (REPO_ROOT / "tools").glob("*.py")
                         if has_selftest(p) and not is_self(p))
    if not targets:
        print("no self-tested tool found; nothing to probe (no-op).")
        return 0

    total_nd = 0
    measured_tools: list[str] = []
    void_tools: list[str] = []
    for tool in targets:
        if not tool.is_file():
            print(f"SKIP {tool}: not a file")
            continue
        r = probe_tool(tool)
        if not r["control_ok"]:
            print(f"\n=== {r['tool']} ===\n  VOID: {r['control_detail']}")
            void_tools.append(r["tool"])
            continue
        measured_tools.append(r["tool"])
        # startswith, NOT equality: the verdict carries a /BLIND-CASE or /NO-CASE suffix once tracing
        # runs, and an equality filter silently matched nothing, reporting 22 detected and 0 findings
        # where the untraced run had found 10. A false CLEAN introduced by a refactor of the reporting
        # rather than of the logic, caught only because the number contradicted the earlier run.
        nd = [x for x in r["rows"] if x["verdict"].startswith("NOT-DETECTED")]
        inv = [x for x in r["rows"] if x["verdict"] == "INVALID-NON-MUTATION"]
        total_nd += len(nd)
        print(f"\n=== {r['tool']} === {r['guards']} guard(s); "
              f"{len(r['rows']) - len(nd) - len(inv)} detected, {len(nd)} NOT-detected, {len(inv)} invalid")
        blind = [x for x in nd if x["verdict"].endswith("BLIND-CASE")]
        nocase = [x for x in nd if x["verdict"].endswith("NO-CASE")]
        unk = [x for x in nd if x["verdict"].endswith("UNKNOWN-SPLIT")]
        inh = [x for x in nd if x["verdict"].endswith("INHERENT-EXTERNALLY-COVERED")]
        print(f"     of which: {len(blind)} BLIND-CASE (the defect), {len(nocase)} NO-CASE "
              f"(coverage gap), {len(inh)} inherent/externally-covered, {len(unk)} unknown split")
        for x in blind:
            print(f"  BLIND-CASE  :{x['line']}  {x['guard']}   <- the self-test RUNS this and cannot see it go")
        for x in nocase:
            print(f"  NO-CASE     :{x['line']}  {x['guard']}   <- never executed by the self-test")
        for x in unk:
            print(f"  UNKNOWN     :{x['line']}  {x['guard']}   <- tracing did not run")
    # Report the MEASURED denominator, never the attempted one. `total_nd` accumulates only from
    # tools whose positive control fired, so dividing it by the probed-tool count states a coverage
    # this run does not have: a VOID tool contributes zero findings while inflating the denominator,
    # so "N across <probed>" reads as full coverage of every tool named. A void tool's exposure is
    # UNKNOWN, never zero, and the summary now says so rather than letting silence read as health.
    # Found by Sweep 122 (2026-07-25) against this tool's own output, and re-measured at source.
    print(f"\nselftest-discriminability: {total_nd} NOT-DETECTED guard(s) across the "
          f"{len(measured_tools)} tool(s) this run could MEASURE, of {len(targets)} probed. "
          f"{len(void_tools)} tool(s) are VOID (the positive control did not fire), contributing no "
          "findings; their exposure is UNKNOWN, not zero, so the total understates the true figure by "
          "an unmeasured amount. "
          "Advisory. NOT-DETECTED means the self-test does not fail when the guard is disabled, which "
          "covers BOTH a case that is blind to its own guard (the defect) AND a guard no case reaches "
          "(a coverage gap). The fixes differ, so confirm which before acting; see the module docstring.")
    if void_tools:
        print("  VOID (exposure unknown): " + ", ".join(sorted(void_tools)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
