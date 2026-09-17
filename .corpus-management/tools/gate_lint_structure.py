#!/usr/bin/env python3
"""Structural index-integrity check (grc gate): pack-owned engine (source of record).

Verify that a documentation corpus organized into domain directories keeps its
central document-index register and its per-domain README indexes complete and
resolvable: every active domain document is referenced by the central index
register AND by its own domain README, and every path those two surfaces
reference actually exists on disk.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine
carries the PURE check (``parse_referenced_paths``, ``iter_domain_files``,
``collect_findings``), fully parameterized by ``repo_root`` and the corpus
structure config (the domain list, the index-register relative path, the
files exempt from the membership rule, and the exempt directory prefixes). It
holds no repository-root or domain policy of its own. The project wrapper
(``tools/lint-structure.py``) supplies the grc domain list, the grc index-register
path, the grc exempt sets, and the ``--root`` handling and grouped reporting in
``main``.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

LINK_TARGET_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")


def parse_referenced_paths(text: str) -> set[str]:
    """Return the set of repository-relative ``.md`` paths a document links to.

    A referenced path is the DISPLAY text of a ``[`path`](target)`` link whose
    display ends in ``.md`` (the corpus convention: the code-span display carries
    the repo-relative path).
    """
    refs = set()
    for m in LINK_TARGET_RE.finditer(text):
        display = m.group(1)
        if display.endswith(".md"):
            refs.add(display)
    return refs


def iter_domain_files(
    domain: str,
    repo_root: Path,
    exempt_from_index: set[str],
    exempt_directory_prefixes: tuple[str, ...],
) -> list[Path]:
    """Return the active (non-README, non-exempt) ``.md`` files under a domain dir."""
    base = repo_root / domain
    if not base.is_dir():
        return []
    files = []
    for f in base.rglob("*.md"):
        rel = f.relative_to(repo_root).as_posix()
        if f.name == "README.md":
            continue
        if rel in exempt_from_index:
            continue
        if any(rel.startswith(p) for p in exempt_directory_prefixes):
            continue
        files.append(f)
    return sorted(files)


def collect_findings(
    repo_root: Path,
    domains: list[str],
    index_rel_path: str,
    exempt_from_index: set[str],
    exempt_directory_prefixes: tuple[str, ...],
) -> list[str]:
    """Return the structural-integrity finding strings for the corpus.

    Four checks: (1) every active domain document is referenced by the central
    index register; (2) every active domain document is referenced by its domain
    README; (3) every path the index register references exists on disk; (4) every
    path each domain README references exists on disk. A missing index register is
    a single terminal finding.
    """
    findings: list[str] = []

    index_path = repo_root / index_rel_path
    if not index_path.exists():
        findings.append(f"FAIL: {index_path} not found.")
        return findings
    index_text = index_path.read_text(encoding="utf-8")
    indexed = parse_referenced_paths(index_text)

    def _domain_files(domain: str) -> list[Path]:
        return iter_domain_files(domain, repo_root, exempt_from_index, exempt_directory_prefixes)

    # (1) every active document is in the index register.
    for domain in domains:
        for f in _domain_files(domain):
            rel = f.relative_to(repo_root).as_posix()
            if rel not in indexed:
                findings.append(f"index miss: {rel} not referenced by {index_rel_path}")

    # (2) every active document is in its domain README.
    for domain in domains:
        readme = repo_root / domain / "README.md"
        if not readme.exists():
            findings.append(f"missing README: {domain}/README.md")
            continue
        readme_refs = parse_referenced_paths(readme.read_text(encoding="utf-8"))
        for f in _domain_files(domain):
            rel = f.relative_to(repo_root).as_posix()
            if rel not in readme_refs:
                findings.append(f"domain README miss: {rel} not referenced by {domain}/README.md")

    # (3) referenced paths in the index actually exist on disk.
    for ref in indexed:
        target = repo_root / ref
        if not target.exists():
            findings.append(
                f"index broken: {index_rel_path} references non-existent {ref}"
            )

    # (4) referenced paths in each domain README actually exist on disk.
    for domain in domains:
        readme = repo_root / domain / "README.md"
        if not readme.exists():
            continue
        for ref in parse_referenced_paths(readme.read_text(encoding="utf-8")):
            target = repo_root / ref
            if not target.exists():
                findings.append(f"README broken: {domain}/README.md references non-existent {ref}")

    return findings
