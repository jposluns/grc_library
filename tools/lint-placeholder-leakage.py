#!/usr/bin/env python3
"""Placeholder-leakage audit (grc gate 12): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_placeholder_leakage.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-placeholder-leakage``, enforcing the pack's ``placeholder-leakage``
clause); this thin wrapper keeps the house ``python3 tools/lint-placeholder-leakage.py`` shape (gate
35 parses exactly that) and supplies the grc-local scan configuration the pack engine deliberately
does not carry: the AIQT bootstrap, the default scan root (whole repo), the markdown target selector
(``iter_targets``, kept here so the scan-scope regression's ALLOW map observes it unmoved), and the
grc exempt policy (``is_exempt`` with the exempt-file set, the exempt-dir set, and the ``template-`` /
``worklist-`` filename-prefix carve-outs). The wrapper filters exempt files out before delegating, so
the engine holds no project-file policy. These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them.

Boundary with the shall-near-uncertainty audit (``lint-shall-near-uncertainty.py``): the two share
five marker tokens (TODO, TBD, FIXME, XXX, [Unverified]) plus a sixth in differing forms (this gate
matches the parenthesized ``(placeholder)``; that one matches bare ``placeholder``), and split by
PRESENCE vs CONJUNCTION. Each maintains its own token list; extend both deliberately.

Usage:
    python3 tools/lint-placeholder-leakage.py
    python3 tools/lint-placeholder-leakage.py path1 path2 ...

Exit codes are the engine's: 0 clean; 1 findings.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, is_adopter_exempt, DEFAULT_EXEMPT_DIRS, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

# Derive the pack tools/ from this file's location, independent of REPO_ROOT.
PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Filenames whose content legitimately mentions these markers.
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "specification-citation-verification.md",
    # The Audit Programme Specification discusses the placeholder linter's
    # rule set and references TODO.md by name; both produce false positives.
    "specification-audit-programme.md",
    # The coverage-gaps register uses "TODO backlog: <topic>" planned-target
    # references to TODO.md items; this is by design, not leakage.
    "register-coverage-gaps.md",
    # The decision tree references TODO.md and coverage gaps by name.
    "decision-tree.md",
}

# Directories whose content is exempt. The default set
# (``.git``/``node_modules``/``__pycache__``) plus ``guardrails``,
# where rule files use angle-bracket placeholders as documentation of
# command syntax, not as template-fill markers.
EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS | {"guardrails"}


def is_exempt(path: Path) -> bool:
    """Return True if the file should be skipped."""
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return True
    # Adopter overlay-exemption (3.183): honor the adopter's private-overlay dir here too,
    # since this gate builds its own exempt set rather than routing through is_target.
    if is_adopter_exempt(path, repo_root=REPO_ROOT):
        return True
    if path.name in EXEMPT_FILES:
        return True
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return True
    # Template documents legitimately contain placeholders.
    if path.name.startswith("template-"):
        return True
    # Worklist documents contain intentional blank fields for human completion.
    if path.name.startswith("worklist-"):
        return True
    # Only scan markdown documents.
    if path.suffix != ".md":
        return True
    return False


def iter_targets(paths: list[str]) -> list[Path]:
    """Walk supplied paths and return markdown files to scan."""
    targets: list[Path] = []
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if not is_exempt(f):
                    targets.append(f)
    # Remove duplicates while preserving order
    seen = set()
    out = []
    for t in targets:
        if t in seen:
            continue
        seen.add(t)
        if not is_exempt(t):
            out.append(t)
    return out


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_placeholder_leakage  # the pack-owned engine (source of record)
    return gate_lint_placeholder_leakage


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect placeholder leakage in production library documents."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=DEFAULT_PATHS,
        help="Files or directories to scan (default: whole repo).",
    )
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    return _engine().run(targets, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
