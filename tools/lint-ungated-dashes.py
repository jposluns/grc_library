#!/usr/bin/env python3
"""Ungated-surface dash audit (grc gate 82): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_ungated_dashes.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-ungated-dashes``, enforcing the pack's
``language-convention`` clause, the SAME clause the corpus language gate enforces); this thin
wrapper keeps the house ``python3 tools/lint-ungated-dashes.py`` shape (gate 35 parses
exactly that) and supplies the grc-local scan configuration the pack engine deliberately does
not carry: the AIQT bootstrap, the repo root, and the OPERATIONAL scan scope (the surfaces
``lint-language.py`` does NOT walk). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; the linter-regression suite and gate 99's
entry-point existence check are the wrapper's mechanical coverage. ``_targets`` stays here
(grc scan config) so the scan-scope regression's WALKERS map observes it unmoved.

Scope: ``tools/*.py`` and ``tools/*.sh`` (tool comments and docstrings), everything under
``.claude/`` (CLAUDE.md, commands, hooks, the loaded rule copies), everything under
``references/`` (the activity playbooks), and everything under ``.corpus-management/`` (the
Corpus-Management pack source). ``lint-language.py`` enforces the same no-em/en-dash house
style on the CORPUS (``.md`` domain docs) and generator-source prose, but does not scan these
operational surfaces; PR #1314 swept them clean and this gate prevents re-drift.

Exemptions (each principled, not a drive-by allow-list):
  - ``.claude/rules/external/`` : the THIRD-PARTY overlay (addyosmani / kariedo / tikitribe,
    each under its own MIT licence and PROVENANCE.md). It is refreshed FROM SOURCE, never
    hand-edited to conform to this project's house style, so its Unicode dashes are legitimate
    external content.
  - A glyph inside a markdown inline-code backtick span or a fenced code block: the deliberate
    illustration / functional form (handled by the engine's PURE check).
  - The standard exempt dirs (``.git``, ``__pycache__``, ``node_modules``) and non-text
    artefacts.

Usage:
    python3 tools/lint-ungated-dashes.py
    python3 tools/lint-ungated-dashes.py --self-test

Exit codes are the engine's: 0 clean; 1 findings.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path

EXEMPT_DIR_PARTS = {".git", "__pycache__", "node_modules"}
# The third-party overlay, exempt as external-licensed content (see docstring).
EXTERNAL_OVERLAY = REPO_ROOT / ".claude" / "rules" / "external"
TEXT_SUFFIXES = {".py", ".md", ".sh", ".yml", ".yaml", ".json", ".txt", ".toml"}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ungated_dashes  # the pack-owned engine (source of record)
    return gate_lint_ungated_dashes


def _targets():
    """The files in scope: tools/*.py, tools/*.sh, .claude/**, references/**, .corpus-management/** (the pack source)."""
    out = []
    # tools/ operational SCRIPTS (.py and .sh) carry prose comments/docstrings; the tool config
    # data files (.json) are not prose and are not scanned here.
    for pat in ("*.py", "*.sh"):
        for f in sorted((REPO_ROOT / "tools").glob(pat)):
            out.append(f)
    for base in (".claude", "references", ".corpus-management"):
        root = REPO_ROOT / base
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("*")):
            if not f.is_file():
                continue
            if any(part in EXEMPT_DIR_PARTS for part in f.parts):
                continue
            if EXTERNAL_OVERLAY in f.parents:
                continue
            if f.suffix.lower() not in TEXT_SUFFIXES:
                continue
            out.append(f)
    return out


def _self_test() -> int:
    engine = _engine()
    checks = list(engine.pure_self_test_checks())

    def c(name, cond):
        checks.append((name, cond))

    # _targets() scope (the logic that hid the tools/*.sh gap from unit tests; dual-family
    # finding): tools/ scripts .py AND .sh are in scope; the third-party overlay is excluded.
    tgt = _targets()
    c("targets-includes-sh", any(t.name == "pre-push-guard.sh" for t in tgt))
    c("targets-includes-py", any(t.name == "lint-ungated-dashes.py" for t in tgt))
    c("targets-excludes-external", not any("rules" in t.parts and "external" in t.parts for t in tgt))
    c("targets-includes-corpus-management", any(".corpus-management" in t.parts for t in tgt))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"lint-ungated-dashes self-test: FAIL {bad}")
        return 1
    print(f"lint-ungated-dashes self-test: OK ({len(checks)} checks)")
    return 0


def main(argv) -> int:
    if "--self-test" in argv:
        return _self_test()
    engine = _engine()
    return engine.run(_targets(), repo_root=REPO_ROOT)


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument other than --self-test; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ("--self-test",))
    sys.exit(main(sys.argv[1:]))
