#!/usr/bin/env python3
"""Orphan-document audit (grc gate): pack-owned engine (source of record).

Build the corpus reverse-reference graph (which documents link to which) and,
paired with the project wrapper's artefact set, detect artefact documents with
zero inbound references. An orphan artefact is unreachable from the library's
reference graph. Fenced code blocks are skipped via ``aiqt_corpus`` (a link inside
a fence is documentation, not a live reference).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE graph machinery (``LINK_RE``, ``normalise_link``, ``build_reverse_graph``),
parameterized by ``repo_root`` so it is repository-root-free. The project wrapper
(``tools/lint-orphan-documents.py``) supplies the grc scan scope + artefact policy
(``is_artefact`` / ``find_artefacts`` / ``find_all_markdown`` / ``ALWAYS_EXEMPT``)
and the orphan aggregation + reporting in ``main``. The engine is scope-free and
repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more orphans.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_orphan_documents: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# Reference patterns: markdown links to local files.
# ``[text](path)`` or ``[text](path#anchor)``. We extract the path.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def normalise_link(referrer: Path, target_text: str, repo_root: Path) -> Path | None:
    """Resolve a markdown link target to a repo-relative Path (under ``repo_root``), or None."""
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
        rel = resolved.relative_to(repo_root)
    except ValueError:
        return None
    return repo_root / rel


def build_reverse_graph(all_md: list[Path], repo_root: Path) -> dict[Path, set[Path]]:
    """Return {referenced_path -> {set of referrers}} over ``all_md`` (paths under ``repo_root``).

    A document's link to ITSELF (a self-link, such as a Repository Path field or an in-page
    reference) is not an inbound reference: the rule requires a link from another document, so a
    self-link-only artefact is still an orphan (P-1.89(a))."""
    rev: dict[Path, set[Path]] = defaultdict(set)
    for f in all_md:
        text = read_text_safe(f)
        if text is None:
            continue
        for _lineno, line in iter_non_code_lines(text):
            for m in LINK_RE.finditer(line):
                target = normalise_link(f, m.group(1), repo_root)
                if target is None or target.resolve() == f.resolve():
                    continue
                rev[target].add(f)
    return rev
