#!/usr/bin/env python3
"""PreToolUse: refuse to open or merge a PR while a confirmed defect sits undispositioned.

WHY THIS IS A HOOK AND NOT A CONVENTION. The convention existed and failed twice in one day on the
same axis. Its scope hole was that "a delivered QA result blocks progress" covered findings arriving
FROM WORKERS and said nothing about findings the orchestrator generates ITSELF; on 2026-07-25 two live
defects in a file-moving tool, produced by the orchestrator's own probe minutes earlier, were rendered
as a table row and walked past in favour of writing a summary statistic about them. Reading a finding
is not acting on one, and the gap between those two is where the cost lives, so the block is
mechanical.

WHAT IT READS. `open-findings.md`, resolved via `lint_common.resolve_working`: the first existing of an
eligible out-of-repo operational store (`$GRC_STORE`, else `<repo-parent>/private`), then the
`grc_library_private/.working/` sibling, then the in-repo `.working/` (if the resolver helper cannot be
imported, only the in-repo path is checked). Its `## Open` table carries one row per
confirmed defect with a severity and a disposition. A row with an EMPTY disposition is undispositioned.
A row leaves the ledger only via FIXED, ROUTED, REFUTED or ACCEPTED, so "no disposition" is the
primary blocking condition; the one other blocking condition is a MIS-FILED row (below).

WHAT IT BLOCKS. An `error`-severity undispositioned row blocks a Bash command whose
whitespace-collapsed text contains the case-sensitive substring `gh pr create` or `gh pr merge`, or whose
shell tokens have `gh`, then `pr`, then `create` or `merge`, with no fresh `gh` between (so a quoted
`gh pr 'merge'` is caught, and `echo "gh pr merge"` and `gh pr view 1 && git merge x` are gated; text
matching, not a shell model, so the class the is_blocking_command docstring states (another shell or eval,
stdin or a heredoc, a variable or alias, shlex-vs-bash quoting, mixed continuations) can evade when the hook does not see gh, pr and the verb as one command's words; 3b112), or any command
that mentions tools/merge-when-green.py other than a simple direct --dry-run or --self-test (3b108;
see invokes_merge_tool), because
shipping past a known wrong behaviour is the thing worth preventing. A `warning` does not block a PR
(an in-flight change should finish rather than be abandoned half-landed) and is surfaced instead.
Notes never block. SECOND blocking condition (P-1.70, 2026-09-10): a MIS-FILED finding-row - one that
carries the finding-row shape but sits BEFORE the scanned sections open (in the preamble above
'## Open', or stranded by a phantom heading between '## Open' and '## Closed today'), so it escapes
the disposition scan - also blocks (any severity/disposition). The legitimate post-'## Closed today'
archive is location-EXEMPT (a row there is indistinguishable from an archived one; see the
misfiled_finding_rows SCOPE/RESIDUES). This covers the push->merge edit window the pre-push D14
check cannot see.

FAIL-OPEN BY DESIGN, AND SAID SO PLAINLY. If the ledger is missing or unreadable this hook ALLOWS the
action, because a guard that blocks all work on its own malfunction would be removed within a day, and
a removed guard protects nothing. ONE exception is deliberately fail-CLOSED: a single MALFORMED row
(wrong column count, e.g. a stray unescaped pipe) UNDER ``## Open`` is forced toward BLOCK, not allow,
so it cannot silently disable the guard (a malformed row under ``## Closed today`` or the dated archive
is out of the Open-scoped scan, so it neither blocks nor fails open). That is a deliberate trade recorded
here rather than an oversight: the ledger plus the convention are the primary control and this hook is
defence in depth.

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
import os
import re
import shlex
import sys
from pathlib import Path

LEDGER_REL = ".working/open-findings.md"
BLOCKING_CMDS = (("gh", "pr", "create"), ("gh", "pr", "merge"))


# `.working/` -> `_private` migration: resolve the (maintainer-only) working-state file through
# lint_common.resolve_working (an eligible out-of-repo operational store preferred, then the private
# sibling, then the in-repo fallback). Fail-SAFE: if the
# helper cannot be imported, fall back to the historical in-repo path so this hook never breaks.
def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


try:
    _resolve_working = _load_sibling("lint_common").resolve_working
except Exception:  # pragma: no cover - fail-safe: never let a helper-load failure break the hook
    _resolve_working = None


def _working_file(rel_below, root):
    """`.working/<rel_below>` resolved via lint_common (operational store preferred, else private sibling, else in-repo), or None."""
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root)
    cand = root / ".working" / rel_below
    return cand if cand.exists() else None


def project_root() -> Path:
    # Derived from this file's location, never hardcoded, so the guard follows a repo relocation
    # (the row-E lesson from an earlier checkout move, where five hooks kept a stale absolute root).
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
    of scope, where the mis-filed-row detector converts the old silence into a BLOCK (P-1.70, 2026-09-10). No real
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


# A fence-ELIGIBLE line sits at 0-3 spaces of indent (the CommonMark limit, the same rule as the
# repo's shared fence predicate, grc 3b83): a marker indented four or more columns, or behind a
# tab, is content, so it neither opens a fence nor closes one. Callers test the RAW line with this
# before reading the stripped line's run.
_FENCE_ELIGIBLE_RE = re.compile(r" {0,3}[`~]")


def _fence_run(line: str, stripped: str):
    """PURE. If the line begins a code fence, return (char, length) where char is `` ` `` or `~` and
    length is the run of that char (>= 3); else None (also None for a line that is not fence-ELIGIBLE:
    indented four or more columns, or behind a tab, per `_FENCE_ELIGIBLE_RE`; grc 3b83). CommonMark-aware
    fence tracking (codex QA #1996): the OPENER records its char and length, and a line CLOSES it only
    when it is the same char, at least as long, and bare (no info string). This keeps a `~~~` line inside
    a ``` fence from closing it, AND a three-backtick line inside a four-backtick fence from closing it."""
    if not _FENCE_ELIGIBLE_RE.match(line):
        return None
    for ch in ("`", "~"):
        if stripped.startswith(ch * 3):
            return (ch, len(stripped) - len(stripped.lstrip(ch)))
    return None


def _fence_closes(run, fence, stripped: str) -> bool:
    """PURE. Does this fence-run line CLOSE the open `fence` (char, length)? Same char, length >=
    opener, AND BARE, meaning the run spans the whole stripped line so there is no info string
    (codex/gemini QA #1996: ``` ```python ``` closes nothing; a CommonMark closing fence carries no
    info string). An indented (4+ columns) marker yields run=None (grc 3b83) and so never closes.
    RESIDUE (accepted): backtick-in-info-string openers and container blocks are not modelled; the
    operational ledger uses column-0 bare fences."""
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
        run = _fence_run(line, stripped)
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
        run = _fence_run(line, stripped)
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
# A ref is a PR number (`#1178`), a public backlog item (`3.73`, `3.56a`), a private `P-N.M` item
# (`P-1.71`), or a `TODO`-qualified item (`TODO 3.73`, `TODO P-1.60`).
TERMINAL = ("fixed", "routed", "refuted", "accepted")
# A ref is a PR number (`#1`.., never `#0`), a public backlog item (`3.73`, `3.56a`, `3.139.1`), a
# private `P-N.M` item (`P-1.71`), or a `TODO`-qualified item. The private `P-` namespace is a
# first-class routing target (e.g. P-1.60/P-1.61); rejecting it read a valid `ROUTED P-1.71` as
# undispositioned (self-caught 2026-09-05, #2016). `(` or `[` may sit immediately before it (a parenthesized or link-form ref).
# The private backlog's letter-series ids (3b108, 3b50b2e1) are refs too: routing to one was read as
# undispositioned before (3b108).
_REF = r"[(\[]?(?:#[1-9]\d*|TODO\s+(?:P-)?\d+(?:\.\d+)+[a-z]?|P-\d+(?:\.\d+)+[a-z]?|\d+(?:\.\d+)+[a-z]?|\d+b\d+(?:[a-z]\d+)*)"
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



def invokes_merge_tool(cmd: str) -> bool:
    """PURE. Could this command run tools/merge-when-green.py for a real merge (3b108)? That tool runs
    `gh pr merge` as a subprocess, so the literal-text match never sees it. Parsing shell for every way
    to run it (wrappers, bash -c, backticks, python -m, continuations, newlines) cannot be made
    complete (3b108 QA r1), so this over-gates by intent. THREAT MODEL, stated: a speed bump for an
    honest actor's slip, not an adversarial control; a deliberately obfuscated command (a glob such as
    gree[n] or gree*, a variable holding part of the name, code run through python -c) can still evade,
    and merge-when-green.py enforces the open-findings decision itself on every merge. after dropping quotes and backslash-newline
    continuations, any mention of merge-when-green gates, except a single simple command (one line,
    no shell operator, no substitution) that passes --dry-run or --self-test. A read of the file is
    gated too; that costs little, since this hook blocks only while its blocking state holds, and
    merge-when-green.py enforces the open-findings check itself on every merge."""
    if not isinstance(cmd, str):
        return False
    norm = cmd.replace("\\\n", "")
    for q in ("'", '"', "`", "\\"):  # quotes and escapes (merge-when-\\green) do not hide the name
        norm = norm.replace(q, "")
    if "merge-when-green" not in norm:
        return False
    # The exemption needs the flag among the tool's OWN arguments in a direct invocation (the tool, or a
    # python interpreter with single-letter options, then the tool): a comment, a `bash -c ... --dry-run`
    # ($0 of the inner shell) or any other placement gates (3b108 QA r2).
    simple = "\n" not in cmd.strip() and not any(op in cmd for op in (";", "&", "|", "`", "$(", "<", ">", "\\", "#"))
    if simple:
        try:
            toks = shlex.split(cmd)
        except ValueError:
            return True
        i = 0
        if toks and os.path.basename(toks[0]).startswith("python"):
            i = 1
            while i < len(toks) and len(toks[i]) == 2 and toks[i].startswith("-") and toks[i] not in ("-m", "-c"):
                i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "merge-when-green.py":
            if "--dry-run" in toks[i + 1:] or "--self-test" in toks[i + 1:]:
                return False
    return True

def is_blocking_command(cmd: str) -> bool:
    """PURE. Does this command open or merge a PR? Three detectors, OR'd, matching
    block-pr-without-resume-validate.py so the two hooks agree (3b112):
      (1) the case-sensitive substring `gh pr create` or `gh pr merge` after whitespace collapse
          (operator-glued and unbalanced-quote forms);
      (2) the ordered shlex token subsequence `gh` (bare or a path ending /gh), `pr`, `create` or
          `merge` (quoted subcommands such as gh "pr" merge or gh pr 'merge', and interleaved flags);
      (3) a mention of tools/merge-when-green.py other than a simple direct --dry-run or --self-test
          (3b108; see invokes_merge_tool).
    The token match allows any tokens or operators between gh, pr and the verb, and a fresh gh resets
    it, so `gh pr view 12 && git merge main` and `echo "gh pr merge"` are gated (over-gating is the safe
    direction). The gh detectors run on the text as written AND with backslash-newlines joined, and
    block on either (3b112 QA r1, r2). RESIDUE, as a class: this is text matching, not a shell model.
    A command it does not see as gh, pr and the verb in one command's words evades, and these forms can
    produce one (a plain bash -c "gh pr merge 1" is still caught by the substring pass): one run through
    another shell or eval (bash -c "...", sh -c, eval), fed on stdin or through a heredoc, built from a
    variable or an alias, or quoted in a way shlex reads differently from bash (ANSI-C quoting, a mid-word
    #), or split by a mix of continuations bash joins and does not. Rounds 3-6 of 3b112 tried to model those forms and each attempt introduced new misses, so they are
    left to this statement; the merge tool applies the open-findings decision itself on every merge. A
    speed bump for an honest slip, not an adversarial control."""
    if not isinstance(cmd, str):
        return False
    if invokes_merge_tool(cmd):  # the sanctioned merge path runs gh pr merge as a subprocess (3b108)
        return True
    # Both the text as written and the text with every backslash-newline joined: bash joins only some of
    # them (not after an even run of backslashes or in a comment), so blocking on either keeps both cases
    # (3b112 QA r1, r2). The merge-tool exemption above reads only the unjoined text.
    return _gh_pr_verb(cmd) or _gh_pr_verb(cmd.replace("\\\n", ""))


def _gh_pr_verb(cmd: str) -> bool:
    """PURE. The substring pass and the ordered shlex token pass for `gh pr create|merge`."""
    flat = " ".join(cmd.split())
    if any(" ".join(parts) in flat for parts in BLOCKING_CMDS):
        return True
    toks = _tokens(cmd)
    if toks is None:
        return False  # unparseable is already covered by the substring pass above
    seen_gh = seen_pr = False
    for tk in toks:
        if tk == "gh" or tk.endswith("/gh"):   # bare `gh` or an absolute/relative path to it
            seen_gh, seen_pr = True, False
        elif seen_gh and tk == "pr":
            seen_pr = True
        elif seen_pr and tk in ("create", "merge"):
            return True
    return False


def _tokens(cmd: str):
    """PURE. shlex tokens with operators split out and a trailing # comment dropped, as bash does;
    None on an unparseable command (unbalanced quotes). Same as block-pr-without-resume-validate.py."""
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        return list(lex)
    except ValueError:
        return None


def decide_exit(rows, ledger_text) -> int:
    """PURE decision: the exit code (0 allow / 2 block) for a PARSED ledger.

    Extracted from main() (P-1.70, #2094) so BOTH blocking conditions - an
    undispositioned error-severity row, and a mis-filed finding-row - are directly
    regression-tested by self_test(), not just the misfiled DETECTOR. main() keeps the
    fail-open ledger read/parse; this decides on the already-parsed result and emits the
    same stderr diagnostics as before.
    """
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
            lines = [
                f"BLOCKED (open-findings-misfiled): (P-1.70 part-2b) a PR create/merge with {len(misfiled)} finding-row(s) in "
                f"{LEDGER_REL} OUTSIDE '## Open' / '## Closed today'.\n"
                "WHY: a row outside a scanned section is invisible to this hook's disposition scan, so "
                "an undispositioned defect would escape the guard entirely.\n"
                "CONSIDER INSTEAD: move each row below into a scanned section ('## Open' or "
                "'## Closed today'); if a row is a deliberate archive, give it a scanned heading or "
                "remove the finding-row shape:",
            ]
            for _ln, _sec, _line in misfiled[:5]:
                lines.append(f"  - line {_ln} (under {_sec or 'no scanned heading'}): {_line[:100]}")
            lines.append(
                "This now BLOCKS at gh pr create/merge (P-1.70, maintainer-GO'd 2026-09-10), covering "
                "the push->merge edit window the pre-push D14 check cannot see; D14 remains the "
                "pre-push backstop.")
            print("\n".join(lines), file=sys.stderr)
            return 2
        return 0

    lines = [f"BLOCKED (open-findings): a PR create/merge with {len(errs)} error-severity finding(s) in {LEDGER_REL} "
             "without a disposition.", ""]
    for _s, finding, _d in errs[:5]:
        lines.append(f"  - {finding[:150]}")
    lines += ["",
              "WHY: a finding READ but not acted on is the most expensive state a defect can be in, "
              "because the record shows it was found and the surface therefore reads as examined "
              "while the defect is still live.",
              "CONSIDER INSTEAD: give each row above a disposition (FIXED / ROUTED / REFUTED / "
              "ACCEPTED) and move it to '## Closed today'; do NOT write a count or summary about them "
              "first (turning live defects into a statistic is the specific failure this guard stops)."]
    print("\n".join(lines), file=sys.stderr)
    return 2



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

    return decide_exit(rows, ledger_text)

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
    ck("ROUTED + adjacent P-namespace ref is valid", disposition_valid("ROUTED P-1.71 (Nigeria batch)"), True)
    ck("ROUTED + adjacent TODO P-ref is valid", disposition_valid("ROUTED TODO P-1.60"), True)
    ck("a P- ref without a dotted number is INVALID", disposition_valid("ROUTED P-71"), False)
    ck("TODO with a P-less hyphenless malformed ref is INVALID", disposition_valid("ROUTED TODO P1.60"), False)
    ck("TODO with a bare-hyphen malformed ref is INVALID", disposition_valid("ROUTED TODO -1.60"), False)
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
    ck("whitespace is collapsed before the substring pass", is_blocking_command("gh  pr\tmerge 1 'x"), True)
    ck("stated residue: ANSI-C quoting is not seen (text matching, not a shell model)", is_blocking_command("gh pr $'merge' 1"), False)
    ck("an unparseable command is still caught by the substring pass", is_blocking_command("gh pr merge 1 'unclosed"), True)
    ck("an unrelated command does not block", is_blocking_command("git status --short"), False)
    ck("gh pr checks does not block", is_blocking_command("gh pr checks 12"), False)
    # 3b112: the token detector, matching block-pr-without-resume-validate.py
    ck("quoted verb blocks (gh pr 'merge')", is_blocking_command("gh pr 'merge' 12 --admin"), True)
    ck("quoted subcommand blocks (gh \"pr\" create)", is_blocking_command('gh "pr" create --title x'), True)
    ck("interleaved flag blocks (gh -R o/r pr merge)", is_blocking_command("gh -R o/r pr merge 12"), True)
    ck("path to gh blocks (/usr/bin/gh pr merge)", is_blocking_command("/usr/bin/gh pr  'merge' 1"), True)
    ck("glued operator and flag block (gh -R x pr merge&&echo)",
       is_blocking_command("gh -R x pr merge&&echo ok"), True)
    ck("quoted gh pr view does not block", is_blocking_command("gh 'pr' view 12"), False)
    ck("commented-out verb does not block", is_blocking_command("gh pr view 12 # then merge"), False)
    ck("unbalanced quote falls back to substring only", is_blocking_command("gh 'pr view 12"), False)
    ck("non-string does not block", is_blocking_command(None), False)
    # 3b112 QA r1: a fresh gh resets the match; a continuation is also checked joined
    ck("gh repo create is not a pr command", is_blocking_command("gh repo create foo"), False)
    ck("gh pr list then gh repo create is not a pr-create", is_blocking_command("gh pr list && gh repo create x"), False)
    ck("pr merge without gh does not block", is_blocking_command("echo pr merge"), False)
    ck("backslash-newline continuation blocks", is_blocking_command("gh pr \\\nmerge 1"), True)
    # 3b112 QA r2: bash does not join after an even backslash run or inside a comment; both texts are checked
    for s in ("echo x\\\\\ngh pr 'merge' 1", "# note \\\ngh pr 'merge' 1", "true # trailing\\\ngh pr 'create'",
              '# note \\\ngh "pr" create'):
        ck(f"unjoined text still checked: {s!r}", is_blocking_command(s), True)
    ck("quoted --dry-ru<nl>n is not a dry-run exemption",
       is_blocking_command("python3 tools/merge-when-green.py 12 '--dry-\\\nrun'"), True)
    # 3b108: letter-series backlog ids are valid refs; a bare word or a lone letter-number is not.
    ck("ROUTED 3b108 is dispositioned", disposition_valid("ROUTED 3b108 (next PR)"), True)
    ck("FIXED 3b50b2e1 is dispositioned", disposition_valid("FIXED 3b50b2e1"), True)
    ck("ROUTED 3b alone is not", disposition_valid("ROUTED 3b later"), False)
    ck("ROUTED b12 is not", disposition_valid("ROUTED b12"), False)
    for bad in ("ROUTED 3b108pending", "ROUTED 3b108garbage", "ROUTED 24x7 support", "FIXED 1e2rror"):
        ck(f"not a ref: {bad}", disposition_valid(bad), False)
    # 3b108: the sanctioned merge path runs gh pr merge as a subprocess, so the tool itself is gated;
    # detection over-gates by intent (QA r1: shell parsing could not be made complete).
    for c in ("python3 tools/merge-when-green.py 12 --repo o/r --admin",
              "for i in 1; do out=$(python3 -B /x/tools/merge-when-green.py 12 --admin 2>&1); done",
              "./tools/merge-when-green.py 12",
              "python3 tools/merge-when-green.py 12 --admin\npython3 tools/merge-when-green.py 13 --dry-run",
              "timeout 60 ./tools/merge-when-green.py 12", "bash -c 'tools/merge-when-green.py 12 --admin'",
              "out=`python3 tools/merge-when-green.py 12`", 'out="$(python3 tools/merge-when-green.py 12)"',
              "python3 -m tools.merge-when-green 12", "python3 tools/merge-when-\\\ngreen.py 12",
              'python3 tools/merge-when-""green.py 12 --admin', "python3 tools/merge-when-green.py 12 --admin # ' --dry-run",
              "python3 tools/merge-when-green.py 12 --admin > --dry-run", "grep -n x tools/merge-when-green.py",
              "python3 tools/merge-when-green.py 12 --admin # --dry-run",
              "bash -c 'python3 tools/merge-when-green.py 12 --admin' --dry-run",
              "sh -c 'tools/merge-when-green.py 12' --self-test", "env python3 tools/merge-when-green.py 12 --dry-run",
              "python3 -c 'import os' tools/merge-when-green.py --dry-run",
              "python3 tools/merge-when-\\green.py 12 --admin",
              "python3 -c 'print(1) or 1/merge-when-green.py' --dry-run"):
        ck(f"gated: {c[:48]}", is_blocking_command(c), True)
    for c in ("python3 tools/merge-when-green.py 12 --dry-run", "python3 tools/merge-when-green.py --self-test",
              "python3 -B /opt/x/tools/merge-when-green.py 2620 --repo o/r --dry-run", "git status --short",
              "/usr/bin/python3.12 -B tools/merge-when-green.py --self-test", "./tools/merge-when-green.py 12 --dry-run"):
        ck(f"not gated: {c[:48]}", is_blocking_command(c), False)

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

    # --- grc 3b83: a marker indented four or more columns is content, not a fence. ---
    mf_indent = (
        "## Disposition values\n"
        "    ```\n"
        "| 2026-09-03 | error | a preamble row after an indented marker | probe | FIXED #1 |\n"
        "```\n"
        "| 2026-09-03 | error | a fenced row under a real opener | probe | FIXED #2 |\n"
        "    ```\n"
        "| 2026-09-03 | error | a row after an indented non-closer | probe | FIXED #3 |\n"
        "```\n"
        "## Open\n"
        "| Found | Severity | Finding | Source | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    mf_in = [ln for (_l, _s, ln) in misfiled_finding_rows(mf_indent)]
    ck("3b83: an indented (4-space) marker does NOT open a fence (the row after it IS flagged)",
       any("after an indented marker" in x for x in mf_in), True)
    ck("3b83: a row under the real opener stays fenced (not flagged)",
       any("a fenced row under a real opener" in x for x in mf_in), False)
    ck("3b83: an indented marker does NOT close the open fence (the row after it stays fenced)",
       any("after an indented non-closer" in x for x in mf_in), False)

    # P-1.70 (#2094): regression-test the BLOCKING branches of decide_exit directly, not just
    # the misfiled DETECTOR (codex #2094 vpr F2). Clean ledger allows (0); an undispositioned
    # error blocks (2); a mis-filed preamble row blocks (2).
    _hdr = "| Found | Severity | Finding | Source | Disposition |\n| --- | --- | --- | --- | --- |\n"
    _clean = "## Open\n\n" + _hdr + "\n## Closed today\n"
    ck("decide_exit: clean ledger allows (0)", decide_exit(parse_open_rows(_clean), _clean), 0)
    _err = "## Open\n\n" + _hdr + "| 2026-01-01 | error | undispositioned err | s |  |\n"
    ck("decide_exit: undispositioned error blocks (2)", decide_exit(parse_open_rows(_err), _err), 2)
    _mf = "| 2026-01-01 | error | preamble stray finding | s | FIXED #1 |\n\n## Open\n\n" + _hdr
    ck("decide_exit: mis-filed preamble row blocks (2)", decide_exit(parse_open_rows(_mf), _mf), 2)

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
