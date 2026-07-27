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

    Two robustness properties (TODO 3.126). (1) Columns are split on UNESCAPED pipes, so a cell may
    carry a literal `|` written as `\\|` without shifting the columns. (2) A row whose column count
    is NOT the well-formed five yields `disposition = None`, which the caller treats as
    undispositioned (fail closed), rather than silently reading a middle fragment as the disposition,
    the #1208 defect where an unescaped `| Operation | read/write |` in a Finding cell shifted the
    columns and a valid `**FIXED #1208**` row was mis-read as undispositioned (there in the
    false-BLOCK direction; the general fix makes the parser answer honestly either way).
    """
    rows = []
    in_open = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_open = line.strip().lower().startswith("## open")
            continue
        if not in_open or not line.startswith("|"):
            continue
        parts = re.split(r"(?<!\\)\|", line.strip())
        cells = [c.strip() for c in parts]
        if cells and cells[0] == "":          # drop the empty cell the leading border pipe makes
            cells = cells[1:]
        if cells and cells[-1] == "":         # and the trailing one
            cells = cells[:-1]
        if not cells or cells[0].lower() == "found" or all(set(c) <= {"-"} for c in cells):
            continue                          # header row or the `--- | --- | ...` delimiter
        sev = cells[1].lower() if len(cells) > 1 else ""
        finding = cells[2] if len(cells) > 2 else ""
        disp = cells[4] if len(cells) == 5 else None   # None == malformed -> fail closed downstream
        rows.append((sev, finding, disp))
    return rows


# The disposition GRAMMAR (TODO 3.126, maintainer-decided 2026-07-27). The closed vocabulary is
# still the four words, but a bare terminal WORD is no longer enough: an earlier check only asked
# that the cell START with one of them, so `ROUTED nowhere yet, it smells like 3.145 territory` and
# even a lone `FIXED` passed while saying nothing checkable. Two rules close that, and they differ by
# disposition because the ledger's own legend does:
#   - FIXED / ROUTED must carry a REF ADJACENT to the word (whitespace or markup only between):
#     `FIXED #1178`, `ROUTED TODO 3.73`. The ref is what a reader follows to confirm the claim, and
#     requiring it adjacent (not scanned-for past arbitrary prose) is what makes the cell answer
#     "where did this go?" rather than merely mention a number somewhere. Prose may follow the ref.
#   - REFUTED / ACCEPTED carry PROSE (the legend defines `REFUTED <evidence>` / `ACCEPTED <rationale>`),
#     so only the terminal WORD is machine-required; the evidence/rationale is author judgement.
# A ref is a PR number (`#1178`), a backlog item (`3.73`, `3.56a`), or a `TODO`-qualified item.
TERMINAL = ("fixed", "routed", "refuted", "accepted")
_REF = r"(?:#\d+|TODO\s+\d+\.\d+[a-z]?|\d+\.\d+[a-z]?)"
_DISPOSITION_RE = re.compile(
    r"^(?:fixed|routed)\s+" + _REF + r"(?:\b|[.,;:)])"   # FIXED/ROUTED + adjacent ref
    r"|^(?:refuted|accepted)\b",                           # REFUTED/ACCEPTED + prose (word only)
    re.IGNORECASE,
)


def disposition_valid(cell: str) -> bool:
    """PURE. Does the Disposition cell carry a well-formed terminal disposition (3.126 grammar)?

    Leading markup (`**`, `` ` ``, `_`, spaces) is stripped first, so `**FIXED #1208**` still counts.
    Returns False for an empty cell, a bare terminal word with no adjacent ref (FIXED/ROUTED), a
    narration that merely mentions a ref later (`FIXED in #1208` fails: `in` sits between), and any
    non-vocabulary prose (`pending`, `OPEN: ...`)."""
    return bool(_DISPOSITION_RE.match(cell.strip().lstrip("*_` ")))


def undispositioned(rows: list, severity: str) -> list:
    """PURE. Rows of `severity` whose Disposition cell is not a well-formed terminal disposition.

    This is the guard-input-authority class the project fixed three times elsewhere: the check was
    correct, and its input (a free-prose cell) could not answer the question asked of it. The 3.126
    grammar makes the cell able to answer it, and makes ignorance (a bare word, a narration, a
    mentioned-but-not-adjacent ref) REFUSE rather than permit. A row that arrives MALFORMED from the
    parser (`disposition is None`, e.g. an unescaped `|` shifted its columns) is treated as
    undispositioned here, so a mis-columned row fails closed rather than silently mis-reading a
    middle fragment as the disposition (the #1208 pipe-in-cell defect)."""
    return [
        (s, f, d)
        for (s, f, d) in rows
        if s == severity and not (d is not None and disposition_valid(d))
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

    # --- 3.126 grammar: the disposition_valid vocabulary + adjacent-ref rule (unit level) -----
    ck("FIXED + adjacent ref is valid", disposition_valid("FIXED #1178"), True)
    ck("bold FIXED + adjacent ref is valid", disposition_valid("**FIXED #1208** then prose"), True)
    ck("ROUTED + adjacent TODO ref is valid", disposition_valid("ROUTED TODO 3.73, P1 tier"), True)
    ck("ROUTED + adjacent bare item ref is valid", disposition_valid("ROUTED 3.56a (residual)"), True)
    ck("FIXED with a NON-adjacent ref is INVALID", disposition_valid("FIXED in #1208: the branch"), False)
    ck("ROUTED narration with a later ref is INVALID",
       disposition_valid("ROUTED nowhere yet, it smells like 3.145 territory"), False)
    ck("a bare FIXED with no ref is INVALID", disposition_valid("FIXED"), False)
    ck("REFUTED + prose is valid (word only, per legend)",
       disposition_valid("REFUTED by the maintainer, 2026-07-26"), True)
    ck("ACCEPTED + prose is valid (word only, per legend)",
       disposition_valid("ACCEPTED: structurally untestable in place"), True)
    ck("an empty cell is INVALID", disposition_valid(""), False)
    ck("a bare 'pending' is INVALID", disposition_valid("pending"), False)
    ck("an 'OPEN:' narration is INVALID", disposition_valid("OPEN: a fresh worker is requested"), False)

    # Same shapes at the row level: exactly the three narrations/bare-words block, the four
    # well-formed rows do not. This is the reality fixture for the false-pass class 3.126 closes:
    # `ROUTED nowhere ... 3.145` and `FIXED in #1208` LOOK dispositioned to the old startswith test.
    vocab = ("## Open\n"
             "| Found | Severity | Finding | Source | Disposition |\n"
             "| --- | --- | --- | --- | --- |\n"
             "| 2026-07-25 | error | narrated-open | probe | OPEN: a fresh worker is requested |\n"
             "| 2026-07-25 | error | routed-narration | probe | ROUTED nowhere yet, near 3.145 |\n"
             "| 2026-07-25 | error | fixed-nonadjacent | probe | **FIXED** in #1178 |\n"
             "| 2026-07-25 | error | fixed-adjacent | probe | FIXED #1178 then prose |\n"
             "| 2026-07-25 | error | routed-ok | probe | ROUTED TODO 3.73 |\n"
             "| 2026-07-25 | error | refuted-prose | probe | REFUTED, the maintainer confirmed |\n"
             "| 2026-07-25 | error | accepted-prose | probe | accepted: recorded decision |\n")
    vopen = [f for (_s, f, _d) in undispositioned(parse_open_rows(vocab), "error")]
    ck("OPEN: narration blocks", "narrated-open" in vopen, True)
    ck("ROUTED narration (non-adjacent ref) blocks", "routed-narration" in vopen, True)
    ck("FIXED with a non-adjacent ref blocks", "fixed-nonadjacent" in vopen, True)
    ck("FIXED with an adjacent ref does not block", "fixed-adjacent" in vopen, False)
    ck("ROUTED with an adjacent ref does not block", "routed-ok" in vopen, False)
    ck("REFUTED + prose does not block", "refuted-prose" in vopen, False)
    ck("ACCEPTED + prose does not block", "accepted-prose" in vopen, False)
    ck("exactly the three narrations block", len(vopen), 3)

    # --- 3.126 pipe-robustness: a literal `|` in a cell (the #1208 reality fixture) -----------
    # An UNESCAPED pipe in the Finding cell shifts the columns; the row becomes malformed
    # (disposition None) and fails CLOSED (blocks) rather than mis-reading a middle fragment.
    piped = ("## Open\n"
             "| Found | Severity | Finding | Source | Disposition |\n"
             "| --- | --- | --- | --- | --- |\n"
             "| 2026-07-25 | error | a cell with a raw | pipe inside | probe | FIXED #9 |\n"
             "| 2026-07-25 | error | a cell with an escaped \\| pipe | probe | FIXED #9 |\n")
    prows = parse_open_rows(piped)
    pmalformed = [d for (_s, _f, d) in prows]
    ck("an unescaped-pipe row is malformed (disposition None)", pmalformed[0], None)
    ck("only the unescaped-pipe row fails closed (blocks); the escaped one does not",
       len(undispositioned(prows, "error")), 1)
    ck("an escaped-pipe row parses to a valid disposition",
       pmalformed[1] is not None and disposition_valid(pmalformed[1]), True)

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
