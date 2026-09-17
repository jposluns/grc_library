#!/usr/bin/env python3
"""Listing-surface completeness audit - grc wrapper over the pack engine.

Every MECHANICAL listing surface (the central document-index register, each domain
README) must enumerate every active document in its scope.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan (the
regexes, Finding, active_documents, paths_in_section, paths_in_file, is_register_required,
domain_of, check_register, check_domain_readmes) is the source of record in the pack
engine (.corpus-management/tools/gate_lint_listing_surface_completeness.py); it is
layout-free and takes the corpus layout via configure(ref). This wrapper supplies the
grc layout (taxonomy, register, section), configures the engine, and keeps module-global
shims (active_documents / check_register / check_domain_readmes, called by the in-process
regression), Finding, main, and the exit codes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

TAXONOMY = "taxonomy.yml"
REGISTER = "governance/register-document-index-and-classification.md"

# The register lists its documents under one clean index section; the
# domain READMEs vary in section structure, so they are scanned whole.
REGISTER_SECTION = "Active document index"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_listing_surface_completeness  # the pack-owned engine (source of record)
    return gate_lint_listing_surface_completeness


# Configure the engine ONCE with the grc corpus layout.
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    repo_root=REPO_ROOT, taxonomy=TAXONOMY, register=REGISTER, register_section=REGISTER_SECTION))

# Finding is defined in the engine; expose it so main's annotation resolves and the
# in-process regression sees the same dataclass the shims return.
Finding = _engine().Finding


def active_documents():
    """Shim -> engine (engine already configured); kept module-global for the in-process regression."""
    return _engine().active_documents()


def check_register(active):
    """Shim -> engine (engine already configured); kept module-global for the in-process regression."""
    return _engine().check_register(active)


def check_domain_readmes(active):
    """Shim -> engine (engine already configured); kept module-global for the in-process regression."""
    return _engine().check_domain_readmes(active)


def domain_of(path):
    """Shim -> engine (used by main's OK-message domain count)."""
    return _engine().domain_of(path)


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
