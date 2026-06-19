#!/usr/bin/env python3
"""Skill-to-rule reference-integrity audit.

Each `SKILL.md` file under `dev-security/claude-rules/skills/<name>/` is a
workflow document that DERIVES from a canonical pack rule (typically
under `dev-security/claude-rules/governance/`). The skill's YAML
frontmatter must declare the derivation explicitly via a
``derives_from:`` field whose value is a relative path from the skill
file to the canonical rule's markdown file. This audit enforces that:

  1. Every ``SKILL.md`` under ``dev-security/claude-rules/skills/`` has a
     ``derives_from:`` field in its YAML frontmatter.
  2. The path named by ``derives_from:`` resolves to an existing file in
     the repository.

The audit does not perform a semantic check: it does not verify that the
skill's Process steps match the rule's protocol, only that the rule
exists. A semantic check is out of scope (would require parsing both
documents' procedural content and comparing); the link-coverage and
section-anchor audits already catch broken cross-references elsewhere in
the body.

The audit is deliberately permissive when ``dev-security/claude-rules/``
contains no ``skills/`` subdirectory or when ``skills/`` contains no
``SKILL.md`` files: zero skills means nothing to audit. The audit returns
exit code 0 with a "no skills found" note in that case, matching the
bootstrap-friendly pattern used by other gates that audit optional
content (e.g., the version-date-consistency audit when the CHANGELOG has
no entries yet).

The ``--root`` argument overrides the repository root used to resolve
``skills/`` and the ``derives_from:`` target paths. Used by the
regression test suite to point at a synthetic minimal source set with
engineered errors so the linter's detection logic can be exercised.
Default: the repository root derived from this file's location.

Stdlib-only Python 3.11. YAML frontmatter is parsed line-by-line with
regex; this avoids a YAML dependency for what is a fixed key-and-value
contract.

Exit codes:

    0   every SKILL.md declares ``derives_from:`` and the referenced
        file exists; or no SKILL.md files were found (bootstrap pass).
    1   one or more findings.
    2   internal error (a SKILL.md file could not be parsed).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR_REL = "dev-security/claude-rules/skills"

# Matches a YAML frontmatter ``derives_from:`` line. The path captured
# group spans to end-of-line (after stripping leading whitespace), and
# may be quoted (single or double quotes) or bare.
DERIVES_FROM_RE = re.compile(
    r"^\s*derives_from:\s*[\"']?(?P<path>[^\"'\n]+?)[\"']?\s*$",
    re.MULTILINE,
)

# YAML frontmatter delimiter.
FRONTMATTER_DELIMITER = "---"


def extract_frontmatter(text: str) -> str | None:
    """Return the text between the first two ``---`` lines, or None.

    The frontmatter must start at the very first line of the file (no
    leading blank lines or BOM). This matches the convention used by
    every existing SKILL.md in the pack and by the addyosmani overlay.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIMITER:
            return "\n".join(lines[1:i])
    return None


def find_skill_files(root: Path) -> list[Path]:
    skills_dir = root / SKILLS_DIR_REL
    if not skills_dir.is_dir():
        return []
    return sorted(skills_dir.rglob("SKILL.md"))


def check_skill(skill_path: Path, root: Path) -> list[str]:
    findings: list[str] = []
    text = read_text_safe(skill_path)
    if text is None:
        findings.append("file could not be read as UTF-8 text")
        return findings

    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        findings.append(
            "missing YAML frontmatter (file must start with a `---` delimiter)"
        )
        return findings

    match = DERIVES_FROM_RE.search(frontmatter)
    if not match:
        findings.append(
            "missing `derives_from:` field in YAML frontmatter. "
            "Add a line of the form: derives_from: <relative path to canonical rule>"
        )
        return findings

    declared_path = match.group("path").strip()
    if not declared_path:
        findings.append("`derives_from:` field is empty")
        return findings

    # Resolve relative to the skill file's directory.
    resolved = (skill_path.parent / declared_path).resolve()
    try:
        resolved_rel = resolved.relative_to(root)
    except ValueError:
        findings.append(
            f"`derives_from:` path resolves outside the repository: "
            f"{declared_path!r} -> {resolved}"
        )
        return findings

    if not resolved.is_file():
        findings.append(
            f"`derives_from:` target does not exist: "
            f"{declared_path!r} (resolved to {resolved_rel.as_posix()})"
        )
        return findings

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit that every SKILL.md under dev-security/claude-rules/skills/ "
            "declares a derives_from: frontmatter field pointing at an existing "
            "pack rule."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=(
            "Override the repository root used to resolve SKILL.md locations "
            "and derives_from: target paths. Defaults to the repository root "
            "derived from this file's location."
        ),
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    skill_files = find_skill_files(root)

    if not skill_files:
        print(
            f"OK: no SKILL.md files found under {SKILLS_DIR_REL}/; "
            f"nothing to verify."
        )
        return 0

    total_findings = 0
    files_flagged = 0
    for skill in skill_files:
        findings = check_skill(skill, root)
        if not findings:
            continue
        files_flagged += 1
        rel = skill.relative_to(root).as_posix()
        print(f"=== {rel} ===")
        for f in findings:
            print(f"  [derives-from] {f}")
            total_findings += 1

    if total_findings == 0:
        return 0

    print(
        f"\nFAIL: {total_findings} derives-from finding(s) across "
        f"{files_flagged} SKILL.md file(s). Each skill must declare a "
        f"`derives_from:` YAML frontmatter field whose value is a relative "
        f"path to the canonical pack rule the skill derives from."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
