#!/usr/bin/env python3
"""Gate-name-citation inventory audit (gate 77; backlog item 3.56a (closing PR #1139) guard 2, private list).

Wiring sections, command stubs, and the CLAUDE.md files cite gates by number
AND name, for example ``gate 35 (gate-name parity)`` or ``the
document-date-staleness gate (31)``. When a gate is renumbered, such a citation
can silently point its number at a DIFFERENT gate while keeping the old name, a
drift no other gate catches. This gate is the renumbering guard: for each
genuine gate-name citation it compares the cited NAME against the canonical name
that the audit-programme specification's section 6 inventory records for that
NUMBER, and flags a citation whose name shares NO significant token with the
number's current canonical name (the shape a renumber produces).

FP-safety (census-derived, backlog item 3.56a (closing PR #1139), private list; the census is
``grc_library_scratch:results/research-guard2-gatename-citation-census.md``):

  * SCOPE: it scans only the CITATION surfaces (pack ``SKILL.md`` files, the
    ``.claude/commands/`` stubs, the pack ``CLAUDE.md`` and the project
    ``.claude/CLAUDE.md``). It deliberately does NOT scan the audit-programme
    specification itself: that file's section 6.x prose is dense with
    ``gate N (...)`` role-glosses and relationship-descriptors that are the
    single biggest false-positive source, and it is the ground truth, not a
    citation surface.
  * NAME-SHAPED ONLY: a parenthetical is treated as a name-citation only when it
    is a NAME, not a role-gloss or a relationship. A parenthetical that opens
    with an article (``the`` / ``a`` / ``an``), or that itself contains a
    ``gate <digit>`` cross-reference, is a role/relationship description, not a
    name, and is skipped (for example ``gate 5 (the enumeration axis ...)``,
    ``gate 50 (the gate-48 ... precedent)``). A bare ``gate N`` with no adjacent
    parenthetical name (``gates 48 and 49``, ``gate 41 checks four surfaces``) is
    never a name-citation.
  * TOKEN-OVERLAP, not exact string: the cited name and the section 6 canonical
    name are normalized (lowercased, hyphens to spaces, the stop-words
    ``the/a/an/and/or/of/for/to/in`` and the generic ``gate`` and ``audit``
    dropped) and compared by SET INTERSECTION. A citation is a MISMATCH only when
    the intersection is EMPTY. This tolerates the real citation style
    (``guardrail-review cadence currency`` vs ``Guardrail-review cadence audit``
    is a MATCH on the ``guardrail-review``, ``cadence`` tokens) while still
    catching a genuine renumber (a name that belongs to a different number shares
    no token with the new occupant).
  * A cited number ABSENT from the inventory is also flagged (a citation of a
    gate number that section 6 does not define).

Count-free by construction (the gate-39 trap): this module, its wiring, and its
spec row state the mechanism WITHOUT a hard gate-count number, so gate 39 does
not read a stale count claim here.

It ships green guard-first (the census found zero live name-drift): the fix for a
future finding is to correct the citation's name (or number) to match section 6,
never to weaken the gate.

Exit codes: 0 pass, 1 findings (a name-vs-inventory mismatch), 2 internal error.

Self-test: ``python3 tools/lint-gate-citation-inventory.py --self-test``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from lint_common import REPO_ROOT
except Exception:  # pragma: no cover
    REPO_ROOT = Path(__file__).resolve().parent.parent

SPEC = "governance/specification-audit-programme.md"
# The section 6 inventory row: `| N | Canonical Name | [`tools/...`](...) |`.
_INV_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")

# Section-6 region delimiters (3.109 F2 scoping; F3 container-awareness). ATX headings
# allow up to 3 leading spaces and a space OR tab after the ``N.``; the region scan is
# FENCE- and CONTAINER-aware (the _BlockScan block-structure scanner below), so
# heading-shaped or inventory-shaped text inside a code block, a blockquote, or a
# list item cannot start, truncate, or inject rows into the region, while an indented
# heading at true top level still bounds it.
# A fenced-code-block delimiter: 3+ backticks or 3+ tildes, up to 3 leading spaces,
# optionally followed by an info string. CommonMark closes a fence only with the SAME
# marker char, a run at least as long, and no info string (3.109 F2).
_FENCE_LINE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})[ \t]*(.*)$")

# CommonMark line endings are LF, CR, or CRLF only. Python's str.splitlines() ALSO
# breaks on U+0085/U+2028/U+2029/U+000B/U+000C, which would let a Unicode separator
# after a fence marker masquerade as a bare closing fence; split on the CommonMark set
# so those code points stay line CONTENT (3.109 F2).
_LINE_SPLIT = re.compile(r"\r\n|\r|\n")


def _fence_info(line: str):
    """``(marker_char, run_length, has_info_string)`` for a fence-delimiter line, else None.

    CommonMark conformance (3.109 F2): a BACKTICK fence's info string may not contain a
    backtick, so such a line is not a fence delimiter at all (a tilde fence's info may
    contain anything). ``has_info_string`` is taken WITHOUT stripping, because the
    ``[ \t]+`` in :data:`_FENCE_LINE` already consumed the only whitespace a CLOSING
    fence may carry (ASCII space/tab); any remainder, including non-ASCII whitespace such
    as U+00A0, is an info string, so the line cannot close a fence."""
    m = _FENCE_LINE.match(line)
    if not m:
        return None
    run = m.group(1)
    info = m.group(2)
    if run[0] == "`" and "`" in info:
        return None
    return run[0], len(run), bool(info)


# ---- CommonMark block-structure scan (3.109 F3: container-aware region) ----
# The section-6 boundaries and the inventory rows are TOP-LEVEL constructs: a
# heading-shaped or row-shaped line nested in a BLOCKQUOTE or a LIST ITEM (or in
# a fence inside one) is that container's content, never a region boundary or an
# inventory row, while an indented heading at true top level still is one. Only
# block-structure parsing distinguishes the two, so the scanner below implements a
# the CommonMark block phase for the subset this tool needs: blockquote
# containers (spec 5.1: 0-3 columns indent, ``>``, one optional space or tab
# column), list-item containers (spec 5.2: bullets -, +, * and ordered markers
# of 1-9 digits followed by ``.`` or ``)``, establishing a content-indent
# offset), their nesting, fenced code blocks in any container context (spec
# 4.5), ATX headings (4.2), thematic breaks (4.4), blank lines, paragraph LAZY
# continuation (5.1 laziness), the at-most-one-blank-line rule for an item that
# begins empty (5.2), and tab-stop-4 column arithmetic (2.2). This is a
# CONTAINER-AWARE scan, NOT a complete CommonMark parser: setext headings, HTML
# blocks, link-reference definitions, GFM table block structure, and some
# list/paragraph-interruption and tab-expansion edges are not fully modelled, so
# an ADVERSARIAL construct of those shapes could misclassify. That is accepted
# for THIS guard-first tool by MEASUREMENT, not by a full-conformance claim: the
# live section-6 region contains none of these constructs (zero containers,
# fences, HTML openers, or setext underlines, measured), so the scanner is a
# no-op on today's spec and active only against future edits, which a maintainer
# reviews before they reach section 6; and the gate checks gate-name citations,
# not markdown rendering. Full CommonMark conformance would need a complete
# stdlib parser (gate 71 forbids a markdown library); deferred as disproportionate
# to this latent scoping fix (see the PR record for the residue detail).

_BLANK_LINE = re.compile(r"^[ \t]*$")
_ATX_LINE = re.compile(r"^[ ]{0,3}#{1,6}(?:[ \t]|$)")
_THEMATIC_LINE = re.compile(r"^[ ]{0,3}([-_*])[ \t]*(?:\1[ \t]*){2,}$")
_LIST_MARKER = re.compile(r"([-+*]|\d{1,9}[.)])(?=[ \t]|$)")


def _ws_width(text: str, col: int) -> int:
    """Column width of TEXT's leading space/tab run, tabs at 4-column stops
    from absolute column COL (CommonMark 2.2)."""
    w = 0
    for ch in text:
        if ch == " ":
            w += 1
        elif ch == "\t":
            w += 4 - ((col + w) % 4)
        else:
            break
    return w


def _strip_cols(text: str, col: int, n: int):
    """Strip N columns of leading whitespace from TEXT (which starts at
    absolute column COL): ``(rest, rest_col)``. A partially consumed tab
    leaves its remaining columns behind as literal spaces (CommonMark 2.2)."""
    i, c = 0, col
    target = col + n
    while i < len(text) and c < target:
        ch = text[i]
        if ch == " ":
            c += 1
            i += 1
        elif ch == "\t":
            stop = c + 4 - (c % 4)
            if stop <= target:
                c = stop
                i += 1
            else:
                return " " * (stop - target) + text[i + 1:], target
        else:
            break
    return text[i:], c


def _match_bq(rest: str, col: int):
    """Consume a blockquote marker (CommonMark 5.1: 0-3 columns of indent,
    ``>``, one optional space or tab column): ``(rest, col)`` past it, else
    None."""
    w = _ws_width(rest, col)
    if w > 3:
        return None
    r, c = _strip_cols(rest, col, w)
    if not r.startswith(">"):
        return None
    r, c = r[1:], c + 1
    if r[:1] in (" ", "\t"):
        r, c = _strip_cols(r, c, 1)
    return r, c


def _match_li(rest: str, col: int):
    """Consume a list-item marker (CommonMark 5.2): ``(content, content_col,
    rel_indent, marker)`` where REL_INDENT is the item's content indent
    relative to the enclosing container, else None. 1-4 following whitespace
    columns extend the content indent; 5+ (a code-block first line) and a
    blank or empty marker line both pin it to one column past the marker."""
    w = _ws_width(rest, col)
    if w > 3:
        return None
    r, c = _strip_cols(rest, col, w)
    m = _LIST_MARKER.match(r)
    if m is None:
        return None
    marker = m.group(1)
    r, c = r[len(marker):], c + len(marker)
    pad = _ws_width(r, c)
    if pad >= 5 or _BLANK_LINE.match(r):
        r, c = _strip_cols(r, c, 1)
        return r, c, w + len(marker) + 1, marker
    r, c = _strip_cols(r, c, pad)
    return r, c, w + len(marker) + pad, marker


class _BlockScan:
    """CommonMark block-phase line classifier: ``visible(line)`` is True
    exactly when LINE is a top-level leaf line (container stack empty, no open
    fence, not blank, not a fence delimiter, not a container-marker line),
    i.e. a line the section-6 boundary and inventory-row patterns may
    legitimately match."""

    def __init__(self) -> None:
        # container stack, outermost first: ["bq"] or ["li", rel_indent, empty_open]
        self._stack: list[list] = []
        self._fence: tuple[str, int] | None = None  # open fence at depth len(stack)
        self._para = False  # the innermost open leaf is a paragraph

    def _starts_block(self, rest: str, col: int) -> bool:
        """Can REST interrupt an open paragraph? ATX headings, fenced code,
        blockquotes, and thematic breaks always can; a list item only when it
        is non-empty AND is a bullet or an ordered marker numbered 1
        (CommonMark 5.2 interruption rules)."""
        if _match_bq(rest, col) is not None or _fence_info(rest) is not None:
            return True
        if _ATX_LINE.match(rest) or _THEMATIC_LINE.match(rest):
            return True
        li = _match_li(rest, col)
        if li is None or _BLANK_LINE.match(li[0]):
            return False
        marker = li[3]
        return not marker[0].isdigit() or int(marker[:-1]) == 1

    def visible(self, line: str) -> bool:
        rest, col = line, 0
        matched = 0
        for cont in self._stack:  # phase 1: match the open container prefixes
            if cont[0] == "bq":
                m = _match_bq(rest, col)
                if m is None:
                    break
                rest, col = m
            elif _BLANK_LINE.match(rest):
                if cont[2]:
                    break  # an item that began empty holds at most one blank line
            elif _ws_width(rest, col) >= cont[1]:
                rest, col = _strip_cols(rest, col, cont[1])
                cont[2] = False
            else:
                break
            matched += 1
        if self._fence is not None:
            if matched == len(self._stack):
                fm = _fence_info(rest)
                if (fm is not None and fm[0] == self._fence[0]
                        and fm[1] >= self._fence[1] and not fm[2]):
                    self._fence = None
                return False  # fence content, or its closing delimiter
            # a lost container prefix closes the containers AND the fence they
            # hold: fenced code has no lazy continuation (CommonMark 5.1)
            self._fence = None
            self._stack = self._stack[:matched]
        if _BLANK_LINE.match(rest):
            self._para = False
            self._stack = self._stack[:matched]  # a blank closes an unmatched quote
            return False
        if matched < len(self._stack):
            if self._para and not self._starts_block(rest, col):
                return False  # lazy continuation: the line stays in its container
            self._stack = self._stack[:matched]
            self._para = False
        while True:  # phase 2: new container starts on the remainder
            m = _match_bq(rest, col)
            if m is not None:
                self._stack.append(["bq"])
                self._para = False
                rest, col = m
                if _BLANK_LINE.match(rest):
                    return False
                continue
            if _THEMATIC_LINE.match(rest):
                self._para = False
                return False
            li = _match_li(rest, col)
            if li is not None:
                rest, col, rel, _marker = li
                empty = bool(_BLANK_LINE.match(rest))
                self._stack.append(["li", rel, empty])
                self._para = False
                if empty:
                    return False
                continue
            break
        fm = _fence_info(rest)  # leaf classification on the remainder
        if fm is not None:
            self._fence = (fm[0], fm[1])
            self._para = False
            return False  # an opening fence delimiter
        if _ATX_LINE.match(rest):
            self._para = False
            return not self._stack
        # any other leaf: a paragraph, its continuation, or (at 4+ columns)
        # indented code, which cannot interrupt an open paragraph (4.4, 4.8)
        self._para = self._para or _ws_width(rest, col) <= 3
        return not self._stack


_SECTION6_HEADING = re.compile(r"^[ ]{0,3}##[ \t]+6\.(?:[ \t]|$)")
_TOP_SECTION_HEADING = re.compile(r"^[ ]{0,3}##[ \t]+\d+\.(?:[ \t]|$)")


def _section6_lines(spec_text: str) -> list[str]:
    """The TOP-LEVEL leaf lines of the section-6 region: from the ``## 6. ``
    heading through the line before the next top-level ``## N. `` heading, with
    every line that sits inside a fenced code block OR inside a blockquote or
    list-item container removed (3.109 F2/F3). Block-structure-aware
    (:class:`_BlockScan`) so a heading-shaped or row-shaped line nested in a
    fence or a container cannot start, truncate, or inject rows into the
    region, while an indented heading at true top level still bounds it. Empty
    list when no section-6 heading exists; RAISES when more than one real
    section-6 heading exists (ambiguous: fail loud rather than guess)."""
    scan = _BlockScan()
    rows: list[tuple[str, bool, bool, bool]] = []  # (text, visible, is_top, is_section6)
    for ln in _LINE_SPLIT.split(spec_text):
        vis = scan.visible(ln)
        is_top = vis and bool(_TOP_SECTION_HEADING.match(ln))
        rows.append((ln, vis, is_top, is_top and bool(_SECTION6_HEADING.match(ln))))
    starts = [i for i, r in enumerate(rows) if r[3]]
    if not starts:
        return []
    if len(starts) > 1:
        raise ValueError(
            f"multiple section-6 headings at lines {[s + 1 for s in starts]}; ambiguous")
    start = starts[0]
    end = next((i for i in range(start + 1, len(rows)) if rows[i][2]), len(rows))
    return [rows[i][0] for i in range(start, end) if rows[i][1]]

# Citation surfaces (NOT the spec).
_SURFACE_GLOBS = (
    "guardrails/skills/*/SKILL.md",
    ".claude/commands/*.md",
)
_SURFACE_FILES = (
    "guardrails/CLAUDE.md",
    ".claude/CLAUDE.md",
)

# `gate N (<phrase>)` and `the <phrase> gate (N)`.
_CITE_PARENS = re.compile(r"\bgate\s+(\d+)\s*\(([^)]{2,140})\)")
_CITE_THEGATE = re.compile(r"\bthe\s+([A-Za-z][A-Za-z0-9 ,'/-]{2,90}?)\s+gate\s*\((\d+)\)")

_STOPWORDS = frozenset(
    {"the", "a", "an", "and", "or", "of", "for", "to", "in", "gate", "audit", "gates"})
_ARTICLE_OPEN = re.compile(r"^\s*(the|a|an)\b", re.IGNORECASE)
_HAS_GATE_DIGIT = re.compile(r"\bgate[\s-]+\d")


def parse_inventory(spec_text: str) -> dict[int, str]:
    """Parse the section 6 inventory table: {gate_number: canonical name}.

    Scoped to the section-6 region via :func:`_section6_lines` (fence- and
    container-aware, whitespace-tolerant) so a row, heading, or fence nested in
    a blockquote or a list item is that container's content (3.109 F3), and so
    an inventory-shaped table row ELSEWHERE in the spec (an
    example in section 9, a category table in section 5, a fenced sample) is not
    misread as a gate inventory row (3.109 F2). A spec with no section-6 heading
    RAISES, so a structurally-absent section-6 fails loud (main() maps it to exit 2)
    even when stray numeric rows exist elsewhere, which the pre-fix whole-spec parse
    would have silently collected; a direct caller likewise cannot mistake an absent
    section for valid data. (A truly-empty PARSED inventory was already caught by the
    ``if not inv`` guard in main(); this closes the different miss where section 6 is
    gone but numeric rows elsewhere would have masqueraded as the inventory.)"""
    region = _section6_lines(spec_text)
    if not region:
        raise ValueError("section-6 gate inventory region not found in the spec")
    inv: dict[int, str] = {}
    for line in region:
        m = _INV_ROW.match(line)
        if not m:
            continue
        # skip the header row `| Gate | Name | ... |` and separator `| --- |`
        num_cell = m.group(1)
        if not num_cell.isdigit():
            continue
        name = m.group(2).strip()
        if name and name != "---":
            inv[int(num_cell)] = name
    return inv


def _tokens(name: str) -> set[str]:
    name = name.lower().replace("-", " ")
    raw = re.split(r"[^a-z0-9]+", name)
    return {t for t in raw if t and t not in _STOPWORDS}


def _is_name_citation(phrase: str) -> bool:
    """A parenthetical is a NAME (not a role-gloss/relationship) when it does not
    open with an article and carries no gate-digit cross-reference."""
    if _ARTICLE_OPEN.match(phrase):
        return False
    if _HAS_GATE_DIGIT.search(phrase):
        return False
    return True


def _check_citation(num: int, cited_name: str, inv: dict[int, str]) -> str | None:
    """Return a mismatch description, or None if the citation is consistent."""
    if num not in inv:
        return (f"cites gate {num} but section 6 defines no gate {num} "
                f"(cited name: {cited_name!r})")
    canon = inv[num]
    cited_toks = _tokens(cited_name)
    canon_toks = _tokens(canon)
    if not cited_toks:
        return None  # nothing name-like to compare (e.g. a lone stop-word)
    if cited_toks & canon_toks:
        return None  # shares a significant token: consistent
    return (f"gate {num} is cited as {cited_name!r} but section 6 gate {num} is "
            f"{canon!r} (no shared token: a renumber or a wrong name)")


def scan_text(text: str, inv: dict[int, str]) -> list[str]:
    findings: list[str] = []
    for m in _CITE_PARENS.finditer(text):
        num, phrase = int(m.group(1)), m.group(2).strip()
        if not _is_name_citation(phrase):
            continue
        f = _check_citation(num, phrase, inv)
        if f:
            findings.append(f)
    for m in _CITE_THEGATE.finditer(text):
        phrase, num = m.group(1).strip(), int(m.group(2))
        f = _check_citation(num, phrase, inv)
        if f:
            findings.append(f)
    return findings


def _iter_surface_files() -> list[Path]:
    files: list[Path] = []
    for g in _SURFACE_GLOBS:
        files.extend(sorted(REPO_ROOT.glob(g)))
    for f in _SURFACE_FILES:
        p = REPO_ROOT / f
        if p.is_file():
            files.append(p)
    return files


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    spec_path = REPO_ROOT / SPEC
    try:
        inv = parse_inventory(spec_path.read_text(encoding="utf-8"))
    except Exception as e:  # pragma: no cover
        print(f"ERROR: cannot read the section 6 inventory: {e}", file=sys.stderr)
        return 2
    print("=== gate-name-citation inventory audit ===")
    if not inv:
        print("ERROR: parsed an empty section 6 inventory.", file=sys.stderr)
        return 2
    all_findings: list[str] = []
    surfaces = _iter_surface_files()
    for path in surfaces:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        for f in scan_text(text, inv):
            all_findings.append(f"{rel}: {f}")
    if all_findings:
        for f in all_findings:
            print(f"  {f}")
        print(
            f"\nFAIL: {len(all_findings)} gate-name-citation mismatch(es) against the "
            "section 6 inventory. Correct the citation's name or number to match "
            "section 6 (the ground truth); do not weaken the gate."
        )
        return 1
    print(
        f"OK: {len(surfaces)} citation surface(s) scanned against a "
        f"{len(inv)}-entry inventory; every gate-name citation is consistent."
    )
    return 0


def _self_test() -> int:
    import unittest

    INV = {31: "Document Date staleness audit", 35: "Gate-name parity audit",
           60: "Guardrail-review cadence audit", 41: "Collection-enumeration consistency audit"}

    class T(unittest.TestCase):
        def test_matching_paren_citation_passes(self):
            self.assertEqual(scan_text("see gate 35 (gate-name parity) here.", INV), [])

        def test_matching_thegate_form_passes(self):
            self.assertEqual(
                scan_text("the document-date-staleness gate (31) fires.", INV), [])

        def test_token_overlap_tolerates_style(self):
            # "guardrail-review cadence currency" vs "Guardrail-review cadence audit"
            self.assertEqual(
                scan_text("gate 60 (guardrail-review cadence currency) resets.", INV), [])

        def test_renumber_mismatch_flagged(self):
            # gate 35's name cited on number 41 (a renumber): zero token overlap
            self.assertTrue(scan_text("gate 41 (gate-name parity) here.", INV))

        def test_role_gloss_article_open_skipped(self):
            self.assertEqual(
                scan_text("gate 5 (the enumeration axis, a hand-curated denylist).", INV), [])

        def test_relationship_crossref_skipped(self):
            self.assertEqual(
                scan_text("gate 50 (the gate-48 two-checks-to-four precedent).", INV), [])

        def test_bare_number_list_skipped(self):
            self.assertEqual(scan_text("gates 48 and 49 both fire; gate 41 checks it.", INV), [])

        def test_undefined_number_flagged(self):
            self.assertTrue(scan_text("gate 999 (mystery parity) here.", INV))

        def test_inventory_parse(self):
            spec = ("## 6. Gate inventory (current)\n"
                    "| Gate | Name | Linter |\n| --- | --- | --- |\n"
                    "| 31 | Document Date staleness audit | x |\n"
                    "| 35 | Gate-name parity audit | y |\n")
            inv = parse_inventory(spec)
            self.assertEqual(inv, {31: "Document Date staleness audit",
                                   35: "Gate-name parity audit"})

        def test_inventory_row_outside_section6_ignored(self):
            # 3.109 F2: an inventory-shaped row in a LATER section must NOT be read
            # as a gate (parse_inventory previously scanned the whole spec).
            spec = ("## 6. Gate inventory (current)\n"
                    "| 31 | Document Date staleness audit | x |\n"
                    "## 9. Adding a new gate\n"
                    "| 99 | Not A Real Gate | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Document Date staleness audit"})

        def test_missing_section6_raises(self):
            # 3.109 F2: a structurally-absent section 6 fails loud (main -> exit 2)
            # even when numeric rows exist elsewhere, rather than masquerading as data.
            with self.assertRaises(ValueError):
                parse_inventory("## 9. Other\n| 31 | Document Date staleness audit | x |\n")

        def test_boundary_whitespace_tolerant(self):
            # a markdown-valid indented / tab-after-number heading still ends the region
            for hdr in ("   ## 7. Next", "## 7.\tNext"):
                spec = ("## 6. Gate inventory (current)\n"
                        "| 31 | Document Date staleness audit | x |\n"
                        f"{hdr}\n| 99 | Outside | z |\n")
                self.assertEqual(parse_inventory(spec),
                                 {31: "Document Date staleness audit"}, hdr)

        def test_fenced_headings_and_rows_ignored(self):
            # a fenced ## 6./## 7. or | N | must not start, end, or inject a row
            # into the region (3.109 F2 fence-awareness)
            spec = ("```\n## 6. Fake heading in a fence\n| 98 | Phantom Pre | z |\n```\n"
                    "## 6. Gate inventory (current)\n"
                    "| 31 | Document Date staleness audit | x |\n"
                    "```\n## 7. Fake end in a fence\n| 97 | Phantom Mid | z |\n```\n"
                    "| 35 | Gate-name parity audit | y |\n"
                    "## 7. Real end\n| 99 | Outside | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Document Date staleness audit",
                              35: "Gate-name parity audit"})

        def test_multiple_section6_raises(self):
            # two real section-6 headings is ambiguous -> fail loud, never guess
            with self.assertRaises(ValueError):
                parse_inventory("## 6. One\n| 31 | A | x |\n## 6. Two\n| 35 | B | y |\n")

        def test_nested_fence_length_matching(self):
            # 3.109 F2: a 3-backtick line does NOT close a 4-backtick fence, so the
            # inner heading/row stays fenced and the real section 6 is not swallowed.
            spec = ("````markdown\n```\n## 6. Fake\n| 98 | Phantom | z |\n````\n"
                    "## 6. Real\n| 31 | Real | x |\n## 7. End\n| 99 | out | z |\n")
            self.assertEqual(parse_inventory(spec), {31: "Real"})

        def test_mismatched_fence_char_not_closed(self):
            # a ~~~ line does NOT close a ``` fence (different marker char)
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "```\n~~~\n## 7. Fake in fence\n| 98 | Phantom | z |\n```\n"
                    "| 35 | Also Real | y |\n## 7. End\n| 99 | out | z |\n")
            self.assertEqual(parse_inventory(spec), {31: "Real", 35: "Also Real"})

        def test_backtick_info_string_with_backtick_is_not_a_fence(self):
            # 3.109 F2-A: a backtick fence's info string may not contain a backtick, so
            # ```` aa ``` does NOT open a fence and the real section 6 is not swallowed.
            spec = ("```` aa ```\n## 6. Real\n| 31 | Real | x |\n## 7. End\n")
            self.assertEqual(parse_inventory(spec), {31: "Real"})

        def test_unicode_line_separators_not_line_breaks(self):
            # 3.109 F2: only LF/CR/CRLF end a line in CommonMark; a Unicode separator
            # after a fence marker must NOT read as a bare close (which splitlines() would
            # allow by breaking the line there), so the inner row stays fenced.
            for sep in ("\u0085", "\u2028", "\u2029", "\u000b", "\u000c"):
                spec = ("## 6. Real\n| 31 | Real | x |\n```\n"
                        f"```{sep}\n| 98 | Phantom | z |\n```\n## 7. End\n")
                self.assertEqual(parse_inventory(spec), {31: "Real"}, repr(sep))

        def test_nonascii_whitespace_after_close_is_not_a_close(self):
            # 3.109 F2-B: only ASCII space/tab may follow a closing fence; a U+00A0 keeps
            # the fence OPEN, so the inner row stays fenced (no phantom injected).
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "```\n```\u00a0\n| 98 | Phantom | z |\n```\n"
                    "## 7. End\n| 99 | out | z |\n")
            self.assertEqual(parse_inventory(spec), {31: "Real"})

        def test_list_nested_fence_ignored(self):
            # 3.109 F3 (the codex case): the fence opens INSIDE the list item,
            # so the heading-shaped line is fenced CODE per CommonMark, never a
            # boundary; the col-0 row after the item closes is top-level again.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "- ```\n  ## 7. Fake in code\n  ```\n"
                    "| 35 | Also Real | y |\n## 7. Real end\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

        def test_blockquote_nested_fence_ignored(self):
            # the fence and the fake heading/row are blockquote content
            # (CommonMark 5.1); the col-0 row after the quote is top-level.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "> ```\n> ## 7. Fake\n> | 98 | Phantom | z |\n> ```\n"
                    "| 35 | Also Real | y |\n## 7. End\n| 99 | out | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

        def test_fence_two_containers_deep_ignored(self):
            # a fence nested list-in-blockquote deep stays fenced while both
            # prefixes match; the col-0 row afterwards is top-level.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "> - ```\n>   ## 7. Fake\n>   ```\n"
                    "| 35 | Also Real | y |\n## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

        def test_ordered_list_nested_fence_ignored(self):
            # an ordered marker (``1.``) gives content indent 3; the 3-space
            # fence and the fake heading are item content (CommonMark 5.2).
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "1. ```\n   ## 7. Fake\n   ```\n"
                    "| 35 | Also Real | y |\n## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

        def test_row_inside_list_item_not_parsed(self):
            # a row on the marker line and one on a continuation line are LIST
            # content per CommonMark, never inventory rows.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "- | 96 | Phantom On Marker | z |\n"
                    "  | 97 | Phantom Continuation | z |\n"
                    "## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real"})

        def test_row_as_lazy_continuation_not_parsed(self):
            # CommonMark lazy continuation: the col-0 row line starts no block,
            # so it continues the open item PARAGRAPH and stays inside it.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "- prose paragraph\n| 96 | Phantom Lazy | z |\n"
                    "## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real"})

        def test_heading_after_container_closes_is_boundary(self):
            # an ATX heading interrupts a paragraph and never lazily continues,
            # so the col-0 ``## 7.`` right after list content ends the region.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "- item prose\n## 7. Real end\n| 99 | Outside | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real"})

        def test_indented_heading_inside_list_not_boundary(self):
            # the same 2-space ``## 7.`` shape that bounds the region at true
            # top level (test_boundary_whitespace_tolerant) is item CONTENT
            # here (indent 2 >= content indent 2): only block structure can
            # distinguish the two (3.109 F3).
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "- item\n  ## 7. Fake inside item\n"
                    "| 35 | Also Real | y |\n## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

        def test_blockquote_dedent_closes_fence(self):
            # fenced code has NO lazy continuation: losing the ``>`` prefix
            # closes the quote AND its fence (CommonMark 5.1, spec example
            # 226), so this col-0 heading is REAL and ends the region.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "> ```\n## 7. Real end\n| 99 | Outside | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real"})

        def test_empty_item_blank_then_indented_heading_is_boundary(self):
            # an item that begins EMPTY holds at most one blank line
            # (CommonMark 5.2), so the item closed at the blank and the
            # 2-space ATX heading is a real top-level region end.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "-\n\n  ## 7. Real end\n| 99 | Outside | z |\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real"})

        def test_top_level_fence_still_fence(self):
            # container-awareness must not regress the plain top-level fence.
            spec = ("## 6. Real\n| 31 | Real | x |\n"
                    "```\n## 7. Fake\n| 98 | Phantom | z |\n```\n"
                    "| 35 | Also Real | y |\n## 7. End\n")
            self.assertEqual(parse_inventory(spec),
                             {31: "Real", 35: "Also Real"})

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
