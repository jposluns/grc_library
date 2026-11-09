#!/usr/bin/env python3
"""Ungated-surface dash audit (grc gate 82): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_ungated_dashes.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-ungated-dashes``, enforcing the pack's
``language-convention`` clause, the SAME clause the corpus language gate enforces); this thin
wrapper keeps the house ``python3 .claude/skills/corpus-management/tools/lint-ungated-dashes.py`` shape (gate 35 parses
exactly that) and supplies the grc-local scan configuration the pack engine deliberately does
not carry: the AIQT bootstrap, the repo root, and the OPERATIONAL scan scope (the surfaces
``lint-language.py`` does NOT walk). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; the linter-regression suite and gate 99's
entry-point existence check are the wrapper's mechanical coverage. ``_targets`` stays here
(grc scan config) so the scan-scope regression's WALKERS map observes it unmoved.

Scope: the top-level ``.py`` and ``.sh`` files of ``.claude/skills/corpus-management/tools/``
(tool comments and docstrings), and every file with a text suffix under ``.claude/``
(CLAUDE.md, commands, hooks, the loaded rule copies, ``.claude/references/`` with the activity
playbooks, and ``.claude/skills/corpus-management/src/`` with the Corpus-Management pack
source). The ``.claude/`` walk skips 2 folders: ``.claude/skills/corpus-management/tests/``
and ``.claude/skills/corpus-management/tools/``. In the tools folder only those top-level
scripts are scanned, so its data files and its subfolders are not. The test suite ``.claude/skills/corpus-management/tests/`` is
left out of the ``.claude/`` walk exactly as the pre-move gate never scanned the top-level
``tests/``: its fixtures hold dashes on purpose as test data for the dash checks (scope parity
with the pre-move gate). ``lint-language.py`` enforces the same no-em/en-dash house
style on the CORPUS (``.md`` domain docs) and generator-source prose, but does not scan these
operational surfaces; PR #1314 swept them clean and this gate prevents re-drift.

Exemptions (each principled, not a drive-by allow-list):
  - ``.claude/rules/external/``: the local-only rule overlay that gate 37 still supports for
    adopters. Gate 37's ``LOCAL_ONLY_SUBDIR`` leaves the directory out of its rule-ownership
    check, and its finding for an unowned rule file tells the author to move a local-only
    overlay there. Third-party rules placed there are refreshed from their source, not
    edited to match this project's house style, so their Unicode dashes are external
    content. No shipped file uses the directory, so the exemption matches nothing here.
  - No ``.claude/skills/`` directory is exempt: every skill directory is scanned.
  - A glyph inside a markdown inline-code backtick span or a fenced code block: the deliberate
    illustration / functional form (handled by the engine's PURE check).
  - The standard exempt dirs (``.git``, ``__pycache__``, ``node_modules``) and non-text
    artefacts.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-ungated-dashes.py
    python3 .claude/skills/corpus-management/tools/lint-ungated-dashes.py --self-test

Exit codes are the engine's: 0 clean; 1 findings.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PACK_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: verifies the vendored AIQT pack .claude/aiqt/ and publishes aiqt_corpus in sys.modules
from safe_fs import (  # noqa: E402
    InputError, directory_entries, path_stat, read_utf8, require_inside, walk_files,
)

EXEMPT_DIR_PARTS = {".git", "__pycache__", "node_modules"}
# The local-only rule overlay that gate 37 supports, exempt as external content (see docstring).
EXTERNAL_OVERLAY = REPO_ROOT / ".claude" / "rules" / "external"
# The skill tools directory: its .py and .sh are scanned directly (not its data files), so the
# .claude walk below skips it.
SKILL_TOOLS = Path(__file__).resolve().parent
# The skill test suite: out of scope, as the pre-move top-level tests/ was (see docstring); its
# fixtures hold dashes on purpose as test data.
SKILL_TESTS = SKILL_TOOLS.parent / "tests"
TEXT_SUFFIXES = {".py", ".md", ".sh", ".yml", ".yaml", ".json", ".txt", ".toml"}


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ungated_dashes  # the pack-owned engine (source of record)
    return gate_lint_ungated_dashes


def _targets():
    """Return the files in scope, as the module docstring's Scope paragraph sets out.

    These are the top-level .py and .sh files of .claude/skills/corpus-management/tools/
    and every file with a text suffix under .claude/, including .claude/references/ and the
    pack source in .claude/skills/corpus-management/src/. The .claude/ walk skips
    .claude/skills/corpus-management/tests/, .claude/skills/corpus-management/tools/, and
    the paths that the module docstring exempts. A scanned root (the tools folder or
    .claude/) that resolves outside the repository root is refused.
    """
    out = []
    # .claude/skills/corpus-management/tools/ operational SCRIPTS (.py and .sh) carry prose comments/docstrings; the tool config
    # data files (.json) are not prose and are not scanned here.
    tools = SKILL_TOOLS
    info = path_stat(tools, missing_ok=True)
    if info is not None:
        # A tools folder that is itself a link out of the repository is refused.
        require_inside(tools, REPO_ROOT)
        for f in directory_entries(tools):
            if f.name.endswith((".py", ".sh")):
                # A linked script whose target is outside the tools folder is refused.
                require_inside(f, tools)
                out.append(f)

    def excluded(path):
        return (path.name in EXEMPT_DIR_PARTS or path == EXTERNAL_OVERLAY or path == SKILL_TOOLS
                or path == SKILL_TESTS)

    # The pack source .claude/skills/corpus-management/src/ is under .claude/.
    for base in (".claude",):
        root = REPO_ROOT / base
        info = path_stat(root, missing_ok=True)
        if info is None:
            continue
        require_inside(root, REPO_ROOT)
        for f in walk_files(root, exclude=excluded):
            if f.suffix.lower() in TEXT_SUFFIXES:
                out.append(f)
    return out


def _fixture_targets():
    """_targets() over a throwaway fixture tree holding one file in each scope boundary.

    Hermetic: it does not depend on which directories the live tree happens to hold. Returns
    the in-scope paths relative to the fixture.
    """
    import tempfile
    names = ("REPO_ROOT", "EXTERNAL_OVERLAY", "SKILL_TOOLS", "SKILL_TESTS")
    saved = {n: globals()[n] for n in names}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        skill = root / ".claude" / "skills" / "corpus-management"
        for rel in (".claude/skills/corpus-management/tools/t.py",
                    ".claude/skills/corpus-management/src/s.py",
                    ".claude/skills/corpus-management/tests/x.py",
                    ".claude/hooks/h.py",
                    ".claude/references/r.md"):
            f = root / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("fixture\n", encoding="utf-8")
        try:
            globals().update(REPO_ROOT=root, EXTERNAL_OVERLAY=root / ".claude" / "rules" / "external",
                             SKILL_TOOLS=skill / "tools", SKILL_TESTS=skill / "tests")
            return {t.relative_to(root).as_posix() for t in _targets()}
        finally:
            globals().update(saved)


def _self_test() -> int:
    engine = _engine()
    checks = list(engine.pure_self_test_checks())

    def c(name, cond):
        checks.append((name, cond))

    # _targets() scope (the logic that hid the .claude/skills/corpus-management/tools/*.sh gap from unit tests; dual-family
    # finding): .claude/skills/corpus-management/tools/ scripts .py AND .sh are in scope; the local-only rule overlay
    # that gate 37 supports (.claude/rules/external/) is excluded.
    tgt = _targets()
    c("targets-includes-sh", any(t.name == "pre-push-guard.sh" for t in tgt))
    c("targets-includes-py", any(t.name == "lint-ungated-dashes.py" for t in tgt))
    c("targets-excludes-external", not any("rules" in t.parts and "external" in t.parts for t in tgt))
    # A file in the skill folder itself, outside src/, tools/ and tests/, is scanned.
    c("targets-includes-corpus-management", SKILL_TOOLS.parent / "SKILL.md" in tgt)
    c(
        "targets-includes-cleanlanguage",
        REPO_ROOT / ".claude/skills/cleanlanguage/SKILL.md" in tgt,
    )
    # Scope parity with the pre-move gate: the skill test suite (the old top-level tests/) is out
    # of scope; the pack source, the hooks and .claude/references/ stay in. The live exclusion check
    # needs the suite present with text files, or it would pass over nothing.
    c("targets-skill-tests-present", any(
        f.suffix.lower() in TEXT_SUFFIXES
        for f in walk_files(SKILL_TESTS, exclude=lambda p: p.name in EXEMPT_DIR_PARTS)
    ) if path_stat(SKILL_TESTS, missing_ok=True) is not None else False)
    c("targets-excludes-skill-tests", not any(SKILL_TESTS in t.parents for t in tgt))
    c("targets-includes-skill-src", any(PACK_TOOLS.parent in t.parents for t in tgt))
    c("targets-includes-hooks", any(REPO_ROOT / ".claude" / "hooks" in t.parents for t in tgt))
    fixture = _fixture_targets()
    c("fixture-excludes-skill-tests",
      ".claude/skills/corpus-management/tests/x.py" not in fixture)
    c("fixture-includes-skill-src", ".claude/skills/corpus-management/src/s.py" in fixture)
    c("fixture-includes-skill-tools", ".claude/skills/corpus-management/tools/t.py" in fixture)
    c("fixture-includes-hooks", ".claude/hooks/h.py" in fixture)
    c("fixture-includes-references", ".claude/references/r.md" in fixture)
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"lint-ungated-dashes self-test: FAIL {bad}")
        return 1
    print(f"lint-ungated-dashes self-test: OK ({len(checks)} checks)")
    return 0


def main(argv) -> int:
    try:
        if "--self-test" in argv:
            return _self_test()
        engine = _engine()

        def scan(path):
            return engine.scan_text(read_utf8(path), path.suffix.lower() == ".md")

        return engine.run(_targets(), repo_root=REPO_ROOT, scan=scan)
    except InputError as exc:
        # A refused path outside the repository root has no relative form, so it is
        # shown in full.
        path = exc.path
        shown = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"FAIL: inaccessible-input: {shown}: {exc}")
        return 1


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument other than --self-test; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ("--self-test",))
    sys.exit(main(sys.argv[1:]))
