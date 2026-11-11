#!/usr/bin/env python3
"""Stub-document audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_stub_documents.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-stub-documents``, enforcing the pack's ``no-stub-documents``
clause); this thin wrapper keeps the house ``python3 .claude/skills/corpus-management/tools/lint-stub-documents.py`` shape (gate 35
parses exactly that) and supplies the grc-local configuration the pack engine deliberately does not
carry: the AIQT bootstrap, the repo root, the target selection (the exempt files, the ``template-``
/ ``worklist-`` / ``Status: Superseded`` skips, the narrative / default-exempt predicates via
``is_target`` + ``iter_targets``), and the default scan root. The stub-phrase list and word-count
threshold are profile-loaded (``defaults/grc/stubs.toml`` via ``_stubs_config()``) and passed to the
engine's generic check. These wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99
does NOT own them; ``is_target`` / ``iter_targets`` / ``main`` stay HERE (grc config) so the
scan-scope regression's WALKER map and the CLI tests observe them unmoved.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-stub-documents.py
    python3 .claude/skills/corpus-management/tools/lint-stub-documents.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: verifies the vendored AIQT pack .claude/aiqt/ and publishes aiqt_corpus in sys.modules
from lint_common import guard_explicit_paths_cwd, is_default_exempt_root, DEFAULT_EXEMPT_DIRS, in_exempt_dir, is_narrative_root, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]


EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS  # narrative-root exclusion is root-anchored via is_narrative_root

# Files exempt because they are indexes / short by design / describe the linter patterns.
# The linter scans `.md` files only, so a non-`.md` entry here would be unreachable.
EXEMPT_FILES = {
    "README.md",  # domain READMEs are indexes; main README is a navigation hub
    "NOTICE.md",  # license notice; short by design
    "AUTHORS.md",
    # .working/CHANGELOG.md describes phase changes including this linter's patterns.
    ".working/CHANGELOG.md",
    # The Audit Programme Specification names this gate in its inventory
    # and therefore contains the literal phrase "stub document".
    "specification-audit-programme.md",
}



# Upstream owns these pinned bytes; gates 98 (lint-aiqt-vendor-digest.py) and
# 37 (lint-claude-rules-sync.py) verify their exact inventory and fidelity
# against the vendored upstream manifest and release root. Short upstream
# rules are not unfinished project-authored documents. (The snapshot lives
# under .claude/, which is already default-exempt; this root-anchored entry is
# defence in depth and documents the ownership.)
EXEMPT_PATHS = {".claude/aiqt": "Pinned upstream AIQT snapshot; no local authorship"}


def is_target(path: Path) -> bool:
    if any(path.resolve().is_relative_to(REPO_ROOT / rel) for rel in EXEMPT_PATHS):
        return False
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return False
    if path.suffix != ".md":
        return False
    if in_exempt_dir(path, EXEMPT_DIR_PARTS, repo_root=REPO_ROOT) or is_narrative_root(path):
        return False
    if path.name in EXEMPT_FILES:
        return False
    # Templates legitimately have placeholder content.
    if path.name.startswith("template-"):
        return False
    # Worklists have blank fields for human completion.
    if path.name.startswith("worklist-"):
        return False
    # Documents marked Status: Superseded (the lifecycle marker) are
    # deliberately short redirect notices and not stubs.
    try:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\*\*Status:\*\*\s+Superseded", text, re.MULTILINE):
            return False
    except (OSError, UnicodeDecodeError):
        pass
    return True


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_stub_documents  # the pack-owned engine (source of record)
    return gate_lint_stub_documents


def _stubs_config():
    """Load the gate-16 stub vocabulary from the pack profile.

    Returns the engine's ``StubVocabulary`` composed from the ``stubs``
    reference-vocabulary profile (``defaults/grc/stubs.toml``, loaded lazily via
    ``profile_loader.load('stubs')``). Fail-closed: a malformed profile raises
    ProfileError / ValueError, never a silent default.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader

    return _engine().stub_vocabulary(**profile_loader.load("stubs"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect stub documents in production library content."
    )
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])
    # Explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    return _engine().run(iter_targets(args.paths), repo_root=REPO_ROOT, vocab=_stubs_config())


if __name__ == "__main__":
    sys.exit(main(sys.argv))
