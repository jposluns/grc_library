#!/usr/bin/env python3
"""Gate-name-citation inventory audit (gate 77; TODO section 3.56a guard 2).

Wiring sections, command stubs, and the CLAUDE.md files cite gates by number
AND name, for example ``gate 35 (gate-name parity)`` or ``the
document-date-staleness gate (31)``. When a gate is renumbered, such a citation
can silently point its number at a DIFFERENT gate while keeping the old name, a
drift no other gate catches. This gate is the renumbering guard: for each
genuine gate-name citation it compares the cited NAME against the canonical name
that the audit-programme specification's section 6 inventory records for that
NUMBER, and flags a citation whose name shares NO significant token with the
number's current canonical name (the shape a renumber produces).

FP-safety (census-derived, TODO section 3.56a; the census is
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

# Citation surfaces (NOT the spec).
_SURFACE_GLOBS = (
    "dev-security/claude-rules/skills/*/SKILL.md",
    ".claude/commands/*.md",
)
_SURFACE_FILES = (
    "dev-security/claude-rules/CLAUDE.md",
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
    """Parse the section 6 inventory table: {gate_number: canonical name}."""
    inv: dict[int, str] = {}
    for line in spec_text.splitlines():
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
            spec = ("| Gate | Name | Linter |\n| --- | --- | --- |\n"
                    "| 31 | Document Date staleness audit | x |\n"
                    "| 35 | Gate-name parity audit | y |\n")
            inv = parse_inventory(spec)
            self.assertEqual(inv, {31: "Document Date staleness audit",
                                   35: "Gate-name parity audit"})

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
