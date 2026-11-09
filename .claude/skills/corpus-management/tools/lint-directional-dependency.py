#!/usr/bin/env python3
"""Directional-dependency audit (grc gate): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_directional_dependency.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-directional-dependency``, enforcing the pack's
``directional-dependency`` clause); this thin wrapper keeps the house
``python3 .claude/skills/corpus-management/tools/lint-directional-dependency.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the repo root, the grc
project-governance directory path (``PROJECT_GOV_DIR``), the derived deliverable-corpus scan roots,
the non-deliverable exempt prefixes, and the target selection. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them; ``iter_markdown_files`` stays
here so the scan-scope regression's ALLOW map observes it unmoved.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-directional-dependency.py
    python3 .claude/skills/corpus-management/tools/lint-directional-dependency.py path1 path2 ...
    python3 .claude/skills/corpus-management/tools/lint-directional-dependency.py --self-test

Exit codes are the engine's: 0 clean; 1 finding(s).
"""

from __future__ import annotations

import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, PROJECT_SPECS_DIR, REPO_ROOT, guard_explicit_paths, positional_args, self_test_requested

PACK_TOOLS = REPO_ROOT / ".claude" / "skills" / "corpus-management" / "src" / "tools"

# The grc project-internal governance directory a deliverable-corpus document must not link into
# (decision D5: the registers directory, formerly .project-governance). It is the exact string
# lint_common.AUDITED_DOMAIN_DIRS carries, so the derivation of DEFAULT_CORPUS_ROOTS below removes
# it; a repository-relative POSIX path, matched by the engine as a contiguous run of path parts.
PROJECT_GOV_DIR = ".claude/skills/corpus-management/registers"
if PROJECT_GOV_DIR not in AUDITED_DOMAIN_DIRS:
    raise SystemExit(
        f"lint-directional-dependency: PROJECT_GOV_DIR {PROJECT_GOV_DIR!r} is not in "
        "lint_common.AUDITED_DOMAIN_DIRS; the two must name the same directory."
    )

# Non-deliverable subtrees that are absent from the derived scan roots, kept
# as an explicit exemption (defence-in-depth) for an explicit-path invocation;
# they MAY link into the registers directory per separation-spec section 4. Path
# prefixes are relative to REPO_ROOT, POSIX form. The pack source tree is the
# non-deliverable subtree named here; .working/ and the rest of .claude/ are
# likewise absent from the scan roots below.
EXEMPT_PREFIXES: tuple[str, ...] = (".claude/skills/corpus-management/src/",)

# Root-level deliverable documents (the published library specifications
# and front matter), matching the broken-link checker's root set minus
# the tooling/generated surfaces it additionally scans.
ROOT_DELIVERABLE_DOCS: tuple[str, ...] = (
    "README.md",
    "NOTICE.md",
    "governance/specification-master-project.md",
    "governance/specification-ingestion.md",
    ".claude/skills/corpus-management/specs/instruction-ai-document-ingestion.md",
)

# Deliverable-corpus scan roots: the audited domain directories minus the
# project-governance directory (derived from the single source of truth so
# a future audited domain propagates here, and so this gate does not
# itself hardcode the domain run), the moved specifications directory, plus
# the root deliverable documents. D5 / RBQ64 (chunk CR2A): before the move this
# gate scanned S1 and S2 in governance/ and S3 at the root, so the specifications
# are scanned as corpus documents and may not link into the registers directory;
# the adopter guides (formerly docs/) were outside this gate's roots and stay out.
DEFAULT_CORPUS_ROOTS: list[str] = [
    *(d for d in AUDITED_DOMAIN_DIRS if d != PROJECT_GOV_DIR),
    PROJECT_SPECS_DIR,
    *ROOT_DELIVERABLE_DOCS,
]


def _is_exempt(path: Path) -> bool:
    """True if ``path`` is under a non-deliverable exempt subtree."""
    try:
        rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return False  # outside the repo (a temp-dir fixture): not exempt
    return any(rel.startswith(prefix) for prefix in EXEMPT_PREFIXES)


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = (REPO_ROOT / p) if not Path(p).is_absolute() else Path(p)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    # Exclude the project-governance tree itself (links within it are
    # allowed) and the non-deliverable exempt subtrees (the pack source).
    in_project_gov = _engine().path_in_project_gov
    kept = [
        f
        for f in files
        if not in_project_gov(f.resolve(), PROJECT_GOV_DIR) and not _is_exempt(f)
    ]
    return sorted(set(kept))


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_directional_dependency  # the pack-owned engine (source of record)
    return gate_lint_directional_dependency


def main(argv: list[str]) -> int:
    explicit = positional_args(argv[1:])
    if self_test_requested(argv[1:], explicit):
        return _engine()._self_test()
    # 3b50: refuse (exit 2) a missing explicit path instead of passing silently. Content-only:
    # the check resolves each link against the file's own location and tests it against this
    # tree's project-governance directory, which is sound for a file in another tree (the
    # regression fixtures live in temp directories by design).
    paths = guard_explicit_paths(explicit, allow_outside=True) if explicit else DEFAULT_CORPUS_ROOTS
    return _engine().run(
        iter_markdown_files(paths), project_gov_dir=PROJECT_GOV_DIR, repo_root=REPO_ROOT
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
