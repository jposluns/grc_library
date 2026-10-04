#!/usr/bin/env python3
"""Broken-internal-link audit (grc gate 3): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_links.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-links``, enforcing the pack's ``markdown-link-resolution``
clause); this thin wrapper keeps the house ``python3 tools/lint-links.py`` shape (gate 35
parses exactly that) and supplies the grc-local scan configuration the pack engine
deliberately does not carry: the AIQT bootstrap, the repo root, and the scope
selector (``iter_markdown_files``). By default, scan existing tracked ``.md`` files
from Git's index, excluding ``.corpus-management/`` and configured adopter overlays.
New directories need no allow-list update. Untracked Markdown is checked only via
explicit paths, whose recursive selection is unchanged. Renamed provenance files
remain included. Git selection failures return 2 rather than passing an empty scan.
These wrapper bytes are HAND-MAINTAINED, not compiler-generated.

Usage:
    python3 tools/lint-links.py
    python3 tools/lint-links.py path1 path2 ...

Exit codes: 0 clean; 1 broken link(s); 2 invalid paths or selection failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from external_overlay import RULE_PROVENANCE_PATHS
from lint_common import REPO_ROOT, guard_explicit_paths, iter_scan_roots_markdown, is_default_exempt_root, is_adopter_exempt  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


def iter_markdown_files(paths: list[str] | None = None) -> list[Path]:
    if paths is None:
        tracked = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        )
        files = {
            REPO_ROOT / os.fsdecode(name)
            for name in tracked.split(b"\0") if name.endswith(b".md")
        }
        files = {p for p in files if p.is_file()
                 and not is_default_exempt_root(p, repo_root=REPO_ROOT)
                 and not is_adopter_exempt(p, repo_root=REPO_ROOT)}
        roots = [REPO_ROOT]
    else:
        files = set(iter_scan_roots_markdown(paths, repo_root=REPO_ROOT))
        roots = [REPO_ROOT / p for p in paths]
    # The renamed provenance still contains Markdown links. Include it for
    # both directory scans and explicit-file scans, without adding arbitrary txt.
    for rel in RULE_PROVENANCE_PATHS:
        path = REPO_ROOT / rel
        if path.is_file() and any(p == path or p in path.parents for p in roots):
            files.add(path)
    return sorted(files)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_links  # the pack-owned engine (source of record)
    return gate_lint_links


def main(argv: list[str]) -> int:
    # Explicit paths are refused when unsound and normalized otherwise (3b21).
    paths = guard_explicit_paths(argv[1:], repo_root=REPO_ROOT) if argv[1:] else None
    try:
        files = iter_markdown_files(paths)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: cannot select link-audit files: {exc}", file=sys.stderr)
        return 2
    return _engine().run(files, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
