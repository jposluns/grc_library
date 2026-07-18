#!/usr/bin/env python3
"""Detect orphan documents: artefacts with zero inbound references.

A document that exists in the repo but is never referenced by any
other document is either dead weight or unintentionally hidden from
adopters. This linter builds the reverse-reference graph and flags
artefacts with no inbound links.

Entry-point documents (the main README, NOTICE, AUTHORS, CHANGELOG,
TODO, CONTRIBUTING, SECURITY) are exempt because they are reached by
filename convention rather than by inbound link. LICENSE and
CITATION.cff were previously listed but removed in Phase 23.62
since the scanner skips non-.md files and they are auto-exempt.

Domain READMEs are exempt because they are reached by directory
navigation. Worklists are exempt because they are working artefacts.
The ``claude-rules`` directory is also exempt: rule files there are
loaded by tooling, not referenced by markdown documents.

Usage:
    python3 tools/lint-orphan-documents.py

Exit codes:
    0   no orphans (every artefact has at least one inbound reference)
    1   one or more orphan documents detected
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS

ALWAYS_EXEMPT = {
    # Entry-point documents reached by filename convention.
    # Phase 23.62 removed `LICENSE` and `CITATION.cff` from this set:
    # `is_artefact` returns False for non-`.md` files before reaching
    # the ALWAYS_EXEMPT check, so those two entries were unreachable.
    "README.md", "NOTICE.md", "AUTHORS.md",
    "CHANGELOG.md", "TODO.md", "CONTRIBUTING.md", "SECURITY.md",
    # RESUME.md is a manual session-resume entry point opened by filename
    # convention (its own header: "manual entry point"), the same category as
    # the other root entry points above. Its only markdown-linked referrer was
    # a CHANGELOG entry body; the plain-language CHANGELOG rework (TODO 3.16)
    # collapses bodies, so relying on that incidental link is fragile. It is
    # reached by convention, not by inbound link, so it is exempt like its peers.
    "RESUME.md",
    # Generated public bibliography (tools/build-reference-manifest.py): reached by
    # the /adopt bootstrap and its standalone purpose, not by an inbound corpus link,
    # the same convention-reached category as RESUME.md (TODO 1.19.7).
    "reference-acquisition-manifest.md",
}

# Reference patterns: markdown links to local files.
# `[text](path)` or `[text](path#anchor)`. We extract the path.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def is_artefact(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in ALWAYS_EXEMPT:
        return False
    # Domain READMEs (any README.md in subdirs) are entry points by convention.
    if path.name == "README.md":
        return False
    # Worklists are working artefacts.
    if path.name.startswith("worklist-"):
        return False
    # claude-rules files are standalone drag-and-drop artefacts referenced
    # by the claude-rules README's tree diagram (plain-text, not markdown
    # links). Their inbound-link semantics differ from library artefacts.
    if "claude-rules" in path.parts:
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
        if p.suffix == ".md" and not any(part in EXEMPT_DIR_PARTS for part in p.parts)
    ]


def normalise_link(referrer: Path, target_text: str) -> Path | None:
    """Resolve a markdown link target to a repo-relative Path, or None."""
    # Strip anchor
    if "#" in target_text:
        target_text = target_text.split("#", 1)[0]
    target_text = target_text.strip()
    if not target_text:
        return None
    # Skip external
    if target_text.startswith(("http://", "https://", "mailto:", "ftp://")):
        return None
    base = referrer.parent
    try:
        resolved = (base / target_text).resolve()
    except (OSError, ValueError):
        return None
    try:
        rel = resolved.relative_to(REPO_ROOT)
    except ValueError:
        return None
    return REPO_ROOT / rel


def build_reverse_graph(all_md: list[Path]) -> dict[Path, set[Path]]:
    """Return {referenced_path -> {set of referrers}}."""
    rev: dict[Path, set[Path]] = defaultdict(set)
    for f in all_md:
        text = read_text_safe(f)
        if text is None:
            continue
        for _lineno, line in iter_non_code_lines(text):
            for m in LINK_RE.finditer(line):
                target = normalise_link(f, m.group(1))
                if target is None:
                    continue
                rev[target].add(f)
    return rev


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
