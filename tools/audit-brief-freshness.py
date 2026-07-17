#!/usr/bin/env python3
"""Advisory cross-repo freshness report for the staged worker briefs (TODO
section 4.4 slice 3; design of record: .working/design-decisions.md
"Worker-ready brief staging" and .working/multi-session-orchestration.md
subsection 5.1).

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID, not an audit gate.
The staged worker briefs live in the SIBLING repository ``grc_library_scratch``
(``research/<work-unit-id>/brief.md`` plus the ``research/COVERAGE.md`` index),
each stamped ``Verified-against: grc_library PR #N (<sha>), <date> UTC``.
Neither repository's CI can see the other, so no CI gate can check cross-repo
freshness; the check is orchestrator-side by design ("advisory cross-repo
freshness check", the settled slice-1 design). This tool produces that report:

  1. INDEX AGE: the coverage index's stamp PR number versus this repo's newest
     merged PR number on ``origin/main`` (merge-squash subjects carry ``(#N)``).
     The design's advisory refresh threshold is 15-20 PRs behind; the report
     flags at 15 (ADVISORY, not an error).
  2. DEAD TARGET PATHS: every path bullet in every staged brief's
     ``## Target paths`` section is checked against this repo's ``origin/main``
     tree; a path that no longer exists means the brief drifted (a rename or
     deletion landed after the stamp) and its work-unit needs a targeted
     re-verify before any worker picks it up.
  3. DEAD TODO ANCHORS: every ``research/COVERAGE.md`` row's section anchor
     (``§N.M``, or an ``SR-N`` id for the scratch-reference rows) is checked
     against a live ``### N.M `` / ``### SR-N `` heading in ``TODO.md``; a dead
     anchor means a TODO renumber or close landed without the paired coverage
     sync (the close-out pairing line in .claude/CLAUDE.md is the convention
     this mechanizes a report for).

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the
four-surface parity gate 35, the regression suite gate 36) does NOT
auto-discover it, and it is NOT wired into ``run_all_audits.sh`` /
``quality.yml`` / ``.pre-commit-config.yaml``. It always exits 0: its findings
are refresh-queue candidates for the orchestrator (the targeted-first refresh
of the affected rows), never workflow failures. Making it a blocking gate
would be a decorative gate (gate-discipline rule) because the scratch checkout
is not guaranteed present in every environment. When the scratch checkout is
absent the tool says so and exits 0 (an advisory tool must not manufacture a
failure out of its own optional input). Its self-test lives behind
``--self-test`` (inline unittest on the parsers) rather than in ``tests/`` so
the gate-36 regression runner does not adopt it as a gated test.

Usage:
  python3 tools/audit-brief-freshness.py [--scratch PATH] [--self-test]

The scratch checkout is located by ``--scratch``, else the
``GRC_SCRATCH_PATH`` environment variable, else the sibling directory
``../grc_library_scratch`` relative to this repository's root.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from lint_common import resolve_sibling, sibling_placeholder_present

REPO_ROOT = Path(__file__).resolve().parent.parent

STAMP_RE = re.compile(
    r'^\*\*Verified-against:\*\* grc_library PR #(\d+) \([0-9a-f]{7,40}\), '
    r'\d{4}-\d{2}-\d{2} UTC\s*$', re.M)
MERGE_PR_RE = re.compile(r'\(#(\d+)\)')
PATH_BULLET_RE = re.compile(r'^- `([^`]+\.(?:md|py|sh|yml|yaml|csv))`', re.M)
SECTION_ANCHOR_RE = re.compile(r'§(\d+\.\d+)')
SR_ANCHOR_RE = re.compile(r'\bSR-(\d+)\b')
ADVISORY_PRS_BEHIND = 15


def find_scratch(cli_path):
    """Resolve the scratch checkout path, or None if not found.

    An EXPLICITLY named path (--scratch or GRC_SCRATCH_PATH) that does not
    resolve is reported and NOT silently substituted with the sibling default:
    a report attributed to a checkout the operator did not name is worse than
    no report.
    """
    for label, cand in (("--scratch", cli_path),
                        ("GRC_SCRATCH_PATH", os.environ.get("GRC_SCRATCH_PATH"))):
        if cand:
            if Path(cand).is_dir() and (Path(cand) / "research").is_dir():
                return Path(cand)
            print(f"advisory: {label}={cand} is not a scratch checkout with a "
                  "research/ tree; not falling back to any other location; "
                  "nothing to report.")
            sys.exit(0)
    # Default: the real grc_library_scratch sibling, via the shared resolver
    # (TODO section 1.19.2). None on a portable clone with no scratch sibling.
    default = resolve_sibling("scratch")
    if default is not None and (default / "research").is_dir():
        return default
    return None


def newest_main_pr():
    """Newest merged PR number on origin/main, from squash-merge subjects."""
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "log", "--format=%s", "-40",
         "origin/main"],
        capture_output=True, text=True, check=True).stdout
    nums = [int(m.group(1)) for m in MERGE_PR_RE.finditer(out)]
    return max(nums) if nums else None


def path_on_main(path):
    """True when the path exists in the origin/main tree."""
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), "cat-file", "-e",
         f"origin/main:{path}"],
        capture_output=True).returncode == 0


def stamp_pr(text):
    """The stamp's PR number, or None when the stamp is missing/malformed."""
    m = STAMP_RE.search(text)
    return int(m.group(1)) if m else None


def brief_target_paths(text):
    """Path bullets of the brief's ``## Target paths`` section."""
    m = re.search(r'## Target paths\n(.*?)\n## ', text, re.S)
    return PATH_BULLET_RE.findall(m.group(1)) if m else []


def todo_anchors():
    """Live ``### N.M`` and ``### SR-N`` heading anchors in TODO.md."""
    todo = (REPO_ROOT / "TODO.md").read_text(errors="replace")
    sections = set(re.findall(r'^### (\d+\.\d+)\s', todo, re.M))
    srs = set(re.findall(r'^### (SR-\d+)\s', todo, re.M))
    return sections, srs


def run_report(scratch):
    findings = []
    tip = newest_main_pr()
    cov_path = scratch / "research" / "COVERAGE.md"
    cov_text = cov_path.read_text(errors="replace") if cov_path.exists() else ""

    # 1. index age
    idx_pr = stamp_pr(cov_text)
    if idx_pr is None:
        findings.append("[index] research/COVERAGE.md: index-level stamp "
                        "missing or malformed")
    elif tip is not None:
        behind = tip - idx_pr
        state = ("ADVISORY: refresh sync recommended"
                 if behind >= ADVISORY_PRS_BEHIND else "within threshold")
        print(f"index age: stamped at PR #{idx_pr}, main tip PR #{tip} "
              f"({behind} PR(s) behind; {state})")
        if behind >= ADVISORY_PRS_BEHIND:
            findings.append(f"[index] coverage index is {behind} PRs behind "
                            f"main (threshold {ADVISORY_PRS_BEHIND})")

    # 2. dead target paths per brief
    briefs = sorted(scratch.glob("research/*/brief.md"))
    dead = 0
    for b in briefs:
        text = b.read_text(errors="replace")
        for p in brief_target_paths(text):
            if not path_on_main(p):
                dead += 1
                findings.append(f"[brief] {b.parent.name}: target path no "
                                f"longer on origin/main: {p}")
    print(f"target paths: {len(briefs)} staged brief(s) checked; "
          f"{dead} dead path(s)")

    # 3. dead TODO anchors per coverage row
    sections, srs = todo_anchors()
    rows = [ln for ln in cov_text.splitlines()
            if ln.startswith("| ") and "TODO item (stable id" not in ln]
    dead_anchor = 0
    for row in rows:
        first_cell = row.split("|")[1]
        sec = SECTION_ANCHOR_RE.search(first_cell)
        sr = SR_ANCHOR_RE.search(first_cell)
        if sec and sec.group(1) not in sections:
            dead_anchor += 1
            findings.append(f"[coverage] row anchor §{sec.group(1)} has no "
                            f"live TODO heading: {first_cell.strip()}")
        elif sr and f"SR-{sr.group(1)}" not in srs:
            dead_anchor += 1
            findings.append(f"[coverage] row anchor SR-{sr.group(1)} has no "
                            f"live TODO heading: {first_cell.strip()}")
    print(f"coverage anchors: {len(rows)} row(s) checked; "
          f"{dead_anchor} dead anchor(s)")

    if findings:
        print(f"\n{len(findings)} advisory finding(s) (refresh-queue "
              "candidates, not failures):")
        for f in findings:
            print("  -", f)
    else:
        print("\nadvisory report clean: no refresh candidates.")


def self_test():
    import unittest

    class Parsers(unittest.TestCase):
        def test_stamp(self):
            good = ("**Verified-against:** grc_library PR #618 "
                    "(7499075), 2026-07-03 UTC")
            self.assertEqual(stamp_pr(good), 618)
            self.assertIsNone(stamp_pr(good.replace(" UTC", "")))
            self.assertIsNone(stamp_pr("**Verified-against:** grc_library "
                                       "PR #<N> (<sha>), <date> UTC"))

        def test_target_paths(self):
            brief = ("## Target paths\n\n- `a/b.md`\n- `tools/c.py` "
                     "(read-only)\n\n## Partition\n")
            self.assertEqual(brief_target_paths(brief),
                             ["a/b.md", "tools/c.py"])

        def test_anchor_regexes(self):
            self.assertEqual(
                SECTION_ANCHOR_RE.search("Item, §2.10 ").group(1), "2.10")
            self.assertEqual(
                SR_ANCHOR_RE.search("SR-3 validate.py binary-scan gaps").group(1),
                "3")

        def test_merge_pr(self):
            self.assertEqual(MERGE_PR_RE.findall("x (#618)\ny (#51)"),
                             ["618", "51"])

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Parsers))
    return 0 if result.wasSuccessful() else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", help="path to the grc_library_scratch checkout")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline parser self-test and exit")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return self_test()

    scratch = find_scratch(args.scratch)
    if scratch is None:
        if sibling_placeholder_present("scratch"):
            print("advisory: grc_library_scratch sibling absent (portable clone; "
                  ".scratch placeholder present); maintainer-only advisory, "
                  "nothing to report.")
        else:
            print("advisory: no scratch checkout found (no --scratch or "
                  "GRC_SCRATCH_PATH given, and no sibling grc_library_scratch "
                  "directory with a research/ tree); nothing to report.")
        return 0

    run_report(scratch)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
