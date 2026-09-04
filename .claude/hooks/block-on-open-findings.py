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

CLASS-COMPLETENESS ATTESTATION (P-1.67, advisory here). A Finding cell that LEADS with a
bracketed class token names a CLASS of defect, so its FIXED disposition must attest the fix
was checked at the width of the class: a `[class: "<token>" @ <count>]` clause (emitted by
tools/check-class-completeness.py --attest) or a `[class-exempt: <reason>]` from a closed
set. A FIXED class row missing the attestation is SURFACED AS A WARNING here, never a block
(preserving this hook's fail-open posture); the fail-closed half is the pre-push D14 check
(tools/check-class-attestation-on-pr.py), which also REPRODUCES the probe.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LEDGER_REL = ".working/open-findings.md"
BLOCKING_CMDS = (("gh", "pr", "create"), ("gh", "pr", "merge"))


# `.working/` -> `_private` migration: resolve the (maintainer-only) working-state file through
# lint_common.resolve_working (private sibling preferred, in-repo fallback). Fail-SAFE: if the
# helper cannot be imported, fall back to the historical in-repo path so this hook never breaks.
_TOOLS_DIR = str(Path(__file__).resolve().parents[2] / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from lint_common import resolve_working as _resolve_working
except Exception:  # pragma: no cover - fail-safe: never let a helper-load failure break the hook
    _resolve_working = None


def _working_file(rel_below, root):
    """`.working/<rel_below>` resolved via lint_common (private preferred), or None."""
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root)
    cand = root / ".working" / rel_below
    return cand if cand.exists() else None


def project_root() -> Path:
    # Derived from this file's location, never hardcoded, so the guard follows a repo relocation
    # (the row-E lesson from the /home/grc move, where five hooks kept a stale absolute root).
    return Path(__file__).resolve().parents[2]


def _parse_rows_full(text: str, section_prefixes: tuple) -> list:
    """PURE. Rows of the `## Open` table as (found, severity, finding, disposition).

    Scoped to the `## Open` section so the `## Closed today` table cannot block anything, and so a
    row is retired simply by moving it, which is the cheapest possible disposition action.

    Two robustness properties (3.126 (closing PR #1209)). (1) Columns are split on UNESCAPED pipes, so a cell may
    carry a literal `|` written as `\\|` without shifting the columns. (2) A row whose column count
    is NOT the well-formed five yields `disposition = None`, which the caller treats as
    undispositioned (fail closed), rather than silently reading a middle fragment as the disposition,
    the #1208 defect where an unescaped `| Operation | read/write |` in a Finding cell shifted the
    columns and a valid `**FIXED #1208**` row was mis-read as undispositioned (there in the
    false-BLOCK direction; the general fix makes the parser answer honestly either way).
    """
    rows = []
    in_scope = False
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line.strip().lower()
            in_scope = any(heading.startswith(pfx) for pfx in section_prefixes)
            continue
        if not in_scope or not line.startswith("|"):
            continue
        parts = re.split(r"(?<!\\)\|", line.strip())
        cells = [c.strip() for c in parts]
        if cells and cells[0] == "":          # drop the empty cell the leading border pipe makes
            cells = cells[1:]
        if cells and cells[-1] == "":         # and the trailing one
            cells = cells[:-1]
        if not cells or cells[0].lower() == "found" or all(set(c) <= {"-"} for c in cells):
            continue                          # header row or the `--- | --- | ...` delimiter
        if len(cells) == 5:
            rows.append((cells[0], cells[1].lower(), cells[2], cells[4]))
        else:
            # MALFORMED (wrong column count, e.g. an unescaped `|` shifted the columns). We cannot
            # trust ANY cell, INCLUDING the severity: an early-column pipe makes the severity read as
            # something other than `error`, so the row would escape the error check entirely (codex
            # verify-3126 false-pass). Force it to a blocking error with no disposition so it fails
            # closed regardless of what the shifted cells happen to say. The Found cell is equally
            # untrustworthy, so it is BLANKED: a consumer that windows on the Found date (the D14
            # ship-floor) must treat an unknown date as in-window, never as exempt.
            finding = (cells[2] if len(cells) > 2 else line.strip())[:120]
            rows.append(("", "error", finding, None))
    return rows


def parse_open_rows_full(text: str) -> list:
    """PURE. Rows of the `## Open` table as (found, severity, finding, disposition).
    Open-only, so the `## Closed today` archive never affects the undispositioned-blocking
    path (the hook blocks only on `## Open`)."""
    return _parse_rows_full(text, ("## open",))


def parse_dispositioned_rows_full(text: str) -> list:
    """PURE. Rows of BOTH `## Open` and `## Closed today` as 4-tuples, for the D14
    class-completeness reproduce-check. A FIXED class row is DISPOSITIONED the moment it is
    fixed and, per this hook's own guidance, MOVED to `## Closed today` in the same PR; a
    D14 that scanned only `## Open` would therefore miss exactly the rows it exists to
    verify (the move-to-Closed evasion, gemini QA #1989). The dynamic ship floor in D14
    keeps this from retro-failing archived pre-mechanization rows."""
    return _parse_rows_full(text, ("## open", "## closed today"))


def parse_open_rows(text: str) -> list:
    """PURE. The (severity, finding, disposition) projection of ``parse_open_rows_full``
    (the shape every pre-P-1.67 consumer reads; the D14 pre-push check reads the 4-tuple
    form because its ship-date floor needs the Found cell)."""
    return [(s, f, d) for (_found, s, f, d) in parse_open_rows_full(text)]


# The disposition GRAMMAR (3.126 (closing PR #1209), maintainer-decided 2026-07-27). The closed vocabulary is
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
# A ref is a PR number (`#1`.., never `#0`), a backlog item (`3.73`, `3.56a`, `3.139.1`), or a
# `TODO`-qualified item. `(` or `[` may sit immediately before it (a parenthesized or link-form ref).
_REF = r"[(\[]?(?:#[1-9]\d*|TODO\s+\d+(?:\.\d+)+[a-z]?|\d+(?:\.\d+)+[a-z]?)"
_DISPOSITION_RE = re.compile(
    r"^(?:fixed|routed)\s+" + _REF + r"(?:\b|[.,;:)\]])"   # FIXED/ROUTED + adjacent ref
    r"|^(?:refuted|accepted)\b",                            # REFUTED/ACCEPTED + prose (word only)
    re.IGNORECASE,
)


def disposition_valid(cell: str) -> bool:
    """PURE. Does the Disposition cell carry a well-formed terminal disposition (3.126 grammar)?

    Inline markup (`*`, `_`, `` ` ``, and markdown-link brackets `[` `]`) is removed FIRST, so the
    documented "whitespace OR markup between the word and the ref" holds: `**FIXED** #1178`,
    `` FIXED `#1178` ``, `FIXED **#1208**`, `FIXED [#1208](url)`, and `**ROUTED** 3.56a` all validate
    (claude + codex verify-3126). A colon between the word and the ref (`ROUTED: 3.56a`, `FIXED: #1210`)
    is normalized to whitespace too (3.149 (closing PR #1341)), since the ledger writes some dispositions with a colon. The ref shapes carry none of those characters, so removing them is
    lossless for the match. Returns False for an empty cell, a bare terminal word with no adjacent
    ref, a narration that merely mentions a ref later (`FIXED in #1208`: `in` sits between), a `#0`
    PR ref, and any non-vocabulary prose (`pending`, `OPEN: ...`)."""
    plain = re.sub(r"[*_`\[\]]", "", cell)
    # 3.149 (closing PR #1341): a colon separating the keyword from the ref (`ROUTED: 3.56a`, `FIXED: #1210`) is a
    # SEPARATOR, not markup, and the ref shapes carry no colon, so normalizing it to whitespace is
    # lossless and lets the adjacent-ref grammar match. The REFUTED/ACCEPTED word-only branch (which
    # already tolerates a trailing colon via `\b`) is unaffected.
    plain = plain.replace(":", " ").strip()
    return bool(_DISPOSITION_RE.match(plain))


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


# --- Class-completeness attestation grammar (P-1.67) -------------------------------------
# The recurring class this consumes: "fix the cited instance, miss the siblings". A Finding
# cell that LEADS with a bracketed class token (`[R1-APPI] ...`, `[held-branch-discrepancy]
# ...`) names a CLASS of defect, so a FIXED disposition on it must attest the fix was checked
# at the width of the class, not the one cited instance. Exactly one of:
#   [class: "<distinctive-token>" @ <count>]  the corpus-wide completeness probe ran; the
#       clause is emitted by tools/check-class-completeness.py --attest, and <count> is the
#       occurrence count over the git-tracked corpus set at attest time, the attested state
#       the pre-push D14 check REPRODUCES (it fails on growth or a coverage escape).
#   [class-exempt: <reason>]                  no textual class exists to probe; the reason
#       comes from the CLOSED set below (an open reason field would be a free-prose bypass,
#       the same failure the 3.126 disposition grammar closed).
# GUARD-INPUT NOTE: the token is AUTHOR-DECLARED, never derived from the finding prose. The
# prose has no authority to answer "which distinctive string identifies this class", so a
# derived token would feed the guard an input that cannot answer the question asked of it.
# The machinery verifies the DECLARED probe reproduces; relatedness judgement stays the
# author's, encoded as the count. This hook only WARNS on a missing/invalid attestation
# (fail-open, matching its posture); the fail-closed enforcement is D14.
CLASS_TOKEN_RE = re.compile(r"^\[([A-Za-z0-9][A-Za-z0-9_.-]*)\](?!\()")
CLASS_ATTEST_RE = re.compile(r'\[class:\s*"([^"\r\n]+)"\s*@\s*(\d+)\s*\]', re.IGNORECASE)
CLASS_EXEMPT_REASONS = ("singleton", "non-textual", "cross-repo")
CLASS_EXEMPT_RE = re.compile(r"\[class-exempt:\s*([^\]]+?)\s*\]", re.IGNORECASE)
_FIXED_WORD_RE = re.compile(r"^\s*fixed\b", re.IGNORECASE)


def leading_class_token(finding: str) -> str | None:
    """PURE. The bracketed class token a Finding cell LEADS with, or None.

    Identifier-shaped only (letters, digits, `_`, `.`, `-`; no spaces or colons), so a
    `[class: ...]` clause, bracketed prose, and a leading markdown link (`[text](url)`,
    excluded by the `](` lookahead) never trigger. Leading only: a bracket mid-cell
    classifies nothing."""
    m = CLASS_TOKEN_RE.match(finding.strip())
    return m.group(1) if m else None


def is_fixed_disposition(cell: str) -> bool:
    """PURE. A VALID (3.126) disposition whose terminal word is FIXED: the only
    disposition that owes a class attestation (ROUTED carries the class question to the
    routed item; REFUTED/ACCEPTED fix nothing)."""
    if not disposition_valid(cell):
        return False
    plain = re.sub(r"[*_`\[\]]", "", cell).replace(":", " ").strip()
    return bool(_FIXED_WORD_RE.match(plain))


def class_attestation_state(cell: str) -> str:
    """PURE. 'class' | 'exempt' | 'bad-exempt' | 'multi' | 'none' for a Disposition cell.

    Matches the RAW cell (F1, codex QA #1989 iter-2): the `[class: ...]` / `[class-exempt: ...]`
    clause is delimited by its own brackets, so emphasis markup AROUND it never interferes,
    and stripping `*`/`_`/backtick FIRST would (a) corrupt a token that contains one and (b)
    NORMALIZE an invalid exempt reason into a valid one (`sing_leton` -> `singleton`,
    `non-*textual` -> `non-textual`), a false pass. The exempt reason must be matched exactly
    as written so an off-set reason returns 'bad-exempt' and refuses."""
    # Enforce the ledger's "exactly one clause per row" rule (codex QA #1989 iter-3): count
    # ALL class and exempt clauses. Any malformed exempt reason fails closed with precedence,
    # so a valid class clause cannot mask an invalid exemption in the same cell; more than one
    # clause of any kind is 'multi' (rejected); zero is 'none'.
    class_clauses = CLASS_ATTEST_RE.findall(cell)
    exempt_reasons = CLASS_EXEMPT_RE.findall(cell)
    if any(r.lower() not in CLASS_EXEMPT_REASONS for r in exempt_reasons):
        return "bad-exempt"
    total = len(class_clauses) + len(exempt_reasons)
    if total != 1:
        return "multi" if total > 1 else "none"
    return "class" if class_clauses else "exempt"


def extract_class_attestation(cell: str):
    """PURE. (token, attested_count) from the first `[class: "<token>" @ <count>]` clause,
    or None. A literal `|` is written `\\|` inside a table cell, so it is unescaped here
    (the emit side, --attest, performs the matching escape)."""
    m = CLASS_ATTEST_RE.search(cell)  # RAW cell (F1): never strip inside the token
    if not m:
        return None
    return m.group(1).replace("\\|", "|"), int(m.group(2))


def fixed_class_rows_unattested(rows: list) -> list:
    """PURE. (severity, finding, disposition) rows FIXED on a class-token finding with no
    valid attestation: the clause is missing entirely, or the class-exempt reason falls
    outside the closed set (ignorance REFUSES rather than permits)."""
    return [
        (s, f, d)
        for (s, f, d) in rows
        if d is not None
        and is_fixed_disposition(d)
        and leading_class_token(f)
        and class_attestation_state(d) not in ("class", "exempt")
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

    ledger = _working_file("open-findings.md", project_root())
    try:
        rows = parse_open_rows(ledger.read_text(encoding="utf-8"))
    except Exception:
        return 0  # fail-open (a None/missing/unreadable ledger), per the docstring

    errs = undispositioned(rows, "error")
    if not errs:
        warns = undispositioned(rows, "warning")
        if warns:
            print(f"NOTE ({len(warns)} undispositioned warning-severity finding(s) in {LEDGER_REL}): "
                  "an in-flight PR may finish, but no NEW work starts until each is dispositioned.",
                  file=sys.stderr)
        una = fixed_class_rows_unattested(rows)
        if una:
            print(
                f"WARNING (class-completeness attestation, P-1.67): {len(una)} FIXED row(s) in "
                f"{LEDGER_REL} lead with a bracketed class token but carry no "
                '[class: "<token>" @ <count>] or [class-exempt: <reason>] clause. Run '
                'python3 tools/check-class-completeness.py --attest "<distinctive-token>" and '
                "paste the emitted clause into the Disposition cell, or use [class-exempt: "
                f"{'|'.join(CLASS_EXEMPT_REASONS)}] where no textual class exists. Advisory "
                "here (fail-open); the pre-push D14 check fails closed on it.",
                file=sys.stderr,
            )
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
    # Markup between the word and the ref is admitted (the contract is "whitespace OR markup"):
    # claude + codex verify-3126 flagged bold/backtick/paren/link forms as wrongly rejected.
    ck("bold around just the keyword is valid", disposition_valid("**FIXED** #1178"), True)
    ck("bold around the ref is valid", disposition_valid("FIXED **#1208**"), True)
    ck("a backticked ref is valid", disposition_valid("FIXED `#1178`"), True)
    ck("a parenthesized ref is valid", disposition_valid("FIXED (#1178)"), True)
    ck("a markdown-link ref is valid", disposition_valid("FIXED [#1208](https://x/pr/1208)"), True)
    ck("a dotted three-part item ref is valid", disposition_valid("ROUTED 3.139.1"), True)
    ck("colon-adjacent ROUTED ref is valid (3.149)", disposition_valid("ROUTED: 3.56a"), True)
    ck("colon-adjacent FIXED PR ref is valid (3.149)", disposition_valid("FIXED: #1210"), True)
    ck("colon-no-space ROUTED ref is valid (3.149)", disposition_valid("ROUTED:3.56a"), True)
    ck("ACCEPTED with a colon stays valid (word-only branch, 3.149 regression)", disposition_valid("ACCEPTED: untestable"), True)
    ck("colon does not rescue a non-adjacent ref (3.149)", disposition_valid("FIXED: in #1208 later"), False)
    ck("a stray leading colon before a genuine disposition is benign-valid (3.149)", disposition_valid(":FIXED #1208"), True)
    ck("a '#0' PR ref is INVALID (no real PR is #0)", disposition_valid("FIXED #0"), False)

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
    # An EARLY-column unescaped pipe shifts the SEVERITY too, so without forcing a malformed row to
    # a blocking error it reads as severity `injected` and escapes the error check (codex verify-3126
    # false-pass reality fixture).
    early = ("## Open\n"
             "| Found | Severity | Finding | Source | Disposition |\n"
             "| --- | --- | --- | --- | --- |\n"
             "| 2026-07-25 | injected | error | a confirmed defect | probe | |\n")
    ck("an early-column pipe (mis-read severity) still fails closed",
       len(undispositioned(parse_open_rows(early), "error")), 1)

    # --- P-1.67 class-completeness attestation grammar (unit level) ----------------
    ck("a leading class token is recognized", leading_class_token("[R1-APPI] a wrong value"), "R1-APPI")
    ck("a hyphenated class token is recognized",
       leading_class_token("[held-branch-discrepancy] stale row"), "held-branch-discrepancy")
    ck("a mid-cell bracket is not a class token", leading_class_token("fixed the [R1] case"), None)
    ck("a leading markdown link is not a class token",
       leading_class_token("[a link](https://example.org) prose"), None)
    ck("a class clause is not itself a class token",
       leading_class_token('[class: "x" @ 1] prose'), None)
    ck("bracketed prose with spaces is not a class token",
       leading_class_token("[not a token] prose"), None)
    ck("an attest clause is recognized",
       class_attestation_state('FIXED #1 [class: "180-day baseline" @ 2]'), "class")
    ck("an attest clause survives emphasis markup",
       class_attestation_state('**FIXED #1** [class: "x y" @ 0]'), "class")
    ck("a closed-set exemption is recognized",
       class_attestation_state("FIXED #1 [class-exempt: singleton]"), "exempt")
    ck("an off-set exemption reason is bad-exempt (refuses, never permits)",
       class_attestation_state("FIXED #1 [class-exempt: too-hard]"), "bad-exempt")
    ck("F1: an underscore in an exempt reason does NOT normalize to a valid reason",
       class_attestation_state("FIXED #1 [class-exempt: sing_leton]"), "bad-exempt")
    ck("F1: a star in an exempt reason does NOT normalize to a valid reason",
       class_attestation_state("FIXED #1 [class-exempt: non-*textual]"), "bad-exempt")
    ck("F1: a valid closed-set reason still classifies exempt",
       class_attestation_state("FIXED #1 [class-exempt: cross-repo]"), "exempt")
    ck("iter3: a class clause plus an invalid exempt is bad-exempt (precedence)",
       class_attestation_state('FIXED #1 [class: "never-present" @ 0] [class-exempt: sing_leton]'), "bad-exempt")
    ck("iter3: two valid exempt clauses are multi (exactly-one rule)",
       class_attestation_state("FIXED #1 [class-exempt: singleton] [class-exempt: cross-repo]"), "multi")
    ck("iter3: a class clause plus a valid exempt is multi (exactly-one rule)",
       class_attestation_state('FIXED #1 [class: "x" @ 1] [class-exempt: singleton]'), "multi")
    ck("iter3: two class clauses are multi",
       class_attestation_state('FIXED #1 [class: "x" @ 1] [class: "y" @ 2]'), "multi")
    ck("no clause is none", class_attestation_state("FIXED #1 then prose"), "none")
    ck("extraction unescapes a table-escaped pipe",
       extract_class_attestation('FIXED #1 [class: "a \\| b" @ 4]'), ("a | b", 4))
    ck("F1: extraction preserves an underscore inside the token",
       extract_class_attestation('FIXED #1 [class: "foo_bar" @ 1]'), ("foo_bar", 1))
    ck("F1: extraction preserves asterisk and backtick inside the token",
       extract_class_attestation('FIXED #1 [class: "a*b`c" @ 2]'), ("a*b`c", 2))
    ck("F1: an underscore token still detected as a class attestation",
       class_attestation_state('**FIXED #1** [class: "foo_bar" @ 1]'), "class")
    ck("FIXED is the attesting disposition", is_fixed_disposition("FIXED #1178"), True)
    ck("ROUTED owes no attestation", is_fixed_disposition("ROUTED 3.56a"), False)
    ck("an invalid bare FIXED is not an attesting disposition", is_fixed_disposition("FIXED"), False)

    attn = ("## Open\n"
            "| Found | Severity | Finding | Source | Disposition |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 2026-09-04 | warning | [CE3-CASP] cited instance fixed, class unchecked | probe | FIXED #1984 |\n"
            '| 2026-09-04 | warning | [R1-APPI] classed and attested | probe | FIXED #1985 [class: "publicly available data" @ 2] |\n'
            "| 2026-09-04 | note | [one-off] no textual class | probe | FIXED #1986 [class-exempt: non-textual] |\n"
            "| 2026-09-04 | warning | [E9] routed class | probe | ROUTED TODO 3.73 |\n"
            "| 2026-09-04 | warning | unclassed finding | probe | FIXED #1987 |\n"
            "| 2026-09-04 | warning | [bad-reason] off-set exemption | probe | FIXED #1988 [class-exempt: too-hard] |\n")
    urows = fixed_class_rows_unattested(parse_open_rows(attn))
    uflagged = [f for (_s, f, _d) in urows]
    ck("an unattested FIXED class row is flagged",
       any(f.startswith("[CE3-CASP]") for f in uflagged), True)
    ck("an off-set exemption is flagged",
       any(f.startswith("[bad-reason]") for f in uflagged), True)
    ck("attested, exempt, routed and unclassed rows are not flagged", len(urows), 2)
    full = parse_open_rows_full(attn)
    ck("the full parse carries the Found cell", full[0][0], "2026-09-04")
    ck("the projection matches the full parse", parse_open_rows(attn),
       [(s, f, d) for (_fd, s, f, d) in full])

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
