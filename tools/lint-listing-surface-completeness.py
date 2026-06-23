#!/usr/bin/env python3
"""Listing-surface completeness audit.

A "listing surface" is a file that enumerates corpus documents, such
that adding a new document of the relevant kind obliges updating that
surface. This gate enforces completeness for the MECHANICAL listing
surfaces -- those with a deterministic inclusion rule -- against the
canonical active-document set recorded in ``taxonomy.yml`` (itself kept
in sync with document metadata by the taxonomy-sync gate).

MECHANICAL surfaces gated here:

  1. ``governance/register-document-index-and-classification.md`` -- the
     authoritative active-document index. Rule: every domain-prefixed
     active document must appear in the index table. Root-level
     meta-specifications (``specification-*.md`` at the repository root)
     are exempt: the register is organized by domain and has never
     indexed root-level meta-specs, which describe the library's own
     infrastructure rather than its GRC content. The exemption is
     explicit and documented here rather than a silent skip.

  2. Each domain README (``ai/README.md`` ... ``supply-chain/README.md``).
     Rule: every active document whose path begins with that domain
     directory must be referenced (as a repository-path link) somewhere
     in the domain README. The whole README is scanned rather than a
     single fixed section because the domain READMEs do not share one
     listing-section name: most use "## Active documents", but the
     compliance README lists across "## Core compliance documents
     (root)" and "## Sector sub-directories" (it has sector
     sub-directories). Cross-domain links a README may carry
     (references to documents in other domains) are not flagged; only
     missing own-domain documents are a finding.

SEMANTIC surfaces -- the framework matrices and crosswalks, the
glossary and key-terms registers, and per-document ``Related Documents``
fields -- are deliberately NOT gated here. Their inclusion rule is
relevance- or materiality-based, so a hard completeness gate would be
noisy and would erode gate-discipline (a gate that cries wolf gets
ignored or weakened). The companion authoring tool
``tools/suggest-listing-surfaces.py`` emits high-recall candidate
surfaces for a new document, including the semantic ones, for a human
to ratify.

The canonical source of truth is ``taxonomy.yml`` rather than a
filesystem walk so that the active-document set this gate enforces is
exactly the set the taxonomy-sync gate already validates against the
document metadata; the two gates therefore cannot disagree about what
"active" means.

Exit codes: 0 pass, 1 findings (incompleteness detected), 2 internal error.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

TAXONOMY = "taxonomy.yml"
REGISTER = "governance/register-document-index-and-classification.md"

# The register lists its documents under one clean index section; the
# domain READMEs vary in section structure, so they are scanned whole.
REGISTER_SECTION = "Active document index"

# Matches a corpus document path inside a markdown code span, e.g.
# `ai/framework-ai-governance-and-risk.md`. Requires a domain-dir
# prefix (a "/" before the basename) so bare-filename mentions in prose
# are not mistaken for index entries.
PATH_IN_CODESPAN = re.compile(r"`([a-z][a-z0-9-]*(?:/[a-z0-9._-]+)+\.md)`")

# Matches a taxonomy active-document path entry.
TAXONOMY_PATH = re.compile(r'^- path: "([^"]+)"', re.M)


@dataclass(frozen=True)
class Finding:
    surface: str
    missing: tuple[str, ...]
    extra: tuple[str, ...]


def active_documents() -> set[str]:
    """Return the canonical active-document path set from taxonomy.yml."""
    text = read_text_safe(REPO_ROOT / TAXONOMY)
    if text is None:
        raise RuntimeError(f"taxonomy not readable: {TAXONOMY}")
    paths = set(TAXONOMY_PATH.findall(text))
    if not paths:
        raise RuntimeError("no active-document paths parsed from taxonomy.yml")
    return paths


def paths_in_section(file_rel: str, section_header: str) -> set[str]:
    """Extract domain-prefixed document paths listed under a named H2 section.

    The section runs from the line ``## <section_header>`` to the next
    ``## `` heading (or end of file). Only paths inside markdown code
    spans are collected.
    """
    text = read_text_safe(REPO_ROOT / file_rel)
    if text is None:
        raise RuntimeError(f"listing surface not readable: {file_rel}")
    lines = text.splitlines()
    header_re = re.compile(r"^##\s+" + re.escape(section_header) + r"\s*$")
    start = None
    for i, line in enumerate(lines):
        if header_re.match(line):
            start = i + 1
            break
    if start is None:
        raise RuntimeError(
            f"section '## {section_header}' not found in {file_rel}"
        )
    collected: set[str] = set()
    for line in lines[start:]:
        if line.startswith("## "):
            break
        for m in PATH_IN_CODESPAN.finditer(line):
            collected.add(m.group(1))
    return collected


def paths_in_file(file_rel: str) -> set[str]:
    """Extract all domain-prefixed document paths referenced anywhere in a file."""
    text = read_text_safe(REPO_ROOT / file_rel)
    if text is None:
        raise RuntimeError(f"listing surface not readable: {file_rel}")
    return set(PATH_IN_CODESPAN.findall(text))


def is_register_required(path: str) -> bool:
    """Whether an active document must appear in the index register.

    Domain-prefixed documents (those with a "/" in the path) are
    required. Root-level documents (no "/") are exempt: the register is
    domain-organized and root-level meta-specifications are
    library-infrastructure, not indexed GRC content.
    """
    return "/" in path


def domain_of(path: str) -> str | None:
    """Return the top-level domain directory of a path, or None for root-level."""
    return path.split("/", 1)[0] if "/" in path else None


def check_register(active: set[str]) -> Finding | None:
    required = {p for p in active if is_register_required(p)}
    listed = paths_in_section(REGISTER, REGISTER_SECTION)
    missing = tuple(sorted(required - listed))
    # An "extra" is a path listed in the register that is not an active
    # document at all -- a stale or mistyped entry.
    extra = tuple(sorted(p for p in listed if p not in active))
    if missing or extra:
        return Finding(surface=REGISTER, missing=missing, extra=extra)
    return None


def check_domain_readmes(active: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    domains = sorted({d for p in active if (d := domain_of(p)) is not None})
    for domain in domains:
        readme = f"{domain}/README.md"
        if not (REPO_ROOT / readme).is_file():
            # A domain with active documents but no README is itself a
            # completeness defect.
            findings.append(
                Finding(
                    surface=readme,
                    missing=tuple(
                        sorted(p for p in active if domain_of(p) == domain)
                    ),
                    extra=(),
                )
            )
            continue
        required = {p for p in active if domain_of(p) == domain}
        listed = paths_in_file(readme)
        missing = tuple(sorted(required - listed))
        # Do NOT flag README "extra" entries: a domain README may
        # legitimately link to documents in other domains.
        if missing:
            findings.append(Finding(surface=readme, missing=missing, extra=()))
    return findings


def main(argv: list[str]) -> int:
    try:
        active = active_documents()
        findings: list[Finding] = []
        reg = check_register(active)
        if reg is not None:
            findings.append(reg)
        findings.extend(check_domain_readmes(active))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not findings:
        n_domains = len({domain_of(p) for p in active if domain_of(p)})
        print(
            f"OK: {len(active)} active document(s); register index and "
            f"{n_domains} domain README(s) are complete."
        )
        return 0

    for finding in findings:
        print(f"=== {finding.surface} ===")
        if finding.missing:
            print(
                "  active documents missing from this listing surface: "
                + ", ".join(finding.missing)
            )
        if finding.extra:
            print(
                "  listed paths that are not active documents (stale/typo): "
                + ", ".join(finding.extra)
            )
    print(
        f"\nFAIL: {len(findings)} listing-surface completeness finding(s). "
        f"Each MECHANICAL listing surface must enumerate every active "
        f"document in its scope (the register: every domain-prefixed "
        f"document; a domain README: every document in that domain). "
        f"Resolve by adding the missing document(s) to the surface, or "
        f"correcting a stale entry. SEMANTIC surfaces (matrices, "
        f"glossary, Related Documents) are not gated; use "
        f"tools/suggest-listing-surfaces.py for those.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
