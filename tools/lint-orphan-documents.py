#!/usr/bin/env python3
"""Orphan-document audit (grc wrapper over the pack-owned engine).

Detect artefact documents with zero inbound references: an orphan artefact is
unreachable from the library's reference graph. Either link to it from a relevant
register/README/related document, or remove it if no longer needed. Entry-point
documents reached by filename convention (root READMEs, CHANGELOG, TODO, RESUME,
the reference manifest, domain READMEs, worklists) and pack files are exempt.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE graph
machinery (``LINK_RE``, ``normalise_link``, ``build_reverse_graph``, parameterized
by ``repo_root``) lives in the pack-owned engine
(``.corpus-management/tools/gate_lint_orphan_documents.py``, source of record). This
wrapper supplies the grc scan scope + artefact policy (``is_artefact`` /
``find_artefacts`` / ``find_all_markdown`` / ``ALWAYS_EXEMPT`` / ``EXEMPT_DIR_PARTS``)
and the orphan aggregation + reporting in ``main``.

Exit codes:
    0   every artefact has at least one inbound reference.
    1   one or more orphan artefacts with zero inbound references.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, DEFAULT_EXEMPT_DIRS, is_narrative_root, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS  # narrative-root exclusion is root-anchored via is_narrative_root (P-1.25 scan-root split)

ALWAYS_EXEMPT = {
    # Entry-point documents reached by filename convention.
    # Phase 23.62 removed `LICENSE` and `CITATION.cff` from this set:
    # `is_artefact` returns False for non-`.md` files before reaching
    # the ALWAYS_EXEMPT check, so those two entries were unreachable.
    "README.md", "NOTICE.md", "AUTHORS.md",
    "CHANGELOG.md", "TODO.md", "TODO-REFERENCE.md", "CONTRIBUTING.md", "SECURITY.md",
    # RESUME.md is a manual session-resume entry point opened by filename
    # convention (its own header: "manual entry point"), the same category as
    # the other root entry points above. Its only markdown-linked referrer was
    # a CHANGELOG entry body; the plain-language CHANGELOG rework (3.16 (closing PR #862))
    # collapses bodies, so relying on that incidental link is fragile. It is
    # reached by convention, not by inbound link, so it is exempt like its peers.
    "RESUME.md",
    # Generated public bibliography (tools/build-reference-manifest.py): reached by
    # the /adopt bootstrap and its standalone purpose, not by an inbound corpus link,
    # the same convention-reached category as RESUME.md (1.19.7 (closing PR #1007)).
    "reference-acquisition-manifest.md",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_orphan_documents  # the pack-owned engine (source of record)
    return gate_lint_orphan_documents


def is_artefact(path: Path) -> bool:
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return False
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts) or is_narrative_root(path):
        return False
    if path.name in ALWAYS_EXEMPT:
        return False
    # Domain READMEs (any README.md in subdirs) are entry points by convention.
    if path.name == "README.md":
        return False
    # Worklists are working artefacts.
    if path.name.startswith("worklist-"):
        return False
    # guardrails pack files are standalone drag-and-drop artefacts referenced
    # by the guardrails README's tree diagram (plain-text, not markdown
    # links). Their inbound-link semantics differ from library artefacts.
    if "guardrails" in path.parts:
        return False
    return True


def find_artefacts() -> list[Path]:
    return [
        p for p in REPO_ROOT.rglob("*.md")
        if is_artefact(p)
    ]


def find_all_markdown() -> list[Path]:
    return [
        p for p in REPO_ROOT.rglob("*.md")
        if p.suffix == ".md" and not any(part in EXEMPT_DIR_PARTS for part in p.parts) and not is_narrative_root(p)
        and not is_default_exempt_root(p, repo_root=REPO_ROOT)
    ]


def build_reverse_graph(all_md: list[Path]) -> dict[Path, set[Path]]:
    """Thin shim delegating to the pack engine (supplying the grc REPO_ROOT)."""
    return _engine().build_reverse_graph(all_md, REPO_ROOT)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect orphan documents with zero inbound references."
    )
    args = parser.parse_args(argv[1:])
    artefacts = find_artefacts()
    all_md = find_all_markdown()
    rev = build_reverse_graph(all_md)
    orphans: list[Path] = []
    for a in artefacts:
        if a not in rev or not rev[a]:
            orphans.append(a)
    if not orphans:
        print(f"OK: every artefact has at least one inbound reference (checked {len(artefacts)} artefacts; {len(all_md)} files in the reference graph).")
        return 0
    print(f"=== orphan documents ===")
    for o in sorted(orphans):
        try:
            rel = o.relative_to(REPO_ROOT)
        except ValueError:
            rel = o
        print(f"  {rel}")
    print(f"\nFAIL: {len(orphans)} orphan document(s) with zero inbound references.")
    print(
        "Orphan artefacts are not reachable from the library's reference "
        "graph. Either link to them from a relevant register, README, or "
        "related document, or remove them if they are no longer needed."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
