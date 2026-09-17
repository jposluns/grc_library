#!/usr/bin/env python3
"""Listing-surface completeness - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the path/taxonomy regexes, Finding, active_documents, paths_in_section,
paths_in_file, is_register_required, domain_of, check_register, check_domain_readmes)
is the source of record here in the pack, moved verbatim from the grc gate. The
corpus layout config (repo root, taxonomy path, register path, register section) is
supplied by the adopter via configure(ref), so the engine carries no project layout;
the grc wrapper (tools/lint-listing-surface-completeness.py) supplies the config,
configures the engine, and keeps module-global shims (active_documents / check_register
/ check_domain_readmes, called by its in-process regression), main, and the exit codes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_listing_surface_completeness: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Corpus layout config: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
REPO_ROOT = None
TAXONOMY = ""
REGISTER = ""
REGISTER_SECTION = ""


def configure(ref) -> None:
    """Populate the corpus layout config (repo root, taxonomy path, register path,
    register section) from the adopter. The functions below resolve these as module
    globals; call once before active_documents()/check_register()/check_domain_readmes()."""
    global REPO_ROOT, TAXONOMY, REGISTER, REGISTER_SECTION
    REPO_ROOT = ref.repo_root
    TAXONOMY = ref.taxonomy
    REGISTER = ref.register
    REGISTER_SECTION = ref.register_section


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

