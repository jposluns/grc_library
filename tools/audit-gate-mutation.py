#!/usr/bin/env python3
"""Gate mutation probe: seed defect variants into a DISPOSABLE repo copy and report
which gates detect them.

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID for the deep-assessment
skill's audit-programme phase, not an audit gate. It probes the WIDTH of each gate's
detection pattern, the property the regression suite (one canonical fixture per rule)
does not exercise: the same defect class in a table cell, inside or outside a fence,
appended to a real corpus document, with separator or phrasing variants, and with
near-miss legitimate content for the false-positive direction.

SAFETY INVARIANT (non-negotiable). The probe REFUSES to run unless ALL THREE hold:
  1. The target directory contains a marker file named ``DISPOSABLE-COPY-OK`` at its
     root. The marker is a DELIBERATE DECLARATION by whoever made the copy; creating
     it on a live checkout defeats the safety by design and is on the creator.
  2. The target does not resolve to (or contain) the repository this tool itself
     lives in (effective once the tool is installed in the repo it protects).
  3. The target's git working tree is CLEAN apart from the marker itself. The probe
     reverts via ``git checkout -- .`` and ``git clean -fd`` after every variant, so
     a dirty tree would lose uncommitted work; refusing dirty trees bounds the worst
     case even when checks 1 and 2 are both satisfied in error.
The expected workflow: copy the repo (including ``.git``, which the revert step
uses) into a scratch location, ``touch DISPOSABLE-COPY-OK`` there, and point
``--target`` at it. Every refusal is a hard exit (code 2), not a warning, so a
mis-typed path cannot mutate a working tree.

Variants live in ``gate-mutation-variants.json`` next to this script (override with
``--variants``). Each variant: ``gate`` (script filename under ``tools/``), ``id``,
``expect`` (``detect`` for a seeded defect the gate should flag; ``clean`` for a
near-miss the gate should NOT flag), and an ``action`` (``append_file`` /
``create_file`` with ``path`` and ``text``). The special path ``@any-corpus-md``
resolves at run time to the first tracked ``.md`` file under a corpus domain
directory, so the library does not hard-code file names that may move.

Verdicts per (gate, variant): ``DETECTED`` (expected defect flagged), ``MISSED``
(expected defect not flagged), ``CLEAN-PASS`` (near-miss correctly ignored),
``FALSE-POSITIVE`` (near-miss flagged), ``BASELINE-DIRTY`` (the gate failed on the
pristine copy, so the variant is unjudgeable). A ``MISSED`` or ``FALSE-POSITIVE``
row is a CANDIDATE finding for the deep-assessment run's adjudication, not a
verdict against the gate: an expectation encodes the variant author's hypothesis
about the gate's intended scope, and adjudication may conclude the variant is out
of scope rather than the gate deficient. The starter library ships variants only
for gates whose detection intent is documented; coverage grows run over run by
extending the JSON.

Usage:
    cp -r /path/to/grc_library /scratch/mutcopy && touch /scratch/mutcopy/DISPOSABLE-COPY-OK
    python3 tools/audit-gate-mutation.py --target /scratch/mutcopy
    python3 tools/audit-gate-mutation.py --target /scratch/mutcopy --gate lint-language.py

Stdlib-only Python 3.11. Exit 0 after printing the report (whatever the verdicts);
exit 2 on the safety refusal or an internal error.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
TOOL_REPO_ROOT = TOOL_DIR.parent
MARKER = "DISPOSABLE-COPY-OK"
CORPUS_DIRS = (
    "ai", "architecture", "compliance", "dev-security", "governance",
    "operations", "privacy", "resilience", "risk", "security", "supply-chain",
)


def refuse(msg: str) -> int:
    print(f"REFUSING to run: {msg}", file=sys.stderr)
    return 2


def safety_check(target: Path) -> str | None:
    """Return an error string if the target is unsafe, else None."""
    if not target.is_dir():
        return f"target is not a directory: {target}"
    if not (target / MARKER).is_file():
        return (
            f"no {MARKER} marker at target root. Create the disposable copy "
            f"deliberately (cp -r <repo> <copy> && touch <copy>/{MARKER}) and "
            f"point --target at the copy. This tool never mutates a live checkout."
        )
    resolved = target.resolve()
    if resolved == TOOL_REPO_ROOT or TOOL_REPO_ROOT.is_relative_to(resolved):
        return (
            f"target resolves to (or contains) this tool's own repository "
            f"({TOOL_REPO_ROOT}); a marker file there does not make it disposable."
        )
    if not (target / ".git").exists():
        return "target has no .git; the revert step needs the copy's git history."
    porcelain = subprocess.run(
        ["git", "-C", str(target), "status", "--porcelain"],
        capture_output=True, text=True,
    )
    if porcelain.returncode != 0:
        return f"git status failed in target: {porcelain.stderr.strip()}"
    dirty = [
        ln for ln in porcelain.stdout.splitlines()
        if ln.strip() and not ln.endswith(MARKER)
    ]
    if dirty:
        return (
            f"target working tree is dirty ({len(dirty)} entr(y/ies), first: "
            f"{dirty[0]!r}); the probe's revert step would destroy uncommitted "
            f"work. Use a fresh copy."
        )
    return None


def run_gate(target: Path, gate: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, f"tools/{gate}"],
        cwd=target,
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout + proc.stderr)[-2000:]


def revert(target: Path) -> None:
    subprocess.run(["git", "-C", str(target), "checkout", "--", "."],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(target), "clean", "-fdq",
                    "--exclude", MARKER],
                   check=True, capture_output=True)


def resolve_path(target: Path, raw: str) -> Path:
    if raw == "@any-corpus-md":
        out = subprocess.run(
            ["git", "-C", str(target), "ls-files", "*.md"],
            capture_output=True, text=True, check=True,
        )
        for rel in out.stdout.splitlines():
            parts = rel.split("/")
            if len(parts) > 1 and parts[0] in CORPUS_DIRS:
                return target / rel
        raise RuntimeError("no corpus .md found for @any-corpus-md")
    p = (target / raw).resolve()
    if not p.is_relative_to(target.resolve()):
        raise RuntimeError(f"variant path escapes the target: {raw}")
    return p


def apply_action(target: Path, action: dict) -> str:
    kind = action["type"]
    path = resolve_path(target, action["path"])
    text = action["text"]
    if kind == "append_file":
        if not path.is_file():
            raise RuntimeError(f"append target missing: {path}")
        with path.open("a", encoding="utf-8") as fh:
            fh.write("\n" + text + "\n")
    elif kind == "create_file":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    else:
        raise RuntimeError(f"unknown action type: {kind}")
    return str(path.relative_to(target.resolve()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Probe gate detection width in a disposable repo copy."
    )
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--variants", type=Path,
                        default=TOOL_DIR / "gate-mutation-variants.json")
    parser.add_argument("--gate", action="append", default=None,
                        help="Limit to the named gate script(s), for example "
                             "lint-language.py. Repeatable.")
    args = parser.parse_args(argv)

    err = safety_check(args.target)
    if err:
        return refuse(err)
    target = args.target.resolve()

    try:
        variants = json.loads(args.variants.read_text(encoding="utf-8"))["variants"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR reading variants: {exc}", file=sys.stderr)
        return 2
    if args.gate:
        wanted = set(args.gate)
        variants = [v for v in variants if v["gate"] in wanted]
    if not variants:
        print("No variants selected; nothing to probe.")
        return 0

    # Pristine baseline per gate, computed once.
    revert(target)
    baseline: dict[str, int] = {}
    for gate in sorted({v["gate"] for v in variants}):
        rc, _ = run_gate(target, gate)
        baseline[gate] = rc

    rows: list[tuple[str, str, str, str]] = []
    counts = {"DETECTED": 0, "MISSED": 0, "CLEAN-PASS": 0,
              "FALSE-POSITIVE": 0, "BASELINE-DIRTY": 0}
    for v in variants:
        gate, vid, expect = v["gate"], v["id"], v["expect"]
        if baseline.get(gate, 1) != 0:
            verdict, detail = "BASELINE-DIRTY", "gate fails on the pristine copy"
        else:
            try:
                where = apply_action(target, v["action"])
                rc, tail = run_gate(target, gate)
                if expect == "detect":
                    verdict = "DETECTED" if rc != 0 else "MISSED"
                else:
                    verdict = "CLEAN-PASS" if rc == 0 else "FALSE-POSITIVE"
                detail = f"{where} (rc={rc})"
                if verdict == "MISSED":
                    detail += "; defect present, gate exit 0"
            except (RuntimeError, subprocess.CalledProcessError) as exc:
                verdict, detail = "BASELINE-DIRTY", f"variant unapplied: {exc}"
            finally:
                revert(target)
        counts[verdict] += 1
        rows.append((gate, vid, verdict, detail))

    print(f"# Gate mutation probe report (target copy: {target})\n")
    print("| Gate | Variant | Verdict | Detail |")
    print("| --- | --- | --- | --- |")
    for gate, vid, verdict, detail in rows:
        print(f"| `{gate}` | {vid} | {verdict} | {detail} |")
    print(
        f"\nSummary: {counts['DETECTED']} detected, {counts['MISSED']} missed, "
        f"{counts['CLEAN-PASS']} clean-pass, {counts['FALSE-POSITIVE']} "
        f"false-positive, {counts['BASELINE-DIRTY']} unjudgeable. MISSED and "
        f"FALSE-POSITIVE rows are CANDIDATE findings for adjudication, not "
        f"verdicts against the gates."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
