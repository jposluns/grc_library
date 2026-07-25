#!/usr/bin/env python3
"""PreToolUse: refuse to open or merge a PR while a confirmed defect sits undispositioned.

WHY THIS IS A HOOK AND NOT A CONVENTION. The convention existed and failed twice in one day on the
same axis. Its scope hole was that "a delivered QA result blocks progress" covered findings arriving
FROM WORKERS and said nothing about findings the orchestrator generates ITSELF; on 2026-07-25 two live
defects in a file-moving tool, produced by the orchestrator's own probe minutes earlier, were rendered
as a table row and walked past in favour of writing a summary statistic about them. Reading a finding
is not acting on one, and the gap between those two is where the cost lives, so the block is
mechanical.

WHAT IT READS. `.working/open-findings.md`, the ledger, whose `## Open` table carries one row per
confirmed defect with a severity and a disposition. A row with an EMPTY disposition is undispositioned.
A row leaves the ledger only via FIXED, ROUTED, REFUTED or ACCEPTED, so "no disposition" is the single
blocking condition and there is no third state to argue about.

WHAT IT BLOCKS. An `error`-severity undispositioned row blocks opening or merging a PR, because
shipping past a known wrong behaviour is the thing worth preventing. A `warning` does not block a PR
(an in-flight change should finish rather than be abandoned half-landed) and is surfaced instead.
Notes never block.

FAIL-OPEN BY DESIGN, AND SAID SO PLAINLY. If the ledger is missing or unparseable this hook ALLOWS the
action, because a guard that blocks all work on its own malfunction would be removed within a day, and
a removed guard protects nothing. That is a deliberate trade recorded here rather than an oversight: the
ledger plus the convention are the primary control and this hook is defence in depth.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LEDGER_REL = ".working/open-findings.md"
BLOCKING_CMDS = (("gh", "pr", "create"), ("gh", "pr", "merge"))


def project_root() -> Path:
    # Derived from this file's location, never hardcoded, so the guard follows a repo relocation
    # (the row-E lesson from the /home/grc move, where five hooks kept a stale absolute root).
    return Path(__file__).resolve().parents[2]


def parse_open_rows(text: str) -> list:
    """PURE. Rows of the `## Open` table as (severity, finding, disposition).

    Scoped to the `## Open` section so the `## Closed today` table cannot block anything, and so a
    row is retired simply by moving it, which is the cheapest possible disposition action.
    """
    rows = []
    in_open = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_open = line.strip().lower().startswith("## open")
            continue
        if not in_open or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0].lower() in ("found", "---") or set(cells[0]) <= {"-"}:
            continue
        rows.append((cells[1].lower(), cells[2], cells[4]))
    return rows


# The closed disposition vocabulary. The ledger's own contract is that a row leaves only via one
# of these four, so anything else in the cell is NOT a disposition however much text it carries.
TERMINAL = ("fixed", "routed", "refuted", "accepted")


def undispositioned(rows: list, severity: str) -> list:
    """PURE. Rows of `severity` carrying no TERMINAL disposition.

    Emptiness is not the right test, and testing it was a live gap: the cell is free prose, so
    `OPEN: still working on it` or `pending` is non-empty and satisfied the old check while saying
    in plain words that the finding is undispositioned. That is the guard-input-authority class the
    project already fixed three times elsewhere: the check was correct, and its input could not
    answer the question asked of it. Requiring one of the four vocabulary words makes the cell able
    to answer it, and makes ignorance refuse rather than permit.
    """
    return [
        (s, f, d)
        for (s, f, d) in rows
        if s == severity and not d.strip().lstrip("*_` ").lower().startswith(TERMINAL)
    ]


def is_blocking_command(cmd: str) -> bool:
    """PURE. Does this shell command open or merge a PR?"""
    flat = " ".join(cmd.split())
    return any(" ".join(parts) in flat for parts in BLOCKING_CMDS)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    if not is_blocking_command(cmd):
        return 0

    ledger = project_root() / LEDGER_REL
    try:
        rows = parse_open_rows(ledger.read_text(encoding="utf-8"))
    except Exception:
        return 0  # fail-open, per the docstring

    errs = undispositioned(rows, "error")
    if not errs:
        warns = undispositioned(rows, "warning")
        if warns:
            print(f"NOTE ({len(warns)} undispositioned warning-severity finding(s) in {LEDGER_REL}): "
                  "an in-flight PR may finish, but no NEW work starts until each is dispositioned.",
                  file=sys.stderr)
        return 0

    lines = [f"BLOCKED (open-findings guard): {len(errs)} error-severity finding(s) in {LEDGER_REL} "
             "have no disposition, so this PR must not open or merge.", ""]
    for _s, finding, _d in errs[:5]:
        lines.append(f"  - {finding[:150]}")
    lines += ["",
              "A finding that has been READ but not acted on is the most expensive state a defect can "
              "be in, because the record shows it was found and the surface therefore reads as "
              "examined. Give each row a disposition (FIXED / ROUTED / REFUTED / ACCEPTED) and move it "
              "to '## Closed today'. Do NOT write a count or a summary about these first: turning live "
              "defects into a statistic is the specific failure this guard exists to stop."]
    print("\n".join(lines), file=sys.stderr)
    return 2


def self_test() -> int:
    cases, fails = 0, []

    def ck(name, got, want):
        nonlocal cases
        cases += 1
        if got != want:
            fails.append(f"{name}: {got!r} != {want!r}")
        print(f"  {'PASS' if got == want else 'FAIL'}: {name}")

    doc = ("## Open\n"
           "| Found | Severity | Finding | Source | Disposition |\n"
           "| --- | --- | --- | --- | --- |\n"
           "| 2026-07-25 | error | a wrong thing | probe |  |\n"
           "| 2026-07-25 | warning | a lesser thing | probe | FIXED #1 |\n"
           "| 2026-07-25 | warning | an open lesser thing | probe |  |\n"
           "## Closed today\n"
           "| Found | Severity | Finding | Source | Disposition |\n"
           "| 2026-07-25 | error | a closed thing | probe | FIXED #2 |\n")
    rows = parse_open_rows(doc)
    ck("parses only the Open section", len(rows), 3)
    ck("an undispositioned error is found", len(undispositioned(rows, "error")), 1)
    ck("a dispositioned warning does not count", len(undispositioned(rows, "warning")), 1)
    ck("a closed-section error never blocks",
       [f for (_s, f, _d) in undispositioned(rows, "error")], ["a wrong thing"])
    # The reality fixture for the vocabulary gap: these exact cell shapes are non-empty and were
    # accepted by the emptiness test while stating in plain words that nothing had been decided.
    vocab = ("## Open\n"
             "| Found | Severity | Finding | Source | Disposition |\n"
             "| --- | --- | --- | --- | --- |\n"
             "| 2026-07-25 | error | narrated-open | probe | OPEN: a fresh worker is requested |\n"
             "| 2026-07-25 | error | pending-word | probe | pending |\n"
             "| 2026-07-25 | error | really-routed | probe | ROUTED TODO 3.73, P1 tier |\n"
             "| 2026-07-25 | error | bolded-fixed | probe | **FIXED** in #1178 |\n"
             "| 2026-07-25 | error | lowercase-accepted | probe | accepted: recorded decision |\n")
    vrows = parse_open_rows(vocab)
    vopen = [f for (_s, f, _d) in undispositioned(vrows, "error")]
    ck("an OPEN: narration is NOT a disposition", "narrated-open" in vopen, True)
    ck("a bare 'pending' is NOT a disposition", "pending-word" in vopen, True)
    ck("ROUTED counts as dispositioned", "really-routed" in vopen, False)
    ck("bold markup around FIXED still counts", "bolded-fixed" in vopen, False)
    ck("lowercase accepted still counts", "lowercase-accepted" in vopen, False)
    ck("exactly the two narrations block", len(vopen), 2)
    ck("gh pr create blocks", is_blocking_command("cd /x && gh pr create --title y"), True)
    ck("gh pr merge blocks", is_blocking_command("gh pr merge 12 --squash --admin"), True)
    ck("an unrelated command does not block", is_blocking_command("git status --short"), False)
    ck("gh pr checks does not block", is_blocking_command("gh pr checks 12"), False)
    if fails:
        print(f"\nself-test: FAILED ({len(fails)} of {cases})")
        for f in fails:
            print(f"  {f}")
        return 1
    print(f"\nself-test: {cases}/{cases} passed")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
