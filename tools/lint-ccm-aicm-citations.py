#!/usr/bin/env python3
"""Per-document CSA CCM v4.1.0 / AICM v1.1.0 citation validity - grc wrapper over the pack engine.

Validate every CSA CCM v4.1.0 / AICM v1.1.0 control-code citation in the corpus
against the authoritative catalogue in :mod:`ccm_aicm_reference` (domain validity,
control-number range, per-catalogue title fit, bare-domain and bare-code checks,
and the cross-catalogue title-confusion check).

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the token/heading/context regexes, the helpers, and scan_file) is the
source of record in the pack engine
(.corpus-management/tools/gate_lint_ccm_aicm_citations.py); it is catalogue-agnostic
and takes the reference via configure(ref). This wrapper imports the shared grc
reference catalogue, configures the engine with it, and keeps the grc scan scope
(main's iter_markdown_targets over REPO_ROOT with EXEMPT_FILES), the module-global
scan_file(path) shim, the reporting, and the exit codes.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

try:
    from ccm_aicm_reference import (  # noqa: E402  # grc reference catalogue (fair-use citation index)
        AICM_V11,
        ALL_TITLES,
        CCM_V41,
        DOMAIN_NAMES,
        KNOWN_BAD_DOMAINS,
        VALID_DOMAINS,
    )
except ImportError as exc:  # pragma: no cover - import guard
    print(f"ERROR: cannot load ccm_aicm_reference: {exc}", file=sys.stderr)
    sys.exit(2)

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ccm_aicm_citations  # the pack-owned engine (source of record)
    return gate_lint_ccm_aicm_citations


# Configure the engine ONCE with the grc CCM/AICM reference catalogue. The engine
# builds every derived structure (CCM_FAMILY, the bare-code/bare-domain regexes,
# DIVERGENT_CONTROLS) from this, verbatim from the original gate's module level.
_engine().configure(types.SimpleNamespace(
    VALID_DOMAINS=VALID_DOMAINS,
    KNOWN_BAD_DOMAINS=KNOWN_BAD_DOMAINS,
    CCM_V41=CCM_V41,
    AICM_V11=AICM_V11,
    ALL_TITLES=ALL_TITLES,
    DOMAIN_NAMES=DOMAIN_NAMES,
))

# Meta-documents whose purpose is to describe this gate's rule set inevitably
# contain the codes the gate searches for; they are exempted by name (kept
# wrapper-side, grc scan config).
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
    "TODO.md",
    "TODO-REFERENCE.md",
})


def scan_file(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan.

    Kept as a module-global because a regression test may call ``mod.scan_file(path)``
    directly; the engine is already configured with the grc reference at import.
    """
    return _engine().scan_file(path)


def main(argv: list[str]) -> int:
    paths = argv[1:] or [str(REPO_ROOT)]
    targets = iter_markdown_targets(
        paths, exempt_dirs=DEFAULT_EXEMPT_DIRS, exempt_files=EXEMPT_FILES)
    all_findings: list = []
    for path in targets:
        all_findings.extend(scan_file(path))

    if not all_findings:
        print(
            f"OK: CCM/AICM citations valid across {len(targets)} files "
            f"({len(VALID_DOMAINS)} domains, {len(ALL_TITLES)} controls in the "
            f"CCM v4.1.0 / AICM v1.1.0 reference).")
        return 0

    by_file: dict = {}
    for f in all_findings:
        by_file.setdefault(f.path, []).append(f)
    for path in sorted(by_file):
        print(f"=== {path.relative_to(REPO_ROOT).as_posix()} ===")
        for f in by_file[path]:
            print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(all_findings)} CCM/AICM citation issue(s) across "
        f"{len(by_file)} file(s). The authoritative reference is "
        f"tools/ccm_aicm_reference.py (CSA CCM v4.1.0 / AICM v1.1.0).",
        file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
