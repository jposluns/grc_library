#!/usr/bin/env python3
"""Broken-internal-link audit (grc gate 3): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_links.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-links``, enforcing the pack's ``markdown-link-resolution``
clause); this thin wrapper keeps the house ``python3 .claude/skills/corpus-management/tools/lint-links.py`` shape (gate 35
parses exactly that) and supplies the grc-local scan configuration the pack engine
deliberately does not carry: the AIQT bootstrap, the repo root, and the scope
selector (``iter_markdown_files``). By default, scan tracked ``.md`` files
from Git's index, excluding ``.claude/skills/corpus-management/src/`` and configured adopter overlays.
New directories need no allow-list update. Untracked Markdown is checked only via
explicit paths, whose recursive selection is unchanged. The default scan fails
closed (exit 2) when Git selection fails,
when the repo root is not the Git top level, or when it selects no Markdown. Every
selected file must read as UTF-8 or the gate exits 2 naming it, so a tracked file
missing from the checkout or under an unreadable directory is never skipped.
These wrapper bytes are HAND-MAINTAINED, not compiler-generated.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-links.py
    python3 .claude/skills/corpus-management/tools/lint-links.py path1 path2 ...

Exit codes: 0 clean; 1 broken link(s); 2 invalid paths, selection failure, or an
unreadable selected file.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from lint_common import REPO_ROOT, guard_explicit_paths, iter_scan_roots_markdown, is_default_exempt_root, is_adopter_exempt  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"


class SelectionError(Exception):
    """The default selection does not cover the tracked corpus (exit 2)."""


def iter_markdown_files(paths: list[str] | None = None) -> list[Path]:
    if paths is None:
        # Below the Git top level, the index listing covers only part of the repo.
        prefix = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--show-prefix"], text=True,
        ).strip()
        if prefix:
            raise SelectionError(
                f"{REPO_ROOT} is not the Git top level (it is subdirectory {prefix!r})")
        tracked = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        )
        files = {
            REPO_ROOT / os.fsdecode(name)
            for name in tracked.split(b"\0") if name.endswith(b".md")
        }
        # No existence filter: main() fails on any selected file it cannot read.
        files = {p for p in files
                 if not is_default_exempt_root(p, repo_root=REPO_ROOT)
                 and not is_adopter_exempt(p, repo_root=REPO_ROOT)}
        if not files:
            raise SelectionError(f"no tracked Markdown selected under {REPO_ROOT}")
    else:
        files = set(iter_scan_roots_markdown(paths, repo_root=REPO_ROOT))
    return sorted(files)


def unreadable_files(files: list[Path]) -> list[tuple[Path, str]]:
    """Return each selected file that cannot be read as UTF-8, with the reason."""
    failures = []
    for path in files:
        try:
            path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            failures.append((path, str(exc)))
    return failures


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_links  # the pack-owned engine (source of record)
    return gate_lint_links


def main(argv: list[str]) -> int:
    # Explicit paths are refused when unsound and normalized otherwise.
    paths = guard_explicit_paths(argv[1:], repo_root=REPO_ROOT) if argv[1:] else None
    try:
        files = iter_markdown_files(paths)
    except (OSError, subprocess.CalledProcessError, SelectionError) as exc:
        print(f"ERROR: cannot select link-audit files: {exc}", file=sys.stderr)
        return 2
    # A selected file that cannot be read fails the gate; it is never skipped.
    unreadable = unreadable_files(files)
    for path, reason in unreadable:
        shown = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"ERROR: cannot read selected file {shown.as_posix()}: {reason}",
              file=sys.stderr)
    if unreadable:
        return 2
    return _engine().run(files, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
