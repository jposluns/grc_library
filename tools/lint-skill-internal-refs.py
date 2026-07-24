#!/usr/bin/env python3
"""Skill-body internal-reference audit (gate 76; TODO section 3.56a guard 1).

Pack skills under ``dev-security/claude-rules/skills/<name>/SKILL.md`` are
PORTABLE: their body is meant to be project-agnostic so an adopting fork can use
it unchanged. Each skill may carry ONE project-instantiation block, the
``## Project wiring (the parent library's instantiation; adopters substitute
their own)`` section, where concrete project identifiers (gate numbers,
``.working/`` paths, tool filenames, repo names) legitimately live. Outside that
section, a concrete project-internal reference is CONVENTION EROSION: the skill's
portable body has been contaminated with this project's specifics.

This gate flags such a leak. For each pack SKILL.md (except the special ``adopt``
skill, see below), it computes the PORTABLE BODY (every line outside the wiring
section) and flags a line carrying one of these project-internal token classes:

  * a concrete gate number: ``gate <digit>`` (singular; the plural generic forms
    ``N gates`` / ``gates 1-N`` that a skill about the gate machinery uses as
    placeholders are NOT flagged, and neither is ``gates`` without a following
    digit);
  * a ``.working/`` path (a maintainer-working-tree file no adopter has);
  * a PR-number reference ``#NNN`` (three-plus digits);
  * a backlog-section reference ``§N`` / ``§N.M`` / ``PN.M``;
  * a PROJECT tool path ``tools/<name>.(py|sh)`` where ``<name>`` is a REAL tool
    in this repo's ``tools/`` dir (a placeholder like ``tools/build-foo.py`` that
    names no real tool is NOT flagged; the ``.claude/`` tree, the standard Claude
    Code wiring surface every adopter shares, is NOT a project-unique path and is
    NOT flagged);
  * a sibling-repo name ``grc_library_scratch`` / ``grc_library_private`` /
    ``grc_library_ref`` (the bare token ``_private`` is NOT flagged, to avoid the
    ``ipaddress.is_private`` substring false positive; only the full repo name or
    a ``_private/`` path form counts).

Exemptions (census-derived, TODO section 3.56a; the census is
``grc_library_scratch:results/research-guard1-skillbody-tokens-census.md``):

  * The ``adopt`` skill is EXEMPT WHOLESALE: it is inherently the parent
    library's adoption procedure, so its body legitimately names concrete parent
    machinery throughout (the portable-body-versus-wiring split does not apply to
    it).
  * The ``.claude/`` tree is not a project-unique path (every adopter uses the
    same ``.claude/commands/`` and ``.claude/rules/`` wiring), so it is not
    flagged.
  * A ``tools/<name>`` path naming no real tool (a placeholder example) is not
    flagged, via the real-tool existence check.

Precision: the corpus is clean today (the census found zero PR/section refs and
zero unexempted gate/path/repo leaks in skill bodies after the one mild
``citation-quote-verification`` linter-name leak was genericized in the same PR),
so the gate ships GREEN guard-first. A future concrete leak in a portable body is
the failure; the fix is to genericize the body (or move the reference into the
wiring section), never to weaken the gate.

Exit codes: 0 pass, 1 findings (a leak), 2 internal error.

Self-test: ``python3 tools/lint-skill-internal-refs.py --self-test``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from lint_common import REPO_ROOT
except Exception:  # pragma: no cover - allow standalone/self-test import
    REPO_ROOT = Path(__file__).resolve().parent.parent

SKILLS_DIR = "dev-security/claude-rules/skills"

# The single canonical wiring-section heading (census: one marker shape only).
_WIRING_START = re.compile(r"^##\s+Project wiring\b")
# A level-1-or-2 heading closes the wiring section.
_HEADING = re.compile(r"^#{1,2}\s+\S")

# The skill exempt wholesale (inherently the parent's adoption procedure).
EXEMPT_SKILLS = frozenset({"adopt"})

# Token-class patterns applied to a portable-body line.
_PAT_GATE = re.compile(r"\bgate\s+\d+\b")
_PAT_WORKING = re.compile(r"(?<![\w./])\.working/")
_PAT_PR = re.compile(r"#\d{3,5}\b")
# A backlog-section reference is the project's MULTI-LEVEL numbering (`§3.56a`,
# `§5.9`, `§1.22.3`, `PN.M`); it requires at least one dot. A bare single-level
# `§3` / `§8` is a document's OWN section reference (a skill naming its report's
# `§3 Findings` section, or a pack rule's `§1`), which is legitimate and portable,
# so it is NOT flagged (census: zero backlog-section leaks in skill bodies).
_PAT_SECTION = re.compile(r"(?:§\s?\d+\.\d+[a-z]?)|(?:\bP\d+\.\d+\b)")
_PAT_TOOLPATH = re.compile(r"\btools/([A-Za-z0-9_-]+\.(?:py|sh))\b")
_PAT_REPO = re.compile(r"\bgrc_library_(?:scratch|private|ref)\b|(?<![\w])_private/")


def _iter_skill_files() -> list[Path]:
    base = REPO_ROOT / SKILLS_DIR
    if not base.is_dir():
        return []
    return sorted(base.glob("*/SKILL.md"))


def _portable_body_lines(text: str) -> list[tuple[int, str]]:
    """Return (1-indexed line number, line) for every line OUTSIDE the wiring section."""
    lines = text.splitlines()
    in_wiring = False
    out: list[tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        if _WIRING_START.match(line):
            in_wiring = True
            continue
        if in_wiring:
            # A new level-1/2 heading (that is not the wiring heading) closes it.
            if _HEADING.match(line):
                in_wiring = False
                # fall through: this heading line is itself portable body
            else:
                continue
        out.append((i, line))
    return out


def _scan_line(line: str, tools_dir: Path) -> list[str]:
    """Return a list of leak descriptions found on one portable-body line."""
    hits: list[str] = []
    if _PAT_GATE.search(line):
        hits.append(f"concrete gate number ({_PAT_GATE.search(line).group(0)!r})")
    if _PAT_WORKING.search(line):
        hits.append("`.working/` path")
    if _PAT_PR.search(line):
        hits.append(f"PR-number reference ({_PAT_PR.search(line).group(0)!r})")
    m = _PAT_SECTION.search(line)
    if m:
        hits.append(f"backlog-section reference ({m.group(0)!r})")
    for name in _PAT_TOOLPATH.findall(line):
        # Only a REAL project tool counts (a placeholder example does not).
        if (tools_dir / name).is_file():
            hits.append(f"project tool path (`tools/{name}`)")
    if _PAT_REPO.search(line):
        hits.append(f"sibling-repo name ({_PAT_REPO.search(line).group(0)!r})")
    return hits


def scan_skill(path: Path, tools_dir: Path) -> list[str]:
    """Return findings ('<relpath>:<line>: <leak>') for one SKILL.md."""
    skill_name = path.parent.name
    if skill_name in EXEMPT_SKILLS:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    findings: list[str] = []
    for lineno, line in _portable_body_lines(text):
        for leak in _scan_line(line, tools_dir):
            findings.append(f"{rel}:{lineno}: {leak} in a portable skill body")
    return findings


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    tools_dir = REPO_ROOT / "tools"
    all_findings: list[str] = []
    skills = _iter_skill_files()
    for path in skills:
        all_findings.extend(scan_skill(path, tools_dir))
    print("=== skill-body internal-reference audit ===")
    if all_findings:
        for f in all_findings:
            print(f"  {f}")
        print(
            f"\nFAIL: {len(all_findings)} internal-reference leak(s) in portable skill "
            "bodies. A pack skill's body is portable; move the concrete project "
            "reference into the skill's `## Project wiring` section or genericize it. "
            "Do not weaken the gate."
        )
        return 1
    print(
        f"OK: {len(skills)} pack skill(s) scanned; no project-internal reference "
        "leaks in any portable skill body."
    )
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    WIRING = "## Project wiring (the parent library's instantiation; adopters substitute their own)"

    class T(unittest.TestCase):
        def setUp(self):
            self.tmp = Path(tempfile.mkdtemp())
            (self.tmp / "tools").mkdir()
            # a REAL tool for the real-tool check
            (self.tmp / "tools" / "lint-citations.py").write_text("")
            self.tools_dir = self.tmp / "tools"

        def _scan(self, body: str, name: str = "somekill"):
            p = self.tmp / name / "SKILL.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
            return scan_skill(p, self.tools_dir)

        def test_clean_body_passes(self):
            self.assertEqual(self._scan("# Skill\n\nDo the thing generically.\n"), [])

        def test_concrete_gate_flagged(self):
            self.assertTrue(self._scan("# S\n\nThe register guard is gate 50.\n"))

        def test_generic_gate_placeholders_allowed(self):
            # plural "N gates" / "gates 1-N" are placeholders, not concrete
            self.assertEqual(
                self._scan('# S\n\nStale "N gates" or "gates 1-N" prose.\n'), [])

        def test_working_path_flagged(self):
            self.assertTrue(self._scan("# S\n\nWrites to .working/validate-pr/.\n"))

        def test_pr_ref_flagged(self):
            self.assertTrue(self._scan("# S\n\nAs in PR #1042 the fix landed.\n"))

        def test_section_ref_flagged(self):
            self.assertTrue(self._scan("# S\n\nSee §3.56a for the plan.\n"))

        def test_single_level_section_ref_allowed(self):
            # a bare `§3` / `§8` is a document's own section reference, not a
            # project backlog reference; requires a dot to flag
            self.assertEqual(
                self._scan("# S\n\nEvery row in §3 (Findings) and §8 inherits it.\n"), [])

        def test_real_tool_path_flagged(self):
            self.assertTrue(self._scan("# S\n\nRun `tools/lint-citations.py` here.\n"))

        def test_placeholder_tool_path_allowed(self):
            # build-foo.py is not a real tool in tools_dir -> not flagged
            self.assertEqual(
                self._scan("# S\n\ncommonly `tools/build-foo.py` or make.\n"), [])

        def test_claude_tree_path_allowed(self):
            self.assertEqual(
                self._scan("# S\n\nCreate the `.claude/commands/x.md` sibling.\n"), [])

        def test_repo_name_flagged(self):
            self.assertTrue(self._scan("# S\n\nDeliver to grc_library_scratch inbox.\n"))

        def test_bare_is_private_substring_allowed(self):
            self.assertEqual(
                self._scan("# S\n\nPython `ipaddress.is_private` excludes CGNAT.\n"), [])

        def test_wiring_section_is_exempt(self):
            body = f"# S\n\nPortable text.\n\n{WIRING}\n\nUses gate 50 and .working/x here.\n"
            self.assertEqual(self._scan(body), [])

        def test_leak_after_wiring_section_flagged(self):
            # a heading closes the wiring section; a leak below it is portable-body
            body = f"# S\n\n{WIRING}\n\nwiring gate 50 here.\n\n## Overview\n\ngate 63 leak.\n"
            self.assertTrue(self._scan(body))

        def test_adopt_skill_exempt_wholesale(self):
            body = "# Adopt\n\nRun `tools/lint-citations.py`, see gate 50, .working/x, grc_library_ref.\n"
            self.assertEqual(self._scan(body, name="adopt"), [])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
