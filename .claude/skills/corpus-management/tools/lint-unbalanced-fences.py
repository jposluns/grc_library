#!/usr/bin/env python3
"""Unbalanced-fence audit (grc gate 66): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_unbalanced_fences.py`` (Corpus-Management pack,
gate register ``core/gates.toml``, id ``lint-unbalanced-fences``, enforcing the pack's
``corpus-scan-integrity`` clause); this thin wrapper keeps the house
``python3 .claude/skills/corpus-management/tools/lint-unbalanced-fences.py`` shape (gate 35 parses exactly that) and
supplies the grc-local scan configuration the pack engine deliberately does not carry:
the AIQT bootstrap, the repo root, and lint_common's default markdown walk (the
``DEFAULT_EXEMPT_DIRS`` / ``is_default_exempt_root`` exemption plus the explicit-path
iterator). These wrapper bytes are HAND-MAINTAINED, not compiler-generated, so gate 99
does NOT own them; the linter-regression suite (``UnbalancedFenceTests``) and gate 99's
entry-point existence check are the wrapper's mechanical coverage. ``iter_targets`` stays
here (grc scan config) so the scan-scope regression's WALKERS map observes it unmoved.

Scope (unchanged when the engine moved to the pack): a default run walks every ``*.md``
under the repository root, minus both the ``DEFAULT_EXEMPT_DIRS`` path components and the
``is_default_exempt_root`` default-root exemption (``DEFAULT_EXEMPT_ROOTS``, currently
``.claude/skills/corpus-management/src``); explicit path arguments are scanned with ONLY
the default-root exemption applied (no ``DEFAULT_EXEMPT_DIRS`` component filter), so an
explicit ``.claude/`` path IS scanned (the mandated new-pack-prose run) while an explicit
``.claude/skills/corpus-management/src`` path is still default-root-exempted.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-unbalanced-fences.py
    python3 .claude/skills/corpus-management/tools/lint-unbalanced-fences.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 findings; plus 2 when an explicit path is
refused (missing, or relative while not run from the tree root).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PACK_TOOLS = REPO_ROOT / ".claude" / "skills" / "corpus-management" / "src" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: verifies the vendored AIQT pack .claude/aiqt/ and publishes aiqt_corpus in sys.modules
from lint_common import (  # noqa: E402  # grc-config/store, stays local
    is_default_exempt_root,
    in_exempt_dir,
    guard_explicit_paths,
    positional_args,
    iter_scan_roots_markdown,
)


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_unbalanced_fences  # the pack-owned engine (source of record)
    return gate_lint_unbalanced_fences


def iter_targets(paths: list[str]) -> list[Path]:
    if paths:
        return iter_scan_roots_markdown(paths, repo_root=REPO_ROOT)
    files: list[Path] = []
    for f in REPO_ROOT.rglob("*.md"):
        if is_default_exempt_root(f, repo_root=REPO_ROOT):
            continue
        if in_exempt_dir(f, repo_root=REPO_ROOT):
            continue
        files.append(f)
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    argv = positional_args(list(sys.argv[1:] if argv is None else argv), known_flags=())  # '--' separates paths (quick-guard passes one)
    # Explicit paths must exist, and a relative one is accepted only when run from the
    # tree root (it resolves against REPO_ROOT, not the current directory); refused with
    # exit 2 rather than silently passing. The fence check is content-only, so an
    # absolute path in another tree is scanned soundly and stays allowed.
    if argv:
        argv = guard_explicit_paths(argv, repo_root=REPO_ROOT, allow_outside=True)
    engine = _engine()
    return engine.run(iter_targets(argv), repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main())
