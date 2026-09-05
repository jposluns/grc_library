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


# The ledger's closed SEVERITY vocabulary (cell 2 of a finding-row). Widen HERE if a new
# severity is ever added; the D14 self-test pins this set so a silent narrowing is caught.
SEVERITIES = ("error", "warning", "note")
# A finding-row fingerprint (P-1.70 part-2b): date-leading AND severity-second, at column 0.
# The severity screen is what separates a real finding-row from the heterogeneous QA sub-table /
# archive rows that legitimately live OUTSIDE the scanned sections (date-leading but NOT
# severity-second, per the D14 module docstring). `^`-anchored, so a backtick-quoted legend example
# (which starts with a backtick) can never match; a `YYYY-MM-DD` placeholder fails the literal-date.
MISFILED_ROW_RE = re.compile(
    r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*(?:" + "|".join(SEVERITIES) + r")\s*\|",
    re.IGNORECASE,
)


# A scanned heading may carry ONE complete parenthetical decoration and nothing else (codex QA #1996:
# `## Closed today (swept 2026-09) and the row is deleted` must NOT open -- trailing prose after the
# `)` is a phantom-heading tail, and an unclosed `(` is not a decoration either).
_DECORATION_RE = re.compile(r"\([^()]*\)")


def _opens_scanned_section(heading_lower: str, section_prefixes: tuple) -> bool:
    """PURE. Does this `## ` heading (already lower-cased and stripped) OPEN a scanned section?

    Opens only if it prefix-matches a scanned name AND carries no backtick. The backtick screen is
    the P-1.70 phantom-heading fix: the observed corruption spliced a sentence tail beginning with a
    backtick-quoted ``## Closed today` `` at column 0, which prefix-matched and opened a false
    section. CLOSING stays wide (the caller resets scope on ANY `## ` line), so junk pushes rows OUT
    of scope, where the mis-filed-row detector converts the old silence into a loud failure. No real
    SCANNED ledger heading currently carries a backtick, so the exclusion risk is near zero (the live
    ledger's only backtick-bearing heading is a dated ARCHIVE heading, which is not scanned; a
    backtick-free heading that is an EXACT scanned name or carries one COMPLETE `(...)` decoration and
    nothing else opens (`## Open (swept 2026-09)`); trailing prose after the decoration, an unclosed
    `(`, or any backtick does not (codex QA #1996). RESIDUE: a backtick-DECORATED scanned heading
    (e.g. ``## Closed today (`sweep-700`)``) is rejected and its rows flagged LOUDLY, a
    fail-closed FP in the safe direction (never silence), which is the signal to undo the decoration.
    """
    if "`" in heading_lower:
        return False
    for pfx in section_prefixes:
        if heading_lower.startswith(pfx):
            rest = heading_lower[len(pfx):]
            # exact scanned name, or a parenthetical decoration (`## Open (swept 2026-09)`); NOT
            # arbitrary trailing prose (codex QA #1996: a backtick-FREE phantom `## Closed today and
            # the row is deleted` must NOT prefix-match and open a false scanned section).
            rest = rest.strip()
            if rest == "" or _DECORATION_RE.fullmatch(rest):
                return True
    return False


def _fence_run(stripped: str):
    """PURE. If the line begins a code fence, return (char, length) where char is `` ` `` or `~` and
    length is the run of that char (>= 3); else None. CommonMark-aware fence tracking (codex QA
    #1996): the OPENER records its char and length, and a line CLOSES it only when it is the same
    char, at least as long, and bare (no info string). This keeps a `~~~` line inside a ``` fence
    from closing it, AND a three-backtick line inside a four-backtick fence from closing it."""
    for ch in ("`", "~"):
        if stripped.startswith(ch * 3):
            return (ch, len(stripped) - len(stripped.lstrip(ch)))
    return None


def _fence_closes(run, fence, stripped: str) -> bool:
    """PURE. Does this fence-run line CLOSE the open `fence` (char, length)? Same char, length >=
    opener, AND BARE, meaning the run spans the whole stripped line so there is no info string
    (codex/gemini QA #1996: ``` ```python ``` closes nothing; a CommonMark closing fence carries no
    info string). RESIDUE (accepted): four-space-indented and backtick-in-info-string openers are not
    modelled (callers pass ``line.strip()``); the operational ledger uses column-0 bare fences."""
    return (fence is not None and run is not None and run[0] == fence[0]
            and run[1] >= fence[1] and run[1] == len(stripped))


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
    fence = None
    for line in text.splitlines():
        stripped = line.strip()
        run = _fence_run(stripped)
        if fence is not None:
            if _fence_closes(run, fence, stripped):
                fence = None
            continue                      # inside a fence (or the line that closes it): never a row
        if run is not None:
            fence = run
            continue                      # the line that opens a fence
        if line.startswith("## "):
            heading = stripped.lower()
            in_scope = _opens_scanned_section(heading, section_prefixes)
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


def misfiled_finding_rows(text: str, section_prefixes: tuple = ("## open", "## closed today")) -> list:
    """PURE. Finding-rows mis-filed BEFORE the `## Closed today` archive opens (P-1.70 part-2b).

    Returns [(lineno, governing_section_or_None, line), ...] for each column-0, non-fenced line that
    matches ``MISFILED_ROW_RE`` while (a) no scanned section is currently open AND (b) the real
    `## Closed today` section has not yet opened. This catches BOTH the observed 2026-09-05 preamble
    corruption (twelve dispositioned rows spliced into the `## Disposition values` legend, above
    `## Open`) AND a finding-row orphaned by a phantom heading BETWEEN `## Open` and `## Closed today`
    (codex QA #1996: a backtick-quoted `## Closed today` after `## Open` resets the parser's scope but
    must not silently swallow the rows it strands). Shares heading + delimiter-aware fence semantics
    with ``_parse_rows_full`` (both use ``_opens_scanned_section`` and ``_fence_run``), so the
    parser and detector cannot disagree at the phantom-heading or the fenced-heading seam.

    SCOPE (stops once the real `## Closed today` opens, established by the part-2b pre-landing sweep):
    the ledger keeps a large LEGITIMATE archive of old finding-rows under dated `## YYYY-MM-DD ...`
    headings BELOW `## Closed today`, in the SAME `date | severity |` schema (40 rows observed), so a
    row in the post-`## Closed today` archive is indistinguishable from a legitimately-archived one by
    location and is exempt.

    RESIDUES (stated, ACCEPTED): (1) an OPEN (undispositioned) finding-row spliced into the archive
    region escapes this location-based check (a future disposition-aware extension could catch it);
    (2) a row FUSED onto a prose line (not `|`-leading) escapes the `^`-anchor, which is deliberate
    FP-safety (matching mid-prose `| ... |` would flag ordinary tables-in-sentences); (3) the backtick
    screen in ``_opens_scanned_section`` rejects ANY scanned heading carrying a backtick, so a
    backtick-decorated scanned heading (e.g. ``## Closed today (`sweep-700`)``) is rejected and its
    rows are flagged LOUDLY (a fail-closed FP, never silence). No CURRENT scanned heading carries a
    backtick (the live ledger's only backtick-bearing heading is a dated ARCHIVE heading, which is not
    scanned); if a maintainer ever decorates a scanned heading, the loud flag is the signal to undo it.
    """
    out = []
    in_scope = False
    closed_today_opened = False
    fence = None
    current = None
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        run = _fence_run(stripped)
        if fence is not None:
            if _fence_closes(run, fence, stripped):
                fence = None
            continue
        if run is not None:
            fence = run
            continue
        if line.startswith("## "):
            heading = stripped.lower()
            in_scope = _opens_scanned_section(heading, section_prefixes)
            if in_scope and heading.startswith("## closed today"):
                closed_today_opened = True
            current = None if in_scope else stripped
            continue
        if not closed_today_opened and not in_scope and MISFILED_ROW_RE.match(line):
            out.append((i, current, stripped))
    return out


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
    class_spans = [m.span() for m in CLASS_ATTEST_RE.finditer(cell)]
    # Overlap-aware clause counting (P-1.70): a `[class-exempt: ...]` substring INSIDE a
    # `[class: "<token>" @ n]` clause's span is part of that token, not a second clause, so it
    # is not counted again. A genuine standalone clause can never fall inside a class span (the
    # token is `[^"\r\n]+`, which cannot cross a quote), so this is safe-direction: it removes
    # a false 'multi' AND a false 'bad-exempt' for an off-set reason written inside a token
    # (that reason belongs to the author-declared token, and the resulting 'class' still routes
    # to the D14 count-reproduction probe), and never turns a genuinely multi-clause or
    # standalone-bad-exempt cell into a pass.
    # SCOPE NOTE (codex+claude QA #1994; NARROWED by P-1.70 parts 1-2): a MALFORMED `[class:` wrapper
    # (non-numeric count, or a spaced/obfuscated opener) fails CLASS_ATTEST_RE, so class_spans is empty
    # and an embedded `[class-exempt: ...]` is counted standalone -> 'exempt'. Chasing opener-obfuscation
    # with a regex is an unbounded regress, so it is not attempted here. The D14 gate's row-level
    # fail-closed (P-1.70 parts 1-2) catches every case where the wrapper corruption ALSO breaks the
    # row's columns (an unescaped `|` -> cell count != 5). The residue it does NOT catch is the contrived
    # case of a WELL-FORMED 5-col row whose Disposition holds a malformed `[class:` wrapper TOGETHER WITH
    # any valid `[class-exempt: ...]` reason (whether inside the malformed wrapper OR standalone/adjacent
    # in the cell -- a malformed wrapper yields empty class_spans, so CLASS_EXEMPT_RE then matches an
    # adjacent exempt too, gemini QA #1995); that is adversarial-only in this author-run tooling, ACCEPTED.
    exempt_reasons = [
        m.group(1)
        for m in CLASS_EXEMPT_RE.finditer(cell)
        if not any(a <= m.start() and m.end() <= b for (a, b) in class_spans)
    ]
    if any(r.lower() not in CLASS_EXEMPT_REASONS for r in exempt_reasons):
        return "bad-exempt"
    total = len(class_spans) + len(exempt_reasons)
    if total != 1:
        return "multi" if total > 1 else "none"
    return "class" if class_spans else "exempt"


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
        ledger_text = ledger.read_text(encoding="utf-8")
        rows = parse_open_rows(ledger_text)
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
        misfiled = misfiled_finding_rows(ledger_text)
        if misfiled:
            print(
                f"WARNING (mis-filed finding-row, P-1.70 part-2b): {len(misfiled)} finding-row(s) in "
                f"{LEDGER_REL} sit OUTSIDE '## Open' / '## Closed today', so they are invisible to "
                "this hook AND the D14 gate. Move each into a scanned section (or, if a deliberate "
                "archive, its heading must be a scanned one / it must not carry the finding-row "
                "shape):",
                file=sys.stderr,
            )
            for _ln, _sec, _line in misfiled[:5]:
                print(f"  - line {_ln} (under {_sec or 'no scanned heading'}): {_line[:100]}",
                      file=sys.stderr)
            print("Advisory here (fail-open); the pre-push D14 check fails closed on it.",
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
    ck("P-1.70: a [class-exempt: ...] substring INSIDE a class token is not a 2nd clause",
       class_attestation_state('FIXED #1 [class: "the [class-exempt: singleton] literal" @ 3]'), "class")
    ck("P-1.70: a real standalone exempt AFTER a class token is still multi",
       class_attestation_state('FIXED #1 [class: "x [class-exempt: singleton] y" @ 1] [class-exempt: cross-repo]'), "multi")
    ck("P-1.70: an OFF-SET exempt reason INSIDE a valid token is part of the token -> class",
       class_attestation_state('FIXED #1 [class: "x [class-exempt: bogus] y" @ 1]'), "class")
    ck("P-1.70: an off-set exempt inside a token PLUS a real standalone bad exempt is bad-exempt",
       class_attestation_state('FIXED #1 [class: "x [class-exempt: bogus] y" @ 1] [class-exempt: alsobad]'), "bad-exempt")
    ck("P-1.70: a literal [class: opener INSIDE a valid token does not false-block -> class",
       class_attestation_state('FIXED #1 [class: "see [class: nested] here" @ 2]'), "class")
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

    # --- P-1.70 part-2b: mis-filed finding-row detector (reality fixture + negative controls) ----
    # Mirrors the observed corruption: rows spliced into the PREAMBLE legend (above `## Open`), a
    # false backtick-`## ` heading, backtick/fenced/placeholder examples, an in-scope row, and a
    # legitimate dated ARCHIVE row below `## Closed today` (must NOT be flagged: pre-Closed-today scope).
    mf_fixture = (
        "## Disposition values\n"
        "A DISPOSITIONED row is moved to `## Closed today` (an archive), leaving `## Open` open.\n"
        "| 2026-08-31 | warning | a standalone mis-filed row | probe | FIXED #1 |\n"
        "| 2026-09-03 | note | a standalone note row | probe | ROUTED 3.1 |\n"
        "| 2026-09-03 | error | a standalone E9-shape row | probe | FIXED #2 |\n"
        "An inline example `| 2026-09-03 | error | quoted example | probe |  |` stays backticked.\n"
        "| YYYY-MM-DD | error | placeholder example | probe |  |\n"
        "```\n"
        "| 2026-09-03 | error | fenced example row | probe |  |\n"
        "```\n"
        "## Closed today` and the row is deleted from the legend.\n"
        "| 2026-09-03 | error | a row after the phantom heading | probe | FIXED #3 |\n"
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | error | an in-scope open row | probe |  |\n"
        "## Closed today\n"
        "| 2026-09-05 | error | a closed row | probe | FIXED #4 |\n"
        "## 2026-08-24 resume /validate (archived QA record)\n"
        "| 2026-08-24 | error | a legitimately archived row | probe | FIXED #5 |\n"
    )
    mf = misfiled_finding_rows(mf_fixture)
    mf_lines = [ln for (_ln, _sec, ln) in mf]
    ck("part-2b: exactly the 3 preamble + 1 post-phantom rows are flagged", len(mf), 4)
    ck("part-2b: an in-scope Open row is NOT flagged",
       any("an in-scope open row" in x for x in mf_lines), False)
    ck("part-2b: a row in the post-Closed-today archive region is NOT flagged (positional exemption)",
       any("a legitimately archived row" in x for x in mf_lines), False)
    ck("part-2b: a backtick-quoted legend example is NOT flagged (not `|`-leading)",
       any("quoted example" in x for x in mf_lines), False)
    ck("part-2b: a YYYY-MM-DD placeholder is NOT flagged (no literal date)",
       any("placeholder example" in x for x in mf_lines), False)
    ck("part-2b: a fenced example row is NOT flagged",
       any("fenced example row" in x for x in mf_lines), False)
    ck("part-2b: a standalone preamble mis-filed row IS flagged",
       any("a standalone mis-filed row" in x for x in mf_lines), True)
    ck("part-2b: a row after a phantom backtick-heading IS flagged",
       any("after the phantom heading" in x for x in mf_lines), True)
    _parsed = [fi for (_fd, _sv, fi, _d) in parse_dispositioned_rows_full(mf_fixture)]
    ck("part-2b seam: the parser does NOT treat the post-phantom row as in-scope",
       any("after the phantom heading" in fi for fi in _parsed), False)
    ck("part-2b: a clean ledger (no preamble rows) yields zero mis-filed",
       len(misfiled_finding_rows(doc)), 0)

    # --- codex QA #1996 HIGH-1: a phantom heading AFTER `## Open` strands an OPEN row -----------
    mf_postopen = (
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | error | a real open row | probe |  |\n"
        "## Closed today` and the rest is deleted.\n"
        "| 2026-09-05 | error | an orphaned open row after a post-Open phantom | probe |  |\n"
        "## Closed today\n"
        "| 2026-09-04 | error | a genuinely closed row | probe | FIXED #1 |\n"
        "## 2026-08-01 archive\n"
        "| 2026-08-01 | error | an archived row | probe | FIXED #2 |\n"
    )
    mf_po = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_postopen)]
    ck("part-2b codex-1: a row orphaned by a post-Open phantom heading IS flagged",
       any("an orphaned open row" in x for x in mf_po), True)
    ck("part-2b codex-1: the in-scope Open row is NOT flagged",
       any("a real open row" in x for x in mf_po), False)
    ck("part-2b codex-1: a genuine Closed-today row is NOT flagged",
       any("a genuinely closed row" in x for x in mf_po), False)
    ck("part-2b codex-1: a post-Closed-today archive row is NOT flagged",
       any("an archived row" in x for x in mf_po), False)

    # --- codex QA #1996 HIGH-2: delimiter-aware fences + parser/detector seam ------------------
    mf_fence = (
        "## Disposition values\n"
        "```\n"
        "~~~\n"
        "## Closed today\n"
        "| 2026-09-03 | error | a fenced row that must be ignored | probe | FIXED #1 |\n"
        "```\n"
        "| 2026-09-03 | error | a real preamble row after the fence | probe | FIXED #2 |\n"
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    mf_fn = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_fence)]
    ck("part-2b codex-2: a fenced row (mixed ~~~ inside ``` ) is NOT flagged",
       any("a fenced row that must be ignored" in x for x in mf_fn), False)
    ck("part-2b codex-2: a real preamble row after the fence IS flagged",
       any("a real preamble row after the fence" in x for x in mf_fn), True)
    mf_fence_open = (
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "```\n"
        "## Closed today\n"
        "```\n"
        "| 2026-09-05 | error | an open row after a FENCED phantom heading | probe |  |\n"
    )
    _po = [fi for (_fd, _sv, fi, _d) in parse_open_rows_full(mf_fence_open)]
    ck("part-2b codex-2 seam: the parser ignores a FENCED `## ` heading (row stays in Open scope)",
       any("after a FENCED phantom heading" in fi for fi in _po), True)

    # --- codex QA #1996 iter-2 HIGH: a backtick-FREE phantom `## Closed today <prose>` must NOT open a
    # scanned section (only an exact name or a `(`-decoration opens); a decorated real heading DOES. ---
    mf_bf = (
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | error | a real open row | probe |  |\n"
        "## Closed today and the row is deleted from the legend.\n"
        "| 2026-09-05 | error | an orphan after a backtick-free phantom | probe |  |\n"
        "## Closed today\n"
        "| 2026-09-04 | error | a real closed row | probe | FIXED #1 |\n"
    )
    mf_bfl = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_bf)]
    ck("part-2b iter2: a backtick-FREE phantom `## Closed today <prose>` does NOT open (orphan flagged)",
       any("an orphan after a backtick-free phantom" in x for x in mf_bfl), True)
    mf_dec = (
        "## Disposition values\n"
        "| 2026-09-03 | error | a preamble row | probe | FIXED #1 |\n"
        "## Open (swept 2026-09)\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | error | a row under a decorated Open heading | probe |  |\n"
    )
    _dec = [fi for (_fd, _sv, fi, _d) in parse_open_rows_full(mf_dec)]
    ck("part-2b iter2: a `(`-decorated `## Open (swept ...)` heading DOES open (row parsed)",
       any("a row under a decorated Open heading" in fi for fi in _dec), True)

    # --- codex QA #1996 iter-2 MED: a 4-backtick fence is not closed by a 3-backtick content line. ---
    mf_4f = (
        "## Disposition values\n"
        "````\n"
        "```\n"
        "| 2026-09-03 | error | a row inside a 4-backtick fence | probe | FIXED #1 |\n"
        "````\n"
        "| 2026-09-03 | error | a real row after the 4-backtick fence | probe | FIXED #2 |\n"
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    mf_4fl = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_4f)]
    ck("part-2b iter2: a row inside a 4-backtick fence (3-backtick content) is NOT flagged",
       any("inside a 4-backtick fence" in x for x in mf_4fl), False)
    ck("part-2b iter2: a real row after the 4-backtick fence IS flagged",
       any("after the 4-backtick fence" in x for x in mf_4fl), True)

    # --- codex QA #1996 iter-3 HIGH: a decoration with TRAILING PROSE (or unclosed `(`) must NOT open. ---
    mf_trail = (
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | error | real open | probe |  |\n"
        "## Closed today (swept 2026-09) and the row is deleted\n"
        "| 2026-09-05 | error | an orphan after a paren+prose phantom | probe |  |\n"
        "## Closed today\n"
        "| 2026-09-04 | error | closed | probe | FIXED #1 |\n"
    )
    mf_tl = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_trail)]
    ck("part-2b iter3: a `(...)`-decoration with TRAILING PROSE does NOT open (orphan flagged)",
       any("an orphan after a paren+prose phantom" in x for x in mf_tl), True)
    mf_unclosed = (
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
        "## Closed today (and the row is deleted\n"
        "| 2026-09-05 | error | an orphan after an unclosed-paren phantom | probe |  |\n"
        "## Closed today\n"
        "| 2026-09-04 | error | closed | probe | FIXED #2 |\n"
    )
    mf_uc = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_unclosed)]
    ck("part-2b iter3: an UNCLOSED `(` heading does NOT open (orphan flagged)",
       any("an orphan after an unclosed-paren phantom" in x for x in mf_uc), True)

    # --- codex/gemini QA #1996 iter-3 MED: an info-string line (```python) must NOT close a fence. ---
    mf_info = (
        "## Disposition values\n"
        "```\n"
        "```python\n"
        "| 2026-09-03 | error | a row after an info-string line inside a fence | probe | FIXED #1 |\n"
        "```\n"
        "| 2026-09-03 | error | a real row after the true fence close | probe | FIXED #2 |\n"
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    mf_if = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_info)]
    ck("part-2b iter3: an info-string ```lang line does NOT close the fence (fenced row not flagged)",
       any("after an info-string line inside a fence" in x for x in mf_if), False)
    ck("part-2b iter3: the row after the true (bare) fence close IS flagged",
       any("after the true fence close" in x for x in mf_if), True)

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
